"""Read-only verification of the repository Python environment baseline."""

from __future__ import annotations

import json
import platform
import sys

EXPECTED_PYTHON = (3, 13)
EXPECTED_MT5 = "5.0.6180"


def main() -> int:
    payload = {
        "status": "PASS",
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
            "platform": platform.platform(),
        },
        "dependencies": {},
        "checks": [],
    }

    python_ok = sys.version_info[:2] == EXPECTED_PYTHON
    payload["checks"].append({
        "id": "PYTHON_BASELINE",
        "status": "PASS" if python_ok else "FAIL",
        "expected": f"CPython {EXPECTED_PYTHON[0]}.{EXPECTED_PYTHON[1]}",
    })

    try:
        import MetaTrader5 as mt5
    except ImportError as exc:
        payload["dependencies"]["MetaTrader5"] = {"status": "FAIL", "error": str(exc)}
        payload["checks"].append({
            "id": "MT5_IMPORT",
            "status": "FAIL",
            "expected": EXPECTED_MT5,
        })
        payload["status"] = "FAIL"
        print(json.dumps(payload, indent=2))
        return 1

    mt5_version = str(mt5.__version__)
    mt5_ok = mt5_version == EXPECTED_MT5
    payload["dependencies"]["MetaTrader5"] = {
        "status": "PASS" if mt5_ok else "FAIL",
        "version": mt5_version,
    }
    payload["checks"].append({
        "id": "MT5_IMPORT",
        "status": "PASS" if mt5_ok else "FAIL",
        "expected": EXPECTED_MT5,
        "observed": mt5_version,
    })

    if not python_ok or not mt5_ok:
        payload["status"] = "FAIL"

    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
