# CR1 — registry SHA binding incident

Date: 2026-09-26
Branch: `integration/system-v1`
Fresh HEAD before correction: `397e01a3cb77ac931550aa7248bde571ee302807`.

## Observed local block

The governed CR1 materializer stopped before helper execution with:

`REGISTRY_SHA256_MISMATCH=24db0f82a602fa9e1abc04d2793898847c98dc27ed5fe4a16bcd12502fd787a4`

The staged registry was materialized from the exact expected Git blob:
`490039cecf5a02ac7e553f8f7e47f6d4baedb584`.

Therefore the registry bytes were not corrupted or substituted.

## Root cause

The previously recorded auxiliary registry SHA-256:
`0320e51fb4f53fbed2c2e6a51d41c83e2b8ddd7afe59c6fca91a0a34eaf7f8f5`

was incorrect.

The SHA-256 of the exact raw Git blob bytes is:
`24db0f82a602fa9e1abc04d2793898847c98dc27ed5fe4a16bcd12502fd787a4`.

This is an identity-metadata correction, not a research-result correction.

No CR1 corpus calculation occurred before the block.

## Corrective scope

Only:
- correct `EXPECTED_REGISTRY_SHA256` in the CR1 helper;
- correct the registry SHA in the local handoff;
- revoke the previous corpus-run authorization until persisted-head re-break passes.

No hypothesis, fold, target, baseline, threshold rule, scoring rule or scope flag is changed.

## Candidate corrected helper identity

Expected after one-line correction:
- bytes: 36,971
- Git blob: `bb5cd4acd1b48141019c0ec3796ea61627dc0dbf`
- SHA-256: `423eed0f22b87a92210f53c6668c5b242c8ddb687da3292415c43879fb1f4eac`

Local pre-persistence checks:
- py_compile PASS
- synthetic 26/26 PASS
- mutation 20/20 KILLED

These local checks do not authorize corpus execution until persisted-head re-break.
