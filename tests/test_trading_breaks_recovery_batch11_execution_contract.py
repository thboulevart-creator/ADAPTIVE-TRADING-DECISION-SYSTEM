from pathlib import Path


def test_batch11_execution_uses_frozen_membership_only():
    source = Path('tools/trading_breaks_recovery_batch11_execute.py').read_text(encoding='utf-8')
    assert 'batch11_targets()' in source
    assert 'probe_candidate' in source
    assert 'eligible_recovery_queue' not in source
    assert 'recovery_queue' not in source
    assert 'progression_decisions' not in source
