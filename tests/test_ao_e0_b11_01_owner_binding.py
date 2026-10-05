import importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("b",R/"breakers"/"ao_e0_b11_01_owner_binding_breaker.py")
b=importlib.util.module_from_spec(s); s.loader.exec_module(b)
def test_full_breaker(): b.run()
def test_b11_blocked_exactly(): assert b.C["closures"]["b11"]=="BLOCKED"
def test_p1_owner_gap_exact(): assert b.C["bindings"]["p1"]["blocker"]=="BLOCKED_P1_CC05_NATIVE_EXECUTION_OWNER_NOT_QUALIFIED"
def test_no_generic_execution_substitution(): assert b.C["bindings"]["execution"]["generic_execution_substitution"] is False
def test_m11_not_bypassed(): assert next(x for x in b.SMF["methods"] if x["method"]=="M11")["state"].endswith("B9")
def test_m09_not_oos_authority(): assert next(x for x in b.SMF["methods"] if x["method"]=="M09")["state"].endswith("B8_AND_B12")
def test_m10_not_cost_stress_conflated(): assert next(x for x in b.SMF["methods"] if x["method"]=="M10")["state"]=="NOT_APPLICABLE_TO_BASE_CC05"
def test_conditional_dormant(): assert b.SMF["conditional_families"]["C01-C12"]=="DORMANT_BY_DEFAULT"
def test_no_authority(): assert all(v is False for v in b.C["authority"].values())
