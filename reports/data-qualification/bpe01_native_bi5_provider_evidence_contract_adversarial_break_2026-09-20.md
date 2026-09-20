# B-PE-01 — NATIVE BI5 PROVIDER EVIDENCE CONTRACT — ADVERSARIAL BREAK

**Date:** 2026-09-20  
**Candidate under attack:** `reports/data-qualification/bpe01_native_bi5_provider_evidence_contract_candidate_2026-09-20.md`  
**Candidate blob:** `d21ce35fe9acdcdc1b3b0828bb2525f75c15054a`  
**Candidate commit:** `9d2a7bbb5e42af5261e2881c050f9442b998c5cb`  
**Scope:** contract attack only. No provider evidence gathered. No BI5 downloaded or processed.

## 1. Attack objective

Attempt to obtain a false or under-justified C01-C08 PASS while formally satisfying the candidate rules.

The attack assumes an adversary may supply plausible-looking documentation metadata, mirrors, ports, broad provider pages, or incomplete technical references.

---

## 2. Demonstrated defects

### BPE-F01 — SINGLE_PROVIDER_ESCAPE_UNDERCUTS_INDEPENDENCE_REQUIREMENT

Attack:

Supply one provider-owned normative-looking page that explicitly states the desired claim, with no independent corroborating lineage.

Candidate Section 6 contains an exception:

`PASS_SINGLE_PROVIDER_NORMATIVE`.

Result:

The contract can waive the exact independence requirement it was created to enforce.

Why material:

The previous global reconciliation selected B-PE-01 precisely because project convergence is not external truth. A provider singleton can be authoritative, but the candidate currently lets it become final PASS without an independent check for mis-scoping, stale documentation, documentation defect, or symbol-family mismatch.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

No claim PASS in V0.1 from one evidentiary lineage alone. A provider-primary lineage remains mandatory, plus one genuinely distinct corroborating lineage. If only one provider lineage exists, verdict is BLOCKED, not degraded PASS.

---

### BPE-F02 — CLAIM_SUPPORT_CAN_BE_SELF_ASSERTED_WITHOUT_EXACT SOURCE ANCHOR

Attack:

Create an evidence record with:

```text
claim_ids_supported = [BPE-C03]
source_locator = large provider repository/document
content_integrity_digest = valid
```

but provide no exact section, path+symbol, line/range, commit-location or minimal proposition extracted from the source.

Result:

The evidence record can claim support for C03 while the pinned source merely exists somewhere.

Why material:

A digest proves bytes, not semantic entailment.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Separate source identity from claim mapping and require per-claim evidence anchors plus an adjudicator-authored support/contradiction proposition.

---

### BPE-F03 — LINEAGE_INDEPENDENCE_IS_SELF_ASSERTED

Attack:

Submit two articles/implementations that both derive their BI5 knowledge from the same upstream parser.

Give each a different:

`evidence_lineage_id`

and set:

`project_independence_status = INDEPENDENT`.

Result:

The candidate has no required proof/basis fields forcing lineage relationships to be justified.

Why material:

Two mirrors can be counted as two independent sources.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Independence must itself have auditable basis references. Unknown or unproven lineage independence must collapse sources into one lineage or BLOCK the independence count.

---

### BPE-F04 — TARGET PROVIDER SCOPE/VERSION BINDING IS NOT CONCRETE ENOUGH

Attack:

Use a current Dukascopy BI5 page for a different product/API epoch and map it to the project candidate version:

`DUKASCOPY_NATIVE_BI5_HOURLY_TICKS_V1_CANDIDATE`.

Result:

The evidence can be "version pinned" to its own source but there is no closed target-scope tuple against which applicability is judged.

Why material:

The project representation version is not a provider format version.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Define an explicit target representation scope signature distinct from source version, including provider, representation family, native hourly tick object family, instrument/symbol scope where needed, project R identity/version, and temporal applicability to the intended research epoch.

---

### BPE-F05 — C07 MIXES PROVIDER FACT WITH PROJECT DECODER BEHAVIOR

Attack:

Provide a source proving two binary32 volume fields, but no source describing project decoder scaling.

Candidate C07 includes:

`not implicitly price-scaled by the BI5 decoder`.

Result:

An external representation fact is mixed with implementation behavior.

Why material:

Provider evidence cannot prove what the project's decoder does; project code cannot be independent provider evidence.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Restate C07 only as a representation-level claim: encoded primitive, ask/bid role/order, provider-defined transform/scale if any. Project decoder conformance is checked later against the qualified claim.

---

### BPE-F06 — BROAD CLAIM CAN PASS WITH AN UNPROVEN REQUIRED DIMENSION

Attack:

For C02, provide two lineages proving only "20-byte records" but neither proving byte-zero frame origin or absence/presence of a record header.

Candidate Section 6 asks two lineages to support the "material semantics" but does not formally require every claim's listed proof dimension to receive its own sufficiency result.

Result:

A broad claim can be promoted while one mandatory dimension remains merely assumed.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Create mandatory dimension IDs under each C01-C08 claim. Claim PASS requires every mandatory dimension PASS; each dimension must meet the evidence sufficiency rule.

---

### BPE-F07 — NO CLOSED PERSISTED ADJUDICATION OUTPUT / EVIDENCE-SET BINDING

Attack:

Adjudicate C03 as PASS, then later add/remove evidence records without changing any formal claim-verdict artifact because the candidate defines verdict semantics but no immutable adjudication record schema.

Result:

The statement "C03 PASS" is not bound to an exact evidence set, contract version, lineage resolution, or claim dimensions.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Define a closed adjudication record containing exact evidence IDs/digests, evidence-set digest, lineage-resolution digest, dimension verdicts, claim verdicts, contract identity/version, target-scope signature, and adjudication seal.

---

### BPE-F08 — POST-PASS CONFLICT / SUPERSESSION SEMANTICS ARE INCOMPLETE

Attack:

A claim receives PASS. Later, admissible exact-scope evidence materially contradicts it.

The candidate says conflicts are BLOCKED during adjudication, but it does not define whether an already persisted PASS becomes stale/superseded or how downstream B must react.

Result:

A historical PASS can continue to be treated as current despite a newly admitted conflict.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Current claim status must be versioned against an exact evidence set. Any newly admitted material contradiction invalidates use of the prior PASS as current authority and requires a new adjudication; downstream promotion must pin an exact non-superseded adjudication.

---

## 3. Attacks that did NOT demonstrate defects

The following candidate properties resisted the break:

- project V4.3 / I_A / I_B are explicitly inadmissible as independent provider support;
- evidence age is correctly separated from scope staleness;
- generic forex evidence does not automatically satisfy USATECHIDXUSD C06;
- representation-wide evidence is separated from later D materialization;
- conflicts are not resolved by naive source-count voting;
- a real project BI5 sample is not required merely to formalize representation-wide provider facts;
- FAIL does not silently mutate B.

---

## 4. Initial verdict

Eight contract defects were demonstrated.

```text
B-PE-01 NATIVE BI5 PROVIDER-SENSITIVE PHYSICAL SEMANTICS
EVIDENCE CONTRACT CANDIDATE = FAIL
```

This FAIL is contract-local.

It does not change:

```text
B global gate = BLOCKED
Q-RM-12 compatibility chain = PASS
```

No provider evidence was gathered and no real data was touched.

## 5. Allowed correction scope

Correct only BPE-F01 through BPE-F08 in the persisted candidate.

Do not:

- gather evidence;
- decide C01-C08 truth;
- modify B/A/Q/F/O/I_A/I_B runtimes;
- download/process BI5;
- materialize D;
- backtest.
