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
        pytest.fail("A0_AUTHORITY_MODULE_REQUIRED", pytrace=False)

    spec = importlib.util.spec_from_file_location(
        "a0_research_authority_adversarial_v02_target",
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


def _field(projection, name):
    assert isinstance(projection, dict)
    assert name in projection
    return projection[name]


# -----------------------------------------------------------------
# REPRESENTATION / SOURCE-NATIVE SEMANTICS
# -----------------------------------------------------------------


def test_ac01_rich_governed_properties_are_represented():
    module = _module()
    case = _rich_case()

    projection = _derive(module, case)

    assert projection is not None
    assert _field(projection, "control_states") == {
        "C_CRITICAL": "EVIDENCED_PASS"
    }
    assert _field(projection, "fold_roles") == {
        "F_PRIMARY": "PRIMARY",
        "F_DIAGNOSTIC": "DIAGNOSTIC",
    }
    assert _field(projection, "applicability_domain")
    assert _field(projection, "lineage")
    assert (
        _field(projection, "shared_corpus_identity")
        == "SYNTHETIC_SHARED_CORPUS_V0_1"
    )
    assert _field(projection, "source_supersession")
    assert _field(projection, "measurement_references")


def test_ac02_critical_evidenced_fail_not_rescued_by_metric():
    module = _module()
    case = _rich_case()

    source = _decode(case, "source_artifact")
    source["controls"]["C_CRITICAL"]["state"] = "EVIDENCED_FAIL"
    source["findings"][0]["measurement"]["value"] = 999999.0
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_ac03_caller_asserted_control_never_becomes_evidenced_pass():
    module = _module()
    case = _rich_case()

    source = _decode(case, "source_artifact")
    source["controls"]["C_CRITICAL"]["state"] = "CALLER_ASSERTED"
    case["source_artifact"] = _json_bytes(source)

    projection = _derive(module, case)

    assert projection is not None
    assert (
        _field(projection, "control_states")["C_CRITICAL"]
        == "CALLER_ASSERTED"
    )


def test_ac04_unresolved_native_status_conflict_rejected():
    module = _module()
    case = _rich_case()

    source = _decode(case, "source_artifact")
    source["artifact_status"] = "REFUTED_N0"
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_ac05_downstream_status_redeclaration_cannot_replace_native():
    module = _module()
    case = _base_case()
    case["downstream_status_redeclaration"] = {
        "H2": "SUPPORTED_N0"
    }

    projection = _derive(module, case)

    assert projection is not None
    assert projection["raw_native_statuses"]["H2"] == "REFUTED_N0"
    assert projection["normalized_conclusion"]["H2"] == "REFUTED"


def test_ac06_explicitly_superseded_source_rejected():
    module = _module()
    case = _rich_case()

    source = _decode(case, "source_artifact")
    source["supersession"] = {
        "status": "SUPERSEDED",
        "superseded_by": "SYNTHETIC_RESULT_V0_2",
    }
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


# -----------------------------------------------------------------
# MEASUREMENT / FOLD / APPLICABILITY / LINEAGE
# -----------------------------------------------------------------


def test_ac07_not_interpretable_strong_metric_not_positive():
    module = _module()
    case = _rich_case()

    projection = _derive(module, case)

    assert projection is not None
    assert (
        projection["positive_evidence_consumability"]["H3"]
        is False
    )


def test_ac08_refuted_strong_metric_not_positive():
    module = _module()
    case = _rich_case()

    projection = _derive(module, case)

    assert projection is not None
    assert (
        projection["positive_evidence_consumability"]["H2"]
        is False
    )


def test_ac09_measurement_references_preserve_exact_binding():
    module = _module()
    case = _rich_case()

    projection = _derive(module, case)

    refs = _field(projection, "measurement_references")
    assert refs["H3"]["metric"] == "SYNTHETIC_SCORE"
    assert refs["H3"]["value"] == 999.0
    assert refs["H3"]["sample_size"] == 100
    assert refs["H3"]["fold_id"] == "F_DIAGNOSTIC"


def test_ac10_fold_role_comes_from_governed_fold_authority():
    module = _module()
    case = _rich_case()
    case["caller_fold_role_override"] = {
        "F_DIAGNOSTIC": "PRIMARY"
    }

    projection = _derive(module, case)

    assert projection is not None
    assert (
        _field(projection, "fold_roles")["F_DIAGNOSTIC"]
        == "DIAGNOSTIC"
    )


def test_ac11_applicability_is_preserved_and_caller_cannot_widen():
    module = _module()
    case = _rich_case()
    case["caller_applicability_override"] = {
        "primary_horizon": "ALL_HORIZONS",
    }

    projection = _derive(module, case)

    applicability = _field(
        projection,
        "applicability_domain",
    )
    assert applicability["primary_horizon"] == "H1"
    assert "ALL_HORIZONS" not in str(applicability)


def test_ac12_lineage_and_shared_corpus_cannot_disappear():
    module = _module()
    case = _rich_case()
    case["caller_lineage_override"] = {
        "derived_from": [],
        "shared_corpus_identity": None,
    }

    projection = _derive(module, case)

    assert (
        _field(projection, "lineage")
        == ["SYNTHETIC_PARENT_V0_1"]
    )
    assert (
        _field(projection, "shared_corpus_identity")
        == "SYNTHETIC_SHARED_CORPUS_V0_1"
    )


# -----------------------------------------------------------------
# PINNED AUTHORITY / POST-OBSERVATION MUTATION
# -----------------------------------------------------------------


def test_ac13_same_version_registry_content_mutation_rejected():
    module = _module()
    case = _base_case()

    registry = _decode(case, "profile_registry")
    registry["unregistered_content_change"] = "FORGED"
    case["profile_registry"] = _json_bytes(registry)

    assert _derive(module, case) is None


def test_ac14_profile_permission_widening_after_outcome_rejected():
    module = _module()
    case = _base_case()

    profile = _decode(case, "source_profile")
    profile["profile_restriction_permissions"] = [
        "HYPOTHESIS_INPUT",
        "AUDIT_ONLY",
        "TRACE_ONLY",
    ]
    profile_raw = _json_bytes(profile)
    case["source_profile"] = profile_raw

    registry = _decode(case, "profile_registry")
    registry["entries"][0]["profile_sha256"] = _sha256(
        profile_raw
    )
    case["profile_registry"] = _json_bytes(registry)

    assert _derive(module, case) is None


def test_ac15_same_schema_normalization_mapping_mutation_rejected():
    module = _module()
    case = _base_case()

    policy = _decode(case, "normalization_policy")
    policy["normalized_status_map"]["SUPPORTED_N0"] = "REFUTED"
    case["normalization_policy"] = _json_bytes(policy)

    assert _derive(module, case) is None


# -----------------------------------------------------------------
# PERMISSION UNIVERSE / SEMANTIC ESCAPE
# -----------------------------------------------------------------


def test_ac16_seventh_permission_dimension_rejected():
    module = _module()
    case = _base_case()

    policy = _decode(case, "normalization_policy")
    policy["permissions"]["caller_added_dimension"] = {
        "ALLOW": ["HYPOTHESIS_INPUT"]
    }
    case["normalization_policy"] = _json_bytes(policy)

    assert _derive(module, case) is None


def test_ac17_operational_permission_token_rejected_from_universe():
    module = _module()
    case = _base_case()

    policy = _decode(case, "normalization_policy")
    policy["permission_universe"].append("BUY")
    case["normalization_policy"] = _json_bytes(policy)

    assert _derive(module, case) is None


def test_ac18_semantic_caller_fields_create_no_authority():
    module = _module()
    case = _base_case()
    case["decision"] = "BUY"
    case["action"] = "EXECUTE"
    case["p1_1_authorization"] = True
    case["knowledge_promotion"] = "DURABLE"

    projection = _derive(module, case)

    assert projection is not None
    assert "BUY" not in projection["effective_usage_permissions"]
    assert "EXECUTE" not in projection["effective_usage_permissions"]
    assert projection["normalized_conclusion"]["H1"] == "SUPPORTED"
