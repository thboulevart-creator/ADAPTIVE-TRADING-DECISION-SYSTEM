# E0-SOURCE-B-F2 — exécution locale observée, JSON exact à ingérer

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD vérifié avant écriture : `b2ef568cf6f74bc6f7855370815694b530c56b7d`

## Sortie terminale fournie par le propriétaire

```text
F2_COMPLETE
Rows read: 376003618
Bid null: 0; Ask null: 0
Ask < Bid: 0
Nonpositive spread: 0
Spread min/max/mean: 0.000999999996565748 / 35.66699999999764 / 2.1395040593705223
Report: C:\Users\Boulevart\AppData\Local\Temp\ATDS-E0-SOURCE-B-F2-BID-ASK-QUALITY.json
```

## Adjudication bornée

Le helper F2 courant était lié au manifest exact, au F0 exact, au F1 exact et au schéma unique courant avant cette tentative.

Constats terminaux :
- statut : `F2_COMPLETE` ;
- lignes lues : **376 003 618** ;
- bid null : **0** ;
- ask null : **0** ;
- `ask < bid` : **0** ;
- spread non positif : **0** ;
- spread min : **0.000999999996565748** ;
- spread max : **35.66699999999764** ;
- spread moyen : **2.1395040593705223**.

## Verdict

**PASS — exécution locale F2 complète selon la sortie terminale fournie.**

Ce PASS ne qualifie pas encore :
- l'identité SHA-256 du JSON F2 ;
- les compteurs nonfinite/nonpositive détaillés ;
- les extrema bid/ask ;
- le détail fichier par fichier ;
- la conformité complète du budget/binding dans le JSON exact ;
- toute qualité des volumes.

## Prochaine action gouvernée unique

Rendre accessible :
`C:\Users\Boulevart\AppData\Local\Temp\ATDS-E0-SOURCE-B-F2-BID-ASK-QUALITY.json`.

Puis :
1. fresh HEAD ;
2. ingestion intégrale du JSON F2 exact ;
3. adjudication bid/ask ;
4. synthèse Source-B Data Truth ;
5. déterminer si la base DATA TRUTH peut être clôturée avec limites explicites ou si un dernier contrôle minimal est requis.

Aucun volume scan, E1, backtest, MT5, paper/broker/live.
