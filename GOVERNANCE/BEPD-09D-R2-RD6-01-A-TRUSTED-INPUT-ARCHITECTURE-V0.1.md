# BEPD-09D-R2-RD6-01-A — TRUSTED INPUT ARCHITECTURE V0.1
**EVIDENCE:** Documentary design candidate / static source examination only. **NOT IMPLEMENTED, NOT ADOPTED, NO REAL ROW READ.** 2026-10-09.

## Authoritative bindings and immutable science
Parent HEAD `4b826d3a805dfd7555089453232e4cba2cb86eb1`, TREE `8fffd69faf361a2107ecd8b9d7205065d18fbc16`. RD5 closure blob `32137259fbd29008071528107cd4f86560ad3890`; RD5 adoption blob `cf3bb96620fe65622cdbdaa9b8f9fb37aacab519`; adopted synthetic adapter blob `bfbf586914c852047123c3a4cd1b2fa6a7dc4daa`. Model and C1 calendar binding may not change.

Known ledger identity from FROZEN RD4 METADATA ONLY: path `artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/EVENT_LEDGER.jsonl`, Git blob `0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2`, declared SHA256 `301a621b97fea14a72540d4c2c6da78eb742cc44c5009e44ad98e9f678ca4731`, declared 472 rows and 754544 bytes. These are **unrecomputed declarations**, not newly verified content. Frozen C1 weeks = 259, from 2021-06-07 to 2026-05-18; B1=44, B2–B6=43 weeks; first source-run week 2021-05-31 excluded in C1 documentary reconciliation.

## Fundamental physical-read impossibility
A producer **cannot derive new fold-filtered views from a monolithic unindexed JSONL ledger without inspecting some of its bytes**, and the inherited `tools/bepd09d_real_execution_harness.py` explicitly invokes `LEDGER_PATH.read_bytes()` (source line 361). Reading the whole file to compute its digest, to filter it or to verify it **is already a whole-file physical read**. A downstream model can be barred from seeing the full ledger, but that fact DOES NOT retroactively authorize upstream physical exposure. Therefore:
- If **NO CURRENT-FOLD TEST RESPONSE READ** applies to every actor, a monolithic ledger is not directly eligible for any materialization requiring reading test-response bytes. **BLOCKED** pending preexisting *independently verified* physical partitions or a changed human authority boundary.
- Option A (conditional): use **preexisting, physically scoped and independently attested train-only immutable shards**, provided proof of creation, byte provenance and original scope exists. No such shards or attestation have been verified in RD6-01; **NOT ASSESSABLE**.
- Option B (conditional): separately authorize a highly constrained **data-owner-side one-time raw ledger pass** and explicitly adjudicate the physical exposure of all rows, including protected responses, for *that producer only*; model worker must never gain that scope. This is a **material new real-data exposure** and is **NOT AUTHORIZED** by RD6-01.
- Option C: redesign source acquisition prospectively to emit partitioned immutable views before a monolithic corpus arises. Requires independent acquisition authority and is **NOT IMPLEMENTED**.

## Proposed trust boundary and roles
```text
TRUSTED_CANONICAL_DATA_OWNER [may hold frozen data, NO NEW READ PER RD6-01]
  | separate human grant and auditable scoped materialization required
  v
ISOLATED_VIEW_PRODUCER [no code or privilege granted]
  | emits immutable TRAIN_ONLY scoped objects plus signed/attested manifest
  v
VIEW_AUTHENTICATOR / INTEGRITY GATE [read manifest + bounded train-only object]
  | no raw ledger access; checks signer, identities, digest, schema, folded ids
  v
SYNTHETICALLY_QUALIFIED_RD5_LOGIC [requires a NEW real input integration and review]
  | only train X,y and ephemeral fit diagnostics, NO test design
  v
ALLOWLIST_EXPORTER + GOVERNED RECEIPTS [no rows, X/y, coefficients, or scores]
```
Separate operating-system privileges, credentials, paths, process boundaries and audit logs must enforce—not merely narrate—the trust separation. Git object SHA binds bytes but does **not** certify origin, signer, role or allowed access; a caller-provided `RD5_SYNTHETIC_GENERATED_IN_PROCESS` marker is not provenance authentication.

## Permission matrix — **proposal, not operational permission**
| Component | Original ledger bytes | Scoped train view | Current-fold test responses | Fit parameters | Public diagnostics |
|---|---|---|---|---|---|
| Canonical data owner | Existing custody only; **new reads forbidden in RD6-01** | No creation yet | No new read permission | No | Metadata only |
| Future isolated materializer | **Separately authorized only** | Write once per authorized fold | Only if separately and expressly adjudicated; otherwise STOP | No | Manifest only |
| Authenticator | Never | Read exactly nominated fold | Never | No | Gate status |
| RD5 adapter/model | Never | Future admitted bytes only; currently synthetic only | Never | In-memory ephemeral only | Allowlist |
| Independent reference fit | Never | Same authorized train matrix only, future grant | Never | In-memory, no fallback | Independent diagnostics |
| Audit/persistence | Never | Digest+metadata only | Never | Never | Redacted fixed schema |
| External reviewer | Never | Synthetic fixtures/documentation only | Never | Never | Static findings |

## Immutable train-view contract candidate
The prospective signed machine-manifest MUST bind: exact producer identity and delegated authority id; authorized ledger *manifest* Git object and cryptographic source digest; C1 partition/calendar Git blobs; fold index 1..5 and exact ordered train week IDs/block IDs; nonempty current test-week denylist digest **without test responses**; schema/version; immutable view object byte digest, immutable length, strict row count, per-week and per-cluster uniqueness counts (metadata only); content-addressed object id; timestamp and single-use nonce/attempt id; provenance signature/attestation of producer key trusted by consumer; admitted feature/response fields only; serialization canonicalization (including timezone, NaN rejection, no duplicate JSON keys); precise consumer identity and expiry; stop state. **No test-row data should be included in the view or its logs.** A digest alone provides integrity, not absence of forbidden test-response reads; proof requires trusted execution boundary/permissions plus auditable producer logic and materialization authority.

A future view must contain strictly the training subset by *current fold*. F1 train B1/test B2 (44 weeks); F2 train B1–B2/test B3 (87); F3 train B1–B3/test B4 (130); F4 train B1–B4/test B5 (173); F5 train B1–B5/test B6 (216); each protected test 43 weeks. Earlier test blocks may be training blocks later, according to frozen chronology. Never mix exposure semantics across folds.

## Required negative authorization and isolation tests — future only
Reject: manifest without verifiable signer; signer not delegated for requested fold; materialization created after authority expiry; source/partition/consumer blob drift; current-test-week row/response; off-calendar row; unbound/untracked entry; cluster crossing an inadmissible week; duplicate id; partial/missing view; extra columns, NaN/nonfinite or timestamp/DST mismatch; source identity mismatch; replay/reuse nonce; output contains rows, paths, coefficient vector, unredacted exceptions or predictions; attempts at filesystem open of source ledger; inherited full-ledger harness; temporary/cache/trace spill; network egress; proof of scope absent.

External review must inspect process privilege boundaries, sandbox mount policy, filesystem syscalls or equivalent attestation, no DEBUG/exception string leakage, secret and MAC-key custody, signed audit events, TTL, deletion/retention, and concurrency/nonce isolation.

## Explicit static source findings
- `tools/bepd09d_r2_rd5_training_only_adapter.py` lines 86–105 checks a caller-supplied provenance **string** and caller-supplied list; it cannot prove the list was sourced from a trusted producer. It is intentionally limited to synthetic inputs.
- RD5 lines 171–220 builds `validate_rows`, `_stats` and `_mats` from rows *already* supplied; no real materializer is implemented.
- `tools/bepd09c_runtime.py` lines 130–136 constructs test matrices/predictions/scores: **legacy `run_protocol` is prohibited**.
- `tools/bepd09d_real_execution_harness.py` lines 361–399 loads full ledger and invokes `run_protocol`; prohibited for train-only and physical-read guarantee.
- Read of source ledger in RD6-01: **NONE**. Manifest records are preexisting metadata, not fresh empirical validation.

## Decision packet
**Recommended architecture choice:** adopt an attested per-fold immutable train-only view interface **as a design constraint**, reserve any producer read semantics to an independent human decision. **Do not human-adopt a real read permission, materializer or view today.**
`A_ARCHITECTURE_DESIGN=PASS_DOCUMENTARY`; `A_PHYSICAL_READ_BOUNDARY=BLOCKED`; `A_ATTESTED_REAL_VIEW=NOT_ASSESSABLE`; `A_REAL_MATERIALIZATION=NOT_AUTHORIZED`.
