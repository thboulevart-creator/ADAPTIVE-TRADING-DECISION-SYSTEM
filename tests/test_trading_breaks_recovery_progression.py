from __future__ import annotations

import inspect
from dataclasses import replace
from datetime import date

from tools.trading_breaks_recovery_progression import (
    AttemptRecord,
    CapabilityIdentity,
    MaterialCapabilityChange,
    actual_changed_dimensions,
    current_capability,
    eligible_recovery_queue,
    eligibility_for_unresolved_candidate,
    load_attempt_ledger,
    progression_decisions,
    validate_material_capability_change,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


def _latest(target: date) -> AttemptRecord:
    _, _, attempts = load_attempt_ledger()
    return max(
        (item for item in attempts if item.target_date == target),
        key=lambda item: item.attempt_sequence,
    )


def _capability_with_added(base: CapabilityIdentity, capability: str) -> CapabilityIdentity:
    return replace(
        base,
        proof_capabilities=base.proof_capabilities | frozenset({capability}),
    )


def _change(
    previous: AttemptRecord,
    new: CapabilityIdentity,
    *,
    added: str,
    addresses: str | None = None,
    changed_dimensions: frozenset[str] | None = None,
    from_fingerprint: str | None = None,
    to_fingerprint: str | None = None,
) -> MaterialCapabilityChange:
    blocker = addresses or previous.blocking_reason
    return MaterialCapabilityChange(
        change_id="TEST_MATERIAL_CHANGE_V1",
        from_fingerprint=from_fingerprint or previous.capability.fingerprint(),
        to_fingerprint=to_fingerprint or new.fingerprint(),
        changed_dimensions=(
            changed_dimensions
            if changed_dimensions is not None
            else actual_changed_dimensions(previous.capability, new)
        ),
        added_proof_capabilities=frozenset({added}),
        addresses_blocking_reasons=frozenset({blocker}) if blocker else frozenset(),
    )


def test_attempt_ledger_preserves_all_ten_historical_attempts_and_duplicate_history():
    capabilities, current_id, attempts = load_attempt_ledger()
    assert current_id == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert current_id in capabilities
    assert len(attempts) == 10
    assert [item.attempt_sequence for item in attempts] == list(range(1, 11))
    assert len({item.attempt_id for item in attempts}) == 10

    christmas = [x for x in attempts if x.target_date == date(2021, 12, 24)]
    new_year = [x for x in attempts if x.target_date == date(2021, 12, 31)]
    assert [x.attempt_id for x in christmas] == [
        "batch01:2021-12-24",
        "batch02:2021-12-24",
    ]
    assert [x.attempt_id for x in new_year] == [
        "batch01:2021-12-31",
        "batch02:2021-12-31",
    ]
    assert len({x.capability.fingerprint() for x in christmas + new_year}) == 1


def test_attempted_blocked_dates_remain_unresolved_calendar_candidates():
    queue_days = {day for day, _ in recovery_queue()}
    assert date(2021, 12, 24) in queue_days
    assert date(2021, 12, 31) in queue_days
    assert date(2022, 4, 15) in queue_days


def test_progression_plan_covers_every_unresolved_candidate_without_hidden_skipping():
    queue = recovery_queue()
    decisions = progression_decisions()
    assert [(d.target_date, d.candidate_reason) for d in decisions] == queue
    assert len(decisions) == len(queue) == 61
    assert all(d.calendar_state == "UNRESOLVED" for d in decisions)


def test_unchanged_capability_forbids_third_retry_of_historical_blocked_dates():
    decisions = {d.target_date: d for d in progression_decisions()}
    for target in (date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15)):
        decision = decisions[target]
        assert decision.eligible is False
        assert decision.latest_attempt_outcome == "BLOCKED"
        assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
        assert decision.contract_verdict == "PASS"


def test_ineligible_blocked_prefix_does_not_starve_later_never_attempted_candidates():
    eligible = eligible_recovery_queue()
    assert eligible
    assert eligible[0] == (date(2022, 5, 30), "MEMORIAL_DAY")
    eligible_days = {day for day, _ in eligible}
    assert date(2021, 12, 24) not in eligible_days
    assert date(2021, 12, 31) not in eligible_days
    assert date(2022, 4, 15) not in eligible_days
    assert date(2022, 5, 30) in eligible_days


def test_execution_projection_preserves_chronology_and_has_no_manual_priority_input():
    decisions = progression_decisions()
    expected_projection = [
        (d.target_date, d.candidate_reason)
        for d in decisions
        if d.eligible and d.contract_verdict == "PASS"
    ]
    assert eligible_recovery_queue() == expected_projection
    assert expected_projection == sorted(expected_projection, key=lambda item: item[0])
    parameters = inspect.signature(eligible_recovery_queue).parameters
    assert "expected_outcome" not in parameters
    assert "priority" not in parameters
    assert "manual_skip" not in parameters


def test_new_run_artifact_or_probe_commit_cannot_change_semantic_capability():
    previous = _latest(date(2021, 12, 31))
    altered_provenance = dict(previous.provenance)
    altered_provenance.update(
        workflow_run=999999,
        job_id=888888,
        artifact_id=777777,
        artifact_sha256="a" * 64,
        probe_commit="b" * 40,
    )
    replay = replace(
        previous,
        attempt_sequence=99,
        attempt_id="synthetic:new-provenance-same-capability",
        provenance=altered_provenance,
    )
    base = current_capability()
    assert replay.capability.fingerprint() == base.fingerprint()
    decision = eligibility_for_unresolved_candidate(
        replay.target_date,
        replay.candidate_reason,
        [replay],
        base,
    )
    assert decision.eligible is False
    assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"


def test_version_string_only_change_without_new_proof_capability_is_not_material():
    previous = _latest(date(2021, 12, 31))
    base = previous.capability
    renamed = replace(base, route_contract=base.route_contract + "_V2_LABEL_ONLY")
    change = MaterialCapabilityChange(
        change_id="LABEL_ONLY_V2",
        from_fingerprint=base.fingerprint(),
        to_fingerprint=renamed.fingerprint(),
        changed_dimensions=frozenset({"route_contract"}),
        added_proof_capabilities=frozenset(),
        addresses_blocking_reasons=frozenset({previous.blocking_reason}),
    )
    valid, reason = validate_material_capability_change(previous, renamed, change)
    assert valid is False
    assert reason == "NEW_PROOF_CAPABILITY_NOT_PROVEN"


def test_unrelated_added_capability_cannot_be_claimed_as_retry_justification():
    previous = _latest(date(2021, 12, 31))
    new = _capability_with_added(previous.capability, "FASTER_SCREENSHOT_CAPTURE")
    change = _change(previous, new, added="FASTER_SCREENSHOT_CAPTURE")
    valid, reason = validate_material_capability_change(previous, new, change)
    assert valid is False
    assert reason == "ADDED_CAPABILITY_IRRELEVANT_TO_BLOCKER"


def test_declared_changed_dimensions_must_equal_real_semantic_difference():
    previous = _latest(date(2021, 12, 31))
    added = "ALTERNATE_BROKER_NATIVE_RECORD_ROUTE"
    new = _capability_with_added(previous.capability, added)
    change = _change(
        previous,
        new,
        added=added,
        changed_dimensions=frozenset({"route_contract"}),
    )
    valid, reason = validate_material_capability_change(previous, new, change)
    assert valid is False
    assert reason == "DECLARED_CHANGED_DIMENSIONS_MISMATCH"


def test_wrong_old_or_new_fingerprint_cannot_authorize_retry():
    previous = _latest(date(2021, 12, 31))
    added = "ALTERNATE_BROKER_NATIVE_RECORD_ROUTE"
    new = _capability_with_added(previous.capability, added)

    wrong_old = _change(
        previous,
        new,
        added=added,
        from_fingerprint="0" * 64,
    )
    valid, reason = validate_material_capability_change(previous, new, wrong_old)
    assert valid is False
    assert reason == "CAPABILITY_CHANGE_FINGERPRINT_MISMATCH"

    wrong_new = _change(
        previous,
        new,
        added=added,
        to_fingerprint="f" * 64,
    )
    valid, reason = validate_material_capability_change(previous, new, wrong_new)
    assert valid is False
    assert reason == "CAPABILITY_CHANGE_FINGERPRINT_MISMATCH"


def test_relevant_new_route_capability_can_deterministically_reenable_no_record_date():
    previous = _latest(date(2021, 12, 31))
    added = "ALTERNATE_BROKER_NATIVE_RECORD_ROUTE"
    new = _capability_with_added(previous.capability, added)
    change = _change(previous, new, added=added)
    valid, reason = validate_material_capability_change(previous, new, change)
    assert valid is True
    assert reason == "MATERIAL_CAPABILITY_CHANGE_PROVEN"

    decision = eligibility_for_unresolved_candidate(
        previous.target_date,
        previous.candidate_reason,
        [previous],
        new,
        [change],
    )
    assert decision.eligible is True
    assert decision.reason == "MATERIAL_CAPABILITY_CHANGE_RETRY"


def test_cross_date_blocker_requires_cross_date_or_exact_target_recovery_capability():
    previous = _latest(date(2021, 12, 24))

    irrelevant = "ALTERNATE_BROKER_NATIVE_RECORD_ROUTE"
    wrong_new = _capability_with_added(previous.capability, irrelevant)
    wrong_change = _change(previous, wrong_new, added=irrelevant)
    valid, reason = validate_material_capability_change(previous, wrong_new, wrong_change)
    assert valid is False
    assert reason == "ADDED_CAPABILITY_IRRELEVANT_TO_BLOCKER"

    relevant = "QUALIFIED_CROSS_DATE_INTERVAL_ATTRIBUTION"
    right_new = _capability_with_added(previous.capability, relevant)
    right_change = _change(previous, right_new, added=relevant)
    valid, reason = validate_material_capability_change(previous, right_new, right_change)
    assert valid is True
    assert reason == "MATERIAL_CAPABILITY_CHANGE_PROVEN"


def test_material_change_must_explicitly_name_the_prior_blocking_reason():
    previous = _latest(date(2021, 12, 31))
    added = "ALTERNATE_BROKER_NATIVE_RECORD_ROUTE"
    new = _capability_with_added(previous.capability, added)
    change = _change(
        previous,
        new,
        added=added,
        addresses="EXPECTED_DOM_CROSSCHECK_MISSING",
    )
    valid, reason = validate_material_capability_change(previous, new, change)
    assert valid is False
    assert reason == "BLOCKING_REASON_NOT_EXPLICITLY_ADDRESSED"


def test_pass_still_unresolved_is_a_fail_closed_contradiction():
    base = current_capability()
    synthetic = AttemptRecord(
        attempt_sequence=999,
        attempt_id="synthetic:pass-unresolved",
        batch_contract="SYNTHETIC_TEST_ONLY",
        target_date=date(2022, 5, 30),
        candidate_reason="MEMORIAL_DAY",
        outcome="PASS",
        adjudication_reason="SYNTHETIC_PASS",
        blocking_reason=None,
        capability_id="TRADING_BREAKS_PRIMARY_WIDGET_V1",
        capability=base,
        provenance={
            "workflow_run": 1,
            "job_id": 1,
            "artifact_id": 1,
            "artifact_sha256": "a" * 64,
            "probe_commit": "b" * 40,
        },
    )
    decision = eligibility_for_unresolved_candidate(
        synthetic.target_date,
        synthetic.candidate_reason,
        [synthetic],
        base,
    )
    assert decision.eligible is False
    assert decision.contract_verdict == "FAIL"
    assert decision.reason == "PASS_ATTEMPT_STILL_PRESENT_IN_UNRESOLVED_QUEUE"


def test_fail_attempt_is_not_silently_retried_by_progression_contract():
    base = current_capability()
    synthetic = AttemptRecord(
        attempt_sequence=999,
        attempt_id="synthetic:fail",
        batch_contract="SYNTHETIC_TEST_ONLY",
        target_date=date(2022, 5, 30),
        candidate_reason="MEMORIAL_DAY",
        outcome="FAIL",
        adjudication_reason="SYNTHETIC_INVARIANT_FAILURE",
        blocking_reason=None,
        capability_id="TRADING_BREAKS_PRIMARY_WIDGET_V1",
        capability=base,
        provenance={
            "workflow_run": 1,
            "job_id": 1,
            "artifact_id": 1,
            "artifact_sha256": "a" * 64,
            "probe_commit": "b" * 40,
        },
    )
    decision = eligibility_for_unresolved_candidate(
        synthetic.target_date,
        synthetic.candidate_reason,
        [synthetic],
        base,
    )
    assert decision.eligible is False
    assert decision.reason == "PREVIOUS_ATTEMPT_FAIL_REQUIRES_SEPARATE_REMEDIATION"
