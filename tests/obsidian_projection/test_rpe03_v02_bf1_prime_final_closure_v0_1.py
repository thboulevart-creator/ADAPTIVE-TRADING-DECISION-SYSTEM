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
    td = tempfile.TemporaryDirectory(prefix="rpe03-bf1p-final-")
    repo = pathlib.Path(td.name) / "repo"
    subprocess.run([GIT, "init", str(repo)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run([GIT, "-C", str(repo), "config", "user.name", "bf1p-final"], check=True)
    subprocess.run([GIT, "-C", str(repo), "config", "user.email", "bf1p-final@example.invalid"], check=True)
    (repo / "x").write_text("a", encoding="utf-8")
    subprocess.run([GIT, "-C", str(repo), "add", "x"], check=True)
    subprocess.run([GIT, "-C", str(repo), "commit", "-m", "a"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    a = subprocess.run([GIT, "-C", str(repo), "rev-parse", "HEAD"], check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
    (repo / "x").write_text("b", encoding="utf-8")
    subprocess.run([GIT, "-C", str(repo), "add", "x"], check=True)
    subprocess.run([GIT, "-C", str(repo), "commit", "-m", "b"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    b = subprocess.run([GIT, "-C", str(repo), "rev-parse", "HEAD"], check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
    return td, repo, a, b


def compile_sentinel_git(fake: pathlib.Path):
    source = (
        'using System; using System.IO; '
        'public class P { public static void Main(string[] args) { '
        'var p=Environment.GetEnvironmentVariable("RPE03_SENTINEL"); '
        'if(!String.IsNullOrEmpty(p)) File.WriteAllText(p,"FAKE_GIT_EXECUTED"); '
        'Environment.Exit(7); } }'
    )
    source_file = fake.with_suffix(".cs")
    source_file.write_text(source, encoding="utf-8")
    ps = (
        "$ErrorActionPreference='Stop'; "
        f"Add-Type -Path '{source_file}' -OutputAssembly '{fake}' "
        "-OutputType ConsoleApplication"
    )
    cp = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", ps],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if cp.returncode != 0 or not fake.is_file():
        raise AssertionError(cp.stderr)


class TestRPE03V02BF1PrimeFinalClosure(unittest.TestCase):
    def test_non_absolute_values_are_rejected(self):
        m = load_module("bf1p_final_relative")
        old = os.getcwd()
        try:
            os.chdir(GIT_DIR)
            for value in ("git", "git.exe", r".\git.exe", r"relative\git.exe"):
                self.assertIsNone(m._resolve_and_verify_governed_git_executable(value))
                self.assertFalse(m._verify_governed_git_executable(value))
        finally:
            os.chdir(old)

    def test_classify_with_bare_git_exe_is_unknown(self):
        m = load_module("bf1p_final_classify")
        td, repo, a, b = make_repo()
        old = os.getcwd()
        try:
            os.chdir(GIT_DIR)
            self.assertEqual(m.classify_transition(repo, a, b, "git.exe"), "UNKNOWN")
        finally:
            os.chdir(old)
            td.cleanup()

    def test_internal_run_git_rejects_raw_non_absolute_token_without_subprocess(self):
        m = load_module("bf1p_final_run")
        with mock.patch.object(m.subprocess, "run") as wrapped:
            self.assertIsNone(
                m._run_git(pathlib.Path.cwd(), "git.exe", "rev-parse", "--is-bare-repository")
            )
        wrapped.assert_not_called()

    def test_verified_path_is_exact_path_used_by_all_classifier_subprocesses(self):
        m = load_module("bf1p_final_exact")
        td, repo, a, b = make_repo()
        seen = []
        original = m.subprocess.run

        def wrapped(cmd, *args, **kwargs):
            if isinstance(cmd, list) and cmd:
                seen.append(cmd[0])
            return original(cmd, *args, **kwargs)

        try:
            with mock.patch.object(m.subprocess, "run", side_effect=wrapped):
                self.assertEqual(m.classify_transition(repo, a, b, GIT), "FAST_FORWARD")
            self.assertTrue(seen)
            governed = str(pathlib.Path(GIT).resolve(strict=True))
            self.assertTrue(all(x == governed for x in seen))
        finally:
            td.cleanup()

    @unittest.skipUnless(os.name == "nt", "Windows positive sentinel falsification")
    def test_windows_positive_sentinel_control_and_final_candidate(self):
        m = load_module("bf1p_final_sentinel")
        td, repo, a, b = make_repo()
        with tempfile.TemporaryDirectory(prefix="rpe03-bf1p-sentinel-") as fake_td:
            fake_dir = pathlib.Path(fake_td)
            fake = fake_dir / "git.exe"
            sentinel = fake_dir / "sentinel.txt"
            compile_sentinel_git(fake)

            old = os.getcwd()
            old_sentinel = os.environ.get("RPE03_SENTINEL")
            try:
                os.chdir(fake_dir)
                os.environ["RPE03_SENTINEL"] = str(sentinel)

                control = subprocess.run(
                    ["git", "--version"],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertEqual(control.returncode, 7)
                self.assertTrue(sentinel.is_file())
                self.assertEqual(sentinel.read_text(encoding="utf-8"), "FAKE_GIT_EXECUTED")

                sentinel.unlink()
                self.assertEqual(m.classify_transition(repo, a, b, GIT), "FAST_FORWARD")
                self.assertFalse(sentinel.exists())
            finally:
                os.chdir(old)
                if old_sentinel is None:
                    os.environ.pop("RPE03_SENTINEL", None)
                else:
                    os.environ["RPE03_SENTINEL"] = old_sentinel
                td.cleanup()


if __name__ == "__main__":
    unittest.main()
