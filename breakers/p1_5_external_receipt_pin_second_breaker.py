from __future__ import annotations

import copy
import hashlib
import inspect
import json
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.memory_episode import (
    ObservationalMemoryEpisode,
    produce_observational_memory_episode,
)
from src.memory_interprocess import (
    CONTRACT,
    RECEIPT_SCHEMA,
    RECORD_SCHEMA,
    HistoricalMemoryEpisode,
    is_factory_attested_historical_memory,
    persist_witnessed_memory_episode,
    reattest_persisted_memory_episode,
)
from tests.research_runtime_fixture import coherent_runtime_inputs


AUTHORITY_ID = "P1_5_TEST_CAPTURE_AUTHORITY_V1"
HEX = set("0123456789abcdef")


def _canonical(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        + b"\n"
    )


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _registration_id(*, authority_id: str, capture_nonce: str, episode_id: str, record_sha256: str) -> str:
    payload = {
        "contract_id": CONTRACT,
        "authority_id": authority_id,
        "capture_nonce": capture_nonce,
        "episode_id": episode_id,
        "record_sha256": record_sha256,
    }
    return "MREG-" + _sha256(_canonical(payload))[:32]


def _coherent_episode(*, outcome: str = "OBSERVED"):
    evidence, context = coherent_runtime_inputs()
    decision = produce_decision(evidence, context=context, decision="HOLD")
    action = engage_qualification_action(decision, behavior="NO_ACTION")
    result = observe_qualification_result(action, outcome=outcome)
    trace = produce_decision_trace(evidence, decision, action, result)
    episode = produce_observational_memory_episode(trace, action, result)
    return episode


def _capture(tmp_path: Path, episode: ObservationalMemoryEpisode | None = None):
    if episode is None:
        episode = _coherent_episode()
    capture = persist_witnessed_memory_episode(tmp_path, episode, authority_id=AUTHORITY_ID)
    return capture, episode


def _reattest(capture):
    return reattest_persisted_memory_episode(
        capture.record_path,
        capture.receipt_path,
        expected_contract_id=CONTRACT,
        expected_authority_id=AUTHORITY_ID,
        expected_receipt_sha256=capture.receipt_sha256,
    )


def _load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write(path: Path, document: dict) -> None:
    path.write_bytes(_canonical(document))


def _receipt_for_record(record_path: Path, source_receipt: dict) -> tuple[Path, str]:
    receipt = dict(source_receipt)
    receipt["record_sha256"] = _sha256(record_path.read_bytes())
    receipt["registration_id"] = _registration_id(
        authority_id=receipt["authority_id"],
        capture_nonce=receipt["capture_nonce"],
        episode_id=receipt["episode_id"],
        record_sha256=receipt["record_sha256"],
    )
    path = record_path.parent / "forged-receipt.json"
    _write(path, receipt)
    return path, _sha256(path.read_bytes())


# H — Canonicalization must have one exact byte representation.


def test_h0_noncanonical_record_is_rejected_even_with_matching_receipt_and_external_pin(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    record = _load(capture.record_path)
    pretty = tmp_path / "pretty-record.json"
    pretty.write_text(json.dumps(record, sort_keys=True, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    forged_receipt, pin = _receipt_for_record(pretty, _load(capture.receipt_path))
    with pytest.raises((TypeError, ValueError)):
        reattest_persisted_memory_episode(
            pretty,
            forged_receipt,
            expected_contract_id=CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=pin,
        )


def test_h1_duplicate_receipt_key_is_rejected_even_when_exact_bytes_are_externally_pinned(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    receipt = _load(capture.receipt_path)
    raw = Path(capture.receipt_path).read_text(encoding="utf-8")
    needle = '"authority_id":' + json.dumps(receipt["authority_id"], ensure_ascii=False) + ","
    assert needle in raw
    duplicate = raw.replace(needle, needle + needle, 1).encode("utf-8")
    forged = tmp_path / "duplicate-key-receipt.json"
    forged.write_bytes(duplicate)
    with pytest.raises((TypeError, ValueError)):
        reattest_persisted_memory_episode(
            capture.record_path,
            forged,
            expected_contract_id=CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=_sha256(duplicate),
        )


def test_h2_unknown_record_field_is_rejected_even_when_receipt_and_pin_are_recomputed(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    record = _load(capture.record_path)
    record["unexpected"] = "FORBIDDEN"
    forged_record = tmp_path / "unknown-field-record.json"
    _write(forged_record, record)
    forged_receipt, pin = _receipt_for_record(forged_record, _load(capture.receipt_path))
    with pytest.raises((TypeError, ValueError)):
        reattest_persisted_memory_episode(
            forged_record,
            forged_receipt,
            expected_contract_id=CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=pin,
        )


def test_h3_unknown_receipt_field_is_rejected_even_when_new_receipt_pin_is_external(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    receipt = _load(capture.receipt_path)
    receipt["unexpected"] = "FORBIDDEN"
    forged = tmp_path / "unknown-field-receipt.json"
    _write(forged, receipt)
    with pytest.raises((TypeError, ValueError)):
        reattest_persisted_memory_episode(
            capture.record_path,
            forged,
            expected_contract_id=CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=_sha256(forged.read_bytes()),
        )


def test_h4_noncanonical_receipt_is_rejected_even_when_exact_bytes_are_externally_pinned(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    receipt = _load(capture.receipt_path)
    pretty = tmp_path / "pretty-receipt.json"
    pretty.write_text(json.dumps(receipt, sort_keys=True, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with pytest.raises((TypeError, ValueError)):
        reattest_persisted_memory_episode(
            capture.record_path,
            pretty,
            expected_contract_id=CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=_sha256(pretty.read_bytes()),
        )


# I — Receipt/registration substitution must fail closed.


def test_i0_receipt_from_different_episode_cannot_authorize_current_record(tmp_path: Path) -> None:
    first, _ = _capture(tmp_path / "first", _coherent_episode(outcome="ONE"))
    second, _ = _capture(tmp_path / "second", _coherent_episode(outcome="TWO"))
    with pytest.raises((TypeError, ValueError)):
        reattest_persisted_memory_episode(
            first.record_path,
            second.receipt_path,
            expected_contract_id=CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=second.receipt_sha256,
        )


def test_i1_transplanted_registration_id_is_rejected_even_with_fresh_external_pin(tmp_path: Path) -> None:
    first, _ = _capture(tmp_path / "first")
    second, _ = _capture(tmp_path / "second")
    receipt = _load(second.receipt_path)
    receipt["registration_id"] = first.registration_id
    forged = tmp_path / "transplanted-registration.json"
    _write(forged, receipt)
    with pytest.raises((TypeError, ValueError)):
        reattest_persisted_memory_episode(
            second.record_path,
            forged,
            expected_contract_id=CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=_sha256(forged.read_bytes()),
        )


def test_i2_receipt_episode_id_substitution_is_rejected(tmp_path: Path) -> None:
    first, first_episode = _capture(tmp_path / "first", _coherent_episode(outcome="ONE"))
    second, _ = _capture(tmp_path / "second", _coherent_episode(outcome="TWO"))
    receipt = _load(second.receipt_path)
    receipt["episode_id"] = first_episode.episode_id
    receipt["registration_id"] = _registration_id(
        authority_id=receipt["authority_id"],
        capture_nonce=receipt["capture_nonce"],
        episode_id=receipt["episode_id"],
        record_sha256=receipt["record_sha256"],
    )
    forged = tmp_path / "episode-substitution.json"
    _write(forged, receipt)
    with pytest.raises((TypeError, ValueError)):
        reattest_persisted_memory_episode(
            second.record_path,
            forged,
            expected_contract_id=CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=_sha256(forged.read_bytes()),
        )
    assert first.registration_id != second.registration_id


def test_i3_registration_id_string_alone_is_never_historical_memory_authority(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    assert not is_factory_attested_historical_memory(capture.registration_id)


# J — Fresh local historical attestation has exact-object lifecycle semantics.


def _manual_historical(bundle: HistoricalMemoryEpisode) -> HistoricalMemoryEpisode:
    episode = ObservationalMemoryEpisode(**asdict(bundle.episode))
    return HistoricalMemoryEpisode(
        episode=episode,
        registration_id=bundle.registration_id,
        authority_id=bundle.authority_id,
        contract_id=bundle.contract_id,
        record_sha256=bundle.record_sha256,
        receipt_sha256=bundle.receipt_sha256,
    )


def test_j0_manual_same_valued_historical_memory_is_not_attested(tmp_path: Path) -> None:
    bundle = _reattest(_capture(tmp_path)[0])
    forged = _manual_historical(bundle)
    assert forged == bundle and forged is not bundle
    assert not is_factory_attested_historical_memory(forged)


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_j1_copy_or_deepcopy_historical_memory_is_not_attested(tmp_path: Path, copier) -> None:
    bundle = _reattest(_capture(tmp_path)[0])
    copied = copier(bundle)
    assert copied == bundle and copied is not bundle
    assert not is_factory_attested_historical_memory(copied)


def test_j1_replace_historical_memory_is_not_attested(tmp_path: Path) -> None:
    bundle = _reattest(_capture(tmp_path)[0])
    copied = replace(bundle, registration_id=bundle.registration_id)
    assert copied == bundle and copied is not bundle
    assert not is_factory_attested_historical_memory(copied)


def test_j2_top_level_mutation_invalidates_fresh_local_attestation(tmp_path: Path) -> None:
    bundle = _reattest(_capture(tmp_path)[0])
    object.__setattr__(bundle, "authority_id", "MUTATED")
    assert not is_factory_attested_historical_memory(bundle)


def test_j3_nested_episode_mutation_invalidates_fresh_local_attestation(tmp_path: Path) -> None:
    bundle = _reattest(_capture(tmp_path)[0])
    object.__setattr__(bundle.episode, "outcome", "MUTATED")
    assert not is_factory_attested_historical_memory(bundle)


def test_j4_reverification_mints_distinct_local_objects_for_same_registration(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    first = _reattest(capture)
    second = _reattest(capture)
    assert first == second
    assert first is not second
    assert first.registration_id == second.registration_id
    assert is_factory_attested_historical_memory(first)
    assert is_factory_attested_historical_memory(second)


def test_j5_post_capture_mutation_of_original_p14_object_does_not_rewrite_durable_snapshot(tmp_path: Path) -> None:
    capture, original = _capture(tmp_path)
    old_outcome = original.outcome
    object.__setattr__(original, "outcome", "MUTATED_AFTER_CAPTURE")
    bundle = _reattest(capture)
    assert bundle.episode.outcome == old_outcome
    assert is_factory_attested_historical_memory(bundle)


# K — Local bundle material must not become an implicit external trust channel.


def test_k0_capture_result_itself_is_not_historical_memory_authority(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    assert not is_factory_attested_historical_memory(capture)


def test_k1_all_external_expectations_are_required_and_have_no_defaults() -> None:
    signature = inspect.signature(reattest_persisted_memory_episode)
    for name in ("expected_contract_id", "expected_authority_id", "expected_receipt_sha256"):
        assert signature.parameters[name].default is inspect.Parameter.empty


def test_k2_receipt_path_cannot_be_confused_with_external_receipt_pin(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        reattest_persisted_memory_episode(
            capture.record_path,
            capture.receipt_path,
            expected_contract_id=CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=capture.receipt_path,
        )


# L — Verification must bind to one in-memory read of each durable artifact.


def test_l0_verifier_reads_record_and_receipt_bytes_once_each() -> None:
    source = inspect.getsource(reattest_persisted_memory_episode)
    assert source.count("record_file.read_bytes()") == 1
    assert source.count("receipt_file.read_bytes()") == 1


def test_l1_post_verification_file_mutation_does_not_mutate_attested_local_snapshot(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    bundle = _reattest(capture)
    snapshot = asdict(bundle)
    Path(capture.record_path).write_bytes(Path(capture.record_path).read_bytes() + b" ")
    Path(capture.receipt_path).write_bytes(Path(capture.receipt_path).read_bytes() + b" ")
    assert asdict(bundle) == snapshot
    assert is_factory_attested_historical_memory(bundle)


def test_l2_preverification_receipt_change_is_rejected_under_original_external_pin(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    Path(capture.receipt_path).write_bytes(Path(capture.receipt_path).read_bytes() + b" ")
    with pytest.raises((TypeError, ValueError)):
        _reattest(capture)


# M — Capture nonce distinguishes registrations but never becomes caller authority.


def test_m0_same_exact_p14_episode_captured_twice_gets_distinct_nonce_registration_and_pin(tmp_path: Path) -> None:
    episode = _coherent_episode()
    first, _ = _capture(tmp_path / "first", episode)
    second, _ = _capture(tmp_path / "second", episode)
    first_receipt = _load(first.receipt_path)
    second_receipt = _load(second.receipt_path)
    assert first_receipt["capture_nonce"] != second_receipt["capture_nonce"]
    assert first.registration_id != second.registration_id
    assert first.receipt_sha256 != second.receipt_sha256


def _forge_nonce_receipt(capture, tmp_path: Path, nonce: str) -> tuple[Path, str]:
    receipt = _load(capture.receipt_path)
    receipt["capture_nonce"] = nonce
    receipt["registration_id"] = _registration_id(
        authority_id=receipt["authority_id"],
        capture_nonce=nonce,
        episode_id=receipt["episode_id"],
        record_sha256=receipt["record_sha256"],
    )
    forged = tmp_path / ("nonce-" + _sha256(nonce.encode("utf-8"))[:8] + ".json")
    _write(forged, receipt)
    return forged, _sha256(forged.read_bytes())


def test_m1_short_capture_nonce_is_rejected_even_with_content_bound_registration_and_pin(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    forged, pin = _forge_nonce_receipt(capture, tmp_path, "ab12")
    with pytest.raises((TypeError, ValueError)):
        reattest_persisted_memory_episode(
            capture.record_path,
            forged,
            expected_contract_id=CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=pin,
        )


def test_m2_nonhex_capture_nonce_is_rejected_even_with_content_bound_registration_and_pin(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    forged, pin = _forge_nonce_receipt(capture, tmp_path, "z" * 64)
    with pytest.raises((TypeError, ValueError)):
        reattest_persisted_memory_episode(
            capture.record_path,
            forged,
            expected_contract_id=CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=pin,
        )


def test_m3_nonce_tamper_without_registration_rebinding_is_rejected_even_with_fresh_pin(tmp_path: Path) -> None:
    capture, _ = _capture(tmp_path)
    receipt = _load(capture.receipt_path)
    original_registration = receipt["registration_id"]
    receipt["capture_nonce"] = "a" * 64 if receipt["capture_nonce"] != "a" * 64 else "b" * 64
    receipt["registration_id"] = original_registration
    forged = tmp_path / "nonce-tamper.json"
    _write(forged, receipt)
    with pytest.raises((TypeError, ValueError)):
        reattest_persisted_memory_episode(
            capture.record_path,
            forged,
            expected_contract_id=CONTRACT,
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=_sha256(forged.read_bytes()),
        )


def test_m4_capture_nonce_is_not_a_caller_supplied_parameter() -> None:
    assert "capture_nonce" not in inspect.signature(persist_witnessed_memory_episode).parameters
