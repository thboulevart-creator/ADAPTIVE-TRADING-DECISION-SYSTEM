# OBSIDIAN P5-D3F — V7 PATHSCOPED INDEX STAT RECONCILIATION STATIC REVIEW

Date: 2026-09-28

## Evidence status

Same-assistant static review.

Not independent execution evidence.
Does not qualify P5-D3F.

## Triggering evidence

USER-REPORTED LOCAL diagnostics showed:

- exact identity between HEAD, index, raw worktree and filtered worktree blob for the representative P5-D3F contract;
- whole-index `git update-index --really-refresh` left the representative path dirty;
- path-scoped `git update-index --really-refresh -- <path>` cleared it;
- staged mode/OID/stage remained unchanged;
- real index integrity remained unchanged because the causal comparison used temporary index copies.

The separate `git add --refresh` path remained dirty and is rejected as a correction.

## Exact V7 functional candidate

    49eda71d200cca7a860fd9b0d212aa0e94e9cea7

Exact blobs:

Runner:

    18d56b5a2cf1e9fdbd502ce2545f69e685e40e4d

Runner tests:

    4857a0e7eb55caf23071b7cabae3449322433e76

P5-D3F contract unchanged:

    64744325251db350d26c0269090ce62d5fa5f2e8

P5-D3F contract tests unchanged:

    3dc1d7315874d4352eeaf05407f266961c878e70

.gitattributes unchanged:

    e0154899b5640da025a082ef6b02f4bf179d3030

## Test-first sequence

The pathscope breaker was committed before the V7 implementation change.

It requires the runner to issue exactly one:

    git update-index --really-refresh -- <relative-path>

call for each entry in the existing bounded BYTE_PIN_COMPATIBILITY_PATHS tuple.

No new compatibility path was introduced.

## Static implementation review

The runner:

1. preserves the existing exact committed-blob materialization;
2. verifies raw worktree blob identity before attempting stat reconciliation;
3. snapshots all staged mode/OID/stage entries;
4. refreshes only the preregistered bounded compatibility paths, individually;
5. accepts only return code 0 or the observed return code 1;
6. snapshots all staged entries again;
7. rejects any staged representation change;
8. requires the repository to be clean afterwards;
9. continues the existing contract, compile, targeted and full historical re-break controls.

This avoids the invalid V6 whole-index refresh.

## Boundary preservation

No historical expected blob was changed.

No historical test was weakened.

No P5-D3F contract semantic changed.

No `.gitattributes` change was made.

No production handoff runtime was implemented.

No CURRENT mutation was introduced.

No real Vault write was introduced.

## Remaining uncertainty

The causal experiment directly demonstrated path-scoped cleanup for one representative bounded path.

It has not yet demonstrated that sequential path-scoped refresh clears all eight bounded paths in the real Windows qualification checkout.

The existing local checkout is also still carrying the eight stat-only dirty classifications left by V5.

Therefore a bounded real-index recovery, guarded by complete staged-entry invariance, must occur before the governed V7 runner can start from its required clean-worktree precondition.

## Verdict

    STATIC CORRECTION REVIEW = PASS
    V7 FUNCTIONAL CANDIDATE = READY FOR LOCAL GATE
    V7 LOCAL GOVERNED RE-BREAK = NOT YET EXECUTED
    P5-D3F CONTRACT = UNQUALIFIED
    P5-D3F IMPLEMENTATION = UNAUTHORIZED
    P5-D3G = CLOSED
    REAL VAULT WRITE = CLOSED
