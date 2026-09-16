import copy
import json
import lzma
from dataclasses import replace
from pathlib import Path

import pytest

from src.context import build_context
from src.data.dataset_admissibility import DatasetIdentity
from src.decision import produce_decision
from src.research.engine import BI5ResearchEngine
from src.research.execution import (
    QualifiedResearchInput,
    is_qualified_execution_result,
    run_qualified_research,
)
from src.research.input_binding import (
    BoundResearchInput,
    bind_execution_input,
    corpus_inventory_hash,
    is_bound_research_input,
    sha256_file,
)
from src.research_findings import (
    ResearchFinding,
    ResearchFindings,
    ResearchHypothesis,
    ResearchMeasurement,
)
from src.research_run_evidence import (
    ResearchRunEvidence,
    _stable_hash,
    from_research_execution,
    from_v43_report,
    is_factory_attested,
)
from tests.research_runtime_fixture import CODE_VERSION, synthetic_runtime_case


def legacy_inputs():
    report = {
        "schema": "RESEARCH_EXECUTION_COMPATIBILITY_V4_3",
        "version": "V4.3",
        "status": "UNVERIFIED",
        "scope": {
            "research_instrument": "Dukascopy USATECHIDXUSD",
            "execution_instrument": "VT Markets NAS100.s",
            "minimum_research_years": 5.0,
        },
        "research": {
            "files": [
                {"path": "research/a.bi5", "sha256": "aaa"},
                {"path": "research/b.bi5", "sha256": "bbb"},
            ],
            "rows": 100,
            "first": "2020-01-01T00:00:00+00:00",
            "last": "2025-01-01T00:00:00+00:00",
        },
    }
    source_hashes = ["aaa", "bbb"]
    dataset_id = "DATA-" + _stable_hash({"research_files": source_hashes})[:16]
    dataset_version = _stable_hash(report["research"])[:16]
    configuration_version = "CFG-" + _stable_hash(report["scope"])[:16]
    dataset = DatasetIdentity(
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        content_hash="content-hash",
        format="csv",
        schema_version="tick-csv-v1",
        instrument="VT Markets NAS100.s",
        granularity="tick",
        timezone_storage="UTC",
    )
    context = build_context(
        dataset,
        configuration_version=configuration_version,
        observation_start="2020-01-01T00:00:00+00:00",
        observation_end="2025-01-01T00:00:00+00:00",
    )
    return report, dataset, context


def _qualified_input(root: Path, *, write_empty_bi5: bool) -> QualifiedResearchInput:
    corpus = root / "corpus"
    corpus.mkdir(parents=True)
    if write_empty_bi5:
        (corpus / "2026010200.bi5").write_bytes(lzma.compress(b"", format=lzma.FORMAT_ALONE))
    contract_path = root / "contract.json"
    contract_path.write_text(
        json.dumps(
            {
                "asset_id": "USATECHIDXUSD",
                "source": "Dukascopy",
                "format": "BI5",
                "record_size": 20,
                "record_struct": ">IIIff",
                "timestamp_unit": "milliseconds",
                "price_scale": 1000,
            },
            sort_keys=True,
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )
    return QualifiedResearchInput(
        corpus_root=corpus,
        contract_path=contract_path,
        expected_corpus_hash=corpus_inventory_hash(corpus),
        expected_contract_hash=sha256_file(contract_path),
    )


def test_c0_real_runtime_path_is_attested_and_downstream_admissible() -> None:
    with synthetic_runtime_case() as case:
        assert is_qualified_execution_result(case.result, case.execution_input)
        assert is_factory_attested(case.evidence)
        decision = produce_decision(case.evidence, context=case.context, decision="HOLD")
        assert decision.research_run_id == case.evidence.research_run_id

        hypothesis = ResearchHypothesis("H1", "scope", "prediction", "falsifier")
        measurement = ResearchMeasurement("M1", "RUN", "EXP", "metric", 1.0, 1, "scope")
        finding = ResearchFinding("F1", "H1", "scope", ("M1",), "SUPPORTED", "rule", "reason")
        findings = ResearchFindings.from_research_run_evidence(
            case.evidence,
            hypotheses=(hypothesis,),
            measurements=(measurement,),
            findings=(finding,),
        )
        assert findings.research_run_id == case.evidence.research_run_id


def test_c1_legacy_v43_report_only_path_is_not_downstream_admissible() -> None:
    report, dataset, context = legacy_inputs()
    evidence = from_v43_report(report, code_version=CODE_VERSION, context=context, dataset=dataset)
    assert not is_factory_attested(evidence)
    with pytest.raises(ValueError, match="factory-attested"):
        produce_decision(evidence, context=context, decision="HOLD")


def test_c2_module_exposes_no_raw_evidence_attestation_minter() -> None:
    import src.research_run_evidence as module

    assert not hasattr(module, "_attest_factory_evidence")


def test_c3_manual_evidence_cannot_be_promoted_through_module_escape() -> None:
    import src.research_run_evidence as module

    _, _, context = legacy_inputs()
    fabricated = ResearchRunEvidence(
        provenance_id="PROV-manual",
        research_run_id="RUN-manual",
        code_version=CODE_VERSION,
        configuration_version=context.configuration_version,
        dataset_id=context.dataset_id,
        dataset_version=context.dataset_version,
        context_id=context.context_id,
    )
    assert getattr(module, "_attest_factory_evidence", None) is None
    assert not is_factory_attested(fabricated)
    with pytest.raises(ValueError, match="factory-attested"):
        produce_decision(fabricated, context=context, decision="HOLD")


def test_c4_reconstructed_and_copied_bound_inputs_are_rejected() -> None:
    with synthetic_runtime_case() as case:
        bound = bind_execution_input(
            case.execution_input.corpus_root,
            case.execution_input.contract_path,
            case.execution_input.expected_corpus_hash,
            case.execution_input.expected_contract_hash,
        )
        assert is_bound_research_input(bound)
        reconstructed = BoundResearchInput(
            corpus_root=bound.corpus_root,
            contract_path=bound.contract_path,
            contract=dict(bound.contract),
            expected_corpus_hash=bound.expected_corpus_hash,
            expected_contract_hash=bound.expected_contract_hash,
        )
        for candidate in (reconstructed, copy.copy(bound), copy.deepcopy(bound)):
            assert candidate is not bound
            assert not is_bound_research_input(candidate, revalidate_sources=False)
            with pytest.raises(ValueError, match="factory-bound"):
                BI5ResearchEngine(candidate)


def test_c5_post_binding_identity_mutation_invalidates_bound_input() -> None:
    with synthetic_runtime_case() as case:
        bound = bind_execution_input(
            case.execution_input.corpus_root,
            case.execution_input.contract_path,
            case.execution_input.expected_corpus_hash,
            case.execution_input.expected_contract_hash,
        )
        object.__setattr__(bound, "expected_corpus_hash", "0" * 64)
        assert not is_bound_research_input(bound, revalidate_sources=False)
        with pytest.raises(ValueError, match="factory-bound"):
            BI5ResearchEngine(bound)


def test_c6_source_bytes_changed_after_binding_are_rejected() -> None:
    with synthetic_runtime_case() as case:
        bound = bind_execution_input(
            case.execution_input.corpus_root,
            case.execution_input.contract_path,
            case.execution_input.expected_corpus_hash,
            case.execution_input.expected_contract_hash,
        )
        case.contract_path.write_text(case.contract_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        assert not is_bound_research_input(bound)
        with pytest.raises(ValueError, match="factory-bound"):
            BI5ResearchEngine(bound)

    with synthetic_runtime_case() as case:
        bound = bind_execution_input(
            case.execution_input.corpus_root,
            case.execution_input.contract_path,
            case.execution_input.expected_corpus_hash,
            case.execution_input.expected_contract_hash,
        )
        bi5 = next(case.corpus_root.glob("*.bi5"))
        bi5.write_bytes(bi5.read_bytes() + b"forged")
        assert not is_bound_research_input(bound)
        with pytest.raises(ValueError, match="factory-bound"):
            BI5ResearchEngine(bound)


def test_c7_reconstructed_and_copied_execution_results_are_rejected() -> None:
    with synthetic_runtime_case() as case:
        for candidate in (copy.copy(case.result), copy.deepcopy(case.result)):
            assert candidate == case.result and candidate is not case.result
            assert not is_qualified_execution_result(candidate, case.execution_input)
            with pytest.raises(ValueError, match="identity-bound qualified execution result"):
                from_research_execution(
                    case.execution_input,
                    candidate,
                    code_version=CODE_VERSION,
                    context=case.context,
                    dataset=case.dataset,
                )


def test_c8_execution_result_cannot_be_rebound_to_different_input() -> None:
    with synthetic_runtime_case() as first, synthetic_runtime_case() as second:
        assert not is_qualified_execution_result(first.result, second.execution_input)
        with pytest.raises(ValueError, match="identity-bound qualified execution result"):
            from_research_execution(
                second.execution_input,
                first.result,
                code_version=CODE_VERSION,
                context=second.context,
                dataset=second.dataset,
            )


def test_c9_post_execution_result_mutation_invalidates_attestation() -> None:
    with synthetic_runtime_case() as case:
        object.__setattr__(case.result, "stream_sha256", "0" * 64)
        assert not is_qualified_execution_result(case.result, case.execution_input)
        with pytest.raises(ValueError, match="identity-bound qualified execution result"):
            from_research_execution(
                case.execution_input,
                case.result,
                code_version=CODE_VERSION,
                context=case.context,
                dataset=case.dataset,
            )


def test_c10_zero_file_and_zero_tick_executions_are_rejected(tmp_path: Path) -> None:
    no_files = _qualified_input(tmp_path / "no-files", write_empty_bi5=False)
    with pytest.raises(ValueError, match="at least one BI5 file"):
        run_qualified_research(no_files)

    zero_ticks = _qualified_input(tmp_path / "zero-ticks", write_empty_bi5=True)
    with pytest.raises(ValueError, match="at least one decoded tick"):
        run_qualified_research(zero_ticks)


def test_c11_foreign_dataset_identity_is_rejected() -> None:
    with synthetic_runtime_case() as case:
        foreign = replace(case.dataset, dataset_id="DATA-foreign")
        with pytest.raises(ValueError, match="dataset mismatch"):
            from_research_execution(
                case.execution_input,
                case.result,
                code_version=CODE_VERSION,
                context=case.context,
                dataset=foreign,
            )


def test_c12_foreign_context_configuration_and_bounds_are_rejected() -> None:
    with synthetic_runtime_case() as case:
        forged_config = replace(case.context, configuration_version="CFG-foreign")
        forged_bounds = replace(case.context, observation_end="2099-01-01T00:00:00+00:00")
        for foreign in (forged_config, forged_bounds):
            with pytest.raises(ValueError):
                from_research_execution(
                    case.execution_input,
                    case.result,
                    code_version=CODE_VERSION,
                    context=foreign,
                    dataset=case.dataset,
                )


def test_c13_malformed_code_version_is_rejected() -> None:
    with synthetic_runtime_case() as case:
        with pytest.raises(ValueError, match="40-hex commit"):
            from_research_execution(
                case.execution_input,
                case.result,
                code_version="not-a-commit",
                context=case.context,
                dataset=case.dataset,
            )


def test_c14_manual_evidence_reconstruction_after_valid_run_is_rejected() -> None:
    with synthetic_runtime_case() as case:
        evidence = case.evidence
        reconstructed = ResearchRunEvidence(
            provenance_id=evidence.provenance_id,
            research_run_id=evidence.research_run_id,
            code_version=evidence.code_version,
            configuration_version=evidence.configuration_version,
            dataset_id=evidence.dataset_id,
            dataset_version=evidence.dataset_version,
            context_id=evidence.context_id,
        )
        assert reconstructed == evidence and reconstructed is not evidence
        assert not is_factory_attested(reconstructed)
        with pytest.raises(ValueError, match="factory-attested"):
            produce_decision(reconstructed, context=case.context, decision="HOLD")


def test_c15_rejected_legacy_path_cannot_seed_research_findings() -> None:
    report, dataset, context = legacy_inputs()
    legacy = from_v43_report(report, code_version=CODE_VERSION, context=context, dataset=dataset)
    hypothesis = ResearchHypothesis("H1", "scope", "prediction", "falsifier")
    measurement = ResearchMeasurement("M1", "RUN", "EXP", "metric", 1.0, 1, "scope")
    finding = ResearchFinding("F1", "H1", "scope", ("M1",), "SUPPORTED", "rule", "reason")
    with pytest.raises(ValueError, match="factory-attested"):
        ResearchFindings.from_research_run_evidence(
            legacy,
            hypotheses=(hypothesis,),
            measurements=(measurement,),
            findings=(finding,),
        )
