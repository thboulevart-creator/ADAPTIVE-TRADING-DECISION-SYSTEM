# SESSION BACKUP — 2026-09-19 — NATIVE BI5 I_A/I_B TEST-FIRST RED BASELINE

## 0. Purpose

Durable recovery snapshot for the test-first executable qualification layer governing future native-BI5 I_A/I_B implementations.

Repository:

`thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch:

`integration/system-v1`

GitHub and the current Recovery Checkpoint remain authoritative.

No production I_A/I_B runtime was created in this block.

---

## 1. Starting governed state

Starting HEAD:

`ea9104d633d55dc99f4cc2b74a0add305585bd73`

Message:

`checkpoint: persist native BI5 I_A/I_B boundary formalization`

The branch was verified identical before mutation.

The corrected/re-broken implementation-boundary candidate blob remained:

`fac8d143a836b0c02538c607ac5ab71357824537`

Implementation-boundary adversarial blob remained:

`6653953562ffaa5f7d8ff23578356ab794f37827`

Official gates at start:

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

## 2. Initial test-first breakers

### I_A initial breaker

Path:

`breakers/native_bi5_ia_reference_qualifier_breaker.py`

Initial breaker commit:

`ccdf6a8dfc2cb12d0532ab7f92d356665520b79b`

Initial breaker blob:

`b95501729ef7d1282b7915f4895f978e190c5eb6`

Initial workflow commit:

`d96829418520ad726696c827623c19bc512ac282`

Initial RED:

```text
run 35441192904
job 105892147172
20 errors
all due only to absent src.native_bi5_reference_qualifier
```

### I_B initial breaker

Path:

`breakers/native_bi5_ib_independent_qualifier_breaker.py`

Initial breaker commit:

`e526a07da0493327baeb512f4bad98fbf0cd901f`

Initial breaker blob:

`4080b9899ca02f3eea071fb70371f0be5cc80855`

Initial workflow commit:

`58a80df0bd9513cbc0f80c8b24896fedb354f4aa`

Initial RED:

```text
run 35441243836
job 105892281429
19 errors
all due only to absent src.native_bi5_independent_qualifier
```

All pre-breaker controls and clean worktree checks passed.

---

## 3. Breaker/harness adversarial qualification

Adversarial artifact:

`reports/data-qualification/iab_native_bi5_testfirst_harness_adversarial_break_2026-09-19.md`

Initial adversarial commit:

`1353eb2d35d6e2bd4c7d2dc71c98c475e9f4396f`

Initial verdict:

`FAIL`

Demonstrated defects:

```text
IAB-TF-F01 — SELF_ATTESTED_INDEPENDENCE_EVIDENCE
IAB-TF-F02 — SELF_REPORTED_ISOLATION_EVIDENCE
IAB-TF-F03 — STATIC_ONLY_SHARED_SEMANTIC_DEPENDENCY_DETECTION
```

The RED runs themselves were valid, but the future breaker could still be fooled.

---

## 4. First correction + re-break

Correction commit:

`f3df1cdaae1ed55e852df37444ba69ed55a7e069`

Breaker blobs:

```text
I_A = 5509474aed15aad452d38333fa66a3b86224b0f4
I_B = e8f6d3b41a1ecd8acdfb01090d7499cb24d93dea
```

Added:

- breaker-owned runtime audit hooks;
- breaker-owned source-structure similarity review;
- removal of implementation self-authored PASS labels.

RED reruns:

```text
I_A run 35441467755 / job 105892871250 / 21 errors
I_B run 35441467767 / job 105892871359 / 21 errors
```

All errors still only missing runtimes.

Residual defects found:

```text
IAB-TF-R01 — UNRESOLVED_EVIDENCE_REFERENCE_TRUST
IAB-TF-R02 — ENVIRONMENT_CHANNEL_NOT_OBSERVED
IAB-TF-R03 — IMPORT_TIME_DYNAMIC_DEPENDENCY_GAP
```

Residual record commit:

`5b5f96d11e1458f037ac2c6fab39a53b26017736`

---

## 5. Second correction + re-break

Correction commit:

`f495bcb61abff6741ccee23e2dfbd67c4e4300fd`

Breaker blobs:

```text
I_A = 8fd8d141d961a73904215236812c224d5e8af355
I_B = b3c342ecfbbf3c2b68c109762e2b936215a316f2
```

Added:

- exact future I_B evidence-reference paths;
- external JSON evidence validation;
- implementation/version/source-digest evidence binding;
- environment canaries during execution;
- cold-import audit;
- module-global opposite-origin checks.

RED reruns:

```text
I_A run 35441590246 / job 105893220295 / 23 errors
I_B run 35441590283 / job 105893220419 / 23 errors
```

All errors still only missing runtimes.

Residual defects found:

```text
IAB-TF-R04 — IMPORT_TIME_ENVIRONMENT_LEAK_GAP
IAB-TF-R05 — CACHED_OPPOSITE_MODULE_RUNTIME_AUDIT_BLIND_SPOT
```

Residual record commit:

`b2bcfd01ceadbf0acb6c89b26b67749f0d63a12e`

---

## 6. Third correction + final persisted-head re-break

Third correction persisted HEAD:

`331f48ad4080daf1b41f69dddb559e6820cbcff0`

Final breaker/workflow blobs:

```text
I_A breaker
64d3a391e1b5cb5aecfdf926551acd3ee5f0d7dd

I_B breaker
d1a305e3b9ae813e891b34522e3a12bb6bc8ac34

I_A workflow
c3325de6f65be5c99f8df5aab19404d1cd627a9a

I_B workflow
02151244113b5654647c529899b11997c8762c66
```

Third correction added:

- cold-import environment canary/tracking;
- opposite-module `sys.modules` eviction before audited semantic execution;
- explicit proof that candidate import did not preload the opposite implementation;
- workflow hash-lock updates.

Final RED runs:

```text
I_A
run 35441702806
job 105893512667
23 errors
sole cause = missing src.native_bi5_reference_qualifier

I_B
run 35441702856
job 105893512796
23 errors
sole cause = missing src.native_bi5_independent_qualifier
```

For both runs:

```text
persisted HEAD/hash locks        PASS
expected runtime absence         PASS
qualification environment        PASS
breaker                          EXPECTED RED
clean worktree                   PASS
```

No additional internal breaker/harness defect was demonstrated.

Final adversarial re-break persistence commit:

`5873767377f7374566a7c8319f22211965fe096a`

Final adversarial artifact blob:

`13737aef3b3b8fd7e7257c0e731719965e2e3a23`

---

## 7. Durable RED baseline

Baseline artifact:

`reports/data-qualification/iab_native_bi5_preimplementation_red_baseline_2026-09-19.md`

Baseline commit:

`cd543e463593a182d6bdb3e69860080b6c7500af`

Baseline blob:

`18393a03b39a54433ad85e0236c217e41fdcfd6e`

Global reconciliation audit update commit:

`f49062965a3269a0440d6b3e25f1484019cb8551`

Global audit blob:

`06ae81c3715b11ae9a3c7dbf30c3942054e53b90`

---

## 8. Final verdict of this block

```text
I_A/I_B TEST-FIRST BREAKER / HARNESS LAYER = PASS

I_A = BLOCKED
I_B = BLOCKED
```

The PASS is limited to the persisted qualification harness and RED baseline.

No production implementation exists yet.

---

## 9. Safety truth

```text
production I_A module          = ABSENT
production I_B module          = ABSENT
I_B derivation evidence files  = ABSENT / future implementation requirement

real data acquisition          = NOT AUTHORIZED
native BI5 download            = NOT AUTHORIZED
real BI5 processing            = NOT AUTHORIZED
massive acquisition            = NOT AUTHORIZED
real backtest                  = NOT AUTHORIZED
positive P1.1 AUTHORIZED       = BLOCKED
paper / broker / live          = NOT AUTHORIZED
```

---

## 10. Do not repeat

Do not:

- rebuild the test-first breakers from scratch;
- remove the environment/import/cache isolation attacks;
- replace breaker-owned evidence adjudication with implementation self-claims;
- weaken the structural-copy attack to make I_B easier to implement;
- create I_B as a wrapper/copy/port of I_A;
- download BI5 or run a real backtest merely because the harness is PASS.

---

## 11. Exactly one next governed action

Open only the **I_A reference implementation candidate** block.

Create:

`src/native_bi5_reference_qualifier.py`

only from the pinned D/R/M/B/A/Q/F candidate contracts and the now-frozen I_A breaker.

Do not create I_B yet.

The I_A block must follow:

```text
fresh HEAD verification
→ implement minimal I_A candidate
→ run I_A breaker
→ adversarially diagnose failures
→ minimal corrections only
→ persisted-head I_A re-break
→ PASS / FAIL / BLOCKED
→ audit + backup + checkpoint
```

Do not consult or derive future I_B source from I_A implementation.

No real acquisition, BI5 data processing or backtest is authorized in the I_A block; synthetic/in-memory fixtures remain the execution boundary.
