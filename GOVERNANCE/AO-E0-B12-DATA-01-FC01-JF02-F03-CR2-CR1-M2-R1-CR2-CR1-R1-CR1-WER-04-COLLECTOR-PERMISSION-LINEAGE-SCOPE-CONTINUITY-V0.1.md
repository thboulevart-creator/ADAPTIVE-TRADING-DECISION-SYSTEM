# AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-04 — Collector permissions, parent identity, scope and continuity V0.1

## Authority and evidence discipline
**HUMAN_ADOPTED_AND_EXECUTION_AUTHORIZED** for P0-P6, **documentary and static only**. No Windows worker, ETW session, probe, supervisor, Sandbox launch, source mutation, security policy change, privilege elevation, provider request or dependency download.
Canonical P0: branch `integration/system-v1`, HEAD `a5a6351a5cb664c1f36c3b4ee4f84c3f56a0b78d`, TREE `e5c5fd95917a50349c4e351c01bfcd7b42293a0f`, zero tracked changes. FC01 blob `44ccaeafdd22cede207fef6038e5c747ff5d1454`, E1 blob `2dcacfde5fdf9b39ce0c9647c4413f2d2fc67a0b` unchanged. WER03 frozen JSON SHA256 `101a3e760cb6704e6786885c15d5642003df89f404bc632e641123571663ea11`; WER02 candidate SHA256 `a73cc58b7b21a0c29130f07aab1173ed18a5c6947f6049036e954fd98ab447d4`; GREEN SHA256 `8092c558370130acd9eb16b1c3d1cfed209ff0b8b6f7e78f6a02354c2fc7f0e1`; RED oracle SHA256 `2335423d1afe32bb9985a8a58331e3bd69ccdb811ac222cdfc197e47f3801aee`.

## P1 — Permission decision and minimal privileges
- Observed host: Windows 11 Professionnel N 10.0.22631 x64; `ADMIN_ELEVATED=False`, `PERF_LOG_USERS_GROUP=False`. Kernel Process ETW provider metadata is registered, but **no session was opened and permission to start it is NOT PROVEN**.
- Microsoft ETW session controllers generally require elevated rights, Performance Log Users membership or service identities; actual kernel provider rights may have additional requirements. WER04 authorizes no group membership/policy changes and no privilege elevation.
- **Option A / current host:** `NOT_QUALIFIED`. Available ETW DLLs and provider metadata do not grant rights.
- **Option B / dedicated isolated environment:** `SELECTED_AS_CONDITIONAL_PREFERRED_DESIGN`, NOT READY TO RUN. Explicit, limited VM-contained permissions and proof of no unauthorized process collection required separately.
- **Option C / no admissible environment:** `BLOCKED` if VM, permissions, scope or event-loss guarantees cannot be satisfied. No real session can be opened under this contract.

## P2 — Parent identity and precise semantics
- Inspected `Microsoft-Windows-Kernel-Process` event ID 1 v0 fields: child `ProcessID`, child `CreateTime`, `ParentProcessID`, `SessionID`, `ImageName`. **No parent creation FILETIME is provided** by this inspected event version.
- Required correlation: acquire and keep a handle to the **reported parent** while its identity is unambiguous; `GetProcessTimes` binds reported parent PID and exact creation FILETIME. The parent handle must predate or securely overlap the child creation event, with session-window and PID-reuse checks. A late `OpenProcess(parent_pid)` after PID reuse is not sufficient. Track child `(PID, FILETIME)` from event plus corroborating handle where feasible.
- A boot-scoped process start key is a possible **supplemental** discriminator if the exact chosen kernel provider/extended data path supports it; it is NOT a substitute for the required parent FILETIME in this contract and remains unqualified.
- `PROC_THREAD_ATTRIBUTE_PARENT_PROCESS` permits an alternate parent identity to be supplied during process creation. Consequently separate `REPORTED_CREATION_PARENT`, `VERIFIED_REPORTED_PARENT_IDENTITY`, `ACTUAL_INITIATING_PROCESS_NOT_PROVEN`. Never promote a *reported* parent to independently proven initiating creator without additional qualifying evidence.
- Strong zero-gap rule: if parent handle is gone, parent start unverified, captured event delayed, or start key/FILETIME conflicts, return `BLOCKED`. Unknown Job member or descendant under ambiguous lineage is not classified by scenario markers.

## P3 — Capture scope: explicit comparison
| Dimension | Provider-side PID filtering (Option A) | Isolated Windows VM/Sandbox (Option B) |
|---|---|---|
| Source isolation | Provider/version-specific; **not proven** for kernel process-start events | Host processes separated from guest kernel; guest may still expose incidental guest OS process events |
| Risks | PID reuse, process start before filter, filtering only after event production, filters not implemented by provider | VM feature readiness, hypervisor support, guest permissions, default network/clipboard/folder mappings, loss of evidence when guest discarded |
| Privileges | Current non-admin token not qualified | Explicitly approved in guest only; not automatically granted |
| Decision | `NOT_QUALIFIED` | `CONDITIONALLY_PREFERRED_NOT_EXECUTABLE` |

**Observed** host facts via read-only CIM: Windows Sandbox optional feature `Containers-DisposableClientVM` reported `InstallState=1`, hypervisor `HypervisorPresent=True`, RAM 16,954,851,328 bytes; processor CIM reported `VirtualizationFirmwareEnabled=False` and `SecondLevelAddressTranslationExtensions=False`, a potentially inconsistent virtualized reporting condition. No Sandbox was started; real availability, guest trace permissions, provider filtering and guest process universe are **not verified**.
Sandbox's default network connectivity is on; a future standalone configuration would disable networking and reduce clipboard, host folder mappings, vGPU and other shared capabilities as applicable. Such configuration is not authorized now.
**Crucial privacy qualification:** a dedicated guest segregates host user processes but a guest-wide kernel ETW session may still record unrelated guest OS service activity. VM isolation alone does **not** prove all collected events are from the one intended worker. Need guest process scope/admissibility, event data minimization and a truthful scope receipt.

## P4 — Independent event and crash continuity
- Observer must start and persist readiness receipt **before** any worker launch; source enablement must be acknowledged with a definite pre-start capture window.
- Preserve session/provider identity, clock/time semantics, event sequence, `EventsLost`, `BuffersLost`, truncation and source disable/gap indicators; loss=0 is insufficient absent a complete start-to-stop coverage proof.
- Keep observer independent from supervisor: separate process/job/lifetime boundaries, capture and evidence stream kept alive through the supervisor crash; explicitly record observer startup and shutdown plus independent cleanup checks.
- Every Job member must have full `(PID, creation FILETIME)` and **specific Job handle** proof; retain member process handles for exit status. Null `IsProcessInJob` identifies membership in any Job, not the expected one.
- Reconcile Job membership snapshots with event lineage including `OTHER_IDENTIFIED_JOB_MEMBER`, `VERIFIED_DESCENDANT` and unknown members; unknown/unclassified, member handle lost or observer crash => `BLOCKED`.
- A process already terminated before observation cannot be reconstructed with a reliable historical handle; do not mint retroactive individual exit or descendant-absence proof.

## P5 — Adversarial qualification boundary
Existing frozen WER02 suite rerun: **47/47 PASS**, zero errors, proof limited to `SYNTHETIC_CONTRACT`.
Additional WER04 12-case matrix is **DOCUMENTARY**, not newly executed Windows tests or novel executable tests. It distinguishes existing synthetic coverage from gaps that remain untested. See P5 JSON matrix and captured raw/JUnit output.
Uncovered real cases: ETW permission, actual creator vs reported parent, provider-side scope, incidental third-party capture, buffers lost, observer prestart, crash witness continuity. No synthetic success promotes these.

## Future probe boundary — separate human decision
Proposed only: dedicated disposable isolated Windows guest, network disabled, one tightly controlled worker, one collector and one launcher, zero descendants; exact source/binary/ETW provider/session/filter, guest permissions, privacy scope and per-process launch ceilings must first be FROZEN. Historic 13-worker campaign and 36/14 old regression counts **remain closed/not transferable**. Current worker/ETW/probe budget = 0. No VM creation, ETW collection, worker launch or cleanup exercise is authorized by WER04.

## Source references (official Microsoft API documentation; not execution evidence)
- https://learn.microsoft.com/en-us/windows/win32/etw/controlling-event-tracing-sessions
- https://learn.microsoft.com/en-us/windows/win32/etw/configuring-and-starting-a-systemtraceprovider-session
- https://learn.microsoft.com/en-us/windows/win32/api/evntprov/ns-evntprov-event_filter_descriptor
- https://learn.microsoft.com/windows/win32/api/evntrace/ns-evntrace-enable_trace_parameters
- https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute
- https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/
- https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file

## WER04 terminal gate
`R1_CR1_WER_04 = REQUIRES_TARGETED_CORRECTION` because **four real-mechanism gates are not qualified**: collector permissions, independent parent creation identity, admissible capture scope, and event/crash continuity.
`REAL_ETW_CAPTURE=0`; `REAL_WINDOWS_PROBE=0`; `WORKERS=0`; `FC01_REAL_MEMORY_SAFETY=NOT_QUALIFIED`; `READ_A_RETRY=FALSE`; `READ_B=FALSE`; `B12=CLOSED`; `FORCE=FALSE`; `FAIL_CLOSED=TRUE`; `STOP=MANDATORY`.
