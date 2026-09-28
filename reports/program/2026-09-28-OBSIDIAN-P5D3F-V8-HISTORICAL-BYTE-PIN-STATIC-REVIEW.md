# OBSIDIAN P5-D3F — V8 HISTORICAL BYTE-PIN COMPATIBILITY STATIC REVIEW

Date: 2026-09-28

## Evidence status

Same-assistant static review. Not independent execution evidence. Does not qualify P5-D3F.

## Exact V8 functional candidate

    6b45681bf060d6571782b83593a347ca6acd7a30

Runner:

    ec4ad41f26334e1350106c79650c6d381a7cfcdc

Runner tests:

    2adf0d72f3d4d7d007ee3ed3ee6ccb184431b2d2

P5-D3F contract, contract tests, and .gitattributes are unchanged.

## Static finding

V7 already proved locally that exact committed-byte materialization plus individually path-scoped stat reconciliation works for the existing compatibility set through the targeted P5-D3F gate.

The full-suite block exposed seven additional historical raw-byte-pinned P2/P3 dependencies whose local worktree bytes were CRLF while their Git blobs and filtered identities were LF.

V8 extends only BYTE_PIN_COMPATIBILITY_PATHS with those seven observed paths.

No pin value changes.
No historical test changes.
No contract semantic changes.
No new materialization mechanism is introduced.

The existing staged mode/OID/stage invariance breaker still surrounds the path-scoped refresh sequence.

## Expected effect

Directly supported:

- materialization_contract_v0_1.json raw-byte mismatch should be removed;
- materialize.py and the five qualified P2 core raw-byte mismatches should be removed;
- the three directly observed P2/P3 byte-pin failures should no longer fail for CRLF reasons.

Not yet independently proven:

- whether the P5-D3D and P5-D3E failures were entirely downstream cascades;
- whether the complete 1089-test historical suite passes after V8.

The unchanged full-suite gate adjudicates both questions.

## Verdict

    STATIC CORRECTION REVIEW = PASS
    V8 FUNCTIONAL CANDIDATE = READY FOR LOCAL GATE
    V8 LOCAL GOVERNED RE-BREAK = NOT EXECUTED
    P5-D3F CONTRACT = UNQUALIFIED
    P5-D3F IMPLEMENTATION = UNAUTHORIZED
    P5-D3G = CLOSED
    REAL VAULT WRITE = CLOSED
