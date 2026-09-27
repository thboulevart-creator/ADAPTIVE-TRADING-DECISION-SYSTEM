# C01 CONFIRMATION RUNNER — MINIMAL RUNTIME CANDIDATE V0.1

Date: 2026-09-27

Qualified implementation base HEAD:

`4f545e19bcb7283d52a36fd51bbe74934db9286e`

Runtime path:

`tools/c01_confirmation_runner.py`

Working runtime blob before persistence:

`22617ba26603aa56ee0d462a5dd3a313690bcc37`

Qualified breaker blob:

`f2596da79f37a7bd7f46078e6b60a661158b6bf7`

## Authorization boundary

Authorized development class:

`SYNTHETIC_ONLY`

Not authorized:

- confirmation-window outcome access;
- primary scientific confirmation scoring;
- real confirmation execution;
- MT5;
- parameter refit;
- threshold/bin search;
- probability refit;
- feature redesign;
- interaction redesign;
- semantic regime naming;
- strategy;
- direction target;
- signals;
- trades;
- PnL;
- C02 redesign.

## Minimal runtime surface

The candidate exposes only:

- `RUNNER_CONTRACT`
- `RESULT_SCHEMA`
- `evaluate_confirmation_case(case)`

The runtime contains no data loader and no MT5 dependency.

## Qualified harness result

`py_compile = PASS`

Qualified test-first harness:

`33 passed`

Collection errors:

`0`

Qualified breaker remained unchanged:

`f2596da79f37a7bd7f46078e6b60a661158b6bf7`

## Supplemental adversarial hardening

Three additional local probes were executed after static review:

1. non-finite primary metric `NaN`;
2. non-finite primary metric `Infinity`;
3. non-integer/non-finite joint-state count.

Results:

- `NONFINITE_NAN = PASS`
- `NONFINITE_INFINITY = PASS`
- `NONFINITE_JOINT_STATE = PASS`

The runtime now rejects non-finite primary metrics and invalid joint-state count values fail-closed as:

`NOT_INTERPRETABLE`

## Guard-first behavior

The candidate preserves:

`eligibility -> critical controls -> sparse guard -> primary metrics`

Therefore:

- pristine/new-data eligibility failure cannot become `REFUTED`;
- identity/provenance/continuity failure cannot become `REFUTED`;
- sparse-state failure cannot become `REFUTED`;
- primary metric adjudication occurs only after critical guards pass.

## Metric convention

Frozen convention:

`delta = baseline - candidate`

Positive delta means candidate improvement.

## Synthetic/scientific separation

Synthetic cases may produce simulated:

- `CONFIRMED`
- `REFUTED`
- `NOT_INTERPRETABLE`

while still preserving:

- `primary_confirmation_score_computed = false`
- `real_confirmation_execution = false`
- `scientific_confirmation = NOT_YET_PERFORMED`

A synthetic `CONFIRMED` status is not a scientific confirmation result.

## Current scientific state

Confirmation data accessed:

`false`

Primary confirmation score computed:

`false`

Real confirmation execution:

`false`

Scientific confirmation:

`NOT_YET_PERFORMED`

## Status

**MINIMAL RUNTIME PERSISTENCE CANDIDATE — NOT YET QUALIFIED.**

## Next governed action

Persist exactly:

1. `tools/c01_confirmation_runner.py`
2. this candidate report
3. the checkpoint update

Then perform a fresh persisted-head adversarial re-break.

Only after that persisted-head re-break returns PASS may the runtime itself be qualified.
