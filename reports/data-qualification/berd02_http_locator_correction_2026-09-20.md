# B-ERD-02 — HTTP LOCATOR CORRECTION AFTER GITHUB ACTIONS TLS BLOCK

**Date:** 2026-09-20
**Prior run:** 35532656928
**Prior run HEAD:** 828b0fc8555f78a919330c360870aaf9bab8c10d
**Prior result:** BLOCKED

The GitHub Actions runtime itself executed correctly. All nine K1 HTTPS attempts failed before HTTP status with TLS/connection timeouts.

This is a demonstrated transport defect, not K1 evidence.

Pinned independent source `saleem-latif/duka-data@2220708e...` explicitly renders the legacy hourly locator with `http://datafeed.dukascopy.com/datafeed`. B-PE-03 also preserved the historical Dukascopy statement describing an HTTP file server.

Therefore the minimum correction is:

~~~text
LocatorManifest V0.1 HTTPS
→ superseded for this rerun by
LocatorManifest V0.2 HTTP
~~~

Nothing else changes:

- same USATECH instrument;
- same PW/P0-P7 windows;
- same zero-indexed month rule;
- same no-retry policy;
- same exact body/header capture;
- same independent diagnostics;
- K2 remains SECURITY_CAPTURE_POLICY_BLOCK;
- no full acquisition or backtest.

The V0.1 HTTPS run remains immutable evidence of its own transport failure.

**Verdict: PASS TO EXECUTE ONE NEW HTTP-LOCATOR BOUNDED RUN.**
