# RECOVERY CHECKPOINT — 16 SEPTEMBRE 2026 — P0.6 SYSTEM REPRODUCIBILITY PASS / FINAL DOCUMENTARY REBREAK PENDING

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Active branch: `integration/system-v1`

## Source of truth

GitHub code, persisted qualification reports, tests, workflow evidence and this checkpoint are authoritative. Do not reconstruct governed project state from conversation memory.

Construction rule:

**UNDERSTAND → COMPARE → BREAK → DECIDE.**

Allowed verdicts: `PASS / FAIL / BLOCKED`. `BLOCKED` is never `PASS`.

## Integration lineage

Integration base:

`main@43ec28f3e09856fe508874af3aaf32079761d2d5`

P0.2 qualified decision source:

`feat/decision-producer-contract@c0116d195063c464d602fb699654ac61adc7290c`

P0.3 qualified multi-year source:

`feat/multi-year-dukascopy-acquisition@b7d13bb3492fb6e1f0d4dcab64079bf1a8f55698`

P0.4 final closed base:

`aa9551addc0fe554af9cbb8ebdb26314d37e412e`

P0.5 final closed HEAD:

`7ae5f3cb77d6914699df3cd1104bc02ecb3c2bf4`

No blind merge, rebase, reset, force-push or branch-history replay is authorized by this checkpoint.

## P0.6 — SYSTEM REPRODUCIBILITY

Contract:

`04-REFERENCE/SYSTEM-REPRODUCIBILITY-CONTRACT.md`

Contract ID:

`SYSTEM_REPRODUCIBILITY_ENVELOPE_V1`

Environment lock:

`04-REFERENCE/QUALIFICATION-ENVIRONMENT-LOCK.json`

Lock schema:

`QUALIFICATION_ENVIRONMENT_LOCK_V1`

Requirements lock:

`requirements/qualification.lock.txt`

Requirements SHA-256:

`4ef534add869a64dd4957ea986f7ada98dffd41f89021e1719d02d9c2062a0db`

Verifier:

`tools/qualification_environment.py`

Tier-A tests:

`tests/test_system_reproducibility_tier_a.py`

Workflow:

`.github/workflows/p0-6-system-reproducibility.yml`

Qualification report:

`reports/data-qualification/p0_6_system_reproducibility_qualification.md`

Session backup:

`99-BACKUP/SESSION-2026-09-16-P0.6-SYSTEM-REPRODUCIBILITY-PASS.md`

JIT audit marker:

`P0_6_SYSTEM_REPRODUCIBILITY_JIT_AUDIT_V1`

## Locked qualification envelope

Authoritative current qualification environment:

- implementation: CPython;
- Python: `3.12.14`;
- OS family: Linux;
- GitHub runner: `ubuntu-24.04`;
- GitHub runner architecture: `X64`;
- checkout action commit: `11d5960a326750d5838078e36cf38b85af677262`;
- setup-python action commit: `a26af69be951a213d495a4c3e4e4022e16d87065`;
- `PYTHONDONTWRITEBYTECODE=1`;
- `PYTHONHASHSEED=0`;
- `TZ=UTC`;
- `LANG=C.UTF-8`;
- `LC_ALL=C.UTF-8`.

Exact qualification packages:

- `iniconfig==2.3.0`;
- `packaging==26.3`;
- `pluggy==1.6.0`;
- `Pygments==2.21.0`;
- `pytest==8.4.2`.

The GitHub-hosted image build (`20260907.300.1` in the technical proof), runner patch version and cloud region are observational evidence only, not lock fields.

`pyarrow` remains explicitly `BLOCKED_OUTSIDE_P0_6`; no unqualified Parquet dependency version was invented.

## Initial Tier-A FAIL

Pre-correction HEAD:

`96762ef94fa7ec07550c17997c2bd34c8100c9e3`

Run/job:

`35145837748 / 104961521577` — **FAIL expected**.

Evidence:

- P0.5 D0–D14 still passed: `15 passed`;
- provisional P0.6 breaker exposed two independent failures;
- authoritative lock/verifier was absent;
- protected workflows still floated runner/actions/Python/direct pytest installation;
- no acquisition/backtest side effect;
- worktree clean.

## Corrected technical persisted-HEAD qualification

HEAD:

`e96396ab3f807144144ff548dfe771c6a0584b44`

Run/job:

`35146586182 / 104964108341` — **SUCCESS**.

Exact results:

- environment verifier: PASS (`QUALIFICATION_ENVIRONMENT_LOCK_V1`, Python `3.12.14`);
- P0.6 E0–E12: `13 passed`;
- complete repository: `220 passed`;
- P0.5 D0–D14: `15 passed`;
- P0.4 C0–C15: `16 passed`;
- P0.2 decision Tier-A: `83 passed`;
- P0.3 calendar/freeze Tier-A: `80 passed`;
- exact locked packages installed with `--no-deps`;
- immutable action commits: PASS;
- optional `pyarrow` outside envelope: PASS;
- worktree clean;
- permissions read-only.

## P0.2 migration safety

P0.6 necessarily changes the four durable decision workflow YAML files, so historical byte identity for those YAML files is no longer the correct invariant.

The governed replacement is stricter where it matters:

- 17 P0.2 protected functional artifacts remain source-identical;
- durable workflows remain branch-neutral, PR-covered and read-only;
- original protected test commands remain present;
- exact runner/Python/actions/packages/verifier are now required;
- P0.2 re-break remains `83 passed` under the lock.

This is an explicit governed environment evolution, not a relaxation of the decision boundary.

## Current multi-year safety truth

Still re-derived unchanged:

- global candidates/resolved/unresolved: `111 / 91 / 20`;
- global coverage: **BLOCKED**;
- selected execution window: `2021-08-14 → 2026-08-14`;
- selected-window candidates/resolved/unresolved: `68 / 68 / 0`;
- persisted freeze: **PASS**;
- acquisition after persisted freeze: **BLOCKED**;
- persisted `massive_acquisition_authorized = false`;
- persisted `real_backtest_authorized = false`.

## Covered by P0.6

P0.6 closes only:

- actual qualified dependency/environment inventory for P0.2–P0.5;
- exact qualification requirements lock;
- authoritative machine-verifiable environment lock;
- fail-closed environment/package/schema verification;
- immutable action references;
- exact Python and stable runner-family references in protected workflows;
- deterministic qualification environment variables;
- adversarial version/missing-dependency/environment/workflow drift attacks;
- re-break of P0.2–P0.5 and full repository under the lock.

## Explicitly NOT covered by P0.6

Still open / not authorized:

- optional `pyarrow` / Parquet execution path;
- immutable GitHub-hosted image-build pinning unavailable via stable runner labels;
- non-replay cryptographic bearer attestation and signing-key lifecycle;
- native `.bi5` acquisition/readiness/authorization;
- acquisition manifests and tick completeness/reconciliation;
- exact OOS split;
- real-data backtest;
- `DECISION → RISK → ACTION → RESULT → TRACE` completion;
- complete transverse decision reconstruction;
- general resilience/restoration;
- promotion gate or live activation.

Historical broad governance verdicts remain unchanged outside this bounded scope:

- Decision Traceability: **FAIL globally** until the downstream chain is proven;
- Resilience / Continuity: **FAIL**;
- Governance Effectiveness: **BLOCKED globally**, despite bounded JIT PASSes.

## Documentary closure status

The P0.6 technical boundary is qualified PASS.

This checkpoint is part of the documentary closure candidate. P0.6 becomes durably CLOSED only after a final read-only persisted-HEAD P0.6 re-break succeeds on the exact HEAD containing:

- this checkpoint;
- `GOVERNANCE/GOVERNANCE-AUDIT-REGISTER.md` with `P0_6_SYSTEM_REPRODUCIBILITY_JIT_AUDIT_V1`;
- `reports/data-qualification/p0_6_system_reproducibility_qualification.md`;
- `99-BACKUP/SESSION-2026-09-16-P0.6-SYSTEM-REPRODUCIBILITY-PASS.md`;
- the final P0.6 persisted-HEAD workflow.

No final run ID is written back after that successful execution because such a write would move the qualified HEAD.

## Mandatory recovery order before next substantive block

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-16-P0.6-SYSTEM-REPRODUCIBILITY-PASS.md`
4. `reports/data-qualification/p0_6_system_reproducibility_qualification.md`
5. `GOVERNANCE/GOVERNANCE-AUDIT-REGISTER.md`
6. `04-REFERENCE/SYSTEM-REPRODUCIBILITY-CONTRACT.md`
7. `04-REFERENCE/QUALIFICATION-ENVIRONMENT-LOCK.json`
8. `requirements/qualification.lock.txt`
9. `tools/qualification_environment.py`
10. `tests/test_system_reproducibility_tier_a.py`
11. `.github/workflows/p0-6-system-reproducibility.yml`
12. P0.5 contract/workflow/runtime/tests and final closed evidence
13. P0.4, P0.3 and P0.2 regression guards
14. verify branch HEAD and latest successful final P0.6 persisted-HEAD re-break before mutation.

## Exactly one next governed action after final P0.6 documentary re-break

**P1 — formalize and adversarially qualify an early fail-closed/reject-all promotion gate before any permissive capability promotion, live activation or governance relaxation path.**

P1 must initially deny promotion by default and must not authorize acquisition or real backtest merely because the qualification environment is reproducible.
