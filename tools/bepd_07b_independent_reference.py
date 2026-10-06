#!/usr/bin/env python3
"""Independent BEPD-07B recomputation.

Does not import the canonical runner. Reimplements:
- AP0 provenance verification,
- canonical target-week path reconstruction,
- HIGH/LOW behavioral excursion geometry,
- Type-7 quantiles and exact ECDFs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from bisect import bisect_left, bisect_right
from datetime import datetime, timedelta, time, timezone
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from fractions import Fraction
from pathlib import Path
from zoneinfo import ZoneInfo

getcontext().prec = 80
Q18 = Decimal("0.000000000000000001")
ZERO = Decimal(0)
NY = ZoneInfo("America/New_York")
EXPECTED_DATASET = "USTECH_PROFILE_MINUTE_CORE_V0_1"
EXPECTED_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
EXPECTED_FILE_SET_DIGEST = "1ff14ab4fea11c2480088a322f5bec23ea183de14cbc65ee6c684c7ea185062a"
QUANTILE_METHOD = "HYNDMAN_FAN_TYPE_7"
ECDF_METHOD = "EXACT_UNSMOOTHED_UNBINNED"

PROBS = {
    "P01": Decimal("0.01"),
    "P05": Decimal("0.05"),
    "P10": Decimal("0.10"),
    "P25": Decimal("0.25"),
    "P50": Decimal("0.50"),
    "P75": Decimal("0.75"),
    "P90": Decimal("0.90"),
    "P95": Decimal("0.95"),
    "P99": Decimal("0.99"),
}


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()


def q18(v: Decimal) -> str:
    return format(v.quantize(Q18,rounding=ROUND_HALF_EVEN),"f")


def rf(n:int,d:int)->str:
    f=Fraction(n,d)
    return str(f.numerator) if f.denominator==1 else f"{f.numerator}/{f.denominator}"


def utc_ms(s:str)->int:
    d=datetime.fromisoformat(s.replace("Z","+00:00"))
    if d.tzinfo is None or d.utcoffset() is None or d.utcoffset().total_seconds()!=0:
        raise ValueError("timestamp not UTC")
    return int(d.timestamp()*1000)


def week_end_ms(week_id:str)->int:
    monday=datetime.strptime(week_id,"%Y-%m-%d").date()
    start=datetime.combine(monday-timedelta(days=1),time(18,0),tzinfo=NY)
    end=start+timedelta(days=7)
    return int(end.astimezone(timezone.utc).timestamp()*1000)


def qtype7(v:list[Decimal],p:Decimal)->Decimal:
    s=sorted(v)
    n=len(s)
    if n==1:return s[0]
    h=Decimal(1)+Decimal(n-1)*p
    j=int(h)
    g=h-Decimal(j)
    if j>=n:return s[-1]
    return s[j-1]+g*(s[j]-s[j-1])


def surface(v:list[Decimal])->dict:
    s=sorted(v)
    n=len(s)
    qs={k:q18(qtype7(s,p)) for k,p in PROBS.items()}
    z=sum(x==ZERO for x in s)
    counts={}
    for x in s:counts[x]=counts.get(x,0)+1
    cum=0
    ecdf=[]
    for x in sorted(counts):
        cum+=counts[x]
        ecdf.append({
            "support_value":q18(x),
            "support_count":counts[x],
            "cumulative_count":cum,
            "cumulative_fraction":rf(cum,n),
            "cumulative_decimal":q18(Decimal(cum)/Decimal(n)),
        })
    return {
        "N":n,
        "MINIMUM":q18(s[0]),
        "MAXIMUM":q18(s[-1]),
        "MEAN":q18(sum(s,ZERO)/Decimal(n)),
        "MEDIAN":qs["P50"],
        **qs,
        "ZERO_COUNT":z,
        "ZERO_FRACTION":rf(z,n),
        "ZERO_FRACTION_DECIMAL":q18(Decimal(z)/Decimal(n)),
        "EMPIRICAL_CDF":ecdf,
    }


def verify_ap0(root:Path):
    mp=root/"AP0-MANIFEST.json"
    if sha256_file(mp)!=EXPECTED_MANIFEST_SHA256:
        raise RuntimeError("manifest hash mismatch")
    m=json.loads(mp.read_text(encoding="utf-8"))
    if m["output_identity"]!=EXPECTED_DATASET or len(m["files"])!=61:
        raise RuntimeError("manifest identity/count mismatch")
    lines=[]
    for e in m["files"]:
        p=root/Path(e["relative_path"])
        if sha256_file(p)!=e["sha256"]:
            raise RuntimeError("file sha mismatch "+e["relative_path"])
        lines.append(f"{e['relative_path']}:{e['sha256']}")
    digest=hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest()
    if digest!=EXPECTED_FILE_SET_DIGEST:
        raise RuntimeError("file set mismatch")
    return m


def load_arrays(root:Path,m):
    import pyarrow.parquet as pq
    ts=[]; hi=[]; lo=[]
    for e in m["files"]:
        t=pq.read_table(root/Path(e["relative_path"]),columns=["minute_start_ms_utc","mid_high","mid_low"])
        ts.extend(int(x) for x in t["minute_start_ms_utc"].to_pylist())
        hi.extend(float(x) for x in t["mid_high"].to_pylist())
        lo.extend(float(x) for x in t["mid_low"].to_pylist())
    if len(ts)!=1709180 or any(ts[i]>=ts[i+1] for i in range(len(ts)-1)):
        raise RuntimeError("AP0 ordering/rows mismatch")
    return ts,hi,lo


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--event-ledger",required=True)
    ap.add_argument("--ap0-root",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()

    events=[json.loads(x) for x in Path(args.event_ledger).read_text(encoding="utf-8").splitlines() if x.strip()]
    if len(events)!=472 or len({e["event_id"] for e in events})!=472:
        raise RuntimeError("event population mismatch")

    root=Path(args.ap0_root)
    m=verify_ap0(root)
    ts,highs,lows=load_arrays(root,m)

    rein=[]; ext=[]; diag=[]
    for e in events:
        if e["dataset_id"]!=EXPECTED_DATASET or e["dataset_manifest_sha256"]!=EXPECTED_MANIFEST_SHA256:
            raise RuntimeError("event AP0 binding mismatch")
        start=utc_ms(e["take_h1_close_utc"])
        end=week_end_ms(e["target_week_id"])
        a=bisect_right(ts,start)
        b=bisect_left(ts,end)
        if b<=a:raise RuntimeError("empty path")
        p_hi=highs[a:b]; p_lo=lows[a:b]; p_ts=ts[a:b]
        anchor=Decimal(str(e["take_h1_close_mid"]))
        hi=Decimal(str(max(p_hi))); lo=Decimal(str(min(p_lo)))
        if e["side"]=="HIGH":
            r=max(ZERO,anchor-lo); x=max(ZERO,hi-anchor)
        elif e["side"]=="LOW":
            r=max(ZERO,hi-anchor); x=max(ZERO,anchor-lo)
        else:raise RuntimeError("side")
        rein.append(r); ext.append(x)
        gaps=[p_ts[i+1]-p_ts[i] for i in range(len(p_ts)-1)]
        source_paths=[
            f["relative_path"] for f in m["files"]
            if int(f["last_minute_ms_utc"])>start and int(f["first_minute_ms_utc"])<end
        ]
        if not source_paths:raise RuntimeError("source binding")
        diag.append({
            "event_id":e["event_id"],
            "path_observation_count":len(p_ts),
            "path_first_observed_minute_ms_utc":p_ts[0],
            "path_last_observed_minute_ms_utc":p_ts[-1],
            "internal_gap_count_gt60s":sum(g>60000 for g in gaps),
            "max_observed_internal_gap_ms":max(gaps) if gaps else 0,
            "source_file_paths":source_paths,
        })

    obj={
        "schema":"ATDS_BEPD_07B_INDEPENDENT_REFERENCE_V0_1",
        "implementation":"INDEPENDENT_NO_IMPORT_FROM_CANONICAL_RUNNER",
        "quantile_method":QUANTILE_METHOD,
        "ecdf":ECDF_METHOD,
        "metrics":{
            "MAX_REINTEGRATIVE_EXCURSION":surface(rein),
            "MAX_EXTERNAL_EXCURSION":surface(ext),
        },
        "path_diagnostics_digest":canonical_sha(diag),
        "event_level_path_diagnostics_persisted":False,
    }
    Path(args.output).write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")


if __name__=="__main__":
    main()
