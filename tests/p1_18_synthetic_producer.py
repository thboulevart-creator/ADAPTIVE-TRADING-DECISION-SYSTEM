"""P1-18 test-only synthetic producer.

No AP1 logic, market result, signal, PnL, OOS or trading conclusion exists here.
The producer inventories synthetic byte files and emits a deterministic synthetic
JSON object. Special modes exist only to verify P1.12C fail-closed behavior.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


SCHEMA = "ATDS_P1_18_SYNTHETIC_PRODUCER_OUTPUT_V0_1"
STATUS = "SYNTHETIC_COMPLETE"


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def corpus_inventory(root: Path) -> tuple[str, int, int]:
    rows = []
    total = 0
    count = 0
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest = sha256_path(path)
        size = path.stat().st_size
        rows.append(f"{path.relative_to(root).as_posix()}\t{size}\t{digest}\n")
        total += size
        count += 1
    h = hashlib.sha256()
    for row in rows:
        h.update(row.encode("utf-8"))
    return h.hexdigest(), count, total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--parameters", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--producer-id", required=True)
    ns = parser.parse_args()

    source_root = Path(ns.source_root)
    parameters = json.loads(Path(ns.parameters).read_text(encoding="utf-8"))
    mode = parameters.get("mode", "normal")

    if mode == "network_attempt":
        import socket
        socket.socket()
        raise AssertionError("network audit hook did not block socket creation")

    if mode == "child_process_attempt":
        import subprocess
        subprocess.run(["echo", "forbidden"], check=False)
        raise AssertionError("audit hook did not block child process")

    if mode == "mutate_source":
        target = next(iter(sorted(source_root.rglob("*.parquet"))))
        with target.open("ab") as handle:
            handle.write(b"P1-18-MUTATION\n")

    inventory_sha, file_count, total_bytes = corpus_inventory(source_root)
    parameter_digest = hashlib.sha256(canonical(parameters)).hexdigest()
    result = {
        "schema": SCHEMA,
        "status": "NOT_COMPLETE" if mode == "invalid_status" else STATUS,
        "producer_id": ns.producer_id,
        "source_inventory_sha256": inventory_sha,
        "parameter_digest": parameter_digest,
        "synthetic_file_count": file_count,
        "synthetic_total_bytes": total_bytes,
        "synthetic_transform": "BYTE_INVENTORY_ONLY",
        "market_semantics": "NONE",
        "trading_semantics": "NONE",
    }
    Path(ns.output).write_bytes(canonical(result) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
