# RECOVERY CHECKPOINT — 16 SEPTEMBRE 2026 — CLASS-B COMPLETENESS PASS / CALENDAR CLOSURE NEXT

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `feat/multi-year-dukascopy-acquisition`

## Source of truth

GitHub code, persisted reports, tests and qualified workflow evidence are authoritative. Do not reconstruct state from conversation memory.

Construction rule remains:

**UNDERSTAND → COMPARE → BREAK → DECIDE.**

A successful prior mechanism is not, by itself, evidence that the same mechanism is the next correct action.

## Batch 15 V2 — FULLY CLOSED

Atomic integration:

`4dee7e22af1402626341f76611926b108fd1d8c0`

Independent persisted-HEAD re-break:

- corrected verifier: `4bb7712bcab8b8930c4054e1500302621f881f4f`
- authoritative run/job: `35085635675 / 104759660665`
- permissions: `contents: read`
- post-state-safe regression: `65 passed in 0.25s`
- progression regeneration: byte-stable
- final worktree: clean
- verifier mutation: NONE

Verdict:

**PASS — `BATCH15_V2_PERSISTED_HEAD_REBREAK_CONFIRMS_INTEGRATION`**

Durable report:

`reports/data-qualification/historical_trading_breaks_recovery_batch15_v2_persisted_head_rebreak.md`

## Target-day overlap semantic capability V2 — QUALIFIED

Contract:

`TRADING_BREAKS_TARGET_DAY_OVERLAP_ATTRIBUTION_V1`

Current positive-evidence capability:

`TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`

Fingerprint:

`e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31`

Qualified facts:

- target-day cross-date interval attribution: PASS;
- immutable binding to original historical V1 source attempts: PASS;
- all 14 Class-A cases offline readjudicated: `14 PASS / 0 BLOCKED / 0 FAIL`;
- first five were integrated as Batch 15;
- nine Class-A positive V2 PASS decisions remain qualified but not yet integrated;
- no browser/probe/live recapture was needed for the V2 semantic readjudication.

Authoritative readjudication:

`reports/data-qualification/trading_breaks_target_day_overlap_readjudication.md`

## Negative-evidence completeness V1 — QUALIFIED AND RE-BROKEN

Contract:

`TRADING_BREAKS_NEGATIVE_EVIDENCE_COMPLETENESS_V1`

Reference:

`04-REFERENCE/TRADING-BREAKS-NEGATIVE-EVIDENCE-COMPLETENESS.md`

Durable qualification report:

`reports/data-qualification/trading_breaks_negative_evidence_completeness_qualification.md`

Initial qualification:

- HEAD: `ddb781da2a06975903b2a1f67950672d0da3d31e`
- run/job: `35096828077 / 104796142245`
- conclusion: success
- adversarial suite: `20 passed in 0.07s`

Persisted-contract re-break:

- HEAD: `6abae7c94e6e442c2009fcad95869864b0eab739`
- run/job: `35097034040 / 104796843502`
- conclusion: success
- adversarial suite: `20 passed in 0.07s`
- workflow permissions: `contents: read`, `actions: read`
- final worktree: clean

No browser, broker probe or new capture was used. The workflow downloaded only the four already-persisted GitHub Actions artifacts and revalidated their exact SHA-256 digests against runtime/ledger provenance.

Qualified structural property:

`FULL_RANGE_SINGLE_RESPONSE_RAW_LIST_COMPLETENESS`

This rejects direct `matching_records=[] → PASS` promotion. PASS requires full target-day response scope, one target-range request/response pair, no pagination/continuation, complete untruncated JSONP, exact target-instrument raw/DOM controls, exact provenance, and an independent scan of every raw `9016` interval.

### Class-B results

1. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
   - observations: 2
   - repeated consistency: PASS
   - date verdict: **PASS — `NO_BROKER_TRADING_BREAK_INTERVAL_OVERLAPS_TARGET_DAY`**
2. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
   - observations: 1
   - date verdict: **PASS — `NO_BROKER_TRADING_BREAK_INTERVAL_OVERLAPS_TARGET_DAY`**
3. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
   - observations: 1
   - date verdict: **PASS — `NO_BROKER_TRADING_BREAK_INTERVAL_OVERLAPS_TARGET_DAY`**

Overall verdict:

**PASS — `ALL_THREE_CLASS_B_DATES_HAVE_COMPLETE_BROKER_NATIVE_NEGATIVE_EVIDENCE`**

This is qualification only. It does not itself write `NO_SPECIAL_CHANGE_EVIDENCE` into the executable calendar and it does not represent a new broker recovery attempt.

## Current persisted executable state — intentionally unchanged by qualification

Global calendar:

- candidates: `111`
- resolved: `79`
- unresolved: `32`
- FAIL: `0`

Execution-window candidate `2021-08-14 → 2026-08-14`:

- candidates: `68`
- resolved: `56`
- unresolved: `12`
- FAIL: `0`

Recovery state:

- attempt ledger: `73`
- registered material capability changes: `1`
- current positive capability: `TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`
- current fingerprint: `e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31`
- execution window frozen: **NO**
- `.bi5`: **FORBIDDEN**
- real backtest: **NOT AUTHORIZED**

## All 12 in-window unresolved dates now possess qualified decisions

### Remaining Class A — 9 positive V2 PASS decisions

1. `2023-12-25 — CHRISTMAS_OBSERVED`
2. `2024-01-01 — NEW_YEARS_OBSERVED`
3. `2024-03-29 — GOOD_FRIDAY`
4. `2024-12-25 — CHRISTMAS_OBSERVED`
5. `2025-01-01 — NEW_YEARS_OBSERVED`
6. `2025-04-18 — GOOD_FRIDAY`
7. `2025-12-25 — CHRISTMAS_OBSERVED`
8. `2026-01-01 — NEW_YEARS_OBSERVED`
9. `2026-04-03 — GOOD_FRIDAY`

These nine belong to the authoritative `14 PASS / 0 BLOCKED / 0 FAIL` V2 readjudication and do not require Batch 16 / Batch 17 re-processing.

### Class B — 3 negative-evidence PASS decisions

1. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
2. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
3. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

These three are now independently qualified by `TRADING_BREAKS_NEGATIVE_EVIDENCE_COMPLETENESS_V1`.

There is therefore no remaining informational uncertainty inside the selected execution-window candidate. The remaining work is controlled integration of already-qualified decisions.

## Next integration boundary

The next operation is **not** a broker retry and **not** Batch 16.

It is one bounded Trading Breaks **calendar-closure integration** combining all twelve already-qualified unresolved decisions.

The integration must at minimum prove before persistence:

1. membership is exactly the nine remaining Class-A dates plus the three qualified Class-B dates;
2. every Class-A record is bound to its immutable historical source attempt and V2 readjudication evidence;
3. every Class-B `NO_SPECIAL_CHANGE_EVIDENCE` entry is bound to the negative-evidence completeness contract/report and original persisted source observations;
4. no new browser/broker capture is performed;
5. no new broker attempt is fabricated merely to integrate an offline adjudication;
6. historical attempt ledger entries remain unchanged unless a separately versioned accounting contract proves a non-broker integration entry is necessary;
7. the capability-change registry remains unchanged by the integration itself;
8. calendar coverage regressions show no orphan evidence, contradictions or evidence-shape errors;
9. execution-window state becomes exactly `68 candidates / 68 resolved / 0 unresolved / 0 FAIL`;
10. global state becomes exactly `111 candidates / 91 resolved / 20 unresolved`;
11. deterministic progression is regenerated consistently with zero in-window recovery candidates;
12. only the minimum governed state surfaces are changed atomically;
13. an independent persisted-HEAD re-break follows before any execution-window-freeze decision.

The integration may not infer that window freeze or `.bi5` acquisition is automatically authorized merely because unresolved reaches zero; the separate boundary must be evaluated afterward.

## Mandatory recovery order before next substantive write

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. latest `99-BACKUP/SESSION-2026-09-16-TRADING-BREAKS-NEGATIVE-EVIDENCE-COMPLETENESS-PASS.md`
4. `reports/data-qualification/trading_breaks_negative_evidence_completeness_qualification.md`
5. `04-REFERENCE/TRADING-BREAKS-NEGATIVE-EVIDENCE-COMPLETENESS.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch15_v2_persisted_head_rebreak.md`
7. `reports/data-qualification/trading_breaks_target_day_overlap_readjudication.md`
8. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
9. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
10. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
11. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
12. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
13. compare active branch HEAD against the commit containing this checkpoint before any governed-state mutation.

## Exactly one next governed action

**Design, adversarially qualify, and only then atomically execute one bounded Trading Breaks calendar-closure integration for the exact 9 Class-A + 3 Class-B already-qualified decisions, followed by an independent persisted-HEAD re-break.**

Do not create Batch 16 / Batch 17.  
Do not perform a new browser/broker capture.  
Do not acquire `.bi5`.  
Do not run a real backtest.
