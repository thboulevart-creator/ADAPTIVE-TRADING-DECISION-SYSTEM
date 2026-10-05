from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_EVEN
from fractions import Fraction
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

REPOSITORY="thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
BRANCH="integration/system-v1"

AUTH=Path("GOVERNANCE/BEPD-03E-EVENT-CONDITIONAL-TAKE-DAY-NY-DISTRIBUTION-HUMAN-AUTHORIZATION-2026-10-05.md")
IMPL=Path("GOVERNANCE/BEPD-03E-TAKE-DAY-NY-DISTRIBUTION-IMPLEMENTATION-CONTRACT-V0.1.json")
DIMS=Path("GOVERNANCE/BEPD-03A-PREREGISTERED-OCCURRENCE-DIMENSIONS-V0.1.json")
MEASURE=Path("GOVERNANCE/BEPD-03A-WEEKLY-LIQUIDITY-OCCURRENCE-MEASUREMENT-CONTRACT-V0.1.json")
M05=Path("GOVERNANCE/BEPD-03A-SMF-M05-OCCURRENCE-UNCERTAINTY-ACTIVATION-RECORD-V0.1.json")
ADJ=Path("GOVERNANCE/BEPD-03A-WEEKLY-LIQUIDITY-OCCURRENCE-MEASUREMENT-HUMAN-ADJUDICATION-2026-10-05.md")
Q03B=Path("reports/program/2026-10-05-BEPD-03B-GLOBAL-WEEKLY-LIQUIDITY-OCCURRENCE-BASELINE-QUALIFICATION-V0.1.md")
Q03C=Path("reports/program/2026-10-05-BEPD-03C-PREREGISTERED-CALENDAR-OCCURRENCE-MAP-QUALIFICATION-V0.1.md")
Q03D=Path("reports/program/2026-10-05-BEPD-03D-LEVEL-AGE-OCCURRENCE-MAP-QUALIFICATION-V0.1.md")
EVENT=Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/EVENT_LEDGER.jsonl")
SOURCE_RUN=Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/RUN_MANIFEST.json")
SELF=Path("tools/bepd_03e_take_day_ny_distribution_v0_1.py")

EXPECTED_BLOBS={
 AUTH:"e6e91abc1449ecc55f2241446e80da657148ca8f",
 IMPL:"5a4aa7f22abd68e47fe67b888314a33d0128530a",
 DIMS:"b7ec6a00e3d2281217c30e11d21527b5ce72aef6",
 MEASURE:"e117ddea324dd1b6906bc9eadcf8a5806b8b591a",
 M05:"53d33074038fa9d971b4672b1d981589da020a1e",
 ADJ:"b796fd69a9b40c0397cc89db5be755d59974b1fe",
 Q03B:"e88bcce2d3256a9e374e76cfb5e9ebc641316d56",
 Q03C:"fd3b0caa97361e61e81510a2e69f0fbeb25cbe12",
 Q03D:"c7151af0bd7acce71f5d7f0e1e059c6f141c57d1",
 EVENT:"0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2",
 SOURCE_RUN:"ccd5e31e1aeeadb4cceee24a8b8cd5eb0f8cf6d5",
}
SOURCE_RUN_ID="68d858ffcb6cde1941cd16b73ad0590ef4ae9a9528fb3a2c82099fca5a33a821"
OUTPUT_SUBDIR=Path("artifacts/bepd03e/event-conditional-take-day-ny-distribution-v0.1")
CATEGORIES=["SUNDAY_OPEN","MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY"]
NY=ZoneInfo("America/New_York")
DECIMAL_QUANT=Decimal("0.000000000000000001")
DECIMAL_TOLERANCE=Decimal("0.000000000000000003")


class TakeDayFailure(RuntimeError):
    pass


def fail(code:str)->None:
    raise TakeDayFailure(code)


def git_text(root:Path,*args:str)->str:
    cp=subprocess.run(["git","-C",str(root),*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=False)
    if cp.returncode!=0:
        fail(f"GIT_COMMAND_FAILED:{' '.join(args)}:{cp.stderr.strip()}")
    return cp.stdout.strip()


def git_blob(root:Path,rel:Path)->str:
    return git_text(root,"rev-parse",f"HEAD:{rel.as_posix()}")


def canonical_hash(payload:dict[str,Any])->str:
    raw=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def verify_bindings(root:Path)->None:
    for rel,expected in EXPECTED_BLOBS.items():
        actual=git_blob(root,rel)
        if actual!=expected:
            fail(f"GIT_BINDING_MISMATCH:{rel.as_posix()}:{actual}:{expected}")


def parse_utc(value:Any,row_number:int)->datetime:
    if not isinstance(value,str) or not value:
        fail(f"MISSING_TAKE_H1_CLOSE_UTC:{row_number}")
    try:
        dt=datetime.fromisoformat(value)
    except ValueError as exc:
        fail(f"INVALID_TAKE_H1_CLOSE_UTC:{row_number}:{exc}")
    if dt.tzinfo is None or dt.utcoffset() is None:
        fail(f"NAIVE_TAKE_H1_CLOSE_UTC:{row_number}")
    if dt.utcoffset().total_seconds()!=0:
        fail(f"NON_UTC_TAKE_H1_CLOSE_UTC:{row_number}:{value}")
    return dt.astimezone(timezone.utc)


def category_for_utc(dt_utc:datetime)->str:
    local=dt_utc.astimezone(NY)
    weekday=local.weekday()
    mapping={6:"SUNDAY_OPEN",0:"MONDAY",1:"TUESDAY",2:"WEDNESDAY",3:"THURSDAY",4:"FRIDAY"}
    if weekday==5:
        fail(f"SATURDAY_LOCAL_TAKE:{local.isoformat()}")
    if weekday not in mapping:
        fail(f"UNMAPPED_LOCAL_WEEKDAY:{weekday}:{local.isoformat()}")
    return mapping[weekday]


def validate_timezone_runtime()->None:
    if getattr(NY,"key",None)!="America/New_York":
        fail(f"TIMEZONE_KEY_DRIFT:{getattr(NY,'key',None)}")
    probes=[
      ("2024-03-10T06:59:00+00:00","2024-03-10T01:59:00-05:00"),
      ("2024-03-10T07:00:00+00:00","2024-03-10T03:00:00-04:00"),
      ("2024-11-03T05:59:00+00:00","2024-11-03T01:59:00-04:00"),
      ("2024-11-03T06:00:00+00:00","2024-11-03T01:00:00-05:00"),
    ]
    for raw,expected in probes:
        actual=datetime.fromisoformat(raw).astimezone(NY).isoformat()
        if actual!=expected:
            fail(f"DST_PROBE_MISMATCH:{raw}:{actual}:{expected}")


def read_events(path:Path)->list[dict[str,Any]]:
    rows=[]
    required={"run_id","event_id","sweep_cluster_id","target_week_id","take_h1_close_utc"}
    with path.open("r",encoding="utf-8") as f:
        for n,line in enumerate(f,1):
            row=json.loads(line)
            missing=[k for k in required if k not in row]
            if missing:
                fail(f"EVENT_SCHEMA_MISSING:{n}:{','.join(sorted(missing))}")
            if row["run_id"]!=SOURCE_RUN_ID:
                fail(f"SOURCE_RUN_ID_DRIFT:{n}")
            if not isinstance(row["event_id"],str) or not row["event_id"]:
                fail(f"INVALID_EVENT_ID:{n}")
            if not isinstance(row["sweep_cluster_id"],str) or not row["sweep_cluster_id"]:
                fail(f"INVALID_SWEEP_CLUSTER_ID:{n}")
            if not isinstance(row["target_week_id"],str) or not row["target_week_id"]:
                fail(f"INVALID_TARGET_WEEK_ID:{n}")
            dt=parse_utc(row["take_h1_close_utc"],n)
            category=category_for_utc(dt)
            rows.append({
              "event_id":row["event_id"],
              "sweep_cluster_id":row["sweep_cluster_id"],
              "target_week_id":row["target_week_id"],
              "take_h1_close_utc":row["take_h1_close_utc"],
              "take_day_ny":category,
            })
    if not rows:
        fail("EMPTY_EVENT_LEDGER")
    if len({r["event_id"] for r in rows})!=len(rows):
        fail("DUPLICATE_EVENT_ID")
    return rows


def share_decimal(count:int,total:int)->str:
    if total<=0:
        fail("ZERO_EVENT_DENOMINATOR")
    value=(Decimal(count)/Decimal(total)).quantize(DECIMAL_QUANT,rounding=ROUND_HALF_EVEN)
    return format(value,"f")


def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,default=None)
    args=parser.parse_args()
    root=args.root.resolve()
    out=(args.output_dir or (root/OUTPUT_SUBDIR)).resolve()

    try:
        verify_bindings(root)
        validate_timezone_runtime()
        calculator_blob=git_blob(root,SELF)
        head=git_text(root,"rev-parse","HEAD")
        tree=git_text(root,"rev-parse","HEAD^{tree}")

        source_run=json.loads((root/SOURCE_RUN).read_text(encoding="utf-8"))
        if source_run.get("run_id")!=SOURCE_RUN_ID:
            fail("SOURCE_RUN_MANIFEST_ID_DRIFT")

        if out.exists():
            if any(out.iterdir()):
                fail(f"OUTPUT_DIR_NOT_EMPTY:{out}")
        else:
            out.mkdir(parents=True,exist_ok=False)

        events=read_events(root/EVENT)
        total=len(events)
        cells=[]
        exact_sum=Fraction(0,1)
        decimal_sum=Decimal("0")
        for category in CATEGORIES:
            count=sum(1 for r in events if r["take_day_ny"]==category)
            frac=Fraction(count,total)
            exact_sum+=frac
            dec=share_decimal(count,total)
            decimal_sum+=Decimal(dec)
            cells.append({
              "category":category,
              "event_count":count,
              "conditional_event_fraction":f"{count}/{total}",
              "conditional_event_share_decimal":dec,
            })

        if sum(c["event_count"] for c in cells)!=total:
            fail("EVENT_COUNT_RECONCILIATION")
        if exact_sum!=Fraction(1,1):
            fail(f"EXACT_SHARE_RECONCILIATION:{exact_sum}")
        decimal_error=abs(decimal_sum-Decimal("1"))
        if decimal_error>DECIMAL_TOLERANCE:
            fail(f"DECIMAL_SHARE_RECONCILIATION:{decimal_sum}:{decimal_error}")

        run_payload={
          "repository":REPOSITORY,
          "branch":BRANCH,
          "head":head,
          "tree":tree,
          "source_bepd02_run_id":SOURCE_RUN_ID,
          "event_ledger_blob":EXPECTED_BLOBS[EVENT],
          "authorization_blob":EXPECTED_BLOBS[AUTH],
          "implementation_contract_blob":EXPECTED_BLOBS[IMPL],
          "dimensions_blob":EXPECTED_BLOBS[DIMS],
          "measurement_contract_blob":EXPECTED_BLOBS[MEASURE],
          "m05_activation_blob":EXPECTED_BLOBS[M05],
          "calculator_blob":calculator_blob,
        }
        run_id=canonical_hash(run_payload)

        result={
          "schema":"ATDS_BEPD_03E_EVENT_CONDITIONAL_TAKE_DAY_NY_DISTRIBUTION_RESULT_V0_1",
          "interpretation":"EVENT_CONDITIONAL_HISTORICAL_FIXED_CORPUS_TAKE_TIMING_DISTRIBUTION",
          "run_id":run_id,
          "source_bepd02_run_id":SOURCE_RUN_ID,
          "population":{
            "unit":"one LEVEL_SWEEP_EVENT / one EVENT_LEDGER row",
            "condition":"sweep already observed",
            "total_sweep_event_count":total,
            "denominator_source":"EVENT_LEDGER"
          },
          "dependence_statement":"EVENT != IID OBSERVATION; sweep_cluster_id and target_week_id preserve dependence/provenance; multiple level events in one cluster or target week are dependent",
          "m05_generalization_uncertainty":"BLOCKED",
          "dimension":{
            "dimension_id":"V06_TAKE_DAY_NY",
            "timezone":"America/New_York",
            "timestamp_source":"take_h1_close_utc",
            "category_order":CATEGORIES,
            "cells":cells
          },
          "decimal_reconciliation":{
            "sum_of_cell_decimal_shares":format(decimal_sum,"f"),
            "absolute_error_from_one":format(decimal_error,"f"),
            "tolerance":"0.000000000000000003",
            "within_tolerance":True
          },
          "forbidden_analytics_executed":False,
        }

        result_path=out/"RESULT.json"
        result_path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")

        manifest={
          "schema":"ATDS_BEPD_03E_TAKE_DAY_NY_DISTRIBUTION_RUN_MANIFEST_V0_1",
          "repository":REPOSITORY,
          "branch":BRANCH,
          "head":head,
          "tree":tree,
          "run_id":run_id,
          "source_bepd02_run_id":SOURCE_RUN_ID,
          "input_git_blobs":{
            "EVENT_LEDGER":EXPECTED_BLOBS[EVENT],
            "BEPD02_RUN_MANIFEST":EXPECTED_BLOBS[SOURCE_RUN],
          },
          "policy_git_blobs":{
            "BEPD03E_AUTHORIZATION":EXPECTED_BLOBS[AUTH],
            "BEPD03E_IMPLEMENTATION_CONTRACT":EXPECTED_BLOBS[IMPL],
            "BEPD03A_DIMENSIONS":EXPECTED_BLOBS[DIMS],
            "BEPD03A_MEASUREMENT_CONTRACT":EXPECTED_BLOBS[MEASURE],
            "BEPD03A_M05_ACTIVATION":EXPECTED_BLOBS[M05],
            "BEPD03A_ADJUDICATION":EXPECTED_BLOBS[ADJ],
            "BEPD03B_QUALIFICATION":EXPECTED_BLOBS[Q03B],
            "BEPD03C_QUALIFICATION":EXPECTED_BLOBS[Q03C],
            "BEPD03D_QUALIFICATION":EXPECTED_BLOBS[Q03D],
          },
          "timezone_runtime":{
            "zoneinfo_key":"America/New_York",
            "dst_probes_passed":True
          },
          "calculator_blob":calculator_blob,
          "output_files":[{
            "relative_path":result_path.relative_to(root).as_posix(),
            "sha256":sha256_file(result_path),
            "size_bytes":result_path.stat().st_size,
          }],
          "forbidden_analytics_executed":False,
        }
        manifest_path=out/"RUN_MANIFEST.json"
        manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")

        print(json.dumps({
          "status":"BEPD03E_TAKE_DAY_NY_DISTRIBUTION_COMPLETE",
          "run_id":run_id,
          "total_sweep_event_count":total,
          "result_sha256":sha256_file(result_path),
          "manifest_sha256":sha256_file(manifest_path),
          "category_count":len(cells)
        },sort_keys=True))
        return 0
    except TakeDayFailure as exc:
        print(f"BEPD03E_TAKE_DAY_FAIL:{exc}")
        return 1


if __name__=="__main__":
    raise SystemExit(main())
