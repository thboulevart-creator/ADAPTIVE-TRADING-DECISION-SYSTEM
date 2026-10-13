# WER-03 V0.1 — Windows real-evidence readiness and future probe draft

CONTROL_ID = AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-03

## P1 — Observed, read-only Windows capabilities

- Windows 11 Professionnel N, OS 10.0.22631, x64; PowerShell 5.1.22621.6133; audit token NOT elevated.
- Present: advapi32.dll, kernel32.dll, tdh.dll; logman, wevtutil, tracerpt, wpr. xperf not found.
- Registered Microsoft-Windows-Kernel-Process: GUID 22fb2cd6-0e7b-422b-a0c7-2fad1fd0e716, 41 metadata entries.
- Event ID 1 v0 STATIC template: ProcessID, CreateTime (child FILETIME), ParentProcessID, SessionID, ImageName. It does NOT contain a parent creation FILETIME.
- Provider presence and local DLLs do NOT demonstrate ETW session permission or event authenticity. No event logs, ETW streams or third-party processes were sampled.

## P2 — Independent evidence matrix

| RC | Interface proposal | Material gap | Decision |
|---|---|---|---|
| RC-01 Immutable process identity | GetProcessTimes, retained process handle | PID + creation FILETIME lifetime/handle binding not proven | REQUIRES_TARGETED_INSTRUMENTATION |
| RC-02 Independent parent-child lineage | ETW process-start event, independently bound parent creation FILETIME | ParentProcessID is not parent creation FILETIME; timing, loss, privileges and privacy scope unresolved | INSUFFICIENT_EVIDENCE_DESIGN |
| RC-03 Specific Job membership | QueryInformationJobObject and IsProcessInJob with non-null specific Job HANDLE | Exact Job identity, buffer completeness and normal/crash full inventory unproved | REQUIRES_TARGETED_INSTRUMENTATION |
| RC-04 Per-member exit verification | Retained HANDLE, WaitForSingleObject, GetExitCodeProcess, GetProcessTimes | Crash-independent all-member handles/exits unqualified | REQUIRES_TARGETED_INSTRUMENTATION |
| RC-05 Authenticity, integrity and continuity | Observer identity, raw ETW records and TRACE_LOGFILE_HEADER EventsLost/BuffersLost | Event/session completeness, observer crash, filtering scope and authenticity unqualified | INSUFFICIENT_EVIDENCE_DESIGN |

Immutable parent identity requires event-time correlation of parent PID with a verified parent creation FILETIME. Job membership alone is NOT lineage; IsProcessInJob with NULL only checks any Job. ETW session loss counters are necessary but insufficient to prove complete coverage (for example, the session may start late).
Kernel ETW provider permission, event-source privacy scope, event completeness, and supervisor-crash continuity remain unqualified. PID filters cannot be presumed effective at the source; filtering after recording may already observe unrelated third-party processes. A confined VM/Sandbox or verified provider-side scope is a prerequisite.

## P3 — First real probe contract, draft ONLY

Proposed future isolated machine: one controlled worker, one launcher, one collector, zero descendants, one Job, maximum 15 s and 1000 event records. THESE ARE DRAFT CAPS, NOT EXECUTION AUTHORITY. Current budgets: 0 workers, 0 ETW sessions, 0 probes.
Exact immutable probe ID, provider event version, binaries, SHA-256, process/child/auxiliary budgets, permissions, privacy isolation and pre-launch ledger must be frozen by a SEPARATE human gate.
STOP on any missing/delayed event, event loss, PID reuse ambiguity, parent identity mismatch, unexpected Job member, unrelated process observation, handle loss, collector crash, or inconsistent receipt.

## P4 — Purely synthetic non-regression

Frozen WER-02 contract and adversarial suite: 47/47 PASS, zero collection errors, no worker or Windows observer.
RAW_SHA256 = 569758b88bb4f40b142b2149b5f50afc26df0e3425dde200d67cba52ffc83cb5
JUNIT_SHA256 = 7e9578ef861084634853c67a8a26df357b152c8aad4ba5bcab4ebe8a7e22872d

## Authoritative Windows API references (not runtime evidence)

- ETW Process schema: https://learn.microsoft.com/en-us/windows/win32/etw/process-v2-typegroup1
- SystemTraceProvider sessions: https://learn.microsoft.com/en-us/windows/win32/etw/configuring-and-starting-a-systemtraceprovider-session
- ETW trace security: https://learn.microsoft.com/en-us/windows/win32/api/evntcons/nf-evntcons-eventaccesscontrol
- ETW loss counters: https://learn.microsoft.com/en-us/windows/desktop/ETW/trace-logfile-header
- IsProcessInJob: https://learn.microsoft.com/en-us/windows/win32/api/jobapi/nf-jobapi-isprocessinjob
- QueryInformationJobObject: https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-queryinformationjobobject
- GetProcessTimes: https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getprocesstimes
- ETW provider filtering: https://learn.microsoft.com/fr-fr/windows/win32/api/evntrace/nf-evntrace-enabletraceex2

## Terminal boundary

R1_CR1_WER_03 = REQUIRES_TARGETED_CORRECTION
P0=PASS; P1=INVENTORIED; P2=INSUFFICIENT_EVIDENCE_DESIGN; P3=DRAFT_ONLY; P4=47/47_SYNTHETIC_PASS; P5=PENDING_GITHUB_CONFIRMATION.
REAL_WINDOWS_EVIDENCE=NOT_ACQUIRED; WINDOWS_WORKERS=0; ETW_CAPTURE=0; FC01_REAL_MEMORY_SAFETY=NOT_QUALIFIED;
READ_A_RETRY=FALSE; READ_B=FALSE; B12=CLOSED; FORCE=FALSE; FAIL_CLOSED=TRUE; STOP=MANDATORY
