from __future__ import annotations

import json

BINDINGS = {
    "contract_blob": "8e6e888f8330e40d792b43650c32b09a8dc6a281",
    "decision_table_blob": "da9bb3a7436072795fced2d171cae8df23591279",
    "breaker_contract_blob": "c52eca89c45fd68e83c506925626a3c389b5d4a2",
    "traceability_blob": "364baff4a603c9be69f29742ba2647477742974f",
    "final_receipt_blob": "769fcc81f4b365b4a54152042be31a2dd1ce9412",
    "final_closure_blob": "4433648fb71684695513eddb2c60c4eddae41b6a",
}

MATERIAL = {
    "tick_count p50",
    "tick_count p90",
    "tick_count p99",
    "minute_range p50",
    "minute_range p90",
    "minute_range p95",
    "minute_range p99",
    "spread_mean p50",
}
NONMATERIAL = {"spread_mean p90", "spread_mean p95", "spread_mean p99"}
KNOWN = MATERIAL | NONMATERIAL
ROUTES = ("A", "B", "C")

FIELDS = {
    "case_id",
    "claim_unit",
    "downstream_claim_id",
    "downstream_analysis_id",
    "requested_temporal_scope",
    "pooling_requested",
    "conditioning_requested",
    "preregistered_robust_method_requested",
    "requested_routes",
    "pooling_justification_ref",
    "pooling_justification_status",
    "pooling_justification_reason_code",
    "temporal_conditioning_spec_ref",
    "temporal_conditioning_spec_status",
    "robust_method_preregistration_ref",
    "robust_method_preregistration_status",
    "robust_method_fields",
    "evidence_state_request",
    "authority_requests",
    "real_data_dependency_requested",
    "admissibility_basis_claim_unit",
}

A_ALLOWED = {
    "JUSTIFICATION_ABSENT",
    "JUSTIFICATION_PRESENT_PENDING_ADJUDICATION",
    "JUSTIFICATION_HUMAN_ADOPTED",
}
B_ALLOWED = {
    "SPEC_ABSENT",
    "SPEC_PRESENT_NOT_QUALIFIED_OR_FROZEN",
    "SPEC_QUALIFIED_AND_FROZEN",
}
C_ALLOWED = {
    "METHOD_PREREG_ABSENT_OR_INCOMPLETE",
    "METHOD_PREREG_QUALIFIED_AND_COMPLETE",
}
BAD_A_REASONS = {
    "ALL_YEARS_BELONG_TO_SAME_DATASET_ONLY",
    "SAMPLE_SIZE_IS_LARGE_ONLY",
    "POOLING_IS_CONVENIENT_ONLY",
}
METHOD_FIELDS = {
    "EXACT_METHOD_IDENTITY",
    "EXACT_FAILURE_MODE",
    "EXACT_ASSUMPTION_SET",
    "EXACT_VALIDITY_SCOPE",
    "EXACT_MATERIAL_PARAMETERS",
}
AUTH = {"M04_AUTHORIZE", "M05_AUTHORIZE", "M08_AUTHORIZE", "M09_AUTHORIZE", "M11_AUTHORIZE"}
EXEC = {"METHOD_EXECUTE", "M04_EXECUTE", "M05_EXECUTE", "M08_EXECUTE", "M09_EXECUTE", "M11_EXECUTE"}
METHOD_STATE = {"M04": "CLOSED", "M05": "CLOSED", "M08": "CLOSED", "M09": "CLOSED", "M11": "CLOSED"}


class PCGFailClosedError(ValueError):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


def canonical_json_bytes(value):
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("ascii")


def _raise(code):
    raise PCGFailClosedError(code)


def _text(v):
    return isinstance(v, str) and bool(v.strip())


def _metric(v):
    return v.split(" ", 1)[0]


def _validate(p):
    if not isinstance(p, dict):
        _raise("PACKET_NOT_OBJECT")
    if FIELDS - set(p):
        _raise("MISSING_REQUIRED_FIELD")
    if set(p) - FIELDS:
        _raise("UNKNOWN_INPUT_FIELD")

    for k in ("case_id", "claim_unit", "downstream_claim_id", "downstream_analysis_id", "requested_temporal_scope"):
        if not _text(p[k]):
            _raise("MALFORMED_REQUIRED_FIELD")

    if p["claim_unit"] not in KNOWN:
        _raise("UNKNOWN_CLAIM_UNIT")

    for k in ("pooling_requested", "conditioning_requested", "preregistered_robust_method_requested", "real_data_dependency_requested"):
        if type(p[k]) is not bool:
            _raise("MALFORMED_REQUIRED_FIELD")

    rr = p["requested_routes"]
    if not isinstance(rr, list) or any(not isinstance(x, str) for x in rr):
        _raise("MALFORMED_ROUTE_LIST")
    if len(rr) != len(set(rr)):
        _raise("DUPLICATE_ROUTE")
    if any(x not in ROUTES for x in rr):
        _raise("UNKNOWN_ROUTE")
    if "A" in rr and not p["pooling_requested"]:
        _raise("ROUTE_REQUEST_CONTRADICTION")
    if (("B" in rr) != p["conditioning_requested"]) or (("C" in rr) != p["preregistered_robust_method_requested"]):
        _raise("ROUTE_REQUEST_CONTRADICTION")

    if p["pooling_justification_status"] not in A_ALLOWED:
        _raise("MALFORMED_REFERENCE_STATUS")
    if p["temporal_conditioning_spec_status"] not in B_ALLOWED:
        _raise("MALFORMED_REFERENCE_STATUS")
    if p["robust_method_preregistration_status"] not in C_ALLOWED:
        _raise("MALFORMED_REFERENCE_STATUS")
    if p["evidence_state_request"] not in {"PRESERVE_EXPOSED_NON_PRISTINE", "RESET_TO_PRISTINE"}:
        _raise("MALFORMED_EVIDENCE_STATE")

    astat = p["pooling_justification_status"]
    if astat == "JUSTIFICATION_ABSENT":
        if p["pooling_justification_ref"] is not None or p["pooling_justification_reason_code"] != "NONE":
            _raise("MALFORMED_REFERENCE_STATUS")
    else:
        if not _text(p["pooling_justification_ref"]):
            _raise("MALFORMED_REFERENCE_STATUS")
        if not _text(p["pooling_justification_reason_code"]) or p["pooling_justification_reason_code"] == "NONE":
            _raise("MALFORMED_REFERENCE_STATUS")

    bstat = p["temporal_conditioning_spec_status"]
    if bstat == "SPEC_ABSENT":
        if p["temporal_conditioning_spec_ref"] is not None:
            _raise("MALFORMED_REFERENCE_STATUS")
    elif not _text(p["temporal_conditioning_spec_ref"]):
        _raise("MALFORMED_REFERENCE_STATUS")

    cstat = p["robust_method_preregistration_status"]
    cf = p["robust_method_fields"]
    if not isinstance(cf, dict):
        _raise("MALFORMED_ROBUST_METHOD_PREREGISTRATION")
    if cstat == "METHOD_PREREG_QUALIFIED_AND_COMPLETE":
        if not _text(p["robust_method_preregistration_ref"]):
            _raise("MALFORMED_REFERENCE_STATUS")
        if set(cf) != METHOD_FIELDS or any(not _text(cf[k]) for k in METHOD_FIELDS):
            _raise("MALFORMED_ROBUST_METHOD_PREREGISTRATION")

    ar = p["authority_requests"]
    if not isinstance(ar, list) or any(not isinstance(x, str) for x in ar):
        _raise("MALFORMED_AUTHORITY_REQUEST")
    if any(x not in (AUTH | EXEC) for x in ar):
        _raise("UNKNOWN_AUTHORITY_REQUEST")

    basis = p["admissibility_basis_claim_unit"]
    if basis is not None and not _text(basis):
        _raise("MALFORMED_BASIS_CLAIM_UNIT")


def _blocked(p, classification, code):
    return _assemble(p, classification, {}, "BLOCKED", code, code)


def _assemble(p, classification, route_states, overall, reason, block):
    ordered = [r for r in ROUTES if r in p["requested_routes"]]
    qualifying = [r for r in ordered if route_states.get(r) == "ADMISSIBLE_BY_ROUTE_" + r]
    if not ordered:
        selected = "NONE"
    elif len(ordered) == 1:
        selected = ordered[0]
    else:
        selected = "MULTIPLE"

    if block is not None:
        states = ["BLOCKED"]
        qualifying = []
    elif ordered:
        states = [route_states[r] for r in ordered]
    elif overall == "NOT_APPLICABLE":
        states = ["NOT_APPLICABLE"]
    elif classification == "MATERIAL_TEMPORAL_VARIATION":
        states = ["BLOCKED"]
    else:
        states = ["NON_MATERIAL_POOLING_REVIEW_REQUIRED"]

    return {
        "claim_unit": p["claim_unit"],
        "downstream_claim_id": p["downstream_claim_id"],
        "downstream_analysis_id": p["downstream_analysis_id"],
        "requested_temporal_scope": p["requested_temporal_scope"],
        "input_classification": classification,
        "selected_route": selected,
        "gate_state": states,
        "route_states": {r: route_states[r] for r in ROUTES if r in route_states},
        "decision_reason": reason,
        "block_reason": block,
        "binding_references": {
            "pcg00": dict(BINDINGS),
            "pooling_justification_ref": p["pooling_justification_ref"],
            "temporal_conditioning_spec_ref": p["temporal_conditioning_spec_ref"],
            "robust_method_preregistration_ref": p["robust_method_preregistration_ref"],
        },
        "authority_created": "NONE",
        "qualifying_routes": qualifying,
        "overall_gate_admissibility": overall,
        "method_state": dict(METHOD_STATE),
        "real_data_read": False,
    }


def reference_evaluate(p):
    _validate(p)
    classification = "MATERIAL_TEMPORAL_VARIATION" if p["claim_unit"] in MATERIAL else "NO_MATERIAL_TEMPORAL_VARIATION_DETECTED"

    if p["evidence_state_request"] == "RESET_TO_PRISTINE":
        return _blocked(p, classification, "PRISTINE_RESET_FORBIDDEN")

    ar = set(p["authority_requests"])
    if ar & AUTH:
        return _blocked(p, classification, "METHOD_AUTHORITY_REQUEST_FORBIDDEN")
    if ar & EXEC:
        return _blocked(p, classification, "METHOD_EXECUTION_REQUEST_FORBIDDEN")
    if p["real_data_dependency_requested"]:
        return _blocked(p, classification, "REAL_DATA_DEPENDENCY_FORBIDDEN")

    basis = p["admissibility_basis_claim_unit"]
    if basis is not None and basis != p["claim_unit"]:
        if _metric(basis) != _metric(p["claim_unit"]):
            return _blocked(p, classification, "CROSS_METRIC_PROPAGATION_ATTEMPT")
        return _blocked(p, classification, "CROSS_CLAIM_PROPAGATION_ATTEMPT")

    ordered = [r for r in ROUTES if r in p["requested_routes"]]
    if not ordered:
        any_intent = p["pooling_requested"] or p["conditioning_requested"] or p["preregistered_robust_method_requested"]
        if not any_intent:
            return _assemble(
                p,
                classification,
                {},
                "NOT_APPLICABLE",
                "NO_TEMPORAL_POOLING_OR_CONDITIONING_DECISION_REQUESTED",
                None,
            )
        if classification == "MATERIAL_TEMPORAL_VARIATION":
            return _blocked(p, classification, "MATERIAL_CLAIM_UNIT_NO_ADMISSIBILITY_ROUTE")
        return _assemble(
            p,
            classification,
            {},
            "NOT_ADMISSIBLE_YET",
            "NO_MATERIAL_VARIATION_DETECTED_DOES_NOT_AUTO_VALIDATE_POOLING",
            None,
        )

    states = {}
    for route in ordered:
        if route == "A":
            astat = p["pooling_justification_status"]
            reason = p["pooling_justification_reason_code"]
            if reason in BAD_A_REASONS or astat == "JUSTIFICATION_ABSENT":
                states["A"] = "BLOCKED"
            elif astat == "JUSTIFICATION_PRESENT_PENDING_ADJUDICATION":
                states["A"] = "ROUTE_A_PENDING"
            else:
                states["A"] = "ADMISSIBLE_BY_ROUTE_A"
        elif route == "B":
            if p["temporal_conditioning_spec_status"] == "SPEC_QUALIFIED_AND_FROZEN":
                states["B"] = "ADMISSIBLE_BY_ROUTE_B"
            else:
                states["B"] = "ROUTE_B_PENDING"
        else:
            if p["robust_method_preregistration_status"] == "METHOD_PREREG_QUALIFIED_AND_COMPLETE":
                states["C"] = "ADMISSIBLE_BY_ROUTE_C"
            else:
                states["C"] = "ROUTE_C_PENDING"

    valid = [r for r in ordered if states[r] == "ADMISSIBLE_BY_ROUTE_" + r]
    if valid:
        return _assemble(
            p,
            classification,
            states,
            "ADMISSIBLE",
            "ADMISSIBLE_BY_ONE_OR_MORE_QUALIFIED_ROUTES",
            None,
        )
    return _assemble(
        p,
        classification,
        states,
        "NOT_ADMISSIBLE_YET",
        "NO_QUALIFIED_ROUTE_YET",
        None,
    )
