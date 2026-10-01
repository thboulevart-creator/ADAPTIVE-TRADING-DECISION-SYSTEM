# P5-E V0.1 — TARGETED REGRESSION QUALIFICATION

Date: 2026-10-01

## Scope

This record consolidates the predecessor and cross-cutting regression evidence before the single preregistered full Obsidian re-break.

No real P5-E execution was performed.

## First targeted predecessor surface

Covered:

- P5-A continuous projection contract;
- P5-D1 observer core;
- P5-D2 one-shot observer tick;
- P5-D4 bounded-loop contract/runtime/adversarial;
- P5-D4 control-root binding base/adversarial;
- P5-E base/adversarial.

The initial run exposed two stale P5-D4 remediation-only assumptions that the production root must remain absent forever.

Those tests were mechanically corrected to reflect the later human-adopted P5-D4 V0.2 lifecycle without weakening binding, reparse, old-root rejection, or cross-interpreter controls.

Post-correction result:

```text
Ran 208 tests in 3.159s

OK
```

## Cross-cutting static/regression surface

Before consuming the one full re-break, 53 test modules containing cross-cutting tokens or repository-wide/static inspection behavior were selected.

Observed result:

```text
Ran 876 tests in 174.833s

OK
```

Non-failing observations:

- one sample-worktree LF/CRLF warning;
- existing `ResourceWarning` messages for historical subprocess text streams.

Neither changed the unittest verdict.

## Runtime identity preservation

P5-D4 runtime blob remained:

`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

No P5-D4 runtime implementation change was made.

## Adjudication

```text
P5E_TARGETED_PREDECESSOR_REGRESSION
= 208 / 208 PASS

P5E_CROSS_CUTTING_REGRESSION
= 876 / 876 PASS

P5D4_RUNTIME_CHANGE
= NONE

FULL_OBSIDIAN_REBREAK
= NOT_YET_CONSUMED

REAL_P5E
= CLOSED
```

The next operation is the one preregistered full `tests/obsidian_projection/test_*.py` re-break.

## Worktree provenance anomaly before full re-break

After the 876/876 cross-cutting PASS, a pre-persistence status check observed temporary worktree divergence in exactly:

- `tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json`
- `tools/obsidian_projection/p5e_near_real_time_model.py`

Observed transient worktree blobs were:

- contract: `ec54aaee33fc5c56be3636392856766097ae3e50`
- model: `de9ad391664a2cb249ac28b1622814442092b27a`

The committed authoritative blobs remained:

- contract: `e5c3d7a9d451aba65e8062078c6c10d23e586f39`
- model: `8662dd97a1c8a1af33d6593ae923384e96404b5a`

No persistence of the transient content was attempted.

A subsequent 42-test P5-E run passed and the worktree files returned byte-for-byte to the committed authoritative blobs without a restoration action being issued by this qualification flow.

The cause is not proven and is therefore recorded as:

```text
WORKTREE_PROVENANCE_ANOMALY
= OBSERVED

CAUSE
= UNKNOWN

TRANSIENT_CONTENT_ADOPTED
= FALSE

TRANSIENT_CONTENT_PERSISTED
= FALSE
```

Because provenance is not established, the primary worktree is not used as the execution surface for the final full re-break.

The final full re-break must instead use a fresh disposable control clone fetched from the exact remote P5-E branch HEAD, verify clean state and exact origin identity before execution, and be discarded afterward.
