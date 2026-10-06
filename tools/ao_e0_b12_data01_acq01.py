from __future__ import annotations
import hashlib, json
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable

CONTRACT = "ATDS_AO_E0_B12_DATA01_ACQ01_V0_1"
FORWARD_START_MS = 1791284400000
WARMUP_H1_MAX = 20
REQUIRED_CLOSED_TRADES = 58927
CANDIDATE_DIVISOR = Decimal("1000")
REQUIRED_FINAL_FIELDS = (
    "raw_forward_manifest_sha256","raw_forward_inventory_digest",
    "ap0_forward_manifest_sha256","h1_forward_stream_sha256",
    "exact_first_evidence_decision_time","exact_terminal_decision_time",
    "exact_closed_trade_count","non_overlap_attestation",
)
FORBIDDEN_KEYS = {
    "pnl","expectancy","ci","confidence_interval","win_rate","drawdown",
    "support","refute","inconclusive","qualification_result","strategy_qualified",
}
class ACQ01Error(ValueError): pass

def canonical_json_bytes(payload: Any) -> bytes:
    return (json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)+"\n").encode()

def canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()

def reject_performance_surface(payload: Any) -> None:
    if isinstance(payload,dict):
        for k,v in payload.items():
            if str(k).casefold() in FORBIDDEN_KEYS:
                raise ACQ01Error("BLOCKED_PERFORMANCE_PEEK")
            reject_performance_surface(v)
    elif isinstance(payload,(list,tuple)):
        for v in payload: reject_performance_surface(v)

def validate_source_binding(binding: dict[str,Any]) -> dict[str,Any]:
    expected={"candidate_id":"DUKASCOPY_USATECH_FORWARD_CANDIDATE_V0_1","provider":"DUKASCOPY",
              "instrument":"USATECH.IDX/USD","symbol":"USATECHIDXUSD"}
    if binding != expected: return {"status":"BLOCKED_SOURCE_SUBSTITUTION"}
    return {"status":"PASS_SOURCE_BINDING"}

def validate_cost_gate(*,requester_pays: bool,human_spend_authorized: bool) -> dict[str,Any]:
    if requester_pays and not human_spend_authorized:
        return {"status":"BLOCKED_REQUESTER_PAYS_HUMAN_AUTHORIZATION_REQUIRED"}
    return {"status":"PASS_COST_GATE"}

def validate_forward_boundary(*,first_evidence_ms:int,warmup_h1_bars:int,warmup_in_evidence:bool) -> dict[str,Any]:
    if int(first_evidence_ms) != FORWARD_START_MS: return {"status":"BLOCKED_WRONG_FORWARD_START"}
    if not (0 <= int(warmup_h1_bars) <= WARMUP_H1_MAX): return {"status":"BLOCKED_WARMUP_SCOPE"}
    if warmup_in_evidence: return {"status":"BLOCKED_WARMUP_INCLUDED_AS_EVIDENCE"}
    return {"status":"PASS_FORWARD_BOUNDARY"}

def seal_raw_object(raw: bytes, prior: dict[str,Any] | None=None) -> dict[str,Any]:
    digest=hashlib.sha256(raw).hexdigest(); size=len(raw)
    if prior is not None:
        if prior.get("sha256")==digest and int(prior.get("size_bytes",-1))==size:
            return {"status":"PASS_REPRODUCIBILITY_DUPLICATE","sha256":digest,"size_bytes":size}
        return {"status":"BLOCKED_SOURCE_OBJECT_MUTATION","sha256":digest,"size_bytes":size}
    return {"status":"PASS_NEW_RAW_OBJECT","sha256":digest,"size_bytes":size}

def _norm_ref(row:dict[str,Any]) -> tuple[int,Decimal,Decimal]:
    return int(row["timestamp"]),Decimal(str(row["bid_price"])),Decimal(str(row["ask_price"]))

def _norm_candidate(row:dict[str,Any]) -> tuple[int,Decimal,Decimal]:
    ts=int(row["timestamp"])
    if "raw_bid" in row and "raw_ask" in row:
        bid=Decimal(str(row["raw_bid"]))/CANDIDATE_DIVISOR
        ask=Decimal(str(row["raw_ask"]))/CANDIDATE_DIVISOR
    else:
        bid=Decimal(str(row["bid_price"])); ask=Decimal(str(row["ask_price"]))
    return ts,bid,ask

def assess_exact_overlap(reference_rows:Iterable[dict[str,Any]],candidate_rows:Iterable[dict[str,Any]]) -> dict[str,Any]:
    ref=[_norm_ref(x) for x in reference_rows]; cand=[_norm_candidate(x) for x in candidate_rows]
    if any(ref[i][0] >= ref[i+1][0] for i in range(len(ref)-1)): return {"status":"BLOCKED_REFERENCE_ORDER"}
    if any(cand[i][0] >= cand[i+1][0] for i in range(len(cand)-1)): return {"status":"BLOCKED_CANDIDATE_ORDER"}
    r={x[0]:x[1:] for x in ref}; c={x[0]:x[1:] for x in cand}
    timestamps=sorted(set(r)|set(c))
    tm=sum(1 for t in timestamps if t not in r or t not in c)
    bm=am=0
    for t in set(r)&set(c):
        bm += int(r[t][0] != c[t][0]); am += int(r[t][1] != c[t][1])
    status="PASS_EXACT_SOURCE_CONTINUATION" if (tm,bm,am)==(0,0,0) else "BLOCKED_SOURCE_CONTINUATION_NOT_EXACT"
    return {"status":status,"timestamp_mismatch_count":tm,"bid_mismatch_count":bm,"ask_mismatch_count":am,
            "reference_rows":len(ref),"candidate_rows":len(cand)}

def validate_rolling_state(state:dict[str,Any]) -> dict[str,Any]:
    reject_performance_surface(state)
    if state.get("b12") != "CLOSED": return {"status":"BLOCKED_AUTHORITY_BOUNDARY"}
    if state.get("pipe01_first_read_invoked"): return {"status":"BLOCKED_AUTHORITY_BOUNDARY"}
    n=int(state.get("exact_closed_trade_count",0))
    if n < REQUIRED_CLOSED_TRADES:
        if state.get("data01_state")=="READY" or state.get("instance_digest") not in (None,"NOT_YET_AVAILABLE"):
            return {"status":"BLOCKED_PREMATURE_READY"}
        return {"status":"WAIT_NOT_READY_NO_PERFORMANCE_OBSERVATION","closed_trade_count":n}
    return {"status":"BLOCKED_FINAL_INSTANCE_REQUIRES_SEPARATE_COUNT_ONLY_READINESS_CONTRACT","closed_trade_count":n}

def build_final_instance_digest(_:dict[str,Any]) -> str:
    raise ACQ01Error("BLOCKED_FINAL_INSTANCE_OUT_OF_SCOPE")

def validate_local_store_paths(root:Path) -> dict[str,Any]:
    expected={"raw","manifests","evidence","ap0","h1"}
    actual={p.name for p in root.iterdir() if p.is_dir()} if root.exists() else set()
    return {"status":"PASS_STORE_LAYOUT" if expected <= actual else "BLOCKED_STORE_LAYOUT","missing":sorted(expected-actual)}
