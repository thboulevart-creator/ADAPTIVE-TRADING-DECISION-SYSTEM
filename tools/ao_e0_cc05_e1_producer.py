"""Bounded AO-E0 CC05 E1 execution-evidence producer.

This module orchestrates the already-qualified E1-05 momentum runner with the
already-qualified E1-04 execution runtime. It does not compute scientific
support, expectancy, qualification decisions, trading authority, or capital
authority. Real-data execution remains separately gated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from tools import e1_04_execution_cost_model as e1_04
from tools import e1_05_minimal_momentum_runner as e1_05

PRODUCER_ID = "ATDS_AO_E0_CC05_E1_NATIVE_EXECUTION_V0_1"
OUTPUT_SCHEMA = "ATDS_AO_E0_CC05_E1_EXECUTION_EVIDENCE_V0_1"
OUTPUT_STATUS = "EXECUTION_EVIDENCE_COMPLETE"
CELL_IDENTITY = "sha256:38610ff2afd70998a7fa3e522575faf697ec3159e00829c2b2bbd5da45c52054"
CLAIM_CLASS = "CC05_ECONOMIC_NET_PROFITABILITY"

SEMANTIC_PARAMETERS = {
    "strategy_id": "MOMENTUM_V1",
    "instrument": "USTECH",
    "timeframe": "H1",
    "h1_identity": "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1",
    "temporal_mode": "E1_REPLAY_POINT_IN_TIME",
    "execution_contract": "ATDS_E1_04_EXECUTION_COST_MODEL_V0_1",
    "cost_node": "F2_S4",
    "financing_multiplier": 2,
    "financing_adverse_anchor": 6.3665,
    "slippage_bps_per_execution_event": 4,
    "delta_min": 5.0,
    "policy_stress_is_observed_historical_cost": False,
}
SEMANTIC_PARAMETER_DIGEST = hashlib.sha256(
    json.dumps(SEMANTIC_PARAMETERS, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
).hexdigest()

FORBIDDEN_SCIENTIFIC_KEYS = {
    "expectancy", "mean_pnl", "net_pnl", "profit", "pnl", "sharpe",
    "hit_rate", "drawdown", "p_value", "confidence_interval", "qualification",
}


def build_execution_evidence(h1_rows, raw_ticks) -> dict:
    result = e1_05.run_momentum_runner(
        h1_rows,
        raw_ticks=raw_ticks,
        e1_03_identity="USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1",
        e1_04_runtime=e1_04,
        initial_position=0,
    )
    if result.get("status") != "PASS":
        return {
            "schema": OUTPUT_SCHEMA,
            "status": "BLOCKED",
            "reason": result.get("reason", "E1_RUNNER_BLOCKED"),
            "producer_id": PRODUCER_ID,
            "cell_identity": CELL_IDENTITY,
            "claim_class": CLAIM_CLASS,
            "parameter_digest": SEMANTIC_PARAMETER_DIGEST,
        }
    output = {
        "schema": OUTPUT_SCHEMA,
        "status": OUTPUT_STATUS,
        "producer_id": PRODUCER_ID,
        "cell_identity": CELL_IDENTITY,
        "claim_class": CLAIM_CLASS,
        "parameter_digest": SEMANTIC_PARAMETER_DIGEST,
        "execution_model": "E1_04_RAW_BID_ASK",
        "temporal_mode": "E1_REPLAY_POINT_IN_TIME",
        "cost_node": "F2_S4",
        "records": result["records"],
        "scientific_authority": False,
        "qualification_decision": False,
        "trading_authority": False,
        "capital_authority": False,
    }
    if FORBIDDEN_SCIENTIFIC_KEYS & set(output):
        raise RuntimeError("SCIENTIFIC_RESULT_LAUNDERING_FORBIDDEN")
    return output


def _load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--h1-json", required=True)
    parser.add_argument("--ticks-json", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    h1_rows = _load_json(args.h1_json)
    raw_ticks = _load_json(args.ticks_json)
    result = build_execution_evidence(h1_rows, raw_ticks)
    Path(args.output).write_text(
        json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0 if result.get("status") == OUTPUT_STATUS else 2


if __name__ == "__main__":
    raise SystemExit(main())
