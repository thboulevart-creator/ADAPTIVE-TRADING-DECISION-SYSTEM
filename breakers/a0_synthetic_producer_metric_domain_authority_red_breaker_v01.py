from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_PATH = (
    ROOT
    / "GOVERNANCE"
    / "A0-SYNTHETIC-PRODUCER-METRIC-DOMAIN-AUTHORITY-V0.1.json"
)
TARGET_PATH = ROOT / "src" / "a0_metric_domain_authority.py"

PRODUCER = "ATDS_A0_SYNTHETIC_PRODUCER_V0_1"
SOURCE_SCHEMA = "ATDS_A0_SYNTHETIC_SCIENTIFIC_RESULT_V0_1"
METRIC = "SYNTHETIC_SCORE"


def _canonical(value) -> bytes:
    return json.dumps(
        value,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _authority_raw() -> bytes:
    return AUTHORITY_PATH.read_bytes()


def _authority_obj():
    return json.loads(_authority_raw().decode("utf-8"))


def _target():
    if not TARGET_PATH.is_file():
        pytest.fail(
            "A0_METRIC_DOMAIN_QUALIFIER_REQUIRED",
            pytrace=False,
        )
    spec = importlib.util.spec_from_file_location(
        "a0_metric_domain_authority_red_target",
        TARGET_PATH,
    )
    if spec is None or spec.loader is None:
        pytest.fail(
            "A0_METRIC_DOMAIN_QUALIFIER_UNLOADABLE",
            pytrace=False,
        )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fn = getattr(
        module,
        "validate_measurement_domain",
        None,
    )
    if not callable(fn):
        pytest.fail(
            "validate_measurement_domain_REQUIRED",
            pytrace=False,
        )
    return fn


def _validate(
    *,
    authority_raw=None,
    producer_identity=PRODUCER,
    source_schema=SOURCE_SCHEMA,
    metric_identity=METRIC,
    metric_value=1.0,
    source_profile_claim=None,
    normalization_policy_claim=None,
):
    fn = _target()
    return fn(
        authority_raw=(
            _authority_raw()
            if authority_raw is None
            else authority_raw
        ),
        producer_identity=producer_identity,
        source_schema=source_schema,
        metric_identity=metric_identity,
        metric_value=metric_value,
        source_profile_claim=source_profile_claim,
        normalization_policy_claim=normalization_policy_claim,
    )


def _mutated_authority(mutator) -> bytes:
    obj = _authority_obj()
    mutator(obj)
    return _canonical(obj)


def test_mg00_exact_frozen_authority_positive_control():
    assert _validate() is True


def test_mg01_wrong_authority_schema_rejected():
    raw = _mutated_authority(
        lambda x: x.__setitem__(
            "schema",
            "ATDS_A0_SYNTHETIC_PRODUCER_METRIC_DOMAIN_AUTHORITY_V9",
        )
    )
    assert _validate(authority_raw=raw) is False


def test_mg02_wrong_authority_version_rejected():
    raw = _mutated_authority(
        lambda x: x.__setitem__("version", "V9")
    )
    assert _validate(authority_raw=raw) is False


def test_mg03_wrong_producer_binding_rejected():
    assert _validate(
        producer_identity="ATDS_A0_OTHER_SYNTHETIC_PRODUCER"
    ) is False


def test_mg04_wrong_source_schema_binding_rejected():
    assert _validate(
        source_schema="ATDS_A0_OTHER_SYNTHETIC_RESULT_V0_1"
    ) is False


def test_mg05_one_byte_authority_mutation_rejected():
    assert _validate(
        authority_raw=_authority_raw() + b" "
    ) is False


def test_mg06_semantically_equal_byte_different_authority_rejected():
    obj = _authority_obj()
    raw = json.dumps(
        obj,
        indent=2,
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    assert raw != _authority_raw()
    assert _validate(authority_raw=raw) is False


def test_mg07_unknown_metric_synth_score_rejected():
    assert _validate(
        metric_identity="SYNTH_SCORE"
    ) is False


def test_mg08_wrong_case_metric_rejected():
    assert _validate(
        metric_identity="synthetic_score"
    ) is False


def test_mg09_version_like_metric_rejected():
    assert _validate(
        metric_identity="SYNTHETIC_SCORE_V2"
    ) is False


def test_mg10_added_second_metric_in_authority_rejected():
    def mutate(obj):
        obj["metric_identity_domain"].append("ALT_SCORE")
        obj["metric_rules"]["ALT_SCORE"] = {
            "value_semantics": "FINITE_JSON_NUMBER",
            "allow_bool": False,
            "allow_numeric_string": False,
            "minimum": None,
            "maximum": None,
        }
    assert _validate(
        authority_raw=_mutated_authority(mutate)
    ) is False


def test_mg11_alias_introduction_after_freeze_rejected():
    raw = _mutated_authority(
        lambda x: x["metric_aliases"].append("SYNTH_SCORE")
    )
    assert _validate(authority_raw=raw) is False


def test_mg12_bool_metric_value_rejected():
    assert _validate(metric_value=True) is False


def test_mg13_numeric_string_metric_value_rejected():
    assert _validate(metric_value="1.0") is False


def test_mg14_nan_metric_value_rejected():
    assert math.isnan(float("nan"))
    assert _validate(metric_value=float("nan")) is False


def test_mg15_positive_infinity_metric_value_rejected():
    assert _validate(metric_value=float("inf")) is False


def test_mg16_negative_infinity_metric_value_rejected():
    assert _validate(metric_value=float("-inf")) is False


def test_mg17_source_profile_metric_widening_rejected():
    assert _validate(
        source_profile_claim={
            "metric_identity_domain": [
                "SYNTHETIC_SCORE",
                "ALT_SCORE",
            ]
        }
    ) is False


def test_mg18_source_profile_alias_attempt_rejected():
    assert _validate(
        source_profile_claim={
            "metric_aliases": ["SYNTH_SCORE"]
        }
    ) is False


def test_mg19_global_normalization_policy_takeover_rejected():
    assert _validate(
        normalization_policy_claim={
            "metric_identity_domain": [
                "SYNTHETIC_SCORE",
                "ALT_SCORE",
            ]
        }
    ) is False


def test_mg20_permission_semantic_escape_rejected():
    raw = _mutated_authority(
        lambda x: x.__setitem__(
            "permission_semantics",
            "HYPOTHESIS_INPUT",
        )
    )
    assert _validate(authority_raw=raw) is False


def test_mg21_scientific_normalization_escape_rejected():
    raw = _mutated_authority(
        lambda x: x.__setitem__(
            "scientific_normalization_semantics",
            "SUPPORTED",
        )
    )
    assert _validate(authority_raw=raw) is False
