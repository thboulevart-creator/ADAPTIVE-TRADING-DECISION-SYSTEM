from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
from typing import Any

AUTH=Path("GOVERNANCE/BEPD-03B-GLOBAL-WEEKLY-LIQUIDITY-OCCURRENCE-BASELINE-HUMAN-AUTHORIZATION-2026-10-05.md")
IMPL=Path("GOVERNANCE/BEPD-03B-GLOBAL-OCCURRENCE-BASELINE-IMPLEMENTATION-CONTRACT-V0.1.json")
CALC=Path("tools/bepd_03b_global_occurrence_baseline_v0_1.py")
BREAKER_CONTRACT=Path("GOVERNANCE/BEPD-03B-FROZEN-GLOBAL-OCCURRENCE-BASELINE-BREAKER-CONTRACT-V0.1.json")
MEASURE=Path("GOVERNANCE/BEPD-03A-WEEKLY-LIQUIDITY-OCCURRENCE-MEASUREMENT-CONTRACT-V0.1.json")
M05=Path("GOVERNANCE/BEPD-03A-SMF-M05-OCCURRENCE-UNCERTAINTY-ACTIVATION-RECORD-V0.1.json")
ADJ=Path("GOVERNANCE/BEPD-03A-WEEKLY-LIQUIDITY-OCCURRENCE-MEASUREMENT-HUMAN-ADJUDICATION-2026-10-05.md")
OPP=Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/LEVEL_WEEK_OPPORTUNITY.jsonl")
EVENT=Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/EVENT_LEDGER.jsonl")
LEVEL=Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/LEVEL_LEDGER.jsonl")
SOURCE_RUN=Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/RUN_MANIFEST.json")

EXPECTED_BLOBS={
    AUTH:"506e75c4c88a04019ae71156dbebf3c8f02d5d2b",
    IMPL:"a949cdf6b43a20a981e4a1fb4667de16f3b3c260",
    CALC:"7f8cebd92437ec724c8ebe81f0e9befdccc7dba4",
    BREAKER_CONTRACT:"a559aae07f7c5471949c9c5de6cfa6fdcaa20926",
    MEASURE:"e117ddea324dd1b6906bc9eadcf8a5806b8b591a",
    M05:"53d33074038fa9d971b4672b1d981589da020a1e",
    ADJ:"b796fd69a9b40c0397cc89db5be755d59974b1fe",
    OPP:"0e97fb3b45bf8510b8531bb733cc155467a2ce49",
    EVENT:"0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2",
    LEVEL:"c50cea414a95e498199fbe0c426f4d246a1f1f99",
    SOURCE_RUN:"ccd5e31e1aeeadb4cceee24a8b8cd5eb0f8cf6d5",
}
SOURCE_RUN_ID="68d858ffcb6cde1941cd16b73ad0590ef4ae9a9528fb3a2c82099fca5a33a821"


class BreakerFailure(AssertionError):
    pass


def fail(code:str)->None:
    print(f"BEPD_03B_BREAKER_FAIL:{code}")
    raise SystemExit(1)


def require(condition:bool, code:str)->None:
    if not condition:
        raise BreakerFailure(code)


def eq(actual,expected,code:str)->None:
    if actual!=expected:
        raise BreakerFailure(f"{code}:expected={expected!r}:actual={actual!r}")


def git_blob(root:Path,rel:Path)->str:
    cp=subprocess.run(["git","-C",str(root),"rev-parse",f"HEAD:{rel.as_posix()}"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=False)
    if cp.returncode!=0:
        raise BreakerFailure(f"MISSING_BOUND_OBJECT:{rel.as_posix()}")
    return cp.stdout.strip()


def canonical_hash(payload:dict[str,Any])->str:
    raw=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def read_jsonl(path:Path)->list[dict[str,Any]]:
    out=[]
    with path.open("r",encoding="utf-8") as f:
        for n,line in enumerate(f,1):
            if not line.endswith("\n"):
                raise BreakerFailure(f"JSONL_LINE_END:{path.name}:{n}")
            out.append(json.loads(line))
    return out


def decimal_prop(events:int,opportunities:int)->str:
    if opportunities<=0:
        raise BreakerFailure("ZERO_DENOMINATOR")
    return format((Decimal(events)/Decimal(opportunities)).quantize(Decimal("0.000000000000000001"),rounding=ROUND_HALF_EVEN),"f")


def expected_view(view_id:str, side:str|None, rows:list[dict[str,Any]])->dict[str,Any]:
    selected=rows if side is None else [r for r in rows if r["side"]==side]
    events=sum(1 for r in selected if r["swept_this_week"] is True)
    n=len(selected)
    return {
        "view_id":view_id,
        "side_filter":side,
        "eligible_target_week_count":len({r["target_week_id"] for r in selected}),
        "unique_level_count":len({r["level_id"] for r in selected}),
        "opportunity_count":n,
        "event_count":events,
        "occurrence_fraction":f"{events}/{n}",
        "occurrence_proportion_decimal":decimal_prop(events,n),
    }


def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,required=True)
    parser.add_argument("--result-dir",type=Path,required=True)
    args=parser.parse_args()
    root=args.root.resolve()
    out=args.result_dir.resolve()

    try:
        for rel,expected in EXPECTED_BLOBS.items():
            eq(git_blob(root,rel),expected,f"GIT_BLOB:{rel.as_posix()}")

        bc=json.loads((root/BREAKER_CONTRACT).read_text(encoding="utf-8"))
        eq([x["id"] for x in bc["cases"]],[f"BEPD03B-B{i:02d}" for i in range(1,26)],"CASE_IDS")
        eq(bc["exact_result_contract"]["m05_generalization_uncertainty"],"BLOCKED","BREAKER_M05")
        eq(bc["authority"]["calendar_segmentation"],False,"AUTH_CALENDAR")
        eq(bc["authority"]["inference"],False,"AUTH_INFERENCE")

        expected_files={"RESULT.json","RUN_MANIFEST.json"}
        require(out.is_dir(),"RESULT_DIR_MISSING")
        eq({p.name for p in out.iterdir()},expected_files,"RESULT_FILE_SURFACE")

        result=json.loads((out/"RESULT.json").read_text(encoding="utf-8"))
        manifest=json.loads((out/"RUN_MANIFEST.json").read_text(encoding="utf-8"))

        result_fields={"schema","interpretation","run_id","source_bepd02_run_id","dependence_statement","m05_generalization_uncertainty","views","forbidden_analytics_executed"}
        eq(set(result),result_fields,"RESULT_TOP_LEVEL_FIELDS")
        eq(result["schema"],"ATDS_BEPD_03B_GLOBAL_WEEKLY_LIQUIDITY_OCCURRENCE_BASELINE_RESULT_V0_1","RESULT_SCHEMA")
        eq(result["interpretation"],"HISTORICAL_FIXED_CORPUS_DESCRIPTIVE_PROPORTION","INTERPRETATION")
        eq(result["source_bepd02_run_id"],SOURCE_RUN_ID,"SOURCE_RUN_ID")
        eq(result["m05_generalization_uncertainty"],"BLOCKED","M05_BLOCKED")
        eq(result["forbidden_analytics_executed"],False,"FORBIDDEN_ANALYTICS_FLAG")
        require("OPPORTUNITY ROW != IID OBSERVATION" in result["dependence_statement"],"DEPENDENCE_STATEMENT")
        require("dependence_key=target_week_id" in result["dependence_statement"],"DEPENDENCE_KEY_STATEMENT")

        opps=read_jsonl(root/OPP)
        events=read_jsonl(root/EVENT)
        require(len(opps)>0,"EMPTY_OPPORTUNITIES")
        for i,r in enumerate(opps):
            require(r["side"] in {"HIGH","LOW"},f"SIDE_DOMAIN:{i}")
            eq(r["dependence_key"],r["target_week_id"],f"DEPENDENCE_KEY:{i}")
            require(isinstance(r["swept_this_week"],bool),f"SWEEP_BOOL:{i}")
            eq(r["swept_this_week"],r["event_id"] is not None,f"EVENT_FLAG:{i}")

        expected_views=[
            expected_view("GLOBAL_ALL_SIDES",None,opps),
            expected_view("HIGH","HIGH",opps),
            expected_view("LOW","LOW",opps),
        ]
        eq(result["views"],expected_views,"VIEW_RECOMPUTATION")

        global_v,high_v,low_v=expected_views
        eq(global_v["opportunity_count"],len(opps),"NO_ROW_EXCLUSION")
        eq(global_v["event_count"],sum(1 for r in opps if r["swept_this_week"]),"GLOBAL_EVENT_DIRECT")
        eq(global_v["opportunity_count"],high_v["opportunity_count"]+low_v["opportunity_count"],"SIDE_OPPORTUNITY_PARITY")
        eq(global_v["event_count"],high_v["event_count"]+low_v["event_count"],"SIDE_EVENT_PARITY")
        eq(global_v["unique_level_count"],high_v["unique_level_count"]+low_v["unique_level_count"],"SIDE_LEVEL_PARITY")
        eq(set(r["target_week_id"] for r in opps),set(r["target_week_id"] for r in opps if r["side"]=="HIGH")|set(r["target_week_id"] for r in opps if r["side"]=="LOW"),"TARGET_WEEK_UNION")

        event_counts={
            "GLOBAL_ALL_SIDES":len(events),
            "HIGH":sum(1 for r in events if r["side"]=="HIGH"),
            "LOW":sum(1 for r in events if r["side"]=="LOW"),
        }
        for v in expected_views:
            eq(v["event_count"],event_counts[v["view_id"]],f"EVENT_LEDGER_PARITY:{v['view_id']}")

        view_fields={"view_id","side_filter","eligible_target_week_count","unique_level_count","opportunity_count","event_count","occurrence_fraction","occurrence_proportion_decimal"}
        for v in result["views"]:
            eq(set(v),view_fields,f"VIEW_FIELD_SET:{v.get('view_id')}")
        eq([v["view_id"] for v in result["views"]],["GLOBAL_ALL_SIDES","HIGH","LOW"],"VIEW_ORDER")

        forbidden_tokens={"confidence_interval","standard_error","p_value","significance","rank","best","worst","target_month","target_year","level_age_band","take_day_ny","bootstrap"}
        serialized=json.dumps(result,sort_keys=True).lower()
        for token in forbidden_tokens:
            require(token.lower() not in serialized,f"FORBIDDEN_RESULT_TOKEN:{token}")

        manifest_fields={"schema","repository","branch","head","tree","run_id","source_bepd02_run_id","input_git_blobs","policy_git_blobs","calculator_blob","output_files","forbidden_analytics_executed"}
        eq(set(manifest),manifest_fields,"MANIFEST_FIELD_SET")
        eq(manifest["schema"],"ATDS_BEPD_03B_GLOBAL_OCCURRENCE_BASELINE_RUN_MANIFEST_V0_1","MANIFEST_SCHEMA")
        eq(manifest["repository"],"thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM","REPOSITORY")
        eq(manifest["branch"],"integration/system-v1","BRANCH")
        eq(manifest["source_bepd02_run_id"],SOURCE_RUN_ID,"MANIFEST_SOURCE_RUN")
        eq(manifest["calculator_blob"],EXPECTED_BLOBS[CALC],"CALCULATOR_BLOB")
        eq(manifest["forbidden_analytics_executed"],False,"MANIFEST_FORBIDDEN_FLAG")
        eq(manifest["input_git_blobs"],{
            "LEVEL_LEDGER":EXPECTED_BLOBS[LEVEL],
            "EVENT_LEDGER":EXPECTED_BLOBS[EVENT],
            "LEVEL_WEEK_OPPORTUNITY":EXPECTED_BLOBS[OPP],
            "RUN_MANIFEST":EXPECTED_BLOBS[SOURCE_RUN],
        },"INPUT_BLOBS")
        eq(manifest["policy_git_blobs"],{
            "BEPD03B_AUTHORIZATION":EXPECTED_BLOBS[AUTH],
            "BEPD03B_IMPLEMENTATION_CONTRACT":EXPECTED_BLOBS[IMPL],
            "BEPD03A_DIMENSIONS":"b7ec6a00e3d2281217c30e11d21527b5ce72aef6",
            "BEPD03A_MEASUREMENT_CONTRACT":EXPECTED_BLOBS[MEASURE],
            "BEPD03A_M05_ACTIVATION":EXPECTED_BLOBS[M05],
            "BEPD03A_ADJUDICATION":EXPECTED_BLOBS[ADJ],
        },"POLICY_BLOBS")

        run_payload={
            "repository":manifest["repository"],
            "branch":manifest["branch"],
            "head":manifest["head"],
            "tree":manifest["tree"],
            "source_bepd02_run_id":SOURCE_RUN_ID,
            "opportunity_blob":EXPECTED_BLOBS[OPP],
            "authorization_blob":EXPECTED_BLOBS[AUTH],
            "implementation_contract_blob":EXPECTED_BLOBS[IMPL],
            "measurement_contract_blob":EXPECTED_BLOBS[MEASURE],
            "m05_activation_blob":EXPECTED_BLOBS[M05],
            "adjudication_blob":EXPECTED_BLOBS[ADJ],
            "calculator_blob":EXPECTED_BLOBS[CALC],
        }
        eq(canonical_hash(run_payload),manifest["run_id"],"RUN_ID_RECOMPUTE")
        eq(result["run_id"],manifest["run_id"],"RESULT_MANIFEST_RUN_ID")

        eq(len(manifest["output_files"]),1,"MANIFEST_OUTPUT_COUNT")
        out_info=manifest["output_files"][0]
        result_path=out/"RESULT.json"
        eq(out_info["relative_path"],"artifacts/bepd03b/global-weekly-liquidity-occurrence-baseline-v0.1/RESULT.json","RESULT_REL_PATH")
        eq(out_info["sha256"],sha256_file(result_path),"RESULT_SHA256")
        eq(out_info["size_bytes"],result_path.stat().st_size,"RESULT_SIZE")

        print("BEPD_03B_GLOBAL_OCCURRENCE_BASELINE_BREAKER_PASS")
        return 0
    except (BreakerFailure,KeyError,ValueError,json.JSONDecodeError) as exc:
        fail(str(exc))


if __name__=="__main__":
    sys.exit(main())
