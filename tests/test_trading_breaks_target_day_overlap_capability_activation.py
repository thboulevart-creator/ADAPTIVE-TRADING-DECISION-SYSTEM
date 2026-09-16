from __future__ import annotations

from datetime import date

from tools.activate_trading_breaks_target_day_overlap_capability import (
    NEW_CAPABILITY_ID,
    NEW_FINGERPRINT,
    OLD_FINGERPRINT,
    proposed_capability,
    proposed_change,
    validate_activation_preconditions,
)
from tools.trading_breaks_recovery_progression import (
    actual_changed_dimensions,
    load_attempt_ledger,
    validate_material_capability_change,
)
from tools.trading_breaks_target_day_overlap_semantics import (
    ADDRESSES_BLOCKER,
    CLASS_A_SOURCES,
    QUALIFIED_PROOF_CAPABILITY,
)


def test_proposed_v2_identity_is_exact_and_monotonic():
    capabilities, current_id, _ = load_attempt_ledger()
    old = capabilities[current_id]
    new = proposed_capability()
    assert current_id == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert old.fingerprint() == OLD_FINGERPRINT
    assert NEW_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2"
    assert new.fingerprint() == NEW_FINGERPRINT
    assert old.route_contract == new.route_contract
    assert old.capture_implementation == new.capture_implementation
    assert old.protocol_contract != new.protocol_contract
    assert old.proof_capabilities < new.proof_capabilities
    assert new.proof_capabilities - old.proof_capabilities == {QUALIFIED_PROOF_CAPABILITY}
    assert actual_changed_dimensions(old, new) == frozenset({"protocol_contract", "proof_capabilities"})


def test_change_registry_candidate_is_exactly_scoped_to_class_a_blocker():
    change = proposed_change()
    assert change.from_fingerprint == OLD_FINGERPRINT
    assert change.to_fingerprint == NEW_FINGERPRINT
    assert change.changed_dimensions == frozenset({"protocol_contract", "proof_capabilities"})
    assert change.added_proof_capabilities == frozenset({QUALIFIED_PROOF_CAPABILITY})
    assert change.addresses_blocking_reasons == frozenset({ADDRESSES_BLOCKER})
    assert change.qualification_contract == "TRADING_BREAKS_TARGET_DAY_OVERLAP_ATTRIBUTION_V1"
    assert change.qualification_commit == "061e97d90eed2c4c3f1d5f2a261e457fd796413f"


def test_material_change_is_proven_for_all_14_class_a_latest_attempts_only():
    _, _, attempts = load_attempt_ledger()
    latest = {}
    for item in attempts:
        latest[item.target_date] = item
    new = proposed_capability()
    change = proposed_change()
    class_a_days = {day for day, _, _ in CLASS_A_SOURCES}
    assert len(class_a_days) == 14
    for day in class_a_days:
        attempt = latest[day]
        assert attempt.outcome == "BLOCKED"
        assert attempt.blocking_reason == ADDRESSES_BLOCKER
        assert validate_material_capability_change(attempt, new, change) == (
            True,
            "MATERIAL_CAPABILITY_CHANGE_PROVEN",
        )

    class_b_days = {
        date(2021, 12, 31),
        date(2022, 7, 1),
        date(2026, 7, 2),
    }
    for day in class_b_days:
        attempt = latest[day]
        valid, reason = validate_material_capability_change(attempt, new, change)
        assert valid is False
        assert reason == "BLOCKING_REASON_NOT_EXPLICITLY_ADDRESSED"


def test_activation_preconditions_prove_68_attempts_immutable_and_split_14_plus_3():
    state = validate_activation_preconditions()
    assert state == {
        "old_capability_id": "TRADING_BREAKS_PRIMARY_WIDGET_V1",
        "old_fingerprint": OLD_FINGERPRINT,
        "new_capability_id": NEW_CAPABILITY_ID,
        "new_fingerprint": NEW_FINGERPRINT,
        "attempt_count": 68,
        "class_a_retry_qualified": 14,
        "class_b_still_unaddressed": 3,
    }
