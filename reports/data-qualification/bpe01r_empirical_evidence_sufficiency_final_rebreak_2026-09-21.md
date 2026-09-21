# B-PE-01R — EMPIRICAL EVIDENCE SUFFICIENCY / PROVIDER-PRIMARY SUPERSESSION REVIEW — FINAL RE-BREAK

**Date:** 2026-09-21  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Persisted corrected-composite HEAD:** `b095e461bc94c4f9bd4712ad3b13333555d543b4`

Normative composite under re-break:

```text
parent candidate blob
0a9ed4c6bcb921910f287da4646d5870061b9a31

+
correction V0.2 blob
a0d873184d058e4c05c3108f6a2374bf2d4ce8de
```

Composite identity:

```text
B_PE_01R_OPERATIONAL_EMPIRICAL_SUPERSESSION_V0_2_CORRECTED
```

## 1. Review question

Determine whether direct provider empirical evidence can prospectively replace the mandatory provider-primary **documentary** burden for the operational problem protected by:

```text
C08-D4 — instrument applicability
C08-D5 — temporal/version applicability to target research epoch
```

without silently rewriting B-PE-01 V0.1.

## 2. Documentary vs operational truth

The re-break confirms that two different claims must remain separate.

### Documentary axis

```text
C08-D4-DOC
C08-D5-DOC
```

These answer what Dukascopy authoritatively states about historical representation scope/version policy.

They continue to require the B-PE-01 V0.1 provider-primary rule.

### Operational axis

```text
C08-D4-OP
C08-D5-OP
BPE-C08-OP-V0.2
```

These answer whether the exact provider archive material selected for the governed historical backtest is empirically bound to USATECHIDXUSD and fully classified across the complete research representation domain.

The operational axis may use:

```text
EC-P3 — PROVIDER-DIRECT EMPIRICAL REPRESENTATION EVIDENCE
```

under the successor rules.

The two axes are not interchangeable.

## 3. Adversarial attack matrix

### A1 — bounded sample extrapolation

Attack:

```text
B-ERD-02 9/9 supported
→ claim five-year continuity
```

Rejected.

```text
PROBE_SUPPORTED
!=
FULL_INTERVAL_QUALIFIED
```

remains hard.

Every manifest-relevant interval across the complete warmup + evaluation domain must be accounted for.

### A2 — false empirical equivalence

Attack:

Two project decoders agree and are used to manufacture provider truth about compression, field roles, scaling or volumes.

Rejected.

EC-P3 can establish direct provider-object applicability/compatibility only.

It cannot bootstrap C01-C07.

Every applicable C01-C07 adjudication referenced by the operational scope tuple must already be current authority.

### A3 — common-premise agreement

Attack:

Two independent parsers share one wrong semantic premise.

Rejected as a route to semantic truth.

The independent diagnostics establish:

```text
REPRESENTATION_COMPATIBLE_WITH_QUALIFIED_SEMANTICS
```

only.

Normative semantics remain externally qualified under C01-C07.

### A4 — interval inventory omission

Attack:

A five-year "full" qualification silently omits intervals because the manifest is hand-selected.

Rejected.

The interval universe must be sealed before requests and derived from:

- frozen execution window;
- mandatory warmup;
- current-authority session calendar;
- exact instrument;
- deterministic inclusion/exclusion rule.

The interval inventory root is part of the authority scope tuple.

### A5 — market absence / transport failure converted to continuity

Attack:

404, timeout, zero bytes or auth failure becomes a valid empty interval.

Rejected.

`QUALIFIED_EMPTY` requires a separately qualified empty/no-tick rule.

All unresolved transport/locator/unknown states prevent FULL_INTERVAL_QUALIFIED.

### A6 — hidden regime transition

Attack:

K1 works before and after a transition but semantics/regime changes in between.

Rejected.

Every manifest-relevant interval must be classified.

Any multi-regime path requires exact deterministic complete regime boundaries; no sampled transition instant is allowed.

### A7 — representation aliasing / coexistence

Attack:

Existence of another provider representation is treated either as automatic refutation or silently ignored when material divergence is observed.

Rejected.

Mere coexistence is not a contradiction.

But any positively observed same-scope material contradiction creates:

```text
BLOCKED — COMPETING_PROVIDER_REPRESENTATION_UNRESOLVED
```

until adjudicated.

The successor claim deliberately does **not** assert that no richer/unobserved provider representation exists.

Its scope is the operational adequacy of the exact selected provider representation/capture set for this governed research pipeline.

If the project later requires proof of provider-canonical exhaustiveness across all internal/provider stores, BPE-C08-OP-V0.2 is insufficient.

### A8 — sequential capture misrepresented as atomic provider snapshot

Closed by BPE01R-F01 correction.

The authoritative identity is:

```text
qualification_capture_set_root_sha256
```

with per-object retrieval timestamps.

No provider-atomic snapshot claim is permitted.

### A9 — provider archive retroactive mutation

Attack:

qualification PASS is reused after same-locator bytes change.

Rejected.

Differing bytes create:

```text
ARCHIVE_MUTATION_DETECTED
→ OPEN OperationalEvidenceReopenEvent
```

Old bytes remain historical evidence of what was actually used, but old PASS loses current promotion authority.

### A10 — stale operational PASS reuse

Closed by BPE01R-F02 correction.

A PASS is current authority only if:

- exact successor contract/version matches;
- exact authority scope tuple matches;
- exact capture-set root matches;
- no superseding adjudication exists;
- no OPEN reopen event exists;
- all referenced C01-C07 adjudications remain current authority;
- evidence integrity re-verifies.

### A11 — cross-scope reuse

Closed by BPE01R-F03 correction.

The immutable authority scope tuple pins:

- provider;
- instrument;
- representation rule;
- full-D domain;
- execution-window freeze;
- warmup;
- session calendar;
- interval inventory;
- delivery identity policy;
- locator/transport identities;
- applicable C01-C07 adjudications;
- qualified-empty rule when used;
- capture-set root;
- successor contract/version.

Any tuple change requires a new adjudication.

### A12 — adaptive repair after failures

Rejected.

No same-lineage substitution of K2, alternate URL, parser or scaling rule is allowed after results are visible.

A change requires a new qualification lineage/version.

### A13 — silent weakening of B-PE-01

Rejected.

B-PE-01 V0.1 remains authoritative for its original documentary claim identities.

The successor creates new operational claim identities instead of mutating historical PASS/BLOCKED semantics.

### A14 — point-in-time historical infrastructure claim

Attack:

sequential current retrieval is used to claim exact provider infrastructure state as it existed in 2022/2023/etc.

Rejected.

The successor path proves only the provider archive capture set qualified for the project.

If point-in-time archival fidelity or provider-atomic historical state becomes a requirement, the operational supersession path is insufficient unless separately qualified.

## 4. Initial defects and closure

Initial adversarial break demonstrated:

```text
BPE01R-F01 — SEQUENTIAL_CAPTURE_ROOT_OVERCLAIMED_AS_PROVIDER_ARCHIVE_SNAPSHOT
BPE01R-F02 — SUCCESSOR CURRENT-AUTHORITY / REOPEN PREDICATE NOT CLOSED
BPE01R-F03 — DOWNSTREAM AUTHORITY SCOPE TUPLE NOT NORMATIVELY PINNED
```

All three are closed by correction blob:

`a0d873184d058e4c05c3108f6a2374bf2d4ce8de`

No new defect was demonstrated in the corrected composite.

## 5. Final decision

```text
B-PE-01R =
PASS

DECISION =
VERSIONED_EMPIRICAL_SUPERSESSION
```

Meaning:

```text
B-PE-01 V0.1 documentary provider-primary rule
→ preserved

C08-D4-DOC / C08-D5-DOC
→ still require documentary provider-primary evidence

new BPE-C08-OP-V0.2
→ may satisfy the operational C08 prerequisite
   for the governed historical-backtest pipeline
   IF and only if FULL_INTERVAL_QUALIFIED
   and all successor current-authority conditions hold
```

## 6. Exact operational supersession rule

For the operational historical-backtest pipeline only:

```text
C08 prerequisite =
current-authority BPE-C08 V0.1 documentary PASS

OR

current-authority BPE-C08-OP-V0.2 PASS
with exact downstream authority_scope_tuple match
```

The operational alternative cannot be used for claims about:

- official historical Dukascopy policy;
- contemporaneous historical serving infrastructure;
- provider-atomic point-in-time state;
- regulatory/provider-attested format history;
- provider-canonical exhaustiveness across every possible internal representation.

## 7. What FULL_INTERVAL_QUALIFIED must mean prospectively

The future qualification must satisfy the parent FI-E1 through FI-E14 conditions plus the V0.2 corrections.

At minimum:

```text
complete presealed interval inventory
+
provider-bound exact locators
+
exact USATECHIDXUSD binding
+
closed disposition for every interval
+
no unresolved transport/locator/unknown state
+
separately qualified empty semantics where needed
+
exact response bytes/hashes/provenance
+
two independent compatibility diagnostics
+
current-authority C01-C07 semantics
+
exact complete transition rules if multiple regimes
+
positive contradiction fail-closed
+
qualification_capture_set_root_sha256
+
D exact-byte/hash binding
+
durable evidence
+
no adaptive repair
+
closed current-authority/reopen/supersession state
+
exact authority scope tuple
```

## 8. Current B-ERD-02 status under the new rule

Existing evidence remains:

```text
B-ERD-02 = PROBE_SUPPORTED
K1 = SUPPORTED 9/9
```

This proves feasibility and materially supports the chosen direction.

But it still does not satisfy the new successor requirement:

```text
B-ERD-02
!=
FULL_INTERVAL_QUALIFIED

C08-D4-OP = NOT YET PASS
C08-D5-OP = NOT YET PASS
BPE-C08-OP-V0.2 = NOT YET PASS
```

## 9. Current global gate state

Unchanged:

```text
C08-D4-DOC = BLOCKED
C08-D5-DOC = BLOCKED
BPE-C08 V0.1 documentary = BLOCKED

BPE-C08-OP-V0.2 = NOT YET QUALIFIED

B global executable gate = BLOCKED
FINAL EXECUTABLE DATA GATE = BLOCKED

full acquisition = NO
D materialization = NO
backtest = NO
paper/broker/live = NO
```

## 10. Exactly one next governed action

Open only:

```text
B-FIQ-01 —
FULL_INTERVAL_QUALIFIED empirical representation-qualification contract
```

Formalization only.

Required scope:

```text
fresh HEAD
→ read B-PE-01R PASS
→ define exact FULL_D_REPRESENTATION_DOMAIN inventory construction
→ define presealed IntervalInventory + root
→ define provider-delivery / LocatorManifest rules
→ define transport and request-volume constraints
→ define every-interval disposition state machine
→ define QUALIFIED_EMPTY rule boundary
→ define dual independent diagnostics at full-interval scale
→ define transition-regime handling
→ define qualification_capture_set_root
→ define durable evidence storage/binding
→ define OperationalApplicabilityAdjudication
→ define reopen/supersession/current-authority predicates
→ define exact authority_scope_tuple
→ define PASS / FAIL / BLOCKED

→ adversarial break
→ minimal corrections only
→ persisted-head final re-break
→ audit + backup + checkpoint
→ STOP
```

Still prohibited inside B-FIQ-01:

```text
new full-domain BI5 download
exhaustive five-year qualification execution
D materialization
real Q/F/Q-RM-12 full execution
backtest
paper/broker/live
```

The eventual full-interval execution will require a separate explicit authorization.

## 11. Final verdict

```text
B-PE-01R EMPIRICAL EVIDENCE SUFFICIENCY /
PROVIDER-PRIMARY SUPERSESSION REVIEW = PASS

VERSIONED_EMPIRICAL_SUPERSESSION = QUALIFIED
```

STOP.
