from __future__ import annotations

import copy
import inspect
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

import tools.trading_breaks_recovery_batch05_adjudication as adjudication_module
from tools.trading_breaks_recovery_batch05_adjudication import RUNTIME_PATH, adjudicate_runtime


def _runtime() -> dict:
    return json.loads(Path(RUNTIME_PATH).read_text(encoding="utf-8"))


def _ms(value: str) -> str:
    dt = datetime.strptime(value, "%d-%b-%y %H:%M:%S").replace(tzinfo=timezone.utc)
    return str(int(dt.timestamp() * 1000))


def test_authoritative_batch05_runtime_adjudicates_5_pass_0_blocked_0_fail():
    report = adjudicate_runtime(_runtime())
    assert report["verdict"] == "PASS"
    assert report["attempted"] == 5
    assert report["pass"] == 5
    assert report["blocked"] == 0
    assert report["fail"] == 0
    assert [x["verdict"] for x in report["adjudications"]] == ["PASS"] * 5


def test_exact_positive_records_and_target_day_hour_projection():
    report = adjudicate_runtime(_runtime())
    expected = {
        0: ("49338", [18, 19, 20, 21, 22]),
        1: ("50456", [18, 19, 20, 21, 22]),
        2: ("52290", [15, 16, 17, 18, 19, 20, 21, 22, 23]),
        3: ("54373", [17, 18, 19, 20, 21]),
        4: ("55281", [17, 18, 19, 20, 21]),
    }
    for index, (record_id, hours) in expected.items():
        item = report["adjudications"][index]
        assert item["verdict"] == "PASS"
        assert item["reason"] == "EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED"
        assert item["broker_record_id"] == record_id
        assert item["fully_closed_hours_utc"] == hours
        assert item["dom_witness_present"] is True


def test_good_friday_multi_day_interval_is_projected_only_to_target_day_hours():
    item = adjudicate_runtime(_runtime())["adjudications"][2]
    assert item["break_start_utc"] == "2023-04-07T14:14:00Z"
    assert item["final_closed_minute_utc"] == "2023-04-09T21:59:00Z"
    assert item["reopen_utc"] == "2023-04-09T22:00:00Z"
    assert item["fully_closed_hours_utc"] == [15, 16, 17, 18, 19, 20, 21, 22, 23]


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


def test_wrong_dom_instrument_is_rejected():
    runtime = _runtime()
    runtime["results"][0]["dom_witness_lines"][0] = runtime["results"][0]["dom_witness_lines"][0].replace("USATECH.IDX/USD", "OTHER.INSTRUMENT")
    with pytest.raises(ValueError, match="DOM_WITNESS_INSTRUMENT_NAME_MISMATCH"):
        adjudicate_runtime(runtime)


def test_dom_network_contradiction_fails_closed():
    runtime = _runtime()
    runtime["results"][0]["dom_witness_lines"] = [
        "USATECH.IDX/USD\t16-Jan-23 16:59:00\t16-Jan-23 22:59:00\tMartin Luther King Jr. Day"
    ]
    report = adjudicate_runtime(runtime)
    assert report["verdict"] == "FAIL"
    assert report["adjudications"][0]["reason"] == "DOM_NETWORK_CONTRADICTION"


def test_multiple_records_fail_closed():
    runtime = _runtime()
    runtime["results"][0]["matching_records"].append(copy.deepcopy(runtime["results"][0]["matching_records"][0]))
    with pytest.raises(ValueError, match="MULTIPLE_MATCHING_RECORDS_REQUIRE_SEPARATE_ADJUDICATION"):
        adjudicate_runtime(runtime)


def test_exact_target_record_cannot_be_demoted_to_overlap_blocked_path():
    report = adjudicate_runtime(_runtime())
    assert all(x["reason"] != "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE" for x in report["adjudications"])


def test_cross_date_record_is_not_promoted_if_runtime_is_tampered():
    runtime = _runtime()
    record = runtime["results"][0]["matching_records"][0]
    record["start"] = _ms("15-Jan-23 23:00:00")
    record["end"] = _ms("16-Jan-23 22:59:00")
    runtime["results"][0]["dom_witness_lines"] = [
        "USATECH.IDX/USD\t15-Jan-23 23:00:00\t16-Jan-23 22:59:00\tMartin Luther King Jr. Day"
    ]
    item = adjudicate_runtime(runtime)["adjudications"][0]
    assert item["verdict"] == "BLOCKED"
    assert item["reason"] == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"


def test_adjudicator_has_no_browser_probe_or_live_queue_path():
    source = inspect.getsource(adjudication_module).lower()
    assert "playwright" not in source
    assert "chromium" not in source
    assert "probe_candidate" not in source
    assert "eligible_recovery_queue" not in source
    assert "recovery_queue()" not in source
    assert "batch05_targets()" in source
