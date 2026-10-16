# ATDS-EA-02-D0 — CONSOLIDATED OBSERVATION CONTRACT V0.2

**Authority:** HUMAN ADOPTED D0 with amendments A01–A08.
**V0.2 status:** D1 IMPLEMENTATION CANDIDATE FOR HUMAN REVIEW, not separately adopted.
**D1 scope:** pure standard-library Python, synthetic inputs only, fully offline.
**Canonical reference:** integration/system-v1 at HEAD 91fc53c406c67acde340599cb0ba35fd5347b02d, TREE c9274ca4f91c5b51d60aad2c607a8528c4f05027.

## 1. Purpose, rights, isolation

Way A retains the three original EX5 executables unchanged, confidential and unexamined by D1. Way B will eventually hold independently authored strategies. A shared observation interface is the bridge to a future laboratory; D1 neither decodes EX5 binaries nor connects to MetaTrader 5, performs a backtest, calculates true performance, or trades. Source records in D1 are strictly synthetic. Reproduced synthetic provenance does not prove authenticity of a real source, ownership of trades, or profitability.

## 2. Seven required logical collections

1. ea_registry: EA ID, binary SHA-256, optional configuration SHA-256, ownership class.
2. run_manifest: run, EA and source identity, synthetic mode, isolated-account attestation, account scope, position mode, instrument, account currency and equity coverage; optional run-specific configuration, FX/cost completeness and bounded replay conditions.
3. source_manifest: synthetic source ID, hash, record count, raw synthetic records and separate orders/deals/positions/account/market completeness.
4. trade_events: source-bound event identity, native order/deal/position IDs as appropriate, type ORDER/DEAL/CASH_FLOW, original time, optional UTC, time precision, row order and EA attribution.
5. position_snapshots: native position ID, signed side, size, floating outcome, observation time and optional attribution.
6. account_snapshots: account balance, equity, used/free margin, currency and time; never silently allocated to one EA.
7. market_context_refs: source-bound context time, decision time and claimed usability for the decision.

Required batch metadata: schema_version, batch_id, synthetic=true, authority all false and requested_claim (defaults to descriptive). Only synthetic sources and synthetic run modes are admissible in D1.

## 3. Mandatory amendments adopted in D0

### A01 — REQUIREDNESS
Require structural identifiers independently from optional economic components; unknown configuration, execution venue, commissions or currency-conversion costs never become invented values. Report structural, attribution, economic and scientific status separately.

### A02 — ATTRIBUTION
Magic Number, comment and EA filename are not proof of strategy ownership. Synthetic EXACT requires isolated run, explicit attested binding, matching EA identity and a source-bound synthetic reference; shared or uncertain account ownership is ambiguous or unassigned. Synthetic attestation is not authentication of actual MT5 executions.

### A03 — TIME AND CAUSALITY
Preserve raw timestamps, timezone knowledge, precision and normalized UTC separately. Unknown timezone prevents UTC minting. Arrival/source row order is not automatically causal; simultaneous times are marked ambiguous. Future-available market context cannot be consumed by earlier decisions.

### A04 — ACCOUNTING
Orders are not deals, deals are not full trades, cash-flow operations are not trading profit. Multi-fill, partial close, reversal in NETTING and distinct HEDGING positions are represented without double counting. Bounded synthetic deal reconciliation requires complete deals, a known initially-flat book, distinct clocks and a verifiable ordering. Unsupported cases fail closed.

### A05 — FLOATING AND PORTFOLIO RISK
Capture exposure, floating results, account equity and margin without artificial allocation. A broker account can aggregate several EAs. No exact drawdown, risk-of-ruin or EA-level risk claim is generated in D1; even a user-declared complete equity path is insufficient to establish real tick-complete coverage.

### A06 — COSTS AND NUMERICS
Prices, quantities and financial components are finite decimal strings, never binary floats. Preserve actual currencies and missing cost/FX fields. Synthetic realized gross totals include only DEAL profit and exclude DEPOSIT, WITHDRAWAL, ADJUSTMENT. There is no D1 net profit calculator and all profitability requests are blocked.

### A07 — PROVENANCE AND CONFIDENTIALITY
Verify record references, source synthetic hash, declared raw record count and separate completeness. Exact event reimports are idempotent while original source records remain unchanged. Contradictory event or deal IDs are rejected. No third-party EX5 or protected performance is used. A future importer must hash original real bytes, not use the canonical-fixture hash as a substitute. Field-by-field source provenance remains a limitation requiring hardening before real use.

### A08 — SYNTHETIC GATE
No import or call to MetaTrader5, no MT5 connection, EX5 execution, network operation during D1, broker access, backtest or strategy optimization. No trading, capital, real-observation or scientific authority. Synthetic tests T01–T26 and adversarial B01–B18 must be run and reported honestly; a green result does not qualify actual trading.

## 4. Return states

STRUCTURALLY_VALID: checked synthetic structure and scoped invariants pass.
PARTIAL_DESCRIPTIVE_ONLY: structural validity with attribution/coverage limits.
BLOCKED: requested claim or use exceeds allowed D1 authority or evidence.
FAIL: contradiction or invalid structure.
NOT_RUN: a test not executed.
Scientific status remains NOT_ASSESSED. Trading, capital and real observation authority remain false. Claims EA_NET_PNL, PORTFOLIO_NET_PNL, EXACT_DRAWDOWN, EXACT_EA_RISK and TRADING_AUTHORIZATION are always blocked even on an internally consistent synthetic fixture. Synthetic structural economic readiness is not an admissibility or performance verdict.

## 5. Tests designed and executed

T01 valid synthetic fixture; T02 tampering; T03 duplicate idempotence; T04 event ID conflict; T05 partial fills; T06 partial close; T07 NETTING reversal; T08 separate HEDGING positions; T09 shared NETTING ambiguity; T10 Magic Number collision; T11 unknown commission; T12 unavailable equity drawdown; T13 noncausal arrival order; T14 tied timestamps; T15 missing parameters; T16 broker-symbol equivalence refusal; T17 lookahead context; T18 trading authority forbidden; T19 floating DCA risk; T20 real-source disguise; T21 deposits excluded from trading PnL; T22 shared account identity; T23 final-only equity; T24 distinct parameter configurations; T25 unknown cost conversion; T26 real-run disguise.

B01–B18: float precision, forged binding/source reference, native deal ID collision, fabricated UTC, duplicate NETTING positions, overclosure, invalid HEDGING reversal, unknown claim, forged authority, synthetic raw hash alteration, wrong position snapshot, missing realized results, incomplete source, profitability/equity/risk overclaim and authority invariants.

## 6. Existing ATDS modules retained unchanged

- src/research/input_binding.py — reference identity model.
- src/data/dataset_admissibility.py — reference source screening.
- src/data/claim_scoped_admission.py — bounded claim design.
- src/p1_12c_qualified_producer_execution.py — execution-proof architecture reference.
- tools/ao_e0_exec_01_all_in_cost.py — costs reference, restricted to original scope.
- src/decision_action_authorization.py — non-authorizing decision boundary.

No implicit transfer of DATA-02, P1, MOMENTUM V1, CORE-02, WER-05, B11 or B12 authority or proofs.

## 7. Unresolved technical limitations

- D1 cannot prove native MT5 exporter compatibility or full broker event semantics.
- Limited synthetic reversal and partial-close checking does not cover all broker accounting cases.
- Field-level attribution is not yet independently attested for every observed field.
- There is no authenticated real raw-byte importer, broker telemetry, or EX5 provenance attestation.
- No exact portfolio equity reconciliation, margin stress model, independent performance data or production integration.
- A later phase must independently qualify real observability, broker semantics and the relationship between any EX5 version, parameter set and observed trading run.

**STOP at CANDIDATE_FOR_HUMAN_REVIEW. No commit, push, merge, live data, MT5 or EA-03 opening.**
