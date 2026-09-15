from tools.freeze_trading_breaks_recovery_batch12 import derive
from tools.trading_breaks_recovery_batch12 import batch12_targets


def test_batch12_frozen_size_copy_and_mechanical_prefix():
    a = batch12_targets()
    b = batch12_targets()
    assert len(a) == 5
    assert a == list(derive())
    a.pop()
    assert len(b) == 5
    assert len(batch12_targets()) == 5
