"""BEPD-09D-R2-RD5: synthetic-only fixture; no disk data access."""
from __future__ import annotations
import hashlib
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

WEEK0 = date(2021, 6, 7)
BLOCK_SIZES = (44, 43, 43, 43, 43, 43)
WEEKS = tuple((WEEK0 + timedelta(weeks=i)).isoformat() for i in range(sum(BLOCK_SIZES)))
assert len(WEEKS) == 259 and WEEKS[-1] == "2026-05-18"
BLOCKS = {}
_cursor = 0
for _i, _n in enumerate(BLOCK_SIZES, 1):
    BLOCKS[f"B{_i}"] = WEEKS[_cursor:_cursor+_n]
    _cursor += _n
FOLDS = {i: (tuple(w for j in range(1, i+1) for w in BLOCKS[f"B{j}"]), BLOCKS[f"B{i+1}"]) for i in range(1, 6)}
KEYS = frozenset(("event_id", "target_week_id", "sweep_cluster_id", "side",
    "level_price_mid", "take_h1_close_mid", "take_h1_close_utc", "level_age_weeks",
    "active_level_count_at_target_week_start", "same_week_reintegration"))
PROVENANCE = "RD5_SYNTHETIC_GENERATED_IN_PROCESS"

def synthetic_row(week, j):
    d = date.fromisoformat(week)
    n = (d - WEEK0).days // 7
    local = datetime.combine(d + timedelta(days=j % 5), time(hour=8 + (j % 7), minute=59), tzinfo=ZoneInfo("America/New_York"))
    utc = local.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    event = hashlib.sha256(f"RD5/FIXTURE/{week}/{j}".encode()).hexdigest()
    cluster = hashlib.sha256(f"RD5/CLUSTER/{week}/{j//2}".encode()).hexdigest()
    level = float(10000 + (n * 31 + j * 19) % 997)
    overshoot = 0.00014 * (1 + (n * 5 + j * 7) % 17)
    y = hashlib.sha256(f"RD5/Y/{week}/{j}".encode()).digest()[0] % 2 == 0
    return {"event_id": event, "target_week_id": week, "sweep_cluster_id": cluster,
        "side": "HIGH" if j % 2 else "LOW", "level_price_mid": level,
        "take_h1_close_mid": level * (1 + overshoot if j % 2 else 1 - overshoot),
        "take_h1_close_utc": utc, "level_age_weeks": 1 + ((n * 7 + j * 3) % 19),
        "active_level_count_at_target_week_start": 2 + ((n * 11 + j * 7) % 13),
        "same_week_reintegration": y}

def training_rows(fold=1, per_week=6):
    if type(fold) is not int or fold not in FOLDS: raise ValueError("INVALID_SYNTHETIC_FOLD")
    return [synthetic_row(w,j) for w in FOLDS[fold][0] for j in range(per_week)]
