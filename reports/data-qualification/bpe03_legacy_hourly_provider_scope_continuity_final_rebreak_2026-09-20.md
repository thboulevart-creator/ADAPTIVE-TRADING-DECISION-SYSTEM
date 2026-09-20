# B-PE-03 — LEGACY-HOURLY BI5 PROVIDER-PRIMARY SCOPE / VERSION CONTINUITY — FINAL PERSISTED-HEAD RE-BREAK

**Date:** 2026-09-20  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Corrected candidate HEAD:** `14740bec256d97c86761c89af8e74b5d6c8ca04b`  
**Corrected evidence bundle blob:** `f934df8ea93018ee0c22b2d69575f15fc8f2c72f`  
**Corrected candidate report blob:** `f0970e50746993343590cb4ef252727c0457935e`

## 1. Provider-owned evidence searched

Provider-owned/versioned/archived/persisted evidence used:

1. Dukascopy API Support dated 2013-11-07:
   provider statement linking historical tick history, earliest-history HTTP file server and an hour-addressed `h_ticks.bi5` object.
2. Dukascopy official Maven DDS2/JForex repository:
   versioned client artifacts spanning 2021-01 through 2025-10.
3. Dukascopy JForex 4.8.0 release notes:
   versioned 2026-03-03 release introducing historical price data from JETTA.

Current live daily-format documentation was not promoted as immutable legacy-hourly continuity evidence.

## 2. Initial candidate defects

Adversarial break demonstrated exactly:

```text
BPE03-F01 — FREE_TEXT_CORROBORATION_BYPASSES_EVIDENCE_BINDING
BPE03-F02 — JETTA_BACKEND_CHANGE_MISCLASSIFIED_AS_CONTRADICTION
```

Corrections:

- imported exact BPE02-E03 and BPE02-E09 source records + sealed admissibility decisions;
- created exact closed BPE03 cross-bundle ClaimEvidenceAssertions;
- removed JETTA from claim SUPPORT/CONTRADICT stance;
- retained JETTA only as contextual provider boundary evidence.

## 3. Persisted-head integrity re-break

Recomputed from persisted evidence bytes:

```text
admissibility decision seal mismatches = 0
lineage digest mismatch                = 0
evidence-set digest mismatch           = 0
assertion-set digest mismatch          = 0
adjudication seal mismatch             = 0
```

Final adjudication seal:

`90c240c2aea78fed5fd1509daecf390fd439b38376e3c3a4fc4368d19d6af2be`

Final evidence-set digest:

`5cdf41debc110d5b5de0cedd552643300e75b2a03b305cfb9220f18c62fdf30c`

Final assertion-set digest:

`42761bf85b04b43710770c069f965ac314e7baa9714c6ff81c554c1295f62d3b`

## 4. Final semantic adversarial matrix

```text
historical provider statement → target temporal continuity     REJECTED
Maven client versions → unchanged file format                 REJECTED
JETTA 2026-03-03 → public BI5 transition date                 REJECTED
generic legacy hourly → USATECH legacy hourly                 REJECTED
current daily documentation → legacy hourly byte semantics    REJECTED
independent implementations → replace provider-primary        REJECTED
```

No new adjudication defect was demonstrated.

## 5. Re-adjudicated dimensions

```text
C08-D1 provider identity applicability            = PASS
C08-D2 legacy hourly BI5 family existence         = PASS
C08-D3 historical tick file-object family binding = PASS
C08-D4 USATECH legacy-hourly applicability        = BLOCKED
C08-D5 target temporal/version continuity          = BLOCKED
```

Therefore:

```text
BPE-C08 = BLOCKED
```

No C01-C07 dimension was reopened.

## 6. What B-PE-03 established

Provider-primary evidence now proves, with independent corroboration:

```text
Dukascopy
→ historical tick file server
→ legacy hourly h_ticks.bi5 object family
```

This is real progress over B-PE-02.

## 7. What remains absent

No searched provider-owned immutable/versioned artifact establishes either:

```text
A. USATECHIDXUSD specifically belonged to the same legacy-hourly BI5 scope
   for the target research epoch
```

or:

```text
B. the exact hourly→daily transition / continuity boundary proving that
   legacy-hourly BI5 semantics apply through
   2021-08-14 → 2026-08-14.
```

The 2026-03-03 JETTA release is a boundary clue only.

## 8. Final verdict

```text
B-PE-03 LEGACY-HOURLY PROVIDER-PRIMARY
SCOPE / VERSION CONTINUITY EVIDENCE = BLOCKED

overall_provider_evidence_status = BLOCKED
B global executable gate = BLOCKED
FINAL EXECUTABLE DATA GATE = BLOCKED
```

This is BLOCKED by absent exact provider-primary continuity evidence, not FAIL of the historical hourly hypothesis.

## 9. Smallest admissible alternative evidence route

B-PE-01's provider-primary requirement remains unchanged.

Open only:

```text
B-PE-04 — provider-authoritative hourly→daily transition clarification package
```

Goal:

obtain and persist a Dukascopy-authored, exact, citable response/artifact answering at minimum:

1. the date/version boundary at which public historical tick objects moved from hourly `HHh_ticks.bi5` to daily files;
2. whether legacy hourly BI5 remained the applicable representation for 2021-08-14 → that transition;
3. whether USATECHIDXUSD used that legacy hourly representation during the target interval.

Optional only if provided in the same authoritative response:

- exact legacy-hourly compression/envelope;
- record layout/signedness;
- timestamp offset rules;
- USATECH raw price divisor.

No threshold relaxation is authorized if the provider does not answer.

No project BI5 download, processing, acquisition or backtest occurred.
