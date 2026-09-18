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

- `B0` Result cohérent issue du futur mécanisme d'observation qualifié pour l'Action exacte ;
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

---

# SÉLECTION GOUVERNÉE — 17 SEPTEMBRE 2026 — P1.5 CAPTURE AUTHORITY / EXTERNAL TRUST MODEL

**Selection ID:** `P1_5_EXTERNAL_RECEIPT_PIN_TRUST_MODEL_V1`  
**Base observée avant sélection:** `3474e7dc3a6f422ae21b75dfccfbc4342d09b793`  
**Statut:** `SELECTED — TEST-FIRST, NOT IMPLEMENTED`  
**Portée:** qualification durable de MEMORY uniquement ; aucun effet sur KNOWLEDGE, AUDIT, REVISION ou autorisation opérationnelle.

## 49. Comparaison adversariale des modèles

### 49.1 Hash/content-address contenu uniquement dans l'artefact — REJETÉ

Un auteur capable de modifier le record peut recalculer tous ses hashes. Sans attente extérieure, le record reste auto-autorisant. Ce modèle ne ferme pas B0/B1/C4/C5.

### 49.2 `authority_id` auto-déclaré + hash — REJETÉ

Un label d'autorité présent uniquement dans le receipt ne prouve pas que cette autorité est admissible. Il déplace l'auto-autorisation dans un champ supplémentaire sans créer de trust root.

### 49.3 Git/GitHub comme autorité implicite — REJETÉ au HEAD observé

La branche `integration/system-v1` n'est pas protégée et les commits observés ne fournissent pas une attestation cryptographique qualifiée de capture MEMORY. Un commit SHA établit une identité de contenu Git ; il n'est pas, à lui seul, le témoin P1.5 d'un épisode localement attesté.

### 49.4 Secret symétrique / HMAC partagé entre capture et vérificateur — REJETÉ pour le modèle minimal

Un MAC peut authentifier des bytes, mais tout vérificateur possédant le secret possède aussi le pouvoir de fabriquer de nouveaux receipts. Cela fusionne inutilement `capture authority` et `consumer verifier` et agrandit le trust boundary. Cette propriété n'est pas nécessaire pour fermer P1.5.

### 49.5 Signature asymétrique avec clé publique épinglée — ADMISSIBLE MAIS DIFFÉRÉE

Ce modèle fermerait la frontière tout en séparant mint et verify. Il exige toutefois déjà choix d'algorithme, dépendance cryptographique, génération/custody/rotation/révocation de clé et qualification d'un signer. Aucun de ces coûts n'est nécessaire pour le premier trust model P1.5.

### 49.6 Service/registre append-only de confiance — ADMISSIBLE MAIS DIFFÉRÉ

Un service peut jouer le rôle d'autorité, mais ajoute identité de service, stockage d'autorité, disponibilité, recovery, transport authentifié et politique opérationnelle. Il est plus large que nécessaire pour la première qualification.

### 49.7 Pin externe exact par registration — RETENU

Le plus petit modèle qui ferme l'auto-autorisation sans nouveau secret, signer ou service consiste à faire sortir, au moment de la capture qualifiée, l'identité cryptographique exacte du receipt vers un trust channel extérieur au bundle persisté.

Le processus frais reçoit ensuite cette attente depuis l'extérieur et ne fait confiance au record/receipt que s'ils correspondent exactement à cette attente.

## 50. Modèle retenu : `EXTERNAL_RECEIPT_PIN_V1`

Le chemin minimal retenu est :

`exact P1.4-attested MemoryEpisode → trusted in-process capture → canonical record + canonical receipt → external receipt pin provisioning → process exit → fresh process + external expected pin → exact verification → fresh local historical-memory attestation`

La **capture authority** est le contexte gouverné qui :

1. voit l'objet P1.4 exact pendant que son attestation process-local est encore valide ;
2. produit record + receipt canoniques ;
3. transmet séparément au trust channel le pin exact de ce receipt.

Le **trust channel** n'est pas le record, le receipt, leur répertoire ni leur nom de fichier. Son mécanisme de persistance/provisionnement reste hors périmètre de cette sélection ; il doit seulement être indépendant du bundle que le consommateur est en train de vérifier.

## 51. External trust expectation minimale

Pour une registration donnée, le processus frais doit recevoir séparément au minimum :

- `expected_contract_id` ;
- `expected_authority_id` ;
- `expected_receipt_sha256`.

Le receipt doit lier canoniquement au minimum :

- le contrat/schema de receipt ;
- `authority_id` ;
- `registration_id` ;
- `episode_id` ;
- l'identité cryptographique exacte du durable record.

Le pin externe porte sur les **bytes canoniques complets du receipt**. Ainsi une modification du record, du `registration_id`, de l'`authority_id`, de l'`episode_id` ou de la liaison record↔receipt nécessite un nouveau receipt et donc un nouveau pin externe.

`expected_receipt_sha256` n'est pas un « checksum auto-autorisant » : il n'est admissible que parce qu'il est fourni au consommateur depuis un canal de trust extérieur au bundle vérifié. Si cette valeur est lue depuis le receipt ou un fichier compagnon non indépendamment trusted, la frontière doit échouer fermée.

## 52. Limites assumées du modèle retenu

Ce modèle est volontairement **par registration**. Il ne prétend pas être la solution la plus scalable : chaque receipt accepté nécessite une attente extérieure exacte.

Cette contrainte est un avantage pour la première qualification :

- aucun secret n'est distribué au vérificateur ;
- le vérificateur ne gagne aucun pouvoir de mint ;
- aucune PKI n'est créée ;
- aucun service de trust n'est présupposé ;
- le blast radius d'un pin compromis est borné à la registration concernée.

Si le coût de provisioning par registration devient réellement bloquant, ce sera une preuve exécutable justifiant une évolution vers un modèle de signature ou de registre d'autorité. Cette évolution ne doit pas être anticipée.

Le modèle ne qualifie pas la résistance à un compromis arbitraire du processus producteur P1.4 lui-même. Il conserve le trust boundary déjà assumé par les attestations process-locales P1.2–P1.4. Une future exposition à du code non fiable dans ce processus nécessitera une isolation séparément qualifiée.

## 53. Breaker à construire avant toute implémentation

Le breaker P1.5 doit être écrit **avant** tout `src/memory_interprocess.py` ou mécanisme équivalent. Il doit utiliser un transport local synthétique uniquement et casser au minimum A0–G4 :

### A — Source de capture
- `A0` exact MemoryEpisode P1.4 encore attesté : seul chemin positif admissible ;
- `A1` épisode manuel same-valued rejeté ;
- `A2` copy/deepcopy/replace rejetés ;
- `A3` dictionnaire/JSON rejeté ;
- `A4` épisode muté/inattesté rejeté.

### B — Record / receipt non autorisants
- `B0` record seul rejeté ;
- `B1` receipt seul rejeté ;
- `B2` record + receipt avec hashes internes cohérents mais sans external pin rejetés ;
- `B3` modification + recomputation de tous les hashes internes rejetée contre le pin externe ;
- `B4` chemin Git/storage/filename non traité comme trust root.

### C — External trust expectation
- `C0` exact `(contract, authority_id, receipt_sha256)` fourni hors bundle permet la vérification ;
- `C1` mauvais receipt pin rejeté ;
- `C2` mauvais authority attendu rejeté ;
- `C3` mauvais contract attendu rejeté ;
- `C4` receipt/record tentant de fournir lui-même les valeurs `expected_*` rejeté.

### D — Fresh-process re-attestation / anti-replay
- `D0` processus frais + pin externe exact → nouvelle attestation locale historique ;
- `D1` désérialisation brute du record reste non attestée ;
- `D2` replay Action/Result ne reconstitue pas l'autorité historique ;
- `D3` nouvel épisode same-valued ne récupère pas l'ancienne registration ;
- `D4` nouvelle attestation locale n'est pas l'objet P1.4 original ressuscité.

### E — Registration / duplication
- `E0` `registration_id ≠ episode_id` ;
- `E1` deux registrations du même contenu ne valent pas deux expériences indépendantes ;
- `E2` copie physique record/receipt ne crée pas de registration ;
- `E3` collision/incohérence de registration échoue fermée ;
- `E4` pin d'une registration ne peut autoriser une autre registration.

### F — Temporalité minimale
- `F0` aucun timestamp caller-supplied n'est nécessaire au PASS ;
- `F1` timestamp contenu dans le bundle ne devient pas trusted par le pin ;
- `F2` registration ne devient pas `known_from` ;
- `F3` receipt tardif ne prouve pas disponibilité antérieure ;
- `F4` absence de temps qualifié ne peut être réparée par défaut/horloge locale silencieuse.

### G — Direction / non-promotion
- `G0` record/receipt ne mint ni ne répare Trace/Action/Result ;
- `G1` re-attested historical memory n'est pas `ResearchRunEvidence`/`ResearchFindings` ;
- `G2` receipt ne produit ni connaissance ni `SUPPORTED` ;
- `G3` receipt/re-attestation ne produit jamais `AUTHORIZED` ;
- `G4` aucun broker/order/sizing/acquisition/backtest/live n'est ouvert.

**État après sélection : modèle de trust = SELECTED ; runtime P1.5 = BLOCKED.**

La prochaine mutation autorisée est uniquement l'ajout du breaker + workflow P1.5. Aucun runtime P1.5 ne doit exister avant l'observation de son FAIL initial.

---

# FORMALISATION GOUVERNÉE — 18 SEPTEMBRE 2026 — P1.6 MEMORY COLLECTION → AUDIT

**Contract ID:** `P1_6_MEMORY_COLLECTION_AUDIT_BOUNDARY_V1`  
**Base observée avant formalisation:** `ddbbcb5cc8644d62d22ebd69e2ca9cb3efee06b3`  
**Statut:** `FORMALIZED — QUALIFICATION-ONLY, NOT IMPLEMENTED`  
**Portée:** audit de collection de mémoires historiques P1.5 uniquement ; aucune promotion épistémique, aucune révision automatique, aucune autorisation opérationnelle.

## 54. Question de frontière

P1.6 répond uniquement à la question :

> **Une collection déclarée de mémoires historiques P1.5 est-elle constituée, reliée, dédupliquée, contextualisée et contestée correctement relativement à un scope d'audit déclaré extérieurement ?**

P1.6 ne répond pas à :

> « Cette collection prouve-t-elle qu'une hypothèse est vraie, qu'une stratégie fonctionne ou qu'une règle doit être changée ? »

Cette seconde question appartient à une future qualification épistémique/expérimentale qui reste **BLOCKED**.

Le premier P1.6 doit donc conserver la séparation :

`COLLECTION INTEGRITY / CONTESTABILITY AUDIT ≠ EPISTEMIC / KNOWLEDGE AUDIT`

## 55. Entrée minimale

L'entrée conceptuelle minimale est :

```text
externally declared AuditScope / AuditQuestion
+
1..N exact factory-attested HistoricalMemoryEpisode P1.5
↓
MemoryCollectionAuditAssessment
```

### 55.1 AuditScope / AuditQuestion externe

Le scope ne doit pas être inféré depuis la collection qu'il audite.

Il doit être fourni extérieurement à la collection et décrire au minimum, selon ce qui est réellement démontrable :

- une identité de scope/audit ;
- la question ou l'objet exact de l'audit ;
- la règle d'inclusion ;
- la règle d'exclusion ;
- l'univers ou population bornée attendue lorsque cet univers est connaissable ;
- les dimensions de contexte pertinentes pour comparer ou séparer les épisodes.

Le scope ne constitue pas une hypothèse scientifique validée. Il décrit uniquement **ce que l'audit prétend avoir reçu et examiné**.

Une collection ne peut jamais être considérée complète ou représentative simplement parce que ses propres membres disent l'être.

### 55.2 Collection P1.5

Chaque entrée utilisée comme preuve de collection doit être un `HistoricalMemoryEpisode` exact encore reconnu par l'attestation locale P1.5.

Ne constituent pas des entrées qualifiées :

- un `registration_id` seul ;
- un `episode_id` seul ;
- un record/receipt brut non re-attesté ;
- un dictionnaire/JSON ;
- une copie, reconstruction same-valued, `replace` ou objet manuel non attesté ;
- un épisode P1.4 brut présenté à la place de sa mémoire historique P1.5.

AUDIT peut consommer une attestation P1.5 ; il ne peut pas la créer, réparer ou reconstruire.

## 56. Sortie minimale

La sortie P1.6 doit rester un **constat d'audit de collection**.

Elle peut représenter conceptuellement :

- identité de l'audit ;
- identité du scope/question audité ;
- registrations effectivement examinées ;
- `episode_id` uniques observés ;
- groupes de registrations portant sur le même contenu ;
- duplications/incohérences de membership ;
- groupes ou différences de contexte pertinentes ;
- contradictions factuelles détectables ;
- état de complétude relativement au scope : démontrée / non démontrable / violée ;
- limites d'indépendance expérimentale ;
- limites temporelles ou de provenance pertinentes ;
- anomalies ;
- preuves/références utilisées ;
- verdict `PASS / FAIL / BLOCKED`.

Elle ne doit pas contenir ou produire automatiquement :

- `SUPPORTED` ;
- `REFUTED` ;
- `NOT_INTERPRETABLE` comme substitut à une absence de preuve d'audit ;
- connaissance validée ;
- vérité ;
- causalité ;
- niveau de confiance ;
- probabilité de vérité ;
- recommandation de règle ;
- recommandation de trading ;
- décision de révision ;
- `AUTHORIZED`.

## 57. Sémantique stricte des verdicts P1.6

### PASS

`PASS` signifie uniquement :

> **pour le scope déclaré et les preuves disponibles, la collection fournie satisfait les contrôles P1.6 exécutables de provenance, membership, déduplication, grouping, contextualisation, contradiction et complétude lorsque cette complétude est effectivement démontrable.**

Un `PASS` P1.6 n'est jamais un PASS scientifique ou épistémique sur l'efficacité du comportement observé.

### FAIL

`FAIL` signifie qu'une violation démontrée du contrat de collection existe, par exemple :

- entrée non P1.5-attestée présentée comme preuve ;
- membership incohérent ;
- duplication comptée comme occurrence supplémentaire ;
- registration rebondie/substituée ;
- contexte incompatible agrégé silencieusement ;
- contradiction supprimée ou masquée ;
- prétention de complétude contredite par les preuves ;
- promotion interdite vers connaissance/causalité/révision.

### BLOCKED

`BLOCKED` signifie qu'une propriété nécessaire ne peut pas être démontrée.

Exemples :

- univers attendu inconnu ;
- aucune preuve d'exhaustivité ;
- identité d'occurrence expérimentale indépendante absente ;
- temporalité requise mais non qualifiée ;
- règle de sélection insuffisante ;
- contradiction impossible à arbitrer dans le périmètre disponible.

`BLOCKED` n'est jamais converti en `PASS` par absence d'anomalie observable.

## 58. Membership, duplication et identité

P1.6 doit distinguer au minimum :

```text
physical copy
≠ registration
≠ episode content identity
≠ independent experimental occurrence
```

Règles obligatoires :

1. deux copies physiques du même bundle ne constituent qu'une même registration ;
2. le même `registration_id` rencontré plusieurs fois ne peut jamais augmenter le nombre d'éléments probatoires ;
3. plusieurs `registration_id` portant le même `episode_id` sont plusieurs captures du même contenu, pas plusieurs expériences indépendantes ;
4. plusieurs `episode_id` différents ne prouvent pas, à eux seuls, plusieurs occurrences expérimentales indépendantes ;
5. P1.6 ne peut pas fabriquer une identité d'occurrence globale absente de P1.5 ;
6. une future preuve d'indépendance expérimentale devra être qualifiée séparément.

Le système peut produire des **comptages descriptifs** de registrations ou contenus. Ces comptages ne doivent jamais être renommés silencieusement en réplications indépendantes.

## 59. Contextes et comparabilité

Les dimensions déjà présentes dans les épisodes historiques — notamment provenance, research run, versions de code/configuration/dataset, `context_id`, Decision, Action/behavior et Result/outcome — doivent rester visibles à l'audit.

P1.6 doit :

- détecter les contextes différents ;
- conserver les différences plutôt que les écraser ;
- grouper uniquement selon une règle déclarée ;
- refuser de traiter automatiquement des contextes différents comme homogènes ;
- signaler en anomalie ou `BLOCKED` toute comparabilité nécessaire mais non démontrée.

Une similarité de résultat ne prouve pas une similarité de conditions.

## 60. Contradictions

P1.6 doit conserver les contradictions observables.

Une contradiction ne doit pas être :

- supprimée ;
- filtrée silencieusement ;
- masquée par moyenne/agrégation ;
- transformée en simple succès majoritaire ;
- réparée en modifiant rétroactivement les épisodes.

L'audit peut constater :

- résultats incompatibles ;
- comportements identiques suivis d'outcomes différents ;
- contextes apparemment semblables avec résultats divergents ;
- claims de scope incompatibles avec les membres fournis.

La présence d'une contradiction ne donne pas automatiquement son explication ni sa cause.

P1.6 peut émettre un constat/anomalie ou `BLOCKED`; l'arbitrage sémantique détaillé reste une capacité séparée.

## 61. Complétude et survivorship bias

La complétude doit être relative à un scope externe borné.

Deux cas doivent être distingués :

### 61.1 Univers démontrable

Si le scope fournit un univers attendu vérifiable et une règle de membership testable, P1.6 peut comparer membres attendus et membres observés.

Une différence démontrée peut produire `FAIL`.

Une concordance démontrée peut permettre un `PASS` **de complétude de collection uniquement**.

### 61.2 Univers non démontrable

Si l'univers attendu, la règle de capture ou les absences ne sont pas vérifiables, la complétude doit être `BLOCKED`.

Une collection de résultats tous favorables ne prouve jamais qu'aucun résultat défavorable n'a été omis.

Ainsi :

`ALL PROVIDED EPISODES ARE VALID ≠ ALL RELEVANT EPISODES WERE PROVIDED`

et :

`NO OBSERVED MISSING MEMBER ≠ PROOF OF NO MISSING MEMBER`.

## 62. Indépendance expérimentale

P1.6 doit explicitement conserver :

**INDEPENDENCE STATUS = BLOCKED**

tant qu'aucune preuve qualifiée d'identité/conditions d'occurrence expérimentale indépendante n'existe.

Le contrat P1.6 ne peut pas déduire l'indépendance à partir de :

- `registration_id` différents ;
- `episode_id` différents ;
- `research_run_id` différents ;
- timestamps ou ordre local non qualifiés ;
- résultats différents ;
- répétition du même behavior ;
- nombre total de membres.

L'absence de preuve d'indépendance n'empêche pas un audit descriptif de collection. Elle interdit seulement de transformer ce descriptif en preuve de réplication.

## 63. Observation, fréquence, succès et connaissance

Les séparations antérieures restent obligatoires et sont étendues à la collection :

```text
ONE OBSERVATION ≠ KNOWLEDGE
MANY OBSERVATIONS ≠ KNOWLEDGE
MANY REGISTRATIONS ≠ REPLICATIONS
MANY SUCCESSFUL OUTCOMES ≠ SUPPORTED HYPOTHESIS
TEMPORAL SUCCESSION ≠ CAUSALITY
AUDIT PASS ≠ KNOWLEDGE PASS
AUDIT PASS ≠ REVISION
AUDIT PASS ≠ AUTHORIZATION
```

P1.6 peut décrire :

> « N registrations examinées contiennent tel outcome sous tels contextes ».

P1.6 ne peut pas convertir cette phrase en :

> « N expériences indépendantes confirment que le behavior cause cet outcome ».

La charte `ResearchFindings` et ses statuts ne doivent pas être importés dans P1.6 comme raccourci.

## 64. Temporalité

P1.6 n'invente aucun nouveau temps de connaissance.

Une mémoire P1.5 auditée aujourd'hui ne devient pas, de ce seul fait :

- connue à l'heure d'une Decision passée ;
- disponible avant sa capture ;
- admissible dans un ancien research run ;
- valide depuis l'instant du résultat.

Si la question d'audit exige une disponibilité historique ou un ordre temporel qualifié qui n'est pas démontré, le verdict pertinent doit être `BLOCKED`.

P1.6 ne rend pas normatif le contrat temporel encore non qualifié par simple besoin de l'audit.

## 65. Direction de l'autorité

La direction autorisée est :

```text
P1.5 HISTORICAL MEMORY
        ↓
P1.6 COLLECTION AUDIT
        ↓
constat / verdict / anomalies
```

Sont interdits :

```text
AUDIT → réparation de MEMORY
AUDIT → mint Trace/Action/Result
AUDIT → ResearchFindings
AUDIT → KNOWLEDGE
AUDIT → REVISION automatique
AUDIT → Decision/Action AUTHORIZED
AUDIT → broker/backtest/live
```

Un audit peut demander un retest, signaler une contradiction, constater une preuve insuffisante ou recommander conceptuellement qu'une question soit examinée par la future fonction REVISION. Il ne réalise jamais lui-même cette révision.

## 66. Relation avec REVISION

P1.6 ne ferme pas R9 `AUDIT → REVISION`.

La sortie P1.6 peut seulement fournir une base contestée à une future fonction REVISION.

Une future REVISION devra rester capable de conclure :

- maintenir l'état ;
- ne rien changer ;
- demander une nouvelle expérience ;
- demander une preuve supplémentaire ;
- reformuler une hypothèse/question ;
- suspendre une proposition de changement.

Même une révision ultérieure ne pourra pas modifier le comportement opérationnel sans repasser par nouvelle expérience/preuve et autorisation contrôlée lorsque requises.

## 67. Invariants adversariaux minimaux P1.6

La future qualification P1.6 devra au minimum casser les familles suivantes avant tout PASS :

### A — Scope / question auto-sélectionnés
- collection choisissant elle-même son scope ;
- scope absent ou vide ;
- inclusion/exclusion modifiées après observation des outcomes ;
- scope prétendant une population qu'il ne peut identifier.

### B — Entrées non qualifiées
- objet manuel same-valued ;
- copy/deepcopy/replace ;
- JSON/dict ;
- raw record/receipt ;
- simple `registration_id` / `episode_id` ;
- `HistoricalMemoryEpisode` muté/inattesté.

### C — Duplication / inflation
- même registration répétée N fois ;
- copies physiques traitées comme nouveaux membres ;
- plusieurs registrations du même `episode_id` comptées comme réplications ;
- nouveaux `episode_id` comptés automatiquement comme indépendants.

### D — Membership / complétude / survivorship
- membre hors scope accepté silencieusement ;
- membre attendu manquant ;
- population inconnue mais verdict de complétude PASS ;
- collection favorable sélectionnée après coup ;
- absence de membre défavorable interprétée comme preuve qu'il n'en existe pas.

### E — Contexte
- versions/configurations/datasets/contextes incompatibles agrégés silencieusement ;
- grouping modifié pour améliorer le résultat ;
- différences de contexte supprimées de la sortie d'audit.

### F — Contradictions
- outcome contradictoire supprimé ;
- contradiction transformée en moyenne sans trace ;
- majorité utilisée pour effacer la minorité ;
- contradiction interprétée automatiquement comme causalité ou erreur d'un membre.

### G — Promotion interdite
- fréquence → réplication ;
- répétition → `SUPPORTED` ;
- succès → connaissance ;
- succession → causalité ;
- PASS d'audit → recommandation de règle ;
- PASS d'audit → REVISION ;
- PASS d'audit → `AUTHORIZED` / opérationnel.

### H — Temporalité / provenance
- audit tardif présenté comme connaissance antérieure ;
- local clock réparant une temporalité absente ;
- membership reconstruit depuis IDs sans preuve ;
- audit réparant ou re-attestant un membre amont.

## 68. Qualification positive autorisée à P1.6

Un futur PASS P1.6 pourra signifier uniquement :

- le scope/question d'audit a été fourni séparément de la collection ;
- toutes les entrées utilisées comme membres qualifiés sont des `HistoricalMemoryEpisode` P1.5 exacts et attestés ;
- membership et duplications ont été vérifiés ;
- les registrations same-content ont été regroupées sans être promues en réplications ;
- les différences de contexte pertinentes ont été conservées ;
- les contradictions détectables ont été conservées et signalées ;
- la complétude a été qualifiée uniquement lorsqu'elle était démontrable relativement au scope ;
- l'indépendance expérimentale non démontrée reste explicitement `BLOCKED` ;
- le résultat est limité à constat/verdict/anomalies `PASS / FAIL / BLOCKED`.

Un PASS P1.6 ne signifiera pas :

- hypothèse `SUPPORTED` ou `REFUTED` ;
- connaissance validée ;
- causalité ;
- confiance suffisante ;
- réplication indépendante démontrée ;
- efficacité d'une stratégie ;
- recommandation de règle ;
- décision de révision ;
- modification de comportement ;
- autorisation opérationnelle.

## 69. État après formalisation P1.6

**FORMALISATION P1.6 : PASS.**

La frontière exécutable reste :

**P1.5 HISTORICAL MEMORY COLLECTION → P1.6 COLLECTION AUDIT : BLOCKED / NOT IMPLEMENTED.**

La frontière suivante reste également :

**P1.6 AUDIT → REVISION : BLOCKED / NOT FORMALIZED AS EXECUTABLE BOUNDARY.**

La cartographie historique R7/R8/R9 plus haut dans ce document est conservée comme état observé au moment de sa rédaction. Les addenda P1.4/P1.5 ont depuis fermé TRACE→MEMORY dans leur périmètre qualifié ; le présent addendum formalise désormais R8 sans prétendre qu'il est exécutable.

## 70. Prochaine action gouvernée unique

**Déterminer, à partir des APIs P1.5 réelles et sans implémenter encore AUDIT, le plus petit `AuditScope` et le plus petit `MemoryCollectionAuditAssessment` exécutables capables de représenter exactement scope externe, membership, déduplication, content-groups, context-groups, contradictions, complétude `PASS/FAIL/BLOCKED` et indépendance `BLOCKED`, puis construire le breaker A0–H avant toute implémentation.**

---

# SÉLECTION GOUVERNÉE — 18 SEPTEMBRE 2026 — P1.6 MINIMAL EXECUTABLE AUDIT MODEL

**Selection ID:** `P1_6_MINIMAL_COLLECTION_AUDIT_MODEL_V1`  
**Base observée avant sélection:** `a03204624be47136736d82531a7449226d4388f6`  
**Statut:** `SELECTED — TEST-FIRST, NOT IMPLEMENTED`  
**Portée:** définition du plus petit modèle exécutable P1.6 ; aucun runtime AUDIT ne doit exister avant le breaker initial.

## 71. Surface exécutable minimale retenue

Le futur module candidat est borné à une surface équivalente à :

```text
CONTRACT = "P1_6_MEMORY_COLLECTION_AUDIT_BOUNDARY_V1"

AuditScope
MemoryCollectionAuditAssessment

create_audit_scope(...)
audit_memory_collection(scope, memories)
is_factory_attested_memory_collection_audit(value)
```

Aucune API de connaissance, promotion, révision ou autorisation n'appartient à P1.6.

## 72. Modèle minimal `AuditScope`

Le scope exécutable minimal retenu est :

```text
AuditScope
- scope_id
- question
- expected_registration_ids : tuple[str, ...] | None
- context_fields : tuple[str, ...]
```

### 72.1 `scope_id`

`scope_id` doit être content-bound à la déclaration canonique du scope.

Deux déclarations identiques peuvent produire le même `scope_id`.

Une modification de la question, de l'univers attendu ou des dimensions de contexte doit produire une autre identité.

Le `scope_id` n'est pas une autorité et ne prouve aucune vérité sur la population réelle. Il identifie seulement la déclaration d'audit.

### 72.2 `question`

La question doit être non vide et descriptive.

Elle ne devient pas une hypothèse scientifique, un claim `SUPPORTED` ou un objectif d'optimisation.

### 72.3 `expected_registration_ids`

Deux modes seulement sont nécessaires :

#### Univers borné déclaré

```text
expected_registration_ids = tuple exact de registration_id attendus
```

Ce tuple constitue l'univers de membership déclaré pour **cet audit**.

P1.6 peut alors comparer :

- attendus ;
- observés ;
- manquants ;
- inattendus.

Un matching exact permet seulement `completeness_status = PASS` relativement à cette déclaration.

Il ne prouve pas que cette déclaration représente toute la réalité historique au-delà du scope fourni.

#### Univers non démontrable

```text
expected_registration_ids = None
```

Alors :

```text
completeness_status = BLOCKED
```

obligatoirement, sauf violation plus forte produisant `FAIL`.

Aucun champ `complete=True`, `trust_scope=True`, `assume_exhaustive=True` ou équivalent ne doit exister.

### 72.4 `context_fields`

Le grouping de contexte doit être déclaré avant l'audit via un tuple non vide de champs autorisés.

Le premier modèle autorise seulement des dimensions descriptives déjà présentes dans l'épisode P1.4 et pertinentes au contexte/comportement :

```text
provenance_id
research_run_id
code_version
configuration_version
dataset_id
dataset_version
context_id
decision
behavior
```

Sont explicitement interdits comme dimensions de contexte :

- `outcome` ;
- `result_id` ;
- `action_id` ;
- `decision_id` ;
- `episode_id` ;
- `registration_id` ;
- tout champ inconnu.

Cette restriction évite notamment de créer des groupes après coup en fonction du résultat observé.

Le scope doit être immuable ; ses listes logiques sont représentées par des tuples.

## 73. Modèle minimal `MemoryCollectionAuditAssessment`

Le plus petit assessment retenu doit représenter exactement :

```text
MemoryCollectionAuditAssessment
- audit_id
- scope_id
- verdict
- completeness_status
- independence_status
- examined_registration_ids
- missing_registration_ids
- unexpected_registration_ids
- duplicate_registration_ids
- unique_episode_ids
- content_groups
- context_groups
- contradiction_groups
- anomalies
```

Tous les ensembles/listes logiques doivent être exposés sous forme immuable et déterministe.

### 73.1 `audit_id`

`audit_id` est une identité de contenu d'audit, dérivée au minimum de :

- `scope_id` ;
- membres P1.5 effectivement examinés ;
- résultat structuré de l'audit.

Il n'est ni une autorité ni une identité d'expérience.

### 73.2 Membership

`examined_registration_ids` contient les registrations uniques effectivement admises comme membres P1.5 exacts.

`duplicate_registration_ids` signale toute répétition du même `registration_id` dans l'entrée, y compris deux re-attestations locales distinctes de la même registration.

Les duplicates ne sont jamais comptés deux fois dans `examined_registration_ids`.

### 73.3 Missing / unexpected

Quand l'univers attendu est borné :

```text
missing = expected - examined
unexpected = examined - expected
```

Toute différence produit `completeness_status = FAIL`.

Quand l'univers est `None` :

- `missing_registration_ids` reste vide ;
- `unexpected_registration_ids` reste vide ;
- `completeness_status = BLOCKED`.

### 73.4 Content groups

`content_groups` groupe déterministiquement les registrations uniques par `episode_id`.

Forme minimale conceptuelle :

```text
(
  (episode_id, (registration_id, ...)),
  ...
)
```

Deux registrations dans le même groupe sont plusieurs captures du même contenu, jamais plusieurs réplications.

### 73.5 Context groups

`context_groups` groupe les registrations uniques selon **exactement** les `context_fields` du scope.

Forme minimale conceptuelle :

```text
(
  (
    ((field_name, field_value), ...),
    (registration_id, ...)
  ),
  ...
)
```

L'ordre doit être déterministe.

Aucun champ non déclaré dans `context_fields` ne peut modifier le grouping.

### 73.6 Contradiction groups

Une contradiction factuelle minimale P1.6 est détectable lorsque, dans un même context-group déclaré :

- la même valeur `decision` ;
- le même `behavior` ;

sont associés à au moins deux `outcome` différents.

`contradiction_groups` conserve les registration IDs concernés.

La contradiction ne dit pas quelle observation est correcte et ne prouve aucune causalité.

Des outcomes différents dans des context-groups différents ne constituent pas automatiquement une contradiction P1.6.

## 74. Règles de verdict retenues

### 74.1 Violations d'entrée

Un membre non P1.5-attesté n'est pas converti en assessment permissif.

L'audit doit refuser l'entrée par exception fail-closed.

### 74.2 Overall `FAIL`

Le verdict global est `FAIL` si au moins une violation démontrée de collection existe, notamment :

- registration dupliquée dans l'entrée ;
- membre attendu manquant ;
- membre inattendu dans un univers borné ;
- incohérence structurelle démontrée.

La simple présence d'une contradiction correctement conservée n'est pas, à elle seule, une défaillance du mécanisme d'audit.

### 74.3 Overall `BLOCKED`

Si aucune violation `FAIL` n'existe mais que `expected_registration_ids is None` :

`verdict = BLOCKED`

car la complétude n'est pas démontrable.

### 74.4 Overall `PASS`

`verdict = PASS` est permis uniquement si :

- toutes les entrées sont des P1.5 exacts attestés ;
- aucune duplication de registration n'existe ;
- un univers borné a été déclaré ;
- aucun attendu ne manque ;
- aucun inattendu n'est présent ;
- grouping/context/contradictions ont été conservés correctement.

Même dans ce cas :

```text
independence_status = BLOCKED
```

obligatoirement dans P1.6 V1.

Ainsi un P1.6 `PASS` peut coexister avec une indépendance expérimentale `BLOCKED` : le PASS porte sur l'intégrité de la collection, pas sur sa force épistémique.

## 75. Attestation locale de l'assessment

Le futur assessment P1.6 doit suivre la même discipline d'identité locale que les frontières précédentes :

- seul l'objet produit par `audit_memory_collection` est factory-attested ;
- manuel same-valued, copy, deepcopy, replace ou reconstruction ne récupèrent pas l'attestation ;
- mutation après production invalide l'attestation ;
- cette attestation ne donne aucune autorité sur MEMORY, KNOWLEDGE ou REVISION.

Cette propriété est requise pour qu'une future frontière AUDIT → REVISION puisse distinguer un constat réellement produit par P1.6 d'un objet forgé same-valued.

## 76. Non-modèle explicite

P1.6 V1 ne contient volontairement aucun champ :

- `supported` ;
- `refuted` ;
- `knowledge` ;
- `confidence` ;
- `probability` ;
- `causal` ;
- `recommended_rule` ;
- `revision` ;
- `authorized` ;
- `known_from` ;
- `registered_at` ;
- `independent_count`.

Il n'existe pas non plus de compteur de « réplications ».

Les comptages autorisés sont descriptifs uniquement : registrations uniques, contenus uniques, groupes.

## 77. Breaker A0–H à construire avant runtime

Le breaker test-first doit cibler au minimum :

### A — Scope externe / identité
- scope positif borné ;
- scope absent ;
- question vide ;
- duplicate expected registration IDs ;
- champ de contexte inconnu/interdit, notamment `outcome` ;
- identité de scope content-bound ;
- immutabilité ;
- aucune dérivation de scope depuis la collection.

### B — Membres P1.5 exacts
- exact historical memory positif ;
- manuel same-valued ;
- copy/deepcopy/replace ;
- dict/JSON ;
- P1.4 brut ;
- IDs seuls ;
- historique muté/inattesté.

### C — Duplication / content groups
- même object répété ;
- deux re-attestations locales de la même registration ;
- deux registrations du même `episode_id` ;
- différents `episode_id` sans promotion à indépendance ;
- déterminisme indépendant de l'ordre d'entrée.

### D — Membership / complétude
- univers borné exact → PASS de complétude ;
- membre attendu manquant → FAIL ;
- inattendu → FAIL ;
- univers `None` → BLOCKED ;
- collection favorable + univers inconnu reste BLOCKED.

### E — Context groups
- contextes différents séparés ;
- grouping suit seulement `context_fields` ;
- ordre déterministe ;
- outcome ne peut pas servir de dimension de grouping.

### F — Contradictions
- même contexte + même decision/behavior + outcomes différents conservés ;
- majorité ne supprime pas la minorité ;
- outcomes différents dans contextes différents non fusionnés en contradiction ;
- contradiction ne produit pas cause/connaissance.

### G — Promotion interdite
- aucun statut `SUPPORTED/REFUTED` ;
- aucun knowledge/confidence/causality ;
- aucune recommendation/revision ;
- aucune autorisation/opération ;
- indépendance toujours `BLOCKED`.

### H — Provenance / temporalité / assessment identity
- aucun timestamp implicite ;
- pas d'horloge locale ;
- manual/copy/replace assessment non attesté ;
- mutation invalide l'attestation ;
- AUDIT ne répare ni ne re-atteste un membre P1.5 ;
- pas de reconstruction de membership depuis des IDs seuls.

**État après sélection : modèle P1.6 = SELECTED ; runtime P1.6 = BLOCKED / NOT IMPLEMENTED.**

## 78. Prochaine mutation autorisée

Ajouter uniquement :

- le breaker P1.6 A0–H ;
- le workflow de cassage P1.6.

Aucun `src/memory_audit.py` ou runtime équivalent ne doit exister avant l'observation du FAIL initial du breaker.

---

# FORMALISATION GOUVERNÉE — 18 SEPTEMBRE 2026 — P1.7 AUDIT → REVISION

**Contract ID:** `P1_7_AUDIT_REVISION_BOUNDARY_V1`  
**Base observée avant formalisation:** `e98ee16ec907dc3263c8d9bd5ce74ce122d2415b`  
**Statut:** `FORMALIZED — QUALIFICATION-ONLY, NOT IMPLEMENTED`  
**Portée:** décision de révision gouvernée issue d'un audit P1.6 exact ; aucune connaissance, règle, expérience, autorisation ou modification de comportement n'est créée par P1.7.

## 79. État amont reconnu

Depuis les sections historiques P1.6 plus haut dans ce document, la frontière :

```text
P1.5 HISTORICAL MEMORY COLLECTION
↓
P1.6 MEMORY COLLECTION AUDIT
```

a été implémentée et qualifiée dans son périmètre `qualification-only`.

P1.6 produit désormais un `MemoryCollectionAuditAssessment` factory-attested, limité à l'intégrité/contestabilité de collection.

Cette évolution ne ferme pas automatiquement R9.

La frontière suivante reste :

```text
P1.6 AUDIT
↓
P1.7 REVISION
```

**BLOCKED / NOT IMPLEMENTED** au moment de cette formalisation.

## 80. Question minimale de P1.7

P1.7 répond uniquement à la question :

> **Peut-on enregistrer de manière contrôlée une orientation de révision explicitement proposée à partir d'un audit P1.6 exact, sans laisser le verdict d'audit inventer automatiquement la révision et sans transformer cette révision en connaissance, preuve, règle, expérience ou permission opérationnelle ?**

Le noyau minimal est :

```text
exact factory-attested MemoryCollectionAuditAssessment
+
matching content-bound AuditScope
+
externally declared disposition
+
externally declared detail
↓
factory-attested RevisionDecision
```

P1.7 ne choisit pas la disposition à partir de `PASS / FAIL / BLOCKED`.

## 81. Séparations sémantiques obligatoires

P1.7 doit préserver simultanément :

```text
AUDIT ≠ REVISION
AUDIT VERDICT ≠ REVISION DISPOSITION
REVISION DECISION ≠ KNOWLEDGE
REVISION DECISION ≠ EVIDENCE
REQUEST_NEW_EVIDENCE ≠ EVIDENCE OBTAINED
REQUEST_NEW_EXPERIMENT ≠ EXPERIMENT CREATED OR EXECUTED
REFORMULATED QUESTION ≠ VALIDATED HYPOTHESIS
KEEP_CURRENT_STATE ≠ VALIDATION OF CURRENT STATE
REVISION ≠ AUTHORIZATION
REVISION ≠ BEHAVIOR CHANGE
```

Et, de manière particulièrement stricte :

```text
SOURCE BLOCKED
→ REVISION
→ SOURCE BLOCKED REMAINS VISIBLE
```

Une révision ne « répare » jamais un `BLOCKED` amont.

## 82. Entrée P1.7 — assessment exact

L'entrée d'audit doit être l'objet complet :

`MemoryCollectionAuditAssessment`

produit et toujours reconnu par l'attestation locale P1.6.

Ne constituent pas une preuve P1.7 :

- `audit_id` seul ;
- dictionnaire/JSON ;
- dataclass reconstruite manuellement ;
- copy/deepcopy/replace same-valued ;
- assessment muté ;
- assessment structurellement plausible mais non factory-attested.

P1.7 consomme l'autorité P1.6 ; il ne peut ni créer, ni réparer, ni re-attester un audit amont.

## 83. Entrée P1.7 — AuditScope correspondant

Le `AuditScope` correspondant doit également être fourni.

P1.7 doit vérifier au minimum :

1. que le scope est structurellement valide selon le contrat P1.6 ;
2. que son identité content-bound est recomputable ;
3. que `scope.scope_id == assessment.scope_id`.

Le `AuditScope` reste une **déclaration content-bound**, pas une autorité process-locale.

Une reconstruction strictement same-valued est donc admissible si son identité recalculée correspond exactement.

En revanche, doivent échouer :

- question modifiée avec ancien `scope_id` ;
- membership attendu modifié avec ancien `scope_id` ;
- `context_fields` modifiés avec ancien `scope_id` ;
- scope étranger ;
- `scope_id` simplement copié d'un autre audit.

L'assessment seul ne suffit pas à comprendre la question source, car P1.6 conserve `scope_id` mais pas nécessairement le texte complet de la question dans sa sortie.

## 84. Dispositions P1.7 autorisées

La V1 autorise exactement quatre dispositions :

```text
KEEP_CURRENT_STATE
REQUEST_NEW_EVIDENCE
REQUEST_NEW_EXPERIMENT
REFORMULATE_QUESTION
```

Toute autre disposition doit échouer fermée.

Sont notamment hors P1.7 V1 :

- `CHANGE_RULE` ;
- `UPDATE_KNOWLEDGE` ;
- `SET_CONFIDENCE` ;
- `AUTHORIZE_ACTION` ;
- `CHANGE_POSITION_SIZE` ;
- `RUN_BACKTEST` ;
- `SEND_ORDER` ;
- `ACTIVATE_LIVE`.

## 85. Disposition externe, jamais dérivée automatiquement

La disposition doit être explicitement fournie à P1.7.

Le runtime futur ne doit contenir aucune table implicite du type :

```text
PASS    → KEEP_CURRENT_STATE
FAIL    → REQUEST_NEW_EXPERIMENT
BLOCKED → REQUEST_NEW_EVIDENCE
```

Ces correspondances sont interdites.

Exemples :

- un `FAIL` de membership peut appeler une meilleure collecte, pas nécessairement une expérience ;
- un `BLOCKED` de complétude peut nécessiter davantage de preuves documentaires ;
- un `PASS` de collection peut encore contenir des contradictions ou une indépendance `BLOCKED`.

Ainsi :

`AUDIT VERDICT ≠ REVISION DISPOSITION`.

## 86. `detail` externe minimal

Chaque disposition doit recevoir un `detail` non vide fourni extérieurement.

Le `detail` documente ce qui est demandé ou la raison de l'orientation ; il ne devient pas une preuve.

### 86.1 KEEP_CURRENT_STATE

Le detail explique pourquoi aucune modification gouvernée n'est demandée à ce stade.

Cette disposition signifie uniquement :

> **conserver l'état existant pour l'instant.**

Elle ne signifie jamais :

- état valide ;
- règle correcte ;
- connaissance vraie ;
- audit résolu ;
- risque absent.

### 86.2 REQUEST_NEW_EVIDENCE

Le detail décrit la preuve supplémentaire demandée.

Cette disposition ne crée pas cette preuve et ne permet pas de prétendre qu'elle existe.

### 86.3 REQUEST_NEW_EXPERIMENT

Le detail décrit l'expérience supplémentaire demandée à un niveau suffisant pour la distinguer d'une simple intention vide.

P1.7 :

- ne crée pas l'expérience ;
- ne la lance pas ;
- ne la qualifie pas ;
- n'autorise aucune acquisition, backtest, broker ou live.

### 86.4 REFORMULATE_QUESTION

Pour cette disposition, le detail doit représenter une nouvelle formulation non vide de la question d'audit.

Cette formulation doit différer de `scope.question`.

Elle ne devient pas :

- nouvelle hypothèse validée ;
- nouveau `AuditScope` qualifié ;
- nouvelle connaissance ;
- nouvelle règle.

Une future étape devra explicitement créer/qualifier le nouvel objet nécessaire.

## 87. Compatibilité disposition ↔ verdict

P1.7 V1 n'impose pas de matrice automatique disposition/verdict.

Les quatre dispositions peuvent être proposées face à `PASS`, `FAIL` ou `BLOCKED`, sous réserve que :

- le detail soit explicite ;
- le verdict source reste conservé ;
- aucune propriété `BLOCKED` ne soit promue ;
- aucune disposition ne soit interprétée comme preuve de vérité ou permission.

Cette absence de matrice est intentionnelle : la sémantique exacte de la réponse dépend de l'objet audité et de la justification, pas uniquement du mot `PASS/FAIL/BLOCKED`.

## 88. Sortie minimale — `RevisionDecision`

Le plus petit objet de sortie candidat est :

```text
RevisionDecision
- revision_id
- audit_id
- scope_id
- disposition
- detail
- source_verdict
- source_completeness_status
- source_independence_status
```

### 88.1 `revision_id`

`revision_id` doit être une identité content-bound dérivée au minimum de :

- contract P1.7 ;
- `audit_id` ;
- `scope_id` ;
- disposition ;
- detail ;
- snapshots des statuts source conservés.

Une décision identique peut donc avoir la même identité de contenu.

`revision_id` n'est pas une autorisation ni une identité d'expérience.

### 88.2 Snapshot des statuts source

La sortie doit conserver explicitement :

- `source_verdict` ;
- `source_completeness_status` ;
- `source_independence_status`.

Objectif :

> empêcher une étape downstream de masquer qu'une orientation a été prise à partir d'un audit `FAIL`, `BLOCKED` ou avec indépendance `BLOCKED`.

P1.7 ne transforme jamais ces snapshots en un nouveau verdict épistémique.

## 89. Préservation obligatoire de BLOCKED

Les statuts `BLOCKED` amont doivent rester littéralement visibles dans le `RevisionDecision`.

Exemples obligatoires :

```text
assessment.verdict = BLOCKED
→ RevisionDecision.source_verdict = BLOCKED
```

```text
assessment.completeness_status = BLOCKED
→ RevisionDecision.source_completeness_status = BLOCKED
```

```text
assessment.independence_status = BLOCKED
→ RevisionDecision.source_independence_status = BLOCKED
```

Aucune disposition ne peut produire :

```text
BLOCKED → PASS
BLOCKED → RESOLVED
BLOCKED → SUPPORTED
BLOCKED → AUTHORIZED
```

Le futur runtime ne doit posséder aucun paramètre comme :

- `assume_resolved=True` ;
- `ignore_blocked=True` ;
- `override_audit=True` ;
- `force_revision=True`.

## 90. Attestation locale de RevisionDecision

Le futur `RevisionDecision` doit être factory-attested exact-object.

Seul l'objet produit par la future fonction P1.7 qualifiée pourra être considéré comme décision de révision admissible.

Ne récupèrent pas cette attestation :

- objet manuel same-valued ;
- copy ;
- deepcopy ;
- replace ;
- reconstruction JSON/dict ;
- mutation post-production.

Cette attestation sert uniquement à la future chaîne downstream.

Elle ne donne aucune autorité rétroactive sur AUDIT, MEMORY ou les objets plus amont.

## 91. Direction de l'autorité

Direction autorisée :

```text
matching AuditScope
+
exact P1.6 MemoryCollectionAuditAssessment
+
external disposition/detail
↓
P1.7 RevisionDecision
```

Directions interdites :

```text
REVISION → réparer AUDIT
REVISION → modifier MEMORY
REVISION → créer ResearchFindings
REVISION → créer connaissance validée
REVISION → changer une règle
REVISION → créer/exécuter une expérience
REVISION → autoriser une Action
REVISION → acquisition/backtest/broker/live
```

P1.7 est une décision gouvernée sur **ce qu'il faut examiner/conserver/demander ensuite**, pas une exécution de ce changement.

## 92. Relation avec nouvelle preuve / expérience

Le chemin reste :

```text
P1.6 AUDIT
↓
P1.7 REVISION
↓
future NEW EVIDENCE / EXPERIENCE
↓
future qualification
↓
CONTROLLED AUTHORIZATION when applicable
↓
future behavior change
```

Donc :

```text
REQUEST_NEW_EVIDENCE ≠ NEW EVIDENCE
REQUEST_NEW_EXPERIMENT ≠ NEW EXPERIMENT
```

La frontière exacte P1.7 → nouvelle preuve/expérience reste **BLOCKED / non formalisée comme frontière exécutable**.

## 93. Pas de temporalité inventée

P1.7 V1 n'ajoute aucun :

- `known_from` ;
- `valid_from` ;
- `revision_at` ;
- `registered_at` ;
- horodatage local faisant autorité.

Une décision de révision produite aujourd'hui ne réécrit pas la connaissance disponible au moment d'une Decision historique.

Si une future révision exige une temporalité normative, celle-ci devra être qualifiée séparément.

## 94. Catalogue adversarial minimal P1.7

La future qualification devra au minimum casser les familles suivantes.

### A — Assessment source
- exact P1.6 assessment positif ;
- `audit_id` seul ;
- manuel same-valued ;
- copy/deepcopy/replace ;
- dict/JSON ;
- assessment muté/inattesté ;
- assessment étranger présenté sous un `audit_id` attendu.

### B — Scope matching
- exact/value-equivalent content-bound scope positif ;
- scope absent ;
- scope étranger ;
- question modifiée + stale `scope_id` ;
- membership attendu modifié + stale `scope_id` ;
- context fields modifiés + stale `scope_id` ;
- `scope_id` seul utilisé à la place du scope.

### C — Disposition
- chacune des quatre dispositions positives ;
- disposition absente/vide ;
- disposition inconnue ;
- casse/alias permissif non prévu ;
- `CHANGE_RULE`, `AUTHORIZED`, `RUN_BACKTEST`, etc. rejetés ;
- verdict source utilisé pour sélectionner silencieusement la disposition.

### D — Detail
- detail non vide positif ;
- detail absent/vide/whitespace ;
- `REFORMULATE_QUESTION` avec question identique ;
- reformulation vide ;
- detail traité comme preuve obtenue ;
- detail traité comme expérience exécutée.

### E — Préservation des statuts source
- source `PASS` conservé ;
- source `FAIL` conservé ;
- source `BLOCKED` conservé ;
- completeness `BLOCKED` conservé ;
- independence `BLOCKED` conservé ;
- tentative de mutation/promotion des snapshots rejetée.

### F — Sémantique des dispositions
- KEEP ≠ validation ;
- REQUEST_NEW_EVIDENCE ≠ evidence ;
- REQUEST_NEW_EXPERIMENT ≠ experiment ;
- REFORMULATE ≠ hypothesis ;
- aucune disposition ne crée knowledge/confidence/causality.

### G — RevisionDecision identity
- production positive factory-attested ;
- manual same-valued non attesté ;
- copy/deepcopy/replace non attesté ;
- mutation invalide l'attestation ;
- identité content-bound ;
- changement de disposition/detail change `revision_id`.

### H — Reverse authority / bypass
- REVISION ne répare pas assessment ;
- REVISION ne répare pas scope ;
- REVISION ne mint pas MEMORY/AUDIT/ResearchFindings ;
- aucune règle comportementale ;
- aucune autorisation ;
- aucune acquisition/backtest/order/live ;
- aucune horloge locale donnant une autorité temporelle.

## 95. Qualification positive autorisée à P1.7

Un futur PASS P1.7 pourra signifier uniquement :

- un assessment P1.6 exact et attesté a été reçu ;
- son `AuditScope` correspondant a été vérifié par identité content-bound ;
- une disposition explicitement externe parmi les quatre autorisées a été reçue ;
- un detail non vide et cohérent avec cette disposition a été reçu ;
- la décision de révision conserve exactement les statuts source ;
- les `BLOCKED` restent visibles ;
- la sortie est une `RevisionDecision` factory-attested et content-bound ;
- aucune mutation de connaissance, règle, expérience ou comportement n'a été effectuée.

Un PASS P1.7 ne signifiera pas :

- connaissance validée ;
- hypothèse soutenue/refutée ;
- nouvelle preuve acquise ;
- nouvelle expérience exécutée ;
- règle corrigée ;
- changement de comportement approuvé ;
- autorisation opérationnelle.

## 96. État après formalisation P1.7

**FORMALISATION P1.7 : PASS.**

La frontière exécutable reste :

**P1.6 AUDIT → P1.7 REVISION : BLOCKED / NOT IMPLEMENTED.**

La frontière suivante reste :

**P1.7 REVISION → NEW EVIDENCE / EXPERIENCE : BLOCKED / NOT FORMALIZED AS EXECUTABLE BOUNDARY.**

La cartographie historique R9 plus haut dans ce document reste conservée comme preuve de l'état observé au moment de sa rédaction ; le présent addendum formalise désormais R9 sans prétendre qu'il est exécutable.

## 97. Prochaine action gouvernée unique

**Déterminer, à partir des APIs P1.6 réelles et sans implémenter encore REVISION, le plus petit `RevisionDecision` exécutable et la plus petite fonction de production capables de lier exact assessment + matching scope + external disposition/detail, puis construire le breaker A0–H P1.7 avant toute implémentation.**

---

# SÉLECTION GOUVERNÉE — 18 SEPTEMBRE 2026 — P1.7 MINIMAL EXECUTABLE REVISION MODEL

**Selection ID:** `P1_7_MINIMAL_REVISION_DECISION_MODEL_V1`  
**Base observée avant sélection:** `560afe1180ccd9e80c30891409ea390ad03960c7`  
**Statut:** `SELECTED — TEST-FIRST, NOT IMPLEMENTED`  
**Portée:** plus petite surface exécutable AUDIT → REVISION compatible avec `P1_7_AUDIT_REVISION_BOUNDARY_V1`.

## 98. Décision de minimalité

Aucun objet `RevisionRequest` séparé n'est nécessaire en P1.7 V1.

La disposition et son détail restent des entrées explicites de la fonction de production.

La future surface minimale est donc équivalente à :

```text
CONTRACT = "P1_7_AUDIT_REVISION_BOUNDARY_V1"

RevisionDecision

produce_revision_decision(
    assessment,
    scope,
    disposition,
    detail,
)

is_factory_attested_revision_decision(value)
```

Le module candidat attendu est :

`src/revision.py`

Aucune autre API de mutation, exécution, promotion ou autorisation n'appartient à P1.7 V1.

## 99. Entrées exactes de la fonction

La fonction de production doit recevoir exactement quatre entrées obligatoires, sans fallback ni valeur par défaut :

1. `assessment` — exact `MemoryCollectionAuditAssessment` P1.6 encore factory-attested ;
2. `scope` — `AuditScope` content-bound correspondant ;
3. `disposition` — chaîne explicitement fournie de l'extérieur ;
4. `detail` — chaîne explicitement fournie de l'extérieur.

La signature ne doit pas accepter :

- `audit_id` à la place de l'assessment ;
- `scope_id` à la place du scope ;
- `verdict` comme raccourci de disposition ;
- `force`, `override`, `ignore_blocked`, `authorized` ou équivalent.

## 100. Validation minimale de l'assessment

P1.7 doit vérifier :

- type exact compatible `MemoryCollectionAuditAssessment` ;
- `is_factory_attested_memory_collection_audit(assessment) == True`.

Un assessment manuel, same-valued, copié, remplacé, sérialisé ou muté échoue fermé.

P1.7 ne doit pas appeler une fonction capable de reconstituer ou ré-attester l'assessment.

## 101. Validation minimale du scope

P1.7 ne dépend pas d'une fonction privée P1.6.

La validation du scope doit être reconstructible à partir de l'API publique P1.6 :

```text
canonical_scope = create_audit_scope(
    question=scope.question,
    expected_registration_ids=scope.expected_registration_ids,
    context_fields=scope.context_fields,
)
```

Puis P1.7 exige :

```text
canonical_scope == scope
scope.scope_id == assessment.scope_id
```

Conséquences :

- un scope manuel strictement same-valued reste admissible ;
- un scope stale/forgé est rejeté ;
- un scope étranger est rejeté ;
- P1.7 n'introduit pas une seconde autorité process-locale pour `AuditScope`.

## 102. Dispositions exactes

L'ensemble autorisé est exactement :

```text
KEEP_CURRENT_STATE
REQUEST_NEW_EVIDENCE
REQUEST_NEW_EXPERIMENT
REFORMULATE_QUESTION
```

Les comparaisons sont exactes et sensibles à la casse.

Aucun alias n'est admis.

Aucune disposition n'est dérivée depuis :

- `assessment.verdict` ;
- `assessment.completeness_status` ;
- `assessment.independence_status` ;
- les anomalies ;
- le nombre de membres ;
- les contradictions.

## 103. Detail minimal

`detail` doit être une chaîne dont `detail.strip()` n'est pas vide.

Le contenu exact fourni est conservé dans le `RevisionDecision` et participe à son identité.

P1.7 V1 n'interprète pas automatiquement le contenu du detail comme preuve, protocole expérimental, règle ou autorisation.

Pour `REFORMULATE_QUESTION`, une contrainte supplémentaire s'applique :

```text
detail.strip() != scope.question.strip()
```

Une différence composée uniquement d'espaces ne constitue pas une reformulation.

## 104. Modèle minimal `RevisionDecision`

Le modèle exécutable retenu est exactement :

```text
RevisionDecision
- revision_id
- audit_id
- scope_id
- disposition
- detail
- source_verdict
- source_completeness_status
- source_independence_status
```

Aucun champ supplémentaire n'est nécessaire pour le premier candidat.

Sont notamment exclus :

- `supported` ;
- `refuted` ;
- `knowledge` ;
- `confidence` ;
- `causal` ;
- `rule` ;
- `recommended_rule` ;
- `experiment_id` ;
- `evidence_id` ;
- `authorized` ;
- `known_from` ;
- `revision_at`.

## 105. Snapshot exact des statuts source

La production copie sans transformation :

```text
source_verdict = assessment.verdict
source_completeness_status = assessment.completeness_status
source_independence_status = assessment.independence_status
```

P1.7 ne possède aucune logique qui puisse transformer ces valeurs.

En particulier, `BLOCKED` reste `BLOCKED`.

## 106. Identité de contenu de la révision

`revision_id` est déterministe et content-bound à :

```text
contract
audit_id
scope_id
disposition
detail
source_verdict
source_completeness_status
source_independence_status
```

Préfixe candidat :

`REV-`

Deux productions avec exactement le même contenu peuvent avoir le même `revision_id` tout en étant des objets locaux distincts.

Modifier la disposition, le detail, l'audit ou le scope doit modifier l'identité.

`revision_id` n'est jamais une permission.

## 107. Attestation de la sortie

`RevisionDecision` suit le modèle process-local exact-object déjà qualifié en amont :

- production par la factory → attestation locale ;
- objet manuel same-valued → non attesté ;
- copy/deepcopy/replace → non attesté ;
- mutation post-production → attestation invalide ;
- deux productions same-valued peuvent être deux objets distincts tous deux attestés.

L'attestation P1.7 ne confère aucune autorité à l'assessment ou au scope en sens inverse.

## 108. Absence volontaire de matrice verdict → disposition

Le premier runtime doit permettre à chacune des quatre dispositions d'être explicitement proposée avec un audit `PASS`, `FAIL` ou `BLOCKED`, sous réserve des autres validations.

Ainsi, le runtime ne contient pas de table décisionnelle implicite.

Cette permissivité de **choix de disposition** n'est pas une permission opérationnelle : elle signifie seulement que P1.7 enregistre une orientation externe au lieu de l'inventer.

## 109. Sémantique non-promotrice

Le modèle doit rester descriptif et gouverné :

```text
KEEP_CURRENT_STATE
→ no governed mutation performed

REQUEST_NEW_EVIDENCE
→ evidence requested, not obtained

REQUEST_NEW_EXPERIMENT
→ experiment requested, not created/executed

REFORMULATE_QUESTION
→ alternative wording recorded, not validated
```

Aucun `RevisionDecision` ne peut constituer :

- preuve ;
- connaissance ;
- hypothèse validée ;
- correction de règle ;
- expérience ;
- autorisation d'action.

## 110. Breaker A0–H retenu avant runtime

Le breaker test-first doit au minimum couvrir :

### A — Assessment exact
- exact P1.6 assessment positif ;
- `audit_id` seul ;
- dict/JSON ;
- manuel same-valued ;
- copy/deepcopy/replace ;
- assessment muté ;
- absence d'assessment.

### B — Scope matching
- exact scope positif ;
- scope manuel same-valued positif ;
- scope absent ;
- scope étranger ;
- question + stale ID ;
- membership + stale ID ;
- context fields + stale ID ;
- `scope_id` seul.

### C — Disposition externe
- chacune des quatre dispositions ;
- None/vide ;
- casse différente ;
- alias ;
- disposition inconnue ;
- dispositions de mutation/autorisation rejetées ;
- signature exacte sans défauts/fallback ;
- même verdict source compatible avec plusieurs dispositions explicites.

### D — Detail
- non vide positif ;
- None/vide/whitespace ;
- reformulation identique ;
- reformulation whitespace-equivalente ;
- reformulation réellement différente positive ;
- detail conservé comme texte, sans preuve/expérience implicite.

### E — Préservation source
- `PASS` conservé ;
- `FAIL` conservé ;
- `BLOCKED` conservé ;
- completeness `BLOCKED` conservé ;
- independence `BLOCKED` conservé ;
- aucun paramètre d'override.

### F — Non-promotion sémantique
- KEEP ≠ validation ;
- evidence request ≠ evidence ;
- experiment request ≠ experiment ;
- reformulation ≠ hypothesis ;
- absence de knowledge/confidence/causality/rule/authorization.

### G — Identité / attestation
- production positive ;
- same inputs → même ID, objets distincts attestés ;
- manual/copy/deepcopy/replace non attestés ;
- mutation invalide ;
- changement disposition/detail → autre ID ;
- `revision_id` seul n'est pas autorité.

### H — Reverse authority / bypass
- ne répare pas assessment ;
- ne crée pas AuditScope ;
- ne mint pas MEMORY/AUDIT/ResearchFindings/ResearchRunEvidence ;
- aucun timestamp implicite ;
- aucune horloge locale ;
- aucune acquisition/backtest/order/live ;
- aucune surface de changement de comportement.

## 111. État après sélection

**MODÈLE MINIMAL P1.7 : SELECTED.**

**RUNTIME P1.7 : BLOCKED / NOT IMPLEMENTED.**

La prochaine mutation autorisée est limitée à :

- `breakers/p1_7_audit_revision_breaker.py` ;
- `.github/workflows/p1-7-audit-revision.yml`.

Aucun `src/revision.py` ne doit exister avant l'observation du FAIL pré-implémentation.

---

# FORMALISATION GOUVERNÉE — 18 SEPTEMBRE 2026 — P1.8 REVISION → FOLLOW-UP REQUEST

**Contract ID:** `P1_8_REVISION_FOLLOWUP_REQUEST_BOUNDARY_V1`  
**Base observée avant formalisation:** `87a01a8bd969941336fb485af20baab96a9ebde8`  
**Statut:** `FORMALIZED — QUALIFICATION-ONLY, NOT IMPLEMENTED`  
**Portée:** transformation contrôlée d'une décision de révision P1.7 en demande de suivi non exécutable ; aucune preuve, expérience, exécution ou permission n'est créée par P1.8.

## 112. État amont reconnu

Depuis les sections historiques P1.7 plus haut dans ce document, la frontière :

```text
P1.6 AUDIT
↓
P1.7 REVISION
```

a été implémentée et qualifiée dans son périmètre `qualification-only`.

P1.7 produit désormais un `RevisionDecision` factory-attested, content-bound et non exécutoire.

Les quatre dispositions P1.7 restent :

```text
KEEP_CURRENT_STATE
REQUEST_NEW_EVIDENCE
REQUEST_NEW_EXPERIMENT
REFORMULATE_QUESTION
```

P1.8 ne prolonge pas ces quatre branches de la même manière.

## 113. Question minimale de P1.8

P1.8 répond uniquement à :

> **Une RevisionDecision P1.7 exacte et attestée demande-t-elle explicitement un nouveau travail de preuve ou d'expérimentation, et peut-on enregistrer cette demande sans prétendre que la preuve existe déjà, que l'expérience est spécifiée/exécutée ou qu'une permission d'exécution a été accordée ?**

La frontière minimale est :

```text
exact factory-attested RevisionDecision
        ↓
routing strict sur disposition
        ↓
factory-attested FollowUpRequest
```

avec uniquement deux routes autorisées :

```text
REQUEST_NEW_EVIDENCE
→ FollowUpRequest(request_kind = EVIDENCE)

REQUEST_NEW_EXPERIMENT
→ FollowUpRequest(request_kind = EXPERIMENT)
```

Les deux autres dispositions s'arrêtent avant cette frontière.

## 114. Séparation centrale

P1.8 doit imposer :

```text
REQUEST ≠ FULFILLMENT
REQUEST ≠ EVIDENCE
REQUEST ≠ EXPERIMENT
REQUEST ≠ EXECUTION
REQUEST ≠ AUTHORIZATION
```

Et plus précisément :

```text
EVIDENCE REQUEST ≠ EVIDENCE OBTAINED
EXPERIMENT REQUEST ≠ EXPERIMENT SPECIFICATION
EXPERIMENT REQUEST ≠ EXPERIMENT EXECUTED
FOLLOW-UP REQUEST ≠ QUALIFIED RESEARCH INPUT
FOLLOW-UP REQUEST ≠ RESEARCH RUN EVIDENCE
FOLLOW-UP REQUEST ≠ PERMISSION
```

Cette séparation est l'objet principal de P1.8.

## 115. Dispositions routables

P1.8 V1 accepte exactement :

```text
REQUEST_NEW_EVIDENCE
REQUEST_NEW_EXPERIMENT
```

Le `request_kind` doit être dérivé mécaniquement :

```text
REQUEST_NEW_EVIDENCE
→ EVIDENCE

REQUEST_NEW_EXPERIMENT
→ EXPERIMENT
```

Le caller P1.8 ne choisit pas `request_kind`.

Aucun paramètre `request_kind`, `kind`, `mode`, `route` ou équivalent n'est nécessaire dans la future factory.

## 116. Dispositions terminales / non routables

### 116.1 KEEP_CURRENT_STATE

`KEEP_CURRENT_STATE` est terminal à P1.7 pour cette branche.

Il signifie :

> **aucun nouveau travail de preuve ou d'expérience n'est demandé par cette décision.**

P1.8 doit donc refuser explicitement :

`RevisionDecision(disposition = KEEP_CURRENT_STATE)`.

Il ne doit pas produire :

- `FollowUpRequest` vide ;
- `NOOP_REQUEST` ;
- `request_kind = NONE` ;
- `None` comme pseudo-succès silencieux.

Le refus explicite évite de confondre :

```text
valid terminal revision
```

avec :

```text
follow-up request successfully created
```

### 116.2 REFORMULATE_QUESTION

`REFORMULATE_QUESTION` ne traverse pas P1.8.

Cette disposition appartient à une future branche séparée conceptuellement de type :

```text
RevisionDecision(REFORMULATE_QUESTION)
↓
future candidate question/scope boundary
```

Elle ne doit pas être convertie automatiquement en demande de preuve ou d'expérience.

Ainsi :

```text
REFORMULATED WORDING ≠ EVIDENCE REQUEST
REFORMULATED WORDING ≠ EXPERIMENT REQUEST
```

## 117. Entrée minimale P1.8

P1.8 prend uniquement :

`RevisionDecision`

et rien d'autre.

La future fonction candidate doit être équivalente à :

```text
produce_follow_up_request(revision)
```

Cette minimalité est intentionnelle.

Ne doivent pas être fournis par le caller :

- `request_kind` ;
- `specification` ;
- `revision_id` séparé ;
- `audit_id` séparé ;
- `scope_id` séparé ;
- `authorized` ;
- `execute` ;
- `run` ;
- `force`.

P1.8 dérive tout ce qu'il doit conserver depuis l'objet P1.7 exact.

## 118. Exactitude de l'entrée P1.7

L'entrée doit être un `RevisionDecision` complet encore reconnu par :

`is_factory_attested_revision_decision(revision) == True`.

Ne constituent pas une entrée qualifiée :

- `revision_id` seul ;
- dict/JSON ;
- objet manuel same-valued ;
- copy/deepcopy/replace ;
- objet muté ;
- objet anciennement muté puis restauré après invalidation sticky ;
- objet structurellement plausible mais non attesté.

P1.8 consomme l'autorité P1.7 ; il ne peut pas la recréer ou la réparer.

## 119. Specification dérivée

La future sortie doit conserver :

```text
specification = revision.detail
```

exactement, sans normalisation sémantique.

Le caller ne fournit pas une nouvelle specification.

Cette règle empêche le rebinding suivant :

```text
RevisionDecision:
  disposition = REQUEST_NEW_EVIDENCE
  detail = "obtain missing source documents"

caller P1.8:
  request_kind = EXPERIMENT
  specification = "run backtest"
```

Ce contournement doit être impossible par contrat.

P1.8 n'interprète pas `specification` comme un protocole exécutable.

## 120. Modèle minimal `FollowUpRequest`

Le plus petit modèle conceptuel retenu est :

```text
FollowUpRequest
- request_id
- revision_id
- audit_id
- scope_id
- request_kind
- specification
- source_verdict
- source_completeness_status
- source_independence_status
```

Aucun champ d'exécution ou de fulfillment n'appartient à P1.8 V1.

Sont notamment interdits :

- `evidence_id` ;
- `finding_id` ;
- `research_run_id` ;
- `experiment_id` ;
- `dataset_id` ;
- `qualified_input` ;
- `execution_result` ;
- `evidence_obtained` ;
- `experiment_completed` ;
- `execution_allowed` ;
- `authorized` ;
- `supported` ;
- `confidence`.

## 121. Request kind

Les seules valeurs de `request_kind` sont :

```text
EVIDENCE
EXPERIMENT
```

Elles sont dérivées exclusivement de `revision.disposition`.

Il n'existe aucune valeur :

- `KEEP` ;
- `REFORMULATE` ;
- `EXECUTE` ;
- `BACKTEST` ;
- `LIVE` ;
- `AUTHORIZED`.

## 122. Snapshot exact de la provenance de révision

La sortie doit conserver exactement :

```text
revision_id = revision.revision_id
audit_id = revision.audit_id
scope_id = revision.scope_id

source_verdict = revision.source_verdict
source_completeness_status = revision.source_completeness_status
source_independence_status = revision.source_independence_status
```

Aucune valeur source n'est recalculée ou promue.

La demande doit rester reliée à la révision exacte qui l'a produite.

## 123. Préservation de BLOCKED

P1.8 doit préserver littéralement tout état `BLOCKED` reçu depuis P1.7.

Exemple :

```text
RevisionDecision:
  disposition = REQUEST_NEW_EVIDENCE
  source_verdict = BLOCKED
  source_completeness_status = BLOCKED
  source_independence_status = BLOCKED
```

devient :

```text
FollowUpRequest:
  request_kind = EVIDENCE
  source_verdict = BLOCKED
  source_completeness_status = BLOCKED
  source_independence_status = BLOCKED
```

La création d'une demande ne signifie jamais :

```text
BLOCKED → RESOLVED
BLOCKED → PASS
BLOCKED → SUPPORTED
BLOCKED → AUTHORIZED
```

Donc :

`REQUEST CREATED ≠ REQUEST SATISFIED`.

## 124. Identité de contenu

`request_id` doit être content-bound au minimum à :

```text
contract
revision_id
audit_id
scope_id
request_kind
specification
source_verdict
source_completeness_status
source_independence_status
```

Préfixe candidat possible :

`FUR-`

Deux productions identiques peuvent avoir le même `request_id` tout en étant deux objets locaux distincts attestés.

Modifier la révision, le kind dérivé, la specification ou un snapshot source doit modifier l'identité.

`request_id` n'est :

- ni une identité d'expérience ;
- ni une identité de preuve ;
- ni une permission ;
- ni une preuve d'exécution.

## 125. Attestation locale

Le futur `FollowUpRequest` doit être factory-attested exact-object.

La discipline P1.7 doit être réutilisée dès la première implémentation :

- objet produit par factory → attesté ;
- manuel same-valued → non attesté ;
- copy/deepcopy/replace → non attesté ;
- mutation observée → invalidation ;
- invalidation sticky ;
- restauration des anciennes valeurs après mismatch → attestation toujours invalide.

P1.8 ne doit pas redécouvrir une troisième fois cette classe de défaut.

## 126. Relation avec les APIs RESEARCH existantes

Les surfaces existantes :

```text
QualifiedResearchInput
run_qualified_research(...)
ResearchExecutionResult
ResearchRunEvidence
ResearchFindings
```

ne sont pas des objets P1.8.

Elles représentent respectivement :

- un input concret d'exécution ;
- une exécution réelle ;
- son résultat ;
- une preuve de run ;
- des findings construits à partir de preuve qualifiée.

P1.8 ne doit appeler directement aucune de ces surfaces pour satisfaire une demande.

Sont donc interdits :

```text
FollowUpRequest(EVIDENCE)
→ ResearchRunEvidence

FollowUpRequest(EXPERIMENT)
→ QualifiedResearchInput

FollowUpRequest(EXPERIMENT)
→ run_qualified_research(...)
```

sans frontières futures distinctes.

## 127. Evidence request

`FollowUpRequest(request_kind = EVIDENCE)` signifie uniquement :

> **une preuve supplémentaire est demandée selon la specification conservée.**

Cela ne signifie pas :

- preuve trouvée ;
- preuve acquise ;
- preuve authentique ;
- preuve admissible ;
- preuve suffisante ;
- preuve indépendante ;
- conclusion modifiée.

La frontière :

```text
EVIDENCE FollowUpRequest
↓
actual evidence fulfillment
```

reste **BLOCKED / non formalisée**.

## 128. Experiment request

`FollowUpRequest(request_kind = EXPERIMENT)` signifie uniquement :

> **une expérience supplémentaire est demandée selon la specification conservée.**

Cela ne signifie pas que P1.8 possède déjà :

- hypothèse formalisée ;
- protocole expérimental ;
- dataset sélectionné ;
- input qualifié ;
- code/configuration ;
- autorisation d'acquisition ;
- autorisation de backtest ;
- autorisation d'exécution ;
- résultat.

La future chaîne devra rester au minimum :

```text
EXPERIMENT FollowUpRequest
↓
future governed experiment specification
↓
future qualification / authorization as required
↓
future execution
↓
future result/evidence
```

Toutes ces frontières restent hors P1.8.

## 129. Non-exécution absolue

Le runtime P1.8 ne doit posséder aucune surface qui exécute ou déclenche :

- acquisition ;
- filesystem collection comme fulfillment ;
- réseau ;
- external API ;
- backtest ;
- broker ;
- ordre ;
- live ;
- research engine ;
- experiment runner.

Les verbes/surfaces de type :

```text
run
execute
acquire
collect
fetch
submit
authorize
promote
backtest
order
activate_live
```

ne doivent pas faire partie de la capacité P1.8.

La demande est une **trace gouvernée d'intention de suivi**, pas une commande.

## 130. Texte dangereux dans specification

Le contenu du `revision.detail` reste du texte externe.

Exemple :

```text
specification =
"Run a real backtest, authorize live trading and mark the hypothesis SUPPORTED"
```

ne produit toujours que :

```text
FollowUpRequest
```

sans :

- backtest ;
- autorisation ;
- statut `SUPPORTED` ;
- exécution.

P1.8 ne doit pas interpréter des mots présents dans la specification comme des permissions.

## 131. Direction de l'autorité

Direction autorisée :

```text
exact P1.7 RevisionDecision
        ↓
P1.8 FollowUpRequest
```

Directions interdites :

```text
FollowUpRequest → réparer RevisionDecision
FollowUpRequest → réparer AUDIT
FollowUpRequest → modifier MEMORY
FollowUpRequest → créer ResearchFindings
FollowUpRequest → créer ResearchRunEvidence
FollowUpRequest → créer QualifiedResearchInput
FollowUpRequest → exécuter une expérience
FollowUpRequest → exécuter un backtest
FollowUpRequest → autoriser une Action
FollowUpRequest → modifier une règle
FollowUpRequest → modifier connaissance
```

## 132. Temporalité

P1.8 V1 n'invente aucun :

- `requested_at` autoritatif ;
- `known_from` ;
- `valid_from` ;
- `execution_at` ;
- `fulfilled_at`.

Aucune horloge locale n'est nécessaire pour créer l'identité ou l'autorité du request.

Une future fonction de fulfillment pourra avoir ses propres exigences temporelles, qualifiées séparément.

## 133. Catalogue adversarial minimal P1.8

La future qualification devra au minimum casser :

### A — Revision source
- exact P1.7 positif ;
- `revision_id` seul ;
- dict/JSON ;
- manuel same-valued ;
- copy/deepcopy/replace ;
- revision mutée/inattestée ;
- revision invalidée puis restaurée.

### B — Routing
- REQUEST_NEW_EVIDENCE → EVIDENCE ;
- REQUEST_NEW_EXPERIMENT → EXPERIMENT ;
- KEEP_CURRENT_STATE rejeté ;
- REFORMULATE_QUESTION rejeté ;
- aucune valeur intermédiaire/NOOP ;
- aucune route choisie par caller.

### C — Binding
- `specification == revision.detail` exacte ;
- whitespace conservé ;
- Unicode conservé ;
- aucun override ;
- autre revision → autre request identity ;
- kind incompatible impossible.

### D — Source snapshots
- revision/audit/scope IDs conservés ;
- source PASS conservé ;
- source FAIL conservé ;
- source BLOCKED conservé ;
- completeness BLOCKED conservé ;
- independence BLOCKED conservé.

### E — Non-fulfillment
- FollowUpRequest ≠ ResearchRunEvidence ;
- FollowUpRequest ≠ ResearchFindings ;
- FollowUpRequest ≠ QualifiedResearchInput ;
- FollowUpRequest ≠ ResearchExecutionResult ;
- aucune preuve/expérience implicitement créée.

### F — Non-execution
- pas de `run_qualified_research` ;
- pas de `bind_execution_input` comme fulfillment ;
- pas d'acquisition ;
- pas de backtest ;
- pas de broker/live ;
- texte dangereux dans specification sans effet.

### G — Identity / attestation
- production positive ;
- même contenu → même ID, objets distincts attestés ;
- manual/copy/deepcopy/replace non attestés ;
- mutation invalide ;
- invalidation sticky ;
- changement de revision/detail/kind/source status change l'identité ;
- `request_id` seul n'est pas autorité.

### H — Reverse authority
- request ne répare pas revision ;
- request ne mint pas audit/memory/research evidence ;
- request ne devient pas permission ;
- aucune horloge locale ;
- aucune modification downstream silencieuse.

## 134. Qualification positive autorisée à P1.8

Un futur PASS P1.8 pourra signifier uniquement :

- une `RevisionDecision` P1.7 exacte et attestée a été reçue ;
- sa disposition est routable ;
- le `request_kind` a été dérivé correctement ;
- la specification est exactement le detail de la révision ;
- les IDs et statuts source ont été conservés ;
- les `BLOCKED` restent visibles ;
- la sortie est un `FollowUpRequest` factory-attested content-bound ;
- aucune preuve n'a été obtenue ;
- aucune expérience n'a été spécifiée ou exécutée ;
- aucune permission n'a été accordée.

Un PASS P1.8 ne signifiera pas :

- evidence obtained ;
- experiment designed ;
- experiment executed ;
- research run completed ;
- hypothesis supported/refuted ;
- knowledge validated ;
- rule changed ;
- authorization granted.

## 135. État après formalisation P1.8

**FORMALISATION P1.8 : PASS.**

La frontière exécutable reste :

**P1.7 REVISION → P1.8 FOLLOW-UP REQUEST : BLOCKED / NOT IMPLEMENTED.**

Les branches suivantes restent séparément bloquées :

```text
P1.8 EVIDENCE REQUEST → ACTUAL EVIDENCE
= BLOCKED / NOT FORMALIZED

P1.8 EXPERIMENT REQUEST → EXPERIMENT SPECIFICATION
= BLOCKED / NOT FORMALIZED

P1.8 EXPERIMENT REQUEST → EXECUTION
= BLOCKED

P1.8 REQUEST → AUTHORIZATION
= BLOCKED
```

Et les deux dispositions non routables restent :

```text
KEEP_CURRENT_STATE
→ STOP at P1.7 for this branch

REFORMULATE_QUESTION
→ future separate question/scope branch
```

## 136. Prochaine action gouvernée unique

**Déterminer, à partir des APIs P1.7 réelles et sans implémenter encore P1.8, le plus petit `FollowUpRequest` exécutable et la plus petite factory `produce_follow_up_request(revision)`, puis construire le breaker A0–H P1.8 avant toute implémentation.**

---

# SÉLECTION GOUVERNÉE — 18 SEPTEMBRE 2026 — P1.8 MINIMAL EXECUTABLE FOLLOW-UP REQUEST MODEL

**Selection ID:** `P1_8_MINIMAL_FOLLOWUP_REQUEST_MODEL_V1`  
**Base observée avant sélection:** `86a57b4acbbaecdf32a16e08e37d12da70fd0d4f`  
**Statut:** `SELECTED — TEST-FIRST, NOT IMPLEMENTED`  
**Portée:** plus petite surface exécutable REVISION → FOLLOW-UP REQUEST compatible avec `P1_8_REVISION_FOLLOWUP_REQUEST_BOUNDARY_V1`.

## 137. Surface minimale retenue

Le futur module candidat est limité à :

```text
CONTRACT = "P1_8_REVISION_FOLLOWUP_REQUEST_BOUNDARY_V1"

FollowUpRequest

produce_follow_up_request(revision)

is_factory_attested_follow_up_request(value)
```

Module candidat attendu :

`src/follow_up_request.py`

Aucune autre API de fulfillment, spécification expérimentale, exécution, collecte ou autorisation n'appartient à P1.8 V1.

## 138. Entrée unique

La factory prend exactement un argument obligatoire :

```text
produce_follow_up_request(revision)
```

Elle ne reçoit aucun :

- `request_kind` ;
- `specification` ;
- `audit_id` ;
- `scope_id` ;
- `revision_id` ;
- `force` ;
- `override` ;
- `execute` ;
- `authorized`.

Cette signature évite tout rebinding par le caller.

## 139. Validation de la RevisionDecision

La factory exige :

- type `RevisionDecision` ;
- `is_factory_attested_revision_decision(revision) == True`.

Sont rejetés :

- `revision_id` seul ;
- dict/JSON ;
- objet manuel same-valued ;
- copy/deepcopy/replace ;
- objet muté ;
- objet invalidé puis restauré après sticky invalidation.

P1.8 ne reconstitue, ne répare et ne re-atteste jamais la RevisionDecision.

## 140. Routing exact

Deux dispositions seulement sont routables :

```text
REQUEST_NEW_EVIDENCE   → EVIDENCE
REQUEST_NEW_EXPERIMENT → EXPERIMENT
```

Le mapping est exact et sensible à la casse.

Les deux dispositions suivantes sont explicitement rejetées :

```text
KEEP_CURRENT_STATE
REFORMULATE_QUESTION
```

Elles ne produisent ni `None`, ni request vide, ni `NOOP_REQUEST`.

## 141. Specification exacte

La sortie doit porter :

```text
specification = revision.detail
```

strictement.

Aucune normalisation n'est appliquée :

- whitespace conservé ;
- Unicode conservé ;
- retours ligne conservés ;
- mots tels que `AUTHORIZED`, `SUPPORTED`, `RUN_BACKTEST` restent du texte sans effet.

Le caller ne peut substituer une autre specification.

## 142. Modèle minimal FollowUpRequest

Le modèle exécutable retenu est exactement :

```text
FollowUpRequest
- request_id
- revision_id
- audit_id
- scope_id
- request_kind
- specification
- source_verdict
- source_completeness_status
- source_independence_status
```

Aucun champ supplémentaire n'est nécessaire pour P1.8 V1.

Sont notamment exclus :

- `evidence_id` ;
- `finding_id` ;
- `research_run_id` ;
- `experiment_id` ;
- `dataset_id` ;
- `qualified_input` ;
- `execution_result` ;
- `evidence_obtained` ;
- `experiment_completed` ;
- `execution_allowed` ;
- `authorized` ;
- `supported` ;
- `confidence` ;
- `requested_at`.

## 143. Snapshot exact de la source

La factory copie sans transformation :

```text
revision_id = revision.revision_id
audit_id = revision.audit_id
scope_id = revision.scope_id
source_verdict = revision.source_verdict
source_completeness_status = revision.source_completeness_status
source_independence_status = revision.source_independence_status
```

Aucun snapshot source ne peut être fourni ou corrigé par le caller.

## 144. Identité de contenu

`request_id` est déterministe et content-bound à :

```text
contract
revision_id
audit_id
scope_id
request_kind
specification
source_verdict
source_completeness_status
source_independence_status
```

Préfixe candidat :

`FUR-`

Deux productions same-valued peuvent avoir le même `request_id` tout en étant des objets locaux distincts.

Changer la RevisionDecision, sa disposition, son detail ou ses snapshots source doit changer l'identité de request lorsque le contenu P1.8 change.

`request_id` n'est ni preuve, ni expérience, ni permission.

## 145. Préservation de BLOCKED

Les valeurs source sont littéralement préservées.

En particulier :

```text
source_verdict = BLOCKED
→ request.source_verdict = BLOCKED

source_completeness_status = BLOCKED
→ request.source_completeness_status = BLOCKED

source_independence_status = BLOCKED
→ request.source_independence_status = BLOCKED
```

Créer un request ne résout aucun blocage.

## 146. Attestation locale et invalidation sticky

`FollowUpRequest` doit être factory-attested exact-object.

Dès le premier candidat :

- manual same-valued → non attesté ;
- copy/deepcopy/replace → non attesté ;
- mutation observée → invalidation ;
- mismatch de weakref → invalidation ;
- invalidation → retrait du registre ;
- restauration des anciennes valeurs → ne réactive jamais l'attestation.

Cette propriété est obligatoire dès P1.8 V1.

## 147. Non-fulfillment

Un FollowUpRequest n'est pas :

- `ResearchRunEvidence` ;
- `ResearchFindings` ;
- `QualifiedResearchInput` ;
- `ResearchExecutionResult` ;
- une hypothèse ;
- une mesure ;
- un résultat ;
- une preuve obtenue.

P1.8 n'a pas de factory ou adaptateur produisant ces objets.

## 148. Non-exécution

Le module P1.8 ne doit pas :

- importer/appeler `run_qualified_research` pour exécuter une demande ;
- appeler `bind_execution_input` comme fulfillment ;
- lire/acquérir un corpus ;
- lancer un backtest ;
- faire du réseau ;
- appeler un broker ;
- créer un ordre ;
- activer du live ;
- accorder une autorisation.

Le request est uniquement une trace gouvernée de travail futur demandé.

## 149. Direction d'autorité

Direction autorisée :

```text
exact P1.7 RevisionDecision
↓
P1.8 FollowUpRequest
```

Directions interdites :

```text
FollowUpRequest → RevisionDecision authority
FollowUpRequest → Audit authority
FollowUpRequest → HistoricalMemory authority
FollowUpRequest → ResearchRunEvidence
FollowUpRequest → QualifiedResearchInput
FollowUpRequest → experiment execution
FollowUpRequest → authorization
```

## 150. Breaker A0–H retenu avant runtime

Le breaker test-first doit au minimum couvrir :

### A — Revision source
- exact routable P1.7 revision positif ;
- `revision_id` seul ;
- dict/JSON ;
- manual same-valued ;
- copy/deepcopy/replace ;
- revision mutée ;
- revision invalidée puis restaurée.

### B — Routing
- REQUEST_NEW_EVIDENCE → EVIDENCE ;
- REQUEST_NEW_EXPERIMENT → EXPERIMENT ;
- KEEP_CURRENT_STATE rejeté ;
- REFORMULATE_QUESTION rejeté ;
- aucun `NOOP`/None ;
- factory à un seul argument sans défaut.

### C — Binding
- specification = detail exacte ;
- whitespace conservé ;
- Unicode conservé ;
- multiline conservé ;
- aucune API d'override ;
- autre revision → autre identité si contenu différent ;
- kind non fourni par caller.

### D — Source snapshots
- revision_id conservé ;
- audit_id conservé ;
- scope_id conservé ;
- PASS conservé ;
- FAIL conservé ;
- BLOCKED conservé ;
- completeness BLOCKED conservé ;
- independence BLOCKED conservé.

### E — Non-fulfillment
- request ≠ ResearchRunEvidence ;
- request ≠ ResearchFindings ;
- request ≠ QualifiedResearchInput ;
- request ≠ ResearchExecutionResult ;
- aucun champ de fulfillment/execution.

### F — Non-execution
- pas de run_qualified_research ;
- pas de bind_execution_input comme fulfillment ;
- pas de filesystem/network/backtest/broker/live ;
- texte dangereux dans specification sans effet ;
- pas de permission.

### G — Identity / attestation
- production positive ;
- mêmes inputs → même ID, objets distincts attestés ;
- manual/copy/deepcopy/replace non attestés ;
- mutation invalide ;
- sticky invalidation ;
- changement de revision/detail/kind/source snapshot change l'identité ;
- request_id seul n'est pas autorité.

### H — Reverse authority
- request ne répare pas revision ;
- request ne mint pas audit/memory/research evidence ;
- request ne peut être passé comme RevisionDecision ;
- aucune horloge locale ;
- aucune mutation silencieuse upstream/downstream.

## 151. État après sélection

**MODÈLE MINIMAL P1.8 : SELECTED.**

**RUNTIME P1.8 : BLOCKED / NOT IMPLEMENTED.**

La prochaine mutation autorisée est limitée à :

- `breakers/p1_8_revision_followup_request_breaker.py` ;
- `.github/workflows/p1-8-revision-followup-request.yml`.

Aucun `src/follow_up_request.py` ne doit exister avant l'observation du FAIL pré-implémentation.

---

# FORMALISATION GOUVERNÉE — 18 SEPTEMBRE 2026 — P1.9 FOLLOW-UP REQUEST BRANCHING

**Contracts:**
- `P1_9A_EVIDENCE_SUBMISSION_BOUNDARY_V1`
- `P1_9B_EXPERIMENT_SPECIFICATION_BOUNDARY_V1`

**Base observée avant formalisation:** `654a54b88c7bf4aec3ee54bd475a5cedda0dbf80`  
**Statut:** `FORMALIZED — QUALIFICATION-ONLY, NOT IMPLEMENTED`  
**Portée:** séparation stricte des branches `EVIDENCE` et `EXPERIMENT` issues de P1.8, sans promotion directe vers preuve admissible, fulfillment, input exécutable, exécution ou autorisation.

## 152. État amont reconnu

Depuis les sections historiques P1.8 plus haut dans ce document, la frontière :

```text
P1.7 REVISION
↓
P1.8 FOLLOW-UP REQUEST
```

a été implémentée et qualifiée dans son périmètre `qualification-only`.

P1.8 produit désormais un `FollowUpRequest` factory-attested, content-bound, non exécutable, avec exactement deux `request_kind` :

```text
EVIDENCE
EXPERIMENT
```

P1.9 ne doit pas recombiner ces deux branches en une seule sémantique générique.

## 153. Séparation obligatoire des branches

La chaîne devient :

```text
FollowUpRequest(EVIDENCE)
↓
P1.9A EvidenceSubmission
↓
future evidence qualification / fulfillment assessment
↓
future admissible evidence
```

et séparément :

```text
FollowUpRequest(EXPERIMENT)
↓
P1.9B ExperimentSpecification
↓
future execution-input binding
↓
future execution qualification / authorization
↓
future execution
↓
future result / evidence
```

Les deux branches sont mutuellement exclusives.

Il est interdit de définir une seule factory permissive du type :

```text
fulfill_follow_up_request(request, mode=...)
```

qui laisserait le caller choisir ou transformer la nature du request.

## 154. Invariant central P1.9

P1.9 doit préserver :

```text
EVIDENCE MATERIAL RECEIVED ≠ EVIDENCE ADMISSIBLE
EVIDENCE MATERIAL RECEIVED ≠ REQUEST FULFILLED
EVIDENCE MATERIAL RECEIVED ≠ EVIDENCE SUFFICIENT

EXPERIMENT SPECIFICATION ≠ QUALIFIED RESEARCH INPUT
EXPERIMENT SPECIFICATION ≠ EXECUTION
EXPERIMENT SPECIFICATION ≠ RESULT
EXPERIMENT SPECIFICATION ≠ AUTHORIZATION
```

Et, pour les deux branches :

```text
P1.9 OUTPUT ≠ ResearchRunEvidence
P1.9 OUTPUT ≠ ResearchFindings
P1.9 OUTPUT ≠ QualifiedResearchInput
P1.9 OUTPUT ≠ ResearchExecutionResult
P1.9 OUTPUT ≠ AUTHORIZATION
```

---

# P1.9A — EVIDENCE SUBMISSION

## 155. Question minimale P1.9A

P1.9A répond uniquement à :

> **Un matériau exact a-t-il été explicitement soumis pour répondre à un FollowUpRequest(EVIDENCE) exact et attesté, et peut-on enregistrer cette soumission de manière content-bound sans prétendre qu'elle satisfait la demande ni qu'elle constitue une preuve admissible ?**

La frontière minimale est :

```text
exact factory-attested FollowUpRequest(request_kind = EVIDENCE)
+
exact externally supplied evidence material
↓
factory-attested EvidenceSubmission
```

P1.9A enregistre une **soumission**, pas un verdict de fulfillment.

## 156. Pourquoi P1.9A n'est pas encore un fulfillment

`FollowUpRequest.specification` est actuellement du texte externe libre.

Il ne définit pas nécessairement de manière machine-checkable :

- combien de matériaux sont requis ;
- quelles sources sont recevables ;
- quelle période doit être couverte ;
- quel niveau d'indépendance est requis ;
- quels critères de suffisance doivent être satisfaits ;
- quelles contradictions sont admissibles ;
- quelles propriétés rendent la demande complète.

Par conséquent :

```text
MATERIAL RECEIVED
≠ REQUEST FULFILLED
```

et :

```text
NO MISSING ERROR OBSERVED
≠ PROOF OF SUFFICIENT EVIDENCE
```

La future frontière `EvidenceSubmission(s) → fulfillment/admissibility assessment` reste séparée et BLOCKED.

## 157. Entrée request P1.9A

P1.9A exige le `FollowUpRequest` complet et exact.

Conditions minimales :

- type exact `FollowUpRequest` ;
- `is_factory_attested_follow_up_request(request) == True` ;
- `request.request_kind == "EVIDENCE"`.

Doivent être rejetés :

- `request_id` seul ;
- dict/JSON ;
- manual same-valued ;
- copy/deepcopy/replace ;
- request muté ;
- request invalidé puis restauré ;
- `FollowUpRequest(EXPERIMENT)`.

P1.9A ne peut reconstituer ou réparer l'autorité P1.8.

## 158. Matériau exact

Le matériau de preuve doit être fourni extérieurement comme contenu exact.

Le contrat conceptuel minimal distingue :

```text
source_ref
media_type
content
```

où :

- `source_ref` identifie descriptivement l'origine déclarée du matériau ;
- `media_type` décrit son format déclaré ;
- `content` contient les octets exacts soumis.

Le futur runtime doit calculer lui-même l'identité de contenu à partir des octets.

Le caller ne doit pas pouvoir remplacer les octets par un hash non vérifié et obtenir le même niveau d'autorité.

Ainsi :

```text
content_sha256 = SHA256(content)
content_size = len(content)
```

sont dérivés, pas déclarés.

## 159. Factory conceptuelle P1.9A

La future surface minimale est équivalente à :

```text
submit_evidence(
    request,
    *,
    source_ref,
    media_type,
    content,
)
```

La factory ne reçoit aucun :

- `fulfilled` ;
- `admissible` ;
- `sufficient` ;
- `supported` ;
- `confidence` ;
- `evidence_id` externe ;
- `research_run_id` ;
- `authorized`.

Elle ne fait aucune acquisition réseau ou filesystem autonome.

## 160. Modèle conceptuel minimal EvidenceSubmission

Le modèle minimal retenu est :

```text
EvidenceSubmission
- submission_id
- request_id
- revision_id
- audit_id
- scope_id
- source_ref
- media_type
- content_sha256
- content_size
- source_verdict
- source_completeness_status
- source_independence_status
```

Le contenu brut n'est pas nécessairement conservé dans l'objet runtime minimal si l'identité de contenu et la soumission exacte sont établies au moment de la factory.

Cette décision de stockage est distincte de la sémantique d'autorité.

## 161. Sémantique exacte de EvidenceSubmission

`EvidenceSubmission` signifie uniquement :

> **Ces octets exacts, déclarés sous ce source_ref et ce media_type, ont été soumis pour ce FollowUpRequest(EVIDENCE).**

Cela ne signifie jamais :

- preuve authentique ;
- source fiable ;
- preuve indépendante ;
- preuve pertinente ;
- preuve suffisante ;
- preuve complète ;
- demande satisfaite ;
- hypothèse supportée/refutée ;
- connaissance validée.

## 162. Multiplicité des soumissions

Une même demande EVIDENCE peut recevoir plusieurs soumissions distinctes.

P1.9A ne transforme pas automatiquement plusieurs soumissions en collection exhaustive.

Ainsi :

```text
MANY SUBMISSIONS ≠ COMPLETE EVIDENCE SET
MANY SUBMISSIONS ≠ INDEPENDENT SOURCES
MANY SUBMISSIONS ≠ FULFILLMENT
```

La collection, la déduplication, la suffisance et l'admissibilité éventuelles appartiennent à une frontière future.

## 163. Identité de contenu P1.9A

`submission_id` doit être content-bound au minimum à :

```text
contract
request_id
revision_id
audit_id
scope_id
source_ref
media_type
content_sha256
content_size
source_verdict
source_completeness_status
source_independence_status
```

Préfixe candidat possible :

`EVS-`

`submission_id` n'est ni un `evidence_id` qualifié ni une preuve d'admissibilité.

## 164. Préservation des statuts source P1.9A

La sortie copie sans transformation :

```text
source_verdict
source_completeness_status
source_independence_status
```

depuis le request.

En particulier :

```text
BLOCKED
→ EvidenceSubmission
→ BLOCKED
```

La présence d'un nouveau matériau ne résout pas automatiquement une propriété BLOCKED.

## 165. Attestation P1.9A

Le futur `EvidenceSubmission` doit être factory-attested exact-object.

Dès le premier candidat :

- manual same-valued → non attesté ;
- copy/deepcopy/replace → non attesté ;
- mutation observée → invalidation ;
- invalidation sticky ;
- restauration des anciennes valeurs → attestation toujours invalide.

L'attestation prouve seulement la production par la factory P1.9A avec ce contenu, pas la qualité épistémique du matériau.

## 166. Non-fulfillment et non-promotion P1.9A

Le runtime P1.9A ne doit produire ni appeler directement :

- `ResearchRunEvidence` ;
- `ResearchFindings` ;
- `ResearchFinding` ;
- `QualifiedResearchInput` ;
- `ResearchExecutionResult` ;
- `run_qualified_research` ;
- `SUPPORTED` / `REFUTED` ;
- autorisation opérationnelle.

Les mots présents dans le contenu ou `source_ref` n'ont aucun pouvoir d'autorité.

---

# P1.9B — EXPERIMENT SPECIFICATION

## 167. Question minimale P1.9B

P1.9B répond uniquement à :

> **Un FollowUpRequest(EXPERIMENT) exact et attesté peut-il être transformé en une spécification expérimentale falsifiable et non exécutable, sans sélectionner implicitement dataset/corpus, sans créer QualifiedResearchInput et sans lancer l'expérience ?**

La frontière minimale est :

```text
exact factory-attested FollowUpRequest(request_kind = EXPERIMENT)
+
externally declared:
  hypothesis_statement
  prediction
  falsification_rule
  protocol
  measurement_plan
↓
factory-attested ExperimentSpecification
```

## 168. Entrée request P1.9B

P1.9B exige :

- type exact `FollowUpRequest` ;
- attestation P1.8 exacte ;
- `request.request_kind == "EXPERIMENT"`.

Doivent être rejetés :

- ID seul ;
- dict/JSON ;
- manual same-valued ;
- copy/deepcopy/replace ;
- request muté/inattesté ;
- request invalidé puis restauré ;
- `FollowUpRequest(EVIDENCE)`.

## 169. Design expérimental externe minimal

P1.9B reçoit exactement cinq éléments de design externes :

```text
hypothesis_statement
prediction
falsification_rule
protocol
measurement_plan
```

Tous doivent être explicites et non vides.

Leur rôle minimal est :

- `hypothesis_statement` — proposition testée ;
- `prediction` — observation attendue si la proposition tient dans le cadre spécifié ;
- `falsification_rule` — condition observable capable de contredire la proposition ;
- `protocol` — conditions, procédure et contrôles envisagés ;
- `measurement_plan` — mesures/observations prévues et leur usage de test.

P1.9B ne décide pas automatiquement ces cinq éléments à partir du texte libre du request.

Ils sont déclarés extérieurement puis liés au request.

## 170. Objectif dérivé du request

La future sortie conserve :

```text
objective = request.specification
```

exactement.

Le caller ne fournit pas un autre objectif pouvant remplacer silencieusement la demande originale.

Ainsi le design expérimental reste traçable à la demande P1.8 qui l'a motivé.

## 171. Factory conceptuelle P1.9B

La future surface minimale est équivalente à :

```text
specify_experiment(
    request,
    *,
    hypothesis_statement,
    prediction,
    falsification_rule,
    protocol,
    measurement_plan,
)
```

Elle ne reçoit aucun :

- `corpus_root` ;
- `contract_path` ;
- `dataset_id` ;
- `dataset_version` ;
- `expected_corpus_hash` ;
- `expected_contract_hash` ;
- `QualifiedResearchInput` ;
- `execute` ;
- `authorized` ;
- `broker` ;
- `backtest` ;
- `live`.

## 172. Modèle conceptuel minimal ExperimentSpecification

Le modèle minimal retenu est :

```text
ExperimentSpecification
- experiment_spec_id
- request_id
- revision_id
- audit_id
- scope_id
- objective
- hypothesis_statement
- prediction
- falsification_rule
- protocol
- measurement_plan
- source_verdict
- source_completeness_status
- source_independence_status
```

Le champ est volontairement :

`experiment_spec_id`

et non `experiment_id`.

Une spécification ne prouve pas qu'une expérience a été créée ou exécutée.

## 173. Compatibilité conceptuelle avec ResearchHypothesis

Le dépôt possède déjà, en aval, une structure :

```text
ResearchHypothesis
- hypothesis_id
- statement
- prediction
- falsification_rule
```

P1.9B ne doit pas dépendre directement de cette classe post-exécution.

Cependant, les champs :

```text
hypothesis_statement
prediction
falsification_rule
```

sont volontairement compatibles conceptuellement afin de préserver une future traçabilité entre :

```text
pre-execution experiment specification
↓
future execution
↓
future ResearchFindings
```

sans inverser les dépendances de couche.

## 174. Ce que protocol ne signifie pas

Le champ `protocol` est déclaratif.

Il peut décrire :

- population ou corpus souhaité ;
- conditions de contrôle ;
- séquence prévue ;
- comparaisons ;
- contraintes ;
- conditions de répétition.

Mais P1.9B ne convertit pas ce texte en :

- `BoundResearchInput` ;
- `QualifiedResearchInput` ;
- dataset qualifié ;
- chemin filesystem ;
- corpus hash ;
- contrat hash ;
- commande d'exécution.

Donc :

```text
PROTOCOL TEXT ≠ EXECUTION INPUT
```

## 175. Ce que measurement_plan ne signifie pas

`measurement_plan` définit ce qui devra être observé ou mesuré.

Il ne crée aucune :

- `ResearchMeasurement` ;
- valeur observée ;
- sample size réel ;
- métrique réalisée ;
- finding.

Ainsi :

```text
MEASUREMENT PLAN ≠ MEASUREMENT
```

## 176. Identité de contenu P1.9B

`experiment_spec_id` doit être content-bound au minimum à :

```text
contract
request_id
revision_id
audit_id
scope_id
objective
hypothesis_statement
prediction
falsification_rule
protocol
measurement_plan
source_verdict
source_completeness_status
source_independence_status
```

Préfixe candidat possible :

`EXS-`

Changer un élément matériel du design doit changer l'identité.

## 177. Préservation des statuts source P1.9B

Comme toutes les frontières précédentes :

```text
source_verdict
source_completeness_status
source_independence_status
```

sont conservés exactement.

Ainsi :

```text
BLOCKED
→ ExperimentSpecification
→ BLOCKED
```

Une meilleure spécification ne répare pas automatiquement un manque de preuve ou d'indépendance amont.

## 178. Attestation P1.9B

Le futur `ExperimentSpecification` doit être factory-attested exact-object avec invalidation sticky.

L'attestation signifie seulement :

> **Cette spécification exacte a été produite par la factory qualifiée P1.9B à partir de ce request exact et de ce design externe.**

Elle ne signifie pas :

- expérience correcte ;
- expérience suffisante ;
- expérience autorisée ;
- dataset disponible ;
- exécution possible ;
- hypothèse plausible ;
- résultat favorable.

## 179. Non-exécution P1.9B

P1.9B ne doit ni appeler ni produire directement :

- `bind_execution_input` ;
- `QualifiedResearchInput` ;
- `run_qualified_research` ;
- `ResearchExecutionResult` ;
- `ResearchRunEvidence` ;
- `ResearchFindings`.

Il ne doit faire :

- aucune lecture de corpus ;
- aucune acquisition réseau ;
- aucun backtest ;
- aucun broker call ;
- aucun ordre ;
- aucune activation live.

## 180. Interdiction d'autorisation P1.9B

Même une specification contenant :

```text
"execute immediately"
"AUTHORIZED"
"run the real backtest"
"send live orders"
```

reste du texte déclaratif.

Elle ne donne aucune permission.

Donc :

```text
EXPERIMENT SPECIFICATION ≠ EXECUTION AUTHORIZATION
```

---

# RÈGLES COMMUNES P1.9A / P1.9B

## 181. Rejet croisé obligatoire

P1.9A doit refuser :

`FollowUpRequest(request_kind = EXPERIMENT)`.

P1.9B doit refuser :

`FollowUpRequest(request_kind = EVIDENCE)`.

Aucun paramètre caller-side ne peut modifier ce routing.

La règle est :

```text
request_kind is upstream authority for branch selection
```

dans le périmètre P1.9 uniquement.

## 182. Pas de promotion entre branches

Sont interdits :

```text
EvidenceSubmission → ExperimentSpecification
ExperimentSpecification → EvidenceSubmission
```

comme promotion implicite.

Un matériau soumis peut éventuellement devenir input ou preuve d'une expérience future seulement après une frontière explicitement qualifiée.

Une spécification expérimentale peut éventuellement produire des résultats futurs seulement après des frontières d'input, d'autorisation et d'exécution distinctes.

## 183. Direction de l'autorité

Directions autorisées :

```text
exact FollowUpRequest(EVIDENCE)
+ exact external material
↓
EvidenceSubmission
```

```text
exact FollowUpRequest(EXPERIMENT)
+ external experimental design
↓
ExperimentSpecification
```

Directions interdites :

```text
EvidenceSubmission → repair FollowUpRequest
ExperimentSpecification → repair FollowUpRequest

EvidenceSubmission → ResearchRunEvidence
ExperimentSpecification → QualifiedResearchInput

EvidenceSubmission → fulfillment PASS
ExperimentSpecification → execution

either P1.9 output → authorization
either P1.9 output → rule/knowledge mutation
```

## 184. Temporalité

P1.9 V1 n'invente aucune horloge autoritative.

Sont exclus des modèles minimaux :

- `submitted_at` autoritatif ;
- `specified_at` autoritatif ;
- `known_from` ;
- `valid_from` ;
- `executed_at`.

Si une future frontière requiert une temporalité normative, elle devra être qualifiée séparément.

## 185. Catalogues adversariaux futurs

### P1.9A — familles minimales
- exact EVIDENCE request positif ;
- EXPERIMENT request rejeté ;
- request ID seul/manual/copy/mutation rejetés ;
- bytes exacts → hash et size dérivés ;
- source_ref/media_type vides rejetés ;
- contenu vide : décision à fixer dans sélection minimale, pas implicitement accepté ;
- hash caller-side non accepté comme substitut des octets ;
- même contenu/métadonnées → identité déterministe ;
- contenu différent → identité différente ;
- multiple submissions ≠ fulfillment ;
- BLOCKED conservé ;
- aucun ResearchRunEvidence/Findings ;
- aucune IO/acquisition autonome ;
- attestation exact-object + sticky invalidation ;
- GC/snapshot upstream ;
- reverse authority.

### P1.9B — familles minimales
- exact EXPERIMENT request positif ;
- EVIDENCE request rejeté ;
- request ID seul/manual/copy/mutation rejetés ;
- cinq champs design obligatoires non vides ;
- objective exactement dérivé du request ;
- aucun override d'objectif/request kind ;
- protocole/measurement plan restent texte déclaratif ;
- aucune conversion en QualifiedResearchInput ;
- aucun run_qualified_research ;
- BLOCKED conservé ;
- identité déterministe ;
- changement d'un champ design → identité différente ;
- attestation exact-object + sticky invalidation ;
- GC/snapshot upstream ;
- reverse authority ;
- aucun broker/backtest/live/authorization.

## 186. Qualification positive autorisée P1.9A

Un futur PASS P1.9A pourra signifier uniquement :

- un exact `FollowUpRequest(EVIDENCE)` attesté a été reçu ;
- un matériau exact a été fourni ;
- son hash et sa taille ont été dérivés ;
- la soumission a été liée au request exact ;
- les statuts source ont été conservés ;
- la sortie est une `EvidenceSubmission` factory-attested content-bound.

Il ne signifiera pas :

- request fulfilled ;
- evidence admissible ;
- source trustworthy ;
- evidence sufficient ;
- hypothesis supported/refuted ;
- knowledge validated.

## 187. Qualification positive autorisée P1.9B

Un futur PASS P1.9B pourra signifier uniquement :

- un exact `FollowUpRequest(EXPERIMENT)` attesté a été reçu ;
- un design expérimental externe explicite a été fourni ;
- objective reste lié à la demande ;
- hypothèse, prediction, falsification rule, protocol et measurement plan sont présents ;
- les statuts source sont conservés ;
- la sortie est une `ExperimentSpecification` factory-attested content-bound.

Il ne signifiera pas :

- input exécutable prêt ;
- dataset qualifié ;
- expérience autorisée ;
- expérience exécutée ;
- résultat disponible ;
- hypothèse supportée/refutée.

## 188. État après formalisation P1.9

**FORMALISATION P1.9A : PASS.**

**FORMALISATION P1.9B : PASS.**

Les frontières exécutables restent :

```text
P1.8 EVIDENCE FollowUpRequest
→ P1.9A EvidenceSubmission
= BLOCKED / NOT IMPLEMENTED
```

```text
P1.8 EXPERIMENT FollowUpRequest
→ P1.9B ExperimentSpecification
= BLOCKED / NOT IMPLEMENTED
```

Les frontières suivantes restent séparément bloquées :

```text
EvidenceSubmission(s)
→ fulfillment/admissibility assessment
= BLOCKED / NOT FORMALIZED

ExperimentSpecification
→ QualifiedResearchInput / execution-input binding
= BLOCKED / NOT FORMALIZED

ExperimentSpecification
→ execution
= BLOCKED

either branch
→ authorization
= BLOCKED
```

## 189. Prochaine action gouvernée unique

**Déterminer, à partir des APIs P1.8 réelles et sans implémenter encore P1.9, les deux plus petits modèles exécutables `EvidenceSubmission` et `ExperimentSpecification`, fixer les signatures minimales de leurs factories, résoudre explicitement les derniers détails de représentation nécessaires (notamment contenu vide P1.9A et type exact des cinq champs P1.9B), puis construire les breakers test-first P1.9A et P1.9B avant toute implémentation runtime.**

---

# SÉLECTION GOUVERNÉE — 18 SEPTEMBRE 2026 — P1.9 MINIMAL EXECUTABLE MODELS

**Selection IDs:**
- `P1_9A_MINIMAL_EVIDENCE_SUBMISSION_MODEL_V1`
- `P1_9B_MINIMAL_EXPERIMENT_SPECIFICATION_MODEL_V1`

**Base observée avant sélection:** `c1ba6315849490bca19f9dfa1f613ed7eece253d`  
**Statut:** `SELECTED — TEST-FIRST, NOT IMPLEMENTED`

## 190. P1.9A — surface minimale exécutable

Le futur module candidat P1.9A est limité à :

```text
CONTRACT = "P1_9A_EVIDENCE_SUBMISSION_BOUNDARY_V1"

EvidenceSubmission

submit_evidence(
    request,
    *,
    source_ref,
    media_type,
    content,
)

is_factory_attested_evidence_submission(value)
```

Module candidat attendu :

`src/evidence_submission.py`

Aucune API de fulfillment, d'admissibilité ou de promotion épistémique n'appartient à P1.9A V1.

## 191. P1.9A — signature exacte

La signature minimale est exactement :

```text
submit_evidence(
    request,
    *,
    source_ref,
    media_type,
    content,
)
```

Les trois paramètres après `request` sont keyword-only, obligatoires et sans défaut.

Aucun paramètre caller-side n'est admis pour :

- `submission_id` ;
- `content_sha256` ;
- `content_size` ;
- `fulfilled` ;
- `admissible` ;
- `sufficient` ;
- `supported` ;
- `confidence` ;
- `authorized`.

## 192. P1.9A — types exacts

P1.9A V1 choisit les types d'entrée suivants :

```text
request    : exact FollowUpRequest
source_ref : exact str
media_type : exact str
content    : exact bytes
```

Le futur runtime doit rejeter les substituts permissifs :

- `bytearray` ;
- `memoryview` ;
- `str` à la place des bytes ;
- objets bytes-like arbitraires ;
- sous-types custom destinés à modifier le comportement de comparaison/sérialisation.

Le choix `bytes` rend le matériau fourni immutable et hashable de manière déterministe au moment de la factory.

## 193. P1.9A — contraintes source_ref et media_type

`source_ref` et `media_type` doivent être :

- exact `str` ;
- non vides après `.strip()`.

Ils sont conservés verbatim dans la sortie et dans son identité.

P1.9A V1 n'impose pas de syntaxe URI à `source_ref` et n'impose pas de grammaire MIME à `media_type`.

Cette absence de normalisation est intentionnelle : ces champs sont des déclarations descriptives, pas des attestations de source ou de format.

Ainsi :

```text
source_ref declaration ≠ source authenticity
media_type declaration ≠ parser qualification
```

## 194. P1.9A — décision sur contenu vide

`content=b""` est **accepté** lorsqu'il est fourni explicitement.

Raison :

P1.9A enregistre une soumission exacte ; il ne décide pas si cette soumission est utile, admissible ou suffisante.

Donc :

```text
explicit zero-byte submission
→ valid EvidenceSubmission
→ content_size = 0
→ SHA256(empty bytes)
```

mais :

```text
zero-byte submission ≠ sufficient evidence
zero-byte submission ≠ fulfillment
```

En revanche :

- `content=None` est rejeté ;
- absence de l'argument `content` est rejetée par signature ;
- tout type autre que exact `bytes` est rejeté.

Cette séparation empêche P1.9A d'introduire prématurément un jugement épistémique.

## 195. P1.9A — dérivations obligatoires

Le caller fournit les octets exacts.

Le runtime dérive :

```text
content_sha256 = sha256(content).hexdigest()
content_size = len(content)
```

Le caller ne fournitit ni hash ni taille.

Le runtime ne lit aucun fichier, aucune URL et aucune ressource externe pour recalculer le contenu.

## 196. P1.9A — modèle exact retenu

```text
EvidenceSubmission
- submission_id
- request_id
- revision_id
- audit_id
- scope_id
- source_ref
- media_type
- content_sha256
- content_size
- source_verdict
- source_completeness_status
- source_independence_status
```

Types de sortie minimaux :

```text
all identity/status/reference fields : str
content_sha256                      : str
content_size                        : int >= 0
```

Le contenu brut n'est pas stocké dans l'objet minimal P1.9A.

Une future frontière qui doit inspecter les octets devra les recevoir/retrouver séparément et les rebinder à `content_sha256`; P1.9A n'invente pas ce mécanisme aujourd'hui.

## 197. P1.9A — identité

`submission_id` est content-bound à :

```text
contract
request_id
revision_id
audit_id
scope_id
source_ref
media_type
content_sha256
content_size
source_verdict
source_completeness_status
source_independence_status
```

Préfixe retenu :

`EVS-`

Même contenu exact + mêmes métadonnées + même request → même identité de contenu.

Changer les bytes, source_ref, media_type ou request doit changer l'identité si le payload P1.9A change.

## 198. P1.9A — attestation

`EvidenceSubmission` utilise une attestation exact-object process-locale avec sticky invalidation dès V1.

Manual/copy/deepcopy/replace ne sont pas attestés.

Mutation observée invalide définitivement l'objet, même après restauration de ses anciennes valeurs.

## 199. P1.9A — breaker minimal retenu

Le breaker test-first P1.9A doit couvrir au minimum :

### A — Request source
- exact EVIDENCE request positif ;
- EXPERIMENT request rejeté ;
- request_id seul/dict/manual/copy/replace rejetés ;
- mutation et sticky-invalidated request rejetées.

### B — Signature/types
- signature exacte avec request positional + trois keyword-only ;
- source_ref/media_type exact str ;
- content exact bytes ;
- None/bytearray/memoryview/str rejetés ;
- aucun hash/taille caller-side.

### C — Empty/exact content
- b"" accepté ;
- taille 0 ;
- SHA-256 vide exact ;
- contenu non vide hashé exactement ;
- bytes différents → hash/ID différents.

### D — Metadata binding
- source_ref/media_type non vides après strip ;
- valeurs conservées verbatim ;
- aucune normalisation Unicode/whitespace ;
- changement metadata → autre identity.

### E — Source snapshots/BLOCKED
- request/revision/audit/scope IDs conservés ;
- PASS/FAIL/BLOCKED conservés ;
- completeness/independence BLOCKED conservés.

### F — Non-fulfillment
- aucun champ fulfilled/admissible/sufficient/supported/confidence ;
- EvidenceSubmission ≠ ResearchRunEvidence/ResearchFindings ;
- multiple submissions ne deviennent pas fulfillment.

### G — Identity/attestation
- output exact fields ;
- same content → same ID, distinct attested objects ;
- manual/copy/replace non attestés ;
- sticky invalidation ;
- rebinding ID rejeté ;
- GC/snapshot upstream.

### H — No IO/reverse authority
- pas de filesystem/network acquisition ;
- pas de run_qualified_research ;
- pas d'autorisation ;
- request non réparé ;
- submission ne peut remplacer FollowUpRequest.

---

## 200. P1.9B — surface minimale exécutable

Le futur module candidat P1.9B est limité à :

```text
CONTRACT = "P1_9B_EXPERIMENT_SPECIFICATION_BOUNDARY_V1"

ExperimentSpecification

specify_experiment(
    request,
    *,
    hypothesis_statement,
    prediction,
    falsification_rule,
    protocol,
    measurement_plan,
)

is_factory_attested_experiment_specification(value)
```

Module candidat attendu :

`src/experiment_specification.py`

Aucune API d'input binding, exécution, mesure réalisée, finding ou autorisation n'appartient à P1.9B V1.

## 201. P1.9B — signature exacte

La signature minimale est exactement :

```text
specify_experiment(
    request,
    *,
    hypothesis_statement,
    prediction,
    falsification_rule,
    protocol,
    measurement_plan,
)
```

Les cinq champs de design sont keyword-only, obligatoires et sans défaut.

Aucun paramètre caller-side n'est admis pour :

- `objective` ;
- `experiment_spec_id` ;
- `request_kind` ;
- dataset/corpus/paths/hashes ;
- `execute` ;
- `authorized` ;
- `backtest` ;
- `live`.

## 202. P1.9B — types exacts des cinq champs

P1.9B V1 choisit :

```text
hypothesis_statement : exact str
prediction           : exact str
falsification_rule   : exact str
protocol             : exact str
measurement_plan     : exact str
```

Chaque champ doit être non vide après `.strip()`.

Le runtime conserve chaque valeur verbatim.

Il ne normalise pas :

- whitespace ;
- Unicode ;
- casse ;
- ponctuation ;
- format markdown/texte.

Cette règle donne une identité de contenu exacte sans prétendre comprendre ou valider sémantiquement le design.

## 203. P1.9B — contrainte de falsifiabilité minimale

P1.9B V1 ne tente pas de prouver automatiquement qu'une hypothèse est scientifiquement bonne.

La contrainte minimale exécutable est seulement :

```text
hypothesis_statement.strip() != ""
prediction.strip() != ""
falsification_rule.strip() != ""
protocol.strip() != ""
measurement_plan.strip() != ""
```

La présence d'un `falsification_rule` non vide empêche au moins l'absence totale de condition de réfutation.

Mais :

```text
non-empty falsification_rule ≠ actually falsifiable hypothesis
```

Une qualification sémantique plus forte serait une frontière future.

## 204. P1.9B — objectif

`objective` est dérivé exclusivement :

```text
objective = request.specification
```

exactement.

Le caller ne peut le modifier.

P1.9B ne réinterprète pas le texte de l'objectif pour choisir dataset, protocole, exécution ou permission.

## 205. P1.9B — modèle exact retenu

```text
ExperimentSpecification
- experiment_spec_id
- request_id
- revision_id
- audit_id
- scope_id
- objective
- hypothesis_statement
- prediction
- falsification_rule
- protocol
- measurement_plan
- source_verdict
- source_completeness_status
- source_independence_status
```

Tous les champs sont des `str`.

Aucun :

- `experiment_id` ;
- dataset id/version ;
- corpus/path/hash ;
- execution id/result ;
- measurement value ;
- finding ;
- authorization field.

## 206. P1.9B — identité

`experiment_spec_id` est content-bound à :

```text
contract
request_id
revision_id
audit_id
scope_id
objective
hypothesis_statement
prediction
falsification_rule
protocol
measurement_plan
source_verdict
source_completeness_status
source_independence_status
```

Préfixe retenu :

`EXS-`

Chaque modification d'un des cinq champs ou du request doit changer l'identité si le payload P1.9B change.

## 207. P1.9B — attestation

`ExperimentSpecification` utilise l'attestation exact-object process-locale et sticky invalidation dès V1.

Manual/copy/deepcopy/replace ne sont pas attestés.

Mutation observée invalide définitivement l'objet.

## 208. P1.9B — compatibilité sans dépendance inverse

P1.9B ne dépend pas de `ResearchHypothesis` dans `research_findings.py`.

Il conserve seulement une compatibilité conceptuelle :

```text
hypothesis_statement ↔ future ResearchHypothesis.statement
prediction           ↔ future ResearchHypothesis.prediction
falsification_rule   ↔ future ResearchHypothesis.falsification_rule
```

Aucune conversion automatique n'est qualifiée par P1.9B.

## 209. P1.9B — breaker minimal retenu

Le breaker test-first P1.9B doit couvrir au minimum :

### A — Request source
- exact EXPERIMENT request positif ;
- EVIDENCE request rejeté ;
- ID/dict/manual/copy/replace/mutated/sticky-invalidated rejetés.

### B — Signature
- exactement request + cinq keyword-only obligatoires ;
- aucun objective/dataset/hash/execute/authorization caller-side.

### C — Types/emptiness
- chaque champ exact str ;
- None/non-str rejetés ;
- vide/whitespace-only rejetés ;
- valeurs conservées verbatim ;
- Unicode/multiline conservés.

### D — Binding/objective
- objective == request.specification exact ;
- caller ne peut override ;
- autre request → autre identity si payload change ;
- request_kind reste EXPERIMENT.

### E — Source snapshots/BLOCKED
- request/revision/audit/scope IDs conservés ;
- PASS/FAIL/BLOCKED conservés ;
- completeness/independence BLOCKED conservés.

### F — Non-execution
- ≠ QualifiedResearchInput/ResearchExecutionResult/ResearchRunEvidence/ResearchFindings ;
- aucun corpus/path/hash dataset ;
- pas de bind_execution_input ;
- pas de run_qualified_research ;
- protocol dangereux reste texte.

### G — Identity/attestation
- exact output fields ;
- mêmes inputs → même ID, objets distincts attestés ;
- changement de chacun des cinq champs → autre ID ;
- manual/copy/replace non attestés ;
- sticky invalidation ;
- GC/snapshot upstream.

### H — Reverse authority
- specification ne répare pas request ;
- ne devient pas EvidenceSubmission ;
- ne crée pas mesure/finding ;
- aucune horloge locale ;
- aucune autorisation/backtest/broker/live.

## 210. État après sélection

**P1.9A MINIMAL MODEL : SELECTED.**

**P1.9B MINIMAL MODEL : SELECTED.**

**RUNTIME P1.9A : BLOCKED / NOT IMPLEMENTED.**

**RUNTIME P1.9B : BLOCKED / NOT IMPLEMENTED.**

La prochaine mutation autorisée est limitée à :

- `breakers/p1_9a_evidence_submission_breaker.py` ;
- `.github/workflows/p1-9a-evidence-submission.yml` ;
- `breakers/p1_9b_experiment_specification_breaker.py` ;
- `.github/workflows/p1-9b-experiment-specification.yml`.

Aucun `src/evidence_submission.py` et aucun `src/experiment_specification.py` ne doivent exister avant observation des FAIL pré-implémentation.


# P1.9 — POST-IMPLEMENTATION RE-BREAK CHECKPOINT

Runtime candidates now exist at the persisted branch state:

- `src/evidence_submission.py`
- `src/experiment_specification.py`

The original P1.9A/P1.9B breakers remain unchanged. Qualification is **PENDING persisted-HEAD re-break**; this checkpoint grants no PASS, no execution authority, and no operational authorization.


---

# FORMALISATION GOUVERNÉE — 18 SEPTEMBRE 2026 — P1.10 POST-P1.9 BINDING PREREQUISITES

**Contracts candidats :**
- `P1_10A_EVIDENCE_MATERIAL_BINDING_BOUNDARY_V1`
- `P1_10B_EXPERIMENT_EXECUTION_BINDING_BOUNDARY_V1`

**Base qualifiée reconnue :** `c9d0ece7906841858db064eb66c5eb154ef5221b`  
**Statut :** `FORMALIZED — DIRECT DOWNSTREAM CANDIDATES BROKEN — NO RUNTIME`  
**Portée :** préserver la provenance exacte immédiatement après P1.9 sans déclarer fulfillment, admissibilité, suffisance, input exécutable, exécution ou autorisation.

## 211. État amont reconnu

Au HEAD `c9d0ece7906841858db064eb66c5eb154ef5221b` :

- P1.9A est qualifié PASS par le run `35371569841`, job `105686535725`, avec `54 passed`;
- P1.9B est qualifié PASS par le run `35371569886`, job `105686536533`, avec `73 passed`;
- les suites protégées RESEARCH→DECISION et P1.2→P1.8 rejouées dans ces jobs sont vertes;
- le worktree final est propre;
- P1.1 `AUTHORIZED` reste séparément BLOCKED.

P1.10 ne modifie ni les runtimes ni les breakers P1.9.

## 212. Candidat direct P1.10A cassé

La frontière historiquement envisagée était :

```text
EvidenceSubmission(s)
→ fulfillment/admissibility assessment
```

Ce raccord direct est **FAIL conceptuellement** pour V1.

`EvidenceSubmission` conserve :

- l'identité de soumission;
- la provenance de request;
- `source_ref`;
- `media_type`;
- `content_sha256`;
- `content_size`;

mais ne conserve pas les octets bruts.

Par conséquent, un assessment downstream qui ne recevrait que `EvidenceSubmission` ne peut pas démontrer :

- que les octets inspectés sont ceux de la soumission;
- que le contenu est parseable;
- que le matériau est pertinent;
- que la source est authentique;
- que la preuve est admissible;
- que la demande est satisfaite ou suffisante.

De plus, `FollowUpRequest.specification` reste du texte libre et ne fournit pas encore des critères machine-checkables de fulfillment.

Donc :

```text
EvidenceSubmission metadata/hash
≠ bound evidence bytes
≠ admissibility
≠ fulfillment
```

La plus petite frontière nécessaire avant tout assessment sémantique est un **rebinding exact du contenu**.

## 213. Candidat direct P1.10B cassé

La frontière historiquement envisagée était :

```text
ExperimentSpecification
→ QualifiedResearchInput / execution-input binding
```

Le raccord direct vers l'actuel `QualifiedResearchInput` est **FAIL conceptuellement**.

Raisons :

1. `ExperimentSpecification` ne contient aucun corpus, path, dataset ou hash d'entrée.
2. `QualifiedResearchInput` ne contient aucun `experiment_spec_id`.
3. `ResearchExecutionResult` ne contient aucun `experiment_spec_id`.
4. l'actuel `ResearchRunEvidence` ne contient aucun `experiment_spec_id`.
5. Produire directement un `QualifiedResearchInput` ferait donc disparaître la provenance de la spécification avant l'exécution.
6. Un caller pourrait choisir un corpus valide sans qu'un objet qualifié ne conserve explicitement la liaison entre ce corpus et la spécification P1.9B.

Donc :

```text
valid QualifiedResearchInput
≠ input bound to this ExperimentSpecification
```

et :

```text
execution from valid input
≠ execution of the requested/specifed experiment
```

P1.10B doit préserver cette liaison avant toute exécution.

## 214. Décision P1.10

Deux frontières sœurs sont retenues.

### P1.10A

```text
exact factory-attested EvidenceSubmission
+
exact bytes re-supplied by caller
↓
factory-attested BoundEvidenceMaterial
```

P1.10A vérifie uniquement :

```text
sha256(content) == submission.content_sha256
len(content) == submission.content_size
```

et conserve les octets exacts.

Il ne qualifie ni authenticité, ni pertinence, ni admissibilité, ni suffisance, ni fulfillment.

### P1.10B

```text
exact factory-attested ExperimentSpecification
+
exact factory-bound and source-revalidated BoundResearchInput
↓
factory-attested ExperimentExecutionBinding
```

P1.10B lie une spécification exacte à une identité de ressources déjà validée par la surface P0.4 existante.

Il ne produit pas encore `QualifiedResearchInput`, ne lance pas `run_qualified_research`, et ne prétend pas que l'expérience est exécutable ou autorisée.

## 215. Séparations obligatoires

```text
BOUND EVIDENCE MATERIAL ≠ ADMISSIBLE EVIDENCE
BOUND EVIDENCE MATERIAL ≠ FULFILLMENT
BOUND EVIDENCE MATERIAL ≠ ResearchRunEvidence

EXPERIMENT EXECUTION BINDING ≠ QualifiedResearchInput
EXPERIMENT EXECUTION BINDING ≠ EXECUTION
EXPERIMENT EXECUTION BINDING ≠ RESULT
EXPERIMENT EXECUTION BINDING ≠ AUTHORIZATION
```

Et pour les deux branches :

```text
BINDING ≠ KNOWLEDGE
BINDING ≠ BEHAVIOR CHANGE
BINDING ≠ OPERATIONAL AUTHORITY
```

## 216. Direction d'autorité

Directions autorisées :

```text
P1.9A EvidenceSubmission + exact matching bytes
→ P1.10A BoundEvidenceMaterial
```

```text
P1.9B ExperimentSpecification + exact BoundResearchInput
→ P1.10B ExperimentExecutionBinding
```

Directions interdites :

```text
BoundEvidenceMaterial → admissibility/fulfillment PASS
BoundEvidenceMaterial → ResearchRunEvidence

ExperimentExecutionBinding → run_qualified_research
ExperimentExecutionBinding → ResearchExecutionResult
ExperimentExecutionBinding → ResearchRunEvidence

either binding → AUTHORIZED
either binding → repair P1.9 object
```

## 217. Statut après formalisation

**FORMALISATION P1.10A : PASS.**

**FORMALISATION P1.10B : PASS.**

Les candidats directs :

```text
EvidenceSubmission → admissibility/fulfillment
ExperimentSpecification → QualifiedResearchInput
```

sont rejetés pour perte de preuve/provenance.

Les frontières exécutables P1.10A/P1.10B restent :

**BLOCKED / NOT IMPLEMENTED.**

La prochaine action gouvernée est de sélectionner les modèles exécutables minimaux exacts de `BoundEvidenceMaterial` et `ExperimentExecutionBinding`, puis de construire leurs breakers test-first avant tout runtime.


---

# SÉLECTION GOUVERNÉE — 18 SEPTEMBRE 2026 — P1.10 MINIMAL BINDING MODELS

**Selection IDs :**
- `P1_10A_MINIMAL_BOUND_EVIDENCE_MATERIAL_MODEL_V1`
- `P1_10B_MINIMAL_EXPERIMENT_EXECUTION_BINDING_MODEL_V1`

**Base observée avant sélection :** `651d74e5a99a911fe1a8d8cc1b04c0081b9cc85e`  
**Statut :** `SELECTED — TEST-FIRST, NOT IMPLEMENTED`.

## 218. P1.10A — surface minimale

Module candidat futur :

`src/evidence_material_binding.py`

Surface exacte :

```text
CONTRACT = "P1_10A_EVIDENCE_MATERIAL_BINDING_BOUNDARY_V1"

BoundEvidenceMaterial

bind_evidence_material(
    submission,
    *,
    content,
)

is_factory_attested_bound_evidence_material(value)
```

Entrées :

- `submission` : exact `EvidenceSubmission` P1.9A encore factory-attested;
- `content` : exact `bytes`, keyword-only, obligatoire.

Aucun `source_ref`, `media_type`, hash, size, verdict, fulfillment ou admissibility override n'est accepté.

## 219. P1.10A — validation exacte

Le runtime devra vérifier :

```text
sha256(content).hexdigest() == submission.content_sha256
len(content) == submission.content_size
```

Un mismatch de hash **ou** de taille échoue fermé.

`content=b""` reste valide uniquement si la soumission amont représente exactement le contenu vide.

Les types permissifs `str`, `bytearray`, `memoryview` et sous-classe custom de `bytes` sont rejetés.

## 220. P1.10A — modèle exact

```text
BoundEvidenceMaterial
- evidence_binding_id
- submission_id
- request_id
- revision_id
- audit_id
- scope_id
- source_ref
- media_type
- content_sha256
- content_size
- content
- source_verdict
- source_completeness_status
- source_independence_status
```

`content` est conservé comme exact `bytes` afin que la prochaine frontière d'inspection n'ait pas à deviner ou reconstruire le matériau.

Préfixe d'identité :

`EBM-`

L'identité est content-bound à la provenance de soumission et à l'identité exacte du contenu.

## 221. P1.10A — sémantique

`BoundEvidenceMaterial` signifie uniquement :

> les octets présents dans cet objet sont exactement les octets identifiés par cette EvidenceSubmission P1.9A.

Il ne signifie pas :

- source authentique;
- contenu vrai;
- preuve pertinente;
- preuve admissible;
- preuve suffisante;
- demande satisfaite;
- ResearchRunEvidence;
- connaissance.

## 222. P1.10A — attestation

Exact-object process-local avec sticky invalidation dès V1 :

- factory → attesté;
- manual/copy/deepcopy/replace → non attesté;
- mutation observée → retrait du registre;
- restauration ultérieure → non ré-attestée.

La sortie est autonome par snapshot : la collecte de l'objet `EvidenceSubmission` amont ne doit pas invalider un binding déjà produit.

## 223. P1.10A — breaker A0–H minimal

### A — submission authority
- exact P1.9A positif;
- submission ID seul/dict/manual/copy/deepcopy/replace rejetés;
- submission mutée/sticky-invalidated rejetée;
- objet P1.9B rejeté.

### B — signature/type
- signature exacte `submission, *, content`;
- exact bytes uniquement;
- aucun metadata/hash/status override.

### C — content rebinding
- hash exact positif;
- size exact positif;
- zéro-octet positif si amont zéro-octet;
- bytes différents rejetés;
- mismatch size/hash rejeté;
- Unicode/string jamais converti implicitement.

### D — snapshot
- IDs, source_ref, media_type, hash, size et statuts copiés exactement;
- content exact conservé;
- BLOCKED reste BLOCKED.

### E — non-admissibility
- aucun `admissible`, `fulfilled`, `sufficient`, `supported`, `confidence`;
- ≠ ResearchRunEvidence / ResearchFindings.

### F — identity
- exact fields;
- mêmes inputs → même ID, objets distincts attestés;
- autre content valide → autre ID;
- manual/copy/replace non attestés;
- sticky invalidation.

### G — lifetime
- upstream submission peut être collectée;
- binding reste attesté;
- `evidence_binding_id` seul n'est pas autorité.

### H — reverse authority
- binding ne répare pas submission;
- binding ne crée pas evidence qualifiée;
- aucune acquisition réseau/filesystem autonome;
- aucune exécution/backtest/broker/live/authorization.

## 224. P1.10B — surface minimale

Module candidat futur :

`src/experiment_execution_binding.py`

Surface exacte :

```text
CONTRACT = "P1_10B_EXPERIMENT_EXECUTION_BINDING_BOUNDARY_V1"

ExperimentExecutionBinding

bind_experiment_execution(
    specification,
    bound_input,
)

is_factory_attested_experiment_execution_binding(value)
```

Entrées :

- `specification` : exact `ExperimentSpecification` P1.9B encore factory-attested;
- `bound_input` : exact `BoundResearchInput` produit par `bind_execution_input` et encore valide avec revalidation des sources.

P1.10B réutilise la surface P0.4 existante. Il ne crée pas une seconde logique de hash/corpus/contract.

## 225. P1.10B — rejet de QualifiedResearchInput direct

`QualifiedResearchInput` n'est pas une entrée P1.10B valide.

Raison : sa validité d'exécution ne prouve pas son association à cette spécification P1.9B.

Le seul objet de ressource accepté à P1.10B est le `BoundResearchInput` factory-bound existant.

## 226. P1.10B — modèle exact

```text
ExperimentExecutionBinding
- execution_binding_id
- experiment_spec_id
- request_id
- revision_id
- audit_id
- scope_id
- objective
- hypothesis_statement
- prediction
- falsification_rule
- protocol
- measurement_plan
- corpus_root
- contract_path
- expected_corpus_hash
- expected_contract_hash
- source_verdict
- source_completeness_status
- source_independence_status
```

`corpus_root` et `contract_path` sont des chaînes absolues dérivées de `Path.resolve()` du `BoundResearchInput`.

Les deux hashes sont copiés exactement depuis le bound input revalidé.

Préfixe d'identité :

`EEB-`

L'identité est content-bound au design expérimental exact et à l'identité de ressources validée.

## 227. P1.10B — sémantique

`ExperimentExecutionBinding` signifie uniquement :

> cette spécification expérimentale exacte a été associée à cette identité exacte de corpus/contrat actuellement revalidée.

Il ne signifie pas :

- QualifiedResearchInput produit;
- corpus scientifiquement approprié;
- protocole effectivement implémenté par le runtime;
- expérience exécutable;
- expérience autorisée;
- expérience exécutée;
- résultat;
- ResearchRunEvidence.

La conformité sémantique entre le texte libre `protocol/measurement_plan` et les ressources liées reste future et BLOCKED.

## 228. P1.10B — revalidation

Au moment du binding :

```text
is_bound_research_input(bound_input, revalidate_sources=True) == True
```

est obligatoire.

Ainsi :

- source supprimée;
- contract modifié;
- corpus modifié;
- objet bound_input muté;
- objet reconstruit/copié;

doivent échouer.

P1.10B peut relire les ressources pour cette revalidation d'identité; il ne les acquiert pas et ne les exécute pas.

## 229. P1.10B — attestation

Exact-object process-local + sticky invalidation dès V1.

La sortie est un snapshot autonome : l'objet `ExperimentSpecification` ou `BoundResearchInput` amont peut être collecté après production sans invalider le binding.

Cette autonomie n'autorise pas l'exécution; une future frontière devra revalider les ressources avant de dériver/consommer un input exécutable.

## 230. P1.10B — breaker A0–H minimal

### A — specification authority
- exact P1.9B positif;
- ID/dict/manual/copy/deepcopy/replace rejetés;
- spec mutée/sticky-invalidated rejetée;
- EvidenceSubmission rejetée.

### B — bound input authority
- exact factory-bound positif;
- `QualifiedResearchInput` rejeté;
- manual/copy/deepcopy/replace `BoundResearchInput` rejetés;
- bound input muté rejeté;
- source contract/corpus modifiée après binding rejetée.

### C — signature/binding
- signature exacte deux arguments sans overrides;
- aucune sélection implicite de corpus;
- paths absolus dérivés;
- hashes exacts conservés.

### D — spec snapshot
- experiment_spec_id et provenance amont conservés;
- objective + cinq champs design conservés verbatim;
- BLOCKED reste BLOCKED.

### E — non-execution
- ≠ QualifiedResearchInput;
- ≠ ResearchExecutionResult;
- ≠ ResearchRunEvidence;
- aucun `run_qualified_research`;
- aucune création de `QualifiedResearchInput`.

### F — semantic restraint
- valid resource binding ≠ protocole implémenté;
- texte `AUTHORIZED/RUN_BACKTEST/SEND_LIVE_ORDER` reste texte;
- aucun knowledge/finding/measurement/result.

### G — identity/attestation
- exact fields;
- mêmes inputs → même ID, objets distincts attestés;
- changement de spec ou de ressources validées → autre ID;
- manual/copy/replace non attestés;
- sticky invalidation;
- lifetime upstream indépendant après snapshot.

### H — reverse authority
- binding ne répare ni spec ni bound input;
- ne mint pas ResearchRunEvidence;
- ne lance aucune acquisition/backtest/order/live;
- ne donne aucune autorisation.

## 231. État après sélection

**P1.10A MINIMAL MODEL : SELECTED.**

**P1.10B MINIMAL MODEL : SELECTED.**

**RUNTIME P1.10A : BLOCKED / NOT IMPLEMENTED.**

**RUNTIME P1.10B : BLOCKED / NOT IMPLEMENTED.**

Prochaine mutation autorisée :

- ajouter le breaker test-first P1.10A;
- ajouter le workflow pré-implémentation P1.10A;
- ajouter le breaker test-first P1.10B;
- ajouter le workflow pré-implémentation P1.10B.

Aucun `src/evidence_material_binding.py` ni `src/experiment_execution_binding.py` ne doit exister avant observation des FAIL pré-implémentation.


---

# P1.10 — POST-IMPLEMENTATION RE-BREAK CHECKPOINT

Runtime candidates now exist at the persisted branch state:

- `src/evidence_material_binding.py`
- `src/experiment_execution_binding.py`

The original P1.10A/P1.10B breakers remain unchanged.

Qualification is **PENDING persisted-HEAD re-break**.

This checkpoint grants no evidence admissibility, no fulfillment, no QualifiedResearchInput, no execution, no result, no ResearchRunEvidence, and no operational authorization.


---

# P1.10 — QUALIFICATION CANDIDATE PERSISTED FOR FINAL RE-BREAK

**Candidate qualification base:** `cd8f0a739b66c7f9446c54d4426b8a61096b6dd7`

Observed post-implementation runs:

- P1.10A run `35374287883`, job `105695240879`: upstream protected chain PASS, P1.9A+B combined `127 passed`, P1.10A `28 passed`, clean worktree PASS.
- P1.10B run `35374287915`, job `105695203627`: upstream protected chain PASS, P1.9A+B combined `127 passed`, P1.10B `28 passed`, clean worktree PASS.

Candidate verdicts:

```text
P1.10A_EVIDENCE_MATERIAL_BINDING_BOUNDARY_V1
→ PASS CANDIDATE

P1.10B_EXPERIMENT_EXECUTION_BINDING_BOUNDARY_V1
→ PASS CANDIDATE
```

These are not final until both workflows re-break this persisted qualification state itself.

The qualification remains strictly limited:

```text
BoundEvidenceMaterial
≠ admissible evidence
≠ fulfillment
≠ sufficient evidence

ExperimentExecutionBinding
≠ QualifiedResearchInput
≠ execution
≠ result
≠ ResearchRunEvidence
≠ authorization
```


---

# FORMALISATION GOUVERNÉE — 18 SEPTEMBRE 2026 — P1.11 POST-P1.10 PREREQUISITES

**Contracts candidats :**
- `P1_11A_EVIDENCE_ASSESSMENT_CRITERIA_BOUNDARY_V1`
- `P1_11B_QUALIFIED_EXPERIMENT_EXECUTION_INPUT_BOUNDARY_V1`

**Base qualifiée reconnue :** `dbe090e038843c3ace7d6d0f3147a1803865b4b8`  
**Statut :** `FORMALIZED — DIRECT DOWNSTREAM CANDIDATES BROKEN — NO RUNTIME`.

## 232. État amont reconnu

Au HEAD qualifié `dbe090e038843c3ace7d6d0f3147a1803865b4b8` :

- P1.10A `BoundEvidenceMaterial` prouve seulement que des octets exacts correspondent à une `EvidenceSubmission` P1.9A exacte;
- P1.10B `ExperimentExecutionBinding` lie une `ExperimentSpecification` P1.9B exacte à une identité de corpus/contrat P0.4 revalidée;
- aucune de ces frontières ne produit admissibilité, fulfillment, `QualifiedResearchInput`, exécution, résultat, `ResearchRunEvidence` ou autorisation.

P1.11 ne modifie aucune frontière P1.9/P1.10.

## 233. P1.11A — raccord direct cassé

Le raccord naïf suivant est rejeté :

```text
BoundEvidenceMaterial(s)
→ admissible / fulfilled
```

**Verdict conceptuel : FAIL.**

Raison : les matériaux liés exposent des faits observables — provenance de soumission, source_ref déclaré, media_type déclaré, hash, taille et octets — mais aucune règle qualifiée ne dit encore :

- combien de matériaux sont requis;
- si le contenu vide est acceptable pour cette demande;
- quels media types sont acceptables;
- quelles sources déclarées sont acceptables;
- quelles propriétés sémantiques doivent être démontrées;
- quelles conditions rendent la collection complète;
- quelles conditions rendent une source authentique, pertinente ou indépendante.

`FollowUpRequest.specification` reste du texte libre. Le runtime ne peut donc pas l'inventer en règles machine-checkables.

Ainsi :

```text
EXACT BYTES ≠ ADMISSIBILITY
EXACT BYTES ≠ SUFFICIENCY
EXACT BYTES ≠ REQUEST FULFILLMENT
```

La frontière minimale nécessaire avant tout assessment est une **déclaration de critères explicite**.

## 234. P1.11A — question minimale

P1.11A répond uniquement à :

> Peut-on enregistrer un ensemble explicite de critères d'évaluation pour un `FollowUpRequest(EVIDENCE)` exact, sans les dériver du matériau observé et sans prétendre que ces critères sont eux-mêmes complets, vrais ou déjà satisfaits ?

Direction autorisée :

```text
exact factory-attested FollowUpRequest(EVIDENCE)
+
external criteria declaration
↓
EvidenceAssessmentCriteria
```

P1.11A ne consomme encore aucun `BoundEvidenceMaterial`.

Cette séparation empêche un assessment d'inventer silencieusement ses propres critères à partir des éléments qu'il est censé juger.

## 235. P1.11A — portée des critères

La V1 distingue :

### Critères structurels machine-checkables
- nombre minimal de matériaux distincts;
- exigence ou non de contenu non vide;
- liste optionnelle de `media_type` déclarés autorisés;
- liste optionnelle de `source_ref` déclarés autorisés.

### Exigences sémantiques non évaluées
Une liste de textes externes peut enregistrer des exigences telles que :

- authenticité;
- pertinence;
- indépendance;
- période couverte;
- qualité documentaire;
- corroboration.

P1.11A **enregistre** ces exigences mais ne les évalue pas.

Leur présence doit rester visible downstream.

## 236. P1.11A — limite de complétude

P1.11A ne possède aucune preuve que la déclaration de critères capture exhaustivement toute la sémantique de `request.specification`.

Donc la sortie doit conserver explicitement :

```text
criteria_completeness_status = BLOCKED
```

en V1.

Aucun paramètre caller-side ne peut transformer ce statut en PASS.

Ainsi, même une future collection satisfaisant tous les critères structurels déclarés ne pourra pas être appelée « fulfillment complet du request » tant qu'une frontière distincte n'aura pas qualifié la complétude des critères ou fourni une autorité équivalente.

## 237. P1.11B — raccord direct cassé

Le raccord naïf suivant est rejeté :

```text
ExperimentExecutionBinding
→ existing QualifiedResearchInput
→ existing ResearchExecutionResult
→ existing ResearchRunEvidence
```

**Verdict conceptuel : FAIL.**

Les trois types existants `QualifiedResearchInput`, `ResearchExecutionResult` et `ResearchRunEvidence` ne transportent ni :

- `execution_binding_id`;
- `experiment_spec_id`.

Une simple projection vers `QualifiedResearchInput` ferait donc disparaître l'identité expérimentale avant l'exécution.

Ainsi :

```text
valid existing execution result
≠ result proven to belong to this ExperimentSpecification
```

## 238. P1.11B — question minimale

P1.11B répond uniquement à :

> Peut-on produire un input d'exécution expérimental exact qui conserve la provenance complète P1.9B/P1.10B et revalide les ressources, sans exécuter encore l'expérience ?

Direction autorisée :

```text
exact factory-attested ExperimentExecutionBinding
+
source identity revalidation
↓
QualifiedExperimentExecutionInput
```

Ce nouvel objet devient la seule entrée admissible d'une future fonction d'exécution expérimentale liée.

## 239. P1.11B — séparation d'avec l'exécution

`QualifiedExperimentExecutionInput` n'est pas l'actuel `QualifiedResearchInput`.

Il contient suffisamment d'information pour qu'une future frontière puisse :

1. reconstruire/projeter l'entrée technique existante;
2. appeler l'exécution existante;
3. envelopper le résultat avec `execution_binding_id` et `experiment_spec_id`;
4. propager ensuite cette provenance jusqu'à une future evidence de run expérimental.

Mais P1.11B V1 ne fait aucune de ces quatre opérations d'exécution.

Donc :

```text
QUALIFIED EXPERIMENT EXECUTION INPUT
≠ EXECUTION
≠ RESULT
≠ ResearchRunEvidence
≠ AUTHORIZATION
```

## 240. Revalidation des ressources P1.11B

P1.10B est un snapshot. Entre sa création et P1.11B, les ressources peuvent changer.

P1.11B doit donc revalider l'identité courante des ressources en réutilisant la capacité P0.4 existante sur :

- `corpus_root`;
- `contract_path`;
- `expected_corpus_hash`;
- `expected_contract_hash`.

Une source supprimée ou modifiée doit échouer fermée.

Cette revalidation est une vérification d'identité, pas une exécution de recherche.

## 241. Direction d'autorité commune

Directions interdites :

```text
P1.11A criteria → admissible evidence
P1.11A criteria → fulfillment PASS
P1.11A criteria → knowledge

P1.11B input → execution result
P1.11B input → ResearchRunEvidence
P1.11B input → authorization
P1.11B input → broker/backtest/live
```

## 242. État après formalisation

**FORMALISATION P1.11A : PASS.**

**FORMALISATION P1.11B : PASS.**

Les raccords directs :

```text
BoundEvidenceMaterial(s) → admissibility / fulfillment
ExperimentExecutionBinding → existing QualifiedResearchInput → execution
```

sont rejetés.

Les frontières exécutables P1.11A/P1.11B restent :

**BLOCKED / NOT IMPLEMENTED.**

La prochaine action gouvernée est de sélectionner les deux modèles exécutables minimaux et leurs breakers test-first avant tout runtime.


---

# SÉLECTION GOUVERNÉE — 18 SEPTEMBRE 2026 — P1.11 MINIMAL EXECUTABLE MODELS

**Selection IDs :**
- `P1_11A_MINIMAL_EVIDENCE_ASSESSMENT_CRITERIA_MODEL_V1`
- `P1_11B_MINIMAL_QUALIFIED_EXPERIMENT_EXECUTION_INPUT_MODEL_V1`

**Base observée avant sélection :** `b8ca9e9832ebf2695e43d3cffe2316cc1f9b498c`  
**Statut :** `SELECTED — TEST-FIRST, NOT IMPLEMENTED`.

## 243. P1.11A — surface minimale

Module candidat futur :

`src/evidence_assessment_criteria.py`

Surface exacte :

```text
CONTRACT = "P1_11A_EVIDENCE_ASSESSMENT_CRITERIA_BOUNDARY_V1"

EvidenceAssessmentCriteria

declare_evidence_assessment_criteria(
    request,
    *,
    minimum_distinct_materials,
    require_nonempty_content,
    allowed_media_types,
    allowed_source_refs,
    semantic_requirements,
)

is_factory_attested_evidence_assessment_criteria(value)
```

P1.11A ne prend aucun matériau P1.10A en entrée.

## 244. P1.11A — types et contraintes

Entrées exactes :

```text
request                     : exact FollowUpRequest(EVIDENCE)
minimum_distinct_materials  : exact int >= 1, bool rejeté
require_nonempty_content    : exact bool
allowed_media_types         : None | exact tuple[str, ...]
allowed_source_refs         : None | exact tuple[str, ...]
semantic_requirements       : exact tuple[str, ...]
```

Pour les tuples de chaînes :

- chaque élément est exact `str`;
- chaque élément doit être non vide après `.strip()`;
- les doublons exacts sont rejetés;
- les valeurs sont conservées verbatim;
- `None` signifie « aucune restriction structurée déclarée »;
- un tuple vide pour `allowed_media_types` ou `allowed_source_refs` est rejeté afin de ne pas confondre « aucune restriction » avec « aucun élément possible »;
- `semantic_requirements=()` est valide et signifie qu'aucune exigence sémantique supplémentaire n'est enregistrée dans cet objet.

## 245. P1.11A — modèle exact

```text
EvidenceAssessmentCriteria
- criteria_id
- request_id
- revision_id
- audit_id
- scope_id
- specification
- minimum_distinct_materials
- require_nonempty_content
- allowed_media_types
- allowed_source_refs
- semantic_requirements
- criteria_completeness_status
- source_verdict
- source_completeness_status
- source_independence_status
```

`criteria_completeness_status` vaut obligatoirement :

`BLOCKED`

en V1.

Aucun paramètre caller-side ne peut le fournir ou le modifier.

## 246. P1.11A — identité et attestation

Préfixe :

`EAC-`

`criteria_id` est content-bound à :

- contract;
- provenance exacte du request;
- specification;
- cinq dimensions de critères;
- `criteria_completeness_status = BLOCKED`;
- statuts source.

Exact-object attestation + sticky invalidation dès V1.

Manual/copy/deepcopy/replace ne sont pas attestés.

## 247. P1.11A — non-assessment

Le module P1.11A ne doit exposer aucune factory :

- `assess_evidence`;
- `mark_admissible`;
- `mark_fulfilled`;
- `promote_evidence`;
- `create_research_run_evidence`.

La présence de critères ne prouve pas qu'ils sont satisfaits.

## 248. P1.11A — breaker A0–H

### A — request authority
- exact EVIDENCE request positif;
- EXPERIMENT request rejeté;
- ID/dict/manual/copy/deepcopy/replace/mutated/sticky-invalidated rejetés.

### B — signature
- request + cinq keyword-only obligatoires sans défaut;
- aucun champ de verdict/admissibility/fulfillment caller-side.

### C — scalar types
- minimum exact int >=1;
- bool/float/str/0/négatif rejetés;
- require_nonempty_content exact bool.

### D — tuple criteria
- None positif pour allowed lists;
- tuple non vide positif;
- liste/set/string rejetés;
- élément non-str/vide rejeté;
- doublons rejetés;
- valeurs verbatim.

### E — semantic requirements
- tuple vide positif;
- tuple non vide positif;
- types/vides/doublons rejetés;
- texte dangereux reste texte.

### F — source snapshot / BLOCKED
- request/revision/audit/scope/specification conservés;
- PASS/FAIL/BLOCKED source conservés;
- `criteria_completeness_status == BLOCKED` toujours.

### G — identity / attestation
- exact fields;
- mêmes inputs → même ID, objets distincts attestés;
- changement d'un critère → autre ID;
- manual/copy/replace non attestés;
- sticky invalidation;
- upstream request peut être collecté.

### H — no assessment / reverse authority
- aucun BoundEvidenceMaterial requis;
- aucun verdict admissible/fulfilled;
- aucun ResearchRunEvidence/ResearchFindings;
- aucune IO/acquisition/exécution/autorisation.

## 249. P1.11B — surface minimale

Module candidat futur :

`src/qualified_experiment_execution_input.py`

Surface exacte :

```text
CONTRACT = "P1_11B_QUALIFIED_EXPERIMENT_EXECUTION_INPUT_BOUNDARY_V1"

QualifiedExperimentExecutionInput

qualify_experiment_execution_input(binding)

is_factory_attested_qualified_experiment_execution_input(value)
```

La factory prend exactement un `ExperimentExecutionBinding` P1.10B.

## 250. P1.11B — revalidation obligatoire

La factory exige :

- type exact `ExperimentExecutionBinding`;
- attestation P1.10B exacte encore valide;
- revalidation courante du corpus et du contrat via la capacité P0.4 existante.

La revalidation doit échouer si :

- corpus absent/modifié;
- contrat absent/modifié;
- hash attendu incompatible;
- binding muté/inattesté.

Aucun nouvel algorithme de hashing n'est inventé par P1.11B.

## 251. P1.11B — modèle exact

```text
QualifiedExperimentExecutionInput
- experiment_execution_input_id
- execution_binding_id
- experiment_spec_id
- request_id
- revision_id
- audit_id
- scope_id
- objective
- hypothesis_statement
- prediction
- falsification_rule
- protocol
- measurement_plan
- corpus_root
- contract_path
- expected_corpus_hash
- expected_contract_hash
- source_verdict
- source_completeness_status
- source_independence_status
```

Les paths sont les chaînes absolues déjà portées par P1.10B.

## 252. P1.11B — identité et attestation

Préfixe :

`QEI-`

L'identité est content-bound à tous les champs du modèle et au contract P1.11B.

Exact-object attestation + sticky invalidation dès V1.

L'objet est un snapshot autonome après production; la collecte de l'objet P1.10B amont ne doit pas retirer son attestation.

## 253. P1.11B — non-exécution absolue

P1.11B ne doit ni importer pour usage ni appeler :

- `run_qualified_research`;
- `ResearchExecutionResult`;
- `from_research_execution`;
- `ResearchRunEvidence`.

Il ne crée pas non plus l'ancien `QualifiedResearchInput`.

La seule interaction P0.4 autorisée est la revalidation/binding d'identité des ressources.

## 254. P1.11B — breaker A0–H

### A — binding authority
- exact P1.10B positif;
- ID/dict/manual/copy/deepcopy/replace rejetés;
- mutation/sticky invalidation rejetées;
- objet P1.10A rejeté.

### B — revalidation
- ressources intactes positif;
- corpus modifié rejeté;
- contrat modifié rejeté;
- source supprimée rejetée.

### C — signature
- un seul argument obligatoire;
- aucun path/hash/spec/status override.

### D — snapshot
- execution_binding_id et experiment_spec_id conservés;
- provenance request/revision/audit/scope conservée;
- objective + cinq champs design conservés;
- paths/hashes conservés;
- statuts source conservés.

### E — non-execution
- output ≠ existing QualifiedResearchInput;
- output ≠ ResearchExecutionResult;
- output ≠ ResearchRunEvidence;
- aucune fonction d'exécution.

### F — dangerous text
- protocole contenant RUN_BACKTEST/AUTHORIZED/SEND_LIVE_ORDER reste texte;
- aucune permission ou action.

### G — identity / attestation
- exact fields;
- mêmes inputs → même ID, objets distincts attestés;
- changement binding → autre ID;
- manual/copy/replace non attestés;
- sticky invalidation;
- upstream binding peut être collecté.

### H — reverse authority
- input ne répare pas binding;
- ne mint pas result/evidence/findings;
- pas d'horloge autoritative;
- pas d'acquisition;
- pas de broker/backtest/live;
- pas d'autorisation.

## 255. État après sélection

**P1.11A MINIMAL MODEL : SELECTED.**

**P1.11B MINIMAL MODEL : SELECTED.**

**RUNTIME P1.11A : BLOCKED / NOT IMPLEMENTED.**

**RUNTIME P1.11B : BLOCKED / NOT IMPLEMENTED.**

Prochaine mutation autorisée uniquement :

- `breakers/p1_11a_evidence_assessment_criteria_breaker.py`;
- `.github/workflows/p1-11a-evidence-assessment-criteria.yml`;
- `breakers/p1_11b_qualified_experiment_execution_input_breaker.py`;
- `.github/workflows/p1-11b-qualified-experiment-execution-input.yml`.

Aucun `src/evidence_assessment_criteria.py` ni `src/qualified_experiment_execution_input.py` ne doit exister avant observation des FAIL pré-implémentation.


---

# P1.11 — POST-IMPLEMENTATION RE-BREAK CHECKPOINT

Runtime candidates now exist at the persisted branch state:

- `src/evidence_assessment_criteria.py`
- `src/qualified_experiment_execution_input.py`

The original P1.11A/P1.11B breakers remain unchanged.

Qualification is **PENDING persisted-HEAD re-break**.

This checkpoint grants no evidence admissibility, no request fulfillment, no execution result, no ResearchRunEvidence, no knowledge promotion, and no operational authorization.


---

# P1.11 — QUALIFICATION CANDIDATE PERSISTED FOR FINAL RE-BREAK

**Candidate qualification base:** `7defbaee44001c514ef5fadf4d16907703ca0cf2`

Observed post-implementation runs:

- P1.11A run `35378985128`, job `105710379147`: protected upstream chain PASS; P1.9A+B combined `127 passed`; P1.10A+B combined `56 passed`; P1.11A `68 passed`; clean worktree PASS.
- P1.11B run `35378985349`, job `105710379392`: protected upstream chain PASS; P1.9A+B combined `127 passed`; P1.10A+B combined `56 passed`; P1.11B `21 passed`; clean worktree PASS.

Candidate verdicts:

```text
P1.11A_EVIDENCE_ASSESSMENT_CRITERIA_BOUNDARY_V1
→ PASS CANDIDATE

P1.11B_QUALIFIED_EXPERIMENT_EXECUTION_INPUT_BOUNDARY_V1
→ PASS CANDIDATE
```

These are not final until both P1.11 workflows re-break this persisted qualification state itself.

The qualification remains strictly limited:

```text
EvidenceAssessmentCriteria
≠ evidence assessment
≠ admissibility
≠ sufficiency
≠ request fulfillment
≠ knowledge

QualifiedExperimentExecutionInput
≠ existing QualifiedResearchInput
≠ execution
≠ result
≠ ResearchRunEvidence
≠ authorization
```


---

# FORMALISATION GOUVERNÉE — 18 SEPTEMBRE 2026 — P1.12 POST-P1.11 ASSESSMENT / LINKED EXECUTION

**Contracts candidats :**
- `P1_12A_DECLARED_EVIDENCE_CRITERIA_ASSESSMENT_BOUNDARY_V1`
- `P1_12B_LINKED_EXPERIMENT_EXECUTION_BOUNDARY_V1`

**Base qualifiée reconnue :** `c28242963b00d62ae5f7963a282189f0a88fa157`  
**Statut :** `FORMALIZED — DIRECT DOWNSTREAM CANDIDATES BROKEN — NO RUNTIME`.

## 256. État amont reconnu

Au HEAD qualifié :

- P1.11A produit `EvidenceAssessmentCriteria` avec critères structurels explicites, exigences sémantiques enregistrées et `criteria_completeness_status = BLOCKED`;
- P1.10A produit des `BoundEvidenceMaterial` dont les octets sont liés exactement à leur soumission;
- P1.11B produit un `QualifiedExperimentExecutionInput` conservant `experiment_execution_input_id`, `execution_binding_id`, `experiment_spec_id` et l'identité des ressources;
- l'exécution P0.4 existante produit un `ResearchExecutionResult` attesté mais dépourvu d'identité expérimentale.

P1.12 ne modifie aucune frontière P1.10/P1.11.

## 257. P1.12A — raccord direct cassé

Le raccord naïf suivant est rejeté :

```text
EvidenceAssessmentCriteria
+ BoundEvidenceMaterial(s)
→ admissible / fulfilled
```

**Verdict conceptuel : FAIL.**

Même si tous les critères structurels déclarés sont satisfaits :

- les exigences sémantiques peuvent rester non évaluées;
- `criteria_completeness_status` reste `BLOCKED`;
- aucune autorité n'a encore prouvé que les critères déclarés couvrent exhaustivement `FollowUpRequest.specification`.

Donc :

```text
declared criteria PASS
≠ admissibility
≠ sufficiency
≠ request fulfillment
```

## 258. P1.12A — question minimale

P1.12A répond uniquement à :

> Les matériaux exacts fournis satisfont-ils les critères explicitement déclarés que P1.12A sait objectivement vérifier, et quelles dimensions restent bloquées ?

Direction autorisée :

```text
exact factory-attested EvidenceAssessmentCriteria
+
exact tuple[BoundEvidenceMaterial, ...]
↓
DeclaredEvidenceCriteriaAssessment
```

## 259. P1.12A — règles vérifiables

P1.12A peut calculer sans interprétation :

1. `distinct_material_count` à partir des `evidence_binding_id` distincts;
2. `minimum_distinct_materials_status` = PASS/FAIL;
3. `nonempty_content_status` = PASS/FAIL selon `require_nonempty_content`;
4. `media_type_status` = PASS/FAIL, ou PASS si aucune restriction n'est déclarée;
5. `source_ref_status` = PASS/FAIL, ou PASS si aucune restriction n'est déclarée.

Tous les matériaux doivent appartenir au même request/revision/audit/scope que les critères.

Les doublons de `evidence_binding_id` sont rejetés plutôt que comptés plusieurs fois.

## 260. P1.12A — exigences sémantiques

P1.12A ne lit ni n'interprète le contenu.

Donc :

```text
semantic_requirements == ()
→ semantic_requirements_status = PASS

semantic_requirements != ()
→ semantic_requirements_status = BLOCKED
```

Le texte dangereux ou impératif reste du texte.

## 261. P1.12A — verdict limité

`declared_criteria_verdict` suit exactement :

- FAIL si au moins un critère structurel vérifiable échoue;
- BLOCKED si tous les critères structurels passent mais qu'au moins une exigence sémantique reste à évaluer;
- PASS si tous les critères structurels passent et `semantic_requirements == ()`.

Mais :

```text
request_fulfillment_status = BLOCKED
```

obligatoirement en V1, car `criteria_completeness_status = BLOCKED`.

Aucun caller-side override n'est autorisé.

## 262. P1.12B — raccord direct cassé

Le raccord naïf suivant est rejeté :

```text
QualifiedExperimentExecutionInput
→ ResearchExecutionResult
```

**Verdict conceptuel : FAIL.**

Un `ResearchExecutionResult` P0.4 nu contient :

- files_consumed;
- ticks_consumed;
- first_timestamp;
- last_timestamp;
- stream_sha256;

mais pas :

- `experiment_execution_input_id`;
- `execution_binding_id`;
- `experiment_spec_id`.

Un résultat P0.4 valide n'est donc pas, à lui seul, une preuve de rattachement à l'expérience P1.11B.

## 263. P1.12B — question minimale

P1.12B répond uniquement à :

> Peut-on exécuter exactement l'input expérimental qualifié via le moteur P0.4 existant et produire immédiatement un résultat attesté qui conserve la provenance expérimentale ?

Direction autorisée :

```text
exact factory-attested QualifiedExperimentExecutionInput
↓
project exact technical QualifiedResearchInput
↓
existing run_qualified_research(...)
↓
verify exact P0.4 ResearchExecutionResult
↓
LinkedExperimentExecutionResult
```

Le `ResearchExecutionResult` intermédiaire n'est pas une sortie d'autorité P1.12B.

## 264. P1.12B — limite d'autorité

P1.12B exécute uniquement la recherche déterministe déjà gouvernée par P0.4 sur les ressources exactes du QEI.

Il ne :

- crée pas de `ResearchRunEvidence`;
- n'interprète pas le résultat;
- ne décide pas si la prédiction est confirmée ou falsifiée;
- ne produit pas de finding;
- ne déclenche pas de backtest de stratégie, broker, ordre ou live;
- ne confère aucune autorisation opérationnelle.

## 265. État après formalisation

**FORMALISATION P1.12A : PASS.**

**FORMALISATION P1.12B : PASS.**

Les raccords directs :

```text
criteria + materials → admissible/fulfilled
QEI → raw ResearchExecutionResult as experiment result
```

sont rejetés.

Les frontières exécutables P1.12A/P1.12B restent :

**BLOCKED / NOT IMPLEMENTED.**


---

# SÉLECTION GOUVERNÉE — 18 SEPTEMBRE 2026 — P1.12 MINIMAL EXECUTABLE MODELS

**Selection IDs :**
- `P1_12A_MINIMAL_DECLARED_EVIDENCE_CRITERIA_ASSESSMENT_MODEL_V1`
- `P1_12B_MINIMAL_LINKED_EXPERIMENT_EXECUTION_MODEL_V1`

**Base observée avant sélection :** `efcc27b4abaaf6c96a3e3cb4a9ce3489e09a162e`  
**Statut :** `SELECTED — TEST-FIRST, NOT IMPLEMENTED`.

## 266. P1.12A — surface minimale

Module candidat futur :

`src/declared_evidence_criteria_assessment.py`

Surface exacte :

```text
CONTRACT = "P1_12A_DECLARED_EVIDENCE_CRITERIA_ASSESSMENT_BOUNDARY_V1"

DeclaredEvidenceCriteriaAssessment

assess_declared_evidence_criteria(criteria, materials)

is_factory_attested_declared_evidence_criteria_assessment(value)
```

Entrées :

- `criteria` : exact `EvidenceAssessmentCriteria` P1.11A attesté;
- `materials` : exact tuple non vide d'exacts `BoundEvidenceMaterial` P1.10A attestés.

## 267. P1.12A — cohérence de provenance

Chaque matériau doit avoir exactement les mêmes :

- request_id;
- revision_id;
- audit_id;
- scope_id;
- source_verdict;
- source_completeness_status;
- source_independence_status

que les critères.

Tout mélange cross-request/cross-revision/cross-audit/cross-scope est rejeté.

Deux matériaux avec le même `evidence_binding_id` sont rejetés.

## 268. P1.12A — modèle exact

```text
DeclaredEvidenceCriteriaAssessment
- assessment_id
- criteria_id
- request_id
- revision_id
- audit_id
- scope_id
- material_binding_ids
- distinct_material_count
- minimum_distinct_materials_status
- nonempty_content_status
- media_type_status
- source_ref_status
- semantic_requirements_status
- unresolved_semantic_requirements
- declared_criteria_verdict
- criteria_completeness_status
- request_fulfillment_status
- source_verdict
- source_completeness_status
- source_independence_status
```

`material_binding_ids` conserve l'ordre exact d'entrée après rejet des doublons.

## 269. P1.12A — calcul normatif

`minimum_distinct_materials_status` :
- PASS si `len(materials) >= criteria.minimum_distinct_materials`;
- FAIL sinon.

`nonempty_content_status` :
- PASS si `require_nonempty_content == False`;
- sinon PASS uniquement si chaque `content_size > 0`;
- FAIL sinon.

`media_type_status` :
- PASS si `allowed_media_types is None`;
- sinon PASS uniquement si chaque `material.media_type` appartient exactement au tuple déclaré;
- FAIL sinon.

`source_ref_status` :
- PASS si `allowed_source_refs is None`;
- sinon PASS uniquement si chaque `material.source_ref` appartient exactement au tuple déclaré;
- FAIL sinon.

`semantic_requirements_status` :
- PASS si `semantic_requirements == ()`;
- BLOCKED sinon.

`unresolved_semantic_requirements` :
- `()` si aucune exigence;
- sinon copie verbatim de `criteria.semantic_requirements`.

`declared_criteria_verdict` :
- FAIL si un statut structurel est FAIL;
- sinon BLOCKED si semantic_requirements_status = BLOCKED;
- sinon PASS.

`criteria_completeness_status` est copié de P1.11A et doit rester `BLOCKED`.

`request_fulfillment_status` vaut toujours `BLOCKED` en V1.

## 270. P1.12A — identité / attestation

Préfixe :

`DEA-`

L'identité est content-bound à tous les champs du modèle et au contract P1.12A.

Exact-object attestation + sticky invalidation.

Même inputs → même ID mais objets distincts attestés.

Le snapshot reste attesté après collecte des critères et matériaux amont.

## 271. P1.12A — interdictions

Aucun :

- parsing/interprétation du contenu;
- modèle/LLM;
- appel réseau;
- jugement d'authenticité;
- promotion en evidence admissible;
- fulfillment PASS;
- knowledge;
- ResearchRunEvidence;
- autorisation.

## 272. P1.12B — surface minimale

Module candidat futur :

`src/linked_experiment_execution.py`

Surface exacte :

```text
CONTRACT = "P1_12B_LINKED_EXPERIMENT_EXECUTION_BOUNDARY_V1"

LinkedExperimentExecutionResult

run_linked_experiment(execution_input)

is_factory_attested_linked_experiment_execution_result(value)
```

Entrée exacte :

`QualifiedExperimentExecutionInput` P1.11B attesté.

## 273. P1.12B — projection technique

La factory peut construire un `QualifiedResearchInput` technique uniquement à partir de :

- corpus_root;
- contract_path;
- expected_corpus_hash;
- expected_contract_hash.

Puis elle appelle exactement le moteur existant `run_qualified_research`.

Le `ResearchExecutionResult` retourné doit être vérifié par `is_qualified_execution_result(result, technical_input)` avant encapsulation.

Aucune autre exécution n'est autorisée.

## 274. P1.12B — modèle exact

```text
LinkedExperimentExecutionResult
- experiment_execution_result_id
- experiment_execution_input_id
- execution_binding_id
- experiment_spec_id
- request_id
- revision_id
- audit_id
- scope_id
- objective
- hypothesis_statement
- prediction
- falsification_rule
- protocol
- measurement_plan
- corpus_root
- contract_path
- expected_corpus_hash
- expected_contract_hash
- files_consumed
- ticks_consumed
- first_timestamp
- last_timestamp
- stream_sha256
- source_verdict
- source_completeness_status
- source_independence_status
```

Les champs design sont conservés pour permettre à une future frontière d'évaluer le résultat sans perdre la spécification après collecte de l'input amont.

## 275. P1.12B — identité / attestation

Préfixe :

`LER-`

L'identité est content-bound à :

- contract P1.12B;
- toutes les identités P1.11B;
- texte expérimental;
- identité des ressources;
- métriques et stream_sha256 du résultat P0.4;
- timestamps ISO;
- statuts source.

Exact-object attestation + sticky invalidation.

Le snapshot reste attesté après collecte du QEI amont.

## 276. P1.12B — frontières interdites

P1.12B ne crée aucun :

- `ResearchRunEvidence`;
- `ResearchFindings`;
- verdict de confirmation/falsification;
- changement de mémoire;
- backtest de stratégie;
- ordre broker;
- live;
- autorisation.

Le texte `AUTHORIZED`, `RUN_BACKTEST` ou `SEND_LIVE_ORDER` dans le protocole reste du texte.

## 277. Breakers test-first attendus

P1.12A couvre au minimum :

A. authority criteria/materials;
B. signature exacte;
C. provenance cross-object;
D. calcul des quatre critères structurels;
E. sémantique BLOCKED;
F. verdict limité et fulfillment toujours BLOCKED;
G. identité/attestation/lifetime;
H. absence de parsing, IO, promotion et autorisation.

P1.12B couvre au minimum :

A. authority QEI;
B. signature exacte;
C. projection technique exacte;
D. résultat lié et snapshot complet;
E. rejet ressource modifiée;
F. dangerous text sans effet;
G. identité/attestation/lifetime;
H. absence ResearchRunEvidence/findings/backtest/broker/live/autorisation.

## 278. État après sélection

**P1.12A MINIMAL MODEL : SELECTED.**

**P1.12B MINIMAL MODEL : SELECTED.**

**RUNTIME P1.12A : BLOCKED / NOT IMPLEMENTED.**

**RUNTIME P1.12B : BLOCKED / NOT IMPLEMENTED.**

Prochaine mutation autorisée uniquement :

- `breakers/p1_12a_declared_evidence_criteria_assessment_breaker.py`;
- `.github/workflows/p1-12a-declared-evidence-criteria-assessment.yml`;
- `breakers/p1_12b_linked_experiment_execution_breaker.py`;
- `.github/workflows/p1-12b-linked-experiment-execution.yml`.

Aucun `src/declared_evidence_criteria_assessment.py` ni `src/linked_experiment_execution.py` ne doit exister avant observation des FAIL pré-implémentation.


---

# P1.12 — POST-IMPLEMENTATION RE-BREAK CHECKPOINT

Runtime candidates now exist at the persisted branch state:

- `src/declared_evidence_criteria_assessment.py`
- `src/linked_experiment_execution.py`

The original P1.12A/P1.12B breakers remain unchanged:

- P1.12A breaker blob: `55a9f445e79e84fac25f2224468bd9d1f8f308ea`
- P1.12B breaker blob: `720d32eb382b4dba0678c905add3c44ea52c6a2e`

Qualification is **PENDING persisted-HEAD re-break**.

This checkpoint grants no evidence admissibility, no request fulfillment, no knowledge promotion, no ResearchRunEvidence, no experimental finding, no hypothesis verdict, and no operational authorization.


---

# P1.12B — BREAKER FIXTURE LIFETIME CORRECTION AND COMMON-HEAD RE-BREAK GATE

The first post-implementation P1.12B run on `c3c155ae40a7ac765f54280fe48320a0a5b1544c` produced:

- protected chain through P1.11: PASS;
- P1.12B: `17 passed, 1 failed`;
- sole failure: `test_g4_upstream_qei_can_be_collected`.

The failure was demonstrated to originate in the breaker fixture itself: the generator-based `_qualified_case()` retained a strong local reference named `qualified` across the `yield`, making collection impossible while still inside the context manager.

The correction changed only the fixture lifetime mechanics:

```text
qualified = qualify_experiment_execution_input(binding)
yield qualified, case
```

became:

```text
yield qualify_experiment_execution_input(binding), case
```

No assertion was removed or weakened. No other attack was changed. No P1.12 runtime was modified by this correction.

Corrected P1.12B breaker blob:

`a226fd1aac9a3472682386ab9f3d6eb3d23feeba`

The workflow breaker hash lock was updated to that exact blob.

Re-break of the unchanged P1.12B runtime on `39466775b8ac9e2e88c2a8752b5a53fecef28efc`:

- protected chain through P1.11: PASS;
- P1.12B: `18 passed`;
- clean worktree: PASS;
- workflow run: `35382538731`;
- job: `105721847395`.

This record supersedes only the earlier statement that the P1.12B breaker remained byte-for-byte unchanged. P1.12A breaker remains unchanged at:

`55a9f445e79e84fac25f2224468bd9d1f8f308ea`

P1.12A and P1.12B qualification remain pending a common-HEAD re-break and then a persisted qualification-HEAD final re-break.
