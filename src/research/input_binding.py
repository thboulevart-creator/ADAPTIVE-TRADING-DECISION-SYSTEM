"""Identity-bound research input capability for the P0.4 producer junction.

The underlying B08-A/B09 runtime was reconstructed, not historically recovered.
P0.4 adds process-local identity/content attestation so reconstructed, copied or
mutated bound inputs cannot cross the execution boundary.
"""
from __future__ import annotations

import hashlib
import json
import re
import weakref
from dataclasses import dataclass
from pathlib import Path
from typing import Any


_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


@dataclass(frozen=True)
class BoundResearchInput:
    corpus_root: Path
    contract_path: Path
    contract: dict[str, Any]
    expected_corpus_hash: str
    expected_contract_hash: str


def sha256_file(path: str | Path) -> str:
    source = Path(path)
    digest = hashlib.sha256()
    with source.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def corpus_inventory_hash(corpus_root: str | Path) -> str:
    root = Path(corpus_root)
    rows: list[str] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest = sha256_file(path)
        rows.append(f"{path.relative_to(root).as_posix()}\t{path.stat().st_size}\t{digest}\n")
    digest = hashlib.sha256()
    for row in rows:
        digest.update(row.encode("utf-8"))
    return digest.hexdigest()


def _load_contract(contract_path: Path) -> dict[str, Any]:
    with contract_path.open("r", encoding="utf-8") as handle:
        contract = json.load(handle)
    if not isinstance(contract, dict):
        raise ValueError("Instrument contract must be a JSON object")
    return contract


def _stable_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _fingerprint(bound_input: BoundResearchInput) -> str:
    return _stable_hash(
        {
            "corpus_root": str(bound_input.corpus_root.resolve()),
            "contract_path": str(bound_input.contract_path.resolve()),
            "contract": bound_input.contract,
            "expected_corpus_hash": bound_input.expected_corpus_hash,
            "expected_contract_hash": bound_input.expected_contract_hash,
        }
    )


def _validate_hash(label: str, value: str) -> None:
    if not isinstance(value, str) or _SHA256_RE.fullmatch(value) is None:
        raise ValueError(f"{label} must be a lowercase SHA-256 hex digest")


def _build_binding_api():
    registry: dict[int, tuple[weakref.ReferenceType[BoundResearchInput], str]] = {}

    def register(bound_input: BoundResearchInput) -> BoundResearchInput:
        object_id = id(bound_input)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(bound_input, cleanup)
        registry[object_id] = (reference, _fingerprint(bound_input))
        return bound_input

    def verify(bound_input: object, *, revalidate_sources: bool = True) -> bool:
        if not isinstance(bound_input, BoundResearchInput):
            return False
        entry = registry.get(id(bound_input))
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not bound_input or _fingerprint(bound_input) != expected_fingerprint:
            return False
        if not revalidate_sources:
            return True
        try:
            if not bound_input.corpus_root.is_dir() or not bound_input.contract_path.is_file():
                return False
            if sha256_file(bound_input.contract_path) != bound_input.expected_contract_hash:
                return False
            if corpus_inventory_hash(bound_input.corpus_root) != bound_input.expected_corpus_hash:
                return False
            if _load_contract(bound_input.contract_path) != bound_input.contract:
                return False
        except (OSError, ValueError, json.JSONDecodeError):
            return False
        return True

    def bind(
        corpus_root: str | Path,
        contract_path: str | Path,
        expected_corpus_hash: str,
        expected_contract_hash: str,
    ) -> BoundResearchInput:
        _validate_hash("expected_corpus_hash", expected_corpus_hash)
        _validate_hash("expected_contract_hash", expected_contract_hash)
        root = Path(corpus_root)
        contract_file = Path(contract_path)
        if not root.is_dir():
            raise FileNotFoundError(f"Corpus root not found: {root}")
        if not contract_file.is_file():
            raise FileNotFoundError(f"Contract not found: {contract_file}")
        if sha256_file(contract_file) != expected_contract_hash:
            raise ValueError("Instrument contract identity mismatch")
        if corpus_inventory_hash(root) != expected_corpus_hash:
            raise ValueError("Research corpus identity mismatch")
        contract = _load_contract(contract_file)
        bound_input = BoundResearchInput(
            corpus_root=root,
            contract_path=contract_file,
            contract=json.loads(json.dumps(contract)),
            expected_corpus_hash=expected_corpus_hash,
            expected_contract_hash=expected_contract_hash,
        )
        return register(bound_input)

    return bind, verify


bind_execution_input, is_bound_research_input = _build_binding_api()
del _build_binding_api
