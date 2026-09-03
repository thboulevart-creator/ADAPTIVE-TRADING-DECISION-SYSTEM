# 1.1.2 — V13 ADVERSARIAL CONFORMANCE AUDIT

**Statut : AUDIT ADVERSARIAL — V13 CANDIDATE**

**Commit audité :** `540e96a9b1ed7769676028ed565255929e8a512e`

**Branche :** `1.1.2-v13-minimal-v12-adjudication`

**Références :** V13 candidate, V12 audit/adjudication, V11 adjudication, A-11.

---

# VERDICT V13

```text
→ BLOCKED
```

V13 ne présente pas de nouvelle violation d'architecture sur la continuité ou le périmètre, mais le contrat reste non fermable pour deux raisons :

1. l'égalité par `multiset(identity(...))` ne suffit pas, à elle seule, à démontrer l'unicité/injectivité de l'identité ; cette propriété doit être apportée par le mécanisme d'identité applicable en amont ;
2. V11-06 (`event_time` / `availability_time`) et la politique des late ticks restent explicitement reportées, et V13 reconnaît correctement que les tests dépendant de ces questions ne peuvent pas passer.

---

# 1. FAILLE CRITIQUE

## V13-01 — Le test de correspondance par multiset ne démontre pas l'unicité de l'identité

**Problème :**

V13 ajoute :

```text
multiset(identity(observations))
    = multiset(identity(primary_ticks_assigned_to_bar))
```

avec la cardinalité correspondante. Mais si deux observations primaires distinctes partagent accidentellement la même identité normative, et que la représentation reproduit cette même collision, les deux multisets et les cardinalités peuvent rester égaux.

Le test établit donc une égalité de représentation selon l'identité fournie, mais pas à lui seul l'injectivité de cette identité.

**Pourquoi c'est critique :**

Une collision d'identité peut masquer la distinction entre deux observations primaires et compromettre l'exactitude de l'univers représenté. Le texte affirme pourtant qu'une collision ne doit pas pouvoir être masquée.

**Scénario d'échec :**

Deux ticks distincts A et B reçoivent la même identité I. Le résultat contient I deux fois. Le `count` et le `multiset(identity(...))` peuvent correspondre alors que l'identité ne permet plus de distinguer A et B.

**Exigence concernée :**

§1 V13 ; D1/D2 ; V11-01 ; dépendance au mécanisme d'identité de `1.1.1`.

**Statut normatif :**

[CONSÉQUENCE NÉCESSAIRE]

**Correction nécessaire :**

Ne pas inventer une identité dans `1.1.2`. Le mécanisme d'identité applicable doit être vérifié comme garantissant une identité unique/injective pour les observations concernées, ou le contrat doit explicitement reconnaître cette propriété comme précondition de conformité. Tant que cette précondition n'est pas démontrée, le test reste BLOCKED.

---

# 2. FAILLES MAJEURES

## V13-02 — Dépendance explicite à `event_time` / `availability_time`

**Problème :**

V13 reconnaît correctement que « devient établissable » ne résout pas la distinction `event_time` / `availability_time`, mais le Test V dépend encore de cette sémantique pour déterminer à quel snapshot une relation peut apparaître.

**Statut :** [QUESTION NON RÉSOLUE]

**Conséquence :** aucun PASS/CLOSED/FROZEN ne peut être accordé à une partie de `1.1.2` dont la conformité dépend de cette distinction tant que V11-06 n'est pas adjudiqué.

Aucune décision temporelle ne doit être inventée dans V13.

---

## V13-03 — Late ticks explicitement non résolus

**Problème :**

V13 précise utilement que la continuité `BAR_IN_PROGRESS → BAR_CLOSED` ne tranche pas les late ticks. Mais cette dépendance signifie que l'invariant « BAR_CLOSED contient exactement toutes les observations attribuées à la barre » ne peut être complètement évalué sur un scénario de tick tardif tant que la politique correspondante n'est pas décidée.

**Statut :** [QUESTION NON RÉSOLUE]

**Conséquence :** le texte ne doit pas être modifié pour choisir inclusion, exclusion, réouverture ou recalcul. Le point doit rester bloqué jusqu'à adjudication dédiée.

---

# 3. POINTS PASSÉS AU CONTRÔLE

- V12-01 : la dépendance à l'identité externe est maintenant explicitement reconnue ; aucune identité locale n'est introduite.
- V12-02 : aucune politique de late ticks n'est implicitement décidée ; la clause le dit explicitement.
- V12-03 : aucune sémantique `event_time/availability_time` nouvelle n'est créée.
- V11-01 : cardinalité + correspondance individuelle sont conservées.
- V11-04 : une question non résolue nécessaire bloque le PASS/CLOSED/FROZEN.
- V11-07 : continuité de l'univers `BAR_IN_PROGRESS → BAR_CLOSED` conservée.
- A-11 : `ordered_ticks` reste le champ normatif unique et porte les relations établies sans invention.

---

# 4. CONCLUSION DE L'AUDIT

V13 est plus précis que V12 et n'introduit pas de nouvelle politique sur les sujets explicitement reportés.

Mais le contrôle adversarial révèle que l'assertion « une collision ne peut pas être masquée » est plus forte que ce que le test multiset permet réellement de démontrer.

Le prochain bloc obligatoire est :

```text
V13 AUDIT
→ ADJUDICATION V13-01 / V13-02 / V13-03
```

Aucune correction contractuelle ne doit précéder cette adjudication.
