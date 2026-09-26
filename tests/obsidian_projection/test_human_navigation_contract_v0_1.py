from __future__ import annotations

import json
import unittest
from pathlib import Path


class P4AHumanNavigationContractTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "human_navigation_contract_v0_1.json"
        )
        cls.contract = json.loads(
            cls.path.read_text(encoding="utf-8")
        )

    def test_schema_is_exact(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_HUMAN_NAVIGATION_CONTRACT_V0_1",
        )

    def test_status_is_candidate_only(self) -> None:
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )

    def test_predecessor_is_exact_p3d2_closure(self) -> None:
        self.assertEqual(
            self.contract[
                "predecessor_p3d2_closure_head"
            ],
            "4660a3e5daa57f38175d403b1a1fecef257796af",
        )

    def test_projection_digest_is_bound(self) -> None:
        self.assertEqual(
            self.contract["qualified_projection"][
                "projection_tree_digest_sha256"
            ],
            "bf67fb65d42de58f394a21a884ca180665b3ba550be101ac2d410b0aa425e2e0",
        )

    def test_projection_count_is_bound(self) -> None:
        self.assertEqual(
            self.contract["qualified_projection"][
                "generated_file_count"
            ],
            92,
        )

    def test_canonical_truth_remains_github(self) -> None:
        self.assertEqual(
            self.contract["authority_boundary"][
                "canonical_truth"
            ],
            "GitHub/ATDS",
        )

    def test_generated_remains_derived_machine_owned(
        self,
    ) -> None:
        self.assertEqual(
            self.contract["authority_boundary"][
                "generated_role"
            ],
            "DERIVED_MACHINE_OWNED",
        )

    def test_views_are_non_authoritative(self) -> None:
        boundary = self.contract[
            "authority_boundary"
        ]
        self.assertEqual(
            boundary["views_role"],
            "VIEW_HUMAN_OWNED_NON_AUTHORITATIVE",
        )
        self.assertIn(
            "QUALIFY",
            boundary["forbidden_authority"],
        )
        self.assertIn(
            "CHANGE_CANONICAL_TRUTH",
            boundary["forbidden_authority"],
        )

    def test_p4a_itself_cannot_write_vault(self) -> None:
        p4a = self.contract["p4a_boundary"]
        for key in (
            "vault_write_authorized",
            "generated_write_authorized",
            "views_write_authorized",
            "obsidian_config_write_authorized",
        ):
            with self.subTest(key=key):
                self.assertFalse(p4a[key])

    def test_p4a_cannot_change_p2(self) -> None:
        self.assertFalse(
            self.contract["p4a_boundary"][
                "p2_builder_change_authorized"
            ]
        )

    def test_native_first_has_no_plugin_dependency(
        self,
    ) -> None:
        native = self.contract["native_first"]
        self.assertTrue(native["required"])
        self.assertFalse(
            native["dataview_authorized"]
        )
        self.assertFalse(
            native["excalidraw_authorized"]
        )
        self.assertFalse(
            native["tasks_plugin_authorized"]
        )
        self.assertFalse(
            native["custom_javascript_authorized"]
        )
        self.assertFalse(
            native["custom_css_authorized"]
        )

    def test_sync_and_git_automation_are_forbidden(
        self,
    ) -> None:
        p4a = self.contract["p4a_boundary"]
        self.assertFalse(
            p4a["obsidian_sync_authorized"]
        )
        self.assertFalse(
            p4a["git_automation_authorized"]
        )

    def test_views_are_not_semantic_input(self) -> None:
        views = self.contract["view_root_policy"]
        self.assertFalse(
            views[
                "p2_builder_may_consume_as_semantic_input"
            ]
        )
        self.assertFalse(
            views["p2_builder_may_write"]
        )

    def test_seed_requires_empty_views(self) -> None:
        views = self.contract["view_root_policy"]
        self.assertTrue(
            views[
                "initial_seed_requires_empty_views"
            ]
        )
        self.assertFalse(
            views["automatic_overwrite_after_seed"]
        )
        self.assertEqual(
            views[
                "unexpected_existing_target_result"
            ],
            "BLOCK",
        )

    def test_navigation_links_are_not_semantic(
        self,
    ) -> None:
        nav = self.contract[
            "navigation_semantics"
        ]
        self.assertEqual(
            nav["wikilinks_are"],
            "NAVIGATION_ONLY",
        )
        self.assertEqual(
            nav["backlinks_are"],
            "NAVIGATION_ONLY",
        )
        self.assertFalse(
            nav[
                "filename_similarity_is_semantic_relation"
            ]
        )
        self.assertFalse(
            nav[
                "directory_proximity_is_semantic_relation"
            ]
        )
        self.assertFalse(
            nav[
                "chronology_alone_is_semantic_relation"
            ]
        )

    def test_canvas_edges_default_to_navigation_only(
        self,
    ) -> None:
        nav = self.contract[
            "navigation_semantics"
        ]
        self.assertEqual(
            nav["canvas_edges_are"],
            (
                "NAVIGATION_ONLY_UNLESS_BACKED_BY_"
                "GENERATED_RELATION"
            ),
        )

    def test_generated_relations_remain_authority(
        self,
    ) -> None:
        self.assertEqual(
            self.contract[
                "navigation_semantics"
            ][
                "generated_relation_authority_source"
            ],
            "generated/relations",
        )
        self.assertTrue(
            self.contract[
                "navigation_semantics"
            ][
                "inferred_relation_promotion_forbidden"
            ]
        )

    def test_epistemic_axes_must_remain_separate(
        self,
    ) -> None:
        rules = self.contract[
            "epistemic_display_rules"
        ]
        self.assertTrue(
            rules[
                "qualification_status_and_scientific_status_must_remain_separate"
            ]
        )
        self.assertTrue(
            rules[
                "unknown_must_not_be_silently_omitted"
            ]
        )
        self.assertTrue(
            rules[
                "blocked_must_not_be_rendered_as_failed"
            ]
        )
        self.assertTrue(
            rules["pass_must_preserve_scope"]
        )

    def test_no_synthetic_health_or_quality_score(
        self,
    ) -> None:
        rules = self.contract[
            "epistemic_display_rules"
        ]
        self.assertTrue(
            rules["no_overall_health_score"]
        )
        self.assertTrue(
            rules[
                "no_rankings_or_synthetic_quality_grade"
            ]
        )

    def test_freshness_is_snapshot_bound(self) -> None:
        freshness = self.contract[
            "freshness_model"
        ]
        self.assertEqual(
            freshness["mode"],
            "SNAPSHOT_BOUND",
        )
        self.assertEqual(
            freshness[
                "initial_required_value"
            ],
            "BOUND",
        )
        self.assertEqual(
            freshness[
                "digest_mismatch_result"
            ],
            "STALE_NOT_CURRENT",
        )
        self.assertFalse(
            freshness[
                "stale_view_may_claim_current"
            ]
        )

    def test_initial_bundle_is_exactly_seven_files(
        self,
    ) -> None:
        info = self.contract[
            "initial_information_architecture"
        ]
        required = info["required_files"]
        self.assertEqual(len(required), 7)
        self.assertEqual(
            info["max_initial_files"],
            7,
        )
        self.assertEqual(
            len(required),
            len(set(required)),
        )

    def test_initial_bundle_paths_are_exact(self) -> None:
        required = set(
            self.contract[
                "initial_information_architecture"
            ]["required_files"]
        )
        self.assertEqual(
            required,
            {
                "views/HOME.md",
                (
                    "views/dashboards/"
                    "PROJECT-SNAPSHOT.md"
                ),
                (
                    "views/dashboards/"
                    "QUALIFICATION-STATUS.md"
                ),
                (
                    "views/maps/"
                    "SYSTEM-ARCHITECTURE.md"
                ),
                "views/maps/GOVERNANCE.md",
                (
                    "views/maps/"
                    "RESEARCH-LIFECYCLE.md"
                ),
                (
                    "views/canvas/"
                    "ATDS-OVERVIEW.canvas"
                ),
            },
        )

    def test_markdown_metadata_preserves_non_authority(
        self,
    ) -> None:
        md = self.contract[
            "markdown_view_contract"
        ]
        self.assertEqual(
            md["fixed_values"][
                "authority_role"
            ],
            "VIEW",
        )
        self.assertEqual(
            md["fixed_values"][
                "semantic_authority"
            ],
            "NONE",
        )
        self.assertTrue(
            md["source_body_copy_forbidden"]
        )

    def test_canvas_has_no_external_dependency(
        self,
    ) -> None:
        canvas = self.contract[
            "canvas_contract"
        ]
        self.assertTrue(
            canvas[
                "native_obsidian_canvas_only"
            ]
        )
        self.assertTrue(
            canvas[
                "external_url_nodes_forbidden_initially"
            ]
        )
        self.assertTrue(
            canvas[
                "embedded_files_outside_vault_forbidden"
            ]
        )

    def test_dashboard_axes_are_explicit(self) -> None:
        axes = self.contract[
            "dashboard_contract"
        ]["display_axes"]

        for required in (
            "source_authority_role",
            "qualification_status",
            "scientific_status",
            "epistemic_role",
            "temporal_role",
            "persistence_state",
        ):
            with self.subTest(required=required):
                self.assertIn(required, axes)

        self.assertTrue(
            self.contract[
                "dashboard_contract"
            ][
                "axes_must_not_be_collapsed_into_one_status"
            ]
        )

    def test_p4b_write_scope_is_views_only(
        self,
    ) -> None:
        p4b = self.contract[
            "p4b_candidate_boundary"
        ]
        self.assertEqual(
            p4b["next_gate"],
            (
                "P4B_NATIVE_VIEW_BUNDLE_"
                "IMPLEMENTATION_CANDIDATE"
            ),
        )
        self.assertTrue(
            p4b["may_write_only_views"]
        )
        self.assertTrue(
            p4b[
                "may_write_only_if_views_empty"
            ]
        )
        self.assertTrue(
            p4b["may_not_modify_generated"]
        )
        self.assertTrue(
            p4b["may_not_modify_obsidian_config"]
        )

    def test_p4b_requires_digest_and_post_write_verify(
        self,
    ) -> None:
        p4b = self.contract[
            "p4b_candidate_boundary"
        ]
        self.assertTrue(
            p4b[
                "must_verify_projection_digest_before_write"
            ]
        )
        self.assertTrue(
            p4b[
                "must_verify_written_bundle_after_write"
            ]
        )
        self.assertTrue(
            p4b[
                "must_leave_repository_state_unchanged"
            ]
        )

    def test_breaker_registry_is_unique_and_sufficient(
        self,
    ) -> None:
        breakers = self.contract[
            "acceptance_breakers"
        ]
        self.assertGreaterEqual(
            len(breakers),
            20,
        )
        self.assertEqual(
            len(breakers),
            len(set(breakers)),
        )


if __name__ == "__main__":
    unittest.main()
