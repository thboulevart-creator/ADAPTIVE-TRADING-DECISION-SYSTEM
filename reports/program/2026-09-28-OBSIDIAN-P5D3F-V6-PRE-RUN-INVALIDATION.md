# OBSIDIAN P5-D3F — V6 PRE-RUN INVALIDATION

Date: 2026-09-28

## Evidence status

USER-REPORTED LOCAL EXECUTION / DIAGNOSTIC.

This report does not constitute independent execution evidence.

## Branch state before persistence

Verified remote HEAD:

    699e31d8c8f65bdec647ffedf18c34dcf4ac340d

## V6 candidate under review

Functional candidate:

    c625a9e8d438bb3750dff58d30cbe4442fb3bc42

The candidate was NOT executed as a governed V6 re-break.

## Triggering evidence

The user's local checkout remained on the V5 candidate with the eight stat-only dirty paths.

A real-index recovery attempt using:

    git update-index --really-refresh

produced:

    REFRESH_EXIT_CODE=1
    INDEX_STAGE_UNCHANGED=PASS

but the subsequent real worktree status still reported the same eight paths as modified.

A follow-up timestamp isolation experiment then used two temporary index copies:

- one with the same LastWriteTimeUtc as the real index;
- one deliberately made newer.

Both temporary indexes still reported the representative P5-D3F contract as:

    1 .M N... 100644 100644 100644
    64744325251db350d26c0269090ce62d5fa5f2e8
    64744325251db350d26c0269090ce62d5fa5f2e8
    tools/obsidian_projection/promotion_handoff_contract_v0_1.json

The real index/worktree also remained unchanged by this experiment and continued to report .M.

## Adjudication

The hypothesis that merely making the physical index file newer would remove the dirty classification is REFUTED.

The prior inference that `git update-index --really-refresh` alone was a sufficient V6 correction is also NOT SUPPORTED on the real index.

Therefore:

    V6 LOCAL GOVERNED RE-BREAK = DO NOT RUN
    V6 FUNCTIONAL CANDIDATE = INVALIDATED BEFORE LOCAL QUALIFICATION
    P5-D3F CONTRACT = UNQUALIFIED
    P5-D3F IMPLEMENTATION = UNAUTHORIZED
    P5-D3G = CLOSED
    REAL VAULT WRITE = CLOSED

## Remaining verified facts

For the representative contract path, previous diagnostics established:

    HEAD blob == index blob == raw worktree blob == filtered worktree blob

and mode 100644 is unchanged, while porcelain status continues to report .M.

Therefore the remaining issue is not demonstrated to be a byte-content, EOL, mode, core.trustctime-only, core.checkStat-only, or physical-index-timestamp-only failure.

## Next experiment

Before any new runner mutation, compare `git add --refresh` with `git update-index --really-refresh` against isolated temporary index copies.

The Git documentation explicitly defines `git add --refresh` as refreshing only stat() information in the index without adding file contents.

The experiment must:

1. use only temporary index copies via GIT_INDEX_FILE;
2. preserve and compare complete staged mode/OID/stage snapshots before and after;
3. use `git --no-optional-locks status` for observation;
4. leave the real index and worktree unchanged;
5. stop before any new V7 runner mutation.
