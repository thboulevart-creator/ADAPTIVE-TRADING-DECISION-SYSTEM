# DUKASCOPY USATECH — 2020-01-20 MLK GAP APPLICATION

## Target

- Date: `2020-01-20`
- Candidate reason: `MARTIN_LUTHER_KING_DAY`
- Instrument: `USATECHIDXUSD` / `USATECH.IDX/USD`
- Governing contract: `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`
- Coverage envelope: `2018-05-01` through `2026-08-14`

The fact to prove is the exact Dukascopy special-session treatment required to classify whole UTC hourly BI5 buckets on Martin Luther King Jr. Day 2020.

## Starting state

The branch was verified identical to checkpoint `92d9de87dc596277034f842bc50850916487f7eb` before this qualification began.

Previously locked gaps remain unchanged:

- `2019-07-03` — BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`
- `2020-01-01` — BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`

No execution window is frozen and massive native `.bi5` acquisition remains forbidden.

## Candidate identity

The versioned coverage generator independently produces the third Monday of January as `MARTIN_LUTHER_KING_DAY`. For 2020 this is `2020-01-20`, so the target is a real unresolved calendar candidate, not an inferred extra date.

## Exact exchange/reference evidence recovered

### CME Group clearing advisory

Official CME Group source:

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2020-mlk-day-advisory.pdf`

The memorandum is explicitly for:

`Dr. Martin Luther King, Jr., January 20, 2020`

It confirms the exact holiday date and points trading users to the CME holiday-calendar trading schedule.

### Preserved CME Globex Control Center summary

AMP Futures historical page:

`https://www.ampfutures.com/news/holiday-trading-schedule-mlk-2020`

The preserved text states that, from the CME Globex Control Center, the key Monday 20 January 2020 change was:

`Market HALT - Noon Chicago (CST)`

No exchange timing is promoted to broker truth by this report. For the strongest favorable governance application, the same-date exchange/reference side is treated as present and verified; the decision remains BLOCKED even under that favorable assumption.

## Dukascopy retrieval performed

Targeted retrieval covered:

- Dukascopy site searches for `2020-01-20`, `20 January 2020`, `20th January`, `Martin Luther King`, `MLK`, CFD and `USATECH.IDX/USD`;
- Dukascopy Europe and Swiss `about/ournews` variants;
- multilingual pages;
- exact-title searches around `Market closures on Martin Luther King Jr. Day` and `Trading breaks on MLK day`;
- external web/archive-index searches for a preserved 2020 Dukascopy MLK/USATECH witness.

No qualifying 2020 broker witness was recovered.

Historical Dukascopy witnesses from other years were found, including official USATECH-specific MLK schedules for 2016, 2017 and 2018, plus later generic MLK closure announcements. These are corroborative only and are deliberately rejected as substitutes for 2020 because the qualified rule forbids cross-year promotion.

## Evidence classes under V1

### B0 — exact primary broker witness

Absent.

No live/official Dukascopy page was recovered that identifies all of:

- exact date `2020-01-20`;
- exact target instrument `USATECH.IDX/USD`;
- special-session treatment;
- exact close/reopen timing.

### B1 — exact archived broker witness

Absent.

No faithful archived/mirrored copy of an exact 2020 Dukascopy USATECH MLK notice with verifiable provenance was recovered.

### B2 — date-specific broker event witness explicitly covering target instrument

Absent.

No recovered official Dukascopy source for `2020-01-20` explicitly names `USATECH.IDX/USD` as affected.

### B3 — explicit broker-to-exchange special-session mapping contract

Absent.

No official Dukascopy contract was found establishing that USATECH special/holiday trading hours automatically inherit CME equity-index holiday timing.

### X0/X1 — exact same-date exchange/reference timing

Treated as present/verified for the strongest favorable application, based on the exact CME holiday advisory and the preserved CME Globex Control Center summary.

## Adversarial rejection of plausible shortcuts

The following apparent routes are explicitly rejected:

1. `2020 CME exact date + exact halt -> Dukascopy PASS`
   - rejected because exchange-only evidence does not establish broker treatment.
2. `2018 Dukascopy USATECH MLK schedule + 2020 CME schedule -> PASS`
   - rejected as cross-year substitution.
3. `several Dukascopy years show USATECH MLK closures -> PASS`
   - rejected because repeated historical pattern is corroborative-only evidence.
4. `current/later Dukascopy MLK announcements + 2020 CME -> PASS`
   - rejected because wrong-year broker evidence cannot replace the target-year broker link.
5. `holiday identity implies closure`
   - rejected because the candidate holiday name is not itself session evidence.

## Executable governance decision

The qualified gate was applied under the strongest favorable exchange assumption:

```text
EvidenceBundle(
    exact_broker_primary=False,
    exact_broker_archive=False,
    broker_archive_provenance_verified=False,
    date_specific_broker_event=False,
    broker_target_instrument_explicit=False,
    broker_special_session_mapping_contract=False,
    exact_exchange_schedule=True,
    exchange_provenance_verified=True,
    retrieval_exhausted=True,
)
```

Observed decision:

```text
GapDecision(
    verdict='BLOCKED',
    reason='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP',
    route=None,
    contract='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1'
)
```

## Verdict

**BLOCKED**

Reason:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`

This is an absence-of-proof verdict, not evidence that Dukascopy was open or closed at any particular hour.

## Repository consequence

- No `2020-01-20` record is added to `SPECIAL_SESSION_EVIDENCE`.
- No test expectation is added or modified.
- `2020-01-20` remains unresolved in the global coverage envelope.
- `2019-07-03` remains BLOCKED and unchanged.
- `2020-01-01` remains BLOCKED and unchanged.
- No execution window is frozen.
- No `.bi5` is downloaded.

Because no executable calendar/test code changed, the calendar suite and coverage are not rerun merely to create a newer timestamp. The latest observed executable calendar state remains the checkpoint state: 34 GitHub calendar tests, 24 resolved candidate dates, 87 unresolved candidates, global verdict BLOCKED.

## Chronological continuation

`2020-02-17 — PRESIDENTS_DAY` is already versioned as `SPECIAL_PRESIDENTS_DAY_2020` and remains locked; it is not reopened merely to reconstruct history.

Therefore the next unresolved chronological candidate after this blocked MLK date is:

`2020-04-10 — GOOD_FRIDAY`
