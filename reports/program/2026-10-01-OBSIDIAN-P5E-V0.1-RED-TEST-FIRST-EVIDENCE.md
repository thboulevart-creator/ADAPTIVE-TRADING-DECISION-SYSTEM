# P5-E V0.1 — RED TEST-FIRST EVIDENCE

Date: 2026-10-01

## Scope

This record persists the first RED execution for:

`P5-E — END-TO-END NEAR-REAL-TIME QUALIFICATION V0.1`

Authorized stage:

`CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY`

No real P5-E polling, evaluation, promotion, publication, Vault mutation, Stage A, Stage B, P6, daemon, Scheduled Task, Windows Service, or startup registration was authorized or executed.

## Preregistration basis

Preregistration HEAD:

`7843a5b6a35f08d9e14572d7ecd24f15e2ffce46`

Preregistration blob:

`6ef788532a1e945a42ca524af823710ae4f14ed6`

Artifact:

`tools/obsidian_projection/p5e_end_to_end_near_real_time_preregistration_v0_1.json`

## RED test artifact

`tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py`

The test was created before the P5-E contract and before the synthetic timing model.

## RED execution

Command:

```text
python -B -m unittest tests.obsidian_projection.test_p5e_end_to_end_near_real_time_contract_v0_1
```

Observed result:

```text
Ran 17 tests in 0.014s

FAILED (failures=2, errors=14)

RED_EXIT=1
```

Classification:

- 1 test passed: preregistration presence/status;
- 2 tests failed because the expected P5-E contract/model files did not yet exist;
- 14 tests errored because contract loading or synthetic-model loading reached those intentionally absent files.

The RED signal therefore demonstrates that the new P5-E requirements were not already satisfied by pre-existing files.

## What the RED test freezes

The test surface requires at minimum:

- exact P5-A inherited 30-second candidate interval;
- exact 60-second maximum detection latency;
- explicit detection-latency definition;
- no instantaneous-realtime claim;
- no silent widening of timing bounds;
- no evaluation/promotion/publication/P6 authority;
- current P5-D4 FIFO/no-coalescing queue semantics;
- queue-capacity exhaustion -> `QUEUE_CAPACITY_REQUIRES_ADJUDICATION`;
- no synthetic sleep/network/filesystem/process primitive;
- detection just after a poll;
- one transient read failure with success by 60 seconds;
- rejection after 60 seconds;
- rejection when no detection exists by the bound;
- rejection of a non-30-second synthetic observation schedule;
- no laundering of synthetic qualification into a real P5-E PASS.

## Mandatory next step

Only the minimal P5-E contract and pure synthetic timing model needed to satisfy these already-persisted tests may now be added.

Real P5-E execution remains closed.
