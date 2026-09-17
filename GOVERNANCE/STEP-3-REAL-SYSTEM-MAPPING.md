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

---

# ADDENDUM GOUVERNÉ — 17 SEPTEMBRE 2026 — P1.2 ACTION → RESULT EVIDENCE BOUNDARY

**Contract ID:** `P1_2_ACTION_RESULT_EVIDENCE_BOUNDARY_V1`  
**Branche de formalisation:** `integration/system-v1`  
**Base observée avant écriture:** `9065de2aca900cfcdc81e53d2e753492b173e635`  
**Statut de la formalisation:** `FORMALIZED`  
**Statut de la frontière exécutable:** `BLOCKED`  
**Règle:** cet addendum formalise la frontière ; il ne crée ni ACTION réelle, ni RESULT réel, ni broker/exchange, ni ordre, ni backtest, ni activation live.

L'ancienne cartographie ci-dessus est conservée comme preuve historique de l'état observé à l'ÉTAPE 3. Le présent addendum décrit le prochain contrat gouverné sur la branche d'intégration actuelle ; il ne réécrit pas rétroactivement cette cartographie historique.

## 9. Question minimale de P1.2

> **Peut-on prouver qu'un comportement identifiable a effectivement été engagé à la suite d'une Decision donnée, puis qu'une observation identifiable appartient à cette Action exacte, sans laisser une déclaration, un identifiant ou une Trace inventer l'existence de l'un ou l'autre ?**

Le noyau logique est :

`qualified Decision → Action effectivement engagée → Result effectivement observé`

puis seulement :

`Action + Result → future Trace reconstructible`.

P1.2 ne qualifie pas encore la création d'une Action opérationnelle depuis P1.1. Le chemin positif `AUTHORIZED` de P1.1 reste séparément `BLOCKED`.

## 10. Sémantique minimale

### 10.1 ACTION

`ACTION` signifie **le comportement effectivement engagé à la suite d'une Decision**.

Il peut représenter notamment :

- agir ;
- ne pas agir de manière contrôlée ;
- suspendre ;
- arrêter ;
- réduire une exposition ;
- demander une information ou une expérience supplémentaire.

`ACTION` n'est donc pas synonyme d'ordre broker.

Une intention, une commande préparée, un texte tel que `BUY`, un `action_id`, un champ dans `DecisionTrace` ou une déclaration d'appelant ne prouvent pas qu'une Action a effectivement existé.

### 10.2 RESULT

`RESULT` signifie **une observation effectivement produite ou recueillie après/à propos de l'Action exacte**.

Un `result_id`, une valeur `SUCCESS`, un PnL déclaré, une Trace ou une reconstruction de champs ne prouvent pas qu'un Result a été réellement observé.

`RESULT` n'établit pas automatiquement :

- que l'Action a causé le Result ;
- que la Decision était correcte ;
- que la connaissance utilisée est validée ;
- qu'un changement de comportement est autorisé.

Ces interprétations appartiennent à la future chaîne TRACE → MEMORY → AUDIT → REVISION.

## 11. Noyau informationnel minimal

P1.2 ne prescrit pas encore un module, une classe, un stockage ni une API. Un même mécanisme pourra couvrir ACTION et RESULT si cela reste le plus petit raccord correct.

Le noyau informationnel minimal candidat est :

```text
ActionEvidence
- action_id
- decision_id
- behavior

ResultObservation
- result_id
- action_id
- outcome
```

Ces champs ne constituent **pas** à eux seuls une preuve d'authenticité ou d'existence. Leur admissibilité doit être liée à un producteur/mécanisme qualifié ; l'égalité de valeurs n'est pas suffisante.

Aucune cardinalité universelle `1 Action = 1 Result` n'est imposée ici. Une Action peut avoir zéro, une ou plusieurs observations selon un futur contrat de domaine. P1.2 exige seulement que chaque Result admis soit lié sans ambiguïté à l'Action exacte qu'il prétend observer.

## 12. Invariants obligatoires

Une future qualification positive de la frontière ACTION → RESULT devra satisfaire simultanément :

1. `action_id` seul ne prouve jamais l'existence d'une Action.
2. Le système reçoit une preuve/instance complète d'Action, pas seulement ses champs sérialisés.
3. Une Action admissible est liée à la Decision exacte dont elle découle.
4. Une reconstruction manuelle, `copy`, `deepcopy`, `replace` ou objet de mêmes valeurs ne reproduit pas automatiquement l'admissibilité d'une Action.
5. Une mutation post-production d'identité, de `decision_id` ou de comportement invalide l'admissibilité de l'Action.
6. Une Action déclarée mais non effectivement engagée ne peut être traitée comme Action observée/exécutée.
7. Le no-action contrôlé est une Action valide s'il est explicitement produit comme comportement effectivement engagé ; il ne doit pas être confondu avec une Action manquante.
8. `result_id` seul ne prouve jamais l'existence d'un Result.
9. Un Result admissible est lié à l'Action exacte qu'il observe.
10. Une reconstruction manuelle ou une copie de Result ne reproduit pas automatiquement son admissibilité.
11. Une mutation post-observation de `result_id`, `action_id` ou outcome invalide l'admissibilité du Result.
12. Une valeur de résultat déclarée sans mécanisme d'observation qualifié doit échouer fermée.
13. Une contradiction temporelle explicitement représentée — par exemple une observation affirmée antérieure à l'Action — doit échouer fermée ; P1.2 n'impose toutefois pas encore un champ timestamp universel.
14. `DecisionTrace` ou toute future Trace ne peut jamais créer, attester ou réparer une Action ou un Result absent.
15. La présence de `action_id` et `result_id` dans une Trace ne constitue pas une preuve d'existence.
16. Un Result favorable ne peut jamais être promu automatiquement en preuve causale, validation de connaissance ou autorisation opérationnelle.
17. L'absence de Result ne peut pas être interprétée comme succès, échec ou résultat neutre sans règle explicite.
18. Une Action ou un Result rejeté doit rester sans side effect downstream dans le harness de qualification.
19. Aucun mécanisme P1.2 ne peut inférer une permission d'acquisition, backtest, broker, ordre ou live.
20. Toute incertitude sur l'existence, l'origine ou la liaison Action ↔ Result doit échouer fermée.

## 13. Catalogue adversarial minimal

### A — Existence et origine de l'Action

- `A0` Action cohérente issue du futur producteur qualifié et liée à la bonne Decision ;
- `A1` Action absente ;
- `A2` mauvais type ;
- `A3` `action_id` seul ;
- `A4` dictionnaire/champs sérialisés au lieu de l'Action complète ;
- `A5` reconstruction exacte des champs d'une Action authentique ;
- `A6` Action authentique liée à une Decision étrangère ;
- `A7` copie / deepcopy / replace ;
- `A8` mutation post-production de l'identité, de la Decision liée ou du comportement ;
- `A9` action simplement déclarée/préparée sans preuve qu'elle a effectivement été engagée ;
- `A10` `DecisionTrace.action_id` utilisé comme preuve d'existence ;
- `A11` no-action contrôlé authentique confondu avec Action absente.

### B — Existence et origine du Result

- `B0` Result cohérent issu du futur mécanisme d'observation qualifié pour l'Action exacte ;
- `B1` Result absent ;
- `B2` mauvais type ;
- `B3` `result_id` seul ;
- `B4` dictionnaire/champs sérialisés au lieu du Result complet ;
- `B5` reconstruction exacte des champs d'un Result authentique ;
- `B6` copie / deepcopy / replace ;
- `B7` mutation post-observation de l'identité, de `action_id` ou de l'outcome ;
- `B8` valeur `SUCCESS`/`FAIL`/PnL/outcome déclarée sans preuve d'observation ;
- `B9` `DecisionTrace.result_id` utilisé comme preuve d'existence ;
- `B10` contradiction temporelle explicite entre Action et observation lorsqu'une temporalité est représentée.

### C — Liaison Action → Result

- `C0` Result de l'Action B présenté comme Result de l'Action A ;
- `C1` même Result authentique rebondi vers une autre Action ;
- `C2` même `result_id` réutilisé avec un outcome différent ;
- `C3` paire Action/Result provenant de chaînes de Decision différentes ;
- `C4` Result stale/rejoué hors de son futur domaine de validité ;
- `C5` Result produit/accepté alors que l'Action correspondante n'est pas admissible ;
- `C6` Action présente mais liaison au Result ambiguë ou manquante.

### D — Raccourcis sémantiques interdits

- `D0` `Decision → Result` sans Action prouvée ;
- `D1` Result favorable traité comme preuve automatique de causalité ;
- `D2` Result favorable traité comme validation automatique de la Decision ou de la connaissance ;
- `D3` absence de Result interprétée implicitement comme succès/échec ;
- `D4` Trace structurellement complète utilisée pour fabriquer rétrospectivement Action/Result ;
- `D5` no-action contrôlé rejeté uniquement parce qu'aucun ordre broker n'existe.

### E — Bypass opérationnel

- `E0` construction d'un ordre/broker request comme effet secondaire du candidat P1.2 ;
- `E1` appel réseau, acquisition `.bi5` ou broker/exchange ;
- `E2` position sizing, leverage, stop loss, take profit ou politique de risque quantitative introduite dans cette frontière ;
- `E3` real backtest ou live activation déduits de P1.2 ;
- `E4` Result accepté après rejet d'Action en continuant malgré l'échec ;
- `E5` Action/Result synthétiques de qualification interprétés comme permission opérationnelle.

## 14. Qualification positive autorisée à ce stade

Le futur candidat P1.2, lorsqu'il sera implémenté, doit rester **local, synthétique et sans side effect**.

Il pourra démontrer uniquement :

- qu'une ActionEvidence synthétique authentique peut être liée à une Decision synthétique/qualifiée sans exécuter de marché ;
- qu'un ResultObservation synthétique authentique peut être lié à cette Action exacte ;
- que reconstructions, substitutions, mutations et liaisons étrangères sont rejetées ;
- que Trace reste une projection aval et non un producteur ;
- qu'aucun ordre, broker, acquisition, backtest réel ou live n'est ouvert.

Un test P1.2 vert ne signifiera pas qu'une Action opérationnelle est autorisée. La production opérationnelle d'Action reste dépendante d'une future autorité positive P1.1 séparément qualifiée.

## 15. Hors périmètre explicite

P1.2 ne définit pas encore :

- ordre broker/exchange ;
- statut d'ordre, fill, partial fill ou rejet broker ;
- taille de position ;
- leverage ;
- stop loss / take profit ;
- exposition portefeuille ;
- PnL comme format universel de Result ;
- slippage/execution quality ;
- cardinalité universelle Action ↔ Result ;
- horloge/timestamp universel ;
- causal inference ;
- TRACE/MEMORY/AUDIT/REVISION ;
- persistance inter-process d'Action/Result ;
- acquisition de données ;
- backtest réel ;
- live.

Ces propriétés ne doivent être ajoutées que lorsqu'un test ou une frontière future les rend nécessaires.

## 16. État après formalisation

**FORMALISATION P1.2 : PASS.**

La frontière exécutable reste :

**ACTION → RESULT : BLOCKED.**

Raison : aucun producteur qualifié d'ActionEvidence ni mécanisme qualifié de ResultObservation n'existe actuellement sur `integration/system-v1`.

Aucun code ne doit être créé simplement pour reproduire le vieux harness synthétique. La prochaine étape doit d'abord déterminer le **plus petit candidat exécutable** capable de satisfaire A0–E5 en réutilisant l'existant et sans créer d'architecture opérationnelle.

## 17. Prochaine action gouvernée unique

**Déterminer le plus petit candidat P1.2 — en nombre de responsabilités, pas en nombre de fichiers — permettant seulement :**

1. de produire/attester une ActionEvidence synthétique liée à une Decision exacte ;
2. de produire/attester un ResultObservation synthétique lié à cette Action exacte ;
3. de valider la liaison ACTION → RESULT sans créer d'exécution réelle ;
4. de laisser `DecisionTrace` strictement aval et non producteur.

Puis seulement construire le breaker adversarial A0–E5 avant toute correction de candidat.
