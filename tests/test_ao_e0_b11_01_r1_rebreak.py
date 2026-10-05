from breakers.ao_e0_b11_01_r1_rebreak import rebreak, CONTRACT, OWNER_RECEIPT, SMF

def test_exact_old_blocker_is_closed_only_by_new_owner():
    result=rebreak()
    assert result["old_blocker"]=="CLOSED_BY_AO_E0_P1_OWNER_01"
    assert result["b11"]=="CLOSED"

def test_remaining_gates_stay_separate():
    result=rebreak()
    assert (result["b7"],result["b8"],result["b9"],result["b12"])==("OPEN","OPEN","OPEN","CLOSED")

def test_no_ao_e0_authority_created():
    result=rebreak()
    assert result["ao_e0_execution"]=="NOT_AUTHORIZED"
    assert result["oos_consumption"]=="NOT_AUTHORIZED"
    assert result["performance_observation"]=="NOT_AUTHORIZED"

def test_smf_blocked_prerequisites_remain_blocked():
    states={m["method"]:m["state"] for m in SMF["methods"]}
    assert states["M06"].endswith("B8_NUMERIC_CONFIGURATION")
    assert states["M09"].endswith("B8_AND_B12")
    assert states["M11"].endswith("B9")

def test_owner_green_proof_is_exact():
    assert OWNER_RECEIPT["green"]["workflow_run_id"]==37344925805
    assert OWNER_RECEIPT["green"]["conclusion"]=="SUCCESS"

def test_authority_firewall():
    assert all(v is False for v in CONTRACT["authority"].values())
