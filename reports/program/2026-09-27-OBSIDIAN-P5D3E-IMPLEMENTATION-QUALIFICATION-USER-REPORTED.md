# OBSIDIAN P5-D3E — IMPLEMENTATION QUALIFICATION

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following local Windows execution result was supplied by the user.
It was not independently executed by the assistant.

## Qualified functional candidate

Exact P5-D3E implementation candidate:

    7c6ecec2498d48c4623ecd40aed6c3816f4930b9

Branch:

    feat/obsidian-projection-p5d3e-real-exact-head-sandbox-implementation-v0.1

Evidence-only commits after this candidate do not replace the tested functional candidate.

## Qualified contract and predecessor

P5-D3E contract blob:

    ae4b1691fae16fcd1616e265a089670b9654db4a

Qualified P5-D3D evaluator blob:

    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

## Qualified implementation artifacts

P5-D3E runtime harness:

    tools/obsidian_projection/p5d3e_verify.py
    blob: bd7f63b08432a53eaff5deeb2147396eb60d723f

P5-D3E harness tests:

    tests/obsidian_projection/test_p5d3e_verify.py
    blob: fe47910cf7f10a09021d958d7ae60693d0def4bf

P5-D3E adversarial tests:

    tests/obsidian_projection/test_p5d3e_adversarial.py
    blob: 6b159ede31fb26ac366f9c69cd72256ee553753c

## Reported full regression result

The user reported:

    Ran 1058 tests in 25.564s
    OK

    P5D3E_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN_AFTER_TESTS=PASS

This directly supports successful completion of the full tests/obsidian_projection regression on the qualified implementation candidate and a source-clean control checkout after tests.

## Reported pre-resolved synthetic sandbox qualification

The user reported execution of exactly three focused P5-D3E sandbox tests:

    test_pre_resolved_sandbox_exercises_full_qualified_core ... ok
    test_real_success_status_cannot_be_claimed_without_real_flags ... ok
    test_real_wrapper_is_the_only_path_that_sets_real_context ... ok

Reported result:

    Ran 3 tests in 4.842s
    OK

Final qualification markers:

    P5D3E_PRE_RESOLVED_SYNTHETIC_SANDBOX=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3E_IMPLEMENTATION_QUALIFICATION_COMPLETED=PASS

## Qualified implementation boundary

Within the supplied execution evidence, P5-D3E now qualifies the implementation of:

- the governed exact-head resolver;
- one exact initial branch-resolution fetch path;
- candidate HEAD/TREE freeze semantics;
- local sacrificial clone preparation with --no-hardlinks and --no-checkout;
- local candidate-ref transfer;
- canonical-origin restoration;
- detached exact candidate checkout verification;
- object-store independence checks;
- protected-root / OS-temp boundary checks;
- controlled P5-D2 sandbox activation;
- invocation of the already-qualified P5-D3D finite evaluator;
- post-evaluation Build A / Build B manifest checks;
- post-package P5-D3C2 read-only verification;
- package forbidden-surface checks;
- control/candidate repository cleanliness checks;
- real-Vault fingerprint protection;
- sandbox cleanup;
- separation between synthetic pre-resolved success and real exact-head success.

## Critical synthetic safety properties demonstrated

The focused synthetic qualification demonstrated that:

- the pre-resolved path can exercise the complete qualified core;
- the pre-resolved path cannot claim PASS_REAL_EXACT_HEAD_FINITE_EVALUATION;
- only the real wrapper can set the internal real_context path;
- source-clean state is preserved after the run.

## Explicit limitation preserved

This qualification does NOT establish that the current real integration/system-v1 candidate passes P5-D3E.

No real exact-head evaluation result is established by this qualification report.

The real branch candidate still has to be resolved at run time and then evaluated through the qualified harness.

## Real-run outcome semantics now authorized

The next governed execution may resolve one exact real integration/system-v1 HEAD and evaluate it.

PASS is possible only if:

    candidate_outcome = QUALIFIED

and all real-path invariants hold, including:

    candidate_generation_verification_status =
    PASS_SEALED_UNPROMOTED

    metadata_only_body_read_count = 0

    artifact_record_count = source_record_count

    Build A projection tree = Build B projection tree

    package reverification PASS

    package reverification digest matches evaluator report

    P5-D2 result event emitted

    live projection unchanged

    candidate repository clean after

    control repository clean after

    real Vault unchanged

    current_pointer_created = false

    production_promotion_authorized = false

If the real candidate is rejected:

    FAIL_REAL_CANDIDATE_REJECTED

If infrastructure/evidence blocks classification:

    BLOCKED_REAL_EXACT_HEAD_EVALUATION

Neither outcome is P5-D3E PASS.

## Explicit non-authorizations preserved

Even after successful P5-D3E implementation qualification, the following remain unauthorized:

- production promotion;
- CURRENT pointer mutation;
- real Vault writes;
- background observer execution;
- polling;
- Windows startup/task/service persistence;
- Graph/Search CURRENT semantics.

## Verdict

**PASS — P5-D3E IMPLEMENTATION QUALIFIED ON PRE-RESOLVED SYNTHETIC SANDBOX**

Evidence basis:

    USER-REPORTED LOCAL EXECUTION

This is not independent local execution by the assistant.

## Next governed action

Execute the first real P5-D3E exact-head qualification run:

    resolve_real_candidate()
        ↓
    one governed fetch of integration/system-v1
        ↓
    freeze exact candidate HEAD/TREE
        ↓
    run_real_exact_head_qualification()
        ↓
    QUALIFIED / REJECTED / BLOCKED

No production publication mechanism becomes authorized by that run.
