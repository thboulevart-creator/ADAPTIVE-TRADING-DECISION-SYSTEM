# ATDS-EA-02-D1 — SYNTHETIC QUALIFICATION REPORT V0.1

**Date:** 2026-10-16
**Mission:** ATDS-EA-02-D1 V0.1 (bounded synthetic implementation)
**Current status:** CANDIDATE_FOR_HUMAN_REVIEW
**Decision of this report:** SYNTHETIC_TESTS_PASS / CONTRACT_FIDELITY_PASS_WITH_LIMITATIONS
**Not claimed:** adopted production interface, genuine MT5 compatibility, independent economic proof, trading authorization.

## 1. Git reconciliation and isolation

Repository: thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM
Governed branch: integration/system-v1
Canonical base HEAD: 91fc53c406c67acde340599cb0ba35fd5347b02d
Canonical base TREE: c9274ca4f91c5b51d60aad2c607a8528c4f05027
Original local branch HEAD: 9ed38d72580635d9a63eff76cf6196123be2d8a1 (left unchanged).
Git fetch downloaded missing canonical commit, updating remote-tracking reference only, before D1 began.
Detached worktree: C:\Users\Boulevart\Documents\ATDS-EA-02-D1-ISOLATED
Before new files: all nine target paths absent, worktree clean.
Original local untracked materials from separate work were not modified, deleted or staged.

## 2. Candidate files produced — exactly nine

1. docs/ATDS-EA-02-D0-CONSOLIDATED-CONTRACT-V0.2.md
2. src/ea_observation/__init__.py
3. src/ea_observation/schema.py
4. src/ea_observation/provenance.py
5. src/ea_observation/validation.py
6. tests/test_ea_observation_schema.py
7. tests/test_ea_observation_validation.py
8. tests/fixtures/ea_observation_synthetic_v0_1.json
9. reports/program/ATDS-EA-02-D1-SYNTHETIC-QUALIFICATION-V0.1.md

New code is standard-library Python; no former qualified module was changed.

## 3. Implemented within synthetic scope

- Seven adopted observation collections and their minimal structural fields.
- EA binary and configuration identity kept distinct.
- Binding of source records to the synthetic manifest and SHA-256 checks.
- Four provenance interpretation classes and exact/ambiguous/unassigned EA-attribution status.
- Native ORDER, DEAL, CASH_FLOW separation, explicit account and position snapshots.
- Decimal-string checks for amounts, financial costs, quantities and prices.
- Explicit raw timestamp, UTC timestamp, source sequence and equal-time causal ambiguity.
- Bounded synthetic partial close and NETTING reversal validation where initially-flat, complete, causally ordered evidence is claimed.
- Account equity and floating exposure not silently allocated to an individual EA.
- Broker-symbol mismatch/lookahead vetoes.
- Structural, attribution, economic and scientific statuses separated; all economic, drawdown, risk, trading and capital claims fail closed.
- No import of MetaTrader5, no EX5 execution, no real performance data accessed.

## 4. Test command, matrix and exact outcome

Working directory: detached isolated worktree root.
Command: python -B -m unittest discover -s tests -p test_ea_observation_*.py -v
Environment: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH includes worktree root and tests.
No network, terminal MT5, EX5, backtests, brokerage API, strategy optimization or protected real data used.

**First run:** 40 tests, 39 PASS, one FAIL (B01 expected explicit binary-float reason but received only generic decimal rejection).
**Correction:** inside src/ea_observation/validation.py only, added the explicit binary-float rejection reason without weakening decimal rejection.
**After additional fail-closed scope hardening and rerun:** 44 tests, 44 PASS, 0 FAIL, 0 ERROR.

T01 PASS; T02 PASS; T03 PASS; T04 PASS; T05 PASS; T06 PASS; T07 PASS;
T08 PASS; T09 PASS; T10 PASS; T11 PASS; T12 PASS; T13 PASS; T14 PASS;
T15 PASS; T16 PASS; T17 PASS; T18 PASS; T19 PASS; T20 PASS; T21 PASS;
T22 PASS; T23 PASS; T24 PASS; T25 PASS; T26 PASS.

B01 PASS; B02 PASS; B03 PASS; B04 PASS; B05 PASS; B06 PASS;
B07 PASS; B08 PASS; B09 PASS; B10 PASS; B11 PASS; B12 PASS;
B13 PASS; B14 PASS; B15 PASS; B16 PASS; B17 PASS; B18 PASS.

This is a synthetic unit-test result, NOT adversarial independent assurance against all broker event variants, and not proof of profitable EAs.

## 5. Contract differences and limitations

- D0 adopted seven conceptual collections; the executable candidate formalizes their narrow SYNTHETIC profile only.
- D0 proposes full source provenance; the candidate hashes canonical synthetic embedded records, not raw original MT5 byte streams.
- Source-level and record-level provenance is verified. Per-field independent original-source attestation is NOT implemented.
- Partial-close and reversal consistency is checked on a bounded subset only; full MT5 state-machine and server semantics remain unqualified.
- Exact realized NET PnL, account-to-EA equity allocation, exact drawdown and risk-of-ruin remain OUT OF SCOPE and always BLOCKED.
- Synthetic EA binding cannot prove the operator/program generating a real transaction.
- No trusted MT5 export ingestion or EX5 dependency resolution has been attempted.
- No scientific strategy qualification, prospective data admission, or usable portfolio performance has been produced.
- All new files are uncommitted and confined to the isolated worktree.

## 6. Human-review recommendation

Recommend review of candidate V0.2 with noted provenance and broker-semantic limitations.
Possible verdict: adopt synthetic validator as a nonoperational candidate for further hardening only, or return targeted amendments.
Do NOT promote to real MT5 ingestion, production authority or EA-03 without a separate approved contract and independent qualification.
After review, any publication/commit/merge must have separate explicit authorization.

**STOP — CANDIDATE_FOR_HUMAN_REVIEW / NO_COMMIT / NO_PUSH / NO_MERGE / NO_MT5.**
