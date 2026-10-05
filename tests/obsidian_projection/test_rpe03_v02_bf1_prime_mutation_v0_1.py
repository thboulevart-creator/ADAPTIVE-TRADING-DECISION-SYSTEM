from __future__ import annotations

import os
import pathlib
import tempfile
import types
import unittest
from unittest import mock

from tests.obsidian_projection.test_rpe03_v02_bf1_prime_final_closure_v0_1 import (
    GIT,
    GIT_DIR,
    make_repo,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py"


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


class TestRPE03V02BF1PrimeMutation(unittest.TestCase):
    def test_composite_raw_string_execution_mutant_is_discriminated(self):
        base = load_mutant("bf1p_mut_base")
        mutant = load_mutant(
            "bf1p_mut_raw",
            (
                (
                    "    if not raw.is_absolute():\n        return None\n",
                    "    if False:\n        return None\n",
                ),
                (
                    "    return str(supplied)\n\n\ndef _verify_governed_git_executable",
                    "    return governed_git_executable\n\n\ndef _verify_governed_git_executable",
                ),
                (
                    "    try:\n        executable = Path(governed_git_executable)\n"
                    "    except (TypeError, ValueError):\n        return None\n"
                    "    if not executable.is_absolute():\n        return None\n"
                    "    try:\n        resolved = executable.resolve(strict=True)\n"
                    "        expected = Path(_GOVERNED_GIT_PATH).resolve(strict=True)\n"
                    "    except (OSError, RuntimeError, ValueError):\n        return None\n"
                    "    if not _same_path(resolved, expected):\n        return None\n"
                    '    cmd = [str(resolved), "-c", "core.commitGraph=false", *args]\n',
                    '    cmd = [governed_git_executable, "-c", "core.commitGraph=false", *args]\n',
                ),
            ),
        )
        td, repo, a, b = make_repo()
        old = os.getcwd()
        try:
            os.chdir(GIT_DIR)
            self.assertEqual(base.classify_transition(repo, a, b, "git.exe"), "UNKNOWN")
            self.assertEqual(mutant.classify_transition(repo, a, b, "git.exe"), "FAST_FORWARD")
        finally:
            os.chdir(old)
            td.cleanup()

    def test_sha_guard_mutant_is_discriminated(self):
        base = load_mutant("bf1p_mut_sha_base")
        mutant = load_mutant(
            "bf1p_mut_sha",
            (
                (
                    "    if _sha256_file(supplied) != _GOVERNED_GIT_SHA256:\n        return None\n",
                    "    if False:\n        return None\n",
                ),
            ),
        )
        with mock.patch.object(base, "_sha256_file", return_value="0" * 64), \
             mock.patch.object(mutant, "_sha256_file", return_value="0" * 64), \
             mock.patch.object(base, "_git_version", return_value=base._GOVERNED_GIT_VERSION), \
             mock.patch.object(mutant, "_git_version", return_value=mutant._GOVERNED_GIT_VERSION):
            self.assertIsNone(base._resolve_and_verify_governed_git_executable(GIT))
            self.assertEqual(
                mutant._resolve_and_verify_governed_git_executable(GIT),
                str(pathlib.Path(GIT).resolve(strict=True)),
            )

    def test_version_guard_mutant_is_discriminated(self):
        base = load_mutant("bf1p_mut_ver_base")
        mutant = load_mutant(
            "bf1p_mut_ver",
            (
                (
                    "    if version != _GOVERNED_GIT_VERSION:\n        return None\n"
                    "    parsed = _parse_git_version(version)\n"
                    "    if parsed is None or parsed < _MIN_GIT_VERSION:\n        return None\n",
                    "    if False:\n        return None\n"
                    "    parsed = _MIN_GIT_VERSION\n"
                    "    if False:\n        return None\n",
                ),
            ),
        )
        with mock.patch.object(base, "_git_version", return_value="git version 2.53.0.windows.1"), \
             mock.patch.object(mutant, "_git_version", return_value="git version 2.53.0.windows.1"):
            self.assertIsNone(base._resolve_and_verify_governed_git_executable(GIT))
            self.assertEqual(
                mutant._resolve_and_verify_governed_git_executable(GIT),
                str(pathlib.Path(GIT).resolve(strict=True)),
            )


if __name__ == "__main__":
    unittest.main()
