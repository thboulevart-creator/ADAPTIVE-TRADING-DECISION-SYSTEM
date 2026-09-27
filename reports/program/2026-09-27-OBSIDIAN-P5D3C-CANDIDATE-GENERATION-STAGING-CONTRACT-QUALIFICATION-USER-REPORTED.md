# OBSIDIAN P5-D3C — CANDIDATE GENERATION STAGING CONTRACT QUALIFICATION

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following local Windows execution result was supplied by the user.
It was not independently executed by the assistant.

## Qualified functional candidate

Exact P5-D3C functional candidate:

    f3dc4b582fadff37ffb37108ec677ea88de7dad0

Branch:

    feat/obsidian-projection-p5d3c-candidate-generation-staging-contract-v0.1

Later branch commits before this qualification record contain only evidence/preflight/static-review reports and do not replace the tested functional candidate.

## Reported local re-break result

The user reported:

    Ran 877 tests in 11.955s
    OK
    P5D3C_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3C_LOCAL_REBREAK_COMPLETED=PASS

The governed wrapper reaches the final completion marker only after:

- exact functional-candidate checkout;
- exact staging-contract blob verification;
- py_compile of the P5-D3C contract-breaker module;
- targeted P5-D3B + P5-D3C contract tests;
- full tests/obsidian_projection regression suite;
- final source-clean control-checkout verification;

complete without a blocking exception.

This qualification therefore records the supplied run as the governed P5-D3C local re-break PASS.

## Qualified P5-D3C boundary

P5-D3C qualifies the candidate-generation staging contract only.

Qualified architectural properties include:

- a real candidate package is distinct from the P5-C2 synthetic GEN_A / GEN_B fixture representation;
- P5-C2 contributes the architectural property "complete immutable generation before pointer publication", not its synthetic fixture packager/verifier;
- package staging must occur in a fresh isolated root outside canonical worktree, real Vault and live generation namespaces;
- package layout is limited to generated/ plus _atds_generation/;
- CURRENT, CURRENT.md, CURRENT.json, CURRENT.tmp, views/, .obsidian/ and .git are forbidden package paths;
- payload must be an exact path/byte copy of an already verified deterministic projection;
- all payload files are independently enumerated, hashed and bound through a payload file-map digest;
- upstream projection_tree_digest_sha256 remains a distinct builder-owned identity and is not silently redefined by staging;
- generation identity binds exact candidate HEAD/tree, dynamic-inventory digest, semantic-bridge digest, semantic-record digest, projection contract, projection tree, generated-file count, payload digests, breaker PASS status, determinism PASS status, breaker evidence, determinism evidence and exact P5-D3C contract blob;
- generation ID is deterministic and digest-derived, not time/UUID/random/host/path-derived;
- generation manifest status before sealing is COMPLETE_PENDING_SEAL;
- SEAL.json must be created last and exclusively;
- valid seal status is SEALED_UNPROMOTED;
- candidate-generation digest is defined as SHA-256 of exact canonical SEAL.json bytes;
- logical immutability begins after a valid seal;
- any later payload/manifest/seal mutation, deletion or extra file invalidates the package;
- repair/reseal in place is forbidden;
- verification must be read-only and exhaustive;
- PASS_SEALED_UNPROMOTED does not imply live, CURRENT, promoted or Obsidian-visible state.

## Preserved non-authorizations

P5-D3C qualification does NOT authorize:

    staging packager implementation
    staging verifier implementation
    staging execution
    current-head builder adaptation
    relation-adapter execution
    finite evaluation orchestrator
    production promotion
    CURRENT mutation
    real Vault write
    background observer
    polling loop
    Windows startup registration
    scheduled task creation
    Windows service creation
    Graph/Search CURRENT semantics

## Verdict

**PASS — P5-D3C CANDIDATE GENERATION STAGING CONTRACT QUALIFIED**

Evidence basis:

    USER-REPORTED LOCAL EXECUTION

This is not independent local execution by the assistant.

## Next governed frontier

The next authorized boundary is:

    P5-D3C2 — CANDIDATE GENERATION STAGING IMPLEMENTATION AND SANDBOX QUALIFICATION

P5-D3C2 may implement the packager and read-only verifier defined by P5-D3C and exercise them only in a governed sacrificial staging environment.

It must still not:

- create or mutate CURRENT;
- invoke the P5-C2 promotion primitive;
- write into the real Vault;
- claim live/Obsidian visibility;
- implement the continuous observer;
- implement Graph/Search CURRENT semantics.

Only a verified SEALED_UNPROMOTED candidate package may emerge from P5-D3C2.
