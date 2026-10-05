"""P1-20 dual-owner common downstream synthetic qualification tests."""

from __future__ import annotations

import copy
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from src import p1_12d_qualified_execution_evidence as p12d
from src import p1_13c_common_evaluation as p13c
from src import p1_14c_common_measurement_provenance as p14c
from src import p1_15c_common_evaluator_authority as p15c
from src import p1_16c_common_qualified_finding as p16c
from src.linked_experiment_execution import LinkedExperimentExecutionResult
from src.p1_12c_qualified_producer_execution import QualifiedProducerExecutionResult
from src.qualified_experimental_finding import (
    POLICY as LEGACY_POLICY,
    _INTERPRETATION_TABLE as LEGACY_INTERPRETATION_TABLE,
)
from tests.p1_20_fixture import build_common_chain, build_p112b_native, build_p112c_native


def test_p120_01_p112b_route_end_to_end(tmp_path: Path):
    chain = build_common_chain(tmp_path, owner="P1.12B")
    assert chain["envelope"].execution_owner_id == "P1.12B"
    assert chain["envelope"].measurement_input_identity == chain["native_result"].stream_sha256
    assert p12d.is_factory_attested_qualified_execution_evidence(chain["envelope"])
    assert p13c.is_factory_attested_common_experiment_evaluation(chain["evaluation"])
    assert p14c.is_factory_attested_common_measurement_provenance(chain["provenance"])
    assert p15c.is_factory_attested_common_evaluation_authority(chain["authority"])
    assert p16c.is_factory_attested_common_qualified_finding(chain["finding"])
    assert chain["finding"].finding_status == "SUPPORTED"


def test_p120_02_p112c_route_end_to_end(tmp_path: Path):
    chain = build_common_chain(tmp_path, owner="P1.12C")
    assert chain["envelope"].execution_owner_id == "P1.12C"
    assert chain["envelope"].measurement_input_identity == chain["native_result"].output_sha256
    assert p12d.is_factory_attested_qualified_execution_evidence(chain["envelope"])
    assert p13c.is_factory_attested_common_experiment_evaluation(chain["evaluation"])
    assert p14c.is_factory_attested_common_measurement_provenance(chain["provenance"])
    assert p15c.is_factory_attested_common_evaluation_authority(chain["authority"])
    assert p16c.is_factory_attested_common_qualified_finding(chain["finding"])
    assert chain["finding"].finding_status == "SUPPORTED"


def test_p120_03_native_owner_semantics_remain_distinct_through_finding(tmp_path: Path):
    b = build_common_chain(tmp_path / "b", owner="P1.12B")
    c = build_common_chain(tmp_path / "c", owner="P1.12C")
    assert type(b["native_result"]) is LinkedExperimentExecutionResult
    assert type(c["native_result"]) is QualifiedProducerExecutionResult
    assert b["envelope"].execution_owner_id == b["evaluation"].execution_owner_id == b["provenance"].execution_owner_id == b["authority"].execution_owner_id == b["finding"].execution_owner_id == "P1.12B"
    assert c["envelope"].execution_owner_id == c["evaluation"].execution_owner_id == c["provenance"].execution_owner_id == c["authority"].execution_owner_id == c["finding"].execution_owner_id == "P1.12C"
    assert b["envelope"].native_result_type_id != c["envelope"].native_result_type_id
    assert b["envelope"].measurement_input_identity != c["envelope"].measurement_input_identity


def test_p120_04_common_envelope_does_not_expand_authority(tmp_path: Path):
    for owner in ("P1.12B", "P1.12C"):
        envelope = build_common_chain(tmp_path / owner, owner=owner)["envelope"]
        assert envelope.scientific_authority is False
        assert envelope.operational_authority is False
        assert envelope.trading_authority is False
        assert envelope.capital_authority is False


def test_p120_05_findings_preserve_no_operational_or_trading_authority(tmp_path: Path):
    for owner in ("P1.12B", "P1.12C"):
        finding = build_common_chain(tmp_path / owner, owner=owner)["finding"]
        assert finding.scientific_authority is False
        assert finding.operational_authority is False
        assert finding.trading_authority is False
        assert finding.capital_authority is False


def test_p120_06_p116c_policy_is_exact_legacy_policy():
    assert p16c.POLICY == LEGACY_POLICY
    assert p16c._INTERPRETATION_TABLE == LEGACY_INTERPRETATION_TABLE


def test_p120_07_forged_p112b_native_result_is_rejected(tmp_path: Path):
    native = build_p112b_native(tmp_path)
    forged = replace(native["native_result"])
    assert type(forged) is LinkedExperimentExecutionResult
    with pytest.raises(ValueError, match="factory attestation"):
        p12d.normalize_qualified_execution(forged, native["qualified_input"])


def test_p120_08_forged_p112c_native_result_is_rejected(tmp_path: Path):
    native = build_p112c_native(tmp_path)
    forged = replace(native["native_result"])
    assert type(forged) is QualifiedProducerExecutionResult
    with pytest.raises(ValueError, match="factory attestation"):
        p12d.normalize_qualified_execution(forged, native["qualified_input"])


def test_p120_09_common_envelope_copy_is_not_attested_and_cannot_be_evaluated(tmp_path: Path):
    chain = build_common_chain(tmp_path, owner="P1.12C")
    envelope = chain["envelope"]
    forged = p12d.QualifiedExecutionEvidenceEnvelope(**asdict(envelope))
    assert not p12d.is_factory_attested_qualified_execution_evidence(forged)
    with pytest.raises(ValueError, match="currently-attested"):
        p13c.submit_common_experiment_evaluation(
            forged,
            chain["qualified_input"],
            evaluator_id="evaluator:forged",
            method_ref="method:forged",
            measurements=(p13c.CommonExperimentMeasurementClaim(
                measurement_id="M-X",
                metric="x",
                observed_value="1",
                unit="u",
                sample_size=1,
                scope="synthetic",
                rationale="forgery test",
            ),),
            prediction_status="SUPPORTED",
            falsification_status="NOT_FALSIFIED",
            evaluation_rationale="must not pass",
        )


def test_p120_10_cross_owner_authority_substitution_is_rejected(tmp_path: Path):
    b = build_common_chain(tmp_path / "b", owner="P1.12B")
    c = build_common_chain(tmp_path / "c", owner="P1.12C")
    with pytest.raises(ValueError, match="upstream mismatch"):
        p16c.interpret_common_qualified_finding(b["evaluation"], c["authority"])
    with pytest.raises(ValueError, match="upstream mismatch"):
        p16c.interpret_common_qualified_finding(c["evaluation"], b["authority"])


def test_p120_11_normalization_same_native_result_is_deterministic(tmp_path: Path):
    native = build_p112c_native(tmp_path)
    first = native["envelope"]
    second = p12d.normalize_qualified_execution(native["native_result"], native["qualified_input"])
    assert first is not second
    assert first.execution_evidence_envelope_id == second.execution_evidence_envelope_id
    assert first.native_result_snapshot_digest == second.native_result_snapshot_digest
    assert first.measurement_input_identity == second.measurement_input_identity


def test_p120_12_runtime_attestation_is_not_durable_reconstruction_claim(tmp_path: Path):
    chain = build_common_chain(tmp_path, owner="P1.12C")
    envelope = chain["envelope"]
    assert envelope.reconstruction_class == chain["native_result"].reconstruction_class
    assert "factory_attested" in envelope.native_attestation_verifier_ref
    assert p12d.validate_common_boundary_claim("RUNTIME_ATTESTATION_AS_DURABLE") == {
        "contract": p12d.CONTRACT,
        "status": "BLOCKED",
        "reason": "BLOCKED_RUNTIME_ATTESTATION_NOT_DURABLE",
    }


def test_p120_13_common_evaluation_keeps_execution_status_separate_from_scientific_status(tmp_path: Path):
    chain = build_common_chain(tmp_path, owner="P1.12C")
    evaluation = chain["evaluation"]
    assert evaluation.native_execution_status == chain["envelope"].native_execution_status
    assert evaluation.prediction_status == "SUPPORTED"
    assert evaluation.native_execution_status != evaluation.prediction_status


def test_p120_14_measurement_lineage_binds_exact_owner_specific_input_identity(tmp_path: Path):
    for owner in ("P1.12B", "P1.12C"):
        chain = build_common_chain(tmp_path / owner, owner=owner)
        provenance = chain["provenance"]
        assert provenance.measurement_input_identity == chain["envelope"].measurement_input_identity
        assert all(item.measurement_input_identity == chain["envelope"].measurement_input_identity for item in provenance.derivations)
        assert all(item.native_result_id == chain["envelope"].native_result_id for item in provenance.derivations)


def test_p120_15_manual_copies_of_common_outputs_are_not_factory_attested(tmp_path: Path):
    chain = build_common_chain(tmp_path, owner="P1.12B")
    assert not p13c.is_factory_attested_common_experiment_evaluation(copy.copy(chain["evaluation"]))
    assert not p14c.is_factory_attested_common_measurement_provenance(copy.copy(chain["provenance"]))
    assert not p15c.is_factory_attested_common_evaluation_authority(copy.copy(chain["authority"]))
    assert not p16c.is_factory_attested_common_qualified_finding(copy.copy(chain["finding"]))
