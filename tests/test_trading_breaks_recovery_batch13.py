from tools.freeze_trading_breaks_recovery_batch13 import derive
from tools.trading_breaks_recovery_batch13 import batch13_targets


def test_batch13_frozen_size_copy_and_mechanical_prefix():
    a = batch13_targets()
    b = batch13_targets()
    assert len(a) == 5
    assert a == list(derive())
    a.pop()
    assert len(b) == 5
    assert len(batch13_targets()) == 5
