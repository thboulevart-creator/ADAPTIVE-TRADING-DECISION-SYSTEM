# OBSIDIAN P5-D3F — CANONICAL BLOB MATERIALIZATION STATIC REVIEW

Date: 2026-09-28

## Evidence status

Same-assistant static review.

Not independent local execution evidence.
Does not qualify P5-D3F.

## Triggering evidence

USER-REPORTED LOCAL EXECUTION reached the V4 compatibility guard and blocked because several historical byte-pinned files were still materialized in the Windows worktree with non-canonical bytes.

Representative mismatch:

    committed=5cd11e9512249da26adf4b6f86e79259af725809
    working=6aeeff6ea066c447a7df2ab2b019f6611a39bc39

The failure family affected historical predecessor guards that intentionally hash local file bytes.

## Clarification

VS Code is not the cause.

The integrated terminal remained PowerShell, and the failure is caused by Windows Git checkout byte representation versus canonical committed Git blob bytes.

The move to VS Code and the move out of OneDrive remain valid improvements:

- shorter paths;
- no OneDrive locking of .git object packs;
- versioned Python runners;
- repository-root-bound execution.

## Why .gitattributes alone was insufficient in the existing clone

V4 added:

    * text=auto eol=lf

and attempted:

    git checkout-index --all --force

However the already-materialized Windows worktree still retained non-canonical byte representations for the historical byte-pinned files.

Therefore the qualification runner must not rely on checkout conversion behavior to reconstruct those evidence-critical bytes.

## V5 correction

Functional candidate:

    401cdf3e8eb8fea40fc61536227441de83c49246

Runner blob:

    dcc85c9e426565a56ada1c30d029c3a565769752

Runner-test blob:

    e1d16c07ce3a85c4ef65964346b587dabd4dcf07

The P5-D3F contract remains unchanged.

## Exact materialization rule

For every preregistered historical byte-pin compatibility path, the runner now:

1. requires a clean worktree;
2. reads the exact committed bytes with:

       git cat-file blob HEAD:<path>

3. writes those bytes directly to the tracked working-tree path with Python binary I/O;
4. requires the Git worktree to remain logically clean;
5. computes:

       git hash-object --no-filters <path>

6. requires the raw working-tree blob identity to equal:

       git rev-parse HEAD:<path>

This bypasses platform newline conversion during evidence-critical local execution.

## Compatibility paths

The bounded compatibility set remains explicit:

    tools/obsidian_projection/first_open_safety_contract_v0_1.json
    tools/obsidian_projection/first_open_safety_contract_v0_2.json
    tools/obsidian_projection/deterministic_projection_contract_v0_1.json
    tools/obsidian_projection/first_open.py
    tools/obsidian_projection/p3d_verify.py
    tools/obsidian_projection/obsidian_open_retry_contract_v0_2.json
    tools/obsidian_projection/real_exact_head_sandbox_contract_v0_1.json
    tools/obsidian_projection/promotion_handoff_contract_v0_1.json

These paths correspond to the failure family observed in the supplied full-regression output.

## New unit breaker

A new runner unit test creates a temporary Git repository, commits LF bytes, deliberately changes the worktree to CRLF bytes, verifies the raw blob mismatch, invokes exact committed-blob materialization, and requires the working bytes and raw blob identity to return to the committed LF representation.

## Boundary preservation

No historical predecessor expected blob was changed.

No predecessor test was weakened.

No P5-D3F contract semantic changed.

No publication runtime was implemented.

No real Vault write was introduced.

No CURRENT mutation was introduced.

## Verdict

**STATIC CORRECTION REVIEW PASS — FULL LOCAL CONTRACT RE-BREAK REQUIRED**

Exact functional candidate:

    401cdf3e8eb8fea40fc61536227441de83c49246
