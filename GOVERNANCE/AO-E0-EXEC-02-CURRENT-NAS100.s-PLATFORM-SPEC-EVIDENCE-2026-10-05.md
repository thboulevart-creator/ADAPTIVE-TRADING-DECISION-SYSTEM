# AO-E0-EXEC-02 — CURRENT NAS100.s PLATFORM SPECIFICATION EVIDENCE

Observed date: 2026-10-05

Human-bound execution target:

EXECUTION_VENUE / BROKER =
VT Markets

MT5 SERVER =
VTMarkets-Live 2

ACCOUNT TYPE / COST PROFILE =
Standard STP

EXACT TRADABLE SYMBOL =
NAS100.s

BROKER PRODUCT DESCRIPTION =
NAS100 Cash

ACCOUNT BASE CURRENCY =
EUR

## Screenshot evidence identities

SCREENSHOT_1_SHA256 =
eeeb29d7ddc0e88f4d57e371ea67b26709ebf51d0d089db6733a2e37cc25d9e

SCREENSHOT_2_SHA256 =
f39b9586e6200792d1fefff504313571f9bd4257d1c68bebc6841c1f10a8f5f5

SCREENSHOT_3_SHA256 =
7d876f8d96fcf8aa5c1d8cf6b4b82e2557f4cb0f8283339e1cb3084bc81168af

## Exact current values visible in MT5 Specification

SYMBOL =
NAS100.s

DESCRIPTION =
NAS100 Cash

DIGITS =
2

CONTRACT_SIZE =
1

SPREAD =
FLOATING

STOPS_LEVEL =
0

MARGIN_CURRENCY =
USD

PROFIT_CURRENCY =
USD

CALCULATION_MODE =
CFD

TICK_SIZE =
0.01

TICK_VALUE =
0.01

CHART_MODE =
BID

TRADE_MODE =
FULL_ACCESS

EXECUTION_MODE =
MARKET

GTC_MODE =
VALID_UNTIL_CANCELLED

FILLING_MODE =
IMMEDIATE_OR_CANCEL

EXPIRATION =
ALL

ORDERS =
ALL

MIN_VOLUME_LOTS =
0.1

MAX_VOLUME_LOTS =
125

VOLUME_STEP_LOTS =
0.1

SWAP_TYPE_DISPLAY =
USD

SWAP_LONG =
-6.3665

SWAP_SHORT =
1.2017

SWAP_MULTIPLIER_MONDAY =
1

SWAP_MULTIPLIER_TUESDAY =
1

SWAP_MULTIPLIER_WEDNESDAY =
1

SWAP_MULTIPLIER_THURSDAY =
1

SWAP_MULTIPLIER_FRIDAY =
3

CURRENT_WEEKDAY_TRADE_SESSION_VISIBLE =
01:00-24:00

## Values intentionally NOT bound from truncated UI

The margin-rate rows show truncated values in the screenshot. They are NOT promoted into exact evidence.

## Current unit conversion

From the current symbol specification:

TICK_SIZE = 0.01 index price units
TICK_VALUE = 0.01 USD per 1.0 lot
CONTRACT_SIZE = 1

Therefore, for one lot:

1.00 index price unit movement = 1.00 USD of symbol PnL.

This is a CURRENT CONTRACT conversion identity only.

The AO-E0 normalized price-unit estimand can convert current USD-denominated swap values into index-price units per lot by the exact 1 USD = 1 price-unit-per-lot relation under this current specification.

ACCOUNT_BASE_CURRENCY = EUR does not require EUR conversion for the AO-E0 normalized PRICE_UNITS_PER_UNIT_POSITION estimand itself.

An account-currency EUR PnL claim would require a separate USD/EUR conversion rule.

## Current swap conversion

Under the current specification only:

LONG standard rollover:
-6.3665 USD per lot
=
6.3665 price units of COST per lot

SHORT standard rollover:
+1.2017 USD per lot
=
-1.2017 price units of COST per lot
(credit under positive-cost convention)

Friday multiplier = 3:

LONG Friday rollover cost =
19.0995 price units per lot

SHORT Friday rollover cost =
-3.6051 price units per lot

These are CURRENT observed contract values, not historical OOS values.

## Firewall

CURRENT MT5 SPECIFICATION
!=
HISTORICAL OOS SPECIFICATION

CURRENT SWAP RATE
!=
HISTORICAL SWAP SERIES

MARKET EXECUTION
!=
FINITE SLIPPAGE UPPER BOUND

SOURCE_B PRICE FEED
!=
VT MARKETS EXECUTION FEED

OOS_CONSUMPTION =
NOT_AUTHORIZED

REAL_PERFORMANCE_OBSERVATION =
NOT_AUTHORIZED

B12 =
CLOSED
