from tools.trading_breaks_recovery_batch11 import batch11_targets


def test_batch11_frozen_membership_is_immutable_copy():
    first = batch11_targets()
    second = batch11_targets()
    assert len(first) == 5
    first.pop()
    assert len(second) == 5
    assert len(batch11_targets()) == 5
