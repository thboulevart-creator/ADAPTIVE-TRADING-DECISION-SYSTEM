from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Sequence

from tools.trading_breaks_recovery_protocol import recovery_queue


CONTRACT = "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
LEDGER_SCHEMA = "HISTORICAL_TRADING_BREAKS_RECOVERY_ATTEMPT_LEDGER_V1"
LEDGER_PATH = Path(__file__).resolve().parents[1] / "reports" / "data-qualification" / "historical_trading_breaks_recovery_attempt_ledger.json"
REPORT_PATH = Path(__file__).resolve().parents[1] / "reports" / "data-qualification" / "historical_trading_breaks_recovery_progression_runtime.json"

_ALLOWED_OUTCOMES = frozenset({"PASS", "BLOCKED", "FAIL"})
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")

RETRY_CAPABILITY_REQUIREMENTS: dict[str, frozenset[str]] = {
    "NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED": frozenset(
        {
            "ALTERNATE_BROKER_NATIVE_RECORD_ROUTE",
            "BROKER_ARCHIVE_BACKFILL_ACCESS",
        }
    ),
    "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE": frozenset(
        {
            "QUALIFIED_CROSS_DATE_INTERVAL_ATTRIBUTION",
            "ALTERNATE_EXACT_TARGET_DATE_PRIMARY_RECORD_ROUTE",
        }
    ),
    "EXPECTED_DOM_CROSSCHECK_MISSING": frozenset(
        {"DOM_CROSSCHECK_RECOVERY_PATH"}
    ),
    "RAW_BROKER_PAYLOAD_NOT_RETAINED": frozenset(
        {"RAW_PAYLOAD_RETENTION_RECOVERY"}
    ),
    "WORKFLOW_PROVENANCE_MISSING": frozenset(
        {"WORKFLOW_PROVENANCE_CAPTURE_RECOVERY"}
    ),
    "ARTIFACT_ID_MISSING": frozenset(
        {"ARTIFACT_PROVENANCE_CAPTURE_RECOVERY"}
    ),
    "ARTIFACT_SHA256_INVALID": frozenset(
        {"ARTIFACT_PROVENANCE_CAPTURE_RECOVERY"}
    ),
    "PROBE_COMMIT_INVALID": frozenset(
        {"PROBE_COMMIT_PROVENANCE_RECOVERY"}
    ),
}


@dataclass(frozen=True)
class CapabilityIdentity:
    route_contract: str
    protocol_contract: str
    capture_implementation: str
    proof_capabilities: frozenset[str]

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "route_contract": self.route_contract,
            "protocol_contract": self.protocol_contract,
            "capture_implementation": self.capture_implementation,
            "proof_capabilities": sorted(self.proof_capabilities),
        }

    def fingerprint(self) -> str:
        payload = json.dumps(
            self.canonical_payload(),
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class AttemptRecord:
    attempt_sequence: int
    attempt_id: str
    batch_contract: str
    target_date: date
    candidate_reason: str
    outcome: str
    adjudication_reason: str
    blocking_reason: str | None
    capability_id: str
    capability: CapabilityIdentity
    provenance: dict[str, Any]


@dataclass(frozen=True)
class MaterialCapabilityChange:
    change_id: str
    from_fingerprint: str
    to_fingerprint: str
    changed_dimensions: frozenset[str]
    added_proof_capabilities: frozenset[str]
    addresses_blocking_reasons: frozenset[str]


@dataclass(frozen=True)
class EligibilityDecision:
    target_date: date
    candidate_reason: str
    calendar_state: str
    latest_attempt_id: str | None
    latest_attempt_outcome: str | None
    latest_capability_fingerprint: str | None
    eligible: bool
    reason: str
    contract_verdict: str = "PASS"

    def as_dict(self) -> dict[str, Any]:
        return {
            "target_date": self.target_date.isoformat(),
            "candidate_reason": self.candidate_reason,
            "calendar_state": self.calendar_state,
            "latest_attempt_id": self.latest_attempt_id,
            "latest_attempt_outcome": self.latest_attempt_outcome,
            "latest_capability_fingerprint": self.latest_capability_fingerprint,
            "eligible": self.eligible,
            "reason": self.reason,
            "contract_verdict": self.contract_verdict,
        }


def capability_from_payload(payload: dict[str, Any]) -> CapabilityIdentity:
    proof_capabilities = payload.get("proof_capabilities")
    if not isinstance(proof_capabilities, list) or not proof_capabilities:
        raise ValueError("capability proof_capabilities must be a non-empty list")
    if any(not isinstance(item, str) or not item.strip() for item in proof_capabilities):
        raise ValueError("capability proof capability must be a non-empty string")
    if len(proof_capabilities) != len(set(proof_capabilities)):
        raise ValueError("duplicate proof capability")

    fields = {}
    for name in ("route_contract", "protocol_contract", "capture_implementation"):
        value = payload.get(name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"capability {name} missing")
        fields[name] = value.strip()

    return CapabilityIdentity(
        route_contract=fields["route_contract"],
        protocol_contract=fields["protocol_contract"],
        capture_implementation=fields["capture_implementation"],
        proof_capabilities=frozenset(proof_capabilities),
    )


def _validate_provenance(provenance: dict[str, Any]) -> None:
    for key in ("workflow_run", "job_id", "artifact_id"):
        value = provenance.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError(f"invalid provenance {key}")
    artifact_sha256 = provenance.get("artifact_sha256")
    if not isinstance(artifact_sha256, str) or not _SHA256_RE.fullmatch(artifact_sha256):
        raise ValueError("invalid provenance artifact_sha256")
    probe_commit = provenance.get("probe_commit")
    if not isinstance(probe_commit, str) or not _COMMIT_RE.fullmatch(probe_commit):
        raise ValueError("invalid provenance probe_commit")


def load_attempt_ledger(path: Path = LEDGER_PATH) -> tuple[dict[str, CapabilityIdentity], str, list[AttemptRecord]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != LEDGER_SCHEMA:
        raise ValueError("wrong attempt ledger schema")

    raw_capabilities = data.get("capabilities")
    if not isinstance(raw_capabilities, dict) or not raw_capabilities:
        raise ValueError("attempt ledger capabilities missing")
    capabilities = {
        capability_id: capability_from_payload(payload)
        for capability_id, payload in raw_capabilities.items()
    }

    current_capability_id = data.get("current_capability_id")
    if current_capability_id not in capabilities:
        raise ValueError("current capability id missing from ledger")

    raw_attempts = data.get("attempts")
    if not isinstance(raw_attempts, list):
        raise ValueError("attempt ledger attempts missing")

    seen_ids: set[str] = set()
    seen_sequences: set[int] = set()
    attempts: list[AttemptRecord] = []
    for raw in raw_attempts:
        if not isinstance(raw, dict):
            raise ValueError("attempt must be an object")
        sequence = raw.get("attempt_sequence")
        if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence <= 0:
            raise ValueError("invalid attempt sequence")
        if sequence in seen_sequences:
            raise ValueError("duplicate attempt sequence")
        seen_sequences.add(sequence)

        attempt_id = raw.get("attempt_id")
        if not isinstance(attempt_id, str) or not attempt_id.strip():
            raise ValueError("invalid attempt id")
        if attempt_id in seen_ids:
            raise ValueError("duplicate attempt id")
        seen_ids.add(attempt_id)

        capability_id = raw.get("capability_id")
        if capability_id not in capabilities:
            raise ValueError("attempt references unknown capability")

        outcome = raw.get("outcome")
        if outcome not in _ALLOWED_OUTCOMES:
            raise ValueError("invalid attempt outcome")
        blocking_reason = raw.get("blocking_reason")
        if outcome == "BLOCKED":
            if not isinstance(blocking_reason, str) or not blocking_reason.strip():
                raise ValueError("BLOCKED attempt missing blocking reason")
        elif blocking_reason is not None:
            raise ValueError("non-BLOCKED attempt cannot carry blocking reason")

        adjudication_reason = raw.get("adjudication_reason")
        if not isinstance(adjudication_reason, str) or not adjudication_reason.strip():
            raise ValueError("attempt adjudication reason missing")

        candidate_reason = raw.get("candidate_reason")
        batch_contract = raw.get("batch_contract")
        if not isinstance(candidate_reason, str) or not candidate_reason.strip():
            raise ValueError("attempt candidate reason missing")
        if not isinstance(batch_contract, str) or not batch_contract.strip():
            raise ValueError("attempt batch contract missing")

        provenance = raw.get("provenance")
        if not isinstance(provenance, dict):
            raise ValueError("attempt provenance missing")
        _validate_provenance(provenance)

        attempts.append(
            AttemptRecord(
                attempt_sequence=sequence,
                attempt_id=attempt_id,
                batch_contract=batch_contract,
                target_date=date.fromisoformat(raw["target_date"]),
                candidate_reason=candidate_reason,
                outcome=outcome,
                adjudication_reason=adjudication_reason,
                blocking_reason=blocking_reason,
                capability_id=capability_id,
                capability=capabilities[capability_id],
                provenance=dict(provenance),
            )
        )

    attempts.sort(key=lambda item: item.attempt_sequence)
    if [item.attempt_sequence for item in attempts] != list(range(1, len(attempts) + 1)):
        raise ValueError("attempt sequences must be contiguous and monotonic")

    return capabilities, current_capability_id, attempts


def current_capability(path: Path = LEDGER_PATH) -> CapabilityIdentity:
    capabilities, current_capability_id, _ = load_attempt_ledger(path)
    return capabilities[current_capability_id]


def latest_attempt_for_date(target_date: date, attempts: Sequence[AttemptRecord]) -> AttemptRecord | None:
    matching = [item for item in attempts if item.target_date == target_date]
    if not matching:
        return None
    return max(matching, key=lambda item: item.attempt_sequence)


def actual_changed_dimensions(old: CapabilityIdentity, new: CapabilityIdentity) -> frozenset[str]:
    changed: set[str] = set()
    if old.route_contract != new.route_contract:
        changed.add("route_contract")
    if old.protocol_contract != new.protocol_contract:
        changed.add("protocol_contract")
    if old.capture_implementation != new.capture_implementation:
        changed.add("capture_implementation")
    if old.proof_capabilities != new.proof_capabilities:
        changed.add("proof_capabilities")
    return frozenset(changed)


def validate_material_capability_change(
    previous_attempt: AttemptRecord,
    current: CapabilityIdentity,
    change: MaterialCapabilityChange,
) -> tuple[bool, str]:
    if previous_attempt.outcome != "BLOCKED" or not previous_attempt.blocking_reason:
        return False, "PREVIOUS_ATTEMPT_NOT_BLOCKED"

    old = previous_attempt.capability
    old_fp = old.fingerprint()
    new_fp = current.fingerprint()
    if old_fp == new_fp:
        return False, "SEMANTIC_CAPABILITY_UNCHANGED"
    if change.from_fingerprint != old_fp or change.to_fingerprint != new_fp:
        return False, "CAPABILITY_CHANGE_FINGERPRINT_MISMATCH"

    actual_dimensions = actual_changed_dimensions(old, current)
    if not actual_dimensions or change.changed_dimensions != actual_dimensions:
        return False, "DECLARED_CHANGED_DIMENSIONS_MISMATCH"

    added = current.proof_capabilities - old.proof_capabilities
    if not added or change.added_proof_capabilities != added:
        return False, "NEW_PROOF_CAPABILITY_NOT_PROVEN"

    blocker = previous_attempt.blocking_reason
    required = RETRY_CAPABILITY_REQUIREMENTS.get(blocker)
    if not required:
        return False, "BLOCKING_REASON_HAS_NO_GOVERNED_RETRY_CAPABILITY"
    if blocker not in change.addresses_blocking_reasons:
        return False, "BLOCKING_REASON_NOT_EXPLICITLY_ADDRESSED"
    if not (added & required):
        return False, "ADDED_CAPABILITY_IRRELEVANT_TO_BLOCKER"
    if not isinstance(change.change_id, str) or not change.change_id.strip():
        return False, "MATERIAL_CHANGE_ID_MISSING"

    return True, "MATERIAL_CAPABILITY_CHANGE_PROVEN"


def eligibility_for_unresolved_candidate(
    target_date: date,
    candidate_reason: str,
    attempts: Sequence[AttemptRecord],
    current: CapabilityIdentity,
    changes: Iterable[MaterialCapabilityChange] = (),
) -> EligibilityDecision:
    latest = latest_attempt_for_date(target_date, attempts)
    if latest is None:
        return EligibilityDecision(
            target_date=target_date,
            candidate_reason=candidate_reason,
            calendar_state="UNRESOLVED",
            latest_attempt_id=None,
            latest_attempt_outcome=None,
            latest_capability_fingerprint=None,
            eligible=True,
            reason="INITIAL_ATTEMPT",
        )

    latest_fp = latest.capability.fingerprint()
    common = {
        "target_date": target_date,
        "candidate_reason": candidate_reason,
        "calendar_state": "UNRESOLVED",
        "latest_attempt_id": latest.attempt_id,
        "latest_attempt_outcome": latest.outcome,
        "latest_capability_fingerprint": latest_fp,
    }

    if latest.outcome == "PASS":
        return EligibilityDecision(
            **common,
            eligible=False,
            reason="PASS_ATTEMPT_STILL_PRESENT_IN_UNRESOLVED_QUEUE",
            contract_verdict="FAIL",
        )
    if latest.outcome == "FAIL":
        return EligibilityDecision(
            **common,
            eligible=False,
            reason="PREVIOUS_ATTEMPT_FAIL_REQUIRES_SEPARATE_REMEDIATION",
        )

    current_fp = current.fingerprint()
    if latest_fp == current_fp:
        return EligibilityDecision(
            **common,
            eligible=False,
            reason="SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED",
        )

    matching_changes = [
        item
        for item in changes
        if item.from_fingerprint == latest_fp and item.to_fingerprint == current_fp
    ]
    if len(matching_changes) != 1:
        return EligibilityDecision(
            **common,
            eligible=False,
            reason="RETRY_MATERIAL_CHANGE_NOT_PROVEN",
        )

    valid, material_reason = validate_material_capability_change(
        latest, current, matching_changes[0]
    )
    if not valid:
        return EligibilityDecision(
            **common,
            eligible=False,
            reason=f"RETRY_MATERIAL_CHANGE_NOT_PROVEN:{material_reason}",
        )

    return EligibilityDecision(
        **common,
        eligible=True,
        reason="MATERIAL_CAPABILITY_CHANGE_RETRY",
    )


def progression_decisions(
    *,
    attempts: Sequence[AttemptRecord] | None = None,
    current: CapabilityIdentity | None = None,
    changes: Iterable[MaterialCapabilityChange] = (),
) -> list[EligibilityDecision]:
    if attempts is None or current is None:
        capabilities, current_capability_id, ledger_attempts = load_attempt_ledger()
        if attempts is None:
            attempts = ledger_attempts
        if current is None:
            current = capabilities[current_capability_id]

    queue = recovery_queue()
    return [
        eligibility_for_unresolved_candidate(
            target_date=target_date,
            candidate_reason=candidate_reason,
            attempts=attempts,
            current=current,
            changes=changes,
        )
        for target_date, candidate_reason in queue
    ]


def eligible_recovery_queue(
    *,
    attempts: Sequence[AttemptRecord] | None = None,
    current: CapabilityIdentity | None = None,
    changes: Iterable[MaterialCapabilityChange] = (),
) -> list[tuple[date, str]]:
    decisions = progression_decisions(
        attempts=attempts,
        current=current,
        changes=changes,
    )
    return [
        (item.target_date, item.candidate_reason)
        for item in decisions
        if item.eligible and item.contract_verdict == "PASS"
    ]


def build_progression_report() -> dict[str, Any]:
    capabilities, current_capability_id, attempts = load_attempt_ledger()
    current = capabilities[current_capability_id]
    decisions = progression_decisions(attempts=attempts, current=current)
    queue = recovery_queue()

    if [(d.target_date, d.candidate_reason) for d in decisions] != queue:
        return {
            "schema": CONTRACT,
            "verdict": "FAIL",
            "reason": "PROGRESSION_PLAN_DOES_NOT_COVER_EXACT_UNRESOLVED_QUEUE",
        }
    contradictions = [d.as_dict() for d in decisions if d.contract_verdict == "FAIL"]
    if contradictions:
        return {
            "schema": CONTRACT,
            "verdict": "FAIL",
            "reason": "CALENDAR_ATTEMPT_STATE_CONTRADICTION",
            "contradictions": contradictions,
        }

    eligible = [d for d in decisions if d.eligible]
    attempted_blocked_ineligible = [
        d
        for d in decisions
        if d.latest_attempt_outcome == "BLOCKED" and not d.eligible
    ]

    return {
        "schema": CONTRACT,
        "verdict": "PASS",
        "reason": "ATTEMPT_AWARE_PROGRESSION_STATE_IS_DETERMINISTIC_AND_NON_STARVING",
        "calendar_unresolved_count": len(queue),
        "attempt_ledger_count": len(attempts),
        "current_capability_id": current_capability_id,
        "current_capability_fingerprint": current.fingerprint(),
        "attempted_blocked_ineligible_count": len(attempted_blocked_ineligible),
        "eligible_initial_or_retry_count": len(eligible),
        "decisions": [item.as_dict() for item in decisions],
    }


def main() -> int:
    report = build_progression_report()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report.get("verdict") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
