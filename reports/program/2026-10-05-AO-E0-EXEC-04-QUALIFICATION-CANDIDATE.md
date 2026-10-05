# AO-E0-EXEC-04 — PRE-RESULT CONSERVATIVE COST-STRESS POLICY — QUALIFICATION CANDIDATE

## Status

CANDIDATE =
QUALIFIED_SYNTHETICALLY / NOT_HUMAN_ADOPTED

OOS =
NOT OBSERVED

PERFORMANCE =
NOT OBSERVED

## Why EXEC-04 exists

EXEC-03 established that perfect historical financing reconstruction and a guaranteed finite slippage maximum are unavailable from accessible evidence.

EXEC-04 therefore changes the question from:

"what exactly did every historical cost equal?"

to:

"does the economic edge survive a preregistered conservative cost-stress surface?"

POLICY_STRESS != OBSERVED_HISTORICAL_COST

## Base cost treatment

SPREAD =
raw BID/ASK intrinsic, already owned by E1-04

COMMISSION =
0 separate commission under the documented Standard STP account structure

## Financing candidate grid

Current observed worst adverse standard rollover anchor:

6.3665 price units per lot

The policy deliberately applies this adverse anchor to BOTH long and short positions, so the current favorable short credit is never assumed.

Frozen candidate multipliers:

0x
1x
2x
4x

Friday rollover retains x3.

This is a policy stress anchor, not a claim that historical swaps equaled the current rate.

## Slippage candidate grid

Slippage is expressed as basis points of the reference execution price PER EXECUTION EVENT:

0
0.5
1
2
4
8
16 bps

BUY uses raw ASK as the reference price.
SELL uses raw BID as the reference price.

A reversal has two execution events, so stress is charged twice.

The grid uses Source-B prices only as the arithmetic reference price at which the policy percentage is applied.

SOURCE_B is NOT used as evidence of VT Markets slippage.

## Stress surface

4 financing nodes × 7 slippage nodes = 28 nodes.

Every node must be reported.

POST-RESULT NODE SELECTION =
FORBIDDEN

The future output is a cost-robustness surface/frontier, not one cherry-picked scenario.

## Test-first qualification

EXPECTED RED =
PASS

FROZEN BREAKER =
PASS

PYTEST =
8 / 8 PASS

Synthetic checks cover:
- no OOS/performance authority;
- frozen exact grids;
- monotone stress levels;
- direction-neutral adverse financing;
- Friday x3;
- slippage per execution event;
- double charge for reversal close+open;
- full 28-node reporting;
- no selected node in runtime;
- explicit POLICY_STRESS_NOT_OBSERVED_HISTORICAL_COST label.

## Human boundary

The exact numeric grid is a normative research-policy choice.

Therefore EXEC-04 intentionally does NOT self-adopt it.

The remaining human decision is whether to adopt exactly:

FINANCING MULTIPLIERS =
[0, 1, 2, 4]

SLIPPAGE BPS PER EXECUTION EVENT =
[0, 0.5, 1, 2, 4, 8, 16]

and the associated semantics.

The minimum robustness level required for eventual AO-E0 qualification remains a separate PRE-OOS human decision.

No performance may be observed before both policy and decision rule are frozen.

STOP =
AO-E0-EXEC-04 COST-STRESS POLICY CANDIDATE QUALIFIED — HUMAN ADOPTION REQUIRED
