# OBSIDIAN P5-D3F — V6 INDEX STAT RECONCILIATION STATIC REVIEW

Date: 2026-09-28

## Evidence status

Same-assistant static review.

Not independent execution evidence.
Does not qualify P5-D3F.

## Trigger

V5 USER-REPORTED LOCAL EXECUTION reached the exact candidate and verified remote race guard, then blocked because Git marked the eight byte-pin compatibility paths modified after exact committed-blob materialization.

Subsequent USER-REPORTED LOCAL DIAGNOSTICS established for the representative contract file:

    HEAD blob == index blob == raw worktree blob == filtered worktree blob

while Git status still reported `.M`.

A temporary-index experiment then showed that `git update-index --really-refresh` removed the dirty classification without changing HEAD/index/raw blob identities, while the real index SHA-256 remained unchanged.

## Root-cause classification

Supported diagnosis:

    STALE / NON-RECONCILED GIT INDEX STAT METADATA AFTER BYTE-EXACT WRITE

This is narrower than the earlier LF/CRLF failure family.

The evidence does not support attributing the remaining V5 block to VS Code, file content, blob identity, EOL representation, core.trustctime alone, or core.checkStat alone.

## Exact V6 functional candidate

    c625a9e8d438bb3750dff58d30cbe4442fb3bc42

Exact blobs:

Runner:

    06103797b5aaf34a9f847e0cc908b4b245452cb9

Runner tests:

    90151e541ded4cbb50d7773730e1fba840f7cc0c

P5-D3F contract unchanged:

    64744325251db350d26c0269090ce62d5fa5f2e8

P5-D3F contract tests unchanged:

    3dc1d7315874d4352eeaf05407f266961c878e70

.gitattributes unchanged:

    e0154899b5640da025a082ef6b02f4bf179d3030

## Static correction review

V6 changes only the governed contract qualification runner and its runner tests.

The runner now:

1. materializes the exact committed bytes;
2. verifies raw worktree blob equality before any index refresh;
3. snapshots the complete staged index representation with `git ls-files --stage -z`;
4. executes `git update-index --really-refresh`;
5. accepts only return code 0 or the locally observed return code 1;
6. snapshots staged index representation again;
7. rejects any stage/mode/OID change;
8. requires the repository to be clean afterwards.

The first implementation draft used `git write-tree` as an invariance witness. Static review rejected that approach because `write-tree` can create a Git tree object and therefore introduces an unnecessary object-database mutation.

The final candidate instead uses `git ls-files --stage -z`, which is read-only and directly captures staged mode/OID/stage entries.

## Breakers added

Runner tests now require:

- observed refresh return code 1 is acceptable only when the staged-index snapshot remains identical;
- any staged-index snapshot mutation across refresh raises `GovernedRunError`.

These are additive runner breakers.

No historical expected blob was changed.
No historical test was weakened.

## Remaining uncertainty

The V6 logic has not yet been executed on the user's Windows checkout.

Therefore the following remain unproven until the governed local V6 re-break:

- whether the refresh step clears all eight V5 stat-only dirty classifications in the real qualification flow;
- whether the targeted runner tests pass under the user's Python/Git environment;
- whether the complete historical Obsidian regression remains PASS;
- whether the final control clone is clean.

## Verdict

    STATIC CORRECTION REVIEW = PASS
    V6 LOCAL GOVERNED RE-BREAK = REQUIRED
    P5-D3F CONTRACT = UNQUALIFIED
    P5-D3F IMPLEMENTATION = UNAUTHORIZED
    P5-D3G = CLOSED
    REAL VAULT WRITE = CLOSED
