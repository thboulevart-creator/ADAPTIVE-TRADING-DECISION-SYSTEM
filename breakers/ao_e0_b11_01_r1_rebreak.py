from __future__ import annotations
import json
from pathlib import Path

from src import p1_12c_ao_e0_native_owner as owner
from src import p1_12d_ao_e0_extension as ext

ROOT=Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

CONTRACT=load("GOVERNANCE/AO-E0-B11-01-R1-OWNER-REBIND-CLOSURE-CONTRACT-V0.1.json")
OWNER_RECEIPT=load("reports/program/2026-10-05-AO-E0-P1-OWNER-01-QUALIFICATION-RECEIPT-V0.1.json")
OLD_BLOCKER=load("reports/program/2026-10-05-AO-E0-B11-01-REPRODUCIBILITY-BLOCKER-RECEIPT-V0.1.json")
DT=load("reports/program/2026-10-05-AO-E0-DT-01-B6-B10-CLOSURE-RECEIPT-V0.1.json")
SMF=load("GOVERNANCE/AO-E0-B11-01-SMF-ACTIVATION-MATRIX-V0.1.json")

def rebreak():
    assert OLD_BLOCKER["verdict"]=="BLOCKED"
    assert OLD_BLOCKER["blocker"]=="BLOCKED_P1_CC05_NATIVE_EXECUTION_OWNER_NOT_QUALIFIED"

    assert OWNER_RECEIPT["verdict"]=="QUALIFIED_SYNTHETICALLY_PRE_EXECUTION"
    assert OWNER_RECEIPT["native_owner_id"]=="P1.12C.AO-E0"
    assert OWNER_RECEIPT["green"]["conclusion"]=="SUCCESS"
    assert OWNER_RECEIPT["green"]["real_ao_e0_output"]=="ABSENT"

    assert owner.OWNER_ID=="P1.12C.AO-E0"
    assert owner.CELL_IDENTITY==CONTRACT["cell_identity"]
    assert owner.CLAIM_CLASS==CONTRACT["claim_class"]
    assert ext.AO_E0_ALLOWED_OWNER=="P1.12C.AO-E0"
    assert ext.BASE_ALLOWED_OWNERS==("P1.12B","P1.12C")

    assert DT["closures"]["b6"]=="CLOSED"
    assert DT["closures"]["b10"]=="CLOSED"

    states={m["method"]:m["state"] for m in SMF["methods"]}
    assert states["M01"]=="ACTIVATED_REQUIRED"
    assert states["M02"]=="ACTIVATED_REQUIRED"
    assert states["M04"]=="ACTIVATED_REQUIRED"
    assert states["M05"]=="PREDECLARED_CONDITIONAL_ACTIVATION"
    assert states["M06"]=="BINDING_REQUIRED_EXECUTION_BLOCKED_PENDING_B8_NUMERIC_CONFIGURATION"
    assert states["M07"]=="ACTIVATED_REQUIRED"
    assert states["M08"]=="ACTIVATED_REQUIRED"
    assert states["M09"]=="BINDING_REQUIRED_EXECUTION_BLOCKED_PENDING_B8_AND_B12"
    assert states["M10"]=="NOT_APPLICABLE_TO_BASE_CC05"
    assert states["M11"]=="BINDING_REQUIRED_EXECUTION_BLOCKED_PENDING_B9"
    assert SMF["conditional_families"]["C01-C12"]=="DORMANT_BY_DEFAULT"

    assert CONTRACT["preserved_gates"]["b7"]=="OPEN"
    assert CONTRACT["preserved_gates"]["b8"]=="OPEN"
    assert CONTRACT["preserved_gates"]["b9"]=="OPEN"
    assert CONTRACT["preserved_gates"]["b12"]=="CLOSED"
    assert all(v is False for v in CONTRACT["authority"].values())
    assert all(CONTRACT["semantics"].values())

    return {
        "status":"PASS",
        "old_blocker":"CLOSED_BY_AO_E0_P1_OWNER_01",
        "b11":"CLOSED",
        "b7":"OPEN",
        "b8":"OPEN",
        "b9":"OPEN",
        "b12":"CLOSED",
        "ao_e0_execution":"NOT_AUTHORIZED",
        "oos_consumption":"NOT_AUTHORIZED",
        "performance_observation":"NOT_AUTHORIZED",
    }

def test_rebreak():
    assert rebreak()["b11"]=="CLOSED"
