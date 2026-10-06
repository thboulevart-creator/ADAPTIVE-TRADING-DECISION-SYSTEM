from __future__ import annotations
import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
FIX=json.loads((ROOT/"tests/fixtures/bepd_04f_response_nonstationarity_gate_synthetic_v0_1.json").read_text())
try:
    from tools.bepd_04f_response_nonstationarity_gate_v0_1 import evaluate_gate
except Exception as exc:
    raise RuntimeError("BEPD04F_RUNTIME_ABSENT_EXPECTED_RED") from exc

def req(case):
    x=copy.deepcopy(FIX["base_request"]); c=FIX["cases"][case]
    for k,v in c.get("patch",{}).items(): x[k]=copy.deepcopy(v)
    for k in c.get("remove",[]): x.pop(k,None)
    return x,c

class TestBEPD04F(unittest.TestCase):
    def test_substantive_states(self):
        for name in ("S01_STABLE_EXACT_SPREAD_0_10","S02_STABLE_ZERO_SPREAD","S03_STABLE_BELOW_THRESHOLD","S04_UNSTABLE_ABOVE_THRESHOLD","S05_ONE_STRATUM_N29","S06_ONE_STRATUM_N30","S07_MULTIPLE_INSUFFICIENT"):
            x,c=req(name); o=evaluate_gate(x)
            self.assertEqual(o["state"],c["expected_state"],name)
            self.assertEqual(o["structural_validation_status"],"PASS")
    def test_exact_spread_boundary(self):
        o=evaluate_gate(req("S01_STABLE_EXACT_SPREAD_0_10")[0])
        self.assertEqual(o["maximum_spread"],"0.10")
        self.assertEqual(o["spread_classification"],"WITHIN_ADOPTED_TOLERANCE")
    def test_n30_boundary(self):
        o=evaluate_gate(req("S06_ONE_STRATUM_N30")[0])
        self.assertEqual(o["sample_adequacy"],"PASS")
    def test_m04_semantics(self):
        o=evaluate_gate(req("S02_STABLE_ZERO_SPREAD")[0])
        self.assertEqual(o["m04_status"],"NOT_APPLICABLE_BY_REPRESENTATION")
        self.assertFalse(o["m04_executed"])
    def test_fail_closed_cases(self):
        for name,c in FIX["cases"].items():
            if not name.startswith("B"): continue
            x,_=req(name)
            with self.assertRaisesRegex(ValueError,c["expected_error"],msg=name):
                evaluate_gate(x)
    def test_deterministic_replay(self):
        x,_=req("S03_STABLE_BELOW_THRESHOLD")
        self.assertEqual(evaluate_gate(x),evaluate_gate(x))
if __name__=="__main__": unittest.main()
