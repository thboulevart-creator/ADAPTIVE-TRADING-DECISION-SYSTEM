#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import stat
import tempfile
from pathlib import Path

EXPECTED_AP0_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
EXPECTED_AP0_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
EXPECTED_FILES = 61
EXPECTED_MINUTES = 1_709_180
EXPECTED_SOURCE_TICKS = 376_003_618
EXPECTED_SEGMENTS = 1_606

EXPECTED_CR1_HELPER_BLOB = "bb5cd4acd1b48141019c0ec3796ea61627dc0dbf"
EXPECTED_CR1_HELPER_PATH = Path("tools/cr1_context_informativeness.py")
EXPECTED_CONTEXT_PATH = Path("reports/program/evidence/2026-09-26-CR1-CONTEXT-V0.1.json")
EXPECTED_CONTEXT_SHA256 = "3c507795c996e571152d4877a594abb889e4a8a017130332a166d5dda84af866"
EXPECTED_CONTEXT_ID = "CTX-d0501ec820062bfe373f1f4b94de4e191ca2c7e05bbe788b3d5d963750158cbf"
EXPECTED_CR1_EVIDENCE_PATH = Path("reports/program/evidence/2026-09-26-CR1-CONTEXT-INFORMATIVENESS.json")
EXPECTED_CR1_EVIDENCE_BLOB = "cd40bf975613d1fa0e6d7277c2850ec87104727e"
EXPECTED_CR2_REGISTRY_PATH = Path("reports/program/evidence/2026-09-26-CR2-CANDIDATE-REGISTRY-V0.1.json")
EXPECTED_CR2_REGISTRY_BLOB = "c6e19dc67c521d8f79814473ffa19ae427398e4f"

EXPECTED_CR1_STATUSES = {
    "CR-H01-NY-HOUR":"SUPPORTED_N0",
    "CR-H02-WEEKDAY":"SUPPORTED_N0",
    "CR-H03-ABS-VOL":"SUPPORTED_N0",
    "CR-H04-REL-VOL":"SUPPORTED_N0",
    "CR-H05-SPREAD":"NOT_INTERPRETABLE",
    "CR-H06-TICK-DENSITY":"SUPPORTED_N0",
    "CR-H07-GAP-REOPEN":"REFUTED_N0",
    "CR-H08-EFFICIENCY":"REFUTED_N0",
}
EXPECTED_FAMILIES = ("CR2-C01-ABS_VOL_X_TICK","CR2-C02-REL_VOL_X_TICK")
PRIMARY_FOLDS = ("F1","F2","F3")
ALL_FOLDS = ("F1","F2","F3","D2026")
SPARSE_MIN_TEST = 500
ALPHA = 1.0
TARGET_CLASSES = 25
MAX_OUTPUT_BYTES = 32 * 1024 * 1024

SCOPE = {
    "epistemic_class":"N0_EXPLORATORY",
    "strategy_agnostic":True,
    "direction_target_used":False,
    "pnl_calculated":False,
    "trades_calculated":False,
    "signals_calculated":False,
    "optimization":False,
    "threshold_search":False,
    "feature_search":False,
    "interaction_search":False,
    "winner_selection":False,
    "semantic_regime_labels_instantiated":False,
    "mt5_used":False,
    "pristine_oos_claim":False,
}

READ_COLUMNS = ["minute_start_ms_utc","tick_count","segment_id","mid_close"]

def sha256_path(path: Path, chunk: int = 1024*1024) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(chunk),b""): h.update(b)
    return h.hexdigest()

def git_blob_sha1_bytes(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii")+raw).hexdigest()

def git_blob_sha1_path(path: Path) -> str:
    return git_blob_sha1_bytes(path.read_bytes())

def is_reparse_or_symlink(path: Path) -> bool:
    st=path.lstat()
    if stat.S_ISLNK(st.st_mode): return True
    attrs=getattr(st,"st_file_attributes",0)
    return bool(attrs & getattr(stat,"FILE_ATTRIBUTE_REPARSE_POINT",0x400))

def path_chain_has_reparse_or_symlink(path: Path) -> bool:
    absolute=path.absolute(); parts=absolute.parts
    if not parts: return False
    cur=Path(parts[0])
    for part in parts[1:]:
        cur=cur/part
        if os.path.lexists(cur):
            if is_reparse_or_symlink(cur): return True
        else:
            break
    return False

def is_within(child: Path,parent: Path) -> bool:
    try:
        c=os.path.normcase(str(child.resolve(strict=False)))
        p=os.path.normcase(str(parent.resolve(strict=False)))
        return os.path.commonpath([c,p])==p
    except ValueError:
        return False

def resolve_bound_file(repo_root: Path, rel: Path, *, sha256=None, git_blob=None) -> Path:
    raw=repo_root/rel
    if path_chain_has_reparse_or_symlink(raw): raise RuntimeError(f"bound path contains reparse/symlink: {rel}")
    p=raw.resolve(strict=False)
    if not is_within(p,repo_root) or not p.is_file() or is_reparse_or_symlink(p):
        raise RuntimeError(f"invalid bound path: {rel}")
    if sha256 is not None and sha256_path(p)!=sha256: raise RuntimeError(f"SHA mismatch: {rel}")
    if git_blob is not None and git_blob_sha1_path(p)!=git_blob: raise RuntimeError(f"Git blob mismatch: {rel}")
    return p

def load_cr1_module(repo_root: Path):
    p=resolve_bound_file(repo_root,EXPECTED_CR1_HELPER_PATH,git_blob=EXPECTED_CR1_HELPER_BLOB)
    spec=importlib.util.spec_from_file_location("atds_cr1_bound",p)
    if spec is None or spec.loader is None: raise RuntimeError("cannot load bound CR1 helper")
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def write_json_exclusive(path: Path,payload: dict) -> None:
    raw=(json.dumps(payload,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
    if len(raw)>MAX_OUTPUT_BYTES: raise RuntimeError("CR2 JSON exceeds output bound")
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("xb") as f: f.write(raw)

def validate_context(ctx: dict) -> None:
    if ctx.get("schema")!="ATDS_CR1_CONTEXT_V0_1" or ctx.get("context_id")!=EXPECTED_CONTEXT_ID:
        raise RuntimeError("Context identity mismatch")
    if ctx.get("dataset_id")!=EXPECTED_AP0_IDENTITY or ctx.get("content_hash")!=EXPECTED_AP0_MANIFEST_SHA256:
        raise RuntimeError("Context dataset binding mismatch")

def validate_cr1_evidence(ev: dict) -> None:
    if ev.get("schema")!="ATDS_CR1_CONTEXT_INFORMATIVENESS_V0_1" or ev.get("status")!="CR1_COMPLETE":
        raise RuntimeError("CR1 evidence schema/status mismatch")
    if ev.get("research_class")!="N0_EXPLORATORY_PREVIOUSLY_EXPOSED_CORPUS": raise RuntimeError("CR1 research class mismatch")
    if ev.get("context_id")!=EXPECTED_CONTEXT_ID: raise RuntimeError("CR1 Context mismatch")
    if ev.get("fold_contract",{}).get("pristine_oos") is not False: raise RuntimeError("CR1 pristine OOS mismatch")
    got={x.get("hypothesis_id"):x.get("scientific_status") for x in ev.get("hypotheses",[])}
    if got!=EXPECTED_CR1_STATUSES: raise RuntimeError("CR1 status family mismatch")
    scope=ev.get("scope") or {}
    forbidden=("pnl_calculated","direction_target_used","optimization","feature_search","interaction_search","winner_selection","regime_labels_instantiated","mt5_used")
    if any(scope.get(k) is not False for k in forbidden): raise RuntimeError("CR1 scope mismatch")

def validate_cr2_registry(reg: dict) -> None:
    if reg.get("schema")!="ATDS_CR2_REGIME_CANDIDATE_REGISTRY_V0_1" or reg.get("status")!="PREFLIGHT_ONLY_NO_SYNTHESIS_EXECUTED":
        raise RuntimeError("CR2 registry schema/status mismatch")
    fam=tuple(x.get("id") for x in reg.get("candidate_families",[]))
    if fam!=EXPECTED_FAMILIES: raise RuntimeError("CR2 candidate family mismatch")
    admitted=reg.get("admitted_axes") or []
    expected=["NY_HOUR","NY_WEEKDAY","BACKWARD_RV15_ABSOLUTE_STATE","BACKWARD_RV15_HOUR_RELATIVE_STATE","BACKWARD_TICK5_HOUR_RELATIVE_STATE"]
    if admitted!=expected: raise RuntimeError("CR2 admitted axes mismatch")
    if int((reg.get("scoring") or {}).get("sparse_min_test_per_joint_state",-1))!=SPARSE_MIN_TEST:
        raise RuntimeError("CR2 sparse floor mismatch")

def joint_target_classes(rv, tick, train_valid):
    import numpy as np
    rv=np.asarray(rv,dtype=np.float64); tick=np.asarray(tick,dtype=np.float64); train_valid=np.asarray(train_valid,dtype=bool)
    rv_th=np.percentile(rv[train_valid],(20,40,60,80),method="linear")
    tk_th=np.percentile(tick[train_valid],(20,40,60,80),method="linear")
    out=np.full(len(rv),-1,dtype=np.int16)
    valid=np.isfinite(rv)&np.isfinite(tick)
    r=np.searchsorted(rv_th,rv[valid],side="right").astype(np.int16)
    t=np.searchsorted(tk_th,tick[valid],side="right").astype(np.int16)
    out[valid]=(r*5+t).astype(np.int16)
    return out,rv_th,tk_th

def tertile_states(values, train_mask):
    import numpy as np
    x=np.asarray(values,dtype=np.float64); train_mask=np.asarray(train_mask,dtype=bool)
    valid=train_mask & np.isfinite(x)
    if not np.any(valid): raise RuntimeError("empty state training sample")
    th=np.percentile(x[valid],(100/3,200/3),method="linear")
    out=np.full(len(x),-1,dtype=np.int16)
    ok=np.isfinite(x)
    out[ok]=np.searchsorted(th,x[ok],side="right").astype(np.int16)
    return out,th

def joint_state(vol_state,tick_state):
    import numpy as np
    v=np.asarray(vol_state,dtype=np.int16); t=np.asarray(tick_state,dtype=np.int16)
    out=np.full(len(v),-1,dtype=np.int16)
    ok=(v>=0)&(v<=2)&(t>=0)&(t<=2)
    out[ok]=(v[ok]*3+t[ok]).astype(np.int16)
    return out

def b2_codes(ny_hour,ny_weekday):
    import numpy as np
    h=np.asarray(ny_hour,dtype=np.int16); w=np.asarray(ny_weekday,dtype=np.int16)
    return h.astype(np.int32)*7+w.astype(np.int32)

def conditional_codes(base,state,n_states):
    import numpy as np
    b=np.asarray(base,dtype=np.int64); s=np.asarray(state,dtype=np.int16)
    out=np.full(len(b),-1,dtype=np.int64)
    ok=(s>=0)&(s<n_states)
    out[ok]=b[ok]*n_states+s[ok]
    return out

def fit_model(keys,classes,k=TARGET_CLASSES,alpha=ALPHA):
    import numpy as np
    keys=np.asarray(keys,dtype=np.int64); classes=np.asarray(classes,dtype=np.int16)
    valid=(keys>=0)&(classes>=0)
    if not np.any(valid): raise RuntimeError("empty categorical training sample")
    counts=np.zeros((int(np.max(keys[valid]))+1,k),dtype=np.int64)
    np.add.at(counts,(keys[valid],classes[valid]),1)
    return counts

def probabilities(counts,keys,k=TARGET_CLASSES,alpha=ALPHA):
    import numpy as np
    keys=np.asarray(keys,dtype=np.int64)
    out=np.full((len(keys),k),1.0/k,dtype=np.float64)
    known=(keys>=0)&(keys<counts.shape[0])
    if np.any(known):
        c=counts[keys[known]].astype(np.float64)
        out[known]=(c+alpha)/(c.sum(axis=1,keepdims=True)+alpha*k)
    return out

def score(counts,keys,classes,k=TARGET_CLASSES):
    import numpy as np
    keys=np.asarray(keys,dtype=np.int64); classes=np.asarray(classes,dtype=np.int16)
    valid=(keys>=0)&(classes>=0)
    keys=keys[valid]; classes=classes[valid]
    if classes.size==0: raise RuntimeError("empty scoring sample")
    p=probabilities(counts,keys,k=k)
    tp=np.maximum(p[np.arange(classes.size),classes],1e-300)
    ll=-np.log(tp); br=np.sum(p*p,axis=1)-2.0*tp+1.0
    return {"n":int(classes.size),"log_loss":float(np.mean(ll)),"brier":float(np.mean(br)),
            "log_sum":float(np.sum(ll,dtype=np.float64)),"brier_sum":float(np.sum(br,dtype=np.float64))}

def sparse_joint_states(states,test_valid):
    import numpy as np
    s=np.asarray(states,dtype=np.int16); mask=np.asarray(test_valid,dtype=bool)
    out=[]
    for v in range(9):
        n=int(np.count_nonzero(mask&(s==v)))
        if n<SPARSE_MIN_TEST: out.append({"state":v,"count":n})
    return out

def comparison_result(base_counts,cand_counts,base_keys,cand_keys,classes):
    bs=score(base_counts,base_keys,classes); cs=score(cand_counts,cand_keys,classes)
    if bs["n"]!=cs["n"]: raise RuntimeError("comparison sample mismatch")
    return {"n":bs["n"],"delta_log_loss":bs["log_loss"]-cs["log_loss"],
            "delta_brier":bs["brier"]-cs["brier"],
            "baseline_log_sum":bs["log_sum"],"candidate_log_sum":cs["log_sum"],
            "baseline_brier_sum":bs["brier_sum"],"candidate_brier_sum":cs["brier_sum"]}

def pooled_comparison(folds,comparison_name):
    n=sum(folds[f]["comparisons"][comparison_name]["n"] for f in PRIMARY_FOLDS)
    if n<=0: raise RuntimeError("empty pooled comparison")
    bll=sum(folds[f]["comparisons"][comparison_name]["baseline_log_sum"] for f in PRIMARY_FOLDS)/n
    cll=sum(folds[f]["comparisons"][comparison_name]["candidate_log_sum"] for f in PRIMARY_FOLDS)/n
    bbr=sum(folds[f]["comparisons"][comparison_name]["baseline_brier_sum"] for f in PRIMARY_FOLDS)/n
    cbr=sum(folds[f]["comparisons"][comparison_name]["candidate_brier_sum"] for f in PRIMARY_FOLDS)/n
    return {"n":n,"delta_log_loss":bll-cll,"delta_brier":bbr-cbr}

def adjudicate_candidate(folds,pooled,sparse_any):
    if sparse_any: return "NOT_INTERPRETABLE"
    comp_names=tuple(pooled.keys())
    all_supported=True
    for c in comp_names:
        vals=[folds[f]["comparisons"][c]["delta_log_loss"] for f in PRIMARY_FOLDS]
        if pooled[c]["delta_log_loss"]<=0 or sum(v<=0 for v in vals)>=2:
            return "REFUTED_N0_SYNTHESIS"
        if not (all(v>0 for v in vals) and pooled[c]["delta_brier"]>0):
            all_supported=False
    return "SUPPORTED_N0_SYNTHESIS" if all_supported else "NOT_INTERPRETABLE"

def evaluate_family_fold(family_id,fold_id,utc_year,ny_hour,ny_weekday,rv_context,tick_context,rv_target,tick_target):
    import numpy as np
    train_fold,test_fold = _fold_masks(utc_year,fold_id)
    base=b2_codes(ny_hour,ny_weekday)

    if family_id=="CR2-C01-ABS_VOL_X_TICK":
        vol_raw=np.asarray(rv_context["abs"],dtype=np.float64)
    elif family_id=="CR2-C02-REL_VOL_X_TICK":
        vol_raw=np.asarray(rv_context["rel_by_fold"][fold_id],dtype=np.float64)
    else:
        raise ValueError("unknown CR2 family")
    tick_raw=np.asarray(tick_context["rel_by_fold"][fold_id],dtype=np.float64)

    vol_state,vol_th=tertile_states(vol_raw,train_fold)
    tick_state,tick_th=tertile_states(tick_raw,train_fold)
    joint=joint_state(vol_state,tick_state)

    rv=np.asarray(rv_target,dtype=np.float64); tk=np.asarray(tick_target,dtype=np.float64)
    target_valid=np.isfinite(rv)&np.isfinite(tk)
    context_valid=(joint>=0)
    train_valid=train_fold&target_valid&context_valid
    test_valid=test_fold&target_valid&context_valid
    classes,rv_q,tick_q=joint_target_classes(rv,tk,train_valid)

    cand_keys=conditional_codes(base,joint,9)
    vol_keys=conditional_codes(base,vol_state,3)
    tick_keys=conditional_codes(base,tick_state,3)

    ytr=classes[train_valid]; yte=classes[test_valid]
    cand=fit_model(cand_keys[train_valid],ytr)
    volm=fit_model(vol_keys[train_valid],ytr)
    tickm=fit_model(tick_keys[train_valid],ytr)

    comps={
        "vs_vol":comparison_result(volm,cand,vol_keys[test_valid],cand_keys[test_valid],yte),
        "vs_tick":comparison_result(tickm,cand,tick_keys[test_valid],cand_keys[test_valid],yte),
    }
    sparse=sparse_joint_states(joint,test_valid)
    return {
        "fold":fold_id,
        "train_n":int(np.count_nonzero(train_valid)),
        "test_n":int(np.count_nonzero(test_valid)),
        "comparisons":comps,
        "sparse_states":sparse,
        "joint_state_counts_test":{str(v):int(np.count_nonzero(test_valid&(joint==v))) for v in range(9)},
        "vol_state_thresholds":[float(x) for x in vol_th],
        "tick_state_thresholds":[float(x) for x in tick_th],
        "rv_target_quintiles":[float(x) for x in rv_q],
        "tick_target_quintiles":[float(x) for x in tick_q],
    }

def _fold_masks(utc_year,fold_id):
    import numpy as np
    y=np.asarray(utc_year,dtype=np.int16)
    if fold_id=="F1": return y<=2022,y==2023
    if fold_id=="F2": return y<=2023,y==2024
    if fold_id=="F3": return y<=2024,y==2025
    if fold_id=="D2026": return y<=2025,y==2026
    raise ValueError("unknown fold")

def make_relative_by_fold(cr1,values,ny_hour,utc_year):
    out={}
    for fold in ALL_FOLDS:
        train,_=_fold_masks(utc_year,fold)
        med=cr1.hour_medians(values,ny_hour,train)
        out[fold]=cr1.relative_by_hour(values,ny_hour,med)
    return out

def evaluate_family(family_id,utc_year,ny_hour,ny_weekday,rv_context,tick_context,targets15,targets60):
    folds15={f:evaluate_family_fold(family_id,f,utc_year,ny_hour,ny_weekday,rv_context,tick_context,targets15["rv"],targets15["tick"]) for f in ALL_FOLDS}
    pooled15={c:pooled_comparison(folds15,c) for c in ("vs_vol","vs_tick")}
    sparse15=any(folds15[f]["sparse_states"] for f in PRIMARY_FOLDS)
    status=adjudicate_candidate(folds15,pooled15,sparse15)

    folds60={f:evaluate_family_fold(family_id,f,utc_year,ny_hour,ny_weekday,rv_context,tick_context,targets60["rv"],targets60["tick"]) for f in ALL_FOLDS}
    pooled60={c:pooled_comparison(folds60,c) for c in ("vs_vol","vs_tick")}
    return {
        "candidate_id":family_id,
        "scientific_status":status,
        "primary_15m":folds15,
        "pooled_primary_15m":pooled15,
        "secondary_60m":folds60,
        "pooled_secondary_60m":pooled60,
        "sparse_guard_triggered":sparse15,
    }

def main():
    ap=argparse.ArgumentParser(description="CR2 N0 bounded regime-candidate synthesis")
    ap.add_argument("--repo-root",required=True)
    ap.add_argument("--ap0-root",required=True)
    ap.add_argument("--ap0-manifest",required=True)
    ap.add_argument("--context-json",required=True)
    ap.add_argument("--cr1-evidence-json",required=True)
    ap.add_argument("--cr2-registry-json",required=True)
    ap.add_argument("--output",default=str(Path(tempfile.gettempdir())/"ATDS-CR2-REGIME-CANDIDATE-SYNTHESIS.json"))
    args=ap.parse_args()

    repo_raw=Path(args.repo_root).expanduser(); root_raw=Path(args.ap0_root).expanduser()
    manifest_raw=Path(args.ap0_manifest).expanduser(); ctx_raw=Path(args.context_json).expanduser()
    cr1ev_raw=Path(args.cr1_evidence_json).expanduser(); reg_raw=Path(args.cr2_registry_json).expanduser()
    output_raw=Path(args.output).expanduser()

    if os.path.lexists(output_raw):
        print("BLOCKED_CR2_OUTPUT_EXISTS"); print(output_raw); return 2
    for raw,label in ((repo_raw,"repo-root"),(root_raw,"AP0 root"),(manifest_raw,"AP0 manifest"),(ctx_raw,"Context"),(cr1ev_raw,"CR1 evidence"),(reg_raw,"CR2 registry"),(output_raw.parent,"output parent")):
        if path_chain_has_reparse_or_symlink(raw):
            print("BLOCKED_CR2_REPARSE"); print(f"{label}: {raw}"); return 2

    repo_root=repo_raw.resolve(strict=False); root=root_raw.resolve(strict=False); manifest_path=manifest_raw.resolve(strict=False)
    ctx_path=ctx_raw.resolve(strict=False); cr1ev_path=cr1ev_raw.resolve(strict=False); reg_path=reg_raw.resolve(strict=False); output=output_raw.resolve(strict=False)

    def block(code,reason):
        payload={"schema":"ATDS_CR2_BLOCKED_V0_1","status":code,"reason":reason}
        try:
            if not output.exists(): write_json_exclusive(output,payload)
        except Exception: pass
        print(code); print(reason); print(f"Report: {output}"); return 2

    try:
        if not repo_root.is_dir() or not root.is_dir() or not manifest_path.is_file(): raise RuntimeError("required input missing")
        if output==root or is_within(output,root): raise RuntimeError("output inside AP0 input")
        if sha256_path(manifest_path)!=EXPECTED_AP0_MANIFEST_SHA256: raise RuntimeError("AP0 manifest SHA mismatch")

        cr1=load_cr1_module(repo_root)
        bound_ctx=resolve_bound_file(repo_root,EXPECTED_CONTEXT_PATH,sha256=EXPECTED_CONTEXT_SHA256)
        bound_ev=resolve_bound_file(repo_root,EXPECTED_CR1_EVIDENCE_PATH,git_blob=EXPECTED_CR1_EVIDENCE_BLOB)
        bound_reg=resolve_bound_file(repo_root,EXPECTED_CR2_REGISTRY_PATH,git_blob=EXPECTED_CR2_REGISTRY_BLOB)
        if ctx_path!=bound_ctx or cr1ev_path!=bound_ev or reg_path!=bound_reg:
            raise RuntimeError("CR2 governance input path mismatch")

        ctx=json.loads(ctx_path.read_text(encoding="utf-8")); ev=json.loads(cr1ev_path.read_text(encoding="utf-8")); reg=json.loads(reg_path.read_text(encoding="utf-8"))
        validate_context(ctx); validate_cr1_evidence(ev); validate_cr2_registry(reg)

        manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("status")!="AP0_COMPLETE" or manifest.get("output_identity")!=EXPECTED_AP0_IDENTITY: raise RuntimeError("AP0 identity/status mismatch")
        files=manifest.get("files"); cov=manifest.get("coverage") or {}
        if not isinstance(files,list) or len(files)!=EXPECTED_FILES: raise RuntimeError("AP0 file count mismatch")
        if cov.get("minute_rows_written")!=EXPECTED_MINUTES or cov.get("source_ticks_read")!=EXPECTED_SOURCE_TICKS or cov.get("segments")!=EXPECTED_SEGMENTS: raise RuntimeError("AP0 coverage mismatch")

        import numpy as np, pyarrow as pa, pyarrow.parquet as pq
        chunks={k:[] for k in ("minute","tick","seg","close")}; rows=0; ticks=0; previous=None
        for rec in files:
            rel=rec["relative_path"]; p=cr1.resolve_manifest_member(root,rel)
            if int(p.stat().st_size)!=int(rec["size_bytes"]) or sha256_path(p)!=rec["sha256"]: raise RuntimeError(f"AP0 identity mismatch: {rel}")
            pf=pq.ParquetFile(p)
            if int(pf.metadata.num_rows)!=int(rec["rows"]): raise RuntimeError(f"AP0 rows mismatch: {rel}")
            meta=pf.schema_arrow.metadata or {}
            if meta.get(b"dataset_identity")!=EXPECTED_AP0_IDENTITY.encode() or meta.get(b"volumes_used")!=b"false": raise RuntimeError(f"AP0 metadata mismatch: {rel}")
            table=pf.read(columns=READ_COLUMNS,use_threads=False)
            if table.column_names!=READ_COLUMNS: raise RuntimeError("CR2 column scope violation")
            vals={
                "minute":table["minute_start_ms_utc"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64,copy=False),
                "tick":table["tick_count"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64,copy=False),
                "seg":table["segment_id"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64,copy=False),
                "close":table["mid_close"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64,copy=False),
            }
            n=len(vals["minute"])
            if n==0 or any(len(v)!=n for v in vals.values()): raise RuntimeError("decoded row mismatch")
            if np.any(np.diff(vals["minute"])<=0) or np.any(vals["tick"]<=0) or np.any(~np.isfinite(vals["close"])) or np.any(vals["close"]<=0): raise RuntimeError("AP0 array invariant violation")
            if previous is not None and (int(vals["minute"][0])<=previous[0] or int(vals["seg"][0])-previous[1] not in (0,1)): raise RuntimeError("global AP0 boundary violation")
            if np.any(np.diff(vals["seg"])<0) or np.any(np.diff(vals["seg"])>1): raise RuntimeError("segment jump violation")
            previous=(int(vals["minute"][-1]),int(vals["seg"][-1]))
            rows+=n; ticks+=int(np.sum(vals["tick"],dtype=np.int64))
            for k,v in vals.items(): chunks[k].append(v.copy())
            if sha256_path(p)!=rec["sha256"]: raise RuntimeError(f"AP0 changed during CR2: {rel}")
        if rows!=EXPECTED_MINUTES or ticks!=EXPECTED_SOURCE_TICKS: raise RuntimeError("CR2 coverage mismatch")
        a={k:np.concatenate(v) for k,v in chunks.items()}
        if int(a["seg"][0])!=0 or int(a["seg"][-1])!=EXPECTED_SEGMENTS-1: raise RuntimeError("segment coverage mismatch")

        signed,valid=cr1.signed_return_1m_bps(a["minute"],a["seg"],a["close"])
        rv15=cr1.rolling_realized_vol_bps(signed,valid,a["minute"],a["seg"],15)
        rv60=cr1.rolling_realized_vol_bps(signed,valid,a["minute"],a["seg"],60)
        tick5=cr1.trailing_mean(a["tick"],a["minute"],a["seg"],5)
        fwd_rv15=cr1.forward_from_endpoint(rv15,a["minute"],a["seg"],15)
        fwd_rv60=cr1.forward_from_endpoint(rv60,a["minute"],a["seg"],60)
        fwd_tick15=cr1.forward_mean(a["tick"],a["minute"],a["seg"],15)
        fwd_tick60=cr1.forward_mean(a["tick"],a["minute"],a["seg"],60)
        ny_hour,ny_weekday,utc_year=cr1.time_dimensions(a["minute"])

        rv_rel=make_relative_by_fold(cr1,rv15,ny_hour,utc_year)
        tick_rel=make_relative_by_fold(cr1,tick5,ny_hour,utc_year)
        rv_context={"abs":rv15,"rel_by_fold":rv_rel}; tick_context={"rel_by_fold":tick_rel}
        targets15={"rv":fwd_rv15,"tick":fwd_tick15}; targets60={"rv":fwd_rv60,"tick":fwd_tick60}

        candidates=[evaluate_family(fid,utc_year,ny_hour,ny_weekday,rv_context,tick_context,targets15,targets60) for fid in EXPECTED_FAMILIES]
        payload={
            "schema":"ATDS_CR2_REGIME_CANDIDATE_SYNTHESIS_V0_1",
            "status":"CR2_COMPLETE",
            "research_class":"N0_EXPLORATORY_PREVIOUSLY_EXPOSED_CORPUS",
            "context_id":EXPECTED_CONTEXT_ID,
            "binding":{
                "ap0_manifest_sha256":EXPECTED_AP0_MANIFEST_SHA256,
                "ap0_files_rehashed":EXPECTED_FILES,
                "cr1_helper_git_blob":EXPECTED_CR1_HELPER_BLOB,
                "cr1_evidence_git_blob":EXPECTED_CR1_EVIDENCE_BLOB,
                "cr2_registry_git_blob":EXPECTED_CR2_REGISTRY_BLOB,
            },
            "coverage":{"minute_rows":rows,"source_ticks_accounted":ticks,"segments":EXPECTED_SEGMENTS},
            "fold_contract":{"primary_folds":list(PRIMARY_FOLDS),"diagnostic_fold":"D2026","pristine_oos":False},
            "score_contract":{"target_classes":25,"laplace_alpha":ALPHA,"sparse_min_test_per_joint_state":SPARSE_MIN_TEST},
            "scope":SCOPE,
            "candidates":candidates,
            "runtime":{"numpy_version":np.__version__,"pyarrow_version":pa.__version__},
        }
        write_json_exclusive(output,payload)
        print("CR2_COMPLETE")
        print(f"Minute rows: {rows}")
        print(f"Source ticks accounted: {ticks}")
        for c in candidates:
            print(f"{c['candidate_id']}: {c['scientific_status']}")
        print(f"Report: {output}")
        return 0
    except Exception as exc:
        return block("BLOCKED_CR2_RUNTIME",str(exc))

if __name__=="__main__":
    raise SystemExit(main())
