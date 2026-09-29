from __future__ import annotations

import copy
import importlib.util
import json
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/P22-03-EVIDENCE-ENVELOPE-RECORDER-CONTRACT-V0.1.json"
TARGET_PATH = ROOT / "tools/p22_03_evidence_envelope_recorder.py"

CONTRACT_DOC = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
RUNTIME_CONTRACT = "ATDS_P22_03_EVIDENCE_ENVELOPE_RECORDER_V0_1"
ENVELOPE_SCHEMA = "ATDS_P22_03_EVIDENCE_ENVELOPE_V0_1"

assert CONTRACT_DOC["schema"] == "ATDS_P22_03_EVIDENCE_ENVELOPE_RECORDER_CONTRACT_V0_1"
assert [x[0] for x in CONTRACT_DOC["test_cases"]] == [f"P2203-{i:02d}" for i in range(1, 37)]


def _target():
    if not TARGET_PATH.is_file():
        pytest.fail("P22_03_TARGET_ABSENT_EXPECTED_RED", pytrace=False)
    spec = importlib.util.spec_from_file_location("p22_03_under_test", TARGET_PATH)
    if spec is None or spec.loader is None:
        pytest.fail("P22_03_TARGET_UNLOADABLE_EXPECTED_RED", pytrace=False)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _base_evidence():
    return {
        "operation_id": "P22-03-SYNTHETIC-001",
        "operation_class": "TEST_OR_PROBE",
        "command_or_check": "python -m pytest -q synthetic_breaker.py",
        "start_head": "0" * 40,
        "start_tree": "1" * 40,
        "end_head": "2" * 40,
        "end_tree": "3" * 40,
        "exit_code": 0,
        "stdout": "36 passed",
        "stderr": "",
        "files_changed": [
            "tools/p22_03_evidence_envelope_recorder.py",
            "reports/program/example.md",
        ],
        "test_results": [
            {"name": "P22_03_FROZEN_BREAKER", "status": "PASS"},
        ],
        "probe_results": [
            {"name": "WORKTREE_AFTER", "status": "PASS", "details": "CLEAN"},
        ],
        "artifact_hashes": {
            "tools/p22_03_evidence_envelope_recorder.py": "a" * 64,
            "reports/program/example.md": "b" * 64,
        },
        "started_at_utc": "2026-09-29T14:00:00Z",
        "finished_at_utc": "2026-09-29T14:00:01Z",
        "authority_reference": "GOVERNANCE/P22-03-AUTHORITY.md",
        "final_status": "PASS",
    }


def test_p2203_01_runtime_contract_and_surface():
    m = _target()
    assert m.CONTRACT == RUNTIME_CONTRACT
    assert set(CONTRACT_DOC["required_runtime_surface"]).issubset(set(dir(m)))


def test_p2203_02_canonical_json_deterministic():
    m = _target()
    a = {"b": 2, "a": 1}
    b = {"a": 1, "b": 2}
    assert m.canonical_json_bytes(a) == m.canonical_json_bytes(b)


def test_p2203_03_identical_input_identical_envelope_and_digest():
    m = _target()
    a = _base_evidence()
    b = copy.deepcopy(a)
    ea = m.build_evidence_envelope(a)
    eb = m.build_evidence_envelope(b)
    assert ea == eb
    assert ea["evidence_digest"] == eb["evidence_digest"]


@pytest.mark.parametrize("field", CONTRACT_DOC["required_evidence_fields"])
def test_p2203_04_required_fields_enforced(field):
    m = _target()
    evidence = _base_evidence()
    evidence.pop(field)
    with pytest.raises(m.P2203Error, match="EVIDENCE_FIELDS"):
        m.build_evidence_envelope(evidence)


def test_p2203_05_unknown_top_level_field_rejected():
    m = _target()
    evidence = _base_evidence()
    evidence["surprise"] = True
    with pytest.raises(m.P2203Error, match="EVIDENCE_FIELDS"):
        m.build_evidence_envelope(evidence)


@pytest.mark.parametrize("value", ["", None, 7])
def test_p2203_06_operation_id_required_nonempty(value):
    m = _target()
    evidence = _base_evidence()
    evidence["operation_id"] = value
    with pytest.raises(m.P2203Error, match="OPERATION_ID"):
        m.build_evidence_envelope(evidence)


def test_p2203_07_operation_class_restricted():
    m = _target()
    evidence = _base_evidence()
    evidence["operation_class"] = "MAGIC_AUTONOMOUS"
    with pytest.raises(m.P2203Error, match="OPERATION_CLASS"):
        m.build_evidence_envelope(evidence)


def test_p2203_08_command_or_check_preserved_exactly():
    m = _target()
    evidence = _base_evidence()
    evidence["command_or_check"] = "  exact check | with spacing  "
    out = m.build_evidence_envelope(evidence)
    assert out["command_or_check"] == "  exact check | with spacing  "


def test_p2203_09_valid_git_identities_accepted():
    m = _target()
    out = m.build_evidence_envelope(_base_evidence())
    assert out["start_head"] == "0" * 40
    assert out["end_tree"] == "3" * 40


@pytest.mark.parametrize("field", ["start_head", "start_tree", "end_head", "end_tree"])
@pytest.mark.parametrize("value", ["abc", "", "g" * 40, None])
def test_p2203_10_malformed_git_identity_rejected(field, value):
    m = _target()
    evidence = _base_evidence()
    evidence[field] = value
    with pytest.raises(m.P2203Error, match="GIT_IDENTITY"):
        m.build_evidence_envelope(evidence)


def test_p2203_11_explicit_unknown_git_identity_preserved():
    m = _target()
    evidence = _base_evidence()
    for field in ("start_head", "start_tree", "end_head", "end_tree"):
        evidence[field] = "UNKNOWN"
    out = m.build_evidence_envelope(evidence)
    assert [out[x] for x in ("start_head", "start_tree", "end_head", "end_tree")] == ["UNKNOWN"] * 4


@pytest.mark.parametrize("value", [0, 1, -1, "UNKNOWN"])
def test_p2203_12_valid_exit_code_or_unknown(value):
    m = _target()
    evidence = _base_evidence()
    evidence["exit_code"] = value
    assert m.build_evidence_envelope(evidence)["exit_code"] == value


@pytest.mark.parametrize("value", [None, 1.5, "0"])
def test_p2203_12b_invalid_exit_code_rejected(value):
    m = _target()
    evidence = _base_evidence()
    evidence["exit_code"] = value
    with pytest.raises(m.P2203Error, match="EXIT_CODE"):
        m.build_evidence_envelope(evidence)


def test_p2203_13_stdout_stderr_preserved_exactly():
    m = _target()
    evidence = _base_evidence()
    evidence["stdout"] = " line 1\nline 2 "
    evidence["stderr"] = "\twarning\n"
    out = m.build_evidence_envelope(evidence)
    assert out["stdout"] == evidence["stdout"]
    assert out["stderr"] == evidence["stderr"]


def test_p2203_14_relative_changed_paths_accepted():
    m = _target()
    evidence = _base_evidence()
    evidence["files_changed"] = ["a.txt", "dir/b.json"]
    assert m.build_evidence_envelope(evidence)["files_changed"] == ["a.txt", "dir/b.json"]


@pytest.mark.parametrize("bad", ["/abs.txt", "../escape.txt", "dir/../escape.txt", "C:/abs.txt", "./same.txt", ""])
def test_p2203_15_absolute_or_traversal_path_rejected(bad):
    m = _target()
    evidence = _base_evidence()
    evidence["files_changed"] = [bad]
    with pytest.raises(m.P2203Error, match="FILES_CHANGED_PATH"):
        m.build_evidence_envelope(evidence)


def test_p2203_16_duplicate_changed_paths_rejected():
    m = _target()
    evidence = _base_evidence()
    evidence["files_changed"] = ["a.txt", "a.txt"]
    with pytest.raises(m.P2203Error, match="FILES_CHANGED_DUPLICATE"):
        m.build_evidence_envelope(evidence)


def test_p2203_17_artifact_sha256_accepted():
    m = _target()
    out = m.build_evidence_envelope(_base_evidence())
    assert out["artifact_hashes"]["tools/p22_03_evidence_envelope_recorder.py"] == "a" * 64


@pytest.mark.parametrize("value", ["abc", "g" * 64, "", None])
def test_p2203_18_malformed_artifact_sha_rejected(value):
    m = _target()
    evidence = _base_evidence()
    evidence["artifact_hashes"] = {"artifact.txt": value}
    with pytest.raises(m.P2203Error, match="ARTIFACT_HASH"):
        m.build_evidence_envelope(evidence)


def test_p2203_19_test_result_fail_preserved():
    m = _target()
    evidence = _base_evidence()
    evidence["test_results"] = [{"name": "test-x", "status": "FAIL", "details": "assertion"}]
    out = m.build_evidence_envelope(evidence)
    assert out["test_results"][0]["status"] == "FAIL"


def test_p2203_20_probe_result_unknown_preserved():
    m = _target()
    evidence = _base_evidence()
    evidence["probe_results"] = [{"name": "probe-x", "status": "UNKNOWN"}]
    out = m.build_evidence_envelope(evidence)
    assert out["probe_results"][0]["status"] == "UNKNOWN"


def test_p2203_21_utc_z_timestamps_accepted():
    m = _target()
    out = m.build_evidence_envelope(_base_evidence())
    assert out["started_at_utc"].endswith("Z")
    assert out["finished_at_utc"].endswith("Z")


@pytest.mark.parametrize(
    "field,value",
    [
        ("started_at_utc", "2026-09-29T14:00:00"),
        ("finished_at_utc", "2026-09-29T14:00:01+02:00"),
        ("started_at_utc", "not-a-time"),
    ],
)
def test_p2203_22_naive_or_non_utc_timestamp_rejected(field, value):
    m = _target()
    evidence = _base_evidence()
    evidence[field] = value
    with pytest.raises(m.P2203Error, match="UTC_TIMESTAMP"):
        m.build_evidence_envelope(evidence)


def test_p2203_23_reversed_interval_rejected():
    m = _target()
    evidence = _base_evidence()
    evidence["started_at_utc"] = "2026-09-29T14:00:02Z"
    evidence["finished_at_utc"] = "2026-09-29T14:00:01Z"
    with pytest.raises(m.P2203Error, match="TIME_ORDER"):
        m.build_evidence_envelope(evidence)


def test_p2203_24_authority_reference_provenance_only():
    m = _target()
    evidence = _base_evidence()
    evidence["authority_reference"] = "AUTH-REF-123"
    out = m.build_evidence_envelope(evidence)
    assert out["authority_reference"] == "AUTH-REF-123"
    assert out["envelope_authority"] is False
    assert out["operation_authorized_by_envelope"] is False


def test_p2203_25_envelope_cannot_grant_authority():
    m = _target()
    for operation_class in CONTRACT_DOC["allowed_operation_classes"]:
        evidence = _base_evidence()
        evidence["operation_class"] = operation_class
        out = m.build_evidence_envelope(evidence)
        assert out["envelope_authority"] is False
        assert out["operation_authorized_by_envelope"] is False


def test_p2203_26_digest_binds_entire_body():
    m = _target()
    envelope = m.build_evidence_envelope(_base_evidence())
    body = {k: v for k, v in envelope.items() if k != "evidence_digest"}
    assert envelope["evidence_digest"] == m.canonical_sha256(body)
    changed = copy.deepcopy(body)
    changed["authority_reference"] = "DIFFERENT"
    assert m.canonical_sha256(changed) != envelope["evidence_digest"]


def test_p2203_27_single_field_mutation_detected():
    m = _target()
    envelope = m.build_evidence_envelope(_base_evidence())
    envelope["stdout"] = "tampered"
    assert m.validate_evidence_envelope(envelope)["status"] == "BLOCKED_TAMPERED_ENVELOPE"


def test_p2203_28_validation_does_not_repair_or_reseal():
    m = _target()
    envelope = m.build_evidence_envelope(_base_evidence())
    envelope["stderr"] = "tampered"
    before = copy.deepcopy(envelope)
    result = m.validate_evidence_envelope(envelope)
    assert result["status"] == "BLOCKED_TAMPERED_ENVELOPE"
    assert envelope == before


def test_p2203_29_canonical_json_forbids_nonfinite():
    m = _target()
    with pytest.raises(ValueError):
        m.canonical_json_bytes({"x": math.nan})
    with pytest.raises(ValueError):
        m.canonical_json_bytes({"x": math.inf})


def test_p2203_30_input_evidence_not_mutated():
    m = _target()
    evidence = _base_evidence()
    before = copy.deepcopy(evidence)
    m.build_evidence_envelope(evidence)
    assert evidence == before


def test_p2203_31_output_machine_readable():
    m = _target()
    envelope = m.build_evidence_envelope(_base_evidence())
    assert set(envelope) == set(CONTRACT_DOC["output_fields"])
    assert envelope["schema"] == ENVELOPE_SCHEMA
    assert json.loads(m.canonical_json_bytes(envelope).decode("utf-8")) == envelope


def test_p2203_32_no_execution_network_or_write_surface():
    m = _target()
    src = TARGET_PATH.read_text(encoding="utf-8")
    forbidden_tokens = (
        "subprocess",
        "os.system",
        "Popen(",
        "requests",
        "urllib",
        "httpx",
        "aiohttp",
        "socket.",
        ".write_text(",
        ".write_bytes(",
        ".unlink(",
        ".rename(",
        ".replace(",
    )
    assert all(token not in src for token in forbidden_tokens)
    for name in CONTRACT_DOC["forbidden_runtime_surface"]:
        assert not hasattr(m, name)


def test_p2203_33_no_e1_or_performance_execution_surface():
    m = _target()
    for name in ("run_momentum", "compute_pnl", "backtest", "build_h1", "tail_dependence"):
        assert not hasattr(m, name)


def test_p2203_34_td03b_event_cannot_be_consumed():
    m = _target()
    assert not hasattr(m, "consume_td03b_event")
    assert not hasattr(m, "collect_source_b")
    assert not hasattr(m, "acquire_market_data")


def test_p2203_35_p2202_evidence_represented_without_laundering():
    m = _target()
    evidence = _base_evidence()
    evidence["operation_id"] = "P22-02-REAL-QUALIFICATION"
    evidence["operation_class"] = "READ_ONLY_INFORMATIONAL"
    evidence["command_or_check"] = "P22_02_REAL_VERIFICATION"
    evidence["stdout"] = json.dumps(
        {
            "P22_02_REAL_VERIFICATION": "PASS",
            "P22_01_INTEGRATION": "PASS",
            "PROTECTED_COUNT": 10,
        },
        sort_keys=True,
    )
    evidence["files_changed"] = []
    evidence["artifact_hashes"] = {}
    evidence["test_results"] = [{"name": "P22_02_FROZEN_BREAKER", "status": "PASS"}]
    evidence["probe_results"] = [{"name": "WORKTREE_AFTER", "status": "PASS", "details": "CLEAN"}]
    out = m.build_evidence_envelope(evidence)
    decoded = json.loads(out["stdout"])
    assert decoded["P22_02_REAL_VERIFICATION"] == "PASS"
    assert decoded["PROTECTED_COUNT"] == 10
    assert out["final_status"] == "PASS"
    assert out["operation_authorized_by_envelope"] is False


def test_p2203_36_untouched_envelope_validates_pass():
    m = _target()
    envelope = m.build_evidence_envelope(_base_evidence())
    result = m.validate_evidence_envelope(envelope)
    assert result == {
        "status": "PASS",
        "evidence_digest": envelope["evidence_digest"],
    }
