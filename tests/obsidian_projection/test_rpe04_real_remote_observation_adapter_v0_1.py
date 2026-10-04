from __future__ import annotations

import importlib.util
import inspect
import json
import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_v0_1.py"
PREREG = ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_preregistration_v0_1.json"
SCHEMA = ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_preregistration_v0_1_schema_v0_1.json"
GUARD = ROOT / "tools/obsidian_projection/rpe01_governed_closed_schema.py"

GIT = pathlib.Path(r"C:\Program Files\Git\cmd\git.exe")
CONTROL = pathlib.Path(r"C:\Users\Boulevart\ATDS-CONTROL\RPE04-QUALIFICATION")
SOURCE = CONTROL / "source.git"
OBSERVER = CONTROL / "observer.git"
PRODUCER = CONTROL / "producer"
SOURCE_REF = "refs/heads/rpe04-source"
LOCAL_REF = "refs/rpe04/observed"


def load_file_module(path: pathlib.Path, name: str):
    if not path.exists():
        raise AssertionError(f"required implementation missing: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def clean_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_REPLACE_OBJECTS": "1",
    })
    return env


def git(*args: str, cwd: pathlib.Path | None = None, check: bool = True):
    cp = subprocess.run(
        [str(GIT), *args],
        cwd=str(cwd) if cwd else None,
        env=clean_env(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and cp.returncode != 0:
        raise AssertionError(f"git failed {args}: {cp.stderr}")
    return cp


def init_fixture():
    shutil.rmtree(CONTROL, ignore_errors=True)
    CONTROL.mkdir(parents=True, exist_ok=True)
    git("init", "--bare", str(SOURCE))
    git("init", "--bare", str(OBSERVER))
    git("init", str(PRODUCER))
    git("config", "user.name", "RPE04 Fixture", cwd=PRODUCER)
    git("config", "user.email", "rpe04@example.invalid", cwd=PRODUCER)
    (PRODUCER / "trace.txt").write_text("A\n", encoding="utf-8")
    git("add", "trace.txt", cwd=PRODUCER)
    git("commit", "-m", "A", cwd=PRODUCER)
    a = git("rev-parse", "HEAD", cwd=PRODUCER).stdout.strip()
    git("push", str(SOURCE), f"{a}:{SOURCE_REF}", cwd=PRODUCER)
    return a


def new_commit(label: str):
    with (PRODUCER / "trace.txt").open("a", encoding="utf-8") as fh:
        fh.write(label + "\n")
    git("add", "trace.txt", cwd=PRODUCER)
    git("commit", "-m", label, cwd=PRODUCER)
    return git("rev-parse", "HEAD", cwd=PRODUCER).stdout.strip()


def publish(sha: str):
    temp_ref = "refs/heads/rpe04-stage"
    git("push", str(SOURCE), f"{sha}:{temp_ref}", cwd=PRODUCER)
    git(f"--git-dir={SOURCE}", "update-ref", SOURCE_REF, sha)
    git(f"--git-dir={SOURCE}", "update-ref", "-d", temp_ref)


class TestRPE04Preregistration(unittest.TestCase):
    def test_preregistration_is_governed_by_rpe01_public_entrypoint(self):
        guard = load_file_module(GUARD, "rpe04_guard")
        raw = PREREG.read_text(encoding="utf-8")
        schema = SCHEMA.read_text(encoding="utf-8")
        guard.validate_governed_json(raw, schema)

    def test_preregistration_pins_git_identity_and_local_only_scope(self):
        p = json.loads(PREREG.read_text(encoding="utf-8"))
        self.assertEqual(p["git_executable"]["resolved_path"], str(GIT))
        self.assertEqual(p["git_executable"]["observed_version"], "git version 2.54.0.windows.1")
        self.assertFalse(p["authority"]["github_polling_authorized"])
        self.assertFalse(p["authority"]["external_network_qualification_authorized"])
        self.assertFalse(p["authority"]["remote_push_authorized"])


class TestRPE04Adapter(unittest.TestCase):
    def setUp(self):
        self.a = init_fixture()

    def tearDown(self):
        shutil.rmtree(CONTROL, ignore_errors=True)

    def m(self, name="rpe04_adapter"):
        return load_file_module(MODULE, name)

    def test_public_interface_cannot_accept_observed_head_transition_or_containment(self):
        m = self.m()
        params = list(inspect.signature(m.observe_once).parameters)
        self.assertEqual(params, ["previous_observed_head"])

    def test_initial_observation_is_exact_remote_tip(self):
        m = self.m()
        out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertEqual(out["event_type"], "REMOTE_HEAD_OBSERVED")
        self.assertEqual(out["evidence_label"], "OBSERVED_REMOTE_TIP")
        self.assertEqual(out["observed_head"], self.a)
        self.assertEqual(out["transition_class"], "INITIAL")
        self.assertFalse(out["blocked"])
        self.assertRegex(out["observed_head"], r"^[0-9a-f]{40}$")

    def test_timestamp_order_is_integer_monotonic_nanoseconds(self):
        m = self.m()
        out = m.observe_once(None)
        fields = [
            out["attempt_started_at_ns"],
            out["remote_observation_completed_at_ns"],
            out["attempt_completed_at_ns"],
        ]
        self.assertTrue(all(type(x) is int for x in fields))
        self.assertLessEqual(fields[0], fields[1])
        self.assertLessEqual(fields[1], fields[2])

    def test_one_fetch_transaction_per_attempt(self):
        m = self.m()
        original = m._run_fetch
        with mock.patch.object(m, "_run_fetch", wraps=original) as wrapped:
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertEqual(wrapped.call_count, 1)

    def test_fast_forward_transition_is_derived_by_rpe03(self):
        m = self.m()
        first = m.observe_once(None)
        b = new_commit("B")
        publish(b)
        second = m.observe_once(first["observed_head"])
        self.assertEqual(second["observed_head"], b)
        self.assertEqual(second["transition_class"], "FAST_FORWARD")

    def test_non_fast_forward_local_namespace_update_is_supported(self):
        m = self.m()
        b = new_commit("B")
        publish(b)
        first = m.observe_once(None)
        self.assertEqual(first["observed_head"], b)
        git(f"--git-dir={SOURCE}", "update-ref", SOURCE_REF, self.a)
        second = m.observe_once(b)
        self.assertEqual(second["observed_head"], self.a)
        self.assertEqual(second["transition_class"], "NON_FAST_FORWARD")

    def test_contained_history_is_not_laundered_as_observed_tip(self):
        m = self.m()
        b = new_commit("B")
        publish(b)
        out = m.observe_once(None)
        self.assertEqual(out["observed_head"], b)
        self.assertNotIn(self.a, json.dumps(out, sort_keys=True))

    def test_missing_remote_ref_fails_closed(self):
        m = self.m()
        git(f"--git-dir={SOURCE}", "update-ref", "-d", SOURCE_REF)
        out = m.observe_once(None)
        self.assertEqual(out["outcome"], "READ_FAILURE")
        self.assertEqual(out["failure_code"], "REMOTE_FETCH_FAILED")

    def test_timeout_fails_closed(self):
        m = self.m()
        with mock.patch.object(
            m,
            "_run_fetch",
            side_effect=subprocess.TimeoutExpired(cmd=["git", "fetch"], timeout=5),
        ):
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "READ_FAILURE")
        self.assertEqual(out["failure_code"], "REMOTE_FETCH_TIMEOUT")

    def test_unexpected_observation_namespace_ref_blocks(self):
        m = self.m()
        first = m.observe_once(None)
        self.assertEqual(first["outcome"], "REMOTE_HEAD_OBSERVED")
        git(f"--git-dir={OBSERVER}", "update-ref", "refs/rpe04/extra", self.a)
        out = m.observe_once(self.a)
        self.assertEqual(out["outcome"], "READ_FAILURE")
        self.assertEqual(out["failure_code"], "UNEXPECTED_OBSERVATION_NAMESPACE")

    def test_malformed_observed_sha_blocks(self):
        m = self.m()
        with mock.patch.object(m, "_extract_observed_sha", return_value="A" * 40):
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "READ_FAILURE")
        self.assertEqual(out["failure_code"], "MALFORMED_OBSERVED_SHA")

    def test_observed_sha_not_materialized_blocks(self):
        m = self.m()
        with mock.patch.object(m, "_extract_observed_sha", return_value="f" * 40):
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "READ_FAILURE")
        self.assertEqual(out["failure_code"], "OBSERVED_SHA_NOT_MATERIALIZED")

    def test_rpe03_unknown_propagates_as_blocked_not_positive_transition(self):
        m = self.m()
        out = m.observe_once("f" * 40)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertEqual(out["transition_class"], "UNKNOWN")
        self.assertTrue(out["blocked"])
        self.assertEqual(out["failure_code"], "ANCESTRY_UNKNOWN")

    def test_local_include_path_is_rejected(self):
        m = self.m()
        git(f"--git-dir={OBSERVER}", "config", "--local", "include.path", r"C:\evil-rpe04.cfg")
        out = m.observe_once(None)
        self.assertEqual(out["outcome"], "READ_FAILURE")
        self.assertEqual(out["failure_code"], "LOCAL_CONFIG_NOT_ALLOWLISTED")

    def test_local_include_if_is_rejected(self):
        m = self.m()
        git(
            f"--git-dir={OBSERVER}",
            "config",
            "--local",
            'includeIf.gitdir:C:/tmp/.path',
            r"C:\evil-rpe04.cfg",
        )
        out = m.observe_once(None)
        self.assertEqual(out["outcome"], "READ_FAILURE")
        self.assertEqual(out["failure_code"], "LOCAL_CONFIG_NOT_ALLOWLISTED")

    def test_inherited_global_config_and_url_insteadof_are_neutralized(self):
        m = self.m()
        with tempfile.TemporaryDirectory() as td:
            hostile = pathlib.Path(td) / "global.gitconfig"
            hostile.write_text(
                '[url "C:/definitely-wrong/"]\n\tinsteadOf = C:/Users/Boulevart/ATDS-CONTROL/RPE04-QUALIFICATION/\n',
                encoding="utf-8",
            )
            with mock.patch.dict(
                os.environ,
                {
                    "GIT_CONFIG_GLOBAL": str(hostile),
                    "GIT_DIR": r"C:\definitely-wrong",
                    "GIT_OBJECT_DIRECTORY": r"C:\definitely-wrong-objects",
                },
                clear=False,
            ):
                out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertEqual(out["observed_head"], self.a)

    def test_git_environment_strips_inherited_git_authority(self):
        m = self.m()
        with mock.patch.dict(
            os.environ,
            {"GIT_DIR": "evil", "GIT_CONFIG_SYSTEM": "evil", "GIT_TERMINAL_PROMPT": "1"},
            clear=False,
        ):
            env = m._build_git_env()
        self.assertNotEqual(env.get("GIT_DIR"), "evil")
        self.assertNotEqual(env.get("GIT_CONFIG_SYSTEM"), "evil")
        self.assertEqual(env["GIT_CONFIG_NOSYSTEM"], "1")
        self.assertEqual(env["GIT_CONFIG_GLOBAL"], "NUL")
        self.assertEqual(env["GIT_TERMINAL_PROMPT"], "0")

    def test_fetch_argv_is_exact_and_disables_tags_submodules_fetch_head_and_hooks(self):
        m = self.m()
        argv = m._build_fetch_argv()
        self.assertEqual(argv[0], str(GIT))
        self.assertIn("core.hooksPath=NUL", argv)
        self.assertIn("gc.auto=0", argv)
        self.assertIn("--no-tags", argv)
        self.assertIn("--no-recurse-submodules", argv)
        self.assertIn("--no-write-fetch-head", argv)
        self.assertEqual(argv[-1], "+refs/heads/rpe04-source:refs/rpe04/observed")
        self.assertNotIn("ls-remote", argv)

    def test_git_executable_identity_is_verified(self):
        m = self.m()
        self.assertTrue(m._verify_git_executable_identity())
        with mock.patch.object(m, "_sha256_file", return_value="0" * 64):
            self.assertFalse(m._verify_git_executable_identity())

    def test_physical_object_domain_accepts_normal_bare_repo(self):
        m = self.m()
        ok, code = m._verify_physical_object_domain(OBSERVER)
        self.assertTrue(ok, code)

    def test_physical_object_domain_rejects_actual_indirection(self):
        m = self.m()
        with tempfile.TemporaryDirectory(prefix="rpe04-link-") as td:
            td = pathlib.Path(td)
            fake = td / "fake.git"
            target = td / "outside-objects"
            fake.mkdir()
            target.mkdir()
            (target / "pack").mkdir()
            (target / "info").mkdir()
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
            self.assertFalse(ok)
            self.assertEqual(code, "PHYSICAL_OBJECT_DOMAIN_INDIRECTION")

    def test_exact_observed_sha_only_no_intermediate_injection(self):
        m = self.m()
        b = new_commit("B")
        publish(b)
        out = m.observe_once(None)
        self.assertEqual(
            set(out),
            {
                "outcome",
                "event_type",
                "evidence_label",
                "observed_head",
                "transition_class",
                "attempt_started_at_ns",
                "remote_observation_completed_at_ns",
                "attempt_completed_at_ns",
                "blocked",
                "failure_code",
            },
        )
        self.assertEqual(out["observed_head"], b)


if __name__ == "__main__":
    unittest.main()
