"""Synthetic producer used only to prove AP1-profile argv forwarding."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ap0-root", required=True)
    parser.add_argument("--ap0-manifest", required=True)
    parser.add_argument("--output", required=True)
    ns = parser.parse_args()
    payload = {
        "schema": "ATDS_P1_21_AP1_ARGV_PROBE_V0_1",
        "status": "SYNTHETIC_COMPLETE",
        "ap0_root": ns.ap0_root,
        "ap0_manifest": ns.ap0_manifest,
        "output": ns.output,
        "real_market_data_opened": False,
        "ap1_logic_executed": False,
    }
    Path(ns.output).write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
