import importlib.util
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py"


def load():
    spec=importlib.util.spec_from_file_location("rpe03_targeted",MODULE)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load RPE-03 module")
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def git(repo,*args,input_text=None):
    cp=subprocess.run(["git",*args],cwd=str(repo),input=input_text,text=True,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
    if cp.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {cp.stderr}")
    return cp.stdout.strip()


def make_linear_graph():
    td=tempfile.TemporaryDirectory()
    repo=Path(td.name)
    git(repo,"init")
    git(repo,"config","user.email","rpe03-targeted@example.invalid")
    git(repo,"config","user.name","RPE03 Targeted")
    (repo/"f.txt").write_text("A\n",encoding="utf-8")
    git(repo,"add","f.txt"); git(repo,"commit","-m","A")
    a=git(repo,"rev-parse","HEAD")
    (repo/"f.txt").write_text("B\n",encoding="utf-8")
    git(repo,"commit","-am","B")
    b=git(repo,"rev-parse","HEAD")
    return td,repo,a,b


def make_three_commit_graph():
    td,repo,a,b=make_linear_graph()
    (repo/"f.txt").write_text("C\n",encoding="utf-8")
    git(repo,"commit","-am","C")
    c=git(repo,"rev-parse","HEAD")
    return td,repo,a,b,c


class TestRPE03ExternalReviewTargetedClosureV01(unittest.TestCase):
    def test_supplied_subdirectory_of_parent_repository_is_unknown(self):
        m=load()
        td,repo,a,b=make_linear_graph()
        try:
            sub=repo/"plain"/"sub"
            sub.mkdir(parents=True)
            self.assertEqual(m.classify_transition(sub,a,b),"UNKNOWN")
        finally:
            td.cleanup()

    def test_gitfile_redirecting_to_other_repository_is_unknown(self):
        m=load()
        td,repo,a,b=make_linear_graph()
        redirect_td=tempfile.TemporaryDirectory()
        redirect=Path(redirect_td.name)
        try:
            git_dir=git(repo,"rev-parse","--absolute-git-dir")
            (redirect/".git").write_text(f"gitdir: {git_dir}\n",encoding="utf-8")
            self.assertEqual(m.classify_transition(redirect,a,b),"UNKNOWN")
        finally:
            redirect_td.cleanup()
            td.cleanup()

    def test_main_worktree_root_remains_allowed(self):
        m=load()
        td,repo,a,b=make_linear_graph()
        try:
            self.assertEqual(m.classify_transition(repo,a,b),"FAST_FORWARD")
        finally:
            td.cleanup()

    def test_bare_repository_root_is_allowed(self):
        m=load()
        td,repo,a,b=make_linear_graph()
        bare_td=tempfile.TemporaryDirectory()
        bare=Path(bare_td.name)/"repo.git"
        try:
            git(repo,"clone","--bare",str(repo),str(bare))
            self.assertEqual(m.classify_transition(bare,a,b),"FAST_FORWARD")
        finally:
            bare_td.cleanup()
            td.cleanup()

    def test_annotated_tag_as_previous_is_unknown(self):
        m=load()
        td,repo,a,b=make_linear_graph()
        try:
            git(repo,"tag","-a","tag-a",a,"-m","tag A")
            tag_sha=git(repo,"rev-parse","tag-a")
            self.assertNotEqual(tag_sha,a)
            self.assertEqual(m.classify_transition(repo,tag_sha,b),"UNKNOWN")
        finally:
            td.cleanup()

    def test_previous_blob_is_unknown(self):
        m=load()
        td,repo,a,b=make_linear_graph()
        try:
            blob=git(repo,"hash-object","-w","--stdin",input_text="blob")
            self.assertEqual(m.classify_transition(repo,blob,b),"UNKNOWN")
        finally:
            td.cleanup()

    def test_merge_base_exit_other_than_zero_or_one_is_unknown(self):
        m=load()
        td,repo,a,b=make_linear_graph()
        original=m._run_git
        def wrapped(repo_path,*args):
            if args[:2] == ("merge-base","--is-ancestor"):
                return subprocess.CompletedProcess(["git"],128,"","forced error")
            return original(repo_path,*args)
        try:
            with mock.patch.object(m,"_run_git",side_effect=wrapped):
                self.assertEqual(m.classify_transition(repo,a,b),"UNKNOWN")
        finally:
            td.cleanup()

    def test_corrupted_intermediate_ancestry_object_is_unknown(self):
        m=load()
        td,repo,a,b,c=make_three_commit_graph()
        try:
            gd=Path(git(repo,"rev-parse","--absolute-git-dir"))
            obj=gd/"objects"/b[:2]/b[2:]
            self.assertTrue(obj.exists())
            os.chmod(obj,stat.S_IWRITE)
            obj.write_bytes(b"corrupt-intermediate")
            self.assertEqual(m.classify_transition(repo,a,c),"UNKNOWN")
        finally:
            td.cleanup()

    def test_hostile_global_git_config_does_not_influence(self):
        m=load()
        td,repo,a,b=make_linear_graph()
        home_td=tempfile.TemporaryDirectory()
        home=Path(home_td.name)
        bad=home/"bad.inc"
        bad.write_text("[broken\n",encoding="utf-8")
        (home/".gitconfig").write_text(f"[include]\n\tpath = {bad.as_posix()}\n",encoding="utf-8")
        try:
            with mock.patch.dict(os.environ,{"HOME":str(home),"USERPROFILE":str(home)},clear=False):
                self.assertEqual(m.classify_transition(repo,a,b),"FAST_FORWARD")
        finally:
            home_td.cleanup()
            td.cleanup()


if __name__ == "__main__":
    unittest.main()
