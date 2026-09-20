# B-PE-02 — NATIVE BI5 PROVIDER / REFERENCE EVIDENCE — FINAL PERSISTED-HEAD RE-BREAK

**Date:** 2026-09-20  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Corrected adjudication HEAD:** `0a7d684e3470d1b5df980733a36785e239f8bf52`  
**Evidence bundle blob:** `df22332709377591d73571a4940c1fda39565867`  
**Corrected report blob:** `d9076187ad4db01d2b781fa04ad750b5267af6e8`

## 1. Evidence collected

Provider-primary observations:

- Dukascopy Historical Price Data live page:
  current daily BI5 = LZMA-compressed, fixed 20-byte big-endian records;
  current timestamp basis = milliseconds since start of day;
  explicit warning that legacy hourly files may use milliseconds since start of hour;
  no legacy-hourly transition date/version binding;
  index/commodity scaling must be confirmed per instrument.
- Dukascopy USATECH CFD live page:
  identifies USATECH.IDX/USD and current quoted CFD point value 0.01 USD;
  does not define the raw BI5 integer divisor.

Independent exact-revision references:

```text
saleem-latif/duka-data
commit 2220708e7d0be9d2b6feaf6efe4d3f89c6bb040c
download.py SHA256
42e7ada6a7c841ab2a92387954e30e0dfeb21ddc50b8b31ddef8b9851506a24b

ninety47/dukascopy
commit 8654ad197bdf55579544cf71735369f0d227569f
src/dukascopy.cpp SHA256
0eb44b369b77c47306f7bf5d440d96aa177b7f9535772e95f83f2963a56f2dbd
README.md SHA256
9fa5aaf0c78106f8a8ef8dd8aaf944870a48c8b74444ac826a16789475e317b2

leoclc/dukascopy-tick
commit 989987db0808e215962e136ce043797992d1a1a2
decompressor/types.ts SHA256
a7979e5154a52e8e886771a4526769ab5b29e54248cdd52b9a43d67f7fb355fa
decompressor/index.ts SHA256
2e88f793e9f615a43c44ad344416f917540c007f5460ddf92c4e2fafe057208a
data-normaliser/index.ts SHA256
3270e2a2c14d8fe67baefc83776422b423a4485430640e42ae3f80fdf1619b3e
url-generator/index.ts SHA256
2f6c88b204e19217fb18746b8aa069e78cbc5d1d2c3fa44fa5da499bedbe861e
USATECH metadata SHA256
8b380d2a33e6ecfa44e5cb94752e6f01b1ed2e2b8f2257f0d8a7e1491dbf8e50
```

Project V4.3 was persisted as EC-PROJECT and REJECTED from independent evidentiary weight.

## 2. Demonstrated adjudication defects and corrections

Initial adversarial defects:

```text
BPE02-F01 — NONRECURSIVE_CANONICAL_SEAL_GENERATION
BPE02-F02 — LIVE_PROVIDER_PAGE_SNAPSHOT_NOT_DURABLY_MATERIALIZED
BPE02-F03 — CLAIM_ASSERTION_SCHEMA_NOT_CLOSED
BPE02-F04 — MULTI_FILE_SOURCE_DIGEST_PROJECTION_NOT_SELF_DESCRIBING
```

Corrections:

- every structured seal/digest now uses recursive sorted-key canonical JSON;
- provider live pages E01/E02 are source-level BLOCKED, not ADMISSIBLE;
- every claim assertion targets one exact claim/dimension/stance with closed schema;
- every GitHub evidence file is one EvidenceSourceRecord with exact commit/path/SHA-256;
- project evidence remains REJECTED;
- no pairwise third-party semantic independence is assumed without proof.

## 3. Final persisted-HEAD integrity re-break

Recomputed from persisted bytes:

```text
admissibility decision seal mismatches = 0
lineage digest mismatch                = 0
evidence_set_digest mismatch           = 0
assertion_set_digest mismatch          = 0
adjudication_seal mismatch             = 0
```

Persisted adjudication seal:

`d27771bc8c2023571b4fbbe66238dbc28b29ca69949a1db114480346f1c90a76`

Persisted evidence-set digest:

`d2c9cd9a62c7f000f6821a3b04898400dbb28a363c161c0c398228aa79b6ba98`

Persisted assertion-set digest:

`5d8cfd7e9d5afde69c0ddc59ff6c481e16f3f562a0abe3e02e726d3daf909a4f`

## 4. Final adversarial semantic re-break

Attacks survived fail-closed:

```text
current daily provider docs → legacy hourly target             BLOCKED
raw LZMA → LZMA-Alone equivalence                              BLOCKED
current CFD 0.01 point → raw BI5 /1000                         BLOCKED
signed/unsigned disagreement resolved by majority vote         FORBIDDEN
multiple third-party repos counted as independent lineages     FORBIDDEN
third-party current behavior → provider temporal continuity    FORBIDDEN
generic 20-byte/layout evidence bypasses C08 target scope       FORBIDDEN
project V4.3 used as provider corroboration                     REJECTED
```

No new adjudication defect was demonstrated.

## 5. Claim-level final state

```text
BPE-C01 compression / envelope = BLOCKED
BPE-C02 physical framing       = BLOCKED
BPE-C03 primitive layout       = BLOCKED
BPE-C04 timestamp semantics    = BLOCKED
BPE-C05 ask/bid raw roles      = BLOCKED
BPE-C06 USATECH price scaling  = BLOCKED
BPE-C07 volume semantics       = BLOCKED
BPE-C08 target applicability   = BLOCKED
```

No claim is FAIL.

The evidence is technically strong enough to support hypotheses, but B-PE-01 does not permit hypothesis strength to replace an admissible provider-primary exact-target source.

## 6. Dominant blocker

The smallest demonstrated evidence gap is:

```text
provider-primary immutable/versioned proof that the legacy hourly BI5
representation and its physical semantics apply to the target
USATECHIDXUSD hourly acquisition epoch (2021–2026),
including the provider transition/continuity boundary.
```

Until that scope bridge exists, provider-current daily documentation cannot be promoted into target legacy-hourly authority.

C06 also retains a separate raw-USATECH scaling gap; it is downstream of the scope/version bridge for the current next-action ordering.

## 7. Final verdict

```text
B-PE-02 PROVIDER / REFERENCE EVIDENCE ADJUDICATION = BLOCKED
overall_provider_evidence_status = BLOCKED
B global executable gate = BLOCKED
FINAL EXECUTABLE DATA GATE = BLOCKED
```

This BLOCKED verdict is the successful governed outcome of the evidence adjudication. It is not a failure of B-PE-01.

No project BI5 was downloaded or processed. No acquisition, backtest or trading execution occurred.
