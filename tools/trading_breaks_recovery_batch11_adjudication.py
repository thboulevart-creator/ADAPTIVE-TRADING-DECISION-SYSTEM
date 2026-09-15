from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from tools.trading_breaks_recovery_batch11 import BATCH_CONTRACT, BATCH_SIZE, CURRENT_CAPABILITY_FINGERPRINT, CURRENT_CAPABILITY_ID, PARENT_PROGRESSION_CONTRACT, SELECTION_RULE, batch11_targets
from tools.trading_breaks_recovery_protocol import CONTRACT as RECOVERY_PROTOCOL, RecoveryEvidence, derive_fully_closed_hours_utc, derive_interval, validate_positive_recovery_against_frozen_batch

REPO=Path(__file__).resolve().parents[1]
RUNTIME_PATH=REPO/'reports/data-qualification/historical_trading_breaks_recovery_batch11_runtime.json'
ADJUDICATION_JSON=REPO/'reports/data-qualification/historical_trading_breaks_recovery_batch11_adjudication.json'
QUALIFICATION_MD=REPO/'reports/data-qualification/historical_trading_breaks_recovery_batch11_qualification.md'
EXPECTED_RUN=35009400933
EXPECTED_JOB=104517277101
EXPECTED_ARTIFACT=10412379849
EXPECTED_ARTIFACT_SHA256='f5bf2a2ee5cc7e2cb535266cd918cabfeedd1eb04ad59d518912b02c31276ef2'
EXPECTED_PROBE_COMMIT='7b5bbef03db35bf954c9a96364dba84d11b2fc94'
TARGET_NAME='USATECH.IDX/USD'
TARGET_ID='9016'
SCHEMA='HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH11_ADJUDICATION_V1'


def _epoch_ms(dt): return int(dt.timestamp()*1000)
def _iso_z(dt): return dt.isoformat().replace('+00:00','Z')


def _parse_dom(line):
    parts=[x.strip() for x in line.split('\t')]
    if len(parts)!=4 or parts[0]!=TARGET_NAME: raise ValueError('DOM_WITNESS_INVALID')
    start=datetime.strptime(parts[1],'%d-%b-%y %H:%M:%S').replace(tzinfo=timezone.utc)
    end=datetime.strptime(parts[2],'%d-%b-%y %H:%M:%S').replace(tzinfo=timezone.utc)
    return {'instrument':TARGET_ID,'start':_epoch_ms(start),'end':_epoch_ms(end),'reason':parts[3]}


def adjudicate_runtime(runtime):
    if runtime.get('schema')!=BATCH_CONTRACT: raise ValueError('RUNTIME_SCHEMA_MISMATCH')
    if runtime.get('parent_protocol')!=RECOVERY_PROTOCOL: raise ValueError('PARENT_PROTOCOL_MISMATCH')
    if runtime.get('parent_progression_contract')!=PARENT_PROGRESSION_CONTRACT: raise ValueError('PARENT_PROGRESSION_MISMATCH')
    if runtime.get('batch_number')!=11 or runtime.get('batch_size')!=BATCH_SIZE: raise ValueError('BATCH_IDENTITY_MISMATCH')
    if runtime.get('selection_rule')!=SELECTION_RULE: raise ValueError('SELECTION_RULE_MISMATCH')
    if runtime.get('capability_id')!=CURRENT_CAPABILITY_ID or runtime.get('capability_fingerprint')!=CURRENT_CAPABILITY_FINGERPRINT: raise ValueError('CAPABILITY_MISMATCH')
    expected_targets=[{'target_date':d.isoformat(),'candidate_reason':r} for d,r in batch11_targets()]
    if runtime.get('targets')!=expected_targets: raise ValueError('FROZEN_MEMBERSHIP_MISMATCH')
    if runtime.get('read_only') is not True or runtime.get('market_data_written') is not False: raise ValueError('READ_ONLY_BOUNDARY_MISMATCH')
    p=runtime.get('provenance') or {}
    expected_p={'workflow_run':EXPECTED_RUN,'job_id':EXPECTED_JOB,'probe_commit':EXPECTED_PROBE_COMMIT,'artifact_id':EXPECTED_ARTIFACT,'artifact_sha256':EXPECTED_ARTIFACT_SHA256}
    for k,v in expected_p.items():
        if p.get(k)!=v: raise ValueError(f'PROVENANCE_MISMATCH:{k}')
    results=runtime.get('results')
    if not isinstance(results,list) or len(results)!=BATCH_SIZE: raise ValueError('RESULT_COUNT_MISMATCH')
    adjudications=[]
    frozen=batch11_targets()
    for raw,(day,reason) in zip(results,frozen,strict=True):
        if raw.get('target_date')!=day.isoformat() or raw.get('requested_date')!=day.isoformat() or raw.get('candidate_reason')!=reason: raise ValueError('RESULT_IDENTITY_MISMATCH')
        if raw.get('instrument_name')!=TARGET_NAME or raw.get('instrument_id_expected')!=TARGET_ID or raw.get('instrument_id_observed')!=TARGET_ID: raise ValueError('INSTRUMENT_MISMATCH')
        if raw.get('date_honored') is not True or raw.get('raw_payload_present') is not True or raw.get('runtime_errors'): raise ValueError('CAPTURE_ENVELOPE_INVALID')
        if raw.get('capture_verdict')!='CAPTURED': raise ValueError('CAPTURE_NOT_POSITIVE')
        for key in ('official_page_status','current_control_status','target_nav_status'):
            if not (200 <= int(raw.get(key,0)) < 400): raise ValueError(f'HTTP_STATUS_INVALID:{key}')
        records=raw.get('matching_records'); dom_lines=raw.get('dom_witness_lines')
        if not isinstance(records,list) or len(records)!=1 or not isinstance(dom_lines,list) or len(dom_lines)!=1: raise ValueError('POSITIVE_EVIDENCE_CARDINALITY_INVALID')
        rec=records[0]; dom=_parse_dom(dom_lines[0])
        if str(rec.get('instrument'))!=TARGET_ID or str(rec.get('reason','')).strip()=='' or str(rec.get('id','')).strip()=='': raise ValueError('NETWORK_RECORD_INVALID')
        if int(rec['start'])!=int(dom['start']) or int(rec['end'])!=int(dom['end']) or str(rec['reason']).strip()!=str(dom['reason']).strip(): raise ValueError('DOM_NETWORK_CONTRADICTION')
        start,end,reopen=derive_interval(rec)
        if start.date()!=day: raise ValueError('CROSS_DATE_RECORD_NOT_ADMISSIBLE')
        hours=sorted(derive_fully_closed_hours_utc(day,start,reopen))
        if rec.get('start_utc')!=_iso_z(start) or rec.get('end_last_closed_minute_utc')!=_iso_z(end) or rec.get('derived_reopen_utc')!=_iso_z(reopen) or rec.get('fully_closed_hours_utc')!=hours: raise ValueError('DERIVED_INTERVAL_MISMATCH')
        evidence=RecoveryEvidence(target_date=day,candidate_reason=reason,requested_date=day,instrument_id=TARGET_ID,instrument_name=TARGET_NAME,network_record=rec,raw_payload_present=True,dom_available=True,dom_record=dom,workflow_run=EXPECTED_RUN,artifact_id=EXPECTED_ARTIFACT,artifact_sha256=EXPECTED_ARTIFACT_SHA256,probe_commit=EXPECTED_PROBE_COMMIT)
        verdict=validate_positive_recovery_against_frozen_batch(evidence,frozen)
        verdict['broker_record_id']=str(rec['id']); verdict['broker_reason']=rec['reason']; verdict['dom_witness_present']=True
        adjudications.append(verdict)
    fail=sum(x.get('verdict')=='FAIL' for x in adjudications); blocked=sum(x.get('verdict')=='BLOCKED' for x in adjudications); passed=sum(x.get('verdict')=='PASS' for x in adjudications)
    return {'schema':SCHEMA,'batch_contract':BATCH_CONTRACT,'parent_protocol':RECOVERY_PROTOCOL,'verdict':'PASS' if fail==0 else 'FAIL','reason':'BATCH11_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED' if fail==0 else 'BATCH11_ADJUDICATION_CONTAINS_FAIL','attempted':BATCH_SIZE,'pass':passed,'blocked':blocked,'fail':fail,'provenance':p,'adjudications':adjudications}


def main():
    runtime=json.loads(RUNTIME_PATH.read_text(encoding='utf-8'))
    report=adjudicate_runtime(runtime)
    ADJUDICATION_JSON.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    lines=['# HISTORICAL TRADING BREAKS RECOVERY — BATCH 11 ADJUDICATION','',f"**{report['verdict']} — `{report['reason']}`**",'',f"- attempted: `{report['attempted']}`",f"- PASS: `{report['pass']}`",f"- BLOCKED: `{report['blocked']}`",f"- FAIL: `{report['fail']}`",'']
    for item in report['adjudications']: lines.append(f"- `{item.get('target_date')}` → **{item.get('verdict')}** — record `{item.get('broker_record_id')}` — `{item.get('reason')}`")
    QUALIFICATION_MD.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    return 0 if report['verdict']=='PASS' else 1

if __name__=='__main__': raise SystemExit(main())
