# OBSIDIAN P5-D3G — IMPLEMENTATION QUALIFICATION TARGET V3

Date: 2026-09-29

## Evidence status

Static qualification target only.

No full local P5-D3G implementation qualification is claimed here.

## Exact corrected functional candidate

    f725854a7539d1a3b589ca2e49d45c22f6699d3d

Implementation blob:

    b8875f8973ddf1076ff20d8e725ce04abbb814a8

Implementation tests blob:

    bb66cc935b8632eef8fec4a70e205e2fb5b02fd4

Governed runner blob:

    94d2a08cce581244c64945e7a50de76cbe13900b

Frozen contract blob:

    64997ddd9977229961387f66af4de356c045c0ac

## Closed representative blocker

The isolated publication-plan test now passes on USER-REPORTED LOCAL EXECUTION:

    test_planning_is_read_only ... ok
    Ran 1 test in 3.126s
    OK

## Qualification gate

The governed implementation runner must now pass:

1. exact implementation-branch remote race guard;
2. exact corrected implementation candidate checkout;
3. exact blob pins;
4. Python compilation;
5. targeted P5-D3G contract + implementation tests;
6. complete historical tests/obsidian_projection suite;
7. final clean-control-clone check.

Any FAIL / ERROR / BLOCKED result keeps the implementation unqualified.

The real Vault remains closed.
