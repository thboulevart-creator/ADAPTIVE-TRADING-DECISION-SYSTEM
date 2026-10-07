from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping

CONTROL_ID = "SMF-AP1-M03-02-R1-POST-M10-DRE-01"
RESULT_SCHEMA = "ATDS_SMF_AP1_M03_02_R1_POST_M10_DRE_01_YEAR_STRATIFIED_REFERENCE_VECTOR_V0_1"
BLOCKED_SCHEMA = "ATDS_SMF_AP1_M03_02_R1_POST_M10_DRE_01_BLOCKED_RESULT_V0_1"
M03_SCHEMA = "ATDS_SMF_AP1_M03_02_REAL_EXECUTION_V0_1"
M03_STATUS = "M03_REAL_EXECUTION_COMPLETE"
BUCKET_SCHEMA = "ATDS_SMF_AP1_M03_01_COMPACT_RESULT_EVIDENCE_V0_1"
CLAIM_SCOPE_ID = "CC02_DESCRIPTIVE_MARKET_BEHAVIOR:RETROSPECTIVE_DESCRIPTIVE_ONLY:ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
CLAIM_ID = "POST_M10-DC02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES"
ESTIMAND_ID = "POST_M10-E02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES"
ANALYSIS_ID = "POST_M10-DA02-TICKCOUNT-P50-YEAR-STRATIFIED-REFERENCE-CONSTRUCTION"
CONDITIONING_SPEC_ID = "POST_M10-TCS01-TICKCOUNT-P50-UTC-YEAR-STRATA-2022-2025"
DATASET_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
AP0_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
EXPECTED_AP0_FILES = 61
EXPECTED_AP0_MINUTES = 1_709_180
REQUIRED_SOURCE_SHA256 = "7d4369cdfab545f0edb94b93ad9d1d1070e6afa35a1000376af55d9c10943a9e"
PROCEDURE_REF = "gitblob:b67d63bbbc4f93be3fe1e7327c1f1f1cc440ebeb#ecdf_quantiles"
SMF_CORE_BLOB = "b67d63bbbc4f93be3fe1e7327c1f1f1cc440ebeb"
QUANTILE_DEFINITION = "linear interpolation with h=(n-1)*p"
TAIL_RULE = "FORBIDDEN"
REQUIRED_QUANTILE_KEYS = ("0.5", "0.9", "0.99")
COMPONENTS = (
    ("R_2022", "UTC_YEAR:2022"),
    ("R_2023", "UTC_YEAR:2023"),
    ("R_2024", "UTC_YEAR:2024"),
    ("R_2025", "UTC_YEAR:2025"),
)
SOURCE_AUTHORITY = {"scientific": False, "operational": False, "trading": False, "capital": False}
OUTPUT_AUTHORITY = {"authority_created": "NONE", "trading": False, "capital": False, "oos": False, "method": False, "method_execution": False}
EPISTEMIC_STATE = {"evidence_state": "EXPOSED", "claim_provenance": "RESULT_AWARE", "same_corpus_confirmatory_status": "NON_PRISTINE", "reset_to_pristine": "FORBIDDEN"}


def _finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _canonical_m03(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _m03_result_digest(bucket: Mapping[str, Any]) -> str:
    body = dict(bucket)
    body.pop("result_digest", None)
    return "sha256:" + hashlib.sha256(_canonical_m03(body)).hexdigest()


def _valid_sha256_ref(value: Any) -> bool:
    if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
        return False
    try:
        int(value[7:], 16)
    except ValueError:
        return False
    return True


def _blocked(reasons: set[str]) -> dict[str, Any]:
    return {
        "schema": BLOCKED_SCHEMA,
        "status": "DRE01_BLOCKED",
        "control_id": CONTROL_ID,
        "reason_codes": sorted(reasons),
        "authority": dict(OUTPUT_AUTHORITY),
    }


def evaluate(payload: Any, *, observed_source_sha256: str) -> dict[str, Any]:
    reasons: set[str] = set()
    if observed_source_sha256 != REQUIRED_SOURCE_SHA256:
        reasons.add("SOURCE_SHA256_MISMATCH")
    if not isinstance(payload, Mapping):
        reasons.add("SOURCE_PAYLOAD_NOT_OBJECT")
        return _blocked(reasons)

    if payload.get("schema") != M03_SCHEMA:
        reasons.add("SOURCE_SCHEMA_MISMATCH")
    if payload.get("status") != M03_STATUS:
        reasons.add("SOURCE_STATUS_MISMATCH")

    source_data = payload.get("source_data02")
    if not isinstance(source_data, Mapping):
        reasons.add("SOURCE_DATA02_MISSING")
    else:
        if source_data.get("dataset_identity") != DATASET_IDENTITY:
            reasons.add("DATASET_IDENTITY_MISMATCH")
        if source_data.get("ap0_manifest_sha256") != AP0_MANIFEST_SHA256:
            reasons.add("AP0_MANIFEST_SHA256_MISMATCH")
        if source_data.get("expected_files") != EXPECTED_AP0_FILES:
            reasons.add("AP0_FILE_COUNT_MISMATCH")
        if source_data.get("minute_rows") != EXPECTED_AP0_MINUTES:
            reasons.add("AP0_MINUTE_COUNT_MISMATCH")

    method = payload.get("method")
    if not isinstance(method, Mapping):
        reasons.add("SOURCE_METHOD_MISSING")
    else:
        if method.get("procedure_ref") != PROCEDURE_REF:
            reasons.add("M03_PROCEDURE_REF_MISMATCH")
        if method.get("core_blob") != SMF_CORE_BLOB:
            reasons.add("M03_CORE_BLOB_MISMATCH")
        if method.get("tail_extrapolation") != TAIL_RULE:
            reasons.add("M03_TAIL_RULE_MISMATCH")

    if payload.get("authority") != SOURCE_AUTHORITY:
        reasons.add("SOURCE_AUTHORITY_MISMATCH")
    if payload.get("result_semantics") != "M03_METHOD_EXECUTION_RESULT_ONLY":
        reasons.add("SOURCE_RESULT_SEMANTICS_MISMATCH")

    bucket_evidence = payload.get("bucket_evidence")
    if not isinstance(bucket_evidence, Mapping):
        reasons.add("BUCKET_EVIDENCE_MISSING")
        return _blocked(reasons)

    extracted: list[dict[str, Any]] = []
    for component_id, bucket_id in COMPONENTS:
        bucket_group = bucket_evidence.get(bucket_id)
        if not isinstance(bucket_group, Mapping):
            reasons.add(f"BUCKET_MISSING:{bucket_id}")
            continue
        bucket = bucket_group.get("tick_count")
        if not isinstance(bucket, Mapping):
            reasons.add(f"TICK_COUNT_MISSING:{bucket_id}")
            continue
        if bucket.get("schema") != BUCKET_SCHEMA:
            reasons.add(f"BUCKET_SCHEMA_MISMATCH:{bucket_id}")
        if bucket.get("claim_scope_id") != CLAIM_SCOPE_ID:
            reasons.add(f"BUCKET_CLAIM_SCOPE_MISMATCH:{bucket_id}")
        if bucket.get("metric") != "tick_count":
            reasons.add(f"BUCKET_METRIC_MISMATCH:{bucket_id}")
        if bucket.get("bucket_id") != bucket_id:
            reasons.add(f"BUCKET_ID_MISMATCH:{bucket_id}")
        n = bucket.get("n")
        if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
            reasons.add(f"BUCKET_N_INVALID:{bucket_id}")
        quantiles = bucket.get("quantiles")
        if not isinstance(quantiles, Mapping):
            reasons.add(f"QUANTILES_MISSING:{bucket_id}")
            p50 = None
        else:
            if set(quantiles.keys()) != set(REQUIRED_QUANTILE_KEYS):
                reasons.add(f"QUANTILE_KEYS_MISMATCH:{bucket_id}")
            for qk in REQUIRED_QUANTILE_KEYS:
                if qk not in quantiles or not _finite_number(quantiles.get(qk)):
                    reasons.add(f"QUANTILE_VALUE_INVALID:{bucket_id}:{qk}")
            p50 = quantiles.get("0.5")
        if bucket.get("procedure_ref") != PROCEDURE_REF:
            reasons.add(f"BUCKET_PROCEDURE_REF_MISMATCH:{bucket_id}")
        if bucket.get("smf_core_blob") != SMF_CORE_BLOB:
            reasons.add(f"BUCKET_CORE_BLOB_MISMATCH:{bucket_id}")
        if bucket.get("tail_extrapolation") != TAIL_RULE:
            reasons.add(f"BUCKET_TAIL_RULE_MISMATCH:{bucket_id}")
        if not _valid_sha256_ref(bucket.get("activation_digest")):
            reasons.add(f"BUCKET_ACTIVATION_DIGEST_INVALID:{bucket_id}")
        if not _valid_sha256_ref(bucket.get("sorted_values_digest")):
            reasons.add(f"BUCKET_SORTED_VALUES_DIGEST_INVALID:{bucket_id}")
        if not _valid_sha256_ref(bucket.get("ecdf_digest")):
            reasons.add(f"BUCKET_ECDF_DIGEST_INVALID:{bucket_id}")
        if bucket.get("authority") != SOURCE_AUTHORITY:
            reasons.add(f"BUCKET_AUTHORITY_MISMATCH:{bucket_id}")
        result_digest = bucket.get("result_digest")
        if not isinstance(result_digest, str):
            reasons.add(f"BUCKET_RESULT_DIGEST_MISSING:{bucket_id}")
        else:
            try:
                expected_digest = _m03_result_digest(bucket)
            except (TypeError, ValueError):
                expected_digest = None
            if result_digest != expected_digest:
                reasons.add(f"BUCKET_RESULT_DIGEST_MISMATCH:{bucket_id}")

        extracted.append({
            "id": component_id,
            "stratum": bucket_id,
            "metric": "tick_count",
            "probability": 0.5,
            "n": n,
            "value": p50,
            "source_result_digest": result_digest,
        })

    if reasons:
        return _blocked(reasons)

    result = {
        "schema": RESULT_SCHEMA,
        "status": "DRE01_COMPLETE",
        "control_id": CONTROL_ID,
        "claim_unit": "tick_count p50",
        "claim_id": CLAIM_ID,
        "estimand_id": ESTIMAND_ID,
        "analysis_id": ANALYSIS_ID,
        "conditioning_spec_id": CONDITIONING_SPEC_ID,
        "source": {
            "m03_payload_sha256": REQUIRED_SOURCE_SHA256,
            "dataset_identity": DATASET_IDENTITY,
            "ap0_manifest_sha256": AP0_MANIFEST_SHA256,
            "procedure_ref": PROCEDURE_REF,
            "quantile_definition": QUANTILE_DEFINITION,
        },
        "components": extracted,
        "vector_order": [x[0] for x in COMPONENTS],
        "relation_between_components": "A_CONDITIONED_REFERENCE_VECTOR",
        "aggregation": "NONE",
        "epistemic_state": dict(EPISTEMIC_STATE),
        "authority": dict(OUTPUT_AUTHORITY),
        "result_semantics": "DESCRIPTIVE_YEAR_CONDITIONED_REFERENCE_VECTOR",
    }
    canonical_bytes(result)
    return result
