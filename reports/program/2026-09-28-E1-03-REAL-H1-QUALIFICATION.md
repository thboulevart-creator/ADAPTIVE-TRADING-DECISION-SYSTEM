# E1-03 — REAL AP0 → H1 QUALIFICATION

Date: 2026-09-28

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`

Qualified source HEAD:

`4a8292c2ad7dc671663bda7bb83b52cd616abad6`

Qualified source TREE:

`5f1455f88046b2ca50308ec834d3b163165e2246`

## 1. Purpose

This artifact records the governed real-data qualification of:

`E1-03 — EXACT GAP-AWARE H1 DATASET IDENTITY`

No Momentum signal, PnL, E1-05 runner or E1 backtest is produced or authorized by this qualification.

## 2. Protected implementation identity

```text
runtime blob =
38d481755e00ce3c2ed9c66c4db710500ca0911a

contract blob =
c2d4323039d65fcd9319d4f5eb02f45ee27c8afc

H1-01..H1-21 breaker blob =
958e338a1e9e7c5b56198eb3585f25ca140aa331

RC01 breaker blob =
38db4d3c01d60b885a694183df6da8317fd30dc0
```

These identities were revalidated before the real-data replay.

## 3. Real AP0 source revalidation

Governed AP0 identity:

`USTECH_PROFILE_MINUTE_CORE_V0_1`

Exact AP0 manifest SHA-256:

`62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`

Observed source validation:

```text
AP0_PARQUET_FILES = 61
AP0_PARQUET_FILES_HASH_MATCH = 61/61
AP0_PARQUET_BYTES = 91734766
AP0_MINUTE_ROWS = 1709180
```

The exact persisted runtime function `verify_ap0_binding()` returned:

```text
status = PASS
files_rehashed = 61
```

No file identity mismatch was observed.

## 4. Real H1 result

Output identity:

`USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1`

Observed result:

```text
accepted_h1_rows = 27677
first_admissible_h1 = 2021-05-25T01:00:00Z
last_admissible_h1 = 2026-05-24T22:00:00Z

pre_oos_h1_rows = 22199
oos_h1_rows = 5478

continuity_blocks = 1436
momentum_eligible_h1_rows = 1927
```

Canonical stream SHA-256:

`15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f`

## 5. Deterministic independent rebuild

Two builds were performed from the qualified real AP0 source.

Observed equality:

```text
ROWS_EXACT_EQUAL = TRUE
MANIFEST_EXACT_EQUAL = TRUE
CANONICAL_DIGEST_EXACT_EQUAL = TRUE
```

Both builds produced:

```text
accepted_h1_rows = 27677
canonical_stream_sha256 =
15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f
```

The second build reconstructed the H1 result independently rather than accepting the first build's rows or digest as authority.

## 6. Execution-method note

The E1-03 runtime itself does not implement Parquet decoding.

In the isolated qualification environment, the real AP0 Parquet inputs were first identity-checked byte-for-byte against the governed manifest, then the E1-required AP0 fields were decoded and supplied to the exact persisted E1-03 runtime.

A second independent reconstruction re-read the source and rebuilt H1 separately.

This qualification therefore establishes the E1-03 H1 dataset identity for the governed AP0 corpus. It does not qualify a generic Parquet ingestion subsystem.

## 7. Method limitation — conservative continuity/warmup policy

The observed:

`momentum_eligible_h1_rows = 1927`

is a direct consequence of the already human-adopted E1-03 policy that warmup resets after a continuity rupture.

The policy remains:

```text
new continuity block when:
- source_segment_id changes, OR
- current H1 is not exactly previous H1 + 1 hour

warmup resets to ordinal 0
first Momentum-eligible ordinal = 20
cross-block warmup = forbidden
```

Therefore 1,927 is not interpreted as a generic statement about all possible Momentum-V1 sampling policies. It is the exact result under the adopted conservative E1 policy.

## 8. Local artifact identities

Qualification-result artifact:

`E1-03-REAL-H1-QUALIFICATION-RESULT.json`

SHA-256:

`3a96ac264f23b7c1f14de69dbe0444af5b25265b7a61d5e233479a4b581e6425`

Real H1 JSONL artifact:

`E1-H1-MID-CLOSE.jsonl`

SHA-256:

`94ccb7c78e2e21cb3baa2dfe0945e7b39e20f74300c3c72addb89135d5af1ca0`

The human operator re-hashed both artifacts after placing them in the local ATDS-DERIVED storage and reported PASS for both identities.

These local files are not repository authority; their hashes are recorded for reproducibility.

## 9. E1-03 adjudication

```text
E1_03_REAL_AP0_FILE_REHASH = PASS
E1_03_REAL_H1_BUILD = PASS
E1_03_REAL_CANONICAL_DIGEST = PASS
E1_03_REAL_DETERMINISTIC_REBUILD = PASS

E1_03_TECHNICAL_QUALIFICATION = PASS
E1_03 = PASS
```

Authority remains limited to the E1-03 DatasetIdentity boundary.

This PASS does not authorize or qualify Momentum execution, PnL, E1-05, E1-06, E1-07 or E1-08.

## 10. E1-02 dependency impact

E1-02 was previously blocked pending the exact H1 dataset identity.

E1-03 now supplies:

- exact first admissible H1;
- exact last admissible H1;
- exact H1 row count;
- exact PRE-OOS/OOS H1 counts;
- deterministic canonical H1 identity;
- deterministic rebuild equality.

Therefore the specific E1-02 dependency on E1-03 H1 identity is closed.

Formal E1-02 re-adjudication must still preserve the already-frozen raw Source-B window and OOS split.
