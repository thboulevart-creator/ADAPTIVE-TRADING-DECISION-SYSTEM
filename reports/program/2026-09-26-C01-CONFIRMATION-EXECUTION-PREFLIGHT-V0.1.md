# C01 — CONFIRMATION EXECUTION PREFLIGHT V0.1

Date: 2026-09-26

Persistence base HEAD:

`6aef3b1304313c3446c08a3a37b51ea61733f41e`

## Purpose

C01 V0.2 is frozen and finally sealed.

This preflight freezes the execution boundary for later confirmation.

It does **not** execute the confirmation experiment.

Current state:

- confirmation data accessed: `false`
- primary score computed: `false`
- real confirmation execution authorized now: `false`
- next implementation data class after persisted-head re-break: `SYNTHETIC_ONLY`

## Frozen identities

Charter blob:

`ada0ebf41ecd7ab406d2656ac745ed7003d5b5c1`

Sealed model blob:

`68ee4795462c5dbd5747a7bfdef81716dc84227f`

Sealed model SHA-256:

`ae06a5177aa04195a959deb1ee63e114a16448a87cdb2f6a2a8b639a4cba199f`

Model digest:

`a8b8b823336fb0f7cd5a6b2bbae80d858603b6ff7567fe5e67e4b20c46726c7f`

Qualified producer blob:

`13bdc28585e9c6d34bc2217c750f1716fa3e7f9c`

Seal-candidate blob:

`3a6897a63ef2f07a26429342b45977767090651e`

Final-seal adjudication blob:

`d54ec7840a7bf4eecd94a72f753a02418ea8f543`

Any identity mismatch fails closed.

## Confirmation window

Fixed window:

`2026-05-25T00:00:00Z -> 2027-05-24T23:59:59Z`

Earliest primary evaluation:

`2027-05-25T00:00:00Z`

No partial-window primary scoring.

No early primary-score peek.

## Pristine/new-data status axes

The frozen Charter contains two existing clauses that are preserved rather
than collapsed.

Confirmatory-claim axis:

`if_pristine_status_cannot_be_proven -> NOT_CONFIRMATORY`

Primary scientific decision axis:

`new/pristine eligibility cannot be established -> NOT_INTERPRETABLE`

Therefore a future pristine/new-data eligibility failure must report both:

- confirmatory claim status: `NOT_CONFIRMATORY`
- primary scientific decision status: `NOT_INTERPRETABLE`

This is an execution/reporting distinction only.

It does not amend the frozen Charter, candidate, thresholds or decision
criteria.

## Causal execution

For each future eligible anchor `t`:

- context cutoff: `<=t`
- target start: `t+1`
- no gap crossing
- no segment crossing
- exact-minute continuity required
- same-segment continuity required
- confirmation anchors cannot enter fitting

## Frozen primary evaluation

Primary horizon:

`15m`

Secondary horizon:

`60m diagnostic only`

Target:

`25-class RV15 quintile x TICK15 quintile`

Joint states:

`9`

Sparse floor:

`500 valid primary targets per joint state`

Required comparisons:

`C01 vs B2+ABS_VOL`

`C01 vs B2+TICK`

Primary metrics:

`delta_log_loss`

`delta_brier`

No refit is authorized.

## Primary decision

CONFIRMED only if all nine state-count guards pass, both required baseline
comparisons have strictly positive delta log loss and delta Brier, and all
critical identity/provenance/causality/continuity controls pass.

REFUTED if either required comparison has delta log loss <=0 or delta Brier
<=0.

NOT_INTERPRETABLE on sparse, new/pristine eligibility, provenance,
identity, continuity or other critical control failure.

The 60m diagnostic cannot rescue the 15m primary result.

## Adjudication precedence

Validity gates have precedence over metric verdicts.

The future runner must adjudicate, in this order:

1. new/pristine eligibility;
2. critical identity, provenance, causality and continuity controls;
3. the nine-state sparse guard;
4. only if all preceding guards PASS, the frozen primary metrics.

Any critical validity/control failure forces the primary scientific
decision to:

`NOT_INTERPRETABLE`

regardless of whether the numerical deltas would otherwise satisfy the
CONFIRMED or REFUTED metric rule.

A pristine/new-data eligibility failure additionally forces the
confirmatory-claim axis to:

`NOT_CONFIRMATORY`

Therefore:

- sparse + negative metrics cannot become `REFUTED`;
- control failure + negative metrics cannot become `REFUTED`;
- pristine failure + negative metrics cannot become `REFUTED`;
- invalid tests cannot become `CONFIRMED`.

This is a fail-closed execution precedence rule. It does not alter any
frozen scientific threshold, baseline or metric criterion.

## Current authorization

Real confirmation execution:

**NOT AUTHORIZED**

Confirmation-window outcome access:

**NOT AUTHORIZED**

Primary scoring:

**NOT AUTHORIZED**

Runner development after persisted-head qualification:

**SYNTHETIC DATA ONLY**

## Machine-readable contract

`reports/program/evidence/2026-09-26-C01-CONFIRMATION-EXECUTION-CONTRACT-V0.1.json`

## Verdict

**PREFLIGHT PERSISTENCE CANDIDATE — NOT YET QUALIFIED.**

Next governed action:

**PERSISTED-HEAD RE-BREAK OF THIS PREFLIGHT AND CONTRACT.**

Only after PASS:

**TEST-FIRST CONFIRMATION RUNNER — SYNTHETIC DATA ONLY.**
