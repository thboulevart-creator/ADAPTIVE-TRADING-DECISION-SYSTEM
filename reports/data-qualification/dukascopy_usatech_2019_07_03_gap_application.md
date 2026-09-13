# APPLICATION REPORT — IRREDUCIBLE HISTORICAL BROKER EVIDENCE GAP — 2019-07-03

## 1. Governance prerequisite

Applied rule:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

Rule document:

`04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`

Qualification report:

`reports/data-qualification/irreducible_historical_broker_evidence_gap_qualification.md`

The rule received **PASS** under adversarial qualification before this application.

## 2. Target fact

- Broker: Dukascopy
- Instrument: `USATECH.IDX/USD` / project symbol `USATECHIDXUSD`
- Date: `2019-07-03`
- Candidate reason: `INDEPENDENCE_PRE_HOLIDAY_SESSION`
- Fact required: whether Dukascopy applied a special early-close/reopen schedule to USATECH on that exact date, precise enough to classify whole UTC hourly BI5 buckets.

## 3. Durable retrieval evidence

Primary witness-search report:

`reports/data-qualification/dukascopy_usatech_2019_07_03_witness_search.md`

The dedicated search established:

- no exact live/official Dukascopy witness for `2019-07-03` + USATECH + exact special hours was recovered;
- no verified exact archived copy of such a 2019 Dukascopy witness was recovered;
- the recovered Dukascopy 2019 Independence announcement concerns **4 July 2019**, not 3 July;
- exact Dukascopy July-3 examples exist in other years, but the timing is year-specific and those examples are corroborative only;
- exact 2019 exchange-derived evidence supports an ES/NQ/YM early close at 12:15 Chicago time on 3 July 2019;
- no official broker special-session mapping contract was recovered proving that Dukascopy USATECH must inherit that exact exchange holiday schedule;
- retrieval was materially exhausted under the governed search process.

## 4. Evidence classification under V1

- B0 exact primary broker witness: **ABSENT**
- B1 exact archived broker witness with verified provenance: **ABSENT**
- B2 exact-date broker event witness explicitly covering target instrument: **ABSENT**
- B3 explicit official broker special-session mapping contract: **ABSENT**
- X0/X1 exact same-date exchange/reference timing: **PRESENT**
- exchange/archive provenance accepted for this application: **PRESENT**
- retrieval exhausted: **YES**
- strong exact-broker contradiction: **NO**
- witness date/instrument identity mismatch claimed as target evidence: **NO**
- falsified archive provenance: **NO**
- bucket conversion contradiction: **NO**

The application deliberately grants the strongest favorable treatment to the 2019 exchange evidence (`exact_exchange_schedule=True`, `exchange_provenance_verified=True`). The result still cannot PASS because the required broker-side link is absent.

## 5. Executable gate application

Input state equivalent to:

```python
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

## 6. Why other-year Dukascopy witnesses do not change the result

The 2018, 2017, 2015 and 2026 July-3 broker witnesses are explicitly corroborative-only under V1.

They can show that Dukascopy sometimes applies July-3 special treatment, but they cannot establish the 2019 broker fact. They therefore have no PASS-bearing field in the executable gate.

This is intentional: historical examples with different timings demonstrate why cross-year interpolation is unsafe.

## 7. Application verdict

**BLOCKED**

Reason:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`

No PASS route is complete:

- PASS-A unavailable: B0 absent;
- PASS-B unavailable: B1 absent;
- PASS-C unavailable: B2 and B3 absent even though exact exchange timing exists.

No FAIL condition is proven because the evidence is incomplete rather than internally contradictory.

## 8. Repository effect

- no `SPECIAL_SESSION_EVIDENCE` record is created for `2019-07-03`;
- no calendar test expectation is changed;
- no coverage PASS is claimed;
- the last observed calendar execution remains 34 tests PASS from the prior executable state;
- the last observed coverage remains 24 resolved / 87 unresolved / BLOCKED;
- massive `.bi5` acquisition remains forbidden under the current coverage gate.

The governance rule is PASS. The historical date is still BLOCKED. These verdicts are intentionally distinct.
