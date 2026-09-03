# DECISION / ADJUDICATION — V9 FOLLOW-UP / A-11

## Statut

**ADJUDICATION EXPLICITE — AVANT V10**

**Périmètre :** `1.1.2 — DATA NORMALIZATION & OBSERVATION CONTRACT`

**Base normative auditée :** V9 candidate issue de `ceac45a4d09571d894cad3741c60019962b8c73c`

**Règle :** ce document consigne les décisions nécessaires avant correction V10. Il ne modifie pas V9.

---

## 1 — TICKS ISOLÉS

**Question :** comment préserver les ticks sans relation d'ordre établie sans créer un second champ normatif ?

**Décision : ACCEPTÉE.**

`ordered_ticks` reste l'unique champ normatif portant l'ordre, mais sa représentation canonique contient dans ce même champ :

```text
ordered_ticks = {
  observations: [A, B, C],
  relations: [[B, C]]
}
```

`observations` est l'univers exact des observations de la barre ; `relations` est l'ensemble des relations établies. Un tick isolé reste donc représenté sans qu'une absence de relation soit transformée en ordre.

**Statut : [CONSÉQUENCE NÉCESSAIRE]**

---

## 2 — CANONISATION EXACTE

**Décision : ACCEPTÉE.**

Règles :

1. `observations` contient exactement une fois chaque identité normative de la barre ;
2. les identités sont sérialisées selon l'ordre canonique défini par leur identité stable ;
3. `relations` contient exactement une fois chaque relation établie ;
4. `[A,B]` signifie strictement `A précède B` ;
5. `A` et `B` appartiennent à `observations` et sont distincts ;
6. `[A,B]` et `[B,A]` ne peuvent coexister ;
7. `relations` est trié de manière déterministe selon les deux identités ;
8. les conséquences transitives exigées sont présentes ;
9. aucune relation non établie n'est ajoutée ;
10. l'ordre de sérialisation n'ajoute aucune information temporelle.

**Statut : [CONSÉQUENCE NÉCESSAIRE]**

---

## 3 — CONTRAINTES STRUCTURELLES

**Décision : ACCEPTÉE.**

Une représentation est invalide en présence notamment de :

- identité hors univers de la barre ;
- identité dupliquée ;
- relation vers une identité absente ;
- `[A,A]` ;
- paire inverse simultanée ;
- relation dupliquée ;
- cycle de précédence ;
- relation vers une autre barre ;
- interprétation temporelle de l'ordre de sérialisation ;
- relation ajoutée pour fabriquer artificiellement un ordre total.

**Statut : [CONSÉQUENCE NÉCESSAIRE]**

---

## 4 — TICKS ARRIVANT TARDIVEMENT

**Résultat du corpus : NON RÉSOLU.**

Le corpus établit `event_time` comme temps canonique, l'interdiction du look-ahead et l'impossibilité de réécrire rétroactivement une observation déjà exposée. Il ne choisit pas explicitement entre rejet, différé, backfill/nouvelle version ou autre politique pour un tick reçu tardivement dont `event_time` appartient à une barre déjà clôturée.

**Décision : REPORTÉE.**

Aucune politique opérationnelle n'est inventée dans V10. L'invariant déjà applicable demeure : une arrivée tardive ne peut pas rétroactivement modifier une observation qui avait déjà été normativement exposée à un instant antérieur.

**Statut : [QUESTION NON RÉSOLUE / REPORTÉE]**

---

## 5 — TEST CAUSAL PAR EXTENSION FUTURE

**Décision : ACCEPTÉE.**

Le protocole doit explicitement comparer deux exécutions isolées :

```text
RUN-A : Data ≤ t
RUN-B : Data ≤ t + futur
```

avec :

```text
TRACE-A(≤t) = TRACE-B(≤t)
```

Aucun cache, artefact calculé ou état dérivé de l'autre exécution ne peut être partagé. La comparaison porte sur les productions normatives intermédiaires, pas uniquement sur la sortie finale.

**Statut : [CONSÉQUENCE NÉCESSAIRE]**

---

## 6 — CONSÉQUENCE POUR V10

Seules les corrections suivantes sont autorisées par cette adjudication :

1. fermer la représentation des ticks isolés dans l'unique champ `ordered_ticks` ;
2. fermer la canonisation ;
3. fermer les contraintes structurelles ;
4. intégrer le test causal par extension future ;
5. ne pas inventer de politique de tick tardif tant que cette question reste reportée.

Aucune autre modification de V9 n'est autorisée par cette adjudication.

---

## 7 — STATUT PIPELINE

```text
AUDIT CORPUS       = EXÉCUTÉ
ADJUDICATION       = EXÉCUTÉE
QUESTIONS 1/2/3/5  = FERMÉES POUR CORRECTION
QUESTION 4         = OUVERTE / REPORTÉE
V9                 = CANDIDATE
V10                = NON CRÉÉ
```
