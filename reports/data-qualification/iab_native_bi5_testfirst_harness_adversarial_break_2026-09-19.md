# I_A + I_B — ADVERSARIAL BREAK OF TEST-FIRST BREAKER / HARNESS LAYER

**Date:** 2026-09-19  
**Candidate HEAD under attack:** `58a80df0bd9513cbc0f80c8b24896fedb354f4aa`

Candidate breaker blobs:

```text
I_A breaker
b95501729ef7d1282b7915f4895f978e190c5eb6

I_B breaker
4080b9899ca02f3eea071fb70371f0be5cc80855
```

Preimplementation workflows:

```text
I_A run 35441192904 / job 105892147172
→ failure
→ 20 errors
→ every breaker error caused by absent src.native_bi5_reference_qualifier

I_B run 35441243836 / job 105892281429
→ failure
→ 19 errors
→ every breaker error caused by absent src.native_bi5_independent_qualifier
```

All workflow steps before the breaker passed, including exact persisted hashes, expected runtime absence, qualification-environment verification and clean-worktree proof.

No production I_A/I_B code, BI5 download, real-data processing or backtest occurred.

---

## 1. Attack objective

A valid RED baseline is not sufficient if the future breaker can be fooled by the implementation under test.

The breaker/harness layer was therefore attacked for:

- self-attested independence;
- self-reported isolation;
- static-only shared-semantic dependency detection;
- ability to distinguish real external evidence from implementation claims.

---

## 2. Demonstrated defect IAB-TF-F01 — SELF_ATTESTED_INDEPENDENCE_EVIDENCE

Current I_B breaker requires implementation-authored manifest fields equivalent to:

```text
independent_derivation_attestation = PASS
no_copy_or_generated_from_other_path = true
source_similarity_review_result = PASS
```

Attack:

An I_B implementation is copied from I_A, mechanically renamed, and returns exactly those strings/booleans in its own manifest.

The breaker accepts the implementation's own assertion as the evidence intended to audit that implementation.

Result:

```text
BREAK — IAB-TF-F01
SELF_ATTESTED_INDEPENDENCE_EVIDENCE
```

Required correction:

- implementation manifest may expose source provenance and immutable evidence references;
- PASS/FAIL of independence must be computed by the breaker/harness from external evidence;
- source similarity review must be breaker-owned, not implementation-authored;
- copied/near-copied semantic source must be independently detectable.

---

## 3. Demonstrated defect IAB-TF-F02 — SELF_REPORTED_ISOLATION_EVIDENCE

Current I_A/I_B breakers inspect `result.isolation_evidence` and trust fields such as:

```text
other_path_output_readable = False
network_policy = DENY
ipc_policy = DENY
runtime_read_set subset-of preseal_input_allowlist
```

Attack:

A non-conforming I_B reads an I_A result through a temp file, environment variable, shared cache or IPC, then returns a fabricated isolation-evidence mapping claiming those reads did not occur.

The current breaker has no independent observation of that runtime access path.

Result:

```text
BREAK — IAB-TF-F02
SELF_REPORTED_ISOLATION_EVIDENCE
```

Required correction:

The breaker/harness must independently observe or enforce the pre-seal boundary. At minimum for the synthetic test layer:

- breaker-owned runtime audit/read trace;
- explicit trap artifacts/environment values for other-path leakage;
- denial/detection of network/socket/subprocess channels;
- comparison of implementation-reported isolation evidence against breaker-observed facts.

Implementation-produced isolation evidence may remain supplementary but cannot be sole proof.

---

## 4. Demonstrated defect IAB-TF-F03 — STATIC_ONLY_SHARED_SEMANTIC_DEPENDENCY_DETECTION

Current source checks reject literal forbidden module names and inspect implementation-reported dependency lists.

Attack:

An implementation dynamically constructs the forbidden module name or reaches another semantic helper through an alias not present as a forbidden literal.

The literal source scan can miss the dependency, while an implementation-authored dependency manifest can omit it.

Result:

```text
BREAK — IAB-TF-F03
STATIC_ONLY_SHARED_SEMANTIC_DEPENDENCY_DETECTION
```

Required correction:

Add breaker-owned runtime audit evidence capable of observing forbidden dynamic import/file/network/subprocess events during synthetic qualification.

Static source/import checks remain useful but may not be the only evidence.

---

## 5. Attacks that survive

The following current breaker properties remain sound and are not weakened:

- exact future module absence produces deliberate RED;
- exact status axes are encoded;
- strict duplicates are tested;
- traversal-relative timestamp regression is preserved;
- zero/crossed prices and finite negative volume are retained;
- local reject accounting is tested;
- late semantic BLOCKED prohibits a partial universe;
- missing determinants fail closed;
- filename hour inference is rejected;
- result seals are mutation-sensitive;
- pair-side one-sided semantic mutants are testable;
- result byte hash is not treated as semantic equality;
- permission leakage is forbidden.

---

## 6. Verdict

```text
TEST-FIRST I_A/I_B BREAKER / HARNESS CANDIDATE
FAIL
```

Demonstrated defects:

1. `IAB-TF-F01 — SELF_ATTESTED_INDEPENDENCE_EVIDENCE`
2. `IAB-TF-F02 — SELF_REPORTED_ISOLATION_EVIDENCE`
3. `IAB-TF-F03 — STATIC_ONLY_SHARED_SEMANTIC_DEPENDENCY_DETECTION`

The initial RED runs remain valid preimplementation evidence, but the breaker layer itself must be corrected and re-run before it can govern production implementation.

No production implementation is authorized yet.

---

## 7. Authorized minimal correction

Correct only the breaker/harness layer:

1. move independence adjudication out of implementation self-claims and into breaker-owned checks;
2. retain only immutable provenance/evidence references in implementation manifests;
3. add breaker-owned source-similarity detection as a non-sufficient but independent copy detector;
4. add breaker-owned runtime audit/trap evidence for dynamic cross-path import/read/network/subprocess leakage;
5. compare self-reported isolation evidence against breaker-observed behavior rather than trusting it alone;
6. update workflow breaker hash locks;
7. rerun both preimplementation workflows.

Expected result after correction:

```text
I_A workflow RED only because I_A module absent
I_B workflow RED only because I_B module absent
all pre-breaker controls PASS
clean worktrees
```

No I_A/I_B production code may be created during this correction.
