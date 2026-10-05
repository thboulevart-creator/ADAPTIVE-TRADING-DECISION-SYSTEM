from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from tools.smf03_core_foundation import create_activation_record, ecdf_quantiles

CONTRACT = "ATDS_SMF_AP1_M03_01_BINDING_V0_1"
CLAIM_SCOPE_ID = "CC02_DESCRIPTIVE_MARKET_BEHAVIOR:RETROSPECTIVE_DESCRIPTIVE_ONLY:ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
COMPANION_ID = "ATDS_SMF_AP1_M03_COMPANION_V0_1"

AP1_PRODUCER_BLOB = "9f613063fb8a190a1ff6f2f8b12c97c4ed97712a"
DATA02_RECEIPT_BLOB = "ccfccda676abfe7e02082a331557ffed14e1f32b"
P121_RECEIPT_BLOB = "49142e1928cf32ec10ed9a4809388a782559ad42"
SMF_CORE_BLOB = "b67d63bbbc4f93be3fe1e7327c1f1f1cc440ebeb"
SMF_REFERENCE_BLOB = "00131e4369c15cf5efdbc3a6523b57e77b91b2f4"
METHOD_PROCEDURE_REF = "gitblob:b67d63bbbc4f93be3fe1e7327c1f1f1cc440ebeb#ecdf_quantiles"
DATASET_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
AP0_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"

QUANTILE_DEFINITION = "linear interpolation with h=(n-1)*p"
TAIL_EXTRAPOLATION = "FORBIDDEN"
METRIC_PROBABILITIES = {
    "tick_count": (0.5, 0.9, 0.99),
    "minute_range": (0.5, 0.9, 0.95, 0.99),
    "spread_mean": (0.5, 0.9, 0.95, 0.99),
}
POPULATION_SEMANTICS = {
    "observational_unit": "ONE_ADMITTED_AP0_MINUTE",
    "population_scope": "CENSUS_OF_ALL_ADMITTED_AP0_MINUTES_IN_EACH_PREDECLARED_AP1_BUCKET",
    "stochastic_sample_claim": False,
    "iid_claim": False,
    "inference_claim": False,
}
AUTHORITY_NONE = {
    "scientific": False,
    "operational": False,
    "trading": False,
    "capital": False,
}

class BindingBlocked(RuntimeError):
    pass

def _canonical_json(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise BindingBlocked("NON_CANONICAL_BINDING_VALUE") from exc

def canonical_sha256(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()

def _require(condition: bool, code: str) -> None:
    if not condition:
        raise BindingBlocked(code)

def create_m03_activation(*, result_exposed: bool = False) -> dict[str, Any]:
    try:
        return create_activation_record(
            claim_definition_ref="claim:" + CLAIM_SCOPE_ID,
            failure_mode_ref="EMPIRICAL_DISTRIBUTION_QUANTILE_DEFINITION_AND_PROCEDURE_IDENTITY",
            method_family_ref="M03",
            validity_scope_ref="scope:RETROSPECTIVE_DESCRIPTIVE_ONLY:NO_INFERENCE",
            assumption_set_ref="assumptions:CENSUS_NO_IID_NO_INFERENCE",
            activation_reason="AP1 declares empirical percentile summaries for tick_count, minute_range, and per-minute spread_mean",
            activation_rule="M03 required before any empirical quantile result for the exact AP1 descriptive claim",
            parameter_selection_policy={
                "quantile_definition": QUANTILE_DEFINITION,
                "tail_extrapolation": TAIL_EXTRAPOLATION,
                "probabilities": {k: list(v) for k, v in METRIC_PROBABILITIES.items()},
                "population_semantics": POPULATION_SEMANTICS,
                "empty_bucket_rule": "NO_NUMERICAL_RESULT",
            },
            dependency_refs=[
                "SMF-01:M03",
                "SMF-02:PRE_RESULT_ACTIVATION",
                "DATA-02:" + DATA02_RECEIPT_BLOB,
                "P1-21:" + P121_RECEIPT_BLOB,
                "AP1:" + AP1_PRODUCER_BLOB,
            ],
            activation_state="ACTIVATED",
            result_exposed=result_exposed,
        )
    except ValueError as exc:
        raise BindingBlocked(str(exc)) from exc

def validate_activation(record: Mapping[str, Any]) -> dict[str, Any]:
    _require(isinstance(record, Mapping), "ACTIVATION_RECORD_REQUIRED")
    expected = create_m03_activation(result_exposed=False)
    if record.get("activation_digest") != expected["activation_digest"]:
        raise BindingBlocked("ACTIVATION_DIGEST_MISMATCH")
    _require(dict(record) == expected, "ACTIVATION_IDENTITY_MISMATCH")
    return expected

def build_execution_plan(
    *,
    activation: Mapping[str, Any],
    ap1_producer_blob: str,
    data02_receipt_blob: str,
    p121_receipt_blob: str,
    smf_core_blob: str,
    ap0_manifest_sha256: str,
    dataset_identity: str,
) -> dict[str, Any]:
    act = validate_activation(activation)
    _require(ap1_producer_blob == AP1_PRODUCER_BLOB, "AP1_PRODUCER_IDENTITY_MISMATCH")
    _require(data02_receipt_blob == DATA02_RECEIPT_BLOB, "DATA02_RECEIPT_IDENTITY_MISMATCH")
    _require(p121_receipt_blob == P121_RECEIPT_BLOB, "P121_RECEIPT_IDENTITY_MISMATCH")
    _require(smf_core_blob == SMF_CORE_BLOB, "SMF_CORE_IDENTITY_MISMATCH")
    _require(ap0_manifest_sha256 == AP0_MANIFEST_SHA256, "AP0_MANIFEST_IDENTITY_MISMATCH")
    _require(dataset_identity == DATASET_IDENTITY, "DATASET_IDENTITY_MISMATCH")
    body = {
        "schema": "ATDS_SMF_AP1_M03_01_EXECUTION_PLAN_V0_1",
        "status": "M03_BINDING_PLAN_READY",
        "claim_scope_id": CLAIM_SCOPE_ID,
        "companion_id": COMPANION_ID,
        "activation_digest": act["activation_digest"],
        "identities": {
            "ap1_producer_blob": AP1_PRODUCER_BLOB,
            "data02_receipt_blob": DATA02_RECEIPT_BLOB,
            "p121_receipt_blob": P121_RECEIPT_BLOB,
            "smf_core_blob": SMF_CORE_BLOB,
            "smf_reference_blob": SMF_REFERENCE_BLOB,
            "ap0_manifest_sha256": AP0_MANIFEST_SHA256,
            "dataset_identity": DATASET_IDENTITY,
        },
        "procedure_ref": METHOD_PROCEDURE_REF,
        "metric_probabilities": {k: list(v) for k, v in METRIC_PROBABILITIES.items()},
        "population_semantics": POPULATION_SEMANTICS,
        "transport_paths_excluded_from_identity": True,
        "result_minted": False,
        "authority": {
            "execution": False,
            "scientific": False,
            "operational": False,
            "trading": False,
            "capital": False,
        },
        "g05_materialized": False,
    }
    return {**body, "plan_digest": canonical_sha256(body)}

def execute_m03_observations(
    values,
    *,
    metric: str,
    bucket_id: str,
    activation: Mapping[str, Any],
) -> dict[str, Any]:
    act = validate_activation(activation)
    _require(metric in METRIC_PROBABILITIES, "UNSUPPORTED_M03_METRIC")
    _require(isinstance(bucket_id, str) and bool(bucket_id.strip()), "BUCKET_ID_REQUIRED")
    try:
        exact = ecdf_quantiles(values, probabilities=METRIC_PROBABILITIES[metric])
    except ValueError as exc:
        raise BindingBlocked(str(exc)) from exc
    compact = {
        "schema": "ATDS_SMF_AP1_M03_01_COMPACT_RESULT_EVIDENCE_V0_1",
        "claim_scope_id": CLAIM_SCOPE_ID,
        "metric": metric,
        "bucket_id": bucket_id.strip(),
        "n": exact["n"],
        "quantiles": exact["quantiles"],
        "tail_extrapolation": exact["tail_extrapolation"],
        "activation_digest": act["activation_digest"],
        "procedure_ref": METHOD_PROCEDURE_REF,
        "smf_core_blob": SMF_CORE_BLOB,
        "sorted_values_digest": canonical_sha256(exact["sorted_values"]),
        "ecdf_digest": canonical_sha256(exact["ecdf"]),
        "authority": dict(AUTHORITY_NONE),
    }
    return {**compact, "result_digest": canonical_sha256(compact)}
