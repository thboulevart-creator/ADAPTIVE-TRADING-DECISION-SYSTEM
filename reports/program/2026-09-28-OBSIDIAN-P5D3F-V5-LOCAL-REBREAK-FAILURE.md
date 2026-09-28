# OBSIDIAN P5-D3F — V5 LOCAL CONTRACT RE-BREAK FAILURE

Date: 2026-09-28

## Evidence status

USER-REPORTED LOCAL EXECUTION.

This report does not constitute independent execution evidence.

## Governed target

Branch:

    feat/obsidian-projection-p5d3f-promotion-handoff-contract-v0.1

Remote HEAD verified immediately before persistence:

    23c788f988d9e9deab4ff3f13eb9ec9722c17d49

V5 functional candidate:

    401cdf3e8eb8fea40fc61536227441de83c49246

## User-reported execution

The governed runner reached:

    CONTROL_CLONE_CLEAN_BEFORE=PASS
    FETCHED_HEAD=23c788f988d9e9deab4ff3f13eb9ec9722c17d49
    REMOTE_RACE_GUARD=PASS
    P5D3F_REEXEC_AFTER_CHECKOUT=REQUIRED

After self-checkout/re-exec:

    CONTROL_CLONE_CLEAN_BEFORE=PASS
    FETCHED_HEAD=23c788f988d9e9deab4ff3f13eb9ec9722c17d49
    REMOTE_RACE_GUARD=PASS
    P5D3F_RUNTIME_HEAD=401cdf3e8eb8fea40fc61536227441de83c49246

The run then blocked:

    BLOCKED: working tree non propre après canonical blob materialization:
     M tools/obsidian_projection/deterministic_projection_contract_v0_1.json
     M tools/obsidian_projection/first_open.py
     M tools/obsidian_projection/first_open_safety_contract_v0_1.json
     M tools/obsidian_projection/first_open_safety_contract_v0_2.json
     M tools/obsidian_projection/obsidian_open_retry_contract_v0_2.json
     M tools/obsidian_projection/p3d_verify.py
     M tools/obsidian_projection/promotion_handoff_contract_v0_1.json
     M tools/obsidian_projection/real_exact_head_sandbox_contract_v0_1.json

## Adjudication

    P5-D3F CONTRACT = UNQUALIFIED
    P5-D3F IMPLEMENTATION = UNAUTHORIZED
    P5-D3G = CLOSED
    LIVE VAULT PUBLICATION = CLOSED

No PASS is inferred beyond the markers explicitly emitted by the user-reported run.

## Static root-cause boundary

Verified statically:

- the runner writes exact bytes from `git cat-file blob HEAD:<path>`;
- immediately afterwards it requires `git status --porcelain` to be empty;
- the Windows execution reports all eight bounded byte-pin compatibility paths as modified;
- the historical P5-D3F contract test also uses `git diff --quiet HEAD -- <contract path>`.

Therefore the failure is narrowed to the relationship between exact raw blob materialization and Git's logical working-tree comparison on the user's Windows checkout.

The exact mechanism is NOT YET PROVEN.

In particular, this report does not yet assert that `core.autocrlf`, `core.eol`, attributes, index normalization, or another Git setting is the root cause.

## Required next evidence

Before changing the runner again, perform a bounded read-only Git/EOL diagnostic on the current failed checkout to determine:

1. effective `core.autocrlf` and `core.eol`, including origin;
2. effective attributes for one affected path;
3. `git ls-files --eol` for the bounded affected paths;
4. whether a process-local Git configuration override changes the dirty classification without changing file bytes.

No historical blob repinning is authorized.
No breaker weakening is authorized.
No real Vault write is authorized.
