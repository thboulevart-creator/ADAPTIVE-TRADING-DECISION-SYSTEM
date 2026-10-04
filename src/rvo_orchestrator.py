"""Minimal non-authoritative RVO runtime for RVO-02 synthetic qualification.

This module owns orchestration mechanics only. It does not own experiment,
statistical, data, temporal, execution, provenance, scientific, operational,
trading, or capital semantics.
"""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

CONTRACT = "ATDS_RVO_THIN_ORCHESTRATOR_RUNTIME_V0_1"
CATALOG_SCHEMA = "ATDS_RVO_CONTROL_CATALOG_V0_1"
PRE_SNAPSHOT_SCHEMA = "ATDS_RVO_PRE_SNAPSHOT_V0_1"
MANIFEST_SCHEMA = "ATDS_RVO_PRE_RESULT_CONTROL_MANIFEST_V0_1"
POST_SNAPSHOT_SCHEMA = "ATDS_RVO_POST_SNAPSHOT_V0_1"
RECONSTRUCTION_SCHEMA = "ATDS_RVO_RECONSTRUCTION_DESCRIPTOR_V0_1"
PACKAGE_SCHEMA = "ATDS_RVO_VALIDATION_PACKAGE_V0_1"

RVO_AUTHORITY = "NONE"
UNKNOWN_UNKNOWN_COVERAGE = "NOT_CLAIMED"

APPLICABILITY_STATES = {"APPLICABLE", "NOT_APPLICABLE", "UNKNOWN"}
ORCHESTRATION_STATES = {"READY", "BLOCKED"}
RECONSTRUCTION_CLASSES = {"EXACT_REPLAY", "EVIDENCE_REPLAY", "UNRECONSTRUCTIBLE"}

_ALLOWED_RVO_AUTHORITY_CLAIMS = {
    "ORCHESTRATION",
    "ROUTING",
    "PROTOCOL_COMPLETENESS",
    "MANIFEST_VALIDITY",
    "PACKAGE_COMPLETENESS",
    "RECONSTRUCTION_STATUS",
}
_FORBIDDEN_GLOBAL_CLAIMS = {
    "STRATEGY_VALIDATION",
    "SCIENTIFIC_VALIDITY",
    "PROFITABILITY_VALIDATION",
    "PROMOTION_AUTHORITY",
}
_FORBIDDEN_PACKAGE_INTERPRETATIONS = {
    "SCIENTIFIC_SUPPORT",
    "SCIENTIFIC_AUTHORITY",
    "PROFITABILITY",
    "PROMOTION_AUTHORITY",
    "OPERATIONAL_AUTHORITY",
}
_CONTROL_FIELDS = {
    "control_id",
    "owner_id",
    "owner_contract_ref",
    "failure_mode_refs",
    "applicability_rule_ref",
    "input_contract_ref",
    "output_contract_ref",
    "dependency_control_ids",
    "native_status_schema_ref",
    "blocking_rule_ref",
    "reconstructibility_contract_ref",
    "validity_scope",
}
_APPLICABILITY_FIELDS = {
    "control_id",
    "applicability_state",
    "applicability_basis",
    "material",
}
_METHOD_BINDING_FIELDS = {
    "p1_method_ref",
    "activation_digest",
    "qualified_method_ref",
    "claim_ref",
    "failure_mode_ref",
    "assumption_set_ref",
    "parameter_policy_ref",
    "dependency_refs",
}


class RVOError(RuntimeError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


class RVOFail(RVOError):
    """Intrinsic contract violation."""


class RVOBlocked(RVOError):
    """Safe orchestration conclusion unavailable."""


def _fail(code: str):
    raise RVOFail(code)


def _block(code: str):
    raise RVOBlocked(code)


def _text(value: Any, code: str) -> str:
    if type(value) is not str or not value:
        _fail(code)
    return value


def _string_list(value: Any, code: str, *, allow_empty: bool = True) -> list[str]:
    if type(value) not in (list, tuple):
        _fail(code)
    out = []
    for item in value:
        out.append(_text(item, code))
    if not allow_empty and not out:
        _fail(code)
    if len(out) != len(set(out)):
        _fail(code)
    return sorted(out)


def _canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise RVOFail("NON_CANONICAL_VALUE") from exc


def canonical_sha256(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json_bytes(value)).hexdigest()


def _verify_digest(record: dict[str, Any], digest_key: str, code: str) -> None:
    if type(record) is not dict:
        _fail(code)
    digest = record.get(digest_key)
    if type(digest) is not str or not digest.startswith("sha256:"):
        _fail(code)
    body = {key: copy.deepcopy(value) for key, value in record.items() if key != digest_key}
    if canonical_sha256(body) != digest:
        _fail(code)


def _normalize_control(entry: Any) -> dict[str, Any]:
    if type(entry) is not dict or set(entry) != _CONTROL_FIELDS:
        _fail("CONTROL_SCHEMA")
    out = copy.deepcopy(entry)
    for key in (
        "control_id",
        "owner_id",
        "owner_contract_ref",
        "applicability_rule_ref",
        "input_contract_ref",
        "output_contract_ref",
        "native_status_schema_ref",
        "blocking_rule_ref",
        "reconstructibility_contract_ref",
        "validity_scope",
    ):
        out[key] = _text(out[key], "CONTROL_SCHEMA")
    out["failure_mode_refs"] = _string_list(out["failure_mode_refs"], "CONTROL_SCHEMA", allow_empty=False)
    out["dependency_control_ids"] = _string_list(out["dependency_control_ids"], "CONTROL_SCHEMA")
    return out


def _topological_order(controls: list[dict[str, Any]]) -> list[str]:
    by_id = {item["control_id"]: item for item in controls}
    for item in controls:
        for dep in item["dependency_control_ids"]:
            if dep not in by_id:
                _fail("UNKNOWN_CONTROL_DEPENDENCY")
    indegree = {cid: 0 for cid in by_id}
    children = {cid: [] for cid in by_id}
    for item in controls:
        cid = item["control_id"]
        for dep in item["dependency_control_ids"]:
            indegree[cid] += 1
            children[dep].append(cid)
    ready = sorted(cid for cid, degree in indegree.items() if degree == 0)
    order: list[str] = []
    while ready:
        current = ready.pop(0)
        order.append(current)
        for child in sorted(children[current]):
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
                ready.sort()
    if len(order) != len(by_id):
        _fail("CONTROL_DEPENDENCY_CYCLE")
    return order


def build_control_catalog(entries, *, catalog_version):
    catalog_version = _text(catalog_version, "CATALOG_VERSION")
    if type(entries) not in (list, tuple) or not entries:
        _fail("CONTROL_CATALOG_EMPTY")
    controls = [_normalize_control(item) for item in entries]
    ids = [item["control_id"] for item in controls]
    if len(ids) != len(set(ids)):
        _fail("DUPLICATE_CONTROL_ID")
    controls = sorted(controls, key=lambda item: item["control_id"])
    _topological_order(controls)
    body = {
        "schema": CATALOG_SCHEMA,
        "catalog_version": catalog_version,
        "controls": controls,
        "catalog_authority": False,
        "unknown_unknown_coverage": UNKNOWN_UNKNOWN_COVERAGE,
    }
    return {**body, "catalog_digest": canonical_sha256(body)}


def verify_catalog(catalog):
    _verify_digest(catalog, "catalog_digest", "CATALOG_DIGEST_MISMATCH")
    if catalog.get("schema") != CATALOG_SCHEMA or catalog.get("catalog_authority") is not False:
        _fail("CATALOG_SCHEMA")
    controls = catalog.get("controls")
    if type(controls) is not list or not controls:
        _fail("CATALOG_SCHEMA")
    normalized = [_normalize_control(item) for item in controls]
    if normalized != sorted(normalized, key=lambda item: item["control_id"]):
        _fail("CATALOG_NON_CANONICAL_ORDER")
    _topological_order(normalized)
    return True


def build_routing_plan(catalog, *, owner_contract_overrides=None, owner_semantic_overrides=None):
    verify_catalog(catalog)
    if owner_contract_overrides:
        _fail("OWNER_OVERRIDE_FORBIDDEN")
    if owner_semantic_overrides:
        _fail("OWNER_SEMANTIC_REWRITE_FORBIDDEN")
    return _topological_order(catalog["controls"])


def assert_rvo_authority_claim(claim):
    claim = _text(claim, "RVO_AUTHORITY_CLAIM")
    if claim not in _ALLOWED_RVO_AUTHORITY_CLAIMS:
        _fail("RVO_AUTHORITY_EXPANSION")
    return claim


def assert_evidence_authority(owner_id, claimed_authority):
    _text(owner_id, "EVIDENCE_OWNER")
    claimed_authority = _text(claimed_authority, "EVIDENCE_AUTHORITY")
    if claimed_authority not in {"NONE", "PROCEDURAL_EVIDENCE"}:
        _fail("EVIDENCE_AUTHORITY_LAUNDERING")
    return claimed_authority


def assert_catalog_implication(catalog, source_state, target_state):
    verify_catalog(catalog)
    source_state = _text(source_state, "CATALOG_STATE")
    target_state = _text(target_state, "CATALOG_STATE")
    if source_state != target_state:
        _fail("CATALOG_STATE_LAUNDERING")
    return target_state


def build_pre_snapshot(
    *,
    repository,
    branch,
    head,
    tree,
    dataset_refs,
    temporal_ref,
    execution_ref,
    smf_activation_refs,
    mcepr_pre_ref,
    oos_pre_state,
    environment_identity,
    owner_contract_refs,
):
    repository = _text(repository, "PRE_SNAPSHOT_SCHEMA")
    branch = _text(branch, "PRE_SNAPSHOT_SCHEMA")
    head = _text(head, "PRE_SNAPSHOT_SCHEMA")
    tree = _text(tree, "PRE_SNAPSHOT_SCHEMA")
    temporal_ref = _text(temporal_ref, "PRE_SNAPSHOT_SCHEMA")
    execution_ref = _text(execution_ref, "PRE_SNAPSHOT_SCHEMA")
    mcepr_pre_ref = _text(mcepr_pre_ref, "PRE_SNAPSHOT_SCHEMA")
    oos_pre_state = _text(oos_pre_state, "PRE_SNAPSHOT_SCHEMA")
    environment_identity = _text(environment_identity, "PRE_SNAPSHOT_SCHEMA")
    if type(owner_contract_refs) is not dict or not owner_contract_refs:
        _fail("PRE_SNAPSHOT_SCHEMA")
    owners = {}
    for key, value in owner_contract_refs.items():
        owners[_text(key, "PRE_SNAPSHOT_SCHEMA")] = _text(value, "PRE_SNAPSHOT_SCHEMA")
    body = {
        "schema": PRE_SNAPSHOT_SCHEMA,
        "repository": repository,
        "branch": branch,
        "head": head,
        "tree": tree,
        "dataset_refs": _string_list(dataset_refs, "PRE_SNAPSHOT_SCHEMA"),
        "temporal_ref": temporal_ref,
        "execution_ref": execution_ref,
        "smf_activation_refs": _string_list(smf_activation_refs, "PRE_SNAPSHOT_SCHEMA"),
        "mcepr_pre_ref": mcepr_pre_ref,
        "oos_pre_state": oos_pre_state,
        "environment_identity": environment_identity,
        "owner_contract_refs": dict(sorted(owners.items())),
        "snapshot_authority": False,
    }
    return {**body, "pre_snapshot_digest": canonical_sha256(body)}


def _verify_pre_snapshot(snapshot):
    _verify_digest(snapshot, "pre_snapshot_digest", "PRE_SNAPSHOT_DIGEST_MISMATCH")
    if snapshot.get("schema") != PRE_SNAPSHOT_SCHEMA or snapshot.get("snapshot_authority") is not False:
        _fail("PRE_SNAPSHOT_SCHEMA")
    return True


def _normalize_applicability(records, control_ids):
    if type(records) not in (list, tuple):
        _fail("CONTROL_APPLICABILITY_INCOMPLETE")
    normalized = []
    seen = set()
    for record in records:
        if type(record) is not dict or set(record) != _APPLICABILITY_FIELDS:
            _fail("APPLICABILITY_SCHEMA")
        cid = _text(record["control_id"], "APPLICABILITY_SCHEMA")
        if cid in seen:
            _fail("DUPLICATE_APPLICABILITY_RECORD")
        seen.add(cid)
        state = record["applicability_state"]
        if state not in APPLICABILITY_STATES:
            _fail("APPLICABILITY_STATE")
        basis = record["applicability_basis"]
        if type(basis) is not str:
            _fail("APPLICABILITY_SCHEMA")
        if type(record["material"]) is not bool:
            _fail("APPLICABILITY_SCHEMA")
        if state == "NOT_APPLICABLE" and not basis:
            _block("UNJUSTIFIED_NOT_APPLICABLE")
        if state == "UNKNOWN" and record["material"]:
            _block("MATERIAL_APPLICABILITY_UNKNOWN")
        normalized.append(
            {
                "control_id": cid,
                "applicability_state": state,
                "applicability_basis": basis,
                "material": record["material"],
            }
        )
    if seen != set(control_ids):
        _block("CONTROL_APPLICABILITY_INCOMPLETE")
    return sorted(normalized, key=lambda item: item["control_id"])


def _normalize_method_bindings(method_bindings, *, claim_ref, controls, applicability):
    if type(method_bindings) is not dict:
        _fail("METHOD_BINDING_SCHEMA")
    by_control = {item["control_id"]: item for item in controls}
    app_by_control = {item["control_id"]: item for item in applicability}
    required = {
        cid
        for cid, item in by_control.items()
        if item["owner_id"] == "SMF" and app_by_control[cid]["applicability_state"] == "APPLICABLE"
    }
    if set(method_bindings) != required:
        if required:
            _block("LABEL_ONLY_METHOD_REF")
        if method_bindings:
            _fail("METHOD_BINDING_UNEXPECTED")
        return {}
    out = {}
    for cid in sorted(required):
        binding = method_bindings[cid]
        if type(binding) is not dict:
            _block("LABEL_ONLY_METHOD_REF")
        if set(binding) != _METHOD_BINDING_FIELDS:
            _block("LABEL_ONLY_METHOD_REF")
        clean = copy.deepcopy(binding)
        for key in _METHOD_BINDING_FIELDS - {"dependency_refs"}:
            if type(clean[key]) is not str:
                _fail("METHOD_BINDING_SCHEMA")
        if not clean["parameter_policy_ref"]:
            _block("MATERIAL_PARAMETER_POLICY_MISSING")
        for key in (
            "p1_method_ref",
            "activation_digest",
            "qualified_method_ref",
            "claim_ref",
            "failure_mode_ref",
            "assumption_set_ref",
        ):
            if not clean[key]:
                _fail("METHOD_BINDING_SCHEMA")
        clean["dependency_refs"] = _string_list(clean["dependency_refs"], "METHOD_BINDING_SCHEMA")
        expected = by_control[cid]
        if clean["claim_ref"] != claim_ref:
            _block("METHOD_BINDING_MISMATCH")
        if clean["failure_mode_ref"] not in expected["failure_mode_refs"]:
            _block("METHOD_BINDING_MISMATCH")
        if clean["dependency_refs"] != sorted(expected["dependency_control_ids"]):
            _block("METHOD_BINDING_MISMATCH")
        out[cid] = clean
    return out


def build_pre_result_manifest(
    *,
    catalog,
    experiment_spec_id,
    claim_ref,
    estimand_ref,
    validity_scope_ref,
    pre_snapshot,
    applicability_records,
    method_bindings,
    result_exposed=False,
):
    if result_exposed is not False:
        _block("POST_RESULT_MANIFEST_FORBIDDEN")
    verify_catalog(catalog)
    _verify_pre_snapshot(pre_snapshot)
    experiment_spec_id = _text(experiment_spec_id, "MANIFEST_SCHEMA")
    claim_ref = _text(claim_ref, "MANIFEST_SCHEMA")
    estimand_ref = _text(estimand_ref, "MANIFEST_SCHEMA")
    validity_scope_ref = _text(validity_scope_ref, "MANIFEST_SCHEMA")
    control_ids = [item["control_id"] for item in catalog["controls"]]
    applicability = _normalize_applicability(applicability_records, control_ids)
    bindings = _normalize_method_bindings(
        method_bindings,
        claim_ref=claim_ref,
        controls=catalog["controls"],
        applicability=applicability,
    )
    applicable_ids = {
        item["control_id"] for item in applicability if item["applicability_state"] == "APPLICABLE"
    }
    routing_plan = [cid for cid in build_routing_plan(catalog) if cid in applicable_ids]
    body = {
        "schema": MANIFEST_SCHEMA,
        "catalog_digest": catalog["catalog_digest"],
        "experiment_spec_id": experiment_spec_id,
        "claim_ref": claim_ref,
        "estimand_ref": estimand_ref,
        "validity_scope_ref": validity_scope_ref,
        "pre_snapshot_digest": pre_snapshot["pre_snapshot_digest"],
        "applicability_records": applicability,
        "method_bindings": bindings,
        "routing_plan": routing_plan,
        "result_exposed": False,
        "manifest_authority": False,
        "orchestration_state": "SEALED",
    }
    return {**body, "manifest_digest": canonical_sha256(body)}


def verify_manifest(manifest):
    _verify_digest(manifest, "manifest_digest", "MANIFEST_DIGEST_MISMATCH")
    if (
        manifest.get("schema") != MANIFEST_SCHEMA
        or manifest.get("manifest_authority") is not False
        or manifest.get("result_exposed") is not False
        or manifest.get("orchestration_state") != "SEALED"
    ):
        _fail("MANIFEST_SCHEMA")
    return True


def amend_manifest(manifest, changes, *, result_exposed):
    verify_manifest(manifest)
    if result_exposed:
        _block("SEALED_MANIFEST_MUTATION")
    if type(changes) is not dict or not changes:
        _fail("MANIFEST_AMENDMENT")
    _fail("MANIFEST_REQUIRES_NEW_SPECIFICATION")


def rebind_manifest_catalog(manifest, new_catalog_digest, *, result_exposed):
    verify_manifest(manifest)
    _text(new_catalog_digest, "CATALOG_DIGEST")
    if result_exposed:
        _block("RETROACTIVE_CATALOG_SUBSTITUTION")
    _fail("CATALOG_REBIND_REQUIRES_NEW_MANIFEST")


def bind_owner_result(
    *,
    control_id,
    owner_id,
    native_status_schema_ref,
    native_status,
    asserted_native_status,
    orchestration_state,
    blocking_rule_ref,
    snapshot_digest,
):
    control_id = _text(control_id, "OWNER_RESULT_SCHEMA")
    owner_id = _text(owner_id, "OWNER_RESULT_SCHEMA")
    native_status_schema_ref = _text(native_status_schema_ref, "OWNER_RESULT_SCHEMA")
    native_status = _text(native_status, "OWNER_RESULT_SCHEMA")
    asserted_native_status = _text(asserted_native_status, "OWNER_RESULT_SCHEMA")
    if asserted_native_status != native_status:
        _fail("STATUS_LAUNDERING")
    if orchestration_state not in ORCHESTRATION_STATES:
        _fail("ORCHESTRATION_STATE")
    if orchestration_state == "BLOCKED" and (type(blocking_rule_ref) is not str or not blocking_rule_ref):
        _block("UNGROUNDED_STATUS_INTERPRETATION")
    if orchestration_state == "READY" and blocking_rule_ref is not None:
        _fail("SPURIOUS_BLOCKING_RULE")
    if snapshot_digest is not None:
        _text(snapshot_digest, "OWNER_RESULT_SCHEMA")
    return {
        "control_id": control_id,
        "owner_id": owner_id,
        "native_status_schema_ref": native_status_schema_ref,
        "native_status": native_status,
        "orchestration_state": orchestration_state,
        "blocking_rule_ref": blocking_rule_ref,
        "snapshot_digest": snapshot_digest,
        "rvo_rewritten_status": None,
        "result_authority": False,
    }


def build_post_snapshot(
    *,
    pre_manifest_digest,
    actual_input_refs,
    owner_output_refs,
    p1_finding_refs,
    pcp_post_ref,
    mcepr_post_ref,
    oos_post_state,
    environment_identity,
    material_dependency_refs,
):
    body = {
        "schema": POST_SNAPSHOT_SCHEMA,
        "pre_manifest_digest": _text(pre_manifest_digest, "POST_SNAPSHOT_SCHEMA"),
        "actual_input_refs": _string_list(actual_input_refs, "POST_SNAPSHOT_SCHEMA"),
        "owner_output_refs": _string_list(owner_output_refs, "POST_SNAPSHOT_SCHEMA"),
        "p1_finding_refs": _string_list(p1_finding_refs, "POST_SNAPSHOT_SCHEMA"),
        "pcp_post_ref": _text(pcp_post_ref, "POST_SNAPSHOT_SCHEMA"),
        "mcepr_post_ref": _text(mcepr_post_ref, "POST_SNAPSHOT_SCHEMA"),
        "oos_post_state": _text(oos_post_state, "POST_SNAPSHOT_SCHEMA"),
        "environment_identity": _text(environment_identity, "POST_SNAPSHOT_SCHEMA"),
        "material_dependency_refs": _string_list(material_dependency_refs, "POST_SNAPSHOT_SCHEMA"),
        "snapshot_authority": False,
    }
    return {**body, "post_snapshot_digest": canonical_sha256(body)}


def _verify_post_snapshot(snapshot):
    _verify_digest(snapshot, "post_snapshot_digest", "POST_SNAPSHOT_DIGEST_MISMATCH")
    if snapshot.get("schema") != POST_SNAPSHOT_SCHEMA or snapshot.get("snapshot_authority") is not False:
        _fail("POST_SNAPSHOT_SCHEMA")
    return True


def enforce_pre_post_firewall(pre_snapshot, post_snapshot, *, current_mcepr_ref, current_oos_state):
    if pre_snapshot is None:
        _block("MISSING_PRE_STATE")
    if pre_snapshot is post_snapshot:
        _fail("PRE_POST_COLLAPSE")
    _verify_pre_snapshot(pre_snapshot)
    _verify_post_snapshot(post_snapshot)
    if current_mcepr_ref != pre_snapshot["mcepr_pre_ref"] or current_oos_state != pre_snapshot["oos_pre_state"]:
        _fail("RETROACTIVE_PRE_STATE_REWRITE")
    return "PASS"


def validate_material_drift(bound_before, observed_after, *, revalidated_refs, head_changed, impact_known):
    if type(bound_before) is not dict or type(observed_after) is not dict or type(revalidated_refs) is not dict:
        _fail("DRIFT_SCHEMA")
    if type(head_changed) is not bool or type(impact_known) is not bool:
        _fail("DRIFT_SCHEMA")
    if head_changed and not impact_known:
        _block("UNKNOWN_DRIFT_IMPACT")
    keys = set(bound_before) | set(observed_after)
    changed = {key for key in keys if bound_before.get(key) != observed_after.get(key)}
    if changed:
        for key in changed:
            if revalidated_refs.get(key) != observed_after.get(key):
                _block("STALE_MATERIAL_BINDING")
        return "REVALIDATED"
    return "UNCHANGED"


def validate_snapshot_coherence(records, *, expected_snapshot_digest):
    expected_snapshot_digest = _text(expected_snapshot_digest, "SNAPSHOT_COHERENCE")
    if type(records) not in (list, tuple) or not records:
        _block("MIXED_SNAPSHOT_EXECUTION")
    for record in records:
        if type(record) is not dict or record.get("snapshot_digest") != expected_snapshot_digest:
            _block("MIXED_SNAPSHOT_EXECUTION")
    return "PASS"


def validate_reconstruction_descriptor(
    *,
    reconstruction_class,
    material_inputs,
    environment_identity,
    dependency_refs,
    schema_refs,
    parameters,
    seeds,
    owner_contract_refs,
    routing_order,
    pre_manifest_digest,
    runtime_attestation,
):
    if reconstruction_class not in RECONSTRUCTION_CLASSES:
        _fail("RECONSTRUCTION_CLASS")
    if runtime_attestation is not None and (
        not material_inputs or not environment_identity or not pre_manifest_digest
    ):
        _block("RUNTIME_ATTESTATION_NOT_DURABLE")
    complete = (
        type(material_inputs) is dict and bool(material_inputs)
        and type(environment_identity) is str and bool(environment_identity)
        and type(dependency_refs) in (list, tuple) and bool(dependency_refs)
        and type(schema_refs) in (list, tuple) and bool(schema_refs)
        and type(parameters) is dict and bool(parameters)
        and type(seeds) is dict
        and type(owner_contract_refs) is dict and bool(owner_contract_refs)
        and type(routing_order) in (list, tuple) and bool(routing_order)
        and type(pre_manifest_digest) is str and bool(pre_manifest_digest)
    )
    if not complete:
        _block("INCOMPLETE_RECONSTRUCTION")
    body = {
        "schema": RECONSTRUCTION_SCHEMA,
        "reconstruction_class": reconstruction_class,
        "material_inputs": copy.deepcopy(material_inputs),
        "environment_identity": environment_identity,
        "dependency_refs": _string_list(dependency_refs, "RECONSTRUCTION_SCHEMA", allow_empty=False),
        "schema_refs": _string_list(schema_refs, "RECONSTRUCTION_SCHEMA", allow_empty=False),
        "parameters": copy.deepcopy(parameters),
        "seeds": copy.deepcopy(seeds),
        "owner_contract_refs": dict(sorted(owner_contract_refs.items())),
        "routing_order": list(routing_order),
        "pre_manifest_digest": pre_manifest_digest,
        "runtime_attestation_informational_only": runtime_attestation is not None,
    }
    return {**body, "reconstruction_digest": canonical_sha256(body)}


def promote_reconstruction_class(source_class, target_class):
    if source_class not in RECONSTRUCTION_CLASSES or target_class not in RECONSTRUCTION_CLASSES:
        _fail("RECONSTRUCTION_CLASS")
    rank = {"UNRECONSTRUCTIBLE": 0, "EVIDENCE_REPLAY": 1, "EXACT_REPLAY": 2}
    if rank[target_class] > rank[source_class]:
        _fail("RECONSTRUCTION_CLASS_ESCALATION")
    return target_class


def resolve_multiplicity_parameter(*, mcepr_event_count, explicit_n_trials, search_universe_status):
    _text(search_universe_status, "MULTIPLICITY_SCHEMA")
    if explicit_n_trials is None:
        if mcepr_event_count is not None:
            _block("INVENTED_MULTIPLICITY_PARAMETER")
        _block("MULTIPLICITY_PARAMETER_UNRESOLVED")
    if type(explicit_n_trials) is not int or isinstance(explicit_n_trials, bool) or explicit_n_trials < 1:
        _fail("MULTIPLICITY_PARAMETER")
    return explicit_n_trials


def interpret_relation_absence(*, relation_present):
    if type(relation_present) is not bool:
        _fail("RELATION_PRESENCE")
    return "RELATION_PRESENT" if relation_present else "UNKNOWN"


def validate_mcepr_claim(claim):
    claim = _text(claim, "MCEPR_CLAIM")
    if claim in {"COMPLETE", "PRISTINE_EVIDENCE", "EXHAUSTIVE"}:
        _fail("MCEPR_COMPLETENESS_OVERCLAIM")
    return claim


def validate_claim_capabilities(claim_requirements, capabilities):
    if type(claim_requirements) is not dict or type(capabilities) is not dict:
        _fail("CAPABILITY_SCHEMA")
    if claim_requirements.get("historical_point_in_time_required") is True:
        if capabilities.get("temporal_status") != "QUALIFIED":
            _block("TEMPORAL_CAPABILITY_GAP")
    if claim_requirements.get("all_in_profitability_required") is True:
        required = {"spread", "commission", "slippage", "financing"}
        actual = set(capabilities.get("execution_cost_components") or [])
        if not required.issubset(actual):
            _block("EXECUTION_COST_CAPABILITY_GAP")
    return "PASS"


def assert_global_claim(claim_name, value):
    claim_name = _text(claim_name, "GLOBAL_CLAIM")
    _text(value, "GLOBAL_CLAIM")
    if claim_name in _FORBIDDEN_GLOBAL_CLAIMS:
        _fail("GLOBAL_SCIENTIFIC_PASS_FORBIDDEN")
    return value


def interpret_package_state(package_state, target_interpretation):
    package_state = _text(package_state, "PACKAGE_STATE")
    target_interpretation = _text(target_interpretation, "PACKAGE_INTERPRETATION")
    if target_interpretation in _FORBIDDEN_PACKAGE_INTERPRETATIONS:
        _fail("PROCEDURAL_TO_SCIENTIFIC_LAUNDERING")
    return {"package_state": package_state, "interpretation": target_interpretation}


def aggregate_procedural_state(owner_results):
    if type(owner_results) not in (list, tuple) or not owner_results:
        return "PACKAGE_INCOMPLETE"
    states = [item.get("orchestration_state") for item in owner_results if type(item) is dict]
    if len(states) != len(owner_results):
        return "PACKAGE_INCOMPLETE"
    if "BLOCKED" in states:
        return "PACKAGE_BLOCKED"
    if all(state == "READY" for state in states):
        return "PACKAGE_COMPLETE"
    return "PACKAGE_INCOMPLETE"


def build_validation_package(
    *,
    manifest,
    pre_snapshot,
    post_snapshot,
    owner_results,
    reconstruction_descriptor,
):
    verify_manifest(manifest)
    _verify_pre_snapshot(pre_snapshot)
    _verify_post_snapshot(post_snapshot)
    if manifest["pre_snapshot_digest"] != pre_snapshot["pre_snapshot_digest"]:
        _block("MANIFEST_PRE_SNAPSHOT_MISMATCH")
    if post_snapshot["pre_manifest_digest"] != manifest["manifest_digest"]:
        _block("POST_MANIFEST_MISMATCH")
    if type(reconstruction_descriptor) is not dict:
        _block("INCOMPLETE_RECONSTRUCTION")
    _verify_digest(reconstruction_descriptor, "reconstruction_digest", "RECONSTRUCTION_DIGEST_MISMATCH")
    if reconstruction_descriptor.get("schema") != RECONSTRUCTION_SCHEMA:
        _fail("RECONSTRUCTION_SCHEMA")
    if reconstruction_descriptor["pre_manifest_digest"] != manifest["manifest_digest"]:
        _block("RECONSTRUCTION_MANIFEST_MISMATCH")
    applicable = {
        item["control_id"]
        for item in manifest["applicability_records"]
        if item["applicability_state"] == "APPLICABLE"
    }
    if type(owner_results) not in (list, tuple):
        _block("OWNER_RESULTS_INCOMPLETE")
    result_ids = {item.get("control_id") for item in owner_results if type(item) is dict}
    if result_ids != applicable:
        _block("OWNER_RESULTS_INCOMPLETE")
    validate_snapshot_coherence(owner_results, expected_snapshot_digest=pre_snapshot["pre_snapshot_digest"])
    package_state = aggregate_procedural_state(owner_results)
    body = {
        "schema": PACKAGE_SCHEMA,
        "manifest_digest": manifest["manifest_digest"],
        "pre_snapshot_digest": pre_snapshot["pre_snapshot_digest"],
        "post_snapshot_digest": post_snapshot["post_snapshot_digest"],
        "owner_results": sorted(copy.deepcopy(list(owner_results)), key=lambda item: item["control_id"]),
        "reconstruction_digest": reconstruction_descriptor["reconstruction_digest"],
        "package_state": package_state,
        "package_authority": False,
        "scientific_authority": False,
        "operational_authority": False,
        "rvo_authority": RVO_AUTHORITY,
    }
    return {**body, "package_digest": canonical_sha256(body)}


def verify_package(package):
    _verify_digest(package, "package_digest", "PACKAGE_DIGEST_MISMATCH")
    if package.get("schema") != PACKAGE_SCHEMA:
        _fail("PACKAGE_SCHEMA")
    if (
        package.get("package_authority") is not False
        or package.get("scientific_authority") is not False
        or package.get("operational_authority") is not False
        or package.get("rvo_authority") != "NONE"
    ):
        _fail("RVO_AUTHORITY_EXPANSION")
    return True


def qualification_semantics():
    return {
        "pass_semantics": "NO_MATERIAL_FAILURE_FOUND_WITHIN_EXACT_IMPLEMENTED_AND_TESTED_SYNTHETIC_RVO_SURFACE",
        "unknown_unknown_coverage": UNKNOWN_UNKNOWN_COVERAGE,
        "rvo_authority": RVO_AUTHORITY,
        "pass_grants_scientific_authority": False,
        "pass_grants_operational_authority": False,
        "pass_grants_trading_authority": False,
    }
