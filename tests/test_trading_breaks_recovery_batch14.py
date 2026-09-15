from datetime import date

from tools.freeze_trading_breaks_recovery_batch14 import (
    NOMINAL_BATCH_SIZE,
    TERMINAL_BATCH_SIZE,
    derive,
)
from tools.trading_breaks_recovery_batch14 import batch14_targets
from tools.trading_breaks_recovery_progression import eligible_recovery_queue


def test_batch14_is_complete_terminal_remainder_and_returns_copy():
    a = batch14_targets()
    b = batch14_targets()
    eligible = eligible_recovery_queue()
    assert NOMINAL_BATCH_SIZE == 5
    assert TERMINAL_BATCH_SIZE == 3
    assert 0 < len(eligible) < NOMINAL_BATCH_SIZE
    assert a == list(derive()) == eligible
    assert a == [
        (date(2026, 6, 19), 'JUNETEENTH_OBSERVED'),
        (date(2026, 7, 2), 'INDEPENDENCE_PRE_HOLIDAY_SESSION'),
        (date(2026, 7, 3), 'INDEPENDENCE_DAY_OBSERVED'),
    ]
    a.pop()
    assert len(b) == 3
    assert len(batch14_targets()) == 3
