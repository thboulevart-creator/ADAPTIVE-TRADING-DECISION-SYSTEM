# SESSION BACKUP — 2026-09-26 — CR1 COMPLETE / CR2 PREFLIGHT NEXT

Repo: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branch: `integration/system-v1`

## Exact CR1 evidence

- 49,694 bytes
- SHA-256 `c7aacf73c175c6af49a4866ad62f1d65c0b46b05fa6cd0dd0def4eb5ce87ba3f`
- Git blob `cd40bf975613d1fa0e6d7277c2850ec87104727e`
- CR1_COMPLETE
- N0_EXPLORATORY_PREVIOUSLY_EXPOSED_CORPUS

## Results

SUPPORTED_N0:
- NY hour
- NY weekday
- absolute RV15 state
- hour-relative RV15 state
- relative tick-density state

NOT_INTERPRETABLE:
- relative spread state — sparse F2 state count 21

REFUTED_N0:
- gap/reopen state
- efficiency state

## Important limits

- no pristine OOS claim
- no strategy/PnL
- no regime labels yet
- no ranking/winner selection
- H02 weekday effect is small and 60m robustness is mixed
- H03 and H04 are overlapping volatility representations; CR2 must not blindly combine/search them

## Next governed action

Create only a bounded CR2 REGIME-CANDIDATE SYNTHESIS PREFLIGHT.

Use only CR1-supported axes.
Do not reopen H05/H07/H08.
Do not perform combinatorial feature search.
