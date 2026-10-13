# WER-04 V0.1 — P6 forensic report

CONTROL_ID: AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-04

## Terminal conclusion
R1_CR1_WER_04 = **REQUIRES_TARGETED_CORRECTION**. No independent real Windows event or Job evidence acquired. Design preference is **separate Windows guest** subject to unresolved prerequisites, not a runtime-ready collector.

## Fresh P0 canonical identity
Remote + local integration/system-v1 HEAD a5a6351a5cb664c1f36c3b4ee4f84c3f56a0b78d, TREE e5c5fd95917a50349c4e351c01bfcd7b42293a0f, tracked diff empty, protected FC01/E1 blobs unchanged. WER03 P5 receipt SHA256 101a3e760cb6704e6786885c15d5642003df89f404bc632e641123571663ea11; WER02 candidate SHA256 a73cc58b7b21a0c29130f07aab1173ed18a5c6947f6049036e954fd98ab447d4. RED-CR2/GREEN-R1 SHA256 conform.

## P1 privileges
Host Windows 11 Professionnel N build 22631: current process NOT admin elevated and NOT Performance Log Users. ETW provider metadata alone does not establish session privileges. A host session is NOT_QUALIFIED; no escalation allowed. Windows Sandbox feature inventory InstallState=1 and hypervisor present, but processor firmware virtualization/SLAT fields inconsistent and launchability NOT proven. A guest is conditionally preferred for confinement, not certified.

## P2 immutable parent identity
Inspected ETW Kernel-Process event 1 version 0 carries child ProcessID + CreateTime and parent PID but not parent FILETIME. Proposed retained parent handle/event-time binding and exact 64-bit FILETIME must be qualified in a later gate. Reported parent is not automatically the actual initiating creator due to PROC_THREAD_ATTRIBUTE_PARENT_PROCESS. No independent real relation acquired.

## P3 source scope
Provider-side PID filter applicability to *kernel process creation* not proven. Post-event filtering cannot eliminate prior observation. An isolated guest reduces host exposure, but guest-wide ETW can still report incidental guest processes. Actual guest permissions, admissible event scope and privacy-limited data contract remain unresolved.

## P4 event/crash continuity
Independent observer must predate worker startup, survive supervisor crash, have session/provider receipts and loss accounting plus complete specific-Job handle/member and individual termination evidence. None verified on live Windows. Missing or ambiguous evidence => BLOCKED.

## P5 observed vs designed adversarial review
Existing frozen WER02 tests were rerun: **47 PASS / 0 FAIL / 0 errors**. WER04's 12 adversarial scenarios are **a documentary matrix only**, with each case marked according to observed prior synthetic coverage or an untested gap. No 12 novel tests were executed, and zero tests of actual ETW permission, guest privacy, crash continuity or actual parent identity were performed.

Raw pytest SHA256 e968f9adb6bdb91650262f5000a8c131a3c40a1ef72455eb2097b5eab467ad7f. JUnit SHA256 30c6735fa429ba2e2a53ffe973e3d093dce4d5a125955136f836230cfe9e2837.

## P6 exact evidence inventory
| Document | SHA256 |
|---|---|
| `GOVERNANCE/AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-04-COLLECTOR-PERMISSION-LINEAGE-SCOPE-CONTINUITY-V0.1.md` | `eb608a233ece41dcced67a718e2c145261c79267bdd51b059f65e1c7b66b145a` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-04-P5-ADVERSARIAL-STATIC-MATRIX-V0.1.json` | `ae48a40540ac9f10a889c3bf74cec4c7da5bdf182c55e72ba768414b47bf331a` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-04-P5-EXISTING-SYNTHETIC-REQUALIFICATION-RAW-V0.1.txt` | `e968f9adb6bdb91650262f5000a8c131a3c40a1ef72455eb2097b5eab467ad7f` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-04-P5-EXISTING-SYNTHETIC-REQUALIFICATION-JUNIT-V0.1.xml` | `30c6735fa429ba2e2a53ffe973e3d093dce4d5a125955136f836230cfe9e2837` |

New terminal receipt and report are additional WER04-only files. No old source or WER01 local-only file is staged.

## Strict final safety boundary
```text
R1_CR1_WER_04 = REQUIRES_TARGETED_CORRECTION
P0=PASS
P1=PERMISSION_DESIGN_BOUNDED_NOT_ACTIVATED
P2=PARENT_BINDING_DESIGN_CONDITIONAL
P3=ISOLATED_GUEST_DESIGN_PREFERRED_NOT_EXECUTABLE
P4=CONTINUITY_DESIGN_CONDITIONAL
P5=47/47_SYNTHETIC_PASS_WITH_DOCUMENTARY_GAPS
P6=PENDING_FINAL_GITHUB_VERIFICATION_AT_REPORT_CREATION
WINDOWS_WORKERS=0
REAL_ETW_CAPTURE=0
REAL_WINDOWS_PROBE=0
INDEPENDENT_WINDOWS_EVIDENCE=NOT_ACQUIRED
FC01_REAL_MEMORY_SAFETY=NOT_QUALIFIED
READ_A_RETRY=FALSE
READ_B=FALSE
B12=CLOSED
FORCE=FALSE
FAIL_CLOSED=TRUE
STOP=MANDATORY
```

NEXT requires a distinct human authorization for isolated guest capability and real collector permission/scope preflight; **NOT** the 13-worker campaign or real probe execution.
