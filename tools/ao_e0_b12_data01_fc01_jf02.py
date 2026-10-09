from __future__ import annotations

import hashlib
from pathlib import Path

FROM_MS = 1791446400000
TO_MS_INCLUSIVE = 1791449999999
HEADER = b"timestamp,askPrice,bidPrice,askVolume,bidVolume"


def sha256_file(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate_canonical_payload(path: str | Path) -> dict:
    p = Path(path)
    raw = p.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("BOM")
    if b"\r\n" in raw:
        raise ValueError("CRLF")
    lines = raw.splitlines()
    if not lines or lines[0] != HEADER:
        raise ValueError("SCHEMA")
    if len(lines) <= 1:
        raise ValueError("EMPTY_RESPONSE")

    previous = None
    first_ms = None
    last_ms = None
    for row in lines[1:]:
        cols = row.decode("utf-8").split(",")
        if len(cols) != 5:
            raise ValueError("SCHEMA")
        ts, ask, bid, ask_volume, bid_volume = cols
        from datetime import datetime
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        ms = int(dt.timestamp() * 1000)
        if ms < FROM_MS or ms > TO_MS_INCLUSIVE:
            raise ValueError("INTERVAL_LEAK")
        if previous is not None and ms < previous:
            raise ValueError("SOURCE_ORDERING")
        previous = ms
        if first_ms is None:
            first_ms = ms
        last_ms = ms

        a = float(ask); b = float(bid); av = float(ask_volume); bv = float(bid_volume)
        import math
        if not all(math.isfinite(x) for x in (a, b, av, bv)):
            raise ValueError("NONFINITE")
        if a <= 0 or b <= 0 or a < b:
            raise ValueError("PRICE_INVARIANT")
        if av < 0 or bv < 0:
            raise ValueError("NEGATIVE_VOLUME")

    return {
        "tick_count": len(lines) - 1,
        "first_ms": first_ms,
        "last_ms": last_ms,
        "byte_count": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def compare_reads(a: str | Path, b: str | Path) -> dict:
    ar = Path(a).read_bytes()
    br = Path(b).read_bytes()
    return {
        "byte_parity": ar == br,
        "sha256_parity": hashlib.sha256(ar).digest() == hashlib.sha256(br).digest(),
        "a": validate_canonical_payload(a),
        "b": validate_canonical_payload(b),
    }
