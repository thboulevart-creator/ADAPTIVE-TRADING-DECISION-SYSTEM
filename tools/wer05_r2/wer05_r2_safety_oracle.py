"""WER-05-R2 V0.1: PURE SYNTHETIC decision oracle. No Windows or process API.

This module MUST NOT be treated as an operational shutdown controller.
All inputs are supplied as test fixtures or mock observations; no side effects.
"""
from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Optional


class Decision(str, Enum):
    STOP_UNQUALIFIED = "STOP_UNQUALIFIED"
    OBSERVE = "OBSERVE"
    PROPOSE_GRACEFUL = "PROPOSE_GRACEFUL"
    PROPOSE_FALLBACK = "PROPOSE_FALLBACK"
    CLOSED_PENDING_INDEPENDENT_PROOF = "CLOSED_PENDING_INDEPENDENT_PROOF"
    CLOSED_PROVEN_IN_MODEL = "CLOSED_PROVEN_IN_MODEL"
    DEADLINE_BREACH = "DEADLINE_BREACH"


@dataclass(frozen=True)
class MockObservation:
    monotonic_elapsed_seconds: float
    baseline_ids: FrozenSet[str]
    current_ids: FrozenSet[str]
    claimed_guest_id: Optional[str]
    trusted_unique_launch_binding: bool
    hcs_identity_metadata_qualified: bool
    local_watchdog_independent: bool
    privileged_control_permission_proven: bool
    graceful_path_qualified: bool
    fallback_path_qualified: bool
    remote_control_connected: bool  # intentionally NOT required if watchdog is local
    graceful_proposed: bool
    fallback_proposed: bool
    host_process_absence_confirmed: bool
    independent_lifecycle_terminal_record: bool
    previous_monotonic_elapsed_seconds: float = 0.0


def evaluate(obs: MockObservation) -> Decision:
    """Return a recommendation ONLY; does not operate on any system."""
    t = obs.monotonic_elapsed_seconds
    if t < 0 or t < obs.previous_monotonic_elapsed_seconds:
        return Decision.STOP_UNQUALIFIED
    if not obs.local_watchdog_independent:
        return Decision.STOP_UNQUALIFIED
    if not (obs.privileged_control_permission_proven
            and obs.graceful_path_qualified and obs.fallback_path_qualified):
        return Decision.STOP_UNQUALIFIED
    if not obs.trusted_unique_launch_binding or not obs.hcs_identity_metadata_qualified:
        return Decision.STOP_UNQUALIFIED
    guest_id = obs.claimed_guest_id
    if not guest_id or guest_id in obs.baseline_ids:
        return Decision.STOP_UNQUALIFIED
    added = obs.current_ids.difference(obs.baseline_ids)
    if added and added != frozenset({guest_id}):
        # Another new VM, or ambiguous target: never act.
        return Decision.STOP_UNQUALIFIED
    if guest_id not in obs.current_ids:
        if not obs.graceful_proposed and not obs.fallback_proposed:
            return Decision.STOP_UNQUALIFIED
        if obs.host_process_absence_confirmed and obs.independent_lifecycle_terminal_record:
            return Decision.CLOSED_PROVEN_IN_MODEL
        return Decision.CLOSED_PENDING_INDEPENDENT_PROOF
    # The 300s boundary cannot be met solely by issuing a command at the deadline.
    if t >= 300:
        return Decision.DEADLINE_BREACH
    if t >= 270 and obs.graceful_proposed and not obs.fallback_proposed:
        return Decision.PROPOSE_FALLBACK
    if t >= 240 and not obs.graceful_proposed:
        return Decision.PROPOSE_GRACEFUL
    return Decision.OBSERVE
