# OBSIDIAN P5-D3F — PERSISTENT PRODUCTION HANDOFF IMPLEMENTATION QUALIFICATION TARGET V2

Date: 2026-09-29

## Correction reason

The V1 qualification target named functional commit:

    b6129fd735186fa0a68d0862b3326308f1ba3d25

That commit contains the implementation and frozen tests but predates the governed re-break runner.

The governed runner is designed to detach to --expected-candidate-head and re-exec itself. Therefore b6129fd... is not a self-contained executable qualification candidate: after checkout the runner path is absent and re-exec fails with ENOENT.

This is a qualification-target packaging defect, not an implementation failure.

## Corrected exact qualification candidate

    7873f955d3c7888fe6a88bd27d176ca86bd65b84

This commit contains, unchanged:

Implementation blob:

    d2f40c8b2c8fb06b37bb34442c59d78222046452

Frozen tests blob:

    7da1fadeb1b3e9efee54b7ca09f0735277af345c

Governed runner blob:

    65016ec10d2ad9b2ddf4ce5c9a359fc035a323ef

Qualified persistent gate contract blob:

    59ce9e079d256799d072405fa4a623ba58b75c0d

Qualified P5-D3F runtime blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

## Authority effect

No implementation semantic changed.

No test expectation changed.

No persistent staging creation is authorized.

No real Vault access is authorized.

No real Vault write is authorized.

The only correction is that the exact qualification candidate now includes its own governed runner so checkout + re-exec is self-contained.

## Required synthetic re-break

The corrected governed invocation must use:

    --expected-candidate-head 7873f955d3c7888fe6a88bd27d176ca86bd65b84

The branch remote HEAD must be freshly pinned at execution time.

Only a complete targeted + historical-suite + clean-clone PASS may qualify the implementation synthetically.
