# P5-D3F Recovery V0.4 — Qualified-Blob Rebind Amendment V0.1 — Qualification

Date: 2026-09-30

## Scope

This report qualifies the narrow P5-D3F Recovery V0.4 real-execution-runner identity rebind only.

It does not authorize or record any real P5-D3F execution, persistent handoff materialization, real Vault write, CURRENT.md/CURRENT.tmp mutation, live publication, PROMOTION_CONFIRMED, real Stage A, Stage B, P5-D4, P6, polling, background observer, scheduled task, or Windows service.

The one-shot human authorization `AUTHORIZE_ONE_P5D3F_PERSISTENT_READY_UNAUTHORIZED_HANDOFF` was not consumed during this qualification.

## Source state

- Source branch: `feat/obsidian-projection-p5d3g-production-enablement-dependency-pin-requalification-v0.1`
- Source HEAD: `4cf7d94f9c8d49e647ec56fbf55d8afc9d892f51`
- Qualification branch: `feat/obsidian-projection-p5d3f-recovery-v04-qualified-blob-rebind-amendment-v0.1`
- Fully tested qualification HEAD: `426f9888dfd49044854b52bc7db11b3206dcb647`

## Historical authority preserved

The historical Recovery V0.4 authority was not silently rewritten.

- Historical runner blob: `0dfb31d86c84739fc66ee7efb6ca82e97396d87b`
- Historical runner test blob: `667e458962aca47a1d3f08ef3f12c80015c1390b`
- Historical runner re-break blob: `e6c9ab7f98c9fa8f77db3dc98571120e6cbeb7c0`
- Historical expected persistent handoff blob: `dcd70a9d9794675eab90e41df560f8b030b5dbf3`
- Historical expected P5-D3F blob: `2108131914cf65bb076b80f5bb63cd63267567fa`

## Effective requalification

The effective runner binding is explicitly distinct from historical authority.

- Amendment contract blob: `3667488c6cb7a348eab6564b7152049e0ba32d3b`
- RED test blob: `46f3e2886b7b22d167fcd352521c8db22ac8c2bf`
- Requalified Recovery V0.4 runner blob: `9228ea75d269c9bfc89537374dec5990498c3e4a`
- Qualified persistent handoff wrapper blob: `375607d88bc926e4fd4c297ddc6fedba5506642a`
- Qualified P5-D3F promotion handoff blob: `23a4cc69b3b9f6fab1a6d77bed0247fce9b69c60`
- Qualified persistent destination verifier blob: `398bda75604f8172128fbe0ddaf78cab4cee9f92`
- Dedicated re-break blob: `364bc57d7bf70aa33819ffa16b3a35d4a935ab90`

The runtime change was limited to the effective amendment/branch/blob identities and exact-runtime verification binding. The historical constants remained present and unchanged.

Runtime candidate diff: 19 insertions, 3 deletions.

## RED evidence

After normalizing the contract pin to the committed Git blob, the preregistered test suite produced a discriminating RED:

- 6 tests total
- 4 PASS
- 1 FAIL
- 1 ERROR

The remaining failures were exclusively the absence of the new effective binding surfaces: `RECOVERY_V04_REBIND_AMENDMENT_CONTRACT_BLOB` and `EFFECTIVE_RUNNER_BRANCH` / effective runtime identity surfaces.

No historical test was weakened to obtain GREEN.

## Targeted qualification

After the minimal runtime rebind: new amendment tests + historical Recovery V0.4 tests = 17/17 PASS.

Historical runner test and historical runner re-break remained byte-exact.

## Dedicated Recovery V0.4 synthetic re-break

- Targeted: 17/17 PASS
- Full Obsidian: 1316/1316 PASS
- Full duration: 180.884 s
- CONTROL_CLONE_CLEAN_BEFORE=PASS
- REMOTE_RACE_GUARD=PASS
- P5D3F_RECOVERY_REAL_RUNNER_BLOBS=PASS
- P5D3F_RECOVERY_REAL_RUNNER_SURFACE_SCAN=PASS
- P5D3F_RECOVERY_REAL_RUNNER_PY_COMPILE=PASS
- P5D3F_RECOVERY_REAL_RUNNER_TARGETED=PASS
- P5D3F_RECOVERY_REAL_RUNNER_FULL_REBREAK=PASS
- CONTROL_CLONE_CLEAN=PASS
- P5D3F_RECOVERY_REAL_RUNNER_REBREAK_COMPLETED=PASS

The re-break was synthetic only and performed no persistent staging or real Vault access.

## P5-D3G regression qualification

- Direct P5-D3G qualification: 25/25 PASS in 79.735 s
- Production Enablement / dependency-pin qualification: 23/23 PASS in 48.047 s

## P5-D3F regression qualification

- Targeted: 85/85 PASS in 22.918 s
- Full Obsidian: 1316/1316 PASS in 190.813 s
- CONTROL_CLONE_CLEAN_BEFORE=PASS
- REMOTE_RACE_GUARD=PASS
- P5D3F_PERSISTENT_VERIFIER_AMENDMENT_BLOBS=PASS
- P5D3F_PERSISTENT_VERIFIER_AMENDMENT_SURFACE_SCAN=PASS
- P5D3F_PERSISTENT_VERIFIER_AMENDMENT_PY_COMPILE=PASS
- P5D3F_PERSISTENT_VERIFIER_AMENDMENT_TARGETED=PASS
- P5D3F_PERSISTENT_VERIFIER_AMENDMENT_FULL_REBREAK=PASS
- CONTROL_CLONE_CLEAN=PASS
- P5D3F_PERSISTENT_VERIFIER_AMENDMENT_REBREAK_COMPLETED=PASS

## Adjudication

`RECOVERY_V04_QUALIFIED_BLOB_REBIND = PASS`

`RECOVERY_V04_TARGETED = PASS`

`RECOVERY_V04_FULL_OBSIDIAN_REBREAK = PASS`

`P5D3G_DIRECT_REGRESSION = PASS`

`P5D3G_PRODUCTION_ENABLEMENT_REGRESSION = PASS`

`P5D3F_TARGETED_REGRESSION = PASS`

`P5D3F_FULL_OBSIDIAN_REBREAK = PASS`

`REAL_P5D3F_EXECUTION = NOT_STARTED`

`PERSISTENT_HANDOFF_MATERIALIZATION = NOT_EXECUTED`

`REAL_VAULT_WRITE = NONE`

`LIVE_PUBLICATION = NOT_EXECUTED`

`P5D3F_ONE_SHOT_AUTHORIZATION = NOT_CONSUMED`

## Next boundary

`P5-D3F — FRESH PRE-EXECUTION REAL-ENVIRONMENT PREFLIGHT`

The next operation is read-only. It must freshly verify repository/remote identity, exact requalified runner and qualified blobs, monitored branch HEAD/tree, exact persistent staging recovery prestate, real Vault identity, CURRENT.md/CURRENT.tmp state, before/after real Vault fingerprints, and control-clone cleanliness.

Mandatory STOP before any real P5-D3F execution.
