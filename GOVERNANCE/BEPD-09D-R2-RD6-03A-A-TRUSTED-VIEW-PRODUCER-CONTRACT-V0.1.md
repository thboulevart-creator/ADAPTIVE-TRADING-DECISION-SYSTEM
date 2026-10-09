# BEPD-09D-R2-RD6-03A-A — TRUSTED TRAINING VIEW PRODUCER CONTRACT V0.1
**DESIGN CANDIDATE ONLY. HUMAN ADOPTION PENDING. NO CODE, TEST, REAL READ, FIT OR MATERIALIZATION.**
Date 2026-10-09; authorized baseline HEAD `5ed4d74ec1aab2fd7e215eabeb995faadfc72625`, TREE `032e78bc8188a3ec172e19a7dfd98dd67ff48c81`; branch `integration/system-v1`.
RD6-02 closure git blob `9719665d20a0e85e00e1fdd64648e978b4a40058`; source RD5 adapter `bfbf586914c852047123c3a4cd1b2fa6a7dc4daa`. No promotion of synthetic competence to real capability.

## Boundary contract and state machine
```text
FROZEN_AUTHORITY_GRANT (documentary only; no active real grant)
    -> CANONICAL_DATA_OWNER
    -> ISOLATED_VIEW_PRODUCER
    -> VIEW_AUTHENTICATOR / ADMISSION_GATE
    -> TRAIN_ONLY_CONSUMER (new gateway, NOT legacy run_protocol)
    -> REDACTED_AUDIT_EXPORTER
```
Interface candidates, **not callable production capabilities**:
* `produce_synthetic_view(fold_id, authorized_synthetic_rows, owner_grant, producer_identity, signing_key)` returns immutable `view_bytes, signed_manifest`; explicit `synthetic_mode=true`; future test-only keys; never reads source paths. No import of legacy whole-ledger harness.
* `authenticate_view(signed_manifest_bytes, frozen_trust_store, expected_fold_id, expected_receiver_id, explicit_scope, nonce_state, time_source)` returns `ADMISSION_DENIED(reason)` or a single-use sealed handle; signature/contract/fold/permissions checked **before** view content exposure; never fallback to marker string.
* `admit_train_only_view(handle, train_view_bytes)` verifies exactly-once digest/byte size/schema, ordered week ids and event/cluster invariants before consumer handoff; zero row data in logs or error strings.
* `record_redacted_gate(outcome, hashes, controlled_status)` accepts exact recursive types, bounded scalar fields only, canonical and atomic persistence; must not include rows, coefficients, paths, diagnostics or predictions.

State transitions: `NEW -> MANIFEST_VERIFIED -> HANDLE_RESERVED -> VIEW_VERIFIED -> ADMITTED_ONCE -> CONSUMED`; any missing/unknown evidence `-> DENIED_AND_STOP`. Deny must occur before downstream import, fit or exposure. Timeout, nondeterministic clock, duplicate/replayed nonce, stale signer, unverifiable attestation or entropy failure STOP. Reservation, audit receipt and nonce state must be atomic; on failure burn nonce by default unless an explicitly adopted transactional rollback policy proves no read. No reuse across sessions/folds/consumers.

## Physical-read boundary: explicit impossibility and bounded options
Historical source identity, **preexisting metadata only**: monolithic ledger git blob `0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2`, declared SHA-256 `301a621b97fea14a72540d4c2c6da78eb742cc44c5009e44ad98e9f678ca4731`, declared 472 rows / 754544 bytes. Neither bytes nor rows re-read or verified.
The real legacy harness invokes full `read_bytes()` at `tools/bepd09d_real_execution_harness.py:361`; it is explicitly unsuitable. A producer cannot attest *absence of upstream forbidden physical reads* merely from a filtered downstream artifact or SHA.
* A — preexisting independently attested per-fold immutable train-only shards: admissibility NOT_ASSESSABLE, owner attestation/creation logs and independent byte scope absent; no content read authorized now.
* B — separately authorized owner-side one-time raw read: requires human adjudication of all physical exposure including current fold test answers, exact principal, byte scope, time, audit and destruction policy; FORBIDDEN now.
* C — prospective partition at acquisition before forming a monolith: NOT_IMPLEMENTED; new acquisition/data authority required.
All three options are design alternatives, **none selected operationally**.

## Frozen science and admissibility
259 Monday target weeks `2021-06-07..2026-05-18`; six contiguous blocks sizes `44,43,43,43,43,43`; fold f=1..5 trains exactly B1..Bf and tests B(f+1), with ordered train week counts `44,87,130,173,216`. Earlier fold tests may be future train folds legitimately but never current fold test. No test labels, test-row matrices, scoring, performance computations, source-wide data or future weeks in admitted view. The exact 10 RD5 synthetic fixture keys and semantics remain frozen (`tools/bepd09d_r2_rd5_synthetic_fixture.py` blob `c6d8b0e678270e379e758052c40be23355bc3800`); key names: `event_id,target_week_id,sweep_cluster_id,side,level_price_mid,take_h1_close_mid,take_h1_close_utc,level_age_weeks,active_level_count_at_target_week_start,same_week_reintegration`. No changes to response, features, folds, objective, Hessian, score, Candidate B solver or `TAU_SCORE`.
Admissibility must verify exact schema, data types (including strict bool not int), finite numeric fields, positive price, sorted canonical events, unique event IDs, cluster membership confined to valid training weeks, UTC timestamp normalization and session bounds **against frozen source contract**, not locally invented acceptance gates. Any unresolved calendar/DST question BLOCKED pending human adjudication.

## Separation of integrity, provenance, authority and science
SHA-256 provides content commitment; does not authenticate producer or authority. Synthetic Ed25519 can authenticate signer possession, but does not prove OS-level filesystem isolation, real source chain of custody or human physical-read permission. `fixture.PROVENANCE` is only a marker. `CONTENT_INTEGRITY != ORIGIN_AUTHENTICITY != DATA_ACCESS_AUTHORITY != SCIENTIFIC_ADMISSIBILITY`.
Synthetic signer must be separately named and untrusted for real. Future OS capability proof must establish denied ledger mounts, no inherited sensitive descriptors, separate fresh interpreter/process, denied network and forbidden cache/temp read; documentary process diagram is NOT a capability proof.

## Security gates and error semantics
Fail closed at, in order: G0 authority/scenario, G1 source+scientific exact identity, G2 trust-root signer/key revocation and signature, G3 fold/receiver/nonce/clock and delegated scope, G4 content digest and canonical view format, G5 row-level week/id/cluster/schema, G6 sealed handle, G7 bounded redacted receipt. If downstream import/module patch/single-use identity changes STOP. No exception message may become a public receipt. Unauthorized G0–G5 never gets raw view byte access at the **consumer** boundary; authenticator may need bounded contents later under an adopted synthetic grant.
No real producer or security PASS is asserted. Pending human materials: selection of owner read option, independent isolation verifier, trust-root custody/rotation, cryptographic signature variant, T1–T5 per-actor OS permission evidence, and exact retention and nonce atomics.
`RD6_03A=CONTRACT_CANDIDATE_DOCUMENTARY_ONLY`; `RD6_03B=NOT_AUTHORIZED`; `REAL_MATERIALIZER=BLOCKED`.
