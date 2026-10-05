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
    parser.add_argument("--invocation-profile", default="P1_12C_PYTHON_JSON_FILE_V1")
    parser.add_argument("--source-root")
    parser.add_argument("--parameters")
    parser.add_argument("--output", required=True)
    parser.add_argument("--producer-id")
    parser.add_argument("--ap0-root")
    parser.add_argument("--ap0-manifest")
    ns = parser.parse_args()

    sys.addaudithook(_audit)
    if ns.invocation_profile == "P1_12C_PYTHON_JSON_FILE_V1":
        if not ns.source_root or not ns.parameters or not ns.producer_id:
            parser.error("legacy synthetic profile requires --source-root --parameters --producer-id")
        sys.argv = [
            ns.producer,
            "--source-root", ns.source_root,
            "--parameters", ns.parameters,
            "--output", ns.output,
            "--producer-id", ns.producer_id,
        ]
    elif ns.invocation_profile == "P1_12C_AP1_CLAIM_SCOPED_V1":
        if not ns.ap0_root or not ns.ap0_manifest:
            parser.error("AP1 profile requires --ap0-root --ap0-manifest")
        sys.argv = [
            ns.producer,
            "--ap0-root", ns.ap0_root,
            "--ap0-manifest", ns.ap0_manifest,
            "--output", ns.output,
        ]
    else:
        parser.error("unsupported P1.12C invocation profile")
    runpy.run_path(ns.producer, run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
