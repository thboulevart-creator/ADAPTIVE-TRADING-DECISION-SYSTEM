# E0-SOURCE-B-F0 — exécution locale observée, JSON exact à ingérer

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD vérifié avant écriture : `2d084d8e8116748d42cf95dc5bb63043bb21ec1d`

## Sortie terminale fournie par le propriétaire

```text
F0_COMPLETE
Files: 212
Footer envelope bytes: 448636
Rows: 376003618
Row groups: 488
Schema signatures: 1
Temporal candidates: timestamp
Report: C:\Users\Boulevart\AppData\Local\Temp\ATDS-E0-SOURCE-B-F0-FOOTER-CENSUS.json
```

## Adjudication bornée de la sortie terminale

Le helper courant était lié au manifest exact corrigé et re-breaké avant cette tentative.

Constats fournis par sa terminaison :
- statut terminal : `F0_COMPLETE` ;
- 212 fichiers traités ;
- somme des enveloppes footer : **448 636 octets** ;
- nombre total de lignes metadata : **376 003 618** ;
- nombre total de row groups : **488** ;
- nombre de signatures de schéma : **1** ;
- candidat temporel détecté : **timestamp**.

Budget :
- probe initial : 212 × 8 = **1 696 octets** ;
- footer envelopes : **448 636 octets** ;
- cumul logique planifié : **450 332 octets** ;
- plafond : **134 217 728 octets (128 MiB)**.

Le run se situe très largement sous le plafond metadata préenregistré.

## Verdict

**PASS — exécution locale F0 complète selon la sortie terminale fournie par le propriétaire.**

Ce PASS prouve seulement que le helper a atteint sa terminaison F0 sous ses breakers.

Reste **TO-PROVE dans la session** jusqu'à ingestion du JSON exact :
- identité SHA-256 du rapport F0 ;
- détail du schéma unique ;
- noms/types/nullabilité des colonnes ;
- metadata Arrow/Parquet ;
- champs bid/ask/spread détectés ;
- statistiques temporelles min/max ;
- row groups avec/sans statistiques timestamp ;
- cohérence fichier par fichier des 212 entrées ;
- stabilité déclarée dans le rapport exact.

Aucune conclusion F1 ne doit être tirée de la seule sortie terminale.

## Prochaine action gouvernée unique

Rendre accessible à la session :

`C:\Users\Boulevart\AppData\Local\Temp\ATDS-E0-SOURCE-B-F0-FOOTER-CENSUS.json`

Puis :
1. fresh HEAD ;
2. ingestion intégrale du JSON exact ;
3. adjudication F0 ;
4. déterminer si les footers suffisent aux bornes temporelles et à une partie de la continuité ;
5. seulement si nécessaire, formaliser F1 comme scan de la seule colonne temporelle.

Aucun F1 n'est encore ouvert par ce rapport.
Aucun E1/backtest/MT5/paper/broker/live.

STOP à la frontière de transfert local.
