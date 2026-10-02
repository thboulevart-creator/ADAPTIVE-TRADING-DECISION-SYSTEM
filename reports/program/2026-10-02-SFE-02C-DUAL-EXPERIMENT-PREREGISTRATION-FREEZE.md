# SFE-02C — DUAL EXPERIMENT PREREGISTRATION — FREEZE RECORD

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`

## 1. Human-authorized boundary

The human explicitly opened the next frontier:

```text
BREAKOUT EXPERIMENT CONTRACT
+
MEAN REVERSION EXPERIMENT CONTRACT
        ↓
BOTH FROZEN FIRST
        ↓
ONLY AFTER THAT
PERFORMANCE OBSERVATION MAY BE CONSIDERED
```

This record closes that preregistration boundary only.

It does not authorize performance observation.

## 2. Persisted state before freeze record

```text
HEAD =
1ec5fd1cc5145408249585c1337ecf3a3e872238

TREE =
0c88872b8b118b352deb3bd1390d5a7baf70e8dc
```

## 3. Frozen shared experiment surface

```text
PATH =
GOVERNANCE/SFE-02C-DUAL-EXPERIMENT-SHARED-SURFACE-V0.1.json

BLOB =
0fcf3ce86033b5d8b75caa0a1f18cc6b64fd54a2
```

This shared surface freezes:

- exact historical H1 evidence identity;
- E1 exposure status;
- data construction and continuity;
- directional-event semantics;
- t+1 admissibility;
- primary estimand;
- evidence sufficiency;
- dependence-aware inference;
- multiplicity;
- diagnostic reporting;
- paired-execution firewall.

## 4. Frozen BREAKOUT_V1 experiment contract

```text
PATH =
GOVERNANCE/SFE-02C-A-BREAKOUT-V1-EXPERIMENT-CONTRACT-V0.1.json

BLOB =
55db053489a3c00b015c424297e316e9e5461e38

EXPERIMENT_ID =
BREAKOUT_V1_SOURCE_B_USTECH_H1_E1_EXPOSED_EXPLORATORY_V0_1
```

Bound runtime:

```text
tools/sfe_02a_breakout_v1.py

BLOB =
60f32b2d054390c2b5dbb975b015d7e09a5a1a96
```

## 5. Frozen MEAN_REVERSION_V1 experiment contract

```text
PATH =
GOVERNANCE/SFE-02C-B-MEAN-REVERSION-V1-EXPERIMENT-CONTRACT-V0.1.json

BLOB =
672b059b17413c9058cea749992e0ee08e11f2b4

EXPERIMENT_ID =
MEAN_REVERSION_V1_SOURCE_B_USTECH_H1_E1_EXPOSED_EXPLORATORY_V0_1
```

Bound runtime:

```text
tools/sfe_02b_mean_reversion_v1.py

BLOB =
273e184093e4cc98f0eb6569cd6f1007366cce40
```

## 6. Exact shared evidence identity

Both experiments are frozen to:

```text
INSTRUMENT =
USTECH / Nasdaq 100 Index CFD
as represented by SOURCE_B_USTECH_PRICE_CORE_V0_1

H1 DATASET =
USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1

H1 CANONICAL STREAM SHA-256 =
15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f

ACCEPTED H1 ROWS =
27677

CONTINUITY BLOCKS =
1436

FIRST ADMISSIBLE H1 =
2021-05-25T01:00:00Z

LAST ADMISSIBLE H1 =
2026-05-24T22:00:00Z

PRICE FIELD =
mid_close
```

The entire surface is classified:

```text
EXPERIMENT_CLASS =
EXPLORATORY

EXPOSURE_STATUS =
E1_EXPOSED

PRISTINE_CONFIRMATORY =
FALSE

TD03B_CONSUMED =
FALSE

RESERVED_CONFIRMATORY_EVIDENCE_CONSUMED =
FALSE
```

No result from this surface may later be relabeled pristine confirmation.

## 7. Frozen primary estimand

For each strategy family:

```text
DIRECTIONAL_EVENT =
every eligible LONG or SHORT H1 bar

R_(t,t+1) =
C_(t+1) / C_t - 1

Y_t =
direction_t × R_(t,t+1)

PRIMARY_ESTIMAND =
mean(Y_t)
over ALL VALID DIRECTIONAL EVENTS

PRIMARY_REFERENCE =
RAW_ZERO
```

No execution or PnL meaning is attached to this behavioral outcome.

## 8. Frozen evidence-sufficiency gates

Each family must independently satisfy all of:

```text
VALID DIRECTIONAL EVENTS >= 100

VALID LONG EVENTS >= 20

VALID SHORT EVENTS >= 20

EVENT-BEARING FIXED 20-H1 INFERENCE BLOCKS >= 30
```

Raw event count alone is not sufficient.

Failure of any gate yields:

```text
NOT_INTERPRETABLE /
INSUFFICIENT_EVIDENCE
```

## 9. Frozen dependence-aware inference

Eligible signal bars are assigned to fixed non-overlapping 20-H1 inference blocks inside each continuity block:

```text
INFERENCE_BLOCK_INDEX =
floor((continuity_ordinal - 20) / 20)
```

Inference uses event-bearing blocks as cluster units.

For each family:

```text
theta =
sum(Y) / N

cluster jackknife =
leave one event-bearing 20-H1 block out at a time

SE =
sqrt(
  ((K-1)/K)
  ×
  sum((theta_minus_b - theta_jack_mean)^2)
)
```

Degenerate or nonfinite inference yields `NOT_INTERPRETABLE`.

## 10. Frozen multiplicity and decision rule

Two decision-bearing family experiments are preregistered together.

Multiplicity is fixed before results:

```text
METHOD =
BONFERRONI

FAMILYWISE_ALPHA =
0.05

PER-FAMILY TWO-SIDED ALPHA =
0.025

NORMAL CRITICAL VALUE =
2.241402727604947
```

Per-family interval:

```text
theta ± 2.241402727604947 × SE
```

Decision:

```text
LOWER BOUND > 0
→ SUPPORTED_ON_THIS_EXPLORATORY_E1_EXPOSED_SURFACE

UPPER BOUND <= 0
→ REFUTED_ON_THIS_EXPLORATORY_E1_EXPOSED_SURFACE

OTHERWISE
→ NOT_INTERPRETABLE /
  NON_DECISIVE_STATISTICAL_EVIDENCE
```

These statuses remain scoped to this exact exposed exploratory surface.

## 11. Frozen secondary diagnostics

The following are mandatory but non-decision-bearing unless separately preregistered under a new version:

- `n_total`;
- `n_LONG`;
- `n_SHORT`;
- `mean_Y_combined`;
- `mean_Y_LONG`;
- `mean_Y_SHORT`;
- unconditional H1 drift on all valid consecutive same-block H1 transitions;
- t+1 exclusion count/fraction and calendar-month distribution;
- exclusion reason categories;
- included-vs-excluded median prior observable absolute H1 return;
- Breakout/Mean-Reversion co-firing counts;
- exclusive-other-NEUTRAL vs exclusive-other-UNDEFINED counts.

No subgroup may silently replace the primary `ALL_DIRECTIONAL_EVENTS` decision surface.

## 12. Paired contamination firewall

The following state is now established:

```text
BREAKOUT CONTRACT =
FROZEN

MEAN REVERSION CONTRACT =
FROZEN

SHARED SURFACE =
FROZEN

PERFORMANCE OBSERVED =
NO
```

Any future authorized result run must satisfy:

```text
ONE GOVERNED DUAL RUN

COMPUTE BOTH FAMILY RESULT ENVELOPES
BEFORE HUMAN OR MODEL REVIEW
OF EITHER FAMILY RESULT

NO INTERMEDIATE INSPECTION

NO CONTRACT MUTATION
AFTER FIRST RESULT COMPUTATION
```

This prevents the result of one family from modifying the experiment design of the other.

## 13. Protected evidence firewall

This preregistration does not consume:

```text
TD03B PROSPECTIVE EVIDENCE
C01 RESERVED CONFIRMATORY EVIDENCE
OTHER RESERVED FUTURE CONFIRMATORY WINDOWS
```

The selected historical H1 surface is already E1-exposed and is used only as an exploratory strategy-family behavioral experiment.

## 14. Current status

```text
SFE_02C_SHARED_SURFACE =
FROZEN

SFE_02C_A_BREAKOUT_EXPERIMENT =
FROZEN

SFE_02C_B_MEAN_REVERSION_EXPERIMENT =
FROZEN

DUAL_PREREGISTRATION =
COMPLETE

BREAKOUT_PERFORMANCE =
NOT_OBSERVED

MEAN_REVERSION_PERFORMANCE =
NOT_OBSERVED

BEHAVIORAL_Y =
NOT_CALCULATED

REAL_RESULT_RUN =
NOT_AUTHORIZED

PNL =
NOT_AUTHORIZED

BACKTEST =
NOT_AUTHORIZED

EXECUTION =
NOT_AUTHORIZED

OPTIMIZATION =
NOT_AUTHORIZED

RANKING =
NOT_AUTHORIZED
```

## 15. Next candidate boundary

The next possible boundary is no longer experiment design.

It is a separately authorized, fail-closed **dual result-run qualification** that would:

1. revalidate all three preregistration blobs;
2. revalidate the exact H1 canonical stream identity;
3. run both already-qualified strategy kernels;
4. calculate both behavioral result envelopes in one governed operation;
5. persist both envelopes before any human/model inspection;
6. perform the preregistered inference and diagnostics;
7. STOP before any PnL, execution, optimization, ranking or routing.

That boundary is **not authorized by this freeze record**.

## 16. STOP

```text
SFE-02C =
DUAL_PREREGISTRATION_FROZEN

PERFORMANCE_OBSERVATION =
NOT_AUTHORIZED

NEXT =
SEPARATE HUMAN AUTHORIZATION
FOR DUAL RESULT-RUN QUALIFICATION

STOP =
TRUE
```
