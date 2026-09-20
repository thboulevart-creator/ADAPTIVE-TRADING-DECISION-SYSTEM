# B-ERD-02 — BOUNDED EMPIRICAL REPRESENTATION-DISCRIMINATION — FINAL SUPPORTED CLOSEOUT

**Date:** 2026-09-20  
**Repository:** thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM  
**Branch:** integration/system-v1  
**Final evidence HEAD before closeout:** 3cad19a8f4f4ee06873c5a6f7f62bf68a0e889df

## 1. Runtime evolution

Three immutable execution attempts were required to obtain a transport-capable bounded probe.

### Run 35532656928 — Python HTTPS

~~~text
source HEAD = 828b0fc8555f78a919330c360870aaf9bab8c10d
result = BLOCKED
9/9 K1 = TLS/connection timeout before HTTP status
~~~

No retry was performed.

### Run 35532946835 — evidenced HTTP locator

~~~text
source HEAD = ee2cafaf3dfbdae6c84a2a9eed557c484f71314f
result = BLOCKED
9/9 K1 = HTTP 301
~~~

Every `Location` header pointed exactly to the already registered HTTPS K1 locator.

This established that the historical HTTP path canonicalizes to the registered HTTPS object path.

### Run 35533153289 — curl / IPv4 / HTTPS

~~~text
source HEAD = 2eb8350fb24c3043017c91475d202b5e0d6bb501
execution_id = BERD02-GHA-35533153289-1
workflow conclusion = success
overall_probe_verdict = PROBE_SUPPORTED
~~~

Transport policy:

~~~text
curl
IPv4 forced
HTTP/1.1
GET
retry = 0
redirect follow = 0
Accept-Encoding: identity
exact response body preserved
actual outbound header trace preserved
response headers preserved
~~~

## 2. Exact K1 transport result

All nine required bounded probes returned:

~~~text
HTTP 200
OBJECT_BYTES_OBTAINED
FAMILY_OBSERVED
~~~

Exact raw body evidence:

~~~text
PW  bytes=14931   sha256=8698d78a705b61e8da22e4577736c80975ff9600cb43d73151acf5e69d045aa7
P0  bytes=19224   sha256=d2a5ee662d3669f477b7c621080c5c302644ffa213e9a88319fb7fb7e5668b41
P1  bytes=21365   sha256=3e822be146df9a0a841806ebf56b34fde628faef37c8cc2d246c9f3550a83a27
P2  bytes=45739   sha256=00b9651b22a8d38c0f6cd7f4ce5921c7a31c213d7c587a05bc1df5a550f23f6a
P3  bytes=41480   sha256=1fdd059df242e5d8a947319d981a187df208d0771204a249a92d2eadc8c0f639
P4  bytes=34789   sha256=2c05aa59e85e8f50377f5504b445e78e9e08f07283329eb054dd229b51a5176d
P5  bytes=54305   sha256=1db10b7adfff4fb9e2e3056e585b29a84784836ece574c4f3579bae34a05a9bc
P6  bytes=104246  sha256=29a5865bc6b1f3ec13111f51fc499a780efb6896f69db44180714f61a1d3ef87
P7  bytes=17831   sha256=f4f6f3c529d8454dd661a52116b7533fe3a266a7f45dcd0fde0536367d90041e
~~~

## 3. Independent semantic diagnostics

Diagnostic A:

~~~text
Python lzma FORMAT_ALONE
+
struct >IIIff
~~~

Diagnostic B:

~~~text
xz --format=lzma -dc
+
independent manual integer parse
~~~

Both diagnostic paths succeeded on all nine raw inputs.

For every probe:

~~~text
A decompressed SHA-256 = B decompressed SHA-256
A projection SHA-256   = B projection SHA-256
A record count         = B record count
plausibility errors    = 0
~~~

Record counts:

~~~text
PW  3048
P0  3792
P1  4348
P2  9282
P3  7875
P4  6967
P5  10609
P6  20259
P7  3650
~~~

Every candidate timestamp offset remained inside the hourly millisecond domain and no zero raw price, ask<bid, or non-finite volume diagnostic violation occurred.

Therefore each bounded K1 disposition is:

~~~text
SUPPORTED
reason = TWO_INDEPENDENT_DIAGNOSTICS_AGREE
~~~

## 4. Exact persisted evidence

GitHub Actions source run:

~~~text
workflow run = 35533153289
job = 106137359561
artifact = 10612217020
artifact digest =
sha256:ec36b42f01116374ce017d1d00544a2862b83845d0066110d5d01c7d3bb62f61
~~~

Exact evidence is now durable in:

~~~text
evidence/berd02/gha_run_35533153289/
~~~

Key blobs:

~~~text
PROVENANCE.json
dff6f3d3e82d21df484173320fea09ada9203f7c

execution_result.json
c4d994a9c39cb2addae492a4f55556c7f799d091

transport_captures.json
7048fd421e934382dfbbe830e23fd3f6161540e3

diagnostic_a.json
77c5b216e92bd04e9c3bb121e7b2759bf38a66b7

diagnostic_b.json
6322cc44bdedb89a377f9e7c401446c36a4407d7
~~~

Result seal:

~~~text
ab5c5bdf97ce3dcfa773ed555afa842443ef21b7a155057ab0e9517bb573f5ef
~~~

Capture-set seal:

~~~text
cd989e127a43145dad52aee53f3f6bbdc466b1242f0f039a9a898ace973e6336
~~~

Independent post-download verification confirmed:

~~~text
result seal = exact
9/9 capture seals = exact
18/18 diagnostic seals = exact
9/9 raw body hashes = exact
9/9 raw body byte lengths = exact
~~~

## 5. K2 boundary

K2 was deliberately not executed.

State:

~~~text
K2 = SECURITY_CAPTURE_POLICY_BLOCK
request_sent = false
~~~

Reason:

AWS Requester Pays requires a signed request, while B-ERD-01 requires exact request-header persistence. Persisting an exact AWS SigV4 Authorization value would expose credential-bearing material.

No K2 absence/refutation/support is inferred.

## 6. Final B-ERD-02 verdict

~~~text
B-ERD-02 BOUNDED EMPIRICAL
REPRESENTATION-DISCRIMINATION EXECUTION = PROBE_SUPPORTED
~~~

Exactly:

~~~text
K1_SUPPORTED = 9 / 9
K1_REFUTED = 0
K1_NOT_OBSERVED = 0
K1_BLOCKED = 0

T_HOURLY =
SUPPORTED ON EVERY REQUIRED BOUNDED PROBE
~~~

This is the first direct empirical evidence in the project that the legacy hourly K1 representation is actually retrievable and semantically consistent for USATECHIDXUSD at stratified points spanning the warmup boundary and 2021–2026 target interval.

## 7. Anti-extrapolation remains binding

Hard boundary:

~~~text
PROBE_SUPPORTED
≠
FULL_INTERVAL_QUALIFIED
~~~

Nine supported probes do not prove every manifest-relevant H1 in the five-year domain.

This result therefore does not set:

~~~text
C08-D4 = PASS
C08-D5 = PASS
BPE-C08 = PASS
B = PASS
D = materialized
~~~

under current governance.

## 8. Current global state

~~~text
B-PE-05 = NOT EXECUTED
K2 empirical state = BLOCKED / NOT EXECUTED

C08-D4 documentary state = BLOCKED
C08-D5 documentary state = BLOCKED
BPE-C08 = BLOCKED
B global executable gate = BLOCKED
FINAL EXECUTABLE DATA GATE = BLOCKED
~~~

No full acquisition, no backtest, no paper/broker/live execution occurred.

## 9. Required next governance decision

B-PE-04R previously required an explicit decision before empirical evidence could ever replace the provider-primary documentary threshold.

Now that B-ERD-02 has produced real empirical K1 support, the next governed action should be:

~~~text
B-PE-01R —
empirical evidence sufficiency / provider-primary supersession review
~~~

Purpose:

~~~text
decide prospectively whether
FULL_INTERVAL_QUALIFIED empirical representation evidence
can satisfy C08-D4/D5 operationally
without direct Dukascopy support confirmation,
while preserving the stricter provider-evidence requirements
for any dimensions where empirical equivalence is not enough
~~~

Only after that rule decision should the project spend effort on exhaustive full-interval representation qualification.

STOP.
