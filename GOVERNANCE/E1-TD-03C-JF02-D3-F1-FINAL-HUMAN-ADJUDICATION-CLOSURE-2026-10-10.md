# HUMAN ADJUDICATION —
# E1-TD-03C-JF02-D3-F1
# CONNECTION-FAILURE READ-ONLY FORENSIC V0.1

DECISION =
ADOPT_D3_F1_FINDINGS_WITH_CONNECTION_ROOT_CAUSE_SUPPORTED_BUT_NOT_PROVEN

## 1. CANONICAL REPOSITORY IDENTITY

REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

FRESH_OBSERVED_HEAD =
724340048e83a2d588828eb4c096cfffc49616f7

FRESH_OBSERVED_TREE =
e51b0070046bb496bb388b773a3d9869d4d002eb

FORCE =
FALSE

CONCURRENT_DRIFT =
FC01_AND_BEPD_ONLY_NON_MATERIAL_FOR_D3_F1

---

## 2. D3-F1 RESULT

D3_F1 =
QUALIFIED_READ_ONLY_FORENSIC

CONNECTION_FAILURE_ROOT_CAUSE =
SUPPORTED_BUT_NOT_PROVEN

PROVIDER_EXPLICIT_CONNECTION_REJECTION =
NOT_PROVEN

EXPLICIT_CREDENTIAL_AUTHENTICATION_REJECTION =
REJECTED_FOR_THIS_ATTEMPT

CLIENT_FULLY_READY_WITHIN_30_SECONDS =
FALSE

MOST_SUPPORTED_STAGE =
JFOREX_TRANSPORT_OR_SESSION_INITIALIZATION_NOT_COMPLETE_WITHIN_BOUND

---

## 3. HUMAN-ADOPTED CANDIDATE CLASSIFICATION

F1-C01 CREDENTIAL_OR_AUTHENTICATION_REJECTION =
REJECTED

F1-C02 DUKASCOPY_ENDPOINT_OR_BOOTSTRAP_UNREACHABLE =
WEAKLY_SUPPORTED

F1-C03 DNS_TCP_TLS_HTTP_TRANSPORT_FAILURE =
PLAUSIBLE

F1-C04 TRANSIENT_PROVIDER_CONNECTION_FAILURE =
PLAUSIBLE

F1-C05 JFOREX_SDK_BOOTSTRAP_OR_SESSION_INITIALIZATION_FAILURE =
SUPPORTED

F1-C06 JAVA_TLS_OR_RUNTIME_COMPATIBILITY_FAILURE =
WEAKLY_SUPPORTED

F1-C07 JNLP_SDK_VERSION_COMPATIBILITY_FAILURE =
REJECTED

F1-C08 LOCAL_PROXY_FIREWALL_OR_NETWORK_CONFIGURATION_INTERFERENCE =
WEAKLY_SUPPORTED

F1-C09 COLLECTOR_30_SECOND_CONNECTION_DEADLINE_TOO_SHORT =
PLAUSIBLE

F1-C10 D3_ISOLATED_CACHE_INITIALIZATION_INTERFERENCE =
WEAKLY_SUPPORTED

F1-C11 COLLECTOR_IMPLEMENTATION_DEFECT_IN_CONNECTION_PHASE =
SUPPORTED

F1-C12 UNDOCUMENTED_PROVIDER_BEHAVIOR =
PLAUSIBLE

F1-C13 OTHER_ROOT_CAUSE =
UNRESOLVED

---

## 4. CONNECTION-STATE INTERPRETATION

I explicitly adopt that:

JF02_CONNECT_FAILED

means only that the collector did not observe:

client.isConnected() == true

within its fixed 30-second post-connect observation window.

I do NOT adopt that this proves:

- invalid credentials;
- provider rejection;
- Dukascopy outage;
- DNS failure;
- TCP failure;
- TLS failure;
- Java failure;
- SDK defect;
- cache interference.

The static SDK evidence establishes that:

isConnected() == true

requires both:

TRANSPORT_ONLINE = TRUE

AND:

SESSION_INITIALIZED = TRUE

Therefore:

TRANSPORT_ONLINE_AT_TIMEOUT =
UNRESOLVED

SESSION_INITIALIZED_AT_TIMEOUT =
UNRESOLVED

---

## 5. COLLECTOR OBSERVABILITY LIMITATION

The D3 collector used:

- empty onConnect callback;
- empty onDisconnect callback;
- one final isConnected predicate;
- one fixed 30-second deadline.

Therefore:

CONNECTION_PHASE_DIAGNOSTIC_RESOLUTION =
INSUFFICIENT_TO_ISOLATE_ROOT_CAUSE

F1-C11 =
SUPPORTED

This does NOT mean the collector caused the provider-side
failure.

It means the collector did not retain enough state to
distinguish the possible connection-stage causes.

---

## 6. PRIOR STACK COMPATIBILITY EVIDENCE

The same stack:

SDK =
3.6.51

API =
2.13.99

previously achieved:

AUTHENTICATION =
PASS

INSTRUMENT_SUBSCRIPTION =
PASS

during the earlier governed READ_A execution.

Therefore:

PERMANENT_SDK_API_INCOMPATIBILITY =
REJECTED_AS_CURRENT_PRIMARY_EXPLANATION

GLOBAL_JFOREX_DEFECT =
NOT_PROVEN

---

## 7. D3-F1 CLOSURE

D3_F1 =
HUMAN_ADOPTED_AND_CLOSED

CONNECTION_FAILURE_ROOT_CAUSE =
SUPPORTED_BUT_NOT_PROVEN

REPAIR_SELECTED =
NONE

NEW_REAL_TEST_EXECUTED_DURING_F1 =
NO

LOGIN_DURING_F1 =
NO

CONNECTION_DURING_F1 =
NO

GETTICKS_DURING_F1 =
NO

MARKET_DATA_BYTES_DURING_F1 =
0

CACHE_MUTATION_DURING_F1 =
NO

---

## 8. NEXT CANDIDATE

NEXT_CANDIDATE =

E1-TD-03C-JF02-D3-F2 —
CONNECTION-ONLY STATE-OBSERVABILITY CONTROL V0.1

PURPOSE =

Discriminate the connection phase itself before returning
to any historical-data experiment.

F2 SHOULD preserve:

SDK =
3.6.51

API =
2.13.99

ACCOUNT_MODE =
DEMO

and SHALL perform:

- one login only;
- one connect attempt only;
- zero reconnect;
- zero retry;
- zero strategy start;
- zero getTicks;
- zero historical-data request;
- zero market-data acquisition.

F2 SHOULD record:

- connect() start timestamp;
- connect() return timestamp;
- connect() duration;
- exact exception class if connect() throws;
- onConnect timestamp;
- onDisconnect timestamp;
- isConnected observations over a preregistered window;
- final connection-state classification.

A longer observation window MAY be authorized prospectively,
but its exact duration MUST be frozen before execution.

---

## 9. F2 AUTHORITY

D3_F2_AUTHORIZED =
NO

This adjudication does NOT authorize:

- login;
- connection;
- retry;
- strategy start;
- getTicks;
- history request;
- cache mutation;
- market data;
- trading.

A separate human authorization is required.

---

## 10. STOP

NEXT =
SEPARATE_HUMAN_AUTHORIZATION_FOR_D3_F2

STOP =
TRUE
