# P5-E V0.1 — EXTERNAL REVIEW TARGETED CLOSURE RED EVIDENCE

Date: 2026-10-01

## Scope

First targeted RED execution after internal adjudication of external-review findings B1→B5.

Branch:

`feat/obsidian-projection-p5e-v0.1-external-review-targeted-closure`

Preregistration HEAD:

`db1e952a07a143d5dab3f646bc5974f5c156d58b`

Preregistration blob:

`0832daa9c553945e4bc2169b0d9c2d1b762b8b4d`

Internal adjudication blob:

`ba4f0bdc5a77894fcfa6504c754d40cb77a9e820`

## RED test artifact

`tests/obsidian_projection/test_p5e_external_review_targeted_closure_v0_1.py`

The targeted closure test was created before any B1→B5 contract/model correction.

## Command

```text
python -B -m unittest tests.obsidian_projection.test_p5e_external_review_targeted_closure_v0_1
```

## Observed result

```text
Ran 12 tests in 0.038s

FAILED (failures=1, errors=10)

RED_EXIT=1
```

Classification:

- 1 PASS: current model imports already satisfy the AST allowlist used by the new guard;
- 1 FAIL: current adversarial invariant function does not reject all previously demonstrated B1 mutations;
- 10 ERROR: corrected contract blocks/model API/tip-classification surface do not yet exist.

## RED families frozen

The RED test now requires:

- exact required-case and base-breaker lists plus an explicit targeted-closure breaker list;
- adversarial rejection of the previously surviving B1 mutations;
- controlled local monotonic source-release origin;
- successful remote-read completion as latency endpoint;
- fixed-rate scheduling;
- explicit rejection of remote-head-availability as a measurable local origin;
- exact distinction between observed remote tip and unobserved intermediate fast-forward commit;
- skipped required slot -> fail-closed;
- cadence gap -> fail-closed;
- target head observed before controlled release -> fail-closed;
- nonzero read duration included in latency;
- non-aligned source release with no remaining possible in-bound attempt -> FAIL;
- observed-head identity required;
- exact-tip and containment classifications remain distinct.

## Authority

No real P5-E polling, evaluation, Stage A/B, promotion, publication, Vault mutation, CURRENT mutation, daemon, task, service, startup registration, P6, or human adoption was executed or authorized by this RED run.

`REAL_P5E = CLOSED`.
