from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any

CONTRACT = "ATDS_P22_01_PURE_STATE_PROJECTOR_V0_1"

_UNKNOWN = "UNKNOWN"
_WORKTREE_STATES = {"CLEAN", "DIRTY", "UNKNOWN"}
_OID40 = re.compile(r"^[0-9a-fA-F]{40}$")


class P2201Error(ValueError):
    pass


def canonical_json_bytes(payload: Any) -> bytes:
    return (
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
        + b"\n"
    )


def canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def _require_nonempty_string(snapshot: dict[str, Any], key: str) -> str:
    value = snapshot.get(key)
    if not isinstance(value, str) or not value:
        raise P2201Error(f"CRITICAL_FIELD_{key.upper()}")
    return value


def _require_oid(snapshot: dict[str, Any], key: str) -> str:
    value = _require_nonempty_string(snapshot, key)
    if _OID40.fullmatch(value) is None:
        raise P2201Error(f"CRITICAL_FIELD_{key.upper()}_OID")
    return value


def _project_protected_artifacts(value: Any) -> dict[str, dict[str, Any]]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise P2201Error("PROTECTED_ARTIFACTS")

    projected: dict[str, dict[str, Any]] = {}
    for name in sorted(value):
        record = value[name]
        if not isinstance(name, str) or not name or not isinstance(record, dict):
            raise P2201Error("PROTECTED_ARTIFACT_RECORD")

        expected = record.get("expected_blob")
        observed = record.get("observed_blob")

        if expected is not None and (
            not isinstance(expected, str) or _OID40.fullmatch(expected) is None
        ):
            raise P2201Error("PROTECTED_ARTIFACT_EXPECTED_BLOB")
        if observed is not None and (
            not isinstance(observed, str) or _OID40.fullmatch(observed) is None
        ):
            raise P2201Error("PROTECTED_ARTIFACT_OBSERVED_BLOB")

        if expected is None or observed is None:
            status = _UNKNOWN
        elif expected == observed:
            status = "PASS"
        else:
            status = "BLOCKED_PROTECTED_BLOB_DRIFT"

        projected[name] = {
            "expected_blob": expected,
            "observed_blob": observed,
            "status": status,
        }

    return projected


def _project_recovery_status(value: Any, *, head: str, tree: str) -> str:
    if value is None:
        return _UNKNOWN
    if not isinstance(value, dict):
        raise P2201Error("RECOVERY_CHECKPOINT")

    checkpoint_head = value.get("head")
    checkpoint_tree = value.get("tree")

    if checkpoint_head is None or checkpoint_tree is None:
        return _UNKNOWN

    if not isinstance(checkpoint_head, str) or _OID40.fullmatch(checkpoint_head) is None:
        raise P2201Error("RECOVERY_CHECKPOINT_HEAD")
    if not isinstance(checkpoint_tree, str) or _OID40.fullmatch(checkpoint_tree) is None:
        raise P2201Error("RECOVERY_CHECKPOINT_TREE")

    if checkpoint_head != head or checkpoint_tree != tree:
        return "STALE_DERIVED_STATE_DETECTED"
    return "CURRENT"


def _optional(snapshot: dict[str, Any], key: str) -> Any:
    if key not in snapshot or snapshot[key] is None:
        return _UNKNOWN
    return copy.deepcopy(snapshot[key])


def project_active_state(snapshot: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(snapshot, dict):
        raise P2201Error("SNAPSHOT_TYPE")

    repository = _require_nonempty_string(snapshot, "repository")
    if repository.count("/") != 1:
        raise P2201Error("CRITICAL_FIELD_REPOSITORY_FORMAT")

    branch = _require_nonempty_string(snapshot, "branch")
    head = _require_oid(snapshot, "head")
    tree = _require_oid(snapshot, "tree")

    working_tree_state = snapshot.get("working_tree_state", _UNKNOWN)
    if working_tree_state is None:
        working_tree_state = _UNKNOWN
    if working_tree_state not in _WORKTREE_STATES:
        raise P2201Error("WORKING_TREE_STATE")

    protected_artifacts = _project_protected_artifacts(
        snapshot.get("protected_artifacts")
    )
    recovery_checkpoint_status = _project_recovery_status(
        snapshot.get("recovery_checkpoint"),
        head=head,
        tree=tree,
    )

    output = {
        "schema": CONTRACT,
        "repository": repository,
        "branch": branch,
        "head": head,
        "tree": tree,
        "working_tree_state": working_tree_state,
        "protected_artifacts": protected_artifacts,
        "recovery_checkpoint_status": recovery_checkpoint_status,
        "authority_state": _optional(snapshot, "authority_state"),
        "experimental_exposure_state": _optional(
            snapshot, "experimental_exposure_state"
        ),
        "protected_research_state": _optional(
            snapshot, "protected_research_state"
        ),
        "current_frontier": _optional(snapshot, "current_frontier"),
        "last_completed_boundary": _optional(
            snapshot, "last_completed_boundary"
        ),
        "open_blockers": _optional(snapshot, "open_blockers"),
        "hard_stops": _optional(snapshot, "hard_stops"),
        "projection_authority": False,
        "cache_authority": False,
        "reconstructible_from_canonical_inputs": True,
    }

    canonical_json_bytes(output)
    return output
