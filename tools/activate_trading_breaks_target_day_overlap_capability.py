from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from tools.trading_breaks_recovery_progression import (
    CapabilityIdentity,
    MaterialCapabilityChange,
    actual_changed_dimensions,
    capability_from_payload,
    load_attempt_ledger,
    load_material_capability_changes,
    validate_material_capability_change,
)
from tools.trading_breaks_target_day_overlap_semantics import (
    ADDRESSES_BLOCKER,
    CLASS_A_SOURCES,
    CONTRACT as QUALIFICATION_CONTRACT,
    QUALIFIED_PROOF_CAPABILITY,
    qualify_class_a,
)

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "reports" / "data-qualification" / "historical_trading_breaks_recovery_attempt_ledger.json"
REGISTRY_PATH = ROOT / "reports" / "data-qualification" / "historical_trading_breaks_recovery_capability_changes.json"

OLD_CAPABILITY_ID = "TRADING_BREAKS_PRIMARY_WIDGET_V1"
OLD_FINGERPRINT = "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"
NEW_CAPABILITY_ID = "TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2"
NEW_PROTOCOL_CONTRACT = "TRADING_BREAKS_TARGET_DAY_OVERLAP_ATTRIBUTION_V1"
NEW_FINGERPRINT = "e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31"
CHANGE_ID = "TRADING_BREAKS_TARGET_DAY_OVERLAP_ATTRIBUTION_CHANGE_V1"
QUALIFICATION_COMMIT = "061e97d90eed2c4c3f1d5f2a261e457fd796413f"
CLASS_B_BLOCKER = "NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED"

NEW_CAPABILITY_PAYLOAD = {
    "route_contract": "HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION_V1",
    "protocol_contract": NEW_PROTOCOL_CONTRACT,
    "capture_implementation": "tools.trading_breaks_recovery_batch01.probe_candidate",
    "proof_capabilities": [
        "ARTIFACT_PROVENANCE",
        "DOM_NETWORK_CROSSCHECK",
        "EXACT_HISTORICAL_DATE_REQUEST",
        "EXACT_TARGET_DATE_POSITIVE_RECORD_ONLY",
        "QUALIFIED_CROSS_DATE_INTERVAL_ATTRIBUTION",
        "RAW_PRIMARY_BROKER_BREAK_PAYLOAD",
        "USATECH_INSTRUMENT_IDENTITY",
    ],
}


def proposed_capability() -> CapabilityIdentity:
    capability = capability_from_payload(deepcopy(NEW_CAPABILITY_PAYLOAD))
    if capability.fingerprint() != NEW_FINGERPRINT:
        raise RuntimeError("NEW_CAPABILITY_FINGERPRINT_DRIFT")
    return capability


def proposed_change() -> MaterialCapabilityChange:
    return MaterialCapabilityChange(
        change_id=CHANGE_ID,
        from_fingerprint=OLD_FINGERPRINT,
        to_fingerprint=NEW_FINGERPRINT,
        changed_dimensions=frozenset({"protocol_contract", "proof_capabilities"}),
        added_proof_capabilities=frozenset({QUALIFIED_PROOF_CAPABILITY}),
        addresses_blocking_reasons=frozenset({ADDRESSES_BLOCKER}),
        qualification_contract=QUALIFICATION_CONTRACT,
        qualification_commit=QUALIFICATION_COMMIT,
    )


def validate_activation_preconditions() -> dict[str, object]:
    capabilities, current_id, attempts = load_attempt_ledger()
    changes = load_material_capability_changes()
    if current_id != OLD_CAPABILITY_ID:
        raise RuntimeError(f"CURRENT_CAPABILITY_NOT_V1:{current_id}")
    if set(capabilities) != {OLD_CAPABILITY_ID}:
        raise RuntimeError(f"UNEXPECTED_PREEXISTING_CAPABILITIES:{sorted(capabilities)}")
    old = capabilities[OLD_CAPABILITY_ID]
    if old.fingerprint() != OLD_FINGERPRINT:
        raise RuntimeError("OLD_CAPABILITY_FINGERPRINT_MISMATCH")
    if len(attempts) != 68:
        raise RuntimeError(f"ATTEMPT_LEDGER_COUNT_MISMATCH:{len(attempts)}")
    if changes:
        raise RuntimeError("CAPABILITY_CHANGE_REGISTRY_NOT_EMPTY")

    qualification = qualify_class_a()
    if qualification.get("verdict") != "PASS" or qualification.get("class_a_count") != 14:
        raise RuntimeError("OVERLAP_SEMANTIC_QUALIFICATION_NOT_PASS")

    new = proposed_capability()
    change = proposed_change()
    if actual_changed_dimensions(old, new) != frozenset({"protocol_contract", "proof_capabilities"}):
        raise RuntimeError("ACTUAL_CHANGED_DIMENSIONS_MISMATCH")
    if not old.proof_capabilities < new.proof_capabilities:
        raise RuntimeError("PROOF_CAPABILITY_NOT_STRICT_SUPERSET")

    class_a_days = {day for day, _, _ in CLASS_A_SOURCES}
    latest_by_day = {}
    for attempt in attempts:
        latest_by_day[attempt.target_date] = attempt
    if set(day for day in class_a_days if day not in latest_by_day):
        raise RuntimeError("CLASS_A_ATTEMPT_MISSING")

    for day in class_a_days:
        latest = latest_by_day[day]
        if latest.outcome != "BLOCKED" or latest.blocking_reason != ADDRESSES_BLOCKER:
            raise RuntimeError(f"CLASS_A_LATEST_BLOCKER_MISMATCH:{day}")
        valid, reason = validate_material_capability_change(latest, new, change)
        if not valid or reason != "MATERIAL_CAPABILITY_CHANGE_PROVEN":
            raise RuntimeError(f"CLASS_A_CHANGE_NOT_PROVEN:{day}:{reason}")

    class_b = [
        attempt for attempt in latest_by_day.values()
        if attempt.outcome == "BLOCKED" and attempt.blocking_reason == CLASS_B_BLOCKER
    ]
    if len(class_b) != 3:
        raise RuntimeError(f"CLASS_B_COUNT_MISMATCH:{len(class_b)}")
    for latest in class_b:
        valid, reason = validate_material_capability_change(latest, new, change)
        if valid or reason != "BLOCKING_REASON_NOT_EXPLICITLY_ADDRESSED":
            raise RuntimeError(f"CLASS_B_MUST_REMAIN_UNADDRESSED:{latest.target_date}:{reason}")

    return {
        "old_capability_id": OLD_CAPABILITY_ID,
        "old_fingerprint": OLD_FINGERPRINT,
        "new_capability_id": NEW_CAPABILITY_ID,
        "new_fingerprint": NEW_FINGERPRINT,
        "attempt_count": len(attempts),
        "class_a_retry_qualified": 14,
        "class_b_still_unaddressed": 3,
    }


def _change_payload(change: MaterialCapabilityChange) -> dict[str, object]:
    return {
        "change_id": change.change_id,
        "from_fingerprint": change.from_fingerprint,
        "to_fingerprint": change.to_fingerprint,
        "changed_dimensions": sorted(change.changed_dimensions),
        "added_proof_capabilities": sorted(change.added_proof_capabilities),
        "addresses_blocking_reasons": sorted(change.addresses_blocking_reasons),
        "qualification_contract": change.qualification_contract,
        "qualification_commit": change.qualification_commit,
    }


def apply_activation() -> None:
    validate_activation_preconditions()
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    attempts_before = deepcopy(ledger["attempts"])

    if NEW_CAPABILITY_ID in ledger["capabilities"]:
        raise RuntimeError("NEW_CAPABILITY_ALREADY_EXISTS")
    ledger["capabilities"][NEW_CAPABILITY_ID] = deepcopy(NEW_CAPABILITY_PAYLOAD)
    ledger["current_capability_id"] = NEW_CAPABILITY_ID
    registry["changes"].append(_change_payload(proposed_change()))

    if ledger["attempts"] != attempts_before:
        raise RuntimeError("HISTORICAL_ATTEMPTS_MUTATED_DURING_CAPABILITY_ACTIVATION")

    LEDGER_PATH.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    state = validate_activation_preconditions()
    print(json.dumps(state, indent=2, sort_keys=True))
    apply_activation()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
