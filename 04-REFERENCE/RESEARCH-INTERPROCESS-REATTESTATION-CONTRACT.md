# RESEARCH INTER-PROCESS RE-ATTESTATION — TIER-A CONTRACT V1

**Contract ID:** `RESEARCH_INTERPROCESS_REATTESTATION_V1`  
**Boundary:** persisted research execution proof → fresh process-local `ResearchRunEvidence`  
**Tier:** `A`  
**Initial status:** `BLOCKED` until adversarial qualification

## 1. Purpose

P0.4 qualified only an in-process producer junction. Its attestation registry is intentionally process-local and disappears when the producer process exits.

P0.5 closes the smallest durable bridge required before RESEARCH and DECISION may execute in separate processes.

The bridge MUST NOT make a serialized `ResearchRunEvidence` authoritative merely because its fields or checksum look valid.

## 2. Selected minimal model

No asymmetric trust root, signing-key lifecycle or locked cryptographic dependency is currently qualified in this repository. Therefore P0.5 MUST NOT invent a bearer token or checksum-only signature and call it provenance.

The only admissible P0.5 model is **durable replay re-attestation**:

`qualified RESEARCH execution → content-addressed persisted proof → fresh process → source-byte revalidation → deterministic replay → exact claim comparison → fresh local ResearchRunEvidence attestation → ResearchFindings / DECISION`

The persisted proof is a replay recipe and immutable evidence record. It is **not itself downstream authority**.

A consumer process accepts it only by reproducing the qualified execution against source bytes whose identities match the proof and then minting a new process-local attestation through the already-qualified P0.4 factory.

## 3. Required persisted proof

The proof MUST carry, at minimum:

- exact schema and producer-contract identifiers;
- corpus SHA-256;
- instrument-contract SHA-256;
- execution claims: files, ticks, first/last timestamps and stream SHA-256;
- full `DatasetIdentity` fields;
- full `Context` fields;
- all `ResearchRunEvidence` identity fields;
- code version;
- canonical proof SHA-256.

The proof filename MUST be content-addressed by the canonical proof SHA-256. Renaming or modifying a proof without a matching content identity must fail closed.

The proof MUST contain no producer filesystem path as identity. A byte-identical corpus/contract relocated to another path must remain reproducible.

## 4. Producer requirements

A durable proof may be written only from:

- a `QualifiedResearchInput` whose current source hashes still match;
- a currently qualified `ResearchExecutionResult` bound to that exact input;
- a currently factory-attested `ResearchRunEvidence` produced from that execution;
- coherent Dataset and Context identities;
- a valid explicit 40-hex code version.

Report-only V4.3 evidence, manually reconstructed evidence, copied evidence or mutated evidence MUST NOT be persistable as a qualified inter-process proof.

Proof files are immutable/content-addressed. Reusing an existing path is allowed only when the existing canonical bytes are exactly identical.

## 5. Consumer requirements

The consumer MUST receive a trusted `expected_code_version` separately from the proof. The proof is not allowed to select the code version that authorizes itself.

To re-attest, the consumer MUST:

1. parse the proof using an exact schema; unknown/missing fields fail closed;
2. verify canonical proof hash and content-addressed filename;
3. require `proof.code_version == expected_code_version`;
4. receive local corpus and contract paths from outside the proof;
5. rebuild `QualifiedResearchInput` using proof hashes and those local paths;
6. revalidate corpus and contract bytes;
7. deterministically run `run_qualified_research()` in the consumer process;
8. compare every persisted execution claim with the fresh result;
9. reconstruct Dataset and Context objects from the proof and revalidate them against the derived runtime identity and replay result;
10. call the qualified P0.4 `from_research_execution(...)` factory in the consumer process;
11. require every resulting `ResearchRunEvidence` field to equal the persisted evidence claim;
12. return only that fresh locally-attested evidence (plus its coherent Context/Dataset when required).

No `trust_proof=True`, `skip_replay`, `accept_digest_only` or equivalent bypass is permitted.

## 6. Security / trust statement

P0.5 does **not** claim that a SHA-256 checksum proves who created a file. A caller capable of writing arbitrary JSON can also recompute a checksum.

P0.5 obtains authorization safety by making the durable record **non-authorizing until independently replayed** from content-addressed source bytes in the consumer process.

A future non-replay signed attestation may be designed only after an explicit trust-root/key-lifecycle/dependency decision. It is not silently implied by P0.5.

## 7. Required adversarial attacks

P0.5 must at minimum prove:

- `D0` positive producer → persisted proof → fresh-process replay → fresh attestation → DECISION path;
- `D1` directly deserialized/reconstructed `ResearchRunEvidence` remains unattested;
- `D2` evidence fields changed and proof digest recomputed are rejected by replay comparison;
- `D3` a different but valid-shaped 40-hex code version is rejected against trusted `expected_code_version`;
- `D4` execution claims changed and digest recomputed are rejected;
- `D5` Dataset fields changed and digest recomputed are rejected;
- `D6` Context fields changed and digest recomputed are rejected;
- `D7` corpus bytes substituted after persistence are rejected;
- `D8` instrument-contract bytes substituted after persistence are rejected;
- `D9` proof rename/content-address mismatch is rejected;
- `D10` unknown fields, missing fields or schema substitution are rejected;
- `D11` V4.3 report-only evidence cannot mint a qualified persisted proof;
- `D12` copied/reconstructed/mutated process-local evidence cannot mint a qualified persisted proof;
- `D13` identical corpus/contract bytes relocated to different filesystem paths can re-attest successfully;
- `D14` proof replay produces a new factory-attested object in the consumer process, while raw serialized fields remain non-authorizing;
- `D15` P0.2/P0.3/P0.4 regressions, blocked acquisition and no-real-backtest invariants survive P0.5.

Positive-path tests may use only deterministic synthetic local BI5 fixtures. No network access, real `.bi5` acquisition or real backtest is permitted.

## 8. Qualification rule

P0.5 may be PASS only after:

`formalisation → observed adversarial FAIL on pre-P0.5 state → minimal correction → D0–D15 re-break → P0.2/P0.3/P0.4 regressions → persisted-HEAD re-break → bounded JIT audit/report/checkpoint/backup → final documentary persisted-HEAD re-break`

A checksum-only green path or a same-process test is insufficient.

## 9. Explicitly outside P0.5

P0.5 does not authorize or close:

- non-replay cryptographic bearer attestation;
- signing-key generation, custody, rotation or revocation;
- dependency/environment lock for the whole repository;
- native `.bi5` acquisition;
- exact OOS split;
- real backtest;
- `DECISION → RISK → ACTION → RESULT → TRACE`;
- promotion/live activation;
- resilience/restoration beyond this one proof replay path.
