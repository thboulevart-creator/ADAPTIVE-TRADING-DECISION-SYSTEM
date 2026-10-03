# E1-TD-03C-R2A — REQUESTER-PAYS ENABLEMENT + METADATA PROBE

**Date:** 2026-10-03  
**Mode:** READINESS + METADATA-ONLY  
**Authorized parent HEAD:** `b7e0c643e580af917dbb741a78b308d42d3f3c27`  
**Authorized parent TREE:** `9cdd77ca46aaffbbc7816c318c2a3df233db2778`

## 1. Result

```text
MINIMAL_AWS_CLIENT_ENABLEMENT =
PASS

AWS_CREDENTIAL_CAPABILITY =
BLOCKED_MISSING

ListObjectsV2 =
NOT_EXECUTED

HeadObject =
NOT_EXECUTED

AWS_REQUEST_COST_CONSUMED =
0

MARKET_OBJECT_DOWNLOAD =
FALSE

REAL_MARKET_BYTES =
FALSE

EVENT_0002_VERIFIED_KEY_FREEZE =
NOT_ACHIEVED

STOP =
TRUE
```

R2A stopped before any S3 request because no AWS credential capability exists on the execution machine.

## 2. Minimal AWS client

A dedicated isolated Python environment was created outside the repository:

```text
C:\Users\Boulevart\ATDS-TOOLS\aws-metadata-client-v0.1\.venv
```

Installed runtime:

```text
Python =
3.13.14

boto3 =
1.43.108

botocore =
1.43.108
```

No AWS CLI was required.

This environment creation did not modify the governed repository and did not access market data.

## 3. Non-secret credential-capability check

The credential provider chain was inspected with EC2 instance metadata disabled.

Observed:

```text
AVAILABLE_PROFILES = 0
CREDENTIALS_RESOLVED = FALSE
CREDENTIAL_METHOD = NONE
REGION_RESOLVED = NONE

ENV_ACCESS_KEY_PRESENT = FALSE
ENV_SECRET_KEY_PRESENT = FALSE
ENV_SESSION_TOKEN_PRESENT = FALSE

AWS_CREDENTIALS_FILE_EXISTS = FALSE
AWS_CONFIG_FILE_EXISTS = FALSE
```

No credential value or secret was displayed, read into evidence, or persisted.

## 4. Requester Pays requirement

Dukascopy currently documents its raw historical-data archive as:

```text
BUCKET =
cfg-public-proper-wallaby

REGION =
eu-west-1

POLICY =
REQUESTER PAYS
```

and requires valid AWS credentials.

Amazon S3 documents that Requester Pays buckets do not support anonymous requests and that authenticated requests must acknowledge requester payment. `ListObjectsV2` and `HeadObject` support the requester-pays acknowledgement.

Documentary sources:

- https://www.dukascopy.com/wiki/en/development/data-export/
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/RequesterPaysBuckets.html
- https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjectsV2.html
- https://docs.aws.amazon.com/AmazonS3/latest/API/API_HeadObject.html

## 5. Preregistered metadata calls

The authorization allowed at most:

```text
1 × ListObjectsV2
1 × HeadObject
```

The first call was preregistered as:

```text
API =
ListObjectsV2

Bucket =
cfg-public-proper-wallaby

Delimiter =
/

RequestPayer =
requester

Purpose =
verify exact top-level instrument prefix
```

Observed execution count:

```text
0
```

Reason:

```text
BLOCKED_MISSING_AWS_CREDENTIAL_CAPABILITY
```

Because the prefix was not verified, the conditional `HeadObject` was not permitted to execute.

```text
HeadObject execution count =
0
```

## 6. Event 0002 state

The existing preregistration remains:

```text
GOVERNANCE/
E1-TD-03C-EVENT-0002-S3-REQUEST-PREREGISTRATION-V0.1.json

BLOB =
04ac356046d57b168596dc9381b9cfd523439bdd
```

Candidate:

```text
USATECHIDXUSD/2026/09/01_ticks.bi5
```

Current status remains:

```text
S3_PREFIX =
UNVERIFIED

CANDIDATE_KEY =
UNVERIFIED

VERIFIED_EVENT_0002_KEY_FROZEN =
FALSE

EVENT_0002_EXECUTABLE =
FALSE
```

The candidate must not be promoted to a verified key from documentary inference alone.

## 7. Cost boundary

Although the human authorized the minimum necessary Requester Pays metadata cost, no authenticated request could be executed.

Therefore:

```text
AWS_REQUESTS_SENT =
0

AWS_REQUEST_COST_CONSUMED =
0

DATA_TRANSFER =
0
```

## 8. Protected boundaries

No action performed:

```text
GetObject
MARKET OBJECT DOWNLOAD
REAL MARKET BYTES
DECOMPRESSION
DECODING
SOURCE-B EQUIVALENCE
SOURCE-B SUBSTITUTION
TD01 MERGE
HISTORICAL OVERLAP ANALYSIS
H1
SIGNALS
STRATEGIES
PNL
PERFORMANCE
BACKTEST
```

## 9. Verdict

```text
E1_TD_03C_R2A =
BLOCKED_PENDING_HUMAN_AWS_CREDENTIAL_CAPABILITY

MINIMAL_AWS_CLIENT =
READY

METADATA_PROBE =
NOT_STARTED

VERIFIED_EVENT_0002_KEY =
NOT_AVAILABLE

STOP =
TRUE
```

## 10. Next boundary

The next step is not a second R2A probe and not Event 0002.

A human must first establish AWS credential capability on the execution machine without disclosing secret values into ATDS evidence.

After that, a fresh authority/state check may resume R2A using the already authorized limits:

```text
ListObjectsV2 = MAX 1
HeadObject = MAX 1, ONLY IF PREFIX MATCHES
GetObject = FORBIDDEN
```

No new market-data authority follows from this report.
