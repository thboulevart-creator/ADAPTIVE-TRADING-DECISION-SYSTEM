from __future__ import annotations

import json
from pathlib import Path

from tools.trading_breaks_recovery_batch11 import BATCH_CONTRACT, CURRENT_CAPABILITY_ID, batch11_targets

REPO=Path(__file__).resolve().parents[1]
CALENDAR=REPO/'tools/dukascopy_usatech_calendar.py'
LEDGER=REPO/'reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json'
ADJUDICATION=REPO/'reports/data-qualification/historical_trading_breaks_recovery_batch11_adjudication.json'
RUN_ID=35009400933
JOB_ID=104517277101
PROBE_COMMIT='7b5bbef03db35bf954c9a96364dba84d11b2fc94'
ARTIFACT_ID=10412379849
ARTIFACT_SHA256='f5bf2a2ee5cc7e2cb535266cd918cabfeedd1eb04ad59d518912b02c31276ef2'

PASS_RECORDS={
 '2025-05-26':{'reason_token':'SPECIAL_MEMORIAL_DAY_2025','record_id':'81578','broker_reason':'Memorial Day','request_epoch_ms':1748217600000,'start_utc':'2025-05-26T16:59:59Z','final_closed_minute_utc':'2025-05-26T21:59:59Z','reopen_utc':'2025-05-26T22:00:59Z','closed_hours':(17,18,19,20,21)},
 '2025-06-19':{'reason_token':'SPECIAL_JUNETEENTH_OBSERVED_2025','record_id':'82497','broker_reason':'Juneteenth Holiday','request_epoch_ms':1750291200000,'start_utc':'2025-06-19T16:59:59Z','final_closed_minute_utc':'2025-06-19T21:59:59Z','reopen_utc':'2025-06-19T22:00:59Z','closed_hours':(17,18,19,20,21)},
 '2025-07-03':{'reason_token':'SPECIAL_INDEPENDENCE_PRE_HOLIDAY_SESSION_2025','record_id':'83303','broker_reason':'Independence Day in the United States','request_epoch_ms':1751500800000,'start_utc':'2025-07-03T16:59:59Z','final_closed_minute_utc':'2025-07-03T21:59:59Z','reopen_utc':'2025-07-03T22:00:59Z','closed_hours':(17,18,19,20,21)},
 '2025-07-04':{'reason_token':'SPECIAL_INDEPENDENCE_DAY_OBSERVED_2025','record_id':'83304','broker_reason':'Independence Day in the United States','request_epoch_ms':1751587200000,'start_utc':'2025-07-04T16:59:59Z','final_closed_minute_utc':'2025-07-06T21:59:59Z','reopen_utc':'2025-07-06T22:00:59Z','closed_hours':(17,18,19,20,21,22,23)},
 '2025-09-01':{'reason_token':'SPECIAL_LABOR_DAY_2025','record_id':'84407','broker_reason':'Labor Day','request_epoch_ms':1756684800000,'start_utc':'2025-09-01T16:59:59Z','final_closed_minute_utc':'2025-09-01T21:59:59Z','reopen_utc':'2025-09-01T22:00:59Z','closed_hours':(17,18,19,20,21)},
}


def replace_once(text,old,new,label):
    count=text.count(old)
    if count!=1: raise RuntimeError(f'{label}: expected exactly one match, found {count}')
    return text.replace(old,new,1)


def load_adjudication():
    report=json.loads(ADJUDICATION.read_text(encoding='utf-8'))
    if report.get('schema')!='HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH11_ADJUDICATION_V1' or report.get('verdict')!='PASS': raise RuntimeError('BATCH11_ADJUDICATION_NOT_AUTHORITATIVE_PASS')
    if (report.get('attempted'),report.get('pass'),report.get('blocked'),report.get('fail'))!=(5,5,0,0): raise RuntimeError('BATCH11_ADJUDICATION_ACCOUNTING_MISMATCH')
    p=report.get('provenance') or {}
    expected={'workflow_run':RUN_ID,'job_id':JOB_ID,'probe_commit':PROBE_COMMIT,'artifact_id':ARTIFACT_ID,'artifact_sha256':ARTIFACT_SHA256}
    for k,v in expected.items():
        if p.get(k)!=v: raise RuntimeError(f'BATCH11_PROVENANCE_MISMATCH:{k}')
    observed=[(x.get('target_date'),x.get('candidate_reason'),x.get('verdict')) for x in report.get('adjudications',[])]
    expected_obs=[(d.isoformat(),r,'PASS') for d,r in batch11_targets()]
    if observed!=expected_obs: raise RuntimeError('BATCH11_FROZEN_ADJUDICATION_IDENTITY_MISMATCH')
    by_day={x['target_date']:x for x in report['adjudications']}
    for day,rec in PASS_RECORDS.items():
        item=by_day[day]
        checks={'reason':'EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED','broker_record_id':rec['record_id'],'broker_reason':rec['broker_reason'],'break_start_utc':rec['start_utc'],'final_closed_minute_utc':rec['final_closed_minute_utc'],'reopen_utc':rec['reopen_utc'],'fully_closed_hours_utc':list(rec['closed_hours']),'dom_witness_present':True}
        for k,v in checks.items():
            if item.get(k)!=v: raise RuntimeError(f'BATCH11_PASS_RECORD_MISMATCH:{day}:{k}')
    return report


def guard_preintegration_state():
    text=CALENDAR.read_text(encoding='utf-8')
    for token in [x['reason_token'] for x in PASS_RECORDS.values()]:
        if token in text: raise RuntimeError('BATCH11_ALREADY_OR_PARTIALLY_INTEGRATED')
    ledger=json.loads(LEDGER.read_text(encoding='utf-8')); attempts=ledger.get('attempts')
    if not isinstance(attempts,list) or len(attempts)!=50: raise RuntimeError('PRE_BATCH11_ATTEMPT_COUNT_MISMATCH')
    if any(str(x.get('attempt_id','')).startswith('batch11:') for x in attempts): raise RuntimeError('BATCH11_ATTEMPTS_ALREADY_PRESENT')


def render_entry(day,rec):
    y,m,d=map(int,day.split('-')); hours=rec['closed_hours']
    if hours!=tuple(range(hours[0],hours[-1]+1)): raise RuntimeError(f'NONCONTIGUOUS_HOURS:{day}')
    return f'''    date({y}, {m}, {d}): {{
        "reason": "{rec['reason_token']}",
        "fully_closed_hours_utc": frozenset(range({hours[0]}, {hours[-1]+1})),
        "broker_record_id": "{rec['record_id']}",
        "broker_reason": "{rec['broker_reason']}",
        "artifact_id": {ARTIFACT_ID},
        "artifact_sha256": "{ARTIFACT_SHA256}",
        "probe_commit": "{PROBE_COMMIT}",
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date={rec['request_epoch_ms']}"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/{RUN_ID}"
        ),
        "qualification_report_source": (
            "reports/data-qualification/historical_trading_breaks_recovery_batch11_qualification.md"
        ),
    }},
'''


def integrate_calendar():
    text=CALENDAR.read_text(encoding='utf-8')
    block=''.join(render_entry(day,PASS_RECORDS[day]) for day in PASS_RECORDS)
    marker='}\n\nCALENDAR_CONTRACT = "DUKASCOPY_USATECH_SESSION_CALENDAR_V3"'
    text=replace_once(text,marker,block+marker,'Batch11 calendar insertion')
    CALENDAR.write_text(text,encoding='utf-8')


def integrate_ledger(report):
    ledger=json.loads(LEDGER.read_text(encoding='utf-8')); attempts=ledger['attempts']
    provenance={'workflow_run':RUN_ID,'job_id':JOB_ID,'artifact_id':ARTIFACT_ID,'artifact_sha256':ARTIFACT_SHA256,'probe_commit':PROBE_COMMIT}
    for seq,((day,reason),adj) in enumerate(zip(batch11_targets(),report['adjudications'],strict=True),start=51):
        if adj['verdict']!='PASS': raise RuntimeError(f'BATCH11_UNINTEGRABLE_OUTCOME:{day}:{adj["verdict"]}')
        attempts.append({'attempt_sequence':seq,'attempt_id':f'batch11:{day.isoformat()}','batch_contract':BATCH_CONTRACT,'target_date':day.isoformat(),'candidate_reason':reason,'outcome':'PASS','adjudication_reason':adj['reason'],'blocking_reason':None,'capability_id':CURRENT_CAPABILITY_ID,'provenance':dict(provenance)})
    if len(attempts)!=55: raise RuntimeError('BATCH11_POST_LEDGER_COUNT_MISMATCH')
    LEDGER.write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')


def rewrite_current_state_tests():
    replacements={
      'assert len(attempts) == 50':'assert len(attempts) == 55',
      'list(range(1, 51))':'list(range(1, 56))',
      'len({item.attempt_id for item in attempts}) == 50':'len({item.attempt_id for item in attempts}) == 55',
      'assert len(queue) == 31':'assert len(queue) == 26',
      'assert len(decisions) == len(queue) == 31':'assert len(decisions) == len(queue) == 26',
      'assert len(recovery_queue()) == len(decisions) == 31':'assert len(recovery_queue()) == len(decisions) == 26',
      'assert len(eligible) == 18':'assert len(eligible) == 13',
      '(111, 60, 51)':'(111, 65, 46)',
      '(68, 37, 31)':'(68, 42, 26)',
      'global_report["resolved_candidate_dates"] == 60':'global_report["resolved_candidate_dates"] == 65',
      'global_report["unresolved_candidate_dates"] == 51':'global_report["unresolved_candidate_dates"] == 46',
      'window_report["resolved_candidate_dates"] == 37':'window_report["resolved_candidate_dates"] == 42',
      'window_report["unresolved_candidate_dates"] == 31':'window_report["unresolved_candidate_dates"] == 26',
      'eligible[0] == (date(2025, 5, 26), "MEMORIAL_DAY")':'eligible[0] == (date(2025, 11, 27), "THANKSGIVING_DAY")',
      'post_batch10_state':'post_batch11_state',
      'post_batch10_progression_state':'post_batch11_progression_state',
    }
    for path in sorted((REPO/'tests').glob('test_*.py')):
        if path.name.endswith('_integration_contract.py') or path.name in {'test_trading_breaks_recovery_batch11_adjudication.py','test_trading_breaks_recovery_batch11_execution_contract.py'}: continue
        text=path.read_text(encoding='utf-8'); original=text
        for old,new in replacements.items(): text=text.replace(old,new)
        if text!=original: path.write_text(text,encoding='utf-8')


def main():
    report=load_adjudication(); guard_preintegration_state(); integrate_calendar(); integrate_ledger(report); rewrite_current_state_tests()
    print('PASS: prepared Batch 11 atomic worktree integration')
    print('calendar PASS dates:', ', '.join(PASS_RECORDS))
    print('ledger attempts: 51..55')
    return 0

if __name__=='__main__': raise SystemExit(main())
