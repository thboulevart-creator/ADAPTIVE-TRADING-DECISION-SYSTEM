# RPE-03 — EXTERNAL REVIEW TARGETED CLOSURE V0.1 — DELTA REVIEW PACKET

Date: 2026-10-03

## Mandate

Review only the targeted closure following the prior RPE-03 external review.

Prior verdict:
VERDICT = PASS_WITH_NON_BLOCKING_NOTES
BLOCKING_FINDINGS = NONE

Candidate status:
RPE-03 TARGETED CLOSURE = QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW

This packet creates no authority.
RPE-04 = CLOSED
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

## Lineage

Prior externally reviewed packet HEAD:
1ffa36b67fd24461283d541a194f1ca09f2eff0a

Review/adjudication HEAD:
d0cac5b6833e5e94f0235a07b27449ef41464d3a

Targeted preregistration HEAD:
cd2804ac3ec865e065e121cdd7dd92a09b304a8b

Targeted RED HEAD:
9cf0056eb938c631100ac7e4891b750d0bdb5984

Targeted patch HEAD:
b0e57da54c09a838107e33fed34e0afc0afab6de

Targeted qualification HEAD:
6c8ad0dbdbe42da4b3dbee629075a6db2a3ac73d

## Candidate identities

External review return = 50acb047475ba568a54b15ea8a4d3aaea170878c
Internal adjudication = bf9caa0792e6e47fd48f4186f7e3e71577375459
Targeted preregistration = 250f351c656d5a782a4c4e4edad42bfa52a3e498
Targeted schema = 8f2ccf1cbfa5196785a7cc8edb591f3f1fc381da
Targeted historical RED test = 14d63db2c986d19f217ec598404927764944a05d
Targeted RED report = 2125afe83dc58ffff6305d22dacf0b35b9bc8664
Final implementation = 145b3112fd9309cc34d95a62c091cb6a6bc3bb11
Targeted mutation test = 0a4dbebcb61b13badc8c15b14b41924e3d9c031d
Qualification JSON = da4a10581bd84b4bca2ebac3d9b71927ae293fb9
Qualification report = 5ab434ca60862fde130eea219cec8a90b137e2fb

## Packet fidelity identities — deliberately distinct

ORIGINAL HISTORICAL RED TEST BLOB
= eca438187aceb64b4d96d29bcda6c5896864b12e

ORIGINAL FINAL PRE-CLOSURE MAIN TEST BLOB
= d424f5becbb40d5b9a9276132a1ac684986b7d0d

TARGETED HISTORICAL RED TEST BLOB
= 14d63db2c986d19f217ec598404927764944a05d

The targeted RED test remained byte-identical after the implementation patch and became GREEN because the implementation changed.

## Observed evidence

Targeted RED:
9 tests / 2 failures / 7 passes.

Targeted GREEN:
9 / 9 PASS.

Targeted mutation discrimination:
5 / 5 PASS; 5 / 5 mutants killed.

Full targeted regression:
148 / 148 PASS.

Protected diffs:
P5-E contract = 0
P5-E synthetic model = 0
P5-D4 runtime = 0

## Closure claims to review

NB-1 supplied-domain confinement:
- only exact MAIN_WORKTREE_ROOT or exact BARE_REPOSITORY_ROOT is accepted;
- ordinary subdirectory of a parent repository => UNKNOWN;
- .git redirection file => UNKNOWN;
- main worktree requires exact show-toplevel, local .git directory, git-dir == common-dir and git-dir == supplied/.git;
- bare repository requires git-dir/common-dir == supplied root.

NB-2 discrimination:
- annotated tag previous => UNKNOWN;
- previous blob => UNKNOWN;
- merge-base exit other than 0/1 => UNKNOWN;
- corrupted intermediate ancestry => UNKNOWN;
- hostile global Git config does not influence classification;
- five targeted mutants are killed.

NB-3 carry to RPE-04:
- Git executable identity must be explicit/governed;
- minimum supported Git version must be preregistered and verified.

NB-4 carry to RPE-04:
- local repository config domain must be controlled;
- include.path/includeIf must not introduce ungoverned authority/provenance.

NB-5:
- historical RED and final test identities are separated explicitly.

## Required review

Return:
VERDICT = PASS | PASS_WITH_NON_BLOCKING_NOTES | FAIL

Then:
- BLOCKING_FINDINGS
- NON_BLOCKING_FINDINGS
- DOMAIN_CONFINEMENT_CHECK
- DISCRIMINATION_CHECK
- RPE04_CARRIED_PRECONDITIONS_CHECK
- NB5_PACKET_FIDELITY_CHECK
- MUTATION_CHECK
- REGRESSION_CHECK
- AUTHORITY_LEAKAGE_CHECK
- CLAIM_SCOPE_CHECK
- RPE03_ADOPTION_READINESS
- RECOMMENDED_NEXT_ACTION

Attempt falsification with parent-repository subdirectory, .git redirection, main root, bare root, annotated tag, non-commit previous object, unexpected merge-base exit, corrupted intermediate ancestry, hostile global config, and mutants removing each corresponding protection.

This review creates no authority.
RPE-04 = CLOSED.
REAL P5-E = CLOSED.

---

# NORMALIZED DELTA — PRIOR REVIEWED HEAD TO TARGETED QUALIFICATION
~~~~diff
diff --git a/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE03-EXTERNAL-REVIEW-TARGETED-CLOSURE-QUALIFICATION.md b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE03-EXTERNAL-REVIEW-TARGETED-CLOSURE-QUALIFICATION.md
new file mode 100644
index 0000000..5ab434c
--- /dev/null
+++ b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE03-EXTERNAL-REVIEW-TARGETED-CLOSURE-QUALIFICATION.md
@@ -0,0 +1,113 @@
+# RPE-03 — EXTERNAL REVIEW TARGETED CLOSURE V0.1 — QUALIFICATION
+
+Date: 2026-10-03
+
+## Result
+
+`RPE-03 TARGETED CLOSURE = QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW`
+
+The prior external verdict was `PASS_WITH_NON_BLOCKING_NOTES`. No human adoption is created here.
+
+## Closure identities
+
+External review:
+`50acb047475ba568a54b15ea8a4d3aaea170878c`
+
+Internal adjudication:
+`bf9caa0792e6e47fd48f4186f7e3e71577375459`
+
+Targeted preregistration:
+`250f351c656d5a782a4c4e4edad42bfa52a3e498`
+
+Schema:
+`8f2ccf1cbfa5196785a7cc8edb591f3f1fc381da`
+
+Targeted RED HEAD:
+`9cf0056eb938c631100ac7e4891b750d0bdb5984`
+
+Targeted RED test:
+`14d63db2c986d19f217ec598404927764944a05d`
+
+Targeted RED report:
+`2125afe83dc58ffff6305d22dacf0b35b9bc8664`
+
+Final candidate HEAD:
+`b0e57da54c09a838107e33fed34e0afc0afab6de`
+
+Final implementation:
+`145b3112fd9309cc34d95a62c091cb6a6bc3bb11`
+
+Targeted mutation tests:
+`0a4dbebcb61b13badc8c15b14b41924e3d9c031d`
+
+## NB-1 supplied-domain confinement
+
+The supplied path is now accepted only as:
+- exact main worktree root; or
+- exact bare repository root.
+
+Main-worktree acceptance requires:
+- git --show-toplevel equals the supplied resolved path;
+- .git is a local directory, not a redirection file;
+- git-dir equals common-dir;
+- git-dir equals supplied_path/.git.
+
+Bare acceptance requires git-dir/common-dir to equal the supplied resolved root.
+
+An ordinary subdirectory of a parent repository returns UNKNOWN.
+A directory using a .git redirection file returns UNKNOWN.
+
+## NB-2 discrimination
+
+New permanent cases cover:
+- annotated tag as previous object -> UNKNOWN;
+- previous blob -> UNKNOWN;
+- merge-base exit other than 0/1 -> UNKNOWN;
+- corrupted intermediate ancestry object -> UNKNOWN;
+- hostile global Git configuration -> no influence.
+
+Five targeted mutants are killed, covering:
+- parent-repository discovery;
+- .git redirection;
+- commit-type enforcement using an annotated tag;
+- merge-base unexpected-exit mapping;
+- global-config neutralization.
+
+## NB-3 / NB-4 carry
+
+RPE-04 must not consume RPE-03 until it qualifies:
+- explicit governed Git executable identity;
+- preregistered/verified minimum Git version;
+- a controlled repository configuration domain;
+- include.path/includeIf cannot create ungoverned authority or provenance.
+
+These are explicit preconditions, not claimed closed by RPE-03.
+
+## Evidence
+
+Targeted closure:
+`9 / 9 PASS`
+
+Targeted mutation discrimination:
+`5 / 5 PASS; 5 / 5 mutants killed`
+
+P5-E + RPE-01 + RPE-03 regression:
+`148 / 148 PASS`
+
+Protected diffs:
+- P5-E contract = 0;
+- P5-E synthetic model = 0;
+- P5-D4 runtime = 0.
+
+## Packet fidelity
+
+The rebuilt packet must distinguish:
+- original historical RED test blob `eca438187aceb64b4d96d29bcda6c5896864b12e`;
+- original final test blob `d424f5becbb40d5b9a9276132a1ac684986b7d0d`;
+- targeted historical RED test blob `14d63db2c986d19f217ec598404927764944a05d`.
+
+## Authority
+
+RPE-03 human adoption = pending.
+RPE-04/05/06 = closed.
+REAL P5-E = closed.
diff --git a/tests/obsidian_projection/test_rpe03_external_review_targeted_closure_v0_1.py b/tests/obsidian_projection/test_rpe03_external_review_targeted_closure_v0_1.py
new file mode 100644
index 0000000..14d63db
--- /dev/null
+++ b/tests/obsidian_projection/test_rpe03_external_review_targeted_closure_v0_1.py
@@ -0,0 +1,163 @@
+import importlib.util
+import os
+import stat
+import subprocess
+import tempfile
+import unittest
+from pathlib import Path
+from unittest import mock
+
+
+ROOT = Path(__file__).resolve().parents[2]
+MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py"
+
+
+def load():
+    spec=importlib.util.spec_from_file_location("rpe03_targeted",MODULE)
+    if spec is None or spec.loader is None:
+        raise AssertionError("cannot load RPE-03 module")
+    m=importlib.util.module_from_spec(spec)
+    spec.loader.exec_module(m)
+    return m
+
+
+def git(repo,*args,input_text=None):
+    cp=subprocess.run(["git",*args],cwd=str(repo),input=input_text,text=True,
+        stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
+    if cp.returncode != 0:
+        raise AssertionError(f"git {' '.join(args)} failed: {cp.stderr}")
+    return cp.stdout.strip()
+
+
+def make_linear_graph():
+    td=tempfile.TemporaryDirectory()
+    repo=Path(td.name)
+    git(repo,"init")
+    git(repo,"config","user.email","rpe03-targeted@example.invalid")
+    git(repo,"config","user.name","RPE03 Targeted")
+    (repo/"f.txt").write_text("A\n",encoding="utf-8")
+    git(repo,"add","f.txt"); git(repo,"commit","-m","A")
+    a=git(repo,"rev-parse","HEAD")
+    (repo/"f.txt").write_text("B\n",encoding="utf-8")
+    git(repo,"commit","-am","B")
+    b=git(repo,"rev-parse","HEAD")
+    return td,repo,a,b
+
+
+def make_three_commit_graph():
+    td,repo,a,b=make_linear_graph()
+    (repo/"f.txt").write_text("C\n",encoding="utf-8")
+    git(repo,"commit","-am","C")
+    c=git(repo,"rev-parse","HEAD")
+    return td,repo,a,b,c
+
+
+class TestRPE03ExternalReviewTargetedClosureV01(unittest.TestCase):
+    def test_supplied_subdirectory_of_parent_repository_is_unknown(self):
+        m=load()
+        td,repo,a,b=make_linear_graph()
+        try:
+            sub=repo/"plain"/"sub"
+            sub.mkdir(parents=True)
+            self.assertEqual(m.classify_transition(sub,a,b),"UNKNOWN")
+        finally:
+            td.cleanup()
+
+    def test_gitfile_redirecting_to_other_repository_is_unknown(self):
+        m=load()
+        td,repo,a,b=make_linear_graph()
+        redirect_td=tempfile.TemporaryDirectory()
+        redirect=Path(redirect_td.name)
+        try:
+            git_dir=git(repo,"rev-parse","--absolute-git-dir")
+            (redirect/".git").write_text(f"gitdir: {git_dir}\n",encoding="utf-8")
+            self.assertEqual(m.classify_transition(redirect,a,b),"UNKNOWN")
+        finally:
+            redirect_td.cleanup()
+            td.cleanup()
+
+    def test_main_worktree_root_remains_allowed(self):
+        m=load()
+        td,repo,a,b=make_linear_graph()
+        try:
+            self.assertEqual(m.classify_transition(repo,a,b),"FAST_FORWARD")
+        finally:
+            td.cleanup()
+
+    def test_bare_repository_root_is_allowed(self):
+        m=load()
+        td,repo,a,b=make_linear_graph()
+        bare_td=tempfile.TemporaryDirectory()
+        bare=Path(bare_td.name)/"repo.git"
+        try:
+            git(repo,"clone","--bare",str(repo),str(bare))
+            self.assertEqual(m.classify_transition(bare,a,b),"FAST_FORWARD")
+        finally:
+            bare_td.cleanup()
+            td.cleanup()
+
+    def test_annotated_tag_as_previous_is_unknown(self):
+        m=load()
+        td,repo,a,b=make_linear_graph()
+        try:
+            git(repo,"tag","-a","tag-a",a,"-m","tag A")
+            tag_sha=git(repo,"rev-parse","tag-a")
+            self.assertNotEqual(tag_sha,a)
+            self.assertEqual(m.classify_transition(repo,tag_sha,b),"UNKNOWN")
+        finally:
+            td.cleanup()
+
+    def test_previous_blob_is_unknown(self):
+        m=load()
+        td,repo,a,b=make_linear_graph()
+        try:
+            blob=git(repo,"hash-object","-w","--stdin",input_text="blob")
+            self.assertEqual(m.classify_transition(repo,blob,b),"UNKNOWN")
+        finally:
+            td.cleanup()
+
+    def test_merge_base_exit_other_than_zero_or_one_is_unknown(self):
+        m=load()
+        td,repo,a,b=make_linear_graph()
+        original=m._run_git
+        def wrapped(repo_path,*args):
+            if args[:2] == ("merge-base","--is-ancestor"):
+                return subprocess.CompletedProcess(["git"],128,"","forced error")
+            return original(repo_path,*args)
+        try:
+            with mock.patch.object(m,"_run_git",side_effect=wrapped):
+                self.assertEqual(m.classify_transition(repo,a,b),"UNKNOWN")
+        finally:
+            td.cleanup()
+
+    def test_corrupted_intermediate_ancestry_object_is_unknown(self):
+        m=load()
+        td,repo,a,b,c=make_three_commit_graph()
+        try:
+            gd=Path(git(repo,"rev-parse","--absolute-git-dir"))
+            obj=gd/"objects"/b[:2]/b[2:]
+            self.assertTrue(obj.exists())
+            os.chmod(obj,stat.S_IWRITE)
+            obj.write_bytes(b"corrupt-intermediate")
+            self.assertEqual(m.classify_transition(repo,a,c),"UNKNOWN")
+        finally:
+            td.cleanup()
+
+    def test_hostile_global_git_config_does_not_influence(self):
+        m=load()
+        td,repo,a,b=make_linear_graph()
+        home_td=tempfile.TemporaryDirectory()
+        home=Path(home_td.name)
+        bad=home/"bad.inc"
+        bad.write_text("[broken\n",encoding="utf-8")
+        (home/".gitconfig").write_text(f"[include]\n\tpath = {bad.as_posix()}\n",encoding="utf-8")
+        try:
+            with mock.patch.dict(os.environ,{"HOME":str(home),"USERPROFILE":str(home)},clear=False):
+                self.assertEqual(m.classify_transition(repo,a,b),"FAST_FORWARD")
+        finally:
+            home_td.cleanup()
+            td.cleanup()
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/tests/obsidian_projection/test_rpe03_external_review_targeted_mutation_v0_1.py b/tests/obsidian_projection/test_rpe03_external_review_targeted_mutation_v0_1.py
new file mode 100644
index 0000000..0a4dbeb
--- /dev/null
+++ b/tests/obsidian_projection/test_rpe03_external_review_targeted_mutation_v0_1.py
@@ -0,0 +1,152 @@
+import os
+import subprocess
+import tempfile
+import types
+import unittest
+from pathlib import Path
+from unittest import mock
+
+
+ROOT=Path(__file__).resolve().parents[2]
+MODULE=ROOT/"tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py"
+
+
+def load(name,replacements=()):
+    source=MODULE.read_text(encoding="utf-8")
+    for old,new in replacements:
+        if source.count(old) != 1:
+            raise AssertionError(f"mutation anchor count != 1: {old!r}")
+        source=source.replace(old,new,1)
+    m=types.ModuleType(name); m.__file__=str(MODULE)
+    exec(compile(source,str(MODULE),"exec"),m.__dict__)
+    return m
+
+
+def git(repo,*args,input_text=None):
+    cp=subprocess.run(["git",*args],cwd=str(repo),input=input_text,text=True,
+        stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
+    if cp.returncode != 0:
+        raise AssertionError(cp.stderr)
+    return cp.stdout.strip()
+
+
+def make_graph():
+    td=tempfile.TemporaryDirectory(); repo=Path(td.name)
+    git(repo,"init"); git(repo,"config","user.email","mut@example.invalid"); git(repo,"config","user.name","Mut")
+    (repo/"f").write_text("A\n",encoding="utf-8"); git(repo,"add","f"); git(repo,"commit","-m","A")
+    a=git(repo,"rev-parse","HEAD")
+    (repo/"f").write_text("B\n",encoding="utf-8"); git(repo,"commit","-am","B")
+    b=git(repo,"rev-parse","HEAD")
+    return td,repo,a,b
+
+
+class TestRPE03ExternalReviewTargetedMutationV01(unittest.TestCase):
+    def test_parent_discovery_confinement_mutant_is_killed(self):
+        base=load("base_parent")
+        old='''    else:
+        top_text = _stdout_ok(_run_git(repo, "rev-parse", "--show-toplevel"))
+        if not top_text:
+            return None
+        top = _canonical_path(top_text, repo)
+        if not _same_path(top, repo):
+            return None
+        if not dot_git.is_dir():
+            return None
+        if not _same_path(git_dir, dot_git.resolve(strict=False)):
+            return None
+'''
+        mut=load("mut_parent",((old,'''    else:
+        pass
+'''),))
+        td,repo,a,b=make_graph()
+        try:
+            sub=repo/"plain"/"sub"; sub.mkdir(parents=True)
+            self.assertEqual(base.classify_transition(sub,a,b),"UNKNOWN")
+            self.assertEqual(mut.classify_transition(sub,a,b),"FAST_FORWARD")
+        finally:
+            td.cleanup()
+
+    def test_gitfile_redirect_confinement_mutant_is_killed(self):
+        base=load("base_gitfile")
+        old='''    if dot_git.is_file():
+        return None
+'''
+        main='''        top_text = _stdout_ok(_run_git(repo, "rev-parse", "--show-toplevel"))
+        if not top_text:
+            return None
+        top = _canonical_path(top_text, repo)
+        if not _same_path(top, repo):
+            return None
+        if not dot_git.is_dir():
+            return None
+        if not _same_path(git_dir, dot_git.resolve(strict=False)):
+            return None
+'''
+        source=MODULE.read_text(encoding="utf-8")
+        if source.count(old)!=1 or source.count(main)!=1:
+            raise AssertionError("gitfile mutation anchors")
+        source=source.replace(old,"",1).replace(main,"        pass\n",1)
+        mut=types.ModuleType("mut_gitfile"); mut.__file__=str(MODULE)
+        exec(compile(source,str(MODULE),"exec"),mut.__dict__)
+        td,repo,a,b=make_graph(); redir_td=tempfile.TemporaryDirectory(); redir=Path(redir_td.name)
+        try:
+            gd=git(repo,"rev-parse","--absolute-git-dir")
+            (redir/".git").write_text(f"gitdir: {gd}\n",encoding="utf-8")
+            self.assertEqual(base.classify_transition(redir,a,b),"UNKNOWN")
+            self.assertEqual(mut.classify_transition(redir,a,b),"FAST_FORWARD")
+        finally:
+            redir_td.cleanup(); td.cleanup()
+
+    def test_commit_type_check_mutant_is_killed_by_annotated_tag(self):
+        base=load("base_type")
+        mut=load("mut_type",((
+            '    return cp is not None and cp.returncode == 0 and cp.stdout.strip() == "commit"\n',
+            '    return cp is not None and cp.returncode == 0\n',
+        ),))
+        td,repo,a,b=make_graph()
+        try:
+            git(repo,"tag","-a","tag-a",a,"-m","tag A")
+            tag=git(repo,"rev-parse","tag-a")
+            self.assertEqual(base.classify_transition(repo,tag,b),"UNKNOWN")
+            self.assertEqual(mut.classify_transition(repo,tag,b),"FAST_FORWARD")
+        finally:
+            td.cleanup()
+
+    def test_other_merge_base_exit_mapping_mutant_is_killed(self):
+        base=load("base_exit")
+        mut=load("mut_exit",((
+            '    if cp.returncode == 1:\n        return "NON_FAST_FORWARD"\n    return "UNKNOWN"\n',
+            '    if cp.returncode == 1:\n        return "NON_FAST_FORWARD"\n    return "NON_FAST_FORWARD"\n',
+        ),))
+        td,repo,a,b=make_graph()
+        def force(module):
+            original=module._run_git
+            def wrapped(repo_path,*args):
+                if args[:2] == ("merge-base","--is-ancestor"):
+                    return subprocess.CompletedProcess(["git"],128,"","forced")
+                return original(repo_path,*args)
+            return wrapped
+        try:
+            with mock.patch.object(base,"_run_git",side_effect=force(base)):
+                self.assertEqual(base.classify_transition(repo,a,b),"UNKNOWN")
+            with mock.patch.object(mut,"_run_git",side_effect=force(mut)):
+                self.assertEqual(mut.classify_transition(repo,a,b),"NON_FAST_FORWARD")
+        finally:
+            td.cleanup()
+
+    def test_global_config_neutralization_mutant_is_killed(self):
+        base=load("base_global")
+        mut=load("mut_global",(('            "GIT_CONFIG_GLOBAL": os.devnull,\n',''),))
+        td,repo,a,b=make_graph(); home_td=tempfile.TemporaryDirectory(); home=Path(home_td.name)
+        bad=home/"bad.inc"; bad.write_text("[broken\n",encoding="utf-8")
+        (home/".gitconfig").write_text(f"[include]\n\tpath = {bad.as_posix()}\n",encoding="utf-8")
+        try:
+            with mock.patch.dict(os.environ,{"HOME":str(home),"USERPROFILE":str(home)},clear=False):
+                self.assertEqual(base.classify_transition(repo,a,b),"FAST_FORWARD")
+                self.assertNotEqual(mut.classify_transition(repo,a,b),"FAST_FORWARD")
+        finally:
+            home_td.cleanup(); td.cleanup()
+
+
+if __name__=="__main__":
+    unittest.main()
diff --git a/tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py b/tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py
index 7c41bb6..145b311 100644
--- a/tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py
+++ b/tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py
@@ -71,26 +71,50 @@ def _canonical_path(text: str, base: Path) -> Path:
     return p.resolve(strict=False)


+def _same_path(left: Path, right: Path) -> bool:
+    return os.path.normcase(str(left)) == os.path.normcase(str(right))
+
+
 def _verified_domain(repo_path: Path) -> tuple[Path, Path] | None:
     try:
         repo = repo_path.resolve(strict=True)
     except (OSError, RuntimeError):
         return None
-    if not repo.exists():
+    if not repo.is_dir():
         return None

+    dot_git = repo / ".git"
+    if dot_git.is_file():
+        return None
+
+    bare_text = _stdout_ok(_run_git(repo, "rev-parse", "--is-bare-repository"))
     git_dir_text = _stdout_ok(_run_git(repo, "rev-parse", "--absolute-git-dir"))
     common_dir_text = _stdout_ok(
         _run_git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")
     )
-    if not git_dir_text or not common_dir_text:
+    if bare_text not in {"true", "false"} or not git_dir_text or not common_dir_text:
         return None

     git_dir = _canonical_path(git_dir_text, repo)
     common_dir = _canonical_path(common_dir_text, repo)
-    if os.path.normcase(str(git_dir)) != os.path.normcase(str(common_dir)):
+    if not _same_path(git_dir, common_dir):
         return None

+    if bare_text == "true":
+        if not _same_path(git_dir, repo):
+            return None
+    else:
+        top_text = _stdout_ok(_run_git(repo, "rev-parse", "--show-toplevel"))
+        if not top_text:
+            return None
+        top = _canonical_path(top_text, repo)
+        if not _same_path(top, repo):
+            return None
+        if not dot_git.is_dir():
+            return None
+        if not _same_path(git_dir, dot_git.resolve(strict=False)):
+            return None
+
     shallow = _stdout_ok(_run_git(repo, "rev-parse", "--is-shallow-repository"))
     if shallow is None or shallow.lower() != "false":
         return None
diff --git a/tools/obsidian_projection/rpe03_external_review_targeted_closure_preregistration_v0_1.json b/tools/obsidian_projection/rpe03_external_review_targeted_closure_preregistration_v0_1.json
new file mode 100644
index 0000000..250f351
--- /dev/null
+++ b/tools/obsidian_projection/rpe03_external_review_targeted_closure_preregistration_v0_1.json
@@ -0,0 +1,77 @@
+{
+  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE03_EXTERNAL_REVIEW_TARGETED_CLOSURE_PREREGISTRATION_V0_1",
+  "status": "PREREGISTERED_BEFORE_TARGETED_RED",
+  "base": {
+    "branch": "feat/obsidian-projection-rpe03-ancestry-classifier-v0.1",
+    "review_adjudication_head": "d0cac5b6833e5e94f0235a07b27449ef41464d3a",
+    "external_review_verdict": "PASS_WITH_NON_BLOCKING_NOTES",
+    "blocking_findings": "NONE",
+    "qualified_impl_blob": "7c41bb66a1438c2df9e2e77149a2c3cccb131abb",
+    "qualified_main_test_blob": "d424f5becbb40d5b9a9276132a1ac684986b7d0d",
+    "qualified_mutation_test_blob": "72d5f6d5ec38c7dc5785834e636943d7ec5ad181"
+  },
+  "authority": {
+    "targeted_closure_authorized": true,
+    "rpe04_authorized": false,
+    "rpe05_authorized": false,
+    "rpe06_authorized": false,
+    "real_p5e_authorized": false,
+    "network_authorized": false
+  },
+  "closure_scope": [
+    "NB-1",
+    "NB-2",
+    "NB-5"
+  ],
+  "supplied_domain_confinement": {
+    "allowed_domain_kinds": [
+      "MAIN_WORKTREE_ROOT",
+      "BARE_REPOSITORY_ROOT"
+    ],
+    "parent_repository_discovery_forbidden": true,
+    "gitfile_redirection_forbidden": true,
+    "main_worktree_requirements": [
+      "supplied path resolves exactly to git --show-toplevel",
+      ".git exists as local directory not file",
+      "git_dir equals common_dir",
+      "git_dir equals supplied_path/.git"
+    ],
+    "bare_requirements": [
+      "git --is-bare-repository equals true",
+      "git_dir equals common_dir",
+      "git_dir equals supplied resolved path"
+    ],
+    "supplied_subdirectory_result": "UNKNOWN",
+    "gitfile_redirection_result": "UNKNOWN",
+    "git_ceiling_directories": "OPTIONAL_DERIVED_DEFENSE_NOT_NORMATIVE_AUTHORITY"
+  },
+  "additional_discrimination": {
+    "annotated_tag_previous_result": "UNKNOWN",
+    "previous_noncommit_result": "UNKNOWN",
+    "merge_base_exit_other_than_0_or_1": "UNKNOWN",
+    "corrupt_intermediate_ancestry_object_result": "UNKNOWN",
+    "hostile_global_git_config_must_not_influence": true
+  },
+  "rpe04_carried_preconditions": {
+    "git_executable_identity": "EXPLICIT_AND_GOVERNED",
+    "minimum_supported_git_version": "PREREGISTERED_AND_VERIFIED",
+    "local_repository_config": "CONTROLLED_DOMAIN_REQUIRED",
+    "include_path_and_includeif": "MUST_NOT_INTRODUCE_UNGOVERNED_AUTHORITY_OR_PROVENANCE"
+  },
+  "packet_fidelity": {
+    "historical_red_test_blob": "eca438187aceb64b4d96d29bcda6c5896864b12e",
+    "final_preclosure_test_blob": "d424f5becbb40d5b9a9276132a1ac684986b7d0d",
+    "historical_red_must_be_sourced_from_historical_blob": true,
+    "final_test_must_be_labeled_separately": true
+  },
+  "mandatory_red_cases": [
+    "ordinary subdirectory of parent repository",
+    "gitfile redirecting to another repository",
+    "annotated tag as previous head",
+    "previous blob as previous head",
+    "merge-base exit 128",
+    "corrupted intermediate ancestry object",
+    "hostile global Git config"
+  ],
+  "stop": "TARGETED_DELTA_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
+}
diff --git a/tools/obsidian_projection/rpe03_external_review_targeted_closure_qualification_v0_1.json b/tools/obsidian_projection/rpe03_external_review_targeted_closure_qualification_v0_1.json
new file mode 100644
index 0000000..da4a105
--- /dev/null
+++ b/tools/obsidian_projection/rpe03_external_review_targeted_closure_qualification_v0_1.json
@@ -0,0 +1,87 @@
+{
+  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE03_EXTERNAL_REVIEW_TARGETED_CLOSURE_QUALIFICATION_V0_1",
+  "status": "QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW",
+  "date": "2026-10-03",
+  "branch": "feat/obsidian-projection-rpe03-ancestry-classifier-v0.1",
+  "external_review": {
+    "verdict": "PASS_WITH_NON_BLOCKING_NOTES",
+    "review_blob": "50acb047475ba568a54b15ea8a4d3aaea170878c",
+    "adjudication_blob": "bf9caa0792e6e47fd48f4186f7e3e71577375459"
+  },
+  "preregistration": {
+    "head": "cd2804ac3ec865e065e121cdd7dd92a09b304a8b",
+    "blob": "250f351c656d5a782a4c4e4edad42bfa52a3e498",
+    "schema_blob": "8f2ccf1cbfa5196785a7cc8edb591f3f1fc381da"
+  },
+  "targeted_red": {
+    "head": "9cf0056eb938c631100ac7e4891b750d0bdb5984",
+    "test_blob": "14d63db2c986d19f217ec598404927764944a05d",
+    "report_blob": "2125afe83dc58ffff6305d22dacf0b35b9bc8664",
+    "result": "9 tests; 2 failures; 7 passes"
+  },
+  "final_candidate": {
+    "head": "b0e57da54c09a838107e33fed34e0afc0afab6de",
+    "implementation_blob": "145b3112fd9309cc34d95a62c091cb6a6bc3bb11",
+    "targeted_test_blob": "14d63db2c986d19f217ec598404927764944a05d",
+    "targeted_mutation_blob": "0a4dbebcb61b13badc8c15b14b41924e3d9c031d"
+  },
+  "closures": {
+    "nb1": "CLOSED_CANDIDATE",
+    "nb2": "CLOSED_CANDIDATE",
+    "nb3": "CARRIED_TO_RPE04_PRECONDITION",
+    "nb4": "CARRIED_TO_RPE04_PRECONDITION",
+    "nb5": "PACKET_REBUILD_REQUIRED_AND_AUTHORIZED"
+  },
+  "domain_semantics": {
+    "allowed": [
+      "MAIN_WORKTREE_ROOT",
+      "BARE_REPOSITORY_ROOT"
+    ],
+    "ordinary_parent_subdirectory": "UNKNOWN",
+    "gitfile_redirection": "UNKNOWN",
+    "main_worktree_requires_exact_toplevel": true,
+    "main_worktree_requires_local_dot_git_directory": true,
+    "main_worktree_git_dir_equals_supplied_dot_git": true,
+    "bare_git_dir_equals_supplied_root": true,
+    "git_dir_equals_common_dir": true
+  },
+  "discrimination": {
+    "annotated_tag_previous": "UNKNOWN",
+    "previous_noncommit": "UNKNOWN",
+    "merge_base_other_exit": "UNKNOWN",
+    "corrupt_intermediate_ancestry": "UNKNOWN",
+    "hostile_global_git_config": "NO_INFLUENCE",
+    "targeted_mutants_killed": 5
+  },
+  "rpe04_preconditions": {
+    "git_executable_identity": "EXPLICIT_AND_GOVERNED",
+    "minimum_supported_git_version": "PREREGISTERED_AND_VERIFIED",
+    "local_repository_config": "CONTROLLED_DOMAIN_REQUIRED",
+    "include_path_includeif": "NO_UNGOVERNED_AUTHORITY_OR_PROVENANCE"
+  },
+  "tests": {
+    "targeted_green": "9/9 PASS",
+    "targeted_mutation": "5/5 PASS / 5 mutants killed",
+    "full_targeted_regression": "148/148 PASS"
+  },
+  "protected_diffs": {
+    "p5e_contract": 0,
+    "p5e_synthetic_model": 0,
+    "p5d4_runtime": 0
+  },
+  "packet_fidelity": {
+    "original_historical_red_test_blob": "eca438187aceb64b4d96d29bcda6c5896864b12e",
+    "original_final_test_blob": "d424f5becbb40d5b9a9276132a1ac684986b7d0d",
+    "targeted_historical_red_test_blob": "14d63db2c986d19f217ec598404927764944a05d",
+    "labels_must_remain_distinct": true
+  },
+  "claim_boundary": {
+    "rpe03_human_adopted": false,
+    "rpe04_opened": false,
+    "rpe05_opened": false,
+    "rpe06_opened": false,
+    "real_p5e_authorized": false
+  },
+  "next_gate": "SHORT_EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADJUDICATION",
+  "stop": true
+}
~~~~

# GIT-BLOB-SOURCED COPY: PRIOR EXTERNAL REVIEW RETURN
Path: reports/program/...RPE03-EXTERNAL-REVIEW-CLAUDE-RETURN.md
Authoritative Git blob: 50acb047475ba568a54b15ea8a4d3aaea170878c
~~~~
# RPE-03 — EXTERNAL REVIEW RETURN — CLAUDE

Date: 2026-10-03

## Verdict

`VERDICT = PASS_WITH_NON_BLOCKING_NOTES`

`BLOCKING_FINDINGS = NONE`

## Non-blocking findings selected for pre-adoption closure

### NB-1 — supplied-domain confinement

The current classifier verifies the repository discovered by Git, but the supplied path can be:
- an ordinary subdirectory of a parent repository;
- a directory whose `.git` file redirects to another repository.

Required closure before RPE-04 consumption:
- exact supplied root must be a verified main worktree root or exact bare repository root;
- parent discovery and `.git` redirection must not be accepted.

### NB-2 — missing discriminating tests

Required additional tests:
- annotated tag as previous object -> UNKNOWN;
- previous object non-commit -> UNKNOWN;
- merge-base exit other than 0/1 -> UNKNOWN;
- corrupted intermediate ancestry object -> UNKNOWN;
- hostile global Git config must not influence classification.

### NB-3 — Git executable identity

Carried as mandatory RPE-04 prerequisite:
- explicit/governed Git executable identity;
- preregistered and verified minimum supported Git version.

### NB-4 — local repository config

Carried as mandatory RPE-04 domain prerequisite. Local config/include/includeIf must not introduce ungoverned authority/provenance.

### NB-5 — packet fidelity

The previous packet labeled the final test as the RED test. The replacement packet must distinguish historical RED blob from final test blob.

## Adoption readiness

The reviewer considered RPE-03 adoptable with notes, but the human authorization explicitly chooses targeted closure of NB-1/NB-2/NB-5 before adoption.

This review creates no authority.

`RPE-04 = CLOSED`
`REAL_P5E = CLOSED`
~~~~

# GIT-BLOB-SOURCED COPY: TARGETED PREREGISTRATION
Path: tools/obsidian_projection/rpe03_external_review_targeted_closure_preregistration_v0_1.json
Authoritative Git blob: 250f351c656d5a782a4c4e4edad42bfa52a3e498
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE03_EXTERNAL_REVIEW_TARGETED_CLOSURE_PREREGISTRATION_V0_1",
  "status": "PREREGISTERED_BEFORE_TARGETED_RED",
  "base": {
    "branch": "feat/obsidian-projection-rpe03-ancestry-classifier-v0.1",
    "review_adjudication_head": "d0cac5b6833e5e94f0235a07b27449ef41464d3a",
    "external_review_verdict": "PASS_WITH_NON_BLOCKING_NOTES",
    "blocking_findings": "NONE",
    "qualified_impl_blob": "7c41bb66a1438c2df9e2e77149a2c3cccb131abb",
    "qualified_main_test_blob": "d424f5becbb40d5b9a9276132a1ac684986b7d0d",
    "qualified_mutation_test_blob": "72d5f6d5ec38c7dc5785834e636943d7ec5ad181"
  },
  "authority": {
    "targeted_closure_authorized": true,
    "rpe04_authorized": false,
    "rpe05_authorized": false,
    "rpe06_authorized": false,
    "real_p5e_authorized": false,
    "network_authorized": false
  },
  "closure_scope": [
    "NB-1",
    "NB-2",
    "NB-5"
  ],
  "supplied_domain_confinement": {
    "allowed_domain_kinds": [
      "MAIN_WORKTREE_ROOT",
      "BARE_REPOSITORY_ROOT"
    ],
    "parent_repository_discovery_forbidden": true,
    "gitfile_redirection_forbidden": true,
    "main_worktree_requirements": [
      "supplied path resolves exactly to git --show-toplevel",
      ".git exists as local directory not file",
      "git_dir equals common_dir",
      "git_dir equals supplied_path/.git"
    ],
    "bare_requirements": [
      "git --is-bare-repository equals true",
      "git_dir equals common_dir",
      "git_dir equals supplied resolved path"
    ],
    "supplied_subdirectory_result": "UNKNOWN",
    "gitfile_redirection_result": "UNKNOWN",
    "git_ceiling_directories": "OPTIONAL_DERIVED_DEFENSE_NOT_NORMATIVE_AUTHORITY"
  },
  "additional_discrimination": {
    "annotated_tag_previous_result": "UNKNOWN",
    "previous_noncommit_result": "UNKNOWN",
    "merge_base_exit_other_than_0_or_1": "UNKNOWN",
    "corrupt_intermediate_ancestry_object_result": "UNKNOWN",
    "hostile_global_git_config_must_not_influence": true
  },
  "rpe04_carried_preconditions": {
    "git_executable_identity": "EXPLICIT_AND_GOVERNED",
    "minimum_supported_git_version": "PREREGISTERED_AND_VERIFIED",
    "local_repository_config": "CONTROLLED_DOMAIN_REQUIRED",
    "include_path_and_includeif": "MUST_NOT_INTRODUCE_UNGOVERNED_AUTHORITY_OR_PROVENANCE"
  },
  "packet_fidelity": {
    "historical_red_test_blob": "eca438187aceb64b4d96d29bcda6c5896864b12e",
    "final_preclosure_test_blob": "d424f5becbb40d5b9a9276132a1ac684986b7d0d",
    "historical_red_must_be_sourced_from_historical_blob": true,
    "final_test_must_be_labeled_separately": true
  },
  "mandatory_red_cases": [
    "ordinary subdirectory of parent repository",
    "gitfile redirecting to another repository",
    "annotated tag as previous head",
    "previous blob as previous head",
    "merge-base exit 128",
    "corrupted intermediate ancestry object",
    "hostile global Git config"
  ],
  "stop": "TARGETED_DELTA_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
}
~~~~

# GIT-BLOB-SOURCED COPY: ORIGINAL HISTORICAL RED TEST
Path: historical tests/obsidian_projection/test_rpe03_ancestry_classifier_v0_1.py
Authoritative Git blob: eca438187aceb64b4d96d29bcda6c5896864b12e
~~~~
﻿import importlib.util
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
~~~~

# GIT-BLOB-SOURCED COPY: ORIGINAL FINAL PRE-CLOSURE MAIN TEST
Path: tests/obsidian_projection/test_rpe03_ancestry_classifier_v0_1.py
Authoritative Git blob: d424f5becbb40d5b9a9276132a1ac684986b7d0d
~~~~
import importlib.util
import inspect
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py"
PREREG = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1.json"
SCHEMA = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1_schema_v0_1.json"
AMENDMENT = ROOT / "tools/obsidian_projection/rpe03_no_lazy_fetch_amendment_v0_1.json"
AMENDMENT_SCHEMA = ROOT / "tools/obsidian_projection/rpe03_no_lazy_fetch_amendment_v0_1_schema_v0_1.json"
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

    def test_implementation_constants_match_governed_preregistration(self):
        g=load(GUARD,"rpe01_guard_for_rpe03_parity")
        d=g.validate_governed_json(PREREG.read_text(encoding="utf-8"),SCHEMA.read_text(encoding="utf-8"))
        a=g.validate_governed_json(AMENDMENT.read_text(encoding="utf-8"),AMENDMENT_SCHEMA.read_text(encoding="utf-8"))
        m=load(MODULE,"rpe03_governed_config_parity")
        self.assertEqual(
            m._TIMEOUT_SECONDS * 1000,
            d["git_execution"]["command_timeout_milliseconds"],
        )
        env=m._safe_git_env()
        self.assertEqual(env["GIT_NO_REPLACE_OBJECTS"],"1")
        self.assertEqual(env["GIT_CONFIG_NOSYSTEM"],"1")
        self.assertEqual(env["GIT_TERMINAL_PROMPT"],"0")
        self.assertEqual(env["GIT_OPTIONAL_LOCKS"],"0")
        self.assertEqual(
            env["GIT_NO_LAZY_FETCH"],
            a["added_requirement"]["required_value"],
        )

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
            os.chmod(obj, stat.S_IWRITE)
            obj.write_bytes(b"corrupt-object")
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
                self.assertEqual(env["GIT_NO_LAZY_FETCH"],"1")
                self.assertFalse(any(k.startswith("GIT_") and k not in {"GIT_NO_REPLACE_OBJECTS","GIT_CONFIG_NOSYSTEM","GIT_CONFIG_GLOBAL","GIT_TERMINAL_PROMPT","GIT_OPTIONAL_LOCKS","GIT_NO_LAZY_FETCH"} for k in env))
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
~~~~

# GIT-BLOB-SOURCED COPY: TARGETED HISTORICAL RED TEST
Path: tests/obsidian_projection/test_rpe03_external_review_targeted_closure_v0_1.py
Authoritative Git blob: 14d63db2c986d19f217ec598404927764944a05d
~~~~
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
~~~~

# GIT-BLOB-SOURCED COPY: FINAL IMPLEMENTATION
Path: tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py
Authoritative Git blob: 145b3112fd9309cc34d95a62c091cb6a6bc3bb11
~~~~
"""RPE-03 V0.1: fail-closed local Git ancestry classifier.

No network operations are permitted. The classifier rebuilds a sanitized Git
environment, verifies the local object domain, validates commit identities, and
only then maps merge-base ancestry to the governed transition vocabulary.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Final


_SHA40_RE: Final = re.compile(r"[0-9a-f]{40}\Z")
_TIMEOUT_SECONDS: Final = 5
_SAFE_GIT_ENV_KEYS: Final = {
    "GIT_NO_REPLACE_OBJECTS",
    "GIT_CONFIG_NOSYSTEM",
    "GIT_CONFIG_GLOBAL",
    "GIT_TERMINAL_PROMPT",
    "GIT_OPTIONAL_LOCKS",
    "GIT_NO_LAZY_FETCH",
}


def _safe_git_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(
        {
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_NO_LAZY_FETCH": "1",
        }
    )
    return env


def _run_git(repo_path: Path, *args: str) -> subprocess.CompletedProcess[str] | None:
    cmd = ["git", "-c", "core.commitGraph=false", *args]
    try:
        return subprocess.run(
            cmd,
            cwd=str(repo_path),
            env=_safe_git_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
    except (subprocess.TimeoutExpired, OSError, ValueError):
        return None


def _stdout_ok(cp: subprocess.CompletedProcess[str] | None) -> str | None:
    if cp is None or cp.returncode != 0:
        return None
    return cp.stdout.strip()


def _canonical_path(text: str, base: Path) -> Path:
    p = Path(text)
    if not p.is_absolute():
        p = base / p
    return p.resolve(strict=False)


def _same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(str(left)) == os.path.normcase(str(right))


def _verified_domain(repo_path: Path) -> tuple[Path, Path] | None:
    try:
        repo = repo_path.resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    if not repo.is_dir():
        return None

    dot_git = repo / ".git"
    if dot_git.is_file():
        return None

    bare_text = _stdout_ok(_run_git(repo, "rev-parse", "--is-bare-repository"))
    git_dir_text = _stdout_ok(_run_git(repo, "rev-parse", "--absolute-git-dir"))
    common_dir_text = _stdout_ok(
        _run_git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")
    )
    if bare_text not in {"true", "false"} or not git_dir_text or not common_dir_text:
        return None

    git_dir = _canonical_path(git_dir_text, repo)
    common_dir = _canonical_path(common_dir_text, repo)
    if not _same_path(git_dir, common_dir):
        return None

    if bare_text == "true":
        if not _same_path(git_dir, repo):
            return None
    else:
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

    shallow = _stdout_ok(_run_git(repo, "rev-parse", "--is-shallow-repository"))
    if shallow is None or shallow.lower() != "false":
        return None

    if (common_dir / "shallow").exists():
        return None
    if (common_dir / "info" / "grafts").exists():
        return None
    if (common_dir / "objects" / "info" / "alternates").exists():
        return None

    return repo, common_dir


def _valid_commit(repo: Path, sha: object) -> bool:
    if type(sha) is not str or _SHA40_RE.fullmatch(sha) is None:
        return False
    cp = _run_git(repo, "cat-file", "-t", sha)
    return cp is not None and cp.returncode == 0 and cp.stdout.strip() == "commit"


def classify_transition(
    repo_path,
    previous_observed_head,
    new_exact_observed_head,
):
    """Return INITIAL, SAME, FAST_FORWARD, NON_FAST_FORWARD, or UNKNOWN."""
    if type(new_exact_observed_head) is not str or _SHA40_RE.fullmatch(
        new_exact_observed_head
    ) is None:
        return "UNKNOWN"
    if previous_observed_head is not None and (
        type(previous_observed_head) is not str
        or _SHA40_RE.fullmatch(previous_observed_head) is None
    ):
        return "UNKNOWN"

    try:
        repo_candidate = Path(repo_path)
    except (TypeError, ValueError):
        return "UNKNOWN"

    domain = _verified_domain(repo_candidate)
    if domain is None:
        return "UNKNOWN"
    repo, _common_dir = domain

    if not _valid_commit(repo, new_exact_observed_head):
        return "UNKNOWN"

    if previous_observed_head is None:
        return "INITIAL"

    if not _valid_commit(repo, previous_observed_head):
        return "UNKNOWN"

    if previous_observed_head == new_exact_observed_head:
        return "SAME"

    cp = _run_git(
        repo,
        "merge-base",
        "--is-ancestor",
        previous_observed_head,
        new_exact_observed_head,
    )
    if cp is None:
        return "UNKNOWN"
    if cp.returncode == 0:
        return "FAST_FORWARD"
    if cp.returncode == 1:
        return "NON_FAST_FORWARD"
    return "UNKNOWN"
~~~~

# GIT-BLOB-SOURCED COPY: TARGETED MUTATION TEST
Path: tests/obsidian_projection/test_rpe03_external_review_targeted_mutation_v0_1.py
Authoritative Git blob: 0a4dbebcb61b13badc8c15b14b41924e3d9c031d
~~~~
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
~~~~

# GIT-BLOB-SOURCED COPY: TARGETED QUALIFICATION JSON
Path: tools/obsidian_projection/rpe03_external_review_targeted_closure_qualification_v0_1.json
Authoritative Git blob: da4a10581bd84b4bca2ebac3d9b71927ae293fb9
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE03_EXTERNAL_REVIEW_TARGETED_CLOSURE_QUALIFICATION_V0_1",
  "status": "QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW",
  "date": "2026-10-03",
  "branch": "feat/obsidian-projection-rpe03-ancestry-classifier-v0.1",
  "external_review": {
    "verdict": "PASS_WITH_NON_BLOCKING_NOTES",
    "review_blob": "50acb047475ba568a54b15ea8a4d3aaea170878c",
    "adjudication_blob": "bf9caa0792e6e47fd48f4186f7e3e71577375459"
  },
  "preregistration": {
    "head": "cd2804ac3ec865e065e121cdd7dd92a09b304a8b",
    "blob": "250f351c656d5a782a4c4e4edad42bfa52a3e498",
    "schema_blob": "8f2ccf1cbfa5196785a7cc8edb591f3f1fc381da"
  },
  "targeted_red": {
    "head": "9cf0056eb938c631100ac7e4891b750d0bdb5984",
    "test_blob": "14d63db2c986d19f217ec598404927764944a05d",
    "report_blob": "2125afe83dc58ffff6305d22dacf0b35b9bc8664",
    "result": "9 tests; 2 failures; 7 passes"
  },
  "final_candidate": {
    "head": "b0e57da54c09a838107e33fed34e0afc0afab6de",
    "implementation_blob": "145b3112fd9309cc34d95a62c091cb6a6bc3bb11",
    "targeted_test_blob": "14d63db2c986d19f217ec598404927764944a05d",
    "targeted_mutation_blob": "0a4dbebcb61b13badc8c15b14b41924e3d9c031d"
  },
  "closures": {
    "nb1": "CLOSED_CANDIDATE",
    "nb2": "CLOSED_CANDIDATE",
    "nb3": "CARRIED_TO_RPE04_PRECONDITION",
    "nb4": "CARRIED_TO_RPE04_PRECONDITION",
    "nb5": "PACKET_REBUILD_REQUIRED_AND_AUTHORIZED"
  },
  "domain_semantics": {
    "allowed": [
      "MAIN_WORKTREE_ROOT",
      "BARE_REPOSITORY_ROOT"
    ],
    "ordinary_parent_subdirectory": "UNKNOWN",
    "gitfile_redirection": "UNKNOWN",
    "main_worktree_requires_exact_toplevel": true,
    "main_worktree_requires_local_dot_git_directory": true,
    "main_worktree_git_dir_equals_supplied_dot_git": true,
    "bare_git_dir_equals_supplied_root": true,
    "git_dir_equals_common_dir": true
  },
  "discrimination": {
    "annotated_tag_previous": "UNKNOWN",
    "previous_noncommit": "UNKNOWN",
    "merge_base_other_exit": "UNKNOWN",
    "corrupt_intermediate_ancestry": "UNKNOWN",
    "hostile_global_git_config": "NO_INFLUENCE",
    "targeted_mutants_killed": 5
  },
  "rpe04_preconditions": {
    "git_executable_identity": "EXPLICIT_AND_GOVERNED",
    "minimum_supported_git_version": "PREREGISTERED_AND_VERIFIED",
    "local_repository_config": "CONTROLLED_DOMAIN_REQUIRED",
    "include_path_includeif": "NO_UNGOVERNED_AUTHORITY_OR_PROVENANCE"
  },
  "tests": {
    "targeted_green": "9/9 PASS",
    "targeted_mutation": "5/5 PASS / 5 mutants killed",
    "full_targeted_regression": "148/148 PASS"
  },
  "protected_diffs": {
    "p5e_contract": 0,
    "p5e_synthetic_model": 0,
    "p5d4_runtime": 0
  },
  "packet_fidelity": {
    "original_historical_red_test_blob": "eca438187aceb64b4d96d29bcda6c5896864b12e",
    "original_final_test_blob": "d424f5becbb40d5b9a9276132a1ac684986b7d0d",
    "targeted_historical_red_test_blob": "14d63db2c986d19f217ec598404927764944a05d",
    "labels_must_remain_distinct": true
  },
  "claim_boundary": {
    "rpe03_human_adopted": false,
    "rpe04_opened": false,
    "rpe05_opened": false,
    "rpe06_opened": false,
    "real_p5e_authorized": false
  },
  "next_gate": "SHORT_EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADJUDICATION",
  "stop": true
}
~~~~

# GIT-BLOB-SOURCED COPY: TARGETED QUALIFICATION REPORT
Path: reports/program/...RPE03-EXTERNAL-REVIEW-TARGETED-CLOSURE-QUALIFICATION.md
Authoritative Git blob: 5ab434ca60862fde130eea219cec8a90b137e2fb
~~~~
# RPE-03 — EXTERNAL REVIEW TARGETED CLOSURE V0.1 — QUALIFICATION

Date: 2026-10-03

## Result

`RPE-03 TARGETED CLOSURE = QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW`

The prior external verdict was `PASS_WITH_NON_BLOCKING_NOTES`. No human adoption is created here.

## Closure identities

External review:
`50acb047475ba568a54b15ea8a4d3aaea170878c`

Internal adjudication:
`bf9caa0792e6e47fd48f4186f7e3e71577375459`

Targeted preregistration:
`250f351c656d5a782a4c4e4edad42bfa52a3e498`

Schema:
`8f2ccf1cbfa5196785a7cc8edb591f3f1fc381da`

Targeted RED HEAD:
`9cf0056eb938c631100ac7e4891b750d0bdb5984`

Targeted RED test:
`14d63db2c986d19f217ec598404927764944a05d`

Targeted RED report:
`2125afe83dc58ffff6305d22dacf0b35b9bc8664`

Final candidate HEAD:
`b0e57da54c09a838107e33fed34e0afc0afab6de`

Final implementation:
`145b3112fd9309cc34d95a62c091cb6a6bc3bb11`

Targeted mutation tests:
`0a4dbebcb61b13badc8c15b14b41924e3d9c031d`

## NB-1 supplied-domain confinement

The supplied path is now accepted only as:
- exact main worktree root; or
- exact bare repository root.

Main-worktree acceptance requires:
- git --show-toplevel equals the supplied resolved path;
- .git is a local directory, not a redirection file;
- git-dir equals common-dir;
- git-dir equals supplied_path/.git.

Bare acceptance requires git-dir/common-dir to equal the supplied resolved root.

An ordinary subdirectory of a parent repository returns UNKNOWN.
A directory using a .git redirection file returns UNKNOWN.

## NB-2 discrimination

New permanent cases cover:
- annotated tag as previous object -> UNKNOWN;
- previous blob -> UNKNOWN;
- merge-base exit other than 0/1 -> UNKNOWN;
- corrupted intermediate ancestry object -> UNKNOWN;
- hostile global Git configuration -> no influence.

Five targeted mutants are killed, covering:
- parent-repository discovery;
- .git redirection;
- commit-type enforcement using an annotated tag;
- merge-base unexpected-exit mapping;
- global-config neutralization.

## NB-3 / NB-4 carry

RPE-04 must not consume RPE-03 until it qualifies:
- explicit governed Git executable identity;
- preregistered/verified minimum Git version;
- a controlled repository configuration domain;
- include.path/includeIf cannot create ungoverned authority or provenance.

These are explicit preconditions, not claimed closed by RPE-03.

## Evidence

Targeted closure:
`9 / 9 PASS`

Targeted mutation discrimination:
`5 / 5 PASS; 5 / 5 mutants killed`

P5-E + RPE-01 + RPE-03 regression:
`148 / 148 PASS`

Protected diffs:
- P5-E contract = 0;
- P5-E synthetic model = 0;
- P5-D4 runtime = 0.

## Packet fidelity

The rebuilt packet must distinguish:
- original historical RED test blob `eca438187aceb64b4d96d29bcda6c5896864b12e`;
- original final test blob `d424f5becbb40d5b9a9276132a1ac684986b7d0d`;
- targeted historical RED test blob `14d63db2c986d19f217ec598404927764944a05d`.

## Authority

RPE-03 human adoption = pending.
RPE-04/05/06 = closed.
REAL P5-E = closed.
~~~~
