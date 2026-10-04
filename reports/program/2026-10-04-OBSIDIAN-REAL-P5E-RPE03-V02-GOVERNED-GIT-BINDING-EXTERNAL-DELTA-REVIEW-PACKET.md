# RPE-03 V0.2 — GOVERNED GIT EXECUTABLE BINDING — EXTERNAL DELTA REVIEW PACKET

Date: 2026-10-04

Candidate:
RPE-03 — GOVERNED GIT EXECUTABLE BINDING TARGETED AMENDMENT V0.2

Status:
QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW

Qualification HEAD before packet:
20367f1a7bc083e6ce2afa37c1d239900285eef1

RPE-03 V0.1 adoption commit:
546ce03b8c56a48eb54aaf163e02a9be0e028ce6

RPE-03 V0.1 classifier blob:
145b3112fd9309cc34d95a62c091cb6a6bc3bb11

V0.2 classifier blob:
65aec74ae089f51786f85a9742ea0a7ac2fdbe38

Qualification blob:
29df931941a4467180b014536b249ab2e8f39ebf

Qualification report blob:
4243e152116c92e7577c8dde54a0d4b1ad960439

Governed Git:
C:\Program Files\Git\cmd\git.exe
SHA-256 = 81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5
Observed version = git version 2.54.0.windows.1
Minimum qualified version = 2.54.0

Evidence:
- targeted V0.2: 8/8 PASS
- mutation tests: 4/4 PASS
- RPE-04 compatibility harness: 1/1 PASS
- complete RPE-03 regression: 51/51 PASS
- Windows implicit executable-search falsification: OBSERVED

Scope:
- V0.1 is immutable historical evidence.
- V0.2 changes only governed executable binding.
- RPE-04 is NOT rebound yet.
- RPE-04 BF-1 is NOT closed until V0.2 is human-adopted and RPE-04 is rebound.
- NF-2 and NF-3 remain open.
- RPE-05, RPE-06, REAL P5-E remain CLOSED.

## Required reviewer output

VERDICT = PASS | PASS_WITH_NON_BLOCKING_NOTES | FAIL

### BLOCKING_FINDINGS
### NON_BLOCKING_FINDINGS
### ACTUALLY_EXECUTED_BINARY_BINDING_CHECK
### WINDOWS_SEARCH_PATH_FALSIFICATION_CHECK
### ABSOLUTE_PATH_USAGE_CHECK
### SHA256_BINDING_CHECK
### VERSION_BINDING_CHECK
### NO_CALLER_AUTHORITY_LAUNDERING_CHECK
### UNCHANGED_ANCESTRY_SEMANTICS_CHECK
### MUTATION_DISCRIMINATION_CHECK
### RPE04_CALL_SITE_COMPATIBILITY_CHECK
### CLAIM_SCOPE_CHECK
### RPE03_V02_ADOPTION_READINESS
### RECOMMENDED_NEXT_ACTION

Key questions:
1. Is the executable whose path/hash/version are verified exactly the executable supplied to every classifier Git subprocess?
2. Can a caller select any alternate executable and still obtain a positive transition?
3. Does the Windows falsification prove implicit "git" resolution can differ while V0.2 remains bound to the absolute path?
4. Are path, SHA-256, observed version, and minimum version all fail-closed?
5. Are INITIAL/SAME/FAST_FORWARD/NON_FAST_FORWARD/UNKNOWN semantics unchanged from V0.1?
6. Does any test or implementation accidentally broaden RPE-03 authority?
7. Is the claim limited to the directly executed Git binary, without claiming the downstream Git-for-Windows helper chain?
8. Is RPE-04 correctly left blocked until separate human adoption and rebind?

This review creates no authority.

## HISTORICAL FROZEN RED TEST

PATH AT RED HEAD: tests/obsidian_projection/test_rpe03_governed_git_executable_binding_v0_2.py

~~~python
from __future__ import annotations

import importlib.util
import inspect
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py"
GIT = r"C:\Program Files\Git\cmd\git.exe"
EXPECTED_SHA256 = "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5"
EXPECTED_VERSION = "git version 2.54.0.windows.1"


def load_module(name: str):
    if not MODULE.exists():
        raise AssertionError(f"required V0.2 implementation missing: {MODULE}")
    spec = importlib.util.spec_from_file_location(name, MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def safe_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_LAZY_FETCH": "1",
    })
    return env


def git(repo: pathlib.Path, *args: str):
    cp = subprocess.run(
        [GIT, *args],
        cwd=str(repo),
        env=safe_env(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if cp.returncode != 0:
        raise AssertionError(cp.stderr)
    return cp.stdout.strip()


def make_repo():
    td = tempfile.TemporaryDirectory(prefix="rpe03-v02-")
    repo = pathlib.Path(td.name) / "repo"
    subprocess.run([GIT, "init", str(repo)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    git(repo, "config", "user.name", "RPE03 V02")
    git(repo, "config", "user.email", "rpe03-v02@example.invalid")
    (repo / "f.txt").write_text("A\n", encoding="utf-8")
    git(repo, "add", "f.txt")
    git(repo, "commit", "-m", "A")
    a = git(repo, "rev-parse", "HEAD")
    (repo / "f.txt").write_text("A\nB\n", encoding="utf-8")
    git(repo, "add", "f.txt")
    git(repo, "commit", "-m", "B")
    b = git(repo, "rev-parse", "HEAD")
    return td, repo, a, b


class TestRPE03GovernedGitExecutableBindingV02(unittest.TestCase):
    def test_public_interface_requires_governed_git_executable(self):
        m = load_module("rpe03_v02_sig")
        self.assertEqual(
            list(inspect.signature(m.classify_transition).parameters),
            ["repo_path", "previous_observed_head", "new_exact_observed_head", "governed_git_executable"],
        )

    def test_governed_absolute_executable_is_used(self):
        m = load_module("rpe03_v02_abs")
        seen = []
        original = subprocess.run

        def wrapped(cmd, *args, **kwargs):
            if isinstance(cmd, list) and cmd:
                seen.append(cmd[0])
            return original(cmd, *args, **kwargs)

        td, repo, a, b = make_repo()
        try:
            with mock.patch.object(m.subprocess, "run", side_effect=wrapped):
                result = m.classify_transition(repo, a, b, GIT)
            self.assertEqual(result, "FAST_FORWARD")
            self.assertTrue(seen)
            self.assertTrue(all(x == GIT for x in seen))
        finally:
            td.cleanup()

    def test_wrong_supplied_path_fails_closed(self):
        m = load_module("rpe03_v02_wrong_path")
        td, repo, a, b = make_repo()
        try:
            self.assertEqual(m.classify_transition(repo, a, b, r"C:\Windows\System32\cmd.exe"), "UNKNOWN")
        finally:
            td.cleanup()

    def test_wrong_sha_fails_closed(self):
        m = load_module("rpe03_v02_wrong_sha")
        td, repo, a, b = make_repo()
        try:
            with mock.patch.object(m, "_sha256_file", return_value="0" * 64):
                self.assertEqual(m.classify_transition(repo, a, b, GIT), "UNKNOWN")
        finally:
            td.cleanup()

    def test_version_below_minimum_fails_closed(self):
        m = load_module("rpe03_v02_old_version")
        td, repo, a, b = make_repo()
        try:
            with mock.patch.object(m, "_git_version", return_value="git version 2.53.0.windows.1"):
                self.assertEqual(m.classify_transition(repo, a, b, GIT), "UNKNOWN")
        finally:
            td.cleanup()

    def test_version_and_sha_constants_match_preregistered_identity(self):
        m = load_module("rpe03_v02_constants")
        self.assertEqual(m._GOVERNED_GIT_PATH, GIT)
        self.assertEqual(m._GOVERNED_GIT_SHA256, EXPECTED_SHA256)
        self.assertEqual(m._GOVERNED_GIT_VERSION, EXPECTED_VERSION)
        self.assertEqual(m._MIN_GIT_VERSION, (2, 54, 0))

    def test_transition_semantics_initial_same_ff_nonff_unknown(self):
        m = load_module("rpe03_v02_semantics")
        td, repo, a, b = make_repo()
        try:
            self.assertEqual(m.classify_transition(repo, None, a, GIT), "INITIAL")
            self.assertEqual(m.classify_transition(repo, a, a, GIT), "SAME")
            self.assertEqual(m.classify_transition(repo, a, b, GIT), "FAST_FORWARD")
            self.assertEqual(m.classify_transition(repo, b, a, GIT), "NON_FAST_FORWARD")
            self.assertEqual(m.classify_transition(repo, "f" * 40, b, GIT), "UNKNOWN")
        finally:
            td.cleanup()

    @unittest.skipUnless(os.name == "nt", "Windows executable-search falsification")
    def test_windows_implicit_search_can_select_wrong_git_but_v02_ignores_it(self):
        m = load_module("rpe03_v02_windows_search")
        td, repo, a, b = make_repo()
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory(prefix="rpe03-v02-fakegit-") as fake_dir:
            fake = pathlib.Path(fake_dir) / "git.exe"
            shutil.copy2(sys.executable, fake)
            try:
                os.chdir(fake_dir)
                cp = subprocess.run(
                    ["git", "--version"],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertIn("Python", cp.stdout + cp.stderr)
                self.assertEqual(m.classify_transition(repo, a, b, GIT), "FAST_FORWARD")
            finally:
                os.chdir(old_cwd)
                td.cleanup()


if __name__ == "__main__":
    unittest.main()

~~~

## RPE04 EXTERNAL REVIEW PROVENANCE

PATH: reports/program/2026-10-04-OBSIDIAN-REAL-P5E-RPE04-EXTERNAL-REVIEW-RETURN.md

~~~text
# RPE-04 — EXTERNAL ADVERSARIAL REVIEW RETURN

Date: 2026-10-04

Source: external Claude review returned by the human principal.

## Verdict

VERDICT = FAIL

RPE-04 tests were not independently executed by the reviewer because the package is Windows-bound. The reviewer replayed the exact Git command shape under Git 2.43/Linux, executed the physical-domain verifier extracted from the package, and tested the RPE-02 handoff of adapter failure events.

## Blocking finding

BF-1 — The Git executable whose identity is verified is not proven to be the Git executable actually used by RPE-03.

Observed code relationship:
- RPE-04 verifies C:\Program Files\Git\cmd\git.exe.
- RPE-03 V0.1 invokes the implicit executable token "git".
- On Windows, CreateProcess executable search can select a different git.exe before PATH.
- Therefore the binary producing FAST_FORWARD / NON_FAST_FORWARD is not bound to the verified binary.

Reviewer status: strong inference, not executed under Windows.

Required correction:
RPE-03 must execute an absolute governed Git executable path and tests must verify the actually launched binary.

## Non-blocking findings accepted for adjudication

NF-2 — Annotated-tag dereference can turn contained commit content into OBSERVED_REMOTE_TIP.
Correction: read exact ref without ^{commit}, then require exact object type == commit.

NF-3 — Physical containment covers objects paths but not the full authority-bearing bare repository domain. A redirected refs path can write outside the domain.
Correction: extend containment or create a fresh controlled domain and recursively reject indirections.

NF-4 — RPE-02 timing handoff is valid only for success paths; failure-event mapping is not yet a valid RPE-02 observation.

NF-5 — The hashed Git executable may be a launcher rather than the full executable chain.

NF-6 — Runtime binding has a small TOCTOU/import limitation; raw SHA-256 is environment/line-ending bound.

NF-7 — Pre-fetch checks occur before attempt_started_at_ns and therefore contribute to future RPE-05 scheduling delay.

NF-8 — Source identity checks are valid only for the local bare-remote qualification and do not transpose directly to GitHub.

NF-9 — Some qualification provenance uses abbreviated commit SHAs; full-SHA hygiene should be restored.

NF-10 — Mutation proof is indirect but acceptable with the main suite.

## Review conclusion

RPE04_ADOPTION_READINESS = NOT_READY

Recommended next action:
1. Targeted RPE-03 amendment binding the actually executed Git binary.
2. Then rebind RPE-04 and close BF-1, NF-2 and NF-3.
3. Carry NF-4 and NF-7 to RPE-05.
4. Use a Windows falsification test for BF-1 in the delta review.

This review creates no authority.

RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

~~~

## RPE04 HUMAN ADJUDICATION

PATH: GOVERNANCE/RPE-04-EXTERNAL-REVIEW-HUMAN-ADJUDICATION-2026-10-04.md

~~~text
# RPE-04 — EXTERNAL REVIEW HUMAN ADJUDICATION

Date: 2026-10-04

EXTERNAL_RPE04_REVIEW = VALID_EXTERNAL_EVIDENCE

VERDICT = FAIL

BF-1 = ACCEPTED_AS_BLOCKING

RPE-04 = NOT_READY_FOR_HUMAN_ADOPTION
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

Adjudication of notes:

NF-2 = ACCEPTED / MUST_CLOSE_BEFORE_RPE04_ADOPTION
NF-3 = ACCEPTED / MUST_CLOSE_BEFORE_RPE04_ADOPTION
NF-4 = ACCEPTED / CARRIED_TO_RPE-05
NF-5 = ACCEPTED_AS_ENVIRONMENT_BOUND_NOTE / NO_BROADER_EXECUTABLE_CHAIN_CLAIM_WITHOUT_NEW_EVIDENCE
NF-6 = ACCEPTED_AS_RUNTIME_BINDING_LIMITATION / HARDEN_IF_REQUIRED_BY_TARGETED_DELTA
NF-7 = ACCEPTED / CARRIED_TO_RPE-05
NF-8 = ACCEPTED / LOCAL_ONLY_LIMIT / CARRIED_TO_RPE-06_PRODUCTION_REMOTE_DESIGN
NF-9 = ACCEPTED / FULL_SHA_HYGIENE_MUST_BE_CORRECTED
NF-10 = ACCEPTED_AS_NON_BLOCKING

Authorized next stage:
RPE-03 — GOVERNED GIT EXECUTABLE BINDING TARGETED AMENDMENT V0.2

RPE-04 remains open and blocked pending adopted RPE-03 V0.2.

No RPE-04 functional correction is authorized in this subphase except a minimal compatibility harness demonstrating a future V0.2 call-site.

RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

~~~

## V0.2 PREREGISTRATION

PATH: tools/obsidian_projection/rpe03_governed_git_executable_binding_amendment_v0_2.json

~~~json
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE03_GOVERNED_GIT_EXECUTABLE_BINDING_AMENDMENT_V0_2",
  "status": "PREREGISTERED_BEFORE_RED",
  "date": "2026-10-04",
  "base": {
    "rpe03_v01_adoption_commit": "546ce03b8c56a48eb54aaf163e02a9be0e028ce6",
    "rpe03_v01_adoption_blob": "3a5933a59ad68e342595721e30ee71909d075a3f",
    "rpe03_v01_classifier_blob": "145b3112fd9309cc34d95a62c091cb6a6bc3bb11",
    "rpe01_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887",
    "rpe04_external_review_blob": "fa34c6cd69d19ec4e1913b10b2b5237b9d007220",
    "rpe04_human_adjudication_blob": "77656b362e24adc412df3040ae5221da99d49a7e",
    "blocker_provenance_head": "d596fa136e3b4ed21a1ade341e34f800dfd4a540"
  },
  "authority": {
    "stage": "RPE-03-V0.2-TARGETED-AMENDMENT",
    "implementation_authorized": true,
    "rpe03_v01_history_rewrite_authorized": false,
    "rpe04_functional_rebind_authorized": false,
    "rpe05_authorized": false,
    "rpe06_authorized": false,
    "real_p5e_authorized": false,
    "network_authorized": false,
    "real_p5d4_state_mutation_authorized": false,
    "vault_or_current_mutation_authorized": false
  },
  "governed_config": {
    "authorized_entrypoint": "validate_governed_json(raw_document, raw_schema)",
    "private_guard_functions_forbidden": true,
    "runtime_preregistration_path": "tools/obsidian_projection/rpe03_governed_git_executable_binding_amendment_v0_2.json",
    "runtime_schema_path": "tools/obsidian_projection/rpe03_governed_git_executable_binding_amendment_v0_2_schema_v0_1.json"
  },
  "executable_binding": {
    "absolute_git_executable_path": "C:\\Program Files\\Git\\cmd\\git.exe",
    "git_executable_sha256": "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5",
    "observed_git_version": "git version 2.54.0.windows.1",
    "minimum_qualified_git_version": "2.54.0",
    "exact_path_required": true,
    "exact_sha256_required": true,
    "observed_version_required": true,
    "minimum_version_required": true,
    "implicit_git_token_forbidden": true,
    "actually_executed_binary_must_equal_verified_binary": true
  },
  "public_interface": {
    "function": "classify_transition",
    "positional_parameters": [
      "repo_path",
      "previous_observed_head",
      "new_exact_observed_head",
      "governed_git_executable"
    ],
    "caller_supplied_executable_is_authority": false,
    "supplied_path_must_equal_preregistered_path": true,
    "invalid_or_unverified_executable_result": "UNKNOWN"
  },
  "semantic_immutability": {
    "outputs": [
      "INITIAL",
      "SAME",
      "FAST_FORWARD",
      "NON_FAST_FORWARD",
      "UNKNOWN"
    ],
    "missing_object": "UNKNOWN",
    "non_commit": "UNKNOWN",
    "invalid_domain": "UNKNOWN",
    "shallow_graft_alternate": "UNKNOWN",
    "unexpected_merge_base_exit": "UNKNOWN",
    "timeout_or_corruption": "UNKNOWN",
    "no_other_functional_extension_authorized": true
  },
  "windows_falsification": {
    "required": true,
    "implicit_search_wrong_binary_selection_must_be_demonstrated": true,
    "governed_absolute_path_must_ignore_fake_git": true,
    "fake_git_must_not_execute_in_v02": true,
    "safe_controlled_simulation_allowed": true
  },
  "mandatory_red_cases": [
    "implicit executable search can select wrong binary",
    "governed absolute executable must be used",
    "wrong supplied executable path fails closed",
    "wrong executable SHA fails closed",
    "version below qualified minimum fails closed",
    "RPE-03 transition semantics remain unchanged",
    "caller cannot create executable authority",
    "actual subprocess executable equals governed absolute path"
  ],
  "qualification_required": [
    "TARGETED_GREEN",
    "RPE03_DEDICATED_REGRESSION",
    "RPE03_MUTATION_TESTS",
    "RPE04_CALL_SITE_COMPATIBILITY_TEST",
    "PROTECTED_PREDECESSOR_DIFF_CHECK"
  ],
  "stop": "EXTERNAL_DELTA_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
}

~~~

## V0.2 PREREGISTRATION SCHEMA

PATH: tools/obsidian_projection/rpe03_governed_git_executable_binding_amendment_v0_2_schema_v0_1.json

~~~json
{
  "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
  "artifact_role": "RPE03_GOVERNED_GIT_EXECUTABLE_BINDING_AMENDMENT_V0_2",
  "root": {
    "kind": "object",
    "fields": {
      "schema": {
        "kind": "string",
        "const": "ATDS_OBSIDIAN_REAL_P5E_RPE03_GOVERNED_GIT_EXECUTABLE_BINDING_AMENDMENT_V0_2"
      },
      "status": {
        "kind": "string",
        "const": "PREREGISTERED_BEFORE_RED"
      },
      "date": {
        "kind": "string",
        "const": "2026-10-04"
      },
      "base": {
        "kind": "object",
        "fields": {
          "rpe03_v01_adoption_commit": {
            "kind": "string",
            "const": "546ce03b8c56a48eb54aaf163e02a9be0e028ce6"
          },
          "rpe03_v01_adoption_blob": {
            "kind": "string",
            "const": "3a5933a59ad68e342595721e30ee71909d075a3f"
          },
          "rpe03_v01_classifier_blob": {
            "kind": "string",
            "const": "145b3112fd9309cc34d95a62c091cb6a6bc3bb11"
          },
          "rpe01_guard_blob": {
            "kind": "string",
            "const": "26f977961d72a062199d71ffd628d5a5cc047887"
          },
          "rpe04_external_review_blob": {
            "kind": "string",
            "const": "fa34c6cd69d19ec4e1913b10b2b5237b9d007220"
          },
          "rpe04_human_adjudication_blob": {
            "kind": "string",
            "const": "77656b362e24adc412df3040ae5221da99d49a7e"
          },
          "blocker_provenance_head": {
            "kind": "string",
            "const": "d596fa136e3b4ed21a1ade341e34f800dfd4a540"
          }
        }
      },
      "authority": {
        "kind": "object",
        "fields": {
          "stage": {
            "kind": "string",
            "const": "RPE-03-V0.2-TARGETED-AMENDMENT"
          },
          "implementation_authorized": {
            "kind": "boolean",
            "const": true
          },
          "rpe03_v01_history_rewrite_authorized": {
            "kind": "boolean",
            "const": false
          },
          "rpe04_functional_rebind_authorized": {
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
          "real_p5e_authorized": {
            "kind": "boolean",
            "const": false
          },
          "network_authorized": {
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
          "runtime_preregistration_path": {
            "kind": "string",
            "const": "tools/obsidian_projection/rpe03_governed_git_executable_binding_amendment_v0_2.json"
          },
          "runtime_schema_path": {
            "kind": "string",
            "const": "tools/obsidian_projection/rpe03_governed_git_executable_binding_amendment_v0_2_schema_v0_1.json"
          }
        }
      },
      "executable_binding": {
        "kind": "object",
        "fields": {
          "absolute_git_executable_path": {
            "kind": "string",
            "const": "C:\\Program Files\\Git\\cmd\\git.exe"
          },
          "git_executable_sha256": {
            "kind": "string",
            "const": "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5"
          },
          "observed_git_version": {
            "kind": "string",
            "const": "git version 2.54.0.windows.1"
          },
          "minimum_qualified_git_version": {
            "kind": "string",
            "const": "2.54.0"
          },
          "exact_path_required": {
            "kind": "boolean",
            "const": true
          },
          "exact_sha256_required": {
            "kind": "boolean",
            "const": true
          },
          "observed_version_required": {
            "kind": "boolean",
            "const": true
          },
          "minimum_version_required": {
            "kind": "boolean",
            "const": true
          },
          "implicit_git_token_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "actually_executed_binary_must_equal_verified_binary": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "public_interface": {
        "kind": "object",
        "fields": {
          "function": {
            "kind": "string",
            "const": "classify_transition"
          },
          "positional_parameters": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 4,
            "max_items": 4,
            "unique": true,
            "ordered_const": [
              "repo_path",
              "previous_observed_head",
              "new_exact_observed_head",
              "governed_git_executable"
            ],
            "allowed_values": [
              "repo_path",
              "previous_observed_head",
              "new_exact_observed_head",
              "governed_git_executable"
            ]
          },
          "caller_supplied_executable_is_authority": {
            "kind": "boolean",
            "const": false
          },
          "supplied_path_must_equal_preregistered_path": {
            "kind": "boolean",
            "const": true
          },
          "invalid_or_unverified_executable_result": {
            "kind": "string",
            "const": "UNKNOWN"
          }
        }
      },
      "semantic_immutability": {
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
          "missing_object": {
            "kind": "string",
            "const": "UNKNOWN"
          },
          "non_commit": {
            "kind": "string",
            "const": "UNKNOWN"
          },
          "invalid_domain": {
            "kind": "string",
            "const": "UNKNOWN"
          },
          "shallow_graft_alternate": {
            "kind": "string",
            "const": "UNKNOWN"
          },
          "unexpected_merge_base_exit": {
            "kind": "string",
            "const": "UNKNOWN"
          },
          "timeout_or_corruption": {
            "kind": "string",
            "const": "UNKNOWN"
          },
          "no_other_functional_extension_authorized": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "windows_falsification": {
        "kind": "object",
        "fields": {
          "required": {
            "kind": "boolean",
            "const": true
          },
          "implicit_search_wrong_binary_selection_must_be_demonstrated": {
            "kind": "boolean",
            "const": true
          },
          "governed_absolute_path_must_ignore_fake_git": {
            "kind": "boolean",
            "const": true
          },
          "fake_git_must_not_execute_in_v02": {
            "kind": "boolean",
            "const": true
          },
          "safe_controlled_simulation_allowed": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "mandatory_red_cases": {
        "kind": "array",
        "items": {
          "kind": "string"
        },
        "min_items": 8,
        "max_items": 8,
        "unique": true,
        "ordered_const": [
          "implicit executable search can select wrong binary",
          "governed absolute executable must be used",
          "wrong supplied executable path fails closed",
          "wrong executable SHA fails closed",
          "version below qualified minimum fails closed",
          "RPE-03 transition semantics remain unchanged",
          "caller cannot create executable authority",
          "actual subprocess executable equals governed absolute path"
        ],
        "allowed_values": [
          "implicit executable search can select wrong binary",
          "governed absolute executable must be used",
          "wrong supplied executable path fails closed",
          "wrong executable SHA fails closed",
          "version below qualified minimum fails closed",
          "RPE-03 transition semantics remain unchanged",
          "caller cannot create executable authority",
          "actual subprocess executable equals governed absolute path"
        ]
      },
      "qualification_required": {
        "kind": "array",
        "items": {
          "kind": "string"
        },
        "min_items": 5,
        "max_items": 5,
        "unique": true,
        "ordered_const": [
          "TARGETED_GREEN",
          "RPE03_DEDICATED_REGRESSION",
          "RPE03_MUTATION_TESTS",
          "RPE04_CALL_SITE_COMPATIBILITY_TEST",
          "PROTECTED_PREDECESSOR_DIFF_CHECK"
        ],
        "allowed_values": [
          "TARGETED_GREEN",
          "RPE03_DEDICATED_REGRESSION",
          "RPE03_MUTATION_TESTS",
          "RPE04_CALL_SITE_COMPATIBILITY_TEST",
          "PROTECTED_PREDECESSOR_DIFF_CHECK"
        ]
      },
      "stop": {
        "kind": "string",
        "const": "EXTERNAL_DELTA_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
      }
    }
  }
}

~~~

## HISTORICAL RED REPORT

PATH: reports/program/2026-10-04-OBSIDIAN-REAL-P5E-RPE03-V02-GOVERNED-GIT-BINDING-RED.md

~~~text
# RPE-03 V0.2 — GOVERNED GIT EXECUTABLE BINDING — TARGETED RED

Date: 2026-10-04

Status: RED CONFIRMED / TEST-FIRST

Preregistration HEAD:
6de09282b4a97371d662f8871b3e34d2bb7ee9f0

Targeted RED test blob:
3a3947c6b75038644f84900d8c01a6ce91a360e1

Observed result:
- 8 tests executed
- 8 failures
- reason: rpe03_ancestry_classifier_v0_2.py does not exist
- exit = 1

Covered requirements:
- explicit governed executable parameter;
- absolute executable use;
- wrong path fail-closed;
- wrong SHA fail-closed;
- version below minimum fail-closed;
- identity constants;
- unchanged transition vocabulary/semantics;
- Windows implicit executable-search falsification.

RPE-03 V0.1 remains unchanged.
RPE-04 remains blocked pending adopted RPE-03 V0.2.
RPE-05, RPE-06 and REAL P5-E remain CLOSED.

~~~

## WINDOWS HARNESS CORRECTION

PATH: reports/program/2026-10-04-OBSIDIAN-REAL-P5E-RPE03-V02-WINDOWS-FALSIFICATION-HARNESS-CORRECTION.md

~~~text
# RPE-03 V0.2 — WINDOWS FALSIFICATION HARNESS CORRECTION — INTERNAL ADJUDICATION

Date: 2026-10-04

The frozen targeted RED test attempted to create a fake git.exe by copying sys.executable.

On this Windows host, Python resolves through WindowsApps and shutil.copy2(sys.executable, ...) fails with WinError 1920 before the executable-search falsification can run.

This is a test-fixture defect, not an implementation finding.

Authorized correction under the existing V0.2 authorization:
- replace the fake executable source only;
- use an accessible inert Windows executable copied as git.exe;
- preserve the same executable-search falsification;
- preserve the same expected security verdict;
- make no implementation change to satisfy the harness.

The corrected test must still prove:
1. implicit subprocess execution of "git" can select the fake executable from the process current directory;
2. RPE-03 V0.2 uses the governed absolute Git path and therefore ignores that fake executable.

~~~

## FINAL V0.2 CLASSIFIER

PATH: tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py

~~~python
"""RPE-03 V0.2: fail-closed local Git ancestry classifier with governed executable binding."""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
from pathlib import Path
from typing import Final


_SHA40_RE: Final = re.compile(r"[0-9a-f]{40}\Z")
_TIMEOUT_SECONDS: Final = 5

_GOVERNED_GIT_PATH: Final = r"C:\Program Files\Git\cmd\git.exe"
_GOVERNED_GIT_SHA256: Final = "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5"
_GOVERNED_GIT_VERSION: Final = "git version 2.54.0.windows.1"
_MIN_GIT_VERSION: Final = (2, 54, 0)

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


def _same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(str(left)) == os.path.normcase(str(right))


def _sha256_file(path: Path) -> str | None:
    try:
        h = hashlib.sha256()
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def _git_version(executable: str) -> str | None:
    try:
        cp = subprocess.run(
            [executable, "--version"],
            env=_safe_git_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
    except (subprocess.TimeoutExpired, OSError, ValueError):
        return None
    if cp.returncode != 0:
        return None
    return cp.stdout.strip()


def _parse_git_version(text: str | None) -> tuple[int, int, int] | None:
    if type(text) is not str:
        return None
    m = re.fullmatch(r"git version (\d+)\.(\d+)\.(\d+)(?:\..*)?", text)
    if m is None:
        return None
    return tuple(int(x) for x in m.groups())


def _verify_governed_git_executable(governed_git_executable) -> bool:
    if type(governed_git_executable) is not str:
        return False
    try:
        supplied = Path(governed_git_executable).resolve(strict=True)
        expected = Path(_GOVERNED_GIT_PATH).resolve(strict=True)
    except (OSError, RuntimeError, ValueError):
        return False
    if not supplied.is_file() or not _same_path(supplied, expected):
        return False
    if _sha256_file(supplied) != _GOVERNED_GIT_SHA256:
        return False
    version = _git_version(str(supplied))
    if version != _GOVERNED_GIT_VERSION:
        return False
    parsed = _parse_git_version(version)
    if parsed is None or parsed < _MIN_GIT_VERSION:
        return False
    return True


def _run_git(
    repo_path: Path,
    governed_git_executable: str,
    *args: str,
) -> subprocess.CompletedProcess[str] | None:
    cmd = [governed_git_executable, "-c", "core.commitGraph=false", *args]
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


def _verified_domain(
    repo_path: Path,
    governed_git_executable: str,
) -> tuple[Path, Path] | None:
    try:
        repo = repo_path.resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    if not repo.is_dir():
        return None

    dot_git = repo / ".git"
    if dot_git.is_file():
        return None

    bare_text = _stdout_ok(
        _run_git(repo, governed_git_executable, "rev-parse", "--is-bare-repository")
    )
    git_dir_text = _stdout_ok(
        _run_git(repo, governed_git_executable, "rev-parse", "--absolute-git-dir")
    )
    common_dir_text = _stdout_ok(
        _run_git(
            repo,
            governed_git_executable,
            "rev-parse",
            "--path-format=absolute",
            "--git-common-dir",
        )
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
        top_text = _stdout_ok(
            _run_git(repo, governed_git_executable, "rev-parse", "--show-toplevel")
        )
        if not top_text:
            return None
        top = _canonical_path(top_text, repo)
        if not _same_path(top, repo):
            return None
        if not dot_git.is_dir():
            return None
        if not _same_path(git_dir, dot_git.resolve(strict=False)):
            return None

    shallow = _stdout_ok(
        _run_git(repo, governed_git_executable, "rev-parse", "--is-shallow-repository")
    )
    if shallow is None or shallow.lower() != "false":
        return None
    if (common_dir / "shallow").exists():
        return None
    if (common_dir / "info" / "grafts").exists():
        return None
    if (common_dir / "objects" / "info" / "alternates").exists():
        return None

    return repo, common_dir


def _valid_commit(repo: Path, sha: object, governed_git_executable: str) -> bool:
    if type(sha) is not str or _SHA40_RE.fullmatch(sha) is None:
        return False
    cp = _run_git(repo, governed_git_executable, "cat-file", "-t", sha)
    return cp is not None and cp.returncode == 0 and cp.stdout.strip() == "commit"


def classify_transition(
    repo_path,
    previous_observed_head,
    new_exact_observed_head,
    governed_git_executable,
):
    """Return INITIAL, SAME, FAST_FORWARD, NON_FAST_FORWARD, or UNKNOWN."""

    if not _verify_governed_git_executable(governed_git_executable):
        return "UNKNOWN"

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

    domain = _verified_domain(repo_candidate, governed_git_executable)
    if domain is None:
        return "UNKNOWN"
    repo, _common_dir = domain

    if not _valid_commit(repo, new_exact_observed_head, governed_git_executable):
        return "UNKNOWN"

    if previous_observed_head is None:
        return "INITIAL"

    if not _valid_commit(repo, previous_observed_head, governed_git_executable):
        return "UNKNOWN"

    if previous_observed_head == new_exact_observed_head:
        return "SAME"

    cp = _run_git(
        repo,
        governed_git_executable,
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

~~~

## FINAL TARGETED TEST

PATH: tests/obsidian_projection/test_rpe03_governed_git_executable_binding_v0_2.py

~~~python
from __future__ import annotations

import importlib.util
import inspect
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py"
GIT = r"C:\Program Files\Git\cmd\git.exe"
EXPECTED_SHA256 = "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5"
EXPECTED_VERSION = "git version 2.54.0.windows.1"


def load_module(name: str):
    if not MODULE.exists():
        raise AssertionError(f"required V0.2 implementation missing: {MODULE}")
    spec = importlib.util.spec_from_file_location(name, MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def safe_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_LAZY_FETCH": "1",
    })
    return env


def git(repo: pathlib.Path, *args: str):
    cp = subprocess.run(
        [GIT, *args],
        cwd=str(repo),
        env=safe_env(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if cp.returncode != 0:
        raise AssertionError(cp.stderr)
    return cp.stdout.strip()


def make_repo():
    td = tempfile.TemporaryDirectory(prefix="rpe03-v02-")
    repo = pathlib.Path(td.name) / "repo"
    subprocess.run([GIT, "init", str(repo)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    git(repo, "config", "user.name", "RPE03 V02")
    git(repo, "config", "user.email", "rpe03-v02@example.invalid")
    (repo / "f.txt").write_text("A\n", encoding="utf-8")
    git(repo, "add", "f.txt")
    git(repo, "commit", "-m", "A")
    a = git(repo, "rev-parse", "HEAD")
    (repo / "f.txt").write_text("A\nB\n", encoding="utf-8")
    git(repo, "add", "f.txt")
    git(repo, "commit", "-m", "B")
    b = git(repo, "rev-parse", "HEAD")
    return td, repo, a, b


class TestRPE03GovernedGitExecutableBindingV02(unittest.TestCase):
    def test_public_interface_requires_governed_git_executable(self):
        m = load_module("rpe03_v02_sig")
        self.assertEqual(
            list(inspect.signature(m.classify_transition).parameters),
            ["repo_path", "previous_observed_head", "new_exact_observed_head", "governed_git_executable"],
        )

    def test_governed_absolute_executable_is_used(self):
        m = load_module("rpe03_v02_abs")
        seen = []
        original = subprocess.run

        def wrapped(cmd, *args, **kwargs):
            if isinstance(cmd, list) and cmd:
                seen.append(cmd[0])
            return original(cmd, *args, **kwargs)

        td, repo, a, b = make_repo()
        try:
            with mock.patch.object(m.subprocess, "run", side_effect=wrapped):
                result = m.classify_transition(repo, a, b, GIT)
            self.assertEqual(result, "FAST_FORWARD")
            self.assertTrue(seen)
            self.assertTrue(all(x == GIT for x in seen))
        finally:
            td.cleanup()

    def test_wrong_supplied_path_fails_closed(self):
        m = load_module("rpe03_v02_wrong_path")
        td, repo, a, b = make_repo()
        try:
            self.assertEqual(m.classify_transition(repo, a, b, r"C:\Windows\System32\cmd.exe"), "UNKNOWN")
        finally:
            td.cleanup()

    def test_wrong_sha_fails_closed(self):
        m = load_module("rpe03_v02_wrong_sha")
        td, repo, a, b = make_repo()
        try:
            with mock.patch.object(m, "_sha256_file", return_value="0" * 64):
                self.assertEqual(m.classify_transition(repo, a, b, GIT), "UNKNOWN")
        finally:
            td.cleanup()

    def test_version_below_minimum_fails_closed(self):
        m = load_module("rpe03_v02_old_version")
        td, repo, a, b = make_repo()
        try:
            with mock.patch.object(m, "_git_version", return_value="git version 2.53.0.windows.1"):
                self.assertEqual(m.classify_transition(repo, a, b, GIT), "UNKNOWN")
        finally:
            td.cleanup()

    def test_version_and_sha_constants_match_preregistered_identity(self):
        m = load_module("rpe03_v02_constants")
        self.assertEqual(m._GOVERNED_GIT_PATH, GIT)
        self.assertEqual(m._GOVERNED_GIT_SHA256, EXPECTED_SHA256)
        self.assertEqual(m._GOVERNED_GIT_VERSION, EXPECTED_VERSION)
        self.assertEqual(m._MIN_GIT_VERSION, (2, 54, 0))

    def test_transition_semantics_initial_same_ff_nonff_unknown(self):
        m = load_module("rpe03_v02_semantics")
        td, repo, a, b = make_repo()
        try:
            self.assertEqual(m.classify_transition(repo, None, a, GIT), "INITIAL")
            self.assertEqual(m.classify_transition(repo, a, a, GIT), "SAME")
            self.assertEqual(m.classify_transition(repo, a, b, GIT), "FAST_FORWARD")
            self.assertEqual(m.classify_transition(repo, b, a, GIT), "NON_FAST_FORWARD")
            self.assertEqual(m.classify_transition(repo, "f" * 40, b, GIT), "UNKNOWN")
        finally:
            td.cleanup()

    @unittest.skipUnless(os.name == "nt", "Windows executable-search falsification")
    def test_windows_implicit_search_can_select_wrong_git_but_v02_ignores_it(self):
        m = load_module("rpe03_v02_windows_search")
        td, repo, a, b = make_repo()
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory(prefix="rpe03-v02-fakegit-") as fake_dir:
            fake = pathlib.Path(fake_dir) / "git.exe"
            source = pathlib.Path(os.environ.get("SystemRoot", r"C:\\Windows")) / "System32" / "where.exe"
            shutil.copy2(source, fake)
            try:
                os.chdir(fake_dir)
                cp = subprocess.run(
                    ["git", "--version"],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertNotEqual(cp.returncode, 0)
                self.assertNotIn("git version", (cp.stdout + cp.stderr).lower())
                self.assertEqual(m.classify_transition(repo, a, b, GIT), "FAST_FORWARD")
            finally:
                os.chdir(old_cwd)
                td.cleanup()


if __name__ == "__main__":
    unittest.main()

~~~

## MUTATION TEST

PATH: tests/obsidian_projection/test_rpe03_governed_git_executable_binding_mutation_v0_2.py

~~~python
from __future__ import annotations

import pathlib
import tempfile
import types
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py"
GIT = r"C:\Program Files\Git\cmd\git.exe"


def load_mutant(name: str, replacements=()):
    source = MODULE.read_text(encoding="utf-8")
    for old, new in replacements:
        if source.count(old) != 1:
            raise AssertionError(f"mutation anchor count != 1: {old!r}")
        source = source.replace(old, new, 1)
    m = types.ModuleType(name)
    m.__file__ = str(MODULE)
    exec(compile(source, str(MODULE), "exec"), m.__dict__)
    return m


class TestRPE03V02Mutation(unittest.TestCase):
    def test_path_binding_guard_is_required(self):
        base = load_mutant("rpe03_v02_base_path")
        mutant = load_mutant(
            "rpe03_v02_mut_path",
            ((
                "    if not supplied.is_file() or not _same_path(supplied, expected):\n        return False\n",
                "    if not supplied.is_file():\n        return False\n",
            ),),
        )
        with tempfile.TemporaryDirectory(prefix="rpe03-v02-copy-") as td:
            alt = pathlib.Path(td) / "git.exe"
            alt.write_bytes(pathlib.Path(GIT).read_bytes())
            with mock.patch.object(base, "_git_version", return_value=base._GOVERNED_GIT_VERSION),                  mock.patch.object(mutant, "_git_version", return_value=mutant._GOVERNED_GIT_VERSION):
                self.assertFalse(base._verify_governed_git_executable(str(alt)))
                self.assertTrue(mutant._verify_governed_git_executable(str(alt)))

    def test_sha_binding_guard_is_required(self):
        base = load_mutant("rpe03_v02_base_sha")
        mutant = load_mutant(
            "rpe03_v02_mut_sha",
            ((
                "    if _sha256_file(supplied) != _GOVERNED_GIT_SHA256:\n        return False\n",
                "    if False:\n        return False\n",
            ),),
        )
        with mock.patch.object(base, "_sha256_file", return_value="0" * 64),              mock.patch.object(mutant, "_sha256_file", return_value="0" * 64),              mock.patch.object(base, "_git_version", return_value=base._GOVERNED_GIT_VERSION),              mock.patch.object(mutant, "_git_version", return_value=mutant._GOVERNED_GIT_VERSION):
            self.assertFalse(base._verify_governed_git_executable(GIT))
            self.assertTrue(mutant._verify_governed_git_executable(GIT))

    def test_version_binding_guard_is_required(self):
        base = load_mutant("rpe03_v02_base_version")
        mutant = load_mutant(
            "rpe03_v02_mut_version",
            ((
                "    if version != _GOVERNED_GIT_VERSION:\n        return False\n    parsed = _parse_git_version(version)\n    if parsed is None or parsed < _MIN_GIT_VERSION:\n        return False\n",
                "    if False:\n        return False\n    parsed = _MIN_GIT_VERSION\n    if False:\n        return False\n",
            ),),
        )
        with mock.patch.object(base, "_git_version", return_value="git version 2.53.0.windows.1"),              mock.patch.object(mutant, "_git_version", return_value="git version 2.53.0.windows.1"):
            self.assertFalse(base._verify_governed_git_executable(GIT))
            self.assertTrue(mutant._verify_governed_git_executable(GIT))

    def test_run_git_must_use_governed_absolute_path(self):
        mutant = load_mutant(
            "rpe03_v02_mut_implicit",
            ((
                '    cmd = [governed_git_executable, "-c", "core.commitGraph=false", *args]\n',
                '    cmd = ["git", "-c", "core.commitGraph=false", *args]\n',
            ),),
        )
        seen = []
        def fake_run(cmd, **kwargs):
            seen.append(cmd)
            return types.SimpleNamespace(returncode=0, stdout="", stderr="")
        with mock.patch.object(mutant.subprocess, "run", side_effect=fake_run):
            mutant._run_git(pathlib.Path.cwd(), GIT, "rev-parse", "--is-bare-repository")
        self.assertEqual(seen[0][0], "git")
        self.assertNotEqual(seen[0][0], GIT)


if __name__ == "__main__":
    unittest.main()

~~~

## RPE04 CALL-SITE COMPATIBILITY HARNESS

PATH: tests/obsidian_projection/test_rpe04_call_site_compatibility_with_rpe03_v0_2.py

~~~python
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

~~~

## WINDOWS EXECUTABLE SEARCH FALSIFICATION

PATH: reports/program/2026-10-04-OBSIDIAN-REAL-P5E-RPE03-V02-WINDOWS-EXECUTABLE-SEARCH-FALSIFICATION.md

~~~text
# RPE-03 V0.2 — WINDOWS EXECUTABLE SEARCH FALSIFICATION EVIDENCE

Date: 2026-10-04

Environment:
- Windows host
- governed Git: C:\Program Files\Git\cmd\git.exe
- governed Git version: git version 2.54.0.windows.1

Controlled falsification:
- a temporary fake git.exe was created by copying C:\WINDOWS\System32\where.exe;
- the process current directory was changed to the temporary directory;
- an implicit subprocess invocation ["git", "--version"] was executed;
- in the same process context, the governed absolute Git path was executed directly.

Observed output:

FAKE_SOURCE = C:\WINDOWS\System32\where.exe
IMPLICIT_RC = 1
IMPLICIT_STDOUT = empty
IMPLICIT_STDERR = empty
ABSOLUTE_RC = 0
ABSOLUTE_STDOUT = git version 2.54.0.windows.1

Interpretation:
- the implicit token "git" did not execute the governed Git binary, because the governed binary returns rc=0 and the exact version string;
- the controlled fake executable won implicit Windows executable resolution from the process current directory;
- absolute execution of C:\Program Files\Git\cmd\git.exe remained bound to the governed binary in the same context.

The targeted V0.2 test additionally verifies that ancestry classification still returns the correct transition while the fake git.exe is present because V0.2 uses the absolute governed path.

This evidence closes the Windows-search falsification requirement for the V0.2 candidate only. It does not adopt V0.2.

~~~

## QUALIFICATION

PATH: tools/obsidian_projection/rpe03_governed_git_executable_binding_qualification_v0_2.json

~~~json
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE03_GOVERNED_GIT_EXECUTABLE_BINDING_QUALIFICATION_V0_2",
  "status": "QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW",
  "date": "2026-10-04",
  "branch": "feat/obsidian-projection-rpe03-governed-git-executable-binding-v0.2",
  "lineage": {
    "rpe03_v01_human_adoption_commit": "546ce03b8c56a48eb54aaf163e02a9be0e028ce6",
    "blocker_provenance_head": "d596fa136e3b4ed21a1ade341e34f800dfd4a540",
    "preregistration_head": "6de09282b4a97371d662f8871b3e34d2bb7ee9f0",
    "targeted_red_head": "aaf045644051a6002b908a330f8fcdfe494a9dde",
    "implementation_head": "8dfda75a89181034a3c352f06d7a76cefbb56a54",
    "windows_falsification_evidence_head": "4b61fa1477d63885ca74938316ad722fbc4f52b9"
  },
  "exact_identities": {
    "rpe03_v01_adoption_blob": "3a5933a59ad68e342595721e30ee71909d075a3f",
    "rpe03_v01_classifier_blob": "145b3112fd9309cc34d95a62c091cb6a6bc3bb11",
    "rpe04_external_review_blob": "fa34c6cd69d19ec4e1913b10b2b5237b9d007220",
    "rpe04_human_adjudication_blob": "77656b362e24adc412df3040ae5221da99d49a7e",
    "preregistration_blob": "c173ec092cec571f7c0ad8229892800fa9ca3634",
    "preregistration_schema_blob": "e0d2ac35ea4a2a0f85a4093c4fbeb7ba36e2779b",
    "historical_red_test_blob": "3a3947c6b75038644f84900d8c01a6ce91a360e1",
    "historical_red_report_blob": "da34d645de7abd0d22d9a8d17cf82928ce149b21",
    "windows_harness_correction_blob": "c5ee2713d78055bbaa4f98774318581cd2a769c9",
    "final_classifier_v02_blob": "65aec74ae089f51786f85a9742ea0a7ac2fdbe38",
    "final_targeted_test_blob": "8daeabec8f189a88c6bb37a4941bd217bc3318e1",
    "mutation_test_blob": "0e36cdc59b62fa9ee473f88604a6a8d8eaca0298",
    "rpe04_compatibility_test_blob": "631931f334e7b8d54ff91d58dbc916b15ae04151",
    "windows_falsification_evidence_blob": "5ec59d27c7113fb02bff41e1759ac022e5a688d3",
    "rpe01_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887"
  },
  "governed_git": {
    "absolute_path": "C:\\Program Files\\Git\\cmd\\git.exe",
    "sha256": "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5",
    "observed_version": "git version 2.54.0.windows.1",
    "minimum_qualified_version": "2.54.0",
    "actually_executed_classifier_binary_is_absolute_governed_path": true,
    "implicit_git_token_removed": true,
    "broader_git_for_windows_helper_chain_qualified": false
  },
  "evidence": {
    "targeted_green": "8/8 PASS",
    "targeted_mutation_tests": "4/4 PASS",
    "rpe04_call_site_compatibility": "1/1 PASS",
    "combined_mutation_and_compatibility": "5/5 PASS",
    "complete_rpe03_regression": "51/51 PASS",
    "windows_implicit_search_falsification": "OBSERVED",
    "preregistration_rpe01_guard_validation": "PASS",
    "rpe03_v01_classifier_unchanged": true,
    "rpe01_guard_unchanged": true
  },
  "windows_falsification": {
    "fake_executable_source": "C:\\WINDOWS\\System32\\where.exe",
    "fake_name": "git.exe",
    "placement": "PROCESS_CURRENT_DIRECTORY",
    "implicit_git_result": "FAKE_EXECUTABLE_SELECTED / RC=1 / NO_GIT_VERSION_OUTPUT",
    "governed_absolute_git_result": "RC=0 / git version 2.54.0.windows.1",
    "v02_result": "CORRECT_TRANSITION_WITH_FAKE_PRESENT"
  },
  "qualified_claims": {
    "exact_governed_path_required": true,
    "exact_sha256_required": true,
    "observed_version_required": true,
    "minimum_version_required": true,
    "caller_cannot_select_alternate_executable": true,
    "subprocess_git_commands_use_governed_absolute_path": true,
    "ancestry_semantics_unchanged_from_v01": true,
    "no_network_inside_classifier": true
  },
  "claim_boundary": {
    "rpe03_v02_human_adopted": false,
    "rpe04_rebound_to_v02": false,
    "rpe04_bf1_closed": false,
    "nf2_closed": false,
    "nf3_closed": false,
    "rpe05_opened": false,
    "rpe06_opened": false,
    "real_p5e_opened": false
  },
  "next_gate": "EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADOPTION",
  "stop": true
}

~~~

## QUALIFICATION SCHEMA

PATH: tools/obsidian_projection/rpe03_governed_git_executable_binding_qualification_v0_2_schema_v0_1.json

~~~json
{
  "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
  "artifact_role": "RPE03_GOVERNED_GIT_EXECUTABLE_BINDING_QUALIFICATION_V0_2",
  "root": {
    "kind": "object",
    "fields": {
      "schema": {
        "kind": "string",
        "const": "ATDS_OBSIDIAN_REAL_P5E_RPE03_GOVERNED_GIT_EXECUTABLE_BINDING_QUALIFICATION_V0_2"
      },
      "status": {
        "kind": "string",
        "const": "QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW"
      },
      "date": {
        "kind": "string",
        "const": "2026-10-04"
      },
      "branch": {
        "kind": "string",
        "const": "feat/obsidian-projection-rpe03-governed-git-executable-binding-v0.2"
      },
      "lineage": {
        "kind": "object",
        "fields": {
          "rpe03_v01_human_adoption_commit": {
            "kind": "string",
            "const": "546ce03b8c56a48eb54aaf163e02a9be0e028ce6"
          },
          "blocker_provenance_head": {
            "kind": "string",
            "const": "d596fa136e3b4ed21a1ade341e34f800dfd4a540"
          },
          "preregistration_head": {
            "kind": "string",
            "const": "6de09282b4a97371d662f8871b3e34d2bb7ee9f0"
          },
          "targeted_red_head": {
            "kind": "string",
            "const": "aaf045644051a6002b908a330f8fcdfe494a9dde"
          },
          "implementation_head": {
            "kind": "string",
            "const": "8dfda75a89181034a3c352f06d7a76cefbb56a54"
          },
          "windows_falsification_evidence_head": {
            "kind": "string",
            "const": "4b61fa1477d63885ca74938316ad722fbc4f52b9"
          }
        }
      },
      "exact_identities": {
        "kind": "object",
        "fields": {
          "rpe03_v01_adoption_blob": {
            "kind": "string",
            "const": "3a5933a59ad68e342595721e30ee71909d075a3f"
          },
          "rpe03_v01_classifier_blob": {
            "kind": "string",
            "const": "145b3112fd9309cc34d95a62c091cb6a6bc3bb11"
          },
          "rpe04_external_review_blob": {
            "kind": "string",
            "const": "fa34c6cd69d19ec4e1913b10b2b5237b9d007220"
          },
          "rpe04_human_adjudication_blob": {
            "kind": "string",
            "const": "77656b362e24adc412df3040ae5221da99d49a7e"
          },
          "preregistration_blob": {
            "kind": "string",
            "const": "c173ec092cec571f7c0ad8229892800fa9ca3634"
          },
          "preregistration_schema_blob": {
            "kind": "string",
            "const": "e0d2ac35ea4a2a0f85a4093c4fbeb7ba36e2779b"
          },
          "historical_red_test_blob": {
            "kind": "string",
            "const": "3a3947c6b75038644f84900d8c01a6ce91a360e1"
          },
          "historical_red_report_blob": {
            "kind": "string",
            "const": "da34d645de7abd0d22d9a8d17cf82928ce149b21"
          },
          "windows_harness_correction_blob": {
            "kind": "string",
            "const": "c5ee2713d78055bbaa4f98774318581cd2a769c9"
          },
          "final_classifier_v02_blob": {
            "kind": "string",
            "const": "65aec74ae089f51786f85a9742ea0a7ac2fdbe38"
          },
          "final_targeted_test_blob": {
            "kind": "string",
            "const": "8daeabec8f189a88c6bb37a4941bd217bc3318e1"
          },
          "mutation_test_blob": {
            "kind": "string",
            "const": "0e36cdc59b62fa9ee473f88604a6a8d8eaca0298"
          },
          "rpe04_compatibility_test_blob": {
            "kind": "string",
            "const": "631931f334e7b8d54ff91d58dbc916b15ae04151"
          },
          "windows_falsification_evidence_blob": {
            "kind": "string",
            "const": "5ec59d27c7113fb02bff41e1759ac022e5a688d3"
          },
          "rpe01_guard_blob": {
            "kind": "string",
            "const": "26f977961d72a062199d71ffd628d5a5cc047887"
          }
        }
      },
      "governed_git": {
        "kind": "object",
        "fields": {
          "absolute_path": {
            "kind": "string",
            "const": "C:\\Program Files\\Git\\cmd\\git.exe"
          },
          "sha256": {
            "kind": "string",
            "const": "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5"
          },
          "observed_version": {
            "kind": "string",
            "const": "git version 2.54.0.windows.1"
          },
          "minimum_qualified_version": {
            "kind": "string",
            "const": "2.54.0"
          },
          "actually_executed_classifier_binary_is_absolute_governed_path": {
            "kind": "boolean",
            "const": true
          },
          "implicit_git_token_removed": {
            "kind": "boolean",
            "const": true
          },
          "broader_git_for_windows_helper_chain_qualified": {
            "kind": "boolean",
            "const": false
          }
        }
      },
      "evidence": {
        "kind": "object",
        "fields": {
          "targeted_green": {
            "kind": "string",
            "const": "8/8 PASS"
          },
          "targeted_mutation_tests": {
            "kind": "string",
            "const": "4/4 PASS"
          },
          "rpe04_call_site_compatibility": {
            "kind": "string",
            "const": "1/1 PASS"
          },
          "combined_mutation_and_compatibility": {
            "kind": "string",
            "const": "5/5 PASS"
          },
          "complete_rpe03_regression": {
            "kind": "string",
            "const": "51/51 PASS"
          },
          "windows_implicit_search_falsification": {
            "kind": "string",
            "const": "OBSERVED"
          },
          "preregistration_rpe01_guard_validation": {
            "kind": "string",
            "const": "PASS"
          },
          "rpe03_v01_classifier_unchanged": {
            "kind": "boolean",
            "const": true
          },
          "rpe01_guard_unchanged": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "windows_falsification": {
        "kind": "object",
        "fields": {
          "fake_executable_source": {
            "kind": "string",
            "const": "C:\\WINDOWS\\System32\\where.exe"
          },
          "fake_name": {
            "kind": "string",
            "const": "git.exe"
          },
          "placement": {
            "kind": "string",
            "const": "PROCESS_CURRENT_DIRECTORY"
          },
          "implicit_git_result": {
            "kind": "string",
            "const": "FAKE_EXECUTABLE_SELECTED / RC=1 / NO_GIT_VERSION_OUTPUT"
          },
          "governed_absolute_git_result": {
            "kind": "string",
            "const": "RC=0 / git version 2.54.0.windows.1"
          },
          "v02_result": {
            "kind": "string",
            "const": "CORRECT_TRANSITION_WITH_FAKE_PRESENT"
          }
        }
      },
      "qualified_claims": {
        "kind": "object",
        "fields": {
          "exact_governed_path_required": {
            "kind": "boolean",
            "const": true
          },
          "exact_sha256_required": {
            "kind": "boolean",
            "const": true
          },
          "observed_version_required": {
            "kind": "boolean",
            "const": true
          },
          "minimum_version_required": {
            "kind": "boolean",
            "const": true
          },
          "caller_cannot_select_alternate_executable": {
            "kind": "boolean",
            "const": true
          },
          "subprocess_git_commands_use_governed_absolute_path": {
            "kind": "boolean",
            "const": true
          },
          "ancestry_semantics_unchanged_from_v01": {
            "kind": "boolean",
            "const": true
          },
          "no_network_inside_classifier": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "claim_boundary": {
        "kind": "object",
        "fields": {
          "rpe03_v02_human_adopted": {
            "kind": "boolean",
            "const": false
          },
          "rpe04_rebound_to_v02": {
            "kind": "boolean",
            "const": false
          },
          "rpe04_bf1_closed": {
            "kind": "boolean",
            "const": false
          },
          "nf2_closed": {
            "kind": "boolean",
            "const": false
          },
          "nf3_closed": {
            "kind": "boolean",
            "const": false
          },
          "rpe05_opened": {
            "kind": "boolean",
            "const": false
          },
          "rpe06_opened": {
            "kind": "boolean",
            "const": false
          },
          "real_p5e_opened": {
            "kind": "boolean",
            "const": false
          }
        }
      },
      "next_gate": {
        "kind": "string",
        "const": "EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADOPTION"
      },
      "stop": {
        "kind": "boolean",
        "const": true
      }
    }
  }
}

~~~

## QUALIFICATION REPORT

PATH: reports/program/2026-10-04-OBSIDIAN-REAL-P5E-RPE03-V02-GOVERNED-GIT-BINDING-QUALIFICATION.md

~~~text
# RPE-03 V0.2 — GOVERNED GIT EXECUTABLE BINDING — QUALIFICATION

Date: 2026-10-04

## Result

RPE-03 V0.2 = QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW

This is not human adoption.

## Blocker addressed

BF-1 from the RPE-04 external review required:

VERIFIED GIT EXECUTABLE
=
ACTUALLY EXECUTED ANCESTRY CLASSIFIER GIT EXECUTABLE

V0.1 remains immutable and historically adopted.

V0.2 adds only explicit governed Git executable binding.

## Governed Git identity

Absolute path:
C:\Program Files\Git\cmd\git.exe

SHA-256:
81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5

Observed version:
git version 2.54.0.windows.1

Minimum qualified version:
2.54.0

The classifier rejects:
- any other supplied path;
- SHA mismatch;
- observed-version mismatch;
- version below minimum.

Every Git command issued by V0.2 uses the supplied path only after it has matched the preregistered governed identity.

## Windows falsification

A controlled fake git.exe was placed in the process current directory.

Implicit ["git", "--version"]:
- selected the fake executable;
- return code = 1;
- did not return the governed Git version.

Absolute governed Git:
- return code = 0;
- returned git version 2.54.0.windows.1.

The V0.2 test confirms correct ancestry classification with the fake executable present because the absolute governed path is used.

## Evidence

Targeted V0.2:
8/8 PASS

Targeted mutation tests:
4/4 PASS

RPE-04 call-site compatibility harness:
1/1 PASS

Complete RPE-03 V0.1 + V0.2 regression:
51/51 PASS

RPE-03 V0.1 classifier remains:
145b3112fd9309cc34d95a62c091cb6a6bc3bb11

RPE-01 guard remains:
26f977961d72a062199d71ffd628d5a5cc047887

## Semantic immutability

The transition vocabulary remains:

INITIAL
SAME
FAST_FORWARD
NON_FAST_FORWARD
UNKNOWN

Missing object, non-commit, invalid domain, shallow/graft/alternate domain, unexpected merge-base exit, timeout and corruption remain fail-closed to UNKNOWN.

## Claim boundary

This qualification binds the executable directly launched by the classifier.

It does not claim qualification of the entire downstream Git-for-Windows helper executable chain.

It does not rebind RPE-04 yet.

It does not close RPE-04 BF-1 until V0.2 is externally reviewed and human-adopted, then RPE-04 is rebound.

NF-2 and NF-3 remain open in RPE-04.

RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

Next gate:
EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADOPTION

~~~

## ADOPTED RPE03 V0.1 CLASSIFIER

PATH: tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py

~~~python
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

~~~

## RPE03 V0.1 HUMAN ADOPTION

PATH: GOVERNANCE/RPE-03-NB5-ANCESTRY-CLASSIFIER-HUMAN-ADJUDICATION-2026-10-03.md

~~~text
# RPE-03 — NB5 ANCESTRY CLASSIFIER V0.1 — HUMAN ADJUDICATION

Date: 2026-10-03

## Human decision

The human authority adopts:

`RPE-03 — NB5 ANCESTRY CLASSIFIER V0.1`

in its final qualified state after:
- initial qualification;
- independent external review;
- external-review targeted closure;
- NB-6 bare-root test-only closure;
- explicit scope adjudication of NB-1′.

The adopted normative state is:

`RPE03_ANCESTRY_CLASSIFIER = QUALIFIED_AND_HUMAN_ADOPTED`

After persistence and verification of this record:

`RPE-03 = CLOSED`

This adoption does not open RPE-04.

## Binding pre-adoption identity

```text
FINAL PRE-ADOPTION HEAD
= 827e7cfadfddc779c915a8efc6d4b33cc784f810

RPE-03 CLASSIFIER
= 145b3112fd9309cc34d95a62c091cb6a6bc3bb11

NB-6 TEST
= b7724499e0fe15b069689afb2f222ed2f4223eeb

FINAL PRE-ADOPTION QUALIFICATION
= 883aa61e90d50c8a2c44f495d985295d16874302

FINAL PRE-ADOPTION QUALIFICATION REPORT
= 25b7e4957306c5f4473c597de2a2a28834c83bec

FINAL EXTERNAL REVIEW RETURN
= 980e0d65da684fac88f16422f4843983c9ecbc8d

FINAL INTERNAL ADJUDICATION
= 8228fae41f7c81598e871858c9cdf2ef4ca74d48
```

Branch at adoption:

`feat/obsidian-projection-rpe03-ancestry-classifier-v0.1`

Pre-adoption local and remote HEAD were equal.

Pre-adoption worktree was clean.

## Final evidence accepted

```text
RPE-03 DEDICATED SURFACE
= 38 / 38 PASS

P5-E + RPE-01 + RPE-03 TARGETED REGRESSION
= 151 / 151 PASS

P5-E CONTRACT DIFF
= 0

P5-E SYNTHETIC MODEL DIFF
= 0

P5-D4 RUNTIME DIFF
= 0
```

## Adopted classification vocabulary

```text
INITIAL
SAME
FAST_FORWARD
NON_FAST_FORWARD
UNKNOWN
```

Adopted properties include:

```text
NETWORK INSIDE CLASSIFIER
= FORBIDDEN

MISSING / INVALID / NON-COMMIT OBJECT
= UNKNOWN

TIMEOUT / CORRUPTION / UNVERIFIED DOMAIN
= UNKNOWN

SAME
= EXPLICITLY DETECTED BEFORE ANCESTRY TEST

MERGE-BASE EXIT 0
= FAST_FORWARD

MERGE-BASE EXIT 1
= NON_FAST_FORWARD

OTHER MERGE-BASE EXIT
= UNKNOWN
```

No caller-supplied transition class may override the classifier result.

## Adopted supplied-path confinement

```text
RPE03_SUPPLIED_PATH_CONFINEMENT
= QUALIFIED
```

Qualified supplied-domain kinds:

```text
MAIN_WORKTREE_ROOT
BARE_REPOSITORY_ROOT
```

according to the exact qualified rules.

## NB-6 — adopted closure

```text
EXACT BARE REPOSITORY ROOT
= ALLOWED

BARE REPOSITORY SUBDIRECTORY
= UNKNOWN

NB-6
= CLOSED
```

The final test-only closure did not modify the classifier implementation.

Classifier blob:
`145b3112fd9309cc34d95a62c091cb6a6bc3bb11`

NB-6 test blob:
`b7724499e0fe15b069689afb2f222ed2f4223eeb`

The targeted mutant removing the exact bare-root condition is killed.

## NB-1' — explicit adopted scope boundary

```text
RPE03_PHYSICAL_OBJECT_STORE_CONTAINMENT
= NOT_CLAIMED
```

Therefore:

```text
PATH IDENTITY
!=
PHYSICAL OBJECT-STORE CONTAINMENT
```

and:

```text
RPE-03 CLASSIFIED
!=
PROOF THAT OBJECTS ARE PHYSICALLY MATERIALIZED
INSIDE AN ISOLATED OBJECT-STORE DOMAIN
```

RPE-03 does not by itself qualify physical object-store containment against:
- SYMLINK;
- JUNCTION;
- REPARSE_POINT;
- equivalent filesystem redirection.

This boundary is intentional and does not reopen RPE-03.

## Mandatory RPE-04 preconditions carried by this adoption

RPE-04 may not consume RPE-03 without separately preregistering and qualifying:

```text
GIT EXECUTABLE IDENTITY
= EXPLICIT / GOVERNED

MINIMUM SUPPORTED GIT VERSION
= PREREGISTERED / VERIFIED

LOCAL REPOSITORY CONFIG
= CONTROLLED DOMAIN REQUIRED

include.path / includeIf
= MUST NOT INTRODUCE UNGOVERNED AUTHORITY OR PROVENANCE

FILESYSTEM OBJECT-DOMAIN INDIRECTION
= ABSENT OR EXPLICITLY GOVERNED AND QUALIFIED
```

The filesystem qualification must cover, when applicable:
- .git
- objects
- objects/pack
- objects/info
- bare repository equivalents.

RPE-04 must preserve:

```text
PATH IDENTITY
!=
PHYSICAL OBJECT-STORE CONTAINMENT
```

and may not infer:

```text
RPE-03 CLASSIFIED
-> OBJECTS PHYSICALLY MATERIALIZED IN ISOLATED DOMAIN
```

without independent qualification evidence.

## Protected predecessor integrity

This persistence step does not modify:
- the adopted P5-E contract;
- the adopted P5-E synthetic model;
- the P5-D4 runtime;
- RPE-01;
- RPE-02;
- any real P5-D4 control state;
- Vault or CURRENT;
- RPE-04 or later stages.

## Stage state after verified persistence

```text
RPE-03
= CLOSED
= QUALIFIED_AND_HUMAN_ADOPTED

RPE-04
= CLOSED

RPE-05
= CLOSED

RPE-06
= CLOSED

REAL P5-E
= CLOSED
```

RPE-02 state is unchanged by this RPE-03 adoption record.

This record does not open or authorize RPE-04.

## Explicitly not authorized

This adoption does not authorize:
- RPE-04 implementation or execution;
- RPE-05 implementation or execution;
- RPE-06 implementation or execution;
- real GitHub observation;
- real polling;
- remote fetch;
- sandbox creation;
- experimental repository/ref creation;
- experimental push;
- P5-D4 real-state mutation;
- Stage A;
- Stage B;
- promotion or publication;
- Vault mutation;
- CURRENT mutation;
- daemon registration;
- Scheduled Task registration;
- Windows Service registration;
- startup registration;
- P6;
- REAL P5-E.

```text
RPE-04 = CLOSED
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED
```

## Persistence authority

The only operations authorized by the human adoption statement are:
- persist this human-adoption record;
- commit it;
- push it;
- verify final local/remote repository consistency;
- STOP.

This record persists pre-existing human authority. It does not create or enlarge that authority.

No classifier, test, qualification, P5-E artifact, P5-D4 artifact, control state, Vault/CURRENT artifact, or future RPE artifact may be modified by this persistence step.

~~~

## RPE01 GOVERNED SCHEMA GUARD

PATH: tools/obsidian_projection/rpe01_governed_closed_schema.py

~~~python
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

~~~
