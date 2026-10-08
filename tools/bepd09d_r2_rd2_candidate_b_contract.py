from __future__ import annotations
import hashlib, json, math
from typing import Any

FLOAT64_EPSILON = 2.220446049250313e-16
TAU_RELATIVE = math.sqrt(FLOAT64_EPSILON)
TAU_DERIVATION_CONTRACT_BLOB = "bd89123221cdf2f9dc852a5aadfed1186eab3d4f"

EXPECTED_SOLVER = "Newton-CG"
EXPECTED_MODEL_ID = "BEPD09B_R1_C1_UNREGULARIZED_BINARY_LOGISTIC"
EXPECTED_FEATURE_CONTRACT_ID = "BEPD09B_R1_FROZEN_EXPOSURE_SPLINE_PLUS_CONTEXT"
EXPECTED_BINDINGS = {
    "source_runtime_blob": "72645c3201d3d454d4d5402a0e2191e1195c68a6",
    "r2_overlay_blob": "209b3b5b804da4da9ee6751f2a15a32df0e3e4b1",
    "reference_runtime_blob": "2c8a82405082ce3f820b580017a96af77e74b0e4",
    "event_ledger_blob": "0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2",
    "calendar_partition_blob": "7d950d957611cf209d811c788ff10abded30d011",
}

def _finite_number(x: Any) -> bool:
    return isinstance(x, (int, float)) and math.isfinite(float(x))

def _audit_scalar(x: Any) -> Any:
    return float(x) if _finite_number(x) else "NONFINITE_OR_MISSING"

def _finite_vector(xs: Any) -> bool:
    return isinstance(xs, list) and bool(xs) and all(_finite_number(x) for x in xs)

def _finite_matrix(X: Any) -> bool:
    return (
        isinstance(X, list) and bool(X) and
        all(isinstance(r, list) and bool(r) for r in X) and
        len({len(r) for r in X}) == 1 and
        all(_finite_number(v) for r in X for v in r)
    )

def score_scale(X: list[list[float]]) -> float:
    if not _finite_matrix(X):
        raise ValueError("NONFINITE_OR_INVALID_INPUT")
    ncols = len(X[0])
    col_abs_sums = [sum(abs(float(row[j])) for row in X) for j in range(ncols)]
    return max(1.0, max(col_abs_sums))

def tau_score(X: list[list[float]]) -> float:
    return TAU_RELATIVE * score_scale(X)

def evaluate(packet: dict[str, Any]) -> dict[str, Any]:
    X = packet.get("X")
    gates: dict[str, bool] = {}

    gates["FINITE_INPUT"] = _finite_matrix(X)
    gates["FINITE_PARAMETERS"] = _finite_vector(packet.get("parameters"))
    gates["FINITE_OBJECTIVE"] = _finite_number(packet.get("objective"))
    gates["FINITE_SCORE"] = _finite_number(packet.get("score_inf_norm"))
    gates["FINITE_DERIVATIVES"] = bool(packet.get("derivatives_finite") is True)
    gates["FULL_REQUIRED_DESIGN_RANK"] = bool(packet.get("full_required_design_rank") is True)
    gates["NO_PERFECT_SEPARATION"] = bool(packet.get("perfect_separation") is False)
    gates["NOT_ONE_CLASS"] = bool(packet.get("one_class_sample") is False)

    tau = tau_score(X) if gates["FINITE_INPUT"] else None
    gates["SCORE_INF_NORM_LTE_TAU_SCORE"] = bool(
        tau is not None and gates["FINITE_SCORE"] and float(packet["score_inf_norm"]) <= tau
    )
    gates["EXPECTED_SOLVER"] = packet.get("solver") == EXPECTED_SOLVER
    gates["EXPECTED_MODEL"] = packet.get("model_id") == EXPECTED_MODEL_ID
    gates["EXPECTED_FEATURE_SET"] = packet.get("feature_contract_id") == EXPECTED_FEATURE_CONTRACT_ID
    gates["EXPECTED_DATA_BINDING"] = packet.get("bindings") == EXPECTED_BINDINGS
    gates["EXPECTED_TAU_DERIVATION_CONTRACT"] = packet.get("tau_contract_blob") == TAU_DERIVATION_CONTRACT_BLOB

    registered_state = packet.get("registered_state", True) is True
    all_pass = registered_state and all(gates.values())
    verdict = "ACCEPT" if all_pass else ("FAIL_CLOSED" if not registered_state else "REJECT")

    optimizer_metadata = {
        "success": packet.get("optimizer_success"),
        "status": packet.get("optimizer_status"),
        "message": packet.get("optimizer_message"),
        "binding_role": "NON_BINDING_DIAGNOSTIC",
    }
    receipt_core = {
        "verdict": verdict,
        "gates": gates,
        "score_scale": (tau / TAU_RELATIVE) if tau is not None else None,
        "tau_relative": TAU_RELATIVE,
        "tau_score": tau,
        "score_inf_norm": _audit_scalar(packet.get("score_inf_norm")),
        "optimizer_metadata": optimizer_metadata,
        "reference_metadata": packet.get("reference_metadata"),
    }
    identity = hashlib.sha256(
        json.dumps(receipt_core, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()
    return {**receipt_core, "receipt_identity": identity}
