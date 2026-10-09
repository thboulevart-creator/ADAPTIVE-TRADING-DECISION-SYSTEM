from __future__ import annotations

import hashlib
import math
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Iterable, Mapping

ATDS_INSTRUMENT = "USATECH.IDX-USD"
JFOREX_INSTRUMENT_STRING = "USATECH.IDX/USD"
CANDIDATE_TRANSPORT = "JFOREX_SDK_IHISTORY"
TRANSFORMATION_ID = "DUKASCOPY_JFOREX_CANONICAL_TICK_ADAPTER_V0_1"
EXPECTED_SOURCE_FIELDS = ("time_ms", "ask", "bid", "askVolume", "bidVolume")
CSV_HEADER = "timestamp,askPrice,bidPrice,askVolume,bidVolume\n"
ONE_HOUR = timedelta(hours=1)


class JF01Blocked(RuntimeError):
    pass


def bind_instrument(resolved: str | None) -> str:
    if resolved is None:
        raise JF01Blocked("BLOCKED_JF01_NULL_INSTRUMENT")
    if resolved != JFOREX_INSTRUMENT_STRING:
        raise JF01Blocked("BLOCKED_JF01_IDENTITY_MISMATCH")
    return resolved


def _require_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None or dt.utcoffset() != timedelta(0):
        raise JF01Blocked("BLOCKED_JF01_INTERVAL_NOT_UTC")
    return dt.astimezone(timezone.utc)


def jforex_interval_ms(start: datetime, end_exclusive: datetime) -> tuple[int, int]:
    start = _require_utc(start)
    end_exclusive = _require_utc(end_exclusive)
    if end_exclusive - start != ONE_HOUR:
        raise JF01Blocked("BLOCKED_JF01_INTERVAL_NOT_ONE_HOUR")
    start_ms = int(start.timestamp() * 1000)
    end_ms = int(end_exclusive.timestamp() * 1000)
    return start_ms, end_ms - 1


def _iso_ms(epoch_ms: int) -> str:
    seconds, millis = divmod(epoch_ms, 1000)
    dt = datetime.fromtimestamp(seconds, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + f".{millis:03d}Z"


def _plain_double(value: object, *, volume: bool = False) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise JF01Blocked("BLOCKED_JF01_NONFINITE_VALUE") from exc
    if not math.isfinite(number):
        raise JF01Blocked("BLOCKED_JF01_NONFINITE_VALUE")
    if volume and number < 0:
        raise JF01Blocked("BLOCKED_JF01_NEGATIVE_VOLUME")
    return format(Decimal(str(number)), "f")


def canonicalize_ticks(
    ticks: Iterable[Mapping[str, object]],
    *,
    interval_start: datetime,
    interval_end_exclusive: datetime,
) -> bytes:
    start = _require_utc(interval_start)
    end = _require_utc(interval_end_exclusive)
    if end - start != ONE_HOUR:
        raise JF01Blocked("BLOCKED_JF01_INTERVAL_NOT_ONE_HOUR")

    start_ms = int(start.timestamp() * 1000)
    end_ms = int(end.timestamp() * 1000)
    lines = [CSV_HEADER]
    previous_ms: int | None = None

    for tick in ticks:
        if set(tick.keys()) != set(EXPECTED_SOURCE_FIELDS):
            raise JF01Blocked("BLOCKED_JF01_SCHEMA_DRIFT")

        try:
            epoch_ms = int(tick["time_ms"])
        except (TypeError, ValueError) as exc:
            raise JF01Blocked("BLOCKED_JF01_NONFINITE_VALUE") from exc

        if epoch_ms < start_ms or epoch_ms >= end_ms:
            raise JF01Blocked("BLOCKED_JF01_INTERVAL_LEAK")
        if previous_ms is not None and epoch_ms < previous_ms:
            raise JF01Blocked("BLOCKED_JF01_SOURCE_ORDERING")
        previous_ms = epoch_ms

        ask_text = _plain_double(tick["ask"])
        bid_text = _plain_double(tick["bid"])
        ask_volume_text = _plain_double(tick["askVolume"], volume=True)
        bid_volume_text = _plain_double(tick["bidVolume"], volume=True)

        ask = Decimal(ask_text)
        bid = Decimal(bid_text)
        if ask <= 0 or bid <= 0:
            raise JF01Blocked("BLOCKED_JF01_NONFINITE_VALUE")
        if ask < bid:
            raise JF01Blocked("BLOCKED_JF01_ASK_BELOW_BID")

        lines.append(
            f"{_iso_ms(epoch_ms)},{ask_text},{bid_text},{ask_volume_text},{bid_volume_text}\n"
        )

    return "".join(lines).encode("utf-8")


def payload_sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def contract() -> dict:
    return {
        "control_id": "AO-E0-B12-DATA-01-FC01-JF01",
        "provider": "DUKASCOPY",
        "current_transport": "JETTA_DUKASCOPY_TICKS_API",
        "candidate_transport": CANDIDATE_TRANSPORT,
        "atds_instrument": ATDS_INSTRUMENT,
        "jforex_instrument_string": JFOREX_INSTRUMENT_STRING,
        "field_mapping": {
            "tick.getTime()": "timestamp",
            "tick.getAsk()": "askPrice",
            "tick.getBid()": "bidPrice",
            "tick.getAskVolume()": "askVolume",
            "tick.getBidVolume()": "bidVolume",
        },
        "target_schema": [
            "timestamp",
            "askPrice",
            "bidPrice",
            "askVolume",
            "bidVolume",
        ],
        "timestamp_format": "YYYY-MM-DDTHH:MM:SS.SSSZ",
        "interval_semantics": {
            "fc01": "[HOUR_START,HOUR_END)",
            "jforex": "[FROM,TO]",
            "translation": "FROM=HOUR_START_MS;TO=HOUR_END_MS-1",
        },
        "ordering": "PRESERVE_PROVIDER_RETURN_ORDER",
        "deduplication": False,
        "line_ending": "LF",
        "bom": False,
        "transformation_id": TRANSFORMATION_ID,
        "real_jforex_request": False,
    }
