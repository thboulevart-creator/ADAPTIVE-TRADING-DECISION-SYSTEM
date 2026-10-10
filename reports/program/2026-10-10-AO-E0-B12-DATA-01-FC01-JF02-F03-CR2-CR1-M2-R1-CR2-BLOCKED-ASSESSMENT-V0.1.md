# F03-CR2-CR1-M2-R1-CR2 — BLOCKED QUALIFICATION ASSESSMENT V0.1

## Terminal result

```text
CONTROL_ID = AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2
STATUS = HUMAN_ADOPTED_AND_EXECUTION_AUTHORIZED
M2_R1_CR2 = BLOCKED
P0_FRESH_READINESS = PASS
P1_RED = 17_EXPECTED_FAILURES
P2_ISOLATED_STATIC_GREEN = 17/17_PASS
P2_CSHARP_OFFLINE_COMPILATION = PASS
P3_CAMPAIGN = STOPPED_AFTER_4_OF_13_WORKER_LAUNCHES
P4_REGRESSION = NOT_RERUN_AFTER_P3_BLOCKER
P5_EVIDENCE = PARTIAL_BLOCKED_RECEIPTS_PERSISTED
PRIMARY_BLOCKER = TERMINATION_BOOLEAN_TRUE_CASE_NOT_NORMALIZED
RETRY = FALSE
STOP_AFTER_F03_CR2_CR1_M2_R1_CR2 = APPLIED
```

## Canonical scope

The authorized GitHub starting point is `52ba45d6590fc51aacb356e6cb14fb30b8da69d8`, TREE `f9c2a8b846d3893c5004771bbc98f92e1e51531f`, branch `integration/system-v1`. Protected FC01 and E1 blobs remained unchanged during read-only checks. The prior CR1 BLOCKED evidence SHA-256 was `8b579f3a2b9dca130e8d58629c33cad85385e31715c0e181f9d60083b53faacc`.

Previously adopted M2 policy remains governing: enforce Job memory limit, observe current committed memory, handle errors and verified termination, retain peak as diagnostic-only. Prior M2-R1 and CR1 BLOCKED adjudications were not altered. Root cause of internal Windows peak accounting remains `NOT_PROVEN`.

## Test-first evidence

CR2 contract RED was performed with the validator absent: **17 expected failures, zero setup/collection errors** across CR2-01..CR2-16 and no-provider control. After implementing the CR2 isolated validator: **17/17 static PASS**. A new isolated `F03CR2SupervisorCR2.cs` derivative compiled offline. It uses Windows `CreateProcessW` extended startup attributes with an explicit 3-handle inheritance allowlist for `NUL` stdin and two direct JVM stdout/stderr capture files, created before worker resumption. The original FC01, E1, CR2 and CR1 sources were not modified.

The campaign `M2R1CR2_20261010_CAP01` was individually frozen with exactly **13** planned worker launches, no retries, and **zero worker-launching regression tests authorized** unless separately pre-registered. The isolated capture owner created supervisor stream files before launch and persisted direct-JVM files, per-worker identities, Job current commit/peak, receipt integrity and exit evidence.

## Campaign outcome

| # | Scenario | Supervisory result | Evidence validation | Final output |
|---|---|---|---|---|
| 1 | normal_A | PUBLISHED / exit 0 | PASS | present |
| 2 | normal_B | PUBLISHED / exit 0 | PASS | present; identical SHA |
| 3 | java_oom | BLOCKED_MEMORY / exit 22 | PASS | verified absent; final_sha256 = null |
| 4 | timeout | BLOCKED_TIMEOUT / exit 21 | **BLOCKED** | verified absent |

The fourth supervisor raw output included:

```text
CR1_TERMINATION_REQUEST=TERMINATE_JOB
CR1_WORKER_TERMINATED=True
CR1_WORKER_EXIT_CODE=88
RESULT=BLOCKED_TIMEOUT
```

However, the CR2 receipt owner compared the termination string case-sensitively with the literal `TRUE`, so it stored `termination_confirmed=false` and `tree_terminated=false` and the independent policy validator correctly produced:

```text
TREE_TERMINATION_UNVERIFIED
WORKER_TERMINATION_UNVERIFIED
```

This is a proven collector-side representation defect for the fourth scenario, rather than direct evidence of failure of the Windows `TerminateJobObject` action. Nevertheless, the terminal safety receipt is BLOCKED and must **not** be changed retroactively. The worker's Win32 exit was recorded as `88` and a post-test process check found zero synthetic Java workers; this observation does not automatically promote the failed receipt.

The independent direct-JVM stream capture was effective for the four executed scenarios: both Java output files and both supervisor output files were present and SHA-256 checked; zero-length JVM output is not automatically a failure when the capture was established before worker resume. No distinction between supervisor logs and JVM byte streams has been erased.

## Unexecuted scope and nonclaims

```text
NEW_CAMPAIGN_LAUNCH_BUDGET_CONSUMED = 4/13
UNSPENT_WORKER_LAUNCHES = 9
OPPORTUNISTIC_RETRY = FALSE
CHILD_HANG = NOT_EXECUTED
EXISTING_FINAL_COLLISION = NOT_EXECUTED
SUPERVISOR_CRASH_AND_RECOVERY = NOT_EXECUTED
SIX_WAY_CONCURRENT_PUBLICATION = NOT_EXECUTED
REGRESSION_WORKER_BUDGET = 0
P4_FULL_CROSS_LANE_REGRESSIONS = NOT_RERUN_AFTER_STOP
```

The remaining nine slots are **not** authorization to resume the stopped campaign. Crash recovery, descendant identity, and no-overwrite under actual concurrent racing remain unqualified in CR2.

The four per-run raw streams, receipts, hashes, source snapshots, freeze packet and launch log must be preserved exactly. Worker and Job details in transient stdout have not been recreated as fabricated authoritative new measurements.

## Required separate next human decision

The next frontier is a tightly scoped **CR2-CR1 — BOOLEAN TERMINATION RECEIPT NORMALIZATION & INDEPENDENT REQUALIFICATION** decision. It should authorize only a frozen case-insensitive parsing rule for the explicit boolean values `True`/`False` (and `TRUE`/`FALSE`) with rejection of unexpected values, paired with fresh red and green tests and a new, separate synthetic worker campaign if needed. Previous CR2 campaign evidence, worker count and received hashes must remain frozen.

This does not authorize amending the previous CR2 receipt in place, modifying OS-memory decision logic, or running the nine unspent old campaign slots.

## Strict authority firewall

```text
M2_POLICY = HUMAN_ADOPTED
M2_R1 = BLOCKED
M2_R1_CR1 = BLOCKED
M2_R1_CR2 = BLOCKED
WINDOWS_INTERNAL_ROOT_CAUSE = NOT_PROVEN
F03_CR2 = BLOCKED
F03_CR2_CR1 = BLOCKED
FC01_REAL_MEMORY_SAFETY = NOT_QUALIFIED
PROVIDER_REQUESTS = 0
JFOREX_LOGIN = 0
JFOREX_CONNECT = 0
REAL_HISTORY_READ = 0
READ_A_RETRY = FALSE
READ_B = FALSE
B12 = CLOSED
CANONICAL_RUNTIME_MUTATION = FALSE
FORCE = FALSE
FAIL_CLOSED = TRUE
STOP_AFTER_F03_CR2_CR1_M2_R1_CR2 = APPLIED
```
