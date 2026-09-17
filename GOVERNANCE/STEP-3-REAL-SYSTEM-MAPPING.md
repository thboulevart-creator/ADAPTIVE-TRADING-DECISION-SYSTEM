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

---

# ADDENDUM GOUVERNÉ — 17 SEPTEMBRE 2026 — P1.3 RESULT → TRACE EVIDENCE BOUNDARY

**Contract ID:** `P1_3_RESULT_TRACE_EVIDENCE_BOUNDARY_V1`  
**Branche de formalisation:** `integration/system-v1`  
**Base observée avant écriture:** `8a36198fce100fb41275c778a405a3100e209aab`  
**Statut de la formalisation:** `FORMALIZED`  
**Statut de la frontière exécutable:** `BLOCKED`  
**Règle:** cet addendum qualifie la reconstruction de TRACE ; il ne crée aucun événement amont et n'ouvre aucune permission opérationnelle.

## 18. État P1.2 qui précède P1.3

Le statut `BLOCKED` de l'addendum P1.2 ci-dessus est historique et supersédé pour le harness de qualification.

P1.2 qualification-only est désormais **PASS** sur le HEAD `8a36198fce100fb41275c778a405a3100e209aab` :

- `RESEARCH → DECISION` : 16 tests PASS ;
- P1.2 A0–E5 + second breaker exact-provenance : 60 tests PASS ;
- run `35245152286`, attempt 2, job `105283562009` : SUCCESS ;
- aucune Action opérationnelle, aucun broker, aucun ordre, aucun backtest réel et aucun live ne sont autorisés par ce PASS.

## 19. Question minimale de P1.3

> **DecisionTrace peut-elle reconstruire une histoire seulement à partir d'événements réellement qualifiés, sans qu'un ensemble cohérent de simples IDs ou de métadonnées déclarées puisse fabriquer rétrospectivement une fausse chaîne ?**

Le noyau logique visé est :

`qualified upstream evidence + exact Decision + exact ActionEvidence + exact ResultObservation → DecisionTrace`

TRACE reste strictement aval : elle décrit ce qui a déjà été produit/observé ; elle ne crée, n'atteste, ne répare ni Decision, ni Action, ni Result.

## 20. Constat de minimalité : les trois objets downstream ne suffisent pas au schéma actuel

Le triplet :

`Decision + QualificationActionEvidence + QualificationResultObservation`

est suffisant pour prouver la chaîne downstream qualifiée :

`Decision → Action → Result`.

Il est **insuffisant** pour remplir honnêtement l'actuel `DecisionTrace`, qui exige aussi :

- `provenance_id` ;
- `research_run_id` ;
- `code_version` ;
- `configuration_version` ;
- `dataset_id` ;
- `dataset_version` ;
- `context_id`.

`Decision` ne conserve publiquement que `decision_id`, `research_run_id`, `context_id` et `decision`. Les autres valeurs appartiennent à `ResearchRunEvidence`.

Par conséquent, P1.3 interdit explicitement de remplir ces champs avec :

- constantes ;
- placeholders ;
- valeurs déclarées par l'appelant ;
- reconstruction depuis des IDs seuls ;
- déduction non prouvée.

Le plus petit candidat truthful devra donc recevoir la preuve amont complète nécessaire à la Trace. À ce stade, l'entrée minimale est :

`ResearchRunEvidence + Decision + QualificationActionEvidence + QualificationResultObservation`.

P1.3 ne décide pas encore si une future évolution devra mémoriser la provenance amont dans l'attestation privée de `Decision`. Cette question ne doit être ouverte que si le breaker démontre qu'une simple liaison par identité/attestation des quatre objets reste contournable.

## 21. Invariants obligatoires P1.3

Une future qualification positive doit satisfaire simultanément :

1. `DecisionTrace` ne peut pas être qualifiée à partir de `decision_id`, `action_id` et `result_id` seuls.
2. La construction qualifiée exige la `Decision` complète et factory-attested.
3. La construction qualifiée exige l'`ActionEvidence` complète et encore admissible.
4. La construction qualifiée exige le `ResultObservation` complet et encore admissible.
5. La chaîne `Decision → Action → Result` doit être vérifiée avant toute création de Trace.
6. Les métadonnées RESEARCH/provenance nécessaires au schéma de Trace doivent venir d'un `ResearchRunEvidence` complet et factory-attested, jamais de valeurs caller-supplied libres.
7. `ResearchRunEvidence.research_run_id` et `context_id` doivent être cohérents avec la Decision fournie.
8. Les champs de la Trace doivent être copiés depuis les objets qualifiés correspondants ; aucun champ historique obligatoire ne peut être inventé.
9. Une reconstruction manuelle de `DecisionTrace` avec les mêmes champs ne reproduit pas automatiquement une future admissibilité de Trace qualifiée.
10. `copy`, `deepcopy`, `replace` ou mutation post-production d'une Trace qualifiée doivent être détectables/rejetables si l'admissibilité de Trace devient une propriété downstream.
11. Une Trace avec Result étranger, Action étrangère ou Decision étrangère doit échouer fermée, même si certains IDs coïncident.
12. Une Trace ne peut jamais servir de producteur rétrospectif pour rendre admissible un objet Decision/Action/Result non admissible.
13. `DecisionTrace.validate() == PASS` structurel ne vaut pas preuve P1.3 d'authenticité ou de provenance.
14. `reconstruction_chain()` ne doit pas être interprété comme preuve que les événements référencés ont réellement existé.
15. Une incohérence entre preuve amont et chaîne downstream doit échouer fermée.
16. L'absence d'une preuve amont nécessaire doit laisser TRACE incomplète/BLOCKED plutôt que créer une métadonnée de remplacement.
17. TRACE ne doit pas déduire causalité, qualité de Decision, validation de connaissance ou permission opérationnelle à partir du Result.
18. Aucun mécanisme P1.3 ne peut acquérir de données, lancer un backtest réel, appeler un broker, produire un ordre ou activer le live.
19. Toute incertitude sur l'origine ou la liaison d'un maillon obligatoire doit échouer fermée.

## 22. Catalogue adversarial minimal P1.3

### A — Faux récit par identifiants

- `A0` chaîne complète issue des objets qualifiés exacts ;
- `A1` seulement `decision_id/action_id/result_id` ;
- `A2` `DecisionTrace(...)` construite manuellement avec des IDs cohérents ;
- `A3` dictionnaire sérialisé reprenant tous les champs de Trace ;
- `A4` Trace structurellement `PASS` mais sans objets qualifiés amont ;
- `A5` `reconstruction_chain()` cohérente utilisée comme preuve d'existence.

### B — Substitutions d'objets

- `B0` Decision étrangère ;
- `B1` Action étrangère ;
- `B2` Result étranger ;
- `B3` paire Action/Result étrangère avec IDs superficiellement cohérents ;
- `B4` objets reconstruits/copied/deepcopied/replaced au lieu des originaux admissibles ;
- `B5` objet amont muté après qualification.

### C — Provenance RESEARCH et métadonnées de Trace

- `C0` `ResearchRunEvidence` absente ;
- `C1` mauvais type ;
- `C2` champs sérialisés ou IDs seuls au lieu de la preuve complète ;
- `C3` preuve non factory-attested ;
- `C4` `research_run_id` étranger ;
- `C5` `context_id` étranger ;
- `C6` provenance/code/configuration/dataset inventés ou override par l'appelant ;
- `C7` preuve amont authentique mais incompatible avec la Decision fournie.

### D — Direction de causalité de TRACE

- `D0` Trace utilisée pour mint/attester une Decision ;
- `D1` Trace utilisée pour mint/attester une Action ;
- `D2` Trace utilisée pour mint/attester un Result ;
- `D3` modification de Trace utilisée pour réécrire l'historique amont ;
- `D4` Result favorable transformé par Trace en validation causale/épistémique ;
- `D5` Trace incomplète réparée silencieusement par défaut/placeholder.

### E — Bypass opérationnel

- `E0` import ou appel broker/exchange ;
- `E1` ordre/exécution/sizing/risk policy ;
- `E2` acquisition `.bi5` ou réseau ;
- `E3` backtest réel ;
- `E4` live activation ;
- `E5` PASS de Trace interprété comme permission opérationnelle.

## 23. Qualification positive autorisée à ce stade

Le futur candidat P1.3 peut démontrer uniquement qu'une Trace de qualification :

- est construite à partir d'une preuve RESEARCH authentique et de la chaîne exacte Decision → Action → Result ;
- reproduit fidèlement les identités déjà qualifiées ;
- rejette substitutions, reconstructions et histoires constituées de simples IDs ;
- reste une projection downstream sans effet secondaire.

Il ne doit pas créer de mémoire expérimentale, d'audit automatique ni de boucle de révision ; ces fonctions restent en aval de TRACE.

## 24. État après formalisation P1.3

**FORMALISATION P1.3 : PASS.**

La frontière exécutable reste :

**RESULT → TRACE : BLOCKED.**

Raison : l'actuel `DecisionTrace` n'est qu'une dataclass publiquement constructible dont `validate()` vérifie la complétude structurelle des chaînes. Aucun producteur qualifié ne lie encore une Trace aux objets exacts qui ont réellement produit Decision, Action et Result.

## 25. Prochaine action gouvernée unique

**Déterminer le plus petit candidat exécutable P1.3 qui réutilise `DecisionTrace` au lieu de créer un second modèle de Trace, puis seulement construire le breaker A0–E5 avant toute correction.**

Le candidat devra rester local, synthétique, sans side effect et ne devra pas modifier P1.2 sauf si un breaker prouve qu'une dépendance de provenance exacte manque réellement.

---

# ADDENDUM GOUVERNÉ — 17 SEPTEMBRE 2026 — P1.4 TRACE → MEMORY EPISODE BOUNDARY

**Contract ID:** `P1_4_TRACE_MEMORY_EPISODE_BOUNDARY_V1`  
**Branche de formalisation:** `integration/system-v1`  
**Base observée avant écriture:** `a1f5b86c74e64ee128753afdcc66d150dd7c645c`  
**Statut de la formalisation:** `FORMALIZED`  
**Statut de la frontière exécutable:** `BLOCKED`  
**Règle:** cet addendum formalise uniquement la création d'un épisode observationnel de mémoire à partir d'objets déjà qualifiés. Il ne crée pas de stockage durable, de connaissance, d'interprétation expérimentale, d'audit, de révision ni d'autorisation opérationnelle.

L'état historique P1.3 ci-dessus est conservé. Au HEAD observé avant cette écriture, P1.3 qualification-only est désormais PASS : une `DecisionTrace` factory-attested reste un snapshot downstream autonome après collecte ou mutation des objets amont. Ce PASS ne signifie toutefois pas que la Trace contient le contenu complet de l'Action ou du Result : elle ne conserve que `action_id` et `result_id`, pas `behavior` ni `outcome`.

## 26. Question minimale de P1.4

> **Peut-on préserver un épisode observationnel réutilisable uniquement à partir d'une Trace P1.3 exacte et qualifiée, de l'ActionEvidence exacte encore admissible et du ResultObservation exact encore admissible, sans transformer l'observation en interprétation, l'expérience en connaissance ou la mémoire en autorisation ?**

Le noyau logique est :

`exact qualified DecisionTrace + exact admissible ActionEvidence + exact admissible ResultObservation → observational MemoryEpisode`

P1.4 ne qualifie pas encore une « expérience interprétée » au sens hypothèse → test → conclusion. Il qualifie seulement la conservation fidèle d'un épisode factuel relié à la chaîne déjà prouvée.

## 27. Quatre séparations obligatoires

P1.4 verrouille explicitement quatre frontières sémantiques :

### 27.1 `EVENT ≠ EXPERIENCE`

Une Action et un Result, même authentiques, ne constituent pas à eux seuls une expérience réutilisable. L'épisode doit les relier à la Trace exacte qui porte la provenance, le contexte, la Decision et les identités de reconstruction déjà qualifiées.

### 27.2 `OBSERVATION ≠ INTERPRETATION`

`behavior` et `outcome` décrivent ce qui a été engagé et observé. Ils ne prouvent pas :

- que l'Action a causé le Result ;
- que la Decision était correcte ;
- qu'une hypothèse a été testée ;
- qu'une explication est soutenue, réfutée ou ininterprétable ;
- qu'un résultat favorable a une signification générale.

P1.4 doit préserver l'observation sans lui ajouter de sens épistémique non prouvé.

### 27.3 `EXPERIENCE ≠ KNOWLEDGE`

Un MemoryEpisode P1.4 n'est pas une connaissance validée. La répétition, la similarité, le succès, l'échec ou l'existence de plusieurs épisodes ne constituent pas automatiquement une promotion vers KNOWLEDGE.

Toute promotion épistémique reste BLOCKED en aval et devra passer par des mécanismes futurs d'AUDIT / CONTESTATION / REVISION / nouvelle preuve.

### 27.4 `KNOWLEDGE ≠ OPERATIONAL AUTHORIZATION`

Même une future connaissance validée ne constituera pas à elle seule un droit d'agir. La frontière P1.1 reste l'autorité séparée sur DECISION → ACTION et son chemin positif `AUTHORIZED` demeure hors de P1.4.

Aucun MemoryEpisode ne peut être utilisé comme bearer token, permission ou contournement vers DECISION/ACTION.

## 28. Entrée minimale P1.4

L'entrée sémantique minimale est exactement :

1. une `DecisionTrace` P1.3 factory-attested et non mutée ;
2. une `QualificationActionEvidence` exacte encore admissible ;
3. un `QualificationResultObservation` exact encore admissible.

P1.4 n'accepte pas comme substituts :

- `decision_id`, `action_id`, `result_id` seuls ;
- dictionnaires/champs sérialisés ;
- objets reconstruits, copied, deepcopied ou replaced ;
- une Trace seulement structurellement `PASS` ;
- une Action ou un Result devenu inadmissible après mutation ;
- une paire Action/Result provenant d'une autre chaîne même si des valeurs coïncident.

La cohérence minimale doit inclure au moins :

- `trace.decision_id == action.decision_id` ;
- `trace.action_id == action.action_id` ;
- `trace.result_id == result.result_id` ;
- `result.action_id == action.action_id` ;
- admissibilité réelle de l'Action et du Result selon la frontière P1.2, pas seulement égalité de champs.

Si l'API publique existante ne permet pas encore de démontrer cette admissibilité sans réintroduire la Decision amont, la frontière exécutable reste BLOCKED : le futur candidat devra identifier le plus petit hook de vérification nécessaire, sans élargir silencieusement le contrat.

## 29. Conséquence de durée de vie des objets

P1.3 a volontairement qualifié la propriété suivante : une Trace déjà produite reste factory-attested même après collecte des objets amont.

P1.4 en déduit une limite différente :

> **une Trace survivante ne peut pas recréer `behavior` ou `outcome` si l'ActionEvidence ou le ResultObservation exacts ne sont plus disponibles/admissibles.**

Par conséquent :

- la Trace seule ne permet jamais de fabriquer rétrospectivement un MemoryEpisode complet ;
- P1.4 doit être créé pendant que l'Action et le Result exacts nécessaires sont encore vérifiables ;
- la perte de ces objets avant création de l'épisode doit laisser la frontière BLOCKED, jamais déclencher une reconstruction depuis les IDs ou des valeurs déclarées.

Cette règle ne remet pas en cause l'autonomie historique de la Trace P1.3 ; elle reconnaît simplement que la Trace n'a jamais prétendu conserver le contenu complet de l'Action/Result.

## 30. Noyau informationnel minimal de l'épisode

P1.4 ne fige pas encore une classe, un module, une base ni un format de stockage. Tout candidat devra toutefois préserver sans perte :

### 30.1 Projection de reconstruction déjà qualifiée

Au minimum les informations de la Trace :

- `decision_id` ;
- `provenance_id` ;
- `research_run_id` ;
- `code_version` ;
- `configuration_version` ;
- `dataset_id` ;
- `dataset_version` ;
- `context_id` ;
- `decision` ;
- `action_id` ;
- `result_id`.

Le candidat pourra conserver l'objet Trace exact ou copier fidèlement sa projection dans l'épisode ; ce choix d'implémentation ne doit pas changer la sémantique ni créer une nouvelle autorité.

### 30.2 Contenu observationnel absent de la Trace

- `behavior` provenant de l'ActionEvidence exacte ;
- `outcome` provenant du ResultObservation exact.

Aucune valeur observationnelle ne peut être réécrite à partir d'une interprétation.

### 30.3 Identité d'épisode

Un futur candidat devra rendre l'épisode identifiable sans permettre qu'un nouvel identifiant suffise à prouver son authenticité. Le mécanisme exact d'identité/attestation n'est pas figé ici ; il doit être dérivé des entrées qualifiées et cassé adversarialement avant PASS.

## 31. Ce que P1.4 interdit de stocker comme vérité qualifiée

Le premier MemoryEpisode P1.4 n'a pas d'autorité pour qualifier :

- `hypothesis` ;
- `prediction` ;
- `falsification_rule` ;
- `ResearchFinding.status` ;
- `SUPPORTED`, `REFUTED` ou `NOT_INTERPRETABLE` ;
- candidate explanation ;
- tested explanation ;
- causal relation ;
- decision correctness ;
- confidence score ;
- knowledge status ;
- operational rule ;
- authorization state.

Ces informations peuvent exister ailleurs dans le dépôt mais elles ne sont pas des entrées P1.4 qualifiées à ce stade.

L'absence de `ResearchFindings` dans P1.4 ne doit surtout pas être traduite en `NOT_INTERPRETABLE` : `NOT_INTERPRETABLE` est un statut précis d'un `ResearchFinding`, pas un synonyme d'absence d'interprétation.

## 32. Invariants obligatoires P1.4

Une future qualification positive doit satisfaire simultanément :

1. Une Trace seulement structurale ou reconstruite ne peut pas produire un MemoryEpisode qualifié.
2. Une Trace qualifiée ne suffit jamais seule à produire l'épisode, car elle ne porte ni `behavior` ni `outcome`.
3. L'ActionEvidence exacte est obligatoire et doit rester admissible au moment de la création de l'épisode.
4. Le ResultObservation exact est obligatoire et doit rester admissible au moment de la création de l'épisode.
5. Les identités Trace ↔ Action ↔ Result doivent être cohérentes et la cohérence de valeurs ne remplace jamais l'admissibilité des objets.
6. Le contenu `behavior` doit provenir exclusivement de l'Action exacte.
7. Le contenu `outcome` doit provenir exclusivement du Result exact.
8. Un MemoryEpisode ne peut pas modifier, réparer, mint ou ré-attester la Trace, l'Action ou le Result.
9. Un MemoryEpisode ne peut pas inférer que l'Action a causé le Result.
10. Un MemoryEpisode ne peut pas inférer que la Decision était correcte ou incorrecte à partir du seul Result.
11. Un MemoryEpisode ne peut pas produire ou promouvoir une hypothèse, un Finding, un statut épistémique ou une connaissance validée.
12. `SUPPORTED`, `REFUTED` et `NOT_INTERPRETABLE` ne peuvent pas être ajoutés comme statut de l'épisode P1.4 sans future frontière qualifiée distincte.
13. Un MemoryEpisode ne peut pas devenir une règle de décision, une permission ou une autorisation d'Action.
14. Une reconstruction manuelle, sérialisation, copie, deepcopy, replace ou objet same-valued ne doit pas reproduire automatiquement l'admissibilité d'un épisode qualifié.
15. Un hash, checksum, `episode_id` ou JSON cohérent ne constitue jamais à lui seul une preuve que l'épisode s'est produit.
16. P1.4 ne peut pas prétendre que la mémoire est exhaustive, non biaisée ou exempte de survivorship bias à partir de la validité d'un épisode individuel.
17. P1.4 ne peut pas déclarer qu'une hypothèse était disponible avant une Decision : aucun invariant temporel de cette nature n'est actuellement prouvé par les objets d'entrée.
18. Toute contradiction temporelle explicitement représentée doit échouer fermée, mais P1.4 n'introduit pas encore d'horloge universelle ni de `known_from`.
19. Aucun mécanisme P1.4 ne peut acquérir des données, lancer un backtest réel, appeler un broker, créer un ordre, faire du sizing/risk ou activer le live.
20. Toute incertitude sur l'origine, l'admissibilité ou la liaison des trois entrées obligatoires doit échouer fermée.

## 33. Catalogue adversarial minimal P1.4

### A — Substitution / faux TRACE

- `A0` exact `DecisionTrace` P1.3 factory-attested ;
- `A1` Trace manuelle same-valued ;
- `A2` Trace structurale `validate() == PASS` mais non attestée ;
- `A3` dictionnaire/JSON de Trace ;
- `A4` copy / deepcopy / replace de Trace ;
- `A5` Trace mutée post-production.

### B — Substitution Action / Result

- `B0` exact Action + exact Result encore admissibles ;
- `B1` Action reconstruite avec mêmes champs ;
- `B2` Result reconstruit avec mêmes champs ;
- `B3` copy / deepcopy / replace ;
- `B4` Action ou Result muté après production ;
- `B5` Action étrangère ;
- `B6` Result étranger ;
- `B7` paire authentique Action/Result d'une autre chaîne ;
- `B8` perte/GC de l'Action ou du Result suivie d'une tentative de reconstruction depuis la Trace.

### C — Cohérence de la chaîne

- `C0` `trace.action_id` différent de `action.action_id` ;
- `C1` `trace.result_id` différent de `result.result_id` ;
- `C2` `trace.decision_id` différent de `action.decision_id` ;
- `C3` `result.action_id` différent de `action.action_id` ;
- `C4` IDs cohérents mais objets non admissibles ;
- `C5` contenu `behavior` ou `outcome` override par l'appelant.

### D — Contamination observation → interprétation

- `D0` `Action followed by Result → Action caused Result` ;
- `D1` Result favorable → Decision correcte ;
- `D2` Result défavorable → Decision incorrecte ;
- `D3` ajout caller-supplied d'une hypothesis/explanation au MemoryEpisode ;
- `D4` ajout d'un score de confiance comme vérité qualifiée ;
- `D5` réécriture du `behavior` ou `outcome` avec une classification/interprétation aval.

### E — Promotion épistémique interdite

- `E0` Result favorable → `SUPPORTED` ;
- `E1` épisode → connaissance validée ;
- `E2` répétition d'épisodes → vérité/règle sans AUDIT ;
- `E3` absence de Findings → `NOT_INTERPRETABLE` ;
- `E4` MemoryEpisode utilisé comme evidence de préexistence d'une hypothèse ;
- `E5` MemoryEpisode utilisé pour créer/réparer un `ResearchFindings`.

### F — Autorité inverse / bypass opérationnel

- `F0` MemoryEpisode mint/atteste/répare Trace ;
- `F1` MemoryEpisode mint/atteste/répare Action ou Result ;
- `F2` MemoryEpisode → Decision sans frontière gouvernée ;
- `F3` MemoryEpisode → Action / `AUTHORIZED` ;
- `F4` broker/order/sizing/risk/backtest réel/live activé depuis P1.4 ;
- `F5` PASS P1.4 interprété comme permission opérationnelle.

### G — Sérialisation, durabilité et complétude hors périmètre

- `G0` JSON/hash/`episode_id` utilisé comme autorité après désérialisation ;
- `G1` épisode process-local sérialisé puis présenté comme ré-attesté sans mécanisme qualifié ;
- `G2` même épisode dupliqué et compté comme preuves indépendantes ;
- `G3` mémoire ne conservant que les succès mais prétendant être exhaustive/non biaisée ;
- `G4` interprétation ultérieure réécrivant silencieusement l'observation d'origine.

G0–G4 doivent être reconnus par le contrat, mais P1.4 ne prétend pas fermer toute la politique de persistance, de déduplication, de capture exhaustive ou de révision. Leur présence empêche seulement un faux PASS plus large que la frontière réellement qualifiée.

## 34. Surfaces explicitement BLOCKED après P1.4

### 34.1 Attachement de `ResearchFindings`

BLOCKED.

`ResearchFindings` porte hypothèses, mesures et statuts utiles, mais P1.4 ne possède pas encore de preuve qualifiée que :

- l'objet Findings exact est l'autorité aval légitime à attacher à cet épisode ;
- l'hypothèse ou l'interprétation existait avant la Decision ou avant l'observation concernée ;
- le statut peut être attaché sans réécriture post-hoc.

Ajouter seulement une égalité de `research_run_id/context_id` ou un hash ne suffit pas. Ajouter seulement une attestation d'objet exact ne résoudrait pas non plus, à elle seule, la question temporelle de préexistence de l'hypothèse.

### 34.2 Promotion `EXPERIENCE → KNOWLEDGE`

BLOCKED.

P1.4 ne définit ni confiance, ni réplication, ni agrégation, ni causalité, ni critères de validation/promotion. Ces questions appartiennent à la future boucle MEMORY → AUDIT → REVISION → nouvelle preuve.

### 34.3 Persistance durable / inter-process MEMORY

BLOCKED.

P1.4 peut être qualifié d'abord localement comme frontière sémantique, à l'image des étapes précédentes. Aucun JSON, checksum ou fichier persisté ne doit être considéré comme autorité durable simplement parce qu'il contient un épisode P1.4.

Le précédent P0.5 reste pertinent comme principe négatif — **sérialisation/hash ≠ autorité** — mais son replay déterministe ne peut pas être transposé automatiquement à un événement historique non rejouable. La stratégie de persistance/revalidation MEMORY devra être formalisée séparément.

### 34.4 Temporalité de connaissance / look-ahead

BLOCKED au-delà de la règle négative minimale.

P1.4 interdit de prétendre qu'une connaissance ou hypothèse était disponible avant une Decision sans preuve temporelle qualifiée. Il n'adopte pas silencieusement le contrat `TEMPORAL / POINT-IN-TIME` non normatif et n'introduit pas encore `known_from`, `usable_from` ou un timestamp universel.

### 34.5 Exhaustivité / survivorship bias / indépendance statistique

BLOCKED.

La qualification d'un épisode individuel ne prouve pas que tous les épisodes pertinents ont été capturés, ni que la sélection est non biaisée, ni que plusieurs épisodes sont indépendants. Ces propriétés exigent une future politique de capture/registre et/ou AUDIT.

## 35. Qualification positive autorisée à ce stade

Un futur PASS P1.4 pourra signifier uniquement :

- une Trace P1.3 exacte et qualifiée a été associée aux Action/Result exacts encore admissibles qui correspondent à ses identités ;
- le contenu observationnel `behavior` et `outcome` a été préservé sans réinterprétation ;
- un épisode identifiable peut être produit localement sans permettre aux IDs, copies ou sérialisations de fabriquer une fausse expérience ;
- l'épisode reste strictement non causal, non épistémique et non autorisant.

Il ne signifiera pas :

- connaissance validée ;
- hypothèse préexistante prouvée ;
- ResearchFindings authentiquement attachés ;
- confiance ;
- mémoire exhaustive ;
- persistance durable ;
- permission de Decision/Action ;
- capacité opérationnelle.

## 36. État après formalisation P1.4

**FORMALISATION P1.4 : PASS.**

La frontière exécutable reste :

**TRACE → MEMORY EPISODE : BLOCKED.**

Raison : aucun producteur/attesteur de MemoryEpisode n'existe encore et la surface publique P1.2 doit être confrontée à l'exigence exacte `Trace + Action + Result` pour vérifier si l'admissibilité Action/Result peut être prouvée sans réintroduire inutilement la Decision.

Aucun nouveau composant MEMORY, stockage, ResearchFindings attestation, timestamp, AUDIT ou REVISION n'est justifié par la seule formalisation.

## 37. Prochaine action gouvernée unique

**Déterminer, à partir des APIs réelles P1.2/P1.3, le plus petit candidat exécutable P1.4 capable de produire/attester localement un épisode observationnel exact depuis `DecisionTrace + QualificationActionEvidence + QualificationResultObservation`, puis construire le breaker A0–G4 avant toute correction.**

Si les APIs actuelles ne permettent pas de vérifier l'admissibilité des exacts Action/Result sans Decision, choisir le plus petit raccord de vérification nécessaire ; ne pas élargir le modèle de mémoire et ne pas introduire ResearchFindings, temporalité ou persistance durable dans ce raccord.

---

# ADDENDUM GOUVERNÉ — 17 SEPTEMBRE 2026 — P1.5 DURABLE MEMORY / INTER-PROCESS WITNESSED RE-ATTESTATION BOUNDARY

**Contract ID:** `P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1`  
**Branche de formalisation:** `integration/system-v1`  
**Base observée avant écriture:** `12936ce44a1ba5dd3ac154fc62c62bf39a9997b5`  
**Statut de la formalisation:** `FORMALIZED`  
**Statut de la frontière exécutable:** `BLOCKED`  
**Règle:** cet addendum formalise uniquement la confiance durable nécessaire pour faire survivre un `ObservationalMemoryEpisode` qualifié au processus qui l'a produit. Il ne choisit ni technologie de signature, ni service de stockage, ni trust root concret, ni format cryptographique, et ne crée aucune connaissance, AUDIT, REVISION ou autorisation opérationnelle.

## 38. État qualifié qui précède P1.5

Le statut `BLOCKED` de l'addendum P1.4 ci-dessus est historique et supersédé pour le harness de qualification.

P1.4 qualification-only est désormais **PASS** au HEAD `12936ce44a1ba5dd3ac154fc62c62bf39a9997b5` :

- l'épisode est produit uniquement depuis la Trace P1.3 exacte et les Action/Result P1.2 exacts historiquement liés à cette Trace ;
- l'attestation locale repose sur identité d'objet, weakref et fingerprint ;
- un `episode_id` déterministe identifie le contenu observationnel mais ne constitue pas, seul, une autorité ;
- JSON, reconstruction same-valued, copie, deepcopy, mutation et paire same-ID issue d'un autre lifecycle restent non autorisants ;
- le re-break persisted-HEAD P1.4 est PASS sur ce même SHA.

Cette qualification est volontairement **process-local** : lorsque le processus producteur disparaît, son registre d'attestation disparaît également. Les octets de l'épisode peuvent être copiés ou persistés, mais leur autorité P1.4 ne survit pas automatiquement.

## 39. Question minimale de P1.5

> **Peut-on faire survivre un épisode P1.4 à la disparition de son processus producteur en prouvant dans un processus ultérieur que des octets exacts ont été capturés pendant que l'épisode possédait encore son attestation P1.4, sans transformer le fichier persisté, son hash ou son propre identifiant en autorité, et sans prétendre rejouer l'événement historique ?**

Le noyau logique visé est :

`exact locally-attested ObservationalMemoryEpisode → trusted capture/witness → canonical durable record + authority-bound receipt → fresh process + independently supplied trust expectation → verification → fresh local historical-memory re-attestation`

Le terme **re-attestation** ne signifie pas résurrection de l'objet Python initial. Il signifie création d'une nouvelle attestation locale portant sur un record historique dont la capture a été qualifiée.

## 40. Séparations obligatoires de confiance durable

### 40.1 `DURABLE RECORD ≠ AUTHORITY`

Un record persistant est une représentation canonique de l'épisode. Sa présence sur disque, dans Git, dans une base, dans un objet storage ou dans tout autre support ne prouve pas à elle seule qu'il a été produit depuis un épisode P1.4 authentique.

### 40.2 `CONTENT INTEGRITY ≠ PROVENANCE / AUTHENTICITY`

Un hash, checksum, `episode_id`, nom content-addressed ou comparaison byte-for-byte peut établir l'identité/intégrité d'un contenu. Il ne prouve pas qui l'a capturé ni qu'une attestation P1.4 était valide au moment de cette capture.

### 40.3 `CAPTURE AUTHORITY ≠ CAPTURED ARTIFACT`

L'artefact ne peut jamais sélectionner lui-même l'autorité qui le rend fiable. Le processus consommateur doit recevoir la ou les autorités admissibles depuis une source de confiance extérieure au record et à son receipt.

Un champ `authority_id` auto-déclaré dans le JSON n'est donc pas une racine de confiance.

### 40.4 `RECEIPT ≠ HISTORICAL EVENT`

Un receipt qualifié atteste au maximum qu'une autorité de capture admissible a accepté des octets exacts alors que le producteur démontrait l'admissibilité P1.4 exigée. Il ne transforme pas cette attestation de capture en preuve causale, vérité du monde, connaissance validée ou preuve d'indépendance expérimentale.

### 40.5 `CONTENT IDENTITY ≠ OCCURRENCE / REGISTRATION IDENTITY`

L'actuel `episode_id` P1.4 est dérivé du contenu de l'épisode. Deux épisodes same-valued peuvent donc partager cette identité de contenu.

P1.5 doit distinguer au minimum :

- l'identité du contenu observationnel ;
- l'identité d'une opération durable de capture/registration.

Une future `registration_id`/identité de receipt identifie une capture durable ; elle ne prouve pas automatiquement l'existence de deux événements historiques ou de deux expériences statistiquement indépendantes.

P1.5 ne prétend pas encore disposer d'un identifiant global qualifié de l'**occurrence historique** elle-même. Si une telle identité devient nécessaire, elle devra être dérivée d'une future source d'événement qualifiée, pas inventée par MEMORY.

### 40.6 `REPLAY ≠ HISTORICAL VERIFICATION`

Rejouer RESEARCH peut reproduire un calcul déterministe. Rejouer une Action ou recréer un Result produit un **nouvel événement**, pas une vérification de l'ancien.

Par conséquent, aucune re-exécution de `Decision → Action → Result`, même avec les mêmes champs, IDs ou résultats, ne peut servir de preuve P1.5 que l'événement P1.4 historique s'est produit.

### 40.7 `FRESH-PROCESS RE-ATTESTATION ≠ ORIGINAL OBJECT RESURRECTION`

Le processus consommateur peut, après vérification qualifiée de la chaîne durable, mint une nouvelle autorité process-local sur le record historique accepté. Cette nouvelle attestation n'est ni l'objet P1.4 original, ni une ré-attestation par égalité de valeurs.

## 41. Composants sémantiques minimaux du contrat

P1.5 ne fige pas encore classes, modules ni stockage. Il distingue toutefois six responsabilités qui ne peuvent pas être confondues.

### 41.1 Source qualifiée : `ObservationalMemoryEpisode`

La capture durable ne peut commencer que depuis l'objet P1.4 exact, encore factory-attested dans son processus producteur. Une dataclass reconstruite, un dictionnaire, un JSON ou un épisode same-valued ne peut pas initier une capture qualifiée.

### 41.2 Durable record

Le durable record préserve canoniquement :

- le contrat/schema qui décrit le record ;
- la projection complète de l'épisode P1.4 ;
- l'identité de contenu correspondante ;
- toute information strictement nécessaire à une future vérification de schema et d'intégrité.

Il ne porte aucune autorité autonome. Sa localisation physique n'est pas une preuve d'origine.

### 41.3 Capture authority

La capture authority est l'acteur ou mécanisme auquel la gouvernance accorde le droit de témoigner qu'un épisode actuellement P1.4-attesté a été capturé sous forme de record exact.

P1.5 ne choisit pas sa technologie. Il exige seulement que son identité/admissibilité puisse être fournie et vérifiée indépendamment de l'artefact capturé.

### 41.4 Receipt

Le receipt est l'attestation durable émise par la capture authority. Il doit être lié sans ambiguïté au contenu exact du durable record et à l'identité de registration/capture qu'il prétend représenter.

Le mécanisme futur de vérification peut varier, mais il ne doit jamais se réduire à « le record contient un hash de lui-même ».

### 41.5 Fresh-process trust expectation

Le consommateur doit recevoir séparément ce qu'il est autorisé à croire : identité/admissibilité de capture authority, version de contrat attendue et autres paramètres de trust strictement nécessaires au mécanisme retenu.

Ni le durable record ni le receipt ne peuvent s'auto-déclarer comme trust root accepté.

### 41.6 Fresh local historical-memory attestation

Après vérification réussie, un nouveau processus peut mint une attestation locale qui signifie uniquement :

> « ce contenu historique exact possède une chaîne de capture durable vérifiée selon P1.5 ».

Cette attestation ne recrée pas les anciennes weakrefs Action/Result et ne prétend pas que les objets Python amont existent encore.

## 42. Confrontation explicite avec P0.5

P0.5 constitue un précédent **partiellement réutilisable**.

### 42.1 Principes P0.5 réutilisables

P1.5 reprend les principes suivants :

- un artefact sérialisé n'est jamais autorité par lui-même ;
- un hash/content-address établit l'intégrité, pas l'identité de l'autorité ;
- les attentes de trust doivent être fournies séparément de l'artefact ;
- schema inconnu, champ manquant, substitution ou incohérence doivent échouer fermés ;
- la validation dans un nouveau processus doit aboutir à une **nouvelle attestation locale**, pas à une confiance brute dans les champs désérialisés ;
- aucun bypass de type `trust_record=True`, `accept_digest_only`, `skip_verification` ou équivalent n'est admissible.

### 42.2 Mécanisme P0.5 non transposable

P0.5 peut reconstruire l'autorité RESEARCH par :

`source bytes → deterministic replay → exact claim comparison → fresh ResearchRunEvidence`.

P1.5 ne peut pas utiliser :

`stored episode → replay Action/Result → same values → historical authority`.

Ce chemin est invalide parce qu'une nouvelle Action/Result, même authentique et same-valued, constitue une nouvelle occurrence. Le breaker P1.4 same-ID a précisément démontré que l'égalité d'identifiants/valeurs entre lifecycles ne remplace pas la provenance historique exacte.

P1.5 doit donc utiliser une **witness/capture re-attestation**, pas une **replay re-attestation**.

## 43. Invariants obligatoires P1.5

Une future qualification positive doit satisfaire simultanément :

1. La capture persistante ne peut être initiée que depuis un `ObservationalMemoryEpisode` exact encore P1.4-attesté.
2. Une reconstruction same-valued de l'épisode ne peut pas produire un receipt qualifié.
3. Le durable record doit représenter exactement l'épisode accepté ; le producteur ne peut pas modifier `behavior`, `outcome`, provenance ou identités pendant la capture.
4. Le durable record, son chemin, son nom, son hash, son `episode_id` ou son content-address ne constituent jamais une autorité durable suffisante.
5. Toute modification des octets du record doit invalider tout receipt qui prétendait attester les octets antérieurs.
6. Un receipt ne peut pas être rebondi vers un autre record, même same-valued partiellement ou doté d'identifiants compatibles.
7. L'identité/admissibilité de la capture authority doit venir d'une trust expectation extérieure au record et au receipt.
8. Le record ou receipt ne peut jamais sélectionner seul l'autorité que le consommateur doit croire.
9. En l'absence d'une capture authority qualifiée ou d'un mécanisme permettant de vérifier son receipt, le consommateur doit échouer fermé ; il ne doit pas se rabattre sur un checksum-only PASS.
10. Le processus frais ne peut pas re-attester depuis un JSON/record seul.
11. Le processus frais doit vérifier schema, intégrité de contenu, liaison receipt ↔ record, admissibilité de l'autorité attendue et cohérence des claims avant de mint une nouvelle attestation locale.
12. La re-attestation fraîche représente un record historique witnessed ; elle n'est pas l'objet original ressuscité.
13. Aucune re-exécution de l'Action/Result ne peut servir de preuve que l'ancienne occurrence s'est produite.
14. Une nouvelle paire Action/Result authentique possédant les mêmes IDs ou valeurs que l'ancienne reste une nouvelle paire et ne peut pas réparer la chaîne historique.
15. `episode_id` doit rester traité comme identité de contenu et non comme preuve d'une occurrence historique globalement unique.
16. Chaque capture durable acceptée doit posséder une identité de registration/receipt distincte du content identity ; le mécanisme exact de génération n'est pas figé par cet addendum.
17. Plusieurs registrations ou receipts portant sur le même contenu ne constituent pas automatiquement plusieurs preuves indépendantes ni plusieurs occurrences historiques.
18. Une identité de registration ne peut pas être promue en causalité, confiance, répétition indépendante ou connaissance.
19. Si un ordre ou timestamp de registration est représenté, il doit provenir de la capture authority selon un futur mécanisme qualifié ; une valeur temporelle fournie uniquement par le record n'est pas une preuve temporelle.
20. `registration_at` éventuel ne doit pas être silencieusement assimilé à `known_from`, `valid_from`, `decision_at` ou à l'heure réelle de l'Action/Result.
21. Le déplacement d'un record vers un autre chemin/storage ne crée jamais une nouvelle autorité ; inversement, la localisation physique ne doit pas remplacer la vérification de la chaîne de trust.
22. Perte, corruption, receipt absent, autorité inconnue ou contradiction de claims doivent échouer fermés ; aucune reconstruction depuis des valeurs similaires ne doit réparer silencieusement le record.
23. P1.5 ne peut pas ajouter `ResearchFindings`, causalité, confiance, statut épistémique, connaissance ou règle opérationnelle au record qualifié.
24. Un receipt P1.5 ne peut pas servir de bearer token vers DECISION, ACTION, `AUTHORIZED`, broker, backtest ou live.
25. Un mécanisme de persistance P1.5 ne peut pas modifier, réparer ou ré-attester rétroactivement Trace/Action/Result.

## 44. Catalogue adversarial minimal P1.5

### A — Capture depuis une source non qualifiée

- `A0` exact MemoryEpisode P1.4 attesté au moment de la capture ;
- `A1` épisode manuel same-valued ;
- `A2` copy / deepcopy / replace ;
- `A3` JSON/dictionnaire de l'épisode ;
- `A4` épisode muté dont l'attestation P1.4 est devenue invalide ;
- `A5` `episode_id` seul utilisé pour demander une capture qualifiée.

### B — Durable record auto-autorisant

- `B0` record canonique intègre mais sans receipt ;
- `B1` contenu modifié puis hash/nom recomputé ;
- `B2` record contenant son propre `authority_id` et demandant qu'il soit cru ;
- `B3` chemin Git/storage considéré comme provenance suffisante ;
- `B4` schema inconnu, champ manquant, champ inconnu ou clé dupliquée ;
- `B5` content identity/filename incohérents.

### C — Receipt / capture authority

- `C0` receipt valide lié au record exact sous une authority attendue extérieurement ;
- `C1` receipt d'un autre record rebondi vers le record courant ;
- `C2` record modifié mais ancien receipt conservé ;
- `C3` receipt forgé ou émis par une authority non attendue ;
- `C4` record/receipt imposant lui-même le trust root au consommateur ;
- `C5` absence d'autorité qualifiée remplacée par `accept_digest_only`/`trust_me` ;
- `C6` copie d'un receipt utilisée pour prétendre créer une nouvelle occurrence indépendante.

### D — Faux replay historique

- `D0` replay/reconstruction Action→Result utilisé pour prétendre vérifier l'événement original ;
- `D1` nouveau lifecycle P1.2 produisant les mêmes IDs/valeurs présenté comme l'ancien événement ;
- `D2` nouvel épisode P1.4 same-valued présenté comme résurrection du précédent ;
- `D3` résultat de RESEARCH rejoué utilisé pour inventer les anciennes identités Action/Result qui ne sont plus vérifiables.

### E — Occurrence / registration / duplication

- `E0` même `episode_id` enregistré deux fois et présenté comme deux expériences indépendantes ;
- `E1` deux `registration_id` du même contenu présentés comme deux occurrences historiques prouvées ;
- `E2` duplication physique du même record présentée comme nouvelle evidence ;
- `E3` collision ou incohérence d'identité de registration traitée comme simple warning plutôt que fail closed ;
- `E4` registration identity utilisée comme preuve de causalité, confiance ou répétition.

### F — Temporalité et look-ahead

- `F0` timestamp de registration librement fourni par le record et traité comme trusted ;
- `F1` `registration_at` interprété comme `known_from` ou disponibilité à une Decision antérieure ;
- `F2` receipt créé plus tard mais utilisé pour prétendre que MEMORY était disponible avant sa capture ;
- `F3` absence de temps/ordre qualifié masquée par un timestamp caller-supplied.

### G — Autorité inverse / promotion interdite

- `G0` durable Memory record ou receipt utilisé pour mint/repair Trace, Action ou Result ;
- `G1` record ré-attesté utilisé directement comme `ResearchRunEvidence` ou `ResearchFindings` ;
- `G2` receipt interprété comme connaissance validée ;
- `G3` receipt interprété comme autorisation P1.1 ;
- `G4` persistance ouvrant broker/order/sizing/acquisition/backtest/live.

## 45. Décisions explicitement différées

P1.5 ne choisit pas encore :

- algorithme ou format de signature ;
- clé symétrique/asymétrique, certificat ou identité cryptographique ;
- custody, rotation, révocation ou récupération de clés ;
- service append-only, base de données, filesystem, object storage ou Git comme support ;
- trusted timestamp authority ou horloge matérielle ;
- quorum/multi-authority ;
- hardware attestation ;
- chiffrement/confidentialité du record ;
- politique complète de rétention, backup et disaster recovery ;
- ResearchFindings, connaissance, AUDIT ou REVISION.

Ces choix ne peuvent être introduits qu'après sélection et cassage du plus petit trust model capable de satisfaire le contrat. Une primitive technique ne peut pas être choisie uniquement parce qu'elle produit un hash ou une signature.

## 46. Qualification positive autorisée à P1.5

Un futur PASS P1.5 pourra signifier uniquement :

- un épisode P1.4 exact et encore attesté a été capturé sous forme d'un record canonique exact ;
- une capture authority qualifiée a produit un receipt lié sans ambiguïté à ce record et à une registration identifiable ;
- un nouveau processus, disposant indépendamment de l'autorité qu'il est autorisé à croire, a vérifié le record + receipt ;
- ce nouveau processus a mint une nouvelle attestation locale attestant la chaîne de custody du snapshot historique ;
- l'artefact persisté n'a jamais été utilisé comme sa propre autorité.

Un PASS P1.5 ne signifiera pas :

- replay ou reproduction de l'événement historique ;
- vérité causale ;
- Decision correcte ;
- hypothèse testée ;
- `ResearchFindings` attachés ;
- connaissance validée ;
- plusieurs occurrences indépendantes ;
- mémoire exhaustive/non biaisée ;
- point-in-time knowledge admissibility complète ;
- autorisation de Decision/Action ;
- capacité opérationnelle.

## 47. État après formalisation P1.5

**FORMALISATION P1.5 : PASS.**

La frontière exécutable reste :

**LOCAL MEMORY EPISODE → DURABLE WITNESSED MEMORY → FRESH-PROCESS RE-ATTESTATION : BLOCKED.**

Raison : le dépôt ne possède actuellement aucun capture-authority trust root qualifié ni mécanisme qualifié permettant à un processus frais de vérifier un receipt sans faire confiance à l'artefact lui-même. P0.5 fournit le principe négatif et la discipline de fresh-process verification, mais son replay déterministe ne peut pas fermer cette frontière historique.

Aucun stockage, signer, secret, clé, certificat ou service durable ne doit être créé simplement pour obtenir un artefact persistant. Le prochain travail doit d'abord déterminer **quelle autorité de capture minimale est réellement admissible et comment son trust est fourni indépendamment au consommateur**.

## 48. Prochaine action gouvernée unique

**Déterminer, en lecture seule et par comparaison adversariale, le plus petit modèle de `capture authority + external trust expectation` capable de rendre un receipt P1.5 vérifiable dans un nouveau processus sans auto-autorisation de l'artefact ; éliminer les modèles qui ne ferment pas cette frontière, puis seulement figer le modèle retenu et construire le breaker A0–G4 avant toute implémentation.**
