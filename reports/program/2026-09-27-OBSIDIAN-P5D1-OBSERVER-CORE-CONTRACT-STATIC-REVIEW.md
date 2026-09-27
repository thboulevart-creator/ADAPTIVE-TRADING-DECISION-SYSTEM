# OBSIDIAN P5-D1 — OBSERVER CORE CONTRACT STATIC REVIEW

Date: 2026-09-27

## Review status

This is a static review performed by the same assistant that produced the P5-D1 contract.

It is not an independent review.
It is not local runtime evidence.
It does not authorize P5-D2.

## Candidate reviewed

Functional candidate HEAD:

    06899f10a758a0a93575ca66c4e5c00fd936699e

Branch:

    feat/obsidian-projection-p5d1-observer-core-contract-v0.1

Evidence-only preflight commit:

    b86d0c72711595736842e7cdb74dfde602b480ca

## Scope reviewed

The P5-D1 delta was reviewed for:

- exact repository and branch authority;
- predecessor qualification identity;
- deterministic state-machine purity;
- separation of remote freshness from projection state;
- same-HEAD NOOP semantics;
- INITIAL / FAST_FORWARD eligibility;
- NON_FAST_FORWARD / UNKNOWN fail-closed behavior;
- qualification versus promotion separation;
- exact-head queue identity;
- active-evaluation immutability;
- last-known-good preservation;
- append-only audit semantics;
- volatile-data exclusion from deterministic digests;
- single-writer requirement;
- reuse of qualified P5-B2 / P5-C2 / P5-C3R2 components;
- P5-D1 runtime non-authorization;
- next-gate ordering.

## Static findings

    exact repository pinned                                      PASS
    exact monitored branch pinned                               PASS
    local working tree not authority                            PASS

    P5-A contract dependency pinned                              PASS
    P5-B2 qualification dependency pinned                        PASS
    P5-C2 qualification dependency pinned                        PASS
    P5-C3R2 qualification dependency pinned                      PASS
    P5-C3R2 runtime candidate pinned                             PASS

    transition defined as pure state function                    PASS
    network IO inside transition forbidden                       PASS
    filesystem IO inside transition forbidden                    PASS
    process launch inside transition forbidden                   PASS
    wall-clock dependency forbidden                              PASS
    environment-variable dependency forbidden                    PASS
    randomness forbidden                                         PASS
    byte-identical output requirement present                    PASS

    observer phase separated from projection state               PASS
    remote freshness separated from projection state             PASS
    deterministic state excludes timestamps                      PASS
    deterministic state excludes PID                             PASS
    deterministic state excludes host paths                      PASS

    SAME HEAD => NOOP                                            PASS
    SAME HEAD queue growth forbidden                             PASS
    SAME HEAD evaluation start forbidden                         PASS

    network failure preserves live head                          PASS
    network failure forbids new CURRENT claim                    PASS
    previous CURRENT degrades to STALE on freshness loss         PASS

    CURRENT requires freshness KNOWN                             PASS
    CURRENT requires observed == live                            PASS
    CURRENT requires live == last qualified                      PASS

    INITIAL may queue exact HEAD                                 PASS
    FAST_FORWARD may queue exact HEAD                            PASS
    NON_FAST_FORWARD auto-evaluation forbidden                   PASS
    NON_FAST_FORWARD auto-promotion forbidden                    PASS
    UNKNOWN auto-evaluation forbidden                            PASS
    UNKNOWN auto-promotion forbidden                             PASS

    evaluation start preserves live projection                   PASS
    evaluation PASS advances last_qualified_head only            PASS
    evaluation PASS preserves live projection                    PASS
    evaluation FAIL preserves live projection                    PASS
    promotion semantics modelled but execution unauthorized      PASS

    pending HEAD identity exact                                  PASS
    duplicate pending HEAD forbidden                             PASS
    observation order preserved                                  PASS
    active evaluation cannot be retargeted                       PASS
    supersession requires proven FF containment                  PASS

    append-only event required                                   PASS
    previous/input/decision/next digests required                PASS
    volatile envelope excluded from deterministic digests        PASS
    event log explicitly non-authoritative                       PASS
    event sequence strictly monotonic                            PASS

    single writer required                                       PASS
    second writer has no write authority                         PASS
    lock acquisition outside pure transition                     PASS
    lock-owner identity excluded from deterministic digest       PASS

    last-known-good required                                     PASS
    failed observation cannot change live head                   PASS
    failed evaluation cannot change live head                    PASS
    failed promotion cannot change live head                     PASS
    recursive LKG deletion forbidden                             PASS

    dynamic inventory must be reused                             PASS
    atomic pointer primitive must be reused                      PASS
    P5-C3R2 reader retry policy must not be weakened             PASS
    human views remain protected                                 PASS
    .obsidian remains protected                                  PASS
    Graph/Search CURRENT semantics remain deferred to P6         PASS

    observer implementation unauthorized in P5-D1                PASS
    network observation unauthorized in P5-D1                    PASS
    remote fetch unauthorized in P5-D1                           PASS
    background observer unauthorized in P5-D1                    PASS
    polling loop unauthorized in P5-D1                           PASS
    production promotion unauthorized in P5-D1                   PASS
    continuous Vault write unauthorized in P5-D1                 PASS
    Windows startup registration unauthorized                    PASS
    scheduled task unauthorized                                  PASS
    Windows service unauthorized                                 PASS

    required breaker count = 50                                  PASS
    required breakers unique = 50                                PASS
    Python contract-test methods = 24                             PASS

    P5-D2 next = one-shot observer tick                          PASS
    P5-D3 next = controlled candidate evaluation pipeline        PASS
    P5-D4 next = bounded observer loop candidate                 PASS
    P5-E remains end-to-end near-real-time qualification         PASS
    P6 remains controlled knowledge graph architecture           PASS

## Exact candidate blobs

Contract:

    tools/obsidian_projection/continuous_observer_core_contract_v0_1.json
    a20999ae991e07447e25ecd1592964f2d333449b

Contract breakers:

    tests/obsidian_projection/test_continuous_observer_core_contract_v0_1.py
    08cff6908535838a87ee71054295a67c94d5d529

Documentation:

    docs/OBSIDIAN-P5D1-CONTINUOUS-OBSERVER-CORE-CONTRACT-V0.1.md
    77bc4ca8c59d91d950e1d664afe76ecd712c77a9

## Delta boundary

Relative to the final P5-C3R2 qualification commit, the functional P5-D1 candidate adds only:

- one JSON contract;
- one Python contract breaker module;
- one Markdown protocol document.

No observer implementation module was added.

No polling code was added.

No Windows persistence mechanism was added.

No production Vault write path was added.

## Important limitation

No Python compilation, targeted breaker execution, full Obsidian test suite, background process, network observer, or real Vault mutation was executed by this static review.

## Verdict

**STATIC REVIEW PASS — LOCAL RE-BREAK REQUIRED.**

P5-D1 is not yet qualified.

P5-D2 remains unauthorized until the exact P5-D1 functional candidate passes its local re-break.
