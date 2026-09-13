# SESSION BACKUP — 2026-09-13 — MULTI-YEAR DUKASCOPY CALENDAR COVERAGE

## Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- Prior authoritative checkpoint before this governance block: `b8b29ab936dc32058f2d589c46ff33fa46329799`
- Instrument: `USATECHIDXUSD` / Dukascopy `USATECH.IDX/USD`
- Coverage envelope: `2018-05-01` through `2026-08-14`
- Execution/backtest window: NOT frozen
- Massive native `.bi5` acquisition: FORBIDDEN while the governing acquisition gate is unresolved

## Source-of-truth verification

Before this block, GitHub comparison proved branch `feat/multi-year-dukascopy-acquisition` was exactly identical to checkpoint `b8b29ab936dc32058f2d589c46ff33fa46329799` (`ahead_by=0`, `behind_by=0`).

The governed recovery chain was consulted before writes:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. `04-REFERENCE/RECOVERY-CHECKPOINT.md`
3. this durable session backup
4. prior `2019-07-03` witness-search state

No conversational reconstruction was used as technical source of truth.

## Locked upstream state preserved

- B02–B09 historical qualification remains locked.
- B09 final remains historical PASS.
- 3.1.1 Momentum V1 definition remains PASS.
- 3.1.2 baseline protocol remains PASS.
- Actual 3.1.2 execution remains BLOCKED until a verified >=5-year native-tick corpus and realistic execution-cost environment exist.
- No partial/synthetic/fabricated backtest is authorized.

## Calendar state entering this governance block

Twelve 2019 candidate dates were resolved. The only unresolved 2019 candidate remained:

- `2019-07-03` — `INDEPENDENCE_PRE_HOLIDAY_SESSION`

Prior dedicated search verdict:

**BLOCKED** — `DATE_SPECIFIC_DUKASCOPY_USATECH_2019_07_03_WITNESS_NOT_FOUND`

Durable search report:

`reports/data-qualification/dukascopy_usatech_2019_07_03_witness_search.md`

Latest observed calendar execution entering this block remained:

- 28 historical/current calendar tests PASS;
- 6 late-2019 targeted tests PASS;
- combined observed: `34 passed`;
- coverage: 111 candidates / 24 resolved / 87 unresolved / BLOCKED.

No calendar code changed during the governance block described below.

## IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP — formalisation

A durable governance rule was created:

`04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`

Commit:

`1085a0c5ee71a5c327eb802fe001c9b198dd683a`

Contract:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

The rule prevents evidence-by-plausibility. It exposes exactly three PASS routes:

1. `PASS-A` — exact primary broker witness for exact date + instrument + precise timing;
2. `PASS-B` — exact archived broker witness with verified provenance;
3. `PASS-C` — exact-date broker event witness explicitly covering the target instrument + explicit official broker special-session mapping contract + exact same-date verified exchange/reference timing.

Everything weaker remains BLOCKED unless a proven contradiction/malformed witness creates FAIL.

Corroborative-only evidence cannot be accumulated into PASS. This includes:

- broker schedules from other years;
- holiday-name analogy;
- current regular hours;
- exchange-only timing;
- third-party paraphrases without exact broker provenance;
- missing BI5/ticks;
- HTTP failures;
- empty widgets;
- search non-results;
- majority-of-years reasoning.

## Executable governance gate

Executable gate created:

`tools/irreducible_historical_broker_evidence_gap.py`

Commit:

`c749622ac19e055cefc5e464cb8b7de1523976e5`

The executable model deliberately has no PASS-bearing fields for cross-year examples, HTTP failures, missing BI5 data, or generic holiday context. Those facts therefore cannot be accidentally summed into a PASS.

## Adversarial tests

Adversarial tests created:

`tests/test_irreducible_historical_broker_evidence_gap.py`

Commit:

`851612685826bdd4a116306d65173348d667c425`

The attacks cover:

- exact broker primary PASS;
- exact archive requiring verified provenance;
- complete PASS-C;
- removal of every PASS-C component one by one;
- exchange-only evidence;
- broker event + exchange without explicit mapping;
- mapping + exchange without same-date broker event;
- generic broker notice without target instrument;
- cross-year broker patterns;
- missing-data/HTTP-style evidence;
- incomplete retrieval;
- strong broker contradiction;
- wrong date/instrument identity;
- falsified archive provenance;
- bucket conversion contradicting proven timing.

### First execution attempt

The first local run failed during pytest collection because the temporary materialisation did not expose the repository root on `PYTHONPATH`:

`ModuleNotFoundError: No module named 'tools.irreducible_historical_broker_evidence_gap'`

This was an execution-environment failure, not a governance verdict. No versioned logic was changed.

### Corrected execution

The same versioned gate/tests were rerun with only the local import environment corrected:

```text
..............                                                           [100%]
14 passed in 0.03s
```

## Adversarial break and correction

A weaker candidate route was explicitly rejected:

`same-date broker event context + exact exchange timing -> PASS`

It was broken because a broker can acknowledge a holiday/event while applying broker-specific timing that differs from the exchange.

Correction: PASS-C now requires an explicit official broker contract mapping **special/holiday sessions** for the target instrument to the named exchange/reference schedule. Similar regular hours or historical coincidence cannot substitute for that contract.

Re-break of the corrected rule: PASS (`14 passed`).

Qualification report:

`reports/data-qualification/irreducible_historical_broker_evidence_gap_qualification.md`

Commit:

`1caa9227f4a8525320085e70e39098c38c3e5376`

### Governance-rule verdict

**PASS**

Reason:

`ALL_ADVERSARIAL_FALSE_PASS_AND_FAIL_PATHS_REJECTED_AS_SPECIFIED`

This PASS applies to the governance rule only. It does not resolve a historical date.

## Application to 2019-07-03

After the governance rule itself was qualified PASS, V1 was applied to `2019-07-03`.

Evidence classification:

- B0 exact primary broker witness: absent;
- B1 exact archived broker witness: absent;
- B2 exact-date broker event witness explicitly covering USATECH: absent;
- B3 explicit broker special-session mapping contract: absent;
- exact same-date 2019 exchange timing: present;
- exchange provenance: treated as verified for the strongest favorable application;
- retrieval exhausted: yes;
- strong exact-broker contradiction: no.

Observed executable gate decision:

```text
GapDecision(
    verdict='BLOCKED',
    reason='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP',
    route=None,
    contract='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1'
)
```

Application report:

`reports/data-qualification/dukascopy_usatech_2019_07_03_gap_application.md`

Commit:

`2566eccf1a8ca1439f6d7296a741f24b4419fc76`

### 2019-07-03 verdict

**BLOCKED**

Reason:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`

No calendar record was added. No calendar test expectation changed. No coverage PASS was claimed.

## Important distinction now locked

Two simultaneous statements are true:

1. the **governance rule is PASS** — the method for handling irreducible historical broker gaps survived adversarial qualification;
2. `2019-07-03` is still **BLOCKED** — the available evidence does not complete PASS-A, PASS-B, or PASS-C.

Do not collapse these two verdicts.

## Latest executable calendar/coverage evidence

Because no calendar/test classification changed during this governance block, the calendar tests and coverage were not rerun merely to fabricate a newer timestamp.

The latest observed calendar state remains:

- 34 calendar tests PASS from the prior run;
- 111 candidate dates;
- 24 resolved candidate dates;
- 87 unresolved candidate dates;
- first unresolved date `2019-07-03`;
- coverage verdict BLOCKED.

## Evidence discipline preserved

- Verdicts only PASS / FAIL / BLOCKED.
- Missing evidence never becomes PASS.
- Other-year schedules remain corroborative only.
- Exchange-only timing does not become broker truth.
- Missing BI5/HTTP failures remain non-evidence for closure.
- Partial hours remain open at hourly-bucket granularity.
- The historical Trading Breaks widget route remains CLOSED unless materially new evidence appears.
- Do not repeat the generic `2019-07-03` witness search unless materially new evidence appears.

## Exactly one next governed action

**Formalize and qualify the boundary between global coverage-envelope completeness and admissibility of a future frozen >=5-year execution window when an irreducible historical broker-evidence gap exists outside that future window. The rule must determine whether qualification may continue into 2020+ while `2019-07-03` remains explicitly BLOCKED, without treating that date as resolved and without authorizing `.bi5` acquisition. Do not begin massive acquisition until this boundary itself is qualified.**
