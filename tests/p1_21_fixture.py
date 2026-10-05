"""P1-21 synthetic/non-empirical fixture.

Uses the canonical DATA-02 receipt and RVO-06 runtime observation as documentary
inputs only. It never opens the real AP0 corpus and never invokes AP1.
"""
from __future__ import annotations

import json
from pathlib import Path

from src import p1_12c_qualified_producer_execution as p12c
from tests.p1_18_fixture import build_case

ROOT = Path(__file__).resolve().parents[1]
DATA_RECEIPT = ROOT / "reports" / "program" / "2026-10-04-DATA-02-REAL-AP0-READ-ONLY-ADMISSION-RECEIPT-V0.1.json"
RUNTIME_EVIDENCE = ROOT / "GOVERNANCE" / "RVO-06-REAL-AP1-RUNTIME-LOCK-OBSERVATION-V0.1.json"
AP1 = ROOT / "tools" / "ap1_intraday_spread_census.py"
RUNNER = ROOT / "tools" / "p1_12c_sandbox_runner.py"


def build_real_capability_case(tmp_path: Path, *, suffix: str = "A"):
    legacy = build_case(tmp_path / "legacy")
    qualified_input = legacy["qualified_input"]

    data_binding = p12c.bind_real_data_owner_evidence(DATA_RECEIPT)
    invocation_profile = p12c.qualify_ap1_invocation_profile(AP1)
    runtime_evidence = json.loads(RUNTIME_EVIDENCE.read_text(encoding="utf-8"))
    runtime_lock = p12c.qualify_real_producer_runtime_lock(
        runtime_evidence,
        invocation_profile,
        runtime_evidence_source_ref=p12c.RVO06_RUNTIME_EVIDENCE_BLOB,
        timeout_seconds=3600,
        material_environment={
            "PYTHONHASHSEED": "0",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
    )
    plan = p12c.qualify_real_producer_execution_plan(
        qualified_input,
        data_binding,
        invocation_profile,
        runtime_lock,
        producer_path=AP1,
        ap0_root_transport=f"NON_EMPIRICAL_AP0_ROOT_{suffix}",
        ap0_manifest_transport=f"NON_EMPIRICAL_AP0_MANIFEST_{suffix}",
        output_transport=f"NON_EMPIRICAL_AP1_OUTPUT_{suffix}",
        expected_output_schema=p12c.AP1_OUTPUT_SCHEMA,
        expected_output_status=p12c.AP1_OUTPUT_STATUS,
        expected_output_contract="ATDS_AP1_CANONICAL_JSON_OUTPUT_V1",
        maximum_output_bytes=32 * 1024 * 1024,
        result_exposed=False,
    )
    return {
        "legacy": legacy,
        "qualified_input": qualified_input,
        "data_binding": data_binding,
        "invocation_profile": invocation_profile,
        "runtime_evidence": runtime_evidence,
        "runtime_lock": runtime_lock,
        "plan": plan,
    }
