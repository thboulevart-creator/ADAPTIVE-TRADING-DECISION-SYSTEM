from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from typing import Callable, Iterable, Mapping


EVENT_CONTRACT = "ATDS_MCEPR_EVENT_V0_1"
RELATION_CONTRACT = "ATDS_MCEPR_RELATION_V0_1"
SEGMENT_CONTRACT = "ATDS_MCEPR_REGISTRY_SEGMENT_V0_1"
SEGMENT_SCHEMA = "ATDS_MCEPR_REGISTRY_SEGMENT_V0_1"

EVENT_FIELDS = ("event_id", "event_core")
EVENT_CORE_FIELDS = (
    "occurred_at_utc",
    "operator",
    "nature",
    "declared_purpose",
    "source_refs",
    "asset",
    "period_start_utc",
    "period_end_utc",
    "consultation_intensity",
    "information_accessed",
    "evidence_refs",
)
RELATION_FIELDS = ("relation_id", "relation_core")
RELATION_CORE_FIELDS = (
    "source_ref",
    "relation_type",
    "target_ref",
    "relation_status",
    "basis_ref",
    "supersedes_relation_ref",
)
SEGMENT_FIELDS = ("schema", "registry_id", "parent_registry_ref", "events", "relations")

RELATION_TYPES = {
    "INFORMED_BY",
    "PREREGISTERED_BY",
    "RESERVED_FOR",
    "CLASSIFIED_BY",
}
RELATION_STATUSES = {"DECLARED", "ADJUDICATED", "DISPUTED", "UNKNOWN"}
INTENSITIES = {None, "I1", "I2", "I3"}

_SHA40 = r"[0-9a-f]{40}"
_SHA64 = r"[0-9a-f]{64}"
REF_PATTERNS = (
    re.compile(rf"^git_blob:{_SHA40}$"),
    re.compile(rf"^git_commit:{_SHA40}$"),
    re.compile(rf"^event:EVT-{_SHA64}$"),
    re.compile(rf"^relation:REL-{_SHA64}$"),
    re.compile(rf"^registry:RGS-{_SHA64}$"),
)
EVENT_ID_RE = re.compile(rf"^EVT-{_SHA64}$")
RELATION_ID_RE = re.compile(rf"^REL-{_SHA64}$")
REGISTRY_ID_RE = re.compile(rf"^RGS-{_SHA64}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class MCEPRFail(ValueError):
    """Intrinsic deterministic contract violation."""


class MCEPRBlocked(RuntimeError):
    """Safe conclusion unavailable because resolution/authority/chain is incomplete."""


def _raise_fail(message: str) -> None:
    raise MCEPRFail(message)


def _reject_numbers(value: object) -> None:
    if value is None or isinstance(value, (str, bool)):
        return
    if isinstance(value, (int, float)):
        _raise_fail("JSON numbers are forbidden in identity-bearing payloads")
    if isinstance(value, list):
        for item in value:
            _reject_numbers(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                _raise_fail("JSON object keys must be strings")
            _reject_numbers(item)
        return
    _raise_fail(f"unsupported identity-bearing value type: {type(value).__name__}")


def canonical_bytes(value: object) -> bytes:
    _reject_numbers(value)
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise MCEPRFail(f"value is not canonically serializable: {exc}") from exc


def _object_no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            _raise_fail(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def parse_json_strict(raw: bytes | str) -> object:
    if isinstance(raw, bytes):
        if raw.startswith(b"\xef\xbb\xbf"):
            _raise_fail("UTF-8 BOM is forbidden")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise MCEPRFail("JSON is not valid UTF-8") from exc
    elif isinstance(raw, str):
        text = raw
    else:
        _raise_fail("JSON input must be bytes or str")
    try:
        return json.loads(text, object_pairs_hook=_object_no_duplicates)
    except MCEPRFail:
        raise
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        raise MCEPRFail(f"invalid JSON: {exc}") from exc


def _exact_fields(value: object, expected: Iterable[str], label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        _raise_fail(f"{label} must be an object")
    expected_set = set(expected)
    actual_set = set(value)
    if actual_set != expected_set:
        missing = sorted(expected_set - actual_set)
        extra = sorted(actual_set - expected_set)
        _raise_fail(f"{label} fields mismatch; missing={missing}; extra={extra}")
    return value


def _non_empty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        _raise_fail(f"{label} must be a non-empty string")
    return value


def _utc(value: object, label: str, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or UTC_RE.fullmatch(value) is None:
        _raise_fail(f"{label} must be RFC3339 UTC whole-second YYYY-MM-DDTHH:MM:SSZ")
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise MCEPRFail(f"{label} is not a valid UTC timestamp") from exc
    return value


def _ref_kind(ref: str) -> str:
    for pattern in REF_PATTERNS:
        if pattern.fullmatch(ref):
            return ref.split(":", 1)[0]
    _raise_fail(f"invalid decisive reference: {ref}")


def _decisive_ref(value: object, label: str, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str):
        _raise_fail(f"{label} must be a decisive reference string")
    _ref_kind(value)
    return value


def _sorted_unique_refs(value: object, label: str) -> list[str]:
    if not isinstance(value, list):
        _raise_fail(f"{label} must be an array")
    refs: list[str] = []
    for item in value:
        ref = _decisive_ref(item, label)
        assert isinstance(ref, str)
        refs.append(ref)
    if refs != sorted(refs):
        _raise_fail(f"{label} must be lexicographically sorted")
    if len(refs) != len(set(refs)):
        _raise_fail(f"{label} must be duplicate-free")
    return refs


def _hash_id(prefix: str, payload: object) -> str:
    return prefix + hashlib.sha256(canonical_bytes(payload)).hexdigest()


def _validate_event_core(core: object) -> dict[str, object]:
    value = _exact_fields(core, EVENT_CORE_FIELDS, "event_core")
    _utc(value["occurred_at_utc"], "occurred_at_utc")
    _non_empty_string(value["operator"], "operator")
    _non_empty_string(value["nature"], "nature")
    _non_empty_string(value["declared_purpose"], "declared_purpose")
    _sorted_unique_refs(value["source_refs"], "source_refs")

    asset = value["asset"]
    if asset is not None:
        _non_empty_string(asset, "asset")

    start = _utc(value["period_start_utc"], "period_start_utc", nullable=True)
    end = _utc(value["period_end_utc"], "period_end_utc", nullable=True)
    if (start is None) != (end is None):
        _raise_fail("period boundaries must both be null or both be present")
    if start is not None and end is not None:
        if datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ") > datetime.strptime(
            end, "%Y-%m-%dT%H:%M:%SZ"
        ):
            _raise_fail("period_start_utc must be <= period_end_utc")

    intensity = value["consultation_intensity"]
    if intensity not in INTENSITIES:
        _raise_fail("invalid consultation_intensity")

    information_accessed = value["information_accessed"]
    if information_accessed is not None:
        _non_empty_string(information_accessed, "information_accessed")

    evidence = _sorted_unique_refs(value["evidence_refs"], "evidence_refs")
    if intensity is not None and not evidence:
        _raise_fail("consultation_intensity requires evidence_refs")
    if intensity == "I1" and information_accessed is None:
        _raise_fail("I1 requires information_accessed")
    return value


def make_event(event_core: object) -> dict[str, object]:
    core = _validate_event_core(event_core)
    payload = {"contract": EVENT_CONTRACT, "event_core": core}
    return {
        "event_id": _hash_id("EVT-", payload),
        "event_core": core,
    }


def _validate_event_record(event: object) -> dict[str, object]:
    value = _exact_fields(event, EVENT_FIELDS, "event")
    event_id = value["event_id"]
    if not isinstance(event_id, str) or EVENT_ID_RE.fullmatch(event_id) is None:
        _raise_fail("invalid event_id")
    expected = make_event(value["event_core"])
    if event_id != expected["event_id"]:
        _raise_fail("EVENT_ID/content mismatch")
    return value


def _validate_relation_core(core: object) -> dict[str, object]:
    value = _exact_fields(core, RELATION_CORE_FIELDS, "relation_core")
    _decisive_ref(value["source_ref"], "source_ref")
    relation_type = value["relation_type"]
    if relation_type not in RELATION_TYPES:
        _raise_fail("invalid relation_type")
    _decisive_ref(value["target_ref"], "target_ref")
    relation_status = value["relation_status"]
    if relation_status not in RELATION_STATUSES:
        _raise_fail("invalid relation_status")
    _decisive_ref(value["basis_ref"], "basis_ref")
    _decisive_ref(value["supersedes_relation_ref"], "supersedes_relation_ref", nullable=True)
    return value


def make_relation(relation_core: object) -> dict[str, object]:
    core = _validate_relation_core(relation_core)
    payload = {"contract": RELATION_CONTRACT, "relation_core": core}
    return {
        "relation_id": _hash_id("REL-", payload),
        "relation_core": core,
    }


def _validate_relation_record(relation: object) -> dict[str, object]:
    value = _exact_fields(relation, RELATION_FIELDS, "relation")
    relation_id = value["relation_id"]
    if not isinstance(relation_id, str) or RELATION_ID_RE.fullmatch(relation_id) is None:
        _raise_fail("invalid relation_id")
    expected = make_relation(value["relation_core"])
    if relation_id != expected["relation_id"]:
        _raise_fail("RELATION_ID/content mismatch")
    return value


def _strictly_sorted_unique_ids(records: object, id_field: str, label: str) -> list[dict[str, object]]:
    if not isinstance(records, list):
        _raise_fail(f"{label} must be an array")
    typed: list[dict[str, object]] = []
    ids: list[str] = []
    for record in records:
        if not isinstance(record, dict):
            _raise_fail(f"{label} entries must be objects")
        identifier = record.get(id_field)
        if not isinstance(identifier, str):
            _raise_fail(f"{label} entry missing string {id_field}")
        typed.append(record)
        ids.append(identifier)
    if ids != sorted(ids):
        _raise_fail(f"{label} must be strictly sorted by {id_field}")
    if len(ids) != len(set(ids)):
        _raise_fail(f"{label} must be duplicate-free")
    return typed


def make_segment(
    parent_registry_ref: object,
    events: object,
    relations: object,
) -> dict[str, object]:
    parent = _decisive_ref(parent_registry_ref, "parent_registry_ref", nullable=True)
    if parent is not None and _ref_kind(parent) != "registry":
        _raise_fail("parent_registry_ref must be a registry reference")

    event_records = _strictly_sorted_unique_ids(events, "event_id", "events")
    relation_records = _strictly_sorted_unique_ids(relations, "relation_id", "relations")
    for event in event_records:
        _validate_event_record(event)
    for relation in relation_records:
        _validate_relation_record(relation)
    if not event_records and not relation_records:
        _raise_fail("empty registry segment is forbidden")

    core = {
        "schema": SEGMENT_SCHEMA,
        "parent_registry_ref": parent,
        "events": event_records,
        "relations": relation_records,
    }
    payload = {"contract": SEGMENT_CONTRACT, "segment_core": core}
    return {
        "schema": SEGMENT_SCHEMA,
        "registry_id": _hash_id("RGS-", payload),
        "parent_registry_ref": parent,
        "events": event_records,
        "relations": relation_records,
    }


def _validate_segment_record(segment: object, filename: str) -> dict[str, object]:
    value = _exact_fields(segment, SEGMENT_FIELDS, "registry segment")
    if value["schema"] != SEGMENT_SCHEMA:
        _raise_fail("invalid registry segment schema")
    registry_id = value["registry_id"]
    if not isinstance(registry_id, str) or REGISTRY_ID_RE.fullmatch(registry_id) is None:
        _raise_fail("invalid registry_id")
    if filename != registry_id + ".json":
        _raise_fail("segment filename does not match registry_id")
    expected = make_segment(
        value["parent_registry_ref"],
        value["events"],
        value["relations"],
    )
    if registry_id != expected["registry_id"]:
        _raise_fail("REGISTRY_ID/content mismatch")
    return value


def _resolve_git(ref: str, resolver: Callable[[str], bool]) -> None:
    try:
        resolved = resolver(ref)
    except Exception as exc:
        raise MCEPRBlocked(f"git reference resolution unavailable: {ref}") from exc
    if resolved is not True:
        raise MCEPRBlocked(f"unresolved immutable git reference: {ref}")


def validate_registry_files(
    registry_files: Mapping[str, bytes | str],
    *,
    git_resolver: Callable[[str], bool],
    adjudication_basis_allowlist: set[str],
) -> dict[str, object]:
    if not isinstance(registry_files, Mapping) or not registry_files:
        raise MCEPRBlocked("registry segment set is empty or unavailable")
    if not callable(git_resolver):
        raise MCEPRBlocked("git resolver unavailable")
    if not isinstance(adjudication_basis_allowlist, set):
        raise MCEPRBlocked("adjudication basis allowlist unavailable")

    segments_by_id: dict[str, dict[str, object]] = {}
    filenames_by_id: dict[str, str] = {}

    for filename, raw in registry_files.items():
        if not isinstance(filename, str) or not filename:
            _raise_fail("registry filename must be a non-empty string")
        segment = parse_json_strict(raw)
        value = _validate_segment_record(segment, filename)
        registry_id = value["registry_id"]
        assert isinstance(registry_id, str)
        if registry_id in segments_by_id:
            _raise_fail("duplicate registry_id")
        segments_by_id[registry_id] = value
        filenames_by_id[registry_id] = filename

    genesis_ids: list[str] = []
    children: dict[str, list[str]] = {}
    for registry_id, segment in segments_by_id.items():
        parent_ref = segment["parent_registry_ref"]
        if parent_ref is None:
            genesis_ids.append(registry_id)
            continue
        assert isinstance(parent_ref, str)
        parent_id = parent_ref.split(":", 1)[1]
        if parent_id not in segments_by_id:
            raise MCEPRBlocked(f"missing parent registry segment: {parent_ref}")
        children.setdefault(parent_id, []).append(registry_id)

    if len(genesis_ids) != 1:
        raise MCEPRBlocked("registry must contain exactly one genesis")
    if any(len(child_ids) > 1 for child_ids in children.values()):
        raise MCEPRBlocked("REGISTRY_FORK: one parent has multiple children")

    genesis = genesis_ids[0]
    order: list[str] = []
    seen: set[str] = set()
    current = genesis
    while True:
        if current in seen:
            raise MCEPRBlocked("registry cycle prevents unique linear head")
        seen.add(current)
        order.append(current)
        next_ids = children.get(current, [])
        if not next_ids:
            break
        current = next_ids[0]

    if len(seen) != len(segments_by_id):
        raise MCEPRBlocked("registry graph is disconnected or has no unique linear head")

    event_records: dict[str, dict[str, object]] = {}
    relation_records: dict[str, dict[str, object]] = {}
    active_relations: set[str] = set()
    direct_successor: dict[str, str] = {}

    for registry_id in order:
        segment = segments_by_id[registry_id]
        current_events: dict[str, dict[str, object]] = {}
        current_relations: dict[str, dict[str, object]] = {}

        for event in segment["events"]:
            assert isinstance(event, dict)
            event_id = event["event_id"]
            assert isinstance(event_id, str)
            if event_id in event_records:
                _raise_fail("event_id already present in ancestor chain")
            current_events[event_id] = event

        for relation in segment["relations"]:
            assert isinstance(relation, dict)
            relation_id = relation["relation_id"]
            assert isinstance(relation_id, str)
            if relation_id in relation_records:
                _raise_fail("relation_id already present in ancestor chain")
            current_relations[relation_id] = relation

        available_event_ids = set(event_records) | set(current_events)
        ancestor_relation_ids = set(relation_records)

        for event in current_events.values():
            core = event["event_core"]
            assert isinstance(core, dict)
            for ref in [*core["source_refs"], *core["evidence_refs"]]:
                assert isinstance(ref, str)
                kind = _ref_kind(ref)
                if kind in {"git_blob", "git_commit"}:
                    _resolve_git(ref, git_resolver)
                elif kind == "event":
                    target = ref.split(":", 1)[1]
                    if target not in available_event_ids:
                        raise MCEPRBlocked(f"unresolved event reference: {ref}")
                elif kind == "relation":
                    target = ref.split(":", 1)[1]
                    if target not in ancestor_relation_ids:
                        _raise_fail("event cannot reference a current/unresolved relation")
                elif kind == "registry":
                    target = ref.split(":", 1)[1]
                    if target not in seen or order.index(target) >= order.index(registry_id):
                        raise MCEPRBlocked(f"unresolved/non-ancestor registry reference: {ref}")

        for relation in current_relations.values():
            relation_id = relation["relation_id"]
            core = relation["relation_core"]
            assert isinstance(relation_id, str)
            assert isinstance(core, dict)

            for field in ("source_ref", "target_ref", "basis_ref"):
                ref = core[field]
                assert isinstance(ref, str)
                kind = _ref_kind(ref)
                target = ref.split(":", 1)[1]
                if kind in {"git_blob", "git_commit"}:
                    _resolve_git(ref, git_resolver)
                elif kind == "event":
                    if target not in available_event_ids:
                        raise MCEPRBlocked(f"unresolved event reference: {ref}")
                elif kind == "relation":
                    if target not in ancestor_relation_ids:
                        _raise_fail("same-segment or unresolved relation reference is forbidden")
                elif kind == "registry":
                    if target not in order[: order.index(registry_id)]:
                        raise MCEPRBlocked(f"unresolved/non-ancestor registry reference: {ref}")

            if core["relation_status"] == "ADJUDICATED":
                basis = core["basis_ref"]
                assert isinstance(basis, str)
                if _ref_kind(basis) != "git_blob" or basis not in adjudication_basis_allowlist:
                    raise MCEPRBlocked(
                        "ADJUDICATED relation lacks separately human-authorized adjudication basis"
                    )

            supersedes_ref = core["supersedes_relation_ref"]
            if supersedes_ref is not None:
                assert isinstance(supersedes_ref, str)
                if _ref_kind(supersedes_ref) != "relation":
                    _raise_fail("supersedes_relation_ref must be a relation reference")
                previous_id = supersedes_ref.split(":", 1)[1]
                if previous_id not in ancestor_relation_ids:
                    _raise_fail("supersedes relation does not resolve to an ancestor relation")
                if previous_id not in active_relations:
                    _raise_fail("superseded relation is not currently active")
                if previous_id in direct_successor:
                    _raise_fail("relation already has a direct successor")

                previous = relation_records[previous_id]
                previous_core = previous["relation_core"]
                assert isinstance(previous_core, dict)
                for stable_field in ("source_ref", "relation_type", "target_ref"):
                    if core[stable_field] != previous_core[stable_field]:
                        _raise_fail(
                            f"supersession must preserve {stable_field}"
                        )
                direct_successor[previous_id] = relation_id
                active_relations.remove(previous_id)
            active_relations.add(relation_id)

        event_records.update(current_events)
        relation_records.update(current_relations)

    head_id = order[-1]
    return {
        "status": "PASS",
        "head_ref": "registry:" + head_id,
        "event_ids": tuple(event_records.keys()),
        "relation_ids": tuple(relation_records.keys()),
    }
