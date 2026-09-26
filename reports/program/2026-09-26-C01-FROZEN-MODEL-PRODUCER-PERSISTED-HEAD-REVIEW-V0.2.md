# C01 frozen-model producer — persisted-HEAD review V0.2

Date: 2026-09-26
Persisted candidate HEAD: `01e8a392a86faab0db7d712c46b79547de51b800`

## Reason for V0.2

The V0.1 development run reproduced the exact intended model but serialized the internally undefined NY-hour-17 median as the non-standard JSON token `NaN`.

V0.2 changes representation only:
- undefined median -> JSON `null`;
- explicit `tick5_ny_hour_unavailable: [17]`;
- `allow_nan=False`;
- output schema `ATDS_C01_FROZEN_CONFIRMATORY_MODEL_V0_2`.

The internal model digest remains unchanged.

## Exact persisted identities

Producer:
- blob `13bdc28585e9c6d34bc2217c750f1716fa3e7f9c`
- SHA-256 `a7d1782debb31bee089f99351e1f83345333caf8bb9453d5db3d9be83f1cd4ed`
- 22,169 bytes

Tests:
- blob `60a15d2a985f13d71d137ece8aa527c759f314e8`
- SHA-256 `05a68021e31b657b468ae1f630cdf14ef0ed3b0ed741eeb576c53e15eb7783c4`
- 8,337 bytes

Mutation runner:
- blob `128e80e8d6efd66f038d47abbfb00345ce0a096c`
- SHA-256 `5655379a57e025d759f94d17ca535078d79c739b69259a2c23a330a073def1cd`
- 3,245 bytes

## Persisted-head re-break

- py_compile: PASS
- synthetic: **29/29 PASS**
- mutation: **17/17 KILLED**

Additional V0.2 breakers cover:
- non-standard NaN JSON;
- unavailable-hour guard drift.

## V0.1 run evidence retained

- output bytes: 2,597,107
- SHA-256: `05cb33679a48ba683ba6a68b95a371ed7ec630df24c237bebbdab404f8200b31`
- Git blob: `010a77df979d4b5347686320bb338d4dffdd28d0`
- model digest: `a8b8b823336fb0f7cd5a6b2bbae80d858603b6ff7567fe5e67e4b20c46726c7f`
- confirmation_data_accessed=false
- D2026 reproduction exact

V0.1 is execution evidence only, not the sealed final model artifact.

## Verdict

**PASS — V0.2 strict-JSON producer qualified for one development-only AP0 rerun.**

No confirmation-window access or scoring is authorized.
