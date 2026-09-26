# C01 — Frozen Confirmatory Model — local development-only handoff

Date: 2026-09-26

## Authorized governed HEAD

This handoff becomes executable only from the qualification commit that persists this document.

## Exact producer

- blob `ee0989f29399bf9f904ca314fdb5f01cc45ddec8`
- SHA-256 `682c1ce6f06f753cf3f0508396394bf6acd51249dfe61dc1c89815755137133c`

Dependencies:
- CR1 helper blob `bb5cd4acd1b48141019c0ec3796ea61627dc0dbf`
- CR2 helper blob `34c702e926b3baec90c57b8366177c2db1eca074`
- CR2 evidence blob `d6543d12fc01405fedb006ddb5d714a772f32678`
- Charter V0.2 blob `ada0ebf41ecd7ab406d2656ac745ed7003d5b5c1`
- AP0 manifest SHA `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`

## Qualification

- py_compile PASS
- 25/25 synthetic PASS
- 15/15 mutants KILLED
- static review PASS

## Authorized run

Exactly one local run using AP0 only.

Expected output:
- schema `ATDS_C01_FROZEN_CONFIRMATORY_MODEL_V0_1`
- status `C01_MODEL_FROZEN`
- candidate `CR2-C01-ABS_VOL_X_TICK`
- coverage 1,709,180 minutes / 376,003,618 ticks / 1,606 segments
- 24 tick5 NY-hour medians
- frozen registered thresholds
- B2+ABS_VOL count/probability table
- B2+TICK count/probability table
- B2+ABS_VOL+TICK count/probability table
- canonical model digest
- exact D2026 reproduction evidence
- `confirmation_data_accessed=false`

## Forbidden

No confirmation-window data access.
No confirmatory scoring.
No PnL/direction/strategy/semantic label/MT5.
