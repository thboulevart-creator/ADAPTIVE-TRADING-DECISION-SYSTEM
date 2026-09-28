# OBSIDIAN P5-D3F — CANONICAL LF CHECKOUT STATIC REVIEW

Date: 2026-09-28

## Evidence status

Same-assistant static correction review.

This is not independent execution evidence and does not qualify P5-D3F.

## Triggering evidence

USER-REPORTED LOCAL EXECUTION reached the full Obsidian regression and reported:

    Ran 1084 tests in 16.750s
    FAILED (failures=4, errors=8)

The failures were dominated by historical byte-pin mismatches on previously-qualified text files.

Examples:

    P3-C first-open contract
    P3-C2 first-open contract
    P2-A deterministic projection contract
    P5-C3R retry contract
    P5-D3E real exact-head contract
    P3-D v0.1 harness
    P3-D v0.1 CLI

P5-D3D / P5-D3E synthetic failures appeared downstream after those predecessor authorities failed verification.

## Repository diagnosis

The repository had no .gitattributes file.

The new Windows clone therefore inherited platform checkout behavior for text files.

Historical qualification surfaces intentionally recompute Git-style blob identities from local file bytes.

A CRLF-materialized working tree can therefore be logically Git-clean while still failing those byte-pinned historical checks.

## Correction

A repository-level .gitattributes file was added:

    * text=auto eol=lf

Blob:

    e0154899b5640da025a082ef6b02f4bf179d3030

This defines canonical LF working-tree text representation independent of machine-global core.autocrlf behavior.

## Runner hardening

The governed Python runner now:

1. requires the exact .gitattributes blob;
2. after target-candidate re-exec, runs:

       git checkout-index --all --force

   to rematerialize all tracked files under the target commit's attributes;
3. requires the repository to remain logically clean;
4. compares raw working-tree byte blobs against committed Git blobs for representative historical byte-pin authorities before any qualification tests;
5. blocks if any representative byte-pinned file is not byte-canonical.

Representative compatibility paths include:

    first_open_safety_contract_v0_1.json
    first_open_safety_contract_v0_2.json
    deterministic_projection_contract_v0_1.json
    first_open.py
    p3d_verify.py
    obsidian_open_retry_contract_v0_2.json
    real_exact_head_sandbox_contract_v0_1.json
    promotion_handoff_contract_v0_1.json

## Functional identities

Corrected functional candidate:

    28a1dd16e09c6534e4af404e1a5b2779113e453e

P5-D3F contract blob unchanged:

    64744325251db350d26c0269090ce62d5fa5f2e8

P5-D3F contract-test blob unchanged:

    3dc1d7315874d4352eeaf05407f266961c878e70

Canonical .gitattributes blob:

    e0154899b5640da025a082ef6b02f4bf179d3030

Governed runner blob:

    b2bdbd90fcb27568940b28c0b389ac2222f76f9a

Runner-test blob:

    a188bf40a8f1e8bc6a457040f8f469d13d8d0281

## Scope

No historical qualified predecessor was modified.

No expected predecessor blob was repinned.

No historical byte-pin test was weakened.

No P5-D3F contract semantic changed.

No handoff runtime was implemented.

No real Vault write was introduced.

No CURRENT mutation or promotion authority was introduced.

## Expected corrected local markers

Before targeted tests:

    P5D3F_CANONICAL_LF_CHECKOUT=PASS
    P5D3F_BYTE_PIN_COMPATIBILITY=PASS

Then:

    P5D3F_CONTRACT_BLOB=PASS
    P5D3F_CONTRACT_TEST_BLOB=PASS
    P5D3F_CONTRACT_PY_COMPILE=PASS
    P5D3F_CONTRACT_TARGETED=PASS
    P5D3F_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_CONTRACT_REBREAK_COMPLETED=PASS

## Verdict

**STATIC CORRECTION REVIEW PASS — FULL LOCAL CONTRACT RE-BREAK REQUIRED**

A local PASS is still required before P5-D3F implementation is authorized.
