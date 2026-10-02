# SFE-02E — NON-DECISIVE RESULT DIAGNOSTIC + NEXT-EXPERIMENT HYPOTHESIS MAP

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`

## 0. Authority and epistemic status

This artifact is produced under:

```text
SFE-02E
NON-DECISIVE RESULT DIAGNOSTIC
+ NEXT-EXPERIMENT HYPOTHESIS MAP
```

Contract:

```text
GOVERNANCE/SFE-02E-NON-DECISIVE-RESULT-DIAGNOSTIC-CONTRACT-V0.1.json
```

This phase is documentary and read-only with respect to performance.

It does not:

- read raw H1 data;
- recompute strategy signals;
- recompute behavioral `Y`;
- compute a new decision-bearing performance statistic;
- search lookbacks;
- search z thresholds;
- search response horizons;
- alter either V1 strategy;
- run a new experiment;
- calculate PnL;
- optimize;
- rank strategies.

Every candidate explanation introduced after SFE-02D is classified:

```text
POST_RESULT_EXPOSED
HYPOTHESIS_GENERATING
NOT_CONFIRMATORY
```

## 1. Canonical evidence base

SFE-02D closure:

```text
BLOB =
4365bef87dd9dd4613261aeba70dffe2e8ba4500
```

Breakout result envelope:

```text
BLOB =
e8dec64b78bed3e4dbd6534f7837c97791f6e242
```

Mean-Reversion result envelope:

```text
BLOB =
a294efd25302f01ccce6ea53a2fb83bac9f93e23
```

Dual-run manifest:

```text
BLOB =
bedb27b5cf19e5f383b11f649077391d67f5f4da
```

Dual preregistration freeze:

```text
BLOB =
72d3bbb05d76a69c3d5f487500908d3a9c40bc3c
```

Strategy-definition source:

```text
SFE-01 V0.2 BLOB =
027c42b38bf9c74415b21e98bcce19124f744995

SFE-01 HUMAN ADJUDICATION BLOB =
66aa556e4e161e49550451062273bc8d6422593c
```

## 2. What SFE-02D actually established

### 2.1 BREAKOUT_V1

**FACT**

```text
raw directional events =
688

valid directional events =
297

valid LONG =
171

valid SHORT =
126

event-bearing inference blocks =
297

all preregistered evidence gates =
PASS
```

Primary result:

```text
theta =
+0.0005131894673214159

cluster-jackknife SE =
0.0002918824026987399

Bonferroni-adjusted CI =
[-0.00014103654622742525,
 +0.001167415480870257]

status =
NOT_INTERPRETABLE /
NON_DECISIVE_STATISTICAL_EVIDENCE
```

### 2.2 MEAN_REVERSION_V1

**FACT**

```text
raw directional events =
1416

valid directional events =
612

valid LONG =
262

valid SHORT =
350

event-bearing inference blocks =
612

all preregistered evidence gates =
PASS
```

Primary result:

```text
theta =
-0.0003036181295215912

cluster-jackknife SE =
0.00017987160033643617

Bonferroni-adjusted CI =
[-0.0007067828251343461,
 +0.00009954656609116369]

status =
NOT_INTERPRETABLE /
NON_DECISIVE_STATISTICAL_EVIDENCE
```

### 2.3 Proximate statistical reason for non-decision

**FACT**

For both families:

```text
EVIDENCE-SUFFICIENCY GATES =
PASS

BUT

PREREGISTERED CONFIDENCE INTERVAL
CONTAINS ZERO
```

Therefore neither frozen decision rule reaches:

```text
SUPPORTED
or
REFUTED
```

**INTERPRETATION**

The immediate reason for the non-decisive outcome is not insufficient raw event count under the preregistered gates.

It is that the uncertainty remaining under the frozen dependence-aware inference is large enough that zero remains inside both decision intervals.

This statement does not identify the deeper causal reason for that uncertainty.

## 3. Diagnostic domain D01 — continuity and t+1 attrition

### Facts

BREAKOUT_V1:

```text
excluded directional events =
391 / 688

fraction excluded =
0.5683139534883721

END_OF_CONTINUITY_BLOCK =
391

END_OF_DATASET =
0

OTHER_ADMISSIBILITY_FAILURE =
0
```

MEAN_REVERSION_V1:

```text
excluded directional events =
804 / 1416

fraction excluded =
0.5677966101694916

END_OF_CONTINUITY_BLOCK =
804

END_OF_DATASET =
0

OTHER_ADMISSIBILITY_FAILURE =
0
```

Thus more than half of raw directional events in each family lacked an admissible same-block `t+1` response under the frozen experiment rules.

### Interpretation

This is a large measurement loss relative to the raw directional-event surface.

However:

```text
LARGE ATTRITION
DOES NOT BY ITSELF PROVE
THAT ATTRITION CAUSED
THE NON-DECISIVE RESULT
```

SFE-02C did not preregister an exclusion-fraction threshold that would invalidate the experiment.

Therefore SFE-02E must not retroactively declare SFE-02D invalid.

## 4. Diagnostic domain D02 — attrition-selection risk

### Facts

BREAKOUT_V1:

```text
median prior abs H1 return — included =
0.0022926043866677848

median prior abs H1 return — excluded =
0.002584055401291252
```

MEAN_REVERSION_V1:

```text
median prior abs H1 return — included =
0.0016091355635006188

median prior abs H1 return — excluded =
0.0017347183911985975
```

For both families, the persisted diagnostic shows a higher median prior observable absolute H1 return among excluded events than included events.

### Interpretation

This is a legitimate warning that t+1 admissibility is not obviously behavior-neutral.

It does **not** prove that exclusions are missing-not-at-random with respect to the unobserved behavioral outcome, nor does it show the direction or magnitude of any selection effect.

### Diagnostic conclusion

```text
ATTRITION_SELECTION_RISK =
PLAUSIBLE / NOT ESTABLISHED
```

This becomes a post-result hypothesis, not a correction to SFE-02D.

## 5. Diagnostic domain D03 — one-H1 response-horizon scope

### Facts

Both adopted V1 definitions explicitly test:

```text
ONE RESPONSE H1 BAR
```

The definitions explicitly deny claims about persistence or reversion beyond the immediately following admissible H1 bar.

SFE-02D therefore tested only:

```text
t
→
t+1
```

### Interpretation

SFE-02D contains no evidence capable of deciding whether either family exhibits a behavioral effect at another response horizon.

Therefore:

```text
SFE-02D NON-DECISION
≠
MULTI-HORIZON NON-DECISION
```

No alternative horizon may now be selected from the exposed SFE-02D surface.

## 6. Diagnostic domain D04 — BREAKOUT_V1 construct validity

### Facts

The adopted BREAKOUT_V1 construct is:

```text
20-BAR PRIOR-CLOSE RANGE-EXTREME BREACH
+
ONE-BAR DIRECTIONAL CONTINUATION
```

It explicitly:

```text
DOES NOT REQUIRE
PRIOR VOLATILITY COMPRESSION
```

and SFE-01 states:

```text
BREAKOUT_V1
≠
COMPRESSION_CONDITIONED_BREAKOUT
```

### Interpretation

The SFE-02D result is evidence only about this minimal range-extreme construct.

It does not decide whether a conceptually narrower breakout construct would behave differently.

This is a construct-validity boundary, not evidence that the V1 definition should now be changed.

## 7. Diagnostic domain D05 — MEAN_REVERSION_V1 construct validity

### Facts

MEAN_REVERSION_V1 uses price levels relative to the recent 20-bar mean and population dispersion.

SFE-01 explicitly states:

```text
MEAN_REVERSION_V1
DOES NOT DISTINGUISH
STEADY TREND DISPLACEMENT
FROM SHOCK-LIKE DISPLACEMENT
```

### Interpretation

A directional event may therefore represent either:

- a displacement that could plausibly revert;
- or a continuing trend that merely places the current level far from the recent mean.

The non-decisive SFE-02D result cannot determine whether this construct mixture diluted, reversed or had no material effect on the primary result.

## 8. Diagnostic domain D06 — cross-family mechanical coupling

### Facts

Persisted SFE-02D counts:

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
```

SFE-01 had already established before the experiment that on directional co-firing bars:

```text
d_BREAKOUT =
-d_MEAN_REVERSION
```

and because the same `R_(t,t+1)` is used:

```text
Y_BREAKOUT =
-Y_MEAN_REVERSION
```

### Interpretation

The two V1 families are not independent behavioral probes on Breakout directional bars.

Almost the entire Breakout directional surface is mechanically paired with an opposite Mean-Reversion directional state.

This reduces the degree of orthogonal information provided by treating those co-firing events as conceptually independent family evidence.

It does not justify ranking, combining, inverting or deleting either family post hoc.

## 9. Diagnostic domain D07 — source, instrument and period specificity

### Facts

SFE-02D used exactly:

```text
USTECH / Nasdaq 100 Index CFD
SOURCE_B
historical H1 surface
2021-05-25 → 2026-05-24
```

The evidence was explicitly:

```text
EXPLORATORY
E1_EXPOSED
NOT_PRISTINE_CONFIRMATORY
```

### Interpretation

The result does not establish that the same finding would hold:

- on another data source;
- on another instrument;
- in another period;
- prospectively;
- under a pristine confirmatory design.

This is a generalization boundary, not proof that a different source or period would produce a different result.

## 10. Diagnostic domain D08 — RAW_ZERO and unconditional drift

### Facts

The primary reference was frozen as:

```text
RAW_ZERO
```

Shared secondary diagnostic:

```text
mean unconditional H1 return =
0.00001907812782388708

valid same-block H1 transitions =
26241
```

The unconditional drift diagnostic was explicitly secondary and non-decision-bearing.

### Interpretation

A nonzero unconditional drift is present in the recorded diagnostic.

SFE-02E cannot conclude that this drift caused either family result.

It also cannot replace the frozen RAW_ZERO proposition with a drift-adjusted proposition after seeing SFE-02D.

Any future drift-relative proposition would be a different, separately preregistered experimental question.

## 11. Diagnostic domain D09 — genuine null, weak or heterogeneous effect remains possible

### Facts

Both confidence intervals include zero.

The signs of the point estimates differ:

```text
BREAKOUT theta > 0

MEAN_REVERSION theta < 0
```

but neither sign satisfies the frozen decision rule by itself.

### Interpretation

At least three broad explanations remain compatible with the persisted evidence:

```text
A. the underlying effect is absent or very small;

B. an effect exists but the available admissible evidence
   is too uncertain under the frozen design;

C. heterogeneous effects cancel or vary across contexts
   that SFE-02D did not preregister as decision-bearing.
```

SFE-02D cannot distinguish these explanations.

The third possibility does not authorize subgroup mining.

## 12. What SFE-02D did and did not teach us

### Established

```text
1. both deterministic V1 kernels can be run reproducibly;

2. both experiments met their preregistered minimum evidence gates;

3. both primary intervals contain zero;

4. both primary verdicts are NON_DECISIVE;

5. t+1 continuity attrition is large in both families;

6. excluded events show higher persisted median prior absolute H1 movement
   than included events in both families;

7. Breakout directional events are almost entirely co-firing
   with Mean-Reversion directional events;

8. the test was one-H1, Source-B/USTECH, historical and E1-exposed.
```

### Not established

```text
1. that continuity attrition caused the non-decision;

2. that another response horizon would work better;

3. that a compression-conditioned breakout would work better;

4. that a shock-specific mean-reversion construct would work better;

5. that another source, instrument or period would produce a decision;

6. that either family has or lacks economic edge;

7. that either family is superior;

8. that more data necessarily resolves the uncertainty.
```

## 13. Post-result hypothesis map

Every hypothesis below is:

```text
STATUS =
OPEN_POST_RESULT_HYPOTHESIS

EXPOSURE =
POST_RESULT_EXPOSED

CONFIRMATORY STATUS =
NONE
```

### H-E01 — continuity attrition may materially affect evidentiary resolution

**Candidate explanation**

The large loss of directional events at continuity-block endings may reduce effective information and/or induce a selected admissible-event surface.

**Basis in persisted evidence**

```text
Breakout excluded fraction ≈ 56.8%
Mean-Reversion excluded fraction ≈ 56.8%

all exclusions =
END_OF_CONTINUITY_BLOCK
```

Excluded-event prior absolute H1 movement is also higher in median than included-event prior movement for both families.

**What is not established**

- that excluded events would have different `Y`;
- that including them would change either verdict;
- that the current segmentation rule is wrong.

**Falsification question**

> On a separately preregistered evidence surface whose continuity/admissibility properties are fixed independently of SFE-02D outcomes, does the same frozen V1 proposition remain non-decisive when t+1 coverage is materially different?

**Minimum new evidence class**

A new preregistered dataset/continuity contract with explicit exposure status and no silent use of reserved confirmatory evidence.

**Contamination risk**

High if a source is selected because its continuity profile appears favorable after SFE-02D.

---

### H-E02 — the one-H1 response horizon may be misaligned with the behavioral timescale

**Candidate explanation**

The hypothesized continuation or reversion phenomenon may not be resolved within exactly one following H1 bar.

**Basis in persisted evidence**

Both V1 hypotheses were explicitly restricted to one response H1.

SFE-02D says nothing about other response horizons.

**What is not established**

- that a longer or shorter horizon produces an effect;
- that any particular alternative horizon is scientifically preferable.

**Falsification question**

> Does a separately justified and preregistered response-horizon proposition produce a different inferential conclusion under a design whose horizon is fixed before observing its outcomes?

**Minimum new evidence class**

A new experiment version with the response horizon justified independently of post-result performance inspection.

**Contamination risk**

Very high if multiple horizons are tried on the exposed SFE-02D evidence and the most favorable is selected.

---

### H-E03 — BREAKOUT_V1 may be too broad a construct for a compression-breakout proposition

**Candidate explanation**

A prior-close range-extreme breach without a compression condition may mix structurally different events under the label "breakout."

**Basis in persisted evidence**

SFE-01 explicitly defines BREAKOUT_V1 as not compression-conditioned.

**What is not established**

- that compression conditioning improves the behavioral effect;
- that the V1 construct is invalid;
- that a narrower construct is superior.

**Falsification question**

> Does a separately versioned breakout construct, defined from an independently motivated concept of pre-break compression before seeing its outcomes, behave differently from the frozen V1 proposition?

**Minimum new evidence class**

A new strategy-definition version, external/adversarial review, implementation qualification, and newly preregistered experiment.

**Contamination risk**

Very high if compression is defined by trying candidate filters against the already exposed outcome surface.

---

### H-E04 — MEAN_REVERSION_V1 may mix trend displacement with reversion-type displacement

**Candidate explanation**

A level-based z displacement can become directional during a steady trend, so the V1 event population may combine qualitatively different price processes.

**Basis in persisted evidence**

This limitation was explicitly declared in SFE-01 before SFE-02D.

**What is not established**

- that shock-like displacement reverts more strongly;
- that trend displacement explains the negative point estimate;
- that a different displacement definition is superior.

**Falsification question**

> Does a separately versioned mean-reversion construct that distinguishes the intended displacement mechanism before outcome observation produce a different result under new preregistered evidence?

**Minimum new evidence class**

A new strategy-definition version and experiment contract, with construct semantics fixed before performance.

**Contamination risk**

Very high if displacement classes are discovered by mining SFE-02D outcomes.

---

### H-E05 — mechanical coupling may limit the information gained from the dual-family comparison

**Candidate explanation**

Because nearly every Breakout directional event co-fires with an opposite Mean-Reversion directional event, the pair may provide less independent family information than their separate names imply.

**Basis in persisted evidence**

```text
687 / 688 Breakout directional events
co-fire with Mean-Reversion
```

and the algebraic relation:

```text
Y_BREAKOUT =
-Y_MEAN_REVERSION
```

was preregistered for co-firing bars.

**What is not established**

- that coupling caused either non-decisive verdict;
- that one family should be removed;
- that a different family pair would be better.

**Falsification question**

> Would separately defined behavioral probes with materially less mechanical overlap provide genuinely different evidentiary information under a preregistered design?

**Minimum new evidence class**

A new family-definition or comparison design whose independence claim is explicitly tested rather than assumed.

**Contamination risk**

High if "orthogonality" is optimized against the already observed SFE-02D results.

---

### H-E06 — the finding may be source/instrument/period-specific

**Candidate explanation**

The non-decisive outcome may reflect the specific USTECH / Source-B / historical-period evidence surface rather than a general family property.

**Basis in persisted evidence**

Only one instrument/source historical surface was tested, and it was E1-exposed.

**What is not established**

- that another source or instrument changes the result;
- that the current source is deficient;
- that cross-asset replication will become decisive.

**Falsification question**

> Do the exact frozen V1 definitions reproduce the same qualitative inferential outcome on separately preregistered evidence not selected from SFE-02D performance?

**Minimum new evidence class**

Independent or prospective evidence with an explicit provenance/exposure classification.

**Contamination risk**

High if assets or periods are screened and only favorable replications retained.

---

### H-E07 — the V1 behavioral effects may simply be absent, weak or too heterogeneous to distinguish from zero

**Candidate explanation**

The most conservative explanation remains that the frozen V1 propositions may have no stable positive one-H1 effect of a magnitude distinguishable under this design.

**Basis in persisted evidence**

Both primary intervals include zero despite passing the minimum evidence gates.

**What is not established**

- exact zero effect;
- permanent absence of effect;
- absence at other horizons or under other constructs.

**Falsification question**

> Under a new preregistered replication of the same frozen V1 proposition, does evidence emerge that excludes zero according to a decision rule fixed before outcomes?

**Minimum new evidence class**

New evidence capable of testing the same frozen proposition without parameter or construct changes.

**Contamination risk**

Lower than construct-changing hypotheses if the V1 definitions are kept exactly fixed, but still requires explicit exposure/source governance.

---

### H-E08 — continuity exclusions may interact with observable market-state intensity

**Candidate explanation**

The higher persisted median prior absolute H1 movement among excluded events suggests that block endings may occur disproportionately around higher-movement contexts.

**Basis in persisted evidence**

For both families:

```text
median prior abs H1 return excluded
>
median prior abs H1 return included
```

**What is not established**

- a causal relation between continuity endings and volatility;
- that this interaction biases `theta`;
- that any volatility-conditioned strategy is justified.

**Falsification question**

> Under a separately preregistered data-quality study, are continuity endings statistically associated with pre-event observable movement intensity independently of strategy outcome?

**Minimum new evidence class**

A data-quality/measurement experiment whose target is continuity behavior itself, not strategy performance.

**Contamination risk**

Moderate to high if the diagnostic is converted directly into a volatility filter for the strategies.

## 14. Candidate next-experiment question classes

SFE-02E does not select a next experiment.

It identifies four legitimate **question classes** that could later be adjudicated:

```text
CLASS A — REPLICATION
Keep the V1 strategy definitions fixed
and ask whether the result reproduces on new evidence.

CLASS B — MEASUREMENT / CONTINUITY
Study whether the data-continuity mechanism materially shapes
which directional events receive admissible t+1 outcomes.

CLASS C — RESPONSE-TIMESCALE
Ask a separately preregistered behavioral question
at a theoretically justified response timescale.

CLASS D — CONSTRUCT REVISION
Create a new strategy version for a more specific
breakout or mean-reversion construct.
```

None is authorized.

No class is declared superior by SFE-02E.

## 15. Anti-snooping firewall after SFE-02D

The following actions would invalidate a claim of clean prospective discovery if performed directly on the exposed SFE-02D surface:

```text
TRY MULTIPLE LOOKBACKS
→ SELECT BEST

TRY MULTIPLE Z THRESHOLDS
→ SELECT BEST

TRY MULTIPLE RESPONSE HORIZONS
→ SELECT BEST

ADD COMPRESSION DEFINITIONS
→ SELECT BEST

ADD VOLATILITY / ATR FILTERS
→ SELECT BEST

MINE LONG / SHORT SUBGROUPS
→ REDEFINE PRIMARY RULE

USE CO-FIRING SUBGROUPS
→ SELECT FAVORABLE FAMILY

SCREEN ASSETS OR PERIODS
→ REPORT ONLY FAVORABLE ONES
```

Such work could be exploratory hypothesis generation only and would require explicit labeling plus new validation evidence before any confirmatory claim.

## 16. Diagnostic conclusion

The strongest conclusion supported by the current record is:

```text
SFE-02D WAS NON-DECISIVE
BECAUSE BOTH PREREGISTERED PRIMARY INTERVALS
CONTAINED ZERO.

THE RECORD ALSO REVEALS
MATERIAL DESIGN/MEASUREMENT LIMITS:
- large t+1 continuity attrition;
- possible attrition-selection risk;
- one-H1-only response scope;
- known construct-validity limits;
- very strong cross-family mechanical coupling;
- one-source / one-instrument / one-historical-surface scope.

NONE OF THESE LIMITS
HAS BEEN SHOWN TO CAUSE
THE NON-DECISIVE RESULT.
```

Therefore the correct next epistemic state is not:

```text
TUNE UNTIL ONE WORKS
```

It is:

```text
CHOOSE ONE NEW QUESTION
FOR A NEW PREREGISTERED TEST
OR
REPLICATE THE SAME FROZEN QUESTION
ON NEW EVIDENCE
```

## 17. SFE-02E state

```text
SFE_02E_DIAGNOSTIC =
COMPLETE

SFE_02E_HYPOTHESIS_MAP =
COMPLETE

POST_RESULT_HYPOTHESES =
H-E01 THROUGH H-E08

RAW_DATA_RECOMPUTATION =
NONE

NEW PERFORMANCE METRIC =
NONE

PARAMETER SEARCH =
NONE

STRATEGY CHANGE =
NONE

NEW EXPERIMENT =
NONE

NEXT_EXPERIMENT_SELECTION =
PENDING HUMAN DECISION

STOP =
TRUE
```

## 18. STOP

No new experiment, strategy version, parameter change, response horizon, data source, PnL surface, ranking or router is authorized by SFE-02E.

The next boundary is a human adjudication over which **question class** should be pursued next, followed by a separately preregistered design.

