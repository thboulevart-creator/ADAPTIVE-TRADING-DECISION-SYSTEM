"""P1.5 qualification-only durable MEMORY witnessed re-attestation.

This module implements the minimal EXTERNAL_RECEIPT_PIN trust model selected by
P1.5. It persists canonical evidence bytes and permits a fresh process to mint
only a new local historical-memory attestation when an independently supplied
receipt pin matches exactly.

It does not replay historical Action/Result objects, attach interpretation or
knowledge, or create any operational permission.
"""

from __future__ import annotations

import hashlib
import json
import secrets
import weakref
from dataclasses import asdict, dataclass, fields
from pathlib import Path

from src.memory_episode import (
    CONTRACT as P14_CONTRACT,
    ObservationalMemoryEpisode,
    is_factory_attested_memory_episode,
)


CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
RECORD_SCHEMA = "P1_5_DURABLE_MEMORY_RECORD_V1"
RECEIPT_SCHEMA = "P1_5_WITNESSED_MEMORY_RECEIPT_V1"

_HEX = frozenset("0123456789abcdef")
_RECORD_KEYS = frozenset({"schema", "contract_id", "episode"})
_RECEIPT_KEYS = frozenset(
    {
        "schema",
        "contract_id",
        "authority_id",
        "registration_id",
        "capture_nonce",
        "episode_id",
        "record_sha256",
    }
)
_EPISODE_KEYS = frozenset(field.name for field in fields(ObservationalMemoryEpisode))


@dataclass(frozen=True, slots=True)
class WitnessedMemoryCapture:
    record_path: Path
    receipt_path: Path
    receipt_sha256: str
    registration_id: str


@dataclass(frozen=True, slots=True, weakref_slot=True)
class HistoricalMemoryEpisode:
    episode: ObservationalMemoryEpisode
    registration_id: str
    authority_id: str
    contract_id: str
    record_sha256: str
    receipt_sha256: str


def _canonical(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        + b"\n"
    )


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _stable_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def _episode_id_from_document(document: dict[str, object]) -> str:
    content = dict(document)
    content.pop("episode_id", None)
    payload = {"contract": P14_CONTRACT, "content": content}
    return "MEP-" + _stable_hash(payload)[:32]


def _registration_id(
    *,
    authority_id: str,
    capture_nonce: str,
    episode_id: str,
    record_sha256: str,
) -> str:
    payload = {
        "contract_id": CONTRACT,
        "authority_id": authority_id,
        "capture_nonce": capture_nonce,
        "episode_id": episode_id,
        "record_sha256": record_sha256,
    }
    return "MREG-" + _sha256(_canonical(payload))[:32]


def _strict_json(raw: bytes, *, label: str) -> dict[str, object]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label} must be UTF-8") from exc

    def no_duplicates(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{label} contains duplicate key: {key}")
            result[key] = value
        return result

    try:
        document = json.loads(text, object_pairs_hook=no_duplicates)
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"{label} is not valid strict JSON") from exc

    if not isinstance(document, dict):
        raise ValueError(f"{label} must be a JSON object")
    if _canonical(document) != raw:
        raise ValueError(f"{label} is not canonical")
    return document


def _validate_hex_digest(value: object, *, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or not set(value) <= _HEX:
        raise ValueError(f"{label} must be a lowercase SHA-256 hex digest")
    return value


def _load_episode(document: object) -> ObservationalMemoryEpisode:
    if not isinstance(document, dict):
        raise ValueError("durable record episode must be an object")
    if set(document) != _EPISODE_KEYS:
        raise ValueError("durable record episode schema mismatch")
    if any(not isinstance(value, str) for value in document.values()):
        raise ValueError("durable record episode fields must be strings")
    if document["episode_id"] != _episode_id_from_document(document):
        raise ValueError("durable record episode_id mismatch")
    return ObservationalMemoryEpisode(**document)


def _historical_fingerprint(value: HistoricalMemoryEpisode) -> str:
    return _stable_hash(
        {
            "episode": asdict(value.episode),
            "registration_id": value.registration_id,
            "authority_id": value.authority_id,
            "contract_id": value.contract_id,
            "record_sha256": value.record_sha256,
            "receipt_sha256": value.receipt_sha256,
        }
    )


def _build_historical_attestation_api():
    registry: dict[int, tuple[weakref.ReferenceType[HistoricalMemoryEpisode], str]] = {}

    def attest(
        *,
        episode: ObservationalMemoryEpisode,
        registration_id: str,
        authority_id: str,
        record_sha256: str,
        receipt_sha256: str,
    ) -> HistoricalMemoryEpisode:
        produced = HistoricalMemoryEpisode(
            episode=episode,
            registration_id=registration_id,
            authority_id=authority_id,
            contract_id=CONTRACT,
            record_sha256=record_sha256,
            receipt_sha256=receipt_sha256,
        )
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _historical_fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if not isinstance(value, HistoricalMemoryEpisode):
            return False
        entry = registry.get(id(value))
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        return reference() is value and _historical_fingerprint(value) == expected_fingerprint

    return attest, verify


_attest_historical_memory, is_factory_attested_historical_memory = _build_historical_attestation_api()
del _build_historical_attestation_api


def persist_witnessed_memory_episode(
    output_directory: object,
    episode: object,
    authority_id: object,
) -> WitnessedMemoryCapture:
    """Capture one exact P1.4-attested episode as canonical record + receipt."""
    if not isinstance(episode, ObservationalMemoryEpisode):
        raise TypeError("P1.5 capture requires full ObservationalMemoryEpisode")
    if not is_factory_attested_memory_episode(episode):
        raise ValueError("P1.5 capture requires exact currently-attested P1.4 episode")
    if not isinstance(authority_id, str) or not authority_id:
        raise ValueError("P1.5 capture requires non-empty authority_id")
    if not isinstance(output_directory, (str, Path)):
        raise TypeError("P1.5 capture requires output directory path")

    directory = Path(output_directory)
    directory.mkdir(parents=True, exist_ok=True)

    episode_document = asdict(episode)
    if episode_document["episode_id"] != _episode_id_from_document(episode_document):
        raise ValueError("P1.5 capture refuses inconsistent P1.4 episode identity")

    record = {
        "schema": RECORD_SCHEMA,
        "contract_id": CONTRACT,
        "episode": episode_document,
    }
    record_bytes = _canonical(record)
    record_sha256 = _sha256(record_bytes)

    capture_nonce = secrets.token_hex(32)
    registration_id = _registration_id(
        authority_id=authority_id,
        capture_nonce=capture_nonce,
        episode_id=episode.episode_id,
        record_sha256=record_sha256,
    )
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "contract_id": CONTRACT,
        "authority_id": authority_id,
        "registration_id": registration_id,
        "capture_nonce": capture_nonce,
        "episode_id": episode.episode_id,
        "record_sha256": record_sha256,
    }
    receipt_bytes = _canonical(receipt)
    receipt_sha256 = _sha256(receipt_bytes)

    record_path = directory / f"{registration_id}.record.json"
    receipt_path = directory / f"{registration_id}.receipt.json"
    if record_path.exists() or receipt_path.exists():
        raise ValueError("P1.5 registration path collision")
    record_path.write_bytes(record_bytes)
    receipt_path.write_bytes(receipt_bytes)

    return WitnessedMemoryCapture(
        record_path=record_path,
        receipt_path=receipt_path,
        receipt_sha256=receipt_sha256,
        registration_id=registration_id,
    )


def reattest_persisted_memory_episode(
    record_path: object,
    receipt_path: object,
    expected_contract_id: object,
    expected_authority_id: object,
    expected_receipt_sha256: object,
) -> HistoricalMemoryEpisode:
    """Verify an externally pinned durable receipt and mint fresh local authority."""
    if not isinstance(record_path, (str, Path)) or not isinstance(receipt_path, (str, Path)):
        raise TypeError("P1.5 re-attestation requires record and receipt paths")
    if not isinstance(expected_contract_id, str) or not expected_contract_id:
        raise TypeError("P1.5 re-attestation requires external expected contract")
    if not isinstance(expected_authority_id, str) or not expected_authority_id:
        raise TypeError("P1.5 re-attestation requires external expected authority")
    expected_pin = _validate_hex_digest(
        expected_receipt_sha256,
        label="expected_receipt_sha256",
    )

    record_file = Path(record_path)
    receipt_file = Path(receipt_path)
    if not record_file.is_file() or not receipt_file.is_file():
        raise ValueError("P1.5 durable record/receipt missing")

    record_bytes = record_file.read_bytes()
    receipt_bytes = receipt_file.read_bytes()
    actual_receipt_sha256 = _sha256(receipt_bytes)
    if not secrets.compare_digest(actual_receipt_sha256, expected_pin):
        raise ValueError("P1.5 external receipt pin mismatch")

    receipt = _strict_json(receipt_bytes, label="receipt")
    if set(receipt) != _RECEIPT_KEYS:
        raise ValueError("P1.5 receipt schema mismatch")
    if receipt["schema"] != RECEIPT_SCHEMA:
        raise ValueError("P1.5 receipt schema id mismatch")
    if expected_contract_id != CONTRACT or receipt["contract_id"] != expected_contract_id:
        raise ValueError("P1.5 contract expectation mismatch")
    if receipt["authority_id"] != expected_authority_id:
        raise ValueError("P1.5 authority expectation mismatch")

    capture_nonce = receipt["capture_nonce"]
    if (
        not isinstance(capture_nonce, str)
        or len(capture_nonce) < 32
        or not set(capture_nonce.lower()) <= _HEX
    ):
        raise ValueError("P1.5 invalid capture nonce")
    if not isinstance(receipt["episode_id"], str):
        raise ValueError("P1.5 receipt episode_id invalid")
    record_sha256 = _validate_hex_digest(receipt["record_sha256"], label="record_sha256")

    actual_record_sha256 = _sha256(record_bytes)
    if not secrets.compare_digest(actual_record_sha256, record_sha256):
        raise ValueError("P1.5 record integrity mismatch")

    record = _strict_json(record_bytes, label="record")
    if set(record) != _RECORD_KEYS:
        raise ValueError("P1.5 durable record schema mismatch")
    if record["schema"] != RECORD_SCHEMA or record["contract_id"] != CONTRACT:
        raise ValueError("P1.5 durable record contract mismatch")

    episode = _load_episode(record["episode"])
    if receipt["episode_id"] != episode.episode_id:
        raise ValueError("P1.5 receipt/record episode mismatch")

    expected_registration_id = _registration_id(
        authority_id=expected_authority_id,
        capture_nonce=capture_nonce,
        episode_id=episode.episode_id,
        record_sha256=record_sha256,
    )
    if receipt["registration_id"] != expected_registration_id:
        raise ValueError("P1.5 registration identity is not content-bound")

    return _attest_historical_memory(
        episode=episode,
        registration_id=expected_registration_id,
        authority_id=expected_authority_id,
        record_sha256=record_sha256,
        receipt_sha256=actual_receipt_sha256,
    )
