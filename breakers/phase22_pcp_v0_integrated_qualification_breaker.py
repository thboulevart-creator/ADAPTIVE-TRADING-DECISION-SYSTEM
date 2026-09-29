from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/PHASE-22-PCP-V0-INTEGRATED-QUALIFICATION-CONTRACT-V0.1.json"

P1_PATH = ROOT / "tools/p22_01_pure_state_projector.py"
P2_PATH = ROOT / "tools/p22_02_identity_state_verifier.py"
P3_PATH = ROOT / "tools/p22_03_evidence_envelope_recorder.py"

CONTRACT_DOC = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

assert CONTRACT_DOC["schema"] == "ATDS_PHASE_22_PCP_V0_INTEGRATED_QUALIFICATION_CONTRACT_V0_1"
assert CONTRACT_DOC["harness_required"] is False
assert CONTRACT_DOC["test_first_red"] == "NOT_APPLICABLE_NO_NEW_RUNTIME"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P1 = _load(P1_PATH, "phase22_p1")
P2 = _load(P2_PATH, "phase22_p2")
P3 = _load(P3_PATH, "phase22_p3")


def _git(repo: Path, *args: str) -> str:
    cp = subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
        shell=False,
    )
    return cp.stdout.strip()


def _make_repo(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "phase22@example.invalid")
    _git(repo, "config", "user.name", "Phase22 Test")
    (repo / "tracked.txt").write_text("alpha\n", encoding="utf-8")
    _git(repo, "add", "tracked.txt")
    _git(repo, "commit", "-m", "initial")
    _git(repo, "branch", "-M", "integration/system-v1")
    _git(repo, "remote", "add", "origin", "https://github.com/acme/test.git")
    head = _git(repo, "rev-parse", "HEAD")
    tree = _git(repo, "rev-parse", "HEAD^{tree}")
    blob = _git(repo, "rev-parse", "HEAD:tracked.txt")
    expected = {
        "repository": "acme/test",
        "origin": "https://github.com/acme/test.git",
        "branch": "integration/system-v1",
        "head": head,
        "tree": tree,
        "protected_artifacts": {"tracked.txt": blob},
    }
    return repo, expected


def _base_snapshot():
    return {
        "repository": "acme/test",
        "branch": "integration/system-v1",
        "head": "0" * 40,
        "tree": "1" * 40,
        "working_tree_state": "CLEAN",
        "protected_artifacts": {},
    }


def _base_evidence():
    return {
        "operation_id": "PHASE22-INTEGRATED-001",
        "operation_class": "READ_ONLY_INFORMATIONAL",
        "command_or_check": "integrated qualification",
        "start_head": "0" * 40,
        "start_tree": "1" * 40,
        "end_head": "0" * 40,
        "end_tree": "1" * 40,
        "exit_code": 0,
        "stdout": "PASS",
        "stderr": "",
        "files_changed": [],
        "test_results": [{"name": "PHASE22_INTEGRATED", "status": "PASS"}],
        "probe_results": [{"name": "WORKTREE", "status": "PASS", "details": "CLEAN"}],
        "artifact_hashes": {},
        "started_at_utc": "2026-09-29T14:00:00Z",
        "finished_at_utc": "2026-09-29T14:00:01Z",
        "authority_reference": "GOVERNANCE/PHASE-22-PCP-V0-INTEGRATED-QUALIFICATION-CLOSURE-AUTHORITY-V0.1.md",
        "final_status": "PASS",
    }


def test_t22_01_wrong_repository_blocked(tmp_path):
    repo, expected = _make_repo(tmp_path)
    expected["repository"] = "other/repo"
    result = P2.build_verified_snapshot(repo, expected)
    assert result["verification"]["final_status"] == "BLOCKED_REPOSITORY_MISMATCH"


def test_t22_02_wrong_branch_blocked(tmp_path):
    repo, expected = _make_repo(tmp_path)
    expected["branch"] = "main"
    result = P2.build_verified_snapshot(repo, expected)
    assert result["verification"]["final_status"] == "BLOCKED_BRANCH_MISMATCH"


def test_t22_03_head_drift_blocked(tmp_path):
    repo, expected = _make_repo(tmp_path)
    expected["head"] = "a" * 40
    result = P2.build_verified_snapshot(repo, expected)
    assert result["verification"]["final_status"] == "BLOCKED_HEAD_DRIFT"


def test_t22_04_tree_drift_blocked(tmp_path):
    repo, expected = _make_repo(tmp_path)
    expected["tree"] = "b" * 40
    result = P2.build_verified_snapshot(repo, expected)
    assert result["verification"]["final_status"] == "BLOCKED_TREE_DRIFT"


def test_t22_05_protected_blob_drift_blocked(tmp_path):
    repo, expected = _make_repo(tmp_path)
    expected["protected_artifacts"]["tracked.txt"] = "c" * 40
    result = P2.build_verified_snapshot(repo, expected)
    assert result["verification"]["final_status"] == "BLOCKED_PROTECTED_BLOB_DRIFT"
    assert result["snapshot"]["protected_artifacts"]["tracked.txt"]["status"] == "BLOCKED_PROTECTED_BLOB_DRIFT"


def test_t22_06_unavailable_local_state_remains_unknown():
    snapshot = _base_snapshot()
    snapshot.pop("working_tree_state")
    projected = P1.project_active_state(snapshot)
    assert projected["working_tree_state"] == "UNKNOWN"


def test_t22_07_stale_derived_state_detected():
    snapshot = _base_snapshot()
    snapshot["recovery_checkpoint"] = {
        "head": "9" * 40,
        "tree": "8" * 40,
    }
    projected = P1.project_active_state(snapshot)
    assert projected["recovery_checkpoint_status"] == "STALE_DERIVED_STATE_DETECTED"


def test_t22_08_corrupted_cache_has_no_authority_and_rebuilds_from_canonical():
    canonical = _base_snapshot()
    with_corrupt_cache = copy.deepcopy(canonical)
    with_corrupt_cache["cache_authority"] = True
    with_corrupt_cache["cached_active_state"] = {
        "repository": "evil/repo",
        "branch": "evil",
        "head": "f" * 40,
        "tree": "e" * 40,
        "cache_authority": True,
    }
    clean = P1.project_active_state(canonical)
    rebuilt = P1.project_active_state(with_corrupt_cache)
    assert rebuilt == clean
    assert rebuilt["cache_authority"] is False
    assert rebuilt["projection_authority"] is False
    assert rebuilt["reconstructible_from_canonical_inputs"] is True


def test_t22_09_mutation_attempt_blocked(tmp_path):
    repo, _ = _make_repo(tmp_path)
    with pytest.raises(P2.P2202Error, match="GIT_ARGUMENTS_NOT_ALLOWLISTED"):
        P2._run_git_readonly(repo, ("reset", "--hard"))

    evidence = _base_evidence()
    evidence["operation_class"] = "MUTATION"
    envelope = P3.build_evidence_envelope(evidence)
    assert envelope["envelope_authority"] is False
    assert envelope["operation_authorized_by_envelope"] is False
    assert P3.validate_evidence_envelope(envelope)["status"] == "PASS"


def test_t22_10_e1_td_protected_research_isolated():
    snapshot = _base_snapshot()
    protected = {
        "E1_TD_03B": {
            "event_budget": "0 / 1",
            "events_consumed": 0,
            "status": "WAITING_SOURCE_CONTINUATION",
        }
    }
    snapshot["protected_research_state"] = copy.deepcopy(protected)
    projected = P1.project_active_state(snapshot)
    assert projected["protected_research_state"] == protected
    for module in (P1, P2, P3):
        for name in (
            "consume_td03b_event",
            "collect_source_b",
            "acquire_market_data",
            "run_momentum",
            "compute_pnl",
            "backtest",
        ):
            assert not hasattr(module, name)


def test_t22_11_incomplete_evidence_rejected():
    evidence = _base_evidence()
    evidence.pop("artifact_hashes")
    with pytest.raises(P3.P2203Error, match="EVIDENCE_FIELDS"):
        P3.build_evidence_envelope(evidence)


def test_t22_12_no_silent_retry_after_failed_operation(tmp_path, monkeypatch):
    calls = []

    def fail_once(repo_path, args):
        calls.append(tuple(args))
        return 1, "", "synthetic failure"

    monkeypatch.setattr(P2, "_run_git_readonly", fail_once)
    with pytest.raises(P2.P2202Error, match="VERIFICATION_ERROR_ROOT"):
        P2.collect_local_git_state(tmp_path, [])
    assert calls == [("rev-parse", "--show-toplevel")]


def test_i22_01_valid_git_reality_flows_p22_02_to_p22_01(tmp_path):
    repo, expected = _make_repo(tmp_path)
    verified = P2.build_verified_snapshot(repo, expected)
    assert verified["verification"]["final_status"] == "PASS"
    projected = P1.project_active_state(verified["snapshot"])
    assert projected["repository"] == expected["repository"]
    assert projected["branch"] == expected["branch"]
    assert projected["head"] == expected["head"]
    assert projected["tree"] == expected["tree"]
    assert projected["working_tree_state"] == "CLEAN"
    assert projected["projection_authority"] is False
    assert projected["cache_authority"] is False


def test_i22_02_valid_evidence_flows_p22_03_and_tamper_is_blocked():
    evidence = _base_evidence()
    envelope = P3.build_evidence_envelope(evidence)
    assert P3.validate_evidence_envelope(envelope)["status"] == "PASS"

    tampered = copy.deepcopy(envelope)
    tampered["stdout"] = "tampered"
    assert P3.validate_evidence_envelope(tampered)["status"] == "BLOCKED_TAMPERED_ENVELOPE"


def test_i22_03_no_component_grants_authority(tmp_path):
    repo, expected = _make_repo(tmp_path)
    verified = P2.build_verified_snapshot(repo, expected)
    projected = P1.project_active_state(verified["snapshot"])
    envelope = P3.build_evidence_envelope(_base_evidence())

    assert projected["projection_authority"] is False
    assert projected["cache_authority"] is False
    assert envelope["envelope_authority"] is False
    assert envelope["operation_authorized_by_envelope"] is False

    for module in (P1, P2, P3):
        for name in ("authorize", "grant_authority", "approve_operation"):
            assert not hasattr(module, name)


def test_i22_04_no_fourth_runtime_or_production_harness_required():
    assert not (ROOT / "tools/p22_04_authority_classifier.py").exists()
    assert not (ROOT / "tools/phase22_pcp_v0_integrated_qualification.py").exists()
    assert CONTRACT_DOC["harness_required"] is False
