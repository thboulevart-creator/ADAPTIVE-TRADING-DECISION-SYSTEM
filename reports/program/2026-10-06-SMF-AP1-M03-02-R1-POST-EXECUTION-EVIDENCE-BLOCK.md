# SMF-AP1-M03-02-R1 — POST-EXECUTION EVIDENCE BLOCK

Status: BLOCKED

Transport correction was qualified. The R1 pre-result freeze was persisted byte-exact before the single real M03 retry.

The single R1 retry did execute M03 and produced a complete method output:
- output status: M03_REAL_EXECUTION_COMPLETE
- output SHA-256: 7d4369cdfab545f0edb94b93ad9d1d1070e6afa35a1000376af55d9c10943a9e
- real AP1↔M03 parity: PASS
- parity PASS comparisons: 1925
- parity FAIL comparisons: 0
- NOT_COMPARABLE: 165
- maximum absolute difference: 0.0
- stderr bytes: 0
- timeout observed: false

However, the PowerShell controller did not retain the target process exit code. The observed exit-code field is null/unknown.

Because the authorization required the real exit code to be preserved and required STOP on an unexpected material evidence gap, the stage is blocked before scientific interpretation. No exit code is inferred or invented.

No second R1 retry is authorized or performed. No AP1 re-execution, backtest, new OOS, paper/live trading, capital use, finding adoption, or strategy validation occurred.

Next frontier: post-execution exit-code evidence-gap adjudication without rerunning M03.
