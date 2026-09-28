from __future__ import annotations

import copy
import hashlib
import json
import re

CONTRACT = "ATDS_E1_07_PREFLIGHT_REPRODUCIBILITY_TRACE_V0_1"
PREFLIGHT_SCHEMA_ID = "E1_PREFLIGHT_MANIFEST_V0"
RESULT_SCHEMA_ID = "E1_RESULT_ENVELOPE_SCHEMA_V0"
PREFLIGHT_SCHEMA_CANONICAL_SHA256 = "dfef55de3b29f165d60fac5c814be4bd81d0c3674768a3775f4fc6c532e8a99d"
RESULT_SCHEMA_CANONICAL_SHA256 = "d3da7e97b533ce1930e7d4c4ea7d9e5224a737bcef452db951b69c789d853f7c"

REPOSITORY = "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
BRANCH = "integration/system-v1"
EXPERIMENT_ID = "ATDS_E1_MOMENTUM_V1_SOURCE_B_EXPLORATORY_N0_V0"

SHA40_RE = re.compile(r"^[0-9a-f]{40}$")
SHA64_RE = re.compile(r"^[0-9a-f]{64}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")

PREFLIGHT_KEYS = {
    "schema",
    "control_id",
    "experiment_id",
    "repository",
    "strategy",
    "datasets",
    "window",
    "execution_model",
    "runner",
    "qualification",
    "environment",
    "result_schema",
    "authority",
    "canonical_digest",
}
RESULT_KEYS = {
    "schema",
    "experiment_id",
    "run_id",
    "timestamp_utc",
    "preflight_digest",
    "repository",
    "protocol",
    "datasets",
    "window",
    "costs",
    "runner_identity",
    "environment_identity",
    "execution_status",
    "metrics",
    "result_payload",
    "result_digest",
    "trace_digest",
}
OBSERVED_KEYS = {
    "repository_full_name",
    "branch",
    "head",
    "tree",
    "preflight_tool_blob",
    "environment_identity",
    "raw_dataset_identity",
    "raw_manifest_sha256",
    "h1_dataset_identity",
    "h1_stream_sha256",
    "runner_blob",
    "qualification_blob",
    "result_schema_digest",
}
ENVIRONMENT_KEYS = {
    "implementation",
    "version",
    "system",
    "machine",
    "dependencies",
    "environment_variables",
}
EXECUTION_STATUSES = {
    "NOT_EXECUTED",
    "EXECUTED",
    "BLOCKED",
    "FAILED",
    "QUALIFICATION_FIXTURE",
}

STRATEGY = {
    "strategy_id": "MOMENTUM_V1",
    "mode": "OFFLINE",
    "class": "EXPLORATORY",
    "research_level": "N0",
    "timeframe": "H1",
    "lookback_completed_admissible_h1": 20,
    "scope_freeze_blob": "6b1e0d6e76d9813cd50eb01eb4b6c06cbfa8260e",
}
WINDOW = {
    "raw_window_start": "2021-05-25T00:00:00.309Z",
    "raw_window_end": "2026-05-24T23:59:59.963Z",
    "pre_oos": "timestamp < 2025-05-25T00:00:00Z",
    "oos_start": "2025-05-25T00:00:00Z",
    "oos_end": "2026-05-24T23:59:59.963Z",
}
DATASETS = {
    "raw": {
        "identity": "SOURCE_B_USTECH_PRICE_CORE_V0_1",
        "manifest_sha256": "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce",
    },
    "h1": {
        "identity": "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1",
        "canonical_stream_sha256": "15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f",
        "qualification_result_sha256": "3a96ac264f23b7c1f14de69dbe0444af5b25265b7a61d5e233479a4b581e6425",
        "jsonl_sha256": "94ccb7c78e2e21cb3baa2dfe0945e7b39e20f74300c3c72addb89135d5af1ca0",
    },
}
PNL_SCOPE = {
    "spread": {"included": True, "mode": "RAW_BID_ASK_INTRINSIC"},
    "commission": {"included": False, "assumed_zero": False},
    "slippage": {"included": False, "assumed_zero": False},
    "financing": {"included": False, "assumed_zero": False},
}
EXECUTION_MODEL = {
    "contract_blob": "cf07f1400af614fa53fe41afe8a40e412d28c87d",
    "breaker_blob": "092a612e432530a7dfea627704d89ea8d03328e5",
    "runtime_blob": "15e72b8743e7726fc8b8bedd933cf7defe56413b",
    "pnl_scope": PNL_SCOPE,
}
RUNNER = {
    "contract_blob": "51dc1152808ec9e841924976eac572cc4ec2ff93",
    "breaker_blob": "4308e3360f3cd834e863eb740a2eb7f087e242c0",
    "runtime_blob": "baad3bd7c2e810451737c89bf8f9bcabc17c5ba6",
}
QUALIFICATION = {
    "contract_blob": "483552f2ea1def15f94a28f2e45b97dd65f786ff",
    "breaker_blob": "dc4858559a2fda113c7290ad39a45d5291580773",
    "reference_blob": "25b01e6d31709f02f9c095262bfe78366e83003b",
    "qualifier_blob": "0793adc08416563125f57a55c0d272d24bb4b3df",
    "report_blob": "6f16f9367e932379a87b59599b59c7cc47127b1d",
}
AUTHORITY = {
    "real_e1_run_authorized": False,
    "e1_08_authorized": False,
    "real_data_performance_authorized": False,
    "profitability_interpretation_authorized": False,
    "mt5_authorized": False,
    "paper_authorized": False,
    "broker_authorized": False,
    "live_authorized": False,
    "capital_authorized": False,
}


def canonical_sha256(value):
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _blocked(reason):
    return {"status": "BLOCKED", "reason": reason}


def _valid_sha(value, size):
    if size == 40:
        return isinstance(value, str) and SHA40_RE.fullmatch(value) is not None
    return isinstance(value, str) and SHA64_RE.fullmatch(value) is not None


def _valid_environment(snapshot):
    if not isinstance(snapshot, dict) or set(snapshot) != ENVIRONMENT_KEYS:
        return False
    for key in ("implementation", "version", "system", "machine"):
        if not isinstance(snapshot[key], str) or not snapshot[key]:
            return False
    for key in ("dependencies", "environment_variables"):
        if not isinstance(snapshot[key], dict):
            return False
        if not all(isinstance(k, str) and isinstance(v, str) for k, v in snapshot[key].items()):
            return False
    return True


def build_preflight(
    *,
    repository_full_name,
    branch,
    head,
    tree,
    preflight_tool_blob,
    environment_snapshot,
):
    if repository_full_name != REPOSITORY or branch != BRANCH:
        raise ValueError("E1_07_REPOSITORY_BRANCH_MISMATCH")
    if not all(_valid_sha(value, 40) for value in (head, tree, preflight_tool_blob)):
        raise ValueError("E1_07_INVALID_GIT_IDENTITY")
    if not _valid_environment(environment_snapshot):
        raise ValueError("E1_07_INVALID_ENVIRONMENT_DESCRIPTOR")

    descriptor = copy.deepcopy(environment_snapshot)
    manifest = {
        "schema": PREFLIGHT_SCHEMA_ID,
        "control_id": "E1-07",
        "experiment_id": EXPERIMENT_ID,
        "repository": {
            "full_name": REPOSITORY,
            "branch": BRANCH,
            "head": head,
            "tree": tree,
            "preflight_tool_blob": preflight_tool_blob,
        },
        "strategy": copy.deepcopy(STRATEGY),
        "datasets": copy.deepcopy(DATASETS),
        "window": copy.deepcopy(WINDOW),
        "execution_model": copy.deepcopy(EXECUTION_MODEL),
        "runner": copy.deepcopy(RUNNER),
        "qualification": copy.deepcopy(QUALIFICATION),
        "environment": {
            "descriptor": descriptor,
            "identity_sha256": canonical_sha256(descriptor),
        },
        "result_schema": {
            "schema_id": RESULT_SCHEMA_ID,
            "canonical_sha256": RESULT_SCHEMA_CANONICAL_SHA256,
        },
        "authority": copy.deepcopy(AUTHORITY),
    }
    manifest["canonical_digest"] = canonical_sha256(manifest)
    return manifest


def _expected_observed(manifest):
    return {
        "repository_full_name": manifest["repository"]["full_name"],
        "branch": manifest["repository"]["branch"],
        "head": manifest["repository"]["head"],
        "tree": manifest["repository"]["tree"],
        "preflight_tool_blob": manifest["repository"]["preflight_tool_blob"],
        "environment_identity": manifest["environment"]["identity_sha256"],
        "raw_dataset_identity": manifest["datasets"]["raw"]["identity"],
        "raw_manifest_sha256": manifest["datasets"]["raw"]["manifest_sha256"],
        "h1_dataset_identity": manifest["datasets"]["h1"]["identity"],
        "h1_stream_sha256": manifest["datasets"]["h1"]["canonical_stream_sha256"],
        "runner_blob": manifest["runner"]["runtime_blob"],
        "qualification_blob": manifest["qualification"]["qualifier_blob"],
        "result_schema_digest": manifest["result_schema"]["canonical_sha256"],
    }


def verify_preflight(manifest, *, observed=None):
    try:
        if not isinstance(manifest, dict) or set(manifest) != PREFLIGHT_KEYS:
            return _blocked("PREFLIGHT_SCHEMA_OR_UNKNOWN_FIELD")
        digest = manifest.get("canonical_digest")
        unsigned = {k: copy.deepcopy(v) for k, v in manifest.items() if k != "canonical_digest"}
        if not _valid_sha(digest, 64) or canonical_sha256(unsigned) != digest:
            return _blocked("PREFLIGHT_DIGEST_MISMATCH")
        if manifest["schema"] != PREFLIGHT_SCHEMA_ID or manifest["control_id"] != "E1-07" or manifest["experiment_id"] != EXPERIMENT_ID:
            return _blocked("PREFLIGHT_IDENTITY_MISMATCH")
        repo = manifest["repository"]
        if not isinstance(repo, dict) or set(repo) != {"full_name", "branch", "head", "tree", "preflight_tool_blob"}:
            return _blocked("REPOSITORY_BINDING_SCHEMA_MISMATCH")
        if repo["full_name"] != REPOSITORY or repo["branch"] != BRANCH:
            return _blocked("REPOSITORY_BRANCH_MISMATCH")
        if not all(_valid_sha(repo[k], 40) for k in ("head", "tree", "preflight_tool_blob")):
            return _blocked("INVALID_GIT_BINDING")
        if manifest["strategy"] != STRATEGY:
            return _blocked("STRATEGY_BINDING_MISMATCH")
        if manifest["datasets"] != DATASETS:
            return _blocked("DATASET_BINDING_MISMATCH")
        if manifest["window"] != WINDOW:
            return _blocked("WINDOW_BINDING_MISMATCH")
        if manifest["execution_model"] != EXECUTION_MODEL:
            return _blocked("EXECUTION_MODEL_BINDING_MISMATCH")
        if manifest["runner"] != RUNNER:
            return _blocked("RUNNER_BINDING_MISMATCH")
        if manifest["qualification"] != QUALIFICATION:
            return _blocked("QUALIFICATION_BINDING_MISMATCH")
        environment = manifest["environment"]
        if not isinstance(environment, dict) or set(environment) != {"descriptor", "identity_sha256"}:
            return _blocked("ENVIRONMENT_BINDING_SCHEMA_MISMATCH")
        if not _valid_environment(environment["descriptor"]):
            return _blocked("INVALID_ENVIRONMENT_DESCRIPTOR")
        if canonical_sha256(environment["descriptor"]) != environment["identity_sha256"]:
            return _blocked("ENVIRONMENT_IDENTITY_MISMATCH")
        if manifest["result_schema"] != {"schema_id": RESULT_SCHEMA_ID, "canonical_sha256": RESULT_SCHEMA_CANONICAL_SHA256}:
            return _blocked("RESULT_SCHEMA_BINDING_MISMATCH")
        if manifest["authority"] != AUTHORITY or any(manifest["authority"].values()):
            return _blocked("AUTHORITY_ESCALATION")
        if observed is not None:
            if not isinstance(observed, dict) or set(observed) != OBSERVED_KEYS:
                return _blocked("OBSERVED_BINDING_SCHEMA_MISMATCH")
            expected = _expected_observed(manifest)
            if observed != expected:
                return _blocked("OBSERVED_BINDING_MISMATCH")
        return {"status": "PASS", "canonical_digest": digest}
    except (KeyError, TypeError, ValueError):
        return _blocked("PREFLIGHT_MALFORMED")


def build_result_envelope(
    preflight,
    *,
    run_id,
    timestamp_utc,
    execution_status,
    metrics,
    result_payload,
):
    if verify_preflight(preflight)["status"] != "PASS":
        raise ValueError("E1_07_INVALID_PREFLIGHT")
    if not isinstance(run_id, str) or not run_id:
        raise ValueError("E1_07_INVALID_RUN_ID")
    if not isinstance(timestamp_utc, str) or UTC_RE.fullmatch(timestamp_utc) is None:
        raise ValueError("E1_07_INVALID_TIMESTAMP")
    if execution_status not in EXECUTION_STATUSES:
        raise ValueError("E1_07_INVALID_EXECUTION_STATUS")
    if not isinstance(metrics, dict) or not isinstance(result_payload, dict):
        raise ValueError("E1_07_INVALID_RESULT_PAYLOAD")

    envelope = {
        "schema": RESULT_SCHEMA_ID,
        "experiment_id": EXPERIMENT_ID,
        "run_id": run_id,
        "timestamp_utc": timestamp_utc,
        "preflight_digest": preflight["canonical_digest"],
        "repository": copy.deepcopy(preflight["repository"]),
        "protocol": copy.deepcopy(preflight["strategy"]),
        "datasets": copy.deepcopy(preflight["datasets"]),
        "window": copy.deepcopy(preflight["window"]),
        "costs": copy.deepcopy(preflight["execution_model"]["pnl_scope"]),
        "runner_identity": copy.deepcopy(preflight["runner"]),
        "environment_identity": preflight["environment"]["identity_sha256"],
        "execution_status": execution_status,
        "metrics": copy.deepcopy(metrics),
        "result_payload": copy.deepcopy(result_payload),
    }
    envelope["result_digest"] = canonical_sha256(envelope["result_payload"])
    envelope["trace_digest"] = canonical_sha256(envelope)
    return envelope


def verify_result_envelope(envelope, preflight):
    try:
        if verify_preflight(preflight)["status"] != "PASS":
            return _blocked("BOUND_PREFLIGHT_INVALID")
        if not isinstance(envelope, dict) or set(envelope) != RESULT_KEYS:
            return _blocked("RESULT_SCHEMA_OR_UNKNOWN_FIELD")
        if envelope["schema"] != RESULT_SCHEMA_ID or envelope["experiment_id"] != EXPERIMENT_ID:
            return _blocked("RESULT_IDENTITY_MISMATCH")
        if not isinstance(envelope["run_id"], str) or not envelope["run_id"]:
            return _blocked("RESULT_RUN_ID_INVALID")
        if not isinstance(envelope["timestamp_utc"], str) or UTC_RE.fullmatch(envelope["timestamp_utc"]) is None:
            return _blocked("RESULT_TIMESTAMP_INVALID")
        if envelope["execution_status"] not in EXECUTION_STATUSES:
            return _blocked("RESULT_STATUS_INVALID")
        if envelope["preflight_digest"] != preflight["canonical_digest"]:
            return _blocked("RESULT_PREFLIGHT_BINDING_MISMATCH")
        if envelope["repository"] != preflight["repository"]:
            return _blocked("RESULT_REPOSITORY_BINDING_MISMATCH")
        if envelope["protocol"] != preflight["strategy"]:
            return _blocked("RESULT_PROTOCOL_BINDING_MISMATCH")
        if envelope["datasets"] != preflight["datasets"]:
            return _blocked("RESULT_DATASET_BINDING_MISMATCH")
        if envelope["window"] != preflight["window"]:
            return _blocked("RESULT_WINDOW_BINDING_MISMATCH")
        if envelope["costs"] != preflight["execution_model"]["pnl_scope"]:
            return _blocked("RESULT_COST_BINDING_MISMATCH")
        if envelope["runner_identity"] != preflight["runner"]:
            return _blocked("RESULT_RUNNER_BINDING_MISMATCH")
        if envelope["environment_identity"] != preflight["environment"]["identity_sha256"]:
            return _blocked("RESULT_ENVIRONMENT_BINDING_MISMATCH")
        if not isinstance(envelope["metrics"], dict) or not isinstance(envelope["result_payload"], dict):
            return _blocked("RESULT_PAYLOAD_INVALID")
        if canonical_sha256(envelope["result_payload"]) != envelope["result_digest"]:
            return _blocked("RESULT_DIGEST_MISMATCH")
        unsigned_trace = {k: copy.deepcopy(v) for k, v in envelope.items() if k != "trace_digest"}
        if canonical_sha256(unsigned_trace) != envelope["trace_digest"]:
            return _blocked("TRACE_DIGEST_MISMATCH")
        return {"status": "PASS", "result_digest": envelope["result_digest"], "trace_digest": envelope["trace_digest"]}
    except (KeyError, TypeError, ValueError):
        return _blocked("RESULT_MALFORMED")
