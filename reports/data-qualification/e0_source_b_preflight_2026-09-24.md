# E0-SOURCE-B — Préflight d'accès borné au corpus Parquet local

Date : 2026-09-24
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD vérifié avant préflight : `652ef8bdfe4f99d5ac336ff509d8bfef5b47ebaf`
Statut : **AUTORISATION E0 LIMITÉE — AUCUNE E1**

## Périmètre exact

Chemin relatif candidat, déjà désigné dans le checkpoint actif :
`data/research_source_b_ustech/parquet/`

L'accès est limité à la résolution de ce chemin dans l'environnement d'exécution effectivement disponible à cette session. Aucun chemin voisin n'est autorisé comme substitut. Aucun suivi de symlink vers l'extérieur du périmètre. Aucun réseau fournisseur.

## Budget préenregistré AVANT lecture du corpus

1. Inventaire de métadonnées filesystem : maximum **1 000 entrées** sous le périmètre et maximum **500 fichiers .parquet**.
2. Lecture cumulée d'octets de fichiers Parquet pour hashing/inspection/scans : maximum **16 GiB**.
3. Lecture cumulée de footers/métadonnées Parquet : maximum **128 MiB**.
4. Aucun fichier individuel supérieur à **8 GiB** ne sera lu intégralement dans ce mouvement ; il sera seulement staté et marqué hors budget pour hashing complet.
5. Si le total des fichiers Parquet excède **16 GiB**, l'identité complète par SHA-256 de tout le corpus est **BLOCKED PAR BUDGET** ; ne pas élargir silencieusement.
6. L'analyse de continuité utilisera d'abord les métadonnées/footer et statistiques de row groups. Un scan de colonne temporelle n'est autorisé que si son coût reste à l'intérieur du budget de 16 GiB et si aucune donnée non temporelle n'est requise.
7. CPU/processus : aucun calcul de stratégie, aucun signal, aucune position, aucun PnL, aucun backtest.
8. Écriture : **zéro écriture** dans le corpus. Seuls des rapports/artefacts de gouvernance peuvent être écrits dans GitHub.
9. Accès : lecture seule du chemin exact ; si absent/inaccessible dans l'environnement courant, verdict **BLOCKED — CORPUS LOCAL NON ACCESSIBLE**.
10. Droits/licence : l'accès technique ne sera pas assimilé à une licence de redistribution ; provenance/licence restent à documenter séparément si absentes.

## Livrable E0 attendu si accessible

- chemin réellement résolu ;
- inventaire fichiers/tailles ;
- SHA-256 selon budget ;
- schéma Parquet ;
- colonnes temporelles et fuseau s'ils sont établissables ;
- bornes temporelles ;
- comptages ligne/row groups ;
- continuité inter-fichiers et, si prouvable sous budget, trous internes ;
- champs bid/ask/spread disponibles ;
- provenance/licence observables ;
- limites d'usage pour Momentum V1 et recherche portefeuille.

Aucun résultat favorable ne pourra ouvrir E1 automatiquement.

STOP si le chemin n'est pas accessible ou si une borne de budget impose l'arrêt.
