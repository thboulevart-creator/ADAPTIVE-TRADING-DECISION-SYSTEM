# Sauvegarde — F1 COMPLETE, récupération du gap-forensics historique

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`

## F1 terminal

```text
F1_COMPLETE
Rows read: 376003618
Null timestamps: 0
Backward transitions: 0
Equal adjacent timestamps: 0
Gaps >60s: 1605
Largest positive gap ms: 265872098
Report: C:\Users\Boulevart\AppData\Local\Temp\ATDS-E0-SOURCE-B-F1-TIMESTAMP-SCAN.json
```

Verdict borné :
**PASS — terminaison F1 locale selon sortie terminale.**

Le JSON F1 exact reste à joindre pour adjudication complète.

## Travail historique à récupérer avant reclassification

Les indicateurs F1 correspondent au scan historique Source-B déjà étudié.

Le travail antérieur avait notamment progressé jusqu'à :
- 22 `TRUE_OPEN_SESSION_GAP` sur 6 fichiers après filtres session/calendrier ;
- max de ce sous-ensemble ~1 800,923 s ;
- 13 pertes d'acquisition démontrées par cross-check source ;
- 9 gaps restant inconnus ;
- aucune réparation à promouvoir automatiquement ;
- continuité historiquement non certifiée.

Ces éléments ne doivent pas être recalculés depuis zéro avant récupération des preuves locales.

Branche distante historique :
`feat/min-experiment-gaps-batch-v1`
HEAD `2951345d8f0b47400b8b2d52885615f01f11556b`.

Les scripts gap-forensics ne sont pas dans son arbre Git distant ; le précédent status local les montrait non suivis.

## Prochaine action unique

Sur le clone Windows :
1. copier le JSON F1 depuis `%TEMP%` vers le vrai Bureau ;
2. inventorier uniquement les artefacts gap-forensics locaux dans `tools`, `reports`, `LOCAL-EVIDENCE`, `audit`, sans parcourir `data` ;
3. joindre F1 + l'inventaire.

Ensuite récupération ciblée des anciens résultats, vérification de binding et réutilisation si compatible.

Checkpoint actif : §203.

Aucun nouveau calendrier/événement, aucun E1/backtest/MT5/paper/broker/live avant cette récupération.
