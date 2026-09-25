# E0-SOURCE-B-F1 — exécution locale + récupération du travail gap-forensics historique

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche gouvernée : `integration/system-v1`
HEAD vérifié avant écriture : `aa457f5a4e8a517557137d349b885c7648b0e98a`

## 1. Sortie terminale F1 fournie par le propriétaire

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

## 2. Verdict borné de l'exécution

**PASS — F1 a atteint sa terminaison locale selon la sortie terminale fournie.**

Constats terminaux :
- 376 003 618 timestamps lus ;
- 0 timestamp nul ;
- 0 retour temporel ;
- 0 timestamp adjacent égal ;
- 1 605 gaps bruts >60 s ;
- plus grand gap positif : 265 872 098 ms (~73 h 51 min 12,098 s).

Le JSON F1 exact n'est pas encore accessible à la session ; l'adjudication détaillée reste TO-PROVE jusqu'à son ingestion.

## 3. Convergence avec le travail historique

Le résultat F1 reproduit exactement les indicateurs centraux déjà observés dans le travail antérieur Source-B :
- 376 003 618 lignes/ticks ;
- 1 605 gaps >60 s ;
- plus grand gap ~265 872,098 s.

L'ancien travail ne s'était pas arrêté à ce scan brut. Les traces de travail historiques indiquent notamment :
- un passage de classification session/calendrier ;
- un sous-ensemble de **22 TRUE_OPEN_SESSION_GAP** répartis sur 6 fichiers après exclusion des fermetures attendues ;
- parmi ces 22, un maximum d'environ **1 800,923 s** ;
- un travail ultérieur de discrimination d'origine/source ayant établi **13 pertes d'acquisition démontrées** et **9 gaps restant inconnus** ;
- aucune réparation à promouvoir automatiquement ;
- continuité Source-B restant historiquement BLOCKED tant que les gaps résiduels n'étaient pas résolus.

Ces éléments historiques doivent être récupérés et confrontés au F1 courant avant toute répétition de recherche calendrier/événements.

## 4. Localisation des artefacts historiques

Le dépôt distant contient la branche :
`feat/min-experiment-gaps-batch-v1`
HEAD :
`2951345d8f0b47400b8b2d52885615f01f11556b`.

Inspection de son arbre Git distant :
**aucun** des scripts gap-forensics attendus n'est versionné dans cet arbre.

Cela correspond au `git status` local observé antérieurement : ces scripts étaient non suivis dans le clone Windows, notamment des noms de la famille :
- `probe_huggingface_ustech_open_gap_forensics_h9_1_c3_b2_c2.py`;
- `probe_huggingface_ustech_gap_origin_discrimination_h9_1_c3_b2_c3.py`;
- `probe_huggingface_ustech_gap_source_crosscheck_h9_1_c3_b2_c4.py`;
- `probe_huggingface_ustech_gap_loss_quantification_h9_1_c3_b2_c5.py`;
- `probe_huggingface_ustech_single_gap_repair_pilot_h9_1_c3_b2_c7.py`;
- `probe_huggingface_ustech_timezone_normalized_provenance_h9_1_c3_b2_c7_b2.py`;
- `probe_huggingface_ustech_session_continuity_h9_1_c3_b2_c.py`;
- `probe_huggingface_ustech_session_continuity_h9_1_c3_b2_c1.py`;
- `probe_huggingface_ustech_full_dataset_temporal_coverage_census_h9_1_c3_c8.py`;
- `probe_huggingface_ustech_existing_tick_provenance_h9_1_c3_b2_c7_b.py`.

Ces fichiers peuvent encore exister localement sans être récupérables depuis GitHub.

## 5. Décision de méthode

**NE PAS refaire maintenant la recherche calendrier/session/événements depuis zéro.**

Ordre correct :
1. ingérer le JSON F1 exact ;
2. inventorier les anciens artefacts locaux gap-forensics ;
3. récupérer d'abord les anciens **résultats** (JSON/MD/TXT) et seulement ensuite les scripts nécessaires ;
4. comparer leurs corpus/bindings/dates avec le manifest Source-B actuel ;
5. si identité compatible : réutiliser/valider les anciennes conclusions ;
6. seulement si les anciennes preuves sont absentes, incompatibles ou insuffisantes : refaire le minimum manquant.

## 6. Frontière actuelle

**LOCAL USER ACTION REQUIRED** :
- rendre le JSON F1 accessible ;
- produire un inventaire borné des artefacts locaux gap-forensics historiques.

Aucune nouvelle classification calendrier/événements n'est autorisée avant cette récupération.

Aucun E1/backtest/MT5/paper/broker/live.
