# BEPD-09D-R2-RD4 — B TRAINING-ONLY EXECUTION DESIGN V0.1
**CANDIDATE / DOCUMENTARY ONLY / NO IMPLEMENTATION AUTHORITY**

Parent HEAD `5ae2bb0fd80d529e921def8ebcace860df8447eb`; tree `0ec38a3a56053ff3fb0da9f06640351491a1dc9f`.
Frozen data: EVENT_LEDGER git blob `0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2`; C1 259-week partition blob `7d950d957611cf209d811c788ff10abded30d011`.
Adopted Candidate B runtime `38588b0a0b9c5b4cb9fcee0c7d524e63d5039c69`. Source and reference runtime unchanged.

## Exclusive purpose
Design a **future**, separately authorized numerical-only training-fit qualification for the frozen C1 binary logistic regression. This RD4 phase reads **no real event rows**, launches no fit, and creates no executable. No C1 score/performance claim.

## Isolation invariant / fold roles
Fold 1 train B1 / protected B2; fold 2 train B1+B2 / protected B3; fold 3 train B1+B2+B3 / protected B4; fold 4 train B1..B4 / protected B5; fold 5 train B1..B5 / protected B6. Training weeks 44,87,130,173,216; protected test block always 43 weeks. These are metadata counts, **not real sample counts**. Training of fold k may contain a block that was testing in an earlier fold; therefore **the barrier is per-current-fold**. Prohibition applies to current-fold test responses, matrices, predictions, model metrics and any downstream evaluation.

## Future isolation architecture (proposed, not implemented)
1. Prior independent authorization must establish a **trusted bounded training view** for each fold with verifiable source digest, fold role and strict schema. Never pass a complete real ledger object to the C1 model executor.
2. Resolve the physical-read contradiction: the legacy harness's `LEDGER_PATH.read_bytes()` and `validate_rows(rows, calendar)` inspect the complete ledger and cannot satisfy literal **NO TEST RESPONSE READ**. Any proposed trusted materializer/verification boundary requires separate explicit authority; computing a whole-ledger SHA256 is itself a whole-ledger byte read and is **not** authorized now.
3. A separately qualified adapter should accept only (`fold_id`, frozen training week IDs, scoped rows) and reject any row not belonging to the current fold's training block set; enforce event_id uniqueness, week and sweep_cluster binding, data types, datetime/DST, feature contracts, role separation, nonfinite checks, and complete audit trail. Never emit raw observations.
4. Construct `_stats(train)` **from training only** and `_mats(train, stats)` for baseline/context without test matrices. Retain frozen 4-context-feature restriction, intercept/spline basis, response `same_week_reintegration`; use baseline and context exactly as frozen. No adaptive training row deletion or substitute sample.
5. Invoke `fit_logistic_candidate_b(Xtrain,ytrain)` on each designated pair only after a future authorization. This adopted function returns diagnostic metadata and parameter arrays; its return MUST remain ephemeral, with a strict allowlist exporter, never raw `X/y`, coefficients, matrices or prediction data.
6. The candidate has `run_protocol = None` and `REAL_EXECUTION_PATH_ACTIVATION = False`. Never modify those in RD4. Never reuse `bepd09c_runtime.run_protocol` or the historical real harness: both have test-prediction/scoring paths.
7. Reference consistency must use only independent **training** X/y, with standalone reference fitting semantics. Reference is NEVER fallback nor scientific result producer. A valid **training-only** numerical parity statistic and threshold must be chosen ex ante; historical 2e-5 probability/metric tolerance CANNOT be silently repurposed as a coefficient or score tolerance.
8. Future execution is single deterministic bounded attempt with immediate STOP at the first identity, data, fit, reference, or evidence breaker. No retry, tuning, conditional skip or full forward scientific continuation under this authorization.

## Static integration findings, not runtime qualifications
- `tools/bepd09d_r2_rd3_candidate_b_runtime.py:192-216` defines `fit_logistic_candidate_b(X,y)`; `run_protocol=None` at line 26.
- `tools/bepd09c_runtime.py:130-141` builds five forward folds, creates test designs/predictions and calls logloss/Brier `_score`; prohibited for training-only qualification.
- `tools/bepd09d_real_execution_harness.py:360-400` reads full real ledger, constructs both full-row preps and calls `run_protocol`; prohibited.
- Candidate B `build_packet` catches separation-detector exceptions and substitutes `perfect_separation=False` (`tools/bepd09d_r2_rd3_candidate_b_runtime.py:127-133`); in a future real adapter an unknown/separation LP failure must be **fail-closed** and cannot be equated to confirmed no separation. A separate fail-closed guard/diagnostic protocol is required and must be synthetically qualified before real use; no modification to adopted runtime is authorized now.
- `tools/bepd09c_reference.py:63-88` computes test predictions and metrics; reference training-only path must avoid this function.

## Hard unresolved gates
`TRAINING_ONLY_VIEW_MATERIALIZATION = BLOCKED`; `FOLD_SCOPED_INPUT_ISOLATION = BLOCKED`; `SEPARATION_DETECTOR_UNKNOWN_STATE_HANDLING = BLOCKED`; `REFERENCE_TRAINING_PARITY_PREDEFINITION = BLOCKED`; `ADAPTER_IMPLEMENTATION_AND_SYNTHETIC_QUALIFICATION = NOT_AUTHORIZED`; `REAL_EXECUTION = NOT_AUTHORIZED`.

No test scoring, no training fit, no real reference fit, no new OOS, no trading. STOP for human adjudication.
