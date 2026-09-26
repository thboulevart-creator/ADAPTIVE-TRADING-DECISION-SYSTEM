# C01 frozen confirmatory model — local development-only handoff V0.2

Date: 2026-09-26

## Qualified producer

- blob `13bdc28585e9c6d34bc2217c750f1716fa3e7f9c`
- SHA-256 `a7d1782debb31bee089f99351e1f83345333caf8bb9453d5db3d9be83f1cd4ed`

Dependencies unchanged:
- CR1 helper `bb5cd4acd1b48141019c0ec3796ea61627dc0dbf`
- CR2 helper `34c702e926b3baec90c57b8366177c2db1eca074`
- CR2 evidence `d6543d12fc01405fedb006ddb5d714a772f32678`
- Charter V0.2 `ada0ebf41ecd7ab406d2656ac745ed7003d5b5c1`
- AP0 manifest SHA `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`

Expected:
- schema `ATDS_C01_FROZEN_CONFIRMATORY_MODEL_V0_2`
- status `C01_MODEL_FROZEN`
- model digest `a8b8b823336fb0f7cd5a6b2bbae80d858603b6ff7567fe5e67e4b20c46726c7f`
- `tick5_ny_hour_medians[17] = null`
- `tick5_ny_hour_unavailable = [17]`
- no NaN/Infinity JSON tokens
- exact D2026 reproduction
- confirmation_data_accessed=false

One AP0 development-only rerun authorized.
