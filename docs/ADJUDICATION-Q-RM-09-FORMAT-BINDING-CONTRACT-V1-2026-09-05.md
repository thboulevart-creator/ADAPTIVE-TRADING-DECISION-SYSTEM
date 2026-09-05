# ADJUDICATION — Q-RM-09 FORMAT-BINDING CONTRACT

**Date:** 5 septembre 2026  
**Status:** **CONTRACT SCHEMA = PASS; CONCRETE FORMAT BINDINGS = BLOCKED**  
**Depends on:** RB-A, Q-RM-01..08

## 1. QUESTION

What must a concrete format binding specify so that physical input has one deterministic normative interpretation?

Q-RM-06 already closed the universal policy: the binding is an explicit, immutable, versioned normative input and must define every representation-specific property capable of changing logical membership or interpretation.

## 2. [CONSÉQUENCE NÉCESSAIRE]

For each supported representation/version, the binding must uniquely determine:

```text
representation identity/version
record framing / boundaries
logical segmentation
physical → logical cardinality
non-observation classification
logical field mapping and units
occurrence individuation
malformed-input classes
ambiguous-input classes
failure scope / acquisition interaction
cross-component framing
qualification-relevant semantic dependencies
```

A parser/library default is never a substitute.

## 3. EXECUTABLE BINDING CONTRACT

A binding is eligible only if a conformance implementation can answer, for every declared physical unit:

```text
Where does the logical record begin/end?
How many primary occurrences does it produce?
Which material is non-observation?
What fields form the observation payload?
What makes two observations distinct occurrences?
What happens for invalid input?
What happens for ambiguous input?
Can a record cross physical components?
What evidence makes the interpretation deterministic?
```

If any answer is absent, contradictory, or implementation-dependent, the binding is not eligible for normative qualification.

## 4. VERSIONING GATE

A new binding version is mandatory when a semantic change can alter:

- boundaries;
- cardinality;
- occurrence individuation;
- field/payload interpretation;
- qualification membership;
- anomaly/failure scope.

A purely non-semantic implementation/library change does not require a new normative binding version if semantic equivalence is independently demonstrated.

## 5. ADVERSARIAL MATRIX

| Attack | Required result |
|---|---|
| Different parser libraries | Same logical result or implementation non-conformance |
| Same format name, different schema | Distinct explicit binding versions/IDs |
| Schema evolution affecting boundaries | New binding version |
| One object contains N observations | Binding explicitly yields N |
| Several objects form one record | Cross-component rule required |
| Missing delimiter | Q-RM-04 treatment; no parser repair |
| Encoding change | Binding must define whether semantics change |
| Compression/envelope change | Representation/binding semantics explicit |
| Missing binding version | No normative qualification |
| Unknown anomaly class | No silent fallback |
| Binding claims localisability without proof | Non-conforming binding |
| Parser silently repairs malformed data | Non-conforming implementation |

## 6. [CONTRACTUEL]

The project must inventory the actual supported representations and publish one binding artifact per representation/version. The repository evidence currently reviewed does not establish that concrete inventory.

The prior data contract explicitly says its version 0.1 is a proposal and non-validé, so it cannot be promoted implicitly into binding authority. fileciteturn21file0L2-L2

## 7. [ABSENCE DE PREUVE]

No validated repository evidence currently closes the concrete CSV/JSON/binary/etc binding matrix. Therefore this block cannot truthfully be marked fully executable for actual qualification.

## 8. VERDICT

```text
Q-RM-09 UNIVERSAL / CONTRACT COMPLETENESS RULE = PASS
Q-RM-09 CONCRETE FORMAT-BINDING INVENTORY = BLOCKED
```

No implementation-specific default is introduced.

## FIN
