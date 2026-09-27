from __future__ import annotations

import argparse
import json
from pathlib import Path

from .obsidian_open_compatibility import (
    ObsidianOpenCompatibilityError,
)
from .obsidian_open_retry import (
    ObsidianOpenRetryError,
    post_close_retry_verify,
    run_retry_open_experiment,
    run_synthetic_lock_breaker,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "ATDS Obsidian P5-C3R2 reader-only "
            "EACCES retry verifier"
        )
    )

    mode = parser.add_mutually_exclusive_group(
        required=True
    )
    mode.add_argument(
        "--synthetic-lock-breaker",
        action="store_true",
    )
    mode.add_argument(
        "--run-open",
        action="store_true",
    )
    mode.add_argument(
        "--post-close",
        action="store_true",
    )

    parser.add_argument(
        "--snapshot",
        type=Path,
    )
    parser.add_argument(
        "--manual-visual-accepted",
        action="store_true",
    )
    return parser


def _blocked(exc: Exception) -> dict[str, object]:
    return {
        "schema":
            "ATDS_OBSIDIAN_P5C3R2_BLOCKED_REPORT_V0_1",
        "status": "BLOCKED",
        "error_type": type(exc).__name__,
        "error": str(exc),
        "production_promotion_authorized": False,
        "continuous_observer_authorized": False,
        "p5c3r2_qualified": False,
    }


def main() -> int:
    args = _parser().parse_args()

    try:
        if args.synthetic_lock_breaker:
            if args.snapshot is not None:
                raise ObsidianOpenRetryError(
                    "--snapshot forbidden with --synthetic-lock-breaker"
                )
            if args.manual_visual_accepted:
                raise ObsidianOpenRetryError(
                    "manual acceptance forbidden with --synthetic-lock-breaker"
                )
            report = run_synthetic_lock_breaker()

        elif args.run_open:
            if args.snapshot is None:
                raise ObsidianOpenRetryError(
                    "--snapshot required with --run-open"
                )
            if args.manual_visual_accepted:
                raise ObsidianOpenRetryError(
                    "manual acceptance forbidden with --run-open"
                )
            report = run_retry_open_experiment(
                args.snapshot
            )

        else:
            if args.snapshot is None:
                raise ObsidianOpenRetryError(
                    "--snapshot required with --post-close"
                )
            report = post_close_retry_verify(
                args.snapshot,
                manual_visual_accepted=
                    args.manual_visual_accepted,
            )

    except (
        ObsidianOpenRetryError,
        ObsidianOpenCompatibilityError,
        OSError,
        ValueError,
    ) as exc:
        print(
            json.dumps(
                _blocked(exc),
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 2

    print(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
    )

    if args.run_open:
        return (
            0
            if report.get("status")
            == "PASS_AUTOMATED_OPEN_RETRY_EXPERIMENT"
            else 2
        )

    return (
        0
        if report.get("status") == "PASS"
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
