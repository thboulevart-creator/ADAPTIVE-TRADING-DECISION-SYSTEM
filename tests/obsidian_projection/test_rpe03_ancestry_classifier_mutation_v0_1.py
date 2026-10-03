import os
import subprocess
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools" / "obsidian_projection" / "rpe03_ancestry_classifier_v0_1.py"


def load_source_module(name, replacements=()):
    source = MODULE.read_text(encoding="utf-8")
    for old, new in replacements:
        if source.count(old) != 1:
            raise AssertionError(f"mutation anchor count != 1: {old!r}")
        source = source.replace(old, new, 1)
    module = types.ModuleType(name)
    module.__file__ = str(MODULE)
    exec(compile(source, str(MODULE), "exec"), module.__dict__)
    return module


def git(repo, *args):
    cp = subprocess.run(
        ["git", *args],
        cwd=str(repo),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if cp.returncode != 0:
        raise AssertionError(cp.stderr)
    return cp.stdout.strip()


def make_linear_graph():
    td = tempfile.TemporaryDirectory()
    repo = Path(td.name)
    git(repo, "init")
    git(repo, "config", "user.email", "rpe03-mut@example.invalid")
    git(repo, "config", "user.name", "RPE03 Mut")
    (repo / "f.txt").write_text("A\n", encoding="utf-8")
    git(repo, "add", "f.txt")
    git(repo, "commit", "-m", "A")
    a = git(repo, "rev-parse", "HEAD")
    (repo / "f.txt").write_text("B\n", encoding="utf-8")
    git(repo, "commit", "-am", "B")
    b = git(repo, "rev-parse", "HEAD")
    return td, repo, a, b


class TestRPE03MutationDiscriminationV01(unittest.TestCase):
    def test_exit_one_mapping_mutant_is_killed(self):
        base = load_source_module("rpe03_base_exit1")
        mutant = load_source_module(
            "rpe03_mut_exit1",
            ((
                '    if cp.returncode == 1:\n        return "NON_FAST_FORWARD"',
                '    if cp.returncode == 1:\n        return "FAST_FORWARD"',
            ),),
        )
        td, repo, a, b = make_linear_graph()
        try:
            self.assertEqual(base.classify_transition(repo, b, a), "NON_FAST_FORWARD")
            self.assertEqual(mutant.classify_transition(repo, b, a), "FAST_FORWARD")
        finally:
            td.cleanup()

    def test_inherited_git_environment_strip_mutant_is_killed(self):
        base = load_source_module("rpe03_base_env")
        mutant = load_source_module(
            "rpe03_mut_env",
            ((
                'env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}',
                'env = dict(os.environ)',
            ),),
        )
        td, repo, a, b = make_linear_graph()
        try:
            hostile = {
                "GIT_DIR": "X:/forbidden",
                "GIT_OBJECT_DIRECTORY": "X:/forbidden-objects",
                "GIT_ALTERNATE_OBJECT_DIRECTORIES": "X:/forbidden-alt",
            }
            with mock.patch.dict(os.environ, hostile, clear=False):
                self.assertEqual(base.classify_transition(repo, a, b), "FAST_FORWARD")
                self.assertNotEqual(mutant.classify_transition(repo, a, b), "FAST_FORWARD")
        finally:
            td.cleanup()

    def test_replace_object_neutralization_mutant_is_killed(self):
        base = load_source_module("rpe03_base_replace")
        mutant = load_source_module(
            "rpe03_mut_replace",
            (('            "GIT_NO_REPLACE_OBJECTS": "1",\n', ""),),
        )
        td, repo, a, b = make_linear_graph()
        try:
            tree = git(repo, "rev-parse", f"{a}^{{tree}}")
            root = git(repo, "commit-tree", tree, "-m", "unrelated replacement root")
            git(repo, "replace", b, root)
            self.assertEqual(base.classify_transition(repo, a, b), "FAST_FORWARD")
            self.assertNotEqual(mutant.classify_transition(repo, a, b), "FAST_FORWARD")
        finally:
            td.cleanup()

    def test_no_lazy_fetch_environment_mutant_is_killed(self):
        base = load_source_module("rpe03_base_lazy")
        mutant = load_source_module(
            "rpe03_mut_lazy",
            (('            "GIT_NO_LAZY_FETCH": "1",\n', ""),),
        )
        self.assertEqual(base._safe_git_env()["GIT_NO_LAZY_FETCH"], "1")
        self.assertNotIn("GIT_NO_LAZY_FETCH", mutant._safe_git_env())


if __name__ == "__main__":
    unittest.main()
