from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "reports" / "program"

def load(name):
    return json.loads((R / name).read_text(encoding="utf-8-sig"))

def test_controller_probe_is_discriminant():
    rows = load("2026-10-06-SMF-AP1-M03-02-R1-EF-01-CONTROLLER-PROBES-V0.1.json")
    hist = {r["requested"]: r["exit_code"] for r in rows if r["pattern"] == "historical"}
    fixed = {r["requested"]: r["exit_code"] for r in rows if r["pattern"] == "wait_passthru"}
    assert hist == {0: None, 2: None, 3: None}
    assert fixed == {0: 0, 2: 2, 3: 3}

def test_executor_and_bootstrap_control_flow():
    p = load("2026-10-06-SMF-AP1-M03-02-R1-EF-01-CONTROL-FLOW-PROBES-V0.1.json")
    cases = {x["case"]: x["return_code"] for x in p["executor_cases"]}
    assert cases == {"PASS": 0, "FAIL": 3, "EXCEPTION": 2}
    propagation = {x["requested_system_exit"]: x["system_exit_code"] for x in p["bootstrap_systemexit_propagation"]}
    assert propagation == {0: 0, 2: 2, 3: 3}

def test_adjudication_preserves_exit_code_semantics():
    a = load("2026-10-06-SMF-AP1-M03-02-R1-EF-01-ADJUDICATION-RECEIPT-V0.1.json")
    assert a["status"] == "EVIDENCE_SUFFICIENT_EXECUTION_QUALIFIED"
    assert a["execution_evidence"]["direct_exit_code_observation"] == "UNAVAILABLE"
    assert a["execution_evidence"]["direct_exit_code_value"] is None
    assert a["adjudication"]["observed_exit_code_fabricated"] is False
    assert a["adjudication"]["execution_success"] == "QUALIFIED_BY_INDEPENDENT_CONVERGENT_EXECUTION_EVIDENCE"
    assert a["adjudication"]["scientific_interpretation"] == "NOT_YET_ADOPTED"
    assert all(x["status"] == "PASS" for x in a["sufficiency_conditions"])

def test_parity_and_boundaries_preserved():
    a = load("2026-10-06-SMF-AP1-M03-02-R1-EF-01-ADJUDICATION-RECEIPT-V0.1.json")
    assert a["parity"] == {
        "overall": "PASS",
        "pass_count": 1925,
        "fail_count": 0,
        "not_comparable_count": 165,
        "max_abs_diff": 0.0,
    }
    assert not any(a["boundaries"].values())
