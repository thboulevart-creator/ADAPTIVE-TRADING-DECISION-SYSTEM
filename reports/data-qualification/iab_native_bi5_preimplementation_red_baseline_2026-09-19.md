# I_A + I_B — NATIVE BI5 PREIMPLEMENTATION RED BASELINE

**Date:** 2026-09-19  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Scope:** test-first executable baseline only — no production I_A/I_B implementation, no real BI5 acquisition/processing, no backtest.

## 1. Governed boundary

Qualified implementation-boundary candidate:

`reports/data-qualification/iab_native_bi5_implementation_boundary_candidate_2026-09-19.md`

Corrected boundary blob:

`fac8d143a836b0c02538c607ac5ab71357824537`

Boundary adversarial re-break blob:

`6653953562ffaa5f7d8ff23578356ab794f37827`

Test-first harness adversarial artifact:

`reports/data-qualification/iab_native_bi5_testfirst_harness_adversarial_break_2026-09-19.md`

Final harness adversarial blob:

`13737aef3b3b8fd7e7257c0e731719965e2e3a23`

Harness verdict:

```text
I_A/I_B TEST-FIRST BREAKER / HARNESS LAYER = PASS
```

Implementation verdicts remain:

```text
I_A = BLOCKED
I_B = BLOCKED
```

---

## 2. Final breaker/workflow identities

```text
I_A breaker
breakers/native_bi5_ia_reference_qualifier_breaker.py
blob = 64d3a391e1b5cb5aecfdf926551acd3ee5f0d7dd

I_B breaker
breakers/native_bi5_ib_independent_qualifier_breaker.py
blob = d1a305e3b9ae813e891b34522e3a12bb6bc8ac34

I_A preimplementation workflow
.github/workflows/native-bi5-ia-reference-qualifier-preimplementation.yml
blob = c3325de6f65be5c99f8df5aab19404d1cd627a9a

I_B preimplementation workflow
.github/workflows/native-bi5-ib-independent-qualifier-preimplementation.yml
blob = 02151244113b5654647c529899b11997c8762c66
```

---

## 3. RED-baseline evolution

### Initial baseline

I_A:

```text
run = 35441192904
job = 105892147172
errors = 20
cause = missing src.native_bi5_reference_qualifier only
```

I_B:

```text
run = 35441243836
job = 105892281429
errors = 19
cause = missing src.native_bi5_independent_qualifier only
```

### After first harness correction

I_A:

```text
run = 35441467755
job = 105892871250
errors = 21
cause = missing src.native_bi5_reference_qualifier only
```

I_B:

```text
run = 35441467767
job = 105892871359
errors = 21
cause = missing src.native_bi5_independent_qualifier only
```

### After second harness correction

I_A:

```text
run = 35441590246
job = 105893220295
errors = 23
cause = missing src.native_bi5_reference_qualifier only
```

I_B:

```text
run = 35441590283
job = 105893220419
errors = 23
cause = missing src.native_bi5_independent_qualifier only
```

### Final persisted-head RED baseline

Persisted candidate HEAD:

`331f48ad4080daf1b41f69dddb559e6820cbcff0`

I_A:

```text
run = 35441702806
job = 105893512667
workflow conclusion = failure
breaker errors = 23
sole breaker cause =
src.native_bi5_reference_qualifier absent
```

I_B:

```text
run = 35441702856
job = 105893512796
workflow conclusion = failure
breaker errors = 23
sole breaker cause =
src.native_bi5_independent_qualifier absent
```

For both final workflows:

```text
exact persisted HEAD/hash locks          PASS
expected production module absence      PASS
locked qualification packages           PASS
qualification environment verification  PASS
breaker execution                       EXPECTED RED
clean worktree                           PASS
```

No syntax, test collection, environment, workflow or hash-lock defect caused the RED state.

---

## 4. Test-first attack surface frozen

The final breakers encode attacks for:

```text
status-axis violations
partial-universe leakage
strict duplicate collapse
timestamp sorting / temporal authority leakage
zero/crossed-price hidden filtering
finite-negative-volume hidden filtering
source→logical mapping corruption
local record-reject accounting loss
missing normative determinants / defaults
filename-derived hour provenance
implementation manifest/source integrity
shared semantic imports/dependencies
fake independent derivation
source-copy/structural similarity
unresolved derivation-evidence references
import-time opposite-path dependencies
runtime dynamic opposite-path dependencies
module-global opposite-path aliases
pre-seal temp/file information leakage
pre-seal environment leakage
pre-seal network / IPC / subprocess leakage
cached-module import bypass
invalid result sealing
O/other-path result used as construction input
I_A-only semantic mutant
I_B-only semantic mutant
result byte hash used as semantic equality
permission leakage
```

All fixtures are synthetic/in-memory except breaker-owned temporary test artifacts created by pytest when future runtimes exist.

No provider data is needed for this test-first layer.

---

## 5. Harness defects found and corrected

Initial adversarial defects:

```text
IAB-TF-F01 — SELF_ATTESTED_INDEPENDENCE_EVIDENCE
IAB-TF-F02 — SELF_REPORTED_ISOLATION_EVIDENCE
IAB-TF-F03 — STATIC_ONLY_SHARED_SEMANTIC_DEPENDENCY_DETECTION
```

Residual re-break defects corrected:

```text
IAB-TF-R01 — UNRESOLVED_EVIDENCE_REFERENCE_TRUST
IAB-TF-R02 — ENVIRONMENT_CHANNEL_NOT_OBSERVED
IAB-TF-R03 — IMPORT_TIME_DYNAMIC_DEPENDENCY_GAP
IAB-TF-R04 — IMPORT_TIME_ENVIRONMENT_LEAK_GAP
IAB-TF-R05 — CACHED_OPPOSITE_MODULE_RUNTIME_AUDIT_BLIND_SPOT
```

Final persisted-head re-break demonstrated no additional internal breaker/harness defect.

---

## 6. What PASS means

```text
I_A/I_B TEST-FIRST BREAKER / HARNESS LAYER = PASS
```

means only:

- the executable attack layer is persistently defined;
- its final RED state is explained solely by absent future production modules;
- demonstrated harness bypasses have been corrected and re-broken;
- the layer is now eligible to govern future implementation work.

It does not mean:

```text
I_A implementation exists
I_B implementation exists
I_A is qualified
I_B is qualified
D/R/M/B/A/Q/F/O are PASS
real data may be acquired
real BI5 may be processed
real backtest may run
```

---

## 7. Official gate state

```text
D   BLOCKED
R   BLOCKED
M   BLOCKED
B   BLOCKED
A   BLOCKED
Q   BLOCKED
F   BLOCKED
O   BLOCKED
I_A BLOCKED
I_B BLOCKED
```

---

## 8. Safety / authorization state

```text
production I_A implementation = ABSENT
production I_B implementation = ABSENT
real BI5 download             = NOT AUTHORIZED
real BI5 processing           = NOT AUTHORIZED
real acquisition              = NOT AUTHORIZED
real backtest                 = NOT AUTHORIZED
paper / broker / live         = NOT AUTHORIZED
positive P1.1 AUTHORIZED      = BLOCKED
```

---

## 9. Closure consequence

The required test-first RED baseline now exists and is persisted.

Production implementation work may therefore become the subject of a **new separately governed block**, but is not performed by this baseline artifact itself.

The safest next implementation order is:

```text
I_A reference implementation first
→ qualify/correct/re-break I_A against the frozen breaker
→ persist I_A state
→ only then open the separately governed I_B independent implementation block
```

I_B must remain derived from the pinned normative contracts and its own derivation evidence, not from copying or wrapping I_A source.
