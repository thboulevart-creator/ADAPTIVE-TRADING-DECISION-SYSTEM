from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Sequence

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE
from tools.trading_breaks_recovery_progression import (
    current_capability,
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


REPO = Path(__file__).resolve().parents[1]
FROZEN_MODULE = REPO / "tools" / "trading_breaks_recovery_batch10.py"
POLICY_DOC = REPO / "04-REFERENCE" / "HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH10-POLICY.md"
BATCH_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch10.py"

BATCH_NUMBER = 10
BATCH_SIZE = 5
BATCH_CONTRACT = "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH10_POLICY_V1"
PARENT_PROGRESSION_CONTRACT = "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
SELECTION_RULE = "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
FREEZE_BASELINE_HEAD = "7264970e0be56f3eb379f6647f8c353885f6e521"
SOURCE_BATCH09_INTEGRATION_COMMIT = "126ff25129728dc9f5c26cfeff701c1e04270843"
SOURCE_BATCH09_PERSISTED_HEAD_REBREAK_TRIGGER = "21965fd00fc92f606665b5db3c20c265b8ad83fe"
CURRENT_CAPABILITY_ID = "TRADING_BREAKS_PRIMARY_WIDGET_V1"
CURRENT_CAPABILITY_FINGERPRINT = "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"
EXPECTED_RECOVERY_QUEUE_COUNT = 34
EXPECTED_ELIGIBLE_QUEUE_COUNT = 23
EXPECTED_ATTEMPT_COUNT = 45
EXPECTED_BLOCKED_INELIGIBLE_COUNT = 11


def validate_freeze_candidate(
    candidate: Sequence[tuple[date, str]],
    governed_eligible: Sequence[tuple[date, str]],
) -> dict[str, str]:
    """Fail closed unless candidate is exactly the fixed-size governed eligible prefix."""
    eligible = list(governed_eligible)
    frozen = list(candidate)
    if len(eligible) < BATCH_SIZE:
        return {"verdict": "BLOCKED", "reason": "INSUFFICIENT_ELIGIBLE_CANDIDATES"}
    if len(frozen) != BATCH_SIZE:
        return {"verdict": "FAIL", "reason": "BATCH_CARDINALITY_CHANGED"}
    if any(
        not isinstance(item, tuple)
        or len(item) != 2
        or not isinstance(item[0], date)
        or not isinstance(item[1], str)
        or not item[1].strip()
        for item in frozen
    ):
        return {"verdict": "FAIL", "reason": "BATCH_MEMBER_MALFORMED"}

    days = [day for day, _ in frozen]
    if len(days) != len(set(days)):
        return {"verdict": "FAIL", "reason": "BATCH_DUPLICATE_DATE"}
    if days != sorted(days):
        return {"verdict": "FAIL", "reason": "BATCH_NOT_CHRONOLOGICAL"}

    expected = eligible[:BATCH_SIZE]
    if frozen == expected:
        return {"verdict": "PASS", "reason": "EXACT_GOVERNED_ELIGIBLE_PREFIX"}
    if set(frozen) == set(expected):
        return {"verdict": "FAIL", "reason": "BATCH_MEMBERSHIP_REORDERED"}
    if expected[0] not in frozen:
        return {"verdict": "FAIL", "reason": "FIRST_ELIGIBLE_MEMBER_SKIPPED"}
    if any(item not in expected for item in frozen):
        return {"verdict": "FAIL", "reason": "NON_PREFIX_MEMBER_SUBSTITUTED"}
    return {"verdict": "FAIL", "reason": "BATCH_PREFIX_MISMATCH"}


def derive_batch10_membership() -> tuple[tuple[date, str], ...]:
    raw = recovery_queue()
    eligible = eligible_recovery_queue()
    decisions = progression_decisions()
    _, current_capability_id, attempts = load_attempt_ledger()
    changes = load_material_capability_changes()

    if len(raw) != EXPECTED_RECOVERY_QUEUE_COUNT:
        raise RuntimeError(f"PRE_BATCH10_RECOVERY_QUEUE_COUNT_MISMATCH:{len(raw)}")
    if len(eligible) != EXPECTED_ELIGIBLE_QUEUE_COUNT:
        raise RuntimeError(f"PRE_BATCH10_ELIGIBLE_QUEUE_COUNT_MISMATCH:{len(eligible)}")
    if len(attempts) != EXPECTED_ATTEMPT_COUNT:
        raise RuntimeError(f"PRE_BATCH10_ATTEMPT_COUNT_MISMATCH:{len(attempts)}")
    if changes:
        raise RuntimeError("PRE_BATCH10_MATERIAL_CAPABILITY_CHANGE_REGISTRY_NOT_EMPTY")
    if current_capability_id != CURRENT_CAPABILITY_ID:
        raise RuntimeError("PRE_BATCH10_CURRENT_CAPABILITY_ID_MISMATCH")
    if current_capability().fingerprint() != CURRENT_CAPABILITY_FINGERPRINT:
        raise RuntimeError("PRE_BATCH10_CURRENT_CAPABILITY_FINGERPRINT_MISMATCH")

    blocked_ineligible = [
        item for item in decisions
        if item.latest_attempt_outcome == "BLOCKED" and not item.eligible
    ]
    if len(blocked_ineligible) != EXPECTED_BLOCKED_INELIGIBLE_COUNT:
        raise RuntimeError(
            f"PRE_BATCH10_BLOCKED_INELIGIBLE_COUNT_MISMATCH:{len(blocked_ineligible)}"
        )
    if eligible != sorted(eligible, key=lambda item: item[0]):
        raise RuntimeError("PRE_BATCH10_ELIGIBLE_QUEUE_NOT_CHRONOLOGICAL")

    frozen = tuple(eligible[:BATCH_SIZE])
    verdict = validate_freeze_candidate(frozen, eligible)
    if verdict != {"verdict": "PASS", "reason": "EXACT_GOVERNED_ELIGIBLE_PREFIX"}:
        raise RuntimeError(f"BATCH10_FREEZE_CANDIDATE_REJECTED:{verdict}")

    decisions_by_day = {item.target_date: item for item in decisions}
    attempted_days = {item.target_date for item in attempts}
    raw_days = {day for day, _ in raw}
    eligible_days = {day for day, _ in eligible}
    resolved_days = set(SPECIAL_SESSION_EVIDENCE) | set(NO_SPECIAL_CHANGE_EVIDENCE)
    frozen_days = {day for day, _ in frozen}

    if not frozen_days <= raw_days or not frozen_days <= eligible_days:
        raise RuntimeError("BATCH10_FROZEN_MEMBER_NOT_UNRESOLVED_AND_ELIGIBLE")
    if frozen_days & attempted_days:
        raise RuntimeError("BATCH10_PRIOR_ATTEMPT_CONTAMINATION")
    if frozen_days & resolved_days:
        raise RuntimeError("BATCH10_RESOLVED_MEMBER_CONTAMINATION")

    for day, reason in frozen:
        decision = decisions_by_day[day]
        if decision.candidate_reason != reason:
            raise RuntimeError(f"BATCH10_REASON_MISMATCH:{day.isoformat()}")
        if not decision.eligible or decision.reason != "INITIAL_ATTEMPT":
            raise RuntimeError(f"BATCH10_MEMBER_NOT_INITIAL_ATTEMPT:{day.isoformat()}")
        if decision.latest_attempt_id is not None or decision.latest_attempt_outcome is not None:
            raise RuntimeError(f"BATCH10_MEMBER_HAS_PRIOR_ATTEMPT:{day.isoformat()}")
        if decision.contract_verdict != "PASS":
            raise RuntimeError(f"BATCH10_MEMBER_PROGRESSION_CONTRACT_NOT_PASS:{day.isoformat()}")
    return frozen


def render_frozen_module(targets: Sequence[tuple[date, str]]) -> str:
    members = "\n".join(
        f'    (date({day.year}, {day.month}, {day.day}), "{reason}"),'
        for day, reason in targets
    )
    return f'''from __future__ import annotations

from datetime import date

BATCH_CONTRACT = "{BATCH_CONTRACT}"
PARENT_PROGRESSION_CONTRACT = "{PARENT_PROGRESSION_CONTRACT}"
BATCH_SIZE = {BATCH_SIZE}
SELECTION_RULE = "{SELECTION_RULE}"
FREEZE_BASELINE_HEAD = "{FREEZE_BASELINE_HEAD}"
SOURCE_BATCH09_INTEGRATION_COMMIT = "{SOURCE_BATCH09_INTEGRATION_COMMIT}"
SOURCE_BATCH09_PERSISTED_HEAD_REBREAK_TRIGGER = "{SOURCE_BATCH09_PERSISTED_HEAD_REBREAK_TRIGGER}"
CURRENT_CAPABILITY_ID = "{CURRENT_CAPABILITY_ID}"
CURRENT_CAPABILITY_FINGERPRINT = "{CURRENT_CAPABILITY_FINGERPRINT}"

FROZEN_BATCH10_TARGETS: tuple[tuple[date, str], ...] = (
{members}
)


def batch10_targets() -> list[tuple[date, str]]:
    """Return immutable Batch 10 membership frozen before any observation."""
    return list(FROZEN_BATCH10_TARGETS)
'''


def render_policy(targets: Sequence[tuple[date, str]]) -> str:
    members = "\n".join(
        f"{index}. `{day.isoformat()} — {reason}`"
        for index, (day, reason) in enumerate(targets, start=1)
    )
    return f'''# HISTORICAL TRADING BREAKS RECOVERY — BATCH 10 POLICY

Contract: `{BATCH_CONTRACT}`

Parent progression contract: `{PARENT_PROGRESSION_CONTRACT}`

## Freeze status

**FROZEN — mechanically derived from persisted post-Batch09 `eligible_recovery_queue()[:5]`; no Batch 10 observation preceded this freeze.**

## Freeze provenance

- pre-freeze checkpoint HEAD: `{FREEZE_BASELINE_HEAD}`
- Batch 09 atomic integration commit: `{SOURCE_BATCH09_INTEGRATION_COMMIT}`
- Batch 09 persisted-HEAD re-break trigger: `{SOURCE_BATCH09_PERSISTED_HEAD_REBREAK_TRIGGER}`
- capability: `{CURRENT_CAPABILITY_ID}`
- fingerprint: `{CURRENT_CAPABILITY_FINGERPRINT}`
- raw unresolved: `{EXPECTED_RECOVERY_QUEUE_COUNT}`
- eligible unresolved: `{EXPECTED_ELIGIBLE_QUEUE_COUNT}`
- historical attempts: `{EXPECTED_ATTEMPT_COUNT}`
- same-capability BLOCKED/ineligible: `{EXPECTED_BLOCKED_INELIGIBLE_COUNT}`
- material capability changes: `0`

## Fixed selection rule

`BATCH_SIZE = {BATCH_SIZE}`

`eligible_recovery_queue()[:5]`

`{SELECTION_RULE}`

Batch size and membership may not depend on expected outcome, holiday type, source availability, apparent difficulty, convenience, manual priority or browser observations.

## Frozen Batch 10 membership

{members}

These identities and this order were emitted mechanically by the freeze generator from the governed eligible queue. No member was manually selected.

## Required qualification

The membership contract rejects skip, reorder, later-member substitution, cardinality change, duplication, raw-queue bypass, same-capability BLOCKED reinsertion, already-resolved reinsertion, prior-attempt contamination, manual selection and expected-outcome dependence.

The frozen module has no browser/probe/network path and no live call to either recovery queue.

No `.bi5`. No real backtest.
'''


def render_batch_test() -> str:
    return '''from __future__ import annotations

import inspect

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE
from tools.freeze_trading_breaks_recovery_batch10 import BATCH_SIZE, validate_freeze_candidate
import tools.trading_breaks_recovery_batch10 as batch10_module
from tools.trading_breaks_recovery_batch10 import batch10_targets
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue


def test_batch10_snapshot_equals_exact_governed_eligible_prefix():
    eligible = eligible_recovery_queue()
    assert batch10_targets() == eligible[:BATCH_SIZE]
    assert validate_freeze_candidate(batch10_targets(), eligible) == {
        "verdict": "PASS",
        "reason": "EXACT_GOVERNED_ELIGIBLE_PREFIX",
    }


def test_batch10_members_are_unresolved_initial_attempts_without_history():
    frozen = batch10_targets()
    decisions = {item.target_date: item for item in progression_decisions()}
    _, _, attempts = load_attempt_ledger()
    attempted_days = {item.target_date for item in attempts}
    assert set(frozen) <= set(recovery_queue())
    assert {day for day, _ in frozen}.isdisjoint(attempted_days)
    for day, reason in frozen:
        decision = decisions[day]
        assert decision.candidate_reason == reason
        assert decision.eligible is True
        assert decision.reason == "INITIAL_ATTEMPT"
        assert decision.latest_attempt_id is None
        assert decision.latest_attempt_outcome is None
        assert decision.contract_verdict == "PASS"


def test_batch10_blocked_and_resolved_dates_are_excluded():
    frozen_days = {day for day, _ in batch10_targets()}
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    resolved_days = set(SPECIAL_SESSION_EVIDENCE) | set(NO_SPECIAL_CHANGE_EVIDENCE)
    assert frozen_days.isdisjoint(raw_days - eligible_days)
    assert frozen_days.isdisjoint(resolved_days)


def test_batch10_accessor_is_immutable_to_caller():
    original = batch10_targets()
    altered = batch10_targets()
    altered.pop()
    assert batch10_targets() == original


def test_batch10_frozen_module_has_no_live_queue_surface():
    source = inspect.getsource(batch10_module).lower()
    assert "eligible_recovery_queue(" not in source
    assert "recovery_queue(" not in source
    assert "probe_candidate" not in source
'''


def write_freeze_artifacts(targets: Sequence[tuple[date, str]]) -> None:
    for path in (FROZEN_MODULE, POLICY_DOC, BATCH_TEST):
        if path.exists():
            raise RuntimeError(f"BATCH10_FREEZE_ARTIFACT_ALREADY_EXISTS:{path.relative_to(REPO)}")
    FROZEN_MODULE.write_text(render_frozen_module(targets), encoding="utf-8")
    POLICY_DOC.write_text(render_policy(targets), encoding="utf-8")
    BATCH_TEST.write_text(render_batch_test(), encoding="utf-8")


def main() -> int:
    targets = derive_batch10_membership()
    write_freeze_artifacts(targets)
    print("BATCH10_FROZEN_MEMBERSHIP")
    for index, (day, reason) in enumerate(targets, start=1):
        print(f"{index}: {day.isoformat()} — {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
