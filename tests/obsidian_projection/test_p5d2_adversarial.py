from __future__ import annotations

import ast
import unittest
from pathlib import Path


class P5D2AdversarialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.module_path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "observer_tick.py"
        )
        cls.module = cls.module_path.read_text(
            encoding="utf-8"
        )
        cls.tree = ast.parse(cls.module)

    def test_contract_blob_is_pinned(self) -> None:
        self.assertIn(
            (
                'CONTRACT_BLOB = '
                '"5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3"'
            ),
            self.module,
        )

    def test_only_expected_imports_exist(self) -> None:
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
        self.assertEqual(
            imported,
            {"hashlib", "json", "re", "typing", "__future__"},
        )

    def test_forbidden_runtime_modules_absent(self) -> None:
        for forbidden in (
            "subprocess",
            "socket",
            "urllib",
            "requests",
            "http",
            "pathlib",
            "os.",
            "os.environ",
            "time.",
            "sleep(",
            "random",
            "threading",
            "multiprocessing",
            "asyncio",
            "winreg",
            "ctypes",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_no_filesystem_write_surface(self) -> None:
        for forbidden in (
            "open(",
            ".write_text(",
            ".write_bytes(",
            ".mkdir(",
            ".unlink(",
            ".rename(",
            ".replace(",
            "shutil",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_no_git_command_surface(self) -> None:
        for forbidden in (
            "git ",
            "git.exe",
            "ls-remote",
            "fetch --",
            "checkout",
            "worktree",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_no_vault_or_windows_persistence_surface(
        self,
    ) -> None:
        for forbidden in (
            "ATDS-OBSIDIAN-PROJECTION",
            "OneDrive",
            "CURRENT.md",
            "Task Scheduler",
            "schtasks",
            "Startup",
            "Start-Process",
            "Windows Service",
            "sc.exe",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_no_graph_search_semantic_claim(self) -> None:
        for forbidden in (
            "Graph/Search",
            "graph_current",
            "native graph",
            "native search",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module.lower(),
                )

    def test_no_while_loop_exists(self) -> None:
        loops = [
            node
            for node in ast.walk(self.tree)
            if isinstance(node, ast.While)
        ]
        self.assertEqual(loops, [])

    def test_no_background_function_primitives(self) -> None:
        names = {
            node.id
            for node in ast.walk(self.tree)
            if isinstance(node, ast.Name)
        }
        for forbidden in (
            "Thread",
            "Process",
            "create_task",
            "run_in_executor",
            "Popen",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    names,
                )

    def test_one_shot_tick_has_no_self_recursion(
        self,
    ) -> None:
        target = next(
            node
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "one_shot_tick"
        )
        recursive_calls = [
            node
            for node in ast.walk(target)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "one_shot_tick"
        ]
        self.assertEqual(recursive_calls, [])

    def test_authority_flags_are_literal_false(self) -> None:
        self.assertIn(
            '"automatic_promotion_authorized": False',
            self.module,
        )
        self.assertIn(
            '"production_write_authorized": False',
            self.module,
        )
        self.assertNotIn(
            '"automatic_promotion_authorized": True',
            self.module,
        )
        self.assertNotIn(
            '"production_write_authorized": True',
            self.module,
        )

    def test_state_and_input_are_cloned_before_transition(
        self,
    ) -> None:
        start = self.module.index(
            "def one_shot_tick("
        )
        body = self.module[start:]
        self.assertIn(
            "previous = _clone(previous_state)",
            body,
        )
        self.assertIn(
            "event = _clone(normalized_input)",
            body,
        )

    def test_validation_precedes_transition(self) -> None:
        start = self.module.index(
            "def one_shot_tick("
        )
        body = self.module[start:]
        state_validation = body.index(
            "_validate_state(previous)"
        )
        input_validation = body.index(
            "_validate_input(previous, event)"
        )
        transition = body.index(
            "_apply_transition("
        )
        self.assertLess(
            state_validation,
            input_validation,
        )
        self.assertLess(
            input_validation,
            transition,
        )

    def test_sequence_is_assigned_once_after_transition(
        self,
    ) -> None:
        start = self.module.index(
            "def one_shot_tick("
        )
        body = self.module[start:]
        assignment = (
            'next_state["last_event_sequence"] = '
            'event["sequence"]'
        )
        self.assertEqual(
            body.count(assignment),
            1,
        )

    def test_audit_binds_all_four_digests(self) -> None:
        for field in (
            '"previous_state_digest": _digest(previous)',
            '"input_digest": _digest(event)',
            '"decision_digest": _digest(decision)',
            '"next_state_digest": _digest(next_state)',
        ):
            with self.subTest(field=field):
                self.assertIn(
                    field,
                    self.module,
                )

    def test_audit_contains_no_volatile_envelope(self) -> None:
        start = self.module.index(
            "audit = {"
        )
        end = self.module.index(
            "\n\n    result = {",
            start,
        )
        audit_body = self.module[start:end]
        for forbidden in (
            "observed_at",
            "host_id",
            "process_id",
            "timestamp",
            "pid",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    audit_body,
                )

    def test_only_one_public_tick_entrypoint(self) -> None:
        defs = {
            node.name
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef)
        }
        self.assertIn(
            "one_shot_tick",
            defs,
        )
        for forbidden in (
            "run_forever",
            "observe_forever",
            "poll_loop",
            "daemon",
            "main",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    defs,
                )


if __name__ == "__main__":
    unittest.main()
