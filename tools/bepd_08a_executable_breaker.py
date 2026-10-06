#!/usr/bin/env python3
"""Executable-equivalent BEPD-08A 27-case breaker for BEPD-08B."""

from __future__ import annotations

import argparse
import copy
import importlib.util
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "bepd_08b_absolute_weekly_close_distance.py"
SPEC = importlib.util.spec_from_file_location("bepd08b_runner", RUNNER)
runner = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(runner)

CASES = [
    "wrong EVENT_LEDGER identity",
    "wrong BEPD-05A contract identity",
    "wrong BEPD-05B adopted-result identity",
    "market reconstruction instead of persisted close_displacement",
    "using target_week_close_mid only",
    "using level_price_mid only",
    "failing to apply absolute value",
    "retaining signed values in D_CLOSE",
    "negative D_CLOSE output",
    "dropping negative close_displacement rows",
    "dropping positive close_displacement rows",
    "dropping no-reintegration rows",
    "filtering by HIGH / LOW",
    "filtering by sign",
    "internal/external subgrouping",
    "post-hoc threshold selection",
    "rounding-to-zero laundering",
    "broker-points laundering",
    "ticks laundering",
    "PnL laundering",
    "IID laundering",
    "distance distribution → prediction laundering",
    "distance distribution → edge laundering",
    "distance distribution → TP laundering",
    "distance distribution → SL laundering",
    "distance distribution → strategy validation laundering",
    "distance distribution → trading authority laundering",
]


def must_fail(fn, label: str) -> None:
    try:
        fn()
    except Exception:
        return
    raise AssertionError(f"breaker did not fail: {label}")


def mutate_policy(**kwargs):
    p = copy.deepcopy(runner.CANONICAL_POLICY)
    p.update(kwargs)
    return p


def run_cases() -> None:
    if len(CASES) != 27:
        raise AssertionError("breaker case count")
    must_fail(lambda: runner.validate_bindings({**runner.EXPECTED_BINDINGS, "event_ledger_blob":"bad"}), CASES[0])
    must_fail(lambda: runner.validate_bindings({**runner.EXPECTED_BINDINGS, "bepd05a_contract_blob":"bad"}), CASES[1])
    must_fail(lambda: runner.validate_bindings({**runner.EXPECTED_BINDINGS, "bepd05b_result_blob":"bad"}), CASES[2])
    must_fail(lambda: runner.validate_policy(mutate_policy(market_reconstruction=True)), CASES[3])
    must_fail(lambda: runner.validate_policy(mutate_policy(source_field="target_week_close_mid")), CASES[4])
    must_fail(lambda: runner.validate_policy(mutate_policy(source_field="level_price_mid")), CASES[5])
    must_fail(lambda: runner.validate_policy(mutate_policy(transformation="close_displacement")), CASES[6])
    must_fail(lambda: runner.validate_policy(mutate_policy(transformation="signed(close_displacement)")), CASES[7])
    must_fail(lambda: runner.validate_distance_values([Decimal("-1")]), CASES[8])
    must_fail(lambda: runner.validate_policy(mutate_policy(retain_negative=False)), CASES[9])
    must_fail(lambda: runner.validate_policy(mutate_policy(retain_positive=False)), CASES[10])
    must_fail(lambda: runner.validate_policy(mutate_policy(retain_no_reintegration=False)), CASES[11])
    must_fail(lambda: runner.validate_policy(mutate_policy(filtering="HIGH_ONLY")), CASES[12])
    must_fail(lambda: runner.validate_policy(mutate_policy(filtering="POSITIVE_SIGN_ONLY")), CASES[13])
    must_fail(lambda: runner.validate_policy(mutate_policy(sign_conditional=True)), CASES[14])
    must_fail(lambda: runner.validate_policy(mutate_policy(threshold_search=True)), CASES[15])
    must_fail(lambda: runner.validate_policy(mutate_policy(zero_semantics="ROUNDED_TO_ZERO")), CASES[16])
    must_fail(lambda: runner.validate_policy(mutate_policy(unit="BROKER_POINTS")), CASES[17])
    must_fail(lambda: runner.validate_policy(mutate_policy(unit="TICKS")), CASES[18])
    must_fail(lambda: runner.validate_policy(mutate_policy(pnl=True)), CASES[19])
    must_fail(lambda: runner.validate_policy(mutate_policy(event_is_iid=True)), CASES[20])
    must_fail(lambda: runner.validate_policy(mutate_policy(prediction=True)), CASES[21])
    must_fail(lambda: runner.validate_policy(mutate_policy(edge=True)), CASES[22])
    must_fail(lambda: runner.validate_policy(mutate_policy(tp=True)), CASES[23])
    must_fail(lambda: runner.validate_policy(mutate_policy(sl=True)), CASES[24])
    must_fail(lambda: runner.validate_policy(mutate_policy(strategy_validation=True)), CASES[25])
    must_fail(lambda: runner.validate_policy(mutate_policy(trading_authority="AUTHORIZED")), CASES[26])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["pre-result","real-preflight"], default="pre-result")
    args = ap.parse_args()
    runner.validate_policy(runner.CANONICAL_POLICY)
    runner.validate_bindings(runner.EXPECTED_BINDINGS)
    run_cases()
    print("BEPD08A_EXECUTABLE_EQUIVALENT_BREAKER=27/27_PASS")
    print(f"MODE={args.mode}")


if __name__ == "__main__":
    main()
