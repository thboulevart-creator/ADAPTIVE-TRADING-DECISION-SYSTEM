# A0 — AF04 METRIC-DOMAIN GOVERNED RE-ADJUDICATION — PASS

Date: 2026-09-27

Reviewed governed HEAD:

`be950b4b0e7c6d7ca658a887955e51b61feaeebd`

Runtime blob:

`1210bee06a2d9aed2ed7d9078542934ff430175c`

Standalone qualifier blob:

`9bd05f2a2a97f092c0fc2988319f15caff57dda3`

Frozen metric-domain authority blob:

`dd205d3e7b4a522a5ba23cef1e665d51c196acb8`

Historical V0.5 candidate breaker blob containing AF04:

`f02eae836b79403673f8a43292cca19eab0c6b33`

AF04 sandbox restoration commit:

`1637edaf9e80b297a3936323c1db7bd65f5ee0c6`

Re-adjudication run:

`36343999416`

## Scope

This boundary executed AF04 separately from all other V0.5 tests.

The exact historical AF04 oracle was reused unchanged:

- start from the admitted rich synthetic fixture;
- replace the source-native measurement metric with `FOREIGN_METRIC`;
- require `NO AUTHORITATIVE OUTPUT`.

No runtime mutation was made before or during classification.

## Frozen-surface preservation

Before AF04 execution:

`127/127 PASS`

Therefore the currently qualified A0 + metric-domain surfaces remained unchanged.

## AF04 observed result

AF04:

`1/1 PASS`

Observed governed classification:

`PASS`

The current qualified runtime rejects the source-native metric identity `FOREIGN_METRIC` under the frozen producer-specific metric-domain authority.

Therefore:

`AF04_IMPLEMENTATION_FAIL = FALSE`

`AF04_ORACLE = GOVERNED_AND_RESOLVED`

`AF04_METRIC_DOMAIN_GOVERNED_READJUDICATION = PASS`

No ABF5 runtime correction is required for AF04.

## Qualification ceiling

This result does NOT by itself qualify the full historical V0.5 breaker against the current runtime.

The other 21 V0.5 cases previously passed on an earlier runtime state but have not yet been replayed against the current qualified runtime.

Therefore:

`A0_ADVERSARIAL_BREAK_EXPANSION_V0_5_FULL_CURRENT_HEAD_QUALIFICATION = NOT_YET`

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

## Next governed boundary

`A0 — ADVERSARIAL BREAK EXPANSION V0.5 GOVERNED REPLAY`

That boundary must:

- preserve all 127 current tests unchanged;
- restore/persist the exact historical V0.5 breaker bytes unchanged;
- execute all 22 V0.5 tests against the current governed runtime;
- perform a fresh persisted-head replay before any full V0.5 qualification claim;
- make no runtime correction unless a current-head V0.5 failure is first established;
- keep A1/A2/DecisionPolicy/Decision/ACTION/trading/MT5/real-C01 closed.
