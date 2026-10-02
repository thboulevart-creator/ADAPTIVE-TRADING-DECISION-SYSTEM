# REAL P5-E — PRE-EXECUTION READINESS V0.2 — SELF-CONTAINED DELTA REVIEW PACKET

Date: 2026-10-02

## Independent reviewer mandate

Review only the targeted readiness amendment from V0.1 to V0.2.

Previous external verdict:

`VERDICT = FAIL`

Previous blocking findings:

- BF1 — no stage built or qualified the finite timed runner;
- BF2 — real monotonic timing evidence was not safely represented by the adopted integer-second synthetic model.

V0.2 is requirements-only.

It does not implement RPE-01→RPE-06 and creates no REAL P5-E authority.

## Identity

Base reviewed readiness HEAD:
`90189ac1ddddc8d81b12eeaa2a4241969a7dc405`

V0.2 technical HEAD:
`d6adcbaef8fc596fc2779901775080e4ac1c6fd5`

V0.2 internal adjudication blob:
`d81ba88c6e3d964928223f31f9e7bbce233b7022`

V0.2 readiness JSON blob:
`7708709840f2f3b4317a7968987b1a280f143b70`

V0.2 readiness report blob:
`0ba9af17f0d62045fec4c5923cc876aedd772fb7`

Adopted P5-E contract remains:
`43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9`

Adopted P5-E synthetic model remains:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`

P5-D4 runtime remains:
`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

## V0.2 dependency DAG under review

```text
RPE-01 — N4 GOVERNED CLOSED SCHEMA
       ├────────────→ RPE-02 — N5 + REAL-TIME REPRESENTATION
       │
       └────────────→ RPE-03 — NB5 ANCESTRY CLASSIFIER

RPE-02 + RPE-03
       ↓
RPE-04 — NB2 + NB3 REAL OBSERVATION ADAPTER
       ↓
RPE-05 — FINITE FIXED-RATE TIMED RUNNER
       ↓
RPE-06 — NB9 CONTROLLED REAL EXPERIMENT PREREGISTRATION
       ↓
SEPARATE ONE-SHOT HUMAN EXECUTION AUTHORIZATION
```

## Required delta-review questions

### BF1 / RPE-05

1. Does RPE-05 now explicitly own every timing/scheduler responsibility that P5-D4 forbids?
2. Can RPE-05 be fully qualified without network using injected clock/sleep/fake adapter?
3. Are fixed-rate anchoring, finite horizon, single active attempt, terminal reason and deterministic STOP all covered?
4. Is any timing authority still missing between RPE-04 and RPE-06?
5. Does RPE-05 accidentally acquire evaluation, queue coalescing, retargeting, promotion, publication or Vault authority?

### BF2 / RPE-02

6. Does integer monotonic nanoseconds avoid the real >60s → truncated 60s false-PASS problem?
7. Are scheduled slot and actual start now explicitly distinct?
8. Are remote observation completion and total attempt completion explicitly distinct?
9. Is the decision gate between a conservative conversion layer and a separate real-time model V0.2 correctly deferred until RED evidence exists?
10. Can either candidate preserve the adopted synthetic model without using lossy conversion for real pass/fail?
11. Is any real-time field or boundary still missing?

### NF1 / RPE-01

12. Does RPE-01 close duplicate-member attacks before normal JSON dictionary construction?
13. Does it close all object depths, strict types, list vocabularies/uniqueness/order and adjacent governed configs?
14. Is binding/versioning the guard itself sufficient to avoid merely moving the recombination target?
15. What additional schema attacks remain?

### NF2 / RPE-03

16. Are replace refs, shallow state, grafts, object type, missing objects, timeout and corruption all handled fail-closed?
17. Is exit 1 from `merge-base --is-ancestor` safely NON_FAST_FORWARD only after both commit objects/domain are verified?
18. Is any Git configuration/environment isolation also required for the local classifier?

### NF3 / RPE-04

19. Is one controlled fetch transaction into an isolated namespace a sound preferred design?
20. Is the exact observed tip still unambiguously defined?
21. Is `CONTENT_CONTAINED_NOT_OBSERVED` protected from queue injection?
22. Are pinned URL, config isolation, hooks, prompt and timeout sufficient?
23. What exact fetch/ref evidence must eventually be preregistered to avoid ambiguity?

### NF4/NF5/NF6 / RPE-06

24. Is a distinct sandbox experiment contract sufficient to avoid silently amending the adopted `integration/system-v1` source?
25. Is an isolated control root enough to protect real P5-D4 state?
26. Is the push outcome matrix complete enough for preregistration?
27. Are release-start and push-completion timestamps both needed?
28. Is same-host same-monotonic-domain correctly REQUIRED?
29. Is sleep/hibernation invalidation adequately represented as a requirement?
30. Is sandbox repository first materially safer than an experiment ref in canonical ATDS?
31. What exact CI/workflow audit evidence must be frozen before push?

### DAG / missing prerequisites

32. Is the V0.2 DAG correct?
33. Should RPE-05 depend on fully qualified RPE-04, or only on a frozen RPE-04 interface?
34. Can RPE-02 and RPE-03 safely proceed independently after RPE-01?
35. Is there any prerequisite still missing before RPE-06?
36. Are any requirements assigned to the wrong stage?
37. Does preserving the adopted contract/model bytes remain appropriate?

## Required adversarial mandate

Try to falsify at least:

- duplicate JSON key with contradictory authority values;
- authority in adjacent runner/adapter config;
- float/int/bool type laundering;
- 60.000000001-second real latency;
- scheduled 30s but actual start 54s;
- remote completion versus local completion divergence;
- scheduler fixed-delay drift;
- sleep returning late;
- injected clock discontinuity;
- runner attempt overlap;
- runner terminal reason not stopping;
- replace refs;
- shallow repository;
- grafts;
- non-commit objects;
- Git timeout/error exit;
- remote ref advancing during observation;
- untrusted Git config/hook/url rewrite;
- contained commit treated as observed tip;
- push fails but target appears;
- sandbox success laundered into production-branch SLA;
- accidental production P5-D4 state mutation;
- hidden evaluation/promotion/Vault/P6 authority.

## Required output

Return exactly one:

`VERDICT = PASS | PASS_WITH_NON_BLOCKING_NOTES | FAIL`

Then provide:

- BLOCKING_FINDINGS
- NON_BLOCKING_FINDINGS
- BF1_RUNNER_CHECK
- BF2_REAL_TIME_REPRESENTATION_CHECK
- N4_SCHEMA_CHECK
- NB5_ANCESTRY_CHECK
- NB2_NB3_ADAPTER_CHECK
- NB9_EXPERIMENT_CHECK
- DAG_CHECK
- MISSING_PREREQUISITES
- AUTHORITY_LEAKAGE_CHECK
- CLAIM_SCOPE_CHECK
- RECOMMENDED_NEXT_ACTION

For each finding:
- cite exact packet section/field;
- distinguish OBSERVED from INFERENCE;
- state BLOCKING or NON_BLOCKING;
- give a minimal falsification case when possible.

This delta review creates no authority.

`REAL_P5E = CLOSED`

---

# SOURCE: PREVIOUS EXTERNAL REVIEW RETURN

VERDICT = FAIL

J'ai lu tout le paquet. J'ai rejoué localement deux sondes sur le modèle adopté (`c0f16ba`) et sur le vérificateur d'invariants adopté (`de41337`), en réutilisant les artefacts reconstruits lors des revues précédentes ; leurs blobs correspondent à ceux cités ici.

L'ordre de dépendances proposé est globalement juste. Le FAIL tient à deux trous de décomposition : en suivant la carte à la lettre, chaque étape peut atteindre son critère de sortie alors que deux prérequis indispensables à une exécution réelle ne sont traités par aucune étape.

### BLOCKING_FINDINGS

**BF1 — Aucune étape ne construit ni ne qualifie le runner temporisé.** (OBSERVÉ dans le paquet, conséquence par INFÉRENCE)

- **Sections concernées :**&#x20;
  - « READINESS JSON » `recommended_sequence` (RPE-01 à RPE-05) ;
  - `NB9.safest_first_real_experiment.claim_limit` (« Qualifies runner/transport/adapter timing ») ;
  - « P5-D4 BOUNDED LOOP CONTRACT » `observation_adapter_boundary.time_based_polling_in_p5d4_v0_1_authorized: false`, `sleep_or_timer_authorized: false`, `p5e_owns_near_real_time_polling_qualification: true`.
- **Constat :**&#x20;
  - RPE-04 qualifie une *observation* (une lecture de ref).
  - RPE-05 est une *préregistration*.
  - Le composant qui déclenche les tentatives toutes les 30 s n'est construit ni qualifié nulle part. Ce composant porte l'autorité de sleep et de timer, le single-writer, la borne finie, les conditions d'arrêt et l'arrêt sur raison terminale D4.
  - D4 interdit explicitement sleep et timer et délègue cette responsabilité à P5-E.
- **Conséquence :** la déclaration NB9 mentionne la qualification du « runner », mais aucun artefact correspondant n'existe dans la chaîne.
- **Falsification minimale :** RPE-01 à RPE-05 sont tous `QUALIFIED` ou `PREREGISTERED` selon leurs critères de sortie, et l'expérience réelle exige pourtant d'exécuter un code temporisé jamais testé.

**BF2 — La représentation du temps réel est incompatible avec le modèle adopté, et le traitement N5 prévu ne la couvre pas.** (OBSERVÉ)

- **Sections concernées :** « ADOPTED P5-E SYNTHETIC MODEL » (`_is_nonnegative_int`, champ `scheduled_at_seconds`) ; « READINESS JSON » `N5.recommended_closure.preserve_synthetic_model_bytes_unless_a_test_exposes_inconsistency` ; `NB2_NB3.requirements` (« record attempt-start and read-completion monotonic timestamps »).
- **Sondes sur le modèle adopté :**&#x20;
  - `release=1.37`, `(30.004, 31.2, A)` → exception `controlled source release time must be a nonnegative integer`. Le modèle ne peut pas consommer d'horodatages monotones réels.
  - `release=1`, `(30, 55, A)` → `PASS`, latence 54. Le modèle n'a pas de champ « début effectif » : une tentative prévue à 30 et réellement démarrée à 54 est indiscernable d'une tentative à l'heure. Le contrat dit pourtant `attempt_start_and_read_completion_are_distinct`.
  - Une latence réelle de 60,4 s tronquée en 60 → `PASS`. Une troncature naïve transforme un dépassement en réussite.
- **Ce qui manque :**&#x20;
  - une règle de quantification conservatrice, ou bien un modèle en flottants ;
  - une tolérance maximale entre le créneau et le début effectif, au-delà de laquelle le créneau compte comme manqué ;
  - la définition de la « complétion » quand une tentative comporte deux phases (lecture de la ref, puis matérialisation de l'objet), aussi bien pour la latence que pour l'occupation single-writer.
- **Pourquoi la carte ne le couvre pas :** RPE-02 est cadrée sur les égalités entières autour du modèle inchangé. RPE-04 enregistre des timestamps sans dire comment ils sont convertis. La conversion serait donc décidée implicitement en aval, sans qualification.

### NON_BLOCKING_FINDINGS

- **NF1 — N4 : une clé dupliquée échappe à un schéma fermé basé sur le dictionnaire.** (OBSERVÉ)&#x20;
  - Concerné : `N4.recommended_closure.requirements`.
  - J'insère `"evaluation_authorized": true` avant la clé existante `false` dans `authority_boundary`. `json.loads` garde la dernière occurrence, donc `assert_contract_invariants` passe. Un parseur qui garde la première occurrence lirait `true`.
  - Correction : un chargeur avec `object_pairs_hook` qui rejette les doublons.
  - Autres points à intégrer au garde N4 :&#x20;
    - fermer *tous* les niveaux du contrat plutôt que sélectionner les blocs « pertinents », ce qui est plus simple et évite un jugement de pertinence ;
    - types stricts (`is True`, entier non booléen ; la coercition `30 → 30.0` survit aujourd'hui) ;
    - unicité et appartenance à un vocabulaire fermé pour les listes ;
    - ordre figé pour `real_end_to_end_stages`.
  - Le garde doit lui-même être lié par blob, et toute modification de son ensemble de clés doit être traitée comme un amendement. Sinon il ne fait que déplacer la cible d'une recombinaison de blob.
  - Il doit s'appliquer à chaque nouveau JSON gouverné (configuration de l'adaptateur, préregistration RPE-05), pas seulement au contrat adopté. Sinon l'autorité peut passer par un fichier voisin ou un drapeau du runner.
- **NF2 — NB5 : l'intégrité du domaine d'objets n'est pas définie.** (INFÉRENCE)&#x20;
  - Concerné : `NB5.recommended_closure.input` (« verified_local_git_object_domain »).
  - Seul « `previous_is_ancestor_of_new` → FAST_FORWARD » peut produire un faux positif dangereux. Les replace refs (`refs/replace`), les grafts et un historique shallow peuvent fausser `merge-base --is-ancestor`.
  - À exiger :&#x20;
    - `GIT_NO_REPLACE_OBJECTS=1`, absence de fichiers `shallow` et `info/grafts`, sinon UNKNOWN ;
    - vérification du type `commit` pour les deux SHA ;
    - code de sortie 0 → ancêtre, 1 → non-ancêtre, tout autre code → UNKNOWN ;
    - tête précédente absente du domaine (par exemple après un GC) → UNKNOWN ;
    - timeout → UNKNOWN.
- **NF3 — NB2/NB3 : la course entre deux lectures distantes, et une option plus simple.** (INFÉRENCE)&#x20;
  - Concerné : `NB2_NB3.requirements` (ls-remote puis matérialisation).
  - Faire `ls-remote` puis `fetch` revient à faire deux lectures distantes à deux instants différents. La valeur vue par le fetch est elle-même une observation.
  - Option plus simple : un seul `git fetch` de la ref vers un espace de noms isolé. Dans une même session upload-pack, le SHA annoncé et ses objets arrivent ensemble, ce qui supprime la course. Le coût est une latence plus élevée, biaisée dans le sens conservateur.
  - Si on garde deux lectures, il faut dire laquelle est l'observation. Une course qui reste en avance rapide (FF) ne devrait pas donner UNKNOWN (ce qui bloque la boucle) si X a bien été matérialisé comme ancêtre de la valeur fetchée.
  - Isolation de l'environnement Git : le motif D3F (`_run`) hérite de `os.environ` et résout `origin` par nom. `url.insteadOf`, les helpers de credentials, les proxies et les hooks (`reference-transaction` s'exécute sur un fetch) proviennent donc de la configuration de l'utilisateur. Il faut une URL épinglée, `GIT_CONFIG_GLOBAL` et `GIT_CONFIG_NOSYSTEM` neutralisés, un `core.hooksPath` vide, `GIT_TERMINAL_PROMPT=0`, et un timeout qui se traduit par un échec de lecture.
- **NF4 — NB9 : contrat de référence et état de contrôle de l'expérience non définis.** (OBSERVÉ et INFÉRENCE)&#x20;
  - Concerné : « ADOPTED P5-E CONTRACT » `monitored_source.branch = integration/system-v1`, qui est gardé ; `NB9.safest_first_real_experiment.remote_ref = DEDICATED_EXPERIMENT_REF`.
  - Une expérience sur une autre ref sort de la source surveillée du contrat adopté. Il faut un contrat d'expérience distinct, et dire explicitement qu'il ne s'agit pas d'un amendement silencieux.
  - Le résolveur de racine de contrôle de D4 pointe vers la racine de production (`USERPROFILE`), qui contient la tête `1d4c…` en attente. L'expérience exige donc une racine de contrôle isolée.
  - Le bloc `authority` de la carte ne contient pas `p5d4_real_state_mutation_authorized: false`, alors que la préregistration BB1 le contenait.
- **NF5 — NB9 : protocole de push incomplet.** (INFÉRENCE)&#x20;
  - Il faut une matrice des issues possibles :&#x20;
    | Push   | Cible observée ?   | Classement                              |
    | ------ | ------------------ | --------------------------------------- |
    | succès | oui, dans la borne | valide                                  |
    | succès | non, dans la borne | échec SLA                               |
    | échec  | non                | `INVALID_EXPERIMENT` (pas un échec SLA) |
    | échec  | oui                | `INCONCLUSIVE` / `BLOCKED`              |
  - Push en création seule : `--force-with-lease=<ref>:` avec une valeur attendue vide, et refspec explicite `<sha>:refs/heads/<exp>`.
  - Enregistrer aussi la fin du push pour encadrer la latence des deux côtés.
  - Auditer les workflows GitHub Actions déclenchés par `on: push` sans filtre de branche avant tout push : un push sur une ref d'expérience peut lancer de la CI avec des secrets.
  - Envisager un dépôt bac à sable comme toute première expérience. C'est encore plus sûr qu'une ref dans le dépôt canonique, au prix d'un écart sur des facteurs propres au dépôt qui sont probablement mineurs (INFÉRENCE).
- **NF6 — Domaine d'horloge.**&#x20;
  - `same_host_preferred` devrait être `required`. L'échappatoire « cross-host clocks without proven common monotonic domain » laisse ouverte une preuve qui n'est pas réalisable en pratique.
  - La veille ou l'hibernation de l'hôte pendant l'expérience doit être interdite ou détectée.
  - La résolution de l'horloge monotone de Python sur Windows est à vérifier ; je ne la connais pas avec certitude.
- **NF7 — Coût de gouvernance.**&#x20;
  - RPE-01 et RPE-02 sont deux durcissements de tests autour d'artefacts adoptés, sans code runtime. Ils peuvent partager une passe avec des familles RED séparées sans affaiblir l'isolation test-first.
  - RPE-03 doit rester séparée, car c'est du code nouveau.
  - NB5 ne dépend que de N4 : la chaîne présentée comme linéaire est plus stricte que les dépendances réelles du JSON.

### N4_CHECK

- **Question 1.** Oui, le durcissement est requis avant les amendements à venir, notamment ceux de RPE-02 et RPE-05.
- **Question 2.** Un garde séparé est préférable à une modification du contrat adopté, à condition d'être lié par blob et versionné comme un amendement.
- **Question 3.** Tous les niveaux du contrat doivent être fermés, pas seulement certains blocs.
- **Question 4.** L'égalité exacte des clés ne suffit pas : il faut aussi les types stricts, l'unicité, les vocabulaires fermés et le rejet des clés dupliquées.
- **Question 5.** Oui, il existe des attaques non couvertes :&#x20;
  - clé dupliquée (démontrée, NF1) ;
  - autorité portée par un fichier voisin ou un drapeau du runner (INFÉRENCE).

### N5_CHECK

- **Questions 6 à 10.** Les égalités observées sont cohérentes avec le contrat adopté :&#x20;
  - une libération exactement sur un créneau est éligible (ordonnancement conservateur) ;
  - une fin de lecture exactement au créneau suivant n'est pas un débordement ;
  - une fin précédente égale au début suivant n'est pas un chevauchement ;
  - `latency <= 60` correspond au « max 60 » du contrat.
- **Question 11.** À figer en plus : les points de BF2 (flottants, début effectif, tolérance de démarrage, fin en deux phases).
- **Question 12.** Il faut probablement soit un modèle V0.2 qui accepte des flottants et un début effectif, soit une couche de conversion qualifiée. La conserver octet pour octet ne peut se décider qu'après avoir tranché BF2.

### NB5_CHECK

- **Questions 13 et 14.** Les règles sont complètes et fail-closed, sous réserve de NF2. NON_FAST_FORWARD convient aussi bien au retour arrière qu'à l'historique divergent ; un sous-type peut être enregistré comme simple preuve, sans changer la classe.
- **Question 15.** UNKNOWN doit couvrir : objet manquant, objet qui n'est pas un commit, erreur Git (code > 1), shallow, grafts ou replace refs, tête précédente absente, timeout, corruption.
- **Question 16.** Oui, sans réseau.
- **Question 17.** Aucun composant qualifié n'est réutilisable tel quel.

### NB2_NB3_CHECK

- **Question 18.** Le couplage NB2 et NB3 dans un seul adaptateur est correct.
- **Question 19.** Seul le SHA d'une lecture distante réussie peut être appelé pointe observée. Oui.
- **Question 20.** Les commits intermédiaires découverts par énumération d'ascendance restent `CONTENT_CONTAINED_NOT_OBSERVED`. Oui.
- **Questions 21 et 22.** Voir NF3 : préférer un fetch unique ; UNKNOWN est correct si le SHA ne peut pas être prouvé, mais la fin de lecture doit alors être mappée vers le modèle (BF2).
- **Question 23.** P5-D2 reste un consommateur déterministe d'événements normalisés. Préservé.
- **Question 24.** Aucune coalescence ni aucun reciblage n'est introduit dans le texte.

### NB9_CHECK

- **Question 25.** Une ref dédiée est plus sûre que `integration/system-v1`. Un dépôt bac à sable l'est encore plus (NF5).
- **Question 26.** La déclaration est légitime si elle est bornée au transport, à l'adaptateur et au runner. Le runner n'existe pas encore (BF1).
- **Questions 27 et 28.** Prendre l'origine juste avant le début du push est conservateur et falsifiable : la règle de pré-libération bloque une détection antérieure. Il faut ajouter la fin du push comme borne de preuve (NF5).
- **Question 29.** Oui, même hôte et même domaine d'horloge, comme exigence (NF6).
- **Question 30.** Conditions avant toute expérience sur `integration/system-v1` :&#x20;
  - autorisation humaine distincte ;
  - mise à jour gouvernée légitime, poussée depuis l'hôte instrumenté ;
  - décision explicite sur l'état réel de D4 (tête en attente, capacité de file) ;
  - garde N4 appliqué.
- **Question 31.** Interdire un commit canonique créé uniquement pour mesurer est correct.

### DEPENDENCY_ORDER_CHECK

- **Question 32.** L'ordre N4, puis N5, puis NB5, puis NB2/NB3, puis NB9 est correct, avec une étape manquante (BF1).
- **Question 33.** RPE-01 et RPE-02 peuvent être combinés (NF7).
- **Question 36.** Le figement du modèle est trop rigide tant que BF2 n'est pas tranché.

### MISSING_PREREQUISITES

- **Question 34.**&#x20;
  - Représentation du temps réel et correspondance avec le modèle (BF2), à placer dans RPE-02 ou dans une étape dédiée.
  - Runner temporisé fini qualifié en local, sans réseau, avec une horloge injectée (BF1). Il se place entre RPE-04 et RPE-05.
  - Racine de contrôle isolée et contrat de référence de l'expérience (NF4).

### AUTHORITY_LEAKAGE_CHECK

- **Question 35.** La carte n'accorde aucune autorité : tous ses drapeaux sont à false.
- Fuites latentes :&#x20;
  - l'état de contrôle réel de D4 n'est pas nommé dans la carte (NF4) ;
  - la configuration Git héritée de l'utilisateur (NF3) ;
  - la CI déclenchée par un push (NF5) ;
  - une autorité qui passerait hors du contrat, par un fichier voisin ou un drapeau du runner (NF1).

### CLAIM_SCOPE_CHECK

- La carte ne prétend aucune exécution et ne requalifie aucun composant existant.
- La formulation NB9 « runner timing » dépasse ce qu'aucune étape prévue ne produit (BF1).

### RECOMMENDED_NEXT_ACTION

Amender la carte de préparation, puis faire une revue delta courte. Concrètement :

1. Ajouter une étape « RUNNER TEMPORISÉ FINI » entre RPE-04 et RPE-05.
2. Étendre RPE-02, ou créer une étape dédiée, à la représentation du temps réel, et décider explicitement entre un modèle V0.2 et une couche de conversion qualifiée.
3. Ajouter les points NF1 à NF6 comme exigences des étapes concernées.
4. Optionnel : fusionner RPE-01 et RPE-02.

Cette revue ne crée aucune autorité. `REAL_P5E = CLOSED`.
# EXACT READINESS DIFF — V0.1 BASE TO V0.2 TECHNICAL HEAD
~~~~diff
diff --git a/reports/program/2026-10-02-OBSIDIAN-REAL-P5E-PRE-EXECUTION-READINESS-V0.2.md b/reports/program/2026-10-02-OBSIDIAN-REAL-P5E-PRE-EXECUTION-READINESS-V0.2.md
new file mode 100644
index 0000000..0ba9af1
--- /dev/null
+++ b/reports/program/2026-10-02-OBSIDIAN-REAL-P5E-PRE-EXECUTION-READINESS-V0.2.md
@@ -0,0 +1,448 @@
+# REAL P5-E ÔÇö PRE-EXECUTION READINESS V0.2
+
+Date: 2026-10-02
+
+## Purpose
+
+Amend V0.1 after external review `FAIL` without opening any implementation.
+
+V0.2 closes the two decomposition gaps:
+
+- BF1 ÔÇö missing finite timed runner;
+- BF2 ÔÇö missing qualified real-time evidence representation.
+
+It also incorporates NF1ÔåÆNF7 into the appropriate readiness stages.
+
+```text
+P5-E V0.1 CONTRACT + SYNTHETIC MODEL
+= QUALIFIED_AND_HUMAN_ADOPTED
+= UNCHANGED
+
+REAL P5-E
+= CLOSED
+
+RPE-01ÔåÆRPE-06
+= NOT OPENED
+```
+
+## Lineage
+
+Base checkpoint:
+`90189ac1ddddc8d81b12eeaa2a4241969a7dc405`
+
+V0.1 readiness:
+```text
+JSON   = 9ee1e02cf371cc990097af0ae6e31317ed083a69
+REPORT = 5434397e87fe0f204891d230b03832c625e01368
+```
+
+Internal V0.2 adjudication:
+`BF1/BF2 confirmed; NF1ÔåÆNF7 accepted as stage requirements.`
+## Corrected dependency architecture
+
+V0.1 incorrectly behaved like a total order and omitted one runtime layer.
+
+V0.2 uses the following DAG:
+
+```text
+                         RPE-01
+                  N4 GOVERNED CLOSED SCHEMA
+                       /                 \
+                      /                   \
+                     Ôåô                     Ôåô
+             RPE-02                        RPE-03
+      N5 + REAL-TIME                  NB5 ANCESTRY
+       REPRESENTATION                  CLASSIFIER
+                     \                   /
+                      \                 /
+                       Ôåô               Ôåô
+                          RPE-04
+                    NB2 + NB3 REAL
+                   OBSERVATION ADAPTER
+                             Ôåô
+                          RPE-05
+                    FINITE FIXED-RATE
+                       TIMED RUNNER
+                             Ôåô
+                          RPE-06
+                     NB9 CONTROLLED
+                 EXPERIMENT PREREGISTRATION
+                             Ôåô
+                 SEPARATE HUMAN EXECUTION
+                        AUTHORIZATION
+```
+
+Exact dependency edges:
+
+```text
+RPE-01 ÔåÆ RPE-02
+RPE-01 ÔåÆ RPE-03
+RPE-02 + RPE-03 ÔåÆ RPE-04
+RPE-04 ÔåÆ RPE-05
+RPE-01 + RPE-02 + RPE-03 + RPE-04 + RPE-05 ÔåÆ RPE-06
+```
+
+RPE-02 and RPE-03 may progress independently once RPE-01 is qualified.
+## RPE-01 ÔÇö N4 GOVERNED CLOSED SCHEMA
+
+### Why it comes first
+
+Future REAL P5-E artifacts will add configuration and authority surfaces.
+
+If the schema guard is not qualified first, authority can migrate from the adopted contract into:
+- adapter config;
+- runner config;
+- experiment preregistration;
+- evidence envelope.
+
+### Required protection
+
+The guard must operate on raw JSON bytes plus parsed structure.
+
+It must reject:
+- duplicate object member names before normal JSON dictionary construction;
+- unknown keys at every object depth;
+- wrong types;
+- boolean-as-integer laundering;
+- float-as-integer coercion;
+- duplicate normative list values;
+- unknown enum/list members;
+- normative list reordering where order matters.
+
+The guard and its schema specification must themselves be versioned and blob-bound.
+
+A change to the allowed schema is an amendment, not an incidental edit.
+
+### Exit criterion
+
+`ALL_SCHEMA_AND_ADDED_KEY_BREAKERS_REJECTED_WITHOUT_COVERED_OBJECT_BINDING_AS_THE_ONLY_DEFENSE`
+## RPE-02 ÔÇö N5 + REAL-TIME REPRESENTATION AND BOUNDARY FREEZE
+
+### BF2 correction
+
+The adopted synthetic model is intentionally integer-second and synthetic.
+
+It cannot safely serve as the raw real-time evidence model.
+
+V0.2 therefore separates:
+
+```text
+synthetic adopted semantics
+Ôëá
+raw real-time evidence representation
+```
+
+Preferred raw unit:
+`integer monotonic nanoseconds`
+
+Floating-point seconds are not the normative evidence format.
+
+Lossy truncation to seconds is forbidden for pass/fail classification.
+
+### Candidate evidence fields
+
+```text
+schedule_origin_ns
+scheduled_at_ns
+attempt_started_at_ns
+remote_observation_completed_at_ns
+attempt_completed_at_ns
+controlled_source_release_started_at_ns
+```
+
+These separate:
+- intended slot;
+- actual start;
+- remote evidence completion;
+- total local attempt completion.
+
+### Boundary decisions that must be frozen
+
+RPE-02 must explicitly decide and test:
+- release exactly on a slot;
+- release immediately after a slot;
+- first-slot ceiling rule;
+- permitted scheduler start lag or missed-slot rule;
+- completion exactly on next slot;
+- completion just after next slot;
+- completion equal to next attempt start;
+- true overlap;
+- exactly 60 seconds;
+- strictly greater than 60 seconds;
+- exact SHA format;
+- how remote-completion and full-attempt-completion interact.
+
+### Architecture decision
+
+RPE-02 begins with RED cases that expose the real/synthetic mismatch.
+
+Then choose between:
+
+A. qualified conservative conversion layer; or
+B. separate native real-time model V0.2.
+
+The adopted synthetic model is not modified unless a separately authorized future decision explicitly says so.
+## RPE-03 ÔÇö NB5 QUALIFIED ANCESTRY CLASSIFIER
+
+P5-D2 remains a deterministic consumer.
+
+RPE-03 removes caller authority over transition classification.
+
+### Verified object domain
+
+Before any ancestry claim:
+- no replace objects;
+- no shallow state;
+- no grafts;
+- both SHA identities resolve to commits;
+- missing objects fail to UNKNOWN;
+- timeout/corruption fail to UNKNOWN.
+
+### Classification
+
+```text
+no previous head
+ÔåÆ INITIAL
+
+same head
+ÔåÆ SAME
+
+merge-base --is-ancestor previous new
+exit 0
+ÔåÆ FAST_FORWARD
+
+exit 1 after both commits verified
+ÔåÆ NON_FAST_FORWARD
+
+anything else
+ÔåÆ UNKNOWN
+```
+
+Rollback and sibling divergence remain one D2 class:
+`NON_FAST_FORWARD`
+
+Optional sub-evidence may distinguish them, but cannot change D2 authority semantics.
+## RPE-04 ÔÇö NB2 + NB3 REAL OBSERVATION ADAPTER
+
+RPE-04 binds real remote evidence to RPE-03.
+
+### Preferred remote observation design
+
+One governed fetch transaction per attempt into an isolated namespace/object domain.
+
+This is preferred over:
+`ls-remote ÔåÆ independent fetch`
+
+because the latter creates two remote observations and a race between them.
+
+RPE-04 must still preregister exactly:
+- the fetch command;
+- the refspec;
+- how the observed SHA is extracted;
+- when remote observation completion is timestamped;
+- when total attempt completion is timestamped;
+- timeout behavior;
+- zero/multiple/unexpected-ref behavior;
+- namespace/object-domain lifecycle.
+
+### Git environment isolation
+
+Required:
+- pinned URL or equivalently governed verified remote config;
+- no inherited global/system config;
+- hooks disabled;
+- terminal prompt disabled;
+- explicit timeout;
+- no inherited `url.insteadOf`;
+- no canonical user worktree mutation.
+
+### Evidence semantics
+
+Only the exact SHA produced by the successful governed remote transaction is:
+
+`OBSERVED_REMOTE_TIP`
+
+A commit only discovered through history/ancestry is:
+
+`CONTENT_CONTAINED_NOT_OBSERVED`
+
+and cannot be queued as though it had been independently observed.
+## RPE-05 ÔÇö FINITE FIXED-RATE TIMED RUNNER
+
+This is the new BF1-closing stage missing from V0.1.
+
+### Qualification environment
+
+```text
+NO NETWORK
+INJECTED CLOCK
+INJECTED SLEEP
+FAKE ADAPTER
+```
+
+The runner must be fully qualifiable without GitHub.
+
+### Responsibilities
+
+The runner owns only:
+- fixed-rate scheduling;
+- finite horizon;
+- actual attempt start;
+- wait/sleep;
+- exactly one active attempt;
+- terminal stop.
+
+It consumes RPE-02 timing semantics and the RPE-04 adapter interface.
+
+It must prove:
+- 30-second anchored fixed-rate schedule;
+- no fixed-delay drift;
+- separate scheduled and actual start;
+- separate remote and total completion;
+- single active attempt;
+- no overlap;
+- exact late-start/overrun policy from RPE-02;
+- deterministic terminal reason;
+- deterministic STOP;
+- finite maximum horizon;
+- fail-closed adapter failure;
+- no implicit retry beyond schedule.
+
+It must not gain:
+- evaluation;
+- Stage A/B;
+- promotion;
+- publication;
+- Vault/CURRENT mutation;
+- queue coalescing;
+- retargeting;
+- daemon/service/startup authority.
+
+### Exit criterion
+
+`FINITE_FIXED_RATE_RUNNER_IS_DETERMINISTIC_FAIL_CLOSED_AND_QUALIFIED_WITHOUT_NETWORK`
+## RPE-06 ÔÇö NB9 CONTROLLED REAL EXPERIMENT PREREGISTRATION
+
+RPE-06 happens only after RPE-01ÔåÆRPE-05 are qualified.
+
+It remains a preregistration, not execution.
+
+### Experiment contract
+
+A sandbox experiment uses a different source from the adopted production source.
+
+Therefore it requires an explicit experiment contract.
+
+It must define:
+- exact repository URL;
+- exact experiment ref;
+- isolated producer clone;
+- isolated observer/control root;
+- claim boundary;
+- `p5d4_real_state_mutation_authorized = false`.
+
+### Clock domain
+
+For Pilot A:
+`SAME HOST = REQUIRED`
+
+Release recorder, runner and adapter must share one qualified monotonic clock domain.
+
+The pilot must invalidate itself if sleep/hibernation/suspend continuity is not proven.
+
+Current local observation only:
+Python reports `monotonic` as `QueryPerformanceCounter()`, monotonic, non-adjustable, reported resolution `1e-7 s`.
+
+That observation is not qualification and must be captured again during the actual RPE-02/RPE-06 qualification environment.
+
+### Push protocol
+
+Record:
+- target commit before release;
+- release-start monotonic time immediately before push;
+- push completion;
+- explicit refspec;
+- creation-only guard;
+- no force push.
+
+Minimum experiment classification:
+
+```text
+push success + observed within bound
+ÔåÆ VALID_PASS_CANDIDATE
+
+push success + not observed by bound
+ÔåÆ SLA_FAIL_CANDIDATE
+
+push failure + not observed
+ÔåÆ INVALID_EXPERIMENT
+
+push failure + target nevertheless observed
+ÔåÆ INCONCLUSIVE_OR_BLOCKED
+```
+
+Exact labels remain to be frozen in the preregistration.
+
+### Side-effect audit
+
+Before push, inspect:
+- workflows triggered by push;
+- branch/ref filters;
+- secret-bearing automation;
+- external side effects.
+
+Do not run a pilot whose side effects are not bounded.
+
+Preferred first surface:
+a dedicated sandbox repository or equivalently isolated experiment surface.
+
+Sandbox success does not qualify `integration/system-v1`-specific SLA.
+## Production-source gate after sandbox
+
+A later observation against `integration/system-v1` requires:
+
+- separate human authorization;
+- a legitimate governed update, not a dummy measurement commit;
+- target commit known before push;
+- explicit adjudication of real P5-D4 pending state and queue capacity;
+- production-specific evidence;
+- no inference that sandbox latency automatically equals production-branch latency.
+
+## Governance efficiency
+
+RPE-01 and RPE-02 may share a future macro-authorization only if:
+- preregistrations remain separate;
+- RED families remain separate;
+- RPE-01 is qualified before RPE-02 artifacts rely on its schema authority.
+
+RPE-03 remains a separate code/runtime qualification.
+
+## V0.2 readiness verdict
+
+```text
+BF1 = MAPPED_TO_RPE_05
+BF2 = MAPPED_TO_RPE_02
+
+NF1 = INTEGRATED_RPE_01
+NF2 = INTEGRATED_RPE_03
+NF3 = INTEGRATED_RPE_04
+NF4 = INTEGRATED_RPE_06
+NF5 = INTEGRATED_RPE_06
+NF6 = INTEGRATED_RPE_02_AND_RPE_06
+NF7 = INTEGRATED_AS_DAG
+
+RPE-01 = NOT OPENED
+RPE-02 = NOT OPENED
+RPE-03 = NOT OPENED
+RPE-04 = NOT OPENED
+RPE-05 = NOT OPENED
+RPE-06 = NOT OPENED
+
+REAL_P5E = CLOSED
+P6 = CLOSED
+```
+
+Next gate:
+external delta-review of this V0.2 readiness amendment.
+
+No implementation may begin before that review is adjudicated.
diff --git a/reports/program/2026-10-02-OBSIDIAN-REAL-P5E-READINESS-V0.2-INTERNAL-ADJUDICATION.md b/reports/program/2026-10-02-OBSIDIAN-REAL-P5E-READINESS-V0.2-INTERNAL-ADJUDICATION.md
new file mode 100644
index 0000000..d81ba88
--- /dev/null
+++ b/reports/program/2026-10-02-OBSIDIAN-REAL-P5E-READINESS-V0.2-INTERNAL-ADJUDICATION.md
@@ -0,0 +1,547 @@
+# REAL P5-E ÔÇö PRE-EXECUTION READINESS V0.2 ÔÇö INTERNAL ADJUDICATION
+
+Date: 2026-10-02
+
+## Opening identity
+
+Base checkpoint:
+`90189ac1ddddc8d81b12eeaa2a4241969a7dc405`
+
+Branch:
+`feat/obsidian-projection-real-p5e-pre-execution-readiness-v0.2-targeted-amendment`
+
+Opening worktree:
+`CLEAN`
+
+V0.1 readiness JSON:
+`9ee1e02cf371cc990097af0ae6e31317ed083a69`
+
+V0.1 readiness report:
+`5434397e87fe0f204891d230b03832c625e01368`
+
+Adopted P5-E contract:
+`43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9`
+
+Adopted P5-E synthetic model:
+`c0f16baa151c1466e30ba5778f1fca8184cd4aac`
+## External review result
+
+External verdict:
+`FAIL`
+
+The external review states that the general ordering is directionally correct, but two indispensable prerequisites are absent from the decomposition.
+
+Internal adjudication:
+
+```text
+BF1 = CONFIRMED_BLOCKING
+BF2 = CONFIRMED_BLOCKING
+
+NF1 = ACCEPTED_REQUIREMENT
+NF2 = ACCEPTED_REQUIREMENT
+NF3 = ACCEPTED_REQUIREMENT
+NF4 = ACCEPTED_REQUIREMENT
+NF5 = ACCEPTED_REQUIREMENT
+NF6 = ACCEPTED_REQUIREMENT
+NF7 = ACCEPTED_WITH_DAG_REFINEMENT
+```
+
+This adjudication does not authorize implementation.
+
+`REAL_P5E = CLOSED`
+## BF1 ÔÇö missing finite timed runner
+
+Verdict:
+`CONFIRMED_BLOCKING`
+
+V0.1 contains:
+- RPE-04 ÔÇö remote observation adapter;
+- RPE-05 ÔÇö real experiment preregistration.
+
+It does not contain the component that owns:
+- fixed-rate scheduling;
+- timer/sleep;
+- actual attempt start;
+- finite horizon;
+- single active attempt / single-writer timing discipline;
+- terminal-stop reasons;
+- scheduler stop.
+
+P5-D4 explicitly forbids time-based polling and sleep/timer in D4 and assigns near-real-time polling qualification to P5-E.
+
+Therefore the V0.1 claim that the future real experiment would qualify runner/transport/adapter timing was structurally incomplete.
+
+### V0.2 decision
+
+Add:
+
+`RPE-05 ÔÇö FINITE FIXED-RATE TIMED RUNNER`
+
+Move controlled real-experiment preregistration to:
+
+`RPE-06`
+
+RPE-05 must be qualified first without network using:
+- injected monotonic clock;
+- injected sleeper/wait primitive;
+- fake observation adapter;
+- deterministic terminal outcomes.
+
+No real GitHub polling is authorized by this amendment.
+## BF2 ÔÇö real-time evidence representation incompatible with adopted synthetic representation
+
+Verdict:
+`CONFIRMED_BLOCKING`
+
+Local reproduction on the adopted synthetic model confirmed:
+
+```text
+source_release_at_seconds = 1.37
+ÔåÆ P5ETimingModelError
+
+scheduled=30, completed=55
+ÔåÆ PASS latency 54
+ÔåÆ no actual-start field exists
+
+a real 60.4 second latency naively truncated to 60
+ÔåÆ can be misclassified as PASS
+```
+
+The adopted synthetic model is intentionally integer-second and synthetic.
+
+It must not silently become the real-time evidence representation.
+
+### V0.2 decision
+
+RPE-02 becomes:
+
+`N5 + REAL-TIME REPRESENTATION AND BOUNDARY FREEZE`
+
+The preferred real evidence representation is integer monotonic nanoseconds, not floating-point seconds and not truncated integer seconds.
+
+Candidate real evidence fields:
+
+```text
+schedule_origin_ns
+scheduled_at_ns
+attempt_started_at_ns
+remote_observation_completed_at_ns
+attempt_completed_at_ns
+controlled_source_release_started_at_ns
+```
+
+Exact field names remain preregistration candidates until RPE-02 is opened.
+
+The separation is normative:
+- `scheduled_at_ns` = intended fixed-rate slot;
+- `attempt_started_at_ns` = actual execution start;
+- `remote_observation_completed_at_ns` = completion of the remote operation that produced the observed remote-ref evidence;
+- `attempt_completed_at_ns` = completion of local materialization/classification/event construction.
+
+RPE-02 must decide, test-first, whether:
+1. a qualified conversion layer can preserve the adopted synthetic semantics; or
+2. a separate real-time model V0.2 is required.
+
+No choice is made by this readiness amendment beyond requiring that decision gate.
+## NF1 ÔÇö closed-schema hardening
+
+Verdict:
+`ACCEPTED_REQUIREMENT`
+
+RPE-01 must be strengthened beyond key-set equality on parsed dictionaries.
+
+Requirements:
+
+1. Reject duplicate JSON object member names during parsing, before dictionary construction.
+2. Close every object level of each governed JSON schema, not a selected subset.
+3. Enforce strict types:
+   - booleans are booleans;
+   - integers exclude booleans and float coercion;
+   - strings are exact strings;
+   - nullability is explicit.
+4. Freeze list vocabularies where list entries are normative enums.
+5. Enforce list uniqueness where duplicates would change or launder meaning.
+6. Freeze order where order is normative, including `real_end_to_end_stages`.
+7. Bind/version the schema guard itself by exact object identity.
+8. Treat any change to allowed-key sets or type/vocabulary rules as a governed amendment.
+9. Apply the same governed-schema discipline to future REAL P5-E JSON artifacts:
+   - adapter configuration;
+   - runner configuration;
+   - experiment preregistration;
+   - execution evidence envelopes.
+
+RPE-01 must therefore defend against authority moving from the adopted contract into an adjacent configuration file.
+## NF2 ÔÇö verified Git ancestry domain
+
+Verdict:
+`ACCEPTED_REQUIREMENT`
+
+RPE-03 ancestry classification may return FAST_FORWARD only from a controlled local Git object domain.
+
+Required domain conditions:
+
+- `GIT_NO_REPLACE_OBJECTS=1`;
+- no shallow repository state;
+- no `.git/info/grafts`;
+- both identities resolve to Git object type `commit`;
+- previous head missing from the object domain ÔåÆ UNKNOWN;
+- new head missing from the object domain ÔåÆ UNKNOWN;
+- timeout ÔåÆ UNKNOWN;
+- corruption ÔåÆ UNKNOWN;
+- any Git execution error other than the defined ancestry negative result ÔåÆ UNKNOWN.
+
+For:
+
+`git merge-base --is-ancestor PREVIOUS NEW`
+
+interpretation must be:
+
+```text
+exit 0 ÔåÆ FAST_FORWARD
+exit 1 ÔåÆ NON_FAST_FORWARD
+other  ÔåÆ UNKNOWN
+```
+
+only after both objects have independently passed commit-type/domain verification.
+
+Rollback and divergent sibling history share the top-level class NON_FAST_FORWARD.
+
+Optional sub-evidence may record rollback/divergence, but it must not alter D2's five-class authority surface.
+## NF3 ÔÇö remote observation transaction and Git environment
+
+Verdict:
+`ACCEPTED_REQUIREMENT`
+
+V0.2 prefers one controlled `git fetch` transaction for the observed ref into an isolated namespace/object domain rather than:
+`ls-remote ÔåÆ second independent fetch`.
+
+Reason:
+the single transaction reduces the race between the remote-ref observation and materialization of the corresponding objects.
+
+RPE-04 must preregister the exact Git command/environment before implementation.
+
+At minimum:
+
+- pinned remote URL, not an inherited symbolic remote name unless that remote config itself is governed and verified;
+- neutralize global/system Git configuration;
+- empty/disabled hooks path;
+- `GIT_TERMINAL_PROMPT=0`;
+- explicit timeout;
+- no inherited `url.*.insteadOf` authority;
+- no user hooks;
+- no canonical user worktree mutation;
+- fetch into an isolated namespace/object domain.
+
+The exact SHA evidenced by the successful controlled remote operation is the observed remote tip.
+
+Intermediate commits learned from its history are:
+`CONTENT_CONTAINED_NOT_OBSERVED`
+
+unless independently evidenced by another successful remote observation.
+
+If the exact advertised/observed SHA cannot be proven/materialized under the preregistered transaction semantics:
+`UNKNOWN / BLOCKED`
+
+rather than retargeting to a newer SHA.
+## NF4 ÔÇö experiment source contract and isolated state
+
+Verdict:
+`ACCEPTED_REQUIREMENT`
+
+A sandbox/ref experiment is not the adopted monitored source `integration/system-v1`.
+
+RPE-06 must therefore define a distinct experiment contract, not silently amend the adopted P5-E source identity.
+
+Mandatory:
+- experiment source identity;
+- remote URL/repository identity;
+- exact experiment ref;
+- separate claim boundary;
+- isolated experiment control root;
+- no reuse/mutation of the production P5-D4 control root;
+- explicit:
+  `p5d4_real_state_mutation_authorized = false`.
+
+A sandbox qualification may support:
+- runner timing;
+- adapter transaction semantics;
+- transport path;
+- evidence envelope.
+
+It may not qualify an SLA specific to `integration/system-v1`.
+## NF5 ÔÇö push outcome protocol and CI side effects
+
+Verdict:
+`ACCEPTED_REQUIREMENT`
+
+RPE-06 must freeze a push outcome matrix.
+
+Minimum semantics:
+
+```text
+push succeeds + target observed within bound
+ÔåÆ VALID_PASS_CANDIDATE
+
+push succeeds + target not observed by bound
+ÔåÆ SLA_FAIL_CANDIDATE
+
+push fails + target not observed
+ÔåÆ INVALID_EXPERIMENT
+
+push fails + target observed
+ÔåÆ INCONCLUSIVE_OR_BLOCKED
+```
+
+The exact final labels must be preregistered before execution.
+
+Push requirements for a new experiment ref:
+- explicit commit/refspec;
+- no force push;
+- creation-only semantics;
+- use a creation guard such as an explicit empty expected lease when technically validated;
+- record controlled release start before push;
+- record push completion;
+- preserve both timestamps as evidence.
+
+Before any real remote push:
+- audit repository workflows triggered by `push`;
+- identify branch filters;
+- identify any workflow capable of secret-bearing or external side effects;
+- do not execute if experiment-ref push side effects are not bounded.
+
+Preferred Pilot A:
+a dedicated sandbox repository or equivalently isolated experiment surface.
+
+A canonical ATDS branch must not be mutated solely to create a timing sample.
+## NF6 ÔÇö clock domain and host continuity
+
+Verdict:
+`ACCEPTED_REQUIREMENT`
+
+For the first real pilot:
+
+`SAME_HOST = REQUIRED`
+
+not merely preferred.
+
+Release recorder, timed runner, and observation adapter must use one process/host monotonic clock domain or a directly demonstrated equivalent in the same runtime environment.
+
+RPE-02 must record actual clock capability and precision during qualification.
+
+RPE-06 must define a fail-closed policy for:
+- sleep;
+- hibernation;
+- host suspend/resume;
+- clock-domain discontinuity or unverified continuity.
+
+The real pilot is invalid if host continuity cannot be established for the measurement window.
+
+No assumption about Windows sleep semantics of a particular clock source may be made without qualification evidence.
+## NF7 ÔÇö dependency order / governance cost
+
+Verdict:
+`ACCEPTED_WITH_DAG_REFINEMENT`
+
+The architecture must not be represented as a false total order.
+
+Dependency DAG:
+
+```text
+RPE-01 ÔÇö N4 GOVERNED CLOSED SCHEMA
+       Ôö£ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔåÆ RPE-02 ÔÇö N5 + REAL-TIME REPRESENTATION
+       Ôöé                         Ôöé
+       ÔööÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔåÆ RPE-03 ÔÇö NB5 ANCESTRY CLASSIFIER
+                                 Ôöé
+RPE-02 ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöñ
+                                 Ôåô
+                       RPE-04 ÔÇö NB2 + NB3
+                       REAL OBSERVATION ADAPTER
+                                 Ôåô
+                       RPE-05 ÔÇö FINITE TIMED RUNNER
+                                 Ôåô
+                       RPE-06 ÔÇö NB9
+                       CONTROLLED REAL EXPERIMENT
+                       PREREGISTRATION
+```
+
+More explicitly:
+
+```text
+RPE-01 ÔåÆ RPE-02
+RPE-01 ÔåÆ RPE-03
+RPE-02 + RPE-03 ÔåÆ RPE-04
+RPE-04 ÔåÆ RPE-05
+RPE-01 + RPE-02 + RPE-03 + RPE-04 + RPE-05 ÔåÆ RPE-06
+```
+
+RPE-01 and RPE-02 may later share one macro-authorization for efficiency only if:
+- their preregistrations remain separate;
+- their RED families remain separate;
+- RPE-01's schema guard is qualified before any RPE-02 governed artifact relies on it.
+
+RPE-03 remains a separate runtime/code qualification because it introduces new executable Git-graph logic.
+## RPE-05 ÔÇö finite fixed-rate timed runner requirement
+
+New blocker-closing stage.
+
+Purpose:
+provide the timing/scheduler authority explicitly delegated to P5-E but absent from V0.1.
+
+Initial qualification environment:
+`NO_NETWORK / INJECTED_CLOCK / INJECTED_SLEEP / FAKE_ADAPTER`
+
+Required properties:
+
+1. Fixed-rate schedule anchored to one origin, never fixed-delay drift.
+2. Interval target:
+   `30_000_000_000 ns`.
+3. Bound target:
+   `60_000_000_000 ns`.
+4. Separate:
+   - scheduled slot;
+   - actual attempt start;
+   - remote observation completion;
+   - total attempt completion.
+5. Exactly one active attempt.
+6. No overlapping observation operation.
+7. Late start is classified according to the exact RPE-02 policy.
+8. Previous attempt crossing a required slot is handled according to the exact RPE-02 policy.
+9. Finite maximum slots / finite terminal horizon.
+10. Terminal reason causes deterministic STOP.
+11. Injected adapter exception/network-equivalent failure becomes fail-closed evidence, not loop crash or implicit retry authority.
+12. No queue coalescing.
+13. No candidate retargeting.
+14. No evaluation authority.
+15. No Stage A/B authority.
+16. No promotion/publication/Vault/CURRENT authority.
+17. No daemon/service/startup registration authority.
+18. No real P5-D4 production control-state mutation.
+19. Scheduler state/evidence is isolated from production P5-D4 state.
+20. Runner can be fully qualified without network using deterministic fake-clock traces.
+
+RPE-05 does not itself authorize real polling.
+## RPE-02 decision gate ÔÇö conversion layer versus real-time model V0.2
+
+The readiness amendment does not choose implementation prematurely.
+
+RPE-02 must begin with RED cases that cannot be represented safely by the adopted integer-second synthetic model, including:
+
+- non-integer monotonic release;
+- non-integer attempt start;
+- non-integer remote completion;
+- latency just above 60 seconds;
+- actual start delayed from scheduled slot;
+- two-phase observation/classification completion.
+
+Then compare two candidate architectures:
+
+### Candidate A ÔÇö qualified conservative conversion layer
+
+Requirements:
+- real evidence stored losslessly in integer nanoseconds;
+- conversion to synthetic semantics only for parity/reference comparison;
+- no conversion result may turn a real >bound measurement into PASS;
+- conversion does not erase actual-start evidence;
+- real runner decisions are not based on lossy synthetic conversion.
+
+### Candidate B ÔÇö separate real-time model V0.2
+
+Requirements:
+- native integer-nanosecond representation;
+- explicit actual-start field;
+- explicit remote-completion and attempt-completion fields;
+- independently qualified parity against adopted synthetic semantics on the common exact-grid domain.
+
+Decision criterion:
+
+Choose the smallest architecture that can satisfy all RED cases without weakening conservative classification.
+
+No mutation of the adopted synthetic model is implied.
+## RPE-04 ÔÇö controlled single-fetch observation candidate
+
+Readiness preference:
+
+one governed fetch transaction per attempt into an isolated Git namespace.
+
+The future contract must answer before implementation:
+
+- exact command form;
+- how the ref's observed SHA is extracted;
+- whether SHA extraction is from fetch protocol evidence, isolated fetched ref, or another exact governed surface;
+- what timestamp constitutes remote observation completion;
+- what timestamp constitutes full attempt completion;
+- how timeout is represented;
+- how zero/multiple/unexpected ref results are represented;
+- how the isolated object domain is reset or retained between attempts;
+- how previous observed commits remain available for ancestry checks without inheriting untrusted Git configuration.
+
+If a two-read design is retained instead, it requires separate explicit justification and race semantics.
+
+No choice of Git command is executable authority at this readiness stage.
+## RPE-06 ÔÇö controlled experiment preregistration strengthened
+
+RPE-06 is now the final preregistration gate, not the runner qualification stage.
+
+It requires prior qualification of RPE-01 through RPE-05.
+
+It must define:
+
+- experiment contract distinct from production monitored-source contract;
+- sandbox repository/ref identity;
+- isolated producer clone;
+- isolated observer/control root;
+- exact release operation;
+- exact push refspec;
+- creation-only guard;
+- same-host monotonic clock domain;
+- release-start timestamp;
+- push-completion timestamp;
+- scheduled attempt timeline;
+- actual-start evidence;
+- remote observation completion evidence;
+- total attempt completion evidence;
+- push outcome matrix;
+- terminal experiment outcome matrix;
+- sleep/hibernate invalidation;
+- CI/workflow side-effect audit result;
+- cleanup policy and separate cleanup authority;
+- claim limits;
+- STOP conditions.
+
+RPE-06 may be human-adopted as a preregistration only.
+
+Actual execution still requires a separate one-shot human authorization.
+## Internal verdict
+
+```text
+REAL_P5E_READINESS_V0_1_EXTERNAL_REVIEW
+= FAIL
+
+BF1
+= CONFIRMED_BLOCKING_AND_MAPPED_TO_NEW_RPE_05
+
+BF2
+= CONFIRMED_BLOCKING_AND_MAPPED_TO_EXTENDED_RPE_02
+
+NF1_TO_NF6
+= ACCEPTED_AS_STAGE_REQUIREMENTS
+
+NF7
+= ACCEPTED_WITH_EXPLICIT_DAG
+
+P5E_V0_1_ADOPTED_CONTRACT
+= UNCHANGED
+
+P5E_V0_1_ADOPTED_SYNTHETIC_MODEL
+= UNCHANGED
+
+REAL_P5E
+= CLOSED
+```
+
+Next authorized work under the current amendment:
+- produce V0.2 machine-readable readiness map;
+- produce V0.2 human report;
+- produce self-contained external delta-review packet;
+- commit/push;
+- STOP before RPE-01.
diff --git a/tools/obsidian_projection/real_p5e_pre_execution_readiness_v0_2.json b/tools/obsidian_projection/real_p5e_pre_execution_readiness_v0_2.json
new file mode 100644
index 0000000..7708709
--- /dev/null
+++ b/tools/obsidian_projection/real_p5e_pre_execution_readiness_v0_2.json
@@ -0,0 +1,459 @@
+{
+  "schema": "ATDS_OBSIDIAN_REAL_P5E_PRE_EXECUTION_READINESS_V0_2",
+  "status": "TARGETED_AMENDMENT_CANDIDATE_FOR_EXTERNAL_DELTA_REVIEW",
+  "date": "2026-10-02",
+  "repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
+  "branch": "feat/obsidian-projection-real-p5e-pre-execution-readiness-v0.2-targeted-amendment",
+  "base_checkpoint": "90189ac1ddddc8d81b12eeaa2a4241969a7dc405",
+  "supersedes_readiness_v0_1": {
+    "json_blob": "9ee1e02cf371cc990097af0ae6e31317ed083a69",
+    "report_blob": "5434397e87fe0f204891d230b03832c625e01368",
+    "external_review_verdict": "FAIL",
+    "blocking_findings": ["BF1", "BF2"]
+  },
+  "authority": {
+    "purpose": "Close the decomposition gaps in REAL P5-E pre-execution readiness without implementing any prerequisite.",
+    "requirements_only": true,
+    "runtime_modification_authorized": false,
+    "adopted_p5e_contract_modification_authorized": false,
+    "adopted_synthetic_model_modification_authorized": false,
+    "schema_guard_implementation_authorized": false,
+    "real_time_model_or_conversion_implementation_authorized": false,
+    "ancestry_classifier_implementation_authorized": false,
+    "remote_adapter_implementation_authorized": false,
+    "timed_runner_implementation_authorized": false,
+    "real_remote_polling_authorized": false,
+    "experimental_push_authorized": false,
+    "real_head_evaluation_authorized": false,
+    "p5d4_real_state_mutation_authorized": false,
+    "vault_or_current_mutation_authorized": false,
+    "stage_a_authorized": false,
+    "stage_b_authorized": false,
+    "promotion_authorized": false,
+    "publication_authorized": false,
+    "daemon_or_service_registration_authorized": false,
+    "p6_authorized": false
+  },
+  "adopted_predecessor": {
+    "human_adjudication_blob": "76defeedea7ca7cff6af40534e479e7bc2bdd95a",
+    "contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
+    "synthetic_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
+    "state": "P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL_QUALIFIED_AND_HUMAN_ADOPTED",
+    "real_p5e": "CLOSED"
+  },
+  "external_review_adjudication": {
+    "BF1": {
+      "verdict": "CONFIRMED_BLOCKING",
+      "closure_location": "RPE-05",
+      "summary": "V0.1 had no qualified component owning fixed-rate timer/sleep, finite scheduling, single active attempt, and terminal STOP."
+    },
+    "BF2": {
+      "verdict": "CONFIRMED_BLOCKING",
+      "closure_location": "RPE-02",
+      "summary": "The adopted integer-second synthetic model is not a safe lossless representation of real monotonic timing evidence and has no actual-start field."
+    },
+    "NF1": "ACCEPTED_REQUIREMENT_RPE_01",
+    "NF2": "ACCEPTED_REQUIREMENT_RPE_03",
+    "NF3": "ACCEPTED_REQUIREMENT_RPE_04",
+    "NF4": "ACCEPTED_REQUIREMENT_RPE_06",
+    "NF5": "ACCEPTED_REQUIREMENT_RPE_06",
+    "NF6": "ACCEPTED_REQUIREMENT_RPE_02_AND_RPE_06",
+    "NF7": "ACCEPTED_WITH_DAG_REFINEMENT"
+  },
+  "non_normative_local_clock_observation": {
+    "purpose": "Example of evidence RPE-02/RPE-06 must capture again on the actual qualification environment; not a pilot qualification.",
+    "python_clock": "monotonic",
+    "implementation_observed": "QueryPerformanceCounter()",
+    "monotonic_observed": true,
+    "adjustable_observed": false,
+    "reported_resolution_seconds": 1e-7,
+    "normative_authority": "NONE"
+  },
+  "dependency_dag": {
+    "nodes": ["RPE-01", "RPE-02", "RPE-03", "RPE-04", "RPE-05", "RPE-06"],
+    "edges": [
+      ["RPE-01", "RPE-02"],
+      ["RPE-01", "RPE-03"],
+      ["RPE-02", "RPE-04"],
+      ["RPE-03", "RPE-04"],
+      ["RPE-04", "RPE-05"],
+      ["RPE-01", "RPE-06"],
+      ["RPE-02", "RPE-06"],
+      ["RPE-03", "RPE-06"],
+      ["RPE-04", "RPE-06"],
+      ["RPE-05", "RPE-06"]
+    ],
+    "notes": [
+      "RPE-02 and RPE-03 may proceed independently after RPE-01.",
+      "RPE-04 requires both real-time representation semantics and qualified ancestry classification.",
+      "RPE-05 consumes the qualified RPE-04 adapter interface but is first qualified with a fake adapter and injected time, without network.",
+      "RPE-06 is the final preregistration gate and requires RPE-01 through RPE-05."
+    ]
+  },
+  "stages": {
+    "RPE-01": {
+      "title": "N4_GOVERNED_CLOSED_SCHEMA",
+      "closes": ["N4", "NF1"],
+      "status": "NOT_OPENED",
+      "depends_on": [],
+      "purpose": "Prevent new authority, timing, queue, claim, or execution semantics from entering governed JSON through added or duplicate members, type coercion, list laundering, or adjacent configuration files.",
+      "preserve_adopted_contract_bytes_if_possible": true,
+      "requirements": {
+        "reject_duplicate_json_member_names_before_dictionary_construction": true,
+        "close_all_object_levels": true,
+        "strict_types": true,
+        "integer_must_exclude_boolean_and_float_coercion": true,
+        "normative_list_vocabularies_closed": true,
+        "normative_list_uniqueness_enforced": true,
+        "normative_list_order_frozen_where_required": true,
+        "real_end_to_end_stages_order_normative": true,
+        "schema_guard_itself_versioned_and_blob_bound": true,
+        "schema_change_requires_governed_amendment": true,
+        "future_real_p5e_json_artifacts_must_use_governed_schema_guard": [
+          "adapter_configuration",
+          "runner_configuration",
+          "experiment_preregistration",
+          "execution_evidence_envelope"
+        ]
+      },
+      "minimum_red_families": [
+        "duplicate authority key with contradictory first/last values",
+        "unknown authority key",
+        "unknown claim key",
+        "unknown timing key",
+        "unknown queue key",
+        "integer to float coercion",
+        "boolean where integer required",
+        "duplicate normative list member",
+        "unknown normative enum member",
+        "real_end_to_end_stages reorder",
+        "authority moved to adjacent governed config"
+      ],
+      "exit_criterion": "ALL_SCHEMA_AND_ADDED_KEY_BREAKERS_REJECTED_WITHOUT_RELYING_ON_COVERED_OBJECT_BINDING_ALONE"
+    },
+    "RPE-02": {
+      "title": "N5_PLUS_REAL_TIME_REPRESENTATION_AND_BOUNDARY_FREEZE",
+      "closes": ["N5", "BF2", "NF6_TIMING_CAPABILITY_PART"],
+      "status": "NOT_OPENED",
+      "depends_on": ["RPE-01"],
+      "purpose": "Define a lossless real-time evidence representation and freeze equality, rounding, actual-start, completion, and bound semantics before any real scheduler or adapter consumes them.",
+      "adopted_synthetic_model_remains_immutable_by_default": true,
+      "preferred_real_evidence_unit": "INTEGER_MONOTONIC_NANOSECONDS",
+      "floating_point_seconds_as_normative_evidence_forbidden": true,
+      "lossy_truncation_to_integer_seconds_for_real_pass_fail_forbidden": true,
+      "candidate_real_evidence_fields": [
+        "schedule_origin_ns",
+        "scheduled_at_ns",
+        "attempt_started_at_ns",
+        "remote_observation_completed_at_ns",
+        "attempt_completed_at_ns",
+        "controlled_source_release_started_at_ns"
+      ],
+      "field_semantics_to_freeze": {
+        "scheduled_at_ns": "planned fixed-rate slot",
+        "attempt_started_at_ns": "actual start of one observation attempt",
+        "remote_observation_completed_at_ns": "completion of the governed remote observation operation that produced the exact observed remote-ref evidence",
+        "attempt_completed_at_ns": "completion of local materialization, ancestry classification, and normalized event construction",
+        "controlled_source_release_started_at_ns": "same-host monotonic timestamp captured immediately before starting the separately authorized source release operation"
+      },
+      "boundary_rules_to_freeze": [
+        "release exactly on scheduled slot",
+        "release just after scheduled slot",
+        "first required slot ceiling rule",
+        "attempt actual-start delay relative to scheduled slot",
+        "maximum permitted start lag or explicit missed-slot rule",
+        "remote observation completion exactly on next slot",
+        "remote observation completion just after next slot",
+        "previous attempt completion exactly equal to next attempt start",
+        "previous attempt completion greater than next attempt start",
+        "latency exactly 60 seconds",
+        "latency strictly greater than 60 seconds",
+        "lowercase exact commit identity format",
+        "relationship between remote observation completion and full attempt completion"
+      ],
+      "clock_capability_evidence_required": [
+        "clock implementation",
+        "monotonic property",
+        "adjustable property",
+        "reported resolution",
+        "same process/host domain for compared timestamps"
+      ],
+      "mandatory_red_cases": [
+        "non-integer monotonic release",
+        "non-integer actual attempt start",
+        "non-integer remote completion",
+        "real latency just above 60 seconds",
+        "late actual start hidden behind on-time scheduled slot",
+        "two-phase remote-completion versus attempt-completion case"
+      ],
+      "architecture_decision_gate": {
+        "candidate_A": "QUALIFIED_CONSERVATIVE_CONVERSION_LAYER",
+        "candidate_B": "SEPARATE_REAL_TIME_MODEL_V0_2",
+        "decision_rule": "Choose the smallest architecture that passes all preregistered RED cases without weakening conservative classification.",
+        "candidate_A_constraints": [
+          "real evidence retained losslessly in integer nanoseconds",
+          "conversion used only for parity/reference comparison or explicitly qualified mapping",
+          "conversion may not turn real >bound into PASS",
+          "actual-start evidence may not be erased",
+          "real runner pass/fail may not depend on lossy conversion"
+        ],
+        "candidate_B_constraints": [
+          "native integer nanoseconds",
+          "explicit actual-start field",
+          "explicit remote-completion field",
+          "explicit full-attempt-completion field",
+          "parity qualification against adopted synthetic model on common exact-grid domain"
+        ]
+      },
+      "exit_criterion": "REAL_TIME_REPRESENTATION_AND_ALL_EQUALITY_ROUNDING_START_COMPLETION_BOUNDARIES_ARE_EXPLICITLY_CONTRACTED_AND_EXECUTABLY_QUALIFIED"
+    },
+    "RPE-03": {
+      "title": "NB5_QUALIFIED_ANCESTRY_CLASSIFIER",
+      "closes": ["NB5", "NF2"],
+      "status": "NOT_OPENED",
+      "depends_on": ["RPE-01"],
+      "purpose": "Remove caller authority over INITIAL/SAME/FAST_FORWARD/NON_FAST_FORWARD/UNKNOWN by deriving transition class from a controlled verified local Git object domain.",
+      "network_inside_classifier_forbidden": true,
+      "input": [
+        "previous_observed_head_or_null",
+        "new_exact_observed_head",
+        "verified_local_git_object_domain"
+      ],
+      "output": ["INITIAL", "SAME", "FAST_FORWARD", "NON_FAST_FORWARD", "UNKNOWN"],
+      "verified_domain_requirements": [
+        "GIT_NO_REPLACE_OBJECTS=1",
+        "repository is not shallow",
+        "no git info/grafts",
+        "previous object type commit when previous exists",
+        "new object type commit",
+        "previous missing -> UNKNOWN",
+        "new missing -> UNKNOWN",
+        "timeout -> UNKNOWN",
+        "corruption -> UNKNOWN"
+      ],
+      "ancestry_command_semantics": {
+        "command_family": "git merge-base --is-ancestor PREVIOUS NEW",
+        "exit_0": "FAST_FORWARD",
+        "exit_1": "NON_FAST_FORWARD",
+        "other_exit": "UNKNOWN"
+      },
+      "classification_rules": {
+        "no_previous_head": "INITIAL",
+        "same_exact_head": "SAME",
+        "verified_previous_is_ancestor_of_new": "FAST_FORWARD",
+        "verified_both_commits_previous_not_ancestor_of_new": "NON_FAST_FORWARD",
+        "unprovable_or_invalid_domain": "UNKNOWN"
+      },
+      "local_fixture_cases": [
+        "null to A",
+        "A to A",
+        "A to B fast-forward",
+        "B to A rollback",
+        "B and C divergent siblings",
+        "missing previous",
+        "missing new",
+        "non-commit object",
+        "replace-ref attempt",
+        "shallow repository",
+        "graft presence",
+        "timeout",
+        "corrupt repository"
+      ],
+      "exit_criterion": "TRANSITION_CLASS_IS_DERIVED_FROM_VERIFIED_LOCAL_GIT_GRAPH_AND_CANNOT_BE_CALLER_FORGED"
+    },
+    "RPE-04": {
+      "title": "NB2_NB3_REAL_REMOTE_OBSERVATION_ADAPTER",
+      "closes": ["NB2", "NB3", "NF3"],
+      "status": "NOT_OPENED",
+      "depends_on": ["RPE-02", "RPE-03"],
+      "purpose": "Convert one governed remote-ref observation into exact evidence plus independently derived ancestry without conflating observed tips with contained history.",
+      "initial_qualification_environment": "LOCAL_BARE_REMOTE_OR_INJECTED_REMOTE_IO_NO_GITHUB_POLLING",
+      "preferred_remote_transaction": "SINGLE_GOVERNED_FETCH_TO_ISOLATED_NAMESPACE",
+      "two_read_ls_remote_then_fetch": "REQUIRES_SEPARATE_JUSTIFICATION_AND_RACE_SEMANTICS_IF_RETAINED",
+      "git_environment_isolation": [
+        "pinned remote URL or equivalently governed verified remote configuration",
+        "neutralized global Git config",
+        "neutralized system Git config",
+        "empty or disabled hooks path",
+        "GIT_TERMINAL_PROMPT=0",
+        "explicit timeout",
+        "no inherited url.insteadOf authority",
+        "no canonical user worktree mutation",
+        "isolated ref namespace and object domain"
+      ],
+      "requirements": [
+        "one exact configured remote ref per attempt",
+        "zero/multiple/unexpected ref outcomes fail closed",
+        "exact lower-case 40-hex observed identity",
+        "remote observation completion timestamp uses RPE-02 representation",
+        "network/read failure emits fail-closed observation failure",
+        "exact observed commit materialized/proven in isolated domain",
+        "invoke only qualified RPE-03 ancestry classifier",
+        "emit normalized P5-D2 REMOTE_HEAD_OBSERVED event with derived transition class",
+        "only exact SHA evidenced by successful governed remote operation is OBSERVED_REMOTE_TIP",
+        "ancestry-enumerated commits are CONTENT_CONTAINED_NOT_OBSERVED",
+        "no intermediate commit injection without independent successful remote observation",
+        "unprovable exact observed SHA -> UNKNOWN/BLOCKED",
+        "no queue coalescing",
+        "no retargeting",
+        "no evaluation/promotion/publication/Vault authority"
+      ],
+      "transaction_questions_to_preregister": [
+        "exact fetch command/refspec",
+        "exact source of observed SHA evidence",
+        "timestamp point for remote observation completion",
+        "timestamp point for full attempt completion",
+        "timeout representation",
+        "isolated namespace lifecycle",
+        "object-domain retention across attempts"
+      ],
+      "exit_criterion": "ADAPTER_OUTPUT_IS_EXACT_GOVERNED_REMOTE_EVIDENCE_PLUS_QUALIFIED_ANCESTRY_WITH_NO_CALLER_SUPPLIED_CONTAINMENT_OR_TRANSITION_AUTHORITY"
+    },
+    "RPE-05": {
+      "title": "FINITE_FIXED_RATE_TIMED_RUNNER",
+      "closes": ["BF1"],
+      "status": "NOT_OPENED",
+      "depends_on": ["RPE-04"],
+      "purpose": "Qualify the finite P5-E timing/scheduler authority delegated away from P5-D4 before any network execution.",
+      "initial_qualification_environment": "NO_NETWORK_INJECTED_CLOCK_INJECTED_SLEEP_FAKE_ADAPTER",
+      "target_interval_ns": 30000000000,
+      "target_detection_bound_ns": 60000000000,
+      "required_properties": [
+        "fixed-rate schedule anchored to one origin",
+        "no fixed-delay drift",
+        "separate scheduled slot and actual attempt start",
+        "separate remote observation completion and total attempt completion",
+        "exactly one active attempt",
+        "no overlapping observation operation",
+        "late-start handling delegated to qualified RPE-02 policy",
+        "attempt-crossing-next-slot handling delegated to qualified RPE-02 policy",
+        "finite maximum slots or finite terminal horizon",
+        "deterministic terminal reason",
+        "terminal reason causes STOP",
+        "adapter exception or network-equivalent failure becomes fail-closed evidence",
+        "no implicit retry authority beyond preregistered schedule",
+        "no queue coalescing",
+        "no candidate retargeting",
+        "no evaluation authority",
+        "no Stage A/B authority",
+        "no promotion/publication/Vault/CURRENT authority",
+        "no daemon/service/startup registration",
+        "no production P5-D4 control-state mutation",
+        "runner state and evidence isolated from production P5-D4 state"
+      ],
+      "minimum_fake_clock_traces": [
+        "perfect on-time attempts",
+        "late start within chosen policy",
+        "late start beyond chosen policy",
+        "attempt completes exactly at next slot",
+        "attempt overruns next slot",
+        "adapter failure",
+        "terminal success",
+        "terminal latency failure",
+        "finite no-detection stop",
+        "sleep returns early",
+        "sleep returns late",
+        "clock discontinuity injected"
+      ],
+      "exit_criterion": "FINITE_FIXED_RATE_RUNNER_IS_DETERMINISTIC_FAIL_CLOSED_SINGLE_ACTIVE_ATTEMPT_AND_QUALIFIED_WITHOUT_NETWORK"
+    },
+    "RPE-06": {
+      "title": "NB9_CONTROLLED_REAL_EXPERIMENT_PREREGISTRATION",
+      "closes": ["NB9", "NF4", "NF5", "NF6_EXPERIMENT_PART"],
+      "status": "NOT_OPENED",
+      "depends_on": ["RPE-01", "RPE-02", "RPE-03", "RPE-04", "RPE-05"],
+      "purpose": "Define exactly one finite real-network experiment after every static/runtime prerequisite is qualified.",
+      "experiment_contract_must_be_distinct_from_adopted_production_source_contract": true,
+      "p5d4_real_state_mutation_authorized": false,
+      "same_host_same_monotonic_clock_domain_required": true,
+      "sleep_hibernation_suspend_resume_must_be_prevented_or_detected_and_invalidate_run": true,
+      "preferred_first_pilot_surface": "DEDICATED_SANDBOX_REPOSITORY_OR_EQUIVALENT_ISOLATED_EXPERIMENT_SURFACE",
+      "sandbox_claim_limit": "May qualify runner/transport/adapter timing path; may not qualify integration/system-v1-specific SLA.",
+      "required_identity_and_isolation": [
+        "exact experiment repository URL",
+        "exact experiment ref",
+        "isolated producer clone",
+        "isolated observer/control root",
+        "no production P5-D4 control-root reuse",
+        "explicit claim boundary"
+      ],
+      "release_and_push_evidence": [
+        "target commit precomputed before release",
+        "same-host controlled source release start monotonic timestamp captured immediately before starting push",
+        "push completion monotonic timestamp",
+        "explicit refspec",
+        "no force push",
+        "creation-only guard technically validated before use",
+        "separate cleanup authority",
+        "cleanup not implicitly authorized by execution authorization"
+      ],
+      "push_outcome_matrix_minimum": {
+        "push_success_target_observed_within_bound": "VALID_PASS_CANDIDATE",
+        "push_success_target_not_observed_by_bound": "SLA_FAIL_CANDIDATE",
+        "push_failure_target_not_observed": "INVALID_EXPERIMENT",
+        "push_failure_target_observed": "INCONCLUSIVE_OR_BLOCKED"
+      },
+      "pre_push_side_effect_audit": [
+        "GitHub Actions workflows triggered by push",
+        "branch/ref filters",
+        "secret-bearing workflows",
+        "external side effects",
+        "other automation triggered by experiment ref"
+      ],
+      "execution_evidence_required": [
+        "clock capability evidence",
+        "host continuity evidence",
+        "release-start timestamp",
+        "push-completion timestamp",
+        "scheduled slots",
+        "actual attempt starts",
+        "remote observation completions",
+        "attempt completions",
+        "exact observed heads",
+        "derived transition classes",
+        "terminal runner reason",
+        "push outcome",
+        "experiment verdict"
+      ],
+      "production_ref_gate_after_sandbox": {
+        "integration_system_v1_mutation_for_measurement_only_forbidden": true,
+        "separate_human_authorization_required": true,
+        "preferred_source_event": "separately authorized legitimate governed update with target commit known before push",
+        "production_ref_sla_claim_requires_own_evidence": true,
+        "production_p5d4_pending_state_and_queue_capacity_must_be_explicitly_adjudicated": true
+      },
+      "exit_criterion": "SELF_CONTAINED_HUMAN_ADOPTED_PREREGISTRATION_EXISTS_FOR_ONE_FINITE_REAL_EXPERIMENT_WITH_EXACT_SOURCE_CLOCK_PUSH_RUNNER_ADAPTER_EVIDENCE_AND_STOP_RULES"
+    }
+  },
+  "governance_efficiency": {
+    "rpe_01_and_rpe_02_may_share_future_macro_authorization": true,
+    "conditions": [
+      "separate preregistrations",
+      "separate RED families",
+      "RPE-01 schema guard qualified before any RPE-02 governed artifact relies on it"
+    ],
+    "rpe_03_must_remain_separate_runtime_qualification": true
+  },
+  "post_readiness_gate": {
+    "real_experiment_execution_authorized_by_this_map": false,
+    "required_before_real_experiment": [
+      "RPE-01 QUALIFIED",
+      "RPE-02 QUALIFIED",
+      "RPE-03 QUALIFIED",
+      "RPE-04 QUALIFIED",
+      "RPE-05 QUALIFIED",
+      "RPE-06 PREREGISTERED_AND_HUMAN_ADOPTED",
+      "separate one-shot human execution authorization"
+    ],
+    "mandatory_stop": true
+  },
+  "claim_boundary": {
+    "real_p5e_qualified": false,
+    "real_60_second_sla_qualified": false,
+    "integration_system_v1_sla_qualified": false,
+    "real_tip_visibility_adapter_qualified": false,
+    "ancestry_classifier_qualified": false,
+    "timed_runner_qualified": false,
+    "real_experiment_authorized": false
+  }
+}
~~~~

# SOURCE: READINESS V0.1 JSON
Path: tools/obsidian_projection/real_p5e_pre_execution_readiness_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_PRE_EXECUTION_READINESS_V0_1",
  "status": "CANDIDATE_REQUIREMENT_EXTRACTION_AND_BLOCKER_MAP",
  "date": "2026-10-02",
  "repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "branch": "feat/obsidian-projection-real-p5e-pre-execution-readiness-v0.1",
  "opening_head": "15047e3e60a7973b341bbb05b859cfa26ef71f3f",
  "authority": {
    "purpose": "Map and order the prerequisites that must close before any REAL P5-E preregistration or execution.",
    "requirements_only": true,
    "runtime_modification_authorized": false,
    "real_remote_polling_authorized": false,
    "real_head_evaluation_authorized": false,
    "vault_or_current_mutation_authorized": false,
    "stage_a_authorized": false,
    "stage_b_authorized": false,
    "promotion_authorized": false,
    "publication_authorized": false,
    "daemon_or_service_registration_authorized": false,
    "p6_authorized": false
  },
  "adopted_predecessor": {
    "human_adjudication_blob": "76defeedea7ca7cff6af40534e479e7bc2bdd95a",
    "contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
    "synthetic_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
    "state": "P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL_QUALIFIED_AND_HUMAN_ADOPTED",
    "real_p5e": "CLOSED"
  },
  "reusable_qualified_or_observed_surfaces": {
    "p5a_continuous_projection_contract": {
      "blob": "96ec1a768b8e9ff77d94bbcd36ee513678c258e6",
      "use": "remote source identity, read-only remote observation intent, 30s candidate poll / 60s target, isolated control checkout principle"
    },
    "p5d1_observer_core_contract": {
      "blob": "a20999ae991e07447e25ecd1592964f2d333449b",
      "use": "explicit transition classes and fail-closed NON_FAST_FORWARD/UNKNOWN semantics"
    },
    "p5d2_observer_tick": {
      "blob": "fd212f61ec38332b677110f40265638af55a73e2",
      "use": "deterministic normalized-event consumer; transition_class is caller supplied and is not independently proven"
    },
    "p5d4_bounded_loop_contract": {
      "blob": "6980de1eb55e49c0c2bd2f91620aeb75640753b6",
      "use": "injected observation_adapter boundary; real read-only Git permitted; timing/sleep explicitly deferred to P5-E"
    },
    "p5d4_bounded_loop_runtime": {
      "blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
      "use": "bounded orchestration only; no time scheduler; no real P5-E authority"
    },
    "p5d3f_real_remote_ref_pattern": {
      "blob": "9228ea75d269c9bfc89537374dec5990498c3e4a",
      "use": "existing proof pattern for exact git ls-remote --heads origin refs/heads/integration/system-v1 identity validation; not a qualified P5-E observation adapter"
    },
    "frozen_git_source": {
      "blob": "aef3a232980fa6ceb5253d38616419e41182162a",
      "use": "read-only access to an already frozen exact commit/tree/blob domain; not remote-ref observation or ancestry classification"
    }
  },
  "blockers": {
    "N4": {
      "title": "CLOSED_SCHEMA_AND_ADDED_KEY_HARDENING",
      "status": "OPEN_CONFIRMED",
      "failure_mode": "A future amendment can add a new authority/claim/timing/queue key and rebind object identity while existing semantic guards do not reject the new key.",
      "observed_evidence": [
        "authority_boundary.pending_head_evaluation_override=true survives current assert_contract_invariants",
        "claim_boundary.additional_current_claims=[P5E_REAL_END_TO_END_QUALIFIED] survives",
        "near_real_time_timing.poll_interval_seconds_override=300 survives",
        "queue_and_supersession.coalescing_authorized_v0_2=true survives"
      ],
      "recommended_closure": {
        "preserve_adopted_contract_bytes_if_possible": true,
        "artifact": "P5E_V0_1_CLOSED_SCHEMA_GUARD",
        "requirements": [
          "exact top-level key set",
          "exact key sets for every nested object used by current or future authority/claim/timing/queue logic",
          "unexpected keys fail closed independent of covered-object blob binding",
          "authority and claim lists reject duplicates and unknown enum members where applicable",
          "added-key adversarial sweep"
        ],
        "exit_criterion": "ALL_PREREGISTERED_ADDED_KEY_BREAKERS_REJECTED_WITH_OBJECT_BINDING_TESTS_EXCLUDED"
      },
      "dependencies": []
    },
    "N5": {
      "title": "EXACT_TIMING_AND_IDENTITY_BOUNDARY_FREEZE",
      "status": "OPEN_BEHAVIOR_EXISTS_NOT_FULLY_NORMATIVELY_FROZEN",
      "observed_current_behavior": {
        "source_release_exactly_on_slot_is_eligible": true,
        "source_release_non_aligned_31_first_required_slot": 60,
        "completion_exactly_on_next_slot_is_allowed": true,
        "previous_completion_equal_to_next_attempt_start_is_not_overlap": true,
        "completion_after_next_slot_is_blocked": "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT",
        "latency_equal_to_bound_is_eligible_for_pass": true,
        "uppercase_sha_is_rejected": true,
        "read_completion_before_attempt_start_is_blocked": true
      },
      "failure_mode": "Off-by-one or rounding changes can alter real SLA classification without changing the high-level 30s/60s contract.",
      "recommended_closure": {
        "preserve_synthetic_model_bytes_unless_a_test_exposes_inconsistency": true,
        "artifact": "REAL_P5E_TIMING_BOUNDARY_CONTRACT_V0_1",
        "tests_required": [
          "release exactly at 30 and 60",
          "release immediately after a slot / non-aligned release ceiling rule",
          "completion exactly at next fixed-rate slot",
          "completion one unit after next fixed-rate slot",
          "previous read completion exactly equals next attempt start",
          "previous read completion exceeds next attempt start",
          "latency exactly 60 versus greater than 60",
          "first required slot rounding",
          "lowercase exact SHA accepted and uppercase/malformed SHA rejected"
        ],
        "exit_criterion": "ALL_EQUALITY_AND_ROUNDING_BOUNDARIES_HAVE_EXPLICIT_CONTRACT_RULE_AND_EXECUTABLE_TEST"
      },
      "dependencies": ["N4"]
    },
    "NB5": {
      "title": "QUALIFIED_ANCESTRY_CLASSIFIER",
      "status": "OPEN_CONFIRMED",
      "failure_mode": "P5-D2 trusts caller-supplied INITIAL/SAME/FAST_FORWARD/NON_FAST_FORWARD/UNKNOWN and cannot prove whether that classification matches the Git graph.",
      "observed_evidence": [
        "Aâ†’Bâ†’A can be supplied to P5-D2 with the second A mislabeled FAST_FORWARD; P5-D2 accepts the class because classification is outside its authority.",
        "No qualified ancestry classifier exists under tools/obsidian_projection.",
        "A one-off merge-base use elsewhere in the repository is not qualified as an Obsidian P5-E component."
      ],
      "recommended_closure": {
        "artifact": "REAL_P5E_ANCESTRY_CLASSIFIER_V0_1",
        "network_inside_classifier_forbidden": true,
        "input": [
          "previous_observed_head_or_null",
          "new_exact_observed_head",
          "verified_local_git_object_domain"
        ],
        "output": [
          "INITIAL",
          "SAME",
          "FAST_FORWARD",
          "NON_FAST_FORWARD",
          "UNKNOWN"
        ],
        "classification_rules": {
          "no_previous_head": "INITIAL",
          "same_head": "SAME",
          "previous_is_ancestor_of_new": "FAST_FORWARD",
          "both_commits_verified_but_previous_is_not_ancestor_of_new": "NON_FAST_FORWARD",
          "missing_object_invalid_type_git_error_or_unprovable_relation": "UNKNOWN"
        },
        "local_fixture_cases": [
          "Aâ†’B fast-forward",
          "Bâ†’A rollback",
          "B and C divergent siblings",
          "same Aâ†’A",
          "initial nullâ†’A",
          "missing/unreadable commit object",
          "non-commit object"
        ],
        "exit_criterion": "CLASSIFICATION_IS_DERIVED_FROM_VERIFIED_GIT_GRAPH_AND_CANNOT_BE_CALLER_FORGED"
      },
      "dependencies": ["N4"]
    },
    "NB2_NB3": {
      "title": "REAL_REMOTE_OBSERVATION_ADAPTER_AND_TIP_VISIBILITY",
      "status": "OPEN_CONFIRMED",
      "failure_mode": "A real remote observation is not yet converted into a normalized P5-D2 event with independently proven ancestry; intermediate contained commits can otherwise be confused with actually observed remote tips.",
      "observed_evidence": [
        "P5-D4 already exposes an injected observation_adapter boundary and permits read-only Git outside P5-D2.",
        "P5-D3F contains an exact ls-remote ref validation pattern but does not emit P5-D2 events or classify ancestry.",
        "P5-E classify_tip_visibility is stateless and trusts caller-supplied fast_forward_contains_target."
      ],
      "recommended_closure": {
        "artifact": "REAL_P5E_REMOTE_OBSERVATION_ADAPTER_V0_1",
        "initial_qualification_environment": "LOCAL_BARE_REMOTE_OR_SYNTHETIC_NETWORK_ADAPTER_NO_REAL_GITHUB_POLLING",
        "requirements": [
          "read exactly one configured remote ref and validate exact ref plus lowercase 40-hex head",
          "record attempt-start and read-completion monotonic timestamps outside deterministic P5-D2 state",
          "network/read failure emits REMOTE_OBSERVATION_FAILED and cannot create a CURRENT claim",
          "same exact head emits SAME",
          "new exact observed head must be materialized/proven in isolated control Git object storage before ancestry classification",
          "invoke only the qualified NB5 ancestry classifier",
          "emit normalized P5-D2 REMOTE_HEAD_OBSERVED event with independently derived transition_class",
          "only the SHA returned by the successful remote read is an observed remote tip",
          "intermediate commits discovered by ancestry/history enumeration are CONTENT_CONTAINED_NOT_OBSERVED and must not be injected into the queue unless independently observed on a successful remote read",
          "exact-fetch/materialization race or inability to prove the observed SHA results in UNKNOWN/BLOCKED rather than retargeting to a newer head",
          "no canonical worktree mutation, no Vault mutation, no evaluation/promotion authority"
        ],
        "NB2_resolution_semantics": "Do not infer motive such as lag, rollback, or third-party push. Classify only the observed sequence and provable Git graph relation. A later observed head that is not a descendant of the previous observed head is NON_FAST_FORWARD; unprovable relation is UNKNOWN.",
        "NB3_resolution_semantics": "Observation and containment are distinct evidence classes. Containment never becomes exact tip observation.",
        "exit_criterion": "ADAPTER_OUTPUT_IS_EXACT_REMOTE_EVIDENCE_PLUS_QUALIFIED_ANCESTRY_WITH_NO_CALLER_SUPPLIED_CONTAINMENT_OR_TRANSITION_AUTHORITY"
      },
      "dependencies": ["NB5", "N5"]
    },
    "NB9": {
      "title": "CONTROLLED_REAL_EXPERIMENT_PROTOCOL",
      "status": "OPEN_CONFIRMED",
      "failure_mode": "There is no preregistered real protocol binding source release, observer schedule, clock domain, target ref, push authority, and read completion into one falsifiable real experiment.",
      "observed_evidence": [
        "P5-E adopted metric requires CONTROLLED_SOURCE_RELEASE_MONOTONIC â†’ SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC.",
        "No REAL P5-E observation adapter currently records that protocol.",
        "Existing time.monotonic uses elsewhere in Obsidian tooling do not qualify this P5-E experiment.",
        "Current authority forbids silent mutation of integration/system-v1."
      ],
      "recommended_closure": {
        "artifact": "REAL_P5E_CONTROLLED_EXPERIMENT_PREREGISTRATION_V0_1",
        "same_clock_domain_required": true,
        "same_host_preferred": true,
        "fixed_rate_schedule": {
          "interval_seconds": 30,
          "bound_seconds": 60,
          "attempt_start_and_completion_recorded_separately": true
        },
        "source_release_definition_candidate": "MONOTONIC_TIMESTAMP_CAPTURED_IMMEDIATELY_BEFORE_STARTING_THE_EXPLICITLY_AUTHORIZED_PUSH_OF_A_PRECOMPUTED_TARGET_COMMIT",
        "reason_for_release_definition": "Conservative and locally falsifiable; includes push transport time and cannot detect the target before the recorded release point without exposing an inconsistency.",
        "safest_first_real_experiment": {
          "remote_ref": "DEDICATED_EXPERIMENT_REF_NOT_INTEGRATION_SYSTEM_V1",
          "force_push_forbidden": true,
          "one_explicit_push_authorization_required": true,
          "target_commit_precomputed_before_release": true,
          "producer_clone_isolated_from_canonical_user_worktree": true,
          "remote_ref_deletion_not_implicitly_authorized": true,
          "claim_limit": "Qualifies runner/transport/adapter timing on the GitHub remote path but does not by itself qualify branch-specific production behavior for integration/system-v1."
        },
        "production_ref_gate_after_safe_experiment": {
          "integration_system_v1_mutation_may_not_be_created_only_for_measurement": true,
          "preferred_source_event": "A separately authorized legitimate governed update whose target commit is known before push.",
          "separate_human_authorization_required": true,
          "production_ref_sla_claim_requires_its_own_evidence": true
        },
        "forbidden": [
          "silent push to integration/system-v1",
          "force push",
          "using GitHub/server wall-clock as the normative measurement origin",
          "cross-host clocks without proven common monotonic domain",
          "real Vault/CURRENT mutation",
          "evaluation, promotion, publication",
          "daemon/startup/service registration"
        ],
        "exit_criterion": "A SELF_CONTAINED_PREREGISTRATION EXISTS_FOR_ONE_FINITE_REAL_EXPERIMENT_WITH_EXACT_REF_RELEASE_CLOCK_SCHEDULE_ADAPTER_AND_STOP_CONDITIONS"
      },
      "dependencies": ["N4", "N5", "NB5", "NB2_NB3"]
    }
  },
  "recommended_sequence": [
    {
      "id": "RPE-01",
      "closes": ["N4"],
      "name": "CLOSED_SCHEMA_GUARD",
      "reason": "Prevent future prerequisite amendments from creating new unguarded authority keys."
    },
    {
      "id": "RPE-02",
      "closes": ["N5"],
      "name": "TIMING_BOUNDARY_FREEZE",
      "reason": "Freeze exact equality/rounding semantics before any real scheduler or adapter consumes them."
    },
    {
      "id": "RPE-03",
      "closes": ["NB5"],
      "name": "ANCESTRY_CLASSIFIER",
      "reason": "Remove caller authority over FAST_FORWARD/NON_FAST_FORWARD/UNKNOWN before building the real adapter."
    },
    {
      "id": "RPE-04",
      "closes": ["NB2", "NB3"],
      "name": "REMOTE_OBSERVATION_ADAPTER",
      "reason": "Bind exact remote observation evidence to the qualified ancestry classifier and preserve observed-tip versus contained-content semantics."
    },
    {
      "id": "RPE-05",
      "closes": ["NB9"],
      "name": "CONTROLLED_REAL_EXPERIMENT_PREREGISTRATION",
      "reason": "Only after static/runtime prerequisites are qualified should a real network experiment be specified."
    }
  ],
  "post_readiness_gate": {
    "real_experiment_execution_authorized_by_this_map": false,
    "required_before_real_experiment": [
      "RPE-01 QUALIFIED",
      "RPE-02 QUALIFIED",
      "RPE-03 QUALIFIED",
      "RPE-04 QUALIFIED",
      "RPE-05 PREREGISTERED_AND_HUMAN_ADOPTED",
      "separate one-shot human execution authorization"
    ],
    "mandatory_stop": true
  }
}

~~~~

# SOURCE: READINESS V0.1 REPORT
Path: reports/program/2026-10-02-OBSIDIAN-REAL-P5E-PRE-EXECUTION-READINESS-V0.1.md
~~~~
# REAL P5-E â€” PRE-EXECUTION READINESS V0.1

Date: 2026-10-02

## Purpose

Transform the six retained prerequisites:

`N4 / N5 / NB2 / NB3 / NB5 / NB9`

into an executable closure order before any REAL P5-E preregistration or network execution.

This stage is requirements/readiness only.

```text
REAL P5-E = CLOSED
REAL HEAD EVALUATION = CLOSED
VAULT / CURRENT MUTATION = CLOSED
P6 = CLOSED
```

## Opening identity

Branch:
`feat/obsidian-projection-real-p5e-pre-execution-readiness-v0.1`

Opening HEAD:
`15047e3e60a7973b341bbb05b859cfa26ef71f3f`

Adopted P5-E human adjudication blob:
`76defeedea7ca7cff6af40534e479e7bc2bdd95a`

Adopted contract blob:
`43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9`

Adopted synthetic model blob:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`
## Executive blocker map

The six prerequisites should not be implemented as six unrelated workstreams.

Recommended dependency chain:

```text
RPE-01 â€” N4 CLOSED SCHEMA
        â†“
RPE-02 â€” N5 TIMING BOUNDARIES
        â†“
RPE-03 â€” NB5 ANCESTRY CLASSIFIER
        â†“
RPE-04 â€” NB2 + NB3 REAL OBSERVATION ADAPTER
        â†“
RPE-05 â€” NB9 CONTROLLED REAL EXPERIMENT PREREGISTRATION
        â†“
SEPARATE HUMAN AUTHORIZATION
        â†“
ONE FINITE REAL EXPERIMENT
```

This order minimizes rework because each later layer consumes the semantics frozen by the previous layer.

## VERIFIED â€” N4

Current P5-E invariant checks validate expected values but do not enforce a closed schema.

Read-only mutation probes confirmed that the following added keys survive current semantic invariants:

```text
authority_boundary.pending_head_evaluation_override = true
claim_boundary.additional_current_claims = ["P5E_REAL_END_TO_END_QUALIFIED"]
near_real_time_timing.poll_interval_seconds_override = 300
queue_and_supersession.coalescing_authorized_v0_2 = true
```

Therefore:

`N4 = OPEN_CONFIRMED`

The current blob binding detects byte drift, but it does not independently prevent a future amendment from intentionally rebinding a contract containing an unexpected authority key.

### Recommended closure

Do not rewrite the adopted contract merely to add schema metadata.

Prefer a separate closed-schema guard/verifier that:
- pins exact top-level and nested key sets;
- rejects unknown keys independently of blob binding;
- rejects unknown authority/claim enum members;
- rejects duplicates where list semantics require uniqueness.

Exit criterion:

`ADDED_KEY_BREAKERS = 0 survivors without relying on object-binding tests`
## VERIFIED â€” N5

The synthetic model currently behaves coherently, but the equality and rounding semantics are not fully frozen by dedicated contract language/tests.

Read-only probes of the adopted model produced:

```text
release exactly at 30 â†’ slot 30 eligible â†’ PASS latency 0
release exactly at 60 â†’ slot 60 eligible â†’ PASS latency 0
release at 31 â†’ first required slot 60 â†’ PASS latency 29

attempt 30 completing at 60 â†’ allowed
previous completion 60 and next attempt start 60 â†’ allowed / not overlap
attempt 30 completing at 61 â†’ BLOCKED ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT

uppercase SHA â†’ rejected
```

The current algorithm also uses:
- ceiling-to-grid for non-aligned release;
- `latency <= 60` as within bound;
- `previous_completed > next_scheduled` as overlap;
- `completed > scheduled + interval` as overrun.

Therefore:

`N5 = OPEN_BEHAVIOR_EXISTS_NOT_FULLY_NORMATIVELY_FROZEN`

### Recommended closure

Create a timing-boundary contract and dedicated tests around the unchanged adopted model first.

Freeze explicitly:
- equality at a poll slot;
- non-aligned release rounding;
- completion exactly on the next slot;
- completion one unit after;
- overlap equality versus strict exceedance;
- latency exactly 60 versus >60;
- lower-case exact SHA format.

Only change the model if the new tests expose an actual inconsistency.
## VERIFIED â€” NB5

P5-D2 is a deterministic consumer of a normalized event.

Its input requires an explicit:

`transition_class`

but P5-D2 does not prove that class against the Git graph.

A read-only probe demonstrated that an Aâ†’Bâ†’A sequence can be supplied with the second A mislabeled `FAST_FORWARD`; P5-D2 accepts the caller-provided class because classification is outside its authority.

Repository search found no qualified ancestry classifier under:

`tools/obsidian_projection`

A one-off `git merge-base --is-ancestor` use elsewhere in the repository does not constitute a qualified P5-E component.

Therefore:

`NB5 = OPEN_CONFIRMED`

### Recommended closure

Create a standalone ancestry classifier with no network access.

Inputs:
- previous observed head or null;
- new exact observed head;
- verified local Git object domain.

Outputs:
- INITIAL;
- SAME;
- FAST_FORWARD;
- NON_FAST_FORWARD;
- UNKNOWN.

Rules:
- no previous â†’ INITIAL;
- same SHA â†’ SAME;
- previous is ancestor of new â†’ FAST_FORWARD;
- both commits verified but previous is not ancestor of new â†’ NON_FAST_FORWARD;
- missing object, non-commit object, Git error, or unprovable relation â†’ UNKNOWN.

Qualify against a temporary local Git graph containing fast-forward, rollback, divergence, same, initial, missing-object, and non-commit cases.
## VERIFIED â€” NB2 + NB3

P5-D4 already exposes an injected `observation_adapter` boundary.

Its contract already establishes:
- remote I/O occurs outside P5-D2;
- real remote observation may use read-only Git;
- timing/sleep are not P5-D4 authority and belong to P5-E.

There is also a prior real-execution pattern that validates exactly:

`git ls-remote --heads origin refs/heads/integration/system-v1`

against an expected HEAD.

That pattern is useful evidence for exact remote-ref parsing, but it is not a P5-E observation adapter.

The adopted P5-E helper:

`classify_tip_visibility(..., fast_forward_contains_target=bool)`

is intentionally insufficient for real authority because containment is supplied by the caller.

Observed probe:

```text
caller supplies containment=true
â†’ CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED

caller supplies containment=false
â†’ UNRELATED_OR_UNPROVEN_REQUIRES_ADJUDICATION
```

Therefore:

`NB2 + NB3 = OPEN_CONFIRMED_AND_COUPLED`

### Recommended closure

Build one real-observation adapter only after NB5 is qualified.

Initial qualification should use a local bare Git remote or injected network fixture, not GitHub polling.

The adapter must:
1. read one exact configured remote ref;
2. validate the returned exact ref and lower-case 40-hex SHA;
3. record attempt start/completion monotonic timestamps outside P5-D2 state;
4. emit REMOTE_OBSERVATION_FAILED on read/network failure;
5. classify SAME directly;
6. for a changed SHA, prove/materialize the exact observed commit in isolated control storage;
7. invoke only the qualified ancestry classifier;
8. emit a normalized P5-D2 event with independently derived transition class;
9. treat only the SHA returned by the successful remote read as an observed remote tip;
10. never queue ancestry-enumerated intermediate commits unless independently observed.

NB2 should be resolved without guessing motive.

The system does not need to decide whether a Bâ†’A observation was caused by lag, rollback, or a third-party push. It needs only to prove the Git graph relation:
- descendant â†’ FAST_FORWARD;
- verified not-descendant â†’ NON_FAST_FORWARD;
- unprovable â†’ UNKNOWN.

NB3 is closed when exact tip observation and content containment become distinct runtime evidence classes rather than caller assertions.
## VERIFIED â€” NB9

The adopted timing metric requires:

```text
CONTROLLED_SOURCE_RELEASE_MONOTONIC
â†’
SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC
```

No current P5-E runtime records that real protocol.

Search confirms that other Obsidian tools use `time.monotonic()`, but those uses do not qualify P5-E timing.

No REAL P5-E adapter/scheduler exists yet.

Therefore:

`NB9 = OPEN_CONFIRMED`

### Recommended safest real-experiment protocol

Do not begin by mutating `integration/system-v1` solely for measurement.

First qualify one finite experiment on a dedicated experimental remote ref.

Candidate rules:

- precompute the target commit before release;
- isolated producer clone;
- force=false;
- one explicit human push authorization;
- capture the release monotonic timestamp immediately before starting the authorized push;
- observer and release recorder share the same host/monotonic clock domain;
- fixed-rate 30-second attempts;
- record start and completion separately;
- bound = 60 seconds;
- no evaluation, promotion, publication, Vault/CURRENT mutation;
- no daemon/service/startup registration;
- no implicit remote-ref deletion authority.

This first experiment can qualify the real runner/transport/adapter timing path, but it must not overclaim branch-specific production behavior for `integration/system-v1`.

A later production-ref claim should use a separately authorized legitimate governed update whose target commit is known before push. Do not create a meaningless canonical commit solely to satisfy a measurement.
## Reuse versus new construction

### Reuse

```text
P5-A
â†’ source identity
â†’ read-only Git intent
â†’ isolated checkout principle
â†’ candidate 30s / 60s target

P5-D1 / P5-D2
â†’ deterministic state machine
â†’ normalized event schema
â†’ fail-closed NON_FAST_FORWARD / UNKNOWN

P5-D4
â†’ bounded orchestration
â†’ injected observation adapter boundary
â†’ single-writer / persistent state discipline

P5-D3F real runner pattern
â†’ exact ls-remote ref validation pattern

FrozenGitSource
â†’ exact frozen commit/tree/blob reads after identity is already frozen
```

### New construction required

```text
RPE-01 closed-schema guard
RPE-02 timing-boundary freeze
RPE-03 qualified ancestry classifier
RPE-04 qualified real observation adapter
RPE-05 controlled real experiment preregistration
```

No existing component should be relabeled to pretend those five surfaces are already qualified.
## Recommended implementation sequence

### RPE-01 â€” CLOSED SCHEMA GUARD

Scope:
`N4 only`

Mode:
`CONTRACT_FIRST / TEST_FIRST / NO_RUNTIME_COUPLING`

STOP after qualification.

### RPE-02 â€” TIMING BOUNDARY FREEZE

Scope:
`N5 only`

Prefer tests/contract around unchanged model.

STOP after qualification.

### RPE-03 â€” ANCESTRY CLASSIFIER

Scope:
`NB5 only`

Use local finite Git fixtures.

No network.

STOP after qualification.

### RPE-04 â€” REAL OBSERVATION ADAPTER

Scope:
`NB2 + NB3`

First qualify against local bare remote/injected I/O.

No real GitHub polling.

STOP after qualification.

### RPE-05 â€” CONTROLLED REAL EXPERIMENT PREREGISTRATION

Scope:
`NB9 only`

Define exact release/ref/clock/schedule/stop protocol.

STOP before execution.

### Final execution gate

Only after RPE-01â†’RPE-05 are closed:

`ONE FINITE REAL P5-E EXPERIMENT`

requires a new explicit human authorization.

## Current verdict

```text
P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL
= QUALIFIED_AND_HUMAN_ADOPTED

REAL_P5E_PRE_EXECUTION_READINESS_MAP
= PRODUCED_CANDIDATE

RPE-01 = NOT_OPENED
RPE-02 = NOT_OPENED
RPE-03 = NOT_OPENED
RPE-04 = NOT_OPENED
RPE-05 = NOT_OPENED

REAL_P5E = CLOSED
P6 = CLOSED
```

The next decision should be review/adoption of this readiness ordering, not real execution.

~~~~

# SOURCE: READINESS V0.2 INTERNAL ADJUDICATION
Path: reports/program/2026-10-02-OBSIDIAN-REAL-P5E-READINESS-V0.2-INTERNAL-ADJUDICATION.md
~~~~
# REAL P5-E â€” PRE-EXECUTION READINESS V0.2 â€” INTERNAL ADJUDICATION

Date: 2026-10-02

## Opening identity

Base checkpoint:
`90189ac1ddddc8d81b12eeaa2a4241969a7dc405`

Branch:
`feat/obsidian-projection-real-p5e-pre-execution-readiness-v0.2-targeted-amendment`

Opening worktree:
`CLEAN`

V0.1 readiness JSON:
`9ee1e02cf371cc990097af0ae6e31317ed083a69`

V0.1 readiness report:
`5434397e87fe0f204891d230b03832c625e01368`

Adopted P5-E contract:
`43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9`

Adopted P5-E synthetic model:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`
## External review result

External verdict:
`FAIL`

The external review states that the general ordering is directionally correct, but two indispensable prerequisites are absent from the decomposition.

Internal adjudication:

```text
BF1 = CONFIRMED_BLOCKING
BF2 = CONFIRMED_BLOCKING

NF1 = ACCEPTED_REQUIREMENT
NF2 = ACCEPTED_REQUIREMENT
NF3 = ACCEPTED_REQUIREMENT
NF4 = ACCEPTED_REQUIREMENT
NF5 = ACCEPTED_REQUIREMENT
NF6 = ACCEPTED_REQUIREMENT
NF7 = ACCEPTED_WITH_DAG_REFINEMENT
```

This adjudication does not authorize implementation.

`REAL_P5E = CLOSED`
## BF1 â€” missing finite timed runner

Verdict:
`CONFIRMED_BLOCKING`

V0.1 contains:
- RPE-04 â€” remote observation adapter;
- RPE-05 â€” real experiment preregistration.

It does not contain the component that owns:
- fixed-rate scheduling;
- timer/sleep;
- actual attempt start;
- finite horizon;
- single active attempt / single-writer timing discipline;
- terminal-stop reasons;
- scheduler stop.

P5-D4 explicitly forbids time-based polling and sleep/timer in D4 and assigns near-real-time polling qualification to P5-E.

Therefore the V0.1 claim that the future real experiment would qualify runner/transport/adapter timing was structurally incomplete.

### V0.2 decision

Add:

`RPE-05 â€” FINITE FIXED-RATE TIMED RUNNER`

Move controlled real-experiment preregistration to:

`RPE-06`

RPE-05 must be qualified first without network using:
- injected monotonic clock;
- injected sleeper/wait primitive;
- fake observation adapter;
- deterministic terminal outcomes.

No real GitHub polling is authorized by this amendment.
## BF2 â€” real-time evidence representation incompatible with adopted synthetic representation

Verdict:
`CONFIRMED_BLOCKING`

Local reproduction on the adopted synthetic model confirmed:

```text
source_release_at_seconds = 1.37
â†’ P5ETimingModelError

scheduled=30, completed=55
â†’ PASS latency 54
â†’ no actual-start field exists

a real 60.4 second latency naively truncated to 60
â†’ can be misclassified as PASS
```

The adopted synthetic model is intentionally integer-second and synthetic.

It must not silently become the real-time evidence representation.

### V0.2 decision

RPE-02 becomes:

`N5 + REAL-TIME REPRESENTATION AND BOUNDARY FREEZE`

The preferred real evidence representation is integer monotonic nanoseconds, not floating-point seconds and not truncated integer seconds.

Candidate real evidence fields:

```text
schedule_origin_ns
scheduled_at_ns
attempt_started_at_ns
remote_observation_completed_at_ns
attempt_completed_at_ns
controlled_source_release_started_at_ns
```

Exact field names remain preregistration candidates until RPE-02 is opened.

The separation is normative:
- `scheduled_at_ns` = intended fixed-rate slot;
- `attempt_started_at_ns` = actual execution start;
- `remote_observation_completed_at_ns` = completion of the remote operation that produced the observed remote-ref evidence;
- `attempt_completed_at_ns` = completion of local materialization/classification/event construction.

RPE-02 must decide, test-first, whether:
1. a qualified conversion layer can preserve the adopted synthetic semantics; or
2. a separate real-time model V0.2 is required.

No choice is made by this readiness amendment beyond requiring that decision gate.
## NF1 â€” closed-schema hardening

Verdict:
`ACCEPTED_REQUIREMENT`

RPE-01 must be strengthened beyond key-set equality on parsed dictionaries.

Requirements:

1. Reject duplicate JSON object member names during parsing, before dictionary construction.
2. Close every object level of each governed JSON schema, not a selected subset.
3. Enforce strict types:
   - booleans are booleans;
   - integers exclude booleans and float coercion;
   - strings are exact strings;
   - nullability is explicit.
4. Freeze list vocabularies where list entries are normative enums.
5. Enforce list uniqueness where duplicates would change or launder meaning.
6. Freeze order where order is normative, including `real_end_to_end_stages`.
7. Bind/version the schema guard itself by exact object identity.
8. Treat any change to allowed-key sets or type/vocabulary rules as a governed amendment.
9. Apply the same governed-schema discipline to future REAL P5-E JSON artifacts:
   - adapter configuration;
   - runner configuration;
   - experiment preregistration;
   - execution evidence envelopes.

RPE-01 must therefore defend against authority moving from the adopted contract into an adjacent configuration file.
## NF2 â€” verified Git ancestry domain

Verdict:
`ACCEPTED_REQUIREMENT`

RPE-03 ancestry classification may return FAST_FORWARD only from a controlled local Git object domain.

Required domain conditions:

- `GIT_NO_REPLACE_OBJECTS=1`;
- no shallow repository state;
- no `.git/info/grafts`;
- both identities resolve to Git object type `commit`;
- previous head missing from the object domain â†’ UNKNOWN;
- new head missing from the object domain â†’ UNKNOWN;
- timeout â†’ UNKNOWN;
- corruption â†’ UNKNOWN;
- any Git execution error other than the defined ancestry negative result â†’ UNKNOWN.

For:

`git merge-base --is-ancestor PREVIOUS NEW`

interpretation must be:

```text
exit 0 â†’ FAST_FORWARD
exit 1 â†’ NON_FAST_FORWARD
other  â†’ UNKNOWN
```

only after both objects have independently passed commit-type/domain verification.

Rollback and divergent sibling history share the top-level class NON_FAST_FORWARD.

Optional sub-evidence may record rollback/divergence, but it must not alter D2's five-class authority surface.
## NF3 â€” remote observation transaction and Git environment

Verdict:
`ACCEPTED_REQUIREMENT`

V0.2 prefers one controlled `git fetch` transaction for the observed ref into an isolated namespace/object domain rather than:
`ls-remote â†’ second independent fetch`.

Reason:
the single transaction reduces the race between the remote-ref observation and materialization of the corresponding objects.

RPE-04 must preregister the exact Git command/environment before implementation.

At minimum:

- pinned remote URL, not an inherited symbolic remote name unless that remote config itself is governed and verified;
- neutralize global/system Git configuration;
- empty/disabled hooks path;
- `GIT_TERMINAL_PROMPT=0`;
- explicit timeout;
- no inherited `url.*.insteadOf` authority;
- no user hooks;
- no canonical user worktree mutation;
- fetch into an isolated namespace/object domain.

The exact SHA evidenced by the successful controlled remote operation is the observed remote tip.

Intermediate commits learned from its history are:
`CONTENT_CONTAINED_NOT_OBSERVED`

unless independently evidenced by another successful remote observation.

If the exact advertised/observed SHA cannot be proven/materialized under the preregistered transaction semantics:
`UNKNOWN / BLOCKED`

rather than retargeting to a newer SHA.
## NF4 â€” experiment source contract and isolated state

Verdict:
`ACCEPTED_REQUIREMENT`

A sandbox/ref experiment is not the adopted monitored source `integration/system-v1`.

RPE-06 must therefore define a distinct experiment contract, not silently amend the adopted P5-E source identity.

Mandatory:
- experiment source identity;
- remote URL/repository identity;
- exact experiment ref;
- separate claim boundary;
- isolated experiment control root;
- no reuse/mutation of the production P5-D4 control root;
- explicit:
  `p5d4_real_state_mutation_authorized = false`.

A sandbox qualification may support:
- runner timing;
- adapter transaction semantics;
- transport path;
- evidence envelope.

It may not qualify an SLA specific to `integration/system-v1`.
## NF5 â€” push outcome protocol and CI side effects

Verdict:
`ACCEPTED_REQUIREMENT`

RPE-06 must freeze a push outcome matrix.

Minimum semantics:

```text
push succeeds + target observed within bound
â†’ VALID_PASS_CANDIDATE

push succeeds + target not observed by bound
â†’ SLA_FAIL_CANDIDATE

push fails + target not observed
â†’ INVALID_EXPERIMENT

push fails + target observed
â†’ INCONCLUSIVE_OR_BLOCKED
```

The exact final labels must be preregistered before execution.

Push requirements for a new experiment ref:
- explicit commit/refspec;
- no force push;
- creation-only semantics;
- use a creation guard such as an explicit empty expected lease when technically validated;
- record controlled release start before push;
- record push completion;
- preserve both timestamps as evidence.

Before any real remote push:
- audit repository workflows triggered by `push`;
- identify branch filters;
- identify any workflow capable of secret-bearing or external side effects;
- do not execute if experiment-ref push side effects are not bounded.

Preferred Pilot A:
a dedicated sandbox repository or equivalently isolated experiment surface.

A canonical ATDS branch must not be mutated solely to create a timing sample.
## NF6 â€” clock domain and host continuity

Verdict:
`ACCEPTED_REQUIREMENT`

For the first real pilot:

`SAME_HOST = REQUIRED`

not merely preferred.

Release recorder, timed runner, and observation adapter must use one process/host monotonic clock domain or a directly demonstrated equivalent in the same runtime environment.

RPE-02 must record actual clock capability and precision during qualification.

RPE-06 must define a fail-closed policy for:
- sleep;
- hibernation;
- host suspend/resume;
- clock-domain discontinuity or unverified continuity.

The real pilot is invalid if host continuity cannot be established for the measurement window.

No assumption about Windows sleep semantics of a particular clock source may be made without qualification evidence.
## NF7 â€” dependency order / governance cost

Verdict:
`ACCEPTED_WITH_DAG_REFINEMENT`

The architecture must not be represented as a false total order.

Dependency DAG:

```text
RPE-01 â€” N4 GOVERNED CLOSED SCHEMA
       â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â†’ RPE-02 â€” N5 + REAL-TIME REPRESENTATION
       â”‚                         â”‚
       â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â†’ RPE-03 â€” NB5 ANCESTRY CLASSIFIER
                                 â”‚
RPE-02 â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
                                 â†“
                       RPE-04 â€” NB2 + NB3
                       REAL OBSERVATION ADAPTER
                                 â†“
                       RPE-05 â€” FINITE TIMED RUNNER
                                 â†“
                       RPE-06 â€” NB9
                       CONTROLLED REAL EXPERIMENT
                       PREREGISTRATION
```

More explicitly:

```text
RPE-01 â†’ RPE-02
RPE-01 â†’ RPE-03
RPE-02 + RPE-03 â†’ RPE-04
RPE-04 â†’ RPE-05
RPE-01 + RPE-02 + RPE-03 + RPE-04 + RPE-05 â†’ RPE-06
```

RPE-01 and RPE-02 may later share one macro-authorization for efficiency only if:
- their preregistrations remain separate;
- their RED families remain separate;
- RPE-01's schema guard is qualified before any RPE-02 governed artifact relies on it.

RPE-03 remains a separate runtime/code qualification because it introduces new executable Git-graph logic.
## RPE-05 â€” finite fixed-rate timed runner requirement

New blocker-closing stage.

Purpose:
provide the timing/scheduler authority explicitly delegated to P5-E but absent from V0.1.

Initial qualification environment:
`NO_NETWORK / INJECTED_CLOCK / INJECTED_SLEEP / FAKE_ADAPTER`

Required properties:

1. Fixed-rate schedule anchored to one origin, never fixed-delay drift.
2. Interval target:
   `30_000_000_000 ns`.
3. Bound target:
   `60_000_000_000 ns`.
4. Separate:
   - scheduled slot;
   - actual attempt start;
   - remote observation completion;
   - total attempt completion.
5. Exactly one active attempt.
6. No overlapping observation operation.
7. Late start is classified according to the exact RPE-02 policy.
8. Previous attempt crossing a required slot is handled according to the exact RPE-02 policy.
9. Finite maximum slots / finite terminal horizon.
10. Terminal reason causes deterministic STOP.
11. Injected adapter exception/network-equivalent failure becomes fail-closed evidence, not loop crash or implicit retry authority.
12. No queue coalescing.
13. No candidate retargeting.
14. No evaluation authority.
15. No Stage A/B authority.
16. No promotion/publication/Vault/CURRENT authority.
17. No daemon/service/startup registration authority.
18. No real P5-D4 production control-state mutation.
19. Scheduler state/evidence is isolated from production P5-D4 state.
20. Runner can be fully qualified without network using deterministic fake-clock traces.

RPE-05 does not itself authorize real polling.
## RPE-02 decision gate â€” conversion layer versus real-time model V0.2

The readiness amendment does not choose implementation prematurely.

RPE-02 must begin with RED cases that cannot be represented safely by the adopted integer-second synthetic model, including:

- non-integer monotonic release;
- non-integer attempt start;
- non-integer remote completion;
- latency just above 60 seconds;
- actual start delayed from scheduled slot;
- two-phase observation/classification completion.

Then compare two candidate architectures:

### Candidate A â€” qualified conservative conversion layer

Requirements:
- real evidence stored losslessly in integer nanoseconds;
- conversion to synthetic semantics only for parity/reference comparison;
- no conversion result may turn a real >bound measurement into PASS;
- conversion does not erase actual-start evidence;
- real runner decisions are not based on lossy synthetic conversion.

### Candidate B â€” separate real-time model V0.2

Requirements:
- native integer-nanosecond representation;
- explicit actual-start field;
- explicit remote-completion and attempt-completion fields;
- independently qualified parity against adopted synthetic semantics on the common exact-grid domain.

Decision criterion:

Choose the smallest architecture that can satisfy all RED cases without weakening conservative classification.

No mutation of the adopted synthetic model is implied.
## RPE-04 â€” controlled single-fetch observation candidate

Readiness preference:

one governed fetch transaction per attempt into an isolated Git namespace.

The future contract must answer before implementation:

- exact command form;
- how the ref's observed SHA is extracted;
- whether SHA extraction is from fetch protocol evidence, isolated fetched ref, or another exact governed surface;
- what timestamp constitutes remote observation completion;
- what timestamp constitutes full attempt completion;
- how timeout is represented;
- how zero/multiple/unexpected ref results are represented;
- how the isolated object domain is reset or retained between attempts;
- how previous observed commits remain available for ancestry checks without inheriting untrusted Git configuration.

If a two-read design is retained instead, it requires separate explicit justification and race semantics.

No choice of Git command is executable authority at this readiness stage.
## RPE-06 â€” controlled experiment preregistration strengthened

RPE-06 is now the final preregistration gate, not the runner qualification stage.

It requires prior qualification of RPE-01 through RPE-05.

It must define:

- experiment contract distinct from production monitored-source contract;
- sandbox repository/ref identity;
- isolated producer clone;
- isolated observer/control root;
- exact release operation;
- exact push refspec;
- creation-only guard;
- same-host monotonic clock domain;
- release-start timestamp;
- push-completion timestamp;
- scheduled attempt timeline;
- actual-start evidence;
- remote observation completion evidence;
- total attempt completion evidence;
- push outcome matrix;
- terminal experiment outcome matrix;
- sleep/hibernate invalidation;
- CI/workflow side-effect audit result;
- cleanup policy and separate cleanup authority;
- claim limits;
- STOP conditions.

RPE-06 may be human-adopted as a preregistration only.

Actual execution still requires a separate one-shot human authorization.
## Internal verdict

```text
REAL_P5E_READINESS_V0_1_EXTERNAL_REVIEW
= FAIL

BF1
= CONFIRMED_BLOCKING_AND_MAPPED_TO_NEW_RPE_05

BF2
= CONFIRMED_BLOCKING_AND_MAPPED_TO_EXTENDED_RPE_02

NF1_TO_NF6
= ACCEPTED_AS_STAGE_REQUIREMENTS

NF7
= ACCEPTED_WITH_EXPLICIT_DAG

P5E_V0_1_ADOPTED_CONTRACT
= UNCHANGED

P5E_V0_1_ADOPTED_SYNTHETIC_MODEL
= UNCHANGED

REAL_P5E
= CLOSED
```

Next authorized work under the current amendment:
- produce V0.2 machine-readable readiness map;
- produce V0.2 human report;
- produce self-contained external delta-review packet;
- commit/push;
- STOP before RPE-01.

~~~~

# SOURCE: READINESS V0.2 JSON
Path: tools/obsidian_projection/real_p5e_pre_execution_readiness_v0_2.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_PRE_EXECUTION_READINESS_V0_2",
  "status": "TARGETED_AMENDMENT_CANDIDATE_FOR_EXTERNAL_DELTA_REVIEW",
  "date": "2026-10-02",
  "repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "branch": "feat/obsidian-projection-real-p5e-pre-execution-readiness-v0.2-targeted-amendment",
  "base_checkpoint": "90189ac1ddddc8d81b12eeaa2a4241969a7dc405",
  "supersedes_readiness_v0_1": {
    "json_blob": "9ee1e02cf371cc990097af0ae6e31317ed083a69",
    "report_blob": "5434397e87fe0f204891d230b03832c625e01368",
    "external_review_verdict": "FAIL",
    "blocking_findings": ["BF1", "BF2"]
  },
  "authority": {
    "purpose": "Close the decomposition gaps in REAL P5-E pre-execution readiness without implementing any prerequisite.",
    "requirements_only": true,
    "runtime_modification_authorized": false,
    "adopted_p5e_contract_modification_authorized": false,
    "adopted_synthetic_model_modification_authorized": false,
    "schema_guard_implementation_authorized": false,
    "real_time_model_or_conversion_implementation_authorized": false,
    "ancestry_classifier_implementation_authorized": false,
    "remote_adapter_implementation_authorized": false,
    "timed_runner_implementation_authorized": false,
    "real_remote_polling_authorized": false,
    "experimental_push_authorized": false,
    "real_head_evaluation_authorized": false,
    "p5d4_real_state_mutation_authorized": false,
    "vault_or_current_mutation_authorized": false,
    "stage_a_authorized": false,
    "stage_b_authorized": false,
    "promotion_authorized": false,
    "publication_authorized": false,
    "daemon_or_service_registration_authorized": false,
    "p6_authorized": false
  },
  "adopted_predecessor": {
    "human_adjudication_blob": "76defeedea7ca7cff6af40534e479e7bc2bdd95a",
    "contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
    "synthetic_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
    "state": "P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL_QUALIFIED_AND_HUMAN_ADOPTED",
    "real_p5e": "CLOSED"
  },
  "external_review_adjudication": {
    "BF1": {
      "verdict": "CONFIRMED_BLOCKING",
      "closure_location": "RPE-05",
      "summary": "V0.1 had no qualified component owning fixed-rate timer/sleep, finite scheduling, single active attempt, and terminal STOP."
    },
    "BF2": {
      "verdict": "CONFIRMED_BLOCKING",
      "closure_location": "RPE-02",
      "summary": "The adopted integer-second synthetic model is not a safe lossless representation of real monotonic timing evidence and has no actual-start field."
    },
    "NF1": "ACCEPTED_REQUIREMENT_RPE_01",
    "NF2": "ACCEPTED_REQUIREMENT_RPE_03",
    "NF3": "ACCEPTED_REQUIREMENT_RPE_04",
    "NF4": "ACCEPTED_REQUIREMENT_RPE_06",
    "NF5": "ACCEPTED_REQUIREMENT_RPE_06",
    "NF6": "ACCEPTED_REQUIREMENT_RPE_02_AND_RPE_06",
    "NF7": "ACCEPTED_WITH_DAG_REFINEMENT"
  },
  "non_normative_local_clock_observation": {
    "purpose": "Example of evidence RPE-02/RPE-06 must capture again on the actual qualification environment; not a pilot qualification.",
    "python_clock": "monotonic",
    "implementation_observed": "QueryPerformanceCounter()",
    "monotonic_observed": true,
    "adjustable_observed": false,
    "reported_resolution_seconds": 1e-7,
    "normative_authority": "NONE"
  },
  "dependency_dag": {
    "nodes": ["RPE-01", "RPE-02", "RPE-03", "RPE-04", "RPE-05", "RPE-06"],
    "edges": [
      ["RPE-01", "RPE-02"],
      ["RPE-01", "RPE-03"],
      ["RPE-02", "RPE-04"],
      ["RPE-03", "RPE-04"],
      ["RPE-04", "RPE-05"],
      ["RPE-01", "RPE-06"],
      ["RPE-02", "RPE-06"],
      ["RPE-03", "RPE-06"],
      ["RPE-04", "RPE-06"],
      ["RPE-05", "RPE-06"]
    ],
    "notes": [
      "RPE-02 and RPE-03 may proceed independently after RPE-01.",
      "RPE-04 requires both real-time representation semantics and qualified ancestry classification.",
      "RPE-05 consumes the qualified RPE-04 adapter interface but is first qualified with a fake adapter and injected time, without network.",
      "RPE-06 is the final preregistration gate and requires RPE-01 through RPE-05."
    ]
  },
  "stages": {
    "RPE-01": {
      "title": "N4_GOVERNED_CLOSED_SCHEMA",
      "closes": ["N4", "NF1"],
      "status": "NOT_OPENED",
      "depends_on": [],
      "purpose": "Prevent new authority, timing, queue, claim, or execution semantics from entering governed JSON through added or duplicate members, type coercion, list laundering, or adjacent configuration files.",
      "preserve_adopted_contract_bytes_if_possible": true,
      "requirements": {
        "reject_duplicate_json_member_names_before_dictionary_construction": true,
        "close_all_object_levels": true,
        "strict_types": true,
        "integer_must_exclude_boolean_and_float_coercion": true,
        "normative_list_vocabularies_closed": true,
        "normative_list_uniqueness_enforced": true,
        "normative_list_order_frozen_where_required": true,
        "real_end_to_end_stages_order_normative": true,
        "schema_guard_itself_versioned_and_blob_bound": true,
        "schema_change_requires_governed_amendment": true,
        "future_real_p5e_json_artifacts_must_use_governed_schema_guard": [
          "adapter_configuration",
          "runner_configuration",
          "experiment_preregistration",
          "execution_evidence_envelope"
        ]
      },
      "minimum_red_families": [
        "duplicate authority key with contradictory first/last values",
        "unknown authority key",
        "unknown claim key",
        "unknown timing key",
        "unknown queue key",
        "integer to float coercion",
        "boolean where integer required",
        "duplicate normative list member",
        "unknown normative enum member",
        "real_end_to_end_stages reorder",
        "authority moved to adjacent governed config"
      ],
      "exit_criterion": "ALL_SCHEMA_AND_ADDED_KEY_BREAKERS_REJECTED_WITHOUT_RELYING_ON_COVERED_OBJECT_BINDING_ALONE"
    },
    "RPE-02": {
      "title": "N5_PLUS_REAL_TIME_REPRESENTATION_AND_BOUNDARY_FREEZE",
      "closes": ["N5", "BF2", "NF6_TIMING_CAPABILITY_PART"],
      "status": "NOT_OPENED",
      "depends_on": ["RPE-01"],
      "purpose": "Define a lossless real-time evidence representation and freeze equality, rounding, actual-start, completion, and bound semantics before any real scheduler or adapter consumes them.",
      "adopted_synthetic_model_remains_immutable_by_default": true,
      "preferred_real_evidence_unit": "INTEGER_MONOTONIC_NANOSECONDS",
      "floating_point_seconds_as_normative_evidence_forbidden": true,
      "lossy_truncation_to_integer_seconds_for_real_pass_fail_forbidden": true,
      "candidate_real_evidence_fields": [
        "schedule_origin_ns",
        "scheduled_at_ns",
        "attempt_started_at_ns",
        "remote_observation_completed_at_ns",
        "attempt_completed_at_ns",
        "controlled_source_release_started_at_ns"
      ],
      "field_semantics_to_freeze": {
        "scheduled_at_ns": "planned fixed-rate slot",
        "attempt_started_at_ns": "actual start of one observation attempt",
        "remote_observation_completed_at_ns": "completion of the governed remote observation operation that produced the exact observed remote-ref evidence",
        "attempt_completed_at_ns": "completion of local materialization, ancestry classification, and normalized event construction",
        "controlled_source_release_started_at_ns": "same-host monotonic timestamp captured immediately before starting the separately authorized source release operation"
      },
      "boundary_rules_to_freeze": [
        "release exactly on scheduled slot",
        "release just after scheduled slot",
        "first required slot ceiling rule",
        "attempt actual-start delay relative to scheduled slot",
        "maximum permitted start lag or explicit missed-slot rule",
        "remote observation completion exactly on next slot",
        "remote observation completion just after next slot",
        "previous attempt completion exactly equal to next attempt start",
        "previous attempt completion greater than next attempt start",
        "latency exactly 60 seconds",
        "latency strictly greater than 60 seconds",
        "lowercase exact commit identity format",
        "relationship between remote observation completion and full attempt completion"
      ],
      "clock_capability_evidence_required": [
        "clock implementation",
        "monotonic property",
        "adjustable property",
        "reported resolution",
        "same process/host domain for compared timestamps"
      ],
      "mandatory_red_cases": [
        "non-integer monotonic release",
        "non-integer actual attempt start",
        "non-integer remote completion",
        "real latency just above 60 seconds",
        "late actual start hidden behind on-time scheduled slot",
        "two-phase remote-completion versus attempt-completion case"
      ],
      "architecture_decision_gate": {
        "candidate_A": "QUALIFIED_CONSERVATIVE_CONVERSION_LAYER",
        "candidate_B": "SEPARATE_REAL_TIME_MODEL_V0_2",
        "decision_rule": "Choose the smallest architecture that passes all preregistered RED cases without weakening conservative classification.",
        "candidate_A_constraints": [
          "real evidence retained losslessly in integer nanoseconds",
          "conversion used only for parity/reference comparison or explicitly qualified mapping",
          "conversion may not turn real >bound into PASS",
          "actual-start evidence may not be erased",
          "real runner pass/fail may not depend on lossy conversion"
        ],
        "candidate_B_constraints": [
          "native integer nanoseconds",
          "explicit actual-start field",
          "explicit remote-completion field",
          "explicit full-attempt-completion field",
          "parity qualification against adopted synthetic model on common exact-grid domain"
        ]
      },
      "exit_criterion": "REAL_TIME_REPRESENTATION_AND_ALL_EQUALITY_ROUNDING_START_COMPLETION_BOUNDARIES_ARE_EXPLICITLY_CONTRACTED_AND_EXECUTABLY_QUALIFIED"
    },
    "RPE-03": {
      "title": "NB5_QUALIFIED_ANCESTRY_CLASSIFIER",
      "closes": ["NB5", "NF2"],
      "status": "NOT_OPENED",
      "depends_on": ["RPE-01"],
      "purpose": "Remove caller authority over INITIAL/SAME/FAST_FORWARD/NON_FAST_FORWARD/UNKNOWN by deriving transition class from a controlled verified local Git object domain.",
      "network_inside_classifier_forbidden": true,
      "input": [
        "previous_observed_head_or_null",
        "new_exact_observed_head",
        "verified_local_git_object_domain"
      ],
      "output": ["INITIAL", "SAME", "FAST_FORWARD", "NON_FAST_FORWARD", "UNKNOWN"],
      "verified_domain_requirements": [
        "GIT_NO_REPLACE_OBJECTS=1",
        "repository is not shallow",
        "no git info/grafts",
        "previous object type commit when previous exists",
        "new object type commit",
        "previous missing -> UNKNOWN",
        "new missing -> UNKNOWN",
        "timeout -> UNKNOWN",
        "corruption -> UNKNOWN"
      ],
      "ancestry_command_semantics": {
        "command_family": "git merge-base --is-ancestor PREVIOUS NEW",
        "exit_0": "FAST_FORWARD",
        "exit_1": "NON_FAST_FORWARD",
        "other_exit": "UNKNOWN"
      },
      "classification_rules": {
        "no_previous_head": "INITIAL",
        "same_exact_head": "SAME",
        "verified_previous_is_ancestor_of_new": "FAST_FORWARD",
        "verified_both_commits_previous_not_ancestor_of_new": "NON_FAST_FORWARD",
        "unprovable_or_invalid_domain": "UNKNOWN"
      },
      "local_fixture_cases": [
        "null to A",
        "A to A",
        "A to B fast-forward",
        "B to A rollback",
        "B and C divergent siblings",
        "missing previous",
        "missing new",
        "non-commit object",
        "replace-ref attempt",
        "shallow repository",
        "graft presence",
        "timeout",
        "corrupt repository"
      ],
      "exit_criterion": "TRANSITION_CLASS_IS_DERIVED_FROM_VERIFIED_LOCAL_GIT_GRAPH_AND_CANNOT_BE_CALLER_FORGED"
    },
    "RPE-04": {
      "title": "NB2_NB3_REAL_REMOTE_OBSERVATION_ADAPTER",
      "closes": ["NB2", "NB3", "NF3"],
      "status": "NOT_OPENED",
      "depends_on": ["RPE-02", "RPE-03"],
      "purpose": "Convert one governed remote-ref observation into exact evidence plus independently derived ancestry without conflating observed tips with contained history.",
      "initial_qualification_environment": "LOCAL_BARE_REMOTE_OR_INJECTED_REMOTE_IO_NO_GITHUB_POLLING",
      "preferred_remote_transaction": "SINGLE_GOVERNED_FETCH_TO_ISOLATED_NAMESPACE",
      "two_read_ls_remote_then_fetch": "REQUIRES_SEPARATE_JUSTIFICATION_AND_RACE_SEMANTICS_IF_RETAINED",
      "git_environment_isolation": [
        "pinned remote URL or equivalently governed verified remote configuration",
        "neutralized global Git config",
        "neutralized system Git config",
        "empty or disabled hooks path",
        "GIT_TERMINAL_PROMPT=0",
        "explicit timeout",
        "no inherited url.insteadOf authority",
        "no canonical user worktree mutation",
        "isolated ref namespace and object domain"
      ],
      "requirements": [
        "one exact configured remote ref per attempt",
        "zero/multiple/unexpected ref outcomes fail closed",
        "exact lower-case 40-hex observed identity",
        "remote observation completion timestamp uses RPE-02 representation",
        "network/read failure emits fail-closed observation failure",
        "exact observed commit materialized/proven in isolated domain",
        "invoke only qualified RPE-03 ancestry classifier",
        "emit normalized P5-D2 REMOTE_HEAD_OBSERVED event with derived transition class",
        "only exact SHA evidenced by successful governed remote operation is OBSERVED_REMOTE_TIP",
        "ancestry-enumerated commits are CONTENT_CONTAINED_NOT_OBSERVED",
        "no intermediate commit injection without independent successful remote observation",
        "unprovable exact observed SHA -> UNKNOWN/BLOCKED",
        "no queue coalescing",
        "no retargeting",
        "no evaluation/promotion/publication/Vault authority"
      ],
      "transaction_questions_to_preregister": [
        "exact fetch command/refspec",
        "exact source of observed SHA evidence",
        "timestamp point for remote observation completion",
        "timestamp point for full attempt completion",
        "timeout representation",
        "isolated namespace lifecycle",
        "object-domain retention across attempts"
      ],
      "exit_criterion": "ADAPTER_OUTPUT_IS_EXACT_GOVERNED_REMOTE_EVIDENCE_PLUS_QUALIFIED_ANCESTRY_WITH_NO_CALLER_SUPPLIED_CONTAINMENT_OR_TRANSITION_AUTHORITY"
    },
    "RPE-05": {
      "title": "FINITE_FIXED_RATE_TIMED_RUNNER",
      "closes": ["BF1"],
      "status": "NOT_OPENED",
      "depends_on": ["RPE-04"],
      "purpose": "Qualify the finite P5-E timing/scheduler authority delegated away from P5-D4 before any network execution.",
      "initial_qualification_environment": "NO_NETWORK_INJECTED_CLOCK_INJECTED_SLEEP_FAKE_ADAPTER",
      "target_interval_ns": 30000000000,
      "target_detection_bound_ns": 60000000000,
      "required_properties": [
        "fixed-rate schedule anchored to one origin",
        "no fixed-delay drift",
        "separate scheduled slot and actual attempt start",
        "separate remote observation completion and total attempt completion",
        "exactly one active attempt",
        "no overlapping observation operation",
        "late-start handling delegated to qualified RPE-02 policy",
        "attempt-crossing-next-slot handling delegated to qualified RPE-02 policy",
        "finite maximum slots or finite terminal horizon",
        "deterministic terminal reason",
        "terminal reason causes STOP",
        "adapter exception or network-equivalent failure becomes fail-closed evidence",
        "no implicit retry authority beyond preregistered schedule",
        "no queue coalescing",
        "no candidate retargeting",
        "no evaluation authority",
        "no Stage A/B authority",
        "no promotion/publication/Vault/CURRENT authority",
        "no daemon/service/startup registration",
        "no production P5-D4 control-state mutation",
        "runner state and evidence isolated from production P5-D4 state"
      ],
      "minimum_fake_clock_traces": [
        "perfect on-time attempts",
        "late start within chosen policy",
        "late start beyond chosen policy",
        "attempt completes exactly at next slot",
        "attempt overruns next slot",
        "adapter failure",
        "terminal success",
        "terminal latency failure",
        "finite no-detection stop",
        "sleep returns early",
        "sleep returns late",
        "clock discontinuity injected"
      ],
      "exit_criterion": "FINITE_FIXED_RATE_RUNNER_IS_DETERMINISTIC_FAIL_CLOSED_SINGLE_ACTIVE_ATTEMPT_AND_QUALIFIED_WITHOUT_NETWORK"
    },
    "RPE-06": {
      "title": "NB9_CONTROLLED_REAL_EXPERIMENT_PREREGISTRATION",
      "closes": ["NB9", "NF4", "NF5", "NF6_EXPERIMENT_PART"],
      "status": "NOT_OPENED",
      "depends_on": ["RPE-01", "RPE-02", "RPE-03", "RPE-04", "RPE-05"],
      "purpose": "Define exactly one finite real-network experiment after every static/runtime prerequisite is qualified.",
      "experiment_contract_must_be_distinct_from_adopted_production_source_contract": true,
      "p5d4_real_state_mutation_authorized": false,
      "same_host_same_monotonic_clock_domain_required": true,
      "sleep_hibernation_suspend_resume_must_be_prevented_or_detected_and_invalidate_run": true,
      "preferred_first_pilot_surface": "DEDICATED_SANDBOX_REPOSITORY_OR_EQUIVALENT_ISOLATED_EXPERIMENT_SURFACE",
      "sandbox_claim_limit": "May qualify runner/transport/adapter timing path; may not qualify integration/system-v1-specific SLA.",
      "required_identity_and_isolation": [
        "exact experiment repository URL",
        "exact experiment ref",
        "isolated producer clone",
        "isolated observer/control root",
        "no production P5-D4 control-root reuse",
        "explicit claim boundary"
      ],
      "release_and_push_evidence": [
        "target commit precomputed before release",
        "same-host controlled source release start monotonic timestamp captured immediately before starting push",
        "push completion monotonic timestamp",
        "explicit refspec",
        "no force push",
        "creation-only guard technically validated before use",
        "separate cleanup authority",
        "cleanup not implicitly authorized by execution authorization"
      ],
      "push_outcome_matrix_minimum": {
        "push_success_target_observed_within_bound": "VALID_PASS_CANDIDATE",
        "push_success_target_not_observed_by_bound": "SLA_FAIL_CANDIDATE",
        "push_failure_target_not_observed": "INVALID_EXPERIMENT",
        "push_failure_target_observed": "INCONCLUSIVE_OR_BLOCKED"
      },
      "pre_push_side_effect_audit": [
        "GitHub Actions workflows triggered by push",
        "branch/ref filters",
        "secret-bearing workflows",
        "external side effects",
        "other automation triggered by experiment ref"
      ],
      "execution_evidence_required": [
        "clock capability evidence",
        "host continuity evidence",
        "release-start timestamp",
        "push-completion timestamp",
        "scheduled slots",
        "actual attempt starts",
        "remote observation completions",
        "attempt completions",
        "exact observed heads",
        "derived transition classes",
        "terminal runner reason",
        "push outcome",
        "experiment verdict"
      ],
      "production_ref_gate_after_sandbox": {
        "integration_system_v1_mutation_for_measurement_only_forbidden": true,
        "separate_human_authorization_required": true,
        "preferred_source_event": "separately authorized legitimate governed update with target commit known before push",
        "production_ref_sla_claim_requires_own_evidence": true,
        "production_p5d4_pending_state_and_queue_capacity_must_be_explicitly_adjudicated": true
      },
      "exit_criterion": "SELF_CONTAINED_HUMAN_ADOPTED_PREREGISTRATION_EXISTS_FOR_ONE_FINITE_REAL_EXPERIMENT_WITH_EXACT_SOURCE_CLOCK_PUSH_RUNNER_ADAPTER_EVIDENCE_AND_STOP_RULES"
    }
  },
  "governance_efficiency": {
    "rpe_01_and_rpe_02_may_share_future_macro_authorization": true,
    "conditions": [
      "separate preregistrations",
      "separate RED families",
      "RPE-01 schema guard qualified before any RPE-02 governed artifact relies on it"
    ],
    "rpe_03_must_remain_separate_runtime_qualification": true
  },
  "post_readiness_gate": {
    "real_experiment_execution_authorized_by_this_map": false,
    "required_before_real_experiment": [
      "RPE-01 QUALIFIED",
      "RPE-02 QUALIFIED",
      "RPE-03 QUALIFIED",
      "RPE-04 QUALIFIED",
      "RPE-05 QUALIFIED",
      "RPE-06 PREREGISTERED_AND_HUMAN_ADOPTED",
      "separate one-shot human execution authorization"
    ],
    "mandatory_stop": true
  },
  "claim_boundary": {
    "real_p5e_qualified": false,
    "real_60_second_sla_qualified": false,
    "integration_system_v1_sla_qualified": false,
    "real_tip_visibility_adapter_qualified": false,
    "ancestry_classifier_qualified": false,
    "timed_runner_qualified": false,
    "real_experiment_authorized": false
  }
}

~~~~

# SOURCE: READINESS V0.2 REPORT
Path: reports/program/2026-10-02-OBSIDIAN-REAL-P5E-PRE-EXECUTION-READINESS-V0.2.md
~~~~
# REAL P5-E â€” PRE-EXECUTION READINESS V0.2

Date: 2026-10-02

## Purpose

Amend V0.1 after external review `FAIL` without opening any implementation.

V0.2 closes the two decomposition gaps:

- BF1 â€” missing finite timed runner;
- BF2 â€” missing qualified real-time evidence representation.

It also incorporates NF1â†’NF7 into the appropriate readiness stages.

```text
P5-E V0.1 CONTRACT + SYNTHETIC MODEL
= QUALIFIED_AND_HUMAN_ADOPTED
= UNCHANGED

REAL P5-E
= CLOSED

RPE-01â†’RPE-06
= NOT OPENED
```

## Lineage

Base checkpoint:
`90189ac1ddddc8d81b12eeaa2a4241969a7dc405`

V0.1 readiness:
```text
JSON   = 9ee1e02cf371cc990097af0ae6e31317ed083a69
REPORT = 5434397e87fe0f204891d230b03832c625e01368
```

Internal V0.2 adjudication:
`BF1/BF2 confirmed; NF1â†’NF7 accepted as stage requirements.`
## Corrected dependency architecture

V0.1 incorrectly behaved like a total order and omitted one runtime layer.

V0.2 uses the following DAG:

```text
                         RPE-01
                  N4 GOVERNED CLOSED SCHEMA
                       /                 \
                      /                   \
                     â†“                     â†“
             RPE-02                        RPE-03
      N5 + REAL-TIME                  NB5 ANCESTRY
       REPRESENTATION                  CLASSIFIER
                     \                   /
                      \                 /
                       â†“               â†“
                          RPE-04
                    NB2 + NB3 REAL
                   OBSERVATION ADAPTER
                             â†“
                          RPE-05
                    FINITE FIXED-RATE
                       TIMED RUNNER
                             â†“
                          RPE-06
                     NB9 CONTROLLED
                 EXPERIMENT PREREGISTRATION
                             â†“
                 SEPARATE HUMAN EXECUTION
                        AUTHORIZATION
```

Exact dependency edges:

```text
RPE-01 â†’ RPE-02
RPE-01 â†’ RPE-03
RPE-02 + RPE-03 â†’ RPE-04
RPE-04 â†’ RPE-05
RPE-01 + RPE-02 + RPE-03 + RPE-04 + RPE-05 â†’ RPE-06
```

RPE-02 and RPE-03 may progress independently once RPE-01 is qualified.
## RPE-01 â€” N4 GOVERNED CLOSED SCHEMA

### Why it comes first

Future REAL P5-E artifacts will add configuration and authority surfaces.

If the schema guard is not qualified first, authority can migrate from the adopted contract into:
- adapter config;
- runner config;
- experiment preregistration;
- evidence envelope.

### Required protection

The guard must operate on raw JSON bytes plus parsed structure.

It must reject:
- duplicate object member names before normal JSON dictionary construction;
- unknown keys at every object depth;
- wrong types;
- boolean-as-integer laundering;
- float-as-integer coercion;
- duplicate normative list values;
- unknown enum/list members;
- normative list reordering where order matters.

The guard and its schema specification must themselves be versioned and blob-bound.

A change to the allowed schema is an amendment, not an incidental edit.

### Exit criterion

`ALL_SCHEMA_AND_ADDED_KEY_BREAKERS_REJECTED_WITHOUT_COVERED_OBJECT_BINDING_AS_THE_ONLY_DEFENSE`
## RPE-02 â€” N5 + REAL-TIME REPRESENTATION AND BOUNDARY FREEZE

### BF2 correction

The adopted synthetic model is intentionally integer-second and synthetic.

It cannot safely serve as the raw real-time evidence model.

V0.2 therefore separates:

```text
synthetic adopted semantics
â‰ 
raw real-time evidence representation
```

Preferred raw unit:
`integer monotonic nanoseconds`

Floating-point seconds are not the normative evidence format.

Lossy truncation to seconds is forbidden for pass/fail classification.

### Candidate evidence fields

```text
schedule_origin_ns
scheduled_at_ns
attempt_started_at_ns
remote_observation_completed_at_ns
attempt_completed_at_ns
controlled_source_release_started_at_ns
```

These separate:
- intended slot;
- actual start;
- remote evidence completion;
- total local attempt completion.

### Boundary decisions that must be frozen

RPE-02 must explicitly decide and test:
- release exactly on a slot;
- release immediately after a slot;
- first-slot ceiling rule;
- permitted scheduler start lag or missed-slot rule;
- completion exactly on next slot;
- completion just after next slot;
- completion equal to next attempt start;
- true overlap;
- exactly 60 seconds;
- strictly greater than 60 seconds;
- exact SHA format;
- how remote-completion and full-attempt-completion interact.

### Architecture decision

RPE-02 begins with RED cases that expose the real/synthetic mismatch.

Then choose between:

A. qualified conservative conversion layer; or
B. separate native real-time model V0.2.

The adopted synthetic model is not modified unless a separately authorized future decision explicitly says so.
## RPE-03 â€” NB5 QUALIFIED ANCESTRY CLASSIFIER

P5-D2 remains a deterministic consumer.

RPE-03 removes caller authority over transition classification.

### Verified object domain

Before any ancestry claim:
- no replace objects;
- no shallow state;
- no grafts;
- both SHA identities resolve to commits;
- missing objects fail to UNKNOWN;
- timeout/corruption fail to UNKNOWN.

### Classification

```text
no previous head
â†’ INITIAL

same head
â†’ SAME

merge-base --is-ancestor previous new
exit 0
â†’ FAST_FORWARD

exit 1 after both commits verified
â†’ NON_FAST_FORWARD

anything else
â†’ UNKNOWN
```

Rollback and sibling divergence remain one D2 class:
`NON_FAST_FORWARD`

Optional sub-evidence may distinguish them, but cannot change D2 authority semantics.
## RPE-04 â€” NB2 + NB3 REAL OBSERVATION ADAPTER

RPE-04 binds real remote evidence to RPE-03.

### Preferred remote observation design

One governed fetch transaction per attempt into an isolated namespace/object domain.

This is preferred over:
`ls-remote â†’ independent fetch`

because the latter creates two remote observations and a race between them.

RPE-04 must still preregister exactly:
- the fetch command;
- the refspec;
- how the observed SHA is extracted;
- when remote observation completion is timestamped;
- when total attempt completion is timestamped;
- timeout behavior;
- zero/multiple/unexpected-ref behavior;
- namespace/object-domain lifecycle.

### Git environment isolation

Required:
- pinned URL or equivalently governed verified remote config;
- no inherited global/system config;
- hooks disabled;
- terminal prompt disabled;
- explicit timeout;
- no inherited `url.insteadOf`;
- no canonical user worktree mutation.

### Evidence semantics

Only the exact SHA produced by the successful governed remote transaction is:

`OBSERVED_REMOTE_TIP`

A commit only discovered through history/ancestry is:

`CONTENT_CONTAINED_NOT_OBSERVED`

and cannot be queued as though it had been independently observed.
## RPE-05 â€” FINITE FIXED-RATE TIMED RUNNER

This is the new BF1-closing stage missing from V0.1.

### Qualification environment

```text
NO NETWORK
INJECTED CLOCK
INJECTED SLEEP
FAKE ADAPTER
```

The runner must be fully qualifiable without GitHub.

### Responsibilities

The runner owns only:
- fixed-rate scheduling;
- finite horizon;
- actual attempt start;
- wait/sleep;
- exactly one active attempt;
- terminal stop.

It consumes RPE-02 timing semantics and the RPE-04 adapter interface.

It must prove:
- 30-second anchored fixed-rate schedule;
- no fixed-delay drift;
- separate scheduled and actual start;
- separate remote and total completion;
- single active attempt;
- no overlap;
- exact late-start/overrun policy from RPE-02;
- deterministic terminal reason;
- deterministic STOP;
- finite maximum horizon;
- fail-closed adapter failure;
- no implicit retry beyond schedule.

It must not gain:
- evaluation;
- Stage A/B;
- promotion;
- publication;
- Vault/CURRENT mutation;
- queue coalescing;
- retargeting;
- daemon/service/startup authority.

### Exit criterion

`FINITE_FIXED_RATE_RUNNER_IS_DETERMINISTIC_FAIL_CLOSED_AND_QUALIFIED_WITHOUT_NETWORK`
## RPE-06 â€” NB9 CONTROLLED REAL EXPERIMENT PREREGISTRATION

RPE-06 happens only after RPE-01â†’RPE-05 are qualified.

It remains a preregistration, not execution.

### Experiment contract

A sandbox experiment uses a different source from the adopted production source.

Therefore it requires an explicit experiment contract.

It must define:
- exact repository URL;
- exact experiment ref;
- isolated producer clone;
- isolated observer/control root;
- claim boundary;
- `p5d4_real_state_mutation_authorized = false`.

### Clock domain

For Pilot A:
`SAME HOST = REQUIRED`

Release recorder, runner and adapter must share one qualified monotonic clock domain.

The pilot must invalidate itself if sleep/hibernation/suspend continuity is not proven.

Current local observation only:
Python reports `monotonic` as `QueryPerformanceCounter()`, monotonic, non-adjustable, reported resolution `1e-7 s`.

That observation is not qualification and must be captured again during the actual RPE-02/RPE-06 qualification environment.

### Push protocol

Record:
- target commit before release;
- release-start monotonic time immediately before push;
- push completion;
- explicit refspec;
- creation-only guard;
- no force push.

Minimum experiment classification:

```text
push success + observed within bound
â†’ VALID_PASS_CANDIDATE

push success + not observed by bound
â†’ SLA_FAIL_CANDIDATE

push failure + not observed
â†’ INVALID_EXPERIMENT

push failure + target nevertheless observed
â†’ INCONCLUSIVE_OR_BLOCKED
```

Exact labels remain to be frozen in the preregistration.

### Side-effect audit

Before push, inspect:
- workflows triggered by push;
- branch/ref filters;
- secret-bearing automation;
- external side effects.

Do not run a pilot whose side effects are not bounded.

Preferred first surface:
a dedicated sandbox repository or equivalently isolated experiment surface.

Sandbox success does not qualify `integration/system-v1`-specific SLA.
## Production-source gate after sandbox

A later observation against `integration/system-v1` requires:

- separate human authorization;
- a legitimate governed update, not a dummy measurement commit;
- target commit known before push;
- explicit adjudication of real P5-D4 pending state and queue capacity;
- production-specific evidence;
- no inference that sandbox latency automatically equals production-branch latency.

## Governance efficiency

RPE-01 and RPE-02 may share a future macro-authorization only if:
- preregistrations remain separate;
- RED families remain separate;
- RPE-01 is qualified before RPE-02 artifacts rely on its schema authority.

RPE-03 remains a separate code/runtime qualification.

## V0.2 readiness verdict

```text
BF1 = MAPPED_TO_RPE_05
BF2 = MAPPED_TO_RPE_02

NF1 = INTEGRATED_RPE_01
NF2 = INTEGRATED_RPE_03
NF3 = INTEGRATED_RPE_04
NF4 = INTEGRATED_RPE_06
NF5 = INTEGRATED_RPE_06
NF6 = INTEGRATED_RPE_02_AND_RPE_06
NF7 = INTEGRATED_AS_DAG

RPE-01 = NOT OPENED
RPE-02 = NOT OPENED
RPE-03 = NOT OPENED
RPE-04 = NOT OPENED
RPE-05 = NOT OPENED
RPE-06 = NOT OPENED

REAL_P5E = CLOSED
P6 = CLOSED
```

Next gate:
external delta-review of this V0.2 readiness amendment.

No implementation may begin before that review is adjudicated.

~~~~

# SOURCE: ADOPTED P5-E CONTRACT
Path: tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1",
  "status": "CANDIDATE_TARGETED_CLOSURE_PENDING_EXTERNAL_REREVIEW",
  "qualification_stage": "CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY",
  "real_p5e_execution_authorized": false,
  "source_repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "monitored_source": {
    "remote": "origin",
    "branch": "integration/system-v1",
    "canonical_authority": "GITHUB_REMOTE_BRANCH",
    "local_working_tree_is_not_authority": true
  },
  "predecessors": {
    "p5a_continuous_projection_contract_blob": "96ec1a768b8e9ff77d94bbcd36ee513678c258e6",
    "p5a_qualification_report_blob": "8954475370494ff00f77af8331b2e54b80cf3f70",
    "p5d1_observer_contract_blob": "a20999ae991e07447e25ecd1592964f2d333449b",
    "p5d1_static_review_blob": "d10a6659e8deec917803f53c652fc7e4d4d19458",
    "p5d2_one_shot_contract_blob": "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3",
    "p5d2_static_review_blob": "023cc210facdbc4b571b88bd257057c67a3df46b",
    "p5d4_loop_contract_blob": "6980de1eb55e49c0c2bd2f91620aeb75640753b6",
    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
    "p5d4_real_v0_2_qualification_blob": "660a679532d1bb122b0df382230d4d249a0cac1f",
    "p5d4_human_adjudication_blob": "ef5e07c6641db94e91d9f2bc0e8093b244baa507"
  },
  "objective": {
    "name": "END_TO_END_NEAR_REAL_TIME_QUALIFICATION",
    "purpose": "Define the temporal and authority contract required before any real repeated observation experiment may claim bounded near-real-time behavior around the already-qualified P5-D4 bounded loop.",
    "this_stage_is_not_real_end_to_end_execution": true,
    "this_stage_may_not_claim_continuous_synchronization": true
  },
  "near_real_time_timing": {
    "delivery_semantics": "NEAR_REAL_TIME_BOUNDED_LATENCY",
    "poll_interval_seconds": 30,
    "detection_latency_seconds_max": 60,
    "instantaneous_realtime_claim_forbidden": true,
    "silent_interval_widening_forbidden": true,
    "silent_latency_bound_widening_forbidden": true,
    "detection_latency_definition": "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC_MINUS_CONTROLLED_SOURCE_RELEASE_MONOTONIC",
    "future_real_bound_clock": "MONOTONIC_ELAPSED_TIME",
    "future_real_wall_clock_may_be_recorded_as_evidence_only": true,
    "future_real_poll_schedule_semantics": "FIXED_RATE_30_SECOND_GRID",
    "single_transient_read_failure_may_still_meet_60_second_bound": false,
    "latency_bound_breach_must_not_be_reported_as_near_real_time_pass": true,
    "real_measurement_origin": "CONTROLLED_SOURCE_RELEASE_MONOTONIC",
    "measurement_endpoint": "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC",
    "schedule_semantics": "FIXED_RATE",
    "remote_head_available_time_is_measurable_origin": false,
    "real_latency_metric": "REMOTE_READ_COMPLETION_MONOTONIC_MINUS_CONTROLLED_SOURCE_RELEASE_MONOTONIC",
    "attempt_start_and_read_completion_are_distinct": true,
    "read_duration_is_included_in_detection_latency": true,
    "eligible_detection_attempt_must_start_at_or_after_release": true,
    "single_transient_read_failure_may_meet_bound_only_if_read_completion_is_within_60_seconds": true
  },
  "synthetic_timing_model": {
    "required": true,
    "clock_source": "EXPLICIT_INJECTED_MONOTONIC_SECONDS_ONLY",
    "sleep_forbidden": true,
    "network_forbidden": true,
    "filesystem_state_forbidden": true,
    "process_launch_forbidden": true,
    "environment_read_forbidden": true,
    "real_p5d4_control_state_access_forbidden": true,
    "real_vault_access_forbidden": true,
    "purpose": "Prove timing arithmetic and claim boundaries without performing repeated real observation.",
    "schedule_semantics": "FIXED_RATE",
    "schedule_origin_seconds": 0,
    "observation_record_fields": [
      "scheduled_at_seconds",
      "completed_at_seconds",
      "outcome",
      "observed_head"
    ],
    "head_identity_required_on_successful_remote_observation": true,
    "skipped_required_attempt_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "cadence_gap_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "pre_source_target_observation_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "explicit_non_pass_statuses": [
      "INCOMPLETE_SYNTHETIC_WINDOW"
    ],
    "attempt_overruns_next_required_slot_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "attempt_overruns_next_required_slot_failure_code": "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT",
    "duplicate_fixed_rate_slot_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "duplicate_fixed_rate_slot_failure_code": "DUPLICATE_FIXED_RATE_SLOT",
    "read_completion_before_attempt_start_forbidden": true
  },
  "authority_boundary": {
    "observer_may_create_governance_authority": false,
    "pending_head_evaluation_authorized": false,
    "evaluation_authorized": false,
    "stage_a_authorized": false,
    "stage_b_authorized": false,
    "promotion_authorized": false,
    "publication_authorized": false,
    "real_vault_mutation_authorized": false,
    "current_mutation_authorized": false,
    "current_tmp_mutation_authorized": false,
    "real_polling_loop_authorized": false,
    "daemon_authorized": false,
    "startup_registration_authorized": false,
    "scheduled_task_authorized": false,
    "windows_service_authorized": false,
    "p6_authorized": false
  },
  "head_transition_policy": {
    "same_head_result": "NOOP",
    "same_head_queue_growth_forbidden": true,
    "initial_head_may_queue_exact_head_only_under_existing_p5d2_semantics": true,
    "fast_forward_head_may_queue_exact_head_only_under_existing_p5d2_semantics": true,
    "non_fast_forward_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "unknown_ancestry_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "non_fast_forward_auto_continue_forbidden": true,
    "unknown_ancestry_auto_continue_forbidden": true,
    "active_or_pending_candidate_retarget_forbidden": true
  },
  "queue_and_supersession": {
    "precedence_rule": "CURRENT_QUALIFIED_P5D4_EXECUTABLE_QUEUE_SEMANTICS_OVERRIDE_EARLIER_P5A_DESIGN_INTENT_WHERE_THEY_CONFLICT",
    "p5a_supersession_intent_preserved_as_future_design_debt": true,
    "fifo_required": true,
    "unique_heads_required": true,
    "silent_drop_forbidden": true,
    "silent_reorder_forbidden": true,
    "latest_only_replacement_forbidden": true,
    "coalescing_authorized": false,
    "new_coalescing_semantic_event_authorized": false,
    "pending_head_retarget_forbidden": true,
    "capacity_exhausted_result": "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
    "capacity_exhausted_must_not_mutate_p5d2_state": true,
    "burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification": true
  },
  "failure_and_freshness": {
    "fail_closed_default": true,
    "network_failure_must_not_create_current_claim": true,
    "last_known_good_live_projection_preserved": true,
    "latency_bound_breach_result": "NEAR_REAL_TIME_BOUND_NOT_QUALIFIED",
    "queue_capacity_exhaustion_result": "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
    "non_fast_forward_or_unknown_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "unexpected_state_or_timing_ambiguity_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "timing_inconsistency_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "skipped_required_attempt_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "cadence_gap_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "pre_source_target_observation_result": "BLOCKED_REQUIRES_ADJUDICATION"
  },
  "end_to_end_definition": {
    "real_end_to_end_stages": [
      "SOURCE_HEAD_BECOMES_OBSERVABLE",
      "REMOTE_HEAD_DETECTED_WITHIN_BOUND",
      "HEAD_TRANSITION_CLASSIFIED",
      "EXACT_HEAD_ENTERED_GOVERNED_QUEUE_OR_FAIL_CLOSED",
      "EXACT_HEAD_EVALUATED_IF_SEPARATELY_AUTHORIZED",
      "PROMOTION_DECISION_IF_SEPARATELY_AUTHORIZED",
      "PUBLICATION_IF_SEPARATELY_AUTHORIZED",
      "LIVE_GENERATION_VERIFIED_IF_PUBLICATION_AUTHORIZED"
    ],
    "current_stage_may_qualify_only": [
      "TIMING_CONTRACT",
      "SYNTHETIC_FIXED_RATE_DETECTION_MODEL",
      "AUTHORITY_BOUNDARIES",
      "REUSED_MAPPED_P5D2_P5D4_FAIL_CLOSED_QUEUE_BEHAVIOR"
    ],
    "real_end_to_end_pass_requires_all_authorized_applicable_stages": true,
    "omitted_unauthorized_downstream_stages_may_not_be_relabelled_pass": true,
    "transient_tip_exact_detection_sla_not_qualified": true,
    "real_remote_availability_to_detection_sla_not_qualified": true
  },
  "claim_boundary": {
    "maximum_current_claim": "P5E_V0_1_TARGETED_CLOSURE_CANDIDATE_QUALIFIED_PENDING_EXTERNAL_REREVIEW",
    "real_end_to_end_qualification_requires_separate_authorization": true,
    "forbidden_current_claims": [
      "P5E_REAL_END_TO_END_QUALIFIED",
      "CONTINUOUS_SYNCHRONIZATION_QUALIFIED",
      "REAL_60_SECOND_SLA_QUALIFIED",
      "AUTOMATIC_EVALUATION_QUALIFIED",
      "AUTOMATIC_PROMOTION_QUALIFIED",
      "AUTOMATIC_PUBLICATION_QUALIFIED",
      "REMOTE_HEAD_AVAILABLE_TIME_TO_DETECTION_SLA_QUALIFIED",
      "PER_TRANSIENT_TIP_DETECTION_SLA_QUALIFIED"
    ]
  },
  "real_context_evidence_only": {
    "live_projection_head_at_opening": "59f1dc26973b0b50efefccf12b26784d1e41f546",
    "queued_unevaluated_head_at_opening": "1d4c2f3d657b36ecaa6ab25b967e46b3620190d1",
    "remote_head_observed_during_contract_opening": "fcca78571a26955ae3fe462746ef49557e4e84e5",
    "queued_head_is_ancestor_of_remote_head": true,
    "must_not_be_used_as_real_experiment_execution": true,
    "must_not_be_mutated_by_contract_qualification": true
  },
  "required_synthetic_cases": [
    "SAME_HEAD_NOOP",
    "CHANGE_JUST_AFTER_POLL_DETECTED_AT_NEXT_30_SECOND_SLOT",
    "ONE_TRANSIENT_READ_FAILURE_THEN_DETECTED_BY_60_SECONDS",
    "DETECTION_AFTER_60_SECONDS_REJECTED",
    "NO_DETECTION_BY_60_SECONDS_REJECTED",
    "NON_FAST_FORWARD_BLOCKED",
    "UNKNOWN_ANCESTRY_BLOCKED",
    "PENDING_QUEUE_FULL_NEWER_HEAD_FAILS_CLOSED",
    "SAME_HEAD_DOES_NOT_GROW_QUEUE",
    "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD"
  ],
  "required_breakers": [
    "POLL_INTERVAL_NOT_EXACTLY_30_ACCEPTED",
    "DETECTION_BOUND_ABOVE_60_ACCEPTED",
    "INSTANTANEOUS_REALTIME_CLAIM_ACCEPTED",
    "WALL_CLOCK_USED_AS_SYNTHETIC_CONTROL_CLOCK",
    "SLEEP_USED_IN_SYNTHETIC_MODEL",
    "NETWORK_USED_IN_SYNTHETIC_MODEL",
    "FILESYSTEM_STATE_USED_IN_SYNTHETIC_MODEL",
    "PROCESS_LAUNCH_USED_IN_SYNTHETIC_MODEL",
    "SUCCESS_AFTER_60_SECONDS_CLASSIFIED_PASS",
    "NO_SUCCESS_BY_60_SECONDS_CLASSIFIED_PASS",
    "SAME_HEAD_GROWS_QUEUE",
    "NON_FAST_FORWARD_AUTO_CONTINUES",
    "UNKNOWN_ANCESTRY_AUTO_CONTINUES",
    "QUEUE_FULL_SILENTLY_DROPS_HEAD",
    "QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD",
    "QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT",
    "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD",
    "EVALUATION_AUTHORITY_BECOMES_TRUE",
    "PROMOTION_AUTHORITY_BECOMES_TRUE",
    "PUBLICATION_AUTHORITY_BECOMES_TRUE",
    "REAL_VAULT_MUTATION_AUTHORITY_BECOMES_TRUE",
    "REAL_POLLING_AUTHORITY_BECOMES_TRUE",
    "DAEMON_OR_SERVICE_AUTHORITY_BECOMES_TRUE",
    "P6_AUTHORITY_BECOMES_TRUE",
    "CONTRACT_PASS_LAUNDERS_INTO_REAL_P5E_PASS"
  ],
  "next_gate_after_candidate_qualification": {
    "external_adversarial_review_required_before_normative_adoption": true,
    "human_adjudication_required_after_external_review": true,
    "real_p5e_execution_requires_separate_human_authorization": true,
    "p6_remains_closed": true,
    "external_adversarial_rereview_required": true,
    "human_adjudication_before_external_rereview_forbidden": true
  },
  "tip_visibility_semantics": {
    "observed_remote_tip_definition": "HEAD_IDENTITY_RETURNED_BY_A_SUCCESSFUL_REMOTE_READ",
    "intermediate_fast_forward_commit_definition": "COMMIT_CONTAINED_BY_LATER_OBSERVED_FAST_FORWARD_HEAD_BUT_NOT_ITSELF_OBSERVED_AS_REMOTE_TIP",
    "unobserved_intermediate_tip_may_be_claimed_observed": false,
    "unobserved_intermediate_tip_may_be_queued": false,
    "fast_forward_content_containment_is_queue_coalescing": false,
    "already_observed_queued_head_replacement_forbidden": true,
    "already_observed_queued_head_retarget_forbidden": true,
    "per_transient_tip_detection_sla_authorized": false,
    "future_ancestry_enumeration_requires_separate_qualification": true,
    "unobserved_intermediate_tip_non_injection_is_future_adapter_rule": true,
    "unobserved_intermediate_tip_non_injection_is_current_runtime_qualified_property": false
  },
  "external_review_targeted_closure": {
    "findings": {
      "B1": "CONFIRMED_BLOCKING_WITH_UPSTREAM_COVERAGE_NUANCE",
      "B2": "CONFIRMED_BLOCKING",
      "B3": "CONFIRMED_BLOCKING",
      "B4": "CONFIRMED_BLOCKING",
      "B5": "PARTIALLY_CONFIRMED_BLOCKING_SEMANTIC_GAP"
    },
    "required_breakers": [
      "SKIPPED_REQUIRED_ATTEMPT_ACCEPTED",
      "CADENCE_GAP_ACCEPTED",
      "PRE_SOURCE_TARGET_OBSERVATION_IGNORED",
      "REMOTE_AVAILABILITY_TIME_TREATED_AS_MEASURABLE_ORIGIN",
      "READ_COMPLETION_LATENCY_HIDDEN",
      "OBSERVATION_WITHOUT_HEAD_IDENTITY_ACCEPTED",
      "UNOBSERVED_TRANSIENT_TIP_CLAIMED_EXACTLY_OBSERVED",
      "REQUIRED_CASE_OR_BREAKER_UNMAPPED"
    ],
    "requirement_to_executable_evidence_matrix_required": true,
    "all_required_cases_must_be_mapped": true,
    "all_base_breakers_must_be_mapped": true,
    "all_targeted_closure_breakers_must_be_mapped": true,
    "unmapped_requirement_result": "BLOCKED",
    "external_rereview_required_before_human_normative_adoption": true
  }
}

~~~~

# SOURCE: ADOPTED P5-E SYNTHETIC MODEL
Path: tools/obsidian_projection/p5e_near_real_time_model.py
~~~~
from __future__ import annotations

from typing import Any


PLAN_SCHEMA = "ATDS_OBSIDIAN_P5E_SYNTHETIC_TIMING_PLAN_V0_1_AMENDED"
RESULT_SCHEMA = "ATDS_OBSIDIAN_P5E_SYNTHETIC_TIMING_RESULT_V0_1_AMENDED"

_POLL_INTERVAL_SECONDS = 30
_DETECTION_LATENCY_SECONDS_MAX = 60
_SCHEDULE_ORIGIN_SECONDS = 0
_ALLOWED_OUTCOMES = frozenset({"READ_FAILURE", "REMOTE_HEAD_OBSERVED"})


class P5ETimingModelError(ValueError):
    pass


def _is_nonnegative_int(value: Any) -> bool:
    return (
        not isinstance(value, bool)
        and isinstance(value, int)
        and value >= 0
    )


def _valid_head(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 40:
        return False
    return all(ch in "0123456789abcdef" for ch in value)


def make_timing_plan(
    *,
    poll_interval_seconds: int = _POLL_INTERVAL_SECONDS,
    detection_latency_seconds_max: int = _DETECTION_LATENCY_SECONDS_MAX,
    schedule_origin_seconds: int = _SCHEDULE_ORIGIN_SECONDS,
) -> dict[str, Any]:
    if poll_interval_seconds != _POLL_INTERVAL_SECONDS:
        raise P5ETimingModelError(
            "P5-E V0.1 poll interval must remain exactly 30 seconds"
        )
    if detection_latency_seconds_max != _DETECTION_LATENCY_SECONDS_MAX:
        raise P5ETimingModelError(
            "P5-E V0.1 detection bound must remain exactly 60 seconds"
        )
    if schedule_origin_seconds != _SCHEDULE_ORIGIN_SECONDS:
        raise P5ETimingModelError(
            "P5-E V0.1 synthetic fixed-rate origin must remain exactly zero"
        )
    return {
        "schema": PLAN_SCHEMA,
        "poll_interval_seconds": _POLL_INTERVAL_SECONDS,
        "detection_latency_seconds_max": _DETECTION_LATENCY_SECONDS_MAX,
        "schedule_origin_seconds": _SCHEDULE_ORIGIN_SECONDS,
        "schedule_semantics": "FIXED_RATE",
        "clock_source": "EXPLICIT_INJECTED_MONOTONIC_SECONDS_ONLY",
        "measurement_origin": "CONTROLLED_SOURCE_RELEASE_MONOTONIC",
        "measurement_endpoint": "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC",
        "real_execution_authorized": False,
    }


def _validate_plan(plan: dict[str, Any]) -> None:
    if not isinstance(plan, dict):
        raise P5ETimingModelError("plan must be an object")
    if plan != make_timing_plan(
        poll_interval_seconds=plan.get("poll_interval_seconds"),
        detection_latency_seconds_max=plan.get(
            "detection_latency_seconds_max"
        ),
        schedule_origin_seconds=plan.get("schedule_origin_seconds"),
    ):
        raise P5ETimingModelError("plan fields mismatch")


def _blocked(failure_code: str) -> dict[str, Any]:
    return _result(
        status="BLOCKED_REQUIRES_ADJUDICATION",
        failure_code=failure_code,
        detection_latency_seconds=None,
        first_detection_scheduled_at_seconds=None,
        first_detection_completed_at_seconds=None,
        observed_head=None,
    )


def _result(
    *,
    status: str,
    failure_code: str | None,
    detection_latency_seconds: int | None,
    first_detection_scheduled_at_seconds: int | None,
    first_detection_completed_at_seconds: int | None,
    observed_head: str | None,
) -> dict[str, Any]:
    return {
        "schema": RESULT_SCHEMA,
        "status": status,
        "failure_code": failure_code,
        "detection_latency_seconds": detection_latency_seconds,
        "first_detection_scheduled_at_seconds": (
            first_detection_scheduled_at_seconds
        ),
        "first_detection_completed_at_seconds": (
            first_detection_completed_at_seconds
        ),
        "observed_head": observed_head,
        "real_end_to_end_qualified": False,
        "continuous_synchronization_qualified": False,
        "automatic_evaluation_authorized": False,
        "automatic_promotion_authorized": False,
        "automatic_publication_authorized": False,
    }


def _first_fixed_rate_slot_at_or_after(
    *,
    instant_seconds: int,
    interval: int,
    origin: int,
) -> int:
    first_slot = origin + interval
    if instant_seconds <= first_slot:
        return first_slot
    delta = instant_seconds - origin
    quotient, remainder = divmod(delta, interval)
    return origin + (quotient + (1 if remainder else 0)) * interval


def _validate_observation_shapes(
    observations: list[dict[str, Any]],
) -> None:
    if not isinstance(observations, list) or not observations:
        raise P5ETimingModelError("observations must be a non-empty list")
    required_fields = {
        "scheduled_at_seconds",
        "completed_at_seconds",
        "outcome",
        "observed_head",
    }
    for observation in observations:
        if not isinstance(observation, dict):
            raise P5ETimingModelError("observation must be an object")
        if set(observation) != required_fields:
            raise P5ETimingModelError("observation fields mismatch")
        scheduled = observation["scheduled_at_seconds"]
        completed = observation["completed_at_seconds"]
        outcome = observation["outcome"]
        observed_head = observation["observed_head"]
        if not _is_nonnegative_int(scheduled):
            raise P5ETimingModelError("scheduled time must be nonnegative")
        if not _is_nonnegative_int(completed):
            raise P5ETimingModelError("completion time must be nonnegative")
        if outcome not in _ALLOWED_OUTCOMES:
            raise P5ETimingModelError("observation outcome invalid")
        if outcome == "READ_FAILURE":
            if observed_head is not None:
                raise P5ETimingModelError(
                    "read failure may not carry a head identity"
                )
        elif not _valid_head(observed_head):
            raise P5ETimingModelError(
                "successful remote observation requires exact head identity"
            )


def classify_tip_visibility(
    *,
    target_head: str,
    observed_head: str,
    fast_forward_contains_target: bool,
) -> str:
    if not _valid_head(target_head) or not _valid_head(observed_head):
        raise P5ETimingModelError("tip identity must be a lowercase 40-hex SHA")
    if not isinstance(fast_forward_contains_target, bool):
        raise P5ETimingModelError("containment fact must be boolean")
    if observed_head == target_head:
        return "EXACT_TIP_OBSERVED"
    if fast_forward_contains_target:
        return "CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED"
    return "UNRELATED_OR_UNPROVEN_REQUIRES_ADJUDICATION"


def qualify_detection(
    *,
    plan: dict[str, Any],
    source_release_at_seconds: int,
    target_head: str,
    observations: list[dict[str, Any]],
) -> dict[str, Any]:
    _validate_plan(plan)
    if not _is_nonnegative_int(source_release_at_seconds):
        raise P5ETimingModelError(
            "controlled source release time must be a nonnegative integer"
        )
    if not _valid_head(target_head):
        raise P5ETimingModelError(
            "target head must be a lowercase 40-hex SHA"
        )
    _validate_observation_shapes(observations)

    interval = plan["poll_interval_seconds"]
    bound = plan["detection_latency_seconds_max"]
    origin = plan["schedule_origin_seconds"]

    previous_scheduled: int | None = None
    previous_completed: int | None = None
    for observation in observations:
        scheduled = observation["scheduled_at_seconds"]
        completed = observation["completed_at_seconds"]

        if scheduled <= origin or (scheduled - origin) % interval != 0:
            return _blocked("ATTEMPT_OFF_FIXED_RATE_GRID")
        if completed < scheduled:
            return _blocked("READ_COMPLETION_PRECEDES_ATTEMPT_START")
        if previous_scheduled is not None:
            if scheduled == previous_scheduled:
                return _blocked("DUPLICATE_FIXED_RATE_SLOT")
            if scheduled - previous_scheduled != interval:
                return _blocked("CADENCE_GAP")
            if previous_completed is not None and previous_completed > scheduled:
                return _blocked("ATTEMPT_OVERLAP")
        previous_scheduled = scheduled
        previous_completed = completed

        if (
            observation["outcome"] == "REMOTE_HEAD_OBSERVED"
            and observation["observed_head"] == target_head
            and scheduled < source_release_at_seconds
        ):
            return _blocked(
                "TARGET_HEAD_OBSERVED_BEFORE_CONTROLLED_RELEASE"
            )

    last_observation = observations[-1]
    if (
        last_observation["completed_at_seconds"]
        > last_observation["scheduled_at_seconds"] + interval
    ):
        return _blocked("ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT")

    first_required_slot = _first_fixed_rate_slot_at_or_after(
        instant_seconds=source_release_at_seconds,
        interval=interval,
        origin=origin,
    )
    scheduled_slots = {
        observation["scheduled_at_seconds"] for observation in observations
    }
    if (
        any(slot >= first_required_slot for slot in scheduled_slots)
        and first_required_slot not in scheduled_slots
    ):
        return _blocked("SKIPPED_REQUIRED_ATTEMPT")

    first_detection: dict[str, Any] | None = None
    for observation in observations:
        if observation["scheduled_at_seconds"] < source_release_at_seconds:
            continue
        if (
            observation["outcome"] == "REMOTE_HEAD_OBSERVED"
            and observation["observed_head"] == target_head
        ):
            first_detection = observation
            break

    if first_detection is not None:
        completed = first_detection["completed_at_seconds"]
        latency = completed - source_release_at_seconds
        if latency <= bound:
            status = "PASS_DETECTED_WITHIN_BOUND"
            failure_code = None
        else:
            status = "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED"
            failure_code = "DETECTION_COMPLETION_EXCEEDED_BOUND"
        return _result(
            status=status,
            failure_code=failure_code,
            detection_latency_seconds=latency,
            first_detection_scheduled_at_seconds=(
                first_detection["scheduled_at_seconds"]
            ),
            first_detection_completed_at_seconds=completed,
            observed_head=first_detection["observed_head"],
        )

    last_scheduled = observations[-1]["scheduled_at_seconds"]
    next_required_slot = last_scheduled + interval
    if next_required_slot - source_release_at_seconds > bound:
        return _result(
            status="FAIL_NO_DETECTION_BY_BOUND",
            failure_code="NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND",
            detection_latency_seconds=None,
            first_detection_scheduled_at_seconds=None,
            first_detection_completed_at_seconds=None,
            observed_head=None,
        )

    return _result(
        status="INCOMPLETE_SYNTHETIC_WINDOW",
        failure_code=None,
        detection_latency_seconds=None,
        first_detection_scheduled_at_seconds=None,
        first_detection_completed_at_seconds=None,
        observed_head=None,
    )

~~~~

# SOURCE: P5-D2 OBSERVER TICK
Path: tools/obsidian_projection/observer_tick.py
~~~~
from __future__ import annotations

import hashlib
import json
import re
from typing import Any


class ObserverTickError(RuntimeError):
    pass


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
EXPECTED_BRANCH = "integration/system-v1"
CONTRACT_BLOB = "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3"

STATE_SCHEMA = "ATDS_OBSIDIAN_OBSERVER_STATE_V0_1"
INPUT_SCHEMA = "ATDS_OBSIDIAN_OBSERVER_INPUT_V0_1"
DECISION_SCHEMA = "ATDS_OBSIDIAN_OBSERVER_DECISION_V0_1"
EVENT_SCHEMA = "ATDS_OBSIDIAN_OBSERVER_EVENT_V0_1"
RESULT_SCHEMA = "ATDS_OBSIDIAN_ONE_SHOT_TICK_RESULT_V0_1"

OBSERVER_PHASES = frozenset(
    {
        "IDLE",
        "CANDIDATE_PENDING",
        "EVALUATING",
        "BLOCKED",
        "STOPPED",
    }
)
REMOTE_FRESHNESS = frozenset({"KNOWN", "UNKNOWN"})
PROJECTION_STATES = frozenset(
    {
        "CURRENT",
        "STALE",
        "BLOCKED",
        "ORPHAN",
        "MISSING",
    }
)
EVENT_TYPES = frozenset(
    {
        "BOOTSTRAP",
        "REMOTE_HEAD_OBSERVED",
        "REMOTE_OBSERVATION_FAILED",
        "EVALUATION_STARTED",
        "EVALUATION_PASSED",
        "EVALUATION_FAILED",
        "PROMOTION_CONFIRMED",
        "PROMOTION_FAILED",
        "LOCK_CONTENDED",
        "SHUTDOWN_REQUESTED",
    }
)
TRANSITION_CLASSES = frozenset(
    {
        "INITIAL",
        "SAME",
        "FAST_FORWARD",
        "NON_FAST_FORWARD",
        "UNKNOWN",
    }
)

_STATE_KEYS = frozenset(
    {
        "schema",
        "repository",
        "branch",
        "observer_phase",
        "remote_freshness",
        "latest_observed_head",
        "last_qualified_head",
        "live_projection_head",
        "projection_state",
        "pending_heads",
        "blocked_head",
        "last_failure_code",
        "last_event_sequence",
    }
)
_INPUT_KEYS = frozenset(
    {
        "schema",
        "event_type",
        "sequence",
        "observed_head",
        "transition_class",
        "candidate_head",
        "failure_code",
    }
)

_HEAD_RE = re.compile(r"^[0-9a-f]{40}$")


def _canonical_json_bytes(value: Any) -> bytes:
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ObserverTickError(
            "value is not canonical JSON"
        ) from exc
    return (encoded + "\n").encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(
        _canonical_json_bytes(value)
    ).hexdigest()


def _clone(value: Any) -> Any:
    try:
        return json.loads(
            _canonical_json_bytes(value).decode("utf-8")
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ObserverTickError(
            "canonical clone failed"
        ) from exc


def _is_head(value: Any) -> bool:
    return (
        isinstance(value, str)
        and _HEAD_RE.fullmatch(value) is not None
    )


def _require_optional_head(
    value: Any,
    field: str,
) -> None:
    if value is not None and not _is_head(value):
        raise ObserverTickError(
            f"{field} must be lowercase 40-hex SHA-1 or null"
        )


def _require_failure_code(
    value: Any,
    *,
    required: bool,
) -> None:
    if required:
        if (
            not isinstance(value, str)
            or not value
            or value.strip() != value
        ):
            raise ObserverTickError(
                "failure_code required"
            )
        return
    if value is not None:
        raise ObserverTickError(
            "failure_code must be null"
        )


def _validate_state(state: dict[str, Any]) -> None:
    if not isinstance(state, dict):
        raise ObserverTickError("state must be an object")
    if frozenset(state) != _STATE_KEYS:
        raise ObserverTickError("state fields mismatch")
    if state["schema"] != STATE_SCHEMA:
        raise ObserverTickError("state schema mismatch")
    if state["repository"] != EXPECTED_REPOSITORY:
        raise ObserverTickError("repository mismatch")
    if state["branch"] != EXPECTED_BRANCH:
        raise ObserverTickError("branch mismatch")
    if state["observer_phase"] not in OBSERVER_PHASES:
        raise ObserverTickError("invalid observer phase")
    if state["remote_freshness"] not in REMOTE_FRESHNESS:
        raise ObserverTickError("invalid remote freshness")
    if state["projection_state"] not in PROJECTION_STATES:
        raise ObserverTickError("invalid projection state")

    _require_optional_head(
        state["latest_observed_head"],
        "latest_observed_head",
    )
    _require_optional_head(
        state["last_qualified_head"],
        "last_qualified_head",
    )
    _require_optional_head(
        state["live_projection_head"],
        "live_projection_head",
    )
    _require_optional_head(
        state["blocked_head"],
        "blocked_head",
    )

    pending = state["pending_heads"]
    if not isinstance(pending, list):
        raise ObserverTickError(
            "pending_heads must be an array"
        )
    if not all(_is_head(item) for item in pending):
        raise ObserverTickError(
            "pending_heads contains invalid HEAD"
        )
    if len(pending) != len(set(pending)):
        raise ObserverTickError(
            "pending_heads contains duplicate HEAD"
        )

    failure = state["last_failure_code"]
    if failure is not None and (
        not isinstance(failure, str)
        or not failure
        or failure.strip() != failure
    ):
        raise ObserverTickError(
            "invalid last_failure_code"
        )

    sequence = state["last_event_sequence"]
    if (
        isinstance(sequence, bool)
        or not isinstance(sequence, int)
        or sequence < 0
    ):
        raise ObserverTickError(
            "invalid last_event_sequence"
        )

    if state["projection_state"] == "CURRENT":
        if state["remote_freshness"] != "KNOWN":
            raise ObserverTickError(
                "CURRENT requires KNOWN remote freshness"
            )
        live = state["live_projection_head"]
        if live is None:
            raise ObserverTickError(
                "CURRENT requires live projection HEAD"
            )
        if state["latest_observed_head"] != live:
            raise ObserverTickError(
                "CURRENT requires observed == live"
            )
        if state["last_qualified_head"] != live:
            raise ObserverTickError(
                "CURRENT requires live == qualified"
            )

    if (
        state["observer_phase"] == "EVALUATING"
        and not pending
    ):
        raise ObserverTickError(
            "EVALUATING requires pending queue head"
        )

    if (
        state["observer_phase"] == "CANDIDATE_PENDING"
        and state["last_qualified_head"] is None
    ):
        raise ObserverTickError(
            "CANDIDATE_PENDING requires qualified HEAD"
        )

    if state["observer_phase"] == "BLOCKED":
        if state["projection_state"] != "BLOCKED":
            raise ObserverTickError(
                "BLOCKED phase requires BLOCKED projection"
            )
        if state["blocked_head"] is None:
            raise ObserverTickError(
                "BLOCKED phase requires blocked HEAD"
            )
        if state["last_failure_code"] is None:
            raise ObserverTickError(
                "BLOCKED phase requires failure code"
            )


def _validate_input(
    previous_state: dict[str, Any],
    event: dict[str, Any],
) -> None:
    if not isinstance(event, dict):
        raise ObserverTickError("input must be an object")
    if frozenset(event) != _INPUT_KEYS:
        raise ObserverTickError("input fields mismatch")
    if event["schema"] != INPUT_SCHEMA:
        raise ObserverTickError("input schema mismatch")
    if event["event_type"] not in EVENT_TYPES:
        raise ObserverTickError("invalid event type")

    sequence = event["sequence"]
    if (
        isinstance(sequence, bool)
        or not isinstance(sequence, int)
        or sequence
        != previous_state["last_event_sequence"] + 1
    ):
        raise ObserverTickError(
            "input sequence must advance exactly once"
        )

    _require_optional_head(
        event["observed_head"],
        "observed_head",
    )
    _require_optional_head(
        event["candidate_head"],
        "candidate_head",
    )

    transition_class = event["transition_class"]
    if (
        transition_class is not None
        and transition_class not in TRANSITION_CLASSES
    ):
        raise ObserverTickError(
            "invalid transition class"
        )

    event_type = event["event_type"]

    if event_type == "REMOTE_HEAD_OBSERVED":
        if event["observed_head"] is None:
            raise ObserverTickError(
                "REMOTE_HEAD_OBSERVED requires observed_head"
            )
        if transition_class is None:
            raise ObserverTickError(
                "REMOTE_HEAD_OBSERVED requires transition_class"
            )
        if event["candidate_head"] is not None:
            raise ObserverTickError(
                "remote observation forbids candidate_head"
            )
        _require_failure_code(
            event["failure_code"],
            required=False,
        )
        return

    if event_type == "REMOTE_OBSERVATION_FAILED":
        if (
            event["observed_head"] is not None
            or transition_class is not None
            or event["candidate_head"] is not None
        ):
            raise ObserverTickError(
                "remote failure carries no HEAD"
            )
        _require_failure_code(
            event["failure_code"],
            required=True,
        )
        return

    if event_type in {
        "EVALUATION_STARTED",
        "EVALUATION_PASSED",
        "PROMOTION_CONFIRMED",
    }:
        if (
            event["observed_head"] is not None
            or transition_class is not None
            or event["candidate_head"] is None
        ):
            raise ObserverTickError(
                f"{event_type} normalized fields invalid"
            )
        _require_failure_code(
            event["failure_code"],
            required=False,
        )
        return

    if event_type in {
        "EVALUATION_FAILED",
        "PROMOTION_FAILED",
    }:
        if (
            event["observed_head"] is not None
            or transition_class is not None
            or event["candidate_head"] is None
        ):
            raise ObserverTickError(
                f"{event_type} normalized fields invalid"
            )
        _require_failure_code(
            event["failure_code"],
            required=True,
        )
        return

    if event_type == "LOCK_CONTENDED":
        if (
            event["observed_head"] is not None
            or transition_class is not None
            or event["candidate_head"] is not None
            or event["failure_code"] != "LOCK_CONTENDED"
        ):
            raise ObserverTickError(
                "LOCK_CONTENDED normalized fields invalid"
            )
        return

    if (
        event["observed_head"] is not None
        or transition_class is not None
        or event["candidate_head"] is not None
    ):
        raise ObserverTickError(
            f"{event_type} carries unexpected HEAD"
        )
    _require_failure_code(
        event["failure_code"],
        required=False,
    )


def make_initial_state() -> dict[str, Any]:
    state = {
        "schema": STATE_SCHEMA,
        "repository": EXPECTED_REPOSITORY,
        "branch": EXPECTED_BRANCH,
        "observer_phase": "IDLE",
        "remote_freshness": "UNKNOWN",
        "latest_observed_head": None,
        "last_qualified_head": None,
        "live_projection_head": None,
        "projection_state": "MISSING",
        "pending_heads": [],
        "blocked_head": None,
        "last_failure_code": None,
        "last_event_sequence": 0,
    }
    _validate_state(state)
    return state


def _decision(
    *,
    action: str,
    reason_code: str,
    observed_head: str | None,
    candidate_head: str | None,
    previous_live_head: str | None,
    next_projection_state: str,
) -> dict[str, Any]:
    return {
        "schema": DECISION_SCHEMA,
        "action": action,
        "reason_code": reason_code,
        "observed_head": observed_head,
        "candidate_head": candidate_head,
        "previous_live_head": previous_live_head,
        "next_projection_state": next_projection_state,
        "automatic_promotion_authorized": False,
        "production_write_authorized": False,
    }


def _apply_remote_observed(
    state: dict[str, Any],
    event: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    observed = event["observed_head"]
    transition_class = event["transition_class"]
    previous_live = state["live_projection_head"]
    previous_observed = state["latest_observed_head"]

    if transition_class == "INITIAL":
        if previous_observed is not None:
            raise ObserverTickError(
                "INITIAL requires no previous observed HEAD"
            )
    elif transition_class == "SAME":
        if previous_observed != observed:
            raise ObserverTickError(
                "SAME requires previous observed HEAD equality"
            )
    else:
        if previous_observed is None:
            raise ObserverTickError(
                f"{transition_class} requires previous observed HEAD"
            )
        if previous_observed == observed:
            raise ObserverTickError(
                f"{transition_class} requires a new observed HEAD"
            )

    if state["observer_phase"] == "BLOCKED":
        if (
            transition_class == "SAME"
            and state["latest_observed_head"] != observed
        ):
            raise ObserverTickError(
                "SAME requires previous observed HEAD equality"
            )
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        decision = _decision(
            action="BLOCK_REQUIRES_ADJUDICATION",
            reason_code="OBSERVER_ALREADY_BLOCKED",
            observed_head=observed,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state="BLOCKED",
        )
        return next_state, decision

    if transition_class == "SAME":
        if state["latest_observed_head"] != observed:
            raise ObserverTickError(
                "SAME requires previous observed HEAD equality"
            )
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        next_state["last_failure_code"] = None
        if (
            next_state["observer_phase"] != "BLOCKED"
            and next_state["live_projection_head"] is not None
            and next_state["live_projection_head"] == observed
            and next_state["last_qualified_head"] == observed
        ):
            next_state["projection_state"] = "CURRENT"
        decision = _decision(
            action="NOOP",
            reason_code="REMOTE_HEAD_SAME",
            observed_head=observed,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=next_state[
                "projection_state"
            ],
        )
        return next_state, decision

    if transition_class == "INITIAL":
        if state["latest_observed_head"] is not None:
            raise ObserverTickError(
                "INITIAL requires no previous observed HEAD"
            )
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        next_state["last_failure_code"] = None
        if observed not in next_state["pending_heads"]:
            next_state["pending_heads"].append(observed)
        next_state["projection_state"] = (
            "MISSING"
            if next_state["live_projection_head"] is None
            else "STALE"
        )
        decision = _decision(
            action="QUEUE_EXACT_HEAD_FOR_EVALUATION",
            reason_code="REMOTE_HEAD_INITIAL_QUEUED",
            observed_head=observed,
            candidate_head=observed,
            previous_live_head=previous_live,
            next_projection_state=next_state[
                "projection_state"
            ],
        )
        return next_state, decision

    if state["latest_observed_head"] is None:
        raise ObserverTickError(
            f"{transition_class} requires previous observed HEAD"
        )
    if state["latest_observed_head"] == observed:
        raise ObserverTickError(
            f"{transition_class} requires a new observed HEAD"
        )

    if transition_class == "FAST_FORWARD":
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        next_state["last_failure_code"] = None
        if observed not in next_state["pending_heads"]:
            next_state["pending_heads"].append(observed)
        next_state["projection_state"] = "STALE"
        decision = _decision(
            action="QUEUE_EXACT_HEAD_FOR_EVALUATION",
            reason_code="REMOTE_HEAD_FAST_FORWARD_QUEUED",
            observed_head=observed,
            candidate_head=observed,
            previous_live_head=previous_live,
            next_projection_state="STALE",
        )
        return next_state, decision

    if transition_class in {
        "NON_FAST_FORWARD",
        "UNKNOWN",
    }:
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        next_state["observer_phase"] = "BLOCKED"
        next_state["projection_state"] = "BLOCKED"
        next_state["blocked_head"] = observed
        next_state["last_failure_code"] = (
            "NON_FAST_FORWARD_REQUIRES_ADJUDICATION"
            if transition_class == "NON_FAST_FORWARD"
            else "UNKNOWN_ANCESTRY_REQUIRES_ADJUDICATION"
        )
        decision = _decision(
            action="BLOCK_REQUIRES_ADJUDICATION",
            reason_code=next_state["last_failure_code"],
            observed_head=observed,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state="BLOCKED",
        )
        return next_state, decision

    raise ObserverTickError(
        "unsupported remote transition class"
    )


def _apply_transition(
    state: dict[str, Any],
    event: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    event_type = event["event_type"]
    previous_live = state["live_projection_head"]

    if state["observer_phase"] == "STOPPED":
        raise ObserverTickError(
            "STOPPED observer accepts no further events"
        )

    if event_type == "BOOTSTRAP":
        if state["last_event_sequence"] != 0:
            raise ObserverTickError(
                "BOOTSTRAP allowed only at sequence zero"
            )
        if state != make_initial_state():
            raise ObserverTickError(
                "BOOTSTRAP requires canonical initial state"
            )
        next_state = _clone(state)
        decision = _decision(
            action="NOOP",
            reason_code="BOOTSTRAP_ACCEPTED",
            observed_head=None,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=state[
                "projection_state"
            ],
        )
        return next_state, decision

    if event_type == "REMOTE_HEAD_OBSERVED":
        return _apply_remote_observed(state, event)

    if event_type == "REMOTE_OBSERVATION_FAILED":
        next_state = _clone(state)
        next_state["remote_freshness"] = "UNKNOWN"
        next_state["last_failure_code"] = event[
            "failure_code"
        ]
        if next_state["projection_state"] == "CURRENT":
            next_state["projection_state"] = "STALE"
        decision = _decision(
            action="RETAIN_LAST_KNOWN_GOOD",
            reason_code="REMOTE_OBSERVATION_FAILED",
            observed_head=None,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=next_state[
                "projection_state"
            ],
        )
        return next_state, decision

    if event_type == "EVALUATION_STARTED":
        candidate = event["candidate_head"]
        if state["observer_phase"] != "IDLE":
            raise ObserverTickError(
                "evaluation may start only from IDLE"
            )
        if (
            not state["pending_heads"]
            or state["pending_heads"][0] != candidate
        ):
            raise ObserverTickError(
                "evaluation candidate must equal queue head"
            )
        next_state = _clone(state)
        next_state["observer_phase"] = "EVALUATING"
        decision = _decision(
            action="START_EXACT_HEAD_EVALUATION",
            reason_code="EVALUATION_STARTED",
            observed_head=None,
            candidate_head=candidate,
            previous_live_head=previous_live,
            next_projection_state=next_state[
                "projection_state"
            ],
        )
        return next_state, decision

    if event_type in {
        "EVALUATION_PASSED",
        "EVALUATION_FAILED",
    }:
        candidate = event["candidate_head"]
        if state["observer_phase"] != "EVALUATING":
            raise ObserverTickError(
                f"{event_type} requires EVALUATING phase"
            )
        if (
            not state["pending_heads"]
            or state["pending_heads"][0] != candidate
        ):
            raise ObserverTickError(
                "evaluation result candidate must equal queue head"
            )
        next_state = _clone(state)
        next_state["pending_heads"] = (
            next_state["pending_heads"][1:]
        )

        if event_type == "EVALUATION_PASSED":
            next_state["last_qualified_head"] = candidate
            next_state["observer_phase"] = (
                "CANDIDATE_PENDING"
            )
            next_state["blocked_head"] = None
            next_state["last_failure_code"] = None
            decision = _decision(
                action=(
                    "CANDIDATE_QUALIFIED_PENDING_PROMOTION"
                ),
                reason_code="EVALUATION_PASSED",
                observed_head=None,
                candidate_head=candidate,
                previous_live_head=previous_live,
                next_projection_state=next_state[
                    "projection_state"
                ],
            )
            return next_state, decision

        next_state["observer_phase"] = "BLOCKED"
        next_state["projection_state"] = "BLOCKED"
        next_state["blocked_head"] = candidate
        next_state["last_failure_code"] = event[
            "failure_code"
        ]
        decision = _decision(
            action="RETAIN_LAST_KNOWN_GOOD",
            reason_code="EVALUATION_FAILED",
            observed_head=None,
            candidate_head=candidate,
            previous_live_head=previous_live,
            next_projection_state="BLOCKED",
        )
        return next_state, decision

    if event_type in {
        "PROMOTION_CONFIRMED",
        "PROMOTION_FAILED",
    }:
        candidate = event["candidate_head"]
        if state["observer_phase"] != "CANDIDATE_PENDING":
            raise ObserverTickError(
                f"{event_type} requires CANDIDATE_PENDING"
            )
        if state["last_qualified_head"] != candidate:
            raise ObserverTickError(
                "promotion candidate must equal last qualified HEAD"
            )
        next_state = _clone(state)

        if event_type == "PROMOTION_CONFIRMED":
            next_state["live_projection_head"] = candidate
            next_state["observer_phase"] = "IDLE"
            next_state["blocked_head"] = None
            next_state["last_failure_code"] = None
            if (
                next_state["remote_freshness"] == "KNOWN"
                and next_state["latest_observed_head"]
                == candidate
            ):
                next_state["projection_state"] = "CURRENT"
            else:
                next_state["projection_state"] = "STALE"
            decision = _decision(
                action="CONFIRM_LIVE_PROJECTION",
                reason_code="PROMOTION_CONFIRMED",
                observed_head=None,
                candidate_head=candidate,
                previous_live_head=previous_live,
                next_projection_state=next_state[
                    "projection_state"
                ],
            )
            return next_state, decision

        next_state["observer_phase"] = "BLOCKED"
        next_state["projection_state"] = "BLOCKED"
        next_state["blocked_head"] = candidate
        next_state["last_failure_code"] = event[
            "failure_code"
        ]
        decision = _decision(
            action="RETAIN_LAST_KNOWN_GOOD",
            reason_code="PROMOTION_FAILED",
            observed_head=None,
            candidate_head=candidate,
            previous_live_head=previous_live,
            next_projection_state="BLOCKED",
        )
        return next_state, decision

    if event_type == "LOCK_CONTENDED":
        next_state = _clone(state)
        decision = _decision(
            action="NOOP",
            reason_code="LOCK_CONTENDED",
            observed_head=None,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=state[
                "projection_state"
            ],
        )
        return next_state, decision

    if event_type == "SHUTDOWN_REQUESTED":
        next_state = _clone(state)
        next_state["observer_phase"] = "STOPPED"
        decision = _decision(
            action="STOP",
            reason_code="SHUTDOWN_REQUESTED",
            observed_head=None,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=state[
                "projection_state"
            ],
        )
        return next_state, decision

    raise ObserverTickError("unsupported event type")


def one_shot_tick(
    previous_state: dict[str, Any],
    normalized_input: dict[str, Any],
) -> dict[str, Any]:
    previous = _clone(previous_state)
    event = _clone(normalized_input)

    _validate_state(previous)
    _validate_input(previous, event)

    next_state, decision = _apply_transition(
        previous,
        event,
    )
    next_state["last_event_sequence"] = event["sequence"]

    _validate_state(next_state)

    audit = {
        "schema": EVENT_SCHEMA,
        "sequence": event["sequence"],
        "event_type": event["event_type"],
        "previous_state_digest": _digest(previous),
        "input_digest": _digest(event),
        "decision_digest": _digest(decision),
        "next_state_digest": _digest(next_state),
        "reason_code": decision["reason_code"],
    }

    result = {
        "schema": RESULT_SCHEMA,
        "next_state": next_state,
        "decision": decision,
        "audit": audit,
    }

    _canonical_json_bytes(result)
    return result


def canonical_result_bytes(
    result: dict[str, Any],
) -> bytes:
    return _canonical_json_bytes(result)

~~~~

# SOURCE: P5-D4 BOUNDED LOOP CONTRACT
Path: tools/obsidian_projection/p5d4_bounded_observer_loop_contract_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_P5D4_BOUNDED_OBSERVER_LOOP_CONTRACT_V0_1",
  "status": "CANDIDATE_PREREGISTRATION_ONLY",
  "source_repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "monitored_source": {
    "remote": "origin",
    "branch": "integration/system-v1",
    "canonical_authority": "GITHUB_REMOTE_BRANCH",
    "local_working_tree_is_not_authority": true
  },
  "frontier": "P5-D4-BOUNDED-OBSERVER-LOOP-CANDIDATE",
  "title": "BOUNDED_OBSERVER_LOOP_CONTRACT",
  "purpose": "Define a finite, persistent and auditable orchestration envelope around already-qualified P5-D2/P5-D3 one-shot primitives without creating implicit promotion authority, permanent background execution, or P5-E near-real-time authority.",
  "qualified_predecessors": {
    "p5d1_observer_core_contract_blob": "a20999ae991e07447e25ecd1592964f2d333449b",
    "p5d2_one_shot_contract_blob": "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3",
    "p5d2_observer_tick_blob": "fd212f61ec38332b677110f40265638af55a73e2",
    "p5d3d_finite_evaluator_contract_blob": "b6c17167875874db30a575be95e8e6aa33d630dd",
    "p5d3d_finite_evaluator_blob": "bff5f51abbb344c1ccc5e9c669a11cf0e26c2562",
    "p5d3e_real_exact_head_sandbox_contract_blob": "ae4b1691fae16fcd1616e265a089670b9654db4a",
    "p5d3e_verifier_blob": "bd7f63b08432a53eaff5deeb2147396eb60d723f",
    "p5d3f_handoff_contract_blob": "64744325251db350d26c0269090ce62d5fa5f2e8",
    "p5d3f_handoff_blob": "23a4cc69b3b9f6fab1a6d77bed0247fce9b69c60",
    "p5d3g_live_publication_contract_blob": "64997ddd9977229961387f66af4de356c045c0ac",
    "p5d3g_live_publication_blob": "956ccb7274cea366b1a414df5a9239cbf580e3bf",
    "p5d3g_stage_b_gate_contract_blob": "c5c7fbb52f3dd2e3d3f5d1c1bbdc1069e2dabead",
    "p5d3g_stage_b_prestate_rebind_amendment_blob": "441fea40d33aa85dcfc6305d4d32cef39c42388e",
    "p5d3g_stage_b_runtime_blob": "077ea7a428f90d64122f15fe6b52f342f329f7b6"
  },
  "core_authority_model": {
    "observer_semantic_state_mutation_authority": "P5D2_ONE_SHOT_TICK_ONLY",
    "direct_observer_state_mutation_forbidden": true,
    "p5d3_primitive_reimplementation_forbidden": true,
    "loop_authority_is_not_promotion_authority": true,
    "qualified_candidate_requires_separate_promotion_authority": true,
    "candidate_pending_without_separate_authority_result": "PROMOTION_AUTHORITY_REQUIRED",
    "automatic_live_publication_authorized": false,
    "implicit_stage_a_authority_authorized": false,
    "implicit_stage_b_authority_authorized": false,
    "historical_stage_a_or_stage_b_authority_reuse_forbidden": true
  },
  "schemas": {
    "loop_plan": "ATDS_OBSIDIAN_P5D4_LOOP_PLAN_V0_1",
    "loop_checkpoint": "ATDS_OBSIDIAN_P5D4_LOOP_CHECKPOINT_V0_1",
    "loop_event": "ATDS_OBSIDIAN_P5D4_LOOP_EVENT_V0_1",
    "ownership_record": "ATDS_OBSIDIAN_P5D4_OWNERSHIP_RECORD_V0_1",
    "reconciliation_report": "ATDS_OBSIDIAN_P5D4_RECONCILIATION_REPORT_V0_1"
  },
  "bounded_loop_envelope": {
    "every_run_requires_explicit_canonical_plan": true,
    "plan_digest_required": true,
    "unbounded_defaults_forbidden": true,
    "required_limits": {
      "max_cycles": {
        "type": "POSITIVE_INTEGER",
        "minimum": 1
      },
      "max_remote_observations": {
        "type": "POSITIVE_INTEGER",
        "minimum": 1
      },
      "max_evaluations": {
        "type": "NONNEGATIVE_INTEGER",
        "minimum": 0
      },
      "max_pending_heads": {
        "type": "POSITIVE_INTEGER",
        "minimum": 1
      },
      "max_consecutive_failures": {
        "type": "NONNEGATIVE_INTEGER",
        "minimum": 0
      }
    },
    "cycle_budget_consumed_exactly_once_per_started_cycle": true,
    "budget_check_required_before_starting_next_cycle": true,
    "bound_reached_must_not_inject_p5d2_shutdown_event": true,
    "bound_reached_is_runner_stop_not_semantic_state_transition": true,
    "loop_construct_without_verified_budget_forbidden": true,
    "allowed_terminal_reasons": [
      "BOUND_REACHED",
      "NO_PENDING_WORK",
      "BLOCKED_REQUIRES_ADJUDICATION",
      "PROMOTION_AUTHORITY_REQUIRED",
      "SHUTDOWN_REQUESTED",
      "LOCK_CONTENDED",
      "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
      "RECONCILIATION_REQUIRED",
      "FATAL_INCONSISTENCY"
    ],
    "terminal_reason_must_be_persisted": true,
    "new_cycle_after_terminal_reason_forbidden": true
  },
  "durable_observer_state_checkpoint": {
    "required": true,
    "location_class": "LOCALAPPDATA_OUTSIDE_VAULT",
    "candidate_root_expression": "%LOCALAPPDATA%\\ATDS-OBSIDIAN-PROJECTION\\P5D4",
    "inside_real_vault_forbidden": true,
    "inside_canonical_repository_forbidden": true,
    "canonical_json_required": true,
    "utf8_required": true,
    "terminal_lf_required": true,
    "sha256_required": true,
    "required_fields": [
      "schema",
      "loop_plan_digest_sha256",
      "observer_state",
      "observer_state_digest_sha256",
      "last_event_sequence",
      "last_event_digest_sha256",
      "checkpoint_generation"
    ],
    "observer_state_must_validate_under_p5d2": true,
    "last_event_sequence_must_equal_observer_state_last_event_sequence": true,
    "volatile_host_data_excluded_from_observer_state_digest": [
      "pid",
      "hostname",
      "wall_clock_time",
      "absolute_runtime_path",
      "process_start_time"
    ],
    "commit_protocol": [
      "BUILD_NEXT_STATE_ONLY_VIA_P5D2_ONE_SHOT_TICK",
      "BUILD_CANONICAL_LOOP_EVENT",
      "APPEND_AND_DURABLY_FLUSH_LOOP_EVENT",
      "WRITE_CHECKPOINT_TO_SIBLING_TEMP",
      "DURABLY_FLUSH_CHECKPOINT_TEMP",
      "ATOMIC_REPLACE_CHECKPOINT",
      "VERIFY_CHECKPOINT_READ_AFTER_WRITE"
    ],
    "checkpoint_may_not_be_committed_before_corresponding_event": true,
    "direct_in_place_checkpoint_overwrite_forbidden": true
  },
  "append_only_observer_event_log": {
    "required": true,
    "location_class": "LOCALAPPDATA_OUTSIDE_VAULT",
    "format": "CANONICAL_JSONL",
    "append_only": true,
    "truncate_forbidden": true,
    "rewrite_prior_record_forbidden": true,
    "durable_flush_required_before_checkpoint_replace": true,
    "every_accepted_p5d2_tick_requires_record": true,
    "required_fields": [
      "schema",
      "sequence",
      "loop_id",
      "cycle_index",
      "normalized_input",
      "p5d2_audit",
      "previous_state_digest_sha256",
      "next_state_digest_sha256",
      "previous_record_digest_sha256",
      "record_digest_sha256",
      "record_origin"
    ],
    "record_origin_allowed": [
      "LIVE_BOUNDED_LOOP",
      "EVIDENCE_RECONSTRUCTION"
    ],
    "hash_chain_required": true,
    "sequence_strictly_monotonic": true,
    "duplicate_sequence_forbidden": true,
    "unterminated_or_noncanonical_tail_requires_reconciliation": true,
    "event_log_is_evidence_not_source_authority": true
  },
  "queue_capacity_policy": {
    "runtime_capacity_source": "loop_plan.max_pending_heads",
    "fifo_required": true,
    "unique_heads_required": true,
    "silent_drop_forbidden": true,
    "silent_reorder_forbidden": true,
    "latest_only_replacement_forbidden": true,
    "direct_queue_mutation_outside_p5d2_forbidden": true,
    "coalescing_authorized": false,
    "reason_coalescing_closed": "P5-D2 has no qualified queue-coalescing semantic event in V0.1",
    "preflight_capacity_check_required_before_event_that_would_append": true,
    "capacity_exhausted_result": "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
    "capacity_exhausted_must_not_feed_mutating_event_to_p5d2": true,
    "active_evaluation_candidate_retargeting_forbidden": true
  },
  "single_instance_ownership": {
    "required": true,
    "scope": "P5D4_CONTROL_STATE_ROOT",
    "exclusive_ownership_record_required": true,
    "ownership_record_outside_vault": true,
    "second_instance_result": "NO_WRITE_BLOCKED_BY_LOCK",
    "second_instance_may_observe_only": false,
    "second_instance_may_advance_sequence": false,
    "second_instance_may_modify_checkpoint": false,
    "second_instance_may_append_event": false,
    "second_instance_may_start_evaluation": false,
    "stale_or_ambiguous_lock_auto_steal_authorized": false,
    "stale_or_ambiguous_lock_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "volatile_ownership_metadata_must_not_enter_semantic_observer_digest": true
  },
  "restart_reconciliation_protocol": {
    "required_before_any_loop_continuation_after_restart": true,
    "authority_order": [
      "GITHUB_REMOTE_BRANCH_SOURCE_AUTHORITY",
      "VERIFIED_PHYSICAL_CURRENT_PUBLICATION_FACT",
      "P5D4_CHECKPOINT_DERIVED_OPERATIONAL_STATE",
      "P5D4_EVENT_LOG_AUDIT_EVIDENCE"
    ],
    "fresh_remote_read_only_observation_required": true,
    "physical_current_verification_required": true,
    "checkpoint_validation_required_if_present": true,
    "event_log_tail_validation_required_if_present": true,
    "allowed_checkpoint_log_relation": [
      "EXACTLY_ALIGNED",
      "LOG_EXACTLY_ONE_RECORD_AHEAD_WITH_REPLAYABLE_TRANSITION"
    ],
    "checkpoint_ahead_of_log_forbidden": true,
    "log_more_than_one_record_ahead_forbidden": true,
    "one_record_ahead_recovery": {
      "requires_previous_state_digest_match_checkpoint": true,
      "requires_deterministic_replay_via_p5d2_one_shot_tick": true,
      "requires_replayed_next_state_digest_match_log": true,
      "action": "ADVANCE_CHECKPOINT_ONLY_AFTER_REPLAY_MATCH"
    },
    "current_head_checkpoint_live_head_mismatch_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "event_tail_checkpoint_sequence_mismatch_unrecoverable_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "remote_non_fast_forward_or_unknown_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "restart_may_not_repeat_completed_evaluation_without_evidence": true,
    "restart_may_not_repeat_completed_promotion_without_evidence": true,
    "no_checkpoint_no_log_current_absent_result": "INITIALIZE_CANONICAL_P5D2_STATE",
    "no_checkpoint_no_log_current_present_result": "EVIDENCE_RECONSTRUCTION_REQUIRED",
    "evidence_reconstruction": {
      "direct_state_assignment_forbidden": true,
      "must_start_from_p5d2_make_initial_state": true,
      "must_use_p5d2_one_shot_tick_for_each_semantic_transition": true,
      "verified_current_identity_required": true,
      "matching_p5d3g_physical_and_logical_receipts_required": true,
      "reconstructed_event_records_must_use_origin": "EVIDENCE_RECONSTRUCTION",
      "reconstruction_must_not_claim_new_evaluation_or_new_publication_execution": true,
      "missing_or_ambiguous_p5d3g_evidence_result": "BLOCKED_REQUIRES_ADJUDICATION"
    }
  },
  "observation_adapter_boundary": {
    "remote_io_outside_p5d2_required": true,
    "normalized_event_injection_required": true,
    "one_shot_tick_network_io_remains_forbidden": true,
    "real_remote_observation_may_use_read_only_git": true,
    "time_based_polling_in_p5d4_v0_1_authorized": false,
    "sleep_or_timer_authorized": false,
    "p5e_owns_near_real_time_polling_qualification": true
  },
  "evaluation_orchestration": {
    "evaluation_may_start_only_on_p5d2_action": "START_EXACT_HEAD_EVALUATION",
    "evaluation_candidate_must_equal_queue_head": true,
    "candidate_head_frozen_for_entire_finite_evaluation": true,
    "new_remote_head_may_be_observed_while_evaluation_active_only_as_separately_queued_work": true,
    "active_evaluation_retarget_forbidden": true,
    "finite_evaluator_reuse_required": true,
    "qualified_evaluator_reimplementation_forbidden": true,
    "blocked_and_rejected_semantics_must_remain_distinct": true,
    "evaluation_result_must_reenter_state_only_via_p5d2_one_shot_tick": true
  },
  "promotion_boundary": {
    "candidate_pending_is_terminal_for_automatic_p5d4_orchestration": true,
    "required_stop_reason_without_separate_authority": "PROMOTION_AUTHORITY_REQUIRED",
    "p5d3f_or_p5d3g_invocation_from_loop_without_separate_authority_forbidden": true,
    "automatic_stage_a_authority_forbidden": true,
    "automatic_stage_b_authority_forbidden": true,
    "old_authorization_reuse_forbidden": true,
    "promotion_confirmed_may_enter_observer_state_only_from_verified_external_promotion_evidence": true,
    "promotion_failed_may_enter_observer_state_only_from_verified_external_failure_evidence": true
  },
  "failure_and_stop_semantics": {
    "fail_closed_default": true,
    "state_or_log_corruption_result": "FATAL_INCONSISTENCY",
    "unexpected_exception_result": "FATAL_INCONSISTENCY",
    "network_failure_must_not_create_current_claim": true,
    "last_known_good_live_projection_preserved_on_failure": true,
    "loop_stop_must_not_delete_checkpoint_or_event_log": true,
    "loop_stop_must_not_delete_last_known_good_generation": true
  },
  "contract_only_boundary": {
    "contract_and_tests_only": true,
    "loop_runtime_creation_authorized": false,
    "loop_runtime_modification_authorized": false,
    "bounded_loop_execution_authorized": false,
    "repeated_real_polling_authorized": false,
    "sleep_authorized": false,
    "timer_authorized": false,
    "permanent_daemon_authorized": false,
    "windows_startup_authorized": false,
    "scheduled_task_authorized": false,
    "windows_service_authorized": false,
    "real_vault_mutation_authorized": false,
    "automatic_publication_authorized": false,
    "implicit_stage_a_authority_authorized": false,
    "implicit_stage_b_authority_authorized": false,
    "p5e_authorized": false,
    "p6_authorized": false
  },
  "required_breakers": [
    "UNBOUNDED_LOOP_PLAN_ACCEPTED",
    "ZERO_OR_NEGATIVE_MAX_CYCLES_ACCEPTED",
    "CYCLE_STARTED_AFTER_BUDGET_EXHAUSTED",
    "BOUND_REACHED_INJECTS_P5D2_SHUTDOWN_EVENT",
    "NEW_CYCLE_AFTER_TERMINAL_REASON",
    "DIRECT_OBSERVER_STATE_MUTATION",
    "CHECKPOINT_INSIDE_REAL_VAULT",
    "CHECKPOINT_INSIDE_CANONICAL_REPOSITORY",
    "CHECKPOINT_DIRECT_IN_PLACE_OVERWRITE",
    "CHECKPOINT_COMMITTED_BEFORE_EVENT_APPEND",
    "CHECKPOINT_STATE_DIGEST_MISMATCH",
    "CHECKPOINT_SEQUENCE_DIFFERS_FROM_OBSERVER_STATE",
    "VOLATILE_HOST_DATA_LAUNDERED_INTO_SEMANTIC_DIGEST",
    "EVENT_LOG_TRUNCATED",
    "EVENT_LOG_PRIOR_RECORD_REWRITTEN",
    "EVENT_SEQUENCE_DUPLICATED",
    "EVENT_SEQUENCE_SKIPPED",
    "EVENT_HASH_CHAIN_BROKEN",
    "CHECKPOINT_AHEAD_OF_EVENT_LOG",
    "EVENT_LOG_MORE_THAN_ONE_RECORD_AHEAD",
    "ONE_RECORD_AHEAD_REPLAY_DIGEST_MISMATCH",
    "QUEUE_OVERFLOW_SILENT_DROP",
    "QUEUE_OVERFLOW_LATEST_ONLY_REPLACEMENT",
    "QUEUE_REORDERED",
    "QUEUE_DUPLICATE_HEAD",
    "QUEUE_MUTATED_OUTSIDE_P5D2",
    "QUEUE_COALESCING_WITHOUT_QUALIFIED_P5D2_EVENT",
    "ACTIVE_EVALUATION_RETARGETED",
    "SECOND_LOOP_RUNNER_ADVANCES_SEQUENCE",
    "SECOND_LOOP_RUNNER_WRITES_CHECKPOINT",
    "SECOND_LOOP_RUNNER_STARTS_EVALUATION",
    "STALE_LOCK_AUTO_STOLEN",
    "RESTART_CONTINUES_WITHOUT_RECONCILIATION",
    "CURRENT_DIFFERS_FROM_CHECKPOINT_LIVE_HEAD",
    "CHECKPOINT_LOG_TAIL_UNRECOVERABLE_MISMATCH_CONTINUES",
    "RESTART_REPEATS_COMPLETED_EVALUATION",
    "RESTART_REPEATS_COMPLETED_PROMOTION",
    "BOOTSTRAP_CURRENT_PRESENT_DIRECT_STATE_ASSIGNMENT",
    "BOOTSTRAP_CURRENT_PRESENT_WITHOUT_P5D3G_EVIDENCE",
    "EVIDENCE_RECONSTRUCTION_CLAIMS_NEW_PUBLICATION",
    "SAME_HEAD_TRIGGERS_EVALUATION",
    "REMOTE_NETWORK_FAILURE_MARKS_CURRENT",
    "NON_FAST_FORWARD_CONTINUES_AUTOMATICALLY",
    "UNKNOWN_ANCESTRY_CONTINUES_AUTOMATICALLY",
    "BLOCKED_RESULT_RELABELED_REJECTED",
    "REJECTED_RESULT_RELABELED_BLOCKED",
    "P5D3_FINITE_EVALUATOR_REIMPLEMENTED",
    "CANDIDATE_PENDING_AUTO_PUBLISHED",
    "P5D3F_CALLED_WITHOUT_SEPARATE_AUTHORITY",
    "P5D3G_CALLED_WITHOUT_SEPARATE_AUTHORITY",
    "OLD_STAGE_A_AUTHORITY_REUSED",
    "OLD_STAGE_B_AUTHORITY_REUSED",
    "PROMOTION_CONFIRMED_WITHOUT_VERIFIED_EXTERNAL_EVIDENCE",
    "LOOP_PUSHES_TO_GITHUB",
    "LOOP_COMMITS_CANONICAL_REPOSITORY",
    "LOOP_MUTATES_CANONICAL_WORKTREE",
    "LOOP_OVERWRITES_HUMAN_VIEWS",
    "LOOP_MODIFIES_OBSIDIAN_CONFIG",
    "REAL_VAULT_WRITE_SURFACE_INTRODUCED",
    "PERMANENT_DAEMON_SURFACE_INTRODUCED",
    "SLEEP_OR_TIMER_SURFACE_INTRODUCED",
    "WINDOWS_STARTUP_SURFACE_INTRODUCED",
    "SCHEDULED_TASK_SURFACE_INTRODUCED",
    "WINDOWS_SERVICE_SURFACE_INTRODUCED",
    "P5E_AUTHORITY_LEAK",
    "P6_AUTHORITY_LEAK"
  ],
  "qualification_requirements": {
    "static_contract_tests_required": true,
    "predecessor_pin_tests_required": true,
    "breaker_coverage_tests_required": true,
    "directly_affected_predecessor_contract_tests_required": [
      "P5D1_CONTINUOUS_OBSERVER_CORE_CONTRACT",
      "P5D2_ONE_SHOT_OBSERVER_TICK_CONTRACT",
      "P5D3A_CANDIDATE_EVALUATION_CONTRACT",
      "P5D3D_FINITE_CANDIDATE_EVALUATOR_CONTRACT",
      "P5D3G_LIVE_PUBLICATION_TRANSACTION_CONTRACT"
    ],
    "runtime_tests_required": false,
    "real_loop_execution_required": false,
    "real_vault_access_required": false
  },
  "next_gate": {
    "after_contract_qualification": "P5-D4-BOUNDED-OBSERVER-LOOP-RUNTIME-IMPLEMENTATION-CANDIDATE",
    "p5e": "END_TO_END_NEAR_REAL_TIME_QUALIFICATION",
    "p6": "CONTROLLED_KNOWLEDGE_GRAPH_ARCHITECTURE",
    "mandatory_human_stop_before_runtime": true
  }
}

~~~~

# SOURCE: P5-D3F REMOTE REF PATTERN
Path: tools/obsidian_projection/p5d3f_recovery_real_execution_v0_4.py
~~~~
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from tools.obsidian_projection.persistent_production_handoff import (
    PERSISTENT_STAGING,
    REAL_VAULT,
    PersistentHandoffPostSuccessCleanupBlockedError,
    execute_persistent_production_handoff,
    validate_persistent_paths,
    validate_staging_prestate,
)


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
RUNNER_BRANCH = (
    "feat/obsidian-projection-p5d3f-recovery-real-execution-runner-v0.4-monitored-head-pin"
)
MONITORED_BRANCH = "integration/system-v1"
EXPECTED_IMPLEMENTATION_BLOB = (
    "dcd70a9d9794675eab90e41df560f8b030b5dbf3"
)
EXPECTED_RECOVERY_IMPLEMENTATION_TEST_BLOB = (
    "242305bc0f95bbe243158b5c806255508093a357"
)
EXPECTED_RECOVERY_GATE_CONTRACT_BLOB = (
    "aef627936b6f745017bcace7e8a3e44270f95674"
)
EXPECTED_GATE_CONTRACT_BLOB = (
    "59ce9e079d256799d072405fa4a623ba58b75c0d"
)
EXPECTED_QUALIFIED_P5D3F_BLOB = (
    "2108131914cf65bb076b80f5bb63cd63267567fa"
)
RECOVERY_V04_REBIND_AMENDMENT_CONTRACT_BLOB = (
    "3667488c6cb7a348eab6564b7152049e0ba32d3b"
)
EFFECTIVE_RUNNER_BRANCH = (
    "feat/obsidian-projection-p5d3f-recovery-v04-qualified-blob-rebind-amendment-v0.1"
)
EFFECTIVE_IMPLEMENTATION_BLOB = (
    "375607d88bc926e4fd4c297ddc6fedba5506642a"
)
EFFECTIVE_QUALIFIED_P5D3F_BLOB = (
    "23a4cc69b3b9f6fab1a6d77bed0247fce9b69c60"
)

AUTHORIZATION_LITERAL = (
    "AUTHORIZE_ONE_P5D3F_PERSISTENT_READY_UNAUTHORIZED_HANDOFF"
)
AUTHORIZED_STAGING_PRESTATE = (
    "PRESENT_EMPTY_PACKAGES_RECOVERY"
)

OID40 = re.compile(r"^[0-9a-f]{40}$")
RUNNER_RELATIVE = (
    "tools/obsidian_projection/"
    "p5d3f_recovery_real_execution_v0_4.py"
)


class RealExecutionRunnerError(RuntimeError):
    pass


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _run(
    *args: str,
    cwd: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=str(cwd),
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "GIT_OPTIONAL_LOCKS": "0",
        },
    )


def _git(
    repo: Path,
    *args: str,
) -> str:
    result = _run(
        "git",
        *args,
        cwd=repo,
    )
    if result.returncode != 0:
        details = (
            (result.stderr or "").strip()
            or (result.stdout or "").strip()
        )
        raise RealExecutionRunnerError(
            "git command failed"
            + (f": {details}" if details else "")
        )
    return (result.stdout or "").strip()


def _normalize_origin(origin: str) -> str:
    value = origin.strip()
    for prefix in (
        "git@github.com:",
        "https://github.com/",
        "ssh://git@github.com/",
    ):
        if value.startswith(prefix):
            value = value[len(prefix):]
            break
    else:
        raise RealExecutionRunnerError(
            f"unsupported origin form: {origin}"
        )

    if value.endswith(".git"):
        value = value[:-4]

    return value.strip("/")


def _require_clean(repo: Path) -> None:
    dirty = _git(
        repo,
        "status",
        "--porcelain",
        "--untracked-files=all",
    )
    if dirty:
        raise RealExecutionRunnerError(
            "BLOCKED_CONTROL_CLONE_DIRTY: "
            + dirty
        )


def _committed_blob(
    repo: Path,
    relative: str,
) -> str:
    return _git(
        repo,
        "rev-parse",
        f"HEAD:{relative}",
    )


def _worktree_blob(
    repo: Path,
    relative: str,
) -> str:
    return _git(
        repo,
        "hash-object",
        "--no-filters",
        relative,
    )


def _verify_exact_runtime(
    repo: Path,
    expected_runner_head: str,
    expected_runner_blob: str,
) -> None:
    if _normalize_origin(
        _git(
            repo,
            "remote",
            "get-url",
            "origin",
        )
    ) != EXPECTED_REPOSITORY:
        raise RealExecutionRunnerError(
            "repository identity mismatch"
        )

    _require_clean(repo)

    local_head = _git(
        repo,
        "rev-parse",
        "HEAD",
    )
    if local_head != expected_runner_head:
        raise RealExecutionRunnerError(
            "local HEAD is not the authorized runner HEAD"
        )

    _git(
        repo,
        "fetch",
        "--no-tags",
        "origin",
        EFFECTIVE_RUNNER_BRANCH,
    )
    fetched = _git(
        repo,
        "rev-parse",
        "FETCH_HEAD",
    )
    if fetched != expected_runner_head:
        raise RealExecutionRunnerError(
            "BLOCKED_RUNNER_REMOTE_HEAD_RACE"
        )

    if _committed_blob(
        repo,
        RUNNER_RELATIVE,
    ) != expected_runner_blob:
        raise RealExecutionRunnerError(
            "governed runner committed blob mismatch"
        )

    if _worktree_blob(
        repo,
        RUNNER_RELATIVE,
    ) != expected_runner_blob:
        raise RealExecutionRunnerError(
            "governed runner worktree blob mismatch"
        )

    expected_blobs = {
        (
            "tools/obsidian_projection/"
            "p5d3f_recovery_v04_qualified_blob_rebind_amendment_contract_v0_1.json"
        ): RECOVERY_V04_REBIND_AMENDMENT_CONTRACT_BLOB,
        (
            "tools/obsidian_projection/"
            "persistent_production_handoff.py"
        ): EFFECTIVE_IMPLEMENTATION_BLOB,
        (
            "tests/obsidian_projection/"
            "test_p5d3f_persistent_handoff_recovery_implementation_v0_3.py"
        ): EXPECTED_RECOVERY_IMPLEMENTATION_TEST_BLOB,
        (
            "tools/obsidian_projection/"
            "persistent_production_handoff_gate_contract_v0_2.json"
        ): EXPECTED_RECOVERY_GATE_CONTRACT_BLOB,
        (
            "tools/obsidian_projection/"
            "persistent_production_handoff_gate_contract_v0_1.json"
        ): EXPECTED_GATE_CONTRACT_BLOB,
        (
            "tools/obsidian_projection/"
            "p5d3f_promotion_handoff.py"
        ): EFFECTIVE_QUALIFIED_P5D3F_BLOB,
    }

    for relative, expected_blob in (
        expected_blobs.items()
    ):
        actual = _committed_blob(
            repo,
            relative,
        )
        if actual != expected_blob:
            raise RealExecutionRunnerError(
                "qualified blob mismatch: "
                + relative
            )


def _verify_expected_monitored_head(
    repo: Path,
    expected_monitored_head: str,
) -> None:
    ref = (
        "refs/heads/"
        + MONITORED_BRANCH
    )
    parts = _git(
        repo,
        "ls-remote",
        "--heads",
        "origin",
        ref,
    ).split()

    if (
        len(parts) != 2
        or parts[1] != ref
        or parts[0] != expected_monitored_head
    ):
        raise RealExecutionRunnerError(
            "BLOCKED_MONITORED_HEAD_AUTHORITY_MISMATCH"
        )


def _require_authorized_prestate(
    prestate: str,
) -> None:
    if prestate != AUTHORIZED_STAGING_PRESTATE:
        raise RealExecutionRunnerError(
            "BLOCKED_UNAUTHORIZED_STAGING_PRESTATE: "
            + prestate
        )


def _validate_final_success_result(
    result: dict[str, object],
    expected_monitored_head: str,
) -> None:
    if result.get("candidate_head") != expected_monitored_head:
        raise RealExecutionRunnerError(
            "result candidate head differs from authorized monitored head"
        )

    if result.get("status") != (
        "PASS_PERSISTENT_PRODUCTION_HANDOFF_READY_UNAUTHORIZED"
    ):
        raise RealExecutionRunnerError(
            "unexpected persistent handoff status"
        )

    if result.get(
        "publication_authorized"
    ) is not False:
        raise RealExecutionRunnerError(
            "publication authority unexpectedly true"
        )

    if result.get(
        "live_publication_executed"
    ) is not False:
        raise RealExecutionRunnerError(
            "live publication unexpectedly executed"
        )

    if result.get(
        "mandatory_stop"
    ) is not True:
        raise RealExecutionRunnerError(
            "mandatory STOP missing"
        )

    zero = result.get(
        "zero_mutation_proof"
    )
    if (
        not isinstance(zero, dict)
        or zero.get("unchanged") is not True
        or zero.get("status")
        != "PASS_REAL_VAULT_ZERO_MUTATION"
    ):
        raise RealExecutionRunnerError(
            "real Vault zero-mutation proof missing"
        )


def _post_success_cleanup_block_details(
    exc: PersistentHandoffPostSuccessCleanupBlockedError,
    expected_monitored_head: str,
) -> dict[str, object]:
    temp_root = getattr(
        exc,
        "p5d3f_temp_root",
        None,
    )
    success_result = getattr(
        exc,
        "p5d3f_success_result",
        None,
    )

    if (
        not isinstance(temp_root, str)
        or not temp_root
    ):
        raise RealExecutionRunnerError(
            "post-success cleanup block missing temp root"
        )

    if not isinstance(
        success_result,
        dict,
    ):
        raise RealExecutionRunnerError(
            "post-success cleanup block missing success result"
        )

    _validate_final_success_result(
        success_result,
        expected_monitored_head,
    )

    return {
        "temp_root": temp_root,
        "success_result": success_result,
    }


def _snapshot_staging_residual(
    staging: Path,
) -> dict[str, object]:
    snapshot: dict[str, object] = {
        "path": str(staging),
        "exists": False,
        "state": "ABSENT",
        "entries": [],
    }

    try:
        if not staging.exists():
            return snapshot

        snapshot["exists"] = True

        if not staging.is_dir():
            snapshot["state"] = (
                "PRESENT_NON_DIRECTORY"
            )
            return snapshot

        rows: list[dict[str, object]] = []
        for path in sorted(
            staging.rglob("*"),
            key=lambda p: p.relative_to(
                staging
            ).as_posix(),
        ):
            relative = path.relative_to(
                staging
            ).as_posix()

            try:
                if path.is_dir():
                    rows.append(
                        {
                            "path": relative,
                            "type": "DIRECTORY",
                        }
                    )
                elif path.is_file():
                    info = path.stat()
                    rows.append(
                        {
                            "path": relative,
                            "type": "FILE",
                            "size": int(
                                info.st_size
                            ),
                        }
                    )
                else:
                    rows.append(
                        {
                            "path": relative,
                            "type": "OTHER",
                        }
                    )
            except OSError as exc:
                rows.append(
                    {
                        "path": relative,
                        "type": "UNREADABLE",
                        "error_type":
                            type(exc).__name__,
                        "error": str(exc),
                    }
                )

        snapshot["entries"] = rows
        snapshot["state"] = (
            "PRESENT_EMPTY"
            if not rows
            else "PRESENT_NONEMPTY"
        )
        return snapshot

    except Exception as exc:
        snapshot["state"] = (
            "SNAPSHOT_UNAVAILABLE"
        )
        snapshot["snapshot_error_type"] = (
            type(exc).__name__
        )
        snapshot["snapshot_error"] = str(exc)
        return snapshot

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--expected-runner-head",
        required=True,
    )
    parser.add_argument(
        "--expected-runner-blob",
        required=True,
    )
    parser.add_argument(
        "--expected-monitored-head",
        required=True,
    )
    parser.add_argument(
        "--authorization",
        required=True,
    )
    args = parser.parse_args()

    if OID40.fullmatch(
        args.expected_runner_head
    ) is None:
        raise RealExecutionRunnerError(
            "invalid --expected-runner-head"
        )

    if OID40.fullmatch(
        args.expected_runner_blob
    ) is None:
        raise RealExecutionRunnerError(
            "invalid --expected-runner-blob"
        )

    if OID40.fullmatch(
        args.expected_monitored_head
    ) is None:
        raise RealExecutionRunnerError(
            "invalid --expected-monitored-head"
        )

    if args.authorization != (
        AUTHORIZATION_LITERAL
    ):
        raise RealExecutionRunnerError(
            "explicit one-shot human authorization literal missing"
        )

    repo = _repo_root()

    print(
        "=== P5-D3F PERSISTENT PRODUCTION HANDOFF "
        "REAL EXECUTION ==="
    )
    print(
        "AUTHORITY=ONE_FINITE_READY_UNAUTHORIZED_HANDOFF_ONLY"
    )
    print(
        "REAL_VAULT_WRITE_AUTHORIZED=FALSE"
    )
    print(
        "LIVE_PUBLICATION_AUTHORIZED=FALSE"
    )
    print(
        "STAGE_A_AUTHORIZED=FALSE"
    )
    print(
        "STAGE_B_AUTHORIZED=FALSE"
    )

    _verify_exact_runtime(
        repo,
        args.expected_runner_head,
        args.expected_runner_blob,
    )
    print(
        "P5D3F_PERSISTENT_REAL_EXECUTION_RUNTIME_IDENTITY=PASS"
    )

    _verify_expected_monitored_head(
        repo,
        args.expected_monitored_head,
    )
    print(
        "P5D3F_EXPECTED_MONITORED_HEAD="
        + args.expected_monitored_head
    )
    print(
        "P5D3F_MONITORED_HEAD_AUTHORITY=PASS"
    )

    staging, vault = (
        validate_persistent_paths()
    )

    if staging != PERSISTENT_STAGING.resolve(
        strict=False
    ):
        raise RealExecutionRunnerError(
            "persistent staging identity mismatch"
        )

    if vault != REAL_VAULT.resolve(
        strict=True
    ):
        raise RealExecutionRunnerError(
            "real Vault identity mismatch"
        )

    prestate = validate_staging_prestate(
        staging
    )
    print(
        "P5D3F_PERSISTENT_STAGING_PRESTATE="
        + prestate
    )
    _require_authorized_prestate(
        prestate
    )
    print(
        "P5D3F_RECOVERY_PRESTATE_AUTHORIZED=PASS"
    )

    try:
        result = execute_persistent_production_handoff(
            control_repo=repo,
        )
    except PersistentHandoffPostSuccessCleanupBlockedError as cleanup_exc:
        details = (
            _post_success_cleanup_block_details(
                cleanup_exc,
                args.expected_monitored_head,
            )
        )
        residual = _snapshot_staging_residual(
            staging
        )
        print(
            "P5D3F_POST_SUCCESS_CLEANUP_BLOCKED=TRUE",
            file=sys.stderr,
        )
        print(
            "P5D3F_POST_SUCCESS_TEMP_ROOT="
            + str(details["temp_root"]),
            file=sys.stderr,
        )
        print(
            "P5D3F_POST_SUCCESS_RESULT_JSON="
            + json.dumps(
                details["success_result"],
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ),
            file=sys.stderr,
        )
        print(
            "P5D3F_PERSISTENT_FAILURE_RESIDUAL_JSON="
            + json.dumps(
                residual,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ),
            file=sys.stderr,
        )
        raise
    except Exception as original_exc:
        residual = _snapshot_staging_residual(
            staging
        )
        print(
            "P5D3F_PERSISTENT_FAILURE_ORIGINAL="
            + type(original_exc).__name__
            + ": "
            + str(original_exc),
            file=sys.stderr,
        )
        temp_root = getattr(
            original_exc,
            "p5d3f_temp_root",
            None,
        )
        if isinstance(
            temp_root,
            str,
        ) and temp_root:
            print(
                "P5D3F_PERSISTENT_FAILURE_TEMP_ROOT="
                + temp_root,
                file=sys.stderr,
            )
        print(
            "P5D3F_PERSISTENT_FAILURE_RESIDUAL_JSON="
            + json.dumps(
                residual,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ),
            file=sys.stderr,
        )
        raise

    _validate_final_success_result(
        result,
        args.expected_monitored_head,
    )

    print(
        "P5D3F_PERSISTENT_HANDOFF_REAL_EXECUTION=PASS"
    )
    print(
        "REAL_VAULT_ZERO_MUTATION=PASS"
    )
    print(
        "LIVE_PUBLICATION_EXECUTED=FALSE"
    )
    print(
        "MANDATORY_STOP=TRUE"
    )
    print(
        "RESULT_JSON="
        + json.dumps(
            result,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    )

    _require_clean(repo)
    print(
        "CONTROL_CLONE_CLEAN=PASS"
    )
    print(
        "P5D3F_PERSISTENT_HANDOFF_REAL_EXECUTION_COMPLETED=PASS"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        RealExecutionRunnerError,
        Exception,
    ) as exc:
        if isinstance(
            exc,
            KeyboardInterrupt,
        ):
            raise
        print(
            f"BLOCKED: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(2)

~~~~
