from dataclasses import replace
from datetime import date

import tools.trading_breaks_target_day_overlap_semantics as semantics
from tools.trading_breaks_recovery_progression import load_attempt_ledger

PROVENANCE_KEYS = (
    "workflow_run",
    "job_id",
    "artifact_id",
    "artifact_sha256",
    "probe_commit",
)


def _source_attempt(attempts, attempt_id):
    return next(item for item in attempts if item.attempt_id == attempt_id)


def _assert_governed_provenance(runtime_provenance, source_provenance):
    assert {key: runtime_provenance[key] for key in PROVENANCE_KEYS} == {
        key: source_provenance[key] for key in PROVENANCE_KEYS
    }


def test_class_a_loader_binds_exact_historical_source_attempts():
    loaded = semantics.load_class_a_evidence()
    _, _, attempts = load_attempt_ledger()
    attempts_by_id = {item.attempt_id: item for item in attempts}
    assert len(loaded) == 14
    for day, reason, _raw, provenance, batch in loaded:
        attempt_id = f"batch{batch:02d}:{day.isoformat()}"
        source = attempts_by_id[attempt_id]
        assert source.target_date == day
        assert source.candidate_reason == reason
        assert source.outcome == "BLOCKED"
        assert source.blocking_reason == semantics.ADDRESSES_BLOCKER
        assert source.capability_id == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
        _assert_governed_provenance(provenance, source.provenance)


def test_later_v2_retry_cannot_shadow_immutable_class_a_source(monkeypatch):
    capabilities, current_id, attempts = load_attempt_ledger()
    target = date(2021, 12, 24)
    source = _source_attempt(attempts, "batch02:2021-12-24")
    v2 = capabilities[current_id]
    synthetic_retry = replace(
        source,
        attempt_sequence=999,
        attempt_id="synthetic-overlap-v2:2021-12-24",
        batch_contract="SYNTHETIC_POST_SOURCE_RETRY",
        outcome="PASS",
        adjudication_reason="TARGET_DAY_OVERLAP_PRIMARY_BROKER_INTERVAL_VALIDATED",
        blocking_reason=None,
        capability_id=current_id,
        capability=v2,
    )
    monkeypatch.setattr(
        semantics,
        "load_attempt_ledger",
        lambda: (capabilities, current_id, [*attempts, synthetic_retry]),
    )
    loaded = semantics.load_class_a_evidence()
    row = next(item for item in loaded if item[0] == target)
    _assert_governed_provenance(row[3], source.provenance)
    assert semantics.qualify_class_a()["class_a_count"] == 14


def test_wrong_source_attempt_identity_is_rejected(monkeypatch):
    capabilities, current_id, attempts = load_attempt_ledger()
    source = _source_attempt(attempts, "batch02:2021-12-24")
    corrupted = [
        replace(item, candidate_reason="CORRUPTED") if item.attempt_id == source.attempt_id else item
        for item in attempts
    ]
    monkeypatch.setattr(semantics, "load_attempt_ledger", lambda: (capabilities, current_id, corrupted))
    try:
        semantics.load_class_a_evidence()
    except ValueError as exc:
        assert str(exc).startswith("CLASS_A_SOURCE_ATTEMPT_IDENTITY_MISMATCH")
    else:
        raise AssertionError("corrupted source attempt was accepted")
