from __future__ import annotations

import ast
import copy
import inspect
import json
from pathlib import Path

import pytest

import tools.trading_breaks_recovery_batch09_adjudication as adjudication_module
from tools.trading_breaks_recovery_batch09_adjudication import (
    RUNTIME_PATH,
    adjudicate_runtime,
)


def _runtime() -> dict:
    return json.loads(Path(RUNTIME_PATH).read_text(encoding="utf-8"))


def _called_function_names(source: str) -> set[str]:
    tree = ast.parse(source)
    calls: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            calls.add(node.func.id.lower())
        elif isinstance(node.func, ast.Attribute):
            calls.add(node.func.attr.lower())
    return calls


def test_authoritative_batch09_runtime_adjudicates_4_pass_1_blocked_0_fail():
    report = adjudicate_runtime(_runtime())
    assert report["verdict"] == "PASS"
    assert report["attempted"] == 5
    assert report["pass"] == 4
    assert report["blocked"] == 1
    assert report["fail"] == 0
    assert [item["verdict"] for item in report["adjudications"]] == [
        "PASS",
        "PASS",
        "PASS",
        "PASS",
        "BLOCKED",
    ]


def test_dec25_cross_date_record_74339_is_blocked_and_never_promoted():
    item = adjudicate_runtime(_runtime())["adjudications"][4]
    assert item["capture_verdict"] == "CAPTURED"
    assert item["verdict"] == "BLOCKED"
    assert item["reason"] == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert item["overlap_record_id"] == "74339"
    assert item["broker_record_id"] == "74339"
    assert "break_start_utc" not in item
    assert "fully_closed_hours_utc" not in item


def test_exact_target_positive_records_pass_with_independent_hour_projection():
    report = adjudicate_runtime(_runtime())
    expected = {
        0: ("70878", [17, 18, 19, 20, 21]),
        1: ("72887", [18, 19, 20, 21, 22]),
        2: ("72888", [19, 20, 21, 22, 23]),
        3: ("74339", [19, 20, 21, 22, 23]),
    }
    for index, (record_id, hours) in expected.items():
        item = report["adjudications"][index]
        assert item["verdict"] == "PASS"
        assert item["reason"] == "EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED"
        assert item["broker_record_id"] == record_id
        assert item["fully_closed_hours_utc"] == hours
        assert item["dom_witness_present"] is True


def test_partial_start_hours_are_not_rounded_closed():
    report = adjudicate_runtime(_runtime())
    thanksgiving_friday = report["adjudications"][2]
    christmas_eve = report["adjudications"][3]

    assert thanksgiving_friday["break_start_utc"] == "2024-11-29T18:14:59Z"
    assert thanksgiving_friday["fully_closed_hours_utc"] == [19, 20, 21, 22, 23]
    assert 18 not in thanksgiving_friday["fully_closed_hours_utc"]

    assert christmas_eve["break_start_utc"] == "2024-12-24T18:14:59Z"
    assert christmas_eve["fully_closed_hours_utc"] == [19, 20, 21, 22, 23]
    assert 18 not in christmas_eve["fully_closed_hours_utc"]


def test_frozen_membership_tampering_is_rejected():
    runtime = _runtime()
    runtime["targets"][0]["date"] = "2099-01-01"
    with pytest.raises(ValueError, match="FROZEN_MEMBERSHIP_MISMATCH"):
        adjudicate_runtime(runtime)


def test_runtime_result_reordering_is_rejected():
    runtime = _runtime()
    runtime["results"][0], runtime["results"][1] = (
        runtime["results"][1],
        runtime["results"][0],
    )
    with pytest.raises(ValueError, match="RESULT_TARGET_ORDER_OR_IDENTITY_MISMATCH"):
        adjudicate_runtime(runtime)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("workflow_run", 1),
        ("job_id", 2),
        ("artifact_id", 3),
        ("artifact_sha256", "0" * 64),
        ("probe_commit", "0" * 40),
        ("artifact_url", "https://example.invalid/tampered"),
    ],
)
def test_provenance_tampering_is_rejected(key: str, value: object):
    runtime = _runtime()
    runtime["provenance"][key] = value
    with pytest.raises(ValueError, match=f"PROVENANCE_MISMATCH:{key}"):
        adjudicate_runtime(runtime)


def test_top_level_execution_identity_tampering_is_rejected():
    runtime = _runtime()
    runtime["workflow_run"] = "1"
    with pytest.raises(ValueError, match="RUNTIME_RUN_ID_MISMATCH"):
        adjudicate_runtime(runtime)

    runtime = _runtime()
    runtime["probe_commit"] = "0" * 40
    with pytest.raises(ValueError, match="RUNTIME_PROBE_COMMIT_MISMATCH"):
        adjudicate_runtime(runtime)


def test_wrong_observed_instrument_is_rejected():
    runtime = _runtime()
    runtime["results"][0]["instrument_id_observed"] = "9999"
    with pytest.raises(ValueError, match="RESULT_OBSERVED_INSTRUMENT_MISMATCH"):
        adjudicate_runtime(runtime)


def test_wrong_requested_date_and_epoch_are_rejected():
    runtime = _runtime()
    runtime["results"][0]["requested_date"] = "2024-09-03"
    with pytest.raises(ValueError, match="RESULT_REQUESTED_DATE_MISMATCH"):
        adjudicate_runtime(runtime)

    runtime = _runtime()
    runtime["results"][0]["target_epoch_ms"] += 1
    with pytest.raises(ValueError, match="RESULT_TARGET_EPOCH_MISMATCH"):
        adjudicate_runtime(runtime)


def test_dom_network_contradiction_fails_closed():
    runtime = _runtime()
    runtime["results"][0]["dom_witness_lines"] = [
        "USATECH.IDX/USD\t02-Sep-24 16:59:59\t02-Sep-24 20:59:59\tLabor Day"
    ]
    report = adjudicate_runtime(runtime)
    assert report["verdict"] == "FAIL"
    assert report["adjudications"][0]["reason"] == "DOM_NETWORK_CONTRADICTION"


def test_wrong_dom_instrument_is_rejected_before_promotion():
    runtime = _runtime()
    runtime["results"][0]["dom_witness_lines"][0] = runtime["results"][0][
        "dom_witness_lines"
    ][0].replace("USATECH.IDX/USD", "OTHER.INSTRUMENT")
    with pytest.raises(ValueError, match="DOM_WITNESS_INSTRUMENT_NAME_MISMATCH"):
        adjudicate_runtime(runtime)


def test_multiple_network_records_fail_closed():
    runtime = _runtime()
    runtime["results"][0]["matching_records"].append(
        copy.deepcopy(runtime["results"][0]["matching_records"][0])
    )
    with pytest.raises(
        ValueError,
        match="MULTIPLE_MATCHING_RECORDS_REQUIRE_SEPARATE_ADJUDICATION",
    ):
        adjudicate_runtime(runtime)


def test_multiple_dom_witnesses_fail_closed():
    runtime = _runtime()
    runtime["results"][0]["dom_witness_lines"].append(
        runtime["results"][0]["dom_witness_lines"][0]
    )
    with pytest.raises(
        ValueError,
        match="MULTIPLE_DOM_WITNESSES_REQUIRE_SEPARATE_ADJUDICATION",
    ):
        adjudicate_runtime(runtime)


def test_capture_layer_captured_is_not_automatic_pass_for_cross_date_record():
    runtime = _runtime()
    assert runtime["results"][4]["capture_verdict"] == "CAPTURED"
    item = adjudicate_runtime(runtime)["adjudications"][4]
    assert item["verdict"] == "BLOCKED"
    assert item["reason"] == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"


def test_capture_layer_captured_without_record_is_blocked_not_pass():
    runtime = _runtime()
    raw = runtime["results"][0]
    raw["matching_records"] = []
    raw["dom_witness_lines"] = []
    raw["capture_verdict"] = "CAPTURED"
    raw["capture_reason"] = "POSITIVE_RECORD_CAPTURED_PENDING_ARTIFACT_PROVENANCE_ADJUDICATION"
    item = adjudicate_runtime(runtime)["adjudications"][0]
    assert item["verdict"] == "BLOCKED"
    assert item["reason"] == "NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED"


def test_capture_layer_blocked_exact_record_cannot_be_upgraded_without_dom():
    runtime = _runtime()
    raw = runtime["results"][0]
    raw["dom_witness_lines"] = []
    raw["capture_verdict"] = "BLOCKED"
    raw["capture_reason"] = "EXPECTED_DOM_CROSSCHECK_MISSING"
    item = adjudicate_runtime(runtime)["adjudications"][0]
    assert item["verdict"] == "BLOCKED"
    assert item["reason"] == "EXPECTED_DOM_CROSSCHECK_MISSING"


def test_capture_layer_pass_token_is_not_an_admissible_capture_verdict():
    runtime = _runtime()
    runtime["results"][0]["capture_verdict"] = "PASS"
    with pytest.raises(ValueError, match="CAPTURE_VERDICT_INVALID"):
        adjudicate_runtime(runtime)


def test_partial_hour_rounding_tamper_is_detected_independently():
    runtime = _runtime()
    runtime["results"][2]["matching_records"][0]["fully_closed_hours_utc"] = [
        18,
        19,
        20,
        21,
        22,
        23,
    ]
    report = adjudicate_runtime(runtime)
    assert report["verdict"] == "FAIL"
    assert report["adjudications"][2]["reason"] == "CAPTURE_DERIVED_CLOSED_HOURS_MISMATCH"


def test_capture_derived_reopen_tamper_is_detected():
    runtime = _runtime()
    runtime["results"][1]["matching_records"][0]["derived_reopen_utc"] = (
        "2024-11-28T23:59:59Z"
    )
    report = adjudicate_runtime(runtime)
    assert report["verdict"] == "FAIL"
    assert report["adjudications"][1]["reason"] == "CAPTURE_DERIVED_REOPEN_MISMATCH"


def test_dom_witness_without_network_record_is_rejected():
    runtime = _runtime()
    runtime["results"][0]["matching_records"] = []
    with pytest.raises(ValueError, match="DOM_WITNESS_WITHOUT_NETWORK_RECORD"):
        adjudicate_runtime(runtime)


def test_adjudicator_has_no_browser_probe_or_live_membership_recalculation_path():
    source = inspect.getsource(adjudication_module)
    tree = ast.parse(source)
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.lower() for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add((node.module or "").lower())

    calls = _called_function_names(source)
    assert not any("playwright" in name or "selenium" in name for name in imports)
    for forbidden in (
        "probe_candidate",
        "eligible_recovery_queue",
        "recovery_queue",
        "progression_decisions",
        "derive_batch09_membership",
    ):
        assert forbidden not in calls
    assert "batch09_targets" in calls
    assert "validate_positive_recovery_against_frozen_batch" in calls


def test_adjudication_surface_has_no_selection_override_arguments():
    assert list(inspect.signature(adjudicate_runtime).parameters) == ["runtime"]
