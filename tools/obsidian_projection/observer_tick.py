from __future__ import annotations

import hashlib
import json
import re
from typing import Any


class ObserverTickError(RuntimeError):
    pass


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
EXPECTED_BRANCH = "integration/system-v1"

STATE_SCHEMA = "ATDS_OBSIDIAN_OBSERVER_STATE_V0_1"
INPUT_SCHEMA = "ATDS_OBSIDIAN_OBSERVER_INPUT_V0_1"
DECISION_SCHEMA = "ATDS_OBSIDIAN_OBSERVER_DECISION_V0_1"
EVENT_SCHEMA = "ATDS_OBSIDIAN_OBSERVER_EVENT_V0_1"
RESULT_SCHEMA = "ATDS_OBSIDIAN_ONE_SHOT_TICK_RESULT_V0_1"

OBSERVER_PHASES = frozenset(
    {
        "IDLE",
        "CANDIDATE_PENDING",
        "EVALUATING",
        "BLOCKED",
        "STOPPED",
    }
)
REMOTE_FRESHNESS = frozenset({"KNOWN", "UNKNOWN"})
PROJECTION_STATES = frozenset(
    {
        "CURRENT",
        "STALE",
        "BLOCKED",
        "ORPHAN",
        "MISSING",
    }
)
EVENT_TYPES = frozenset(
    {
        "BOOTSTRAP",
        "REMOTE_HEAD_OBSERVED",
        "REMOTE_OBSERVATION_FAILED",
        "EVALUATION_STARTED",
        "EVALUATION_PASSED",
        "EVALUATION_FAILED",
        "PROMOTION_CONFIRMED",
        "PROMOTION_FAILED",
        "LOCK_CONTENDED",
        "SHUTDOWN_REQUESTED",
    }
)
TRANSITION_CLASSES = frozenset(
    {
        "INITIAL",
        "SAME",
        "FAST_FORWARD",
        "NON_FAST_FORWARD",
        "UNKNOWN",
    }
)

_STATE_KEYS = frozenset(
    {
        "schema",
        "repository",
        "branch",
        "observer_phase",
        "remote_freshness",
        "latest_observed_head",
        "last_qualified_head",
        "live_projection_head",
        "projection_state",
        "pending_heads",
        "blocked_head",
        "last_failure_code",
        "last_event_sequence",
    }
)
_INPUT_KEYS = frozenset(
    {
        "schema",
        "event_type",
        "sequence",
        "observed_head",
        "transition_class",
        "candidate_head",
        "failure_code",
    }
)

_HEAD_RE = re.compile(r"^[0-9a-f]{40}$")


def _canonical_json_bytes(value: Any) -> bytes:
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ObserverTickError(
            "value is not canonical JSON"
        ) from exc
    return (encoded + "\n").encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(
        _canonical_json_bytes(value)
    ).hexdigest()


def _clone(value: Any) -> Any:
    try:
        return json.loads(
            _canonical_json_bytes(value).decode("utf-8")
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ObserverTickError(
            "canonical clone failed"
        ) from exc


def _is_head(value: Any) -> bool:
    return (
        isinstance(value, str)
        and _HEAD_RE.fullmatch(value) is not None
    )


def _require_optional_head(
    value: Any,
    field: str,
) -> None:
    if value is not None and not _is_head(value):
        raise ObserverTickError(
            f"{field} must be lowercase 40-hex SHA-1 or null"
        )


def _require_failure_code(
    value: Any,
    *,
    required: bool,
) -> None:
    if required:
        if (
            not isinstance(value, str)
            or not value
            or value.strip() != value
        ):
            raise ObserverTickError(
                "failure_code required"
            )
        return
    if value is not None:
        raise ObserverTickError(
            "failure_code must be null"
        )


def _validate_state(state: dict[str, Any]) -> None:
    if not isinstance(state, dict):
        raise ObserverTickError("state must be an object")
    if frozenset(state) != _STATE_KEYS:
        raise ObserverTickError("state fields mismatch")
    if state["schema"] != STATE_SCHEMA:
        raise ObserverTickError("state schema mismatch")
    if state["repository"] != EXPECTED_REPOSITORY:
        raise ObserverTickError("repository mismatch")
    if state["branch"] != EXPECTED_BRANCH:
        raise ObserverTickError("branch mismatch")
    if state["observer_phase"] not in OBSERVER_PHASES:
        raise ObserverTickError("invalid observer phase")
    if state["remote_freshness"] not in REMOTE_FRESHNESS:
        raise ObserverTickError("invalid remote freshness")
    if state["projection_state"] not in PROJECTION_STATES:
        raise ObserverTickError("invalid projection state")

    _require_optional_head(
        state["latest_observed_head"],
        "latest_observed_head",
    )
    _require_optional_head(
        state["last_qualified_head"],
        "last_qualified_head",
    )
    _require_optional_head(
        state["live_projection_head"],
        "live_projection_head",
    )
    _require_optional_head(
        state["blocked_head"],
        "blocked_head",
    )

    pending = state["pending_heads"]
    if not isinstance(pending, list):
        raise ObserverTickError(
            "pending_heads must be an array"
        )
    if not all(_is_head(item) for item in pending):
        raise ObserverTickError(
            "pending_heads contains invalid HEAD"
        )
    if len(pending) != len(set(pending)):
        raise ObserverTickError(
            "pending_heads contains duplicate HEAD"
        )

    failure = state["last_failure_code"]
    if failure is not None and (
        not isinstance(failure, str)
        or not failure
        or failure.strip() != failure
    ):
        raise ObserverTickError(
            "invalid last_failure_code"
        )

    sequence = state["last_event_sequence"]
    if (
        isinstance(sequence, bool)
        or not isinstance(sequence, int)
        or sequence < 0
    ):
        raise ObserverTickError(
            "invalid last_event_sequence"
        )

    if state["projection_state"] == "CURRENT":
        if state["remote_freshness"] != "KNOWN":
            raise ObserverTickError(
                "CURRENT requires KNOWN remote freshness"
            )
        live = state["live_projection_head"]
        if live is None:
            raise ObserverTickError(
                "CURRENT requires live projection HEAD"
            )
        if state["latest_observed_head"] != live:
            raise ObserverTickError(
                "CURRENT requires observed == live"
            )
        if state["last_qualified_head"] != live:
            raise ObserverTickError(
                "CURRENT requires live == qualified"
            )

    if (
        state["observer_phase"] == "EVALUATING"
        and not pending
    ):
        raise ObserverTickError(
            "EVALUATING requires pending queue head"
        )


def _validate_input(
    previous_state: dict[str, Any],
    event: dict[str, Any],
) -> None:
    if not isinstance(event, dict):
        raise ObserverTickError("input must be an object")
    if frozenset(event) != _INPUT_KEYS:
        raise ObserverTickError("input fields mismatch")
    if event["schema"] != INPUT_SCHEMA:
        raise ObserverTickError("input schema mismatch")
    if event["event_type"] not in EVENT_TYPES:
        raise ObserverTickError("invalid event type")

    sequence = event["sequence"]
    if (
        isinstance(sequence, bool)
        or not isinstance(sequence, int)
        or sequence
        != previous_state["last_event_sequence"] + 1
    ):
        raise ObserverTickError(
            "input sequence must advance exactly once"
        )

    _require_optional_head(
        event["observed_head"],
        "observed_head",
    )
    _require_optional_head(
        event["candidate_head"],
        "candidate_head",
    )

    transition_class = event["transition_class"]
    if (
        transition_class is not None
        and transition_class not in TRANSITION_CLASSES
    ):
        raise ObserverTickError(
            "invalid transition class"
        )

    event_type = event["event_type"]

    if event_type == "REMOTE_HEAD_OBSERVED":
        if event["observed_head"] is None:
            raise ObserverTickError(
                "REMOTE_HEAD_OBSERVED requires observed_head"
            )
        if transition_class is None:
            raise ObserverTickError(
                "REMOTE_HEAD_OBSERVED requires transition_class"
            )
        if event["candidate_head"] is not None:
            raise ObserverTickError(
                "remote observation forbids candidate_head"
            )
        _require_failure_code(
            event["failure_code"],
            required=False,
        )
        return

    if event_type == "REMOTE_OBSERVATION_FAILED":
        if (
            event["observed_head"] is not None
            or transition_class is not None
            or event["candidate_head"] is not None
        ):
            raise ObserverTickError(
                "remote failure carries no HEAD"
            )
        _require_failure_code(
            event["failure_code"],
            required=True,
        )
        return

    if event_type in {
        "EVALUATION_STARTED",
        "EVALUATION_PASSED",
        "PROMOTION_CONFIRMED",
    }:
        if (
            event["observed_head"] is not None
            or transition_class is not None
            or event["candidate_head"] is None
        ):
            raise ObserverTickError(
                f"{event_type} normalized fields invalid"
            )
        _require_failure_code(
            event["failure_code"],
            required=False,
        )
        return

    if event_type in {
        "EVALUATION_FAILED",
        "PROMOTION_FAILED",
    }:
        if (
            event["observed_head"] is not None
            or transition_class is not None
            or event["candidate_head"] is None
        ):
            raise ObserverTickError(
                f"{event_type} normalized fields invalid"
            )
        _require_failure_code(
            event["failure_code"],
            required=True,
        )
        return

    if event_type == "LOCK_CONTENDED":
        if (
            event["observed_head"] is not None
            or transition_class is not None
            or event["candidate_head"] is not None
            or event["failure_code"] != "LOCK_CONTENDED"
        ):
            raise ObserverTickError(
                "LOCK_CONTENDED normalized fields invalid"
            )
        return

    if (
        event["observed_head"] is not None
        or transition_class is not None
        or event["candidate_head"] is not None
    ):
        raise ObserverTickError(
            f"{event_type} carries unexpected HEAD"
        )
    _require_failure_code(
        event["failure_code"],
        required=False,
    )


def make_initial_state() -> dict[str, Any]:
    state = {
        "schema": STATE_SCHEMA,
        "repository": EXPECTED_REPOSITORY,
        "branch": EXPECTED_BRANCH,
        "observer_phase": "IDLE",
        "remote_freshness": "UNKNOWN",
        "latest_observed_head": None,
        "last_qualified_head": None,
        "live_projection_head": None,
        "projection_state": "MISSING",
        "pending_heads": [],
        "blocked_head": None,
        "last_failure_code": None,
        "last_event_sequence": 0,
    }
    _validate_state(state)
    return state


def _decision(
    *,
    action: str,
    reason_code: str,
    observed_head: str | None,
    candidate_head: str | None,
    previous_live_head: str | None,
    next_projection_state: str,
) -> dict[str, Any]:
    return {
        "schema": DECISION_SCHEMA,
        "action": action,
        "reason_code": reason_code,
        "observed_head": observed_head,
        "candidate_head": candidate_head,
        "previous_live_head": previous_live_head,
        "next_projection_state": next_projection_state,
        "automatic_promotion_authorized": False,
        "production_write_authorized": False,
    }


def _apply_remote_observed(
    state: dict[str, Any],
    event: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    observed = event["observed_head"]
    transition_class = event["transition_class"]
    previous_live = state["live_projection_head"]

    if transition_class == "SAME":
        if state["latest_observed_head"] != observed:
            raise ObserverTickError(
                "SAME requires previous observed HEAD equality"
            )
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        next_state["last_failure_code"] = None
        if (
            next_state["observer_phase"] != "BLOCKED"
            and next_state["live_projection_head"] is not None
            and next_state["live_projection_head"] == observed
            and next_state["last_qualified_head"] == observed
        ):
            next_state["projection_state"] = "CURRENT"
        decision = _decision(
            action="NOOP",
            reason_code="REMOTE_HEAD_SAME",
            observed_head=observed,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=next_state[
                "projection_state"
            ],
        )
        return next_state, decision

    if transition_class == "INITIAL":
        if state["latest_observed_head"] is not None:
            raise ObserverTickError(
                "INITIAL requires no previous observed HEAD"
            )
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        next_state["last_failure_code"] = None
        if observed not in next_state["pending_heads"]:
            next_state["pending_heads"].append(observed)
        next_state["projection_state"] = (
            "MISSING"
            if next_state["live_projection_head"] is None
            else "STALE"
        )
        decision = _decision(
            action="QUEUE_EXACT_HEAD_FOR_EVALUATION",
            reason_code="REMOTE_HEAD_INITIAL_QUEUED",
            observed_head=observed,
            candidate_head=observed,
            previous_live_head=previous_live,
            next_projection_state=next_state[
                "projection_state"
            ],
        )
        return next_state, decision

    if state["latest_observed_head"] is None:
        raise ObserverTickError(
            f"{transition_class} requires previous observed HEAD"
        )
    if state["latest_observed_head"] == observed:
        raise ObserverTickError(
            f"{transition_class} requires a new observed HEAD"
        )

    if transition_class == "FAST_FORWARD":
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        next_state["last_failure_code"] = None
        if observed not in next_state["pending_heads"]:
            next_state["pending_heads"].append(observed)
        next_state["projection_state"] = "STALE"
        decision = _decision(
            action="QUEUE_EXACT_HEAD_FOR_EVALUATION",
            reason_code="REMOTE_HEAD_FAST_FORWARD_QUEUED",
            observed_head=observed,
            candidate_head=observed,
            previous_live_head=previous_live,
            next_projection_state="STALE",
        )
        return next_state, decision

    if transition_class in {
        "NON_FAST_FORWARD",
        "UNKNOWN",
    }:
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        next_state["observer_phase"] = "BLOCKED"
        next_state["projection_state"] = "BLOCKED"
        next_state["blocked_head"] = observed
        next_state["last_failure_code"] = (
            "NON_FAST_FORWARD_REQUIRES_ADJUDICATION"
            if transition_class == "NON_FAST_FORWARD"
            else "UNKNOWN_ANCESTRY_REQUIRES_ADJUDICATION"
        )
        decision = _decision(
            action="BLOCK_REQUIRES_ADJUDICATION",
            reason_code=next_state["last_failure_code"],
            observed_head=observed,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state="BLOCKED",
        )
        return next_state, decision

    raise ObserverTickError(
        "unsupported remote transition class"
    )


def _apply_transition(
    state: dict[str, Any],
    event: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    event_type = event["event_type"]
    previous_live = state["live_projection_head"]

    if state["observer_phase"] == "STOPPED":
        raise ObserverTickError(
            "STOPPED observer accepts no further events"
        )

    if event_type == "BOOTSTRAP":
        if state["last_event_sequence"] != 0:
            raise ObserverTickError(
                "BOOTSTRAP allowed only at sequence zero"
            )
        next_state = _clone(state)
        decision = _decision(
            action="NOOP",
            reason_code="BOOTSTRAP_ACCEPTED",
            observed_head=None,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=state[
                "projection_state"
            ],
        )
        return next_state, decision

    if event_type == "REMOTE_HEAD_OBSERVED":
        return _apply_remote_observed(state, event)

    if event_type == "REMOTE_OBSERVATION_FAILED":
        next_state = _clone(state)
        next_state["remote_freshness"] = "UNKNOWN"
        next_state["last_failure_code"] = event[
            "failure_code"
        ]
        if next_state["projection_state"] == "CURRENT":
            next_state["projection_state"] = "STALE"
        decision = _decision(
            action="RETAIN_LAST_KNOWN_GOOD",
            reason_code="REMOTE_OBSERVATION_FAILED",
            observed_head=None,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=next_state[
                "projection_state"
            ],
        )
        return next_state, decision

    if event_type == "EVALUATION_STARTED":
        candidate = event["candidate_head"]
        if state["observer_phase"] != "IDLE":
            raise ObserverTickError(
                "evaluation may start only from IDLE"
            )
        if (
            not state["pending_heads"]
            or state["pending_heads"][0] != candidate
        ):
            raise ObserverTickError(
                "evaluation candidate must equal queue head"
            )
        next_state = _clone(state)
        next_state["observer_phase"] = "EVALUATING"
        decision = _decision(
            action="START_EXACT_HEAD_EVALUATION",
            reason_code="EVALUATION_STARTED",
            observed_head=None,
            candidate_head=candidate,
            previous_live_head=previous_live,
            next_projection_state=next_state[
                "projection_state"
            ],
        )
        return next_state, decision

    if event_type in {
        "EVALUATION_PASSED",
        "EVALUATION_FAILED",
    }:
        candidate = event["candidate_head"]
        if state["observer_phase"] != "EVALUATING":
            raise ObserverTickError(
                f"{event_type} requires EVALUATING phase"
            )
        if (
            not state["pending_heads"]
            or state["pending_heads"][0] != candidate
        ):
            raise ObserverTickError(
                "evaluation result candidate must equal queue head"
            )
        next_state = _clone(state)
        next_state["pending_heads"] = (
            next_state["pending_heads"][1:]
        )

        if event_type == "EVALUATION_PASSED":
            next_state["last_qualified_head"] = candidate
            next_state["observer_phase"] = (
                "CANDIDATE_PENDING"
            )
            next_state["blocked_head"] = None
            next_state["last_failure_code"] = None
            decision = _decision(
                action=(
                    "CANDIDATE_QUALIFIED_PENDING_PROMOTION"
                ),
                reason_code="EVALUATION_PASSED",
                observed_head=None,
                candidate_head=candidate,
                previous_live_head=previous_live,
                next_projection_state=next_state[
                    "projection_state"
                ],
            )
            return next_state, decision

        next_state["observer_phase"] = "BLOCKED"
        next_state["projection_state"] = "BLOCKED"
        next_state["blocked_head"] = candidate
        next_state["last_failure_code"] = event[
            "failure_code"
        ]
        decision = _decision(
            action="RETAIN_LAST_KNOWN_GOOD",
            reason_code="EVALUATION_FAILED",
            observed_head=None,
            candidate_head=candidate,
            previous_live_head=previous_live,
            next_projection_state="BLOCKED",
        )
        return next_state, decision

    if event_type in {
        "PROMOTION_CONFIRMED",
        "PROMOTION_FAILED",
    }:
        candidate = event["candidate_head"]
        if state["observer_phase"] != "CANDIDATE_PENDING":
            raise ObserverTickError(
                f"{event_type} requires CANDIDATE_PENDING"
            )
        if state["last_qualified_head"] != candidate:
            raise ObserverTickError(
                "promotion candidate must equal last qualified HEAD"
            )
        next_state = _clone(state)

        if event_type == "PROMOTION_CONFIRMED":
            next_state["live_projection_head"] = candidate
            next_state["observer_phase"] = "IDLE"
            next_state["blocked_head"] = None
            next_state["last_failure_code"] = None
            if (
                next_state["remote_freshness"] == "KNOWN"
                and next_state["latest_observed_head"]
                == candidate
            ):
                next_state["projection_state"] = "CURRENT"
            else:
                next_state["projection_state"] = "STALE"
            decision = _decision(
                action="CONFIRM_LIVE_PROJECTION",
                reason_code="PROMOTION_CONFIRMED",
                observed_head=None,
                candidate_head=candidate,
                previous_live_head=previous_live,
                next_projection_state=next_state[
                    "projection_state"
                ],
            )
            return next_state, decision

        next_state["observer_phase"] = "BLOCKED"
        next_state["projection_state"] = "BLOCKED"
        next_state["blocked_head"] = candidate
        next_state["last_failure_code"] = event[
            "failure_code"
        ]
        decision = _decision(
            action="RETAIN_LAST_KNOWN_GOOD",
            reason_code="PROMOTION_FAILED",
            observed_head=None,
            candidate_head=candidate,
            previous_live_head=previous_live,
            next_projection_state="BLOCKED",
        )
        return next_state, decision

    if event_type == "LOCK_CONTENDED":
        next_state = _clone(state)
        decision = _decision(
            action="NOOP",
            reason_code="LOCK_CONTENDED",
            observed_head=None,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=state[
                "projection_state"
            ],
        )
        return next_state, decision

    if event_type == "SHUTDOWN_REQUESTED":
        next_state = _clone(state)
        next_state["observer_phase"] = "STOPPED"
        decision = _decision(
            action="STOP",
            reason_code="SHUTDOWN_REQUESTED",
            observed_head=None,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=state[
                "projection_state"
            ],
        )
        return next_state, decision

    raise ObserverTickError("unsupported event type")


def one_shot_tick(
    previous_state: dict[str, Any],
    normalized_input: dict[str, Any],
) -> dict[str, Any]:
    previous = _clone(previous_state)
    event = _clone(normalized_input)

    _validate_state(previous)
    _validate_input(previous, event)

    next_state, decision = _apply_transition(
        previous,
        event,
    )
    next_state["last_event_sequence"] = event["sequence"]

    _validate_state(next_state)

    audit = {
        "schema": EVENT_SCHEMA,
        "sequence": event["sequence"],
        "event_type": event["event_type"],
        "previous_state_digest": _digest(previous),
        "input_digest": _digest(event),
        "decision_digest": _digest(decision),
        "next_state_digest": _digest(next_state),
        "reason_code": decision["reason_code"],
    }

    result = {
        "schema": RESULT_SCHEMA,
        "next_state": next_state,
        "decision": decision,
        "audit": audit,
    }

    _canonical_json_bytes(result)
    return result


def canonical_result_bytes(
    result: dict[str, Any],
) -> bytes:
    return _canonical_json_bytes(result)
