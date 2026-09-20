from __future__ import annotations

import copy
from dataclasses import replace
from typing import Any

import pytest

from breakers import native_bi5_qrm12_compatibility_breaker as qrm
from src import native_bi5_qrm12_handoff as handoff


def _normal():
    ia, ib, left, right = qrm._qualify_pair()
    left_receipt = qrm._receipt(
        ia, left, run_id="HANDOFF-A", workspace="QRM12-IA-PRIVATE"
    )
    right_receipt = qrm._receipt(
        ib, right, run_id="HANDOFF-B", workspace="QRM12-IB-PRIVATE"
    )
    return (
        ia,
        ib,
        left,
        left_receipt,
        right,
        right_receipt,
        qrm._pin(ia),
        qrm._pin(ib),
    )


def _run(
    left,
    left_receipt,
    right,
    right_receipt,
    left_pin,
    right_pin,
):
    return handoff.compare_sealed_results(
        left,
        left_receipt,
        right,
        right_receipt,
        expected_left=left_pin,
        expected_right=right_pin,
    )


def test_control_normal_pair_reaches_exact_o_semantic_equal() -> None:
    _, _, left, lr, right, rr, lp, rp = _normal()
    result = _run(left, lr, right, rr, lp, rp)
    assert result["handoff_result"] == "SEMANTIC_EQUAL"
    assert result["oracle_result"] == "SEMANTIC_EQUAL"


def test_h1_left_right_roles_are_not_interchangeable() -> None:
    ia, ib, left, _, right, _, _, _ = _normal()
    swapped_left_receipt = qrm._receipt(
        ib, right, run_id="SWAPPED-B-AS-LEFT", workspace="QRM12-IB-PRIVATE"
    )
    swapped_right_receipt = qrm._receipt(
        ia, left, run_id="SWAPPED-A-AS-RIGHT", workspace="QRM12-IA-PRIVATE"
    )
    result = _run(
        right,
        swapped_left_receipt,
        left,
        swapped_right_receipt,
        qrm._pin(ib),
        qrm._pin(ia),
    )
    assert result["handoff_result"] == "BLOCKED"
    assert result["oracle_result"] == "NOT_INVOKED"


def test_h2_both_results_cannot_rebind_to_a_forged_o_version() -> None:
    ia, ib, left, _, right, _, lp, rp = _normal()
    left2 = qrm._replace_binding(
        left,
        "O",
        normative_version="O_FORGED_SAME_VERSION_ON_BOTH_PATHS",
    )
    right2 = qrm._replace_binding(
        right,
        "O",
        normative_version="O_FORGED_SAME_VERSION_ON_BOTH_PATHS",
    )
    left2 = qrm._reseal_result(left2)
    right2 = qrm._reseal_result(right2)
    lr = qrm._receipt(
        ia, left2, run_id="FORGED-O-A", workspace="QRM12-IA-PRIVATE"
    )
    rr = qrm._receipt(
        ib, right2, run_id="FORGED-O-B", workspace="QRM12-IB-PRIVATE"
    )
    result = _run(left2, lr, right2, rr, lp, rp)
    assert result["handoff_result"] == "BLOCKED"
    assert result["oracle_result"] == "NOT_INVOKED"


def test_h3_path_workspaces_must_remain_distinct() -> None:
    ia, ib, left, lr, right, _, lp, rp = _normal()
    isolation = copy.deepcopy(dict(right.isolation_evidence))
    isolation["workspace_isolation_identity"] = "QRM12-IA-PRIVATE"
    right2 = qrm._reseal_result(replace(right, isolation_evidence=isolation))
    rr = qrm._receipt(
        ib,
        right2,
        run_id="WORKSPACE-COLLISION-B",
        workspace="QRM12-IA-PRIVATE",
    )
    result = _run(left, lr, right2, rr, lp, rp)
    assert result["handoff_result"] == "BLOCKED"
    assert result["oracle_result"] == "NOT_INVOKED"


def test_h4_external_pin_schema_is_closed() -> None:
    _, _, left, lr, right, rr, lp, rp = _normal()
    forged = dict(lp)
    forged["extra_authority"] = "NOT_ALLOWED"
    result = _run(left, lr, right, rr, forged, rp)
    assert result["handoff_result"] == "BLOCKED"
    assert result["oracle_result"] == "NOT_INVOKED"


def test_h5_oracle_output_identity_and_schema_are_validated(monkeypatch) -> None:
    _, _, left, lr, right, rr, lp, rp = _normal()

    def forged_oracle(_left: Any, _right: Any):
        return {
            "schema": "FORGED_ORACLE_SCHEMA",
            "oracle_id": "FORGED_ORACLE",
            "oracle_version": "FORGED_VERSION",
            "oracle_result": "SEMANTIC_EQUAL",
            "qualified_universe_comparison": "SEMANTIC_EQUAL",
            "comparison_scope": "SAME_QUALIFICATION_STATE",
            "reason": "FORGED_BUT_PLAUSIBLE",
        }

    monkeypatch.setattr(handoff.oracle, "compare_freeze_artifacts", forged_oracle)
    result = _run(left, lr, right, rr, lp, rp)
    assert result["handoff_result"] == "BLOCKED"


def test_h6_oracle_output_keyset_is_closed(monkeypatch) -> None:
    _, _, left, lr, right, rr, lp, rp = _normal()
    original = handoff.oracle.compare_freeze_artifacts

    def extra_key_oracle(_left: Any, _right: Any):
        value = dict(original(_left, _right))
        value["postseal_repair_hint"] = "MUST_NOT_BE_ACCEPTED"
        return value

    monkeypatch.setattr(handoff.oracle, "compare_freeze_artifacts", extra_key_oracle)
    result = _run(left, lr, right, rr, lp, rp)
    assert result["handoff_result"] == "BLOCKED"


def test_h7_handoff_inputs_remain_immutable_on_blocked_path() -> None:
    _, _, left, lr, right, rr, lp, rp = _normal()
    forged = dict(lr)
    forged["result_seal"] = "0" * 64
    before = copy.deepcopy((left, forged, right, rr, lp, rp))
    _run(left, forged, right, rr, lp, rp)
    after = (left, forged, right, rr, lp, rp)
    assert after == before
