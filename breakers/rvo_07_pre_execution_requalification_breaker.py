from __future__ import annotations

import copy
import pytest

MARKER = "RVO_07_REQUALIFICATION_RUNTIME_ABSENT_EXPECTED_RED"
CASE_IDS = ["RVO07-B01","RVO07-B02","RVO07-B03","RVO07-B04","RVO07-B05","RVO07-B06","RVO07-B07","RVO07-B08","RVO07-B09","RVO07-B10","RVO07-B11","RVO07-B12","RVO07-B13","RVO07-B14","RVO07-B15","RVO07-B16","RVO07-B17","RVO07-B18","RVO07-B19","RVO07-B20","RVO07-B21","RVO07-B22","RVO07-B23","RVO07-B24","RVO07-B25","RVO07-B26","RVO07-B27","RVO07-B28","RVO07-B29","RVO07-B30","RVO07-B31","RVO07-B32","RVO07-B33","RVO07-B34","RVO07-B35"]

def _m():
    try:
        import src.rvo_07_pre_execution_requalification as m
    except ModuleNotFoundError:
        pytest.fail(MARKER)
    return m

def _valid(m):
    return m.synthetic_valid_workspace_receipt(
        head="1"*40,
        tree="2"*40,
        workspace_clean=True,
        workspace_detached=True,
    )

def _eval(m, receipt=None, **kwargs):
    receipt = receipt if receipt is not None else _valid(m)
    return m.evaluate_pre_execution_readiness(
        receipt,
        current_head=kwargs.pop("current_head", "1"*40),
        current_tree=kwargs.pop("current_tree", "2"*40),
        workspace_clean=kwargs.pop("workspace_clean", True),
        workspace_detached=kwargs.pop("workspace_detached", True),
        observed_owner_blobs=kwargs.pop("observed_owner_blobs", dict(m.EXPECTED_OWNER_BLOBS)),
        **kwargs,
    )

@pytest.mark.parametrize("case_id", CASE_IDS)
def test_rvo_07_frozen_breakers(case_id):
    m=_m()
    if case_id=="RVO07-B01":
        assert m.CONTRACT=="ATDS_RVO_07_PRE_EXECUTION_REQUALIFICATION_V0_1"
    elif case_id=="RVO07-B02":
        assert m.REPOSITORY=="thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
    elif case_id=="RVO07-B03":
        assert m.CANONICAL_BRANCH=="integration/system-v1"
    elif case_id=="RVO07-B04":
        assert m.EXPECTED_OWNER_BLOBS["tools/ap1_intraday_spread_census.py"]=="9f613063fb8a190a1ff6f2f8b12c97c4ed97712a"
    elif case_id=="RVO07-B05":
        r=_valid(m); r["schema"]="WRONG"; assert _eval(m,r)["verdict"]=="NO_GO"
    elif case_id=="RVO07-B06":
        r=_valid(m); r["status"]="BLOCKED"; assert _eval(m,r)["verdict"]=="NO_GO"
    elif case_id=="RVO07-B07":
        assert _eval(m,current_head="3"*40)["verdict"]=="NO_GO"
    elif case_id=="RVO07-B08":
        assert _eval(m,current_tree="3"*40)["verdict"]=="NO_GO"
    elif case_id=="RVO07-B09":
        r=_valid(m); r["identity"]["protected_blobs"]["tools/ap1_intraday_spread_census.py"]="bad"; assert _eval(m,r)["verdict"]=="NO_GO"
    elif case_id=="RVO07-B10":
        r=_valid(m); r["ap0"]["dataset_identity"]="WRONG"; assert _eval(m,r)["verdict"]=="NO_GO"
    elif case_id=="RVO07-B11":
        r=_valid(m); r["ap0"]["manifest_sha256"]="bad"; assert _eval(m,r)["verdict"]=="NO_GO"
    elif case_id=="RVO07-B12":
        r=_valid(m); r["ap0"]["parquet_file_count"]=60; assert _eval(m,r)["verdict"]=="NO_GO"
    elif case_id=="RVO07-B13":
        r=_valid(m); r["ap0"]["parquet_content_opened"]=True; assert _eval(m,r)["verdict"]=="NO_GO"
    elif case_id=="RVO07-B14":
        r=_valid(m); r["output_probe"]["probe_removed"]=False; assert _eval(m,r)["verdict"]=="NO_GO"
    elif case_id=="RVO07-B15":
        r=_valid(m); r["p1"]["data_binding_id"]=""; assert _eval(m,r)["gaps"]["G01"]["status"]=="OPEN"
    elif case_id=="RVO07-B16":
        r=_valid(m); r["p1"]["invocation_profile_id"]="WRONG"; assert _eval(m,r)["gaps"]["G02"]["status"]=="OPEN"
    elif case_id=="RVO07-B17":
        r=_valid(m); r["runtime_lock"]["runtime_lock_digest"]="bad"; assert _eval(m,r)["gaps"]["G03"]["status"]=="OPEN"
    elif case_id=="RVO07-B18":
        r=_valid(m); r["runtime_lock"]["execution_authority"]=True; assert _eval(m,r)["gaps"]["G03"]["status"]=="OPEN"
    elif case_id=="RVO07-B19":
        r=_valid(m); r["runtime_lock"]["timeout_seconds"]=0; assert _eval(m,r)["gaps"]["G03"]["status"]=="OPEN"
    elif case_id=="RVO07-B20":
        r=_valid(m); r["runtime_lock"]["material_environment_json"]="{}"; assert _eval(m,r)["gaps"]["G03"]["status"]=="OPEN"
    elif case_id=="RVO07-B21":
        r=_valid(m); r["smf"]["activation_digest"]="bad"; assert _eval(m,r)["gaps"]["G04"]["status"]=="OPEN"
    elif case_id=="RVO07-B22":
        r=_valid(m); r["smf"]["dry_plan_digest"]="bad"; assert _eval(m,r)["gaps"]["G04"]["status"]=="OPEN"
    elif case_id=="RVO07-B23":
        r=_valid(m); r["smf"]["method_executed"]=True; assert _eval(m,r)["gaps"]["G04"]["status"]=="OPEN"
    elif case_id=="RVO07-B24":
        assert _eval(m,workspace_clean=False)["gaps"]["G05"]["status"]=="OPEN"
    elif case_id=="RVO07-B25":
        r=_valid(m); r["p1"]["exact_real_cc02_input_minted"]=True; assert _eval(m,r)["verdict"]=="NO_GO"
    elif case_id=="RVO07-B26":
        r=_valid(m); r["p1"]["result_minted"]=True; assert _eval(m,r)["verdict"]=="NO_GO"
    elif case_id=="RVO07-B27":
        r=_valid(m); r["authority"]["execution"]=True; assert _eval(m,r)["verdict"]=="NO_GO"
    elif case_id=="RVO07-B28":
        r=_valid(m); r["forbidden_observations"]["new_empirical_result"]=True; assert _eval(m,r)["verdict"]=="NO_GO"
    elif case_id=="RVO07-B29":
        obs=dict(m.EXPECTED_OWNER_BLOBS); obs["tools/ap1_intraday_spread_census.py"]="bad"; assert _eval(m,observed_owner_blobs=obs)["verdict"]=="NO_GO"
    elif case_id=="RVO07-B30":
        out=_eval(m); assert out["pre_result_freeze"]["head"]=="1"*40 and out["pre_result_freeze"]["tree"]=="2"*40
    elif case_id=="RVO07-B31":
        assert _eval(m)["pre_result_freeze"]["freeze_digest"]==_eval(m)["pre_result_freeze"]["freeze_digest"]
    elif case_id=="RVO07-B32":
        r=_valid(m); r["p1"]["data_binding_id"]=""; assert _eval(m,r)["verdict"]=="NO_GO"
    elif case_id=="RVO07-B33":
        assert _eval(m)["verdict"]=="GO"
    elif case_id=="RVO07-B34":
        assert _eval(m)["authority"]["execution"] is False
    elif case_id=="RVO07-B35":
        assert _eval(m)["authority"]=={"execution":False,"scientific":False,"operational":False,"trading":False,"capital":False}
