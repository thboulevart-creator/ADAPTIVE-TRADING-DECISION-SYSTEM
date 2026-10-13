# AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-02 — P1 SOURCE PROVENANCE & P2 STATIC DESIGN V0.1

## Scope and identity
Canonical branch `integration/system-v1`, HEAD `bf67850e79d776761cf34b406f218e85ba0ff9ac`, TREE `f5af0309e563be4de8cbcb5545cb10a9f88f0759`. Remote equals local; tracked diff empty at P0.

WER-01 is available **only as untracked local documents** and was NOT published to the canonical GitHub branch. Its protected SHA256: governance `aea1848a8ebb916ab3915b848aae712a22f7c2ccf50e7aeed1726590fc0e1a4f`, JSON `00a558df1efc33d3f4fa4d701300fc82bc22c0e29a198d1898cac81322761a10`, Markdown `521715e0e4255a383a81813c36675fca76e376ffbe43e7593f42f1a34d8ae01c`.

Protected tracked source FC01 blob `44ccaeafdd22cede207fef6038e5c747ff5d1454`, E1 blob `2dcacfde5fdf9b39ce0c9647c4413f2d2fc67a0b`. GREEN-R1 SHA256 `8092c558370130acd9eb16b1c3d1cfed209ff0b8b6f7e78f6a02354c2fc7f0e1`; RED-CR2 oracle SHA256 `2335423d1afe32bb9985a8a58331e3bd69ccdb811ac222cdfc197e47f3801aee`; RED-CR2 test SHA256 `cb58f8f36cb7a88ffa21ca7bbd027fa945990f582e83663313077bb43338d980`.

## P1 read-only provenance decisions

All six inputs are existing, locally untracked UTF-8 experimental candidate sources. Their **qualified role is LOCAL_REFERENCE**, not a canonical Git source, not a runtime entrypoint, and not automatically publishable. SHA256 verified on P0:

| Path suffix beneath `tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1/` | Bytes | SHA256 | Decision |
|---|---:|---|---|
| `F03CR2SupervisorR1.cs` | 24952 | `7a9685e0793e73f3590d3c70d2d0259fb4e5f5380ec2204a4ead5665e280c83f` | QUALIFIED_LOCAL_REFERENCE |
| `F03CR2RecoveryR1.cs` | 9952 | `d598b67f44c33363400d9ecbd0cca277ffd1dcca94288114ff7fd342ed36a40c` | QUALIFIED_LOCAL_REFERENCE |
| `windows_witness.py` | 3388 | `d25a55bf2d2aa457023429e31d4ae3fac0dcd1f9e8a77896ecc575d60effbbaf` | QUALIFIED_LOCAL_REFERENCE |
| `run_r1_campaign.py` | 23249 | `83f8f612b9b47b8f8cca9686e8df61ae79af975ee09aae73e010b6ec5cdc0e56` | QUALIFIED_LOCAL_REFERENCE |
| `forensic_contract.py` | 7921 | `7878c1bcefed0b275fe5b17cd375628c04e6384364fde5a28bc1dea309d5ca97` | QUALIFIED_LOCAL_REFERENCE |
| `freeze_r1_campaign.py` | 4261 | `d53d8c64945c4a5751a953ee8c75bbc9545927908e4ccc481536e72e4a3ba1d8` | QUALIFIED_LOCAL_REFERENCE |

Historical usage: supervisor and recovery create/manage a Windows Job and supervisor crash continuity; witness retains only primary-worker handle; Python runner launches scenarios and constructs receipts; forensic contract validates old tree/descendant status; freeze script preregistered old campaign budget. **None is a currently qualified independent lineage producer.** All source modifications and uploads forbidden in WER-02.

## P2 conditional independent-proof design

The following is a **STATIC DESIGN** and synthetic candidate, not a system collector or actual proof of Windows lineage. A real ETW provider/manifest/event schema and permissions must be qualified **separately** before any runtime collector is implemented or activated.

| Unit | Proposed independently verifiable producer | Offline candidate scope | Fail-closed gate |
|---|---|---|---|
| IT-01 process identity | Retained Windows process handle plus `GetProcessTimes`, pre/post FILETIME bound to PID | strict decimal FILETIME parser and pair matching | PID reused; missing/mismatched start; lossy floating-point conversion |
| IT-02 parent-child lineage | Candidate kernel process-start event stream (ETW, provider and version to be frozen later), corroborated parent handle creation identity and continuous coverage | validate *synthetic event envelopes*, parent/child process start identities, sequence/coverage and transitive lineage | absent event, dropped sequence, wrong source, parent identity unknown, event outside window, broken chain |
| IT-03 Job membership | Specific Job handle identity, full enumeration + observed PID creation FILETIME on each member at pre/post boundaries; query buffer overflow/partial listings fail-closed | validate membership statements for **same specific synthetic Job identity** and counter/list consistency | wrong Job, duplicated member, partial query, unclassified member |
| IT-04 member exit | Retained handle per member, `WaitForSingleObject`, `GetExitCodeProcess` and matching post identity; supervisor-crash witness coverage needs separate design | validate synthetic exit evidence for **every** member | lost handle, still-active exit, inconsistent start identity, missing post-state |
| IT-05 receipt consistency | Versioned raw-evidence envelope, protected source hashes, independently produced member classifications, full inventory and final receipt | strict schema of synthetic receipt, expected lineages and absence, SHA256 over canonical fixture payload | receipt disagreement, false Windows provenance, missing coverage, missing classifications |

Synthetic event source label `ETW_KERNEL_PROCESS_PROPOSED` is **only an offline tag**; it is not a verified Windows event producer. Fixture booleans do not establish OS provenance. A complete event range and empty missed-events claim are merely synthetic *design assertions*, never proof of actual ETW continuity.

In particular **`Job Object membership != parent-child relationship`**. A parent PID is insufficient without verified creation FILETIME and event-time correlation; an absence claim is blocked if any event-loss or job-inventory gap exists. External/unrelated Job members need a corroborated event-time non-descendant lineage. Transitive descendants must be classified from the complete chain, not inferred by mode name.

## Readiness and freeze boundary

This design supports only test-first **offline simulation** and no Windows supervisor, ETW session, real Job Object, process worker, runtime activation, JForex call, privileged operation or external network access.

Future 13-worker campaign, per-scenario descendant/auxiliary budgets, exact regression node IDs and immutable binary freeze **NOT authorized or assigned**. Historic 36 supervised and 14 Java regressions have no transferable authority.

```text
P1 = QUALIFIED_LOCAL_REFERENCE_ONLY
P2 = QUALIFIED_STATIC_DESIGN_FOR_SYNTHETIC_CANDIDATE_ONLY
INDEPENDENT_WINDOWS_EVIDENCE = NOT_ACQUIRED
WINDOWS_COLLECTOR_IMPLEMENTATION = FORBIDDEN
WINDOWS_WORKERS = 0
WER01_GITHUB_PERSISTENCE = BLOCKED
FORCE = FALSE
FAIL_CLOSED = TRUE
```
