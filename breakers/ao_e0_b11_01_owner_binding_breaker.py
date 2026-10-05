from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text(encoding="utf-8"))
C=load("GOVERNANCE/AO-E0-B11-01-EXACT-OWNER-BINDING-CONTRACT-V0.1.json")
RVO=load("GOVERNANCE/AO-E0-B11-01-RVO-CC05-ROUTING-RECORD-V0.1.json")
P1=load("GOVERNANCE/AO-E0-B11-01-P1-COMMON-DOWNSTREAM-BINDING-V0.1.json")
SMF=load("GOVERNANCE/AO-E0-B11-01-SMF-ACTIVATION-MATRIX-V0.1.json")
CELL="sha256:38610ff2afd70998a7fa3e522575faf697ec3159e00829c2b2bbd5da45c52054"
def run():
    assert C["cell_identity"]==CELL and C["claim_class"]=="CC05_ECONOMIC_NET_PROFITABILITY"
    assert C["status"]=="BLOCKED"
    assert C["bindings"]["data"]["b10"]=="CLOSED" and C["bindings"]["temporal"]["b6"]=="CLOSED"
    assert C["bindings"]["execution"]["generic_execution_substitution"] is False
    assert C["bindings"]["p1"]["blocker"]=="BLOCKED_P1_CC05_NATIVE_EXECUTION_OWNER_NOT_QUALIFIED"
    assert P1["status"]=="BLOCKED_OWNER_GAP"
    assert P1["native_owner_requirements"]["ao_e0_exact_native_owner_available"] is False
    assert P1["p1_12c_incompatibility"]["required_temporal_scope_literal"]=="RETROSPECTIVE_DESCRIPTIVE_ONLY"
    assert P1["p1_12c_incompatibility"]["cc05_or_oos_temporal_escalation"]=="BLOCKED_TEMPORAL_SCOPE_ESCALATION"
    assert all(P1["preserved"].values())
    states={m["method"]:m["state"] for m in SMF["methods"]}
    assert states["M01"]=="ACTIVATED_REQUIRED" and states["M02"]=="ACTIVATED_REQUIRED"
    assert states["M04"]=="ACTIVATED_REQUIRED" and states["M05"]=="PREDECLARED_CONDITIONAL_ACTIVATION"
    assert states["M06"].endswith("B8_NUMERIC_CONFIGURATION")
    assert states["M07"]=="ACTIVATED_REQUIRED" and states["M08"]=="ACTIVATED_REQUIRED"
    assert states["M09"].endswith("B8_AND_B12")
    assert states["M10"]=="NOT_APPLICABLE_TO_BASE_CC05"
    assert states["M11"].endswith("B9")
    assert SMF["conditional_families"]["C01-C12"]=="DORMANT_BY_DEFAULT"
    assert all(RVO["separations"].values())
    assert C["closures"]=={"b11":"BLOCKED","b7":"OPEN","b8":"OPEN","b9":"OPEN","b12":"CLOSED"}
    assert all(v is False for v in C["authority"].values())
    print("AO_E0_B11_01_BREAKER_PASS")
if __name__=="__main__": run()
