from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any

from tools import trading_breaks_recovery_batch01 as capture
from tools.trading_breaks_recovery_batch10 import (
    BATCH_CONTRACT,
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE,
    batch10_targets,
)
from tools.trading_breaks_recovery_protocol import CONTRACT as PARENT_PROTOCOL


OUT = Path("trading_breaks_batch10_artifacts")


async def execute_frozen_batch(browser: Any) -> tuple[list[tuple[object, str]], list[dict[str, Any]]]:
    """Capture every immutable Batch 10 target exactly once and in frozen order."""
    targets = batch10_targets()
    if len(targets) != BATCH_SIZE:
        raise RuntimeError(f"FROZEN_BATCH10_SIZE_DRIFT:{len(targets)}")

    days = [day for day, _ in targets]
    if len(days) != len(set(days)):
        raise RuntimeError("FROZEN_BATCH10_DUPLICATE_TARGET")
    if days != sorted(days):
        raise RuntimeError("FROZEN_BATCH10_ORDER_DRIFT")

    results: list[dict[str, Any]] = []
    for target_day, candidate_reason in targets:
        try:
            result = await capture.probe_candidate(browser, target_day, candidate_reason)
        except Exception as exc:  # one technical failure cannot skip later frozen members
            result = {
                "target_date": target_day.isoformat(),
                "candidate_reason": candidate_reason,
                "requested_date": target_day.isoformat(),
                "instrument_name": capture.TARGET_INSTRUMENT_NAME,
                "instrument_id": capture.TARGET_INSTRUMENT_ID,
                "capture_verdict": "BLOCKED",
                "capture_reason": "PROBE_EXECUTION_EXCEPTION",
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
            }
        results.append(result)
    return targets, results


async def main() -> int:
    from playwright.async_api import async_playwright

    capture.OUT = OUT
    OUT.mkdir(parents=True, exist_ok=True)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            try:
                targets, results = await execute_frozen_batch(browser)
            finally:
                await browser.close()

        summary = {
            "schema": BATCH_CONTRACT,
            "parent_protocol": PARENT_PROTOCOL,
            "parent_progression_contract": PARENT_PROGRESSION_CONTRACT,
            "batch_number": 10,
            "batch_size": BATCH_SIZE,
            "selection_rule": SELECTION_RULE,
            "capability_id": CURRENT_CAPABILITY_ID,
            "capability_fingerprint": CURRENT_CAPABILITY_FINGERPRINT,
            "targets": [
                {"target_date": day.isoformat(), "candidate_reason": reason}
                for day, reason in targets
            ],
            "workflow_run": int(os.environ["GITHUB_RUN_ID"]) if os.environ.get("GITHUB_RUN_ID") else None,
            "probe_commit": os.environ.get("GITHUB_SHA"),
            "read_only": True,
            "market_data_written": False,
            "results": results,
        }
        (OUT / "batch_summary.json").write_text(
            json.dumps(summary, indent=2) + "\n", encoding="utf-8"
        )
        return 1 if any(item.get("capture_verdict") == "FAIL" for item in results) else 0
    except Exception as exc:
        blocked = {
            "schema": BATCH_CONTRACT,
            "parent_protocol": PARENT_PROTOCOL,
            "parent_progression_contract": PARENT_PROGRESSION_CONTRACT,
            "batch_number": 10,
            "batch_size": BATCH_SIZE,
            "selection_rule": SELECTION_RULE,
            "capability_id": CURRENT_CAPABILITY_ID,
            "capability_fingerprint": CURRENT_CAPABILITY_FINGERPRINT,
            "targets": [
                {"target_date": day.isoformat(), "candidate_reason": reason}
                for day, reason in batch10_targets()
            ],
            "workflow_run": int(os.environ["GITHUB_RUN_ID"]) if os.environ.get("GITHUB_RUN_ID") else None,
            "probe_commit": os.environ.get("GITHUB_SHA"),
            "read_only": True,
            "market_data_written": False,
            "verdict": "BLOCKED",
            "reason": "BATCH10_EXECUTION_EXCEPTION",
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "results": [],
        }
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "batch_summary.json").write_text(
            json.dumps(blocked, indent=2) + "\n", encoding="utf-8"
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
