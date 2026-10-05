from __future__ import annotations
CONTRACT="ATDS_AO_E0_DT_01A_CC05_FIRST_USE_DATA_FAMILY_ADMISSION_V0_1"
CELL_IDENTITY="sha256:38610ff2afd70998a7fa3e522575faf697ec3159e00829c2b2bbd5da45c52054"
EXPECTED={
 "raw":{"dataset_identity":"SOURCE_B_USTECH_PRICE_CORE_V0_1","manifest_sha256":"c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5","inventory_digest":"5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf","role":"RAW_BID_ASK_EXECUTION_INPUT_UNDER_E1_04_ONLY"},
 "ap0":{"dataset_identity":"USTECH_PROFILE_MINUTE_CORE_V0_1","manifest_sha256":"62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce","file_set_digest":"1ff14ab4fea11c2480088a322f5bec23ea183de14cbc65ee6c684c7ea185062a","schema_identity":"5c5f5302891567b62024c718d4e7700b766d1ace8f3e40f7a0a29cee6b93bf88","role":"DETERMINISTIC_PARENT_FOR_E1_03_H1_DERIVATION"},
 "h1":{"dataset_identity":"USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1","canonical_stream_sha256":"15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f","role":"MOMENTUM_V1_SIGNAL_INPUT_ONLY"}
}
AUTHORITY={"temporal":False,"scientific":False,"rvo":False,"oos_consumption":False,"performance_observation":False}
def qualify(package:dict)->dict:
    if package.get("cell_identity")!=CELL_IDENTITY: return {"status":"BLOCKED","reason":"CELL_IDENTITY_MISMATCH"}
    if package.get("claim_class")!="CC05_ECONOMIC_NET_PROFITABILITY": return {"status":"BLOCKED","reason":"CLAIM_SCOPE_MISMATCH"}
    if package.get("source_b_feed_equals_vt_execution_feed") is not False: return {"status":"BLOCKED","reason":"SOURCE_FEED_EQUIVALENCE_LAUNDERING"}
    if package.get("native_dukascopy_tick_equivalence_claimed") is not False: return {"status":"BLOCKED","reason":"NATIVE_DUKASCOPY_EQUIVALENCE_LAUNDERING"}
    if package.get("data02_cc02_transferred_to_cc05") is not False: return {"status":"BLOCKED","reason":"CC02_TO_CC05_QUALIFICATION_TRANSFER"}
    fam=package.get("family")
    if not isinstance(fam,dict): return {"status":"BLOCKED","reason":"DATA_FAMILY_MISSING"}
    for key in ("raw","ap0","h1"):
        if fam.get(key)!=EXPECTED[key]: return {"status":"BLOCKED","reason":f"{key.upper()}_IDENTITY_OR_ROLE_MISMATCH"}
    if package.get("mid_as_execution_price") is not False: return {"status":"BLOCKED","reason":"MID_EXECUTION_LAUNDERING"}
    if package.get("temporal_pass_claimed") is not False: return {"status":"BLOCKED","reason":"DATA_TO_TEMPORAL_AUTHORITY_LAUNDERING"}
    if package.get("scientific_support_claimed") is not False: return {"status":"BLOCKED","reason":"DATA_TO_SCIENTIFIC_AUTHORITY_LAUNDERING"}
    return {"status":"QUALIFIED_CANDIDATE","b10":"CANDIDATE_PASS","unknown_unknown_coverage":"NOT_CLAIMED"}
