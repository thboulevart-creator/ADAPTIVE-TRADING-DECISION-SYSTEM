# ATDS — OBSIDIAN P5-E SESSION CHECKPOINT — END OF DAY

Date: 2026-10-01
Purpose: exact restart point for the next session.

## Discussion identity

This checkpoint belongs to:

`ATDS — OBSIDIAN PROJECTION / P5-D4 → P5-E NEAR-REAL-TIME`

It does not belong to Family Agent System, Cross-System / Architecture Moat, or the E1 trading/backtest workstream.

## Repository identity at checkpoint

Repository:
`thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch:
`feat/obsidian-projection-p5e-v0.1-external-review-targeted-closure`

HEAD before checkpoint persistence:
`a7931cc29132cb847beba03810ef23d84a9011a4`

Remote HEAD before checkpoint persistence:
`a7931cc29132cb847beba03810ef23d84a9011a4`

Worktree before checkpoint persistence:
`CLEAN`
## Stable predecessor state

P5-D4 real bounded observer loop:

```text
P5-D4
= QUALIFIED_AND_HUMAN_ADOPTED
```

P5-D4 runtime blob:

`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

The P5-D4 real control state was not mutated by P5-E contract/synthetic work.

Real P5-E remained closed throughout the day.

## What was completed today — P5-E V0.1 initial candidate

P5-E was opened in governed contract-first/test-first mode.

The first candidate froze inherited P5-A timing parameters:

```text
POLL_INTERVAL = 30 seconds
MAX_DETECTION_LATENCY = 60 seconds
```

The initial contract/synthetic candidate reached:
``text
PREREGISTRATION = PASS
RED TEST-FIRST = PASS
MINIMAL GREEN = 17 / 17 PASS
ADVERSARIAL = 42 / 42 PASS
TARGETED PREDECESSOR REGRESSION = 208 / 208 PASS
CROSS-CUTTING REGRESSION = 876 / 876 PASS
FULL OBSIDIAN RE-BREAK = 1466 / 1466 PASS
```

That candidate was deliberately not treated as real P5-E qualification.

## First external Claude review

The first external adversarial review returned:

`VERDICT = FAIL`

It raised B1→B5.

Internal adjudication concluded:

```text
B1 = CONFIRMED_BLOCKING_WITH_UPSTREAM_COVERAGE_NUANCE
B2 = CONFIRMED_BLOCKING
B3 = CONFIRMED_BLOCKING
B4 = CONFIRMED_BLOCKING
B5 = PARTIALLY_CONFIRMED_BLOCKING_SEMANTIC_GAP
```
## B1→B5 targeted closure completed today

A separately authorized targeted-closure amendment was opened.

It produced:

```text
B1→B5 TARGETED GREEN = 45 / 45 PASS
REQUIREMENT / EVIDENCE MATRIX = 43 / 43 MAPPED
UNMAPPED = 0
DEFERRED = 0
MATRIX TESTS = 5 / 5 PASS
COMBINED TARGETED P5-E = 50 / 50 PASS
TARGETED PREDECESSOR REGRESSION = 270 / 270 PASS
FULL OBSIDIAN RE-BREAK = 1474 / 1474 PASS
```

The full-suite budget for that amendment was consumed exactly once.

Corrected P5-E contract blob:

`b0668b4dff65b8e30ee0d93a3e5a3fe42c4421dd`

Corrected P5-E synthetic model blob:

`b783717c9e9596b585b7b1686835c73fffbd1a7c`
Requirement/evidence matrix blob:

`0440175fbb79877e466119cb973ea82389a4ecd8`

The candidate claim after this closure was only:

`P5E_V0_1_TARGETED_CLOSURE_CANDIDATE_QUALIFIED_PENDING_EXTERNAL_REREVIEW`

Not claimed:

- real P5-E end-to-end qualification;
- real 60-second SLA;
- continuous synchronization qualification;
- per-transient-tip detection SLA;
- automatic evaluation;
- automatic promotion;
- automatic publication.

## Second external Claude re-review — current external result

The second external re-review has now returned:

`VERDICT = FAIL`

The complete external response is persisted verbatim at:

`reports/program/2026-10-01-OBSIDIAN-P5E-V0.1-TARGETED-CLOSURE-EXTERNAL-REREVIEW-CLAUDE-RETURN.md`

The FAIL now rests on one demonstrated blocker:

`BB1 — B1 closure remains incomplete because normative contract leaves can be mutated without breaking the 50 P5-E tests.`
## BB1 — exact current blocker

Claude reports an exhaustive leaf mutation sweep:

```text
154 contract-leaf mutations attempted
36 survive
```

The critical issue is not that current values are wrong.

The current values are reported as correct.

The blocker is that some normative values are not strictly guarded, so a future drift can reintroduce B4 or other prohibited semantics while tests still pass.

Minimal demonstrated regression includes changing together:

- `near_real_time_timing.detection_latency_definition` back to remote-availability semantics;
- `future_real_bound_clock` to `WALL_CLOCK`;
- `future_real_wall_clock_may_be_recorded_as_evidence_only` to false;
- `latency_bound_breach_must_not_be_reported_as_near_real_time_pass` to false;
- `monitored_source.branch` to `main`;
- burst catch-up guard to false.

External reproduction result remained:

`Ran 50 tests ... OK`

Therefore BB1 is a real guard-coverage defect.
### Normative areas reported as insufficiently guarded

Claude identified surviving normative leaves in at least:

- `monitored_source`;
- `near_real_time_timing`;
- `head_transition_policy`;
- `queue_and_supersession`;
- `end_to_end_definition`;
- `real_context_evidence_only`;
- `tip_visibility_semantics`;
- `external_review_targeted_closure`.

The evidence matrix also does not currently pin the exact covered contract blob and model blob.

Therefore contract/model drift can leave the matrix looking valid.

## Non-blocking findings to adjudicate tomorrow

Claude also returned NB1→NB9.

They must be adjudicated, not automatically adopted.

### NB1 — read crosses next fixed-rate slot

A read starting at 30 and completing at 61 can still PASS at latency 60 although the 60-second slot did not start.

This conflicts with the preregistered requirement that required slots be present until terminal result.

### NB2 — ambiguous B → A observation order

The model can PASS when a different head B is observed after release and target A appears later.

The model lacks enough pre-release state to distinguish lag, third-party push, or rollback.
### NB3 — stateless classify_tip_visibility

Containment is caller-supplied and not independently verified.

It is currently not connected to a queue decision path, so Claude classifies this non-blocking.

### NB4 — part of B5 closure remains declarative

The rule that an unobserved intermediate tip must not enter the queue is not executable yet because the future observation adapter does not exist.

It should be described as a rule, not as an already-qualified runtime property.

### NB5 — D2 evidence depends on caller-supplied transition classification

D2 correctly reacts to NON_FAST_FORWARD / UNKNOWN labels, but does not prove the ancestry classifier that supplied those labels is correct.

This is predecessor behavior outside the current closure.

### NB6 — semantic mismatches in evidence matrix

Some entries map pending-head semantics to tests covering active-head semantics.

Queue replacement/coalescing entries are labelled DIRECT_P5E although behavioral proof also exists in P5-D4 queue-capacity tests.

### NB7 — residual vocabulary / guards

`INCOMPLETE_SYNTHETIC_WINDOW` is not declared in the contract as a non-PASS status.

Duplicate slots are labelled `CADENCE_GAP`.

AST purity guard can theoretically be bypassed through dynamic builtin access, although the current model is pure.
### NB8 — evidence discipline

Claude could not independently verify the persisted 270/270 and 1474/1474 run records.

It recommends a future full pass, if one is authorized, preferably in a disposable clone and with stronger pre/post state fingerprints.

### NB9 — prerequisites for any future real protocol

Before any real experiment, the following must be frozen:

- exact meaning of `CONTROLLED_SOURCE_RELEASE_MONOTONIC`;
- same monotonic clock domain for release and reader;
- exact release ref;
- authority to push to that ref;
- no silent mutation of canonical `integration/system-v1`.

These are not current-candidate blockers but are mandatory before real P5-E preregistration.

## External reviewer recommendation

The external reviewer recommends mechanically:

1. strict invariants for the surviving normative fields;
2. pin covered contract and model blobs in the evidence matrix and test them;
3. rerun exhaustive leaf mutation sweep as an exit criterion;
4. optionally close NB1 / NB6 / NB7 in the same pass;
5. defer NB2 / NB3 / NB4 / NB9 to future real-experiment preregistration where appropriate.

No external review creates authority.
## Exact current boundary

At end of day:

```text
SECOND_EXTERNAL_REREVIEW = FAIL
BLOCKING_FINDINGS = 1
CURRENT_BLOCKER = BB1
BB1_INTERNAL_ADJUDICATION = NOT_YET_DONE
NB1_TO_NB9_INTERNAL_ADJUDICATION = NOT_YET_DONE
NEW_CORRECTION_AMENDMENT = NOT_OPENED
HUMAN_NORMATIVE_ADOPTION = CLOSED
REAL_P5E = CLOSED
P6 = CLOSED
```

No BB1 correction is authorized merely by this checkpoint.

## Correct restart sequence for next session

Resume in this exact order:

1. Fresh read-only repository / branch / HEAD / worktree verification.
2. Read the persisted Claude re-review return.
3. Internally adjudicate BB1:
   - CONFIRMED / PARTIAL / REJECTED;
   - reproduce the minimal mutation if useful;
   - identify exact normative leaves requiring guards.
4. Internally adjudicate NB1→NB9 individually.
5. Decide which NB findings belong to the same closure versus future real-experiment preregistration.
6. Produce a minimal correction plan only.
7. STOP and request / consume explicit human authorization before any BB1 mutation.
If a BB1 closure is later authorized, expected high-level path is:

```text
PREREGISTER BB1 TARGETED CLOSURE
→ RED mutation-sweep / object-binding tests
→ minimal strict guard corrections
→ pin contract + model in evidence matrix
→ exhaustive normative leaf mutation sweep
→ targeted regressions
→ one authorized full-suite only if explicitly allowed
→ new self-contained external review packet
→ external re-review
→ human normative adjudication only after external closure
```

## Do-not-cross boundaries

Until separately authorized:

- no real polling loop;
- no real HEAD evaluation;
- no Stage A;
- no Stage B;
- no promotion;
- no publication;
- no Vault or CURRENT mutation;
- no daemon;
- no Scheduled Task;
- no Windows Service;
- no startup registration;
- no P6;
- no automatic human adoption.

`REAL_P5E = CLOSED`

## Restart phrase

The next session may safely resume from:

`P5-E V0.1 — SECOND EXTERNAL REREVIEW FAIL / BB1 INTERNAL ADJUDICATION`
