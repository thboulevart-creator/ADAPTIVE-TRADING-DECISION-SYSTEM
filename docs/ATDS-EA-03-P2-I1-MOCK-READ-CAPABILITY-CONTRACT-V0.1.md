# ATDS-EA-03-P2-I1 — MOCK-ONLY READ CAPABILITY FIREWALL V0.1

Date: 2026-10-17
Status: IMPLEMENTATION_CANDIDATE_FOR_HUMAN_REVIEW
Governance: User-authorized offline implementation I1, expressly limited to a reusable engine component for the existing TERMINAL JOURNAL MT5.
Canonical parent HEAD: 4c8f6b573f70396667c0b2d511b7924482075bb7
Canonical parent TREE: a43a4fddd64d3944a4ba02d0a2bb57cbe349dec7

## 1. Separation of projects

ATDS provides observation contracts, source/evidence controls, decision guards and future integration interfaces. TERMINAL JOURNAL MT5, developed in its separate chat and still incomplete, remains the SINGLE future UI for journal, screenshots, statistics, strategies and visualizations. The Terminal has not completed UI approval or MT5 account connections. This P2-I1 task is NOT Terminal development, and does NOT reproduce any GUI, journal, statistical engine, MT5 connector or strategy.

No existing Terminal file or repository is touched. Existing D0, D1, CR1 and P1 files remain unchanged. No EX5 is opened, loaded or run.

## 2. Mock-only interface

Python standard library only, module: src/ea_observation/mock_read_firewall.py.
Entry point: MockReadFirewall(dataset).execute(request).
Protocol: ATDS_EA03_P2_I1_READ_V0_1
Fixture schema: ATDS_EA03_P2_I1_MOCK_FIXTURE_V0_1
Data source marking: SYNTHETIC_MOCK
Response authority flags: trading=false, capital=false, real_data=false, network=false.

Exact request fields: protocol_version, request_id, capability, filters.
Exact response fields: protocol_version, request_id, status, source, records, errors, authority.

Seven allowed capabilities:
- read_ea_registry: ea_registry, no filters
- read_run_manifest: run_manifest, scoped to one mock run_id
- read_orders: orders, scoped to one mock run_id
- read_deals: deals, scoped to one mock run_id
- read_positions: positions, scoped to one mock run_id
- read_account_snapshots: account_snapshots, scoped to one mock run_id
- read_market_context: market_context, scoped to one mock run_id

The interface exchanges plain JSON-compatible dictionaries for future contract review. COMPATIBILITY WITH THE EXISTING TERMINAL IS NOT VERIFIED OR ADOPTED.

## 3. Mock read guard

No callbacks, injectable backend, broker handle, terminal path, network IO or trade methods are provided.
Allowed capabilities are selected by an exact static allowlist, never by runtime dynamic method reflection.
All unknown capabilities, command attempts, extra request keys, malformed scopes and schema deviations are denied without records.
Only explicit synthetic rows, synthetic EA ownership, synthetic run modes and false authorities are accepted.
The input dataset is copied after structural checks, returned records are copied, and financial values preserve exact decimal strings and null missing costs.
Return status OK means only that a mock read succeeded, not that D1 admitted a real market record, not a trading authorization and not an economic verdict.

## 4. Explicit limits and threat model

NOT A PRODUCTION SECURITY SANDBOX: arbitrary Python code sharing the same process could inspect private attributes or invoke unrelated libraries; production enforcement requires process isolation and independent broker/account read-only rights, operating-system permissions, disabled trade network paths and review of the entire stack.
NOT A REAL-SOURCE ATTESTATION: anyone controlling a mock fixture could fabricate a self-consistent synthetic feed.
NOT A TERMINAL INTEGRATION: no interface has been compared with the Terminal code; no GUI, journal, storage or statistics is created here. GitHub versions code and technical contracts; private account history and personal journal data require separately approved storage.
NOT A D1/P1 INGESTION PATH: seven mock read collections and P1/D1 observation contracts remain unconnected; a future versioned bridge must be qualified independently.

## 5. Scope and stopping point

Predeclared five NEW files only:
1. docs/ATDS-EA-03-P2-I1-MOCK-READ-CAPABILITY-CONTRACT-V0.1.md
2. src/ea_observation/mock_read_firewall.py
3. tests/fixtures/ea03_p2_i1_mock_feed_v0_1.json
4. tests/test_ea03_p2_i1_mock_read_firewall.py
5. reports/program/ATDS-EA-03-P2-I1-MOCK-READ-CAPABILITY-QUALIFICATION-V0.1.md

Proof: RED import failure; GREEN I1 tests; D1 65 and P1 34 unchanged non-regression checks; new separate adversarial mutations; SHA-256 and tracked/untracked scope audit.

No Git commit, push, merge, rebase, reset, real MT5 observation, EX5 loading, broker connection, backtest or capital activity.

IF QUALIFIED: EA-03-P2-I1 = QUALIFIED_MOCK_ONLY_CANDIDATE.
STOP BEFORE HUMAN ADOPTION, GITHUB PUBLICATION, TERMINAL INTEGRATION OR REAL MT5 OBSERVATION.
