from __future__ import annotations

import ast
import copy
import hashlib
import importlib
import json
from pathlib import Path

import pytest

PRIMARY = importlib.import_module("tools.smf_ap1_m03_02_r1_post_m10_dre_02")
REFERENCE = importlib.import_module("tools.smf_ap1_m03_02_r1_post_m10_dre_02_reference")
ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures" / "smf_ap1_m03_02_r1_post_m10_dre_02"
EXPECTED_HASH = "7d4369cdfab545f0edb94b93ad9d1d1070e6afa35a1000376af55d9c10943a9e"


def load_fixture():
    return json.loads((FIX / "SYNTHETIC_VALID_M03_PAYLOAD.json").read_text(encoding="utf-8"))


def expected_success():
    return json.loads((FIX / "SYNTHETIC_EXPECTED_SUCCESS.json").read_text(encoding="utf-8"))


def eval_both(payload, sha=EXPECTED_HASH):
    p = PRIMARY.evaluate(copy.deepcopy(payload), observed_source_sha256=sha)
    r = REFERENCE.reference_evaluate(copy.deepcopy(payload), observed_source_sha256=sha)
    assert p == r
    assert PRIMARY.canonical_bytes(p) == REFERENCE.canonical_bytes(r)
    return p


def assert_blocked(result, contains=None):
    assert result["schema"] == "ATDS_SMF_AP1_M03_02_R1_POST_M10_DRE_01_BLOCKED_RESULT_V0_1"
    assert result["status"] == "DRE01_BLOCKED"
    assert set(result) == {"schema", "status", "control_id", "reason_codes", "authority"}
    assert result["reason_codes"] == sorted(set(result["reason_codes"]))
    assert "components" not in result
    if contains:
        assert any(contains in code for code in result["reason_codes"])


def redigest(bucket):
    body = dict(bucket)
    body.pop("result_digest", None)
    bucket["result_digest"] = "sha256:" + hashlib.sha256(
        json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    ).hexdigest()


def test_valid_fixture_green_and_extras_ignored():
    result = eval_both(load_fixture())
    assert result == expected_success()
    assert len(result["components"]) == 4
    assert [x["stratum"] for x in result["components"]] == [f"UTC_YEAR:{y}" for y in (2022, 2023, 2024, 2025)]
    assert all(x["stratum"] not in ("UTC_YEAR:2021", "UTC_YEAR:2026") for x in result["components"])


def test_success_schema_exact():
    result = eval_both(load_fixture())
    assert result["claim_unit"] == "tick_count p50"
    assert result["claim_id"] == "POST_M10-DC02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES"
    assert result["estimand_id"] == "POST_M10-E02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES"
    assert result["analysis_id"] == "POST_M10-DA02-TICKCOUNT-P50-YEAR-STRATIFIED-REFERENCE-CONSTRUCTION"
    assert result["conditioning_spec_id"] == "POST_M10-TCS01-TICKCOUNT-P50-UTC-YEAR-STRATA-2022-2025"
    assert result["vector_order"] == ["R_2022", "R_2023", "R_2024", "R_2025"]
    assert result["relation_between_components"] == "A_CONDITIONED_REFERENCE_VECTOR"
    assert result["aggregation"] == "NONE"
    assert result["epistemic_state"]["same_corpus_confirmatory_status"] == "NON_PRISTINE"
    assert result["authority"] == {"authority_created":"NONE","trading":False,"capital":False,"oos":False,"method":False,"method_execution":False}
    forbidden = {"global_reference","pooled_reference","mean_of_year_references","weighted_mean_of_year_references","median_of_year_medians","trend","change_point","regime","signal","strategy_verdict","trading_action","capital_action"}
    assert forbidden.isdisjoint(result)


@pytest.mark.parametrize("year", [2022, 2023, 2024, 2025])
def test_missing_year_bucket_blocks(year):
    p = load_fixture()
    del p["bucket_evidence"][f"UTC_YEAR:{year}"]
    assert_blocked(eval_both(p), f"BUCKET_MISSING:UTC_YEAR:{year}")


def test_wrong_source_sha_blocks():
    assert_blocked(eval_both(load_fixture(), sha="0"*64), "SOURCE_SHA256_MISMATCH")


def test_wrong_source_schema_blocks():
    p=load_fixture(); p["schema"]="WRONG"
    assert_blocked(eval_both(p), "SOURCE_SCHEMA_MISMATCH")


def test_wrong_source_status_blocks():
    p=load_fixture(); p["status"]="WRONG"
    assert_blocked(eval_both(p), "SOURCE_STATUS_MISMATCH")


def test_wrong_dataset_identity_blocks():
    p=load_fixture(); p["source_data02"]["dataset_identity"]="WRONG"
    assert_blocked(eval_both(p), "DATASET_IDENTITY_MISMATCH")


def test_wrong_manifest_identity_blocks():
    p=load_fixture(); p["source_data02"]["ap0_manifest_sha256"]="WRONG"
    assert_blocked(eval_both(p), "AP0_MANIFEST_SHA256_MISMATCH")


def test_wrong_file_count_blocks():
    p=load_fixture(); p["source_data02"]["expected_files"]=60
    assert_blocked(eval_both(p), "AP0_FILE_COUNT_MISMATCH")


def test_wrong_minute_count_blocks():
    p=load_fixture(); p["source_data02"]["minute_rows"]=1
    assert_blocked(eval_both(p), "AP0_MINUTE_COUNT_MISMATCH")


def test_missing_tick_count_blocks():
    p=load_fixture(); del p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]
    assert_blocked(eval_both(p), "TICK_COUNT_MISSING:UTC_YEAR:2022")


def test_missing_quantiles_blocks():
    p=load_fixture(); b=p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]; del b["quantiles"]; redigest(b)
    assert_blocked(eval_both(p), "QUANTILES_MISSING:UTC_YEAR:2022")


def test_missing_p50_blocks():
    p=load_fixture(); b=p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]; del b["quantiles"]["0.5"]; redigest(b)
    result=eval_both(p)
    assert_blocked(result, "QUANTILE_KEYS_MISMATCH:UTC_YEAR:2022")
    assert any("QUANTILE_VALUE_INVALID:UTC_YEAR:2022:0.5" in x for x in result["reason_codes"])


@pytest.mark.parametrize("value", [None, True, "12", float("nan"), float("inf"), float("-inf")])
def test_invalid_p50_values_block(value):
    p=load_fixture(); p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]["quantiles"]["0.5"]=value
    assert_blocked(eval_both(p), "QUANTILE_VALUE_INVALID:UTC_YEAR:2022:0.5")


@pytest.mark.parametrize("value", [0, -1, 1.5, True])
def test_invalid_n_blocks(value):
    p=load_fixture(); b=p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]; b["n"]=value; redigest(b)
    assert_blocked(eval_both(p), "BUCKET_N_INVALID:UTC_YEAR:2022")


def test_wrong_bucket_id_blocks():
    p=load_fixture(); b=p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]; b["bucket_id"]="UTC_YEAR:2021"; redigest(b)
    assert_blocked(eval_both(p), "BUCKET_ID_MISMATCH:UTC_YEAR:2022")


def test_wrong_metric_blocks():
    p=load_fixture(); b=p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]; b["metric"]="spread_mean"; redigest(b)
    assert_blocked(eval_both(p), "BUCKET_METRIC_MISMATCH:UTC_YEAR:2022")


def test_wrong_bucket_schema_blocks():
    p=load_fixture(); b=p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]; b["schema"]="WRONG"; redigest(b)
    assert_blocked(eval_both(p), "BUCKET_SCHEMA_MISMATCH:UTC_YEAR:2022")


def test_wrong_procedure_ref_blocks():
    p=load_fixture(); p["method"]["procedure_ref"]="WRONG"
    b=p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]; b["procedure_ref"]="WRONG"; redigest(b)
    result=eval_both(p); assert_blocked(result)
    assert "M03_PROCEDURE_REF_MISMATCH" in result["reason_codes"]
    assert "BUCKET_PROCEDURE_REF_MISMATCH:UTC_YEAR:2022" in result["reason_codes"]


def test_wrong_core_blob_blocks():
    p=load_fixture(); p["method"]["core_blob"]="WRONG"
    b=p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]; b["smf_core_blob"]="WRONG"; redigest(b)
    result=eval_both(p); assert_blocked(result)
    assert "M03_CORE_BLOB_MISMATCH" in result["reason_codes"]
    assert "BUCKET_CORE_BLOB_MISMATCH:UTC_YEAR:2022" in result["reason_codes"]


def test_tail_rule_violation_blocks():
    p=load_fixture(); p["method"]["tail_extrapolation"]="ALLOWED"
    b=p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]; b["tail_extrapolation"]="ALLOWED"; redigest(b)
    result=eval_both(p); assert_blocked(result)
    assert "M03_TAIL_RULE_MISMATCH" in result["reason_codes"]
    assert "BUCKET_TAIL_RULE_MISMATCH:UTC_YEAR:2022" in result["reason_codes"]


def test_result_digest_mismatch_blocks():
    p=load_fixture(); p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]["result_digest"]="sha256:"+"0"*64
    assert_blocked(eval_both(p), "BUCKET_RESULT_DIGEST_MISMATCH:UTC_YEAR:2022")


def test_quantile_key_extra_blocks():
    p=load_fixture(); b=p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]; b["quantiles"]["0.95"]=77.0; redigest(b)
    assert_blocked(eval_both(p), "QUANTILE_KEYS_MISMATCH:UTC_YEAR:2022")


def test_source_authority_mismatch_blocks():
    p=load_fixture(); p["authority"]["trading"]=True
    assert_blocked(eval_both(p), "SOURCE_AUTHORITY_MISMATCH")


def test_bucket_authority_mismatch_blocks():
    p=load_fixture(); b=p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]; b["authority"]["capital"]=True; redigest(b)
    assert_blocked(eval_both(p), "BUCKET_AUTHORITY_MISMATCH:UTC_YEAR:2022")


def test_invalid_digest_fields_block():
    p=load_fixture(); b=p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]
    b["activation_digest"]="bad"; b["sorted_values_digest"]="bad"; b["ecdf_digest"]="bad"; redigest(b)
    result=eval_both(p); assert_blocked(result)
    assert "BUCKET_ACTIVATION_DIGEST_INVALID:UTC_YEAR:2022" in result["reason_codes"]
    assert "BUCKET_SORTED_VALUES_DIGEST_INVALID:UTC_YEAR:2022" in result["reason_codes"]
    assert "BUCKET_ECDF_DIGEST_INVALID:UTC_YEAR:2022" in result["reason_codes"]


def test_all_material_failures_are_atomic_blocked():
    variants=[]
    p=load_fixture(); del p["bucket_evidence"]["UTC_YEAR:2024"]; variants.append(p)
    p=load_fixture(); p["bucket_evidence"]["UTC_YEAR:2023"]["tick_count"]["n"]=0; variants.append(p)
    p=load_fixture(); p["source_data02"]["dataset_identity"]="WRONG"; variants.append(p)
    for payload in variants:
        result=eval_both(payload)
        assert_blocked(result)
        assert "components" not in result


def test_determinism_repeated_runs():
    p=load_fixture()
    outputs=[PRIMARY.evaluate(copy.deepcopy(p), observed_source_sha256=EXPECTED_HASH) for _ in range(5)]
    assert all(x==outputs[0] for x in outputs)
    bytes_=[PRIMARY.canonical_bytes(x) for x in outputs]
    assert all(x==bytes_[0] for x in bytes_)
    assert len({hashlib.sha256(x).hexdigest() for x in bytes_})==1


def test_primary_reference_parity_all_cases():
    cases=[load_fixture()]
    for year in (2022,2023,2024,2025):
        p=load_fixture(); del p["bucket_evidence"][f"UTC_YEAR:{year}"]; cases.append(p)
    p=load_fixture(); p["schema"]="WRONG"; cases.append(p)
    p=load_fixture(); p["source_data02"]["dataset_identity"]="WRONG"; cases.append(p)
    p=load_fixture(); p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]["quantiles"]["0.5"]=None; cases.append(p)
    for case in cases:
        primary=PRIMARY.evaluate(copy.deepcopy(case), observed_source_sha256=EXPECTED_HASH)
        reference=REFERENCE.reference_evaluate(copy.deepcopy(case), observed_source_sha256=EXPECTED_HASH)
        assert primary==reference
        assert PRIMARY.canonical_bytes(primary)==REFERENCE.canonical_bytes(reference)


def test_reference_is_independent():
    psrc=(ROOT/"tools"/"smf_ap1_m03_02_r1_post_m10_dre_02.py").read_text(encoding="utf-8")
    rsrc=(ROOT/"tools"/"smf_ap1_m03_02_r1_post_m10_dre_02_reference.py").read_text(encoding="utf-8")
    assert "smf_ap1_m03_02_r1_post_m10_dre_02" not in rsrc
    assert "smf_ap1_m03_02_r1_post_m10_dre_02_reference" not in psrc
    assert "evaluate(" not in rsrc.replace("reference_evaluate(", "")
    assert "reference_evaluate(" not in psrc


def test_no_raw_ap0_or_quantile_recompute_symbols():
    sources=(ROOT/"tools"/"smf_ap1_m03_02_r1_post_m10_dre_02.py").read_text()+"\n"+(ROOT/"tools"/"smf_ap1_m03_02_r1_post_m10_dre_02_reference.py").read_text()
    text=sources.lower()
    assert "numpy" not in text and "pandas" not in text and "statistics.median" not in text
    tree=ast.parse(sources)
    calls=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Call):
            if isinstance(node.func,ast.Name): calls.append(node.func.id)
            elif isinstance(node.func,ast.Attribute): calls.append(node.func.attr)
    assert not ({"percentile","quantile","median","ecdf_quantiles","_quantile_linear"} & set(calls))


def test_no_timestamp_rebucketing():
    text=((ROOT/"tools"/"smf_ap1_m03_02_r1_post_m10_dre_02.py").read_text()+"\n"+(ROOT/"tools"/"smf_ap1_m03_02_r1_post_m10_dre_02_reference.py").read_text()).lower()
    for forbidden in ("datetime","zoneinfo",".year","astimezone","fromtimestamp"):
        assert forbidden not in text


def test_no_dynamic_bucket_discovery():
    p=load_fixture()
    p["bucket_evidence"]["UTC_YEAR:2030"]={"tick_count":copy.deepcopy(p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"])}
    result=eval_both(p)
    assert result["status"]=="DRE01_COMPLETE"
    assert [c["stratum"] for c in result["components"]]==[f"UTC_YEAR:{y}" for y in (2022,2023,2024,2025)]


def test_no_round_cast_transform():
    p=load_fixture(); p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"]["quantiles"]["0.5"]=12.345678901234567
    redigest(p["bucket_evidence"]["UTC_YEAR:2022"]["tick_count"])
    assert eval_both(p)["components"][0]["value"]==12.345678901234567


def test_no_imputation_borrowing_or_aggregation():
    p=load_fixture(); del p["bucket_evidence"]["UTC_YEAR:2024"]
    result=eval_both(p)
    assert_blocked(result)
    assert "aggregation" not in result and "components" not in result


def test_no_scientific_wall_clock():
    text=json.dumps(eval_both(load_fixture()),sort_keys=True).lower()
    for key in ("started_at","ended_at","timestamp","generated_at","created_at"):
        assert key not in text


def test_no_random_locale_timezone_fs_dependency():
    sources=(ROOT/"tools"/"smf_ap1_m03_02_r1_post_m10_dre_02.py").read_text()+"\n"+(ROOT/"tools"/"smf_ap1_m03_02_r1_post_m10_dre_02_reference.py").read_text()
    tree=ast.parse(sources)
    imports=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Import): imports += [x.name for x in node.names]
        elif isinstance(node,ast.ImportFrom) and node.module: imports.append(node.module)
    assert not any(x.split(".")[0] in {"random","locale","datetime","zoneinfo","pathlib","os"} for x in imports)


def test_static_real_source_path_not_read():
    sources=(ROOT/"tools"/"smf_ap1_m03_02_r1_post_m10_dre_02.py").read_text()+"\n"+(ROOT/"tools"/"smf_ap1_m03_02_r1_post_m10_dre_02_reference.py").read_text()
    assert "M03-R1-REAL-e73a24ca.json" not in sources
    assert "ATDS-CONTROL" not in sources
    assert "REAL_SOURCE_PATH" not in sources
    assert "open(" not in sources and "read_text" not in sources and "read_bytes" not in sources


def test_real_budget_unconsumed():
    assert not hasattr(PRIMARY,"main") and not hasattr(REFERENCE,"main")
    assert not hasattr(PRIMARY,"read_real_payload") and not hasattr(REFERENCE,"read_real_payload")


def test_static_frozen_identities():
    assert PRIMARY.REQUIRED_SOURCE_SHA256 == EXPECTED_HASH
    assert PRIMARY.PROCEDURE_REF.endswith("#ecdf_quantiles")
    assert PRIMARY.SMF_CORE_BLOB == "b67d63bbbc4f93be3fe1e7327c1f1f1cc440ebeb"
    assert REFERENCE.EXPECTED_HASH == EXPECTED_HASH
    assert REFERENCE.PROC == PRIMARY.PROCEDURE_REF
    assert REFERENCE.CORE == PRIMARY.SMF_CORE_BLOB


def test_static_no_identifier_collision():
    assert len({PRIMARY.CONTROL_ID,PRIMARY.RESULT_SCHEMA,PRIMARY.BLOCKED_SCHEMA})==3


def test_static_old_pooling_remains_closed():
    result=eval_both(load_fixture())
    assert result["aggregation"]=="NONE"
    assert "pooled_reference" not in result
    assert result["relation_between_components"]=="A_CONDITIONED_REFERENCE_VECTOR"


def test_methods_remain_closed_in_qualification_contract():
    result=eval_both(load_fixture())
    assert result["authority"]["method"] is False
    assert result["authority"]["method_execution"] is False


def test_breaker_coverage_matrix_is_69_of_69():
    matrix=json.loads((FIX/"BREAKER_COVERAGE_MATRIX.json").read_text())
    assert matrix["breaker_count"]==69 and matrix["covered_breaker_count"]==69
    assert [x["breaker_id"] for x in matrix["rows"]]==[f"DRE01-B{i:02d}" for i in range(1,70)]
    assert all(x["coverage_type"] in {"EXECUTABLE","STATIC"} and x["test_id"] for x in matrix["rows"])


def test_fixture_manifest_declares_no_real_values():
    m=json.loads((FIX/"SYNTHETIC_FIXTURE_MANIFEST.json").read_text())
    assert m["classification"]=="SYNTHETIC_ONLY_NO_MARKET_MEANING"
    assert m["contains_real_m03_values"] is False
    assert m["contains_real_ap0_rows"] is False
    assert m["contains_real_r_values"] is False
    assert len(m["required_adversarial_classes"])>=40
