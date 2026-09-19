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


---

## 8. First correction and residual persisted-head re-break

First correction commit:

`f3df1cdaae1ed55e852df37444ba69ed55a7e069`

Corrected breaker blobs:

```text
I_A
5509474aed15aad452d38333fa66a3b86224b0f4

I_B
e8f6d3b41a1ecd8acdfb01090d7499cb24d93dea
```

The first correction:

- moved I_B manifest expectations from self-authored PASS labels to evidence references;
- added breaker-owned AST-structure similarity review;
- added breaker-owned Python audit hooks for runtime import/open/socket/subprocess events;
- updated workflow hash locks atomically.

Re-run evidence on that exact persisted HEAD:

```text
I_A run 35441467755
job 105892871250
21 errors
all due only to absent src.native_bi5_reference_qualifier

I_B run 35441467767
job 105892871359
21 errors
all due only to absent src.native_bi5_independent_qualifier
```

All pre-breaker workflow steps and clean-worktree checks passed.

The RED baseline therefore remained clean.

However, adversarial re-break of the corrected harness still found residual proof gaps.

### IAB-TF-R01 — UNRESOLVED_EVIDENCE_REFERENCE_TRUST

The corrected I_B breaker requires non-empty immutable evidence-reference strings, but does not yet resolve those references or bind them to the actual implementation source digests.

Attack:

I_B returns plausible-looking nonexistent evidence paths.

Current result:

the manifest surface test can still pass.

Verdict:

`FAIL / residual TF-F01`.

Required correction:

hard-bind the expected evidence paths in the breaker, require the files to exist once I_B exists, parse them externally, and require their implementation/source bindings to match the runtime manifest.

### IAB-TF-R02 — ENVIRONMENT_CHANNEL_NOT_OBSERVED

The Python audit hook observes import/open/socket/subprocess events but ordinary environment-variable reads are not reliably represented by those audit events.

Attack:

I_B reads an I_A semantic hint from an environment variable and fabricates clean self-reported isolation evidence.

Current result:

the breaker-owned audit may miss the read.

Verdict:

`FAIL / residual TF-F02`.

Required correction:

add a breaker-owned environment canary/tracker and forbid ambient-environment semantic reads.

### IAB-TF-R03 — IMPORT_TIME_DYNAMIC_DEPENDENCY_GAP

The runtime audit hook is installed when qualification executes, after the candidate module has already been imported by the breaker fixture.

Attack:

I_B dynamically imports I_A at module-import time, stores the module/function under an alias, and never imports it again during qualification.

A literal source scan may miss a dynamically constructed module name, and the runtime hook is installed too late.

Verdict:

`FAIL / residual TF-F03`.

Required correction:

breaker-owned inspection of candidate module globals must reject any object/module/function/class whose origin is the opposite implementation path, independently of the implementation-reported dependency manifest.

---

## 9. Second authorized minimal correction

Correct only these residual proof gaps:

1. hard-bind and externally validate future I_B derivation-evidence files against implementation identity/version and source digests;
2. add breaker-owned environment canary/tracking for ambient semantic leakage;
3. inspect imported candidate globals for opposite-path module/function/class origins;
4. preserve the existing source-similarity and runtime-audit controls;
5. update breaker hash locks atomically;
6. re-run both RED workflows.

No production I_A/I_B implementation is authorized during this correction.


---

## 10. Second correction and residual re-break

Second correction commit:

`f495bcb61abff6741ccee23e2dfbd67c4e4300fd`

Breaker blobs:

```text
I_A
8fd8d141d961a73904215236812c224d5e8af355

I_B
b3c342ecfbbf3c2b68c109762e2b936215a316f2
```

The second correction added:

- hard-bound future I_B derivation-evidence paths and external JSON validation;
- exact implementation/version/source-digest bindings for those evidence artifacts;
- breaker-owned environment canaries during qualification;
- breaker-owned cold-import audit;
- candidate-global origin inspection for opposite-path objects/functions/modules.

Re-run evidence:

```text
I_A run 35441590246
job 105893220295
23 errors
all due only to absent src.native_bi5_reference_qualifier

I_B run 35441590283
job 105893220419
23 errors
all due only to absent src.native_bi5_independent_qualifier
```

All pre-breaker workflow controls and clean-worktree checks passed.

The RED baseline remains valid.

### IAB-TF-R04 — IMPORT_TIME_ENVIRONMENT_LEAK_GAP

The environment canary currently wraps qualification execution, not the candidate module's cold import.

Attack:

candidate module reads an opposite-path semantic hint from ambient environment during module import and stores the derived value.

Result:

runtime canary may be too late.

Verdict:

`FAIL / residual TF-F02`.

Required correction:

cold-import audit must install its own environment tracker/canary before candidate import and prove that the forbidden canary was not accessed.

### IAB-TF-R05 — CACHED_OPPOSITE_MODULE_RUNTIME_AUDIT_BLIND_SPOT

In the I_B breaker, source-similarity review legitimately imports I_A before later runtime-audit tests execute.

Attack:

I_B dynamically calls `importlib.import_module(IA_MODULE)` during qualification.

If I_A is already present in `sys.modules`, Python may return it without a new import audit event.

Result:

runtime audit can miss the dynamic dependency.

Verdict:

`FAIL / residual TF-F03`.

Required correction:

before audited semantic execution, temporarily remove the opposite implementation module from `sys.modules`, then restore it after the run.

The cold-import test must also prove the opposite module was not already loaded as a side effect of candidate import.

---

## 11. Third authorized minimal correction

Correct only:

1. cold-import environment canary/tracking;
2. opposite-module `sys.modules` eviction around audited semantic execution;
3. explicit proof that candidate import did not preload the opposite implementation;
4. workflow breaker hash locks.

Then re-run both preimplementation RED workflows.

No production implementation is authorized.


---

## 12. Third correction — final persisted-head re-break

Third correction persisted HEAD:

`331f48ad4080daf1b41f69dddb559e6820cbcff0`

Final breaker/workflow blobs:

```text
I_A breaker
64d3a391e1b5cb5aecfdf926551acd3ee5f0d7dd

I_B breaker
d1a305e3b9ae813e891b34522e3a12bb6bc8ac34

I_A preimplementation workflow
c3325de6f65be5c99f8df5aab19404d1cd627a9a

I_B preimplementation workflow
02151244113b5654647c529899b11997c8762c66
```

The branch was freshly verified identical to that HEAD before final re-break.

The third correction closed:

- import-time environment canary coverage;
- opposite-module `sys.modules` cache eviction during audited execution;
- explicit candidate-import proof that the opposite implementation was not preloaded;
- candidate-global origin checks.

### Final persisted RED executions

I_A:

```text
run = 35441702806
job = 105893512667
result = FAILURE / EXPECTED RED
errors = 23
sole cause = src.native_bi5_reference_qualifier absent
```

I_B:

```text
run = 35441702856
job = 105893512796
result = FAILURE / EXPECTED RED
errors = 23
sole cause = src.native_bi5_independent_qualifier absent
```

For both workflows:

- exact persisted HEAD/hash-lock step: PASS;
- expected production-runtime absence step: PASS;
- locked Python environment installation: PASS;
- qualification-environment verification: PASS;
- only breaker execution step: FAILURE as expected;
- clean worktree: PASS.

No syntax, collection, environment, hash-lock, workflow or worktree defect was observed.

### Final attack matrix

```text
self-attested independence PASS label                 REJECTED / SURVIVES
unresolved evidence reference                        EXTERNAL RESOLUTION REQUIRED / SURVIVES
copied semantic source with simple renaming          SIMILARITY + PROVENANCE CHECK / SURVIVES
shared project semantic module                       FORBIDDEN / SURVIVES
dynamic opposite-path import during module import    COLD-IMPORT AUDIT / SURVIVES
dynamic opposite-path import during execution        CACHE EVICTION + RUNTIME AUDIT / SURVIVES
opposite-path object hidden in module globals        GLOBAL ORIGIN CHECK / SURVIVES

self-reported isolation only                         INSUFFICIENT / SURVIVES
other-path temp-file read                            BREAKER AUDIT/TRAP BOUNDARY / SURVIVES
other-path environment canary read at import         TRACKED / SURVIVES
other-path environment canary read at runtime        TRACKED / SURVIVES
network/socket semantic leak                         AUDITED/FORBIDDEN / SURVIVES
subprocess semantic leak                             AUDITED/FORBIDDEN / SURVIVES
cached opposite module hiding import                 EVICTED BEFORE AUDIT / SURVIVES

status-axis collapse                                 FORBIDDEN / SURVIVES
semantic BLOCKED emits partial universe              FORBIDDEN / SURVIVES
strict duplicate collapse                            BREAKER ATTACKED / SURVIVES
timestamp regression silently sorted/rejected        BREAKER ATTACKED / SURVIVES
zero/crossed price hidden filter                     BREAKER ATTACKED / SURVIVES
finite negative volume hidden filter                 BREAKER ATTACKED / SURVIVES
local REJECT RECORD accounting loss                  BREAKER ATTACKED / SURVIVES
source→logical mapping mutation                      BREAKER ATTACKED / SURVIVES
missing determinant filled by default                FORBIDDEN / SURVIVES
filename used for missing hour provenance            FORBIDDEN / SURVIVES

invalid result seal                                  DETECTED / SURVIVES
I_A-only semantic mutant                             PAIR BREAKER DETECTION ENCODED / SURVIVES
I_B-only semantic mutant                             PAIR BREAKER DETECTION ENCODED / SURVIVES
result byte hash used as semantic equality           FORBIDDEN / SURVIVES
O/other result used as construction input            INPUT SURFACE FORBIDDEN / SURVIVES

download/acquisition surface                         FORBIDDEN / SURVIVES
real backtest surface                                FORBIDDEN / SURVIVES
broker/live authorization                            FORBIDDEN / SURVIVES
```

No additional internal breaker/harness defect was demonstrated.

The boundary still does not claim a mathematical proof that two independently authored implementations can never share a conceptual mistake. The test-first layer closes the demonstrated execution/provenance shortcuts and preserves the governed requirement for independent derivation + adversarial semantic comparison.

## 13. Final verdict

```text
I_A/I_B TEST-FIRST BREAKER / HARNESS LAYER
PASS
```

This PASS is strictly limited to the persisted test-first qualification layer.

It does **not** promote:

```text
I_A = PASS
I_B = PASS
F/O = PASS
FINAL EXECUTABLE GATE = PASS
```

Official implementation gates remain:

```text
I_A = BLOCKED
I_B = BLOCKED
```

because the production implementation candidates and I_B derivation evidence artifacts do not yet exist.

No real acquisition, BI5 processing or backtest is authorized.
