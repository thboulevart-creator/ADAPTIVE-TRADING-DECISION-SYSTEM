from __future__ import annotations

import ast
import unittest
from pathlib import Path


class P5D3DAdversarialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]

        cls.relations_path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "current_head_relations.py"
        )
        cls.projection_path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "current_head_projection.py"
        )
        cls.breakers_path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "current_head_breakers.py"
        )
        cls.evaluator_path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "finite_candidate_evaluator.py"
        )
        cls.harness_path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "p5d3d_verify.py"
        )

        cls.relations = cls.relations_path.read_text(
            encoding="utf-8"
        )
        cls.projection = cls.projection_path.read_text(
            encoding="utf-8"
        )
        cls.breakers = cls.breakers_path.read_text(
            encoding="utf-8"
        )
        cls.evaluator = cls.evaluator_path.read_text(
            encoding="utf-8"
        )
        cls.harness = cls.harness_path.read_text(
            encoding="utf-8"
        )

        cls.relations_tree = ast.parse(
            cls.relations
        )
        cls.projection_tree = ast.parse(
            cls.projection
        )
        cls.evaluator_tree = ast.parse(
            cls.evaluator
        )
        cls.harness_tree = ast.parse(
            cls.harness
        )

    def test_implementation_pins_qualified_contracts(
        self,
    ) -> None:
        self.assertIn(
            "6bc5286367890a8c393e4f5bea2b4ecb0fb20af2",
            self.relations,
        )
        self.assertIn(
            "6bc5286367890a8c393e4f5bea2b4ecb0fb20af2",
            self.projection,
        )
        self.assertIn(
            "b6c17167875874db30a575be95e8e6aa33d630dd",
            self.breakers,
        )
        self.assertIn(
            "b6c17167875874db30a575be95e8e6aa33d630dd",
            self.evaluator,
        )
        self.assertIn(
            "c2d0323df53c40c8818d7f8d9805210e1961116e",
            self.projection,
        )
        self.assertIn(
            "c2d0323df53c40c8818d7f8d9805210e1961116e",
            self.evaluator,
        )

    def test_no_legacy_builder_or_relation_extractor_reuse(
        self,
    ) -> None:
        combined = (
            self.relations
            + self.projection
            + self.evaluator
        )
        for forbidden in (
            "build_projection_from_records",
            "extract_relations(",
            "FrozenInventory",
            "classify_inventory",
            "pilot_inventory_digest_sha256=",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    combined,
                )

    def test_projection_builder_never_reads_source_blob_directly(
        self,
    ) -> None:
        self.assertNotIn(
            "source.read_blob(",
            self.projection,
        )
        self.assertIn(
            "extract_current_head_relations(",
            self.projection,
        )

    def test_relation_adapter_has_single_blob_read_site(
        self,
    ) -> None:
        self.assertEqual(
            self.relations.count(
                "source.read_blob("
            ),
            1,
        )
        target = next(
            node
            for node in self.relations_tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "_read_eligible_blob"
        )
        source = (
            ast.get_source_segment(
                self.relations,
                target,
            )
            or ""
        )
        self.assertIn(
            "source.read_blob(",
            source,
        )

    def test_relation_adapter_skips_metadata_and_nonrelation_suffixes(
        self,
    ) -> None:
        target = next(
            node
            for node in self.relations_tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name
            == "extract_current_head_relations"
        )
        source = (
            ast.get_source_segment(
                self.relations,
                target,
            )
            or ""
        )
        self.assertIn(
            'entry.content_mode == "METADATA_ONLY"',
            source,
        )
        self.assertIn(
            'suffix not in {".md", ".json"}',
            source,
        )
        self.assertLess(
            source.index(
                'entry.content_mode == "METADATA_ONLY"'
            ),
            source.index(
                "_read_eligible_blob("
            ),
        )
        self.assertLess(
            source.index(
                'suffix not in {".md", ".json"}'
            ),
            source.index(
                "_read_eligible_blob("
            ),
        )

    def test_evaluator_imports_no_network_or_process_runtime(
        self,
    ) -> None:
        imported: set[str] = set()
        for node in ast.walk(self.evaluator_tree):
            if isinstance(node, ast.Import):
                imported.update(
                    alias.name.split(".", 1)[0]
                    for alias in node.names
                )
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported.add(
                        node.module.split(".", 1)[0]
                    )

        forbidden = {
            "subprocess",
            "socket",
            "urllib",
            "requests",
            "http",
            "asyncio",
            "threading",
            "multiprocessing",
            "winreg",
            "ctypes",
        }
        self.assertEqual(
            imported & forbidden,
            set(),
        )

    def test_evaluator_contains_no_checkout_or_network_command(
        self,
    ) -> None:
        for forbidden in (
            "git fetch",
            "git clone",
            "git checkout",
            "git switch",
            "git push",
            "git commit",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.evaluator.lower(),
                )

    def test_breakers_run_before_packaging(
        self,
    ) -> None:
        self.assertLess(
            self.evaluator.index(
                "run_current_head_projection_breakers("
            ),
            self.evaluator.index(
                "stage_candidate_generation("
            ),
        )

    def test_p5d2_result_applies_only_via_one_shot_tick(
        self,
    ) -> None:
        self.assertIn(
            "one_shot_tick(",
            self.evaluator,
        )
        self.assertNotIn(
            '["live_projection_head"] =',
            self.evaluator,
        )
        self.assertNotIn(
            '["observer_phase"] =',
            self.evaluator,
        )
        self.assertNotIn(
            '["pending_heads"] =',
            self.evaluator,
        )

    def test_evaluator_has_no_background_loop(self) -> None:
        while_nodes = [
            node
            for node in ast.walk(self.evaluator_tree)
            if isinstance(node, ast.While)
        ]
        self.assertEqual(
            while_nodes,
            [],
        )
        for forbidden in (
            "run_forever",
            "poll_loop",
            "observe_forever",
            "start_background",
        ):
            self.assertNotIn(
                forbidden,
                self.evaluator,
            )

    def test_evaluator_does_not_import_promotion_runtime(
        self,
    ) -> None:
        for forbidden in (
            "promotion_experiment",
            "_write_pointer",
            "PROMOTION_CONFIRMED",
            "promote_candidate",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.evaluator,
                )

    def test_harness_git_commands_are_local_fixture_only(
        self,
    ) -> None:
        commands: set[str] = set()
        for node in ast.walk(self.harness_tree):
            if not isinstance(node, ast.Call):
                continue
            if (
                isinstance(node.func, ast.Name)
                and node.func.id == "_git"
                and len(node.args) >= 2
                and isinstance(
                    node.args[1],
                    ast.Constant,
                )
                and isinstance(
                    node.args[1].value,
                    str,
                )
            ):
                commands.add(
                    node.args[1].value
                )

        self.assertEqual(
            commands,
            {
                "init",
                "config",
                "remote",
                "add",
                "commit",
                "rev-parse",
            },
        )
        for forbidden in (
            "fetch",
            "clone",
            "checkout",
            "switch",
            "push",
            "pull",
        ):
            self.assertNotIn(
                forbidden,
                commands,
            )

    def test_harness_explicitly_denies_real_candidate_claim(
        self,
    ) -> None:
        self.assertIn(
            '"real_candidate_evaluated": False',
            self.harness,
        )
        self.assertIn(
            '"network_fetch_performed": False',
            self.harness,
        )
        self.assertIn(
            '"production_promotion_authorized":',
            self.harness,
        )

    def test_no_current_pointer_write_surface(
        self,
    ) -> None:
        combined = (
            self.projection
            + self.breakers
            + self.evaluator
        )
        for forbidden in (
            "_write_pointer",
            "promotion_experiment",
            "validate_pointer_entry",
            "PROMOTION_CONFIRMED",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    combined,
                )

        for module in (
            self.breakers,
            self.evaluator,
        ):
            self.assertNotIn(
                'open("CURRENT',
                module,
            )
            self.assertNotIn(
                'Path("CURRENT',
                module,
            )

    def test_chp_runner_is_read_only(self) -> None:
        for forbidden in (
            ".write_bytes(",
            ".write_text(",
            ".unlink(",
            ".mkdir(",
            "exclusive_write(",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.breakers,
                )


if __name__ == "__main__":
    unittest.main()
