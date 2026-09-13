# DUKASCOPY USATECH — 2019-07-03 HISTORICAL BROKER WITNESS SEARCH

## Scope

Target date: `2019-07-03`
Candidate reason: `INDEPENDENCE_PRE_HOLIDAY_SESSION`
Instrument: `USATECH.IDX/USD`
Required threshold: a materially date-specific Dukascopy/USATECH broker witness. CME-only timing is insufficient. Cross-year extrapolation is forbidden.

## Starting state

- Active branch: `feat/multi-year-dukascopy-acquisition`
- Starting checkpoint: `3a39e86d457095ca99d782b4eb48cc206cbefa2f`
- Branch was verified identical to that checkpoint before this search.
- Existing exact CME-derived 2019 evidence indicates ES/NQ/YM early close at 12:15 Chicago time on Wednesday 3 July 2019, corresponding to a partially tradable 17 UTC hour and fully closed exchange buckets 18-21 UTC.
- The missing proof is broker-specific Dukascopy treatment for USATECH on this exact date.

## Search performed

The search was deliberately restricted to finding a new historical broker witness rather than reopening the closed Trading Breaks widget route.

Search dimensions included:

- `site:dukascopy.com` + `2019 July 3` + `US Independence Day` + `USATECH`;
- exact `USATECH.IDX/USD` + `3 July 2019` / `July 3, 2019`;
- exact `17:15` + Dukascopy + USATECH + 2019;
- Dukascopy company-news pages around 1-5 July 2019;
- exact publication timestamps around `2019-07-01T12:00:00Z`, `2019-07-02T12:00:00Z`, and `2019-07-03T12:00:00Z`;
- multilingual Dukascopy pages;
- external indexed/archive references and RSS/news-digest style mirrors;
- official/social-web searches for a Dukascopy Independence-Day trading-hours notice from July 2019.

## Relevant witnesses found

### Official Dukascopy 2018 — qualifying for 2018 only

`https://www.dukascopy.com/swiss/english/about/ournews/us-independence-day-on-wednesday-4th-july`

Published 29 June 2018. It explicitly states for CFD indexes including `USATECH.IDX/USD`:

- trading stops at 17:15 GMT on Tuesday 3 July 2018;
- markets reopen at 22:00 GMT on Tuesday 3 July 2018.

This is strong broker-specific evidence, but for 2018 only. It MUST NOT be extrapolated to 2019.

### Official Dukascopy 2017 — non-qualifying for 2019

`https://www.dukascopy.com/europe/french/about/ournews/holiday-on-4-july-in-the-us`

Published 30 June 2017. It identifies a July-3 pre-holiday CFD closure for `USATECH.IDX/USD`, but at a different historical time and year. This reinforces why cross-year extrapolation would be unsafe.

### Official Dukascopy 2015 — non-qualifying for 2019

`https://www.dukascopy.com/swiss/english/about/ournews/us-independence-day-trading-hours`

Published 2 July 2015. It contains a July-3 USATECH closure for that year's observed holiday. Wrong year and different calendar configuration.

### Official Dukascopy 2026 — non-qualifying for 2019

`https://www.dukascopy.com/swiss/english/about/ournews/market-closures-on-independence-day-in-the-us-dbl203546`

Published 1 July 2026. It confirms that Dukascopy can apply special breaks on a July-3 pre-holiday session in some years, but it is not evidence for 2019.

### Dukascopy pages genuinely dated 3 July 2019

The indexed historical site does contain Dukascopy material from 3 July 2019, including market-research/company material. This means the failure to find the required witness is not simply because the date is absent from the searchable Dukascopy corpus. None of the retrieved 3-July-2019 pages establishes a USATECH special broker break.

### Current Dukascopy regular USATECH schedule — context only

The current Dukascopy range-of-markets page identifies `USATECH.IDX/USD` regular summer hours as Sun-Fri 22:00-20:15 GMT with a 20:15-22:00 daily break. This is regular-session context, not proof of the special 2019-07-03 holiday treatment.

## Archive-path limitation

A direct CDX/Wayback query was attempted from the local execution environment for Dukascopy `about/ournews` captures around 1-5 July 2019. The environment has no direct DNS/network route to `web.archive.org`, so that archive endpoint could not be queried there.

This network limitation is NOT interpreted as evidence that no archived page exists. However, web-index searches for Wayback/archived copies also returned no qualifying 2019-07-03 Dukascopy/USATECH witness.

## Adversarial conclusion

What remains proven:

- exact 2019 exchange timing exists for the July-3 early close;
- Dukascopy had year-specific July-3 pre-holiday USATECH breaks in some other years;
- Dukascopy regular summer USATECH schedule is known.

What remains unproven:

- that Dukascopy applied the 2019 CME July-3 early close to `USATECH.IDX/USD` on `2019-07-03`;
- the exact Dukascopy 2019 July-3 stop/reopen times.

Using 2018, 2017, 2015, or 2026 as a substitute would violate the locked no-cross-year-extrapolation rule. Using CME-only timing would violate the locked broker-evidence threshold.

## Verdict

**BLOCKED**

Reason: `DATE_SPECIFIC_DUKASCOPY_USATECH_2019_07_03_WITNESS_NOT_FOUND`

No calendar record is added for `2019-07-03`.
No test expectation is changed.
No coverage PASS is claimed.
Massive `.bi5` acquisition remains forbidden.
