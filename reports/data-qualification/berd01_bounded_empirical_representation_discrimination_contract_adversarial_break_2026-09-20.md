# B-ERD-01 — BOUNDED REPRESENTATION-DISCRIMINATION CONTRACT — ADVERSARIAL BREAK

**Date:** 2026-09-20
**Candidate HEAD:** a2452d9dbe43952d1837f85ffa74864201ca2152
**Candidate blob:** c9d8c0ab270050f373607fb9f6800335582dd29a

## 1. Attack objective

Try to make the future bounded probe return a convincing representation conclusion while:

- hourly and daily candidates cover different time scopes;
- transport failure masquerades as representation absence;
- network retry choices become outcome-dependent;
- multiple hypotheses make the overall verdict ambiguous;
- an unknown representation is inferred without observable evidence;
- sealed artifacts are not independently reproducible;
- the mandatory warmup domain is omitted from later full-interval qualification.

## 2. Demonstrated defects

### BERD01-F01 — PROBE_COMPARISON_WINDOW_NOT_NORMATIVELY_FIXED

The candidate resolves each anchor to a "market-open probe interval" but does not define its exact duration.

Attack:

- K1 hourly probe represents one hour;
- K2 daily object contains a whole UTC/provider day;
- the comparison uses all K2 observations instead of the same one-hour target window.

The resulting cardinality/coverage comparison is meaningless while appearing deterministic.

Verdict: DEMONSTRATED DEFECT.

Correction required:

Every probe must resolve to one exact governed H1 comparison window:

~~~text
W_probe = [market_h1_start_utc, market_h1_start_utc + 1 hour)
~~~

All candidate representations must be projected to exactly W_probe before cross-family coverage comparison.

Daily surrounding observations remain captured but are outside the comparison window.

---

### BERD01-F02 — REPRESENTATION_ABSENCE / MARKET_ABSENCE / TRANSPORT_FAILURE NOT CLOSED

The candidate correctly states that 404 alone does not prove representation absence, but PROBE_SUPPORTED examples still permit one family to be "validly absent or refuted" without defining valid absence evidence.

Attack:

A known market-open H1 interval is probed, but the hourly locator returns 404 because of:

- transient CDN inconsistency;
- wrong locator rendering;
- server policy;
- provider-side archive gap.

K2 succeeds.

Without a closed absence predicate, K1 can be incorrectly refuted.

Verdict: DEMONSTRATED DEFECT.

Correction required:

Define exact family disposition predicates:

~~~text
FAMILY_OBSERVED
FAMILY_NOT_OBSERVED
FAMILY_REFUTED
FAMILY_TRANSPORT_BLOCKED
FAMILY_LOCATOR_BLOCKED
~~~

FAMILY_NOT_OBSERVED carries zero refutation weight.

FAMILY_REFUTED requires a falsifiable candidate prediction plus valid captured evidence that contradicts it; transport status alone is insufficient.

---

### BERD01-F03 — HTTP METHOD / RETRY POLICY DEFERRED

Candidate says HEAD is insufficient and retry policy must be fixed before execution, but leaves both mutable.

Attack:

One execution uses HEAD first, another GET.
One retries 404/5xx until success; another does not.

Outcome can change without changing contract/version.

Verdict: DEMONSTRATED DEFECT.

Correction required:

For BI5 object probes:

~~~text
request_method = GET
automatic_retry_count = 0
~~~

Any timeout, 429, 5xx, auth/policy error, incomplete transport or client transport exception:

~~~text
probe candidate transport = BLOCKED
~~~

A rerun is a new execution ID and never overwrites the prior capture.

---

### BERD01-F04 — MULTI-HYPOTHESIS OVERALL PROBE_REFUTED IS AMBIGUOUS

Per-probe candidate hypotheses can be independently supported/refuted.

But the candidate also defines one overall verdict:

~~~text
PROBE_SUPPORTED
PROBE_REFUTED
BLOCKED
~~~

Attack:

K1 is refuted at P4 while K2 is supported at P4.

Is the overall result PROBE_SUPPORTED or PROBE_REFUTED?

Both are defensible under current wording.

Verdict: DEMONSTRATED DEFECT.

Correction required:

Separate:

~~~text
per_candidate_disposition =
SUPPORTED | REFUTED | NOT_OBSERVED | BLOCKED

per_probe_disposition =
DISCRIMINATED | NON_DISCRIMINATING | BLOCKED

overall_probe_verdict =
PROBE_SUPPORTED | PROBE_REFUTED | BLOCKED
~~~

Define overall PROBE_REFUTED against one explicit predeclared target proposition, not merely because any candidate was refuted.

For B-ERD-01 the target proposition should be:

~~~text
T0 = "the bounded probe set can discriminate the observed representation state
      without unresolved transport/unknown/semantic competition"
~~~

Then:

- PROBE_SUPPORTED = T0 holds for every required probe;
- PROBE_REFUTED = valid captures demonstrate T0 is false for at least one required probe for a non-transport reason;
- BLOCKED = evidence is insufficient/ambiguous/unknown/transport-blocked to decide T0.

---

### BERD01-F05 — H_UNKNOWN TRIGGER OVERCLAIMS UNOBSERVABLE UNKNOWN FAMILY

The candidate says known candidates failing to explain provider behavior can establish H_UNKNOWN.

But if K1 and K2 simply return no usable material, the execution has not observed a third representation.

Verdict: DEMONSTRATED DEFECT.

Correction required:

Separate:

~~~text
UNKNOWN_REPRESENTATION_EVIDENCED
KNOWN_CANDIDATES_INSUFFICIENT
~~~

UNKNOWN_REPRESENTATION_EVIDENCED requires positive observed evidence such as:

- redirect to unregistered family;
- provider response bytes/content structure incompatible with registered signatures;
- provider metadata explicitly identifying another object family.

If all known candidates are merely absent/unusable:

~~~text
KNOWN_CANDIDATES_INSUFFICIENT
→ BLOCKED
~~~

Do not claim an unknown family was observed.

---

### BERD01-F06 — STRUCTURED SEAL CANONICALIZATION NOT BOUND

LocatorManifest, ProbePlan, TransportCapture and ExecutionResult have seal fields but the candidate does not bind their canonical byte rule.

Two implementations can seal semantically identical JSON differently.

Verdict: DEMONSTRATED DEFECT.

Correction required:

All structured artifacts inherit exactly the B-PE-01 canonical JSON and SHA-256/lowercase-hex rules.

Every schema must define:

~~~text
seal =
SHA256(canonical_json(payload_without_seal))
~~~

Raw body SHA-256 remains over exact response bytes.

---

### BERD01-F07 — FULL D WARMUP REPRESENTATION COVERAGE NOT EXPLICIT

The future D domain is:

~~~text
mandatory 20-H1 warmup prefix
+
five-year evaluation window
~~~

The candidate probes the evaluation interval only.

Its FULL_INTERVAL_QUALIFIED section says "every manifest-relevant interval", but does not explicitly bind the warmup prefix.

Attack:

Representation differs only in the mandatory warmup prefix.

Evaluation interval is fully qualified, but D is incorrectly promoted despite unqualified warmup material.

Verdict: DEMONSTRATED DEFECT.

Correction required:

Define:

~~~text
FULL_D_REPRESENTATION_DOMAIN =
mandatory deterministic 20-H1 warmup prefix
+
frozen evaluation interval
~~~

Any future FULL_INTERVAL_QUALIFIED claim used by D must cover this entire domain.

Add a bounded warmup probe anchor:

~~~text
PW = final governed market-open H1 interval of the mandatory warmup prefix
~~~

This does not qualify the warmup; it only includes it in bounded discrimination.

## 3. Attacks that did not demonstrate defects

The candidate already resists:

- hourly-first assumption;
- closed-world hourly/daily assumption;
- silent sample-to-full-period promotion;
- using strategy profitability as a plausibility criterion;
- using I_A/I_B agreement as provider authority;
- reusing provider contact as a hidden prerequisite;
- full D/backtest permission leakage.

## 4. Initial verdict

~~~text
B-ERD-01 CONTRACT CANDIDATE = FAIL
~~~

Seven defects demonstrated.

Only BERD01-F01 through F07 are authorized for correction.

No provider contact, BI5 download, BI5 processing, acquisition or backtest occurred.
