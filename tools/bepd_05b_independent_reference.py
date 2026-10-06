#!/usr/bin/env python3
"""Independent BEPD-05B reference recomputation.

Deliberately does not import the canonical BEPD-05B runner.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 80
Q18 = Decimal("0.000000000000000001")


def out18(x: Decimal) -> str:
    return format(x.quantize(Q18, rounding=ROUND_HALF_EVEN), "f")


def support_string(x: Decimal) -> str:
    return format(x, "f")


def frac_reduced(n: int, d: int) -> str:
    f = Fraction(n, d)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def sign_fraction(n: int, d: int) -> dict:
    return {"fraction": f"{n}/{d}", "decimal": out18(Decimal(n) / Decimal(d))}


def q_type7(values: list[Decimal], p: Decimal) -> Decimal:
    n = len(values)
    if n == 0:
        raise ValueError("empty input")
    if n == 1:
        return values[0]
    h = Decimal(1) + Decimal(n - 1) * p
    lo_index_1 = int(h)
    weight = h - Decimal(lo_index_1)
    if lo_index_1 >= n:
        return values[-1]
    a = values[lo_index_1 - 1]
    b = values[lo_index_1]
    return a + weight * (b - a)


def read(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line, parse_float=Decimal))
    return rows


def recompute(rows: list[dict], expected_n: int) -> dict:
    if len(rows) != expected_n:
        raise RuntimeError("unexpected N")
    ids = [r["event_id"] for r in rows]
    if len(set(ids)) != expected_n:
        raise RuntimeError("event id uniqueness failure")
    vals = [r["close_displacement"] if isinstance(r["close_displacement"], Decimal) else Decimal(str(r["close_displacement"])) for r in rows]
    vals.sort()
    n = len(vals)

    probs = {
        "P01": Decimal("0.01"),
        "P05": Decimal("0.05"),
        "P10": Decimal("0.10"),
        "P25": Decimal("0.25"),
        "P50": Decimal("0.50"),
        "P75": Decimal("0.75"),
        "P90": Decimal("0.90"),
        "P95": Decimal("0.95"),
        "P99": Decimal("0.99"),
    }
    qs = {k: out18(q_type7(vals, p)) for k, p in probs.items()}

    pos = sum(v > 0 for v in vals)
    zer = sum(v == 0 for v in vals)
    neg = sum(v < 0 for v in vals)

    support_counts = defaultdict(int)
    for v in vals:
        support_counts[v] += 1
    cumulative = 0
    ecdf = []
    for v in sorted(support_counts):
        cnt = support_counts[v]
        cumulative += cnt
        ecdf.append({
            "support_value": support_string(v),
            "support_count": cnt,
            "cumulative_count": cumulative,
            "cumulative_fraction": frac_reduced(cumulative, n),
            "cumulative_decimal": out18(Decimal(cumulative) / Decimal(n)),
        })

    core = {
        "N": n,
        "MINIMUM": out18(vals[0]),
        "MAXIMUM": out18(vals[-1]),
        "MEAN": out18(sum(vals, Decimal(0)) / Decimal(n)),
        "MEDIAN": qs["P50"],
        **qs,
        "POSITIVE_COUNT": pos,
        "ZERO_COUNT": zer,
        "NEGATIVE_COUNT": neg,
        "POSITIVE_FRACTION": sign_fraction(pos, n),
        "ZERO_FRACTION": sign_fraction(zer, n),
        "NEGATIVE_FRACTION": sign_fraction(neg, n),
        "EMPIRICAL_CDF": ecdf,
    }
    if core["P50"] != core["MEDIAN"]:
        raise AssertionError("P50 mismatch")
    if pos + zer + neg != n:
        raise AssertionError("sign reconciliation")
    if ecdf[-1]["cumulative_count"] != n or ecdf[-1]["cumulative_fraction"] != "1":
        raise AssertionError("ECDF terminal state")
    return core


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--expected-n", type=int, required=True)
    args = ap.parse_args()

    rows = read(Path(args.input))
    result = {
        "schema": "ATDS_BEPD_05B_INDEPENDENT_REFERENCE_V0_1",
        "implementation": "INDEPENDENT_NO_IMPORT_FROM_CANONICAL_RUNNER",
        "expected_n": args.expected_n,
        "core": recompute(rows, args.expected_n),
    }
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
