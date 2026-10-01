# P5-E V0.1 — CONTRACT + SYNTHETIC QUALIFICATION

Date: 2026-10-01

## Verdict

```text
P5E_V0_1_PREREGISTRATION
= PASS

P5E_V0_1_RED_TEST_FIRST
= PASS

P5E_V0_1_MINIMAL_GREEN
= 17 / 17 PASS

P5E_V0_1_ADVERSARIAL_SURFACE
= 42 / 42 PASS

P5E_TARGETED_PREDECESSOR_REGRESSION
= 208 / 208 PASS

P5E_CROSS_CUTTING_REGRESSION
= 876 / 876 PASS

ADMISSIBLE_FULL_OBSIDIAN_REBREAK
= 1466 / 1466 PASS

P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL
= QUALIFIED_CANDIDATE

P5E_REAL_END_TO_END
= NOT_QUALIFIED

EXTERNAL_ADVERSARIAL_REVIEW
= PENDING

HUMAN_NORMATIVE_ADOPTION
= PENDING
```

This is a candidate qualification, not normative adoption and not a real end-to-end runtime qualification.

## 1. Scope actually qualified

This stage qualifies only:

- the P5-E temporal contract;
- exact inherited 30-second observation interval;
- exact inherited 60-second maximum detection latency;
- explicit detection-latency semantics;
- a pure synthetic timing model;
- timing-bound edge cases;
- authority boundaries;
- P5-D4 queue interaction under newer-head/burst pressure;
- fail-closed behavior;
- synthetic-to-real claim separation;
- compatibility with the existing Obsidian projection test surface.

This stage does not qualify:

- a real repeated polling implementation;
- a daemon or scheduler;
- a real 60-second operational SLA;
- automatic candidate evaluation;
- Stage A;
- Stage B;
- promotion;
- publication;
- continuous synchronization;
- P6.

## 2. Persisted artifact identities

Preregistration:

`6ef788532a1e945a42ca524af823710ae4f14ed6`

RED test:

`2305e0768182d82657c34a7cb53c502714a2ab81`

Contract:

`e5c3d7a9d451aba65e8062078c6c10d23e586f39`

Synthetic timing model:

`8662dd97a1c8a1af33d6593ae923384e96404b5a`

Adversarial test:

`6235c4b2addc16acd043832664440ec76f6dada2`

RED evidence:

`6de316c3c968c2b73122170bb2b86fbec6093951`

Minimal GREEN evidence:

`10bddb856462d16c6a214ccb3f31a2a8a554e748`

Adversarial qualification:

`7068dacade8c7263ab6a6f70dab360f1b53cc6f9`

P5-D4 lifecycle regression correction:

`1d015548ad69b790494da42d29c6167e65cbc624`

Targeted regression qualification:

`d3f089762f84368e4f071890af4b1be55d19b896`

Final admissible full re-break HEAD:

`f146201301b150efb35713e7aed3f0105821d41c`

## 3. Timing contract

Inherited P5-A parameters remain exactly:

```text
POLL_INTERVAL_SECONDS
= 30

DETECTION_LATENCY_SECONDS_MAX
= 60
```

Detection latency is defined as:

```text
FIRST_SUCCESSFUL_EXACT_REMOTE_HEAD_OBSERVATION_TIME
-
SOURCE_HEAD_AVAILABLE_TIME
```

The future real implementation must use monotonic elapsed time for bound enforcement.

The current synthetic model uses explicit injected seconds only.

It contains no real sleep, network observation, filesystem state access, process launch, real P5-D4 control-state access, or Vault access.

Synthetic cases qualified include:

- source change just after a poll and detection at the next 30-second slot;
- one transient read failure and detection by the 60-second bound;
- exact 60-second boundary;
- rejection of first detection after 60 seconds;
- rejection of no detection by the bound;
- rejection of invalid/non-30-second schedules;
- rejection of malformed observation inputs;
- incomplete-window state not laundered into PASS.

## 4. Queue-semantics conflict resolution

A real architectural conflict was identified.

Earlier P5-A design language allowed a later fast-forward HEAD to supersede/skippably contain older observed heads.

Current qualified executable P5-D4 V0.1 semantics instead require:

```text
FIFO
= REQUIRED

SILENT_DROP
= FORBIDDEN

SILENT_REORDER
= FORBIDDEN

LATEST_ONLY_REPLACEMENT
= FORBIDDEN

COALESCING
= NOT_AUTHORIZED

PENDING_HEAD_RETARGET
= FORBIDDEN

QUEUE_CAPACITY_EXHAUSTED
= QUEUE_CAPACITY_REQUIRES_ADJUDICATION
```

P5-E V0.1 resolves the conflict in favor of the current qualified executable P5-D4 semantics.

It does not invent a new P5-D2 coalescing event.

Any future supersession/coalescing policy requires its own governed semantic extension and qualification.

## 5. Read-only real context

At P5-E opening, the durable P5-D4 state contained:

```text
LIVE_PROJECTION_HEAD
= 59f1dc26973b0b50efefccf12b26784d1e41f546

QUEUED_UNEVALUATED_HEAD
= 1d4c2f3d657b36ecaa6ab25b967e46b3620190d1
```

The remote branch later observed read-only was:

`fcca78571a26955ae3fe462746ef49557e4e84e5`

and the queued HEAD was verified as an ancestor of that remote HEAD.

This context was evidence only.

Neither HEAD was evaluated, promoted, or published.

## 6. Adversarial qualification

The combined 42-test P5-E surface broke at minimum:

- 30 -> 31 second interval widening;
- 60 -> 61 second latency-bound widening;
- real-execution authority activation;
- evaluation authority activation;
- promotion authority activation;
- publication authority activation;
- real-polling authority activation;
- P6 authority activation;
- queue coalescing reintroduction;
- latest-only replacement;
- silent queue-capacity continuation;
- P5-A design intent overriding P5-D4 executable semantics;
- synthetic qualification relabelled as real P5-E qualification;
- removal of forbidden real-PASS claims;
- invalid observation schedules and malformed timing inputs.

Result:

`42 / 42 PASS`

No contract/model correction was required after adversarial expansion.

## 7. Regression qualification

Targeted predecessor surface:

`208 / 208 PASS`

A stale P5-D4 remediation-only test assumption was found: two tests still required the production root to remain absent forever.

That assumption contradicted the later authorized and human-adopted P5-D4 V0.2 lifecycle.

Only those phase-local assertions were mechanically changed to verify exact non-mutating canonical binding whether the root is absent or already legitimately present.

P5-D4 runtime remained unchanged.

Cross-cutting regression surface:

`876 / 876 PASS`

## 8. Worktree provenance anomaly and evidence handling

During broad qualification, the primary worktree P5-E contract/model were temporarily observed at non-authoritative worktree blobs and later returned exactly to their committed blobs.

Cause:

`UNKNOWN`

The transient content was not adopted and not persisted.

Because the primary worktree could not be treated as provenance-stable, its full-suite execution was not used as final proof.

A first isolated-clone wrapper attempt also failed at the harness layer because PowerShell `ErrorActionPreference=Stop` converted a non-failing native stderr warning into `NativeCommandError` before a test verdict.

The final admissible re-break therefore used a fresh disposable GitHub clone pinned to the exact remote HEAD and exact candidate blobs.

## 9. Final admissible full re-break

Exact remote HEAD:

`f146201301b150efb35713e7aed3f0105821d41c`

Pre-run clone status:

`CLEAN`

Result:

```text
Ran 1466 tests in 242.153s

OK

FULL_EXIT=0
```

After generated bytecode cleanup:

`CONTROL_POST_STATUS_COUNT = 0`

Control HEAD remained unchanged.

P5-D4 runtime blob remained:

`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

The complete real-state pre/post fingerprint was identical, including:

- live Vault content;
- `.obsidian`;
- current immutable generation;
- `CURRENT.md`;
- `CURRENT.tmp`;
- P5-D3G publication event evidence;
- P5-D4 event log;
- P5-D4 checkpoint;
- P5-D4 last-run state;
- P5-D4 ownership/temp state.

See:

`reports/program/2026-10-01-OBSIDIAN-P5E-V0.1-FULL-OBSIDIAN-REBREAK.md`

## 10. Authority boundary

Throughout this qualification stage:

```text
REAL_POLLING_LOOP
= NOT_AUTHORIZED

PENDING_HEAD_EVALUATION
= NOT_AUTHORIZED

EVALUATION
= NOT_AUTHORIZED

STAGE_A
= CLOSED

STAGE_B
= CLOSED

PROMOTION
= NOT_AUTHORIZED

PUBLICATION
= NOT_AUTHORIZED

REAL_VAULT_MUTATION
= NOT_AUTHORIZED

CURRENT_MUTATION
= NOT_AUTHORIZED

P6
= CLOSED
```

## 11. Claim boundary

The maximum technical claim supported before external review/human adoption is:

`P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL = QUALIFIED_CANDIDATE`

It is not permissible to infer:

- `P5E_REAL_END_TO_END_QUALIFIED`;
- `CONTINUOUS_SYNCHRONIZATION_QUALIFIED`;
- `REAL_60_SECOND_SLA_QUALIFIED`;
- automatic evaluation qualification;
- automatic promotion qualification;
- automatic publication qualification.

## 12. External adversarial review gate

Before normative human adoption, an external reviewer must receive the self-contained review packet and attack at minimum:

- timing semantics;
- exact 30/60 inheritance;
- whether the detection-latency definition is operationally meaningful;
- monotonic-clock requirements;
- transient network failure behavior;
- queue saturation;
- multiple HEAD arrivals;
- P5-A/P5-D4 conflict resolution;
- authority leakage;
- synthetic-to-real evidence laundering;
- hidden evaluation/promotion/publication paths;
- missing adversarial cases;
- whether the evidence justifies only the scoped candidate claim.

External review creates no authority by itself.

## 13. Mandatory stop

```text
P5E_CONTRACT_SYNTHETIC_CANDIDATE
= QUALIFIED

EXTERNAL_ADVERSARIAL_REVIEW
= REQUIRED_BEFORE_NORMATIVE_ADOPTION

REAL_P5E_EXECUTION
= CLOSED

HUMAN_NORMATIVE_ADOPTION
= PENDING

P6
= CLOSED

STOP
= TRUE
```
