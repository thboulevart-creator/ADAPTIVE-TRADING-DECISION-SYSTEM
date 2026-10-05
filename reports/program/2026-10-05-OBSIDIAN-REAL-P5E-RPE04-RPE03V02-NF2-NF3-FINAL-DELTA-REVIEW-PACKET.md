# RPE-04 — RPE03 V0.2 REBIND + NF2 + NF3 — FINAL DELTA REVIEW PACKET

Date: 2026-10-05

Candidate state:
RPE04_REMOTE_OBSERVATION_ADAPTER = QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW

Human adoption:
PENDING

Qualification HEAD before packet:
e971005737af308f7849d16cf9c423d6096752a8

Final RPE-04 implementation Git blob:
e188414cd433f839d5efbe5d28840d7acf4938d5

Final RPE-04 implementation raw SHA-256:
1300e60a5cd353557cc16779a372979b436fcacfeb082435cd749987342d1638

Human-adopted RPE-03 V0.2 classifier:
5bbe455418fe1396ee5824379ad7450a1379cbba

RPE-03 V0.2 adoption commit:
f266121e6a65daa3bf19480412f1addd299b8172

Qualification blob:
0cbb3df84edc0726ef09cad1b6ec702933b547eb

Qualification schema blob:
784e5ef03f7d3b1ac831df7c219f403340bccc4f

Qualification report blob:
4e25778a0498863a674531ae90d3969506a3d8bb

Final test-evidence blob:
0dab2fe5904acbf698f6c4eae29e4eb31c532b67

Candidate closures:
BF-1 = CLOSED_BY_EXACT_RPE03_V0.2_REBIND
NF-2 = CLOSED
NF-3 = CLOSED
NF-4 = CARRIED_TO_RPE-05

Observed Windows evidence:
- RPE-03 V0.2 rebind + NF-2: 5/5 PASS
- NF-3 full physical domain: 7/7 PASS
- runtime-binding hardening: 5/5 PASS
- NF-2/NF-3 mutations: 3/3 PASS
- RPE-04 current dedicated surface: 55/55 PASS
- RPE-03 exact final qualified surface: 59/59 PASS
- RPE-02 protected regression: 51/51 PASS
- RPE-01 protected regression: 46/46 PASS
- P5-E protected regression: 67/67 PASS
- protected blob identities: PASS

Scope:
LOCAL-ONLY QUALIFICATION
NO GITHUB POLLING
NO PRODUCTION REMOTE OBSERVATION
NO REAL 60-SECOND SLA CLAIM
NF-4 REMAINS CARRIED TO RPE-05

## Required reviewer output

VERDICT = PASS | PASS_WITH_NON_BLOCKING_NOTES | FAIL

### BLOCKING_FINDINGS
### NON_BLOCKING_FINDINGS
### EXACT_RPE03_V02_BINDING_CHECK
### EXACT_OBSERVED_REF_IDENTITY_CHECK
### NO_TAG_DEREFERENCE_LAUNDERING_CHECK
### OBSERVED_TIP_VS_CONTAINED_HISTORY_CHECK
### FULL_PHYSICAL_DOMAIN_CONTAINMENT_CHECK
### REFS_CONTAINMENT_CHECK
### CONFIG_HEAD_PACKED_REFS_CONTAINMENT_CHECK
### OBJECT_ALTERNATES_REJECTION_CHECK
### POST_FETCH_REVALIDATION_CHECK
### CALLER_AUTHORITY_LAUNDERING_CHECK
### MUTATION_DISCRIMINATION_CHECK
### REGRESSION_CHECK
### PROTECTED_IDENTITY_CHECK
### CLAIM_SCOPE_CHECK
### RPE04_ADOPTION_READINESS
### RECOMMENDED_NEXT_ACTION

Key adversarial questions:

1. Is RPE-04 bound exactly to the human-adopted RPE-03 V0.2 classifier blob, with the governed absolute Git executable handed to it?
2. Is the observed-tip SHA now the exact object ID stored in refs/rpe04/observed, without commit peeling or equivalent dereference?
3. Can an annotated tag or other non-commit exact ref target cause its contained commit to receive OBSERVED_REMOTE_TIP authority?
4. Does the physical-domain verifier cover refs, refs/rpe04, HEAD, config, packed-refs, objects, objects/info, objects/pack, alternates, and existing descendants?
5. Can a symlink, junction, reparse point, alternates file, redirected ref, redirected config/HEAD/packed-refs, or pack/index indirection escape the governed domain?
6. Are physical-domain conditions revalidated after fetch before positive observed-tip acceptance and before RPE-03 classification?
7. Can caller-supplied transition, containment, executable, or intermediate-commit data create authority?
8. Do targeted mutations discriminate the NF-2 peeling and NF-3 containment protections?
9. Are predecessor identities unchanged and regressions supported by the supplied execution evidence?
10. Is the claim correctly limited to local-only RPE-04 qualification, with NF-4, RPE-05, RPE-06 and REAL P5-E still closed?

This review creates no authority.
RPE-04 HUMAN ADOPTION = PENDING
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

## PRIOR RPE04 EXTERNAL REVIEW

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

## PRIOR RPE04 HUMAN ADJUDICATION

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

## RPE03 V0.2 HUMAN ADOPTION

PATH: GOVERNANCE/RPE-03-V02-GOVERNED-GIT-EXECUTABLE-BINDING-HUMAN-ADJUDICATION-2026-10-05.md

~~~text
# RPE-03 V0.2 — GOVERNED GIT EXECUTABLE BINDING — HUMAN ADJUDICATION

Date: 2026-10-05

## External review adjudication

EXTERNAL_DELTA_REVIEW
= VALID_EXTERNAL_EVIDENCE

VERDICT
= PASS_WITH_NON_BLOCKING_NOTES

BLOCKING_FINDINGS
= NONE

## Independent repository identity verification

FINAL_CLASSIFIER_BLOB
= 5bbe455418fe1396ee5824379ad7450a1379cbba

WORKTREE_CLASSIFIER_BLOB
= 5bbe455418fe1396ee5824379ad7450a1379cbba

PRE-ADOPTION HEAD
= ecee5880b6fc26404255226d4309629cf08ff05d

LOCAL_HEAD
= ecee5880b6fc26404255226d4309629cf08ff05d

REMOTE_HEAD
= ecee5880b6fc26404255226d4309629cf08ff05d

WORKTREE
= CLEAN

## Findings adjudication

BF-1
= CLOSED

BF-1 PRIME
= CLOSED

N-1
= CLOSED_BY_EXACT_REPOSITORY_IDENTITY_VERIFICATION

N-2
= ACCEPTED_AS_NON_BLOCKING_TOCTOU_LIMIT
= OUTSIDE_CURRENT_LOCAL_THREAT_MODEL

N-3
= ACCEPTED_AS_OPTIONAL_WINDOWS_EDGE_TEST
= NON_BLOCKING

N-4
= ACCEPTED_AS_EXTERNAL_EXECUTION_LIMITATION

## Human adoption

RPE03_V02_GOVERNED_GIT_EXECUTABLE_BINDING
= QUALIFIED_AND_HUMAN_ADOPTED

Normative identity:

PRE-ADOPTION HEAD
= ecee5880b6fc26404255226d4309629cf08ff05d

RPE-03 V0.2 CLASSIFIER
= 5bbe455418fe1396ee5824379ad7450a1379cbba

BF-1 PRIME QUALIFICATION
= 688a2abcc2caa2edeed5e67f2d3c38b293bcc238

EXTERNAL DELTA REVIEW PACKET
= a5264208ee9be57725dd9c73251e462452275b77

## Adopted executable-binding semantics

CALLER EXECUTABLE
→ MUST BE ABSOLUTE

ABSOLUTE INPUT
→ STRICT CANONICAL RESOLUTION

CANONICAL EXECUTABLE
→ EXACT GOVERNED PATH MATCH
→ SHA-256 MATCH
→ EXACT VERSION MATCH
→ MINIMUM VERSION CHECK

VERIFIED CANONICAL EXECUTABLE
→ EXACT EXECUTABLE USED BY CLASSIFIER SUBPROCESSES

Non-absolute inputs remain fail-closed:

git
git.exe
.\git.exe
relative\git.exe
→ UNKNOWN

## Ancestry semantic immutability

The ancestry vocabulary remains:

INITIAL
SAME
FAST_FORWARD
NON_FAST_FORWARD
UNKNOWN

RPE-03 V0.1 remains an immutable historically adopted artifact.

## Explicit claim limits

This adoption does not qualify:

FULL GIT-FOR-WINDOWS HELPER CHAIN
PRIVILEGED PROGRAM-FILES TOCTOU ATTACK
RPE-04 BF-1 REBIND
RPE-04 NF-2
RPE-04 NF-3
RPE-05
RPE-06
REAL P5-E

## Post-adoption state

RPE-03 V0.2
= CLOSED
= QUALIFIED_AND_HUMAN_ADOPTED

RPE-04
= OPEN
= ELIGIBLE_FOR_TARGETED_REBIND_AND_NF2_NF3_CLOSURE

RPE-05
= CLOSED

RPE-06
= CLOSED

REAL P5-E
= CLOSED

## Authority boundary

Authorized by the human principal for this operation only:

PERSIST THIS HUMAN ADOPTION
COMMIT
PUSH
LOCAL=REMOTE VERIFICATION
CLEAN WORKTREE VERIFICATION
STOP

Not authorized in this operation:

RPE-04 REBIND
RPE-04 NF-2 CORRECTION
RPE-04 NF-3 CORRECTION
RPE-05
RPE-06
REAL P5-E

STOP after persistence and verification of this adoption.

~~~

## RPE03 V0.2 ADOPTED CLASSIFIER

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

## CLOSURE PREREGISTRATION

PATH: tools/obsidian_projection/rpe04_rpe03v02_rebind_nf2_nf3_closure_v0_1.json

~~~json
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE04_RPE03V02_REBIND_NF2_NF3_CLOSURE_V0_1",
  "status": "PREREGISTERED_BEFORE_RED",
  "date": "2026-10-05",
  "base": {
    "rpe04_external_review_adjudicated_head": "ec41c8a79defad9f343ee5c93b55c0c776f690fe",
    "adopted_rpe03_v02_dependency_import_head": "017fca56001c2181d6aafcce153283b0562adcb1",
    "rpe03_v02_adoption_commit": "f266121e6a65daa3bf19480412f1addd299b8172",
    "rpe03_v02_adoption_blob": "73b5a951a2ed9ed42cb827b4fadc555fc3dd7a7d",
    "rpe03_v02_classifier_blob": "5bbe455418fe1396ee5824379ad7450a1379cbba",
    "rpe03_v02_qualification_blob": "688a2abcc2caa2edeed5e67f2d3c38b293bcc238",
    "rpe03_v02_classifier_raw_sha256": "4b743e187245585f4a4d9c923e316961f2842f96634d04dcac01972a29e60b41"
  },
  "scope": {
    "close_bf1_by_exact_rpe03_v02_rebind": true,
    "close_nf2_exact_observed_tip": true,
    "close_nf3_full_physical_domain": true,
    "close_nf4": false,
    "rpe05_authorized": false,
    "rpe06_authorized": false,
    "real_p5e_authorized": false
  },
  "rpe03_v02_rebind": {
    "classifier_path": "tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py",
    "classifier_blob": "5bbe455418fe1396ee5824379ad7450a1379cbba",
    "classifier_raw_sha256": "4b743e187245585f4a4d9c923e316961f2842f96634d04dcac01972a29e60b41",
    "governed_git_absolute_path": "C:\\Program Files\\Git\\cmd\\git.exe",
    "governed_git_sha256": "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5",
    "governed_git_version": "git version 2.54.0.windows.1",
    "caller_creates_executable_authority": false
  },
  "nf2_exact_observed_tip": {
    "exact_local_ref": "refs/rpe04/observed",
    "extraction_command_semantics": "for-each-ref exact ref objectname plus objecttype without peeling",
    "peeling_for_observed_tip_authority_forbidden": true,
    "commit_required": true,
    "accepted_object_type": "commit",
    "annotated_tag_object_type": "tag",
    "annotated_tag_behavior": "READ_FAILURE_EXACT_OBSERVED_REF_NOT_COMMIT",
    "exact_oid_format": "lowercase 40-hex",
    "contained_commit_from_tag_must_not_be_observed_tip": true
  },
  "nf3_full_physical_domain": {
    "governed_root": "C:\\Users\\Boulevart\\ATDS-CONTROL\\RPE04-QUALIFICATION\\observer.git",
    "check_before_fetch": true,
    "check_after_fetch_before_tip_acceptance": true,
    "check_before_rpe03_classification": true,
    "reject_reparse_points_recursively": true,
    "reject_symlinks_recursively": true,
    "reject_junctions_recursively": true,
    "resolved_paths_must_remain_under_root": true,
    "reject_alternates": true,
    "required_directories": [
      "objects",
      "objects/info",
      "objects/pack",
      "refs"
    ],
    "authority_paths": [
      "HEAD",
      "config",
      "packed-refs",
      "refs",
      "refs/rpe04",
      "objects",
      "objects/info",
      "objects/pack",
      "objects/info/alternates"
    ],
    "inspect_existing_descendants_recursively": true,
    "pack_and_index_file_indirections_rejected": true,
    "absent_optional_authority_files_allowed": [
      "packed-refs",
      "objects/info/alternates"
    ],
    "missing_required_path_behavior": "BLOCKED"
  },
  "semantic_immutability": {
    "one_governed_fetch_transaction_per_attempt": true,
    "no_ls_remote_plus_independent_fetch": true,
    "exact_source_ref": true,
    "isolated_local_observation_ref": true,
    "no_tag_fetch": true,
    "no_submodule_recursion": true,
    "no_fetch_head_write": true,
    "no_caller_transition_authority": true,
    "no_caller_containment_authority": true,
    "unknown_is_blocked": true,
    "no_intermediate_commit_injection": true
  },
  "timing_boundary": {
    "success_timing_semantics_unchanged": true,
    "nf4_failure_mapping_carried_to_rpe05": true
  },
  "required_red": [
    "annotated tag cannot be laundered to peeled commit observed tip",
    "exact ref object type must be commit",
    "objects indirection blocked",
    "refs indirection blocked",
    "refs/rpe04 indirection blocked",
    "config indirection blocked",
    "HEAD indirection blocked",
    "packed-refs indirection blocked",
    "objects/info/alternates presence blocked",
    "pack or index file indirection blocked where representable",
    "post-fetch containment change blocks before positive observation"
  ],
  "stop": "EXTERNAL_DELTA_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
}

~~~

## CLOSURE PREREGISTRATION SCHEMA

PATH: tools/obsidian_projection/rpe04_rpe03v02_rebind_nf2_nf3_closure_v0_1_schema_v0_1.json

~~~json
{
  "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
  "artifact_role": "RPE04_RPE03V02_REBIND_NF2_NF3_CLOSURE",
  "root": {
    "kind": "object",
    "fields": {
      "schema": {
        "kind": "string",
        "const": "ATDS_OBSIDIAN_REAL_P5E_RPE04_RPE03V02_REBIND_NF2_NF3_CLOSURE_V0_1"
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
          "rpe04_external_review_adjudicated_head": {
            "kind": "string",
            "const": "ec41c8a79defad9f343ee5c93b55c0c776f690fe"
          },
          "adopted_rpe03_v02_dependency_import_head": {
            "kind": "string",
            "const": "017fca56001c2181d6aafcce153283b0562adcb1"
          },
          "rpe03_v02_adoption_commit": {
            "kind": "string",
            "const": "f266121e6a65daa3bf19480412f1addd299b8172"
          },
          "rpe03_v02_adoption_blob": {
            "kind": "string",
            "const": "73b5a951a2ed9ed42cb827b4fadc555fc3dd7a7d"
          },
          "rpe03_v02_classifier_blob": {
            "kind": "string",
            "const": "5bbe455418fe1396ee5824379ad7450a1379cbba"
          },
          "rpe03_v02_qualification_blob": {
            "kind": "string",
            "const": "688a2abcc2caa2edeed5e67f2d3c38b293bcc238"
          },
          "rpe03_v02_classifier_raw_sha256": {
            "kind": "string",
            "const": "4b743e187245585f4a4d9c923e316961f2842f96634d04dcac01972a29e60b41"
          }
        }
      },
      "scope": {
        "kind": "object",
        "fields": {
          "close_bf1_by_exact_rpe03_v02_rebind": {
            "kind": "boolean",
            "const": true
          },
          "close_nf2_exact_observed_tip": {
            "kind": "boolean",
            "const": true
          },
          "close_nf3_full_physical_domain": {
            "kind": "boolean",
            "const": true
          },
          "close_nf4": {
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
      "rpe03_v02_rebind": {
        "kind": "object",
        "fields": {
          "classifier_path": {
            "kind": "string",
            "const": "tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py"
          },
          "classifier_blob": {
            "kind": "string",
            "const": "5bbe455418fe1396ee5824379ad7450a1379cbba"
          },
          "classifier_raw_sha256": {
            "kind": "string",
            "const": "4b743e187245585f4a4d9c923e316961f2842f96634d04dcac01972a29e60b41"
          },
          "governed_git_absolute_path": {
            "kind": "string",
            "const": "C:\\Program Files\\Git\\cmd\\git.exe"
          },
          "governed_git_sha256": {
            "kind": "string",
            "const": "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5"
          },
          "governed_git_version": {
            "kind": "string",
            "const": "git version 2.54.0.windows.1"
          },
          "caller_creates_executable_authority": {
            "kind": "boolean",
            "const": false
          }
        }
      },
      "nf2_exact_observed_tip": {
        "kind": "object",
        "fields": {
          "exact_local_ref": {
            "kind": "string",
            "const": "refs/rpe04/observed"
          },
          "extraction_command_semantics": {
            "kind": "string",
            "const": "for-each-ref exact ref objectname plus objecttype without peeling"
          },
          "peeling_for_observed_tip_authority_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "commit_required": {
            "kind": "boolean",
            "const": true
          },
          "accepted_object_type": {
            "kind": "string",
            "const": "commit"
          },
          "annotated_tag_object_type": {
            "kind": "string",
            "const": "tag"
          },
          "annotated_tag_behavior": {
            "kind": "string",
            "const": "READ_FAILURE_EXACT_OBSERVED_REF_NOT_COMMIT"
          },
          "exact_oid_format": {
            "kind": "string",
            "const": "lowercase 40-hex"
          },
          "contained_commit_from_tag_must_not_be_observed_tip": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "nf3_full_physical_domain": {
        "kind": "object",
        "fields": {
          "governed_root": {
            "kind": "string",
            "const": "C:\\Users\\Boulevart\\ATDS-CONTROL\\RPE04-QUALIFICATION\\observer.git"
          },
          "check_before_fetch": {
            "kind": "boolean",
            "const": true
          },
          "check_after_fetch_before_tip_acceptance": {
            "kind": "boolean",
            "const": true
          },
          "check_before_rpe03_classification": {
            "kind": "boolean",
            "const": true
          },
          "reject_reparse_points_recursively": {
            "kind": "boolean",
            "const": true
          },
          "reject_symlinks_recursively": {
            "kind": "boolean",
            "const": true
          },
          "reject_junctions_recursively": {
            "kind": "boolean",
            "const": true
          },
          "resolved_paths_must_remain_under_root": {
            "kind": "boolean",
            "const": true
          },
          "reject_alternates": {
            "kind": "boolean",
            "const": true
          },
          "required_directories": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 4,
            "max_items": 4,
            "unique": true,
            "ordered_const": [
              "objects",
              "objects/info",
              "objects/pack",
              "refs"
            ],
            "allowed_values": [
              "objects",
              "objects/info",
              "objects/pack",
              "refs"
            ]
          },
          "authority_paths": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 9,
            "max_items": 9,
            "unique": true,
            "ordered_const": [
              "HEAD",
              "config",
              "packed-refs",
              "refs",
              "refs/rpe04",
              "objects",
              "objects/info",
              "objects/pack",
              "objects/info/alternates"
            ],
            "allowed_values": [
              "HEAD",
              "config",
              "packed-refs",
              "refs",
              "refs/rpe04",
              "objects",
              "objects/info",
              "objects/pack",
              "objects/info/alternates"
            ]
          },
          "inspect_existing_descendants_recursively": {
            "kind": "boolean",
            "const": true
          },
          "pack_and_index_file_indirections_rejected": {
            "kind": "boolean",
            "const": true
          },
          "absent_optional_authority_files_allowed": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 2,
            "max_items": 2,
            "unique": true,
            "ordered_const": [
              "packed-refs",
              "objects/info/alternates"
            ],
            "allowed_values": [
              "packed-refs",
              "objects/info/alternates"
            ]
          },
          "missing_required_path_behavior": {
            "kind": "string",
            "const": "BLOCKED"
          }
        }
      },
      "semantic_immutability": {
        "kind": "object",
        "fields": {
          "one_governed_fetch_transaction_per_attempt": {
            "kind": "boolean",
            "const": true
          },
          "no_ls_remote_plus_independent_fetch": {
            "kind": "boolean",
            "const": true
          },
          "exact_source_ref": {
            "kind": "boolean",
            "const": true
          },
          "isolated_local_observation_ref": {
            "kind": "boolean",
            "const": true
          },
          "no_tag_fetch": {
            "kind": "boolean",
            "const": true
          },
          "no_submodule_recursion": {
            "kind": "boolean",
            "const": true
          },
          "no_fetch_head_write": {
            "kind": "boolean",
            "const": true
          },
          "no_caller_transition_authority": {
            "kind": "boolean",
            "const": true
          },
          "no_caller_containment_authority": {
            "kind": "boolean",
            "const": true
          },
          "unknown_is_blocked": {
            "kind": "boolean",
            "const": true
          },
          "no_intermediate_commit_injection": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "timing_boundary": {
        "kind": "object",
        "fields": {
          "success_timing_semantics_unchanged": {
            "kind": "boolean",
            "const": true
          },
          "nf4_failure_mapping_carried_to_rpe05": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "required_red": {
        "kind": "array",
        "items": {
          "kind": "string"
        },
        "min_items": 11,
        "max_items": 11,
        "unique": true,
        "ordered_const": [
          "annotated tag cannot be laundered to peeled commit observed tip",
          "exact ref object type must be commit",
          "objects indirection blocked",
          "refs indirection blocked",
          "refs/rpe04 indirection blocked",
          "config indirection blocked",
          "HEAD indirection blocked",
          "packed-refs indirection blocked",
          "objects/info/alternates presence blocked",
          "pack or index file indirection blocked where representable",
          "post-fetch containment change blocks before positive observation"
        ],
        "allowed_values": [
          "annotated tag cannot be laundered to peeled commit observed tip",
          "exact ref object type must be commit",
          "objects indirection blocked",
          "refs indirection blocked",
          "refs/rpe04 indirection blocked",
          "config indirection blocked",
          "HEAD indirection blocked",
          "packed-refs indirection blocked",
          "objects/info/alternates presence blocked",
          "pack or index file indirection blocked where representable",
          "post-fetch containment change blocks before positive observation"
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

## TARGETED RED REPORT

PATH: reports/program/2026-10-05-OBSIDIAN-REAL-P5E-RPE04-RPE03V02-NF2-NF3-TARGETED-RED.md

~~~text
# RPE-04 — RPE-03 V0.2 REBIND + NF-2 + NF-3 — TARGETED RED

Date: 2026-10-05

Preregistration HEAD:
1ba14c2d89904c51b6766a686f4249cca3b6b7ee

## RPE-03 V0.2 rebind + NF-2

Test:
tests/obsidian_projection/test_rpe04_rpe03v02_rebind_nf2_v0_1.py

Blob:
49540da4a64c25febe0bec26edbf0ce768193551

Observed:
- 5 tests
- 1 PASS
- 4 FAIL
- no ERROR

Confirmed RED findings:
- runtime binding still targets rpe03_ancestry_classifier_v0_1.py;
- RPE-03 call site supplies only 3 arguments, not governed Git path;
- annotated tag object is peeled to its contained commit and accepted as OBSERVED_REMOTE_TIP;
- exact local observation ref identity is not preserved because ^{commit} changes tag object ID to peeled commit ID.

Healthy control:
- normal commit ref remains a valid OBSERVED_REMOTE_TIP.

## NF-3 full physical Git domain

Test:
tests/obsidian_projection/test_rpe04_nf3_full_physical_domain_v0_1.py

Blob:
eadddb42e5806c57d95737965ba501dbe427722c

Observed:
- 7 tests
- 1 PASS
- 6 FAIL
- no ERROR

Confirmed RED findings:
- refs indirection not checked;
- refs/rpe04 indirection not checked;
- config / HEAD / packed-refs indirection not checked;
- objects/info/alternates presence not rejected by RPE-04 physical-domain verifier;
- pack-file-level indirection is not inspected recursively;
- alternates introduced after fetch are not rejected by RPE-04 before positive observation.

Healthy control:
- normal bare observation domain is accepted.

No RPE-04 implementation change existed during these RED runs.

RPE-03 V0.2 remains HUMAN_ADOPTED.
RPE-04 HUMAN ADOPTION remains PENDING.
RPE-05, RPE-06 and REAL P5-E remain CLOSED.

~~~

## FINAL RPE04 IMPLEMENTATION

PATH: tools/obsidian_projection/rpe04_real_remote_observation_adapter_v0_1.py

~~~python
"""RPE-04 V0.1: governed single-fetch remote observation adapter.

Qualification surface: local bare remote only. No GitHub polling, remote push,
queue mutation, evaluation, promotion, publication, Vault, or CURRENT authority.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import shutil
import stat
import subprocess
import time
from pathlib import Path
from typing import Final


_ROOT: Final = Path(__file__).resolve().parents[2]
_PREREG_PATH: Final = _ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_preregistration_v0_1.json"
_SCHEMA_PATH: Final = _ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_preregistration_v0_1_schema_v0_1.json"
_CLOSURE_PATH: Final = _ROOT / "tools/obsidian_projection/rpe04_rpe03v02_rebind_nf2_nf3_closure_v0_1.json"
_CLOSURE_SCHEMA_PATH: Final = _ROOT / "tools/obsidian_projection/rpe04_rpe03v02_rebind_nf2_nf3_closure_v0_1_schema_v0_1.json"
_GUARD_PATH: Final = _ROOT / "tools/obsidian_projection/rpe01_governed_closed_schema.py"
_RPE03_PATH: Final = _ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py"
_SHA40_RE: Final = re.compile(r"[0-9a-f]{40}\Z")

_EXPECTED_RUNTIME_SHA256: Final = {
    "preregistration": "0c59111fe90b8d80f0c41daf0911d772274eca733c6e68673d484ab8abf2c6ba",
    "schema": "e39dbc4f3bc82f5d5c2181574bdd120ad6d0fca46bcfdf358fac406b572a8861",
    "closure": "4c6c156c2bde72ed83b360a3ddccaf97a46b55b45cd107c85e32d998ef95cf11",
    "closure_schema": "b812979ffcd6496929a2e9cab672278708943c20cdd0f5e504f2d97c0bd02a41",
    "rpe01_guard": "24b36f5b3c0a02bc6247732fe1fa23d6c0fe30bc2b1629a7c54d4c094a628298",
    "rpe03_classifier": "4b743e187245585f4a4d9c923e316961f2842f96634d04dcac01972a29e60b41",
}


def _raw_sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _verify_runtime_bindings() -> bool:
    expected = {
        _PREREG_PATH: _EXPECTED_RUNTIME_SHA256["preregistration"],
        _SCHEMA_PATH: _EXPECTED_RUNTIME_SHA256["schema"],
        _CLOSURE_PATH: _EXPECTED_RUNTIME_SHA256["closure"],
        _CLOSURE_SCHEMA_PATH: _EXPECTED_RUNTIME_SHA256["closure_schema"],
        _GUARD_PATH: _EXPECTED_RUNTIME_SHA256["rpe01_guard"],
        _RPE03_PATH: _EXPECTED_RUNTIME_SHA256["rpe03_classifier"],
    }
    try:
        return all(path.is_file() and _raw_sha256_file(path) == digest for path, digest in expected.items())
    except (OSError, ValueError):
        return False


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load governed dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_preregistration() -> dict:
    if not _verify_runtime_bindings():
        raise RuntimeError("RPE04_RUNTIME_BINDING_MISMATCH")
    guard = _load_module(_GUARD_PATH, "rpe04_rpe01_guard")
    raw_document = _PREREG_PATH.read_text(encoding="utf-8")
    raw_schema = _SCHEMA_PATH.read_text(encoding="utf-8")
    validated = guard.validate_governed_json(raw_document, raw_schema)
    if type(validated) is not dict:
        raise RuntimeError("governed preregistration did not validate to an object")

    closure_document = _CLOSURE_PATH.read_text(encoding="utf-8")
    closure_schema = _CLOSURE_SCHEMA_PATH.read_text(encoding="utf-8")
    closure_validated = guard.validate_governed_json(closure_document, closure_schema)
    if type(closure_validated) is not dict:
        raise RuntimeError("governed closure preregistration did not validate to an object")

    return validated


_CFG: Final = _load_preregistration()
_RPE03: Final = _load_module(_RPE03_PATH, "rpe04_bound_rpe03_classifier")

_GIT: Final = Path(_CFG["git_executable"]["resolved_path"])
_SOURCE: Final = Path(_CFG["qualification_environment"]["source_bare_repository"])
_OBSERVER: Final = Path(_CFG["qualification_environment"]["observer_bare_repository"])
_SOURCE_REF: Final = _CFG["remote_transaction"]["source_ref"]
_LOCAL_REF: Final = _CFG["remote_transaction"]["isolated_local_ref"]
_TIMEOUT_SECONDS: Final = _CFG["remote_transaction"]["timeout_milliseconds"] / 1000


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(str(left.resolve(strict=False))) == os.path.normcase(
        str(right.resolve(strict=False))
    )


def _build_git_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(
        {
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "NUL",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
        }
    )
    return env


def _verify_git_executable_identity() -> bool:
    try:
        if not _GIT.is_file():
            return False
        if _sha256_file(_GIT) != _CFG["git_executable"]["sha256"]:
            return False
        resolved_token = shutil.which("git", path=os.environ.get("PATH"))
        if resolved_token is None or not _same_path(Path(resolved_token), _GIT):
            return False
        cp = subprocess.run(
            [str(_GIT), "--version"],
            env=_build_git_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
        return (
            cp.returncode == 0
            and cp.stdout.strip() == _CFG["git_executable"]["observed_version"]
        )
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False


def _is_indirection(path: Path) -> bool:
    try:
        if path.is_symlink():
            return True
        isjunction = getattr(os.path, "isjunction", None)
        if isjunction is not None and isjunction(path):
            return True
        attrs = getattr(os.lstat(path), "st_file_attributes", 0)
        reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        return bool(reparse and attrs & reparse)
    except (OSError, ValueError):
        return True


def _lexists(path: Path) -> bool:
    return os.path.lexists(str(path))


def _inside_root(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def _verify_physical_object_domain(repo_path: Path) -> tuple[bool, str | None]:
    legacy_required_dirs = [
        repo_path,
        repo_path / "objects",
        repo_path / "objects" / "pack",
        repo_path / "objects" / "info",
    ]

    try:
        if not _lexists(repo_path):
            return False, "PHYSICAL_OBJECT_DOMAIN_REQUIRED_PATH_MISSING"
        if _is_indirection(repo_path):
            return False, "PHYSICAL_OBJECT_DOMAIN_INDIRECTION"
        repo = repo_path.resolve(strict=True)
        if not repo.is_dir():
            return False, "PHYSICAL_OBJECT_DOMAIN_REQUIRED_PATH_MISSING"
    except (OSError, RuntimeError, ValueError):
        return False, "PHYSICAL_OBJECT_DOMAIN_UNPROVABLE"

    for path in legacy_required_dirs:
        try:
            if not _lexists(path) or not path.is_dir():
                return False, "PHYSICAL_OBJECT_DOMAIN_REQUIRED_PATH_MISSING"
            if _is_indirection(path):
                return False, "PHYSICAL_OBJECT_DOMAIN_INDIRECTION"
            resolved = path.resolve(strict=True)
            if not _inside_root(resolved, repo):
                return False, "PHYSICAL_OBJECT_DOMAIN_ESCAPE"
        except (OSError, RuntimeError, ValueError):
            return False, "PHYSICAL_OBJECT_DOMAIN_UNPROVABLE"

    refs = repo_path / "refs"
    try:
        if not _lexists(refs) or not refs.is_dir():
            return False, "PHYSICAL_GIT_DOMAIN_REQUIRED_PATH_MISSING"
        if _is_indirection(refs):
            return False, "PHYSICAL_GIT_DOMAIN_INDIRECTION"
        if not _inside_root(refs.resolve(strict=True), repo):
            return False, "PHYSICAL_GIT_DOMAIN_ESCAPE"
    except (OSError, RuntimeError, ValueError):
        return False, "PHYSICAL_GIT_DOMAIN_UNPROVABLE"

    for required_file in (repo_path / "HEAD", repo_path / "config"):
        try:
            if not _lexists(required_file) or not required_file.is_file():
                return False, "PHYSICAL_GIT_DOMAIN_REQUIRED_PATH_MISSING"
            if _is_indirection(required_file):
                return False, "PHYSICAL_GIT_DOMAIN_INDIRECTION"
            if not _inside_root(required_file.resolve(strict=True), repo):
                return False, "PHYSICAL_GIT_DOMAIN_ESCAPE"
        except (OSError, RuntimeError, ValueError):
            return False, "PHYSICAL_GIT_DOMAIN_UNPROVABLE"

    for optional_path in (repo_path / "packed-refs", repo_path / "refs" / "rpe04"):
        if not _lexists(optional_path):
            continue
        try:
            if _is_indirection(optional_path):
                return False, "PHYSICAL_GIT_DOMAIN_INDIRECTION"
            if not _inside_root(optional_path.resolve(strict=True), repo):
                return False, "PHYSICAL_GIT_DOMAIN_ESCAPE"
        except (OSError, RuntimeError, ValueError):
            return False, "PHYSICAL_GIT_DOMAIN_UNPROVABLE"

    alternates = repo_path / "objects" / "info" / "alternates"
    if _lexists(alternates):
        return False, "PHYSICAL_GIT_DOMAIN_ALTERNATES_FORBIDDEN"

    try:
        for current, dirs, files in os.walk(repo, topdown=True, followlinks=False):
            current_path = Path(current)
            for name in [*dirs, *files]:
                child = current_path / name
                if _is_indirection(child):
                    return False, "PHYSICAL_GIT_DOMAIN_INDIRECTION"
                resolved = child.resolve(strict=True)
                if not _inside_root(resolved, repo):
                    return False, "PHYSICAL_GIT_DOMAIN_ESCAPE"
    except (OSError, RuntimeError, ValueError):
        return False, "PHYSICAL_GIT_DOMAIN_UNPROVABLE"

    return True, None


def _run_local_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(_GIT), "-c", "core.hooksPath=NUL", "-c", "gc.auto=0", f"--git-dir={_OBSERVER}", *args],
        env=_build_git_env(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=_TIMEOUT_SECONDS,
        check=False,
    )


def _verify_local_config_allowlist() -> bool:
    try:
        cp = subprocess.run(
            [str(_GIT), f"--git-dir={_OBSERVER}", "config", "--local", "--no-includes", "--list"],
            env=_build_git_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False
    if cp.returncode != 0:
        return False
    observed = [line.strip() for line in cp.stdout.splitlines() if line.strip()]
    expected = _CFG["git_environment_isolation"]["local_config_allowlist"]
    return len(observed) == len(expected) and set(observed) == set(expected)


def _verify_remote_identity() -> bool:
    try:
        if not _SOURCE.exists() or not _SOURCE.is_dir() or _is_indirection(_SOURCE):
            return False
        cp = subprocess.run(
            [str(_GIT), f"--git-dir={_SOURCE}", "rev-parse", "--is-bare-repository"],
            env=_build_git_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
        return cp.returncode == 0 and cp.stdout.strip() == "true"
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False


def _build_fetch_argv() -> list[str]:
    return [
        str(_GIT),
        "-c",
        "core.hooksPath=NUL",
        "-c",
        "gc.auto=0",
        f"--git-dir={_OBSERVER}",
        "fetch",
        "--no-tags",
        "--no-recurse-submodules",
        "--no-write-fetch-head",
        "--",
        str(_SOURCE),
        f"+{_SOURCE_REF}:{_LOCAL_REF}",
    ]


def _render_command(argv: list[str]) -> str:
    return " ".join(f'"{x}"' if (" " in x or "\\" in x) else x for x in argv)


def _fetch_contract_exact() -> bool:
    return _render_command(_build_fetch_argv()) == _CFG["remote_transaction"]["fetch_command_exact"]


def _run_fetch() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        _build_fetch_argv(),
        env=_build_git_env(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=_TIMEOUT_SECONDS,
        check=False,
    )


def _namespace_refs() -> list[str] | None:
    try:
        cp = _run_local_git("for-each-ref", "--format=%(refname)", "refs/rpe04")
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    if cp.returncode != 0:
        return None
    return [line.strip() for line in cp.stdout.splitlines() if line.strip()]


def _extract_observed_sha() -> str | None:
    try:
        cp = _run_local_git(
            "for-each-ref",
            "--format=%(refname) %(objectname)",
            _LOCAL_REF,
        )
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    if cp.returncode != 0:
        return None
    lines = [line.strip() for line in cp.stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        return None
    parts = lines[0].split()
    if len(parts) != 2 or parts[0] != _LOCAL_REF:
        return None
    return parts[1]


def _materialized_object_type(sha: str) -> str | None:
    try:
        cp = _run_local_git("cat-file", "-t", sha)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    if cp.returncode != 0:
        return None
    return cp.stdout.strip()


def _materialized_commit(sha: str) -> bool:
    return _materialized_object_type(sha) == "commit"


def _failure(
    code: str,
    attempt_started_at_ns: int | None = None,
    remote_observation_completed_at_ns: int | None = None,
) -> dict:
    return {
        "outcome": "READ_FAILURE",
        "failure_code": code,
        "observed_head": None,
        "attempt_started_at_ns": attempt_started_at_ns,
        "remote_observation_completed_at_ns": remote_observation_completed_at_ns,
        "attempt_completed_at_ns": time.monotonic_ns(),
    }


def observe_once(previous_observed_head):
    """Perform one governed local-bare remote observation attempt."""
    if not _verify_git_executable_identity():
        return _failure("GIT_EXECUTABLE_IDENTITY_MISMATCH")

    ok, code = _verify_physical_object_domain(_OBSERVER)
    if not ok:
        return _failure(code or "PHYSICAL_OBJECT_DOMAIN_UNPROVABLE")

    if not _verify_local_config_allowlist():
        return _failure("LOCAL_CONFIG_NOT_ALLOWLISTED")

    if not _verify_remote_identity():
        return _failure("REMOTE_IDENTITY_UNPROVABLE")

    if not _fetch_contract_exact():
        return _failure("FETCH_CONTRACT_MISMATCH")

    attempt_started_at_ns = time.monotonic_ns()
    try:
        fetch = _run_fetch()
    except subprocess.TimeoutExpired:
        remote_done = time.monotonic_ns()
        return _failure("REMOTE_FETCH_TIMEOUT", attempt_started_at_ns, remote_done)
    except (OSError, ValueError):
        remote_done = time.monotonic_ns()
        return _failure("REMOTE_FETCH_EXECUTION_ERROR", attempt_started_at_ns, remote_done)

    remote_done = time.monotonic_ns()
    if fetch.returncode != 0:
        return _failure("REMOTE_FETCH_FAILED", attempt_started_at_ns, remote_done)

    ok, code = _verify_physical_object_domain(_OBSERVER)
    if not ok:
        return _failure(code or "PHYSICAL_OBJECT_DOMAIN_UNPROVABLE", attempt_started_at_ns, remote_done)

    if not _verify_local_config_allowlist():
        return _failure("LOCAL_CONFIG_NOT_ALLOWLISTED", attempt_started_at_ns, remote_done)

    refs = _namespace_refs()
    if refs != [_LOCAL_REF]:
        return _failure("UNEXPECTED_OBSERVATION_NAMESPACE", attempt_started_at_ns, remote_done)

    observed_head = _extract_observed_sha()
    if type(observed_head) is not str or _SHA40_RE.fullmatch(observed_head) is None:
        return _failure("MALFORMED_OBSERVED_SHA", attempt_started_at_ns, remote_done)

    observed_type = _materialized_object_type(observed_head)
    if observed_type is None:
        return _failure("OBSERVED_SHA_NOT_MATERIALIZED", attempt_started_at_ns, remote_done)
    if observed_type != "commit":
        return _failure("EXACT_OBSERVED_REF_NOT_COMMIT", attempt_started_at_ns, remote_done)

    if not _verify_runtime_bindings():
        return _failure("RUNTIME_BINDING_MISMATCH", attempt_started_at_ns, remote_done)

    if not _verify_git_executable_identity():
        return _failure("GIT_EXECUTABLE_IDENTITY_MISMATCH", attempt_started_at_ns, remote_done)

    ok, code = _verify_physical_object_domain(_OBSERVER)
    if not ok:
        return _failure(code or "PHYSICAL_GIT_DOMAIN_UNPROVABLE", attempt_started_at_ns, remote_done)

    transition = _RPE03.classify_transition(
        _OBSERVER,
        previous_observed_head,
        observed_head,
        str(_GIT),
    )

    event = {
        "outcome": "REMOTE_HEAD_OBSERVED",
        "event_type": "REMOTE_HEAD_OBSERVED",
        "evidence_label": "OBSERVED_REMOTE_TIP",
        "observed_head": observed_head,
        "transition_class": transition,
        "attempt_started_at_ns": attempt_started_at_ns,
        "remote_observation_completed_at_ns": remote_done,
        "attempt_completed_at_ns": 0,
        "blocked": transition == "UNKNOWN",
        "failure_code": "ANCESTRY_UNKNOWN" if transition == "UNKNOWN" else None,
    }
    event["attempt_completed_at_ns"] = time.monotonic_ns()
    return event

~~~

## REBIND + NF2 TEST

PATH: tests/obsidian_projection/test_rpe04_rpe03v02_rebind_nf2_v0_1.py

~~~python
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

~~~

## NF3 FULL PHYSICAL DOMAIN TEST

PATH: tests/obsidian_projection/test_rpe04_nf3_full_physical_domain_v0_1.py

~~~python
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

~~~

## NF2 NF3 MUTATION TEST

PATH: tests/obsidian_projection/test_rpe04_rpe03v02_nf2_nf3_mutation_v0_1.py

~~~python
from __future__ import annotations

import pathlib
import shutil
import types
import unittest
from unittest import mock

from tests.obsidian_projection.test_rpe04_real_remote_observation_adapter_v0_1 import (
    CONTROL,
    LOCAL_REF,
    MODULE,
    OBSERVER,
    PRODUCER,
    git,
    init_fixture,
)


def load_mutant(name: str, replacements):
    source = MODULE.read_text(encoding="utf-8")
    for old, new in replacements:
        if source.count(old) != 1:
            raise AssertionError(f"mutation anchor count != 1: {old!r}")
        source = source.replace(old, new, 1)
    module = types.ModuleType(name)
    module.__file__ = str(MODULE)
    exec(compile(source, str(MODULE), "exec"), module.__dict__)
    return module


class TestRPE04RPE03V02NF2NF3Mutation(unittest.TestCase):
    def setUp(self):
        self.a = init_fixture()

    def tearDown(self):
        shutil.rmtree(CONTROL, ignore_errors=True)

    def test_nf2_peeling_mutant_is_discriminated(self):
        base = load_mutant("rpe04_nf2_base", ())
        mutant = load_mutant(
            "rpe04_nf2_peeling_mutant",
            ((
'''def _extract_observed_sha() -> str | None:
    try:
        cp = _run_local_git(
            "for-each-ref",
            "--format=%(refname) %(objectname)",
            _LOCAL_REF,
        )
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    if cp.returncode != 0:
        return None
    lines = [line.strip() for line in cp.stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        return None
    parts = lines[0].split()
    if len(parts) != 2 or parts[0] != _LOCAL_REF:
        return None
    return parts[1]
''',
'''def _extract_observed_sha() -> str | None:
    try:
        cp = _run_local_git("rev-parse", "--verify", f"{_LOCAL_REF}^{{commit}}")
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    if cp.returncode != 0:
        return None
    return cp.stdout.strip()
'''
            ),),
        )
        git("tag", "-a", "mutation-tag", "-m", "mutation", self.a, cwd=PRODUCER)
        tag_oid = git("rev-parse", "refs/tags/mutation-tag", cwd=PRODUCER).stdout.strip()
        peeled = git("rev-parse", "refs/tags/mutation-tag^{commit}", cwd=PRODUCER).stdout.strip()
        git("fetch", str(PRODUCER / ".git"), f"refs/tags/mutation-tag:{LOCAL_REF}", cwd=OBSERVER)
        self.assertEqual(base._extract_observed_sha(), tag_oid)
        self.assertEqual(mutant._extract_observed_sha(), peeled)
        self.assertNotEqual(tag_oid, peeled)

    def test_nf3_alternates_guard_mutant_is_discriminated(self):
        base = load_mutant("rpe04_nf3_alt_base", ())
        mutant = load_mutant(
            "rpe04_nf3_alt_mutant",
            ((
'''    alternates = repo_path / "objects" / "info" / "alternates"
    if _lexists(alternates):
        return False, "PHYSICAL_GIT_DOMAIN_ALTERNATES_FORBIDDEN"
''',
'''    alternates = repo_path / "objects" / "info" / "alternates"
    if False:
        return False, "PHYSICAL_GIT_DOMAIN_ALTERNATES_FORBIDDEN"
'''
            ),),
        )
        alt = OBSERVER / "objects" / "info" / "alternates"
        alt.write_text(r"C:\outside-object-store" + "\n", encoding="ascii")
        self.assertEqual(
            base._verify_physical_object_domain(OBSERVER),
            (False, "PHYSICAL_GIT_DOMAIN_ALTERNATES_FORBIDDEN"),
        )
        self.assertEqual(mutant._verify_physical_object_domain(OBSERVER), (True, None))

    def test_nf3_recursive_indirection_guard_mutant_is_discriminated(self):
        base = load_mutant("rpe04_nf3_walk_base", ())
        mutant = load_mutant(
            "rpe04_nf3_walk_mutant",
            ((
'''                if _is_indirection(child):
                    return False, "PHYSICAL_GIT_DOMAIN_INDIRECTION"
''',
'''                if False:
                    return False, "PHYSICAL_GIT_DOMAIN_INDIRECTION"
'''
            ),),
        )
        pack = OBSERVER / "objects" / "pack" / "pack-mutant.pack"
        pack.write_bytes(b"fixture")
        original_base = base._is_indirection
        original_mutant = mutant._is_indirection

        def base_indirection(path):
            if pathlib.Path(path) == pack:
                return True
            return original_base(path)

        def mutant_indirection(path):
            if pathlib.Path(path) == pack:
                return True
            return original_mutant(path)

        with mock.patch.object(base, "_is_indirection", side_effect=base_indirection):
            self.assertEqual(
                base._verify_physical_object_domain(OBSERVER),
                (False, "PHYSICAL_GIT_DOMAIN_INDIRECTION"),
            )
        with mock.patch.object(mutant, "_is_indirection", side_effect=mutant_indirection):
            self.assertEqual(mutant._verify_physical_object_domain(OBSERVER), (True, None))


if __name__ == "__main__":
    unittest.main()

~~~

## RUNTIME BINDING TEST

PATH: tests/obsidian_projection/test_rpe04_runtime_binding_hardening_v0_1.py

~~~python
from __future__ import annotations

import importlib.util
import pathlib
import unittest
from unittest import mock

from tests.obsidian_projection.test_rpe04_real_remote_observation_adapter_v0_1 import (
    init_fixture,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_v0_1.py"


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TestRPE04RuntimeBindingHardening(unittest.TestCase):
    def setUp(self):
        self.a = init_fixture()

    def tearDown(self):
        import shutil
        shutil.rmtree(
            pathlib.Path(r"C:\Users\Boulevart\ATDS-CONTROL\RPE04-QUALIFICATION"),
            ignore_errors=True,
        )

    def test_governed_runtime_dependencies_are_raw_sha256_bound(self):
        m = load_module("rpe04_binding_base")
        self.assertTrue(m._verify_runtime_bindings())
        self.assertEqual(
            m._EXPECTED_RUNTIME_SHA256["preregistration"],
            "0c59111fe90b8d80f0c41daf0911d772274eca733c6e68673d484ab8abf2c6ba",
        )
        self.assertEqual(
            m._EXPECTED_RUNTIME_SHA256["schema"],
            "e39dbc4f3bc82f5d5c2181574bdd120ad6d0fca46bcfdf358fac406b572a8861",
        )
        self.assertEqual(
            m._EXPECTED_RUNTIME_SHA256["rpe01_guard"],
            "24b36f5b3c0a02bc6247732fe1fa23d6c0fe30bc2b1629a7c54d4c094a628298",
        )
        self.assertEqual(
            m._EXPECTED_RUNTIME_SHA256["rpe03_classifier"],
            "4b743e187245585f4a4d9c923e316961f2842f96634d04dcac01972a29e60b41",
        )

    def test_runtime_binding_mismatch_fails_closed(self):
        m = load_module("rpe04_binding_mut")
        original = m._sha256_file

        def fake(path):
            if pathlib.Path(path) == m._RPE03_PATH:
                return "0" * 64
            return original(path)

        with mock.patch.object(m, "_raw_sha256_file", side_effect=fake):
            self.assertFalse(m._verify_runtime_bindings())

    def test_physical_domain_is_reverified_after_fetch(self):
        m = load_module("rpe04_binding_physical")
        with mock.patch.object(
            m,
            "_verify_physical_object_domain",
            wraps=m._verify_physical_object_domain,
        ) as wrapped:
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertGreaterEqual(wrapped.call_count, 2)

    def test_git_identity_is_reverified_before_rpe03_classification(self):
        m = load_module("rpe04_binding_git")
        with mock.patch.object(
            m,
            "_verify_git_executable_identity",
            wraps=m._verify_git_executable_identity,
        ) as wrapped:
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertGreaterEqual(wrapped.call_count, 2)

    def test_local_config_is_reverified_before_rpe03_classification(self):
        m = load_module("rpe04_binding_config")
        with mock.patch.object(
            m,
            "_verify_local_config_allowlist",
            wraps=m._verify_local_config_allowlist,
        ) as wrapped:
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertGreaterEqual(wrapped.call_count, 2)


if __name__ == "__main__":
    unittest.main()

~~~

## RUNTIME BINDING TEST REBIND ADJUDICATION

PATH: reports/program/2026-10-05-OBSIDIAN-REAL-P5E-RPE04-RUNTIME-BINDING-TEST-REBIND-ADJUDICATION.md

~~~text
# RPE-04 — RUNTIME BINDING TEST EXPECTATION REBIND — INTERNAL ADJUDICATION

Date: 2026-10-05

The existing runtime-binding hardening test remained bound to the raw SHA-256 of the historical RPE-03 V0.1 classifier:

cbcb996199b06859d257cc194e673a6bc51419890dc0641b42837d3f7cfcb0c3

The authorized RPE-04 closure explicitly requires rebinding to the human-adopted RPE-03 V0.2 classifier.

The active governed dependency is now:

Git blob:
5bbe455418fe1396ee5824379ad7450a1379cbba

Raw SHA-256:
4b743e187245585f4a4d9c923e316961f2842f96634d04dcac01972a29e60b41

Authorized test correction:
- change only the expected RPE-03 runtime dependency raw SHA-256 from V0.1 to V0.2;
- change no failure mode;
- change no runtime-binding requirement;
- change no authority;
- preserve all other historical expectations.

This is an authorized dependency-identity rebind, not a test relaxation.

~~~

## LEGACY RPE04 MUTATION TEST

PATH: tests/obsidian_projection/test_rpe04_real_remote_observation_adapter_mutation_v0_1.py

~~~python
from __future__ import annotations

import os
import pathlib
import subprocess
import tempfile
import types
import unittest
from unittest import mock

from tests.obsidian_projection.test_rpe04_real_remote_observation_adapter_v0_1 import (
    GIT,
    OBSERVER,
    SOURCE,
    SOURCE_REF,
    init_fixture,
    git,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_v0_1.py"


def load_source_module(name: str, replacements=()):
    source = MODULE.read_text(encoding="utf-8")
    for old, new in replacements:
        if source.count(old) != 1:
            raise AssertionError(f"mutation anchor count != 1: {old!r}")
        source = source.replace(old, new, 1)
    module = types.ModuleType(name)
    module.__file__ = str(MODULE)
    exec(compile(source, str(MODULE), "exec"), module.__dict__)
    return module


class TestRPE04MutationSweep(unittest.TestCase):
    def setUp(self):
        self.a = init_fixture()

    def tearDown(self):
        import shutil
        shutil.rmtree(SOURCE.parent, ignore_errors=True)

    def test_mutant_removing_git_hash_binding_is_detected(self):
        m = load_source_module(
            "rpe04_mut_hash",
            ((
                '        if _sha256_file(_GIT) != _CFG["git_executable"]["sha256"]:\n'
                '            return False\n',
                '        if False:\n'
                '            return False\n',
            ),),
        )
        with mock.patch.object(m, "_sha256_file", return_value="0" * 64):
            self.assertTrue(m._verify_git_executable_identity())

    def test_mutant_removing_path_token_binding_is_detected(self):
        m = load_source_module(
            "rpe04_mut_which",
            ((
                '        if resolved_token is None or not _same_path(Path(resolved_token), _GIT):\n'
                '            return False\n',
                '        if False:\n'
                '            return False\n',
            ),),
        )
        with mock.patch.object(m.shutil, "which", return_value=r"C:\evil\git.exe"):
            self.assertTrue(m._verify_git_executable_identity())

    def test_mutant_preserving_inherited_git_environment_is_detected(self):
        base = load_source_module("rpe04_base_env")
        m = load_source_module(
            "rpe04_mut_env",
            ((
                '    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\n',
                '    env = dict(os.environ)\n',
            ),),
        )
        with mock.patch.dict(os.environ, {"GIT_DIR": "evil"}, clear=False):
            self.assertNotIn("GIT_DIR", base._build_git_env())
            self.assertEqual(m._build_git_env()["GIT_DIR"], "evil")

    def test_mutant_bypassing_local_config_allowlist_is_detected(self):
        m = load_source_module(
            "rpe04_mut_config",
            ((
                '    return len(observed) == len(expected) and set(observed) == set(expected)\n',
                '    return True\n',
            ),),
        )
        git(f"--git-dir={OBSERVER}", "config", "--local", "include.path", r"C:\evil-rpe04.cfg")
        out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")

    def test_mutant_ignoring_unexpected_namespace_ref_is_detected(self):
        m = load_source_module(
            "rpe04_mut_namespace",
            ((
                '    if refs != [_LOCAL_REF]:\n',
                '    if False:\n',
            ),),
        )
        first = m.observe_once(None)
        self.assertEqual(first["outcome"], "REMOTE_HEAD_OBSERVED")
        git(f"--git-dir={OBSERVER}", "update-ref", "refs/rpe04/extra", self.a)
        out = m.observe_once(self.a)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")

    def test_mutant_skipping_materialization_proof_is_detected(self):
        m = load_source_module(
            "rpe04_mut_materialized",
            ((
                '    observed_type = _materialized_object_type(observed_head)\n'
                '    if observed_type is None:\n'
                '        return _failure("OBSERVED_SHA_NOT_MATERIALIZED", attempt_started_at_ns, remote_done)\n'
                '    if observed_type != "commit":\n'
                '        return _failure("EXACT_OBSERVED_REF_NOT_COMMIT", attempt_started_at_ns, remote_done)\n',
                '    observed_type = "commit"\n',
            ),),
        )
        with mock.patch.object(m, "_extract_observed_sha", return_value="f" * 40):
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertEqual(out["transition_class"], "UNKNOWN")

    def test_mutant_laundering_unknown_as_fast_forward_is_detected(self):
        m = load_source_module(
            "rpe04_mut_transition",
            ((
                '    transition = _RPE03.classify_transition(\n'
                '        _OBSERVER,\n'
                '        previous_observed_head,\n'
                '        observed_head,\n'
                '        str(_GIT),\n'
                '    )\n',
                '    transition = "FAST_FORWARD"\n',
            ),),
        )
        out = m.observe_once("f" * 40)
        self.assertEqual(out["transition_class"], "FAST_FORWARD")
        self.assertFalse(out["blocked"])

    def test_mutant_dropping_no_write_fetch_head_breaks_exact_contract(self):
        m = load_source_module(
            "rpe04_mut_fetchhead",
            (('        "--no-write-fetch-head",\n', ''),),
        )
        self.assertNotIn("--no-write-fetch-head", m._build_fetch_argv())
        self.assertFalse(m._fetch_contract_exact())

    def test_mutant_dropping_local_plus_breaks_exact_contract(self):
        m = load_source_module(
            "rpe04_mut_plus",
            ((
                '        f"+{_SOURCE_REF}:{_LOCAL_REF}",\n',
                '        f"{_SOURCE_REF}:{_LOCAL_REF}",\n',
            ),),
        )
        self.assertFalse(m._fetch_contract_exact())

    def test_mutant_accepting_physical_escape_is_detected(self):
        m = load_source_module(
            "rpe04_mut_physical",
            (
                (
                    'def _is_indirection(path: Path) -> bool:\n'
                    '    try:\n',
                    'def _is_indirection(path: Path) -> bool:\n'
                    '    return False\n'
                    '    try:\n',
                ),
                (
                    'def _inside_root(path: Path, root: Path) -> bool:\n'
                    '    return path == root or root in path.parents\n',
                    'def _inside_root(path: Path, root: Path) -> bool:\n'
                    '    return True\n',
                ),
            ),
        )
        with tempfile.TemporaryDirectory(prefix="rpe04-mut-link-") as td:
            td = pathlib.Path(td)
            fake = td / "fake.git"
            target = td / "outside-objects"
            git("init", "--bare", str(fake))
            target.mkdir()
            (target / "pack").mkdir()
            (target / "info").mkdir()
            subprocess.run(["cmd.exe", "/c", "rmdir", "/s", "/q", str(fake / "objects")], check=True)
            link = fake / "objects"
            made = False
            try:
                os.symlink(target, link, target_is_directory=True)
                made = True
            except (OSError, NotImplementedError):
                cp = subprocess.run(
                    ["cmd.exe", "/c", "mklink", "/J", str(link), str(target)],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                made = cp.returncode == 0
            if not made:
                self.skipTest("platform cannot create symlink or junction")
            ok, code = m._verify_physical_object_domain(fake)
            self.assertTrue(ok, code)

    def test_mutant_accepting_uppercase_sha_is_detected(self):
        m = load_source_module(
            "rpe04_mut_sha",
            ((
                '    if type(observed_head) is not str or _SHA40_RE.fullmatch(observed_head) is None:\n',
                '    if False:\n',
            ),),
        )
        with mock.patch.object(m, "_extract_observed_sha", return_value=self.a.upper()):
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")


if __name__ == "__main__":
    unittest.main()

~~~

## FINAL TEST EXECUTION EVIDENCE

PATH: reports/program/2026-10-05-OBSIDIAN-REAL-P5E-RPE04-RPE03V02-NF2-NF3-FINAL-TEST-EVIDENCE.md

~~~text
# RPE-04 — RPE-03 V0.2 REBIND + NF-2 + NF-3 — FINAL TEST EXECUTION EVIDENCE

Date: 2026-10-05

## Execution protocol

Tests were executed locally on Windows through a bounded detached runner under:

C:\Users\Boulevart\ATDS-CONTROL\BOUNDED-TEST-RUNNER

The runner:
- launches each test family in a separate process;
- writes stdout/stderr and completion state to disk;
- imposes a Windows-side hard timeout;
- does not rely on the chat transport remaining open;
- avoids overlapping ATDS test executions.

No GitHub polling or external-network qualification occurred.

## Targeted closure evidence

### RPE-03 V0.2 rebind + NF-2

Suite:
tests.obsidian_projection.test_rpe04_rpe03v02_rebind_nf2_v0_1

Result:
5 / 5 PASS

This covers:
- exact binding to the human-adopted RPE-03 V0.2 classifier;
- governed absolute Git path handoff;
- exact observation-ref identity without peeling;
- annotated-tag laundering rejection;
- normal commit-ref success.

### NF-3 full physical Git-domain containment

Suite:
tests.obsidian_projection.test_rpe04_nf3_full_physical_domain_v0_1

Result:
7 / 7 PASS

This covers:
- normal bare repository acceptance;
- recursive indirection rejection;
- refs and refs/rpe04 containment;
- config / HEAD / packed-refs containment;
- alternates rejection;
- pack/index-level indirection where representable;
- post-fetch containment revalidation before positive authority.

### Runtime-binding hardening after RPE-03 V0.2 rebind

Suite:
tests.obsidian_projection.test_rpe04_runtime_binding_hardening_v0_1

Result:
5 / 5 PASS

The only historical-test correction was the expected raw SHA-256 rebind from the adopted RPE-03 V0.1 runtime dependency to the adopted RPE-03 V0.2 runtime dependency. The security requirement and failure mode were unchanged.

### NF-2 / NF-3 mutation discrimination

Suite:
tests.obsidian_projection.test_rpe04_rpe03v02_nf2_nf3_mutation_v0_1

Result:
3 / 3 PASS

Mutations discriminate:
- reintroduction of observed-tip peeling;
- removal of alternates rejection;
- removal of recursive physical-indirection rejection.

## RPE-04 dedicated regression

Discovery pattern:
test_rpe04*.py

Result:
55 / 55 PASS

This includes the current RPE-04 adapter, legacy mutation surface, runtime-binding hardening, RPE-03 V0.2 rebind, NF-2, NF-3 and final targeted mutation coverage.

## Protected predecessor regressions

### RPE-03 final qualified surface

An initial broad discovery of all test_rpe03*.py files executed 62 tests and produced one error in:

test_rpe03_v02_bf1_prime_executable_identity_closure_v0_1.py

That file is a historical intermediate BF-1 PRIME closure test whose direct _run_git expectation predates the final canonical-path hardening. It is not part of the final 59-test qualified RPE-03 V0.2 surface.

The final qualified surface was reconstructed exactly as:
- every current RPE-03 qualified test module;
- excluding the historical 4-test intermediate closure file above;
- including the 1-test RPE-04 call-site compatibility harness.

Arithmetic:
62 - 4 + 1 = 59

Exact final replay result:
59 / 59 PASS

No RPE-03 file was modified during this regression.

### RPE-02

Discovery pattern:
test_rpe02*.py

Result:
51 / 51 PASS

### RPE-01

Discovery pattern:
test_rpe01*.py

Result:
46 / 46 PASS

### P5-E

Discovery pattern:
test_p5e*.py

Result:
67 / 67 PASS

## Protected identity checks

RPE-01 governed schema guard:
26f977961d72a062199d71ffd628d5a5cc047887

RPE-02 real-time model:
31db5d944a25e54db81bd901a087cdc2039925ad

RPE-03 V0.1 historical classifier:
145b3112fd9309cc34d95a62c091cb6a6bc3bb11

RPE-03 V0.2 human-adopted classifier:
5bbe455418fe1396ee5824379ad7450a1379cbba

P5-E contract:
43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9

P5-E synthetic timing model:
c0f16baa151c1466e30ba5778f1fca8184cd4aac

P5-D4 runtime:
1825e53d195ba2a63b5b646a5b78eb77939b94b5

All match the protected expected identities.

## Final RPE-04 candidate

Implementation Git blob:
e188414cd433f839d5efbe5d28840d7acf4938d5

Implementation raw SHA-256:
1300e60a5cd353557cc16779a372979b436fcacfeb082435cd749987342d1638

RPE-03 V0.2 classifier raw SHA-256:
4b743e187245585f4a4d9c923e316961f2842f96634d04dcac01972a29e60b41

Closure preregistration raw SHA-256:
4c6c156c2bde72ed83b360a3ddccaf97a46b55b45cd107c85e32d998ef95cf11

## Claim boundary

This evidence supports only the local-only RPE-04 closure candidate.

It does not qualify:
- production GitHub polling;
- production remote observation;
- RPE-02 failure-event handoff NF-4;
- RPE-05;
- RPE-06;
- REAL P5-E;
- promotion/publication;
- Vault/CURRENT;
- persistent services.

RPE-04 human adoption remains pending external review and a separate human decision.

~~~

## FINAL QUALIFICATION

PATH: tools/obsidian_projection/rpe04_rpe03v02_nf2_nf3_final_qualification_v0_1.json

~~~json
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE04_RPE03V02_NF2_NF3_FINAL_QUALIFICATION_V0_1",
  "status": "QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW",
  "date": "2026-10-05",
  "branch": "feat/obsidian-projection-rpe04-real-remote-observation-adapter-v0.1",
  "lineage": {
    "prior_rpe04_external_review_adjudication_head": "ec41c8a79defad9f343ee5c93b55c0c776f690fe",
    "adopted_rpe03_v02_dependency_import_head": "017fca56001c2181d6aafcce153283b0562adcb1",
    "closure_preregistration_head": "1ba14c2d89904c51b6766a686f4249cca3b6b7ee",
    "targeted_red_head": "629e3f08134ae5592454e0628c311c1fea358934",
    "minimal_implementation_head": "535277f59795d3904b8583c32746e4d125f828be",
    "final_test_closure_head": "21f4eb820b501d585e96d07df84ccea5982fd5c7",
    "legacy_mutation_rebind_head": "9aeb2764565f8cd65a6fcbf39ca5f7fe40c56b5b"
  },
  "exact_identities": {
    "rpe03_v02_adoption_commit": "f266121e6a65daa3bf19480412f1addd299b8172",
    "rpe03_v02_adoption_blob": "73b5a951a2ed9ed42cb827b4fadc555fc3dd7a7d",
    "rpe03_v02_classifier_blob": "5bbe455418fe1396ee5824379ad7450a1379cbba",
    "rpe03_v02_qualification_blob": "688a2abcc2caa2edeed5e67f2d3c38b293bcc238",
    "final_rpe04_implementation_blob": "e188414cd433f839d5efbe5d28840d7acf4938d5",
    "closure_preregistration_blob": "6f19ca7da0a791801f07b20d1645354666a6ffba",
    "closure_preregistration_schema_blob": "ba35ddaa201e8bc11703a07efe794aaab2d3ab8c",
    "targeted_red_report_blob": "d160048f5e8594b8647d33393438f4523a3ef7a2",
    "rebind_nf2_test_blob": "49540da4a64c25febe0bec26edbf0ce768193551",
    "nf3_test_blob": "eadddb42e5806c57d95737965ba501dbe427722c",
    "nf2_nf3_mutation_test_blob": "dc2701d9722e626bb520b30e8db15d3308818ff5",
    "runtime_binding_test_blob": "b8089430ccf320c95bb9b01eb2b4cef28bbe866c",
    "legacy_rpe04_mutation_test_blob": "1b8e18e20be2dda2ed2d792730b0ab03f4b47845",
    "final_test_evidence_blob": "0dab2fe5904acbf698f6c4eae29e4eb31c532b67",
    "rpe01_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887",
    "rpe02_model_blob": "31db5d944a25e54db81bd901a087cdc2039925ad",
    "rpe03_v01_classifier_blob": "145b3112fd9309cc34d95a62c091cb6a6bc3bb11",
    "p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
    "p5e_synthetic_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5"
  },
  "raw_sha256": {
    "final_rpe04_implementation": "1300e60a5cd353557cc16779a372979b436fcacfeb082435cd749987342d1638",
    "adopted_rpe03_v02_classifier": "4b743e187245585f4a4d9c923e316961f2842f96634d04dcac01972a29e60b41",
    "closure_preregistration": "4c6c156c2bde72ed83b360a3ddccaf97a46b55b45cd107c85e32d998ef95cf11",
    "governed_git_executable": "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5"
  },
  "candidate_closures": {
    "bf1": "CLOSED_BY_EXACT_RPE03_V0_2_REBIND",
    "nf2": "CLOSED",
    "nf3": "CLOSED",
    "nf4": "CARRIED_TO_RPE05"
  },
  "rpe03_v02_rebind": {
    "classifier_blob": "5bbe455418fe1396ee5824379ad7450a1379cbba",
    "governed_git_absolute_path": "C:\\Program Files\\Git\\cmd\\git.exe",
    "governed_git_sha256": "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5",
    "governed_git_version": "git version 2.54.0.windows.1",
    "caller_creates_executable_authority": false
  },
  "nf2_exact_observed_tip": {
    "exact_local_ref": "refs/rpe04/observed",
    "extraction": "EXACT_REF_OBJECT_ID_WITHOUT_PEELING",
    "exact_object_type_required": "commit",
    "annotated_tag_behavior": "READ_FAILURE_EXACT_OBSERVED_REF_NOT_COMMIT",
    "peeled_commit_must_not_receive_observed_tip_authority": true,
    "observed_tip_format": "LOWERCASE_40_HEX"
  },
  "nf3_full_physical_domain": {
    "recursive_indirection_rejection": true,
    "required_directories": [
      "objects",
      "objects/info",
      "objects/pack",
      "refs"
    ],
    "authority_paths": [
      "HEAD",
      "config",
      "packed-refs",
      "refs",
      "refs/rpe04",
      "objects",
      "objects/info",
      "objects/pack",
      "objects/info/alternates"
    ],
    "reject_symlink": true,
    "reject_junction": true,
    "reject_reparse_point": true,
    "reject_uncontrolled_alternates": true,
    "resolved_paths_must_remain_under_governed_root": true,
    "check_before_fetch": true,
    "check_after_fetch_before_tip_acceptance": true,
    "check_before_rpe03_classification": true
  },
  "evidence": {
    "rebind_nf2_targeted": "5/5 PASS",
    "nf3_targeted": "7/7 PASS",
    "runtime_binding_hardening": "5/5 PASS",
    "nf2_nf3_mutations": "3/3 PASS",
    "rpe04_discovery": "55/55 PASS",
    "rpe03_final_qualified_surface": "59/59 PASS",
    "rpe02_protected_regression": "51/51 PASS",
    "rpe01_protected_regression": "46/46 PASS",
    "p5e_protected_regression": "67/67 PASS",
    "protected_blob_checks": "PASS"
  },
  "semantic_immutability": {
    "one_governed_fetch_transaction_per_attempt": true,
    "no_ls_remote_plus_independent_fetch": true,
    "exact_source_ref": true,
    "isolated_local_observation_ref": true,
    "no_tag_fetch": true,
    "no_submodule_recursion": true,
    "no_fetch_head_write": true,
    "no_caller_transition_authority": true,
    "no_caller_containment_authority": true,
    "unknown_is_blocked": true,
    "no_intermediate_commit_injection": true
  },
  "qualification_scope": {
    "local_only": true,
    "github_polling_qualified": false,
    "production_remote_observation_qualified": false,
    "real_60_second_sla_qualified": false,
    "rpe02_failure_handoff_nf4_closed": false,
    "rpe04_human_adopted": false,
    "rpe05_opened": false,
    "rpe06_opened": false,
    "real_p5e_opened": false
  },
  "next_gate": "EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADJUDICATION",
  "stop": true
}

~~~

## FINAL QUALIFICATION SCHEMA

PATH: tools/obsidian_projection/rpe04_rpe03v02_nf2_nf3_final_qualification_v0_1_schema_v0_1.json

~~~json
{
  "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
  "artifact_role": "RPE04_RPE03V02_NF2_NF3_FINAL_QUALIFICATION",
  "root": {
    "kind": "object",
    "fields": {
      "schema": {
        "kind": "string",
        "const": "ATDS_OBSIDIAN_REAL_P5E_RPE04_RPE03V02_NF2_NF3_FINAL_QUALIFICATION_V0_1"
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
        "const": "feat/obsidian-projection-rpe04-real-remote-observation-adapter-v0.1"
      },
      "lineage": {
        "kind": "object",
        "fields": {
          "prior_rpe04_external_review_adjudication_head": {
            "kind": "string",
            "const": "ec41c8a79defad9f343ee5c93b55c0c776f690fe"
          },
          "adopted_rpe03_v02_dependency_import_head": {
            "kind": "string",
            "const": "017fca56001c2181d6aafcce153283b0562adcb1"
          },
          "closure_preregistration_head": {
            "kind": "string",
            "const": "1ba14c2d89904c51b6766a686f4249cca3b6b7ee"
          },
          "targeted_red_head": {
            "kind": "string",
            "const": "629e3f08134ae5592454e0628c311c1fea358934"
          },
          "minimal_implementation_head": {
            "kind": "string",
            "const": "535277f59795d3904b8583c32746e4d125f828be"
          },
          "final_test_closure_head": {
            "kind": "string",
            "const": "21f4eb820b501d585e96d07df84ccea5982fd5c7"
          },
          "legacy_mutation_rebind_head": {
            "kind": "string",
            "const": "9aeb2764565f8cd65a6fcbf39ca5f7fe40c56b5b"
          }
        }
      },
      "exact_identities": {
        "kind": "object",
        "fields": {
          "rpe03_v02_adoption_commit": {
            "kind": "string",
            "const": "f266121e6a65daa3bf19480412f1addd299b8172"
          },
          "rpe03_v02_adoption_blob": {
            "kind": "string",
            "const": "73b5a951a2ed9ed42cb827b4fadc555fc3dd7a7d"
          },
          "rpe03_v02_classifier_blob": {
            "kind": "string",
            "const": "5bbe455418fe1396ee5824379ad7450a1379cbba"
          },
          "rpe03_v02_qualification_blob": {
            "kind": "string",
            "const": "688a2abcc2caa2edeed5e67f2d3c38b293bcc238"
          },
          "final_rpe04_implementation_blob": {
            "kind": "string",
            "const": "e188414cd433f839d5efbe5d28840d7acf4938d5"
          },
          "closure_preregistration_blob": {
            "kind": "string",
            "const": "6f19ca7da0a791801f07b20d1645354666a6ffba"
          },
          "closure_preregistration_schema_blob": {
            "kind": "string",
            "const": "ba35ddaa201e8bc11703a07efe794aaab2d3ab8c"
          },
          "targeted_red_report_blob": {
            "kind": "string",
            "const": "d160048f5e8594b8647d33393438f4523a3ef7a2"
          },
          "rebind_nf2_test_blob": {
            "kind": "string",
            "const": "49540da4a64c25febe0bec26edbf0ce768193551"
          },
          "nf3_test_blob": {
            "kind": "string",
            "const": "eadddb42e5806c57d95737965ba501dbe427722c"
          },
          "nf2_nf3_mutation_test_blob": {
            "kind": "string",
            "const": "dc2701d9722e626bb520b30e8db15d3308818ff5"
          },
          "runtime_binding_test_blob": {
            "kind": "string",
            "const": "b8089430ccf320c95bb9b01eb2b4cef28bbe866c"
          },
          "legacy_rpe04_mutation_test_blob": {
            "kind": "string",
            "const": "1b8e18e20be2dda2ed2d792730b0ab03f4b47845"
          },
          "final_test_evidence_blob": {
            "kind": "string",
            "const": "0dab2fe5904acbf698f6c4eae29e4eb31c532b67"
          },
          "rpe01_guard_blob": {
            "kind": "string",
            "const": "26f977961d72a062199d71ffd628d5a5cc047887"
          },
          "rpe02_model_blob": {
            "kind": "string",
            "const": "31db5d944a25e54db81bd901a087cdc2039925ad"
          },
          "rpe03_v01_classifier_blob": {
            "kind": "string",
            "const": "145b3112fd9309cc34d95a62c091cb6a6bc3bb11"
          },
          "p5e_contract_blob": {
            "kind": "string",
            "const": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9"
          },
          "p5e_synthetic_model_blob": {
            "kind": "string",
            "const": "c0f16baa151c1466e30ba5778f1fca8184cd4aac"
          },
          "p5d4_runtime_blob": {
            "kind": "string",
            "const": "1825e53d195ba2a63b5b646a5b78eb77939b94b5"
          }
        }
      },
      "raw_sha256": {
        "kind": "object",
        "fields": {
          "final_rpe04_implementation": {
            "kind": "string",
            "const": "1300e60a5cd353557cc16779a372979b436fcacfeb082435cd749987342d1638"
          },
          "adopted_rpe03_v02_classifier": {
            "kind": "string",
            "const": "4b743e187245585f4a4d9c923e316961f2842f96634d04dcac01972a29e60b41"
          },
          "closure_preregistration": {
            "kind": "string",
            "const": "4c6c156c2bde72ed83b360a3ddccaf97a46b55b45cd107c85e32d998ef95cf11"
          },
          "governed_git_executable": {
            "kind": "string",
            "const": "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5"
          }
        }
      },
      "candidate_closures": {
        "kind": "object",
        "fields": {
          "bf1": {
            "kind": "string",
            "const": "CLOSED_BY_EXACT_RPE03_V0_2_REBIND"
          },
          "nf2": {
            "kind": "string",
            "const": "CLOSED"
          },
          "nf3": {
            "kind": "string",
            "const": "CLOSED"
          },
          "nf4": {
            "kind": "string",
            "const": "CARRIED_TO_RPE05"
          }
        }
      },
      "rpe03_v02_rebind": {
        "kind": "object",
        "fields": {
          "classifier_blob": {
            "kind": "string",
            "const": "5bbe455418fe1396ee5824379ad7450a1379cbba"
          },
          "governed_git_absolute_path": {
            "kind": "string",
            "const": "C:\\Program Files\\Git\\cmd\\git.exe"
          },
          "governed_git_sha256": {
            "kind": "string",
            "const": "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5"
          },
          "governed_git_version": {
            "kind": "string",
            "const": "git version 2.54.0.windows.1"
          },
          "caller_creates_executable_authority": {
            "kind": "boolean",
            "const": false
          }
        }
      },
      "nf2_exact_observed_tip": {
        "kind": "object",
        "fields": {
          "exact_local_ref": {
            "kind": "string",
            "const": "refs/rpe04/observed"
          },
          "extraction": {
            "kind": "string",
            "const": "EXACT_REF_OBJECT_ID_WITHOUT_PEELING"
          },
          "exact_object_type_required": {
            "kind": "string",
            "const": "commit"
          },
          "annotated_tag_behavior": {
            "kind": "string",
            "const": "READ_FAILURE_EXACT_OBSERVED_REF_NOT_COMMIT"
          },
          "peeled_commit_must_not_receive_observed_tip_authority": {
            "kind": "boolean",
            "const": true
          },
          "observed_tip_format": {
            "kind": "string",
            "const": "LOWERCASE_40_HEX"
          }
        }
      },
      "nf3_full_physical_domain": {
        "kind": "object",
        "fields": {
          "recursive_indirection_rejection": {
            "kind": "boolean",
            "const": true
          },
          "required_directories": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 4,
            "max_items": 4,
            "unique": true,
            "ordered_const": [
              "objects",
              "objects/info",
              "objects/pack",
              "refs"
            ],
            "allowed_values": [
              "objects",
              "objects/info",
              "objects/pack",
              "refs"
            ]
          },
          "authority_paths": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 9,
            "max_items": 9,
            "unique": true,
            "ordered_const": [
              "HEAD",
              "config",
              "packed-refs",
              "refs",
              "refs/rpe04",
              "objects",
              "objects/info",
              "objects/pack",
              "objects/info/alternates"
            ],
            "allowed_values": [
              "HEAD",
              "config",
              "packed-refs",
              "refs",
              "refs/rpe04",
              "objects",
              "objects/info",
              "objects/pack",
              "objects/info/alternates"
            ]
          },
          "reject_symlink": {
            "kind": "boolean",
            "const": true
          },
          "reject_junction": {
            "kind": "boolean",
            "const": true
          },
          "reject_reparse_point": {
            "kind": "boolean",
            "const": true
          },
          "reject_uncontrolled_alternates": {
            "kind": "boolean",
            "const": true
          },
          "resolved_paths_must_remain_under_governed_root": {
            "kind": "boolean",
            "const": true
          },
          "check_before_fetch": {
            "kind": "boolean",
            "const": true
          },
          "check_after_fetch_before_tip_acceptance": {
            "kind": "boolean",
            "const": true
          },
          "check_before_rpe03_classification": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "evidence": {
        "kind": "object",
        "fields": {
          "rebind_nf2_targeted": {
            "kind": "string",
            "const": "5/5 PASS"
          },
          "nf3_targeted": {
            "kind": "string",
            "const": "7/7 PASS"
          },
          "runtime_binding_hardening": {
            "kind": "string",
            "const": "5/5 PASS"
          },
          "nf2_nf3_mutations": {
            "kind": "string",
            "const": "3/3 PASS"
          },
          "rpe04_discovery": {
            "kind": "string",
            "const": "55/55 PASS"
          },
          "rpe03_final_qualified_surface": {
            "kind": "string",
            "const": "59/59 PASS"
          },
          "rpe02_protected_regression": {
            "kind": "string",
            "const": "51/51 PASS"
          },
          "rpe01_protected_regression": {
            "kind": "string",
            "const": "46/46 PASS"
          },
          "p5e_protected_regression": {
            "kind": "string",
            "const": "67/67 PASS"
          },
          "protected_blob_checks": {
            "kind": "string",
            "const": "PASS"
          }
        }
      },
      "semantic_immutability": {
        "kind": "object",
        "fields": {
          "one_governed_fetch_transaction_per_attempt": {
            "kind": "boolean",
            "const": true
          },
          "no_ls_remote_plus_independent_fetch": {
            "kind": "boolean",
            "const": true
          },
          "exact_source_ref": {
            "kind": "boolean",
            "const": true
          },
          "isolated_local_observation_ref": {
            "kind": "boolean",
            "const": true
          },
          "no_tag_fetch": {
            "kind": "boolean",
            "const": true
          },
          "no_submodule_recursion": {
            "kind": "boolean",
            "const": true
          },
          "no_fetch_head_write": {
            "kind": "boolean",
            "const": true
          },
          "no_caller_transition_authority": {
            "kind": "boolean",
            "const": true
          },
          "no_caller_containment_authority": {
            "kind": "boolean",
            "const": true
          },
          "unknown_is_blocked": {
            "kind": "boolean",
            "const": true
          },
          "no_intermediate_commit_injection": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "qualification_scope": {
        "kind": "object",
        "fields": {
          "local_only": {
            "kind": "boolean",
            "const": true
          },
          "github_polling_qualified": {
            "kind": "boolean",
            "const": false
          },
          "production_remote_observation_qualified": {
            "kind": "boolean",
            "const": false
          },
          "real_60_second_sla_qualified": {
            "kind": "boolean",
            "const": false
          },
          "rpe02_failure_handoff_nf4_closed": {
            "kind": "boolean",
            "const": false
          },
          "rpe04_human_adopted": {
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
        "const": "EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADJUDICATION"
      },
      "stop": {
        "kind": "boolean",
        "const": true
      }
    }
  }
}

~~~

## FINAL QUALIFICATION REPORT

PATH: reports/program/2026-10-05-OBSIDIAN-REAL-P5E-RPE04-RPE03V02-NF2-NF3-FINAL-QUALIFICATION.md

~~~text
# RPE-04 — RPE-03 V0.2 REBIND + NF-2 + NF-3 — FINAL QUALIFICATION

Date: 2026-10-05

## Result

RPE04_REMOTE_OBSERVATION_ADAPTER
= QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW

RPE-04 HUMAN ADOPTION
= PENDING

## Candidate closures

BF-1
= CLOSED_BY_EXACT_RPE03_V0.2_REBIND

NF-2
= CLOSED

NF-3
= CLOSED

NF-4
= CARRIED_TO_RPE-05

## Exact RPE-03 V0.2 rebind

Human-adopted RPE-03 V0.2 adoption commit:
f266121e6a65daa3bf19480412f1addd299b8172

Adoption blob:
73b5a951a2ed9ed42cb827b4fadc555fc3dd7a7d

Classifier blob:
5bbe455418fe1396ee5824379ad7450a1379cbba

Classifier raw SHA-256:
4b743e187245585f4a4d9c923e316961f2842f96634d04dcac01972a29e60b41

RPE-04 supplies only the governed absolute Git executable:
C:\Program Files\Git\cmd\git.exe

## NF-2 exact observed tip

The candidate no longer uses commit peeling to establish remote-tip authority.

The observed identity is taken from the exact isolated local observation ref without dereference.

The exact referenced object must itself be a commit.

Therefore:

REF -> commit C
=> C may become OBSERVED_REMOTE_TIP

REF -> annotated tag T -> commit C
=> T is not a commit
=> fail closed
=> C does not receive OBSERVED_REMOTE_TIP authority

## NF-3 full physical-domain containment

The candidate recursively checks the governed local bare observation domain and rejects filesystem indirection across authority-bearing and fetch-written surfaces.

The closure includes:
- repository root;
- objects;
- objects/info;
- objects/pack;
- refs;
- refs/rpe04;
- HEAD;
- config;
- packed-refs;
- objects/info/alternates;
- existing pack/index and loose-ref descendants.

Symlink, junction, reparse-point or equivalent indirection is blocked.

Uncontrolled alternates are blocked.

Material conditions are checked before fetch and rechecked after fetch before exact-tip acceptance and before RPE-03 classification.

## Final evidence

RPE-03 V0.2 rebind + NF-2 targeted:
5/5 PASS

NF-3 targeted:
7/7 PASS

Runtime-binding hardening:
5/5 PASS

NF-2/NF-3 mutation discrimination:
3/3 PASS

RPE-04 dedicated discovery:
55/55 PASS

RPE-03 final qualified protected surface:
59/59 PASS

RPE-02 protected regression:
51/51 PASS

RPE-01 protected regression:
46/46 PASS

P5-E protected regression:
67/67 PASS

Protected blob checks:
PASS

Detailed execution evidence:
reports/program/2026-10-05-OBSIDIAN-REAL-P5E-RPE04-RPE03V02-NF2-NF3-FINAL-TEST-EVIDENCE.md

## Final candidate identity

RPE-04 implementation Git blob:
e188414cd433f839d5efbe5d28840d7acf4938d5

RPE-04 implementation raw SHA-256:
1300e60a5cd353557cc16779a372979b436fcacfeb082435cd749987342d1638

Closure preregistration blob:
6f19ca7da0a791801f07b20d1645354666a6ffba

Closure preregistration schema blob:
ba35ddaa201e8bc11703a07efe794aaab2d3ab8c

## Protected predecessors

RPE-01 guard:
26f977961d72a062199d71ffd628d5a5cc047887

RPE-02 model:
31db5d944a25e54db81bd901a087cdc2039925ad

RPE-03 V0.1 historical classifier:
145b3112fd9309cc34d95a62c091cb6a6bc3bb11

RPE-03 V0.2 adopted classifier:
5bbe455418fe1396ee5824379ad7450a1379cbba

P5-E contract:
43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9

P5-E synthetic model:
c0f16baa151c1466e30ba5778f1fca8184cd4aac

P5-D4 runtime:
1825e53d195ba2a63b5b646a5b78eb77939b94b5

All remain exact.

## Claim boundary

This qualification is local-only.

It does not qualify:
- GitHub polling;
- production remote observation;
- real 60-second SLA;
- NF-4 failure-event handoff to RPE-02;
- RPE-05;
- RPE-06;
- REAL P5-E;
- promotion/publication;
- Vault/CURRENT;
- daemon, Scheduled Task, Windows Service or startup activation.

Next gate:
EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADJUDICATION

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

## RPE02 REAL-TIME MODEL

PATH: tools/obsidian_projection/rpe02_real_time_model_v0_1.py

~~~python
"""RPE-02 V0.1: nanosecond-native real-time representation.

Pure timing qualification except capture_monotonic_clock_capability(), which records
host clock capability/evidence. No network, CLI, environment, filesystem config, or
P5-D4/Vault mutation authority exists in this module.
"""

from __future__ import annotations

import platform
import re
import sys
import time
from typing import Any, Mapping, Sequence


NANOSECONDS_PER_SECOND = 1_000_000_000
POLL_INTERVAL_NS = 30 * NANOSECONDS_PER_SECOND
DETECTION_LATENCY_BOUND_NS = 60 * NANOSECONDS_PER_SECOND
_SHA40_RE = re.compile(r"[0-9a-f]{40}\Z")
_ALLOWED_OUTCOMES = {"READ_FAILURE", "REMOTE_HEAD_OBSERVED"}


class RPE02TimingError(ValueError):
    """Invalid RPE-02 timing evidence or plan."""


def _strict_int(name: str, value: object) -> int:
    if type(value) is not int:
        raise RPE02TimingError(f"{name} must be an integer nanosecond value")
    return value


def _strict_sha40(name: str, value: object) -> str:
    if type(value) is not str or _SHA40_RE.fullmatch(value) is None:
        raise RPE02TimingError(f"{name} must be lowercase 40-hex")
    return value


def make_real_time_plan(*, schedule_origin_ns: int) -> dict[str, Any]:
    origin = _strict_int("schedule_origin_ns", schedule_origin_ns)
    return {
        "schema": "ATDS_RPE02_REAL_TIME_PLAN_V0_1",
        "normative_unit": "INTEGER_MONOTONIC_NANOSECONDS",
        "schedule_origin_ns": origin,
        "poll_interval_ns": POLL_INTERVAL_NS,
        "detection_latency_bound_ns": DETECTION_LATENCY_BOUND_NS,
        "synthetic_reference_role": "IMMUTABLE_SEMANTIC_AND_EXACT_GRID_PARITY_REFERENCE",
    }


def first_fixed_rate_slot_at_or_after_ns(
    timestamp_ns: int,
    poll_interval_ns: int,
    schedule_origin_ns: int,
) -> int:
    timestamp = _strict_int("timestamp_ns", timestamp_ns)
    interval = _strict_int("poll_interval_ns", poll_interval_ns)
    origin = _strict_int("schedule_origin_ns", schedule_origin_ns)
    if interval <= 0:
        raise RPE02TimingError("poll_interval_ns must be positive")
    if timestamp <= origin:
        return origin + interval
    delta = timestamp - origin
    q, r = divmod(delta, interval)
    return origin + (q if r == 0 else q + 1) * interval


def _blocked(code: str, **extra: Any) -> dict[str, Any]:
    out: dict[str, Any] = {
        "status": "BLOCKED_REQUIRES_ADJUDICATION",
        "failure_code": code,
        "detection_latency_ns": None,
    }
    out.update(extra)
    return out


def _validate_plan(plan: Mapping[str, Any]) -> tuple[int, int, int]:
    if not isinstance(plan, Mapping):
        raise RPE02TimingError("plan must be a mapping")
    if plan.get("normative_unit") != "INTEGER_MONOTONIC_NANOSECONDS":
        raise RPE02TimingError("plan normative unit mismatch")
    origin = _strict_int("plan.schedule_origin_ns", plan.get("schedule_origin_ns"))
    interval = _strict_int("plan.poll_interval_ns", plan.get("poll_interval_ns"))
    bound = _strict_int(
        "plan.detection_latency_bound_ns",
        plan.get("detection_latency_bound_ns"),
    )
    if interval != POLL_INTERVAL_NS:
        raise RPE02TimingError("poll interval is not the preregistered 30 seconds")
    if bound != DETECTION_LATENCY_BOUND_NS:
        raise RPE02TimingError("latency bound is not the preregistered 60 seconds")
    return origin, interval, bound


def _normalize_observation(raw: Mapping[str, Any], index: int) -> dict[str, Any]:
    if not isinstance(raw, Mapping):
        raise RPE02TimingError(f"observations[{index}] must be a mapping")
    required = {
        "scheduled_at_ns",
        "attempt_started_at_ns",
        "remote_observation_completed_at_ns",
        "attempt_completed_at_ns",
        "outcome",
        "observed_head",
    }
    if set(raw) != required:
        raise RPE02TimingError(
            f"observations[{index}] keys mismatch: "
            f"missing={sorted(required - set(raw))}, "
            f"unknown={sorted(set(raw) - required)}"
        )
    out = dict(raw)
    for key in (
        "scheduled_at_ns",
        "attempt_started_at_ns",
        "remote_observation_completed_at_ns",
        "attempt_completed_at_ns",
    ):
        out[key] = _strict_int(f"observations[{index}].{key}", out[key])
    if type(out["outcome"]) is not str or out["outcome"] not in _ALLOWED_OUTCOMES:
        raise RPE02TimingError(
            f"observations[{index}].outcome must be one of "
            f"{sorted(_ALLOWED_OUTCOMES)}"
        )
    if out["outcome"] == "READ_FAILURE":
        if out["observed_head"] is not None:
            raise RPE02TimingError(
                f"observations[{index}] READ_FAILURE may not carry observed_head"
            )
    else:
        out["observed_head"] = _strict_sha40(
            f"observations[{index}].observed_head",
            out["observed_head"],
        )
    return out


def qualify_detection_ns(
    *,
    plan: Mapping[str, Any],
    controlled_source_release_started_at_ns: int,
    target_head: str,
    observations: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    origin, interval, bound = _validate_plan(plan)
    release = _strict_int(
        "controlled_source_release_started_at_ns",
        controlled_source_release_started_at_ns,
    )
    target = _strict_sha40("target_head", target_head)
    if release <= origin:
        raise RPE02TimingError(
            "controlled_source_release_started_at_ns must be greater than schedule_origin_ns"
        )
    if not isinstance(observations, Sequence) or isinstance(
        observations, (str, bytes, bytearray)
    ):
        raise RPE02TimingError("observations must be a sequence")

    normalized = [_normalize_observation(raw, i) for i, raw in enumerate(observations)]
    for index in range(1, len(normalized)):
        if normalized[index]["scheduled_at_ns"] < normalized[index - 1]["scheduled_at_ns"]:
            return _blocked("OBSERVATION_ORDER_NOT_STRICTLY_INCREASING")

    previous_scheduled: int | None = None
    previous_completion: int | None = None
    seen_slots: set[int] = set()

    for item in normalized:
        scheduled = item["scheduled_at_ns"]
        started = item["attempt_started_at_ns"]
        remote_done = item["remote_observation_completed_at_ns"]
        attempt_done = item["attempt_completed_at_ns"]

        if scheduled <= origin or (scheduled - origin) % interval != 0:
            return _blocked("ATTEMPT_OFF_FIXED_RATE_GRID")
        if scheduled in seen_slots:
            return _blocked("DUPLICATE_FIXED_RATE_SLOT")
        seen_slots.add(scheduled)

        if previous_scheduled is not None and scheduled != previous_scheduled + interval:
            return _blocked("CADENCE_GAP")
        if started < scheduled:
            return _blocked("ACTUAL_START_PRECEDES_SCHEDULED_SLOT")
        if started >= scheduled + interval:
            return _blocked("ACTUAL_START_MISSED_FIXED_RATE_SLOT")
        if remote_done < started:
            return _blocked("REMOTE_COMPLETION_PRECEDES_ATTEMPT_START")
        if remote_done > scheduled + interval:
            return _blocked("ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT")
        if attempt_done < remote_done:
            return _blocked("ATTEMPT_COMPLETION_PRECEDES_REMOTE_COMPLETION")
        if previous_completion is not None and previous_completion > started:
            return _blocked("ATTEMPT_OVERLAP")

        if (
            item["outcome"] == "REMOTE_HEAD_OBSERVED"
            and item["observed_head"] == target
            and started < release
        ):
            return _blocked(
                "TARGET_HEAD_OBSERVED_BY_PRE_RELEASE_ATTEMPT",
                first_detection_scheduled_at_ns=scheduled,
                first_detection_attempt_started_at_ns=started,
                first_detection_remote_observation_completed_at_ns=remote_done,
                first_detection_attempt_completed_at_ns=attempt_done,
            )

        previous_scheduled = scheduled
        previous_completion = attempt_done

    first_required = first_fixed_rate_slot_at_or_after_ns(release, interval, origin)
    if normalized:
        slots_at_or_after_release = [
            item["scheduled_at_ns"]
            for item in normalized
            if item["scheduled_at_ns"] >= first_required
        ]
        if slots_at_or_after_release and slots_at_or_after_release[0] != first_required:
            return _blocked("SKIPPED_REQUIRED_ATTEMPT")

    for item in normalized:
        if item["attempt_started_at_ns"] < release:
            continue
        if (
            item["outcome"] == "REMOTE_HEAD_OBSERVED"
            and item["observed_head"] == target
        ):
            latency = item["remote_observation_completed_at_ns"] - release
            status = (
                "PASS_DETECTED_WITHIN_BOUND"
                if latency <= bound
                else "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED"
            )
            return {
                "status": status,
                "failure_code": None,
                "detection_latency_ns": latency,
                "first_detection_scheduled_at_ns": item["scheduled_at_ns"],
                "first_detection_attempt_started_at_ns": item["attempt_started_at_ns"],
                "first_detection_remote_observation_completed_at_ns": item[
                    "remote_observation_completed_at_ns"
                ],
                "first_detection_attempt_completed_at_ns": item["attempt_completed_at_ns"],
            }

    next_required_slot = (
        normalized[-1]["scheduled_at_ns"] + interval
        if normalized
        else first_required
    )
    if next_required_slot - release > bound:
        return {
            "status": "FAIL_NO_DETECTION_BY_BOUND",
            "failure_code": "NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND",
            "detection_latency_ns": None,
        }
    return {
        "status": "INCOMPLETE_REAL_TIME_WINDOW",
        "failure_code": None,
        "detection_latency_ns": None,
    }


def capture_monotonic_clock_capability() -> dict[str, Any]:
    info = time.get_clock_info("monotonic")
    sample_1 = time.monotonic_ns()
    sample_2 = time.monotonic_ns()
    if not info.monotonic:
        raise RPE02TimingError("host monotonic clock does not report monotonic capability")
    return {
        "schema": "ATDS_RPE02_MONOTONIC_CLOCK_CAPABILITY_V0_1",
        "api": "time.monotonic_ns",
        "metadata_api": "time.get_clock_info('monotonic')",
        "normative_unit": "INTEGER_MONOTONIC_NANOSECONDS",
        "monotonic": bool(info.monotonic),
        "adjustable": bool(info.adjustable),
        "resolution_seconds": info.resolution,
        "implementation": info.implementation,
        "sample_1_ns": sample_1,
        "sample_2_ns": sample_2,
        "same_process_host_domain": True,
        "python_version": sys.version.replace("\n", " "),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
    }

~~~

## RPE03 V0.1 HISTORICAL CLASSIFIER

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

## P5E CONTRACT

PATH: tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json

~~~json
{
  "schema": "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1",
  "status": "CANDIDATE_TARGETED_CLOSURE_PENDING_EXTERNAL_REREVIEW",
  "qualification_stage": "CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY",
  "real_p5e_execution_authorized": false,
  "source_repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "monitored_source": {
    "remote": "origin",
    "branch": "integration/system-v1",
    "canonical_authority": "GITHUB_REMOTE_BRANCH",
    "local_working_tree_is_not_authority": true
  },
  "predecessors": {
    "p5a_continuous_projection_contract_blob": "96ec1a768b8e9ff77d94bbcd36ee513678c258e6",
    "p5a_qualification_report_blob": "8954475370494ff00f77af8331b2e54b80cf3f70",
    "p5d1_observer_contract_blob": "a20999ae991e07447e25ecd1592964f2d333449b",
    "p5d1_static_review_blob": "d10a6659e8deec917803f53c652fc7e4d4d19458",
    "p5d2_one_shot_contract_blob": "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3",
    "p5d2_static_review_blob": "023cc210facdbc4b571b88bd257057c67a3df46b",
    "p5d4_loop_contract_blob": "6980de1eb55e49c0c2bd2f91620aeb75640753b6",
    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
    "p5d4_real_v0_2_qualification_blob": "660a679532d1bb122b0df382230d4d249a0cac1f",
    "p5d4_human_adjudication_blob": "ef5e07c6641db94e91d9f2bc0e8093b244baa507"
  },
  "objective": {
    "name": "END_TO_END_NEAR_REAL_TIME_QUALIFICATION",
    "purpose": "Define the temporal and authority contract required before any real repeated observation experiment may claim bounded near-real-time behavior around the already-qualified P5-D4 bounded loop.",
    "this_stage_is_not_real_end_to_end_execution": true,
    "this_stage_may_not_claim_continuous_synchronization": true
  },
  "near_real_time_timing": {
    "delivery_semantics": "NEAR_REAL_TIME_BOUNDED_LATENCY",
    "poll_interval_seconds": 30,
    "detection_latency_seconds_max": 60,
    "instantaneous_realtime_claim_forbidden": true,
    "silent_interval_widening_forbidden": true,
    "silent_latency_bound_widening_forbidden": true,
    "detection_latency_definition": "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC_MINUS_CONTROLLED_SOURCE_RELEASE_MONOTONIC",
    "future_real_bound_clock": "MONOTONIC_ELAPSED_TIME",
    "future_real_wall_clock_may_be_recorded_as_evidence_only": true,
    "future_real_poll_schedule_semantics": "FIXED_RATE_30_SECOND_GRID",
    "single_transient_read_failure_may_still_meet_60_second_bound": false,
    "latency_bound_breach_must_not_be_reported_as_near_real_time_pass": true,
    "real_measurement_origin": "CONTROLLED_SOURCE_RELEASE_MONOTONIC",
    "measurement_endpoint": "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC",
    "schedule_semantics": "FIXED_RATE",
    "remote_head_available_time_is_measurable_origin": false,
    "real_latency_metric": "REMOTE_READ_COMPLETION_MONOTONIC_MINUS_CONTROLLED_SOURCE_RELEASE_MONOTONIC",
    "attempt_start_and_read_completion_are_distinct": true,
    "read_duration_is_included_in_detection_latency": true,
    "eligible_detection_attempt_must_start_at_or_after_release": true,
    "single_transient_read_failure_may_meet_bound_only_if_read_completion_is_within_60_seconds": true
  },
  "synthetic_timing_model": {
    "required": true,
    "clock_source": "EXPLICIT_INJECTED_MONOTONIC_SECONDS_ONLY",
    "sleep_forbidden": true,
    "network_forbidden": true,
    "filesystem_state_forbidden": true,
    "process_launch_forbidden": true,
    "environment_read_forbidden": true,
    "real_p5d4_control_state_access_forbidden": true,
    "real_vault_access_forbidden": true,
    "purpose": "Prove timing arithmetic and claim boundaries without performing repeated real observation.",
    "schedule_semantics": "FIXED_RATE",
    "schedule_origin_seconds": 0,
    "observation_record_fields": [
      "scheduled_at_seconds",
      "completed_at_seconds",
      "outcome",
      "observed_head"
    ],
    "head_identity_required_on_successful_remote_observation": true,
    "skipped_required_attempt_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "cadence_gap_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "pre_source_target_observation_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "explicit_non_pass_statuses": [
      "INCOMPLETE_SYNTHETIC_WINDOW"
    ],
    "attempt_overruns_next_required_slot_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "attempt_overruns_next_required_slot_failure_code": "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT",
    "duplicate_fixed_rate_slot_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "duplicate_fixed_rate_slot_failure_code": "DUPLICATE_FIXED_RATE_SLOT",
    "read_completion_before_attempt_start_forbidden": true
  },
  "authority_boundary": {
    "observer_may_create_governance_authority": false,
    "pending_head_evaluation_authorized": false,
    "evaluation_authorized": false,
    "stage_a_authorized": false,
    "stage_b_authorized": false,
    "promotion_authorized": false,
    "publication_authorized": false,
    "real_vault_mutation_authorized": false,
    "current_mutation_authorized": false,
    "current_tmp_mutation_authorized": false,
    "real_polling_loop_authorized": false,
    "daemon_authorized": false,
    "startup_registration_authorized": false,
    "scheduled_task_authorized": false,
    "windows_service_authorized": false,
    "p6_authorized": false
  },
  "head_transition_policy": {
    "same_head_result": "NOOP",
    "same_head_queue_growth_forbidden": true,
    "initial_head_may_queue_exact_head_only_under_existing_p5d2_semantics": true,
    "fast_forward_head_may_queue_exact_head_only_under_existing_p5d2_semantics": true,
    "non_fast_forward_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "unknown_ancestry_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "non_fast_forward_auto_continue_forbidden": true,
    "unknown_ancestry_auto_continue_forbidden": true,
    "active_or_pending_candidate_retarget_forbidden": true
  },
  "queue_and_supersession": {
    "precedence_rule": "CURRENT_QUALIFIED_P5D4_EXECUTABLE_QUEUE_SEMANTICS_OVERRIDE_EARLIER_P5A_DESIGN_INTENT_WHERE_THEY_CONFLICT",
    "p5a_supersession_intent_preserved_as_future_design_debt": true,
    "fifo_required": true,
    "unique_heads_required": true,
    "silent_drop_forbidden": true,
    "silent_reorder_forbidden": true,
    "latest_only_replacement_forbidden": true,
    "coalescing_authorized": false,
    "new_coalescing_semantic_event_authorized": false,
    "pending_head_retarget_forbidden": true,
    "capacity_exhausted_result": "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
    "capacity_exhausted_must_not_mutate_p5d2_state": true,
    "burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification": true
  },
  "failure_and_freshness": {
    "fail_closed_default": true,
    "network_failure_must_not_create_current_claim": true,
    "last_known_good_live_projection_preserved": true,
    "latency_bound_breach_result": "NEAR_REAL_TIME_BOUND_NOT_QUALIFIED",
    "queue_capacity_exhaustion_result": "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
    "non_fast_forward_or_unknown_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "unexpected_state_or_timing_ambiguity_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "timing_inconsistency_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "skipped_required_attempt_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "cadence_gap_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "pre_source_target_observation_result": "BLOCKED_REQUIRES_ADJUDICATION"
  },
  "end_to_end_definition": {
    "real_end_to_end_stages": [
      "SOURCE_HEAD_BECOMES_OBSERVABLE",
      "REMOTE_HEAD_DETECTED_WITHIN_BOUND",
      "HEAD_TRANSITION_CLASSIFIED",
      "EXACT_HEAD_ENTERED_GOVERNED_QUEUE_OR_FAIL_CLOSED",
      "EXACT_HEAD_EVALUATED_IF_SEPARATELY_AUTHORIZED",
      "PROMOTION_DECISION_IF_SEPARATELY_AUTHORIZED",
      "PUBLICATION_IF_SEPARATELY_AUTHORIZED",
      "LIVE_GENERATION_VERIFIED_IF_PUBLICATION_AUTHORIZED"
    ],
    "current_stage_may_qualify_only": [
      "TIMING_CONTRACT",
      "SYNTHETIC_FIXED_RATE_DETECTION_MODEL",
      "AUTHORITY_BOUNDARIES",
      "REUSED_MAPPED_P5D2_P5D4_FAIL_CLOSED_QUEUE_BEHAVIOR"
    ],
    "real_end_to_end_pass_requires_all_authorized_applicable_stages": true,
    "omitted_unauthorized_downstream_stages_may_not_be_relabelled_pass": true,
    "transient_tip_exact_detection_sla_not_qualified": true,
    "real_remote_availability_to_detection_sla_not_qualified": true
  },
  "claim_boundary": {
    "maximum_current_claim": "P5E_V0_1_TARGETED_CLOSURE_CANDIDATE_QUALIFIED_PENDING_EXTERNAL_REREVIEW",
    "real_end_to_end_qualification_requires_separate_authorization": true,
    "forbidden_current_claims": [
      "P5E_REAL_END_TO_END_QUALIFIED",
      "CONTINUOUS_SYNCHRONIZATION_QUALIFIED",
      "REAL_60_SECOND_SLA_QUALIFIED",
      "AUTOMATIC_EVALUATION_QUALIFIED",
      "AUTOMATIC_PROMOTION_QUALIFIED",
      "AUTOMATIC_PUBLICATION_QUALIFIED",
      "REMOTE_HEAD_AVAILABLE_TIME_TO_DETECTION_SLA_QUALIFIED",
      "PER_TRANSIENT_TIP_DETECTION_SLA_QUALIFIED"
    ]
  },
  "real_context_evidence_only": {
    "live_projection_head_at_opening": "59f1dc26973b0b50efefccf12b26784d1e41f546",
    "queued_unevaluated_head_at_opening": "1d4c2f3d657b36ecaa6ab25b967e46b3620190d1",
    "remote_head_observed_during_contract_opening": "fcca78571a26955ae3fe462746ef49557e4e84e5",
    "queued_head_is_ancestor_of_remote_head": true,
    "must_not_be_used_as_real_experiment_execution": true,
    "must_not_be_mutated_by_contract_qualification": true
  },
  "required_synthetic_cases": [
    "SAME_HEAD_NOOP",
    "CHANGE_JUST_AFTER_POLL_DETECTED_AT_NEXT_30_SECOND_SLOT",
    "ONE_TRANSIENT_READ_FAILURE_THEN_DETECTED_BY_60_SECONDS",
    "DETECTION_AFTER_60_SECONDS_REJECTED",
    "NO_DETECTION_BY_60_SECONDS_REJECTED",
    "NON_FAST_FORWARD_BLOCKED",
    "UNKNOWN_ANCESTRY_BLOCKED",
    "PENDING_QUEUE_FULL_NEWER_HEAD_FAILS_CLOSED",
    "SAME_HEAD_DOES_NOT_GROW_QUEUE",
    "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD"
  ],
  "required_breakers": [
    "POLL_INTERVAL_NOT_EXACTLY_30_ACCEPTED",
    "DETECTION_BOUND_ABOVE_60_ACCEPTED",
    "INSTANTANEOUS_REALTIME_CLAIM_ACCEPTED",
    "WALL_CLOCK_USED_AS_SYNTHETIC_CONTROL_CLOCK",
    "SLEEP_USED_IN_SYNTHETIC_MODEL",
    "NETWORK_USED_IN_SYNTHETIC_MODEL",
    "FILESYSTEM_STATE_USED_IN_SYNTHETIC_MODEL",
    "PROCESS_LAUNCH_USED_IN_SYNTHETIC_MODEL",
    "SUCCESS_AFTER_60_SECONDS_CLASSIFIED_PASS",
    "NO_SUCCESS_BY_60_SECONDS_CLASSIFIED_PASS",
    "SAME_HEAD_GROWS_QUEUE",
    "NON_FAST_FORWARD_AUTO_CONTINUES",
    "UNKNOWN_ANCESTRY_AUTO_CONTINUES",
    "QUEUE_FULL_SILENTLY_DROPS_HEAD",
    "QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD",
    "QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT",
    "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD",
    "EVALUATION_AUTHORITY_BECOMES_TRUE",
    "PROMOTION_AUTHORITY_BECOMES_TRUE",
    "PUBLICATION_AUTHORITY_BECOMES_TRUE",
    "REAL_VAULT_MUTATION_AUTHORITY_BECOMES_TRUE",
    "REAL_POLLING_AUTHORITY_BECOMES_TRUE",
    "DAEMON_OR_SERVICE_AUTHORITY_BECOMES_TRUE",
    "P6_AUTHORITY_BECOMES_TRUE",
    "CONTRACT_PASS_LAUNDERS_INTO_REAL_P5E_PASS"
  ],
  "next_gate_after_candidate_qualification": {
    "external_adversarial_review_required_before_normative_adoption": true,
    "human_adjudication_required_after_external_review": true,
    "real_p5e_execution_requires_separate_human_authorization": true,
    "p6_remains_closed": true,
    "external_adversarial_rereview_required": true,
    "human_adjudication_before_external_rereview_forbidden": true
  },
  "tip_visibility_semantics": {
    "observed_remote_tip_definition": "HEAD_IDENTITY_RETURNED_BY_A_SUCCESSFUL_REMOTE_READ",
    "intermediate_fast_forward_commit_definition": "COMMIT_CONTAINED_BY_LATER_OBSERVED_FAST_FORWARD_HEAD_BUT_NOT_ITSELF_OBSERVED_AS_REMOTE_TIP",
    "unobserved_intermediate_tip_may_be_claimed_observed": false,
    "unobserved_intermediate_tip_may_be_queued": false,
    "fast_forward_content_containment_is_queue_coalescing": false,
    "already_observed_queued_head_replacement_forbidden": true,
    "already_observed_queued_head_retarget_forbidden": true,
    "per_transient_tip_detection_sla_authorized": false,
    "future_ancestry_enumeration_requires_separate_qualification": true,
    "unobserved_intermediate_tip_non_injection_is_future_adapter_rule": true,
    "unobserved_intermediate_tip_non_injection_is_current_runtime_qualified_property": false
  },
  "external_review_targeted_closure": {
    "findings": {
      "B1": "CONFIRMED_BLOCKING_WITH_UPSTREAM_COVERAGE_NUANCE",
      "B2": "CONFIRMED_BLOCKING",
      "B3": "CONFIRMED_BLOCKING",
      "B4": "CONFIRMED_BLOCKING",
      "B5": "PARTIALLY_CONFIRMED_BLOCKING_SEMANTIC_GAP"
    },
    "required_breakers": [
      "SKIPPED_REQUIRED_ATTEMPT_ACCEPTED",
      "CADENCE_GAP_ACCEPTED",
      "PRE_SOURCE_TARGET_OBSERVATION_IGNORED",
      "REMOTE_AVAILABILITY_TIME_TREATED_AS_MEASURABLE_ORIGIN",
      "READ_COMPLETION_LATENCY_HIDDEN",
      "OBSERVATION_WITHOUT_HEAD_IDENTITY_ACCEPTED",
      "UNOBSERVED_TRANSIENT_TIP_CLAIMED_EXACTLY_OBSERVED",
      "REQUIRED_CASE_OR_BREAKER_UNMAPPED"
    ],
    "requirement_to_executable_evidence_matrix_required": true,
    "all_required_cases_must_be_mapped": true,
    "all_base_breakers_must_be_mapped": true,
    "all_targeted_closure_breakers_must_be_mapped": true,
    "unmapped_requirement_result": "BLOCKED",
    "external_rereview_required_before_human_normative_adoption": true
  }
}

~~~

## P5E SYNTHETIC MODEL

PATH: tools/obsidian_projection/p5e_near_real_time_model.py

~~~python
from __future__ import annotations

from typing import Any


PLAN_SCHEMA = "ATDS_OBSIDIAN_P5E_SYNTHETIC_TIMING_PLAN_V0_1_AMENDED"
RESULT_SCHEMA = "ATDS_OBSIDIAN_P5E_SYNTHETIC_TIMING_RESULT_V0_1_AMENDED"

_POLL_INTERVAL_SECONDS = 30
_DETECTION_LATENCY_SECONDS_MAX = 60
_SCHEDULE_ORIGIN_SECONDS = 0
_ALLOWED_OUTCOMES = frozenset({"READ_FAILURE", "REMOTE_HEAD_OBSERVED"})


class P5ETimingModelError(ValueError):
    pass


def _is_nonnegative_int(value: Any) -> bool:
    return (
        not isinstance(value, bool)
        and isinstance(value, int)
        and value >= 0
    )


def _valid_head(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 40:
        return False
    return all(ch in "0123456789abcdef" for ch in value)


def make_timing_plan(
    *,
    poll_interval_seconds: int = _POLL_INTERVAL_SECONDS,
    detection_latency_seconds_max: int = _DETECTION_LATENCY_SECONDS_MAX,
    schedule_origin_seconds: int = _SCHEDULE_ORIGIN_SECONDS,
) -> dict[str, Any]:
    if poll_interval_seconds != _POLL_INTERVAL_SECONDS:
        raise P5ETimingModelError(
            "P5-E V0.1 poll interval must remain exactly 30 seconds"
        )
    if detection_latency_seconds_max != _DETECTION_LATENCY_SECONDS_MAX:
        raise P5ETimingModelError(
            "P5-E V0.1 detection bound must remain exactly 60 seconds"
        )
    if schedule_origin_seconds != _SCHEDULE_ORIGIN_SECONDS:
        raise P5ETimingModelError(
            "P5-E V0.1 synthetic fixed-rate origin must remain exactly zero"
        )
    return {
        "schema": PLAN_SCHEMA,
        "poll_interval_seconds": _POLL_INTERVAL_SECONDS,
        "detection_latency_seconds_max": _DETECTION_LATENCY_SECONDS_MAX,
        "schedule_origin_seconds": _SCHEDULE_ORIGIN_SECONDS,
        "schedule_semantics": "FIXED_RATE",
        "clock_source": "EXPLICIT_INJECTED_MONOTONIC_SECONDS_ONLY",
        "measurement_origin": "CONTROLLED_SOURCE_RELEASE_MONOTONIC",
        "measurement_endpoint": "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC",
        "real_execution_authorized": False,
    }


def _validate_plan(plan: dict[str, Any]) -> None:
    if not isinstance(plan, dict):
        raise P5ETimingModelError("plan must be an object")
    if plan != make_timing_plan(
        poll_interval_seconds=plan.get("poll_interval_seconds"),
        detection_latency_seconds_max=plan.get(
            "detection_latency_seconds_max"
        ),
        schedule_origin_seconds=plan.get("schedule_origin_seconds"),
    ):
        raise P5ETimingModelError("plan fields mismatch")


def _blocked(failure_code: str) -> dict[str, Any]:
    return _result(
        status="BLOCKED_REQUIRES_ADJUDICATION",
        failure_code=failure_code,
        detection_latency_seconds=None,
        first_detection_scheduled_at_seconds=None,
        first_detection_completed_at_seconds=None,
        observed_head=None,
    )


def _result(
    *,
    status: str,
    failure_code: str | None,
    detection_latency_seconds: int | None,
    first_detection_scheduled_at_seconds: int | None,
    first_detection_completed_at_seconds: int | None,
    observed_head: str | None,
) -> dict[str, Any]:
    return {
        "schema": RESULT_SCHEMA,
        "status": status,
        "failure_code": failure_code,
        "detection_latency_seconds": detection_latency_seconds,
        "first_detection_scheduled_at_seconds": (
            first_detection_scheduled_at_seconds
        ),
        "first_detection_completed_at_seconds": (
            first_detection_completed_at_seconds
        ),
        "observed_head": observed_head,
        "real_end_to_end_qualified": False,
        "continuous_synchronization_qualified": False,
        "automatic_evaluation_authorized": False,
        "automatic_promotion_authorized": False,
        "automatic_publication_authorized": False,
    }


def _first_fixed_rate_slot_at_or_after(
    *,
    instant_seconds: int,
    interval: int,
    origin: int,
) -> int:
    first_slot = origin + interval
    if instant_seconds <= first_slot:
        return first_slot
    delta = instant_seconds - origin
    quotient, remainder = divmod(delta, interval)
    return origin + (quotient + (1 if remainder else 0)) * interval


def _validate_observation_shapes(
    observations: list[dict[str, Any]],
) -> None:
    if not isinstance(observations, list) or not observations:
        raise P5ETimingModelError("observations must be a non-empty list")
    required_fields = {
        "scheduled_at_seconds",
        "completed_at_seconds",
        "outcome",
        "observed_head",
    }
    for observation in observations:
        if not isinstance(observation, dict):
            raise P5ETimingModelError("observation must be an object")
        if set(observation) != required_fields:
            raise P5ETimingModelError("observation fields mismatch")
        scheduled = observation["scheduled_at_seconds"]
        completed = observation["completed_at_seconds"]
        outcome = observation["outcome"]
        observed_head = observation["observed_head"]
        if not _is_nonnegative_int(scheduled):
            raise P5ETimingModelError("scheduled time must be nonnegative")
        if not _is_nonnegative_int(completed):
            raise P5ETimingModelError("completion time must be nonnegative")
        if outcome not in _ALLOWED_OUTCOMES:
            raise P5ETimingModelError("observation outcome invalid")
        if outcome == "READ_FAILURE":
            if observed_head is not None:
                raise P5ETimingModelError(
                    "read failure may not carry a head identity"
                )
        elif not _valid_head(observed_head):
            raise P5ETimingModelError(
                "successful remote observation requires exact head identity"
            )


def classify_tip_visibility(
    *,
    target_head: str,
    observed_head: str,
    fast_forward_contains_target: bool,
) -> str:
    if not _valid_head(target_head) or not _valid_head(observed_head):
        raise P5ETimingModelError("tip identity must be a lowercase 40-hex SHA")
    if not isinstance(fast_forward_contains_target, bool):
        raise P5ETimingModelError("containment fact must be boolean")
    if observed_head == target_head:
        return "EXACT_TIP_OBSERVED"
    if fast_forward_contains_target:
        return "CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED"
    return "UNRELATED_OR_UNPROVEN_REQUIRES_ADJUDICATION"


def qualify_detection(
    *,
    plan: dict[str, Any],
    source_release_at_seconds: int,
    target_head: str,
    observations: list[dict[str, Any]],
) -> dict[str, Any]:
    _validate_plan(plan)
    if not _is_nonnegative_int(source_release_at_seconds):
        raise P5ETimingModelError(
            "controlled source release time must be a nonnegative integer"
        )
    if not _valid_head(target_head):
        raise P5ETimingModelError(
            "target head must be a lowercase 40-hex SHA"
        )
    _validate_observation_shapes(observations)

    interval = plan["poll_interval_seconds"]
    bound = plan["detection_latency_seconds_max"]
    origin = plan["schedule_origin_seconds"]

    previous_scheduled: int | None = None
    previous_completed: int | None = None
    for observation in observations:
        scheduled = observation["scheduled_at_seconds"]
        completed = observation["completed_at_seconds"]

        if scheduled <= origin or (scheduled - origin) % interval != 0:
            return _blocked("ATTEMPT_OFF_FIXED_RATE_GRID")
        if completed < scheduled:
            return _blocked("READ_COMPLETION_PRECEDES_ATTEMPT_START")
        if previous_scheduled is not None:
            if scheduled == previous_scheduled:
                return _blocked("DUPLICATE_FIXED_RATE_SLOT")
            if scheduled - previous_scheduled != interval:
                return _blocked("CADENCE_GAP")
            if previous_completed is not None and previous_completed > scheduled:
                return _blocked("ATTEMPT_OVERLAP")
        previous_scheduled = scheduled
        previous_completed = completed

        if (
            observation["outcome"] == "REMOTE_HEAD_OBSERVED"
            and observation["observed_head"] == target_head
            and scheduled < source_release_at_seconds
        ):
            return _blocked(
                "TARGET_HEAD_OBSERVED_BEFORE_CONTROLLED_RELEASE"
            )

    last_observation = observations[-1]
    if (
        last_observation["completed_at_seconds"]
        > last_observation["scheduled_at_seconds"] + interval
    ):
        return _blocked("ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT")

    first_required_slot = _first_fixed_rate_slot_at_or_after(
        instant_seconds=source_release_at_seconds,
        interval=interval,
        origin=origin,
    )
    scheduled_slots = {
        observation["scheduled_at_seconds"] for observation in observations
    }
    if (
        any(slot >= first_required_slot for slot in scheduled_slots)
        and first_required_slot not in scheduled_slots
    ):
        return _blocked("SKIPPED_REQUIRED_ATTEMPT")

    first_detection: dict[str, Any] | None = None
    for observation in observations:
        if observation["scheduled_at_seconds"] < source_release_at_seconds:
            continue
        if (
            observation["outcome"] == "REMOTE_HEAD_OBSERVED"
            and observation["observed_head"] == target_head
        ):
            first_detection = observation
            break

    if first_detection is not None:
        completed = first_detection["completed_at_seconds"]
        latency = completed - source_release_at_seconds
        if latency <= bound:
            status = "PASS_DETECTED_WITHIN_BOUND"
            failure_code = None
        else:
            status = "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED"
            failure_code = "DETECTION_COMPLETION_EXCEEDED_BOUND"
        return _result(
            status=status,
            failure_code=failure_code,
            detection_latency_seconds=latency,
            first_detection_scheduled_at_seconds=(
                first_detection["scheduled_at_seconds"]
            ),
            first_detection_completed_at_seconds=completed,
            observed_head=first_detection["observed_head"],
        )

    last_scheduled = observations[-1]["scheduled_at_seconds"]
    next_required_slot = last_scheduled + interval
    if next_required_slot - source_release_at_seconds > bound:
        return _result(
            status="FAIL_NO_DETECTION_BY_BOUND",
            failure_code="NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND",
            detection_latency_seconds=None,
            first_detection_scheduled_at_seconds=None,
            first_detection_completed_at_seconds=None,
            observed_head=None,
        )

    return _result(
        status="INCOMPLETE_SYNTHETIC_WINDOW",
        failure_code=None,
        detection_latency_seconds=None,
        first_detection_scheduled_at_seconds=None,
        first_detection_completed_at_seconds=None,
        observed_head=None,
    )

~~~

## P5D4 RUNTIME

PATH: tools/obsidian_projection/p5d4_bounded_observer_loop.py

~~~python
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import tempfile
from pathlib import Path
from typing import Any, Callable, Iterable

from .observer_tick import (
    INPUT_SCHEMA,
    _validate_state,
    make_initial_state,
    one_shot_tick,
)

PLAN_SCHEMA = "ATDS_OBSIDIAN_P5D4_LOOP_PLAN_V0_1"
CHECKPOINT_SCHEMA = "ATDS_OBSIDIAN_P5D4_LOOP_CHECKPOINT_V0_1"
EVENT_SCHEMA = "ATDS_OBSIDIAN_P5D4_LOOP_EVENT_V0_1"
OWNERSHIP_SCHEMA = "ATDS_OBSIDIAN_P5D4_OWNERSHIP_RECORD_V0_1"
EVIDENCE_SCHEMA = "ATDS_OBSIDIAN_P5D4_VERIFIED_PUBLICATION_EVIDENCE_V0_1"
RUN_RESULT_SCHEMA = "ATDS_OBSIDIAN_P5D4_BOUNDED_LOOP_RESULT_V0_1"

_HEAD_RE = re.compile(r"^[0-9a-f]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_PLAN_KEYS = frozenset({
    "schema","loop_id","max_cycles","max_remote_observations",
    "max_evaluations","max_pending_heads","max_consecutive_failures",
    "plan_digest_sha256",
})

class P5D4RuntimeError(RuntimeError):
    pass

class LoopPlanError(P5D4RuntimeError):
    pass

class PersistenceError(P5D4RuntimeError):
    pass

class ReconciliationError(P5D4RuntimeError):
    pass

class OwnershipError(P5D4RuntimeError):
    pass

class OwnershipContended(OwnershipError):
    pass

class QueueCapacityError(P5D4RuntimeError):
    pass

class ControlRootBindingError(P5D4RuntimeError):
    pass

def _canonical_bytes(value: Any) -> bytes:
    try:
        text = json.dumps(
            value, ensure_ascii=False, sort_keys=True,
            separators=(",", ":"), allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise PersistenceError("value is not canonical JSON") from exc
    return (text + "\n").encode("utf-8")

def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()

def _is_int(value: Any, minimum: int) -> bool:
    return not isinstance(value, bool) and isinstance(value, int) and value >= minimum

def _is_head(value: Any) -> bool:
    return isinstance(value, str) and _HEAD_RE.fullmatch(value) is not None

def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None

def _plan_payload(plan: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in plan.items() if key != "plan_digest_sha256"}

def make_loop_plan(
    *,
    loop_id: str,
    max_cycles: int,
    max_remote_observations: int,
    max_evaluations: int,
    max_pending_heads: int,
    max_consecutive_failures: int,
) -> dict[str, Any]:
    plan = {
        "schema": PLAN_SCHEMA,
        "loop_id": loop_id,
        "max_cycles": max_cycles,
        "max_remote_observations": max_remote_observations,
        "max_evaluations": max_evaluations,
        "max_pending_heads": max_pending_heads,
        "max_consecutive_failures": max_consecutive_failures,
    }
    plan["plan_digest_sha256"] = _digest(plan)
    return validate_loop_plan(plan)

def validate_loop_plan(plan: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(plan, dict) or frozenset(plan) != _PLAN_KEYS:
        raise LoopPlanError("loop plan fields mismatch")
    if plan["schema"] != PLAN_SCHEMA:
        raise LoopPlanError("loop plan schema mismatch")
    loop_id = plan["loop_id"]
    if not isinstance(loop_id, str) or not loop_id or loop_id.strip() != loop_id:
        raise LoopPlanError("invalid loop_id")
    for field, minimum in (
        ("max_cycles", 1),
        ("max_remote_observations", 1),
        ("max_evaluations", 0),
        ("max_pending_heads", 1),
        ("max_consecutive_failures", 0),
    ):
        if not _is_int(plan[field], minimum):
            raise LoopPlanError(f"invalid {field}")
    expected = _digest(_plan_payload(plan))
    if plan["plan_digest_sha256"] != expected:
        raise LoopPlanError("loop plan digest mismatch")
    return json.loads(_canonical_bytes(plan).decode("utf-8"))

def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]

def _resolved(path: Path) -> Path:
    try:
        return Path(path).resolve(strict=False)
    except OSError as exc:
        raise P5D4RuntimeError("path resolution unavailable") from exc

def _intersects(first: Path, second: Path) -> bool:
    return (
        first == second
        or first in second.parents
        or second in first.parents
    )

def _normcase_path(path: Path) -> str:
    return os.path.normcase(os.path.normpath(str(path)))

def _path_is_within(path: Path, anchor: Path) -> bool:
    candidate = _normcase_path(path)
    parent = _normcase_path(anchor)
    try:
        return os.path.commonpath([candidate, parent]) == parent
    except ValueError:
        return False

def _existing_chain_has_reparse_point(path: Path) -> bool:
    current = Path(path)
    visited: set[str] = set()
    for _ in range(512):
        key = _normcase_path(current)
        if key in visited:
            raise ControlRootBindingError("control root path chain loop detected")
        visited.add(key)
        try:
            if current.exists() or current.is_symlink():
                info = os.lstat(current)
                attributes = getattr(info, "st_file_attributes", 0)
                reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
                if current.is_symlink() or (reparse_flag and attributes & reparse_flag):
                    return True
                is_junction = getattr(current, "is_junction", None)
                if callable(is_junction) and is_junction():
                    return True
        except OSError as exc:
            raise ControlRootBindingError(
                "control root path chain inspection unavailable"
            ) from exc
        if current.parent == current:
            return False
        current = current.parent
    raise ControlRootBindingError("control root path depth exceeds bound")

def _userprofile_root() -> Path:
    value = os.environ.get("USERPROFILE")
    if not isinstance(value, str) or not value.strip():
        raise ControlRootBindingError("USERPROFILE unavailable")
    profile = Path(value)
    if not profile.is_absolute():
        raise ControlRootBindingError("USERPROFILE is not absolute")
    return _resolved(profile)

def canonical_production_control_root() -> Path:
    return _userprofile_root() / "ATDS-CONTROL" / "OBSIDIAN-PROJECTION" / "P5D4"

def _qualification_control_anchor() -> Path:
    return _userprofile_root() / "ATDS-CONTROL" / "_QUALIFICATION"

def resolve_and_validate_control_root(root: Path) -> Path:
    requested = Path(root)
    if not requested.is_absolute():
        raise ControlRootBindingError("control root must be absolute")
    if _existing_chain_has_reparse_point(requested):
        raise ControlRootBindingError(
            "control root path chain contains reparse point"
        )

    resolved = _resolved(requested)
    canonical = _resolved(canonical_production_control_root())
    qualification = _resolved(_qualification_control_anchor())
    temp_root = _resolved(Path(tempfile.gettempdir()))

    requested_norm = _normcase_path(resolved)
    canonical_norm = _normcase_path(canonical)
    is_production = requested_norm == canonical_norm
    is_qualification = _path_is_within(resolved, qualification)
    is_temp = _path_is_within(resolved, temp_root)

    if not (is_production or is_qualification or is_temp):
        raise ControlRootBindingError(
            "control root is outside canonical or synthetic qualification namespaces"
        )

    if is_production:
        localappdata = os.environ.get("LOCALAPPDATA")
        appdata = os.environ.get("APPDATA")
        for forbidden in (localappdata, appdata):
            if isinstance(forbidden, str) and forbidden.strip():
                if _path_is_within(canonical, _resolved(Path(forbidden))):
                    raise ControlRootBindingError(
                        "production control root depends on AppData"
                    )
        lowered = _normcase_path(canonical)
        if (
            os.path.normcase("\\packages\\") in lowered
            or os.path.normcase("\\localcache\\") in lowered
        ):
            raise ControlRootBindingError(
                "production control root is Store-redirectable"
            )
        return canonical

    return resolved

def _validate_control_root(
    root: Path,
    *,
    forbidden_roots: Iterable[Path] = (),
) -> Path:
    resolved = resolve_and_validate_control_root(root)
    protected = (_resolved(_repo_root()),) + tuple(_resolved(x) for x in forbidden_roots)
    if any(_intersects(resolved, item) for item in protected):
        raise P5D4RuntimeError("control root intersects protected root")
    try:
        resolved.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise P5D4RuntimeError("control root unavailable") from exc
    if not resolved.is_dir():
        raise P5D4RuntimeError("control root is not a directory")
    return resolved

def _write_durable(path: Path, raw: bytes, *, exclusive: bool = False) -> None:
    flags = os.O_WRONLY | os.O_CREAT
    flags |= os.O_EXCL if exclusive else os.O_TRUNC
    fd = os.open(str(path), flags, 0o600)
    try:
        with os.fdopen(fd, "wb", closefd=False) as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(fd)
def acquire_ownership(
    control_root: Path,
    *,
    loop_id: str,
    owner_token: str,
) -> dict[str, Any]:
    root = _validate_control_root(control_root)
    if not isinstance(loop_id, str) or not loop_id:
        raise OwnershipError("invalid loop id")
    if not isinstance(owner_token, str) or not owner_token:
        raise OwnershipError("invalid owner token")
    record = {
        "schema": OWNERSHIP_SCHEMA,
        "loop_id": loop_id,
        "owner_token": owner_token,
    }
    path = root / "ownership.lock"
    try:
        _write_durable(path, _canonical_bytes(record), exclusive=True)
    except FileExistsError as exc:
        raise OwnershipContended("ownership already held") from exc
    return record

def release_ownership(control_root: Path, ownership: dict[str, Any]) -> None:
    root = _validate_control_root(control_root)
    path = root / "ownership.lock"
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise OwnershipError("ownership record unavailable") from exc
    try:
        current = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise OwnershipError("ownership record invalid") from exc
    if raw != _canonical_bytes(current) or current != ownership:
        raise OwnershipError("ownership mismatch")
    try:
        path.unlink()
    except OSError as exc:
        raise OwnershipError("ownership release failed") from exc

def _event_record_digest(record: dict[str, Any]) -> str:
    body = dict(record)
    body.pop("record_digest_sha256", None)
    return _digest(body)

def load_event_log(control_root: Path) -> list[dict[str, Any]]:
    root = _validate_control_root(control_root)
    path = root / "observer-events.jsonl"
    if not path.exists():
        return []
    raw = path.read_bytes()
    if not raw:
        return []
    if not raw.endswith(b"\n"):
        raise PersistenceError("event log has unterminated record")
    records: list[dict[str, Any]] = []
    previous_digest: str | None = None
    expected_sequence = 1
    for line in raw.splitlines(keepends=True):
        try:
            record = json.loads(line.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PersistenceError("event log record invalid") from exc
        if line != _canonical_bytes(record):
            raise PersistenceError("event log record noncanonical")
        required = {
            "schema","sequence","loop_id","cycle_index","normalized_input",
            "p5d2_audit","previous_state_digest_sha256",
            "next_state_digest_sha256","previous_record_digest_sha256",
            "record_digest_sha256","record_origin",
        }
        if set(record) != required or record.get("schema") != EVENT_SCHEMA:
            raise PersistenceError("event log fields mismatch")
        if record["record_origin"] not in {
            "LIVE_BOUNDED_LOOP",
            "EVIDENCE_RECONSTRUCTION",
        }:
            raise PersistenceError("event log record origin invalid")
        if record["sequence"] != expected_sequence:
            raise PersistenceError("event log sequence mismatch")
        if record["previous_record_digest_sha256"] != previous_digest:
            raise PersistenceError("event log hash chain mismatch")
        if record["record_digest_sha256"] != _event_record_digest(record):
            raise PersistenceError("event log digest mismatch")
        event = record["normalized_input"]
        audit = record["p5d2_audit"]
        if (
            not isinstance(event, dict)
            or event.get("sequence") != expected_sequence
            or not isinstance(audit, dict)
            or audit.get("sequence") != expected_sequence
            or audit.get("next_state_digest") != record["next_state_digest_sha256"]
            or audit.get("previous_state_digest") != record["previous_state_digest_sha256"]
        ):
            raise PersistenceError("event log P5-D2 binding mismatch")
        previous_digest = record["record_digest_sha256"]
        expected_sequence += 1
        records.append(record)
    return records

def load_checkpoint(control_root: Path) -> dict[str, Any] | None:
    root = _validate_control_root(control_root)
    path = root / "observer-checkpoint.json"
    if not path.exists():
        return None
    raw = path.read_bytes()
    try:
        checkpoint = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PersistenceError("checkpoint invalid") from exc
    if raw != _canonical_bytes(checkpoint):
        raise PersistenceError("checkpoint noncanonical")
    required = {
        "schema","loop_plan_digest_sha256","observer_state",
        "observer_state_digest_sha256","last_event_sequence",
        "last_event_digest_sha256","checkpoint_generation",
    }
    if set(checkpoint) != required or checkpoint.get("schema") != CHECKPOINT_SCHEMA:
        raise PersistenceError("checkpoint fields mismatch")
    state = checkpoint["observer_state"]
    try:
        _validate_state(state)
    except Exception as exc:
        raise PersistenceError("checkpoint observer state invalid") from exc
    if checkpoint["observer_state_digest_sha256"] != _digest(state):
        raise PersistenceError("checkpoint state digest mismatch")
    if checkpoint["last_event_sequence"] != state["last_event_sequence"]:
        raise PersistenceError("checkpoint sequence mismatch")
    if not _is_int(checkpoint["checkpoint_generation"], 1):
        raise PersistenceError("checkpoint generation invalid")
    if not _is_sha256(checkpoint["loop_plan_digest_sha256"]):
        raise PersistenceError("checkpoint plan digest invalid")
    if not _is_sha256(checkpoint["last_event_digest_sha256"]):
        raise PersistenceError("checkpoint event digest invalid")
    return checkpoint

def _checkpoint_value(
    *,
    plan: dict[str, Any],
    state: dict[str, Any],
    event_digest: str,
    generation: int,
) -> dict[str, Any]:
    return {
        "schema": CHECKPOINT_SCHEMA,
        "loop_plan_digest_sha256": plan["plan_digest_sha256"],
        "observer_state": state,
        "observer_state_digest_sha256": _digest(state),
        "last_event_sequence": state["last_event_sequence"],
        "last_event_digest_sha256": event_digest,
        "checkpoint_generation": generation,
    }

def _write_checkpoint(
    root: Path,
    *,
    plan: dict[str, Any],
    state: dict[str, Any],
    event_digest: str,
) -> dict[str, Any]:
    existing = load_checkpoint(root)
    generation = 1 if existing is None else existing["checkpoint_generation"] + 1
    value = _checkpoint_value(
        plan=plan, state=state, event_digest=event_digest, generation=generation)
    temp = root / "observer-checkpoint.tmp"
    final = root / "observer-checkpoint.json"
    _write_durable(temp, _canonical_bytes(value))
    try:
        os.replace(str(temp), str(final))
    except OSError as exc:
        raise PersistenceError("checkpoint atomic replace failed") from exc
    verified = load_checkpoint(root)
    if verified != value:
        raise PersistenceError("checkpoint read-after-write mismatch")
    return verified
def _append_event(root: Path, record: dict[str, Any]) -> None:
    path = root / "observer-events.jsonl"
    raw = _canonical_bytes(record)
    try:
        with path.open("ab") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except OSError as exc:
        raise PersistenceError("event append failed") from exc

def _would_append_queue(state: dict[str, Any], event: dict[str, Any]) -> bool:
    return (
        event.get("event_type") == "REMOTE_HEAD_OBSERVED"
        and event.get("transition_class") in {"INITIAL", "FAST_FORWARD"}
        and event.get("observed_head") not in state.get("pending_heads", [])
    )

def persist_tick(
    *,
    control_root: Path,
    plan: dict[str, Any],
    previous_state: dict[str, Any],
    normalized_input: dict[str, Any],
    loop_id: str,
    cycle_index: int,
    record_origin: str = "LIVE_BOUNDED_LOOP",
    fault_injector: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    plan = validate_loop_plan(plan)
    root = _validate_control_root(control_root)
    try:
        _validate_state(previous_state)
    except Exception as exc:
        raise PersistenceError("previous observer state invalid") from exc
    if loop_id != plan["loop_id"]:
        raise PersistenceError("loop id mismatch")
    if record_origin not in {"LIVE_BOUNDED_LOOP", "EVIDENCE_RECONSTRUCTION"}:
        raise PersistenceError("record origin invalid")
    if _would_append_queue(previous_state, normalized_input):
        if len(previous_state["pending_heads"]) >= plan["max_pending_heads"]:
            raise QueueCapacityError("pending queue capacity exhausted")

    log = load_event_log(root)
    if log:
        tail = log[-1]
        if tail["sequence"] != previous_state["last_event_sequence"]:
            raise PersistenceError("event log/state sequence mismatch")
        if tail["next_state_digest_sha256"] != _digest(previous_state):
            raise PersistenceError("event log/state digest mismatch")
    elif previous_state["last_event_sequence"] != 0:
        raise PersistenceError("noninitial state has no event history")
    tick = one_shot_tick(previous_state, normalized_input)
    audit = tick["audit"]
    previous_record_digest = log[-1]["record_digest_sha256"] if log else None
    record = {
        "schema": EVENT_SCHEMA,
        "sequence": normalized_input["sequence"],
        "loop_id": loop_id,
        "cycle_index": cycle_index,
        "normalized_input": normalized_input,
        "p5d2_audit": audit,
        "previous_state_digest_sha256": audit["previous_state_digest"],
        "next_state_digest_sha256": audit["next_state_digest"],
        "previous_record_digest_sha256": previous_record_digest,
        "record_origin": record_origin,
    }
    record["record_digest_sha256"] = _event_record_digest(record)
    _append_event(root, record)
    if fault_injector is not None:
        fault_injector("AFTER_EVENT_DURABLE_BEFORE_CHECKPOINT_REPLACE")
    checkpoint = _write_checkpoint(
        root,
        plan=plan,
        state=tick["next_state"],
        event_digest=record["record_digest_sha256"],
    )
    return {
        "tick_result": tick,
        "event_record": record,
        "checkpoint": checkpoint,
    }

def _replay_record(
    state: dict[str, Any],
    record: dict[str, Any],
) -> dict[str, Any]:
    if record["previous_state_digest_sha256"] != _digest(state):
        raise ReconciliationError("replay previous-state digest mismatch")
    try:
        tick = one_shot_tick(state, record["normalized_input"])
    except Exception as exc:
        raise ReconciliationError("P5-D2 replay rejected") from exc
    if tick["audit"] != record["p5d2_audit"]:
        raise ReconciliationError("replay audit mismatch")
    if _digest(tick["next_state"]) != record["next_state_digest_sha256"]:
        raise ReconciliationError("replay next-state digest mismatch")
    return tick["next_state"]

def _validate_evidence(
    verified_current_head: str,
    evidence: dict[str, Any] | None,
) -> dict[str, Any]:
    if not _is_head(verified_current_head):
        raise ReconciliationError("verified CURRENT head invalid")
    if not isinstance(evidence, dict):
        raise ReconciliationError("verified publication evidence required")
    required = {
        "schema","candidate_head","status","transaction_plan_digest_sha256",
        "physical_receipt_digest_sha256","logical_receipt_digest_sha256",
        "p5d2_promotion_confirmed_emitted",
    }
    if set(evidence) != required or evidence.get("schema") != EVIDENCE_SCHEMA:
        raise ReconciliationError("publication evidence fields mismatch")
    if evidence["candidate_head"] != verified_current_head:
        raise ReconciliationError("publication evidence head mismatch")
    if evidence["status"] != "PASS_LIVE_PUBLICATION_CONFIRMED":
        raise ReconciliationError("publication evidence status mismatch")
    for field in (
        "transaction_plan_digest_sha256",
        "physical_receipt_digest_sha256",
        "logical_receipt_digest_sha256",
    ):
        if not _is_sha256(evidence[field]):
            raise ReconciliationError("publication evidence digest invalid")
    if evidence["p5d2_promotion_confirmed_emitted"] is not True:
        raise ReconciliationError("promotion confirmation evidence missing")
    return evidence

def reconstruct_from_verified_publication_evidence(
    *,
    control_root: Path,
    plan: dict[str, Any],
    verified_current_head: str,
    promotion_evidence: dict[str, Any] | None,
) -> dict[str, Any]:
    plan = validate_loop_plan(plan)
    root = _validate_control_root(control_root)
    if load_checkpoint(root) is not None or load_event_log(root):
        raise ReconciliationError("evidence reconstruction requires empty control state")
    _validate_evidence(verified_current_head, promotion_evidence)
    state = make_initial_state()
    events = (
        {
            "schema": INPUT_SCHEMA, "event_type": "REMOTE_HEAD_OBSERVED",
            "sequence": 1, "observed_head": verified_current_head,
            "transition_class": "INITIAL", "candidate_head": None, "failure_code": None,
        },
        {
            "schema": INPUT_SCHEMA, "event_type": "EVALUATION_STARTED",
            "sequence": 2, "observed_head": None, "transition_class": None,
            "candidate_head": verified_current_head, "failure_code": None,
        },
        {
            "schema": INPUT_SCHEMA, "event_type": "EVALUATION_PASSED",
            "sequence": 3, "observed_head": None, "transition_class": None,
            "candidate_head": verified_current_head, "failure_code": None,
        },
        {
            "schema": INPUT_SCHEMA, "event_type": "PROMOTION_CONFIRMED",
            "sequence": 4, "observed_head": None, "transition_class": None,
            "candidate_head": verified_current_head, "failure_code": None,
        },
    )
    for event in events:
        persisted = persist_tick(
            control_root=root,
            plan=plan,
            previous_state=state,
            normalized_input=event,
            loop_id=plan["loop_id"],
            cycle_index=0,
            record_origin="EVIDENCE_RECONSTRUCTION",
        )
        state = persisted["tick_result"]["next_state"]
    return {
        "status": "PASS_RECONSTRUCTED_VERIFIED_PUBLICATION_EVIDENCE",
        "observer_state": state,
        "evidence": promotion_evidence,
    }

def reconcile_control_state(
    *,
    control_root: Path,
    plan: dict[str, Any],
    verified_current_head: str | None,
    promotion_evidence: dict[str, Any] | None,
) -> dict[str, Any]:
    plan = validate_loop_plan(plan)
    root = _validate_control_root(control_root)
    log = load_event_log(root)
    checkpoint = load_checkpoint(root)

    if checkpoint is None and not log:
        if verified_current_head is None:
            return {
                "status": "PASS_CANONICAL_INITIAL_STATE",
                "observer_state": make_initial_state(),
            }
        return reconstruct_from_verified_publication_evidence(
            control_root=root,
            plan=plan,
            verified_current_head=verified_current_head,
            promotion_evidence=promotion_evidence,
        )

    if checkpoint is None:
        if len(log) != 1:
            raise ReconciliationError("event log too far ahead without checkpoint")
        base = make_initial_state()
        next_state = _replay_record(base, log[0])
        _write_checkpoint(
            root,
            plan=plan,
            state=next_state,
            event_digest=log[0]["record_digest_sha256"],
        )
        return {
            "status": "PASS_RECONCILED_ONE_RECORD_AHEAD",
            "observer_state": next_state,
        }

    if checkpoint["loop_plan_digest_sha256"] != plan["plan_digest_sha256"]:
        raise ReconciliationError("checkpoint loop-plan mismatch")
    cp_seq = checkpoint["last_event_sequence"]
    if cp_seq > len(log):
        raise ReconciliationError("checkpoint ahead of event log")
    delta = len(log) - cp_seq
    if delta > 1:
        raise ReconciliationError("event log more than one record ahead")
    state = checkpoint["observer_state"]
    if cp_seq:
        tail_at_checkpoint = log[cp_seq - 1]
        if checkpoint["last_event_digest_sha256"] != tail_at_checkpoint["record_digest_sha256"]:
            raise ReconciliationError("checkpoint event digest mismatch")
        if checkpoint["observer_state_digest_sha256"] != tail_at_checkpoint["next_state_digest_sha256"]:
            raise ReconciliationError("checkpoint/log state digest mismatch")
    if delta == 1:
        record = log[-1]
        state = _replay_record(state, record)
        _write_checkpoint(
            root,
            plan=plan,
            state=state,
            event_digest=record["record_digest_sha256"],
        )
        status = "PASS_RECONCILED_ONE_RECORD_AHEAD"
    else:
        status = "PASS_RECONCILED_ALIGNED"

    live = state["live_projection_head"]
    if verified_current_head is None:
        if live is not None:
            raise ReconciliationError("checkpoint live head has no physical CURRENT")
    elif live != verified_current_head:
        raise ReconciliationError("physical CURRENT differs from checkpoint live head")

    return {"status": status, "observer_state": state}

def _normalized_event(
    state: dict[str, Any],
    event_type: str,
    *,
    candidate_head: str | None = None,
    failure_code: str | None = None,
) -> dict[str, Any]:
    return {
        "schema": INPUT_SCHEMA,
        "event_type": event_type,
        "sequence": state["last_event_sequence"] + 1,
        "observed_head": None,
        "transition_class": None,
        "candidate_head": candidate_head,
        "failure_code": failure_code,
    }

def _write_run_result(root: Path, result: dict[str, Any]) -> None:
    temp = root / "last-run.tmp"
    final = root / "last-run.json"
    _write_durable(temp, _canonical_bytes(result))
    try:
        os.replace(str(temp), str(final))
    except OSError as exc:
        raise PersistenceError("run-result replace failed") from exc

def _base_run_result(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": RUN_RESULT_SCHEMA,
        "loop_id": plan["loop_id"],
        "loop_plan_digest_sha256": plan["plan_digest_sha256"],
        "terminal_reason": None,
        "cycles_started": 0,
        "remote_observations": 0,
        "evaluations_started": 0,
        "consecutive_failures": 0,
        "observer_state": None,
        "automatic_promotion_authorized": False,
        "production_write_authorized": False,
    }

def run_bounded_loop(
    *,
    plan: dict[str, Any],
    control_root: Path,
    observation_adapter: Callable[[dict[str, Any]], dict[str, Any]],
    evaluation_adapter: Callable[[str, dict[str, Any]], dict[str, Any]],
    verified_current_head: str | None,
    promotion_evidence: dict[str, Any] | None,
    forbidden_roots: Iterable[Path] = (),
    owner_token: str,
) -> dict[str, Any]:
    plan = validate_loop_plan(plan)
    root = _validate_control_root(control_root, forbidden_roots=forbidden_roots)
    result = _base_run_result(plan)
    try:
        ownership = acquire_ownership(
            root, loop_id=plan["loop_id"], owner_token=owner_token)
    except OwnershipContended:
        result["terminal_reason"] = "LOCK_CONTENDED"
        return result

    state: dict[str, Any] | None = None
    try:
        reconciled = reconcile_control_state(
            control_root=root,
            plan=plan,
            verified_current_head=verified_current_head,
            promotion_evidence=promotion_evidence,
        )
        state = reconciled["observer_state"]

        if state["observer_phase"] == "CANDIDATE_PENDING":
            result["terminal_reason"] = "PROMOTION_AUTHORITY_REQUIRED"
        elif state["observer_phase"] == "BLOCKED":
            result["terminal_reason"] = "BLOCKED_REQUIRES_ADJUDICATION"
        elif state["observer_phase"] == "EVALUATING":
            result["terminal_reason"] = "RECONCILIATION_REQUIRED"
        elif state["observer_phase"] == "STOPPED":
            result["terminal_reason"] = "SHUTDOWN_REQUESTED"

        for cycle_index in range(1, plan["max_cycles"] + 1):
            if result["terminal_reason"] is not None:
                break
            result["cycles_started"] += 1

            if state["pending_heads"]:
                if result["evaluations_started"] >= plan["max_evaluations"]:
                    result["terminal_reason"] = "BOUND_REACHED"
                    break
                candidate = state["pending_heads"][0]
                started = persist_tick(
                    control_root=root,
                    plan=plan,
                    previous_state=state,
                    normalized_input=_normalized_event(
                        state, "EVALUATION_STARTED", candidate_head=candidate),
                    loop_id=plan["loop_id"],
                    cycle_index=cycle_index,
                )
                state = started["tick_result"]["next_state"]
                result["evaluations_started"] += 1
                outcome = evaluation_adapter(candidate, started["tick_result"])
                if not isinstance(outcome, dict):
                    raise P5D4RuntimeError("evaluation adapter result invalid")
                classification = outcome.get("outcome")
                failure_code = outcome.get("failure_code")
                if classification == "QUALIFIED":
                    finished = persist_tick(
                        control_root=root, plan=plan, previous_state=state,
                        normalized_input=_normalized_event(
                            state, "EVALUATION_PASSED", candidate_head=candidate),
                        loop_id=plan["loop_id"], cycle_index=cycle_index)
                    state = finished["tick_result"]["next_state"]
                    result["terminal_reason"] = "PROMOTION_AUTHORITY_REQUIRED"
                elif classification == "REJECTED":
                    if not isinstance(failure_code, str) or not failure_code:
                        raise P5D4RuntimeError("rejected evaluation requires failure code")
                    finished = persist_tick(
                        control_root=root, plan=plan, previous_state=state,
                        normalized_input=_normalized_event(
                            state, "EVALUATION_FAILED",
                            candidate_head=candidate, failure_code=failure_code),
                        loop_id=plan["loop_id"], cycle_index=cycle_index)
                    state = finished["tick_result"]["next_state"]
                    result["terminal_reason"] = "BLOCKED_REQUIRES_ADJUDICATION"
                elif classification == "BLOCKED":
                    result["terminal_reason"] = "BLOCKED_REQUIRES_ADJUDICATION"
                else:
                    raise P5D4RuntimeError("evaluation outcome invalid")
                continue

            if result["remote_observations"] >= plan["max_remote_observations"]:
                result["terminal_reason"] = "BOUND_REACHED"
                break
            event = observation_adapter(state)
            result["remote_observations"] += 1
            observed = persist_tick(
                control_root=root,
                plan=plan,
                previous_state=state,
                normalized_input=event,
                loop_id=plan["loop_id"],
                cycle_index=cycle_index,
            )
            state = observed["tick_result"]["next_state"]
            if event.get("event_type") == "REMOTE_OBSERVATION_FAILED":
                result["consecutive_failures"] += 1
                if result["consecutive_failures"] > plan["max_consecutive_failures"]:
                    result["terminal_reason"] = "BOUND_REACHED"
                    break
            else:
                result["consecutive_failures"] = 0

            if state["observer_phase"] == "BLOCKED":
                result["terminal_reason"] = "BLOCKED_REQUIRES_ADJUDICATION"
                break
            if (
                observed["tick_result"]["decision"]["action"] == "NOOP"
                and not state["pending_heads"]
            ):
                result["terminal_reason"] = "NO_PENDING_WORK"
                break

        if result["terminal_reason"] is None:
            result["terminal_reason"] = "BOUND_REACHED"
        result["observer_state"] = state
        _write_run_result(root, result)
        return result
    except QueueCapacityError:
        result["terminal_reason"] = "QUEUE_CAPACITY_REQUIRES_ADJUDICATION"
        result["observer_state"] = state
        _write_run_result(root, result)
        return result
    except ReconciliationError:
        result["terminal_reason"] = "RECONCILIATION_REQUIRED"
        result["observer_state"] = state
        _write_run_result(root, result)
        return result
    except Exception:
        result["terminal_reason"] = "FATAL_INCONSISTENCY"
        result["observer_state"] = state
        _write_run_result(root, result)
        return result
    finally:
        release_ownership(root, ownership)

~~~
