# CR1 — Context Informativeness — helper adversarial review V0.2

Date: 2026-09-26
Persisted HEAD reviewed: `03b02dc1d29bfbaed1c0839872544401659f5d92`

## Correction from V0.1

The first local corpus attempt never reached CR1 execution. It stopped during raw-Git staging because the registry auxiliary SHA-256 was wrong.

Registry content identity was unchanged:
- Git blob: `490039cecf5a02ac7e553f8f7e47f6d4baedb584`
- bytes: 7,215
- correct SHA-256: `24db0f82a602fa9e1abc04d2793898847c98dc27ed5fe4a16bcd12502fd787a4`

The incorrect value `0320e51f...` was orchestration metadata, not a different registry.

## Corrected helper identity

- Git blob: `bb5cd4acd1b48141019c0ec3796ea61627dc0dbf`
- SHA-256: `423eed0f22b87a92210f53c6668c5b242c8ddb687da3292415c43879fb1f4eac`
- bytes: 36,971

Only `EXPECTED_REGISTRY_SHA256` changed.

No hypothesis, baseline, fold, target, threshold, score, scope flag or research rule changed.

## Persisted-head re-break

- py_compile: PASS
- synthetic suite: **26/26 PASS**
- mutation suite: **20/20 KILLED**

The persisted helper Git blob exactly matches the re-broken local bytes.

## Verdict

**PASS — corrected CR1 helper V0.2 qualified for one governed local N0 corpus attempt.**

No CR1 hypothesis is yet supported.
No regime exists yet.
