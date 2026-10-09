# BEPD-09D-R2-RD6-03A-B — TRUST BOUNDARY & CAPABILITY MATRIX V0.1
**PROPOSED SECURITY MODEL ONLY — NOT PROVEN OS ISOLATION.** Bound to HEAD `5ed4d74ec1aab2fd7e215eabeb995faadfc72625`. No execution or real data access.

| Role / boundary | Real ledger | Synthetic rows | Frozen train-only object | Test labels | Signer key | Output | Authority / STOP |
|---|---|---|---|---|---|---|---|
| Canonical data owner (T0–T1) | Existing custody; new read **DENIED** | synthetic metadata only | no production shard issuance yet | no new exposure grant | none | authority metadata | separate human physical-byte grant mandatory |
| Isolated view producer (T1–T2) | **DENIED** in RD6-03A and RD6-03B | future synthetic fixture input only | future synthetic write-once | **DENIED** | synthetic signer only, isolated | manifest + view digest | no privileged real owner scope |
| View authenticator (T2–T3) | **DENIED** | synthetic view payload future | future bounded verification/read | **DENIED** | public trust anchor only | opaque single-use handle or breaker | verify signature+view+fold+expiry+receiver+nonce |
| Train-only consumer (T3–T4) | **DENIED** | future authenticated fixture only | train-only handle scoped to fold | **DENIED** | **DENIED** | internal training arrays only under future grant | no `run_protocol`, no test scoring |
| Redacted exporter (T4–T5) | **DENIED** | **DENIED** | **DENIED** | **DENIED** | **DENIED** | bounded allowlisted scalars/digests only | reject nesting/free-text diagnostic errors |
| External reviewer | **DENIED** | documents only now | **DENIED** | **DENIED** | **DENIED** | signed external report after distinct grant | no external review completed |

**Read-meaning rule:** a process that reads the full source, even only to compute a hash or filter, has exposed all its bytes. A downstream bounded consumer does not cure upstream overbroad physical exposure. This is a real-data authority defect, not merely a schema failure.

### Candidate physical owner options
| Option | Actor allowed to see physically | Required proof before future admission | Residual uncertainty | Current decision |
|---|---|---|---|---|
| A: preexisting attested train-only shards | Preexisting qualified owner only, current proposed model workers none | exact shard origin and independent creation/byte-scope attestation; immutable hash and signer; no test bytes in shard | real shards not confirmed to exist; prehistorical source read unknown | NOT_ASSESSABLE, no verification-by-content |
| B: explicitly delegated owner materialization | Only newly authorized independent owner-side materializer, **potential whole ledger including test labels** | separate human grant accepting that exposure, audited read scope/time/principal, deterministic one-pass constraints and denial to all other actors | irreversible test exposure / science contamination policy | FORBIDDEN |
| C: prospective partition at ingestion | acquisition owner bounded per-shard source | approved architecture and upstream acquisition authority, sealed per-fold/views plus trustworthy collection attestation | not implemented; future source quality unknown | NOT_IMPLEMENTED |

### Threats and required future proof
T1/T2 forged owner/overbroad physical read -> OS ACL/process/mount/read-syscall evidence; audit principal and negative filesystem access probe; metadata and synthetic only here.
T2/T3 forged signer/manifest -> Ed25519 verify, cryptographic trust root outside attacker control, exact signed domain, deny revoked or expired key; synthetic-only fixtures.
T3/T4 future-week/test label escape -> freeze ordered train-week list, calendar code blob, strict response field list; deny before consuming any row.
T4 global imports -> separate worker process, require code/dynamic import identities, deny inheriting `_base.fit_logistic` mutation; controls not proven.
T5 output poisoning -> recursively typed schema, fixed status codes, field/array/text-length caps, no tracebacks, no raw label, paths, coefficients, probabilities or PnL.
Unknown privilege, cannot attest inherited descriptors, signer key custody absent, anti-replay store not atomic, no crypto provenance or tested barriers -> BLOCKED.

### Trust control proof levels
`DOCUMENTARY_SPECIFIED`: RD6-03A possible.
`SYNTHETIC_TESTED`: not until separately authorized RD6-03B.
`EXTERNALLY_INDEPENDENTLY_REVIEWED`: no evidence today.
`OS_ACCESS_BOUNDARY_QUALIFIED`: no evidence today.
`REAL_PHYSICAL_READ_AUTHORIZED`: no.
`REAL_TRAINING_ADMISSION`: BLOCKED.

### Future security environment prerequisites
Explicit process UID/security principal and capability list; sandbox path and symlink/TOCTOU defense; no shared temp, no inherited FD, no subprocess escape, network egress denied, no debugger secrets, immutable artifact IDs, auditable FS attempts, schema-enforced output. Attack simulations do not prove real OS isolation. No hidden credentials or secret material may be committed in any RD6-03A document.
