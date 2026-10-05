"""Narrow P1.12C Python producer sandbox runner.

The runner blocks Python-level socket and child-process/FFI escape events through
an audit hook. It is not a general command runner and has no authority semantics.
"""
from __future__ import annotations

import argparse
import runpy
import sys


def _audit(event: str, args) -> None:
    blocked_exact = {
        "subprocess.Popen",
        "os.system",
        "os.fork",
        "os.forkpty",
        "ctypes.dlopen",
        "ctypes.dlsym",
    }
    blocked_prefixes = (
        "socket.",
        "os.exec",
        "os.spawn",
        "os.posix_spawn",
    )
    if event in blocked_exact or any(event.startswith(prefix) for prefix in blocked_prefixes):
        raise RuntimeError(f"P1_12C_SANDBOX_FORBIDDEN_EVENT:{event}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--producer", required=True)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--parameters", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--producer-id", required=True)
    ns = parser.parse_args()

    sys.addaudithook(_audit)
    sys.argv = [
        ns.producer,
        "--source-root", ns.source_root,
        "--parameters", ns.parameters,
        "--output", ns.output,
        "--producer-id", ns.producer_id,
    ]
    runpy.run_path(ns.producer, run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
