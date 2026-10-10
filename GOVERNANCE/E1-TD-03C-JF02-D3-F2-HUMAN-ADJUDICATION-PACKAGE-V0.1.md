# HUMAN ADJUDICATION PACKAGE —
# E1-TD-03C-JF02-D3-F2
# CONNECTION-ONLY STATE-OBSERVABILITY CONTROL V0.1

RECOMMENDED_HUMAN_DECISION =
ADOPT_D3_F2_CONNECTED_WITHIN_ORIGINAL_BOUND_WITH_D3_ROOT_CAUSE_STILL_NOT_PROVEN

## 1. F2 observed result

```
F2_REAL_EXECUTION = COMPLETED
CONNECT_EXCEPTION_THROWN = FALSE
CONNECT_CALL_DURATION_MS = 4950
ONCONNECT_OBSERVED = TRUE
FIRST_CONNECTED_ELAPSED_MS = 1001
F2_RESULT = CONNECTED_WITHIN_ORIGINAL_BOUND
```

## 2. Authorized CASE classification

```
CASE = C
F1_C09_30_SECOND_DEADLINE_TOO_SHORT = WEAKENED
D3_FAILURE_TRANSIENCE = SUPPORTED
D3_ROOT_CAUSE = NOT_AUTOMATICALLY_PROVEN
```

## 3. Recommended causal adjudication

Adopt:

```
D3_CONNECTION_FAILURE = TRANSIENT_OR_STATE_DEPENDENT_EVENT_SUPPORTED
UNIQUE_D3_CONNECTION_FAILURE_ROOT_CAUSE = NOT_PROVEN

F1_C09 = WEAKENED

F1_C05_PERSISTENT_STATIC_INTERPRETATION = WEAKENED
F1_C05_TRANSIENT_D3_INITIALIZATION_STALL = PLAUSIBLE

F1_C11_OBSERVABILITY_DEFECT = REMAINS_SUPPORTED
```

Do not adopt any claim that F2 proves which transient component caused D3.

## 4. Safety / evidence result

```
START_STRATEGY = FALSE
HISTORY_REQUEST = FALSE
GETTICKS = FALSE
UNEXPECTED_MARKET_DATA_FILES = 0

BASELINE_CACHE_UNCHANGED = TRUE
D3_CACHE_UNCHANGED = TRUE
```

## 5. Termination note

`client.disconnect()` was invoked once after successful connection.

No `onDisconnect` callback was observed within the authorized 10-second observation window. The connection-only main program reached `F2_DONE=true`, but SDK/Maven background threads left the JVM alive.

The residual local F2 Java process was then terminated solely as STOP enforcement.

This is proposed as:

```
F2_TERMINATION_LIFECYCLE_NOTE = NON_BLOCKING
```

It does not change CASE C.

## 6. F2 closure

Recommended:

```
F2 = HUMAN_ADOPTED_AND_CLOSED
LOGIN_BUDGET = 1/1 CONSUMED
CONNECT_BUDGET = 1/1 CONSUMED
RECONNECT = 0
RETRY = 0
NO_SECOND_EXECUTION = TRUE
```

## 7. Next frontier

Do **not** automatically return to the D3 historical `getTicks` experiment.

The new evidence removes the connection-phase blocker for this observed F2 attempt, but the next scientific decision must separately determine whether:

1. a single history-only cache-neutral retry now has enough value; or
2. the existing D1/D2/D3/F1/F2 evidence is already sufficient to stop investing in JForex as an AWS substitute.

Recommended next step:

```
E1-TD-03C-JF02-D3-F2-A1 —
POST-F2 JFOREX PATH NECESSITY / VALUE-OF-INFORMATION ADJUDICATION V0.1
```

This should be documentary/read-only first.

No new login, connect, history request or market data is authorized by this package.

## STOP

```
NEXT = HUMAN_ADJUDICATION_OF_D3_F2_RESULT
STOP = TRUE
```
