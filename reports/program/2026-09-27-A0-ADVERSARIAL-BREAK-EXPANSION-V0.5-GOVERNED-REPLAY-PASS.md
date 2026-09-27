# A0 — ADVERSARIAL BREAK EXPANSION V0.5 — GOVERNED REPLAY PASS

Date: 2026-09-27

Reviewed governed HEAD:

`b8c538aabc2793ecc6d2ba57725a8919135a3335`

Runtime blob:

`1210bee06a2d9aed2ed7d9078542934ff430175c`

Standalone metric-domain qualifier blob:

`9bd05f2a2a97f092c0fc2988319f15caff57dda3`

Frozen metric-domain authority blob:

`dd205d3e7b4a522a5ba23cef1e665d51c196acb8`

Exact restored V0.5 breaker blob:

`f02eae836b79403673f8a43292cca19eab0c6b33`

V0.5 governed restoration commit:

`b8c538aabc2793ecc6d2ba57725a8919135a3335`

Governed replay run:

`36344507144`

## Governed restoration

The historical V0.5 breaker bytes were restored unchanged from the original sandbox source.

The restored governed breaker contains 22 tests AF01..AF22.

No runtime file was modified by the restoration.

## Replay gates

Existing qualified surface:

`127/127 PASS`

Complete V0.5 breaker:

`22/22 PASS`

Combined current-head surface:

`149/149 PASS`

Therefore:

```
A0_EXISTING_127 = PASS_UNCHANGED
A0_V05_GOVERNED_REPLAY = PASS_22_OF_22
A0_CURRENT_HEAD_COMBINED_SURFACE = PASS_149_OF_149
```

## V0.5 qualification

All 22 historical V0.5 cases now pass against the current governed runtime, including AF04 under the now-qualified source-specific metric-domain authority and runtime binding.

Therefore:

`A0_ADVERSARIAL_BREAK_EXPANSION_V0_5 = PASS_CURRENT_HEAD`

`A0_ADVERSARIAL_BREAK_EXPANSION_V0_5_GOVERNED_REPLAY = PASS_22_OF_22`

`A0_V0_5_CURRENT_HEAD_QUALIFICATION = PASS`

No current-head V0.5 implementation failure is established.

No V0.5 runtime correction is authorized or required.

## Qualification ceiling

This replay closes V0.5 at the current governed HEAD.

It does NOT by itself establish full A0 V0.3 implementation qualification.

A separate coverage closure review is required to map every mandatory V0.3 mutation family and invariant to persisted qualified evidence and identify any remaining untested or under-tested requirement.

Therefore:

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

## Next governed boundary

`A0 — V0.3 COVERAGE CLOSURE REVIEW`

That boundary must be documentary/read-only with respect to runtime first.

It must:

1. enumerate the mandatory V0.3 adversarial families and qualification conditions;
2. map each to exact persisted tests/reports/blobs;
3. identify any uncovered or insufficiently evidenced requirement without inventing new requirements;
4. verify the current combined 149-test surface remains unchanged;
5. decide only whether the evidence is sufficient to open a final V0.3 implementation qualification boundary.

No runtime correction may be made inside the review itself.

No A1/A2/DecisionPolicy/Decision/ACTION/trading/MT5/real-C01 authority is opened.
