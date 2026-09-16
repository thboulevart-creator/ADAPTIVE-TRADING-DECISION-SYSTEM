from datetime import date

from tools.freeze_trading_breaks_recovery_batch15 import NOMINAL_BATCH_SIZE, derive
from tools.trading_breaks_recovery_batch15 import (
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    EVIDENCE_MODE,
    FREEZE_BASELINE_HEAD,
    FROZEN_BATCH15_TARGETS,
    batch15_targets,
)
from tools.trading_breaks_recovery_progression import eligible_recovery_queue


def test_batch15_is_exact_first_five_v2_eligible_retries_and_returns_copy():
    a = batch15_targets()
    b = batch15_targets()
    eligible = eligible_recovery_queue()

    assert NOMINAL_BATCH_SIZE == BATCH_SIZE == 5
    assert len(eligible) == 14
    assert a == list(derive()) == eligible[:5] == list(FROZEN_BATCH15_TARGETS)
    assert a == [
        (date(2021, 12, 24), 'CHRISTMAS_OBSERVED'),
        (date(2022, 4, 15), 'GOOD_FRIDAY'),
        (date(2022, 12, 26), 'CHRISTMAS_OBSERVED'),
        (date(2023, 1, 2), 'NEW_YEARS_OBSERVED'),
        (date(2023, 7, 4), 'INDEPENDENCE_DAY_OBSERVED'),
    ]
    assert FREEZE_BASELINE_HEAD == 'd6622e8da58e2d4218947ff3f2953fe8e19a2c96'
    assert CURRENT_CAPABILITY_ID == 'TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2'
    assert CURRENT_CAPABILITY_FINGERPRINT == 'e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31'
    assert EVIDENCE_MODE == 'PERSISTED_CLASS_A_OFFLINE_READJUDICATION_ONLY'

    a.pop()
    assert len(b) == 5
    assert len(batch15_targets()) == 5


def test_batch15_selection_attacks_do_not_equal_frozen_membership():
    frozen = batch15_targets()
    eligible = eligible_recovery_queue()
    attacks = [
        frozen[:-1],
        [*frozen, eligible[5]],
        list(reversed(frozen)),
        [frozen[1], frozen[0], *frozen[2:]],
        [frozen[0], frozen[0], *frozen[2:]],
        eligible[1:6],
        [eligible[5], *frozen[1:]],
    ]
    assert all(attack != frozen for attack in attacks)
