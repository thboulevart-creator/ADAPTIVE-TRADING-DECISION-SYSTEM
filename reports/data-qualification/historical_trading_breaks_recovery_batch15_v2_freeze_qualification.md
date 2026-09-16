# Historical Trading Breaks Recovery — Batch 15 V2 freeze qualification

## Verdict

`PASS — BATCH15_V2_RETRY_MEMBERSHIP_ADVERSARIALLY_FROZEN`

## Authoritative freeze

- freeze baseline HEAD: `d6622e8da58e2d4218947ff3f2953fe8e19a2c96`
- qualified freeze HEAD: `8066e82607db1f8de0b406ec36684a6856e0646d`
- workflow: `Trading Breaks Recovery Batch 15 V2 Freeze`
- run: `35067822465`
- job: `104702050599`
- permissions: `contents: read`
- capability: `TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`
- capability fingerprint: `e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31`

## Immutable membership

The membership is exactly the first five rows of the governed V2 eligible recovery queue at the freeze baseline:

1. `2021-12-24 — CHRISTMAS_OBSERVED`
2. `2022-04-15 — GOOD_FRIDAY`
3. `2022-12-26 — CHRISTMAS_OBSERVED`
4. `2023-01-02 — NEW_YEARS_OBSERVED`
5. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`

At qualification time:

- raw unresolved queue: `17`
- governed V2 eligible queue: `14`
- historical attempt ledger: `68`
- material capability changes: `1`
- batch size: `5`

## Adversarial qualification

The authoritative run proved that the frozen list equals `eligible_recovery_queue()[:5]` and rejected:

- shrink;
- expansion;
- reverse order;
- pair reordering;
- duplicate insertion;
- skip-first sliding window;
- substitution with the sixth eligible row.

Each frozen target is a prior V1 `BLOCKED` attempt with blocker `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE` and is eligible only through the qualified material capability change. The public progression verdict is `MATERIAL_CAPABILITY_CHANGE_RETRY`.

The freeze source contains no browser, Selenium, Playwright, probe, or readjudication-data access path. The persisted progression report remained byte-stable and the final worktree was clean.

## Governing consequence

No execution/evidence selection, adjudication, calendar mutation, attempt-ledger append, or next-batch freeze is admissible until this persisted membership has passed an independent read-only persisted-HEAD re-break.
