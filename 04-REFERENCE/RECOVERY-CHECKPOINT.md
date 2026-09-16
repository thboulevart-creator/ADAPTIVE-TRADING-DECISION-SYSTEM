# RECOVERY CHECKPOINT — 16 SEPTEMBRE 2026 — P0.6 CLOSED / P1.0 WIP PAUSED SAFELY

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Active branch: `integration/system-v1`

## Source of truth

GitHub code, persisted qualification reports, workflow evidence, the end-of-day backup and this checkpoint are authoritative. Do not reconstruct governed state from conversation memory.

Construction rule:

**UNDERSTAND → COMPARE → BREAK → DECIDE.**

Allowed verdicts: `PASS / FAIL / BLOCKED`. `BLOCKED` is never `PASS`.

## Closed integration lineage

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

P0.6 final closed HEAD:

`8061127c148f06454dac6e7977a8d0cb921276f8`

No blind merge, rebase, reset, force-push or branch-history replay is authorized by this checkpoint.

## P0.6 — DURABLY CLOSED

Contract:

`04-REFERENCE/SYSTEM-REPRODUCIBILITY-CONTRACT.md`

Environment lock:

`04-REFERENCE/QUALIFICATION-ENVIRONMENT-LOCK.json`

Requirements lock:

`requirements/qualification.lock.txt`

Requirements SHA-256:

`4ef534add869a64dd4957ea986f7ada98dffd41f89021e1719d02d9c2062a0db`

Final P0.6 documentary persisted-HEAD re-break:

- HEAD: `8061127c148f06454dac6e7977a8d0cb921276f8`
- run/job: `35147651568 / 104967695069`
- conclusion: **SUCCESS**.

The previous checkpoint wording `FINAL DOCUMENTARY REBREAK PENDING` is superseded. P0.6 is now **CLOSED / PASS**.

Qualified locked envelope:

- CPython `3.12.14`;
- Linux / `ubuntu-24.04`;
- X64 in GitHub Actions;
- immutable checkout action `11d5960a326750d5838078e36cf38b85af677262`;
- immutable setup-python action `a26af69be951a213d495a4c3e4e4022e16d87065`;
- `PYTHONDONTWRITEBYTECODE=1`;
- `PYTHONHASHSEED=0`;
- `TZ=UTC`;
- `LANG=C.UTF-8`;
- `LC_ALL=C.UTF-8`;
- exact packages `iniconfig==2.3.0`, `packaging==26.3`, `pluggy==1.6.0`, `Pygments==2.21.0`, `pytest==8.4.2`.

Final qualification evidence preserved:

- P0.6 E0–E12: `13 passed`;
- complete repository technical qualification: `220 passed`;
- P0.5 D0–D14: `15 passed`;
- P0.4 C0–C15: `16 passed`;
- P0.2 decision Tier-A: `83 passed`;
- P0.3 calendar/freeze Tier-A: `80 passed`;
- worktree clean;
- final persisted-head documentary gate: SUCCESS.

`pyarrow` remains outside the qualified envelope.

## Last qualified safety truth

At the closed P0.6 baseline:

- global candidates/resolved/unresolved: `111 / 91 / 20`;
- global coverage: **BLOCKED**;
- selected execution window: `2021-08-14 → 2026-08-14`;
- selected-window candidates/resolved/unresolved: `68 / 68 / 0`;
- persisted freeze: **PASS**;
- acquisition after persisted freeze: **BLOCKED**;
- persisted `massive_acquisition_authorized = false`;
- persisted `real_backtest_authorized = false`;
- no native `.bi5` acquisition authorized;
- no real-data backtest authorized;
- no live activation authorized.

## P1.0 — WIP PAUSED, NOT QUALIFIED

A UI timeout occurred while P1.0 was being started. GitHub writes nevertheless reached the repository.

Exact P1.0 implementation anchor before the end-of-day documentary save:

`c0eef01a505688488a9720d58bad4907ef3d2a18`

Commit message:

`p1.0: formalize fail-closed promotion and tiering contract`

This anchor is 9 commits ahead of the closed P0.6 baseline and modifies/adds exactly these eight P1-related integration surfaces:

1. `.github/workflows/p0-3-multi-year-integration-rebreak.yml`
2. `.github/workflows/p1-0-promotion-gate.yml`
3. `04-REFERENCE/PROMOTION-GATE-CONTRACT.md`
4. `04-REFERENCE/PROMOTION-GATE-TIERING-CONTRACT.md`
5. `src/promotion_gate.py`
6. `tests/test_promotion_gate_acquisition_binding.py`
7. `tests/test_promotion_gate_tier_a.py`
8. `tools/frozen_execution_window.py`

End-of-day recovery backup created immediately after that implementation anchor:

`99-BACKUP/SESSION-2026-09-16-END-OF-DAY-P0.6-CLOSED-P1.0-WIP.md`

Backup creation commit:

`2682baa8d5e9d7a0984518dfa09dbe41278f4411`

The current branch HEAD after this checkpoint update is a documentary pause state on top of the same P1.0 implementation. It MUST NOT be interpreted as a qualified P1.0 HEAD.

## Current P1.0 intended model

P1.0 is intended to enforce:

`REQUESTED TRANSITION → CONSEQUENCE → DERIVED TIER → BOUNDARY MAX-TIER → PERMISSION DELTA → RELAXATION CHECK → EVIDENCE → GATE → BLOCKED / FAIL`

Current WIP intent:

- fail-closed / reject-all by default;
- no P1.0 `PASS` promotion path;
- explicit permission ordering;
- tier derived from consequences rather than caller preference;
- boundary inherits maximum relevant tier;
- caller cannot lower a derived tier;
- Tier `A → B` is a governance relaxation;
- permission increase is a relaxation;
- Tier-A relaxation evidence must cover observability, timely detection, bounded blast radius, executable revocation, rollback/safe state, monitor independence, falsifiability and bounded/known revocation cost;
- 30-day governance-relaxation cooling-off remains applicable;
- more restrictive transitions may be handled without creating a more permissive state;
- acquisition path is intended to be bound to the promotion gate;
- no acquisition/backtest/live side-effect surface belongs in the promotion evaluator.

## P1.0 qualification status — DO NOT MISREAD

**P1.0 verdict: WIP / UNQUALIFIED.**

There is no workflow run associated with exact implementation anchor:

`c0eef01a505688488a9720d58bad4907ef3d2a18`

Therefore:

- no P1.0 PASS exists;
- the current P1.0 implementation is not yet governed-qualified;
- no permission has been promoted;
- acquisition, backtest and live remain unauthorized;
- do not infer safety qualification merely from the presence of code/tests/contracts.

## Known P1.0 gaps to resolve first tomorrow

### Contract authority duplication

Two materially overlapping documents currently exist:

- `04-REFERENCE/PROMOTION-GATE-CONTRACT.md` — `PROMOTION_GATE_FAIL_CLOSED_V1`;
- `04-REFERENCE/PROMOTION-GATE-TIERING-CONTRACT.md` — `PROMOTION_GATE_TIERING_V1`.

They must be reconciled deliberately into one authoritative contract or an explicit non-duplicative split. Do not add a third layer.

### Workflow trigger gap

At implementation anchor `c0eef...`, `.github/workflows/p1-0-promotion-gate.yml` does not path-trigger on:

- `04-REFERENCE/PROMOTION-GATE-TIERING-CONTRACT.md`;
- `tests/test_promotion_gate_acquisition_binding.py`.

This is one reason the exact anchor had no P1.0 run. Close this gap before relying on CI.

### Targeted acquisition-binding visibility

`tests/test_promotion_gate_acquisition_binding.py` must be made explicitly visible in the targeted Tier-A P1.0 qualification, not only incidentally collected through the full repository suite.

### Existing integration edits must be audited, not trusted by existence

Before further modification read:

- `tools/frozen_execution_window.py`;
- `.github/workflows/p0-3-multi-year-integration-rebreak.yml`.

Confirm that the acquisition binding and regression-guard evolution are minimal and preserve prior qualified semantics.

### Adversarial history

Inspect intermediate P1.0 commits and workflow runs. Preserve a real expected FAIL if one exists. If no clean pre-correction FAIL exists, deliberately create the smallest legitimate red breaker before final qualification. Never invent an unobserved FAIL.

## Mandatory recovery order tomorrow

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-16-END-OF-DAY-P0.6-CLOSED-P1.0-WIP.md`
4. `99-BACKUP/SESSION-2026-09-16-P0.6-SYSTEM-REPRODUCIBILITY-PASS.md`
5. `reports/data-qualification/p0_6_system_reproducibility_qualification.md`
6. `GOVERNANCE/GOVERNANCE-AUDIT-REGISTER.md`
7. `04-REFERENCE/SYSTEM-REPRODUCIBILITY-CONTRACT.md`
8. `04-REFERENCE/QUALIFICATION-ENVIRONMENT-LOCK.json`
9. `requirements/qualification.lock.txt`
10. `04-REFERENCE/PROMOTION-GATE-CONTRACT.md`
11. `04-REFERENCE/PROMOTION-GATE-TIERING-CONTRACT.md`
12. `src/promotion_gate.py`
13. `tools/frozen_execution_window.py`
14. `tests/test_promotion_gate_tier_a.py`
15. `tests/test_promotion_gate_acquisition_binding.py`
16. `.github/workflows/p1-0-promotion-gate.yml`
17. `.github/workflows/p0-3-multi-year-integration-rebreak.yml`
18. verify branch HEAD and compare current documentary pause HEAD with implementation anchor `c0eef01a505688488a9720d58bad4907ef3d2a18` before substantive mutation.

## Exactly one next governed action tomorrow

**Resume P1.0 by reconciling the overlapping promotion/tiering contracts and closing the P1.0 workflow-trigger plus targeted acquisition-binding test gap; then execute the adversarial locked qualification and correct only observed defects.**

After that, and only if technically green:

- re-break P0.2 through P0.6 on the combined HEAD;
- re-prove global `111/91/20` BLOCKED;
- re-prove selected `68/68/0` PASS and freeze PASS;
- re-prove acquisition BLOCKED;
- persist P1.0 JIT audit/report/checkpoint/backup;
- run final read-only persisted-HEAD re-break;
- only then declare P1.0 PASS.

## End-of-day stop rule

Tonight, stop here. Do not start P1.1, acquisition, real backtest, downstream risk/action execution or live activation.

Current end-of-day verdicts:

- P0.2: **CLOSED / PASS**
- P0.3: **CLOSED / PASS**
- P0.4: **CLOSED / PASS**
- P0.5: **CLOSED / PASS**
- P0.6: **CLOSED / PASS**
- P1.0: **WIP / UNQUALIFIED — PAUSED SAFELY**
