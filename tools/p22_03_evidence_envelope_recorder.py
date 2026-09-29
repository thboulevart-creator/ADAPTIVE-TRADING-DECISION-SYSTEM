from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any

CONTRACT = "ATDS_P22_03_EVIDENCE_ENVELOPE_RECORDER_V0_1"
ENVELOPE_SCHEMA = "ATDS_P22_03_EVIDENCE_ENVELOPE_V0_1"

_REQUIRED_FIELDS = {
    "operation_id",
    "operation_class",
    "command_or_check",
    "start_head",
    "start_tree",
    "end_head",
    "end_tree",
    "exit_code",
    "stdout",
    "stderr",
    "files_changed",
    "test_results",
    "probe_results",
    "artifact_hashes",
    "started_at_utc",
    "finished_at_utc",
    "authority_reference",
    "final_status",
}

_OPERATION_CLASSES = {
    "READ_ONLY_INFORMATIONAL",
    "TEST_OR_PROBE",
    "MUTATION",
    "EXTERNAL_ACTION",
}

_FINAL_STATUSES = {
    "PASS",
    "FAIL",
    "BLOCKED",
    "UNKNOWN",
    "ABORTED",
}

_RESULT_STATUSES = {
    "PASS",
    "FAIL",
    "BLOCKED",
    "UNKNOWN",
    "ABORTED",
    "NOT_RUN",
}

_OID40 = re.compile(r"^[0-9a-fA-F]{40}$")
_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")


class P2203Error(ValueError):
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


def _safe_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if value.startswith("/") or value.startswith("\\") or ":" in value or "\\" in value:
        return False
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        return False
    return True


def _valid_git_identity(value: Any) -> bool:
    return value == "UNKNOWN" or (
        isinstance(value, str) and _OID40.fullmatch(value) is not None
    )


def _parse_utc_z(value: Any) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise P2203Error("UTC_TIMESTAMP")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise P2203Error("UTC_TIMESTAMP") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise P2203Error("UTC_TIMESTAMP")
    return parsed


def _validate_result_records(value: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise P2203Error(label)
    out: list[dict[str, Any]] = []
    for record in value:
        if not isinstance(record, dict):
            raise P2203Error(label)
        keys = set(record)
        if keys not in ({"name", "status"}, {"name", "status", "details"}):
            raise P2203Error(label)
        name = record.get("name")
        status = record.get("status")
        if not isinstance(name, str) or not name:
            raise P2203Error(label)
        if status not in _RESULT_STATUSES:
            raise P2203Error(label)
        canonical_json_bytes(record)
        out.append(copy.deepcopy(record))
    return out


def _validate_evidence(evidence: Any) -> dict[str, Any]:
    if not isinstance(evidence, dict) or set(evidence) != _REQUIRED_FIELDS:
        raise P2203Error("EVIDENCE_FIELDS")

    data = copy.deepcopy(evidence)

    if not isinstance(data["operation_id"], str) or not data["operation_id"]:
        raise P2203Error("OPERATION_ID")

    if data["operation_class"] not in _OPERATION_CLASSES:
        raise P2203Error("OPERATION_CLASS")

    if not isinstance(data["command_or_check"], str):
        raise P2203Error("COMMAND_OR_CHECK")

    for key in ("start_head", "start_tree", "end_head", "end_tree"):
        if not _valid_git_identity(data[key]):
            raise P2203Error("GIT_IDENTITY")

    exit_code = data["exit_code"]
    if exit_code != "UNKNOWN" and (
        not isinstance(exit_code, int) or isinstance(exit_code, bool)
    ):
        raise P2203Error("EXIT_CODE")

    if not isinstance(data["stdout"], str) or not isinstance(data["stderr"], str):
        raise P2203Error("STDIO")

    files_changed = data["files_changed"]
    if not isinstance(files_changed, list):
        raise P2203Error("FILES_CHANGED_PATH")
    if any(not _safe_relative_path(path) for path in files_changed):
        raise P2203Error("FILES_CHANGED_PATH")
    if len(files_changed) != len(set(files_changed)):
        raise P2203Error("FILES_CHANGED_DUPLICATE")

    data["test_results"] = _validate_result_records(
        data["test_results"], "TEST_RESULTS"
    )
    data["probe_results"] = _validate_result_records(
        data["probe_results"], "PROBE_RESULTS"
    )

    hashes = data["artifact_hashes"]
    if not isinstance(hashes, dict):
        raise P2203Error("ARTIFACT_HASH")
    normalized_hashes: dict[str, str] = {}
    for artifact_path, digest in hashes.items():
        if not _safe_relative_path(artifact_path):
            raise P2203Error("ARTIFACT_HASH")
        if not isinstance(digest, str) or _SHA256.fullmatch(digest) is None:
            raise P2203Error("ARTIFACT_HASH")
        normalized_hashes[artifact_path] = digest
    data["artifact_hashes"] = normalized_hashes

    started = _parse_utc_z(data["started_at_utc"])
    finished = _parse_utc_z(data["finished_at_utc"])
    if finished < started:
        raise P2203Error("TIME_ORDER")

    if (
        not isinstance(data["authority_reference"], str)
        or not data["authority_reference"]
    ):
        raise P2203Error("AUTHORITY_REFERENCE")

    if data["final_status"] not in _FINAL_STATUSES:
        raise P2203Error("FINAL_STATUS")

    canonical_json_bytes(data)
    return data


def build_evidence_envelope(evidence: dict[str, Any]) -> dict[str, Any]:
    data = _validate_evidence(evidence)

    body = {
        "schema": ENVELOPE_SCHEMA,
        **data,
        "envelope_authority": False,
        "operation_authorized_by_envelope": False,
    }

    envelope = {
        **body,
        "evidence_digest": canonical_sha256(body),
    }
    canonical_json_bytes(envelope)
    return envelope


def validate_evidence_envelope(envelope: Any) -> dict[str, Any]:
    if not isinstance(envelope, dict):
        return {"status": "INVALID_ENVELOPE"}

    expected_fields = {
        "schema",
        *_REQUIRED_FIELDS,
        "envelope_authority",
        "operation_authorized_by_envelope",
        "evidence_digest",
    }
    if set(envelope) != expected_fields:
        return {"status": "INVALID_ENVELOPE"}

    if envelope.get("schema") != ENVELOPE_SCHEMA:
        return {"status": "INVALID_ENVELOPE"}
    if envelope.get("envelope_authority") is not False:
        return {"status": "INVALID_ENVELOPE"}
    if envelope.get("operation_authorized_by_envelope") is not False:
        return {"status": "INVALID_ENVELOPE"}

    digest = envelope.get("evidence_digest")
    if not isinstance(digest, str) or _SHA256.fullmatch(digest) is None:
        return {"status": "INVALID_ENVELOPE"}

    evidence = {key: copy.deepcopy(envelope[key]) for key in _REQUIRED_FIELDS}
    try:
        _validate_evidence(evidence)
    except (P2203Error, TypeError, ValueError):
        return {"status": "INVALID_ENVELOPE"}

    body = {key: copy.deepcopy(value) for key, value in envelope.items() if key != "evidence_digest"}
    try:
        calculated = canonical_sha256(body)
    except (TypeError, ValueError):
        return {"status": "INVALID_ENVELOPE"}

    if calculated != digest:
        return {
            "status": "BLOCKED_TAMPERED_ENVELOPE",
            "evidence_digest": digest,
        }

    return {
        "status": "PASS",
        "evidence_digest": digest,
    }
