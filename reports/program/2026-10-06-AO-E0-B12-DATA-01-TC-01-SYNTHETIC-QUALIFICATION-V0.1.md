# AO-E0-B12-DATA-01-TC-01 — SYNTHETIC QUALIFICATION V0.1

STATUS = QUALIFIED

SCOPE = COUNT-ONLY SYNTHETIC + DOCUMENTARY ONLY

## Canonical identity

HEAD = 3fc29fd691ccee43fdb808ae017484f6adcb41f1

TREE = 98d3238e1e3b5f4e14c05babafc9691791c11407

PARENT = 247b74977c5e6b1d907865ea501d900c7c8cc0b7

## Canonical CI

WORKFLOW = AO-E0 DATA-01 TC-01 Synthetic Qualification

RUN = 37521141490

JOB = 112466526335

CONCLUSION = SUCCESS

TC-01 = 44 / 44 PASS

E1-04 REGRESSION = 22 / 22 PASS

E1-05 REGRESSION = 33 / 33 PASS

TOTAL = 99 / 99 PASS

AUTHORITY FIREWALL = PASS

CLEAN WORKTREE = PASS

## Qualified claim

TC-01 is qualified only as a deterministic count-only machine on synthetic fixtures.

The qualified surface is limited to:
- cumulative closed-trade count;
- terminal-threshold reached true/false;
- exact terminal decision time if reached;
- bound-input identity digest;
- count-trace digest.

The runtime does not import the existing E1-04/E1-05 execution path, PIPE-01, or OWNER-02. The independent reference is implemented separately from the primary runtime.

The synthetic qualification covers exact transition semantics, reversal/flat/open/hold behavior, warmup and continuity handling, structural execution admissibility, count accumulation, threshold crossing, deterministic replay, primary/reference parity, output-surface restrictions, and authority-firewall restrictions.

## Performance firewall

REAL_TC01_FORWARD_READ = FALSE

PERFORMANCE_BEARING_READ = FALSE

OOS_PERFORMANCE_CONSUMPTION = FALSE

HUMAN_FORWARD_PRICE_OBSERVATION = FALSE

PNL / RETURNS / EXPECTANCY / CI / SUPPORT / REFUTE / INCONCLUSIVE = NOT EXPOSED

B12 = CLOSED

REAL_AO_E0_EXECUTION = FALSE

REAL_SMF_EXECUTION = FALSE

TRADING / BROKER / CAPITAL = NOT AUTHORIZED

## Repository-wide CI observation

The TC-01 qualification workflow is SUCCESS.

Two pre-existing broad historical guards also ran on the same commit:
- P0.4 run 37521141249 = FAILURE;
- P0.6 run 37521141278 = FAILURE.

Both fail on the same nine BERD02 .bi5 evidence files under evidence/berd02/gha_run_35533153289/bodies.

Those nine files were verified to already exist in parent commit 247b74977c5e6b1d907865ea501d900c7c8cc0b7 and were not introduced by the TC-01 candidate.

Therefore this record does not claim REPOSITORY_GLOBAL_CI = PASS. It records the P0 failures separately and limits the qualification verdict to the exact TC-01 synthetic claim.

## Verdict

TC01_SYNTHETIC_QUALIFICATION = QUALIFIED

This does not authorize the first real count-only forward read.

STOP = HUMAN_DECISION_REQUIRED
