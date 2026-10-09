"""BEPD-09D-R2-RD5 synthetic-only training adapter.

This module is NOT a real ledger reader or real run protocol.
It may never open or select rows from the real historical corpus.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from copy import deepcopy

import numpy as np
from scipy.optimize import linprog as _linprog
from scipy.special import expit

import bepd09c_reference as reference
import bepd09d_r2_rd2_candidate_b_contract as numerical_contract
import bepd09d_r2_rd3_candidate_b_runtime as candidate
import bepd09d_r2_rd5_synthetic_fixture as fixture

REAL_EXECUTION_PATH_ACTIVATION = False
REFERENCE_ROLE = "INDEPENDENT_NUMERICAL_CONSISTENCY_CHECK_ONLY"
EXPECTED_CONTRACT_IDENTITY = "2122aac53d03370df9f76a0ddae880fd9bf6dcaa"
EXPECTED_CANDIDATE_RUNTIME_BLOB = "38588b0a0b9c5b4cb9fcee0c7d524e63d5039c69"
ALLOWLIST = frozenset({
    "fold_id", "model_role", "train_block_ids", "training_row_count",
    "training_class_counts", "source_and_contract_identities", "solver_identity",
    "optimizer_audit_metadata", "score_inf_norm", "score_scale",
    "tau_relative", "tau_score", "mathematical_gate_statuses",
    "verdict", "reference_status", "receipt_identity", "stop_reason",
})
MAX_SYNTHETIC_ROWS = 2000

class TrainingOnlyBreaker(RuntimeError):
    """Bounded synthetic-only fail-closed violation."""

def _stop(code):
    raise TrainingOnlyBreaker(str(code))

def safe_receipt(obj):
    """Deny unknown public fields; never serialize raw X/y or parameter vectors."""
    if type(obj) is not dict or set(obj) != ALLOWLIST:
        _stop("OUTPUT_ALLOWLIST_VIOLATION")
    try:
        copy = json.loads(json.dumps(obj, allow_nan=False, sort_keys=True,
                                     separators=(",", ":"), ensure_ascii=True))
    except (ValueError, TypeError, OverflowError):
        _stop("UNSERIALIZABLE_OR_NONFINITE_OUTPUT")
    if type(copy.get("source_and_contract_identities")) is not dict:
        _stop("RECEIPT_IDENTITY_NOT_REGISTERED")
    return copy

def _receipt(*, fold_id, role, train_blocks, n, cls, verdict,
             optimizer=None, gates=None, score=None, scale=None, tau=None,
             reference_status="UNADJUDICATED", reason=None):
    body = {
        "fold_id": fold_id,
        "model_role": role,
        "train_block_ids": list(train_blocks),
        "training_row_count": int(n),
        "training_class_counts": {"0": int(cls[0]), "1": int(cls[1])},
        "source_and_contract_identities": {
            "input_provenance": fixture.PROVENANCE,
            "rd4_closure_blob": EXPECTED_CONTRACT_IDENTITY,
            "candidate_runtime_blob": EXPECTED_CANDIDATE_RUNTIME_BLOB,
            "calendar_partition_blob": "7d950d957611cf209d811c788ff10abded30d011",
        },
        "solver_identity": "Newton-CG" if role != "PRECHECK_ONLY" else "NOT_RUN",
        "optimizer_audit_metadata": optimizer,
        "score_inf_norm": score,
        "score_scale": scale,
        "tau_relative": numerical_contract.TAU_RELATIVE if role != "PRECHECK_ONLY" else None,
        "tau_score": tau,
        "mathematical_gate_statuses": gates or {},
        "verdict": verdict,
        "reference_status": reference_status,
        "stop_reason": reason,
    }
    serial = json.dumps(body, allow_nan=False, sort_keys=True,
                        separators=(",", ":"), ensure_ascii=True)
    body["receipt_identity"] = hashlib.sha256(serial.encode("ascii")).hexdigest()
    return safe_receipt(body)

def _identity_gate(fold_id, rows, provenance, perform_fit, contract_identity):
    if candidate.REAL_EXECUTION_PATH_ACTIVATION is not False:
        _stop("CANDIDATE_RUNTIME_REAL_ACTIVATION")
    if callable(candidate.run_protocol):
        _stop("CANDIDATE_RUN_PROTOCOL_ACTIVE")
    if provenance != fixture.PROVENANCE:
        _stop("SYNTHETIC_PROVENANCE_REQUIRED")
    if contract_identity != EXPECTED_CONTRACT_IDENTITY:
        _stop("RD4_CLOSURE_IDENTITY_MISMATCH")
    if type(fold_id) is not int or fold_id not in fixture.FOLDS:
        _stop("INVALID_FOLD")
    if type(perform_fit) is not bool:
        _stop("INVALID_EXECUTION_MODE")
    if type(rows) is not list or not rows or len(rows) > MAX_SYNTHETIC_ROWS:
        _stop("INVALID_SYNTHETIC_VIEW_SIZE")
    if tuple(map(len, fixture.BLOCKS.values())) != (44, 43, 43, 43, 43, 43):
        _stop("CALENDAR_BLOCK_IDENTITY_MISMATCH")
    if len(fixture.WEEKS) != 259 or fixture.WEEKS[0] != "2021-06-07" or fixture.WEEKS[-1] != "2026-05-18":
        _stop("CALENDAR_WEEK_BOUNDARY_MISMATCH")
    train_weeks, test_weeks = fixture.FOLDS[fold_id]
    if set(train_weeks) & set(test_weeks):
        _stop("TRAIN_TEST_FOLD_BOUNDARY_OVERLAP")
    allow = set(train_weeks)
    event_ids = set()
    cluster_week = {}
    for row in rows:
        if type(row) is not dict or set(row) != fixture.KEYS:
            _stop("INVALID_EXACT_ROW_SCHEMA")
        if row["target_week_id"] not in allow:
            _stop("CURRENT_FOLD_TEST_OR_UNREGISTERED_WEEK")
        for k in ("event_id", "sweep_cluster_id"):
            ident = row[k]
            if type(ident) is not str or len(ident) != 64:
                _stop("INVALID_EVENT_OR_CLUSTER_IDENTITY")
            try: int(ident, 16)
            except (TypeError, ValueError): _stop("INVALID_HEX_IDENTITY")
        if row["event_id"] in event_ids:
            _stop("DUPLICATE_EVENT_ID")
        event_ids.add(row["event_id"])
        cluster = row["sweep_cluster_id"]
        week = row["target_week_id"]
        if cluster in cluster_week and cluster_week[cluster] != week:
            _stop("CLUSTER_WEEK_MISMATCH")
        cluster_week[cluster] = week
        if type(row["same_week_reintegration"]) is not bool:
            _stop("INVALID_RESPONSE_TYPE")
    return train_weeks

def _independent_lp_guard(X, y):
    """Strict tri-state LP proof. Unknown solver status always aborts."""
    signs = np.where(y > 0.5, 1.0, -1.0)
    try:
        r = _linprog(np.zeros(X.shape[1], dtype=float),
            A_ub=-(signs[:, None] * X), b_ub=-np.ones(len(y)),
            bounds=[(None,None)] * X.shape[1], method="highs")
    except Exception:
        _stop("SEPARATION_LP_UNKNOWN_EXCEPTION")
    if int(r.status) == 0 and bool(r.success):
        _stop("PROVEN_PERFECT_SEPARATION")
    if int(r.status) != 2 or bool(r.success):
        _stop("SEPARATION_LP_UNKNOWN_STATUS")
    return True

def _guarded_candidate_fit(X, y):
    """Observe internal swallowed detector exceptions WITHOUT mutating adopted source."""
    prior = sys.gettrace()
    if prior is not None:
        _stop("UNCONTROLLED_RUNTIME_INSTRUMENTATION_CONFLICT")
    failures = []
    target_code = candidate.perfect_separation.__code__
    def observe(frame, event, arg):
        if event == "exception" and frame.f_code is target_code:
            failures.append("CANDIDATE_INTERNAL_SEPARATION_EXCEPTION")
        return observe
    try:
        sys.settrace(observe)
        result = candidate.fit_logistic_candidate_b(X, y)
    except Exception:
        _stop("CANDIDATE_FITTER_EXCEPTION")
    finally:
        sys.settrace(prior)
    if failures:
        _stop("CANDIDATE_INTERNAL_SEPARATION_UNKNOWN_OR_MASKED")
    return result

def execute_synthetic_fold(*, fold_id, rows, provenance, perform_fit=False,
                           contract_identity=EXPECTED_CONTRACT_IDENTITY):
    """Consume only supplied, already scoped SYNTHETIC training rows."""
    train_weeks = _identity_gate(fold_id, rows, provenance, perform_fit, contract_identity)
    try:
        prepared = candidate.validate_rows(rows, list(fixture.WEEKS))
        classes = (sum(r["y"] == 0.0 for r in prepared),
                   sum(r["y"] == 1.0 for r in prepared))
        if not all(classes):
            _stop("ONE_CLASS_TRAINING_FOLD")
        stats = candidate._stats(prepared)
        Xb, Xc = candidate._mats(prepared, stats)
        y = np.asarray([r["y"] for r in prepared], dtype=np.float64)
        if Xb.ndim != 2 or Xc.ndim != 2 or Xb.shape[0] != len(y) or Xc.shape[0] != len(y):
            _stop("DESIGN_DIMENSIONS_INVALID")
        if Xb.shape[1] != 5 or Xc.shape[1] != 9:
            _stop("FROZEN_FEATURE_SET_MISMATCH")
        for X in (Xb,Xc):
            if not np.all(np.isfinite(X)):
                _stop("NONFINITE_TRAINING_DESIGN")
            if perform_fit and np.linalg.matrix_rank(X) != X.shape[1]:
                _stop("RANK_DEFICIENT_TRAINING_DESIGN")
            _independent_lp_guard(X,y)
    except TrainingOnlyBreaker:
        raise
    except Exception:
        _stop("FROZEN_SCIENCE_OR_INPUT_PREPARATION_FAILED")
    blocks = [f"B{j}" for j in range(1,fold_id+1)]
    if not perform_fit:
        return _receipt(fold_id=fold_id, role="PRECHECK_ONLY", train_blocks=blocks,
            n=len(prepared), cls=classes, verdict="STATIC_SYNTHETIC_PRECHECK_PASS",
            gates={"EXACT_TRAINING_FOLD_SCOPE":True,"FROZEN_MODEL_MATRICES":True,
                   "INDEPENDENT_SEPARATION_LP_PROOF":True})
    outputs=[]
    for role,X in (("BASELINE",Xb),("CONTEXT",Xc)):
        _independent_lp_guard(X,y)
        result = _guarded_candidate_fit(X,y)
        _independent_lp_guard(X,y)
        if result.get("final_acceptance_verdict") != "ACCEPT":
            _stop("CANDIDATE_B_NUMERICAL_FIT_NOT_ACCEPTED")
        gates = result.get("contract_receipt",{}).get("gates",{})
        if type(gates) is not dict or not gates or not all(v is True for v in gates.values()):
            _stop("CANDIDATE_B_NUMERICAL_GATE_FAILURE")
        # Never expose parameters, raw X/y, training matrices or predictions.
        outputs.append(_receipt(fold_id=fold_id, role=role, train_blocks=blocks,
            n=len(prepared), cls=classes, verdict="ACCEPT",
            optimizer={"success":result.get("optimizer_success"),
                "status":result.get("optimizer_status"),
                "message":result.get("optimizer_message")},
            gates=deepcopy(gates), score=float(result["score_inf_norm"]),
            scale=float(result["score_scale"]), tau=float(result["tau_score"]),
            reference_status="UNADJUDICATED_NOT_EXECUTED"))
    return outputs

def synthetic_reference_probe():
    """One bounded independent training-only reference fit; no test rows or scoring."""
    X = np.array([[1.,-1.],[1.,0.],[1.,1.],[1.,2.]],dtype=float)
    y = np.array([0.,1.,0.,1.],dtype=float)
    try:
        b = reference._fit(X,y)
        independent_score = X.T @ (expit(X @ b) - y)
        stationarity = bool(np.max(np.abs(independent_score)) <= numerical_contract.tau_score(X.tolist()))
    except Exception:
        _stop("SYNTHETIC_REFERENCE_NUMERICAL_FAILURE")
    if not stationarity:
        _stop("SYNTHETIC_REFERENCE_STATIONARITY_GATE_FAILED")
    return {"reference_role":REFERENCE_ROLE, "stationarity_gate":stationarity,
            "comparison_parity":"UNADJUDICATED_NOT_EXECUTED"}
