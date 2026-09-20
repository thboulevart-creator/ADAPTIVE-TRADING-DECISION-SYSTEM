# B-ERD-02 — GITHUB ACTIONS TRANSPORT RUNTIME RE-ENTRY REVIEW

**Date:** 2026-09-20
**Starting HEAD:** 3d5179024982b4effc1ae3aa94d2454cf22ad7d5
**Verdict:** PASS TO RUN ONE NEW BOUNDED EXECUTION ID

The prior B-ERD-02 execution was BLOCKED only because the chat/web runtime did not expose binary BI5 HTTP responses.

The user explicitly requested that the transport-capable runtime be put in place directly.

Reuse is authorized for the already sealed LocatorManifest and ProbePlan. Current Dukascopy documentation was reverified on 2026-09-20: the provider still documents the Requester Pays S3 daily tick archive and warns that legacy hourly files can use an hourly timestamp base. AWS documentation still requires authenticated Requester Pays requests.

## K1

K1 is executed through raw HTTPS GET in GitHub Actions with:

~~~text
retry = 0
Accept-Encoding: identity
no automatic redirect
no HTTP content decoding
exact response body preservation
all response headers preservation
50 MiB body cap
~~~

K1 requires two independent diagnostics before SUPPORTED.

## K2

K2 requires AWS SigV4. B-ERD-01 also requires exact request-header persistence.

Persisting the exact signed Authorization header would expose credential-bearing material, so this runtime intentionally sets:

~~~text
K2 = SECURITY_CAPTURE_POLICY_BLOCK
~~~

and sends no K2 request.

This is not evidence of K2 absence.

## New execution identity

~~~text
BERD02-GHA-<github_run_id>-<github_run_attempt>
~~~

The previous closed execution identity is not reused.

## Scope

Only PW/P0-P7 K1 locators from the sealed ProbePlan may be fetched.

Still prohibited:

~~~text
full acquisition
D materialization
backtest
paper/broker/live
~~~
