from __future__ import annotations

from datetime import date
from pathlib import Path

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, load_material_capability_changes, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue

REPO = Path(__file__).resolve().parents[1]
BATCH_SIZE = 5


def derive():
    raw = recovery_queue(); eligible = eligible_recovery_queue(); decisions = progression_decisions(); _, _, attempts = load_attempt_ledger()
    assert len(raw) == 31 and len(eligible) == 18 and len(attempts) == 50
    assert sum((not d.eligible) and d.latest_attempt_outcome == 'BLOCKED' for d in decisions) == 13
    assert load_material_capability_changes() == []
    assert eligible == sorted(eligible, key=lambda x: x[0])
    frozen = tuple(eligible[:5])
    attempted = {x.target_date for x in attempts}; resolved = set(SPECIAL_SESSION_EVIDENCE) | set(NO_SPECIAL_CHANGE_EVIDENCE); by_day={x.target_date:x for x in decisions}
    assert len(frozen) == 5 and len({d for d,_ in frozen}) == 5
    for day, reason in frozen:
        d=by_day[day]; assert day not in attempted and day not in resolved; assert d.candidate_reason==reason and d.eligible and d.reason=='INITIAL_ATTEMPT'
    return frozen


def main():
    targets=derive(); module=REPO/'tools/trading_breaks_recovery_batch11.py'; policy=REPO/'04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH11-POLICY.md'; test=REPO/'tests/test_trading_breaks_recovery_batch11.py'
    for p in (module,policy,test):
        if p.exists(): raise RuntimeError(f'EXISTS:{p}')
    members='\n'.join(f'    (date({d.year},{d.month},{d.day}), {r!r}),' for d,r in targets)
    module.write_text(f"from datetime import date\n\nBATCH_CONTRACT='HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH11_POLICY_V1'\nBATCH_SIZE=5\nFREEZE_BASELINE_HEAD='4b274db8f7b4e2abb21e30e710577938795e8198'\nCURRENT_CAPABILITY_ID='TRADING_BREAKS_PRIMARY_WIDGET_V1'\nCURRENT_CAPABILITY_FINGERPRINT='82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f'\nFROZEN_BATCH11_TARGETS=(\n{members}\n)\n\ndef batch11_targets(): return list(FROZEN_BATCH11_TARGETS)\n",encoding='utf-8')
    listing='\n'.join(f'{i}. `{d.isoformat()} — {r}`' for i,(d,r) in enumerate(targets,1)); policy.write_text(f'# BATCH 11 POLICY\n\n**FROZEN mechanically from `eligible_recovery_queue()[:5]`.**\n\n{listing}\n\nNo observation preceded freeze.\n',encoding='utf-8')
    test.write_text("from tools.trading_breaks_recovery_batch11 import batch11_targets\n\ndef test_batch11_frozen_size_and_copy():\n a=batch11_targets(); b=batch11_targets(); assert len(a)==5; a.pop(); assert len(b)==5 and len(batch11_targets())==5\n",encoding='utf-8')
    print('BATCH11_FROZEN_MEMBERSHIP'); [print(f'{i}: {d.isoformat()} — {r}') for i,(d,r) in enumerate(targets,1)]

if __name__=='__main__': main()
