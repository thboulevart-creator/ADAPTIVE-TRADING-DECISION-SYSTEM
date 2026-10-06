#!/usr/bin/env python3
"""Independent BEPD-08B recomputation. Does not import canonical runner."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 80
Q18 = Decimal("0.000000000000000001")
PROBS = {
    "P01": Decimal("0.01"), "P05": Decimal("0.05"),
    "P10": Decimal("0.10"), "P25": Decimal("0.25"),
    "P50": Decimal("0.50"), "P75": Decimal("0.75"),
    "P90": Decimal("0.90"), "P95": Decimal("0.95"),
    "P99": Decimal("0.99"),
}


def q18(x: Decimal) -> str:
    return format(x.quantize(Q18, rounding=ROUND_HALF_EVEN), "f")


def frac(n: int, d: int) -> str:
    f = Fraction(n, d)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def type7(values: list[Decimal], p: Decimal) -> Decimal:
    n = len(values)
    if n == 0:
        raise ValueError("empty")
    if n == 1:
        return values[0]
    h = Decimal(1) + Decimal(n - 1) * p
    j = int(h)
    g = h - Decimal(j)
    if j >= n:
        return values[-1]
    return values[j - 1] + g * (values[j] - values[j - 1])


def load(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line, parse_float=Decimal))
    return rows


def recompute(rows: list[dict], expected_n: int) -> dict:
    if len(rows) != expected_n:
        raise RuntimeError("unexpected N")
    ids = [r.get("event_id") for r in rows]
    if any(not isinstance(x, str) or not x for x in ids) or len(set(ids)) != expected_n:
        raise RuntimeError("event id uniqueness failure")
    values = []
    for r in rows:
        if "close_displacement" not in r:
            raise RuntimeError("missing close_displacement")
        raw = r["close_displacement"]
        v = raw if isinstance(raw, Decimal) else Decimal(str(raw))
        if not v.is_finite():
            raise RuntimeError("non-finite close_displacement")
        values.append(abs(v))
    values.sort()
    if any(v < 0 for v in values):
        raise RuntimeError("negative D_CLOSE")
    n = len(values)
    qs = {k: q18(type7(values, p)) for k, p in PROBS.items()}
    zero = sum(v == 0 for v in values)
    counts = defaultdict(int)
    for v in values:
        counts[v] += 1
    cumulative = 0
    ecdf = []
    for v in sorted(counts):
        c = counts[v]
        cumulative += c
        ecdf.append({
            "support_value": format(v, "f"),
            "support_count": c,
            "cumulative_count": cumulative,
            "cumulative_fraction": frac(cumulative, n),
            "cumulative_decimal": q18(Decimal(cumulative) / Decimal(n)),
        })
    core = {
        "N": n,
        "MINIMUM": q18(values[0]),
        "MAXIMUM": q18(values[-1]),
        "MEAN": q18(sum(values, Decimal(0)) / Decimal(n)),
        "MEDIAN": qs["P50"],
        **qs,
        "ZERO_COUNT": zero,
        "ZERO_FRACTION": {"fraction": frac(zero, n), "decimal": q18(Decimal(zero) / Decimal(n))},
        "EMPIRICAL_CDF": ecdf,
    }
    if core["P50"] != core["MEDIAN"]:
        raise RuntimeError("P50 mismatch")
    if ecdf[-1]["cumulative_count"] != n or ecdf[-1]["cumulative_fraction"] != "1":
        raise RuntimeError("ECDF terminal mismatch")
    return core


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--expected-n", type=int, required=True)
    args = ap.parse_args()
    result = {
        "schema": "ATDS_BEPD_08B_INDEPENDENT_REFERENCE_V0_1",
        "implementation": "INDEPENDENT_NO_IMPORT_FROM_CANONICAL_RUNNER",
        "expected_n": args.expected_n,
        "core": recompute(load(Path(args.input)), args.expected_n),
    }
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
