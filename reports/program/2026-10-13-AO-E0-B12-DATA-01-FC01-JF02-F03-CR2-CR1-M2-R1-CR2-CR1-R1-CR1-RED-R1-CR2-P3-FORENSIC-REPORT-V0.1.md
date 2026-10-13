# AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-RED-R1-CR2 — SYNTHETIC RED REQUALIFICATION V0.1

## Human authorization and terminal decision

```text
HUMAN_DECISION = HUMAN_ADOPTED_AND_EXECUTION_AUTHORIZED
CONTROL_ID = AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-RED-R1-CR2
TERMINAL_DECISION = PASS_RED_BEHAVIORALLY_QUALIFIED
QUALIFICATION_SCOPE = SYNTHETIC_ORACLE_ONLY
P0_FRESH_READINESS = PASS
P1_ORACLE_AMENDMENT = PASS
P2_SYNTHETIC_RED_REQUALIFICATION = PASS
P3_FORENSIC_PERSISTENCE = PENDING_VERIFIED_GITHUB_COMMIT
GREEN_IMPLEMENTATION = FORBIDDEN
WINDOWS_CAMPAIGN = FORBIDDEN
NEW_WINDOWS_WORKERS = 0
FORCE = FALSE
FAIL_CLOSED = TRUE
STOP_AFTER_R1_CR1_RED_R1_CR2 = MANDATORY
```

**Interpretation:** All 12 new CR2 oracle tests passed because their assertions demonstrated **existing legacy adapter behavior and deficiencies**. This does not say the original validator is GREEN. It does not mean independent Windows evidence has been obtained. In the legacy adapter's observed case matrix, **5** cases return `PASS` and **7** return `BLOCKED`. Their RED gap classes were separately captured.

## P0 canonical read-only gate

Canonical branch: `integration/system-v1`.

Before mutation the local and remote HEAD were both `400d008b2ec8624c4811e27f8bb70f3e3fc5b0c9`; TREE `5a02180fde7684b80f7462b7ee348e678ae2232b`. Tracked diff and staged diff were empty. Protected FC01 blob `44ccaeafdd22cede207fef6038e5c747ff5d1454`; E1 blob `2dcacfde5fdf9b39ce0c9647c4413f2d2fc67a0b`.

Historical sources frozen and unchanged: original 12-test file SHA256 `65cb60153e6a7458adce0373ad51d95e84c3c4fb84ca19e2843dceb8a8944282`; original historical RED adapter SHA256 `6260021b5e1259677413c341587de92d71168e96ce2d2abc5b51446434fa2c85`.

Original RED receipt remains `INCONCLUSIVE` (1/12 pass, 11/12 failed assertions). Those historical results are not promoted retroactively. Old Windows campaign remains `BLOCKED` (4/13 historically spent).

## P1 Oracle corrections, separately versioned

New CR2-only files:
- `tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/red_r1_cr2_oracle.py`: source-frozen synthetic fixture and historical adapter observations; explicit `LEGACY_ADAPTER`, `SYNTHETIC_CONTRACT`, `WINDOWS_EVIDENCE=False`.
- `tests/test_fc01_f03_cr2_cr1_m2_r1_cr2_cr1_r1_cr1_red_r1_cr2.py`: exactly 12 separate tests, explicitly demonstrating one RED case each.
- `tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/red_r1_cr2_capture.py`: pure Python capture of the 12-case observation matrix without file mutation or worker starts.

No original tests or original adapter were modified; the CR2 oracles do not attempt a functional correction of production behavior.

## P2 Qualifier — observed results and bounded semantics

Python 3.12 pytest normal execution from repository root with `-p no:cacheprovider`; exit code `0`; JUnit reports `tests=12,failures=0,errors=0`.

| Test | Legacy status | Bounded observed gap | Adjudication |
|---|---|---|---|
| JM01 | PASS | EXISTING_POSITIVE_CONTROL | CR2 oracle PASS; legacy gap NONE (positive control) |
| JM02 | BLOCKED | SYNTHETIC_FALSE_BLOCK | CR2 oracle PASS; legacy gap observed or classified |
| JM03 | BLOCKED | REASON_SPECIFICITY | CR2 oracle PASS; legacy gap observed or classified |
| JM04 | BLOCKED | CROSS_FIELD_CONSISTENCY | CR2 oracle PASS; legacy gap observed or classified |
| JM05 | PASS | INPUT_TRANSPORT_OMISSION | CR2 oracle PASS; legacy gap observed or classified |
| JM06 | BLOCKED | REASON_AND_TRANSPORT | CR2 oracle PASS; legacy gap observed or classified |
| JM07 | BLOCKED | REASON_SPECIFICITY | CR2 oracle PASS; legacy gap observed or classified |
| JM08 | PASS | INPUT_TRANSPORT_OMISSION | CR2 oracle PASS; legacy gap observed or classified |
| JM09 | PASS | ABSENCE_PROOF_SEMANTICS | CR2 oracle PASS; legacy gap observed or classified |
| JM10 | BLOCKED | SYNTHETIC_FALSE_BLOCK | CR2 oracle PASS; legacy gap observed or classified |
| JM11 | PASS | INPUT_TRANSPORT_OMISSION | CR2 oracle PASS; legacy gap observed or classified |
| JM12 | BLOCKED | SYNTHETIC_FALSE_BLOCK | CR2 oracle PASS; legacy gap observed or classified |

Explicit five targeted clarifications:

- **JM03:** Unclassified member is already blocked but does not emit `UNCLASSIFIED_JOB_MEMBER`.
- **JM04:** An invalid creation identity is blocked, yet the legacy adapter still presents `descendant_absence_proven=True`. This is a cross-field inconsistency, not only a reason-code difference.
- **JM06:** The fixture's claimed absence with synthetic verified parent data is not forwarded to the historical adapter, which blocks under `DESCENDANT_ABSENCE_UNPROVEN` but cannot emit `CONTRADICTORY_DESCENDANT_ABSENCE`. No Windows lineage is proven.
- **JM07:** Unverified termination is blocked, but `MEMBER_TERMINATION_NOT_VERIFIED` is absent and previous diagnostics remain required.
- **JM09:** `ENUMERATED_EMPTY` is the sole favorable absence evidence; provenance is omitted by the legacy adapter. It cannot be promoted to `ENUMERATED_MEMBERS_ALL_CLASSIFIED_NO_DESCENDANTS`.

Preserved criteria for JM01, JM02, JM05, JM08, JM10, JM11 and JM12 were each checked. Input transport omissions in JM05, JM08, and JM11 are **properties of the synthetic adapter**, not independently demonstrated Windows acceptance. Fixtures' `parent_identity_verified` and `external_lineage_proven` booleans remain synthetic declarations, not forensic proof of parenthood.

## P2 evidence (immutable at persistence)

| Evidence | SHA-256 |
|---|---|
| `tests/test_fc01_f03_cr2_cr1_m2_r1_cr2_cr1_r1_cr1_red_r1_cr2.py` | `cb58f8f36cb7a88ffa21ca7bbd027fa945990f582e83663313077bb43338d980` |
| `tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/red_r1_cr2_oracle.py` | `2335423d1afe32bb9985a8a58331e3bd69ccdb811ac222cdfc197e47f3801aee` |
| `tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/red_r1_cr2_capture.py` | `fee4394d1dd510e0c32b8c12f84354b1af191c62d5aa0633b90a4c6b700e548b` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-RED-R1-CR2-P2-RAW-PYTEST-V0.1.txt` | `d6a8eb2e1d0aa18f1e82ad1e69493710ad477ff16194d73eb1db1fd9c79ce7ca` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-RED-R1-CR2-P2-JUNIT-V0.1.xml` | `e160ca4ec2fb0df6e00e15de37e92f668fecefbb4c19f3b0bfe023ecdd90cc14` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-RED-R1-CR2-P2-CASE-MATRIX-V0.1.json` | `c8595dcb979e3847f41f45cd4fc71f147c8fdb7c67c377794caddc1a6272430a` |

The JUnit result, raw pytest output, and case-matrix JSON were captured separately. Every case in the matrix specifies its evidence class and retains the old validator's observed status and violations.

## Strict firewall and next authority

```text
R1_CR1_RED_R1_CR2 = PASS_RED_BEHAVIORALLY_QUALIFIED
SCOPE = SYNTHETIC_ONLY
LEGACY_RUNTIME_FIXED = FALSE
INDEPENDENT_WINDOWS_EVIDENCE = FALSE
FC01_REAL_MEMORY_SAFETY = NOT_QUALIFIED
HISTORICAL_RED = INCONCLUSIVE_UNCHANGED
GREEN_IMPLEMENTATION = NOT_AUTHORIZED
WINDOWS_CAMPAIGN = FORBIDDEN
WORKER_BUDGET = 0
PROVIDER_REQUESTS = 0
JFOREX_CONNECT = 0
REAL_HISTORY_READ = 0
READ_A_RETRY = FALSE
READ_B = FALSE
B12 = CLOSED
FC01_E1_M2_MUTATION = FALSE
HISTORY_REWRITE = FALSE
FORCE = FALSE
FAIL_CLOSED = TRUE
STOP = APPLIED_ON_SUCCESSFUL_EVIDENCE_PERSISTENCE
```

**NEXT**: a separate human gate for isolated functional GREEN and subsequent Windows evidence preparation. This receipt grants neither one automatically.
