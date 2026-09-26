from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any, Mapping, Sequence

from .classification import SemanticRecord


class RenderingError(RuntimeError):
    """Raised when deterministic projection rendering cannot fail closed."""


@dataclass(frozen=True)
class RenderedFile:
    relative_path: str
    content: bytes

    @property
    def size_bytes(self) -> int:
        return len(self.content)

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.content).hexdigest()


def _first16_sha256(parts: Sequence[str]) -> str:
    payload = b"\0".join(
        part.encode("utf-8")
        for part in parts
    )
    return hashlib.sha256(payload).hexdigest()[:16]


def artifact_record_id(
    source_repository: str,
    source_path: str,
) -> str:
    return "A-" + _first16_sha256(
        (source_repository, source_path)
    )


def relation_record_id(
    source_record_id: str,
    relation_type: str,
    target_record_id: str,
    basis: str,
    evidence_source_path: str,
    evidence_source_blob_sha: str,
) -> str:
    return "R-" + _first16_sha256(
        (
            source_record_id,
            relation_type,
            target_record_id,
            basis,
            evidence_source_path,
            evidence_source_blob_sha,
        )
    )


def _encode_frontmatter_value(value: Any) -> str:
    if value is None:
        return "null"

    if isinstance(value, bool):
        return "true" if value else "false"

    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)

    if isinstance(value, str):
        return json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
        )

    if isinstance(value, (list, tuple)):
        if not all(isinstance(item, str) for item in value):
            raise RenderingError(
                "frontmatter arrays may contain strings only"
            )
        return json.dumps(
            list(value),
            ensure_ascii=False,
            separators=(",", ":"),
        )

    raise RenderingError(
        f"unsupported frontmatter value type: "
        f"{type(value).__name__}"
    )


def render_frontmatter(
    values: Mapping[str, Any],
    field_order: Sequence[str],
) -> bytes:
    expected = list(field_order)
    actual = list(values.keys())

    if set(actual) != set(expected):
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        raise RenderingError(
            f"frontmatter field mismatch: "
            f"missing={missing} extra={extra}"
        )

    lines = ["---"]
    for field in expected:
        lines.append(
            f"{field}: "
            f"{_encode_frontmatter_value(values[field])}"
        )
    lines.append("---")

    raw = ("\n".join(lines) + "\n").encode("utf-8")

    if raw.startswith(b"\xef\xbb\xbf"):
        raise RenderingError("UTF-8 BOM is forbidden")
    if b"\r" in raw:
        raise RenderingError("CR/CRLF output is forbidden")

    return raw


def _code_span(value: str) -> str:
    if "\x60" in value:
        raise RenderingError(
            "backtick in deterministic Markdown code span"
        )
    if any(ord(char) < 32 for char in value):
        raise RenderingError(
            "control character in deterministic Markdown body"
        )
    return "\x60" + value + "\x60"


def _validate_source_path(source_path: str) -> None:
    if not source_path:
        raise RenderingError("empty source_path")
    if source_path.startswith(("/", "\\")):
        raise RenderingError("absolute source_path forbidden")
    if (
        len(source_path) >= 3
        and source_path[1] == ":"
        and source_path[2] in "\\/"
    ):
        raise RenderingError(
            "Windows absolute source_path forbidden"
        )
    if "\\" in source_path:
        raise RenderingError(
            "source_path must use repository POSIX separators"
        )
    if ".." in PurePosixPath(source_path).parts:
        raise RenderingError(
            "source_path parent traversal forbidden"
        )
    if any(ord(char) < 32 for char in source_path):
        raise RenderingError(
            "control character in source_path"
        )


def artifact_frontmatter(
    record: SemanticRecord,
    contract: Mapping[str, Any],
) -> tuple[str, dict[str, Any]]:
    _validate_source_path(record.source_path)
    artifact_contract = contract["artifact_record"]
    projection_id = artifact_record_id(
        record.source_repository,
        record.source_path,
    )

    values: dict[str, Any] = {
        "record_schema":
            artifact_contract["record_schema"],
        "record_type":
            artifact_contract["record_type"],
        "projection_record_id":
            projection_id,
        "source_repository":
            record.source_repository,
        "source_branch":
            record.source_branch,
        "source_commit":
            record.source_commit,
        "source_tree":
            record.source_tree,
        "source_path":
            record.source_path,
        "source_blob_sha":
            record.source_blob_sha,
        "source_blob_size":
            record.source_blob_size,
        "artifact_family":
            record.artifact_family,
        "semantic_role":
            record.semantic_role,
        "procedure_role":
            record.procedure_role,
        "source_authority_role":
            record.authority_role,
        "projection_authority_role":
            "DERIVED",
        "qualification_status":
            record.qualification_status,
        "qualification_scope":
            record.qualification_scope,
        "scientific_status":
            record.scientific_status,
        "epistemic_role":
            record.epistemic_role,
        "temporal_role":
            record.temporal_role,
        "persistence_state":
            record.persistence_state,
        "source_freshness":
            "UNKNOWN",
        "projection_integrity":
            "CLEAN",
        "limitations":
            list(record.limitations),
        "non_claims":
            list(record.non_claims),
    }

    return projection_id, values


def render_artifact(
    record: SemanticRecord,
    contract: Mapping[str, Any],
) -> RenderedFile:
    projection_id, values = artifact_frontmatter(
        record,
        contract,
    )

    frontmatter = render_frontmatter(
        values,
        contract["artifact_record"][
            "frontmatter_field_order"
        ],
    )

    body = (
        f"# {projection_id}\n\n"
        f"Source artifact: {_code_span(record.source_path)}\n"
    ).encode("utf-8")

    content = frontmatter + body

    if b"\r" in content:
        raise RenderingError("CR/CRLF output is forbidden")
    if content.startswith(b"\xef\xbb\xbf"):
        raise RenderingError("UTF-8 BOM is forbidden")
    if not content.endswith(b"\n"):
        raise RenderingError(
            "deterministic Markdown must end with LF"
        )

    return RenderedFile(
        relative_path=(
            f"generated/artifacts/{projection_id}.md"
        ),
        content=content,
    )


def render_relation(
    relation: Any,
    contract: Mapping[str, Any],
) -> RenderedFile:
    relation_contract = contract["relation_record"]

    values: dict[str, Any] = {
        "record_schema":
            relation_contract["record_schema"],
        "record_type":
            relation_contract["record_type"],
        "projection_relation_id":
            relation.projection_relation_id,
        "source_record_id":
            relation.source_record_id,
        "relation_type":
            relation.relation_type,
        "target_record_id":
            relation.target_record_id,
        "basis":
            relation.basis,
        "evidence_source_path":
            relation.evidence_source_path,
        "evidence_source_blob_sha":
            relation.evidence_source_blob_sha,
        "source_commit":
            relation.source_commit,
        "projection_authority_role":
            "DERIVED",
        "projection_integrity":
            "CLEAN",
    }

    frontmatter = render_frontmatter(
        values,
        relation_contract["frontmatter_field_order"],
    )

    body = (
        f"# {relation.projection_relation_id}\n\n"
        f"{relation.source_record_id} "
        f"—[{relation.relation_type}]→ "
        f"{relation.target_record_id}\n"
    ).encode("utf-8")

    content = frontmatter + body

    if b"\r" in content:
        raise RenderingError("CR/CRLF output is forbidden")
    if content.startswith(b"\xef\xbb\xbf"):
        raise RenderingError("UTF-8 BOM is forbidden")
    if not content.endswith(b"\n"):
        raise RenderingError(
            "deterministic Markdown must end with LF"
        )

    return RenderedFile(
        relative_path=(
            "generated/relations/"
            f"{relation.projection_relation_id}.md"
        ),
        content=content,
    )
