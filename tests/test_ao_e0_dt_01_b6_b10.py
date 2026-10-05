from pathlib import Path
import importlib.util
R=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("br",R/"breakers"/"ao_e0_dt_01_b6_b10_breaker.py"); br=importlib.util.module_from_spec(s); s.loader.exec_module(br)
def test_full_breaker(): br.run()
def test_data_candidate(): assert br.A.qualify(br.good_data())["b10"]=="CANDIDATE_PASS"
def test_temporal_candidate(): assert br.B.assess(br.good_trace())["b6"]=="CANDIDATE_PASS"
def test_data_not_temporal_authority(): assert br.A.AUTHORITY["temporal"] is False
def test_temporal_not_rvo_authority(): assert br.B.AUTHORITY["rvo"] is False
def test_no_oos_data(): assert br.A.AUTHORITY["oos_consumption"] is False
def test_no_oos_temporal(): assert br.B.AUTHORITY["oos_consumption"] is False
def test_unknown_fails_closed():
    x=br.good_trace(); x["essential_temporal_unknown"]=True
    assert br.B.assess(x)["status"]=="BLOCKED"
def test_pre_oos_history_can_cross_oos_boundary_without_reset():
    assert br.B.assess(br.good_trace())["status"]=="QUALIFIED_CANDIDATE"
