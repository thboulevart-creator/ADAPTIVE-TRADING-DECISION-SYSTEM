# R1-CR1-WER-05-R1 V0.1 — Host memory and guest control readiness qualification

**Terminal verdict:** `REQUIRES_TARGETED_CORRECTION`  
**Safety state:** `STOP = APPLIED`  
**Human authority:** explicit R1 read-only authorization adopted 2026-10-13. Does **not** authorize Sandbox launch, guest shutdown/termination, active supervisor, ETW, host configuration change or process termination.

## 1. Immutable references and scope
- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`; governed branch `integration/system-v1`.
- Fresh pre-publication HEAD: `9ed38d72580635d9a63eff76cf6196123be2d8a1`; TREE: `2cc1e7c78bc493be9ade9277a4acc3699dc646e1`; matches the approved references.
- Local Windows repository at `C:\Users\Boulevart\Documents\ADAPTIVE-TRADING-DECISION-SYSTEM` also matched branch, HEAD, TREE and origin. Git tracked diff and staged diff empty. **88 existing untracked entries** counted; untouched. No local reset, clean, checkout or checkout-based mutation.
- At pre-publication, the two proposed R1 paths returned GitHub 404 (no collision). Two new documentary files only are authorized; publication must be atomic with `force=false` and expected-HEAD lease.
- Historical WER-05 remains `BLOCKED`: P0 PASS, P1 blocked, P2–P6 not started, P7 historical forensic documents published; zero Sandbox boot attempts. No historical campaign or budget is reopened.

## 2. Three 30-second host-memory measurements (real, read-only)
Sources: Windows PowerShell `Get-CimInstance Win32_OperatingSystem` and `Win32_PerfFormattedData_PerfOS_Memory`, collected via Desktop Commander without elevation. Times UTC, 2026-10-13.

| Sample | UTC | OS free physical bytes | Perf available MiB | Committed bytes | Commit limit bytes | Commit headroom bytes | PageReads/s | Pages/s | PageWrites/s |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 12:32:46.7828354 | 2032979968 | 1688 | 30052876288 | 35796262912 | 5743386624 | 517 | 7967 | 0 |
| 2 | 12:33:17.2196510 | 1544822784 | 1450 | 30428815360 | 35796262912 | 5367447552 | 15 | 59 | 0 |
| 3 | 12:33:47.6616571 | 1697075200 | 1621 | 30214057984 | 35796262912 | 5582204928 | 0 | 0 | 0 |

- Elapsed sample spacing: ~30.44 s, then ~30.44 s.
- Visible physical memory: 16954851328 bytes (~15.79 GiB).
- **Adopted conservative thresholds:** free/available host physical RAM >= 6 GiB **and** commit headroom >= 6 GiB at all three samples; no sustained material degradation. Both numerical thresholds **FAIL in all three samples**. The independently sampled performance-counter available-memory measurements also fail the 6-GiB criterion.
- Observed physical availability roughly 1.44–1.89 GiB (OS samples) and commit headroom roughly 5.00–5.35 GiB. The three samples fluctuate; no stable 6-GiB reserve is demonstrated.
- Page activity at sample 1 is transient; three samples cannot prove sustained thrashing or predict launch failure. No causal explanation for the variation is claimed.
- Guest memory contract unchanged: `MemoryInMB=4096` (4,294,967,296 bytes). These conservative margins are engineering admission criteria, not Microsoft boot requirements, and are not proof that Sandbox cannot technically start.
- No memory was force-freed; no user process stopped; no host parameter changed.

## 3. Guest identification and control preflight (without guest)
**Verified on this host, in read-only mode:**
- Windows 11 Professionnel N build 22631 (Windows 11 23H2), 64-bit; `HypervisorPresent=True`; no elevated administrator token.
- `WindowsSandbox.exe` and `WindowsSandboxClient.exe` commands exist; `wsb.exe` is absent. The documented `wsb list/stop/exec` CLI is available only from Windows 11 24H2 onward, not as a verified tool on this host.
- `hcsdiag.exe` present; `hcsdiag list -raw` returned exit code 0 and the following baseline system: `fb568601-3fab-442c-b602-9bbc54ea64c1`, `SystemType=VirtualMachine`, `Owner=CmService`, `State=SavedAsTemplate`. This **preexisting** system is explicitly excluded from any future manipulation. Baseline enumeration does not imply a running Sandbox.
- No `WindowsSandbox.exe`, `WindowsSandboxClient.exe` or `vmwp.exe` host process was returned by the bounded read-only query.
- `Microsoft-Windows-Hyper-V-Compute-Admin` and `Microsoft-Windows-Hyper-V-Worker-Admin` event logs exist and are enabled (metadata enumeration only).
- The PowerShell `HostComputeService` module and `Get-VM` cmdlet were not available in the checked non-elevated session.
- Desktop Commander supplied reliable remote shell execution/readback and HCS inventory, **not** direct control of the guest graphical desktop or proof of a guest shutdown.

**Not proven / not executed:**
- A unique real guest HCS ID cannot be established before a separately authorized boot. A pre/post HCS delta + owner/state/process/timestamp correlation is a proposed method, not a passed live test. A new HCS entry alone does not establish guest identity if concurrent systems change.
- Non-elevated ability to target the correct Sandbox for orderly shutdown; fallback privileged termination; actual exit and resource release; or guest-inside telemetry/capture permissions.
- A local independent watchdog meeting the 300-second deadline. No Windows supervisor was run, no scheduled task/service created, no kill command tested. Remote connectivity cannot serve as sole watchdog.
- Closing the GUI process cannot be treated as proof of HCS teardown. Independent evidence will require targeted guest-ID HCS disappearance/terminal state, host-side process ownership reconciliation, and appropriate lifecycle events, with no unrelated VM affected.
- Network, clipboard and mapped-folder exchange remain forbidden. Only read-only host-side logs/diagnostics can support evidence under current isolation policy. Guest-only facts cannot be inferred from host metadata.

Microsoft technical references:
- Windows Sandbox .wsb settings: https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file
- Windows Sandbox CLI availability (from 24H2): https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-cli
- HCS API overview and separation of graceful shutdown and forced terminate: https://learn.microsoft.com/en-us/virtualization/api/hcs/reference/apioverview

## 4. Risk decision and minimum next boundary
**Terminal verdict = `REQUIRES_TARGETED_CORRECTION`.** Memory admission FAIL and independent controlled teardown NOT QUALIFIED. The safety breaker `CONTROLLED_TEARDOWN_NOT_JUSTIFIED` is applied; no additional host execution beyond read-only preflight occurred after that determination.

Future **separate human adjudication** must address both blockers without silently changing WER-05:
1. Host resources: allow only user-chosen, non-destructive workload changes (if desired), then collect a fresh spaced triad meeting both 6-GiB criteria. A lower `MemoryInMB` requires distinct contract authorization; neither is automatic.
2. Guest control: establish an autonomous, host-local timeout and targeted stop/cleanup mechanism suitable for Windows build 22631, with unique positive guest identity, strict exclusions of `CmService` baseline, exact 300-second bound, lost-remote-control fail-closed behavior, and host-only teardown evidence. Any active supervisor/stop mechanism implementation, dry-run or live test requires its own authorization. If no provable bounded teardown path exists, no boot.
3. Only then consider a **separate WER-05 Sandbox boot adjudication**, with one explicit finite budget and STOP conditions. No permission is inherited from the historical unspent WER-05 boot budget.

## 5. Authority firewall and terminal stop
```ini
R1_CR1_WER_05_R1=REQUIRES_TARGETED_CORRECTION
HOST_MEMORY_6_GIB_GATE=FAIL_3_OF_3
COMMIT_HEADROOM_6_GIB_GATE=FAIL_3_OF_3
GUEST_CONTROL_READ_ONLY=PARTIALLY_VERIFIED
INDEPENDENT_300S_TEARDOWN=NOT_QUALIFIED
PREEXISTING_HCS_VM_MODIFIED=FALSE
SANDBOX_BOOT_ATTEMPTS=0
WSB_CONFIG_CREATED=FALSE
WINDOWS_SUPERVISOR_EXECUTIONS=0
ETW_SESSION_STARTS=0
REAL_ETW_CAPTURE=0
ATDS_WORKERS=0
REGRESSION_WORKERS=0
PROCESS_TERMINATION=0
HOST_PRIVILEGE_ESCALATION=FALSE
SECURITY_POLICY_MUTATION=FALSE
HOST_REBOOT=FALSE
HISTORICAL_EVIDENCE_MUTATION=FALSE
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
