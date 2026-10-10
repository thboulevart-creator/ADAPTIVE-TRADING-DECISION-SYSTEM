# HUMAN ADJUDICATION PACKAGE —
# E1-TD-03C-JF02-D3-F1
# CONNECTION-FAILURE READ-ONLY FORENSIC V0.1

RECOMMENDED_HUMAN_DECISION =
ADOPT_D3_F1_FINDINGS_WITH_CONNECTION_ROOT_CAUSE_SUPPORTED_BUT_NOT_PROVEN

## Recommended findings

```
D3_F1 =
QUALIFIED_READ_ONLY_FORENSIC

PROVIDER_EXPLICIT_CONNECTION_REJECTION =
NOT_PROVEN

EXPLICIT_CREDENTIAL_AUTHENTICATION_REJECTION =
REJECTED_FOR_THIS_ATTEMPT

CLIENT_FULLY_READY_WITHIN_30_SECONDS =
FALSE

CONNECTION_FAILURE_ROOT_CAUSE =
SUPPORTED_BUT_NOT_PROVEN

MOST_SUPPORTED_STAGE =
JFOREX_TRANSPORT_OR_SESSION_INITIALIZATION_NOT_COMPLETE_WITHIN_BOUND

F1_C05 =
SUPPORTED

F1_C11 =
SUPPORTED

F1_C09 =
PLAUSIBLE
```

## Human-adoption boundary

Do not adopt any claim that:
- credentials were invalid;
- Dukascopy was down;
- DNS/TCP/TLS failed;
- the isolated cache caused the connection failure;
- the SDK is globally defective;
- 30 seconds is definitively too short.

Those remain unproven.

## Recommended next frontier

`E1-TD-03C-JF02-D3-F2 — CONNECTION-ONLY STATE-OBSERVABILITY CONTROL V0.1`

Purpose: isolate the connection phase before any further history experiment.

Recommended constraints:
- one DEMO login;
- one connect attempt;
- zero reconnect/retry;
- no strategy start;
- no getTicks/history request;
- no market-data acquisition;
- exact exception-class capture;
- onConnect/onDisconnect timestamps;
- bounded isConnected observation up to a preregistered longer limit;
- separate fresh isolated cache;
- separate human authorization required.

## STOP

No repair selected.
No real test executed during D3-F1.
No login/connect/getTicks occurred during D3-F1.
No cache/configuration mutation occurred.
D3-F2 remains unauthorized.
