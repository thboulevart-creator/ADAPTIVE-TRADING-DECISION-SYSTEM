# E0-SOURCE-B — inventaire local du gap-forensics historique à récupérer

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD vérifié avant écriture : `661ad954827659175c469f76647d9dcf5bcccf11`

## Source

Inventaire CSV fourni par le propriétaire après scan borné du clone Windows :
- taille : **9 968 octets** ;
- SHA-256 : `a9a3fa3719c87a64526b1ef8f33e10611a11f1f752a4b06c562afd26a8ee8871`;
- lignes artefacts : **53**.

Répartition :
- **28** artefacts sous `reports/`, total **5 186 327 octets** ;
- **25** scripts sous `tools/`, total **588 160 octets** ;
- total inventorié : **5 774 487 octets**.

Aucun artefact de `data/` n'est inclus.

## Résultats historiques présents localement

Les rapports suivants existent explicitement dans :
`reports/data-qualification/dukascopy_research_a/`

Chaîne gap/continuité :
- `huggingface_ustech_session_continuity_h9_1_c3_b2_c.json`
- `huggingface_ustech_session_continuity_h9_1_c3_b2_c1.json`
- `huggingface_ustech_open_gap_forensics_h9_1_c3_b2_c2.json`
- `huggingface_ustech_gap_origin_discrimination_h9_1_c3_b2_c3.json`
- `huggingface_ustech_gap_source_crosscheck_h9_1_c3_b2_c4.json`
- `huggingface_ustech_gap_loss_quantification_h9_1_c3_b2_c5.json`
- `huggingface_ustech_dataset_repairability_h9_1_c3_b2_c6.json`
- `huggingface_ustech_single_gap_repair_pilot_h9_1_c3_b2_c7.json`
- `huggingface_ustech_existing_gap_reconciliation_h9_1_c3_b2_c7_a.json`

Sémantique temps/provenance :
- `huggingface_ustech_timestamp_semantics_h9_1_c3_b2_c7_b1.json`
- `huggingface_ustech_timezone_normalized_provenance_h9_1_c3_b2_c7_b2.json`
- `huggingface_ustech_time_alignment_forensics_h9_1_c3_b2_c7_b4.json`
- `huggingface_ustech_existing_tick_provenance_h9_1_c3_b2_c7_b.json`
- `provenance_timestamp_search.txt`.

Qualification plus large :
- `huggingface_ustech_integrity_provenance_h9_1_c3_b1.json`
- `huggingface_ustech_tick_quality_h9_1_c3_b2.json`
- `huggingface_ustech_full_dataset_temporal_coverage_census_h9_1_c3_c8.json`
- `huggingface_ustech_local_dataset_inventory_coverage_h9_1_c3_c7_c9.json`
- `huggingface_ustech_full_dataset_qualification_c7_c11.json`.

Les scripts correspondants sont également présents localement sous `tools/`.

## Décision

**PASS — les artefacts historiques nécessaires à la non-répétition du gap-forensics sont encore présents localement.**

Ils ne sont pas encore qualifiés comme réutilisables :
- leurs contenus exacts n'ont pas encore été ingérés dans la session ;
- leurs hashes actuels restent à sceller ;
- leur binding précis au snapshot Source-B courant reste à confronter.

## Stratégie de récupération

Ne pas demander 53 uploads séparés.

Créer un bundle read-only contenant exactement ces 53 artefacts plus un manifest SHA-256 généré localement.

Le bundle ne doit :
- lire aucun fichier `data/` ;
- modifier aucun artefact historique ;
- écrire uniquement hors du dépôt ;
- refuser tout symlink/reparse point ;
- refuser un inventaire inattendu ou excessif.

Après ingestion du bundle :
1. parser d'abord les rapports JSON ;
2. reconstruire la chaîne session → open gaps → origin discrimination → source crosscheck → loss quantification → repairability ;
3. vérifier les nombres historiques 22 / 13 / 9 à partir des preuves exactes ;
4. comparer corpus/dates/paths/hashes avec F1 courant ;
5. seulement si une preuve manque, relancer le minimum nécessaire.

Aucune nouvelle recherche calendrier/événement avant cette récupération.
