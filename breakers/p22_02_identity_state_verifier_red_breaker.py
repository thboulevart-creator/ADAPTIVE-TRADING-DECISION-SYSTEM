from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/P22-02-IDENTITY-STATE-VERIFIER-CONTRACT-V0.1.json"
TARGET_PATH = ROOT / "tools/p22_02_identity_state_verifier.py"
P2201_PATH = ROOT / "tools/p22_01_pure_state_projector.py"

CONTRACT_DOC = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
RUNTIME_CONTRACT = "ATDS_P22_02_IDENTITY_STATE_VERIFIER_V0_1"

assert CONTRACT_DOC["schema"] == "ATDS_P22_02_IDENTITY_STATE_VERIFIER_CONTRACT_V0_1"
assert [x[0] for x in CONTRACT_DOC["test_cases"]] == [f"P2202-{i:02d}" for i in range(1, 29)]


def _target():
    if not TARGET_PATH.is_file():
        pytest.fail("P22_02_TARGET_ABSENT_EXPECTED_RED", pytrace=False)
    spec = importlib.util.spec_from_file_location("p22_02_under_test", TARGET_PATH)
    if spec is None or spec.loader is None:
        pytest.fail("P22_02_TARGET_UNLOADABLE_EXPECTED_RED", pytrace=False)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _p2201():
    spec = importlib.util.spec_from_file_location("p22_01_for_integration", P2201_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    _git(repo, "config", "user.email", "p22@example.invalid")
    _git(repo, "config", "user.name", "P22 Test")
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


def _clean_result(tmp_path: Path):
    m = _target()
    repo, expected = _make_repo(tmp_path)
    return m, repo, expected, m.build_verified_snapshot(repo, expected)


def test_p2202_01_exact_repository_accepted(tmp_path):
    _, _, _, result = _clean_result(tmp_path)
    assert result["verification"]["checks"]["repository"] == "PASS"
    assert result["verification"]["final_status"] == "PASS"


def test_p2202_02_wrong_repository_blocked(tmp_path):
    m, repo, expected = _make_repo_and_target(tmp_path)
    expected["repository"] = "other/repo"
    result = m.build_verified_snapshot(repo, expected)
    assert result["verification"]["final_status"] == "BLOCKED_REPOSITORY_MISMATCH"


def _make_repo_and_target(tmp_path):
    m = _target()
    repo, expected = _make_repo(tmp_path)
    return m, repo, expected


def test_p2202_03_expected_origin_accepted(tmp_path):
    _, _, _, result = _clean_result(tmp_path)
    assert result["verification"]["checks"]["origin"] == "PASS"


def test_p2202_04_wrong_origin_blocked(tmp_path):
    m, repo, expected = _make_repo_and_target(tmp_path)
    expected["origin"] = "https://github.com/acme/other.git"
    assert m.build_verified_snapshot(repo, expected)["verification"]["final_status"] == "BLOCKED_REMOTE_MISMATCH"


def test_p2202_05_correct_branch_accepted(tmp_path):
    _, _, _, result = _clean_result(tmp_path)
    assert result["verification"]["checks"]["branch"] == "PASS"


def test_p2202_06_wrong_branch_blocked(tmp_path):
    m, repo, expected = _make_repo_and_target(tmp_path)
    expected["branch"] = "main"
    assert m.build_verified_snapshot(repo, expected)["verification"]["final_status"] == "BLOCKED_BRANCH_MISMATCH"


def test_p2202_07_detached_head_blocked(tmp_path):
    m, repo, expected = _make_repo_and_target(tmp_path)
    _git(repo, "checkout", "--detach")
    result = m.build_verified_snapshot(repo, expected)
    assert result["observed"]["detached_head"] is True
    assert result["verification"]["final_status"] == "BLOCKED_DETACHED_HEAD"


def test_p2202_08_exact_head_accepted(tmp_path):
    _, _, _, result = _clean_result(tmp_path)
    assert result["verification"]["checks"]["head"] == "PASS"


def test_p2202_09_wrong_head_blocked(tmp_path):
    m, repo, expected = _make_repo_and_target(tmp_path)
    expected["head"] = "a" * 40
    assert m.build_verified_snapshot(repo, expected)["verification"]["final_status"] == "BLOCKED_HEAD_DRIFT"


def test_p2202_10_exact_tree_accepted(tmp_path):
    _, _, _, result = _clean_result(tmp_path)
    assert result["verification"]["checks"]["tree"] == "PASS"


def test_p2202_11_wrong_tree_blocked(tmp_path):
    m, repo, expected = _make_repo_and_target(tmp_path)
    expected["tree"] = "b" * 40
    assert m.build_verified_snapshot(repo, expected)["verification"]["final_status"] == "BLOCKED_TREE_DRIFT"


def test_p2202_12_clean_worktree(tmp_path):
    _, _, _, result = _clean_result(tmp_path)
    assert result["observed"]["working_tree_state"] == "CLEAN"
    assert result["verification"]["checks"]["working_tree"] == "PASS"


def test_p2202_13_tracked_modification_dirty(tmp_path):
    m, repo, expected = _make_repo_and_target(tmp_path)
    (repo / "tracked.txt").write_text("changed\n", encoding="utf-8")
    result = m.build_verified_snapshot(repo, expected)
    assert result["observed"]["tracked_modifications"] is True
    assert result["verification"]["final_status"] == "DIRTY_WORKTREE"


def test_p2202_14_untracked_file_dirty(tmp_path):
    m, repo, expected = _make_repo_and_target(tmp_path)
    (repo / "untracked.txt").write_text("x\n", encoding="utf-8")
    result = m.build_verified_snapshot(repo, expected)
    assert result["observed"]["untracked_files"] is True
    assert result["verification"]["final_status"] == "DIRTY_WORKTREE"


def test_p2202_15_protected_exact_blob_passes(tmp_path):
    _, _, _, result = _clean_result(tmp_path)
    assert result["snapshot"]["protected_artifacts"]["tracked.txt"]["status"] == "PASS"


def test_p2202_16_protected_blob_mismatch_blocks(tmp_path):
    m, repo, expected = _make_repo_and_target(tmp_path)
    expected["protected_artifacts"]["tracked.txt"] = "c" * 40
    result = m.build_verified_snapshot(repo, expected)
    assert result["verification"]["final_status"] == "BLOCKED_PROTECTED_BLOB_DRIFT"
    assert result["snapshot"]["protected_artifacts"]["tracked.txt"]["status"] == "BLOCKED_PROTECTED_BLOB_DRIFT"


def test_p2202_17_missing_protected_path_blocks(tmp_path):
    m, repo, expected = _make_repo_and_target(tmp_path)
    expected["protected_artifacts"] = {"missing.txt": "d" * 40}
    result = m.build_verified_snapshot(repo, expected)
    assert result["verification"]["final_status"] == "BLOCKED_PROTECTED_PATH_MISSING"
    assert result["snapshot"]["protected_artifacts"]["missing.txt"]["observed_blob"] is None


@pytest.mark.parametrize(
    "field,value",
    [
        ("head", "abc"),
        ("tree", ""),
        ("repository", ""),
        ("origin", ""),
        ("branch", ""),
    ],
)
def test_p2202_18_malformed_expected_binding_fails_closed(tmp_path, field, value):
    m, repo, expected = _make_repo_and_target(tmp_path)
    expected[field] = value
    result = m.build_verified_snapshot(repo, expected)
    assert result["verification"]["final_status"] == "INVALID_EXPECTED_BINDING"


def test_p2202_18b_malformed_protected_sha_fails_closed(tmp_path):
    m, repo, expected = _make_repo_and_target(tmp_path)
    expected["protected_artifacts"]["tracked.txt"] = "xyz"
    result = m.build_verified_snapshot(repo, expected)
    assert result["verification"]["final_status"] == "INVALID_EXPECTED_BINDING"


def test_p2202_19_fixed_read_only_allowlist():
    m = _target()
    allowed = {tuple(x) for x in CONTRACT_DOC["allowed_git_arguments"][:-1]}
    assert allowed.issubset(set(m.ALLOWED_GIT_ARGUMENTS))
    assert m.PROTECTED_BLOB_PATTERN == ("rev-parse", "HEAD:<PROTECTED_RELATIVE_PATH>")


def test_p2202_20_no_shell_execution_surface():
    _target()
    src = TARGET_PATH.read_text(encoding="utf-8")
    assert "shell=True" not in src
    assert "os.system" not in src
    assert "Popen(" not in src


def test_p2202_21_no_network_fetch_pull_surface():
    m = _target()
    flat = {item for args in m.ALLOWED_GIT_ARGUMENTS for item in args}
    assert "fetch" not in flat
    assert "pull" not in flat
    assert "ls-remote" not in flat
    src = TARGET_PATH.read_text(encoding="utf-8")
    for token in ("requests", "urllib", "httpx", "aiohttp", "socket."):
        assert token not in src


def test_p2202_22_no_repository_mutation_command_surface():
    m = _target()
    forbidden = {
        "add", "checkout", "clean", "commit", "fetch", "merge", "pull", "push",
        "rebase", "reset", "restore", "rm", "switch", "tag",
    }
    flat = {item for args in m.ALLOWED_GIT_ARGUMENTS for item in args}
    assert forbidden.isdisjoint(flat)
    for name in CONTRACT_DOC["forbidden_runtime_surface"]:
        assert not hasattr(m, name)


def test_p2202_23_deterministic_machine_readable_output(tmp_path):
    m, repo, expected = _make_repo_and_target(tmp_path)
    a = m.build_verified_snapshot(repo, expected)
    b = m.build_verified_snapshot(repo, copy.deepcopy(expected))
    assert a == b
    encoded = m.canonical_json_bytes(a)
    assert json.loads(encoded.decode("utf-8")) == a
    assert m.canonical_sha256(a) == m.canonical_sha256(b)


def test_p2202_24_snapshot_accepted_by_p2201(tmp_path):
    m, repo, expected = _make_repo_and_target(tmp_path)
    result = m.build_verified_snapshot(repo, expected)
    assert result["verification"]["final_status"] == "PASS"
    p1 = _p2201()
    projected = p1.project_active_state(result["snapshot"])
    assert projected["repository"] == "acme/test"
    assert projected["working_tree_state"] == "CLEAN"
    assert projected["protected_artifacts"]["tracked.txt"]["status"] == "PASS"


def test_p2202_25_expectations_not_mutated(tmp_path):
    m, repo, expected = _make_repo_and_target(tmp_path)
    before = copy.deepcopy(expected)
    m.build_verified_snapshot(repo, expected)
    assert expected == before


def test_p2202_26_failure_cannot_self_repair(tmp_path):
    m, repo, expected = _make_repo_and_target(tmp_path)
    expected["head"] = "e" * 40
    before = _git(repo, "rev-parse", "HEAD")
    result = m.build_verified_snapshot(repo, expected)
    after = _git(repo, "rev-parse", "HEAD")
    assert result["verification"]["final_status"] == "BLOCKED_HEAD_DRIFT"
    assert before == after
    assert before != expected["head"]


def test_p2202_27_e1_td_artifacts_observational_only(tmp_path):
    m, repo, expected = _make_repo_and_target(tmp_path)
    expected["protected_artifacts"] = {"GOVERNANCE/E1-TD-03B.json": "f" * 40}
    result = m.build_verified_snapshot(repo, expected)
    assert result["verification"]["final_status"] == "BLOCKED_PROTECTED_PATH_MISSING"
    assert not hasattr(m, "run_momentum")
    assert not hasattr(m, "compute_pnl")
    assert not hasattr(m, "backtest")


def test_p2202_28_td03b_event_budget_cannot_be_consumed():
    m = _target()
    assert not hasattr(m, "consume_td03b_event")
    assert not hasattr(m, "collect_source_b")
    assert not hasattr(m, "acquire_market_data")
