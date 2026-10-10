"""F03-CR2-CR1-M1 evidence integrity + causal discriminator tests.
Pure read-only replay of persisted measurements. No synthetic worker starts here.
"""
import base64
import csv
import hashlib
import io
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "reports/program/2026-10-10-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M1-FORENSIC-EVIDENCE-V0.1.json"
FREEZE = ROOT / "GOVERNANCE/AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M1-PREEXECUTION-FREEZE-V0.1.json"
EXPECTED = {"A1": 96, "B1": 512, "A2": 96, "B2": 512}
STEP = 16 * 1024 * 1024


@pytest.fixture(scope="module")
def evidence():
    j = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert j["terminal_decision"] == "ROOT_CAUSE_NOT_PROVEN"
    assert j["experiment_budget_used"] == 4
    assert j["experiment_budget_max"] == 8
    return j


def decode_case(evidence, case):
    d = evidence["cases"][case]
    b = base64.b64decode(d["csv_base64"], validate=True)
    assert hashlib.sha256(b).hexdigest() == d["sha256"]
    return list(csv.DictReader(io.StringIO(b.decode("utf-8"))))


def test_freeze_and_instrument_sha(evidence):
    raw = FREEZE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == evidence["freeze_sha256"]
    source = base64.b64decode(evidence["instrument_source_base64"], validate=True)
    assert hashlib.sha256(source).hexdigest() == evidence["instrument_source_sha256"]
    assert evidence["instrument_binary_sha256"]
    assert evidence["frozen_parameters"]["native_allocation_step_bytes"] == STEP
    assert evidence["frozen_parameters"]["planned_process_executions"] == 4


@pytest.mark.parametrize("case,limit", list(EXPECTED.items()))
def test_replay_case_identity(evidence, case, limit):
    data = evidence["cases"][case]
    rows = decode_case(evidence, case)
    assert rows
    assert int(data["limit_mib"]) == limit
    assert rows[0]["event"] == "T0_BEFORE_JOB_CONFIGURATION"
    assert rows[-1]["event"] == "T7_AFTER_TERMINATION"
    assert int(data["supervisor_exit"]) == 0
    assert all(int(x["limit"]) == limit * 1024 * 1024 for x in rows)
    assert len({x["worker_pid"] for x in rows if x["worker_pid"] != "NA"}) == 1


@pytest.mark.parametrize("case", ["A1", "A2"])
def test_denial_changes_peak_not_committed(evidence, case):
    rows = decode_case(evidence, case)
    pre = [r for r in rows if r["event"] == "T4_AFTER_SUCCESSFUL_ALLOCATION"][-1]
    denied = [r for r in rows if r["event"] == "T5_AFTER_DENIED_ALLOCATION"]
    assert len(denied) == 1
    denied = denied[0]
    assert int(denied["win32"]) == 1455
    assert int(denied["committed_chunks"]) == 4
    assert int(denied["job_current"]) == int(pre["job_current"])
    assert int(denied["psapi_private"]) == int(pre["psapi_private"])
    assert int(denied["dotnet_private"]) == int(pre["dotnet_private"])
    assert int(denied["job_peak_28"]) - int(pre["job_peak_28"]) == STEP + 32768
    assert int(denied["job_peak_28"]) > 96 * 1024 * 1024
    assert int(denied["job_peak_9"]) == int(denied["job_peak_28"])


@pytest.mark.parametrize("case", ["B1", "B2"])
def test_positive_controls_are_truly_committed(evidence, case):
    rows = decode_case(evidence, case)
    good = [r for r in rows if r["event"] == "T4_AFTER_SUCCESSFUL_ALLOCATION"]
    assert len(good) == 12
    assert not [r for r in rows if r["event"] == "T5_AFTER_DENIED_ALLOCATION"]
    assert int(good[-1]["requested_bytes"]) == 192 * 1024 * 1024
    assert int(good[-1]["committed_chunks"]) == 12
    assert int(good[-1]["job_peak_28"]) == int(good[-1]["job_current"])
    assert int(good[-1]["job_peak_9"]) == int(good[-1]["job_peak_28"])


def test_unique_workers_and_no_more_than_four_experiments(evidence):
    assert set(evidence["cases"]) == set(EXPECTED)
    allpids = []
    for c in EXPECTED:
        rows = decode_case(evidence, c)
        pids = [r["worker_pid"] for r in rows if r["worker_pid"] != "NA"]
        allpids.append(pids[0])
    assert len(set(allpids)) == 4
    assert evidence["live_worker_count_after_tests"] == 0


def test_causal_distinction_does_not_overclaim(evidence):
    assert evidence["root_cause_internal_windows"] == "NOT_PROVEN"
    assert evidence["observable_counter_behavior"] == "REPRODUCED_AND_QUANTITATIVELY_CONSTRAINED"
    assert evidence["job_limit_enforcement"] == "PASS_SYNTHETIC"
    assert evidence["discriminating_observations"]["denied_attempt_peak_delta_bytes"] == 16809984
    assert evidence["discriminating_observations"]["denied_attempt_requested_bytes"] == STEP
    assert evidence["discriminating_observations"]["unexplained_remainder_bytes"] == 32768


def test_no_frozen_sources_modified(evidence):
    assert evidence["firewall"]["fc01_canonical_source_mutation"] is False
    assert evidence["firewall"]["cr2_existing_sources_mutated"] is False
    assert evidence["firewall"]["provider_requests"] == 0
    assert evidence["firewall"]["b12"] == "CLOSED"


def test_measurement_apis_are_distinct_paths(evidence):
    bindings = evidence["measurement_instrumentation"]
    assert "QueryInformationJobObject" in bindings["job"]
    assert "GetProcessMemoryInfo" in bindings["process"]
    assert "VirtualAlloc" in bindings["allocation"]
    assert bindings["independent_of_kernel"] is False
