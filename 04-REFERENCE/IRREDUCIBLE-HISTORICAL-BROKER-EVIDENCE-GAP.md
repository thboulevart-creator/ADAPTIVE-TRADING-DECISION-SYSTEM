# IRREDUCIBLE HISTORICAL BROKER EVIDENCE GAP — GOVERNANCE RULE V1

## 1. Purpose

This rule governs historical calendar/session qualification when exhaustive retrieval cannot recover the original date-specific broker witness.

It exists to prevent two opposite failures:

1. a **false PASS** produced by filling a historical broker gap with plausible but non-equivalent evidence; and
2. a permanent research loop that repeatedly searches for the same missing page without changing the evidence state.

This rule does **not** weaken the existing Dukascopy calendar threshold. It defines exactly when a missing live primary page may be replaced by a sufficiently strong historical evidence chain, and when the only valid outcome remains BLOCKED.

Allowed verdicts remain only: **PASS / FAIL / BLOCKED**.

Rule contract: `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`.

## 2. Preconditions

This rule may be invoked only when all of the following are true:

- the target is a historical broker session/calendar fact;
- the target date, instrument, and fact to be proven are explicitly identified;
- normal primary-source retrieval has been attempted;
- archive/mirror retrieval has been attempted where materially available;
- the failed retrieval path and searched evidence are durably recorded;
- the missing witness is not being inferred from HTTP failure, missing market data, or a holiday name;
- no already-valid date-specific broker witness is being ignored merely because another route is easier.

If retrieval is not yet materially exhausted, the verdict is **BLOCKED — RETRIEVAL_INCOMPLETE**, not an irreducible-gap decision.

## 3. Evidence classes

### B0 — Exact primary broker witness

A live/official broker source that identifies:

- the exact target date;
- the exact target instrument/symbol;
- the special-session treatment; and
- the exact close/reopen time needed to classify the requested buckets.

B0 is sufficient for PASS if internally coherent.

### B1 — Exact archived broker witness

A preserved historical copy of official broker content that identifies the same four facts as B0.

B1 is admissible only when provenance is verifiable, including enough information to establish that the archived/mirrored content is a faithful copy of the broker's historical publication rather than a third-party paraphrase.

Examples of acceptable provenance can include an archived official URL/capture identity or a preserved exact copy with traceable original broker URL/date/content.

B1 is sufficient for PASS if provenance is verified and no equal-or-higher-rank contradiction exists.

### B2 — Date-specific broker event witness

An official broker source for the **exact target date** that explicitly identifies the **exact target instrument/symbol** as affected by a special session/event but does not provide sufficiently precise hours.

A generic statement such as "U.S. markets may close early" is not B2 unless the target instrument is explicitly and unambiguously in scope.

B2 alone is not sufficient for PASS.

### B3 — Explicit broker-to-exchange special-session mapping contract

Official broker documentation that explicitly establishes that the target instrument's **special/holiday session timing** follows a named reference exchange/product schedule.

Similarity of regular trading hours is not B3.
Repeated historical coincidence is not B3.
A model inference that the broker "normally follows CME" is not B3.

### X0 — Exact primary exchange/reference schedule

An official exchange/reference-market source for the exact target date and exact mapped product/session, with timing precise enough for the requested bucket classification.

### X1 — Exact archived exchange/reference schedule

A faithful historical copy/mirror of X0 whose provenance and target date/product are sufficiently verifiable. It must remain explicitly labelled archive/mirror evidence and must not be relabelled as a live primary source.

## 4. Corroborative-only evidence — never sufficient to create PASS

The following can support investigation but cannot independently or collectively substitute for the required broker link:

- exact broker schedules from other years;
- same holiday name in another year;
- current broker regular trading hours;
- exact exchange timing without a valid broker linkage route;
- third-party paraphrases of broker hours without verifiable preserved broker content;
- another broker's schedule;
- missing `.bi5` files or absent ticks;
- HTTP 403/404/503 responses;
- empty historical widgets;
- search-engine non-results;
- social posts that do not preserve an exact attributable broker statement;
- statistical regularity or majority-of-years reasoning.

No number of corroborative-only items may be summed into a PASS.

## 5. PASS routes

There are exactly three admissible PASS routes.

### PASS-A — Exact live broker proof

Requirements:

- B0 present;
- target date/instrument identity verified;
- exact timing sufficient for bucket classification;
- no unresolved equal-or-higher-rank contradiction.

### PASS-B — Exact archived broker proof

Requirements:

- B1 present;
- archive/mirror provenance verified;
- target date/instrument identity verified;
- exact timing sufficient for bucket classification;
- no unresolved equal-or-higher-rank contradiction.

### PASS-C — Broker event + explicit mapping + exact exchange timing

All of the following are mandatory:

1. B2: official broker evidence for the exact target date;
2. B2 explicitly identifies the target instrument/symbol as affected;
3. B3: official broker documentation explicitly maps **special/holiday** timing for that instrument to the named reference exchange/product;
4. X0 or verified X1: exact same-date reference timing for the mapped product;
5. date/product/time-zone conversion is explicit and reproducible;
6. partial tradable hours remain open at hourly-bucket granularity;
7. no unresolved equal-or-higher-rank contradiction.

If any one item is absent, PASS-C is unavailable.

## 6. FAIL conditions

The rule returns **FAIL** when the evidence/control itself is contradictory or malformed, including:

- two equal-or-higher-rank broker witnesses for the same date/instrument materially disagree and the conflict cannot be reconciled;
- a claimed exact witness is proven to refer to the wrong date or wrong instrument;
- an archive/mirror is presented as exact broker evidence but its provenance is falsified or its content is shown not to be a faithful broker copy;
- a supposed broker-to-exchange mapping contract does not actually cover special/holiday sessions or the target instrument;
- the proposed bucket conversion contradicts the proven source timing.

FAIL is not used merely because evidence is missing. Missing evidence remains BLOCKED.

## 7. BLOCKED conditions

The rule returns **BLOCKED** whenever no PASS route is complete and no FAIL condition is proven.

Important mandatory BLOCKED combinations include:

- exact same-date exchange timing with no same-date broker witness;
- same-date broker event evidence plus exact exchange timing but no explicit B3 special-session mapping contract;
- B3 + exchange timing but no same-date broker event witness B2;
- exact broker timing from another year + exact same-date exchange timing;
- multiple other-year broker examples showing a pattern;
- broker notice for a different date, even inside the same holiday week;
- generic broker holiday context that does not explicitly include the target instrument;
- exact archived broker content whose provenance cannot be verified;
- missing data / HTTP failures / empty widget / search failure;
- a historically plausible classification that cannot cross one of PASS-A/B/C.

When retrieval has been materially exhausted, the reason becomes:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`

This is still BLOCKED. "Irreducible" records the retrieval state; it does not convert uncertainty into truth.

## 8. Priority and contradiction rules

Evidence priority is:

`B0 > B1 > (B2 + B3 + X0/X1) > corroborative evidence`

A stronger broker-specific witness may legitimately differ from the exchange schedule because the calendar being qualified is the broker instrument calendar.

Therefore an exchange/broker difference is not automatically FAIL when B0/B1 explicitly proves a broker-specific schedule. The broker-specific exact witness controls.

However, unresolved contradictions between two exact broker witnesses of comparable authority are FAIL until reconciled.

## 9. Anti-bypass invariants

The following shortcuts are forbidden:

- replacing `exact target date` with `same holiday in another year`;
- replacing `exact instrument` with `same asset class` unless the source itself explicitly includes the target instrument;
- replacing B3 with an observed resemblance between regular broker and exchange hours;
- treating two weak sources as equivalent to one exact source;
- using data absence as closure proof;
- using a future or past broker schedule as a hidden template;
- downgrading a contradiction to BLOCKED merely to preserve a preferred classification;
- changing the evidence threshold after seeing the desired calendar result.

## 10. Required durable application record

Every invocation must record:

- target date;
- target instrument;
- fact to prove;
- retrieval-exhaustion status;
- evidence classes actually present;
- evidence classes missing;
- contradictions checked;
- exact PASS route attempted, if any;
- verdict PASS / FAIL / BLOCKED;
- machine-readable reason code;
- whether calendar/test code changed.

## 11. Qualification requirement before use

This rule is not valid merely because this document exists.

Before first application it must undergo the repository protocol:

**formalisation → candidate → adversarial break → correction → re-break → verdict**

The qualification must specifically attack false-PASS routes involving cross-year evidence, exchange-only evidence, generic broker notices, archive provenance, missing data, and hidden broker/exchange divergence.

Only after the rule itself receives PASS may it be applied to `2019-07-03` or any other historical gap.
