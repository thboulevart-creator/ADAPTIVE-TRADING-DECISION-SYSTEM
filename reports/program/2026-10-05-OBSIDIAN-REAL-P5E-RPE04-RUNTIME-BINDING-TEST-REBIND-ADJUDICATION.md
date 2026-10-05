# RPE-04 — RUNTIME BINDING TEST EXPECTATION REBIND — INTERNAL ADJUDICATION

Date: 2026-10-05

The existing runtime-binding hardening test remained bound to the raw SHA-256 of the historical RPE-03 V0.1 classifier:

cbcb996199b06859d257cc194e673a6bc51419890dc0641b42837d3f7cfcb0c3

The authorized RPE-04 closure explicitly requires rebinding to the human-adopted RPE-03 V0.2 classifier.

The active governed dependency is now:

Git blob:
5bbe455418fe1396ee5824379ad7450a1379cbba

Raw SHA-256:
4b743e187245585f4a4d9c923e316961f2842f96634d04dcac01972a29e60b41

Authorized test correction:
- change only the expected RPE-03 runtime dependency raw SHA-256 from V0.1 to V0.2;
- change no failure mode;
- change no runtime-binding requirement;
- change no authority;
- preserve all other historical expectations.

This is an authorized dependency-identity rebind, not a test relaxation.
