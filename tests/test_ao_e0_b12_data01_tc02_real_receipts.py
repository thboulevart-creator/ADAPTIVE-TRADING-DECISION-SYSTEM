from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "reports" / "program"

FILES = {
    "input_manifest": P / "2026-10-07-AO-E0-B12-DATA-01-TC-02-REAL-INPUT-MANIFEST-V0.1.json",
    "primary_result": P / "2026-10-07-AO-E0-B12-DATA-01-TC-02-PRIMARY-RESULT-V0.1.json",
    "reference_result": P / "2026-10-07-AO-E0-B12-DATA-01-TC-02-REFERENCE-RESULT-V0.1.json",
    "parity_receipt": P / "2026-10-07-AO-E0-B12-DATA-01-TC-02-PRIMARY-REFERENCE-PARITY-V0.1.json",
    "firewall_receipt": P / "2026-10-07-AO-E0-B12-DATA-01-TC-02-AUTHORITY-FIREWALL-V0.1.json",
    "execution_receipt": P / "2026-10-07-AO-E0-B12-DATA-01-TC-02-REAL-EXECUTION-RECEIPT-V0.1.json",
    "technical_qualification": P / "2026-10-07-AO-E0-B12-DATA-01-TC-02-TECHNICAL-QUALIFICATION-V0.1.json",
}
HASHES = P / "2026-10-07-AO-E0-B12-DATA-01-TC-02-EVIDENCE-HASHES-V0.1.json"

def j(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def sha256_file(path: Path):
    rel = path.relative_to(ROOT).as_posix()
    raw = subprocess.check_output(["git", "-C", str(ROOT), "show", f"HEAD:{rel}"])
    return hashlib.sha256(raw).hexdigest()

def git_blob(path: str):
    return subprocess.check_output(
        ["git", "-C", str(ROOT), "hash-object", path],
        text=True,
    ).strip()

def test_01_evidence_hashes_exact():
    expected = j(HASHES)
    assert set(expected) == set(FILES)
    for key, path in FILES.items():
        assert sha256_file(path) == expected[key]

def test_02_primary_output_surface_exact():
    assert set(j(FILES["primary_result"])) == {
        "cumulative_closed_trade_count",
        "reference_planning_n_reached",
        "bound_input_identity_digest",
        "count_trace_digest",
    }

def test_03_reference_output_surface_exact():
    assert set(j(FILES["reference_result"])) == {
        "cumulative_closed_trade_count",
        "reference_planning_n_reached",
    }

def test_04_primary_reference_count_parity():
    p = j(FILES["primary_result"])
    r = j(FILES["reference_result"])
    assert p["cumulative_closed_trade_count"] == r["cumulative_closed_trade_count"]

def test_05_reference_n_status_parity():
    p = j(FILES["primary_result"])
    r = j(FILES["reference_result"])
    assert p["reference_planning_n_reached"] == r["reference_planning_n_reached"]

def test_06_parity_receipt_pass():
    x = j(FILES["parity_receipt"])
    assert x["count_parity"] is True
    assert x["reference_n_status_parity"] is True
    assert x["pass"] is True

def test_07_single_real_read_consumed():
    x = j(FILES["execution_receipt"])
    assert x["status"] == "REAL_STRUCTURAL_READ_EXECUTED_ONCE"
    assert x["real_read_count"] == 1
    assert x["tc02_read_token"] == "CONSUMED"

def test_08_reference_n_not_terminal_authority():
    x = j(FILES["execution_receipt"])
    assert x["reference_planning_n"] == 58927
    assert x["reference_planning_n_is_terminal_authority"] is False

def test_09_firewall_closed():
    x = j(FILES["firewall_receipt"])
    assert x["b12"] == "CLOSED"
    assert x["performance_bearing_read"] is False
    assert x["oos_performance_consumption"] is False
    assert x["real_forward_performance_observation"] is False
    assert x["pipe01_first_performance_read"] is False
    assert x["dr01_invoked"] is False
    assert x["m04_m05_real_forward_inference"] is False
    assert x["force"] is False

def test_10_no_price_pnl_returns_exposed():
    x = j(FILES["firewall_receipt"])
    assert x["price_output_exposed"] is False
    assert x["pnl_output_exposed"] is False
    assert x["returns_exposed"] is False
    assert x["expectancy_exposed"] is False

def test_11_input_window_exact():
    x = j(FILES["input_manifest"])
    assert x["evidence_start_utc"] == "2026-10-06T11:00:00Z"
    assert x["snapshot_end_exclusive_utc"] == "2026-10-06T20:00:00Z"
    assert x["first_decision_capable_boundary_utc"] == "2026-10-06T19:00:00Z"

def test_12_input_identity_exact():
    x = j(FILES["input_manifest"])
    assert x["raw_forward_inventory_digest"] == "504b910a05d8a6420175b016253547faa83bf126099d75ed813f4da6fdfbac0c"
    assert x["raw_forward_manifest_sha256"] == "b2fecce7fd607885e6874e27b0afe9dd91ae14f052ef327b1f430c64773d14af"
    assert x["ap0_forward_manifest_sha256"] == "9c7d54026a08856485ef1ff59bcea40a358737dfbf1cd30e2c5c05353ab01de6"
    assert x["h1_forward_stream_sha256"] == "2fcbad3719c3825101f8159ec707c694700c5f14cb7be62c3a2e1f1c9129211c"

def test_13_input_is_decision_capable():
    x = j(FILES["input_manifest"])
    assert x["max_supplied_continuity_ordinal"] >= 20
    assert x["h1_rows_supplied"] == 27
    assert x["raw_ticks_supplied"] > 0

def test_14_v02_blobs_exact():
    x = j(FILES["input_manifest"])["v0_2_blobs"]
    assert x["m06"] == git_blob("GOVERNANCE/AO-E0-B8-M06-02-SAMPLE-ADEQUACY-PREREGISTRATION-V0.2.json")
    assert x["data01"] == git_blob("GOVERNANCE/AO-E0-B12-DATA-01-PROSPECTIVE-FORWARD-INSTANCE-FORMATION-CONTRACT-V0.2.json")
    assert x["dr01"] == git_blob("GOVERNANCE/AO-E0-B8-DR-01-FINAL-QUALIFICATION-DECISION-RULE-V0.2.json")
    assert x["tc01"] == git_blob("GOVERNANCE/AO-E0-B12-DATA-01-TC-01-COUNT-ONLY-CONTRACT-V0.2.json")

def test_15_technical_qualification_pass():
    x = j(FILES["technical_qualification"])
    assert x["tc02_real_structural_read"] == "PASS"
    assert x["input_binding"] == "PASS"
    assert x["fixed_window_enforcement"] == "PASS"
    assert x["primary_reference_parity"] == "PASS"
    assert x["output_surface"] == "COUNT_ONLY"
    assert x["no_performance_exposure"] == "PASS"
    assert x["no_dr01_inference"] == "PASS"

def test_16_stop_preserved():
    x = j(FILES["technical_qualification"])
    assert x["b12"] == "CLOSED"
    assert x["strategy_qualified"] == "NO_CLAIM"
    assert x["stop"] == "HUMAN_DECISION_REQUIRED"

def test_17_primary_result_has_no_performance_keys():
    keys = {k.lower() for k in j(FILES["primary_result"])}
    forbidden = {
        "price","entry_price","exit_price","pnl","gross_pnl","net_pnl",
        "return","returns","expectancy","win_rate","profit_factor",
        "drawdown","support","refute","confidence_interval","p_value",
    }
    assert not keys.intersection(forbidden)

def test_18_reference_result_has_no_performance_keys():
    keys = {k.lower() for k in j(FILES["reference_result"])}
    assert keys == {"cumulative_closed_trade_count", "reference_planning_n_reached"}

def test_19_input_manifest_is_nonperformance():
    x = j(FILES["input_manifest"])
    assert x["read_class"] == "REAL_FORWARD_STRUCTURAL_COUNT_ONLY"
    assert x["performance_bearing_read"] is False
    assert x["b12"] == "CLOSED"

def test_20_execution_receipt_matches_input_digest():
    x = j(FILES["execution_receipt"])
    m = j(FILES["input_manifest"])
    assert x["input_manifest_digest"] == m["input_manifest_digest"]
