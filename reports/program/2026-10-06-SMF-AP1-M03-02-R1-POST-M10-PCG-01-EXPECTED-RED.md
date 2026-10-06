# SMF-AP1-M03-02-R1-POST-M10-PCG-01 — EXPECTED RED V0.1

Status: EXPECTED_RED_CONFIRMED_BEFORE_RUNTIME_IMPLEMENTATION

## Frozen synthetic surface

FIXTURE PATH =
tests/fixtures/smf_ap1_m03_02_r1_post_m10_pcg_01_synthetic_cases_v0_1.json

FIXTURE SHA256 =
12f8ec564b86a8db91df48b497a409871dbb719b31b8f96f949325ef31462b4c

FIXTURE CASE COUNT =
32

FROZEN BREAKER COUNT =
46

## Test-first execution

Command:

python -B -m pytest -q tests/test_smf_ap1_m03_02_r1_post_m10_pcg_01.py

Observed:

13 FAILED
3 PASSED

Primary expected failure:

MISSING_IMPLEMENTATION:smf_ap1_m03_02_r1_post_m10_pcg_01.py

The independent reference implementation was also absent.

## Classification

EXPECTED_RED =
PASS

RUNTIME_PRESENT_DURING_FREEZE =
FALSE

REFERENCE_PRESENT_DURING_FREEZE =
FALSE

REAL_DATA_READ =
FALSE

REAL_PCG_APPLICATION =
FALSE

NEW_MARKET_RESULT =
FALSE

The RED state is a test-first qualification event, not a scientific or governance failure.
