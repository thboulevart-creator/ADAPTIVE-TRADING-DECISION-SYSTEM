from __future__ import annotations
import copy, hashlib, importlib.util, json, math, pathlib, subprocess
import pytest

ROOT=pathlib.Path(__file__).resolve().parents[1]
G=ROOT/"GOVERNANCE"
CONTRACT=G/"SMF-AP1-M03-02-R1-M10-00-CLAIM-SCOPED-EXECUTABLE-BINDING-V0.1.json"
ACTIVATION=G/"SMF-AP1-M03-02-R1-M10-00-ACTIVATION-RECORD-V0.1.json"
RUNTIME=ROOT/"tools"/"smf_ap1_m03_02_r1_m10_00.py"
REFERENCE=ROOT/"tools"/"smf_ap1_m03_02_r1_m10_00_reference.py"
M01=G/"SMF-AP1-M03-02-R1-M01-01-TEMPORAL-STABILITY-CONTRACT-V0.2.json"
HUMAN=G/"SMF-AP1-M03-02-R1-M01-01-HUMAN-MATERIALITY-ADJUDICATION-V0.1.json"
EXPECTED_M01_BLOB="2293c665a2d30c520056c7814aec6a9dc79d68d1"
EXPECTED_HUMAN_BLOB="a9382bc08f354e9142ccd55308f46c86da3f1af3"
EXPECTED_M03_SHA="7d4369cdfab545f0edb94b93ad9d1d1070e6afa35a1000376af55d9c10943a9e"

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def blob(p):
 rel=p.relative_to(ROOT).as_posix()
 return subprocess.check_output(["git","rev-parse",f"HEAD:{rel}"],text=True).strip()
def mod(path,name):
 assert path.exists(), f"MISSING_IMPLEMENTATION:{path.name}"
 spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def runtime(): return mod(RUNTIME,"m10_runtime")
def reference(): return mod(REFERENCE,"m10_reference")

def synthetic(base=100.0):
 d={"bucket_evidence":{}}
 for year,mult in [(2022,1.00),(2023,1.05),(2024,1.10),(2025,1.15),(2021,9.0),(2026,9.0)]:
  yd={}
  for metric,probs in {"tick_count":[0.5,0.9,0.99],"minute_range":[0.5,0.9,0.95,0.99],"spread_mean":[0.5,0.9,0.95,0.99]}.items():
   yd[metric]={"quantiles":{str(p):base*mult*(1+p/100) for p in probs}}
  d["bucket_evidence"][f"UTC_YEAR:{year}"]=yd
 d["bucket_evidence"]["UTC_YEAR:2022"]["EXTRA"]={"quantiles":{"0.1":999}}
 return d

def claim(out,metric,p):
 return next(x for x in out["claim_units"] if x["metric"]==metric and x["probability"]==p)

def test_b01_b03_exact_governed_identities_and_input_requirement():
 assert blob(M01)==EXPECTED_M01_BLOB
 assert blob(HUMAN)==EXPECTED_HUMAN_BLOB
 c=load(CONTRACT)
 assert c["binding_sources"]["m03_real_output"]["sha256"]==EXPECTED_M03_SHA
 assert c["binding_sources"]["m03_real_output"]["read_values_during_m10_00"] is False
 assert runtime().EXPECTED_REAL_M03_SHA256==EXPECTED_M03_SHA

def test_b04_b06_exact_claim_surface():
 c=load(CONTRACT)
 assert c["claim_binding"]["claim_units"]==11
 assert c["claim_binding"]["primary_contrasts"]==33
 assert c["claim_binding"]["transitions"]==["2022->2023","2023->2024","2024->2025"]
 out=runtime().evaluate_temporal_materiality(synthetic())
 assert len(out["claim_units"])==11
 assert sum(len(x["contrasts"]) for x in out["claim_units"])==33

def test_b07_formula_exact():
 m=runtime()
 assert m.symmetric_relative_change(100.0,125.0)==pytest.approx(2*25/225)

def test_b08_exact_threshold_is_material():
 m=runtime()
 # 90 and 110 => 40/200 = 0.20 exactly
 assert m.classify_contrast(90.0,110.0)["status"]=="MATERIAL"

def test_b09_b10_below_threshold_and_any_material_rule():
 d=synthetic()
 out=runtime().evaluate_temporal_materiality(d)
 assert claim(out,"tick_count",0.5)["status"]=="NO_MATERIAL_TEMPORAL_VARIATION_DETECTED"
 d["bucket_evidence"]["UTC_YEAR:2023"]["tick_count"]["quantiles"]["0.5"]=150.0
 out=runtime().evaluate_temporal_materiality(d)
 assert claim(out,"tick_count",0.5)["status"]=="MATERIAL_TEMPORAL_VARIATION"

def test_b11_b12_zero_denominator_blocks_with_precedence():
 d=synthetic()
 for y in (2022,2023):
  d["bucket_evidence"][f"UTC_YEAR:{y}"]["tick_count"]["quantiles"]["0.5"]=0.0
 d["bucket_evidence"]["UTC_YEAR:2024"]["tick_count"]["quantiles"]["0.5"]=1000.0
 out=runtime().evaluate_temporal_materiality(d)
 x=claim(out,"tick_count",0.5)
 assert x["status"]=="BLOCKED"
 assert any(c["status"]=="BLOCKED" and c["reason"]=="ZERO_DENOMINATOR" for c in x["contrasts"])

@pytest.mark.parametrize("mutation,reason",[
 ("year","MISSING_YEAR"),
 ("metric","MISSING_METRIC"),
 ("prob","MISSING_REQUIRED_PROBABILITY"),
])
def test_b13_b15_missing_required_surface_blocks(mutation,reason):
 d=synthetic()
 if mutation=="year": del d["bucket_evidence"]["UTC_YEAR:2024"]
 elif mutation=="metric": del d["bucket_evidence"]["UTC_YEAR:2024"]["minute_range"]
 else: del d["bucket_evidence"]["UTC_YEAR:2024"]["minute_range"]["quantiles"]["0.95"]
 out=runtime().evaluate_temporal_materiality(d)
 xs=[x for x in out["claim_units"] if x["status"]=="BLOCKED"]
 assert xs and any(reason in x["block_reasons"] for x in xs)

def test_b16_undeclared_surface_cannot_expand_claim():
 d=synthetic()
 d["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]["quantiles"]["0.123"]=999999
 out=runtime().evaluate_temporal_materiality(d)
 assert len(out["claim_units"])==11
 assert all(x["probability"]!=0.123 for x in out["claim_units"])

def test_b17_partial_years_do_not_control_primary():
 d1=synthetic(); d2=copy.deepcopy(d1)
 for y in (2021,2026):
  for metric in d2["bucket_evidence"][f"UTC_YEAR:{y}"]:
   for p in d2["bucket_evidence"][f"UTC_YEAR:{y}"][metric]["quantiles"]:
    d2["bucket_evidence"][f"UTC_YEAR:{y}"][metric]["quantiles"][p]*=1000000
 assert runtime().evaluate_temporal_materiality(d1)==runtime().evaluate_temporal_materiality(d2)

def test_b18_no_global_cross_metric_verdict():
 out=runtime().evaluate_temporal_materiality(synthetic())
 forbidden={"global_verdict","overall_stable","overall_unstable","global_pass","global_fail","strategy_valid","strategy_invalid"}
 assert forbidden.isdisjoint(out.keys())

def test_b19_nonfinite_fails_closed():
 d=synthetic(); d["bucket_evidence"]["UTC_YEAR:2023"]["spread_mean"]["quantiles"]["0.9"]=float("nan")
 x=claim(runtime().evaluate_temporal_materiality(d),"spread_mean",0.9)
 assert x["status"]=="BLOCKED"
 assert "NONFINITE_QUANTILE" in x["block_reasons"]

def test_b20_deterministic_serialization():
 m=runtime(); x=m.evaluate_temporal_materiality(synthetic())
 assert m.canonical_json(x)==m.canonical_json(m.evaluate_temporal_materiality(synthetic()))
 assert hashlib.sha256(m.canonical_json(x).encode()).hexdigest()==hashlib.sha256(m.canonical_json(x).encode()).hexdigest()

def test_b21_independent_reference_parity():
 d=synthetic()
 d["bucket_evidence"]["UTC_YEAR:2025"]["minute_range"]["quantiles"]["0.99"]=300.0
 assert runtime().evaluate_temporal_materiality(d)==reference().reference_evaluate_temporal_materiality(d)

def test_b22_epistemic_limit_exact():
 out=runtime().evaluate_temporal_materiality(synthetic())
 assert out["epistemic_limit"]=="EXPLORATORY_DIAGNOSTIC_TEMPORAL_STABILITY_EVIDENCE"
 forbidden=("CONFIRM","GENERALIZ","PROFIT","EDGE","STRATEGY_VALID")
 assert not any(tok in json.dumps(out).upper() for tok in forbidden)

def test_b23_no_other_method_auto_activation():
 c=load(CONTRACT)
 assert c["dependencies"]=={
  "M04":"NOT_AUTOMATICALLY_ACTIVATED","M05":"NOT_AUTOMATICALLY_ACTIVATED","M08":"NOT_AUTOMATICALLY_ACTIVATED",
  "M09":"NOT_ACTIVATED_REQUIRED_ONLY_FOR_FUTURE_PRISTINE_CONFIRMATION",
  "M11":"NOT_AUTOMATICALLY_ACTIVATED_REQUIRED_ONLY_FOR_INFERENTIAL_PROMOTION"}

def test_b24_no_trading_or_capital_authority():
 out=runtime().evaluate_temporal_materiality(synthetic())
 assert out["authority"]=={"scientific_execution":False,"trading":False,"capital":False}
 a=load(ACTIVATION)
 assert a["real_execution_authority"] is False and a["authority"]=={"trading":False,"capital":False}

def test_b25_no_real_result_exposure_during_qualification():
 c=load(CONTRACT); a=load(ACTIVATION)
 assert c["authority"]["real_m10_execution"] is False
 assert c["authority"]["real_m10_r_calculation"] is False
 assert a["m10_result_exposed"] is False
 matches=list(ROOT.glob("artifacts/smf_ap1_m03_02_r1_m10*"))
 assert matches==[]

def test_real_source_identity_guard_is_fail_closed_without_reading_real_values():
 m=runtime()
 assert m.require_real_source_identity(EXPECTED_M03_SHA)==EXPECTED_M03_SHA
 with pytest.raises(ValueError,match="REAL_M03_IDENTITY_MISMATCH"):
  m.require_real_source_identity("0"*64)


def test_readiness_receipt_binds_persisted_m10_00_identities_and_keeps_m10_01_closed():
    receipt = ROOT / "reports" / "program" / "2026-10-06-SMF-AP1-M03-02-R1-M10-00-REAL-EXECUTION-READINESS-RECEIPT-V0.1.json"
    r = load(receipt)
    ids = r["binding_identities"]
    assert ids["m10_00_contract_blob"] == "d9217071091656bd2a8bd7588d8dbbd9eb9ab00d"
    assert ids["m10_00_activation_blob"] == "51c3b386a070ef84fd28abc53b3105323591f3ce"
    assert ids["m10_00_breaker_blob"] == "9659f0ac80562d188bbf38018566186f4d6162be"
    assert ids["m10_00_runtime_blob"] == "c1765a56d6c861522db02af6200b7072ce621799"
    assert ids["m10_00_reference_blob"] == "2ddc0f69425d0a8349eb43b26f956f4159b76d93"
    assert ids["m10_01_real_execution_plan_blob"] == "573c1faa5588dbf95548f77d9eb33afae0210a85"
    assert r["verdict"]["M10_REAL_EXECUTION_READINESS"] == "READY_FOR_SEPARATE_HUMAN_AUTHORIZATION"
    assert r["M10_REAL_EXECUTION_AUTHORIZED"] is False
    assert r["M10_EXECUTED"] is False
    assert r["M10_RESULT_EXPOSED"] is False
    assert r["automatic_open"] is False
