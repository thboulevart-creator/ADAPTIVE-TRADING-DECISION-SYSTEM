# OBSIDIAN P5-C3R2 — READER-ONLY EACCES RETRY PREFLIGHT

Date: 2026-09-27

## Evidence chain

Failed P5-C3R runtime candidate:

    ae7d1adbb146fffb60c4e302750abb896136d968

Observed first failure:

    cycles_completed = 250
    semantic_partial_generation_count = 19

Forensic runtime candidate:

    2cd17fe24668a276efda490c9102e423d9de70b8

Observed forensic failure:

    cycles_completed = 250
    semantic_partial_generation_count = 12
    semantic_partial_signature_total_count = 12

Exact repeated signature:

    message=CURRENT.md unreadable|cause_type=PermissionError|errno=13|winerror=None

Persisted forensic failure record:

    reports/program/2026-09-27-OBSIDIAN-P5C3R-SEMANTIC-PARTIAL-FORENSIC-RUN-FAILURE-USER-REPORTED.md

P5-C3R remains failed.

## Candidate branch

    feat/obsidian-projection-p5c3r2-reader-eacces-retry-v0.1

Candidate HEAD before local re-break:

    c7dc58706f59e9a31fbd844e92604256c36a392d

## Exact persisted artifacts

V0.2 contract:

    tools/obsidian_projection/obsidian_open_retry_contract_v0_2.json
    blob: a3fb7736f2c25f144b1d9bc4a50cbf4029e3dc33

Implementation:

    tools/obsidian_projection/obsidian_open_retry.py
    blob: df1a6988c5ce09d52941793a98f2a88728aaed41

P5-C3R2 CLI:

    tools/obsidian_projection/p5c3r2_verify.py
    blob: 1290ad909b7e78251fedd13303e87832833d487c

P5-C3R2 open runner:

    tools/obsidian_projection/run_p5c3r2_open.ps1
    blob: 125022e1e9c367d83bbc9d3394b73c5d1a585dd2

P5-C3R2 post-close runner:

    tools/obsidian_projection/run_p5c3r2_post_close.ps1
    blob: 0ce328c326e2b13774d9a2e71101f85cefdecfaf

V0.2 contract tests:

    tests/obsidian_projection/test_obsidian_open_retry_contract_v0_2.py
    blob: 3757cb311be2b778d6f52f3c8db7781ab0bed2dd

Unit tests:

    tests/obsidian_projection/test_obsidian_open_retry.py
    blob: 633b15ddff45b720696faea8244f759db7ede0ab

Adversarial breakers:

    tests/obsidian_projection/test_p5c3r_adversarial.py
    blob: 44413620e0068a094c588c9a939bbd74f0f3c9bf

Protocol:

    docs/OBSIDIAN-P5C3R2-READER-EACCES-RETRY-V0.1.md
    blob: da1e5b70a81288ac84170d1ff577b4f43cbd640b

## Preserved predecessor artifacts

Base P5-C3 harness remains:

    tools/obsidian_projection/obsidian_open_compatibility.py
    blob: b970e65f21792cccc6ee2e4271d630f371102ff7

P5-C3R open runner remains:

    tools/obsidian_projection/run_p5c3r_open.ps1
    blob: ea6dc7d45d98df9507db4015d4e15b76fbc1fd52

P5-C3R post-close runner remains:

    tools/obsidian_projection/run_p5c3r_post_close.ps1
    blob: 1409ed062e7a1546ad0d7afa42168d8c47312840

## Write policy

Unchanged.

Only:

    PermissionError
    winerror in {5, 32}

may retry os.replace(CURRENT.tmp, CURRENT.md).

Reader-only errno EACCES fallback is forbidden on the write path.

## Reader policy candidate

Retryable reader access conditions are exactly:

A.

    PermissionError
    winerror in {5, 32}

B.

    PermissionError
    winerror is None
    errno == EACCES
    errno == 13

The B fallback is reader-only.

The reader deadline remains 500 ms.

A permanent access denial remains terminal after the deadline.

## Required local breakers

Before any P5-C3R2 open experiment:

1. Obsidian closed.
2. Exact candidate checkout.
3. V0.1 contract tests.
4. V0.2 contract tests.
5. retry unit tests.
6. adversarial breakers.
7. full Obsidian suite.
8. clean working tree.
9. synthetic Windows lock breaker through P5-C3R2 CLI.
10. clean working tree again.

No recovery is authorized by default.

The latest forensic runtime completed with final GEN_A and no postcondition failure.
The live state must still be rechecked by the read-only precheck when Obsidian is reopened.

## Open experiment criteria

Unchanged:

    250 promotions
    >= 5000 reader samples
    >= 1 fresh reader sample per promotion
    final = GEN_A

Required zero outcomes:

    terminal_pointer_write_error_count = 0
    retry_deadline_exceeded_count = 0
    mixed_generation_count = 0
    missing_entrypoint_count = 0
    semantic_partial_generation_count = 0
    parse_error_count = 0
    reader_terminal_access_error_count = 0

New evidence of interest:

    reader_eacces_without_winerror_retry_count

This count may be non-zero.

## Qualification identity

Even after full P5-C3R2 PASS:

    p5c3r_qualified = false
    p5c3r2_qualified = true

Only the dedicated P5-C3R2 post-close path may emit the latter.

## Current verdict

**P5-C3R2 CANDIDATE PERSISTED — LOCAL RE-BREAK REQUIRED.**

No runtime PASS is claimed.
No production promotion is authorized.
No continuous observer is authorized.
