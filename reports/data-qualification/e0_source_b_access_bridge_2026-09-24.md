# E0-SOURCE-B-ACCESS — bridge local vers manifest exact

Date : 2026-09-24
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD avant clôture du bridge : `24783868b8294f0c29d4254117c77e0d935372f5`

## Objet

Le corpus `data/research_source_b_ustech/parquet/` n'est pas monté dans l'environnement ChatGPT courant. Il est impossible de rendre un dossier Windows local visible à cette session par une simple opération GitHub. Pour ne pas élargir le périmètre ni demander un transfert massif aveugle, le mouvement ACCESS matérialise un **bridge read-only** permettant au propriétaire d'exécuter localement le préflight déjà gelé et de produire un manifest exact à joindre ensuite à la session.

Aucune donnée fournisseur n'est téléchargée. Aucun fichier Parquet n'est modifié.

## Artefact opérationnel unique

`tools/e0_source_b_access_manifest.py`

Blob après création : `892ceca1d7f64572f16de9a8a874fe8c3cacec44`.

Un premier brouillon PowerShell a été créé puis **supprimé avant activation** après relecture statique, car :
- il dépendait d'une API .NET de chemin relatif dont la disponibilité varie avec Windows PowerShell ;
- son énumération récursive pouvait matérialiser plus d'entrées que le plafond avant d'appliquer le contrôle.

Le brouillon PowerShell n'est donc pas une voie autorisée. Le helper Python est l'unique bridge retenu.

## Contrôles du helper Python

Le script standard-library :
- résout uniquement `data/research_source_b_ustech/parquet/` relatif au repo root ;
- refuse une sortie de périmètre ;
- refuse symlink/reparse-style détectable ;
- arrête l'énumération dès la 1001e entrée ;
- arrête au 501e Parquet ;
- vérifie `PAR1` en tête et fin avec 8 octets par fichier ;
- bloque avant hashing si le total dépasse 16 GiB ;
- bloque si un fichier dépasse 8 GiB ;
- calcule SHA-256 par chunks de 8 MiB si le budget le permet ;
- re-stat chaque fichier après hash ;
- refait un snapshot metadata et bloque si le corpus a changé pendant l'inventaire ;
- écrit uniquement un JSON hors corpus, par défaut dans le répertoire temporaire du système ;
- ne contient aucun moteur Parquet, stratégie, signal, trade, PnL ou backtest.

## Test effectué avant versionnement

Une copie locale du helper a été :
1. compilée par `python -m py_compile` ;
2. exécutée sur un corpus synthétique temporaire comportant deux faux conteneurs Parquet minimalement encadrés par `PAR1` ;
3. vérifiée pour produire `MANIFEST_COMPLETE`, deux fichiers, SHA-256 complets, magic PASS et snapshot stable.

Ce test prouve le fonctionnement du bridge sur ce cas synthétique seulement. Il ne prouve rien sur Source-B.

## Commande locale à exécuter

Depuis la racine **du clone ATDS qui contient réellement le corpus** :

```powershell
python tools/e0_source_b_access_manifest.py
```

Sortie par défaut sous Windows :

```text
%TEMP%\ATDS-E0-SOURCE-B-MANIFEST.json
```

Si le clone utilisé n'est pas le répertoire courant :

```powershell
python tools/e0_source_b_access_manifest.py --repo-root "C:\CHEMIN\VERS\ADAPTIVE-TRADING-DECISION-SYSTEM"
```

Le script doit être exécuté tel que versionné. Le JSON doit être conservé même si le statut est `BLOCKED_*`, car il constitue le constat de préflight.

## Condition pour rendre le corpus accessible à la session

La prochaine session doit recevoir **le fichier JSON généré**. S'il est `MANIFEST_COMPLETE`, il donnera la liste exacte, tailles et SHA-256 permettant de décider quels octets/footers doivent être rendus accessibles ensuite, sans uploader aveuglément tout le corpus.

Si le manifest conclut `BLOCKED_TOTAL_READ_BUDGET`, `BLOCKED_FILE_COUNT_BUDGET`, `BLOCKED_ENTRY_BUDGET`, `BLOCKED_SYMLINK`, `BLOCKED_PARQUET_MAGIC` ou autre statut bloquant, ne pas contourner le résultat : joindre le JSON et réadjudication avant toute nouvelle lecture.

## Statut

**ACCESS BRIDGE = READY.**
**CORPUS ACCESS IN CHAT = STILL BLOCKED until the generated manifest/corpus is actually attached or mounted.**

Aucun E1, backtest, développement Momentum, paper/broker/live ou contact Dukascopy n'est ouvert.

## Prochaine action gouvernée unique

Exécuter localement le helper versionné sur le clone contenant Source-B et rendre `ATDS-E0-SOURCE-B-MANIFEST.json` accessible à cette session. Puis fresh HEAD et adjudication du manifest sous le budget déjà figé.

STOP.
