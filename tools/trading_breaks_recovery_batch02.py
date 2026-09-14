from __future__ import annotations

import asyncio
import json
import os
from datetime import date
from pathlib import Path
from typing import Any

from tools import trading_breaks_recovery_batch01 as capture
from tools.trading_breaks_recovery_protocol import CONTRACT as RECOVERY_PROTOCOL


BATCH_CONTRACT = "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02_POLICY_V1"
BATCH_SIZE = 5
OUT = Path("trading_breaks_batch02_artifacts")

FROZEN_BATCH02_TARGETS: tuple[tuple[date, str], ...] = (
    (date(2021, 12, 24), "CHRISTMAS_OBSERVED"),
    (date(2021, 12, 31), "NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED"),
    (date(2022, 1, 17), "MARTIN_LUTHER_KING_DAY"),
    (date(2022, 2, 21), "PRESIDENTS_DAY"),
    (date(2022, 4, 15), "GOOD_FRIDAY"),
)


def batch02_targets() -> list[tuple[date, str]]:
    """Return immutable membership versioned before Batch 02 observation."""
    return list(FROZEN_BATCH02_TARGETS)


async def main() -> int:
    from playwright.async_api import async_playwright

    # Reuse only the already-qualified capture implementation. Its output root
    # is explicitly redirected so Batch 01 evidence/history remains untouched.
    capture.OUT = OUT
    OUT.mkdir(parents=True, exist_ok=True)

    targets = batch02_targets()
    results: list[dict[str, Any]] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
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
        await browser.close()

    summary = {
        "schema": BATCH_CONTRACT,
        "parent_protocol": RECOVERY_PROTOCOL,
        "batch_number": 2,
        "batch_size": BATCH_SIZE,
        "selection_rule": "FIRST_N_OF_POST_BATCH01_GOVERNED_RECOVERY_QUEUE",
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
            "batch_number": 2,
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
