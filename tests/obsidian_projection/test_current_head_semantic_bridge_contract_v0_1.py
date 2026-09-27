from __future__ import annotations

import json
import unittest
from pathlib import Path


class P5D3BCurrentHeadSemanticBridgeContractTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "current_head_semantic_bridge_contract_v0_1.json"
        )
        cls.contract = json.loads(
            cls.path.read_text(encoding="utf-8")
        )

    def test_schema_and_status_are_exact(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            (
                "ATDS_OBSIDIAN_"
                "CURRENT_HEAD_SEMANTIC_BRIDGE_CONTRACT_V0_1"
            ),
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )

    def test_p5d3a_and_p5b2_are_pinned(self) -> None:
        p = self.contract["qualified_predecessors"]
        self.assertEqual(
            p["p5d3a_qualification_commit"],
            "d1198a5b7e32607d2a2ef46084f6d11bca36b3e2",
        )
        self.assertEqual(
            p["p5d3a_qualification_report_blob"],
            "bf8c5e917b08a6a1b1de7fdd7c0098a5969bfb87",
        )
        self.assertEqual(
            p["p5b2_dynamic_inventory_contract_blob"],
            "80729156f4ac51b760c4347f581f052a175b88b3",
        )
        self.assertEqual(
            p["p5b2_dynamic_inventory_implementation_blob"],
            "5f6ed61f36e889dc27ef14ef09467ada9f9f0f58",
        )

    def test_bridge_is_pure_and_count_free(self) -> None:
        objective = self.contract["objective"]
        self.assertTrue(objective["pure_in_memory"])
        self.assertTrue(
            objective["body_read_forbidden_in_bridge_v0_1"]
        )
        self.assertTrue(objective["network_io_forbidden"])
        self.assertTrue(objective["filesystem_io_forbidden"])
        self.assertTrue(objective["process_launch_forbidden"])
        self.assertTrue(objective["fixed_source_count_forbidden"])
        self.assertTrue(
            objective[
                "frozen_pilot_inventory_dependency_forbidden"
            ]
        )

    def test_input_is_exact_dynamic_inventory(self) -> None:
        input_contract = self.contract["input_contract"]
        self.assertEqual(
            input_contract["python_type"],
            "DynamicInventory",
        )
        self.assertEqual(
            input_contract["schema"],
            "ATDS_OBSIDIAN_DYNAMIC_INVENTORY_V0_1",
        )
        self.assertEqual(
            input_contract["repository_exact"],
            (
                "thboulevart-creator/"
                "ADAPTIVE-TRADING-DECISION-SYSTEM"
            ),
        )
        self.assertEqual(
            input_contract["branch_exact"],
            "integration/system-v1",
        )
        self.assertTrue(
            input_contract[
                "inventory_digest_recomputed_and_bound"
            ]
        )

    def test_output_is_one_to_one(self) -> None:
        output = self.contract["bridge_output"]
        self.assertTrue(
            output["one_output_entry_per_input_entry"]
        )
        self.assertTrue(
            output[
                "source_blob_count_must_equal_output_entry_count"
            ]
        )
        self.assertTrue(
            output[
                "semantic_record_count_must_equal_output_entry_count"
            ]
        )
        self.assertTrue(output["no_silent_drop"])

    def test_dispositions_are_exact(self) -> None:
        policy = self.contract["disposition_policy"]
        self.assertEqual(
            policy["FULL_TEXT"],
            "SEMANTIC_FULL_TEXT",
        )
        self.assertEqual(
            policy["METADATA_ONLY"],
            "SEMANTIC_METADATA_ONLY",
        )
        self.assertFalse(policy["excluded_by_default"])

    def test_artifact_family_never_uses_selection_zone(
        self,
    ) -> None:
        policy = self.contract["artifact_family_policy"]
        self.assertTrue(
            policy[
                "selection_zone_may_not_determine_artifact_family"
            ]
        )
        self.assertTrue(
            policy[
                "selection_zone_may_not_determine_semantic_axes"
            ]
        )
        self.assertTrue(
            policy["path_zone_equivalence_to_family_forbidden"]
        )
        self.assertEqual(
            policy["basis"],
            "EXPLICIT_EXTENSION_ONLY_PHYSICAL_CLASSIFICATION",
        )

    def test_extension_registry_is_explicit(self) -> None:
        registry = self.contract[
            "artifact_family_policy"
        ]["full_text_extension_registry"]
        self.assertEqual(registry[".md"], "DOCUMENT")
        self.assertEqual(registry[".py"], "CODE")
        self.assertEqual(
            registry[".json"],
            "STRUCTURED_DATA",
        )
        self.assertEqual(registry[".txt"], "TEXT")
        self.assertEqual(registry[".html"], "WEB_ASSET")

    def test_semantic_defaults_are_conservative(self) -> None:
        policy = self.contract["semantic_record_policy"]
        self.assertEqual(policy["semantic_role"], "UNKNOWN")
        self.assertEqual(policy["procedure_role"], "NONE")
        self.assertEqual(
            policy["qualification_status"],
            "UNKNOWN",
        )
        self.assertIsNone(policy["qualification_scope"])
        self.assertEqual(
            policy["scientific_status"],
            "UNKNOWN",
        )
        self.assertEqual(
            policy["epistemic_role"],
            "UNKNOWN",
        )
        self.assertEqual(
            policy["temporal_role"],
            "UNKNOWN",
        )
        self.assertTrue(
            policy[
                "body_derived_semantic_promotion_in_v0_1_forbidden"
            ]
        )

    def test_metadata_only_never_allows_body_semantics(
        self,
    ) -> None:
        safety = self.contract["metadata_only_safety"]
        self.assertFalse(safety["semantic_body_read"])
        self.assertFalse(
            safety["downstream_body_read_allowed"]
        )
        self.assertTrue(
            safety["relation_extraction_from_body_forbidden"]
        )
        self.assertTrue(safety["content_decode_forbidden"])
        self.assertTrue(
            safety[
                "semantic_axes_must_remain_conservative_defaults"
            ]
        )

    def test_full_text_bridge_still_does_not_read_body(
        self,
    ) -> None:
        safety = self.contract["full_text_safety"]
        self.assertFalse(
            safety["semantic_body_read_in_bridge_v0_1"]
        )
        self.assertTrue(
            safety["downstream_body_read_allowed"]
        )
        self.assertTrue(
            safety[
                "semantic_axes_must_remain_conservative_defaults_in_v0_1"
            ]
        )

    def test_provenance_is_preserved(self) -> None:
        p = self.contract["provenance_invariants"]
        for field in (
            "source_path_preserved_exactly",
            "source_blob_sha_preserved_exactly",
            "source_blob_size_preserved_exactly",
            "git_mode_preserved_exactly",
            "selection_zone_preserved_exactly_as_nonsemantic_provenance",
            "content_mode_preserved_exactly",
            "source_commit_preserved_exactly",
            "source_tree_preserved_exactly",
            "repository_preserved_exactly",
            "branch_preserved_exactly",
        ):
            with self.subTest(field=field):
                self.assertTrue(p[field])

    def test_digest_model_binds_bridge_semantics(self) -> None:
        d = self.contract["digest_model"]
        self.assertEqual(d["algorithm"], "SHA256")
        self.assertTrue(
            d["selection_zone_included_in_bridge_entry_digest"]
        )
        self.assertTrue(
            d["content_mode_included_in_bridge_entry_digest"]
        )
        self.assertTrue(
            d["disposition_included_in_bridge_entry_digest"]
        )
        self.assertTrue(
            d["semantic_record_included_in_bridge_entry_digest"]
        )
        self.assertTrue(d["volatile_host_data_forbidden"])

    def test_legacy_classifier_is_explicitly_not_reused(
        self,
    ) -> None:
        legacy = self.contract[
            "legacy_classifier_non_reuse_reason"
        ]
        self.assertEqual(
            legacy["status"],
            "NOT_APPLICABLE_TO_DYNAMIC_CURRENT_HEAD_V0_1",
        )
        self.assertTrue(
            legacy[
                "current_head_bridge_may_import_semantic_record_dataclass"
            ]
        )
        self.assertTrue(
            legacy[
                "current_head_bridge_may_reuse_records_digest_function"
            ]
        )
        self.assertFalse(
            legacy["current_head_bridge_may_call_classify_inventory"]
        )
        self.assertFalse(
            legacy["current_head_bridge_may_call_classify_record"]
        )
        self.assertFalse(
            legacy[
                "current_head_bridge_may_load_semantic_classification_rules_v0_1"
            ]
        )

    def test_legacy_relation_extractor_is_not_metadata_safe(
        self,
    ) -> None:
        boundary = self.contract[
            "legacy_relation_extractor_boundary"
        ]
        self.assertEqual(
            boundary["status"],
            "NOT_SAFE_FOR_UNFILTERED_BRIDGE_OUTPUT",
        )
        self.assertTrue(
            boundary[
                "metadata_only_records_must_not_be_passed_to_legacy_body_relation_extractor"
            ]
        )
        self.assertTrue(
            boundary[
                "future_relation_adapter_must_filter_or_use_content_mode_aware_rules"
            ]
        )

    def test_legacy_builder_is_not_current_head_qualified(
        self,
    ) -> None:
        boundary = self.contract[
            "legacy_builder_boundary"
        ]
        self.assertEqual(
            boundary["status"],
            "NOT_YET_CURRENT_HEAD_QUALIFIED",
        )
        self.assertTrue(
            boundary[
                "bridge_output_may_not_be_fed_blindly_to_legacy_builder"
            ]
        )
        self.assertTrue(
            boundary[
                "current_head_builder_adaptation_requires_separate_governed_change"
            ]
        )

    def test_failure_model_is_fail_closed(self) -> None:
        failure = self.contract["failure_model"]
        self.assertTrue(failure["partial_output_forbidden"])
        for field in (
            "invalid_inventory",
            "invalid_entry",
            "unsupported_full_text_extension",
            "duplicate_source_path",
            "unsorted_input_entries",
        ):
            with self.subTest(field=field):
                self.assertIn(
                    "ERROR_NO_OUTPUT",
                    failure[field],
                )

    def test_p5d3b_runtime_boundary_is_narrow(self) -> None:
        boundary = self.contract["p5d3b_boundary"]
        self.assertTrue(
            boundary["pure_bridge_implementation_authorized"]
        )
        for field in (
            "body_semantic_enrichment_authorized",
            "network_fetch_authorized",
            "filesystem_source_read_authorized",
            "legacy_frozen_inventory_conversion_authorized",
            "legacy_classifier_execution_authorized",
            "legacy_relation_extractor_execution_authorized",
            "projection_builder_execution_authorized",
            "candidate_generation_staging_authorized",
            "evaluation_orchestrator_authorized",
            "real_vault_write_authorized",
            "production_promotion_authorized",
            "background_observer_authorized",
            "polling_loop_authorized",
            "graph_search_current_semantics_authorized",
        ):
            with self.subTest(field=field):
                self.assertFalse(boundary[field])

    def test_real_head_qualification_harness_is_bounded(
        self,
    ) -> None:
        harness = self.contract[
            "qualification_harness"
        ]
        self.assertTrue(
            harness["may_reuse_p5b2_build_from_repository"]
        )
        self.assertTrue(
            harness["exact_source_head_required"]
        )
        self.assertTrue(
            harness["exact_source_tree_required"]
        )
        self.assertTrue(
            harness[
                "observed_remote_head_must_equal_source_head"
            ]
        )
        self.assertTrue(harness["control_clone_required"])
        self.assertTrue(
            harness["canonical_worktree_write_forbidden"]
        )
        self.assertTrue(
            harness["real_vault_write_forbidden"]
        )
        self.assertTrue(
            harness["projection_write_forbidden"]
        )
        self.assertTrue(
            harness[
                "source_body_bytes_in_report_forbidden"
            ]
        )
        self.assertTrue(
            harness["fixed_expected_source_count_forbidden"]
        )
        self.assertGreaterEqual(
            len(harness["required_summary_checks"]),
            10,
        )

    def test_breaker_registry_is_broad_and_unique(
        self,
    ) -> None:
        breakers = self.contract["required_breakers"]
        self.assertGreaterEqual(len(breakers), 70)
        self.assertEqual(
            len(breakers),
            len(set(breakers)),
        )

    def test_next_gates_remain_ordered(self) -> None:
        gates = self.contract["next_gates"]
        self.assertEqual(
            list(gates.keys()),
            [
                "p5d3c",
                "p5d3d",
                "p5d3e",
                "p5d4",
                "p5e",
                "p6",
            ],
        )


if __name__ == "__main__":
    unittest.main()
