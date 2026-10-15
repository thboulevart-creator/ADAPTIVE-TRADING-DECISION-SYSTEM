# WER-05-ALT-02 V0.1 — Hosted Windows capability preflight

**Terminal verdict:** `HOSTED_WINDOWS_CAPABILITY_PREFLIGHT_PASS` — restricted to static/metadata-only preflight.  
**STOP:** `APPLIED`; no further job authorized.  
**Authority:** explicitly human adopted one hosted `windows-2025` GitHub Actions job, no ETW start, no worker, no Job Object creation, no Sandbox, no real capture.

## 1. Provenance and immutable references

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`; canonical branch `integration/system-v1`, not `main`.
- Human-authorized input HEAD `8650034a82fbb8a5f3be7769f1ad7cd3c4d61f6d`, TREE `1aed2c12c7d0f64df11f1d2118b5f4e8f4404950`. These exact refs were verified before publication.
- One new-only workflow `.github/workflows/wer-05-alt-02-hosted-windows-capability-preflight.yml`; Git blob `5cf5796ebc00b6daa44dba0117403649766bba21`, published via a **single** non-forced branch ref move with expected parent HEAD.
- Executed commit HEAD `2d91a97b9fd1b6b6fbbe465ac708e399e0bddebf`, TREE `ec74473ae6de8510d5b37092041d1107dc04a8d9`. Parent `8650034a82fbb8a5f3be7769f1ad7cd3c4d61f6d`. Exactly one changed file (added workflow).
- Commit message pre-registered and matched exactly: `WER-05-ALT-02-V0.1 ONE-SHOT AUTHORIZED CAPABILITY PREFLIGHT`.
- Run ID `38707799690`, job ID `116331438391`, attempt `1`, `push` event, **one** job named `capability`, GitHub conclusion `success`. Action log timestamp of actual inventory `2026-10-15T08:44:19.5881924Z`.
- User-visible run: https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/38707799690
- GitHub Actions API filtered on this commit SHA returned **exactly one run**, the authorized workflow. No other run for that SHA was returned at inspection time.

## 2. P0 — Existing workflow trigger audit

- GitHub canonical HEAD/TREE matched at start; ALT-02 path did not exist (404 absence/collision check).
- Compared local historical HEAD `9ed38d72580635d9a63eff76cf6196123be2d8a1` to canonical input: exactly three later commits adding six files; **no existing workflow files changed**. This allowed read-only inspection of the identical historical workflow tree locally, with no checkout/reset/clean/pull.
- All **185 existing** YAML workflows inspected. 184 declared `push`; 180 could match the governed branch; **zero** preexisting `push` filters matched the proposed ALT-02 workflow path; **zero** on this branch had no paths filter; **zero** `workflow_run` triggers were detected.
- Two proposed evidence paths in `reports/program` were also statically checked against those 185 triggers; zero matching `push` path patterns found. One isolated ALT-02 push job was subsequently confirmed by GitHub.
- The workflow uses only a branch/path-filtered `push` event and exact commit-message job guard; no `workflow_dispatch`, `pull_request`, `schedule` or `workflow_run`. Its single source addition was proven with a post-publication GitHub commit comparison.
- No guarantee about actions taken on unrelated future repository pushes is claimed.

## 3. P1 — Static candidate qualification

- Python YAML BaseLoader parsed the candidate: exactly one `on.push` event, one branch `integration/system-v1`, one exact-path filter, one `windows-2025` job, five-minute timeout, one metadata-only PowerShell step.
- `permissions: {}`; concurrency group `wer-05-alt-02-v0-1-single-capability-job`, `cancel-in-progress: false`.
- No `actions/checkout`, external `uses`, dependency download, secrets, token emission or deployment.
- No ATDS business source is executed. No process inventory, third-party process collection, Job creation, ETW session start or process termination instruction appears in the step.
- Runtime checks the governed ref and `GITHUB_RUN_ATTEMPT=1`. Native `logman.exe query providers` is used only for provider **metadata**, never for `logman start`/capture.

## 4. P3 — Actually observed Windows runner results

**Authoritative source:** the structured, whitelisted JSON output in job ID `116331438391` log, plus GitHub run and job metadata (not assertions from a local simulator).

| Property | Actual value |
|---|---|
| Runner image version | `20260925.250.1` |
| OS version / build | `10.0.26100` / `26100` |
| Architecture | `64-bit` |
| PowerShell | `7.6.6` |
| Total physical memory | `15.99 GiB` |
| Logical processors | `4` |
| Admin token | `true` |
| Performance Log Users member | `false` |
| `kernel32.dll`, `advapi32.dll`, `tdh.dll` | all present `true` |
| `logman.exe`, `wevtutil.exe`, `tracerpt.exe` | all available `true` |
| `GetProcessTimes`, `QueryInformationJobObject`, `IsProcessInJob` | all exported `true` |
| `Microsoft-Windows-Kernel-Process` provider registered | `true` |
| Internal metadata summary | `METADATA_COMPLETE` |
| Run attempt / job result | `1` / `success` |

The workflow reported `etw_permission_tested=false`, `etw_session_started=false`, `atds_worker_started=false`. GitHub job metadata confirms all three structural steps ("Set up job", inventory, "Complete job") succeeded. The Windows GitHub host itself is provisioned by GitHub; the workflow did not create any nested VM.

## 5. Scope limitations — expressly NOT proven

- Administrative token and DLL/API/provider registration do **NOT** establish actual privilege to start a kernel ETW session or permission to collect it; **no ETW session was started**.
- Exported API symbols do **NOT** prove runtime Job Object membership, accurate PID plus creation FILETIME, parent-child causal ancestry, per-member exit receipts or supervision on failure; none were exercised.
- Host-wide ETW could capture incidental runner system or GitHub processes. Privacy/source-side provider filtering and acceptable process capture boundaries remain unqualified. No raw process event captured or published.
- The `windows-2025` runner image is a temporary hosted Windows environment, **not an assertion of equivalence to Windows 11 Pro N build 22631** or to Windows Sandbox. Any environment substitution requires independent human adjudication.
- Runner auto-disposal at job end is **not** proof of independent process cleanup by ATDS, ETW continuity or controlled termination.
- A completed single job does not qualify an independent supervisor, exact crash lineage, full evidence chain, event-loss counters, memory enforcement, guest teardown or the historical one-shot WER-05 launch.

## 6. Terminal authority firewall and next separate gate

```ini
WER_05_ALT_02=HOSTED_WINDOWS_CAPABILITY_PREFLIGHT_PASS
P0=PASS
P1=PASS_STATIC
P2=ONE_NEW_WORKFLOW_ONLY_PUBLISHED
P3=ONE_RUN_ONE_JOB_SUCCESS_METADATA_COMPLETE
P4=NEW_REPORT_AND_RECEIPT_AUTHORIZED
REAL_ETW_SESSION_STARTS=0
REAL_ETW_CAPTURE=0
ATDS_EXPERIMENTAL_WORKERS=0
REAL_JOB_OBJECT_CREATION=0
SANDBOX_LAUNCHES=0
EXPERIMENTAL_PROCESS_TERMINATIONS=0
PRIVILEGE_ESCALATION=0
HOST_CONFIGURATION_MUTATION=0
MAIN_BRANCH_MUTATION=0
HISTORICAL_EVIDENCE_MUTATION=FALSE
RETRIES_CONSUMED=0
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

**Next requires a separate human authority:** choose and preregister a privacy-safe hosted Windows permission/scope qualification plan, with limits on incidental runner process observation and unambiguous provenance. No authority to run ETW, worker, trace collector or supervisor follows from ALT-02 PASS.
