# P5-E V0.1 — TARGETED CLOSURE FULL OBSIDIAN RE-BREAK

Date: 2026-10-01

## Scope

This is the single full Obsidian re-break authorized by:

`P5-E V0.1 — EXTERNAL REVIEW TARGETED CLOSURE AMENDMENT`

No second full-suite is authorized or executed by this amendment.

## Exact execution identity

Branch:

`feat/obsidian-projection-p5e-v0.1-external-review-targeted-closure`

HEAD:

`f7da7fe1394f9000d9f2f7f3fd6c792b78489d20`

P5-D4 runtime blob before:

`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

Corrected P5-E contract blob:

`b0668b4dff65b8e30ee0d93a3e5a3fe42c4421dd`

Corrected P5-E model blob:

`b783717c9e9596b585b7b1686835c73fffbd1a7c`

Requirement/evidence matrix blob:

`0440175fbb79877e466119cb973ea82389a4ecd8`

The branch and remote were equal and the worktree was clean immediately before the run.

## Command

```text
python -B -m unittest discover -s tests/obsidian_projection -p 'test_*.py'
```

## Result

```text
Ran 1474 tests in 243.640s

OK

FULL_EXIT=0
FULL_SECONDS=245.366
```

P5-D4 runtime blob after:

`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

Therefore:

`P5D4_RUNTIME_CHANGE = NONE`

## Non-failing observations

The run emitted:

- one existing sample-worktree LF/CRLF warning;
- historical `ResourceWarning` messages for unclosed subprocess text streams.

Neither changed the unittest verdict.

Cross-interpreter tests produced three Python 3.14 `__pycache__` files. They were removed after the run before evidence persistence.

## Verdict

```text
FULL_OBSIDIAN_REBREAK
= 1474 / 1474 PASS

FULL_SUITE_BUDGET
= 1 / 1 CONSUMED

P5D4_RUNTIME
= UNCHANGED

REAL_P5E
= CLOSED
```

This evidence supports only the targeted-closure candidate and does not qualify a real P5-E loop or a real 60-second SLA.
