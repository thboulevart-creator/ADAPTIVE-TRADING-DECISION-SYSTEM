# Sauvegarde E0 — première archive GitHub historique inventoriée, corpus portefeuille encore absent

Date : 2026-09-23
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
Nature : E0 lecture seule ; aucune acquisition fournisseur, aucun backtest, aucun développement de stratégie.

## Références GitHub

HEAD initial fresh : `19f8b363e45f070ccbce9a5d0322f005579b4f08`.
Rapport E0 : `reports/data-qualification/e0_github_existing_bounded_market_archive_inventory_2026-09-23.md`.
Commit du rapport : `bbe72c7c0394385c0eeb153eabd4124e2fdc25f3`.
Blob du rapport : `298cb62753ff7a6c187859c3994c7d1e77d834e2`.
Checkpoint §194 actualisé : `be2d14329df19a6fd78e3214080a49410745e577`.
Blob du checkpoint : `58db9f36e045b53bd6477a9ee4348928a0385046`.

## Exact périmètre réellement exécuté

Dossier `evidence/berd02/gha_run_35533153289/bodies/`, neuf objets `K1.bi5` (`PW`, `P0`–`P7`) déjà présents au HEAD initial. Comparaison avec quatre JSON de provenance/capture/diagnostics archivés dans `evidence/berd02/gha_run_35533153289/`. Aucune écriture dans ces fichiers ni aucun contact Dukascopy.

SHA-256 des octets bruts recalculées via un outil mémoire dont l'implémentation SHA256 a été auto-testée sur le vecteur public « abc » ; **9/9 identités correspondantes** aux captures/diagnostics. Volume total **353 910 octets**. Les neuf en-têtes montrent `5d00004000` compatible LZMA-Alone. Le décodage historique A/B documente **69 830 enregistrements** au format `>IIIff`, qui n'ont **pas été recomptés pendant ce mouvement**.

Fenêtres UTC nominales : 2021-08-13 20:00 → 2026-08-14 21:00, **neuf heures isolées dans cet intervalle**, avec huit lacunes interfenêtres totalisant **43 840 heures**. Pas de corpus cinq ans continu, pas de données permettant une qualification Momentum V1 ou un portefeuille.

Incident corrigé : un premier décodeur base64 de la routine de contrôle donnait des longueurs/hashes incorrects et a été rejeté ; second passage corrigé et auto-testé : neuf concordances. Les données source n'ont jamais été modifiées. Limite procédurale : petite portée effectivement bornée, mais budget cumulatif chiffré non persisté **avant** la première lecture ; le futur E0 doit pré-enregistrer ses plafonds avant accès.

## Statuts préservés

PASS : **identité brute des neuf archives précisément désignées**, pas leur admissibilité générale.
BLOCKED : **admissibilité de ce lot comme corpus de recherche portefeuille/Momentum V1**.
A=AMBIGUOUS ; B=NOT_FOUND ; C=INCOMPLETE_VERSION_COVERAGE ; gate BI5 natif global BLOCKED. B-ERD-02 = PROBE_SUPPORTED pour neuf sondes seulement, pas FULL_INTERVAL_QUALIFIED. R-04/R-05/R-06 abandonnés ; aucun contact fournisseur.

Le dépôt à ce HEAD ne versionne aucun Parquet ni CSV historique. Les précédentes références au chemin relatif local `data/research_source_b_ustech/parquet/` indiquent un **candidat hors GitHub et à vérifier**, dont aucun octet n'a été inspecté ici ; aucune présence ni nombre actuels n'ont été affirmés. La bibliothèque de fichiers de cette session ne fournissait pas le corpus Parquet local.

## Prochaine action gouvernée unique

**E0-SOURCE-B : rendre effectivement accessible dans un emplacement expressément autorisé le corpus Parquet existant `data/research_source_b_ustech/parquet/`, préenregistrer un budget chiffré puis inventaire E0 borné des octets accessibles**, avec SHA-256, schéma, période, continuité, trous, timezone/sessions, source/licence et limites. Si l'accès n'est pas disponible : BLOCKED et STOP. Ne pas acquérir des données auprès du fournisseur, ni lancer E1, backtest, paper, broker ou live.

STOP.
