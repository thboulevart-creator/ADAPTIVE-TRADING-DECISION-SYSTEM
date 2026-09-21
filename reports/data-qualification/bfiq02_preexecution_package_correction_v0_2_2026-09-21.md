# B-FIQ-02 — PRE-EXECUTION PACKAGE — CORRECTION RECORD V0.2

Date: 2026-09-21

Parent materialized package HEAD:
2600e08894e9f19d2c20c38231aa21498b84ae8c

Adversarial break HEAD:
7f5a91261e273473410ce32ac8e6b4a43906cc80

Adversarial report blob:
abb9035bf6f6fff90cc2cb39c67249be47351cd8

Corrected only:

BFIQ02-F01
- diagnostic manifest now includes exact decompressor version/hash fields;
- parser/projection/invariant source hashes use raw SHA-256 as required.

BFIQ02-F02
- decompression is no longer overclaimed as independently implemented;
- both paths' shared CPython lzma primitive is exact-pinned and explicitly excluded from the independent-stage claim;
- independence remains based on distinct project-owned framing/parsing/projection/invariant lineages qualified by the Q-RM-12 I_A/I_B evidence.

BFIQ02-F03
- GitHub Release asset storage is no longer called intrinsically immutable;
- policy now defines a SHA256 content identity plus release/asset retrieval locator;
- deletion/replacement/mismatch is detectable and opens CAPTURE_INTEGRITY_FAILURE.

BFIQ02-F04
- provisional authority scope now explicitly states the digest domain;
- authority_scope_tuple_digest excludes only itself and scope_seal under strict canonical JSON.

The upstream semantic blocker is intentionally unchanged:

C01-C07 current authority = BLOCKED.

No provider GET, FULL_INTERVAL execution, D materialization or backtest occurred.
