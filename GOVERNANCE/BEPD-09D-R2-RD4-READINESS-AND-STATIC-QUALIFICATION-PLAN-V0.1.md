# BEPD-09D-R2-RD4 — H Readiness and static qualification plan V0.1

Scope: **documentary and static only**, source GitHub. No executable, no rerun, no test/scoring, no real event observation. Frozen parent: `5ae2bb0fd80d529e921def8ebcace860df8447eb` / `0ec38a3a56053ff3fb0da9f06640351491a1dc9f`.

## Requirements and qualification gates
| Gate | Basis | Status |
|---|---|---|
| Identity of repository/branch/parent | Fresh branch read plus frozen RD3 receipt | PASS at inspection checkpoint (must recheck prewrite) |
| RD2/RD3 preserved | Git blob SHA frozen | PASS (metadata/static source reads) |
| 259-week C1 identity | exact 259/259 IDs in partition vs calendar binding; 7-day sequence | PASS documentary |
| 260 vs 259 reconciliation | source manifest 260 weeks from 2021-05-31; C1 starts 2021-06-07 | PASS **for documented boundaries only**; no full run 260-ID source content read |
| Fold plan | B1..B5 cumulatively train, B2..B6 current tests | PASS documentary |
| Candidate-B numeric identity and gates | frozen RD2 accept/tau/solver contracts | PASS documentary |
| Exact training-only guarded input boundary | legacy harness reads whole ledger; future reader not designed/qualified | BLOCKED |
| Fold-scoped response read and trusted source digest | physical full-ledger read would expose protected bytes | BLOCKED |
| Fail-closed separation detector unknown/error | current `build_packet` may map exception to false | BLOCKED |
| Training-only reference comparison | existing 2e-5 concerns predictions/scoring, not train fit coefficient parity | BLOCKED |
| Deterministic synthetic adapter qualification | implementation and workflow expressly forbidden under RD4 | BLOCKED, NEXT AUTHORIZATION |
| Time and resource budget | upper bound 10 primary+10 reference proposed, no exact time/cost budget adopted | BLOCKED |
| Current RD4 real execution | no authority | NOT_AUTHORIZED |

## Pre-execution qualification plan (for separate future authority)
1. Human adjudicate four blocking material contract choices: physical/logical response isolation; unknown separation status; reference parity; exact budgets and fail-stop order.
2. Implement a **new isolated training-only adapter**, not modifying the RD3 runtime and not activating historic `run_protocol`.
3. Test-first synthetic RED: leak current-fold test label, wrong fold, identity drift, separation LP error/unknown, invalid rank, nonfinite, invalid class labels, mismatch reference, output containing coefficients/metrics, forced retry. Every case MUST FAIL CLOSED.
4. Synthetic GREEN: exact training fold IDs, 10 primary model-role inputs declared in fixture only, accepted/rejected numerical outcomes according to adopted Candidate B, exact interface binding, equality-boundary TAU gate, deterministic receipt identity, zero test scoring, zero output outside allowlist, parity against preregistered independent reference metric.
5. Verify frozen numeric environment and exact SHA/Git tree, developer and evaluator not conflated; separate external adversarial review if required by broader ATDS governance.
6. Human adjudicate implementation and synthetic qualification separately. **Only afterward** consider human authorization of the smallest controlled training-only real run.
7. Real run must STOP on first disqualifying state; never automatically continue into C1 scientific forward scoring, fresh OOS or trading.

## Current maximum status and stop
`DOCUMENTARILY_PREREGISTERED_AND_STATICALLY_ASSESSED_FOR_HUMAN_ADJUDICATION` with **readiness BLOCKED**. `HUMAN_ADOPTION=PENDING`. No implied `REAL_EXECUTION_READY` or `REAL_EXECUTION_AUTHORIZED`. New adapter or runtime/test/workflow creation is not authorized by RD4.
