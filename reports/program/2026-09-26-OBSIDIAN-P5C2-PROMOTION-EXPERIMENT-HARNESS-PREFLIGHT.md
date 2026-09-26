# OBSIDIAN P5-C2 — PROMOTION EXPERIMENT HARNESS PREFLIGHT

Date: 2026-09-26

## Scope

P5-C2 implements the preregistered P5-C Windows/OneDrive promotion experiment protocol.

It is sandbox-only. The real ATDS Obsidian Vault is never an experiment target.

## Qualified predecessor

P5-C qualification:

    0a649ec676d0b4ef7331f008a8701beecd14bf5d

Qualified P5-C contract blob:

    36e49e72a867e30a69f63eb413fd924d0e56297b

## Candidate branch

    feat/obsidian-projection-p5c2-promotion-experiment-harness-v0.1

## Persisted implementation artifacts

Harness:

    tools/obsidian_projection/promotion_experiment.py
    blob: b5ba13a6aa9ddf1690842aafea422973e15cdf2d

CLI:

    tools/obsidian_projection/p5c2_verify.py
    blob: 267b1da5832e31af32886f747e73727ae58bb59e

Unit tests:

    tests/obsidian_projection/test_promotion_experiment.py
    blob: 604ef68f5ef51fe0bacfcee780f2d3f1c62a8171

Adversarial breakers:

    tests/obsidian_projection/test_p5c2_adversarial.py
    blob: f4a3be3b151c7a064587bed7588ba5ed963a189f

Persisted control runner:

    tools/obsidian_projection/run_p5c2_control.ps1
    blob: 6eb34646a78961af13bce86e23cf060e543cb493

## Protected live Vault

The harness knows the qualified live Vault only for:

- strict non-overlap checks;
- before/after read-only digests of `generated/`;
- before/after read-only digests of `views/`;
- reporting.

The experiment never uses the live Vault as a promotion target.

Any change in the byte-level tree digest of live `generated/` or `views/` during the sandbox experiment causes BLOCKED.

## Sacrificial sandbox

Exact experiment root:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-P5C-PROMOTION-SANDBOX

Requirements:

- exact OneDrive sibling of the live Vault;
- absent before experiment;
- no overlap with live Vault;
- no .git;
- sacrificial;
- retained after execution for evidence/inspection unless separately cleaned later.

## Fixture

Two complete immutable fixture generations are built:

    GEN_A
    GEN_B

Each contains:

    128 files
    8 nested directories
    per-file generation IDs
    per-file SHA-256
    manifest
    deterministic generation tree digest

## Reader

The concurrent reader validates a logical generation end-to-end:

- entrypoint exists;
- manifest parses;
- all 128 referenced files exist;
- every file SHA-256 matches;
- every file embeds the manifest generation ID;
- recomputed tree digest matches;
- pointer mode cannot expose stage/temp paths.

Each qualifiable candidate requires:

    250 promotion cycles
    5000 total reader samples
    at least one fresh reader sample after each individual promotion cycle

This prevents a false PASS where most observations happen only after promotion activity has ended.

## Candidates

Negative control:

    DIRECT_IN_PLACE_PER_FILE_REPLACE

It passes only as a negative-control validation when the reader actually detects non-atomic behavior. It can never qualify as a production primitive.

Qualifiable candidates:

    DIRECTORY_TWO_RENAME_SWAP
    WINDOWS_MOVEFILEEX_DIRECTORY_REPLACE
    IMMUTABLE_GENERATION_ATOMIC_POINTER

## Final-state verification

A candidate cannot pass merely because its final directory is internally valid.

After all required cycles, the final:

    generation_id
    tree_digest_sha256

must equal the exact generation expected after the final A/B transition.

## Candidate adjudication

- no qualifiable candidate PASS → FAIL / ALL_CANDIDATES_REJECTED;
- exactly one PASS → candidate may proceed to crash-recovery probe;
- multiple PASS → BLOCKED / MULTIPLE_CANDIDATES_REQUIRE_ADJUDICATION.

No winner is selected by preference.

## Crash recovery

The pointer primitive contains a bounded recovery probe:

- BEFORE_PROMOTION;
- atomic pointer mutation;
- AFTER_PROMOTION_BEFORE_STATE_RECORD.

If another primitive becomes the sole filesystem PASS, P5-C2 remains BLOCKED until that primitive receives its own candidate-specific crash probe.

## Metrics

Raw reports use:

    ATDS_OBSIDIAN_P5C_PROMOTION_METRICS_V0_1

An append-only JSONL evidence stream is written outside the Vault under LocalAppData.

The report also records:

- Windows identity;
- filesystem type;
- OneDrive sandbox path;
- sandbox reparse summary;
- Python version.

## Important non-authorization

Even a P5-C2 filesystem PASS leaves:

    obsidian_open_qualified = false
    production_promotion_authorized = false

P5-C2 cannot enable continuous synchronization by itself.

## Required qualification sequence

Before the real sandbox experiment:

1. recover exact persisted P5-C2 HEAD using LF-preserving clone;
2. run targeted unit tests;
3. run targeted adversarial breakers;
4. run the full Obsidian projection suite;
5. require source-clean clone;
6. run `--preflight`;
7. only if all above PASS, run `--run-experiment`.

## Current verdict

**P5-C2 HARNESS CANDIDATE PERSISTED — LOCAL RE-BREAK + SANDBOX EXPERIMENT REQUIRED**
