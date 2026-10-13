"""Print observed synthetic RED case evidence to stdout; no writes/workers."""
from __future__ import annotations
from pathlib import Path
import importlib.util
import json
import hashlib

HERE=Path(__file__).resolve().parent
ORACLE=HERE/"red_r1_cr2_oracle.py"
spec=importlib.util.spec_from_file_location("r1cr1redr1cr2oracle",ORACLE)
oracle=importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)
data={
  "schema":"ATDS_R1_CR1_RED_R1_CR2_SYNTHETIC_CASE_MATRIX_V0_1",
  "control_id":"AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-RED-R1-CR2",
  "evidence_class":"LEGACY_ADAPTER",
  "input_class":"SYNTHETIC_CONTRACT",
  "independent_windows_evidence":False,
  "green_implementation":False,
  "oracle_sha256":hashlib.sha256(ORACLE.read_bytes()).hexdigest(),
  "frozen_sources":oracle.verify_frozen_sources(),
  "test_cases":oracle.matrix_observations(),
}
assert len(data["test_cases"])==12
assert len({case["test_id"] for case in data["test_cases"]})==12
assert sum(case["observed_legacy_status"]=="PASS" for case in data["test_cases"])==5
assert sum(case["observed_legacy_status"]=="BLOCKED" for case in data["test_cases"])==7
print(json.dumps(data,sort_keys=True,indent=2,ensure_ascii=False))
