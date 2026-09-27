from __future__ import annotations

import ast
import unittest
from pathlib import Path


class P5D3C2AdversarialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "candidate_generation_staging.py"
        )
        cls.module = cls.path.read_text(
            encoding="utf-8"
        )
        cls.tree = ast.parse(cls.module)
        cls.runner_path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "p5d3c2_verify.py"
        )
        cls.runner = cls.runner_path.read_text(
            encoding="utf-8"
        )
        cls.runner_tree = ast.parse(
            cls.runner
        )

    def test_exact_contract_and_qualification_are_pinned(
        self,
    ) -> None:
        self.assertIn(
            (
                'STAGING_CONTRACT_BLOB = (\n'
                '    "79c6a3380a1dcefc49aa4619259baaa8eeadb535"'
            ),
            self.module,
        )
        self.assertIn(
            (
                'P5D3C_QUALIFICATION_COMMIT = (\n'
                '    "437ab790f2a1fa4b490344d28cb7b7a2e8116db3"'
            ),
            self.module,
        )
        self.assertIn(
            (
                'IMPLEMENTATION_CONTRACT_BLOB = (\n'
                '    "12f04ad90567c6b0451713a4180f3b10df66de41"'
            ),
            self.module,
        )

    def test_p5c2_fixture_runtime_is_not_imported(
        self,
    ) -> None:
        for forbidden in (
            "promotion_experiment",
            "build_generation",
            "validate_generation_dir",
            "_write_pointer",
            "validate_pointer_entry",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_network_and_git_runtime_modules_absent(
        self,
    ) -> None:
        imported: set[str] = set()
        for node in ast.walk(self.tree):
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
            "git",
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

    def test_no_time_uuid_or_random_identity_surface(
        self,
    ) -> None:
        for forbidden in (
            "time.",
            "datetime",
            "uuid",
            "random",
            "secrets",
            "gethostname",
            "platform.node",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_verifier_has_no_direct_write_surface(
        self,
    ) -> None:
        target = next(
            node
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name
            == "verify_candidate_generation"
        )
        source = (
            ast.get_source_segment(
                self.module,
                target,
            )
            or ""
        )

        for forbidden in (
            "_write_exclusive(",
            ".write_bytes(",
            ".write_text(",
            ".mkdir(",
            ".unlink(",
            ".rename(",
            ".replace(",
            'open("w',
            'open("x',
            'open("a',
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    source,
                )

    def test_descriptor_authority_is_literal_false(
        self,
    ) -> None:
        target = next(
            node
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name
            == "verify_candidate_generation"
        )
        source = (
            ast.get_source_segment(
                self.module,
                target,
            )
            or ""
        )
        self.assertIn(
            '"promotion_authorized": False',
            source,
        )
        self.assertNotIn(
            '"promotion_authorized": True',
            source,
        )

    def test_descriptor_contains_no_stage_path_field(
        self,
    ) -> None:
        target = next(
            node
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name
            == "verify_candidate_generation"
        )
        source = (
            ast.get_source_segment(
                self.module,
                target,
            )
            or ""
        )
        for forbidden in (
            '"package_root"',
            '"stage_path"',
            '"absolute_path"',
            '"host"',
            '"pid"',
            '"timestamp"',
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    source,
                )

    def test_stage_function_never_invokes_promotion(
        self,
    ) -> None:
        target = next(
            node
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name
            == "stage_candidate_generation"
        )
        source = (
            ast.get_source_segment(
                self.module,
                target,
            )
            or ""
        )
        for forbidden in (
            "promote",
            "_write_pointer",
            "CURRENT.md",
            "CURRENT.json",
            "CURRENT.tmp",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    source,
                )

    def test_seal_write_occurs_after_manifest_writes(
        self,
    ) -> None:
        target = next(
            node
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name
            == "stage_candidate_generation"
        )
        source = (
            ast.get_source_segment(
                self.module,
                target,
            )
            or ""
        )

        payload_pos = source.index(
            "_PAYLOAD_MANIFEST,"
        )
        generation_pos = source.index(
            "_GENERATION_MANIFEST,"
        )
        seal_pos = source.index(
            "_SEAL,"
        )

        self.assertLess(
            payload_pos,
            generation_pos,
        )
        self.assertLess(
            generation_pos,
            seal_pos,
        )

    def test_stage_returns_read_only_verifier_result(
        self,
    ) -> None:
        target = next(
            node
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name
            == "stage_candidate_generation"
        )
        source = (
            ast.get_source_segment(
                self.module,
                target,
            )
            or ""
        )
        self.assertIn(
            "return verify_candidate_generation(",
            source,
        )

    def test_package_root_uses_temp_guard(self) -> None:
        self.assertIn(
            "validate_new_temp_staging_path",
            self.module,
        )
        self.assertIn(
            "package root must be below OS temp root",
            self.module,
        )

    def test_alias_and_hardlink_checks_are_explicit(
        self,
    ) -> None:
        self.assertIn(
            "FILE_ATTRIBUTE_REPARSE_POINT",
            self.module,
        )
        self.assertIn(
            "hard-link alias forbidden",
            self.module,
        )
        self.assertIn(
            "_assert_directory_chain_no_alias",
            self.module,
        )

    def test_manifest_canonicalization_is_sorted_compact(
        self,
    ) -> None:
        target = next(
            node
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "_canonical_json_bytes"
        )
        source = (
            ast.get_source_segment(
                self.module,
                target,
            )
            or ""
        )
        self.assertIn(
            "sort_keys=True",
            source,
        )
        self.assertIn(
            'separators=(",", ":")',
            source,
        )
        self.assertIn(
            "allow_nan=False",
            source,
        )

    def test_generation_identity_has_no_runtime_path(
        self,
    ) -> None:
        target = next(
            node
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "_identity_basis"
        )
        source = (
            ast.get_source_segment(
                self.module,
                target,
            )
            or ""
        )
        for forbidden in (
            "package_root",
            "verified_projection_root",
            "tempfile",
            "time",
            "uuid",
            "host",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    source,
                )

    def test_runner_does_not_reuse_p5c2_fixture(
        self,
    ) -> None:
        for forbidden in (
            "promotion_experiment",
            "build_generation",
            "validate_generation_dir",
            "_write_pointer",
            "validate_pointer_entry",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.runner,
                )

    def test_runner_has_no_network_or_git_mutation_modules(
        self,
    ) -> None:
        imported: set[str] = set()
        for node in ast.walk(self.runner_tree):
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
            "git",
            "winreg",
            "ctypes",
        }
        self.assertEqual(
            imported & forbidden,
            set(),
        )

    def test_runner_never_creates_current_pointer(
        self,
    ) -> None:
        for forbidden in (
            '"CURRENT"',
            '"CURRENT.md"',
            '"CURRENT.json"',
            '"CURRENT.tmp"',
            "promote(",
            '"production_promotion_authorized": true',
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.runner,
                )

    def test_runner_fixture_is_explicitly_packager_only(
        self,
    ) -> None:
        self.assertIn(
            "P5D3C2_SANDBOX_PACKAGER_INPUT",
            self.runner,
        )
        self.assertNotIn(
            "CURRENT_HEAD_BUILDER_QUALIFIED",
            self.runner,
        )

    def test_runner_uses_temp_sandbox(self) -> None:
        self.assertIn(
            "tempfile.TemporaryDirectory(",
            self.runner,
        )
        self.assertIn(
            "sandbox_retained",
            self.runner,
        )

    def test_no_background_loop_entrypoints(self) -> None:
        defs = {
            node.name
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef)
        }
        for forbidden in (
            "run_forever",
            "poll_loop",
            "observe_forever",
            "daemon",
            "start_background",
        ):
            self.assertNotIn(forbidden, defs)

        while_nodes = [
            node
            for node in ast.walk(self.tree)
            if isinstance(node, ast.While)
        ]
        self.assertEqual(while_nodes, [])


if __name__ == "__main__":
    unittest.main()
