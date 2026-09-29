from __future__ import annotations

import copy
import importlib.util
import json
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/P22-01-PURE-STATE-PROJECTOR-CONTRACT-V0.1.json"
TARGET_PATH = ROOT / "tools/p22_01_pure_state_projector.py"

CONTRACT_DOC = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
RUNTIME_CONTRACT = "ATDS_P22_01_PURE_STATE_PROJECTOR_V0_1"

assert CONTRACT_DOC["schema"] == "ATDS_P22_01_PURE_STATE_PROJECTOR_CONTRACT_V0_1"
assert [x[0] for x in CONTRACT_DOC["test_cases"]] == [f"P2201-{i:02d}" for i in range(1, 19)]


def _target():
    if not TARGET_PATH.is_file():
        pytest.fail("P22_01_TARGET_ABSENT_EXPECTED_RED", pytrace=False)
    spec = importlib.util.spec_from_file_location("p22_01_under_test", TARGET_PATH)
    if spec is None or spec.loader is None:
        pytest.fail("P22_01_TARGET_UNLOADABLE_EXPECTED_RED", pytrace=False)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _base_snapshot():
    return {
        "repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
        "branch": "integration/system-v1",
        "head": "0" * 40,
        "tree": "1" * 40,
        "working_tree_state": "CLEAN",
        "protected_artifacts": {
            "phase22_contract": {
                "expected_blob": "2" * 40,
                "observed_blob": "2" * 40,
            },
            "phase22_adoption": {
                "expected_blob": "3" * 40,
                "observed_blob": "4" * 40,
            },
            "td03b": {
                "expected_blob": "5" * 40,
                "observed_blob": None,
            },
        },
        "recovery_checkpoint": {
            "head": "0" * 40,
            "tree": "1" * 40,
            "claimed_frontier": "P22-01",
        },
        "authority_state": {"P22_01": "AUTHORIZED"},
        "experimental_exposure_state": {"E1_OOS": "PERMANENTLY_EXPOSED"},
        "protected_research_state": {
            "E1_TD_03B": {
                "event_budget": "0 / 1",
                "events_consumed": 0,
                "status": "WAITING_SOURCE_CONTINUATION",
            }
        },
        "current_frontier": "P22-01",
        "last_completed_boundary": "PHASE_22_CONTRACT_ADOPTION",
        "open_blockers": [],
        "hard_stops": ["P22-02_NOT_AUTHORIZED"],
    }


def test_p2201_01_runtime_contract_and_surface():
    m = _target()
    assert m.CONTRACT == RUNTIME_CONTRACT
    assert set(CONTRACT_DOC["required_runtime_surface"]).issubset(set(dir(m)))


def test_p2201_02_deterministic_projection_and_digest():
    m = _target()
    a = _base_snapshot()
    b = copy.deepcopy(a)
    pa = m.project_active_state(a)
    pb = m.project_active_state(b)
    assert pa == pb
    assert m.canonical_sha256(pa) == m.canonical_sha256(pb)


def test_p2201_03_repository_identity_explicit():
    m = _target()
    out = m.project_active_state(_base_snapshot())
    assert out["repository"] == "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"


def test_p2201_04_branch_head_tree_explicit():
    m = _target()
    out = m.project_active_state(_base_snapshot())
    assert out["branch"] == "integration/system-v1"
    assert out["head"] == "0" * 40
    assert out["tree"] == "1" * 40


def test_p2201_05_missing_optional_facts_remain_unknown():
    m = _target()
    snapshot = {k: v for k, v in _base_snapshot().items() if k in {"repository", "branch", "head", "tree"}}
    out = m.project_active_state(snapshot)
    for key in (
        "working_tree_state",
        "authority_state",
        "experimental_exposure_state",
        "protected_research_state",
        "current_frontier",
        "last_completed_boundary",
        "open_blockers",
        "hard_stops",
        "recovery_checkpoint_status",
    ):
        assert out[key] == "UNKNOWN"
    assert out["protected_artifacts"] == {}


@pytest.mark.parametrize("state", ["CLEAN", "DIRTY", "UNKNOWN"])
def test_p2201_06_working_tree_state_preserved(state):
    m = _target()
    snapshot = _base_snapshot()
    snapshot["working_tree_state"] = state
    assert m.project_active_state(snapshot)["working_tree_state"] == state


def test_p2201_07_invalid_working_tree_state_fails_closed():
    m = _target()
    snapshot = _base_snapshot()
    snapshot["working_tree_state"] = "PROBABLY_CLEAN"
    with pytest.raises(m.P2201Error, match="WORKING_TREE_STATE"):
        m.project_active_state(snapshot)


def test_p2201_08_protected_artifact_statuses_derived_without_repair():
    m = _target()
    out = m.project_active_state(_base_snapshot())
    assert out["protected_artifacts"]["phase22_contract"]["status"] == "PASS"
    assert out["protected_artifacts"]["phase22_adoption"]["status"] == "BLOCKED_PROTECTED_BLOB_DRIFT"
    assert out["protected_artifacts"]["td03b"]["status"] == "UNKNOWN"
    assert out["protected_artifacts"]["phase22_adoption"]["observed_blob"] == "4" * 40


def test_p2201_09_stale_recovery_checkpoint_detected():
    m = _target()
    snapshot = _base_snapshot()
    snapshot["recovery_checkpoint"]["head"] = "9" * 40
    assert m.project_active_state(snapshot)["recovery_checkpoint_status"] == "STALE_DERIVED_STATE_DETECTED"


def test_p2201_10_matching_recovery_checkpoint_not_false_stale():
    m = _target()
    assert m.project_active_state(_base_snapshot())["recovery_checkpoint_status"] == "CURRENT"


def test_p2201_11_projection_and_cache_non_authoritative():
    m = _target()
    out = m.project_active_state(_base_snapshot())
    assert out["projection_authority"] is False
    assert out["cache_authority"] is False
    assert out["reconstructible_from_canonical_inputs"] is True


def test_p2201_12_protected_research_surfaced_without_mutation_or_consumption():
    m = _target()
    snapshot = _base_snapshot()
    before = copy.deepcopy(snapshot["protected_research_state"])
    out = m.project_active_state(snapshot)
    assert out["protected_research_state"] == before
    assert snapshot["protected_research_state"] == before
    assert not hasattr(m, "consume_td03b_event")


def test_p2201_13_authority_explicit_and_missing_authority_unknown():
    m = _target()
    snapshot = _base_snapshot()
    assert m.project_active_state(snapshot)["authority_state"] == {"P22_01": "AUTHORIZED"}
    snapshot.pop("authority_state")
    assert m.project_active_state(snapshot)["authority_state"] == "UNKNOWN"


@pytest.mark.parametrize(
    "mutation",
    [
        lambda s: s.pop("repository"),
        lambda s: s.update(repository=""),
        lambda s: s.update(branch=""),
        lambda s: s.update(head="abc"),
        lambda s: s.update(tree="xyz"),
    ],
)
def test_p2201_14_malformed_critical_input_fails_closed(mutation):
    m = _target()
    snapshot = _base_snapshot()
    mutation(snapshot)
    with pytest.raises(m.P2201Error):
        m.project_active_state(snapshot)


def test_p2201_15_canonical_json_forbids_nonfinite():
    m = _target()
    with pytest.raises(ValueError):
        m.canonical_json_bytes({"x": math.nan})
    with pytest.raises(ValueError):
        m.canonical_json_bytes({"x": math.inf})


def test_p2201_16_no_repository_mutation_command_or_network_surface():
    m = _target()
    for name in CONTRACT_DOC["forbidden_runtime_surface"]:
        assert not hasattr(m, name)
    src = TARGET_PATH.read_text(encoding="utf-8")
    forbidden_tokens = (
        "subprocess",
        "os.system",
        "requests",
        "urllib",
        "httpx",
        "aiohttp",
        "socket.",
        ".write_text(",
        ".unlink(",
        ".rename(",
        ".replace(",
    )
    assert all(token not in src for token in forbidden_tokens)


def test_p2201_17_input_snapshot_not_mutated():
    m = _target()
    snapshot = _base_snapshot()
    before = copy.deepcopy(snapshot)
    m.project_active_state(snapshot)
    assert snapshot == before


def test_p2201_18_machine_readable_frozen_output_surface():
    m = _target()
    out = m.project_active_state(_base_snapshot())
    assert set(CONTRACT_DOC["required_output"]) == set(out)
    encoded = m.canonical_json_bytes(out)
    assert isinstance(encoded, bytes)
    assert json.loads(encoded.decode("utf-8")) == out
