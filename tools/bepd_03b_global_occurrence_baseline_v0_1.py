from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
from typing import Any

REPOSITORY = "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
BRANCH = "integration/system-v1"

AUTH = Path("GOVERNANCE/BEPD-03B-GLOBAL-WEEKLY-LIQUIDITY-OCCURRENCE-BASELINE-HUMAN-AUTHORIZATION-2026-10-05.md")
IMPL = Path("GOVERNANCE/BEPD-03B-GLOBAL-OCCURRENCE-BASELINE-IMPLEMENTATION-CONTRACT-V0.1.json")
DIMS = Path("GOVERNANCE/BEPD-03A-PREREGISTERED-OCCURRENCE-DIMENSIONS-V0.1.json")
MEASURE = Path("GOVERNANCE/BEPD-03A-WEEKLY-LIQUIDITY-OCCURRENCE-MEASUREMENT-CONTRACT-V0.1.json")
M05 = Path("GOVERNANCE/BEPD-03A-SMF-M05-OCCURRENCE-UNCERTAINTY-ACTIVATION-RECORD-V0.1.json")
ADJ = Path("GOVERNANCE/BEPD-03A-WEEKLY-LIQUIDITY-OCCURRENCE-MEASUREMENT-HUMAN-ADJUDICATION-2026-10-05.md")
OPP = Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/LEVEL_WEEK_OPPORTUNITY.jsonl")
LEVEL = Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/LEVEL_LEDGER.jsonl")
EVENT = Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/EVENT_LEDGER.jsonl")
SOURCE_RUN = Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/RUN_MANIFEST.json")
SELF = Path("tools/bepd_03b_global_occurrence_baseline_v0_1.py")

EXPECTED_BLOBS = {
    AUTH: "506e75c4c88a04019ae71156dbebf3c8f02d5d2b",
    IMPL: "a949cdf6b43a20a981e4a1fb4667de16f3b3c260",
    DIMS: "b7ec6a00e3d2281217c30e11d21527b5ce72aef6",
    MEASURE: "e117ddea324dd1b6906bc9eadcf8a5806b8b591a",
    M05: "53d33074038fa9d971b4672b1d981589da020a1e",
    ADJ: "b796fd69a9b40c0397cc89db5be755d59974b1fe",
    OPP: "0e97fb3b45bf8510b8531bb733cc155467a2ce49",
    LEVEL: "c50cea414a95e498199fbe0c426f4d246a1f1f99",
    EVENT: "0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2",
    SOURCE_RUN: "ccd5e31e1aeeadb4cceee24a8b8cd5eb0f8cf6d5",
}
SOURCE_RUN_ID = "68d858ffcb6cde1941cd16b73ad0590ef4ae9a9528fb3a2c82099fca5a33a821"
OUTPUT_SUBDIR = Path("artifacts/bepd03b/global-weekly-liquidity-occurrence-baseline-v0.1")


class BaselineFailure(RuntimeError):
    pass


def fail(code: str) -> None:
    raise BaselineFailure(code)


def git_text(root: Path, *args: str) -> str:
    cp = subprocess.run(["git","-C",str(root),*args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if cp.returncode != 0:
        fail(f"GIT_COMMAND_FAILED:{' '.join(args)}:{cp.stderr.strip()}")
    return cp.stdout.strip()


def git_blob(root: Path, rel: Path) -> str:
    return git_text(root, "rev-parse", f"HEAD:{rel.as_posix()}")


def canonical_hash(payload: dict[str, Any]) -> str:
    raw=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def verify_bindings(root: Path) -> None:
    for rel, expected in EXPECTED_BLOBS.items():
        actual=git_blob(root,rel)
        if actual != expected:
            fail(f"GIT_BINDING_MISMATCH:{rel.as_posix()}:{actual}:{expected}")


def read_opportunities(path: Path) -> list[dict[str, Any]]:
    rows=[]
    required={"run_id","level_id","target_week_id","dependence_key","side","level_age_weeks","swept_this_week","event_id","active_level_count_at_target_week_start"}
    with path.open("r",encoding="utf-8") as f:
        for n,line in enumerate(f,1):
            row=json.loads(line)
            if set(row) != required:
                fail(f"OPPORTUNITY_SCHEMA_DRIFT:{n}")
            if row["side"] not in {"HIGH","LOW"}:
                fail(f"INVALID_SIDE:{n}:{row['side']}")
            if not isinstance(row["swept_this_week"],bool):
                fail(f"NON_BOOLEAN_SWEEP:{n}")
            if row["dependence_key"] != row["target_week_id"]:
                fail(f"DEPENDENCE_KEY_DRIFT:{n}")
            if row["run_id"] != SOURCE_RUN_ID:
                fail(f"SOURCE_RUN_ID_DRIFT:{n}")
            if row["swept_this_week"] != (row["event_id"] is not None):
                fail(f"EVENT_FLAG_DRIFT:{n}")
            rows.append(row)
    if not rows:
        fail("EMPTY_OPPORTUNITY_LEDGER")
    return rows


def proportion(events: int, opportunities: int) -> str:
    if opportunities <= 0:
        fail("ZERO_DENOMINATOR")
    value=(Decimal(events)/Decimal(opportunities)).quantize(Decimal("0.000000000000000001"),rounding=ROUND_HALF_EVEN)
    return format(value,"f")


def view(view_id: str, side_filter: str | None, rows: list[dict[str, Any]]) -> dict[str, Any]:
    selected=rows if side_filter is None else [r for r in rows if r["side"]==side_filter]
    if not selected:
        fail(f"EMPTY_VIEW:{view_id}")
    events=sum(1 for r in selected if r["swept_this_week"])
    opportunities=len(selected)
    return {
        "view_id":view_id,
        "side_filter":side_filter,
        "eligible_target_week_count":len({r["target_week_id"] for r in selected}),
        "unique_level_count":len({r["level_id"] for r in selected}),
        "opportunity_count":opportunities,
        "event_count":events,
        "occurrence_fraction":f"{events}/{opportunities}",
        "occurrence_proportion_decimal":proportion(events,opportunities),
    }


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,default=None)
    args=parser.parse_args()
    root=args.root.resolve()
    out=(args.output_dir or (root/OUTPUT_SUBDIR)).resolve()

    try:
        verify_bindings(root)
        calc_blob=git_blob(root,SELF)
        head=git_text(root,"rev-parse","HEAD")
        tree=git_text(root,"rev-parse","HEAD^{tree}")

        source_run=json.loads((root/SOURCE_RUN).read_text(encoding="utf-8"))
        if source_run.get("run_id") != SOURCE_RUN_ID:
            fail("SOURCE_RUN_MANIFEST_ID_DRIFT")

        if out.exists():
            if any(out.iterdir()):
                fail(f"OUTPUT_DIR_NOT_EMPTY:{out}")
        else:
            out.mkdir(parents=True,exist_ok=False)

        rows=read_opportunities(root/OPP)

        views=[
            view("GLOBAL_ALL_SIDES",None,rows),
            view("HIGH","HIGH",rows),
            view("LOW","LOW",rows),
        ]

        global_v, high_v, low_v=views
        if global_v["opportunity_count"] != high_v["opportunity_count"]+low_v["opportunity_count"]:
            fail("GLOBAL_SIDE_OPPORTUNITY_PARITY")
        if global_v["event_count"] != high_v["event_count"]+low_v["event_count"]:
            fail("GLOBAL_SIDE_EVENT_PARITY")
        if global_v["unique_level_count"] != high_v["unique_level_count"]+low_v["unique_level_count"]:
            fail("GLOBAL_SIDE_LEVEL_PARITY")

        run_payload={
            "repository":REPOSITORY,
            "branch":BRANCH,
            "head":head,
            "tree":tree,
            "source_bepd02_run_id":SOURCE_RUN_ID,
            "opportunity_blob":EXPECTED_BLOBS[OPP],
            "authorization_blob":EXPECTED_BLOBS[AUTH],
            "implementation_contract_blob":EXPECTED_BLOBS[IMPL],
            "measurement_contract_blob":EXPECTED_BLOBS[MEASURE],
            "m05_activation_blob":EXPECTED_BLOBS[M05],
            "adjudication_blob":EXPECTED_BLOBS[ADJ],
            "calculator_blob":calc_blob,
        }
        run_id=canonical_hash(run_payload)

        result={
            "schema":"ATDS_BEPD_03B_GLOBAL_WEEKLY_LIQUIDITY_OCCURRENCE_BASELINE_RESULT_V0_1",
            "interpretation":"HISTORICAL_FIXED_CORPUS_DESCRIPTIVE_PROPORTION",
            "run_id":run_id,
            "source_bepd02_run_id":SOURCE_RUN_ID,
            "dependence_statement":"OPPORTUNITY ROW != IID OBSERVATION; dependence_key=target_week_id; multiple active levels in one target week are structurally dependent",
            "m05_generalization_uncertainty":"BLOCKED",
            "views":views,
            "forbidden_analytics_executed":False,
        }
        result_path=out/"RESULT.json"
        result_path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")

        manifest={
            "schema":"ATDS_BEPD_03B_GLOBAL_OCCURRENCE_BASELINE_RUN_MANIFEST_V0_1",
            "repository":REPOSITORY,
            "branch":BRANCH,
            "head":head,
            "tree":tree,
            "run_id":run_id,
            "source_bepd02_run_id":SOURCE_RUN_ID,
            "input_git_blobs":{
                "LEVEL_LEDGER":EXPECTED_BLOBS[LEVEL],
                "EVENT_LEDGER":EXPECTED_BLOBS[EVENT],
                "LEVEL_WEEK_OPPORTUNITY":EXPECTED_BLOBS[OPP],
                "RUN_MANIFEST":EXPECTED_BLOBS[SOURCE_RUN],
            },
            "policy_git_blobs":{
                "BEPD03B_AUTHORIZATION":EXPECTED_BLOBS[AUTH],
                "BEPD03B_IMPLEMENTATION_CONTRACT":EXPECTED_BLOBS[IMPL],
                "BEPD03A_DIMENSIONS":EXPECTED_BLOBS[DIMS],
                "BEPD03A_MEASUREMENT_CONTRACT":EXPECTED_BLOBS[MEASURE],
                "BEPD03A_M05_ACTIVATION":EXPECTED_BLOBS[M05],
                "BEPD03A_ADJUDICATION":EXPECTED_BLOBS[ADJ],
            },
            "calculator_blob":calc_blob,
            "output_files":[],
            "forbidden_analytics_executed":False,
        }
        manifest_path=out/"RUN_MANIFEST.json"
        for p in (result_path,):
            manifest["output_files"].append({
                "relative_path":p.relative_to(root).as_posix(),
                "sha256":sha256_file(p),
                "size_bytes":p.stat().st_size,
            })
        manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")

        print(json.dumps({
            "status":"BEPD03B_GLOBAL_OCCURRENCE_BASELINE_COMPLETE",
            "run_id":run_id,
            "result_sha256":sha256_file(result_path),
            "manifest_sha256":sha256_file(manifest_path),
            "views":views
        },sort_keys=True))
        return 0
    except BaselineFailure as exc:
        print(f"BEPD03B_BASELINE_FAIL:{exc}")
        return 1


if __name__=="__main__":
    raise SystemExit(main())
