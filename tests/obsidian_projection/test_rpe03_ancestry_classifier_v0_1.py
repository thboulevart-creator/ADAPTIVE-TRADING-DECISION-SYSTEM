import importlib.util
import inspect
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py"
PREREG = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1.json"
SCHEMA = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1_schema_v0_1.json"
GUARD = ROOT / "tools/obsidian_projection/rpe01_governed_closed_schema.py"
MISSING = "f" * 40


def load(path, name):
    if not path.exists():
        raise AssertionError(f"required module missing: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def git(repo, *args, input_text=None):
    cp = subprocess.run(["git", *args], cwd=str(repo), input=input_text, text=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if cp.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {cp.stderr}")
    return cp.stdout.strip()


def make_graph():
    td = tempfile.TemporaryDirectory()
    repo = Path(td.name)
    git(repo, "init")
    git(repo, "config", "user.email", "rpe03@example.invalid")
    git(repo, "config", "user.name", "RPE03")
    (repo/"f.txt").write_text("A\n", encoding="utf-8")
    git(repo, "add", "f.txt"); git(repo, "commit", "-m", "A")
    a = git(repo, "rev-parse", "HEAD")
    (repo/"f.txt").write_text("B\n", encoding="utf-8")
    git(repo, "commit", "-am", "B")
    b = git(repo, "rev-parse", "HEAD")
    git(repo, "checkout", "-b", "side", a)
    (repo/"g.txt").write_text("C\n", encoding="utf-8")
    git(repo, "add", "g.txt"); git(repo, "commit", "-m", "C")
    c = git(repo, "rev-parse", "HEAD")
    git(repo, "checkout", "-")
    return td, repo, a, b, c


class TestRPE03AncestryClassifierV01(unittest.TestCase):
    def test_preregistration_is_rpe01_guarded(self):
        g=load(GUARD,"rpe01_guard_for_rpe03")
        d=g.validate_governed_json(PREREG.read_text(encoding="utf-8"),SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(d["classification"]["outputs"],["INITIAL","SAME","FAST_FORWARD","NON_FAST_FORWARD","UNKNOWN"])

    def test_static_source_has_no_network_commands_or_network_modules(self):
        source=MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""
        for forbidden in ("fetch","ls-remote","urllib","socket","requests","http.client"):
            self.assertNotIn(forbidden,source)

    def test_caller_cannot_supply_transition_class(self):
        m=load(MODULE,"rpe03_sig")
        params=set(inspect.signature(m.classify_transition).parameters)
        self.assertEqual(params,{"repo_path","previous_observed_head","new_exact_observed_head"})

    def test_initial_same_fast_forward_rollback_and_divergent(self):
        m=load(MODULE,"rpe03_graph")
        td,repo,a,b,c=make_graph()
        try:
            self.assertEqual(m.classify_transition(repo,None,a),"INITIAL")
            self.assertEqual(m.classify_transition(repo,a,a),"SAME")
            self.assertEqual(m.classify_transition(repo,a,b),"FAST_FORWARD")
            self.assertEqual(m.classify_transition(repo,b,a),"NON_FAST_FORWARD")
            self.assertEqual(m.classify_transition(repo,b,c),"NON_FAST_FORWARD")
        finally: td.cleanup()

    def test_missing_previous_and_new_are_unknown(self):
        m=load(MODULE,"rpe03_missing")
        td,repo,a,b,c=make_graph()
        try:
            self.assertEqual(m.classify_transition(repo,MISSING,b),"UNKNOWN")
            self.assertEqual(m.classify_transition(repo,a,MISSING),"UNKNOWN")
        finally: td.cleanup()

    def test_non_commit_object_is_unknown(self):
        m=load(MODULE,"rpe03_blob")
        td,repo,a,b,c=make_graph()
        try:
            blob=git(repo,"hash-object","-w","--stdin",input_text="blob")
            self.assertEqual(m.classify_transition(repo,a,blob),"UNKNOWN")
        finally: td.cleanup()

    def test_shallow_domain_is_unknown(self):
        m=load(MODULE,"rpe03_shallow")
        td,repo,a,b,c=make_graph()
        try:
            gd=Path(git(repo,"rev-parse","--absolute-git-dir"))
            (gd/"shallow").write_text(b+"\n",encoding="ascii")
            self.assertEqual(m.classify_transition(repo,a,b),"UNKNOWN")
        finally: td.cleanup()

    def test_graft_domain_is_unknown(self):
        m=load(MODULE,"rpe03_graft")
        td,repo,a,b,c=make_graph()
        try:
            gd=Path(git(repo,"rev-parse","--absolute-git-dir"))
            (gd/"info").mkdir(exist_ok=True)
            (gd/"info"/"grafts").write_text(b+" "+a+"\n",encoding="ascii")
            self.assertEqual(m.classify_transition(repo,a,b),"UNKNOWN")
        finally: td.cleanup()

    def test_alternates_domain_is_unknown(self):
        m=load(MODULE,"rpe03_alt")
        td,repo,a,b,c=make_graph()
        other=tempfile.TemporaryDirectory()
        try:
            gd=Path(git(repo,"rev-parse","--absolute-git-dir"))
            p=gd/"objects"/"info"/"alternates"; p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(other.name+"\n",encoding="utf-8")
            self.assertEqual(m.classify_transition(repo,a,b),"UNKNOWN")
        finally:
            other.cleanup(); td.cleanup()

    def test_inherited_git_environment_is_neutralized(self):
        m=load(MODULE,"rpe03_env")
        td,repo,a,b,c=make_graph()
        try:
            with mock.patch.dict(os.environ,{
                "GIT_DIR":"X:/forbidden",
                "GIT_OBJECT_DIRECTORY":"X:/forbidden-objects",
                "GIT_ALTERNATE_OBJECT_DIRECTORIES":"X:/forbidden-alt",
                "GIT_REPLACE_REF_BASE":"refs/evil/",
            },clear=False):
                self.assertEqual(m.classify_transition(repo,a,b),"FAST_FORWARD")
        finally: td.cleanup()

    def test_replace_ref_cannot_alter_ancestry(self):
        m=load(MODULE,"rpe03_replace")
        td,repo,a,b,c=make_graph()
        try:
            git(repo,"replace",a,c)
            self.assertEqual(m.classify_transition(repo,a,b),"FAST_FORWARD")
        finally: td.cleanup()

    def test_timeout_is_unknown(self):
        m=load(MODULE,"rpe03_timeout")
        with mock.patch.object(m.subprocess,"run",side_effect=subprocess.TimeoutExpired(["git"],5)):
            self.assertEqual(m.classify_transition(Path("."),None,"a"*40),"UNKNOWN")

    def test_corrupt_requested_object_is_unknown(self):
        m=load(MODULE,"rpe03_corrupt")
        td,repo,a,b,c=make_graph()
        try:
            gd=Path(git(repo,"rev-parse","--absolute-git-dir"))
            obj=gd/"objects"/b[:2]/b[2:]
            self.assertTrue(obj.exists())
            obj.unlink()
            self.assertEqual(m.classify_transition(repo,a,b),"UNKNOWN")
        finally: td.cleanup()

    def test_linked_worktree_domain_is_unknown(self):
        m=load(MODULE,"rpe03_worktree")
        td,repo,a,b,c=make_graph(); wtd=tempfile.TemporaryDirectory(); wt=Path(wtd.name)/"linked"
        try:
            git(repo,"worktree","add","-b","linked-test",str(wt),a)
            self.assertEqual(m.classify_transition(wt,None,a),"UNKNOWN")
        finally:
            subprocess.run(["git","worktree","remove","--force",str(wt)],cwd=str(repo),capture_output=True,text=True)
            wtd.cleanup(); td.cleanup()

    def test_commands_disable_commit_graph_and_environment_is_sanitized(self):
        m=load(MODULE,"rpe03_cmd")
        td,repo,a,b,c=make_graph()
        calls=[]; original=m.subprocess.run
        def wrapped(*args,**kwargs):
            calls.append((args,kwargs))
            return original(*args,**kwargs)
        try:
            with mock.patch.object(m.subprocess,"run",side_effect=wrapped):
                self.assertEqual(m.classify_transition(repo,a,b),"FAST_FORWARD")
            self.assertTrue(calls)
            for args,kwargs in calls:
                cmd=list(args[0])
                self.assertIn("core.commitGraph=false",cmd)
                env=kwargs["env"]
                self.assertEqual(env["GIT_NO_REPLACE_OBJECTS"],"1")
                self.assertEqual(env["GIT_CONFIG_NOSYSTEM"],"1")
                self.assertEqual(env["GIT_TERMINAL_PROMPT"],"0")
                self.assertFalse(any(k.startswith("GIT_") and k not in {"GIT_NO_REPLACE_OBJECTS","GIT_CONFIG_NOSYSTEM","GIT_CONFIG_GLOBAL","GIT_TERMINAL_PROMPT","GIT_OPTIONAL_LOCKS"} for k in env))
        finally: td.cleanup()

    def test_invalid_head_format_is_unknown(self):
        m=load(MODULE,"rpe03_invalid")
        td,repo,a,b,c=make_graph()
        try:
            for bad in ("HEAD","A"*40,"123",None,True):
                with self.subTest(bad=bad):
                    self.assertEqual(m.classify_transition(repo,a,bad),"UNKNOWN")
        finally: td.cleanup()


if __name__ == "__main__":
    unittest.main()
