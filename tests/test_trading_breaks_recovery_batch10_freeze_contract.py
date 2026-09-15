from __future__ import annotations

from datetime import date

import tools.freeze_trading_breaks_recovery_batch10 as freeze

HISTORICAL_FROZEN = [
    (date(2024, 12, 31), "NEW_YEARS_EVE_CANDIDATE"),
    (date(2025, 1, 1), "NEW_YEARS_OBSERVED"),
    (date(2025, 1, 20), "MARTIN_LUTHER_KING_DAY"),
    (date(2025, 2, 17), "PRESIDENTS_DAY"),
    (date(2025, 4, 18), "GOOD_FRIDAY"),
]
HISTORICAL_ELIGIBLE_PREFIX_PLUS_NEXT = HISTORICAL_FROZEN + [
    (date(2025, 5, 26), "MEMORIAL_DAY"),
]


def test_batch10_freeze_historical_identity_preserved_without_live_rederivation():
    assert freeze.BATCH_SIZE == 5
    assert freeze.validate_freeze_candidate(HISTORICAL_FROZEN, HISTORICAL_ELIGIBLE_PREFIX_PLUS_NEXT) == {
        "verdict": "PASS", "reason": "EXACT_GOVERNED_ELIGIBLE_PREFIX"
    }


def test_batch10_historical_attacks_remain_rejected():
    eligible = HISTORICAL_ELIGIBLE_PREFIX_PLUS_NEXT
    reordered = [HISTORICAL_FROZEN[1], HISTORICAL_FROZEN[0], *HISTORICAL_FROZEN[2:]]
    assert freeze.validate_freeze_candidate(reordered, eligible)["verdict"] == "FAIL"
    assert freeze.validate_freeze_candidate(eligible[1:6], eligible)["reason"] == "FIRST_ELIGIBLE_MEMBER_SKIPPED"
    assert freeze.validate_freeze_candidate([*HISTORICAL_FROZEN[:-1], eligible[5]], eligible)["reason"] == "NON_PREFIX_MEMBER_SUBSTITUTED"
    assert freeze.validate_freeze_candidate(HISTORICAL_FROZEN[:-1], eligible)["reason"] == "BATCH_CARDINALITY_CHANGED"
    duplicate = [HISTORICAL_FROZEN[0], HISTORICAL_FROZEN[0], *HISTORICAL_FROZEN[2:]]
    assert freeze.validate_freeze_candidate(duplicate, eligible)["reason"] == "BATCH_DUPLICATE_DATE"
