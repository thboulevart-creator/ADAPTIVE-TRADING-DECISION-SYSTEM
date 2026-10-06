from __future__ import annotations
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

spec=importlib.util.spec_from_file_location("r2",ROOT/"tools"/"ao_e0_b8_02_r2_rebreak.py")
R2=importlib.util.module_from_spec(spec); spec.loader.exec_module(R2)
BASE=json.loads((ROOT/"GOVERNANCE"/"AO-E0-B8-02-R2-FINAL-FORWARD-ONLY-PREREGISTRATION-FREEZE-CANDIDATE-V0.2.json").read_text())

class TestAOE0B802R2(unittest.TestCase):
    def mutate(self,path,value,code):
        x=copy.deepcopy(BASE)
        cur=x
        for key in path[:-1]: cur=cur[key]
        cur[path[-1]]=value
        with self.assertRaisesRegex(ValueError,code):
            R2.validate(x)

    def test_00_green(self): self.assertTrue(R2.validate(copy.deepcopy(BASE)))
    def test_01_cell(self): self.mutate(["canonical_bindings","cell_identity"],"bad","CELL_IDENTITY_MISMATCH")
    def test_02_strategy(self): self.mutate(["canonical_bindings","strategy_version_identity"],"bad","STRATEGY_VERSION_MISMATCH")
    def test_03_dr01_table(self): self.mutate(["canonical_bindings","dr01_decision_table_blob"],"bad","DR01_TABLE_MISMATCH")
    def test_04_delta(self): self.mutate(["claim","delta_min"],4.0,"DELTA_MIN_MISMATCH")
    def test_05_f2(self): self.mutate(["claim","minimum_required_cost_robustness_node"],"F1_S1","F2_MISMATCH")
    def test_06_h0(self): self.mutate(["claim","h0"],"theta <= 0","H0_MISMATCH")
    def test_07_h1(self): self.mutate(["claim","h1"],"theta > 0","H1_MISMATCH")
    def test_08_design_alt(self): self.mutate(["claim","design_alternative_is_qualification_threshold"],True,"DESIGN_ALT_SEMANTICS_MISMATCH")
    def test_09_m04_est(self): self.mutate(["method_freeze","m04","acf_estimator"],"BIASED","M04_ESTIMATOR_MISMATCH")
    def test_10_m04_lags(self): self.mutate(["method_freeze","m04","lags_rule"],"1..10","M04_LAGS_MISMATCH")
    def test_11_m04_thr(self): self.mutate(["method_freeze","m04","absolute_threshold"],0.1,"M04_THRESHOLD_MISMATCH")
    def test_12_m05_scheme(self): self.mutate(["method_freeze","m05","scheme"],"IID","M05_SCHEME_MISMATCH")
    def test_13_m05_interval(self): self.mutate(["method_freeze","m05","interval_method"],"BASIC","M05_INTERVAL_MISMATCH")
    def test_14_m05_conf(self): self.mutate(["method_freeze","m05","confidence_level"],0.95,"M05_CONFIDENCE_MISMATCH")
    def test_15_m05_reps(self): self.mutate(["method_freeze","m05","replications"],1000,"M05_REPLICATIONS_MISMATCH")
    def test_16_m05_seed(self): self.mutate(["method_freeze","m05","seed"],1,"M05_SEED_MISMATCH")
    def test_17_block(self): self.mutate(["method_freeze","m05","block_length_rule"],"1","M05_BLOCK_RULE_MISMATCH")
    def test_18_n(self): self.mutate(["method_freeze","m06","final_required_n"],100,"M06_N_MISMATCH")
    def test_19_m07(self): self.mutate(["method_freeze","m07","materiality_abs_delta"],1.0,"M07_THRESHOLD_MISMATCH")
    def test_20_m08(self): self.mutate(["method_freeze","m08","max_inclusion_rate_gap"],0.5,"M08_THRESHOLD_MISMATCH")
    def test_21_m09(self): self.mutate(["method_freeze","m09","state"],"OPEN","M09_ROUTING_MISMATCH")
    def test_22_m10(self): self.mutate(["method_freeze","m10","state"],"APPLICABLE","M10_ROUTING_MISMATCH")
    def test_23_m11(self): self.mutate(["method_freeze","m11","search_provenance_gate"],"PASS","M11_ROUTING_MISMATCH")
    def test_24_dr_state(self): self.mutate(["decision_rule_freeze","state"],"OPEN","DR01_NOT_FROZEN")
    def test_25_support_map(self): self.mutate(["decision_rule_freeze","m05_support"],"point > 5","SUPPORT_MAPPING_MISMATCH")
    def test_26_refute_map(self): self.mutate(["decision_rule_freeze","m05_refute"],"point <= 5","REFUTE_MAPPING_MISMATCH")
    def test_27_inconclusive_map(self): self.mutate(["decision_rule_freeze","m05_inconclusive"],"REFUTE","INCONCLUSIVE_MAPPING_MISMATCH")
    def test_28_m06_disp(self): self.mutate(["decision_rule_freeze","n_lt_58927"],"REFUTE","M06_DISPOSITION_MISMATCH")
    def test_29_m07_disp(self): self.mutate(["decision_rule_freeze","m07_material_influence"],"DIAGNOSTIC","M07_DISPOSITION_MISMATCH")
    def test_30_m08_disp(self): self.mutate(["decision_rule_freeze","m08_material_selection_asymmetry"],"IGNORE","M08_DISPOSITION_MISMATCH")
    def test_31_multifail(self): self.mutate(["decision_rule_freeze","all_simultaneous_material_reasons_preserved"],False,"MULTIFAIL_REASONS_NOT_PRESERVED")
    def test_32_precedence(self): self.mutate(["decision_rule_freeze","fixed_primary_reason_precedence"],False,"PRECEDENCE_NOT_FIXED")
    def test_33_old_oos(self): self.mutate(["provenance","old_e1_oos_independent_confirmation_eligible"],True,"OLD_OOS_RELABELED")
    def test_34_exposure(self): self.mutate(["provenance","prior_exposure_state"],"PRISTINE","EXPOSURE_STATE_MISMATCH")
    def test_35_search(self): self.mutate(["provenance","search_universe_status"],"COMPLETE","SEARCH_UNIVERSE_MISMATCH")
    def test_36_trials(self): self.mutate(["provenance","n_trials"],1,"N_TRIALS_INVENTED")
    def test_37_route(self): self.mutate(["provenance","confirmatory_route"],"OLD_E1_OOS","FORWARD_ROUTE_MISMATCH")
    def test_38_multcorr(self): self.mutate(["provenance","invent_numeric_multiplicity_correction"],True,"MULTIPLICITY_CORRECTION_INVENTED")
    def test_39_discretion(self): self.mutate(["no_free_material_parameter_decision_check","post_result_discretion"],"NONZERO","POST_RESULT_DISCRETION_PRESENT")
    def test_40_new_param(self): self.mutate(["no_free_material_parameter_decision_check","new_material_parameter_found"],True,"NEW_MATERIAL_PARAMETER_FOUND")
    def test_41_new_decision(self): self.mutate(["no_free_material_parameter_decision_check","new_material_decision_found"],True,"NEW_MATERIAL_DECISION_FOUND")
    def test_42_b8_autoclose(self): self.mutate(["state","b8"],"CLOSED","B8_AUTO_CLOSED")
    def test_43_b12(self): self.mutate(["state","b12"],"OPEN","B12_OPENED")
    def test_44_authority(self): self.mutate(["authority","trading"],True,"AUTHORITY_CREATED")
    def test_45_force(self): self.mutate(["force"],True,"FORCE_TRUE")
    def test_46_performance_read(self): self.mutate(["timing_attestation","new_ao_e0_performance_data_read"],True,"PERFORMANCE_DATA_CONSUMED")
    def test_47_timing(self): self.mutate(["timing_attestation","b8_qualification_occurs_before_b12_opening"],False,"TIMING_FIREWALL_BROKEN")

if __name__=="__main__": unittest.main()
