# RPE-04 — RPE-03 V0.2 REBIND + NF-2 + NF-3 — FINAL TEST EXECUTION EVIDENCE

Date: 2026-10-05

## Execution protocol

Tests were executed locally on Windows through a bounded detached runner under:

C:\Users\Boulevart\ATDS-CONTROL\BOUNDED-TEST-RUNNER

The runner:
- launches each test family in a separate process;
- writes stdout/stderr and completion state to disk;
- imposes a Windows-side hard timeout;
- does not rely on the chat transport remaining open;
- avoids overlapping ATDS test executions.

No GitHub polling or external-network qualification occurred.

## Targeted closure evidence

### RPE-03 V0.2 rebind + NF-2

Suite:
tests.obsidian_projection.test_rpe04_rpe03v02_rebind_nf2_v0_1

Result:
5 / 5 PASS

This covers:
- exact binding to the human-adopted RPE-03 V0.2 classifier;
- governed absolute Git path handoff;
- exact observation-ref identity without peeling;
- annotated-tag laundering rejection;
- normal commit-ref success.

### NF-3 full physical Git-domain containment

Suite:
tests.obsidian_projection.test_rpe04_nf3_full_physical_domain_v0_1

Result:
7 / 7 PASS

This covers:
- normal bare repository acceptance;
- recursive indirection rejection;
- refs and refs/rpe04 containment;
- config / HEAD / packed-refs containment;
- alternates rejection;
- pack/index-level indirection where representable;
- post-fetch containment revalidation before positive authority.

### Runtime-binding hardening after RPE-03 V0.2 rebind

Suite:
tests.obsidian_projection.test_rpe04_runtime_binding_hardening_v0_1

Result:
5 / 5 PASS

The only historical-test correction was the expected raw SHA-256 rebind from the adopted RPE-03 V0.1 runtime dependency to the adopted RPE-03 V0.2 runtime dependency. The security requirement and failure mode were unchanged.

### NF-2 / NF-3 mutation discrimination

Suite:
tests.obsidian_projection.test_rpe04_rpe03v02_nf2_nf3_mutation_v0_1

Result:
3 / 3 PASS

Mutations discriminate:
- reintroduction of observed-tip peeling;
- removal of alternates rejection;
- removal of recursive physical-indirection rejection.

## RPE-04 dedicated regression

Discovery pattern:
test_rpe04*.py

Result:
55 / 55 PASS

This includes the current RPE-04 adapter, legacy mutation surface, runtime-binding hardening, RPE-03 V0.2 rebind, NF-2, NF-3 and final targeted mutation coverage.

## Protected predecessor regressions

### RPE-03 final qualified surface

An initial broad discovery of all test_rpe03*.py files executed 62 tests and produced one error in:

test_rpe03_v02_bf1_prime_executable_identity_closure_v0_1.py

That file is a historical intermediate BF-1 PRIME closure test whose direct _run_git expectation predates the final canonical-path hardening. It is not part of the final 59-test qualified RPE-03 V0.2 surface.

The final qualified surface was reconstructed exactly as:
- every current RPE-03 qualified test module;
- excluding the historical 4-test intermediate closure file above;
- including the 1-test RPE-04 call-site compatibility harness.

Arithmetic:
62 - 4 + 1 = 59

Exact final replay result:
59 / 59 PASS

No RPE-03 file was modified during this regression.

### RPE-02

Discovery pattern:
test_rpe02*.py

Result:
51 / 51 PASS

### RPE-01

Discovery pattern:
test_rpe01*.py

Result:
46 / 46 PASS

### P5-E

Discovery pattern:
test_p5e*.py

Result:
67 / 67 PASS

## Protected identity checks

RPE-01 governed schema guard:
26f977961d72a062199d71ffd628d5a5cc047887

RPE-02 real-time model:
31db5d944a25e54db81bd901a087cdc2039925ad

RPE-03 V0.1 historical classifier:
145b3112fd9309cc34d95a62c091cb6a6bc3bb11

RPE-03 V0.2 human-adopted classifier:
5bbe455418fe1396ee5824379ad7450a1379cbba

P5-E contract:
43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9

P5-E synthetic timing model:
c0f16baa151c1466e30ba5778f1fca8184cd4aac

P5-D4 runtime:
1825e53d195ba2a63b5b646a5b78eb77939b94b5

All match the protected expected identities.

## Final RPE-04 candidate

Implementation Git blob:
e188414cd433f839d5efbe5d28840d7acf4938d5

Implementation raw SHA-256:
1300e60a5cd353557cc16779a372979b436fcacfeb082435cd749987342d1638

RPE-03 V0.2 classifier raw SHA-256:
4b743e187245585f4a4d9c923e316961f2842f96634d04dcac01972a29e60b41

Closure preregistration raw SHA-256:
4c6c156c2bde72ed83b360a3ddccaf97a46b55b45cd107c85e32d998ef95cf11

## Claim boundary

This evidence supports only the local-only RPE-04 closure candidate.

It does not qualify:
- production GitHub polling;
- production remote observation;
- RPE-02 failure-event handoff NF-4;
- RPE-05;
- RPE-06;
- REAL P5-E;
- promotion/publication;
- Vault/CURRENT;
- persistent services.

RPE-04 human adoption remains pending external review and a separate human decision.
