# V3.3 — Adversarial audit package

## Objective
Audit `download_ticks_v3_3.ps1` as an executable data-acquisition component. The goal is NOT to obtain a PASS by opinion. The goal is to identify every defect that could invalidate RAW tick acquisition, restart safety, integrity, reproducibility, or downstream backtests.

## Required evidence rule
A PASS is valid only when supported by executable, reproducible evidence. A static observation is not a runtime PASS. A failed/blocked command followed by manually printed PASS labels is invalid evidence.

## Known facts to challenge
- Instrument: `usatechidxusd` (Dukascopy USATECH.IDX/USD).
- Timeframe: `tick`.
- Volumes enabled.
- Expected canonical columns: `timestamp,askPrice,bidPrice,askVolume,bidVolume`.
- RAW is intended to be immutable after acceptance.
- Daily partitions are intended: `YYYY/MM/YYYY-MM-DD.csv`.
- Expected terminal statuses include `VALID`, `NO_DATA`, `FAILED`, `INTEGRITY_FAILURE`, `BLOCKED`, `SKIP`.
- Dukascopy `askVolume` / `bidVolume` must NOT be represented as centralized exchange executed volume.

## Known defects already observed — do not merely repeat them
1. V3.3 previously contained an idempotence defect where `SKIP` could mask the historical `VALID` record. The intended correction is `Get-LatestValidManifestRecord` and the invariant `VALID -> SKIP -> SKIP -> ...`.
2. V3.3 previously failed in the real behavioral test because `Get-RawPath` used `New-Item -LiteralPath`, which is unsupported in the target PowerShell environment. A local targeted fix changed that specific `New-Item` parameter to `-Path` and passed syntax + targeted static checks.
3. The previous real behavioral gate did NOT pass: the runner failed before download, produced zero RAW files and zero manifest records. Any later PASS labels printed after `throw` are invalid evidence.

## Audit tasks
### A. Static/source audit
Inspect the complete V3.3 source and report:
- control-flow correctness;
- exact schema enforcement;
- tick-only enforcement;
- timestamp type, bounds and monotonicity;
- price finiteness and bid/ask invariants;
- volume validity;
- single-output-file enforcement;
- daily partition correctness;
- no unintended overwrite;
- manifest semantics;
- `VALID` proof semantics;
- idempotence;
- restart safety;
- failure classification;
- SHA-256 and size integrity;
- provenance and runner hash;
- dependency/version pinning;
- deterministic process exit codes;
- PowerShell compatibility issues, especially parameter support;
- hidden assumptions that would fail at 10-year scale.

### B. Adversarial falsification
Actively try to break these invariants:
- `VALID -> SKIP -> SKIP`;
- RAW hash unchanged across skips;
- existing RAW without VALID cannot be silently accepted;
- `NO_DATA` does not create fake VALID;
- one malformed tick causes rejection;
- out-of-range timestamp causes rejection;
- non-monotonic timestamps cause rejection;
- invalid volume causes rejection;
- multiple CSV outputs are rejected;
- download failure cannot become VALID;
- post-copy corruption cannot become VALID;
- rerun after failure is deterministic and recoverable;
- a stale/old manifest record cannot authorize a new RAW file;
- date-boundary leakage cannot enter a daily partition.

### C. Runtime gate
If execution is possible, use an autonomous `.ps1` test harness, not a long interactive paste. The harness MUST stop on assertion failure and MUST derive the final verdict from actual exit status and observed filesystem/manifest state.

Minimum runtime sequence:
1. isolated test root;
2. run #1 on a known trading day -> require `VALID`;
3. record RAW SHA-256 and manifest state;
4. run #2 -> require exactly one new `SKIP`, preserve the original `VALID`, preserve SHA;
5. run #3 -> require another `SKIP`, preserve `VALID`, preserve SHA;
6. test a no-data day -> require `NO_DATA`;
7. test failure/recovery semantics if feasible.

Do not run a 10-year acquisition as part of this audit.

## Verdict format
For every finding use exactly one of:
- `PASS` — executable evidence exists;
- `FAIL` — a reproducible violation exists;
- `BLOCKED` — the control cannot be executed/proven with the available environment/evidence.

Distinguish explicitly between:
- current violation;
- architectural exposure;
- absence of proof.

## Deliverable
Return:
1. Executive verdict.
2. Findings ordered CRITICAL / HIGH / MEDIUM / LOW.
3. Exact file/line/function evidence.
4. Minimal corrective action for each FAIL/BLOCKED item.
5. Runtime tests actually executed, with raw outputs or precise observations.
6. What would be required for a final PASS.

Do NOT modify the source under audit. This package is an adversarial review artifact only.
