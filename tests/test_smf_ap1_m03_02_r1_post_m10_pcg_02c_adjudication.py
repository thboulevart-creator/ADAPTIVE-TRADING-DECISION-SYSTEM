from __future__ import annotations
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ADJ=ROOT/"GOVERNANCE"/"SMF-AP1-M03-02-R1-POST-M10-PCG-02C-HUMAN-ADJUDICATION-2026-10-06.md"

EXPECTED={
    "pcg02b_receipt":"5e7810ebd00f65a001772ecd0f53e71181eaeb9a",
    "pcg02b_closure":"1c35d07477a65809ebcfd4e0812fbea7557afa0b",
    "primary":"c36e30ab427ba092bfb935aeec42d32881765d39",
    "reference":"c36e30ab427ba092bfb935aeec42d32881765d39",
    "parity":"9a0ccb4afa82c8bacd774fe6a688621596642184",
}

def text():
    return ADJ.read_text(encoding="utf-8")

def blob(path):
    return subprocess.check_output(
        ["git","-C",str(ROOT),"rev-parse",f"HEAD:{path}"],
        text=True
    ).strip()

def test_01_exact_pcg02b_bindings():
    assert blob("reports/program/2026-10-06-SMF-AP1-M03-02-R1-POST-M10-PCG-02B-FINAL-EXECUTION-RECEIPT-V0.1.json")==EXPECTED["pcg02b_receipt"]
    assert blob("reports/program/2026-10-06-SMF-AP1-M03-02-R1-POST-M10-PCG-02B-FINAL-CLOSURE.md")==EXPECTED["pcg02b_closure"]
    assert blob("artifacts/smf_ap1_m03_02_r1_post_m10_pcg_02b/REAL_PCG_RESULT.json")==EXPECTED["primary"]
    assert blob("artifacts/smf_ap1_m03_02_r1_post_m10_pcg_02b/REAL_PCG_REFERENCE_RESULT.json")==EXPECTED["reference"]
    assert blob("artifacts/smf_ap1_m03_02_r1_post_m10_pcg_02b/REAL_REFERENCE_PARITY.json")==EXPECTED["parity"]

def test_02_technical_result_is_human_adopted():
    t=text()
    assert "PCG_02B_TECHNICAL_RESULT =\nHUMAN_ADOPTED" in t
    assert "PCG_02B_GATE_RESULT =\nHUMAN_ADOPTED" in t
    assert "PCG_02B_BLOCKED_RESULT =\nHUMAN_ADOPTED" in t

def test_03_exact_claim_unit_and_classification_preserved():
    t=text()
    assert "CLAIM_UNIT =\ntick_count p50" in t
    assert "INPUT_CLASSIFICATION =\nMATERIAL_TEMPORAL_VARIATION" in t

def test_04_exact_blocked_result_preserved():
    t=text()
    assert "SELECTED_ROUTE =\nNONE" in t
    assert "GATE_STATE =\n[BLOCKED]" in t
    assert "DECISION_REASON =\nMATERIAL_CLAIM_UNIT_NO_ADMISSIBILITY_ROUTE" in t
    assert "BLOCK_REASON =\nMATERIAL_CLAIM_UNIT_NO_ADMISSIBILITY_ROUTE" in t
    assert "QUALIFYING_ROUTES =\n[]" in t
    assert "OVERALL_GATE_ADMISSIBILITY =\nBLOCKED" in t
    assert "AUTHORITY_CREATED =\nNONE" in t

def test_05_blocked_semantics_is_narrow():
    t=text()
    assert "DOES NOT CURRENTLY SATISFY" in t
    for forbidden in (
        "POOLING_IS_SCIENTIFICALLY_IMPOSSIBLE",
        "CLAIM_IS_FALSE",
        "FORMAL_NONSTATIONARITY",
        "STATIONARITY_REFUTED",
        "CHANGE_POINT",
        "REGIME_CHANGE",
        "MARKET_STRUCTURE_CAUSATION",
        "STRATEGY_INVALID",
        "TRADING_EDGE_ABSENT",
    ):
        assert forbidden in t

def test_06_old_pooled_claim_remains_blocked():
    t=text()
    assert "POST_M10-DC01-TICKCOUNT-P50-POOLED-HISTORICAL-REFERENCE =\nPRESERVED_AS_BLOCKED" in t
    assert "POST_M10-DA01-POOLED-TICKCOUNT-P50-REFERENCE-CONSTRUCTION =\nBLOCKED" in t
    assert "SEMANTIC_REWRITE =\nFORBIDDEN" in t
    assert "UNIQUE_POOLED_REFERENCE_CALCULATION =\nNOT_AUTHORIZED" in t

def test_07_route_a_not_selected():
    assert "ROUTE_A =\nNOT_SELECTED_AT_THIS_STAGE" in text()

def test_08_route_b_is_preferred_design_direction_only():
    t=text()
    assert "ROUTE_B =\nSELECTED_AS_PREFERRED_NEXT_DESIGN_DIRECTION" in t
    assert "PREFERRED_NEXT_ROUTE =\nB" in t
    assert "ROUTE_B_SEMANTICS =\nCONDITION_OR_STRATIFY_BY_TIME" in t
    assert "ROUTE_B_ADMISSIBLE =\nNOT_YET_ESTABLISHED" in t
    assert "TEMPORAL_CONDITIONING_EXECUTED =\nFALSE" in t

def test_09_route_c_not_selected():
    assert "ROUTE_C =\nNOT_SELECTED_AT_THIS_STAGE" in text()

def test_10_candidate_year_strata_are_design_only():
    t=text()
    assert "CANDIDATE_TEMPORAL_CONDITIONING =\nYEAR_STRATA" in t
    for year in ("UTC_YEAR:2022","UTC_YEAR:2023","UTC_YEAR:2024","UTC_YEAR:2025"):
        assert year in t
    assert "YEAR_STRATA_SPEC =\nNOT_YET_FROZEN" in t
    assert "YEAR_STRATA_SPEC_QUALIFIED =\nFALSE" in t

def test_11_epistemic_state_preserved():
    t=text()
    assert "EVIDENCE_STATE =\nEXPOSED" in t
    assert "CLAIM_PROVENANCE =\nRESULT_AWARE" in t
    assert "SAME_CORPUS_CONFIRMATORY_STATUS =\nNON_PRISTINE" in t
    assert "RESET_TO_PRISTINE =\nFORBIDDEN" in t

def test_12_methods_remain_closed():
    t=text()
    for method in ("M04","M05","M08","M09","M11"):
        assert f"{method} = CLOSED" in t

def test_13_authorities_all_false():
    t=text()
    for authority in (
        "POOLING_AUTHORITY",
        "CONDITIONING_EXECUTION_AUTHORITY",
        "METHOD_AUTHORITY",
        "METHOD_EXECUTION_AUTHORITY",
        "OOS_AUTHORITY",
        "TRADING_AUTHORITY",
        "CAPITAL_AUTHORITY",
    ):
        assert f"{authority} =\nFALSE" in t

def test_14_dc01_remains_closed():
    t=text()
    assert "SMF-AP1-M03-02-R1-POST-M10-DC-01 =\nCLOSED" in t
    assert "SEPARATE_HUMAN_AUTHORIZATION_REQUIRED =\nTRUE" in t
    assert "AUTOMATIC_OPEN =\nFALSE" in t

def test_15_no_execution_authority_for_dc01():
    t=text()
    assert "REAL_DATA_READ =\nFALSE" in t
    assert "CONDITIONING_EXECUTION =\nFALSE" in t
    assert "METHOD_EXECUTION =\nFALSE" in t

def test_16_no_pcg02c_runtime_or_data_artifact_surface():
    assert not list((ROOT/"tools").glob("*pcg_02c*"))
    assert not list((ROOT/"artifacts").glob("*pcg_02c*"))
    assert not list((ROOT/"artifacts").glob("*PCG-02C*"))

def test_17_record_ends_with_stop():
    assert text().rstrip().endswith("STOP.")
