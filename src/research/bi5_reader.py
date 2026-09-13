"""Controlled reconstruction of the BI5 reader.

RECONSTRUCTION != RECOVERY: this implementation is reconstructed from the
persisted B07-B09 architectural evidence and is not claimed to be the lost
historical source byte-for-byte.
"""
from __future__ import annotations

import lzma
import math
import re
import struct
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterator


@dataclass(frozen=True)
class Tick:
    timestamp: datetime
    ask: float
    bid: float
    ask_volume: float
    bid_volume: float


_HOUR_RE = re.compile(r"(?P<date>\d{8})(?P<hour>\d{2})\.bi5$", re.IGNORECASE)


def parse_hour(path: Path) -> datetime:
    match = _HOUR_RE.search(path.name)
    if not match:
        raise ValueError(f"Invalid BI5 hourly filename: {path.name}")
    return datetime.strptime(match.group("date") + match.group("hour"), "%Y%m%d%H").replace(tzinfo=timezone.utc)


def _decode_payload(payload: bytes, hour: datetime, contract: dict) -> Iterator[Tick]:
    record_size = int(contract["record_size"])
    record_struct = contract["record_struct"]
    timestamp_unit = contract["timestamp_unit"]
    price_scale = float(contract["price_scale"])
    if record_size != struct.calcsize(record_struct):
        raise ValueError("BI5 contract record_size does not match record_struct")
    if timestamp_unit != "milliseconds":
        raise ValueError("Unsupported BI5 timestamp_unit")
    if len(payload) % record_size:
        raise ValueError("BI5 payload is not aligned to record size")

    previous = None
    for offset in range(0, len(payload), record_size):
        raw_time, raw_ask, raw_bid, ask_volume, bid_volume = struct.unpack_from(record_struct, payload, offset)
        timestamp = hour + timedelta(milliseconds=raw_time)
        ask = raw_ask / price_scale
        bid = raw_bid / price_scale
        if timestamp < hour or timestamp >= hour + timedelta(hours=1):
            raise ValueError("Tick timestamp outside its declared hour")
        if not (math.isfinite(ask) and math.isfinite(bid) and ask > 0 and bid > 0):
            raise ValueError("Invalid BI5 price")
        if ask < bid:
            raise ValueError("Ask price below bid price")
        if not (math.isfinite(ask_volume) and math.isfinite(bid_volume)):
            raise ValueError("Invalid BI5 volume")
        if ask_volume < 0 or bid_volume < 0:
            raise ValueError("Negative BI5 volume")
        tick = Tick(timestamp, float(ask), float(bid), float(ask_volume), float(bid_volume))
        if previous is not None and tick.timestamp < previous:
            raise ValueError("BI5 ticks are not monotonic within file")
        previous = tick.timestamp
        yield tick


def iter_ticks(path: Path, contract: dict) -> Iterator[Tick]:
    hour = parse_hour(path)
    with lzma.open(path, "rb", format=lzma.FORMAT_ALONE) as handle:
        payload = handle.read()
    yield from _decode_payload(payload, hour, contract)
