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
            "A0_AUTHORITY_MODULE_ABSENT_EXPECTED_RED",
            pytrace=False,
        )

    spec = importlib.util.spec_from_file_location(
        "a0_research_authority_under_test",
        MODULE_PATH,
    )

    if spec is None or spec.loader is None:
        pytest.fail(
            "A0_AUTHORITY_MODULE_UNLOADABLE_EXPECTED_RED",
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
            f"A0_AUTHORITY_SURFACE_INCOMPLETE_EXPECTED_RED:{missing}",
            pytrace=False,
        )

    assert module.CONTRACT == CONTRACT
    return module


def _field(value, name):
    if isinstance(value, dict):
        return value[name]
    return getattr(value, name)


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
        "producer_artifact": b"ATDS_A0_SYNTHETIC_PRODUCER_V0_1",
        "profile_registry": _json_bytes(registry),
        "source_profile": profile_raw,
        "normalization_policy": _json_bytes(policy),
    }


def test_red_positive_synthetic_projection():
    module = _module()
    case = _base_case()

    projection = _derive(module, case)

    assert projection is not None
    assert _field(projection, "normalized_conclusion")
    assert _field(projection, "canonical_projection_sha256")
    assert _verify(module, case, projection) is True


def test_red_registry_profile_authority_rejects_profile_hash_mismatch():
    module = _module()
    case = _base_case()

    profile = json.loads(
        case["source_profile"].decode("utf-8")
    )
    profile["accepted_producer_identity"] = "FORGED_PRODUCER"
    case["source_profile"] = _json_bytes(profile)

    assert _derive(module, case) is None


def test_red_strict_source_binding_rejects_foreign_producer():
    module = _module()
    case = _base_case()

    source = json.loads(
        case["source_artifact"].decode("utf-8")
    )
    source["producer_contract"] = "FOREIGN_PRODUCER"
    case["source_artifact"] = _json_bytes(source)

    assert _derive(module, case) is None


def test_red_closed_permission_intersection_is_exact():
    module = _module()
    case = _base_case()

    projection = _derive(module, case)

    assert projection is not None

    permissions = frozenset(
        _field(
            projection,
            "effective_usage_permissions",
        )
    )

    assert permissions == frozenset(
        {"HYPOTHESIS_INPUT"}
    )


def test_red_downstream_verification_rejects_tampered_reconstruction():
    module = _module()
    case = _base_case()

    projection = _derive(module, case)

    assert projection is not None
    assert _verify(module, case, projection) is True

    tampered = copy.deepcopy(projection)

    if isinstance(tampered, dict):
        tampered["canonical_projection_sha256"] = "0" * 64
    else:
        object.__setattr__(
            tampered,
            "canonical_projection_sha256",
            "0" * 64,
        )

    assert _verify(module, case, tampered) is False


def test_red_fail_closed_on_ambiguous_registry():
    module = _module()
    case = _base_case()

    registry = json.loads(
        case["profile_registry"].decode("utf-8")
    )

    duplicate = copy.deepcopy(registry["entries"][0])
    duplicate["profile_contract_id"] = (
        "ATDS_A0_SYNTHETIC_SOURCE_PROFILE_V0_1_DUP"
    )

    registry["entries"].append(duplicate)
    case["profile_registry"] = _json_bytes(registry)

    assert _derive(module, case) is None
