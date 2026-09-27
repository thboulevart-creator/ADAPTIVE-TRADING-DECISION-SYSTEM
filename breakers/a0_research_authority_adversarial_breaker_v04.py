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


def _json_bytes(value, *, allow_nan=False) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=allow_nan,
    ).encode("utf-8")


def _canonical_projection_hash(value: dict) -> str:
    payload = copy.deepcopy(value)
    payload.pop("canonical_projection_sha256", None)
    raw = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return _sha256(raw)


def _module():
    if not MODULE_PATH.is_file():
        pytest.fail("A0_AUTHORITY_MODULE_REQUIRED", pytrace=False)

    spec = importlib.util.spec_from_file_location(
        "a0_research_authority_adversarial_v04_target",
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
# STRICT PARSING / NUMERIC SEMANTICS REMAINDERS
# -----------------------------------------------------------------


def test_ae01_positive_infinity_measurement_rejected():
    module = _module()
    case = _base_case()
    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"] = {
        "metric": "SYNTHETIC_SCORE",
        "value": float("inf"),
        "sample_size": 100,
    }
    case["source_artifact"] = _json_bytes(
        source,
        allow_nan=True,
    )

    assert _derive(module, case) is None


def test_ae02_negative_infinity_measurement_rejected():
    module = _module()
    case = _base_case()
    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"] = {
        "metric": "SYNTHETIC_SCORE",
        "value": float("-inf"),
        "sample_size": 100,
    }
    case["source_artifact"] = _json_bytes(
        source,
        allow_nan=True,
    )

    assert _derive(module, case) is None


def test_ae03_bool_measurement_value_rejected():
    module = _module()
    case = _base_case()
    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"] = {
        "metric": "SYNTHETIC_SCORE",
        "value": True,
        "sample_size": 100,
    }
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_ae04_numeric_string_measurement_value_rejected():
    module = _module()
    case = _base_case()
    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"] = {
        "metric": "SYNTHETIC_SCORE",
        "value": "1.0",
        "sample_size": 100,
    }
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_ae05_zero_sample_size_rejected():
    module = _module()
    case = _base_case()
    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"] = {
        "metric": "SYNTHETIC_SCORE",
        "value": 1.0,
        "sample_size": 0,
    }
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_ae06_negative_sample_size_rejected():
    module = _module()
    case = _base_case()
    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"] = {
        "metric": "SYNTHETIC_SCORE",
        "value": 1.0,
        "sample_size": -1,
    }
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


# -----------------------------------------------------------------
# POST-OBSERVATION PROFILE AUTHORITY
# -----------------------------------------------------------------


def test_ae07_profile_applicability_path_mutation_rejected():
    module = _module()
    case = _rich_case()

    profile = _decode(case, "source_profile")
    profile["applicability_path"] = "wider_applicability"
    profile_raw = _json_bytes(profile)
    case["source_profile"] = profile_raw

    registry = _decode(case, "profile_registry")
    registry["entries"][0]["profile_sha256"] = _sha256(
        profile_raw
    )
    case["profile_registry"] = _json_bytes(registry)

    assert _derive(module, case) is None


def test_ae08_profile_native_status_path_mutation_rejected():
    module = _module()
    case = _rich_case()

    profile = _decode(case, "source_profile")
    profile["native_status_paths"] = [
        "caller_status",
        "artifact_status",
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
# PREREGISTRATION AUTHORITY / POST-OBSERVATION CONTENT
# -----------------------------------------------------------------


def test_ae09_canonical_preregistration_extra_content_cannot_create_authority():
    module = _module()
    case = _base_case()

    prereg = _decode(case, "preregistration")
    prereg["post_observation_annotation"] = (
        "OUTCOME_SEEN"
    )
    case["preregistration"] = _json_bytes(prereg)

    assert _derive(module, case) is None


# -----------------------------------------------------------------
# CROSS-DIMENSION EPISTEMIC CONTRADICTIONS
# -----------------------------------------------------------------


def test_ae10_supported_n0_cannot_be_redeclared_as_n4_in_source():
    module = _module()
    case = _rich_case()

    source = _decode(case, "source_artifact")
    source["evidence_level"] = "N4"
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_ae11_synthetic_n0_cannot_be_redeclared_as_confirmatory_research_class():
    module = _module()
    case = _rich_case()

    source = _decode(case, "source_artifact")
    source["research_class"] = "N4_CONFIRMATORY"
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_ae12_synthetic_research_class_cannot_be_redeclared_real():
    module = _module()
    case = _rich_case()

    source = _decode(case, "source_artifact")
    source["data_class"] = "REAL"
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_ae13_synthetic_data_cannot_claim_confirmatory_established():
    module = _module()
    case = _rich_case()

    source = _decode(case, "source_artifact")
    source["confirmatory_claim_status"] = (
        "CONFIRMATORY_ESTABLISHED"
    )
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_ae14_confirmed_does_not_establish_n4():
    module = _module()
    case = _rich_case()

    source = _decode(case, "source_artifact")
    source["findings"][0]["raw_status"] = "CONFIRMED"
    source["evidence_level"] = "N4"
    case["source_artifact"] = _json_bytes(source)

    policy = _decode(case, "normalization_policy")
    policy["normalized_status_map"]["CONFIRMED"] = "SUPPORTED"
    case["normalization_policy"] = _json_bytes(policy)

    assert _derive(module, case) is None


# -----------------------------------------------------------------
# PERMISSION SEMANTICS / MONOTONICITY
# -----------------------------------------------------------------


def test_ae15_supported_conclusion_may_have_zero_permissions():
    module = _module()
    case = _base_case()

    source = _decode(case, "source_artifact")
    source.pop("evidence_level")
    case["source_artifact"] = _json_bytes(source)

    projection = _derive(module, case)

    assert projection is not None
    assert projection["normalized_conclusion"]["H1"] == "SUPPORTED"
    assert projection["effective_usage_permissions"] == []


def test_ae16_added_restriction_cannot_increase_permissions():
    module = _module()

    base = _derive(module, _base_case())
    assert base is not None

    restricted_case = _base_case()
    policy = _decode(
        restricted_case,
        "normalization_policy",
    )
    policy["permissions"].pop("confirmatory_claim")
    restricted_case["normalization_policy"] = _json_bytes(
        policy
    )

    restricted = _derive(module, restricted_case)

    assert restricted is not None
    assert set(
        restricted["effective_usage_permissions"]
    ).issubset(
        set(base["effective_usage_permissions"])
    )
    assert restricted["effective_usage_permissions"] == []


# -----------------------------------------------------------------
# RECONSTRUCTION / EXACT-BYTE SOURCE BINDING
# -----------------------------------------------------------------


def test_ae17_tampered_projection_with_recomputed_hash_still_rejected():
    module = _module()
    case = _base_case()
    projection = _derive(module, case)

    assert projection is not None

    tampered = copy.deepcopy(projection)
    tampered["normalized_conclusion"]["H1"] = "REFUTED"
    tampered["canonical_projection_sha256"] = (
        _canonical_projection_hash(tampered)
    )

    assert _verify(module, case, tampered) is False


def test_ae18_one_byte_source_change_invalidates_existing_projection():
    module = _module()
    case = _base_case()
    projection = _derive(module, case)

    assert projection is not None

    changed_case = copy.deepcopy(case)
    changed_case["source_artifact"] = (
        changed_case["source_artifact"] + b" "
    )

    assert _verify(
        module,
        changed_case,
        projection,
    ) is False


# -----------------------------------------------------------------
# FREE TEXT / CALLER PROFILE SELECTION / PRODUCER BINDING
# -----------------------------------------------------------------


def test_ae19_narrative_change_changes_only_opaque_identity_not_scientific_semantics():
    module = _module()

    first_case = _base_case()
    source = _decode(first_case, "source_artifact")
    source["findings"][0]["statement"] = "FIRST TEXT"
    first_case["source_artifact"] = _json_bytes(source)

    second_case = copy.deepcopy(first_case)
    source = _decode(second_case, "source_artifact")
    source["findings"][0]["statement"] = "SECOND TEXT"
    second_case["source_artifact"] = _json_bytes(source)

    first = _derive(module, first_case)
    second = _derive(module, second_case)

    assert first is not None
    assert second is not None
    assert (
        first["normalized_conclusion"]
        == second["normalized_conclusion"]
    )
    assert (
        first["effective_usage_permissions"]
        == second["effective_usage_permissions"]
    )
    assert (
        first["opaque_narrative_references"]
        != second["opaque_narrative_references"]
    )


def test_ae20_caller_selected_profile_has_no_authority():
    module = _module()
    case = _base_case()
    expected = _derive(module, case)

    assert expected is not None

    case["caller_selected_profile"] = {
        "contract_id": "FOREIGN_PROFILE",
        "profile_restriction_permissions": [
            "HYPOTHESIS_INPUT",
            "AUDIT_ONLY",
            "TRACE_ONLY",
        ],
    }

    actual = _derive(module, case)

    assert actual is not None
    assert actual == expected


def test_ae21_foreign_producer_artifact_rejected():
    module = _module()
    case = _base_case()
    case["producer_artifact"] = b"FOREIGN_PRODUCER"

    assert _derive(module, case) is None
