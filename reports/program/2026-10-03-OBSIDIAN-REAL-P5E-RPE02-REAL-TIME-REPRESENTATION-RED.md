# RPE-02 — N5 + REAL-TIME REPRESENTATION V0.1 — RED EVIDENCE

Date: 2026-10-03

## Preregistered predecessor

Preregistration HEAD:
c42a0f3df48807b3681db782f0a6fd58bd5c7aea

Preregistration blob:
614d3724c5c36bbdb6afbf9b49a31f88da465719

Preregistration schema blob:
923671b1539585b5c32c8e2d284598b521fc0bba

## RED command

python -B -m unittest tests.obsidian_projection.test_rpe02_real_time_representation_v0_1

## Observed result

Ran 17 tests.

FAILED (failures=15).

RPE02_RED_EXIT=1.

Two tests passed:
- governed preregistration validates through RPE-01;
- the absent implementation source contains no environment/CLI authority by construction.

The fifteen RED failures all arise because the preregistered module
tools/obsidian_projection/rpe02_real_time_model_v0_1.py
does not yet exist.

The frozen test surface already covers integer-nanosecond representation, exact 60-second and +1 ns boundaries, actual-start semantics, next-slot completion equality, overlap equality, pre-release target handling, remote-completion versus full-completion separation, release ceiling, synthetic parity and host monotonic-clock evidence.

No network or protected predecessor mutation occurred.

RPE-04 = CLOSED.
RPE-05 = CLOSED.
RPE-06 = CLOSED.
REAL P5-E = CLOSED.
