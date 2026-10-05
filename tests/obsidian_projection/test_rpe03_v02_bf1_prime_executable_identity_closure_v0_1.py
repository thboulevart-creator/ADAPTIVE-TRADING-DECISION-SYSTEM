from __future__ import annotations

import importlib.util
import os
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py"
GIT = r"C:\Program Files\Git\cmd\git.exe"
GIT_DIR = pathlib.Path(GIT).parent


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, MODULE)
    m = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(m)
    return m


def make_repo():
    td = tempfile.TemporaryDirectory(prefix="rpe03-bf1p-")
    repo = pathlib.Path(td.name) / "repo"
    subprocess.run([GIT, "init", str(repo)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run([GIT, "-C", str(repo), "config", "user.name", "bf1p"], check=True)
    subprocess.run([GIT, "-C", str(repo), "config", "user.email", "bf1p@example.invalid"], check=True)
    (repo / "x").write_text("a", encoding="utf-8")
    subprocess.run([GIT, "-C", str(repo), "add", "x"], check=True)
    subprocess.run([GIT, "-C", str(repo), "commit", "-m", "a"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    a = subprocess.run([GIT, "-C", str(repo), "rev-parse", "HEAD"], check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
    (repo / "x").write_text("b", encoding="utf-8")
    subprocess.run([GIT, "-C", str(repo), "add", "x"], check=True)
    subprocess.run([GIT, "-C", str(repo), "commit", "-m", "b"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    b = subprocess.run([GIT, "-C", str(repo), "rev-parse", "HEAD"], check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
    return td, repo, a, b


class TestRPE03V02BF1PrimeExecutableIdentityClosure(unittest.TestCase):
    def test_bare_git_exe_is_rejected_even_when_cwd_resolves_to_governed_file(self):
        m = load_module("bf1p_bare")
        old = os.getcwd()
        try:
            os.chdir(GIT_DIR)
            self.assertFalse(m._verify_governed_git_executable("git.exe"))
        finally:
            os.chdir(old)

    def test_dot_relative_git_exe_is_rejected(self):
        m = load_module("bf1p_dot")
        old = os.getcwd()
        try:
            os.chdir(GIT_DIR)
            self.assertFalse(m._verify_governed_git_executable(r".\git.exe"))
        finally:
            os.chdir(old)

    def test_classify_with_bare_git_exe_fails_closed_before_positive_transition(self):
        m = load_module("bf1p_classify")
        td, repo, a, b = make_repo()
        old = os.getcwd()
        try:
            os.chdir(GIT_DIR)
            self.assertEqual(m.classify_transition(repo, a, b, "git.exe"), "UNKNOWN")
        finally:
            os.chdir(old)
            td.cleanup()

    def test_run_git_receives_only_verified_absolute_executable(self):
        m = load_module("bf1p_raw_execution")
        seen = []
        def fake_run(cmd, **kwargs):
            seen.append(cmd)
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
        with mock.patch.object(m.subprocess, "run", side_effect=fake_run):
            m._run_git(pathlib.Path.cwd(), "git.exe", "rev-parse", "--is-bare-repository")
        self.assertEqual(seen[0][0], GIT)
        self.assertTrue(pathlib.Path(seen[0][0]).is_absolute())


if __name__ == "__main__":
    unittest.main()
