# P1.0 PROMOTION GATE — QUALIFICATION REPORT

Date: 17 septembre 2026
Branch: `integration/system-v1`
Technical qualification HEAD: `2b7f31c5baca718e84ed90bd240dce38047271a0`
Contract: `PROMOTION_GATE_FAIL_CLOSED_V1`
Companion: `NON_NORMATIVE_QUALIFICATION_COMPANION`

## Scope

P1.0 governs whether a requested transition is a governance relaxation and whether it may be promoted. It is intentionally fail-closed and non-permissive for promotion.

Qualified chain:

`REQUESTED TRANSITION → CONSEQUENCES → DERIVED TIER → BOUNDARY MAX-TIER → PERMISSION DELTA → RELAXATION ? → EVIDENCE / REVOCATION CONDITIONS → PROMOTION GATE → PASS / FAIL / BLOCKED`

## JIT audit — P1.0

Audit ID: `P1_0_PROMOTION_GATE_JIT_AUDIT_V1`

### Covered

- one normative P1.0 authority in `04-REFERENCE/PROMOTION-GATE-CONTRACT.md`;
- `04-REFERENCE/PROMOTION-GATE-TIERING-CONTRACT.md` reduced to a non-normative qualification companion;
- tier derived from consequences, not caller preference;
- unknown or empty consequence sets rejected fail-closed by the evaluator;
- no permissive promotion path introduced;
- acquisition binding routed through the P1.0 promotion gate;
- targeted visibility of `tests/test_promotion_gate_acquisition_binding.py`;
- P1.0 workflow path coverage includes the normative contract, companion, evaluator, Tier-A tests, acquisition-binding tests and frozen execution window;
- no acquisition payload, `.bi5`, data download, real backtest or live side effect introduced by the evaluator;
- locked qualification environment inherited from closed P0.6;
- clean worktree required by CI.

### Explicitly not covered

- authorization of native `.bi5` acquisition;
- authorization of real-data backtest;
- live activation;
- downstream `DECISION → RISK → ACTION → RESULT → TRACE` completion;
- global historical coverage closure: global truth remains `111 / 91 / 20` and BLOCKED.

## Adversarial history

Observed real pre-correction FAIL:

- HEAD: `2ec769a47c53a3238b2fbfa27095919156ae94f8`
- run/job: `35148892189 / 104971854140`
- verdict: FAIL.

Corrective authority / qualification commit:

- `4a26ec16544abb05a67263654b5caaa5fd6825d4`
- message: `p1.0: close contract authority and qualification gaps`.

Closed-block documentary composability correction:

- `0d654ca14639979c0e3cf51e283ca392b66e7fe2`
- P0.4 run `35195823138` — SUCCESS;
- P0.5 run `35195823085` — SUCCESS;
- P0.6 run `35195823123` — SUCCESS.

Persisted-head P1.0 technical qualification trigger:

- HEAD: `2b7f31c5baca718e84ed90bd240dce38047271a0`
- trigger change: semantically neutral workflow comment only;
- P1.0 run/job: `35197201298 / 105123138906` — SUCCESS;
- P0.3 regression guard run/job: `35197201285 / 105123138752` — SUCCESS.

P1.0 successful steps include:

- exact persisted HEAD and closed P0.6 ancestry;
- bounded and non-permissive P1.0 surface;
- exact locked qualification packages;
- P0.6 environment verification and attacks;
- P1.0 promotion-gate and acquisition-binding adversarial tests;
- clean worktree.

## Safety truth preserved

- global candidates/resolved/unresolved: `111 / 91 / 20`;
- global coverage: **BLOCKED**;
- selected execution window: `2021-08-14 → 2026-08-14`;
- selected-window candidates/resolved/unresolved: `68 / 68 / 0`;
- persisted freeze: **PASS**;
- acquisition after persisted freeze: **BLOCKED**;
- `massive_acquisition_authorized = false`;
- `real_backtest_authorized = false`;
- no live activation authorized.

## Closure rule

This report is the documentary closure candidate. P1.0 becomes **CLOSED / PASS** only if the final read-only persisted-HEAD P1.0 re-break, triggered after this report/checkpoint/backup are persisted, completes SUCCESS on the resulting HEAD. The trigger may differ only by a semantically neutral CI comment. No additional documentary mutation is required after that successful final run; this avoids an infinite documentation/requalification loop.

Until that run succeeds: **P1.0 = QUALIFIED CANDIDATE / FINAL REBREAK PENDING**.
