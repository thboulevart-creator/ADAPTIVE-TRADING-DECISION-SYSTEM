# AP1 — adjudication exacte

Date : 2026-09-25

## Preuve
- JSON exact : 179955 octets
- SHA-256 : db8963bb1bd1fa5b76a9a435fcb9b2d24781f92df0c5e53b6664bafe6235076b
- schema : ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1
- status : AP1_COMPLETE
- input : USTECH_PROFILE_MINUTE_CORE_V0_1
- AP0 manifest SHA-256 : 62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce
- AP0 files rehashed : 61

## Couverture
- minutes : 1709180
- source ticks : 376003618
- segment starts : 1606
- 24 UTC hours
- 24 New York hours
- 7 New York weekdays
- 168 New York weekday-hours
- 6 UTC years

Chaque dimension recompte exactement 1709180 minutes, 376003618 ticks et 1606 segment-starts.

## Global
- minute range mean : 6.8231403696509565
- minute range p50/p90/p95/p99 : 4.740000000001601 / 14.248999999998158 / 19.23399999999674 / 33.311210000001516
- tick count mean : 219.99064931721645
- tick count p50/p90/p99 : 184 / 443 / 621
- spread min/max : 0.000999999996565748 / 35.66699999999764
- spread tick-weighted mean : 2.1395040593705206

AP1 reconstruit le spread moyen F2 2.1395040593705223 avec un écart absolu d'environ 1.8e-15, bien inférieur à 1e-9.

## Portée
Le JSON confirme : strategy_agnostic=true, returns=false, signals=false, pnl=false, source_volume=false, optimization=false.

## Verdict
**PASS — AP1 INTRADAY + SPREAD CENSUS qualifié.**

AP2 Volatility Map peut être ouvert.
