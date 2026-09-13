# QUALIFICATION REPORT — IRREDUCIBLE HISTORICAL BROKER EVIDENCE GAP V1

## 1. Target

Governance contract:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

Reference rule:

`04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`

Executable gate:

`tools/irreducible_historical_broker_evidence_gap.py`

Adversarial tests:

`tests/test_irreducible_historical_broker_evidence_gap.py`

The rule was qualified **before** application to `2019-07-03`.

## 2. Formalisation

The problem is not whether exchange timing is known. The problem is whether a missing historical broker-specific witness may be replaced without creating a false broker calendar.

The formal rule therefore forbids evidence accumulation by plausibility and exposes only three PASS routes:

- `PASS-A`: exact primary broker witness;
- `PASS-B`: exact archived broker witness with verified provenance;
- `PASS-C`: exact-date broker event witness for the target instrument + explicit official broker special-session mapping contract + exact same-date exchange/reference schedule with verified provenance.

Any weaker combination is BLOCKED. Proven contradictions or falsified identities/provenance are FAIL.

## 3. Candidate weakness identified before lock

A weaker candidate proxy route was considered:

`same-date broker event context + exact exchange timing -> PASS`

This candidate was **broken** adversarially.

Counterexample:

- a broker can announce that an instrument is affected by a holiday while applying broker-specific close/reopen times that differ from the underlying exchange;
- therefore exact exchange timing cannot safely fill missing broker timing merely because the broker acknowledges the event;
- observed similarity of regular hours is also insufficient because it does not prove holiday/special-session inheritance.

If this weak route had been accepted, it could have converted exchange truth into false broker truth.

### Correction

The candidate was tightened by making an explicit official **B3 special-session mapping contract** mandatory for the proxy route.

Corrected PASS-C requires every component:

1. exact target date broker event evidence;
2. exact target instrument explicitly in scope;
3. official broker documentation explicitly mapping special/holiday timing to the named reference schedule;
4. exact same-date reference timing;
5. verified exchange/archive provenance;
6. reproducible time-zone/bucket conversion;
7. no unresolved strong contradiction.

No component may be replaced by cross-year pattern, regular-hour resemblance, missing BI5 data, HTTP failure, or source-count majority.

## 4. Executable adversarial attacks

The corrected rule was attacked with the following cases:

1. exact primary broker witness -> must PASS-A;
2. exact archived broker witness without provenance -> must BLOCK;
3. same archive with verified provenance -> must PASS-B;
4. complete PASS-C chain -> must PASS;
5. remove each PASS-C component individually -> each must BLOCK;
6. exact exchange schedule alone -> must BLOCK;
7. same-date broker event + exact exchange schedule but no mapping contract -> must BLOCK;
8. mapping contract + exchange schedule but no same-date broker event -> must BLOCK;
9. generic broker event without explicit target instrument -> must BLOCK;
10. cross-year broker pattern + exact target-year exchange timing -> must BLOCK;
11. missing-data/HTTP-style evidence -> cannot be encoded as PASS-bearing evidence and must BLOCK;
12. retrieval not exhausted -> BLOCK with `RETRIEVAL_INCOMPLETE`;
13. exact broker contradiction overrides an apparent PASS -> FAIL;
14. wrong date/instrument identity -> FAIL;
15. falsified archive provenance -> FAIL;
16. bucket conversion contradicting proven timing -> FAIL.

The `test_pass_c_requires_every_component` case iterates over five distinct component-removal attacks inside one pytest test, so the semantic attack count is greater than the pytest function count.

## 5. First execution attempt

The first local execution did not reach the tests because the temporary materialisation lacked the repository root on `PYTHONPATH`:

`ModuleNotFoundError: No module named 'tools.irreducible_historical_broker_evidence_gap'`

This was an execution-environment collection failure, not a verdict on the governance rule.

No versioned rule/test code was changed in response.

## 6. Re-execution

The exact same versioned logic/tests were rerun with only the local import environment corrected:

```text
..............                                                           [100%]
14 passed in 0.03s
```

Observed verdict of the adversarial qualification suite:

**PASS**

Reason:

`ALL_ADVERSARIAL_FALSE_PASS_AND_FAIL_PATHS_REJECTED_AS_SPECIFIED`

## 7. Adversarial conclusion

The corrected rule survives the tested bypasses because:

- other-year broker schedules have no PASS-bearing field;
- exchange-only evidence has no route to PASS;
- generic broker context cannot stand in for the target instrument;
- regular-session similarity cannot stand in for a special-session mapping contract;
- unverified archives cannot pass;
- contradictions are evaluated before PASS routes;
- missing evidence remains BLOCKED rather than being converted to truth.

## 8. Qualification verdict

**PASS**

The governance rule itself is qualified for first application.

This PASS certifies the rule/gate behavior. It does **not** certify any particular historical date.

The next permitted action after this qualification is application of V1 to `2019-07-03` using the already-versioned witness-search evidence state.
