# P5-E V0.1 — CONTRACT + SYNTHETIC TIMING MODEL — HUMAN ADJUDICATION

Date: 2026-10-02

## Human decision

The human authority adopts:

`P5-E V0.1 — CONTRACT + SYNTHETIC TIMING MODEL`

as:

`P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL = QUALIFIED_AND_HUMAN_ADOPTED`

This adoption follows:

- external B1→B5 closure;
- BB1 `NORMATIVE GUARD COVERAGE` closure;
- BB1 external re-review `PASS_WITH_NON_BLOCKING_NOTES`;
- `FINAL PRE-ADOPTION EVIDENCE HYGIENE`;
- final external delta-review `PASS_WITH_NON_BLOCKING_NOTES`;
- final internal adjudication of D1→D4.
## Binding pre-adoption identity

This adoption is bound to the exact pre-adoption repository state:

```text
PRE-ADOPTION HEAD
= 3aca84cea6edf17e337015c195c91a4195bc6dfc

CONTRACT
= 43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9

SYNTHETIC MODEL
= c0f16baa151c1466e30ba5778f1fca8184cd4aac

EVIDENCE MATRIX
= 454889848803bdaeed70a6fdfd80033ff22b8e72
```

Branch at adoption:

`feat/obsidian-projection-p5e-v0.1-final-pre-adoption-evidence-hygiene`

Pre-adoption local HEAD and remote HEAD were equal.

Pre-adoption worktree was clean.
## Adopted scope

The human adoption covers only:

- the P5-E V0.1 contract;
- the P5-E synthetic timing model;
- the evidence and guard structure used to qualify that contract/model candidate;
- the current bounded claim scope established by the reviewed candidate.

This adoption does not convert synthetic qualification into real execution qualification.

## Explicitly not qualified or authorized

This adoption does not qualify:

- real P5-E behavior;
- a real 60-second SLA;
- continuous synchronization;
- detection of every transient remote tip;
- a real observation adapter;
- ancestry-classifier correctness.

This adoption does not authorize:

- automatic evaluation;
- Stage A;
- Stage B;
- promotion;
- publication;
- Vault mutation;
- `CURRENT.md` mutation;
- daemon execution;
- Scheduled Task registration;
- Windows Service registration;
- startup registration;
- P6.
## Mandatory prerequisites before any REAL P5-E preregistration or execution

The following remain mandatory prerequisites:

- `N4` — closed-schema / added-key hardening;
- `N5` — exact real timing-boundary semantics;
- `NB2` — B→A / rollback / lag ambiguity;
- `NB3` — real tip-visibility adapter semantics;
- `NB5` — ancestry-classifier correctness;
- `NB9` — controlled-release real experiment protocol.

These prerequisites are not waived by this adoption.

They remain outside the adopted synthetic candidate and must be explicitly resolved or preregistered before REAL P5-E can be opened.
## Retained non-blocking notes

### D1 — N1 fixture discrimination

The current N1 test correctly verifies:

`READ_COMPLETION_PRECEDES_ATTEMPT_START`

and kills removal of that guard through its exact failure-code assertion.

A future hardening may use a more discriminating fixture such as a valid prior slot followed by an impossible completion-before-start record.

This is a test-quality note only.

### D2 — external packet completeness

Future external-review packets should embed every source required for independent reproduction even when a source is unchanged from a previous packet.

This is a packaging / provenance note only.

### D3 — current semantic sweep count

The current contract includes the N1 field and therefore has:

```text
CURRENT SEMANTIC SWEEP
= 162 leaves
= 13 survivors
= all 13 non-normative
= 0 normative survivors
```

The earlier `161 / 13 / 0 normative` evidence remains historical evidence for the prior BB1 candidate state.

The full qualification surface with object binding produced zero survivors because object identity drift is rejected.

These two measurements answer different questions and must not be conflated.
### D4 — reused evidence provenance granularity

`REUSED_QUALIFIED_P5D2_P5D4` is interpreted at the level of the reused behavioral method, not as a claim that the entire current test file is byte-identical to its historical qualified file.

Current evidence-matrix count:

```text
REUSED_QUALIFIED_P5D2_P5D4
= 11 entries total

7 entries → P5-D2 test_observer_tick.py methods
4 entries → P5-D4 bounded-loop runtime test methods
```

The two newly introduced pending-non-active D2-file mappings remain:

`DIRECT_P5E`

This note does not change the qualification verdict.
## Review and qualification state at adoption

The latest external delta-review returned:

`PASS_WITH_NON_BLOCKING_NOTES`

with:

`BLOCKING_FINDINGS = NONE`

The internally adjudicated result before adoption is:

```text
BB1_EXTERNAL_REVIEW
= PASS_WITH_NON_BLOCKING_NOTES

FINAL_HYGIENE_DELTA_REVIEW
= PASS_WITH_NON_BLOCKING_NOTES

TECHNICAL_CORRECTION_REQUIRED_BEFORE_ADOPTION
= NONE

P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL
= READY_FOR_HUMAN_NORMATIVE_ADJUDICATION
```

The human decision in this record closes that adjudication gate.
## Authority boundary after adoption

The adopted state is:

```text
P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL
= QUALIFIED_AND_HUMAN_ADOPTED

REAL_P5E
= CLOSED

REAL_HEAD_EVALUATION
= CLOSED

STAGE_A
= CLOSED

STAGE_B
= CLOSED

PROMOTION
= CLOSED

PUBLICATION
= CLOSED

VAULT_OR_CURRENT_MUTATION
= CLOSED

DAEMON_OR_SERVICE_REGISTRATION
= CLOSED

P6
= CLOSED
```

No authority is created beyond the exact synthetic-contract adoption recorded here.

## Persistence authority

The only operation authorized after this human statement is:

- persist this adjudication record;
- commit and push it;
- verify final repository consistency;
- STOP.

No contract, model, matrix, runtime, Vault, CURRENT, P5-D4 control state, or real P5-E execution surface may be mutated by this persistence step.
