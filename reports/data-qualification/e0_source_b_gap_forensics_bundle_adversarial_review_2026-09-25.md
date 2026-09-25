# E0-SOURCE-B — revue adversariale du bundler de récupération gap-forensics

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD avant persistance : `1d5185143ca3d575ec046cd92ba709e941003ed8`

## Objet

Revue du helper :
`tools/e0_source_b_recover_gap_forensics_bundle.py`

Blob revu :
`bcdd55c512257afa4e94feab869f7a986f8dc68c`.

Objectif : récupérer les anciens rapports/scripts locaux sans relire `data/`, sans modifier les originaux et sans demander 53 uploads séparés.

## Attaques

### B1 — sélection trop large

Le candidat initial utilisait uniquement des globs + comptes attendus.

Risque :
un fichier attendu pourrait disparaître et être remplacé par un autre fichier au nom compatible tout en conservant le même compte.

**Correction :**
les 53 chemins relatifs exacts observés dans l'inventaire CSV sont maintenant hard-bindés dans `EXPECTED_RELATIVE_PATHS`.

Le helper exige égalité exacte du set sélectionné.

**Re-break : PASS.**

### B2 — lecture involontaire du corpus Parquet

Le helper ne parcourt que :
- `reports/data-qualification/dukascopy_research_a/huggingface_ustech_*.json`;
- `reports/data-qualification/provenance_timestamp_search.txt`;
- `tools/probe_huggingface_ustech_*.py`.

Tout chemin sélectionné contenant `data/` est rejeté.

**PASS.**

### B3 — modification des artefacts historiques

Le helper n'ouvre les sources qu'en lecture.
Le ZIP et son sidecar sont exigés hors du repo root.

**PASS statique.**

### B4 — symlink/reparse point

Chaque source sélectionnée est rejetée si symlink ou reparse point.

**PASS.**

### B5 — path escape

Chaque fichier doit rester sous le repo root après résolution de chemin.

**PASS.**

### B6 — inventaire démesuré

Bornes :
- max 100 fichiers ;
- max 16 MiB source ;
- attendu 53 fichiers.

Inventaire fourni :
- 53 fichiers ;
- ~5,8 MiB.

**PASS.**

### B7 — fichier modifié pendant création du ZIP

Risque :
hash calculé avant compression mais octets source modifiés avant `zf.write`.

**Correction :**
après écriture, le helper réouvre le ZIP et re-hashe **chaque entrée archivée**, puis compare taille et SHA-256 au manifest calculé à partir des sources.

Divergence :
`BLOCKED_GAP_FORENSICS_BUNDLE` et suppression du ZIP invalide.

**Re-break : PASS.**

### B8 — manifest ZIP incohérent

Le `BUNDLE-MANIFEST.json` archivé est relu et comparé objet par objet au manifest planifié.

**PASS.**

### B9 — archive path traversal

Les arcname viennent exclusivement des chemins relatifs exacts hard-bindés au repo et ne contiennent aucun `..`.

**PASS.**

### B10 — écrasement d'un fichier repo

L'output doit être hors repo root.
Un output existant doit être un fichier régulier avant remplacement.

**PASS.**

## Limites

Le bundle scelle l'état **courant** des artefacts historiques locaux. Il ne prouve pas encore :
- que ces artefacts correspondent au snapshot Source-B courant ;
- que leurs anciennes conclusions sont correctes ;
- que leurs sources externes sont toujours vérifiables.

Ces questions seront traitées après ingestion du bundle.

## Verdict

**PASS — helper de récupération suffisamment borné pour exécution locale read-only.**

## Frontière suivante

Exécuter localement le bundler.
Si :
`GAP_FORENSICS_BUNDLE_COMPLETE`
alors joindre le ZIP produit.

Aucune nouvelle recherche calendrier/événement avant ingestion et adjudication de ce bundle.
