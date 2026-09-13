# RECOVERY CHECKPOINT — END OF DAY — 12 SEPTEMBRE 2026

> Versioned durable handoff point for recovery across conversations.
> This checkpoint is the authoritative memory of the current workstream on `feat/v4-3-instrument-contracts`.

## 1. ÉTAT ACTUEL

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Branch:** `feat/v4-3-instrument-contracts`
- **PR:** #8 — draft, unmerged
- **Reference baseline:** `ff50b6d5d123969e091b5df18c46d438f7cb8052`
- **Last durable workstream:** B09 — PASS verrouillé
- **Current research block:** Phase 3 → 3.1 Expert Momentum → **3.1.1 PASS**
- **Next governed block:** **3.1.2 — Premier backtest baseline**

## 2. RÈGLE DE RÉCUPÉRATION

Au début de toute nouvelle discussion ou action substantielle, consulter dans cet ordre :

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. ce `04-REFERENCE/RECOVERY-CHECKPOINT.md`
3. `99-BACKUP/README.md`
4. le dernier `99-BACKUP/SESSION-YYYY-MM-DD.md`
5. `docs/00-MASTER-EXECUTION-CHECKLIST.md`
6. les artefacts de qualification/recherche référencés ci-dessous
7. l'état GitHub/worktree réel

La conversation ne constitue pas une source de vérité suffisante.

## 3. TRAVAIL DE QUALIFICATION DONNÉE — ÉTAT À CONSERVER

Le chantier de la journée a commencé par la qualification du chemin de donnée BI5/Dukascopy avant toute recherche de stratégie.

### Qualification verrouillée

- B02 — PASS : identité physique du corpus.
- B03 — FAIL initial : continuité 24/7 naïve invalide avec le calendrier de marché.
- B03.1 — FAIL initial : un trou inattendu restait.
- B03.2 — FAIL : perte d'acquisition confirmée ; corpus de référence incomplet à ce stade.
- B03.3 — FAIL intentionnel : une reconstruction candidate n'est pas une preuve de validité du dataset.
- B02' — PASS : corpus candidat qualifié à 495 fichiers.
- B03.1' — PASS : gaps restants expliqués par le calendrier explicite.
- B04 — PASS : intégrité sémantique des ticks.
- B05 — PASS : reproductibilité déterministe corpus/contrat.
- B06-A — PASS : identité corpus/contrat/source-format/fenêtre.
- B07-A — PASS : moteur BI5 natif verrouillé sur `BoundResearchInput`.
- B07-B — PASS : moteur natif a consommé le corpus qualifié.
- B06-B — PASS : binding fail-closed.
- B08 — PASS : exécution officielle qualifiée.
- B08-A — PASS : binding de production comme frontière architecturale moteur.
- B08-B.1 — PASS : graphe de production et contrôles de bypass.
- B09.0.1 — PASS.
- B09.1 — PASS.
- B09.2 — PASS : comparaison reader direct / moteur, 5 130 393 ticks.
- B09.3 — PASS immutabilité/séquence, mais FAIL sur l'ancienne représentation décimale du hash.
- B09.4 — BLOCKED : représentation numérique non définie dans le contrat ; aucune sémantique inventée.
- B09.5 — PASS : représentation IEEE-754 binaire exacte démontrée.
- B09.6 — PASS : hash de production corrigé avec `struct.pack(">d", value)`.
- B09.7 synthétique — PASS.
- B09.7 full-stream — PASS sur le corpus B05 exact.
- B09 run() exposure closure — PASS : `run()` classé `NON_OFFICIAL_NON_PRODUCTION` et exclu du chemin officiel qualifié.
- **B09 final — PASS verrouillé.**

## 4. IDENTITÉS / PREUVES IMPORTANTES

- B05 canonical corpus hash : `868a21c6a1bedf095b30bc64b6c2ef60b5db9d30146ac53034360254413f8ad7`
- B05 contract hash : `49e272534bf5061522eb624afe4e27d6585f730e0271b5284bff2442d5c04b07`
- Historical B08 stream SHA : `4768c0e66647a15ba703d2dcdc88c03db84846a625e8eb3f70914428bf11c8d7`
- Current B09 canonical stream SHA : `d8da494b2a1380ea0db0e0370ece4f609374ecb3e5647b6c1fb290836867abda`
- Corpus : `C:\ALGO-DATA\qualification\v4_3_multi_year_acquisition\candidate_b03_3_repaired\USATECHIDXUSD`
- Physical files : 495
- Full stream : 5 130 393 ticks

## 5. ERREURS / LEÇONS À NE PAS RÉPÉTER

1. Ne jamais supposer qu'un probe ou un fichier temporaire existe encore.
2. Ne jamais supposer qu'un chemin d'un worktree est celui du worktree actif.
3. Ne jamais qualifier une reconstruction de corpus comme équivalente au corpus de référence.
4. Ne jamais transformer un contrôle non exécutable ou BLOCKED en PASS.
5. Ne jamais considérer un cassage synthétique comme équivalent à un cassage full-stream sur le corpus qualifié.
6. Diagnostiquer un échec précis avant toute nouvelle tentative.
7. Préférer une réécriture propre à une substitution textuelle fragile.
8. Ne pas rerun B02–B08 ni B09.7 sauf nouvelle preuve invalidante.
9. Ne pas confondre une description de code dans un checkpoint avec la persistance réelle du code.
10. Toute session importante doit laisser une trace durable dans `99-BACKUP/`.

## 6. PHASE 3.1.1 — MOMENTUM V1

### Formalisation finale

- **Timeframe :** H1
- **Variable :** Close
- **Horizon :** 20 barres
- **Formule :** `M_t = Close_t / Close_{t-20} - 1`
- `M_t > 0` → `LONG`
- `M_t < 0` → `SHORT`
- `M_t = 0` → `NEUTRE`
- historique insuffisant → `UNDEFINED`
- calcul à la clôture de `t`
- signal utilisable à partir de `t+1`

### Contraintes validées

- pas de look-ahead ;
- pas de filtre de régime ;
- pas d'optimisation massive ;
- `20` est une hypothèse de baseline, pas une valeur prétendument optimale ;
- signal directionnel distinct d'une transaction ;
- risque, SL/TP et exécution hors périmètre de la définition Momentum.

### Cassage

Premier cassage : FAIL de formalisation sur timeframe non figé et confusion possible signal/action.

Correction : H1 explicite + séparation signal/transaction + `UNDEFINED` avant historique suffisant + convention `t`/`t+1`.

Second cassage :
- look-ahead PASS ;
- current-bar handling PASS ;
- timeframe PASS ;
- ambiguïté PASS ;
- direction change ≠ ordre PASS ;
- séparation régime PASS ;
- optimisation cachée PASS sous la contrainte baseline ;
- reproductibilité PASS ;
- historique insuffisant PASS ;
- données manquantes PASS sous réserve du contrôle par la couche data.

### Verdict

**3.1.1 — PASS**

Ce PASS valide uniquement la définition formelle. Il ne valide ni rentabilité, ni robustesse, ni valeur économique, ni supériorité par régime.

### Artefacts persistés aujourd'hui

- `docs/03.1.1-MOMENTUM-V1-DEFINITION.md` — commit `b98f4e547e09b31b3b45efc22705238c15ffdbb7`
- `reports/research/3_1_1_momentum_v1_adversarial_report.md` — commit `14d6274f8f4ab30fccef6ca41190ffc0894b57c6`

## 7. AUDIT DE PERSISTENCE DE FIN DE JOURNÉE

### Ce qui est bien persistant sur GitHub

- `04-REFERENCE/AI-OPERATING-MEMORY.md` — protocole durable de récupération et gouvernance.
- ce `04-REFERENCE/RECOVERY-CHECKPOINT.md` — handoff durable mis à jour.
- `99-BACKUP/README.md` — procédure durable de sauvegarde/récupération.
- `99-BACKUP/SESSION-2026-09-13.md` — snapshot durable de contexte de session.
- rapports B09 persistés :
  - `reports/data-qualification/b09_7_full_rebreak_report.json`
  - `reports/data-qualification/b09_run_exposure_closure_report.json`
- définition et cassage Momentum 3.1.1 persistés dans les deux artefacts ci-dessus.

### Point critique détecté pendant la vérification

La vérification GitHub montre que les fichiers de code B08-A/B09 décrits par le checkpoint historique (`src/research/input_binding.py`, `src/research/bi5_reader.py`, `src/research/engine.py`, `src/research/execution.py`) **ne sont pas présents sur la branche GitHub `feat/v4-3-instrument-contracts`**.

Le PR #8 actuellement visible sur GitHub contient les artefacts de contrat V4.3, rapports B09, outils et tests, mais pas ces quatre fichiers `src/research/*.py`.

Donc :

- **mémoire / état / résultats B09 : persistés ;**
- **rapports B09 visibles : persistés ;**
- **Momentum 3.1.1 : définition + cassage + verdict : persistés ;**
- **couche de sauvegarde durable de contexte : désormais persistée dans `99-BACKUP/`;**
- **persistance du code local B08-A/B09 : BLOCKED tant que le worktree local exact n'est pas récupéré et comparé/commité.**

Cette distinction est volontaire : aucun code absent de GitHub n'est déclaré comme sauvegardé.

### Incident de sauvegarde corrigé

Les deux artefacts Momentum avaient d'abord été créés par erreur sur `main` faute d'avoir explicité la branche dans l'appel d'écriture. Ils ont été supprimés de `main` et recréés sur `feat/v4-3-instrument-contracts`. La branche gouvernée est la destination de ces artefacts.

## 8. COUCHE DE SAUVEGARDE DURABLE AJOUTÉE

Le dossier dédié est désormais :

`99-BACKUP/`

Il contient :

- `99-BACKUP/README.md` — protocole de récupération du matin et règles de contenu.
- `99-BACKUP/SESSION-2026-09-13.md` — snapshot durable du contexte de la session.

L'AI Operating Memory a été renforcée pour rendre cette couche obligatoire au démarrage et à la clôture des sessions importantes.

Cette couche n'est pas un substitut au code : elle garantit que le contexte de recherche, les décisions, hypothèses, expériences, échecs, corrections, preuves, divergences et prochaine action ne dépendent plus uniquement de la conversation.

## 9. PROCHAINE ACTION UNIQUE

**Récupérer et vérifier l'état exact du worktree local B08-A/B09, puis décider sur preuves s'il doit être persisté dans GitHub ou s'il existe déjà ailleurs.**

Après cette vérification seulement : formaliser le protocole de `3.1.2 — Premier backtest baseline` avant toute implémentation ou exécution de backtest.

Ne pas rerun B02–B08. Ne pas rerun B09.7. Ne pas traiter `BI5ResearchEngine.run()` comme entrée qualifiée.

## 10. RÈGLE DE FIN DE JOURNÉE

À chaque fin de journée, mettre à jour ce checkpoint et créer/mettre à jour le snapshot `99-BACKUP/SESSION-YYYY-MM-DD.md` avec :

- ce qui a réellement été fait ;
- les verdicts ;
- les preuves et chemins ;
- les échecs/corrections ;
- ce qui est réellement présent sur GitHub ;
- toute divergence entre local et GitHub ;
- une seule prochaine action.

Objectif : qu'une nouvelle conversation puisse reprendre le travail sans dépendre de la mémoire conversationnelle et sans repartir à la recherche d'éléments dispersés.
