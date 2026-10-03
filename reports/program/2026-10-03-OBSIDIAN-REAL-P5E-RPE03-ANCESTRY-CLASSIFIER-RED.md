# RPE-03 — NB5 ANCESTRY CLASSIFIER V0.1 — RED EVIDENCE

Date: 2026-10-03

## Preregistered predecessor

Preregistration HEAD:
8aa4ee2128a404fd57e64affc4f3b04751e86d87

Preregistration blob:
4eca84a17f7d0c53a794f34af65d1d0a81302930

Preregistration schema blob:
621f909fcde85694a0cc7548adffad7e14ae3970

## RED command

python -B -m unittest tests.obsidian_projection.test_rpe03_ancestry_classifier_v0_1

## Observed result

Ran 16 tests.

FAILED (failures=14).

RPE03_RED_EXIT=1.

Two tests passed:
- governed preregistration validates through RPE-01;
- the absent classifier source contains no forbidden network tokens by construction.

The fourteen RED failures arise because
tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py
does not yet exist.

The frozen test surface already covers INITIAL/SAME/FAST_FORWARD/NON_FAST_FORWARD, missing and non-commit objects, shallow/graft/alternate domains, inherited Git environment, replace refs, timeout, requested-object corruption, linked worktrees, commit-graph disabling, environment sanitization and invalid head identities.

No network operation or protected predecessor mutation occurred.

RPE-04 = CLOSED.
RPE-05 = CLOSED.
RPE-06 = CLOSED.
REAL P5-E = CLOSED.
