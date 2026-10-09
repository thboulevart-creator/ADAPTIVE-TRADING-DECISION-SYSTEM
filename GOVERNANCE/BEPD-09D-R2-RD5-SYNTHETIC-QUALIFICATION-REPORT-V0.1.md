# BEPD-09D-R2-RD5 — Synthetic adapter qualification report V0.1
Date: 2026-10-09
Evidence class: **SYNTHETIC_ONLY / FOR_HUMAN_ADJUDICATION**
Authority: explicit human authorization RD5, not automatic human adoption.

## Canonical lineage
Initial authorized HEAD `be08ea7284a6734a942cd618efa2b1db61e40c45`, TREE `3fcaa00e263263cfff924c9252e8791c800984ec`.
Frozen RD4 closure git blob `2122aac53d03370df9f76a0ddae880fd9bf6dcaa`; RD4 receipt `6a8e913db3f250d6c8b16489a85dc66faf43a90a`.
Frozen Candidate B runtime `38588b0a0b9c5b4cb9fcee0c7d524e63d5039c69`; RD2 numeric acceptance blob `ccb519aad05cf0739b54ee50e0521a85a5374f13`.

## RED / GREEN execution evidence
RED preregistration commit `49b024af6c5f94a4242b4ebfe196a8bab7dc084c`; [Actions RED #37920071131](https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/37920071131), one attempt, conclusion `failure` **as preregistered**. Log: `ModuleNotFoundError: No module named 'bepd09d_r2_rd5_training_only_adapter'`. This RED shows the adapter was absent, not that the full negative matrix executed before implementation.

GREEN implementation commit `22f65720b6f18d49d77899d4effd6aafce0e48d7`; [Actions GREEN #37920547662](https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/37920547662), one attempt, conclusion `success`; job `113787146183`. **29/29 frozen synthetic tests PASS**, independent of real historical C1 responses. No RED or GREEN retry occurred in these RD5 runs.

## Tested scope
Synthetic exact 259-week calendar and all five cumulative fold identities; allowed later use of earlier test blocks as later training. Rejected invalid fold, injected current test/week and future weeks, duplicated event, cluster crossing weeks, extra or missing response, invalid side or response type, NaN, zero level price, single-class or deficient design, wrong provenance or closure binding. Checked strict public field allowlist, absence of raw rows or coefficient outputs, no legacy real protocol use, rejection on unexpected LP errors and specifically **masked LP failure on second internal Candidate B detector call**. Performed actual Newton-CG baseline and context **synthetic** training fits, deterministic second replay and one standalone independent synthetic reference-stationarity probe. No new primary-reference coefficient/likelihood parity threshold was adopted.

The new adapter is explicitly `REAL_EXECUTION_PATH_ACTIVATION=False`. Its exposed entry takes *caller-supplied synthetic rows* and a synthetic provenance marker. The marker is a synthetic qualification boundary, **not** a trusted real input materializer and **not** a cryptographic origin proof. The future real trust boundary remains unresolved. The internal detector-exception guard uses scoped Python tracing with an independent pre/post LP feasibility check; this has qualified synthetic tests but does not establish unrestricted real-runtime reliability.

## Static non-regression
Fifteen protected and new Git blobs matched expected identities after GREEN; cumulative initial-RD5-to-GREEN delta contained **eight newly added RD5 files only**, zero previously existing file modifications. Protected RD2/RD3/RD4 and legacy runtime unchanged.

## Explicit unrelated Tier-A failures
On RED push, pre-existing P0.4 run `37920071070` and P0.6 run `37920071103` both concluded `failure`; their logged assertions rejected nine `evidence/berd02/gha_run_35533153289/bodies/*.bi5` files in a diff spanning prior history. The exact RD5 RED diff added no `.bi5` files. These historical Tier-A guards **remain FAIL**, are NOT requalified by RD5, and MUST NOT be presented as repository-wide regression PASS. They are separately actionable, without modification under RD5 authorization.

## Qualification conclusion
`RD5_SYNTHETIC_MATRIX = PASS (29/29)`
`RD5_BOUNDED_SYNTHETIC_IMPLEMENTATION = SYNTHETICALLY_QUALIFIED_FOR_HUMAN_ADJUDICATION_WITH_EXTERNAL_TIER_A_NOTES`
`GLOBAL_REPOSITORY_TIER_A_REGRESSION = NOT_PASS (P0.4/P0.6 failure)`
`HUMAN_ADOPTION = PENDING`
`REAL_TRAINING_FIT = NOT_AUTHORIZED`
`CURRENT_FOLD_REAL_TEST_ACCESS = FORBIDDEN`
`NEW_REAL_LEDGER_READ = NONE`
`REFERENCE_PARITY_METRIC_FOR_REAL = UNADJUDICATED`
`REAL_EXECUTION_BUDGET = UNADJUDICATED`
`REAL_DATA_MATERIALIZER = BLOCKED`
`C1_RETRY = NOT_AUTHORIZED`
`FRESH_OOS = CLOSED`
`TRADING_AUTHORITY = NONE`

**STOP for human adjudication**. No automatic real activation, new workflow run, patch, retry or science.
