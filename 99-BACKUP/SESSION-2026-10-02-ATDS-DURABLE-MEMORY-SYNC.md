# SESSION BACKUP — 2026-10-02 — ATDS DURABLE MEMORY SYNC

## 0. Purpose

This snapshot repairs the durable recovery-memory layer only.

It records canonical repository state already present before this synchronization.

```text
SCIENTIFIC_STATE_CHANGE = NONE
RUNTIME_CHANGE = NONE
TEST_OR_BREAKER_CHANGE = NONE
STRATEGY_CHANGE = NONE
AUTHORITY_EXPANSION = NONE
```

## 1. Repository identity

```text
repository =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

branch =
integration/system-v1

PRE_SYNC_HEAD =
77fedcec4906d01a85a275b2d5c02e059e28d23f

PRE_SYNC_TREE =
e1e8317f0db2a47e152e3bcada1afafcf3337f3a

PRE_SYNC_HEAD_MESSAGE =
governance: adopt SFE-01 V0.2 with amendments
```

The post-sync commit/tree are intentionally not self-embedded in this file because their identities do not exist until the commit containing this file is created. They must be re-read from the governed branch when resuming.

## 2. Sources read for synchronization

Mandatory operating/recovery sources:

- `04-REFERENCE/AI-OPERATING-MEMORY.md`
  - blob `2b49a3b190c529f3e6135c60efb35f683a67f620`
- `04-REFERENCE/RECOVERY-CHECKPOINT.md`
  - pre-sync blob `c0ceccd80999493662145ed93ee1e2d7cdf846d7`
- `99-BACKUP/SESSION-2026-09-27-C01-CONFIRMATION-RUNNER-TEST-FIRST-RED.md`
  - blob `445d220c206dc0122daa2f8daa4ed91f92315f9c`

Canonical state sources:

- `reports/program/2026-09-29-E1-EXPERIMENTAL-MEMORY-FINAL.md`
  - blob `46450fea882f453335fcca7851df9764fc1ddf5c`
- `GOVERNANCE/ATDS-ARCHITECTURE-V2-HUMAN-ADJUDICATION-2026-10-01.md`
  - blob `1817969d1b2431be3476a7ab4b52b61e8f5da172`
- `reports/program/2026-10-01-P1-16-FINAL-PERSISTED-STATE-REBREAK-CLOSURE.md`
  - blob `8839e6df3ea0ccff69ec82fdfccb1527e5601faf`
- `reports/program/2026-10-01-END-OF-DAY-ATDS-SFE01-CHECKPOINT.md`
  - blob `61e701eecd1f6d612932b088d653201b0f577ca2`
- `GOVERNANCE/SFE-01-DUAL-STRATEGY-FAMILY-DEFINITION-CANDIDATE-V0.1.md`
  - blob `99d1698d303797b25ed7c140c5ad43f276cefe2c`
- `GOVERNANCE/SFE-01-DUAL-STRATEGY-FAMILY-DEFINITION-CANDIDATE-V0.2.md`
  - blob `027c42b38bf9c74415b21e98bcce19124f744995`
- `GOVERNANCE/SFE-01-V0.2-HUMAN-ADJUDICATION-2026-10-02.md`
  - blob `66aa556e4e161e49550451062273bc8d6422593c`

## 3. Path traversed

```text
E1 readiness / one-shot path
→ real exploratory E1 execution history
→ E1 experimental memory closure
→ Architecture V2 human adoption
→ P1.16 final persisted-state re-break closure
→ Strategy Family Expansion
→ SFE-01 V0.1
→ external adversarial break
→ SFE-01 V0.2 targeted closure
→ external V0.2 re-review
→ SFE-01 V0.2 human adoption with amendments
```

## 4. E1 final experimental state

```text
E1_EXPERIMENTAL_MEMORY =
ADOPTED_FOR_PERSISTENCE

E1_EVIDENCE_REVIEW =
CLOSED

E1_EXPLORATORY_EXPERIMENT =
CLOSED

STRATEGY_VALIDATED =
FALSE

NEW_BACKTEST =
NOT_AUTHORIZED

NEXT_EXPERIMENT =
NOT_AUTHORIZED
```

Important execution incidents preserved:

```text
E1-REAL-001
= ABORTED_PRE_OOS
= AUTHORITY_EXECUTOR_MISMATCH
= OOS_EXPOSED FALSE

E1-REAL-002
= ABORTED_AFTER_OOS_COMPUTATION
= E1_07_INVALID_ENVIRONMENT_DESCRIPTOR
= OOS_EXPOSED TRUE

E1-REAL-003
= PASS
= REPRODUCTION_OF_EXPOSED_OOS
= OOS_UNTOUCHED FALSE
= OOS_CLEAN FALSE
```

Durable lesson:

A failed technical run may irreversibly expose OOS if performance was computed before persistence failure. Exposure status cannot depend only on the presence of a persisted result artifact.

The E1 OOS must never regain untouched-OOS or independent-confirmation status.

## 5. Architecture V2

```text
ARCHITECTURE_V2 =
HUMAN_ADOPTED_WITH_AMENDMENTS

UNKNOWN_UNKNOWN_DISCOVERY_PROBLEM =
PRESERVED

UU-P1 =
FUTURE_BOUNDARY_NOT_AUTHORIZED

UU-P2 =
FUTURE_BOUNDARY_NOT_AUTHORIZED

UU-P3 =
FUTURE_BOUNDARY_NOT_AUTHORIZED
```

Architecture V2 preserves the functional backbone:

```text
DATA
→ CONTEXT
→ RESEARCH / EXPERIENCE
→ DECISION
→ ACTION
→ RESULT
→ TRACE
→ MEMORY
→ AUDIT / SELF-CHALLENGE
→ REVISION
→ NEW RESEARCH / EXPERIENCE
```

No automatic consequential authority is created.

## 6. P1.16

```text
P1_16_PROTECTED_CHAIN_REBREAK =
PASS

P1_16_EXACT_ENVIRONMENT_VERIFICATION =
PASS

P1_16_PERSISTED_STATE_REBREAK =
PASS

P1_16_FINAL =
PASS

P1_16 =
CLOSED
```

P1.16 remains an interpretation boundary only. It is not durable knowledge or operational/trading authority.

## 7. SFE-01 path and adopted state

The V0.1 external review produced adoption-blocking and hardening findings. V0.2 was produced as targeted documentary closure without changing the frozen V1 signal rules or parameters.

The current canonical adjudication is:

`GOVERNANCE/SFE-01-V0.2-HUMAN-ADJUDICATION-2026-10-02.md`

```text
SFE_01_V0_2 =
HUMAN_ADOPTED_WITH_AMENDMENTS

BREAKOUT_V1_DEFINITION =
HUMAN_ADOPTED
UNTESTED

MEAN_REVERSION_V1_DEFINITION =
HUMAN_ADOPTED
UNTESTED

V0_2_EXTERNAL_REVIEW =
PASS_WITH_NON_BLOCKING_FINDINGS

PERFORMANCE_OBSERVATION =
NOT_AUTHORIZED

SFE_02A =
NOT_AUTHORIZED

SFE_02B =
NOT_AUTHORIZED
```

Important adopted downstream protections include:

- exposure is semantic, not limited to identical dataset overlap;
- uncertain exposure defaults to EXPOSED;
- evidence reserved for other experiments cannot be silently consumed;
- preregistration must be persisted before performance observation;
- multiplicity must be handled where applicable;
- numerical semantics must be frozen before implementation.

## 8. Current prohibitions / separate debts

This synchronization does not authorize or reopen:

```text
A0
C01
E1_RERUN
MOMENTUM_V1_MODIFICATION
E1-TD / TD03B mutation or event consumption
P22-04
PHASE_23
UU-P1
UU-P2
UU-P3
RISK_ENGINE
PORTFOLIO_ENGINE
MT5
PAPER
BROKER
LIVE
CAPITAL
SFE-02A
SFE-02B
IMPLEMENTATION
BACKTEST
PERFORMANCE_OBSERVATION
OPTIMIZATION
```

P1.16 is closed and must not be reopened without new evidence.

## 9. Parallel non-normative discussion

A separate conversational study exists under the provisional label:

`ATDS — EXPERIENCE / LOSS / BACKTEST INTEGRITY GAP STUDY`

with conversational G0/G1 analysis.

Its status is:

```text
NON_NORMATIVE
NON_PERSISTED_AS_ATDS_PROGRAM_STATE
NO_AUTHORITY
NO_PHASE_CREATED
NO_RUNTIME_CHANGE
NO_SFE01_CHANGE
```

It must not be treated as the canonical ATDS frontier.

## 10. Durable-memory divergence repaired by this session

Before this synchronization:

- the central Recovery Checkpoint stopped at E1-08A-R2;
- the newest `99-BACKUP/SESSION-*` snapshot was dated 2026-09-27;
- later canonical artifacts were present elsewhere in the governed repository.

This session updates the Recovery Checkpoint and adds this dated snapshot only.

No other defect discovered during the synchronization is corrected opportunistically.

## 11. Exactly one next canonical frontier

From the adopted SFE-01 adjudication:

```text
NEXT_ACTION =
HUMAN CHOICE OF WHICH SEPARATE DOWNSTREAM CONTRACT TO AUTHORIZE
```

This is a choice boundary, not an authorization.

Therefore:

```text
SFE_02A = NOT_AUTHORIZED
SFE_02B = NOT_AUTHORIZED
NEW_IMPLEMENTATION = NOT_AUTHORIZED
BACKTEST = NOT_AUTHORIZED
PERFORMANCE_OBSERVATION = NOT_AUTHORIZED
STOP = TRUE
```

## 12. Recovery instruction

At the next substantive ATDS session:

1. read `04-REFERENCE/AI-OPERATING-MEMORY.md`;
2. read the current `04-REFERENCE/RECOVERY-CHECKPOINT.md`;
3. read this backup;
4. fresh-verify repository / branch / HEAD / TREE;
5. treat the current canonical frontier as the human choice of which separate downstream SFE contract, if any, to authorize;
6. do not infer authorization from the existence of SFE-01 definitions.

