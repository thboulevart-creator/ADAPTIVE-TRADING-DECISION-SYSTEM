# SFE-02D — DUAL RESULT-RUN — FINAL QUALIFICATION / CLOSURE

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`

## 0. Closure scope

This closes only the governed dual behavioral-result experiment defined by SFE-02C and executed under SFE-02D.

It does **not** authorize or establish:

```text
PNL
PROFITABILITY
ECONOMIC EDGE
EXECUTION
OPTIMIZATION
RANKING
ROUTER
REGIME FILTER
ROBUSTNESS
SOURCE-INDEPENDENT CONFIRMATION
PRODUCTION READINESS
```

The evidence surface remains:

```text
EXPLORATORY
E1_EXPOSED
NOT_PRISTINE_CONFIRMATORY
```

## 1. Canonical persisted state under closure

Immediately before this closure artifact:

```text
HEAD =
f002a2dc84f70d8aa768962f1fc551c43cab0ba3

TREE =
bca8bc7bd6b396d48d4a62c5e43eada70bcc56f6
```

SFE-02D run contract:

```text
GOVERNANCE/SFE-02D-DUAL-RESULT-RUN-CONTRACT-V0.1.json

BLOB =
4fd8b1adb2bb8e6d2ca11870bdee88fd232c757f
```

Frozen SFE-02C preregistration:

```text
SHARED SURFACE BLOB =
0fcf3ce86033b5d8b75caa0a1f18cc6b64fd54a2

BREAKOUT CONTRACT BLOB =
55db053489a3c00b015c424297e316e9e5461e38

MEAN REVERSION CONTRACT BLOB =
672b059b17413c9058cea749992e0ee08e11f2b4

DUAL FREEZE RECORD BLOB =
72d3bbb05d76a69c3d5f487500908d3a9c40bc3c
```

Qualified strategy runtimes:

```text
BREAKOUT_V1 RUNTIME BLOB =
60f32b2d054390c2b5dbb975b015d7e09a5a1a96

MEAN_REVERSION_V1 RUNTIME BLOB =
273e184093e4cc98f0eb6569cd6f1007366cce40
```

Final SFE-02D runner used for the real dual run:

```text
RUNNER V0.4 BLOB =
29a348648f76e7e234687388b119b2a729b51985
```

## 2. Preflight history

SFE-02D remained fail-closed through three pre-result defects:

### 2.1 Synthetic breaker V0.1 defects

The initial synthetic breaker produced:

```text
8 PASS
2 FAIL
```

Both failures were breaker-fixture/assertion defects, not runner defects:

- impossible directional events during a reset warmup;
- explicit `PNL` governance non-claim incorrectly treated as a PnL result field.

No real result had been calculated.

### 2.2 Git EOL provenance defect

Runner V0.1 attempted to identify protected Git blobs by hashing raw checkout bytes.

On Windows:

```text
core.autocrlf = true
```

made raw checkout bytes differ from canonical Git objects.

The real run blocked before reading the H1 dataset.

Correction:

```text
canonical Git object identity via HEAD:path
+
clean-worktree verification
```

No statistical logic changed.

### 2.3 E1 canonical-prefix reproduction defect

Runner V0.2 used an actual newline byte in its reimplementation of the E1 canonical-stream prefix.

The canonical E1 implementation uses literal backslash+n bytes:

```text
hex suffix =
5c6e
```

The run again blocked before strategy execution.

The persisted E1 implementation reproduced:

```text
H1 CANONICAL SHA-256 =
15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f
```

on the same local H1 JSONL artifact.

### 2.4 Final preflight

Final runner/breaker surface:

```text
RUNNER V0.4 =
SELF-BOUND TO ITS OWN GIT OBJECT

FINAL SYNTHETIC / PROVENANCE BREAKER =
13 / 13 PASS
```

No result had been observed before this final preflight passed.

## 3. Exact dataset revalidation

Real H1 artifact:

```text
IDENTITY =
USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1

LOCAL FILE SHA-256 =
94ccb7c78e2e21cb3baa2dfe0945e7b39e20f74300c3c72addb89135d5af1ca0

CANONICAL STREAM SHA-256 =
15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f

ROWS =
27677

CONTINUITY BLOCKS =
1436

FIRST H1 =
2021-05-25T01:00:00Z

LAST H1 =
2026-05-24T22:00:00Z
```

Dataset revalidation:

```text
PASS
```

TD03B and other reserved prospective confirmatory evidence were not consumed.

## 4. No-peek atomicity qualification

The two family envelopes were computed in one process and persisted together before either result was inspected.

Atomic result commit:

```text
f002a2dc84f70d8aa768962f1fc551c43cab0ba3
```

Persisted files:

```text
BREAKOUT =
reports/program/2026-10-02-SFE-02D-BREAKOUT-V1-RESULT-ENVELOPE.json

GIT BLOB =
e8dec64b78bed3e4dbd6534f7837c97791f6e242

SHA-256 =
bff35e4269603e7ca16d1659f3ef2afb31c9dc14699ef5ca8cf068b156a14b1


MEAN REVERSION =
reports/program/2026-10-02-SFE-02D-MEAN-REVERSION-V1-RESULT-ENVELOPE.json

GIT BLOB =
a294efd25302f01ccce6ea53a2fb83bac9f93e23

SHA-256 =
5be94345ea7f2a595206360acba0ddd1fcf24c5c90ad90ef4d35d1b6075a1399


DUAL MANIFEST =
reports/program/2026-10-02-SFE-02D-DUAL-RUN-MANIFEST.json

GIT BLOB =
bedb27b5cf19e5f383b11f649077391d67f5f4da

SHA-256 =
cda7d0e984b57cb43479895a18bc7c11f59a7b05049a1ba9d1050d078baf2400
```

The manifest records:

```text
single_process = true
both_envelopes_written_before_manifest = true
no_result_values_emitted_to_stdout = true
```

The two envelopes were first inspected only after the atomic result commit had been pushed.

Therefore:

```text
NO_PEEK_ATOMICITY =
PASS
```

## 5. Frozen decision rule applied

The preregistered primary surface for each family was:

```text
ALL VALID DIRECTIONAL EVENTS
```

with:

```text
Y_t =
direction_t × (C_(t+1) / C_t - 1)

PRIMARY REFERENCE =
RAW_ZERO
```

Evidence gates required all of:

```text
valid directional events >= 100
valid LONG events >= 20
valid SHORT events >= 20
event-bearing fixed 20-H1 blocks >= 30
```

Inference:

```text
cluster jackknife
over fixed event-bearing 20-H1 blocks
```

Multiplicity:

```text
Bonferroni across 2 decision-bearing family experiments

familywise alpha =
0.05

per-family two-sided alpha =
0.025

critical value =
2.241402727604947
```

Frozen mapping:

```text
CI lower > 0
→ SUPPORTED_ON_THIS_EXPLORATORY_E1_EXPOSED_SURFACE

CI upper <= 0
→ REFUTED_ON_THIS_EXPLORATORY_E1_EXPOSED_SURFACE

otherwise
→ NOT_INTERPRETABLE /
  NON_DECISIVE_STATISTICAL_EVIDENCE
```

No decision rule was changed after result observation.

## 6. BREAKOUT_V1 result

Evidence sufficiency:

```text
RAW DIRECTIONAL EVENTS =
688

VALID DIRECTIONAL EVENTS =
297

VALID LONG =
171

VALID SHORT =
126

EVENT-BEARING INFERENCE BLOCKS =
297

ALL EVIDENCE GATES =
PASS
```

Primary estimate:

```text
theta =
0.0005131894673214159

cluster-jackknife SE =
0.0002918824026987399

Bonferroni-adjusted CI =
[-0.00014103654622742525,
  0.001167415480870257]
```

The confidence interval crosses zero.

Frozen verdict:

```text
BREAKOUT_V1 =
NOT_INTERPRETABLE /
NON_DECISIVE_STATISTICAL_EVIDENCE
```

This means the preregistered experiment did not establish either:

```text
SUPPORTED
or
REFUTED
```

for the one-H1 behavioral Breakout proposition on this exact exploratory E1-exposed surface.

## 7. MEAN_REVERSION_V1 result

Evidence sufficiency:

```text
RAW DIRECTIONAL EVENTS =
1416

VALID DIRECTIONAL EVENTS =
612

VALID LONG =
262

VALID SHORT =
350

EVENT-BEARING INFERENCE BLOCKS =
612

ALL EVIDENCE GATES =
PASS
```

Primary estimate:

```text
theta =
-0.0003036181295215912

cluster-jackknife SE =
0.00017987160033643617

Bonferroni-adjusted CI =
[-0.0007067828251343461,
  0.00009954656609116369]
```

The confidence interval crosses zero.

Frozen verdict:

```text
MEAN_REVERSION_V1 =
NOT_INTERPRETABLE /
NON_DECISIVE_STATISTICAL_EVIDENCE
```

This means the preregistered experiment did not establish either:

```text
SUPPORTED
or
REFUTED
```

for the one-H1 behavioral Mean-Reversion proposition on this exact exploratory E1-exposed surface.

## 8. Mandatory diagnostics

Shared unconditional H1 drift:

```text
VALID SAME-BLOCK H1 TRANSITIONS =
26241

MEAN UNCONDITIONAL RETURN =
0.00001907812782388708
```

This remains a secondary diagnostic and does not replace the RAW_ZERO primary reference.

### 8.1 t+1 exclusions — Breakout

```text
EXCLUDED =
391 / 688 raw directional events

FRACTION =
0.5683139534883721

END_OF_CONTINUITY_BLOCK =
391

END_OF_DATASET =
0

OTHER_ADMISSIBILITY_FAILURE =
0

MEDIAN PRIOR ABS H1 RETURN — INCLUDED =
0.0022926043866677848

MEDIAN PRIOR ABS H1 RETURN — EXCLUDED =
0.002584055401291252
```

### 8.2 t+1 exclusions — Mean Reversion

```text
EXCLUDED =
804 / 1416 raw directional events

FRACTION =
0.5677966101694916

END_OF_CONTINUITY_BLOCK =
804

END_OF_DATASET =
0

OTHER_ADMISSIBILITY_FAILURE =
0

MEDIAN PRIOR ABS H1 RETURN — INCLUDED =
0.0016091355635006188

MEDIAN PRIOR ABS H1 RETURN — EXCLUDED =
0.0017347183911985975
```

The large exclusion fractions are caused entirely by continuity-block endings under the preregistered `t+1` admissibility rule.

These diagnostics were mandatory but no preregistered exclusion-fraction threshold existed.

Therefore they do **not** retroactively alter the frozen primary verdicts.

They remain an important design observation for any future separately authorized experiment.

## 9. Co-firing diagnostic

Persisted diagnostic counts:

```text
N_BREAKOUT_DIRECTIONAL =
688

N_MEAN_REVERSION_DIRECTIONAL =
1416

N_CO_FIRING =
687

N_BREAKOUT_EXCLUSIVE_OTHER_NEUTRAL =
1

N_BREAKOUT_EXCLUSIVE_OTHER_UNDEFINED =
0

N_MEAN_REVERSION_EXCLUSIVE_OTHER_NEUTRAL =
729

N_MEAN_REVERSION_EXCLUSIVE_OTHER_UNDEFINED =
0
```

This confirms the previously documented strong mechanical coupling on Breakout directional bars.

The co-firing surface remains descriptive only and does not create a comparative ranking.

## 10. No post-hoc rescue or optimization

No change was made after observing the results to:

- strategy rules;
- strategy parameters;
- dataset;
- window;
- continuity;
- event definition;
- `t+1` rule;
- evidence gates;
- inference blocks;
- cluster-jackknife formula;
- multiplicity;
- confidence threshold;
- primary reference;
- decision mapping.

No post-result integrity audit was initiated to rescue either result.

Therefore:

```text
POST_HOC_RESCUE =
NONE

OPTIMIZATION =
NONE

RESULT-DRIVEN CONTRACT MUTATION =
NONE
```

## 11. Scientific interpretation boundary

The correct scientific result is:

```text
BREAKOUT_V1 =
NON_DECISIVE
ON THIS EXACT EXPLORATORY E1-EXPOSED SURFACE

MEAN_REVERSION_V1 =
NON_DECISIVE
ON THIS EXACT EXPLORATORY E1-EXPOSED SURFACE
```

It is incorrect to conclude from SFE-02D that either family:

- is profitable;
- is unprofitable;
- has an economic edge;
- lacks an economic edge;
- is superior to the other;
- is robust;
- is confirmed;
- is generally refuted.

The experiment was behavioral, one-H1, Source-B/USTECH, historical, exploratory and E1-exposed.

## 12. Final qualification verdict

```text
SFE_02D_DATASET_REVALIDATION =
PASS

SFE_02D_FINAL_SYNTHETIC_PREFLIGHT =
PASS_13_OF_13

SFE_02D_NO_PEEK_ATOMIC_PERSISTENCE =
PASS

SFE_02D_BREAKOUT_EVIDENCE_GATES =
PASS

SFE_02D_MEAN_REVERSION_EVIDENCE_GATES =
PASS

SFE_02D_BREAKOUT_RESULT =
NOT_INTERPRETABLE_NON_DECISIVE

SFE_02D_MEAN_REVERSION_RESULT =
NOT_INTERPRETABLE_NON_DECISIVE

SFE_02D_PREREGISTERED_INFERENCE =
EXECUTED

SFE_02D_POST_HOC_OPTIMIZATION =
NONE

SFE_02D =
QUALIFIED_AND_CLOSED
```

## 13. Authority after closure

SFE-02D does not automatically authorize any next experiment or system change.

Still not authorized:

```text
PNL
ECONOMIC BACKTEST
EXECUTION MODEL
COST MODEL FOR THESE SFE RESULTS
OPTIMIZATION
PARAMETER CHANGE
RANKING
ROUTER
REGIME FILTER
TD03B CONSUMPTION
C01 RESERVED EVIDENCE CONSUMPTION
MT5
PAPER
BROKER
LIVE
CAPITAL
```

Any next step must start from the fact that the first preregistered dual behavioral experiment produced **non-decisive evidence for both families**.

## 14. STOP

```text
SFE-02D =
QUALIFIED_AND_CLOSED

BREAKOUT_V1 RESULT =
NON_DECISIVE

MEAN_REVERSION_V1 RESULT =
NON_DECISIVE

NEXT FRONTIER =
NOT AUTOMATICALLY AUTHORIZED

STOP =
TRUE
```
