import subprocess
import tempfile
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py"


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
        raise AssertionError(f"git {' '.join(args)} failed: {cp.stderr}")
    return cp.stdout.strip()


def make_bare_graph():
    source_td = tempfile.TemporaryDirectory()
    source = Path(source_td.name)
    git(source, "init")
    git(source, "config", "user.email", "rpe03-nb6@example.invalid")
    git(source, "config", "user.name", "RPE03 NB6")
    (source / "f.txt").write_text("A\n", encoding="utf-8")
    git(source, "add", "f.txt")
    git(source, "commit", "-m", "A")
    a = git(source, "rev-parse", "HEAD")
    (source / "f.txt").write_text("B\n", encoding="utf-8")
    git(source, "commit", "-am", "B")
    b = git(source, "rev-parse", "HEAD")

    bare_td = tempfile.TemporaryDirectory()
    bare = Path(bare_td.name) / "repo.git"
    git(source, "clone", "--bare", str(source), str(bare))
    return source_td, bare_td, bare, a, b


def load_module(name, replacements=()):
    source = MODULE.read_text(encoding="utf-8")
    for old, new in replacements:
        if source.count(old) != 1:
            raise AssertionError(f"mutation anchor count != 1: {old!r}")
        source = source.replace(old, new, 1)
    module = types.ModuleType(name)
    module.__file__ = str(MODULE)
    exec(compile(source, str(MODULE), "exec"), module.__dict__)
    return module


class TestRPE03NB6BareRootTestOnlyClosureV01(unittest.TestCase):
    def test_exact_bare_repository_root_remains_allowed(self):
        m = load_module("rpe03_nb6_base_root")
        source_td, bare_td, bare, a, b = make_bare_graph()
        try:
            self.assertEqual(m.classify_transition(bare, a, b), "FAST_FORWARD")
        finally:
            bare_td.cleanup()
            source_td.cleanup()

    def test_bare_repository_subdirectory_is_unknown(self):
        m = load_module("rpe03_nb6_base_subdir")
        source_td, bare_td, bare, a, b = make_bare_graph()
        try:
            self.assertEqual(
                m.classify_transition(bare / "objects", a, b),
                "UNKNOWN",
            )
        finally:
            bare_td.cleanup()
            source_td.cleanup()

    def test_bare_exact_root_condition_mutant_is_killed(self):
        base = load_module("rpe03_nb6_base_mut")
        mutant = load_module(
            "rpe03_nb6_mutant",
            ((
                '    if bare_text == "true":\n'
                '        if not _same_path(git_dir, repo):\n'
                '            return None\n',
                '    if bare_text == "true":\n'
                '        pass\n',
            ),),
        )
        source_td, bare_td, bare, a, b = make_bare_graph()
        try:
            self.assertEqual(base.classify_transition(bare / "objects", a, b), "UNKNOWN")
            self.assertEqual(
                mutant.classify_transition(bare / "objects", a, b),
                "FAST_FORWARD",
            )
        finally:
            bare_td.cleanup()
            source_td.cleanup()


if __name__ == "__main__":
    unittest.main()
