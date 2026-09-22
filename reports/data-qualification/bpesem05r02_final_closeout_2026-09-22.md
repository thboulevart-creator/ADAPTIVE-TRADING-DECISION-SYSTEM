# B-PE-SEM-05R-02 — FINAL CLOSEOUT

Date: 2026-09-22

Repository: thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

Branch: integration/system-v1

## 1. Closed block

B-PE-SEM-05R-02 —
PROVIDER PRIMARY AUTHORITY INQUIRY CONTRACT
PRE-CONTACT FORMALIZATION ONLY

Final governed result:

package integrity = PASS

inquiry contract qualification = PASS

A preserved = AMBIGUOUS

B preserved = NOT_FOUND

C preserved = INCOMPLETE_VERSION_COVERAGE

provider contact authorized = NO

provider contact performed = NO

provider inquiry sent = NO

Lane S authority effect = NONE

Lane P authority effect = NONE

B-PE-SEM-05R-02 = CLOSED / PASS

demonstrated final defects = 0

## 2. Starting authority

Starting checkpoint:

cecfe1e409a0e0ccd85be5e50c1d31b51a78c0b8

checkpoint: select B-PE-SEM-05R-02 provider inquiry contract

Recovery state preserved from B-PE-SEM-05R-01:

A = AMBIGUOUS

B = NOT_FOUND

C = INCOMPLETE_VERSION_COVERAGE

Recovery qualification input:

evidence/bpesem05r01/recovery_qualification_v0_1.json

blob =
cd260eb27ac31c0fc68dea4449923ac484544307

qualification seal =
7ecc77a75c4bcf333edce03ec2a6504a8f0ded39fc49789d0556d7bd54f3866a

Escalation route input:

reports/data-qualification/
post_bpesem05r01_blocked_authority_recovery_escalation_route_selection_2026-09-22.md

blob =
6a3afce89da39638e1960a9a57a66eb1a8fb2bf4

## 3. Qualified inquiry contract

Artifact:

evidence/bpesem05r02/
provider_primary_authority_inquiry_contract_v0_1.json

blob =
3eeb079b834102a2c8983563bd21088ad50796ed

contract seal =
39b3cd8ad0c3bd68a3326f31ec2e27ae1cd7d34d6d1fb0c9eebe9b49c2e1f0a2

Target binding:

provider =
Dukascopy Bank SA

representation =
K1 / historical hourly tick .bi5 legacy family

instrument =
USATECHIDXUSD / USATECH.IDX/USD

target interval =
2021-08-13T01:00:00Z
→
2026-08-14T20:00:00Z

## 4. Contact-channel policy

Permitted future channel classes are limited to:
- official Dukascopy support/contact channel on a provider-controlled domain;
- email where provider identity is independently verifiable on a Dukascopy-controlled domain;
- provider-owned support/forum channel only when the responder is independently verifiable as official Dukascopy staff/support.

Forbidden as provider-primary:
- anonymous community response;
- third-party forum/social response;
- unverified personal email;
- LLM/search summary;
- project-authored interpretation without provider statement.

This contract authorizes no contact by itself.

## 5. Responder identity policy

Provider-primary use requires:
- provider-owned channel or independently verifiable Dukascopy identity;
- responder/support identity or official role where supplied;
- sender/account identity where available;
- thread/ticket/message identity where available;
- exact response timestamp.

Partial or unresolved identity remains BLOCKED for provider-primary authority.

## 6. Frozen questions

Question groups:

A = 7 questions

B = 3 questions

C = 3 questions

JETTA = 2 questions

A asks independently for:
- compression/container framing;
- record sizing/delimitation;
- byte order / field sequence / primitive types;
- timestamp meaning/unit/origin/time basis;
- ask/bid roles;
- volume roles/primitive representation;
- changes across the target interval.

B asks independently for:
- exact native stored-price transformation for USATECH.IDX/USD;
- period/version applicability;
- provider-owned authoritative source for the transformation.

The B questions do NOT mention:
- 1000;
- /1000;
- decimalFactor=1000;
- a proposed raw divisor.

C asks independently for:
- all semantic changes across the target interval;
- any legacy-hourly to daily-object transition;
- client-cache versus server/public raw-object semantic equivalence or differences.

JETTA asks independently whether the 2026-03-03 historical-data retrieval change altered raw payload semantics or only retrieval/backend behavior, without presuming either outcome.

## 7. Non-leading firewall

The contract forbids priming the provider with:
- third-party decoder agreement;
- empirical plausibility;
- project-decoder expectations;
- proposed /1000 scale;
- assumed continuity from stable client code;
- assumed JETTA change or non-change.

Separate A/B/C/JETTA questions must not be collapsed into one confirmation bundle.

## 8. Response preservation

A later consumer must capture:
- exact question text sent;
- exact complete provider response;
- original attachments where available;
- provider channel identity;
- responder/sender identity;
- ticket/thread/message identity where available;
- sent and received timestamps;
- provider-supplied references.

Required sealing:
- SHA-256 per raw message/export/attachment;
- SHA-256 canonical manifest binding questions, responses and metadata.

Raw provider evidence must remain unchanged.

Normalized extracts must be separately identified derived artifacts.

Provider caveats, uncertainty and scope limitations must not be removed.

## 9. Admissibility

Provider-primary evidence requires:
- verified provider identity;
- exact target representation/scope or explicit different scope;
- sufficiently explicit factual statement;
- preserved and sealed raw provenance.

Blocking/inadmissible conditions include:
- anonymous/unverified responder;
- speculative support language;
- current-daily-only answer where legacy-hourly remains unresolved;
- example-value/market-plausibility reasoning;
- missing applicability period where material;
- provider inability to confirm.

A provider-cited specification/artifact is a new evidence lead, not automatically an independently verified source. It requires a later governed acquisition/sealing block.

## 10. Later outcome taxonomy

Per-question statuses are frozen as:

RECOVERED_PROVIDER_PRIMARY

PARTIALLY_RECOVERED

AMBIGUOUS

NOT_ANSWERED

PROVIDER_CANNOT_CONFIRM

CONTRADICTED

INADMISSIBLE

BLOCKED

No response has zero positive authority.

Partial answers preserve answered subquestions only.

Required unanswered/ambiguous subquestions remain BLOCKED.

Material contradictions require a later adjudication/reopen block.

A future provider answer cannot directly authorize Lane P.

Recovered evidence must return through separately governed Lane S re-adjudication.

## 11. Retry and mutation rules

Initial contact count:

1

Automatic retry:

NO

Any later retry requires a new governed decision.

Question mutation after send:

FORBIDDEN within the same contract version.

A new question version requires a new governed contract version.

## 12. Candidate / adversarial break

Candidate commit:

c5c39707c07ca60b0fb6a7475ab3d0426d6e45a7

Candidate report:

reports/data-qualification/
bpesem05r02_inquiry_contract_candidate_2026-09-22.md

blob =
4c4115556bdf513f87d2d7c4633841ac51c472b5

Adversarial break workflow:

B-PE-SEM-05R-02 inquiry contract

run =
35763230539

job =
106866219537

Adversarial break report:

reports/data-qualification/
bpesem05r02_inquiry_contract_adversarial_break_2026-09-22.md

blob =
94d190231d46f5849a106efdae908ed4f7d1c471

Result:

breaker verdict = PASS

attack count = 36

demonstrated defects = 0

No candidate correction was justified.

## 13. Final persisted-head re-break

Workflow:

B-PE-SEM-05R-02 final rebreak

run =
35763432564

job =
106866875065

Final output commit:

ce0586499b6dec1db976f30fec00b222ad541c62

Qualification artifact:

evidence/bpesem05r02/
inquiry_contract_qualification_v0_1.json

blob =
87971297e47bfe78e030dadf0a61c03e94b4957a

qualification seal =
2501061249854339f3bfb8b7ec1acb15f6dc9701c14f17f306e5d04d8d7e162a

Final report:

reports/data-qualification/
bpesem05r02_final_persisted_head_rebreak_2026-09-22.md

blob =
b05721240d8cf6556aec3b7e2c3ca291fb0fb7f9

Final checks:

candidate ancestor = PASS

breaker verdict = PASS

breaker attacks = 36

breaker defects = 0

post-candidate changed paths = 3

unresolved changed paths = 0

package integrity = PASS

contract qualification = PASS

demonstrated final defects = 0

## 14. Execution boundary

During B-PE-SEM-05R-02:

provider contact = NO

provider inquiry sending = NO

new documentary acquisition = NO

provider BI5 GET = NO

historical market-data object acquisition = NO

Lane S re-adjudication = NO

Lane P RequestManifest = NO

P-DIAG implementation = NO

physical semantic discrimination = NO

B-PE-SEM-06 = NO

B-FIQ-02R = NO

FULL_INTERVAL = NO

D materialization = NO

backtest = NO

paper/broker/live = NO

## 15. Closure

B-PE-SEM-05R-02 = CLOSED / PASS

The pre-contact inquiry contract is qualified.

A/B/C remain unchanged.

Provider contact remains NOT AUTHORIZED until a separate governed consumer-route decision selects the exact contact execution path.

STOP.
