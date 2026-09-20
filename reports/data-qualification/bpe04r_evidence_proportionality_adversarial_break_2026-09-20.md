# B-PE-04R — EVIDENCE PROPORTIONALITY / NECESSITY REVIEW — ADVERSARIAL BREAK

**Date:** 2026-09-20  
**Candidate HEAD:** `1d6db3fec533723775e1e1ad8fc7dc8f47cbb02f`  
**Candidate review blob:** `d2ac1889a5d598d0752345f7bfe0415e5a1c2824`

## 1. Attacks that the candidate survives

### A1 — shared false premise survives I_A/I_B agreement

Survived.

The candidate explicitly states that D/Q/I_A/I_B cannot independently falsify a common external representation premise.

### A2 — structurally valid compatibility alias silently omits data

Survived.

The candidate explicitly requires cross-family coverage/cardinality comparison rather than relying on decode success.

### A3 — provider contact is the only way to know historical policy

Rejected as a necessity claim for the current research objective.

The candidate distinguishes provider historical-policy truth from operational truth about material actually acquired now.

### A4 — point-in-time archival fidelity requirement

No currently declared repository requirement was identified that the backtest must reproduce the exact provider representation as served contemporaneously at historical time T.

The candidate correctly keeps this as a reopen condition if project scope later changes.

### A5 — silent bypass of B-PE-01

Survived.

C08-D4/D5 remain BLOCKED and B remains BLOCKED. The candidate explicitly forbids using empirical evidence to silently rewrite B-PE-01 V0.1.

---

## 2. Demonstrated defects

### BPE04R-F01 — BOUNDED_SAMPLE_TO_FULL_INTERVAL_PROMOTION_NOT_CLOSED

Candidate next action proposes a:

`minimal stratified USATECH target-date sample`.

Attack:

```text
2021 sample = hourly
2023 sample = hourly
2025 sample = hourly
2026 sample = hourly

but a temporary representation change occurred during a non-sampled period
or a transition occurred between samples and later reverted.
```

A bounded sample can demonstrate that at least one observed date behaves a certain way.

It cannot by itself establish:

```text
full 2021-08-14 → 2026-08-14 representation continuity
```

or authorize a full-period D component manifest.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Separate future empirical outcomes:

```text
PROBE_SUPPORTED
≠ FULL_INTERVAL_QUALIFIED
```

A bounded discriminator may falsify a premise or identify candidate regimes.

Before full D completeness can rely on that result, the representation rule must be established for every manifest-relevant interval through either:

- exhaustive locator/membership evidence;
- deterministic transition-boundary evidence;
- or another explicitly qualified full-interval method.

No sample extrapolation.

---

### BPE04R-F02 — CLOSED_WORLD_HOURLY_DAILY_LOCATOR ASSUMPTION

Candidate future discriminator says:

`probe all plausible provider object families allowed by evidence`.

Attack:

Provider serves an undocumented or third representation family.

If the discriminator tests only known hourly and daily forms, both may fail and the implementation may incorrectly choose the "least bad" known candidate, or treat absence as missing data rather than unknown representation.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

The future discriminator must have an explicit:

```text
UNKNOWN_REPRESENTATION
```

state.

Rules:

- no candidate winner when all known representations fail;
- no candidate winner when provider material exists but matches no qualified signature;
- unexpected successful object/locator/content signature becomes evidence of an unknown representation;
- unknown representation = BLOCKED, not fallback.

---

## 3. Information-cost decision challenge

Even after F01/F02, the relative-cost conclusion remains stable:

Provider clarification:

- high documentary authority;
- uncertain responsiveness;
- external dependency;
- does not by itself validate acquired bytes;
- Q1-Q3 do not close C01-C07.

Empirical discrimination:

- directly tests current operational material;
- can falsify wrong representation assumptions;
- can be bounded before any backtest;
- requires strong anti-extrapolation and open-world handling.

The candidate decision `SIMPLIFY` is not overturned.

## 4. Break verdict

```text
B-PE-04R CANDIDATE = FAIL
```

because F01/F02 require correction.

Only those two defects are authorized for correction.

No provider contact, BI5 download, real acquisition or backtest occurred.
