from __future__ import annotations

import importlib.util
import pathlib
import unittest
from unittest import mock

from tests.obsidian_projection.test_rpe04_real_remote_observation_adapter_v0_1 import (
    init_fixture,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_v0_1.py"


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TestRPE04RuntimeBindingHardening(unittest.TestCase):
    def setUp(self):
        self.a = init_fixture()

    def tearDown(self):
        import shutil
        shutil.rmtree(
            pathlib.Path(r"C:\Users\Boulevart\ATDS-CONTROL\RPE04-QUALIFICATION"),
            ignore_errors=True,
        )

    def test_governed_runtime_dependencies_are_raw_sha256_bound(self):
        m = load_module("rpe04_binding_base")
        self.assertTrue(m._verify_runtime_bindings())
        self.assertEqual(
            m._EXPECTED_RUNTIME_SHA256["preregistration"],
            "0c59111fe90b8d80f0c41daf0911d772274eca733c6e68673d484ab8abf2c6ba",
        )
        self.assertEqual(
            m._EXPECTED_RUNTIME_SHA256["schema"],
            "e39dbc4f3bc82f5d5c2181574bdd120ad6d0fca46bcfdf358fac406b572a8861",
        )
        self.assertEqual(
            m._EXPECTED_RUNTIME_SHA256["rpe01_guard"],
            "24b36f5b3c0a02bc6247732fe1fa23d6c0fe30bc2b1629a7c54d4c094a628298",
        )
        self.assertEqual(
            m._EXPECTED_RUNTIME_SHA256["rpe03_classifier"],
            "4b743e187245585f4a4d9c923e316961f2842f96634d04dcac01972a29e60b41",
        )

    def test_runtime_binding_mismatch_fails_closed(self):
        m = load_module("rpe04_binding_mut")
        original = m._sha256_file

        def fake(path):
            if pathlib.Path(path) == m._RPE03_PATH:
                return "0" * 64
            return original(path)

        with mock.patch.object(m, "_raw_sha256_file", side_effect=fake):
            self.assertFalse(m._verify_runtime_bindings())

    def test_physical_domain_is_reverified_after_fetch(self):
        m = load_module("rpe04_binding_physical")
        with mock.patch.object(
            m,
            "_verify_physical_object_domain",
            wraps=m._verify_physical_object_domain,
        ) as wrapped:
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertGreaterEqual(wrapped.call_count, 2)

    def test_git_identity_is_reverified_before_rpe03_classification(self):
        m = load_module("rpe04_binding_git")
        with mock.patch.object(
            m,
            "_verify_git_executable_identity",
            wraps=m._verify_git_executable_identity,
        ) as wrapped:
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertGreaterEqual(wrapped.call_count, 2)

    def test_local_config_is_reverified_before_rpe03_classification(self):
        m = load_module("rpe04_binding_config")
        with mock.patch.object(
            m,
            "_verify_local_config_allowlist",
            wraps=m._verify_local_config_allowlist,
        ) as wrapped:
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertGreaterEqual(wrapped.call_count, 2)


if __name__ == "__main__":
    unittest.main()
