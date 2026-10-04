"""Positive synthetic qualification for the minimal RVO runtime."""

from __future__ import annotations

import copy

from src import rvo_orchestrator as rvo
from tests import rvo_runtime_fixture as fx


def _build():
    catalog = rvo.build_control_catalog(
        fx.catalog_entries(),
        catalog_version="RVO-CATALOG-SYNTHETIC-V1",
    )
    pre = rvo.build_pre_snapshot(**fx.pre_snapshot_kwargs())
    manifest = rvo.build_pre_result_manifest(**fx.manifest_kwargs(catalog, pre))
    return catalog, pre, manifest


def test_positive_synthetic_manifest_is_deterministic_and_non_authoritative():
    catalog1, pre1, manifest1 = _build()
    catalog2 = rvo.build_control_catalog(
        list(reversed(fx.catalog_entries())),
        catalog_version="RVO-CATALOG-SYNTHETIC-V1",
    )
    pre2 = rvo.build_pre_snapshot(**fx.pre_snapshot_kwargs())
    kw = fx.manifest_kwargs(catalog2, pre2)
    kw["applicability_records"] = list(reversed(kw["applicability_records"]))
    manifest2 = rvo.build_pre_result_manifest(**kw)

    assert catalog1["catalog_digest"] == catalog2["catalog_digest"]
    assert pre1["pre_snapshot_digest"] == pre2["pre_snapshot_digest"]
    assert manifest1["manifest_digest"] == manifest2["manifest_digest"]
    assert manifest1["routing_plan"] == manifest2["routing_plan"]
    assert manifest1["manifest_authority"] is False
    assert rvo.RVO_AUTHORITY == "NONE"


def test_positive_synthetic_package_preserves_native_status_and_pre_post_firewall():
    catalog, pre, manifest = _build()
    post = rvo.build_post_snapshot(
        pre_manifest_digest=manifest["manifest_digest"],
        actual_input_refs=["input:synthetic"],
        owner_output_refs=["output:synthetic"],
        p1_finding_refs=["finding:synthetic"],
        pcp_post_ref="pcp:synthetic:post",
        mcepr_post_ref="registry:synthetic:post",
        oos_post_state="EXPOSED_SYNTHETIC",
        environment_identity=fx.SYNTHETIC_ENV,
        material_dependency_refs=["dep:synthetic"],
    )
    assert rvo.enforce_pre_post_firewall(
        pre,
        post,
        current_mcepr_ref=pre["mcepr_pre_ref"],
        current_oos_state=pre["oos_pre_state"],
    ) == "PASS"

    by_id = {item["control_id"]: item for item in catalog["controls"]}
    results = []
    for control_id in manifest["routing_plan"]:
        control = by_id[control_id]
        native = {
            "DATA-ADMISSIBILITY": "UNVERIFIED",
            "TEMPORAL-PIT": "PASS",
            "EXECUTION-COST": "PASS",
            "SMF-INFERENCE": "SUPPORTED",
            "MCEPR-SEARCH": "UNKNOWN",
        }[control_id]
        results.append(
            rvo.bind_owner_result(
                control_id=control_id,
                owner_id=control["owner_id"],
                native_status_schema_ref=control["native_status_schema_ref"],
                native_status=native,
                asserted_native_status=native,
                orchestration_state="READY",
                blocking_rule_ref=None,
                snapshot_digest=pre["pre_snapshot_digest"],
            )
        )

    recon = rvo.validate_reconstruction_descriptor(
        reconstruction_class="EXACT_REPLAY",
        material_inputs={
            "catalog_digest": catalog["catalog_digest"],
            "pre_snapshot_digest": pre["pre_snapshot_digest"],
        },
        environment_identity=fx.SYNTHETIC_ENV,
        dependency_refs=["dep:synthetic"],
        schema_refs=[
            rvo.CATALOG_SCHEMA,
            rvo.MANIFEST_SCHEMA,
            rvo.PACKAGE_SCHEMA,
        ],
        parameters={"synthetic": "frozen"},
        seeds={"synthetic_rng": "0"},
        owner_contract_refs=pre["owner_contract_refs"],
        routing_order=manifest["routing_plan"],
        pre_manifest_digest=manifest["manifest_digest"],
        runtime_attestation={"informational": "not durable authority"},
    )

    package = rvo.build_validation_package(
        manifest=manifest,
        pre_snapshot=pre,
        post_snapshot=post,
        owner_results=results,
        reconstruction_descriptor=recon,
    )
    assert package["package_state"] == "PACKAGE_COMPLETE"
    assert package["package_authority"] is False
    assert package["scientific_authority"] is False
    assert package["operational_authority"] is False
    assert package["rvo_authority"] == "NONE"
    assert {item["native_status"] for item in package["owner_results"]} >= {
        "UNVERIFIED",
        "UNKNOWN",
        "SUPPORTED",
    }
    assert rvo.verify_package(copy.deepcopy(package)) is True


def test_positive_head_drift_can_continue_only_when_material_bindings_are_exact():
    before = {"catalog": "c1", "dataset": "d1"}
    after = {"catalog": "c1", "dataset": "d1"}
    assert rvo.validate_material_drift(
        before,
        after,
        revalidated_refs={},
        head_changed=True,
        impact_known=True,
    ) == "UNCHANGED"


def test_qualification_semantics_remain_bounded():
    semantics = rvo.qualification_semantics()
    assert semantics["unknown_unknown_coverage"] == "NOT_CLAIMED"
    assert semantics["rvo_authority"] == "NONE"
    assert semantics["pass_grants_scientific_authority"] is False
    assert semantics["pass_grants_operational_authority"] is False
    assert semantics["pass_grants_trading_authority"] is False
