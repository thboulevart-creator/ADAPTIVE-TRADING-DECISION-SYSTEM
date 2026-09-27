from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]

MODULE_PATH = Path(
    os.environ.get(
        "A0_AUTHORITY_MODULE_PATH",
        str(ROOT / "src/a0_research_authority.py"),
    )
)

CONTRACT = "ATDS_A0_RESEARCH_FINDINGS_AUTHORITY_INTERPRETATION_V0_3"


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _json_bytes(value) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _module():
    if not MODULE_PATH.is_file():
        pytest.fail(
            "A0_AUTHORITY_MODULE_REQUIRED",
            pytrace=False,
        )

    spec = importlib.util.spec_from_file_location(
        "a0_research_authority_adversarial_target",
        MODULE_PATH,
    )

    if spec is None or spec.loader is None:
        pytest.fail(
            "A0_AUTHORITY_MODULE_UNLOADABLE",
            pytrace=False,
        )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    required = (
        "CONTRACT",
        "derive_authoritative_projection",
        "verify_authoritative_projection",
    )

    missing = [
        name
        for name in required
        if not hasattr(module, name)
    ]

    if missing:
        pytest.fail(
            f"A0_AUTHORITY_SURFACE_INCOMPLETE:{missing}",
            pytrace=False,
        )

    assert module.CONTRACT == CONTRACT
    return module


def _derive(module, case):
    try:
        return module.derive_authoritative_projection(
            copy.deepcopy(case)
        )
    except (TypeError, ValueError, KeyError):
        return None


def _verify(module, case, projection):
    try:
        return bool(
            module.verify_authoritative_projection(
                copy.deepcopy(case),
                copy.deepcopy(projection),
            )
        )
    except (TypeError, ValueError, KeyError):
        return False


def _field(value, name):
    if isinstance(value, dict):
        return value[name]
    return getattr(value, name)


def _decode(case, key):
    return json.loads(
        case[key].decode("utf-8")
    )


def _base_case():
    source = {
        "schema": "ATDS_A0_SYNTHETIC_SCIENTIFIC_RESULT_V0_1",
        "producer_contract": "ATDS_A0_SYNTHETIC_PRODUCER_V0_1",
        "data_class": "SYNTHETIC_ONLY",
        "confirmatory_claim_status": "NOT_CONFIRMATORY",
        "research_class": "N0_EXPLORATORY_SYNTHETIC",
        "evidence_level": "N0",
        "source_promotion_limit": "HYPOTHESIS_ONLY",
        "findings": [
            {
                "id": "H1",
                "raw_status": "SUPPORTED_N0",
            },
            {
                "id": "H2",
                "raw_status": "REFUTED_N0",
            },
            {
                "id": "H3",
                "raw_status": "NOT_INTERPRETABLE",
            },
        ],
    }

    preregistration = {
        "schema": "ATDS_A0_SYNTHETIC_PREREGISTRATION_V0_1",
        "expected_family": ["H1", "H2", "H3"],
    }

    profile = {
        "contract_id": "ATDS_A0_SYNTHETIC_SOURCE_PROFILE_V0_1",
        "accepted_source_schema": source["schema"],
        "accepted_producer_identity": source["producer_contract"],
        "expected_family_source": "preregistration.expected_family",
        "profile_restriction_permissions": ["HYPOTHESIS_INPUT"],
    }
    profile_raw = _json_bytes(profile)

    registry = {
        "schema": "ATDS_A0_SOURCE_PROFILE_REGISTRY_V0_1",
        "version": "V0_1",
        "entries": [
            {
                "source_schema": source["schema"],
                "profile_contract_id": profile["contract_id"],
                "profile_sha256": _sha256(profile_raw),
                "profile_status": "ACTIVE",
                "supersedes_profile_sha256": None,
            }
        ],
    }

    policy = {
        "schema": "ATDS_A0_GLOBAL_NORMALIZATION_POLICY_V0_1",
        "permission_universe": [
            "HYPOTHESIS_INPUT",
            "AUDIT_ONLY",
            "TRACE_ONLY",
        ],
        "normalized_status_map": {
            "SUPPORTED_N0": "SUPPORTED",
            "REFUTED_N0": "REFUTED",
            "NOT_INTERPRETABLE": "NOT_INTERPRETABLE",
        },
        "permissions": {
            "evidence_level": {
                "N0": [
                    "HYPOTHESIS_INPUT",
                    "AUDIT_ONLY",
                ],
            },
            "research_class": {
                "N0_EXPLORATORY_SYNTHETIC": [
                    "HYPOTHESIS_INPUT",
                    "TRACE_ONLY",
                ],
            },
            "source_promotion_limit": {
                "HYPOTHESIS_ONLY": [
                    "HYPOTHESIS_INPUT",
                    "AUDIT_ONLY",
                    "TRACE_ONLY",
                ],
            },
            "data_class": {
                "SYNTHETIC_ONLY": [
                    "HYPOTHESIS_INPUT",
                    "TRACE_ONLY",
                ],
                "REAL": [
                    "HYPOTHESIS_INPUT",
                    "TRACE_ONLY",
                ],
            },
            "confirmatory_claim": {
                "NOT_CONFIRMATORY": [
                    "HYPOTHESIS_INPUT",
                    "AUDIT_ONLY",
                ],
                "NOT_ESTABLISHED": [
                    "HYPOTHESIS_INPUT",
                    "AUDIT_ONLY",
                ],
            },
        },
    }

    return {
        "source_artifact": _json_bytes(source),
        "preregistration": _json_bytes(preregistration),
        "producer_artifact":
            b"ATDS_A0_SYNTHETIC_PRODUCER_V0_1",
        "profile_registry": _json_bytes(registry),
        "source_profile": profile_raw,
        "normalization_policy": _json_bytes(policy),
    }


# -----------------------------------------------------------------
# STRICT PARSING / COERCION
# -----------------------------------------------------------------


def test_ab01_duplicate_json_key_rejected():
    module = _module()
    case = _base_case()

    case["source_artifact"] = (
        b'{"schema":"ATDS_A0_SYNTHETIC_SCIENTIFIC_RESULT_V0_1",'
        b'"schema":"DUPLICATE","producer_contract":'
        b'"ATDS_A0_SYNTHETIC_PRODUCER_V0_1"}'
    )

    assert _derive(module, case) is None


def test_ab02_non_finite_json_number_rejected():
    module = _module()
    case = _base_case()

    source = _decode(case, "source_artifact")
    source["illegal_numeric"] = float("nan")

    case["source_artifact"] = json.dumps(
        source,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=True,
    ).encode("utf-8")

    assert _derive(module, case) is None


def test_ab03_bool_sample_size_rejected_not_ignored():
    module = _module()
    case = _base_case()

    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"] = {
        "metric": "SYNTHETIC_SCORE",
        "value": 1.0,
        "sample_size": True,
    }
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_ab04_numeric_string_sample_size_rejected_not_coerced_or_ignored():
    module = _module()
    case = _base_case()

    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"] = {
        "metric": "SYNTHETIC_SCORE",
        "value": 1.0,
        "sample_size": "100",
    }
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


# -----------------------------------------------------------------
# COMPLETENESS / CHERRY-PICKING
# -----------------------------------------------------------------


def test_ab05_missing_expected_finding_rejected():
    module = _module()
    case = _base_case()

    source = _decode(case, "source_artifact")
    source["findings"] = [
        finding
        for finding in source["findings"]
        if finding["id"] != "H2"
    ]
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_ab06_foreign_finding_rejected():
    module = _module()
    case = _base_case()

    source = _decode(case, "source_artifact")
    source["findings"].append(
        {
            "id": "H_FOREIGN",
            "raw_status": "SUPPORTED_N0",
        }
    )
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_ab07_duplicate_finding_rejected():
    module = _module()
    case = _base_case()

    source = _decode(case, "source_artifact")
    source["findings"].append(
        copy.deepcopy(source["findings"][0])
    )
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_ab08_forged_preregistration_cannot_hide_refuted_member():
    module = _module()
    case = _base_case()

    source = _decode(case, "source_artifact")
    source["findings"] = [
        finding
        for finding in source["findings"]
        if finding["id"] != "H2"
    ]
    case["source_artifact"] = _json_bytes(source)

    prereg = _decode(case, "preregistration")
    prereg["expected_family"] = ["H1", "H3"]
    case["preregistration"] = _json_bytes(prereg)

    assert _derive(module, case) is None


# -----------------------------------------------------------------
# MISSING / UNKNOWN PERMISSION AUTHORITIES
# -----------------------------------------------------------------


def test_ab09_unknown_permission_token_rejected():
    module = _module()
    case = _base_case()

    policy = _decode(case, "normalization_policy")
    policy["permissions"]["evidence_level"]["N0"].append(
        "UNKNOWN_PERMISSION"
    )
    case["normalization_policy"] = _json_bytes(policy)

    assert _derive(module, case) is None


def test_ab10_undetermined_evidence_level_contributes_empty_set():
    module = _module()
    case = _base_case()

    source = _decode(case, "source_artifact")
    del source["evidence_level"]
    case["source_artifact"] = _json_bytes(source)

    policy = _decode(case, "normalization_policy")
    policy["permissions"]["evidence_level"][
        "UNDETERMINED"
    ] = ["HYPOTHESIS_INPUT"]
    case["normalization_policy"] = _json_bytes(policy)

    projection = _derive(module, case)

    assert projection is not None
    assert (
        set(
            _field(
                projection,
                "effective_usage_permissions",
            )
        )
        == set()
    )


def test_ab11_unrepresented_promotion_limit_contributes_empty_set():
    module = _module()
    case = _base_case()

    source = _decode(case, "source_artifact")
    del source["source_promotion_limit"]
    case["source_artifact"] = _json_bytes(source)

    policy = _decode(case, "normalization_policy")
    policy["permissions"]["source_promotion_limit"][
        "NOT_REPRESENTED"
    ] = ["HYPOTHESIS_INPUT"]
    case["normalization_policy"] = _json_bytes(policy)

    projection = _derive(module, case)

    assert projection is not None
    assert (
        set(
            _field(
                projection,
                "effective_usage_permissions",
            )
        )
        == set()
    )


def test_ab12_missing_permission_dimension_fails_closed_to_empty():
    module = _module()
    case = _base_case()

    policy = _decode(case, "normalization_policy")
    del policy["permissions"]["confirmatory_claim"]
    case["normalization_policy"] = _json_bytes(policy)

    projection = _derive(module, case)

    assert projection is not None
    assert (
        set(
            _field(
                projection,
                "effective_usage_permissions",
            )
        )
        == set()
    )


# -----------------------------------------------------------------
# EPISTEMIC LAUNDERING
# -----------------------------------------------------------------


def test_ab13_synthetic_confirmed_cannot_normalize_to_supported():
    module = _module()
    case = _base_case()

    source = _decode(case, "source_artifact")
    source["findings"][0]["raw_status"] = "CONFIRMED"
    source["data_class"] = "SYNTHETIC_ONLY"
    source["confirmatory_claim_status"] = "NOT_CONFIRMATORY"
    case["source_artifact"] = _json_bytes(source)

    policy = _decode(case, "normalization_policy")
    policy["normalized_status_map"]["CONFIRMED"] = "SUPPORTED"
    case["normalization_policy"] = _json_bytes(policy)

    projection = _derive(module, case)

    assert projection is not None
    assert (
        _field(
            projection,
            "normalized_conclusion",
        )["H1"]
        == "NO_SCIENTIFIC_CLAIM"
    )


def test_ab14_real_but_not_established_confirmed_cannot_be_supported():
    module = _module()
    case = _base_case()

    source = _decode(case, "source_artifact")
    source["findings"][0]["raw_status"] = "CONFIRMED"
    source["data_class"] = "REAL"
    source["confirmatory_claim_status"] = "NOT_ESTABLISHED"
    case["source_artifact"] = _json_bytes(source)

    policy = _decode(case, "normalization_policy")
    policy["normalized_status_map"]["CONFIRMED"] = "SUPPORTED"
    case["normalization_policy"] = _json_bytes(policy)

    projection = _derive(module, case)

    assert projection is not None
    assert (
        _field(
            projection,
            "normalized_conclusion",
        )["H1"]
        == "NO_SCIENTIFIC_CLAIM"
    )


# -----------------------------------------------------------------
# NATIVE-STATUS / AUTHORITY BINDING
# -----------------------------------------------------------------


def test_ab15_foreign_normalization_policy_identity_rejected():
    module = _module()
    case = _base_case()

    policy = _decode(case, "normalization_policy")
    policy["schema"] = "FOREIGN_NORMALIZATION_POLICY"
    case["normalization_policy"] = _json_bytes(policy)

    assert _derive(module, case) is None


def test_ab16_coforged_registry_and_profile_cannot_create_new_authority():
    module = _module()
    case = _base_case()

    profile = _decode(case, "source_profile")
    profile["contract_id"] = (
        "ATDS_A0_SYNTHETIC_SOURCE_PROFILE_FORGED"
    )
    profile_raw = _json_bytes(profile)
    case["source_profile"] = profile_raw

    registry = _decode(case, "profile_registry")
    registry["entries"][0]["profile_contract_id"] = (
        profile["contract_id"]
    )
    registry["entries"][0]["profile_sha256"] = _sha256(
        profile_raw
    )
    case["profile_registry"] = _json_bytes(registry)

    assert _derive(module, case) is None


# -----------------------------------------------------------------
# CANONICAL RECONSTRUCTION / TAMPERING
# -----------------------------------------------------------------


def test_ab17_derivation_is_deterministic():
    module = _module()
    case = _base_case()

    first = _derive(module, case)
    second = _derive(module, case)

    assert first is not None
    assert second is not None
    assert first == second

    assert (
        _field(first, "canonical_projection_sha256")
        == _field(
            second,
            "canonical_projection_sha256",
        )
    )


def test_ab18_foreign_inputs_cannot_verify_existing_projection():
    module = _module()
    case = _base_case()

    projection = _derive(module, case)
    assert projection is not None
    assert _verify(module, case, projection) is True

    foreign_case = copy.deepcopy(case)
    source = _decode(
        foreign_case,
        "source_artifact",
    )
    source["research_class"] = "FOREIGN_CLASS"
    foreign_case["source_artifact"] = _json_bytes(
        source
    )

    assert (
        _verify(
            module,
            foreign_case,
            projection,
        )
        is False
    )
