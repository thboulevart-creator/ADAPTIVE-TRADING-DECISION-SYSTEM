from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

import src.research_run_evidence as evidence_module
from tests.research_runtime_fixture import synthetic_runtime_case


def test_pre_p05_d0_durable_replay_bridge_must_exist() -> None:
    assert hasattr(evidence_module, "persist_research_execution_proof"), (
        "P0.5 requires a content-addressed durable proof writer"
    )
    assert hasattr(evidence_module, "reattest_persisted_research_execution"), (
        "P0.5 requires fresh-process deterministic replay re-attestation"
    )


def test_pre_p05_d1_raw_serialized_evidence_does_not_keep_attestation(tmp_path: Path) -> None:
    with synthetic_runtime_case() as case:
        payload = asdict(case.evidence)
    payload_path = tmp_path / "raw-evidence.json"
    payload_path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")

    script = """
import json
import sys
from src.research_run_evidence import ResearchRunEvidence, is_factory_attested
payload = json.load(open(sys.argv[1], 'r', encoding='utf-8'))
evidence = ResearchRunEvidence(**payload)
assert not is_factory_attested(evidence)
print('PASS: raw serialized ResearchRunEvidence is not authoritative in a fresh process')
"""
    completed = subprocess.run(
        [sys.executable, "-c", script, str(payload_path)],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "PASS:" in completed.stdout
