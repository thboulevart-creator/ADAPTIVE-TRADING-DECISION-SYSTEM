# Q-RM-12 — TEST-FIRST EXECUTABLE COMPATIBILITY — PERSISTED-HEAD FINAL RED RE-BREAK

**Date:** 2026-09-20  
**Qualified breaker HEAD:** `5733f7d3c213eb73056c8b8b8f3addd95a25a584`

## Final qualified identities

```text
breaker
breakers/native_bi5_qrm12_compatibility_breaker.py
blob = 967ab86d517cc8736344bb27154641eb9bac7996

workflow
.github/workflows/native-bi5-qrm12-compatibility-preimplementation.yml
blob = 76bfe3ccaf7cf2fbb359e33d9b5a737709ea22da
```

Frozen governed formalization:

```text
qrm12_postseal_f_o_handoff_formalization_candidate_2026-09-19.md
= a1f1c0edf6f45fd96620e3f2274cc9da0214e3f7

qrm12_postseal_f_o_handoff_persisted_head_rebreak_2026-09-19.md
= 408074e0480ba101368ba219ad50624567ab28e5
```

## Executed evidence

Workflow:

`Native BI5 Q-RM-12 Compatibility Preimplementation RED`

Run:

`35497152042`

Job:

`106042122886`

```text
persisted HEAD / hash locks     PASS
future V0.2 surfaces absent     PASS
qualification environment       PASS
pytest collection               70 tests / PASS
breaker execution               70 failed — EXPECTED RED
unexpected failure causes       0
clean worktree                  PASS
```

All 70 failures are breaker-controlled missing-future-surface outcomes.

No raw import exception or unrelated failure remains.

## Preserved qualified identities

```text
I_A V0.1 source     098040812de654a9c5e4f9961f4a26b2ba959adf
I_B V0.1 source     25fadd36761616e89a21964201b3bfa3c7349ea4
F source            199b07929fe8ec40d719b001b0321d1f26c8faab
O source            219b22bc92855c24eef3a7abb08e177644d05c76

I_A V0.1 breaker    64d3a391e1b5cb5aecfdf926551acd3ee5f0d7dd
I_B V0.1 breaker    d1a305e3b9ae813e891b34522e3a12bb6bc8ac34
F frozen breaker    3d9eb75c2f4e988c984da67af0af344d3dc24148
F adversarial       c4c499d5e76e15a8fdcaeb91dde80beadad6487a
O frozen breaker    9e1d897329a15f8b26172558b6579d61d9ba3820
O adversarial       255ff9f02d206815638b5e63e92546e647e826e4
```

## Verdict

```text
Q-RM-12 TEST-FIRST EXECUTABLE COMPATIBILITY BREAKER / HARNESS = PASS
```

Scope:

```text
test-first harness PASS
production compatibility implementations ABSENT
Q-RM-12 runtime ABSENT
Q-RM-12 executable/global gate BLOCKED
```

No acquisition, BI5 processing, backtest or trading execution is authorized by this result.
