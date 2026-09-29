# E1-08A-R1 — AUTHORITY BINDING + REAL-RUN ORCHESTRATION CLOSURE — QUALIFICATION

Date: 2026-09-29

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`

Qualified persisted HEAD:

`5c5746990d0d1cce8b2a3c5cbb85cb8144116ec4`

Qualified persisted TREE:

`fdd1b822911904cf331ad548054160935f49a8ec`

GitHub Actions qualification run:

`36537791106`

GitHub Actions job:

`109305754371`

## 1. Scope

R1 was explicitly human-authorized to close the four blockers found by the E1-08B draft review without computing real Momentum OOS performance.

Authorized scope:

```text
authority HEAD/TREE binding
human decision reference binding
bounded real Source-B Parquet → E1 runner orchestration
exact Parquet runtime environment
synthetic/identity-only qualification
HARD STOP
```

Forbidden throughout:

```text
REAL E1 RUN
REAL OOS PERFORMANCE
automatic rerun
strategy change
OOS change
MT5
paper
broker
live
capital
```

## 2. Frozen preregistration

```text
R1 contract =
d4155af3fa5e1db2abfd3902469b9ae332434464

R1 breaker =
eaf8dc6846f30a068c3a6cbebb3286e188e419d9

R1 real-run requirements =
8a047b50d76c12784c9b0bee7b6f2a629df60fd5

R1 qualification workflow =
30e7c9146c169a872d6871b8e7796985b5eb6516
```

Exact runtime environment frozen by R1:

```text
Python = 3.12.14
pyarrow = 25.0.1
```

## 3. Test-first RED

RED HEAD:

`18b320214c47d5a93d61d795920489fee1a2374c`

RED TREE:

`eb37b167c78e87b5d3a452dae8d0a0bf4545f211`

RED workflow run/job:

`36536996640 / 109303214432`

Observed:

```text
22 preregistered test families
26 executable cases after parametrization

PASS = 0
FAIL = 26

UNIQUE FAILURE =
E1_08A_R1_TARGET_ABSENT_EXPECTED_RED
```

Environment precondition before RED:

`R1_ENVIRONMENT = PASS`

Adjudication:

`E1_08A_R1_TEST_FIRST_RED = PASS_EXPECTED_FAILURE`

## 4. Minimal additive runtime

Target:

`tools/e1_08a_r1_real_run.py`

Qualified target blob:

`d3e9c848f5585346048e1a911d82cdf865b06e85`

R1 is additive.

The previously qualified E1-08A executor remains byte-identical:

`a4a04a7f63546e09d43f8c043d41872ec973a900`

No E1-01→E1-08A frozen technical artifact was modified.

## 5. B01 — exact HEAD/TREE authority binding — CLOSED

R1 adds a strict real-run authority verifier.

A valid one-shot authority must now bind exactly:

- current observed Git HEAD;
- current observed Git TREE;
- exact R1 executor blob;
- frozen protected bindings;
- exact Source-B manifest;
- exact H1 JSONL;
- exact OOS window;
- max_runs = 1.

Adversarial HEAD and TREE substitutions are BLOCKED.

The real-run runtime independently observes Git identity through `git rev-parse`; HEAD/TREE are not merely copied from the authority payload.

```text
E1-08B-B01 = CLOSED_BY_R1
```

## 6. B02 — human authority reference — CLOSED

A future E1-08B authority must contain:

```text
HUMAN_DECISION_SHA256:<64 lowercase hex>
```

The exact reference supplied to the runtime must equal the reference inside the authority payload.

`authorized_at_utc` must be an explicit UTC `Z` timestamp.

Malformed, missing or substituted human references are BLOCKED.

```text
E1-08B-B02 = CLOSED_BY_R1
```

This is a mechanical binding to the exact human-decision text digest. It is not represented as independent cryptographic proof of human identity.

## 7. B03 — real Source-B Parquet → runner orchestration — CLOSED

R1 now provides a bounded real-run path that:

1. observes exact Git HEAD/TREE;
2. verifies the strict one-shot authority;
3. verifies output paths are unused and outside the source corpus;
4. revalidates protected runtime Git blobs;
5. verifies the exact Source-B manifest;
6. verifies the exact H1 JSONL + canonical H1 stream;
7. persists the OOS exposure declaration before strategy execution;
8. consumes the one-shot authorization using exclusive creation;
9. streams Source-B Parquet through a monotone single-pass cursor;
10. delegates unchanged to E1-05 and E1-04;
11. builds the frozen E1 result;
12. wraps the result with corrected R1 provenance and the preserved E1-07 legacy trace;
13. writes result and trace with exclusive-create semantics.

The raw cursor never materializes the 376,003,618-tick corpus in memory.

It preserves source order and reads only:

```text
timestamp
bid_price
ask_price
```

No sorting, deduplication, repair, interpolation or forward filling is performed.

```text
E1-08B-B03 = CLOSED_BY_R1
```

## 8. Parquet integrity and monotone cursor

For every file reached by the cursor:

- manifest relative path is validated;
- expected size is checked;
- SHA-256 is recomputed before tick emission;
- Parquet schema is checked;
- original Arrow schema metadata is checked when present;
- timestamp semantics must be `timestamp[ms]`;
- bid/ask must be floating values;
- prices must be finite and positive;
- ask < bid is blocked;
- timestamps must be strictly increasing across batches and files.

Continuity mapping remains:

```text
delta <= 60,000 ms → OK
delta > 60,000 ms  → FORBIDDEN_BOUNDARY
```

The cursor is stateful and single-pass. Re-iteration continues from the existing position rather than restarting the corpus.

## 9. B04 — Parquet runtime environment — CLOSED

Frozen environment:

```text
CPython 3.12.14
pyarrow 25.0.1
```

Requirements:

`requirements/e1_08a_r1_real_run.lock.txt`

The qualification workflow installed and verified this exact environment before running R1.

```text
E1-08B-B04 = CLOSED_BY_R1
```

## 10. Provenance correction without reopening E1-07

R1 identified and explicitly preserves a historical E1-07 mismatch.

The physical raw execution source is:

```text
SOURCE_B_USTECH_PRICE_CORE_V0_1
manifest =
c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5
```

The AP0 intermediate signal source is:

```text
USTECH_PROFILE_MINUTE_CORE_V0_1
manifest =
62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce
```

The H1 signal source remains:

```text
USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1

JSONL =
94ccb7c78e2e21cb3baa2dfe0945e7b39e20f74300c3c72addb89135d5af1ca0

canonical stream =
15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f
```

E1-07 is not mutated.

Instead, the R1 result/trace explicitly states that the legacy E1-07 `datasets.raw` identity/hash pair combines the Source-B label with the AP0 manifest hash.

The R1 wrapper is authoritative for the physical Source-B execution provenance of the future real E1.

## 11. Qualification path

Initial implementation replay:

```text
24/26 PASS
2/26 FAIL
```

Frozen tests identified:

1. original Parquet timestamp-unit handling;
2. E1-07 legacy execution-status vocabulary.

Corrections were limited to the R1 target.

Second replay after the semantic corrections exposed one mechanical patch defect: missing `base64` import.

No breaker was changed.

Final qualified runtime blob:

`d3e9c848f5585346048e1a911d82cdf865b06e85`

## 12. Final exact persisted-head qualification

GitHub Actions:

```text
run = 36537791106
job = 109305754371
```

Observed:

```text
R1 environment = PASS

R1 frozen breaker:
26 passed in 0.25s

existing Q8 frozen breaker:
20 passed in 0.10s

clean worktree:
PASS
```

Therefore:

```text
E1_08A_R1_BREAKER = PASS_26_OF_26
E1_08A_Q8_REBREAK = PASS_20_OF_20
```

## 13. Protected invariance

At qualified HEAD, exact blob checks confirmed unchanged identities for:

- E1-01/E1-02 freeze package;
- E1-03 runtime;
- E1-04 runtime;
- E1-05 runner;
- E1-06 independent reference;
- E1-06 qualifier;
- E1-07 runtime;
- E1-08A contract;
- E1-08A breaker;
- E1-08A executor;
- E1-08A qualification report;
- R1 contract;
- R1 breaker;
- R1 requirements;
- R1 workflow.

## 14. Adjudication

```text
E1_08A_R1_PREREGISTRATION = PASS
E1_08A_R1_TEST_FIRST_RED = PASS_EXPECTED_FAILURE
E1_08A_R1_AUTHORITY_BINDING = PASS
E1_08A_R1_HUMAN_REFERENCE_BINDING = PASS
E1_08A_R1_PARQUET_CURSOR = PASS
E1_08A_R1_REAL_RUN_ORCHESTRATION = PASS_SYNTHETIC_PARQUET_ONLY
E1_08A_R1_ENVIRONMENT_FREEZE = PASS
E1_08A_R1_PROVENANCE_BRIDGE = PASS
E1_08A_R1 = PASS

E1_08B_B01 = CLOSED
E1_08B_B02 = CLOSED
E1_08B_B03 = CLOSED
E1_08B_B04 = CLOSED
```

This does not mean a real E1 has run.

## 15. Authority state and HARD STOP

```text
E1-08A = PASS
E1-08A-R1 = PASS

E1-08B = NOT_AUTHORIZED
REAL_E1_RUN = NOT_AUTHORIZED
REAL_OOS_PERFORMANCE = NOT_OBSERVED
AUTOMATIC_RERUN = NOT_AUTHORIZED

MT5 = CLOSED
PAPER = CLOSED
BROKER = CLOSED
LIVE = CLOSED
CAPITAL = CLOSED
PHASE_22_PLUS = CLOSED

HARD_STOP = TRUE
```

Next candidate boundary:

```text
E1-08B
—
EXACT HUMAN ONE-SHOT REAL E1 AUTHORIZATION
```

A separate explicit human decision is still required before any valid authority payload can be created or any real Source-B Momentum result can be computed.
