# B-ERD-02 — BOUNDED EMPIRICAL REPRESENTATION-DISCRIMINATION EXECUTION

**Date:** 2026-09-20
**Starting execution-input HEAD:** ab219e54daa05b88cc7ef69e2f68fb43bec82750

## Pre-request state

Qualified B-ERD-01 contract: PASS.

Pre-request sealed inputs:

- LocatorManifest: a9fc7115af925fcb5e848e76fb98da7c51053ad136dfb2f6adbd239c004b4db7
- ProbePlan: af5b70ffef6125a0ab6b146c3bb917089182a5abb3adc260a9092e8d584b44ce
- TransportPolicy: 136b5a0fecd6387bf5054cd13dc8cb090e7d5e991bd9971d040b0f9c07099b44

Nine required probe windows and two registered candidate families produced exactly 18 predeclared locator attempts.

## Transport observation

Every attempted binary .bi5 locator was rejected by the available web transport before usable HTTP response evidence was exposed.

Observed for all 18 attempts:

~~~text
http_status = unavailable
response headers = unavailable
response body bytes = unavailable
provider request reached = UNKNOWN
transport disposition = TRANSPORT_AMBIGUOUS
family disposition = FAMILY_TRANSPORT_BLOCKED
retry = none
~~~

No HTTP 404/403/200 claim is made because none was exposed.

No locator is classified as absent.

## Diagnostics

~~~text
raw BI5 bytes available = NO
diagnostic path A = NOT_REACHED
diagnostic path B = NOT_REACHED
cross-family semantic comparison = COMPARISON_BLOCKED
~~~

The contract forbids deriving support/refutation from transport ambiguity.

## Per-probe state

PW/P0/P1/P2/P3/P4/P5/P6/P7:

~~~text
K1 = BLOCKED
K2 = BLOCKED
probe = BLOCKED
~~~

No UNKNOWN_REPRESENTATION_EVIDENCED event occurred because no positive unregistered-family evidence was observed.

## Verdict

~~~text
B-ERD-02 BOUNDED EXECUTION = BLOCKED

overall_probe_verdict = BLOCKED

PROBE_SUPPORTED = NO
PROBE_REFUTED = NO
~~~

Reason:

~~~text
ALL_REQUIRED_PROBES_TRANSPORT_BLOCKED
NO_RAW_BYTES
T_HOURLY_UNDECIDABLE
~~~

This is an environment/tool transport limitation, not evidence against Dukascopy K1/K2 availability.

No full acquisition, D materialization, backtest or trading execution occurred.
