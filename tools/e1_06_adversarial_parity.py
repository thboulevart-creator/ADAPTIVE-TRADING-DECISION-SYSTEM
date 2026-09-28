from __future__ import annotations


CONTRACT = "ATDS_E1_06_ADVERSARIAL_REFERENCE_PARITY_V0_1"
H1_IDENTITY = "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1"

PNL_SCOPE = {
    "spread": {"included": True, "mode": "RAW_BID_ASK_INTRINSIC"},
    "commission": {"included": False, "assumed_zero": False},
    "slippage": {"included": False, "assumed_zero": False},
    "financing": {"included": False, "assumed_zero": False},
}

FORBIDDEN_CLAIMS = (
    "STRATEGY_QUALIFIED",
    "BROKER_NET_PNL",
    "ALL_IN_COST_PROFITABILITY",
    "LIVE_PROFITABILITY",
    "FULL_BROKER_EXECUTION_REALISM",
)


def _derive_runner_projection(records, initial_position=0):
    position = initial_position
    entry = None
    components = []
    transitions = []

    for record in records:
        execution = record["execution"]
        events = execution.get("events", [])
        before = position

        if execution["status"] != "EXECUTED":
            transitions.append(
                {
                    "h1_start_ms_utc": record["h1_start_ms_utc"],
                    "before": before,
                    "after": position,
                    "status": execution["status"],
                }
            )
            continue

        for event in events:
            price = float(event["price"])
            action = event["action"]
            role = event.get("role")

            if role == "CLOSE":
                if position == 1 and action == "SELL":
                    components.append(round(price - entry, 12))
                    position = 0
                    entry = None
                elif position == -1 and action == "BUY":
                    components.append(round(entry - price, 12))
                    position = 0
                    entry = None
                continue

            if role == "OPEN":
                position = 1 if action == "BUY" else -1
                entry = price
                continue

            if position == 0:
                position = 1 if action == "BUY" else -1
                entry = price
            elif position == 1 and action == "SELL":
                components.append(round(price - entry, 12))
                position = 0
                entry = None
            elif position == -1 and action == "BUY":
                components.append(round(entry - price, 12))
                position = 0
                entry = None

        transitions.append(
            {
                "h1_start_ms_utc": record["h1_start_ms_utc"],
                "before": before,
                "after": position,
                "status": execution["status"],
            }
        )

    return {
        "components": components,
        "aggregate": round(sum(components), 12),
        "trade_count": len(components),
        "transitions": transitions,
    }


def _execution_events(records):
    return [
        event
        for record in records
        for event in record["execution"].get("events", [])
    ]


def _parity(runner, reference):
    runner_records = runner["records"]
    reference_records = reference["records"]

    runner_events = _execution_events(runner_records)
    reference_events = _execution_events(reference_records)

    return {
        "signal_direction": [
            record["signal"] for record in runner_records
        ]
        == [
            record["signal"] for record in reference_records
        ],
        "signal_timestamp": [
            record["h1_start_ms_utc"] for record in runner_records
        ]
        == [
            record["h1_start_ms_utc"] for record in reference_records
        ],
        "execution_timestamp": [
            event["timestamp_ms"] for event in runner_events
        ]
        == [
            event["timestamp_ms"] for event in reference_events
        ],
        "execution_side": [
            event["price_side"] for event in runner_events
        ]
        == [
            event["price_side"] for event in reference_events
        ],
        "execution_price": [
            event["price"] for event in runner_events
        ]
        == [
            event["price"] for event in reference_events
        ],
        "position_transition": runner["transitions"] == reference["transitions"],
        "closed_trade_count": runner["trade_count"] == reference["trade_count"],
        "realized_pnl_components": runner["pnl_components"]
        == reference["pnl_components"],
        "aggregate_realized_pnl": runner["aggregate_pnl"]
        == reference["aggregate_pnl"],
    }


def qualify_fixture(
    h1_rows,
    *,
    raw_ticks,
    e1_05_runtime,
    e1_04_runtime,
    reference_runtime,
    initial_position=0,
):
    runner_result = e1_05_runtime.run_momentum_runner(
        h1_rows,
        raw_ticks=raw_ticks,
        e1_03_identity=H1_IDENTITY,
        e1_04_runtime=e1_04_runtime,
        initial_position=initial_position,
    )

    if runner_result.get("status") != "PASS":
        return {
            "status": "FAIL",
            "parity": {},
            "runner": runner_result,
            "reference": {},
        }

    projection = _derive_runner_projection(
        runner_result["records"],
        initial_position=initial_position,
    )
    runner = {
        "status": "PASS",
        "records": runner_result["records"],
        "pnl_components": projection["components"],
        "aggregate_pnl": projection["aggregate"],
        "trade_count": projection["trade_count"],
        "transitions": projection["transitions"],
        "pnl_scope": PNL_SCOPE,
    }

    reference = reference_runtime.reference_run(
        h1_rows,
        raw_ticks=raw_ticks,
        initial_position=initial_position,
    )

    parity = _parity(runner, reference)

    return {
        "status": "PASS" if all(parity.values()) else "FAIL",
        "parity": parity,
        "runner": runner,
        "reference": reference,
    }
