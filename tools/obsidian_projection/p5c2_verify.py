from __future__ import annotations

import argparse
import json
from pathlib import Path

from .promotion_experiment import (
    LIVE_VAULT,
    SANDBOX,
    PromotionExperimentError,
    assert_sandbox_boundary,
    run_full_experiment,
    verify_contract,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "ATDS Obsidian P5-C2 OneDrive "
            "promotion experiment harness"
        )
    )
    mode = parser.add_mutually_exclusive_group(
        required=True
    )
    mode.add_argument(
        "--preflight",
        action="store_true",
    )
    mode.add_argument(
        "--run-experiment",
        action="store_true",
    )
    return parser


def _blocked(exc: Exception) -> dict[str, object]:
    return {
        "schema":
            "ATDS_OBSIDIAN_P5C2_BLOCKED_REPORT_V0_1",
        "status": "BLOCKED",
        "error_type": type(exc).__name__,
        "error": str(exc),
        "sandbox_path": str(SANDBOX),
        "live_vault_path": str(LIVE_VAULT),
        "live_vault_modified": False,
        "production_promotion_authorized": False,
    }


def main() -> int:
    args = _parser().parse_args()

    try:
        verify_contract(
            Path(__file__).resolve().parent
        )

        if args.preflight:
            assert_sandbox_boundary(
                SANDBOX
            )
            if SANDBOX.exists():
                raise PromotionExperimentError(
                    "sandbox already exists"
                )
            if not (LIVE_VAULT / "generated").is_dir():
                raise PromotionExperimentError(
                    "live generated directory missing"
                )
            if not (LIVE_VAULT / "views").is_dir():
                raise PromotionExperimentError(
                    "live views directory missing"
                )
            report: dict[str, object] = {
                "schema":
                    "ATDS_OBSIDIAN_P5C2_PREFLIGHT_REPORT_V0_1",
                "status": "PASS",
                "sandbox_path": str(SANDBOX),
                "sandbox_absent": True,
                "live_vault_path":
                    str(LIVE_VAULT),
                "live_vault_modified": False,
                "experiment_authorized_by_preflight":
                    False,
            }
        else:
            report = run_full_experiment(
                SANDBOX
            )

    except (
        PromotionExperimentError,
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

    if args.run_experiment:
        return (
            0
            if report.get("status") == "PASS"
            else 2
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
