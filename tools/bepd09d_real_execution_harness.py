from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import platform
import subprocess
import sys
import traceback
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "bepd09d-real-execution"
OUT.mkdir(parents=True, exist_ok=True)

LEDGER_PATH = ROOT / "artifacts" / "bepd02" / "real-historical-weekly-liquidity-ledger-v0.1" / "EVENT_LEDGER.jsonl"
PARTITION_PATH = ROOT / "GOVERNANCE" / "BEPD-09D0-FROZEN-CALENDAR-PARTITION-MANIFEST-V0.1.json"
PRIMARY_PATH = ROOT / "tools" / "bepd09c_runtime.py"
REFERENCE_PATH = ROOT / "tools" / "bepd09c_reference.py"

FLOAT_ATOL = 2e-5
STRUCT_ATOL = 1e-12

EXPECTED_BLOBS = {
    "GOVERNANCE/BEPD-09B-R1-FINAL-HUMAN-ADJUDICATION-CLOSURE-2026-10-07.md": "b104681e6cda77d726b72c62905ec1820f840553",
    "GOVERNANCE/BEPD-09C-FINAL-HUMAN-ADJUDICATION-CLOSURE-2026-10-07.md": "c643cad3093888fd9e88b84b3b3071a7a96ba6b8",
    "GOVERNANCE/BEPD-09D0-FINAL-HUMAN-ADJUDICATION-CLOSURE-2026-10-07.md": "d327b7d7f83221eec2030907b792e15dcde907dc",
    "GOVERNANCE/BEPD-09D0-REAL-INPUT-IDENTITY-MANIFEST-V0.1.json": "780dd4cfd518becf8a7127675feb42fbd75ffabd",
    "GOVERNANCE/BEPD-09D0-REAL-SCHEMA-RUNTIME-BINDING-CONTRACT-V0.1.json": "86a4319da6c2a1c946031a16765e1548178f3dda",
    "reports/program/2026-10-07-BEPD-09D0-CALENDAR-RECONCILIATION-RECEIPT-V0.1.json": "c59c990497191dd06279ffadec73b536637b9ccd",
    "GOVERNANCE/BEPD-09D0-FROZEN-CALENDAR-PARTITION-MANIFEST-V0.1.json": "7d950d957611cf209d811c788ff10abded30d011",
    "GOVERNANCE/BEPD-09D0-EXECUTION-ENVIRONMENT-MANIFEST-V0.1.json": "df1761a0aca7d77efe813f3f14580187f653fd27",
    "GOVERNANCE/BEPD-09D0-FIRST-RUN-EXECUTION-MANIFEST-V0.1.json": "81401f7748baa5ea994a9996b46d1f7b9382891f",
    "GOVERNANCE/BEPD-09D0-FROZEN-RESULT-SURFACE-SCHEMA-V0.1.json": "0991fd018818d4913148fbf144ba9d306b03bc45",
    "GOVERNANCE/BEPD-09D0-PRE-EXECUTION-BREAKER-CONTRACT-V0.1.json": "b7572f6f7163d4442bdbc9a73539e25a7c54b30f",
    "GOVERNANCE/BEPD-09D0-SINGLE-RUN-RETRY-POLICY-V0.1.json": "6f2a90c89e21fd6082bb2abbb4c1c1d553ba4b35",
    "reports/program/2026-10-07-BEPD-09D0-PRE-EXECUTION-READINESS-RECEIPT-V0.1.json": "d0c1954dac7df5ab16546858a2e530c7e05d1104",
    "reports/program/2026-10-07-BEPD-09D0-PERSISTED-HEAD-VERIFICATION-RECEIPT-V0.1.json": "f4ad76ad136c4e524c7ed5a2d669e487d6505cf2",
    "GOVERNANCE/BEPD-09C-IMPLEMENTATION-CONTRACT-V0.1.json": "d3c6a4c4d400a8766f58a63211af8d0655be61e6",
    "GOVERNANCE/BEPD-09C-EXECUTABLE-BREAKER-CONTRACT-V0.1.json": "00d6c9cb4a0fa62ea4fdf98917c3bccf72e6d494",
    "tools/bepd09c_runtime.py": "72645c3201d3d454d4d5402a0e2191e1195c68a6",
    "tools/bepd09c_reference.py": "2c8a82405082ce3f820b580017a96af77e74b0e4",
    "GOVERNANCE/BEPD-04E-COMPLETE-WEEK-CALENDAR-BINDING-V0.1.json": "26385eb2547892df4b87206ad59fc2ba07721354",
    "artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/RUN_MANIFEST.json": "ccd5e31e1aeeadb4cceee24a8b8cd5eb0f8cf6d5",
    "GOVERNANCE/BEPD-09D-HUMAN-AUTHORIZATION-2026-10-07.md": "4bf0bbafe1b4f614a6fa2eb29b32ce24b25a2782",
}

EXPECTED_LEDGER_BLOB = "0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2"
EXPECTED_LEDGER_SHA256 = "301a621b97fea14a72540d4c2c6da78eb742cc44c5009e44ad98e9f678ca4731"
EXPECTED_LEDGER_ROWS = 472

state = {
    "real_read_started": False,
    "primary_executed": False,
    "reference_executed": False,
    "result_exposed": False,
    "parity_assessable": False,
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def tracked_blob(path: str) -> str:
    line = git("ls-tree", "HEAD", "--", path)
    if not line:
        raise RuntimeError("MISSING_TRACKED_PATH:" + path)
    return line.split()[2]


def write_json(name: str, payload: dict) -> None:
    (OUT / name).write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def failure(stage: str, error: str) -> None:
    write_json(
        "10_FAILURE_RECEIPT.json",
        {
            "schema": "ATDS_BEPD_09D_FAILURE_RECEIPT_V0_1",
            "status": "STOPPED_FAIL_CLOSED",
            "failure_point": stage,
            "error": error,
            "real_read_started": state["real_read_started"],
            "whether_any_real_result_was_exposed": state["result_exposed"],
            "whether_primary_executed": state["primary_executed"],
            "whether_reference_executed": state["reference_executed"],
            "whether_parity_was_assessable": state["parity_assessable"],
            "discretionary_rerun_authorized": False,
            "trading_authority": "NONE",
        },
    )
    raise SystemExit(2)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("MODULE_LOAD_FAILURE:" + name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def mean(values):
    values = list(values)
    if not values:
        raise RuntimeError("EMPTY_METRIC_COLLECTION")
    return sum(values) / len(values)


def fold_metrics(fold: dict) -> dict:
    weekly = fold["weekly"]
    vals = list(weekly.values())
    bl = mean(v["baseline_logloss"] for v in vals)
    cl = mean(v["context_logloss"] for v in vals)
    bb = mean(v["baseline_brier"] for v in vals)
    cb = mean(v["context_brier"] for v in vals)
    return {
        "fold": fold["fold"],
        "train_event_count": fold["train_event_count"],
        "test_event_count": fold["test_event_count"],
        "train_response_class_counts": fold["train_response_class_counts"],
        "convergence_status": fold["convergence_status"],
        "baseline_logloss": bl,
        "context_logloss": cl,
        "logloss_delta": bl - cl,
        "baseline_brier": bb,
        "context_brier": cb,
        "brier_delta": bb - cb,
    }


def public_surface(result: dict, parity_status: str) -> dict:
    blocks = []
    for idx, block in enumerate(result["blocks"], start=1):
        blocks.append(
            {
                "block": "B" + str(idx),
                "week_count": len(block),
                "first_week": block[0],
                "last_week": block[-1],
            }
        )
    agg = result["aggregate"]
    return {
        "source_identity_checks": "PASS",
        "admissibility_status": "PASS",
        "calendar_block_boundaries": blocks,
        "folds": [fold_metrics(f) for f in result["folds"]],
        "aggregate_week_balanced_logloss": {
            "baseline": agg["baseline_week_balanced_logloss"],
            "context": agg["context_week_balanced_logloss"],
        },
        "primary_delta": agg["primary_logloss_improvement_delta"],
        "aggregate_week_balanced_brier": {
            "baseline": agg["baseline_week_balanced_brier"],
            "context": agg["context_week_balanced_brier"],
        },
        "secondary_delta": agg["secondary_brier_improvement_delta"],
        "event_weighted_diagnostics": {
            "baseline_logloss": agg["event_weighted_baseline_logloss"],
            "context_logloss": agg["event_weighted_context_logloss"],
            "baseline_brier": agg["event_weighted_baseline_brier"],
            "context_brier": agg["event_weighted_context_brier"],
        },
        "primary_reference_parity_status": parity_status,
        "deterministic_execution_identity": result["deterministic_replay_identity"],
        "breaker_status": "PASS",
        "evidence_class": "EXPLORATORY_ONLY",
        "automatic_scientific_verdict": "NONE_HUMAN_ADJUDICATION_REQUIRED",
        "trading_authority": "NONE",
    }


def numeric_max_diff(a, b) -> float:
    import numpy as np
    aa = np.asarray(a, dtype=float)
    bb = np.asarray(b, dtype=float)
    if aa.shape != bb.shape:
        raise RuntimeError("NUMERIC_SHAPE_MISMATCH")
    if aa.size == 0:
        return 0.0
    return float(np.max(np.abs(aa - bb)))


def assess_parity(primary: dict, reference: dict, prep_primary: list, prep_reference: list) -> dict:
    if primary["blocks"] != reference["blocks"]:
        raise RuntimeError("PRIMARY_REFERENCE_BLOCK_DIVERGENCE")
    if len(primary["folds"]) != len(reference["folds"]):
        raise RuntimeError("PRIMARY_REFERENCE_FOLD_COUNT_DIVERGENCE")
    if len(prep_primary) != len(prep_reference):
        raise RuntimeError("PRIMARY_REFERENCE_PREP_COUNT_DIVERGENCE")

    max_exposure = 0.0
    max_basis = 0.0
    for a, b in zip(prep_primary, prep_reference):
        if a["event_id"] != b["event_id"] or a["target_week_id"] != b["target_week_id"]:
            raise RuntimeError("PRIMARY_REFERENCE_PREP_IDENTITY_DIVERGENCE")
        max_exposure = max(max_exposure, abs(float(a["exposure_fraction"]) - float(b["exposure"])))
        max_basis = max(max_basis, numeric_max_diff(a["basis"], b["basis"]))

    max_standardization = 0.0
    max_design = 0.0
    max_probability = 0.0
    max_weekly = 0.0

    for a, b in zip(primary["folds"], reference["folds"]):
        if a["fold"] != b["fold"] or a["train_weeks"] != b["train_weeks"] or a["test_weeks"] != b["test_weeks"]:
            raise RuntimeError("PRIMARY_REFERENCE_FOLD_STRUCTURE_DIVERGENCE")
        if a["train_event_count"] != b["train_event_count"] or a["test_event_count"] != b["test_event_count"]:
            raise RuntimeError("PRIMARY_REFERENCE_EVENT_COUNT_DIVERGENCE")
        if a["train_response_class_counts"] != b["train_response_class_counts"]:
            raise RuntimeError("PRIMARY_REFERENCE_CLASS_COUNT_DIVERGENCE")

        for key in ("age", "active", "overshoot"):
            max_standardization = max(
                max_standardization,
                abs(float(a["standardization"][key]["mean"]) - float(b["standardization"][key]["mean"])),
                abs(float(a["standardization"][key]["sample_sd"]) - float(b["standardization"][key]["sample_sd"])),
            )

        max_design = max(
            max_design,
            numeric_max_diff(a["baseline_design"], b["baseline_design"]),
            numeric_max_diff(a["context_design"], b["context_design"]),
        )
        max_probability = max(
            max_probability,
            numeric_max_diff(a["baseline_probabilities"], b["baseline_probabilities"]),
            numeric_max_diff(a["context_probabilities"], b["context_probabilities"]),
        )

        if set(a["weekly"]) != set(b["weekly"]):
            raise RuntimeError("PRIMARY_REFERENCE_WEEKLY_KEY_DIVERGENCE")
        for week in a["weekly"]:
            for metric in ("baseline_logloss", "context_logloss", "baseline_brier", "context_brier"):
                max_weekly = max(
                    max_weekly,
                    abs(float(a["weekly"][week][metric]) - float(b["weekly"][week][metric])),
                )

    if set(primary["aggregate"]) != set(reference["aggregate"]):
        raise RuntimeError("PRIMARY_REFERENCE_AGGREGATE_KEY_DIVERGENCE")
    max_aggregate = max(
        abs(float(primary["aggregate"][key]) - float(reference["aggregate"][key]))
        for key in primary["aggregate"]
    )

    status = (
        "PASS"
        if max_exposure <= STRUCT_ATOL
        and max_basis <= STRUCT_ATOL
        and max_standardization <= STRUCT_ATOL
        and max_design <= STRUCT_ATOL
        and max_probability <= FLOAT_ATOL
        and max_weekly <= FLOAT_ATOL
        and max_aggregate <= FLOAT_ATOL
        else "FAIL"
    )

    return {
        "status": status,
        "floating_absolute_tolerance": FLOAT_ATOL,
        "structural_design_matrix_absolute_tolerance": STRUCT_ATOL,
        "max_exposure_fraction_abs_difference": max_exposure,
        "max_spline_basis_abs_difference": max_basis,
        "max_standardization_abs_difference": max_standardization,
        "max_design_matrix_abs_difference": max_design,
        "max_probability_abs_difference": max_probability,
        "max_weekly_metric_abs_difference": max_weekly,
        "max_aggregate_metric_abs_difference": max_aggregate,
    }


try:
    if os.environ.get("GITHUB_REPOSITORY") != "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM":
        failure("PREFLIGHT_REPOSITORY", "REPOSITORY_IDENTITY_MISMATCH")
    if os.environ.get("GITHUB_REF_NAME") != "integration/system-v1":
        failure("PREFLIGHT_BRANCH", "BRANCH_IDENTITY_MISMATCH")

    local_head = git("rev-parse", "HEAD")
    subprocess.check_call(["git", "fetch", "origin", "integration/system-v1", "--quiet"], cwd=ROOT)
    remote_head = git("rev-parse", "origin/integration/system-v1")
    concurrent_files = []
    drift_class = "NONE"
    if remote_head != local_head:
        raw_changed = git("diff", "--name-only", local_head + ".." + remote_head)
        concurrent_files = [x for x in raw_changed.splitlines() if x]
        material = any(("BEPD" in x or "bepd" in x) for x in concurrent_files)
        drift_class = "MATERIAL_TO_BEPD_09D" if material else "NON_MATERIAL_TO_BEPD_09D"
        if material:
            failure("PREFLIGHT_CONCURRENT_DRIFT", "MATERIAL_CONCURRENT_BEPD_DRIFT")

    identity_observed = {}
    for path, expected in EXPECTED_BLOBS.items():
        observed = tracked_blob(path)
        identity_observed[path] = {"expected": expected, "observed": observed, "status": "PASS" if observed == expected else "FAIL"}
        if observed != expected:
            failure("PREFLIGHT_IDENTITY", "IDENTITY_MISMATCH:" + path)

    ledger_blob = tracked_blob(str(LEDGER_PATH.relative_to(ROOT)))
    if ledger_blob != EXPECTED_LEDGER_BLOB:
        failure("PREFLIGHT_LEDGER_BLOB", "EVENT_LEDGER_GIT_BLOB_MISMATCH")

    harness_blob = tracked_blob("tools/bepd09d_real_execution_harness.py")
    workflow_blob = tracked_blob(".github/workflows/bepd-09d-real-execution.yml")

    write_json(
        "01_FRESH_REAL_EXECUTION_PREFLIGHT_RECEIPT.json",
        {
            "schema": "ATDS_BEPD_09D_FRESH_REAL_EXECUTION_PREFLIGHT_RECEIPT_V0_1",
            "status": "PASS",
            "repository": os.environ.get("GITHUB_REPOSITORY"),
            "branch": os.environ.get("GITHUB_REF_NAME"),
            "execution_commit": local_head,
            "remote_branch_head_observed": remote_head,
            "concurrent_drift_classification": drift_class,
            "concurrent_drift_files": concurrent_files,
            "frozen_identity_checks": identity_observed,
            "event_ledger_git_blob": ledger_blob,
            "execution_harness_blob": harness_blob,
            "workflow_blob": workflow_blob,
            "real_data_read_at_receipt_creation": False,
        },
    )

    import numpy as np
    import scipy

    env_ok = (
        platform.python_version().startswith("3.12.")
        and np.__version__ == "2.3.5"
        and scipy.__version__ == "1.17.0"
        and ZoneInfo("America/New_York").key == "America/New_York"
    )
    if not env_ok:
        failure("ENVIRONMENT_GATE", "ENVIRONMENT_REQUIREMENT_MISMATCH")

    write_json(
        "02_REAL_EXECUTION_ENVIRONMENT_RECEIPT.json",
        {
            "schema": "ATDS_BEPD_09D_REAL_EXECUTION_ENVIRONMENT_RECEIPT_V0_1",
            "status": "PASS",
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "zoneinfo_key": ZoneInfo("America/New_York").key,
            "floating_absolute_tolerance": FLOAT_ATOL,
            "structural_design_matrix_absolute_tolerance": STRUCT_ATOL,
            "real_data_read_at_receipt_creation": False,
        },
    )

    state["real_read_started"] = True
    raw_ledger = LEDGER_PATH.read_bytes()
    ledger_sha256 = hashlib.sha256(raw_ledger).hexdigest()
    if ledger_sha256 != EXPECTED_LEDGER_SHA256:
        failure("REAL_SOURCE_SHA256", "DECLARED_EVENT_LEDGER_SHA256_MISMATCH")

    text_ledger = raw_ledger.decode("utf-8")
    rows = [json.loads(line) for line in text_ledger.splitlines() if line.strip()]
    if len(rows) != EXPECTED_LEDGER_ROWS:
        failure("REAL_SOURCE_ROW_COUNT", "EVENT_LEDGER_ROW_COUNT_MISMATCH")

    write_json(
        "03_REAL_SOURCE_IDENTITY_RECEIPT.json",
        {
            "schema": "ATDS_BEPD_09D_REAL_SOURCE_IDENTITY_RECEIPT_V0_1",
            "status": "PASS",
            "path": str(LEDGER_PATH.relative_to(ROOT)),
            "git_blob": ledger_blob,
            "sha256": ledger_sha256,
            "row_count": len(rows),
            "declared_size_bytes": len(raw_ledger),
            "evidence_class": "EXPLORATORY_ONLY",
        },
    )

    partition = json.loads(PARTITION_PATH.read_text(encoding="utf-8"))
    calendar = [week for block in partition["blocks"] for week in block["weeks"]]
    if len(calendar) != 259 or calendar[0] != "2021-06-07" or calendar[-1] != "2026-05-18":
        failure("CALENDAR_GATE", "FOLD_MANIFEST_MISMATCH")
    if [len(block["weeks"]) for block in partition["blocks"]] != [44, 43, 43, 43, 43, 43]:
        failure("CALENDAR_GATE", "FOLD_MANIFEST_MISMATCH")

    primary_module = load_module("bepd09d_primary", PRIMARY_PATH)
    reference_module = load_module("bepd09d_reference", REFERENCE_PATH)

    prep_primary = primary_module.validate_rows(rows, calendar)
    prep_reference = reference_module._prep(rows, calendar)

    state["primary_executed"] = True
    primary = primary_module.run_protocol(rows, calendar)
    state["result_exposed"] = True
    write_json("04_PRIMARY_REAL_RESULT.json", public_surface(primary, "NOT_YET_ASSESSED"))

    state["reference_executed"] = True
    reference = reference_module.run_reference(rows, calendar)
    write_json("05_INDEPENDENT_REFERENCE_REAL_RESULT.json", public_surface(reference, "NOT_YET_ASSESSED"))

    state["parity_assessable"] = True
    parity = assess_parity(primary, reference, prep_primary, prep_reference)
    write_json(
        "06_PRIMARY_REFERENCE_PARITY_RECEIPT.json",
        {
            "schema": "ATDS_BEPD_09D_PRIMARY_REFERENCE_PARITY_RECEIPT_V0_1",
            **parity,
            "primary_execution_identity": primary["deterministic_replay_identity"],
            "reference_execution_identity": reference["deterministic_replay_identity"],
        },
    )

    write_json("04_PRIMARY_REAL_RESULT.json", public_surface(primary, parity["status"]))
    write_json("05_INDEPENDENT_REFERENCE_REAL_RESULT.json", public_surface(reference, parity["status"]))

    if parity["status"] != "PASS":
        failure("PRIMARY_REFERENCE_PARITY", "PARITY_FAILURE")

    execution_receipt = {
        "schema": "ATDS_BEPD_09D_REAL_EXECUTION_RECEIPT_V0_1",
        "status": "REAL_HISTORICAL_EXPLORATORY_C1_EXECUTION_COMPLETED",
        "execution_pair_count": 1,
        "primary_run_count": 1,
        "reference_run_count": 1,
        "same_frozen_input": True,
        "real_row_count": len(rows),
        "calendar_week_count": len(calendar),
        "partition_counts": [44, 43, 43, 43, 43, 43],
        "evidence_class": "EXPLORATORY_ONLY",
        "primary_reference_parity": "PASS",
        "discretionary_rerun_authorized": False,
        "fresh_oos": "CLOSED",
        "automatic_scientific_verdict": "NONE",
        "trading_authority": "NONE",
    }
    write_json("07_REAL_EXECUTION_RECEIPT.json", execution_receipt)

    write_json(
        "08_TECHNICAL_QUALIFICATION_RECEIPT.json",
        {
            "schema": "ATDS_BEPD_09D_TECHNICAL_QUALIFICATION_RECEIPT_V0_1",
            "status": "PASS",
            "verdict": "REAL_HISTORICAL_EXPLORATORY_C1_EXECUTION_COMPLETED_AND_TECHNICALLY_QUALIFIED_FOR_HUMAN_ADJUDICATION",
            "source_identity": "PASS",
            "environment": "PASS",
            "admissibility": "PASS",
            "primary_run": "COMPLETED",
            "reference_run": "COMPLETED",
            "primary_reference_parity": "PASS",
            "result_surface": "FROZEN_ONLY",
            "evidence_class": "EXPLORATORY_ONLY",
            "c1_automatic_adoption": False,
            "c1_automatic_rejection": False,
            "generalization_established": False,
            "edge_established": False,
            "strategy_validated": False,
            "fresh_oos": "CLOSED",
            "trading_authority": "NONE",
            "next": "HUMAN_ADJUDICATION_OF_FIRST_REAL_BEPD_09D_C1_RESULT",
            "stop": True,
        },
    )

    print("BEPD-09D REAL EXECUTION PAIR COMPLETED; TECHNICAL QUALIFICATION PASS; STOP FOR HUMAN ADJUDICATION")

except SystemExit:
    raise
except Exception as exc:
    failure("UNHANDLED_EXECUTION_EXCEPTION", type(exc).__name__ + ":" + str(exc) + "\n" + traceback.format_exc())
