# C01 frozen-model V0.1 — non-standard JSON incident

Date: 2026-09-26

## Observed successful development run

The qualified V0.1 producer completed on the AP0 development corpus.

Exact local output identity:
- bytes: 2,597,107
- SHA-256: `05cb33679a48ba683ba6a68b95a371ed7ec630df24c237bebbdab404f8200b31`
- Git blob: `010a77df979d4b5347686320bb338d4dffdd28d0`
- model digest: `a8b8b823336fb0f7cd5a6b2bbae80d858603b6ff7567fe5e67e4b20c46726c7f`
- train_valid_n: 1,535,174
- D2026 reproduction: exact
- confirmation_data_accessed: false

## Defect

The 24-hour tick5 NY-hour median vector contains one structurally unavailable hour:
- NY hour 17 = undefined because no finite development tick5 observations exist for that hour.

The CR1-qualified semantics already represent such an unavailable hour internally as `np.nan` and exclude it from relative normalization.

However Python `json.dumps` defaulted to `allow_nan=True`, so V0.1 serialized that internal value as the token `NaN`.

`NaN` is not valid standard JSON.

Therefore the V0.1 file is retained as execution evidence but **is not accepted as the sealed confirmatory model artifact**.

## Scientific impact

None.

The internal model is unchanged:
- same 24-element numeric vector internally;
- same unavailable NY hour 17;
- same thresholds;
- same count matrices;
- same Laplace probabilities;
- same D2026 reproduction;
- same canonical model digest.

This is a representation/portability correction only.

## Corrective candidate V0.2

The producer now:
- serializes unavailable hour medians as JSON `null`;
- serializes `tick5_ny_hour_unavailable: [17]`;
- requires the unavailable set to be exactly `[17]`;
- writes with `allow_nan=False`;
- emits schema `ATDS_C01_FROZEN_CONFIRMATORY_MODEL_V0_2`.

The canonical model digest remains computed on the internal numeric arrays, including the same IEEE NaN slot, so the expected digest remains:
`a8b8b823336fb0f7cd5a6b2bbae80d858603b6ff7567fe5e67e4b20c46726c7f`.

Local corrective qualification before persistence:
- py_compile PASS
- 29/29 synthetic PASS
- 17/17 mutation breakers KILLED

No confirmation data was accessed.
