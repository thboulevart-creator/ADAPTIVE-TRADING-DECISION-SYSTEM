from __future__ import annotations

import importlib.util
import inspect
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py"
GIT = r"C:\Program Files\Git\cmd\git.exe"
EXPECTED_SHA256 = "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5"
EXPECTED_VERSION = "git version 2.54.0.windows.1"


def load_module(name: str):
    if not MODULE.exists():
        raise AssertionError(f"required V0.2 implementation missing: {MODULE}")
    spec = importlib.util.spec_from_file_location(name, MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def safe_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_LAZY_FETCH": "1",
    })
    return env


def git(repo: pathlib.Path, *args: str):
    cp = subprocess.run(
        [GIT, *args],
        cwd=str(repo),
        env=safe_env(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if cp.returncode != 0:
        raise AssertionError(cp.stderr)
    return cp.stdout.strip()


def make_repo():
    td = tempfile.TemporaryDirectory(prefix="rpe03-v02-")
    repo = pathlib.Path(td.name) / "repo"
    subprocess.run([GIT, "init", str(repo)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    git(repo, "config", "user.name", "RPE03 V02")
    git(repo, "config", "user.email", "rpe03-v02@example.invalid")
    (repo / "f.txt").write_text("A\n", encoding="utf-8")
    git(repo, "add", "f.txt")
    git(repo, "commit", "-m", "A")
    a = git(repo, "rev-parse", "HEAD")
    (repo / "f.txt").write_text("A\nB\n", encoding="utf-8")
    git(repo, "add", "f.txt")
    git(repo, "commit", "-m", "B")
    b = git(repo, "rev-parse", "HEAD")
    return td, repo, a, b


class TestRPE03GovernedGitExecutableBindingV02(unittest.TestCase):
    def test_public_interface_requires_governed_git_executable(self):
        m = load_module("rpe03_v02_sig")
        self.assertEqual(
            list(inspect.signature(m.classify_transition).parameters),
            ["repo_path", "previous_observed_head", "new_exact_observed_head", "governed_git_executable"],
        )

    def test_governed_absolute_executable_is_used(self):
        m = load_module("rpe03_v02_abs")
        seen = []
        original = subprocess.run

        def wrapped(cmd, *args, **kwargs):
            if isinstance(cmd, list) and cmd:
                seen.append(cmd[0])
            return original(cmd, *args, **kwargs)

        td, repo, a, b = make_repo()
        try:
            with mock.patch.object(m.subprocess, "run", side_effect=wrapped):
                result = m.classify_transition(repo, a, b, GIT)
            self.assertEqual(result, "FAST_FORWARD")
            self.assertTrue(seen)
            self.assertTrue(all(x == GIT for x in seen))
        finally:
            td.cleanup()

    def test_wrong_supplied_path_fails_closed(self):
        m = load_module("rpe03_v02_wrong_path")
        td, repo, a, b = make_repo()
        try:
            self.assertEqual(m.classify_transition(repo, a, b, r"C:\Windows\System32\cmd.exe"), "UNKNOWN")
        finally:
            td.cleanup()

    def test_wrong_sha_fails_closed(self):
        m = load_module("rpe03_v02_wrong_sha")
        td, repo, a, b = make_repo()
        try:
            with mock.patch.object(m, "_sha256_file", return_value="0" * 64):
                self.assertEqual(m.classify_transition(repo, a, b, GIT), "UNKNOWN")
        finally:
            td.cleanup()

    def test_version_below_minimum_fails_closed(self):
        m = load_module("rpe03_v02_old_version")
        td, repo, a, b = make_repo()
        try:
            with mock.patch.object(m, "_git_version", return_value="git version 2.53.0.windows.1"):
                self.assertEqual(m.classify_transition(repo, a, b, GIT), "UNKNOWN")
        finally:
            td.cleanup()

    def test_version_and_sha_constants_match_preregistered_identity(self):
        m = load_module("rpe03_v02_constants")
        self.assertEqual(m._GOVERNED_GIT_PATH, GIT)
        self.assertEqual(m._GOVERNED_GIT_SHA256, EXPECTED_SHA256)
        self.assertEqual(m._GOVERNED_GIT_VERSION, EXPECTED_VERSION)
        self.assertEqual(m._MIN_GIT_VERSION, (2, 54, 0))

    def test_transition_semantics_initial_same_ff_nonff_unknown(self):
        m = load_module("rpe03_v02_semantics")
        td, repo, a, b = make_repo()
        try:
            self.assertEqual(m.classify_transition(repo, None, a, GIT), "INITIAL")
            self.assertEqual(m.classify_transition(repo, a, a, GIT), "SAME")
            self.assertEqual(m.classify_transition(repo, a, b, GIT), "FAST_FORWARD")
            self.assertEqual(m.classify_transition(repo, b, a, GIT), "NON_FAST_FORWARD")
            self.assertEqual(m.classify_transition(repo, "f" * 40, b, GIT), "UNKNOWN")
        finally:
            td.cleanup()

    @unittest.skipUnless(os.name == "nt", "Windows executable-search falsification")
    def test_windows_implicit_search_can_select_wrong_git_but_v02_ignores_it(self):
        m = load_module("rpe03_v02_windows_search")
        td, repo, a, b = make_repo()
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory(prefix="rpe03-v02-fakegit-") as fake_dir:
            fake = pathlib.Path(fake_dir) / "git.exe"
            source = pathlib.Path(os.environ.get("SystemRoot", r"C:\\Windows")) / "System32" / "where.exe"
            shutil.copy2(source, fake)
            try:
                os.chdir(fake_dir)
                cp = subprocess.run(
                    ["git", "--version"],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertNotEqual(cp.returncode, 0)
                self.assertNotIn("git version", (cp.stdout + cp.stderr).lower())
                self.assertEqual(m.classify_transition(repo, a, b, GIT), "FAST_FORWARD")
            finally:
                os.chdir(old_cwd)
                td.cleanup()


if __name__ == "__main__":
    unittest.main()
