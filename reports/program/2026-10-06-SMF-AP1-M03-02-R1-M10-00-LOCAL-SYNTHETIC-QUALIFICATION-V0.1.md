# SMF-AP1-M03-02-R1-M10-00 — LOCAL SYNTHETIC QUALIFICATION V0.1

Status: LOCAL_GREEN_PRE_CANONICAL_CI

## Test-first evidence

Expected RED was observed before implementation:

- command: `python -B -m pytest -q -x tests/test_smf_ap1_m03_02_r1_m10_00.py`
- result: FAIL
- exact blocking reason: `MISSING_IMPLEMENTATION:smf_ap1_m03_02_r1_m10_00.py`

No real M10 result was produced during RED.

## Minimal implementation

The generic SMF-03 M10 runtime was not modified.

A claim-scoped AP1/M01 companion was added with a separate independent reference implementation.

The procedure is fixed to:

- 11 metric/probability claim units;
- 3 adjacent complete-year transitions per claim unit;
- 33 primary contrasts;
- symmetric relative change;
- materiality threshold R >= 0.20;
- zero denominator => BLOCKED;
- BLOCKED precedence;
- no global cross-metric verdict.

## Local GREEN

Observed local qualification:

```text
M10-00 targeted = 20/20 PASS
M01 CR1 regression = 7/7 PASS
M01 regression = 5/5 PASS
SI-01 regression = 4/4 PASS
EF-01 regression = 4/4 PASS
git diff --check = PASS
```

The 20 pytest cases collectively cover the frozen B1-B25 breaker semantics.

## Real-result boundary

During M10-00 qualification:

```text
REAL M10 EXECUTION = FALSE
REAL M10 R CALCULATION = FALSE
REAL M10 CLAIM-UNIT CLASSIFICATION = FALSE
M10 RESULT EXPOSED = FALSE
NEW M03 = FALSE
RAW AP0 READ = FALSE
```

Only the exact M03 SHA-256 identity requirement is bound.

Canonical CI and persisted-head rebreak remain required before real-execution readiness can be declared.
