# RPE-03 — NB5 ANCESTRY CLASSIFIER V0.1 — EXTERNAL REVIEW PACKET

Date: 2026-10-03

## Reviewer mandate

Independently review RPE-03 only.

Candidate status:
RPE-03 = QUALIFIED_FOR_EXTERNAL_REVIEW

This review creates no authority.

RPE-02 is a separate branch and is outside this packet.
RPE-04 = CLOSED
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

## Lineage

RPE-01 human-adoption base:
8ed3ec4079f3f996a5159b78fc40d0f32a917b25

RPE-01 adoption blob:
49203ebc2fb208c5dd23ded140295ac00c0afab6

RPE-03 preregistration HEAD:
8aa4ee2128a404fd57e64affc4f3b04751e86d87

RPE-03 RED HEAD:
55f00460dd1ae1004a2d450528937e7a870fc61d

No-lazy-fetch amendment HEAD:
b15e9ddeab00257f96cd622f3c80d45d96108e30

RPE-03 implementation HEAD:
c1ccde876b9ef9e542e97dd70f290b819e837ac2

RPE-03 qualification HEAD:
65f10b8d695925fb7c4838113095bfa8f49bcf31

## Candidate identities

Preregistration:
4eca84a17f7d0c53a794f34af65d1d0a81302930

Preregistration schema:
621f909fcde85694a0cc7548adffad7e14ae3970

RED test:
eca438187aceb64b4d96d29bcda6c5896864b12e

RED report:
bdc4055499b32c4e4aaa8abac788a95d3b63b3f4

No-lazy-fetch amendment:
acb57635ee2daf0a65aa57b7f2dab7d5d7d5dcec

No-lazy-fetch amendment schema:
b05984dc868655e0a05f1fab66769032fed2ab3c

Implementation:
7c41bb66a1438c2df9e2e77149a2c3cccb131abb

Final main test:
d424f5becbb40d5b9a9276132a1ac684986b7d0d

Mutation test:
72d5f6d5ec38c7dc5785834e636943d7ec5ad181

Qualification JSON:
58617c68b8200b994d4fa058224e749fd5396730

Qualification report:
721ef61dd3a65a2c2bfe676c87cf2b35a4730457

Protected parent identities:
RPE-01 guard = 26f977961d72a062199d71ffd628d5a5cc047887
P5-E contract = 43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9
P5-E synthetic model = c0f16baa151c1466e30ba5778f1fca8184cd4aac
P5-D4 runtime = 1825e53d195ba2a63b5b646a5b78eb77939b94b5

## Reproduced local evidence

Dedicated RPE-03 surface:
21 / 21 PASS

P5-E + RPE-01 + RPE-03 targeted regression:
134 / 134 PASS

Targeted mutants:
4 / 4 KILLED

Protected diffs from RPE-01 adoption base:
P5-E contract = 0
P5-E synthetic model = 0
P5-D4 runtime = 0

Qualification environment:
Git 2.54.0.windows.1
CPython 3.13.14
Windows-11-10.0.22631-SP0

## Required review questions

### Classification semantics
1. Are INITIAL, SAME, FAST_FORWARD, NON_FAST_FORWARD and UNKNOWN the only possible outputs?
2. Can the caller forge or supply a transition class?
3. Is INITIAL emitted only after the new head is a verified commit in a verified domain?
4. Is SAME checked explicitly after commit/domain verification and before ancestry testing?
5. Does merge-base exit 0 map only to FAST_FORWARD?
6. Does merge-base exit 1 map only to NON_FAST_FORWARD and only after both requested objects are verified commits?
7. Do all other merge-base exits map UNKNOWN?
8. Can missing or non-commit objects ever be mislabeled NON_FAST_FORWARD?

### Object-domain verification
9. Does the classifier reject linked worktree/common-dir mismatch?
10. Are shallow repositories rejected?
11. Does mere presence of info/grafts force UNKNOWN?
12. Does mere presence of objects/info/alternates force UNKNOWN?
13. Is inherited GIT_ALTERNATE_OBJECT_DIRECTORIES neutralized?
14. Can GIT_DIR or GIT_OBJECT_DIRECTORY redirect the classifier domain?
15. Is git_dir == common_dir sufficient for the intended first RPE-03 domain, or is an additional containment/bare-repository rule needed before RPE-04 consumes it?
16. Can any local repository metadata not currently checked alter ancestry/object resolution in a way that invalidates the five-way classification?

### Git execution isolation / no network
17. Are all inherited GIT_* variables stripped before explicit safe values are added?
18. Is GIT_NO_REPLACE_OBJECTS=1 sufficient to neutralize replace refs for these commands?
19. Is core.commitGraph=false applied to every Git subprocess?
20. Are system/global Git config neutralized as claimed?
21. Are prompts and optional locks disabled?
22. Is GIT_NO_LAZY_FETCH=1 correctly applied to every Git subprocess?
23. Could cat-file, rev-parse or merge-base still trigger any implicit remote access despite the current environment?
24. Is there any hidden network-capable command/API in the implementation?
25. Does the no-lazy-fetch amendment close the promisor-object lazy retrieval path without creating new authority?

### Fail-closed behavior
26. Does timeout return UNKNOWN?
27. Does requested-object corruption return UNKNOWN?
28. Are invalid SHA forms rejected as UNKNOWN before Git ancestry decisions?
29. Does local subprocess/config failure fail closed?
30. Is the Windows corruption-fixture correction evidence-only and semantically neutral?

### Mutation/provenance/regression
31. Do the four mutation checks genuinely discriminate:
    - exit-1 mapping;
    - inherited Git environment stripping;
    - replace-object neutralization;
    - no-lazy-fetch hardening?
32. Do implementation timeout/environment requirements match the governed preregistration and amendment?
33. Is any normative classifier authority silently sourced from environment, CLI or unlisted files?
34. Is the 134/134 targeted regression sufficient for this isolated component?
35. Is a full Obsidian suite unnecessary given zero protected-runtime diff and no activation?

### Authority
36. Did RPE-03 open any network, RPE-04/05/06, P5-D4 real-state, Vault/CURRENT or REAL P5-E authority?
37. Is RPE-03 ready for human adoption if no blocker is found?

## Required adversarial probes

At minimum attempt:
- null -> valid commit;
- same commit;
- ancestor -> descendant;
- rollback descendant -> ancestor;
- divergent siblings;
- missing previous and missing new;
- blob/tree/tag instead of commit where practical;
- malformed/lowercase/uppercase SHA variants;
- shallow marker;
- graft file;
- alternates file;
- inherited GIT_DIR;
- inherited GIT_OBJECT_DIRECTORY;
- inherited GIT_ALTERNATE_OBJECT_DIRECTORIES;
- inherited replace-related variables;
- actual replace refs with and without neutralization;
- absence of GIT_NO_LAZY_FETCH mutant;
- timeout;
- corrupt requested object;
- linked worktree;
- commit graph influence mutant;
- merge-base exit-1 mapping mutant;
- static search for network commands/APIs;
- partial/promisor repository behavior if feasible without violating the reviewer's own safety constraints.

## Required output

Return exactly one:

VERDICT = PASS | PASS_WITH_NON_BLOCKING_NOTES | FAIL

Then provide:
- BLOCKING_FINDINGS
- NON_BLOCKING_FINDINGS
- CLASSIFICATION_CHECK
- OBJECT_DOMAIN_CHECK
- GIT_ENVIRONMENT_ISOLATION_CHECK
- NO_NETWORK_CHECK
- FAIL_CLOSED_CHECK
- CONFIG_PROVENANCE_CHECK
- MUTATION_CHECK
- REGRESSION_CHECK
- AUTHORITY_LEAKAGE_CHECK
- CLAIM_SCOPE_CHECK
- RPE03_ADOPTION_READINESS
- RECOMMENDED_NEXT_ACTION

Distinguish OBSERVED from INFERENCE. Give minimal falsification cases for findings where possible.

This review creates no authority.
RPE-04 = CLOSED
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

---

# NORMALIZED DISPLAY OF EXACT GIT DIFF — RPE-01 ADOPTION TO RPE-03 QUALIFICATION
~~~~diff
diff --git a/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE03-ANCESTRY-CLASSIFIER-PREDRAFT.md b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE03-ANCESTRY-CLASSIFIER-PREDRAFT.md
new file mode 100644
index 0000000..db0dd5f
--- /dev/null
+++ b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE03-ANCESTRY-CLASSIFIER-PREDRAFT.md
@@ -0,0 +1,11 @@
+﻿# RPE-03 — NB5 ANCESTRY CLASSIFIER V0.1 — PRE-DRAFT
+
+Base: RPE-01 adoption commit 8ed3ec4079f3f996a5159b78fc40d0f32a917b25.
+
+RPE-03 defines a no-network local Git ancestry classifier whose only results are INITIAL, SAME, FAST_FORWARD, NON_FAST_FORWARD and UNKNOWN.
+
+The classifier must verify the local Git object domain before ancestry classification. It strips inherited Git authority, disables replace-object and commit-graph influence, rejects shallow/graft/alternate domains, verifies requested objects are commits, and maps timeout, corruption or unprovable state to UNKNOWN.
+
+merge-base --is-ancestor exit 1 may mean NON_FAST_FORWARD only after both commit identities and the local object domain are verified.
+
+No fetch, ls-remote, remote observation, RPE-04/05/06, P5-D4 real-state mutation, Vault/CURRENT mutation or REAL P5-E is authorized.
diff --git a/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE03-ANCESTRY-CLASSIFIER-QUALIFICATION.md b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE03-ANCESTRY-CLASSIFIER-QUALIFICATION.md
new file mode 100644
index 0000000..721ef61
--- /dev/null
+++ b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE03-ANCESTRY-CLASSIFIER-QUALIFICATION.md
@@ -0,0 +1,180 @@
+# RPE-03 — NB5 ANCESTRY CLASSIFIER V0.1 — QUALIFICATION
+
+Date: 2026-10-03
+
+## Verdict
+
+`RPE-03 = QUALIFIED_FOR_EXTERNAL_REVIEW`
+
+Human adoption is pending. RPE-04/RPE-05/RPE-06 and REAL P5-E remain closed.
+
+## Canonical base
+
+RPE-01 adoption commit:
+`8ed3ec4079f3f996a5159b78fc40d0f32a917b25`
+
+RPE-01 adoption blob:
+`49203ebc2fb208c5dd23ded140295ac00c0afab6`
+
+The adopted P5-E contract, synthetic model and P5-D4 runtime remain unchanged.
+
+## Preregistration and RED
+
+Preregistration HEAD:
+`8aa4ee2128a404fd57e64affc4f3b04751e86d87`
+
+Preregistration blob:
+`4eca84a17f7d0c53a794f34af65d1d0a81302930`
+
+Closed-schema blob:
+`621f909fcde85694a0cc7548adffad7e14ae3970`
+
+The preregistration validates through the adopted RPE-01 public entrypoint.
+
+RED HEAD:
+`55f00460dd1ae1004a2d450528937e7a870fc61d`
+
+Observed RED:
+`16 tests / 14 failures / 2 passes`.
+
+The fourteen failures reflected the absence of the preregistered classifier.
+
+A Windows-only fixture correction was later required for the corruption test: Git's loose object was non-writable, so the fixture now makes it writable and corrupts its bytes instead of deleting it. No classifier correction was required by that fixture issue.
+
+## No-lazy-fetch hardening amendment
+
+During adversarial qualification, the no-network contract was tightened against Git promisor-object lazy retrieval.
+
+Amendment HEAD:
+`b15e9ddeab00257f96cd622f3c80d45d96108e30`
+
+Amendment blob:
+`acb57635ee2daf0a65aa57b7f2dab7d5d7d5dcec`
+
+Amendment schema:
+`b05984dc868655e0a05f1fab66769032fed2ab3c`
+
+Every classifier Git subprocess receives:
+`GIT_NO_LAZY_FETCH=1`.
+
+## Final implementation
+
+Implementation HEAD:
+`c1ccde876b9ef9e542e97dd70f290b819e837ac2`
+
+Module:
+`7c41bb66a1438c2df9e2e77149a2c3cccb131abb`
+
+Main tests:
+`d424f5becbb40d5b9a9276132a1ac684986b7d0d`
+
+Mutation tests:
+`72d5f6d5ec38c7dc5785834e636943d7ec5ad181`
+
+## Qualified classifier semantics
+
+The only outputs are:
+
+```text
+INITIAL
+SAME
+FAST_FORWARD
+NON_FAST_FORWARD
+UNKNOWN
+```
+
+The caller cannot provide or override a transition class.
+
+Before classification, the component verifies the local Git domain and requested commit identities.
+
+Fail-closed cases map to `UNKNOWN`, including:
+- invalid SHA identity;
+- missing object;
+- non-commit object;
+- command failure;
+- timeout;
+- requested-object corruption;
+- linked worktree/common-dir mismatch;
+- shallow repository;
+- graft presence;
+- objects/info/alternates presence.
+
+`SAME` is explicit and precedes ancestry testing.
+
+`INITIAL` requires a verified new commit in a verified domain and no predecessor.
+
+Only after both commit identities and the object domain are verified does:
+
+`git merge-base --is-ancestor A B`
+
+map:
+- exit 0 → `FAST_FORWARD`;
+- exit 1 → `NON_FAST_FORWARD`;
+- other exit → `UNKNOWN`.
+
+## Git execution isolation
+
+Every Git subprocess:
+- uses only local command families `rev-parse`, `cat-file`, and `merge-base --is-ancestor`;
+- uses `-c core.commitGraph=false`;
+- strips all inherited `GIT_*` variables;
+- sets `GIT_NO_REPLACE_OBJECTS=1`;
+- sets `GIT_NO_LAZY_FETCH=1`;
+- disables system and global Git config;
+- disables terminal prompts;
+- disables optional locks.
+
+The source contains no network command/API family used by the classifier.
+
+## Governed configuration provenance
+
+The RPE-03 preregistration and its no-lazy-fetch amendment are both closed-schema artifacts validated through RPE-01.
+
+A dedicated parity test binds implementation timeout/environment requirements to those governed artifacts.
+
+No environment, CLI or unlisted file supplies normative classifier authority.
+
+## Mutation/discrimination
+
+Four targeted mutants were killed:
+
+1. merge-base exit 1 incorrectly mapped to FAST_FORWARD;
+2. inherited `GIT_*` stripping removed;
+3. replace-object neutralization removed;
+4. explicit no-lazy-fetch environment hardening removed.
+
+Result:
+`4 / 4 KILLED`.
+
+The replace-object mutation uses an unrelated replacement root so the mutant actually changes the ancestry outcome.
+
+## Test result
+
+Dedicated RPE-03 surface:
+`21 / 21 PASS`
+
+P5-E + RPE-01 + RPE-03 targeted regression:
+`134 / 134 PASS`
+
+Protected diffs:
+```text
+P5-E CONTRACT = 0
+P5-E SYNTHETIC MODEL = 0
+P5-D4 RUNTIME = 0
+```
+
+Qualification environment:
+`Git 2.54.0.windows.1 / CPython 3.13.14 / Windows-11-10.0.22631-SP0`.
+
+## Authority boundary
+
+This qualification does not authorize:
+- RPE-04/05/06;
+- fetch, remote observation or GitHub polling;
+- P5-D4 real-state mutation;
+- Vault/CURRENT mutation;
+- REAL P5-E;
+- human adoption of RPE-03.
+
+Maximum claim:
+`RPE03_ANCESTRY_CLASSIFIER = QUALIFIED_FOR_EXTERNAL_REVIEW`.
diff --git a/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE03-ANCESTRY-CLASSIFIER-RED.md b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE03-ANCESTRY-CLASSIFIER-RED.md
new file mode 100644
index 0000000..bdc4055
--- /dev/null
+++ b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE03-ANCESTRY-CLASSIFIER-RED.md
@@ -0,0 +1,43 @@
+﻿# RPE-03 — NB5 ANCESTRY CLASSIFIER V0.1 — RED EVIDENCE
+
+Date: 2026-10-03
+
+## Preregistered predecessor
+
+Preregistration HEAD:
+8aa4ee2128a404fd57e64affc4f3b04751e86d87
+
+Preregistration blob:
+4eca84a17f7d0c53a794f34af65d1d0a81302930
+
+Preregistration schema blob:
+621f909fcde85694a0cc7548adffad7e14ae3970
+
+## RED command
+
+python -B -m unittest tests.obsidian_projection.test_rpe03_ancestry_classifier_v0_1
+
+## Observed result
+
+Ran 16 tests.
+
+FAILED (failures=14).
+
+RPE03_RED_EXIT=1.
+
+Two tests passed:
+- governed preregistration validates through RPE-01;
+- the absent classifier source contains no forbidden network tokens by construction.
+
+The fourteen RED failures arise because
+tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py
+does not yet exist.
+
+The frozen test surface already covers INITIAL/SAME/FAST_FORWARD/NON_FAST_FORWARD, missing and non-commit objects, shallow/graft/alternate domains, inherited Git environment, replace refs, timeout, requested-object corruption, linked worktrees, commit-graph disabling, environment sanitization and invalid head identities.
+
+No network operation or protected predecessor mutation occurred.
+
+RPE-04 = CLOSED.
+RPE-05 = CLOSED.
+RPE-06 = CLOSED.
+REAL P5-E = CLOSED.
diff --git a/tests/obsidian_projection/test_rpe03_ancestry_classifier_mutation_v0_1.py b/tests/obsidian_projection/test_rpe03_ancestry_classifier_mutation_v0_1.py
new file mode 100644
index 0000000..72d5f6d
--- /dev/null
+++ b/tests/obsidian_projection/test_rpe03_ancestry_classifier_mutation_v0_1.py
@@ -0,0 +1,122 @@
+import os
+import subprocess
+import tempfile
+import types
+import unittest
+from pathlib import Path
+from unittest import mock
+
+
+ROOT = Path(__file__).resolve().parents[2]
+MODULE = ROOT / "tools" / "obsidian_projection" / "rpe03_ancestry_classifier_v0_1.py"
+
+
+def load_source_module(name, replacements=()):
+    source = MODULE.read_text(encoding="utf-8")
+    for old, new in replacements:
+        if source.count(old) != 1:
+            raise AssertionError(f"mutation anchor count != 1: {old!r}")
+        source = source.replace(old, new, 1)
+    module = types.ModuleType(name)
+    module.__file__ = str(MODULE)
+    exec(compile(source, str(MODULE), "exec"), module.__dict__)
+    return module
+
+
+def git(repo, *args):
+    cp = subprocess.run(
+        ["git", *args],
+        cwd=str(repo),
+        text=True,
+        stdout=subprocess.PIPE,
+        stderr=subprocess.PIPE,
+        check=False,
+    )
+    if cp.returncode != 0:
+        raise AssertionError(cp.stderr)
+    return cp.stdout.strip()
+
+
+def make_linear_graph():
+    td = tempfile.TemporaryDirectory()
+    repo = Path(td.name)
+    git(repo, "init")
+    git(repo, "config", "user.email", "rpe03-mut@example.invalid")
+    git(repo, "config", "user.name", "RPE03 Mut")
+    (repo / "f.txt").write_text("A\n", encoding="utf-8")
+    git(repo, "add", "f.txt")
+    git(repo, "commit", "-m", "A")
+    a = git(repo, "rev-parse", "HEAD")
+    (repo / "f.txt").write_text("B\n", encoding="utf-8")
+    git(repo, "commit", "-am", "B")
+    b = git(repo, "rev-parse", "HEAD")
+    return td, repo, a, b
+
+
+class TestRPE03MutationDiscriminationV01(unittest.TestCase):
+    def test_exit_one_mapping_mutant_is_killed(self):
+        base = load_source_module("rpe03_base_exit1")
+        mutant = load_source_module(
+            "rpe03_mut_exit1",
+            ((
+                '    if cp.returncode == 1:\n        return "NON_FAST_FORWARD"',
+                '    if cp.returncode == 1:\n        return "FAST_FORWARD"',
+            ),),
+        )
+        td, repo, a, b = make_linear_graph()
+        try:
+            self.assertEqual(base.classify_transition(repo, b, a), "NON_FAST_FORWARD")
+            self.assertEqual(mutant.classify_transition(repo, b, a), "FAST_FORWARD")
+        finally:
+            td.cleanup()
+
+    def test_inherited_git_environment_strip_mutant_is_killed(self):
+        base = load_source_module("rpe03_base_env")
+        mutant = load_source_module(
+            "rpe03_mut_env",
+            ((
+                'env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}',
+                'env = dict(os.environ)',
+            ),),
+        )
+        td, repo, a, b = make_linear_graph()
+        try:
+            hostile = {
+                "GIT_DIR": "X:/forbidden",
+                "GIT_OBJECT_DIRECTORY": "X:/forbidden-objects",
+                "GIT_ALTERNATE_OBJECT_DIRECTORIES": "X:/forbidden-alt",
+            }
+            with mock.patch.dict(os.environ, hostile, clear=False):
+                self.assertEqual(base.classify_transition(repo, a, b), "FAST_FORWARD")
+                self.assertNotEqual(mutant.classify_transition(repo, a, b), "FAST_FORWARD")
+        finally:
+            td.cleanup()
+
+    def test_replace_object_neutralization_mutant_is_killed(self):
+        base = load_source_module("rpe03_base_replace")
+        mutant = load_source_module(
+            "rpe03_mut_replace",
+            (('            "GIT_NO_REPLACE_OBJECTS": "1",\n', ""),),
+        )
+        td, repo, a, b = make_linear_graph()
+        try:
+            tree = git(repo, "rev-parse", f"{a}^{{tree}}")
+            root = git(repo, "commit-tree", tree, "-m", "unrelated replacement root")
+            git(repo, "replace", b, root)
+            self.assertEqual(base.classify_transition(repo, a, b), "FAST_FORWARD")
+            self.assertNotEqual(mutant.classify_transition(repo, a, b), "FAST_FORWARD")
+        finally:
+            td.cleanup()
+
+    def test_no_lazy_fetch_environment_mutant_is_killed(self):
+        base = load_source_module("rpe03_base_lazy")
+        mutant = load_source_module(
+            "rpe03_mut_lazy",
+            (('            "GIT_NO_LAZY_FETCH": "1",\n', ""),),
+        )
+        self.assertEqual(base._safe_git_env()["GIT_NO_LAZY_FETCH"], "1")
+        self.assertNotIn("GIT_NO_LAZY_FETCH", mutant._safe_git_env())
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/tests/obsidian_projection/test_rpe03_ancestry_classifier_v0_1.py b/tests/obsidian_projection/test_rpe03_ancestry_classifier_v0_1.py
new file mode 100644
index 0000000..d424f5b
--- /dev/null
+++ b/tests/obsidian_projection/test_rpe03_ancestry_classifier_v0_1.py
@@ -0,0 +1,234 @@
+import importlib.util
+import inspect
+import os
+import stat
+import subprocess
+import tempfile
+import unittest
+from pathlib import Path
+from unittest import mock
+
+ROOT = Path(__file__).resolve().parents[2]
+MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py"
+PREREG = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1.json"
+SCHEMA = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1_schema_v0_1.json"
+AMENDMENT = ROOT / "tools/obsidian_projection/rpe03_no_lazy_fetch_amendment_v0_1.json"
+AMENDMENT_SCHEMA = ROOT / "tools/obsidian_projection/rpe03_no_lazy_fetch_amendment_v0_1_schema_v0_1.json"
+GUARD = ROOT / "tools/obsidian_projection/rpe01_governed_closed_schema.py"
+MISSING = "f" * 40
+
+
+def load(path, name):
+    if not path.exists():
+        raise AssertionError(f"required module missing: {path}")
+    spec = importlib.util.spec_from_file_location(name, path)
+    if spec is None or spec.loader is None:
+        raise AssertionError(f"cannot load {path}")
+    m = importlib.util.module_from_spec(spec)
+    spec.loader.exec_module(m)
+    return m
+
+
+def git(repo, *args, input_text=None):
+    cp = subprocess.run(["git", *args], cwd=str(repo), input=input_text, text=True,
+                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
+    if cp.returncode != 0:
+        raise AssertionError(f"git {' '.join(args)} failed: {cp.stderr}")
+    return cp.stdout.strip()
+
+
+def make_graph():
+    td = tempfile.TemporaryDirectory()
+    repo = Path(td.name)
+    git(repo, "init")
+    git(repo, "config", "user.email", "rpe03@example.invalid")
+    git(repo, "config", "user.name", "RPE03")
+    (repo/"f.txt").write_text("A\n", encoding="utf-8")
+    git(repo, "add", "f.txt"); git(repo, "commit", "-m", "A")
+    a = git(repo, "rev-parse", "HEAD")
+    (repo/"f.txt").write_text("B\n", encoding="utf-8")
+    git(repo, "commit", "-am", "B")
+    b = git(repo, "rev-parse", "HEAD")
+    git(repo, "checkout", "-b", "side", a)
+    (repo/"g.txt").write_text("C\n", encoding="utf-8")
+    git(repo, "add", "g.txt"); git(repo, "commit", "-m", "C")
+    c = git(repo, "rev-parse", "HEAD")
+    git(repo, "checkout", "-")
+    return td, repo, a, b, c
+
+
+class TestRPE03AncestryClassifierV01(unittest.TestCase):
+    def test_preregistration_is_rpe01_guarded(self):
+        g=load(GUARD,"rpe01_guard_for_rpe03")
+        d=g.validate_governed_json(PREREG.read_text(encoding="utf-8"),SCHEMA.read_text(encoding="utf-8"))
+        self.assertEqual(d["classification"]["outputs"],["INITIAL","SAME","FAST_FORWARD","NON_FAST_FORWARD","UNKNOWN"])
+
+    def test_implementation_constants_match_governed_preregistration(self):
+        g=load(GUARD,"rpe01_guard_for_rpe03_parity")
+        d=g.validate_governed_json(PREREG.read_text(encoding="utf-8"),SCHEMA.read_text(encoding="utf-8"))
+        a=g.validate_governed_json(AMENDMENT.read_text(encoding="utf-8"),AMENDMENT_SCHEMA.read_text(encoding="utf-8"))
+        m=load(MODULE,"rpe03_governed_config_parity")
+        self.assertEqual(
+            m._TIMEOUT_SECONDS * 1000,
+            d["git_execution"]["command_timeout_milliseconds"],
+        )
+        env=m._safe_git_env()
+        self.assertEqual(env["GIT_NO_REPLACE_OBJECTS"],"1")
+        self.assertEqual(env["GIT_CONFIG_NOSYSTEM"],"1")
+        self.assertEqual(env["GIT_TERMINAL_PROMPT"],"0")
+        self.assertEqual(env["GIT_OPTIONAL_LOCKS"],"0")
+        self.assertEqual(
+            env["GIT_NO_LAZY_FETCH"],
+            a["added_requirement"]["required_value"],
+        )
+
+    def test_static_source_has_no_network_commands_or_network_modules(self):
+        source=MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""
+        for forbidden in ("fetch","ls-remote","urllib","socket","requests","http.client"):
+            self.assertNotIn(forbidden,source)
+
+    def test_caller_cannot_supply_transition_class(self):
+        m=load(MODULE,"rpe03_sig")
+        params=set(inspect.signature(m.classify_transition).parameters)
+        self.assertEqual(params,{"repo_path","previous_observed_head","new_exact_observed_head"})
+
+    def test_initial_same_fast_forward_rollback_and_divergent(self):
+        m=load(MODULE,"rpe03_graph")
+        td,repo,a,b,c=make_graph()
+        try:
+            self.assertEqual(m.classify_transition(repo,None,a),"INITIAL")
+            self.assertEqual(m.classify_transition(repo,a,a),"SAME")
+            self.assertEqual(m.classify_transition(repo,a,b),"FAST_FORWARD")
+            self.assertEqual(m.classify_transition(repo,b,a),"NON_FAST_FORWARD")
+            self.assertEqual(m.classify_transition(repo,b,c),"NON_FAST_FORWARD")
+        finally: td.cleanup()
+
+    def test_missing_previous_and_new_are_unknown(self):
+        m=load(MODULE,"rpe03_missing")
+        td,repo,a,b,c=make_graph()
+        try:
+            self.assertEqual(m.classify_transition(repo,MISSING,b),"UNKNOWN")
+            self.assertEqual(m.classify_transition(repo,a,MISSING),"UNKNOWN")
+        finally: td.cleanup()
+
+    def test_non_commit_object_is_unknown(self):
+        m=load(MODULE,"rpe03_blob")
+        td,repo,a,b,c=make_graph()
+        try:
+            blob=git(repo,"hash-object","-w","--stdin",input_text="blob")
+            self.assertEqual(m.classify_transition(repo,a,blob),"UNKNOWN")
+        finally: td.cleanup()
+
+    def test_shallow_domain_is_unknown(self):
+        m=load(MODULE,"rpe03_shallow")
+        td,repo,a,b,c=make_graph()
+        try:
+            gd=Path(git(repo,"rev-parse","--absolute-git-dir"))
+            (gd/"shallow").write_text(b+"\n",encoding="ascii")
+            self.assertEqual(m.classify_transition(repo,a,b),"UNKNOWN")
+        finally: td.cleanup()
+
+    def test_graft_domain_is_unknown(self):
+        m=load(MODULE,"rpe03_graft")
+        td,repo,a,b,c=make_graph()
+        try:
+            gd=Path(git(repo,"rev-parse","--absolute-git-dir"))
+            (gd/"info").mkdir(exist_ok=True)
+            (gd/"info"/"grafts").write_text(b+" "+a+"\n",encoding="ascii")
+            self.assertEqual(m.classify_transition(repo,a,b),"UNKNOWN")
+        finally: td.cleanup()
+
+    def test_alternates_domain_is_unknown(self):
+        m=load(MODULE,"rpe03_alt")
+        td,repo,a,b,c=make_graph()
+        other=tempfile.TemporaryDirectory()
+        try:
+            gd=Path(git(repo,"rev-parse","--absolute-git-dir"))
+            p=gd/"objects"/"info"/"alternates"; p.parent.mkdir(parents=True,exist_ok=True)
+            p.write_text(other.name+"\n",encoding="utf-8")
+            self.assertEqual(m.classify_transition(repo,a,b),"UNKNOWN")
+        finally:
+            other.cleanup(); td.cleanup()
+
+    def test_inherited_git_environment_is_neutralized(self):
+        m=load(MODULE,"rpe03_env")
+        td,repo,a,b,c=make_graph()
+        try:
+            with mock.patch.dict(os.environ,{
+                "GIT_DIR":"X:/forbidden",
+                "GIT_OBJECT_DIRECTORY":"X:/forbidden-objects",
+                "GIT_ALTERNATE_OBJECT_DIRECTORIES":"X:/forbidden-alt",
+                "GIT_REPLACE_REF_BASE":"refs/evil/",
+            },clear=False):
+                self.assertEqual(m.classify_transition(repo,a,b),"FAST_FORWARD")
+        finally: td.cleanup()
+
+    def test_replace_ref_cannot_alter_ancestry(self):
+        m=load(MODULE,"rpe03_replace")
+        td,repo,a,b,c=make_graph()
+        try:
+            git(repo,"replace",a,c)
+            self.assertEqual(m.classify_transition(repo,a,b),"FAST_FORWARD")
+        finally: td.cleanup()
+
+    def test_timeout_is_unknown(self):
+        m=load(MODULE,"rpe03_timeout")
+        with mock.patch.object(m.subprocess,"run",side_effect=subprocess.TimeoutExpired(["git"],5)):
+            self.assertEqual(m.classify_transition(Path("."),None,"a"*40),"UNKNOWN")
+
+    def test_corrupt_requested_object_is_unknown(self):
+        m=load(MODULE,"rpe03_corrupt")
+        td,repo,a,b,c=make_graph()
+        try:
+            gd=Path(git(repo,"rev-parse","--absolute-git-dir"))
+            obj=gd/"objects"/b[:2]/b[2:]
+            self.assertTrue(obj.exists())
+            os.chmod(obj, stat.S_IWRITE)
+            obj.write_bytes(b"corrupt-object")
+            self.assertEqual(m.classify_transition(repo,a,b),"UNKNOWN")
+        finally: td.cleanup()
+
+    def test_linked_worktree_domain_is_unknown(self):
+        m=load(MODULE,"rpe03_worktree")
+        td,repo,a,b,c=make_graph(); wtd=tempfile.TemporaryDirectory(); wt=Path(wtd.name)/"linked"
+        try:
+            git(repo,"worktree","add","-b","linked-test",str(wt),a)
+            self.assertEqual(m.classify_transition(wt,None,a),"UNKNOWN")
+        finally:
+            subprocess.run(["git","worktree","remove","--force",str(wt)],cwd=str(repo),capture_output=True,text=True)
+            wtd.cleanup(); td.cleanup()
+
+    def test_commands_disable_commit_graph_and_environment_is_sanitized(self):
+        m=load(MODULE,"rpe03_cmd")
+        td,repo,a,b,c=make_graph()
+        calls=[]; original=m.subprocess.run
+        def wrapped(*args,**kwargs):
+            calls.append((args,kwargs))
+            return original(*args,**kwargs)
+        try:
+            with mock.patch.object(m.subprocess,"run",side_effect=wrapped):
+                self.assertEqual(m.classify_transition(repo,a,b),"FAST_FORWARD")
+            self.assertTrue(calls)
+            for args,kwargs in calls:
+                cmd=list(args[0])
+                self.assertIn("core.commitGraph=false",cmd)
+                env=kwargs["env"]
+                self.assertEqual(env["GIT_NO_REPLACE_OBJECTS"],"1")
+                self.assertEqual(env["GIT_CONFIG_NOSYSTEM"],"1")
+                self.assertEqual(env["GIT_TERMINAL_PROMPT"],"0")
+                self.assertEqual(env["GIT_NO_LAZY_FETCH"],"1")
+                self.assertFalse(any(k.startswith("GIT_") and k not in {"GIT_NO_REPLACE_OBJECTS","GIT_CONFIG_NOSYSTEM","GIT_CONFIG_GLOBAL","GIT_TERMINAL_PROMPT","GIT_OPTIONAL_LOCKS","GIT_NO_LAZY_FETCH"} for k in env))
+        finally: td.cleanup()
+
+    def test_invalid_head_format_is_unknown(self):
+        m=load(MODULE,"rpe03_invalid")
+        td,repo,a,b,c=make_graph()
+        try:
+            for bad in ("HEAD","A"*40,"123",None,True):
+                with self.subTest(bad=bad):
+                    self.assertEqual(m.classify_transition(repo,a,bad),"UNKNOWN")
+        finally: td.cleanup()
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1.json b/tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1.json
new file mode 100644
index 0000000..4eca84a
--- /dev/null
+++ b/tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1.json
@@ -0,0 +1,120 @@
+{
+  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE03_ANCESTRY_CLASSIFIER_PREREGISTRATION_V0_1",
+  "status": "PREREGISTERED_BEFORE_RED",
+  "base": {
+    "rpe01_adoption_commit": "8ed3ec4079f3f996a5159b78fc40d0f32a917b25",
+    "rpe01_adoption_blob": "49203ebc2fb208c5dd23ded140295ac00c0afab6",
+    "rpe01_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887",
+    "p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9"
+  },
+  "authority": {
+    "stage": "RPE-03",
+    "rpe03_implementation_authorized": true,
+    "rpe04_authorized": false,
+    "rpe05_authorized": false,
+    "rpe06_authorized": false,
+    "network_inside_classifier_authorized": false,
+    "real_p5e_authorized": false,
+    "real_p5d4_state_mutation_authorized": false,
+    "vault_or_current_mutation_authorized": false
+  },
+  "governed_config": {
+    "authorized_entrypoint": "validate_governed_json(raw_document, raw_schema)",
+    "private_guard_functions_forbidden": true,
+    "validate_schema_definition_not_document_entrypoint": true,
+    "runtime_preregistration_path": "tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1.json",
+    "runtime_schema_path": "tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1_schema_v0_1.json",
+    "environment_config_authority_forbidden": true,
+    "cli_config_authority_forbidden": true,
+    "unlisted_file_config_authority_forbidden": true
+  },
+  "classification": {
+    "outputs": [
+      "INITIAL",
+      "SAME",
+      "FAST_FORWARD",
+      "NON_FAST_FORWARD",
+      "UNKNOWN"
+    ],
+    "previous_null": "INITIAL_AFTER_NEW_COMMIT_AND_DOMAIN_VERIFIED",
+    "same_exact_head": "SAME_AFTER_COMMIT_AND_DOMAIN_VERIFIED",
+    "merge_base_exit_0": "FAST_FORWARD",
+    "merge_base_exit_1": "NON_FAST_FORWARD",
+    "merge_base_other_exit": "UNKNOWN",
+    "invalid_or_unprovable_domain": "UNKNOWN",
+    "invalid_head_format": "UNKNOWN"
+  },
+  "git_execution": {
+    "git_executable_token": "git",
+    "command_timeout_milliseconds": 5000,
+    "network_commands_forbidden": true,
+    "allowed_git_command_families": [
+      "rev-parse",
+      "cat-file",
+      "merge-base --is-ancestor"
+    ],
+    "commit_graph_disabled": true,
+    "replace_objects_disabled": true,
+    "system_git_config_disabled": true,
+    "global_git_config_disabled": true,
+    "terminal_prompt_disabled": true,
+    "optional_locks_disabled": true
+  },
+  "environment_isolation": {
+    "strip_all_inherited_git_prefixed_variables": true,
+    "explicit_git_environment": [
+      "GIT_NO_REPLACE_OBJECTS=1",
+      "GIT_CONFIG_NOSYSTEM=1",
+      "GIT_CONFIG_GLOBAL=os.devnull",
+      "GIT_TERMINAL_PROMPT=0",
+      "GIT_OPTIONAL_LOCKS=0"
+    ],
+    "non_git_process_plumbing_may_be_preserved": true,
+    "git_prefixed_environment_may_not_supply_normative_authority": true
+  },
+  "verified_domain": {
+    "repository_must_resolve": true,
+    "git_dir_must_equal_common_dir": true,
+    "linked_worktree_common_dir_mismatch_result": "UNKNOWN",
+    "shallow_repository_result": "UNKNOWN",
+    "info_grafts_presence_result": "UNKNOWN",
+    "objects_info_alternates_presence_result": "UNKNOWN",
+    "new_object_must_exist_and_be_commit": true,
+    "previous_object_when_present_must_exist_and_be_commit": true,
+    "missing_object_result": "UNKNOWN",
+    "non_commit_result": "UNKNOWN",
+    "timeout_result": "UNKNOWN",
+    "corruption_or_command_error_result": "UNKNOWN"
+  },
+  "local_fixture_cases": [
+    "null to A -> INITIAL",
+    "A to A -> SAME",
+    "A to B -> FAST_FORWARD",
+    "B to A rollback -> NON_FAST_FORWARD",
+    "B to C divergent siblings -> NON_FAST_FORWARD",
+    "missing previous -> UNKNOWN",
+    "missing new -> UNKNOWN",
+    "blob object -> UNKNOWN",
+    "replace ref present but neutralized",
+    "shallow marker -> UNKNOWN",
+    "graft presence -> UNKNOWN",
+    "alternates file presence -> UNKNOWN",
+    "inherited GIT_DIR/GIT_OBJECT_DIRECTORY/GIT_ALTERNATE_OBJECT_DIRECTORIES neutralized",
+    "timeout -> UNKNOWN",
+    "corrupt requested object -> UNKNOWN",
+    "commit graph command influence disabled",
+    "network command absence static check"
+  ],
+  "mandatory_breakers": [
+    "caller cannot forge transition class",
+    "merge-base exit 1 only maps NON_FAST_FORWARD after both commits and domain verified",
+    "missing object never maps NON_FAST_FORWARD",
+    "non-commit never maps NON_FAST_FORWARD",
+    "shallow/graft/alternate domain never maps FAST_FORWARD or NON_FAST_FORWARD",
+    "inherited GIT environment cannot redirect object domain",
+    "replace refs cannot alter ancestry",
+    "timeout/corruption fail closed to UNKNOWN",
+    "no fetch/ls-remote/network API inside classifier"
+  ],
+  "stop": "EXTERNAL_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
+}
diff --git a/tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1_schema_v0_1.json b/tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1_schema_v0_1.json
new file mode 100644
index 0000000..621f909
--- /dev/null
+++ b/tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1_schema_v0_1.json
@@ -0,0 +1,407 @@
+{
+  "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
+  "artifact_role": "RPE03_ANCESTRY_CLASSIFIER_PREREGISTRATION",
+  "root": {
+    "kind": "object",
+    "fields": {
+      "schema": {
+        "kind": "string",
+        "const": "ATDS_OBSIDIAN_REAL_P5E_RPE03_ANCESTRY_CLASSIFIER_PREREGISTRATION_V0_1"
+      },
+      "status": {
+        "kind": "string",
+        "const": "PREREGISTERED_BEFORE_RED"
+      },
+      "base": {
+        "kind": "object",
+        "fields": {
+          "rpe01_adoption_commit": {
+            "kind": "string",
+            "const": "8ed3ec4079f3f996a5159b78fc40d0f32a917b25"
+          },
+          "rpe01_adoption_blob": {
+            "kind": "string",
+            "const": "49203ebc2fb208c5dd23ded140295ac00c0afab6"
+          },
+          "rpe01_guard_blob": {
+            "kind": "string",
+            "const": "26f977961d72a062199d71ffd628d5a5cc047887"
+          },
+          "p5e_contract_blob": {
+            "kind": "string",
+            "const": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9"
+          }
+        }
+      },
+      "authority": {
+        "kind": "object",
+        "fields": {
+          "stage": {
+            "kind": "string",
+            "const": "RPE-03"
+          },
+          "rpe03_implementation_authorized": {
+            "kind": "boolean",
+            "const": true
+          },
+          "rpe04_authorized": {
+            "kind": "boolean",
+            "const": false
+          },
+          "rpe05_authorized": {
+            "kind": "boolean",
+            "const": false
+          },
+          "rpe06_authorized": {
+            "kind": "boolean",
+            "const": false
+          },
+          "network_inside_classifier_authorized": {
+            "kind": "boolean",
+            "const": false
+          },
+          "real_p5e_authorized": {
+            "kind": "boolean",
+            "const": false
+          },
+          "real_p5d4_state_mutation_authorized": {
+            "kind": "boolean",
+            "const": false
+          },
+          "vault_or_current_mutation_authorized": {
+            "kind": "boolean",
+            "const": false
+          }
+        }
+      },
+      "governed_config": {
+        "kind": "object",
+        "fields": {
+          "authorized_entrypoint": {
+            "kind": "string",
+            "const": "validate_governed_json(raw_document, raw_schema)"
+          },
+          "private_guard_functions_forbidden": {
+            "kind": "boolean",
+            "const": true
+          },
+          "validate_schema_definition_not_document_entrypoint": {
+            "kind": "boolean",
+            "const": true
+          },
+          "runtime_preregistration_path": {
+            "kind": "string",
+            "const": "tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1.json"
+          },
+          "runtime_schema_path": {
+            "kind": "string",
+            "const": "tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1_schema_v0_1.json"
+          },
+          "environment_config_authority_forbidden": {
+            "kind": "boolean",
+            "const": true
+          },
+          "cli_config_authority_forbidden": {
+            "kind": "boolean",
+            "const": true
+          },
+          "unlisted_file_config_authority_forbidden": {
+            "kind": "boolean",
+            "const": true
+          }
+        }
+      },
+      "classification": {
+        "kind": "object",
+        "fields": {
+          "outputs": {
+            "kind": "array",
+            "items": {
+              "kind": "string"
+            },
+            "min_items": 5,
+            "max_items": 5,
+            "unique": true,
+            "ordered_const": [
+              "INITIAL",
+              "SAME",
+              "FAST_FORWARD",
+              "NON_FAST_FORWARD",
+              "UNKNOWN"
+            ],
+            "allowed_values": [
+              "INITIAL",
+              "SAME",
+              "FAST_FORWARD",
+              "NON_FAST_FORWARD",
+              "UNKNOWN"
+            ]
+          },
+          "previous_null": {
+            "kind": "string",
+            "const": "INITIAL_AFTER_NEW_COMMIT_AND_DOMAIN_VERIFIED"
+          },
+          "same_exact_head": {
+            "kind": "string",
+            "const": "SAME_AFTER_COMMIT_AND_DOMAIN_VERIFIED"
+          },
+          "merge_base_exit_0": {
+            "kind": "string",
+            "const": "FAST_FORWARD"
+          },
+          "merge_base_exit_1": {
+            "kind": "string",
+            "const": "NON_FAST_FORWARD"
+          },
+          "merge_base_other_exit": {
+            "kind": "string",
+            "const": "UNKNOWN"
+          },
+          "invalid_or_unprovable_domain": {
+            "kind": "string",
+            "const": "UNKNOWN"
+          },
+          "invalid_head_format": {
+            "kind": "string",
+            "const": "UNKNOWN"
+          }
+        }
+      },
+      "git_execution": {
+        "kind": "object",
+        "fields": {
+          "git_executable_token": {
+            "kind": "string",
+            "const": "git"
+          },
+          "command_timeout_milliseconds": {
+            "kind": "integer",
+            "const": 5000
+          },
+          "network_commands_forbidden": {
+            "kind": "boolean",
+            "const": true
+          },
+          "allowed_git_command_families": {
+            "kind": "array",
+            "items": {
+              "kind": "string"
+            },
+            "min_items": 3,
+            "max_items": 3,
+            "unique": true,
+            "ordered_const": [
+              "rev-parse",
+              "cat-file",
+              "merge-base --is-ancestor"
+            ],
+            "allowed_values": [
+              "rev-parse",
+              "cat-file",
+              "merge-base --is-ancestor"
+            ]
+          },
+          "commit_graph_disabled": {
+            "kind": "boolean",
+            "const": true
+          },
+          "replace_objects_disabled": {
+            "kind": "boolean",
+            "const": true
+          },
+          "system_git_config_disabled": {
+            "kind": "boolean",
+            "const": true
+          },
+          "global_git_config_disabled": {
+            "kind": "boolean",
+            "const": true
+          },
+          "terminal_prompt_disabled": {
+            "kind": "boolean",
+            "const": true
+          },
+          "optional_locks_disabled": {
+            "kind": "boolean",
+            "const": true
+          }
+        }
+      },
+      "environment_isolation": {
+        "kind": "object",
+        "fields": {
+          "strip_all_inherited_git_prefixed_variables": {
+            "kind": "boolean",
+            "const": true
+          },
+          "explicit_git_environment": {
+            "kind": "array",
+            "items": {
+              "kind": "string"
+            },
+            "min_items": 5,
+            "max_items": 5,
+            "unique": true,
+            "ordered_const": [
+              "GIT_NO_REPLACE_OBJECTS=1",
+              "GIT_CONFIG_NOSYSTEM=1",
+              "GIT_CONFIG_GLOBAL=os.devnull",
+              "GIT_TERMINAL_PROMPT=0",
+              "GIT_OPTIONAL_LOCKS=0"
+            ],
+            "allowed_values": [
+              "GIT_NO_REPLACE_OBJECTS=1",
+              "GIT_CONFIG_NOSYSTEM=1",
+              "GIT_CONFIG_GLOBAL=os.devnull",
+              "GIT_TERMINAL_PROMPT=0",
+              "GIT_OPTIONAL_LOCKS=0"
+            ]
+          },
+          "non_git_process_plumbing_may_be_preserved": {
+            "kind": "boolean",
+            "const": true
+          },
+          "git_prefixed_environment_may_not_supply_normative_authority": {
+            "kind": "boolean",
+            "const": true
+          }
+        }
+      },
+      "verified_domain": {
+        "kind": "object",
+        "fields": {
+          "repository_must_resolve": {
+            "kind": "boolean",
+            "const": true
+          },
+          "git_dir_must_equal_common_dir": {
+            "kind": "boolean",
+            "const": true
+          },
+          "linked_worktree_common_dir_mismatch_result": {
+            "kind": "string",
+            "const": "UNKNOWN"
+          },
+          "shallow_repository_result": {
+            "kind": "string",
+            "const": "UNKNOWN"
+          },
+          "info_grafts_presence_result": {
+            "kind": "string",
+            "const": "UNKNOWN"
+          },
+          "objects_info_alternates_presence_result": {
+            "kind": "string",
+            "const": "UNKNOWN"
+          },
+          "new_object_must_exist_and_be_commit": {
+            "kind": "boolean",
+            "const": true
+          },
+          "previous_object_when_present_must_exist_and_be_commit": {
+            "kind": "boolean",
+            "const": true
+          },
+          "missing_object_result": {
+            "kind": "string",
+            "const": "UNKNOWN"
+          },
+          "non_commit_result": {
+            "kind": "string",
+            "const": "UNKNOWN"
+          },
+          "timeout_result": {
+            "kind": "string",
+            "const": "UNKNOWN"
+          },
+          "corruption_or_command_error_result": {
+            "kind": "string",
+            "const": "UNKNOWN"
+          }
+        }
+      },
+      "local_fixture_cases": {
+        "kind": "array",
+        "items": {
+          "kind": "string"
+        },
+        "min_items": 17,
+        "max_items": 17,
+        "unique": true,
+        "ordered_const": [
+          "null to A -> INITIAL",
+          "A to A -> SAME",
+          "A to B -> FAST_FORWARD",
+          "B to A rollback -> NON_FAST_FORWARD",
+          "B to C divergent siblings -> NON_FAST_FORWARD",
+          "missing previous -> UNKNOWN",
+          "missing new -> UNKNOWN",
+          "blob object -> UNKNOWN",
+          "replace ref present but neutralized",
+          "shallow marker -> UNKNOWN",
+          "graft presence -> UNKNOWN",
+          "alternates file presence -> UNKNOWN",
+          "inherited GIT_DIR/GIT_OBJECT_DIRECTORY/GIT_ALTERNATE_OBJECT_DIRECTORIES neutralized",
+          "timeout -> UNKNOWN",
+          "corrupt requested object -> UNKNOWN",
+          "commit graph command influence disabled",
+          "network command absence static check"
+        ],
+        "allowed_values": [
+          "null to A -> INITIAL",
+          "A to A -> SAME",
+          "A to B -> FAST_FORWARD",
+          "B to A rollback -> NON_FAST_FORWARD",
+          "B to C divergent siblings -> NON_FAST_FORWARD",
+          "missing previous -> UNKNOWN",
+          "missing new -> UNKNOWN",
+          "blob object -> UNKNOWN",
+          "replace ref present but neutralized",
+          "shallow marker -> UNKNOWN",
+          "graft presence -> UNKNOWN",
+          "alternates file presence -> UNKNOWN",
+          "inherited GIT_DIR/GIT_OBJECT_DIRECTORY/GIT_ALTERNATE_OBJECT_DIRECTORIES neutralized",
+          "timeout -> UNKNOWN",
+          "corrupt requested object -> UNKNOWN",
+          "commit graph command influence disabled",
+          "network command absence static check"
+        ]
+      },
+      "mandatory_breakers": {
+        "kind": "array",
+        "items": {
+          "kind": "string"
+        },
+        "min_items": 9,
+        "max_items": 9,
+        "unique": true,
+        "ordered_const": [
+          "caller cannot forge transition class",
+          "merge-base exit 1 only maps NON_FAST_FORWARD after both commits and domain verified",
+          "missing object never maps NON_FAST_FORWARD",
+          "non-commit never maps NON_FAST_FORWARD",
+          "shallow/graft/alternate domain never maps FAST_FORWARD or NON_FAST_FORWARD",
+          "inherited GIT environment cannot redirect object domain",
+          "replace refs cannot alter ancestry",
+          "timeout/corruption fail closed to UNKNOWN",
+          "no fetch/ls-remote/network API inside classifier"
+        ],
+        "allowed_values": [
+          "caller cannot forge transition class",
+          "merge-base exit 1 only maps NON_FAST_FORWARD after both commits and domain verified",
+          "missing object never maps NON_FAST_FORWARD",
+          "non-commit never maps NON_FAST_FORWARD",
+          "shallow/graft/alternate domain never maps FAST_FORWARD or NON_FAST_FORWARD",
+          "inherited GIT environment cannot redirect object domain",
+          "replace refs cannot alter ancestry",
+          "timeout/corruption fail closed to UNKNOWN",
+          "no fetch/ls-remote/network API inside classifier"
+        ]
+      },
+      "stop": {
+        "kind": "string",
+        "const": "EXTERNAL_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
+      }
+    }
+  }
+}
diff --git a/tools/obsidian_projection/rpe03_ancestry_classifier_qualification_v0_1.json b/tools/obsidian_projection/rpe03_ancestry_classifier_qualification_v0_1.json
new file mode 100644
index 0000000..58617c6
--- /dev/null
+++ b/tools/obsidian_projection/rpe03_ancestry_classifier_qualification_v0_1.json
@@ -0,0 +1,117 @@
+{
+  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE03_ANCESTRY_CLASSIFIER_QUALIFICATION_V0_1",
+  "status": "QUALIFIED_FOR_EXTERNAL_REVIEW",
+  "date": "2026-10-03",
+  "branch": "feat/obsidian-projection-rpe03-ancestry-classifier-v0.1",
+  "base": {
+    "rpe01_adoption_commit": "8ed3ec4079f3f996a5159b78fc40d0f32a917b25",
+    "rpe01_adoption_blob": "49203ebc2fb208c5dd23ded140295ac00c0afab6",
+    "rpe01_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887",
+    "p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
+    "p5e_synthetic_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
+    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5"
+  },
+  "preregistration": {
+    "head": "8aa4ee2128a404fd57e64affc4f3b04751e86d87",
+    "blob": "4eca84a17f7d0c53a794f34af65d1d0a81302930",
+    "schema_blob": "621f909fcde85694a0cc7548adffad7e14ae3970",
+    "predraft_blob": "db0dd5f17d564f948305871274857c544f46ef03"
+  },
+  "red": {
+    "head": "55f00460dd1ae1004a2d450528937e7a870fc61d",
+    "test_blob": "eca438187aceb64b4d96d29bcda6c5896864b12e",
+    "report_blob": "bdc4055499b32c4e4aaa8abac788a95d3b63b3f4",
+    "result": "16 tests; 14 failures; 2 passes; implementation absent"
+  },
+  "no_lazy_fetch_amendment": {
+    "head": "b15e9ddeab00257f96cd622f3c80d45d96108e30",
+    "blob": "acb57635ee2daf0a65aa57b7f2dab7d5d7d5dcec",
+    "schema_blob": "b05984dc868655e0a05f1fab66769032fed2ab3c",
+    "required_environment": "GIT_NO_LAZY_FETCH=1"
+  },
+  "implementation": {
+    "head": "c1ccde876b9ef9e542e97dd70f290b819e837ac2",
+    "module_blob": "7c41bb66a1438c2df9e2e77149a2c3cccb131abb",
+    "main_test_blob": "d424f5becbb40d5b9a9276132a1ac684986b7d0d",
+    "mutation_test_blob": "72d5f6d5ec38c7dc5785834e636943d7ec5ad181"
+  },
+  "qualified_properties": {
+    "outputs": [
+      "INITIAL",
+      "SAME",
+      "FAST_FORWARD",
+      "NON_FAST_FORWARD",
+      "UNKNOWN"
+    ],
+    "network_commands_inside_classifier": false,
+    "caller_supplied_transition_class": false,
+    "same_checked_before_merge_base": true,
+    "initial_requires_verified_domain_and_commit": true,
+    "same_requires_verified_domain_and_commit": true,
+    "merge_base_exit_0": "FAST_FORWARD",
+    "merge_base_exit_1": "NON_FAST_FORWARD",
+    "merge_base_other": "UNKNOWN",
+    "missing_object": "UNKNOWN",
+    "non_commit_object": "UNKNOWN",
+    "timeout": "UNKNOWN",
+    "corrupt_requested_object": "UNKNOWN",
+    "linked_worktree_domain": "UNKNOWN",
+    "shallow_domain": "UNKNOWN",
+    "graft_domain": "UNKNOWN",
+    "alternates_domain": "UNKNOWN",
+    "inherited_git_environment_stripped": true,
+    "replace_objects_disabled": true,
+    "lazy_promisor_fetch_disabled": true,
+    "system_git_config_disabled": true,
+    "global_git_config_disabled": true,
+    "terminal_prompt_disabled": true,
+    "optional_locks_disabled": true,
+    "commit_graph_disabled": true,
+    "git_dir_must_equal_common_dir": true,
+    "implementation_constants_match_governed_preregistration": true,
+    "no_lazy_fetch_matches_governed_amendment": true
+  },
+  "mutation_discrimination": {
+    "checks": 4,
+    "kills": 4,
+    "survivors": 0,
+    "families": [
+      "merge-base exit-1 mapping",
+      "inherited GIT environment stripping",
+      "replace-object neutralization",
+      "no-lazy-fetch environment hardening"
+    ]
+  },
+  "test_results": {
+    "dedicated_surface": "21/21 PASS",
+    "full_targeted_regression": "134/134 PASS",
+    "p5e_contract_diff": 0,
+    "p5e_synthetic_model_diff": 0,
+    "p5d4_runtime_diff": 0
+  },
+  "qualification_environment_non_normative": {
+    "git_version": "git version 2.54.0.windows.1",
+    "python_version": "3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)]",
+    "python_implementation": "CPython",
+    "platform": "Windows-11-10.0.22631-SP0"
+  },
+  "real_p5d4_state_unchanged": {
+    "observer_events_sha256": "54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af",
+    "observer_checkpoint_sha256": "c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4",
+    "last_run_sha256": "eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259"
+  },
+  "claim_boundary": {
+    "rpe03_qualified_for_external_review": true,
+    "rpe03_human_adopted": false,
+    "rpe02_status_untouched_by_this_branch": true,
+    "rpe04_opened": false,
+    "rpe05_opened": false,
+    "rpe06_opened": false,
+    "network_used": false,
+    "real_p5e_authorized": false,
+    "p5d4_real_state_mutated": false,
+    "vault_or_current_mutated": false
+  },
+  "next_gate": "INDEPENDENT_EXTERNAL_REVIEW_THEN_HUMAN_ADJUDICATION",
+  "stop": true
+}
diff --git a/tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py b/tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py
new file mode 100644
index 0000000..7c41bb6
--- /dev/null
+++ b/tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py
@@ -0,0 +1,166 @@
+"""RPE-03 V0.1: fail-closed local Git ancestry classifier.
+
+No network operations are permitted. The classifier rebuilds a sanitized Git
+environment, verifies the local object domain, validates commit identities, and
+only then maps merge-base ancestry to the governed transition vocabulary.
+"""
+
+from __future__ import annotations
+
+import os
+import re
+import subprocess
+from pathlib import Path
+from typing import Final
+
+
+_SHA40_RE: Final = re.compile(r"[0-9a-f]{40}\Z")
+_TIMEOUT_SECONDS: Final = 5
+_SAFE_GIT_ENV_KEYS: Final = {
+    "GIT_NO_REPLACE_OBJECTS",
+    "GIT_CONFIG_NOSYSTEM",
+    "GIT_CONFIG_GLOBAL",
+    "GIT_TERMINAL_PROMPT",
+    "GIT_OPTIONAL_LOCKS",
+    "GIT_NO_LAZY_FETCH",
+}
+
+
+def _safe_git_env() -> dict[str, str]:
+    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
+    env.update(
+        {
+            "GIT_NO_REPLACE_OBJECTS": "1",
+            "GIT_CONFIG_NOSYSTEM": "1",
+            "GIT_CONFIG_GLOBAL": os.devnull,
+            "GIT_TERMINAL_PROMPT": "0",
+            "GIT_OPTIONAL_LOCKS": "0",
+            "GIT_NO_LAZY_FETCH": "1",
+        }
+    )
+    return env
+
+
+def _run_git(repo_path: Path, *args: str) -> subprocess.CompletedProcess[str] | None:
+    cmd = ["git", "-c", "core.commitGraph=false", *args]
+    try:
+        return subprocess.run(
+            cmd,
+            cwd=str(repo_path),
+            env=_safe_git_env(),
+            text=True,
+            stdout=subprocess.PIPE,
+            stderr=subprocess.PIPE,
+            timeout=_TIMEOUT_SECONDS,
+            check=False,
+        )
+    except (subprocess.TimeoutExpired, OSError, ValueError):
+        return None
+
+
+def _stdout_ok(cp: subprocess.CompletedProcess[str] | None) -> str | None:
+    if cp is None or cp.returncode != 0:
+        return None
+    return cp.stdout.strip()
+
+
+def _canonical_path(text: str, base: Path) -> Path:
+    p = Path(text)
+    if not p.is_absolute():
+        p = base / p
+    return p.resolve(strict=False)
+
+
+def _verified_domain(repo_path: Path) -> tuple[Path, Path] | None:
+    try:
+        repo = repo_path.resolve(strict=True)
+    except (OSError, RuntimeError):
+        return None
+    if not repo.exists():
+        return None
+
+    git_dir_text = _stdout_ok(_run_git(repo, "rev-parse", "--absolute-git-dir"))
+    common_dir_text = _stdout_ok(
+        _run_git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")
+    )
+    if not git_dir_text or not common_dir_text:
+        return None
+
+    git_dir = _canonical_path(git_dir_text, repo)
+    common_dir = _canonical_path(common_dir_text, repo)
+    if os.path.normcase(str(git_dir)) != os.path.normcase(str(common_dir)):
+        return None
+
+    shallow = _stdout_ok(_run_git(repo, "rev-parse", "--is-shallow-repository"))
+    if shallow is None or shallow.lower() != "false":
+        return None
+
+    if (common_dir / "shallow").exists():
+        return None
+    if (common_dir / "info" / "grafts").exists():
+        return None
+    if (common_dir / "objects" / "info" / "alternates").exists():
+        return None
+
+    return repo, common_dir
+
+
+def _valid_commit(repo: Path, sha: object) -> bool:
+    if type(sha) is not str or _SHA40_RE.fullmatch(sha) is None:
+        return False
+    cp = _run_git(repo, "cat-file", "-t", sha)
+    return cp is not None and cp.returncode == 0 and cp.stdout.strip() == "commit"
+
+
+def classify_transition(
+    repo_path,
+    previous_observed_head,
+    new_exact_observed_head,
+):
+    """Return INITIAL, SAME, FAST_FORWARD, NON_FAST_FORWARD, or UNKNOWN."""
+    if type(new_exact_observed_head) is not str or _SHA40_RE.fullmatch(
+        new_exact_observed_head
+    ) is None:
+        return "UNKNOWN"
+    if previous_observed_head is not None and (
+        type(previous_observed_head) is not str
+        or _SHA40_RE.fullmatch(previous_observed_head) is None
+    ):
+        return "UNKNOWN"
+
+    try:
+        repo_candidate = Path(repo_path)
+    except (TypeError, ValueError):
+        return "UNKNOWN"
+
+    domain = _verified_domain(repo_candidate)
+    if domain is None:
+        return "UNKNOWN"
+    repo, _common_dir = domain
+
+    if not _valid_commit(repo, new_exact_observed_head):
+        return "UNKNOWN"
+
+    if previous_observed_head is None:
+        return "INITIAL"
+
+    if not _valid_commit(repo, previous_observed_head):
+        return "UNKNOWN"
+
+    if previous_observed_head == new_exact_observed_head:
+        return "SAME"
+
+    cp = _run_git(
+        repo,
+        "merge-base",
+        "--is-ancestor",
+        previous_observed_head,
+        new_exact_observed_head,
+    )
+    if cp is None:
+        return "UNKNOWN"
+    if cp.returncode == 0:
+        return "FAST_FORWARD"
+    if cp.returncode == 1:
+        return "NON_FAST_FORWARD"
+    return "UNKNOWN"
diff --git a/tools/obsidian_projection/rpe03_no_lazy_fetch_amendment_v0_1.json b/tools/obsidian_projection/rpe03_no_lazy_fetch_amendment_v0_1.json
new file mode 100644
index 0000000..acb5763
--- /dev/null
+++ b/tools/obsidian_projection/rpe03_no_lazy_fetch_amendment_v0_1.json
@@ -0,0 +1,26 @@
+{
+  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE03_NO_LAZY_FETCH_AMENDMENT_V0_1",
+  "status": "PREREGISTERED_BEFORE_LAZY_FETCH_HARDENING",
+  "base": {
+    "rpe03_red_head": "55f00460dd1ae1004a2d450528937e7a870fc61d",
+    "rpe03_preregistration_blob": "4eca84a17f7d0c53a794f34af65d1d0a81302930"
+  },
+  "finding": {
+    "category": "IMPLICIT_NETWORK_PATH",
+    "mechanism": "Git may lazily obtain a missing object from a promisor remote on demand.",
+    "relevance": "RPE-03 forbids every network path inside the classifier."
+  },
+  "added_requirement": {
+    "environment_key": "GIT_NO_LAZY_FETCH",
+    "required_value": "1",
+    "applies_to_every_git_subprocess": true,
+    "inherited_value_must_be_removed_before_explicit_safe_value": true
+  },
+  "authority": {
+    "network_authorized": false,
+    "rpe04_authorized": false,
+    "real_p5e_authorized": false
+  },
+  "breaker": "Every captured classifier Git subprocess environment must contain GIT_NO_LAZY_FETCH=1; a mutant removing the explicit key must be killed.",
+  "stop": "REJOIN_RPE03_EXISTING_GREEN_AND_QUALIFICATION_FLOW"
+}
diff --git a/tools/obsidian_projection/rpe03_no_lazy_fetch_amendment_v0_1_schema_v0_1.json b/tools/obsidian_projection/rpe03_no_lazy_fetch_amendment_v0_1_schema_v0_1.json
new file mode 100644
index 0000000..b05984d
--- /dev/null
+++ b/tools/obsidian_projection/rpe03_no_lazy_fetch_amendment_v0_1_schema_v0_1.json
@@ -0,0 +1,93 @@
+{
+  "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
+  "artifact_role": "RPE03_NO_LAZY_FETCH_AMENDMENT",
+  "root": {
+    "kind": "object",
+    "fields": {
+      "schema": {
+        "kind": "string",
+        "const": "ATDS_OBSIDIAN_REAL_P5E_RPE03_NO_LAZY_FETCH_AMENDMENT_V0_1"
+      },
+      "status": {
+        "kind": "string",
+        "const": "PREREGISTERED_BEFORE_LAZY_FETCH_HARDENING"
+      },
+      "base": {
+        "kind": "object",
+        "fields": {
+          "rpe03_red_head": {
+            "kind": "string",
+            "const": "55f00460dd1ae1004a2d450528937e7a870fc61d"
+          },
+          "rpe03_preregistration_blob": {
+            "kind": "string",
+            "const": "4eca84a17f7d0c53a794f34af65d1d0a81302930"
+          }
+        }
+      },
+      "finding": {
+        "kind": "object",
+        "fields": {
+          "category": {
+            "kind": "string",
+            "const": "IMPLICIT_NETWORK_PATH"
+          },
+          "mechanism": {
+            "kind": "string",
+            "const": "Git may lazily obtain a missing object from a promisor remote on demand."
+          },
+          "relevance": {
+            "kind": "string",
+            "const": "RPE-03 forbids every network path inside the classifier."
+          }
+        }
+      },
+      "added_requirement": {
+        "kind": "object",
+        "fields": {
+          "environment_key": {
+            "kind": "string",
+            "const": "GIT_NO_LAZY_FETCH"
+          },
+          "required_value": {
+            "kind": "string",
+            "const": "1"
+          },
+          "applies_to_every_git_subprocess": {
+            "kind": "boolean",
+            "const": true
+          },
+          "inherited_value_must_be_removed_before_explicit_safe_value": {
+            "kind": "boolean",
+            "const": true
+          }
+        }
+      },
+      "authority": {
+        "kind": "object",
+        "fields": {
+          "network_authorized": {
+            "kind": "boolean",
+            "const": false
+          },
+          "rpe04_authorized": {
+            "kind": "boolean",
+            "const": false
+          },
+          "real_p5e_authorized": {
+            "kind": "boolean",
+            "const": false
+          }
+        }
+      },
+      "breaker": {
+        "kind": "string",
+        "const": "Every captured classifier Git subprocess environment must contain GIT_NO_LAZY_FETCH=1; a mutant removing the explicit key must be killed."
+      },
+      "stop": {
+        "kind": "string",
+        "const": "REJOIN_RPE03_EXISTING_GREEN_AND_QUALIFICATION_FLOW"
+      }
+    }
+  }
+}
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-01 HUMAN ADOPTION
Path: GOVERNANCE/RPE-01-N4-GOVERNED-CLOSED-SCHEMA-HUMAN-ADJUDICATION-2026-10-03.md
Authoritative Git blob: 49203ebc2fb208c5dd23ded140295ac00c0afab6
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
# RPE-01 — N4 GOVERNED CLOSED SCHEMA — HUMAN ADJUDICATION

Date: 2026-10-03

## Human decision

The human authority adopts:

`RPE-01 — N4 GOVERNED CLOSED SCHEMA`

in its final qualified state after:
- initial RPE-01 qualification;
- external review `PASS_WITH_NON_BLOCKING_NOTES` with no blocker;
- NB-1 / NB-2 targeted closure;
- portability and raw-breaker discrimination hardening;
- final external delta-review `PASS_WITH_NON_BLOCKING_NOTES` with `BLOCKING_FINDINGS = NONE`;
- NB-α scanner string/escape test-only closure.

The adopted normative state is:

`RPE01_GOVERNED_CLOSED_SCHEMA = QUALIFIED_AND_HUMAN_ADOPTED`

After persistence and verification of this record:

`RPE-01 = CLOSED`

This adoption does not automatically open RPE-02 or RPE-03.

## Binding pre-adoption identity

This human adoption is bound to the exact pre-adoption repository state:

```text
PRE-ADOPTION HEAD
= 686e9266f84e1a9ae05938bf3260728492a17c92

FINAL GUARD
= 26f977961d72a062199d71ffd628d5a5cc047887

P5-E GOVERNED SCHEMA
= 87e45cc75753439879e2902d3cbdbd5d71d8a1b2

FINAL HARDENING QUALIFICATION
= f514af4bf01a62b3f751e14cfffaaf20bfe66885

FINAL HARDENING QUALIFICATION REPORT
= 92e45cf8fa279c0b9643a9ad77d4c1f19d6a7cdf

NB-α TEST
= a170019180579f82e9f9ea0918f4fed445cab1ba

NB-α CLOSURE PROOF
= 76e8b5c2f85fc1088df0a25ef3df194f63904b75
```

Branch at adoption:

`feat/obsidian-projection-rpe01-governed-closed-schema-v0.1`

Pre-adoption local HEAD and remote HEAD were equal.

Pre-adoption worktree was clean.

## Adopted governed-artifact consumer contract

The following constraints are adopted for every future consumer of RPE-01:

```text
AUTHORIZED GOVERNED-ARTIFACT VALIDATION ENTRYPOINT
= validate_governed_json(raw_document, raw_schema)

UNDERSCORE-PREFIXED GUARD FUNCTIONS
= FORBIDDEN FOR EXTERNAL CONSUMERS

validate_schema_definition
= NOT AN AUTHORIZED GOVERNED-DOCUMENT VALIDATION ENTRYPOINT
```

RPE-02, RPE-03 and later consumers must carry this contract explicitly into their preregistration and implementation boundaries.

No future consumer may use a private `_*` guard function as a normative validation path.

## Adopted deterministic JSON depth rule

The final qualified guard contains the preregistered rule:

```text
MAX_GOVERNED_JSON_DEPTH = 64
```

Normative interpretation:

- JSON container nesting is counted lexically outside strings;
- a root object or array has depth 1;
- document and schema raw JSON are both checked before `json.loads`;
- depth `<= 64` is permitted by the depth guard subject to all other validation;
- depth `> 64` is rejected with `GovernedSchemaError`;
- interpreter recursion limits are not normative.

Residual validation recursion is normalized to `GovernedSchemaError` at the qualified boundary.

## Final scanner string/escape proof

NB-α is accepted as test-locked by the final test-only closure.

The qualified guard itself was not modified during NB-α closure.

The final proof establishes:

```text
container characters inside governed JSON strings
→ do not consume JSON depth budget

escaped quote/backslash handling
→ cannot hide later real container depth

in_string mutant
→ KILLED

escaped-state mutant
→ KILLED
```

Final local evidence before adoption:

```text
NB-α dedicated tests
= 4 / 4 PASS

current RPE-01 surface
= 46 / 46 PASS

P5-E + RPE-01 targeted regression
= 113 / 113 PASS
```

## Retained scope boundaries

### NB-3 — structural scope

RPE-01 protects:

- closed object structure;
- strict JSON/member handling;
- strict types;
- closed normative lists and list order where specified;
- governed schema-language structure;
- deterministic JSON depth;
- fail-closed parser/validation behavior covered by the qualified guard.

RPE-01 does not replace the adopted P5-E value-semantic invariant layer.

Existing P5-E invariants continue to carry value semantics.

Future schemas that themselves carry authority flags should normally encode those flags with explicit constraints such as `const: false` where preregistered.

### NB-4 — binding scope

`source_binding` and `artifact_role` are structurally represented and validated.

The generic RPE-01 guard does not claim dynamic verification of expected artifact role or recomputation/enforcement of source Git blob identity.

Where such dynamic binding is required, the future consumer/caller boundary must preregister and enforce it explicitly.

### NB-5 — non-blocking future hardening

The following remain non-blocking future hardening only where a distinct future failure mode requires them:

- proactive rejection of contradictory restrictive schema constraints;
- explicit ASCII regex semantics where relevant;
- isolated Unicode-surrogate handling where downstream UTF-8 persistence requires it.

These notes do not reopen RPE-01.

## NB-β / NB-c consumer-state interpretation

Static repository checks before adoption found no runtime Python consumer under `tools/` using:

- `validate_schema_definition`;
- `_validate_document`;
- `_validate_document_node`;
- `_validate_schema_node`.

No runtime Python consumer currently invokes `validate_governed_json`, which is expected because RPE-02/RPE-03 remain unopened.

Tests may exercise schema utilities directly for qualification purposes; this does not constitute a runtime governed-document consumer.

The consumer contract above is mandatory for future stages.

## Protected predecessor integrity

At adoption, the protected identities remain:

```text
P5-E ADOPTED CONTRACT
= 43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9

P5-E ADOPTED SYNTHETIC MODEL
= c0f16baa151c1466e30ba5778f1fca8184cd4aac

P5-D4 RUNTIME
= 1825e53d195ba2a63b5b646a5b78eb77939b94b5
```

No mutation of those artifacts is part of this adoption.

## Real P5-D4 state integrity before adoption

```text
observer-events.jsonl SHA256
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

observer-checkpoint.json SHA256
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json SHA256
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

No real P5-D4 control-state mutation is authorized by this persistence step.

## Stage state after verified persistence

The human decision closes RPE-01 only.

```text
RPE-01
= CLOSED
= QUALIFIED_AND_HUMAN_ADOPTED

RPE-02
= CLOSED

RPE-03
= CLOSED

RPE-04
= CLOSED

RPE-05
= CLOSED

RPE-06
= CLOSED

REAL P5-E
= CLOSED
```

Under the already adopted readiness DAG, RPE-02 and RPE-03 become eligible to be separately opened after RPE-01 closure, but this record does not itself open or authorize either stage.

## Explicitly not authorized

This adoption does not authorize:

- implementation or execution of RPE-02;
- implementation or execution of RPE-03;
- implementation or execution of RPE-04;
- implementation or execution of RPE-05;
- implementation or execution of RPE-06;
- real GitHub polling;
- sandbox repository or ref creation;
- experimental push;
- real HEAD evaluation;
- Stage A;
- Stage B;
- promotion;
- publication;
- Vault mutation;
- `CURRENT.md` mutation;
- real P5-D4 control-state mutation;
- daemon registration;
- Scheduled Task registration;
- Windows Service registration;
- startup registration;
- P6.

`REAL_P5E = CLOSED`

## Persistence authority

The only operations authorized by the human adoption statement are:

- persist this adjudication record;
- commit and push it;
- verify final repository consistency;
- STOP.

No guard, schema, qualification, test, P5-E contract/model, P5-D4 runtime, control state, Vault, CURRENT or future RPE artifact may be modified by this persistence step.
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-03 PREREGISTRATION
Path: tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1.json
Authoritative Git blob: 4eca84a17f7d0c53a794f34af65d1d0a81302930
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE03_ANCESTRY_CLASSIFIER_PREREGISTRATION_V0_1",
  "status": "PREREGISTERED_BEFORE_RED",
  "base": {
    "rpe01_adoption_commit": "8ed3ec4079f3f996a5159b78fc40d0f32a917b25",
    "rpe01_adoption_blob": "49203ebc2fb208c5dd23ded140295ac00c0afab6",
    "rpe01_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887",
    "p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9"
  },
  "authority": {
    "stage": "RPE-03",
    "rpe03_implementation_authorized": true,
    "rpe04_authorized": false,
    "rpe05_authorized": false,
    "rpe06_authorized": false,
    "network_inside_classifier_authorized": false,
    "real_p5e_authorized": false,
    "real_p5d4_state_mutation_authorized": false,
    "vault_or_current_mutation_authorized": false
  },
  "governed_config": {
    "authorized_entrypoint": "validate_governed_json(raw_document, raw_schema)",
    "private_guard_functions_forbidden": true,
    "validate_schema_definition_not_document_entrypoint": true,
    "runtime_preregistration_path": "tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1.json",
    "runtime_schema_path": "tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1_schema_v0_1.json",
    "environment_config_authority_forbidden": true,
    "cli_config_authority_forbidden": true,
    "unlisted_file_config_authority_forbidden": true
  },
  "classification": {
    "outputs": [
      "INITIAL",
      "SAME",
      "FAST_FORWARD",
      "NON_FAST_FORWARD",
      "UNKNOWN"
    ],
    "previous_null": "INITIAL_AFTER_NEW_COMMIT_AND_DOMAIN_VERIFIED",
    "same_exact_head": "SAME_AFTER_COMMIT_AND_DOMAIN_VERIFIED",
    "merge_base_exit_0": "FAST_FORWARD",
    "merge_base_exit_1": "NON_FAST_FORWARD",
    "merge_base_other_exit": "UNKNOWN",
    "invalid_or_unprovable_domain": "UNKNOWN",
    "invalid_head_format": "UNKNOWN"
  },
  "git_execution": {
    "git_executable_token": "git",
    "command_timeout_milliseconds": 5000,
    "network_commands_forbidden": true,
    "allowed_git_command_families": [
      "rev-parse",
      "cat-file",
      "merge-base --is-ancestor"
    ],
    "commit_graph_disabled": true,
    "replace_objects_disabled": true,
    "system_git_config_disabled": true,
    "global_git_config_disabled": true,
    "terminal_prompt_disabled": true,
    "optional_locks_disabled": true
  },
  "environment_isolation": {
    "strip_all_inherited_git_prefixed_variables": true,
    "explicit_git_environment": [
      "GIT_NO_REPLACE_OBJECTS=1",
      "GIT_CONFIG_NOSYSTEM=1",
      "GIT_CONFIG_GLOBAL=os.devnull",
      "GIT_TERMINAL_PROMPT=0",
      "GIT_OPTIONAL_LOCKS=0"
    ],
    "non_git_process_plumbing_may_be_preserved": true,
    "git_prefixed_environment_may_not_supply_normative_authority": true
  },
  "verified_domain": {
    "repository_must_resolve": true,
    "git_dir_must_equal_common_dir": true,
    "linked_worktree_common_dir_mismatch_result": "UNKNOWN",
    "shallow_repository_result": "UNKNOWN",
    "info_grafts_presence_result": "UNKNOWN",
    "objects_info_alternates_presence_result": "UNKNOWN",
    "new_object_must_exist_and_be_commit": true,
    "previous_object_when_present_must_exist_and_be_commit": true,
    "missing_object_result": "UNKNOWN",
    "non_commit_result": "UNKNOWN",
    "timeout_result": "UNKNOWN",
    "corruption_or_command_error_result": "UNKNOWN"
  },
  "local_fixture_cases": [
    "null to A -> INITIAL",
    "A to A -> SAME",
    "A to B -> FAST_FORWARD",
    "B to A rollback -> NON_FAST_FORWARD",
    "B to C divergent siblings -> NON_FAST_FORWARD",
    "missing previous -> UNKNOWN",
    "missing new -> UNKNOWN",
    "blob object -> UNKNOWN",
    "replace ref present but neutralized",
    "shallow marker -> UNKNOWN",
    "graft presence -> UNKNOWN",
    "alternates file presence -> UNKNOWN",
    "inherited GIT_DIR/GIT_OBJECT_DIRECTORY/GIT_ALTERNATE_OBJECT_DIRECTORIES neutralized",
    "timeout -> UNKNOWN",
    "corrupt requested object -> UNKNOWN",
    "commit graph command influence disabled",
    "network command absence static check"
  ],
  "mandatory_breakers": [
    "caller cannot forge transition class",
    "merge-base exit 1 only maps NON_FAST_FORWARD after both commits and domain verified",
    "missing object never maps NON_FAST_FORWARD",
    "non-commit never maps NON_FAST_FORWARD",
    "shallow/graft/alternate domain never maps FAST_FORWARD or NON_FAST_FORWARD",
    "inherited GIT environment cannot redirect object domain",
    "replace refs cannot alter ancestry",
    "timeout/corruption fail closed to UNKNOWN",
    "no fetch/ls-remote/network API inside classifier"
  ],
  "stop": "EXTERNAL_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
}
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-03 PREREGISTRATION SCHEMA
Path: tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1_schema_v0_1.json
Authoritative Git blob: 621f909fcde85694a0cc7548adffad7e14ae3970
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
{
  "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
  "artifact_role": "RPE03_ANCESTRY_CLASSIFIER_PREREGISTRATION",
  "root": {
    "kind": "object",
    "fields": {
      "schema": {
        "kind": "string",
        "const": "ATDS_OBSIDIAN_REAL_P5E_RPE03_ANCESTRY_CLASSIFIER_PREREGISTRATION_V0_1"
      },
      "status": {
        "kind": "string",
        "const": "PREREGISTERED_BEFORE_RED"
      },
      "base": {
        "kind": "object",
        "fields": {
          "rpe01_adoption_commit": {
            "kind": "string",
            "const": "8ed3ec4079f3f996a5159b78fc40d0f32a917b25"
          },
          "rpe01_adoption_blob": {
            "kind": "string",
            "const": "49203ebc2fb208c5dd23ded140295ac00c0afab6"
          },
          "rpe01_guard_blob": {
            "kind": "string",
            "const": "26f977961d72a062199d71ffd628d5a5cc047887"
          },
          "p5e_contract_blob": {
            "kind": "string",
            "const": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9"
          }
        }
      },
      "authority": {
        "kind": "object",
        "fields": {
          "stage": {
            "kind": "string",
            "const": "RPE-03"
          },
          "rpe03_implementation_authorized": {
            "kind": "boolean",
            "const": true
          },
          "rpe04_authorized": {
            "kind": "boolean",
            "const": false
          },
          "rpe05_authorized": {
            "kind": "boolean",
            "const": false
          },
          "rpe06_authorized": {
            "kind": "boolean",
            "const": false
          },
          "network_inside_classifier_authorized": {
            "kind": "boolean",
            "const": false
          },
          "real_p5e_authorized": {
            "kind": "boolean",
            "const": false
          },
          "real_p5d4_state_mutation_authorized": {
            "kind": "boolean",
            "const": false
          },
          "vault_or_current_mutation_authorized": {
            "kind": "boolean",
            "const": false
          }
        }
      },
      "governed_config": {
        "kind": "object",
        "fields": {
          "authorized_entrypoint": {
            "kind": "string",
            "const": "validate_governed_json(raw_document, raw_schema)"
          },
          "private_guard_functions_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "validate_schema_definition_not_document_entrypoint": {
            "kind": "boolean",
            "const": true
          },
          "runtime_preregistration_path": {
            "kind": "string",
            "const": "tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1.json"
          },
          "runtime_schema_path": {
            "kind": "string",
            "const": "tools/obsidian_projection/rpe03_ancestry_classifier_preregistration_v0_1_schema_v0_1.json"
          },
          "environment_config_authority_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "cli_config_authority_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "unlisted_file_config_authority_forbidden": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "classification": {
        "kind": "object",
        "fields": {
          "outputs": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 5,
            "max_items": 5,
            "unique": true,
            "ordered_const": [
              "INITIAL",
              "SAME",
              "FAST_FORWARD",
              "NON_FAST_FORWARD",
              "UNKNOWN"
            ],
            "allowed_values": [
              "INITIAL",
              "SAME",
              "FAST_FORWARD",
              "NON_FAST_FORWARD",
              "UNKNOWN"
            ]
          },
          "previous_null": {
            "kind": "string",
            "const": "INITIAL_AFTER_NEW_COMMIT_AND_DOMAIN_VERIFIED"
          },
          "same_exact_head": {
            "kind": "string",
            "const": "SAME_AFTER_COMMIT_AND_DOMAIN_VERIFIED"
          },
          "merge_base_exit_0": {
            "kind": "string",
            "const": "FAST_FORWARD"
          },
          "merge_base_exit_1": {
            "kind": "string",
            "const": "NON_FAST_FORWARD"
          },
          "merge_base_other_exit": {
            "kind": "string",
            "const": "UNKNOWN"
          },
          "invalid_or_unprovable_domain": {
            "kind": "string",
            "const": "UNKNOWN"
          },
          "invalid_head_format": {
            "kind": "string",
            "const": "UNKNOWN"
          }
        }
      },
      "git_execution": {
        "kind": "object",
        "fields": {
          "git_executable_token": {
            "kind": "string",
            "const": "git"
          },
          "command_timeout_milliseconds": {
            "kind": "integer",
            "const": 5000
          },
          "network_commands_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "allowed_git_command_families": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 3,
            "max_items": 3,
            "unique": true,
            "ordered_const": [
              "rev-parse",
              "cat-file",
              "merge-base --is-ancestor"
            ],
            "allowed_values": [
              "rev-parse",
              "cat-file",
              "merge-base --is-ancestor"
            ]
          },
          "commit_graph_disabled": {
            "kind": "boolean",
            "const": true
          },
          "replace_objects_disabled": {
            "kind": "boolean",
            "const": true
          },
          "system_git_config_disabled": {
            "kind": "boolean",
            "const": true
          },
          "global_git_config_disabled": {
            "kind": "boolean",
            "const": true
          },
          "terminal_prompt_disabled": {
            "kind": "boolean",
            "const": true
          },
          "optional_locks_disabled": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "environment_isolation": {
        "kind": "object",
        "fields": {
          "strip_all_inherited_git_prefixed_variables": {
            "kind": "boolean",
            "const": true
          },
          "explicit_git_environment": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 5,
            "max_items": 5,
            "unique": true,
            "ordered_const": [
              "GIT_NO_REPLACE_OBJECTS=1",
              "GIT_CONFIG_NOSYSTEM=1",
              "GIT_CONFIG_GLOBAL=os.devnull",
              "GIT_TERMINAL_PROMPT=0",
              "GIT_OPTIONAL_LOCKS=0"
            ],
            "allowed_values": [
              "GIT_NO_REPLACE_OBJECTS=1",
              "GIT_CONFIG_NOSYSTEM=1",
              "GIT_CONFIG_GLOBAL=os.devnull",
              "GIT_TERMINAL_PROMPT=0",
              "GIT_OPTIONAL_LOCKS=0"
            ]
          },
          "non_git_process_plumbing_may_be_preserved": {
            "kind": "boolean",
            "const": true
          },
          "git_prefixed_environment_may_not_supply_normative_authority": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "verified_domain": {
        "kind": "object",
        "fields": {
          "repository_must_resolve": {
            "kind": "boolean",
            "const": true
          },
          "git_dir_must_equal_common_dir": {
            "kind": "boolean",
            "const": true
          },
          "linked_worktree_common_dir_mismatch_result": {
            "kind": "string",
            "const": "UNKNOWN"
          },
          "shallow_repository_result": {
            "kind": "string",
            "const": "UNKNOWN"
          },
          "info_grafts_presence_result": {
            "kind": "string",
            "const": "UNKNOWN"
          },
          "objects_info_alternates_presence_result": {
            "kind": "string",
            "const": "UNKNOWN"
          },
          "new_object_must_exist_and_be_commit": {
            "kind": "boolean",
            "const": true
          },
          "previous_object_when_present_must_exist_and_be_commit": {
            "kind": "boolean",
            "const": true
          },
          "missing_object_result": {
            "kind": "string",
            "const": "UNKNOWN"
          },
          "non_commit_result": {
            "kind": "string",
            "const": "UNKNOWN"
          },
          "timeout_result": {
            "kind": "string",
            "const": "UNKNOWN"
          },
          "corruption_or_command_error_result": {
            "kind": "string",
            "const": "UNKNOWN"
          }
        }
      },
      "local_fixture_cases": {
        "kind": "array",
        "items": {
          "kind": "string"
        },
        "min_items": 17,
        "max_items": 17,
        "unique": true,
        "ordered_const": [
          "null to A -> INITIAL",
          "A to A -> SAME",
          "A to B -> FAST_FORWARD",
          "B to A rollback -> NON_FAST_FORWARD",
          "B to C divergent siblings -> NON_FAST_FORWARD",
          "missing previous -> UNKNOWN",
          "missing new -> UNKNOWN",
          "blob object -> UNKNOWN",
          "replace ref present but neutralized",
          "shallow marker -> UNKNOWN",
          "graft presence -> UNKNOWN",
          "alternates file presence -> UNKNOWN",
          "inherited GIT_DIR/GIT_OBJECT_DIRECTORY/GIT_ALTERNATE_OBJECT_DIRECTORIES neutralized",
          "timeout -> UNKNOWN",
          "corrupt requested object -> UNKNOWN",
          "commit graph command influence disabled",
          "network command absence static check"
        ],
        "allowed_values": [
          "null to A -> INITIAL",
          "A to A -> SAME",
          "A to B -> FAST_FORWARD",
          "B to A rollback -> NON_FAST_FORWARD",
          "B to C divergent siblings -> NON_FAST_FORWARD",
          "missing previous -> UNKNOWN",
          "missing new -> UNKNOWN",
          "blob object -> UNKNOWN",
          "replace ref present but neutralized",
          "shallow marker -> UNKNOWN",
          "graft presence -> UNKNOWN",
          "alternates file presence -> UNKNOWN",
          "inherited GIT_DIR/GIT_OBJECT_DIRECTORY/GIT_ALTERNATE_OBJECT_DIRECTORIES neutralized",
          "timeout -> UNKNOWN",
          "corrupt requested object -> UNKNOWN",
          "commit graph command influence disabled",
          "network command absence static check"
        ]
      },
      "mandatory_breakers": {
        "kind": "array",
        "items": {
          "kind": "string"
        },
        "min_items": 9,
        "max_items": 9,
        "unique": true,
        "ordered_const": [
          "caller cannot forge transition class",
          "merge-base exit 1 only maps NON_FAST_FORWARD after both commits and domain verified",
          "missing object never maps NON_FAST_FORWARD",
          "non-commit never maps NON_FAST_FORWARD",
          "shallow/graft/alternate domain never maps FAST_FORWARD or NON_FAST_FORWARD",
          "inherited GIT environment cannot redirect object domain",
          "replace refs cannot alter ancestry",
          "timeout/corruption fail closed to UNKNOWN",
          "no fetch/ls-remote/network API inside classifier"
        ],
        "allowed_values": [
          "caller cannot forge transition class",
          "merge-base exit 1 only maps NON_FAST_FORWARD after both commits and domain verified",
          "missing object never maps NON_FAST_FORWARD",
          "non-commit never maps NON_FAST_FORWARD",
          "shallow/graft/alternate domain never maps FAST_FORWARD or NON_FAST_FORWARD",
          "inherited GIT environment cannot redirect object domain",
          "replace refs cannot alter ancestry",
          "timeout/corruption fail closed to UNKNOWN",
          "no fetch/ls-remote/network API inside classifier"
        ]
      },
      "stop": {
        "kind": "string",
        "const": "EXTERNAL_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
      }
    }
  }
}
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-03 NO-LAZY-FETCH AMENDMENT
Path: tools/obsidian_projection/rpe03_no_lazy_fetch_amendment_v0_1.json
Authoritative Git blob: acb57635ee2daf0a65aa57b7f2dab7d5d7d5dcec
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE03_NO_LAZY_FETCH_AMENDMENT_V0_1",
  "status": "PREREGISTERED_BEFORE_LAZY_FETCH_HARDENING",
  "base": {
    "rpe03_red_head": "55f00460dd1ae1004a2d450528937e7a870fc61d",
    "rpe03_preregistration_blob": "4eca84a17f7d0c53a794f34af65d1d0a81302930"
  },
  "finding": {
    "category": "IMPLICIT_NETWORK_PATH",
    "mechanism": "Git may lazily obtain a missing object from a promisor remote on demand.",
    "relevance": "RPE-03 forbids every network path inside the classifier."
  },
  "added_requirement": {
    "environment_key": "GIT_NO_LAZY_FETCH",
    "required_value": "1",
    "applies_to_every_git_subprocess": true,
    "inherited_value_must_be_removed_before_explicit_safe_value": true
  },
  "authority": {
    "network_authorized": false,
    "rpe04_authorized": false,
    "real_p5e_authorized": false
  },
  "breaker": "Every captured classifier Git subprocess environment must contain GIT_NO_LAZY_FETCH=1; a mutant removing the explicit key must be killed.",
  "stop": "REJOIN_RPE03_EXISTING_GREEN_AND_QUALIFICATION_FLOW"
}
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-03 NO-LAZY-FETCH AMENDMENT SCHEMA
Path: tools/obsidian_projection/rpe03_no_lazy_fetch_amendment_v0_1_schema_v0_1.json
Authoritative Git blob: b05984dc868655e0a05f1fab66769032fed2ab3c
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
{
  "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
  "artifact_role": "RPE03_NO_LAZY_FETCH_AMENDMENT",
  "root": {
    "kind": "object",
    "fields": {
      "schema": {
        "kind": "string",
        "const": "ATDS_OBSIDIAN_REAL_P5E_RPE03_NO_LAZY_FETCH_AMENDMENT_V0_1"
      },
      "status": {
        "kind": "string",
        "const": "PREREGISTERED_BEFORE_LAZY_FETCH_HARDENING"
      },
      "base": {
        "kind": "object",
        "fields": {
          "rpe03_red_head": {
            "kind": "string",
            "const": "55f00460dd1ae1004a2d450528937e7a870fc61d"
          },
          "rpe03_preregistration_blob": {
            "kind": "string",
            "const": "4eca84a17f7d0c53a794f34af65d1d0a81302930"
          }
        }
      },
      "finding": {
        "kind": "object",
        "fields": {
          "category": {
            "kind": "string",
            "const": "IMPLICIT_NETWORK_PATH"
          },
          "mechanism": {
            "kind": "string",
            "const": "Git may lazily obtain a missing object from a promisor remote on demand."
          },
          "relevance": {
            "kind": "string",
            "const": "RPE-03 forbids every network path inside the classifier."
          }
        }
      },
      "added_requirement": {
        "kind": "object",
        "fields": {
          "environment_key": {
            "kind": "string",
            "const": "GIT_NO_LAZY_FETCH"
          },
          "required_value": {
            "kind": "string",
            "const": "1"
          },
          "applies_to_every_git_subprocess": {
            "kind": "boolean",
            "const": true
          },
          "inherited_value_must_be_removed_before_explicit_safe_value": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "authority": {
        "kind": "object",
        "fields": {
          "network_authorized": {
            "kind": "boolean",
            "const": false
          },
          "rpe04_authorized": {
            "kind": "boolean",
            "const": false
          },
          "real_p5e_authorized": {
            "kind": "boolean",
            "const": false
          }
        }
      },
      "breaker": {
        "kind": "string",
        "const": "Every captured classifier Git subprocess environment must contain GIT_NO_LAZY_FETCH=1; a mutant removing the explicit key must be killed."
      },
      "stop": {
        "kind": "string",
        "const": "REJOIN_RPE03_EXISTING_GREEN_AND_QUALIFICATION_FLOW"
      }
    }
  }
}
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-03 RED TEST
Path: tests/obsidian_projection/test_rpe03_ancestry_classifier_v0_1.py
Authoritative Git blob: d424f5becbb40d5b9a9276132a1ac684986b7d0d
Display copy is normalized for packet formatting and is not claimed byte-identical.
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

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-03 RED REPORT
Path: reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE03-ANCESTRY-CLASSIFIER-RED.md
Authoritative Git blob: bdc4055499b32c4e4aaa8abac788a95d3b63b3f4
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
﻿# RPE-03 — NB5 ANCESTRY CLASSIFIER V0.1 — RED EVIDENCE

Date: 2026-10-03

## Preregistered predecessor

Preregistration HEAD:
8aa4ee2128a404fd57e64affc4f3b04751e86d87

Preregistration blob:
4eca84a17f7d0c53a794f34af65d1d0a81302930

Preregistration schema blob:
621f909fcde85694a0cc7548adffad7e14ae3970

## RED command

python -B -m unittest tests.obsidian_projection.test_rpe03_ancestry_classifier_v0_1

## Observed result

Ran 16 tests.

FAILED (failures=14).

RPE03_RED_EXIT=1.

Two tests passed:
- governed preregistration validates through RPE-01;
- the absent classifier source contains no forbidden network tokens by construction.

The fourteen RED failures arise because
tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py
does not yet exist.

The frozen test surface already covers INITIAL/SAME/FAST_FORWARD/NON_FAST_FORWARD, missing and non-commit objects, shallow/graft/alternate domains, inherited Git environment, replace refs, timeout, requested-object corruption, linked worktrees, commit-graph disabling, environment sanitization and invalid head identities.

No network operation or protected predecessor mutation occurred.

RPE-04 = CLOSED.
RPE-05 = CLOSED.
RPE-06 = CLOSED.
REAL P5-E = CLOSED.
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-03 IMPLEMENTATION
Path: tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py
Authoritative Git blob: 7c41bb66a1438c2df9e2e77149a2c3cccb131abb
Display copy is normalized for packet formatting and is not claimed byte-identical.
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


def _verified_domain(repo_path: Path) -> tuple[Path, Path] | None:
    try:
        repo = repo_path.resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    if not repo.exists():
        return None

    git_dir_text = _stdout_ok(_run_git(repo, "rev-parse", "--absolute-git-dir"))
    common_dir_text = _stdout_ok(
        _run_git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")
    )
    if not git_dir_text or not common_dir_text:
        return None

    git_dir = _canonical_path(git_dir_text, repo)
    common_dir = _canonical_path(common_dir_text, repo)
    if os.path.normcase(str(git_dir)) != os.path.normcase(str(common_dir)):
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

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-03 MUTATION TEST
Path: tests/obsidian_projection/test_rpe03_ancestry_classifier_mutation_v0_1.py
Authoritative Git blob: 72d5f6d5ec38c7dc5785834e636943d7ec5ad181
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
import os
import subprocess
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools" / "obsidian_projection" / "rpe03_ancestry_classifier_v0_1.py"


def load_source_module(name, replacements=()):
    source = MODULE.read_text(encoding="utf-8")
    for old, new in replacements:
        if source.count(old) != 1:
            raise AssertionError(f"mutation anchor count != 1: {old!r}")
        source = source.replace(old, new, 1)
    module = types.ModuleType(name)
    module.__file__ = str(MODULE)
    exec(compile(source, str(MODULE), "exec"), module.__dict__)
    return module


def git(repo, *args):
    cp = subprocess.run(
        ["git", *args],
        cwd=str(repo),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if cp.returncode != 0:
        raise AssertionError(cp.stderr)
    return cp.stdout.strip()


def make_linear_graph():
    td = tempfile.TemporaryDirectory()
    repo = Path(td.name)
    git(repo, "init")
    git(repo, "config", "user.email", "rpe03-mut@example.invalid")
    git(repo, "config", "user.name", "RPE03 Mut")
    (repo / "f.txt").write_text("A\n", encoding="utf-8")
    git(repo, "add", "f.txt")
    git(repo, "commit", "-m", "A")
    a = git(repo, "rev-parse", "HEAD")
    (repo / "f.txt").write_text("B\n", encoding="utf-8")
    git(repo, "commit", "-am", "B")
    b = git(repo, "rev-parse", "HEAD")
    return td, repo, a, b


class TestRPE03MutationDiscriminationV01(unittest.TestCase):
    def test_exit_one_mapping_mutant_is_killed(self):
        base = load_source_module("rpe03_base_exit1")
        mutant = load_source_module(
            "rpe03_mut_exit1",
            ((
                '    if cp.returncode == 1:\n        return "NON_FAST_FORWARD"',
                '    if cp.returncode == 1:\n        return "FAST_FORWARD"',
            ),),
        )
        td, repo, a, b = make_linear_graph()
        try:
            self.assertEqual(base.classify_transition(repo, b, a), "NON_FAST_FORWARD")
            self.assertEqual(mutant.classify_transition(repo, b, a), "FAST_FORWARD")
        finally:
            td.cleanup()

    def test_inherited_git_environment_strip_mutant_is_killed(self):
        base = load_source_module("rpe03_base_env")
        mutant = load_source_module(
            "rpe03_mut_env",
            ((
                'env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}',
                'env = dict(os.environ)',
            ),),
        )
        td, repo, a, b = make_linear_graph()
        try:
            hostile = {
                "GIT_DIR": "X:/forbidden",
                "GIT_OBJECT_DIRECTORY": "X:/forbidden-objects",
                "GIT_ALTERNATE_OBJECT_DIRECTORIES": "X:/forbidden-alt",
            }
            with mock.patch.dict(os.environ, hostile, clear=False):
                self.assertEqual(base.classify_transition(repo, a, b), "FAST_FORWARD")
                self.assertNotEqual(mutant.classify_transition(repo, a, b), "FAST_FORWARD")
        finally:
            td.cleanup()

    def test_replace_object_neutralization_mutant_is_killed(self):
        base = load_source_module("rpe03_base_replace")
        mutant = load_source_module(
            "rpe03_mut_replace",
            (('            "GIT_NO_REPLACE_OBJECTS": "1",\n', ""),),
        )
        td, repo, a, b = make_linear_graph()
        try:
            tree = git(repo, "rev-parse", f"{a}^{{tree}}")
            root = git(repo, "commit-tree", tree, "-m", "unrelated replacement root")
            git(repo, "replace", b, root)
            self.assertEqual(base.classify_transition(repo, a, b), "FAST_FORWARD")
            self.assertNotEqual(mutant.classify_transition(repo, a, b), "FAST_FORWARD")
        finally:
            td.cleanup()

    def test_no_lazy_fetch_environment_mutant_is_killed(self):
        base = load_source_module("rpe03_base_lazy")
        mutant = load_source_module(
            "rpe03_mut_lazy",
            (('            "GIT_NO_LAZY_FETCH": "1",\n', ""),),
        )
        self.assertEqual(base._safe_git_env()["GIT_NO_LAZY_FETCH"], "1")
        self.assertNotIn("GIT_NO_LAZY_FETCH", mutant._safe_git_env())


if __name__ == "__main__":
    unittest.main()
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-03 QUALIFICATION JSON
Path: tools/obsidian_projection/rpe03_ancestry_classifier_qualification_v0_1.json
Authoritative Git blob: 58617c68b8200b994d4fa058224e749fd5396730
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE03_ANCESTRY_CLASSIFIER_QUALIFICATION_V0_1",
  "status": "QUALIFIED_FOR_EXTERNAL_REVIEW",
  "date": "2026-10-03",
  "branch": "feat/obsidian-projection-rpe03-ancestry-classifier-v0.1",
  "base": {
    "rpe01_adoption_commit": "8ed3ec4079f3f996a5159b78fc40d0f32a917b25",
    "rpe01_adoption_blob": "49203ebc2fb208c5dd23ded140295ac00c0afab6",
    "rpe01_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887",
    "p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
    "p5e_synthetic_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5"
  },
  "preregistration": {
    "head": "8aa4ee2128a404fd57e64affc4f3b04751e86d87",
    "blob": "4eca84a17f7d0c53a794f34af65d1d0a81302930",
    "schema_blob": "621f909fcde85694a0cc7548adffad7e14ae3970",
    "predraft_blob": "db0dd5f17d564f948305871274857c544f46ef03"
  },
  "red": {
    "head": "55f00460dd1ae1004a2d450528937e7a870fc61d",
    "test_blob": "eca438187aceb64b4d96d29bcda6c5896864b12e",
    "report_blob": "bdc4055499b32c4e4aaa8abac788a95d3b63b3f4",
    "result": "16 tests; 14 failures; 2 passes; implementation absent"
  },
  "no_lazy_fetch_amendment": {
    "head": "b15e9ddeab00257f96cd622f3c80d45d96108e30",
    "blob": "acb57635ee2daf0a65aa57b7f2dab7d5d7d5dcec",
    "schema_blob": "b05984dc868655e0a05f1fab66769032fed2ab3c",
    "required_environment": "GIT_NO_LAZY_FETCH=1"
  },
  "implementation": {
    "head": "c1ccde876b9ef9e542e97dd70f290b819e837ac2",
    "module_blob": "7c41bb66a1438c2df9e2e77149a2c3cccb131abb",
    "main_test_blob": "d424f5becbb40d5b9a9276132a1ac684986b7d0d",
    "mutation_test_blob": "72d5f6d5ec38c7dc5785834e636943d7ec5ad181"
  },
  "qualified_properties": {
    "outputs": [
      "INITIAL",
      "SAME",
      "FAST_FORWARD",
      "NON_FAST_FORWARD",
      "UNKNOWN"
    ],
    "network_commands_inside_classifier": false,
    "caller_supplied_transition_class": false,
    "same_checked_before_merge_base": true,
    "initial_requires_verified_domain_and_commit": true,
    "same_requires_verified_domain_and_commit": true,
    "merge_base_exit_0": "FAST_FORWARD",
    "merge_base_exit_1": "NON_FAST_FORWARD",
    "merge_base_other": "UNKNOWN",
    "missing_object": "UNKNOWN",
    "non_commit_object": "UNKNOWN",
    "timeout": "UNKNOWN",
    "corrupt_requested_object": "UNKNOWN",
    "linked_worktree_domain": "UNKNOWN",
    "shallow_domain": "UNKNOWN",
    "graft_domain": "UNKNOWN",
    "alternates_domain": "UNKNOWN",
    "inherited_git_environment_stripped": true,
    "replace_objects_disabled": true,
    "lazy_promisor_fetch_disabled": true,
    "system_git_config_disabled": true,
    "global_git_config_disabled": true,
    "terminal_prompt_disabled": true,
    "optional_locks_disabled": true,
    "commit_graph_disabled": true,
    "git_dir_must_equal_common_dir": true,
    "implementation_constants_match_governed_preregistration": true,
    "no_lazy_fetch_matches_governed_amendment": true
  },
  "mutation_discrimination": {
    "checks": 4,
    "kills": 4,
    "survivors": 0,
    "families": [
      "merge-base exit-1 mapping",
      "inherited GIT environment stripping",
      "replace-object neutralization",
      "no-lazy-fetch environment hardening"
    ]
  },
  "test_results": {
    "dedicated_surface": "21/21 PASS",
    "full_targeted_regression": "134/134 PASS",
    "p5e_contract_diff": 0,
    "p5e_synthetic_model_diff": 0,
    "p5d4_runtime_diff": 0
  },
  "qualification_environment_non_normative": {
    "git_version": "git version 2.54.0.windows.1",
    "python_version": "3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)]",
    "python_implementation": "CPython",
    "platform": "Windows-11-10.0.22631-SP0"
  },
  "real_p5d4_state_unchanged": {
    "observer_events_sha256": "54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af",
    "observer_checkpoint_sha256": "c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4",
    "last_run_sha256": "eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259"
  },
  "claim_boundary": {
    "rpe03_qualified_for_external_review": true,
    "rpe03_human_adopted": false,
    "rpe02_status_untouched_by_this_branch": true,
    "rpe04_opened": false,
    "rpe05_opened": false,
    "rpe06_opened": false,
    "network_used": false,
    "real_p5e_authorized": false,
    "p5d4_real_state_mutated": false,
    "vault_or_current_mutated": false
  },
  "next_gate": "INDEPENDENT_EXTERNAL_REVIEW_THEN_HUMAN_ADJUDICATION",
  "stop": true
}
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-03 QUALIFICATION REPORT
Path: reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE03-ANCESTRY-CLASSIFIER-QUALIFICATION.md
Authoritative Git blob: 721ef61dd3a65a2c2bfe676c87cf2b35a4730457
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
# RPE-03 — NB5 ANCESTRY CLASSIFIER V0.1 — QUALIFICATION

Date: 2026-10-03

## Verdict

`RPE-03 = QUALIFIED_FOR_EXTERNAL_REVIEW`

Human adoption is pending. RPE-04/RPE-05/RPE-06 and REAL P5-E remain closed.

## Canonical base

RPE-01 adoption commit:
`8ed3ec4079f3f996a5159b78fc40d0f32a917b25`

RPE-01 adoption blob:
`49203ebc2fb208c5dd23ded140295ac00c0afab6`

The adopted P5-E contract, synthetic model and P5-D4 runtime remain unchanged.

## Preregistration and RED

Preregistration HEAD:
`8aa4ee2128a404fd57e64affc4f3b04751e86d87`

Preregistration blob:
`4eca84a17f7d0c53a794f34af65d1d0a81302930`

Closed-schema blob:
`621f909fcde85694a0cc7548adffad7e14ae3970`

The preregistration validates through the adopted RPE-01 public entrypoint.

RED HEAD:
`55f00460dd1ae1004a2d450528937e7a870fc61d`

Observed RED:
`16 tests / 14 failures / 2 passes`.

The fourteen failures reflected the absence of the preregistered classifier.

A Windows-only fixture correction was later required for the corruption test: Git's loose object was non-writable, so the fixture now makes it writable and corrupts its bytes instead of deleting it. No classifier correction was required by that fixture issue.

## No-lazy-fetch hardening amendment

During adversarial qualification, the no-network contract was tightened against Git promisor-object lazy retrieval.

Amendment HEAD:
`b15e9ddeab00257f96cd622f3c80d45d96108e30`

Amendment blob:
`acb57635ee2daf0a65aa57b7f2dab7d5d7d5dcec`

Amendment schema:
`b05984dc868655e0a05f1fab66769032fed2ab3c`

Every classifier Git subprocess receives:
`GIT_NO_LAZY_FETCH=1`.

## Final implementation

Implementation HEAD:
`c1ccde876b9ef9e542e97dd70f290b819e837ac2`

Module:
`7c41bb66a1438c2df9e2e77149a2c3cccb131abb`

Main tests:
`d424f5becbb40d5b9a9276132a1ac684986b7d0d`

Mutation tests:
`72d5f6d5ec38c7dc5785834e636943d7ec5ad181`

## Qualified classifier semantics

The only outputs are:

```text
INITIAL
SAME
FAST_FORWARD
NON_FAST_FORWARD
UNKNOWN
```

The caller cannot provide or override a transition class.

Before classification, the component verifies the local Git domain and requested commit identities.

Fail-closed cases map to `UNKNOWN`, including:
- invalid SHA identity;
- missing object;
- non-commit object;
- command failure;
- timeout;
- requested-object corruption;
- linked worktree/common-dir mismatch;
- shallow repository;
- graft presence;
- objects/info/alternates presence.

`SAME` is explicit and precedes ancestry testing.

`INITIAL` requires a verified new commit in a verified domain and no predecessor.

Only after both commit identities and the object domain are verified does:

`git merge-base --is-ancestor A B`

map:
- exit 0 → `FAST_FORWARD`;
- exit 1 → `NON_FAST_FORWARD`;
- other exit → `UNKNOWN`.

## Git execution isolation

Every Git subprocess:
- uses only local command families `rev-parse`, `cat-file`, and `merge-base --is-ancestor`;
- uses `-c core.commitGraph=false`;
- strips all inherited `GIT_*` variables;
- sets `GIT_NO_REPLACE_OBJECTS=1`;
- sets `GIT_NO_LAZY_FETCH=1`;
- disables system and global Git config;
- disables terminal prompts;
- disables optional locks.

The source contains no network command/API family used by the classifier.

## Governed configuration provenance

The RPE-03 preregistration and its no-lazy-fetch amendment are both closed-schema artifacts validated through RPE-01.

A dedicated parity test binds implementation timeout/environment requirements to those governed artifacts.

No environment, CLI or unlisted file supplies normative classifier authority.

## Mutation/discrimination

Four targeted mutants were killed:

1. merge-base exit 1 incorrectly mapped to FAST_FORWARD;
2. inherited `GIT_*` stripping removed;
3. replace-object neutralization removed;
4. explicit no-lazy-fetch environment hardening removed.

Result:
`4 / 4 KILLED`.

The replace-object mutation uses an unrelated replacement root so the mutant actually changes the ancestry outcome.

## Test result

Dedicated RPE-03 surface:
`21 / 21 PASS`

P5-E + RPE-01 + RPE-03 targeted regression:
`134 / 134 PASS`

Protected diffs:
```text
P5-E CONTRACT = 0
P5-E SYNTHETIC MODEL = 0
P5-D4 RUNTIME = 0
```

Qualification environment:
`Git 2.54.0.windows.1 / CPython 3.13.14 / Windows-11-10.0.22631-SP0`.

## Authority boundary

This qualification does not authorize:
- RPE-04/05/06;
- fetch, remote observation or GitHub polling;
- P5-D4 real-state mutation;
- Vault/CURRENT mutation;
- REAL P5-E;
- human adoption of RPE-03.

Maximum claim:
`RPE03_ANCESTRY_CLASSIFIER = QUALIFIED_FOR_EXTERNAL_REVIEW`.
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: ADOPTED RPE-01 GUARD
Path: tools/obsidian_projection/rpe01_governed_closed_schema.py
Authoritative Git blob: 26f977961d72a062199d71ffd628d5a5cc047887
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
from __future__ import annotations

import json
import re
from typing import Any


SCHEMA_ID = "ATDS_GOVERNED_JSON_SCHEMA_V0_1"
MAX_GOVERNED_JSON_DEPTH = 64
_ALLOWED_KINDS = {"object", "array", "string", "integer", "boolean", "null"}
_SHA1_RE = re.compile(r"[0-9a-f]{40}\Z")


class GovernedSchemaError(ValueError):
    pass


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise GovernedSchemaError(f"duplicate JSON member: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise GovernedSchemaError(f"non-standard JSON numeric constant forbidden: {value}")


def _enforce_max_json_depth(text: str) -> None:
    depth = 0
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
            continue

        if char in "[{":
            depth += 1
            if depth > MAX_GOVERNED_JSON_DEPTH:
                raise GovernedSchemaError(
                    "maximum governed JSON depth exceeded: "
                    f"{depth} > {MAX_GOVERNED_JSON_DEPTH}"
                )
        elif char in "]}":
            depth -= 1


def parse_json_strict(raw: str | bytes) -> Any:
    if isinstance(raw, bytes):
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise GovernedSchemaError(f"governed JSON must be valid UTF-8: {exc}") from exc
    elif isinstance(raw, str):
        text = raw
    else:
        raise GovernedSchemaError("raw governed JSON must be str or bytes")
    _enforce_max_json_depth(text)
    try:
        return json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except GovernedSchemaError:
        raise
    except (json.JSONDecodeError, ValueError, RecursionError) as exc:
        raise GovernedSchemaError(
            f"invalid or unsupported governed JSON: {type(exc).__name__}: {exc}"
        ) from exc


def _exact_keys(label: str, value: object, allowed: set[str], required: set[str]) -> dict[str, Any]:
    if type(value) is not dict:
        raise GovernedSchemaError(f"{label} must be an object")
    actual = set(value)
    unknown = actual - allowed
    missing = required - actual
    if unknown or missing:
        raise GovernedSchemaError(
            f"{label} schema mismatch: missing={sorted(missing)} unknown={sorted(unknown)}"
        )
    return value


def _strict_int(label: str, value: object, *, minimum: int | None = None) -> int:
    if type(value) is not int:
        raise GovernedSchemaError(f"{label} must be an integer")
    if minimum is not None and value < minimum:
        raise GovernedSchemaError(f"{label} must be >= {minimum}")
    return value


def _strict_bool(label: str, value: object) -> bool:
    if type(value) is not bool:
        raise GovernedSchemaError(f"{label} must be a boolean")
    return value


def _strict_string(label: str, value: object, *, nonempty: bool = True) -> str:
    if type(value) is not str:
        raise GovernedSchemaError(f"{label} must be a string")
    if nonempty and not value:
        raise GovernedSchemaError(f"{label} must be non-empty")
    return value


def _unique_json_values(values: list[Any]) -> bool:
    encoded = [
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        for value in values
    ]
    return len(encoded) == len(set(encoded))


def _value_matches_kind(value: object, kind: str) -> bool:
    if kind == "object":
        return type(value) is dict
    if kind == "array":
        return type(value) is list
    if kind == "string":
        return type(value) is str
    if kind == "integer":
        return type(value) is int
    if kind == "boolean":
        return type(value) is bool
    if kind == "null":
        return value is None
    return False


def _validate_constraint_value(label: str, value: object, kind: str) -> None:
    if not _value_matches_kind(value, kind):
        raise GovernedSchemaError(f"{label} does not match node kind {kind}")


def _validate_schema_node(node: object, path: str) -> None:
    if type(node) is not dict:
        raise GovernedSchemaError(f"{path} schema node must be an object")
    kind = node.get("kind")
    if type(kind) is not str or kind not in _ALLOWED_KINDS:
        raise GovernedSchemaError(f"{path}.kind unsupported")

    if kind == "object":
        allowed = {"kind", "fields"}
        _exact_keys(path, node, allowed, allowed)
        fields = node["fields"]
        if type(fields) is not dict or not fields:
            raise GovernedSchemaError(f"{path}.fields must be a non-empty object")
        for name, child in fields.items():
            _strict_string(f"{path}.fields key", name)
            _validate_schema_node(child, f"{path}.fields.{name}")
        return

    if kind == "array":
        allowed = {
            "kind", "items", "min_items", "max_items", "unique",
            "ordered_const", "allowed_values",
        }
        _exact_keys(path, node, allowed, {"kind", "items"})
        _validate_schema_node(node["items"], f"{path}.items")
        item_kind = node["items"]["kind"]

        minimum = None
        maximum = None
        if "min_items" in node:
            minimum = _strict_int(f"{path}.min_items", node["min_items"], minimum=0)
        if "max_items" in node:
            maximum = _strict_int(f"{path}.max_items", node["max_items"], minimum=0)
        if minimum is not None and maximum is not None and minimum > maximum:
            raise GovernedSchemaError(f"{path} min_items exceeds max_items")
        if "unique" in node:
            _strict_bool(f"{path}.unique", node["unique"])
        for constraint in ("ordered_const", "allowed_values"):
            if constraint not in node:
                continue
            values = node[constraint]
            if type(values) is not list:
                raise GovernedSchemaError(f"{path}.{constraint} must be an array")
            for index, value in enumerate(values):
                _validate_constraint_value(
                    f"{path}.{constraint}[{index}]",
                    value,
                    item_kind,
                )
            if not _unique_json_values(values):
                raise GovernedSchemaError(f"{path}.{constraint} must not contain duplicates")
        if "ordered_const" in node:
            ordered = node["ordered_const"]
            if minimum is not None and len(ordered) < minimum:
                raise GovernedSchemaError(f"{path}.ordered_const shorter than min_items")
            if maximum is not None and len(ordered) > maximum:
                raise GovernedSchemaError(f"{path}.ordered_const longer than max_items")
        return

    if kind == "string":
        allowed = {"kind", "const", "enum", "pattern"}
        _exact_keys(path, node, allowed, {"kind"})
        if "const" in node:
            _validate_constraint_value(f"{path}.const", node["const"], kind)
        if "enum" in node:
            enum = node["enum"]
            if type(enum) is not list or not enum:
                raise GovernedSchemaError(f"{path}.enum must be a non-empty array")
            for index, value in enumerate(enum):
                _validate_constraint_value(f"{path}.enum[{index}]", value, kind)
            if not _unique_json_values(enum):
                raise GovernedSchemaError(f"{path}.enum must be unique")
        if "pattern" in node:
            pattern = _strict_string(f"{path}.pattern", node["pattern"])
            try:
                re.compile(pattern)
            except re.error as exc:
                raise GovernedSchemaError(f"{path}.pattern invalid: {exc}") from exc
        return

    if kind == "integer":
        allowed = {"kind", "const", "enum", "minimum", "maximum"}
        _exact_keys(path, node, allowed, {"kind"})
        if "const" in node:
            _validate_constraint_value(f"{path}.const", node["const"], kind)
        if "enum" in node:
            enum = node["enum"]
            if type(enum) is not list or not enum:
                raise GovernedSchemaError(f"{path}.enum must be a non-empty array")
            for index, value in enumerate(enum):
                _validate_constraint_value(f"{path}.enum[{index}]", value, kind)
            if not _unique_json_values(enum):
                raise GovernedSchemaError(f"{path}.enum must be unique")
        minimum = None
        maximum = None
        if "minimum" in node:
            minimum = _strict_int(f"{path}.minimum", node["minimum"])
        if "maximum" in node:
            maximum = _strict_int(f"{path}.maximum", node["maximum"])
        if minimum is not None and maximum is not None and minimum > maximum:
            raise GovernedSchemaError(f"{path} minimum exceeds maximum")
        return

    if kind == "boolean":
        allowed = {"kind", "const"}
        _exact_keys(path, node, allowed, {"kind"})
        if "const" in node:
            _validate_constraint_value(f"{path}.const", node["const"], kind)
        return

    if kind == "null":
        _exact_keys(path, node, {"kind"}, {"kind"})
        return

    raise GovernedSchemaError(f"{path}.kind unsupported")


def _validate_schema_definition(schema: object) -> dict[str, Any]:
    top = _exact_keys(
        "schema",
        schema,
        {"schema", "artifact_role", "source_binding", "root"},
        {"schema", "artifact_role", "root"},
    )
    if top["schema"] != SCHEMA_ID:
        raise GovernedSchemaError("unsupported governed schema version")
    _strict_string("schema.artifact_role", top["artifact_role"])
    if "source_binding" in top:
        binding = _exact_keys(
            "schema.source_binding",
            top["source_binding"],
            {"path", "git_blob"},
            {"path", "git_blob"},
        )
        _strict_string("schema.source_binding.path", binding["path"])
        blob = _strict_string("schema.source_binding.git_blob", binding["git_blob"])
        if _SHA1_RE.fullmatch(blob) is None:
            raise GovernedSchemaError("schema.source_binding.git_blob must be lowercase 40-hex")
    _validate_schema_node(top["root"], "schema.root")
    return top


def validate_schema_definition(schema: object) -> dict[str, Any]:
    try:
        return _validate_schema_definition(schema)
    except GovernedSchemaError:
        raise
    except RecursionError as exc:
        raise GovernedSchemaError(
            "governed schema validation exceeded recursion safety boundary"
        ) from exc


def _validate_document_node(value: object, node: dict[str, Any], path: str) -> None:
    kind = node["kind"]
    if not _value_matches_kind(value, kind):
        raise GovernedSchemaError(f"{path} must be {kind}")

    if kind == "object":
        fields = node["fields"]
        actual = set(value)
        expected = set(fields)
        if actual != expected:
            raise GovernedSchemaError(
                f"{path} closed-schema mismatch: "
                f"missing={sorted(expected - actual)} unknown={sorted(actual - expected)}"
            )
        for key, child in fields.items():
            _validate_document_node(value[key], child, f"{path}.{key}")
        return

    if kind == "array":
        length = len(value)
        if "min_items" in node and length < node["min_items"]:
            raise GovernedSchemaError(f"{path} shorter than min_items")
        if "max_items" in node and length > node["max_items"]:
            raise GovernedSchemaError(f"{path} longer than max_items")
        if node.get("unique") is True and not _unique_json_values(value):
            raise GovernedSchemaError(f"{path} contains duplicate items")
        if "allowed_values" in node:
            allowed = node["allowed_values"]
            for item in value:
                if item not in allowed:
                    raise GovernedSchemaError(f"{path} contains item outside closed vocabulary")
        if "ordered_const" in node and value != node["ordered_const"]:
            raise GovernedSchemaError(f"{path} violates normative array order/content")
        for index, item in enumerate(value):
            _validate_document_node(item, node["items"], f"{path}[{index}]")
        return

    if "const" in node and value != node["const"]:
        raise GovernedSchemaError(f"{path} const mismatch")
    if "enum" in node and value not in node["enum"]:
        raise GovernedSchemaError(f"{path} outside closed enum")
    if kind == "string" and "pattern" in node:
        if re.fullmatch(node["pattern"], value) is None:
            raise GovernedSchemaError(f"{path} pattern mismatch")
    if kind == "integer":
        if "minimum" in node and value < node["minimum"]:
            raise GovernedSchemaError(f"{path} below minimum")
        if "maximum" in node and value > node["maximum"]:
            raise GovernedSchemaError(f"{path} above maximum")


def parse_schema_json_strict(raw: str | bytes) -> dict[str, Any]:
    schema = parse_json_strict(raw)
    return validate_schema_definition(schema)


def _validate_document(document: object, validated_schema: dict[str, Any]) -> Any:
    _validate_document_node(document, validated_schema["root"], "$")
    return document


def validate_governed_json(
    raw_document: str | bytes,
    raw_schema: str | bytes,
) -> Any:
    try:
        validated_schema = parse_schema_json_strict(raw_schema)
        document = parse_json_strict(raw_document)
        return _validate_document(document, validated_schema)
    except GovernedSchemaError:
        raise
    except RecursionError as exc:
        raise GovernedSchemaError(
            "governed document validation exceeded recursion safety boundary"
        ) from exc
~~~~
