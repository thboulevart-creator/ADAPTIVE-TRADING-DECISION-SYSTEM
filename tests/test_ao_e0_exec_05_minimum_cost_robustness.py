import importlib.util
from pathlib import Path

R=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("m",R/"tools"/"ao_e0_exec_05_minimum_cost_robustness.py")
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)

def test_node():
    assert m.required_node()==("F2_S4",2.0,4.0)

def test_support():
    assert m.evaluate("SUPPORTED")=="PASS"

def test_refute():
    assert m.evaluate("REFUTED")=="FAIL"

def test_inconclusive():
    assert m.evaluate("INCONCLUSIVE")=="INCONCLUSIVE"

def test_no_oos():
    assert m.AUTHORITY["oos_consumption_authorized"] is False
