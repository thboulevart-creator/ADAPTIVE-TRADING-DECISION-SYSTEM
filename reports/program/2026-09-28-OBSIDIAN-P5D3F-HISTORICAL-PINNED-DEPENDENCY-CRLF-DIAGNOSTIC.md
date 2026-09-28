# OBSIDIAN P5-D3F — HISTORICAL PINNED DEPENDENCY CRLF DIAGNOSTIC

Date: 2026-09-28

## Evidence status

USER-REPORTED LOCAL EXECUTION / DIAGNOSTIC.

Not independent execution evidence.

## Branch state before persistence

Verified remote HEAD:

    4047863e2286ae9c21d70117438d055ba5ddcc49

## Diagnostic result

Eight directly relevant P2/P3 dependency paths were inspected using:

- git rev-parse HEAD:<path>
- git hash-object --no-filters -- <path>
- git hash-object --path=<path> <path>
- git ls-files --eol -- <path>

Seven paths showed:

    RAW=MISMATCH
    FILTER=PASS
    i/lf
    w/crlf
    attr/text=auto eol=lf

Affected paths:

    tools/obsidian_projection/materialization_contract_v0_1.json
    tools/obsidian_projection/materialize.py
    tools/obsidian_projection/rendering.py
    tools/obsidian_projection/relations.py
    tools/obsidian_projection/integrity.py
    tools/obsidian_projection/builder.py
    tools/obsidian_projection/p2_verify.py

Representative exact identities:

materialization_contract_v0_1.json:

    HEAD=b11120c9...
    RAW=8a6b93e5...

rendering.py:

    HEAD=5111518b...
    RAW=0572ff84...

The control path:

    tools/obsidian_projection/first_open_safety_contract_v0_1.json

showed:

    RAW=PASS
    FILTER=PASS
    i/lf
    w/lf

The complete repository status still reported:

    STATUS_COUNT=0

## Adjudication

Supported:

- the seven failing dependency paths contain CRLF worktree bytes while their authoritative Git blobs are LF;
- Git's filtered identity matches the authoritative committed blob for all seven paths;
- Git logical cleanliness therefore does not imply raw byte identity for these historical byte-pinned checks;
- the historical expected pins themselves are not invalidated by this evidence.

The directly observed full-suite failures for materialization_contract_v0_1.json and rendering.py are explained by this raw-byte mismatch family.

The later P5-D3D and P5-D3E failures may be downstream cascades from the same package dependency mismatch, but that is not yet independently proven.

## V8 correction boundary

A candidate V8 may extend the existing byte-exact compatibility surface only to these seven already historical byte-pinned dependencies.

It must:

- preserve all historical expected blob values;
- write exact committed bytes only for the bounded compatibility paths;
- verify raw worktree blob == committed blob after materialization;
- path-scope Git stat reconciliation for every bounded path;
- require staged mode/OID/stage invariance;
- require final worktree cleanliness;
- run the existing targeted and full historical suites unchanged.

No historical repinning is authorized.
