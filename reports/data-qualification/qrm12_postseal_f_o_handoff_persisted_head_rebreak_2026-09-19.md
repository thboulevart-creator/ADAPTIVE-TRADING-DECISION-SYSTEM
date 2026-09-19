# Q-RM-12 — POST-SEAL I_A/I_B → F/O HANDOFF — PERSISTED-HEAD FINAL RE-BREAK

**Date:** 2026-09-19  
**Exact candidate HEAD re-broken:** `886567839e13f7b53109b337c411acd1d1c91ec3`  
**Candidate:** `reports/data-qualification/qrm12_postseal_f_o_handoff_formalization_candidate_2026-09-19.md`  
**Candidate blob:** `a1f1c0edf6f45fd96620e3f2274cc9da0214e3f7`

Scope is formalization/documentary qualification only.

No Q-RM-12 runtime, adapter, shared semantic builder, F/O/I_A/I_B production modification, BI5 acquisition, BI5 processing, backtest, paper/broker/live execution or positive P1.1 authorization was used.

## 1. Re-break target

The persisted candidate selects:

```text
same immutable inputs
        ↓                 ↓
 independent I_A     independent I_B
        ↓                 ↓
 path-private F_A    path-private F_B
        ↓                 ↓
 sealed V0.2 result  sealed V0.2 result
        \                 /
         Q-RM-12 post-seal ingress
                  ↓
    pinned producer/run/output validation
                  ↓
      shared F validation post-seal only
                  ↓
             extract F_A/F_B
                  ↓
        existing O comparator unchanged
```

The current V0.1 I_A/I_B implementation candidates remain qualified only at their existing scope and are explicitly BLOCKED for Q-RM-12 compatibility.

## 2. Persisted attack matrix

### R1 — V0.1 fields used to reconstruct F after seal

Required outcome:

```text
FORBIDDEN
```

Observed formalized rule:

- V0.1 is insufficient;
- post-seal F construction/completion/repair is forbidden;
- a version-forward result must embed exact F pre-seal.

Result:

`PASS`

### R2 — common package supplies trusted complete-slot count / terminal fragment

Required:

`FORBIDDEN`

Observed:

- common package supplies raw declared payload plus D/normative bindings;
- complete-slot count and terminal-fragment semantics are independently derived by each path.

Result:

`PASS`

### R3 — both paths share one project semantic F builder

Required:

`FORBIDDEN`

Observed:

- pre-seal F construction must remain path-private and independently implemented.

Result:

`PASS`

### R4 — both paths share one project semantic F validator/normalizer pre-seal

Required:

`FORBIDDEN`

Observed:

- pre-seal semantic validation must also remain path-private;
- the existing shared F validator is permitted only after both seals exist.

Result:

`PASS`

### R5 — shared schema contains semantic defaults/builders

Required:

`FORBIDDEN`

Observed:

- only pure structural schema sharing is allowed;
- no semantic defaults, computed fields, normalization, builder/factory or repair behavior.

Result:

`PASS`

### R6 — changed Q-RM-12-compatible code reuses V0.1 implementation version

Required:

`FORBIDDEN`

Observed:

- both I_A and I_B implementation identities/manifests must version-forward independently;
- V0.1 PASS cannot authorize changed V0.2 behavior.

Result:

`PASS`

### R7 — self-labelled implementation result claims qualified producer identity

Required:

`REJECT`

Observed:

- ingress requires externally pinned implementation id/version, manifest digest and source/blob identity;
- result-local manifest claim cannot create its own pin.

Result:

`PASS`

### R8 — correct source executes, but a different resealed output is substituted afterward

Required:

`REJECT`

Observed:

- external run/sealing evidence must bind exact emitted `result_seal`;
- presented result seal must equal the run-bound seal.

Result:

`PASS`

### R9 — stale F artifact substituted into a qualified result

Required:

`REJECT`

Observed:

- exact F artifact is embedded inside the sealed result;
- substitution changes the result payload/seal;
- run receipt binds exact emitted seal;
- post-seal F validator and result/F cross-binding still apply.

Result:

`PASS`

### R10 — F_A/F_B mix-and-match between path results

Required:

`REJECT`

Observed:

- each F artifact is embedded before its own path seal;
- each result seal is separately run-bound;
- acquisition/result/reconstruction bindings are checked separately before O.

Result:

`PASS`

### R11 — artifact integrity digest used as semantic equality

Required:

`FORBIDDEN`

Observed:

- result/F hashes are integrity only;
- O semantic projection remains the only qualified-universe semantic comparator.

Result:

`PASS`

### R12 — result seal used as producer authentication

Required:

`FORBIDDEN`

Observed:

- candidate explicitly classifies result seal as non-secret integrity only;
- producer/run identity comes from external pinned evidence.

Result:

`PASS`

### R13 — boolean/number or non-finite ambiguity in result-seal normal form

Required:

`REJECT / DISTINGUISH STRICT JSON TYPES`

Observed:

- strict canonical JSON is required;
- non-finite values rejected;
- JSON type distinctions preserved;
- duplicate object keys rejected at serialized ingress.

Result:

`PASS`

### R14 — legitimate different version masks later same-version integrity conflict

Required:

`INTEGRITY CONFLICT HAS PRECEDENCE`

Observed:

- all same-id/same-version stages D/R/M/B/A/Q/F/O are scanned for reference/integrity conflicts first;
- only then may legitimate version difference classify a non-same-state run.

Result:

`PASS`

### R15 — O determinant mismatch while F_A/F_B otherwise match

Required:

`NO O INVOCATION AS SAME-STATE RUN`

Observed:

- O is included in sealed complete determinant bindings;
- same-state gate checks D/R/M/B/A/Q/F/O before O invocation.

Result:

`PASS`

### R16 — result/F acquisition identity mismatch

Required:

`REJECT`

Observed:

- result materialized acquisition id must equal F qualified-universe acquisition-domain id.

Result:

`PASS`

### R17 — result determinant binding differs from F reconstruction tuple

Required:

`REJECT`

Observed:

- D/R/M/B/A/Q/F sealed bindings must exactly match corresponding F reconstruction bindings.

Result:

`PASS`

### R18 — QUALIFIED result has no exact F artifact

Required:

`REJECT`

Observed:

- `COMPLETED + QUALIFIED + FROZEN` requires a valid exact embedded F artifact.

Result:

`PASS`

### R19 — terminal/non-reached result carries synthetic qualified F artifact

Required:

`REJECT`

Observed:

- QUALIFICATION_BLOCKED, ACQUISITION_REJECTED, ENVIRONMENT_BLOCKED and IMPLEMENTATION_ERROR require `bound_f_artifact = null`;
- no qualified universe is synthesized.

Result:

`PASS`

### R20 — both terminal paths are normalized into semantic PASS

Required:

`FORBIDDEN`

Observed:

- terminal states may be recorded separately;
- no qualified-universe equality PASS exists without two qualified frozen F artifacts.

Result:

`PASS`

### R21 — one-sided I_A mutant hidden by a shared post-seal bridge

Required:

`OBSERVABLE`

Observed:

- no semantic bridge/normalizer exists;
- I_A's exact sealed F_A reaches O unchanged after validation.

Result:

`PASS`

### R22 — one-sided I_B mutant hidden by a shared post-seal bridge

Required:

`OBSERVABLE`

Observed:

- same property independently applies to F_B.

Result:

`PASS`

### R23 — source witness / traversal order / serialization order promoted to authority

Required:

`FORBIDDEN`

Observed:

- candidate explicitly lists these as non-authorities;
- O remains responsible for governed semantic comparison.

Result:

`PASS`

### R24 — opposite path output becomes readable before seal

Required:

`FORBIDDEN`

Observed:

- post-seal coordinator read policy activates only after both seals exist;
- private workspaces may not be used to fill handoff gaps.

Result:

`PASS`

### R25 — Q-RM-12 coordinator repairs or completes missing F fields

Required:

`FORBIDDEN`

Observed:

- ingress is validation/extraction only;
- missing semantics block rather than being reconstructed.

Result:

`PASS`

### R26 — shared F validator feeds acceptance/normalization back into pre-seal execution

Required:

`FORBIDDEN`

Observed:

- shared F validation occurs only after both results are sealed.

Result:

`PASS`

### R27 — direct O invocation on sealed result objects rather than exact F artifacts

Required:

`FORBIDDEN`

Observed:

- Q-RM-12 extracts exact embedded F_A/F_B after validation;
- existing O receives only `compare_freeze_artifacts(F_A, F_B)`.

Result:

`PASS`

### R28 — permission leakage from formalization

Required:

`NONE`

Observed:

- no acquisition, BI5 processing, backtest, paper/broker/live or positive P1.1 authorization is created.

Result:

`PASS`

## 3. Residual limitations intentionally preserved

This formalization does **not** prove:

- that a future V0.2 I_A implementation is correct;
- that a future V0.2 I_B implementation is independently derived;
- that their future pre-seal F builders/validators are correct;
- that a future Q-RM-12 runtime is correct;
- that a real materialized acquisition can pass D/R/M/B/A/Q/F/O;
- that a real same-state determinism run exists.

Those require future test-first executable qualification.

No formalization text can substitute for those executions.

## 4. Final formalization verdict

No residual internal handoff-model defect was demonstrated by the persisted-head documentary re-break.

Therefore:

```text
Q-RM-12 POST-SEAL I_A/I_B → F/O HANDOFF FORMALIZATION = PASS
```

This PASS is strictly a **formalization-layer PASS**.

The executable/global state remains:

```text
I_A V0.1 implementation candidate = PASS at existing scope
I_B V0.1 implementation candidate = PASS at existing scope
I_A Q-RM-12 compatibility         = BLOCKED
I_B Q-RM-12 compatibility         = BLOCKED
Q-RM-12 executable runtime         = ABSENT
Q-RM-12 executable run             = BLOCKED

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

## 5. Next-layer implication

Only after this documentary PASS may the next governed block define a **test-first executable Q-RM-12 compatibility boundary** for the version-forward I_A/I_B result/input schema.

That future block must begin RED and must not create real acquisition/backtest execution.

