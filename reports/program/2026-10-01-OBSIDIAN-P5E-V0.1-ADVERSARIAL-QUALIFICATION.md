# P5-E V0.1 — ADVERSARIAL QUALIFICATION

Date: 2026-10-01

## Scope

Adversarial qualification of the P5-E V0.1 candidate contract and pure synthetic timing model.

No real polling, network observation loop, evaluation, promotion, publication, Vault mutation, Stage A, Stage B, P6, daemon, Scheduled Task, Windows Service, or startup registration was executed.

## Candidate identity before adversarial expansion

Minimal GREEN HEAD:

`2f7b16479149602da94c8434ddefe2104adfe4f9`

Contract blob:

`e5c3d7a9d451aba65e8062078c6c10d23e586f39`

Synthetic timing model blob:

`8662dd97a1c8a1af33d6593ae923384e96404b5a`

## Adversarial harness

`tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py`

The harness independently mutates copies of the contract and requires those mutations to violate frozen invariants.

Mutation families include:

- poll interval 30 -> 31 seconds;
- detection bound 60 -> 61 seconds;
- real P5-E authority activation;
- evaluation authority activation;
- promotion authority activation;
- publication authority activation;
- real polling authority activation;
- P6 authority activation;
- queue coalescing reintroduction;
- latest-only pending-head replacement;
- queue-capacity silent continuation;
- P5-A historical supersession intent overriding qualified P5-D4 semantics;
- synthetic qualification relabelled as real P5-E qualification;
- removal of real-PASS claim prohibition.

Synthetic timing edge cases include:

- exactly 60-second detection boundary;
- apparent observation before source availability;
- negative/boolean source time;
- empty observation surface;
- duplicate observation time;
- invalid synthetic outcome;
- incomplete timing window;
- downstream authority remaining false for all model verdicts.

## Result

Command:

```text
python -B -m unittest \
  tests.obsidian_projection.test_p5e_end_to_end_near_real_time_contract_v0_1 \
  tests.obsidian_projection.test_p5e_end_to_end_near_real_time_adversarial_v0_1
```

Observed:

```text
Ran 42 tests in 0.027s

OK
```

No mechanical correction was required.

## Adjudication

```text
P5E_V0_1_BASE_TESTS
= 17 / 17 PASS

P5E_V0_1_COMBINED_ADVERSARIAL_SURFACE
= 42 / 42 PASS

CONTRACT_CORRECTION_REQUIRED
= FALSE

REAL_P5E
= CLOSED
```
