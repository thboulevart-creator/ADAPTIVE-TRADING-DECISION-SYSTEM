# Q-RM-12 — POST-SEAL HANDOFF RUNTIME — ADVERSARIAL BREAK

**Date:** 2026-09-20  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`

## 1. Initial candidate

Runtime:

`src/native_bi5_qrm12_handoff.py`

Initial candidate blob:

`0a198cbd80eb3038cbf0735e88d32ab2a734ad63`

Candidate + targeted workflow commit:

`be77fe792ee8302ada771200d44c7572ed2ca69f`

Initial full frozen-contract execution:

```text
run = 35500675954
job = 106051772524

70 tests collected
69 passed
1 failed

sole failure =
test_e3_preseal_cross_path_information_flow_is_forbidden

qualification environment = PASS
exact persisted locks = PASS
clean worktree = PASS
```

The sole failure was not caused by the handoff runtime. It came from a frozen breaker source-text scan against the already-qualified I_A V0.2 source.

## 2. Dedicated handoff adversarial breaker

Breaker:

`breakers/native_bi5_qrm12_handoff_adversarial.py`

blob:

`59c6f976e72f112c8450de6ac4ba23cff159ba78`

Initial adversarial run:

```text
run = 35500785870
job = 106052057807

8 tests collected
3 passed
5 failed
```

Demonstrated handoff defects:

```text
H-F01 — LEFT_RIGHT_IMPLEMENTATION_ROLES_INTERCHANGEABLE
H-F02 — BOTH_RESULTS_CAN_REBIND_TO_SAME_FORGED_O_VERSION
H-F03 — PATH_WORKSPACE_COLLISION_NOT_REJECTED
H-F04 — ORACLE_OUTPUT_IDENTITY_AND_SCHEMA_NOT_VALIDATED
H-F05 — ORACLE_OUTPUT_KEYSET_NOT_CLOSED
```

## 3. Minimal correction

Correction commit:

`06480a2e9f16aac96b8ce2d5b14a52891fdc368a`

Final corrected handoff source blob:

`95d5fcf0a70757abcb2509363b7b03fdea785c71`

Only the five demonstrated handoff defects were corrected.

No change was made to:

```text
I_A V0.2
cab85272bc5a2e229f56f1e02e624d68dc84ce29

I_B V0.2
6d14704548861c13dfc809adad6ae7a21e31c2ca

Q-RM-12 compatibility breaker
967ab86d517cc8736344bb27154641eb9bac7996

F source
199b07929fe8ec40d719b001b0321d1f26c8faab

O source
219b22bc92855c24eef3a7abb08e177644d05c76
```

## 4. Corrected handoff adversarial re-break

Run:

`35500849184`

Job:

`106052227263`

Observed:

```text
8 tests collected
8 passed
qualification environment = PASS
exact locks = PASS
clean worktree = PASS
```

The corrected handoff therefore survives its dedicated adversarial suite.

## 5. Frozen-breaker E3 defect exposed by full compatibility execution

The frozen breaker test:

`test_e3_preseal_cross_path_information_flow_is_forbidden`

contains a source-text prohibition on the substring:

`other_path_output`

for I_A V0.2.

The qualified I_A source contains that substring only through the required isolation-evidence field:

`other_path_output_readable`

Observed I_A occurrences are limited to:

- default isolation-evidence value;
- reading the execution-context isolation declaration;
- emitting the isolation-evidence field;
- checking that the field is exactly `False`.

No I_B module import, I_B result variable, opposite-result authority, or handoff pre-seal dependency was demonstrated.

Therefore E3 currently conflates:

```text
required isolation evidence:
other_path_output_readable = False
```

with:

```text
forbidden cross-path output information flow
```

This is a demonstrated breaker false positive outside the handoff runtime.

## 6. Adversarial-stage conclusion

```text
handoff dedicated adversarial suite = GREEN
full frozen compatibility contract  = BLOCKED by breaker E3 false positive
```

No production surface outside the handoff was modified to force a green result.
