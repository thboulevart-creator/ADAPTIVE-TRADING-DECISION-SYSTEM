# CANONICAL ENUMERATION — NEXT PROPOSAL FOR COUNTER-EXPERTISE

## Status

**ASSISTANT PROPOSAL ONLY — NO DECISION TAKEN**

## 1. Current adjudicated constraint

The project has explicitly selected:

```text
OBSERVATION_IDENTITY
=
QUALIFIED_DATASET_DOMAIN
+
CANONICAL_RECORD_POSITION
```

The remaining question is how the qualification contract can define the canonical position without creating an artificial temporal order.

Grok's latest counter-expertise correctly rejected the previous assistant formulation as circular: saying that records are assigned positions according to a "deterministic canonical order defined by the qualification contract" does not yet state the criterion that determines that order.

## 2. Assistant's new answer BEFORE further counter-expertise

My current proposal is narrower than the previous one:

> The canonical position should be assigned from the **normatively enumerated sequence of logical primary records produced by the qualification contract from the declared acquisition input**, with the enumeration procedure itself explicitly specified as a deterministic function of the qualified input representation. The procedure must enumerate retained records exactly once, preserve distinct retained records as distinct positions, be independent of runtime traversal, and have no temporal semantics.

This proposal deliberately does NOT yet choose whether the enumeration criterion is:

- physical record appearance;
- provider sequence;
- byte offset;
- a source ordinal;
- a qualification-generated ordinal;
- a composite key;
- another mechanism.

## 3. Critical self-critique

I recognize that this may still be circular because "normatively enumerated sequence" and "deterministic function" may merely rename the missing function.

Therefore the next question is not yet "should we adopt this wording?" but:

> **Can the authoritative corpus constrain the concrete enumeration function any further, or is the choice of enumeration criterion necessarily a new human architecture decision?**

## 4. What must be tested

The counter-expert must attack the following candidate possibilities without selecting one implicitly:

### Candidate A — declared source/artifact appearance order

Records receive positions according to their order of appearance in the exact qualified acquisition representation after a declared deterministic parser.

Risk: this may depend on unresolved record boundaries, physical representation, multi-file order, or format semantics.

### Candidate B — source-provided sequence

Positions follow a source-provided ordinal/sequence if and only if a normative source guarantee exists.

Risk: current corpus may not prove such a guarantee.

### Candidate C — qualification-defined ordinal

Qualification itself constructs a deterministic enumeration and assigns positions once.

Risk: "qualification-defined" is not enough unless the construction rule is specified.

### Candidate D — deterministic composite sort key

Records are sorted by a declared tuple of fields sufficient to distinguish retained records.

Risk: strict duplicates cannot be separated by a content-only key; adding a physical/source tie-break may reintroduce unresolved choices.

### Candidate E — independent enumeration domains

If an acquisition contains multiple files/partitions, each declared domain may have its own local enumeration rather than a global ordinal.

Risk: the exact relationship between domain and identity remains constrained by the already selected `QUALIFIED_DATASET_DOMAIN` but must not be silently expanded.

## 5. Hard constraints for any surviving rule

Any rule must satisfy:

1. Every retained primary observation gets exactly one position.
2. Distinct retained observations get distinct positions.
3. Strict duplicates remain individually distinguishable.
4. Runtime traversal order cannot affect positions.
5. Parallelism cannot affect positions.
6. Restart cannot affect positions.
7. Downstream transformations cannot affect positions.
8. Position cannot establish temporal precedence.
9. Position cannot be used to construct or resolve `ordered_ticks`.
10. The rule must be reproducible by two conforming implementations over the same qualified input.
11. No inter-acquisition identity equivalence is implied.
12. No artifact hash, byte offset, filesystem order, source ID, format continuity, or global multi-file ordinal is assumed unless separately justified by the corpus or explicitly decided.

## 6. Required counter-expertise question

Determine whether the corpus permits the concrete enumeration criterion to be derived as a necessary consequence, or whether selecting the criterion requires a new explicit architecture decision.

If a new human decision is required, formulate exactly ONE decision question that does not presuppose the answer.

Do not modify `1.1.2`.
Do not modify H-04.
Do not create a new normative requirement.
Do not infer that a physically convenient mechanism is normatively required.
