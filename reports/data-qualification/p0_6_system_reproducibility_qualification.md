# P0.6 — SYSTEM REPRODUCIBILITY QUALIFICATION

**Date:** 16 September 2026  
**Branch:** `integration/system-v1`  
**Base P0.5:** `7ae5f3cb77d6914699df3cd1104bc02ecb3c2bf4`  
**Contract:** `SYSTEM_REPRODUCIBILITY_ENVELOPE_V1`  
**Lock schema:** `QUALIFICATION_ENVIRONMENT_LOCK_V1`  
**Tier:** A

## Verdict candidate

**PASS — `QUALIFICATION_ENVIRONMENT_IS_VERSIONED_FAIL_CLOSED_AND_P0_2_TO_P0_5_SURVIVES_LOCKED_REBREAK`**, subject only to the final documentary persisted-HEAD re-break containing this report, the P0.6 JIT audit, checkpoint, backup and final P0.6 verifier.

## Problem closed

Before P0.6, P0.2–P0.5 were behaviorally qualified but the environment that qualified them was partly ambient:

- durable workflows used `ubuntu-latest`;
- action references used moving tags `actions/checkout@v4` and `actions/setup-python@v5`;
- Python was requested as floating `3.12`;
- `pytest==8.4.2` was installed directly while resolved transitive versions were not versioned;
- no authoritative repository lock tied Python, runner family, actions, qualification packages and deterministic environment variables together.

P0.6 closes that reproducibility boundary without introducing a package-manager framework, container platform or second dependency system.

## Dependency and environment inventory

The qualified P0.2–P0.5 functional runtime uses Python standard-library modules only.

The final P0.5 qualification environment had resolved:

- CPython `3.12.14`;
- Ubuntu runner family `ubuntu-24.04` / observed Ubuntu `24.04.5`;
- `pytest==8.4.2`;
- `iniconfig==2.3.0`;
- `packaging==26.3`;
- `pluggy==1.6.0`;
- `Pygments==2.21.0`;
- `actions/checkout` commit `11d5960a326750d5838078e36cf38b85af677262`;
- `actions/setup-python` commit `a26af69be951a213d495a4c3e4e4022e16d87065`.

The observed hosted-runner image build `20260907.300.1`, runner `2.337.0`, kernel/image patch internals and Azure region are recorded as observations only. They are not falsely represented as immutable lock inputs because GitHub does not expose that image build as a stable `runs-on` target.

The optional V4.3 Parquet adapter imports `pyarrow`, but no qualified P0.2–P0.5 run installs or exercises it. P0.6 therefore records `pyarrow` as `BLOCKED_OUTSIDE_P0_6`; no arbitrary version is invented.

## Smallest authoritative lock

P0.6 adds exactly:

- `04-REFERENCE/SYSTEM-REPRODUCIBILITY-CONTRACT.md`;
- `04-REFERENCE/QUALIFICATION-ENVIRONMENT-LOCK.json`;
- `requirements/qualification.lock.txt`;
- `tools/qualification_environment.py`;
- `tests/test_system_reproducibility_tier_a.py`;
- `.github/workflows/p0-6-system-reproducibility.yml`;
- bounded reproducibility edits to the already protected P0.2–P0.5 and durable boundary workflows.

The qualification requirements lock is exactly:

- `iniconfig==2.3.0`;
- `packaging==26.3`;
- `pluggy==1.6.0`;
- `Pygments==2.21.0`;
- `pytest==8.4.2`.

Its authoritative SHA-256 is:

`4ef534add869a64dd4957ea986f7ada98dffd41f89021e1719d02d9c2062a0db`

The environment lock requires:

- CPython `3.12.14`;
- Linux;
- GitHub runner label `ubuntu-24.04`;
- `X64` under GitHub Actions;
- the two immutable action commits above;
- `PYTHONDONTWRITEBYTECODE=1`;
- `PYTHONHASHSEED=0`;
- `TZ=UTC`;
- `LANG=C.UTF-8`;
- `LC_ALL=C.UTF-8`;
- the exact package map and requirements-lock digest.

## Initial adversarial FAIL

Pre-correction HEAD:

`96762ef94fa7ec07550c17997c2bd34c8100c9e3`

Run/job:

`35145837748 / 104961521577` — **FAIL expected**.

Evidence:

- P0.5 D0–D14 remained green: `15 passed`;
- P0.6 provisional breaker: `2 failed`;
- failure 1: no authoritative environment lock / requirements lock / verifier existed;
- failure 2: protected workflows still floated runner/actions/Python and installed pytest directly;
- no acquisition/backtest side effect;
- worktree clean.

This FAIL is retained as the proof that P0.6 detected a real environmental qualification gap rather than merely documenting a green state.

## Corrected technical persisted-HEAD re-break

Technical qualification HEAD:

`e96396ab3f807144144ff548dfe771c6a0584b44`

Run/job:

`35146586182 / 104964108341` — **SUCCESS**.

Observed lock verification:

- `VERDICT=PASS`;
- `CONTRACT=QUALIFICATION_ENVIRONMENT_LOCK_V1`;
- `PYTHON=3.12.14`;
- exact five locked packages installed with `--no-deps`;
- immutable checkout/setup-python action commits were used;
- workflow permissions were `contents: read`, `metadata: read`.

Exact results:

- P0.6 E0–E12: `13 passed`;
- complete repository: `220 passed`;
- P0.5 D0–D14: `15 passed`;
- P0.4 C0–C15: `16 passed`;
- P0.2 decision Tier-A: `83 passed`;
- P0.3 calendar/freeze Tier-A: `80 passed`;
- global truth `111 / 91 / 20`: global coverage **BLOCKED**;
- selected window `68 / 68 / 0`: PASS;
- persisted freeze: PASS;
- acquisition after freeze: **BLOCKED**;
- `massive_acquisition_authorized = false`;
- `real_backtest_authorized = false`;
- `pyarrow`: explicitly outside the P0.6 envelope;
- worktree: clean.

## Adversarial coverage

The executable matrix covers:

- `E0` positive exact locked environment;
- `E1` Python implementation drift rejected;
- `E2` Python version drift rejected;
- `E3` OS drift rejected;
- `E4` GitHub runner OS/architecture drift rejected;
- `E5` deterministic environment variable missing/drift rejected;
- `E6` required package missing rejected;
- `E7` required package version drift rejected;
- `E8` requirements bytes/hash drift rejected;
- `E9` unknown/missing/substituted lock schema rejected;
- `E10` floating action tags rejected;
- `E11` floating runner/Python/direct-pytest bypass rejected while original functional test commands are preserved;
- `E12` optional `pyarrow` remains outside P0.6;
- `E13` P0.2, P0.3, P0.4 and P0.5 are re-broken under the lock;
- `E14` full repository truth, freeze and acquisition prohibitions survive.

## Workflow migration rule

P0.6 changes qualification environment semantics, not functional boundary semantics.

For P0.2 specifically, four durable YAML workflows could no longer remain byte-identical to the historical decision source because their environment had to be locked. P0.6 therefore preserves the 17 protected P0.2 functional artifacts byte-identically and replaces the old YAML byte-identity constraint with executable semantic assertions proving:

- branch-neutral `push` + `pull_request` behavior is preserved;
- `contents: read` is preserved;
- original protected test commands remain present;
- the new exact environment lock/verifier is mandatory.

This is an explicit governed evolution, not silent weakening.

## Covered by P0.6

P0.6 closes only:

- inventory of the actually qualified P0.2–P0.5 Python/test/runner/action environment;
- one exact requirements lock for the current qualification stack;
- one authoritative environment lock with machine-verifiable schema and requirements digest;
- fail-closed verification of Python implementation/version, OS, GitHub runner identity, deterministic environment and package versions;
- immutable action references;
- `ubuntu-24.04` and exact Python `3.12.14` across protected workflows;
- transportable/reconstructible qualification semantics within the supported envelope;
- preservation and re-break of P0.2–P0.5 under that lock.

## Explicitly not covered by P0.6

P0.6 does not close or authorize:

- the optional `pyarrow`/Parquet execution path;
- immutable pinning of GitHub-hosted image internals that GitHub does not expose as a stable runner target;
- non-replay cryptographic bearer attestation or signing-key lifecycle;
- native `.bi5` acquisition/readiness/authorization;
- acquisition manifests, tick completeness/exhaustiveness/reconciliation;
- exact OOS split;
- real-data backtest;
- `DECISION → RISK → ACTION → RESULT → TRACE` completion;
- complete transverse decision reconstruction;
- general resilience/restoration;
- promotion gate or live activation.

## Safety state preserved

P0.6 changes qualification reproducibility only. It does not relax permissions:

- global `111/91/20`: BLOCKED;
- selected `68/68/0`: PASS;
- persisted freeze: PASS;
- acquisition: BLOCKED;
- massive acquisition: false;
- real backtest: false.

## Closure rule

This report is a documentary closure candidate. P0.6 is durably CLOSED only when a final read-only P0.6 persisted-HEAD workflow succeeds on the exact HEAD containing:

- this report;
- `P0_6_SYSTEM_REPRODUCIBILITY_JIT_AUDIT_V1` in the existing audit register;
- the P0.6 recovery checkpoint;
- the P0.6 session backup;
- the final P0.6 verifier.

No final run identifier will be written back into these artifacts after that re-break, because doing so would move the exact persisted HEAD being qualified.
