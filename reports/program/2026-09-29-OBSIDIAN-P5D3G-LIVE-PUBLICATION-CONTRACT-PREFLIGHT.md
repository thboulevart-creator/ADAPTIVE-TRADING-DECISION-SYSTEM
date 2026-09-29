# OBSIDIAN P5-D3G — FINITE LIVE PUBLICATION TRANSACTION CONTRACT PREFLIGHT

Date: 2026-09-29

## Evidence status

READ-ONLY / STATIC RECONSTRUCTION.

No P5-D3G runtime exists.
No real Vault mutation is authorized or performed.
No CURRENT or CURRENT.tmp mutation is authorized or performed.

## Verified opening state

Source qualified checkpoint:

    3fcf9d34fec508ec93a87af1177023af7a8b51ab

New contract branch:

    feat/obsidian-projection-p5d3g-live-publication-transaction-contract-v0.1

No P5-D3G file or runtime existed at branch creation.

## Qualified predecessor authorities

### P5-D3F

Qualified finite retained handoff implementation candidate:

    a41c5b150168c2e4eb06648237022a4974868423

Implementation blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

Implementation qualification report blob:

    d1aafa4ab8e2dfea2fe8cb5d480e9126bc50f257

Sacrificial-staging qualification report blob:

    c99d74383c25653dd05e0831eb4eab355afb3b6e

Required retained-handoff terminal state:

    READY_UNAUTHORIZED

### P5-C2

Promotion contract blob:

    36e49e72a867e30a69f63eb413fd924d0e56297b

Qualification report blob:

    a928598182b25d110c9040c62d846bf9018ac3ed

Only selected filesystem primitive:

    IMMUTABLE_GENERATION_ATOMIC_POINTER

The directory-swap candidates remain unqualified / unsupported.

### P5-C3R2

Qualified runtime candidate:

    b5f3a8de061772e15bc94b20095d419130c20781

Open-compatibility blob:

    b970e65f21792cccc6ee2e4271d630f371102ff7

Retry implementation blob:

    df1a6988c5ce09d52941793a98f2a88728aaed41

Final qualification report blob:

    fd54a78abde8342c6da708d3a4096b4d0b267905

Qualified semantics include:

- CURRENT.tmp candidate write;
- fsync before replace;
- atomic os.replace(CURRENT.tmp, CURRENT.md);
- bounded write retry for Windows sharing conflicts;
- read-after-write verification;
- bounded reader retry for the qualified EACCES path.

Important limitation:

The exact P5-C3R2 test runtime is synthetic and hardcodes:

    GENERATION_IDS = ("GEN_A", "GEN_B")

Therefore P5-D3G may reuse the qualified pointer/retry semantics but must not claim that the exact synthetic GEN_A/GEN_B writer is already a production-generalized publisher.

### P5-D2

Observer implementation blob:

    fd212f61ec38332b677110f40265638af55a73e2

Qualification report blob:

    68cda09d273f19a2a93e1fcd9b0c393e72cd5a35

P5-D2 establishes:

    EVALUATION_PASSED != PROMOTION_CONFIRMED

PROMOTION_CONFIRMED may be emitted only after physical publication is actually verified.

## Missing boundary now opened

P5-D3G must define one finite live publication transaction from:

    verified P5-D3F retained handoff
        ↓
    immutable live generation materialization
        ↓
    verified complete target
        ↓
    atomic CURRENT pointer publication
        ↓
    read-after-write physical verification
        ↓
    durable publication evidence
        ↓
    P5-D2 PROMOTION_CONFIRMED

The transaction must remain finite.

It is not the P5-D4 observer loop.

## Mandatory contract decisions

The contract must freeze at least:

1. read-only publication planning before any write;
2. explicit one-shot human authorization bound to the exact plan;
3. single-writer ownership before first mutation;
4. fresh P5-D3F handoff reverification immediately before mutation;
5. exact previous CURRENT prestate capture;
6. immutable target-generation materialization;
7. exact target verification before pointer mutation;
8. CURRENT.tmp exclusive creation;
9. P5-C3R2-equivalent bounded replace/retry semantics;
10. read-after-write CURRENT + target verification;
11. crash-state classification;
12. deterministic rollback/recovery rules;
13. physical publication before logical PROMOTION_CONFIRMED;
14. durable transaction evidence outside the searchable live generation;
15. preservation of P6 as the future Graph/Search semantics boundary.

## Important productionization gap

P5-C3R2 validated a synthetic generation format with GEN_A / GEN_B.

P5-D3F produces a sealed package:

    package/
        generated/
        _atds_generation/

P5-D3G therefore requires a separately governed production live-generation wrapper.

The sealed P5-D3F package must remain byte-exact and immutable inside that wrapper.

No contract may silently reinterpret the synthetic P5-C3R2 generation manifest as already valid for arbitrary real generation IDs.

## Proposed physical wrapper

Contract candidate should use:

    <REAL_VAULT>/
        generations/
            <generation_id>/
                package/
                    generated/
                    _atds_generation/
                PUBLICATION-MANIFEST.json
                INDEX.md
        CURRENT.md

The inner package remains the exact P5-D3F package.

PUBLICATION-MANIFEST.json and INDEX.md are publication-wrapper artifacts outside the sealed package.

Graph/Search behavior of coexisting immutable generations remains explicitly unqualified and deferred to P6.

## Preserved closures

Until the P5-D3G contract itself is qualified:

    runtime implementation = CLOSED
    real Vault writes = CLOSED
    CURRENT/CURRENT.tmp mutation = CLOSED
    P5-D2 PROMOTION_CONFIRMED emission = CLOSED
    automatic publication = CLOSED
    background observer = CLOSED
    polling = CLOSED
    P5-D4 = CLOSED
    P6 Graph/Search semantics = CLOSED
