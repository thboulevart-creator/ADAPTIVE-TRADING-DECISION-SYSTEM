from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping

CONTROL = "SMF-AP1-M03-02-R1-POST-M10-DRE-01"
SUCCESS_SCHEMA = "ATDS_SMF_AP1_M03_02_R1_POST_M10_DRE_01_YEAR_STRATIFIED_REFERENCE_VECTOR_V0_1"
FAIL_SCHEMA = "ATDS_SMF_AP1_M03_02_R1_POST_M10_DRE_01_BLOCKED_RESULT_V0_1"
M03_SCHEMA = "ATDS_SMF_AP1_M03_02_REAL_EXECUTION_V0_1"
BUCKET_SCHEMA = "ATDS_SMF_AP1_M03_01_COMPACT_RESULT_EVIDENCE_V0_1"
CLAIM_SCOPE = "CC02_DESCRIPTIVE_MARKET_BEHAVIOR:RETROSPECTIVE_DESCRIPTIVE_ONLY:ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
EXPECTED_HASH = "7d4369cdfab545f0edb94b93ad9d1d1070e6afa35a1000376af55d9c10943a9e"
DATASET = "USTECH_PROFILE_MINUTE_CORE_V0_1"
MANIFEST = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
PROC = "gitblob:b67d63bbbc4f93be3fe1e7327c1f1f1cc440ebeb#ecdf_quantiles"
CORE = "b67d63bbbc4f93be3fe1e7327c1f1f1cc440ebeb"
SOURCE_AUTH = {"scientific": False, "operational": False, "trading": False, "capital": False}
OUT_AUTH = {"authority_created": "NONE", "trading": False, "capital": False, "oos": False, "method": False, "method_execution": False}
YEARS = ((2022, "R_2022"), (2023, "R_2023"), (2024, "R_2024"), (2025, "R_2025"))


def canonical_bytes(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def canonical_sha256(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _is_number(x):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return False
    return math.isfinite(float(x))


def _looks_digest(x):
    if not isinstance(x, str) or len(x) != 71 or x[:7] != "sha256:":
        return False
    try:
        bytes.fromhex(x[7:])
    except ValueError:
        return False
    return True


def _bucket_digest(record):
    d = {k: v for k, v in record.items() if k != "result_digest"}
    encoded = json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _blocked(codes):
    unique = sorted(set(codes))
    return {"schema": FAIL_SCHEMA, "status": "DRE01_BLOCKED", "control_id": CONTROL, "reason_codes": unique, "authority": dict(OUT_AUTH)}


def reference_evaluate(payload, *, observed_source_sha256):
    errors = []
    if observed_source_sha256 != EXPECTED_HASH:
        errors.append("SOURCE_SHA256_MISMATCH")
    if not isinstance(payload, Mapping):
        errors.append("SOURCE_PAYLOAD_NOT_OBJECT")
        return _blocked(errors)

    top_expectations = (
        ("schema", M03_SCHEMA, "SOURCE_SCHEMA_MISMATCH"),
        ("status", "M03_REAL_EXECUTION_COMPLETE", "SOURCE_STATUS_MISMATCH"),
        ("result_semantics", "M03_METHOD_EXECUTION_RESULT_ONLY", "SOURCE_RESULT_SEMANTICS_MISMATCH"),
    )
    for key, expected, code in top_expectations:
        if payload.get(key) != expected:
            errors.append(code)
    if payload.get("authority") != SOURCE_AUTH:
        errors.append("SOURCE_AUTHORITY_MISMATCH")

    data = payload.get("source_data02")
    if isinstance(data, Mapping):
        for key, expected, code in (
            ("dataset_identity", DATASET, "DATASET_IDENTITY_MISMATCH"),
            ("ap0_manifest_sha256", MANIFEST, "AP0_MANIFEST_SHA256_MISMATCH"),
            ("expected_files", 61, "AP0_FILE_COUNT_MISMATCH"),
            ("minute_rows", 1709180, "AP0_MINUTE_COUNT_MISMATCH"),
        ):
            if data.get(key) != expected:
                errors.append(code)
    else:
        errors.append("SOURCE_DATA02_MISSING")

    method = payload.get("method")
    if isinstance(method, Mapping):
        if method.get("procedure_ref") != PROC:
            errors.append("M03_PROCEDURE_REF_MISMATCH")
        if method.get("core_blob") != CORE:
            errors.append("M03_CORE_BLOB_MISMATCH")
        if method.get("tail_extrapolation") != "FORBIDDEN":
            errors.append("M03_TAIL_RULE_MISMATCH")
    else:
        errors.append("SOURCE_METHOD_MISSING")

    all_buckets = payload.get("bucket_evidence")
    if not isinstance(all_buckets, Mapping):
        errors.append("BUCKET_EVIDENCE_MISSING")
        return _blocked(errors)

    components = []
    for year, component_name in YEARS:
        label = f"UTC_YEAR:{year}"
        group = all_buckets.get(label)
        if not isinstance(group, Mapping):
            errors.append(f"BUCKET_MISSING:{label}")
            continue
        record = group.get("tick_count")
        if not isinstance(record, Mapping):
            errors.append(f"TICK_COUNT_MISSING:{label}")
            continue

        exact_fields = (
            ("schema", BUCKET_SCHEMA, "BUCKET_SCHEMA_MISMATCH"),
            ("claim_scope_id", CLAIM_SCOPE, "BUCKET_CLAIM_SCOPE_MISMATCH"),
            ("metric", "tick_count", "BUCKET_METRIC_MISMATCH"),
            ("bucket_id", label, "BUCKET_ID_MISMATCH"),
            ("procedure_ref", PROC, "BUCKET_PROCEDURE_REF_MISMATCH"),
            ("smf_core_blob", CORE, "BUCKET_CORE_BLOB_MISMATCH"),
            ("tail_extrapolation", "FORBIDDEN", "BUCKET_TAIL_RULE_MISMATCH"),
        )
        for key, expected, prefix in exact_fields:
            if record.get(key) != expected:
                errors.append(prefix + ":" + label)
        count = record.get("n")
        if isinstance(count, bool) or not isinstance(count, int) or count < 1:
            errors.append("BUCKET_N_INVALID:" + label)

        q = record.get("quantiles")
        p50 = None
        if not isinstance(q, Mapping):
            errors.append("QUANTILES_MISSING:" + label)
        else:
            if set(q) != {"0.5", "0.9", "0.99"}:
                errors.append("QUANTILE_KEYS_MISMATCH:" + label)
            for key in ("0.5", "0.9", "0.99"):
                if key not in q or not _is_number(q.get(key)):
                    errors.append(f"QUANTILE_VALUE_INVALID:{label}:{key}")
            p50 = q.get("0.5")

        for field, prefix in (
            ("activation_digest", "BUCKET_ACTIVATION_DIGEST_INVALID"),
            ("sorted_values_digest", "BUCKET_SORTED_VALUES_DIGEST_INVALID"),
            ("ecdf_digest", "BUCKET_ECDF_DIGEST_INVALID"),
        ):
            if not _looks_digest(record.get(field)):
                errors.append(prefix + ":" + label)
        if record.get("authority") != SOURCE_AUTH:
            errors.append("BUCKET_AUTHORITY_MISMATCH:" + label)
        rd = record.get("result_digest")
        if not isinstance(rd, str):
            errors.append("BUCKET_RESULT_DIGEST_MISSING:" + label)
        else:
            try:
                expected_digest = _bucket_digest(record)
            except (TypeError, ValueError):
                expected_digest = None
            if rd != expected_digest:
                errors.append("BUCKET_RESULT_DIGEST_MISMATCH:" + label)

        components.append({
            "id": component_name,
            "stratum": label,
            "metric": "tick_count",
            "probability": 0.5,
            "n": count,
            "value": p50,
            "source_result_digest": rd,
        })

    if errors:
        return _blocked(errors)

    out = {
        "schema": SUCCESS_SCHEMA,
        "status": "DRE01_COMPLETE",
        "control_id": CONTROL,
        "claim_unit": "tick_count p50",
        "claim_id": "POST_M10-DC02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES",
        "estimand_id": "POST_M10-E02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES",
        "analysis_id": "POST_M10-DA02-TICKCOUNT-P50-YEAR-STRATIFIED-REFERENCE-CONSTRUCTION",
        "conditioning_spec_id": "POST_M10-TCS01-TICKCOUNT-P50-UTC-YEAR-STRATA-2022-2025",
        "source": {
            "m03_payload_sha256": EXPECTED_HASH,
            "dataset_identity": DATASET,
            "ap0_manifest_sha256": MANIFEST,
            "procedure_ref": PROC,
            "quantile_definition": "linear interpolation with h=(n-1)*p",
        },
        "components": components,
        "vector_order": [name for _, name in YEARS],
        "relation_between_components": "A_CONDITIONED_REFERENCE_VECTOR",
        "aggregation": "NONE",
        "epistemic_state": {
            "evidence_state": "EXPOSED",
            "claim_provenance": "RESULT_AWARE",
            "same_corpus_confirmatory_status": "NON_PRISTINE",
            "reset_to_pristine": "FORBIDDEN",
        },
        "authority": dict(OUT_AUTH),
        "result_semantics": "DESCRIPTIVE_YEAR_CONDITIONED_REFERENCE_VECTOR",
    }
    canonical_bytes(out)
    return out
