# SESSION BACKUP — 2026-09-14 — EXECUTION WINDOW SELECTION

## 0. Purpose

Durable recovery snapshot for the transition from global calendar consolidation to a gap-independent primary execution-window candidate.

Do not reconstruct this step from conversation history.

## 1. Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Branch: `feat/multi-year-dukascopy-acquisition`
- Starting checkpoint/HEAD: `0f9a56e0fb8914f562d85eaa5ac32c107213a61a`
- Global envelope: `2018-05-01` → `2026-08-14`
- Global calendar state: `111 candidates / 24 resolved / 87 unresolved / 0 FAIL`
- Global accounting audit: PASS
- Massive `.bi5` acquisition: FORBIDDEN
- Real backtest: NOT authorized

## 2. Why a separate selection rule was required

`COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1` forbids choosing a five-year window merely because it avoids known gaps.

Therefore the project first versioned a selection rule whose inputs cannot include the gap map or strategy results.

## 3. Rule formalized before application

Rule:

`04-REFERENCE/EXECUTION-WINDOW-SELECTION-RULE.md`

Contract:

`EXECUTION_WINDOW_SELECTION_RULE_V1`

Creation commit:

`65adaa6bb22843c15d48e813326c80e7001c8c4a`

Primary rule:

**Use the most recent contiguous five-calendar-year span ending at the already-governed coverage end.**

Allowed inputs only:

- coverage start/end;
- fixed minimum horizon = 5 calendar years.

Forbidden selection inputs include:

- unresolved/FAIL dates;
- gap counts;
- performance results;
- tick availability by sub-period;
- acquisition convenience;
- source/evidence difficulty by date.

## 4. Scientific / methodological rationale

The rule is grounded in existing repository constraints:

- baseline protocol requires at least five years;
- baseline performs no calibration/optimization;
- execution window must be fixed before results;
- recency is maximized by anchoring at the governed terminal date;
- exactly five years satisfies the primary qualification horizon without silently mixing a larger robustness extension into the first baseline;
- older history may later be used as a separate robustness/historical-extension experiment.

The rule MUST remain the same even if its selected interval contains many gaps.

## 5. Adversarial qualification

Report:

`reports/data-qualification/execution_window_selection_rule_qualification.md`

Commit:

`491ab7b9e3bd8aac4d5dab01d5650ec638ebdd60`

Verdict:

**PASS — `WINDOW_SELECTION_RATIONALE_IS_VERSIONED_AND_GAP_INDEPENDENT`**

Attacks rejected include:

- choose start after a gap;
- minimize gap count across candidate windows;
- snap to full calendar years;
- shorten below five years;
- extend because extra years look easier;
- shift end backward;
- manually delete holidays;
- move after PnL/drawdown;
- move after tick availability;
- manipulate OOS to remove outer-window dates.

## 6. Mechanical application after rule PASS

Application report:

`reports/data-qualification/execution_window_candidate_v1.md`

Creation commit:

`ae83ea08c256d2fdc3b852afd51a4cb2ed7dabe0`

Mechanically produced candidate:

- start: `2021-08-14`
- end: `2026-08-14`
- duration: exactly 5 calendar years
- contiguous: YES
- manual exclusions: NO
- frozen: NO

The boundaries were derived only after the rule and its qualification were versioned.

## 7. In-window calendar state

The candidate window contains exactly **68** generated candidate dates:

- 2021 partial: 6
- 2022: 12
- 2023: 13
- 2024: 14
- 2025: 15
- 2026 bounded: 8

Total:

`6 + 12 + 13 + 14 + 15 + 8 = 68`

Resolved in-window:

- `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

Final in-window state:

- candidates: **68**
- resolved: **1**
- unresolved/BLOCKED: **67**
- FAIL: **0**

Global outside-window unresolved remain:

`87 - 67 = 20`

They remain visible and BLOCKED globally.

## 8. Current boundary application

Updated report:

`reports/data-qualification/current_coverage_execution_window_boundary_application.md`

Update commit:

`e6f859bb1d43aab37fd51e62efc91824b07d011e`

Current matrix:

- global accounting audit: PASS
- window-selection rule: PASS
- window candidate defined: PASS
- global coverage declaration: BLOCKED
- freeze execution window: **BLOCKED — `EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`**
- massive `.bi5` acquisition: BLOCKED
- real backtest: BLOCKED

The previous freeze reason `EXECUTION_WINDOW_NOT_DEFINED` is obsolete because a candidate is now defined.

## 9. Critical anti-loop rule

The 67 in-window dates were already researched during the annual/segment campaigns under the current admissible evidence routes.

Do NOT simply repeat the same generic searches for each date.

Locked rule:

- previously BLOCKED dates reopen only if materially new evidence or a materially new admissible evidence route appears;
- the selected window MUST NOT be shifted to reduce the unresolved count.

## 10. Exactly one next governed action

**Determine whether a materially new broker-origin historical-session evidence route exists that can resolve the 67 in-window BLOCKED candidates in bulk or by new admissible proof.**

Examples of genuinely new route classes to investigate:

- official historical Dukascopy Trading Breaks dataset;
- historical widget/API/backend payload;
- broker-origin export or archive with verified provenance;
- another official Dukascopy historical session record capable of binding date + `USATECH.IDX/USD` + special hours.

Do not reopen date-by-date generic holiday searching without such a new route.

If no new route exists, preserve `EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES` as BLOCKED.

Do not download `.bi5`. Do not start a real backtest.
