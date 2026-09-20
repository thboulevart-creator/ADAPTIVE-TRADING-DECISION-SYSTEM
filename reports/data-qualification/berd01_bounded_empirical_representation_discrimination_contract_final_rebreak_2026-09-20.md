# B-ERD-01 — BOUNDED EMPIRICAL REPRESENTATION-DISCRIMINATION CONTRACT — FINAL PERSISTED-HEAD RE-BREAK

**Date:** 2026-09-20
**Repository:** thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM
**Branch:** integration/system-v1
**Final corrected candidate HEAD:** 21248f59e2f9f4f169619e86cf080fc84f7effc5
**Final corrected candidate blob:** ac83ff40c080913de29ba74c3b7423a8f858c2fd

## 1. Scope

B-ERD-01 formalizes a bounded future empirical discriminator for Dukascopy USATECHIDXUSD historical-tick representation.

No BI5 object was requested, downloaded or processed.

Preserved:

~~~text
B-PE-05 = NOT EXECUTED
C08-D4 = BLOCKED
C08-D5 = BLOCKED
BPE-C08 = BLOCKED
B global executable gate = BLOCKED
~~~

## 2. Qualified decision problem

The future bounded probe asks whether the current project premise:

~~~text
T_HOURLY =
"K1 legacy-hourly representation is empirically compatible
with every required bounded probe window"
~~~

survives predeclared USATECH probes.

Known alternatives remain diagnostic:

~~~text
K2 current daily tick candidate
coexistence
transition pattern
UNKNOWN_REPRESENTATION_EVIDENCED
KNOWN_CANDIDATES_INSUFFICIENT
~~~

No closed-world assumption exists.

## 3. Probe domain

Every probe uses exactly one governed H1 comparison window:

~~~text
W_probe = [market_h1_start_utc, market_h1_start_utc + 1 hour)
~~~

Qualified bounded anchors:

~~~text
PW = final H1 of mandatory 20-H1 warmup prefix
P0 = target-window start boundary
P1 = 2022 annual interior anchor
P2 = 2023 annual interior anchor
P3 = 2024 annual interior anchor
P4 = 2025 annual interior anchor
P5 = pre-2026-03-03 contextual anchor
P6 = post-2026-03-03 contextual anchor
P7 = target-window end boundary
~~~

P5/P6 do not assert that JETTA caused a BI5 transition.

Daily material is projected to the same W_probe before cross-family comparison.

## 4. Transport qualification

Future object requests require a sealed TransportPolicy before first request:

~~~text
method = GET
automatic_retry_count = 0
automatic_content_decoding = false
Accept-Encoding: identity
exact request headers persisted
redirect policy presealed
max redirect hops presealed
connect/read timeouts presealed
~~~

Raw response hash domain:

~~~text
SHA256(exact response body bytes exposed
with HTTP automatic content decoding disabled)
~~~

Any transport-policy change requires a new execution identity.

No failed capture is overwritten by a rerun.

## 5. Absence / refutation semantics

The contract distinguishes:

~~~text
FAMILY_OBSERVED
FAMILY_NOT_OBSERVED
FAMILY_REFUTED
FAMILY_TRANSPORT_BLOCKED
FAMILY_LOCATOR_BLOCKED
~~~

Critical rule:

~~~text
FAMILY_NOT_OBSERVED has zero refutation weight
~~~

A 404 is only an absence signal.

K1 can become REFUTED only from valid non-transport evidence contradicting a predeclared K1 prediction.

Transport ambiguity never refutes.

## 6. Open-world semantics

Unknown handling is split:

~~~text
UNKNOWN_REPRESENTATION_EVIDENCED
KNOWN_CANDIDATES_INSUFFICIENT
~~~

Positive unknown-family evidence requires observed provider evidence of an unregistered representation.

Known candidates merely absent/unusable:

~~~text
KNOWN_CANDIDATES_INSUFFICIENT
→ BLOCKED
~~~

No closest-format fallback exists.

## 7. Independent semantic diagnostics

Future semantic comparison requires at least two independently implemented diagnostic paths with:

~~~text
no shared decoded intermediate
no copied per-record interpretation output
separate parse/decompression path where feasible
separate result sealing
exact raw-input hash cross-binding
~~~

Agreement proves only:

~~~text
CANDIDATE_SEMANTIC_CONSISTENCY
~~~

not provider authority.

Disagreement blocks.

## 8. Cross-family comparison

For the same W_probe, future execution records at minimum:

~~~text
candidate occurrence counts
timestamp coverage
first/last candidate timestamps
timestamp multiplicity
strict duplicate multiplicity
overlap
K1-only observations
K2-only observations
matched-timestamp value disagreements
~~~

Possible probe relations:

~~~text
SEMANTICALLY_EQUIVALENT_ON_PROBE
STRICT_SUBSET
STRICT_SUPERSET
OVERLAP_WITH_DIVERGENCE
DISJOINT
COMPARISON_BLOCKED
~~~

No content deduplication.

## 9. Verdict semantics

Per candidate:

~~~text
SUPPORTED
REFUTED
NOT_OBSERVED
BLOCKED
~~~

Overall:

~~~text
PROBE_REFUTED
if any required probe has K1 = REFUTED on valid non-transport evidence

else BLOCKED
if any required probe is blocked or K1 remains merely NOT_OBSERVED

else PROBE_SUPPORTED
if every required probe has K1 = SUPPORTED

else BLOCKED
~~~

K2/coexistence/transition/unknown diagnostics remain persisted regardless of K1 verdict.

## 10. Anti-extrapolation

Hard invariant:

~~~text
PROBE_SUPPORTED
≠
FULL_INTERVAL_QUALIFIED
~~~

and:

~~~text
all bounded probes support K1
≠
K1 proven for every manifest-relevant interval
~~~

B-ERD bounded execution can never authorize full D.

## 11. Future full-D representation domain

Any later FULL_INTERVAL_QUALIFIED evidence used by D must cover:

~~~text
FULL_D_REPRESENTATION_DOMAIN =
mandatory deterministic 20-H1 warmup prefix
+
frozen evaluation interval
~~~

Eligible future complete-coverage methods are limited to:

~~~text
FI-1 exhaustive locator/membership enumeration
FI-2 qualified deterministic transition regimes/boundaries
FI-3 another separately adversarially qualified complete-coverage method
~~~

A bounded sample is never FI evidence.

## 12. Integrity

All structured artifacts inherit B-PE-01 canonical JSON and lowercase SHA-256 rules.

Sealed future artifacts include:

~~~text
LocatorManifest
ProbePlan
TransportPolicy
TransportCapture
ExecutionResult
~~~

Seal mismatch invalidates evidence.

## 13. Adversarial defects closed

Initial break:

~~~text
BERD01-F01 — PROBE_COMPARISON_WINDOW_NOT_NORMATIVELY_FIXED
BERD01-F02 — REPRESENTATION_ABSENCE / MARKET_ABSENCE / TRANSPORT_FAILURE NOT CLOSED
BERD01-F03 — HTTP METHOD / RETRY POLICY DEFERRED
BERD01-F04 — MULTI-HYPOTHESIS OVERALL PROBE_REFUTED IS AMBIGUOUS
BERD01-F05 — H_UNKNOWN TRIGGER OVERCLAIMS UNOBSERVABLE UNKNOWN FAMILY
BERD01-F06 — STRUCTURED SEAL CANONICALIZATION NOT BOUND
BERD01-F07 — FULL D WARMUP REPRESENTATION COVERAGE NOT EXPLICIT
~~~

Persisted-head residual break:

~~~text
BERD01-R01 — OVERALL TARGET PROPOSITION IS META-DISCRIMINATION, NOT THE PROJECT PREMISE
BERD01-R02 — HTTP BODY HASH DOMAIN / REQUEST POLICY NOT BYTE-DETERMINISTIC
~~~

All demonstrated defects are closed.

## 14. Final persisted-head re-break

Verified at persisted candidate blob ac83ff40c080913de29ba74c3b7423a8f858c2fd:

~~~text
V0.2 corrected contract identity = PASS
permission closure = PASS
B-PE-05 not executed = PASS
C08-D4/D5 remain BLOCKED = PASS
T_HOURLY exact = PASS
K1 refutation precedence = PASS
PT1H common comparison window = PASS
PW warmup probe = PASS
FULL_D_REPRESENTATION_DOMAIN = PASS
anti-extrapolation = PASS
UNKNOWN_REPRESENTATION_EVIDENCED split = PASS
KNOWN_CANDIDATES_INSUFFICIENT split = PASS
GET + zero retry = PASS
automatic content decoding disabled = PASS
Accept-Encoding identity = PASS
TransportPolicy sealing = PASS
raw response hash domain = PASS
FAMILY_NOT_OBSERVED zero refutation weight = PASS
K2 locator not fabricated = PASS
future execution authorization boundary = PASS
no backtest permission = PASS
~~~

No new defect was demonstrated.

## 15. Final verdict

~~~text
B-ERD-01 BOUNDED EMPIRICAL
REPRESENTATION-DISCRIMINATION CONTRACT = PASS
~~~

This PASS qualifies the experiment design only.

It does not mean:

~~~text
real BI5 downloaded
representation empirically supported
C08-D4/D5 PASS
B PASS
D materialized
backtest authorized
~~~

Current global state remains blocked.

## 16. Next possible governed action

~~~text
B-ERD-02 — bounded empirical representation-discrimination execution
~~~

This is a real-data boundary and requires explicit user authorization.

If authorized, it must begin with:

~~~text
fresh HEAD
→ read B-ERD-01 PASS
→ materialize and seal LocatorManifest
→ resolve and seal PW/P0-P7 ProbePlan
→ materialize and seal TransportPolicy
→ verify all pre-request hashes/seals
→ execute only presealed bounded GET probes
→ preserve exact TransportCaptures
→ run independent diagnostics
→ produce sealed ExecutionResult
→ PROBE_SUPPORTED / PROBE_REFUTED / BLOCKED
→ audit + backup + checkpoint
→ STOP
~~~

No full acquisition, D materialization or backtest is authorized inside B-ERD-02.
