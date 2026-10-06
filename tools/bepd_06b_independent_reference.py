#!/usr/bin/env python3
"""Independent BEPD-06B timing recomputation.

Deliberately does not import the canonical BEPD-06B runner.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 80
Q18 = Decimal("0.000000000000000001")
HOUR_US = Decimal(3_600_000_000)


def q18(x: Decimal) -> str:
    return format(x.quantize(Q18, rounding=ROUND_HALF_EVEN), "f")


def parse_utc(s: str) -> datetime:
    d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if d.tzinfo is None or d.utcoffset() is None or d.utcoffset().total_seconds() != 0:
        raise ValueError("non-UTC timestamp")
    return d


def hours(a: str, b: str) -> Decimal:
    t0 = parse_utc(a)
    t1 = parse_utc(b)
    if not t1 > t0:
        raise ValueError("T1 <= T0")
    d = t1 - t0
    us = (
        Decimal(d.days) * Decimal(86_400_000_000)
        + Decimal(d.seconds) * Decimal(1_000_000)
        + Decimal(d.microseconds)
    )
    return us / HOUR_US


def type7(v: list[Decimal], p: Decimal) -> Decimal:
    n = len(v)
    h = Decimal(1) + Decimal(n - 1) * p
    j = int(h)
    g = h - Decimal(j)
    if j >= n:
        return v[-1]
    return v[j - 1] + g * (v[j] - v[j - 1])


def rf(n: int, d: int) -> str:
    f = Fraction(n, d)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def recompute(rows: list[dict]) -> dict:
    if len(rows) != 472:
        raise RuntimeError("base N mismatch")
    ids = [r["event_id"] for r in rows]
    if len(set(ids)) != 472:
        raise RuntimeError("event_id uniqueness failure")

    vals = []
    true_n = 0
    false_n = 0
    for r in rows:
        if r["same_week_reintegration"] is True:
            true_n += 1
            if r["take_h1_close_utc"] is None or r["reintegration_h1_close_utc"] is None:
                raise RuntimeError("null T0/T1")
            vals.append(hours(r["take_h1_close_utc"], r["reintegration_h1_close_utc"]))
        elif r["same_week_reintegration"] is False:
            false_n += 1
            if r["reintegration_h1_close_utc"] is not None:
                raise RuntimeError("false event has non-null T1")
        else:
            raise RuntimeError("invalid state")

    if (true_n, false_n) != (370, 102):
        raise RuntimeError("370/102 mismatch")
    vals.sort()
    probs = {
        "P01": Decimal("0.01"), "P05": Decimal("0.05"), "P10": Decimal("0.10"),
        "P25": Decimal("0.25"), "P50": Decimal("0.50"), "P75": Decimal("0.75"),
        "P90": Decimal("0.90"), "P95": Decimal("0.95"), "P99": Decimal("0.99"),
    }
    qs = {k: q18(type7(vals, p)) for k,p in probs.items()}
    counts = defaultdict(int)
    for x in vals:
        counts[x] += 1
    cum = 0
    ecdf = []
    for x in sorted(counts):
        c = counts[x]
        cum += c
        ecdf.append({
            "support_value": format(x, "f"),
            "support_count": c,
            "cumulative_count": cum,
            "cumulative_fraction": rf(cum, 370),
            "cumulative_decimal": q18(Decimal(cum) / Decimal(370)),
        })

    core = {
        "BASE_N": 472,
        "REINTEGRATION_TRUE_N": 370,
        "NO_REINTEGRATION_WITHIN_TARGET_WEEK_N": 102,
        "N_TIMING": 370,
        "MINIMUM_ELAPSED_UTC_HOURS": q18(vals[0]),
        "MAXIMUM_ELAPSED_UTC_HOURS": q18(vals[-1]),
        "MEAN": q18(sum(vals, Decimal(0)) / Decimal(370)),
        "MEDIAN": qs["P50"],
        **qs,
        "EMPIRICAL_CDF": ecdf,
    }
    if core["P50"] != core["MEDIAN"]:
        raise AssertionError("P50 mismatch")
    if ecdf[-1]["cumulative_count"] != 370 or ecdf[-1]["cumulative_fraction"] != "1":
        raise AssertionError("ECDF terminal mismatch")
    return core


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    rows = [json.loads(x) for x in Path(args.input).read_text(encoding="utf-8").splitlines() if x.strip()]
    obj = {
        "schema":"ATDS_BEPD_06B_INDEPENDENT_REFERENCE_V0_1",
        "implementation":"INDEPENDENT_NO_IMPORT_FROM_CANONICAL_RUNNER",
        "core":recompute(rows),
    }
    Path(args.output).write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")


if __name__ == "__main__":
    main()
