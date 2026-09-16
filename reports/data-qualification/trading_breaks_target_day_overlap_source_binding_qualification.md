# Trading Breaks target-day overlap — immutable Class-A source binding qualification

## Verdict

`PASS — CLASS_A_HISTORICAL_EVIDENCE_BOUND_TO_IMMUTABLE_SOURCE_ATTEMPTS`

- qualified source-binding HEAD: `e09c46713ff63296a6411a9274c7b21f63797054`
- workflow run/job: `35068690388 / 104704823928`
- permissions: `contents: read`
- semantic contract: `TRADING_BREAKS_TARGET_DAY_OVERLAP_ATTRIBUTION_V1`

The loader now resolves each of the 14 persisted Class-A runtime evidences through its exact historical V1 source attempt (`batchNN:YYYY-MM-DD`) rather than the latest attempt for that date.

Adversarial qualification proved that:

- all 14 historical source attempts remain exact V1 `BLOCKED` attempts for `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`;
- governed provenance fields match the source runtime evidence;
- a later synthetic V2 PASS retry cannot shadow or replace the original evidence binding;
- corrupted source-attempt identity is rejected;
- all 14 target-day overlap semantic cases still requalify PASS offline;
- the qualification is repository read-only.

This gate is required before integrating V2 retries because future batches must remain able to reproduce the original persisted evidence after earlier Class-A dates acquire newer PASS attempts.
