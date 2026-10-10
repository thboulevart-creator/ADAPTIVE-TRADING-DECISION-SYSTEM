# F03-CR2-CR1-M2-R1-CR1 — BLOCKED CAPTURE-REQUALIFICATION ASSESSMENT V0.1

## Terminal adjudication

```text
M2_R1_CR1 = BLOCKED
BLOCKER_PRIMARY = RECEIPT_VALIDATOR_REQUIRES_FINAL_SHA256_WHEN_FINAL_ABSENT
BLOCKER_SECONDARY = RAW_JVM_WORKER_STDOUT_STDERR_NOT_INSTRUMENTED
P0 = PASS
P1_RED = 14_EXPECTED_FAILS
P2_STATIC_GREEN = 14/14_PASS
P3_NEW_CAMPAIGN = STOPPED_EARLY
P4_BASELINE_REGRESSIONS = NOT_RERUN_AFTER_STOP
P5_EVIDENCE = PARTIAL
CAMPAIGN_LAUNCHES = 3/13_PLANNED
MAX_BUDGET = 24
RETRY = FALSE
STOP_AFTER_F03_CR2_CR1_M2_R1_CR1 = APPLIED
```

## Pre-execution and protected scientific context

The user explicitly adopted CR1 as a separate synthetic-only evidence-persistence correction. Governed GitHub branch: `integration/system-v1`. The reference HEAD/TREE prior to CR1 were `c5e0f7362837b6e171e1aaf849dec703fc320380` / `3beec0d88a38e8b607239b0399ce3e2230041121`.

The M2 policy remains human-adopted: enforced Job Object memory limit is primary; current committed memory is secondary observation; allocation denial and verified termination are mandatory; `PeakJobMemoryUsed` is diagnostic-only. Prior M2-R1 remains `BLOCKED`; M1 Windows internal root cause remains `NOT_PROVEN`. No prior results were modified.

Before launch, CR1's frozen configuration and instrument-source SHA-256 manifest were persisted. The new isolated C# supervisor derivative added only evidence logging, including exact supervisor and worker PID plus Win32 `GetProcessTimes` creation FILETIME, current Job memory and diagnostic peak, and worker exit and termination observations. An isolated Python owner created intent, command, stdout/stderr capture files and started receipt *before* the worker's test was concluded, streamed supervisor outputs directly into those files, and verified hashes by readback. It did not route raw Java child stdout/stderr into those files; this limitation remains independently material to a claim of fully complete per-worker raw stdio.

## Valid RED and bounded GREEN

The 12 adversarial capture-contract cases, one positive control and one no-provider-source control produced **14 expected RED failures, 0 setup errors** before the capture owner existed; afterward the tests completed **14/14 PASS**.

The separate single frozen CR1 campaign `M2R1CR1_20261010_CAP01` started with a planned maximum of 13 worker launches and an absolute authorized cap of 24.

| Launch | Win32 supervisor result | Supervisor exit | Receipt validation | Business final |
|---|---|---:|---|---|
| normal_A | PUBLISHED | 0 | PASS | present; SHA-256 `a39bffc0ddde4ccb2dcf3620510f9c8085139bd7a8ba48af70540a10eb714e91` |
| normal_B | PUBLISHED | 0 | PASS | present; identical SHA-256 |
| java_oom | BLOCKED_MEMORY | 22 | BLOCKED | absent |

The third worker was recorded as PID `16020`, Win32 creation FILETIME `134361201932179565`. Its supervisor PID was `37900` with creation FILETIME `134361201931850216`. Its Job Object limit readback was `268435456` bytes; observed current commit `405504` bytes and diagnostic peak `413696` bytes. The worker exit code was `28`, termination was reported true, and no final file was present. Raw supervisor stdout and stderr were persisted with SHA-256.

The third receipt failed for **one explicitly observed schema reason**: `MISSING_final_sha256`. The validator's generic missing-field rule incorrectly treated `final_sha256=None` as missing mandatory evidence, even though `final_present=False` is required after `BLOCKED_MEMORY`. This is a false-positive *receipt schema* blocker, not proof of a Job Object memory safety failure. Nonetheless, the CR1 fail-closed rule requires STOP and a non-PASS terminal verdict.

No fourth worker was started, no retry was made, and the unspent 21 worker slots were not used. The underlying Job Object original, M2 policy, FC01/E1 sources and M2-R1 historical evidence have not been changed.

## Limits of proof

- Stream files `supervisor_stdout.bin` and `supervisor_stderr.bin` are actual **supervisor** process streams. The Java worker's own raw stdout/stderr were **not separately captured**; this cannot be presented as a complete JVM stream receipt.
- Normal-A and Normal-B were bit-for-bit deterministic, but timeout, descendant confinement, supervisor-crash recovery and concurrent publication were **not executed in this new campaign**.
- The terminal campaign was ended after launch three; thus P3 and P5 are incomplete.
- No separate P4 re-run was conducted **after** the CR1 campaign STOP. The previously reported M2-R1 `22/22` and `116/116` are historical evidence, not CR1-rerun claims.
- A crash/power-loss durability claim was not tested.
- All known files, SHA-256 values, exact supervisor raw byte streams and original receipts are preserved in the CR1 BLOCKED evidence document or on the isolated local NTFS lab.

## Required next human decision

A separate CR1 repair adjudication should address two independent, narrowly scoped corrections **before** any fresh campaign: (A) make the receipt schema conditional so `final_sha256` is required iff a final file exists; (B) directly persist Java worker raw stdout/stderr and start/termination identities, without changing the approved memory safety behavior.

The new adjudication must set a new campaign identity and explicit worker budget. The previous CR1 single frozen campaign is CLOSED and must not be restarted or retroactively promoted.

## Nonnegotiable authority firewall

```text
PROVIDER_REQUESTS = 0
JFOREX_LOGIN = 0
JFOREX_CONNECT = 0
REAL_HISTORY_READ = 0
FC01_CANONICAL_SOURCE_MUTATION = FALSE
E1_SOURCE_MUTATION = FALSE
CR2_EXISTING_RUNTIME_MUTATION = FALSE
M2_POLICY_MUTATION = FALSE
READ_A_RETRY = FALSE
READ_B = FALSE
B12 = CLOSED
FORCE = FALSE
FAIL_CLOSED = TRUE
STOP_AFTER_F03_CR2_CR1_M2_R1_CR1 = APPLIED
```
