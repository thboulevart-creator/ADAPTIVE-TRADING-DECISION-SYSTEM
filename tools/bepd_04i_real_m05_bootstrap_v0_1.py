from __future__ import annotations
import hashlib, random
from tools.bepd_04e_response_generalization_v0_1 import aggregate_week_counts, moving_block_ratio_ci

CONTRACT="ATDS_BEPD_04I_REAL_M05_BOOTSTRAP_HARNESS_V0_1"
EXPECTED={
    "method":"M05",
    "scheme":"MOVING_BLOCK",
    "statistic":"RATIO_OF_SUMS",
    "replications":200000,
    "block_length":13,
    "seed":40420261006,
    "confidence_level":0.99,
    "interval_method":"PERCENTILE",
    "execution_scope":"EXPLORATORY_ONLY",
}
EXPECTED_BINDINGS={
    "bepd04h_activation_blob":"7f2fd16d7cc636e8d3e3cb23f618deb55407bcf1",
    "bepd04g_adjudication_blob":"47c1cbb109381929840cf66cd04c0695be81e4c1",
    "event_ledger_blob":"0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2",
    "calendar_blob":"26385eb2547892df4b87206ad59fc2ba07721354",
    "runtime_blob":"61a996562fe18e0e2efd6f16db27a48738e60421",
    "reference_blob":"e4ad2b642265889455e33f23ead3c5b57c1a7eae",
    "breaker_blob":"eda63bf26230a2b48eb75bb655e64e766b66c1a3",
}

def guard_bindings(bindings):
    if not isinstance(bindings,dict): raise ValueError("BINDINGS_REQUIRED")
    for k,v in EXPECTED_BINDINGS.items():
        if bindings.get(k)!=v: raise ValueError(f"BINDING_MISMATCH:{k}")
    return True

def guard_config(cfg):
    if not isinstance(cfg,dict): raise ValueError("CONFIG_REQUIRED")
    for k,v in EXPECTED.items():
        if cfg.get(k)!=v: raise ValueError(f"PARAMETER_MISMATCH:{k}")
    if cfg.get("response_subgroup") is not None: raise ValueError("SUBGROUP_BOOTSTRAP_FORBIDDEN")
    if cfg.get("sensitivity_analysis") is not False: raise ValueError("SENSITIVITY_ANALYSIS_FORBIDDEN")
    if cfg.get("alternative_response") is not False: raise ValueError("ALTERNATIVE_RESPONSE_FORBIDDEN")
    if cfg.get("alternative_horizon") is not False: raise ValueError("ALTERNATIVE_HORIZON_FORBIDDEN")
    if cfg.get("occurrence_x_response") is not False: raise ValueError("OCCURRENCE_X_RESPONSE_FORBIDDEN")
    if cfg.get("time_to_reintegration") is not False: raise ValueError("TIME_TO_REINTEGRATION_FORBIDDEN")
    if cfg.get("prediction_claim") is not False: raise ValueError("PREDICTION_FORBIDDEN")
    if cfg.get("edge_claim") is not False: raise ValueError("EDGE_FORBIDDEN")
    if cfg.get("strategy_claim") is not False: raise ValueError("STRATEGY_FORBIDDEN")
    if cfg.get("trading_authority")!="NONE": raise ValueError("TRADING_AUTHORITY_FORBIDDEN")
    if cfg.get("post_result_parameter_selection") is not False: raise ValueError("POST_RESULT_SELECTION_FORBIDDEN")
    if cfg.get("competing_canonical_execution") is not False: raise ValueError("SECOND_CANONICAL_EXECUTION_FORBIDDEN")
    return True

def execute_primary(calendar,events,cfg,bindings):
    guard_bindings(bindings); guard_config(cfg)
    return moving_block_ratio_ci(
        calendar,events,
        execution_scope="REAL_AUTHORIZED",
        block_length=13,
        replications=200000,
        seed=40420261006,
        confidence_level=0.99,
        interval_method="PERCENTILE",
        real_execution_authorized=True,
    )

def distribution_evidence(calendar,events):
    agg=aggregate_week_counts(calendar,events)
    n=len(agg); block_length=13
    rng=random.Random(40420261006)
    digest=hashlib.sha256()
    reps=[]
    max_start=n-block_length
    for _ in range(200000):
        sampled=[]
        while len(sampled)<n:
            start=rng.randrange(max_start+1)
            sampled.extend(agg[start:start+block_length])
        sampled=sampled[:n]
        denom=sum(x["event_count"] for x in sampled)
        if denom<=0: raise ValueError("ZERO_DENOMINATOR_REPLICATE")
        value=sum(x["success_count"] for x in sampled)/denom
        reps.append(value)
        digest.update(value.hex().encode("ascii")); digest.update(b"\n")
    ordered=sorted(reps)
    sorted_digest=hashlib.sha256()
    for value in ordered:
        sorted_digest.update(value.hex().encode("ascii")); sorted_digest.update(b"\n")
    return {
        "replications":len(reps),
        "sequence_digest_sha256":digest.hexdigest(),
        "sorted_distribution_digest_sha256":sorted_digest.hexdigest(),
        "minimum_replicate_statistic":min(reps),
        "maximum_replicate_statistic":max(reps),
    }
