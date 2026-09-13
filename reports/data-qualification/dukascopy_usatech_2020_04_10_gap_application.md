# DUKASCOPY USATECH — 2020-04-10 GOOD FRIDAY — GAP APPLICATION

## 1. Target

- Date: `2020-04-10`
- Candidate reason: `GOOD_FRIDAY`
- Instrument: `USATECHIDXUSD` / Dukascopy `USATECH.IDX/USD`
- Intended fact: exact broker special-session classification at whole UTC-hour BI5 granularity.
- Governing rule: `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

This qualification was executed while preserving the previously locked gaps:

- `2019-07-03` — BLOCKED;
- `2020-01-01` — BLOCKED;
- `2020-01-20` — BLOCKED;
- `2020-02-17` — already qualified and locked.

No execution window was frozen and no `.bi5` acquisition was performed.

## 2. Evidence recovered — exchange/reference side

### Official CME Group Good Friday advisory

Source:

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2020-good-friday-advisory.pdf`

The official CME Group Clearing memorandum explicitly identifies:

- `Good Friday, April 10th, 2020`;
- the holiday processing schedule for that date;
- Globex as the applicable trading-hours reference.

The PDF text was retrievable. A screenshot call was also attempted for visual inspection but the screenshot endpoint returned a cache-miss error; this failure is an access limitation and is not evidence either for or against the trading schedule.

### Official CME Good Friday settlement notice

Source:

`https://www.cmegroup.com/tools-information/holiday-calendar/files/good-friday-holiday-settlement-times-2020.pdf`

It states that due to the Good Friday holiday there are no CME Group settlements on Friday `2020-04-10`.

### Preserved CME Globex schedule summary

Source:

`https://www.ampfutures.com/news/holiday-trading-schedule-good-friday-2020`

The page is dated `2020-04-09` and states that it preserves the CME Globex Control Center summary for the `April 9 - 13, 2020` Good Friday holiday schedule.

The preserved schedule image recovered during qualification shows Good Friday `2020-04-10` as fully closed across the listed CME Group product categories, including equity products.

For the strongest favorable gate application, the exact same-date exchange/reference side is therefore treated as present and verified.

## 3. Dukascopy retrieval

Targeted searches covered:

- exact `2020-04-10` / `10 April 2020` / `April 10, 2020` formulations;
- `Good Friday` + `2020` + Dukascopy;
- `Easter weekend market closures 2020`;
- exact `USATECH.IDX/USD` + the target date;
- Swiss and Europe `about/ournews` trees;
- `full-news` routes;
- multilingual variants around Easter / Good Friday;
- archive-index style web searches.

No qualifying Dukascopy 2020 witness was recovered that explicitly identifies `USATECH.IDX/USD` on `2020-04-10` with the special-session treatment required by the calendar contract.

Relevant Dukascopy material found but rejected as substitutes includes:

- exact Easter/USATECH closure schedules from 2017;
- 2019 Easter-weekend closure context;
- 2021 Easter-weekend closure context;
- 2025 and 2026 Easter-weekend closure announcements;
- Dukascopy's 2020 daylight-saving announcement explicitly listing `USATECH.IDX/USD`, which proves the instrument existed and its summer-time schedule context in March 2020 but does **not** prove the Good Friday special session.

Cross-year schedules and regular/summer schedule context are corroborative only under the qualified governance rule.

## 4. Evidence classes under V1

- B0 exact primary broker witness: **absent**
- B1 exact archived broker witness with verified provenance: **absent**
- B2 exact-date broker event explicitly naming target instrument: **absent**
- B3 official broker-to-exchange special-session mapping contract: **absent**
- X0/X1 exact same-date exchange/reference evidence: **present**
- exchange provenance: **accepted as verified for strongest favorable application**
- retrieval materially exhausted: **yes**

No FAIL condition was proven. The missing fact is broker-specific evidence, not exchange timing.

## 5. Gate application

Applying `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` with the strongest favorable exchange assumption yields:

```text
GapDecision(
    verdict='BLOCKED',
    reason='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP',
    route=None,
    contract='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1'
)
```

## 6. Verdict

**BLOCKED**

Reason:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`

This is an absence-of-proof verdict. It does not claim that Dukascopy USATECH was open or closed at any particular hour on `2020-04-10`.

## 7. Executable impact

- no `2020-04-10` record added to `SPECIAL_SESSION_EVIDENCE`;
- no calendar test expectation added or changed;
- no coverage code changed;
- no execution-window state changed;
- no `.bi5` downloaded.

Because no executable calendar/test code changed, the calendar suite and coverage are not rerun merely to create a newer timestamp.

Latest locked executable state therefore remains:

- 34 calendar tests PASS;
- 111 candidate dates;
- 24 resolved candidate dates;
- 87 unresolved candidate dates;
- global coverage verdict BLOCKED.

## 8. Anti-bypass conclusion

Do not promote the full CME Good-Friday closure to Dukascopy broker truth without B0/B1 or complete PASS-C.

Do not reuse 2017/2019/2021/2025/2026 Dukascopy Easter schedules as a hidden template for 2020.

Do not treat the March 2020 Dukascopy daylight-saving announcement as a special-session witness.

Only materially new 2020 date-specific broker evidence may reopen this verdict.
