# OBSIDIAN P5-D3F — CONTRACT QUALIFICATION TARGET V6

Date: 2026-09-28

## Evidence status

Static target only.

No local V6 execution has been performed by this assistant.
P5-D3F remains unqualified until the governed local re-break passes.

## Exact functional candidate

    c625a9e8d438bb3750dff58d30cbe4442fb3bc42

## Exact functional blobs

P5-D3F contract:

    64744325251db350d26c0269090ce62d5fa5f2e8

P5-D3F contract tests:

    3dc1d7315874d4352eeaf05407f266961c878e70

Governed Python runner:

    06103797b5aaf34a9f847e0cc908b4b245452cb9

Runner tests:

    90151e541ded4cbb50d7773730e1fba840f7cc0c

.gitattributes:

    e0154899b5640da025a082ef6b02f4bf179d3030

## Triggering local evidence

USER-REPORTED LOCAL EXECUTION on V5 demonstrated:

- exact HEAD/index/raw/filtered blob identity for the representative P5-D3F contract;
- `git status` still reported `.M`;
- on a temporary copy of the Git index, `git update-index --really-refresh` reported the eight byte-pin paths as needing update and returned 1;
- immediately afterwards, status against that temporary index was clean;
- HEAD/index/raw blob identities remained unchanged;
- SHA-256 of the real index remained unchanged.

This supports the narrow diagnosis that V5's byte-exact writes left stale Git index stat metadata on the Windows checkout.

## V6 correction

V6 preserves V5 exact committed-blob materialization.

The runner now performs this order:

1. write the exact committed blob bytes for the bounded compatibility paths;
2. recompute and require raw worktree blob == committed blob for every bounded path;
3. snapshot the complete staged index representation with `git ls-files --stage -z`;
4. run `git update-index --really-refresh` to reconcile stat metadata;
5. accept return code 0 or the observed transitional return code 1;
6. snapshot the staged index representation again and require byte-for-byte equality with the pre-refresh snapshot;
7. require the worktree to be clean.

The index-stage snapshot invariant prevents the refresh step from laundering any staged content, mode, OID, or stage mutation.

## Required PASS

    P5D3F_CANONICAL_BLOB_MATERIALIZATION=PASS
    P5D3F_INDEX_STAT_REFRESH=PASS
    P5D3F_BYTE_PIN_COMPATIBILITY=PASS
    P5D3F_CONTRACT_BLOB=PASS
    P5D3F_CONTRACT_TEST_BLOB=PASS
    P5D3F_CONTRACT_PY_COMPILE=PASS
    P5D3F_CONTRACT_TARGETED=PASS
    P5D3F_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_CONTRACT_REBREAK_COMPLETED=PASS

## Authority boundary

No historical expected blob was repinned.
No historical test was weakened.
No P5-D3F contract semantic was changed.
No handoff runtime was implemented.
No CURRENT mutation is authorized.
No real Vault write is authorized.
No P5-D3G authority is granted.
