from __future__ import annotations
import copy, importlib.util, json, pathlib, sys, tempfile, unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
CALC=ROOT/"tools/bepd_04b_same_week_reintegration_response_v0_1.py"
FIXTURE=ROOT/"tests/fixtures/bepd_04b_same_week_reintegration_synthetic_v0_1.json"
if not CALC.exists():
    raise RuntimeError("BEPD04B_RUNTIME_ABSENT_EXPECTED_RED")
spec=importlib.util.spec_from_file_location("bepd04b_calc",CALC)
mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(mod)

def enrich(row):
    z=dict(row); z["schema_version"]="ATDS_BEPD_01D_HISTORICAL_LEDGER_SCHEMA_V0_1"; z["run_id"]="SYNTHETIC_BEPD04B_RUN_V0_1"; return z

class TestBEPD04B(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fx=json.loads(FIXTURE.read_text())
    def context(self):
        return {"execution_scope":"SYNTHETIC_QUALIFICATION","source_ledger_blob":"SYNTHETIC_BEPD04B_LEDGER_V0_1","source_run_id":"SYNTHETIC_BEPD04B_RUN_V0_1"}
    def calc(self,rows,options=None):
        return mod.summarize_rows([enrich(x) for x in rows],self.context(),options=options)
    def test_frozen_synthetic_cases(self):
        for c in self.fx["cases"]:
            with self.subTest(case=c["id"]):
                r=self.calc(c["rows"]); e=c["expected"]
                self.assertEqual(r["total_event_count"],e["total"]); self.assertEqual(r["reintegration_true_count"],e["true"]); self.assertEqual(r["reintegration_false_count"],e["false"]); self.assertEqual(r["reintegration_fraction"],e["fraction"]); self.assertEqual(r["reintegration_share_decimal"],e["share_decimal"]); mod.validate_result(r)
    def test_deterministic_repeated_execution(self):
        rows=self.fx["cases"][-1]["rows"]; self.assertEqual(self.calc(rows),self.calc(rows))
    def test_missing_required_fields_fail(self):
        base=enrich(self.fx["cases"][0]["rows"][0])
        for k in mod.REQUIRED_FIELDS:
            with self.subTest(field=k):
                z=dict(base); z.pop(k); self.assertRaisesRegex(mod.ResponseFailure,"MISSING_REQUIRED_FIELD",mod.summarize_rows,[z],self.context())
    def test_duplicate_event_id_fails(self):
        a=enrich(self.fx["cases"][0]["rows"][0]); b=dict(a); self.assertRaisesRegex(mod.ResponseFailure,"DUPLICATE_EVENT_ID",mod.summarize_rows,[a,b],self.context())
    def test_non_boolean_response_fails(self):
        a=enrich(self.fx["cases"][0]["rows"][0]); a["same_week_reintegration"]=1; self.assertRaisesRegex(mod.ResponseFailure,"NON_BOOLEAN_RESPONSE",mod.summarize_rows,[a],self.context())
    def test_empty_fails(self): self.assertRaisesRegex(mod.ResponseFailure,"EMPTY_INPUT",mod.summarize_rows,[],self.context())
    def test_schema_drift_fails(self):
        a=enrich(self.fx["cases"][0]["rows"][0]); a["schema_version"]="DRIFT"; self.assertRaisesRegex(mod.ResponseFailure,"UNEXPECTED_SCHEMA_VERSION",mod.summarize_rows,[a],self.context())
    def test_run_id_drift_fails(self):
        a=enrich(self.fx["cases"][0]["rows"][0]); a["run_id"]="DRIFT"; self.assertRaisesRegex(mod.ResponseFailure,"RUN_ID_MISMATCH",mod.summarize_rows,[a],self.context())
    def test_source_blob_drift_fails(self):
        a=enrich(self.fx["cases"][0]["rows"][0]); c=self.context(); c["source_ledger_blob"]="DRIFT"; self.assertRaisesRegex(mod.ResponseFailure,"SOURCE_LEDGER_BLOB_MISMATCH",mod.summarize_rows,[a],c)
    def test_invalid_side_fails(self):
        a=enrich(self.fx["cases"][0]["rows"][0]); a["side"]="BOTH"; self.assertRaisesRegex(mod.ResponseFailure,"INVALID_SIDE",mod.summarize_rows,[a],self.context())
    def test_invalid_required_string_fails(self):
        a=enrich(self.fx["cases"][0]["rows"][0]); a["event_id"]=""; self.assertRaisesRegex(mod.ResponseFailure,"INVALID_REQUIRED_STRING",mod.summarize_rows,[a],self.context())
    def test_unauthorized_options_fail(self):
        for opt in ["group_by","take_comparator","reintegration_comparator","allow_same_bar","response_horizon","estimand","m05","interpretation","execution_price","close_displacement","future_probability","strategy"]:
            with self.subTest(option=opt): self.assertRaisesRegex(mod.ResponseFailure,"UNAUTHORIZED_OPTION",self.calc,self.fx["cases"][0]["rows"],{opt:True})
    def test_result_reconciliation_fails_closed(self):
        r=self.calc(self.fx["cases"][2]["rows"]); r["reintegration_true_count"]+=1; self.assertRaisesRegex(mod.ResponseFailure,"RESULT_RECONCILIATION_FAIL",mod.validate_result,r)
    def test_forbidden_result_surface_fails_closed(self):
        r=self.calc(self.fx["cases"][0]["rows"]); r["p_value"]=0.01; self.assertRaisesRegex(mod.ResponseFailure,"FORBIDDEN_RESULT_SURFACE",mod.validate_result,r)

if __name__=="__main__": unittest.main()
