# ADJUDICATION — Q-RM-10 ANOMALY MATRIX

**Date:** 5 septembre 2026  
**Status:** **UNIVERSAL FAILURE POLICY = PASS; CONCRETE ANOMALY MATRIX = BLOCKED**  
**Depends on:** Q-RM-04, Q-RM-05, Q-RM-06, Q-RM-08, Q-RM-09

## 1. PURPOSE

Convert the universal Q-RM-04 failure-scope rule into a falsifiable matrix without inventing format-specific anomaly classes.

## 2. [CONSÉQUENCE NÉCESSAIRE]

Every anomaly encountered during physical→logical interpretation must be classified by its normative effect, not by parser convenience.

The admissible semantic outcomes are:

```text
REJECT RECORD
REJECT ACQUISITION
QUALIFICATION BLOCKED
```

`INVALID` and `AMBIGUOUS` are not equivalent to zero observations or metadata.

## 3. LOCALISABILITY TEST

An anomaly is `LOCALISABLE` only when the applicable versioned binding provides constructive proof that:

1. boundaries of all unaffected occurrences remain uniquely determinable;
2. membership of all unaffected occurrences remains unchanged;
3. no alternative interpretation of the anomaly can modify the remainder of the logical universe.

Then:

```text
INVALID + LOCALISABLE → REJECT RECORD
otherwise → QUALIFICATION BLOCKED
```

`REJECT ACQUISITION` is permitted only where the applicable binding explicitly declares the anomaly acquisition-fatal.

## 4. CONCRETE MATRIX CONTRACT

For every supported binding, the anomaly registry must define at minimum:

```text
anomaly_class_id
trigger condition
detection evidence
affected physical scope
localisability test
possible interpretations
normative outcome
whether acquisition-fatal
whether qualification membership is affected
required diagnostic artifact
binding version
```

No unregistered anomaly may receive an implicit recovery policy.

## 5. ADVERSARIAL CASES

| Case | Minimum normative treatment |
|---|---|
| Malformed isolated record with proven boundaries | REJECT RECORD |
| Truncation with proven terminal boundary | May be REJECT RECORD if binding proves locality |
| Truncation with uncertain remainder | QUALIFICATION BLOCKED |
| Missing delimiter / merged records | QUALIFICATION BLOCKED unless locality is constructively proven |
| Corrupt framing affecting later units | QUALIFICATION BLOCKED or acquisition-fatal if explicitly declared |
| Unknown scope | QUALIFICATION BLOCKED |
| Parser cannot understand input | Not metadata; not C=0 |
| Anomaly after many valid records | No automatic valid-prefix qualification |

## 6. [CONTRACTUEL]

The project must enumerate concrete anomaly classes for each supported acquisition/format binding and explicitly map them to outcomes.

The matrix must be versioned with the semantics it depends on.

## 7. [ABSENCE DE PREUVE]

The universal Q-RM-04 policy is already closed, but the repository evidence reviewed does not contain a validated concrete anomaly registry covering the actual supported representations.

Therefore the concrete matrix cannot be passed by inference.

## 8. VERDICT

```text
Q-RM-10 UNIVERSAL FAILURE-SCOPE RULE = PASS
Q-RM-10 CONCRETE ANOMALY MATRIX = BLOCKED
```

## FIN
