# E1-TD-03C-JF02-D3-F2 — CONNECTION-ONLY STATE-OBSERVABILITY CONTROL V0.1

## Result

```
F2_RESULT = CONNECTED_WITHIN_ORIGINAL_BOUND
```

The single authorized F2 connection completed without an explicit `connect(...)` exception.

Observed sequence:

```
CONNECT_CALL_START_UTC  = 2026-10-10T14:55:14.528Z
CONNECT_CALL_RETURN_UTC = 2026-10-10T14:55:19.479Z
CONNECT_CALL_DURATION   = 4950 ms

isConnected @ 0 ms    = false
onConnect             = 2026-10-10T14:55:20.360Z
isConnected @ 1001 ms = true
```

Thus full JForex connection readiness was observed approximately 1.001 seconds after `connect(...)` returned and well inside the original 30-second D3 bound.

## Scientific interpretation

Per the preregistered CASE C:

```
F1_C09_30_SECOND_DEADLINE_TOO_SHORT = WEAKENED
D3_FAILURE_TRANSIENCE = SUPPORTED
D3_ROOT_CAUSE = NOT_AUTOMATICALLY_PROVEN
```

F2 materially weakens the hypothesis that a 30-second window is intrinsically insufficient for this runtime/provider path.

F2 also demonstrates that the same SDK/API/DEMO stack can complete connection/session initialization successfully using a fresh isolated cache.

However, D3 and F2 were executed at different wall-clock times. Provider state, network state and session state were not held constant. Therefore F2 does not prove the unique cause of the earlier D3 failure.

## Effect on prior candidates

Recommended prospective interpretation, pending human adjudication:

- F1-C09 `COLLECTOR_30_SECOND_CONNECTION_DEADLINE_TOO_SHORT`: **WEAKENED**.
- F1-C05 `JFOREX_SDK_BOOTSTRAP_OR_SESSION_INITIALIZATION_FAILURE`: persistent/static-failure interpretation **WEAKENED**; a transient initialization failure during D3 remains plausible.
- F1-C11 `COLLECTOR_IMPLEMENTATION_DEFECT_IN_CONNECTION_PHASE`: **REMAINS SUPPORTED AS AN OBSERVABILITY DEFECT**, because D3 still collapsed transport/session states into one terminal marker.
- Explicit credential rejection: **not observed in F2**.
- Explicit SDK version rejection: **not observed in F2**.
- D3 transient provider/network/session event: **SUPPORTED AS A CLASS OF EXPLANATION, NOT UNIQUELY IDENTIFIED**.

## Market-data firewall

No strategy was started. No history API was called. No `getTicks` occurred. No unexpected `.bi5` market-data object was created in the F2 cache.

Protected baseline and D3 cache identities remained unchanged.

## Termination note

After the probe emitted `F2_DONE=true`, the authorized `client.disconnect()` did not produce an `onDisconnect` callback within the 10-second observation window, and the Maven/JVM process remained alive.

The residual Java process was terminated locally after all provider-facing F2 actions had ended, solely to enforce the STOP rule and allow the parent launcher to finalize evidence. This produced no second login, connect, retry or market-data request.

This termination behavior is non-blocking for the F2 CASE C result but is a separate observability/lifecycle note.

## Boundary

F2 does **not** prove:
- the unique D3 root cause;
- a Dukascopy outage;
- a JForex global defect;
- cache causality;
- history-path qualification;
- Source-B equivalence;
- strategy/performance qualification.

No further provider action is authorized under F2.
