from __future__ import annotations

import copy
import hashlib
import importlib
import inspect
import json
import shutil
import subprocess
import sys
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.memory_episode import (
    ObservationalMemoryEpisode,
    is_factory_attested_memory_episode,
    produce_observational_memory_episode,
)
from src.research_findings import ResearchFindings
from src.research_run_evidence import ResearchRunEvidence
from tests.research_runtime_fixture import coherent_runtime_inputs


P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
RECORD_SCHEMA = "P1_5_DURABLE_MEMORY_RECORD_V1"
RECEIPT_SCHEMA = "P1_5_WITNESSED_MEMORY_RECEIPT_V1"
AUTHORITY_ID = "P1_5_TEST_CAPTURE_AUTHORITY_V1"
HEX = set("0123456789abcdef")


def _canonical(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        + b"\n"
    )


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _p15():
    """Load the not-yet-implemented P1.5 candidate.

    This breaker is deliberately committed before the runtime candidate.  The
    first governed run MUST therefore fail here instead of silently accepting a
    serialization-only bridge.
    """
    try:
        module = importlib.import_module("src.memory_interprocess")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.5 candidate absent — expected pre-implementation FAIL: "
            "src.memory_interprocess does not exist",
            pytrace=False,
        )
        raise AssertionError from exc

    required = (
        "persist_witnessed_memory_episode",
        "reattest_persisted_memory_episode",
        "is_factory_attested_historical_memory",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.5 candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P15_CONTRACT
    assert getattr(module, "RECORD_SCHEMA", None) == RECORD_SCHEMA
    assert getattr(module, "RECEIPT_SCHEMA", None) == RECEIPT_SCHEMA
    return module


def _coherent_episode(
    *, decision_payload: str = "HOLD", behavior: str = "NO_ACTION", outcome: str = "OBSERVED"
):
    evidence, context = coherent_runtime_inputs()
    decision = produce_decision(evidence, context=context, decision=decision_payload)
    action = engage_qualification_action(decision, behavior=behavior)
    result = observe_qualification_result(action, outcome=outcome)
    trace = produce_decision_trace(evidence, decision, action, result)
    episode = produce_observational_memory_episode(trace, action, result)
    return evidence, context, decision, action, result, trace, episode


def _manual_episode(source: ObservationalMemoryEpisode) -> ObservationalMemoryEpisode:
    return ObservationalMemoryEpisode(**asdict(source))


def _capture(tmp_path: Path, episode: object | None = None, *, authority_id: str = AUTHORITY_ID):
    module = _p15()
    if episode is None:
        *_, episode = _coherent_episode()
    capture = module.persist_witnessed_memory_episode(
        tmp_path,
        episode,
        authority_id=authority_id,
    )
    for name in ("record_path", "receipt_path", "receipt_sha256", "registration_id"):
        assert hasattr(capture, name), name
    assert len(capture.receipt_sha256) == 64 and set(capture.receipt_sha256) <= HEX
    assert Path(capture.record_path).is_file()
    assert Path(capture.receipt_path).is_file()
    return capture, episode


def _reattest(capture, **overrides):
    module = _p15()
    kwargs = {
        "expected_contract_id": P15_CONTRACT,
        "expected_authority_id": AUTHORITY_ID,
        "expected_receipt_sha256": capture.receipt_sha256,
    }
    kwargs.update(overrides)
    return module.reattest_persisted_memory_episode(
        capture.record_path,
        capture.receipt_path,
        **kwargs,
    )


def _load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write(path: Path, document: dict) -> None:
    path.write_bytes(_canonical(document))


def _p14_episode_id(episode_document: dict) -> str:
    content = dict(episode_document)
    content.pop("episode_id", None)
    payload = {"contract": "P1_4_TRACE_MEMORY_EPISODE_BOUNDARY_V1", "content": content}
    return "MEP-" + hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()[:32]


def _assert_receipt_shape(receipt: dict) -> None:
    assert set(receipt) == {
        "schema",
        "contract_id",
        "authority_id",
        "registration_id",
        "capture_nonce",
        "episode_id",
        "record_sha256",
    }
    assert receipt["schema"] == RECEIPT_SCHEMA
    assert receipt["contract_id"] == P15_CONTRACT
    assert isinstance(receipt["capture_nonce"], str) and len(receipt["capture_nonce"]) >= 32
    assert set(receipt["capture_nonce"].lower()) <= HEX


# A — Only an exact, still-attested P1.4 episode may be captured.


def test_a0_exact_p14_episode_is_the_only_positive_capture_source(tmp_path: Path) -> None:
    capture, episode = _capture(tmp_path)
    assert is_factory_attested_memory_episode(episode)
    assert capture.registration_id != episode.episode_id


def test_a1_manual_same_valued_episode_is_rejected(tmp_path: Path) -> None:
    *_, episode = _coherent_episode()
    forged = _manual_episode(episode)
    assert forged == episode and forged is not episode
    with pytest.raises((TypeError, ValueError)):
        _p15().persist_witnessed_memory_episode(tmp_path, forged, authority_id=AUTHORITY_ID)


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_a2_copy_or_deepcopy_episode_is_rejected(tmp_path: Path, copier) -> None:
    *_, episode = _coherent_episode()
    copied = copier(episode)
    assert copied == episode and copied is not episode
    with pytest.raises((TypeError, ValueError)):
        _p15().persist_witnessed_memory_episode(tmp_path, copied, authority_id=AUTHORITY_ID)


def test_a2_replace_episode_is_rejected(tmp_path: Path) -> None:
    *_, episode = _coherent_episode()
    copied = replace(episode, episode_id=episode.episode_id)
    assert copied == episode and copied is not episode
    with pytest.raises((TypeError, ValueError)):
        _p15().persist_witnessed_memory_episode(tmp_path, copied, authority_id=AUTHORITY_ID)


def test_a3_dictionary_or_json_episode_is_rejected(tmp_path: Path) -> None:
    *_, episode = _coherent_episode()
    with pytest.raises((TypeError, ValueError)):
        _p15().persist_witnessed_memory_episode(tmp_path, asdict(episode), authority_id=AUTHORITY_ID)
    with pytest.raises((TypeError, ValueError)):
        _p15().persist_witnessed_memory_episode(
            tmp_path, json.dumps(asdict(episode)), authority_id=AUTHORITY_ID
        )


def test_a4_mutated_now_unattested_episode_is_rejected(tmp_path: Path) -> None:
    *_, episode = _coherent_episode()
    object.__setattr__(episode, "outcome", "MUTATED_AFTER_P1_4")
    assert not is_factory_attested_memory_episode(episode)
    with pytest.raises((TypeError, ValueError)):
        _p15().persist_witnessed_memory_episode(tmp_path, episode, authority_id=AUTHORITY_ID)


# B — Record/receipt bytes are evidence, never self-authorizing authority.


def test_b0_record_without_receipt_cannot_reattest(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _p15().reattest_persisted_memory_episode(
            capture.record_path,
            None,
            expected_contract_id=P15_CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=capture.receipt_sha256,
        )


def test_b1_receipt_without_record_cannot_reattest(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _p15().reattest_persisted_memory_episode(
            None,
            capture.receipt_path,
            expected_contract_id=P15_CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=capture.receipt_sha256,
        )


def test_b2_internally_coherent_bundle_without_external_pin_is_rejected(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    with pytest.raises(TypeError):
        _p15().reattest_persisted_memory_episode(capture.record_path, capture.receipt_path)


def test_b3_rehashed_tamper_is_rejected_against_original_external_pin(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    record = _load(capture.record_path)
    receipt = _load(capture.receipt_path)
    _assert_receipt_shape(receipt)

    assert record["schema"] == RECORD_SCHEMA
    record["episode"]["outcome"] = "FORGED_AFTER_CAPTURE"
    record["episode"]["episode_id"] = _p14_episode_id(record["episode"])
    forged_record = tmp_path / "forged-record.json"
    _write(forged_record, record)

    receipt["episode_id"] = record["episode"]["episode_id"]
    receipt["record_sha256"] = _sha256(forged_record.read_bytes())
    # Keep the original capture nonce but make registration content-bound again.
    payload = {
        "contract_id": receipt["contract_id"],
        "authority_id": receipt["authority_id"],
        "capture_nonce": receipt["capture_nonce"],
        "episode_id": receipt["episode_id"],
        "record_sha256": receipt["record_sha256"],
    }
    receipt["registration_id"] = "MREG-" + _sha256(_canonical(payload))[:32]
    forged_receipt = tmp_path / "forged-receipt.json"
    _write(forged_receipt, receipt)

    with pytest.raises((TypeError, ValueError)):
        _p15().reattest_persisted_memory_episode(
            forged_record,
            forged_receipt,
            expected_contract_id=P15_CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=capture.receipt_sha256,
        )


def test_b4_storage_path_is_not_trust_root_and_relocation_preserves_exact_bundle(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path / "source")
    relocated = tmp_path / "looks-trusted" / "git" / "memory"
    relocated.mkdir(parents=True)
    record_copy = relocated / Path(capture.record_path).name
    receipt_copy = relocated / Path(capture.receipt_path).name
    shutil.copyfile(capture.record_path, record_copy)
    shutil.copyfile(capture.receipt_path, receipt_copy)

    bundle = _p15().reattest_persisted_memory_episode(
        record_copy,
        receipt_copy,
        expected_contract_id=P15_CONTRACT,
        expected_authority_id=AUTHORITY_ID,
        expected_receipt_sha256=capture.receipt_sha256,
    )
    assert _p15().is_factory_attested_historical_memory(bundle)


# C — Trust expectations must be supplied outside the verified bundle.


def test_c0_exact_external_contract_authority_and_receipt_pin_verify(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    bundle = _reattest(capture)
    assert _p15().is_factory_attested_historical_memory(bundle)


def test_c1_wrong_external_receipt_pin_is_rejected(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    wrong = "0" * 64
    assert wrong != capture.receipt_sha256
    with pytest.raises((TypeError, ValueError)):
        _reattest(capture, expected_receipt_sha256=wrong)


def test_c2_wrong_external_authority_is_rejected(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _reattest(capture, expected_authority_id="FOREIGN_CAPTURE_AUTHORITY")


def test_c3_wrong_external_contract_is_rejected(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _reattest(capture, expected_contract_id="P1_5_FORGED_CONTRACT_V999")


def test_c4_bundle_cannot_supply_its_own_expected_trust_values(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    receipt = _load(capture.receipt_path)
    receipt["expected_contract_id"] = P15_CONTRACT
    receipt["expected_authority_id"] = AUTHORITY_ID
    receipt["expected_receipt_sha256"] = "self-authorizing"
    forged = tmp_path / "self-authorizing-receipt.json"
    _write(forged, receipt)
    forged_pin = _sha256(forged.read_bytes())
    with pytest.raises((TypeError, ValueError)):
        _p15().reattest_persisted_memory_episode(
            capture.record_path,
            forged,
            expected_contract_id=P15_CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=forged_pin,
        )


# D — Fresh-process verification witnesses history; it never replays/resurrects it.


def test_d0_fresh_process_exact_external_pin_mints_fresh_local_historical_attestation(
    tmp_path: Path,
) -> None:
    capture, _ = _capture(tmp_path)
    script = r'''
import sys
from src.memory_interprocess import (
    reattest_persisted_memory_episode,
    is_factory_attested_historical_memory,
)
bundle = reattest_persisted_memory_episode(
    sys.argv[1],
    sys.argv[2],
    expected_contract_id=sys.argv[3],
    expected_authority_id=sys.argv[4],
    expected_receipt_sha256=sys.argv[5],
)
assert is_factory_attested_historical_memory(bundle)
print("PASS: fresh process minted historical-memory attestation from external receipt pin")
'''
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
            str(capture.record_path),
            str(capture.receipt_path),
            P15_CONTRACT,
            AUTHORITY_ID,
            capture.receipt_sha256,
        ],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "PASS:" in completed.stdout


def test_d1_raw_deserialized_episode_remains_unattested(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    raw = ObservationalMemoryEpisode(**_load(capture.record_path)["episode"])
    assert not is_factory_attested_memory_episode(raw)
    assert not _p15().is_factory_attested_historical_memory(raw)


def test_d2_reattest_api_has_no_action_result_replay_inputs(tmp_path: Path) -> None:
    module = _p15()
    signature = inspect.signature(module.reattest_persisted_memory_episode)
    assert set(signature.parameters) == {
        "record_path",
        "receipt_path",
        "expected_contract_id",
        "expected_authority_id",
        "expected_receipt_sha256",
    }
    capture, _ = _capture(tmp_path)
    _, _, _, action, result, _, _ = _coherent_episode()
    with pytest.raises(TypeError):
        module.reattest_persisted_memory_episode(
            capture.record_path,
            capture.receipt_path,
            expected_contract_id=P15_CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=capture.receipt_sha256,
            action=action,
            result=result,
        )


def test_d3_new_same_content_episode_gets_new_registration_not_old_registration(tmp_path: Path) -> None:
    _, _, _, action, result, trace, first = _coherent_episode()
    second = produce_observational_memory_episode(trace, action, result)
    assert first.episode_id == second.episode_id
    assert first is not second
    first_capture, _ = _capture(tmp_path / "first", first)
    second_capture, _ = _capture(tmp_path / "second", second)
    assert first_capture.registration_id != second_capture.registration_id


def test_d4_fresh_local_historical_object_is_not_original_p14_object_resurrected(tmp_path: Path) -> None:
    capture, original = _capture(tmp_path)
    bundle = _reattest(capture)
    assert _p15().is_factory_attested_historical_memory(bundle)
    assert hasattr(bundle, "episode")
    assert bundle.episode == original
    assert bundle.episode is not original
    assert not is_factory_attested_memory_episode(bundle.episode)


# E — Registration identity is content-bound but not experimental independence.


def test_e0_registration_identity_is_distinct_from_episode_content_identity(tmp_path: Path) -> None:
    capture, episode = _capture(tmp_path)
    assert capture.registration_id != episode.episode_id
    receipt = _load(capture.receipt_path)
    _assert_receipt_shape(receipt)
    assert receipt["registration_id"] == capture.registration_id


def test_e1_two_registrations_same_content_are_not_two_independent_experiments(tmp_path: Path) -> None:
    _, _, _, action, result, trace, first = _coherent_episode()
    second = produce_observational_memory_episode(trace, action, result)
    first_capture, _ = _capture(tmp_path / "one", first)
    second_capture, _ = _capture(tmp_path / "two", second)
    assert first.episode_id == second.episode_id
    assert first_capture.registration_id != second_capture.registration_id
    for bundle in (_reattest(first_capture), _reattest(second_capture)):
        assert not hasattr(bundle, "independent")
        assert not hasattr(bundle, "independent_experiment")


def test_e2_physical_copy_of_bundle_does_not_create_new_registration(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path / "original")
    copied = tmp_path / "copy"
    copied.mkdir()
    record_copy = copied / Path(capture.record_path).name
    receipt_copy = copied / Path(capture.receipt_path).name
    shutil.copyfile(capture.record_path, record_copy)
    shutil.copyfile(capture.receipt_path, receipt_copy)
    bundle = _p15().reattest_persisted_memory_episode(
        record_copy,
        receipt_copy,
        expected_contract_id=P15_CONTRACT,
        expected_authority_id=AUTHORITY_ID,
        expected_receipt_sha256=capture.receipt_sha256,
    )
    assert bundle.registration_id == capture.registration_id


def test_e3_registration_id_is_content_bound_and_rebinding_fails_closed(tmp_path: Path) -> None:
    first, _ = _capture(tmp_path / "first")
    second, _ = _capture(tmp_path / "second")
    assert first.registration_id != second.registration_id

    receipt = _load(second.receipt_path)
    receipt["registration_id"] = first.registration_id
    rebound = tmp_path / "rebound-receipt.json"
    _write(rebound, receipt)
    rebound_pin = _sha256(rebound.read_bytes())
    with pytest.raises((TypeError, ValueError)):
        _p15().reattest_persisted_memory_episode(
            second.record_path,
            rebound,
            expected_contract_id=P15_CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=rebound_pin,
        )


def test_e4_pin_for_one_registration_cannot_authorize_another(tmp_path: Path) -> None:
    first, _ = _capture(tmp_path / "first")
    second, _ = _capture(tmp_path / "second")
    with pytest.raises((TypeError, ValueError)):
        _p15().reattest_persisted_memory_episode(
            second.record_path,
            second.receipt_path,
            expected_contract_id=P15_CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=first.receipt_sha256,
        )


# F — P1.5 deliberately does not fabricate point-in-time knowledge semantics.


def test_f0_positive_capture_requires_no_caller_supplied_timestamp(tmp_path: Path) -> None:
    module = _p15()
    assert set(inspect.signature(module.persist_witnessed_memory_episode).parameters) == {
        "output_directory",
        "episode",
        "authority_id",
    }
    _capture(tmp_path)


def test_f1_bundle_timestamp_is_not_part_of_minimal_trusted_receipt(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    receipt = _load(capture.receipt_path)
    _assert_receipt_shape(receipt)
    forbidden = {"registered_at", "known_from", "valid_from", "decision_at", "usable_from"}
    assert not (set(receipt) & forbidden)


def test_f2_registration_is_not_known_from(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    bundle = _reattest(capture)
    assert not hasattr(bundle, "known_from")
    assert not hasattr(bundle.episode, "known_from")


def test_f3_receipt_does_not_claim_prior_availability(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    bundle = _reattest(capture)
    for name in ("available_before_decision", "historically_known", "known_at_decision"):
        assert not hasattr(bundle, name)
        assert not hasattr(bundle.episode, name)


def test_f4_missing_qualified_time_is_not_silently_repaired_by_local_clock() -> None:
    source = inspect.getsource(_p15())
    forbidden = ("datetime.now", "datetime.utcnow", "time.time", "registered_at =")
    assert all(token not in source for token in forbidden)


# G — Durable witnessing remains downstream, observational and non-authorizing.


def test_g0_historical_memory_cannot_mint_or_repair_upstream_objects(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    bundle = _reattest(capture)
    _, context, decision, action, result, _, _ = _coherent_episode()
    from src.decision_trace import produce_decision_trace

    with pytest.raises(ValueError):
        produce_decision_trace(bundle, decision, action, result)
    with pytest.raises(ValueError):
        engage_qualification_action(bundle, behavior="NO_ACTION")
    with pytest.raises(ValueError):
        observe_qualification_result(bundle, outcome="OBSERVED")


def test_g1_historical_memory_is_not_research_evidence_or_findings(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    bundle = _reattest(capture)
    assert not isinstance(bundle, ResearchRunEvidence)
    assert not isinstance(bundle, ResearchFindings)
    assert not isinstance(bundle.episode, ResearchRunEvidence)
    assert not isinstance(bundle.episode, ResearchFindings)


def test_g2_receipt_and_historical_memory_do_not_create_knowledge_status(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    bundle = _reattest(capture)
    for value in (bundle, bundle.episode):
        for name in ("knowledge", "validated_knowledge", "status", "supported", "confidence"):
            assert not hasattr(value, name)


def test_g3_receipt_and_historical_memory_never_produce_authorized(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    bundle = _reattest(capture)
    for value in (bundle, bundle.episode):
        assert not hasattr(value, "authorized")
        assert not hasattr(value, "authorization")
    source = inspect.getsource(_p15())
    assert "AUTHORIZED" not in source


def test_g4_p15_candidate_has_no_operational_or_acquisition_surface() -> None:
    source = inspect.getsource(_p15())
    forbidden = (
        "MetaTrader5",
        "mt5.",
        "order_send",
        "requests.",
        "urllib.request",
        ".bi5",
        "create_order(",
        "submit_order(",
        "execute_action(",
        "lot_size",
        "position_size",
        "stop_loss",
        "take_profit",
        "run_backtest(",
        "activate_live(",
    )
    assert all(token not in source for token in forbidden)
