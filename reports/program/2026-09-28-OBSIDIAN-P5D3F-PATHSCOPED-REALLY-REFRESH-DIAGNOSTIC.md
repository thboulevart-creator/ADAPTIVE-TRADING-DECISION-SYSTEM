# OBSIDIAN P5-D3F — PATHSCOPED REALLY-REFRESH CAUSAL DIAGNOSTIC

Date: 2026-09-28

## Evidence status

USER-REPORTED LOCAL EXECUTION / DIAGNOSTIC.

Not independent execution evidence.

## Branch state before persistence

Verified remote HEAD:

    61b174f87dc5eea8432699231522674b20779891

## Experiment

Two temporary copies of the same real Git index were used through GIT_INDEX_FILE.

Representative path:

    tools/obsidian_projection/promotion_handoff_contract_v0_1.json

A — whole-index refresh:

    git update-index --really-refresh

Observed:

    A_REFRESH_EXIT=1
    A_STAGE_UNCHANGED=True
    A_STATUS_AFTER=.M

B — path-scoped refresh:

    git update-index --really-refresh -- <representative-path>

Observed:

    B_REFRESH_EXIT=1
    B_STAGE_UNCHANGED=True
    B_STATUS_AFTER=<clean>

The real index SHA-256 remained identical before and after the experiment:

    REAL_INDEX_UNCHANGED=True

## Adjudication

The pathscope variable is causally discriminant for the representative file:

- whole-index --really-refresh did not clear the dirty classification;
- path-scoped --really-refresh did clear it;
- staged mode/OID/stage remained unchanged.

Therefore the prior V6 strategy of whole-index refresh is invalidated.

Supported next correction shape:

    exact committed-blob materialization
    -> verify raw worktree blob equality
    -> path-scoped index stat refresh for the bounded preregistered byte-pin paths
    -> verify complete staged mode/OID/stage invariance
    -> require clean worktree

## Remaining limitation

This experiment directly demonstrated path-scoped cleanup for one representative compatibility path.

The governed V7 runner must apply the same operation only to the existing bounded compatibility set and must still require the final complete worktree to be clean. The full local V7 re-break remains the qualification gate.

No historical expected blob is repinned.
No P5-D3F contract semantic is changed.
No real Vault write is authorized.
