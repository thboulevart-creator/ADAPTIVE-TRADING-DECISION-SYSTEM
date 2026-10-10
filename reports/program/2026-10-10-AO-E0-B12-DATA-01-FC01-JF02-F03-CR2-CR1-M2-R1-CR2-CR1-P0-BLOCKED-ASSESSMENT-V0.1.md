# HUMAN-AUTHORIZED P0 STATIC AUDIT — F03-CR2-CR1-M2-R1-CR2-CR1 V0.1

## Terminal decision: BLOCKED_NEEDS_SEPARATE_CORRECTION — STOP APPLIED

```text
CONTROL_ID = AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1
STATUS = HUMAN_ADOPTED_AND_EXECUTION_AUTHORIZED
P0_CANONICAL_IDENTITY = PASS_WITH_NONMATERIAL_CONCURRENT_DOC_DRIFT
P0_PROTECTED_SOURCES = PASS
P0_COMPLETE_STATIC_AUDIT = BLOCKED_NEEDS_SEPARATE_CORRECTION
P1_RED = NOT_STARTED
P2_BOOLEAN_CORRECTION = NOT_STARTED
P3_NEW_SYNTHETIC_CAMPAIGN = NOT_STARTED
P4_REGRESSIONS = NOT_STARTED
P5 = BLOCKED_FORENSIC_DOCUMENTATION_ONLY
NEW_CR2_CR1_WORKER_LAUNCHES = 0/13
GITHUB_EXECUTABLE_MUTATION = FALSE
STOP_AFTER_F03_CR2_CR1_M2_R1_CR2_CR1 = APPLIED
```

## Authority and immutable evidence

The user adopted the distinct CR2-CR1 authorization to normalize exactly `"True"`, `"TRUE"`, `"False"`, `"FALSE"` in an **isolated copy**, rejecting all other encodings. The same authorization imposes a **complete static audit of all thirteen scenarios before any worker launch** and orders STOP at P0 if other material discrepancies are found. This report is the result of that mandatory gate. It is not a green qualification and does not adopt another corrective scope.

Reference GitHub branch: `integration/system-v1`. User-adopted reference HEAD `3ca1a27ad1af0f99b7af75eeb19a759af303a2c3`, TREE `3f1017db633d9bd20ee48eee2273a5ab0be0cb74`. During P0 the remote HEAD advanced to `fe25ef8aa75250f1bd72e8ec64187245f9bcc651`, TREE `005229c948fc5552027a9a2ddf78465cd8427703`, via two E1-D3-F2-A1 **documentary-only** additions. The local checkout remained at the authorized HEAD with no staged or modified tracked files. No fast-forward, reset or code mutation was needed for this audit.

Previous CR2 BLOCKED forensic evidence SHA-256: `607a0f2b2585a148940efe28fceee322c54146d2be593f77fb9e81964f4ac6a2`. This and the previous campaign's four launches are strictly historical. They have not been replayed or rewritten.

Protected FC01 Git blob: `44ccaeafdd22cede207fef6038e5c747ff5d1454`. Protected E1 Git blob: `2dcacfde5fdf9b39ce0c9647c4413f2d2fc67a0b`.

## Static material blockers outside the authorized one-line Boolean normalization

### P0-B01 — Tree termination not independently proven

File: `tools/fc01_f03_cr2/m2_r1_cr2/run_single_campaign.py`, lines 120–123 and 136.

For all scenarios other than `child_hang`, `tree_term` is derived from `bool(worker_term)`. Thus the same interpreted worker flag is the source of both asserted worker termination and asserted process-tree termination. Normalizing `"True"` to Boolean `True` would make both fields pass without independent process-tree observation. The validator, `receipt_contract.py`, lines 55–56, checks that both are True but cannot distinguish their underlying provenance.

The CR2-CR1 authorization requires independent termination evidence: worker identity, matching process start time, termination action, verified exit and process-tree state. A Boolean representation fix cannot satisfy that requirement.

```text
P0_B01 = BLOCKED_INDEPENDENT_PROCESS_TREE_EVIDENCE_MISSING
```

### P0-B02 — Crash recovery cannot bind PID to original start identity

Files: `tools/fc01_f03_cr2/m2_r1_cr2/F03CR2SupervisorCR2.cs`, line 124; `tools/fc01_f03_cr2/F03CR2Recovery.cs`, lines 24–26, 57–66, 124–128; `run_single_campaign.py`, lines 120–121 and 205–223.

The original synthetic manifest contains `WORKER_START_TICKS=0`. The recovery component's `WorkerAbsent(pid)` checks a PID and signaled/absent state, not a matching Windows process-start identity. The harness then accepts a successful `ORPHAN_RECOVERED` output as `worker_term`. Consequently, even a valid recovery success is not by itself an independently verified PID+start-time and worker-exit receipt.

The mandatory crash scenario cannot obtain a complete approved termination chain through Boolean normalization alone.

```text
P0_B02 = BLOCKED_CRASH_IDENTITY_PROVENANCE
```

### P0-B03 — Descendant identity is not fully validated

Files: `run_single_campaign.py`, lines 108–110, 122–123, 137–138 and 158; `receipt_contract.py`, line 57.

For the `child_hang` scenario, the harness can record a descendant with `start_filetime_utc=0` if the timestamp is absent or unparseable. It annotates `child_worker_identity_missing`, but the validator only checks that `descendant_identities` is nonempty, not that the descendant's PID/start identity and verified exit are valid and bound together.

This is an independent identity-evidence blocker under the adopted termination hierarchy.

```text
P0_B03 = BLOCKED_DESCENDANT_IDENTITY_VALIDATION
```

### P0-B04 — Pre-existing final file integrity is not independently anchored

Files: `run_single_campaign.py`, lines 62–64, 104, 127 and 164; `receipt_contract.py`, lines 20–24.

The sentinel scenario pre-creates `FROZEN_SENTINEL`. Its post-execution `final_sha256` is computed from the current final file, and the expected digest passed to the validator is **the same current computed digest**. This verifies internal consistency with that readback, not preservation of an independently frozen preexisting sentinel's bytes across the collision. Thus the required no-overwrite gate would lack a separate pre-execution digest comparison.

```text
P0_B04 = BLOCKED_NO_OVERWRITE_BASELINE_MISSING
```

## All thirteen preregistered scenario paths — P0 status

| Scenario path | Runs | Static decision |
|---|---:|---|
| Normal A, normal B | 2 | Process-tree evidence aliases worker flag (P0-B01) |
| Java OOM | 1 | Process-tree evidence aliases worker flag (P0-B01) |
| Timeout | 1 | Known `True`/ `TRUE` defect plus P0-B01 |
| Timeout with descendant | 1 | Missing strict descendant start identity verification (P0-B03) |
| Preexisting final collision | 1 | No independent before/after sentinel integrity baseline (P0-B04) |
| Forced supervisor crash/recovery | 1 | Manifest/recovery identity gap (P0-B02) |
| Six-way publication race | 6 | Shares one intended final directory, but tree evidence aliases worker flag (P0-B01) |
| **Total** | **13** | **Not statically admissible for launch** |

The six publisher processes are in fact prepared against a common `race_shared` work directory in `run_single_campaign.py` line 224, so the earlier CR1 defect of separate race targets is not repeated. This observation does **not** clear P0-B01.

Additionally, P4's regression-worker execution budget has not been freshly preregistered. A complete cross-lane terminal PASS would require a distinct admissible regression budget; historical 22/22, 14/14, 17/17 and 116/116 results cannot substitute for reruns.

## Strict stop and next scope boundary

All four material blockers lie outside the approved Boolean text-normalization-only change. Their presence **before** P1/P2 activates the authorization's mandatory P0 STOP. No Boolean correction was made, no RED/GREEN tests were executed for this new control, no campaign directory was created, no worker launched and no network dependency/provider contacted.

```text
P0 = BLOCKED_NEEDS_SEPARATE_CORRECTION
P1 = NOT_STARTED
P2 = NOT_STARTED
P3 = NOT_STARTED
P4 = NOT_STARTED
CR2_CR1_NEW_WORKER_BUDGET = 0_OF_13
CR2_CR1_TERMINAL_DECISION = BLOCKED
M2_POLICY = HUMAN_ADOPTED
M2_R1 = BLOCKED
M2_R1_CR1 = BLOCKED
M2_R1_CR2 = BLOCKED
F03_CR2 = BLOCKED
F03_CR2_CR1 = BLOCKED
WINDOWS_INTERNAL_ROOT_CAUSE = NOT_PROVEN
FC01_REAL_MEMORY_SAFETY = NOT_QUALIFIED
READ_A_RETRY = FALSE
READ_B = FALSE
B12 = CLOSED
FORCE = FALSE
FAIL_CLOSED = TRUE
STOP_AFTER_F03_CR2_CR1_M2_R1_CR2_CR1 = APPLIED
```

A **separate human decision** is required before repairing: (1) independently evidenced process-tree termination; (2) crash PID and start-identity linkage; (3) descendant start/termination identity verification; (4) independently anchored preexisting-final no-overwrite SHA-256 baseline. Strict Boolean normalization may be included in a future separately bounded package but must not be applied under this stopped CR2-CR1 attempt.

This report is eligible for documentary GitHub persistence only after a fresh concurrent-drift, exact-path staging, SHA-256 and non-force push check. No experimental executable is authorized for integration.
