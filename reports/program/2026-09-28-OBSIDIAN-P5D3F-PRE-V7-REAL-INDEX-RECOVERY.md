# OBSIDIAN P5-D3F — PRE-V7 REAL-INDEX PATHSCOPED RECOVERY

Date: 2026-09-28

## Evidence status

USER-REPORTED LOCAL EXECUTION.

This report does not constitute independent execution evidence and does not qualify V7 or P5-D3F.

## Verified GitHub state before persistence

Branch:

    feat/obsidian-projection-p5d3f-promotion-handoff-contract-v0.1

Remote HEAD:

    d1862e62f86e12f282b88ea4e0421f19f7f6adb5

V7 functional candidate:

    49eda71d200cca7a860fd9b0d212aa0e94e9cea7

## Local recovery precondition

The user's local checkout was still on the V5 functional candidate:

    EXPECTED_HEAD=401cdf3e8eb8fea40fc61536227441de83c49246
    ACTUAL_HEAD=401cdf3e8eb8fea40fc61536227441de83c49246

The eight bounded byte-pin compatibility paths were then individually processed with:

    git update-index --really-refresh -- <path>

Each call returned the experimentally accepted exit code 1 while progressively removing the corresponding stat-only dirty classification.

## Invariance proof

The complete staged representation was captured before and after the bounded recovery.

User-reported result:

    INDEX_STAGE_UNCHANGED=PASS

No staged mode/OID/stage change was observed.

## Final cleanliness

User-reported final command:

    git status --porcelain --untracked-files=all

produced no output.

Therefore the local checkout satisfies the clean-worktree precondition required before the governed V7 runner is started.

## Authority boundary

This recovery:

- does not qualify V7;
- does not qualify P5-D3F;
- does not authorize implementation;
- does not authorize P5-D3G;
- does not authorize real Vault writes;
- does not alter historical expected blobs.

Next gate:

    P5-D3F V7 LOCAL GOVERNED CONTRACT RE-BREAK
