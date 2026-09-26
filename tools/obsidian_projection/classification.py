from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import PurePosixPath
from typing import Any, Mapping

from .inventory import (
    FrozenInventory,
    InventoryEntry,
    verify_inventory,
)

_RECORD_SCHEMA = "ATDS_OBSIDIAN_SEMANTIC_RECORD_V0_1"


class ClassificationError(RuntimeError):
    """Raised when P1 semantic classification cannot fail closed."""


@dataclass(frozen=True)
class SemanticRecord:
    record_schema: str
    record_type: str
    source_repository: str
    source_branch: str
    source_commit: str
    source_tree: str
    source_path: str
    source_blob_sha: str
    source_blob_size: int
    artifact_family: str
    semantic_role: str
    procedure_role: str
    authority_role: str
    qualification_status: str
    qualification_scope: str | None
    scientific_status: str
    epistemic_role: str
    temporal_role: str
    persistence_state: str
    limitations: tuple[str, ...]
    non_claims: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["limitations"] = list(self.limitations)
        data["non_claims"] = list(self.non_claims)
        return data


def git_blob_oid(raw: bytes) -> str:
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def _decode_utf8(raw: bytes, source_path: str) -> str:
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ClassificationError(
            f"semantic source is not UTF-8: {source_path}"
        ) from exc


def _artifact_family(entry: InventoryEntry) -> str:
    suffix = PurePosixPath(entry.source_path).suffix.lower()

    if entry.inventory_class == "IMPLEMENTATION" and suffix == ".py":
        return "CODE"
    if entry.inventory_class == "TEST" and suffix == ".py":
        return "TEST"
    if entry.inventory_class == "BREAKER" and suffix == ".py":
        return "BREAKER"
    if entry.inventory_class == "EVIDENCE":
        return "EVIDENCE"
    if entry.inventory_class == "CORE_PROFILE" and suffix == ".json":
        return "EVIDENCE"
    if suffix == ".md":
        return "DOCUMENT"

    raise ClassificationError(
        f"no preregistered artifact_family rule for "
        f"{entry.source_path} class={entry.inventory_class}"
    )


def _heading_sections(text: str) -> dict[str, str]:
    lines = text.splitlines()
    found: dict[str, list[str]] = {}
    current: str | None = None

    for line in lines:
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            current = match.group(1).strip()
            found.setdefault(current, [])
            continue
        if current is not None:
            found[current].append(line)

    return {
        heading: "\n".join(body)
        for heading, body in found.items()
    }


def _normalize_heading(heading: str) -> str:
    lowered = heading.casefold()
    lowered = re.sub(r"^[0-9]+(?:\.[0-9]+)*[.)]?\s*", "", lowered)
    return lowered.strip()


def _bullet_items(section: str) -> tuple[str, ...]:
    items: list[str] = []
    for line in section.splitlines():
        match = re.match(r"^\s*[-*]\s+(.+?)\s*$", line)
        if match:
            value = match.group(1).strip()
            if value and value not in items:
                items.append(value)
    return tuple(items)


def _extract_limitations(text: str) -> tuple[str, ...]:
    sections = _heading_sections(text)
    collected: list[str] = []

    for heading, body in sections.items():
        normalized = _normalize_heading(heading)
        if normalized in {"limitations", "limites"}:
            for item in _bullet_items(body):
                if item not in collected:
                    collected.append(item)

    return tuple(collected)


def _extract_scope_negative_list(text: str) -> tuple[str, ...]:
    sections = _heading_sections(text)
    collected: list[str] = []

    for heading, body in sections.items():
        if _normalize_heading(heading) != "scope":
            continue

        lines = body.splitlines()
        capture = False

        for line in lines:
            stripped = line.strip()
            normalized = stripped.casefold()

            if normalized in {
                "it is not:",
                "this is not:",
                "il ne s'agit pas de :",
                "il ne s’agit pas de :",
            }:
                capture = True
                continue

            if capture:
                match = re.match(r"^\s*[-*]\s+(.+?)\s*$", line)
                if match:
                    value = match.group(1).strip()
                    if value and value not in collected:
                        collected.append(value)
                    continue

                if stripped:
                    capture = False

    return tuple(collected)


def _extract_non_claims(text: str) -> tuple[str, ...]:
    sections = _heading_sections(text)
    collected: list[str] = []

    for heading, body in sections.items():
        normalized = _normalize_heading(heading)
        if normalized in {
            "non-promotions",
            "non promotions",
        }:
            for item in _bullet_items(body):
                if item not in collected:
                    collected.append(item)

    for item in _extract_scope_negative_list(text):
        if item not in collected:
            collected.append(item)

    return tuple(collected)


def _first_h1(text: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return ""


def _has_verdict_section(text: str) -> bool:
    return any(
        _normalize_heading(heading) == "verdict"
        for heading in _heading_sections(text)
    )


def _candidate_procedure_role(
    text: str,
    entry: InventoryEntry,
    parsed_json: object | None,
) -> str:
    h1 = _first_h1(text).casefold()
    sections = {
        _normalize_heading(heading)
        for heading in _heading_sections(text)
    }
    has_verdict = _has_verdict_section(text)

    if (
        has_verdict
        and "adjudication" in h1
        and (
            "inputs" in sections
            or "evidence exacte" in sections
            or "evidence qualifiée" in sections
            or "evidence exacte reçue" in sections
            or "promotion gate" in sections
            or "epistemic review" in sections
        )
    ):
        return "ADJUDICATION"

    if (
        has_verdict
        and "preflight" in h1
        and (
            "objet" in sections
            or "purpose" in sections
            or "interdictions" in sections
            or "scope" in sections
        )
    ):
        return "PREFLIGHT"

    if (
        has_verdict
        and (
            "revue adversariale" in h1
            or "adversarial review" in h1
        )
        and (
            "attaques" in sections
            or re.search(r"^###\s+[A-Z]?\d+\b", text, re.MULTILINE)
        )
    ):
        return "ADVERSARIAL_REVIEW"

    if (
        entry.inventory_class == "HISTORICAL_LINEAGE"
        and "handoff" in h1
    ):
        return "HANDOFF"

    if isinstance(parsed_json, dict) and parsed_json:
        values = list(parsed_json.values())
        if all(
            isinstance(value, str)
            and value in {"KILLED", "SURVIVED"}
            for value in values
        ):
            return "TEST_RESULT"

    return "NONE"


def _candidate_semantic_role(
    text: str,
    entry: InventoryEntry,
    procedure_role: str,
    parsed_json: object | None,
) -> str:
    lowered = text.casefold()

    if (
        entry.inventory_class == "GOVERNANCE_ANCHOR"
        and "authoritative home for validated governance rules"
        in lowered
    ):
        return "GOVERNANCE"

    if (
        entry.inventory_class == "CORE_PROTOCOL"
        and "protocol" in _first_h1(text).casefold()
        and "candidate foundation" in lowered
    ):
        return "PROTOCOL"

    if procedure_role == "ADJUDICATION":
        return "DECISION"
    if procedure_role == "PREFLIGHT":
        return "SPECIFICATION"
    if procedure_role == "ADVERSARIAL_REVIEW":
        return "RESULT"
    if procedure_role == "HANDOFF":
        return "HISTORICAL_RECORD"
    if procedure_role == "TEST_RESULT":
        return "RESULT"

    if isinstance(parsed_json, dict):
        if any(
            key in parsed_json
            for key in ("status", "schema", "scope", "coverage")
        ):
            return "RESULT"

    if entry.inventory_class in {"TEST", "BREAKER", "IMPLEMENTATION"}:
        return "COMPONENT"

    return "UNKNOWN"


def _candidate_temporal_role(
    text: str,
    entry: InventoryEntry,
) -> str:
    if entry.inventory_class != "HISTORICAL_LINEAGE":
        return "UNKNOWN"

    lowered = text.casefold()
    if (
        "session" in lowered
        or "attempt" in lowered
        or "tentative" in lowered
        or "handoff" in lowered
    ):
        return "HISTORICAL"

    return "UNKNOWN"


def _parse_json_if_applicable(
    text: str,
    entry: InventoryEntry,
) -> object | None:
    if PurePosixPath(entry.source_path).suffix.lower() != ".json":
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ClassificationError(
            f"invalid JSON evidence: {entry.source_path}"
        ) from exc


def _fixture_for(
    rules: Mapping[str, Any],
    entry: InventoryEntry,
) -> Mapping[str, Any] | None:
    for fixture in rules.get("exact_fixtures", []):
        if (
            fixture.get("source_path") == entry.source_path
            and fixture.get("source_blob_sha")
            == entry.source_blob_sha
        ):
            return fixture
    return None


def classify_record(
    inventory: FrozenInventory,
    entry: InventoryEntry,
    raw: bytes,
    rules: Mapping[str, Any],
) -> SemanticRecord:
    if len(raw) != entry.source_blob_size:
        raise ClassificationError(
            f"raw byte size mismatch for {entry.source_path}: "
            f"expected={entry.source_blob_size} actual={len(raw)}"
        )

    actual_oid = git_blob_oid(raw)
    if actual_oid != entry.source_blob_sha:
        raise ClassificationError(
            f"raw Git blob identity mismatch for {entry.source_path}: "
            f"expected={entry.source_blob_sha} actual={actual_oid}"
        )

    if rules.get("source_commit") != inventory.source_commit:
        raise ClassificationError(
            "classification rules/source commit mismatch"
        )
    if rules.get("source_tree") != inventory.source_tree:
        raise ClassificationError(
            "classification rules/source tree mismatch"
        )
    if rules.get("pilot_source_count") != inventory.source_artifact_count:
        raise ClassificationError(
            "classification rules/source count mismatch"
        )

    text = _decode_utf8(raw, entry.source_path)
    parsed_json = _parse_json_if_applicable(text, entry)

    defaults = rules["defaults"]
    procedure_role = _candidate_procedure_role(
        text,
        entry,
        parsed_json,
    )
    semantic_role = _candidate_semantic_role(
        text,
        entry,
        procedure_role,
        parsed_json,
    )
    temporal_role = _candidate_temporal_role(
        text,
        entry,
    )

    values: dict[str, Any] = {
        "semantic_role": semantic_role,
        "procedure_role": procedure_role,
        "qualification_status":
            defaults["qualification_status"],
        "qualification_scope": None,
        "scientific_status":
            defaults["scientific_status"],
        "epistemic_role":
            defaults["epistemic_role"],
        "temporal_role": temporal_role,
    }

    fixture = _fixture_for(rules, entry)
    if fixture is not None:
        expected = fixture.get("expected", {})
        for field in (
            "semantic_role",
            "procedure_role",
            "qualification_status",
            "qualification_scope",
            "scientific_status",
            "epistemic_role",
            "temporal_role",
        ):
            if field in expected:
                values[field] = expected[field]

    return SemanticRecord(
        record_schema=_RECORD_SCHEMA,
        record_type="ARTIFACT",
        source_repository=inventory.source_repository,
        source_branch=inventory.source_branch,
        source_commit=inventory.source_commit,
        source_tree=inventory.source_tree,
        source_path=entry.source_path,
        source_blob_sha=entry.source_blob_sha,
        source_blob_size=entry.source_blob_size,
        artifact_family=_artifact_family(entry),
        semantic_role=values["semantic_role"],
        procedure_role=values["procedure_role"],
        authority_role="CANONICAL",
        qualification_status=values["qualification_status"],
        qualification_scope=values["qualification_scope"],
        scientific_status=values["scientific_status"],
        epistemic_role=values["epistemic_role"],
        temporal_role=values["temporal_role"],
        persistence_state="TRACKED_IN_GIT_TREE",
        limitations=_extract_limitations(text),
        non_claims=_extract_non_claims(text),
    )


def classify_inventory(
    source: Any,
    inventory: FrozenInventory,
    rules: Mapping[str, Any],
) -> tuple[SemanticRecord, ...]:
    verified = verify_inventory(source, inventory)

    records: list[SemanticRecord] = []
    for item in verified:
        entry = item.inventory
        raw = source.read_blob(entry.source_blob_sha)
        records.append(
            classify_record(
                inventory,
                entry,
                raw,
                rules,
            )
        )

    records.sort(key=lambda record: record.source_path)
    return tuple(records)


def records_digest_sha256(
    records: tuple[SemanticRecord, ...],
) -> str:
    payload = [
        record.to_dict()
        for record in sorted(
            records,
            key=lambda record: record.source_path,
        )
    ]
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()
