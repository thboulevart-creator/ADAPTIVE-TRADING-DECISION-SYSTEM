# ATDS — E1 PRE-IMPLEMENTATION FREEZE PACKAGE V0

Date: 2026-09-28

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch at adoption/pre-persistence: `integration/system-v1`  
Pre-persistence HEAD: `61af0d79d687f97c1344875a38d7f3f0e52caaf9`  
Pre-persistence TREE: `483eb3e6948986ba4655f6112b1142915b6ab896`

## 1. Status and authority

```text
PACKAGE = ATDS_E1_PRE_IMPLEMENTATION_FREEZE_PACKAGE_V0
HUMAN_ADOPTION = CONFIRMED
MODE = DOCUMENTARY_FREEZE
REAL_E1_RUN_AUTHORIZED = FALSE
E1_03_IMPLEMENTATION_AUTHORIZED_BY_THIS_FILE = FALSE
```

This package persists the human-adopted Phase 18 decisions for E1-01, E1-02 and E1-04.

It does not execute E1, does not qualify Momentum V1, does not confirm an edge, and does not authorize paper, broker, MT5, live or capital use.

A persisted-head read-only verification is required after this package is committed before E1-01, E1-02 or E1-04 may be adjudicated PASS.

---

## 2. E1-01 — E1_SCOPE_FREEZE_V0

Experiment identity:

```text
experiment_id = ATDS_E1_MOMENTUM_V1_SOURCE_B_EXPLORATORY_N0_V0
strategy_id = MOMENTUM_V1
data_source_id = SOURCE_B_USTECH_PRICE_CORE_V0_1
mode = OFFLINE
class = EXPLORATORY
research_level = N0
```

Frozen strategy semantics:

```text
timeframe = H1
signal_price = H1 MID CLOSE
lookback = 20 completed admissible H1 bars

M_t = Close_t / Close_t-20 - 1

M_t > 0  -> LONG
M_t < 0  -> SHORT
M_t = 0  -> NEUTRAL
insufficient admissible history -> UNDEFINED

signal may be calculated only after H1 bar t closes
same-bar execution is forbidden
earliest execution is t+1 under E1-04
```

Frozen exclusions:

```text
NO parameter optimization
NO regime filter
NO discretionary override
NO pyramiding
NO stop-loss
NO take-profit
NO trailing stop
NO break-even
NO position-sizing optimization
```

Normalized research exposure:

```text
LONG = +1
SHORT = -1
NEUTRAL = 0
```

Allowed claim class:

```text
exploratory behavior under the declared E1 model
```

Forbidden claims include:

```text
STRATEGY_QUALIFIED
EDGE_CONFIRMED
ROBUST
LIVE_PROFITABLE
BROKER_REALISTIC_NET_PNL
ALL_COSTS_INCLUDED
FIVE_CALENDAR_YEAR_QUALIFICATION
CONFIRMATORY_RESULT
DECISION_AUTHORITY
ACTION_AUTHORITY
MT5_AUTHORIZED
PAPER_AUTHORIZED
BROKER_AUTHORIZED
LIVE_AUTHORIZED
CAPITAL_AUTHORIZED
```

The Source-B span is not represented as a full five-calendar-year qualification.

---

## 3. E1-02 — E1_WINDOW_FREEZE_V0

Raw DatasetIdentity:

```text
SOURCE_B_USTECH_PRICE_CORE_V0_1
```

Frozen complete raw Source-B outer window:

```text
raw_window_start = 2021-05-25T00:00:00.309Z
raw_window_end   = 2026-05-24T23:59:59.963Z
```

Frozen temporal split:

```text
PRE_OOS:
timestamp < 2025-05-25T00:00:00Z

OOS:
timestamp >= 2025-05-25T00:00:00Z
AND
timestamp <= 2026-05-24T23:59:59.963Z
```

The OOS boundary is frozen before any Momentum V1 performance result is observed.

It must not be moved because of PnL, drawdown, trade count, calendar-period performance, regime behavior or any other observed Momentum result.

E1-03 may derive the first and last admissible H1 bars and exact H1 row counts from these raw bounds, but it may not silently change the frozen raw outer window or OOS boundary.

If this OOS is observed and the model is subsequently modified using information from it, that observed period must not later be represented as untouched independent confirmatory evidence.

---

## 4. E1-04 — E1_EXECUTION_COST_MODEL_V0

Signal/execution separation:

```text
H1 MID-derived bars -> signal generation only
RAW SOURCE-B BID/ASK -> execution pricing
MID_IS_EXECUTION_PRICE = FALSE
```

Execution side:

```text
LONG entry = ASK
LONG exit  = BID

SHORT entry = BID
SHORT exit  = ASK
```

Timing:

```text
1. H1 bar t completes.
2. Momentum is computed using information through t only.
3. The signal is frozen.
4. No event inside t may execute that signal.
5. Execution search starts at t+1.
6. The first admissible raw Source-B tick is the execution candidate.
```

Gap semantics:

```text
NO fabricated execution price
NO forward fill
NO last-price carry
NO MID substitution
NO silent traversal of a forbidden continuity boundary
```

If no admissible execution price exists under the later E1-03 continuity rules:

```text
SIGNAL_EXECUTION = NOT_EXECUTED
```

Position transitions:

```text
FLAT  -> LONG    : buy +1 at ASK
FLAT  -> SHORT   : sell -1 at BID
LONG  -> NEUTRAL : close at BID
SHORT -> NEUTRAL : close at ASK
LONG  -> SHORT   : close long at BID and open short at BID
SHORT -> LONG    : close short at ASK and open long at ASK
LONG  -> LONG    : HOLD
SHORT -> SHORT   : HOLD
```

No pyramiding is permitted.

### Cost scope

Historical Source-B spread is included intrinsically through raw bid/ask execution.

```text
SPREAD_INCLUDED = TRUE
COMMISSION_INCLUDED = FALSE
SLIPPAGE_INCLUDED = FALSE
FINANCING_INCLUDED = FALSE
```

Commission, slippage and financing are not assumed to be zero. They are explicitly excluded because no exact applicable values/model are established for this E1.

Therefore E1 must not claim:

```text
BROKER_NET_PNL
ALL_IN_COST_PROFITABILITY
LIVE_PROFITABILITY
FULL_BROKER_EXECUTION_REALISM
```

Any PnL-like result must be labelled as being under the declared E1 execution model and after observed Source-B bid/ask spread only.

---

## 5. Critical-path authority bridge

The previously recorded A0 V0.3 coverage-gap work remains true and open:

```text
A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET
```

The coverage review did not establish a runtime defect. The remaining A0 V0.3 coverage-gap expansion is therefore deferred post-E1 under the later human critical-path adjudication.

This deferral:

- does not turn A0 V0.3 into PASS;
- does not delete its remaining proof gaps;
- does not weaken existing A0 evidence;
- does not authorize A1, A2, DecisionPolicy, Decision, ACTION, trading, MT5, paper, broker, live or capital use.

The active E1 readiness path is limited to the adopted E1-01 through E1-08 controls.

---

## 6. Next governed boundary after persisted-head verification

After this package and the checkpoint bridge are committed and freshly re-read from the resulting HEAD:

```text
NEXT TECHNICAL BOUNDARY =
E1-03 — EXACT GAP-AWARE H1 DATASET IDENTITY
```

No E1 run is authorized.

No E1-05 runner implementation is authorized before E1-03 is closed under its own governed boundary.
