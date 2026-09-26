from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any, Iterable, Mapping, Sequence

from .classification import SemanticRecord
from .rendering import artifact_record_id, relation_record_id


class RelationError(RuntimeError):
    """Raised when typed relation generation cannot fail closed."""


@dataclass(frozen=True)
class RelationRecord:
    projection_relation_id: str
    source_record_id: str
    relation_type: str
    target_record_id: str
    basis: str
    evidence_source_path: str
    evidence_source_blob_sha: str
    source_commit: str


def _walk_json_strings(
    value: Any,
) -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            label = str(key)
            if isinstance(child, str):
                yield label, child
            else:
                for nested_label, nested_value in _walk_json_strings(
                    child
                ):
                    yield (
                        f"{label}.{nested_label}"
                        if nested_label
                        else label,
                        nested_value,
                    )
        return

    if isinstance(value, list):
        for child in value:
            if isinstance(child, str):
                yield "[]", child
            else:
                yield from _walk_json_strings(child)


def _structured_targets(
    text: str,
    exact_paths: set[str],
) -> set[str]:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return set()

    targets: set[str] = set()

    for _label, value in _walk_json_strings(parsed):
        candidate = value.strip()
        if candidate in exact_paths:
            targets.add(candidate)

    return targets


_LABELED_BACKTICK_PATH = re.compile(
    r"^\s*(?:[-*]\s*)?"
    r"[^:\n]{1,120}:\s*"
    r"\x60([^\x60\r\n]+)\x60"
    r"(?:\s*[.;,]?\s*)$"
)


def _labeled_text_targets(
    text: str,
    exact_paths: set[str],
) -> set[str]:
    targets: set[str] = set()

    for line in text.splitlines():
        match = _LABELED_BACKTICK_PATH.match(line)
        if not match:
            continue
        candidate = match.group(1).strip()
        if candidate in exact_paths:
            targets.add(candidate)

    return targets


def _ensure_reference_rules(
    contract: Mapping[str, Any],
) -> None:
    rules = {
        rule["rule_id"]: rule
        for rule in contract[
            "preregistered_relation_rules"
        ]
    }

    structured = rules.get(
        "REL-V0-EXACT-STRUCTURED-PATH"
    )
    labeled = rules.get(
        "REL-V0-EXPLICIT-LABELED-TEXT-PATH"
    )

    if structured is None or labeled is None:
        raise RelationError(
            "required preregistered reference rules missing"
        )

    for rule in (structured, labeled):
        if "REFERENCES" not in rule["allowed_types"]:
            raise RelationError(
                f"REFERENCES not allowed by {rule['rule_id']}"
            )


def _make_relation(
    *,
    source_record_id: str,
    target_record_id: str,
    basis: str,
    evidence_source_path: str,
    evidence_source_blob_sha: str,
    source_commit: str,
    contract: Mapping[str, Any],
) -> RelationRecord:
    relation_contract = contract["relation_record"]

    if "REFERENCES" not in relation_contract[
        "allowed_relation_types"
    ]:
        raise RelationError(
            "REFERENCES is not an allowed relation type"
        )

    if basis not in relation_contract["allowed_basis"]:
        raise RelationError(
            f"basis is not authoritative: {basis}"
        )

    if basis in relation_contract[
        "forbidden_authoritative_basis"
    ]:
        raise RelationError(
            f"forbidden authoritative basis: {basis}"
        )

    relation_id = relation_record_id(
        source_record_id,
        "REFERENCES",
        target_record_id,
        basis,
        evidence_source_path,
        evidence_source_blob_sha,
    )

    return RelationRecord(
        projection_relation_id=relation_id,
        source_record_id=source_record_id,
        relation_type="REFERENCES",
        target_record_id=target_record_id,
        basis=basis,
        evidence_source_path=evidence_source_path,
        evidence_source_blob_sha=evidence_source_blob_sha,
        source_commit=source_commit,
    )


def extract_relations(
    source: Any,
    records: Sequence[SemanticRecord],
    contract: Mapping[str, Any],
) -> tuple[RelationRecord, ...]:
    _ensure_reference_rules(contract)

    by_path = {
        record.source_path: record
        for record in records
    }
    if len(by_path) != len(records):
        raise RelationError(
            "duplicate source_path in semantic records"
        )

    record_ids: dict[str, str] = {}
    reverse_ids: dict[str, str] = {}

    for record in records:
        projection_id = artifact_record_id(
            record.source_repository,
            record.source_path,
        )
        previous = reverse_ids.get(projection_id)
        if previous is not None and previous != record.source_path:
            raise RelationError(
                "artifact projection ID collision between "
                f"{previous} and {record.source_path}"
            )
        reverse_ids[projection_id] = record.source_path
        record_ids[record.source_path] = projection_id

    exact_paths = set(by_path)
    emitted: dict[str, RelationRecord] = {}

    for record in sorted(
        records,
        key=lambda item: item.source_path,
    ):
        raw = source.read_blob(
            record.source_blob_sha
        )
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise RelationError(
                f"non-UTF8 relation source: "
                f"{record.source_path}"
            ) from exc

        source_id = record_ids[record.source_path]
        suffix = PurePosixPath(
            record.source_path
        ).suffix.lower()

        candidates: list[tuple[str, str]] = []

        if suffix == ".json":
            for target in sorted(
                _structured_targets(
                    text,
                    exact_paths,
                )
            ):
                candidates.append(
                    ("EXPLICIT_STRUCTURED", target)
                )

        if suffix == ".md":
            for target in sorted(
                _labeled_text_targets(
                    text,
                    exact_paths,
                )
            ):
                candidates.append(
                    ("EXPLICIT_TEXT", target)
                )

        for basis, target_path in candidates:
            if target_path == record.source_path:
                continue

            target_id = record_ids.get(
                target_path
            )
            if target_id is None:
                continue

            relation = _make_relation(
                source_record_id=source_id,
                target_record_id=target_id,
                basis=basis,
                evidence_source_path=record.source_path,
                evidence_source_blob_sha=record.source_blob_sha,
                source_commit=record.source_commit,
                contract=contract,
            )

            existing = emitted.get(
                relation.projection_relation_id
            )
            if existing is not None and existing != relation:
                raise RelationError(
                    "relation projection ID collision"
                )
            emitted[
                relation.projection_relation_id
            ] = relation

    return tuple(
        emitted[key]
        for key in sorted(emitted)
    )
