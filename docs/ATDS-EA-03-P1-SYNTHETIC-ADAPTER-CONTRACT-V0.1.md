# ATDS-EA-03-P1 — SYNTHETIC OBSERVATION ADAPTER CONTRACT V0.1

**Date:** 2026-10-17  
**Scope:** EA-03-P1 only  
**Human decision:** ADOPT_P0_READINESS_AND_AUTHORIZE_SYNTHETIC_ADAPTER_ONLY  
**Authority:** NO_REAL_DATA, NO_MT5, NO_EX5, NO_TRADING, NO_CAPITAL  
**State:** Candidate; requires human adjudication. No commit, push or merge authorized.

## 1. Boundaries and canonical lineage

This module converts only explicitly synthetic, MT5-* labeled JSON-style event records into the already-adopted seven D1 collections. The tags are educational simulation labels, **not a real MT5 data-export or Python API compatibility certificate**. It must never import, start or connect to the terminal, process broker records, decode third-party EA files, trigger a backtest or infer performance.

Parent governed commit: `0f2a0c1aab284d98f645346567dd704517db6970`. Parent TREE: `b57415117f223d4d05a2e2dc04e2251b114d9010`.

The implementation imports only Python standard-library modules and the frozen local modules `src.ea_observation.provenance` and `src.ea_observation.validation`. The D1 validator remains the only authority for synthetic structural admissibility.

## 2. Input feed

Required exact top-level keys:

`input_schema`, `batch_id`, `synthetic`, `authority`, `requested_claim`, `ea_registry`, `run_manifest`, `feeds`.

- `input_schema` = `EA03_P1_SYNTHETIC_FEED_V0_1`.
- `synthetic` = Boolean `true`.
- `authority` = exactly `{"trading": false, "capital": false, "real_data": false}`.
- `requested_claim` must be a string; no economic, real or trading claim can pass D1.
- Every `ea_registry` record must use `ownership = SYNTHETIC`. No private EX5 binary is read.
- Every run must declare `mode = SYNTHETIC`.
- `feeds` is a non-empty array of source objects. Each source has exactly `source_id`, `kind`, `synthetic`, `completeness`, `records`.
- Each source declares `kind = SYNTHETIC` and `synthetic = true`.
- Each source record has exactly `ref`, `kind`, `values`, `annotation`. Refs are unique, non-empty strings within the same source.
- `values` are immutable-by-contract simulated source values; `annotation` includes only permitted identity metadata, and cannot overwrite a value field.

Supported synthetic record kinds: `MT5_EA_BINDING`, `MT5_INSTRUMENT_SPEC`, `MT5_ORDER`, `MT5_DEAL`, `MT5_CASH_FLOW`, `MT5_POSITION_SNAPSHOT`, `MT5_ACCOUNT_SNAPSHOT`, `MT5_CONTEXT`.

These names deliberately approximate observation categories; exact native terminal structures, API enums and capabilities have **not** been proven. No import or exporter is implemented.

## 3. Transformation and provenance

- Map each raw synthetic record to an explicit type, source reference and D1 collection without creating fictitious event identifiers, timestamps, prices, volumes, profit, commission, swap or currency conversion.
- Copy input source values verbatim. Decimal strings retain precision and missing costs remain `null`, never inferred zero.
- Non-observational binding/specification records remain source evidence only, with no synthetic deal emitted.
- Derive `source_manifest.sha256` deterministically from canonical JSON for simulated raw records; this hash is **not** an attestation of real MT5 bytes or a proof against a party able to rewrite source and checksum simultaneously.
- Bind each normalized observation to one unique source record; exact future one-to-many derivations remain outside this version.
- Preserve timestamps as supplied; D1 fails on fabricated UTC or look-ahead.
- Preserve order/deal/position/account distinctions; D1 checks their limited synthetic semantics and their causal and attribution limits.
- Fail closed whenever unrecognized source/annotation fields appear, rather than silently discarding them.
- Pass the generated candidate to the unchanged `validate_batch` D1 function.
- Return `PASS` with a candidate batch only for D1 `STRUCTURALLY_VALID` or `PARTIAL_DESCRIPTIVE_ONLY`. Return `BLOCKED` for an inadmissible claim; `FAIL` for malformed input or contradictions. In both latter cases, return `batch = null`.
- For every returned status, all three authorities remain false.

The `PASS` result is a purely synthetic structural/descriptive status and **must not** be interpreted as real observation readiness, real attribution, performance qualification or trading permission.

## 4. Test plan

1. Pre-production RED: the new unittest module cannot import the nonexistent synthetic adapter (expected failure).
2. GREEN: deterministic source-preserving roundtrip to the existing D1 synthetic fixture.
3. Non-regression: execute all 65 historical D1 tests unchanged.
4. P1 cases: strict input gate, duplicate source refs, binding, false authority, economic overclaim, missing costs, negative/invalid volumes, future context, unsupported tags, unknown UTC, nonexact attribution, copied source values, split fills, partial close, Netting/Hedging, floating losses and tied timestamps.
5. Independent adversarial mutations distinct from most GREEN tests, including non-finite numbers, mislabeled event metadata, forged synthetic isolation, duplicated sources, mixed-value claims and synthetic market look-ahead.
6. Confirm no tracked-file modifications, and ensure P1 files are the only new paths.

## 5. Known boundaries / future real-observation prerequisites

- Never accept input labeled REAL even if it shares synthetic field names.
- Before any real adapter: independently approve a source-byte integrity model, terminal/API and broker semantics, immutable exporter provenance, EA version/parameters/config identity, clock/timezone treatment, one-to-many native event cardinality, money/currency/margin reconciliation, account isolation/Netting/Hedging attribution, exact raw-byte attestation, privacy and audit logs, error isolation, authority gates, and dry-run controls.
- P1 offers no qualified mapping to a particular MetaTrader build, broker, account or third-party EX5.
- Never infer actual net profit, EA strategy quality, drawdown or safety of live trading from P1.
- Any real terminal connection, performance read, backtest, EA execution, GitHub commit/push or advancement to real EA-03 must receive a **separate human authorization**.

**STOP = CANDIDATE_FOR_HUMAN_REVIEW.**
