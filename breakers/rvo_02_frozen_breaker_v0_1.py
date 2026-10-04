"""RVO-02 executable materialization of the frozen RVO-01 breaker contract.

This file is intended to be created and executed before the RVO runtime exists.
The initial RED must therefore be an explicit RVO_RUNTIME_ABSENT failure, not an
accidental broken import. Once the runtime exists, all 45 frozen cases execute.
"""

from __future__ import annotations

import copy
import importlib
import json
import subprocess
from pathlib import Path

import pytest

from tests import rvo_runtime_fixture as fx

ROOT = Path(__file__).resolve().parents[1]
FROZEN_CONTRACT = ROOT / "GOVERNANCE" / "RVO-01-FROZEN-ADVERSARIAL-BREAKER-CONTRACT-V0.1.json"
RVO01_PARENT = "1a6b4e3e62e37e1e5827abb14472f84d1aed9888"
RVO01_HEAD = "7ce4665bff29e7e2cbd5e327764b8f2a5fbbf18b"

def _load_contract():
    return json.loads(FROZEN_CONTRACT.read_text(encoding="utf-8"))

CONTRACT = _load_contract()
FROZEN_CASE_IDS = tuple(item["id"] for item in CONTRACT["cases"])
EXPECTED_CASE_IDS = tuple(f"RVO-B{i:02d}" for i in range(1, 46))

def _runtime_or_none():
    try:
        return importlib.import_module("src.rvo_orchestrator")
    except ModuleNotFoundError as exc:
        if exc.name == "src.rvo_orchestrator":
            return None
        raise

def _expect_error(rt, code, fn, *args, **kwargs):
    with pytest.raises((rt.RVOFail, rt.RVOBlocked)) as caught:
        fn(*args, **kwargs)
    assert caught.value.code == code

def _base(rt):
    catalog = rt.build_control_catalog(fx.catalog_entries(), catalog_version="RVO-CATALOG-SYNTHETIC-V1")
    pre = rt.build_pre_snapshot(**fx.pre_snapshot_kwargs())
    manifest = rt.build_pre_result_manifest(**fx.manifest_kwargs(catalog, pre))
    return catalog, pre, manifest

def _git_changed_files(base, head):
    out = subprocess.run(
        ["git", "diff", "--name-only", f"{base}..{head}"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout
    return tuple(line for line in out.splitlines() if line)

# --- B01-B05: ownership / authority ---

def case_b01(rt):
    catalog, _, _ = _base(rt)
    _expect_error(rt, "OWNER_OVERRIDE_FORBIDDEN", rt.build_routing_plan, catalog, owner_contract_overrides={"SMF": "rvo:override"})

def case_b02(rt):
    _expect_error(rt, "RVO_AUTHORITY_EXPANSION", rt.assert_rvo_authority_claim, "SCIENTIFIC_FINDING")

def case_b03(rt):
    for claim in ("NORMATIVE_DECISION", "ACTION", "TRADING", "CAPITAL"):
        _expect_error(rt, "RVO_AUTHORITY_EXPANSION", rt.assert_rvo_authority_claim, claim)

def case_b04(rt):
    catalog, _, _ = _base(rt)
    _expect_error(rt, "OWNER_SEMANTIC_REWRITE_FORBIDDEN", rt.build_routing_plan, catalog, owner_semantic_overrides={"DATA": "RVO_VALIDITY"})

def case_b05(rt):
    _expect_error(rt, "EVIDENCE_AUTHORITY_LAUNDERING", rt.assert_evidence_authority, "PCP", "SCIENTIFIC_AUTHORITY")

# --- B06-B10: applicability / omission ---

def case_b06(rt):
    catalog = rt.build_control_catalog(fx.catalog_entries(), catalog_version="RVO-CATALOG-SYNTHETIC-V1")
    pre = rt.build_pre_snapshot(**fx.pre_snapshot_kwargs())
    kw = fx.manifest_kwargs(catalog, pre)
    kw["applicability_records"] = kw["applicability_records"][:-1]
    _expect_error(rt, "CONTROL_APPLICABILITY_INCOMPLETE", rt.build_pre_result_manifest, **kw)

def case_b07(rt):
    catalog = rt.build_control_catalog(fx.catalog_entries(), catalog_version="RVO-CATALOG-SYNTHETIC-V1")
    pre = rt.build_pre_snapshot(**fx.pre_snapshot_kwargs())
    kw = fx.manifest_kwargs(catalog, pre)
    recs = copy.deepcopy(kw["applicability_records"])
    recs[0] = {**recs[0], "applicability_state": "NOT_APPLICABLE", "applicability_basis": ""}
    kw["applicability_records"] = recs
    _expect_error(rt, "UNJUSTIFIED_NOT_APPLICABLE", rt.build_pre_result_manifest, **kw)

def case_b08(rt):
    catalog = rt.build_control_catalog(fx.catalog_entries(), catalog_version="RVO-CATALOG-SYNTHETIC-V1")
    pre = rt.build_pre_snapshot(**fx.pre_snapshot_kwargs())
    kw = fx.manifest_kwargs(catalog, pre)
    recs = copy.deepcopy(kw["applicability_records"])
    recs[0] = {**recs[0], "applicability_state": "UNKNOWN", "applicability_basis": "owner capability unresolved", "material": True}
    kw["applicability_records"] = recs
    _expect_error(rt, "MATERIAL_APPLICABILITY_UNKNOWN", rt.build_pre_result_manifest, **kw)

def case_b09(rt):
    catalog, _, _ = _base(rt)
    _expect_error(rt, "CATALOG_STATE_LAUNDERING", rt.assert_catalog_implication, catalog, "REGISTERED", "PASSED")

def case_b10(rt):
    _, _, manifest = _base(rt)
    _expect_error(rt, "RETROACTIVE_CATALOG_SUBSTITUTION", rt.rebind_manifest_catalog, manifest, "sha256:" + "9" * 64, result_exposed=True)

# --- B11-B15: pre-result freeze / method binding ---

def case_b11(rt):
    catalog = rt.build_control_catalog(fx.catalog_entries(), catalog_version="RVO-CATALOG-SYNTHETIC-V1")
    pre = rt.build_pre_snapshot(**fx.pre_snapshot_kwargs())
    kw = fx.manifest_kwargs(catalog, pre)
    kw["result_exposed"] = True
    _expect_error(rt, "POST_RESULT_MANIFEST_FORBIDDEN", rt.build_pre_result_manifest, **kw)

def case_b12(rt):
    _, _, manifest = _base(rt)
    _expect_error(rt, "SEALED_MANIFEST_MUTATION", rt.amend_manifest, manifest, {"estimand_ref": "changed"}, result_exposed=True)

def case_b13(rt):
    catalog = rt.build_control_catalog(fx.catalog_entries(), catalog_version="RVO-CATALOG-SYNTHETIC-V1")
    pre = rt.build_pre_snapshot(**fx.pre_snapshot_kwargs())
    kw = fx.manifest_kwargs(catalog, pre)
    kw["method_bindings"] = {"SMF-INFERENCE": {"p1_method_ref": "SMF:M05"}}
    _expect_error(rt, "LABEL_ONLY_METHOD_REF", rt.build_pre_result_manifest, **kw)

def case_b14(rt):
    catalog = rt.build_control_catalog(fx.catalog_entries(), catalog_version="RVO-CATALOG-SYNTHETIC-V1")
    pre = rt.build_pre_snapshot(**fx.pre_snapshot_kwargs())
    kw = fx.manifest_kwargs(catalog, pre)
    bindings = fx.smf_method_bindings()
    bindings["SMF-INFERENCE"]["claim_ref"] = "claim:other"
    kw["method_bindings"] = bindings
    _expect_error(rt, "METHOD_BINDING_MISMATCH", rt.build_pre_result_manifest, **kw)

def case_b15(rt):
    catalog = rt.build_control_catalog(fx.catalog_entries(), catalog_version="RVO-CATALOG-SYNTHETIC-V1")
    pre = rt.build_pre_snapshot(**fx.pre_snapshot_kwargs())
    kw = fx.manifest_kwargs(catalog, pre)
    bindings = fx.smf_method_bindings()
    bindings["SMF-INFERENCE"]["parameter_policy_ref"] = ""
    kw["method_bindings"] = bindings
    _expect_error(rt, "MATERIAL_PARAMETER_POLICY_MISSING", rt.build_pre_result_manifest, **kw)

# --- B16-B21: status preservation ---

@pytest.mark.parametrize("native,attempted", [
    ("UNKNOWN", "PASS"),
    ("BLOCKED", "FAIL"),
    ("NOT_APPLICABLE", "PASS"),
    ("UNVERIFIED", "UNKNOWN"),
    ("SUPPORTED", "VALIDATED_STRATEGY"),
])
def _status_attack_helper(rt, native, attempted):
    _expect_error(rt, "STATUS_LAUNDERING", rt.bind_owner_result,
        control_id="DATA-ADMISSIBILITY", owner_id="DATA",
        native_status_schema_ref="status:data-native",
        native_status=native, asserted_native_status=attempted,
        orchestration_state="READY", blocking_rule_ref=None,
        snapshot_digest="sha256:" + "a" * 64)

def case_b16(rt): _status_attack_helper(rt, "UNKNOWN", "PASS")
def case_b17(rt): _status_attack_helper(rt, "BLOCKED", "FAIL")
def case_b18(rt): _status_attack_helper(rt, "NOT_APPLICABLE", "PASS")
def case_b19(rt): _status_attack_helper(rt, "UNVERIFIED", "UNKNOWN")
def case_b20(rt): _status_attack_helper(rt, "SUPPORTED", "VALIDATED_STRATEGY")

def case_b21(rt):
    _expect_error(rt, "UNGROUNDED_STATUS_INTERPRETATION", rt.bind_owner_result,
        control_id="DATA-ADMISSIBILITY", owner_id="DATA",
        native_status_schema_ref="status:data-native",
        native_status="BLOCKED", asserted_native_status="BLOCKED",
        orchestration_state="BLOCKED", blocking_rule_ref=None,
        snapshot_digest="sha256:" + "a" * 64)

# --- B22-B25: PRE / POST firewall ---

def case_b22(rt):
    _, pre, manifest = _base(rt)
    post = rt.build_post_snapshot(
        pre_manifest_digest=manifest["manifest_digest"],
        actual_input_refs=["input:synthetic"],
        owner_output_refs=["out:synthetic"],
        p1_finding_refs=["finding:synthetic"],
        pcp_post_ref="pcp:post",
        mcepr_post_ref="registry:synthetic:post",
        oos_post_state="EXPOSED_SYNTHETIC",
        environment_identity=fx.SYNTHETIC_ENV,
        material_dependency_refs=["dep:synthetic"],
    )
    _expect_error(rt, "RETROACTIVE_PRE_STATE_REWRITE", rt.enforce_pre_post_firewall,
        pre, post, current_mcepr_ref=post["mcepr_post_ref"], current_oos_state=pre["oos_pre_state"])

def case_b23(rt):
    _, pre, manifest = _base(rt)
    post = rt.build_post_snapshot(
        pre_manifest_digest=manifest["manifest_digest"],
        actual_input_refs=["input:synthetic"], owner_output_refs=["out:synthetic"],
        p1_finding_refs=["finding:synthetic"], pcp_post_ref="pcp:post",
        mcepr_post_ref="registry:synthetic:post", oos_post_state="EXPOSED_SYNTHETIC",
        environment_identity=fx.SYNTHETIC_ENV, material_dependency_refs=["dep:synthetic"],
    )
    _expect_error(rt, "RETROACTIVE_PRE_STATE_REWRITE", rt.enforce_pre_post_firewall,
        pre, post, current_mcepr_ref=pre["mcepr_pre_ref"], current_oos_state=post["oos_post_state"])

def case_b24(rt):
    _expect_error(rt, "MISSING_PRE_STATE", rt.enforce_pre_post_firewall,
        None, {"post_snapshot_digest": "sha256:" + "b"*64}, current_mcepr_ref="x", current_oos_state="x")

def case_b25(rt):
    _, pre, _ = _base(rt)
    _expect_error(rt, "PRE_POST_COLLAPSE", rt.enforce_pre_post_firewall,
        pre, pre, current_mcepr_ref=pre["mcepr_pre_ref"], current_oos_state=pre["oos_pre_state"])

# --- B26-B28: drift / coherence ---

def case_b26(rt):
    _expect_error(rt, "STALE_MATERIAL_BINDING", rt.validate_material_drift,
        {"dataset": "d1"}, {"dataset": "d2"}, revalidated_refs={}, head_changed=True, impact_known=True)

def case_b27(rt):
    _expect_error(rt, "UNKNOWN_DRIFT_IMPACT", rt.validate_material_drift,
        {"dataset": "d1"}, {"dataset": "d1"}, revalidated_refs={}, head_changed=True, impact_known=False)

def case_b28(rt):
    _expect_error(rt, "MIXED_SNAPSHOT_EXECUTION", rt.validate_snapshot_coherence,
        [{"control_id": "A", "snapshot_digest": "sha256:"+"1"*64},
         {"control_id": "B", "snapshot_digest": "sha256:"+"2"*64}],
        expected_snapshot_digest="sha256:"+"1"*64)

# --- B29-B33: reconstructibility ---

def case_b29(rt):
    _expect_error(rt, "RUNTIME_ATTESTATION_NOT_DURABLE", rt.validate_reconstruction_descriptor,
        reconstruction_class="EXACT_REPLAY", material_inputs={},
        environment_identity=None, dependency_refs=[], schema_refs=[],
        parameters={}, seeds={}, owner_contract_refs={}, routing_order=[],
        pre_manifest_digest=None, runtime_attestation={"object_id": 123})

def case_b30(rt):
    _expect_error(rt, "INCOMPLETE_RECONSTRUCTION", rt.validate_reconstruction_descriptor,
        reconstruction_class="EXACT_REPLAY", material_inputs={"x": "y"},
        environment_identity="", dependency_refs=[], schema_refs=["schema:x"],
        parameters={"alpha": "0.05"}, seeds={}, owner_contract_refs={"SMF": "blob:smf"},
        routing_order=["SMF-INFERENCE"], pre_manifest_digest="sha256:"+"c"*64,
        runtime_attestation=None)

def case_b31(rt):
    _expect_error(rt, "RECONSTRUCTION_CLASS_ESCALATION", rt.promote_reconstruction_class,
        "EVIDENCE_REPLAY", "EXACT_REPLAY")

def case_b32(rt):
    catalog1 = rt.build_control_catalog(fx.catalog_entries(), catalog_version="RVO-CATALOG-SYNTHETIC-V1")
    pre1 = rt.build_pre_snapshot(**fx.pre_snapshot_kwargs())
    m1 = rt.build_pre_result_manifest(**fx.manifest_kwargs(catalog1, pre1))
    catalog2 = rt.build_control_catalog(list(reversed(fx.catalog_entries())), catalog_version="RVO-CATALOG-SYNTHETIC-V1")
    pre2 = rt.build_pre_snapshot(**fx.pre_snapshot_kwargs())
    kw = fx.manifest_kwargs(catalog2, pre2)
    kw["applicability_records"] = list(reversed(kw["applicability_records"]))
    m2 = rt.build_pre_result_manifest(**kw)
    assert m1["manifest_digest"] == m2["manifest_digest"]
    assert m1["routing_plan"] == m2["routing_plan"]

def case_b33(rt):
    _, _, manifest = _base(rt)
    tampered = copy.deepcopy(manifest)
    tampered["estimand_ref"] = "tampered"
    _expect_error(rt, "MANIFEST_DIGEST_MISMATCH", rt.verify_manifest, tampered)

# --- B34-B36: provenance / multiplicity ---

def case_b34(rt):
    _expect_error(rt, "INVENTED_MULTIPLICITY_PARAMETER", rt.resolve_multiplicity_parameter,
        mcepr_event_count=12, explicit_n_trials=None, search_universe_status="UNKNOWN_SEARCH_UNIVERSE")

def case_b35(rt):
    assert rt.interpret_relation_absence(relation_present=False) == "UNKNOWN"

def case_b36(rt):
    for claim in ("COMPLETE", "PRISTINE_EVIDENCE"):
        _expect_error(rt, "MCEPR_COMPLETENESS_OVERCLAIM", rt.validate_mcepr_claim, claim)

# --- B37-B38: capability gaps ---

def case_b37(rt):
    _expect_error(rt, "TEMPORAL_CAPABILITY_GAP", rt.validate_claim_capabilities,
        {"historical_point_in_time_required": True, "all_in_profitability_required": False},
        {"temporal_status": "UNRESOLVED", "execution_cost_components": []})

def case_b38(rt):
    _expect_error(rt, "EXECUTION_COST_CAPABILITY_GAP", rt.validate_claim_capabilities,
        {"historical_point_in_time_required": False, "all_in_profitability_required": True},
        {"temporal_status": "QUALIFIED", "execution_cost_components": ["spread"]})

# --- B39-B41: global claim laundering ---

def case_b39(rt):
    _expect_error(rt, "GLOBAL_SCIENTIFIC_PASS_FORBIDDEN", rt.assert_global_claim, "STRATEGY_VALIDATION", "PASS")

def case_b40(rt):
    _expect_error(rt, "PROCEDURAL_TO_SCIENTIFIC_LAUNDERING", rt.interpret_package_state,
        "PACKAGE_COMPLETE", "SCIENTIFIC_SUPPORT")

def case_b41(rt):
    results = [
        {"control_id": "A", "orchestration_state": "READY", "native_status": "PASS"},
        {"control_id": "B", "orchestration_state": "BLOCKED", "native_status": "BLOCKED"},
    ]
    assert rt.aggregate_procedural_state(results) == "PACKAGE_BLOCKED"

# --- B42-B45: RVO-01 authority boundary ---

def case_b42(rt):
    files = _git_changed_files(RVO01_PARENT, RVO01_HEAD)
    assert files
    assert all(not p.endswith((".py", ".pyi")) for p in files)
    assert all(not p.startswith(("src/", "tools/", "tests/", "breakers/")) for p in files)

def case_b43(rt):
    files = _git_changed_files(RVO01_PARENT, RVO01_HEAD)
    forbidden = ("src/", "tools/", "tests/", "breakers/")
    assert not any(p.startswith(forbidden) for p in files)

def case_b44(rt):
    files = _git_changed_files(RVO01_PARENT, RVO01_HEAD)
    assert all("strategy" not in p.lower() and "broker" not in p.lower() for p in files)
    report = (ROOT / "reports/program/2026-10-04-RVO-01-SEMANTIC-PERSISTENCE-ADVERSARIAL-CONTRACT-QUALIFICATION.md").read_text(encoding="utf-8")
    for marker in ("RVO_RUNTIME =\nNOT_IMPLEMENTED", "OOS_CONSUMPTION_AUTHORITY = NONE", "PAPER_BROKER_LIVE_CAPITAL_AUTHORITY = NONE"):
        assert marker in report

def case_b45(rt):
    semantics = rt.qualification_semantics()
    assert semantics["unknown_unknown_coverage"] == "NOT_CLAIMED"
    assert semantics["rvo_authority"] == "NONE"
    assert semantics["pass_grants_scientific_authority"] is False
    assert semantics["pass_grants_operational_authority"] is False

CASE_HANDLERS = {
    "RVO-B01": case_b01, "RVO-B02": case_b02, "RVO-B03": case_b03,
    "RVO-B04": case_b04, "RVO-B05": case_b05, "RVO-B06": case_b06,
    "RVO-B07": case_b07, "RVO-B08": case_b08, "RVO-B09": case_b09,
    "RVO-B10": case_b10, "RVO-B11": case_b11, "RVO-B12": case_b12,
    "RVO-B13": case_b13, "RVO-B14": case_b14, "RVO-B15": case_b15,
    "RVO-B16": case_b16, "RVO-B17": case_b17, "RVO-B18": case_b18,
    "RVO-B19": case_b19, "RVO-B20": case_b20, "RVO-B21": case_b21,
    "RVO-B22": case_b22, "RVO-B23": case_b23, "RVO-B24": case_b24,
    "RVO-B25": case_b25, "RVO-B26": case_b26, "RVO-B27": case_b27,
    "RVO-B28": case_b28, "RVO-B29": case_b29, "RVO-B30": case_b30,
    "RVO-B31": case_b31, "RVO-B32": case_b32, "RVO-B33": case_b33,
    "RVO-B34": case_b34, "RVO-B35": case_b35, "RVO-B36": case_b36,
    "RVO-B37": case_b37, "RVO-B38": case_b38, "RVO-B39": case_b39,
    "RVO-B40": case_b40, "RVO-B41": case_b41, "RVO-B42": case_b42,
    "RVO-B43": case_b43, "RVO-B44": case_b44, "RVO-B45": case_b45,
}

def test_frozen_case_inventory_matches_exact_rvo01_contract():
    assert FROZEN_CASE_IDS == EXPECTED_CASE_IDS
    assert tuple(CASE_HANDLERS) == EXPECTED_CASE_IDS
    assert len(CONTRACT["cases"]) == 45
    assert sum(item["severity"] == "CRITICAL" for item in CONTRACT["cases"]) == 24

def test_rvo_runtime_surface_exists_test_first_gate():
    rt = _runtime_or_none()
    assert rt is not None, (
        "RVO_RUNTIME_ABSENT: expected test-first RED before implementation; "
        "the frozen executable breaker exists but no RVO runtime is present"
    )

@pytest.mark.parametrize("case_id", EXPECTED_CASE_IDS)
def test_frozen_rvo01_case(case_id):
    rt = _runtime_or_none()
    if rt is None:
        pytest.skip("RVO_RUNTIME_ABSENT_TEST_FIRST_RED")
    CASE_HANDLERS[case_id](rt)
