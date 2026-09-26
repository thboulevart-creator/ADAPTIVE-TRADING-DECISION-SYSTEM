from __future__ import annotations

import json
import unittest
from pathlib import Path


class SemanticClassificationRuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(__file__).resolve().parents[2]
        cls.rules_path = (
            root
            / "tools"
            / "obsidian_projection"
            / "semantic_classification_rules_v0_1.json"
        )
        cls.inventory_path = (
            root
            / "tools"
            / "obsidian_projection"
            / "pilot_inventory_v0_1.json"
        )
        cls.rules = json.loads(
            cls.rules_path.read_text(encoding="utf-8")
        )
        cls.inventory = json.loads(
            cls.inventory_path.read_text(encoding="utf-8")
        )

    def test_rules_are_bound_to_frozen_pilot(self) -> None:
        self.assertEqual(
            self.rules["source_commit"],
            self.inventory["source_commit"],
        )
        self.assertEqual(
            self.rules["source_tree"],
            self.inventory["source_tree"],
        )
        self.assertEqual(
            self.rules["pilot_source_count"],
            self.inventory["source_artifact_count"],
        )
        self.assertEqual(self.rules["pilot_source_count"], 74)

    def test_filename_path_cannot_set_semantic_or_status_axes(self) -> None:
        forbidden = set(
            self.rules["path_filename_policy"][
                "forbidden_final_axes"
            ]
        )
        self.assertTrue(
            {
                "semantic_role",
                "procedure_role",
                "qualification_status",
                "qualification_scope",
                "scientific_status",
                "epistemic_role",
                "temporal_role",
                "limitations",
                "non_claims",
            }.issubset(forbidden)
        )

    def test_default_is_uncertainty_preserving(self) -> None:
        defaults = self.rules["defaults"]
        self.assertEqual(
            defaults["qualification_status"],
            "UNKNOWN",
        )
        self.assertEqual(
            defaults["scientific_status"],
            "UNKNOWN",
        )
        self.assertEqual(
            defaults["temporal_role"],
            "UNKNOWN",
        )

    def test_generic_pass_requires_terminal_verdict_and_scope(self) -> None:
        rule = self.rules["axis_rules"][
            "qualification_status"
        ]["generic_terminal_rule"]
        self.assertIn(
            "EXPLICIT_TERMINAL_VERDICT_BLOCK",
            rule["requires"],
        )
        self.assertIn(
            "QUALIFICATION_SCOPE_FROM_SAME_SOURCE",
            rule["requires"],
        )
        self.assertIn(
            "MACHINE_STATUS_ONLY",
            rule["forbids_as_sufficient"],
        )
        self.assertIn(
            "PROFILE_SELF_STATUS_ONLY",
            rule["forbids_as_sufficient"],
        )
        self.assertIn(
            "HANDOFF_REPORTED_VERDICT_ONLY",
            rule["forbids_as_sufficient"],
        )

    def test_pass_never_maps_to_supported(self) -> None:
        self.assertIn(
            "PASS -> SUPPORTED",
            self.rules["forbidden_promotions"],
        )
        scientific = self.rules["axis_rules"][
            "scientific_status"
        ]["rule"]
        self.assertIn(
            "qualification_status never maps",
            scientific,
        )

    def test_current_has_no_automatic_rule(self) -> None:
        current = self.rules["axis_rules"][
            "temporal_role"
        ]["current_rule"]
        self.assertFalse(current["automatic_assignment"])

    def test_exact_fixtures_are_bound_to_pilot_blobs(self) -> None:
        inventory_by_path = {
            item["source_path"]: item
            for item in self.inventory["entries"]
        }
        seen = set()

        for fixture in self.rules["exact_fixtures"]:
            path = fixture["source_path"]
            self.assertNotIn(path, seen)
            seen.add(path)
            self.assertIn(path, inventory_by_path)
            self.assertEqual(
                fixture["source_blob_sha"],
                inventory_by_path[path]["source_blob_sha"],
            )

    def test_pass_fixtures_have_bounded_scope_and_decision_procedure(self) -> None:
        allowed = {
            "ADJUDICATION",
            "PREFLIGHT",
            "ADVERSARIAL_REVIEW",
        }

        for fixture in self.rules["exact_fixtures"]:
            expected = fixture["expected"]
            if expected.get("qualification_status") == "PASS":
                self.assertIn(
                    expected["procedure_role"],
                    allowed,
                )
                self.assertTrue(
                    expected.get("qualification_scope")
                )

    def test_blocked_fixtures_are_exact_blob_exceptions(self) -> None:
        blocked = [
            fixture
            for fixture in self.rules["exact_fixtures"]
            if fixture["expected"].get(
                "qualification_status"
            )
            == "BLOCKED"
        ]
        self.assertEqual(
            {fixture["id"] for fixture in blocked},
            {
                "FX-AP5-R1-BLOCKED",
                "FX-AP5-R2-BLOCKED",
            },
        )
        for fixture in blocked:
            self.assertEqual(
                fixture.get("override_type"),
                "EXACT_BLOB_BOUNDED_EXCEPTION",
            )
            self.assertEqual(
                len(fixture["source_blob_sha"]),
                40,
            )

    def test_self_status_mutation_and_handoff_do_not_self_qualify(self) -> None:
        fixtures = {
            item["id"]: item["expected"]
            for item in self.rules["exact_fixtures"]
        }
        for fixture_id in (
            "FX-CORE-PROFILE-SELF-STATUS",
            "FX-AP4-MUTATION-RESULTS",
            "FX-AP6-SEAL",
            "FX-AP4-HISTORICAL-HANDOFF",
        ):
            self.assertEqual(
                fixtures[fixture_id][
                    "qualification_status"
                ],
                "UNKNOWN",
            )

    def test_historical_handoff_does_not_become_current(self) -> None:
        fixture = next(
            item
            for item in self.rules["exact_fixtures"]
            if item["id"]
            == "FX-AP4-HISTORICAL-HANDOFF"
        )
        self.assertEqual(
            fixture["expected"]["temporal_role"],
            "HISTORICAL",
        )
        self.assertEqual(
            fixture["expected"]["qualification_status"],
            "UNKNOWN",
        )

    def test_next_gate_does_not_authorize_renderer_or_vault(self) -> None:
        gate = self.rules["next_action_gate"]
        self.assertEqual(
            gate["allowed_after_persisted_rebreak"],
            "P1_CLASSIFIER_IMPLEMENTATION_CANDIDATE",
        )
        self.assertFalse(gate["renderer_authorized"])
        self.assertFalse(gate["vault_authorized"])
        self.assertFalse(gate["relations_authorized"])


if __name__ == "__main__":
    unittest.main()
