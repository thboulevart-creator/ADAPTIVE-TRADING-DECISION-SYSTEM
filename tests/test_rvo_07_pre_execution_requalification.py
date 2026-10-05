from __future__ import annotations

import copy
import src.rvo_07_pre_execution_requalification as m

HEAD="1"*40
TREE="2"*40

def valid():
    return m.synthetic_valid_workspace_receipt(head=HEAD,tree=TREE,workspace_clean=True,workspace_detached=True)

def evaluate(receipt=None, **kwargs):
    return m.evaluate_pre_execution_readiness(
        receipt or valid(),
        current_head=kwargs.pop("current_head",HEAD),
        current_tree=kwargs.pop("current_tree",TREE),
        workspace_clean=kwargs.pop("workspace_clean",True),
        workspace_detached=kwargs.pop("workspace_detached",True),
        observed_owner_blobs=kwargs.pop("observed_owner_blobs",dict(m.EXPECTED_OWNER_BLOBS)),
        main_checkout_clean=kwargs.pop("main_checkout_clean",True),
        workspace_receipt_sha256="a"*64,
        **kwargs,
    )

def test_01_valid_surface_is_go():
    out=evaluate()
    assert out["verdict"]=="GO"
    assert all(v["status"]==m.CLOSED for v in out["gaps"].values())

def test_02_go_is_readiness_only():
    out=evaluate()
    assert out["readiness"]=="PRE_EXECUTION_READINESS_GO"
    assert out["execution_authorized"] is False
    assert out["authority"]==m.AUTHORITY_NONE

def test_03_wrong_head_no_go():
    assert evaluate(current_head="3"*40)["verdict"]=="NO_GO"

def test_04_wrong_tree_no_go():
    assert evaluate(current_tree="3"*40)["verdict"]=="NO_GO"

def test_05_dirty_workspace_no_go():
    out=evaluate(workspace_clean=False)
    assert out["verdict"]=="NO_GO" and out["gaps"]["G05"]["status"]==m.OPEN

def test_06_attached_workspace_no_go():
    out=evaluate(workspace_detached=False)
    assert out["verdict"]=="NO_GO" and out["gaps"]["G05"]["status"]==m.OPEN

def test_07_dirty_main_checkout_no_go():
    out=evaluate(main_checkout_clean=False)
    assert out["verdict"]=="NO_GO"

def test_08_owner_blob_drift_no_go():
    obs=dict(m.EXPECTED_OWNER_BLOBS)
    obs["tools/ap1_intraday_spread_census.py"]="bad"
    assert evaluate(observed_owner_blobs=obs)["verdict"]=="NO_GO"

def test_09_g01_requires_data_binding():
    r=valid(); r["p1"]["data_binding_id"]=""
    out=evaluate(r)
    assert out["gaps"]["G01"]["status"]==m.OPEN and out["verdict"]=="NO_GO"

def test_10_g02_requires_exact_profile():
    r=valid(); r["p1"]["invocation_profile_id"]="WRONG"
    out=evaluate(r)
    assert out["gaps"]["G02"]["status"]==m.OPEN

def test_11_g03_requires_exact_runtime():
    r=valid(); r["runtime_lock"]["python_version"]="0"
    out=evaluate(r)
    assert out["gaps"]["G03"]["status"]==m.OPEN

def test_12_g04_requires_unexecuted_smf():
    r=valid(); r["smf"]["method_executed"]=True
    out=evaluate(r)
    assert out["gaps"]["G04"]["status"]==m.OPEN

def test_13_g05_requires_ap0_identity():
    r=valid(); r["ap0"]["manifest_sha256"]="bad"
    out=evaluate(r)
    assert out["gaps"]["G05"]["status"]==m.OPEN

def test_14_forbidden_empirical_observation_no_go():
    r=valid(); r["forbidden_observations"]["new_empirical_result"]=True
    assert evaluate(r)["verdict"]=="NO_GO"

def test_15_exact_real_input_must_not_exist():
    r=valid(); r["p1"]["exact_real_cc02_input_minted"]=True
    assert evaluate(r)["verdict"]=="NO_GO"

def test_16_freeze_is_deterministic():
    assert evaluate()["pre_result_freeze"]["freeze_digest"]==evaluate()["pre_result_freeze"]["freeze_digest"]

def test_17_freeze_binds_owner_blobs_and_workspace_receipt():
    f=evaluate()["pre_result_freeze"]
    assert f["owner_blobs"]==dict(sorted(m.EXPECTED_OWNER_BLOBS.items()))
    assert f["workspace"]["workspace_receipt_sha256"]=="a"*64

def test_18_freeze_declares_no_empirical_execution():
    f=evaluate()["pre_result_freeze"]
    assert f["real_ap1_executed"] is False
    assert f["real_m03_executed"] is False
    assert f["new_empirical_result"] is False

def test_19_no_go_preserves_zero_authority():
    r=valid(); r["status"]="BLOCKED"
    out=evaluate(r)
    assert out["verdict"]=="NO_GO"
    assert out["authority"]==m.AUTHORITY_NONE

def test_20_gap_statuses_are_distinct_from_authority():
    out=evaluate()
    assert out["gaps"]["G01"]["status"]==m.CLOSED
    assert out["authority"]["execution"] is False
