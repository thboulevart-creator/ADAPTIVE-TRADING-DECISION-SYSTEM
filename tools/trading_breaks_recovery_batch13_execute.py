from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from tools import trading_breaks_recovery_batch01 as capture
from tools.trading_breaks_recovery_batch13 import (
    BATCH_CONTRACT,
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE,
    batch13_targets,
)
from tools.trading_breaks_recovery_protocol import CONTRACT as PARENT_PROTOCOL

OUT = Path('trading_breaks_batch13_artifacts')


async def execute_frozen_batch(browser):
    targets = batch13_targets()
    days = [day for day, _ in targets]
    if len(targets) != BATCH_SIZE or len(days) != len(set(days)) or days != sorted(days):
        raise RuntimeError('BATCH13_FROZEN_IDENTITY_DRIFT')

    results = []
    for day, reason in targets:
        try:
            result = await capture.probe_candidate(browser, day, reason)
        except Exception as exc:
            result = {
                'target_date': day.isoformat(),
                'candidate_reason': reason,
                'capture_verdict': 'BLOCKED',
                'capture_reason': 'PROBE_EXECUTION_EXCEPTION',
                'exception_type': type(exc).__name__,
                'exception_message': str(exc),
            }
        results.append(result)
    return targets, results


async def main():
    from playwright.async_api import async_playwright

    capture.OUT = OUT
    OUT.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        try:
            targets, results = await execute_frozen_batch(browser)
        finally:
            await browser.close()

    summary = {
        'schema': BATCH_CONTRACT,
        'parent_protocol': PARENT_PROTOCOL,
        'parent_progression_contract': PARENT_PROGRESSION_CONTRACT,
        'batch_number': 13,
        'batch_size': BATCH_SIZE,
        'selection_rule': SELECTION_RULE,
        'capability_id': CURRENT_CAPABILITY_ID,
        'capability_fingerprint': CURRENT_CAPABILITY_FINGERPRINT,
        'targets': [
            {'target_date': day.isoformat(), 'candidate_reason': reason}
            for day, reason in targets
        ],
        'workflow_run': int(os.environ['GITHUB_RUN_ID']),
        'probe_commit': os.environ.get('GITHUB_SHA'),
        'read_only': True,
        'market_data_written': False,
        'results': results,
    }
    (OUT / 'batch_summary.json').write_text(
        json.dumps(summary, indent=2) + '\n', encoding='utf-8'
    )
    return 1 if any(x.get('capture_verdict') == 'FAIL' for x in results) else 0


if __name__ == '__main__':
    raise SystemExit(asyncio.run(main()))
