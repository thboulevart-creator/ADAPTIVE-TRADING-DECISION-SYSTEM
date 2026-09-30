# P5-D4 ? BOUNDED OBSERVER LOOP CONTRACT V0.1 ? QUALIFICATION

Date: 2026-09-30

## Scope

This qualification covers the P5-D4 contract frontier only.

It does not create, modify, or execute any P5-D4 runtime. It does not authorize repeated polling, sleep/timer behavior, a daemon, Windows startup, Scheduled Task, Windows Service, real-Vault mutation, automatic publication, implicit Stage A/Stage B authority, P5-E, or P6.

## Source authority

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Branch: `feat/obsidian-projection-p5d4-bounded-observer-loop-contract-v0.1`
- Contract base HEAD: `2b03c4965c80a5092d4f92eda95ab523731e3e7d`
- Contract commit: `43d9c52976a0d0ff8e397036b31062bababbbc02`
- Breaker test commit: `237c24d2c875a79263180f2f7aa66ab3097311cd`

## Qualified artifacts

- Contract:
  `tools/obsidian_projection/p5d4_bounded_observer_loop_contract_v0_1.json`
- Contract blob:
  `6980de1eb55e49c0c2bd2f91620aeb75640753b6`
- Breaker tests:
  `tests/obsidian_projection/test_p5d4_bounded_observer_loop_contract_v0_1.py`
- Breaker-test blob:
  `7e572e90cc331a316b58bc3e69970bed9ac40507`

## Predecessor pins

The contract pins the existing qualified P5-D1/P5-D2/P5-D3 authorities and does not redefine them:

- P5-D1 observer core contract: `a20999ae991e07447e25ecd1592964f2d333449b`
- P5-D2 one-shot contract: `5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3`
- P5-D2 observer tick: `fd212f61ec38332b677110f40265638af55a73e2`
- P5-D3D finite evaluator contract: `b6c17167875874db30a575be95e8e6aa33d630dd`
- P5-D3D finite evaluator: `bff5f51abbb344c1ccc5e9c669a11cf0e26c2562`
- P5-D3E sandbox contract: `ae4b1691fae16fcd1616e265a089670b9654db4a`
- P5-D3E verifier: `bd7f63b08432a53eaff5deeb2147396eb60d723f`
- P5-D3F handoff contract: `64744325251db350d26c0269090ce62d5fa5f2e8`
- P5-D3F handoff runtime: `23a4cc69b3b9f6fab1a6d77bed0247fce9b69c60`
- P5-D3G live-publication contract: `64997ddd9977229961387f66af4de356c045c0ac`
- P5-D3G live-publication runtime: `956ccb7274cea366b1a414df5a9239cbf580e3bf`
- P5-D3G Stage-B gate contract: `c5c7fbb52f3dd2e3d3f5d1c1bbdc1069e2dabead`
- P5-D3G Stage-B prestate amendment: `441fea40d33aa85dcfc6305d4d32cef39c42388e`
- P5-D3G Stage-B runtime: `077ea7a428f90d64122f15fe6b52f342f329f7b6`

## Six P5-D4 additions closed by the contract

1. Bounded loop envelope.
2. Durable observer-state checkpoint outside the Vault and canonical repository.
3. Append-only hash-chained observer event log.
4. FIFO, unique, bounded queue-capacity policy with no silent loss or coalescing in V0.1.
5. Single-instance ownership with fail-closed stale/ambiguous-lock behavior.
6. Restart/reconciliation protocol binding GitHub source authority, verified physical CURRENT, the derived checkpoint, and append-only evidence.

## Authority decision

The contract preserves:

`LOOP AUTHORITY != PROMOTION AUTHORITY`

P5-D2 `one_shot_tick()` remains the only semantic observer-state mutation authority.

P5-D4 may later orchestrate bounded observation and finite evaluation, but a qualified candidate without separate promotion authority terminates at:

`PROMOTION_AUTHORITY_REQUIRED`

P5-D4 V0.1 does not authorize automatic P5-D3F/P5-D3G invocation.

## Bootstrap decision

When no P5-D4 checkpoint/log exists and no physical CURRENT exists, runtime may later initialize the canonical P5-D2 initial state.

When no P5-D4 checkpoint/log exists but a verified physical CURRENT already exists, direct state assignment is forbidden. The contract requires evidence reconstruction starting from `make_initial_state()`, using only P5-D2 `one_shot_tick()` semantic transitions bound to matching verified P5-D3G physical and logical receipts.

This is a contract requirement only; no bootstrap runtime is implemented by this qualification.

## Breaker result

P5-D4 contract breaker suite:

- Tests: 29
- Result: PASS
- Runtime surface check: PASS ? no `tools/obsidian_projection/p5d4*.py` runtime exists.

Breaker families cover at minimum:

- finite loop bounds;
- event/sequence monotonicity;
- checkpoint/log commit ordering and digest integrity;
- crash-window reconciliation;
- queue overflow/drop/reorder/direct mutation;
- active-candidate retargeting;
- double-runner and stale-lock behavior;
- restart inconsistencies and replay;
- existing-CURRENT bootstrap;
- remote SAME/network/non-fast-forward/unknown behavior;
- BLOCKED vs REJECTED preservation;
- qualified P5-D3 reuse;
- promotion-authority leakage;
- GitHub/canonical-worktree/Vault/human-view/.obsidian boundaries;
- daemon/timer/startup/scheduled-task/service prohibition;
- P5-E/P6 authority leakage.

## Directly affected predecessor regression

Executed modules:

- P5-D4 bounded observer loop contract V0.1
- P5-D1 continuous observer core contract
- P5-D2 one-shot observer tick contract
- P5-D3A candidate evaluation contract
- P5-D3D finite candidate evaluator contract
- P5-D3G live-publication transaction contract
- P5-D3F promotion-handoff contract

Result:

`Ran 164 tests ? OK`

## Qualification verdict

```
P5D4_CONTRACT_PREREGISTRATION = PASS
P5D4_PREDECESSOR_PINS         = PASS
P5D4_BREAKER_COVERAGE         = PASS
P5D4_CONTRACT_TESTS           = 29 / 29 PASS
DIRECT_PREDECESSOR_REGRESSION = 164 / 164 PASS
P5D4_RUNTIME_CREATED          = FALSE
P5D4_LOOP_EXECUTED            = FALSE
REAL_VAULT_ACCESS_REQUIRED    = FALSE
AUTOMATIC_PROMOTION_AUTHORITY = FALSE
P5E_AUTHORITY                 = FALSE
P6_AUTHORITY                  = FALSE

P5-D4 CONTRACT V0.1           = QUALIFIED
```

## Mandatory stop

The next frontier is:

`P5-D4 ? BOUNDED OBSERVER LOOP RUNTIME IMPLEMENTATION CANDIDATE`

A separate human authorization is required before creating or modifying any P5-D4 runtime.
