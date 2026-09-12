"""Deterministic identity for the minimal CONTEXT contract."""

from __future__ import annotations

import hashlib
import json
from typing import Mapping


_IDENTITY_FIELDS = (
    "dataset_id",
    "dataset_version",
    "content_hash",
    "instrument",
    "granularity",
    "timezone_storage",
    "configuration_version",
)


def context_id(value: Mapping[str, str]) -> str:
    """Return the deterministic identity of a CONTEXT identity contract."""
    payload = {field: value[field] for field in _IDENTITY_FIELDS}
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return "CTX-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
