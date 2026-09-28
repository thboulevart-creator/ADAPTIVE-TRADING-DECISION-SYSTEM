# E1-03 — H1 DATASET IDENTITY — TEST-FIRST RED

Date: 2026-09-28

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`  
Reviewed persisted HEAD: `ebca9292f7fbafcff6facb3997f261ba0b718c60`  
Reviewed persisted TREE: `e5c2a569efc4f4431522fc977f28e45e8186bc8e`

## 1. Scope

This artifact records the preregistered TEST-FIRST RED for E1-03 only.

It does not authorize or contain:

- the E1-03 transformer implementation;
- a real AP0 → H1 build;
- Momentum signal generation;
- positions;
- trades;
- PnL;
- backtest execution;
- E1 execution.

## 2. Persisted governing identities

Contract:

`GOVERNANCE/E1-03-H1-DATASET-IDENTITY-CONTRACT-V0.1.json`

Contract blob:

`c2d4323039d65fcd9319d4f5eb02f45ee27c8afc`

Breaker:

`breakers/e1_03_h1_dataset_identity_red_breaker.py`

Breaker blob:

`958e338a1e9e7c5b56198eb3585f25ca140aa331`

Runtime target:

`tools/e1_03_h1_dataset_identity.py`

Persisted runtime state at reviewed HEAD:

`ABSENT`

The breaker contains exactly 21 frozen cases:

`H1-01 → H1-21`

## 3. Fresh RED execution

The persisted contract and breaker bytes were re-executed before this evidence persistence.

Observed execution profile:

```text
PY_COMPILE = PASS
PYTEST_EXIT_CODE = 1

TOTAL_TESTS = 21
FAILED = 21
COLLECTION_ERRORS = 0
```

All 21 failures had the same expected causal marker:

```text
E1_03_H1_TRANSFORMER_ABSENT_EXPECTED_RED
```

No semantic runtime failure is claimed because the runtime does not exist.

The RED is successful only because the preregistered executable surface fails for the exact expected preimplementation reason.

An unrelated environment warning was observed during the execution environment warmup. It did not prevent Python compilation, pytest collection or execution and is not treated as E1-03 evidence.

## 4. Adjudication

```text
E1_03_TEST_FIRST_CONTRACT_PERSISTENCE = PASS
E1_03_BREAKER_PERSISTENCE = PASS

E1_03_TEST_FIRST_RED = PASS_EXPECTED_FAILURE

E1_03_IMPLEMENTATION = ABSENT
E1_03_REAL_H1_BUILD = NOT_STARTED
E1_03 = BLOCKED
```

The RED establishes only:

```text
PERSISTED CONTRACT
+
PERSISTED 21-CASE BREAKER
+
ABSENT RUNTIME
+
21/21 EXPECTED ABSENCE FAILURES
=
VALID TEST-FIRST RED
```

It does not establish correctness of a future transformer.

## 5. Frozen upstream executable constraint

The following objects are now upstream constraints for any future E1-03 implementation:

```text
contract blob =
c2d4323039d65fcd9319d4f5eb02f45ee27c8afc

breaker blob =
958e338a1e9e7c5b56198eb3585f25ca140aa331
```

The 21 frozen tests must not be weakened or modified merely to make a future implementation pass.

Any later implementation candidate must be judged against these exact persisted bytes unless a separately governed contract revision is explicitly authorized.

## 6. Next governed boundary

After persisted-head verification of this report and checkpoint append, the next candidate development boundary is:

```text
E1-03 — MINIMAL IMPLEMENTATION CANDIDATE
```

That boundary is not authorized by this report.

A separate human authorization is required before creating:

`tools/e1_03_h1_dataset_identity.py`

No real H1 build, Momentum, PnL or E1 run is authorized.
