from __future__ import annotations

import copy

from breakers.native_bi5_o_semantic_comparator_breaker import (
    _compare,
    _frozen,
    _qualified_input,
)


def test_adv_integrity_conflict_precedes_unrelated_distinct_version() -> None:
    left = _frozen()
    data = _qualified_input()

    data["acquisition_declaration_version"] = "D_MATERIALIZATION_V0_2_SYNTHETIC"
    d = next(item for item in data["reconstruction_tuple"] if item["stage"] == "D")
    d["normative_version"] = "D_MATERIALIZATION_V0_2_SYNTHETIC"

    r = next(item for item in data["reconstruction_tuple"] if item["stage"] == "R")
    r["integrity_digest"] = "e" * 64

    right = _frozen(data)
    result = _compare(left, right)

    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] == "NORMATIVE_VERSION_INTEGRITY_CONFLICT"
    assert result["reason"] == "NORMATIVE_VERSION_INTEGRITY_CONFLICT"


def test_adv_component_execution_metadata_is_nonsemantic() -> None:
    left = _frozen()
    data = _qualified_input()
    component = data["acquisition_snapshot"]["components"][0]
    component["worker_id"] = "worker-99"
    component["worker_partition"] = "partition-z"
    component["cache_layout"] = "cache://alternate"
    component["temporary_path"] = "/tmp/alternate"
    component["artifact_filename"] = "alternate.bi5"
    component["git_blob_identity"] = "deadbeef"

    right = _frozen(data)
    result = _compare(left, right)

    assert result["oracle_result"] == "SEMANTIC_EQUAL"
    assert result["qualified_universe_comparison"] == "SEMANTIC_EQUAL"
    assert result["comparison_scope"] == "SAME_QUALIFICATION_STATE"


def test_adv_completeness_execution_metadata_is_nonsemantic() -> None:
    left = _frozen()
    data = _qualified_input()
    evidence = data["acquisition_snapshot"]["completeness_evidence"]
    evidence["worker_id"] = "worker-11"
    evidence["worker_partition"] = "partition-b"
    evidence["cache_layout"] = "cache://other"
    evidence["temporary_path"] = "/tmp/completeness-other"
    evidence["artifact_filename"] = "completeness-evidence.json"

    right = _frozen(data)
    result = _compare(left, right)

    assert result["oracle_result"] == "SEMANTIC_EQUAL"
    assert result["qualified_universe_comparison"] == "SEMANTIC_EQUAL"
    assert result["comparison_scope"] == "SAME_QUALIFICATION_STATE"
