# P5-D4 — BOUNDED OBSERVER LOOP RUNTIME V0.1 — QUALIFICATION

Date: 2026-09-30

## Scope

This qualification covers the P5-D4 bounded observer loop runtime implementation candidate only.

It qualifies a finite, synthetic, isolated orchestration runtime over the already-qualified P5-D2/P5-D3 boundaries.

It does not authorize or claim:
- permanent background execution;
- real repeated polling;
- sleep/timer scheduling;
- Windows startup, Scheduled Task, or Windows Service;
- automatic P5-D3F/P5-D3G promotion;
- implicit Stage A or Stage B authority;
- real-Vault mutation;
- P5-E near-real-time qualification;
- P6.

The real P5-D4 control root was not created:
`C:\Users\Boulevart\AppData\Local\ATDS-OBSIDIAN-PROJECTION\P5D4` = ABSENT.

## Source authority

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Branch: `feat/obsidian-projection-p5d4-bounded-observer-loop-runtime-v0.1`
- Qualified P5-D4 contract HEAD: `b12643109a62f740baa47057c86520304c3ef170`
- Qualified contract blob: `6980de1eb55e49c0c2bd2f91620aeb75640753b6`
- Historical contract breaker blob: `7e572e90cc331a316b58bc3e69970bed9ac40507`
- Historical contract qualification report blob: `2628af543245cae45310334c6bf1d3966d3ba71f`
## Runtime preregistration

Runtime preregistration commit:

`47a99af63a6d30623b04abe65cac736adc451a62`

Artifact:

`tools/obsidian_projection/p5d4_bounded_observer_loop_runtime_preregistration_v0_1.json`

Blob:

`7645a96ae8b9b827a78c3313127219023dd2c7ac`

The preregistration froze before implementation:
- one runtime module;
- injected observation/evaluation adapters;
- P5-D2 `one_shot_tick()` as sole semantic-state mutation authority;
- no P5-D3 projection reimplementation;
- no P5-D3F/P5-D3G automatic promotion surface;
- explicit finite budgets;
- append-only event-before-checkpoint persistence;
- exclusive ownership;
- restart/reconciliation;
- synthetic-temp qualification only.

## RED test-first

RED commit:

`8e1eb0d15e4fa812b9e18ed70c9017a1ea086e36`

RED test blob:

`5bcc563487ca8c64a1afde9f022504b2b618af7b`

Initial RED result before runtime existed:

```
Ran 17 tests
1 PASS
16 FAIL
```

The single PASS verified the preregistration blob. All sixteen failures were caused by the intentionally absent runtime module.

No runtime file existed during this RED.
## Minimal implementation

Initial implementation commit:

`05e06bdede66f482997ce03e7c060e04fc877a1f`

Initial implementation blob:

`07d1a14c66470588a159640b97e52fa6626fcb2e`

After implementation, the frozen RED suite passed:

```
17 / 17 PASS
```

The runtime implements:
- canonical digest-bound loop plans;
- finite cycle/observation/evaluation/failure/queue budgets;
- exclusive ownership record with no auto-steal;
- canonical append-only hash-chained JSONL event log;
- event durable write before checkpoint;
- atomic checkpoint replacement and read-after-write verification;
- queue-capacity preflight;
- deterministic P5-D2 replay for one-record-ahead crash recovery;
- existing-CURRENT evidence reconstruction through P5-D2 events;
- injected observation adapter;
- injected finite-evaluation outcome adapter;
- bounded loop orchestration;
- explicit `PROMOTION_AUTHORITY_REQUIRED` terminal boundary.

The runtime contains no finite projection/evaluation business logic from P5-D3 and contains no automatic publication invocation.

## Adversarial expansion

Adversarial breaker commit:

`df685785cdc84165c677a0953019e9908685ccc7`

Adversarial test blob:

`8da2c73d76a8be6dc11212a57b2bd1f83b03e33d`

After correcting one breaker-harness false positive without changing runtime behavior, the adversarial RED result was:

```
Ran 15 tests
13 PASS
1 FAIL
1 ERROR
```

Two real defects were isolated:
1. a forged but rehashed `record_origin` was accepted;
2. an unexpected adapter exception escaped instead of becoming a persisted fail-closed terminal result.
## Adversarial closure

Runtime stabilization commit:

`a7dcd747f5d12496fe751a4c66e6e70e682a9066`

Final runtime blob:

`b41c6b5172dd8ffe01d49717f5d796e4b5ad8f90`

Mechanical corrections only:
- event-log load now accepts only `LIVE_BOUNDED_LOOP` and `EVIDENCE_RECONSTRUCTION`;
- queue-capacity failure maps to `QUEUE_CAPACITY_REQUIRES_ADJUDICATION`;
- reconciliation failures map to `RECONCILIATION_REQUIRED`;
- unexpected exceptions map to persisted `FATAL_INCONSISTENCY`;
- ownership is released through the same finalizer.

Post-closure result:

```
runtime RED + adversarial = 32 / 32 PASS
```

Adversarial coverage includes:
- unterminated/tampered event log;
- forged event origin;
- checkpoint ahead / log more than one record ahead;
- non-replayable one-record-ahead state;
- queue-order checkpoint tamper;
- physical CURRENT/checkpoint mismatch;
- UNKNOWN ancestry;
- remote observation budget;
- consecutive-failure budget;
- zero evaluation budget;
- unexpected adapter exception;
- second-runner write exclusion;
- stale-lock no-auto-steal semantics;
- restart from EVALUATING without repeated evaluation;
- protected-root nonmutation;
- absence of direct observer semantic-state assignment;
- absence of external process/promotion surfaces.
## Contract-only phase-transition test adaptation

The qualified contract-era breaker originally asserted that no `p5d4*.py` runtime existed in the current worktree.

Once the separately authorized runtime frontier opened, that literal present-time assertion became intentionally false even though the historical contract-only qualification remained valid.

A narrow mechanical adaptation changed that breaker to verify the exact historical fact at the contract qualification HEAD:

`b12643109a62f740baa47057c86520304c3ef170`

Adaptation commit:

`483566b4050643ee5a0a6a882b250eecca79f792`

Current adapted contract-test blob:

`b6eab71d8b52972faeed8cf2edfc5908152c3d89`

The historical qualified breaker blob remains preserved in Git history and remains the blob cited by the P5-D4 contract qualification.

Focused P5-D4 result after this adaptation:

```
61 / 61 PASS
```

## Targeted predecessor regression

Covered:
- P5-D4 contract;
- P5-D4 runtime RED;
- P5-D4 runtime adversarial suite;
- P5-D1 observer core contract;
- P5-D2 one-shot observer contract;
- P5-D2 observer implementation;
- P5-D3D finite evaluator contract/runtime;
- P5-D3E verifier/adversarial surface;
- P5-D3F promotion handoff contract/runtime;
- P5-D3G live-publication contract/runtime.

Final targeted result:

```
Ran 286 tests in 108.146s
OK
```
## Final full Obsidian re-break

Full re-break executed exactly once after runtime stabilization and the phase-transition test adaptation.

HEAD / remote HEAD:

`483566b4050643ee5a0a6a882b250eecca79f792`

Result:

```
Ran 1402 tests in 240.280s
OK

FULL_SECONDS = 241.09
FULL_EXIT = 0
FULL_OBSIDIAN_REBREAK = PASS
```

The pre-run and post-run worktree were clean.

The existing historical line-ending warning for `sample.txt` occurred, but no worktree mutation remained after the suite.

## Authority and safety adjudication

The candidate proves bounded repeated orchestration in synthetic isolated control roots.

It does not create promotion authority.

```
P5D2_SEMANTIC_STATE_AUTHORITY        = PRESERVED
P5D3_BUSINESS_LOGIC_REIMPLEMENTED    = FALSE
BOUNDED_LOOP_BUDGETS                 = PASS
CHECKPOINT_EVENT_PROTOCOL            = PASS
HASH_CHAINED_APPEND_ONLY_EVENT_LOG   = PASS
QUEUE_CAPACITY_ENFORCEMENT           = PASS
SINGLE_INSTANCE_OWNERSHIP            = PASS
RESTART_RECONCILIATION               = PASS
CRASH_WINDOW_ONE_RECORD_REPLAY       = PASS
EXISTING_CURRENT_EVIDENCE_REBUILD    = PASS
PROMOTION_AUTHORITY_REQUIRED_STOP    = PASS

AUTOMATIC_P5D3F                      = FALSE
AUTOMATIC_P5D3G                      = FALSE
IMPLICIT_STAGE_A                     = FALSE
IMPLICIT_STAGE_B                     = FALSE
REAL_VAULT_MUTATION                  = FALSE
REAL_REPEATED_POLLING                = FALSE
DAEMON                               = FALSE
P5E_AUTHORITY                        = FALSE
P6_AUTHORITY                         = FALSE
```
## Qualification verdict

```
P5D4_RUNTIME_PREREGISTRATION       = PASS
P5D4_RED_TEST_FIRST                = PASS
P5D4_MINIMAL_IMPLEMENTATION        = PASS
P5D4_ADVERSARIAL_EXPANSION         = PASS
P5D4_ADVERSARIAL_CLOSURE           = PASS
P5D4_SYNTHETIC_MULTI_CYCLE         = PASS
P5D4_CRASH_RECONCILIATION          = PASS
P5D4_SINGLE_INSTANCE               = PASS
P5D4_TARGETED_REGRESSION           = 286 / 286 PASS
FULL_OBSIDIAN_REBREAK              = 1402 / 1402 PASS

P5-D4 RUNTIME CANDIDATE V0.1
= QUALIFIED_SYNTHETICALLY
```

This verdict does not claim a real bounded production loop has been qualified.

## Mandatory stop and next frontier

The runtime candidate is qualified, but all P5-D4 runtime execution so far was synthetic and isolated.

Therefore the next governed frontier is:

`P5-D4 — REAL BOUNDED LOOP QUALIFICATION`

not P5-E yet.

That frontier should prove the qualified runtime against the real read-only source/current environment with an explicitly finite invocation and without automatic promotion authority.

A separate human authorization is required before any real P5-D4 bounded-loop execution.

P5-E remains closed until the real bounded loop is separately qualified.
