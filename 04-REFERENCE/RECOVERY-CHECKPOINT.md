# RECOVERY CHECKPOINT — ALGO ECOSYSTEM

> Current governed recovery state for `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`.
>
> GitHub is the source of truth. If the repository disagrees with this checkpoint, stop and diagnose the discrepancy before mutation.

## 1. Current workstream

Repository:

`thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch:

`integration/system-v1`

End-of-day session backup:

`99-BACKUP/SESSION-2026-09-18-P1.9-P1.14-QUALIFICATION-CHAIN.md`

Backup commit:

`06a1b383a3b0279daf44a5f59e5daa48a35c6946`

Technical common-HEAD immediately before backup/checkpoint persistence:

`3046293373c41de101008bea8f1f861b1db9081d`

Always verify the live branch HEAD before writing. The checkpoint/backup commits are documentary descendants of that technical state.

Current block:

`P1.16 — QUALIFIED EXPERIMENTAL FINDING INTERPRETATION POLICY`

---

## 2. Governing method

Required progression:

```text
UNDERSTAND → COMPARE → BREAK → DECIDE
```

Then:

```text
formalisation → candidate → adversarial break → correction → re-break → verdict
```

Allowed verdicts:

`PASS / FAIL / BLOCKED`

Never declare PASS without persisted-HEAD final re-break.

Do not reconstruct state from conversation if GitHub is available.

---

## 3. Global safety truth

The following remain unchanged:

- no native `.bi5` acquisition is authorized;
- no real-data acquisition is authorized by this workstream;
- no real backtest is authorized;
- no broker/live activation is authorized;
- P1.1 positive `AUTHORIZED` remains separately BLOCKED;
- request/evidence/experiment objects do not imply operational authorization.

The separation remains:

```text
request ≠ evidence ≠ execution ≠ authorization
```

---

## 4. Qualified chain

Protected/qualified chain at this checkpoint:

- P0.2: PASS / protected baseline
- P0.3: PASS / protected baseline
- P0.4: PASS / protected baseline
- P0.5: PASS / protected baseline
- P0.6: PASS / protected reproducibility envelope
- P1.0: qualified fail-closed promotion boundary
- P1.1: PASS block-only; positive authorization remains BLOCKED
- P1.2: PASS — qualification-only
- P1.3: PASS — qualification-only
- P1.4: PASS — qualification-only
- P1.5: PASS
- P1.6: PASS
- P1.7: PASS
- P1.8: PASS
- P1.9A: PASS
- P1.9B: PASS
- P1.10A: PASS
- P1.10B: PASS
- P1.11A: PASS
- P1.11B: PASS
- P1.12A: PASS
- P1.12B: PASS
- P1.13A: PASS
- P1.13B: PASS

Latest fully qualified persisted HEAD:

`51abe3cc3f556384b9ab3d89d79a375f8b7e8245`

---

## 5. P1.12 qualified state

### P1.12A

Contract:

`P1_12A_DECLARED_EVIDENCE_CRITERIA_ASSESSMENT_BOUNDARY_V1`

Runtime:

`src/declared_evidence_criteria_assessment.py`

Final breaker blob:

`55a9f445e79e84fac25f2224468bd9d1f8f308ea`

### P1.12B

Contract:

`P1_12B_LINKED_EXPERIMENT_EXECUTION_BOUNDARY_V1`

Runtime:

`src/linked_experiment_execution.py`

Corrected breaker blob:

`a226fd1aac9a3472682386ab9f3d6eb3d23feeba`

The correction fixed only a generator-fixture lifetime defect retaining the upstream QEI.

Final P1.12 persisted HEAD:

`96c76e99c0cb961ecba384ec0a8dc87b666a84b1`

Final runs:

- P1.12A run `35382685934`, job `105722329058`;
- P1.12B run `35382686019`, job `105722338874`.

Final counts:

- P1.12A: `33 passed`;
- P1.12B: `18 passed`;
- protected chain: PASS;
- clean worktrees.

---

## 6. P1.13 qualified state

### P1.13A

Contract:

`P1_13A_EVIDENCE_SEMANTIC_COMPLETENESS_REVIEW_SUBMISSION_BOUNDARY_V1`

Runtime:

`src/evidence_semantic_completeness_review.py`

Runtime blob:

`d22f7964223810623fa2bca927a253359aad17c6`

Final breaker blob:

`840be30d17a31c8da8c8c57bc8902073de462b58`

Always:

```text
review_authority_status = BLOCKED
request_fulfillment_status = BLOCKED
```

### P1.13B

Contract:

`P1_13B_EXPERIMENT_EVALUATION_SUBMISSION_BOUNDARY_V1`

Runtime:

`src/experiment_evaluation_submission.py`

Runtime blob:

`968ef47d0fc4e066374b7471110c71d0eaf28865`

Final breaker blob:

`aea742767512c0f318744ab8eeade6f4155c2840`

The final breaker helper uses a sentinel so explicit `None` reaches the runtime rather than being replaced by the omitted-argument default.

Always:

```text
measurement_provenance_status = BLOCKED
evaluation_authority_status = BLOCKED
```

Final P1.13 persisted HEAD:

`51abe3cc3f556384b9ab3d89d79a375f8b7e8245`

Final runs:

- P1.13A run `35385571278`, job `105731567958`;
- P1.13B run `35385571355`, job `105731568441`.

Final counts:

- P1.13A: `43 passed`;
- P1.13B: `49 passed`;
- protected chain: PASS;
- clean worktrees.

---

## 7. P1.14 selected contracts

### P1.14A

Contract:

`P1_14A_REVIEWER_METHOD_AUTHORITY_REATTESTATION_BOUNDARY_V1`

Selected model:

`P1_14A_MINIMAL_REVIEWER_METHOD_AUTHORITY_REATTESTATION_MODEL_V1`

Runtime:

`src/reviewer_method_authority.py`

Runtime blob:

`d56374ab05b07b8a05eafbbba9dde2875ef4f507`

Breaker:

`breakers/p1_14a_reviewer_method_authority_breaker.py`

Current breaker blob:

`f63f24cee1667839edd457f4bd76632fba063544`

Meaning of positive output:

```text
review_authority_status = PASS
request_fulfillment_status = BLOCKED
```

PASS authority means only an externally pinned authority attests the exact reviewer/method/review binding.

It does not mean semantic truth or request fulfillment.

### P1.14B

Contract:

`P1_14B_WITNESSED_MEASUREMENT_PROVENANCE_REATTESTATION_BOUNDARY_V1`

Selected model:

`P1_14B_MINIMAL_WITNESSED_MEASUREMENT_PROVENANCE_MODEL_V1`

Runtime:

`src/experiment_measurement_provenance.py`

Runtime blob:

`4ce8ceb7e46ac2f6ffbd97560225d559ea7757f5`

Breaker:

`breakers/p1_14b_measurement_provenance_breaker.py`

Breaker blob:

`24d8dcd980ec421c75207930174a42cbd62a3b46`

Meaning of positive output:

```text
measurement_provenance_status = PASS
evaluation_authority_status = BLOCKED
finding_status = BLOCKED
```

PASS provenance proves externally witnessed lineage to the exact execution stream and hashed procedures, not mathematical correctness or finding truth.

---

## 8. P1.14 test-first baseline

P1.14A preimplementation:

- run `35386382173`;
- job `105734173160`;
- protected chain through P1.13A+B: PASS;
- P1.13A+B: `92 passed`;
- P1.14A: `34 errors`;
- every error due only to absent `src/reviewer_method_authority`;
- clean worktree.

P1.14B preimplementation:

- run `35386416259`;
- job `105734283344`;
- protected chain through P1.13A+B: PASS;
- P1.13A+B: `92 passed`;
- P1.14B: `38 errors`;
- every error due only to absent `src/experiment_measurement_provenance`;
- clean worktree.

This is valid test-first red evidence.

---

## 9. P1.14 postimplementation common-HEAD re-break

Technical common HEAD:

`3046293373c41de101008bea8f1f861b1db9081d`

### P1.14B

Run:

`35387213254`

Job:

`105736808596`

Result:

- protected chain through P1.13A+B: PASS;
- P1.14B: `38 passed`;
- clean worktree: PASS.

Current verdict:

`PASS CANDIDATE`

Not final because P1.14 global common HEAD is not yet green.

### P1.14A

Run:

`35387213271`

Job:

`105736808586`

Result:

- protected chain through P1.13A+B: PASS;
- P1.14A: `33 passed, 1 failed`;
- clean worktree: PASS.

Sole failure:

`test_c1_external_pin_exact_sha256[None]`

Exact root cause is in the breaker helper:

```python
def _reattest(review, paths, *, authority_id=REVIEW_AUTHORITY, pin=None):
    record_path, receipt_path, receipt_sha256 = paths
    return _p114a().reattest_reviewer_method_authority(
        review,
        record_path,
        receipt_path,
        expected_authority_id=authority_id,
        expected_receipt_sha256=receipt_sha256 if pin is None else pin,
    )
```

The parametrized attack explicitly passes `None`, but the helper replaces it with the valid receipt pin.

Therefore explicit `None` never reaches the runtime.

This is a demonstrated breaker-helper defect, not a demonstrated runtime defect.

Do not modify the runtime to inspect tests/stacks or otherwise fake rejection.

---

## 10. Current verdict

```text
P1.14A
BLOCKED — breaker helper masks explicit None

P1.14B
PASS CANDIDATE

P1.14 GLOBAL QUALIFICATION
BLOCKED
```

No P1.14 qualification candidate has been persisted.

No final P1.14 PASS exists.

---

## 11. Mandatory semantic separations

```text
ReviewerMethodAuthorityQualification
≠ semantic truth
≠ request fulfillment
≠ knowledge
≠ operational authorization
```

```text
WitnessedMeasurementProvenance
≠ measurement correctness
≠ evaluator authority
≠ qualified experimental finding
≠ ResearchRunEvidence
≠ evidence
≠ knowledge
≠ operational authorization
```

Also:

```text
qualified reviewer authority
≠ request fulfillment

witnessed measurement provenance
≠ qualified experimental finding
```

Future promotion boundaries must remain explicit.

---

## 12. Mandatory recovery order

Read in this order:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this `04-REFERENCE/RECOVERY-CHECKPOINT.md`
3. `99-BACKUP/SESSION-2026-09-18-P1.9-P1.14-QUALIFICATION-CHAIN.md`
4. `GOVERNANCE/STEP-3-REAL-SYSTEM-MAPPING.md`
5. `breakers/p1_14a_reviewer_method_authority_breaker.py`
6. `.github/workflows/p1-14a-reviewer-method-authority.yml`
7. `src/reviewer_method_authority.py`
8. `breakers/p1_14b_measurement_provenance_breaker.py`
9. `.github/workflows/p1-14b-measurement-provenance.yml`
10. `src/experiment_measurement_provenance.py`
11. verify real `integration/system-v1` HEAD and compare with this checkpoint before mutation.

GitHub wins if there is any discrepancy.

---

## 13. Do not repeat / do not do

- Do not re-formalize P1.9–P1.14.
- Do not reimplement P1.14 runtimes.
- Do not modify P1.14B.
- Do not fake a P1.14A runtime fix for the explicit-None failure.
- Do not remove `None` from the P1.14A attack.
- Do not weaken the P1.14A assertion.
- Do not alter the other 33 P1.14A attacks.
- Do not jump directly to a qualification commit before a new common-HEAD A+B re-break.
- Do not infer fulfillment or finding from P1.14.
- Do not authorize real acquisition/backtest/live execution.

---

## 14. Exactly one next governed action

**Correct only the demonstrated P1.14A breaker helper ambiguity so explicit `None` reaches `reattest_reviewer_method_authority()`, without changing either runtime, without removing `None`, without weakening the assertion, and without changing the other 33 attacks.**

Use an omitted-argument sentinel, e.g.:

```python
_DEFAULT_PIN = object()

def _reattest(..., pin=_DEFAULT_PIN):
    ...
    expected_receipt_sha256=(
        receipt_sha256 if pin is _DEFAULT_PIN else pin
    )
```

Then:

1. update only the P1.14A workflow breaker hash lock;
2. run targeted P1.14A re-break;
3. require P1.14A `34/34 PASS`;
4. persist the breaker correction in governance;
5. use that governance commit as a common HEAD for P1.14A+B;
6. require A and B both green on that exact common HEAD;
7. persist P1.14 qualification candidate;
8. re-break A and B on that exact persisted qualification HEAD;
9. verify branch identity, breaker blobs, runtime blobs and clean worktrees;
10. only then issue final PASS / FAIL / BLOCKED.

---

## 15. Probable next work after P1.14 final qualification

Only after P1.14 is final PASS:

### Evidence branch

Design an explicit boundary for:

```text
qualified reviewer authority
→ request fulfillment decision
```

without equating reviewer authority with fulfillment automatically.

### Experiment branch

Design an explicit boundary for:

```text
witnessed measurement provenance
→ qualified experimental finding
```

which must separately address evaluator authority and/or procedure correctness before creating any finding.

Do not implement these promotion boundaries before P1.14 closes.

---

## 16. End-of-day stop rule

Stop here for 18 September 2026.

Do not correct the P1.14A breaker tonight after this checkpoint save.

Tomorrow resume from GitHub, this checkpoint, and the dated backup — not from conversational memory.


---

## 17. P1.14 final qualification closure

P1.14 is now fully qualified.

Qualified persisted HEAD:

`bbd4e382f5ce744438079015eb11826aff64be74`

Final P1.14A:

- run `35429884389`;
- job `105862447839`;
- `34 passed`;
- clean worktree.

Final P1.14B:

- run `35429884347`;
- job `105862447690`;
- `38 passed`;
- clean worktree.

Final identities:

- P1.14A breaker `ff8de568b3ed8b1e887b604a8db9d173bdbbd66b`;
- P1.14B breaker `24d8dcd980ec421c75207930174a42cbd62a3b46`;
- P1.14A runtime `d56374ab05b07b8a05eafbbba9dde2875ef4f507`;
- P1.14B runtime `4ce8ceb7e46ac2f6ffbd97560225d559ea7757f5`.

Verdict:

```text
P1.14A PASS
P1.14B PASS
```

---

## 18. P1.15 conceptual formalisation state

Governance formalisation commit:

`483227c09ad10e8be11f95b609a6420443a11b34`

No P1.15 runtime exists.

No P1.15 executable breaker exists.

### P1.15A selected minimal boundary

Contract candidate:

`P1_15A_EVIDENCE_REQUEST_FULFILLMENT_DECISION_BOUNDARY_V1`

Purpose:

```text
exact ReviewerMethodAuthorityQualification
→ explicit EvidenceRequestFulfillmentDecision
```

Deterministic promotion:

```text
review_verdict PASS    → request_fulfillment_status PASS
review_verdict FAIL    → request_fulfillment_status FAIL
review_verdict BLOCKED → request_fulfillment_status BLOCKED
```

Only an exact P1.14A authority qualification is admissible.

Fulfillment does not mean knowledge or operational authorization.

### P1.15B selected minimal boundary

Contract candidate:

`P1_15B_EXPERIMENT_EVALUATOR_METHOD_AUTHORITY_REATTESTATION_BOUNDARY_V1`

Purpose:

```text
exact ExperimentEvaluationSubmission
+
exact WitnessedMeasurementProvenance
+
external evaluator/method/procedure authority
→ QualifiedExperimentEvaluationAuthority
```

Expected positive status:

```text
evaluation_authority_status = PASS
finding_status = BLOCKED
```

P1.15B does NOT create a finding.

The actual experimental finding promotion is deferred because a governed mapping from:

- prediction status;
- falsification status;
- qualified evaluation authority;
- witnessed measurements;

to:

- SUPPORTED;
- REFUTED;
- NOT_INTERPRETABLE;

still needs its own explicit policy boundary.

---

## 19. P1.15 conceptual break verdicts

### P1.15A naive promotion

```text
ReviewerMethodAuthorityQualification
→ implicit fulfillment
```

Verdict:

`FAIL`

Reason:

reviewer authority is necessary but cannot silently mutate request-level state. An explicit promotion gate is required.

### P1.15B naive promotion

```text
WitnessedMeasurementProvenance
→ qualified experimental finding
```

Verdict:

`FAIL`

Reasons:

- provenance is not evaluator authority;
- provenance is not method authority;
- procedure hashes are identity, not correctness;
- P1.14B lacks complete finding interpretation policy;
- current `ResearchFindings` structural factory does not prove this authority chain.

---

## 20. Exactly one next governed action

Create only the P1.15 test-first executable breakers and their workflows, with no P1.15 runtime implementation yet:

- `breakers/p1_15a_evidence_request_fulfillment_breaker.py`;
- `.github/workflows/p1-15a-evidence-request-fulfillment.yml`;
- `breakers/p1_15b_experiment_evaluator_authority_breaker.py`;
- `.github/workflows/p1-15b-experiment-evaluator-authority.yml`.

The breakers must encode the conceptual attack sets already frozen in governance.

Then run pre-implementation qualification and require:

- protected chain through P1.14A+B PASS;
- P1.15A FAIL only because its runtime candidate is absent;
- P1.15B FAIL only because its runtime candidate is absent;
- clean worktrees.

Do not implement either P1.15 runtime before those expected red baselines exist.



---

## 21. P1.15 final qualification closure

P1.15 is fully qualified.

Qualified persisted HEAD:

`e61381813c0539c1339aec6e01310d4046f9dbe3`

Final P1.15A:

- run `35433285721`;
- job `105871556471`;
- `19 passed`;
- clean worktree.

Final P1.15B:

- run `35433285730`;
- job `105871556484`;
- `38 passed`;
- clean worktree.

Final identities:

- P1.15A breaker `bc057806d1a31072258caafb26a3e4c6de8d7448`;
- P1.15B breaker `b077c7e81e60066aed712f8c9212378e3b08916c`;
- P1.15A runtime `a13ec4b3a5ceb44266b214e69c4e596519966050`;
- P1.15B runtime `bfab3c421263434d5e3e3066720f95abb521b09c`.

Verdict:

```text
P1.15A PASS
P1.15B PASS
```

---

## 22. P1.16 selected experimental finding policy

Governance formalisation commit:

`00061b577c5f4212000b9343cbe35bd6781128bb`

Contract candidate:

`P1_16_QUALIFIED_EXPERIMENTAL_FINDING_INTERPRETATION_BOUNDARY_V1`

Policy constant candidate:

`P1_16_FINDING_INTERPRETATION_POLICY_V1`

Future runtime:

`src/qualified_experimental_finding.py`

No P1.16 runtime exists yet.

No P1.16 executable breaker exists yet.

### Total interpretation table

```text
SUPPORTED     + NOT_FALSIFIED → SUPPORTED
NOT_SUPPORTED + FALSIFIED     → REFUTED

SUPPORTED     + FALSIFIED     → NOT_INTERPRETABLE
NOT_SUPPORTED + NOT_FALSIFIED → NOT_INTERPRETABLE

any pair containing BLOCKED    → NOT_INTERPRETABLE
```

Interpretation codes:

- `PREDICTION_SUPPORTED_AND_NOT_FALSIFIED`;
- `PREDICTION_NOT_SUPPORTED_AND_FALSIFIED`;
- `CONTRADICTORY_EVALUATION_STATUSES`;
- `NON_DECISIVE_EVALUATION_STATUSES`;
- `BLOCKED_EVALUATION_STATUS`.

The table is total over all 9 valid status pairs.

### Minimal authoritative inputs

- exact factory-attested `ExperimentEvaluationSubmission`;
- exact factory-attested `QualifiedExperimentEvaluationAuthority`.

No caller may supply:

- finding status;
- interpretation code;
- policy reference;
- supporting measurement IDs.

### Candidate output

`QualifiedExperimentalFinding`

This remains distinct from:

- `ResearchFinding`;
- `ResearchFindings`;
- `ResearchRunEvidence`;
- durable knowledge;
- operational authorization.

---

## 23. Exactly one next governed action

Create only the P1.16 test-first breaker and workflow:

- `breakers/p1_16_qualified_experimental_finding_breaker.py`;
- `.github/workflows/p1-16-qualified-experimental-finding.yml`.

Do not create `src/qualified_experimental_finding.py` yet.

The breaker must exercise all 9 status pairs and prove:

- only the two decisive pairs promote to SUPPORTED / REFUTED;
- contradictory, non-decisive and BLOCKED pairs become NOT_INTERPRETABLE;
- no caller override surface exists;
- exact P1.13B/P1.15B authority chain is required;
- no ResearchFinding/ResearchFindings/ResearchRunEvidence production occurs;
- no knowledge or operational authorization occurs.

Then require:

- protected chain through P1.15A+B PASS;
- P1.16 FAIL only because runtime candidate is absent;
- clean worktree.

