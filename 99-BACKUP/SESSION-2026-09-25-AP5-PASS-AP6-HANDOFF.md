# SESSION BACKUP — AP5 PASS → AP6 HANDOFF — 2026-09-25

Repo : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branche de gouvernance : `integration/system-v1`.

## AP5 status

**PASS — MICROSTRUCTURE PRICE-CORE.**

Evidence exacte :
- path : `reports/program/evidence/2026-09-25-AP5-MICROSTRUCTURE-PRICE-CORE.json` ;
- SHA-256 : `21dc09b082e32f20543c6206c276c24389b7b61fd930fbe2d1783adabaca4406` ;
- size : 39 460 bytes ;
- schema : `ATDS_AP5_MICROSTRUCTURE_PRICE_CORE_V0_1` ;
- status : `AP5_COMPLETE`.

Coverage :
- 1709180 minutes ;
- 376003618 source ticks ;
- 1606 segments ;
- 61 AP0 files rehashed.

R4 provenance :
- canonical helper SHA-256 `fdb929f54d5c816cd12fb03130545b3714a38cb2261d3b23433fb1cd4b0f7671`;
- canonical AP4 SHA-256 `c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad`;
- py_compile PASS ;
- AP5_COMPLETE / exit 0.

Prior attempts :
- R1/R2 blocked on AP4 CRLF normalization ;
- R3 AP5_COMPLETE but rejected for non-canonical helper provenance ;
- R4 first qualified run.

## Key descriptive findings

- global spread tick-weighted mean: 2.1395040593705206;
- NY cash-clock proxy spread: 1.3266027854102884;
- NY outside cash-clock spread: 2.961567212934232;
- spread↔range Pearson: -0.3408104857682299;
- spread↔tick density Pearson: -0.5910554340229595.

No edge/causality/strategy claim.

## Next governed frontier

AP6 — Seasonality / stability.

Protocol requires comparison by hour, weekday, month, year, sub-periods and distribution stability.
Every observed pattern must carry a temporal stability measure.

CORE prohibitions remain active:
no PnL, strategy, Sharpe/PF, parameter sweep, MT5, performance-oriented regime selection.
