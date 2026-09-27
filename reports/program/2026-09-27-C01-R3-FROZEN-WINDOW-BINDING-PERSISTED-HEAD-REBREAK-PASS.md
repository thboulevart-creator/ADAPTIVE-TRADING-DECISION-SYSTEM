# C01-R3 — FROZEN WINDOW BINDING — PERSISTED-HEAD RE-BREAK PASS

Date: 2026-09-27

Reviewed persisted governed HEAD:

`a2f70840fb9adfae02078de810dbe4d965787e1e`

Runtime blob:

`7ea6ed6796eae8618cfd823b49eee1a63a19e096`

Breaker blob:

`cf275dba96e50e8b899223a57267e811af4693ec`

Adversarial workflow run:

`36321372742`

## Finding under re-break

Previously confirmed finding:

`FROZEN_WINDOW_BINDING_FAILS_OPEN`

Correction scope:

- exact `eligible_start_utc = 2026-05-25T00:00:00Z`;
- exact `fixed_end_utc = 2027-05-24T23:59:59Z`;
- exact `earliest_primary_evaluation_utc = 2027-05-25T00:00:00Z`;
- dedicated falsification breakers for all three bindings.

## Structural verification

PASS:

- exact governed HEAD checkout;
- correction commit scope exactly limited to runtime, breaker, correction report and checkpoint;
- runtime blob exact;
- breaker blob exact;
- Charter blob unchanged:
  `ada0ebf41ecd7ab406d2656ac745ed7003d5b5c1`;
- confirmation execution contract blob unchanged:
  `f6823cfa7b3c582524b3d512d45b16fdc0450ee8`;
- frozen model blob unchanged:
  `68ee4795462c5dbd5747a7bfdef81716dc84227f`;
- seal-candidate blob unchanged:
  `3a6897a63ef2f07a26429342b45977767090651e`;
- final-seal blob unchanged:
  `d54ec7840a7bf4eecd94a72f753a02418ea8f543`.

## Executed verification

PASS:

- `py_compile`;
- historical qualified harness: `33/33 PASS`;
- C01-R3 frozen-window breakers: `3/3 PASS`;
- full runner harness: `36/36 PASS`.

The three R3 breaker tests independently attack:

- wrong value;
- missing value;
- malformed boolean value;

for each frozen temporal binding.

## Closed finding

`FROZEN_WINDOW_BINDING_FAILS_OPEN = CLOSED`

The runtime now fails closed if any frozen window identity is absent, malformed or different from the governed temporal contract.

## Authorization boundary

This PASS qualifies only the synthetic confirmation-runner boundary.

Allowed runtime class:

`SYNTHETIC_ONLY`

Still not authorized:

- confirmation-window outcome access;
- real confirmation execution;
- primary scientific confirmation scoring;
- partial-window scoring;
- early score exposure;
- model/parameter refit;
- threshold/bin search;
- probability refit;
- feature or interaction redesign;
- C02 redesign;
- strategy/signals/trades/PnL;
- MT5 execution.

## Scientific state

Confirmation data accessed:

`false`

Primary confirmation score computed:

`false`

Real confirmation execution:

`false`

Scientific confirmation:

`NOT_YET_PERFORMED`

## Verdict

`C01_R3_FRESH_PERSISTED_HEAD_ADVERSARIAL_REBREAK = PASS`

`FROZEN_WINDOW_BINDING_FAILS_OPEN = CLOSED`

Runtime implementation qualification:

`PASS — SYNTHETIC_ONLY`

This PASS supersedes the V0.3 runtime FAIL for the specific frozen-window binding finding. Historical FAIL/PASS artifacts remain preserved as audit history.
