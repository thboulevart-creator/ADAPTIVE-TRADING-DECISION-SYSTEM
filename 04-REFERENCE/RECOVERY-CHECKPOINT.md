# RECOVERY CHECKPOINT — 13 SEPTEMBRE 2026 — MULTI-YEAR DUKASCOPY CALENDAR COVERAGE

## 1. CURRENT STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Prior checkpoint:** `b8b29ab936dc32058f2d589c46ff33fa46329799`
- **Coverage envelope:** `2018-05-01` → `2026-08-14`
- **Execution/backtest window frozen:** no
- **Massive native `.bi5` acquisition:** forbidden under current gate

New governance artifacts:

- rule: `04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`
  - commit `1085a0c5ee71a5c327eb802fe001c9b198dd683a`
- executable gate: `tools/irreducible_historical_broker_evidence_gap.py`
  - commit `c749622ac19e055cefc5e464cb8b7de1523976e5`
- adversarial tests: `tests/test_irreducible_historical_broker_evidence_gap.py`
  - commit `851612685826bdd4a116306d65173348d667c425`
- qualification report: `reports/data-qualification/irreducible_historical_broker_evidence_gap_qualification.md`
  - commit `1caa9227f4a8525320085e70e39098c38c3e5376`
- `2019-07-03` application report: `reports/data-qualification/dukascopy_usatech_2019_07_03_gap_application.md`
  - commit `2566eccf1a8ca1439f6d7296a741f24b4419fc76`
- durable session backup updated after governance qualification.

## 2. RECOVERY ORDER

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/README.md`
4. `99-BACKUP/SESSION-2026-09-13-MULTI-YEAR-DUKASCOPY-CALENDAR.md`
5. `04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`
6. `reports/data-qualification/irreducible_historical_broker_evidence_gap_qualification.md`
7. `reports/data-qualification/dukascopy_usatech_2019_07_03_witness_search.md`
8. `reports/data-qualification/dukascopy_usatech_2019_07_03_gap_application.md`
9. `tools/dukascopy_usatech_calendar.py`
10. `tools/dukascopy_usatech_calendar_coverage.py`
11. calendar tests and governance tests
12. actual GitHub/worktree state and current execution evidence

## 3. LOCKED UPSTREAM STATE — DO NOT REOPEN

- B02–B09 historical qualification remains locked.
- B09 final remains historical PASS.
- 3.1.1 Momentum V1 definition remains PASS.
- 3.1.2 baseline protocol remains PASS.
- 3.1.2 actual execution remains BLOCKED until a verified >=5-year native-tick corpus and realistic execution environment exist.
- No partial/synthetic/fabricated backtest is authorized.

## 4. CALENDAR STATE

The calendar still contains **24** date-specific special-session evidence records inside the coverage envelope.

Latest observed calendar execution remains:

- `28` historical/current calendar tests PASS;
- `6` late-2019 targeted tests PASS;
- combined observed calendar execution: `34 passed`.

Latest observed coverage remains:

- `candidate_dates`: **111**
- `resolved_candidate_dates`: **24**
- `special_session_evidence_dates`: **24**
- `no_special_change_evidence_dates`: **0**
- `unresolved_candidate_dates`: **87**
- `contradictory_evidence_dates`: `[]`
- `evidence_shape_errors`: `[]`
- `orphan_special_evidence`: `[]`
- `verdict`: **BLOCKED**
- `reason`: `SPECIAL_SESSION_EVIDENCE_COVERAGE_INCOMPLETE`

No calendar/test code changed during the governance block, so the calendar suite/coverage were not rerun merely to create a newer timestamp.

## 5. IRREDUCIBLE HISTORICAL BROKER EVIDENCE GAP RULE

Contract:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

Exactly three PASS routes are allowed:

- `PASS-A`: exact primary broker witness for exact target date/instrument/timing;
- `PASS-B`: exact archived broker witness with verified provenance;
- `PASS-C`: exact-date broker event witness explicitly covering the target instrument + explicit official broker special-session mapping contract + exact same-date verified exchange/reference timing.

Corroborative evidence cannot be accumulated into PASS. This includes other-year broker schedules, exchange-only timing, current regular hours, missing BI5/ticks, HTTP failures, empty widgets, search non-results, or source-count majority.

Missing evidence is BLOCKED. Proven contradictions/malformed identities are FAIL.

## 6. ADVERSARIAL QUALIFICATION OF THE RULE

A weaker candidate route:

`same-date broker event + exact exchange timing -> PASS`

was broken because the broker may apply broker-specific special hours different from the exchange.

Correction: PASS-C requires an explicit official broker special-session mapping contract.

Adversarial execution initially hit a local import/collection failure (`ModuleNotFoundError`) due missing temporary `PYTHONPATH`. No rule code changed.

Re-execution with only the local import environment corrected:

```text
..............                                                           [100%]
14 passed in 0.03s
```

### Governance-rule verdict

**PASS**

Reason:

`ALL_ADVERSARIAL_FALSE_PASS_AND_FAIL_PATHS_REJECTED_AS_SPECIFIED`

This PASS certifies the rule only.

## 7. APPLICATION TO 2019-07-03

Target:

`2019-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

Evidence classification under V1:

- B0 exact primary broker witness: absent;
- B1 exact archived broker witness: absent;
- B2 exact-date broker event witness explicitly covering USATECH: absent;
- B3 explicit broker special-session mapping contract: absent;
- exact same-date 2019 exchange timing: present;
- exchange provenance: treated as verified for strongest favorable application;
- retrieval exhausted: yes.

Observed executable decision:

```text
GapDecision(
    verdict='BLOCKED',
    reason='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP',
    route=None,
    contract='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1'
)
```

### Date verdict

**BLOCKED**

Reason:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`

No calendar record was created. No test expectation changed. No coverage PASS was claimed.

## 8. LOCKED DISTINCTION

Do not conflate:

- **Governance rule: PASS**
- **2019-07-03 historical date: BLOCKED**

The rule successfully determines that the current evidence is insufficient. Qualification of the method is not qualification of the date.

## 9. EVIDENCE DISCIPLINE

- Verdicts only PASS / FAIL / BLOCKED.
- Missing evidence never becomes PASS.
- Other-year schedules remain corroborative only.
- Exchange-only timing never silently becomes broker truth.
- Regular-hour similarity is not a special-session mapping contract.
- Missing BI5/ticks and HTTP failures are not closure evidence.
- Partial tradable hours remain EXPECTED_OPEN at hourly granularity.
- Do not repeat generic `2019-07-03` searches without materially new evidence.
- Historical Trading Breaks widget route remains CLOSED unless materially new evidence appears.

## 10. MASSIVE ACQUISITION GATE

Massive `.bi5` acquisition remains forbidden.

The current global coverage contract is still BLOCKED because unresolved candidate dates remain, including the irreducible `2019-07-03` gap.

No OHLC M1, interpolation, synthetic ticks, or substituted ticks are authorized.

## 11. EXACTLY ONE NEXT GOVERNED ACTION

**Formalize and adversarially qualify the boundary between global coverage-envelope completeness and admissibility of a future frozen >=5-year execution window when an `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` exists outside that future window. Determine whether qualification may continue into 2020+ while `2019-07-03` remains explicitly BLOCKED, without marking that date resolved and without authorizing `.bi5` acquisition. Do not begin massive acquisition until this boundary itself receives a verdict.**
