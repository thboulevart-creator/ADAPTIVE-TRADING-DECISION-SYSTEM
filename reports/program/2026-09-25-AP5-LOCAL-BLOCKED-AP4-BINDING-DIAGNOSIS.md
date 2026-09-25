# AP5 — local BLOCKED AP4 binding — diagnosis

Date : 2026-09-25
Branch : `integration/system-v1`
Fresh HEAD before persistence : `ab67856d25c8e7cd714c342fffa9578dc58cbe1a`

## Exact blocked evidence

File received from the local AP5 attempt:
- 151 bytes
- SHA-256 `89bb73dd6008ae66a55306f73a29edb25b586496067d050557f8b258dcaa1860`
- schema `ATDS_AP5_BLOCKED_V0_1`
- status `BLOCKED_AP5_AP4_BINDING`
- reason `AP4 evidence missing, escaped repo-root, or SHA mismatch`

Persisted evidence:
`reports/program/evidence/2026-09-25-AP5-LOCAL-BLOCKED-AP4-BINDING.json`

## Local diagnostic

Reported local resolved paths:
- stage: `C:\Users\Boulevart\AppData\Local\Temp\ATDS-AP5-RUN-fcf7f27be22549d0ba78baef6328a002`
- AP4: same stage under `reports\program\evidence\2026-09-25-AP4-PRICE-STRUCTURE.json`
- `AP4_INSIDE_STAGE=True`
- local AP4 SHA-256: `7019e769da721d757bc8f0cf9fc1203e96bfd1923acc92b1cd3e332d5a96e78e`
- local AP4 size: 16,132 bytes
- attributes: Archive

## GitHub verification

At helper commit `715c3e4affa44778785d6c222782eda257ed19e7`, the canonical AP4 evidence:
- exists at the expected path;
- has 15,488 bytes;
- has SHA-256 `c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad`;
- contains exactly 644 LF line endings and zero CRLF pairs.

Observed size delta:
`16,132 - 15,488 = 644`.

This is exactly the number of LF endings in the canonical file. Therefore the local snapshot AP4 underwent a full `LF -> CRLF` line-ending conversion.

## Adjudication

The AP5 helper correctly failed closed. AP4 itself is not contradicted.

Root cause class:
**LOCAL SNAPSHOT TEXT NORMALIZATION — exact byte identity lost for AP4 JSON.**

This is a handoff/materialization issue, not a corpus failure.

## Next governed action

Materialize the AP4 evidence from Git as raw blob bytes, verify the canonical SHA-256, and retry AP5 to a new output path. Do not delete or overwrite the first BLOCKED JSON.
