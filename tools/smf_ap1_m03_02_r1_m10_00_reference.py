from __future__ import annotations

import math

YEARS = [2022, 2023, 2024, 2025]
PAIRS = [(2022, 2023), (2023, 2024), (2024, 2025)]
SURFACE = [
    ("tick_count", [0.5, 0.9, 0.99]),
    ("minute_range", [0.5, 0.9, 0.95, 0.99]),
    ("spread_mean", [0.5, 0.9, 0.95, 0.99]),
]

def _ok(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))

def reference_evaluate_temporal_materiality(payload):
    buckets = payload["bucket_evidence"]
    rows = []
    for metric, probs in SURFACE:
        for p in probs:
            by_year = {}
            reasons = []
            for y in YEARS:
                b = buckets.get("UTC_YEAR:" + str(y))
                if b is None:
                    by_year[y] = None; reasons.append("MISSING_YEAR"); continue
                m = b.get(metric)
                if m is None:
                    by_year[y] = None; reasons.append("MISSING_METRIC"); continue
                q = m.get("quantiles") if isinstance(m, dict) else None
                if not isinstance(q, dict) or str(p) not in q:
                    by_year[y] = None; reasons.append("MISSING_REQUIRED_PROBABILITY"); continue
                v = q[str(p)]
                if not _ok(v):
                    by_year[y] = None; reasons.append("NONFINITE_QUANTILE"); continue
                by_year[y] = float(v)
            cs = []
            for a, b in PAIRS:
                va, vb = by_year[a], by_year[b]
                if va is None or vb is None:
                    cs.append({"transition":f"{a}->{b}","from_year":a,"to_year":b,"q_a":va,"q_b":vb,"r":None,"status":"BLOCKED","reason":"MISSING_REQUIRED_INPUT" if reasons else "BLOCKED_INPUT"})
                    continue
                den = abs(va) + abs(vb)
                if den == 0.0:
                    cs.append({"transition":f"{a}->{b}","from_year":a,"to_year":b,"q_a":va,"q_b":vb,"r":None,"status":"BLOCKED","reason":"ZERO_DENOMINATOR"})
                else:
                    r = 2.0 * abs(vb - va) / den
                    cs.append({"transition":f"{a}->{b}","from_year":a,"to_year":b,"q_a":va,"q_b":vb,"r":r,"status":"MATERIAL" if r >= 0.20 else "NON_MATERIAL","reason":None})
            br = list(reasons)
            br.extend(c["reason"] for c in cs if c["status"]=="BLOCKED" and c.get("reason") not in (None,"MISSING_REQUIRED_INPUT"))
            br = sorted(set(br))
            if reasons or any(c["status"]=="BLOCKED" for c in cs):
                s="BLOCKED"
            elif any(c["status"]=="MATERIAL" for c in cs):
                s="MATERIAL_TEMPORAL_VARIATION"
            else:
                s="NO_MATERIAL_TEMPORAL_VARIATION_DETECTED"
            rows.append({"metric":metric,"probability":p,"status":s,"block_reasons":br,"contrasts":cs})
    return {
        "schema":"ATDS_SMF_AP1_M03_02_R1_M10_00_RUNTIME_V0_1",
        "claim_units":rows,
        "primary_years":YEARS,
        "transitions":["2022->2023","2023->2024","2024->2025"],
        "materiality_threshold":0.20,
        "epistemic_limit":"EXPLORATORY_DIAGNOSTIC_TEMPORAL_STABILITY_EVIDENCE",
        "partial_years_control_primary":False,
        "authority":{"scientific_execution":False,"trading":False,"capital":False},
    }
