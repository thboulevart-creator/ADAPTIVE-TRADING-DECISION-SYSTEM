# QUALIFICATION INPUT REGISTER — V1

**Date:** 6 septembre 2026  
**Status:** **BLOCKED — execution inputs not yet established**  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Reference state:** `a55fbdfa3995397003303605c26ce7253f1ecb30` (`main`)  
**Purpose:** provide a machine-auditable inventory of the concrete inputs required by the global executable gate without inventing project facts.

---

## 1. Governing rule

The global gate `RB-A → Q-RM-12` requires concrete, versioned, normative inputs before a real execution PASS can be claimed.

This register is an execution aid, not a substitute for those inputs and does not promote any proposal to normative status.

---

## 2. Required inputs

| ID | Required input | Current status | Closure evidence required |
|---|---|---|---|
| D | Acquisition declaration + complete component manifest | **BLOCKED** | Immutable declaration naming the acquisition domain, representation, components, membership policy and completeness evidence |
| R | Representation identity/version | **BLOCKED** | Explicit project decision identifying every supported qualification representation and version |
| M | Record-model version | **BLOCKED** | Explicit reference to the exact frozen record-model version used by the qualification run |
| B | Concrete format binding(s) | **BLOCKED** | Versioned binding defining framing, segmentation, cardinality, fields, individuation and malformed/ambiguous behavior |
| A | Concrete anomaly matrix | **BLOCKED** | Versioned matrix mapping every declared anomaly class to scope and mandatory outcome |
| Q | Qualification contract + parameters | **BLOCKED** | Immutable contract containing qualification identity, parameters, acceptance/rejection rules and adversarial variants |
| F | Freeze artifact + persistence | **BLOCKED** | Concrete serialized artifact and deterministic reconstruction procedure |
| O | Deterministic semantic comparison oracle | **BLOCKED** | Independently reviewable oracle defining equality of qualified logical occurrences |
| I_A | Reference implementation | **BLOCKED** | Executable implementation conforming to D/R/M/B/Q/A/F/O |
| I_B | Independent comparison implementation | **BLOCKED** | Independently implemented path with no shared semantic shortcut that could mask the same defect |

---

## 3. Non-assumptions

The following are intentionally **not selected by this register**:

- CSV, JSON, JSONL, Parquet, binary or any other representation;
- filename-based acquisition membership;
- parser/library defaults;
- file hash as occurrence identity;
- physical row index as occurrence identity;
- provider identity as semantic membership;
- implicit completeness from successful download or file presence;
- any undocumented anomaly class;
- any implementation-derived fallback for malformed or ambiguous input.

A concrete choice becomes normative only through the applicable project adjudication and versioned artifact.

---

## 4. Closure sequence

```text
D + R + M
    ↓
B + A
    ↓
Q
    ↓
F + O
    ↓
I_A + I_B
    ↓
real execution
    ↓
Universe(A) = Universe(B)
    ↓
mandatory adversarial variants conform
    ↓
FINAL EXECUTABLE GATE = PASS
```

Any missing prerequisite keeps the gate **BLOCKED**. A failing adversarial case yields **FAIL**; it is never converted to PASS by changing the expected result after observation.

---

## 5. Relationship to existing adjudication

This register operationalizes, but does not replace, the existing global adjudication and Q-RM-08/Q-RM-09/Q-RM-10/Q-RM-11/Q-RM-12 contracts.

The global adjudication explicitly records that the universal semantics are closed while the concrete acquisition declaration, format binding, anomaly matrix, freeze persistence and executable implementations remain unresolved. The final gate therefore remains BLOCKED until those facts exist and are executed.

## FIN
