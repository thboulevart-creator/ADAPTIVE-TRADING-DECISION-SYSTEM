# B-ERD-01 — CORRECTED CONTRACT — PERSISTED-HEAD RE-BREAK

**Date:** 2026-09-20
**Corrected candidate HEAD:** 9f5c5981ca7ef60031c7b15bfc9a432fabbd2cd1
**Corrected candidate blob:** ce67994d1ba325bff632beb77b29024caa9d4512

## 1. Initial defect closure

The corrected candidate closes BERD01-F01 through BERD01-F07:

~~~text
F01 exact PT1H comparison window
F02 family observed/not-observed/refuted/transport distinctions
F03 GET + zero automatic retry
F04 candidate/probe/overall disposition separation
F05 evidenced unknown vs known-candidates-insufficient
F06 B-PE-01 canonical JSON seal binding
F07 explicit warmup probe + FULL_D_REPRESENTATION_DOMAIN
~~~

Those defects were not reproduced.

## 2. Residual defects

### BERD01-R01 — OVERALL TARGET PROPOSITION IS META-DISCRIMINATION, NOT THE PROJECT PREMISE

The corrected contract defines T0 as:

~~~text
"the bounded probe set can discriminate the observed representation state..."
~~~

This makes PROBE_SUPPORTED a statement about whether the experiment was informative, not whether the project's current K1 hourly representation premise survived.

Attack:

At P4, K1 is conclusively refuted and K2 is supported.

The probe successfully discriminates the state.

Under current T0:

~~~text
overall = PROBE_SUPPORTED
~~~

But the most important project-level fact is that the current K1 premise was refuted.

The verdict therefore hides the decision-relevant result.

Verdict: DEMONSTRATED RESIDUAL DEFECT.

Correction required:

Define the overall target proposition as the current project premise:

~~~text
T_HOURLY =
"K1 legacy-hourly representation is empirically compatible with every required bounded probe window"
~~~

Verdict precedence:

~~~text
if any required probe has K1 = REFUTED on valid non-transport evidence
→ overall = PROBE_REFUTED

else if any required probe is BLOCKED or K1 is NOT_OBSERVED without refutation/support
→ overall = BLOCKED

else if every required probe has K1 = SUPPORTED
→ overall = PROBE_SUPPORTED
~~~

K2/coexistence/unknown results remain diagnostic alternatives and must still be persisted.

PROBE_SUPPORTED remains bounded and does not imply full-interval qualification.

---

### BERD01-R02 — HTTP BODY HASH DOMAIN / REQUEST POLICY NOT BYTE-DETERMINISTIC

The contract says raw response bytes are preserved exactly and fixes GET/no retry.

It does not specify whether an HTTP client may transparently apply Content-Encoding decompression before raw_response_sha256 is computed.

Attack:

Same provider response:

~~~text
Content-Encoding: gzip
wire entity bytes = X
auto-decoded client body = Y
~~~

Implementation A hashes X.
Implementation B hashes Y.

Both claim to hash "raw response bytes."

Request headers and redirect following are also not normatively bound, so provider/CDN behavior can differ within one contract version.

Verdict: DEMONSTRATED RESIDUAL DEFECT.

Correction required:

Add a sealed TransportPolicy input before any object request:

~~~text
schema = B_ERD_01_TRANSPORT_POLICY_V0_2

transport_policy_id
method = GET
automatic_retry_count = 0
automatic_content_decoding = false
request_headers
redirect_policy
max_redirect_hops
connect_timeout_seconds
read_timeout_seconds
policy_seal
~~~

Mandatory request header:

~~~text
Accept-Encoding: identity
~~~

Persist exact request headers.

Define:

~~~text
raw_response_sha256 =
SHA256(exact response body bytes exposed with HTTP content decoding disabled)
~~~

Redirect chain must be captured hop-by-hop.

A policy change requires a new execution identity and cannot overwrite prior evidence.

## 3. Re-break verdict

~~~text
B-ERD-01 CORRECTED CONTRACT = FAIL
~~~

Only BERD01-R01 and BERD01-R02 are authorized for correction.

No real provider/data action occurred.
