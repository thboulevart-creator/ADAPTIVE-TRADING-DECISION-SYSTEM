"""Read-only MT5 tick-source capability probe.

This tool does not modify trading state or write market data. It connects to an
already-installed/running MetaTrader 5 terminal through the official Python
integration and reports whether the broker terminal exposes usable historical
ticks for a requested symbol.

The probe is intentionally small: it establishes capability and evidence before
we design a bulk acquisition pipeline.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe MT5 historical tick availability")
    parser.add_argument("--symbol", required=True, help="Exact MT5 symbol name")
    parser.add_argument("--from", dest="start", required=True, help="UTC ISO datetime, e.g. 2025-06-15T14:00:00Z")
    parser.add_argument("--to", dest="end", required=True, help="UTC ISO datetime, e.g. 2025-06-15T14:05:00Z")
    parser.add_argument("--output", default=None, help="Optional JSON output path")
    return parser.parse_args()


def parse_utc(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    result = datetime.fromisoformat(normalized)
    if result.tzinfo is None:
        raise ValueError("datetime must include an explicit UTC offset or Z")
    return result.astimezone(timezone.utc)


def json_safe(value):
    if isinstance(value, (datetime,)):
        return value.isoformat()
    if hasattr(value, "item"):
        return value.item()
    return value


def main() -> int:
    args = parse_args()
    start = parse_utc(args.start)
    end = parse_utc(args.end)
    if end <= start:
        raise ValueError("--to must be later than --from")

    try:
        import MetaTrader5 as mt5
    except ImportError as exc:
        print("BLOCKED: Python package 'MetaTrader5' is not installed.")
        print(f"DETAIL: {exc}")
        return 2

    if not mt5.initialize():
        print("BLOCKED: MetaTrader 5 terminal initialization failed.")
        print(f"last_error={mt5.last_error()}")
        return 2

    try:
        terminal = mt5.terminal_info()
        account = mt5.account_info()
        symbol_info = mt5.symbol_info(args.symbol)
        selected = False
        if symbol_info is None:
            symbols = mt5.symbols_get()
            matches = []
            if symbols:
                needle = args.symbol.upper()
                matches = [s.name for s in symbols if needle in s.name.upper() or any(k in s.name.upper() for k in ("NAS", "USTEC", "US100", "TECH"))]
            payload = {
                "status": "BLOCKED",
                "reason": "SYMBOL_NOT_FOUND",
                "requested_symbol": args.symbol,
                "candidate_symbols": matches[:100],
            }
            print(json.dumps(payload, indent=2, default=json_safe))
            return 2

        if not symbol_info.visible:
            selected = bool(mt5.symbol_select(args.symbol, True))

        ticks = mt5.copy_ticks_range(args.symbol, start, end, mt5.COPY_TICKS_ALL)
        error = mt5.last_error()

        count = 0 if ticks is None else len(ticks)
        first = None
        last = None
        if count:
            first = {name: json_safe(ticks[0][name].item() if hasattr(ticks[0][name], "item") else ticks[0][name]) for name in ticks.dtype.names}
            last = {name: json_safe(ticks[-1][name].item() if hasattr(ticks[-1][name], "item") else ticks[-1][name]) for name in ticks.dtype.names}

        payload = {
            "status": "PASS" if ticks is not None and count > 0 else "FAIL",
            "requested_symbol": args.symbol,
            "start_utc": start.isoformat(),
            "end_utc": end.isoformat(),
            "tick_count": count,
            "copy_ticks_flags": "COPY_TICKS_ALL",
            "mt5_last_error": list(error) if isinstance(error, tuple) else error,
            "symbol": {
                "name": symbol_info.name,
                "path": symbol_info.path,
                "visible_before_probe": bool(symbol_info.visible),
                "selected_by_probe": selected,
                "digits": int(symbol_info.digits),
                "point": float(symbol_info.point),
                "trade_tick_size": float(symbol_info.trade_tick_size),
                "trade_tick_value": float(symbol_info.trade_tick_value),
            },
            "first_tick": first,
            "last_tick": last,
            "terminal": {
                "name": terminal.name if terminal else None,
                "company": terminal.company if terminal else None,
                "build": terminal.build if terminal else None,
            },
            "account": {
                "login_present": account is not None,
                "server": account.server if account else None,
                "trade_mode": account.trade_mode if account else None,
            },
            "data_written": False,
        }
        text = json.dumps(payload, indent=2, default=json_safe)
        print(text)
        if args.output:
            Path(args.output).write_text(text + "\n", encoding="utf-8")
        return 0 if payload["status"] == "PASS" else 1
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL: probe exception: {type(exc).__name__}: {exc}")
        raise
