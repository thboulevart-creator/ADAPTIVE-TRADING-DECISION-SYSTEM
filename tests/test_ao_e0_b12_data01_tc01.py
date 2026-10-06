from __future__ import annotations

import ast
import copy
import importlib.util
import json
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PRIMARY_PATH = ROOT / "tools/ao_e0_b12_data01_tc01_count_only.py"
REFERENCE_PATH = ROOT / "tools/ao_e0_b12_data01_tc01_reference.py"
CONTRACT_PATH = ROOT / "GOVERNANCE/AO-E0-B12-DATA-01-TC-01-COUNT-ONLY-CONTRACT-V0.1.json"
BREAKERS_PATH = ROOT / "GOVERNANCE/AO-E0-B12-DATA-01-TC-01-FROZEN-BREAKERS-V0.1.json"
M06_REVIEW_PATH = ROOT / "GOVERNANCE/AO-E0-B8-M06-TR-01-OPERATIONAL-COHERENCE-REVIEW-V0.1.json"
AUTH_PATH = ROOT / "GOVERNANCE/AO-E0-TC01-M06-TR01-HUMAN-AUTHORIZATION-RECEIPT-V0.1.json"

H1_ID = "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1"
HOUR = 3_600_000
FIRST = 1_791_284_400_000
BASE = FIRST - 21 * HOUR


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P = load(PRIMARY_PATH, "tc01_primary")
R = load(REFERENCE_PATH, "tc01_reference")


def rows(n=24, block=1):
    return [
        {
            "h1_start_ms_utc": BASE + i * HOUR,
            "source_segment_id": 1,
            "continuity_block_id": block,
            "continuity_ordinal": i,
            "mid_close": 100.0,
        }
        for i in range(n)
    ]


def tick(ts, bid=99.0, ask=101.0, continuity="OK"):
    return {
        "timestamp_ms": ts,
        "bid": bid,
        "ask": ask,
        "continuity_status": continuity,
    }


def alternating_fixture():
    h = rows(24)
    h[20]["mid_close"] = 101.0
    h[21]["mid_close"] = 99.0
    h[22]["mid_close"] = 101.0
    h[23]["mid_close"] = 99.0
    ticks = [tick(h[i]["h1_start_ms_utc"] + HOUR) for i in range(20, 24)]
    return h, ticks


def public(h, ticks, **kwargs):
    return P.run_count_only(h, raw_ticks=ticks, e1_03_identity=H1_ID, **kwargs)


def core(h, ticks, threshold, **kwargs):
    return P._run_count_only_core(
        h,
        raw_ticks=ticks,
        first_evidence_decision_time_ms=kwargs.get("first", FIRST),
        initial_position=kwargs.get("initial", 0),
        required_closed_trades=threshold,
    )


def ref(h, ticks, threshold=58927, **kwargs):
    return R.reference_count_only(
        h,
        raw_ticks=ticks,
        e1_03_identity=H1_ID,
        first_evidence_decision_time_ms=kwargs.get("first", FIRST),
        initial_position=kwargs.get("initial", 0),
        required_closed_trades=threshold,
    )


def _json(path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "current,target,expected_status,expected_close",
    [
        (0, 1, "EXECUTED", 0),
        (0, -1, "EXECUTED", 0),
        (1, 0, "EXECUTED", 1),
        (-1, 0, "EXECUTED", 1),
        (1, -1, "EXECUTED", 1),
        (-1, 1, "EXECUTED", 1),
        (1, 1, "HOLD", 0),
        (-1, -1, "HOLD", 0),
        (0, 0, "HOLD", 0),
    ],
)
def test_01_transition_table(current, target, expected_status, expected_close):
    status = P._structural_transition(current, target, FIRST, [tick(FIRST)])
    assert status == expected_status
    inc = int(status == "EXECUTED" and current != 0 and target != current)
    assert inc == expected_close


def test_02_long_short_reversal_counts_one():
    h, ticks = alternating_fixture()
    out = core(h[:22], ticks, 10)
    assert out["cumulative_closed_trade_count"] == 1


def test_03_short_long_reversal_counts_one():
    h, ticks = alternating_fixture()
    out = core(h[:23], ticks, 10)
    assert out["cumulative_closed_trade_count"] == 2


def test_04_long_flat_counts_one():
    h = rows(22)
    h[20]["mid_close"] = 101.0
    h[21]["mid_close"] = 100.0
    ticks = [tick(h[i]["h1_start_ms_utc"] + HOUR) for i in (20, 21)]
    assert core(h, ticks, 10)["cumulative_closed_trade_count"] == 1


def test_05_short_flat_counts_one():
    h = rows(22)
    h[20]["mid_close"] = 99.0
    h[21]["mid_close"] = 100.0
    ticks = [tick(h[i]["h1_start_ms_utc"] + HOUR) for i in (20, 21)]
    assert core(h, ticks, 10)["cumulative_closed_trade_count"] == 1


def test_06_flat_long_is_open_only():
    h = rows(21)
    h[20]["mid_close"] = 101.0
    out = core(h, [tick(FIRST)], 10)
    assert out["cumulative_closed_trade_count"] == 0


def test_07_flat_short_is_open_only():
    h = rows(21)
    h[20]["mid_close"] = 99.0
    out = core(h, [tick(FIRST)], 10)
    assert out["cumulative_closed_trade_count"] == 0


def test_08_hold_does_not_close():
    h = rows(22)
    h[20]["mid_close"] = 101.0
    h[21]["mid_close"] = 101.0
    ticks = [tick(h[i]["h1_start_ms_utc"] + HOUR) for i in (20, 21)]
    assert core(h, ticks, 10)["cumulative_closed_trade_count"] == 0


def test_09_undefined_warmup_does_not_execute():
    h = rows(20)
    out = core(h, [], 1, first=BASE)
    assert out["cumulative_closed_trade_count"] == 0


def test_10_continuity_block_reset_restarts_warmup():
    h = rows(21)
    start = h[-1]["h1_start_ms_utc"] + HOUR
    h += [
        {
            "h1_start_ms_utc": start + i * HOUR,
            "source_segment_id": 2,
            "continuity_block_id": 2,
            "continuity_ordinal": i,
            "mid_close": 200.0 + i,
        }
        for i in range(20)
    ]
    out = core(h, [tick(FIRST)], 100)
    assert out["cumulative_closed_trade_count"] == 0


def test_11_missing_execution_opportunity_preserves_state():
    h, _ = alternating_fixture()
    out = core(h[:22], [], 10)
    assert out["cumulative_closed_trade_count"] == 0


def test_12_forbidden_boundary_prevents_execution():
    h = rows(21)
    h[20]["mid_close"] = 101.0
    out = core(h, [tick(FIRST, continuity="FORBIDDEN_BOUNDARY"), tick(FIRST + 1)], 10)
    assert out["cumulative_closed_trade_count"] == 0


def test_13_nonfinite_required_side_is_skipped_until_valid():
    assert P._structural_transition(
        0,
        1,
        FIRST,
        [tick(FIRST, ask=math.nan), tick(FIRST + 1, ask=102.0)],
    ) == "EXECUTED"


def test_14_no_pyramiding():
    with pytest.raises(P.TC01Blocked, match="PYRAMIDING_FORBIDDEN"):
        P._required_side(1, 2)


def test_15_deterministic_replay():
    h, ticks = alternating_fixture()
    assert public(h, ticks) == public(copy.deepcopy(h), copy.deepcopy(ticks))


def test_16_exact_count_accumulation():
    h, ticks = alternating_fixture()
    assert core(h, ticks, 99)["cumulative_closed_trade_count"] == 3


def test_17_exact_threshold_crossing_boundary():
    h, ticks = alternating_fixture()
    out = core(h, ticks, 2)
    expected = h[22]["h1_start_ms_utc"] + HOUR
    assert out["terminal_threshold_reached"] is True
    assert out["exact_terminal_decision_time_if_reached"] == expected
    assert out["cumulative_closed_trade_count"] == 2


def test_18_no_early_threshold_declaration():
    h, ticks = alternating_fixture()
    out = core(h[:22], ticks, 2)
    assert out["terminal_threshold_reached"] is False
    assert out["exact_terminal_decision_time_if_reached"] is None


def test_19_success_output_surface_is_exact_and_price_free():
    h, ticks = alternating_fixture()
    out = public(h, ticks)
    assert set(out) == P.ALLOWED_OUTPUT_KEYS
    forbidden = {"price", "entry_price", "exit_price", "execution_price", "trade_price"}
    assert not (set(out) & forbidden)


def test_20_no_pnl_field_reachable():
    h, ticks = alternating_fixture()
    keys = {k.lower() for k in public(h, ticks)}
    assert not (keys & {"pnl", "gross_pnl", "net_pnl", "cumulative_pnl", "profit"})


def test_21_no_return_field_reachable():
    keys = {k.lower() for k in public(*alternating_fixture())}
    assert not (keys & {"return", "returns", "trade_return", "trade_profitability"})


def test_22_no_expectancy_ci_or_verdict_surface():
    keys = {k.lower() for k in public(*alternating_fixture())}
    assert not (keys & {"expectancy", "confidence_interval", "support", "refute", "inconclusive"})


def test_23_primary_imports_no_e104_e105_pipe_or_owner_runtime():
    src = PRIMARY_PATH.read_text(encoding="utf-8")
    tree = ast.parse(src)
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module)
    joined = " ".join(imported).lower()
    for token in ("e1_04", "e1_05", "pipe", "owner"):
        assert token not in joined


def test_24_reference_is_independent_of_primary():
    src = REFERENCE_PATH.read_text(encoding="utf-8").lower()
    assert "ao_e0_b12_data01_tc01_count_only" not in src


def test_25_primary_reference_exact_parity():
    h, ticks = alternating_fixture()
    assert public(h, ticks) == ref(h, ticks)


def test_26_primary_reference_threshold_parity():
    h, ticks = alternating_fixture()
    assert core(h, ticks, 2) == ref(h, ticks, 2)


def test_27_first_forward_decision_starts_from_flat_not_warmup_position():
    h = rows(21)
    h[19]["mid_close"] = 1.0
    h[20]["mid_close"] = 101.0
    out = public(h, [tick(FIRST)])
    assert out["cumulative_closed_trade_count"] == 0


def test_28_wrong_h1_identity_fails_closed():
    h, ticks = alternating_fixture()
    with pytest.raises(P.TC01Blocked, match="E1_03_IDENTITY_MISMATCH"):
        P.run_count_only(h, raw_ticks=ticks, e1_03_identity="WRONG")


def test_29_malformed_tick_fails_closed():
    h = rows(21)
    h[20]["mid_close"] = 101.0
    with pytest.raises(P.TC01Blocked, match="MALFORMED_RAW_TICK"):
        core(h, [{"timestamp_ms": FIRST}], 10)


def test_30_public_real_threshold_is_frozen_58927():
    assert P.REQUIRED_CLOSED_TRADES == 58927
    h, ticks = alternating_fixture()
    out = public(h, ticks)
    assert out["terminal_threshold_reached"] is False


def test_31_no_real_authority_names_in_success_output():
    keys = {k.lower() for k in public(*alternating_fixture())}
    for token in ("b12", "pipe01", "owner02", "trading", "broker", "capital"):
        assert all(token not in key for key in keys)


def test_32_contract_preserves_authority_firewall():
    c = _json(CONTRACT_PATH)
    assert c["runtime"]["required_closed_trades"] == 58927
    assert c["runtime"]["structural_forward_read_class"] == "COUNT_ONLY_STRUCTURAL_READ"
    assert c["runtime"]["performance_bearing_read"] is False
    assert c["authority"]["real_tc01_forward_read"] is False
    assert c["authority"]["b12_open"] is False
    assert c["force"] is False


def test_33_breakers_are_frozen_27_and_pre_real():
    b = _json(BREAKERS_PATH)
    assert b["status"] == "FROZEN_BEFORE_ANY_REAL_TC01_FORWARD_READ"
    assert b["count"] == 27
    assert len(b["cases"]) == 27
    assert b["real_forward_read"] is False
    assert b["b12"] == "CLOSED"


def test_34_m06_review_exact_structural_lower_bound():
    r = _json(M06_REVIEW_PATH)
    lb = r["proven_structural_lower_bound"]
    assert lb["max_closed_trades_per_h1_decision"] == 1
    assert lb["minimum_elapsed_hours"] == 58927
    assert lb["earliest_terminal_utc_under_impossible_24x7_hourly_close_envelope"] == "2033-06-26T18:00:00Z"
    assert lb["classification"] == "PROVEN_STRUCTURAL_LOWER_BOUND"


def test_35_m06_review_preserves_frozen_m06_and_no_forward_read():
    r = _json(M06_REVIEW_PATH)
    g = r["governance_interpretation"]
    assert r["verdict"] == "DESIGN_DEFECT_CANDIDATE"
    assert g["m06_modified_by_review"] is False
    assert g["required_n_modified_by_review"] is False
    assert g["forward_performance_used"] is False
    assert g["real_forward_read"] is False
    assert r["authority"]["b12_open"] is False


def test_36_authorization_receipt_binds_exact_human_source():
    a = _json(AUTH_PATH)
    assert a["source_sha256"] == "02590f35fc5aafd60d28e573727975ef27d38b1c47b49923a708023cce87471e"
    assert a["branch"] == "integration/system-v1"
    assert a["hard_stop"] == "BEFORE_FIRST_REAL_TC01_FORWARD_READ"
    assert a["b12"] == "CLOSED"
