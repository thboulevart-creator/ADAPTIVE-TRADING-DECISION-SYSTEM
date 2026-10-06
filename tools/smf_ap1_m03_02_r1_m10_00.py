from __future__ import annotations

import json
import math

CONTRACT = "ATDS_SMF_AP1_M03_02_R1_M10_00_RUNTIME_V0_1"
EXPECTED_REAL_M03_SHA256 = "7d4369cdfab545f0edb94b93ad9d1d1070e6afa35a1000376af55d9c10943a9e"
PRIMARY_YEARS = (2022, 2023, 2024, 2025)
TRANSITIONS = ((2022, 2023), (2023, 2024), (2024, 2025))
METRICS_PROBABILITIES = (
    ("tick_count", (0.5, 0.9, 0.99)),
    ("minute_range", (0.5, 0.9, 0.95, 0.99)),
    ("spread_mean", (0.5, 0.9, 0.95, 0.99)),
)
MATERIALITY_THRESHOLD = 0.20
EPISTEMIC_LIMIT = "EXPLORATORY_DIAGNOSTIC_TEMPORAL_STABILITY_EVIDENCE"

def canonical_json(value) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False)

def require_real_source_identity(observed_sha256: str) -> str:
    if observed_sha256 != EXPECTED_REAL_M03_SHA256:
        raise ValueError("REAL_M03_IDENTITY_MISMATCH")
    return observed_sha256

def _finite(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))

def symmetric_relative_change(q_a: float, q_b: float) -> float | None:
    if not _finite(q_a) or not _finite(q_b):
        raise ValueError("NONFINITE_QUANTILE")
    a = float(q_a)
    b = float(q_b)
    denominator = abs(a) + abs(b)
    if denominator == 0.0:
        return None
    return 2.0 * abs(b - a) / denominator

def classify_contrast(q_a: float, q_b: float) -> dict:
    if not _finite(q_a) or not _finite(q_b):
        return {
            "q_a": q_a,
            "q_b": q_b,
            "r": None,
            "status": "BLOCKED",
            "reason": "NONFINITE_QUANTILE",
        }
    r = symmetric_relative_change(float(q_a), float(q_b))
    if r is None:
        return {
            "q_a": float(q_a),
            "q_b": float(q_b),
            "r": None,
            "status": "BLOCKED",
            "reason": "ZERO_DENOMINATOR",
        }
    return {
        "q_a": float(q_a),
        "q_b": float(q_b),
        "r": r,
        "status": "MATERIAL" if r >= MATERIALITY_THRESHOLD else "NON_MATERIAL",
        "reason": None,
    }

def _quantile_value(bucket_evidence: dict, year: int, metric: str, probability: float):
    key = f"UTC_YEAR:{year}"
    if key not in bucket_evidence:
        return None, "MISSING_YEAR"
    year_payload = bucket_evidence[key]
    if not isinstance(year_payload, dict) or metric not in year_payload:
        return None, "MISSING_METRIC"
    metric_payload = year_payload[metric]
    if not isinstance(metric_payload, dict) or not isinstance(metric_payload.get("quantiles"), dict):
        return None, "MISSING_REQUIRED_PROBABILITY"
    q = metric_payload["quantiles"]
    pkey = str(probability)
    if pkey not in q:
        return None, "MISSING_REQUIRED_PROBABILITY"
    value = q[pkey]
    if not _finite(value):
        return None, "NONFINITE_QUANTILE"
    return float(value), None

def evaluate_temporal_materiality(payload: dict) -> dict:
    if not isinstance(payload, dict) or not isinstance(payload.get("bucket_evidence"), dict):
        raise ValueError("BUCKET_EVIDENCE_REQUIRED")
    bucket_evidence = payload["bucket_evidence"]
    claim_units = []
    for metric, probabilities in METRICS_PROBABILITIES:
        for probability in probabilities:
            values = {}
            input_reasons = []
            for year in PRIMARY_YEARS:
                value, reason = _quantile_value(bucket_evidence, year, metric, probability)
                values[year] = value
                if reason is not None:
                    input_reasons.append(reason)
            contrasts = []
            for a, b in TRANSITIONS:
                if values[a] is None or values[b] is None:
                    contrasts.append({
                        "transition": f"{a}->{b}",
                        "from_year": a,
                        "to_year": b,
                        "q_a": values[a],
                        "q_b": values[b],
                        "r": None,
                        "status": "BLOCKED",
                        "reason": "MISSING_REQUIRED_INPUT" if input_reasons else "BLOCKED_INPUT",
                    })
                else:
                    c = classify_contrast(values[a], values[b])
                    contrasts.append({
                        "transition": f"{a}->{b}",
                        "from_year": a,
                        "to_year": b,
                        **c,
                    })
            block_reasons = list(input_reasons)
            block_reasons.extend(
                c["reason"] for c in contrasts
                if c["status"] == "BLOCKED" and c.get("reason") not in (None, "MISSING_REQUIRED_INPUT")
            )
            block_reasons = sorted(set(block_reasons))
            if input_reasons or any(c["status"] == "BLOCKED" for c in contrasts):
                status = "BLOCKED"
            elif any(c["status"] == "MATERIAL" for c in contrasts):
                status = "MATERIAL_TEMPORAL_VARIATION"
            else:
                status = "NO_MATERIAL_TEMPORAL_VARIATION_DETECTED"
            claim_units.append({
                "metric": metric,
                "probability": probability,
                "status": status,
                "block_reasons": block_reasons,
                "contrasts": contrasts,
            })
    return {
        "schema": CONTRACT,
        "claim_units": claim_units,
        "primary_years": list(PRIMARY_YEARS),
        "transitions": [f"{a}->{b}" for a, b in TRANSITIONS],
        "materiality_threshold": MATERIALITY_THRESHOLD,
        "epistemic_limit": EPISTEMIC_LIMIT,
        "partial_years_control_primary": False,
        "authority": {
            "scientific_execution": False,
            "trading": False,
            "capital": False,
        },
    }
