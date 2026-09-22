# POST-B-PE-SEM-05R-01 BLOCKED AUTHORITY RECOVERY ESCALATION ROUTE SELECTION

Date: 2026-09-22

Repository: thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

Branch: integration/system-v1

Starting HEAD: 449d0243cf98bd5c46a1d3b9e15c7502ac4bf626

## 1. Authoritative starting state

B-PE-SEM-05R-01 is CLOSED / BLOCKED.

Package integrity is PASS.

Recovery results are frozen as:

A = AMBIGUOUS

B = NOT_FOUND

C = INCOMPLETE_VERSION_COVERAGE

Lane S re-adjudication sufficient new authority = NO.

Lane P authorization = NO.

This route-selection record performs no new documentary acquisition, no provider contact, and no market-data observation.

## 2. Exhausted channel that must not be recycled

The following provider distribution families were already exhausted within B-PE-SEM-05R-01 and must not be represented as a new evidence channel:

- DDS2-jClient-JForex
- JForex-API sources
- DDS2-Charts
- greed-common
- msg

The provider Maven/distribution archaeology recovered useful facts but did not recover the required exact authority.

Therefore repeating or merely widening the same dependency chain without a demonstrated new semantic lead is rejected.

## 3. Authority state A

Target:

exact immutable/provider-versioned legacy-hourly K1 semantic authority.

Current state:

AMBIGUOUS.

Recovered provider facts:
- BI5 is an official provider cache/version identity;
- provider code recognizes _ticks.bi5;
- selected provider cache classes are stable across inspected versions.

Still absent:
- exact legacy-hourly raw payload layout authority;
- exact timestamp-origin authority;
- exact field-role authority;
- exact price/volume primitive authority.

Classification:

PUBLIC DISTRIBUTION CHANNEL INSUFFICIENT.

Remaining credible channel:

DIRECT PROVIDER PRIMARY CLARIFICATION.

Reason:
the missing fact is not generic decoding plausibility; it is an exact provider-owned semantic statement about a legacy representation. A direct provider technical clarification can in principle supply this without relaxing the authority standard.

A is NOT yet declared externally unprovable.

## 4. Authority state B

Target:

exact provider-primary native BI5 USATECH raw scale/divisor authority.

Current state:

NOT_FOUND.

Recovered provider facts:
- USATECHIDXUSD provider identity exists;
- API/runtime price-scale structures exist;
- provider artifacts expose priceScale / pricePipValue related schemas.

Still absent:
- exact binding from USATECH native BI5 raw integer representation to divisor / scale.

Classification:

PUBLIC DISTRIBUTION CHANNEL INSUFFICIENT.

Remaining credible channel:

DIRECT PROVIDER PRIMARY CLARIFICATION.

A provider answer may establish:
- the exact native raw price divisor;
- whether it is instrument-specific;
- whether it changed across the governed target interval;
- the authoritative source/version where the rule is defined.

B is NOT yet declared externally unprovable.

## 5. Authority state C

Target:

exhaustive target-epoch semantic change-point / continuity authority.

Current state:

INCOMPLETE_VERSION_COVERAGE.

Recovered:
- partial 2021-2025 client/cache/history/tick stability;
- exact provider version identities;
- exact unresolved JETTA event on 2026-03-03.

Still absent:
- public provider distribution coverage through 2026-08-14;
- server/public raw-object semantic continuity authority;
- JETTA effect on K1;
- exact legacy-hourly to current-daily transition boundary.

Classification:

PUBLIC DISTRIBUTION CHANNEL INSUFFICIENT.

Remaining credible channel:

DIRECT PROVIDER PRIMARY CLARIFICATION.

C has the highest residual risk of ultimately remaining externally unprovable.

A provider response must not be assumed sufficient merely because it exists. It must explicitly address target-scope continuity or identify exact change points / authoritative records.

## 6. Routes compared

### Route 1 — another broad provider-owned archived/versioned documentation search

Decision:

NOT SELECTED.

Reason:
no specific uninspected provider-owned archive or versioned documentary collection is currently identified by the governed evidence as likely to contain the missing A/B/C semantics.

Opening a broad search would be unbounded and would risk repeating the same mutable-document problem already encountered.

If a provider response later identifies an exact archive, specification, historical manual or release artifact, that newly identified source may be separately governed.

### Route 2 — direct provider contact/support inquiry without pre-contact contract

Decision:

REJECTED.

Reason:
sending questions before freezing the exact claims, wording, scope, response-admissibility rules and evidence-preservation requirements would allow post-response reinterpretation and confirmation bias.

### Route 3 — direct provider contact/support inquiry preceded by a frozen inquiry contract

Decision:

SELECTED.

Reason:
this is the smallest remaining evidence channel capable in principle of resolving A, B and C while preserving provider-primary authority and avoiding any market-data observation.

### Route 4 — SIMPLIFY authority requirements

Decision:

REJECTED AT THIS STAGE.

Reason:
the existing authority contract has not yet been shown impossible to satisfy. A direct provider-primary clarification route remains credible.

Any future simplification must occur through a separate contract-review block, not by weakening the current evidence criteria in-place.

### Route 5 — STOP and classify authority externally unprovable

Decision:

REJECTED AS PREMATURE.

Reason:
the direct provider-primary clarification channel remains unused.

If a bounded provider inquiry fails, receives no authoritative answer, or produces an inadmissible/ambiguous answer, STOP or SIMPLIFY may become justified in a later route decision.

## 7. Decision

Decision:

CONTINUE.

Selected evidence channel:

DIRECT PROVIDER PRIMARY TECHNICAL CLARIFICATION.

No contact is made by this route-selection record.

Exactly one next bounded block is selected:

B-PE-SEM-05R-02 —
PROVIDER PRIMARY AUTHORITY INQUIRY CONTRACT
PRE-CONTACT FORMALIZATION ONLY

## 8. Purpose of B-PE-SEM-05R-02

B-PE-SEM-05R-02 must freeze the inquiry before any provider contact.

It must define:

- exact provider contact channel class permitted;
- exact identity requirements for the responder;
- exact question set for A;
- exact question set for B;
- exact question set for C;
- exact question on the 2026-03-03 JETTA change;
- target interval;
- representation identity K1;
- instrument identity USATECHIDXUSD;
- forbidden leading assumptions;
- acceptable response forms;
- inadmissible response forms;
- provenance preservation;
- immutable capture/sealing procedure;
- contradiction-handling rule;
- partial-answer rule;
- no-response rule;
- reopen rule;
- PASS / FAIL / BLOCKED interpretation for the later inquiry-consumer block.

B-PE-SEM-05R-02 is contract/formalization only.

It must NOT contact Dukascopy.

## 9. Required inquiry content

The frozen inquiry must separate A/B/C and must not combine them into one vague question.

### A — legacy-hourly K1 semantics

The inquiry contract must require exact questions covering, where provider knowledge permits:
- whether historical hourly tick BI5 payloads use LZMA and which wrapper/framing;
- exact decompressed record width;
- exact byte order;
- exact field sequence and primitive types;
- exact meaning/unit/origin of the timestamp field;
- exact ask/bid role;
- exact ask-volume/bid-volume role and primitive encoding;
- applicability dates/version boundaries;
- whether these semantics changed during 2021-08-13 through 2026-08-14.

The inquiry must not assert these answers as facts in the question.

### B — USATECH raw scale/divisor

The inquiry contract must require:
- exact mapping from native BI5 raw ask/bid integers for USATECHIDXUSD to market price;
- exact divisor/multiplier;
- whether this mapping differs by period;
- authoritative metadata/specification/source identifying the rule;
- distinction between native raw BI5 scale and API/display pip/tick/point values.

The inquiry must explicitly avoid suggesting /1000 as the expected answer.

### C — continuity / change points

The inquiry contract must require:
- whether legacy-hourly raw BI5 semantics changed anywhere in the target interval;
- exact effective date/version of every material semantic change;
- exact date and semantic meaning of any legacy-hourly to daily-object transition;
- whether server-side/public raw-object semantics differed from client-cache semantics;
- whether JETTA changed raw K1 payload semantics or only retrieval/backend behavior;
- exact authoritative references if available.

No silence or absence of documented change may be interpreted as continuity.

## 10. Response admissibility requirements

A later inquiry-consumer block may use a response as provider-primary evidence only if the frozen contract's provenance requirements are satisfied.

At minimum the contract must require:
- provider-owned communication channel or independently verifiable Dukascopy identity;
- sender/responder identity or official support identity;
- exact timestamp;
- exact complete response bytes/text as received;
- exact question text sent;
- conversation/thread/ticket identity where available;
- cryptographic hash of captured evidence;
- no semantic editing of the provider response;
- explicit separation between provider statement and project interpretation.

Anonymous community responses are not provider-primary authority.

A response from a provider employee/support identity may still be BLOCKED if the responder disclaims knowledge, speculates, or cannot bind the statement to the target representation/period.

## 11. Later inquiry outcome rules

B-PE-SEM-05R-02 itself cannot recover A/B/C.

A later separately opened inquiry-consumer block will classify each answer independently.

Possible dispositions:

RECOVERED_PROVIDER_PRIMARY

PARTIALLY_RECOVERED

AMBIGUOUS

NOT_ANSWERED

PROVIDER_CANNOT_CONFIRM

CONTRADICTED

INADMISSIBLE

BLOCKED

No-response is not evidence of absence or continuity.

A provider answer cannot self-authorize Lane P.

Recovered evidence, if any, must return through a later governed Lane S re-adjudication.

## 12. Current prohibition boundary

This route-selection record authorizes no contact.

Until B-PE-SEM-05R-02 is separately opened:

provider contact = NOT AUTHORIZED

provider inquiry sending = NOT AUTHORIZED

new documentary acquisition = NOT AUTHORIZED

provider BI5 GET = NOT AUTHORIZED

historical market-data object acquisition = NOT AUTHORIZED

Lane S re-adjudication = NOT AUTHORIZED

Lane P RequestManifest = NOT AUTHORIZED

P-DIAG implementation = NOT AUTHORIZED

physical semantic discrimination = NOT AUTHORIZED

B-PE-SEM-06 = NOT AUTHORIZED

B-FIQ-02R = NOT AUTHORIZED

FULL_INTERVAL = NOT AUTHORIZED

D materialization = NOT AUTHORIZED

backtest = NOT AUTHORIZED

paper/broker/live = NOT AUTHORIZED

## 13. Final route decision

POST-B-PE-SEM-05R-01 BLOCKED AUTHORITY RECOVERY ESCALATION ROUTE SELECTION = PASS

Decision = CONTINUE

Preserved:

A = AMBIGUOUS

B = NOT_FOUND

C = INCOMPLETE_VERSION_COVERAGE

Selected evidence channel:

DIRECT PROVIDER PRIMARY TECHNICAL CLARIFICATION

Selected immediate successor:

B-PE-SEM-05R-02 —
PROVIDER PRIMARY AUTHORITY INQUIRY CONTRACT
PRE-CONTACT FORMALIZATION ONLY

No provider contact occurred.

No new documentary evidence was acquired.

STOP.
