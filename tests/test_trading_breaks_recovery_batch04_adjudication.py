from __future__ import annotations

import copy
import inspect
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

import tools.trading_breaks_recovery_batch04_adjudication as adjudication_module
from tools.trading_breaks_recovery_batch04_adjudication import (
    RUNTIME_PATH,
    adjudicate_runtime,
)


def _runtime() -> dict:
    return json.loads(Path(RUNTIME_PATH).read_text(encoding="utf-8"))


def _ms(value: str) -> str:
    dt = datetime.strptime(value, "%d-%b-%y %H:%M:%S").replace(tzinfo=timezone.utc)
    return str(int(dt.timestamp() * 1000))


def test_authoritative_batch04_runtime_adjudicates_3_pass_2_blocked_0_fail():
    report = adjudicate_runtime(_runtime())
    assert report["verdict"] == "PASS"
    assert report["attempted"] == 5
    assert report["pass"] == 3
    assert report["blocked"] == 2
    assert report["fail"] == 0
    assert [item["verdict"] for item in report["adjudications"]] == [
        "PASS",
        "PASS",
        "PASS",
        "BLOCKED",
        "BLOCKED",
    ]
    assert [item["reason"] for item in report["adjudications"][3:]] == [
        "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE",
        "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE",
    ]


def test_exact_target_positive_records_receive_only_target_day_full_hour_projection():
    report = adjudicate_runtime(_runtime())
    expected = {
        0: ("45119", [18, 19, 20, 21, 22]),
        1: ("45120", [19, 20, 21, 22, 23]),
        2: ("46756", [22, 23]),
    }
    for index, (record_id, hours) in expected.items():
        item = report["adjudications"][index]
        assert item["verdict"] == "PASS"
        assert item["reason"] == "EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED"
        assert item["broker_record_id"] == record_id
        assert item["fully_closed_hours_utc"] == hours
        assert item["dom_witness_present"] is True


def test_christmas_observed_overlap_cannot_be_promoted_as_exact_target_evidence():
    report = adjudicate_runtime(_runtime())
    item = report["adjudications"][3]
    assert item["verdict"] == "BLOCKED"
    assert item["reason"] == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert item["overlap_record_id"] == "46756"
    assert item["overlap_start_utc"] == "2022-12-23T21:14:00Z"
    assert item["target_date"] == "2022-12-26"


def test_new_year_observed_overlap_cannot_be_promoted_as_exact_target_evidence():
    report = adjudicate_runtime(_runtime())
    item = report["adjudications"][4]
    assert item["verdict"] == "BLOCKED"
    assert item["reason"] == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert item["overlap_record_id"] == "48045"
    assert item["overlap_start_utc"] == "2022-12-30T21:14:00Z"
    assert item["target_date"] == "2023-01-02"


def test_frozen_membership_tampering_is_rejected_before_adjudication():
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


def test_artifact_provenance_tampering_is_rejected():
    runtime = _runtime()
    runtime["provenance"]["artifact_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="PROVENANCE_MISMATCH:artifact_sha256"):
        adjudicate_runtime(runtime)


def test_wrong_dom_instrument_name_is_rejected_before_any_normalization():
    runtime = _runtime()
    runtime["results"][0]["dom_witness_lines"][0] = runtime["results"][0][
        "dom_witness_lines"
    ][0].replace("USATECH.IDX/USD", "OTHER.INSTRUMENT")
    with pytest.raises(ValueError, match="DOM_WITNESS_INSTRUMENT_NAME_MISMATCH"):
        adjudicate_runtime(runtime)


def test_dom_network_contradiction_on_exact_positive_fails_closed():
    runtime = _runtime()
    runtime["results"][0]["dom_witness_lines"] = [
        "USATECH.IDX/USD\t24-Nov-22 17:59:00\t24-Nov-22 21:59:00\tThanksgiving Day"
    ]
    report = adjudicate_runtime(runtime)
    assert report["verdict"] == "FAIL"
    item = report["adjudications"][0]
    assert item["verdict"] == "FAIL"
    assert item["reason"] == "DOM_NETWORK_CONTRADICTION"


def test_dom_network_contradiction_on_overlap_witness_also_fails_closed():
    runtime = _runtime()
    runtime["results"][3]["dom_witness_lines"] = [
        "USATECH.IDX/USD\t23-Dec-22 21:14:00\t26-Dec-22 21:59:00\tChristmas Day"
    ]
    report = adjudicate_runtime(runtime)
    assert report["verdict"] == "FAIL"
    item = report["adjudications"][3]
    assert item["verdict"] == "FAIL"
    assert item["reason"] == "DOM_NETWORK_CONTRADICTION"


def test_unrelated_neighbor_record_cannot_hide_behind_overlap_blocked_semantics():
    runtime = _runtime()
    record = runtime["results"][3]["matching_records"][0]
    record["start"] = _ms("20-Dec-22 10:00:00")
    record["end"] = _ms("20-Dec-22 11:00:00")
    record["start_utc"] = "2022-12-20T10:00:00Z"
    record["end_last_closed_minute_utc"] = "2022-12-20T11:00:00Z"
    runtime["results"][3]["dom_witness_lines"] = [
        "USATECH.IDX/USD\t20-Dec-22 10:00:00\t20-Dec-22 11:00:00\tChristmas Day"
    ]
    report = adjudicate_runtime(runtime)
    item = report["adjudications"][3]
    assert item["verdict"] == "FAIL"
    assert item["reason"] == "NON_TARGET_RECORD_DOES_NOT_OVERLAP_TARGET_DAY"


def test_overlap_path_cannot_be_used_for_an_exact_target_start_record():
    runtime = _runtime()
    record = runtime["results"][3]["matching_records"][0]
    record["start"] = _ms("26-Dec-22 00:00:00")
    runtime["results"][3]["dom_witness_lines"] = [
        "USATECH.IDX/USD\t26-Dec-22 00:00:00\t26-Dec-22 22:59:00\tChristmas Day"
    ]
    # The record must leave the overlap-only path and face the parent exact-positive validator.
    report = adjudicate_runtime(runtime)
    item = report["adjudications"][3]
    assert item["reason"] != "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"


def test_multiple_records_fail_closed_instead_of_choosing_conveniently():
    runtime = _runtime()
    runtime["results"][0]["matching_records"].append(
        copy.deepcopy(runtime["results"][0]["matching_records"][0])
    )
    with pytest.raises(
        ValueError, match="MULTIPLE_MATCHING_RECORDS_REQUIRE_SEPARATE_ADJUDICATION"
    ):
        adjudicate_runtime(runtime)


def test_adjudication_uses_frozen_batch_only_and_contains_no_browser_or_live_queue_path():
    source = inspect.getsource(adjudication_module).lower()
    assert "playwright" not in source
    assert "chromium" not in source
    assert "probe_candidate" not in source
    assert "eligible_recovery_queue" not in source
    assert "recovery_queue()" not in source
    assert "batch04_targets()" in source
