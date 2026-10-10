# BEPD-09D-R2-RD6-03B-P0-CR3 — Windows Sandbox and RFC 8785 Readiness V0.1

**Evidence date:** 2026-10-10.  
**Human authorization:** BEPD-09D-R2-RD6-03B-P0-CR3 V0.1; documentary persistence reauthorized under BEPD-09D-R2-RD6-03B-P0-CR3-R1 V0.1.  
**Verdict:** PARTIAL_EVIDENCE_OBTAINED; FULL_P0_READINESS = BLOCKED.  
**Evidence type:** Historical observations recorded during CR3, no additional Windows/PyPI diagnostics for R1.

## 1. Requalified GitHub checkpoint

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`.
- Governing branch: `integration/system-v1`.
- Originally authorized CR3 HEAD: `416e6e6cee24e8297c855ed5ac68bf7e4154c188`.
- Originally authorized CR3 TREE: `ba018026a8edbe59b68053256bb7abc437146b52`.
- CR3-R1 specifically requalified HEAD: `e29768459414ef28dc1099590c1dd9e518c71b14`.
- CR3-R1 requalified TREE: `d8ef2bfb90a0a4705b56de578eb14534c9d41eda`.
- Fresh HEAD and TREE matched before documentary staging.
- Historical drift comparison from the original CR3 HEAD: 2 commits ahead, 0 behind. Exactly two added files:
  - `GOVERNANCE/E1-TD-03C-JF02-D1-FINAL-HUMAN-ADJUDICATION-CLOSURE-2026-10-10.md`
  - `GOVERNANCE/E1-TD-03C-JF02-D1-HUMAN-ADOPTION-RECEIPT-V0.1.json`
- No existing file modifications in the compared delta. Classification: **non-material for CR3 documentary publication only**; no cross-lane adoption or authority.
- **17/17 specifically pinned protected files** from CR2, MAT-01, RD6-03A, RD5 and RD3 matched the exact expected Git blobs on CR3-R1 preflight.
- Both proposed CR3 documentary paths were unoccupied at the requalified tree. No CR3 source or executable changes are authorized.

### Critical identity binding

| Protected artifact | Git blob |
|---|---|
| CR2 governance document | `b524a87b1b125fa675b5f09befe59a082fcf5103` |
| CR2 evidence receipt | `cbc59442bdf1d912b4594a4211723b21484a2a82` |
| MAT-01 human decision | `92a37a92cc8f881bcc28613bb18aa2b89c77d218` |
| MAT-01 adoption receipt **corrected authoritative identity** | `081087fd7479b9b197012b1c653457c8187c1249` |
| RD6-03A test matrix | `7558e6166888c94eca7069a08d095dfda18fd190` |
| RD6-03A breaker matrix | `38863439059d1a2f45aa4c877245613cd48fdc51` |
| RD5 synthetic fixture implementation | `c6d8b0e678270e379e758052c40be23355bc3800` |
| RD3 Candidate B implementation | `38588b0a0b9c5b4cb9fcee0c7d524e63d5039c69` |

The contradictory MAT-01 receipt value in an earlier quotation within the human authorization is explicitly superseded by the corrected authoritative value above; the incorrect value is **not accepted as a binding**.

## 2. CR3-A — Windows Sandbox historical evidence

Windows host accessed for CR3: `DESKTOP-49BN9M3`. Read-only PowerShell command targeted the official optional feature `Containers-DisposableClientVM`.

Observed result:

```text
WINDOWS_SANDBOX_EXECUTABLE = PRESENT (from previously persisted CR2)
WINDOWS_FEATURE_QUERY = EXECUTED
WINDOWS_FEATURE_STATE = UNKNOWN
WINDOWS_FEATURE_QUERY_RESULT = COMException
SANDBOX_ACTIVATION_READINESS = NOT_ASSESSABLE
SANDBOX_LAUNCHES = 0
FEATURE_ACTIVATIONS = 0
HOST_REBOOTS = 0
```

The registry returned product label `Windows 10 Pro N`, display version `23H2`, build `22631`. These are host observations and do not independently establish Sandbox activation. Historical CR2 reported a present hypervisor and `vmcompute` running. The later read-only CR3 query did not produce an authoritative `ENABLED`, `DISABLED`, or `ENABLE_PENDING` state. **No UAC elevation was performed.**

The restrictive `.wsb` profile remains **SPECIFICATION_NOT_EXECUTED** because the required enabled feature state was not proven. Candidate future configuration only (not a deployed file): `Networking=Disable`, `ClipboardRedirection=Disable`, `PrinterRedirection=Disable`, `AudioInput=Disable`, `VideoInput=Disable`, `vGPU=Disable`, `ProtectedClient=Enable` if supported, zero mapped folders, zero logon commands, zero real-data mounts, no credentials. No Windows Sandbox was launched or certified.

## 3. CR3-C — PyPI wheel identification and static integrity

CR3 executed exactly one authorized metadata request to the official version-specific PyPI API endpoint `https://pypi.org/pypi/rfc8785/0.1.4/json`; it returned a single matching wheel record:

```text
PACKAGE = rfc8785
VERSION = 0.1.4
WHEEL = rfc8785-0.1.4-py3-none-any.whl
REQUIRES_PYTHON = >=3.8
SIZE = 9240 bytes
OFFICIAL_PYPI_SHA256 =
520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48
```

One authorized download from the exact wheel URL under `files.pythonhosted.org` into an ephemeral Windows TEMP staging folder succeeded. The downloaded wheel was **not** installed or imported. The SHA-256 computed over downloaded bytes matched the official metadata SHA-256 **exactly**, and the file size matched 9,240 bytes.

```text
ACTUAL_DOWNLOADED_SHA256 =
520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48
ACTUAL_FILE_SIZE = 9240 bytes
OFFICIAL_DIGEST_MATCH = PASS
OFFLINE_WHEEL_IDENTITY = VERIFIED_AGAINST_PYPI_METADATA
```

### ZIP and distribution metadata inspection

The first ZIP inventory attempt failed to load a .NET ZIP class. This failed inspection was not counted as a PASS. A subsequent static inspection succeeded using the built-in `System.IO.Compression.FileSystem` assembly, without installing or importing the wheel:

```text
ZIP_ENTRIES = 7
UNSAFE_ARCHIVE_PATHS = 0
UNEXPECTED_NATIVE_EXECUTABLES = 0
DIST_INFO_METADATA = PRESENT
DIST_INFO_RECORD = PRESENT
DIST_INFO_WHEEL = PRESENT
PACKAGE_NAME_MATCH = PASS
PACKAGE_VERSION_MATCH = PASS
REQUIRES_PYTHON_MATCH = PASS
WHEEL_TAG = py3-none-any
BASE_RUNTIME_DEPENDENCIES = NONE_DECLARED
```

Verified inventory contains two Python source files, a typed marker and the distribution metadata/license/RECORD. The WHEEL/METADATA names and versions correspond to the downloaded filename. No archive path traversal or native executable was observed. The `RECORD` was found and its presence/shape examined; a complete independent verification of each inner RECORD hash was **not performed**.

The result demonstrates byte-level equality with the artifact catalogued by PyPI and bounded ZIP/metadata consistency. **It does not establish third-party supply-chain security or RFC 8785 functional correctness.**

## 4. CR3 invocation and prohibition receipt

- Windows feature state read-only query: 1, returned UNKNOWN/COMException.
- PyPI metadata HTTP requests: **1**.
- Authorized wheel downloads: **1**.
- ZIP/static artifact inspections: **3 attempts**, first unsuccessful, subsequent archive inventory and distribution metadata read successful.
- Total remote diagnostic process invocations: **6**.
- Host-side measured command-body elapsed times (reported by internal stopwatch on the individual commands): 153 ms, 327 ms, 460 ms, 171 ms, 111 ms and 96 ms. These are partial per-command durations; full end-to-end host process wall-time was **not independently attested**.
- The user-authorized individual diagnostic cap was 10 seconds, total diagnostic cap 120 seconds. The recorded stopwatch portions were below these caps, but no claim of fully independently qualified aggregate duration is made.
- Windows feature activations: **0**. Sandbox launches: **0**. Host reboots: **0**.
- Package installations: **0**. Windows/Python modifications to ATDS: **0**. RED/GREEN invocations: **0/0**. Real-data reads: **0** by this activity. Model fits: **0**. External spending: **0**.
- No new PyPI requests, Windows queries, wheel downloads or Windows diagnostics are authorized in R1 and none are part of this documentary R1 execution.

The wheel was downloaded to a **Windows temporary staging directory**, not the GitHub repository or a real-data path. No package binary is included in the GitHub commit.

## 5. Verdicts and evidence limits

| Component | Exact outcome |
|---|---|
| R1 GitHub checkpoint requalification | PASS at preflight; recheck and publication CAS/readback still required |
| Protected Git blobs | 17/17 PASS |
| Concurrent documentary drift | NON_MATERIAL_FOR_CR3_DOCUMENTARY_PERSISTENCE |
| Windows Sandbox activation readiness | NOT_ASSESSABLE |
| Restrictive Sandbox configuration | SPECIFICATION_ONLY_NOT_EXECUTED |
| RFC 8785 wheel SHA-256 and size | PASS |
| RFC 8785 ZIP/metadata static checks | PASS within enumerated checks |
| RFC 8785 functional JCS qualification | NOT_EXECUTED_NOT_QUALIFIED |
| Ed25519 functional integration | NOT_QUALIFIED |
| OS/network/filesystem isolation | NOT_PROVEN |
| Full P0 readiness | BLOCKED |
| Real training readiness | BLOCKED |

```text
CR3_EVIDENCE = PARTIAL_EVIDENCE_OBTAINED
CR3_SANDBOX_FEATURE_READINESS = NOT_ASSESSABLE
CR3_RFC8785_ARTIFACT_READINESS = OFFLINE_ARTIFACT_INTEGRITY_VERIFIED
CR3_RFC8785_FUNCTIONAL_READINESS = NOT_QUALIFIED
RD6_03B_EXECUTION = SUSPENDED
RD6_03B_RED_TESTS = 0
RD6_03B_GREEN_TESTS = 0
RD6_04 = NOT_AUTHORIZED
REAL_TRAINING_READINESS = BLOCKED
HUMAN_ADOPTION_OF_CR3_RESULTS = PENDING
AUTOMATIC_NEXT_STAGE = FORBIDDEN
STOP = MANDATORY
```

## 6. Separate next human frontiers

1. **Windows Sandbox activation-state verification**, with a separately authorized administrative read-only technique; no implicit activation, VM start or host reboot.
2. **Offline RFC8785 functional vector qualification**, with a separately authorized isolated test environment and fixed public vectors; no real datasets and no RD6-03B RED/GREEN.

No further CR3 diagnostics, installation, scientific source modification, code execution or stage progression is authorized by R1. Completion of GitHub persistence only records prior observations; it does not certify the environment.
