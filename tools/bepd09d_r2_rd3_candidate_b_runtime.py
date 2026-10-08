from __future__ import annotations

import math
from types import SimpleNamespace
from typing import Any

import numpy as np
from scipy.optimize import linprog, minimize

import bepd09d_r2_runtime as legacy
import bepd09d_r2_rd2_candidate_b_contract as contract

SOURCE_RUNTIME_BLOB = "72645c3201d3d454d4d5402a0e2191e1195c68a6"
R2_RUNTIME_BLOB = "209b3b5b804da4da9ee6751f2a15a32df0e3e4b1"
TAU_CONTRACT_BLOB = "bd89123221cdf2f9dc852a5aadfed1186eab3d4f"
ACCEPTANCE_CONTRACT_BLOB = "ccb519aad05cf0739b54ee50e0521a85a5374f13"
BREAKER_CONTRACT_BLOB = "028b7fbba56b2bb4f9abd44c5ff075b9bdb80d9a"
RD2_CANDIDATE_CONTRACT_BLOB = "0e87aa62433218b44f8ddaf64351ed0beccd93a3"

SOLVER = "Newton-CG"
MAX_ITER = 5000
XTOL = 1e-10
INITIALIZATION = "ZERO_VECTOR"
REAL_EXECUTION_PATH_ACTIVATION = False
run_protocol = None

MODEL_ID = contract.EXPECTED_MODEL_ID
FEATURE_CONTRACT_ID = contract.EXPECTED_FEATURE_CONTRACT_ID
EXPECTED_BINDINGS = dict(contract.EXPECTED_BINDINGS)

# Re-export unchanged scientific/model-construction helpers for parity checks only.
validate_rows = legacy.validate_rows
validate_fold_integrity = legacy.validate_fold_integrity
partition_calendar = legacy.partition_calendar
exposure_values = legacy.exposure_values
spline_basis = legacy.spline_basis
_stats = legacy._stats
_mats = legacy._mats
_sig = legacy._sig
_score = legacy._score

class CandidateBImplementationError(RuntimeError):
    pass

def _as_arrays(X: Any, y: Any):
    Xa = np.asarray(X, dtype=float)
    ya = np.asarray(y, dtype=float)
    return Xa, ya

def objective(X, y, b):
    X, y = _as_arrays(X, y)
    b = np.asarray(b, dtype=float)
    z = X @ b
    return float(np.sum(np.logaddexp(0, z) - y * z))

def gradient(X, y, b):
    X, y = _as_arrays(X, y)
    b = np.asarray(b, dtype=float)
    z = X @ b
    p = np.where(z >= 0, 1 / (1 + np.exp(-z)), np.exp(z) / (1 + np.exp(z)))
    return X.T @ (p - y)

def hessian(X, y, b):
    X, y = _as_arrays(X, y)
    b = np.asarray(b, dtype=float)
    z = X @ b
    p = np.where(z >= 0, 1 / (1 + np.exp(-z)), np.exp(z) / (1 + np.exp(z)))
    w = p * (1 - p)
    return X.T @ (X * w[:, None])

def perfect_separation(X, y):
    X, y = _as_arrays(X, y)
    if X.ndim != 2 or y.ndim != 1 or len(X) != len(y) or len(y) == 0:
        return False
    signs = np.where(y > 0.5, 1.0, -1.0)
    sep = linprog(
        np.zeros(X.shape[1]),
        A_ub=-(signs[:, None] * X),
        b_ub=-np.ones(len(y)),
        bounds=[(None, None)] * X.shape[1],
        method="highs",
    )
    return bool(sep.success)

def _finite_derivatives(X, y, b):
    try:
        g = gradient(X, y, b)
        H = hessian(X, y, b)
        return bool(np.all(np.isfinite(g)) and np.all(np.isfinite(H)))
    except Exception:
        return False

def _safe_objective(X, y, b):
    try:
        v = objective(X, y, b)
        return v if math.isfinite(v) else float("nan")
    except Exception:
        return float("nan")

def _safe_score(X, y, b):
    try:
        g = gradient(X, y, b)
        if not np.all(np.isfinite(g)):
            return float("nan")
        return float(np.max(np.abs(g)))
    except Exception:
        return float("nan")

def build_packet(
    X,
    y,
    optimizer_result,
    *,
    registered_state=True,
    solver=SOLVER,
    model_id=MODEL_ID,
    feature_contract_id=FEATURE_CONTRACT_ID,
    bindings=None,
    tau_contract_blob=contract.TAU_DERIVATION_CONTRACT_BLOB,
    reference_metadata=None,
):
    Xa, ya = _as_arrays(X, y)
    params = np.asarray(getattr(optimizer_result, "x", []), dtype=float)
    rank_ok = bool(Xa.ndim == 2 and Xa.shape[1] > 0 and np.linalg.matrix_rank(Xa) == Xa.shape[1])
    one_class = bool(ya.ndim == 1 and len(ya) > 0 and len(set(ya.tolist())) < 2)
    sep = False
    if Xa.ndim == 2 and ya.ndim == 1 and len(Xa) == len(ya) and len(ya) > 0 and not one_class:
        try:
            sep = perfect_separation(Xa, ya)
        except Exception:
            sep = False
    packet = {
        "X": Xa.tolist() if Xa.ndim == 2 else [],
        "parameters": params.tolist(),
        "objective": _safe_objective(Xa, ya, params),
        "score_inf_norm": _safe_score(Xa, ya, params),
        "derivatives_finite": _finite_derivatives(Xa, ya, params),
        "full_required_design_rank": rank_ok,
        "perfect_separation": sep,
        "one_class_sample": one_class,
        "solver": solver,
        "model_id": model_id,
        "feature_contract_id": feature_contract_id,
        "bindings": dict(EXPECTED_BINDINGS if bindings is None else bindings),
        "tau_contract_blob": tau_contract_blob,
        "optimizer_success": getattr(optimizer_result, "success", None),
        "optimizer_status": getattr(optimizer_result, "status", None),
        "optimizer_message": str(getattr(optimizer_result, "message", "")),
        "registered_state": registered_state,
        "reference_metadata": reference_metadata,
    }
    return packet

def evaluate_fit_state(packet):
    return contract.evaluate(packet)

def evaluate_optimizer_result(X, y, optimizer_result, **overrides):
    packet = build_packet(X, y, optimizer_result, **overrides)
    receipt = evaluate_fit_state(packet)
    return {
        "solver": SOLVER,
        "max_iter": MAX_ITER,
        "xtol": XTOL,
        "optimizer_success": packet["optimizer_success"],
        "optimizer_status": packet["optimizer_status"],
        "optimizer_message": packet["optimizer_message"],
        "score_inf_norm": packet["score_inf_norm"],
        "score_scale": receipt["score_scale"],
        "tau_relative": receipt["tau_relative"],
        "tau_score": receipt["tau_score"],
        "finite_input": receipt["gates"]["FINITE_INPUT"],
        "finite_parameters": receipt["gates"]["FINITE_PARAMETERS"],
        "finite_objective": receipt["gates"]["FINITE_OBJECTIVE"],
        "finite_score": receipt["gates"]["FINITE_SCORE"],
        "finite_derivatives": receipt["gates"]["FINITE_DERIVATIVES"],
        "full_required_design_rank": receipt["gates"]["FULL_REQUIRED_DESIGN_RANK"],
        "no_perfect_separation": receipt["gates"]["NO_PERFECT_SEPARATION"],
        "not_one_class": receipt["gates"]["NOT_ONE_CLASS"],
        "identity_gates": {
            k: receipt["gates"][k] for k in (
                "EXPECTED_SOLVER","EXPECTED_MODEL","EXPECTED_FEATURE_SET",
                "EXPECTED_DATA_BINDING","EXPECTED_TAU_DERIVATION_CONTRACT"
            )
        },
        "final_acceptance_verdict": receipt["verdict"],
        "receipt_identity": receipt["receipt_identity"],
        "parameters": packet["parameters"],
        "contract_receipt": receipt,
    }

def fit_logistic_candidate_b(X, y):
    X, y = _as_arrays(X, y)
    if X.ndim != 2 or y.ndim != 1 or len(X) != len(y) or len(X) == 0:
        fake = SimpleNamespace(success=False, status="NOT_RUN", message="INVALID_MODEL_INPUT", x=np.zeros(X.shape[1] if X.ndim == 2 else 0))
        return evaluate_optimizer_result(X if X.ndim == 2 else np.empty((0,0)), y if y.ndim == 1 else np.array([]), fake)
    if len(set(y.tolist())) < 2:
        fake = SimpleNamespace(success=False, status="NOT_RUN", message="ONE_CLASS_SAMPLE", x=np.zeros(X.shape[1]))
        return evaluate_optimizer_result(X, y, fake)
    if perfect_separation(X, y):
        fake = SimpleNamespace(success=False, status="NOT_RUN", message="PERFECT_SEPARATION", x=np.zeros(X.shape[1]))
        return evaluate_optimizer_result(X, y, fake)

    def fun(b): return objective(X, y, b)
    def jac(b): return gradient(X, y, b)
    def hess_(b): return hessian(X, y, b)

    res = minimize(
        fun,
        np.zeros(X.shape[1]),
        jac=jac,
        hess=hess_,
        method=SOLVER,
        options={"xtol":XTOL,"maxiter":MAX_ITER,"disp":False},
    )
    return evaluate_optimizer_result(X, y, res)
