"""Synthetic P1-18 qualification fixtures. No real AP0/AP1 data is read."""

from __future__ import annotations

import json
from pathlib import Path

from src import p1_12c_qualified_producer_execution as p12c
from src.data import claim_scoped_admission as data02
from src.experiment_execution_binding import bind_experiment_execution
from src.qualified_experiment_execution_input import qualify_experiment_execution_input
from src.research.input_binding import bind_execution_input, corpus_inventory_hash, sha256_file
from tests.data_02_fixture import make_package as make_data02_package
from tests.rvo_05_fixture import make_p1_spec

ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC_PRODUCER = ROOT / "tests" / "p1_18_synthetic_producer.py"
PRODUCER_ID = "ATDS_P1_18_SYNTHETIC_PRODUCER_V0_1"
OUTPUT_SCHEMA = "ATDS_P1_18_SYNTHETIC_PRODUCER_OUTPUT_V0_1"
OUTPUT_STATUS = "SYNTHETIC_COMPLETE"
OUTPUT_CONTRACT = "P1_18_SYNTHETIC_BYTE_INVENTORY_RESULT_V0_1"


def build_case(tmp_path: Path, *, mode: str = "normal", producer_path: Path | None = None):
    package = make_data02_package(tmp_path / "data")
    admission = data02.evaluate_synthetic(package)
    assert admission["status"] == "READY_FOR_EXACT_CLAIM"

    specification = make_p1_spec(tmp_path / "spec", tag="P118")
    contract_path = tmp_path / "p1-18-resource-contract.json"
    contract_path.write_text(
        json.dumps(
            {
                "format": "SYNTHETIC_DATA02_BYTE_FIXTURE",
                "scope": "P1-18-only",
                "real_market_data": False,
                "oos": False,
            },
            sort_keys=True,
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )
    root = Path(package["root"])
    bound = bind_execution_input(
        root,
        contract_path,
        corpus_inventory_hash(root),
        sha256_file(contract_path),
    )
    execution_binding = bind_experiment_execution(specification, bound)
    qualified_input = qualify_experiment_execution_input(execution_binding)

    chosen = producer_path or SYNTHETIC_PRODUCER
    plan = p12c.qualify_producer_execution_plan(
        qualified_input,
        admission,
        producer_id=PRODUCER_ID,
        producer_path=chosen,
        semantic_parameters={
            "mode": mode,
            "qualification_scope": "P1-18-SYNTHETIC-ONLY",
            "market_semantics": "NONE",
        },
        expected_output_schema=OUTPUT_SCHEMA,
        expected_output_status=OUTPUT_STATUS,
        expected_output_contract=OUTPUT_CONTRACT,
        maximum_output_bytes=1024 * 1024,
        result_exposed=False,
        temporal_scope="RETROSPECTIVE_DESCRIPTIVE_ONLY",
        oos_consumption=False,
    )
    return {
        "package": package,
        "admission": admission,
        "specification": specification,
        "execution_binding": execution_binding,
        "qualified_input": qualified_input,
        "plan": plan,
        "producer_path": chosen,
    }
