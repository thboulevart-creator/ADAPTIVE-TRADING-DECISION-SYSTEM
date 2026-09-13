"""Controlled reconstruction of the B08-A/B09 input-binding boundary.

IMPORTANT: RECONSTRUCTION != RECOVERY.
The original historical implementation was not recoverable from accessible
GitHub history. This module preserves the documented architecture, not the
claim of byte-for-byte identity with the lost implementation.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

_BOUND_INPUT_CAPABILITY = object()


@dataclass(frozen=True)
class BoundResearchInput:
    corpus_root: Path
    contract_path: Path
    contract: dict
    expected_corpus_hash: str
    expected_contract_hash: str

    def __init__(self, _capability, *, corpus_root, contract_path, contract,
                 expected_corpus_hash, expected_contract_hash):
        if _capability is not _BOUND_INPUT_CAPABILITY:
            raise TypeError("BoundResearchInput must be created by bind_execution_input()")
        object.__setattr__(self, "corpus_root", Path(corpus_root))
        object.__setattr__(self, "contract_path", Path(contract_path))
        object.__setattr__(self, "contract", contract)
        object.__setattr__(self, "expected_corpus_hash", expected_corpus_hash)
        object.__setattr__(self, "expected_contract_hash", expected_contract_hash)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _inventory_hash(corpus_root: Path) -> str:
    rows = []
    for path in sorted(p for p in corpus_root.rglob("*") if p.is_file()):
        digest = _sha256_file(path)
        rows.append(f"{path.relative_to(corpus_root).as_posix()}\t{path.stat().st_size}\t{digest}\n")
    digest = hashlib.sha256()
    for row in rows:
        digest.update(row.encode("utf-8"))
    return digest.hexdigest()


def _load_contract(contract_path: Path) -> dict:
    with contract_path.open("r", encoding="utf-8") as handle:
        contract = json.load(handle)
    if not isinstance(contract, dict):
        raise ValueError("Instrument contract must be a JSON object")
    return contract


def bind_execution_input(corpus_root, contract_path, expected_corpus_hash,
                         expected_contract_hash) -> BoundResearchInput:
    """Create the only admissible production input capability.

    Identity is checked before the capability is exposed to the engine.
    """
    root = Path(corpus_root)
    contract = Path(contract_path)
    if not root.is_dir():
        raise FileNotFoundError(f"Corpus root not found: {root}")
    if not contract.is_file():
        raise FileNotFoundError(f"Contract not found: {contract}")
    actual_contract_hash = _sha256_file(contract)
    if actual_contract_hash != expected_contract_hash:
        raise ValueError("Instrument contract identity mismatch")
    actual_corpus_hash = _inventory_hash(root)
    if actual_corpus_hash != expected_corpus_hash:
        raise ValueError("Research corpus identity mismatch")
    return BoundResearchInput(
        _BOUND_INPUT_CAPABILITY,
        corpus_root=root,
        contract_path=contract,
        contract=_load_contract(contract),
        expected_corpus_hash=expected_corpus_hash,
        expected_contract_hash=expected_contract_hash,
    )
