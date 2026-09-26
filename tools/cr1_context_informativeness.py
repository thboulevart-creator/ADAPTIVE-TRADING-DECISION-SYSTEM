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
from pathlib import Path
from zoneinfo import ZoneInfo

EXPECTED_AP0_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
EXPECTED_CONTEXT_SHA256 = "3c507795c996e571152d4877a594abb889e4a8a017130332a166d5dda84af866"
EXPECTED_REGISTRY_SHA256 = "0320e51fb4f53fbed2c2e6a51d41c83e2b8ddd7afe59c6fca91a0a34eaf7f8f5"
EXPECTED_CORE_GIT_BLOB = "eee2c1b4c27029f05d6ea246ae95cf30c17f0d5e"
EXPECTED_CONTEXT_REPO_PATH = "reports/program/evidence/2026-09-26-CR1-CONTEXT-V0.1.json"
EXPECTED_REGISTRY_REPO_PATH = "reports/program/evidence/2026-09-26-CONTEXT-REGIME-HYPOTHESIS-REGISTRY-V0.1.json"
EXPECTED_CORE_REPO_PATH = "reports/program/evidence/2026-09-26-ASSET-BEHAVIORAL-PROFILE-CORE-V0.1.json"
EXPECTED_CORE_BINDING = {
    "ap0_manifest_sha256": "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce",
    "ap1_sha256": "db8963bb1bd1fa5b76a9a435fcb9b2d24781f92df0c5e53b6664bafe6235076b",
    "ap2_sha256": "4e3c79a5b9c8131f62a8fb7f205712d8a5c4301ff01b7fd3ce7226d8799d9c9f",
    "ap3_sha256": "caa2d02942d5cbd05bcfadd0dedfabde000e4e941cdf4aa4b0433801f76f42ef",
    "ap4_sha256": "c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad",
    "ap5_sha256": "21dc09b082e32f20543c6206c276c24389b7b61fd930fbe2d1783adabaca4406",
    "ap6_sha256": "f2cfa2c8c43f70519904c375452027f79415890be20a61c4c0452c06127e17fd",
}
EXPECTED_CONTEXT_ID = "CTX-d0501ec820062bfe373f1f4b94de4e191ca2c7e05bbe788b3d5d963750158cbf"
EXPECTED_REGISTRY_BLOB = "490039cecf5a02ac7e553f8f7e47f6d4baedb584"
EXPECTED_CORE_COMMIT = "23ff3c93356ce93c2a1dbe74ec192d948a78050e"
EXPECTED_AP0_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
EXPECTED_FILES = 61
EXPECTED_MINUTES = 1_709_180
EXPECTED_SOURCE_TICKS = 376_003_618
EXPECTED_SEGMENTS = 1_606
MAX_OUTPUT_BYTES = 64 * 1024 * 1024
NY = ZoneInfo("America/New_York")
ALPHA = 1.0
TARGET_CLASSES = 5
SPARSE_MIN_TEST = 100
PRIMARY_FOLDS = ("F1", "F2", "F3")
ALL_FOLDS = ("F1", "F2", "F3", "D2026")

EXPECTED_HYPOTHESES = (
    "CR-H01-NY-HOUR",
    "CR-H02-WEEKDAY",
    "CR-H03-ABS-VOL",
    "CR-H04-REL-VOL",
    "CR-H05-SPREAD",
    "CR-H06-TICK-DENSITY",
    "CR-H07-GAP-REOPEN",
    "CR-H08-EFFICIENCY",
)

SCOPE = {
    "epistemic_class": "N0_EXPLORATORY",
    "pristine_oos_claim": False,
    "strategy_agnostic": True,
    "direction_target_used": False,
    "signals_calculated": False,
    "trades_calculated": False,
    "pnl_calculated": False,
    "optimization": False,
    "feature_search": False,
    "threshold_search": False,
    "interaction_search": False,
    "winner_selection": False,
    "regime_labels_instantiated": False,
    "mt5_used": False,
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
READ_COLUMNS = ["minute_start_ms_utc", "tick_count", "segment_id", "mid_close", "spread_mean"]

FOLD_BOUNDS = {
    "F1": (None, 2022, 2023),
    "F2": (None, 2023, 2024),
    "F3": (None, 2024, 2025),
    "D2026": (None, 2025, 2026),
}


def sha256_path(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def git_blob_sha1_path(path: Path) -> str:
    raw = path.read_bytes()
    h = hashlib.sha1()
    h.update(f"blob {len(raw)}\0".encode("ascii"))
    h.update(raw)
    return h.hexdigest()


def stable_context_id(value: dict) -> str:
    fields = (
        "dataset_id", "dataset_version", "content_hash", "instrument",
        "granularity", "timezone_storage", "configuration_version",
    )
    payload = {k: value[k] for k in fields}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "CTX-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def validate_context_payload(context: dict) -> None:
    required = {
        "dataset_id": EXPECTED_AP0_IDENTITY,
        "dataset_version": "V0.1",
        "content_hash": EXPECTED_AP0_MANIFEST_SHA256,
        "instrument": "USTECH",
        "granularity": "1-minute",
        "timezone_storage": "UTC",
        "configuration_version": "CR1-CONTEXT-INFORMATIVENESS-V0.1",
    }
    if context.get("schema") != "ATDS_CR1_CONTEXT_V0_1":
        raise RuntimeError("CR1 Context schema mismatch")
    for k, expected in required.items():
        if context.get(k) != expected:
            raise RuntimeError(f"CR1 Context identity field mismatch: {k}")
    if stable_context_id(context) != context.get("context_id") or context.get("context_id") != EXPECTED_CONTEXT_ID:
        raise RuntimeError("CR1 Context context_id mismatch")
    bindings = context.get("bindings") or {}
    if bindings.get("core_commit") != EXPECTED_CORE_COMMIT:
        raise RuntimeError("CR1 Context CORE binding mismatch")
    if bindings.get("hypothesis_registry_git_blob") != EXPECTED_REGISTRY_BLOB:
        raise RuntimeError("CR1 Context registry binding mismatch")


def validate_registry(registry: dict) -> None:
    if registry.get("schema") != "ATDS_CONTEXT_REGIME_HYPOTHESIS_REGISTRY_V0_1":
        raise RuntimeError("CR1 registry schema mismatch")
    if registry.get("status") != "PREFLIGHT_ONLY_NO_RESEARCH_EXECUTED":
        raise RuntimeError("CR1 registry status mismatch")
    if registry.get("epistemic_class") != "N0_EXPLORATORY":
        raise RuntimeError("CR1 registry epistemic class mismatch")
    ids = tuple(h.get("id") for h in registry.get("hypotheses", []))
    if ids != EXPECTED_HYPOTHESES:
        raise RuntimeError("CR1 registry hypothesis family mismatch")
    scoring = registry.get("scoring") or {}
    if scoring.get("ranking_or_winner_selection") is not False:
        raise RuntimeError("CR1 winner selection scope violation")
    if (registry.get("target_contract") or {}).get("pnl_target") is not False:
        raise RuntimeError("CR1 PnL target scope violation")
    if (registry.get("target_contract") or {}).get("directional_return_target") is not False:
        raise RuntimeError("CR1 direction target scope violation")


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


def resolve_bound_file(repo_root: Path, rel: str, *, sha256: str | None = None, git_blob: str | None = None) -> Path:
    raw = repo_root / Path(rel)
    if path_chain_has_reparse_or_symlink(raw):
        raise RuntimeError(f"bound file path contains reparse/symlink: {rel}")
    p = raw.resolve(strict=False)
    if not is_within(p, repo_root) or not p.is_file() or is_reparse_or_symlink(p):
        raise RuntimeError(f"invalid bound file path: {rel}")
    if sha256 is not None and sha256_path(p) != sha256:
        raise RuntimeError(f"bound file SHA-256 mismatch: {rel}")
    if git_blob is not None and git_blob_sha1_path(p) != git_blob:
        raise RuntimeError(f"bound file Git blob mismatch: {rel}")
    return p


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


def window_valid(valid,h):
    import numpy as np
    valid=np.asarray(valid,dtype=bool); n=len(valid)
    result=np.zeros(n,dtype=bool)
    bad=np.concatenate(([0],np.cumsum(~valid,dtype=np.int64)))
    t=np.arange(h,n,dtype=np.int64)
    result[t]=(bad[t+1]-bad[t-h+1])==0
    return result


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


def efficiency_array(signed_bps, valid, h):
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


def trailing_mean(values, minute, segment, h):
    import numpy as np
    x=np.asarray(values,dtype=np.float64); minute=np.asarray(minute,dtype=np.int64); segment=np.asarray(segment,dtype=np.int64)
    n=len(x); out=np.full(n,np.nan,dtype=np.float64)
    if h<=0 or n<h: return out
    cs=np.concatenate(([0.0],np.cumsum(x,dtype=np.float64)))
    end=np.arange(h-1,n,dtype=np.int64); start=end-h+1
    boundary=(segment[end]==segment[start]) & ((minute[end]-minute[start])==(h-1)*60_000)
    vals=(cs[end+1]-cs[start])/h
    out[end[boundary]]=vals[boundary]
    return out


def forward_mean(values, minute, segment, h):
    import numpy as np
    x=np.asarray(values,dtype=np.float64); minute=np.asarray(minute,dtype=np.int64); segment=np.asarray(segment,dtype=np.int64)
    n=len(x); out=np.full(n,np.nan,dtype=np.float64)
    if h<=0 or n<=h: return out
    cs=np.concatenate(([0.0],np.cumsum(x,dtype=np.float64)))
    t=np.arange(0,n-h,dtype=np.int64)
    end=t+h
    boundary=(segment[end]==segment[t]) & ((minute[end]-minute[t])==h*60_000)
    sums=cs[end+1]-cs[t+1]
    out[t[boundary]]=sums[boundary]/h
    return out


def forward_from_endpoint(backward_metric, minute, segment, h):
    import numpy as np
    x=np.asarray(backward_metric,dtype=np.float64); minute=np.asarray(minute,dtype=np.int64); segment=np.asarray(segment,dtype=np.int64)
    n=len(x); out=np.full(n,np.nan,dtype=np.float64)
    if n<=h: return out
    t=np.arange(0,n-h,dtype=np.int64); end=t+h
    ok=(segment[end]==segment[t]) & ((minute[end]-minute[t])==h*60_000) & np.isfinite(x[end])
    out[t[ok]]=x[end[ok]]
    return out


def time_dimensions(minute_ms):
    import numpy as np
    minute_ms=np.asarray(minute_ms,dtype=np.int64)
    hour_code=minute_ms//3_600_000
    unique,inverse=np.unique(hour_code,return_inverse=True)
    ny_hour=np.empty(unique.size,dtype=np.int16); ny_weekday=np.empty(unique.size,dtype=np.int16); utc_year=np.empty(unique.size,dtype=np.int16)
    for i,code in enumerate(unique):
        dt=datetime.fromtimestamp(int(code)*3600,tz=timezone.utc)
        ny=dt.astimezone(NY)
        ny_hour[i]=ny.hour; ny_weekday[i]=ny.weekday(); utc_year[i]=dt.year
    return ny_hour[inverse],ny_weekday[inverse],utc_year[inverse]


def minutes_since_segment_start(minute, segment):
    import numpy as np
    minute=np.asarray(minute,dtype=np.int64); segment=np.asarray(segment,dtype=np.int64)
    out=np.empty(len(minute),dtype=np.int64)
    if len(minute)==0: return out
    start=0
    for i in range(1,len(minute)+1):
        if i==len(minute) or segment[i]!=segment[start]:
            out[start:i]=(minute[start:i]-minute[start])//60_000
            start=i
    return out


def gap_state(minutes_since):
    import numpy as np
    x=np.asarray(minutes_since,dtype=np.int64)
    out=np.full(len(x),3,dtype=np.int8)
    out[x==0]=0
    out[(x>=1)&(x<=15)]=1
    out[(x>=16)&(x<=60)]=2
    return out


def quantile_thresholds(values, qs):
    import numpy as np
    x=np.asarray(values,dtype=np.float64); x=x[np.isfinite(x)]
    if x.size==0: raise RuntimeError("no finite training values for thresholds")
    return np.percentile(x,qs,method="linear")


def classify_target_train_frozen(target, train_valid):
    import numpy as np
    target=np.asarray(target,dtype=np.float64); train_valid=np.asarray(train_valid,dtype=bool)
    thresholds=quantile_thresholds(target[train_valid],(20,40,60,80))
    return discretize(target,thresholds), thresholds


def discretize(values, thresholds):
    import numpy as np
    x=np.asarray(values,dtype=np.float64); t=np.asarray(thresholds,dtype=np.float64)
    out=np.full(len(x),-1,dtype=np.int16)
    mask=np.isfinite(x)
    out[mask]=np.searchsorted(t,x[mask],side="right").astype(np.int16)
    return out


def hour_medians(values, ny_hour, mask):
    import numpy as np
    values=np.asarray(values,dtype=np.float64); ny_hour=np.asarray(ny_hour,dtype=np.int16); mask=np.asarray(mask,dtype=bool)
    med=np.full(24,np.nan,dtype=np.float64)
    for h in range(24):
        x=values[mask & (ny_hour==h) & np.isfinite(values)]
        if x.size: med[h]=np.median(x)
    return med


def relative_by_hour(values, ny_hour, medians):
    import numpy as np
    values=np.asarray(values,dtype=np.float64); ny_hour=np.asarray(ny_hour,dtype=np.int16); medians=np.asarray(medians,dtype=np.float64)
    denom=medians[ny_hour]
    out=np.full(len(values),np.nan,dtype=np.float64)
    ok=np.isfinite(values)&np.isfinite(denom)&(denom>0)
    out[ok]=values[ok]/denom[ok]
    return out


def fold_masks(utc_year, fold_id):
    import numpy as np
    y=np.asarray(utc_year,dtype=np.int16)
    if fold_id=="F1": return y<=2022, y==2023
    if fold_id=="F2": return y<=2023, y==2024
    if fold_id=="F3": return y<=2024, y==2025
    if fold_id=="D2026": return y<=2025, y==2026
    raise ValueError("unknown fold")


def baseline_key_codes(name, ny_hour, ny_weekday):
    import numpy as np
    h=np.asarray(ny_hour,dtype=np.int16); w=np.asarray(ny_weekday,dtype=np.int16)
    if name=="B0": return np.zeros(len(h),dtype=np.int32)
    if name=="B1": return h.astype(np.int32)
    if name=="B2": return (h.astype(np.int32)*7+w.astype(np.int32))
    raise ValueError("unknown baseline")


def candidate_key_codes(baseline_name, ny_hour, ny_weekday, states):
    import numpy as np
    states=np.asarray(states,dtype=np.int32)
    if baseline_name=="B0":
        return states.copy()
    base=baseline_key_codes(baseline_name,ny_hour,ny_weekday)
    n_states=int(states.max())+1 if states.size else 1
    return base*n_states+states


def fit_categorical_model(keys, classes, k=TARGET_CLASSES, alpha=ALPHA):
    import numpy as np
    keys=np.asarray(keys,dtype=np.int64); classes=np.asarray(classes,dtype=np.int16)
    valid=(keys>=0)&(classes>=0)
    if not np.any(valid):
        raise RuntimeError("empty categorical training sample")
    max_key=int(np.max(keys[valid]))
    counts=np.zeros((max_key+1,k),dtype=np.int64)
    np.add.at(counts,(keys[valid],classes[valid]),1)
    return counts


def probabilities_for_keys(counts, keys, k=TARGET_CLASSES, alpha=ALPHA):
    import numpy as np
    keys=np.asarray(keys,dtype=np.int64)
    out=np.full((len(keys),k),1.0/k,dtype=np.float64)
    known=(keys>=0)&(keys<counts.shape[0])
    if np.any(known):
        c=counts[keys[known]].astype(np.float64)
        out[known]=(c+alpha)/(c.sum(axis=1,keepdims=True)+alpha*k)
    return out


def probability_for(counts, key, k=TARGET_CLASSES, alpha=ALPHA):
    return probabilities_for_keys(counts,[int(key)],k,alpha)[0]


def score_model(counts, keys, classes):
    import numpy as np
    keys=np.asarray(keys,dtype=np.int64); classes=np.asarray(classes,dtype=np.int16)
    valid=(classes>=0)&(keys>=0)
    keys=keys[valid]; classes=classes[valid]
    if classes.size==0: raise RuntimeError("empty scoring sample")
    p=probabilities_for_keys(counts,keys)
    true_p=np.maximum(p[np.arange(classes.size),classes],1e-300)
    log_each=-np.log(true_p)
    brier_each=np.sum(p*p,axis=1)-2.0*true_p+1.0
    return {
        "n":int(classes.size),
        "log_loss":float(np.mean(log_each)),
        "brier":float(np.mean(brier_each)),
        "log_sum":float(np.sum(log_each,dtype=np.float64)),
        "brier_sum":float(np.sum(brier_each,dtype=np.float64)),
    }


def sparse_states(states, test_mask, valid_mask):
    import numpy as np
    s=np.asarray(states); mask=np.asarray(test_mask,dtype=bool)&np.asarray(valid_mask,dtype=bool)
    result=[]
    for v in sorted(set(map(int,s[mask].tolist()))):
        count=int(np.count_nonzero(mask & (s==v)))
        if 0<count<SPARSE_MIN_TEST:
            result.append({"state":v,"count":count})
    return result


def adjudicate_status(folds, pooled_delta_log_loss, pooled_delta_brier, sparse_any, critical_controls_pass=True):
    if not critical_controls_pass or sparse_any:
        return "NOT_INTERPRETABLE"
    vals=[folds[f]["delta_log_loss"] for f in PRIMARY_FOLDS]
    if all(v>0 for v in vals) and pooled_delta_brier>0:
        return "SUPPORTED_N0"
    if pooled_delta_log_loss<=0 or sum(v<=0 for v in vals)>=2:
        return "REFUTED_N0"
    return "NOT_INTERPRETABLE"


def hypothesis_spec(hid):
    if hid=="CR-H01-NY-HOUR": return ("RV15","B0","hour",False)
    if hid=="CR-H02-WEEKDAY": return ("RV15","B1","weekday",False)
    if hid=="CR-H03-ABS-VOL": return ("RV15","B2","rv_abs",True)
    if hid=="CR-H04-REL-VOL": return ("RV15","B2","rv_rel",True)
    if hid=="CR-H05-SPREAD": return ("SPREAD15","B2","spread_rel",True)
    if hid=="CR-H06-TICK-DENSITY": return ("TICK15","B2","tick_rel",True)
    if hid=="CR-H07-GAP-REOPEN": return ("RV15","B2","gap",False)
    if hid=="CR-H08-EFFICIENCY": return ("EFF15","B2","eff",True)
    raise ValueError("unknown hypothesis")


def secondary_target_for(hid):
    return {
        "CR-H01-NY-HOUR":"RV60","CR-H02-WEEKDAY":"RV60","CR-H03-ABS-VOL":"RV60","CR-H04-REL-VOL":"RV60",
        "CR-H05-SPREAD":"SPREAD60","CR-H06-TICK-DENSITY":"TICK60","CR-H07-GAP-REOPEN":"RV60","CR-H08-EFFICIENCY":"EFF60",
    }[hid]


def evaluate_one_fold(hid, fold_id, utc_year, ny_hour, ny_weekday, context_raw, targets):
    import numpy as np
    target_name,baseline_name,state_name,learn_tertiles=hypothesis_spec(hid)
    train_fold,test_fold=fold_masks(utc_year,fold_id)
    target=np.asarray(targets[target_name],dtype=np.float64)
    train_target=train_fold & np.isfinite(target)
    test_target=test_fold & np.isfinite(target)

    if state_name=="hour":
        states=ny_hour.astype(np.int16)
        context_valid=np.ones(len(target),dtype=bool)
    elif state_name=="weekday":
        states=ny_weekday.astype(np.int16)
        context_valid=np.ones(len(target),dtype=bool)
    elif state_name=="gap":
        states=np.asarray(context_raw["gap"],dtype=np.int16)
        context_valid=np.ones(len(target),dtype=bool)
    else:
        raw=np.asarray(context_raw[state_name],dtype=np.float64)
        context_valid=np.isfinite(raw)
        train_for_threshold=train_fold & context_valid
        thresholds=quantile_thresholds(raw[train_for_threshold],(100/3,200/3))
        states=discretize(raw,thresholds)

    train_valid=train_target & context_valid
    test_valid=test_target & context_valid
    train_class,target_thresholds=classify_target_train_frozen(target,train_valid)
    test_class=train_class

    base_all=baseline_key_codes(baseline_name,ny_hour,ny_weekday)
    cand_all=candidate_key_codes(baseline_name,ny_hour,ny_weekday,states)
    base_keys_train=base_all[train_valid]; base_keys_test=base_all[test_valid]
    cand_keys_train=cand_all[train_valid]; cand_keys_test=cand_all[test_valid]

    ytr=train_class[train_valid]; yte=test_class[test_valid]
    base=fit_categorical_model(base_keys_train,ytr); cand=fit_categorical_model(cand_keys_train,ytr)
    bs=score_model(base,base_keys_test,yte); cs=score_model(cand,cand_keys_test,yte)
    sparse=sparse_states(states,test_fold,test_valid)
    return {
        "fold":fold_id,"baseline":baseline_name,"primary_target":target_name,
        "train_n":int(np.count_nonzero(train_valid)),"test_n":int(np.count_nonzero(test_valid)),
        "delta_log_loss":bs["log_loss"]-cs["log_loss"],"delta_brier":bs["brier"]-cs["brier"],
        "baseline_log_sum":bs["log_sum"],"candidate_log_sum":cs["log_sum"],
        "baseline_brier_sum":bs["brier_sum"],"candidate_brier_sum":cs["brier_sum"],
        "sparse_states":sparse,
        "target_thresholds":[float(x) for x in target_thresholds],
        "state_counts_test":{str(int(v)):int(np.count_nonzero(test_valid & (states==v))) for v in sorted(set(map(int,states[test_valid].tolist())))},
    }


def evaluate_override_target(hid, fold_id, override_target, utc_year, ny_hour, ny_weekday, context_raw, targets):
    primary_name,baseline,state_name,learn=hypothesis_spec(hid)
    remap=dict(targets); remap[primary_name]=targets[override_target]
    result=evaluate_one_fold(hid,fold_id,utc_year,ny_hour,ny_weekday,context_raw,remap)
    result["override_target"]=override_target
    result.pop("primary_target",None)
    return result


def evaluate_secondary_fold(hid, fold_id, utc_year, ny_hour, ny_weekday, context_raw, targets):
    secondary=secondary_target_for(hid)
    result=evaluate_override_target(hid,fold_id,secondary,utc_year,ny_hour,ny_weekday,context_raw,targets)
    result["secondary_target"]=result.pop("override_target")
    return result


def diagnostic_targets_for(hid):
    return ("SPREAD15",) if hid=="CR-H07-GAP-REOPEN" else ()


def validate_arrays(minute,tick,seg,close,spread,previous=None):
    import numpy as np
    n=len(minute)
    if n==0 or any(len(x)!=n for x in (tick,seg,close,spread)): raise RuntimeError("decoded row mismatch/empty")
    if np.any(np.diff(minute)<=0): raise RuntimeError("minute order violation")
    if previous is None:
        if int(seg[0])!=0: raise RuntimeError("first segment must be zero")
    else:
        if int(minute[0])<=previous[0]: raise RuntimeError("global minute order violation")
        if int(seg[0])-previous[1] not in (0,1): raise RuntimeError("segment boundary violation")
    if np.any(tick<=0) or np.any(~np.isfinite(close)) or np.any(close<=0) or np.any(~np.isfinite(spread)) or np.any(spread<=0):
        raise RuntimeError("numeric domain violation")
    if np.any(np.diff(seg)<0) or np.any(np.diff(seg)>1): raise RuntimeError("segment jump violation")


def write_json_exclusive(path: Path,payload: dict):
    raw=(json.dumps(payload,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
    if len(raw)>MAX_OUTPUT_BYTES: raise RuntimeError("CR1 output exceeds bound")
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("xb") as f: f.write(raw)


def main():
    ap=argparse.ArgumentParser(description="CR1 N0 context-informativeness research")
    ap.add_argument("--repo-root",required=True)
    ap.add_argument("--ap0-root",required=True)
    ap.add_argument("--ap0-manifest",required=True)
    ap.add_argument("--context-json",required=True)
    ap.add_argument("--registry-json",required=True)
    ap.add_argument("--core-json",required=True)
    ap.add_argument("--output",default=str(Path(tempfile.gettempdir())/"ATDS-CR1-CONTEXT-INFORMATIVENESS.json"))
    args=ap.parse_args()

    repo_raw=Path(args.repo_root).expanduser(); root_raw=Path(args.ap0_root).expanduser()
    manifest_raw=Path(args.ap0_manifest).expanduser(); context_raw_path=Path(args.context_json).expanduser()
    registry_raw=Path(args.registry_json).expanduser(); core_raw=Path(args.core_json).expanduser(); output_raw=Path(args.output).expanduser()
    if os.path.lexists(output_raw):
        print("BLOCKED_CR1_OUTPUT_EXISTS"); print(output_raw); return 2
    for raw,label in ((repo_raw,"repo-root"),(root_raw,"AP0 root"),(manifest_raw,"AP0 manifest"),(context_raw_path,"Context"),(registry_raw,"registry"),(core_raw,"CORE"),(output_raw.parent,"output parent")):
        if path_chain_has_reparse_or_symlink(raw):
            print("BLOCKED_CR1_REPARSE"); print(f"{label}: {raw}"); return 2

    repo_root=repo_raw.resolve(strict=False); root=root_raw.resolve(strict=False); manifest_path=manifest_raw.resolve(strict=False)
    context_path=context_raw_path.resolve(strict=False); registry_path=registry_raw.resolve(strict=False); core_path=core_raw.resolve(strict=False); output=output_raw.resolve(strict=False)

    def block(code,reason):
        payload={"schema":"ATDS_CR1_BLOCKED_V0_1","status":code,"reason":reason}
        try:
            if not output.exists(): write_json_exclusive(output,payload)
        except Exception: pass
        print(code); print(reason); print(f"Report: {output}"); return 2

    try:
        if not repo_root.is_dir() or not root.is_dir() or not manifest_path.is_file(): raise RuntimeError("required input missing")
        if output==root or is_within(output,root): raise RuntimeError("output inside AP0 input")
        if sha256_path(manifest_path)!=EXPECTED_AP0_MANIFEST_SHA256: raise RuntimeError("AP0 manifest SHA mismatch")

        # Require supplied exact governance inputs inside repo-root, not reconstruction/fallback.
        expected_context=resolve_bound_file(repo_root,EXPECTED_CONTEXT_REPO_PATH,sha256=EXPECTED_CONTEXT_SHA256)
        expected_registry=resolve_bound_file(repo_root,EXPECTED_REGISTRY_REPO_PATH,sha256=EXPECTED_REGISTRY_SHA256)
        expected_core=resolve_bound_file(repo_root,EXPECTED_CORE_REPO_PATH,git_blob=EXPECTED_CORE_GIT_BLOB)
        if context_path!=expected_context or registry_path!=expected_registry or core_path!=expected_core:
            raise RuntimeError("CR1 governance input path mismatch")
        context=json.loads(context_path.read_text(encoding="utf-8")); registry=json.loads(registry_path.read_text(encoding="utf-8")); core=json.loads(core_path.read_text(encoding="utf-8"))
        validate_context_payload(context); validate_registry(registry)
        if core.get("schema")!="ATDS_ASSET_BEHAVIORAL_PROFILE_CORE_V0_1" or core.get("status")!="CORE_COMPLETE" or core.get("promotion_gate")!="PASS":
            raise RuntimeError("CORE status mismatch")
        if core.get("binding")!=EXPECTED_CORE_BINDING:
            raise RuntimeError("CORE upstream binding mismatch")

        manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("status")!="AP0_COMPLETE" or manifest.get("output_identity")!=EXPECTED_AP0_IDENTITY: raise RuntimeError("AP0 identity/status mismatch")
        files=manifest.get("files"); cov=manifest.get("coverage") or {}
        if not isinstance(files,list) or len(files)!=EXPECTED_FILES: raise RuntimeError("AP0 file count mismatch")
        if cov.get("minute_rows_written")!=EXPECTED_MINUTES or cov.get("source_ticks_read")!=EXPECTED_SOURCE_TICKS or cov.get("segments")!=EXPECTED_SEGMENTS: raise RuntimeError("AP0 coverage mismatch")

        import numpy as np, pyarrow as pa, pyarrow.parquet as pq
        chunks={k:[] for k in ("minute","tick","seg","close","spread")}; rows=0; ticks=0; previous=None
        for rec in files:
            rel=rec["relative_path"]; p=resolve_manifest_member(root,rel)
            if int(p.stat().st_size)!=int(rec["size_bytes"]) or sha256_path(p)!=rec["sha256"]: raise RuntimeError(f"AP0 identity mismatch: {rel}")
            pf=pq.ParquetFile(p)
            if int(pf.metadata.num_rows)!=int(rec["rows"]): raise RuntimeError(f"AP0 rows mismatch: {rel}")
            if [(f.name,str(f.type)) for f in pf.schema_arrow]!=REQUIRED_SCHEMA: raise RuntimeError(f"AP0 schema mismatch: {rel}")
            meta=pf.schema_arrow.metadata or {}
            if meta.get(b"dataset_identity")!=EXPECTED_AP0_IDENTITY.encode() or meta.get(b"volumes_used")!=b"false": raise RuntimeError(f"AP0 metadata mismatch: {rel}")
            table=pf.read(columns=READ_COLUMNS,use_threads=False)
            if table.column_names!=READ_COLUMNS: raise RuntimeError("CR1 column scope violation")
            vals={
                "minute":table["minute_start_ms_utc"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64,copy=False),
                "tick":table["tick_count"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64,copy=False),
                "seg":table["segment_id"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64,copy=False),
                "close":table["mid_close"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64,copy=False),
                "spread":table["spread_mean"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64,copy=False),
            }
            validate_arrays(**vals,previous=previous); previous=(int(vals["minute"][-1]),int(vals["seg"][-1]))
            rows += len(vals["minute"]); ticks += int(np.sum(vals["tick"],dtype=np.int64))
            for k,v in vals.items(): chunks[k].append(v.copy())
            if sha256_path(p)!=rec["sha256"]: raise RuntimeError(f"AP0 changed during CR1: {rel}")
        if rows!=EXPECTED_MINUTES or ticks!=EXPECTED_SOURCE_TICKS: raise RuntimeError("CR1 reconstructed coverage mismatch")
        a={k:np.concatenate(v) for k,v in chunks.items()}
        if int(a["seg"][0])!=0 or int(a["seg"][-1])!=EXPECTED_SEGMENTS-1: raise RuntimeError("CR1 segment coverage mismatch")

        signed,valid=signed_return_1m_bps(a["minute"],a["seg"],a["close"])
        rv15=rolling_realized_vol_bps(signed,valid,a["minute"],a["seg"],15); rv60=rolling_realized_vol_bps(signed,valid,a["minute"],a["seg"],60)
        eff15=efficiency_array(signed,valid,15); eff60=efficiency_array(signed,valid,60)
        spread5=trailing_mean(a["spread"],a["minute"],a["seg"],5); tick5=trailing_mean(a["tick"],a["minute"],a["seg"],5)
        fwd={
            "RV15":forward_from_endpoint(rv15,a["minute"],a["seg"],15),
            "RV60":forward_from_endpoint(rv60,a["minute"],a["seg"],60),
            "EFF15":forward_from_endpoint(eff15,a["minute"],a["seg"],15),
            "EFF60":forward_from_endpoint(eff60,a["minute"],a["seg"],60),
            "SPREAD15":forward_mean(a["spread"],a["minute"],a["seg"],15),
            "SPREAD60":forward_mean(a["spread"],a["minute"],a["seg"],60),
            "TICK15":forward_mean(a["tick"],a["minute"],a["seg"],15),
            "TICK60":forward_mean(a["tick"],a["minute"],a["seg"],60),
        }
        nyh,nyw,uy=time_dimensions(a["minute"])
        mins=minutes_since_segment_start(a["minute"],a["seg"]); gstate=gap_state(mins)

        results=[]
        for hid in EXPECTED_HYPOTHESES:
            primary_folds={}
            secondary_folds={}
            diagnostic_folds={target:{} for target in diagnostic_targets_for(hid)}
            # Fold-specific context arrays because relative normalisation must be learned on train only.
            pooled={"base_log":0.0,"cand_log":0.0,"base_brier":0.0,"cand_brier":0.0,"n":0}
            sparse_any=False
            for fid in ALL_FOLDS:
                train_mask,test_mask=fold_masks(uy,fid)
                context_raw={"gap":gstate,"rv_abs":rv15,"eff":eff15}
                med_rv=hour_medians(rv15,nyh,train_mask & np.isfinite(rv15))
                med_sp=hour_medians(spread5,nyh,train_mask & np.isfinite(spread5))
                med_tk=hour_medians(tick5,nyh,train_mask & np.isfinite(tick5))
                context_raw["rv_rel"]=relative_by_hour(rv15,nyh,med_rv)
                context_raw["spread_rel"]=relative_by_hour(spread5,nyh,med_sp)
                context_raw["tick_rel"]=relative_by_hour(tick5,nyh,med_tk)
                pr=evaluate_one_fold(hid,fid,uy,nyh,nyw,context_raw,fwd)
                sr=evaluate_secondary_fold(hid,fid,uy,nyh,nyw,context_raw,fwd)
                primary_folds[fid]=pr; secondary_folds[fid]=sr
                for diagnostic_target in diagnostic_targets_for(hid):
                    diagnostic_folds[diagnostic_target][fid]=evaluate_override_target(hid,fid,diagnostic_target,uy,nyh,nyw,context_raw,fwd)
                if fid in PRIMARY_FOLDS:
                    pooled["base_log"]+=pr["baseline_log_sum"]; pooled["cand_log"]+=pr["candidate_log_sum"]
                    pooled["base_brier"]+=pr["baseline_brier_sum"]; pooled["cand_brier"]+=pr["candidate_brier_sum"]; pooled["n"]+=pr["test_n"]
                    sparse_any = sparse_any or bool(pr["sparse_states"])
            pooled_dll=(pooled["base_log"]-pooled["cand_log"])/pooled["n"]
            pooled_dbr=(pooled["base_brier"]-pooled["cand_brier"])/pooled["n"]
            status=adjudicate_status(primary_folds,pooled_dll,pooled_dbr,sparse_any,True)
            # Remove sums from public fold details.
            for d in (primary_folds,secondary_folds,*diagnostic_folds.values()):
                for x in d.values():
                    for k in ("baseline_log_sum","candidate_log_sum","baseline_brier_sum","candidate_brier_sum"):
                        x.pop(k,None)
            results.append({
                "hypothesis_id":hid,
                "scientific_status":status,
                "primary":primary_folds,
                "secondary_robustness":secondary_folds,
                "additional_diagnostics":diagnostic_folds,
                "pooled_primary":{"n":pooled["n"],"delta_log_loss":pooled_dll,"delta_brier":pooled_dbr},
                "sparse_guard_triggered":sparse_any,
            })

        if tuple(r["hypothesis_id"] for r in results)!=EXPECTED_HYPOTHESES: raise RuntimeError("CR1 result family omission")
        payload={
            "schema":"ATDS_CR1_CONTEXT_INFORMATIVENESS_V0_1",
            "status":"CR1_COMPLETE",
            "research_class":"N0_EXPLORATORY_PREVIOUSLY_EXPOSED_CORPUS",
            "context_id":context["context_id"],
            "binding":{
                "ap0_manifest_sha256":EXPECTED_AP0_MANIFEST_SHA256,
                "context_sha256":EXPECTED_CONTEXT_SHA256,
                "registry_sha256":EXPECTED_REGISTRY_SHA256,
                "core_git_blob":EXPECTED_CORE_GIT_BLOB,
                "ap0_files_rehashed":EXPECTED_FILES,
            },
            "coverage":{"minute_rows":rows,"source_ticks_accounted":ticks,"segments":EXPECTED_SEGMENTS},
            "scope":SCOPE,
            "fold_contract":{"primary_folds":list(PRIMARY_FOLDS),"diagnostic_fold":"D2026","calendar_boundary":"UTC","pristine_oos":False},
            "score_contract":{"target_classes":TARGET_CLASSES,"laplace_alpha":ALPHA,"sparse_min_test":SPARSE_MIN_TEST},
            "hypotheses":results,
            "runtime":{"numpy_version":np.__version__,"pyarrow_version":pa.__version__},
        }
        write_json_exclusive(output,payload)
        print("CR1_COMPLETE"); print(f"Minute rows: {rows}"); print(f"Source ticks accounted: {ticks}")
        for r in results: print(f"{r['hypothesis_id']}: {r['scientific_status']} pooled_dLL={r['pooled_primary']['delta_log_loss']:.12g}")
        print(f"Report: {output}"); return 0
    except Exception as exc:
        return block("BLOCKED_CR1_RUNTIME",str(exc))


if __name__=="__main__":
    raise SystemExit(main())
