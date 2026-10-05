from __future__ import annotations

import math
import pytest

MARKER = "SMF_AP1_M03_01_RUNTIME_ABSENT_EXPECTED_RED"
CASE_IDS = ["SMFAP1M03-B01","SMFAP1M03-B02","SMFAP1M03-B03","SMFAP1M03-B04","SMFAP1M03-B05","SMFAP1M03-B06","SMFAP1M03-B07","SMFAP1M03-B08","SMFAP1M03-B09","SMFAP1M03-B10","SMFAP1M03-B11","SMFAP1M03-B12","SMFAP1M03-B13","SMFAP1M03-B14","SMFAP1M03-B15","SMFAP1M03-B16","SMFAP1M03-B17","SMFAP1M03-B18","SMFAP1M03-B19","SMFAP1M03-B20","SMFAP1M03-B21","SMFAP1M03-B22","SMFAP1M03-B23","SMFAP1M03-B24","SMFAP1M03-B25","SMFAP1M03-B26","SMFAP1M03-B27","SMFAP1M03-B28"]

def _runtime():
    try:
        import src.smf_ap1_m03_binding as m
    except ModuleNotFoundError:
        pytest.fail(MARKER)
    return m

def _activation(m):
    return m.create_m03_activation(result_exposed=False)

def _plan(m, **overrides):
    args = dict(
        activation=_activation(m),
        ap1_producer_blob=m.AP1_PRODUCER_BLOB,
        data02_receipt_blob=m.DATA02_RECEIPT_BLOB,
        p121_receipt_blob=m.P121_RECEIPT_BLOB,
        smf_core_blob=m.SMF_CORE_BLOB,
        ap0_manifest_sha256=m.AP0_MANIFEST_SHA256,
        dataset_identity=m.DATASET_IDENTITY,
    )
    args.update(overrides)
    return m.build_execution_plan(**args)

def _expect_block(fn, code):
    with pytest.raises(Exception) as exc:
        fn()
    assert code in str(exc.value)

@pytest.mark.parametrize("case_id", CASE_IDS)
def test_smf_ap1_m03_01_frozen_breakers(case_id):
    m = _runtime()
    if case_id == "SMFAP1M03-B01":
        assert m.CONTRACT == "ATDS_SMF_AP1_M03_01_BINDING_V0_1"
    elif case_id == "SMFAP1M03-B02":
        assert m.CLAIM_SCOPE_ID == "CC02_DESCRIPTIVE_MARKET_BEHAVIOR:RETROSPECTIVE_DESCRIPTIVE_ONLY:ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
    elif case_id == "SMFAP1M03-B03":
        assert _activation(m)["activation_state"] == "ACTIVATED"
    elif case_id == "SMFAP1M03-B04":
        _expect_block(lambda: m.create_m03_activation(result_exposed=True), "METHOD_ACTIVATION_AFTER_RESULT_EXPOSURE")
    elif case_id == "SMFAP1M03-B05":
        _expect_block(lambda: _plan(m, ap1_producer_blob="0"*40), "AP1_PRODUCER_IDENTITY_MISMATCH")
    elif case_id == "SMFAP1M03-B06":
        _expect_block(lambda: _plan(m, data02_receipt_blob="0"*40), "DATA02_RECEIPT_IDENTITY_MISMATCH")
    elif case_id == "SMFAP1M03-B07":
        _expect_block(lambda: _plan(m, p121_receipt_blob="0"*40), "P121_RECEIPT_IDENTITY_MISMATCH")
    elif case_id == "SMFAP1M03-B08":
        _expect_block(lambda: _plan(m, smf_core_blob="0"*40), "SMF_CORE_IDENTITY_MISMATCH")
    elif case_id == "SMFAP1M03-B09":
        _expect_block(lambda: _plan(m, ap0_manifest_sha256="0"*64), "AP0_MANIFEST_IDENTITY_MISMATCH")
    elif case_id == "SMFAP1M03-B10":
        _expect_block(lambda: _plan(m, dataset_identity="WRONG"), "DATASET_IDENTITY_MISMATCH")
    elif case_id == "SMFAP1M03-B11":
        assert m.METRIC_PROBABILITIES["tick_count"] == (0.5, 0.9, 0.99)
    elif case_id == "SMFAP1M03-B12":
        assert m.METRIC_PROBABILITIES["minute_range"] == (0.5, 0.9, 0.95, 0.99)
    elif case_id == "SMFAP1M03-B13":
        assert m.METRIC_PROBABILITIES["spread_mean"] == (0.5, 0.9, 0.95, 0.99)
    elif case_id == "SMFAP1M03-B14":
        assert m.QUANTILE_DEFINITION == "linear interpolation with h=(n-1)*p"
        assert m.TAIL_EXTRAPOLATION == "FORBIDDEN"
    elif case_id == "SMFAP1M03-B15":
        assert m.POPULATION_SEMANTICS["population_scope"].startswith("CENSUS_")
        assert m.POPULATION_SEMANTICS["iid_claim"] is False
    elif case_id == "SMFAP1M03-B16":
        _expect_block(lambda: m.execute_m03_observations([], metric="tick_count", bucket_id="GLOBAL", activation=_activation(m)), "EMPTY_SAMPLE")
    elif case_id == "SMFAP1M03-B17":
        _expect_block(lambda: m.execute_m03_observations([1.0, math.inf], metric="tick_count", bucket_id="GLOBAL", activation=_activation(m)), "NONFINITE_OBSERVATION")
    elif case_id == "SMFAP1M03-B18":
        _expect_block(lambda: m.execute_m03_observations([1.0], metric="unknown", bucket_id="GLOBAL", activation=_activation(m)), "UNSUPPORTED_M03_METRIC")
    elif case_id == "SMFAP1M03-B19":
        r=m.execute_m03_observations([1,2,3], metric="tick_count", bucket_id="GLOBAL", activation=_activation(m))
        assert r["procedure_ref"] == m.METHOD_PROCEDURE_REF
    elif case_id == "SMFAP1M03-B20":
        r=m.execute_m03_observations([1,2,3], metric="tick_count", bucket_id="GLOBAL", activation=_activation(m))
        assert "ecdf" not in r and "sorted_values" not in r and "raw_values" not in r
    elif case_id == "SMFAP1M03-B21":
        a=m.execute_m03_observations([3,1,2], metric="tick_count", bucket_id="GLOBAL", activation=_activation(m))
        b=m.execute_m03_observations([3,1,2], metric="tick_count", bucket_id="GLOBAL", activation=_activation(m))
        assert a["result_digest"] == b["result_digest"]
    elif case_id == "SMFAP1M03-B22":
        act=_activation(m); act["activation_digest"]="sha256:"+"0"*64
        _expect_block(lambda: m.execute_m03_observations([1,2], metric="tick_count", bucket_id="GLOBAL", activation=act), "ACTIVATION_DIGEST_MISMATCH")
    elif case_id == "SMFAP1M03-B23":
        assert _plan(m)["authority"]["execution"] is False
    elif case_id == "SMFAP1M03-B24":
        r=m.execute_m03_observations([1,2], metric="tick_count", bucket_id="GLOBAL", activation=_activation(m))
        assert r["authority"] == {"scientific":False,"operational":False,"trading":False,"capital":False}
    elif case_id == "SMFAP1M03-B25":
        assert m.COMPANION_ID != "ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
    elif case_id == "SMFAP1M03-B26":
        _expect_block(lambda: m.execute_m03_observations([1,2], metric="tick_count", bucket_id="", activation=_activation(m)), "BUCKET_ID_REQUIRED")
    elif case_id == "SMFAP1M03-B27":
        act=_activation(m)
        assert act["activation_state"]=="ACTIVATED" and act["method_family_ref"]=="M03"
    elif case_id == "SMFAP1M03-B28":
        plan=_plan(m)
        assert "ap0_root" not in plan and "output" not in plan and plan["result_minted"] is False
