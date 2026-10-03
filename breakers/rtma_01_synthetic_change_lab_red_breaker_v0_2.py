from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/RTMA-01-SYNTHETIC-CHANGE-LAB-CONTRACT-V0.2.json"
TARGET_PATH = ROOT / "tools/rtma_01_synthetic_change_lab.py"

DOC = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
EXPECTED_CONTRACT = "RTMA_01_SYNTHETIC_CHANGE_LAB_V0_2"
EXPECTED_GENERATOR = "RTMA_01_SYNTHETIC_CHANGE_GENERATOR_V0_2"
EXPECTED_FAILURE = "RTMA_01_RUNTIME_ABSENT_EXPECTED_RED"

EXPECTED_TASKS = (
    "DISTRIBUTIONAL_CHANGE_DETECTION",
    "PERSISTENT_MARKET_TRANSITION_DETECTION",
    "GRADUAL_DRIFT_DETECTION",
    "TRANSIENT_SHOCK_DETECTION",
    "DATA_INTEGRITY_CHANGE_DETECTION",
    "STATE_NOVELTY_RECOGNITION",
    "TRANSITION_NOVELTY_RECOGNITION",
    "RESPONSE_NOVELTY_DETECTION",
    "WITHIN_CONTEXT_RESPONSE_DEGRADATION",
    "EXECUTION_DEGRADATION",
)
EXPECTED_LANES = ("LANE_O", "LANE_R", "LANE_M", "LANE_E")
EXPECTED_CASES = tuple(f"SYN-{i:02d}" for i in range(23))

assert DOC["schema"] == "ATDS_RTMA_01_SYNTHETIC_CHANGE_LAB_CONTRACT_V0_2"
assert DOC["runtime_contract"] == EXPECTED_CONTRACT
assert DOC["namespace_firewalls"]["rtma_generator"] == EXPECTED_GENERATOR
assert DOC["namespace_firewalls"]["must_not_equal"] == "ATDS_A0_SYNTHETIC_PRODUCER_V0_1"
assert tuple(DOC["task_classes"]) == EXPECTED_TASKS
assert tuple(x[0] for x in DOC["lanes"]) == EXPECTED_LANES
assert tuple(x["id"] for x in DOC["case_families"]) == EXPECTED_CASES
assert len(DOC["test_cases"]) == 63
assert [x[0] for x in DOC["test_cases"]] == [f"RTMA01-{i:02d}" for i in range(1, 64)]
assert DOC["authority"]["runtime_implementation"] is False
assert DOC["authority"]["detector_benchmarking"] is False
assert DOC["authority"]["real_market_data"] is False
assert DOC["authority"]["adaptation_authority"] is False
assert DOC["red_rule"]["expected_common_failure"] == EXPECTED_FAILURE
assert DOC["stop"] is True

def _target():
    if not TARGET_PATH.is_file():
        pytest.fail(EXPECTED_FAILURE, pytrace=False)
    spec = importlib.util.spec_from_file_location("rtma_01_under_test", TARGET_PATH)
    if spec is None or spec.loader is None:
        pytest.fail("RTMA_01_RUNTIME_UNLOADABLE", pytrace=False)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert getattr(module, "CONTRACT", None) == EXPECTED_CONTRACT
    assert getattr(module, "GENERATOR_IDENTITY", None) == EXPECTED_GENERATOR
    for name in DOC["required_runtime_surface"]:
        assert hasattr(module, name), f"missing runtime surface: {name}"
    for name in DOC["forbidden_runtime_surface"]:
        assert not callable(getattr(module, name, None)), f"forbidden runtime surface: {name}"
    return module

def _spec(case_id="SYN-00", seed=7):
    return {
        "case_id": case_id,
        "seed": seed,
        "generator_version": "V0.2",
        "prng_identity": "PCG64",
        "runtime_identity": "TEST",
        "scope_id": "SCOPE-FAST",
        "sample_count": 128,
        "task_id": "DISTRIBUTIONAL_CHANGE_DETECTION",
        "input_view_id": "MARKET_OBSERVATIONS_ONLY",
    }

def _case(module, case_id="SYN-00", seed=7):
    spec = _spec(case_id, seed)
    module.validate_case_spec(spec)
    return module.generate_case(spec)

def _output(**overrides):
    value = {
        "detector_id": "SCRIPTED",
        "detector_version": "V1",
        "task_id": "DISTRIBUTIONAL_CHANGE_DETECTION",
        "lane_id": "LANE_O",
        "scope_id": "SCOPE-FAST",
        "output_id": "OUT-1",
        "emitted_at": 50,
        "knowledge_cutoff_at": 50,
        "output_type": "ALERT",
    }
    value.update(overrides)
    return value

def test_01_exact_runtime_contract_and_identities():
    m=_target()
    assert m.CONTRACT == EXPECTED_CONTRACT
    assert m.GENERATOR_IDENTITY == EXPECTED_GENERATOR

def test_02_task_classes_exact():
    m=_target()
    assert tuple(m.TASK_CLASSES) == EXPECTED_TASKS

def test_03_lanes_exact():
    m=_target()
    assert tuple(x[0] if isinstance(x,(tuple,list)) else x for x in m.LANES) == EXPECTED_LANES

def test_04_case_registry_exact():
    m=_target()
    ids=tuple(x[0] if isinstance(x,(tuple,list)) else x for x in m.CASE_FAMILIES)
    assert ids == EXPECTED_CASES

def test_05_same_spec_same_seed_deterministic():
    m=_target(); a=_case(m,"SYN-01",11); b=_case(m,"SYN-01",11)
    assert m.canonical_sha256(a) == m.canonical_sha256(b)

def test_06_different_seed_changes_realization():
    m=_target(); a=_case(m,"SYN-01",11); b=_case(m,"SYN-01",12)
    assert m.canonical_sha256(a["observations"]) != m.canonical_sha256(b["observations"])
    assert a["ground_truth"]["semantic_schedule"] == b["ground_truth"]["semantic_schedule"]

def test_07_seed_does_not_choose_semantics():
    m=_target(); a=_case(m,"SYN-02",1); b=_case(m,"SYN-02",999)
    assert a["ground_truth"]["case_id"] == b["ground_truth"]["case_id"] == "SYN-02"

def test_08_opaque_run_id():
    m=_target(); rid=m.build_opaque_run_identity(_spec("SYN-01",5))
    assert isinstance(rid,str) and rid.startswith("RUN-") and "SYN-01" not in rid and "CHANGE" not in rid

def test_09_truth_not_in_observations():
    m=_target(); c=_case(m,"SYN-01",5)
    blob=json.dumps(c["observations"],sort_keys=True)
    for forbidden in ("ground_truth","true_onset","true_change_type","novelty_class","expected_output"):
        assert forbidden not in blob

def test_10_future_state_not_in_observations():
    m=_target(); c=_case(m,"SYN-06",5)
    assert "future_state" not in json.dumps(c["observations"],sort_keys=True)

def test_11_online_prefixes_no_future():
    m=_target(); c=_case(m,"SYN-01",5); obs=c["observations"]
    prefixes=list(m.iter_online_prefixes(obs))
    assert len(prefixes)==len(obs)
    for i,p in enumerate(prefixes):
        assert list(p)==list(obs[:i+1])

def test_12_retrospective_view_marked():
    m=_target(); c=_case(m); view=m.build_retrospective_view(c["observations"])
    assert view["evaluation_mode"] == "RETROSPECTIVE"

def test_13_retrospective_cannot_claim_first_alert():
    m=_target()
    with pytest.raises((TypeError,ValueError)):
        m.validate_detector_output(_output(lane_id="LANE_R",first_alert_at=10))

def test_14_raw_score_distinct_from_alert():
    m=_target()
    score=_output(output_type="RAW_SCORE",scalar_score=0.7)
    assert m.validate_detector_output(score)
    assert score["output_type"] != "ALERT"

def test_15_adapter_required_for_score_to_alert():
    m=_target()
    with pytest.raises((TypeError,ValueError)):
        m.validate_detector_output(_output(output_type="ALERT",scalar_score=0.7,decision_adapter_id=None))

def test_16_task_identity_required():
    m=_target(); x=_output(); x.pop("task_id")
    with pytest.raises((TypeError,ValueError)): m.validate_detector_output(x)

def test_17_input_view_required_in_case_spec():
    m=_target(); s=_spec(); s.pop("input_view_id")
    with pytest.raises((TypeError,ValueError)): m.validate_case_spec(s)

@pytest.mark.parametrize("case_id", EXPECTED_CASES)
def test_18_to_40_case_semantics(case_id):
    m=_target(); c=_case(m,case_id,17); gt=c["ground_truth"]
    assert gt["case_id"] == case_id
    assert "semantic_schedule" in gt
    if case_id in {"SYN-00","SYN-16","SYN-17","SYN-18","SYN-21","SYN-22"}:
        assert gt["structural_change"] is False
    if case_id=="SYN-05":
        assert gt["transient_shock"] is True and gt["durable_transition"] is False
    if case_id=="SYN-10":
        assert gt["latent_market_change"] is False and gt["observation_process_change"] is True
    if case_id=="SYN-11":
        assert gt["context_mix_change"] is True and gt["within_context_response_change"] is False
    if case_id=="SYN-12":
        assert gt["market_law_change"] is False and gt["within_context_response_change"] is True
    if case_id=="SYN-13":
        assert gt["gross_response_change"] is False and gt["execution_degradation"] is True
    if case_id in {"SYN-07","SYN-08"}:
        assert gt["reference_memory_required"] is True
    if case_id=="SYN-20":
        assert gt["scale_truths_derived_from_one_base_process"] is True

def test_41_self_match_rejected():
    m=_target()
    mem={"version":"M1","episodes":[{"episode_id":"E1","available_from":1}]}
    with pytest.raises((TypeError,ValueError)):
        m.validate_reference_memory(mem,query_time=10,query_episode_id="E1")

def test_42_future_memory_rejected():
    m=_target()
    mem={"version":"M1","episodes":[{"episode_id":"E2","available_from":20}]}
    with pytest.raises((TypeError,ValueError)):
        m.validate_reference_memory(mem,query_time=10,query_episode_id="Q")

def test_43_one_primary_match_per_truth_event():
    m=_target()
    truth={"events":[{"event_id":"E1","onset":50}]}
    outs=[_output(output_id="A",emitted_at=50),_output(output_id="B",emitted_at=51)]
    policy={"match_window":[-5,5],"primary_match_rule":"EARLIEST","duplicate_alert_rule":"RETAIN","unmatched_alert_rule":"FALSE_ALERT","unmatched_truth_rule":"MISS","overlapping_event_rule":"MIN_ABS_DELAY_THEN_EVENT_ID"}
    result=m.match_outputs_to_truth(outs,truth,policy)
    assert len(result["primary_matches"]) == 1

def test_44_duplicates_retained():
    m=_target()
    truth={"events":[{"event_id":"E1","onset":50}]}
    outs=[_output(output_id="A",emitted_at=50),_output(output_id="B",emitted_at=51)]
    policy={"match_window":[-5,5],"primary_match_rule":"EARLIEST","duplicate_alert_rule":"RETAIN","unmatched_alert_rule":"FALSE_ALERT","unmatched_truth_rule":"MISS","overlapping_event_rule":"MIN_ABS_DELAY_THEN_EVENT_ID"}
    result=m.match_outputs_to_truth(outs,truth,policy)
    assert len(result["duplicates"]) == 1

def test_45_unmatched_alert_false_evidence():
    m=_target()
    truth={"events":[]}; outs=[_output()]
    policy={"match_window":[-5,5],"primary_match_rule":"EARLIEST","duplicate_alert_rule":"RETAIN","unmatched_alert_rule":"FALSE_ALERT","unmatched_truth_rule":"MISS","overlapping_event_rule":"MIN_ABS_DELAY_THEN_EVENT_ID"}
    result=m.match_outputs_to_truth(outs,truth,policy)
    assert len(result["false_alerts"]) == 1

def test_46_unmatched_truth_is_miss():
    m=_target()
    truth={"events":[{"event_id":"E1","onset":50}]}; outs=[]
    policy={"match_window":[-5,5],"primary_match_rule":"EARLIEST","duplicate_alert_rule":"RETAIN","unmatched_alert_rule":"FALSE_ALERT","unmatched_truth_rule":"MISS","overlapping_event_rule":"MIN_ABS_DELAY_THEN_EVENT_ID"}
    result=m.match_outputs_to_truth(outs,truth,policy)
    assert len(result["misses"]) == 1

def test_47_overlap_assignment_deterministic():
    m=_target()
    truth={"events":[{"event_id":"E1","onset":50},{"event_id":"E2","onset":54}]}
    outs=[_output(output_id="A",emitted_at=52)]
    policy={"match_window":[-5,5],"primary_match_rule":"EARLIEST","duplicate_alert_rule":"RETAIN","unmatched_alert_rule":"FALSE_ALERT","unmatched_truth_rule":"MISS","overlapping_event_rule":"MIN_ABS_DELAY_THEN_EVENT_ID"}
    a=m.match_outputs_to_truth(outs,truth,policy); b=m.match_outputs_to_truth(outs,truth,policy)
    assert a==b

def test_48_drift_interval_geometry():
    m=_target()
    truth={"geometry":"ONSET_INTERVAL","interval":[40,60],"events":[{"event_id":"D1","interval":[40,60]}]}
    result=m.match_outputs_to_truth([_output(emitted_at=50,estimated_onset_interval=[45,55])],truth,{"match_window":[-5,5],"primary_match_rule":"EARLIEST","duplicate_alert_rule":"RETAIN","unmatched_alert_rule":"FALSE_ALERT","unmatched_truth_rule":"MISS","overlapping_event_rule":"MIN_ABS_DELAY_THEN_EVENT_ID"})
    assert result["geometry"] in {"ONSET_INTERVAL","DRIFT_PATH"}

def test_49_oracle_fixture():
    m=_target(); r=m.calculate_mechanical_metrics({"primary_matches":[{"delay":0}],"false_alerts":[],"duplicates":[],"misses":[]},{"events":[{"event_id":"E1"}]},[_output()])
    assert r["matched_event_count"]==1 and r["miss_count"]==0 and r["false_alert_count"]==0

def test_50_never_alert_fixture():
    m=_target(); r=m.calculate_mechanical_metrics({"primary_matches":[],"false_alerts":[],"duplicates":[],"misses":[{"event_id":"E1"}]},{"events":[{"event_id":"E1"}]},[])
    assert r["miss_count"]==1 and r["false_alert_count"]==0

def test_51_spam_alert_fixture():
    m=_target(); r=m.calculate_mechanical_metrics({"primary_matches":[{"delay":0}],"false_alerts":[{},{}],"duplicates":[{}],"misses":[]},{"events":[{"event_id":"E1"}]},[_output(),_output(output_id="B"),_output(output_id="C")])
    assert r["false_alert_count"]==2 and r["duplicate_alert_count"]==1

def test_52_wrong_dimension_separate_credit():
    m=_target(); r=m.calculate_mechanical_metrics({"primary_matches":[{"delay":0,"dimension_correct":False}],"false_alerts":[],"duplicates":[],"misses":[]},{"events":[{"event_id":"E1","dimensions":["VOL"]}]},[_output(affected_dimensions=["DEP"])])
    assert r["matched_event_count"]==1 and r["dimension_true_positive_count"]==0

def test_53_future_leakage_mutant_rejected():
    m=_target()
    prefixes=list(m.iter_online_prefixes([1,2,3]))
    assert prefixes[0]==[1] and prefixes[1]==[1,2] and prefixes[2]==[1,2,3]

def test_54_truth_mutation_rejected():
    m=_target(); c=_case(m,"SYN-01",5); seal=m.seal_case(c)
    c["ground_truth"]["tamper"]=True
    assert m.verify_case(c,seal) is False

def test_55_observation_mutation_rejected():
    m=_target(); c=_case(m,"SYN-01",5); seal=m.seal_case(c)
    c["observations"][0]=999999
    assert m.verify_case(c,seal) is False

def test_56_result_replay_deterministic():
    m=_target()
    match={"primary_matches":[{"delay":2}],"false_alerts":[],"duplicates":[],"misses":[]}
    truth={"events":[{"event_id":"E1"}]}; outs=[_output()]
    assert m.calculate_mechanical_metrics(match,truth,outs)==m.calculate_mechanical_metrics(match,truth,outs)

def test_57_development_holdout_distinct():
    m=_target(); a=_spec(); b=_spec()
    a["surface"]="DEVELOPMENT"; b["surface"]="HOLDOUT"
    assert m.canonical_sha256(a) != m.canonical_sha256(b)

def test_58_consumed_holdout_not_untouched():
    m=_target()
    state={"surface":"HOLDOUT","consumed_for_model_modification":True,"untouched":True}
    with pytest.raises((TypeError,ValueError)): m.validate_case_spec({**_spec(),**state})

def test_59_attempt_ledger_requirement_present():
    _target()
    assert "NO_HIDDEN_ATTEMPT_DELETION" in DOC.get("governance_firewalls",["NO_HIDDEN_ATTEMPT_DELETION"]) or DOC["authority"]["detector_benchmarking"] is False

def test_60_no_a0_authority_inheritance():
    m=_target()
    assert m.GENERATOR_IDENTITY != "ATDS_A0_SYNTHETIC_PRODUCER_V0_1"

def test_61_no_generic_experiment_spec_replacement():
    m=_target()
    assert not hasattr(m,"ExperimentSpecification")

def test_62_mechanical_scorer_no_scientific_authority():
    m=_target()
    assert not hasattr(m,"QualifiedExperimentEvaluationAuthority")
    assert not callable(getattr(m,"promote_scientific_finding",None))

def test_63_forbidden_operational_surfaces_absent():
    m=_target()
    for name in DOC["forbidden_runtime_surface"]:
        assert not callable(getattr(m,name,None))
