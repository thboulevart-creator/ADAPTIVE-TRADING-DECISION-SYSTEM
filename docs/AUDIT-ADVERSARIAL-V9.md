# AUDIT ADVERSARIAL — `1.1.2 V9`

**Statut : AUDIT — FINDINGS OUVERTS**

**Base auditée :** commit `dc6af3020403b787838285b10c4a6136f1d379a4`

**Référence V8 :** `97390d96500fc914ab346ae813c074f5428d975a`

**Principe :** audit de conformité adversarial. Le document est considéré non conforme dès lors que deux implémentations peuvent produire des résultats normatifs différents tout en respectant littéralement le contrat.

---

# VERDICT V9

```text
BLOCKED
```

La correction A-11 est correctement intégrée dans V9 et élimine le défaut structurel A-11 identifié en V8.

Cependant, l'audit adversarial montre que la nouvelle représentation par relations n'est pas encore suffisamment fermée pour garantir une représentation normative complète et univoque.

Les blocages principaux sont :

1. `ordered_ticks` ne permet pas à lui seul de représenter l'appartenance de tous les ticks lorsque certains ticks n'ont aucune relation d'ordre établie ;
2. la règle de sérialisation dite déterministe ne définit pas une convention canonique unique ;
3. la causalité est normée mais ne dispose pas, dans V9, d'un test dédié équivalent au test d'extension par données futures ;
4. le comportement des données arrivant tardivement avec un `event_time` appartenant à une barre déjà clôturée reste insuffisamment déterminé.

---

# 1. FAILLES CRITIQUES

## V9-01

**Problème :** `ordered_ticks` ne représente pas nécessairement tous les ticks de la barre.

**Pourquoi c'est critique :**

A-11 transforme `ordered_ticks` en ensemble complet des relations d'ordre établies. Mais un tick peut être présent dans la barre sans participer à aucune relation établie.

Exemple :

```text
ticks = {A, B, C}
B < C connu
A incomparable / ordre inconnu avec B et C
```

La représentation peut alors être :

```text
ordered_ticks = [[B, C]]
```

Le tick `A` disparaît de `ordered_ticks`.

`tick_count = 3` ne permet pas de reconstruire son identité. Le noyau `BAR_CLOSED` ne contient pas d'autre champ obligatoire énumérant les observations composantes.

Le résultat est donc susceptible de perdre une information primaire pourtant présente dans la barre.

**Scénario d'échec :**

Deux implémentations conformes conservent les mêmes OHLC et `tick_count`, mais l'une conserve implicitement `A` dans un mécanisme externe et l'autre ne l'expose pas. La représentation normative observable de la barre ne permet plus de vérifier l'ensemble des observations qui la composent.

**Exigence concernée :**

Conservation des observations primaires, absence de destruction injustifiée d'information, §6.4, §7.2, principe A-11.

**Statut normatif :**

[CONSÉQUENCE NÉCESSAIRE]

A-11 impose une représentation complète des relations ; cela ne suffit pas à préserver l'ensemble des observations si les éléments isolés ne sont pas représentés ailleurs.

**Correction nécessaire :**

La représentation normative doit permettre d'identifier sans ambiguïté l'ensemble des observations appartenant à la barre, y compris celles qui ne figurent dans aucune relation d'ordre, sans créer un second champ concurrent pour l'ordre.

---

# 2. FAILLES MAJEURES

## V9-02

**Problème :** la sérialisation est déclarée déterministe mais sa forme canonique exacte n'est pas définie.

**Pourquoi c'est critique :**

V9 impose que l'ordre des paires soit déterministe selon l'identité stable, mais ne précise pas la règle exacte de tri.

Deux implémentations peuvent donc choisir, par exemple :

```text
[A,B], [A,C], [B,C]
```

ou :

```text
[B,C], [A,C], [A,B]
```

et chacune peut prétendre utiliser un ordre déterministe fondé sur les identités.

**Scénario d'échec :**

Deux implémentations produisent exactement les mêmes relations mais des sérialisations différentes. Si `ordered_ticks` entre dans une comparaison de représentation normative ou dans un hash, les résultats divergent.

**Exigence concernée :**

§2.2 déterminisme, §6.4 canonicalité, §13.3, A-09/H-04.

**Statut normatif :**

[CONSÉQUENCE NÉCESSAIRE]

Une propriété normative de sérialisation doit disposer d'une convention unique si la sérialisation elle-même est comparée.

**Correction nécessaire :**

Définir une règle canonique exacte de sérialisation des paires, notamment la comparaison des identifiants, l'ordre primaire et secondaire et la représentation des cas vides.

---

## V9-03

**Problème :** la fermeture mathématique de `ordered_ticks` n'est pas entièrement spécifiée.

**Pourquoi c'est critique :**

V9 exige les conséquences transitives, mais ne définit pas explicitement plusieurs propriétés nécessaires à une représentation canonique :

- absence de paires réflexives `[A,A]` ;
- interdiction simultanée de `[A,B]` et `[B,A]` ;
- absence de doublons ;
- validité des identifiants référencés ;
- appartenance des identifiants à la barre concernée ;
- comportement si les relations source sont contradictoires ;
- distinction entre relation d'ordre et égalité/indistinguabilité temporelle.

**Scénario d'échec :**

Deux implémentations traitent différemment une entrée contradictoire ou une paire dupliquée. Le contrat ne donne pas de règle permettant de déterminer laquelle est conforme.

**Exigence concernée :**

Déterminisme, ordre temporel, conservation de l'incertitude, conformité inter-implémentations.

**Statut normatif :**

[CONSÉQUENCE NÉCESSAIRE]

**Correction nécessaire :**

Définir le domaine valide de `ordered_ticks` et la réponse normative à une relation incohérente ou invalide. Ne pas inventer une politique métier supplémentaire : uniquement fermer la représentation déjà décidée.

---

## V9-04

**Problème :** le test de causalité par extension future n'est pas présent comme test autonome dans V9.

**Pourquoi c'est critique :**

§2.1 interdit le look-ahead, mais Test K vérifie principalement la reproductibilité entre implémentations. Tester que deux implémentations identiques donnent le même résultat ne démontre pas qu'une implémentation n'a pas utilisé une donnée future de manière déterministe.

**Scénario d'échec :**

Une implémentation pré-calcule une série avec les données futures puis expose une valeur passée. Deux implémentations utilisant le même mécanisme produisent exactement le même résultat ; Test K passe alors que la causalité est violée.

**Exigence concernée :**

§2.1 absence de look-ahead, critère de fermeture §17.7.

**Statut normatif :**

[CONSÉQUENCE NÉCESSAIRE]

**Correction nécessaire :**

Réintroduire un test causal explicite par comparaison :

```text
RUN-A = Data ≤ t
RUN-B = Data ≤ t + futur
TRACE-A(≤t) = TRACE-B(≤t)
```

avec isolation des caches et artefacts.

---

## V9-05

**Problème :** le comportement des ticks tardifs n'est pas suffisamment déterminé.

**Pourquoi c'est critique :**

Le contrat distingue `event_time` et disponibilité à `observation_time`, mais ne ferme pas explicitement le cas où une observation portant un `event_time` antérieur arrive après la clôture de la barre correspondante.

**Scénario d'échec :**

Un tick `T` avec `event_time = 10:05:30` est reçu à `10:20`, après clôture de la barre 10:05. Une implémentation refuse toute modification d'une barre close ; une autre considère le tick comme historiquement valide et reconstruit la barre. Les deux comportements peuvent être compatibles avec des formulations différentes de « normalement disponible après clôture ».

**Exigence concernée :**

Causalité, BAR_CLOSED, immutabilité, reproductibilité streaming/restart.

**Statut normatif :**

[CONSÉQUENCE NÉCESSAIRE]

**Correction nécessaire :**

Déterminer explicitement la distinction entre :

- observation historiquement admissible mais reçue tardivement ;
- correction/backfill du dataset primaire ;
- événement de streaming effectivement disponible après clôture.

Cette adjudication doit préciser si et comment une représentation déjà exposée peut être révisée, ou si le flux tardif est traité comme une nouvelle version d'artefact. Ne pas choisir implicitement pendant l'implémentation.

---

# 3. FAIBLESSES MINEURES / EXPOSITIONS

## V9-06

**Problème :** `order_status` demeure un champ scalaire de `BAR_IN_PROGRESS`, alors que `ordered_ticks` peut contenir un ordre partiel.

**Risque :** le terme `UNKNOWN` peut être interprété comme « aucun ordre n'est connu » alors que certaines relations sont connues et d'autres non.

**Statut normatif :**

[ABSENCE DE DÉFINITION SUFFISANTE]

**Correction recommandée :**

Adjudicer la sémantique exacte de `order_status` avant utilisation normative par une couche aval. Ne pas modifier le champ sans décision.

---

## V9-07

**Problème :** le cas `ordered_ticks = []` n'est pas explicitement décrit pour une barre contenant plusieurs ticks mais aucune relation d'ordre établie.

**Risque :** certaines implémentations pourraient omettre le champ, utiliser `null`, ou utiliser une structure vide différente.

**Statut normatif :**

[CONSÉQUENCE NÉCESSAIRE]

**Correction recommandée :**

Définir explicitement la représentation vide dans la règle de canonicalisation.

---

# 4. POINTS ADJUDICÉS ET FERMÉS PAR V9

## A-11

**Statut : ACCEPTÉ ET INTÉGRÉ**

La représentation générale par relations remplace la structure groupe précédente pour `ordered_ticks`.

Aucun champ normatif concurrent `order_relations` n'est créé.

## A-12

**Statut : ACCEPTÉ ANTÉRIEUREMENT**

La localisation physique de l'identité/provenance de `BAR_CLOSED` n'est pas normativement imposée ; le mécanisme applicable doit être explicitement déterminé.

V9 ne réouvre pas ce point.

## H-04 / A-08

**Statut : RESCOPÉS PAR A-11**

Leurs principes restent applicables ; leur structure `ordered` + `unordered_groups` n'est plus la forme générale de `ordered_ticks` dans `1.1.2`.

---

# 5. TESTS ADVERSARIAUX V9

Les scénarios suivants doivent être considérés comme requis avant clôture :

1. ordre total ;
2. deux chaînes indépendantes ;
3. relations croisées ;
4. transitivité ;
5. ordre partiellement connu ;
6. ordre totalement inconnu ;
7. plusieurs ticks au même timestamp ;
8. tick isolé sans relation ;
9. doublons de relations ;
10. paire réflexive ;
11. relations contradictoires ;
12. déterminisme exact de sérialisation ;
13. compatibilité H-04 sur ses principes ;
14. compatibilité A-08 sur l'incertitude ;
15. causalité par extension future ;
16. absence de cache partagé ;
17. redémarrage pendant une barre ;
18. redémarrage après clôture ;
19. tick tardif avec `event_time` historique ;
20. dataset modifié après transformation ;
21. environnement différent ;
22. ordre de lecture différent ;
23. parallélisme différent ;
24. reconstruction directe depuis les ticks uniquement.

---

# 6. CONDITIONS DE FERMETURE V9

`1.1.2 V9` ne peut pas être déclaré `CLOSED` tant que :

- V9-01 reste ouvert ;
- V9-02 reste ouvert ;
- V9-03 reste ouvert ;
- V9-04 reste ouvert ;
- V9-05 reste ouvert ;
- les tests correspondants ne sont pas exécutables et passants ;
- la décision A-11 n'est pas conservée comme décision explicite et traçable ;
- H-04/A-08 ne sont pas explicitement rescopés dans la chaîne normative.

---

# 7. CONCLUSION

V9 constitue une correction réelle et substantielle de V8 : le défaut A-11 n'est plus traité par une structure de groupes insuffisante et `ordered_ticks` devient une représentation relationnelle générale.

Mais cette correction ouvre une seconde frontière de conformité : une relation complète n'est pas automatiquement une représentation complète du contenu de la barre.

Le finding le plus important est désormais :

> **La relation d'ordre et l'ensemble des observations ne doivent pas être confondus.**

La représentation doit conserver les deux propriétés sans créer de seconde source de vérité contradictoire.

```text
VERDICT FINAL V9 : BLOCKED
```

Aucune déclaration `FROZEN` n'est autorisée sur la base de cette version.
