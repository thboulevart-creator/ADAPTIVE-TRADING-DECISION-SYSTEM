from __future__ import annotations

from datetime import date

from tools.activate_trading_breaks_target_day_overlap_capability import (
    NEW_CAPABILITY_ID,
    NEW_FINGERPRINT,
    OLD_CAPABILITY_ID,
    OLD_FINGERPRINT,
)
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue
from tools.trading_breaks_target_day_overlap_semantics import CLASS_A_SOURCES


def test_v2_state_has_exact_capability_registry_and_immutable_attempt_history():
    capabilities, current_id, attempts = load_attempt_ledger()
    assert current_id == NEW_CAPABILITY_ID
    assert set(capabilities) == {OLD_CAPABILITY_ID, NEW_CAPABILITY_ID}
    assert capabilities[OLD_CAPABILITY_ID].fingerprint() == OLD_FINGERPRINT
    assert capabilities[NEW_CAPABILITY_ID].fingerprint() == NEW_FINGERPRINT
    assert len(attempts) == 68
    assert [item.attempt_sequence for item in attempts] == list(range(1, 69))
    assert len({item.attempt_id for item in attempts}) == 68
    changes = load_material_capability_changes()
    assert len(changes) == 1
    change = changes[0]
    assert change.from_fingerprint == OLD_FINGERPRINT
    assert change.to_fingerprint == NEW_FINGERPRINT
    assert change.changed_dimensions == frozenset({"protocol_contract", "proof_capabilities"})
    assert change.added_proof_capabilities == frozenset({"QUALIFIED_CROSS_DATE_INTERVAL_ATTRIBUTION"})
    assert change.addresses_blocking_reasons == frozenset({"NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"})


def test_v2_progression_exposes_exactly_14_class_a_retries_and_only_three_class_b_ineligible():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    expected = sorted((day, reason) for day, reason, _ in CLASS_A_SOURCES)
    assert len(recovery_queue()) == len(decisions) == 17
    assert eligible == expected
    assert len(eligible) == 14
    by_day = {item.target_date: item for item in decisions}
    for day, reason, _ in CLASS_A_SOURCES:
        d = by_day[day]
        assert d.candidate_reason == reason
        assert d.latest_attempt_outcome == "BLOCKED"
        assert d.eligible is True
        assert d.reason == "MATERIAL_CAPABILITY_CHANGE_RETRY"
        assert d.contract_verdict == "PASS"

    class_b = (date(2021, 12, 31), date(2022, 7, 1), date(2026, 7, 2))
    for day in class_b:
        d = by_day[day]
        assert d.latest_attempt_outcome == "BLOCKED"
        assert d.eligible is False
        assert d.reason == "RETRY_MATERIAL_CHANGE_NOT_PROVEN:BLOCKING_REASON_NOT_EXPLICITLY_ADDRESSED"
        assert d.contract_verdict == "PASS"
    assert sum((not d.eligible) and d.latest_attempt_outcome == "BLOCKED" for d in decisions) == 3
