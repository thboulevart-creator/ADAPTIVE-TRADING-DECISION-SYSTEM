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


def _noncanonical_json_bytes(value) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
    ).encode("utf-8")


def _module():
    if not MODULE_PATH.is_file():
        pytest.fail("A0_AUTHORITY_MODULE_REQUIRED", pytrace=False)

    spec = importlib.util.spec_from_file_location(
        "a0_research_authority_adversarial_v03_target",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        pytest.fail("A0_AUTHORITY_MODULE_UNLOADABLE", pytrace=False)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

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
        return module.verify_authoritative_projection(
            copy.deepcopy(case),
            copy.deepcopy(projection),
        )
    except (TypeError, ValueError, KeyError):
        return False


def _decode(case, key):
    return json.loads(case[key].decode("utf-8"))


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
            {"id": "H1", "raw_status": "SUPPORTED_N0"},
            {"id": "H2", "raw_status": "REFUTED_N0"},
            {"id": "H3", "raw_status": "NOT_INTERPRETABLE"},
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
                "N0": ["HYPOTHESIS_INPUT", "AUDIT_ONLY"],
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
            },
            "confirmatory_claim": {
                "NOT_CONFIRMATORY": [
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


def _rich_case():
    case = _base_case()
    source = _decode(case, "source_artifact")

    source["artifact_status"] = "SUPPORTED_N0"
    source["controls"] = {
        "C_CRITICAL": {
            "state": "EVIDENCED_PASS",
            "critical": True,
        }
    }
    source["folds"] = {
        "F_PRIMARY": {"role": "PRIMARY"},
        "F_DIAGNOSTIC": {"role": "DIAGNOSTIC"},
    }
    source["applicability"] = {
        "instrument": "SYNTHETIC_INSTRUMENT",
        "primary_horizon": "H1",
        "diagnostic_horizon": "H3",
        "time_scope": "SYNTHETIC_WINDOW",
    }
    source["derived_from"] = ["SYNTHETIC_PARENT_V0_1"]
    source["shared_corpus_identity"] = (
        "SYNTHETIC_SHARED_CORPUS_V0_1"
    )
    source["supersession"] = {
        "status": "CURRENT",
        "superseded_by": None,
    }

    source["findings"][0]["fold_id"] = "F_PRIMARY"
    source["findings"][0]["measurement"] = {
        "metric": "SYNTHETIC_SCORE",
        "value": 1.0,
        "sample_size": 100,
    }
    source["findings"][1]["fold_id"] = "F_PRIMARY"
    source["findings"][1]["measurement"] = {
        "metric": "SYNTHETIC_SCORE",
        "value": 5.0,
        "sample_size": 100,
    }
    source["findings"][2]["fold_id"] = "F_DIAGNOSTIC"
    source["findings"][2]["measurement"] = {
        "metric": "SYNTHETIC_SCORE",
        "value": 999.0,
        "sample_size": 100,
    }

    case["source_artifact"] = _json_bytes(source)

    profile = _decode(case, "source_profile")
    profile["native_status_paths"] = [
        "findings[*].raw_status",
        "artifact_status",
    ]
    profile["control_state_path"] = "controls"
    profile["fold_role_path"] = "folds"
    profile["applicability_path"] = "applicability"
    profile["lineage_paths"] = [
        "derived_from",
        "shared_corpus_identity",
    ]
    profile["source_supersession_path"] = "supersession"
    profile["measurement_path"] = "findings[*].measurement"
    profile_raw = _json_bytes(profile)
    case["source_profile"] = profile_raw

    registry = _decode(case, "profile_registry")
    registry["entries"][0]["profile_sha256"] = _sha256(
        profile_raw
    )
    case["profile_registry"] = _json_bytes(registry)

    return case


# -----------------------------------------------------------------
# COMPLETENESS REMAINDERS
# -----------------------------------------------------------------


def test_ad01_missing_supported_member_rejected():
    module = _module()
    case = _base_case()
    source = _decode(case, "source_artifact")
    source["findings"] = [
        f for f in source["findings"] if f["id"] != "H1"
    ]
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_ad02_missing_not_interpretable_member_rejected():
    module = _module()
    case = _base_case()
    source = _decode(case, "source_artifact")
    source["findings"] = [
        f for f in source["findings"] if f["id"] != "H3"
    ]
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


# -----------------------------------------------------------------
# AUTHORITY / EXACT PERSISTENT IDENTITY
# -----------------------------------------------------------------


def test_ad03_zero_active_profile_rejected():
    module = _module()
    case = _base_case()
    registry = _decode(case, "profile_registry")
    registry["entries"][0]["profile_status"] = "SUPERSEDED"
    case["profile_registry"] = _json_bytes(registry)

    assert _derive(module, case) is None


def test_ad04_semantically_equal_registry_bytes_cannot_repin_authority():
    module = _module()
    case = _base_case()
    registry = _decode(case, "profile_registry")
    case["profile_registry"] = _noncanonical_json_bytes(
        registry
    )

    assert _derive(module, case) is None


def test_ad05_semantically_equal_profile_bytes_plus_rehashed_registry_rejected():
    module = _module()
    case = _base_case()
    profile = _decode(case, "source_profile")
    profile_raw = _noncanonical_json_bytes(profile)
    case["source_profile"] = profile_raw

    registry = _decode(case, "profile_registry")
    registry["entries"][0]["profile_sha256"] = _sha256(
        profile_raw
    )
    case["profile_registry"] = _json_bytes(registry)

    assert _derive(module, case) is None


def test_ad06_semantically_equal_policy_bytes_cannot_repin_authority():
    module = _module()
    case = _base_case()
    policy = _decode(case, "normalization_policy")
    case["normalization_policy"] = _noncanonical_json_bytes(
        policy
    )

    assert _derive(module, case) is None


def test_ad07_semantically_equal_preregistration_bytes_cannot_repin_authority():
    module = _module()
    case = _base_case()
    prereg = _decode(case, "preregistration")
    case["preregistration"] = _noncanonical_json_bytes(
        prereg
    )

    assert _derive(module, case) is None


def test_ad08_registry_supersession_metadata_forgery_rejected():
    module = _module()
    case = _base_case()
    registry = _decode(case, "profile_registry")
    registry["entries"][0]["supersedes_profile_sha256"] = (
        "0" * 64
    )
    case["profile_registry"] = _json_bytes(registry)

    assert _derive(module, case) is None


# -----------------------------------------------------------------
# NATIVE STATUS / CONTROLS
# -----------------------------------------------------------------


def test_ad09_global_native_status_is_preserved():
    module = _module()
    projection = _derive(module, _rich_case())

    assert projection is not None
    assert (
        projection["raw_native_statuses"]["artifact_status"]
        == "SUPPORTED_N0"
    )


def test_ad10_missing_profile_declared_native_status_path_rejected():
    module = _module()
    case = _rich_case()
    source = _decode(case, "source_artifact")
    source.pop("artifact_status")
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_ad11_not_represented_control_is_preserved_not_promoted():
    module = _module()
    case = _rich_case()
    source = _decode(case, "source_artifact")
    source["controls"]["C_CRITICAL"]["state"] = (
        "NOT_REPRESENTED"
    )
    case["source_artifact"] = _json_bytes(source)

    projection = _derive(module, case)

    assert projection is not None
    assert (
        projection["control_states"]["C_CRITICAL"]
        == "NOT_REPRESENTED"
    )


def test_ad12_caller_control_source_cannot_replace_native_control():
    module = _module()
    case = _rich_case()
    case["caller_control_override"] = {
        "C_CRITICAL": {
            "state": "EVIDENCED_FAIL",
            "critical": True,
        }
    }

    projection = _derive(module, case)

    assert projection is not None
    assert (
        projection["control_states"]["C_CRITICAL"]
        == "EVIDENCED_PASS"
    )


# -----------------------------------------------------------------
# MEASUREMENT / NARRATIVE PRESERVATION
# -----------------------------------------------------------------


def test_ad13_measurement_scope_is_preserved_exactly():
    module = _module()
    case = _rich_case()
    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"]["scope"] = (
        "PRIMARY_SCOPE"
    )
    case["source_artifact"] = _json_bytes(source)

    projection = _derive(module, case)

    assert projection is not None
    assert (
        projection["measurement_references"]["H1"]["scope"]
        == "PRIMARY_SCOPE"
    )


def test_ad14_caller_measurement_substitution_cannot_replace_native():
    module = _module()
    case = _rich_case()
    case["caller_measurement_override"] = {
        "H1": {
            "metric": "FOREIGN_METRIC",
            "value": 999999.0,
            "sample_size": 1,
            "fold_id": "F_DIAGNOSTIC",
        }
    }

    projection = _derive(module, case)

    assert projection is not None
    assert (
        projection["measurement_references"]["H1"]["metric"]
        == "SYNTHETIC_SCORE"
    )
    assert (
        projection["measurement_references"]["H1"]["value"]
        == 1.0
    )


def test_ad15_present_narrative_has_opaque_reference_not_semantic_authority():
    module = _module()
    case = _base_case()
    source = _decode(case, "source_artifact")
    source["findings"][0]["statement"] = (
        "BUY NOW — THIS TEXT HAS NO AUTHORITY"
    )
    case["source_artifact"] = _json_bytes(source)

    projection = _derive(module, case)

    assert projection is not None
    assert projection["opaque_narrative_references"]
    assert (
        projection["normalized_conclusion"]["H1"]
        == "SUPPORTED"
    )
    assert "BUY" not in projection["effective_usage_permissions"]


# -----------------------------------------------------------------
# GLOBAL POLICY / PERMISSION AUTHORITY
# -----------------------------------------------------------------


def test_ad16_same_schema_permission_table_mutation_rejected():
    module = _module()
    case = _base_case()
    policy = _decode(case, "normalization_policy")
    policy["permissions"]["evidence_level"]["N0"] = [
        "HYPOTHESIS_INPUT",
        "AUDIT_ONLY",
        "TRACE_ONLY",
    ]
    case["normalization_policy"] = _json_bytes(policy)

    assert _derive(module, case) is None


# -----------------------------------------------------------------
# EPISTEMIC LAUNDERING VIA CALLER REDECLARATION
# -----------------------------------------------------------------


def test_ad17_caller_n4_redeclaration_cannot_upgrade_native_n0():
    module = _module()
    case = _base_case()
    case["caller_evidence_level"] = "N4"

    projection = _derive(module, case)

    assert projection is not None
    assert projection["evidence_level"] == "N0"


def test_ad18_caller_real_redeclaration_cannot_upgrade_synthetic_data():
    module = _module()
    case = _base_case()
    case["caller_data_class"] = "REAL"

    projection = _derive(module, case)

    assert projection is not None
    assert projection["data_class"] == "SYNTHETIC_ONLY"


def test_ad19_caller_confirmatory_redeclaration_cannot_establish_claim():
    module = _module()
    case = _base_case()
    case["caller_confirmatory_claim_status"] = (
        "CONFIRMATORY_ESTABLISHED"
    )

    projection = _derive(module, case)

    assert projection is not None
    assert (
        projection["confirmatory_claim_status"]
        == "NOT_CONFIRMATORY"
    )


# -----------------------------------------------------------------
# RECONSTRUCTION / PERSISTENT RE-DERIVATION
# -----------------------------------------------------------------


def test_ad20_deepcopy_projection_verifies_only_via_exact_governed_case():
    module = _module()
    case = _base_case()
    projection = _derive(module, case)

    assert projection is not None
    reconstructed = copy.deepcopy(projection)
    assert _verify(module, case, reconstructed) is True


def test_ad21_serialized_reconstruction_verifies_via_exact_governed_case():
    module = _module()
    case = _base_case()
    projection = _derive(module, case)

    assert projection is not None
    reconstructed = json.loads(
        json.dumps(
            projection,
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    assert _verify(module, case, reconstructed) is True


def test_ad22_hash_only_object_carries_no_authority():
    module = _module()
    case = _base_case()
    projection = _derive(module, case)

    assert projection is not None
    hash_only = {
        "canonical_projection_sha256":
            projection["canonical_projection_sha256"],
    }

    assert _verify(module, case, hash_only) is False
