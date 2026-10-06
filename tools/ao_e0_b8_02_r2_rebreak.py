from __future__ import annotations
import json

EXPECTED = {
    "cell_identity": "sha256:38610ff2afd70998a7fa3e522575faf697ec3159e00829c2b2bbd5da45c52054",
    "strategy_version_identity": "sha256:0927e983046ef99a01d2a5c165d18ba5d501f69fb863875f72303b95f69b9687",
    "delta_min": 5.0,
    "f2": "F2_S4",
    "required_n": 58927,
    "m04_estimator": "ADJUSTED",
    "m04_lags": "1..min(n-1,ceil(n^(1/3)))",
    "m04_threshold": 0.05,
    "m05_scheme": "MOVING_BLOCK",
    "m05_interval": "PERCENTILE",
    "m05_confidence": 0.99,
    "m05_replications": 50000,
    "m05_seed": 21449402,
    "m05_block_rule": "min(n,1+max(M04_LAGS(n)))",
    "m07_threshold": 5.0,
    "m08_threshold": 0.05,
    "dr01_table_blob": "1126cf429dc064104bdfe0615cea0a96b95b540e",
}

def _req(cond, code):
    if not cond:
        raise ValueError(code)

def validate(doc):
    _req(doc["b8_closure_candidate"] == "QUALIFIED_FOR_HUMAN_ADOPTION", "BAD_VERDICT")
    b=doc["canonical_bindings"]
    _req(b["cell_identity"] == EXPECTED["cell_identity"], "CELL_IDENTITY_MISMATCH")
    _req(b["strategy_version_identity"] == EXPECTED["strategy_version_identity"], "STRATEGY_VERSION_MISMATCH")
    _req(b["dr01_decision_table_blob"] == EXPECTED["dr01_table_blob"], "DR01_TABLE_MISMATCH")

    c=doc["claim"]
    _req(c["delta_min"] == EXPECTED["delta_min"], "DELTA_MIN_MISMATCH")
    _req(c["minimum_required_cost_robustness_node"] == EXPECTED["f2"], "F2_MISMATCH")
    _req(c["h0"] == "theta_AO_E0 <= 5.0", "H0_MISMATCH")
    _req(c["h1"] == "theta_AO_E0 > 5.0", "H1_MISMATCH")
    _req(c["design_alternative_theta"] == 10.0 and c["design_alternative_is_qualification_threshold"] is False, "DESIGN_ALT_SEMANTICS_MISMATCH")

    m=doc["method_freeze"]
    _req(m["m04"]["acf_estimator"] == EXPECTED["m04_estimator"], "M04_ESTIMATOR_MISMATCH")
    _req(m["m04"]["lags_rule"] == EXPECTED["m04_lags"], "M04_LAGS_MISMATCH")
    _req(m["m04"]["absolute_threshold"] == EXPECTED["m04_threshold"], "M04_THRESHOLD_MISMATCH")
    _req(m["m05"]["scheme"] == EXPECTED["m05_scheme"], "M05_SCHEME_MISMATCH")
    _req(m["m05"]["interval_method"] == EXPECTED["m05_interval"], "M05_INTERVAL_MISMATCH")
    _req(m["m05"]["confidence_level"] == EXPECTED["m05_confidence"], "M05_CONFIDENCE_MISMATCH")
    _req(m["m05"]["replications"] == EXPECTED["m05_replications"], "M05_REPLICATIONS_MISMATCH")
    _req(m["m05"]["seed"] == EXPECTED["m05_seed"], "M05_SEED_MISMATCH")
    _req(m["m05"]["block_length_rule"] == EXPECTED["m05_block_rule"], "M05_BLOCK_RULE_MISMATCH")
    _req(m["m06"]["final_required_n"] == EXPECTED["required_n"], "M06_N_MISMATCH")
    _req(m["m07"]["materiality_abs_delta"] == EXPECTED["m07_threshold"], "M07_THRESHOLD_MISMATCH")
    _req(m["m08"]["max_inclusion_rate_gap"] == EXPECTED["m08_threshold"], "M08_THRESHOLD_MISMATCH")
    _req(m["m09"]["state"] == "BINDING_REQUIRED_EXECUTION_BLOCKED_PENDING_B8_AND_B12", "M09_ROUTING_MISMATCH")
    _req(m["m10"]["state"] == "NOT_APPLICABLE_TO_BASE_CC05", "M10_ROUTING_MISMATCH")
    _req(m["m11"]["search_provenance_gate"] == "PASS_WITH_PARTIAL_SEARCH_UNIVERSE", "M11_ROUTING_MISMATCH")

    d=doc["decision_rule_freeze"]
    _req(d["state"] == "HUMAN_ADOPTED_BINDING_FROZEN", "DR01_NOT_FROZEN")
    _req(d["m05_support"] == "lower > 5.0", "SUPPORT_MAPPING_MISMATCH")
    _req(d["m05_refute"] == "upper <= 5.0", "REFUTE_MAPPING_MISMATCH")
    _req(d["m05_inconclusive"] == "otherwise", "INCONCLUSIVE_MAPPING_MISMATCH")
    _req(d["n_lt_58927"] == "INCONCLUSIVE / INSUFFICIENT_SAMPLE", "M06_DISPOSITION_MISMATCH")
    _req(d["m07_material_influence"] == "INCONCLUSIVE", "M07_DISPOSITION_MISMATCH")
    _req(d["m08_material_selection_asymmetry"] == "INCONCLUSIVE", "M08_DISPOSITION_MISMATCH")
    _req(d["all_simultaneous_material_reasons_preserved"] is True, "MULTIFAIL_REASONS_NOT_PRESERVED")
    _req(d["fixed_primary_reason_precedence"] is True, "PRECEDENCE_NOT_FIXED")

    p=doc["provenance"]
    _req(p["old_e1_oos_independent_confirmation_eligible"] is False, "OLD_OOS_RELABELED")
    _req(p["prior_exposure_state"] == "CONTAMINATED", "EXPOSURE_STATE_MISMATCH")
    _req(p["search_universe_status"] == "PARTIAL_SEARCH_UNIVERSE", "SEARCH_UNIVERSE_MISMATCH")
    _req(p["n_trials"] is None, "N_TRIALS_INVENTED")
    _req(p["confirmatory_route"] == "NEW_FORWARD_DATA_ONLY", "FORWARD_ROUTE_MISMATCH")
    _req(p["invent_numeric_multiplicity_correction"] is False, "MULTIPLICITY_CORRECTION_INVENTED")

    nf=doc["no_free_material_parameter_decision_check"]
    _req(nf["post_result_discretion"] == "ZERO", "POST_RESULT_DISCRETION_PRESENT")
    _req(nf["new_material_parameter_found"] is False, "NEW_MATERIAL_PARAMETER_FOUND")
    _req(nf["new_material_decision_found"] is False, "NEW_MATERIAL_DECISION_FOUND")

    t=doc["timing_attestation"]
    _req(all(t[k] is True for k in [
        "b8_qualification_occurs_before_b12_opening",
        "b8_qualification_occurs_before_forward_observation",
        "b8_qualification_occurs_before_oos_consumption",
        "b8_qualification_occurs_before_real_ao_e0_execution",
    ]), "TIMING_FIREWALL_BROKEN")
    _req(all(t[k] is False for k in [
        "new_ao_e0_performance_data_read",
        "new_ao_e0_performance_data_calculated",
        "new_ao_e0_performance_data_materialized",
        "new_ao_e0_performance_data_used",
    ]), "PERFORMANCE_DATA_CONSUMED")

    _req(doc["state"]["b8"] == "NOT_CLOSED_PENDING_DISTINCT_HUMAN_ADOPTION", "B8_AUTO_CLOSED")
    _req(doc["state"]["b12"] == "CLOSED", "B12_OPENED")

    _req(all(v is False for v in doc["authority"].values()), "AUTHORITY_CREATED")
    _req(doc["force"] is False, "FORCE_TRUE")
    return True

if __name__ == "__main__":
    import pathlib
    root=pathlib.Path(__file__).resolve().parents[1]
    doc=json.loads((root/"GOVERNANCE"/"AO-E0-B8-02-R2-FINAL-FORWARD-ONLY-PREREGISTRATION-FREEZE-CANDIDATE-V0.2.json").read_text())
    validate(doc)
    print("AO_E0_B8_02_R2_REBREAK_PASS")
