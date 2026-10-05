# RPE-03 V0.2 — BF-1 PRIME VERIFIED/EXECUTED EXECUTABLE IDENTITY — EXTERNAL DELTA REVIEW PACKET

Date: 2026-10-05

Candidate state:
QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW

Qualification HEAD before packet:
b2b1f913f7ef7447de3592eb1d3e6404451735e6

Prior V0.2 external-packet HEAD:
a6a10b2f4303afac01ddc5d6bca36a9b32d7913a

BF-1 PRIME adjudication HEAD:
96783f48cd1206432a46044c0e9ce35f040be602

BF-1 PRIME preregistration HEAD:
d91d7d373b631e887c087ef6558e507e2c7187f9

BF-1 PRIME RED HEAD:
4f2f8c7ef279f904db905670ffa0f94b6b106f55

BF-1 PRIME patch HEAD:
d973fe17a3ef38af67cbd9bff7dd90a440fcebe2

Final classifier blob:
5bbe455418fe1396ee5824379ad7450a1379cbba

Qualification blob:
688a2abcc2caa2edeed5e67f2d3c38b293bcc238

Qualification report blob:
168c76ef3e058b3a583a203518685a9a16bf652d

Governed direct Git executable:
C:\Program Files\Git\cmd\git.exe

SHA-256:
81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5

Observed version:
git version 2.54.0.windows.1

Minimum version:
2.54.0

Final evidence:
- historical BF-1 PRIME RED: 4/4 FAIL
- final BF-1 PRIME closure: 5/5 PASS
- BF-1 PRIME mutations: 3/3 PASS
- updated prior V0.2 mutations: 4/4 PASS
- complete RPE-03 surface: 59/59 PASS
- Windows control implicit search: rc=7, sentinel created
- final candidate with fake git.exe present: FAST_FORWARD, sentinel absent

Protected identities:
- RPE-03 V0.1 classifier = 145b3112fd9309cc34d95a62c091cb6a6bc3bb11
- RPE-01 guard = 26f977961d72a062199d71ffd628d5a5cc047887
- P5-E contract = 43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9
- P5-D4 runtime = 1825e53d195ba2a63b5b646a5b78eb77939b94b5

Claim boundary:
- direct classifier executable binding only;
- no claim for the full Git-for-Windows helper chain;
- privileged Program Files replacement TOCTOU remains outside current threat model;
- RPE-04 is not rebound;
- RPE-04 NF-2 and NF-3 remain open;
- RPE-05, RPE-06, REAL P5-E remain CLOSED.

## Required reviewer output

VERDICT = PASS | PASS_WITH_NON_BLOCKING_NOTES | FAIL

### BLOCKING_FINDINGS
### NON_BLOCKING_FINDINGS
### NON_ABSOLUTE_INPUT_REJECTION_CHECK
### VERIFIED_PATH_EQUALS_EXECUTED_PATH_CHECK
### RAW_CALLER_STRING_NOT_EXECUTED_CHECK
### SHA256_BINDING_CHECK
### VERSION_BINDING_CHECK
### WINDOWS_SENTINEL_FALSIFICATION_CHECK
### CALLER_AUTHORITY_LAUNDERING_CHECK
### UNCHANGED_ANCESTRY_SEMANTICS_CHECK
### MUTATION_DISCRIMINATION_CHECK
### FULL_SHA_HYGIENE_CHECK
### CLAIM_SCOPE_CHECK
### RPE03_V02_ADOPTION_READINESS
### RECOMMENDED_NEXT_ACTION

Key questions:
1. Are non-absolute values such as git, git.exe, .\git.exe and relative\git.exe rejected before a positive classification?
2. Does validation return a canonical absolute path and is that exact returned path the one used by every classifier Git subprocess?
3. Can the raw caller-supplied string reach subprocess execution after validation?
4. Do path, SHA-256, exact version and minimum version all fail closed?
5. Does the positive-sentinel Windows evidence prove that implicit search can execute a fake git.exe while the final candidate does not?
6. Can any caller select another executable and still obtain a positive transition?
7. Are ancestry semantics unchanged from the adopted V0.1?
8. Do the mutants meaningfully discriminate the raw-string, SHA and version protections?
9. Are all new normative commit identities full SHA values?
10. Is the claim correctly limited to the directly executed classifier executable?

This review creates no authority.
RPE-03 V0.2 human adoption remains pending.
RPE-04 remains blocked.
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

## PRE-BF1-PRIME V0.2 CLASSIFIER

SOURCE: a6a10b2f4303afac01ddc5d6bca36a9b32d7913a:tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py

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

## HISTORICAL FROZEN BF1 PRIME RED TEST

SOURCE: 4f2f8c7ef279f904db905670ffa0f94b6b106f55:tests/obsidian_projection/test_rpe03_v02_bf1_prime_executable_identity_closure_v0_1.py

~~~python
from __future__ import annotations

import importlib.util
import os
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py"
GIT = r"C:\Program Files\Git\cmd\git.exe"
GIT_DIR = pathlib.Path(GIT).parent


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, MODULE)
    m = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(m)
    return m


def make_repo():
    td = tempfile.TemporaryDirectory(prefix="rpe03-bf1p-")
    repo = pathlib.Path(td.name) / "repo"
    subprocess.run([GIT, "init", str(repo)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run([GIT, "-C", str(repo), "config", "user.name", "bf1p"], check=True)
    subprocess.run([GIT, "-C", str(repo), "config", "user.email", "bf1p@example.invalid"], check=True)
    (repo / "x").write_text("a", encoding="utf-8")
    subprocess.run([GIT, "-C", str(repo), "add", "x"], check=True)
    subprocess.run([GIT, "-C", str(repo), "commit", "-m", "a"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    a = subprocess.run([GIT, "-C", str(repo), "rev-parse", "HEAD"], check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
    (repo / "x").write_text("b", encoding="utf-8")
    subprocess.run([GIT, "-C", str(repo), "add", "x"], check=True)
    subprocess.run([GIT, "-C", str(repo), "commit", "-m", "b"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    b = subprocess.run([GIT, "-C", str(repo), "rev-parse", "HEAD"], check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
    return td, repo, a, b


class TestRPE03V02BF1PrimeExecutableIdentityClosure(unittest.TestCase):
    def test_bare_git_exe_is_rejected_even_when_cwd_resolves_to_governed_file(self):
        m = load_module("bf1p_bare")
        old = os.getcwd()
        try:
            os.chdir(GIT_DIR)
            self.assertFalse(m._verify_governed_git_executable("git.exe"))
        finally:
            os.chdir(old)

    def test_dot_relative_git_exe_is_rejected(self):
        m = load_module("bf1p_dot")
        old = os.getcwd()
        try:
            os.chdir(GIT_DIR)
            self.assertFalse(m._verify_governed_git_executable(r".\git.exe"))
        finally:
            os.chdir(old)

    def test_classify_with_bare_git_exe_fails_closed_before_positive_transition(self):
        m = load_module("bf1p_classify")
        td, repo, a, b = make_repo()
        old = os.getcwd()
        try:
            os.chdir(GIT_DIR)
            self.assertEqual(m.classify_transition(repo, a, b, "git.exe"), "UNKNOWN")
        finally:
            os.chdir(old)
            td.cleanup()

    def test_run_git_receives_only_verified_absolute_executable(self):
        m = load_module("bf1p_raw_execution")
        seen = []
        def fake_run(cmd, **kwargs):
            seen.append(cmd)
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
        with mock.patch.object(m.subprocess, "run", side_effect=fake_run):
            m._run_git(pathlib.Path.cwd(), "git.exe", "rev-parse", "--is-bare-repository")
        self.assertEqual(seen[0][0], GIT)
        self.assertTrue(pathlib.Path(seen[0][0]).is_absolute())


if __name__ == "__main__":
    unittest.main()

~~~

## BF1 PRIME EXTERNAL REVIEW RETURN

PATH: reports/program/2026-10-05-OBSIDIAN-REAL-P5E-RPE03-V02-BF1-PRIME-EXTERNAL-DELTA-REVIEW-RETURN.md

~~~text
# RPE-03 V0.2 — BF-1 PRIME EXTERNAL DELTA REVIEW RETURN

Date: 2026-10-05

## Verdict

VERDICT = FAIL

BF-1 PRIME = ACCEPTED AS BLOCKING

## Blocking finding

The V0.2 classifier verifies a resolved executable path but _run_git executes the raw caller-supplied string.

Therefore a relative or bare value such as git.exe can be resolved during verification to the governed executable while later being resolved by subprocess executable search to a different executable.

Observed Linux analogue supplied by the external reviewer:
- absolute governed path on a true rollback: NON_FAST_FORWARD;
- _verify_governed_git_executable("git.exe"): True;
- classify_transition(repo, B, A, "git.exe"): FAST_FORWARD.

This demonstrates that VERIFIED EXECUTABLE and ACTUALLY EXECUTED EXECUTABLE are not identical for non-absolute caller input.

## Required correction

The classifier must:
1. reject non-absolute supplied executable strings;
2. resolve the supplied absolute path strictly;
3. require equality with the governed canonical executable;
4. verify SHA-256;
5. verify exact version;
6. verify minimum version;
7. return the verified canonical absolute path;
8. execute only that verified canonical path in every Git subprocess.

The raw caller string must not be reused after validation.

## Non-blocking findings

NB-1 = TOCTOU note, non-blocking in current threat model.
NB-2 = exact-version plus minimum-version redundancy, accepted.
NB-3 = Windows falsification evidence should use a positive sentinel.
NB-4 = previous harness correction accepted.
NB-5 = V0.1 packet copy newline/provenance note accepted.

## Scope

RPE-03 V0.2 = NOT READY FOR HUMAN ADOPTION
RPE-04 = BLOCKED
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

This review creates no authority.

~~~

## BF1 PRIME HUMAN ADJUDICATION

PATH: GOVERNANCE/RPE-03-V02-BF1-PRIME-HUMAN-ADJUDICATION-2026-10-05.md

~~~text
# RPE-03 V0.2 — BF-1 PRIME HUMAN ADJUDICATION

Date: 2026-10-05

EXTERNAL_RPE03_V02_DELTA_REVIEW = VALID_EXTERNAL_EVIDENCE
VERDICT = FAIL
BF-1 PRIME = ACCEPTED_AS_BLOCKING

RPE-03 V0.2 = NOT_READY_FOR_HUMAN_ADOPTION
RPE-04 = OPEN / BLOCKED_PENDING_RPE03_V0.2
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

NB-1 = ACCEPTED_AS_NON_BLOCKING_TOCTOU_NOTE
NB-2 = ACCEPTED_AS_NON_BLOCKING_REDUNDANCY_NOTE
NB-3 = ACCEPTED / WINDOWS_FALSIFICATION_EVIDENCE_TO_BE_HARDENED_IN_THIS_PASS
NB-4 = ACCEPTED_AS_HARNESS_CORRECTION
NB-5 = ACCEPTED_AS_NON_BLOCKING_PROVENANCE_NOTE

Authorized closure:
RPE-03 V0.2 — BF-1 PRIME VERIFIED-EXECUTABLE / EXECUTED-EXECUTABLE IDENTITY CLOSURE V0.1

Normative property:

CALLER_SUPPLIED_EXECUTABLE_STRING
→ MUST BE ABSOLUTE
→ MUST RESOLVE TO GOVERNED EXECUTABLE
→ MUST MATCH GOVERNED SHA-256
→ MUST MATCH GOVERNED VERSION
→ MUST SATISFY MINIMUM VERSION
→ VERIFIED_CANONICAL_GIT_EXECUTABLE

ACTUALLY EXECUTED EXECUTABLE
= VERIFIED_CANONICAL_GIT_EXECUTABLE

Non-absolute values such as git, git.exe, .\git.exe and relative\git.exe must fail closed to UNKNOWN.

The raw caller string must not be used for any Git subprocess after verification.

An explicit Windows positive-sentinel falsification is required.

RPE-03 ancestry semantics remain immutable.
No RPE-04 functional rebind is authorized.
NF-2 and NF-3 remain open in RPE-04.
RPE-05, RPE-06 and REAL P5-E remain CLOSED.

STOP after targeted qualification, external delta review packet, commit/push, local=remote and clean-worktree verification.

~~~

## BF1 PRIME PREREGISTRATION

PATH: tools/obsidian_projection/rpe03_v02_bf1_prime_executable_identity_closure_v0_1.json

~~~json
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE03_V02_BF1_PRIME_EXECUTABLE_IDENTITY_CLOSURE_V0_1",
  "status": "PREREGISTERED_BEFORE_RED",
  "date": "2026-10-05",
  "base": {
    "rpe03_v02_packet_head": "a6a10b2f4303afac01ddc5d6bca36a9b32d7913a",
    "external_review_adjudication_head": "96783f48cd1206432a46044c0e9ce35f040be602",
    "rpe03_v02_classifier_blob": "65aec74ae089f51786f85a9742ea0a7ac2fdbe38",
    "rpe03_v01_classifier_blob": "145b3112fd9309cc34d95a62c091cb6a6bc3bb11",
    "rpe01_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887"
  },
  "governed_identity": {
    "absolute_git_path": "C:\\Program Files\\Git\\cmd\\git.exe",
    "sha256": "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5",
    "observed_version": "git version 2.54.0.windows.1",
    "minimum_version": "2.54.0"
  },
  "normative_flow": [
    "RAW_CALLER_STRING",
    "REQUIRE_ABSOLUTE",
    "STRICT_RESOLVE",
    "EXACT_CANONICAL_PATH_EQUALITY",
    "SHA256_VERIFY",
    "EXACT_VERSION_VERIFY",
    "MINIMUM_VERSION_VERIFY",
    "VERIFIED_CANONICAL_GIT_EXECUTABLE",
    "ALL_GIT_SUBPROCESSES_USE_VERIFIED_CANONICAL_GIT_EXECUTABLE"
  ],
  "rejection": {
    "non_absolute_values": [
      "git",
      "git.exe",
      ".\\git.exe",
      "relative\\git.exe"
    ],
    "result": "UNKNOWN",
    "raw_string_execution_after_verification_forbidden": true
  },
  "required_tests": [
    "bare git.exe rejected before classification",
    "relative dot git.exe rejected before classification",
    "relative nested git.exe rejected before classification",
    "verified canonical path is exactly subprocess argv zero",
    "raw caller string execution mutant is killed",
    "sha mismatch fails closed",
    "exact version mismatch fails closed",
    "minimum version failure fails closed",
    "Windows positive sentinel proves implicit search can execute fake git",
    "Windows final candidate leaves sentinel absent",
    "RPE03 V0.1 protected regression",
    "RPE03 V0.2 regression",
    "RPE04 compatibility harness"
  ],
  "threat_model": {
    "privileged_program_files_binary_replacement_between_verify_and_execute": "OUT_OF_SCOPE_NON_BLOCKING_TOCTOU_NOTE",
    "full_git_for_windows_helper_chain_qualified": false
  },
  "authority": {
    "rpe03_v02_human_adoption_authorized": false,
    "rpe04_functional_rebind_authorized": false,
    "rpe04_nf2_authorized": false,
    "rpe04_nf3_authorized": false,
    "rpe05_authorized": false,
    "rpe06_authorized": false,
    "real_p5e_authorized": false
  },
  "stop": "EXTERNAL_DELTA_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
}

~~~

## BF1 PRIME PREREGISTRATION SCHEMA

PATH: tools/obsidian_projection/rpe03_v02_bf1_prime_executable_identity_closure_v0_1_schema_v0_1.json

~~~json
{
  "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
  "artifact_role": "RPE03_V02_BF1_PRIME_EXECUTABLE_IDENTITY_CLOSURE",
  "root": {
    "kind": "object",
    "fields": {
      "schema": {
        "kind": "string",
        "const": "ATDS_OBSIDIAN_REAL_P5E_RPE03_V02_BF1_PRIME_EXECUTABLE_IDENTITY_CLOSURE_V0_1"
      },
      "status": {
        "kind": "string",
        "const": "PREREGISTERED_BEFORE_RED"
      },
      "date": {
        "kind": "string",
        "const": "2026-10-05"
      },
      "base": {
        "kind": "object",
        "fields": {
          "rpe03_v02_packet_head": {
            "kind": "string",
            "const": "a6a10b2f4303afac01ddc5d6bca36a9b32d7913a"
          },
          "external_review_adjudication_head": {
            "kind": "string",
            "const": "96783f48cd1206432a46044c0e9ce35f040be602"
          },
          "rpe03_v02_classifier_blob": {
            "kind": "string",
            "const": "65aec74ae089f51786f85a9742ea0a7ac2fdbe38"
          },
          "rpe03_v01_classifier_blob": {
            "kind": "string",
            "const": "145b3112fd9309cc34d95a62c091cb6a6bc3bb11"
          },
          "rpe01_guard_blob": {
            "kind": "string",
            "const": "26f977961d72a062199d71ffd628d5a5cc047887"
          }
        }
      },
      "governed_identity": {
        "kind": "object",
        "fields": {
          "absolute_git_path": {
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
          "minimum_version": {
            "kind": "string",
            "const": "2.54.0"
          }
        }
      },
      "normative_flow": {
        "kind": "array",
        "items": {
          "kind": "string"
        },
        "min_items": 9,
        "max_items": 9,
        "unique": true,
        "ordered_const": [
          "RAW_CALLER_STRING",
          "REQUIRE_ABSOLUTE",
          "STRICT_RESOLVE",
          "EXACT_CANONICAL_PATH_EQUALITY",
          "SHA256_VERIFY",
          "EXACT_VERSION_VERIFY",
          "MINIMUM_VERSION_VERIFY",
          "VERIFIED_CANONICAL_GIT_EXECUTABLE",
          "ALL_GIT_SUBPROCESSES_USE_VERIFIED_CANONICAL_GIT_EXECUTABLE"
        ],
        "allowed_values": [
          "RAW_CALLER_STRING",
          "REQUIRE_ABSOLUTE",
          "STRICT_RESOLVE",
          "EXACT_CANONICAL_PATH_EQUALITY",
          "SHA256_VERIFY",
          "EXACT_VERSION_VERIFY",
          "MINIMUM_VERSION_VERIFY",
          "VERIFIED_CANONICAL_GIT_EXECUTABLE",
          "ALL_GIT_SUBPROCESSES_USE_VERIFIED_CANONICAL_GIT_EXECUTABLE"
        ]
      },
      "rejection": {
        "kind": "object",
        "fields": {
          "non_absolute_values": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 4,
            "max_items": 4,
            "unique": true,
            "ordered_const": [
              "git",
              "git.exe",
              ".\\git.exe",
              "relative\\git.exe"
            ],
            "allowed_values": [
              "git",
              "git.exe",
              ".\\git.exe",
              "relative\\git.exe"
            ]
          },
          "result": {
            "kind": "string",
            "const": "UNKNOWN"
          },
          "raw_string_execution_after_verification_forbidden": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "required_tests": {
        "kind": "array",
        "items": {
          "kind": "string"
        },
        "min_items": 13,
        "max_items": 13,
        "unique": true,
        "ordered_const": [
          "bare git.exe rejected before classification",
          "relative dot git.exe rejected before classification",
          "relative nested git.exe rejected before classification",
          "verified canonical path is exactly subprocess argv zero",
          "raw caller string execution mutant is killed",
          "sha mismatch fails closed",
          "exact version mismatch fails closed",
          "minimum version failure fails closed",
          "Windows positive sentinel proves implicit search can execute fake git",
          "Windows final candidate leaves sentinel absent",
          "RPE03 V0.1 protected regression",
          "RPE03 V0.2 regression",
          "RPE04 compatibility harness"
        ],
        "allowed_values": [
          "bare git.exe rejected before classification",
          "relative dot git.exe rejected before classification",
          "relative nested git.exe rejected before classification",
          "verified canonical path is exactly subprocess argv zero",
          "raw caller string execution mutant is killed",
          "sha mismatch fails closed",
          "exact version mismatch fails closed",
          "minimum version failure fails closed",
          "Windows positive sentinel proves implicit search can execute fake git",
          "Windows final candidate leaves sentinel absent",
          "RPE03 V0.1 protected regression",
          "RPE03 V0.2 regression",
          "RPE04 compatibility harness"
        ]
      },
      "threat_model": {
        "kind": "object",
        "fields": {
          "privileged_program_files_binary_replacement_between_verify_and_execute": {
            "kind": "string",
            "const": "OUT_OF_SCOPE_NON_BLOCKING_TOCTOU_NOTE"
          },
          "full_git_for_windows_helper_chain_qualified": {
            "kind": "boolean",
            "const": false
          }
        }
      },
      "authority": {
        "kind": "object",
        "fields": {
          "rpe03_v02_human_adoption_authorized": {
            "kind": "boolean",
            "const": false
          },
          "rpe04_functional_rebind_authorized": {
            "kind": "boolean",
            "const": false
          },
          "rpe04_nf2_authorized": {
            "kind": "boolean",
            "const": false
          },
          "rpe04_nf3_authorized": {
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
          }
        }
      },
      "stop": {
        "kind": "string",
        "const": "EXTERNAL_DELTA_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
      }
    }
  }
}

~~~

## BF1 PRIME RED REPORT

PATH: reports/program/2026-10-05-OBSIDIAN-REAL-P5E-RPE03-V02-BF1-PRIME-RED.md

~~~text
# RPE-03 V0.2 — BF-1 PRIME EXECUTABLE IDENTITY CLOSURE — RED

Date: 2026-10-05

Status: RED CONFIRMED / TEST-FIRST

Preregistration HEAD:
d91d7d373b631e887c087ef6558e507e2c7187f9

Frozen RED test blob:
984249ee982d652678517707c3f683a8acd57d44

Observed result:
- 4 tests executed
- 4 failures
- exit = 1

Observed failures:
1. bare git.exe is accepted when cwd resolves it to the governed file;
2. .\\git.exe is accepted in the same condition;
3. classify_transition(repo, A, B, "git.exe") returns FAST_FORWARD instead of UNKNOWN;
4. _run_git receives argv[0] = git.exe instead of the governed absolute path.

This reproduces BF-1 PRIME against the current V0.2 candidate before correction.

No RPE-03 ancestry semantics were changed to produce this RED.
RPE-04 remains blocked.
RPE-05, RPE-06 and REAL P5-E remain CLOSED.

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


def _resolve_and_verify_governed_git_executable(
    governed_git_executable,
) -> str | None:
    if type(governed_git_executable) is not str:
        return None
    try:
        raw = Path(governed_git_executable)
    except (TypeError, ValueError):
        return None
    if not raw.is_absolute():
        return None
    try:
        supplied = raw.resolve(strict=True)
        expected = Path(_GOVERNED_GIT_PATH).resolve(strict=True)
    except (OSError, RuntimeError, ValueError):
        return None
    if not supplied.is_file() or not _same_path(supplied, expected):
        return None
    if _sha256_file(supplied) != _GOVERNED_GIT_SHA256:
        return None
    version = _git_version(str(supplied))
    if version != _GOVERNED_GIT_VERSION:
        return None
    parsed = _parse_git_version(version)
    if parsed is None or parsed < _MIN_GIT_VERSION:
        return None
    return str(supplied)


def _verify_governed_git_executable(governed_git_executable) -> bool:
    return _resolve_and_verify_governed_git_executable(governed_git_executable) is not None


def _run_git(
    repo_path: Path,
    governed_git_executable: str,
    *args: str,
) -> subprocess.CompletedProcess[str] | None:
    try:
        executable = Path(governed_git_executable)
    except (TypeError, ValueError):
        return None
    if not executable.is_absolute():
        return None
    try:
        resolved = executable.resolve(strict=True)
        expected = Path(_GOVERNED_GIT_PATH).resolve(strict=True)
    except (OSError, RuntimeError, ValueError):
        return None
    if not _same_path(resolved, expected):
        return None
    cmd = [str(resolved), "-c", "core.commitGraph=false", *args]
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

    verified_git_executable = _resolve_and_verify_governed_git_executable(
        governed_git_executable
    )
    if verified_git_executable is None:
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

    domain = _verified_domain(repo_candidate, verified_git_executable)
    if domain is None:
        return "UNKNOWN"
    repo, _common_dir = domain

    if not _valid_commit(repo, new_exact_observed_head, verified_git_executable):
        return "UNKNOWN"

    if previous_observed_head is None:
        return "INITIAL"

    if not _valid_commit(repo, previous_observed_head, verified_git_executable):
        return "UNKNOWN"

    if previous_observed_head == new_exact_observed_head:
        return "SAME"

    cp = _run_git(
        repo,
        verified_git_executable,
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

## FINAL BF1 PRIME CLOSURE TEST

PATH: tests/obsidian_projection/test_rpe03_v02_bf1_prime_final_closure_v0_1.py

~~~python
from __future__ import annotations

import importlib.util
import os
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py"
GIT = r"C:\Program Files\Git\cmd\git.exe"
GIT_DIR = pathlib.Path(GIT).parent


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, MODULE)
    m = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(m)
    return m


def make_repo():
    td = tempfile.TemporaryDirectory(prefix="rpe03-bf1p-final-")
    repo = pathlib.Path(td.name) / "repo"
    subprocess.run([GIT, "init", str(repo)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run([GIT, "-C", str(repo), "config", "user.name", "bf1p-final"], check=True)
    subprocess.run([GIT, "-C", str(repo), "config", "user.email", "bf1p-final@example.invalid"], check=True)
    (repo / "x").write_text("a", encoding="utf-8")
    subprocess.run([GIT, "-C", str(repo), "add", "x"], check=True)
    subprocess.run([GIT, "-C", str(repo), "commit", "-m", "a"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    a = subprocess.run([GIT, "-C", str(repo), "rev-parse", "HEAD"], check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
    (repo / "x").write_text("b", encoding="utf-8")
    subprocess.run([GIT, "-C", str(repo), "add", "x"], check=True)
    subprocess.run([GIT, "-C", str(repo), "commit", "-m", "b"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    b = subprocess.run([GIT, "-C", str(repo), "rev-parse", "HEAD"], check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
    return td, repo, a, b


def compile_sentinel_git(fake: pathlib.Path):
    source = (
        'using System; using System.IO; '
        'public class P { public static void Main(string[] args) { '
        'var p=Environment.GetEnvironmentVariable("RPE03_SENTINEL"); '
        'if(!String.IsNullOrEmpty(p)) File.WriteAllText(p,"FAKE_GIT_EXECUTED"); '
        'Environment.Exit(7); } }'
    )
    source_file = fake.with_suffix(".cs")
    source_file.write_text(source, encoding="utf-8")
    ps = (
        "$ErrorActionPreference='Stop'; "
        f"Add-Type -Path '{source_file}' -OutputAssembly '{fake}' "
        "-OutputType ConsoleApplication"
    )
    cp = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", ps],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if cp.returncode != 0 or not fake.is_file():
        raise AssertionError(cp.stderr)


class TestRPE03V02BF1PrimeFinalClosure(unittest.TestCase):
    def test_non_absolute_values_are_rejected(self):
        m = load_module("bf1p_final_relative")
        old = os.getcwd()
        try:
            os.chdir(GIT_DIR)
            for value in ("git", "git.exe", r".\git.exe", r"relative\git.exe"):
                self.assertIsNone(m._resolve_and_verify_governed_git_executable(value))
                self.assertFalse(m._verify_governed_git_executable(value))
        finally:
            os.chdir(old)

    def test_classify_with_bare_git_exe_is_unknown(self):
        m = load_module("bf1p_final_classify")
        td, repo, a, b = make_repo()
        old = os.getcwd()
        try:
            os.chdir(GIT_DIR)
            self.assertEqual(m.classify_transition(repo, a, b, "git.exe"), "UNKNOWN")
        finally:
            os.chdir(old)
            td.cleanup()

    def test_internal_run_git_rejects_raw_non_absolute_token_without_subprocess(self):
        m = load_module("bf1p_final_run")
        with mock.patch.object(m.subprocess, "run") as wrapped:
            self.assertIsNone(
                m._run_git(pathlib.Path.cwd(), "git.exe", "rev-parse", "--is-bare-repository")
            )
        wrapped.assert_not_called()

    def test_verified_path_is_exact_path_used_by_all_classifier_subprocesses(self):
        m = load_module("bf1p_final_exact")
        td, repo, a, b = make_repo()
        seen = []
        original = m.subprocess.run

        def wrapped(cmd, *args, **kwargs):
            if isinstance(cmd, list) and cmd:
                seen.append(cmd[0])
            return original(cmd, *args, **kwargs)

        try:
            with mock.patch.object(m.subprocess, "run", side_effect=wrapped):
                self.assertEqual(m.classify_transition(repo, a, b, GIT), "FAST_FORWARD")
            self.assertTrue(seen)
            governed = str(pathlib.Path(GIT).resolve(strict=True))
            self.assertTrue(all(x == governed for x in seen))
        finally:
            td.cleanup()

    @unittest.skipUnless(os.name == "nt", "Windows positive sentinel falsification")
    def test_windows_positive_sentinel_control_and_final_candidate(self):
        m = load_module("bf1p_final_sentinel")
        td, repo, a, b = make_repo()
        with tempfile.TemporaryDirectory(prefix="rpe03-bf1p-sentinel-") as fake_td:
            fake_dir = pathlib.Path(fake_td)
            fake = fake_dir / "git.exe"
            sentinel = fake_dir / "sentinel.txt"
            compile_sentinel_git(fake)

            old = os.getcwd()
            old_sentinel = os.environ.get("RPE03_SENTINEL")
            try:
                os.chdir(fake_dir)
                os.environ["RPE03_SENTINEL"] = str(sentinel)

                control = subprocess.run(
                    ["git", "--version"],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertEqual(control.returncode, 7)
                self.assertTrue(sentinel.is_file())
                self.assertEqual(sentinel.read_text(encoding="utf-8"), "FAKE_GIT_EXECUTED")

                sentinel.unlink()
                self.assertEqual(m.classify_transition(repo, a, b, GIT), "FAST_FORWARD")
                self.assertFalse(sentinel.exists())
            finally:
                os.chdir(old)
                if old_sentinel is None:
                    os.environ.pop("RPE03_SENTINEL", None)
                else:
                    os.environ["RPE03_SENTINEL"] = old_sentinel
                td.cleanup()


if __name__ == "__main__":
    unittest.main()

~~~

## BF1 PRIME MUTATION TEST

PATH: tests/obsidian_projection/test_rpe03_v02_bf1_prime_mutation_v0_1.py

~~~python
from __future__ import annotations

import os
import pathlib
import tempfile
import types
import unittest
from unittest import mock

from tests.obsidian_projection.test_rpe03_v02_bf1_prime_final_closure_v0_1 import (
    GIT,
    GIT_DIR,
    make_repo,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py"


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


class TestRPE03V02BF1PrimeMutation(unittest.TestCase):
    def test_composite_raw_string_execution_mutant_is_discriminated(self):
        base = load_mutant("bf1p_mut_base")
        mutant = load_mutant(
            "bf1p_mut_raw",
            (
                (
                    "    if not raw.is_absolute():\n        return None\n",
                    "    if False:\n        return None\n",
                ),
                (
                    "    return str(supplied)\n\n\ndef _verify_governed_git_executable",
                    "    return governed_git_executable\n\n\ndef _verify_governed_git_executable",
                ),
                (
                    "    try:\n        executable = Path(governed_git_executable)\n"
                    "    except (TypeError, ValueError):\n        return None\n"
                    "    if not executable.is_absolute():\n        return None\n"
                    "    try:\n        resolved = executable.resolve(strict=True)\n"
                    "        expected = Path(_GOVERNED_GIT_PATH).resolve(strict=True)\n"
                    "    except (OSError, RuntimeError, ValueError):\n        return None\n"
                    "    if not _same_path(resolved, expected):\n        return None\n"
                    '    cmd = [str(resolved), "-c", "core.commitGraph=false", *args]\n',
                    '    cmd = [governed_git_executable, "-c", "core.commitGraph=false", *args]\n',
                ),
            ),
        )
        td, repo, a, b = make_repo()
        old = os.getcwd()
        try:
            os.chdir(GIT_DIR)
            self.assertEqual(base.classify_transition(repo, a, b, "git.exe"), "UNKNOWN")
            self.assertEqual(mutant.classify_transition(repo, a, b, "git.exe"), "FAST_FORWARD")
        finally:
            os.chdir(old)
            td.cleanup()

    def test_sha_guard_mutant_is_discriminated(self):
        base = load_mutant("bf1p_mut_sha_base")
        mutant = load_mutant(
            "bf1p_mut_sha",
            (
                (
                    "    if _sha256_file(supplied) != _GOVERNED_GIT_SHA256:\n        return None\n",
                    "    if False:\n        return None\n",
                ),
            ),
        )
        with mock.patch.object(base, "_sha256_file", return_value="0" * 64), \
             mock.patch.object(mutant, "_sha256_file", return_value="0" * 64), \
             mock.patch.object(base, "_git_version", return_value=base._GOVERNED_GIT_VERSION), \
             mock.patch.object(mutant, "_git_version", return_value=mutant._GOVERNED_GIT_VERSION):
            self.assertIsNone(base._resolve_and_verify_governed_git_executable(GIT))
            self.assertEqual(
                mutant._resolve_and_verify_governed_git_executable(GIT),
                str(pathlib.Path(GIT).resolve(strict=True)),
            )

    def test_version_guard_mutant_is_discriminated(self):
        base = load_mutant("bf1p_mut_ver_base")
        mutant = load_mutant(
            "bf1p_mut_ver",
            (
                (
                    "    if version != _GOVERNED_GIT_VERSION:\n        return None\n"
                    "    parsed = _parse_git_version(version)\n"
                    "    if parsed is None or parsed < _MIN_GIT_VERSION:\n        return None\n",
                    "    if False:\n        return None\n"
                    "    parsed = _MIN_GIT_VERSION\n"
                    "    if False:\n        return None\n",
                ),
            ),
        )
        with mock.patch.object(base, "_git_version", return_value="git version 2.53.0.windows.1"), \
             mock.patch.object(mutant, "_git_version", return_value="git version 2.53.0.windows.1"):
            self.assertIsNone(base._resolve_and_verify_governed_git_executable(GIT))
            self.assertEqual(
                mutant._resolve_and_verify_governed_git_executable(GIT),
                str(pathlib.Path(GIT).resolve(strict=True)),
            )


if __name__ == "__main__":
    unittest.main()

~~~

## UPDATED PRIOR V0.2 MUTATION TEST

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
                "    if not supplied.is_file() or not _same_path(supplied, expected):\n        return None\n",
                "    if not supplied.is_file():\n        return None\n",
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
                "    if _sha256_file(supplied) != _GOVERNED_GIT_SHA256:\n        return None\n",
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
                "    if version != _GOVERNED_GIT_VERSION:\n        return None\n    parsed = _parse_git_version(version)\n    if parsed is None or parsed < _MIN_GIT_VERSION:\n        return None\n",
                "    if False:\n        return None\n    parsed = _MIN_GIT_VERSION\n    if False:\n        return None\n",
            ),),
        )
        with mock.patch.object(base, "_git_version", return_value="git version 2.53.0.windows.1"),              mock.patch.object(mutant, "_git_version", return_value="git version 2.53.0.windows.1"):
            self.assertFalse(base._verify_governed_git_executable(GIT))
            self.assertTrue(mutant._verify_governed_git_executable(GIT))

    def test_run_git_must_use_governed_absolute_path(self):
        mutant = load_mutant(
            "rpe03_v02_mut_implicit",
            ((
                '    cmd = [str(resolved), "-c", "core.commitGraph=false", *args]\n',
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

## RPE04 CALL-SITE COMPATIBILITY

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

## WINDOWS SENTINEL EVIDENCE

PATH: reports/program/2026-10-05-OBSIDIAN-REAL-P5E-RPE03-V02-BF1-PRIME-WINDOWS-SENTINEL-EVIDENCE.md

~~~text
# RPE-03 V0.2 — BF-1 PRIME WINDOWS POSITIVE-SENTINEL EVIDENCE

Date: 2026-10-05

A temporary fake git.exe was compiled inside a temporary directory. If executed, it writes a unique sentinel file and exits with code 7.

Observed control:

CONTROL_IMPLICIT_RC = 7
CONTROL_SENTINEL_CREATED = TRUE

The same temporary directory and fake executable remained present for the final candidate classification.

Observed final candidate:

FINAL_CLASSIFICATION = FAST_FORWARD
FINAL_SENTINEL_CREATED = FALSE

Interpretation:
- implicit Windows executable search executed the temporary fake git.exe in the control path;
- the final RPE-03 V0.2 candidate did not execute that fake executable;
- the classifier used the governed absolute Git executable and produced the expected FAST_FORWARD result;
- no write occurred in Program Files, the Python installation directory, or a system directory.

This evidence is specific to direct classifier executable binding. It does not qualify the downstream Git-for-Windows helper chain.

~~~

## HARNESS CORRECTIONS

PATH: reports/program/2026-10-05-OBSIDIAN-REAL-P5E-RPE03-V02-BF1-PRIME-HARNESS-CORRECTIONS.md

~~~text
# RPE-03 V0.2 — BF-1 PRIME TEST-HARNESS CORRECTIONS

Date: 2026-10-05

Two test-harness corrections occurred during the authorized BF-1 PRIME closure.

1. The first positive-sentinel helper embedded C# directly inside a PowerShell command string and failed because of quoting. The helper was corrected to write the C# source to a temporary .cs file and invoke Add-Type -Path. No implementation change was made for this failure and no expected security verdict changed.

2. Four pre-existing V0.2 mutation tests used exact source anchors from the pre-BF-1-PRIME implementation. After the implementation changed bool-return branches from False to canonical-path-return branches using None, and changed the subprocess argv to str(resolved), those source anchors no longer existed. Only the mutation anchor strings were updated; their failure modes and expected verdicts were unchanged.

Historical RED evidence remains preserved at its original commit and blob identities. These harness corrections do not rewrite that history.

~~~

## BF1 PRIME QUALIFICATION

PATH: tools/obsidian_projection/rpe03_v02_bf1_prime_executable_identity_qualification_v0_1.json

~~~json
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE03_V02_BF1_PRIME_EXECUTABLE_IDENTITY_QUALIFICATION_V0_1",
  "status": "QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW",
  "date": "2026-10-05",
  "branch": "feat/obsidian-projection-rpe03-governed-git-executable-binding-v0.2",
  "lineage": {
    "prior_external_packet_head": "a6a10b2f4303afac01ddc5d6bca36a9b32d7913a",
    "bf1_prime_adjudication_head": "96783f48cd1206432a46044c0e9ce35f040be602",
    "bf1_prime_preregistration_head": "d91d7d373b631e887c087ef6558e507e2c7187f9",
    "bf1_prime_red_head": "4f2f8c7ef279f904db905670ffa0f94b6b106f55",
    "bf1_prime_patch_head": "d973fe17a3ef38af67cbd9bff7dd90a440fcebe2"
  },
  "exact_identities": {
    "external_review_blob": "df64d9545ae1eab2661d3ef63646eeaf3142faff",
    "human_adjudication_blob": "e99a0018a3cda7d02ed3bb81914cfea223cdd36a",
    "preregistration_blob": "3f4b193ac15ca3fafa34e13934e0ba1dee84e162",
    "preregistration_schema_blob": "32b4cbd980245ceef781def548ff5e7b591cd41e",
    "historical_red_test_blob": "984249ee982d652678517707c3f683a8acd57d44",
    "historical_red_report_blob": "bf6462f390f445a64d540e99c45b25dc1a52f8fa",
    "final_classifier_blob": "5bbe455418fe1396ee5824379ad7450a1379cbba",
    "final_closure_test_blob": "47d964fcc6a7fdf2b1a018f9b90fcc7b02d8ffd5",
    "bf1_prime_mutation_test_blob": "d04b07e65b58bdc1af949b757de97114b5835793",
    "updated_v02_mutation_test_blob": "3dad153472c433d9451a7343c853d66811719c83",
    "windows_sentinel_evidence_blob": "eb7973e35f24565ad9a685511ff43e500b86f872",
    "harness_corrections_blob": "b82c107a06282f52617f946fe556df66b7e96501",
    "rpe03_v01_classifier_blob": "145b3112fd9309cc34d95a62c091cb6a6bc3bb11",
    "rpe01_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887",
    "p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5"
  },
  "governed_git": {
    "absolute_path": "C:\\Program Files\\Git\\cmd\\git.exe",
    "sha256": "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5",
    "observed_version": "git version 2.54.0.windows.1",
    "minimum_version": "2.54.0",
    "direct_classifier_executable_binding_qualified_candidate": true,
    "full_git_for_windows_helper_chain_qualified": false
  },
  "evidence": {
    "historical_red": "4/4 FAIL",
    "final_bf1_prime_closure": "5/5 PASS",
    "bf1_prime_mutations": "3/3 PASS",
    "updated_prior_v02_mutations": "4/4 PASS",
    "complete_rpe03_surface": "59/59 PASS",
    "rpe04_call_site_compatibility_included_in_surface": true,
    "windows_control_implicit_rc": 7,
    "windows_control_sentinel_created": true,
    "final_classification_with_fake_present": "FAST_FORWARD",
    "final_sentinel_created": false
  },
  "qualified_properties": {
    "non_absolute_executable_input_rejected": true,
    "canonical_path_strictly_resolved": true,
    "canonical_path_equals_governed_path": true,
    "sha256_verified": true,
    "exact_version_verified": true,
    "minimum_version_verified": true,
    "verified_canonical_path_returned": true,
    "raw_caller_string_not_reused_after_verification": true,
    "all_classifier_git_subprocesses_use_verified_canonical_path": true,
    "internal_run_git_rejects_non_absolute_input": true,
    "ancestry_semantics_unchanged": true
  },
  "limitations": {
    "privileged_program_files_toctou_out_of_scope": true,
    "exact_version_and_minimum_version_redundancy_accepted": true,
    "rpe02_model_not_present_on_rpe03_historical_lineage": true,
    "rpe04_rebind_not_performed": true,
    "rpe04_nf2_open": true,
    "rpe04_nf3_open": true
  },
  "authority_boundary": {
    "rpe03_v02_human_adopted": false,
    "rpe04_functional_rebind_authorized": false,
    "rpe05_opened": false,
    "rpe06_opened": false,
    "real_p5e_opened": false
  },
  "next_gate": "EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADOPTION",
  "stop": true
}

~~~

## BF1 PRIME QUALIFICATION SCHEMA

PATH: tools/obsidian_projection/rpe03_v02_bf1_prime_executable_identity_qualification_v0_1_schema_v0_1.json

~~~json
{
  "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
  "artifact_role": "RPE03_V02_BF1_PRIME_EXECUTABLE_IDENTITY_QUALIFICATION",
  "root": {
    "kind": "object",
    "fields": {
      "schema": {
        "kind": "string",
        "const": "ATDS_OBSIDIAN_REAL_P5E_RPE03_V02_BF1_PRIME_EXECUTABLE_IDENTITY_QUALIFICATION_V0_1"
      },
      "status": {
        "kind": "string",
        "const": "QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW"
      },
      "date": {
        "kind": "string",
        "const": "2026-10-05"
      },
      "branch": {
        "kind": "string",
        "const": "feat/obsidian-projection-rpe03-governed-git-executable-binding-v0.2"
      },
      "lineage": {
        "kind": "object",
        "fields": {
          "prior_external_packet_head": {
            "kind": "string",
            "const": "a6a10b2f4303afac01ddc5d6bca36a9b32d7913a"
          },
          "bf1_prime_adjudication_head": {
            "kind": "string",
            "const": "96783f48cd1206432a46044c0e9ce35f040be602"
          },
          "bf1_prime_preregistration_head": {
            "kind": "string",
            "const": "d91d7d373b631e887c087ef6558e507e2c7187f9"
          },
          "bf1_prime_red_head": {
            "kind": "string",
            "const": "4f2f8c7ef279f904db905670ffa0f94b6b106f55"
          },
          "bf1_prime_patch_head": {
            "kind": "string",
            "const": "d973fe17a3ef38af67cbd9bff7dd90a440fcebe2"
          }
        }
      },
      "exact_identities": {
        "kind": "object",
        "fields": {
          "external_review_blob": {
            "kind": "string",
            "const": "df64d9545ae1eab2661d3ef63646eeaf3142faff"
          },
          "human_adjudication_blob": {
            "kind": "string",
            "const": "e99a0018a3cda7d02ed3bb81914cfea223cdd36a"
          },
          "preregistration_blob": {
            "kind": "string",
            "const": "3f4b193ac15ca3fafa34e13934e0ba1dee84e162"
          },
          "preregistration_schema_blob": {
            "kind": "string",
            "const": "32b4cbd980245ceef781def548ff5e7b591cd41e"
          },
          "historical_red_test_blob": {
            "kind": "string",
            "const": "984249ee982d652678517707c3f683a8acd57d44"
          },
          "historical_red_report_blob": {
            "kind": "string",
            "const": "bf6462f390f445a64d540e99c45b25dc1a52f8fa"
          },
          "final_classifier_blob": {
            "kind": "string",
            "const": "5bbe455418fe1396ee5824379ad7450a1379cbba"
          },
          "final_closure_test_blob": {
            "kind": "string",
            "const": "47d964fcc6a7fdf2b1a018f9b90fcc7b02d8ffd5"
          },
          "bf1_prime_mutation_test_blob": {
            "kind": "string",
            "const": "d04b07e65b58bdc1af949b757de97114b5835793"
          },
          "updated_v02_mutation_test_blob": {
            "kind": "string",
            "const": "3dad153472c433d9451a7343c853d66811719c83"
          },
          "windows_sentinel_evidence_blob": {
            "kind": "string",
            "const": "eb7973e35f24565ad9a685511ff43e500b86f872"
          },
          "harness_corrections_blob": {
            "kind": "string",
            "const": "b82c107a06282f52617f946fe556df66b7e96501"
          },
          "rpe03_v01_classifier_blob": {
            "kind": "string",
            "const": "145b3112fd9309cc34d95a62c091cb6a6bc3bb11"
          },
          "rpe01_guard_blob": {
            "kind": "string",
            "const": "26f977961d72a062199d71ffd628d5a5cc047887"
          },
          "p5e_contract_blob": {
            "kind": "string",
            "const": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9"
          },
          "p5d4_runtime_blob": {
            "kind": "string",
            "const": "1825e53d195ba2a63b5b646a5b78eb77939b94b5"
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
          "minimum_version": {
            "kind": "string",
            "const": "2.54.0"
          },
          "direct_classifier_executable_binding_qualified_candidate": {
            "kind": "boolean",
            "const": true
          },
          "full_git_for_windows_helper_chain_qualified": {
            "kind": "boolean",
            "const": false
          }
        }
      },
      "evidence": {
        "kind": "object",
        "fields": {
          "historical_red": {
            "kind": "string",
            "const": "4/4 FAIL"
          },
          "final_bf1_prime_closure": {
            "kind": "string",
            "const": "5/5 PASS"
          },
          "bf1_prime_mutations": {
            "kind": "string",
            "const": "3/3 PASS"
          },
          "updated_prior_v02_mutations": {
            "kind": "string",
            "const": "4/4 PASS"
          },
          "complete_rpe03_surface": {
            "kind": "string",
            "const": "59/59 PASS"
          },
          "rpe04_call_site_compatibility_included_in_surface": {
            "kind": "boolean",
            "const": true
          },
          "windows_control_implicit_rc": {
            "kind": "integer",
            "const": 7
          },
          "windows_control_sentinel_created": {
            "kind": "boolean",
            "const": true
          },
          "final_classification_with_fake_present": {
            "kind": "string",
            "const": "FAST_FORWARD"
          },
          "final_sentinel_created": {
            "kind": "boolean",
            "const": false
          }
        }
      },
      "qualified_properties": {
        "kind": "object",
        "fields": {
          "non_absolute_executable_input_rejected": {
            "kind": "boolean",
            "const": true
          },
          "canonical_path_strictly_resolved": {
            "kind": "boolean",
            "const": true
          },
          "canonical_path_equals_governed_path": {
            "kind": "boolean",
            "const": true
          },
          "sha256_verified": {
            "kind": "boolean",
            "const": true
          },
          "exact_version_verified": {
            "kind": "boolean",
            "const": true
          },
          "minimum_version_verified": {
            "kind": "boolean",
            "const": true
          },
          "verified_canonical_path_returned": {
            "kind": "boolean",
            "const": true
          },
          "raw_caller_string_not_reused_after_verification": {
            "kind": "boolean",
            "const": true
          },
          "all_classifier_git_subprocesses_use_verified_canonical_path": {
            "kind": "boolean",
            "const": true
          },
          "internal_run_git_rejects_non_absolute_input": {
            "kind": "boolean",
            "const": true
          },
          "ancestry_semantics_unchanged": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "limitations": {
        "kind": "object",
        "fields": {
          "privileged_program_files_toctou_out_of_scope": {
            "kind": "boolean",
            "const": true
          },
          "exact_version_and_minimum_version_redundancy_accepted": {
            "kind": "boolean",
            "const": true
          },
          "rpe02_model_not_present_on_rpe03_historical_lineage": {
            "kind": "boolean",
            "const": true
          },
          "rpe04_rebind_not_performed": {
            "kind": "boolean",
            "const": true
          },
          "rpe04_nf2_open": {
            "kind": "boolean",
            "const": true
          },
          "rpe04_nf3_open": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "authority_boundary": {
        "kind": "object",
        "fields": {
          "rpe03_v02_human_adopted": {
            "kind": "boolean",
            "const": false
          },
          "rpe04_functional_rebind_authorized": {
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

## BF1 PRIME QUALIFICATION REPORT

PATH: reports/program/2026-10-05-OBSIDIAN-REAL-P5E-RPE03-V02-BF1-PRIME-QUALIFICATION.md

~~~text
# RPE-03 V0.2 — BF-1 PRIME VERIFIED/EXECUTED EXECUTABLE IDENTITY — QUALIFICATION

Date: 2026-10-05

## Result

RPE03_V02_DIRECT_CLASSIFIER_EXECUTABLE_BINDING
= QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW

This is not human adoption.

## BF-1 PRIME closure

The final candidate requires the caller-supplied executable string to be absolute.

The absolute input is strictly resolved, matched to the governed canonical Git path, SHA-256 verified, exact-version verified, minimum-version verified, and returned as the verified canonical executable.

Only that verified canonical executable is propagated into the ancestry-domain checks and Git subprocess calls.

The raw caller string is not reused after verification.

Internal _run_git additionally rejects non-absolute or non-governed executable paths.

## Governed identity

ABSOLUTE PATH
= C:\Program Files\Git\cmd\git.exe

SHA-256
= 81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5

OBSERVED VERSION
= git version 2.54.0.windows.1

MINIMUM VERSION
= 2.54.0

## Evidence

Historical BF-1 PRIME RED:
4/4 FAIL

Final BF-1 PRIME closure:
5/5 PASS

BF-1 PRIME mutations:
3/3 PASS

Updated prior V0.2 mutation harness:
4/4 PASS

Complete RPE-03 surface including V0.1, V0.2 and RPE-04 call-site compatibility:
59/59 PASS

## Windows positive-sentinel falsification

CONTROL / implicit executable search:
CONTROL_IMPLICIT_RC = 7
CONTROL_SENTINEL_CREATED = TRUE

FINAL CANDIDATE with the same fake git.exe present:
FINAL_CLASSIFICATION = FAST_FORWARD
FINAL_SENTINEL_CREATED = FALSE

Therefore the implicit search path can execute the temporary fake git.exe, while the final candidate does not execute it.

## Protected predecessors

RPE-03 V0.1 classifier remains:
145b3112fd9309cc34d95a62c091cb6a6bc3bb11

RPE-01 guard remains:
26f977961d72a062199d71ffd628d5a5cc047887

P5-E contract remains:
43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9

P5-D4 runtime remains:
1825e53d195ba2a63b5b646a5b78eb77939b94b5

The RPE-02 model is not present on this historical RPE-03 lineage, so no local blob comparison is claimed for it.

## Claim boundary

This candidate qualifies only the directly executed classifier Git executable.

It does not qualify the full Git-for-Windows helper executable chain.

The privileged Program Files replacement TOCTOU scenario remains outside the current threat model and is documented as non-blocking.

Exact-version and minimum-version checks remain intentionally redundant.

RPE-04 has not been rebound to this candidate.

RPE-04 NF-2 and NF-3 remain open.

RPE-03 V0.2 HUMAN ADOPTION = PENDING
RPE-04 = BLOCKED_PENDING_RPE03_V0.2
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
