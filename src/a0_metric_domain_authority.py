from __future__ import annotations

import hashlib
import math
from typing import Any


_AUTHORITY_SHA256 = (
    "5813f9d75395308386b4561b13c4eae889a4565cca3289f08a30d81657057492"
)

_PRODUCER_IDENTITY = "ATDS_A0_SYNTHETIC_PRODUCER_V0_1"
_SOURCE_SCHEMA = "ATDS_A0_SYNTHETIC_SCIENTIFIC_RESULT_V0_1"
_METRIC_IDENTITY = "SYNTHETIC_SCORE"


def _exact_frozen_authority(authority_raw: Any) -> bool:
    if not isinstance(authority_raw, (bytes, bytearray)):
        return False
    return (
        hashlib.sha256(bytes(authority_raw)).hexdigest()
        == _AUTHORITY_SHA256
    )


def _finite_json_number(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if not isinstance(value, (int, float)):
        return False
    return math.isfinite(value)


def _has_takeover_claim(claim: Any) -> bool:
    if claim is None:
        return False
    if not isinstance(claim, dict):
        return True
    return bool(claim)


def validate_measurement_domain(
    *,
    authority_raw: bytes | bytearray,
    producer_identity: str,
    source_schema: str,
    metric_identity: str,
    metric_value: Any,
    source_profile_claim: Any = None,
    normalization_policy_claim: Any = None,
) -> bool:
    """Validate only the frozen synthetic metric-domain authority.

    This qualifier is intentionally standalone. It does not bind the
    authority into A0 runtime semantics and creates no permission,
    scientific-normalization, Decision, or ACTION authority.
    """

    if not _exact_frozen_authority(authority_raw):
        return False

    if producer_identity != _PRODUCER_IDENTITY:
        return False

    if source_schema != _SOURCE_SCHEMA:
        return False

    if metric_identity != _METRIC_IDENTITY:
        return False

    if not _finite_json_number(metric_value):
        return False

    if _has_takeover_claim(source_profile_claim):
        return False

    if _has_takeover_claim(normalization_policy_claim):
        return False

    return True
