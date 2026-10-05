# AO-E0-EXEC-02 — REAL COST PROFILE EVIDENCE BINDING — V0.2

## Human target identity now bound

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

The previous target-identity blocker is therefore CLOSED.

No account number, login or secret is part of the governed identity.

## What official evidence now establishes

VT Markets' dated Standard STP FAQ published 2025-04-22, before the frozen OOS start, describes Standard STP as commission-free. Current Standard STP documentation also states commission $0.

This supports a strong zero-separate-commission account-structure anchor.

However:

CURRENT / DATED ANCHOR != VERSIONED CONTINUOUS HISTORICAL SCHEDULE

Therefore full-OOS commission continuity is not silently promoted to PASS.

VT Markets' NAS100 Cash documentation establishes that the product is a cash-index CFD with overnight swap and directs users to MetaTrader for exact contract specifications.

VT Markets' swap guidance establishes:
- cash-index rollover at server time 00:00;
- Friday-to-Monday triple swap for cash indices;
- exact latest long/short swap values must be obtained from product Specifications in MetaTrader.

VT Markets' execution/slippage policy establishes that market execution may fill at another available price and publishes no numeric maximum adverse slippage bound.

## Current binding matrix

EXECUTION_VENUE_IDENTITY =
VT_MARKETS

MT5_SERVER_IDENTITY =
VTMarkets-Live 2

ACCOUNT_COST_PROFILE_IDENTITY =
VT_MARKETS_STANDARD_STP

USTECH_SYMBOL_CONTRACT_IDENTITY =
VT_MARKETS_MT5_NAS100.s_NAS100_CASH

COMMISSION =
ZERO-SEPARATE-COMMISSION SUPPORTED AT OFFICIAL DOCUMENTED ANCHORS
FULL-OOS CONTINUITY = NOT_YET_VERSION-PROVEN

SLIPPAGE =
UNKNOWN / NO PUBLISHED DEFENSIBLE UPPER BOUND

FINANCING / SWAP =
UNKNOWN / EXACT CURRENT VALUES AND HISTORICAL OOS SERIES NOT BOUND

UNIT CONVERSION =
UNKNOWN PENDING EXACT MT5 SYMBOL SPECIFICATION + ACCOUNT BASE CURRENCY

REAL_COST_PROFILE =
BLOCKED

## Next local evidence required

From MT5 on server VTMarkets-Live 2, Standard STP, open:

Market Watch
→ NAS100.s
→ Specification

Capture the exact specification surface, including where shown:
- contract size;
- digits;
- tick size;
- tick value;
- minimum volume;
- volume step;
- calculation mode;
- swap type;
- swap long;
- swap short;
- triple-swap day;
- profit/trading currency.

Also provide only the account base currency (for example EUR or USD).

Do NOT provide:
- account number;
- password;
- login;
- investor password;
- API key;
- any secret.

## Important limitation

The MT5 specification will bind the current NAS100.s contract mechanics and current swap state.

It will NOT, by itself, prove the complete historical swap schedule from:

2025-05-25T00:00:00Z
→
2026-05-24T23:59:59.963Z

Historical swap continuity and a defensible slippage upper bound remain independent evidence problems.

## Fail-closed status

PRIOR_BLOCKER =
BLOCKED_BY_HUMAN_DECISION

PRIOR_BLOCKER_STATUS =
CLOSED_BY_HUMAN_TARGET_IDENTITY

CURRENT_BLOCKERS =
LOCAL_USER_ACTION_REQUIRED
+
BLOCKED_BY_MISSING_EXTERNAL_EVIDENCE

OOS_CONSUMPTION =
NOT_AUTHORIZED

REAL_PERFORMANCE_OBSERVATION =
NOT_AUTHORIZED

B12 =
CLOSED

STOP = AO-E0-EXEC-02 TARGET IDENTITY BOUND — CURRENT SYMBOL SPECIFICATION REQUIRED
