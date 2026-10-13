# AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-GREEN-R1 — SYNTHETIC GREEN QUALIFICATION V0.1

## Terminal result and authority

```text
DECISION = HUMAN_ADOPTED_AND_EXECUTION_AUTHORIZED
CONTROL_ID = AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-GREEN-R1
R1_CR1_GREEN_R1 = PASS_SYNTHETIC_GREEN_QUALIFIED
SCOPE = ISOLATED_SYNTHETIC_CONTRACT_VALIDATOR_ONLY
WINDOWS_CAMPAIGN = FORBIDDEN
WINDOWS_WORKERS_LAUNCHED = 0
REAL_JFOREX_READ = FORBIDDEN
FC01_REAL_MEMORY_SAFETY = NOT_QUALIFIED
FORCE = FALSE
FAIL_CLOSED = TRUE
STOP_AFTER_R1_CR1_GREEN_R1 = MANDATORY
```

This PASS is **only** evidence that an isolated deterministic validator satisfies synthetic contract tests. The result does **not** independently qualify Windows Job Objects, process-tree membership/exit observations, JForex, FC01 memory safety, real data or trading.

## P0 — Canonical and protected readiness

Local and GitHub canonical HEAD: `6873a98c510f6b7650b0221711c5fb8844c1dfef`; TREE: `f147156083780d5a0e807497144eafa9e03dda2d`; branch: `integration/system-v1`. No tracked changes at P0. Protected FC01 Git blob `44ccaeafdd22cede207fef6038e5c747ff5d1454`, E1 blob `2dcacfde5fdf9b39ce0c9647c4413f2d2fc67a0b`. No prior GREEN files existed. Unrelated untracked tests were preserved.

The original RED-CR2 source hashes remain unchanged: oracle `2335423d1afe32bb9985a8a58331e3bd69ccdb811ac222cdfc197e47f3801aee`, test `cb58f8f36cb7a88ffa21ca7bbd027fa945990f582e83663313077bb43338d980`. Earlier original RED test `65cb60153e6a7458adce0373ad51d95e84c3c4fb84ca19e2843dceb8a8944282`; historical adapter `6260021b5e1259677413c341587de92d71168e96ce2d2abc5b51446434fa2c85`.

## P1 — Test-first RED, before GREEN implementation

The new independent GREEN contract test file was created and frozen, SHA256 `15e93467e251987991210e0e9f2dabcab08d82b27a5e59cdd6f7d5d893353b9f`. Executed against the original frozen legacy adapter before creating `green_r1/validator.py`:

- **44 collected, 44 assertion failures, 0 collection errors, pytest exit 1.**
- RED raw SHA256 `ab5919366d7961965235b88e264c9a22d50c8e0e96502f01124c4ca2bd996f84`.
- RED JUnit SHA256 `835c8f85769dc567fcea1954ea4bb3a5f409f8ff717396eccf474d8ab48543a7`.
- Test-first freeze file SHA256 `1de7eab1c594b99979ac1310b28f4f133d4c271c74a6f776f133b938bbae5399`.

These are behavioral expectation failures, not missing imports or Windows process errors.

## P2 — Isolated GREEN construction

The new pure-Python synthetic contract validator `tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/green_r1/validator.py` was created after P1 freeze; final SHA256 `8092c558370130acd9eb16b1c3d1cfed209ff0b8b6f7e78f6a02354c2fc7f0e1`.

It enforces (1) identity and inventory consistency; (2) complete per-member classification including synthetic transitive descendants; (3) absence proof dependent on full classification and provenance; (4) exit and creation-identity matching; (5) receipt consistency and fail-closed normalization. Each result is unconditionally labeled `evidence_class=SYNTHETIC_CONTRACT`, `independent_windows_evidence=False`, `production_qualification=False`. No Windows API or production code is integrated.

The separately written independent adversarial suite initially reported **12 tests, 8 failures, 4 passes, 0 errors** against the preliminary GREEN. Those eight gaps were corrected strictly in the new isolated GREEN source. Original RED sources were not modified.

## P3 — Independent synthetic qualification and non-regressions

Final captured executions:

| Suite | Tests | Pass | Fail | Error | Meaning |
|---|---:|---:|---:|---:|---|
| GREEN 12 JM + 32 initial adversarial + 12 independent adversarial | 56 | 56 | 0 | 0 | GREEN contract satisfied, synthetic |
| RED-CR2 oracle non-regression | 12 | 12 | 0 | 0 | Previous RED oracle classification unchanged |
| Original pre-CR2 RED non-regression | 12 | 1 | 11 | 0 | Original mixed result reproduced, not retroactively promoted |

The GREEN suite does not treat a manually supplied boolean or marker as independent Windows process evidence. Tests cover swapped or recycled process identities, missing member provenance, missing job membership evidence, unexpected child marker type, duplicate identities, post-termination activity, parent misbinding, and indirect descendants.

The outcomes were captured using Python 3.12 / pytest without any Windows synthetic scenario worker launch, JForex connection or external network dependency.

## P4 — Immutable forensic evidence (SHA256)

| Path | SHA-256 |
|---|---|
| `tests/test_fc01_f03_cr2_cr1_m2_r1_cr2_cr1_r1_cr1_green_r1_contract.py` | `15e93467e251987991210e0e9f2dabcab08d82b27a5e59cdd6f7d5d893353b9f` |
| `tests/test_fc01_f03_cr2_cr1_m2_r1_cr2_cr1_r1_cr1_green_r1_independent.py` | `744486cd60e5965e4929fee4019caaa40f6b1fd20d528a18d36075e13ba81e95` |
| `tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/green_r1/validator.py` | `8092c558370130acd9eb16b1c3d1cfed209ff0b8b6f7e78f6a02354c2fc7f0e1` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-GREEN-R1-P1-TEST-FIRST-FREEZE-V0.1.json` | `1de7eab1c594b99979ac1310b28f4f133d4c271c74a6f776f133b938bbae5399` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-GREEN-R1-P1-TEST-FIRST-RED-RAW-V0.1.txt` | `ab5919366d7961965235b88e264c9a22d50c8e0e96502f01124c4ca2bd996f84` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-GREEN-R1-P1-TEST-FIRST-RED-JUNIT-V0.1.xml` | `835c8f85769dc567fcea1954ea4bb3a5f409f8ff717396eccf474d8ab48543a7` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-GREEN-R1-P3-ADVERSARIAL-INITIAL-RED-RAW-V0.1.txt` | `73c55f7d8c1e7e2a3e2e343553d66ab300ca4dad7776d19f58af2b0b9c1b9bbf` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-GREEN-R1-P3-ADVERSARIAL-INITIAL-RED-JUNIT-V0.1.xml` | `758c5a31dc91a7301fc90590d2a22cc16bfb55b58dc4944f1e1a9de77619f589` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-GREEN-R1-P3-GREEN-RAW-V0.1.txt` | `b0ae3484d53a38bb4ba6c5b6b3000fea144c9142c7a35a5d10d5c70c70965618` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-GREEN-R1-P3-GREEN-JUNIT-V0.1.xml` | `f6e1afddea0aa0c21c307e85e2c6ab6de32817d3dabbf89fce3c9b43f2ce7ab3` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-GREEN-R1-P3-RED-CR2-NONREGRESSION-RAW-V0.1.txt` | `24b87ebb54224e95eb439459c790fe53f2c1a4bbd050d7ce0a8ebe39009d7984` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-GREEN-R1-P3-RED-CR2-NONREGRESSION-JUNIT-V0.1.xml` | `fa8a82fabe1f1a5409823991a094ce33cbdbcbbf6bdb780d67514e5add33fec7` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-GREEN-R1-P3-ORIGINAL-RED-REGRESSION-RAW-V0.1.txt` | `6b3cc7f356dadc9537162fd913dbe2fd7e79ef079653a148fd0c08d64e3ce555` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-GREEN-R1-P3-ORIGINAL-RED-REGRESSION-JUNIT-V0.1.xml` | `e5be6345ba14a7bd4faf1d050adf656a2223bdff06109fb2306a8826030161b0` |

The raw pytest/JUnit evidence has been retained byte-for-byte, even when its whitespace does not pass the source-code formatting check. The source-code and authored report files are subject to separate whitespace verification. No previously frozen evidence is overwritten.

## Mandatory authority firewall

```text
R1_CR1_GREEN_R1 = PASS_SYNTHETIC_GREEN_QUALIFIED
INDEPENDENT_WINDOWS_EVIDENCE = NOT_QUALIFIED
WINDOWS_INTERNAL_ROOT_CAUSE = NOT_PROVEN
FC01_REAL_MEMORY_SAFETY = NOT_QUALIFIED
WINDOWS_CAMPAIGN = NOT_AUTHORIZED
WINDOWS_WORKERS = 0
JFOREX_LOGIN = 0
JFOREX_CONNECT = 0
PROVIDER_REQUESTS = 0
REAL_HISTORY_READ = 0
FC01_E1_M2_MUTATION = FALSE
HISTORICAL_TEST_RECEIPT_MUTATION = FALSE
READ_A_RETRY = FALSE
READ_B = FALSE
B12 = CLOSED
TRADING = FALSE
ORDERS = FALSE
CAPITAL = FALSE
FORCE = FALSE
FAIL_CLOSED = TRUE
STOP_AFTER_R1_CR1_GREEN_R1 = MANDATORY
```

**NEXT**: separate human adjudication before even preparing Windows evidence readiness. This PASS authorizes no worker, replay, runtime cutover, JForex access or downstream gate promotion.
