# B-PE-01R — EMPIRICAL SUPERSESSION CANDIDATE — ADVERSARIAL BREAK

**Date:** 2026-09-21  
**Candidate HEAD:** `f178cf88b5bf5c54e58b373194817ad9ff092493`  
**Candidate blob:** `0a9ed4c6bcb921910f287da4646d5870061b9a31`

## 1. Attack objective

Attempt to obtain an apparently valid operational C08 supersession while:

- overstating what sequential provider retrieval proves;
- reusing a stale/superseded empirical PASS;
- applying a PASS to a different research domain or semantic contract;
- bootstrapping provider semantics from project decoders;
- extrapolating bounded probes;
- hiding regime changes or provider archive mutation.

## 2. Attacks survived

The candidate already resists:

### A1 — bounded sample promoted to full continuity

Rejected.

```text
B-ERD-02 PROBE_SUPPORTED
!=
FULL_INTERVAL_QUALIFIED
```

remains explicit.

### A2 — two project decoders bootstrap provider semantic truth

Rejected.

EC-P3 cannot prove C01-C07 and FI-E8 requires semantic claims to be independently current-authority qualified.

### A3 — one missing K1 object silently replaced with K2

Rejected by FI-E14.

### A4 — 404/zero-byte treated as valid no-tick interval

Rejected by FI-E5 unless a separately qualified empty-object rule exists.

### A5 — hidden transition inferred from sparse samples

Rejected.

Every manifest-relevant interval must be classified, and transitions require deterministic complete boundaries.

### A6 — provider archive mutates after qualification

The candidate detects differing re-retrieved hashes and requires reopening rather than silent substitution.

### A7 — K2 coexistence automatically invalidates K1

Correctly rejected.

Mere coexistence is not itself a contradiction; positive material divergence must be adjudicated.

### A8 — documentary historical claim silently rewritten

Rejected.

C08-D4/D5 documentary claims remain distinct and may remain BLOCKED.

## 3. Demonstrated defects

### BPE01R-F01 — SEQUENTIAL_CAPTURE_ROOT_OVERCLAIMED_AS_PROVIDER_ARCHIVE_SNAPSHOT

Candidate Section 6 / FI-E11 calls the qualification root a:

`qualification_snapshot_root_sha256`

and Section 11 describes an "old qualification snapshot."

Attack:

A five-year exhaustive qualification is necessarily retrieved sequentially.

Provider objects A and B may mutate between their retrieval times.

The resulting root is a perfectly valid identity of **what the project captured**, but it does not prove that all objects coexisted simultaneously in one atomic provider archive state.

Calling it a provider/archive snapshot silently adds an atomicity claim not established by the evidence.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Rename and define:

```text
qualification_capture_set_root_sha256
```

Semantics:

```text
identity of the exact ordered provider responses captured by the project,
with per-object retrieval timestamps;
NO provider-atomic-snapshot claim.
```

D may use those exact captured bytes.

If project requirements later demand a provider-atomic point-in-time snapshot, this empirical supersession path is insufficient unless such atomicity is separately established.

---

### BPE01R-F02 — SUCCESSOR CURRENT-AUTHORITY / REOPEN PREDICATE NOT CLOSED

Candidate creates `BPE-C08-OP-V0_2`, but does not define a closed successor adjudication/current-authority object equivalent to the protections B-PE-01 V0.1 already has.

Attack:

1. empirical package receives PASS;
2. a later ArchiveMutationEvent or contradiction occurs;
3. downstream B continues pinning the old PASS because the successor has no normative current-authority predicate.

Section 11 describes reopening conceptually but does not define the exact authoritative state machine.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Define sealed:

```text
OperationalApplicabilityAdjudication
OperationalEvidenceReopenEvent
OperationalAdjudicationSupersession
```

and the current-authority predicate:

```text
current_authority =
adjudication.verdict == PASS
AND exact successor contract/version matches
AND exact authority_scope_tuple matches
AND no later superseding adjudication
AND no OPEN reopen event
AND evidence/capture-set root matches
```

Any OPEN event makes historical PASS non-authoritative for new promotion.

---

### BPE01R-F03 — DOWNSTREAM AUTHORITY SCOPE TUPLE NOT NORMATIVELY PINNED

The candidate binds many scope components inside the qualification package, but the downstream alternative:

```text
BPE-C08 V0.1 PASS
OR
BPE-C08-OP-V0.2 PASS
```

does not normatively require exact equality between the PASS scope and the B/D target scope.

Attack:

A valid operational PASS for:

- one execution-window version;
- one warmup rule;
- one session calendar;
- one instrument identity;
- one set of qualified C01-C07 semantics;

is reused after one of those inputs changes.

The textual claim still says `BPE-C08-OP-V0.2 PASS`, but its evidentiary domain is stale.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Define immutable:

```text
authority_scope_tuple = {
  provider_identity,
  instrument_identity,
  representation_rule_identity,
  FULL_D_REPRESENTATION_DOMAIN identity,
  execution_window_freeze identity,
  warmup_rule identity,
  session_calendar identity,
  interval_inventory_root,
  applicable C01-C07 adjudication IDs/seals,
  qualification_capture_set_root,
  successor_contract_id/version
}
```

Downstream use requires exact tuple equality.

Any changed tuple component requires new adjudication; no inheritance.

## 4. Decision after break

No attack demonstrated that provider support correspondence is intrinsically necessary for the **operational** D4/D5 question once exhaustive provider-direct evidence is available.

The direction:

```text
VERSIONED_EMPIRICAL_SUPERSESSION
```

therefore remains viable.

But the current candidate is not qualified until F01-F03 are closed.

## 5. Break verdict

```text
B-PE-01R CANDIDATE = FAIL
```

Only BPE01R-F01 through F03 are authorized for correction.

No new provider request, exhaustive qualification, D materialization or backtest occurred.
