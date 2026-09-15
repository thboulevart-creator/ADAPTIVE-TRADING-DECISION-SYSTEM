from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any

from tools import trading_breaks_recovery_batch01 as capture
from tools.trading_breaks_recovery_batch09 import (
    BATCH_CONTRACT,
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE,
    batch09_targets,
)
from tools.trading_breaks_recovery_protocol import CONTRACT as RECOVERY_PROTOCOL


OUT = Path("trading_breaks_batch09_artifacts")


async def execute_frozen_batch(browser: Any) -> tuple[list[tuple[Any, str]], list[dict[str, Any]]]:
    """Execute exactly the versioned Batch 09 snapshot, in frozen order."""
    targets = batch09_targets()
    if len(targets) != BATCH_SIZE:
        raise RuntimeError("FROZEN_BATCH09_SIZE_DRIFT")
    if len({day for day, _ in targets}) != BATCH_SIZE:
        raise RuntimeError("FROZEN_BATCH09_DUPLICATE_TARGET")
    if [day for day, _ in targets] != sorted(day for day, _ in targets):
        raise RuntimeError("FROZEN_BATCH09_ORDER_DRIFT")

    results: list[dict[str, Any]] = []
    for target_day, candidate_reason in targets:
        try:
            results.append(
                await capture.probe_candidate(browser, target_day, candidate_reason)
            )
        except Exception as exc:
            results.append(
                {
                    "target_date": target_day.isoformat(),
                    "candidate_reason": candidate_reason,
                    "requested_date": target_day.isoformat(),
                    "instrument_name": capture.TARGET_INSTRUMENT_NAME,
                    "instrument_id_expected": capture.TARGET_INSTRUMENT_ID,
                    "capture_verdict": "BLOCKED",
                    "capture_reason": "PROBE_EXECUTION_EXCEPTION",
                    "exception": repr(exc),
                }
            )
    return targets, results


async def main() -> int:
    from playwright.async_api import async_playwright

    # Reuse exactly the already-qualified semantic capture implementation.
    # Execution membership comes only from batch09_targets(); no live queue is
    # consulted, recalculated, shortened, expanded, reordered or substituted.
    capture.OUT = OUT
    OUT.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        targets, results = await execute_frozen_batch(browser)
        await browser.close()

    summary = {
        "schema": BATCH_CONTRACT,
        "parent_protocol": RECOVERY_PROTOCOL,
        "parent_progression_contract": PARENT_PROGRESSION_CONTRACT,
        "batch_number": 9,
        "batch_size": BATCH_SIZE,
        "selection_rule": SELECTION_RULE,
        "capability_id": CURRENT_CAPABILITY_ID,
        "capability_fingerprint": CURRENT_CAPABILITY_FINGERPRINT,
        "targets": [
            {"date": target_day.isoformat(), "reason": reason}
            for target_day, reason in targets
        ],
        "workflow_run": os.environ.get("GITHUB_RUN_ID"),
        "probe_commit": os.environ.get("GITHUB_SHA"),
        "read_only": True,
        "market_data_written": False,
        "results": results,
    }
    (OUT / "batch_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))

    return 1 if any(item.get("capture_verdict") == "FAIL" for item in results) else 0


if __name__ == "__main__":
    try:
        raise SystemExit(asyncio.run(main()))
    except Exception as exc:
        OUT.mkdir(parents=True, exist_ok=True)
        failure = {
            "schema": BATCH_CONTRACT,
            "parent_protocol": RECOVERY_PROTOCOL,
            "parent_progression_contract": PARENT_PROGRESSION_CONTRACT,
            "batch_number": 9,
            "batch_size": BATCH_SIZE,
            "verdict": "BLOCKED",
            "reason": "BATCH_EXECUTION_EXCEPTION",
            "exception": repr(exc),
        }
        (OUT / "batch_summary.json").write_text(
            json.dumps(failure, indent=2), encoding="utf-8"
        )
        print(json.dumps(failure, indent=2))
        raise
