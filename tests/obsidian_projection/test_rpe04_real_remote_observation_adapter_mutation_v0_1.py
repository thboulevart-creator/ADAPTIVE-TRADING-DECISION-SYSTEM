from __future__ import annotations

import os
import pathlib
import subprocess
import tempfile
import types
import unittest
from unittest import mock

from tests.obsidian_projection.test_rpe04_real_remote_observation_adapter_v0_1 import (
    GIT,
    OBSERVER,
    SOURCE,
    SOURCE_REF,
    init_fixture,
    git,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_v0_1.py"


def load_source_module(name: str, replacements=()):
    source = MODULE.read_text(encoding="utf-8")
    for old, new in replacements:
        if source.count(old) != 1:
            raise AssertionError(f"mutation anchor count != 1: {old!r}")
        source = source.replace(old, new, 1)
    module = types.ModuleType(name)
    module.__file__ = str(MODULE)
    exec(compile(source, str(MODULE), "exec"), module.__dict__)
    return module


class TestRPE04MutationSweep(unittest.TestCase):
    def setUp(self):
        self.a = init_fixture()

    def tearDown(self):
        import shutil
        shutil.rmtree(SOURCE.parent, ignore_errors=True)

    def test_mutant_removing_git_hash_binding_is_detected(self):
        m = load_source_module(
            "rpe04_mut_hash",
            ((
                '        if _sha256_file(_GIT) != _CFG["git_executable"]["sha256"]:\n'
                '            return False\n',
                '        if False:\n'
                '            return False\n',
            ),),
        )
        with mock.patch.object(m, "_sha256_file", return_value="0" * 64):
            self.assertTrue(m._verify_git_executable_identity())

    def test_mutant_removing_path_token_binding_is_detected(self):
        m = load_source_module(
            "rpe04_mut_which",
            ((
                '        if resolved_token is None or not _same_path(Path(resolved_token), _GIT):\n'
                '            return False\n',
                '        if False:\n'
                '            return False\n',
            ),),
        )
        with mock.patch.object(m.shutil, "which", return_value=r"C:\evil\git.exe"):
            self.assertTrue(m._verify_git_executable_identity())

    def test_mutant_preserving_inherited_git_environment_is_detected(self):
        base = load_source_module("rpe04_base_env")
        m = load_source_module(
            "rpe04_mut_env",
            ((
                '    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\n',
                '    env = dict(os.environ)\n',
            ),),
        )
        with mock.patch.dict(os.environ, {"GIT_DIR": "evil"}, clear=False):
            self.assertNotIn("GIT_DIR", base._build_git_env())
            self.assertEqual(m._build_git_env()["GIT_DIR"], "evil")

    def test_mutant_bypassing_local_config_allowlist_is_detected(self):
        m = load_source_module(
            "rpe04_mut_config",
            ((
                '    return len(observed) == len(expected) and set(observed) == set(expected)\n',
                '    return True\n',
            ),),
        )
        git(f"--git-dir={OBSERVER}", "config", "--local", "include.path", r"C:\evil-rpe04.cfg")
        out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")

    def test_mutant_ignoring_unexpected_namespace_ref_is_detected(self):
        m = load_source_module(
            "rpe04_mut_namespace",
            ((
                '    if refs != [_LOCAL_REF]:\n',
                '    if False:\n',
            ),),
        )
        first = m.observe_once(None)
        self.assertEqual(first["outcome"], "REMOTE_HEAD_OBSERVED")
        git(f"--git-dir={OBSERVER}", "update-ref", "refs/rpe04/extra", self.a)
        out = m.observe_once(self.a)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")

    def test_mutant_skipping_materialization_proof_is_detected(self):
        m = load_source_module(
            "rpe04_mut_materialized",
            ((
                '    observed_type = _materialized_object_type(observed_head)\n'
                '    if observed_type is None:\n'
                '        return _failure("OBSERVED_SHA_NOT_MATERIALIZED", attempt_started_at_ns, remote_done)\n'
                '    if observed_type != "commit":\n'
                '        return _failure("EXACT_OBSERVED_REF_NOT_COMMIT", attempt_started_at_ns, remote_done)\n',
                '    observed_type = "commit"\n',
            ),),
        )
        with mock.patch.object(m, "_extract_observed_sha", return_value="f" * 40):
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertEqual(out["transition_class"], "UNKNOWN")

    def test_mutant_laundering_unknown_as_fast_forward_is_detected(self):
        m = load_source_module(
            "rpe04_mut_transition",
            ((
                '    transition = _RPE03.classify_transition(\n'
                '        _OBSERVER,\n'
                '        previous_observed_head,\n'
                '        observed_head,\n'
                '        str(_GIT),\n'
                '    )\n',
                '    transition = "FAST_FORWARD"\n',
            ),),
        )
        out = m.observe_once("f" * 40)
        self.assertEqual(out["transition_class"], "FAST_FORWARD")
        self.assertFalse(out["blocked"])

    def test_mutant_dropping_no_write_fetch_head_breaks_exact_contract(self):
        m = load_source_module(
            "rpe04_mut_fetchhead",
            (('        "--no-write-fetch-head",\n', ''),),
        )
        self.assertNotIn("--no-write-fetch-head", m._build_fetch_argv())
        self.assertFalse(m._fetch_contract_exact())

    def test_mutant_dropping_local_plus_breaks_exact_contract(self):
        m = load_source_module(
            "rpe04_mut_plus",
            ((
                '        f"+{_SOURCE_REF}:{_LOCAL_REF}",\n',
                '        f"{_SOURCE_REF}:{_LOCAL_REF}",\n',
            ),),
        )
        self.assertFalse(m._fetch_contract_exact())

    def test_mutant_accepting_physical_escape_is_detected(self):
        m = load_source_module(
            "rpe04_mut_physical",
            (
                (
                    'def _is_indirection(path: Path) -> bool:\n'
                    '    try:\n',
                    'def _is_indirection(path: Path) -> bool:\n'
                    '    return False\n'
                    '    try:\n',
                ),
                (
                    'def _inside_root(path: Path, root: Path) -> bool:\n'
                    '    return path == root or root in path.parents\n',
                    'def _inside_root(path: Path, root: Path) -> bool:\n'
                    '    return True\n',
                ),
            ),
        )
        with tempfile.TemporaryDirectory(prefix="rpe04-mut-link-") as td:
            td = pathlib.Path(td)
            fake = td / "fake.git"
            target = td / "outside-objects"
            git("init", "--bare", str(fake))
            target.mkdir()
            (target / "pack").mkdir()
            (target / "info").mkdir()
            subprocess.run(["cmd.exe", "/c", "rmdir", "/s", "/q", str(fake / "objects")], check=True)
            link = fake / "objects"
            made = False
            try:
                os.symlink(target, link, target_is_directory=True)
                made = True
            except (OSError, NotImplementedError):
                cp = subprocess.run(
                    ["cmd.exe", "/c", "mklink", "/J", str(link), str(target)],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                made = cp.returncode == 0
            if not made:
                self.skipTest("platform cannot create symlink or junction")
            ok, code = m._verify_physical_object_domain(fake)
            self.assertTrue(ok, code)

    def test_mutant_accepting_uppercase_sha_is_detected(self):
        m = load_source_module(
            "rpe04_mut_sha",
            ((
                '    if type(observed_head) is not str or _SHA40_RE.fullmatch(observed_head) is None:\n',
                '    if False:\n',
            ),),
        )
        with mock.patch.object(m, "_extract_observed_sha", return_value=self.a.upper()):
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")


if __name__ == "__main__":
    unittest.main()
