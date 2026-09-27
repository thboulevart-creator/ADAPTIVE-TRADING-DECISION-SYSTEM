from __future__ import annotations

import json
import unittest
from pathlib import Path


class CurrentHeadProjectionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "current_head_projection_contract_v0_1.json"
        )
        cls.contract = json.loads(
            cls.path.read_text(encoding="utf-8")
        )

    def test_schema_status_repository_branch(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_CURRENT_HEAD_PROJECTION_CONTRACT_V0_1",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )
        self.assertEqual(
            self.contract["source_repository"],
            "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
        )
        self.assertEqual(
            self.contract["source_branch"],
            "integration/system-v1",
        )

    def test_p5d3b_and_p5d3c2_are_pinned(self) -> None:
        p = self.contract["qualified_predecessors"]
        self.assertEqual(
            p["p5d3b_qualification_commit"],
            "51dfa30a9fcca4f012f80410f24f95007d2cf2e6",
        )
        self.assertEqual(
            p["p5d3b_bridge_contract_blob"],
            "7015db1206cd40b703795d12519707a6455b4fc3",
        )
        self.assertEqual(
            p["p5d3b_bridge_implementation_blob"],
            "ff3c2dd232487594a5283a9ab7750780ac098f2d",
        )
        self.assertEqual(
            p["p5d3c2_qualification_commit"],
            "205d09e22430e60324b76f2713024e36527e5dba",
        )

    def test_objective_removes_pilot_authority(self) -> None:
        o = self.contract["objective"]
        self.assertTrue(o["one_artifact_per_bridge_entry"])
        self.assertTrue(o["fixed_source_count_forbidden"])
        self.assertTrue(o["pilot_inventory_semantics_forbidden"])
        self.assertTrue(o["frozen_inventory_conversion_forbidden"])
        self.assertTrue(o["source_body_copying_forbidden"])

    def test_bridge_input_identity_is_exact(self) -> None:
        i = self.contract["input_contract"]
        self.assertEqual(
            i["required_bridge_schema"],
            "ATDS_OBSIDIAN_CURRENT_HEAD_SEMANTIC_BRIDGE_RESULT_V0_1",
        )
        self.assertTrue(i["bridge_source_commit_is_candidate_head"])
        self.assertTrue(i["bridge_source_tree_is_candidate_tree"])
        self.assertTrue(i["bridge_dynamic_inventory_digest_required"])
        self.assertTrue(i["bridge_entry_digest_required"])
        self.assertTrue(i["semantic_record_digest_required"])
        self.assertTrue(i["artifact_count_must_equal_bridge_entry_count"])
        self.assertTrue(i["empty_bridge_forbidden"])

    def test_body_read_policy_is_default_deny(self) -> None:
        b = self.contract["body_read_authority"]
        self.assertEqual(b["default"], "DENY")
        self.assertFalse(b["metadata_only_body_read_allowed"])
        self.assertFalse(b["artifact_render_body_read_allowed"])
        self.assertFalse(b["full_text_non_relation_suffix_body_read_allowed"])
        self.assertFalse(b["metadata_only_may_be_relation_source"])
        self.assertTrue(b["metadata_only_may_be_relation_target"])
        self.assertEqual(
            b["relation_body_read_allowed_only_when"]["source_suffix_in"],
            [".md", ".json"],
        )
        self.assertEqual(
            b["metadata_only_body_read_count_must_equal"],
            0,
        )

    def test_artifact_renderer_reuse_is_metadata_only(self) -> None:
        a = self.contract["artifact_projection"]
        self.assertTrue(a["reuse_legacy_renderer_allowed"])
        self.assertTrue(a["body_must_not_include_source_blob_bytes"])
        self.assertEqual(
            a["artifact_record_schema"],
            "ATDS_OBSIDIAN_ARTIFACT_V0_1",
        )
        self.assertEqual(
            a["fixed_projection_authority_role"],
            "DERIVED",
        )

    def test_legacy_relation_extractor_is_forbidden(self) -> None:
        r = self.contract["relation_projection"]
        self.assertFalse(
            r["legacy_extract_relations_direct_reuse_allowed"]
        )
        self.assertTrue(
            r["reuse_legacy_relation_renderer_allowed"]
        )
        self.assertEqual(
            r["allowed_relation_types"],
            ["REFERENCES"],
        )
        self.assertEqual(
            r["allowed_basis"],
            ["EXPLICIT_STRUCTURED", "EXPLICIT_TEXT"],
        )
        self.assertIn(
            "DERIVED_BY_RULE",
            r["forbidden_authoritative_basis"],
        )

    def test_relation_sources_and_targets_preserve_metadata_boundary(
        self,
    ) -> None:
        r = self.contract["relation_projection"]
        self.assertEqual(
            r["source_policy"]["metadata_only"],
            "NO_BODY_READ_NO_RELATION",
        )
        self.assertEqual(
            r["source_policy"]["other_full_text_suffix"],
            "NO_BODY_READ_NO_RELATION",
        )
        self.assertTrue(
            r["target_policy"]["metadata_only_target_allowed"]
        )
        self.assertTrue(
            r["target_policy"][
                "target_must_equal_exact_source_path_of_any_bridge_entry"
            ]
        )
        self.assertTrue(
            r["target_policy"]["guessing_forbidden"]
        )

    def test_current_head_relation_rules_are_only_two_explicit_rules(
        self,
    ) -> None:
        rules = self.contract["relation_projection"][
            "preregistered_rules"
        ]
        self.assertEqual(
            [item["rule_id"] for item in rules],
            [
                "CH-REL-V0-EXACT-STRUCTURED-PATH",
                "CH-REL-V0-EXPLICIT-LABELED-TEXT-PATH",
            ],
        )
        self.assertEqual(
            {item["relation_type"] for item in rules},
            {"REFERENCES"},
        )

    def test_build_manifest_replaces_pilot_identity(self) -> None:
        m = self.contract["build_manifest"]
        fields = m["field_order"]
        for required in (
            "source_branch",
            "dynamic_inventory_digest_sha256",
            "semantic_bridge_digest_sha256",
            "semantic_record_digest_sha256",
            "full_text_count",
            "metadata_only_count",
            "relation_source_body_read_count",
            "metadata_only_body_read_count",
            "body_read_audit_digest_sha256",
        ):
            with self.subTest(required=required):
                self.assertIn(required, fields)
        self.assertIn(
            "pilot_inventory_digest_sha256",
            m["forbidden_fields"],
        )
        self.assertNotIn(
            "pilot_inventory_digest_sha256",
            fields,
        )
        self.assertEqual(
            m["required_values"]["metadata_only_body_read_count"],
            0,
        )

    def test_determinism_requires_exact_double_build(self) -> None:
        d = self.contract["determinism"]
        self.assertEqual(d["independent_build_count"], 2)
        self.assertTrue(d["separate_fresh_stage_roots_required"])
        for required in (
            "each_file_bytes",
            "each_file_sha256",
            "body_read_audit_digest_sha256",
            "projection_tree_digest_sha256",
            "generated_file_count",
        ):
            self.assertIn(
                required,
                d["required_equalities"],
            )
        self.assertTrue(d["any_mismatch_is_candidate_rejection"])

    def test_failure_semantics_keep_candidate_and_infra_distinct(
        self,
    ) -> None:
        f = self.contract["failure_semantics"]
        self.assertTrue(
            f["candidate_invalid_must_not_be_relabelled_blocked"]
        )
        self.assertTrue(
            f[
                "infrastructure_blocked_must_not_be_relabelled_candidate_invalid_without_candidate_evidence"
            ]
        )
        self.assertIn(
            "METADATA_ONLY_BODY_READ_ATTEMPT",
            f["candidate_invalid_examples"],
        )
        self.assertIn(
            "SOURCE_BLOB_READ_UNAVAILABLE",
            f["infrastructure_blocked_examples"],
        )

    def test_contract_boundary_authorizes_no_runtime_yet(self) -> None:
        b = self.contract["execution_boundary"]
        self.assertTrue(b["contract_only_until_qualified"])
        for field in (
            "current_head_builder_implementation_authorized",
            "current_head_relation_adapter_implementation_authorized",
            "current_head_build_execution_authorized",
            "real_vault_creation_authorized",
            "current_pointer_mutation_authorized",
            "production_promotion_authorized",
            "background_execution_authorized",
            "polling_authorized",
        ):
            with self.subTest(field=field):
                self.assertFalse(b[field])

    def test_next_gate_allows_implementation_but_not_promotion(
        self,
    ) -> None:
        g = self.contract["next_action_gate"]
        self.assertEqual(
            g["after_contract_qualification"],
            "P5_D3D_IMPLEMENTATION_CANDIDATE",
        )
        self.assertTrue(
            g["current_head_builder_implementation_allowed"]
        )
        self.assertTrue(
            g["current_head_relation_adapter_implementation_allowed"]
        )
        self.assertTrue(
            g["finite_orchestrator_implementation_allowed"]
        )
        self.assertFalse(g["real_vault_creation_allowed"])
        self.assertFalse(g["current_pointer_mutation_allowed"])
        self.assertFalse(g["production_promotion_allowed"])

    def test_projection_breaker_registry_is_large_and_unique(
        self,
    ) -> None:
        breakers = self.contract["required_breakers"]
        self.assertGreaterEqual(len(breakers), 70)
        self.assertEqual(len(breakers), len(set(breakers)))


if __name__ == "__main__":
    unittest.main()
