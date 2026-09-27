from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from contextlib import contextmanager
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
V04_PATH = ROOT / "breakers" / "a0_research_authority_adversarial_breaker_v04.py"
TARGET_PATH = ROOT / "src" / "a0_research_authority.py"
AUTHORITY_PATH = (
    ROOT
    / "GOVERNANCE"
    / "A0-SYNTHETIC-PRODUCER-METRIC-DOMAIN-AUTHORITY-V0.1.json"
)

AUTHORITY_IDENTITY = (
    "ATDS_A0_SYNTHETIC_PRODUCER_METRIC_DOMAIN_AUTHORITY_V0_1"
)
AUTHORITY_SHA256 = (
    "5813f9d75395308386b4561b13c4eae889a4565cca3289f08a30d81657057492"
)


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        pytest.fail(f"UNLOADABLE:{path}", pytrace=False)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _support():
    return _load(
        V04_PATH,
        "a0_metric_binding_red_support",
    )


def _module():
    return _load(
        TARGET_PATH,
        "a0_metric_binding_red_target",
    )


def _base_case():
    return _support()._base_case()


def _rich_case():
    return _support()._rich_case()


def _decode(case, key):
    return json.loads(case[key].decode("utf-8"))


def _json_bytes(value, *, allow_nan=False):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=allow_nan,
    ).encode("utf-8")


def _derive(case):
    module = _module()
    try:
        return module.derive_authoritative_projection(
            copy.deepcopy(case)
        )
    except (
        TypeError,
        ValueError,
        KeyError,
        OSError,
        ImportError,
    ):
        return None


def _verify(case, projection):
    module = _module()
    try:
        return module.verify_authoritative_projection(
            copy.deepcopy(case),
            copy.deepcopy(projection),
        )
    except (
        TypeError,
        ValueError,
        KeyError,
        OSError,
        ImportError,
    ):
        return False


def _canonical_projection_hash(value):
    payload = copy.deepcopy(value)
    payload.pop("canonical_projection_sha256", None)
    raw = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _assert_trace(projection, expected_validation):
    assert projection is not None
    assert (
        projection["metric_domain_authority_identity"]
        == AUTHORITY_IDENTITY
    )
    assert (
        projection["metric_domain_authority_sha256"]
        == AUTHORITY_SHA256
    )
    assert (
        projection["metric_domain_validation"]
        == expected_validation
    )


@contextmanager
def _authority_bytes_temporarily(raw):
    original = AUTHORITY_PATH.read_bytes()
    backup = AUTHORITY_PATH.with_name(
        AUTHORITY_PATH.name + ".binding-red-backup"
    )
    if backup.exists():
        backup.unlink()
    try:
        if raw is None:
            AUTHORITY_PATH.rename(backup)
        else:
            AUTHORITY_PATH.write_bytes(raw)
        yield
    finally:
        if backup.exists():
            if AUTHORITY_PATH.exists():
                AUTHORITY_PATH.unlink()
            backup.rename(AUTHORITY_PATH)
        else:
            AUTHORITY_PATH.write_bytes(original)


def test_rb00_exact_base_binding_positive_control():
    projection = _derive(_base_case())
    _assert_trace(projection, {})


def test_rb01_rich_binding_validates_every_present_measurement():
    projection = _derive(_rich_case())
    _assert_trace(
        projection,
        {"H1": "PASS", "H2": "PASS", "H3": "PASS"},
    )


def test_rb02_missing_authority_file_fails_closed():
    with _authority_bytes_temporarily(None):
        assert _derive(_base_case()) is None


def test_rb03_corrupt_authority_bytes_fail_closed():
    with _authority_bytes_temporarily(b"{}"):
        assert _derive(_base_case()) is None


def test_rb04_byte_different_authority_reconstruction_fails_closed():
    obj = json.loads(AUTHORITY_PATH.read_text(encoding="utf-8"))
    raw = json.dumps(
        obj,
        indent=2,
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    assert raw != AUTHORITY_PATH.read_bytes()
    with _authority_bytes_temporarily(raw):
        assert _derive(_base_case()) is None


def test_rb05_independent_unknown_metric_fails_closed():
    case = _rich_case()
    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"]["metric"] = "UNLISTED_SCORE"
    case["source_artifact"] = _json_bytes(source)
    assert _derive(case) is None


def test_rb06_independent_wrong_case_metric_fails_closed():
    case = _rich_case()
    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"]["metric"] = "Synthetic_Score"
    case["source_artifact"] = _json_bytes(source)
    assert _derive(case) is None


def test_rb07_large_finite_metric_has_no_invented_maximum():
    case = _rich_case()
    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"]["value"] = 1e308
    case["source_artifact"] = _json_bytes(source)
    projection = _derive(case)
    _assert_trace(
        projection,
        {"H1": "PASS", "H2": "PASS", "H3": "PASS"},
    )


def test_rb08_bool_metric_value_remains_fail_closed():
    case = _rich_case()
    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"]["value"] = True
    case["source_artifact"] = _json_bytes(source)
    assert _derive(case) is None


def test_rb09_numeric_string_metric_value_remains_fail_closed():
    case = _rich_case()
    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"]["value"] = "1.0"
    case["source_artifact"] = _json_bytes(source)
    assert _derive(case) is None


def test_rb10_caller_authority_bytes_cannot_select_authority():
    case = _base_case()
    case["metric_domain_authority"] = b"{}"
    projection = _derive(case)
    _assert_trace(projection, {})


def test_rb11_caller_authority_path_cannot_select_authority():
    case = _base_case()
    case["metric_domain_authority_path"] = "caller/alternate.json"
    projection = _derive(case)
    _assert_trace(projection, {})


def test_rb12_caller_disable_flag_cannot_bypass_invalid_metric():
    case = _rich_case()
    source = _decode(case, "source_artifact")
    source["findings"][0]["measurement"]["metric"] = "BYPASS_SCORE"
    case["source_artifact"] = _json_bytes(source)
    case["disable_metric_domain_validation"] = True
    assert _derive(case) is None


def test_rb13_source_profile_metric_domain_widening_fails_closed():
    case = _base_case()
    profile = _decode(case, "source_profile")
    profile["metric_identity_domain"] = ["SYNTHETIC_SCORE", "ALT_SCORE"]
    profile_raw = _json_bytes(profile)
    case["source_profile"] = profile_raw
    registry = _decode(case, "profile_registry")
    registry["entries"][0]["profile_sha256"] = hashlib.sha256(
        profile_raw
    ).hexdigest()
    case["profile_registry"] = _json_bytes(registry)
    assert _derive(case) is None


def test_rb14_global_policy_metric_domain_takeover_fails_closed():
    case = _base_case()
    policy = _decode(case, "normalization_policy")
    policy["metric_identity_domain"] = ["SYNTHETIC_SCORE", "ALT_SCORE"]
    case["normalization_policy"] = _json_bytes(policy)
    assert _derive(case) is None


def test_rb15_rich_carrier_authority_identity_and_hash_exact():
    projection = _derive(_rich_case())
    assert projection is not None
    assert projection["metric_domain_authority_identity"] == AUTHORITY_IDENTITY
    assert projection["metric_domain_authority_sha256"] == AUTHORITY_SHA256


def test_rb16_rich_carrier_validation_map_includes_all_measurements():
    projection = _derive(_rich_case())
    assert projection is not None
    assert projection["metric_domain_validation"] == {
        "H1": "PASS",
        "H2": "PASS",
        "H3": "PASS",
    }


def test_rb17_tampered_authority_identity_recomputed_hash_rejected():
    case = _base_case()
    projection = _derive(case)
    _assert_trace(projection, {})
    tampered = copy.deepcopy(projection)
    tampered["metric_domain_authority_identity"] = "OTHER_AUTHORITY"
    tampered["canonical_projection_sha256"] = _canonical_projection_hash(
        tampered
    )
    assert _verify(case, tampered) is False


def test_rb18_tampered_validation_map_recomputed_hash_rejected():
    case = _rich_case()
    projection = _derive(case)
    _assert_trace(
        projection,
        {"H1": "PASS", "H2": "PASS", "H3": "PASS"},
    )
    tampered = copy.deepcopy(projection)
    tampered["metric_domain_validation"]["H3"] = "SKIPPED"
    tampered["canonical_projection_sha256"] = _canonical_projection_hash(
        tampered
    )
    assert _verify(case, tampered) is False


def test_rb19_caller_validation_map_cannot_replace_derived_trace():
    case = _rich_case()
    case["metric_domain_validation"] = {
        "H1": "FAIL",
        "H2": "FAIL",
        "H3": "FAIL",
    }
    projection = _derive(case)
    _assert_trace(
        projection,
        {"H1": "PASS", "H2": "PASS", "H3": "PASS"},
    )
