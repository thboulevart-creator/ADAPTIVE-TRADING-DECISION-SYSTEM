# B-FIQ-02 — PRE-EXECUTION PACKAGE — ADVERSARIAL BREAK

Structural verification errors: 0

Demonstrated contract/package defects: 5

## Structural checks

[]

## Demonstrated defects

[
  {
    "id": "BFIQ02-F01-DIAGNOSTIC_MANIFEST_SCHEMA_UNDERSPECIFIED",
    "path": "diagnostic_A",
    "missing": [
      "decompressor_binary_or_source_sha256",
      "decompressor_version",
      "invariant_evaluator_source_blob_sha256",
      "parser_source_blob_sha256",
      "projection_source_blob_sha256"
    ]
  },
  {
    "id": "BFIQ02-F01-DIAGNOSTIC_MANIFEST_SCHEMA_UNDERSPECIFIED",
    "path": "diagnostic_B",
    "missing": [
      "decompressor_binary_or_source_sha256",
      "decompressor_version",
      "invariant_evaluator_source_blob_sha256",
      "parser_source_blob_sha256",
      "projection_source_blob_sha256"
    ]
  },
  {
    "id": "BFIQ02-F02-SHARED_GENERIC_DECOMPRESSOR_OVERCLAIMED_AS_INDEPENDENT",
    "detail": "Both qualified I_A/I_B sources use Python stdlib lzma. Generic primitive sharing can be allowed, but the decompression stage must be explicitly classified as shared-generic-exempted rather than independently implemented PASS."
  },
  {
    "id": "BFIQ02-F03-DURABLE_STORAGE_CLASS_OVERCLAIMS_IMMUTABILITY",
    "detail": "GitHub release assets can be deleted. Asset-id plus exact SHA-256 can make mutation detectable, but the storage class itself is not intrinsically immutable."
  },
  {
    "id": "BFIQ02-F04-AUTHORITY_SCOPE_DIGEST_DOMAIN_IMPLICIT",
    "detail": "The provisional scope contains both authority_scope_tuple_digest and scope_seal but does not state the exact excluded fields for the digest domain."
  }
]

## Break verdict

B-FIQ-02 MATERIALIZED CANDIDATE = FAIL

The upstream C01-C07 semantic-authority blocker is preserved and is not counted as a package-construction defect.

No provider GET, FULL_INTERVAL execution, D materialization or backtest occurred.
