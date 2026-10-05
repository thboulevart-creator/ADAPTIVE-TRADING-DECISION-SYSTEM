# AO-E0-EXEC-02 — REAL COST PROFILE EVIDENCE BINDING — V0.3

## Current target and current contract are now bound

BROKER =
VT Markets

SERVER =
VTMarkets-Live 2

ACCOUNT TYPE =
Standard STP

ACCOUNT BASE CURRENCY =
EUR

SYMBOL =
NAS100.s

PRODUCT =
NAS100 Cash

CURRENT CONTRACT SPECIFICATION =
PASS_CURRENT_ONLY

## Local MT5 evidence

Three current MT5 Specification screenshots were supplied and hash-bound.

SCREENSHOT 1 SHA256 =
eeeb29d7ddc0e88f4d57e371ea67b26709ebf51d0d089db6733a2e37cc25d9e

SCREENSHOT 2 SHA256 =
f39b9586e6200792d1fefff504313571f9bd4257d1c68bebc6841c1f10a8f5f5

SCREENSHOT 3 SHA256 =
7d876f8d96fcf8aa5c1d8cf6b4b82e2557f4cb0f8283339e1cb3084bc81168af

Current observed values include:

DIGITS = 2
CONTRACT_SIZE = 1
MARGIN_CURRENCY = USD
PROFIT_CURRENCY = USD
CALCULATION = CFD
TICK_SIZE = 0.01
TICK_VALUE = 0.01
EXECUTION = MARKET
MIN_VOLUME = 0.1
MAX_VOLUME = 125
VOLUME_STEP = 0.1
SWAP_TYPE = USD
SWAP_LONG = -6.3665
SWAP_SHORT = 1.2017
FRIDAY_SWAP_MULTIPLIER = 3

Truncated margin-rate UI values are deliberately not bound.

## Exact current unit conversion

Because current tick size is 0.01 and current tick value is 0.01 USD per lot:

1.00 INDEX PRICE UNIT
=
1.00 USD PER LOT

under the current NAS100.s contract specification.

Therefore current swap values can be represented in AO-E0 normalized price units:

LONG standard rollover cost =
+6.3665 price units per lot

SHORT standard rollover cost =
-1.2017 price units per lot
(credit under positive-cost convention)

Friday:

LONG =
+19.0995 price units per lot

SHORT =
-3.6051 price units per lot

The account base currency EUR does not require EUR conversion for the normalized AO-E0 PRICE_UNITS_PER_UNIT_POSITION estimand.

An account-currency EUR PnL claim would require a separate USD/EUR conversion rule.

## Commission

Official VT Markets Standard STP documentation supports zero separate commission.

This remains a strong account-structure anchor.

Strict full-OOS version continuity is not yet independently proven for every instant of the frozen OOS.

## Financing / swap

Current NAS100.s swap mechanics and values are now exactly observed.

But VT Markets states swap rates can change, and current MetaTrader values do not reconstruct the historical series.

Therefore:

CURRENT_SWAP_PROFILE =
BOUND

HISTORICAL_OOS_SWAP_PROFILE =
UNKNOWN

The current -6.3665 / +1.2017 values MUST NOT be projected backward over 2025-05-25 → 2026-05-24.

## Slippage

The current contract uses MARKET execution.

Official market-execution semantics allow execution at an available price different from the requested price.

No finite adverse slippage upper bound has been established.

Therefore:

SLIPPAGE =
UNKNOWN

SLIPPAGE_UPPER_BOUND =
UNKNOWN

## Real cost profile verdict

REAL_COST_PROFILE =
BLOCKED

CURRENT_CONTRACT_BINDING =
PASS_CURRENT_ONLY

HISTORICAL_OOS_FINANCING =
BLOCKED_BY_MISSING_EXTERNAL_EVIDENCE

SLIPPAGE_BOUND =
BLOCKED_BY_MISSING_EXTERNAL_EVIDENCE_OR_FUTURE_GOVERNED_EXECUTION_POLICY

OOS_CONSUMPTION =
NOT_AUTHORIZED

REAL_PERFORMANCE_OBSERVATION =
NOT_AUTHORIZED

B12 =
CLOSED

## Next frontier inside EXEC-02

The remaining problem is no longer target identity or current symbol specification.

It is historical/economic evidence:

1. historical NAS100.s swap/specification evidence covering the OOS, or a defensible pre-result financing bound;
2. a defensible adverse slippage upper bound, based on admissible execution evidence or a separately governed bounded-execution policy;
3. if strict version continuity is required, evidence that zero separate Standard STP commission and the relevant contract specification remained applicable across the full OOS.

No MOMENTUM_V1 performance is needed or authorized for any of these tasks.

STOP = AO-E0-EXEC-02 CURRENT CONTRACT BOUND — HISTORICAL FINANCING + SLIPPAGE BOUND REMAIN BLOCKED
