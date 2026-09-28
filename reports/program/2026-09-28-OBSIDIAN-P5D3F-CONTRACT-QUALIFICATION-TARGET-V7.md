# OBSIDIAN P5-D3F — CONTRACT QUALIFICATION TARGET V7

Date: 2026-09-28

## Evidence status

Static target only.

No governed V7 local execution has been performed by this assistant.
P5-D3F remains unqualified until the governed local V7 re-break passes.

## Exact functional candidate

    49eda71d200cca7a860fd9b0d212aa0e94e9cea7

## Exact functional blobs

P5-D3F contract:

    64744325251db350d26c0269090ce62d5fa5f2e8

P5-D3F contract tests:

    3dc1d7315874d4352eeaf05407f266961c878e70

Governed Python runner:

    18d56b5a2cf1e9fdbd502ce2545f69e685e40e4d

Runner tests:

    4857a0e7eb55caf23071b7cabae3449322433e76

.gitattributes:

    e0154899b5640da025a082ef6b02f4bf179d3030

## Triggering evidence

USER-REPORTED LOCAL diagnostics established for the representative P5-D3F contract path:

- HEAD blob == index blob == raw worktree blob == filtered worktree blob;
- whole-index `git update-index --really-refresh` left the representative path dirty;
- path-scoped `git update-index --really-refresh -- <path>` cleared the representative dirty classification;
- staged mode/OID/stage remained invariant;
- the real index SHA-256 remained unchanged because the causal experiment used temporary index copies.

## V7 correction

V7 preserves V5 exact committed-blob materialization and the V6 staged-index invariance breaker.

The runner now performs this order:

1. require clean worktree before governed execution;
2. materialize exact committed bytes for the existing bounded byte-pin compatibility paths;
3. require raw worktree blob == committed blob for every bounded path;
4. snapshot the complete staged representation with `git ls-files --stage -z`;
5. for each existing bounded byte-pin path, individually execute:

       git update-index --really-refresh -- <path>

6. accept only return code 0 or the experimentally observed return code 1;
7. snapshot the complete staged representation again;
8. require exact equality of staged mode/OID/stage representation before vs after;
9. require the complete worktree to be clean;
10. continue the existing contract blob, compile, targeted and historical full re-break controls.

## Test-first breaker

The runner-test surface now explicitly requires one individually path-scoped refresh call for every entry in the preregistered BYTE_PIN_COMPATIBILITY_PATHS tuple.

The prior staged-index mutation breaker remains active.

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
No new compatibility path was added.
No handoff runtime was implemented.
No CURRENT mutation is authorized.
No real Vault write is authorized.
No P5-D3G authority is granted.
