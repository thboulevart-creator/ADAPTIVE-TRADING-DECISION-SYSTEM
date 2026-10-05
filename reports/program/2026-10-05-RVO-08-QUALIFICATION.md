# RVO-08 — FIRST REAL CC02 SINGLE AP1 EXECUTION V0.1 — CLOSURE

## Final status

```text
RVO-08 =
BLOCKED_AFTER_SINGLE_AP1_EXECUTION_FAILURE

SINGLE_AUTHORIZED_AP1_INVOCATION =
CONSUMED

INVOCATION_COUNT =
1

AUTOMATIC_RETRY =
FALSE

RETRY_AUTHORIZED =
FALSE
```

The single authorized AP1 invocation returned exit code 1. It did not time out and did not mint an AP1 output file.

This is an execution failure. It is not a scientific finding, not a market finding, and not evidence for or against a trading strategy.

## Canonical execution parent

```text
HEAD =
b7dee2c03eb533eb789c593986dc346b34ce8624

TREE =
8af27f0b27e907c6e3753c8697243db16fa8c796
```

The execution was bound to this exact detached, clean workspace state.

## Drift

The authorization reference was:

```text
e3cd567b7233e90f5f5b2feb7c424db7e213bfa4
ccafb924e157e717cbc2ff51867934ccf965d864
```

Initial preflight was identical.

During controller maturation, concurrent drift appeared after `72e9b70...` and before `b7dee2c...`:

```text
02e734aec02bbd54c5d53d8dfdbc0695a7e67cc2
```

The delta contained only three additive BEPD-04A response-semantics artifacts and was explicitly classified `NON_MATERIAL` for RVO-08. No RVO-07/P1/DATA-02/AP1/SMF/G05 owner surface changed.

Drift reconciliation blob:

```text
e90da864375a7b51f73aba3f0a42d953282292d3
```

No force update was used.

## Fresh RVO-07 / G05 revalidation at execution HEAD

Fresh G05 receipt:

```text
SHA256 =
409d93d1c719ba45c083a5161a0aab7865dc597b88f4a95e4b533c99927360d4

STATUS =
G05_01_WORKSPACE_DRY_READY
```

Fresh RVO-07 receipt:

```text
SHA256 =
d4023c9eff4362b4f8c0835169f96878cc82e51f8dac6128c0852f1fea196281

VERDICT =
GO

READINESS =
PRE_EXECUTION_READINESS_GO
```

All G01-G05 were freshly requalified closed before the RVO-08 session.

## Exact P1 execution identities

```text
EXPERIMENT_SPEC_ID =
EXS-4c70131ddca1dd4b2458d2d647655b04

EXECUTION_BINDING_ID =
EEB-0460cfae3b0275284e78701580230dfa

EXPERIMENT_EXECUTION_INPUT_ID =
QEI-c43f0ebdca64813bf205deb9f0e7114b

P1_DATA_EVIDENCE_BINDING_ID =
P1DE-fcad5b5935300a666e634315c29988de

P1_DATA_EVIDENCE_BINDING_DIGEST =
fcad5b5935300a666e634315c29988de809324a8ce7f5adc366da004372cac84

INVOCATION_PROFILE_ID =
P1_12C_AP1_CLAIM_SCOPED_V1

INVOCATION_PROFILE_DIGEST =
3a8689dcfa79515fae9f38b7e4903722ebdcd601ca16e7d84ef9139eb62b4de4

REAL_PRODUCER_EXECUTION_PLAN_ID =
QRPP-c4ae8febe29061317aa2c44525db4650

REAL_PRODUCER_EXECUTION_PLAN_DIGEST =
c4ae8febe29061317aa2c44525db4650706ee2e45ab3fff5a178e0a4e4fbd33e

COMMAND_DIGEST =
63191c1b99c9cca2b3fc41a8d25789f13e1df0c9404fd4767ebfa24e97f5e9ec
```

Producer identity remained:

```text
tools/ap1_intraday_spread_census.py
blob = 9f613063fb8a190a1ff6f2f8b12c97c4ed97712a
```

## Runtime lock

```text
RUNTIME_LOCK_ID =
RPRL-5b77e0c094812f3e7e9d25efdb87bd3d

RUNTIME_LOCK_DIGEST =
5b77e0c094812f3e7e9d25efdb87bd3da92748bc6f8a436ffe52cefe6d38f6c4

TIMEOUT_SECONDS =
3600
```

The runtime lock remained the exact G05/P1-21 qualified lock.

## Pre-result freeze

The byte-exact local freeze existed before invocation:

```text
SHA256 =
be1447388649be310e524918b7970f5b96e3776d10df7db85f5f47973d0ab7b6

FREEZE_DIGEST =
84b9286dbee74ba319d398dc54bbd5d40c237c813ac22a83de79b0fa80f7db63
```

A persistence defect was discovered after the invocation: the pre-result Git blob recorded as `cdf60184...` contains the tool-rendered wrapper, not the raw freeze bytes. Therefore:

```text
cdf60184396df2c6432321807c036f39fa846aa1
!=
BYTE-EXACT FREEZE BLOB
```

It must not be used as the canonical freeze identity.

The exact freeze bytes were subsequently canonicalized as:

```text
18da0e5df6ea310292f2dcb43b413d553afd233a
```

Because this exact Git blob was created post-result, RVO-08 does not claim qualified canonical pre-result Git-byte persistence. The local freeze SHA-256 was nevertheless fixed and recorded before the invocation.

## One-shot invocation evidence

Exact one-shot ledger:

```text
SHA256 =
714311480be2c1f5f153336419075f81efba0c1747857dd1c29ddd2228f2c4a7

Git blob =
11d47d1dfc2fbfe6a2746f74f245812398494e8e

invocation_count =
1

state =
STARTED

started_at =
2026-10-05T19:49:16.784208Z
```

The ledger was created exclusively before the child process and uses an exclusive-create boundary. Its existence blocks any second invocation under this RVO-08 authorization.

The ledger remains `STARTED` because this controller version only transitions it to `COMPLETED` on successful AP1 completion. It was not rewritten after failure.

## Observed execution

Execution receipt:

```text
Git blob =
937e33846126246596e4d8ecf8327706d59202e5

SHA256 =
39179dbd865639933c0eca8fb0d48e20a88f9a2149f743bddf858f607e909a79

STATUS =
BLOCKED_AP1_EXECUTION_FAILED

EXIT_CODE =
1

TIMEOUT_OBSERVED =
FALSE

TIMEOUT_SECONDS =
3600

DURATION_SECONDS =
0.13509040046483278

STARTED_AT =
2026-10-05T19:49:16.784208Z

ENDED_AT =
2026-10-05T19:49:16.921794Z

STDOUT_SHA256 =
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

STDERR_SHA256 =
3e7806beb5bb6c78a8d5128c9eb871223e14fc1b42e03e64f778ad9070aaf567
```

The child stderr bytes were not persisted, only their SHA-256. Therefore the exact root cause of exit code 1 is not recoverable from this receipt and must not be guessed.

## AP1 output

Intended transport:

```text
C:\Users\Boulevart\ATDS-CONTROL\RVO-08\AP1-FIRST-REAL-CC02-b7dee2c0.json
```

Observed:

```text
OUTPUT_EXISTS = FALSE
OUTPUT_BYTES = NOT_MINTED
OUTPUT_SHA256 = NOT_MINTED
OUTPUT_SCHEMA = NOT_MINTED
OUTPUT_STATUS = NOT_MINTED
```

No AP1 empirical result was exposed.

## Regressions observed at the execution HEAD

Canonical GitHub Actions run:

```text
RUN =
37365326846

JOB =
111948950541

CONCLUSION =
SUCCESS
```

Observed counts:

```text
RVO-08 controller = 5 PASS
P1-21 breakers = 29 PASS
P1-21 positive = 18 PASS
RVO-07 breakers = 35 PASS
RVO-07 positive = 20 PASS
G05 breakers = 30 PASS
G05 positive = 19 PASS
SMF-AP1-M03 breakers = 28 PASS
SMF-AP1-M03 positive = 25 PASS
DATA-02 breakers = 32 PASS
controller-CI real-AP1 guard = PASS
clean worktree = PASS
```

A local Windows P1-21 positive replay also encountered the already-known Windows Store alias hashing fixture defect. It is not converted into a local PASS and does not override the canonical CI evidence above.

## Authority boundary

```text
M03_EXECUTED = FALSE
SCIENTIFIC_FINDING = NONE
STRATEGY_VALIDATED = FALSE
BACKTEST = NONE
NEW_OOS = NONE
PAPER = NONE
BROKER/LIVE = NONE
CAPITAL = NONE

SCIENTIFIC_AUTHORITY = FALSE
OPERATIONAL_AUTHORITY = FALSE
TRADING_AUTHORITY = FALSE
CAPITAL_AUTHORITY = FALSE
```

## STOP

The one-shot budget is consumed.

```text
AP1 RETRY =
NOT AUTHORIZED

SECOND AP1 INVOCATION =
FORBIDDEN UNDER RVO-08

M03 REAL EXECUTION =
NOT AUTHORIZED
```

The next logical boundary is failure forensics only. No retry may occur without a new, separate human authorization after that diagnosis.
