from __future__ import annotations

import ast
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from tools import ao_e0_b12_data01_fc01 as F
from tools.ao_e0_b12_data01_acq02 import seal_raw_object

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "GOVERNANCE" / "AO-E0-B12-DATA-01-FC-01-COLLECTION-CONTRACT-V0.1.json"
AUTH = ROOT / "GOVERNANCE" / "AO-E0-B12-DATA-01-FC-01-HUMAN-AUTHORIZATION-RECEIPT-2026-10-07.json"
RUNTIME = ROOT / "tools" / "ao_e0_b12_data01_fc01.py"


def raw_hour(dt: datetime, *, bid_shift: int = 0) -> bytes:
    base = int(dt.timestamp() * 1000)
    o = {
        "timestamp": base,
        "multiplier": "0.001",
        "times": [1] + [60000] * 59,
        "bid": 100.000 + bid_shift / 1000.0,
        "ask": 100.010 + bid_shift / 1000.0,
        "bids": [0] * 60,
        "asks": [0] * 60,
        "bidVolumes": [1] * 60,
        "askVolumes": [1] * 60,
    }
    return (json.dumps(o, separators=(",", ":")) + "\n").encode()


def fetcher(cache: Path, dt: datetime):
    return raw_hour(dt), "NETWORK", 1


def changed_fetcher(cache: Path, dt: datetime):
    return raw_hour(dt, bid_shift=1), "NETWORK", 1


def test_01_target_is_last_complete_utc_hour():
    now = datetime(2026, 10, 7, 18, 27, 31, tzinfo=timezone.utc)
    assert F.target_end_for(now) == datetime(2026, 10, 7, 18, tzinfo=timezone.utc)


def test_02_target_never_crosses_fixed_horizon():
    now = datetime(2027, 10, 7, 12, tzinfo=timezone.utc)
    assert F.target_end_for(now) == F.FIXED_END


def test_03_naive_clock_blocks():
    with pytest.raises(F.FC01Blocked, match="NAIVE_CLOCK"):
        F.floor_complete_hour(datetime(2026, 10, 7, 18, 0, 0))


def test_04_first_cycle_structural_only_and_replay_pass(tmp_path):
    now = datetime(2026, 10, 6, 12, 30, tzinfo=timezone.utc)
    out = F.collect_cycle(tmp_path, now_utc=now, fetcher=fetcher)
    h = out["health"]
    assert h["collection_status"] == "PASS"
    assert h["coverage_end_exclusive_utc"] == "2026-10-06T12:00:00Z"
    assert h["deterministic_replay_status"] == "PASS"
    assert h["b12"] == "CLOSED"
    assert h["performance_bearing_read"] is False
    assert h["missing_intervals"] == []
    assert h["raw_object_count"] == 22
    assert h["warmup_object_count"] == 20
    assert h["forward_evidence_object_count"] == 2
    assert h["raw_tick_count"] == 22 * 60


def test_05_same_boundary_is_idempotent(tmp_path):
    now = datetime(2026, 10, 6, 12, 30, tzinfo=timezone.utc)
    a = F.collect_cycle(tmp_path, now_utc=now, fetcher=fetcher)
    b = F.collect_cycle(tmp_path, now_utc=now, fetcher=fetcher)
    assert a["health"] == b["health"]
    assert b["run_stats"]["sealed_new_objects"] == 0
    assert b["run_stats"]["replayed_objects"] == 22


def test_06_health_receipt_has_no_performance_surface(tmp_path):
    now = datetime(2026, 10, 6, 12, 30, tzinfo=timezone.utc)
    h = F.collect_cycle(tmp_path, now_utc=now, fetcher=fetcher)["health"]
    keys = {k.lower() for k in h}
    assert not keys.intersection(F.FORBIDDEN_HEALTH_KEYS)
    encoded = json.dumps(h).lower()
    for token in (
        "cumulative_closed_trade_count",
        "win_rate",
        "profit_factor",
        "expectancy",
        "momentum_signal",
        "target_position",
        "support",
        "refute",
    ):
        assert token not in encoded


def test_07_source_object_mutation_blocks(tmp_path):
    now = datetime(2026, 10, 6, 12, 30, tzinfo=timezone.utc)
    F.collect_cycle(tmp_path, now_utc=now, fetcher=fetcher)
    # Remove provider cache relevance: the injected fetcher controls exact bytes.
    with pytest.raises(Exception, match="SOURCE_OBJECT_MUTATION"):
        F.collect_cycle(tmp_path, now_utc=now, fetcher=changed_fetcher)


def test_08_missing_interval_blocks(tmp_path):
    dt = F.WARMUP_START
    seal_raw_object(
        tmp_path,
        interval_start_utc=F._iso(dt),
        interval_end_utc=F._iso(dt + F.HOUR),
        raw=raw_hour(dt),
        acquisition_time_utc="2026-10-06T12:00:00Z",
        classification="WARMUP",
    )
    with pytest.raises(F.FC01Blocked, match="MISSING_INTERVAL"):
        F._ensure_exact_coverage(
            tmp_path,
            F.WARMUP_START + 2 * F.HOUR,
            datetime(2026, 10, 6, 12, tzinfo=timezone.utc),
        )


def test_09_post_horizon_object_blocks(tmp_path):
    dt = F.FIXED_END
    seal_raw_object(
        tmp_path,
        interval_start_utc=F._iso(dt),
        interval_end_utc=F._iso(dt + F.HOUR),
        raw=raw_hour(dt),
        acquisition_time_utc="2027-10-06T12:00:00Z",
        classification="FORWARD_EVIDENCE",
    )
    with pytest.raises(F.FC01Blocked, match="POST_HORIZON_CONTAMINATION"):
        F._ensure_exact_coverage(
            tmp_path,
            F.FIXED_END,
            F.FIXED_END + 2 * F.HOUR,
        )


def test_10_future_of_clock_existing_object_blocks(tmp_path):
    dt = F.WARMUP_START
    seal_raw_object(
        tmp_path,
        interval_start_utc=F._iso(dt),
        interval_end_utc=F._iso(dt + F.HOUR),
        raw=raw_hour(dt),
        acquisition_time_utc="2026-10-05T14:30:00Z",
        classification="WARMUP",
    )
    with pytest.raises(F.FC01Blocked, match="FUTURE_OF_CLOCK"):
        F._ensure_exact_coverage(
            tmp_path,
            F.WARMUP_START + F.HOUR,
            F.WARMUP_START + timedelta(minutes=30),
        )


def test_11_contract_exact_fixed_horizon_and_authority():
    c = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert c["window"]["evidence_start_utc"] == "2026-10-06T11:00:00Z"
    assert c["window"]["evidence_end_exclusive_utc"] == "2027-10-06T11:00:00Z"
    assert c["window"]["future_of_clock_acquisition"] is False
    assert c["window"]["post_horizon_confirmatory_acquisition"] is False
    assert c["authority"]["periodic_real_tc01_read"] is False
    assert c["authority"]["continuous_trade_count_monitoring"] is False
    assert c["authority"]["b12"] == "CLOSED"
    assert c["authority"]["force"] is False


def test_12_authorization_binds_uploaded_human_decision():
    a = json.loads(AUTH.read_text(encoding="utf-8"))
    assert a["source_human_decision_sha256"] == "53e3a157d20135c45ddda0f6c5a18b03185a551b2aaa16fed2132d68a1d35ad9"
    assert a["decision"] == "OPEN_AO_E0_B12_DATA01_FC01_AUTHORIZED"
    assert a["reference_planning_n"] == 58927
    assert a["reference_planning_n_is_terminal_authority"] is False
    assert a["b12"] == "CLOSED"


def test_13_runtime_imports_no_tc01_dr01_or_performance_runtime():
    tree = ast.parse(RUNTIME.read_text(encoding="utf-8"))
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module)
    joined = " ".join(imported).lower()
    for token in ("tc01", "dr01", "m04", "m05", "e1_04", "e1_05"):
        assert token not in joined


def test_14_default_root_is_durable_not_temp():
    assert str(F.DEFAULT_ROOT).lower().endswith(r"atds-data\data01-fc01")
    assert "temp" not in str(F.DEFAULT_ROOT).lower()
    assert "tmp" not in str(F.DEFAULT_ROOT).lower()


def test_15_source_binding_exact():
    c = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert c["source"] == {
        "provider": "DUKASCOPY",
        "transport": "JETTA_DUKASCOPY_TICKS_API",
        "instrument": "USATECH.IDX-USD",
        "transformation_id": "DUKASCOPY_CANONICAL_DECODE_IDENTITY_V0_1",
        "multiplier": "0.001",
        "source_substitution": False,
    }


def test_16_daily_catchup_and_weekly_replay_are_preregistered():
    c = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert c["cadence"]["collection"] == "DAILY_WITH_AUTOMATIC_CATCH_UP"
    assert c["cadence"]["structural_materialization"] == "EACH_SUCCESSFUL_DAILY_CYCLE"
    assert c["cadence"]["deterministic_full_replay"] == "FIRST_CYCLE_AND_AT_LEAST_EVERY_7_DAYS"


def test_17_failure_receipt_is_nonperformance(tmp_path):
    def fail(cache: Path, dt: datetime):
        raise F.FC01Blocked("NETWORK_DOWN")

    with pytest.raises(F.FC01Blocked, match="NETWORK_DOWN"):
        F.collect_cycle(
            tmp_path,
            now_utc=datetime(2026, 10, 6, 12, 30, tzinfo=timezone.utc),
            fetcher=fail,
        )
    files = list((tmp_path / "evidence" / "errors").glob("*.json"))
    assert len(files) == 1
    x = json.loads(files[0].read_text(encoding="utf-8"))
    assert x["b12"] == "CLOSED"
    assert x["performance_bearing_read"] is False
    assert "pnl" not in json.dumps(x).lower()


def test_18_fixed_horizon_reached_only_at_exact_end():
    before = F.target_end_for(datetime(2027, 10, 6, 10, 59, tzinfo=timezone.utc))
    after = F.target_end_for(datetime(2027, 10, 6, 11, 1, tzinfo=timezone.utc))
    assert before == datetime(2027, 10, 6, 10, tzinfo=timezone.utc)
    assert after == F.FIXED_END
