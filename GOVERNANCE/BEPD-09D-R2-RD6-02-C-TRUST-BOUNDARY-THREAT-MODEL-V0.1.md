# BEPD-09D-R2-RD6-02-C — TRUST-BOUNDARY THREAT MODEL V0.1
**Static design analysis, NOT an independently verified production security boundary. 2026-10-09.**
Source parent: `8b14b3f2be26487e74f946c1a48044ab03595f2e`; frozen C1 folds, RD2–RD6-01 authorities and protected blobs unchanged.

## Protected assets and non-negotiable invariants
Protected information: monolithic historical ledger bytes; current-fold test response labels; train-only fold records; ephemeral design matrices and coefficients; repository Git source identity; solver numerical decision and break codes; outputs/logs/temp files; signing keys for a future producer; execution budgets. Protected authority: no real data read, no new fit, no real materializer, no independent external security PASS from this review. Financial/trading outputs never authorized.

C1 documentary partition: 259 contiguous weeks from 2021-06-07 to 2026-05-18: B1=44, B2..B6=43. For fold f, train B1..Bf, test B(f+1); prior fold-test may be legitimate later-fold train. The caller-provided marker `RD5_SYNTHETIC_GENERATED_IN_PROCESS` is **not** an authenticated origin or process capability. RD5 rejects wrong week IDs *after receipt*, not unauthorized upstream physical reading.

## Five trust boundaries and threat paths
| Boundary | Untrusted or mutable actor | Assets at risk | Candidate security control, NOT implemented | Present verdict |
|---|---|---|---|---|
| T1: canonical owner → physical source read | full real ledger, owner process and credentials | hidden test responses, entire source bytes | *separate human authorization*, OS filesystem read capability bound to principal/byte scope, audited sensitive access | BLOCKED |
| T2: owner → proposed producer | producer loader, indexing, JSONL parser, workspace | raw responses, unapproved fold population, logs, cache | isolated process, signed immutable train-only shards, transcript of source access, no public raw data | BLOCKED |
| T3: producer → consumer | unauthenticated manifest, forged fold and view id | model may receive untrusted real bytes/test leaks | accepted signer identity + signed view digest + per-fold attestation + nonce + strict schema + fresh Git binding | BLOCKED |
| T4: admitted train-only view → RD5 adapter | caller-supplied rows and marker, shared interpreter | training/test isolation, scientific invariant, LP failures | synthetic status retained; new bounded real admission wrapper, no ledger mount, fail-closed LP and process isolation | BLOCKED |
| T5: numerical runtime → diagnostics/reviewer | exception strings, serialized nested metadata, workflow artifacts | sensitive rows/coefficient disclosure, model performance | recursive output allowlist and redaction, no test scoring, no network | BLOCKED |

Explicit scope distinction: a model process with no full-source mount can be isolated from the ledger, **but a producer that first reads the entire monolithic source has physically seen protected test responses**. Hashing that source or filtering afterward is an actual read; only a separately human-adjudicated owner authority or independently attested pre-sharded input could change the boundary.

## Source-backed attack narratives — hypothetical, not executed
1. **Forged provenance:** attacker supplies real-derived rows with known synthetic marker. `_identity_gate` compares a string (`RD5 adapter 86–94`), not cryptographic origin; a future real admission process MUST fail closed.
2. **Misleading LP failure:** `RD3 build_packet 127–133` catches exceptions, sets sep=False; `perfect_separation 72–84` collapses `linprog.success`; unknown may be treated as no separator. Even an independently called LP check is not a provenance guarantee.
3. **Tracing bypass concern:** exact Python frame identity (`RD5 149–168`) may miss threads/native code/code-object mutation; no test of these paths in RD5 GREEN; do not claim actual exploited bypass.
4. **Global import coupling:** `bepd09d_r2_runtime.py 19` mutates `_base.fit_logistic`, so a shared interpreter's import ordering may change effective runtime; isolate subprocess.
5. **Output contamination:** top-level allowlist (`RD5 42–53`) but nested optimizer message from downstream solver (`RD5 213–219`) not schema-constrained; possible source of unexpected fields or text.
6. **Whole-source leakage:** `bepd09d_real_execution_harness.py:361` reads complete file before `:399` legacy `run_protocol`; do not reuse for train-only.
7. **Reference fallback and scoring:** `bepd09c_reference.py:63–88` constructs test scores/probabilities and is forbidden for train-only parity; no real reference authorization.
8. **Receipt/replay abuse:** unauthenticated future signer, replayed view nonce or fold substitution can undermine current-fold scope; future synthetic tests and human adoption required.

## Trust policy candidates for separately authorized future work
* Deny-by-default process identity and capability: only trusted producer principal can bind view; model worker cannot open ledger or credential store; reference worker cannot open tests.
* Immutable manifest with exact original view-byte digest, row/size budget, source/partition Git bindings, authorizing human grant identifier, fold id, train/test block digests, signer key id, nonce, time-limited consumer identity, anti-replay store.
* Independent attestations: audit of actual physical read permissions, process image/entry point, use of encrypted temporary storage if needed, fail-closed cache deletion, absent network egress, one-shot worker lifecycle.
* Strict output allowlist: no raw response values, rows, X/y, coefficients, diagnostics containing paths/tracebacks or scientific performance, parameter-ranking or signals.
* Conditional opening: human decision separately for each **physical read** and each **primary/reference fit**; missing evidence = STOP.

## Dependency on unresolved independent review
No external independent report, reviewer signature, external hostile test logs or real materialization audit exists within RD6-02. `INDEPENDENT_EXTERNAL_REVIEW=NOT_ASSESSABLE`. All existing RD5 synthetic GREEN evidence is retained, not upgraded. `TRUST_BOUNDARY_REAL_READINESS=BLOCKED`.
