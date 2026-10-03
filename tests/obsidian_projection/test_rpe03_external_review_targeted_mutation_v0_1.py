import os
import subprocess
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


ROOT=Path(__file__).resolve().parents[2]
MODULE=ROOT/"tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py"


def load(name,replacements=()):
    source=MODULE.read_text(encoding="utf-8")
    for old,new in replacements:
        if source.count(old) != 1:
            raise AssertionError(f"mutation anchor count != 1: {old!r}")
        source=source.replace(old,new,1)
    m=types.ModuleType(name); m.__file__=str(MODULE)
    exec(compile(source,str(MODULE),"exec"),m.__dict__)
    return m


def git(repo,*args,input_text=None):
    cp=subprocess.run(["git",*args],cwd=str(repo),input=input_text,text=True,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
    if cp.returncode != 0:
        raise AssertionError(cp.stderr)
    return cp.stdout.strip()


def make_graph():
    td=tempfile.TemporaryDirectory(); repo=Path(td.name)
    git(repo,"init"); git(repo,"config","user.email","mut@example.invalid"); git(repo,"config","user.name","Mut")
    (repo/"f").write_text("A\n",encoding="utf-8"); git(repo,"add","f"); git(repo,"commit","-m","A")
    a=git(repo,"rev-parse","HEAD")
    (repo/"f").write_text("B\n",encoding="utf-8"); git(repo,"commit","-am","B")
    b=git(repo,"rev-parse","HEAD")
    return td,repo,a,b


class TestRPE03ExternalReviewTargetedMutationV01(unittest.TestCase):
    def test_parent_discovery_confinement_mutant_is_killed(self):
        base=load("base_parent")
        old='''    else:
        top_text = _stdout_ok(_run_git(repo, "rev-parse", "--show-toplevel"))
        if not top_text:
            return None
        top = _canonical_path(top_text, repo)
        if not _same_path(top, repo):
            return None
        if not dot_git.is_dir():
            return None
        if not _same_path(git_dir, dot_git.resolve(strict=False)):
            return None
'''
        mut=load("mut_parent",((old,'''    else:
        pass
'''),))
        td,repo,a,b=make_graph()
        try:
            sub=repo/"plain"/"sub"; sub.mkdir(parents=True)
            self.assertEqual(base.classify_transition(sub,a,b),"UNKNOWN")
            self.assertEqual(mut.classify_transition(sub,a,b),"FAST_FORWARD")
        finally:
            td.cleanup()

    def test_gitfile_redirect_confinement_mutant_is_killed(self):
        base=load("base_gitfile")
        old='''    if dot_git.is_file():
        return None
'''
        main='''        top_text = _stdout_ok(_run_git(repo, "rev-parse", "--show-toplevel"))
        if not top_text:
            return None
        top = _canonical_path(top_text, repo)
        if not _same_path(top, repo):
            return None
        if not dot_git.is_dir():
            return None
        if not _same_path(git_dir, dot_git.resolve(strict=False)):
            return None
'''
        source=MODULE.read_text(encoding="utf-8")
        if source.count(old)!=1 or source.count(main)!=1:
            raise AssertionError("gitfile mutation anchors")
        source=source.replace(old,"",1).replace(main,"        pass\n",1)
        mut=types.ModuleType("mut_gitfile"); mut.__file__=str(MODULE)
        exec(compile(source,str(MODULE),"exec"),mut.__dict__)
        td,repo,a,b=make_graph(); redir_td=tempfile.TemporaryDirectory(); redir=Path(redir_td.name)
        try:
            gd=git(repo,"rev-parse","--absolute-git-dir")
            (redir/".git").write_text(f"gitdir: {gd}\n",encoding="utf-8")
            self.assertEqual(base.classify_transition(redir,a,b),"UNKNOWN")
            self.assertEqual(mut.classify_transition(redir,a,b),"FAST_FORWARD")
        finally:
            redir_td.cleanup(); td.cleanup()

    def test_commit_type_check_mutant_is_killed_by_annotated_tag(self):
        base=load("base_type")
        mut=load("mut_type",((
            '    return cp is not None and cp.returncode == 0 and cp.stdout.strip() == "commit"\n',
            '    return cp is not None and cp.returncode == 0\n',
        ),))
        td,repo,a,b=make_graph()
        try:
            git(repo,"tag","-a","tag-a",a,"-m","tag A")
            tag=git(repo,"rev-parse","tag-a")
            self.assertEqual(base.classify_transition(repo,tag,b),"UNKNOWN")
            self.assertEqual(mut.classify_transition(repo,tag,b),"FAST_FORWARD")
        finally:
            td.cleanup()

    def test_other_merge_base_exit_mapping_mutant_is_killed(self):
        base=load("base_exit")
        mut=load("mut_exit",((
            '    if cp.returncode == 1:\n        return "NON_FAST_FORWARD"\n    return "UNKNOWN"\n',
            '    if cp.returncode == 1:\n        return "NON_FAST_FORWARD"\n    return "NON_FAST_FORWARD"\n',
        ),))
        td,repo,a,b=make_graph()
        def force(module):
            original=module._run_git
            def wrapped(repo_path,*args):
                if args[:2] == ("merge-base","--is-ancestor"):
                    return subprocess.CompletedProcess(["git"],128,"","forced")
                return original(repo_path,*args)
            return wrapped
        try:
            with mock.patch.object(base,"_run_git",side_effect=force(base)):
                self.assertEqual(base.classify_transition(repo,a,b),"UNKNOWN")
            with mock.patch.object(mut,"_run_git",side_effect=force(mut)):
                self.assertEqual(mut.classify_transition(repo,a,b),"NON_FAST_FORWARD")
        finally:
            td.cleanup()

    def test_global_config_neutralization_mutant_is_killed(self):
        base=load("base_global")
        mut=load("mut_global",(('            "GIT_CONFIG_GLOBAL": os.devnull,\n',''),))
        td,repo,a,b=make_graph(); home_td=tempfile.TemporaryDirectory(); home=Path(home_td.name)
        bad=home/"bad.inc"; bad.write_text("[broken\n",encoding="utf-8")
        (home/".gitconfig").write_text(f"[include]\n\tpath = {bad.as_posix()}\n",encoding="utf-8")
        try:
            with mock.patch.dict(os.environ,{"HOME":str(home),"USERPROFILE":str(home)},clear=False):
                self.assertEqual(base.classify_transition(repo,a,b),"FAST_FORWARD")
                self.assertNotEqual(mut.classify_transition(repo,a,b),"FAST_FORWARD")
        finally:
            home_td.cleanup(); td.cleanup()


if __name__=="__main__":
    unittest.main()
