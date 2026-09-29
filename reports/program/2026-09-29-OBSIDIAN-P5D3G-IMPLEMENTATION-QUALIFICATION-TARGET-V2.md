# OBSIDIAN P5-D3G — IMPLEMENTATION QUALIFICATION TARGET V2

Date: 2026-09-29

## Evidence status

Static qualification target only.

No local P5-D3G implementation execution is claimed here.

## Corrected exact candidate

    88e222c0ab95f683b36a9ac08a8b9929a83b5994

Implementation blob unchanged:

    eb0e6607430d32fe51c065ed4bacba05721f42b6

Implementation tests blob unchanged:

    bb66cc935b8632eef8fec4a70e205e2fb5b02fd4

Corrected governed runner blob:

    3b262b06f387322dd04e0326836a40de32c41982

## Correction

The previous runner incorrectly pinned the P5-D3G contract branch in its BRANCH constant.

That caused its internal fetch/FETCH_HEAD race guard to observe the contract branch rather than the implementation branch.

The runner now pins exactly:

    feat/obsidian-projection-p5d3g-live-publication-transaction-implementation-v0.1

No implementation behavior or test expectation changed.

## Qualification gate

The governed runner must now pass targeted P5-D3G tests, the complete historical Obsidian suite, and the final clean-control-clone check.

The real Vault remains closed.
