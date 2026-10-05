from __future__ import annotations

import os
import pathlib
import shutil
import unittest
from unittest import mock

from tests.obsidian_projection.test_rpe04_real_remote_observation_adapter_v0_1 import (
    CONTROL,
    GIT,
    LOCAL_REF,
    MODULE,
    OBSERVER,
    PRODUCER,
    SOURCE,
    SOURCE_REF,
    git,
    init_fixture,
    load_file_module,
)


RPE03_V02 = pathlib.Path(__file__).resolve().parents[2] / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py"
RPE03_V02_BLOB = "5bbe455418fe1396ee5824379ad7450a1379cbba"


def raw_set_source_ref(oid: str) -> None:
    git(f"--git-dir={SOURCE}", "update-ref", "-d", SOURCE_REF, check=False)
    ref = SOURCE / "refs" / "heads" / "rpe04-source"
    ref.parent.mkdir(parents=True, exist_ok=True)
    ref.write_text(oid + "\n", encoding="ascii")


class TestRPE04RPE03V02RebindAndNF2(unittest.TestCase):
    def setUp(self):
        self.a = init_fixture()

    def tearDown(self):
        shutil.rmtree(CONTROL, ignore_errors=True)

    def m(self, name: str):
        return load_file_module(MODULE, name)

    def test_rpe03_runtime_binding_targets_exact_adopted_v02(self):
        m = self.m("rpe04_rebind_red")
        self.assertEqual(m._RPE03_PATH.name, "rpe03_ancestry_classifier_v0_2.py")
        self.assertEqual(
            git("-C", str(pathlib.Path(__file__).resolve().parents[2]), "hash-object", str(RPE03_V02)).stdout.strip(),
            RPE03_V02_BLOB,
        )

    def test_rpe03_v02_call_receives_governed_absolute_git_path(self):
        m = self.m("rpe04_rebind_call_red")
        captured = {}

        def fake(*args):
            captured["args"] = args
            return "INITIAL"

        with mock.patch.object(m._RPE03, "classify_transition", side_effect=fake):
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertEqual(len(captured["args"]), 4)
        self.assertEqual(captured["args"][3], str(GIT))

    def test_normal_commit_ref_remains_observed_tip(self):
        m = self.m("rpe04_nf2_commit")
        out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertEqual(out["observed_head"], self.a)
        self.assertEqual(out["evidence_label"], "OBSERVED_REMOTE_TIP")

    def test_annotated_tag_object_cannot_be_peeled_into_observed_tip(self):
        m = self.m("rpe04_nf2_tag")
        git("tag", "-a", "rpe04-annotated", "-m", "annotated", self.a, cwd=PRODUCER)
        tag_oid = git("rev-parse", "refs/tags/rpe04-annotated", cwd=PRODUCER).stdout.strip()
        peeled = git("rev-parse", "refs/tags/rpe04-annotated^{commit}", cwd=PRODUCER).stdout.strip()
        self.assertNotEqual(tag_oid, peeled)
        git("push", str(SOURCE), "refs/tags/rpe04-annotated:refs/tags/rpe04-annotated", cwd=PRODUCER)
        raw_set_source_ref(tag_oid)

        out = m.observe_once(None)

        self.assertEqual(out["outcome"], "READ_FAILURE")
        self.assertEqual(out["failure_code"], "EXACT_OBSERVED_REF_NOT_COMMIT")
        self.assertIsNone(out["observed_head"])
        self.assertNotEqual(out.get("observed_head"), peeled)

    def test_exact_local_ref_oid_is_not_peeled(self):
        m = self.m("rpe04_nf2_exact")
        git("tag", "-a", "rpe04-local-tag", "-m", "annotated", self.a, cwd=PRODUCER)
        tag_oid = git("rev-parse", "refs/tags/rpe04-local-tag", cwd=PRODUCER).stdout.strip()
        git("fetch", str(PRODUCER / ".git"), f"refs/tags/rpe04-local-tag:{LOCAL_REF}", cwd=OBSERVER)
        exact = m._extract_observed_sha()
        self.assertEqual(exact, tag_oid)


if __name__ == "__main__":
    unittest.main()
