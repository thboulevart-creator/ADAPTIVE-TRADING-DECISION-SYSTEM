from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tools.trading_breaks_recovery_batch03_adjudication import (
    RUNTIME_PATH,
    adjudicate_runtime,
)


def _runtime() -> dict:
    return json.loads(Path(RUNTIME_PATH).read_text(encoding="utf-8"))


def test_authoritative_batch03_runtime_adjudicates_4_pass_1_blocked_0_fail():
    report = adjudicate_runtime(_runtime())
    assert report["verdict"] == "PASS"
    assert report["attempted"] == 5
    assert report["pass"] == 4
    assert report["blocked"] == 1
    assert report["fail"] == 0
    assert [item["verdict"] for item in report["adjudications"]] == [
        "PASS", "PASS", "BLOCKED", "PASS", "PASS"
    ]
    assert report["adjudications"][2]["reason"] == "NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED"


def test_positive_records_are_exact_target_date_and_dom_matched():
    report = adjudicate_runtime(_runtime())
    for index in (0, 1, 3, 4):
        item = report["adjudications"][index]
        assert item["verdict"] == "PASS"
        assert item["reason"] == "EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED"
        assert item["dom_witness_present"] is True
        assert item["broker_record_id"]
        assert item["fully_closed_hours_utc"] == [17, 18, 19, 20, 21]


def test_no_record_date_cannot_be_promoted_from_absence():
    report = adjudicate_runtime(_runtime())
    item = report["adjudications"][2]
    assert item["target_date"] if "target_date" in item else True
    assert item["verdict"] == "BLOCKED"
    assert item["reason"] == "NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED"
    assert item["broker_record_id"] is None


def test_runtime_membership_tampering_is_rejected_before_adjudication():
    runtime = _runtime()
    runtime["targets"][0]["date"] = "2099-01-01"
    with pytest.raises(ValueError, match="FROZEN_MEMBERSHIP_MISMATCH"):
        adjudicate_runtime(runtime)


def test_artifact_provenance_tampering_is_rejected():
    runtime = _runtime()
    runtime["provenance"]["artifact_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="PROVENANCE_MISMATCH:artifact_sha256"):
        adjudicate_runtime(runtime)


def test_missing_dom_witness_on_positive_capture_does_not_silently_pass():
    runtime = _runtime()
    runtime["results"][0]["dom_witness_lines"] = []
    report = adjudicate_runtime(runtime)
    # The protocol permits network-only evidence when DOM is genuinely unavailable,
    # so the independent adjudicator must not claim a DOM cross-check in that case.
    item = report["adjudications"][0]
    assert item["verdict"] == "PASS"
    assert item["dom_witness_present"] is False


def test_dom_network_contradiction_is_fail_closed():
    runtime = _runtime()
    runtime["results"][0]["dom_witness_lines"] = [
        "USATECH.IDX/USD\t30-May-22 16:59:00\t30-May-22 20:59:00\tMemorial Day"
    ]
    report = adjudicate_runtime(runtime)
    item = report["adjudications"][0]
    assert item["verdict"] == "FAIL"
    assert item["reason"] == "DOM_NETWORK_CONTRADICTION"
    assert report["verdict"] == "FAIL"


def test_neighboring_date_record_cannot_be_promoted_as_exact_target_date():
    runtime = _runtime()
    tampered = copy.deepcopy(runtime)
    # Insert the exact Memorial Day record into the July 1 target. The parent
    # protocol must reject it because its start date is not the target date.
    tampered["results"][2]["matching_records"] = [
        copy.deepcopy(runtime["results"][0]["matching_records"][0])
    ]
    tampered["results"][2]["dom_witness_lines"] = []
    report = adjudicate_runtime(tampered)
    item = report["adjudications"][2]
    assert item["verdict"] == "FAIL"
    assert item["reason"] == "NETWORK_RECORD_DATE_MISMATCH"
