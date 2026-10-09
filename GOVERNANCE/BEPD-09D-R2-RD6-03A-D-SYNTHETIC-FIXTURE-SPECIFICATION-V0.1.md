# BEPD-09D-R2-RD6-03A-D — SYNTHETIC FIXTURE SPECIFICATIONS V0.1
**DESIGN ONLY / no generated file and no executable test.** Frozen source fixture `tools/bepd09d_r2_rd5_synthetic_fixture.py`, Git blob `c6d8b0e678270e379e758052c40be23355bc3800`; prior RD5 synthetic GREEN `29/29 PASS` retained as historical evidence, not rerun.

## Deterministic generation (future separate RD6-03B grant only)
Start with exact RD5 frozen `WEEK0=2021-06-07`, block lengths `44,43,43,43,43,43`, weeks=259 ending `2026-05-18`. Generate `training_rows(fold=f,per_week=6)` in-memory only. Stable row count per fold: F1=264, F2=522, F3=780, F4=1038, F5=1296 (synthetic fixture counts, **NOT historical real counts**). Frozen row keys: event_id, target_week_id, sweep_cluster_id, side, level_price_mid, take_h1_close_mid, take_h1_close_utc, level_age_weeks, active_level_count_at_target_week_start, same_week_reintegration.
The RD5 fixture uses deterministic `SHA256('RD5/FIXTURE/<week>/<j>')` IDs, `RD5/CLUSTER/...` and synthetic response seeds; do not invent new scientific input distributions. For contrast tests involving tampered manifests, derive a separate synthetic envelope only: `SYNTHETIC_TEST_ROOT = SHA256('ATDS/RD6-03B/TEST-KEY/SEED-V0.1')`, `TEST_NONCE[i] = SHA256('RD6-03B/NONCE/'+scenario_id)` truncated to 24 bytes. These are **public test vectors, not production secrets**.

## Core positive fixtures
* FX-P01 valid synthetically signed and frozen F1/B1 view; expected future `ADMITTED_SYNTHETIC` with no real ledger access, used once.
* FX-P02..P05 valid F2..F5; historical former test weeks admitted only when they are current training (F2 B2 permitted, F1 B2 denied).
* FX-P06 deterministic identical fixture replay from same generation with **distinct nonce**; same canonical view byte digest, different envelope identity, accepted only if fresh explicitly authorized attempt.
* FX-P07 valid output receipt containing only public enum statuses and fixed evidence digests.

## Fixture mutation boundary (never applied in RD6-03A)
Each RED case starts from a unique valid synthetic fixture, applies exactly one preregistered mutation, keeps all others unchanged, and specifies an independently checkable denial oracle. Mutations may include forged provenance and signer, signature byte flip, manifest-vs-view mismatch, wrong fold, wrong receiver, current test week injection, stale timestamp, duplicate event/cluster, row key/type mutation, inherited FD/capability stub, denied path access simulation and nested diagnostic payload.
No mutation shall include actual ledger rows or actual broker/cloud secrets. No filesystem read of full ledger or real shard to validate expected digests. A future synthetic mock named 'ledger' may be used **only in a separately authorized isolated test workspace** and may not alias real repo path.

## Synthetic signed envelope classes
`AUTH_OK`: synthetic private/public key pair in ephemeral test-only sandbox, signer allowlisted in an ephemeral synthetic trust store, exact signed JCS domain. 
`AUTH_BAD`: altered payload, invalid signature, different key, unknown signer, revocation, expired/unknown authority, nonce replay.
`SCOPE_BAD`: F1 attempted B2, future B3..B6, cluster cross-week contamination, unauthorized date.
`VIEW_BAD`: one bit altered after signing, duplicate/extra JSON key, nonfinite numeric, wrong content length, non-canonical row order, wrong view-byte digest, duplicate IDs.
`PROCESS_BAD`: simulated unauthorized inherited ledger descriptor, cross-process state leak, global import monkeypatch, uncontrolled subprocess/egress; only synthetic mock capability and independent source inspection can be claimed until real OS isolation attested.
`EXPORT_BAD`: nested raw row/response/coefficient/path/traceback/unknown field/oversize Unicode string.

## Exact observed-vs-prospective distinction
`RD6_03A_FIXTURE_SPECIFIED=YES`; `FIXTURE_GENERATED=NO`; `TESTS_WRITTEN=NO`; `TESTS_EXECUTED=0`; `RED_OBSERVED=NONE`; `GREEN_OBSERVED=NONE`; `CRYPTOGRAPHY_QUALIFIED=NO`; `REAL_DATA_BYTES_READ=0`.
Synthetic fixture **cannot** prove owner physical-read authority, real data-chain provenance or production key custody. Those remain independent blockers.
