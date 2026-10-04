from __future__ import annotations

import pathlib
import tempfile
import types
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py"
GIT = r"C:\Program Files\Git\cmd\git.exe"


def load_mutant(name: str, replacements=()):
    source = MODULE.read_text(encoding="utf-8")
    for old, new in replacements:
        if source.count(old) != 1:
            raise AssertionError(f"mutation anchor count != 1: {old!r}")
        source = source.replace(old, new, 1)
    m = types.ModuleType(name)
    m.__file__ = str(MODULE)
    exec(compile(source, str(MODULE), "exec"), m.__dict__)
    return m


class TestRPE03V02Mutation(unittest.TestCase):
    def test_path_binding_guard_is_required(self):
        base = load_mutant("rpe03_v02_base_path")
        mutant = load_mutant(
            "rpe03_v02_mut_path",
            ((
                "    if not supplied.is_file() or not _same_path(supplied, expected):\n        return False\n",
                "    if not supplied.is_file():\n        return False\n",
            ),),
        )
        with tempfile.TemporaryDirectory(prefix="rpe03-v02-copy-") as td:
            alt = pathlib.Path(td) / "git.exe"
            alt.write_bytes(pathlib.Path(GIT).read_bytes())
            with mock.patch.object(base, "_git_version", return_value=base._GOVERNED_GIT_VERSION),                  mock.patch.object(mutant, "_git_version", return_value=mutant._GOVERNED_GIT_VERSION):
                self.assertFalse(base._verify_governed_git_executable(str(alt)))
                self.assertTrue(mutant._verify_governed_git_executable(str(alt)))

    def test_sha_binding_guard_is_required(self):
        base = load_mutant("rpe03_v02_base_sha")
        mutant = load_mutant(
            "rpe03_v02_mut_sha",
            ((
                "    if _sha256_file(supplied) != _GOVERNED_GIT_SHA256:\n        return False\n",
                "    if False:\n        return False\n",
            ),),
        )
        with mock.patch.object(base, "_sha256_file", return_value="0" * 64),              mock.patch.object(mutant, "_sha256_file", return_value="0" * 64),              mock.patch.object(base, "_git_version", return_value=base._GOVERNED_GIT_VERSION),              mock.patch.object(mutant, "_git_version", return_value=mutant._GOVERNED_GIT_VERSION):
            self.assertFalse(base._verify_governed_git_executable(GIT))
            self.assertTrue(mutant._verify_governed_git_executable(GIT))

    def test_version_binding_guard_is_required(self):
        base = load_mutant("rpe03_v02_base_version")
        mutant = load_mutant(
            "rpe03_v02_mut_version",
            ((
                "    if version != _GOVERNED_GIT_VERSION:\n        return False\n    parsed = _parse_git_version(version)\n    if parsed is None or parsed < _MIN_GIT_VERSION:\n        return False\n",
                "    if False:\n        return False\n    parsed = _MIN_GIT_VERSION\n    if False:\n        return False\n",
            ),),
        )
        with mock.patch.object(base, "_git_version", return_value="git version 2.53.0.windows.1"),              mock.patch.object(mutant, "_git_version", return_value="git version 2.53.0.windows.1"):
            self.assertFalse(base._verify_governed_git_executable(GIT))
            self.assertTrue(mutant._verify_governed_git_executable(GIT))

    def test_run_git_must_use_governed_absolute_path(self):
        mutant = load_mutant(
            "rpe03_v02_mut_implicit",
            ((
                '    cmd = [governed_git_executable, "-c", "core.commitGraph=false", *args]\n',
                '    cmd = ["git", "-c", "core.commitGraph=false", *args]\n',
            ),),
        )
        seen = []
        def fake_run(cmd, **kwargs):
            seen.append(cmd)
            return types.SimpleNamespace(returncode=0, stdout="", stderr="")
        with mock.patch.object(mutant.subprocess, "run", side_effect=fake_run):
            mutant._run_git(pathlib.Path.cwd(), GIT, "rev-parse", "--is-bare-repository")
        self.assertEqual(seen[0][0], "git")
        self.assertNotEqual(seen[0][0], GIT)


if __name__ == "__main__":
    unittest.main()
