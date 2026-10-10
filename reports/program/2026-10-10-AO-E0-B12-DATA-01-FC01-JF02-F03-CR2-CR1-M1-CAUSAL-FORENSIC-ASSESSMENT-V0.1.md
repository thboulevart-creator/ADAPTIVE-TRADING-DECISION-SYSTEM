# AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M1 — Independent memory peak accounting forensic V0.1

**Date:** 2026-10-10
**Terminal decision:** `ROOT_CAUSE_NOT_PROVEN`
**Budget consumed:** 4/8 pre-authorized synthetic process executions
**Provider calls / FC01 cutover:** 0 / FORBIDDEN

## Governing identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`, branch `integration/system-v1`.
- Authorized reference HEAD: `94bd5f75ecc9763d093de9eca19ae58bccbf7d1e`.
- Pre-execution current HEAD: `724340048e83a2d588828eb4c096cfffc49616f7`.
- Concurrent difference: two documentary BEPD additions, non-material to FC01/M1, reconciled via read-only blob checks and non-destructive fast-forward.
- FC01 canonical Java blob: `44ccaeafdd22cede207fef6038e5c747ff5d1454` (unchanged).
- E1 Java blob: `2dcacfde5fdf9b39ce0c9647c4413f2d2fc67a0b` (unchanged).

## Experimental method (frozen before runs)

The M1 frozen packet pre-registered four executions in this order: A1 96 MiB, B1 512 MiB, A2 96 MiB, B2 512 MiB. Each worker used Win32 `VirtualAlloc(MEM_RESERVE | MEM_COMMIT)` in 16-MiB increments, with an upper target of 192 MiB. Each allocation step was followed by a worker file-event handshake; the supervisor measured **before acknowledging** the event, so the worker remained alive during observation.

M1 is a synthetic C# native memory forensic instrument, never a real JForex worker. A new suspended worker process was assigned to a Windows Job Object with `JOB_OBJECT_LIMIT_JOB_MEMORY` before resume. The instrument recorded timestamps, Job Object current and peak memory (information classes 28 and 9), PSAPI `GetProcessMemoryInfo` private and resident bytes, .NET `Process.PrivateMemorySize64` and working-set bytes, allocation result and Win32 last error. These measurement paths share the Windows kernel; they are not independent kernel implementations.

Source freeze SHA-256: `1c5b2f63542087d02aea54514f36b92f043a3485c935e6c1086a72fe384d9730`.
Instrument source SHA-256: `c9b4d26cb569147781f382efd16636a4d34eb5a92dd6b7a2a40080a85ecdfec7`.
Instrument binary SHA-256: `271b2256ac484b33e7c95a6ae29c6b901765d3e97f4459bba7c0ca62c95b2e9f`.

## Quantitative results

| Run | Job limit | Allocations completed | Result | Worker status |
|---|---:|---:|---|---|
| A1 | 96 MiB | 4 × 16 MiB | Fifth increment refused (Win32 1455) | Exit 42 |
| B1 | 512 MiB | 12 × 16 MiB | 192 MiB committed | Exit 0 |
| A2 | 96 MiB | 4 × 16 MiB | Fifth increment refused (Win32 1455) | Exit 42 |
| B2 | 512 MiB | 12 × 16 MiB | 192 MiB committed | Exit 0 |

**A1:** Before failed attempt, Job current = 84,901,888 bytes and `PeakJobMemoryUsed` = 84,901,888 bytes. After failure, current = 84,901,888 bytes, PSAPI PrivateUsage = 79,314,944 bytes (unchanged), peak = 101,711,872 bytes. Thus **peak delta = 16,809,984 bytes**, which equals attempted 16-MiB allocation **plus 32 KiB**. The peak exceeds configured limit by 1,048,576 bytes.

**A2:** Job current = 84,926,464 bytes before and after failure, PrivateUsage = 79,339,520 bytes before and after, peak changes from 84,926,464 to 101,736,448 bytes. Again **peak delta = 16,809,984 bytes** (attempted 16 MiB + 32 KiB). Peak exceeds limit by 1,073,152 bytes.

Both information classes 9 and 28 returned identical peak values in each observation. The worker remained alive and paused at the measurement boundary after receiving its allocation failure. On B1 and B2, `JobMemory` and the peak tracked rising committed memory during twelve successful 16-MiB increments. A distinct worker PID was observed for each of the four runs. No M1 worker remained active at the end.

Exact unabridged chronological CSV files and their SHA-256 hashes are included as embedded base64 fixtures in the JSON evidence receipt. In M1 itself, these four runs consumed only 4 of the 8 permitted experimental executions.

## Causal hypothesis adjudication

| Hypothesis | Discriminating observation | Assessment |
|---|---|---|
| H1: Windows raises peak memory accounting on a failed commitment request, before reversing/refusing the charge | Two cases show a peak jump equal to requested bytes plus exactly 32 KiB, while current job and process private memory do not rise | **Strongly supported, internal cause NOT_PROVEN** |
| H2: Incorrect P/Invoke layout causes false reads | Prior x64 offset check PASS; independent classes 9/28 agree | Disfavored, but both depend on kernel state |
| H3: Committed bytes actually exceeded the configured cap | PSAPI private usage and class-28 JobMemory remain below cap and unchanged after denial | Contradicted by these synchronized measurements |
| H4: The apparent peak comes only from querying after worker termination | Peak observed while worker paused alive before acknowledgement and exit | Disfavored |
| H5: A second unobserved process inflated job memory | A single worker PID was tracked, but JobObjectBasicProcessIdList was not independently sampled | Not fully excluded by the M1 trace |

**Interpretation:** These measurements demonstrate the *observable* increase of a peak counter associated with a failed commitment request, without a corresponding persistent increase in currently committed private memory. The exactly reproducible +32-KiB difference is an unexplained quantitative remainder, not proof of a documented Windows kernel algorithm. Available official documentation describes committed-memory limits, error-on-exceed semantics, and continuously tracked peaks, but does not explicitly establish that failed attempted commits are charged to the peak. Consequently, no internal Windows cause can be promoted to `ROOT_CAUSE_PROVEN` under the human-adopted M1 standard.

## Tests, limits and governance

- M1 evidence-replay assertions: **13/13 PASS**.
- M1 plus previous CR2/CR1/FC01/E1 baseline: **116/116 PASS**, exit 0.
- FC01 existing Maven compilation: **PASS, offline**.
- Existing CR2 supervisor, worker and recovery sources: **UNCHANGED**.
- Production FC01, E1, DATA-01: **UNCHANGED**.
- No provider request, login, credential use, real history read, trading or B12 opening.
- The source for M1 instrumentation is forensic-only and not eligible for runtime cutover.
- No more experiments may be run automatically: `STOP_AFTER_F03_CR2_CR1_M1`.

## Sources

- [Microsoft JOBOBJECT_EXTENDED_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information).
- [Microsoft JOBOBJECT_BASIC_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information).
- [Microsoft VirtualAlloc](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualalloc).

The direct observation is stronger than the existing CR2-CR1 evidence but does not by itself supply a verified model of the internal Windows accounting transition. **Next decision:** separately adjudicate whether the operational memory gate can be specified entirely in terms of *current committed JobMemory plus refusal and termination*, while retaining `PeakJobMemoryUsed` as diagnostic-only. Such a change would be a separate runtime/instrumentation design authorization; none is included in M1.
