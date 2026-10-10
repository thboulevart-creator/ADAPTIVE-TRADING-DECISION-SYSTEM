# F03-CR2-CR1-M2-R1 — MEMORY SAFETY POLICY SYNTHETIC QUALIFICATION V0.1

**Terminal decision: `BLOCKED` — P5 raw Windows evidence persistence incomplete.**
**Stop:** `STOP_AFTER_F03_CR2_CR1_M2_R1 = APPLIED`.

## Governing authority

- Human-adopted M2 memory hierarchy: `OS_ENFORCED_JOB_COMMIT_LIMIT` primary, `CURRENT_JOB_COMMITTED_MEMORY` secondary, `ALLOCATION_DENIAL_AND_VERIFIED_TERMINATION` failure authority, `PEAK_JOB_MEMORY_USED` diagnostic-only.
- M2-R1 separately authorized P0–P5, a maximum of 24 supervised synthetic worker launches, and restricted documentary persistence.
- Authorized base: `43cf0f3f534e26b43c084621eec71dc602cde4c5` / `0b7d69592a3d650f9e4f7994b4c88c58a65d0022`.
- Initial preflight: `e15bf453f44098c1dd990ebeb891583efdc85052` / `506d98d888f3dd0fee3d216e336a64d29f72bead`. Initial 4-file E1-D3-F2-only drift was qualified as nonmaterial for FC01/M2.
- Immediately before the Windows campaign, local HEAD changed to `58756f0fc176368abdf9ed65377dd23182ba5fb7` / `ed905414daa939d51fb6d84dc82900f1bbe38872`. The initial attempt stopped **before launching workers**. The intervening changes comprised a separate E1-D3-F2 Java module and two reports; the FC01/E1 critical blobs remained unchanged. Nonmaterial-for-M2 drift classification was documented.
- After the campaign and regression, GitHub advanced to `f22f8072bd5cafab6a282a58670d1b71f56f8cfb` / `b38f6a44b2aa402c30c88890c60de9f08d43ea3f`, with three further E1-D3-F2 documents. A fresh compare and protected-blob check are mandatory before persistence; no concurrent history will be overwritten.

## P0/P1 — preflight and RED

Windows x64, preinstalled .NET Framework compiler, Python 3.12, cached Java 8/JForex jar for **synthetic compilation only**, and NTFS temporary storage were available.

Prior M1 root-cause remains `NOT_PROVEN`. The previous six CR2-CR1 source snapshots matched the local experimental files, with no drift. The M2 signal hierarchy was bound to a frozen packet and a subsequent human-policy transcription witness.

RED was obtained with a missing M2 policy implementation. The first RED attempt gave 21 explicit failures and 1 fixture error. The fixture was corrected without launching a worker. The valid RED then had **22 explicit FAIL and 0 collection/setup errors**, attributable to missing isolated M2 candidate behavior.

## P2/P3 — synthetic candidate / GREEN

A standalone Python signal evaluator was created under `tools/fc01_f03_cr2/m2_r1/memory_policy.py`. It has no production entry point, credentials, provider call, order handling or runtime integration.

A private M2 derivative of the frozen CR2 synthetic Windows supervisor was created in the same isolated directory, with a read of **actual current Job Object committed memory** using `QueryInformationJobObject` information class 28, while preserving the peak counter as telemetry. The original CR2 supervisor, Java worker and recovery code were not modified.

- **20/20** policy scenario decisions passed, including injected missing limits/readback mismatch, assignment failure, missing current-commit observation, over-limit observation, native/Java memory failure classifications, unexplained peak anomaly, termination failures, late publication critical failure, and recovery failure.
- **13/13** pre-registered synthetic worker launches executed once: two normal deterministic outputs, a Java OOM, a timeout, a descendant timeout, preexisting-final collision, forced supervisor death and autonomous recovery, plus six concurrent publishers.
- The complete M2 test file finished **22/22 PASS**, `pytest exit 0`.
- Directly observed filesystem artifacts after test: identical normal outputs and race winner (SHA-256 `a39bffc0ddde4ccb2dcf3620510f9c8085139bd7a8ba48af70540a10eb714e91`); the sentinel final remained intact, SHA-256 `b2547b1b887d4586e8f73dc1d8410fca7cf1212a6e851534872ec505693dbecd`; memory failure/timeout/child termination/supervisor crash produced no final. There were no private CR2 directories left.
- No live `SyntheticHistoryWorker` Java process and no `F03CR2Supervisor.exe` process remained after the campaign.
- Direct launch audit: 13 named entries, SHA-256 `b33905c50dfdfe79f3184d4ebb1b0999a351352b3c8a80c3a3fe05445f14bd0e`.
- Additional tests that depend on the earlier M1 evidence of real native memory refusal are classified as **prior evidence + synthetic policy injection**; they are not represented as a fresh M2 native-allocation-denial test.

Some MS-xx scenarios were **injected policy inputs**, not genuine Windows failure modes. Test totals must not be interpreted as 20 independent OS fault injections.

## P4 — regression

The prior baseline suites CR2, CR2-CR1, M1, FC01/JF01/JF02 and E1 ran independently of the M2 worker-launch campaign:

- **116/116 PASS**, `pytest exit 0`.
- Existing canonical FC01 Maven package compilation **PASS, offline**, exit 0.
- Original FC01 and E1 Java blobs stayed `44ccaeafdd22cede207fef6038e5c747ff5d1454` and `2dcacfde5fdf9b39ce0c9647c4413f2d2fc67a0b`.

The legacy regression tests may spawn separate synthetic workers; those are **baseline regression executions**, and are not being counted as M2 campaign launches. They confer no new provider authority.

## P5 — evidence completeness and strict terminal classification

The M2 test verified important Windows results from process output (Job limit/readback, Job current/peak, assignment-before-resume, worker/child termination, recovery, collision, and hashes). However, the per-worker raw process output was held transiently inside pytest and **not durably archived**. The retained launch audit records scenario names only; it does not contain exact worker process identities, full Win32 counters, raw exit/classification receipts, or complete termination records for each of the 13 launches.

This shortfall cannot be corrected by reconstructing or inventing process output from successful pytest assertions, nor may the sole pre-registered campaign be replayed opportunistically for a favorable result. It prevents marking:

```text
P5_EVIDENCE = COMPLETE
ALL_MANDATORY_RUNTIME_EVIDENCE = PASS
M2_R1 = PASS_SYNTHETIC_POLICY_QUALIFICATION
```

The terminal result is therefore:

```text
M2_R1 = BLOCKED
BLOCKER = RAW_PER_WORKER_WINDOWS_RECEIPTS_NOT_PERSISTED
P1_RED = QUALIFIED
P2_ISOLATED_QUALIFIER = BUILT
P3_SYNTHETIC_GREEN = 22/22 PASS
P4_REGRESSIONS = 116/116 PASS
P5_EVIDENCE = PARTIAL
DIRECT_M2_WORKER_LAUNCHES = 13/24
WINDOWS_INTERNAL_ROOT_CAUSE = NOT_PROVEN
F03_CR2 = BLOCKED
F03_CR2_CR1 = BLOCKED
READ_A_RETRY = FALSE
READ_B = FALSE
B12 = CLOSED
FORCE = FALSE
STOP_AFTER_F03_CR2_CR1_M2_R1 = APPLIED
```

No FC01, E1, DATA-01, CR2 original runtime, production orchestration or provider code was modified. No provider request, real history read, credential use, trade or capital event was authorized or performed.

The eligible documentation and test file may be published after fresh GitHub checks. Executable candidate sources are to remain untracked, with SHA-256-verified forensic snapshots inside the BLOCKED evidence receipt. **No automatic correction, further M2 worker launch or operational adoption is authorized.**

## Next separate human decision

A narrowly scoped evidence-capture correction would need a new human authorization to persist per-worker raw stdout/stderr and Win32 identity and counter receipts **before** any new worker launch, followed by a fresh budgeted requalification. Existing evidence must remain intact. This is an evidence contract repair, not approval for JForex or FC01 integration.
