# B-PE-01R — EMPIRICAL EVIDENCE SUFFICIENCY / PROVIDER-PRIMARY SUPERSESSION REVIEW — CANDIDATE

**Date:** 2026-09-21  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Starting HEAD:** `a804afcfbf17c04a171a66484375727a5339e6cd`  
**Status:** PERSISTED CANDIDATE — NOT YET QUALIFIED  
**Scope:** governance/evidence-sufficiency review only. No new BI5 request, no exhaustive five-year qualification, no D materialization, no backtest.

---

## 0. Review question

Now that B-ERD-02 directly observed and independently decoded K1 on all nine bounded probes, determine whether a future:

```text
FULL_INTERVAL_QUALIFIED
```

direct empirical provider capture may satisfy the **operational** applicability burden protected by:

```text
C08-D4 — instrument applicability
C08-D5 — temporal/version continuity to target research epoch
```

without obtaining direct Dukascopy support correspondence.

Candidate decisions:

```text
KEEP_PROVIDER_PRIMARY
VERSIONED_EMPIRICAL_SUPERSESSION
BLOCKED
```

No exhaustive qualification may begin inside B-PE-01R.

---

## 1. Immutable historical boundary

B-PE-01 V0.1 remains historically valid and unchanged.

Its documentary rule remains:

```text
dimension PASS
→ at least one provider-primary EC-P1/P2 lineage
→ plus one distinct corroborating lineage
```

Therefore the original documentary dimensions remain exactly:

```text
C08-D4-DOC
C08-D5-DOC
```

and they do not become PASS merely because empirical K1 retrieval succeeds.

This review may create a **prospective successor evidence path**. It may not retroactively rewrite B-PE-01 V0.1 adjudications.

---

## 2. Why a second truth axis is necessary

C08-D4/D5 currently mix two materially different questions.

### Documentary question

```text
What does Dukascopy authoritatively state
about the historical applicability/version history
of the native hourly BI5 representation?
```

This requires provider-primary documentary evidence.

### Operational research question

```text
For the exact provider archive material used by this project,
does Dukascopy directly serve USATECHIDXUSD historical objects
over every manifest-relevant interval of the governed research domain,
and do those exact objects remain compatible with the already-qualified
representation semantics required by the decoder?
```

For historical backtesting using the provider archive as retrieved by the project, direct provider-origin empirical evidence can answer this second question more directly than support correspondence.

B-PE-04R already established that the current project objective is operational historical backtesting, not point-in-time forensic reconstruction of the provider infrastructure as it existed at each historical date.

---

## 3. Candidate prospective evidence class

Introduce only for a successor contract:

```text
EC-P3 — PROVIDER-DIRECT EMPIRICAL REPRESENTATION EVIDENCE
```

EC-P3 means:

```text
exact bytes / object dispositions
directly observed from a provider-bound delivery endpoint
under a presealed locator/transport policy,
with exact provenance, hashes and immutable capture evidence
```

EC-P3 is **not** provider normative documentation.

It may establish observed applicability/continuity of provider-served material.

It may not establish unstated semantic meaning such as:

- field roles;
- unit meaning;
- price scaling authority;
- volume economic meaning;
- historical provider policy;
- internal archive exhaustiveness against every possible provider store.

Therefore EC-P3 is not admissible as a replacement for the provider-primary burden of C01-C07.

---

## 4. New operational dimensions

A successor contract would define:

### C08-D4-OP — operational instrument applicability

Candidate proposition:

```text
For every manifest-relevant interval in FULL_D_REPRESENTATION_DOMAIN,
the selected provider representation rule is directly bound to
USATECHIDXUSD provider-served material, or to a separately qualified
explicit empty/absence state, without instrument inference.
```

### C08-D5-OP — operational archive continuity

Candidate proposition:

```text
At the sealed qualification retrieval epoch, every manifest-relevant
interval in FULL_D_REPRESENTATION_DOMAIN is deterministically assigned
to a qualified provider-served representation regime, with no
unclassified gap, unresolved transport state, silent format transition,
or sample extrapolation.
```

Important limitation:

```text
C08-D5-OP
does NOT mean
"Dukascopy historically served the same representation continuously
at the contemporaneous historical time."
```

It means only that the provider archive snapshot qualified for this project covers the market-date domain under a fully classified representation rule.

---

## 5. FULL_D_REPRESENTATION_DOMAIN

The domain remains exactly the B-ERD-01 qualified domain:

```text
mandatory deterministic 20-H1 warmup prefix
+
frozen evaluation interval
```

The component universe must be generated from:

- frozen execution-window identity;
- current-authority governed session-calendar identity;
- explicit instrument identity;
- exact interval inclusion/exclusion rule.

No hand-selected interval list may substitute for the governed universe.

A sealed interval-inventory root must bind the complete ordered set of manifest-relevant intervals before the first provider request.

---

## 6. FULL_INTERVAL_QUALIFIED — candidate successor meaning

A future empirical package may receive:

```text
FULL_INTERVAL_QUALIFIED
```

only if **every** condition below is satisfied.

### FI-E1 — provider-origin binding

Every provider request must derive from a presealed LocatorManifest whose source lineage binds the locator family to Dukascopy.

Redirect chains must remain inside a predeclared provider-delivery identity set or become BLOCKED.

No search-discovered/adaptive locator may be inserted after results are visible.

### FI-E2 — exact instrument binding

Every requested component must bind exactly:

```text
USATECHIDXUSD
```

No generic-index or symbol-family inference can satisfy C08-D4-OP.

### FI-E3 — complete interval inventory

Before requests:

```text
IntervalInventory =
all manifest-relevant intervals
across FULL_D_REPRESENTATION_DOMAIN
```

must be sealed.

The inventory must expose:

- total interval count;
- first/last interval;
- calendar identity;
- execution-window identity;
- warmup identity;
- deterministic ordered interval IDs;
- root digest.

No interval may be added/removed after observation.

### FI-E4 — one closed disposition for every interval

Every interval must end in exactly one qualified representation disposition.

Allowed successful forms:

```text
QUALIFIED_OBJECT
QUALIFIED_EMPTY
QUALIFIED_TRANSITION_REGIME_OBJECT
```

Disallowed unresolved forms:

```text
NOT_OBSERVED
TRANSPORT_BLOCKED
LOCATOR_BLOCKED
UNKNOWN_REPRESENTATION
UNCLASSIFIED_FORMAT
AMBIGUOUS_REGIME
```

Any unresolved form means:

```text
FULL_INTERVAL_QUALIFIED = NO
```

### FI-E5 — empty/absence is never inferred from transport

HTTP 404, zero bytes, timeout or failed retrieval cannot silently become a valid empty market interval.

`QUALIFIED_EMPTY` requires a separately qualified empty-object/no-tick rule applicable to the exact representation regime.

Otherwise the interval remains BLOCKED.

### FI-E6 — exact provider capture

For every obtained provider object:

- requested locator;
- request policy identity;
- retrieval time;
- HTTP status;
- response headers;
- exact compressed byte length;
- exact compressed SHA-256;
- provider delivery identity;
- content metadata when present;
- immutable capture seal

must be persisted.

### FI-E7 — independent representation compatibility diagnostics

Every non-empty candidate payload used for the operational rule must be processed by at least two independent diagnostic paths meeting B-ERD-01 independence constraints.

Agreement may establish only:

```text
REPRESENTATION_COMPATIBLE_WITH_QUALIFIED_SEMANTICS
```

It does not independently prove the semantic meaning of C01-C07.

Any diagnostic disagreement or unclassified payload blocks the affected interval.

### FI-E8 — no semantic self-bootstrapping

The empirical path may use only representation semantics that are already current-authority qualified under the applicable C01-C07 evidence contract.

Therefore:

```text
EC-P3 observed compatibility
cannot bootstrap C01-C07 provider truth
```

For downstream executable use, all physical semantic claims consumed by B must independently satisfy their own current-authority rules.

### FI-E9 — transition handling

If more than one representation regime is observed:

- exact deterministic boundary/rule must be established;
- regimes must be non-overlapping or coexistence semantics explicitly qualified;
- every interval must map to exactly one admissible acquisition rule;
- no nearest-format fallback;
- no sample-inferred transition instant.

Otherwise C08-D5-OP remains BLOCKED.

### FI-E10 — positive contradiction handling

The successor path does not require proving that no other Dukascopy representation exists.

However, any **positively observed** same-scope provider evidence that materially contradicts the selected representation's operational adequacy creates:

```text
BLOCKED — COMPETING_PROVIDER_REPRESENTATION_UNRESOLVED
```

until the relationship is adjudicated.

Mere coexistence is not a contradiction.

### FI-E11 — sealed archive snapshot identity

The complete qualification package must create a dataset-level identity over the ordered component inventory, including:

```text
interval_id
representation_regime_id
disposition
raw_sha256 or qualified-empty identity
capture_seal
diagnostic seals
```

The ordered canonical inventory yields:

```text
qualification_snapshot_root_sha256
```

This identifies the exact provider archive snapshot qualified by the project.

### FI-E12 — D must use the qualified snapshot

Operational supersession is valid for downstream D only if D:

1. consumes the exact qualified bytes; or
2. re-retrieves components and proves exact raw-hash equality to the qualified snapshot.

If a same-locator object later differs:

```text
ARCHIVE_MUTATION_DETECTED
→ reopen operational applicability
→ no silent substitution
```

Thus the empirical claim is snapshot-bound, not a perpetual claim about mutable provider archives.

### FI-E13 — durable evidence

Exact evidence must remain auditable after workflow/artifact expiry.

Compressed bodies may live outside Git only if storage is:

- durable;
- content-addressed;
- access-controlled as required;
- bound by hashes into the repository evidence root;
- recoverable for persisted-head audit.

A transient workflow artifact alone is insufficient.

### FI-E14 — no adaptive repair

During qualification:

- no failed K1 interval may be silently replaced with K2;
- no alternative URL may be discovered after the failing result and inserted into the same sealed execution;
- no parser/scaling rule may be changed in-place.

Any change requires a new versioned qualification lineage.

---

## 7. Successor C08 operational verdict

A new claim identity is required:

```text
BPE-C08-OP-V0_2
```

It does not overwrite `BPE-C08` V0.1.

Candidate PASS:

```text
C08-D1 current-authority PASS
AND C08-D2 current-authority PASS
AND C08-D3 current-authority PASS
AND C08-D4-OP PASS
AND C08-D5-OP PASS
AND no OPEN empirical reopen event
AND no unresolved same-scope material contradiction
```

The original documentary states may simultaneously remain:

```text
C08-D4-DOC = BLOCKED
C08-D5-DOC = BLOCKED
BPE-C08 V0.1 documentary = BLOCKED
```

No contradiction exists because the claims answer different questions.

---

## 8. Downstream gate supersession rule

The candidate prospective rule is:

```text
For the operational historical-backtest pipeline only:

C08 requirement may be satisfied by either:

A. BPE-C08 V0.1 documentary PASS

OR

B. BPE-C08-OP-V0.2 PASS
```

This alternative is permitted only if the pipeline objective remains:

```text
governed historical backtesting using the exact provider archive snapshot
qualified and consumed by the project
```

It is not permitted for claims about:

- what Dukascopy historically served contemporaneously;
- official historical format/version policy;
- regulatory/audit assertions requiring provider attestation;
- any future objective explicitly requiring point-in-time archival fidelity.

Those still require the documentary path.

---

## 9. Relationship to C01-C07

This supersession is narrow.

It does not alter B-PE-01 V0.1 sufficiency for:

```text
C01 compression/envelope semantics
C02 framing
C03 primitive field layout
C04 timestamp meaning
C05 ask/bid roles
C06 USATECH price scaling
C07 volume representation
```

Therefore a future `BPE-C08-OP-V0.2 PASS` cannot alone make global B PASS.

All other B mandatory claims/gates must independently be current-authority PASS.

---

## 10. Relationship to D completeness

`FULL_INTERVAL_QUALIFIED` proves complete empirical **representation applicability classification** over the sealed interval inventory.

It is not automatically:

```text
D MATERIALIZED
Q PASS
F PASS
backtest authorized
```

A later D step must still prove its own:

- component materialization;
- exact snapshot binding;
- completeness;
- anomaly accounting;
- downstream qualification.

The qualification capture may later be reused by D if D explicitly adopts those exact qualified bytes and identities.

---

## 11. Provider retroactive mutation

A later provider archive mutation does not retroactively make a completed backtest lie about the bytes it actually used.

Instead:

```text
old qualification snapshot
→ remains historical evidence of old exact bytes

new differing provider bytes
→ create ArchiveMutationEvent
→ current-authority operational qualification opens
→ any new D/backtest promotion requires requalification
```

The project must never claim that a past snapshot describes the provider forever.

---

## 12. Current B-ERD-02 evidence status

Existing bounded evidence:

~~~text
B-ERD-02 = PROBE_SUPPORTED
K1 = 9/9 supported
~~~

is materially useful because it demonstrates feasibility and falsifies the claim that K1 is merely a hypothetical legacy locator.

But:

```text
B-ERD-02
≠
FULL_INTERVAL_QUALIFIED
```

and therefore it cannot satisfy C08-D4-OP/D5-OP by itself.

---

## 13. Candidate decision

```text
B-PE-01R CANDIDATE DECISION =
VERSIONED_EMPIRICAL_SUPERSESSION
```

Meaning:

- retain B-PE-01 V0.1 documentary provider-primary rule;
- introduce EC-P3 and BPE-C08-OP-V0.2 prospectively;
- allow exhaustive, exact, provider-direct empirical evidence to satisfy only the operational C08-D4/D5 burden;
- never use sampling as full continuity;
- never use EC-P3 to bootstrap C01-C07 semantics;
- bind downstream D to the exact qualified snapshot;
- reopen on archive mutation or contradiction.

---

## 14. Candidate next step if this review qualifies

Only after B-PE-01R PASS may the project formalize the smallest path to:

```text
FULL_INTERVAL_QUALIFIED
```

No such execution is authorized here.

Potential next governed block would be contract/formalization only, not the five-year download itself.

---

## 15. Candidate status

```text
B-PE-01R = PERSISTED CANDIDATE / ADVERSARIAL BREAK REQUIRED

no new BI5 request = YES
no exhaustive qualification = YES
D materialized = NO
backtest = NO
paper/broker/live = NO
```
