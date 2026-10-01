# P5-E V0.1 — REQUIREMENT / EVIDENCE MATRIX QUALIFICATION

Date: 2026-10-01

## Scope

Qualification of the explicit mapping:

`requirement → executable test → Git blob → verdict`

required by the external-review targeted closure amendment.

## RED predecessor

Matrix RED HEAD:

`95881afe5f03783de3c933d2c8ee65373220f3ed`

Matrix test RED blob:

`8cb3287d735b63414e9bf8e73fdf9755f3b8b855`

Matrix RED evidence blob:

`8c22994c16f8f78ded4b2d62892af748741339b5`

## Mechanical correction during implementation

The first matrix generator computed raw working-tree SHA-1 bytes.

That disagreed with Git blob identity for a CRLF-filtered file even though the file was not modified.

Persistence was stopped.

The matrix test and generator were mechanically corrected to use:

`git hash-object --path=<repository-relative-path> <file>`

This respects repository Git filters and produces the same object identity Git would persist.

No requirement, test expectation, or authority boundary was weakened.

## Matrix artifact

`tools/obsidian_projection/p5e_v0_1_requirement_evidence_matrix.json`

Coverage:

```text
REQUIRED_SYNTHETIC_CASES = 10 / 10 MAPPED
BASE_BREAKERS            = 25 / 25 MAPPED
TARGETED_CLOSURE_BREAKERS=  8 /  8 MAPPED

TOTAL                    = 43 / 43 MAPPED
UNMAPPED                 = 0
DEFERRED                 = 0
```

Each entry binds to:

- a repository-relative executable test file;
- a concrete unittest method;
- the exact Git blob of the current test bytes;
- an evidence kind:
  - `DIRECT_P5E`, or
  - `REUSED_QUALIFIED_P5D2_P5D4`;
- verdict `PASS`.

## Reused predecessor evidence

The matrix reuses already-qualified executable behavior instead of duplicating it for:

- SAME-head strict queue NOOP;
- NON_FAST_FORWARD block without queueing;
- UNKNOWN ancestry block without queueing;
- queue capacity fail-closed before P5-D2 mutation;
- newer FAST_FORWARD queued without retargeting the active candidate.

Reused tests are blob-bound.

## Matrix test

Command:

```text
python -B -m unittest tests.obsidian_projection.test_p5e_requirement_evidence_matrix_v0_1
```

Observed:

```text
Ran 5 tests in 1.217s

OK
```

## Combined P5-E targeted surface

Command surface:

- P5-E contract/base tests;
- P5-E adversarial tests;
- external-review B1→B5 targeted-closure tests;
- requirement/evidence matrix tests.

Observed:

```text
Ran 50 tests in 1.337s

OK
```

## Authority

The matrix explicitly records:

```text
REAL_P5E_EXECUTION = FALSE
REAL_60_SECOND_SLA_QUALIFIED = FALSE
PER_TRANSIENT_TIP_DETECTION_SLA_QUALIFIED = FALSE
AUTOMATIC_EVALUATION = FALSE
AUTOMATIC_PROMOTION = FALSE
AUTOMATIC_PUBLICATION = FALSE
```

No real P5-E execution is authorized or claimed.
