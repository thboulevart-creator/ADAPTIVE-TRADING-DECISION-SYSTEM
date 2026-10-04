from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py"
RPE04_GOVERNED_GIT = r"C:\Program Files\Git\cmd\git.exe"


def load_module():
    spec = importlib.util.spec_from_file_location("rpe03_v02_for_rpe04", MODULE)
    m = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(m)
    return m


class TestRPE04CallSiteCompatibilityWithRPE03V02(unittest.TestCase):
    def test_rpe04_can_supply_its_governed_absolute_git_identity(self):
        m = load_module()
        with tempfile.TemporaryDirectory(prefix="rpe04-rpe03v02-") as td:
            repo = pathlib.Path(td) / "repo"
            subprocess.run([RPE04_GOVERNED_GIT, "init", str(repo)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run([RPE04_GOVERNED_GIT, "-C", str(repo), "config", "user.name", "compat"], check=True)
            subprocess.run([RPE04_GOVERNED_GIT, "-C", str(repo), "config", "user.email", "compat@example.invalid"], check=True)
            (repo / "x").write_text("a", encoding="utf-8")
            subprocess.run([RPE04_GOVERNED_GIT, "-C", str(repo), "add", "x"], check=True)
            subprocess.run([RPE04_GOVERNED_GIT, "-C", str(repo), "commit", "-m", "a"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            a = subprocess.run([RPE04_GOVERNED_GIT, "-C", str(repo), "rev-parse", "HEAD"], check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
            (repo / "x").write_text("b", encoding="utf-8")
            subprocess.run([RPE04_GOVERNED_GIT, "-C", str(repo), "add", "x"], check=True)
            subprocess.run([RPE04_GOVERNED_GIT, "-C", str(repo), "commit", "-m", "b"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            b = subprocess.run([RPE04_GOVERNED_GIT, "-C", str(repo), "rev-parse", "HEAD"], check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
            self.assertEqual(
                m.classify_transition(repo, a, b, RPE04_GOVERNED_GIT),
                "FAST_FORWARD",
            )


if __name__ == "__main__":
    unittest.main()
