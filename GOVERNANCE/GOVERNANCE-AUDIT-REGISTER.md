# GOVERNANCE — AUDIT REGISTER

**Status:** AUDIT EXÉCUTÉ — ARCHITECTURE / PREUVE D'IMPLÉMENTATION À DISTINGUER
**Date:** 12 septembre 2026
**Périmètre:** audit minimal de la gouvernance existante du dépôt

## Question fondamentale

> **Comment savons-nous que la gouvernance existante couvre réellement les risques critiques, sans duplication ni complexité inutile, et comment découvrons-nous ce qu'elle ne contrôle pas encore ?**

## Méthode

`EXIGENCE → EXISTANT → PREUVE → GAP → RISQUE → INTÉGRATION MINIMALE → CASSAGE → RE-CASSAGE → VERDICT`

Verdicts : `PASS / FAIL / BLOCKED`.

> Un mécanisme documentaire existant ne constitue pas une preuve d'implémentation opérationnelle.

## Résultats

| Exigence | Existant / preuve | Gap constaté | Risque | Intégration minimale | Verdict |
|---|---|---|---|---|---|
| **1. Change / Validity** | `GOVERNANCE/META-GOVERNANCE-AND-SELF-CHALLENGE.md` couvre le drift, les conditions d'invalidation et la question « Est-elle encore vraie ici et maintenant ? ». `docs/09` et `docs/10` définissent provenance, validité/knowledge time et admissibilité point-in-time. | Les contrats `09/10` restent explicitement des propositions et leur exécution n'est pas démontrée. `08` confirme que la bitemporalité n'est pas encore gelée. | Une connaissance peut avoir été correctement validée dans un contexte donné et devenir invalide ensuite. | Ne rien ajouter. Lors de l'intégration, faire passer `09/10` par arbitrage + tests d'admissibilité et de drift. | **BLOCKED** |
| **2. Decision Traceability** | `docs/09` impose la chaîne `RESULT → RESEARCH_RUN → CODE_VERSION → CONFIGURATION_VERSION → DATASET_VERSION/HASH → PROVENANCE`. `docs/08` définit propriétaires/producteurs/dépositaires/consommateurs. | La reconstruction complète d'une **décision opérationnelle** (état, informations disponibles, connaissances actives, contraintes, alternatives, incertitude, décision, action, résultat) n'est pas encore démontrée comme un artefact exécutable transverse. | Impossible de garantir aujourd'hui une reconstruction complète et reproductible du « pourquoi cette décision, à cet instant ». | Réutiliser provenance + registry + journal de décision existants/cibles ; ne créer une nouvelle couche que si le test de reconstruction échoue. | **FAIL** |
| **3. Resilience / Continuity** | Des mécanismes de version, provenance, hashes et reproductibilité existent conceptuellement (`09`, `10`, règles de dépôt). | Aucun dispositif démontré couvrant explicitement restauration, récupération après perte, portabilité, continuité du savoir et test de restauration. `08` ne recense pas de contrat de continuité opérationnel. | Perte d'un composant, d'une donnée ou d'un environnement pouvant rendre le système non reconstructible malgré une bonne gouvernance documentaire. | Ajouter ultérieurement un contrôle de continuité/recovery au niveau de l'exécution et des dépôts, sans créer de nouveau framework si les mécanismes existants suffisent. | **FAIL** |
| **4. Governance Effectiveness** | `META-GOVERNANCE-AND-SELF-CHALLENGE` impose auto-contestation, adversarial testing, re-test, verdicts et contestation périodique. `11` conserve les contradictions et permet la réouverture. `13` définit l'audit critique. | L'efficacité réelle de ces mécanismes n'est pas encore démontrée par une série d'audits exécutés/reproductibles montrant qu'ils détectent effectivement des problèmes qu'ils étaient censés détecter. | La gouvernance pourrait être correcte sur le papier mais incapable de détecter ses propres angles morts. | Exécuter périodiquement des audits adversariaux réels et conserver leurs résultats dans la mémoire/registre existant. Pas de nouvelle couche tant que ce test n'a pas échoué. | **BLOCKED** |

## Verdict global

**La gouvernance conceptuelle est désormais suffisamment structurée pour arrêter d'ajouter des couches documentaires.**

Mais **elle n'est pas encore suffisante pour déclarer la gouvernance opérationnellement robuste**.

Les deux gaps réels sont :

1. **traçabilité complète de la décision opérationnelle** — FAIL ;
2. **continuité / restauration testée** — FAIL.

Les deux autres sujets sont surtout **BLOCKED par absence de preuve d'exécution**, pas par absence de conception.

## Règle d'arrêt

**NE PAS CRÉER DE NOUVEAU DOCUMENT DE GOUVERNANCE MAINTENANT.**

La prochaine phase doit être l'implémentation et le test des mécanismes déjà définis :

`TRAÇABILITÉ → CONTINUITÉ/RESTAURATION → AUDIT ADVERSARIAL RÉEL → RE-TEST → VERDICT`.

Si ces tests démontrent que les mécanismes existants couvrent les exigences, **on s'arrête là**. Si un test révèle un gap précis, seule la correction minimale correspondante est ajoutée.


---

## Audit JIT — P0.0 rebaseline post-clôture

**Audit ID : `P0_FULL_SUITE_REBASELINE_JIT_AUDIT_V1`**
**Date :** 16 septembre 2026
**Périmètre couvert :** cohérence du corpus de régression après clôture Trading Breaks, présence du corpus de gouvernance supprimé sur la branche, et formalisation minimale de la carence avant assouplissement.
**Complément explicitement non audité :** dérivation probatoire de `BoundaryState`, freeze de fenêtre, jonction `src/research/` ↔ `research_run_evidence`, attestation inter-processus, couplage résiduel des workflows, dépendances/lockfile, promotion gate, acquisition `.bi5` et backtest réel.

Constats exécutés :

- le corpus pré-correction produisait `115 failed / 537 passed` parce que des tests historiques étaient exécutés comme s'ils décrivaient l'état courant ;
- les six documents de gouvernance absents de la branche ont été restaurés depuis `main` sans réécriture de leur contenu ;
- les 115 node IDs historiques sont conservés et rejoués fail-closed contre 42 états Git historiquement verts ;
- aucun `skip`, `xfail` ou effacement de test n'est utilisé pour obtenir le vert ;
- la vérité courante post-clôture est testée séparément ;
- la règle `GOVERNANCE_RELAXATION_COOLING_OFF_V1` est ajoutée au protocole existant au lieu de créer une nouvelle couche documentaire.

**Verdict de cet audit borné : PASS**, sous réserve du re-break persisted-HEAD de la suite complète après cette modification. Ce PASS ne vaut pas audit global de gouvernance et ne ferme aucun élément du complément non audité.

---

## Audit JIT — P0.2 controlled decision-block integration

**Audit ID : `P0_2_DECISION_BLOCK_INTEGRATION_JIT_AUDIT_V1`**  
**Date :** 16 septembre 2026  
**Branche auditée :** `integration/system-v1`  
**Base autorisée :** `main@43ec28f3e09856fe508874af3aaf32079761d2d5`  
**Source fonctionnelle qualifiée :** `feat/decision-producer-contract@c0116d195063c464d602fb699654ac61adc7290c`

### Covered by P0.2

- création de la branche d'intégration depuis le HEAD exact de `main` ;
- import contrôlé, borné et source-identique des contrats `DATA → CONTEXT → RESEARCH FINDINGS → DECISION` retenus ;
- conservation de tous les fichiers de gouvernance déjà présents sur `main` ;
- remise au niveau courant de `AI-OPERATING-MEMORY`, du protocole d'évolution/audit et du registre d'audit ;
- absence de blind merge et absence de replay des suppressions de gouvernance de la branche feature ;
- provenance/identité de `ResearchRunEvidence` et refus des copies, reconstructions, mutations d'identité et auto-attestations forgées à la frontière `RESEARCH → DECISION` ;
- workflows durables branch-neutral, path-scoped, PR-covered et `contents: read` ;
- absence d'import du bloc multi-year, de `.bi5`, de données d'acquisition ou de backtest réel.

### Explicitly not covered by P0.2

- fermeture de la jonction de production réelle `src/research/` → `ResearchRunEvidence` ;
- attestation inter-processus ;
- chaîne `DECISION → RISK → ACTION → RESULT → TRACE` complète ;
- reconstruction transverse complète d'une décision opérationnelle jusqu'au résultat ;
- import du workstream multi-year Dukascopy / Trading Breaks / frozen execution window ;
- exact OOS split ;
- acquisition native `.bi5`, manifeste d'acquisition, exhaustivité des ticks et réconciliation ;
- backtest réel, promotion gate ou activation live.

### Preuves exécutées

- candidat d'intégration : `fa43c44739e75c8d927626a2b3df8eefb185e00f` ;
- re-break P0.2 : run/job `35130280160 / 104909282190` — SUCCESS ;
- suite dépôt : `96 passed` ;
- suite Tier-A ciblée : `83 passed` ;
- workflows durables individuels DATA→CONTEXT, CONTEXT→RESEARCH, RESEARCH FINDINGS et RESEARCH→DECISION : SUCCESS ;
- attaques de forgeabilité/provenance : PASS ;
- worktree : clean ;
- permissions du re-break : `contents: read`.

**Verdict JIT P0.2 : PASS pour le périmètre couvert uniquement.**

Ce PASS ne modifie pas les verdicts globaux historiques `Decision Traceability = FAIL` et `Resilience / Continuity = FAIL` tant que les chaînes transverses correspondantes ne sont pas démontrées de bout en bout.

---

## Audit JIT — P0.3 controlled multi-year integration

**Audit ID : `P0_3_MULTI_YEAR_INTEGRATION_JIT_AUDIT_V1`**  
**Date :** 16 septembre 2026  
**Branche auditée :** `integration/system-v1`  
**Base P0.2 :** `45d9bc8c4bf133eced67ccede7c5f439253869b7`  
**Source multi-year qualifiée :** `feat/multi-year-dukascopy-acquisition@b7d13bb3492fb6e1f0d4dcab64079bf1a8f55698`

### Covered by P0.3

- import explicite par allowlist de la surface minimale courante nécessaire à la dérivation calendrier/fenêtre/freeze ;
- identité octet-pour-octet des 19 artefacts importés avec le HEAD multi-year qualifié ;
- préservation intégrale des 24 artefacts qualifiés du bloc décision P0.2 ;
- dérivation actuelle de la vérité globale `111 / 91 / 20` et de la fenêtre `68 / 68 / 0` ;
- conservation visible des 20 gaps globaux hors fenêtre, tous antérieurs au `2021-08-14` ;
- état terminal Trading Breaks : 73 tentatives, 1 changement de capacité, queue/progression/éligibilité vides ;
- fenêtre gelée `2021-08-14 → 2026-08-14` : PASS ;
- couverture globale : toujours BLOCKED ;
- acquisition massive après freeze : toujours BLOCKED ;
- anti-forgeabilité/provenance `RESEARCH → DECISION` re-cassée avec le bloc multi-year présent ;
- exclusion explicite des tests d'état historique pré-clôture comme tests de vérité courante ;
- absence d'import de `.bi5`, de downloader, de probes Dukascopy, d'activateur de capacité, de scripts de récupération historique et de backtest réel.

### Explicitly not covered by P0.3

- jonction de production réelle `src/research/` → `ResearchRunEvidence` ;
- attestation inter-processus ;
- protocole natif d'acquisition `.bi5`, readiness des gates d'acquisition, manifeste/exhaustivité/réconciliation des ticks ;
- exact OOS split ;
- chaîne `DECISION → RISK → ACTION → RESULT → TRACE` complète ;
- reconstruction transverse complète d'une décision jusqu'au résultat ;
- résilience/restauration ;
- backtest réel ;
- promotion gate ou activation live.

### Preuves exécutées

- candidat P0.3 : `36e207abf779c02ea99f2d2e66ddf4b6bc7103d2` ;
- re-break combiné : run/job `35132710182 / 104917355632` — SUCCESS ;
- suite dépôt combinée : `176 passed` ;
- suite Tier-A décision : `83 passed` ;
- suite Tier-A calendar/freeze : `80 passed` ;
- dérivation `111/91/20`, `68/68/0`, freeze PASS et acquisition BLOCKED : PASS ;
- anti-forgeabilité décision : PASS ;
- allowlist/source identity/governance preservation : PASS ;
- worktree : clean ;
- permissions : `contents: read`, `metadata: read`.

**Verdict JIT P0.3 : PASS pour le périmètre couvert uniquement, sous réserve du re-break persisted-HEAD du commit de clôture.**

Ce PASS ne transforme ni la couverture globale en PASS, ni l'acquisition `.bi5`, ni le backtest réel en action autorisée.

---

## Audit JIT — P0.4 real research producer junction

**Audit ID : `P0_4_RESEARCH_PRODUCER_JUNCTION_JIT_AUDIT_V1`**  
**Date :** 16 septembre 2026  
**Branche auditée :** `integration/system-v1`  
**Contrat :** `RESEARCH_PRODUCER_JUNCTION_V1`

### Covered by P0.4

- cartographie de `src/research/` face au contrat intégré `ResearchRunEvidence` ;
- intégration bornée à exactement cinq fichiers runtime : `__init__.py`, `bi5_reader.py`, `input_binding.py`, `engine.py`, `execution.py` ;
- identité source conservée pour `__init__.py` et `bi5_reader.py` depuis `feat/multi-year-dukascopy-acquisition@b7d13bb3492fb6e1f0d4dcab64079bf1a8f55698` ;
- jonction réelle `QualifiedResearchInput → BoundResearchInput → deterministic runtime execution → ResearchExecutionResult → ResearchRunEvidence` ;
- attestation process-locale liée à l'identité/contenu du bound input et du résultat d'exécution ;
- rejet d'une exécution vide ;
- cohérence obligatoire corpus/contract hashes, Dataset, Context, bornes temporelles et code version ;
- chemin V4.3 report-only conservé comme compatibilité mais rendu non autorisant ;
- suppression du minter brut `_attest_factory_evidence` de la surface module ;
- cassage adversarial C0 + C1–C15 : report-only, minter/manual forge, copies/reconstructions, mutations post-binding/post-exécution, mutation des bytes source, rebinding résultat/input, exécution vide, Dataset/Context/code forgés et contournement downstream ;
- qualification avec fixtures BI5 synthétiques locales uniquement ;
- préservation/composabilité des frontières P0.2 et P0.3 ;
- absence d'acquisition `.bi5`, de probe réseau, de données d'acquisition et de backtest réel.

### Explicitly not covered by P0.4

- attestation inter-processus ou persistée ;
- protocole/readiness/autorisation d'acquisition native `.bi5` ;
- manifeste d'acquisition, exhaustivité/completude/reconciliation des ticks ;
- exact OOS split ;
- backtest réel sur données acquises ;
- chaîne `DECISION → RISK → ACTION → RESULT → TRACE` complète ;
- reconstruction transverse complète d'une décision jusqu'au résultat ;
- résilience/restauration ;
- promotion gate ou activation live.

### Preuve de cassage avant correction

HEAD : `5619f6d3ae608bf9a3f0871345815b7906a6caba`  
Run/job : `35136475040 / 104929994347` — **FAIL attendu**.

Les 56 tests hérités étaient verts puis les trois bypasses cartographiés ont échoué : report-only autorisant, minter brut exposé, promotion manuelle possible.

### Preuve de correction C0–C15

HEAD : `edb2501a2b09bd142f037a82f6971696c08c1213`  
Run/job : `35137560719 / 104933628790` — **SUCCESS**.

- suite dépôt : `192 passed` ;
- C0–C15 : `16 passed` ;
- décision Tier-A : `73 passed` ;
- calendar/freeze Tier-A : `80 passed` ;
- runtime exactement cinq fichiers : PASS ;
- raw minter absent : PASS ;
- worktree clean ;
- permissions read-only.

### Preuve combinée same-SHA

HEAD commun : `3b09bd9f6e06fd8833f7bd93d98e839e335000b5`.

- P0.2 run/job `35140401689 / 104943189786` — **SUCCESS** — `83 passed` ;
- P0.3 run/job `35140401667 / 104943190208` — **SUCCESS** — `72 passed` amont + `80 passed` calendar/freeze ;
- P0.4 run/job `35140401707 / 104943190275` — **SUCCESS** — `192 passed` dépôt + `16 passed` C0–C15 + `73 passed` décision + `80 passed` calendar/freeze.

Les trois gates sont read-only et terminent avec un worktree propre.

La vérité multi-year reste inchangée : global `111/91/20` **BLOCKED**, selected window `68/68/0` PASS, acquisition **BLOCKED**.

**Verdict JIT P0.4 : PASS pour le périmètre couvert uniquement**, sous réserve du dernier re-break persisted-HEAD documentaire de l'exact HEAD contenant audit + rapport + checkpoint + backup + verifier final.

Ce PASS borné ne modifie aucun verdict global non couvert et n'autorise ni acquisition native, ni backtest réel, ni promotion/live.

---

## Audit JIT — P0.5 durable RESEARCH inter-process replay re-attestation

**Audit ID : `P0_5_RESEARCH_INTERPROCESS_REATTESTATION_JIT_AUDIT_V1`**  
**Date :** 16 septembre 2026  
**Branche auditée :** `integration/system-v1`  
**Contrat :** `RESEARCH_INTERPROCESS_REATTESTATION_V1`  
**Base P0.4 :** `aa9551addc0fe554af9cbb8ebdb26314d37e412e`

### Covered by P0.5

- fermeture de la limite process-local identifiée par P0.4 au moyen d'une re-attestation par replay déterministe ;
- preuve persistée canonique et content-addressed, non autorisante par elle-même ;
- code version attendu fourni séparément par le consommateur ;
- chemins corpus/contract fournis séparément et identité basée sur les bytes, pas sur les chemins ;
- revalidation des bytes source puis réexécution dans le processus consommateur ;
- comparaison exacte execution/Dataset/Context/ResearchRunEvidence avant toute nouvelle attestation ;
- rejet d'un digest JSON recalculé après falsification ;
- rejet de preuve renommée, schéma incomplet/inconnu/dupliqué/substitué, sources modifiées et identités forgées ;
- rejet des preuves V4.3 report-only et des preuves issues de copies/reconstructions/mutations d'evidence ;
- acceptation de sources byte-identiques relocalisées ;
- reconstruction d'une nouvelle autorité P0.4 uniquement après replay ;
- préservation de P0.2/P0.3/P0.4 et des interdictions acquisition/backtest.

### Explicitly not covered by P0.5

- bearer proof cryptographique non-replay ;
- génération, garde, rotation ou révocation de clés ;
- lock global des dépendances et de l'environnement ;
- fermeture de tout couplage résiduel des workflows d'intégration ;
- acquisition native `.bi5`, manifestes, exhaustivité et réconciliation ;
- exact OOS split ;
- backtest réel ;
- chaîne `DECISION → RISK → ACTION → RESULT → TRACE` complète ;
- reconstruction transverse complète de la décision ;
- résilience/restauration générale ;
- promotion gate ou activation live.

### Preuve de cassage avant correction

HEAD : `36f97ee715655f6b2470e7836f7c82e6285aa237`  
Run/job : `35143592655 / 104953910890` — **FAIL attendu**.

- P0.4 C0–C15 : `16 passed` ;
- P0.5 provisional : `1 failed / 1 passed` ;
- défaut observé : aucun pont durable writer/re-attestation n'existait ;
- raw serialized evidence restait non autorisant ;
- gate read-only, aucun side effect acquisition/backtest ;
- worktree clean.

### Preuve D0–D14 après correction

HEAD : `7f864b2da4e5590df26ca5a152e84cd67a362d98`  
Run/job : `35144130840 / 104955745568` — **SUCCESS**.

- P0.5 D0–D14 : `15 passed` ;
- P0.4 C0–C15 : `16 passed` ;
- worktree clean.

### Preuve technique combinée

HEAD : `05b9752fff9f25ad2301c6385feba14848b4bb27`  
Run/job : `35144258717 / 104956179724` — **SUCCESS**.

- suite dépôt : `207 passed` ;
- P0.5 D0–D14 : `15 passed` ;
- P0.4 C0–C15 : `16 passed` ;
- P0.2 décision Tier-A : `83 passed` ;
- P0.3 calendar/freeze Tier-A : `80 passed` ;
- global `111/91/20` : BLOCKED ;
- selected `68/68/0` : PASS ;
- persisted freeze : PASS ;
- acquisition : BLOCKED ;
- `massive_acquisition_authorized = false` ;
- `real_backtest_authorized = false` ;
- permissions read-only ;
- worktree clean.

**Verdict JIT P0.5 : PASS pour le périmètre couvert uniquement**, sous réserve du dernier re-break persisted-HEAD documentaire de l'exact HEAD contenant audit + rapport + checkpoint + backup + verifier final.

Ce PASS ne transforme pas la preuve persistée en credential auto-authentifiant et n'autorise aucune acquisition, aucun backtest réel, aucune promotion ni activation live.