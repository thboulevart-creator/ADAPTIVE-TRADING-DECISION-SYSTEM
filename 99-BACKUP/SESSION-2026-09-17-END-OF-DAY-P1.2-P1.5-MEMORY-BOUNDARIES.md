# SESSION BACKUP — 17 SEPTEMBRE 2026 — P1.2 → P1.5 MEMORY BOUNDARIES / END OF DAY

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`  
Implementation / breaker HEAD immediately before this backup: `6a0d33ac08f4825d554ad1d87805b64017b9720f`

## Purpose

This snapshot preserves the governed state reached on 17 September 2026 so the next session can resume without conversational reconstruction.

GitHub, versioned artifacts, workflow evidence, this backup and the current recovery checkpoint are the source of truth.

Method preserved:

`UNDERSTAND → COMPARE → BREAK → DECIDE`

Implementation sequence preserved:

`formalisation → candidate → adversarial break → correction → re-break → verdict`

Allowed verdicts: `PASS / FAIL / BLOCKED`.

No acquisition, real backtest, broker/exchange execution, order placement or live activation became authorized during this session.

---

# 1. State inherited before today's downstream work

The P0 reproducibility envelope remains governed by the existing locked environment:

- CPython `3.12.14`;
- `ubuntu-24.04`;
- checkout action `11d5960a326750d5838078e36cf38b85af677262`;
- setup-python action `a26af69be951a213d495a4c3e4e4022e16d87065`;
- `PYTHONDONTWRITEBYTECODE=1`;
- `PYTHONHASHSEED=0`;
- `TZ=UTC`;
- `LANG=C.UTF-8`;
- `LC_ALL=C.UTF-8`;
- qualification packages locked in `requirements/qualification.lock.txt`.

P1.1 remains block-only. No positive `AUTHORIZED` path was opened.

The persistent safety truth remains unchanged:

- global historical coverage remains BLOCKED where previously qualified as such;
- acquisition remains BLOCKED;
- `massive_acquisition_authorized = false`;
- `real_backtest_authorized = false`;
- live activation remains unauthorized.

---

# 2. P1.2 — ACTION → RESULT qualification-only

## Contract

`P1_2_ACTION_RESULT_EVIDENCE_BOUNDARY_V1`

Formalized in the existing surface:

`GOVERNANCE/STEP-3-REAL-SYSTEM-MAPPING.md`

No new governance document was created.

## Semantic result

ACTION means behavior actually engaged after a Decision, including controlled no-action, suspend, stop, reduce exposure or request information/experiment. It is not synonymous with broker order.

RESULT means an observation actually produced or collected after/about the exact Action. It does not itself establish causality, Decision correctness, knowledge validity or operational authorization.

## Runtime surface

`src/action_result_evidence.py`

Key types:

- `QualificationActionEvidence(action_id, decision_id, behavior)`;
- `QualificationResultObservation(result_id, action_id, outcome)`.

Key APIs:

- `engage_qualification_action(...)`;
- `observe_qualification_result(...)`;
- `verify_qualification_chain(...)`;
- later read-only hook added for P1.4: `verify_qualification_observation_pair(action, result)`.

Trust remains process-local and exact-object based; IDs or same-valued reconstruction are not authority.

## Final P1.2 qualification evidence

Persisted-head qualification anchor:

`8a36198fce100fb41275c778a405a3100e209aab`

Final rerun:

- workflow run `35245152286`;
- attempt `2`;
- job `105283562009`;
- upstream RESEARCH→DECISION `16/16 PASS`;
- P1.2 `60/60 PASS`;
- worktree clean.

Verdict:

**P1.2 ACTION → RESULT: PASS — qualification-only.**

No operational Action permission is implied.

---

# 3. P1.3 — RESULT → TRACE qualification-only

## Contract

`P1_3_RESULT_TRACE_EVIDENCE_BOUNDARY_V1`

Formalized in:

`GOVERNANCE/STEP-3-REAL-SYSTEM-MAPPING.md`

## Existing Trace schema retained

`src/decision_trace.py`

`DecisionTrace` fields:

- `decision_id`;
- `provenance_id`;
- `research_run_id`;
- `code_version`;
- `configuration_version`;
- `dataset_id`;
- `dataset_version`;
- `context_id`;
- `decision`;
- `action_id`;
- `result_id`.

`DecisionTrace.validate()` remains structural only. Structural PASS is not P1.3 authority.

## P1.3 producer / attestation

Added qualified production path:

`produce_decision_trace(evidence, decision, action, result)`

and attestation check:

`is_factory_attested_decision_trace(...)`.

The exact chain is:

`exact ResearchRunEvidence → exact Decision → exact ActionEvidence → exact ResultObservation → factory-attested DecisionTrace`.

Manual or same-valued Trace can be structurally valid while remaining non-attested.

## Exact ResearchRunEvidence provenance defect found and corrected

P1.3 breaker found that same-valued/reconstructed research evidence could otherwise be substituted downstream.

`src/decision.py` was strengthened to retain the exact originating `ResearchRunEvidence` privately and expose:

`is_decision_bound_to_exact_research_evidence(...)`.

Correction commit:

`16ecbcaab3bfc477f2a7de6c2a5d3a7f75adaf94`

Second breaker / workflow update commit:

`a1f5b86c74e64ee128753afdcc66d150dd7c645c`

Qualification run:

- run `35246726515`;
- attempt `2`;
- job `105289153528`;
- RESEARCH→DECISION `16 PASS`;
- P1.2 `60 PASS`;
- P1.3 `41 PASS`;
- clean worktree.

Verdict:

**P1.3 RESULT → TRACE: PASS — qualification-only.**

Important semantic property retained: a produced Trace is an autonomous historical downstream snapshot. It may remain attested after upstream object GC, but it does not contain `Action.behavior` or `Result.outcome`.

---

# 4. PRE-P1.4 — TRACE → MEMORY discovery

A strict read-only discovery was performed before inventing MEMORY.

Files/surfaces inspected included:

- `GOVERNANCE/EXPERIMENTAL-MEMORY-CHARTER.md`;
- `GOVERNANCE/STEP-3-REAL-SYSTEM-MAPPING.md`;
- `src/decision_trace.py`;
- `src/action_result_evidence.py`;
- `src/research_findings.py`;
- `src/research_run_evidence.py`;
- `src/decision.py`;
- `04-REFERENCE/RESEARCH-INTERPROCESS-REATTESTATION-CONTRACT.md`;
- `docs/10-TEMPORAL-POINT-IN-TIME-CONTRACT.md`;
- relevant governance and audit surfaces.

## Key discovery

Trace is not experimental memory.

A qualified Trace establishes that a governed chain occurred/reconstructs, but it does not contain:

- `behavior`;
- `outcome`;
- hypothesis;
- prediction;
- falsification rule;
- measurements;
- explanations;
- `ResearchFinding.status`;
- confidence;
- knowledge status;
- limits/invalidation conditions;
- knowledge availability time.

## `ResearchFindings` assessment

`ResearchFindings` already provides rich experimental semantics:

- `ResearchHypothesis`;
- `ResearchMeasurement`;
- `ResearchFinding`;
- statuses `SUPPORTED`, `REFUTED`, `NOT_INTERPRETABLE`.

Its factory requires an attested `ResearchRunEvidence`, but after creation the frozen object has no downstream exact-object attestation/origin registry equivalent to P1.2/P1.3.

More importantly, even exact-object attestation alone would not prove that a hypothesis existed before a Decision. Current relevant objects lack the temporal evidence necessary for such a claim.

Therefore `ResearchFindings` was deliberately kept out of the first P1.4 runtime boundary.

## Epistemic separations retained

The final P1.4 reasoning preserved four separations:

`EVENT ≠ EXPERIENCE`

`OBSERVATION ≠ INTERPRETATION`

`EXPERIENCE ≠ KNOWLEDGE`

`KNOWLEDGE ≠ OPERATIONAL AUTHORIZATION`

The second separation was strengthened after independent Claude counter-expertise and then adjudicated against the exact repository HEAD.

## Claude counter-expertise adjudication

Useful retained finding:

- `OBSERVATION ≠ INTERPRETATION` is necessary to prevent post-hoc causality/explanation from contaminating factual observation.

Corrections made against Claude's report:

- Claude claimed Trace becomes unverifiable after upstream GC; repository P1.3 tests already prove the produced Trace can remain attested after upstream collection, so that claim was rejected.
- Claude proposed hypothesis-before-Decision as a P1.4 invariant; current repository objects do not carry sufficient timestamp/provenance evidence to execute that invariant, so it was not adopted.
- absence of `ResearchFindings` must not be silently mapped to `NOT_INTERPRETABLE`.
- survivorship bias cannot be closed by validating one episode; it belongs to future capture policy/AUDIT.

PRE-P1.4 verdict:

**PASS — enough information existed to formalize the smallest observation-only boundary.**

---

# 5. P1.4 formalization

Formalization commit:

`da3361a41dada47114cafa518a48412afa1b39a8`

Commit message:

`governance: formalize P1.4 trace-to-memory episode boundary`

Contract:

`P1_4_TRACE_MEMORY_EPISODE_BOUNDARY_V1`

Formalized only in:

`GOVERNANCE/STEP-3-REAL-SYSTEM-MAPPING.md`

No new governance layer was created.

## Minimal input

`exact attested DecisionTrace + exact QualificationActionEvidence + exact QualificationResultObservation → ObservationalMemoryEpisode`

No `ResearchFindings`, hypothesis, knowledge, confidence or time-of-knowledge field belongs to this first episode.

## Meaning

The first episode means only:

> this qualified chain occurred, this exact behavior was engaged, and this exact outcome was observed.

It does not mean:

- Action caused Result;
- Decision was correct;
- hypothesis was tested;
- result supports/refutes anything;
- experience is knowledge;
- memory authorizes future action.

---

# 6. P1.4 minimal executable candidate

Candidate commit:

`ec3487ea3ed74c374a273466bfac977d3553b166`

Commit message:

`p1.4: add minimal observational memory episode candidate`

Runtime file:

`src/memory_episode.py`

Type:

`ObservationalMemoryEpisode`

It contains the Trace projection plus only:

- `behavior` from the exact Action;
- `outcome` from the exact Result.

`episode_id` is deterministic content identity, not authority.

Process-local authority uses exact-object identity + weakref + fingerprint.

P1.2 gained only the smallest read-only hook required by P1.4:

`verify_qualification_observation_pair(action, result)`.

This hook does not mint or repair Action/Result.

---

# 7. P1.4 first breaker A0–G4

Breaker/workflow commit:

`f7278000cdbd5d427db8a9b67d3698f98a5466bd`

Commit message:

`test: break P1.4 observational memory episode boundary`

First run:

- run `35263365734`;
- job `105344333468`;
- SUCCESS.

Counts:

- RESEARCH→DECISION `16/16`;
- P1.2 `60/60`;
- P1.3 `41/41`;
- P1.4 A0–G4 `49/49`;
- worktree clean.

No correction was invented because the first breaker was genuinely green.

---

# 8. P1.4 second breaker — real provenance defect found

A second breaker targeted bypasses not fully covered by A0–G4:

- exact provenance Trace ↔ Action/Result;
- lifetime and mutation after episode creation;
- same-valued authentic collisions;
- duplicate episode behavior;
- misuse of the new P1.2 verifier.

Breaker commit:

`68301d80163a24511e880f856c07ed9e4d646013`

The run became genuinely red.

Eight of nine attacks passed; attack H8 failed.

## H8 defect

After resetting/reloading the P1.2 producer registry, a new authentic Action/Result pair could receive the same IDs as an older pair. P1.4 then had enough value-level identity to accept the newer pair against an older Trace.

This proved:

`same IDs + both authentic ≠ exact historical pair`

## Minimal correction

Correction commit:

`4d1622055f141208e34d717024f2b882934d91a3`

P1.3 Trace attestation was extended to retain private weak references to the exact Action/Result objects that originally produced the Trace, while keeping the already-qualified property that Trace validity survives their later GC.

A read-only verifier was exposed for:

`Trace ↔ exact historical Action/Result`.

P1.4 now requires both:

1. current P1.2 admissibility of the pair; and
2. exact historical provenance binding from the Trace.

---

# 9. P1.4 CI defects discovered while closing

The P1.4 correction caused old regression guards to expose two CI issues unrelated to runtime semantics.

## P0.2 stale documentary equality guard

P0.2 expected the evolving mapping file byte-for-byte equal to an old baseline even though P1.2/P1.3/P1.4 had legitimately appended governed addenda.

The guard was corrected without weakening the protected P0.2 core: the evolving mapping surface was removed from inappropriate byte-equality enforcement and current governed contracts were required explicitly.

Correction commit:

`03e1f8c48442568ef5cc0a717fde4714c8d4eef1`

## Second-breaker interpreter pollution

H8 deliberately reloaded P1.2 modules to simulate lifecycle reset. Executing this reload inside the main pytest interpreter polluted class/registry identity for tests that followed in full-suite guards.

This was a test isolation defect, not a runtime defect.

Correction: execute H8 lifecycle-reset attack in a subprocess.

Isolation correction HEAD:

`64dcfa331736dc8624556a1ac160d56748dd5fab`

## Full-suite guard path filters

P0.4 and P0.6 run the complete repository `pytest -q`, but their workflow path filters did not trigger for all changes under `tests/**`.

They were corrected to monitor `tests/**`, so a test capable of breaking their full suite cannot change silently without triggering those guards.

---

# 10. P1.4 persisted-HEAD final PASS

Final persisted qualification HEAD:

`12936ce44a1ba5dd3ac154fc62c62bf39a9997b5`

On that same SHA:

- P0.4 run `35265181355` — SUCCESS; full repository regression `452 passed`;
- P0.6 run `35265181428` — SUCCESS;
- P1.4 run `35265181318`, attempt `2`, job `105350666230` — SUCCESS.

P1.4 exact counts:

- RESEARCH→DECISION `16/16`;
- P1.2 `60/60`;
- P1.3 `41/41`;
- P1.4 A0–G4 `49/49`;
- second breaker H0–H8 `9/9`;
- worktree clean.

Final verdict:

**P1.4 TRACE → MEMORY EPISODE: PASS — qualification-only.**

Explicitly still NOT qualified by P1.4:

- `ResearchFindings` attachment;
- EXPERIENCE→KNOWLEDGE promotion;
- causal inference;
- confidence;
- knowledge look-ahead semantics;
- persistent/inter-process authority;
- memory exhaustiveness / survivorship-bias protection;
- statistical independence;
- MEMORY→AUDIT/REVISION;
- operational authorization.

---

# 11. PRE-P1.5 — durable MEMORY / inter-process trust discovery

A 100% read-only discovery examined how `ObservationalMemoryEpisode` could survive the process that produced it without turning JSON/hash/storage into its own authority.

## Central distinction

P0.5 RESEARCH re-attestation works because RESEARCH can be deterministically replayed from trusted source bytes.

Historical Action→Result cannot be verified by replay:

`REPLAY(ACTION → RESULT) ≠ PROOF(original ACTION → RESULT)`

A replay would create a new event.

Therefore P1.5 requires a witness/capture model, not replay re-attestation.

## Durable authority decomposition

The minimal conceptual chain discovered was:

`P1.4-attested episode → canonical durable record → trusted capture/witness → durable receipt → fresh process + external trust expectation → verification → fresh local historical-memory re-attestation`

Key separations:

- durable record ≠ authority;
- content integrity ≠ provenance/authenticity;
- capture authority ≠ captured artifact;
- receipt ≠ historical event;
- content identity ≠ occurrence/registration identity;
- replay ≠ historical verification;
- fresh-process re-attestation ≠ original object resurrection.

`episode_id` must remain content identity. It must not silently become globally unique historical occurrence identity.

A durable `registration_id` identifies a capture/registration, not automatically a distinct historical experiment.

PRE-P1.5 verdict:

**PASS — trust boundary sufficiently mapped.**

Executable durable authority remained BLOCKED until a concrete trust model was selected.

---

# 12. P1.5 contract formalization

Formalization commit:

`3474e7dc3a6f422ae21b75dfccfbc4342d09b793`

Commit message:

`governance: formalize P1.5 durable memory re-attestation boundary`

Contract:

`P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1`

Formalized only in:

`GOVERNANCE/STEP-3-REAL-SYSTEM-MAPPING.md`

No storage/signature/key/service technology was chosen at formalization time.

P1.5 explicitly retained P0.5's negative principles:

- serialized artifact is not authority;
- hash/content-address is integrity, not authority;
- trust expectation must be external to the artifact;
- fresh process must fail closed on unknown schema/substitution/missing trust;
- no bypass like `trust_record=True`, `accept_digest_only` or `skip_verification`.

But P0.5 deterministic replay was explicitly rejected for historical MEMORY.

---

# 13. P1.5 capture-authority model comparison

A read-only adversarial comparison was performed before implementation.

Question:

> In a new process, what fact is trusted independently of the record and receipt?

## Models rejected as insufficient or unnecessarily broad

### Hash/content-address only

Rejected: anyone able to rewrite the record can recompute the hash. Integrity is not capture authority.

### Self-declared `authority_id`

Rejected: the bundle would select the authority the verifier is supposed to trust. This is self-authorization.

### Git/GitHub location or commit identity alone

Rejected as trust root: storage location/content identity does not prove the record was captured from an exact P1.4-attested episode. Current commits are also unsigned and the branch is not protected; no such GitHub trust root has been qualified.

### Shared symmetric secret / HMAC

Rejected as the minimal first model: it can authenticate, but every verifier holding the shared secret also gains minting power. This unnecessarily widens the authority boundary.

### Asymmetric signature

Potentially viable but deferred as broader than necessary for the first qualification candidate because it immediately introduces signer isolation plus key custody, rotation, revocation and recovery policy.

### Trusted append-only service / registry

Potentially viable but deferred as broader than necessary because it creates a persistent authority/service boundary before a smaller model has been tested.

## Selected model

`P1_5_EXTERNAL_RECEIPT_PIN_TRUST_MODEL_V1`

Selection commit:

`38595b56fcf1a7e9e53f29dd30d2802ab6e9be40`

Commit message:

`governance: select P1.5 external receipt pin trust model`

## Selected trust expectation

For each durable registration, the fresh process receives OUTSIDE the record/receipt bundle:

- `expected_contract`;
- `expected_authority_id`;
- `expected_receipt_sha256`.

The receipt itself may contain contract and authority claims, but they are only accepted if they match the separately provisioned trust expectation and the exact externally pinned receipt digest.

No secret is needed by the verifier. The verifier therefore gains no receipt-minting capability.

Tradeoff accepted deliberately: one external pin must be provisioned per registration. If this operational cost later becomes unacceptable, that would constitute real evidence for introducing a broader signature/PKI/service model.

## Registration identity refinement discovered test-first

Before runtime implementation, the breaker design exposed one additional requirement:

`registration_id` must be bound to the registration content, otherwise a fresh process with no global registry cannot detect rebinding of the same registration ID to a different capture.

The breaker therefore requires a registration identity derived/bound from at least:

- capture nonce;
- exact record identity/digest;
- contract/authority context as appropriate.

No trusted timestamp is introduced.

A `capture_nonce` can distinguish capture registrations without pretending to prove occurrence time or historical experiment independence.

---

# 14. P1.5 pre-implementation breaker A0–G4

Breaker commit:

`e8ea512cbacf98d954c4d87316365733805d501b`

File:

`breakers/p1_5_external_receipt_pin_breaker.py`

Workflow commit / current implementation-breaker HEAD before backup:

`6a0d33ac08f4825d554ad1d87805b64017b9720f`

Commit message:

`ci: add P1.5 durable memory preimplementation breaker`

Workflow:

`.github/workflows/p1-5-durable-memory-reattestation.yml`

No `src/memory_interprocess.py` exists at this checkpoint.

The workflow explicitly proves the breaker exists before the runtime candidate.

## First P1.5 run — expected red

Run:

`35271832061`

Job:

`105372835362`

HEAD:

`6a0d33ac08f4825d554ad1d87805b64017b9720f`

Result:

**FAIL — expected pre-implementation red.**

Protected upstream results before P1.5 breaker:

- qualification environment: PASS;
- RESEARCH→DECISION: `16 passed`;
- P1.2: `60 passed`;
- P1.3: `41 passed`;
- P1.4 combined: `58 passed`;
- clean worktree check: PASS.

P1.5 breaker:

`37 failed` after parametrization.

Every P1.5 failure has the same controlled cause:

`P1.5 candidate absent — expected pre-implementation FAIL: src.memory_interprocess does not exist`

This proves:

- breaker collection is valid;
- fixtures execute;
- workflow reaches P1.5 only after protected upstream gates pass;
- the red evidence is genuine absence of runtime candidate, not syntax/test corruption.

## Breaker scope

A — capture source exactness / rejection of manual, copy, JSON, mutated episode.

B — record/receipt completeness, external pin requirement, rehashed tamper, storage-location non-authority.

C — exact external contract/authority/receipt pin, rejection of wrong pin/authority/contract and bundle self-trust.

D — fresh-process historical re-attestation, no Action/Result replay inputs, raw deserialized episode remains unattested, no original-object resurrection.

E — registration identity distinct from content identity, duplicate registration not independent experiment, physical copy not new registration, registration rebinding fails closed, one registration pin cannot authorize another.

F — no caller-supplied trusted timestamp, registration is not `known_from`, no local-clock repair of missing qualified time.

G — no reverse authority, no ResearchEvidence/Findings promotion, no knowledge status, no P1.1 authorization, no broker/acquisition/backtest/live surface.

---

# 15. Files that matter most for tomorrow

Read in this order before mutation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. `04-REFERENCE/RECOVERY-CHECKPOINT.md`
3. this backup: `99-BACKUP/SESSION-2026-09-17-END-OF-DAY-P1.2-P1.5-MEMORY-BOUNDARIES.md`
4. `GOVERNANCE/STEP-3-REAL-SYSTEM-MAPPING.md`
5. `src/memory_episode.py`
6. `src/decision_trace.py`
7. `src/action_result_evidence.py`
8. `breakers/p1_5_external_receipt_pin_breaker.py`
9. `.github/workflows/p1-5-durable-memory-reattestation.yml`
10. `04-REFERENCE/RESEARCH-INTERPROCESS-REATTESTATION-CONTRACT.md`
11. `04-REFERENCE/QUALIFICATION-ENVIRONMENT-LOCK.json`
12. `requirements/qualification.lock.txt`

Then verify the real branch HEAD and compare it with the implementation/breaker anchor `6a0d33ac08f4825d554ad1d87805b64017b9720f` plus the documentary backup/checkpoint descendants before substantive mutation.

---

# 16. Do not redo tomorrow

Do not redo the PRE-P1.4 repository discovery unless the relevant files changed materially.

Do not resend/re-run the Claude six-chunk audit protocol. The useful findings were already adjudicated against GitHub and incorporated where valid.

Do not reconsider `ResearchFindings` as mandatory P1.4 input without new evidence. It is intentionally outside the current qualified episode.

Do not replace the selected P1.5 trust model with signatures, HMAC, Git trust or an append-only service merely because those technologies are familiar. The external receipt pin model was selected specifically as the smallest model to test first.

Do not treat P1.5's expected red run as a regression. It is the intentional test-first baseline proving the candidate is absent.

Do not alter the breaker before observing the first runtime candidate against it, except to fix a demonstrated defect in the breaker itself.

Do not interpret a future P1.5 green run as knowledge validation or operational authorization.

---

# 17. Current verdict matrix at end of day

- P0.2: **PASS / protected baseline**
- P0.3: **PASS / protected baseline**
- P0.4: **PASS / protected baseline**
- P0.5: **PASS / protected baseline**
- P0.6: **PASS / protected reproducibility envelope**
- P1.0: **qualified fail-closed promotion boundary; no permissive authorization created**
- P1.1: **PASS block-only; positive AUTHORIZED remains BLOCKED**
- P1.2 ACTION→RESULT: **PASS — qualification-only**
- P1.3 RESULT→TRACE: **PASS — qualification-only**
- P1.4 TRACE→MEMORY EPISODE: **PASS — qualification-only**
- P1.5 durable MEMORY formalization: **PASS**
- P1.5 trust-model selection: **PASS — `EXTERNAL_RECEIPT_PIN_V1` selected**
- P1.5 executable runtime: **BLOCKED / not implemented**
- P1.5 pre-implementation breaker: **real expected FAIL observed**

No positive operational authorization has been created.

---

# 18. Exactly one next governed action

**Implement the smallest possible `src/memory_interprocess.py` candidate satisfying only `P1_5_EXTERNAL_RECEIPT_PIN_TRUST_MODEL_V1`, without modifying the frozen breaker first; run the existing P1.5 A0–G4 breaker, inspect the actual violations, and correct only defects demonstrated by that breaker.**

The first candidate should introduce only the responsibilities already frozen by the contract/breaker:

- capture from exact P1.4-attested `ObservationalMemoryEpisode`;
- canonical durable record bytes;
- canonical receipt bound to exact record + registration identity;
- externally supplied expected contract / authority / receipt digest;
- fresh-process verification;
- fresh local historical-memory attestation;
- no replay of Action/Result;
- no trusted timestamp;
- no knowledge/AUDIT/REVISION/operational surface.

Do not jump directly to final PASS. After the first candidate, preserve real FAILs, apply minimal corrections, build a second targeted breaker if warranted, then require a persisted-HEAD re-break before closure.

---

# 19. End-of-day stop rule

Stop here for 17 September 2026.

Do not implement P1.5 tonight after this backup/checkpoint save.

Tomorrow resume from GitHub, not from conversational memory.
