# ADAPTIVE-TRADING-DECISION-SYSTEM — carte architecturale

> Export Markdown intégral de l'Artifact interactif. Aucun contenu n'a été résumé, reformulé ou modifié : ce fichier contient l'ensemble des composants, statuts, relations, contrats, invariants, preuves, lacunes, capacités, défaillances, dépendances, améliorations et conclusions du snapshot.

- **Dépôt :** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Date du snapshot :** 15 septembre 2026
- **Nature :** carte architecturale reconstruite depuis le dépôt, pas un résumé du repository
- **Artifact interactif équivalent :** https://claude.ai/artifact/8wFqHZKTeKkZHBGxCwj4eV

## Verdicts d'en-tête

| Indicateur | Valeur | Portée |
|---|---|---|
| Tests verts, branche active | **530** | suite rejouée localement |
| Dates calendrier résolues | **60 / 111** | enveloppe 2018-05-01 → 2026-08-14 |
| Couverture calendrier | **BLOCKED** | `SPECIAL_SESSION_EVIDENCE_COVERAGE_INCOMPLETE` |
| Backtest réel et acquisition `.bi5` | **INTERDIT** | checkpoint du 15/09 |

## Avertissement de lecture

`main` n'est pas l'état du système. La chaîne exécutable vit sur des branches non fusionnées, et le `RECOVERY-CHECKPOINT.md` de `main` désigne une branche active qui est elle-même dépassée. Chaque composant porte donc sa branche d'origine.

---

## 1. Légende

### Statuts de maturité

| Marqueur | Statut | Libellé complet | Définition |
|---|---|---|---|
| 🟢 | `EXISTANT` | EXISTANT — prouvé | Code, test ou rapport identifiable dans le dépôt, et exécution reproduite localement. |
| 🟡 | `PARTIEL` | PARTIEL | Existe et fonctionne, mais hors de la branche de référence, ou couvert partiellement, ou avec un défaut ouvert. |
| 🔵 | `SPECIFIE` | SPÉCIFIÉ, non implémenté | Document normatif ou candidat existe. Aucune implémentation correspondante dans src/. |
| ⚪ | `CIBLE` | CIBLE FUTURE | Décrit dans la vision du dépôt comme état final. Aucun artefact. |
| 🔴 | `MANQUANT` | MANQUANT / BLOCAGE | Absent, bloqué, ou présent avec une faille ouverte qui invalide la fonction. |
| 🟣 | `EXTERNE` | DÉPENDANCE EXTERNE | Hors du contrôle du dépôt. |
| ⚠️ | `AMBIGU` | AMBIGUÏTÉ — à vérifier | Deux sources du dépôt se contredisent ou une source est périmée. À trancher. |

### Liaisons entre couches

- **Trait plein vert** — Liaison implémentée et démontrée par exécution.
- **Trait plein ambre** — Liaison implémentée mais hors branche de référence ou partiellement prouvée.
- **Trait interrompu rouge** — Liaison existante mais avec gate BLOCKED ou contrôle contournable.
- **Trait pointillé gris** — Liaison cible. Aucun producteur, aucun consommateur.

### Branches référencées

| Clé | Branche |
|---|---|
| `multi` | `feat/multi-year-dukascopy-acquisition` |
| `dpc` | `feat/decision-producer-contract` |
| `syn` | `feat/synthetic-end-to-end-chain` |
| `pbf` | `audit/pre-backtest-freeze` |
| `v43` | `feat/v4-3-instrument-contracts` |
| `main` | `main` |

---

## 2. NIVEAU 0 — le système en une image

```text
MONDE EXTÉRIEUR   Dukascopy · VT Markets/MT5 · GitHub Actions
      │
GOUVERNANCE       mémoire opérationnelle · sécurité dépôt · frontière humaine
      │
CORPUS NORMATIF   vision · critères de validation · contrats · registres · adjudications
      │
DATA              🟢 identité des octets · admissibilité · BI5 · liaison de corpus
      │
VÉRITÉ TEMPORELLE 🟢 calendrier de sessions · récupération broker
      ╪══ GATE DE GEL DE FENÊTRE : BLOCKED (31 non résolues / 68 en fenêtre)
      ╪══ ACQUISITION .bi5 : INTERDITE   ·   BACKTEST RÉEL : NON AUTORISÉ
      │
CONTEXTE          🟡 identité déterministe (hors main)
      │
RECHERCHE         🟡 preuve de run · 🔵 Momentum V1 défini, non implémenté
      ╪══ FRONTIÈRE RESEARCH → DECISION : CONTOURNABLE (forgeage vérifié)
      │
DÉCISION          🔴 contrat de traçabilité seul · ⚪ aucun moteur
      │
RISQUE            ⚪ absent — zéro code
      │
ACTION            🔴 absent — aucun code broker nulle part
      │
RÉSULTAT          🔴 absent — synthétique uniquement
      │
TRACE             🟡 reconstruction structurelle
      │
MÉMOIRE / AUDIT / RÉVISION  🔵 charte · 🟡 audit exécutable calendrier seulement
      ↺  boucle de révision : rupture TOTALE
```

---

## 3. NIVEAU 1 — couches et frontières de confiance

### 3.1 Les 13 couches

| # | Couche | Périmètre | Composants |
|---|---|---|---|
| 1 | **MONDE EXTÉRIEUR** | Dukascopy, VT Markets/MT5, GitHub Actions | 3 |
| 2 | **GOUVERNANCE** | Mémoire opérationnelle, sécurité dépôt, frontière humaine | 5 |
| 3 | **CORPUS NORMATIF** | Vision, critères de validation, contrats, registres, adjudications | 5 |
| 4 | **DATA** | Identité des octets, admissibilité, lecture BI5, liaison de corpus | 5 |
| 5 | **VÉRITÉ TEMPORELLE** | Calendrier de sessions, récupération broker, fenêtre d'exécution | 5 |
| 6 | **CONTEXTE** | Identité déterministe du contexte d'observation | 1 |
| 7 | **RECHERCHE / EXPÉRIENCE** | Preuve de run, contrat de findings, expert Momentum V1 | 2 |
| 8 | **DÉCISION** | Contrat producteur, moteur de décision | 2 |
| 9 | **RISQUE / GOUVERNANCE D'EXPOSITION** | Risk Engine, Portfolio Engine, architecture de sortie | 2 |
| 10 | **ACTION / EXÉCUTION** | Producteur d'action, ordres broker | 1 |
| 11 | **RÉSULTAT** | Observation et attribution | 1 |
| 12 | **TRACE** | Reconstruction structurelle, chaîne synthétique | 2 |
| 13 | **MÉMOIRE / AUDIT / RÉVISION** | Mémoire expérimentale, audit exécutable, boucle de révision | 2 |

### 3.2 Frontières entre couches

Chaque frontière indique : qui produit, sous quel contrat, avec quel contrôle, et ce qui se passe si le contrat est violé.

| Frontière depuis | Type de trait | Description du contrôle et du comportement en cas de violation | Composant pivot |
|---|---|---|---|
| **DATA** | plein vert — démontré | DATA → CONTEXT · contrôle : identité recalculée sur 7 champs · violation : rejet · statut : exécutable mais hors main | `ctx` |
| **VÉRITÉ TEMPORELLE** | interrompu rouge — BLOCKED ou contournable | VÉRITÉ TEMPORELLE → suite · gate de gel de fenêtre : BLOCKED, 31 dates non résolues sur 68 en fenêtre · acquisition .bi5 : INTERDITE · backtest réel : NON AUTORISÉ | `cal-win` |
| **CONTEXTE** | plein ambre — partiel | CONTEXT → RESEARCH · contrôle : validate_context + configuration_version + identité de rapport · violation : ValueError · statut : testé, CI liée à une autre branche | `res-ev` |
| **RECHERCHE / EXPÉRIENCE** | interrompu rouge — BLOCKED ou contournable | RESEARCH → DECISION · contrôle : jeton _factory_validated · CONTOURNABLE — forgeage vérifié · 2 à 3 tests rouges selon la branche | `dec` |
| **DÉCISION** | pointillé gris — inexistant | DECISION → RISK → ACTION · aucun contrôle, aucun producteur, aucun code | `act` |
| **ACTION / EXÉCUTION** | pointillé gris — inexistant | ACTION → RESULT · inexistant hors harness synthétique | `resu` |
| **RÉSULTAT** | pointillé gris — inexistant | RESULT → TRACE · DecisionTrace peut porter un result_id sans qu'aucun résultat réel existe | `trace` |
| **TRACE** | pointillé gris — inexistant | TRACE → MÉMOIRE → AUDIT → RÉVISION · ruptures qualifiées TOTALES par le dépôt | `mem` |

---

## 4. NIVEAUX 2 à 4 — inventaire canonique des composants

Ordre : couche par couche, dans l'ordre de la chaîne. Chaque fiche contient le rôle, le domaine, le statut, la branche, les entrées, les sorties, le contrat, les invariants, les conditions de fonctionnement, les conditions de refus, les preuves disponibles, les fichiers GitHub et les éléments manquants.

### 4.0 Table de synthèse

| Composant | Couche | Statut | Branche | Vues |
|---|---|---|---|---|
| Dukascopy — ticks BI5 + widget Trading Breaks | MONDE EXTÉRIEUR | 🟣 `EXTERNE` | `feat/multi-year-dukascopy-acquisition` | NOW · TARGET |
| VT Markets / MT5 — flux d'exécution | MONDE EXTÉRIEUR | 🟣 `EXTERNE` | `main` | NOW · TARGET |
| GitHub Actions | MONDE EXTÉRIEUR | 🟣 `EXTERNE` | `feat/multi-year-dukascopy-acquisition` | NOW · TARGET |
| AI Operating Memory | GOUVERNANCE | 🟢 `EXISTANT` | `main` | NOW · TARGET |
| Recovery Checkpoint | GOUVERNANCE | ⚠️ `AMBIGU` | `main + branches` | NOW · TARGET · GAP |
| Repository Safety Rules | GOUVERNANCE | 🟢 `EXISTANT` | `main` | NOW · TARGET |
| Frontière humaine / décision normative | GOUVERNANCE | 🟢 `EXISTANT` | `main` | NOW · TARGET |
| Experimental Memory Charter | GOUVERNANCE | 🔵 `SPECIFIE` | `main` | NOW · TARGET · GAP |
| 01 — System Vision | CORPUS NORMATIF | 🔵 `SPECIFIE` | `main` | TARGET · GAP |
| 04 — Validation Criteria v0.6.2 | CORPUS NORMATIF | 🟢 `EXISTANT` | `main` | NOW · TARGET |
| 05 — Data Contract v0.1 | CORPUS NORMATIF | ⚠️ `AMBIGU` | `main` | NOW · TARGET · GAP |
| 08 — System Registry + registres 09→14 | CORPUS NORMATIF | 🟡 `PARTIEL` | `main` | NOW · TARGET |
| Qualification Input Register — 10 entrées BLOCKED | CORPUS NORMATIF | 🔴 `MANQUANT` | `main` | NOW · GAP |
| tick_reader | DATA | 🟢 `EXISTANT` | `main` | NOW · TARGET |
| dataset_admissibility | DATA | 🟢 `EXISTANT` | `main` | NOW · TARGET |
| input_binding — capacité BoundResearchInput | DATA | 🟢 `EXISTANT` | `feat/multi-year-dukascopy-acquisition` | NOW · TARGET |
| bi5_reader + contrat d'instrument | DATA | 🟡 `PARTIEL` | `feat/multi-year-dukascopy-acquisition` | NOW · TARGET |
| Sonde V4.3 — compatibilité recherche ↔ exécution | DATA | 🟡 `PARTIEL` | `main + branches` | NOW · TARGET |
| Audit de couverture calendrier | VÉRITÉ TEMPORELLE | 🟢 `EXISTANT` | `feat/multi-year-dukascopy-acquisition` | NOW · TARGET |
| Protocole de récupération des Trading Breaks | VÉRITÉ TEMPORELLE | 🟢 `EXISTANT` | `feat/multi-year-dukascopy-acquisition` | NOW · TARGET |
| Machine à lots — Batches 01 → 11 | VÉRITÉ TEMPORELLE | 🟢 `EXISTANT` | `feat/multi-year-dukascopy-acquisition` | NOW · TARGET |
| Règle du gap irréductible de preuve broker | VÉRITÉ TEMPORELLE | 🟢 `EXISTANT` | `feat/multi-year-dukascopy-acquisition` | NOW · TARGET |
| Sélection et gel de la fenêtre d'exécution | VÉRITÉ TEMPORELLE | 🔴 `MANQUANT` | `feat/multi-year-dukascopy-acquisition` | NOW · TARGET · GAP |
| Context + context_identity | CONTEXTE | 🟡 `PARTIEL` | `feat/decision-producer-contract` | NOW · TARGET |
| ResearchRunEvidence | RECHERCHE / EXPÉRIENCE | 🟡 `PARTIEL` | `feat/decision-producer-contract` | NOW · TARGET |
| Momentum V1 — définition + protocole baseline | RECHERCHE / EXPÉRIENCE | 🔵 `SPECIFIE` | `feat/multi-year-dukascopy-acquisition` | NOW · TARGET · GAP |
| produce_decision — frontière RESEARCH → DECISION | DÉCISION | 🔴 `MANQUANT` | `feat/decision-producer-contract` | NOW · TARGET · GAP |
| Moteur de décision (Context Engine, Router, multi-horizon) | DÉCISION | ⚪ `CIBLE` | `—` | TARGET · GAP |
| Risk Engine + Portfolio Engine | RISQUE / GOUVERNANCE D'EXPOSITION | ⚪ `CIBLE` | `—` | TARGET · GAP |
| Architecture de sortie de position | RISQUE / GOUVERNANCE D'EXPOSITION | 🔵 `SPECIFIE` | `main` | TARGET · GAP |
| Producteur d'action / exécution | ACTION / EXÉCUTION | 🔴 `MANQUANT` | `—` | NOW · TARGET · GAP |
| Observation de résultat / attribution | RÉSULTAT | 🔴 `MANQUANT` | `—` | NOW · TARGET · GAP |
| DecisionTrace | TRACE | 🟡 `PARTIEL` | `feat/decision-producer-contract / feat/synthetic-end-to-end-chain` | NOW · TARGET |
| Chaîne synthétique bout en bout | TRACE | 🟡 `PARTIEL` | `feat/synthetic-end-to-end-chain` | NOW · TARGET |
| Mémoire expérimentale | MÉMOIRE / AUDIT / RÉVISION | 🔵 `SPECIFIE` | `main` | NOW · TARGET · GAP |
| Audit exécutable + boucle de révision | MÉMOIRE / AUDIT / RÉVISION | 🟡 `PARTIEL` | `feat/multi-year-dukascopy-acquisition` | NOW · TARGET |

---

### 4.1 Couche — MONDE EXTÉRIEUR

*Dukascopy, VT Markets/MT5, GitHub Actions*

#### 🟣 Dukascopy — ticks BI5 + widget Trading Breaks

| | |
|---|---|
| **Statut** | `EXTERNE` — DÉPENDANCE EXTERNE |
| **Domaine** | MONDE EXTÉRIEUR |
| **Branche** | `feat/multi-year-dukascopy-acquisition` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Source de recherche : historique tick USATECH.IDX/USD, instrument ID 9016. Et source de vérité des sessions spéciales via le widget Trading Breaks.

**Entrées.** Requêtes HTTP + automatisation navigateur Playwright.

**Sorties.** Fichiers .bi5 horaires ; enregistrements natifs de fermeture.

**Contrat.** Enregistrement positif natif broker à 14 conditions.

**Invariants.**
- —

**Fonctionne si.** Widget accessible et enregistrement attribuable à la date exacte.

**Doit refuser si.** Échec HTTP, timeout, sélecteur absent → BLOCKED, jamais preuve de séance normale.

**Preuves disponibles.**
- Seule dépendance tierce du dépôt avec pytest : playwright.
- Témoin de calibration verrouillé : 2020-02-17 PRESIDENTS_DAY.

**Fichiers GitHub.**
- `tools/probe_dukascopy_trading_breaks_widget.py` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/probe_dukascopy_trading_breaks_widget.py
- `tools/download_dukascopy_tick_corpus.py` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/download_dukascopy_tick_corpus.py

**Manquant / dette.**
- Point de fragilité majeur : un changement d'interface ou de politique côté Dukascopy stoppe la seule voie de production actuelle du système.

#### 🟣 VT Markets / MT5 — flux d'exécution

| | |
|---|---|
| **Statut** | `EXTERNE` — DÉPENDANCE EXTERNE |
| **Domaine** | MONDE EXTÉRIEUR |
| **Branche** | `main` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Flux d'exécution de référence. Frontière observable V4.2 : 2024-12-17T09:38:28+00:00.

**Entrées.** Export MT5 (CSV/Parquet).

**Sorties.** Propriétés comparables au flux de recherche.

**Contrat.** Frontière observable/synchronisée MT5, pas une revendication sur l'historique inaccessible côté broker.

**Invariants.**
- Couverture recherche et couverture exécution restent deux vérités séparées.

**Fonctionne si.** —

**Doit refuser si.** Aucune fusion des deux datasets en historique synthétique.

**Preuves disponibles.**
- Aucun code d'intégration MT5 n'existe. La relation est purement documentaire et statistique via V4.3.

**Fichiers GitHub.**
- `tools/probe_research_execution_compatibility_v4_3.py` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/tools/probe_research_execution_compatibility_v4_3.py

**Manquant / dette.**
- Le passage de la recherche à l'exécution réelle n'a aucun support technique dans le dépôt.

#### 🟣 GitHub Actions

| | |
|---|---|
| **Statut** | `EXTERNE` — DÉPENDANCE EXTERNE |
| **Domaine** | MONDE EXTÉRIEUR |
| **Branche** | `feat/multi-year-dukascopy-acquisition` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Substrat d'exécution des preuves. Chaque qualification est rattachée à un run id, un job id et un commit déclencheur.

**Entrées.** Push sur branches nommées, ou workflow_dispatch.

**Sorties.** Runs, jobs, artefacts avec SHA-256.

**Contrat.** Identité de run conservée dans chaque rapport.

**Invariants.**
- —

**Fonctionne si.** Le workflow se déclenche sur la bonne branche.

**Doit refuser si.** —

**Preuves disponibles.**
- 55 workflows sur la branche active. ZÉRO workflow sur main.
- Les workflows de la chaîne décisionnelle se déclenchent sur des branches précises : un test « exécuté en CI » peut ne jamais tourner sur la branche où il vit.

**Fichiers GitHub.**
- `.github/workflows/trading-breaks-recovery-batch11.yml` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/.github/workflows/trading-breaks-recovery-batch11.yml
- `.github/workflows/research-to-decision-boundary.yml` @ `feat/decision-producer-contract` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/.github/workflows/research-to-decision-boundary.yml

**Manquant / dette.**
- Absence totale de CI sur main : la branche de référence n'a aucune garantie automatique.

---

### 4.2 Couche — GOUVERNANCE

*Mémoire opérationnelle, sécurité dépôt, frontière humaine*

#### 🟢 AI Operating Memory

| | |
|---|---|
| **Statut** | `EXISTANT` — EXISTANT — prouvé |
| **Domaine** | GOUVERNANCE |
| **Branche** | `main` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Mémoire opérationnelle durable. Fixe la hiérarchie des sources de vérité (dépôt > rapports > exécution reproductible > conversation > souvenir de l'IA), les verdicts autorisés PASS/FAIL/BLOCKED, la discipline de preuve et le protocole adversarial.

**Entrées.** Aucune — document normatif consulté avant toute action.

**Sorties.** Règles opposables à tout agent travaillant sur le dépôt.

**Contrat.** Verdicts : PASS / FAIL / BLOCKED uniquement. BLOCKED n'est jamais PASS.

**Invariants.**
- Ne jamais émettre un faux PASS.
- Ne jamais inventer fichier, chemin, hash, branche ou résultat.
- Chaîne durable : Script → Rapport → Verdict → Conclusion → Checkpoint.

**Fonctionne si.** Consulté avant chaque action substantielle.

**Doit refuser si.** Si l'état ne peut être établi depuis GitHub + preuves d'exécution → BLOCKED, pas d'invention.

**Preuves disponibles.**
- Fichier présent sur main et sur la branche active, contenu divergent entre les deux.

**Fichiers GitHub.**
- `04-REFERENCE/AI-OPERATING-MEMORY.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/04-REFERENCE/AI-OPERATING-MEMORY.md

**Manquant / dette.**
- Aucun mécanisme exécutable ne force le respect de ces règles. Conformité purement déclarative.

#### ⚠️ Recovery Checkpoint

| | |
|---|---|
| **Statut** | `AMBIGU` — AMBIGUÏTÉ — à vérifier |
| **Domaine** | GOUVERNANCE |
| **Branche** | `main + branches` |
| **Présent dans les vues** | NOW · TARGET · GAP |

**Rôle.** Point d'entrée de reprise entre conversations : branche active, commit de référence, bloc en cours, verdicts, preuves, exactement une action suivante.

**Entrées.** État vérifié du worktree et de GitHub.

**Sorties.** Un état récupérable sans dépendre de l'historique de conversation.

**Contrat.** Le fichier de main est un index ; il ne surclasse pas un checkpoint de branche plus récent.

**Invariants.**
- Exactement une action suivante gouvernée.
- Ne pas relancer des blocs déjà qualifiés.

**Fonctionne si.** Quand le checkpoint de branche est à jour.

**Doit refuser si.** —

**Preuves disponibles.**
- main pointe vers feat/v4-3-instrument-contracts (B09 BLOCKED).
- Le checkpoint réel se trouve sur feat/multi-year-dukascopy-acquisition, daté du 15/09, Batch 10 clos.

**Fichiers GitHub.**
- `04-REFERENCE/RECOVERY-CHECKPOINT.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/04-REFERENCE/RECOVERY-CHECKPOINT.md
- `04-REFERENCE/RECOVERY-CHECKPOINT.md` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/04-REFERENCE/RECOVERY-CHECKPOINT.md

**Manquant / dette.**
- Contradiction temporelle réelle : l'index de main désigne une branche périmée de 2 jours. Un lecteur qui suit la règle « lire main d'abord » atterrit sur le mauvais état.

#### 🟢 Repository Safety Rules

| | |
|---|---|
| **Statut** | `EXISTANT` — EXISTANT — prouvé |
| **Domaine** | GOUVERNANCE |
| **Branche** | `main` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** RSR-01 à RSR-05 : vérifier l'identité du dépôt avant toute écriture, isolation inter-dépôts, discipline de source de vérité, interdiction de fausse clôture, provenance des règles normatives.

**Entrées.** Toute opération GitHub.

**Sorties.** Autorisation ou BLOCKED — DO NOT WRITE.

**Contrat.** IDENTIFIER DÉPÔT → BRANCHE → COMMIT DE BASE → CHEMIN CIBLE → APPLICABILITÉ → ACTION.

**Invariants.**
- RSR-04 : BLOCKED / TO-PROVE / UNKNOWN ne peuvent être requalifiés en PASS par commodité.

**Fonctionne si.** —

**Doit refuser si.** Toute vérification d'identité échouée bloque l'écriture.

**Preuves disponibles.**
- Document présent, statut VALIDATED.

**Fichiers GitHub.**
- `GOVERNANCE/REPOSITORY-SAFETY-RULES.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/GOVERNANCE/REPOSITORY-SAFETY-RULES.md

**Manquant / dette.**
- Aucune protection de branche GitHub observée qui rendrait ces règles techniquement opposables.

#### 🟢 Frontière humaine / décision normative

| | |
|---|---|
| **Statut** | `EXISTANT` — EXISTANT — prouvé |
| **Domaine** | GOUVERNANCE |
| **Branche** | `main` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Sépare objectif final, investigation technique, vérification adversariale et décision normative humaine. Impose de ne jamais demander à l'humain d'improviser une réponse technique.

**Entrées.** Question architecturale consequente.

**Sorties.** Brief de décision, ou exécution autonome si l'évidence détermine le choix.

**Contrat.** Protocole 3 voies : analyse interne + Claude indépendant + Grok indépendant → comparaison adversariale → décision humaine → persistance en gouvernance.

**Invariants.**
- Ne pas optimiser pour confirmer une réponse plausible ; chercher activement où le raisonnement est faux.

**Fonctionne si.** Quand une contre-expertise indépendante est disponible.

**Doit refuser si.** Si une ambiguïté normative subsiste sans autorité suffisante, le flux s'arrête et passe en adjudication humaine.

**Preuves disponibles.**
- Nombreux documents ADJUDICATION-* et COUNTER-EXPERTISE-* dans docs/ attestent que le protocole a réellement tourné.

**Fichiers GitHub.**
- `GOVERNANCE/DECISION-SUPPORT-AND-HUMAN-BOUNDARY.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/GOVERNANCE/DECISION-SUPPORT-AND-HUMAN-BOUNDARY.md

**Manquant / dette.**
- —

#### 🔵 Experimental Memory Charter

| | |
|---|---|
| **Statut** | `SPECIFIE` — SPÉCIFIÉ, non implémenté |
| **Domaine** | GOUVERNANCE |
| **Branche** | `main` |
| **Présent dans les vues** | NOW · TARGET · GAP |

**Rôle.** Charte de la mémoire expérimentale : conserver hypothèses, expériences, échecs, corrections et raisons de rejet, pas seulement les résultats.

**Entrées.** —

**Sorties.** —

**Contrat.** —

**Invariants.**
- —

**Fonctionne si.** —

**Doit refuser si.** —

**Preuves disponibles.**
- Le dépôt lui-même qualifie cette brique de « spécification réservée, pas d'implémentation » dans STEP-3-REAL-SYSTEM-MAPPING.

**Fichiers GitHub.**
- `GOVERNANCE/EXPERIMENTAL-MEMORY-CHARTER.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/GOVERNANCE/EXPERIMENTAL-MEMORY-CHARTER.md

**Manquant / dette.**
- Aucun stockage, schéma ou module de mémoire expérimentale n'existe dans src/ sur aucune branche.

---

### 4.3 Couche — CORPUS NORMATIF

*Vision, critères de validation, contrats, registres, adjudications*

#### 🔵 01 — System Vision

| | |
|---|---|
| **Statut** | `SPECIFIE` — SPÉCIFIÉ, non implémenté |
| **Domaine** | CORPUS NORMATIF |
| **Branche** | `main` |
| **Présent dans les vues** | TARGET · GAP |

**Rôle.** Document fondateur. Décrit l'architecture cible complète : Data Engine, Asset Profile Database, Context Engine, 3 experts (Momentum / Mean Reversion / Breakout), Expert Router, multi-horizon 15m/1h/4h, Risk Engine, Portfolio Engine, Execution Engine, attribution, surveillance, Champion/Challenger.

**Entrées.** —

**Sorties.** La définition de TARGET utilisée par cette carte.

**Contrat.** Règle d'or : toute fonctionnalité doit répondre « où s'intègre-t-elle ? » et « quel problème mesurable résout-elle ? ».

**Invariants.**
- Robustesse > sophistication.
- Contrôle > autonomie.
- Ne pas trader est une décision valide.
- Pas de réentraînement libre en production.

**Fonctionne si.** —

**Doit refuser si.** —

**Preuves disponibles.**
- Aucun des moteurs décrits (Context, Router, Risk, Portfolio, Execution) n'a de code correspondant dans src/ sur aucune branche. Vérifié par recherche exhaustive.

**Fichiers GitHub.**
- `docs/01-SYSTEM-VISION.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/01-SYSTEM-VISION.md

**Manquant / dette.**
- Écart maximal du dépôt : ce document décrit ~10 moteurs, zéro est implémenté.

#### 🟢 04 — Validation Criteria v0.6.2

| | |
|---|---|
| **Statut** | `EXISTANT` — EXISTANT — prouvé |
| **Domaine** | CORPUS NORMATIF |
| **Branche** | `main` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Référence méthodologique de validation : niveaux de preuve N0–N4, statut probatoire du juge, conditions de validation/promotion, budget N, correction de multiplicité.

**Entrées.** Candidat de recherche.

**Sorties.** Conditions de promotion.

**Contrat.** Autorité haute, candidat au gel.

**Invariants.**
- §5.3 c.4 (coûts complets) a été rétrogradée de BLOQUANTE à SUSPENDUE pour lever la contradiction CTR-01.

**Fonctionne si.** —

**Doit refuser si.** —

**Preuves disponibles.**
- 62 Ko, plus gros document du corpus. Re-test CTR-01 : PASS documenté dans 14-AUDIT-PHASE-A-STATUS.

**Fichiers GitHub.**
- `docs/04-VALIDATION-CRITERIA.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/04-VALIDATION-CRITERIA.md
- `docs/14-AUDIT-PHASE-A-STATUS.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/14-AUDIT-PHASE-A-STATUS.md

**Manquant / dette.**
- CTR-01 a été clos en suspendant la condition, pas en résolvant la dépendance vers 05. La dette est parquée, pas payée.

#### ⚠️ 05 — Data Contract v0.1

| | |
|---|---|
| **Statut** | `AMBIGU` — AMBIGUÏTÉ — à vérifier |
| **Domaine** | CORPUS NORMATIF |
| **Branche** | `main` |
| **Présent dans les vues** | NOW · TARGET · GAP |

**Rôle.** Contrat de données proposé : continuité temporelle, rapport de couverture, identité et parenté de dataset, convention temporelle par instrument, parité entre implémentations, format canonique, modèle de coûts.

**Entrées.** —

**Sorties.** 8 concepts CON-006 à CON-013.

**Contrat.** Statut explicite : proposition, aucune règle en vigueur.

**Invariants.**
- 08-SYSTEM-REGISTRY l'enregistre comme « Définiteur proposé », jamais comme autorité normative.

**Fonctionne si.** —

**Doit refuser si.** Aucune brique ne peut invoquer 05 comme règle opposable.

**Preuves disponibles.**
- Contradictions C-02 et CTR-01/CTR-02 tracées dans 08 et 14.

**Fichiers GitHub.**
- `docs/05-DATA-CONTRACT.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/05-DATA-CONTRACT.md
- `docs/08-SYSTEM-REGISTRY.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/08-SYSTEM-REGISTRY.md

**Manquant / dette.**
- Le document le plus structurant pour la couche DATA n'a toujours aucune autorité normative, alors que du code exécutable (dataset_admissibility) implémente déjà de facto certaines de ses idées.

#### 🟡 08 — System Registry + registres 09→14

| | |
|---|---|
| **Statut** | `PARTIEL` — PARTIEL |
| **Domaine** | CORPUS NORMATIF |
| **Branche** | `main` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Cartographie d'ownership : définiteur / définiteur proposé / producteur / dépositaire / consommateur, plus registre d'interfaces IF-001 à IF-006, criticité C1/C2/C3 et 6 contradictions C-01 à C-06.

**Entrées.** Documents du corpus.

**Sorties.** Qui possède la sémantique de quel concept.

**Contrat.** Produire une donnée ne donne jamais le droit d'en redéfinir la sémantique.

**Invariants.**
- Aucune nouvelle brique normative intégrée sans la fiche en 15 points du §10.

**Fonctionne si.** —

**Doit refuser si.** —

**Preuves disponibles.**
- 08 v0.2 marque explicitement comme lacunes : registry de datasets, Asset Profile canonique, registre de contradictions, registre d'arbitrages.

**Fichiers GitHub.**
- `docs/08-SYSTEM-REGISTRY.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/08-SYSTEM-REGISTRY.md
- `docs/09-DATASET-PROVENANCE-REGISTRY.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/09-DATASET-PROVENANCE-REGISTRY.md
- `docs/10-TEMPORAL-POINT-IN-TIME-CONTRACT.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/10-TEMPORAL-POINT-IN-TIME-CONTRACT.md
- `docs/11-CONTRADICTION-ARBITRATION-REGISTRY.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/11-CONTRADICTION-ARBITRATION-REGISTRY.md
- `docs/13-CRITICALITY-AUDIT-PROTOCOL.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/13-CRITICALITY-AUDIT-PROTOCOL.md

**Manquant / dette.**
- C-04 bitemporalité (valide_du / valide_au / connu_depuis) enregistrée comme besoin architectural, pas comme contrat.
- C-05 registre de contradictions et C-06 contestation ascendante : proposés en v0.1, jamais rendus exécutables.

#### 🔴 Qualification Input Register — 10 entrées BLOCKED

| | |
|---|---|
| **Statut** | `MANQUANT` — MANQUANT / BLOCAGE |
| **Domaine** | CORPUS NORMATIF |
| **Branche** | `main` |
| **Présent dans les vues** | NOW · GAP |

**Rôle.** Inventaire auditable des entrées concrètes exigées par le gate exécutable global RB-A → Q-RM-12.

**Entrées.** Décisions normatives du projet.

**Sorties.** Ouverture ou non du gate global.

**Contrat.** D+R+M → B+A → Q → F+O → I_A+I_B → exécution réelle → Universe(A)=Universe(B) → variantes adversariales → PASS.

**Invariants.**
- Aucune représentation (CSV, JSON, Parquet, binaire) n'est sélectionnée par ce registre.
- Le hash de fichier n'est pas une identité d'occurrence.
- L'index physique de ligne n'est pas une identité d'occurrence.

**Fonctionne si.** —

**Doit refuser si.** Tout prérequis manquant maintient le gate BLOCKED. Un cas adversarial en échec donne FAIL, jamais converti en PASS en changeant le résultat attendu après observation.

**Preuves disponibles.**
- Les 10 entrées D, R, M, B, A, Q, F, O, I_A, I_B sont toutes marquées BLOCKED.

**Fichiers GitHub.**
- `docs/QUALIFICATION-INPUT-REGISTER-V1-BLOCKED.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/QUALIFICATION-INPUT-REGISTER-V1-BLOCKED.md
- `docs/ADJUDICATION-GLOBAL-EXECUTABLE-GATE-RB-A-Q-RM-01-12-V1-2026-09-05.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/ADJUDICATION-GLOBAL-EXECUTABLE-GATE-RB-A-Q-RM-01-12-V1-2026-09-05.md

**Manquant / dette.**
- Environ 50 documents ADJUDICATION-* ferment la sémantique universelle du modèle d'enregistrement, mais aucune entrée concrète n'est fermée. Le travail sémantique est terminé ; le travail concret n'a pas commencé.

---

### 4.4 Couche — DATA

*Identité des octets, admissibilité, lecture BI5, liaison de corpus*

#### 🟢 tick_reader

| | |
|---|---|
| **Statut** | `EXISTANT` — EXISTANT — prouvé |
| **Domaine** | DATA |
| **Branche** | `main` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Lecteur minimal de CSV de ticks. Ne trie pas, ne déduplique pas, ne répare pas, ne normalise pas. Préserve l'ordre source via read_index.

**Entrées.** CSV, en-tête exact timestamp,askPrice,bidPrice,askVolume,bidVolume.

**Sorties.** Itérateur de Tick(Decimal…, read_index).

**Contrat.** EXPECTED_COLUMNS figé. Tout autre en-tête lève ValueError.

**Invariants.**
- Aucune transformation silencieuse de la source.
- Prix en Decimal, jamais float, à la lecture.

**Fonctionne si.** En-tête exact, toutes colonnes présentes.

**Doit refuser si.** En-tête absent, en-tête différent, ligne malformée.

**Preuves disponibles.**
- 4 tests. Rejoués localement : verts.
- Test test_repeated_reads_are_identical prouve le déterminisme de lecture.

**Fichiers GitHub.**
- `src/data/tick_reader.py` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/src/data/tick_reader.py
- `tests/test_tick_reader.py` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/tests/test_tick_reader.py

**Manquant / dette.**
- —

#### 🟢 dataset_admissibility

| | |
|---|---|
| **Statut** | `EXISTANT` — EXISTANT — prouvé |
| **Domaine** | DATA |
| **Branche** | `main` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Frontière d'identité et d'admissibilité du dataset. Identifie les octets source exacts par SHA-256 et rend un verdict sans modifier la source.

**Entrées.** Chemin CSV + DatasetIdentity déclarée (dataset_id, version, content_hash, format, schema_version, instrument, granularité, timezone_storage).

**Sorties.** DatasetAdmissibilityReport : 6 contrôles + verdict PASS / FAIL / BLOCKED / UNVERIFIED.

**Contrat.** Contrôles : content_hash, schema, row_shape, timestamp, numeric_domain, quote_integrity, ordering.

**Invariants.**
- Les octets doivent correspondre au content_hash déclaré.
- Timestamps ISO-8601 obligatoirement timezone-aware.
- ask ≥ bid sur chaque ligne.
- Timestamps non décroissants.
- Précédence : BLOCKED > FAIL > UNVERIFIED > PASS.

**Fonctionne si.** Fichier accessible, hash conforme, schéma exact.

**Doit refuser si.** Octets modifiés après déclaration → FAIL. Timestamp naïf → FAIL. ask < bid → FAIL. Source inaccessible → BLOCKED.

**Preuves disponibles.**
- 9 tests dont 5 cas négatifs paramétrés. Rejoués localement : verts.
- C'est la seule frontière du système à la fois exécutable, testée négativement et présente sur main.

**Fichiers GitHub.**
- `src/data/dataset_admissibility.py` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/src/data/dataset_admissibility.py
- `tests/test_dataset_admissibility.py` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/tests/test_dataset_admissibility.py

**Manquant / dette.**
- —

#### 🟢 input_binding — capacité BoundResearchInput

| | |
|---|---|
| **Statut** | `EXISTANT` — EXISTANT — prouvé |
| **Domaine** | DATA |
| **Branche** | `feat/multi-year-dukascopy-acquisition` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Frontière de liaison du corpus de recherche. Vérifie l'identité du corpus et du contrat AVANT d'exposer la capacité au moteur.

**Entrées.** corpus_root, contract_path, hash attendu du corpus, hash attendu du contrat.

**Sorties.** BoundResearchInput — objet-capacité non constructible directement.

**Contrat.** BoundResearchInput.__init__ refuse toute création hors de bind_execution_input() via un jeton _BOUND_INPUT_CAPABILITY privé au module.

**Invariants.**
- Hash d'inventaire = SHA-256 des lignes chemin/taille/hash triées, pas un hash de concaténation naïve.
- L'identité est vérifiée avant exposition, pas après.

**Fonctionne si.** Corpus et contrat conformes aux hashes attendus.

**Doit refuser si.** TypeError si un appelant tente d'instancier la capacité lui-même.

**Preuves disponibles.**
- Le motif le plus solide du dépôt. C'est la référence à généraliser aux autres frontières.

**Fichiers GitHub.**
- `src/research/input_binding.py` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/src/research/input_binding.py
- `src/research/engine.py` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/src/research/engine.py
- `src/research/execution.py` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/src/research/execution.py

**Manquant / dette.**
- Vit uniquement sur branche. Non fusionné dans main.

#### 🟡 bi5_reader + contrat d'instrument

| | |
|---|---|
| **Statut** | `PARTIEL` — PARTIEL |
| **Domaine** | DATA |
| **Branche** | `feat/multi-year-dukascopy-acquisition` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Décodage des ticks Dukascopy BI5 (LZMA, enregistrements 20 octets >IIIff) piloté par un contrat d'instrument versionné, jamais par des constantes en dur.

**Entrées.** Fichier .bi5 horaire + USATECHIDXUSD-Dukascopy-BI5.json (record_size 20, struct >IIIff, unité ms, price_scale 1000).

**Sorties.** Flux de Tick monotone, plus stream_sha256 déterministe au niveau exécution.

**Contrat.** record_size doit égaler struct.calcsize(record_struct). timestamp_unit autre que millisecondes → rejet.

**Invariants.**
- Un tick hors de son heure déclarée lève une erreur.
- Flux global non monotone → erreur.
- Heure dupliquée dans le corpus → erreur.

**Fonctionne si.** Contrat d'instrument présent et cohérent.

**Doit refuser si.** Payload non aligné, prix non finis, ask < bid, volume négatif, heure dupliquée.

**Preuves disponibles.**
- En-tête explicite du module : « RECONSTRUCTION != RECOVERY ». L'implémentation historique originale n'a pas été récupérable depuis l'historique GitHub accessible.

**Fichiers GitHub.**
- `src/research/bi5_reader.py` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/src/research/bi5_reader.py
- `docs/04-REFERENCE/INSTRUMENT-CONTRACTS/USATECHIDXUSD-Dukascopy-BI5.json` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/docs/04-REFERENCE/INSTRUMENT-CONTRACTS/USATECHIDXUSD-Dukascopy-BI5.json
- `tests/test_instrument_contract_v4_3.py` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tests/test_instrument_contract_v4_3.py

**Manquant / dette.**
- Le dépôt reconnaît lui-même qu'il ne peut pas prouver l'identité octet-pour-octet avec l'implémentation perdue. Toute preuve antérieure produite par l'ancien lecteur est donc non reconductible telle quelle.

#### 🟡 Sonde V4.3 — compatibilité recherche ↔ exécution

| | |
|---|---|
| **Statut** | `PARTIEL` — PARTIEL |
| **Domaine** | DATA |
| **Branche** | `main + branches` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Compare les propriétés transférables de deux flux indépendants (Dukascopy recherche vs VT Markets exécution) sans prétendre qu'ils doivent être identiques tick par tick.

**Entrées.** Répertoires CSV / BI5 / Parquet.

**Sorties.** Rapport JSON : RESEARCH_DATA_VALID, EXECUTION_DATA_VALID, TRANSFER_VALIDATION, ratios de spread et de rendements horaires.

**Contrat.** Lecture seule. Précédence BLOCKED > FAIL > UNVERIFIED > PASS. Minimum 5 ans de recherche.

**Invariants.**
- Aucun dataset n'est fusionné ou raccordé en historique synthétique.
- Aucun fuseau horaire n'est deviné pour un timestamp Parquet naïf.
- Aucun seuil d'équivalence statistique n'est inventé.

**Fonctionne si.** Sources accessibles et sémantique temporelle explicite.

**Doit refuser si.** Timestamp Parquet naïf sans --naive-timezone → BLOCKED. TRANSFER_VALIDATION reste UNVERIFIED tant qu'aucun critère d'acceptation n'est gelé.

**Preuves disponibles.**
- Le code force structurellement equivalence_thresholds à UNVERIFIED — le système refuse de conclure au transfert.

**Fichiers GitHub.**
- `tools/probe_research_execution_compatibility_v4_3.py` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/tools/probe_research_execution_compatibility_v4_3.py

**Manquant / dette.**
- Aucun seuil d'équivalence de transfert n'est défini. La question « le backtest Dukascopy prédit-il l'exécution VT Markets ? » reste structurellement sans réponse.

---

### 4.5 Couche — VÉRITÉ TEMPORELLE

*Calendrier de sessions, récupération broker, fenêtre d'exécution*

#### 🟢 Audit de couverture calendrier

| | |
|---|---|
| **Statut** | `EXISTANT` — EXISTANT — prouvé |
| **Domaine** | VÉRITÉ TEMPORELLE |
| **Branche** | `feat/multi-year-dukascopy-acquisition` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Énumère les dates candidates de session spéciale sur l'enveloppe 2018-05-01 → 2026-08-14 et réconcilie résolu / non résolu / orphelin / contradictoire.

**Entrées.** Générateur de candidats versionné candidate_special_dates().

**Sorties.** 111 candidats · 60 résolus · 51 non résolus · 0 orphelin · 0 contradiction · verdict BLOCKED.

**Contrat.** DUKASCOPY_USATECH_SPECIAL_SESSION_COVERAGE_V1.

**Invariants.**
- execution_window_frozen = False.
- BLOCKED ne résout jamais un candidat.

**Fonctionne si.** —

**Doit refuser si.** Verdict BLOCKED tant que SPECIAL_SESSION_EVIDENCE_COVERAGE_INCOMPLETE.

**Preuves disponibles.**
- Chiffres régénérés en exécutant l'outil localement : 111/60/51, verdict BLOCKED. Concordance exacte avec le checkpoint du 15/09.

**Fichiers GitHub.**
- `tools/dukascopy_usatech_calendar_coverage.py` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/dukascopy_usatech_calendar_coverage.py
- `tools/dukascopy_usatech_calendar.py` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/dukascopy_usatech_calendar.py
- `reports/data-qualification/dukascopy_usatech_global_calendar_coverage_audit.md` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/reports/data-qualification/dukascopy_usatech_global_calendar_coverage_audit.md

**Manquant / dette.**
- Le rapport Markdown persisté annonce 24 résolus / 87 non résolus : c'est un instantané daté, dépassé par l'outil. Les rapports figés se périment sans signalement.

#### 🟢 Protocole de récupération des Trading Breaks

| | |
|---|---|
| **Statut** | `EXISTANT` — EXISTANT — prouvé |
| **Domaine** | VÉRITÉ TEMPORELLE |
| **Branche** | `feat/multi-year-dukascopy-acquisition` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Seule procédure systématique admissible pour appliquer la route Dukascopy Trading Breaks aux candidats non résolus. PASS — rejette les contournements connus.

**Entrées.** File de récupération = candidats dans la fenêtre − déjà résolus, triés strictement par date croissante.

**Sorties.** Verdict au niveau de la date, jamais au niveau du lot.

**Contrat.** HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1. Contrat de preuve positive à 14 conditions.

**Invariants.**
- Adressage à la date exacte : jamais une date adjacente, le même jour férié d'une autre année, ni une plage non attribuable.
- Une réponse vide, un échec HTTP, un timeout ou un enregistrement d'un autre instrument NE sont PAS une preuve de séance normale.
- Sémantique calibrée : start = première minute fermée, end = dernière minute fermée, reopen = end + 60 s.
- Une heure UTC n'est émise fermée que si ses 60 minutes sont dans l'intervalle fermé.

**Fonctionne si.** Enregistrement positif natif broker, instrument 9016, USATECH.IDX/USD, provenance complète.

**Doit refuser si.** Emprunt d'enregistrement d'une autre date ou année, preuve par nom de jour férié, horaires de bourse pris pour vérité broker, promotion de tout un lot parce qu'un pilote a réussi, inférence par nombre de sources.

**Preuves disponibles.**
- Run GitHub Actions 34880921889, job 104099717727, 20 tests verts.
- Attaques exécutées : intégrité de file gelée, cibles hors fenêtre, réintroduction de date résolue, mismatch de date et d'instrument, promotion de no-record, payload absent, intervalles négatifs, dates adjacentes, contradiction DOM, provenance manquante, hash invalide, arrondi d'heure partielle.

**Fichiers GitHub.**
- `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md
- `tools/trading_breaks_recovery_protocol.py` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/trading_breaks_recovery_protocol.py
- `tests/test_trading_breaks_recovery_protocol.py` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tests/test_trading_breaks_recovery_protocol.py

**Manquant / dette.**
- Le contrat de preuve négative n'existe pas : l'absence ne peut pas encore prouver des horaires réguliers. C'est pourquoi 51 dates restent non résolues.

#### 🟢 Machine à lots — Batches 01 → 11

| | |
|---|---|
| **Statut** | `EXISTANT` — EXISTANT — prouvé |
| **Domaine** | VÉRITÉ TEMPORELLE |
| **Branche** | `feat/multi-year-dukascopy-acquisition` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Boucle de production gouvernée. Pour chaque lot : gel mécanique depuis la file éligible → qualification adversariale de l'appartenance → capture navigateur → adjudication hors-ligne indépendante → intégration atomique → re-cassage du HEAD persisté.

**Entrées.** eligible_recovery_queue()[:5], figé avant toute observation.

**Sorties.** Preuve calendrier exécutable + rapports + entrées au ledger de tentatives.

**Contrat.** Un lot est gelé avant observation. Taille fixe 5. HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1 empêche les dates déjà tentées d'affamer les suivantes.

**Invariants.**
- Trois états séparés : preuve calendrier / historique des tentatives / capacité de preuve.
- Une tentative BLOCKED ne devient jamais un candidat résolu.
- Les tentatives historiques sont des faits et ne sont jamais supprimées.

**Fonctionne si.** File éligible non vide et capacité de preuve inchangée.

**Doit refuser si.** S'arrête sur FAIL sémantique réel, changement de capacité requis, contradiction nécessitant un jugement humain, ou épuisement de la file éligible.

**Preuves disponibles.**
- 55 workflows GitHub Actions, 89 rapports, 47 sauvegardes de session.
- Batch 10 : intégration atomique PASS, re-cassage HEAD persisté PASS, run 35008589674.
- Batch 11 gelé mécaniquement : 2025-05-26, 2025-06-19, 2025-07-03, 2025-07-04, 2025-09-01.
- Ledger de tentatives : 50 entrées. 13 BLOCKED à capacité identique. 18 éligibles non résolues.

**Fichiers GitHub.**
- `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md
- `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH11-POLICY.md` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH11-POLICY.md
- `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json

**Manquant / dette.**
- Chaque lot génère 4 à 5 workflows dédiés jetables. 55 workflows pour 11 lots : le coût marginal par lot ne décroît pas.

#### 🟢 Règle du gap irréductible de preuve broker

| | |
|---|---|
| **Statut** | `EXISTANT` — EXISTANT — prouvé |
| **Domaine** | VÉRITÉ TEMPORELLE |
| **Branche** | `feat/multi-year-dukascopy-acquisition` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Gouverne le cas où la récupération exhaustive ne peut pas retrouver le témoin broker d'origine. Empêche à la fois le faux PASS par preuve plausible mais non équivalente, et la boucle de recherche infinie.

**Entrées.** Date, instrument et fait cibles explicitement identifiés, récupération primaire et archive déjà tentées et tracées.

**Sorties.** PASS par chaîne de preuve suffisante, ou BLOCKED.

**Contrat.** IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1. Classes B0 / B1 / B2 / B3 / X0 / X1.

**Invariants.**
- B0 témoin broker primaire exact et B1 témoin archivé exact suffisent seuls.
- B2 seul ne suffit pas.
- La similarité d'horaires réguliers n'est pas un mapping B3.
- La coïncidence historique répétée n'est pas un mapping B3.

**Fonctionne si.** Récupération matériellement épuisée et provenance vérifiable.

**Doit refuser si.** Si la récupération n'est pas épuisée → BLOCKED — RETRIEVAL_INCOMPLETE. Un gap irréductible maintient la couverture globale BLOCKED.

**Preuves disponibles.**
- Règle invoquée et testée : tests/test_irreducible_historical_broker_evidence_gap.py.

**Fichiers GitHub.**
- `04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md
- `tools/irreducible_historical_broker_evidence_gap.py` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/irreducible_historical_broker_evidence_gap.py

**Manquant / dette.**
- —

#### 🔴 Sélection et gel de la fenêtre d'exécution

| | |
|---|---|
| **Statut** | `MANQUANT` — MANQUANT / BLOCAGE |
| **Domaine** | VÉRITÉ TEMPORELLE |
| **Branche** | `feat/multi-year-dukascopy-acquisition` |
| **Présent dans les vues** | NOW · TARGET · GAP |

**Rôle.** Sépare quatre revendications à ne jamais confondre : poursuivre la qualification, déclarer la couverture complète, geler une fenêtre d'exécution ≥ 5 ans, autoriser l'acquisition massive.

**Entrées.** coverage_start, coverage_end, horizon minimum 5 ans.

**Sorties.** Candidat de fenêtre 2021-08-14 → 2026-08-14. Gel : BLOCKED.

**Contrat.** COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1 actions A/B/C/D. EXECUTION_WINDOW_SELECTION_RULE_V1.

**Invariants.**
- Entrées interdites à la sélection : dates non résolues, dates FAIL, distribution des trous, disponibilité des ticks, PnL/drawdown/win rate, coûts, connaissance des dates faciles à prouver.
- « Commencer en 2020 parce que 2019-07-03 est BLOCKED » est explicitement invalide.
- La fenêtre ne doit pas être déplacée, raccourcie ou étendue pour réduire le compte de non résolues.

**Fonctionne si.** —

**Doit refuser si.** Gel BLOCKED tant que les non résolues dans la fenêtre ≠ 0. Actuellement 31 non résolues sur 68 candidats en fenêtre. Fenêtre cherry-pickée ou < 5 ans → FAIL.

**Preuves disponibles.**
- Comptabilité fenêtre vérifiée au checkpoint : 68 candidats / 37 résolus / 31 non résolus / 0 FAIL.

**Fichiers GitHub.**
- `04-REFERENCE/EXECUTION-WINDOW-SELECTION-RULE.md` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/04-REFERENCE/EXECUTION-WINDOW-SELECTION-RULE.md
- `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md
- `tools/coverage_execution_window_boundary.py` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/coverage_execution_window_boundary.py

**Manquant / dette.**
- C'est le goulot d'étranglement principal du projet. 31 dates séparent le système de l'autorisation d'acquisition, donc du premier backtest réel.

---

### 4.6 Couche — CONTEXTE

*Identité déterministe du contexte d'observation*

#### 🟡 Context + context_identity

| | |
|---|---|
| **Statut** | `PARTIEL` — PARTIEL |
| **Domaine** | CONTEXTE |
| **Branche** | `feat/decision-producer-contract` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Objet CONTEXTE à la frontière DATA → CONTEXT. Décrit la donnée et la configuration pertinentes pour une observation. Ne contient aucune décision, action, résultat ni information dérivée du futur.

**Entrées.** DatasetIdentity + configuration_version + bornes d'observation explicites.

**Sorties.** Context avec context_id = CTX- + SHA-256 sur 7 champs d'identité.

**Contrat.** Identité déterministe sur dataset_id, dataset_version, content_hash, instrument, granularity, timezone_storage, configuration_version.

**Invariants.**
- observation_start et observation_end ne font PAS partie de l'identité et ne doivent pas y être ajoutés implicitement.
- validate_context recalcule l'identité et la confronte au dataset fourni.

**Fonctionne si.** Dataset identifié et configuration explicite.

**Doit refuser si.** Identité recalculée divergente → rejet.

**Preuves disponibles.**
- Tests test_data_to_context.py verts localement.
- Workflow data-to-context.yml existe, mais ne se déclenche que sur push vers feat/step3-system-mapping et feat/step3-context-research-contract-gate.

**Fichiers GitHub.**
- `src/context.py` @ `feat/decision-producer-contract` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/src/context.py
- `src/context_identity.py` @ `feat/decision-producer-contract` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/src/context_identity.py
- `tests/test_data_to_context.py` @ `feat/decision-producer-contract` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/tests/test_data_to_context.py

**Manquant / dette.**
- Absent de main. Le dépôt lui-même classe CONTEXTE en BLOCKED dans STEP-3-REAL-SYSTEM-MAPPING.

---

### 4.7 Couche — RECHERCHE / EXPÉRIENCE

*Preuve de run, contrat de findings, expert Momentum V1*

#### 🟡 ResearchRunEvidence

| | |
|---|---|
| **Statut** | `PARTIEL` — PARTIEL |
| **Domaine** | RECHERCHE / EXPÉRIENCE |
| **Branche** | `feat/decision-producer-contract` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Adaptateur du rapport V4.3 existant vers la traçabilité de décision. Dérive des identifiants stables depuis le rapport et les hashes des fichiers source, puis valide la frontière CONTEXT.

**Entrées.** Rapport V4.3 + code_version + Context + DatasetIdentity.

**Sorties.** provenance_id, research_run_id, code_version, configuration_version, dataset_id, dataset_version, context_id.

**Contrat.** Schéma du rapport obligatoirement RESEARCH_EXECUTION_COMPATIBILITY_V4_3.

**Invariants.**
- Rapport sans hashes immuables de fichiers source → rejet.
- Le contrôle de frontière a lieu à l'entrée de RESEARCH, pas plus tard dans la trace.

**Fonctionne si.** Rapport V4.3 réel avec hashes, Context cohérent, configuration concordante.

**Doit refuser si.** Schéma inconnu, hashes absents, Context absent ou incohérent, configuration divergente, identité de rapport divergente.

**Preuves disponibles.**
- Tests test_context_to_research_boundary.py verts localement.

**Fichiers GitHub.**
- `src/research_run_evidence.py` @ `feat/decision-producer-contract` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/src/research_run_evidence.py
- `docs/RESEARCH-FINDINGS-CONTRACT.md` @ `feat/decision-producer-contract` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/docs/RESEARCH-FINDINGS-CONTRACT.md

**Manquant / dette.**
- N'est pas raccordé au moteur de recherche réel. Il adapte un rapport de compatibilité de données, pas une expérience de trading.

#### 🔵 Momentum V1 — définition + protocole baseline

| | |
|---|---|
| **Statut** | `SPECIFIE` — SPÉCIFIÉ, non implémenté |
| **Domaine** | RECHERCHE / EXPÉRIENCE |
| **Branche** | `feat/multi-year-dukascopy-acquisition` |
| **Présent dans les vues** | NOW · TARGET · GAP |

**Rôle.** Premier expert défini : H1, Close, horizon 20 barres, M_t = Close_t / Close_t-20 − 1. M>0 LONG, M<0 SHORT, M=0 NEUTRE, historique insuffisant UNDEFINED. Signal calculé à la clôture de t, utilisable à partir de t+1.

**Entrées.** Séries H1 construites depuis des ticks admissibles.

**Sorties.** Signal directionnel — pas une transaction.

**Contrat.** 3.1.1 PASS sur la définition. 3.1.2 PASS sur le protocole, après cassage et re-cassage.

**Invariants.**
- Aucune donnée future.
- Aucun filtre de régime.
- Aucune optimisation du paramètre 20.
- Signal ≠ ordre.
- Harness de sortie gelé AVANT exécution pour empêcher d'inventer une règle de sortie après avoir vu les résultats.

**Fonctionne si.** —

**Doit refuser si.** Le gate de recherche exige au moins 5 ans. Le corpus B05 de janvier 2025 fait un mois et ne peut pas satisfaire ce gate. Aucune extension synthétique, mois copié, interpolation ou substitution silencieuse n'est autorisée.

**Preuves disponibles.**
- Les deux PASS portent exclusivement sur la définition et le protocole. Aucun PASS de performance, de robustesse ou de valeur économique.
- Aucun fichier Python n'implémente ce calcul dans src/ sur aucune branche — vérifié.

**Fichiers GitHub.**
- `docs/03.1.1-MOMENTUM-V1-DEFINITION.md` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/docs/03.1.1-MOMENTUM-V1-DEFINITION.md
- `docs/03.1.2-MOMENTUM-V1-BASELINE-PROTOCOL.md` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/docs/03.1.2-MOMENTUM-V1-BASELINE-PROTOCOL.md
- `reports/research/3_1_2_momentum_v1_baseline_adversarial_report.md` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/reports/research/3_1_2_momentum_v1_baseline_adversarial_report.md

**Manquant / dette.**
- Le plus petit maillon manquant du système : la définition et le protocole sont gelés, l'implémentation n'existe pas.

---

### 4.8 Couche — DÉCISION

*Contrat producteur, moteur de décision*

#### 🔴 produce_decision — frontière RESEARCH → DECISION

| | |
|---|---|
| **Statut** | `MANQUANT` — MANQUANT / BLOCAGE |
| **Domaine** | DÉCISION |
| **Branche** | `feat/decision-producer-contract` |
| **Présent dans les vues** | NOW · TARGET · GAP |

**Rôle.** Produit une Decision à partir d'une preuve de recherche et du contexte qui l'a produite. Le contenu de la décision est une ENTRÉE, pas une logique de trading : le module n'invente délibérément aucune règle.

**Entrées.** ResearchRunEvidence + Context + chaîne de décision fournie par l'appelant.

**Sorties.** Decision(decision_id = DEC- + SHA-256 tronqué, research_run_id, context_id, decision).

**Contrat.** Exige une preuve produite par la fabrique V4.3, plus concordance de context_id, configuration_version, dataset_id, dataset_version, provenance_id, research_run_id et code_version.

**Invariants.**
- Aucun moteur de décision n'existe. Ce module ferme un contrat de traçabilité, pas une logique.

**Fonctionne si.** Preuve issue de from_v43_report() et contexte concordant.

**Doit refuser si.** Preuve absente, mauvais type, contexte absent, mismatch d'identité, décision vide.

**Preuves disponibles.**
- CASSAGE VÉRIFIÉ PAR MOI : le garde-fou repose sur un attribut booléen privé _factory_validated. J'ai construit une ResearchRunEvidence forgée, posé object.__setattr__(evidence,'_factory_validated',True) et obtenu une Decision valide avec research_run_id='RUN-forged' et code_version='attacker'. La frontière est contournable.
- 2 tests rouges sur cette branche : test_c1_forged_context_id_is_rejected et test_c2_empty_research_run_id_is_rejected attendent d'anciens messages d'erreur.
- Sur audit/pre-backtest-freeze, la version SANS correctif est encore présente et 3 tests adversariaux échouent.

**Fichiers GitHub.**
- `src/decision.py` @ `feat/decision-producer-contract` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/src/decision.py
- `tests/test_research_to_decision_boundary.py` @ `feat/decision-producer-contract` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/tests/test_research_to_decision_boundary.py
- `tests/test_context_research_alternative_paths.py` @ `feat/decision-producer-contract` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/tests/test_context_research_alternative_paths.py

**Manquant / dette.**
- Le motif-capacité correct existe déjà dans le dépôt : BoundResearchInput. Il n'a pas été réutilisé ici.
- Deux branches du même jour portent deux versions divergentes de cette frontière, l'une corrigée, l'autre non.

#### ⚪ Moteur de décision (Context Engine, Router, multi-horizon)

| | |
|---|---|
| **Statut** | `CIBLE` — CIBLE FUTURE |
| **Domaine** | DÉCISION |
| **Branche** | `—` |
| **Présent dans les vues** | TARGET · GAP |

**Rôle.** Identifier le régime de marché, router vers l'expert adapté, pondérer par horizon 15m/1h/4h, produire un signal pondéré.

**Entrées.** Contexte de marché + experts.

**Sorties.** Décision avec pondération.

**Contrat.** Spécifié en 01 §5 à §8.

**Invariants.**
- Routeur à règles explicables en V1, pas appris.

**Fonctionne si.** —

**Doit refuser si.** —

**Preuves disponibles.**
- Aucun code. Spécification narrative uniquement.

**Fichiers GitHub.**
- `docs/01-SYSTEM-VISION.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/01-SYSTEM-VISION.md

**Manquant / dette.**
- Tout est à construire.

---

### 4.9 Couche — RISQUE / GOUVERNANCE D'EXPOSITION

*Risk Engine, Portfolio Engine, architecture de sortie*

#### ⚪ Risk Engine + Portfolio Engine

| | |
|---|---|
| **Statut** | `CIBLE` — CIBLE FUTURE |
| **Domaine** | RISQUE / GOUVERNANCE D'EXPOSITION |
| **Branche** | `—` |
| **Présent dans les vues** | TARGET · GAP |

**Rôle.** Déterminer l'exposition rationnelle compte tenu du rendement attendu, de la volatilité, de l'incertitude, du drawdown, des corrélations, de la concentration, de la liquidité et des coûts — puis arbitrer au niveau portefeuille.

**Entrées.** Décision + état du portefeuille.

**Sorties.** Taille de position en R, éventuellement 0R.

**Contrat.** Spécifié en 01 §9 et §10.

**Invariants.**
- La force du signal individuel ne suffit pas à déterminer l'allocation.

**Fonctionne si.** —

**Doit refuser si.** —

**Preuves disponibles.**
- Aucun code, aucun test, aucun contrat exécutable. Absence totale.

**Fichiers GitHub.**
- `docs/01-SYSTEM-VISION.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/01-SYSTEM-VISION.md

**Manquant / dette.**
- Le domaine le plus critique pour un compte prop firm est celui qui a le moins d'existence dans le dépôt.

#### 🔵 Architecture de sortie de position

| | |
|---|---|
| **Statut** | `SPECIFIE` — SPÉCIFIÉ, non implémenté |
| **Domaine** | RISQUE / GOUVERNANCE D'EXPOSITION |
| **Branche** | `main` |
| **Présent dans les vues** | TARGET · GAP |

**Rôle.** Séquence OUVERTURE → ARMEMENT → BASCULEMENT → SORTIE, avec un sélecteur exclusif entre TRAILING_POINTS, PARABOLIC_SAR et MA_CROSS.

**Entrées.** Position ouverte.

**Sorties.** Clôture par un seul moteur actif.

**Contrat.** Règle d'exclusivité : les trois moteurs ne doivent pas être empilés comme décideurs indépendants.

**Invariants.**
- Le break-even est un mécanisme d'armement, pas un quatrième moteur de sortie.

**Fonctionne si.** —

**Doit refuser si.** —

**Preuves disponibles.**
- Statut explicite : PRINCIPE DE CONCEPTION À TESTER. Aucune supériorité d'un mode ne doit être considérée avant validation empirique.

**Fichiers GitHub.**
- `04-REFERENCE/ARCHITECTURE-SORTIE-POSITION.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/04-REFERENCE/ARCHITECTURE-SORTIE-POSITION.md

**Manquant / dette.**
- Exige un EA MT5 qui n'existe pas.

---

### 4.10 Couche — ACTION / EXÉCUTION

*Producteur d'action, ordres broker*

#### 🔴 Producteur d'action / exécution

| | |
|---|---|
| **Statut** | `MANQUANT` — MANQUANT / BLOCAGE |
| **Domaine** | ACTION / EXÉCUTION |
| **Branche** | `—` |
| **Présent dans les vues** | NOW · TARGET · GAP |

**Rôle.** Transformer une décision en comportement réel, y compris une absence d'action contrôlée.

**Entrées.** Decision.

**Sorties.** Action identifiable.

**Contrat.** —

**Invariants.**
- —

**Fonctionne si.** —

**Doit refuser si.** —

**Preuves disponibles.**
- Recherche exhaustive sur toutes les branches : aucun import MetaTrader5, aucune API broker, aucun code d'ordre. Seule existe la chaîne synthétique de test.

**Fichiers GitHub.**
- `src/synthetic_end_to_end.py` @ `feat/synthetic-end-to-end-chain` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/synthetic-end-to-end-chain/src/synthetic_end_to_end.py

**Manquant / dette.**
- Rupture R4 qualifiée CRITIQUE par le dépôt lui-même.

---

### 4.11 Couche — RÉSULTAT

*Observation et attribution*

#### 🔴 Observation de résultat / attribution

| | |
|---|---|
| **Statut** | `MANQUANT` — MANQUANT / BLOCAGE |
| **Domaine** | RÉSULTAT |
| **Branche** | `—` |
| **Présent dans les vues** | NOW · TARGET · GAP |

**Rôle.** Observer ce qui s'est réellement produit et attribuer la performance à sa cause.

**Entrées.** Action + observations.

**Sorties.** Résultat identifiable et attribuable.

**Contrat.** —

**Invariants.**
- —

**Fonctionne si.** —

**Doit refuser si.** —

**Preuves disponibles.**
- Existe uniquement comme champ result_id et dans le harness synthétique.

**Fichiers GitHub.**
- `src/synthetic_end_to_end.py` @ `feat/synthetic-end-to-end-chain` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/synthetic-end-to-end-chain/src/synthetic_end_to_end.py

**Manquant / dette.**
- Ruptures R5 et R6 qualifiées CRITIQUES par le dépôt.

---

### 4.12 Couche — TRACE

*Reconstruction structurelle, chaîne synthétique*

#### 🟡 DecisionTrace

| | |
|---|---|
| **Statut** | `PARTIEL` — PARTIEL |
| **Domaine** | TRACE |
| **Branche** | `feat/decision-producer-contract / feat/synthetic-end-to-end-chain` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Projection de reconstruction d'une décision achevée : provenance → run de recherche → code → configuration → dataset → contexte → décision → action → résultat.

**Entrées.** 10 identifiants obligatoires.

**Sorties.** Verdict PASS / FAIL + liste des liens manquants.

**Contrat.** Un lien manquant est un FAIL, jamais un PASS implicite.

**Invariants.**
- Une trace ne crée jamais les événements qu'elle prétend reconstruire.

**Fonctionne si.** Tous les liens présents et non vides.

**Doit refuser si.** Tout champ vide → FAIL avec la liste précise des manquants.

**Preuves disponibles.**
- Tests test_decision_trace.py verts.
- Validation structurelle uniquement : elle ne vérifie pas que les identifiants désignent des événements réels.

**Fichiers GitHub.**
- `src/decision_trace.py` @ `feat/decision-producer-contract` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/src/decision_trace.py
- `tests/test_decision_trace.py` @ `feat/synthetic-end-to-end-chain` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/synthetic-end-to-end-chain/tests/test_decision_trace.py

**Manquant / dette.**
- Une trace complète structurellement peut décrire une chaîne d'événements qui n'a jamais eu lieu. C'est précisément l'exposition n°2 listée par STEP-3-REAL-SYSTEM-MAPPING.

#### 🟡 Chaîne synthétique bout en bout

| | |
|---|---|
| **Statut** | `PARTIEL` — PARTIEL |
| **Domaine** | TRACE |
| **Branche** | `feat/synthetic-end-to-end-chain` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Harness déterministe DATA → CONTEXT → EXPERIENCE → DECISION → ACTION → RESULT → TRACE qui vérifie que chaque étage exige le précédent et émet un identifiant stable.

**Entrées.** Graines synthétiques.

**Sorties.** DecisionTrace complète + rejet des identités étrangères.

**Contrat.** Chaque étage exige le précédent.

**Invariants.**
- Ce n'est pas un moteur de trading.

**Fonctionne si.** —

**Doit refuser si.** Mutation d'identifiant étranger → rejet, testé en CI.

**Preuves disponibles.**
- 40 tests verts localement.
- Workflow synthetic-foreign-identity.yml exécute les mutations d'identité étrangère.

**Fichiers GitHub.**
- `src/synthetic_end_to_end.py` @ `feat/synthetic-end-to-end-chain` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/synthetic-end-to-end-chain/src/synthetic_end_to_end.py
- `tests/test_synthetic_foreign_identity_links.py` @ `feat/synthetic-end-to-end-chain` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/synthetic-end-to-end-chain/tests/test_synthetic_foreign_identity_links.py
- `.github/workflows/synthetic-foreign-identity.yml` @ `feat/synthetic-end-to-end-chain` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/synthetic-end-to-end-chain/.github/workflows/synthetic-foreign-identity.yml

**Manquant / dette.**
- Preuve de câblage synthétique, pas preuve du système réel. Le dépôt le dit explicitement.

---

### 4.13 Couche — MÉMOIRE / AUDIT / RÉVISION

*Mémoire expérimentale, audit exécutable, boucle de révision*

#### 🔵 Mémoire expérimentale

| | |
|---|---|
| **Statut** | `SPECIFIE` — SPÉCIFIÉ, non implémenté |
| **Domaine** | MÉMOIRE / AUDIT / RÉVISION |
| **Branche** | `main` |
| **Présent dans les vues** | NOW · TARGET · GAP |

**Rôle.** Conserver hypothèses, expériences, résultats, échecs, corrections, connaissances validées et raisons de rejet.

**Entrées.** Expérience + résultat + trace + preuves.

**Sorties.** Mémoire d'expérience.

**Contrat.** —

**Invariants.**
- —

**Fonctionne si.** —

**Doit refuser si.** —

**Preuves disponibles.**
- Le substitut de fait aujourd'hui : 47 fichiers 99-BACKUP/SESSION-*.md et 89 rapports. C'est une mémoire narrative par fichiers, pas un modèle interrogeable.

**Fichiers GitHub.**
- `GOVERNANCE/EXPERIMENTAL-MEMORY-CHARTER.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/GOVERNANCE/EXPERIMENTAL-MEMORY-CHARTER.md
- `99-BACKUP/README.md` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/99-BACKUP/README.md

**Manquant / dette.**
- Rupture R7 qualifiée TOTALE par le dépôt.

#### 🟡 Audit exécutable + boucle de révision

| | |
|---|---|
| **Statut** | `PARTIEL` — PARTIEL |
| **Domaine** | MÉMOIRE / AUDIT / RÉVISION |
| **Branche** | `feat/multi-year-dukascopy-acquisition` |
| **Présent dans les vues** | NOW · TARGET |

**Rôle.** Contester le chemin et ses conclusions, puis décider ce qui doit être modifié, conservé ou retesté.

**Entrées.** Trace + mémoire + règles + preuves.

**Sorties.** Constat, verdict, anomalies.

**Contrat.** Adjudicateurs indépendants par lot, hors ligne, sans raccourci sémantique partagé.

**Invariants.**
- Un adjudicateur ne doit pas partager de code sémantique avec l'implémentation qu'il juge.

**Fonctionne si.** Pour le domaine calendrier uniquement.

**Doit refuser si.** —

**Preuves disponibles.**
- Audit exécutable réel et solide sur le domaine calendrier : adjudicateurs par lot, re-cassage du HEAD persisté, vérification d'intégration atomique.
- Aucun audit exécutable du parcours complet DATA→…→AUDIT.

**Fichiers GitHub.**
- `tools/trading_breaks_recovery_batch11_adjudication.py` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/trading_breaks_recovery_batch11_adjudication.py
- `tools/integrate_trading_breaks_recovery_batch10.py` @ `feat/multi-year-dukascopy-acquisition` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/integrate_trading_breaks_recovery_batch10.py
- `GOVERNANCE/GOVERNANCE-EVOLUTION-AND-AUDIT-PROTOCOL.md` @ `main` — https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/GOVERNANCE/GOVERNANCE-EVOLUTION-AND-AUDIT-PROTOCOL.md

**Manquant / dette.**
- Ruptures R8 et R9 qualifiées TOTALES. La boucle audit → révision → nouvelle expérience n'existe qu'en procédure.

---

## 5. Les trois temporalités

### A — SYSTEM NOW : architecture réellement démontrée aujourd'hui

| Composant | Couche | Statut |
|---|---|---|
| Dukascopy — ticks BI5 + widget Trading Breaks | MONDE EXTÉRIEUR | 🟣 `EXTERNE` |
| VT Markets / MT5 — flux d'exécution | MONDE EXTÉRIEUR | 🟣 `EXTERNE` |
| GitHub Actions | MONDE EXTÉRIEUR | 🟣 `EXTERNE` |
| AI Operating Memory | GOUVERNANCE | 🟢 `EXISTANT` |
| Recovery Checkpoint | GOUVERNANCE | ⚠️ `AMBIGU` |
| Repository Safety Rules | GOUVERNANCE | 🟢 `EXISTANT` |
| Frontière humaine / décision normative | GOUVERNANCE | 🟢 `EXISTANT` |
| Experimental Memory Charter | GOUVERNANCE | 🔵 `SPECIFIE` |
| 04 — Validation Criteria v0.6.2 | CORPUS NORMATIF | 🟢 `EXISTANT` |
| 05 — Data Contract v0.1 | CORPUS NORMATIF | ⚠️ `AMBIGU` |
| 08 — System Registry + registres 09→14 | CORPUS NORMATIF | 🟡 `PARTIEL` |
| Qualification Input Register — 10 entrées BLOCKED | CORPUS NORMATIF | 🔴 `MANQUANT` |
| tick_reader | DATA | 🟢 `EXISTANT` |
| dataset_admissibility | DATA | 🟢 `EXISTANT` |
| input_binding — capacité BoundResearchInput | DATA | 🟢 `EXISTANT` |
| bi5_reader + contrat d'instrument | DATA | 🟡 `PARTIEL` |
| Sonde V4.3 — compatibilité recherche ↔ exécution | DATA | 🟡 `PARTIEL` |
| Audit de couverture calendrier | VÉRITÉ TEMPORELLE | 🟢 `EXISTANT` |
| Protocole de récupération des Trading Breaks | VÉRITÉ TEMPORELLE | 🟢 `EXISTANT` |
| Machine à lots — Batches 01 → 11 | VÉRITÉ TEMPORELLE | 🟢 `EXISTANT` |
| Règle du gap irréductible de preuve broker | VÉRITÉ TEMPORELLE | 🟢 `EXISTANT` |
| Sélection et gel de la fenêtre d'exécution | VÉRITÉ TEMPORELLE | 🔴 `MANQUANT` |
| Context + context_identity | CONTEXTE | 🟡 `PARTIEL` |
| ResearchRunEvidence | RECHERCHE / EXPÉRIENCE | 🟡 `PARTIEL` |
| Momentum V1 — définition + protocole baseline | RECHERCHE / EXPÉRIENCE | 🔵 `SPECIFIE` |
| produce_decision — frontière RESEARCH → DECISION | DÉCISION | 🔴 `MANQUANT` |
| Producteur d'action / exécution | ACTION / EXÉCUTION | 🔴 `MANQUANT` |
| Observation de résultat / attribution | RÉSULTAT | 🔴 `MANQUANT` |
| DecisionTrace | TRACE | 🟡 `PARTIEL` |
| Chaîne synthétique bout en bout | TRACE | 🟡 `PARTIEL` |
| Mémoire expérimentale | MÉMOIRE / AUDIT / RÉVISION | 🔵 `SPECIFIE` |
| Audit exécutable + boucle de révision | MÉMOIRE / AUDIT / RÉVISION | 🟡 `PARTIEL` |

### B — TARGET SYSTEM : architecture finale visée par le dépôt

| Composant | Couche | Statut |
|---|---|---|
| Dukascopy — ticks BI5 + widget Trading Breaks | MONDE EXTÉRIEUR | 🟣 `EXTERNE` |
| VT Markets / MT5 — flux d'exécution | MONDE EXTÉRIEUR | 🟣 `EXTERNE` |
| GitHub Actions | MONDE EXTÉRIEUR | 🟣 `EXTERNE` |
| AI Operating Memory | GOUVERNANCE | 🟢 `EXISTANT` |
| Recovery Checkpoint | GOUVERNANCE | ⚠️ `AMBIGU` |
| Repository Safety Rules | GOUVERNANCE | 🟢 `EXISTANT` |
| Frontière humaine / décision normative | GOUVERNANCE | 🟢 `EXISTANT` |
| Experimental Memory Charter | GOUVERNANCE | 🔵 `SPECIFIE` |
| 01 — System Vision | CORPUS NORMATIF | 🔵 `SPECIFIE` |
| 04 — Validation Criteria v0.6.2 | CORPUS NORMATIF | 🟢 `EXISTANT` |
| 05 — Data Contract v0.1 | CORPUS NORMATIF | ⚠️ `AMBIGU` |
| 08 — System Registry + registres 09→14 | CORPUS NORMATIF | 🟡 `PARTIEL` |
| tick_reader | DATA | 🟢 `EXISTANT` |
| dataset_admissibility | DATA | 🟢 `EXISTANT` |
| input_binding — capacité BoundResearchInput | DATA | 🟢 `EXISTANT` |
| bi5_reader + contrat d'instrument | DATA | 🟡 `PARTIEL` |
| Sonde V4.3 — compatibilité recherche ↔ exécution | DATA | 🟡 `PARTIEL` |
| Audit de couverture calendrier | VÉRITÉ TEMPORELLE | 🟢 `EXISTANT` |
| Protocole de récupération des Trading Breaks | VÉRITÉ TEMPORELLE | 🟢 `EXISTANT` |
| Machine à lots — Batches 01 → 11 | VÉRITÉ TEMPORELLE | 🟢 `EXISTANT` |
| Règle du gap irréductible de preuve broker | VÉRITÉ TEMPORELLE | 🟢 `EXISTANT` |
| Sélection et gel de la fenêtre d'exécution | VÉRITÉ TEMPORELLE | 🔴 `MANQUANT` |
| Context + context_identity | CONTEXTE | 🟡 `PARTIEL` |
| ResearchRunEvidence | RECHERCHE / EXPÉRIENCE | 🟡 `PARTIEL` |
| Momentum V1 — définition + protocole baseline | RECHERCHE / EXPÉRIENCE | 🔵 `SPECIFIE` |
| produce_decision — frontière RESEARCH → DECISION | DÉCISION | 🔴 `MANQUANT` |
| Moteur de décision (Context Engine, Router, multi-horizon) | DÉCISION | ⚪ `CIBLE` |
| Risk Engine + Portfolio Engine | RISQUE / GOUVERNANCE D'EXPOSITION | ⚪ `CIBLE` |
| Architecture de sortie de position | RISQUE / GOUVERNANCE D'EXPOSITION | 🔵 `SPECIFIE` |
| Producteur d'action / exécution | ACTION / EXÉCUTION | 🔴 `MANQUANT` |
| Observation de résultat / attribution | RÉSULTAT | 🔴 `MANQUANT` |
| DecisionTrace | TRACE | 🟡 `PARTIEL` |
| Chaîne synthétique bout en bout | TRACE | 🟡 `PARTIEL` |
| Mémoire expérimentale | MÉMOIRE / AUDIT / RÉVISION | 🔵 `SPECIFIE` |
| Audit exécutable + boucle de révision | MÉMOIRE / AUDIT / RÉVISION | 🟡 `PARTIEL` |

### C — GAP VIEW : uniquement ce qui sépare NOW de TARGET

| Composant | Couche | Statut |
|---|---|---|
| Recovery Checkpoint | GOUVERNANCE | ⚠️ `AMBIGU` |
| Experimental Memory Charter | GOUVERNANCE | 🔵 `SPECIFIE` |
| 01 — System Vision | CORPUS NORMATIF | 🔵 `SPECIFIE` |
| 05 — Data Contract v0.1 | CORPUS NORMATIF | ⚠️ `AMBIGU` |
| Qualification Input Register — 10 entrées BLOCKED | CORPUS NORMATIF | 🔴 `MANQUANT` |
| Sélection et gel de la fenêtre d'exécution | VÉRITÉ TEMPORELLE | 🔴 `MANQUANT` |
| Momentum V1 — définition + protocole baseline | RECHERCHE / EXPÉRIENCE | 🔵 `SPECIFIE` |
| produce_decision — frontière RESEARCH → DECISION | DÉCISION | 🔴 `MANQUANT` |
| Moteur de décision (Context Engine, Router, multi-horizon) | DÉCISION | ⚪ `CIBLE` |
| Risk Engine + Portfolio Engine | RISQUE / GOUVERNANCE D'EXPOSITION | ⚪ `CIBLE` |
| Architecture de sortie de position | RISQUE / GOUVERNANCE D'EXPOSITION | 🔵 `SPECIFIE` |
| Producteur d'action / exécution | ACTION / EXÉCUTION | 🔴 `MANQUANT` |
| Observation de résultat / attribution | RÉSULTAT | 🔴 `MANQUANT` |
| Mémoire expérimentale | MÉMOIRE / AUDIT / RÉVISION | 🔵 `SPECIFIE` |

---

## 6. Carte des capacités

Ce que le système sait faire — et ce qu'il sait qu'il ne doit pas faire. Chaque ligne est rattachée à un artefact du dépôt. Les lignes MUST REFUSE ne sont pas des limitations subies : ce sont des refus contractuels que le code et la gouvernance appliquent activement.

### CAN DO (10)

| Capacité | Support | Niveau de preuve | Limites / conditions |
|---|---|---|---|
| Identifier un CSV de ticks par ses octets exacts et l'accepter ou le rejeter de façon déterministe | dataset_admissibility + tick_reader sur main | 13 tests, dont 5 cas négatifs paramétrés, rejoués localement | Un seul schéma CSV figé. Pas d'autre format. |
| Décoder un corpus Dukascopy BI5 selon un contrat d'instrument versionné et produire un hash de flux déterministe | src/research/ sur branche active | Tests d'instrument + tests de consommateurs V4.3 | Reconstruction, pas récupération : identité avec l'implémentation historique non prouvable. |
| Lier un corpus à une capacité non forgeable avant exécution | input_binding — BoundResearchInput | Le constructeur refuse toute création hors fabrique | Hors main. |
| Comparer les propriétés de deux flux indépendants sans les fusionner | Sonde V4.3 | Code lisible, verdicts structurellement contraints | TRANSFER_VALIDATION reste UNVERIFIED par construction. |
| Énumérer 111 dates candidates sur 2018-05-01 → 2026-08-14 et auditer leur résolution | tools/dukascopy_usatech_calendar_coverage.py | Outil réexécuté : 111/60/51, verdict BLOCKED | Un seul instrument : USATECHIDXUSD. |
| Récupérer des enregistrements natifs de fermeture broker à la date exacte, avec provenance complète, en lots gouvernés | Protocole + machine à lots 01→11 | Run 34880921889, 20 tests d'attaque verts. 55 workflows, 89 rapports. | Dépend de la disponibilité du widget Dukascopy. |
| Refuser de promouvoir une absence de donnée en preuve | Invariant §5 du protocole | Testé : promotion de no-record rejetée | — |
| Empêcher les dates déjà tentées d'affamer les suivantes, sans jamais convertir BLOCKED en résolu | Contrat de progression V1 | Run 34890560172, 72 tests verts | — |
| Reconstruire structurellement une décision et échouer si un lien manque | DecisionTrace | Tests verts | Structurel seulement : ne vérifie pas que les événements ont eu lieu. |
| Rejeter une identité étrangère dans une chaîne complète | Harness synthétique + CI dédiée | 40 tests verts | Synthétique. Ne prouve rien sur le système réel. |

### CAN DO CONDITIONALLY (2)

| Capacité | Support | Niveau de preuve | Limites / conditions |
|---|---|---|---|
| Produire un Context, une ResearchRunEvidence et une Decision | Branche feat/decision-producer-contract uniquement | Tests de frontière verts sauf 2 | Non fusionné. La frontière RESEARCH→DECISION est contournable. |
| Télécharger un corpus .bi5 Dukascopy | tools/download_dukascopy_tick_corpus.py | Outil présent | La gouvernance marque .bi5 : FORBIDDEN. L'outil existe mais l'usage est interdit. |

### CANNOT DO YET (6)

| Capacité | Support | Niveau de preuve | Limites / conditions |
|---|---|---|---|
| Calculer un signal de trading | — | Momentum V1 est défini et son protocole gelé ; aucun code ne l'implémente | — |
| Détecter un régime, router des experts, dimensionner le risque, arbitrer un portefeuille | — | Aucun code sur aucune branche | — |
| Passer ou gérer un ordre, se connecter à MT5 ou à un broker | — | Aucun import MetaTrader5 ni API broker dans tout le dépôt | — |
| Observer un résultat réel et attribuer la performance | — | Ruptures R5 et R6 qualifiées CRITIQUES par le dépôt | — |
| Stocker une mémoire expérimentale, exécuter une boucle audit → révision | — | Ruptures R7, R8, R9 qualifiées TOTALES | — |
| Exécuter un backtest réel | — | Aucun harness de backtest n'existe | — |

### MUST REFUSE (9)

| Capacité | Support | Niveau de preuve | Limites / conditions |
|---|---|---|---|
| Lancer un backtest réel | Checkpoint du 15/09 : real backtest NOT AUTHORIZED | — | Tant que tous les gates amont ne sont pas PASS. |
| Acquisition massive de .bi5 | Checkpoint : .bi5 FORBIDDEN | — | Exige une fenêtre gelée PASS sous Action C. |
| Geler la fenêtre d'exécution | 31 non résolues sur 68 candidats en fenêtre | — | Une fenêtre cherry-pickée ou < 5 ans donne FAIL, pas BLOCKED. |
| Déclarer la couverture calendrier globale PASS | 51 non résolues sur 111 | — | Un gap irréductible maintient aussi BLOCKED. |
| Promouvoir une réponse vide, un échec HTTP ou un no-record en NO_SPECIAL_CHANGE_EVIDENCE | Invariant §5 du protocole | — | Exigerait un contrat de preuve négative qui n'existe pas. |
| Deviner le fuseau d'un timestamp Parquet naïf | Sonde V4.3 : BLOCKED sans --naive-timezone explicite | — | — |
| Déplacer, raccourcir ou étendre la fenêtre 2021-08-14 → 2026-08-14 pour réduire les non résolues | Règle d'immuabilité §12 | — | — |
| Traiter 05-DATA-CONTRACT comme normatif | 08-SYSTEM-REGISTRY : définiteur proposé uniquement | — | — |
| Conclure au transfert recherche → exécution | equivalence_thresholds forcé à UNVERIFIED | — | Exigerait des seuils gelés et testés adversarialement. |

### UNKNOWN / NOT PROVEN (4)

| Capacité | Support | Niveau de preuve | Limites / conditions |
|---|---|---|---|
| Momentum V1 a-t-il un avantage ? | Aucun backtest n'a jamais tourné | — | Les PASS 3.1.1 et 3.1.2 portent sur la définition et le protocole, pas la performance. |
| Le flux Dukascopy prédit-il l'exécution VT Markets ? | TRANSFER_VALIDATION structurellement UNVERIFIED | — | — |
| Le lecteur BI5 reconstruit équivaut-il à l'implémentation historique perdue ? | Le module déclare RECONSTRUCTION != RECOVERY | — | — |
| Les 51 dates non résolues sont-elles récupérables ? | 13 déjà BLOCKED à capacité identique | — | Pourrait exiger un changement de capacité de preuve. |

---

## 7. Carte des modes de défaillance

Ne figurent ici que des modes de défaillance confirmés par le dépôt ou reproduits par exécution. Les catégories théoriques sans preuve dans le dépôt ont été écartées.

### 7.1 Fragmentation par branches  ·  gravité ÉLEVÉ

- **Composant concerné :** Gouvernance / tout le système
- **Preuve :** main a 137 commits et 13 tests ; la branche active en a 530 et 55 workflows. Le RECOVERY-CHECKPOINT de main désigne une branche déjà dépassée de 2 jours.
- **Conséquence :** Un lecteur qui applique la règle « le dépôt est la source de vérité » sur main reconstruit un système faux.
- **Protection actuelle :** Aucune. La règle de gouvernance elle-même produit l'erreur.

### 7.2 Frontière RESEARCH → DECISION contournable  ·  gravité ÉLEVÉ

- **Composant concerné :** produce_decision
- **Preuve :** Vérifié par moi : object.__setattr__(evidence,'_factory_validated',True) sur une preuve forgée produit une Decision valide avec code_version='attacker'.
- **Conséquence :** Une décision peut être rattachée à un run de recherche qui n'a jamais eu lieu. La trace serait structurellement complète et sémantiquement fausse.
- **Protection actuelle :** Le motif correct existe déjà dans le dépôt (BoundResearchInput) mais n'est pas réutilisé ici.

### 7.3 Tests rouges non traités  ·  gravité ÉLEVÉ

- **Composant concerné :** Chaîne décisionnelle
- **Preuve :** 2 tests rouges sur feat/decision-producer-contract, 3 sur audit/pre-backtest-freeze. Vérifié en exécutant les suites.
- **Conséquence :** Deux branches du même jour portent deux versions divergentes de la même frontière, l'une corrigée, l'autre non.
- **Protection actuelle :** Aucune : les workflows ne se déclenchent pas sur ces branches.

### 7.4 Déclencheurs CI liés à des branches nommées  ·  gravité ÉLEVÉ

- **Composant concerné :** GitHub Actions
- **Preuve :** research-to-decision-boundary.yml ne se déclenche que sur push vers feat/decision-producer-contract. Le commit « Execute … in CI » sur audit/pre-backtest-freeze ajoute une étape à un workflow qui ne tourne pas sur cette branche.
- **Conséquence :** Un test déclaré « exécuté en CI » peut n'avoir jamais tourné. La preuve d'exécution est présumée, pas établie.
- **Protection actuelle :** Aucune.

### 7.5 Zéro CI sur main  ·  gravité MOYEN

- **Composant concerné :** main
- **Preuve :** Aucun répertoire .github sur main.
- **Conséquence :** La branche de référence n'a aucune garantie automatique de non-régression.
- **Protection actuelle :** Aucune.

### 7.6 Rapports figés périmés  ·  gravité MOYEN

- **Composant concerné :** Rapports de qualification
- **Preuve :** Le rapport global de couverture annonce 24 résolus / 87 non résolus ; l'outil réexécuté donne 60 / 51.
- **Conséquence :** Un lecteur qui fait confiance au Markdown persisté sous-estime l'avancement de 36 dates.
- **Protection actuelle :** Le checkpoint, lui, est à jour — mais il vit ailleurs.

### 7.7 Dette 05 parquée, pas payée  ·  gravité MOYEN

- **Composant concerné :** Corpus normatif
- **Preuve :** CTR-01 a été clos en rétrogradant 04 §5.3 c.4 de BLOQUANTE à SUSPENDUE, sans adopter 05.
- **Conséquence :** Le modèle de coûts complets — indispensable pour qu'un avantage statistique survive aux frais — n'a plus de condition bloquante qui le protège.
- **Protection actuelle :** Le registre 08 empêche au moins de traiter 05 comme normatif.

### 7.8 Trace complète sans événements réels  ·  gravité MOYEN

- **Composant concerné :** DecisionTrace
- **Preuve :** La validation est purement structurelle : 10 champs non vides donnent PASS.
- **Conséquence :** Une trace peut décrire une chaîne qui n'a jamais eu lieu. Le dépôt liste lui-même cette exposition.
- **Protection actuelle :** La chaîne synthétique teste le rejet d'identités étrangères, mais uniquement dans son propre harness.

### 7.9 Dépendance à une seule voie externe  ·  gravité MOYEN

- **Composant concerné :** Dukascopy
- **Preuve :** Playwright + widget Trading Breaks est la seule voie de production du système aujourd'hui.
- **Conséquence :** Un changement d'interface ou de politique stoppe net l'unique atelier actif.
- **Protection actuelle :** Le protocole traite correctement l'indisponibilité comme BLOCKED, jamais comme preuve. Le risque est d'arrêt, pas de corruption.

### 7.10 Gap irréductible de preuve broker  ·  gravité MOYEN

- **Composant concerné :** Vérité temporelle
- **Preuve :** 13 dates sont BLOCKED à capacité de preuve identique.
- **Conséquence :** Si elles sont irréductibles, le gel de fenêtre exige soit un changement de capacité, soit une adjudication formelle du gap.
- **Protection actuelle :** La règle IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1 existe et encadre exactement ce cas.

### 7.11 Aucune dépendance épinglée  ·  gravité MOYEN

- **Composant concerné :** Tout le code
- **Preuve :** Ni requirements.txt, ni pyproject.toml, ni lockfile. Playwright non versionné.
- **Conséquence :** Un run CI dans six mois peut ne pas reproduire un run d'aujourd'hui, ce qui contredit frontalement l'exigence de reproductibilité.
- **Protection actuelle :** Aucune.

### 7.12 Hygiène de branches  ·  gravité MOYEN

- **Composant concerné :** Dépôt
- **Preuve :** 86 branches, dont une trentaine de quasi-doublons (rf-*, gap02*, step3-…-gate-2 à -10), plus une branche nommée __noop_should_not_exist__.
- **Conséquence :** Localiser l'état réel exige de dater les 86 branches. C'est exactement ce que la mémoire opérationnelle cherchait à éviter.
- **Protection actuelle :** Le RECOVERY-CHECKPOINT devait résoudre ça — mais il vit sur une branche.

### 7.13 Absence totale du domaine risque  ·  gravité ÉLEVÉ à terme

- **Composant concerné :** Risk / Portfolio
- **Preuve :** Zéro ligne de code, zéro test, zéro contrat exécutable.
- **Conséquence :** Pour un compte prop firm, c'est le domaine dont l'absence coûte le plus cher.
- **Protection actuelle :** Aucune. La vision le décrit, rien ne le protège.

> Le dépôt protège remarquablement bien contre les défaillances **sémantiques** — fausse preuve, promotion d'absence, contournement de contrat, fenêtre cherry-pickée. Il ne protège presque pas contre les défaillances **opérationnelles** — état dispersé, CI mal câblée, rapports périmés, dépendances non épinglées. C'est l'asymétrie la plus marquante de l'audit.

---

## 8. Carte des dépendances

Le dépôt est remarquablement peu dépendant. Une seule bibliothèque tierce en dehors de l'outillage de test.

| Dépendance | Type | Utilisée par | Criticité | Comportement en cas d'indisponibilité |
|---|---|---|---|---|
| **Dukascopy** — widget Trading Breaks | Service externe | Toute la machine à lots 01→11, seule voie de production active | CRITIQUE | BLOCKED, jamais converti en preuve. Le système s'arrête proprement. |
| **Dukascopy** — ticks BI5 | Données externes | bi5_reader, sonde V4.3, futur corpus | CRITIQUE | Usage actuellement INTERDIT par gouvernance. |
| **Playwright** | Bibliothèque Python | Sondes navigateur Dukascopy | ÉLEVÉE | Non épinglée. Seule dépendance tierce hors pytest. |
| **GitHub Actions** | Infrastructure | 55 workflows, substrat de toutes les preuves d'exécution | ÉLEVÉE | Les identités de run sont conservées dans les rapports ; elles deviendraient invérifiables. |
| **VT Markets / MT5** | Broker | Flux d'exécution de référence, frontière observable V4.2 | MOYENNE aujourd'hui | Relation purement documentaire. Aucun code d'intégration. |
| **Claude et Grok** | Contre-expertise | Protocole de décision 3 voies, ~50 documents d'adjudication | MOYENNE | Le protocole prévoit l'indisponibilité : « sauf si la contre-expertise indépendante est démontrablement indisponible ». |
| **pytest** + bibliothèque standard Python | Outillage | Tout le code | FAIBLE | Aucun numpy, pandas, scipy. Tout le calcul est en stdlib. |

> Aucun appel LLM en runtime nulle part dans le dépôt. Les IA interviennent comme contre-expertes dans le processus humain, jamais comme composant du système. C'est une décision d'architecture forte, et elle est tenue.

---

## 9. Carte des améliorations

Quatre catégories strictement séparées. Les deux dernières entrées sont des hypothèses de l'auditeur, pas des cibles du dépôt — elles sont marquées comme telles et ne doivent pas être traitées comme décidées.

### GAP OBLIGATOIRE (6)

#### [P1] Désigner une branche d'intégration unique et y consolider l'état

- **Problème et preuve :** main est à 13 tests, la branche active à 530. Le checkpoint de main pointe vers une branche périmée.
- **Conséquence si rien n'est fait :** Chaque session repart d'un état incertain ; la règle « le dépôt est la source de vérité » devient inapplicable.
- **Proposition :** Fusionner feat/multi-year-dukascopy-acquisition dans main, ou déclarer explicitement dans main quelle branche fait foi, avec sa date.
- **Bénéfice attendu :** L'état devient lisible en une lecture.
- **Risque introduit :** Une fusion peut écraser des suppressions volontaires de GOVERNANCE/* observées sur les branches.
- **Dépend de :** —

#### [P1] Remplacer _factory_validated par un objet-capacité

- **Problème et preuve :** Contournement reproduit : object.__setattr__ suffit.
- **Conséquence si rien n'est fait :** Une décision peut se rattacher à un run de recherche inexistant.
- **Proposition :** Appliquer à produce_decision le motif déjà éprouvé dans input_binding : jeton privé au module, constructeur qui refuse toute création externe.
- **Bénéfice attendu :** La frontière la plus critique de la chaîne devient non forgeable, avec un motif déjà validé en interne.
- **Risque introduit :** Aucun. Le motif existe et est testé.
- **Dépend de :** Consolidation de branche

#### [P1] Rendre les tests verts et câbler la CI sur la branche qui fait foi

- **Problème et preuve :** 2 et 3 tests rouges selon la branche ; les workflows ne se déclenchent pas là où vivent les tests.
- **Conséquence si rien n'est fait :** Un test « exécuté en CI » peut n'avoir jamais tourné. La preuve est présumée.
- **Proposition :** Mettre à jour les assertions de message, puis remplacer les déclencheurs par branche nommée par un déclencheur sur la branche d'intégration et sur pull request.
- **Bénéfice attendu :** La CI redevient une preuve, pas une déclaration.
- **Risque introduit :** —
- **Dépend de :** Consolidation de branche

#### [P2] Trancher les 51 dates non résolues

- **Problème et preuve :** 51 sur 111 globalement, 31 sur 68 en fenêtre. 13 déjà BLOCKED à capacité identique.
- **Conséquence si rien n'est fait :** Le gel de fenêtre, donc l'acquisition, donc le premier backtest, sont tous bloqués derrière ce compte.
- **Proposition :** Poursuivre les lots pour les 18 éligibles ; pour les 13 bloquées à capacité identique, instruire formellement la règle IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1 plutôt que de retenter.
- **Bénéfice attendu :** Le chemin vers le backtest se débloque ou se qualifie explicitement comme irréductible.
- **Risque introduit :** Risque de boucle infinie si les 13 sont retentées sans changement de capacité — que le contrat de progression est précisément fait pour empêcher.
- **Dépend de :** Disponibilité du widget Dukascopy

#### [P2] Implémenter Momentum V1

- **Problème et preuve :** Définition PASS, protocole PASS, harness de sortie gelé. Aucun code.
- **Conséquence si rien n'est fait :** C'est le plus petit maillon manquant entre une infrastructure de preuve et un système qui décide quelque chose.
- **Proposition :** Implémenter le calcul H1/20 barres et le harness gelé, puis le raccorder à produce_decision une fois la capacité corrigée.
- **Bénéfice attendu :** Première décision réelle traçable de bout en bout. La rupture R3, qualifiée CRITIQUE, se ferme.
- **Risque introduit :** Aucun si le protocole gelé est respecté à la lettre — il a été conçu pour ça.
- **Dépend de :** Correction de la capacité + 5 ans de données

#### [P3] Fermer les 10 entrées du Qualification Input Register

- **Problème et preuve :** D, R, M, B, A, Q, F, O, I_A, I_B toutes BLOCKED.
- **Conséquence si rien n'est fait :** Le gate exécutable global RB-A → Q-RM-12 reste fermé. ~50 documents d'adjudication restent sans effet opérationnel.
- **Proposition :** Produire les artefacts concrets versionnés dans l'ordre imposé : D+R+M, puis B+A, puis Q, puis F+O, puis I_A+I_B.
- **Bénéfice attendu :** Le travail sémantique déjà fait devient exploitable.
- **Risque introduit :** Charge importante. À séquencer après le déblocage calendrier.
- **Dépend de :** Décisions normatives humaines

### DETTE (4)

#### [P2] Épingler les dépendances

- **Problème et preuve :** Ni requirements.txt, ni pyproject.toml, ni lockfile.
- **Conséquence si rien n'est fait :** Un run futur peut ne pas reproduire un run actuel — en contradiction directe avec l'exigence de reproductibilité.
- **Proposition :** Ajouter un requirements.txt épinglé et l'installer dans les workflows au lieu de pip install pytest.
- **Bénéfice attendu :** La reproductibilité devient réelle et pas seulement revendiquée.
- **Risque introduit :** —
- **Dépend de :** —

#### [P3] Régénérer les rapports au lieu de les figer

- **Problème et preuve :** Le rapport global annonce 24/87, l'outil donne 60/51.
- **Conséquence si rien n'est fait :** Les instantanés se périment silencieusement.
- **Proposition :** Faire produire par la CI un state.json unique depuis les outils, et faire pointer les rapports Markdown vers lui.
- **Bénéfice attendu :** Une seule vérité chiffrée, toujours à jour.
- **Risque introduit :** —
- **Dépend de :** CI sur la branche d'intégration

#### [P3] Nettoyer les 86 branches

- **Problème et preuve :** Une trentaine de quasi-doublons, plus __noop_should_not_exist__.
- **Conséquence si rien n'est fait :** Localiser l'état exige de dater 86 branches.
- **Proposition :** Supprimer les branches fusionnées ou abandonnées après avoir confirmé que leur contenu est ailleurs.
- **Bénéfice attendu :** La navigation redevient possible.
- **Risque introduit :** Perte d'historique si une branche unique est supprimée par erreur. Vérifier avant.
- **Dépend de :** —

#### [P3] Résoudre la dette 05 au lieu de la suspendre

- **Problème et preuve :** 04 §5.3 c.4 suspendue, 05 toujours non normatif.
- **Conséquence si rien n'est fait :** Le modèle de coûts complets n'est plus protégé par une condition bloquante.
- **Proposition :** Soit adjuger 05, soit écrire une règle de coûts minimale et normative dans 04.
- **Bénéfice attendu :** Un avantage statistique ne pourra plus être validé sans épreuve des coûts.
- **Risque introduit :** Adopter 05 tel quel réactiverait 8 concepts non arbitrés.
- **Dépend de :** —

### AMÉLIORATION (2)

#### [P3] Factoriser les workflows de lot

- **Problème et preuve :** 55 workflows pour 11 lots, 4 à 5 par lot.
- **Conséquence si rien n'est fait :** Le coût marginal par lot ne décroît pas.
- **Proposition :** Un workflow paramétré par numéro de lot via workflow_dispatch.
- **Bénéfice attendu :** Chaque lot coûte un input au lieu de cinq fichiers.
- **Risque introduit :** Perte de l'immuabilité par fichier figé — à peser contre le gain, car le gel avant observation est un invariant du protocole.
- **Dépend de :** —

#### [P3] Contract-tester la preuve calendrier contre un schéma

- **Problème et preuve :** 0 erreur de forme aujourd'hui, mais aucun schéma n'est appliqué.
- **Conséquence si rien n'est fait :** Une preuve mal formée passerait jusqu'à l'audit d'intégration.
- **Proposition :** Valider les enregistrements de preuve contre un schéma versionné à l'écriture.
- **Bénéfice attendu :** Détection au plus tôt.
- **Risque introduit :** —
- **Dépend de :** —

### NOUVELLE HYPOTHÈSE — non décidée (2)

#### [P3] Le périmètre V1 : mono-actif ou multi-actifs ?

- **Problème et preuve :** 01-SYSTEM-VISION décrit un système multi-actifs avec backbone NAS100/Gold/DXY/US10Y/VIX/EURUSD/BTC. Tout le travail exécutable porte sur USATECHIDXUSD seul.
- **Conséquence si rien n'est fait :** Le coût de qualification calendrier observé — 11 lots pour 60 dates sur un instrument — se multiplierait par le nombre d'actifs.
- **Proposition :** À arbitrer explicitement : soit V1 est mono-actif et la vision est amendée, soit le coût de qualification par actif doit être réduit d'un ordre de grandeur avant d'élargir.
- **Bénéfice attendu :** Évite de découvrir l'échelle du problème après avoir engagé un deuxième actif.
- **Risque introduit :** C'est mon observation, pas une cible du dépôt. Elle ne doit pas être traitée comme décidée.
- **Dépend de :** —

#### [P3] La rigueur est-elle correctement allouée ?

- **Problème et preuve :** La couche DATA/calendrier concentre 530 tests, 55 workflows et 89 rapports. Les couches DÉCISION, RISQUE, ACTION et RÉSULTAT en concentrent zéro.
- **Conséquence si rien n'est fait :** Un système peut avoir une frontière de données irréprochable et perdre de l'argent par absence de gestion du risque.
- **Proposition :** À arbitrer : le niveau de preuve exigé sur DATA doit-il s'appliquer identiquement aux couches aval, ou un niveau gradué est-il admissible pour atteindre plus vite une chaîne complète testable ?
- **Bénéfice attendu :** Permet de décider consciemment plutôt que par inertie.
- **Risque introduit :** Mon observation, pas une position du dépôt. Baisser l'exigence aval contredirait la gouvernance actuelle.
- **Dépend de :** —

---

## 10. Synthèse

### Où en est réellement le système

Ce n'est pas un système de trading incomplet. C'est une **machine à qualification de preuves** qui n'a pas encore atteint la couche trading — et qui le sait, l'écrit et le fait respecter par du code.

> L'analogie la plus juste : un laboratoire d'étalonnage. L'instrumentation, les protocoles de mesure, les procédures de rejet et la traçabilité sont d'un niveau inhabituel. L'expérience elle-même n'a pas commencé.

### Ce qui est réellement démontré aujourd'hui

Une frontière DATA exécutable et testée négativement. Un décodeur BI5 piloté par contrat versionné. Un objet-capacité non forgeable pour lier un corpus. Une machine de qualification calendrier de qualité industrielle : 111 candidats énumérés, 60 résolus par enregistrement natif broker à la date exacte, 11 lots gelés avant observation, adjudication indépendante, intégration atomique, re-cassage du HEAD persisté. 530 tests verts, rejoués. 55 workflows. 89 rapports. Et un ensemble de refus contractuels que le code applique réellement.

### Ce qui est seulement documenté

La totalité de l'architecture de trading : Context Engine, trois experts, routeur, multi-horizon, Risk Engine, Portfolio Engine, Execution Engine, attribution, surveillance, Champion/Challenger. Plus la mémoire expérimentale, la boucle audit→révision, la bitemporalité, le registre de contradictions et la contestation ascendante. Le corpus décrit ces éléments avec précision ; aucun n'a de code.

### La distance NOW → TARGET

Elle n'est pas uniforme. Sur DATA et VÉRITÉ TEMPORELLE, la distance est d'environ 31 dates. Sur CONTEXTE, RECHERCHE et TRACE, elle est d'une fusion de branches et d'une correction de capacité. Sur DÉCISION, RISQUE, ACTION et RÉSULTAT, elle est totale : il n'y a rien à corriger, tout est à construire.

### Les trois lacunes structurantes, dans l'ordre

**1. L'état du système n'est pas localisable en une lecture.** C'est la lacune la plus grave parce qu'elle attaque la gouvernance elle-même. Un dépôt dont la règle fondatrice est « le dépôt est la source de vérité » et dont la branche de référence décrit un système périmé de deux jours a un problème qui précède tous les autres. Rien d'autre ne devrait être entrepris avant.

**2. La frontière RESEARCH → DECISION est contournable.** J'ai reproduit le contournement. Le correctif est trivial et le motif correct existe déjà dans votre propre dépôt. Tant qu'elle n'est pas corrigée, toute décision produite par cette chaîne est structurellement traçable et sémantiquement non garantie — exactement le scénario que la gouvernance interdit.

**3. Le prochain maillon architectural rationnel est Momentum V1.** Pas le Risk Engine, pas le routeur, pas l'Asset Profile. Momentum V1 parce que sa définition est gelée, son protocole est gelé après cassage et re-cassage, son harness de sortie est gelé avant exécution, et qu'il ferme la rupture R3 que le dépôt qualifie lui-même de CRITIQUE. C'est le seul endroit où le travail de spécification déjà payé peut se convertir immédiatement en capacité.

### Le point sur lequel je serais le plus insistant

L'asymétrie de rigueur. Vous avez construit un appareil de preuve remarquable autour de la donnée et de sa temporalité, et strictement rien autour du risque. Pour un compte prop firm, c'est l'inverse de la hiérarchie des conséquences : une date de session mal qualifiée fausse un backtest, une taille de position mal contrôlée fait sauter un compte. Cette asymétrie n'est pas justifiée nulle part dans le dépôt — elle a l'air d'un effet de séquence, pas d'un choix. Elle mérite d'être arbitrée explicitement.

---

## 11. Méthode, contrôle anti-hallucination et limites

### Méthode d'audit

Clone complet du dépôt. Comparaison des 86 branches distantes par date de dernier commit. Lecture intégrale des documents de référence et de récupération, puis du corpus normatif et du code. Exécution locale des suites de tests sur cinq branches distinctes. Réexécution des outils de couverture pour confronter les chiffres des rapports figés à la réalité courante. Tentative active de contournement des frontières de confiance.

### Contrôle anti-hallucination appliqué

Chaque bloc marqué EXISTANT renvoie à un fichier vérifié et, quand c'est possible, à une exécution que j'ai reproduite. Chaque liaison marquée opérationnelle a été confirmée par lecture du code du producteur et du consommateur, pas par la seule existence des deux fichiers. Chaque capacité marquée fonctionnelle distingue explicitement preuve d'exécution et spécification. Chaque élément TARGET provient de 01-SYSTEM-VISION ou de STEP-2-MINIMAL-SYSTEM-TARGET, jamais de mon inférence — les deux seules propositions qui viennent de moi sont marquées « NOUVELLE HYPOTHÈSE — non décidée » dans les améliorations.

### Ce que je n'ai pas pu vérifier

Les runs GitHub Actions cités dans les rapports (identifiants et jobs) n'ont pas été consultés : je n'ai pas d'accès authentifié à l'onglet Actions. Je les rapporte comme des affirmations du dépôt, pas comme des preuves que j'ai constatées. Le contenu des 5 issues et 10 pull requests ouvertes n'a pas été inspecté systématiquement. Enfin, sur les 86 branches, j'ai analysé en profondeur les 8 plus récentes et significatives ; les autres ont été datées et comparées par diff, sans lecture intégrale.

---

## 12. Annexes

### 12.1 Index des composants par statut

**🟢 EXISTANT (11)** — AI Operating Memory · Repository Safety Rules · Frontière humaine / décision normative · 04 — Validation Criteria v0.6.2 · tick_reader · dataset_admissibility · input_binding — capacité BoundResearchInput · Audit de couverture calendrier · Protocole de récupération des Trading Breaks · Machine à lots — Batches 01 → 11 · Règle du gap irréductible de preuve broker

**🟡 PARTIEL (8)** — 08 — System Registry + registres 09→14 · bi5_reader + contrat d'instrument · Sonde V4.3 — compatibilité recherche ↔ exécution · Context + context_identity · ResearchRunEvidence · DecisionTrace · Chaîne synthétique bout en bout · Audit exécutable + boucle de révision

**🔵 SPECIFIE (5)** — Experimental Memory Charter · 01 — System Vision · Momentum V1 — définition + protocole baseline · Architecture de sortie de position · Mémoire expérimentale

**⚪ CIBLE (2)** — Moteur de décision (Context Engine, Router, multi-horizon) · Risk Engine + Portfolio Engine

**🔴 MANQUANT (5)** — Qualification Input Register — 10 entrées BLOCKED · Sélection et gel de la fenêtre d'exécution · produce_decision — frontière RESEARCH → DECISION · Producteur d'action / exécution · Observation de résultat / attribution

**🟣 EXTERNE (3)** — Dukascopy — ticks BI5 + widget Trading Breaks · VT Markets / MT5 — flux d'exécution · GitHub Actions

**⚠️ AMBIGU (2)** — Recovery Checkpoint · 05 — Data Contract v0.1

### 12.2 Index de toutes les preuves fichier

| Fichier | Branche | Composant | Lien |
|---|---|---|---|
| `04-REFERENCE/AI-OPERATING-MEMORY.md` | `main` | AI Operating Memory | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/04-REFERENCE/AI-OPERATING-MEMORY.md |
| `04-REFERENCE/RECOVERY-CHECKPOINT.md` | `main` | Recovery Checkpoint | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/04-REFERENCE/RECOVERY-CHECKPOINT.md |
| `04-REFERENCE/RECOVERY-CHECKPOINT.md` | `feat/multi-year-dukascopy-acquisition` | Recovery Checkpoint | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/04-REFERENCE/RECOVERY-CHECKPOINT.md |
| `GOVERNANCE/REPOSITORY-SAFETY-RULES.md` | `main` | Repository Safety Rules | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/GOVERNANCE/REPOSITORY-SAFETY-RULES.md |
| `GOVERNANCE/DECISION-SUPPORT-AND-HUMAN-BOUNDARY.md` | `main` | Frontière humaine / décision normative | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/GOVERNANCE/DECISION-SUPPORT-AND-HUMAN-BOUNDARY.md |
| `GOVERNANCE/EXPERIMENTAL-MEMORY-CHARTER.md` | `main` | Experimental Memory Charter | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/GOVERNANCE/EXPERIMENTAL-MEMORY-CHARTER.md |
| `docs/01-SYSTEM-VISION.md` | `main` | 01 — System Vision | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/01-SYSTEM-VISION.md |
| `docs/04-VALIDATION-CRITERIA.md` | `main` | 04 — Validation Criteria v0.6.2 | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/04-VALIDATION-CRITERIA.md |
| `docs/14-AUDIT-PHASE-A-STATUS.md` | `main` | 04 — Validation Criteria v0.6.2 | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/14-AUDIT-PHASE-A-STATUS.md |
| `docs/05-DATA-CONTRACT.md` | `main` | 05 — Data Contract v0.1 | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/05-DATA-CONTRACT.md |
| `docs/08-SYSTEM-REGISTRY.md` | `main` | 05 — Data Contract v0.1 | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/08-SYSTEM-REGISTRY.md |
| `docs/08-SYSTEM-REGISTRY.md` | `main` | 08 — System Registry + registres 09→14 | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/08-SYSTEM-REGISTRY.md |
| `docs/09-DATASET-PROVENANCE-REGISTRY.md` | `main` | 08 — System Registry + registres 09→14 | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/09-DATASET-PROVENANCE-REGISTRY.md |
| `docs/10-TEMPORAL-POINT-IN-TIME-CONTRACT.md` | `main` | 08 — System Registry + registres 09→14 | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/10-TEMPORAL-POINT-IN-TIME-CONTRACT.md |
| `docs/11-CONTRADICTION-ARBITRATION-REGISTRY.md` | `main` | 08 — System Registry + registres 09→14 | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/11-CONTRADICTION-ARBITRATION-REGISTRY.md |
| `docs/13-CRITICALITY-AUDIT-PROTOCOL.md` | `main` | 08 — System Registry + registres 09→14 | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/13-CRITICALITY-AUDIT-PROTOCOL.md |
| `docs/QUALIFICATION-INPUT-REGISTER-V1-BLOCKED.md` | `main` | Qualification Input Register — 10 entrées BLOCKED | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/QUALIFICATION-INPUT-REGISTER-V1-BLOCKED.md |
| `docs/ADJUDICATION-GLOBAL-EXECUTABLE-GATE-RB-A-Q-RM-01-12-V1-2026-09-05.md` | `main` | Qualification Input Register — 10 entrées BLOCKED | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/ADJUDICATION-GLOBAL-EXECUTABLE-GATE-RB-A-Q-RM-01-12-V1-2026-09-05.md |
| `src/data/tick_reader.py` | `main` | tick_reader | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/src/data/tick_reader.py |
| `tests/test_tick_reader.py` | `main` | tick_reader | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/tests/test_tick_reader.py |
| `src/data/dataset_admissibility.py` | `main` | dataset_admissibility | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/src/data/dataset_admissibility.py |
| `tests/test_dataset_admissibility.py` | `main` | dataset_admissibility | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/tests/test_dataset_admissibility.py |
| `src/research/input_binding.py` | `feat/multi-year-dukascopy-acquisition` | input_binding — capacité BoundResearchInput | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/src/research/input_binding.py |
| `src/research/engine.py` | `feat/multi-year-dukascopy-acquisition` | input_binding — capacité BoundResearchInput | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/src/research/engine.py |
| `src/research/execution.py` | `feat/multi-year-dukascopy-acquisition` | input_binding — capacité BoundResearchInput | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/src/research/execution.py |
| `src/research/bi5_reader.py` | `feat/multi-year-dukascopy-acquisition` | bi5_reader + contrat d'instrument | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/src/research/bi5_reader.py |
| `docs/04-REFERENCE/INSTRUMENT-CONTRACTS/USATECHIDXUSD-Dukascopy-BI5.json` | `feat/multi-year-dukascopy-acquisition` | bi5_reader + contrat d'instrument | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/docs/04-REFERENCE/INSTRUMENT-CONTRACTS/USATECHIDXUSD-Dukascopy-BI5.json |
| `tests/test_instrument_contract_v4_3.py` | `feat/multi-year-dukascopy-acquisition` | bi5_reader + contrat d'instrument | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tests/test_instrument_contract_v4_3.py |
| `tools/probe_research_execution_compatibility_v4_3.py` | `main` | Sonde V4.3 — compatibilité recherche ↔ exécution | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/tools/probe_research_execution_compatibility_v4_3.py |
| `tools/dukascopy_usatech_calendar_coverage.py` | `feat/multi-year-dukascopy-acquisition` | Audit de couverture calendrier | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/dukascopy_usatech_calendar_coverage.py |
| `tools/dukascopy_usatech_calendar.py` | `feat/multi-year-dukascopy-acquisition` | Audit de couverture calendrier | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/dukascopy_usatech_calendar.py |
| `reports/data-qualification/dukascopy_usatech_global_calendar_coverage_audit.md` | `feat/multi-year-dukascopy-acquisition` | Audit de couverture calendrier | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/reports/data-qualification/dukascopy_usatech_global_calendar_coverage_audit.md |
| `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md` | `feat/multi-year-dukascopy-acquisition` | Protocole de récupération des Trading Breaks | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md |
| `tools/trading_breaks_recovery_protocol.py` | `feat/multi-year-dukascopy-acquisition` | Protocole de récupération des Trading Breaks | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/trading_breaks_recovery_protocol.py |
| `tests/test_trading_breaks_recovery_protocol.py` | `feat/multi-year-dukascopy-acquisition` | Protocole de récupération des Trading Breaks | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tests/test_trading_breaks_recovery_protocol.py |
| `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md` | `feat/multi-year-dukascopy-acquisition` | Machine à lots — Batches 01 → 11 | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md |
| `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH11-POLICY.md` | `feat/multi-year-dukascopy-acquisition` | Machine à lots — Batches 01 → 11 | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH11-POLICY.md |
| `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json` | `feat/multi-year-dukascopy-acquisition` | Machine à lots — Batches 01 → 11 | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json |
| `04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md` | `feat/multi-year-dukascopy-acquisition` | Règle du gap irréductible de preuve broker | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md |
| `tools/irreducible_historical_broker_evidence_gap.py` | `feat/multi-year-dukascopy-acquisition` | Règle du gap irréductible de preuve broker | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/irreducible_historical_broker_evidence_gap.py |
| `04-REFERENCE/EXECUTION-WINDOW-SELECTION-RULE.md` | `feat/multi-year-dukascopy-acquisition` | Sélection et gel de la fenêtre d'exécution | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/04-REFERENCE/EXECUTION-WINDOW-SELECTION-RULE.md |
| `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md` | `feat/multi-year-dukascopy-acquisition` | Sélection et gel de la fenêtre d'exécution | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md |
| `tools/coverage_execution_window_boundary.py` | `feat/multi-year-dukascopy-acquisition` | Sélection et gel de la fenêtre d'exécution | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/coverage_execution_window_boundary.py |
| `src/context.py` | `feat/decision-producer-contract` | Context + context_identity | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/src/context.py |
| `src/context_identity.py` | `feat/decision-producer-contract` | Context + context_identity | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/src/context_identity.py |
| `tests/test_data_to_context.py` | `feat/decision-producer-contract` | Context + context_identity | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/tests/test_data_to_context.py |
| `src/research_run_evidence.py` | `feat/decision-producer-contract` | ResearchRunEvidence | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/src/research_run_evidence.py |
| `docs/RESEARCH-FINDINGS-CONTRACT.md` | `feat/decision-producer-contract` | ResearchRunEvidence | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/docs/RESEARCH-FINDINGS-CONTRACT.md |
| `docs/03.1.1-MOMENTUM-V1-DEFINITION.md` | `feat/multi-year-dukascopy-acquisition` | Momentum V1 — définition + protocole baseline | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/docs/03.1.1-MOMENTUM-V1-DEFINITION.md |
| `docs/03.1.2-MOMENTUM-V1-BASELINE-PROTOCOL.md` | `feat/multi-year-dukascopy-acquisition` | Momentum V1 — définition + protocole baseline | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/docs/03.1.2-MOMENTUM-V1-BASELINE-PROTOCOL.md |
| `reports/research/3_1_2_momentum_v1_baseline_adversarial_report.md` | `feat/multi-year-dukascopy-acquisition` | Momentum V1 — définition + protocole baseline | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/reports/research/3_1_2_momentum_v1_baseline_adversarial_report.md |
| `src/decision.py` | `feat/decision-producer-contract` | produce_decision — frontière RESEARCH → DECISION | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/src/decision.py |
| `tests/test_research_to_decision_boundary.py` | `feat/decision-producer-contract` | produce_decision — frontière RESEARCH → DECISION | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/tests/test_research_to_decision_boundary.py |
| `tests/test_context_research_alternative_paths.py` | `feat/decision-producer-contract` | produce_decision — frontière RESEARCH → DECISION | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/tests/test_context_research_alternative_paths.py |
| `docs/01-SYSTEM-VISION.md` | `main` | Moteur de décision (Context Engine, Router, multi-horizon) | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/01-SYSTEM-VISION.md |
| `docs/01-SYSTEM-VISION.md` | `main` | Risk Engine + Portfolio Engine | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/docs/01-SYSTEM-VISION.md |
| `04-REFERENCE/ARCHITECTURE-SORTIE-POSITION.md` | `main` | Architecture de sortie de position | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/04-REFERENCE/ARCHITECTURE-SORTIE-POSITION.md |
| `src/synthetic_end_to_end.py` | `feat/synthetic-end-to-end-chain` | Producteur d'action / exécution | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/synthetic-end-to-end-chain/src/synthetic_end_to_end.py |
| `src/synthetic_end_to_end.py` | `feat/synthetic-end-to-end-chain` | Observation de résultat / attribution | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/synthetic-end-to-end-chain/src/synthetic_end_to_end.py |
| `src/decision_trace.py` | `feat/decision-producer-contract` | DecisionTrace | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/src/decision_trace.py |
| `tests/test_decision_trace.py` | `feat/synthetic-end-to-end-chain` | DecisionTrace | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/synthetic-end-to-end-chain/tests/test_decision_trace.py |
| `src/synthetic_end_to_end.py` | `feat/synthetic-end-to-end-chain` | Chaîne synthétique bout en bout | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/synthetic-end-to-end-chain/src/synthetic_end_to_end.py |
| `tests/test_synthetic_foreign_identity_links.py` | `feat/synthetic-end-to-end-chain` | Chaîne synthétique bout en bout | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/synthetic-end-to-end-chain/tests/test_synthetic_foreign_identity_links.py |
| `.github/workflows/synthetic-foreign-identity.yml` | `feat/synthetic-end-to-end-chain` | Chaîne synthétique bout en bout | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/synthetic-end-to-end-chain/.github/workflows/synthetic-foreign-identity.yml |
| `GOVERNANCE/EXPERIMENTAL-MEMORY-CHARTER.md` | `main` | Mémoire expérimentale | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/GOVERNANCE/EXPERIMENTAL-MEMORY-CHARTER.md |
| `99-BACKUP/README.md` | `feat/multi-year-dukascopy-acquisition` | Mémoire expérimentale | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/99-BACKUP/README.md |
| `tools/trading_breaks_recovery_batch11_adjudication.py` | `feat/multi-year-dukascopy-acquisition` | Audit exécutable + boucle de révision | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/trading_breaks_recovery_batch11_adjudication.py |
| `tools/integrate_trading_breaks_recovery_batch10.py` | `feat/multi-year-dukascopy-acquisition` | Audit exécutable + boucle de révision | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/integrate_trading_breaks_recovery_batch10.py |
| `GOVERNANCE/GOVERNANCE-EVOLUTION-AND-AUDIT-PROTOCOL.md` | `main` | Audit exécutable + boucle de révision | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/GOVERNANCE/GOVERNANCE-EVOLUTION-AND-AUDIT-PROTOCOL.md |
| `tools/probe_dukascopy_trading_breaks_widget.py` | `feat/multi-year-dukascopy-acquisition` | Dukascopy — ticks BI5 + widget Trading Breaks | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/probe_dukascopy_trading_breaks_widget.py |
| `tools/download_dukascopy_tick_corpus.py` | `feat/multi-year-dukascopy-acquisition` | Dukascopy — ticks BI5 + widget Trading Breaks | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/tools/download_dukascopy_tick_corpus.py |
| `tools/probe_research_execution_compatibility_v4_3.py` | `main` | VT Markets / MT5 — flux d'exécution | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/main/tools/probe_research_execution_compatibility_v4_3.py |
| `.github/workflows/trading-breaks-recovery-batch11.yml` | `feat/multi-year-dukascopy-acquisition` | GitHub Actions | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/multi-year-dukascopy-acquisition/.github/workflows/trading-breaks-recovery-batch11.yml |
| `.github/workflows/research-to-decision-boundary.yml` | `feat/decision-producer-contract` | GitHub Actions | https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/blob/feat/decision-producer-contract/.github/workflows/research-to-decision-boundary.yml |

### 12.3 Réponses directes aux questions de cadrage

| Question | Où se trouve la réponse |
|---|---|
| Qu'est-ce que mon système ? | Une machine à qualification de preuves qui n'a pas encore atteint la couche trading, et qui le sait, l'écrit et le fait respecter par du code. Voir §10. |
| Quels sont ses grands sous-systèmes ? | 13 couches, du monde extérieur à la boucle mémoire/audit/révision. Voir §3.1. |
| Pourquoi chacun existe-t-il ? | Champ « Rôle » de chaque fiche, §4. |
| Quelles informations entrent dans chaque composant ? | Champ « Entrées » de chaque fiche, §4. |
| Qu'en sort-il ? | Champ « Sorties » de chaque fiche, §4. |
| Qui dépend de quoi ? | §3.2 pour les frontières internes, §8 pour les dépendances externes. |
| Quelles frontières empêchent les contournements ? | §3.2. Les plus solides : identité des octets par SHA-256 (DATA), capacité BoundResearchInput (corpus BI5), contrat de preuve positive à 14 conditions (calendrier). |
| Qu'est-ce qui fonctionne réellement aujourd'hui ? | §5 vue NOW, statuts EXISTANT. §6 catégorie CAN DO. |
| Qu'est-ce qui est seulement documenté ? | §5, statuts SPECIFIE et CIBLE. Détail en §10. |
| Qu'est-ce qui reste à construire ? | §5 vue GAP, et §9 catégorie GAP OBLIGATOIRE. |
| Quelle est la distance entre NOW et TARGET ? | Non uniforme. §10, section « La distance NOW → TARGET ». |
| Que sait réellement faire le système ? | §6, CAN DO. |
| Dans quelles conditions sait-il le faire ? | §6 colonne « Limites / conditions », et champ « Fonctionne si » de chaque fiche. |
| Quand doit-il refuser de fonctionner ? | §6 catégorie MUST REFUSE, et champ « Doit refuser si » de chaque fiche. |
| Où peut-il échouer ? | §7, 13 modes de défaillance confirmés. |
| Qu'est-ce qui protège contre ces échecs ? | §7 champ « Protection actuelle » de chaque mode. |
| Quels éléments ne sont pas suffisamment prouvés ? | §6 catégorie UNKNOWN / NOT PROVEN, et statuts AMBIGU en §12.1. |
| Quelles améliorations sont prioritaires ? | §9, catégorie GAP OBLIGATOIRE, priorités P1. |
| Pourquoi ces améliorations sont-elles prioritaires ? | §9 champs « Problème et preuve » et « Conséquence si rien n'est fait ». |
| Quel est le prochain maillon architectural rationnel à construire ? | Momentum V1. §10, troisième lacune structurante. |

---

*Export généré mécaniquement depuis le modèle de données de l'Artifact. Snapshot du 15 septembre 2026. Aucune conclusion n'a été modifiée ni re-auditée.*
