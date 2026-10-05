from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

from tests.obsidian_projection.test_rpe04_real_remote_observation_adapter_v0_1 import (
    CONTROL,
    MODULE,
    OBSERVER,
    init_fixture,
    load_file_module,
)


class TestRPE04NF3FullPhysicalDomain(unittest.TestCase):
    def setUp(self):
        self.a = init_fixture()

    def tearDown(self):
        shutil.rmtree(CONTROL, ignore_errors=True)

    def m(self, name: str):
        return load_file_module(MODULE, name)

    def test_normal_bare_domain_is_accepted(self):
        m = self.m("rpe04_nf3_normal")
        ok, code = m._verify_physical_object_domain(OBSERVER)
        self.assertTrue(ok, code)

    def test_refs_indirection_is_blocked(self):
        m = self.m("rpe04_nf3_refs")
        original = m._is_indirection

        def fake(path):
            if pathlib.Path(path) == OBSERVER / "refs":
                return True
            return original(path)

        with mock.patch.object(m, "_is_indirection", side_effect=fake):
            ok, code = m._verify_physical_object_domain(OBSERVER)
        self.assertFalse(ok)
        self.assertEqual(code, "PHYSICAL_GIT_DOMAIN_INDIRECTION")

    def test_refs_rpe04_indirection_is_blocked(self):
        m = self.m("rpe04_nf3_refs_rpe04")
        (OBSERVER / "refs" / "rpe04").mkdir(parents=True, exist_ok=True)
        original = m._is_indirection

        def fake(path):
            if pathlib.Path(path) == OBSERVER / "refs" / "rpe04":
                return True
            return original(path)

        with mock.patch.object(m, "_is_indirection", side_effect=fake):
            ok, code = m._verify_physical_object_domain(OBSERVER)
        self.assertFalse(ok)
        self.assertEqual(code, "PHYSICAL_GIT_DOMAIN_INDIRECTION")

    def test_config_head_and_packed_refs_indirection_are_blocked(self):
        m = self.m("rpe04_nf3_files")
        for rel in ("config", "HEAD", "packed-refs"):
            p = OBSERVER / rel
            if not p.exists():
                p.write_text("", encoding="ascii")
            original = m._is_indirection

            def fake(path, target=p):
                if pathlib.Path(path) == target:
                    return True
                return original(path)

            with mock.patch.object(m, "_is_indirection", side_effect=fake):
                ok, code = m._verify_physical_object_domain(OBSERVER)
            self.assertFalse(ok, rel)
            self.assertEqual(code, "PHYSICAL_GIT_DOMAIN_INDIRECTION")

    def test_objects_info_alternates_presence_is_blocked(self):
        m = self.m("rpe04_nf3_alternates")
        alt = OBSERVER / "objects" / "info" / "alternates"
        alt.write_text(r"C:\outside-object-store" + "\n", encoding="ascii")
        ok, code = m._verify_physical_object_domain(OBSERVER)
        self.assertFalse(ok)
        self.assertEqual(code, "PHYSICAL_GIT_DOMAIN_ALTERNATES_FORBIDDEN")

    def test_pack_file_level_indirection_is_blocked_by_recursive_walk(self):
        m = self.m("rpe04_nf3_pack_file")
        pack = OBSERVER / "objects" / "pack" / "pack-test.pack"
        pack.write_bytes(b"fixture")
        original = m._is_indirection

        def fake(path):
            if pathlib.Path(path) == pack:
                return True
            return original(path)

        with mock.patch.object(m, "_is_indirection", side_effect=fake):
            ok, code = m._verify_physical_object_domain(OBSERVER)
        self.assertFalse(ok)
        self.assertEqual(code, "PHYSICAL_GIT_DOMAIN_INDIRECTION")

    def test_post_fetch_alternates_change_blocks_before_positive_observation(self):
        m = self.m("rpe04_nf3_post_fetch")
        original_fetch = m._run_fetch

        def mutate_after_fetch():
            cp = original_fetch()
            alt = OBSERVER / "objects" / "info" / "alternates"
            alt.write_text(r"C:\outside-object-store" + "\n", encoding="ascii")
            return cp

        with mock.patch.object(m, "_run_fetch", side_effect=mutate_after_fetch):
            out = m.observe_once(None)

        self.assertEqual(out["outcome"], "READ_FAILURE")
        self.assertEqual(out["failure_code"], "PHYSICAL_GIT_DOMAIN_ALTERNATES_FORBIDDEN")


if __name__ == "__main__":
    unittest.main()
