# B-PE-SEM-05R-01 — FINAL PERSISTED-HEAD RE-BREAK

Persisted HEAD attacked: 6c8af197013e97bfcaf1e88a8d24ba66ea54d5c1
Persisted tree attacked: d9c5cd882711055999d4d9f22eca9d4c6ba4a107

## Candidate / breaker

~~~text
candidate commit = b98a011e21f539c10d3064b30513efc9817bedf4
candidate ancestor = PASS
breaker verdict = PASS
breaker attacks = 30
breaker defects = 0
post-candidate changed paths = 3
unresolved changed paths = 0
~~~

## Recovery result

~~~text
package integrity = PASS
Recovery A = AMBIGUOUS
Recovery B = NOT_FOUND
Recovery C = INCOMPLETE_VERSION_COVERAGE
any full recovery = NO
Lane S re-adjudication sufficient new authority = NO
Lane P authorized = NO
B-PE-SEM-05R-01 = BLOCKED
demonstrated final defects = 0
NONE
qualification seal = 7ecc77a75c4bcf333edce03ec2a6504a8f0ded39fc49789d0556d7bd54f3866a
~~~

BLOCKED is substantive: provider-versioned artifacts recovered exact BI5 cache identity and partial client/history stability, but did not recover the complete provider-primary A/B/C authority required by the qualified semantic contract.

No provider BI5 market-data object was requested or observed. No Lane P RequestManifest/P-DIAG, FULL_INTERVAL, D or backtest was authorized or executed.

STOP.
