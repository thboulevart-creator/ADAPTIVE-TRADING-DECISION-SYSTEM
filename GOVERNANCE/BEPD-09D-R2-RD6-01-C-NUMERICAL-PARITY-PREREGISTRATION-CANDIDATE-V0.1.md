# BEPD-09D-R2-RD6-01-C — TRAINING-ONLY NUMERICAL PARITY PREREGISTRATION CANDIDATE V0.1
**CANDIDATE FOR FUTURE HUMAN SELECTION; NOT ADOPTED, NOT EXECUTED.** 2026-10-09. No real observations accessed.

## Frozen prerequisites
C1 = unregularized binary logistic regression, target `same_week_reintegration`, baseline design (intercept+4 spline), context design (baseline+4 frozen features), 5 chronological expanding folds. Adopted primary Candidate B: Newton-CG, maxiter 5000, xtol 1e-10, zero-vector initialization. Existing individual primary gate `||∇L(βp)||∞ <= TAU_SCORE(X)`, where `TAU_SCORE(X) = 1.4901161193847656e-8 × max(1, max_j sum_i |X_ij|)`. The 14 required RD2 gates must be obtained **exactly from the frozen acceptance contract**, with no post-hoc relaxation. Reference existing `scipy.optimize.root(... method="hybr", options={"xtol":1e-10,"maxfev":5000})` in `tools/bepd09c_reference.py`. Historical `2e-5` is a test prediction/metric comparison tolerance **not** a coefficient/objective parity tolerance.

## Three independent layers, in this exact order (candidate only)
**P — primary individual acceptance:** before any reference, enforce finite X/y/β/objective/gradient/Hessian; exact column rank; both response classes; no perfect separation (LP statuses: infeasible proves no strict separator, feasible is REJECT, indeterminate/exception = STOP); immutable model/feature/data/TAU identity; compute gradient score with independently checked function; exact adopted `TAU_SCORE`; Candidate B verdict ACCEPT required, optimizer.success informational only.

**R — reference individual validity:** independent train-only fit uses **identical X_train/y_train, same fold/model role** (no test matrices/predictions), independently computes objective, gradient and Hessian under mathematically identical frozen logistic likelihood. For reference stationarity, candidate rule `||∇L(βr)||∞ <= TAU_SCORE(X)` is recommended, **NOT ALREADY ADOPTED FOR THE REFERENCE**. LP solver status, finite derivatives, full rank, two classes and exact identities must be fail-closed. Reference `_fit` historically only checks `sep.success` and a `1e-8` residual condition when root reports failure; this is not sufficient proof of all RD2 primary gates and requires a qualified isolated wrapper (not authorized here).

**C — cross-solver consistency:** independent stationarity of both solutions **does not logically imply coefficient equality in ill-conditioned systems**. Compare exact same deterministic objective calculated by a third, cross-checked evaluator and report scale-free objective difference. Candidate preferred statistic
```text
Jp = sum_i(logaddexp(0, X_i·βp) - y_i*(X_i·βp))
Jr = sum_i(logaddexp(0, X_i·βr) - y_i*(X_i·βr))
DELTA_J = abs(Jp-Jr) / max(1,abs(Jp),abs(Jr))
GATE_C_CANDIDATE = DELTA_J <= 1e-8
```
**The 1e-8 threshold is a PRE-ADOPTION ENGINEERING PROPOSAL, not selected by human authority, not empirically validated, and not fit to exposed Fold3 diagnostics.** Assess separate absolute floor and float sensitivity on preregistered synthetic landscapes before adoption. If score passes but objective parity fails, STOP; **never pick the better solver**, change the objective or invoke reference as fallback. A stronger option is objective plus normalized parameter-distance constrained by a preregistered Hessian condition number, but only if a separate scientific reason justifies parameter identifiability. Do not impose coefficient equality absent condition diagnostics.

## Diagnostic quantities, not scientific model outputs
For each pair (fold, model role): train-only n, class counts, exact digests and version ids; objective finite flags `Jp,Jr` **prefer only export delta or flag, never full raw objective if it is not on public allowlist**; `norm_g_primary/tau`, `norm_g_reference/tau`, `DELTA_J` only after an explicit output-contract adoption; Hessian condition marker without eigenvectors; stop reason and ordinal step id. All parameter vectors remain transient memory; no coefficient ranking, test metrics, fold test responses, new exposure metric or PNL.

## Undefined/exception states
`X` mismatch, permutation or different preprocessing = STOP; rank deficiency, near-singularity with undefined condition statistic, one class, perfect separation, LP status unknown, NaN/inf, optimizer exception, reference errors, trace protection failure, objective-evaluator disagreement, objective negative outside numerical tolerance, unexpected role, mismatch of view hashes, unknown parity tolerance, output allowlist breach = STOP. Mark unknown `BLOCKED`, do NOT impute zeros or accept under `optimizer.success` alone.

## Proposed preregistration sequence for next separately authorized synthetic work
1. Bind exact frozen source blobs/science and draft numerical formulas *before* synthetic data generation.
2. Preregister synthetic cases: well-conditioned equivalent optima; ill-conditioned nearly collinear X; full rank with large scales; one-class; perfect/quasi-separation; reference LP exception/status=UNKNOWN; primary nonconvergence; reference converged but different objective; both stationarity pass with DELTA_J failure; objective evaluator altered; NaN/inf; rank deficiency; optimizer.success false with contract gates true; tolerance just below/on/above chosen boundary.
3. Define precision/normalization, resource budgets and exact default status for missing reference.
4. Run at most the separately authorized synthetic experiments; results reviewed by independent reviewer; only then humans choose formula and tolerance.
5. Freeze code, versions, schema and output/receipt contract prior to any real exposure; no post-hoc modifications after old Fold3 evidence.

## Material human choices
`C-MAT-01`: objective-gap-only metric (candidate preferred) vs objective+conditioned-parameter metric vs no cross-parity gate.
`C-MAT-02`: select or reject `1e-8` objective-gap threshold after independent synthetic calibration; human selection required.
`C-MAT-03`: independent reference stationarity gate `TAU_SCORE(X)` vs independent reference-specific threshold; human selection required.
`C-MAT-04`: reference nonconvergence, objective disagreement, and LP status STOP policy; human adoption before real fit.
`C-MAT-05`: permitted public numerical diagnostic fields / serialization. No automatic expansion of RD5 allowlist.

`PRIMARY_EXISTING_RD2_GATE=PASS_STATIC_IDENTITY`; `REFERENCE_TRAIN_ONLY_QUALIFIED_WRAPPER=BLOCKED`; `REAL_PARITY_METRIC=NOT_ADOPTED`; `REAL_PARITY_TOLERANCE=NOT_ADOPTED`; `SCIENTIFIC_RESULT=NONE`.
