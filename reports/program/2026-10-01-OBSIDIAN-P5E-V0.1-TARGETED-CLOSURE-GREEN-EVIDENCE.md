# P5-E V0.1 — EXTERNAL REVIEW TARGETED CLOSURE GREEN EVIDENCE

Date: 2026-10-01

## Scope

Minimal correction of the internally adjudicated external-review findings B1→B5.

No P5-D2 or P5-D4 runtime implementation was modified.

No real P5-E execution occurred.

## RED predecessor

RED HEAD:

`4acf61474bfec021a1b7e05dcb1f1a8c6bb468fc`

RED test blob:

`15c3e44ab9c1c40873110d88ff42cebb13a2643e`

RED evidence blob:

`7f26fa16ca67926eaaa4f94672d5cb2c8eff0d4b`

## Corrected surfaces

- `tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json`
- `tools/obsidian_projection/p5e_near_real_time_model.py`
- `tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py`
- `tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py`

The preregistered targeted RED test remains unchanged.

## B1 closure

The adversarial invariant surface now checks the normative P5-E blocks that previously allowed silent mutation:

- timing;
- synthetic clock/model;
- head-transition policy;
- queue/supersession;
- failure/freshness;
- authority boundary;
- tip visibility;
- end-to-end claim scope;
- next gate;
- exact required-case list;
- exact base-breaker list;
- exact targeted-closure breaker list.

Previously demonstrated mutations now fail the invariant checker.

Existing qualified P5-D2/P5-D4 behavior is reused rather than reimplemented.

## B2 closure

Synthetic timing now models a fixed-rate 30-second schedule.

It distinguishes:

- scheduled attempt start;
- read completion.

Skipped required slots and cadence gaps return:

`BLOCKED_REQUIRES_ADJUDICATION`

No silent widening of the 30-second cadence is accepted.

## B3 closure

A target HEAD returned by an attempt that started before the controlled source release returns:

`BLOCKED_REQUIRES_ADJUDICATION`

with:

`TARGET_HEAD_OBSERVED_BEFORE_CONTROLLED_RELEASE`

The former silent-ignore behavior is removed.

## B4 closure

The current candidate no longer claims that remote GitHub availability time is a directly measurable local timing origin.

The future real metric is frozen as:

```text
SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC
-
CONTROLLED_SOURCE_RELEASE_MONOTONIC
```

Schedule semantics:

`FIXED_RATE`

Poll interval:

`30 seconds`

Maximum latency:

`60 seconds`

Read duration is included in latency.

A single transient failure is not an unconditional 60-second guarantee.

## B5 closure

The contract and model distinguish:

- `EXACT_TIP_OBSERVED`;
- `CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED`;
- `UNRELATED_OR_UNPROVEN_REQUIRES_ADJUDICATION`.

A transient intermediate commit contained by a later observed fast-forward HEAD is not relabelled as an exactly observed tip.

An unobserved intermediate tip may not be queued.

A head already observed and queued remains protected by existing FIFO/no-retargeting P5-D2/P5-D4 semantics.

## Targeted execution

Command surface:

```text
tests.obsidian_projection.test_p5e_end_to_end_near_real_time_contract_v0_1
tests.obsidian_projection.test_p5e_end_to_end_near_real_time_adversarial_v0_1
tests.obsidian_projection.test_p5e_external_review_targeted_closure_v0_1
```

Observed:

```text
Ran 45 tests in 0.035s

OK
```

Contract JSON validation:

`PASS`

Diff whitespace validation:

`PASS`

## Current verdict

```text
P5E_TARGETED_B1_B5_GREEN
= 45 / 45 PASS

REQUIREMENT_EVIDENCE_MATRIX
= NEXT

REAL_P5E
= CLOSED

HUMAN_NORMATIVE_ADOPTION
= NOT_AUTHORIZED
```
