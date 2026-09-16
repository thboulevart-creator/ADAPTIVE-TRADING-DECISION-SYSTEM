from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

import pytest

from src.decision import produce_decision
from src.research.execution import QualifiedResearchInput
from src.research_interprocess import (
    persist_research_execution_proof,
    reattest_persisted_research_execution,
)
from src.research_run_evidence import (
    ResearchRunEvidence,
    from_v43_report,
    is_factory_attested,
)
from tests.research_runtime_fixture import CODE_VERSION, synthetic_runtime_case
from tests.test_research_producer_junction_tier_a import legacy_inputs


def _canonical(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        + b"\n"
    )


def _load_document(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_rehashed(directory: Path, document: dict) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    updated = copy.deepcopy(document)
    payload = dict(updated)
    payload.pop("proof_sha256", None)
    digest = hashlib.sha256(_canonical(payload)).hexdigest()
    updated["proof_sha256"] = digest
    path = directory / f"research-proof-{digest}.json"
    path.write_bytes(_canonical(updated))
    return path


def _persist_case(case) -> Path:
    return persist_research_execution_proof(
        case.root / "proofs",
        case.execution_input,
        case.result,
        case.evidence,
        dataset=case.dataset,
        context=case.context,
    )


def test_d0_producer_proof_fresh_process_replay_attestation_and_decision() -> None:
    with synthetic_runtime_case() as case:
        proof = _persist_case(case)
        document = _load_document(proof)
        assert proof.name == f"research-proof-{document['proof_sha256']}.json"
        assert _persist_case(case) == proof

        script = r"""
import sys
from pathlib import Path
from src.decision import produce_decision
from src.research.execution import QualifiedResearchInput
from src.research_interprocess import reattest_persisted_research_execution
from src.research_run_evidence import is_factory_attested
execution_input = QualifiedResearchInput(
    corpus_root=Path(sys.argv[2]),
    contract_path=Path(sys.argv[3]),
    expected_corpus_hash=sys.argv[4],
    expected_contract_hash=sys.argv[5],
)
bundle = reattest_persisted_research_execution(
    Path(sys.argv[1]), execution_input, expected_code_version=sys.argv[6]
)
assert is_factory_attested(bundle.evidence)
decision = produce_decision(bundle.evidence, context=bundle.context, decision='HOLD')
assert decision.research_run_id == bundle.evidence.research_run_id
print('PASS: fresh process replay minted new local attestation and DECISION accepted it')
"""
        completed = subprocess.run(
            [
                sys.executable,
                "-c",
                script,
                str(proof),
                str(case.corpus_root),
                str(case.contract_path),
                case.execution_input.expected_corpus_hash,
                case.execution_input.expected_contract_hash,
                CODE_VERSION,
            ],
            cwd=Path(__file__).resolve().parents[1],
            text=True,
            capture_output=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
        assert "PASS:" in completed.stdout


def test_d1_raw_deserialized_evidence_is_unattested_in_fresh_process() -> None:
    with synthetic_runtime_case() as case:
        proof = _persist_case(case)
        script = r"""
import json
import sys
from src.research_run_evidence import ResearchRunEvidence, is_factory_attested
document = json.load(open(sys.argv[1], 'r', encoding='utf-8'))
raw = ResearchRunEvidence(**document['evidence'])
assert not is_factory_attested(raw)
print('PASS: raw persisted evidence fields are non-authorizing')
"""
        completed = subprocess.run(
            [sys.executable, "-c", script, str(proof)],
            cwd=Path(__file__).resolve().parents[1],
            text=True,
            capture_output=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr


def test_d2_evidence_tamper_with_recomputed_digest_is_rejected() -> None:
    with synthetic_runtime_case() as case:
        proof = _persist_case(case)
        document = _load_document(proof)
        document["evidence"]["research_run_id"] = "RUN-forged-but-rehashed"
        forged = _write_rehashed(case.root / "forged-evidence", document)
        with pytest.raises(ValueError, match="replay evidence differs"):
            reattest_persisted_research_execution(
                forged, case.execution_input, expected_code_version=CODE_VERSION
            )


def test_d3_valid_shaped_foreign_code_version_is_rejected() -> None:
    with synthetic_runtime_case() as case:
        proof = _persist_case(case)
        document = _load_document(proof)
        foreign = "f" * 40
        assert foreign != CODE_VERSION
        document["code_version"] = foreign
        document["evidence"]["code_version"] = foreign
        forged = _write_rehashed(case.root / "forged-code", document)
        with pytest.raises(ValueError, match="trusted expected_code_version"):
            reattest_persisted_research_execution(
                forged, case.execution_input, expected_code_version=CODE_VERSION
            )


def test_d4_execution_claim_tamper_with_recomputed_digest_is_rejected() -> None:
    with synthetic_runtime_case() as case:
        proof = _persist_case(case)
        document = _load_document(proof)
        document["execution"]["stream_sha256"] = "0" * 64
        forged = _write_rehashed(case.root / "forged-execution", document)
        with pytest.raises(ValueError, match="replay result differs"):
            reattest_persisted_research_execution(
                forged, case.execution_input, expected_code_version=CODE_VERSION
            )


def test_d5_dataset_tamper_with_recomputed_digest_is_rejected() -> None:
    with synthetic_runtime_case() as case:
        proof = _persist_case(case)
        document = _load_document(proof)
        document["dataset"]["dataset_id"] = "DATA-forged"
        forged = _write_rehashed(case.root / "forged-dataset", document)
        with pytest.raises(ValueError, match="replay dataset differs"):
            reattest_persisted_research_execution(
                forged, case.execution_input, expected_code_version=CODE_VERSION
            )


def test_d6_context_tamper_with_recomputed_digest_is_rejected() -> None:
    with synthetic_runtime_case() as case:
        proof = _persist_case(case)
        document = _load_document(proof)
        document["context"]["context_id"] = "CTX-forged"
        forged = _write_rehashed(case.root / "forged-context", document)
        with pytest.raises(ValueError, match="replay context differs"):
            reattest_persisted_research_execution(
                forged, case.execution_input, expected_code_version=CODE_VERSION
            )


def test_d7_corpus_bytes_substituted_after_persistence_are_rejected() -> None:
    with synthetic_runtime_case() as case:
        proof = _persist_case(case)
        bi5 = next(case.corpus_root.glob("*.bi5"))
        bi5.write_bytes(bi5.read_bytes() + b"forged")
        with pytest.raises(ValueError, match="Research corpus identity mismatch"):
            reattest_persisted_research_execution(
                proof, case.execution_input, expected_code_version=CODE_VERSION
            )


def test_d8_contract_bytes_substituted_after_persistence_are_rejected() -> None:
    with synthetic_runtime_case() as case:
        proof = _persist_case(case)
        case.contract_path.write_text(
            case.contract_path.read_text(encoding="utf-8") + "\n", encoding="utf-8"
        )
        with pytest.raises(ValueError, match="Instrument contract identity mismatch"):
            reattest_persisted_research_execution(
                proof, case.execution_input, expected_code_version=CODE_VERSION
            )


def test_d9_proof_rename_breaks_content_address_identity() -> None:
    with synthetic_runtime_case() as case:
        proof = _persist_case(case)
        renamed = case.root / f"research-proof-{'0' * 64}.json"
        renamed.write_bytes(proof.read_bytes())
        with pytest.raises(ValueError, match="filename/content identity mismatch"):
            reattest_persisted_research_execution(
                renamed, case.execution_input, expected_code_version=CODE_VERSION
            )


def test_d10_schema_missing_unknown_duplicate_and_substitution_fail_closed() -> None:
    with synthetic_runtime_case() as case:
        proof = _persist_case(case)
        original = _load_document(proof)

        missing = copy.deepcopy(original)
        missing.pop("evidence")
        missing_path = _write_rehashed(case.root / "missing", missing)
        with pytest.raises(ValueError, match="schema mismatch"):
            reattest_persisted_research_execution(
                missing_path, case.execution_input, expected_code_version=CODE_VERSION
            )

        unknown = copy.deepcopy(original)
        unknown["trust_me"] = True
        unknown_path = _write_rehashed(case.root / "unknown", unknown)
        with pytest.raises(ValueError, match="schema mismatch"):
            reattest_persisted_research_execution(
                unknown_path, case.execution_input, expected_code_version=CODE_VERSION
            )

        substituted = copy.deepcopy(original)
        substituted["schema"] = "FORGED_SCHEMA_V999"
        substituted_path = _write_rehashed(case.root / "schema", substituted)
        with pytest.raises(ValueError, match="unsupported inter-process proof schema"):
            reattest_persisted_research_execution(
                substituted_path, case.execution_input, expected_code_version=CODE_VERSION
            )

        duplicate = case.root / f"research-proof-{'0' * 64}.json"
        duplicate.write_text('{"schema":"A","schema":"B"}\n', encoding="utf-8")
        with pytest.raises(ValueError, match="duplicate JSON key"):
            reattest_persisted_research_execution(
                duplicate, case.execution_input, expected_code_version=CODE_VERSION
            )


def test_d11_legacy_report_only_evidence_cannot_be_persisted() -> None:
    report, legacy_dataset, legacy_context = legacy_inputs()
    legacy = from_v43_report(
        report,
        code_version=CODE_VERSION,
        context=legacy_context,
        dataset=legacy_dataset,
    )
    assert not is_factory_attested(legacy)
    with synthetic_runtime_case() as case:
        with pytest.raises(ValueError, match="factory-attested"):
            persist_research_execution_proof(
                case.root / "proofs",
                case.execution_input,
                case.result,
                legacy,
                dataset=case.dataset,
                context=case.context,
            )


def test_d12_copied_reconstructed_and_mutated_evidence_cannot_be_persisted() -> None:
    with synthetic_runtime_case() as case:
        reconstructed = ResearchRunEvidence(**asdict(case.evidence))
        for candidate in (copy.copy(case.evidence), copy.deepcopy(case.evidence), reconstructed):
            assert not is_factory_attested(candidate)
            with pytest.raises(ValueError, match="factory-attested"):
                persist_research_execution_proof(
                    case.root / "proofs",
                    case.execution_input,
                    case.result,
                    candidate,
                    dataset=case.dataset,
                    context=case.context,
                )

    with synthetic_runtime_case() as case:
        object.__setattr__(case.evidence, "research_run_id", "RUN-mutated")
        assert not is_factory_attested(case.evidence)
        with pytest.raises(ValueError, match="factory-attested"):
            persist_research_execution_proof(
                case.root / "proofs",
                case.execution_input,
                case.result,
                case.evidence,
                dataset=case.dataset,
                context=case.context,
            )


def test_d13_byte_identical_sources_can_relocate_without_identity_drift() -> None:
    with synthetic_runtime_case() as case:
        proof = _persist_case(case)
        relocated = case.root / "relocated"
        relocated.mkdir(parents=True, exist_ok=True)
        relocated_corpus = relocated / "corpus"
        relocated_contract = relocated / "contract.json"
        shutil.copytree(case.corpus_root, relocated_corpus)
        shutil.copy2(case.contract_path, relocated_contract)
        relocated_input = QualifiedResearchInput(
            corpus_root=relocated_corpus,
            contract_path=relocated_contract,
            expected_corpus_hash=case.execution_input.expected_corpus_hash,
            expected_contract_hash=case.execution_input.expected_contract_hash,
        )
        bundle = reattest_persisted_research_execution(
            proof, relocated_input, expected_code_version=CODE_VERSION
        )
        assert is_factory_attested(bundle.evidence)
        assert bundle.evidence == case.evidence


def test_d14_only_fresh_replay_object_is_authoritative() -> None:
    with synthetic_runtime_case() as case:
        proof = _persist_case(case)
        document = _load_document(proof)
        raw = ResearchRunEvidence(**document["evidence"])
        assert not is_factory_attested(raw)
        with pytest.raises(ValueError, match="factory-attested"):
            produce_decision(raw, context=case.context, decision="HOLD")

        bundle = reattest_persisted_research_execution(
            proof, case.execution_input, expected_code_version=CODE_VERSION
        )
        assert bundle.evidence is not raw
        assert bundle.evidence == raw
        assert is_factory_attested(bundle.evidence)
        decision = produce_decision(bundle.evidence, context=bundle.context, decision="HOLD")
        assert decision.research_run_id == bundle.evidence.research_run_id
