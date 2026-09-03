# 1.1.2 — V12 ADVERSARIAL CONFORMANCE AUDIT

**Statut : AUDIT ADVERSARIAL — V12 CANDIDATE**

**Commit audité :** `d489f6eeefaf8863b9d0fef497f7235ee7537765`

**Base déclarée :** V11 candidate `2afaab076df40b0b496e288816c297f2aab8acb6`

**Références vérifiées :**

- V12 candidate
- V11 adjudication `1.1.2-ADJUDICATION-V11.md`
- A-11 decision register `DECISION-REGISTER-A11.md`
- V11 follow-up adjudication `ADJUDICATION-V11-FOLLOWUP-A11.md`

---

# VERDICT V12

```text
→ BLOCKED
```

V12 corrige bien les trois findings adjudicés V11-01, V11-04 et V11-07 sans introduire de décision explicite sur les sujets reportés. Cependant, deux conditions bloquantes demeurent pour une conformité démontrable :

1. la vérifiabilité effective de l'identité canonique utilisée par le Test R et la représentation `ordered_ticks` dépend toujours du mécanisme d'identité applicable en amont ;
2. la formulation de la continuité `BAR_IN_PROGRESS → BAR_CLOSED` reste exposée au problème des observations arrivant tardivement, alors que la politique des late ticks est explicitement reportée.

Le premier point est une **absence de preuve / dépendance bloquante déjà reconnue**, pas une nouvelle décision d'architecture. Le second est une **exposition normative réelle** créée par la formulation V12 si elle est interprétée comme réglant implicitement les late ticks.

---

# 1. FAILLES CRITIQUES

## V12-01 — Identité nécessaire au Test R toujours non démontrée

**Problème :**

V12 exige :

```text
multiset(identity(observations))
    = multiset(identity(primary_ticks_assigned_to_bar))
```

mais délègue le mécanisme d'identité à `1.1.1`. Le corpus vérifié ne fournit pas dans les artefacts actuellement contrôlés une preuve permettant de conclure que ce mécanisme fournit déjà une identité déterministe, comparable et sérialisable de manière canonique.

**Pourquoi c'est critique :**

Le Test R ne peut pas être exécuté de façon normative si l'identité utilisée pour établir la correspondance individuelle n'est pas elle-même déterministe et disponible. Une implémentation pourrait choisir un identifiant local différent tout en prétendant satisfaire le test.

**Scénario d'échec :**

Deux implémentations représentent les mêmes observations avec des identifiants runtime différents. Le contenu économique est identique mais la comparaison `multiset(identity(...))` devient dépendante de la convention locale. Le test ne permet plus de démontrer la conformité inter-implémentations.

**Exigence concernée :**

§1 V12 ; A-11 déterminisme selon l'identité stable ; V11-04/V11-09.

**Statut normatif :**

[ABSENCE DE PREUVE / QUESTION NON RÉSOLUE]

**Correction nécessaire :**

Aucune nouvelle identité ne doit être inventée dans V12. Il faut d'abord vérifier/adjudicer le mécanisme d'identité applicable en amont. Tant que cette dépendance reste insuffisamment définie pour la conformité de `1.1.2`, V12 ne peut pas être déclaré PASS/CLOSED/FROZEN sur ce point.

---

# 2. FAILLES MAJEURES

## V12-02 — La continuité `BAR_IN_PROGRESS → BAR_CLOSED` peut implicitement absorber les late ticks

**Problème :**

V12 affirme que `BAR_CLOSED` contient exactement toutes les observations primaires attribuées à la barre et qu'il s'agit de l'état final de la même barre. Or la politique des late ticks est explicitement reportée par l'adjudication V11.

La formulation ne définit pas explicitement à quel moment une observation tardive cesse d'être admissible dans l'univers de la barre close. Elle peut donc être interprétée de deux manières divergentes :

- l'univers de `BAR_CLOSED` est figé au moment de clôture ;
- une observation tardive appartenant temporellement à l'intervalle peut ultérieurement modifier l'univers final.

**Pourquoi c'est critique :**

Ces deux comportements produisent des `BAR_CLOSED` différents et peuvent modifier OHLC, `tick_count` et `ordered_ticks`. La seconde interprétation introduirait en pratique une politique de late ticks sans adjudication.

**Scénario d'échec :**

Une barre est clôturée à `t_close`. Un tick portant un timestamp appartenant à l'intervalle de la barre arrive ensuite. Une implémentation l'inclut dans `BAR_CLOSED`, une autre non. Les deux peuvent se réclamer du texte V12.

**Exigence concernée :**

§3.3 V12 ; décision explicite de report des late ticks dans l'adjudication V11.

**Statut normatif :**

[CONSÉQUENCE NÉCESSAIRE / EXPOSITION]

**Correction nécessaire :**

Ne pas inventer de politique. La formulation de V12 doit être adjudiquée afin de ne pas transformer implicitement l'expression « observations attribuées à la barre » en règle de traitement des late ticks.

---

## V12-03 — Le Test V utilise un régime temporel non entièrement fermé

**Problème :**

Le Test V exige que les nouvelles relations présentes à `t2` résultent uniquement des informations/règles disponibles conformément au « régime temporel applicable ». Or V11-06 (`event_time` versus `availability_time`) demeure explicitement `QUESTION NON RÉSOLUE`.

**Pourquoi c'est important :**

Le test peut vérifier la non-réécriture historique, mais il ne peut pas entièrement déterminer quand une relation devient légitimement établissable si la frontière temporelle normative n'est pas encore adjudicée.

**Scénario d'échec :**

Une information porte un timestamp événementiel `t1` mais n'est disponible qu'à `t2`. Deux implémentations peuvent diverger sur le snapshot auquel une relation peut apparaître sans violer explicitement la formulation actuelle.

**Exigence concernée :**

§3.2, §4 Test V ; V11-06 reporté.

**Statut normatif :**

[QUESTION NON RÉSOLUE]

**Correction nécessaire :**

Ne pas résoudre `event_time/availability_time` dans V12. La question doit rester explicitement reportée et empêcher toute prétention de fermeture qui dépend de cette sémantique.

---

# 3. FAILLES MINEURES

## V12-04 — Statut de branche incohérent

**Problème :**

Le document indique :

```text
BRANCHE : à créer depuis V11 après validation du contenu
```

alors que le commit V12 a été créé sur `main` et qu'aucune branche V12 dédiée n'est établie par les éléments vérifiés.

**Pourquoi :**

La provenance de workflow devient ambiguë, même si cela ne change pas la sémantique normative du contrat.

**Statut normatif :**

[ARCHITECTURE PROPOSÉE / GOUVERNANCE]

**Correction :**

Corriger la gouvernance Git avant gel ; ne pas réécrire rétroactivement l'historique pour prétendre qu'une branche existait.

---

# 4. POINTS CORRIGÉS ET NON RETROUVÉS COMME FAILLES

Les trois corrections adjudicées sont présentes :

- V11-01 : correspondance individuelle, cardinalité et multiset d'identités ;
- V11-04 : effet bloquant explicite d'une question non résolue lorsqu'elle est nécessaire ;
- V11-07 : continuité de l'univers d'observations entre `BAR_IN_PROGRESS` et `BAR_CLOSED`.

Aucune nouvelle exigence normative n'est introduite sur :

```text
V11-02
V11-03
V11-05
V11-08
late ticks
contradictions / cycles
```

V11-06 reste reporté et ne doit pas être résolu implicitement.

---

# 5. DÉCISION DE PIPELINE

Le résultat de cet audit est :

```text
V12
→ BLOCKED
```

Le prochain bloc obligatoire est :

```text
AUDIT V12
→ ADJUDICATION DES FINDINGS V12
```

Aucune correction du contrat ne doit être effectuée avant cette adjudication.

Les sujets suivants restent explicitement hors décision :

```text
EVENT_TIME / AVAILABILITY_TIME
LATE TICKS
CONTRADICTIONS / CYCLES
```
