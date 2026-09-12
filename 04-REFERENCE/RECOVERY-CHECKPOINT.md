# RECOVERY CHECKPOINT — B09

> Versioned recovery state for the current qualification workstream.
> This document is the durable handoff point. It must be updated at logical milestones, not after every command.

## 1. ÉTAT ACTUEL

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Branch:** `feat/v4-3-instrument-contracts`
- **PR:** #8 — draft, unmerged
- **Reference baseline:** `ff50b6d5d123969e091b5df18c46d438f7cb8052`
- **Current qualification block:** B09 — Research Output / Event Integrity
- **Execution worktree:** local PR8 test worktree; local state may contain changes not yet present on the remote PR8 head.

## 2. CHEMIN PARCOURU

### Previously locked qualification blocks

- B02 — PASS: physical corpus identity qualified.
- B03 — initial FAIL: naive 24/7 continuity invalid for market calendar.
- B03.1 — initial FAIL: one unexpected data gap remained.
- B03.2 — FAIL: acquisition loss confirmed; reference corpus incomplete at that stage.
- B03.3 — FAIL intentionally: candidate reconstruction is not dataset validity.
- B02' — PASS: candidate physical corpus identity qualified at 495 files.
- B03.1' — PASS: all remaining gaps explained by explicit calendar.
- B04 — PASS: tick semantic integrity qualified.
- B05 — PASS: deterministic corpus/contract reproducibility qualified.
- B06-A — PASS: corpus/contract/source-format/window identity qualified.
- B07-A — PASS: native BI5 engine locked to BoundResearchInput.
- B07-B — PASS: native engine consumed the qualified corpus.
- B06-B — PASS: fail-closed execution input binding qualified.
- B08 — PASS: official qualified research execution.
- B08-A — PASS: production binding established as architectural engine boundary.
- B08-B.1 — PASS: production execution graph and dynamic bypass controls qualified.

### B09 progress

- B09.0.1 — PASS: real-code state/introspection established.
- B09.1 — PASS: lexical/real-code audit found no tick sorting, deduplication, repair, or interpolation in the reader; file sorting is authorized and required; global order is checked by `iter_ticks()`.
- B09.2 — PASS: independent direct-reader stream matched official engine stream for 5,130,393 ticks; SHA-256 matched under the then-current serialization.
- B09.3 — PASS for tick immutability and official sequence integrity; FAIL identified in the decimal hash representation because distinct IEEE-754 float values could serialize identically at 12 decimals; `BI5ResearchEngine.run()` also lacks an explicit global monotonicity check, classified as architectural exposure because the official output path uses `iter_ticks()`.
- B09.4 — BLOCKED: the instrument contract did not explicitly define output numeric representation/rounding semantics. No semantics were invented.
- B09.5 — PASS: exact IEEE-754 binary64 representation was proven distinct and round-trippable for the relevant values.
- B09.6 — PASS: production hash serialization was corrected from decimal formatting to exact `struct.pack(">d", value)` representation.
- B09.7 synthetic re-break — PASS: prior decimal collision eliminated; IEEE-754 byte representations remained distinct; B08-A regression tests remained 2/2 PASS.
- B09.7 full-stream re-break — PASS: exact B05-qualified corpus was re-established and the corrected production stream was independently reproduced and matched across two official runs.
- B09 run() exposure closure — PASS: direct code-path evidence established that the official qualification path uses `iter_ticks()` and does not admit `BI5ResearchEngine.run()` as an official qualification entrypoint. The remaining exposure was formally closed as non-official/non-production.

## 3. ÉTAT DES ARTEFACTS

### Code

- `src/research/input_binding.py` — production binding boundary; sealed `BoundResearchInput`.
- `src/research/bi5_reader.py` — native BI5 decoding and semantic validation.
- `src/research/engine.py` — native BI5 research engine.
- `src/research/execution.py` — official qualified execution and exact IEEE-754 stream hashing.

### Tests

- `tests/test_b08_a_architectural_enforcement.py` — latest observed result: **2 passed** after B09.6 correction.

### Reports

- `reports/data-qualification/b09_7_full_rebreak_report.json` — B09.7 full-stream adversarial re-break: **PASS**.
- `reports/data-qualification/b09_run_exposure_closure_report.json` — B09 run() exposure closure: **PASS**.

### Data

- Exact B05-qualified corpus re-established at:
  `C:\ALGO-DATA\qualification\v4_3_multi_year_acquisition\candidate_b03_3_repaired\USATECHIDXUSD`
- Physical corpus identity: 495 files.
- Full stream cardinality: 5,130,393 ticks.

### Contract / hashes

- B05 canonical corpus hash: `868a21c6a1bedf095b30bc64b6c2ef60b5db9d30146ac53034360254413f8ad7`
- B05 contract hash: `49e272534bf5061522eb624afe4e27d6585f730e0271b5284bff2442d5c04b07`
- Historical B08 stream SHA-256: `4768c0e66647a15ba703d2dcdc88c03db84846a625e8eb3f70914428bf11c8d7`
- Current canonical B09 stream SHA-256 after IEEE-754 correction: `d8da494b2a1380ea0db0e0370ece4f609374ecb3e5647b6c1fb290836867abda`
- The stream signature changed because B09.6 changed only the hash serialization representation; corpus identity and stream cardinality remained unchanged.

## 4. ERREURS / ÉCHECS À NE PAS RÉPÉTER

1. Assuming a probe exists because it existed temporarily during the conversation.
2. Assuming a filesystem path from another worktree.
3. Creating a probe before verifying the actual execution/data context.
4. Repeating a failed command instead of diagnosing its exact failure.
5. Using fragile string replacement when a clean rewrite is safer.
6. Treating a synthetic re-break as equivalent to a full production-corpus re-break.
7. Treating a reconstructed or substituted corpus as the original qualified corpus.

### Methodological correction

The exact B05 corpus was verified by its canonical inventory hash before the B09.7 full-stream re-break. B02–B08 were not rerun; their locked PASS results were reused as prior evidence.

The `BI5ResearchEngine.run()` exposure was closed without a production patch because direct code-path evidence showed that the official qualified execution path uses `iter_ticks()` and the generic `run()` method is not an admissible qualification entrypoint.

## 5. PREUVES

### Reproducible/current evidence

- B05 revalidation: 495 files; canonical inventory hash `868a21c6a1bedf095b30bc64b6c2ef60b5db9d30146ac53034360254413f8ad7`; all reproducibility checks PASS.
- B08-A architectural tests: 2/2 PASS after B09.6.
- B09.5 exact float representation: PASS.
- B09.6 IEEE-754 production serialization: PASS.
- B09.7 synthetic collision re-break: PASS.
- B09.7 full-stream re-break: PASS; 5,130,393 ticks; independent and two official runs all produced `d8da494b2a1380ea0db0e0370ece4f609374ecb3e5647b6c1fb290836867abda`.
- B09 run() exposure closure: PASS; official execution uses `iter_ticks()` and the generic `run()` method is explicitly excluded from qualification use unless separately qualified.

### Historical evidence

- B09.2 independent stream comparison: 5,130,393 ticks, identical stream SHA under the pre-correction serialization.
- B09.3 official sequence integrity evidence.
- B05/B07/B08 qualification results recorded above.

### Final B09 decision

The former `BI5ResearchEngine.run()` architectural exposure is closed as **NON_OFFICIAL_NON_PRODUCTION**. `iter_ticks()` remains the sole admissible stream-consumption path for the qualified research execution covered by B09. A future attempt to use `run()` as a qualification entrypoint requires a new explicit qualification of its invariants, including global tick-stream monotonicity.

## 6. DERNIER VERDICT

**B09: PASS**

Reason: all identified B09 qualification issues are resolved or formally closed. The IEEE-754 hash collision exposure was corrected and fully re-broken on the exact B05-qualified corpus. The remaining `run()` exposure was dispositioned by direct code-path evidence and closed as non-official/non-production. No earlier qualification block was rerun or reopened.

## 7. PROCHAINE ACTION UNIQUE

**Consolidate B09 as locked PASS and recover the next qualification block from the governing Recovery Checkpoint before starting any new substantive work.**

Do not rerun B02–B08. Do not rerun B09.7. Do not treat `BI5ResearchEngine.run()` as a qualified research entrypoint without a new explicit qualification.

## 8. RECOVERY RULE

At the start of the next substantive action, consult:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this `04-REFERENCE/RECOVERY-CHECKPOINT.md`
3. the actual GitHub/worktree state

Then execute only the single next action above unless new evidence changes the verdict.
