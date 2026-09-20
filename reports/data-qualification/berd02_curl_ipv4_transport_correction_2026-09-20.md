# B-ERD-02 — CURL / IPv4 TRANSPORT CORRECTION

**Date:** 2026-09-20

Observed evidence:

~~~text
run 35532656928:
Python HTTPS transport timed out before HTTP status on all 9 K1 probes.

run 35532946835:
HTTP transport returned 301 on all 9 probes.
Every Location header pointed exactly to the already registered HTTPS K1 locator.
~~~

The locator itself is therefore no longer ambiguous. The next correction changes only client transport behavior:

~~~text
canonical HTTPS K1 locator
curl
IPv4 forced
HTTP/1.1
retry = 0
redirect follow = 0
Accept-Encoding: identity
exact response body preserved
actual request-header trace preserved
response headers preserved
~~~

No date, probe, decoding premise, acquisition scope or backtest boundary changes.

K2 remains SECURITY_CAPTURE_POLICY_BLOCK.

**Verdict: PASS TO EXECUTE ONE NEW CURL/IPv4 BOUNDED RUN.**
