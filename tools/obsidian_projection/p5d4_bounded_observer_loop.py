from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import tempfile
from pathlib import Path
from typing import Any, Callable, Iterable

from .observer_tick import (
    INPUT_SCHEMA,
    _validate_state,
    make_initial_state,
    one_shot_tick,
)

PLAN_SCHEMA = "ATDS_OBSIDIAN_P5D4_LOOP_PLAN_V0_1"
CHECKPOINT_SCHEMA = "ATDS_OBSIDIAN_P5D4_LOOP_CHECKPOINT_V0_1"
EVENT_SCHEMA = "ATDS_OBSIDIAN_P5D4_LOOP_EVENT_V0_1"
OWNERSHIP_SCHEMA = "ATDS_OBSIDIAN_P5D4_OWNERSHIP_RECORD_V0_1"
EVIDENCE_SCHEMA = "ATDS_OBSIDIAN_P5D4_VERIFIED_PUBLICATION_EVIDENCE_V0_1"
RUN_RESULT_SCHEMA = "ATDS_OBSIDIAN_P5D4_BOUNDED_LOOP_RESULT_V0_1"

_HEAD_RE = re.compile(r"^[0-9a-f]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_PLAN_KEYS = frozenset({
    "schema","loop_id","max_cycles","max_remote_observations",
    "max_evaluations","max_pending_heads","max_consecutive_failures",
    "plan_digest_sha256",
})

class P5D4RuntimeError(RuntimeError):
    pass

class LoopPlanError(P5D4RuntimeError):
    pass

class PersistenceError(P5D4RuntimeError):
    pass

class ReconciliationError(P5D4RuntimeError):
    pass

class OwnershipError(P5D4RuntimeError):
    pass

class OwnershipContended(OwnershipError):
    pass

class QueueCapacityError(P5D4RuntimeError):
    pass

class ControlRootBindingError(P5D4RuntimeError):
    pass

def _canonical_bytes(value: Any) -> bytes:
    try:
        text = json.dumps(
            value, ensure_ascii=False, sort_keys=True,
            separators=(",", ":"), allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise PersistenceError("value is not canonical JSON") from exc
    return (text + "\n").encode("utf-8")

def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()

def _is_int(value: Any, minimum: int) -> bool:
    return not isinstance(value, bool) and isinstance(value, int) and value >= minimum

def _is_head(value: Any) -> bool:
    return isinstance(value, str) and _HEAD_RE.fullmatch(value) is not None

def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None

def _plan_payload(plan: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in plan.items() if key != "plan_digest_sha256"}

def make_loop_plan(
    *,
    loop_id: str,
    max_cycles: int,
    max_remote_observations: int,
    max_evaluations: int,
    max_pending_heads: int,
    max_consecutive_failures: int,
) -> dict[str, Any]:
    plan = {
        "schema": PLAN_SCHEMA,
        "loop_id": loop_id,
        "max_cycles": max_cycles,
        "max_remote_observations": max_remote_observations,
        "max_evaluations": max_evaluations,
        "max_pending_heads": max_pending_heads,
        "max_consecutive_failures": max_consecutive_failures,
    }
    plan["plan_digest_sha256"] = _digest(plan)
    return validate_loop_plan(plan)

def validate_loop_plan(plan: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(plan, dict) or frozenset(plan) != _PLAN_KEYS:
        raise LoopPlanError("loop plan fields mismatch")
    if plan["schema"] != PLAN_SCHEMA:
        raise LoopPlanError("loop plan schema mismatch")
    loop_id = plan["loop_id"]
    if not isinstance(loop_id, str) or not loop_id or loop_id.strip() != loop_id:
        raise LoopPlanError("invalid loop_id")
    for field, minimum in (
        ("max_cycles", 1),
        ("max_remote_observations", 1),
        ("max_evaluations", 0),
        ("max_pending_heads", 1),
        ("max_consecutive_failures", 0),
    ):
        if not _is_int(plan[field], minimum):
            raise LoopPlanError(f"invalid {field}")
    expected = _digest(_plan_payload(plan))
    if plan["plan_digest_sha256"] != expected:
        raise LoopPlanError("loop plan digest mismatch")
    return json.loads(_canonical_bytes(plan).decode("utf-8"))

def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]

def _resolved(path: Path) -> Path:
    try:
        return Path(path).resolve(strict=False)
    except OSError as exc:
        raise P5D4RuntimeError("path resolution unavailable") from exc

def _intersects(first: Path, second: Path) -> bool:
    return (
        first == second
        or first in second.parents
        or second in first.parents
    )

def _normcase_path(path: Path) -> str:
    return os.path.normcase(os.path.normpath(str(path)))

def _path_is_within(path: Path, anchor: Path) -> bool:
    candidate = _normcase_path(path)
    parent = _normcase_path(anchor)
    try:
        return os.path.commonpath([candidate, parent]) == parent
    except ValueError:
        return False

def _existing_chain_has_reparse_point(path: Path) -> bool:
    current = Path(path)
    visited: set[str] = set()
    while True:
        key = _normcase_path(current)
        if key in visited:
            raise ControlRootBindingError("control root path chain loop detected")
        visited.add(key)
        try:
            if current.exists() or current.is_symlink():
                info = os.lstat(current)
                attributes = getattr(info, "st_file_attributes", 0)
                reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
                if current.is_symlink() or (reparse_flag and attributes & reparse_flag):
                    return True
                is_junction = getattr(current, "is_junction", None)
                if callable(is_junction) and is_junction():
                    return True
        except OSError as exc:
            raise ControlRootBindingError(
                "control root path chain inspection unavailable"
            ) from exc
        if current.parent == current:
            return False
        current = current.parent

def _userprofile_root() -> Path:
    value = os.environ.get("USERPROFILE")
    if not isinstance(value, str) or not value.strip():
        raise ControlRootBindingError("USERPROFILE unavailable")
    profile = Path(value)
    if not profile.is_absolute():
        raise ControlRootBindingError("USERPROFILE is not absolute")
    return _resolved(profile)

def canonical_production_control_root() -> Path:
    return _userprofile_root() / "ATDS-CONTROL" / "OBSIDIAN-PROJECTION" / "P5D4"

def _qualification_control_anchor() -> Path:
    return _userprofile_root() / "ATDS-CONTROL" / "_QUALIFICATION"

def resolve_and_validate_control_root(root: Path) -> Path:
    requested = Path(root)
    if not requested.is_absolute():
        raise ControlRootBindingError("control root must be absolute")
    if _existing_chain_has_reparse_point(requested):
        raise ControlRootBindingError(
            "control root path chain contains reparse point"
        )

    resolved = _resolved(requested)
    canonical = _resolved(canonical_production_control_root())
    qualification = _resolved(_qualification_control_anchor())
    temp_root = _resolved(Path(tempfile.gettempdir()))

    requested_norm = _normcase_path(resolved)
    canonical_norm = _normcase_path(canonical)
    is_production = requested_norm == canonical_norm
    is_qualification = _path_is_within(resolved, qualification)
    is_temp = _path_is_within(resolved, temp_root)

    if not (is_production or is_qualification or is_temp):
        raise ControlRootBindingError(
            "control root is outside canonical or synthetic qualification namespaces"
        )

    if is_production:
        localappdata = os.environ.get("LOCALAPPDATA")
        appdata = os.environ.get("APPDATA")
        for forbidden in (localappdata, appdata):
            if isinstance(forbidden, str) and forbidden.strip():
                if _path_is_within(canonical, _resolved(Path(forbidden))):
                    raise ControlRootBindingError(
                        "production control root depends on AppData"
                    )
        lowered = _normcase_path(canonical)
        if (
            os.path.normcase("\\packages\\") in lowered
            or os.path.normcase("\\localcache\\") in lowered
        ):
            raise ControlRootBindingError(
                "production control root is Store-redirectable"
            )
        return canonical

    return resolved

def _validate_control_root(
    root: Path,
    *,
    forbidden_roots: Iterable[Path] = (),
) -> Path:
    resolved = resolve_and_validate_control_root(root)
    protected = (_resolved(_repo_root()),) + tuple(_resolved(x) for x in forbidden_roots)
    if any(_intersects(resolved, item) for item in protected):
        raise P5D4RuntimeError("control root intersects protected root")
    try:
        resolved.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise P5D4RuntimeError("control root unavailable") from exc
    if not resolved.is_dir():
        raise P5D4RuntimeError("control root is not a directory")
    return resolved

def _write_durable(path: Path, raw: bytes, *, exclusive: bool = False) -> None:
    flags = os.O_WRONLY | os.O_CREAT
    flags |= os.O_EXCL if exclusive else os.O_TRUNC
    fd = os.open(str(path), flags, 0o600)
    try:
        with os.fdopen(fd, "wb", closefd=False) as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(fd)
def acquire_ownership(
    control_root: Path,
    *,
    loop_id: str,
    owner_token: str,
) -> dict[str, Any]:
    root = _validate_control_root(control_root)
    if not isinstance(loop_id, str) or not loop_id:
        raise OwnershipError("invalid loop id")
    if not isinstance(owner_token, str) or not owner_token:
        raise OwnershipError("invalid owner token")
    record = {
        "schema": OWNERSHIP_SCHEMA,
        "loop_id": loop_id,
        "owner_token": owner_token,
    }
    path = root / "ownership.lock"
    try:
        _write_durable(path, _canonical_bytes(record), exclusive=True)
    except FileExistsError as exc:
        raise OwnershipContended("ownership already held") from exc
    return record

def release_ownership(control_root: Path, ownership: dict[str, Any]) -> None:
    root = _validate_control_root(control_root)
    path = root / "ownership.lock"
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise OwnershipError("ownership record unavailable") from exc
    try:
        current = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise OwnershipError("ownership record invalid") from exc
    if raw != _canonical_bytes(current) or current != ownership:
        raise OwnershipError("ownership mismatch")
    try:
        path.unlink()
    except OSError as exc:
        raise OwnershipError("ownership release failed") from exc

def _event_record_digest(record: dict[str, Any]) -> str:
    body = dict(record)
    body.pop("record_digest_sha256", None)
    return _digest(body)

def load_event_log(control_root: Path) -> list[dict[str, Any]]:
    root = _validate_control_root(control_root)
    path = root / "observer-events.jsonl"
    if not path.exists():
        return []
    raw = path.read_bytes()
    if not raw:
        return []
    if not raw.endswith(b"\n"):
        raise PersistenceError("event log has unterminated record")
    records: list[dict[str, Any]] = []
    previous_digest: str | None = None
    expected_sequence = 1
    for line in raw.splitlines(keepends=True):
        try:
            record = json.loads(line.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PersistenceError("event log record invalid") from exc
        if line != _canonical_bytes(record):
            raise PersistenceError("event log record noncanonical")
        required = {
            "schema","sequence","loop_id","cycle_index","normalized_input",
            "p5d2_audit","previous_state_digest_sha256",
            "next_state_digest_sha256","previous_record_digest_sha256",
            "record_digest_sha256","record_origin",
        }
        if set(record) != required or record.get("schema") != EVENT_SCHEMA:
            raise PersistenceError("event log fields mismatch")
        if record["record_origin"] not in {
            "LIVE_BOUNDED_LOOP",
            "EVIDENCE_RECONSTRUCTION",
        }:
            raise PersistenceError("event log record origin invalid")
        if record["sequence"] != expected_sequence:
            raise PersistenceError("event log sequence mismatch")
        if record["previous_record_digest_sha256"] != previous_digest:
            raise PersistenceError("event log hash chain mismatch")
        if record["record_digest_sha256"] != _event_record_digest(record):
            raise PersistenceError("event log digest mismatch")
        event = record["normalized_input"]
        audit = record["p5d2_audit"]
        if (
            not isinstance(event, dict)
            or event.get("sequence") != expected_sequence
            or not isinstance(audit, dict)
            or audit.get("sequence") != expected_sequence
            or audit.get("next_state_digest") != record["next_state_digest_sha256"]
            or audit.get("previous_state_digest") != record["previous_state_digest_sha256"]
        ):
            raise PersistenceError("event log P5-D2 binding mismatch")
        previous_digest = record["record_digest_sha256"]
        expected_sequence += 1
        records.append(record)
    return records

def load_checkpoint(control_root: Path) -> dict[str, Any] | None:
    root = _validate_control_root(control_root)
    path = root / "observer-checkpoint.json"
    if not path.exists():
        return None
    raw = path.read_bytes()
    try:
        checkpoint = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PersistenceError("checkpoint invalid") from exc
    if raw != _canonical_bytes(checkpoint):
        raise PersistenceError("checkpoint noncanonical")
    required = {
        "schema","loop_plan_digest_sha256","observer_state",
        "observer_state_digest_sha256","last_event_sequence",
        "last_event_digest_sha256","checkpoint_generation",
    }
    if set(checkpoint) != required or checkpoint.get("schema") != CHECKPOINT_SCHEMA:
        raise PersistenceError("checkpoint fields mismatch")
    state = checkpoint["observer_state"]
    try:
        _validate_state(state)
    except Exception as exc:
        raise PersistenceError("checkpoint observer state invalid") from exc
    if checkpoint["observer_state_digest_sha256"] != _digest(state):
        raise PersistenceError("checkpoint state digest mismatch")
    if checkpoint["last_event_sequence"] != state["last_event_sequence"]:
        raise PersistenceError("checkpoint sequence mismatch")
    if not _is_int(checkpoint["checkpoint_generation"], 1):
        raise PersistenceError("checkpoint generation invalid")
    if not _is_sha256(checkpoint["loop_plan_digest_sha256"]):
        raise PersistenceError("checkpoint plan digest invalid")
    if not _is_sha256(checkpoint["last_event_digest_sha256"]):
        raise PersistenceError("checkpoint event digest invalid")
    return checkpoint

def _checkpoint_value(
    *,
    plan: dict[str, Any],
    state: dict[str, Any],
    event_digest: str,
    generation: int,
) -> dict[str, Any]:
    return {
        "schema": CHECKPOINT_SCHEMA,
        "loop_plan_digest_sha256": plan["plan_digest_sha256"],
        "observer_state": state,
        "observer_state_digest_sha256": _digest(state),
        "last_event_sequence": state["last_event_sequence"],
        "last_event_digest_sha256": event_digest,
        "checkpoint_generation": generation,
    }

def _write_checkpoint(
    root: Path,
    *,
    plan: dict[str, Any],
    state: dict[str, Any],
    event_digest: str,
) -> dict[str, Any]:
    existing = load_checkpoint(root)
    generation = 1 if existing is None else existing["checkpoint_generation"] + 1
    value = _checkpoint_value(
        plan=plan, state=state, event_digest=event_digest, generation=generation)
    temp = root / "observer-checkpoint.tmp"
    final = root / "observer-checkpoint.json"
    _write_durable(temp, _canonical_bytes(value))
    try:
        os.replace(str(temp), str(final))
    except OSError as exc:
        raise PersistenceError("checkpoint atomic replace failed") from exc
    verified = load_checkpoint(root)
    if verified != value:
        raise PersistenceError("checkpoint read-after-write mismatch")
    return verified
def _append_event(root: Path, record: dict[str, Any]) -> None:
    path = root / "observer-events.jsonl"
    raw = _canonical_bytes(record)
    try:
        with path.open("ab") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except OSError as exc:
        raise PersistenceError("event append failed") from exc

def _would_append_queue(state: dict[str, Any], event: dict[str, Any]) -> bool:
    return (
        event.get("event_type") == "REMOTE_HEAD_OBSERVED"
        and event.get("transition_class") in {"INITIAL", "FAST_FORWARD"}
        and event.get("observed_head") not in state.get("pending_heads", [])
    )

def persist_tick(
    *,
    control_root: Path,
    plan: dict[str, Any],
    previous_state: dict[str, Any],
    normalized_input: dict[str, Any],
    loop_id: str,
    cycle_index: int,
    record_origin: str = "LIVE_BOUNDED_LOOP",
    fault_injector: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    plan = validate_loop_plan(plan)
    root = _validate_control_root(control_root)
    try:
        _validate_state(previous_state)
    except Exception as exc:
        raise PersistenceError("previous observer state invalid") from exc
    if loop_id != plan["loop_id"]:
        raise PersistenceError("loop id mismatch")
    if record_origin not in {"LIVE_BOUNDED_LOOP", "EVIDENCE_RECONSTRUCTION"}:
        raise PersistenceError("record origin invalid")
    if _would_append_queue(previous_state, normalized_input):
        if len(previous_state["pending_heads"]) >= plan["max_pending_heads"]:
            raise QueueCapacityError("pending queue capacity exhausted")

    log = load_event_log(root)
    if log:
        tail = log[-1]
        if tail["sequence"] != previous_state["last_event_sequence"]:
            raise PersistenceError("event log/state sequence mismatch")
        if tail["next_state_digest_sha256"] != _digest(previous_state):
            raise PersistenceError("event log/state digest mismatch")
    elif previous_state["last_event_sequence"] != 0:
        raise PersistenceError("noninitial state has no event history")
    tick = one_shot_tick(previous_state, normalized_input)
    audit = tick["audit"]
    previous_record_digest = log[-1]["record_digest_sha256"] if log else None
    record = {
        "schema": EVENT_SCHEMA,
        "sequence": normalized_input["sequence"],
        "loop_id": loop_id,
        "cycle_index": cycle_index,
        "normalized_input": normalized_input,
        "p5d2_audit": audit,
        "previous_state_digest_sha256": audit["previous_state_digest"],
        "next_state_digest_sha256": audit["next_state_digest"],
        "previous_record_digest_sha256": previous_record_digest,
        "record_origin": record_origin,
    }
    record["record_digest_sha256"] = _event_record_digest(record)
    _append_event(root, record)
    if fault_injector is not None:
        fault_injector("AFTER_EVENT_DURABLE_BEFORE_CHECKPOINT_REPLACE")
    checkpoint = _write_checkpoint(
        root,
        plan=plan,
        state=tick["next_state"],
        event_digest=record["record_digest_sha256"],
    )
    return {
        "tick_result": tick,
        "event_record": record,
        "checkpoint": checkpoint,
    }

def _replay_record(
    state: dict[str, Any],
    record: dict[str, Any],
) -> dict[str, Any]:
    if record["previous_state_digest_sha256"] != _digest(state):
        raise ReconciliationError("replay previous-state digest mismatch")
    try:
        tick = one_shot_tick(state, record["normalized_input"])
    except Exception as exc:
        raise ReconciliationError("P5-D2 replay rejected") from exc
    if tick["audit"] != record["p5d2_audit"]:
        raise ReconciliationError("replay audit mismatch")
    if _digest(tick["next_state"]) != record["next_state_digest_sha256"]:
        raise ReconciliationError("replay next-state digest mismatch")
    return tick["next_state"]

def _validate_evidence(
    verified_current_head: str,
    evidence: dict[str, Any] | None,
) -> dict[str, Any]:
    if not _is_head(verified_current_head):
        raise ReconciliationError("verified CURRENT head invalid")
    if not isinstance(evidence, dict):
        raise ReconciliationError("verified publication evidence required")
    required = {
        "schema","candidate_head","status","transaction_plan_digest_sha256",
        "physical_receipt_digest_sha256","logical_receipt_digest_sha256",
        "p5d2_promotion_confirmed_emitted",
    }
    if set(evidence) != required or evidence.get("schema") != EVIDENCE_SCHEMA:
        raise ReconciliationError("publication evidence fields mismatch")
    if evidence["candidate_head"] != verified_current_head:
        raise ReconciliationError("publication evidence head mismatch")
    if evidence["status"] != "PASS_LIVE_PUBLICATION_CONFIRMED":
        raise ReconciliationError("publication evidence status mismatch")
    for field in (
        "transaction_plan_digest_sha256",
        "physical_receipt_digest_sha256",
        "logical_receipt_digest_sha256",
    ):
        if not _is_sha256(evidence[field]):
            raise ReconciliationError("publication evidence digest invalid")
    if evidence["p5d2_promotion_confirmed_emitted"] is not True:
        raise ReconciliationError("promotion confirmation evidence missing")
    return evidence

def reconstruct_from_verified_publication_evidence(
    *,
    control_root: Path,
    plan: dict[str, Any],
    verified_current_head: str,
    promotion_evidence: dict[str, Any] | None,
) -> dict[str, Any]:
    plan = validate_loop_plan(plan)
    root = _validate_control_root(control_root)
    if load_checkpoint(root) is not None or load_event_log(root):
        raise ReconciliationError("evidence reconstruction requires empty control state")
    _validate_evidence(verified_current_head, promotion_evidence)
    state = make_initial_state()
    events = (
        {
            "schema": INPUT_SCHEMA, "event_type": "REMOTE_HEAD_OBSERVED",
            "sequence": 1, "observed_head": verified_current_head,
            "transition_class": "INITIAL", "candidate_head": None, "failure_code": None,
        },
        {
            "schema": INPUT_SCHEMA, "event_type": "EVALUATION_STARTED",
            "sequence": 2, "observed_head": None, "transition_class": None,
            "candidate_head": verified_current_head, "failure_code": None,
        },
        {
            "schema": INPUT_SCHEMA, "event_type": "EVALUATION_PASSED",
            "sequence": 3, "observed_head": None, "transition_class": None,
            "candidate_head": verified_current_head, "failure_code": None,
        },
        {
            "schema": INPUT_SCHEMA, "event_type": "PROMOTION_CONFIRMED",
            "sequence": 4, "observed_head": None, "transition_class": None,
            "candidate_head": verified_current_head, "failure_code": None,
        },
    )
    for event in events:
        persisted = persist_tick(
            control_root=root,
            plan=plan,
            previous_state=state,
            normalized_input=event,
            loop_id=plan["loop_id"],
            cycle_index=0,
            record_origin="EVIDENCE_RECONSTRUCTION",
        )
        state = persisted["tick_result"]["next_state"]
    return {
        "status": "PASS_RECONSTRUCTED_VERIFIED_PUBLICATION_EVIDENCE",
        "observer_state": state,
        "evidence": promotion_evidence,
    }

def reconcile_control_state(
    *,
    control_root: Path,
    plan: dict[str, Any],
    verified_current_head: str | None,
    promotion_evidence: dict[str, Any] | None,
) -> dict[str, Any]:
    plan = validate_loop_plan(plan)
    root = _validate_control_root(control_root)
    log = load_event_log(root)
    checkpoint = load_checkpoint(root)

    if checkpoint is None and not log:
        if verified_current_head is None:
            return {
                "status": "PASS_CANONICAL_INITIAL_STATE",
                "observer_state": make_initial_state(),
            }
        return reconstruct_from_verified_publication_evidence(
            control_root=root,
            plan=plan,
            verified_current_head=verified_current_head,
            promotion_evidence=promotion_evidence,
        )

    if checkpoint is None:
        if len(log) != 1:
            raise ReconciliationError("event log too far ahead without checkpoint")
        base = make_initial_state()
        next_state = _replay_record(base, log[0])
        _write_checkpoint(
            root,
            plan=plan,
            state=next_state,
            event_digest=log[0]["record_digest_sha256"],
        )
        return {
            "status": "PASS_RECONCILED_ONE_RECORD_AHEAD",
            "observer_state": next_state,
        }

    if checkpoint["loop_plan_digest_sha256"] != plan["plan_digest_sha256"]:
        raise ReconciliationError("checkpoint loop-plan mismatch")
    cp_seq = checkpoint["last_event_sequence"]
    if cp_seq > len(log):
        raise ReconciliationError("checkpoint ahead of event log")
    delta = len(log) - cp_seq
    if delta > 1:
        raise ReconciliationError("event log more than one record ahead")
    state = checkpoint["observer_state"]
    if cp_seq:
        tail_at_checkpoint = log[cp_seq - 1]
        if checkpoint["last_event_digest_sha256"] != tail_at_checkpoint["record_digest_sha256"]:
            raise ReconciliationError("checkpoint event digest mismatch")
        if checkpoint["observer_state_digest_sha256"] != tail_at_checkpoint["next_state_digest_sha256"]:
            raise ReconciliationError("checkpoint/log state digest mismatch")
    if delta == 1:
        record = log[-1]
        state = _replay_record(state, record)
        _write_checkpoint(
            root,
            plan=plan,
            state=state,
            event_digest=record["record_digest_sha256"],
        )
        status = "PASS_RECONCILED_ONE_RECORD_AHEAD"
    else:
        status = "PASS_RECONCILED_ALIGNED"

    live = state["live_projection_head"]
    if verified_current_head is None:
        if live is not None:
            raise ReconciliationError("checkpoint live head has no physical CURRENT")
    elif live != verified_current_head:
        raise ReconciliationError("physical CURRENT differs from checkpoint live head")

    return {"status": status, "observer_state": state}

def _normalized_event(
    state: dict[str, Any],
    event_type: str,
    *,
    candidate_head: str | None = None,
    failure_code: str | None = None,
) -> dict[str, Any]:
    return {
        "schema": INPUT_SCHEMA,
        "event_type": event_type,
        "sequence": state["last_event_sequence"] + 1,
        "observed_head": None,
        "transition_class": None,
        "candidate_head": candidate_head,
        "failure_code": failure_code,
    }

def _write_run_result(root: Path, result: dict[str, Any]) -> None:
    temp = root / "last-run.tmp"
    final = root / "last-run.json"
    _write_durable(temp, _canonical_bytes(result))
    try:
        os.replace(str(temp), str(final))
    except OSError as exc:
        raise PersistenceError("run-result replace failed") from exc

def _base_run_result(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": RUN_RESULT_SCHEMA,
        "loop_id": plan["loop_id"],
        "loop_plan_digest_sha256": plan["plan_digest_sha256"],
        "terminal_reason": None,
        "cycles_started": 0,
        "remote_observations": 0,
        "evaluations_started": 0,
        "consecutive_failures": 0,
        "observer_state": None,
        "automatic_promotion_authorized": False,
        "production_write_authorized": False,
    }

def run_bounded_loop(
    *,
    plan: dict[str, Any],
    control_root: Path,
    observation_adapter: Callable[[dict[str, Any]], dict[str, Any]],
    evaluation_adapter: Callable[[str, dict[str, Any]], dict[str, Any]],
    verified_current_head: str | None,
    promotion_evidence: dict[str, Any] | None,
    forbidden_roots: Iterable[Path] = (),
    owner_token: str,
) -> dict[str, Any]:
    plan = validate_loop_plan(plan)
    root = _validate_control_root(control_root, forbidden_roots=forbidden_roots)
    result = _base_run_result(plan)
    try:
        ownership = acquire_ownership(
            root, loop_id=plan["loop_id"], owner_token=owner_token)
    except OwnershipContended:
        result["terminal_reason"] = "LOCK_CONTENDED"
        return result

    state: dict[str, Any] | None = None
    try:
        reconciled = reconcile_control_state(
            control_root=root,
            plan=plan,
            verified_current_head=verified_current_head,
            promotion_evidence=promotion_evidence,
        )
        state = reconciled["observer_state"]

        if state["observer_phase"] == "CANDIDATE_PENDING":
            result["terminal_reason"] = "PROMOTION_AUTHORITY_REQUIRED"
        elif state["observer_phase"] == "BLOCKED":
            result["terminal_reason"] = "BLOCKED_REQUIRES_ADJUDICATION"
        elif state["observer_phase"] == "EVALUATING":
            result["terminal_reason"] = "RECONCILIATION_REQUIRED"
        elif state["observer_phase"] == "STOPPED":
            result["terminal_reason"] = "SHUTDOWN_REQUESTED"

        for cycle_index in range(1, plan["max_cycles"] + 1):
            if result["terminal_reason"] is not None:
                break
            result["cycles_started"] += 1

            if state["pending_heads"]:
                if result["evaluations_started"] >= plan["max_evaluations"]:
                    result["terminal_reason"] = "BOUND_REACHED"
                    break
                candidate = state["pending_heads"][0]
                started = persist_tick(
                    control_root=root,
                    plan=plan,
                    previous_state=state,
                    normalized_input=_normalized_event(
                        state, "EVALUATION_STARTED", candidate_head=candidate),
                    loop_id=plan["loop_id"],
                    cycle_index=cycle_index,
                )
                state = started["tick_result"]["next_state"]
                result["evaluations_started"] += 1
                outcome = evaluation_adapter(candidate, started["tick_result"])
                if not isinstance(outcome, dict):
                    raise P5D4RuntimeError("evaluation adapter result invalid")
                classification = outcome.get("outcome")
                failure_code = outcome.get("failure_code")
                if classification == "QUALIFIED":
                    finished = persist_tick(
                        control_root=root, plan=plan, previous_state=state,
                        normalized_input=_normalized_event(
                            state, "EVALUATION_PASSED", candidate_head=candidate),
                        loop_id=plan["loop_id"], cycle_index=cycle_index)
                    state = finished["tick_result"]["next_state"]
                    result["terminal_reason"] = "PROMOTION_AUTHORITY_REQUIRED"
                elif classification == "REJECTED":
                    if not isinstance(failure_code, str) or not failure_code:
                        raise P5D4RuntimeError("rejected evaluation requires failure code")
                    finished = persist_tick(
                        control_root=root, plan=plan, previous_state=state,
                        normalized_input=_normalized_event(
                            state, "EVALUATION_FAILED",
                            candidate_head=candidate, failure_code=failure_code),
                        loop_id=plan["loop_id"], cycle_index=cycle_index)
                    state = finished["tick_result"]["next_state"]
                    result["terminal_reason"] = "BLOCKED_REQUIRES_ADJUDICATION"
                elif classification == "BLOCKED":
                    result["terminal_reason"] = "BLOCKED_REQUIRES_ADJUDICATION"
                else:
                    raise P5D4RuntimeError("evaluation outcome invalid")
                continue

            if result["remote_observations"] >= plan["max_remote_observations"]:
                result["terminal_reason"] = "BOUND_REACHED"
                break
            event = observation_adapter(state)
            result["remote_observations"] += 1
            observed = persist_tick(
                control_root=root,
                plan=plan,
                previous_state=state,
                normalized_input=event,
                loop_id=plan["loop_id"],
                cycle_index=cycle_index,
            )
            state = observed["tick_result"]["next_state"]
            if event.get("event_type") == "REMOTE_OBSERVATION_FAILED":
                result["consecutive_failures"] += 1
                if result["consecutive_failures"] > plan["max_consecutive_failures"]:
                    result["terminal_reason"] = "BOUND_REACHED"
                    break
            else:
                result["consecutive_failures"] = 0

            if state["observer_phase"] == "BLOCKED":
                result["terminal_reason"] = "BLOCKED_REQUIRES_ADJUDICATION"
                break
            if (
                observed["tick_result"]["decision"]["action"] == "NOOP"
                and not state["pending_heads"]
            ):
                result["terminal_reason"] = "NO_PENDING_WORK"
                break

        if result["terminal_reason"] is None:
            result["terminal_reason"] = "BOUND_REACHED"
        result["observer_state"] = state
        _write_run_result(root, result)
        return result
    except QueueCapacityError:
        result["terminal_reason"] = "QUEUE_CAPACITY_REQUIRES_ADJUDICATION"
        result["observer_state"] = state
        _write_run_result(root, result)
        return result
    except ReconciliationError:
        result["terminal_reason"] = "RECONCILIATION_REQUIRED"
        result["observer_state"] = state
        _write_run_result(root, result)
        return result
    except Exception:
        result["terminal_reason"] = "FATAL_INCONSISTENCY"
        result["observer_state"] = state
        _write_run_result(root, result)
        return result
    finally:
        release_ownership(root, ownership)
