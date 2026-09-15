from __future__ import annotations

import copy
import inspect
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

import tools.trading_breaks_recovery_batch08_adjudication as adjudication_module
from tools.trading_breaks_recovery_batch08_adjudication import RUNTIME_PATH, adjudicate_runtime


def _runtime() -> dict:
    return json.loads(Path(RUNTIME_PATH).read_text(encoding="utf-8"))


def _ms(value: str) -> str:
    dt = datetime.strptime(value, "%d-%b-%y %H:%M:%S").replace(tzinfo=timezone.utc)
    return str(int(dt.timestamp() * 1000))


def test_authoritative_batch08_runtime_adjudicates_4_pass_1_blocked_0_fail():
    report = adjudicate_runtime(_runtime())
    assert report["verdict"] == "PASS"
    assert report["attempted"] == 5
    assert report["pass"] == 4
    assert report["blocked"] == 1
    assert report["fail"] == 0
    assert [x["verdict"] for x in report["adjudications"]] == ["BLOCKED", "PASS", "PASS", "PASS", "PASS"]


def test_good_friday_cross_date_record_is_blocked_and_never_promoted():
    item = adjudicate_runtime(_runtime())["adjudications"][0]
    assert item["verdict"] == "BLOCKED"
    assert item["reason"] == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert item["overlap_record_id"] == "66555"
    assert item["broker_record_id"] == "66555"
    assert item["capture_reason"] == "EXPECTED_DOM_CROSSCHECK_MISSING"
    assert "break_start_utc" not in item
    assert "fully_closed_hours_utc" not in item


def test_exact_positive_records_are_validated_with_target_day_hour_projection():
    report = adjudicate_runtime(_runtime())
    expected = {
        1: ("68242", [17, 18, 19, 20, 21]),
        2: ("69037", [17, 18, 19, 20, 21]),
        3: ("69819", [18, 19, 20, 21]),
        4: ("69820", [17, 18, 19, 20, 21]),
    }
    for index, (record_id, hours) in expected.items():
        item = report["adjudications"][index]
        assert item["verdict"] == "PASS"
        assert item["reason"] == "EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED"
        assert item["broker_record_id"] == record_id
        assert item["fully_closed_hours_utc"] == hours
        assert item["dom_witness_present"] is True


def test_partial_start_hours_are_not_rounded_closed():
    july3 = adjudicate_runtime(_runtime())["adjudications"][3]
    assert july3["break_start_utc"] == "2024-07-03T17:14:59Z"
    assert july3["fully_closed_hours_utc"] == [18, 19, 20, 21]
    assert 17 not in july3["fully_closed_hours_utc"]


def test_frozen_membership_tampering_is_rejected():
    runtime = _runtime()
    runtime["targets"][0]["date"] = "2099-01-01"
    with pytest.raises(ValueError, match="FROZEN_MEMBERSHIP_MISMATCH"):
        adjudicate_runtime(runtime)


def test_runtime_result_reordering_is_rejected():
    runtime = _runtime()
    runtime["results"][0], runtime["results"][1] = runtime["results"][1], runtime["results"][0]
    with pytest.raises(ValueError, match="RESULT_TARGET_ORDER_OR_IDENTITY_MISMATCH"):
        adjudicate_runtime(runtime)


def test_artifact_provenance_tampering_is_rejected():
    runtime = _runtime()
    runtime["provenance"]["artifact_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="PROVENANCE_MISMATCH:artifact_sha256"):
        adjudicate_runtime(runtime)


def test_probe_commit_tampering_is_rejected():
    runtime = _runtime()
    runtime["provenance"]["probe_commit"] = "0" * 40
    with pytest.raises(ValueError, match="PROVENANCE_MISMATCH:probe_commit"):
        adjudicate_runtime(runtime)


def test_wrong_dom_instrument_is_rejected():
    runtime = _runtime()
    runtime["results"][1]["dom_witness_lines"][0] = runtime["results"][1]["dom_witness_lines"][0].replace("USATECH.IDX/USD", "OTHER.INSTRUMENT")
    with pytest.raises(ValueError, match="DOM_WITNESS_INSTRUMENT_NAME_MISMATCH"):
        adjudicate_runtime(runtime)


def test_dom_network_contradiction_fails_closed():
    runtime = _runtime()
    runtime["results"][1]["dom_witness_lines"] = ["USATECH.IDX/USD\t27-May-24 17:59:59\t27-May-24 21:59:59\tMemorial Day"]
    report = adjudicate_runtime(runtime)
    assert report["verdict"] == "FAIL"
    assert report["adjudications"][1]["reason"] == "DOM_NETWORK_CONTRADICTION"


def test_multiple_records_fail_closed():
    runtime = _runtime()
    runtime["results"][1]["matching_records"].append(copy.deepcopy(runtime["results"][1]["matching_records"][0]))
    with pytest.raises(ValueError, match="MULTIPLE_MATCHING_RECORDS_REQUIRE_SEPARATE_ADJUDICATION"):
        adjudicate_runtime(runtime)


def test_exact_target_records_cannot_be_demoted_to_overlap_path():
    report = adjudicate_runtime(_runtime())
    for index in (1, 2, 3, 4):
        assert report["adjudications"][index]["verdict"] == "PASS"
        assert report["adjudications"][index]["reason"] != "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"


def test_good_friday_cross_date_record_cannot_be_promoted_even_without_dom():
    runtime = _runtime()
    assert runtime["results"][0]["requested_date"] == "2024-03-29"
    assert runtime["results"][0]["matching_records"][0]["start_utc"].startswith("2024-03-28")
    assert runtime["results"][0]["dom_witness_lines"] == []
    item = adjudicate_runtime(runtime)["adjudications"][0]
    assert item["verdict"] == "BLOCKED"
    assert item["reason"] == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"


def test_unrelated_cross_date_record_fails_instead_of_becoming_blocked_witness():
    runtime = _runtime()
    record = runtime["results"][0]["matching_records"][0]
    record["start"] = _ms("20-Mar-24 20:14:59")
    record["end"] = _ms("20-Mar-24 21:59:59")
    item = adjudicate_runtime(runtime)["adjudications"][0]
    assert item["verdict"] == "FAIL"
    assert item["reason"] == "NON_TARGET_RECORD_DOES_NOT_OVERLAP_TARGET_DAY"


def test_adjudicator_has_no_browser_probe_or_live_queue_path():
    source = inspect.getsource(adjudication_module).lower()
    for forbidden in ("playwright", "chromium", "probe_candidate", "eligible_recovery_queue", "recovery_queue()"):
        assert forbidden not in source
    assert "batch08_targets()" in source
