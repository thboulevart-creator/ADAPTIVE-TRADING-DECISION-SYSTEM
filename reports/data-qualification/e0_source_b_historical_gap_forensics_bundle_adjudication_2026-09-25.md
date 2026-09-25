# E0-SOURCE-B — adjudication du bundle historique gap-forensics

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD vérifié avant écriture : `9e9e83d1910810c7f86a78a8703bedf9e2029e89`

## 1. Bundle exact reçu

Fichier :
`ATDS-SOURCE-B-GAP-FORENSICS-HISTORICAL.zip`

Taille :
**569 584 octets**.

SHA-256 recalculé dans la session :
`072f26bfacd51ba1501d3c9009d79c78436f360fc6eccd7143275db759f9d028`.

Cette valeur correspond exactement au sidecar déjà scellé.

## 2. Manifest interne

Schema :
`ATDS_E0_SOURCE_B_GAP_FORENSICS_RECOVERY_BUNDLE_V0_1`.

Génération :
`2026-09-25T14:33:27.262196+00:00`.

Manifest :
- `total_files = 53` ;
- `total_bytes = 5 774 487` ;
- 27 reports JSON ;
- 25 scripts Python ;
- 1 provenance text ;
- aucun chemin `data/` ;
- plafond déclaré 16 MiB ;
- SHA-256 du set de 53 chemins attendus :
  `58ebd481000d1704451b7b1325ceb69de5e00704a453034e410419d894040dea`.

Vérification session :
- 53/53 chemins uniques ;
- 53/53 tailles ZIP = manifest ;
- 53/53 SHA-256 d'entrées ZIP = manifest ;
- manifest interne lisible et cohérent.

**Verdict bundle : PASS.**

## 3. Reconstruction de la chaîne historique

### C7-C2/C3 — six fichiers représentatifs

`session_continuity_h9_1_c3_b2_c1.json` :
- 6 fichiers ;
- 8 941 304 lignes ;
- calendrier America/New_York ;
- fermeture quotidienne modélisée 16:15→18:00 NY ;
- holidays non modélisés ;
- portée représentative uniquement.

`open_gap_forensics_h9_1_c3_b2_c2.json` :
- status PASS ;
- 22 gaps étudiés ;
- seuil 60 s ;
- max 1 800,923 s ;
- portée observational-only ;
- 6 fichiers seulement.

`gap_origin_discrimination_h9_1_c3_b2_c3.json` :
- 22/22 gaps internes aux fichiers ;
- 0 signature de proximité de frontière ;
- origine non prouvée localement ;
- décision : source-level cross-check requis.

### C4 — source cross-check

`gap_source_crosscheck_h9_1_c3_b2_c4.json` :
- 5 gaps représentatifs testés ;
- 2 avec ticks source présents pendant le gap Parquet ;
- 3 avec contexte source insuffisant ;
- contradiction source/dataset démontrée sur au moins un cas ;
- continuité et qualité full-dataset non certifiées.

### C5 — quantification

`gap_loss_quantification_h9_1_c3_b2_c5.json` :
- 22 gaps ;
- **13 DATASET_ACQUISITION_LOSS** ;
- **9 UNKNOWN_INSUFFICIENT_SOURCE_CONTEXT** ;
- 0 SOURCE_GAP_POSSIBLE ;
- 5 542,711 s de pertes d'acquisition démontrées ;
- 2 311,618 s inconnues ;
- 7 854,329 s total.

### C6/C7 — repairability / reconciliation

`dataset_repairability_h9_1_c3_b2_c6.json` :
- repair path = `REPAIRABLE_IN_PRINCIPLE` ;
- repair execution = `REPAIR_NOT_EXECUTED` ;
- scope partiellement classifié ;
- research-source certification BLOCKED.

`existing_gap_reconciliation_h9_1_c3_b2_c7_a.json` :
- un intervalle démontré DATASET_ACQUISITION_LOSS a été confronté au Parquet existant et à une source ;
- temporalité proche mais prix fortement divergents ;
- aucune promotion d'équivalence feed/source.

## 4. Binding des 22 gaps au F1 courant

Le F1 exact courant contient 1 605 gaps >60 s.

Les 22 paires `(start_utc,end_utc)` de l'ancien `open_gap_forensics` ont été converties en epoch-ms puis recherchées dans les 1 605 gaps du F1 courant.

Résultat :
**22/22 match exact**.

Les 22 paires du rapport `gap_loss_quantification` correspondent également :
**22/22 match exact**.

Les six fichiers représentatifs ont les mêmes row counts que dans le F1 courant :
- 2021-05 part0000 : 1 167 137 ;
- 2022-08 part0000 : 1 700 016 ;
- 2023-08 part0000 : 2 130 323 ;
- 2024-08 part0000 : 2 135 266 ;
- 2025-08 part0000 : 468 965 ;
- 2026-05 part0002 : 1 339 597.

Conclusion :
les classifications historiques **13 LOSS / 9 UNKNOWN** sont réutilisables pour ces **22 intervalles exacts** du snapshot courant.

Elles ne doivent PAS être extrapolées aux 1 583 autres gaps >60 s.

## 5. Contradiction de sémantique temporelle historique

Les artefacts récupérés contiennent deux approches incompatibles :

1. les premiers gap/session probes travaillent selon une session NY 16:15→18:00 et certaines conversions Python naïves dépendantes de l'environnement ;
2. des probes ultérieurs imposent :
   `timestamp[ms] naive = Europe/Paris wall-clock → UTC`.

Le rapport `timezone_normalized_provenance` ne certifie pas l'équivalence feed :
- 33 timestamps exacts communs seulement sur 7 156 ticks Parquet / 8 184 source ;
- 0 exact bid/ask match ;
- écart prix moyen ~786 points ;
- classification uniquement observationnelle.

La politique Europe/Paris ne peut donc pas être reprise comme vérité qualifiée sans reconciliation.

## 6. Verdict

**PASS — récupération et intégrité du gap-forensics historique.**

**PASS — réutilisation des conclusions 13 LOSS / 9 UNKNOWN pour les 22 intervalles exacts uniquement.**

**BLOCKED — extrapolation de ces conclusions aux 1 605 gaps du corpus complet.**

**TO-RESOLVE — sémantique timestamp/session avant toute classification full-corpus.**

## 7. Prochaine action

Réconcilier la sémantique temporelle avec :
- le F1 courant ;
- les patterns de coupure récurrents ;
- les heures officielles USATECH ;
- les scripts historiques qui ont introduit une conversion implicite ou explicite.

Ensuite seulement produire une classification full-corpus des 1 605 gaps.
