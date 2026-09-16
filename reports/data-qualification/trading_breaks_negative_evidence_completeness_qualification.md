# Trading Breaks Negative Evidence Completeness V1 — Qualification

## Verdict

**PASS — `ALL_THREE_CLASS_B_DATES_HAVE_COMPLETE_BROKER_NATIVE_NEGATIVE_EVIDENCE`**

Contract:

`TRADING_BREAKS_NEGATIVE_EVIDENCE_COMPLETENESS_V1`

Qualified property:

`FULL_RANGE_SINGLE_RESPONSE_RAW_LIST_COMPLETENESS`

## Authoritative executions

Initial adversarial qualification:

- HEAD: `ddb781da2a06975903b2a1f67950672d0da3d31e`
- run/job: `35096828077 / 104796142245`
- conclusion: `success`

Persisted-contract re-break:

- HEAD: `6abae7c94e6e442c2009fcad95869864b0eab739`
- run/job: `35097034040 / 104796843502`
- conclusion: `success`

Both workflows used:

- `contents: read`
- `actions: read`
- no browser;
- no broker probe;
- no new capture;
- no calendar mutation;
- no attempt-ledger mutation;
- no progression mutation;
- no capability-registry mutation;
- no execution-window mutation.

The persisted-contract re-break finished with a clean worktree.

## Adversarial boundary

Executable validator:

`tools/trading_breaks_negative_evidence_completeness.py`

Tests:

`tests/test_trading_breaks_negative_evidence_completeness.py`

Observed result on both authoritative runs:

`20 passed in 0.07s`

The attacks reject at least:

- HTTP 200 without raw payload;
- date fallback;
- wrong/missing instrument identity;
- raw target record hidden by normalized filtering;
- positive raw target-day overlap disguised as negative evidence;
- capture truncation/unreadable response;
- pagination/continuation uncertainty;
- partial target-day scope;
- missing/multiple target-range response identity;
- adjacent-date/other-year borrowing;
- runtime/network errors;
- artifact/runtime/ledger provenance mismatch;
- malformed/incomplete JSONP;
- missing target-instrument raw or DOM controls;
- inconsistent repeated observations;
- direct `matching_records=[] → PASS` promotion.

## Persisted source artifacts

No broker data was recaptured. The workflow downloaded only the four already-versioned GitHub Actions artifacts and independently rechecked their SHA-256 values:

- artifact `10364872726` → `95d6d820393a358a5539f7959ffa06d240b344b1182a57b5b4f13bb43cb74a1f`
- artifact `10364984459` → `ecd110649b1049d308171357ff0574aee4a8670c0d4f35c018854d7d3771ceab`
- artifact `10367930592` → `994d0f4832400c05bd8fc46e07637e9b68590af1c4b37816ae0cbf650c04bd41`
- artifact `10418961548` → `00dd2044a76d926417779d22c7ce08b67318a9d00933b9cac1bc980f2a7c9910`

All four digests match the persisted runtime/attempt provenance.

## Date-level adjudication

### 2021-12-31 — PASS

Candidate reason:

`NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`

Two independent persisted observations were available and are mutually consistent.

Each observation proves:

- exact historical date honored;
- `USATECH.IDX/USD` / instrument `9016` identity exact;
- successful target-range broker response;
- explicit response range covers the complete UTC target day;
- exactly one target-range request/response pair;
- no pagination/continuation;
- complete parseable JSONP list;
- raw body `115439` bytes, below the `1_000_000`-byte capture ceiling;
- raw list `1075` rows;
- same-response raw target-instrument control exists: record `31532 — Christmas Day`;
- official rendered page contains the same target instrument;
- independent scan of every raw `9016` interval finds zero interval overlapping `2021-12-31`;
- normalized `matching_records` count is also zero.

Date verdict:

**PASS — `NO_BROKER_TRADING_BREAK_INTERVAL_OVERLAPS_TARGET_DAY`**

### 2022-07-01 — PASS

Candidate reason:

`INDEPENDENCE_PRE_HOLIDAY_SESSION`

Persisted evidence proves:

- exact date/instrument/provenance;
- full target-day response scope;
- no pagination/continuation;
- complete parseable JSONP list;
- raw body `87078` bytes;
- raw list `789` rows;
- raw `9016` control record `41225 — Independence Day` begins on `2022-07-04`;
- independent target-day overlap count: `0`;
- normalized matching count: `0`.

Date verdict:

**PASS — `NO_BROKER_TRADING_BREAK_INTERVAL_OVERLAPS_TARGET_DAY`**

### 2026-07-02 — PASS

Candidate reason:

`INDEPENDENCE_PRE_HOLIDAY_SESSION`

Persisted evidence proves:

- exact date/instrument/provenance;
- full target-day response scope;
- no pagination/continuation;
- complete parseable JSONP list;
- raw body `81478` bytes;
- raw list `726` rows;
- raw `9016` control record `101959 — Independence Day` begins on `2026-07-03`;
- independent target-day overlap count: `0`;
- normalized matching count: `0`.

Date verdict:

**PASS — `NO_BROKER_TRADING_BREAK_INTERVAL_OVERLAPS_TARGET_DAY`**

## What this PASS means

The three dates previously blocked by `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED` now possess independently qualified negative broker evidence under a separate completeness contract.

The permitted factual statement is exactly:

`NO_BROKER_TRADING_BREAK_INTERVAL_OVERLAPS_TARGET_DAY`

This qualification does **not** itself write `NO_SPECIAL_CHANGE_EVIDENCE` into the executable calendar.

## Current state remains unchanged

Because this block is qualification-only:

Global calendar remains:

- `111` candidates
- `79` resolved
- `32` unresolved
- `0` FAIL

Execution-window candidate `2021-08-14 → 2026-08-14` remains:

- `68` candidates
- `56` resolved
- `12` unresolved
- `0` FAIL

Attempt ledger remains `73`.

The twelve unresolved dates now all possess qualified decisions outside the executable calendar:

- `9` Class A positive overlap-V2 PASS;
- `3` Class B negative-evidence PASS.

## Executable consequence

The next governed block is one bounded **Trading Breaks calendar-closure integration**, not Batch 16 / Batch 17 and not another broker probe.

That integration must:

1. bind the nine remaining Class-A dates to their already-qualified V2 positive decisions;
2. bind the three Class-B dates to this negative-evidence completeness PASS;
3. preserve all historical broker attempts and source provenance;
4. avoid fabricating new broker attempts or new captures;
5. mutate only the minimum governed calendar/progression surfaces justified by the qualified evidence;
6. rerun calendar, coverage and execution-window regressions;
7. target execution-window state `68 resolved / 0 unresolved / 0 FAIL`;
8. target global state `111 candidates / 91 resolved / 20 unresolved`;
9. be followed by an independent persisted-HEAD re-break before any execution-window freeze decision.

No `.bi5`. No real backtest.
