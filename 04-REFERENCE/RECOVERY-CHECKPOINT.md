# RECOVERY CHECKPOINT — B09

> Versioned recovery state for the current qualification workstream.
> This document is the durable handoff point. It must be updated at logical milestones, not after every command.

## 1. ÉTAT ACTUEL

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Branch:** `feat/v4-3-instrument-contracts`
- **PR:** #8 — draft, unmerged
- **Reference baseline:** `ff50b6d5d123969e091b5df18c46d438f7cb8052`
- **Known remote PR8 head at checkpoint creation:** `761eb1e2bdb12f551cfea2d9db88df26472680ef`
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
- B09.2 — PASS: independent direct-reader stream matched official engine stream for 5,130,393 ticks; SHA-256 matched.
- B09.3 — PASS for tick immutability and official sequence integrity; FAIL identified in the decimal hash representation because distinct IEEE-754 float values could serialize identically at 12 decimals; `BI5ResearchEngine.run()` also lacks an explicit global monotonicity check, classified as architectural exposure because the official output path uses `iter_ticks()`.
- B09.4 — BLOCKED: the instrument contract did not explicitly define output numeric representation/rounding semantics. No semantics were invented.
- B09.5 — PASS: exact IEEE-754 binary64 representation was proven distinct and round-trippable for the relevant values.
- B09.6 — PASS: production hash serialization was corrected from decimal formatting to exact `struct.pack(">d", value)` representation.
- B09.7 synthetic re-break — PASS: prior decimal collision eliminated; IEEE-754 byte representations remained distinct; B08-A regression tests remained 2/2 PASS.
- B09.7 full-stream re-break — BLOCKED: a temporary probe used an assumed corpus path that does not exist in the active PR8 test worktree. The failure was in the probe assumptions, not evidence of a production defect. The exact B05 corpus must be re-established from verified repository/worktree state before the full-stream re-break is run.

## 3. ÉTAT DES ARTEFACTS

### Code

- `src/research/input_binding.py` — production binding boundary; sealed `BoundResearchInput`.
- `src/research/bi5_reader.py` — native BI5 decoding and semantic validation.
- `src/research/engine.py` — native BI5 research engine.
- `src/research/execution.py` — official qualified execution and exact IEEE-754 stream hashing.

### Tests

- `tests/test_b08_a_architectural_enforcement.py` — latest observed result: **2 passed** after B09.6 correction.

### Probes

- Historical B09.2/B09.3/B09.5/B09.7 synthetic probes were executed during the session but were not all persisted as files.
- `tools/probe_batch01_b09_7_full_rebreak.py` was created with an unverified assumed path and produced a BLOCKED execution; it must not be treated as a valid qualification artifact without correction.
- Do not assume temporary probes from conversation history still exist.

### Data

- The exact B05 qualified corpus is not present in the PR8-TEST worktree path previously assumed by the failed B09.7 probe.
- Verified `.bi5` files were found elsewhere under the user's Windows environment, but those are not automatically equivalent to the B05 corpus.

### Contract / hashes

- B05 canonical corpus hash: `868a21c6a1bedf095b30bc64b6c2ef60b5db9d30146ac53034360254413f8ad7`
- B05 contract hash: `49e272534bf5061522eb624afe4e27d6585f730e0271b5284bff2442d5c04b07`
- Official stream SHA previously qualified: `4768c0e66647a15ba703d2dcdc88c03db84846a625e8eb3f70914428bf11c8d7`
- Qualified corpus: 495 files / 5,130,393 ticks.

## 4. ERREURS / ÉCHECS À NE PAS RÉPÉTER

1. Assuming a probe exists because it existed temporarily during the conversation.
2. Assuming a filesystem path from another worktree.
3. Creating a probe before verifying the actual execution/data context.
4. Repeating a failed command instead of diagnosing its exact failure.
5. Using fragile string replacement when a clean rewrite is safer.
6. Treating a synthetic re-break as equivalent to a full production-corpus re-break.
7. Treating a reconstructed or substituted corpus as the original qualified corpus.

### Methodological correction

Before the next B09 action, first verify the real active worktree and identify the exact B05 corpus using the known B05 identity/hash and repository evidence. Do not rerun B02–B08 merely because the path is currently unknown.

## 5. PREUVES

### Reproducible/current evidence

- B08-A architectural tests: 2/2 PASS after B09.6.
- B09.5 exact float representation: PASS.
- B09.6 IEEE-754 production serialization: PASS.
- B09.7 synthetic collision re-break: PASS.

### Historical evidence

- B09.2 independent stream comparison: 5,130,393 ticks, identical stream SHA.
- B09.3 official sequence integrity evidence.
- B05/B07/B08 qualification results recorded above.

### Missing evidence

- Full-stream B09.7 re-break against the exact B05-qualified corpus after the IEEE-754 correction.
- Explicit decision/evidence regarding whether `BI5ResearchEngine.run()` must itself enforce global monotonicity, or whether its non-official status can be formally closed as architectural exposure.

## 6. DERNIER VERDICT

**B09: BLOCKED**

Reason: the final full-stream adversarial re-break cannot yet be executed against the exact qualified B05 corpus from the current verified worktree state. This is an execution-context/evidence gap, not a proven production failure.

## 7. PROCHAINE ACTION UNIQUE

**Identify and verify the exact B05-qualified corpus in the active worktree/repository using the recorded corpus identity/hash, without recreating or rerunning already-PASS qualification blocks.**

Only after that single action is complete may B09.7 full-stream re-break resume.

## 8. RECOVERY RULE

At the start of the next substantive action, consult:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this `04-REFERENCE/RECOVERY-CHECKPOINT.md`
3. the actual GitHub/worktree state

Then execute only the single next action above unless new evidence changes the verdict.
