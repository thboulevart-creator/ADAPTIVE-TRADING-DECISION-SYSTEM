# BEPD-09D-R2-RD6-02-D — INDEPENDENT EXTERNAL REVIEW HANDOFF PACKAGE V0.1
**Prepared only; no reviewer contacted, no external review conducted, no shared data, no spend authorized.** 2026-10-09.

## Purpose
For a reviewer genuinely independent of the RD3/RD5 implementation and current internal assessment: adversarially evaluate the exact frozen code, input provenance, train/test isolation, LP fail-closed semantics, tracing guard and nested outputs. Do not re-engineer trading science or infer readiness to execute on real data. This package is a **handoff specification**, not a completed certification.

## Source identity contract (pinned)
GitHub `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`, branch `integration/system-v1`, review parent HEAD `8b14b3f2be26487e74f946c1a48044ab03595f2e`, TREE `c4a7643a849de607e3a99d78b6d155e59b345a73`.
- RD5 adapter `tools/bepd09d_r2_rd5_training_only_adapter.py` git blob `bfbf586914c852047123c3a4cd1b2fa6a7dc4daa`.
- RD3 Candidate B `tools/bepd09d_r2_rd3_candidate_b_runtime.py` git blob `38588b0a0b9c5b4cb9fcee0c7d524e63d5039c69`.
- RD2 overlay `tools/bepd09d_r2_runtime.py` git blob `209b3b5b804da4da9ee6751f2a15a32df0e3e4b1`.
- Legacy runtime `tools/bepd09c_runtime.py` git blob `72645c3201d3d454d4d5402a0e2191e1195c68a6`.
- Legacy reference `tools/bepd09c_reference.py` git blob `2c8a82405082ce3f820b580017a96af77e74b0e4`.
- Legacy full-data harness `tools/bepd09d_real_execution_harness.py` git blob `bc16016c593f89ec56ab65c9b8f0d6758d59cbe1`.
- Synthetic test matrix `tests/test_bepd09d_r2_rd5_adapter.py` blob `6d6374e701e1572d9ee597add238973223e555ea`.
- Governing closures RD6-01 `3c5fa4c655f5e015e7d4660828162a8c9ab0dcca`; RD5 adoption `cf3bb96620fe65622cdbdaa9b8f9fb37aacab519`.
For other exact package paths/blobs, refer to RD6-02-A manifest.

## Reviewer conditions
1. Reviewer identifies individual/organization, relevant experience, direct or financial relationships to builder/broker/firm, conflicts and whether reviewers previously wrote or edited these source files. No pretended independence.
2. Independently verify SHA of every named blob and establish time/freshness of reviewed checkout; signed report must identify any variance. No replacement from default branch `main`.
3. Read-only static review may inspect only governing public code/documents; any synthetic executable hostile tests require **separately scoped human authorization and a clean environment**. No tests, workflow reruns, benchmark, real ledger or user secrets under present authority.
4. No third-party service transmission of source/documents, account connection or spending until separately authorized.
5. Review methodology must document source ranges, threat assumptions, tested vs hypothesized failures, tool versions, controls actually exercised, evidence hashes, and how alternate explanations are excluded.
6. Evidence types strictly `STATIC_SOURCE_EVIDENCE`, `EXISTING_SYNTHETIC_EXECUTION_EVIDENCE`, `INDEPENDENT_EXTERNAL_EVIDENCE`. A reviewer who reads an existing internal report does not automatically provide independent executable evidence.

## Exact review tasks
IR-01 independent LP tri-state audit and exception-catch semantic, including `linprog` non-raising unknown statuses and build_packet fallback.
IR-02 sys.settrace thread/native/callback/code-object/monkeypatch/tracer-interaction/reentrancy audit; restore trace on every path.
IR-03 signed provenance interface feasibility; forged `fixture.PROVENANCE` and callers supplying unauthorized records.
IR-04 physical byte access semantics and signed fold-scoped views with no model worker ledger mount; audit proof limitations of prefiltering.
IR-05 import-time mutation / shared interpreter side effect isolation.
IR-06 recursive output schema and uncontrolled optimizer message / encoded output/path/stacktrace leakage.
IR-07 independent reference solver status and non-use of test-scoring runtime; no reference fallback.
IR-08 scientific preservation: C1 calendar/folds, y, features, likelihood/gradient/Hessian, Candidate B solver and exact TAU gate.
IR-09 adversarial test gap mapping vs the 29 frozen synthetic RD5 tests, reproducibility and structural limitations.
IR-10 reviewer independence, signed source-binding receipt and accepted/blocked findings.

## Mandatory report schema
```text
REVIEWER_IDENTITY = name and organization, verifiable
INDEPENDENCE_AND_CONFLICTS = declared with evidence
REVIEWED_SOURCE_GIT_COMMIT_AND_TREE = exact
REVIEWED_BLOBS = path, git object hash and content hash
SCOPED_AUTHORITY = explicit and bounded
PROCEDURES_AND_ENVIRONMENT = reproducible; "not executed" where so
FINDINGS = id, source path, exact source lines, precondition, threat/impact
EVIDENCE = type, location, SHA, counterevidence, known limitations
RESULT = PASS | FAIL | BLOCKED | NOT_ASSESSABLE per property
REMEDIATION = source or boundary changes proposed, no auto mutation
REPORT_DIGEST_AND_ATTESTATION = independently verifiable signature or accepted authenticated provenance
REMAINING_BLIND_SPOTS = mandatory
```
If missing identity/provenance/reviewed blobs or unbounded procedures => **external review result NOT_ASSESSABLE**. Any failed security property => independent overall PASS forbidden. External signed review itself still requires distinct human adjudication.

## Immutable stop line
`RD6_02_HANDOFF_DOCUMENT=READY_FOR_SEPARATE_HUMAN_AUTHORIZATION`; `EXTERNAL_REVIEW_SENT=NO`; `EXTERNAL_REVIEW_COMPLETED=NO`; `REAL_TRAINING_READY=BLOCKED`; `STOP=MANDATORY`.
