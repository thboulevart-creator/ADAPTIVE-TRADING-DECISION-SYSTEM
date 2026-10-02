# P5-E V0.1 — FINAL PRE-ADOPTION EVIDENCE HYGIENE — INTERNAL ADJUDICATION

Date: 2026-10-02

## Opening identity

Branch:
`feat/obsidian-projection-p5e-v0.1-final-pre-adoption-evidence-hygiene`

Opening HEAD:
`148c68cb43e77ebff9fb98af91109668b949d62f`

Opening worktree:
`CLEAN`

Contract blob:
`7e3e18ba946246065b43bc5fbabdc35980140eb9`

Model blob:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`

Evidence matrix blob:
`88e13a447a96455d4ac1d9d0f96e11b29329616d`
## External re-review result

External verdict:
`PASS_WITH_NON_BLOCKING_NOTES`

Blocking findings:
`NONE`

The reviewer independently reconstructed the candidate identities and reported:
- P5-E surface: 61 / 61 PASS;
- D2: 55 / 55 PASS;
- the 22 distinct tests referenced by the evidence matrix passed;
- BB1 semantic sweep excluding object-binding tests: only the 13 preregistered non-normative leaves survived.

Therefore:
`BB1_EXTERNAL_CLOSURE = PASS`

This external review creates no execution or adoption authority.
## N1 — read completion before attempt start

Adjudication:
`VALID — CLOSE BEFORE HUMAN ADOPTION`

Current runtime behavior is correct:
`READ_COMPLETION_PRECEDES_ATTEMPT_START`

However the rule is not represented by a dedicated contract field plus dedicated behavioral test.

Authorized correction:
- add one explicit contract field;
- add one strict guard for that field;
- add one behavioral test demonstrating fail-closed behavior.

No model behavior change is required.

## N2 — provenance label for newly added D2-file test

Adjudication:
`VALID — CLOSE BEFORE HUMAN ADOPTION`

The two evidence-matrix entries using:
`ObserverTickTests.test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation`

currently label it:
`REUSED_QUALIFIED_P5D2_P5D4`

That is provenance-overstated because the test was introduced by the BB1 closure.

Authorized correction:
`evidence_kind = DIRECT_P5E`
for those two entries only.
## N3 — mutation-sweep reporting

Adjudication:
`VALID — DOCUMENTARY CORRECTION`

The previous wording conflated two different measurements.

Correct reporting must distinguish:

```text
SEMANTIC SWEEP WITHOUT CONTRACT/MODEL BINDING TESTS
= 13 survivors
= all preregistered non-normative metadata

FULL SURFACE WITH CONTRACT/MODEL BINDING
= 0 survivors
```

The first measurement demonstrates semantic guard coverage.

The second demonstrates object-identity binding.

No claim that "0 survivors exceeds the semantic criterion" is permitted.

## N4 — added-key mutation coverage

Adjudication:
`VALID — DEFERRED`

Current object binding prevents silent drift of added keys.

Closed-schema / unexpected-key rejection is useful hardening but is not required to close the present candidate.

Record as a prerequisite before REAL P5-E.

No mutation authorized here.
## N5 — equality and boundary semantics

Adjudication:
`VALID — DEFERRED`

Examples include:
- `> / >=` at overrun and overlap boundaries;
- source release exactly on a slot;
- exact feasibility at the 60-second boundary;
- first-slot rounding for non-aligned releases;
- uppercase SHA acceptance.

Current behavior is coherent but not exhaustively frozen by dedicated tests.

These boundaries are mandatory hardening before REAL P5-E.

No mutation authorized here.

## N6 — stale matrix construction metadata

Adjudication:
`VALID — CLOSE BEFORE HUMAN ADOPTION`

Current:
`built_against_head = 95881afe5f03783de3c933d2c8ee65373220f3ed`

This is stale and conflicts with the newer object bindings.

Authorized correction:
remove the stale `built_against_head` field.

Do not replace it with the final branch HEAD, because that would make the matrix self-referential and mechanically unstable.

Object identity authority remains:
- `covered_contract_blob`;
- `covered_model_blob`.
## N7 — full re-break evidence scope

Adjudication:
`VALID LIMITATION — NO CURRENT CORRECTION`

The previous authorized full-suite budget is already consumed.

No new full-suite is authorized by this hygiene pass.

The reviewer limitation that 282/282 and 1486/1486 were not independently reproducible is preserved as a provenance note only.

## N8 — P5-A future-design-debt metadata classification

Adjudication:
`NON_MATERIAL_FOR_CURRENT_ADOPTION`

The field:
`queue_and_supersession.p5a_supersession_intent_preserved_as_future_design_debt`

does not grant current behavioral authority.

It remains non-normative metadata in this closure.

## Deferred earlier findings

NB2, NB3, NB5 and NB9 remain deferred exactly as previously recorded.

This hygiene pass does not reopen them.
## Real P5-D4 fingerprint before hygiene

```text
observer-events.jsonl
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

observer-checkpoint.json
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

## Authorized delta only

This pass may modify only:
- P5-E contract fields/tests needed for N1;
- evidence-matrix labels/metadata needed for N2/N6;
- documentary evidence needed for N3;
- mechanically necessary blob bindings;
- targeted tests/reports/delta-review packet.

It may not run another full Obsidian suite.

## Current boundary

```text
BB1_EXTERNAL_REREVIEW = PASS_WITH_NON_BLOCKING_NOTES
N1 = IN_SCOPE
N2 = IN_SCOPE
N3 = IN_SCOPE_DOCUMENTARY
N6 = IN_SCOPE
N4 = DEFERRED_BEFORE_REAL_P5E
N5 = DEFERRED_BEFORE_REAL_P5E
N7 = NO_ACTION
N8 = NO_ACTION

REAL_P5E = CLOSED
HUMAN_NORMATIVE_ADOPTION = CLOSED
```
