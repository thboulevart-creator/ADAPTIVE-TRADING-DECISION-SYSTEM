# P5-E V0.1 — BB1 FULL OBSIDIAN RE-BREAK

Date: 2026-10-02

## Scope

This is the single full Obsidian suite authorized by:
`P5-E V0.1 — BB1 NORMATIVE GUARD COVERAGE CLOSURE`

Full-suite budget:
`1 / 1 CONSUMED`

The run was executed in a disposable clone, not in the canonical working tree.

## Exact executable identity

Branch:
`feat/obsidian-projection-p5e-v0.1-bb1-normative-guard-closure`

HEAD:
`647edf62723fa84c7260c0ea3b25c074f180604f`
Contract blob:
`7e3e18ba946246065b43bc5fbabdc35980140eb9`

Model blob:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`

Evidence matrix blob:
`88e13a447a96455d4ac1d9d0f96e11b29329616d`

P5-D4 runtime blob:
`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

Disposable clone path during execution:
`C:\Users\Boulevart\ATDS-TMP\P5E-BB1-FULL-647edf62723f`

The clone HEAD matched the governed HEAD before execution.
## Real P5-D4 fingerprint before full suite

```text
observer-events.jsonl
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

observer-checkpoint.json
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

## Command

```text
python -B -m unittest discover -s tests/obsidian_projection -p 'test_*.py'
```
## Result

```text
Ran 1486 tests in 245.601s

OK

FULL_EXIT=0
FULL_SECONDS=247.637
```

The disposable clone reported three post-run worktree residues.

They were not enumerated before clone deletion, so no stronger claim is made about their exact filenames.

The disposable clone was removed after the run.

## Real P5-D4 fingerprint after full suite

```text
observer-events.jsonl
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af
observer-checkpoint.json
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

Therefore:
`REAL_P5D4_STATE_CHANGED = FALSE`

Canonical repository status after clone deletion:
`CLEAN`

## Non-failing observations

The run emitted:
- the existing sample-worktree LF/CRLF warning;
- historical `ResourceWarning` messages for unclosed subprocess text streams.

Neither changed the unittest verdict.

## Verdict

```text
FULL_OBSIDIAN_REBREAK = 1486 / 1486 PASS
DISPOSABLE_CLONE = USED_AND_REMOVED
REAL_P5D4_FINGERPRINT = UNCHANGED
REAL_P5E = CLOSED
```
