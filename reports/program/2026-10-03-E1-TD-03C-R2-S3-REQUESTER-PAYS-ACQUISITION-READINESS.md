# E1-TD-03C-R2 — S3 REQUESTER-PAYS ACQUISITION READINESS

**Date:** 2026-10-03  
**Mode:** READINESS / METADATA-ONLY  
**Market object download:** FORBIDDEN  
**Real market bytes:** FORBIDDEN  
**AWS spend:** NOT AUTHORIZED

## 1. Authority binding

Human authorization was issued against:

```text
AUTHORIZED_PARENT_HEAD =
612fb196b45c79e096ea26cf2e09d65435467e5a

AUTHORIZED_PARENT_TREE =
1268f03a4e53e02d6e2efd9296b547c2bdb67c11
```

Before R2 persistence, the governed branch had advanced to:

```text
PERSISTENCE_PARENT_HEAD =
18e9b0543736804a3a6fd8429ca89fc24216f4e1

PERSISTENCE_PARENT_TREE =
b404c0be3a56ed8e9e0c45d0e4a6730b707240b2
```

The intervening canonical delta was reviewed and contains only RTMA-01 synthetic-change-lab artifacts. No E1-TD-03C, Lane-B, TD01, Source-B, runtime, breaker or real-event artifact was modified.

Therefore the original human authority remains the execution authority binding; the newer HEAD is used only as the persistence parent.

## 2. Official S3 acquisition mechanism

Current Dukascopy documentation identifies:

```text
BUCKET =
cfg-public-proper-wallaby

REGION =
eu-west-1

BILLING =
REQUESTER PAYS

ANONYMOUS ACCESS =
NOT SUPPORTED

DOCUMENTED PATH CONVENTION =
SYMBOL/YEAR/MONTH/DAY_ticks.bi5

MONTH =
ZERO-INDEXED
```

The documented example maps January to month directory `00`; therefore October maps to `09`.

The official documentation recommends AWS CLI or Boto3 with valid AWS credentials and `RequestPayer=requester`.

AWS documentation states that successful Requester Pays requests charge the requester for the request and, when applicable, data transfer. A `HeadObject` against a Requester Pays bucket also uses the requester-pays acknowledgement.

## 3. Instrument documentary identity

Current Dukascopy market documentation identifies:

```text
INSTRUMENT =
USATECH.IDX/USD

DESCRIPTION =
US 100 Tech Index
```

This establishes the commercial instrument identity only.

It does **not** independently establish the exact top-level S3 symbol prefix.

## 4. Candidate S3 identity

Using the previously used provider-symbol normalization and the official daily path convention, the preregistered candidate is:

```text
CANDIDATE_SYMBOL_PREFIX =
USATECHIDXUSD

CANDIDATE_KEY =
USATECHIDXUSD/2026/09/01_ticks.bi5

LOGICAL_DATE_UTC =
2026-10-01
```

Classification:

```text
CANDIDATE_SYMBOL_PREFIX_STATUS =
UNVERIFIED_IN_S3

CANDIDATE_KEY_EXISTENCE_STATUS =
UNVERIFIED_IN_S3
```

No claim of S3 existence is made.

## 5. Local AWS readiness

Fresh non-secret inspection found:

```text
AWS_CLI_PRESENT = FALSE
BOTO3_PRESENT = FALSE
BOTOCORE_PRESENT = FALSE

AWS_CREDENTIALS_FILE_EXISTS = FALSE
AWS_CONFIG_FILE_EXISTS = FALSE

AWS_ACCESS_KEY_ID_ENV_PRESENT = FALSE
AWS_SECRET_ACCESS_KEY_ENV_PRESENT = FALSE
AWS_SESSION_TOKEN_ENV_PRESENT = FALSE
AWS_PROFILE_ENV_PRESENT = FALSE
```

No secret value was inspected, printed or persisted.

## 6. Requester-Pays cost gate

The metadata verification requested by R2 would require authenticated Requester Pays S3 calls.

The intended minimal metadata sequence is preregistered as:

```text
STEP 1 =
ListObjectsV2
Bucket=cfg-public-proper-wallaby
Delimiter="/"
RequestPayer="requester"

PURPOSE =
verify exact top-level instrument prefix

STEP 2 =
HeadObject
Bucket=cfg-public-proper-wallaby
Key=USATECHIDXUSD/2026/09/01_ticks.bi5
RequestPayer="requester"

PURPOSE =
verify exact candidate object metadata
```

Neither operation downloads the object body.

However, successful Requester Pays metadata requests are billable S3 requests. The human explicitly withheld AWS-spend authority unless separately required and authorized.

Therefore:

```text
METADATA_PREFIX_VERIFICATION =
NOT_EXECUTED

METADATA_KEY_VERIFICATION =
NOT_EXECUTED

REASON =
MISSING_AWS_CREDENTIAL_CAPABILITY
+
AWS_REQUESTER_PAYS_SPEND_NOT_AUTHORIZED
```

No S3 API request was made.

## 7. Event 0002 preregistration

A separate machine-readable preregistration has been prepared for:

```text
E1-TD-03C-REAL-EVENT-0002
```

The candidate future request is frozen as:

```text
OPERATION =
GetObject

BUCKET =
cfg-public-proper-wallaby

REGION =
eu-west-1

REQUEST_PAYER =
requester

CANDIDATE_KEY =
USATECHIDXUSD/2026/09/01_ticks.bi5

MAX_GET_REQUESTS =
1

RETRIES =
0

FALLBACK_KEY =
FALSE

ALTERNATE_ENDPOINT =
FALSE
```

This preregistration is deliberately:

```text
PREREGISTERED_NON_EXECUTABLE
```

because the exact S3 prefix/key have not yet been metadata-verified and no requester-pays spend authority exists.

If metadata later disproves the candidate prefix or key, Event 0002 must not execute under this V0.1 preregistration. A new exact preregistration version is required before any real GET.

## 8. Protected boundaries

No action in R2 performed or authorized:

```text
MARKET_OBJECT_DOWNLOAD
REAL_MARKET_BYTES
SOURCE_B_EQUIVALENCE
SOURCE_B_SUBSTITUTION
TD01_MERGE
HISTORICAL_OVERLAP_ANALYSIS
H1
SIGNALS
STRATEGIES
PNL
PERFORMANCE
BACKTEST
```

## 9. R2 verdict

```text
OFFICIAL_S3_BUCKET_REGION_BINDING =
PASS_DOCUMENTARY

REQUESTER_PAYS_REQUIREMENT_MAPPING =
PASS_DOCUMENTARY

INSTRUMENT_DOCUMENTARY_IDENTITY =
PASS_DOCUMENTARY

LOCAL_AWS_TOOLING_READINESS =
BLOCKED_MISSING_TOOLING

AWS_CREDENTIAL_CAPABILITY =
BLOCKED_MISSING

AWS_SPEND_AUTHORITY =
NOT_AUTHORIZED

S3_PREFIX_METADATA_VERIFICATION =
NOT_EXECUTED_BLOCKED

S3_KEY_METADATA_VERIFICATION =
NOT_EXECUTED_BLOCKED

EVENT_0002_PREREGISTRATION =
PREPARED_NON_EXECUTABLE

E1_TD_03C_R2 =
READINESS_PRODUCED_FAIL_CLOSED

STOP =
TRUE
```

## 10. Next required decision

The next boundary is not Event 0002 itself.

It is a narrowly bounded requester-pays enablement step that must decide whether to authorize:

1. minimal AWS client capability;
2. non-secret credential setup by the human;
3. a tiny explicit AWS request-cost budget;
4. exactly the two preregistered metadata calls;
5. STOP before any `GetObject`.

No real market object should be requested until those metadata gates pass and Event 0002 receives separate human authority.
