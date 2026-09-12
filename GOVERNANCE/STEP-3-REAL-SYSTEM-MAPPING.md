# ÉTAPE 3 — CARTOGRAPHIE DU SYSTÈME RÉEL EXISTANT

**Statut :** CARTOGRAPHIE FACTUELLE — AVANT CODAGE
**Branche :** `feat/step3-system-mapping`
**Base :** cible minimale gelée de l'ÉTAPE 2
**Règle :** cette cartographie ne crée aucun composant et ne transforme pas une branche expérimentale en composant intégré.

## 1. Règle de lecture

Le dépôt contient actuellement deux réalités qu'il faut séparer :

1. **Système effectivement présent sur `main`** : ce qui est réellement intégré à la branche de référence.
2. **Briques expérimentales présentes sur des branches séparées** : code existant et inspectable, mais non intégré à `main`.

Une branche expérimentale ne vaut donc pas preuve d'intégration.

## 2. État de `main`

Commit observé : `776e39262c58648d07e03634a04f406ab40dc158`.

La branche `main` contient notamment :

- `src/data/dataset_admissibility.py`
- `src/data/tick_reader.py`
- tests correspondants
- `tools/probe_research_execution_compatibility_v4_3.py`
- corpus documentaire `04-REFERENCE`, `docs`, `GOVERNANCE`

Le répertoire `src` de `main` ne contient que `__init__.py` et `data/`. Les briques `CONTEXT`, `DecisionTrace`, `ResearchRunEvidence` et la chaîne synthétique ne sont donc pas intégrées à `main`.

## 3. Cartographie fonctionnelle contre la cible

| Fonction cible | Existant réel | Localisation | Statut d'intégration | Producteur/consommateur identifiable | Rupture principale |
|---|---|---|---|---|---|
| DONNÉE | Lecteur de ticks + identité/admissibilité dataset | `src/data/tick_reader.py`, `src/data/dataset_admissibility.py` | **PASS — présent sur main** | Oui | La chaîne aval n'est pas reliée |
| CONTEXTE | Contrat d'identité expérimental | branche `feat/context-identity-contract-test-v7`, `src/context_identity.py` | **BLOCKED — branche séparée / preuve CI finale non établie** | Partiellement | Pas de CONTEXT intégré à main |
| RECHERCHE / EXPÉRIENCE | Preuve V4.3 + adaptateur `ResearchRunEvidence` | `src/research_run_evidence.py` sur branche synthétique | **BLOCKED — expérimental** | Recherche V4.3 oui ; expérience intégrée non | Pas de raccord réel DATA→CONTEXT→RESEARCH dans main |
| DÉCISION | `DecisionTrace` contient une décision mais ne produit pas de décision | `src/decision_trace.py` sur branche synthétique | **BLOCKED — projection expérimentale** | Trace oui ; moteur de décision non | Aucun producteur de décision opérationnel intégré |
| ACTION | Champ `action_id` + action synthétique de test | `src/decision_trace.py`, `src/synthetic_end_to_end.py` | **BLOCKED — synthétique** | Non pour l'opérationnel | Pas de producteur d'action réel |
| RÉSULTAT | Champ `result_id` + résultat synthétique de test | `src/decision_trace.py`, `src/synthetic_end_to_end.py` | **BLOCKED — synthétique** | Non pour l'opérationnel | Pas d'observation/résultat réel relié |
| TRACE | `DecisionTrace` reconstructible structurellement | `src/decision_trace.py` | **BLOCKED — branche séparée** | Projection de reconstruction | Absence d'intégration et validation d'identités amont/aval hors harness |
| MÉMOIRE | Charte d'architecture | `GOVERNANCE/EXPERIMENTAL-MEMORY-CHARTER.md` | **BLOCKED — spécification réservée, pas d'implémentation** | Non | Aucun stockage/modèle de mémoire expérimental intégré |
| AUDIT | Protocoles et registres documentaires de gouvernance | `GOVERNANCE/*`, `docs/08-SYSTEM-REGISTRY.md` | **BLOCKED — gouvernance documentaire** | Partiellement | Pas d'audit exécutable du parcours complet |
| RÉVISION | Principes de gouvernance et évolution | `GOVERNANCE/GOVERNANCE-EVOLUTION-AND-AUDIT-PROTOCOL.md` notamment | **BLOCKED — procédure/documentation** | Non comme boucle système | Pas de raccord exécutable résultat→mémoire→audit→révision |

## 4. Briques réelles déjà exécutables

### 4.1 DONNÉE

`dataset_admissibility.py` identifie les octets exacts par SHA-256 et vérifie notamment schéma, timestamps, domaine numérique, intégrité des quotes et ordre temporel. Il ne répare, ne trie ni ne déduplique la source. `tick_reader.py` lit les cinq champs source sans normalisation. 

**Conclusion :** frontière DATA réelle et exécutable. La rupture est en aval, pas dans l'existence du lecteur.

### 4.2 RECHERCHE / EXPÉRIENCE

Le dépôt possède déjà un outil V4.3 de compatibilité recherche/exécution sur `main`. Un adaptateur `ResearchRunEvidence` existe sur une branche expérimentale : il dérive des identifiants stables depuis le rapport V4.3 et les hashes des fichiers source, mais laisse explicitement décision/action/résultat/contexte vides lorsqu'ils ne sont pas fournis.

**Conclusion :** il existe une base de preuve de recherche, mais pas encore une continuité intégrée vers une décision réelle.

### 4.3 TRACE

`DecisionTrace` est une projection de reconstruction. Il détecte les champs obligatoires absents et refuse une reconstruction incomplète. Il ne crée ni moteur de décision ni registre de provenance.

**Conclusion :** bonne brique de reconstruction expérimentale, mais pas encore une trace de système intégré.

### 4.4 TEST DE CHAÎNAGE SYNTHÉTIQUE

`synthetic_end_to_end.py` construit une chaîne déterministe DATA→CONTEXT→EXPERIENCE→DECISION→ACTION→RESULT→TRACE et vérifie les identités des liaisons. Le workflow `synthetic-foreign-identity.yml` exécute des mutations d'identifiants étrangers.

**Conclusion :** preuve de test du câblage synthétique, pas preuve du système réel.

## 5. Ruptures de la chaîne minimale

### R1 — DATA → CONTEXT
**Rupture : FORTE**

DATA est exécutable sur `main`. CONTEXT n'est qu'une brique expérimentale séparée. Aucun raccord intégré ne démontre que la donnée réellement admise produit/alimente un contexte identifiable.

### R2 — CONTEXT → RECHERCHE / EXPÉRIENCE
**Rupture : FORTE**

L'expérience synthétique sait référencer un `context_id`, mais la recherche V4.3 réelle n'est pas raccordée à un CONTEXT opérationnel.

### R3 — RECHERCHE / EXPÉRIENCE → DÉCISION
**Rupture : CRITIQUE**

L'adaptateur V4.3 produit une preuve amont, pas une décision. `DecisionTrace` peut porter une décision mais n'en est pas le producteur. Aucun lien réel et exécutable ne relie actuellement une connaissance/expérience à une décision opérationnelle.

### R4 — DÉCISION → ACTION
**Rupture : CRITIQUE**

L'action existe uniquement dans le harness synthétique. Aucun producteur d'action opérationnel intégré n'a été identifié.

### R5 — ACTION → RÉSULTAT
**Rupture : CRITIQUE**

Le résultat existe dans le harness synthétique. Aucun producteur de résultat réel relié à une action n'a été identifié.

### R6 — RÉSULTAT → TRACE
**Rupture : CRITIQUE**

`DecisionTrace` peut référencer un `result_id`, mais aucune chaîne réelle ACTION→RESULT→TRACE n'est intégrée. La trace ne doit pas être utilisée pour inventer ce lien.

### R7 — TRACE → MÉMOIRE
**Rupture : TOTALE**

La charte de mémoire existe, mais aucun mécanisme de mémoire expérimentale exécutable n'a été identifié.

### R8 — MÉMOIRE → AUDIT
**Rupture : TOTALE**

Les règles d'audit/gouvernance existent sous forme documentaire, mais aucun raccord exécutable vers une mémoire d'expérience n'a été identifié.

### R9 — AUDIT → RÉVISION
**Rupture : TOTALE**

La gouvernance décrit l'évolution contrôlée, mais aucune boucle exécutable audit→révision→nouvelle expérience n'a été identifiée.

## 6. Ce qui existe réellement versus ce qui est seulement proposé

### Réel et intégré à `main`

- admissibilité et identité dataset ;
- lecture tick source ;
- tests DATA associés ;
- outil V4.3 de compatibilité recherche/exécution ;
- corpus de gouvernance/documentation.

### Réel mais non intégré

- identité déterministe CONTEXT ;
- `DecisionTrace` ;
- `ResearchRunEvidence` ;
- chaîne synthétique complète ;
- test adversarial des identités étrangères ;
- workflow CI correspondant.

### Documentaire seulement

- mémoire expérimentale ;
- audit de la connaissance ;
- boucle de révision ;
- contradiction/upward challenge ;
- plusieurs registres et protocoles de gouvernance.

## 7. Expositions architecturales importantes

1. **Fragmentation par branches :** plusieurs briques existent, mais aucune preuve ne montre leur assemblage dans la branche de référence.
2. **Trace sans producteurs aval :** `DecisionTrace` peut représenter une chaîne complète, mais cela ne démontre pas que les événements existent réellement.
3. **Recherche sans décision :** V4.3 fournit une preuve de recherche/compatibilité, pas une décision opérationnelle.
4. **Gouvernance documentaire sans boucle exécutable :** les règles de mémoire/audit/révision existent conceptuellement, pas comme parcours système.
5. **Identité de contexte non intégrée :** un contrat existe sur branche dédiée, mais son statut ne justifie pas encore son adoption.

## 8. Verdict de la cartographie

**ÉTAPE 3 — CARTOGRAPHIE : PASS FACTUELLE.**

La cartographie est suffisamment établie pour répondre à la question essentielle : **le système réel actuel ne constitue pas encore la chaîne minimale complète ; il possède surtout une frontière DATA robuste, une base de recherche/documentation et plusieurs briques expérimentales isolées.**

Aucune nouvelle architecture n'est justifiée par cette cartographie.

Le prochain travail doit donc porter sur le **plus petit point de rupture de la chaîne**, et non sur la construction simultanée de tous les blocs manquants.
