"""Synthetic-only fixtures for RVO-02 qualification.

No real strategy, market data, OOS result, broker state, or performance is
consumed by this module.
"""

from __future__ import annotations

import copy

SYNTHETIC_HEAD = "1" * 40
SYNTHETIC_TREE = "2" * 40
SYNTHETIC_ENV = "sha256:" + "3" * 64

def catalog_entries():
    return [
        {
            "control_id": "DATA-ADMISSIBILITY",
            "owner_id": "DATA",
            "owner_contract_ref": "blob:data-owner",
            "failure_mode_refs": ["DATA_IDENTITY_OR_ADMISSIBILITY"],
            "applicability_rule_ref": "rule:data-required",
            "input_contract_ref": "schema:data-input",
            "output_contract_ref": "schema:data-output",
            "dependency_control_ids": [],
            "native_status_schema_ref": "status:data-native",
            "blocking_rule_ref": "rule:data-blocking",
            "reconstructibility_contract_ref": "recon:data",
            "validity_scope": "SYNTHETIC_CLAIM",
        },
        {
            "control_id": "TEMPORAL-PIT",
            "owner_id": "TEMPORAL",
            "owner_contract_ref": "blob:temporal-owner",
            "failure_mode_refs": ["LOOKAHEAD_OR_KNOWLEDGE_LEAKAGE"],
            "applicability_rule_ref": "rule:temporal-required",
            "input_contract_ref": "schema:temporal-input",
            "output_contract_ref": "schema:temporal-output",
            "dependency_control_ids": ["DATA-ADMISSIBILITY"],
            "native_status_schema_ref": "status:temporal-native",
            "blocking_rule_ref": "rule:temporal-blocking",
            "reconstructibility_contract_ref": "recon:temporal",
            "validity_scope": "SYNTHETIC_CLAIM",
        },
        {
            "control_id": "EXECUTION-COST",
            "owner_id": "EXECUTION",
            "owner_contract_ref": "blob:execution-owner",
            "failure_mode_refs": ["EXECUTION_OR_COST_MISMATCH"],
            "applicability_rule_ref": "rule:execution-required",
            "input_contract_ref": "schema:execution-input",
            "output_contract_ref": "schema:execution-output",
            "dependency_control_ids": ["DATA-ADMISSIBILITY"],
            "native_status_schema_ref": "status:execution-native",
            "blocking_rule_ref": "rule:execution-blocking",
            "reconstructibility_contract_ref": "recon:execution",
            "validity_scope": "SYNTHETIC_CLAIM",
        },
        {
            "control_id": "SMF-INFERENCE",
            "owner_id": "SMF",
            "owner_contract_ref": "blob:smf-owner",
            "failure_mode_refs": ["DEPENDENCE_AWARE_INFERENCE"],
            "applicability_rule_ref": "rule:smf-required",
            "input_contract_ref": "schema:smf-input",
            "output_contract_ref": "schema:smf-output",
            "dependency_control_ids": ["DATA-ADMISSIBILITY", "TEMPORAL-PIT", "EXECUTION-COST"],
            "native_status_schema_ref": "status:smf-native",
            "blocking_rule_ref": "rule:smf-blocking",
            "reconstructibility_contract_ref": "recon:smf",
            "validity_scope": "SYNTHETIC_CLAIM",
        },
        {
            "control_id": "MCEPR-SEARCH",
            "owner_id": "MCEPR",
            "owner_contract_ref": "blob:mcepr-owner",
            "failure_mode_refs": ["SEARCH_UNIVERSE_PROVENANCE"],
            "applicability_rule_ref": "rule:mcepr-required",
            "input_contract_ref": "schema:mcepr-input",
            "output_contract_ref": "schema:mcepr-output",
            "dependency_control_ids": [],
            "native_status_schema_ref": "status:mcepr-native",
            "blocking_rule_ref": "rule:mcepr-blocking",
            "reconstructibility_contract_ref": "recon:mcepr",
            "validity_scope": "SYNTHETIC_CLAIM",
        },
    ]

def applicability_records():
    return [
        {
            "control_id": item["control_id"],
            "applicability_state": "APPLICABLE",
            "applicability_basis": "synthetic claim requires this frozen control",
            "material": True,
        }
        for item in catalog_entries()
    ]

def smf_method_bindings():
    return {
        "SMF-INFERENCE": {
            "p1_method_ref": "SMF:M05",
            "activation_digest": "sha256:" + "4" * 64,
            "qualified_method_ref": "blob:smf-m05-qualified",
            "claim_ref": "claim:synthetic",
            "failure_mode_ref": "DEPENDENCE_AWARE_INFERENCE",
            "assumption_set_ref": "assumptions:synthetic",
            "parameter_policy_ref": "params:predeclared",
            "dependency_refs": [
                "DATA-ADMISSIBILITY",
                "TEMPORAL-PIT",
                "EXECUTION-COST",
            ],
        }
    }

def pre_snapshot_kwargs():
    return {
        "repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
        "branch": "integration/system-v1",
        "head": SYNTHETIC_HEAD,
        "tree": SYNTHETIC_TREE,
        "dataset_refs": ["dataset:synthetic:v1"],
        "temporal_ref": "temporal:synthetic:pre",
        "execution_ref": "execution:synthetic:v1",
        "smf_activation_refs": ["sha256:" + "4" * 64],
        "mcepr_pre_ref": "registry:synthetic:pre",
        "oos_pre_state": "PRISTINE_SYNTHETIC",
        "environment_identity": SYNTHETIC_ENV,
        "owner_contract_refs": {
            "DATA": "blob:data-owner",
            "TEMPORAL": "blob:temporal-owner",
            "EXECUTION": "blob:execution-owner",
            "SMF": "blob:smf-owner",
            "MCEPR": "blob:mcepr-owner",
            "P1": "blob:p1-owner",
            "PCP": "blob:pcp-owner",
        },
    }

def manifest_kwargs(catalog, pre_snapshot):
    return {
        "catalog": catalog,
        "experiment_spec_id": "EXS-synthetic",
        "claim_ref": "claim:synthetic",
        "estimand_ref": "estimand:synthetic",
        "validity_scope_ref": "scope:synthetic",
        "pre_snapshot": pre_snapshot,
        "applicability_records": applicability_records(),
        "method_bindings": smf_method_bindings(),
        "result_exposed": False,
    }

def owner_result_kwargs(control_id, owner_id, status_schema, native_status="PASS"):
    return {
        "control_id": control_id,
        "owner_id": owner_id,
        "native_status_schema_ref": status_schema,
        "native_status": native_status,
        "asserted_native_status": native_status,
        "orchestration_state": "READY",
        "blocking_rule_ref": None,
        "snapshot_digest": None,
    }

def copy_value(value):
    return copy.deepcopy(value)
