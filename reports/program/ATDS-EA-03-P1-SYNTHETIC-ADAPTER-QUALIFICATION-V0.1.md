# ATDS-EA-03-P1 — SYNTHETIC ADAPTER QUALIFICATION V0.1

**Date:** 2026-10-17  
**Status:** QUALIFIED_SYNTHETIC_ADAPTER_CANDIDATE — REQUIRES HUMAN ADJUDICATION  
**Decision executed:** ADOPT_P0_READINESS_AND_AUTHORIZE_SYNTHETIC_ADAPTER_ONLY  
**Authority:** READ/WRITE ONLY in the five predeclared P1 paths of detached isolated worktree, synthetic/offline tests, no Git publication.

## 1. Lineage and boundaries

Repository: thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM  
Governed branch: `integration/system-v1`  
Parent HEAD: `0f2a0c1aab284d98f645346567dd704517db6970`  
Parent TREE: `b57415117f223d4d05a2e2dc04e2251b114d9010`  
Candidate worktree: `C:\Users\Boulevart\Documents\ATDS-EA-03-P1-ISOLATED` (detached HEAD)

P0 is adopted for its documented feasibility findings only, not for proven MT5 compatibility or real-observation readiness.

D0, D1 and CR1 remain the adopted synthetic source; no tracked historical file, research module, source-binding code, historical fixture or historical test is edited.

## 2. The five reserved new files

1. `docs/ATDS-EA-03-P1-SYNTHETIC-ADAPTER-CONTRACT-V0.1.md` (contract)
2. `src/ea_observation/synthetic_adapter.py` (pure offline source-preserving transformer)
3. `tests/fixtures/ea03_p1_synthetic_feed_v0_1.json` (fully invented MT5-labeled feed)
4. `tests/test_ea03_p1_synthetic_adapter.py` (34 Python unit tests)
5. `reports/program/ATDS-EA-03-P1-SYNTHETIC-ADAPTER-QUALIFICATION-V0.1.md` (this report)

All five paths were checked absent from the detached worktree before any P1 write. The fixture was reconstructed from the accepted D1 synthetic fixture, not from real MT5 data. Its labels are simulations and are not native terminal records.

## 3. RED executable proof

Before creating the production adapter module:

`py -B -m unittest discover -s tests -p test_ea03_p1_synthetic_adapter.py -q`

Result: **ERROR** from `ModuleNotFoundError: No module named 'src.ea_observation.synthetic_adapter'`, `Ran 1 test`, exit failure. This is the expected fail-first evidence that the proposed adapter did not yet exist.

The RED import failure is not equivalent to 34 independent failing functional tests. Each individual case was exercised after implementation.

## 4. Implementation summary and source discipline

`adapt_synthetic_feed(feed)` returns a structured response with status, optional candidate batch, result of the preserved D1 validator, errors and permanently false authorities.

Strict, explicit input marker: `EA03_P1_SYNTHETIC_FEED_V0_1`, `synthetic = true`, synthetic-only sources/EAs/runs, no broker or real-data connections.

Feeds consist of MT5-labeled simulated ORDER, DEAL, CASH_FLOW, POSITION_SNAPSHOT, ACCOUNT_SNAPSHOT and CONTEXT records, plus an optional synthetic EA_BINDING or INSTRUMENT_SPEC record. Input contains separate `values` (bound to raw synthetic evidence) and `annotation` (whitelisted event identity metadata). Conflicting fields, omitted required source values, unsupported types and repeated raw references fail closed.

The adapter preserves exact decimal strings and raw timestamps rather than rounding, converting to binary floats, or manufacturing a timezone. It does not create order/deal identifiers, fake missing costs or claim a real EA attribution. `source_manifest.sha256` binds only the internal synthetic evidence, not original MetaTrader bytes.

Output always passes to the existing `validate_batch` from D1. The adapter yields a candidate batch only when D1 declares it `STRUCTURALLY_VALID` or `PARTIAL_DESCRIPTIVE_ONLY`. Any D1 structural fail produces `FAIL` and `batch=null`; an inadmissible requested economic/trading claim produces `BLOCKED` and `batch=null`. Authority for trading, capital and real data is always false.

## 5. GREEN + historical non-regression

**P1 unittest suite:** 34/34 PASS, 0 FAIL, 0 ERROR.

Coverage includes: deterministic byte-consistent representation of the D1 accepted synthetic fixture; seven D1 collections; exact value preservation; simulated cash-flow isolation; schema/authority/synthetic-only preconditions; duplicate raw refs; unsupported source tags; source-value/annotation separation; missing/invalid numeric fields; absent commissions; restricted claims; missing UTC; unsupported attribution; non-direct value processing; repeatability; synthetic ownership; split fills, partial closes, Netting, Hedging, conflicting aggregate positions, floating losses and tied timestamps.

**Historic D1 suite:** 65/65 PASS, 0 FAIL, 0 ERROR.
All adopted D1 tests were executed on their existing, unmodified files.

Commands:
- `py -B -m unittest discover -s tests -p test_ea03_p1_synthetic_adapter.py -q`
- `py -B -m unittest discover -s tests -p test_ea_observation_*.py -q`

No MetaTrader import, application start or network activity was required.

## 6. Independent adversarial re-break (separate runtime probe)

A separate in-memory test harness applied **16 additional mutations** outside the production implementation and outside the 34 GREEN test definitions. It did not persist any files.

Final result: **16/16 PASS**.

- RB01 non-finite floating NaN: controlled FAIL.
- RB02 binary float price: controlled FAIL.
- RB03 reused raw record reference: controlled FAIL.
- RB04 artificial profit inside an ORDER annotation: controlled FAIL.
- RB05 unknown raw numeric field: controlled FAIL.
- RB06 unknown timezone despite UTC supplied: controlled FAIL.
- RB07 invented DEAL side: controlled FAIL.
- RB08 non-finite account equity: controlled FAIL.
- RB09 capital authority forged as numeric true: controlled FAIL.
- RB10 missing native deal ID: controlled FAIL.
- RB11 string asserting EA isolation: controlled FAIL.
- RB12 duplicate source ID: controlled FAIL.
- RB13 legitimate synthetic commission variation: remains PASS with exact value preserved.
- RB14 unexpected broker-login field: controlled FAIL.
- RB15 invalid account positioning mode: controlled FAIL.
- RB16 future market context used in an earlier decision: controlled FAIL.

These tests were authored and executed by the same implementation assistant: they are independent vectors, **not an external auditor's validation**.

## 7. SHA-256 of four content-stable source artifacts

`docs/ATDS-EA-03-P1-SYNTHETIC-ADAPTER-CONTRACT-V0.1.md`  
`20A363C953B3362A7474A684B6A85E08A4427F5A82E719A5E643E5FB92925129`

`src/ea_observation/synthetic_adapter.py`  
`D41044BF8B78A8F062A10E799DE963F6E3C572F646AB0784EE65197C54F4C3C1`

`tests/fixtures/ea03_p1_synthetic_feed_v0_1.json`  
`58DB71EAB66DE30CFE1AAFF099C2DF6816F0D6769787979AC4BF685DBDC14B61`

`tests/test_ea03_p1_synthetic_adapter.py`  
`695BEBB606AF03E9B75A8188B8F8EF5A610A7E423775EFE5A9E1FB6A4E97120B`

The report SHA-256 itself is calculated during final verification, not embedded self-referentially.

## 8. Residual limits and next gate

1. The simulated MT5-like records are not fetched from, generated by, or verified against a MetaTrader 5 terminal or native Python API.
2. Source hashes use reproducible synthetic JSON; they neither bind authentic MT5 exporter bytes nor verify immutable broker/account-side events.
3. Input may be made internally consistent by an actor controlling the entire synthetic feed; P1 does not certify actual source authenticity.
4. EA exact synthetic attribution is a controlled fixture assertion, not proof that a real trade was initiated by a particular compiled executable.
5. Native event cardinality, position ownership, account-wide equity allocation, timezone normalization, and money/FX/margin semantics are not fully qualified for real brokerage accounts.
6. No real account history or performance was examined. No backtest, EX5 execution, MT5 connection or capital operation.
7. Future real observation requires an entirely separate, independently reviewed importer design, real-byte provenance, isolation/mode/time/identity controls, privacy and explicit human permission.

**Recommendation:** `QUALIFIED_SYNTHETIC_ADAPTER_CANDIDATE` for human technical review only, subject to the complete set of final filesystem and test checks. Do not silently upgrade to HUMAN_ADOPTED or PERSISTED.

**STOP: NO HUMAN ADOPTION, NO GITHUB COMMIT/PUSH/MERGE, NO REAL MT5 OBSERVATION.**
