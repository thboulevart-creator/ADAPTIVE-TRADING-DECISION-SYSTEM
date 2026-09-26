#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import stat
import tempfile
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from zoneinfo import ZoneInfo

EXPECTED_AP0_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
EXPECTED_AP2_SHA256 = "4e3c79a5b9c8131f62a8fb7f205712d8a5c4301ff01b7fd3ce7226d8799d9c9f"
EXPECTED_AP3_SHA256 = "caa2d02942d5cbd05bcfadd0dedfabde000e4e941cdf4aa4b0433801f76f42ef"
EXPECTED_AP4_SHA256 = "c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad"
EXPECTED_AP5_SHA256 = "21dc09b082e32f20543c6206c276c24389b7b61fd930fbe2d1783adabaca4406"
EXPECTED_AP3_REPO_PATH = Path("reports/program/evidence/2026-09-25-AP3-EXPANSION-COMPRESSION.json")
EXPECTED_AP4_REPO_PATH = Path("reports/program/evidence/2026-09-25-AP4-PRICE-STRUCTURE.json")
EXPECTED_AP5_REPO_PATH = Path("reports/program/evidence/2026-09-25-AP5-MICROSTRUCTURE-PRICE-CORE.json")
EXPECTED_AP0_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
EXPECTED_FILES = 61
EXPECTED_MINUTES = 1_709_180
EXPECTED_SOURCE_TICKS = 376_003_618
EXPECTED_SEGMENTS = 1_606
TOL = 1e-9
MAX_OUTPUT_BYTES = 64 * 1024 * 1024
NY = ZoneInfo("America/New_York")
COMPLETE_YEARS = (2022, 2023, 2024, 2025)
ALL_YEARS = (2021, 2022, 2023, 2024, 2025, 2026)
PCTS = (10, 50, 90, 99)
DECILES = (10,20,30,40,50,60,70,80,90)

SCOPE = {
    "strategy_agnostic": True,
    "signals_calculated": False,
    "pnl_calculated": False,
    "optimization": False,
    "source_volume_used": False,
    "future_labels_used": False,
    "causal_deployable": False,
    "stability_measured": True,
    "stability_threshold_applied": False,
}

REQUIRED_SCHEMA = [
    ("minute_start_ms_utc", "int64"),
    ("first_tick_ms", "int64"),
    ("last_tick_ms", "int64"),
    ("tick_count", "int64"),
    ("segment_id", "int64"),
    ("segment_start", "bool"),
    ("gap_before_ms", "int64"),
    ("mid_open", "double"),
    ("mid_high", "double"),
    ("mid_low", "double"),
    ("mid_close", "double"),
    ("spread_mean", "double"),
    ("spread_min", "double"),
    ("spread_max", "double"),
]
READ_COLUMNS = [
    "minute_start_ms_utc", "tick_count", "segment_id",
    "mid_open", "mid_high", "mid_low", "mid_close", "spread_mean",
]

EXPECTED_GLOBAL = {
    "minute_range_bps": (EXPECTED_MINUTES, 4.033115022615127),
    "abs_log_return_1m_bps": (1_707_574, 2.130371613870453),
    "realized_vol_15m_bps": (1_686_423, 10.478525943077567),
    "realized_vol_60m_bps": (1_620_195, 21.63083566473441),
    "efficiency_15m": (1_686_423, 0.25740927472902353),
    "efficiency_60m": (1_620_195, 0.13080767215518072),
}
EXPECTED_PERSISTENCE = 0.4933796682202942
EXPECTED_SPREAD_TICK_WEIGHTED = 2.1395040593705223
EXPECTED_TICK_MEAN = 219.99064931721645


def sha256_path(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def is_within(child: Path, parent: Path) -> bool:
    try:
        c = os.path.normcase(str(child.resolve(strict=False)))
        p = os.path.normcase(str(parent.resolve(strict=False)))
        return os.path.commonpath([c, p]) == p
    except ValueError:
        return False


def is_reparse_or_symlink(path: Path) -> bool:
    st = path.lstat()
    if stat.S_ISLNK(st.st_mode):
        return True
    attrs = getattr(st, "st_file_attributes", 0)
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(attrs & reparse)


def path_chain_has_reparse_or_symlink(path: Path) -> bool:
    absolute = path.absolute()
    parts = absolute.parts
    if not parts:
        return False
    cur = Path(parts[0])
    for part in parts[1:]:
        cur = cur / part
        if os.path.lexists(cur):
            if is_reparse_or_symlink(cur):
                return True
        else:
            break
    return False


def resolve_manifest_member(root: Path, rel: str) -> Path:
    raw = root / Path(rel)
    if path_chain_has_reparse_or_symlink(raw):
        raise RuntimeError(f"AP0 manifest member path contains reparse/symlink: {rel}")
    p = raw.resolve(strict=False)
    if not is_within(p, root) or not p.is_file() or is_reparse_or_symlink(p):
        raise RuntimeError(f"invalid AP0 file path: {rel}")
    return p


def resolve_bound_evidence(repo_root: Path, rel: Path, expected_sha: str) -> Path:
    raw = repo_root / rel
    if path_chain_has_reparse_or_symlink(raw):
        raise RuntimeError(f"evidence path contains reparse/symlink: {rel}")
    p = raw.resolve(strict=False)
    if not is_within(p, repo_root) or not p.is_file() or is_reparse_or_symlink(p):
        raise RuntimeError(f"invalid evidence path: {rel}")
    if sha256_path(p) != expected_sha:
        raise RuntimeError(f"evidence SHA mismatch: {rel}")
    return p


def validate_upstream_bindings(ap3: dict, ap4: dict, ap5: dict) -> None:
    if ap3.get("schema") != "ATDS_AP3_EXPANSION_COMPRESSION_V0_1" or ap3.get("status") != "AP3_COMPLETE":
        raise RuntimeError("AP3 schema/status mismatch")
    if ap4.get("schema") != "ATDS_AP4_PRICE_STRUCTURE_V0_1" or ap4.get("status") != "AP4_COMPLETE":
        raise RuntimeError("AP4 schema/status mismatch")
    if ap5.get("schema") != "ATDS_AP5_MICROSTRUCTURE_PRICE_CORE_V0_1" or ap5.get("status") != "AP5_COMPLETE":
        raise RuntimeError("AP5 schema/status mismatch")
    if (ap3.get("binding") or {}).get("ap2_sha256") != EXPECTED_AP2_SHA256:
        raise RuntimeError("AP3->AP2 binding mismatch")
    if (ap4.get("binding") or {}).get("ap3_sha256") != EXPECTED_AP3_SHA256:
        raise RuntimeError("AP4->AP3 binding mismatch")
    if (ap5.get("binding") or {}).get("ap4_sha256") != EXPECTED_AP4_SHA256:
        raise RuntimeError("AP5->AP4 binding mismatch")
    for obj,label in ((ap3,"AP3"),(ap4,"AP4"),(ap5,"AP5")):
        if (obj.get("binding") or {}).get("ap0_manifest_sha256") != EXPECTED_AP0_MANIFEST_SHA256:
            raise RuntimeError(f"{label}->AP0 binding mismatch")


def write_json_exclusive(path: Path, payload: dict) -> None:
    raw=(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2)+"\n").encode("utf-8")
    if len(raw)>MAX_OUTPUT_BYTES:
        raise RuntimeError("AP6 JSON exceeds output bound")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as f:
        f.write(raw)


def distribution(values, percentiles=PCTS) -> dict:
    import numpy as np
    x=np.asarray(values,dtype=np.float64)
    x=x[np.isfinite(x)]
    if x.size==0:
        out={"count":0,"mean":None}
        out.update({f"p{q}":None for q in percentiles})
        return out
    out={"count":int(x.size),"mean":float(np.mean(x))}
    for q in percentiles:
        out[f"p{q}"]=float(np.percentile(x,q,method="linear"))
    return out


def tick_weighted_mean(spread_mean, tick_count):
    import numpy as np
    sm=np.asarray(spread_mean,dtype=np.float64); tc=np.asarray(tick_count,dtype=np.int64)
    if sm.size==0 or sm.size!=tc.size or np.any(~np.isfinite(sm)) or np.any(tc<=0):
        raise ValueError("invalid weighted mean input")
    return float(np.sum(sm*tc,dtype=np.float64)/np.sum(tc,dtype=np.int64))


def signed_return_1m_bps(minute, segment, close):
    import numpy as np
    minute=np.asarray(minute,dtype=np.int64); segment=np.asarray(segment,dtype=np.int64); close=np.asarray(close,dtype=np.float64)
    n=minute.size
    out=np.full(n,np.nan,dtype=np.float64); valid=np.zeros(n,dtype=bool)
    if n>1:
        ok=(segment[1:]==segment[:-1]) & ((minute[1:]-minute[:-1])==60_000)
        idx=np.flatnonzero(ok)+1
        out[idx]=np.log(close[1:][ok]/close[:-1][ok])*10000.0
        valid[idx]=True
    return out,valid


def rolling_realized_vol_bps(signed_bps, valid, minute, segment, h):
    import numpy as np
    r=np.asarray(signed_bps,dtype=np.float64)/10000.0
    valid=np.asarray(valid,dtype=bool); minute=np.asarray(minute,dtype=np.int64); segment=np.asarray(segment,dtype=np.int64)
    n=len(r); out=np.full(n,np.nan,dtype=np.float64)
    sq=np.where(valid,r*r,0.0); bad=(~valid).astype(np.int64)
    cs_sq=np.concatenate(([0.0],np.cumsum(sq,dtype=np.float64)))
    cs_bad=np.concatenate(([0],np.cumsum(bad,dtype=np.int64)))
    endpoints=np.arange(h,n,dtype=np.int64); starts=endpoints-h+1
    invalid=cs_bad[endpoints+1]-cs_bad[starts]
    sums=cs_sq[endpoints+1]-cs_sq[starts]
    boundary=(segment[endpoints]==segment[endpoints-h]) & ((minute[endpoints]-minute[endpoints-h])==h*60_000)
    ok=(invalid==0)&boundary
    out[endpoints[ok]]=np.sqrt(sums[ok])*10000.0
    return out


def window_valid(valid,h):
    import numpy as np
    valid=np.asarray(valid,dtype=bool); n=len(valid)
    result=np.zeros(n,dtype=bool)
    bad=np.concatenate(([0],np.cumsum(~valid,dtype=np.int64)))
    t=np.arange(h,n,dtype=np.int64)
    result[t]=(bad[t+1]-bad[t-h+1])==0
    return result


def efficiency_array(signed_bps,valid,h):
    import numpy as np
    r=np.asarray(signed_bps,dtype=np.float64); valid=np.asarray(valid,dtype=bool)
    ok=window_valid(valid,h); clean=np.where(valid,r,0.0)
    cs=np.concatenate(([0.0],np.cumsum(clean))); ca=np.concatenate(([0.0],np.cumsum(np.abs(clean))))
    idx=np.flatnonzero(ok); signed=cs[idx+1]-cs[idx-h+1]; travel=ca[idx+1]-ca[idx-h+1]
    nz=np.concatenate(([0],np.cumsum(valid & (r!=0),dtype=np.int64)))
    nonflat=(nz[idx+1]-nz[idx-h+1])>0
    out=np.full(len(r),np.nan,dtype=np.float64)
    out[idx[nonflat]]=np.abs(signed[nonflat])/travel[nonflat]
    out[idx[nonflat]]=np.clip(out[idx[nonflat]],0.0,1.0)
    return out


def persistence_summary(signed_bps,valid,bucket=None):
    import numpy as np
    r=np.asarray(signed_bps,dtype=np.float64); valid=np.asarray(valid,dtype=bool)
    s=np.sign(np.nan_to_num(r)).astype(np.int8)
    eligible=valid[1:] & valid[:-1]
    if bucket is not None:
        b=np.asarray(bucket,dtype=bool); eligible &= b[1:] & b[:-1]
    matrix=np.zeros((3,3),dtype=np.int64)
    np.add.at(matrix,(s[:-1][eligible]+1,s[1:][eligible]+1),1)
    same=int(matrix[0,0]+matrix[2,2]); rev=int(matrix[0,2]+matrix[2,0]); den=same+rev
    return {"eligible_pairs":int(matrix.sum()),"nonzero_pairs":den,"persistence_rate":same/den if den else None,"reversal_rate":rev/den if den else None}


def time_dimensions(minute_ms):
    import numpy as np
    minute_ms=np.asarray(minute_ms,dtype=np.int64)
    hour_code=minute_ms//3_600_000
    unique,inverse=np.unique(hour_code,return_inverse=True)
    ny_hour=np.empty(unique.size,dtype=np.int16); ny_weekday=np.empty(unique.size,dtype=np.int16); ny_month=np.empty(unique.size,dtype=np.int16)
    utc_year=np.empty(unique.size,dtype=np.int16); utc_quarter=np.empty(unique.size,dtype=np.int32)
    for i,code in enumerate(unique):
        dt=datetime.fromtimestamp(int(code)*3600,tz=timezone.utc); ny=dt.astimezone(NY)
        ny_hour[i]=ny.hour
        ny_weekday[i]=ny.weekday()
        ny_month[i]=ny.month
        utc_year[i]=dt.year
        utc_quarter[i]=dt.year*10+((dt.month-1)//3+1)
    return ny_hour[inverse],ny_weekday[inverse],ny_month[inverse],utc_year[inverse],utc_quarter[inverse]


def reference_mask(utc_year):
    import numpy as np
    y=np.asarray(utc_year,dtype=np.int16)
    return (y>=2022)&(y<=2025)


def cdf_at_thresholds(values,thresholds):
    import numpy as np
    x=np.asarray(values,dtype=np.float64); x=x[np.isfinite(x)]; t=np.asarray(thresholds,dtype=np.float64)
    if x.size==0: return [None]*len(t)
    sx=np.sort(x)
    return [float(np.searchsorted(sx,v,side="right")/sx.size) for v in t]


def cdf_distance(values,thresholds,reference_cdf):
    import numpy as np
    x=np.asarray(values,dtype=np.float64); x=x[np.isfinite(x)]
    if x.size==0: return None
    c=np.asarray(cdf_at_thresholds(x,thresholds),dtype=np.float64); r=np.asarray(reference_cdf,dtype=np.float64)
    return float(np.max(np.abs(c-r)))


def average_ranks(values):
    import numpy as np
    x=np.asarray(values,dtype=np.float64); n=x.size
    order=np.argsort(x,kind="mergesort"); sx=x[order]; ranks=np.empty(n,dtype=np.float64)
    i=0
    while i<n:
        j=i+1
        while j<n and sx[j]==sx[i]: j+=1
        rank=((i+1)+j)/2.0
        ranks[order[i:j]]=rank
        i=j
    return ranks


def pearson(x,y):
    import numpy as np
    a=np.asarray(x,dtype=np.float64); b=np.asarray(y,dtype=np.float64)
    if a.size!=b.size or a.size<2: return None
    ac=a-a.mean(); bc=b-b.mean(); den=math.sqrt(float(np.dot(ac,ac))*float(np.dot(bc,bc)))
    return None if den==0 else float(np.dot(ac,bc)/den)


def spearman(x,y):
    return pearson(average_ranks(x),average_ranks(y))


def population_cv(values):
    import numpy as np
    x=np.asarray(values,dtype=np.float64); x=x[np.isfinite(x)]
    if x.size==0: return None
    m=float(np.mean(x))
    return None if m==0 else float(np.std(x,ddof=0)/m)


def temporal_bucket(code,label,mask,metrics,tick,spread):
    import numpy as np
    mask=np.asarray(mask,dtype=bool); idx=np.flatnonzero(mask)
    out={"code":code,"label":label,"minute_count":int(idx.size),"source_tick_count":int(np.sum(tick[idx],dtype=np.int64))}
    out["metrics"]={name:distribution(values[idx]) for name,values in metrics.items()}
    out["spread_tick_weighted_mean"]=tick_weighted_mean(spread[idx],tick[idx]) if idx.size else None
    return out


def assert_partition_conservation(buckets,metrics,expected_minutes,expected_ticks):
    if sum(b["minute_count"] for b in buckets)!=expected_minutes: raise RuntimeError("minute partition conservation failed")
    if sum(b["source_tick_count"] for b in buckets)!=expected_ticks: raise RuntimeError("tick partition conservation failed")
    for name,values in metrics.items():
        import numpy as np
        expected=int(np.count_nonzero(np.isfinite(values)))
        got=sum(b["metrics"][name]["count"] for b in buckets)
        if got!=expected: raise RuntimeError(f"metric partition conservation failed: {name}")


def seasonal_rank_stability(values,category,category_codes,utc_year):
    import numpy as np
    values=np.asarray(values,dtype=np.float64); category=np.asarray(category); utc_year=np.asarray(utc_year)
    codes=np.asarray(list(category_codes)); yearly={}
    for y in COMPLETE_YEARS:
        mask=(utc_year==y)&np.isfinite(values)
        cats=category[mask]; vals=values[mask]
        positions=np.searchsorted(codes,cats)
        if np.any(positions<0) or np.any(positions>=codes.size) or np.any(codes[positions]!=cats):
            raise RuntimeError("seasonal category outside preregistered codes")
        counts=np.bincount(positions,minlength=codes.size)
        sums=np.bincount(positions,weights=vals,minlength=codes.size)
        yearly[y]=[float(sums[i]/counts[i]) if counts[i] else None for i in range(codes.size)]
    cors=[]
    for a,b in combinations(COMPLETE_YEARS,2):
        pairs=[(yearly[a][i],yearly[b][i]) for i in range(codes.size) if yearly[a][i] is not None and yearly[b][i] is not None]
        if len(pairs)>=3:
            r=spearman([p[0] for p in pairs],[p[1] for p in pairs])
            if r is not None: cors.append(r)
    cvs=[]; eligible=0
    for i,c in enumerate(codes):
        xs=[yearly[y][i] for y in COMPLETE_YEARS]
        if all(v is not None for v in xs):
            eligible+=1; cv=population_cv(xs)
            if cv is not None: cvs.append(cv)
    return {
        "yearly_category_means":{str(y):{str(int(c)):yearly[y][i] for i,c in enumerate(codes)} for y in COMPLETE_YEARS},
        "pair_count":len(cors),"minimum_spearman":min(cors) if cors else None,"mean_spearman":float(np.mean(cors)) if cors else None,"median_spearman":float(np.median(cors)) if cors else None,
        "eligible_category_count":eligible,"median_category_cv":float(np.median(cvs)) if cvs else None,"maximum_category_cv":max(cvs) if cvs else None,
    }


def validate_arrays(minute,tick,seg,op,hi,lo,cl,sm,previous=None):
    import numpy as np
    arr=[minute,tick,seg,op,hi,lo,cl,sm]; n=len(minute)
    if n==0 or any(len(x)!=n for x in arr): raise RuntimeError("decoded row mismatch/empty")
    if np.any(np.diff(minute)<=0): raise RuntimeError("minute order violation")
    if previous is None:
        if int(seg[0])!=0: raise RuntimeError("first segment must be zero")
    else:
        if int(minute[0])<=previous[0]: raise RuntimeError("global minute order violation")
        if int(seg[0])-previous[1] not in (0,1): raise RuntimeError("segment boundary violation")
    if np.any(tick<=0): raise RuntimeError("nonpositive tick_count")
    if np.any(np.diff(seg)<0) or np.any(np.diff(seg)>1): raise RuntimeError("segment jump violation")
    for x in (op,hi,lo,cl,sm):
        if np.any(~np.isfinite(x)): raise RuntimeError("nonfinite numeric field")
    if np.any(op<=0)|np.any(hi<=0)|np.any(lo<=0)|np.any(cl<=0): raise RuntimeError("nonpositive OHLC")
    if np.any(lo>op)|np.any(lo>cl)|np.any(hi<op)|np.any(hi<cl): raise RuntimeError("OHLC invariant violation")
    if np.any(sm<=0): raise RuntimeError("nonpositive spread_mean")


def main():
    ap=argparse.ArgumentParser(description="AP6 strategy-agnostic seasonality/stability profile")
    ap.add_argument("--repo-root",required=True); ap.add_argument("--ap0-root",required=True); ap.add_argument("--ap0-manifest",required=True)
    ap.add_argument("--output",default=str(Path(tempfile.gettempdir())/"ATDS-AP6-SEASONALITY-STABILITY.json"))
    args=ap.parse_args()
    repo_raw=Path(args.repo_root).expanduser(); root_raw=Path(args.ap0_root).expanduser(); manifest_raw=Path(args.ap0_manifest).expanduser(); output_raw=Path(args.output).expanduser()
    if os.path.lexists(output_raw): print("BLOCKED_AP6_OUTPUT_EXISTS"); print(output_raw); return 2
    for raw,label in ((repo_raw,"repo-root"),(root_raw,"AP0 root"),(manifest_raw,"AP0 manifest"),(output_raw.parent,"output parent")):
        if path_chain_has_reparse_or_symlink(raw): print("BLOCKED_AP6_REPARSE"); print(f"{label}: {raw}"); return 2
    repo_root=repo_raw.resolve(strict=False); root=root_raw.resolve(strict=False); manifest_path=manifest_raw.resolve(strict=False); output=output_raw.resolve(strict=False)
    def block(code,reason):
        payload={"schema":"ATDS_AP6_BLOCKED_V0_1","status":code,"reason":reason}
        try:
            if not output.exists(): write_json_exclusive(output,payload)
        except Exception: pass
        print(code); print(reason); print(f"Report: {output}"); return 2
    if not repo_root.is_dir() or not root.is_dir() or not manifest_path.is_file(): return block("BLOCKED_AP6_INPUT_NOT_FOUND","input missing")
    if output==root or is_within(output,root): return block("BLOCKED_AP6_OUTPUT_INSIDE_INPUT",str(output))
    if sha256_path(manifest_path)!=EXPECTED_AP0_MANIFEST_SHA256: return block("BLOCKED_AP6_AP0_MANIFEST_SHA","manifest SHA mismatch")
    try:
        p3=resolve_bound_evidence(repo_root,EXPECTED_AP3_REPO_PATH,EXPECTED_AP3_SHA256); p4=resolve_bound_evidence(repo_root,EXPECTED_AP4_REPO_PATH,EXPECTED_AP4_SHA256); p5=resolve_bound_evidence(repo_root,EXPECTED_AP5_REPO_PATH,EXPECTED_AP5_SHA256)
        ap3=json.loads(p3.read_text(encoding="utf-8")); ap4=json.loads(p4.read_text(encoding="utf-8")); ap5=json.loads(p5.read_text(encoding="utf-8")); validate_upstream_bindings(ap3,ap4,ap5)
        manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("status")!="AP0_COMPLETE" or manifest.get("output_identity")!=EXPECTED_AP0_IDENTITY: raise RuntimeError("AP0 identity/status mismatch")
        files=manifest.get("files"); cov=manifest.get("coverage") or {}
        if not isinstance(files,list) or len(files)!=EXPECTED_FILES: raise RuntimeError("AP0 file count mismatch")
        if cov.get("minute_rows_written")!=EXPECTED_MINUTES or cov.get("source_ticks_read")!=EXPECTED_SOURCE_TICKS or cov.get("segments")!=EXPECTED_SEGMENTS or cov.get("segment_start_rows")!=EXPECTED_SEGMENTS: raise RuntimeError("AP0 coverage mismatch")
        import numpy as np, pyarrow as pa, pyarrow.parquet as pq
        chunks={k:[] for k in ("minute","tick","seg","op","hi","lo","cl","sm")}; rows=0; ticks=0; previous=None
        for rec in files:
            rel=rec["relative_path"]; p=resolve_manifest_member(root,rel)
            if int(p.stat().st_size)!=int(rec["size_bytes"]) or sha256_path(p)!=rec["sha256"]: raise RuntimeError(f"AP0 identity mismatch: {rel}")
            pf=pq.ParquetFile(p)
            if int(pf.metadata.num_rows)!=int(rec["rows"]): raise RuntimeError(f"AP0 rows mismatch: {rel}")
            if [(f.name,str(f.type)) for f in pf.schema_arrow]!=REQUIRED_SCHEMA: raise RuntimeError(f"AP0 schema mismatch: {rel}")
            meta=pf.schema_arrow.metadata or {}
            if meta.get(b"dataset_identity")!=EXPECTED_AP0_IDENTITY.encode() or meta.get(b"volumes_used")!=b"false" or meta.get(b"mid_semantics")!=b"descriptive_only_not_execution_price": raise RuntimeError(f"AP0 metadata mismatch: {rel}")
            table=pf.read(columns=READ_COLUMNS,use_threads=False)
            if table.column_names!=READ_COLUMNS: raise RuntimeError("AP6 column scope violation")
            vals={
                "minute":table["minute_start_ms_utc"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64,copy=False),
                "tick":table["tick_count"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64,copy=False),
                "seg":table["segment_id"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64,copy=False),
                "op":table["mid_open"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64,copy=False),
                "hi":table["mid_high"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64,copy=False),
                "lo":table["mid_low"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64,copy=False),
                "cl":table["mid_close"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64,copy=False),
                "sm":table["spread_mean"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64,copy=False),
            }
            validate_arrays(**vals,previous=previous); previous=(int(vals["minute"][-1]),int(vals["seg"][-1])); rows+=len(vals["minute"]); ticks+=int(np.sum(vals["tick"],dtype=np.int64))
            for k,v in vals.items(): chunks[k].append(v.copy())
            if sha256_path(p)!=rec["sha256"]: raise RuntimeError(f"AP0 changed during AP6: {rel}")
        if rows!=EXPECTED_MINUTES or ticks!=EXPECTED_SOURCE_TICKS: raise RuntimeError("AP6 reconstructed coverage mismatch")
        a={k:np.concatenate(v) for k,v in chunks.items()}
        if int(a["seg"][0])!=0 or int(a["seg"][-1])!=EXPECTED_SEGMENTS-1: raise RuntimeError("AP6 segment coverage mismatch")
        signed,valid=signed_return_1m_bps(a["minute"],a["seg"],a["cl"])
        metrics={
            "minute_range_bps":(a["hi"]-a["lo"])/a["op"]*10000.0,
            "abs_log_return_1m_bps":np.abs(signed),
            "realized_vol_15m_bps":rolling_realized_vol_bps(signed,valid,a["minute"],a["seg"],15),
            "realized_vol_60m_bps":rolling_realized_vol_bps(signed,valid,a["minute"],a["seg"],60),
            "efficiency_15m":efficiency_array(signed,valid,15),
            "efficiency_60m":efficiency_array(signed,valid,60),
            "spread_mean":a["sm"].astype(np.float64),
            "tick_count":a["tick"].astype(np.float64),
        }
        global_summary={name:distribution(v) for name,v in metrics.items()}
        for name,(count,mean) in EXPECTED_GLOBAL.items():
            if global_summary[name]["count"]!=count or abs(global_summary[name]["mean"]-mean)>TOL: raise RuntimeError(f"global reconciliation failed: {name}")
        ps=persistence_summary(signed,valid)
        if abs(ps["persistence_rate"]-EXPECTED_PERSISTENCE)>TOL: raise RuntimeError("persistence reconciliation failed")
        if abs(tick_weighted_mean(a["sm"],a["tick"])-EXPECTED_SPREAD_TICK_WEIGHTED)>TOL: raise RuntimeError("spread reconciliation failed")
        if abs(float(np.mean(a["tick"]))-EXPECTED_TICK_MEAN)>TOL: raise RuntimeError("tick mean reconciliation failed")
        nyh,nyw,nym,uy,uq=time_dimensions(a["minute"])
        specs=[("new_york_hour",range(24),nyh,lambda c:f"{c:02d}:00 America/New_York"),("new_york_weekday",range(7),nyw,lambda c:["MON","TUE","WED","THU","FRI","SAT","SUN"][c]),("new_york_month",range(1,13),nym,lambda c:f"{c:02d}"),("utc_year",ALL_YEARS,uy,lambda c:f"{c}"),("utc_quarter",sorted(set(map(int,uq.tolist()))),uq,lambda c:f"{c//10}-Q{c%10}")]
        dim_payload={}
        for name,codes,arr,labeler in specs:
            buckets=[]
            for c in codes:
                b=temporal_bucket(int(c),labeler(int(c)),arr==c,metrics,a["tick"],a["sm"])
                if name=="utc_year": b["partial_period"]=int(c) in (2021,2026)
                if name=="utc_quarter": b["partial_period"]=int(c) in (20212,20262)
                buckets.append(b)
            assert_partition_conservation(buckets,metrics,EXPECTED_MINUTES,EXPECTED_SOURCE_TICKS)
            dim_payload[name]=buckets
        stability={}
        year_buckets=dim_payload["utc_year"]; quarter_buckets=dim_payload["utc_quarter"]
        for name,v in metrics.items():
            ref=reference_mask(uy)&np.isfinite(v); rv=np.asarray(v)[ref]; thresholds=np.percentile(rv,DECILES,method="linear"); rcdf=cdf_at_thresholds(rv,thresholds)
            byyear=[]
            for y in ALL_YEARS:
                m=uy==y; byyear.append({"code":y,"count":int(np.count_nonzero(m&np.isfinite(v))),"decile_cdf_distance":cdf_distance(np.asarray(v)[m],thresholds,rcdf)})
            byq=[]
            for b in quarter_buckets:
                q=b["code"]; m=uq==q; byq.append({"code":q,"label":b["label"],"count":int(np.count_nonzero(m&np.isfinite(v))),"decile_cdf_distance":cdf_distance(np.asarray(v)[m],thresholds,rcdf)})
            stability[name]={"reference_years":list(COMPLETE_YEARS),"reference_count":int(rv.size),"reference_decile_thresholds":thresholds.tolist(),"reference_cdf":rcdf,"complete_year_cv":{
                "mean_cv":population_cv([b["metrics"][name]["mean"] for b in year_buckets if b["code"] in COMPLETE_YEARS]),
                "p50_cv":population_cv([b["metrics"][name]["p50"] for b in year_buckets if b["code"] in COMPLETE_YEARS]),
                "p90_cv":population_cv([b["metrics"][name]["p90"] for b in year_buckets if b["code"] in COMPLETE_YEARS]),
            },"by_year":byyear,"by_quarter":byq}
        seasonal={}
        for name,v in metrics.items():
            seasonal[name]={
                "new_york_hour":seasonal_rank_stability(v,nyh,list(range(24)),uy),
                "new_york_weekday":seasonal_rank_stability(v,nyw,list(range(7)),uy),
                "new_york_month":seasonal_rank_stability(v,nym,list(range(1,13)),uy),
            }
        struct={"global":ps,"utc_year":[],"utc_quarter":[]}
        for y in ALL_YEARS: struct["utc_year"].append({"code":y,**persistence_summary(signed,valid,uy==y)})
        for b in quarter_buckets: struct["utc_quarter"].append({"code":b["code"],"label":b["label"],**persistence_summary(signed,valid,uq==b["code"])})
        payload={
            "schema":"ATDS_AP6_SEASONALITY_STABILITY_V0_1","status":"AP6_COMPLETE","input_identity":EXPECTED_AP0_IDENTITY,
            "binding":{"ap0_manifest_sha256":EXPECTED_AP0_MANIFEST_SHA256,"ap2_sha256":EXPECTED_AP2_SHA256,"ap3_sha256":EXPECTED_AP3_SHA256,"ap4_sha256":EXPECTED_AP4_SHA256,"ap5_sha256":EXPECTED_AP5_SHA256,"ap0_files_rehashed":EXPECTED_FILES},
            "scope":SCOPE,"coverage":{"minute_rows":rows,"source_ticks_accounted":ticks,"segments":EXPECTED_SEGMENTS},
            "metric_contract":{"complete_year_reference":list(COMPLETE_YEARS),"partial_years":[2021,2026],"distribution_distance":"max absolute empirical CDF delta at frozen reference p10..p90 thresholds","seasonal_rank":"pairwise Spearman of complete-year category means; average ranks for ties","stability_threshold":"none","window_attribution":"endpoint minute"},
            "global":global_summary,"spread_tick_weighted_mean":tick_weighted_mean(a["sm"],a["tick"]),"directional_structure":struct,
            "temporal_dimensions":dim_payload,"distribution_stability":stability,"seasonal_pattern_stability":seasonal,
            "runtime":{"numpy_version":np.__version__,"pyarrow_version":pa.__version__},
        }
        write_json_exclusive(output,payload)
        print("AP6_COMPLETE"); print(f"Minute rows: {rows}"); print(f"Source ticks accounted: {ticks}"); print(f"Reference years: {COMPLETE_YEARS}"); print(f"Report: {output}"); return 0
    except Exception as exc:
        return block("BLOCKED_AP6_RUNTIME",str(exc))

if __name__=="__main__":
    raise SystemExit(main())
