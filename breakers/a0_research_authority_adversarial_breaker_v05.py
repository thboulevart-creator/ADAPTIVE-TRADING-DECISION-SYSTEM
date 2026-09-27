from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
V04_PATH = (
    ROOT
    / "breakers"
    / "a0_research_authority_adversarial_breaker_v04.py"
)
MODULE_PATH = Path(
    os.environ.get(
        "A0_AUTHORITY_MODULE_PATH",
        str(ROOT / "src/a0_research_authority.py"),
    )
)

CONTRACT = "ATDS_A0_RESEARCH_FINDINGS_AUTHORITY_INTERPRETATION_V0_3"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )
    if spec is None or spec.loader is None:
        pytest.fail(
            f"A0_SUPPORT_UNLOADABLE:{path}",
            pytrace=False,
        )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _support():
    if not V04_PATH.is_file():
        pytest.fail(
            "A0_V04_SUPPORT_REQUIRED",
            pytrace=False,
        )
    return _load(
        V04_PATH,
        "a0_research_authority_v05_support",
    )


def _module():
    if not MODULE_PATH.is_file():
        pytest.fail(
            "A0_AUTHORITY_MODULE_REQUIRED",
            pytrace=False,
        )
    module = _load(
        MODULE_PATH,
        "a0_research_authority_adversarial_v05_target",
    )
    assert module.CONTRACT == CONTRACT
    return module


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _json_bytes(value) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _canonical_projection_hash(value: dict) -> str:
    payload = copy.deepcopy(value)
    payload.pop(
        "canonical_projection_sha256",
        None,
    )
    raw = _json_bytes(payload)
    return _sha256(raw)


def _base_case():
    return _support()._base_case()


def _rich_case():
    return _support()._rich_case()


def _decode(case, key):
    return json.loads(
        case[key].decode("utf-8")
    )


def _derive(module, case):
    try:
        return module.derive_authoritative_projection(
            copy.deepcopy(case)
        )
    except (TypeError, ValueError, KeyError):
        return None


def _verify(module, case, projection):
    try:
        return module.verify_authoritative_projection(
            copy.deepcopy(case),
            copy.deepcopy(projection),
        )
    except (TypeError, ValueError, KeyError):
        return False


# -----------------------------------------------------------------
# DIAGNOSTIC -> PRIMARY PROMOTION
# -----------------------------------------------------------------


def test_af01_caller_measurement_fold_promotion_cannot_replace_native_binding():
    module = _module()
    case = _rich_case()
    case["caller_measurement_override"] = {
        "H3": {
            "metric": "SYNTHETIC_SCORE",
            "value": 999.0,
            "sample_size": 100,
            "fold_id": "F_PRIMARY",
        }
    }

    projection = _derive(module, case)

    assert projection is not None
    assert (
        projection["measurement_references"]["H3"]["fold_id"]
        == "F_DIAGNOSTIC"
    )


def test_af02_recomputed_hash_cannot_promote_diagnostic_fold_role():
    module = _module()
    case = _rich_case()
    projection = _derive(module, case)

    assert projection is not None

    tampered = copy.deepcopy(projection)
    tampered["fold_roles"]["F_DIAGNOSTIC"] = "PRIMARY"
    tampered["canonical_projection_sha256"] = (
        _canonical_projection_hash(tampered)
    )

    assert _verify(module, case, tampered) is False


def test_af03_recomputed_hash_cannot_rebind_diagnostic_measurement_primary():
    module = _module()
    case = _rich_case()
    projection = _derive(module, case)

    assert projection is not None

    tampered = copy.deepcopy(projection)
    tampered[
        "measurement_references"
    ]["H3"]["fold_id"] = "F_PRIMARY"
    tampered["canonical_projection_sha256"] = (
        _canonical_projection_hash(tampered)
    )

    assert _verify(module, case, tampered) is False


# -----------------------------------------------------------------
# SOURCE-SPECIFIC METRIC DOMAIN
# -----------------------------------------------------------------


def test_af04_foreign_metric_identity_rejected_for_admitted_synthetic_producer():
    module = _module()
    case = _rich_case()

    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"]["metric"] = (
        "FOREIGN_METRIC"
    )
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_af05_empty_metric_identity_rejected():
    module = _module()
    case = _rich_case()

    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"]["metric"] = ""
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


# -----------------------------------------------------------------
# PERMISSION REMOVAL / REAPPEARANCE / SUPPORTED SEPARATION
# -----------------------------------------------------------------


def test_af06_removed_permission_in_governed_table_cannot_reappear():
    module = _module()
    case = _base_case()

    policy = _decode(
        case,
        "normalization_policy",
    )
    policy["permissions"]["evidence_level"]["N0"] = [
        "AUDIT_ONLY"
    ]
    case["normalization_policy"] = _json_bytes(policy)

    assert _derive(module, case) is None


def test_af07_missing_governed_permission_dimension_stays_empty():
    module = _module()
    case = _base_case()

    policy = _decode(
        case,
        "normalization_policy",
    )
    policy["permissions"].pop(
        "research_class"
    )
    case["normalization_policy"] = _json_bytes(policy)

    projection = _derive(module, case)

    assert projection is not None
    assert projection["effective_usage_permissions"] == []


def test_af08_caller_requested_permission_cannot_reappear_after_missing_source():
    module = _module()
    case = _base_case()

    policy = _decode(
        case,
        "normalization_policy",
    )
    policy["permissions"].pop(
        "research_class"
    )
    case["normalization_policy"] = _json_bytes(policy)
    case["caller_requested_permissions"] = [
        "HYPOTHESIS_INPUT",
        "AUDIT_ONLY",
        "TRACE_ONLY",
    ]

    projection = _derive(module, case)

    assert projection is not None
    assert projection["effective_usage_permissions"] == []


def test_af09_supported_conclusion_does_not_auto_add_permission():
    module = _module()
    case = _base_case()

    source = _decode(case, "source_artifact")
    source.pop("evidence_level")
    case["source_artifact"] = _json_bytes(source)
    case["caller_requested_permissions"] = [
        "HYPOTHESIS_INPUT"
    ]

    projection = _derive(module, case)

    assert projection is not None
    assert (
        projection["normalized_conclusion"]["H1"]
        == "SUPPORTED"
    )
    assert projection["effective_usage_permissions"] == []


def test_af10_profile_permission_addition_excluded_by_other_sets_creates_no_authority():
    module = _module()
    case = _base_case()

    profile = _decode(case, "source_profile")
    profile["profile_restriction_permissions"] = [
        "HYPOTHESIS_INPUT",
        "AUDIT_ONLY",
    ]
    profile_raw = _json_bytes(profile)
    case["source_profile"] = profile_raw

    registry = _decode(case, "profile_registry")
    registry["entries"][0]["profile_sha256"] = _sha256(
        profile_raw
    )
    case["profile_registry"] = _json_bytes(registry)

    assert _derive(module, case) is None


# -----------------------------------------------------------------
# STATUS / EPISTEMIC LAUNDERING REMAINDERS
# -----------------------------------------------------------------


def test_af11_refuted_projection_cannot_be_reconstructed_supported():
    module = _module()
    case = _base_case()
    projection = _derive(module, case)

    assert projection is not None

    tampered = copy.deepcopy(projection)
    tampered["normalized_conclusion"]["H2"] = "SUPPORTED"
    tampered["canonical_projection_sha256"] = (
        _canonical_projection_hash(tampered)
    )

    assert _verify(module, case, tampered) is False


def test_af12_not_interpretable_projection_cannot_be_reconstructed_supported():
    module = _module()
    case = _base_case()
    projection = _derive(module, case)

    assert projection is not None

    tampered = copy.deepcopy(projection)
    tampered["normalized_conclusion"]["H3"] = "SUPPORTED"
    tampered["canonical_projection_sha256"] = (
        _canonical_projection_hash(tampered)
    )

    assert _verify(module, case, tampered) is False


def test_af13_no_scientific_claim_cannot_be_reconstructed_supported():
    module = _module()
    case = _base_case()

    source = _decode(case, "source_artifact")
    source["data_class"] = "REAL"
    source["confirmatory_claim_status"] = (
        "NOT_ESTABLISHED"
    )
    source["findings"][0]["raw_status"] = "CONFIRMED"
    case["source_artifact"] = _json_bytes(source)

    policy = _decode(
        case,
        "normalization_policy",
    )
    policy["normalized_status_map"]["CONFIRMED"] = "SUPPORTED"
    case["normalization_policy"] = _json_bytes(policy)

    projection = _derive(module, case)

    assert projection is not None
    assert (
        projection["normalized_conclusion"]["H1"]
        == "NO_SCIENTIFIC_CLAIM"
    )

    tampered = copy.deepcopy(projection)
    tampered["normalized_conclusion"]["H1"] = "SUPPORTED"
    tampered["canonical_projection_sha256"] = (
        _canonical_projection_hash(tampered)
    )

    assert _verify(module, case, tampered) is False


def test_af14_n0_evidence_cannot_be_erased_in_reconstruction():
    module = _module()
    case = _base_case()
    projection = _derive(module, case)

    assert projection is not None
    assert projection["evidence_level"] == "N0"

    tampered = copy.deepcopy(projection)
    tampered["evidence_level"] = "N4"
    tampered["canonical_projection_sha256"] = (
        _canonical_projection_hash(tampered)
    )

    assert _verify(module, case, tampered) is False


def test_af15_n0_research_class_cannot_be_erased_in_reconstruction():
    module = _module()
    case = _base_case()
    projection = _derive(module, case)

    assert projection is not None

    tampered = copy.deepcopy(projection)
    tampered["research_class"] = "N4_CONFIRMATORY"
    tampered["canonical_projection_sha256"] = (
        _canonical_projection_hash(tampered)
    )

    assert _verify(module, case, tampered) is False


def test_af16_synthetic_data_class_cannot_be_erased_in_reconstruction():
    module = _module()
    case = _base_case()
    projection = _derive(module, case)

    assert projection is not None

    tampered = copy.deepcopy(projection)
    tampered["data_class"] = "REAL"
    tampered["canonical_projection_sha256"] = (
        _canonical_projection_hash(tampered)
    )

    assert _verify(module, case, tampered) is False


# -----------------------------------------------------------------
# APPLICABILITY / LINEAGE RECONSTRUCTION
# -----------------------------------------------------------------


def test_af17_derived_from_cannot_be_erased_in_reconstruction():
    module = _module()
    case = _rich_case()
    projection = _derive(module, case)

    assert projection is not None

    tampered = copy.deepcopy(projection)
    tampered["lineage"] = []
    tampered["canonical_projection_sha256"] = (
        _canonical_projection_hash(tampered)
    )

    assert _verify(module, case, tampered) is False


def test_af18_shared_corpus_cannot_be_erased_in_reconstruction():
    module = _module()
    case = _rich_case()
    projection = _derive(module, case)

    assert projection is not None

    tampered = copy.deepcopy(projection)
    tampered["shared_corpus_identity"] = None
    tampered["canonical_projection_sha256"] = (
        _canonical_projection_hash(tampered)
    )

    assert _verify(module, case, tampered) is False


def test_af19_applicability_horizon_cannot_be_widened_in_reconstruction():
    module = _module()
    case = _rich_case()
    projection = _derive(module, case)

    assert projection is not None

    tampered = copy.deepcopy(projection)
    tampered[
        "applicability_domain"
    ]["primary_horizon"] = "ALL_HORIZONS"
    tampered["canonical_projection_sha256"] = (
        _canonical_projection_hash(tampered)
    )

    assert _verify(module, case, tampered) is False


# -----------------------------------------------------------------
# SEMANTIC ESCAPE / AUTHORITY IDENTITY REMAINDERS
# -----------------------------------------------------------------


def test_af20_sell_hold_and_positive_authorization_fields_create_no_authority():
    module = _module()
    case = _base_case()
    expected = _derive(module, case)

    assert expected is not None

    case["decision"] = "SELL"
    case["alternate_decision"] = "HOLD"
    case["p1_1_positive_authorization"] = True
    case["knowledge_promotion"] = "DURABLE"

    actual = _derive(module, case)

    assert actual is not None
    assert actual == expected
    assert "SELL" not in actual["effective_usage_permissions"]
    assert "HOLD" not in actual["effective_usage_permissions"]


def test_af21_unknown_source_schema_rejected():
    module = _module()
    case = _base_case()

    source = _decode(case, "source_artifact")
    source["schema"] = "ATDS_A0_UNKNOWN_RESULT_V9"
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_af22_cross_producer_profile_rejected_even_when_registry_rehashed():
    module = _module()
    case = _base_case()

    profile = _decode(case, "source_profile")
    profile["accepted_producer_identity"] = (
        "FOREIGN_PRODUCER"
    )
    profile_raw = _json_bytes(profile)
    case["source_profile"] = profile_raw

    registry = _decode(case, "profile_registry")
    registry["entries"][0]["profile_sha256"] = _sha256(
        profile_raw
    )
    case["profile_registry"] = _json_bytes(registry)

    assert _derive(module, case) is None
