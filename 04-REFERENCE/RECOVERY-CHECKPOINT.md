# RECOVERY CHECKPOINT — 17 SEPTEMBRE 2026 — P1.4 CLOSED / P1.5 TEST-FIRST RED

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Active branch: `integration/system-v1`

## 1. Source of truth

For tomorrow's recovery, use this hierarchy:

1. current GitHub branch state;
2. `04-REFERENCE/AI-OPERATING-MEMORY.md`;
3. this checkpoint;
4. newest applicable session backup;
5. executable workflow evidence / qualification reports;
6. conversation only as a last-resort convenience.

Do not reconstruct governed state from conversational memory.

Construction rule:

**UNDERSTAND → COMPARE → BREAK → DECIDE**

Qualification sequence:

**formalisation → candidate → adversarial break → correction → re-break → verdict**

Allowed verdicts: `PASS / FAIL / BLOCKED`. `BLOCKED` is never `PASS`.

Historical versions of this checkpoint remain available in Git history and earlier `99-BACKUP/` session snapshots. The present file intentionally replaces the previously accumulated P1.0/P1.1 historical wording with the current recovery state.

---

## 2. Mandatory end-of-day backup

Current complete session snapshot:

`99-BACKUP/SESSION-2026-09-17-END-OF-DAY-P1.2-P1.5-MEMORY-BOUNDARIES.md`

Backup creation commit:

`31be335aeace3f303c092323c589151856204005`

That backup contains the detailed path traversed today, all relevant commits/runs, real FAILs, corrections, adjudications and semantic decisions from P1.2 through the current P1.5 test-first boundary.

Read it before modifying P1.5 tomorrow.

---

## 3. Exact execution / breaker anchor before documentary save

The last non-documentary implementation/breaker HEAD before this EOD backup/checkpoint sequence is:

`6a0d33ac08f4825d554ad1d87805b64017b9720f`

Commit message:

`ci: add P1.5 durable memory preimplementation breaker`

This HEAD contains:

- all qualified P1.2/P1.3/P1.4 runtime/test state reached today;
- P1.5 contract/trust-model selection;
- P1.5 pre-implementation breaker;
- P1.5 workflow;
- **no** `src/memory_interprocess.py` runtime candidate.

Documentary descendants created after this anchor must not be mistaken for a new runtime qualification state.

Before any substantive mutation tomorrow, verify the real branch HEAD and compare it with:

- execution/breaker anchor `6a0d33ac08f4825d554ad1d87805b64017b9720f`;
- backup commit `31be335aeace3f303c092323c589151856204005`;
- the commit containing this checkpoint.

No blind merge, rebase, reset, force-push or history replay is authorized.

---

## 4. Protected reproducibility / safety baseline

P0.6 remains the qualified reproducibility baseline:

`8061127c148f06454dac6e7977a8d0cb921276f8`

Qualified environment remains:

- CPython `3.12.14`;
- `ubuntu-24.04`;
- checkout action `11d5960a326750d5838078e36cf38b85af677262`;
- setup-python action `a26af69be951a213d495a4c3e4e4022e16d87065`;
- `PYTHONDONTWRITEBYTECODE=1`;
- `PYTHONHASHSEED=0`;
- `TZ=UTC`;
- `LANG=C.UTF-8`;
- `LC_ALL=C.UTF-8`;
- exact packages from `requirements/qualification.lock.txt`.

Safety truth remains unchanged:

- global unresolved historical coverage remains BLOCKED where previously qualified;
- acquisition remains BLOCKED;
- `massive_acquisition_authorized = false`;
- `real_backtest_authorized = false`;
- no native `.bi5` acquisition is authorized;
- no real-data backtest is authorized;
- live activation is unauthorized.

P1.1 remains block-only. No positive `AUTHORIZED` path exists.

---

## 5. Current verdict matrix

- P0.2: **PASS / protected baseline**
- P0.3: **PASS / protected baseline**
- P0.4: **PASS / protected baseline**
- P0.5: **PASS / protected baseline**
- P0.6: **PASS / protected reproducibility envelope**
- P1.0: **qualified fail-closed promotion boundary; no permissive path opened**
- P1.1: **PASS block-only; positive authorization remains BLOCKED**
- P1.2 ACTION → RESULT: **PASS — qualification-only**
- P1.3 RESULT → TRACE: **PASS — qualification-only**
- P1.4 TRACE → MEMORY EPISODE: **PASS — qualification-only**
- P1.5 durable MEMORY contract formalization: **PASS**
- P1.5 trust-model comparison/selection: **PASS**
- P1.5 executable runtime: **BLOCKED / not implemented**
- P1.5 first breaker: **real expected FAIL observed**

No positive operational authorization was created today.

---

## 6. P1.2 — ACTION → RESULT state

Contract:

`P1_2_ACTION_RESULT_EVIDENCE_BOUNDARY_V1`

Runtime:

`src/action_result_evidence.py`

Core types:

- `QualificationActionEvidence(action_id, decision_id, behavior)`;
- `QualificationResultObservation(result_id, action_id, outcome)`.

Important semantic rules:

- ACTION is actual engaged behavior, not necessarily an order;
- controlled no-action can be an Action;
- RESULT is an actual observation tied to exact Action;
- RESULT does not prove causality or Decision correctness;
- IDs/same-valued reconstruction are not authority.

Final persisted-head evidence:

- HEAD `8a36198fce100fb41275c778a405a3100e209aab`;
- run `35245152286`, attempt 2;
- job `105283562009`;
- RESEARCH→DECISION `16/16 PASS`;
- P1.2 `60/60 PASS`;
- clean worktree.

Verdict:

**P1.2 PASS — qualification-only.**

---

## 7. P1.3 — RESULT → TRACE state

Contract:

`P1_3_RESULT_TRACE_EVIDENCE_BOUNDARY_V1`

Runtime:

`src/decision_trace.py`

Qualified chain:

`exact ResearchRunEvidence → exact Decision → exact ActionEvidence → exact ResultObservation → factory-attested DecisionTrace`

Important facts:

- `DecisionTrace.validate()` is structural only;
- same-valued/manual Trace is not automatically attested;
- exact ResearchRunEvidence provenance is privately bound to Decision;
- Trace remains a downstream snapshot and cannot mint/repair upstream objects;
- Trace can survive upstream GC, but it does not contain `behavior`/`outcome`.

Correction commit for exact research provenance:

`16ecbcaab3bfc477f2a7de6c2a5d3a7f75adaf94`

Second breaker / closure commit:

`a1f5b86c74e64ee128753afdcc66d150dd7c645c`

Final run:

- run `35246726515`;
- attempt 2;
- job `105289153528`;
- RESEARCH→DECISION `16 PASS`;
- P1.2 `60 PASS`;
- P1.3 `41 PASS`.

Verdict:

**P1.3 PASS — qualification-only.**

---

## 8. P1.4 — TRACE → MEMORY EPISODE state

Contract:

`P1_4_TRACE_MEMORY_EPISODE_BOUNDARY_V1`

Formalization commit:

`da3361a41dada47114cafa518a48412afa1b39a8`

Runtime candidate commit:

`ec3487ea3ed74c374a273466bfac977d3553b166`

Runtime:

`src/memory_episode.py`

Minimal input:

`exact attested DecisionTrace + exact admissible QualificationActionEvidence + exact admissible QualificationResultObservation → ObservationalMemoryEpisode`

Four required separations:

`EVENT ≠ EXPERIENCE`

`OBSERVATION ≠ INTERPRETATION`

`EXPERIENCE ≠ KNOWLEDGE`

`KNOWLEDGE ≠ OPERATIONAL AUTHORIZATION`

P1.4 does not accept `ResearchFindings` as an authority/input yet.

It preserves factual observation only:

- Trace projection/provenance;
- exact Action `behavior`;
- exact Result `outcome`.

It does not qualify:

- hypothesis;
- causal relation;
- Decision correctness;
- confidence;
- `SUPPORTED/REFUTED/NOT_INTERPRETABLE`;
- knowledge;
- operational permission.

### First breaker

Commit:

`f7278000cdbd5d427db8a9b67d3698f98a5466bd`

Run:

`35263365734 / job 105344333468`

Result:

- RESEARCH→DECISION `16/16 PASS`;
- P1.2 `60/60 PASS`;
- P1.3 `41/41 PASS`;
- P1.4 A0–G4 `49/49 PASS`.

No fake correction was created because the first breaker was genuinely green.

### Second breaker — genuine H8 defect

Breaker commit:

`68301d80163a24511e880f856c07ed9e4d646013`

Real defect:

After a P1.2 lifecycle/registry reset, a newly authentic Action/Result pair could collide on the same IDs as an older pair and be recombined with an old Trace.

Key invariant learned:

`same IDs + both authentic ≠ same historical pair`

Minimal correction commit:

`4d1622055f141208e34d717024f2b882934d91a3`

P1.3 now retains private exact historical Action/Result provenance for downstream verification while preserving Trace survival after GC.

### CI/test-isolation corrections discovered during closure

P0.2 stale evolving-document guard correction:

`03e1f8c48442568ef5cc0a717fde4714c8d4eef1`

H8 reload attack moved to subprocess to avoid polluting later pytest class/registry identity:

`64dcfa331736dc8624556a1ac160d56748dd5fab`

P0.4/P0.6 full-suite workflows were corrected to listen to `tests/**` because they run `pytest -q` over the whole repository.

### Final persisted-head P1.4 qualification

HEAD:

`12936ce44a1ba5dd3ac154fc62c62bf39a9997b5`

Evidence on that same SHA:

- P0.4 run `35265181355` — SUCCESS — full repository `452 passed`;
- P0.6 run `35265181428` — SUCCESS;
- P1.4 run `35265181318`, attempt 2, job `105350666230` — SUCCESS;
- RESEARCH→DECISION `16/16`;
- P1.2 `60/60`;
- P1.3 `41/41`;
- P1.4 A0–G4 `49/49`;
- second breaker H0–H8 `9/9`;
- worktree clean.

Verdict:

**P1.4 PASS — qualification-only.**

---

## 9. PRE-P1.5 — durable MEMORY discovery

The discovery was read-only.

Central conclusion:

P0.5 deterministic replay cannot be copied to historical MEMORY.

`REPLAY(ACTION → RESULT) ≠ PROOF(original ACTION → RESULT)`

Replaying an Action/Result creates a new event.

Therefore the required durable pattern is witness/capture re-attestation:

`P1.4-attested episode → canonical durable record → trusted capture/witness → receipt → fresh process + external trust expectation → verification → fresh local historical-memory re-attestation`

Key separations:

- durable record ≠ authority;
- content integrity ≠ provenance/authenticity;
- capture authority ≠ captured artifact;
- receipt ≠ historical event;
- content identity ≠ registration/occurrence identity;
- replay ≠ historical verification;
- fresh-process re-attestation ≠ original-object resurrection.

`episode_id` remains content identity, not globally unique historical occurrence identity.

Verdict:

**PRE-P1.5 discovery PASS.**

---

## 10. P1.5 contract formalization

Contract:

`P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1`

Formalization commit:

`3474e7dc3a6f422ae21b75dfccfbc4342d09b793`

Commit message:

`governance: formalize P1.5 durable memory re-attestation boundary`

Formalization location:

`GOVERNANCE/STEP-3-REAL-SYSTEM-MAPPING.md`

No signature/key/storage/service technology was selected at this point.

P1.5 preserved P0.5's reusable negative principles:

- serialization/hash is not authority;
- trust expectation must come from outside the artifact;
- unknown schema/substitution/missing trust fails closed;
- fresh process mints a new local attestation only after verification;
- no `accept_digest_only`, `trust_record=True`, `skip_verification` bypass.

But replay of the historical event is forbidden.

---

## 11. P1.5 selected trust model

Selected model:

`P1_5_EXTERNAL_RECEIPT_PIN_TRUST_MODEL_V1`

Selection commit:

`38595b56fcf1a7e9e53f29dd30d2802ab6e9be40`

Commit message:

`governance: select P1.5 external receipt pin trust model`

### External trust expectation

For each registration, the fresh verifier receives separately from the record/receipt bundle:

- `expected_contract`;
- `expected_authority_id`;
- `expected_receipt_sha256`.

The record/receipt cannot choose these expected values itself.

### Why this model was selected first

Rejected / deferred alternatives:

- hash/content-address only: integrity, not authority;
- self-declared `authority_id`: self-authorization;
- Git/GitHub path/commit as implicit trust: not qualified as capture authority;
- HMAC/shared secret: verifier also gains minting power;
- asymmetric signature: potentially valid but introduces signer isolation/key custody/rotation/revocation before needed;
- trusted append-only service: potentially valid but introduces a new persistent authority/service before needed.

The external per-registration receipt pin gives the verifier no minting secret and creates no service/PKI yet.

Tradeoff accepted: an external pin must be provisioned per registration. If this later becomes operationally unacceptable, that will be evidence for a broader signature/service model.

### Registration identity refinement

The breaker design established that `registration_id` must be bound to the registration content.

A capture nonce may distinguish registrations without claiming trusted wall-clock time.

Registration identity must not be interpreted as proof of independent experiment occurrence.

---

## 12. P1.5 pre-implementation breaker state

Breaker:

`breakers/p1_5_external_receipt_pin_breaker.py`

Breaker commit:

`e8ea512cbacf98d954c4d87316365733805d501b`

Workflow:

`.github/workflows/p1-5-durable-memory-reattestation.yml`

Workflow / execution anchor:

`6a0d33ac08f4825d554ad1d87805b64017b9720f`

At this anchor there is intentionally **no**:

`src/memory_interprocess.py`

### First P1.5 run

Run:

`35271832061`

Job:

`105372835362`

Conclusion:

**FAIL — expected pre-implementation red.**

Before the P1.5 breaker failed, the workflow proved:

- exact persisted HEAD / P0.6 ancestry: PASS;
- test-first condition / no runtime candidate: PASS;
- qualification environment: PASS;
- RESEARCH→DECISION: `16 passed`;
- P1.2: `60 passed`;
- P1.3: `41 passed`;
- P1.4 combined: `58 passed`;
- clean worktree: PASS.

P1.5 breaker result:

`37 failed`

Every failure is the same intentional baseline:

`P1.5 candidate absent — expected pre-implementation FAIL: src.memory_interprocess does not exist`

This is genuine red evidence. It is not a regression and must be preserved.

---

## 13. P1.5 breaker scope frozen before implementation

The breaker already covers:

### A — capture source

- exact P1.4 episode positive source;
- manual/same-valued/copy/deepcopy/replace/JSON/mutated source rejection.

### B — durable bundle integrity / non-self-authority

- record without receipt;
- receipt without record;
- internally coherent bundle without external pin;
- rehashed tamper against original external pin;
- storage path/location not authority.

### C — external trust expectation

- exact expected contract/authority/receipt digest;
- wrong receipt pin;
- wrong authority;
- wrong contract;
- bundle cannot supply its own expected trust values.

### D — fresh-process semantics

- fresh local historical-memory attestation;
- raw deserialized episode remains unattested;
- no Action/Result replay inputs;
- same-content new episode gets a new registration;
- fresh object is not original P1.4 object resurrected.

### E — registration / duplication

- registration identity distinct from content identity;
- same-content registrations are not independent experiments;
- physical bundle copy is not a new registration;
- registration identity is content-bound / rebinding fails closed;
- a pin for one registration cannot authorize another.

### F — time/look-ahead

- no caller-supplied trusted timestamp required;
- bundle timestamp is not part of minimal trusted receipt;
- registration ≠ `known_from`;
- receipt does not claim prior availability;
- local clock cannot silently repair missing qualified time.

### G — reverse authority / operational bypass

- historical memory cannot mint/repair upstream objects;
- historical memory is not ResearchRunEvidence/ResearchFindings;
- no knowledge status;
- no `AUTHORIZED`;
- no broker/order/sizing/acquisition/backtest/live surface.

Do not weaken or rewrite this breaker before the first runtime candidate unless a defect in the breaker itself is demonstrated.

---

## 14. Explicitly still BLOCKED / deferred

The following are not qualified by P1.5 selection/breaker:

- concrete storage backend;
- cryptographic signature/PKI;
- symmetric secret/HMAC;
- key custody, rotation, revocation, recovery;
- append-only network/service authority;
- trusted timestamping;
- global historical occurrence identity;
- `ResearchFindings` attachment;
- EXPERIENCE→KNOWLEDGE promotion;
- causal inference;
- confidence aggregation;
- memory exhaustiveness / survivorship-bias proof;
- AUDIT / REVISION;
- positive operational authorization.

Do not add these just because implementation begins.

---

## 15. Mandatory recovery order tomorrow

Read in this order:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this `04-REFERENCE/RECOVERY-CHECKPOINT.md`
3. `99-BACKUP/SESSION-2026-09-17-END-OF-DAY-P1.2-P1.5-MEMORY-BOUNDARIES.md`
4. `GOVERNANCE/STEP-3-REAL-SYSTEM-MAPPING.md`
5. `src/memory_episode.py`
6. `src/decision_trace.py`
7. `src/action_result_evidence.py`
8. `breakers/p1_5_external_receipt_pin_breaker.py`
9. `.github/workflows/p1-5-durable-memory-reattestation.yml`
10. `04-REFERENCE/RESEARCH-INTERPROCESS-REATTESTATION-CONTRACT.md`
11. `04-REFERENCE/QUALIFICATION-ENVIRONMENT-LOCK.json`
12. `requirements/qualification.lock.txt`
13. verify the current branch HEAD and compare it to `6a0d33ac08f4825d554ad1d87805b64017b9720f` plus the documentary descendants before writing runtime code.

If GitHub disagrees with this checkpoint, GitHub wins and the discrepancy must be diagnosed before mutation.

---

## 16. Do not repeat tomorrow

Do not redo PRE-P1.4 discovery without a relevant repository change.

Do not rerun the large Claude six-chunk audit protocol. Its useful findings were adjudicated and incorporated where supported by GitHub.

Do not move `ResearchFindings` into P1.4/P1.5 merely because it contains hypotheses/statuses.

Do not replace the selected external receipt pin model with signatures/HMAC/Git trust/service infrastructure without new evidence that the selected minimal model fails for a reason not already represented by the breaker.

Do not interpret run `35271832061` as a regression: it is the intended test-first red baseline.

Do not jump directly to persisted-head PASS after implementing the first candidate. Preserve real observed failures, correct minimally, second-break if warranted, then do a final persisted-head re-break.

---

## 17. Exactly one next governed action

**Implement the smallest possible `src/memory_interprocess.py` candidate satisfying only `P1_5_EXTERNAL_RECEIPT_PIN_TRUST_MODEL_V1`, without changing the existing breaker first; execute the P1.5 A0–G4 breaker, inspect the actual violations, and correct only defects demonstrated by that breaker.**

The first candidate is allowed only these responsibilities:

- accept capture only from exact currently P1.4-attested `ObservationalMemoryEpisode`;
- produce canonical durable record bytes;
- produce a canonical receipt bound to exact record and content-bound registration identity;
- use a capture nonce if needed for registration distinction, without claiming trusted time;
- verify in a fresh process using separately supplied `expected_contract`, `expected_authority_id`, `expected_receipt_sha256`;
- mint a fresh local historical-memory attestation after successful verification;
- never replay Action/Result as historical proof;
- never self-select its trust root;
- never promote to ResearchFindings, knowledge, authorization or operations.

---

## 18. End-of-day stop rule

Stop here for 17 September 2026.

Do not implement P1.5 after this checkpoint tonight.

Tomorrow resume from GitHub and the artifacts above, not from chat memory.
