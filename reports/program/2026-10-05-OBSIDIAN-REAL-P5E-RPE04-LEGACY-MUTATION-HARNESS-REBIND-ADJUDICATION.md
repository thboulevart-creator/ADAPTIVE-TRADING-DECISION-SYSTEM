# RPE-04 — LEGACY MUTATION HARNESS REBIND — INTERNAL ADJUDICATION

Date: 2026-10-05

A complete RPE-04 regression after the authorized RPE-03 V0.2 rebind + NF-2 + NF-3 patch produced 3 failures, all from mutation source anchors that no longer matched the authorized implementation shape.

No functional assertion failed.

The three harness-only corrections are:

1. MATERIALIZATION MUTANT
Historical anchor:
if not _materialized_commit(observed_head)

Authorized new anchor:
the exact-object-type block using _materialized_object_type(observed_head), including both NOT_MATERIALIZED and EXACT_OBSERVED_REF_NOT_COMMIT failure branches.

The mutant still removes materialization/type proof and preserves the same expected failure mode.

2. UNKNOWN-LAUNDERING MUTANT
Historical RPE-03 V0.1 call anchor had three classifier arguments.

Authorized new anchor:
the exact RPE-03 V0.2 call including the fourth governed executable argument str(_GIT).

The mutant still replaces the classifier result with FAST_FORWARD and preserves the same expected failure mode.

3. PHYSICAL-ESCAPE MUTANT
Historical containment implementation used a prior inline path-parent branch.

Authorized new anchor:
the current _inside_root(path, root) helper.

The mutant makes _inside_root return True unconditionally and preserves the same physical-escape failure mode.

These are test-harness rebinds to the already-authorized implementation delta. They do not change:
- implementation code;
- expected security verdicts;
- claim scope;
- authority;
- RPE-05/RPE-06/REAL P5-E state.

The prior 3 failures are therefore classified as HARNESS_ANCHOR_STALE, pending GREEN replay.
