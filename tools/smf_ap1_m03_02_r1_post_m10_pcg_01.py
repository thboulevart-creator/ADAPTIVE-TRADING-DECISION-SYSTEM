from __future__ import annotations

import json

PCG00_BINDINGS = {
    "contract_blob": "8e6e888f8330e40d792b43650c32b09a8dc6a281",
    "decision_table_blob": "da9bb3a7436072795fced2d171cae8df23591279",
    "breaker_contract_blob": "c52eca89c45fd68e83c506925626a3c389b5d4a2",
    "traceability_blob": "364baff4a603c9be69f29742ba2647477742974f",
    "final_receipt_blob": "769fcc81f4b365b4a54152042be31a2dd1ce9412",
    "final_closure_blob": "4433648fb71684695513eddb2c60c4eddae41b6a",
}

MATERIAL_CLAIMS = (
    "tick_count p50",
    "tick_count p90",
    "tick_count p99",
    "minute_range p50",
    "minute_range p90",
    "minute_range p95",
    "minute_range p99",
    "spread_mean p50",
)

NON_MATERIAL_CLAIMS = (
    "spread_mean p90",
    "spread_mean p95",
    "spread_mean p99",
)

ALL_CLAIMS = frozenset(MATERIAL_CLAIMS + NON_MATERIAL_CLAIMS)
ROUTE_ORDER = ("A", "B", "C")
ALLOWED_ROUTES = frozenset(ROUTE_ORDER)

REQUIRED_FIELDS = frozenset(
    {
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
)

A_STATUSES = frozenset(
    {
        "JUSTIFICATION_ABSENT",
        "JUSTIFICATION_PRESENT_PENDING_ADJUDICATION",
        "JUSTIFICATION_HUMAN_ADOPTED",
    }
)
B_STATUSES = frozenset(
    {
        "SPEC_ABSENT",
        "SPEC_PRESENT_NOT_QUALIFIED_OR_FROZEN",
        "SPEC_QUALIFIED_AND_FROZEN",
    }
)
C_STATUSES = frozenset(
    {
        "METHOD_PREREG_ABSENT_OR_INCOMPLETE",
        "METHOD_PREREG_QUALIFIED_AND_COMPLETE",
    }
)
EVIDENCE_STATES = frozenset(
    {"PRESERVE_EXPOSED_NON_PRISTINE", "RESET_TO_PRISTINE"}
)
METHOD_AUTHORITY_REQUESTS = frozenset(
    {"M04_AUTHORIZE", "M05_AUTHORIZE", "M08_AUTHORIZE", "M09_AUTHORIZE", "M11_AUTHORIZE"}
)
METHOD_EXECUTION_REQUESTS = frozenset(
    {"METHOD_EXECUTE", "M04_EXECUTE", "M05_EXECUTE", "M08_EXECUTE", "M09_EXECUTE", "M11_EXECUTE"}
)
KNOWN_AUTHORITY_REQUESTS = METHOD_AUTHORITY_REQUESTS | METHOD_EXECUTION_REQUESTS
INSUFFICIENT_A_REASONS = frozenset(
    {
        "ALL_YEARS_BELONG_TO_SAME_DATASET_ONLY",
        "SAMPLE_SIZE_IS_LARGE_ONLY",
        "POOLING_IS_CONVENIENT_ONLY",
    }
)
ROBUST_METHOD_REQUIRED_FIELDS = (
    "EXACT_METHOD_IDENTITY",
    "EXACT_FAILURE_MODE",
    "EXACT_ASSUMPTION_SET",
    "EXACT_VALIDITY_SCOPE",
    "EXACT_MATERIAL_PARAMETERS",
)
METHOD_STATE = {"M04": "CLOSED", "M05": "CLOSED", "M08": "CLOSED", "M09": "CLOSED", "M11": "CLOSED"}


class PCGFailClosedError(ValueError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def canonical_json_bytes(value) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")


def _nonempty_string(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _metric(claim_unit: str) -> str:
    return claim_unit.split(" ", 1)[0]


def _fail(code: str):
    raise PCGFailClosedError(code)


def _validate_packet(packet):
    if not isinstance(packet, dict):
        _fail("PACKET_NOT_OBJECT")

    keys = set(packet)
    missing = REQUIRED_FIELDS - keys
    if missing:
        _fail("MISSING_REQUIRED_FIELD")
    extra = keys - REQUIRED_FIELDS
    if extra:
        _fail("UNKNOWN_INPUT_FIELD")

    for key in ("case_id", "claim_unit", "downstream_claim_id", "downstream_analysis_id", "requested_temporal_scope"):
        if not _nonempty_string(packet[key]):
            _fail("MALFORMED_REQUIRED_FIELD")

    claim = packet["claim_unit"]
    if claim not in ALL_CLAIMS:
        _fail("UNKNOWN_CLAIM_UNIT")

    for key in ("pooling_requested", "conditioning_requested", "preregistered_robust_method_requested", "real_data_dependency_requested"):
        if not isinstance(packet[key], bool):
            _fail("MALFORMED_REQUIRED_FIELD")

    routes = packet["requested_routes"]
    if not isinstance(routes, list) or not all(isinstance(x, str) for x in routes):
        _fail("MALFORMED_ROUTE_LIST")
    if len(set(routes)) != len(routes):
        _fail("DUPLICATE_ROUTE")
    if any(x not in ALLOWED_ROUTES for x in routes):
        _fail("UNKNOWN_ROUTE")

    if ("A" in routes and not packet["pooling_requested"]):
        _fail("ROUTE_REQUEST_CONTRADICTION")
    if ("B" in routes) != packet["conditioning_requested"]:
        _fail("ROUTE_REQUEST_CONTRADICTION")
    if ("C" in routes) != packet["preregistered_robust_method_requested"]:
        _fail("ROUTE_REQUEST_CONTRADICTION")

    if packet["pooling_justification_status"] not in A_STATUSES:
        _fail("MALFORMED_REFERENCE_STATUS")
    if packet["temporal_conditioning_spec_status"] not in B_STATUSES:
        _fail("MALFORMED_REFERENCE_STATUS")
    if packet["robust_method_preregistration_status"] not in C_STATUSES:
        _fail("MALFORMED_REFERENCE_STATUS")
    if packet["evidence_state_request"] not in EVIDENCE_STATES:
        _fail("MALFORMED_EVIDENCE_STATE")

    a_status = packet["pooling_justification_status"]
    a_ref = packet["pooling_justification_ref"]
    a_reason = packet["pooling_justification_reason_code"]
    if a_status == "JUSTIFICATION_ABSENT":
        if a_ref is not None or a_reason != "NONE":
            _fail("MALFORMED_REFERENCE_STATUS")
    else:
        if not _nonempty_string(a_ref) or not _nonempty_string(a_reason) or a_reason == "NONE":
            _fail("MALFORMED_REFERENCE_STATUS")

    b_status = packet["temporal_conditioning_spec_status"]
    b_ref = packet["temporal_conditioning_spec_ref"]
    if b_status == "SPEC_ABSENT":
        if b_ref is not None:
            _fail("MALFORMED_REFERENCE_STATUS")
    elif not _nonempty_string(b_ref):
        _fail("MALFORMED_REFERENCE_STATUS")

    c_status = packet["robust_method_preregistration_status"]
    c_ref = packet["robust_method_preregistration_ref"]
    c_fields = packet["robust_method_fields"]
    if not isinstance(c_fields, dict):
        _fail("MALFORMED_ROBUST_METHOD_PREREGISTRATION")
    if c_status == "METHOD_PREREG_QUALIFIED_AND_COMPLETE":
        if not _nonempty_string(c_ref):
            _fail("MALFORMED_REFERENCE_STATUS")
        if set(c_fields) != set(ROBUST_METHOD_REQUIRED_FIELDS):
            _fail("MALFORMED_ROBUST_METHOD_PREREGISTRATION")
        if not all(_nonempty_string(c_fields[x]) for x in ROBUST_METHOD_REQUIRED_FIELDS):
            _fail("MALFORMED_ROBUST_METHOD_PREREGISTRATION")

    requests = packet["authority_requests"]
    if not isinstance(requests, list) or not all(isinstance(x, str) for x in requests):
        _fail("MALFORMED_AUTHORITY_REQUEST")
    if any(x not in KNOWN_AUTHORITY_REQUESTS for x in requests):
        _fail("UNKNOWN_AUTHORITY_REQUEST")

    basis = packet["admissibility_basis_claim_unit"]
    if basis is not None and not _nonempty_string(basis):
        _fail("MALFORMED_BASIS_CLAIM_UNIT")


def _hard_block_reason(packet):
    if packet["evidence_state_request"] == "RESET_TO_PRISTINE":
        return "PRISTINE_RESET_FORBIDDEN"

    requests = set(packet["authority_requests"])
    if requests & METHOD_AUTHORITY_REQUESTS:
        return "METHOD_AUTHORITY_REQUEST_FORBIDDEN"
    if requests & METHOD_EXECUTION_REQUESTS:
        return "METHOD_EXECUTION_REQUEST_FORBIDDEN"

    if packet["real_data_dependency_requested"]:
        return "REAL_DATA_DEPENDENCY_FORBIDDEN"

    basis = packet["admissibility_basis_claim_unit"]
    if basis is not None and basis != packet["claim_unit"]:
        if _metric(basis) != _metric(packet["claim_unit"]):
            return "CROSS_METRIC_PROPAGATION_ATTEMPT"
        return "CROSS_CLAIM_PROPAGATION_ATTEMPT"

    return None


def _route_a(packet):
    status = packet["pooling_justification_status"]
    reason = packet["pooling_justification_reason_code"]
    if reason in INSUFFICIENT_A_REASONS:
        return "BLOCKED"
    if status == "JUSTIFICATION_ABSENT":
        return "BLOCKED"
    if status == "JUSTIFICATION_PRESENT_PENDING_ADJUDICATION":
        return "ROUTE_A_PENDING"
    return "ADMISSIBLE_BY_ROUTE_A"


def _route_b(packet):
    status = packet["temporal_conditioning_spec_status"]
    if status in {"SPEC_ABSENT", "SPEC_PRESENT_NOT_QUALIFIED_OR_FROZEN"}:
        return "ROUTE_B_PENDING"
    return "ADMISSIBLE_BY_ROUTE_B"


def _route_c(packet):
    status = packet["robust_method_preregistration_status"]
    if status == "METHOD_PREREG_ABSENT_OR_INCOMPLETE":
        return "ROUTE_C_PENDING"
    return "ADMISSIBLE_BY_ROUTE_C"


def _output(packet, classification, route_states, overall, reason, block_reason):
    requested = [x for x in ROUTE_ORDER if x in packet["requested_routes"]]
    qualifying = [
        route
        for route in ROUTE_ORDER
        if route_states.get(route) == "ADMISSIBLE_BY_ROUTE_" + route
    ]
    if not requested:
        selected = "NONE"
    elif len(requested) == 1:
        selected = requested[0]
    else:
        selected = "MULTIPLE"

    if block_reason is not None:
        gate_state = ["BLOCKED"]
        qualifying = []
    else:
        gate_state = [route_states[x] for x in requested] if requested else []
    if block_reason is None and not gate_state:
        if overall == "NOT_APPLICABLE":
            gate_state = ["NOT_APPLICABLE"]
        elif classification == "MATERIAL_TEMPORAL_VARIATION":
            gate_state = ["BLOCKED"]
        else:
            gate_state = ["NON_MATERIAL_POOLING_REVIEW_REQUIRED"]

    return {
        "claim_unit": packet["claim_unit"],
        "downstream_claim_id": packet["downstream_claim_id"],
        "downstream_analysis_id": packet["downstream_analysis_id"],
        "requested_temporal_scope": packet["requested_temporal_scope"],
        "input_classification": classification,
        "selected_route": selected,
        "gate_state": gate_state,
        "route_states": {k: route_states[k] for k in ROUTE_ORDER if k in route_states},
        "decision_reason": reason,
        "block_reason": block_reason,
        "binding_references": {
            "pcg00": dict(PCG00_BINDINGS),
            "pooling_justification_ref": packet["pooling_justification_ref"],
            "temporal_conditioning_spec_ref": packet["temporal_conditioning_spec_ref"],
            "robust_method_preregistration_ref": packet["robust_method_preregistration_ref"],
        },
        "authority_created": "NONE",
        "qualifying_routes": qualifying,
        "overall_gate_admissibility": overall,
        "method_state": dict(METHOD_STATE),
        "real_data_read": False,
    }


def evaluate(packet):
    _validate_packet(packet)

    classification = (
        "MATERIAL_TEMPORAL_VARIATION"
        if packet["claim_unit"] in MATERIAL_CLAIMS
        else "NO_MATERIAL_TEMPORAL_VARIATION_DETECTED"
    )

    hard_block = _hard_block_reason(packet)
    if hard_block is not None:
        return _output(
            packet,
            classification,
            {},
            "BLOCKED",
            hard_block,
            hard_block,
        )

    requested = [x for x in ROUTE_ORDER if x in packet["requested_routes"]]

    if not requested:
        if not (
            packet["pooling_requested"]
            or packet["conditioning_requested"]
            or packet["preregistered_robust_method_requested"]
        ):
            return _output(
                packet,
                classification,
                {},
                "NOT_APPLICABLE",
                "NO_TEMPORAL_POOLING_OR_CONDITIONING_DECISION_REQUESTED",
                None,
            )
        if classification == "MATERIAL_TEMPORAL_VARIATION":
            return _output(
                packet,
                classification,
                {},
                "BLOCKED",
                "MATERIAL_CLAIM_UNIT_NO_ADMISSIBILITY_ROUTE",
                "MATERIAL_CLAIM_UNIT_NO_ADMISSIBILITY_ROUTE",
            )
        return _output(
            packet,
            classification,
            {},
            "NOT_ADMISSIBLE_YET",
            "NO_MATERIAL_VARIATION_DETECTED_DOES_NOT_AUTO_VALIDATE_POOLING",
            None,
        )

    route_states = {}
    for route in requested:
        if route == "A":
            route_states[route] = _route_a(packet)
        elif route == "B":
            route_states[route] = _route_b(packet)
        else:
            route_states[route] = _route_c(packet)

    qualifying = [
        route
        for route in requested
        if route_states[route] == "ADMISSIBLE_BY_ROUTE_" + route
    ]
    if qualifying:
        overall = "ADMISSIBLE"
        reason = "ADMISSIBLE_BY_ONE_OR_MORE_QUALIFIED_ROUTES"
    else:
        overall = "NOT_ADMISSIBLE_YET"
        reason = "NO_QUALIFIED_ROUTE_YET"

    return _output(packet, classification, route_states, overall, reason, None)
