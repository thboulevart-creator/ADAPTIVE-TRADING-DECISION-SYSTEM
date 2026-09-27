from __future__ import annotations

import hashlib
import json
from typing import Any


CONTRACT = "ATDS_A0_RESEARCH_FINDINGS_AUTHORITY_INTERPRETATION_V0_3"

_NORMALIZED_CONCLUSIONS = frozenset(
    {
        "SUPPORTED",
        "REFUTED",
        "NOT_INTERPRETABLE",
        "NO_SCIENTIFIC_CLAIM",
    }
)

_PERMISSION_DIMENSIONS = (
    "evidence_level",
    "research_class",
    "source_promotion_limit",
    "data_class",
    "confirmatory_claim",
)

_A0_PERMISSION_UNIVERSE = frozenset(
    {
        "HYPOTHESIS_INPUT",
        "AUDIT_ONLY",
        "TRACE_ONLY",
    }
)

_CONTROL_STATES = frozenset(
    {
        "EVIDENCED_PASS",
        "EVIDENCED_FAIL",
        "NOT_REPRESENTED",
        "CALLER_ASSERTED",
    }
)

_GOVERNED_PERMISSION_TABLE = {
    "evidence_level": {
        "N0": (
            "HYPOTHESIS_INPUT",
            "AUDIT_ONLY",
        ),
        "UNDETERMINED": (
            "HYPOTHESIS_INPUT",
        ),
    },
    "research_class": {
        "N0_EXPLORATORY_SYNTHETIC": (
            "HYPOTHESIS_INPUT",
            "TRACE_ONLY",
        ),
    },
    "source_promotion_limit": {
        "HYPOTHESIS_ONLY": (
            "HYPOTHESIS_INPUT",
            "AUDIT_ONLY",
            "TRACE_ONLY",
        ),
        "NOT_REPRESENTED": (
            "HYPOTHESIS_INPUT",
        ),
    },
    "data_class": {
        "SYNTHETIC_ONLY": (
            "HYPOTHESIS_INPUT",
            "TRACE_ONLY",
        ),
        "REAL": (
            "HYPOTHESIS_INPUT",
            "TRACE_ONLY",
        ),
    },
    "confirmatory_claim": {
        "NOT_CONFIRMATORY": (
            "HYPOTHESIS_INPUT",
            "AUDIT_ONLY",
        ),
        "NOT_ESTABLISHED": (
            "HYPOTHESIS_INPUT",
            "AUDIT_ONLY",
        ),
    },
}

_GOVERNED_AUTHORITIES = {
    "ATDS_A0_SYNTHETIC_SCIENTIFIC_RESULT_V0_1": {
        "producer_identity":
            "ATDS_A0_SYNTHETIC_PRODUCER_V0_1",
        "registry_schema":
            "ATDS_A0_SOURCE_PROFILE_REGISTRY_V0_1",
        "registry_version": "V0_1",
        "profile_contract_id":
            "ATDS_A0_SYNTHETIC_SOURCE_PROFILE_V0_1",
        "preregistration_schema":
            "ATDS_A0_SYNTHETIC_PREREGISTRATION_V0_1",
        "expected_family": ("H1", "H2", "H3"),
        "normalization_policy_schema":
            "ATDS_A0_GLOBAL_NORMALIZATION_POLICY_V0_1",
        "profile_restriction_permissions":
            ("HYPOTHESIS_INPUT",),
        "required_normalization_map": {
            "SUPPORTED_N0": "SUPPORTED",
            "REFUTED_N0": "REFUTED",
            "NOT_INTERPRETABLE": "NOT_INTERPRETABLE",
        },
    }
}


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _reject_duplicate_keys(
    pairs: list[tuple[str, Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}

    for key, value in pairs:
        if key in result:
            raise ValueError(
                f"duplicate JSON key:{key}"
            )
        result[key] = value

    return result


def _reject_non_finite(token: str) -> None:
    raise ValueError(
        f"non-finite JSON number:{token}"
    )


def _parse_object(
    raw: bytes | bytearray,
    *,
    label: str,
) -> dict[str, Any]:
    if not isinstance(raw, (bytes, bytearray)):
        raise TypeError(
            f"{label} must be exact bytes"
        )

    try:
        text = bytes(raw).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            f"{label} is not UTF-8"
        ) from exc

    try:
        value = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_non_finite,
        )
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON:{label}"
        ) from exc

    if not isinstance(value, dict):
        raise ValueError(
            f"{label} must contain a JSON object"
        )

    return value


def _canonical_bytes(
    value: dict[str, Any],
) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _require_canonical_authority_bytes(
    raw: bytes | bytearray,
    value: dict[str, Any],
    *,
    label: str,
) -> None:
    if bytes(raw) != _canonical_bytes(value):
        raise ValueError(
            f"non-canonical governed authority bytes:{label}"
        )


def _strict_string(
    value: Any,
    *,
    label: str,
) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(
            f"invalid string:{label}"
        )
    return value


def _strict_string_list(
    value: Any,
    *,
    label: str,
) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(
            f"invalid list:{label}"
        )

    if any(
        not isinstance(item, str) or not item
        for item in value
    ):
        raise ValueError(
            f"invalid member:{label}"
        )

    if len(value) != len(set(value)):
        raise ValueError(
            f"duplicate member:{label}"
        )

    return list(value)


def _strict_number(
    value: Any,
    *,
    label: str,
) -> int | float:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
    ):
        raise ValueError(
            f"invalid numeric:{label}"
        )
    return value


def _strict_positive_int(
    value: Any,
    *,
    label: str,
) -> int:
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or value <= 0
    ):
        raise ValueError(
            f"invalid positive int:{label}"
        )
    return value


def _permission_set(
    policy_permissions: dict[str, Any],
    dimension: str,
    source_value: str,
    universe: frozenset[str],
) -> frozenset[str]:
    if (
        dimension == "evidence_level"
        and source_value == "UNDETERMINED"
    ):
        return frozenset()

    if (
        dimension == "source_promotion_limit"
        and source_value == "NOT_REPRESENTED"
    ):
        return frozenset()

    dimension_map = policy_permissions.get(
        dimension
    )

    if not isinstance(dimension_map, dict):
        return frozenset()

    raw_permissions = dimension_map.get(
        source_value
    )

    if raw_permissions is None:
        return frozenset()

    values = _strict_string_list(
        raw_permissions,
        label=f"permissions.{dimension}.{source_value}",
    )

    result = frozenset(values)

    if not result.issubset(universe):
        raise ValueError(
            f"unknown permission:{dimension}"
        )

    return result


def derive_authoritative_projection(
    case: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(case, dict):
        raise TypeError("A0 case must be a mapping")

    required_inputs = (
        "source_artifact",
        "preregistration",
        "producer_artifact",
        "profile_registry",
        "source_profile",
        "normalization_policy",
    )

    missing = [
        key
        for key in required_inputs
        if key not in case
    ]

    if missing:
        raise ValueError(
            f"missing governed inputs:{missing}"
        )

    source_raw = case["source_artifact"]
    prereg_raw = case["preregistration"]
    producer_raw = case["producer_artifact"]
    registry_raw = case["profile_registry"]
    profile_raw = case["source_profile"]
    policy_raw = case["normalization_policy"]

    source = _parse_object(
        source_raw,
        label="source_artifact",
    )
    preregistration = _parse_object(
        prereg_raw,
        label="preregistration",
    )
    registry = _parse_object(
        registry_raw,
        label="profile_registry",
    )
    profile = _parse_object(
        profile_raw,
        label="source_profile",
    )
    policy = _parse_object(
        policy_raw,
        label="normalization_policy",
    )

    _require_canonical_authority_bytes(
        prereg_raw,
        preregistration,
        label="preregistration",
    )
    _require_canonical_authority_bytes(
        registry_raw,
        registry,
        label="profile_registry",
    )
    _require_canonical_authority_bytes(
        profile_raw,
        profile,
        label="source_profile",
    )
    _require_canonical_authority_bytes(
        policy_raw,
        policy,
        label="normalization_policy",
    )

    if not isinstance(
        producer_raw,
        (bytes, bytearray),
    ):
        raise TypeError(
            "producer_artifact must be exact bytes"
        )

    try:
        producer_identity = bytes(
            producer_raw
        ).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            "producer_artifact is not UTF-8"
        ) from exc

    producer_identity = _strict_string(
        producer_identity,
        label="producer_identity",
    )

    source_schema = _strict_string(
        source.get("schema"),
        label="source.schema",
    )

    authority = _GOVERNED_AUTHORITIES.get(
        source_schema
    )
    if authority is None:
        raise ValueError(
            "unsupported source schema authority"
        )

    source_producer = _strict_string(
        source.get("producer_contract"),
        label="source.producer_contract",
    )

    if (
        source_producer != producer_identity
        or source_producer
        != authority["producer_identity"]
    ):
        raise ValueError(
            "producer artifact/source mismatch"
        )

    if (
        set(registry)
        != {"schema", "version", "entries"}
        or registry.get("schema")
        != authority["registry_schema"]
        or registry.get("version")
        != authority["registry_version"]
    ):
        raise ValueError(
            "unrecognized registry authority"
        )

    if (
        preregistration.get("schema")
        != authority["preregistration_schema"]
    ):
        raise ValueError(
            "unrecognized preregistration authority"
        )

    if (
        policy.get("schema")
        != authority["normalization_policy_schema"]
    ):
        raise ValueError(
            "unrecognized normalization policy authority"
        )

    entries = registry.get("entries")

    if not isinstance(entries, list):
        raise ValueError(
            "registry entries must be a list"
        )

    active = [
        entry
        for entry in entries
        if (
            isinstance(entry, dict)
            and entry.get("source_schema")
            == source_schema
            and entry.get("profile_status")
            == "ACTIVE"
        )
    ]

    if len(active) != 1:
        raise ValueError(
            "source schema must resolve to exactly one ACTIVE profile"
        )

    registry_entry = active[0]

    if set(registry_entry) != {
        "source_schema",
        "profile_contract_id",
        "profile_sha256",
        "profile_status",
        "supersedes_profile_sha256",
    }:
        raise ValueError(
            "unrecognized registry entry authority"
        )

    if (
        registry_entry.get(
            "supersedes_profile_sha256"
        )
        is not None
    ):
        raise ValueError(
            "unrecognized registry supersession authority"
        )

    profile_contract_id = _strict_string(
        profile.get("contract_id"),
        label="profile.contract_id",
    )

    if (
        profile_contract_id
        != authority["profile_contract_id"]
    ):
        raise ValueError(
            "unrecognized profile authority"
        )

    if (
        registry_entry.get("profile_contract_id")
        != profile_contract_id
    ):
        raise ValueError(
            "registry/profile contract mismatch"
        )

    if (
        registry_entry.get("profile_sha256")
        != _sha256(bytes(profile_raw))
    ):
        raise ValueError(
            "registry/profile SHA-256 mismatch"
        )

    if (
        profile.get("accepted_source_schema")
        != source_schema
    ):
        raise ValueError(
            "profile/source schema mismatch"
        )

    if (
        profile.get("accepted_producer_identity")
        != producer_identity
    ):
        raise ValueError(
            "profile/producer identity mismatch"
        )

    if (
        profile.get("expected_family_source")
        != "preregistration.expected_family"
    ):
        raise ValueError(
            "unsupported expected-family authority"
        )

    base_profile_keys = {
        "contract_id",
        "accepted_source_schema",
        "accepted_producer_identity",
        "expected_family_source",
        "profile_restriction_permissions",
    }
    rich_profile_semantics = {
        "native_status_paths": (
            "findings[*].raw_status",
            "artifact_status",
        ),
        "control_state_path": "controls",
        "fold_role_path": "folds",
        "applicability_path": "applicability",
        "lineage_paths": (
            "derived_from",
            "shared_corpus_identity",
        ),
        "source_supersession_path": "supersession",
        "measurement_path": "findings[*].measurement",
    }
    rich_profile_keys = set(
        rich_profile_semantics
    )

    extra_profile_keys = (
        set(profile) - base_profile_keys
    )
    if extra_profile_keys:
        if extra_profile_keys != rich_profile_keys:
            raise ValueError(
                "unrecognized profile extraction authority"
            )
        for key, expected_value in (
            rich_profile_semantics.items()
        ):
            actual_value = profile.get(key)
            if isinstance(expected_value, tuple):
                if tuple(actual_value or ()) != expected_value:
                    raise ValueError(
                        f"invalid profile extraction authority:{key}"
                    )
            elif actual_value != expected_value:
                raise ValueError(
                    f"invalid profile extraction authority:{key}"
                )

    governed_profile_permissions = tuple(
        _strict_string_list(
            profile.get(
                "profile_restriction_permissions"
            ),
            label=(
                "profile."
                "profile_restriction_permissions"
            ),
        )
    )
    if (
        governed_profile_permissions
        != authority["profile_restriction_permissions"]
    ):
        raise ValueError(
            "profile restriction authority widened"
        )

    expected_family = _strict_string_list(
        preregistration.get("expected_family"),
        label="preregistration.expected_family",
    )

    if (
        tuple(expected_family)
        != authority["expected_family"]
    ):
        raise ValueError(
            "unrecognized expected-family authority"
        )

    findings = source.get("findings")

    if not isinstance(findings, list):
        raise ValueError(
            "source findings must be a list"
        )

    finding_ids: list[str] = []
    raw_statuses: dict[str, str] = {}
    opaque_narrative_references: dict[
        str, dict[str, str]
    ] = {}

    for finding in findings:
        if not isinstance(finding, dict):
            raise ValueError(
                "invalid finding"
            )

        finding_id = _strict_string(
            finding.get("id"),
            label="finding.id",
        )

        raw_status = _strict_string(
            finding.get("raw_status"),
            label=f"finding.{finding_id}.raw_status",
        )

        for narrative_field in (
            "statement",
            "reason",
            "rationale",
        ):
            if narrative_field not in finding:
                continue
            narrative = _strict_string(
                finding.get(narrative_field),
                label=(
                    f"finding.{finding_id}."
                    f"{narrative_field}"
                ),
            )
            opaque_narrative_references[
                f"{finding_id}.{narrative_field}"
            ] = {
                "source_path": (
                    f"findings.{finding_id}."
                    f"{narrative_field}"
                ),
                "sha256": _sha256(
                    narrative.encode("utf-8")
                ),
            }

        if "measurement" in finding:
            measurement = finding["measurement"]
            if not isinstance(measurement, dict):
                raise ValueError(
                    f"invalid measurement:{finding_id}"
                )
            _strict_string(
                measurement.get("metric"),
                label=f"finding.{finding_id}.measurement.metric",
            )
            _strict_number(
                measurement.get("value"),
                label=f"finding.{finding_id}.measurement.value",
            )
            _strict_positive_int(
                measurement.get("sample_size"),
                label=f"finding.{finding_id}.measurement.sample_size",
            )
            if "scope" in measurement:
                _strict_string(
                    measurement.get("scope"),
                    label=(
                        f"finding.{finding_id}."
                        "measurement.scope"
                    ),
                )

        if finding_id in raw_statuses:
            raise ValueError(
                "duplicate finding id"
            )

        finding_ids.append(finding_id)
        raw_statuses[finding_id] = raw_status

    if (
        len(finding_ids) != len(expected_family)
        or set(finding_ids) != set(expected_family)
    ):
        raise ValueError(
            "expected family mismatch"
        )

    if set(policy) != {
        "schema",
        "permission_universe",
        "normalized_status_map",
        "permissions",
    }:
        raise ValueError(
            "unrecognized normalization policy content"
        )

    normalization_map = policy.get(
        "normalized_status_map"
    )

    if not isinstance(normalization_map, dict):
        raise ValueError(
            "normalization policy missing status map"
        )

    allowed_normalization_keys = set(
        authority["required_normalization_map"]
    ) | {"CONFIRMED"}
    if (
        not set(normalization_map).issubset(
            allowed_normalization_keys
        )
        or not set(
            authority["required_normalization_map"]
        ).issubset(normalization_map)
    ):
        raise ValueError(
            "unrecognized normalization mapping authority"
        )

    for raw_status, expected_conclusion in (
        authority["required_normalization_map"].items()
    ):
        if (
            normalization_map.get(raw_status)
            != expected_conclusion
        ):
            raise ValueError(
                "normalization mapping authority changed"
            )

    normalized: dict[str, str] = {}

    for finding_id in expected_family:
        raw_status = raw_statuses[finding_id]
        conclusion = normalization_map.get(
            raw_status
        )

        if conclusion not in _NORMALIZED_CONCLUSIONS:
            raise ValueError(
                f"unknown normalized conclusion:{raw_status}"
            )

        normalized[finding_id] = conclusion

    universe_values = _strict_string_list(
        policy.get("permission_universe"),
        label="permission_universe",
    )
    universe = frozenset(universe_values)

    if universe != _A0_PERMISSION_UNIVERSE:
        raise ValueError(
            "unrecognized A0 permission universe"
        )

    permissions = policy.get("permissions")

    if not isinstance(permissions, dict):
        raise ValueError(
            "normalization policy missing permissions"
        )

    if not set(permissions).issubset(
        set(_PERMISSION_DIMENSIONS)
    ):
        raise ValueError(
            "unexpected permission dimension"
        )

    for dimension, dimension_map in (
        permissions.items()
    ):
        if not isinstance(dimension_map, dict):
            raise ValueError(
                f"invalid permission table:{dimension}"
            )
        governed_dimension = (
            _GOVERNED_PERMISSION_TABLE[dimension]
        )
        for source_value, raw_permissions in (
            dimension_map.items()
        ):
            if source_value not in governed_dimension:
                raise ValueError(
                    "unrecognized permission-table authority"
                )
            values = tuple(
                _strict_string_list(
                    raw_permissions,
                    label=(
                        f"permissions.{dimension}."
                        f"{source_value}"
                    ),
                )
            )
            if (
                values
                != governed_dimension[source_value]
            ):
                raise ValueError(
                    "permission-table authority changed"
                )

    evidence_level = source.get(
        "evidence_level",
        "UNDETERMINED",
    )
    evidence_level = _strict_string(
        evidence_level,
        label="source.evidence_level",
    )

    research_class = _strict_string(
        source.get("research_class"),
        label="source.research_class",
    )

    source_promotion_limit = source.get(
        "source_promotion_limit",
        "NOT_REPRESENTED",
    )
    source_promotion_limit = _strict_string(
        source_promotion_limit,
        label="source.source_promotion_limit",
    )

    data_class = _strict_string(
        source.get("data_class"),
        label="source.data_class",
    )

    confirmatory_claim_status = _strict_string(
        source.get("confirmatory_claim_status"),
        label="source.confirmatory_claim_status",
    )

    for finding_id, raw_status in raw_statuses.items():
        if (
            raw_status == "CONFIRMED"
            and (
                data_class != "REAL"
                or confirmatory_claim_status
                != "CONFIRMATORY_ESTABLISHED"
            )
        ):
            normalized[finding_id] = (
                "NO_SCIENTIFIC_CLAIM"
            )

    control_states: dict[str, str] = {}
    fold_roles: dict[str, str] = {}
    applicability_domain: dict[str, Any] = {}
    lineage: list[str] = []
    shared_corpus_identity: str | None = None
    source_supersession: dict[str, Any] = {
        "status": "NOT_REPRESENTED",
        "superseded_by": None,
    }
    measurement_references: dict[
        str, dict[str, Any]
    ] = {}

    if extra_profile_keys:
        controls = source.get("controls")
        if not isinstance(controls, dict):
            raise ValueError(
                "governed controls missing"
            )
        for control_id, control in controls.items():
            control_id = _strict_string(
                control_id,
                label="control.id",
            )
            if not isinstance(control, dict):
                raise ValueError(
                    f"invalid control:{control_id}"
                )
            state = _strict_string(
                control.get("state"),
                label=f"control.{control_id}.state",
            )
            if state not in _CONTROL_STATES:
                raise ValueError(
                    f"unknown control state:{control_id}"
                )
            critical = control.get("critical")
            if not isinstance(critical, bool):
                raise ValueError(
                    f"invalid control critical flag:{control_id}"
                )
            control_states[control_id] = state
            if (
                critical
                and state == "EVIDENCED_FAIL"
            ):
                raise ValueError(
                    "critical evidenced control failure"
                )

        folds = source.get("folds")
        if not isinstance(folds, dict):
            raise ValueError(
                "governed folds missing"
            )
        for fold_id, fold in folds.items():
            fold_id = _strict_string(
                fold_id,
                label="fold.id",
            )
            if not isinstance(fold, dict):
                raise ValueError(
                    f"invalid fold:{fold_id}"
                )
            role = _strict_string(
                fold.get("role"),
                label=f"fold.{fold_id}.role",
            )
            if role not in {"PRIMARY", "DIAGNOSTIC"}:
                raise ValueError(
                    f"unknown fold role:{fold_id}"
                )
            fold_roles[fold_id] = role

        applicability = source.get(
            "applicability"
        )
        if not isinstance(applicability, dict):
            raise ValueError(
                "governed applicability missing"
            )
        applicability_domain = copy_value = (
            json.loads(
                json.dumps(
                    applicability,
                    sort_keys=True,
                    allow_nan=False,
                )
            )
        )
        if not isinstance(copy_value, dict):
            raise ValueError(
                "invalid applicability"
            )

        lineage = _strict_string_list(
            source.get("derived_from"),
            label="source.derived_from",
        )
        shared_corpus_identity = _strict_string(
            source.get("shared_corpus_identity"),
            label="source.shared_corpus_identity",
        )

        supersession = source.get(
            "supersession"
        )
        if not isinstance(supersession, dict):
            raise ValueError(
                "governed supersession missing"
            )
        supersession_status = _strict_string(
            supersession.get("status"),
            label="source.supersession.status",
        )
        superseded_by = supersession.get(
            "superseded_by"
        )
        if (
            superseded_by is not None
            and (
                not isinstance(superseded_by, str)
                or not superseded_by
            )
        ):
            raise ValueError(
                "invalid source supersession reference"
            )
        if supersession_status == "SUPERSEDED":
            raise ValueError(
                "superseded source cannot be current authority"
            )
        if supersession_status != "CURRENT":
            raise ValueError(
                "unknown source supersession status"
            )
        source_supersession = {
            "status": supersession_status,
            "superseded_by": superseded_by,
        }

        artifact_status = _strict_string(
            source.get("artifact_status"),
            label="source.artifact_status",
        )
        if (
            artifact_status
            in {"REFUTED_N0", "NOT_INTERPRETABLE"}
            and any(
                status == "SUPPORTED_N0"
                for status in raw_statuses.values()
            )
        ):
            raise ValueError(
                "unresolved native-status conflict"
            )
        raw_statuses[
            "artifact_status"
        ] = artifact_status

        for finding in findings:
            finding_id = finding["id"]
            measurement = finding.get(
                "measurement"
            )
            if measurement is None:
                continue
            fold_id = finding.get("fold_id")
            if fold_id is not None:
                fold_id = _strict_string(
                    fold_id,
                    label=(
                        f"finding.{finding_id}.fold_id"
                    ),
                )
                if fold_id not in fold_roles:
                    raise ValueError(
                        "unknown measurement fold binding"
                    )
            measurement_reference = {
                "metric": measurement["metric"],
                "value": measurement["value"],
                "sample_size":
                    measurement["sample_size"],
                "fold_id": fold_id,
            }
            if "scope" in measurement:
                measurement_reference[
                    "scope"
                ] = measurement["scope"]
            measurement_references[
                finding_id
            ] = measurement_reference

    dimension_values = {
        "evidence_level": evidence_level,
        "research_class": research_class,
        "source_promotion_limit":
            source_promotion_limit,
        "data_class": data_class,
        "confirmatory_claim":
            confirmatory_claim_status,
    }

    permission_sets = [
        _permission_set(
            permissions,
            dimension,
            dimension_values[dimension],
            universe,
        )
        for dimension in _PERMISSION_DIMENSIONS
    ]

    profile_permissions = frozenset(
        governed_profile_permissions
    )

    if not profile_permissions.issubset(
        universe
    ):
        raise ValueError(
            "unknown profile permission"
        )

    permission_sets.append(
        profile_permissions
    )

    effective = set(universe)

    for permission_set in permission_sets:
        effective.intersection_update(
            permission_set
        )

    positive_consumability = {
        finding_id: (
            normalized[finding_id]
            == "SUPPORTED"
        )
        for finding_id in expected_family
    }

    payload: dict[str, Any] = {
        "contract": CONTRACT,
        "source_artifact_sha256":
            _sha256(bytes(source_raw)),
        "source_schema": source_schema,
        "producer_identity":
            producer_identity,
        "protocol_identity":
            source_producer,
        "profile_registry_sha256":
            _sha256(bytes(registry_raw)),
        "source_profile_sha256":
            _sha256(bytes(profile_raw)),
        "normalization_policy_sha256":
            _sha256(bytes(policy_raw)),
        "expected_family_identity":
            _sha256(bytes(prereg_raw)),
        "completeness_status":
            "COMPLETE",
        "raw_native_statuses":
            raw_statuses,
        "normalized_conclusion":
            normalized,
        "data_class":
            data_class,
        "confirmatory_claim_status":
            confirmatory_claim_status,
        "evidence_level":
            evidence_level,
        "research_class":
            research_class,
        "effective_usage_permissions":
            sorted(effective),
        "control_states":
            control_states,
        "fold_roles":
            fold_roles,
        "applicability_domain":
            applicability_domain,
        "lineage":
            lineage,
        "shared_corpus_identity":
            shared_corpus_identity,
        "source_supersession":
            source_supersession,
        "measurement_references":
            measurement_references,
        "opaque_narrative_references":
            opaque_narrative_references,
        "positive_evidence_consumability":
            positive_consumability,
    }

    payload[
        "canonical_projection_sha256"
    ] = _sha256(
        _canonical_bytes(payload)
    )

    return payload


def verify_authoritative_projection(
    case: dict[str, Any],
    projection: object,
) -> bool:
    if not isinstance(projection, dict):
        return False

    try:
        expected = derive_authoritative_projection(
            case
        )
    except (TypeError, ValueError, KeyError):
        return False

    return projection == expected
