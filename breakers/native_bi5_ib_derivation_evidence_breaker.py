from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest


IB_ID = "I_B_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_INDEPENDENT_QUALIFIER"
IB_VERSION = "I_B_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_INDEPENDENT_QUALIFIER_V0_1_CANDIDATE"

PROVENANCE = Path("reports/data-qualification/iab/ib_semantic_source_provenance.json")
NO_COPY = Path("reports/data-qualification/iab/ib_no_copy_declaration.json")
INVENTORY = Path("reports/data-qualification/iab/ib_independent_stage_test_inventory.json")
IB_SOURCE = Path("src/native_bi5_independent_qualifier.py")
IA_SOURCE = "src/native_bi5_reference_qualifier.py"

REQUIRED_STAGES = {
    "D_PREFLIGHT",
    "R_COMPATIBILITY",
    "B_ENVELOPE",
    "B_FRAMING",
    "B_BINARY_DECODE",
    "B_TIMESTAMP",
    "B_PRICE",
    "B_VOLUME",
    "A_CLASSIFICATION",
    "M_OCCURRENCE",
    "Q_MEMBERSHIP",
    "F_FREEZE",
}

EXPECTED_ALLOWED_INPUTS = {
    "reports/data-qualification/drm_first_concrete_candidate_formalization_2026-09-19.md":
        "2249bea6dbf6b5a8e0d49b99a93bf16248f9c0e9",
    "reports/data-qualification/ba_native_bi5_binding_anomaly_candidate_2026-09-19.md":
        "25400abcc3a2a24438954ff27b970bd934313ae3",
    "reports/data-qualification/q_native_bi5_qualification_contract_candidate_2026-09-19.md":
        "9e15cfb86716894131485a15a180cc170a230287",
    "reports/data-qualification/fo_native_bi5_freeze_oracle_candidate_2026-09-19.md":
        "fe62da06e63a51c336f9a447e7f1e0f3d89cad3b",
    "reports/data-qualification/iab_native_bi5_implementation_boundary_candidate_2026-09-19.md":
        "fac8d143a836b0c02538c607ac5ab71357824537",
    "breakers/native_bi5_ib_independent_qualifier_breaker.py":
        "d1a305e3b9ae813e891b34522e3a12bb6bc8ac34",
}


def _load(path: Path):
    return json.loads(path.read_text("utf-8"))


def _canonical_sha256(value) -> str:
    raw = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _git_blob_sha1(path: Path) -> str:
    raw = path.read_bytes()
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


@pytest.fixture(scope="module")
def evidence():
    return _load(PROVENANCE), _load(NO_COPY), _load(INVENTORY)


def test_e0_exact_three_evidence_artifacts_exist_and_ib_source_is_absent() -> None:
    assert PROVENANCE.is_file()
    assert NO_COPY.is_file()
    assert INVENTORY.is_file()
    assert not IB_SOURCE.exists()


def test_e1_identity_and_phase_are_exact(evidence) -> None:
    for artifact in evidence:
        assert artifact["implementation_id"] == IB_ID
        assert artifact["implementation_version"] == IB_VERSION
        assert artifact["evidence_phase"] == "PRE_IMPLEMENTATION_DERIVATION"
        assert artifact["source_binding_state"] == "PENDING_IMPLEMENTATION_SOURCE"
        assert artifact["source_digests"] == {}


def test_e2_frozen_semantic_payload_integrity_is_self_consistent(evidence) -> None:
    for artifact in evidence:
        assert artifact["frozen_semantic_payload_sha256"] == _canonical_sha256(
            artifact["frozen_semantic_payload"]
        )


def test_e3_provenance_is_future_breaker_compatible_and_normative_only(evidence) -> None:
    provenance, _, _ = evidence
    assert provenance["derivation_basis"] == "PINNED_NORMATIVE_CONTRACTS"

    payload = provenance["frozen_semantic_payload"]
    allowed = {
        item["path"]: item["blob"]
        for item in payload["allowed_derivation_inputs"]
    }
    assert allowed == EXPECTED_ALLOWED_INPUTS
    assert IA_SOURCE not in allowed
    assert IA_SOURCE in payload["forbidden_derivation_inputs"]

    for path, expected_blob in allowed.items():
        assert Path(path).is_file()
        assert _git_blob_sha1(Path(path)) == expected_blob

    fo = next(
        item
        for item in payload["allowed_derivation_inputs"]
        if item["path"].endswith("fo_native_bi5_freeze_oracle_candidate_2026-09-19.md")
    )
    assert fo["scope"] == ["F_ONLY"]
    assert fo["forbidden_scope"] == ["O_CONSTRUCTION_LOGIC"]


def test_e4_source_binding_protocol_is_non_circular_and_freezes_semantics(evidence) -> None:
    protocols = [
        artifact["frozen_semantic_payload"]["source_binding_protocol"]
        for artifact in evidence
    ]
    assert protocols[0] == protocols[1] == protocols[2]
    protocol = protocols[0]
    assert protocol["pre_code_state"] == "PENDING_IMPLEMENTATION_SOURCE"
    assert protocol["target_source_files"] == ["src/native_bi5_independent_qualifier.py"]
    assert set(protocol["post_code_allowed_mutation"]) == {
        "source_digests",
        "source_binding_state",
    }
    assert protocol["post_code_forbidden_mutation"] == (
        "all fields inside frozen_semantic_payload"
    )
    assert "future I_B implementation manifest source_digests" in protocol[
        "final_binding_requirement"
    ]
    assert "does not by itself qualify I_B executable implementation" in protocol[
        "adjudication_rule"
    ]


def test_e5_no_copy_declaration_is_explicit_but_not_self_adjudicating(evidence) -> None:
    _, declaration, _ = evidence
    assert declaration["statement"] == (
        "INDEPENDENTLY_DERIVED_NOT_COPIED_OR_GENERATED_FROM_I_A"
    )
    payload = declaration["frozen_semantic_payload"]
    assert payload["self_attestation_is_not_pass_evidence"] is True
    methods = " ".join(payload["forbidden_derivation_methods"]).lower()
    for token in (
        "copying i_a source",
        "mechanical renaming",
        "porting i_a",
        "generating i_b from i_a",
        "wrapping or delegating to i_a",
        "expected answers",
        "o comparison output",
        "shared project-owned semantic helpers",
    ):
        assert token in methods


def test_e6_stage_inventory_covers_every_required_stage_without_expected_answer_oracle(evidence) -> None:
    _, _, inventory = evidence
    assert set(inventory["semantic_stages"]) == REQUIRED_STAGES
    tests = inventory["tests"]
    assert tests
    assert len({item["test_id"] for item in tests}) == len(tests)

    covered = {item["stage"] for item in tests}
    assert covered == REQUIRED_STAGES

    for item in tests:
        if "I_A" in item["fixture"] or "O " in item["fixture"]:
            assertion = item["assertion"].lower()
            assert any(word in assertion for word in ("reject", "absent", "forbid"))

    joined = json.dumps(tests, sort_keys=True)
    assert "expected I_A answer" not in joined
    assert "expected_result.json" not in joined


def test_e7_anomaly_inventory_is_granular_enough_to_test_current_a_matrix(evidence) -> None:
    _, _, inventory = evidence
    joined = json.dumps(inventory["tests"], sort_keys=True)
    for number in range(1, 14):
        assert f"A{number:02d}" in joined
    assert "constructive completeness" in joined.lower()
    assert "terminal partial" in joined.lower()


def test_e8_inventory_contains_independence_critical_semantic_attacks(evidence) -> None:
    _, _, inventory = evidence
    joined = json.dumps(inventory["tests"], sort_keys=True).lower()
    required = (
        "strict duplicate",
        "timestamp regression",
        "zero and crossed",
        "finite negative",
        "no partial qualified universe",
        "source",
        "one-sided i_b semantic mutant",
    )
    for token in required:
        assert token in joined
