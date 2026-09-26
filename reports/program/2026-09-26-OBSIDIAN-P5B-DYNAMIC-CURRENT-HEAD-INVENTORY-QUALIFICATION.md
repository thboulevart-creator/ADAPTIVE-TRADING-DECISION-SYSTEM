# OBSIDIAN P5-B — DYNAMIC CURRENT-HEAD INVENTORY QUALIFICATION

Date: 2026-09-26

## Scope

This record closes P5-B, the contract-and-breakers phase for deterministic dynamic source inventory on every exact monitored Git HEAD.

## Persisted candidate

Branch:

    feat/obsidian-projection-p5b-dynamic-current-head-inventory-v0.1

Persisted candidate HEAD:

    4923b1325d08e665d4eae2e24224f374bfe1138d

Qualified predecessor P5-A:

    343d253074abe603eb61bebab29ba58f0bd9301c

## User-reported local execution

The user reported:

    Ran 372 tests in 7.117s
    OK

    P5B_PERSISTED_LOCAL_REBREAK_PASS
    CONTROL_CLONE_CLEAN=PASS

Control clone:

    C:\Users\Boulevart\AppData\Local\Temp\ATDS-P5B-123c1c92527e42b384cf530866f12dfa

This runtime evidence is USER-REPORTED LOCAL EXECUTION, not independent execution evidence.

## Qualified boundary

P5-B qualifies the source-selection and deterministic inventory contract for continuous projection.

Qualified rules include:

- inventory authority is the exact Git tree of the exact monitored HEAD;
- working tree and Git index are not inventory authority;
- every tracked regular blob is inventoried unless an explicit safety exclusion blocks the HEAD;
- unknown future top-level directories are inventoried as OTHER_TRACKED instead of being silently dropped;
- selection zones are provenance/navigation labels only and do not imply semantic role, authority, qualification or scientific state;
- symlinks and gitlinks block the HEAD;
- derived/runtime surfaces such as generated/, views/, .obsidian/, caches and vendored runtime trees block the HEAD;
- sensitive-path candidates block projection;
- FULL_TEXT is limited to <= 1 MiB, valid UTF-8, no NUL, allowlisted extension and secret-scan PASS;
- large/binary/non-text artifacts remain visible as METADATA_ONLY without source-body semantic use;
- deterministic inventory records contain Git-derived stable fields only;
- exact commit/tree/blob identity and size are mandatory;
- delta semantics ADDED / REMOVED / MODIFIED / UNCHANGED do not create semantic rename relations.

## Reference census

At the design HEAD:

    6aef3b1304313c3446c08a3a37b51ea61733f41e

the observed Git tree contained:

    908 tracked regular blobs
    890 FULL_TEXT candidates
    18 METADATA_ONLY candidates

These counts are non-normative and are not future runtime constants.

## Non-authorizations preserved

P5-B does not authorize:

- continuous observer execution;
- Vault writes;
- projection promotion;
- semantic-classifier changes;
- mutation of the historical 74-artifact pilot.

## Verdict

**PASS — P5-B DYNAMIC CURRENT-HEAD INVENTORY CONTRACT QUALIFIED**

The next authorized candidate boundary is:

    P5-B2 — DYNAMIC INVENTORY IMPLEMENTATION CANDIDATE

P5-B2 must implement the qualified contract, survive synthetic adversarial mutants, and reproduce the current-head census before P5-C atomic-promotion work proceeds.
