# B-PE-04R — EVIDENCE PROPORTIONALITY / NECESSITY REVIEW — FINAL PERSISTED-HEAD RE-BREAK

**Date:** 2026-09-20  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Corrected review HEAD:** `6b793277cba1d63943bdbb5522a58b11e26c318d`  
**Corrected review blob:** `33dd9d41342902d4e0efd17f3bdd2b1e603f1a4a`

## 1. Review question

Determine whether unresolved documentary dimensions:

```text
C08-D4 — USATECH legacy-hourly applicability
C08-D5 — target temporal/version continuity 2021–2026
```

must force immediate Dukascopy contact before any further empirical work.

Compared outcomes:

```text
CONTINUE
SIMPLIFY
KEEP BLOCKED
```

## 2. Material risk confirmed

The review confirms C08-D4/D5 protect a real failure mode.

Counterexample:

```text
provider representation changes
+
legacy hourly path remains partially compatible
+
returned bytes are structurally valid
+
project constructs D from the wrong external representation premise
```

Then:

```text
D can be internally complete relative to the wrong manifest
B can decode successfully
Q can conserve every slot
I_A and I_B can agree
O can report equality
yet authoritative provider observations can still be omitted or mis-scoped
```

Therefore:

```text
D/Q/I_A/I_B agreement alone
≠ proof of external provider representation applicability
```

## 3. Existing-control capability

```text
D            = PARTIAL DETECTION
B/A/Q        = PARTIAL DETECTION
I_A/I_B/O    = cannot falsify a shared external premise
```

The current machinery is strong against implementation divergence and structural inconsistency.

It is not, by itself, an external-representation discriminator.

## 4. Why direct provider dispatch is not the proportional next step

A provider response would provide documentary authority but:

- creates an external dependency;
- may be delayed, incomplete or ambiguous;
- does not directly validate the exact bytes actually acquired by the project;
- Q1-Q3 would close at most C08 scope/continuity questions;
- C01-C07 physical semantics would still require separate evidence;
- no explicit current project requirement was found for point-in-time archival reproduction of the exact feed representation as served at historical time T.

The current research objective is operational historical backtesting using governed acquired material, not forensic reconstruction of every provider infrastructure transition.

If that objective changes to point-in-time archival fidelity, this proportionality decision must be reopened.

## 5. More proportional path

Introduce a pre-D empirical representation discriminator.

It must test the external premise before full acquisition membership is trusted.

Required properties include:

```text
bounded scope
exact provider locator/status/headers/bytes/hash capture
USATECHIDXUSD-specific binding
no hourly-first assumption
known candidate representations tested without closed-world assumption
UNKNOWN_REPRESENTATION = BLOCKED
cross-family coverage/cardinality comparison
independent semantic plausibility checks
no backtest
no silent promotion to full D
```

## 6. Anti-extrapolation requirement

The final adversarial break demonstrated:

```text
BPE04R-F01 — BOUNDED_SAMPLE_TO_FULL_INTERVAL_PROMOTION_NOT_CLOSED
BPE04R-F02 — CLOSED_WORLD_HOURLY_DAILY_LOCATOR_ASSUMPTION
```

Both are closed.

Mandatory distinction:

```text
PROBE_SUPPORTED
≠
FULL_INTERVAL_QUALIFIED
```

A bounded probe may:

- falsify a representation premise;
- establish behavior for observed dates;
- identify candidate transition regimes.

It may not certify complete 2021–2026 continuity by sampling.

Before full D completeness can rely on a representation rule, every manifest-relevant interval must be covered by:

- exhaustive locator/membership evidence;
- deterministic qualified transition-boundary evidence;
- or another explicitly qualified full-interval method.

No sample extrapolation.

## 7. Open-world requirement

Known hourly/daily candidates are not assumed exhaustive.

If provider material exists but no known representation explains it:

```text
UNKNOWN_REPRESENTATION
→ BLOCKED
```

No closest-format fallback is allowed.

## 8. B-PE-01 boundary preserved

This review does not set:

```text
C08-D4 = PASS
C08-D5 = PASS
BPE-C08 = PASS
B = PASS
```

Current state remains:

```text
C08-D4 = BLOCKED
C08-D5 = BLOCKED
BPE-C08 = BLOCKED
B global executable gate = BLOCKED
FINAL EXECUTABLE DATA GATE = BLOCKED
```

B-PE-01 V0.1 is not silently weakened.

If empirical evidence is later proposed as sufficient for global B promotion, governance must explicitly version/supersede the relevant evidence-sufficiency rule before promotion.

## 9. Final proportionality verdict

```text
B-PE-04R EVIDENCE PROPORTIONALITY / NECESSITY REVIEW = PASS

DECISION = SIMPLIFY
```

Meaning:

```text
B-PE-05 governed provider clarification dispatch = DO NOT EXECUTE NOW

CONTINUE provider-contact route = rejected as immediate next action

KEEP BLOCKED waiting solely for provider clarification = rejected

next path = formalize bounded empirical representation discrimination
```

Provider clarification remains an optional fallback only if the empirical path becomes ambiguous, contradictory or insufficient.

## 10. Exactly one next governed action

Open only:

```text
B-ERD-01 — bounded empirical representation-discrimination contract
```

Formalization only:

```text
fresh HEAD
→ define exact empirical hypotheses
→ define bounded stratified USATECH probe dates
→ define known candidate representation/locator families without closed-world assumption
→ define UNKNOWN_REPRESENTATION = BLOCKED
→ define exact raw response/provenance capture
→ define cross-family representation/coverage comparison
→ define independent semantic plausibility checks
→ define PROBE_SUPPORTED / PROBE_REFUTED / BLOCKED
→ explicitly forbid sample→full-interval promotion
→ define what later evidence can establish FULL_INTERVAL_QUALIFIED
→ adversarial break
→ persisted-HEAD re-break
→ audit + backup + checkpoint
→ STOP
```

Still prohibited during B-ERD-01 formalization:

```text
provider contact
real BI5 download
real BI5 processing
real acquisition
D materialization
real Q/F/Q-RM-12 execution
backtest
paper/broker/live
```

A later bounded empirical execution remains a separate authorization boundary.

## 11. External-state confirmation

```text
B-PE-05 executed = NO
Dukascopy contacted = NO
ticket/email/forum post created = NO
```
