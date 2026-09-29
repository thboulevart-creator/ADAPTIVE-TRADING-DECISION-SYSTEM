# E1-08B — EXACT ONE-SHOT AUTHORIZATION PACKAGE — DRAFT REVIEW

Date: 2026-09-29

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`

Analysis base HEAD:

`75f435578ccceca7eaf4c826a2fc3e6de2b76f32`

Analysis base TREE:

`1cd1fb1ad24964f0ab763ddd938236f9fee59bbc`

## Verdict

```text
E1_08B_DRAFT = PRODUCED
E1_08B_AUTHORIZATION = BLOCKED
REAL_E1_RUN = NOT_AUTHORIZED
REAL_OOS_PERFORMANCE = NOT_AUTHORIZED
```

The draft review found four concrete blockers before an exact one-shot authority can be considered valid.

## B01 — HEAD/TREE authority binding is not enforced

The frozen E1-08A authority schema contains:

- `authorized_base_head`
- `authorized_base_tree`

but the current runtime verifier does not compare either field against an expected persisted state.

Therefore:

```text
authority says HEAD/TREE X
runtime can still PASS
even if X is arbitrary
```

This contradicts the intended E1-08B property of exact-state authorization.

## B02 — human authority reference is not mechanically enforced

The authority schema contains:

- `human_decision_reference`
- `authorized_at_utc`

but the current verifier does not require a non-empty human decision reference and does not validate the authorization timestamp semantics.

The current runtime therefore proves payload structure/digest and several experiment bindings, but not complete human-origin authority binding.

## B03 — no qualified real-run orchestration entry point

The E1-08A executor currently exposes:

`run_synthetic_qualification(...)`

It does not expose a bounded real function or command that:

1. verifies the exact Source-B corpus;
2. reads the real Parquet files;
3. adapts them to the E1-04 raw-tick contract;
4. loads the exact qualified H1 stream;
5. consumes the one-shot authority;
6. invokes the frozen E1-05 runner;
7. persists the result/trace exactly once.

Without this frozen path, E1-08B would authorize an implementation choice made at execution time.

That is not acceptable for the first irreversible OOS observation.

## B04 — Parquet execution environment is not frozen

Real Source-B input is Parquet.

The repository contains an older read-only compatibility probe using `pyarrow.parquet`, but no exact pyarrow version has been frozen as part of E1 real execution.

The P0.6 qualification environment explicitly excluded pyarrow.

Therefore a real E1 run environment is not yet reproducibly identified.

## Self-reference resolution

The final E1-08B authority must not be stored as a file that claims its own containing commit as its authorized HEAD.

The safe sequence is:

```text
1. finish and qualify the real-run executor
2. persist that qualified state
3. obtain fresh exact HEAD/TREE
4. human authorizes THAT already-persisted HEAD/TREE
5. generate an external/run-local one-shot authority payload
   bound to that HEAD/TREE and human decision reference
6. verify it before consuming it
7. execute exactly once
8. persist result + trace
9. HARD STOP
```

Thus the final human authority record is an execution input referencing an already-existing persisted state, not a self-referential Git artifact.

## Draft candidate identity

Candidate future run id:

`E1-REAL-001`

This is only a reserved draft identifier. It grants no authority.

The persisted JSON draft deliberately contains:

```text
real_e1_run_authorized = false
authorized_base_head = null
authorized_base_tree = null
human_decision_reference = null
authorized_at_utc = null
canonical_digest = null
```

It cannot satisfy the executable E1 one-shot authority schema.

## Required next correction boundary

The next technical step is not the real run.

It is a bounded correction cycle:

```text
E1-08A-R1
—
AUTHORITY BINDING + REAL-RUN ORCHESTRATION CLOSURE
```

Minimum scope:

1. test-first breakers for exact HEAD/TREE authority binding;
2. test-first breaker for missing/invalid human decision reference;
3. minimal real Parquet→runner orchestration;
4. exact real-run dependency/environment freeze;
5. synthetic/identity-only qualification;
6. persisted-head re-break;
7. HARD STOP;
8. return to E1-08B for the separate human one-shot authorization.

No real OOS performance is needed or permitted during this correction cycle.

## Current authority

```text
E1-08A = PASS AS PREVIOUSLY QUALIFIED
E1-08B_DRAFT = PRODUCED
E1-08B = NOT_AUTHORIZED

REAL_E1_RUN = NOT_AUTHORIZED
REAL_OOS_PERFORMANCE = NOT_AUTHORIZED

MT5 = CLOSED
PAPER = CLOSED
BROKER = CLOSED
LIVE = CLOSED
CAPITAL = CLOSED
PHASE_22_PLUS = CLOSED
```
