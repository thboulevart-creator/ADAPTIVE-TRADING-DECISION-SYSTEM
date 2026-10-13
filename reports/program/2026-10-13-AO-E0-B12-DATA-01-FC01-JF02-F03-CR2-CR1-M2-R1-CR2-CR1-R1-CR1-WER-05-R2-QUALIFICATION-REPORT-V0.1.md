# R1-CR1-WER-05-R2 V0.1 — Targeted host memory & autonomous teardown correction

**HUMAN_AUTHORIZATION:** explicitly adopted in conversation, scoped R2.  
**TERMINAL:** `REQUIRES_TARGETED_CORRECTION`  
**STOP:** `APPLIED`  
**Important:** real Windows Sandbox launch, real VM shutdown, real supervisor, OS setting change, process termination, privilege escalation and ETW capture were forbidden and **NOT** executed.

## Canonical reference and unmodified local checkout

Repository `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`; governed branch `integration/system-v1`; adopted entry HEAD `5d42f59b753dc9dc068a5ef26fe33b8c629782e9`, TREE `9227f34066f61af2ef78eadf88b3f85f590c3e9e`.

Fresh GitHub branch verified matching entry at beginning. The authorized two R2 synthetic-source additions were published in commit `39c0685e92a99dceb04fd529d087a719615ec69a`, TREE `46e8e9580d0c5a6bfe74b66307600b943f2a371b`. This report and terminal receipt are further **new-only** R2 evidence, with no changes to existing historical files. Branch ref update uses expected-SHA lease and `force=false`.

Local Windows checkout `C:\Users\Boulevart\Documents\ADAPTIVE-TRADING-DECISION-SYSTEM`: branch `integration/system-v1`, origin correct, local HEAD `9ed38d72580635d9a63eff76cf6196123be2d8a1`, TREE `2cc1e7c78bc493be9ade9277a4acc3699dc646e1`, **behind GitHub by already-known R1/R2 commits**; tracked working diff empty, 88 existing untracked entries. No Git synchronization, reset, checkout, clean or local file mutation performed. GitHub remains canonical. The local mismatch is explicitly disclosed and **not treated as an up-to-date checkout**.

## A. Current memory diagnosis (actual host, read-only)

2026-10-13T14:04:54.4108033Z, `Win32_OperatingSystem` + `Win32_PerfFormattedData_PerfOS_Memory` + `Get-Process`:
- Total visible RAM: ~15.79 GiB; OS physical available: ~1.92 GiB; perf-counter available: ~1.80 GiB.
- Committed: ~28.99 GiB; commit limit ~33.34 GiB; remaining commitment headroom ~4.34 GiB.
- Contract: guest `MemoryInMB=4096` unchanged. Conservative R1 adopted threshold: >=6 GiB physical available **and** >=6 GiB commit headroom on three observations spaced 30s (no new triad taken, because **no user-approved workload change occurred**).
- Instantaneous shortfalls at this inventory: ~4.08 GiB physical and ~1.66 GiB commit headroom. A one-off observation is **not** a new qualification triad.
- Top grouped per-process *private committed memory* (NOT reclaimable resident RAM): Edge 42 processes ~11.30 GiB, VS Code 13 ~1.78 GiB, Claude 12 ~1.57 GiB, Edge WebView2 18 ~0.98 GiB, Obsidian 4 ~0.57 GiB, Notion 6 ~0.50 GiB. Working sets are different and should not be conflated with private bytes or summed to promise a physical-RAM gain.
- Large potential non-destructive user-controlled optimization: identify/save work in inactive Edge tabs/windows and **user voluntarily** close or suspend unneeded browser workloads, then repeat the spaced triad. No remote process termination, no forced release, no host configuration mutation was attempted.
- No new memory qualification after voluntary reduction is claimed. `HOST_MEMORY_READINESS = BLOCKED`.

## B. Native host control — factual verification and solution choice

Host Windows 11 Professional N build 22631 (23H2), non-elevated shell. `WindowsSandbox.exe` and `WindowsSandboxClient.exe` present, but **`wsb.exe` absent**. Microsoft's dedicated `wsb start/list/stop --id` interface begins Windows 11 **24H2**; do not assume it works here:
https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-cli

`hcsdiag list -raw` returns exit code 0, displaying only the pre-existing HCS VM `fb568601-3fab-442c-b602-9bbc54ea64c1`, `Owner=CmService`, `State=SavedAsTemplate`. It is **protected/excluded**. Read-only HCS enumeration is possible and no Sandbox processes were observed; this does **not** prove a future guest's unique identity or an ability to shut it down.

Microsoft HCS APIs support `HcsShutDownComputeSystem` (graceful) and `HcsTerminateComputeSystem` (forced), but these require a precise compute-system handle. Permissions/ownership binding and feasibility against a real Sandbox on build 22631 are **NOT TESTED**:
https://learn.microsoft.com/en-us/virtualization/api/hcs/reference/hcsshutdowncomputesystem
https://learn.microsoft.com/en-us/virtualization/api/hcs/reference/hcsterminatecomputesystem

**Minimal candidate:** host-local independent watchdog, trusted launcher-to-HCS identity binding, immutable baseline exclusion, proactive graceful proposal at mock t=240s, conditional fallback proposal at mock t=270s, independent evidence requirement and deadline-breach gate at t>=300s. **No real Windows controller, service, scheduled task or shutdown adapter was implemented or executed.** An operational watchdog is NOT proven; a modeled proposal at 240/270 does not guarantee completion by 300 seconds. Without verified permissions and a locally executable targeted actuator, fail closed. GUI `WM_CLOSE` or killing a window process is not accepted as teardown proof.

**Alternative:** future Windows feature update to a supported build with official `wsb` CLI, only under separate human authorization (OS mutation/reboot NOT authorized by R2), followed by targeted capability and actual clean shutdown qualification. On current 23H2, creating a custom HCS actuator before proving privileges and unique identity is less defensible and more complex.

Windows Sandbox remains configured with networking/clipboard/mapped-folders forbidden by existing contract. No guest network/clipboard/path was enabled. Host-only diagnostics/logs are the future evidence route; guest-only facts are not observable without separate live authorization.

## C. Source and independently rerun pure synthetic tests

The **new-only** R2 source files on GitHub:
- `tools/wer05_r2/wer05_r2_safety_oracle.py` (Git blob `65ded460c2033b99be8ac8936e6d811eb5a879e3`).
- `tools/wer05_r2/test_wer05_r2_safety_oracle.py` (Git blob `07c4037074a3246c13f8c349b4e4a76c3ec363ae`).

The pure Python oracle imports only dataclasses, enum, typing, consumes synthetic `MockObservation`, and returns decision labels. It has no Windows API, process stop, timer execution, task scheduler, HCS call or real guest control.

**Execution 1:** isolated model-side Python 3.13.5, `python -m unittest -v test_wer05_r2_safety_oracle.py`: 20/20 PASS, exit 0.

**Execution 2:** exact published sources fetched back from GitHub and executed in an ephemeral PowerShell -> `python -B -` pipeline on the Windows machine (in-memory module compilation/execution, no local repository file created): `PUBLISHED_SOURCE_TEST_COUNT=20`, `PUBLISHED_SOURCE_TESTS_PASS=True`, `Ran 20 tests ... OK`. No executable supervisor or real guest.

Coverage includes: no attestation, unclear metadata, protected preexisting VM target, multiple new VMs, no autonomous watchdog, unproven privileges/fallback/graceful path, pre-240 observation, 240/270 mock proposals, lost remote link, t>=300 breach, incomplete disappearance proof, valid fully synthetic disappearance proof, reversed clock, missing and unrelated guest IDs.

**Strict limit:** PASS qualifies **only a pure decision-state model**, not a live watchdog, exact 300s stop, guest permissions, process/FILETIME identity, actual HCS stop, host resource reclamation or Sandbox isolation. Test fixtures asserting permissions/identity do not establish those permissions/identity on Windows.

## D. Terminal result and separate next decision

```ini
R1_CR1_WER_05_R2=REQUIRES_TARGETED_CORRECTION
HOST_MEMORY_6_GIB_GATE=FAIL_CURRENT_INVENTORY
HOST_COMMIT_HEADROOM_6_GIB_GATE=FAIL_CURRENT_INVENTORY
NEW_SPACED_MEMORY_TRIAD=NOT_RUN_NO_VOLUNTARY_WORKLOAD_CHANGE
MODEL_SYNTHETIC_TESTS=20_OF_20_PASS
REAL_AUTONOMOUS_WATCHDOG=NOT_IMPLEMENTED
REAL_GUEST_ID_BINDING=NOT_PROVEN
REAL_TARGETED_STOP_PRIVILEGE=NOT_QUALIFIED
INDEPENDENT_300S_TEARDOWN=NOT_PROVEN
SANDBOX_BOOT_ATTEMPTS=0
ACTIVE_WINDOWS_SUPERVISOR_EXECUTIONS=0
REAL_ETW_CAPTURE=0
ETW_SESSION_STARTS=0
ATDS_WORKERS=0
PROCESS_TERMINATIONS=0
PREEXISTING_HCS_VM_MODIFICATIONS=0
HOST_SETTINGS_MUTATIONS=0
HOST_REBOOTS=0
PRIVILEGE_ESCALATIONS=0
HISTORICAL_EVIDENCE_MUTATIONS=0
WSB_MEMORY_IN_MB=4096_UNCHANGED
READ_A_RETRY=FALSE
READ_B=FALSE
B12=CLOSED
TRADING=FALSE
ORDERS=FALSE
CAPITAL=FALSE
FORCE=FALSE
FAIL_CLOSED=TRUE
STOP=APPLIED
```

**Recommended separate authorization:** user-initiated closure/suspension of nonessential browser workloads, followed by a fresh 30s-spaced memory triad; and choose one of (A) an independently qualified native host-local HCS actuator with specific guest identity, permission verification and real teardown proof, or (B) separately approved OS update to supported `wsb` CLI (subject to user risk/maintenance acceptance). Neither is authorized by R2. Real Sandbox boot only after a further distinct adjudication.
