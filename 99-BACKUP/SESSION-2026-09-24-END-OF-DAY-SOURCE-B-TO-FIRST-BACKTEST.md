# Sauvegarde fin de journée — Source-B vers premier backtest 5 ans

Date : 2026-09-24
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
Fresh HEAD avant sauvegarde : `7a8e7abdbcbf78b993c66445732fb0d54edb4304`

## État durable atteint aujourd'hui

Le corpus local Source-B au chemin :
`data/research_source_b_ustech/parquet/`
a été rendu accessible via un bridge local read-only puis inventorié par manifest exact.

Manifest exact :
- 212 fichiers Parquet ;
- 3 936 721 231 octets ;
- 279 entrées filesystem ;
- 212/212 SHA-256 status PASS ;
- 212/212 magic `PAR1` head/tail PASS ;
- `sha256_complete=true` ;
- `parquet_magic_checked=true` ;
- `snapshot_stable=true` ;
- 61 mois nominaux consécutifs dans les chemins, 2021-05 → 2026-05, sans mois nominal absent.

SHA-256 du JSON manifest :
`c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5`.

Digest canonique path/size/hash :
`c6baf5c42808317167b5dc60c88d86b4481b3d0004565bc3a7b33d54ef13ea54`.

Rapport d'adjudication :
`reports/data-qualification/e0_source_b_manifest_adjudication_2026-09-24.md`.

Checkpoint actif : §198.

Verdict :
**PASS borné — identité/inventaire byte-level du snapshot via helper + manifest exact.**

Ne sont pas encore qualifiés :
- schéma logique Parquet ;
- nombre total de lignes/row groups ;
- champ timestamp/type/timezone ;
- bornes temporelles réellement contenues ;
- ordre/duplicates/trous ;
- bid/ask/spread ;
- provenance/licence ;
- admissibilité pour Momentum V1 / portefeuille ;
- E1.

## Exactement une prochaine action gouvernée demain

**E0-SOURCE-B-F0 — footer census read-only des 212 Parquet sous plafond metadata 128 MiB.**

Séquence :
1. vérifier taille/mtime contre le manifest ;
2. lire 8 octets de fin par fichier ;
3. extraire `footer_len` ;
4. sommer `footer_len + 8` ;
5. BLOCKED si total >128 MiB ;
6. sinon lire uniquement les footers ;
7. extraire schéma, row counts/groups, colonne timestamp/type/timezone, champs bid/ask/spread, statistiques min/max temporelles disponibles ;
8. STOP avant tout scan de colonne.

Si les statistiques footer ne suffisent pas pour prouver les trous internes, une étape séparée F1 sera requise : scan streaming de la seule colonne temporelle.

## Route minimale vers le premier backtest exploratoire 5 ans

Sous la frontière `EXPLORATORY OFFLINE RESEARCH V0`, le premier run E1 N0 peut être ouvert avant fermeture de tous les gates confirmatoires, mais uniquement après :
1. F0 footer census ;
2. F1 temporel si nécessaire pour continuité réelle ;
3. identité des champs nécessaires et convention temporelle ;
4. provenance/droits d'usage suffisamment établis pour la question ;
5. décision d'admissibilité du corpus pour le run exploratoire précis ;
6. protocole de run spécifique + fenêtre exacte + intensité de consultation ;
7. modèle d'exécution et coûts honnêtement étiquetés ; toute composante requise inconnue = BLOCKED, pas zéro ;
8. plafonds de ressources + préflight de run ;
9. autorisation propriétaire spécifique E1 ;
10. intégration/portage vers le moteur choisi, avec contrôle de parité avant de conclure.

Le protocole Momentum V1 baseline existe déjà et est PASS comme spécification, mais son exécution réelle reste distincte.

Pour un backtest MT5 de qualification, les exigences sont plus fortes : dataset gate applicable PASS, cinq ans réels, exécution adaptée en vrais ticks lorsque requise, coûts réalistes, split OOS gelé avant résultat, reproductibilité, et MT5 `Every tick based on real ticks` lorsque le protocole l'exige.

Le global native-BI5 gate historiquement BLOCKED ne devient pas PASS par Source-B Parquet ; inversement il ne doit pas être utilisé automatiquement comme blocker universel pour une E1 Parquet distincte. Les exigences doivent être évaluées pour la source et le run réellement choisis.

Aucune acquisition fournisseur ni contact Dukascopy n'est nécessaire pour la route Source-B actuelle.

## Ce qui peut attendre après le premier E1

Ne sont pas nécessaires pour lancer le tout premier E1 exploratoire si la fiche de run les exclut honnêtement, mais seront nécessaires avant promotion/qualification :
- charte confirmatoire complète ;
- budget d'hypothèses ;
- gel technique confirmatoire ;
- OOS probatoire correctement préservé ;
- robustesse et spread widening ;
- validation multi-critères ;
- niveau de preuve/promotion ;
- paper/broker/live/capital.

## Frontières conservées

Aucun E1 n'est encore autorisé.
Aucun backtest n'est encore lancé.
Aucun paper/broker/live.
Aucun contact Dukascopy.

STOP.
