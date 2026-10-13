# WER-02 — TARGETED WINDOWS PROOF-DESIGN CANDIDATE, FORENSIC V0.1

## Terminal classification

```text
CONTROL_ID = AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-02
DECISION = HUMAN_ADOPTED_AND_EXECUTION_AUTHORIZED
TECHNICAL_RESULT = PASS_STATIC_INSTRUMENTATION_CANDIDATE_QUALIFIED
SCOPE = OFFLINE_SYNTHETIC_DESIGN_ONLY
P0 = PASS
P1 = QUALIFIED_LOCAL_REFERENCE_ONLY
P2 = QUALIFIED_STATIC_DESIGN_FOR_SYNTHETIC_CANDIDATE
P3 = PASS_TEST_FIRST_AND_ISOLATED_CANDIDATE
P4 = PASS_STATIC_SYNTHETIC_QUALIFICATION
P5_GITHUB = PENDING_VERIFIED_PUBLICATION_AT_REPORT_CREATION
REAL_WINDOWS_EVENT_CAPTURE = 0
WINDOWS_WORKERS = 0
WINDOWS_CAMPAIGN = FORBIDDEN
FC01_CUTOVER = FORBIDDEN
FORCE = FALSE
FAIL_CLOSED = TRUE
STOP_AFTER_R1_CR1_WER_02 = MANDATORY
```

## P0 canonical and historical source protection

GitHub/local HEAD `bf67850e79d776761cf34b406f218e85ba0ff9ac`, TREE `f5af0309e563be4de8cbcb5545cb10a9f88f0759`. Tracked diff empty at P0. FC01 Git blob `44ccaeafdd22cede207fef6038e5c747ff5d1454`; E1 Git blob `2dcacfde5fdf9b39ce0c9647c4413f2d2fc67a0b`. Existing GREEN-R1 SHA256 `8092c558370130acd9eb16b1c3d1cfed209ff0b8b6f7e78f6a02354c2fc7f0e1`. Existing RED-CR2 SHA256 `2335423d1afe32bb9985a8a58331e3bd69ccdb811ac222cdfc197e47f3801aee`.

WER-01 local documents remain **not canonically published**. WER-02 is not authorized to stage those historical WER-01 documents. Their three verified SHA256s and full local provenance appear in the adjacent JSON receipt.

## P1 source provenance

The six historical Windows sources are **QUALIFIED_LOCAL_REFERENCE**, UTF-8 valid, SHA256 verified, but `UNTRACKED` and absent from canonical GitHub. None is silently promoted. Their full paths and hashes are in the adjacent governance P1/P2 document and JSON.

A local source SHA256 is evidence of local bytes only; it is **not** a Git commit identity or proof of code origin.

## P2 evidence architecture (design, not implementation)

- **IT01:** strict (PID, creation FILETIME) identity, pre/post handle correlation; FILETIME strings kept exact and numeric floats refused.
- **IT02:** candidate event-time parent/child chain, proposed ETW kernel process-start telemetry, observer identity, event continuity, sequence, timestamp, parent creation binding. Exact provider/manifest, capture permission, event source continuity, and real parent evidence remain unqualified.
- **IT03:** exact specific-Job ID, complete pre-termination inventory, verified membership, count and member identity correspondence; wrong Job blocks.
- **IT04:** per-member retained-handle, exit wait, code and post-identity, plus complete Job post-state. Crash continuity not acquired.
- **IT05:** versioned canonical synthetic envelope and receipt checksum/classification; a SHA256 over a self-asserted fixture gives **integrity consistency, not independent event authenticity**.

No actual ETW session, Win32 Job API, supervisor, Java mock or process worker was executed. The candidate `candidate.py` is pure Python and reports `collector_implemented=False`, `independent_windows_evidence=False` and `production_qualification=False` under every result.

## P3 test-first RED, then bounded candidate construction

The new WER-02 test contract was authored and frozen before creating `candidate.py`.

A deliberately permissive, in-test synthetic comparator (NOT a historical Windows validator) produced **35 assertion failures / 35 tests / 0 collection errors**. This demonstrates the test contract's requirements relative to a model that accepts favorable assertions. It does not demonstrate 35 actual historical source defects.

The initial isolated candidate passed 35 contract tests. A separately written adversarial suite discovered **6 further defects out of 12 synthetic cases**: unaccounted process start, recycled PID in event stream, contradictory global receipt, out-of-order event times, and over-claimed nested Windows provenance. Initial 12-test failure evidence was frozen **before** modifying the new candidate. Corrections were isolated strictly to `wer_02/candidate.py`; historical sources were not changed.

## P4 observed results

| Suite | Tests | Passed | Failed | Collection errors | Meaning |
|---|---:|---:|---:|---:|---|
| WER02 synthetic GREEN (35 contract + 12 adversarial) | **47** | **47** | **0** | **0** | Static envelope checks |
| GREEN-R1 frozen non-regression | **56** | **56** | **0** | **0** | Preserved |
| RED-CR2 frozen non-regression | **12** | **12** | **0** | **0** | Preserved |
| Original mixed RED frozen non-regression | **12** | **1** | **11 expected** | **0** | Original INCONCLUSIVE unchanged |

Python AST parsing passed. No Windows application was compiled or executed; these are offline contract tests. Raw pytest outputs and JUnit XML were captured as separate evidence, with their exact SHA256 in the manifest below.

## P5 evidence inventory

| Artifact | SHA256 |
|---|---|
| `GOVERNANCE/AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-02-P1-P2-PROVENANCE-AND-PROOF-DESIGN-V0.1.md` | `6e49196e9177c9a9a6b10237c1d23d358ebf2ad3db940568042532fb62d0f9a5` |
| `tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/wer_02/candidate.py` | `a73cc58b7b21a0c29130f07aab1173ed18a5c6947f6049036e954fd98ab447d4` |
| `tests/test_fc01_f03_cr2_cr1_m2_r1_cr2_cr1_r1_cr1_wer_02_contract.py` | `2ef36d7c709ca5630410da59f30ff4ba5671f381b0159c359519b5924a8c675a` |
| `tests/test_fc01_f03_cr2_cr1_m2_r1_cr2_cr1_r1_cr1_wer_02_adversarial.py` | `4766631237ebc1f3244520dafeeb14d08b2b84340ef31eef1e46810b4f0f2ad6` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-02-P3-TEST-FIRST-SYNTHETIC-RED-RAW-V0.1.txt` | `675c5ab5a9df5c59d2552023b07d059223ca30df8ccdeb16961e160cdf2c611d` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-02-P3-TEST-FIRST-SYNTHETIC-RED-JUNIT-V0.1.xml` | `a0edc34f2020a8e4cfcd26b2c22cbc5dd4a7dc46c58f6797c1352f9bbbe3e696` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-02-P4-ADVERSARIAL-RED-RAW-V0.1.txt` | `ee8afff9a639c41a16cdc201375708cf1096706a49509897c5a7f9b947f08235` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-02-P4-ADVERSARIAL-RED-JUNIT-V0.1.xml` | `bdb004f8bc7846bd0dc19c197389706c8c4c3732a130509b8a1769745af62000` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-02-P4-WER02-GREEN-RAW-V0.1.txt` | `570c6e9c4955f2685f7810b90bad4d957301deb18eac3f829edd4883bd1328d0` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-02-P4-WER02-GREEN-JUNIT-V0.1.xml` | `d2a1c8c18487eb146ac3ff4e1ae28b63a66f6613e7c150079ce44ef5e60d6840` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-02-P4-GREEN-R1-NONREGRESSION-RAW-V0.1.txt` | `c3512826a80356d496338dab5848899b839939ec695ed0ddbc4ccdd839394850` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-02-P4-GREEN-R1-NONREGRESSION-JUNIT-V0.1.xml` | `6f9af0202b6d161a6af1ce8e6e2f011757c03dfa1ceb4a73b05954c84cb1772f` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-02-P4-RED-CR2-NONREGRESSION-RAW-V0.1.txt` | `244f5e6e1d58dfb1117b15ffb03e93fbb483a6c58d30822120bd270c0326f47a` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-02-P4-RED-CR2-NONREGRESSION-JUNIT-V0.1.xml` | `9dddf1dc812119ed721ce907930ee5cf538dfa107e2641ac7077bc8b4e860410` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-02-P4-ORIGINAL-RED-UNCHANGED-RAW-V0.1.txt` | `0be343851edba2439b5ceabee6eb5198e41c9e47ee902e2de9bf643f67898589` |
| `reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-WER-02-P4-ORIGINAL-RED-UNCHANGED-JUNIT-V0.1.xml` | `c4f0d2b8164c78ee36752075823228877c27066319913409294085b2e7f0f73c` |

All original historical evidence and local-only Windows sources remain protected and outside the exact staged scope. Any raw pytest/JUnit whitespace must be preserved byte-for-byte (not normalized to satisfy `git diff --check`).

## Constraints and next phase

WER02's positive verdict is **only an isolated static/synthetic candidate qualification**, never proof that the actual Windows collector observes trustworthy lineages. Real ETW provider/manifest selection, permissions, event-loss detection, complete Job-member exit observation (particularly supervisor crash), and canonical source provenance for historical R1 sources require additional independent qualification.

A future 13-worker Windows campaign needs an explicit separate human authorization, its own new immutable source/binary/parameter freeze, exact per-scenario child and auxiliary process budgets, separate exact regression budget, and an execution-gated persistent launch ledger. None was established by this mission.

```text
R1_CR1_WER_02 = PASS_STATIC_INSTRUMENTATION_CANDIDATE_QUALIFIED
INDEPENDENT_WINDOWS_EVIDENCE = NOT_ACQUIRED
FC01_REAL_MEMORY_SAFETY = NOT_QUALIFIED
READ_A_RETRY = FALSE
READ_B = FALSE
B12 = CLOSED
WINDOWS_CAMPAIGN = FORBIDDEN
WORKER_LAUNCHES = 0
PROVIDER_REQUESTS = 0
JFOREX_CONNECT = 0
REAL_HISTORY_READ = 0
TRADING = FALSE
ORDERS = FALSE
CAPITAL = FALSE
FORCE = FALSE
FAIL_CLOSED = TRUE
STOP_AFTER_R1_CR1_WER_02 = MANDATORY
```

**NEXT:** Separate human adjudication for real Windows evidence readiness; not automatically authorized.
