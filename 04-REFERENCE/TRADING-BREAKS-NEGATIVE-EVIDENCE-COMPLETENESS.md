# TRADING BREAKS NEGATIVE EVIDENCE COMPLETENESS

Contract:

`TRADING_BREAKS_NEGATIVE_EVIDENCE_COMPLETENESS_V1`

## Status

**PASS — `ALL_THREE_CLASS_B_DATES_HAVE_COMPLETE_BROKER_NATIVE_NEGATIVE_EVIDENCE`.**

Initial adversarial qualification:

- qualification HEAD: `ddb781da2a06975903b2a1f67950672d0da3d31e`
- workflow: `Trading Breaks Negative Evidence Completeness V1`
- run/job: `35096828077 / 104796142245`
- permissions: `contents: read`, `actions: read`
- adversarial suite: `20 passed in 0.07s`
- browser / broker probe / new capture: `NONE`
- governed Trading Breaks state mutation: `NONE`

This contract is deliberately narrower than the positive-record route. It determines whether an already-persisted official Dukascopy Trading Breaks response is complete enough to support the negative statement:

> no `USATECH.IDX/USD` broker-native Trading Breaks interval overlaps the exact addressed target day.

It does **not** infer regular hours from `matching_records=[]` alone.

## Scope

Target instrument:

- `USATECH.IDX/USD`
- instrument ID `9016`

Qualified Class-B targets:

1. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
2. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
3. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

Only already-persisted captures are admissible. No browser, probe, broker recapture, calendar mutation, attempt-ledger mutation, progression mutation, capability-registry mutation, execution-window mutation, `.bi5`, or backtest is authorized by this contract.

## Qualified completeness property

A negative decision is admissible only if the raw broker response proves:

`FULL_RANGE_SINGLE_RESPONSE_RAW_LIST_COMPLETENESS`

For one persisted observation, all of the following are mandatory:

1. artifact bytes match the persisted SHA-256 exactly;
2. runtime, ledger, workflow run, job, artifact ID, digest and probe commit provenance agree;
3. requested date is exactly the candidate date and the historical date was honored;
4. observed instrument identity is exactly `USATECH.IDX/USD` / `9016`;
5. runtime and artifact runtime-error sets are empty;
6. the target Trading Breaks request is HTTP-successful and its explicit `start` / `end` scope covers the complete UTC target day;
7. exactly one target-range `group=trading&method=breaks` request/response pair represents that scope;
8. no pagination/cursor/offset/limit continuation mechanism is present in that target request;
9. the raw response body is retained, has no body-read error, is below the capture implementation's `1_000_000`-byte retention ceiling, and parses as a syntactically complete JSONP list;
10. the same full-range raw list contains at least one broker record for instrument `9016`, proving that the target instrument is represented inside the response scope;
11. the rendered official-widget page independently contains `USATECH.IDX/USD` for that same observation, providing an internal raw/DOM instrument control;
12. an independent interval scan of **every raw `9016` record** finds zero intervals overlapping the exact UTC target day;
13. the independent raw scan and the persisted normalized `matching_records` result agree exactly;
14. no adjacent date, other year, holiday-name inference, exchange timing, or another observation is borrowed as target-day evidence.

For a target date with multiple historical observations, all independently valid observations must also agree on the canonical raw target-instrument record set and on the zero-overlap result. Repetition is a consistency check only; it cannot replace structural completeness.

## Qualified observations

### 2021-12-31

Two independently persisted observations passed.

- artifacts: `10364872726`, `10364984459`
- artifact digests matched the versioned ledger/runtime provenance exactly;
- raw response: `1075` rows, `115439` bytes in each observation;
- full response scope includes the complete target day;
- no pagination/continuation detected;
- target-instrument raw/DOM control present;
- raw `9016` control record: `31532 — Christmas Day`, ending before the target day;
- independent raw overlap count for `2021-12-31`: `0`;
- normalized matching count: `0`;
- repeated-observation consistency: PASS.

### 2022-07-01

- artifact: `10367930592`
- raw response: `789` rows, `87078` bytes;
- full response scope includes the complete target day;
- no pagination/continuation detected;
- target-instrument raw/DOM control present;
- raw `9016` control record: `41225 — Independence Day`, beginning on `2022-07-04`;
- independent raw overlap count for `2022-07-01`: `0`;
- normalized matching count: `0`.

### 2026-07-02

- artifact: `10418961548`
- raw response: `726` rows, `81478` bytes;
- full response scope includes the complete target day;
- no pagination/continuation detected;
- target-instrument raw/DOM control present;
- raw `9016` control record: `101959 — Independence Day`, beginning on `2026-07-03`;
- independent raw overlap count for `2026-07-02`: `0`;
- normalized matching count: `0`.

All three date-level decisions are therefore:

**PASS — `NO_BROKER_TRADING_BREAK_INTERVAL_OVERLAPS_TARGET_DAY`.**

## Decision semantics

### PASS

A Class-B observation may receive negative-evidence PASS only when every structural completeness property above is proven and the independent raw scan finds zero target-day-overlapping `9016` intervals.

The admissible statement is narrow:

`NO_BROKER_TRADING_BREAK_INTERVAL_OVERLAPS_TARGET_DAY`

Only a separately governed integration may translate that statement into executable `NO_SPECIAL_CHANGE_EVIDENCE`.

### BLOCKED

Use BLOCKED when the response could be negative but completeness is not proven, including:

- missing raw payload;
- unreadable or capture-truncated body;
- pagination/continuation uncertainty;
- incomplete target-day request scope;
- missing same-response target-instrument control;
- runtime/network error;
- response structure that cannot prove one complete list for the target scope.

BLOCKED does not authorize a same-capability retry. The next material route must explicitly address `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`.

### FAIL

Use FAIL for contradictions or integrity violations, including:

- wrong date or instrument;
- provenance mismatch;
- raw target-day overlap hidden by normalized filtering;
- inconsistent repeated observations;
- borrowed adjacent/other-year evidence;
- positive interval presented as negative evidence.

## Adversarial qualification

The executable validator:

`tools/trading_breaks_negative_evidence_completeness.py`

was attacked by:

`tests/test_trading_breaks_negative_evidence_completeness.py`

The qualified suite rejects at minimum:

1. HTTP `200` with missing raw payload;
2. date fallback / date not honored;
3. wrong or missing instrument identity;
4. normalized filtering that hides a raw target-instrument record;
5. raw target-day overlap while normalized matches are empty;
6. capture truncation or unreadable raw response;
7. pagination/continuation or target scope that does not prove the full target day;
8. adjacent-date / other-year borrowing;
9. runtime/network errors presented as negative evidence;
10. provenance mismatch between runtime, ledger, artifact digest, job and probe commit;
11. inconsistent repeated observations;
12. direct `matching_records=[] -> PASS` promotion without the independent structural completeness property.

Observed result:

`20 passed in 0.07s`

The initial qualification workflow then independently downloaded the four pre-existing source artifacts from GitHub Actions, rechecked every persisted SHA-256, extracted the raw request/response/page evidence, and produced:

`3 PASS / 0 BLOCKED / 0 FAIL`.

## Downstream boundary

Contract qualification and Class-B adjudication do not themselves mutate the calendar.

The three Class-B dates now possess qualified negative-evidence PASS decisions, while the nine remaining Class-A dates already possess qualified positive V2 PASS decisions.

The next governed operation is therefore one bounded **calendar-closure integration** combining:

- the nine already-qualified remaining Class-A positive V2 PASS dates; and
- the three Class-B negative-evidence PASS dates.

That later integration must preserve historical attempts, must not fabricate new broker observations, must regenerate progression, and must be followed by an independent persisted-HEAD re-break.

No `.bi5`. No real backtest.
