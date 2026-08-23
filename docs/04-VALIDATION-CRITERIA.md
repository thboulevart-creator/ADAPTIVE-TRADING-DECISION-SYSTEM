# Critères de validation

**Version :** 0.6.2 — PROPOSITION, CANDIDATE AU GEL
**Date :** 23 août 2026
**Remplace :** v0.6.1 du 21 août 2026
**Origine :** contre-expertise externe, arbitrage technique croisé, cahier des charges de réécriture en cinq blocs
**Modification :** suspension de la condition de coûts complets c.4 du §5.3, mise en cohérence de §8.C et §9 ; aucune autre modification de fond

---

## Objet

Ce document fixe **avant toute recherche confirmatoire** ce qui constitue une preuve suffisante pour
conserver, promouvoir ou abandonner une hypothèse.

Sans critères définis à l'avance, la décision de conclure reste discrétionnaire, et le biais que le
protocole cherche à éliminer se réintroduit au moment précis où l'on tranche.

---

## Convention de statut

### Statut normatif

| Marqueur | Signification |
|---|---|
| **[NORMATIF]** | Règle méthodologique universelle ou dérivation mathématique explicite. Ne dépend d'aucune préférence. |
| **[PARAMÈTRE OPÉRATIONNEL]** | Valeur fixée dans la charte de chaque recherche confirmatoire, selon son contexte. Une recommandation peut être formulée ; **elle n'engage pas**. |
| **[RECOMMANDATION]** | Aide à la décision, non contraignante. |
| **[INTERFACE]** | Exigence dont le détail relève d'un autre document ; `04` en fixe le principe et le point de raccordement. |
| **[SUSPENDU]** | Règle inscrite mais **inactive** faute de définition opérationnelle. Ne peut fonder aucune décision. |

### Statut décisionnel des conditions de promotion

| Marqueur | Effet |
|---|---|
| **[BLOQUANTE]** | Son échec interdit la promotion. **Jamais compensable par une autre métrique.** |
| **[RENFORCEMENT]** | Son échec n'interdit pas la promotion mais **abaisse le niveau de preuve** atteint (§7). |
| **[CONTEXTUELLE]** | Élément de jugement rattaché au portefeuille ou au contexte d'exploitation. **Ne doit pas être converti artificiellement en seuil numérique.** |

> **Règle de lecture.** Un nombre apparaissant sous [NORMATIF] résulte d'un calcul reproductible dont
> les hypothèses sont énoncées. Tout autre nombre est une illustration ou une recommandation, jamais
> une valeur adoptée.

---

## Règle cardinale — liberté méthodologique encadrée

**[NORMATIF]**

> **`04` n'impose pas une méthode unique lorsque plusieurs méthodes valides sont possibles. Il
> n'autorise pas davantage l'analyste à choisir, après observation, la méthode qui favorise le
> résultat.**

Tout choix méthodologique susceptible d'influencer une conclusion confirmatoire obéit à quatre
exigences cumulatives :

```
DÉCLARÉ avant l'étape confirmatoire concernée
JUSTIFIÉ au regard des conditions d'emploi de la méthode
TRAÇABLE dans la charte et son historique
CONSÉQUENT — sa violation entraîne un effet déterminé, non une simple mention
```

**[NORMATIF]** Aucune règle du présent document ne se limite à exiger la déclaration d'un problème.
Chaque règle associe : **règle → condition → conséquence → procédure → traçabilité**.

---

## Règle cardinale — aucune métrique isolée ne déclenche une décision

**[NORMATIF]**

> **Aucun seuil portant sur une métrique unique — SQN, ratio de Sharpe, profit factor, p-value ou
> toute autre — ne peut à lui seul déclencher une promotion, une conservation ou un abandon.**

**Pourquoi :** une métrique unique est optimisable. Un système suffisamment ajusté finit toujours par
franchir un seuil isolé, sans que sa valeur économique ait changé.

Les seuils statistiques du présent document constituent des **conditions nécessaires**, jamais
suffisantes.

---

# 0. Régimes de travail et charte de recherche

## 0.1 — Deux régimes distincts

**[NORMATIF]**

| | **EXPLORATOIRE** | **CONFIRMATOIRE** |
|---|---|---|
| **Objet** | Découvrir, observer, chercher des relations, formuler des hypothèses | Tester une hypothèse préalablement définie |
| **Budget d'hypothèses** | non requis | requis (§2.A) |
| **Frontières temporelles gelées** | non requises | requises (§3.2) |
| **Gel technique** | non requis | requis (§3.4) |
| **Taille d'échantillon justifiée** | non requise | requise (§1) |
| **Contrôles de données** | **obligatoires** (document `05`) | **obligatoires** |
| **Effet sur une période** | **consultation**, d'intensité déclarée (§4.2) | **consommation** (§4.1) |
| **Conclusion de validité** | **impossible** | possible |

**[NORMATIF]** Un résultat exploratoire ne peut jamais être présenté comme une validation, ni fonder
un **engagement de capital**.

### Définition — engagement de capital

**[NORMATIF]**

> **Constitue un engagement de capital toute allocation de capital réel**, quelle que soit son
> ampleur ou sa dénomination : allocation exploratoire, pilote, déploiement partiel, allocation
> progressive.
>
> **Ne constitue pas un engagement de capital** une simulation, un backtest ou une exécution en
> démonstration sans capital réel.

**Pourquoi cette définition :** sans elle, une « allocation exploratoire de test » permettrait de
contourner l'interdiction en la qualifiant autrement.

## 0.2 — Séquence officielle

**[NORMATIF]**

```
Données → Observation → Exploration → Découverte
                                          ↓
                                  Hypothèse candidate
                                          ↓
                                  CHARTE DE RECHERCHE      ← franchissement du seuil
                                          ↓
                                Recherche confirmatoire
                                          ↓
                                 Validation ou rejet
                                          ↓
                          Niveau de preuve atteint (§7)
                                          ↓
                                    Avantage potentiel
```

Le franchissement du seuil est un **acte explicite** : la rédaction de la charte.

## 0.3 — Charte de recherche

**[NORMATIF]**

> **Toute recherche confirmatoire s'ouvre par une charte écrite, datée et horodatée. Aucun calcul
> confirmatoire ne peut débuter avant sa rédaction.**

**[NORMATIF]** La charte est **immuable**. Toute modification produit un amendement daté ; la version
antérieure est conservée. Un amendement postérieur à la lecture d'un résultat confirmatoire est
recevable mais **entraîne les conséquences du §3.2 ou du §2.A.1** selon son objet.

La charte comporte onze éléments.

| # | Élément | Contenu attendu | Renvoi |
|---|---|---|---|
| 1 | **Observation initiale** | Ce qui a été constaté en exploration, sur quelles données, **avec l'intensité de consultation de chaque période** | §4.2 |
| 2 | **Hypothèse** | Ce que l'on affirme, formulé sans ambiguïté | — |
| 3 | **Justification économique ou comportementale** | Quel acteur agit, sous quelle contrainte, pourquoi cette action laisserait une trace exploitable | §0.4 |
| 4 | **Prédiction testable** | Ce qui devrait être observé si l'hypothèse est vraie | — |
| 5 | **Domaine de généralisation attendu** | Actifs, horizons, régimes et conditions dans lesquels l'hypothèse est censée valoir | §5.3 c.8 |
| 6 | **Conditions de falsification** | Ce qui, observé, réfuterait l'hypothèse | §6.2 |
| 7 | **Conditions d'invalidation de l'essai** | Ce qui rendrait le test non interprétable sans se prononcer sur l'hypothèse | §6.2 |
| 8 | **Spécification du test** | Les huit éléments du §1.9 | §1.9 |
| 9 | **Protocole préalable** | Actif, phases et frontières (§3), `N_budget` et `N_famille` (§2), unité statistique (§1.5), méthode de dimensionnement (§1.3–1.4), taille requise (§1) | §1, §2, §3 |
| 10 | **Spécification des contrôles** | Pour chaque condition du §5 : périmètre, procédure, critère de rejet, **rôle** | §5.2 |
| 11 | **Référence du gel technique** | Identifiants de l'artefact gelé | §3.4 |

**[NORMATIF]** Les éléments 3 et 6 — justification et falsifiabilité — ne sont **pas exigés en
exploration**. Ils deviennent obligatoires au moment de la promotion en hypothèse candidate.

**[NORMATIF]** La charte doit permettre à **deux analystes indépendants de reproduire le test** sans
interprétation arbitraire.

## 0.4 — Justification économique : portée et coût assumé

**[NORMATIF]**

Une hypothèse dont la justification se réduit à « cela apparaît sur les graphiques » ou « cela a
fonctionné dans le passé » n'est pas recevable en régime confirmatoire.

**[NORMATIF] — Limitation assumée**

> **Cette règle écarte délibérément des anomalies empiriquement réelles mais encore dépourvues
> d'explication satisfaisante.** L'absence d'un mécanisme connu n'implique pas l'absence d'avantage :
> des régularités empiriques précèdent parfois leur explication.
>
> Ce coût est accepté au titre de la limitation de l'espace des hypothèses. Il ne s'agit pas d'une
> condition scientifique d'existence d'un avantage, mais d'un **filtre de gouvernance et de
> lisibilité**.

**Risque reconnu :** la règle favorise les hypothèses les mieux rationalisées, non nécessairement les
plus vraies. Elle est maintenue parce que la contrepartie — accepter toute régularité sans mécanisme —
ouvre l'espace de recherche au point de rendre la sélection incontrôlable.

---

# 1. Dimensionnement et spécification du test

## 1.1 — Obligation de justification préalable

**[NORMATIF]**

En régime confirmatoire, la taille d'échantillon nécessaire doit être établie avant le premier calcul
et sa disponibilité vérifiée.

Si elle n'est pas disponible, trois voies :

1. **rester en régime exploratoire**, en le déclarant, sans possibilité de conclure ;
2. **viser un niveau de preuve inférieur** au sens du §7, avec les conséquences correspondantes ;
3. **écarter la piste**.

## 1.2 — L'effet visé se définit ex ante

**[NORMATIF]**

> **L'effet minimal détectable est une hypothèse posée avant l'expérience confirmatoire. Il ne peut
> en aucun cas être dérivé des résultats observés.**

**Pourquoi :** dimensionner à partir d'un effet observé revient à justifier a posteriori la taille dont
on disposait — raisonnement circulaire.

**Articulation avec l'exploration :** une observation exploratoire peut suggérer un ordre de grandeur.
Elle ne constitue pas une mesure.

## 1.3 — Voie analytique

**[NORMATIF]**

### Formule analytique de dimensionnement — test primaire unilatéral

Sous les hypothèses précisées aux §§1.3–1.4, la taille d'échantillon requise pour le test primaire
unilatéral de moyenne s'écrit :

```
n = ( (z_{1-α} + z_{1-β}) / d )^2
```

où :

```
d = (μ_A − μ_0) / σ
```

avec :

| Symbole | Signification |
|---|---|
| `μ_0` | moyenne sous l'hypothèse nulle |
| `μ_A` | moyenne sous l'alternative pertinente définie ex ante |
| `σ` | écart-type supposé ou estimé ex ante pour l'unité statistique retenue |
| `α` | probabilité maximale d'erreur de type I retenue pour le test primaire, après correction applicable |
| `β` | probabilité maximale d'erreur de type II retenue |
| `1 − β` | puissance recherchée |
| `z_q` | quantile d'ordre `q` de la loi normale standard |

**La formule concerne un test unilatéral pré-spécifié.** Pour un test bilatéral de niveau `α`, le
terme critique devient `z_{1-α/2}` :

```
n = ( (z_{1-α/2} + z_{1-β}) / d )^2
```

**[NORMATIF] — Portée.** Cette formule dimensionne **uniquement le test primaire** spécifié dans la
charte conformément au §1.9. Elle ne dimensionne pas automatiquement les contrôles de robustesse, de
stabilité paramétrique, de drawdown, de coûts, de sous-périodes, de régimes, ni aucune autre condition
complémentaire de promotion.

**[NORMATIF] — Conditions d'emploi.** Son emploi reste conditionné aux hypothèses de validité du
présent document, notamment la définition préalable de l'unité statistique, l'indépendance ou le
traitement explicite de la dépendance, la pertinence de l'approximation normale de l'estimateur et une
estimation ex ante de `σ`.

**Conditions d'emploi, à examiner et déclarer dans la charte :**

| Condition | Conséquence si non satisfaite |
|---|---|
| Observations indépendantes ou dépendance traitée (§1.5) | Taille effective inférieure au décompte ; formule optimiste |
| Variance stable sur la période | Puissance réelle inférieure |
| Distribution de l'estimateur suffisamment proche de la normale | Seuils de test non calibrés |
| Direction pré-enregistrée si test unilatéral | Voir ci-dessous |

**[NORMATIF] — Test unilatéral.** Un test unilatéral n'est admissible que si la **direction de
l'hypothèse est pré-enregistrée** à l'élément 8 de la charte. Une direction retenue après observation
n'ouvre pas rétroactivement droit au caractère unilatéral : le test devient bilatéral.

**[NORMATIF] — Conséquence.** Lorsqu'une condition d'emploi n'est pas défendable, la voie analytique
est écartée et **la voie alternative du §1.4 s'applique obligatoirement**. L'absence de voie n'est pas
recevable.

> La proximité à la normalité ne se présume pas par invocation générale d'un théorème asymptotique.
> Elle s'apprécie au regard de la distribution attendue de l'estimateur, de la taille disponible et de
> la structure de dépendance.

## 1.4 — Voie alternative

**[NORMATIF]**

Lorsque les conditions du §1.3 ne sont pas défendables, le dimensionnement s'effectue par une méthode
alternative **déclarée dans la charte avant tout calcul confirmatoire**.

Méthodes admissibles selon le contexte :

```
simulation
rééchantillonnage
bootstrap adapté à la structure de dépendance
borne conservatrice
scénarios conservateurs
toute autre méthode explicitement justifiée
```

**[NORMATIF]** Aucune méthode alternative n'est déclarée universellement supérieure. La méthode
retenue doit **reproduire autant que possible la structure de dépendance pertinente** du problème
étudié, et cette adéquation doit être justifiée dans la charte.

**[NORMATIF]** Le choix entre voie analytique et voie alternative est **déclaré avant l'inférence
confirmatoire**. Un changement de voie postérieur à la lecture d'un résultat constitue un amendement
au sens du §0.3 et entre dans `N_budget`.

## 1.5 — Unité statistique et dépendance

**[NORMATIF]**

Le document n'impose aucune unité statistique universelle. La charte déclare, à son élément 9 :

**a) Unité primaire d'observation** — transaction, grappe d'événements, jour, semaine, fenêtre non
chevauchante, portefeuille, ou autre unité justifiée.

**b) Contrôle explicite de dépendance** — examen des mécanismes de dépendance susceptibles d'affecter
l'unité retenue.

**c) Méthode retenue lorsque l'unité primaire ne satisfait pas les hypothèses de son modèle
statistique** — renvoi au §1.4.

### Interdiction de l'équivalence implicite

**[NORMATIF]**

> **Le nombre de transactions ne vaut pas nombre d'observations indépendantes. Cette équivalence ne
> peut jamais être supposée.**

**Mécanismes de dépendance à examiner :**

| Mécanisme | Effet |
|---|---|
| Positions se chevauchant dans le temps | Résultats partageant le même mouvement |
| Transactions déclenchées par un même événement | Tirages non distincts |
| Autocorrélation résiduelle entre unités non chevauchantes | Information inférieure au décompte |
| Dépendance de régime, grappes de volatilité | Variance non stationnaire |
| Corrélation entre positions sur actifs distincts | Redondance inter-actifs |

### Regroupement — heuristique conservatrice

**[NORMATIF]**

> **Le regroupement d'observations dépendantes est une heuristique conservatrice de gestion de la
> dépendance. Il ne constitue pas un estimateur calibré de taille effective.**

Lorsque le regroupement est employé, sa règle est **définie mécaniquement dans la charte avant tout
calcul** et comporte :

```
unité de regroupement
critère de rattachement — mécanique, non interprétatif
mode d'agrégation du résultat du groupe
```

**[NORMATIF]** La règle de regroupement n'est **pas ajustable après observation**. Un ajustement
postérieur constitue un amendement au sens du §0.3, entre dans `N_budget`, et rend l'inférence
antérieure caduque.

**[NORMATIF] — Conséquence.** Lorsque l'inférence formelle exige une estimation de taille effective
plus élaborée que ce que le regroupement peut fournir, la voie alternative du §1.4 s'applique.

## 1.6 — Estimation ex ante de la dispersion

**[NORMATIF]**

Calculer `d` ex ante suppose d'estimer la dispersion par unité d'observation sans recourir aux
résultats de l'expérience confirmatoire. Cette estimation est documentée dans la charte et sa source
déclarée.

Sources admissibles :

| # | Source | Remarque |
|---|---|---|
| 1 | Dérivation analytique du profil de sortie | Voir restriction ci-dessous |
| 2 | Mesure sur un actif ou une période distincts de ceux de l'expérience | Sous réserve du §4.4 |
| 3 | Référence externe portant sur une famille comparable | — |
| 4 | **Borne conservatrice par simulation ou scénarios** | Déclarée comme telle |

**Source inadmissible :** la dispersion mesurée sur les données mêmes de l'expérience confirmatoire.

### Restriction sur la dérivation analytique

**[NORMATIF]**

> Une stratégie à cible et stop fixes produit une distribution à deux points **avant coûts et sous
> hypothèse d'exécution idéale** — absence de glissement variable, de gap, d'exécution partielle et de
> coût dépendant du marché.
>
> **Cette dérivation fournit un ordre de grandeur pour le dimensionnement, non une distribution nette
> des résultats réels.**

**[NORMATIF]** Une stratégie à sortie variable ne permet pas cette dérivation. La source 4 est alors
la voie normale, et non un pis-aller. **L'absence de dérivation analytique ne constitue pas un motif
d'exclusion d'une hypothèse.**

## 1.7 — Effet économiquement pertinent

**[PARAMÈTRE OPÉRATIONNEL]**

Méthode de détermination proposée, partant de l'économie :

```
1. Rendement annuel net minimal jugé digne d'être exploité
2. Fréquence attendue d'unités d'observation
3. Espérance par unité requise, coûts déduits
4. Dispersion estimée selon le §1.6
5. d = espérance requise / dispersion estimée
6. n calculé par le §1.3 ou §1.4, dépendance traitée selon le §1.5
```

**[RECOMMANDATION]** Relier l'exigence à une fonction économique explicite — coûts, capacité, capital
mobilisé, risque, fréquence, coût d'opportunité — plutôt qu'à un seul objectif de rendement.

## 1.8 — Seuil de significativité et puissance

**[PARAMÈTRE OPÉRATIONNEL]**

| Erreur | Conséquence dans ce projet |
|---|---|
| Faux positif — trader une stratégie sans avantage | Perte de capital, perte de confiance dans le protocole |
| Faux négatif — écarter une stratégie qui en avait un | Coût d'opportunité, aucun risque financier |

**[RECOMMANDATION]** L'asymétrie est nette. Un α plus strict que 0,05 serait cohérent, au prix d'un
échantillon plus grand.

## 1.9 — Spécification du test

**[NORMATIF]**

La charte spécifie, à son élément 8, les huit éléments suivants. **En leur absence, la condition de
significativité du §5.3 n'est pas déterminée et ne peut être évaluée.**

| # | Élément |
|---|---|
| 1 | Variable primaire d'intérêt |
| 2 | Unité d'observation (§1.5) |
| 3 | Hypothèse nulle H₀ |
| 4 | Statistique de test |
| 5 | Estimateur de variance ou méthode équivalente |
| 6 | Traitement de la dépendance et de l'autocorrélation |
| 7 | Caractère unilatéral ou bilatéral, et direction pré-enregistrée le cas échéant |
| 8 | Référentiel de comparaison |

---

# 2. Budget d'hypothèses et multiplicité

**Portée : régime confirmatoire.** L'exploration n'est pas soumise au budget, puisqu'elle ne conclut
pas.

## 2.A — `N_budget` — décompte de gouvernance

### 2.A.1 — Nature et déclaration

**[NORMATIF]**

> **`N_budget` recense l'ensemble des choix et explorations susceptibles d'avoir influencé le résultat
> final.** Il est déclaré dans la charte avant le premier calcul confirmatoire.

**[NORMATIF]** **`N_budget` ne doit jamais être employé directement comme multiplicateur dans une
correction statistique.** Il relève de la gouvernance de la recherche, non de l'inférence.

Toute exploration supplémentaire non prévue exige un amendement daté de la charte.

### 2.A.2 — Périmètre

**[NORMATIF]**

Comptent dans `N_budget` :
- toute combinaison de paramètres évaluée ;
- tout filtre testé ;
- toute variante de règle d'entrée ou de sortie ;
- tout actif supplémentaire testé avec la même hypothèse ;
- toute période supplémentaire testée après un premier résultat ;
- toute redéfinition d'une taxonomie consécutive à un résultat ;
- tout changement de méthode de dimensionnement ou de règle de regroupement postérieur à un résultat.

Ne comptent pas :
- les calculs effectués en régime exploratoire, antérieurement à la charte ;
- les contrôles de voisinage qualifiés de **diagnostiques pré-spécifiés** au sens du §5.5.

### 2.A.3 — Taille du budget

**[PARAMÈTRE OPÉRATIONNEL]**

**[RECOMMANDATION]** Un budget restreint facilite l'interprétation. Un budget large demeure légitime
pour une recherche de découverte ou une comparaison systématique, **à condition que la famille de
tests soit correctement définie et l'inférence adaptée**.

## 2.B — `N_famille` — famille de tests corrigée

### 2.B.1 — Définition

**[NORMATIF]**

> **`N_famille` est le nombre de tests décisionnels comparables portant sur une même hypothèse, dont
> chacun pourrait conduire à une promotion.** C'est le seul décompte entrant dans une correction de
> multiplicité.

`N_famille` est déclaré dans la charte, élément 9, avant le premier calcul confirmatoire.

**[NORMATIF] — Règle de rattachement.** Un contrôle entre dans `N_famille` **si et seulement si son
issue peut conduire au changement de la configuration promue**. Le rôle de chaque contrôle est déclaré
à l'élément 10 de la charte selon la typologie du §5.2.

### 2.B.2 — Correction de multiplicité

**[NORMATIF]**

Une correction est requise dès que `N_famille > 1`. Le principe est normatif ; la méthode est un
paramètre opérationnel déclaré dans la charte.

**Bonferroni.**

> **Bonferroni contrôle le taux d'erreur familial sous dépendance arbitraire**, par l'inégalité de
> Boole. **Elle ne suppose pas l'indépendance des tests.**
>
> La dépendance entre tests la rend **conservatrice** — perte de puissance — sans affecter sa
> validité.
>
> **Sa limite réelle :** elle ne corrige que la **famille de tests déclarée**. Elle ne contrôle ni une
> recherche non enregistrée, ni une sélection extérieure à cette famille.

**Benjamini-Hochberg.** Contrôle la proportion de fausses découvertes parmi les hypothèses retenues.
Plus permissive. Sa validité standard suppose l'indépendance ou certaines formes de dépendance
positive — condition à examiner avant emploi.

**Šidák.** La formule `1 − (1 − α)^N` suppose l'indépendance des tests. Elle ne doit pas être confondue
avec Bonferroni.

**[NORMATIF]** Aucune correction de multiplicité ne traite le data snooping dans son ensemble. Elle
traite la multiplicité **à l'intérieur d'une famille déclarée**. Les idées abandonnées, les décisions
informelles et les sélections antérieures à la charte relèvent de `N_budget` et de la gouvernance, non
de la correction statistique.

## 2.C — Contrôles avancés

**[RECOMMANDATION — non implémentée]**

Trois familles à examiner lorsque le volume de recherche le justifiera : **Deflated Sharpe Ratio**,
**White Reality Check**, **Hansen SPA**. Elles ne font partie d'aucune règle en vigueur.

---

# 3. Phases, frontières et gel

## 3.1 — Architecture des phases

**[NORMATIF]**

Quatre phases sont distinguées. Leur articulation est déclarée dans la charte, élément 9.

| | **A — Exploration / conception** | **B — Validation confirmatoire** | **C — Hors échantillon** | **D — Confirmation prospective** |
|---|---|---|---|---|
| **Objectif** | Formuler l'hypothèse, calibrer la configuration | Mesurer la performance de la configuration gelée | Vérifier sur données non employées à la calibration ni à la validation | Vérifier sur données postérieures à la charte |
| **Informations accessibles** | libres | résultats du test spécifié | résultats du test spécifié | résultats en temps réel |
| **Modifications autorisées** | libres avant la charte ; après la charte, uniquement par amendement compté | **aucune** sur la configuration | **aucune** | **aucune** |
| **Statut probatoire** | nul | dépend du §4.3 | dépend du §4.3 | le plus élevé |
| **Rôle dans la promotion** | aucun | condition bloquante §5.3 c.2 | renforcement ou bloquant selon niveau visé (§7) | requis pour les niveaux supérieurs (§7) |

**[NORMATIF] — Gel de la configuration.** Une configuration destinée à une validation confirmatoire
est **gelée avant l'ouverture de la phase B**. Aucun paramètre ne peut être sélectionné sur la phase A
après le début de la phase B.

**[NORMATIF] — Statut du hors échantillon.** La phase C **n'est pas automatiquement une période
vierge**. Son statut probatoire est déterminé par le §4.3, en fonction de son historique de
consultation et de consommation.

**[NORMATIF]** La charte déclare si la promotion s'appuie sur B seule, sur B et C, ou sur B, C et D.
Ce choix détermine le niveau de preuve atteignable (§7).

## 3.2 — Gel des frontières temporelles

**[NORMATIF]**

> Les frontières séparant les phases A, B, C et D sont gelées, datées et inscrites dans la charte
> **avant le premier calcul confirmatoire utilisant ces données**.

**[NORMATIF] — Modification.** Toute modification exige un amendement daté et une justification
reposant sur une propriété **des données ou du marché**, jamais sur un résultat.

**Recevable :** rupture documentée de couverture d'une source, changement structurel d'instrument,
indisponibilité de données.

**Non recevable :** élargir une période parce qu'elle contient trop peu d'observations, **après avoir
constaté ce nombre**.

**[NORMATIF] — Conséquence.** Une modification non recevable entre dans `N_budget`, et la période
concernée voit son statut probatoire dégradé selon le §4.3.

## 3.3 — Longueur relative des périodes

**[PARAMÈTRE OPÉRATIONNEL]**

**[RECOMMANDATION]** Dimensionner la phase B pour qu'elle contienne au moins la taille effective
requise au §1, au rythme attendu, puis répartir le reste.

## 3.4 — Gel technique

**[NORMATIF] [INTERFACE]**

> **La configuration confirmatoire doit être techniquement reproductible et gelée avant l'ouverture
> de la phase B.**

`04` fixe le principe et l'interface. **Le détail de la procédure relève du document `05` ou d'un
document technique dédié.**

Périmètre minimal du gel, dont les identifiants figurent à l'élément 11 de la charte :

```
code du moteur de recherche et d'exécution simulée
dépendances et versions
environnement d'exécution
jeu de données et sa version
modèle de coûts et sa version
paramètres de la configuration
artefacts nécessaires à la reproduction
```

**[NORMATIF] — Conséquence.** Toute modification post-gel susceptible d'affecter le résultat est
traçable et **peut exiger une nouvelle validation**. La charte, ou le document technique de raccord,
distingue au minimum :

| Nature de la modification | Effet sur la validation |
|---|---|
| Modification d'hypothèse | Nouvelle charte |
| Modification de configuration | Nouvelle validation |
| Correction d'un défaut de code | Voir §6.2 — invalidation de l'essai |
| Modification du moteur ou des données | Nouvelle validation |
| Modification du modèle de coûts | Nouvelle validation ; comparaisons antérieures caduques |

---

# 4. Information, consultation et consommation

## 4.1 — Trois états d'une période

**[NORMATIF]**

| État | Définition |
|---|---|
| **VIERGE** | Jamais observée pour cet actif ni pour un actif corrélé au sens du §4.4 |
| **CONSULTÉE** | Observée en régime exploratoire, sans conclusion de validité, à une intensité déclarée (§4.2) |
| **CONSOMMÉE** | A servi de juge dans une recherche confirmatoire |

**[NORMATIF]** L'exploration **consulte** une période, elle ne la consomme pas. Une période consommée
ne peut plus servir de juge pour une hypothèse de la même famille au sens du §4.5.

## 4.2 — Intensité de consultation

**[NORMATIF]**

Trois intensités au minimum, déclarées à l'élément 1 de la charte pour chaque période employée comme
juge.

| Intensité | Description | Exemples |
|---|---|---|
| **I1 — Consultation procéduralement non décisionnelle** | Consultation limitée à des informations agrégées et non décisionnelles, **cette limitation étant démontrable par les traces** (§4.2 bis) | Existence de la série, couverture temporelle, continuité, métadonnées, format, granularité, fuseau horaire, taux de données manquantes, nombre brut d'observations non conditionné à une règle candidate |
| **I2 — Inspection analytique** | Observation détaillée du comportement, sans test de la configuration ni sélection | Analyse de distribution, examen de sous-périodes, visualisation détaillée |
| **I3 — Consultation active** | Test de la configuration, optimisation, ou sélection effectuée sur la période | Backtest de la stratégie, balayage de paramètres, choix d'une variante |

**[NORMATIF]** La classification est **traçable** et figure au registre du §4.6. En cas de doute sur le
classement, **l'intensité la plus élevée est retenue**.

**[NORMATIF]** Aucune opération unique ne détermine à elle seule la contamination. Le classement
s'apprécie au regard de la question : **cette observation a-t-elle pu influencer la configuration
finalement testée ?**

### 4.2 bis — Conditions d'attribution du statut I1

**[NORMATIF]**

> **Une période ne peut être classée I1 que si la consultation a été limitée à des informations
> agrégées et non décisionnelles, et si cette limitation est démontrable par les traces disponibles.**

**Informations pouvant relever de I1** — descriptives, nécessaires à l'identification ou à la gestion
des données :

```
existence de la série
couverture temporelle
continuité
métadonnées
format
granularité
fuseau horaire
taux de données manquantes
nombre brut d'observations ou de transactions non conditionné à une règle candidate
```

**Informations ne pouvant pas relever de I1** — susceptibles d'influencer une décision confirmatoire,
notamment toute information relative à :

```
la performance, l'espérance, la distribution de résultats, la direction d'un effet
le choix d'une hypothèse, d'un actif, d'une période, d'un domaine, d'un paramètre,
   d'une métrique, d'un seuil, d'une frontière temporelle, d'un test,
   d'un critère de promotion ou d'abandon
la décision de lancer, poursuivre, interrompre ou promouvoir une recherche
```

**[NORMATIF] — Enregistrement.** Toute consultation classée I1 est enregistrée au registre du §4.6
avec, au minimum :

```
date · opérateur · source · période concernée
informations accessibles · finalité déclarée
preuve ou référence permettant de vérifier le périmètre réellement consulté
```

**[NORMATIF] — Antériorité.** Lorsque la consultation précède une charte ou un jalon décisionnel, sa
trace doit permettre de vérifier qu'elle était antérieure à ce jalon **et** que les informations
décisionnelles protégées n'étaient pas accessibles dans le périmètre consulté.

**[NORMATIF] — Vérifiabilité.** Le statut I1 **ne repose pas sur une déclaration rétrospective
d'absence d'influence**. Il est attribué seulement lorsque les traces permettent à un auditeur
indépendant de vérifier le périmètre d'information accessible et l'absence d'accès aux informations
décisionnelles définies ci-dessus.

**[NORMATIF] — Conséquence.** Si une information susceptible d'influencer une décision confirmatoire a
été accessible, **ou si l'absence de cet accès ne peut pas être établie à partir des traces
disponibles**, la période ne reçoit pas le statut I1 et son statut probatoire est dégradé selon les
règles applicables du §4.3.

## 4.3 — Statut probatoire d'une période

**[NORMATIF]**

Le statut probatoire d'une période employée comme juge découle de son état et de l'intensité maximale
de consultation qu'elle a subie.

| État et intensité | Statut probatoire | Conséquence décisionnelle |
|---|---|---|
| VIERGE | **Plein** | Aucune restriction |
| CONSULTÉE — I1 | **Plein** | Intensité déclarée au registre |
| CONSULTÉE — I2 | **Réduit** | Le niveau de preuve atteignable est plafonné (§7). Une confirmation prospective ou une réplication sur période distincte est requise pour atteindre un niveau supérieur |
| CONSULTÉE — I3 | **Faible** | Ne peut fonder qu'une prévalidation. **Ne peut pas fonder à elle seule une promotion.** Confirmation prospective requise |
| CONSOMMÉE, même famille | **Nul** | Ne peut pas servir de juge |
| CONSOMMÉE, famille distincte | **Réduit** | Traité comme CONSULTÉE — I2 |

**[NORMATIF]** Ce tableau est la conséquence décisionnelle exigée par la règle cardinale : la
déclaration d'une consultation ne se limite jamais à une mention, elle détermine un statut.

### Condition d'attribution du statut plein

**[NORMATIF]**

> Le statut probatoire **plein** n'est attribuable à une période classée I1 que si les exigences
> procédurales de traçabilité, de périmètre informationnel et de vérifiabilité définies au §4.2 bis
> sont satisfaites.
>
> **En cas de doute non résoluble sur l'accès à une information décisionnelle, le statut plein n'est
> pas accordé.**

**[NORMATIF]** Cette règle qualifie le **statut de la preuve**. Elle ne transforme pas rétroactivement
la période en période vierge.

## 4.4 — Actifs corrélés

**[NORMATIF]**

> **La consultation d'une période sur un actif n'est ni automatiquement indépendante des actifs
> corrélés, ni automatiquement contaminante pour tous.**

L'évaluation porte sur quatre éléments, déclarés dans la charte lorsqu'un actif corrélé est employé
comme juge sur les mêmes dates :

```
corrélation pertinente sur la période et l'horizon considérés
mécanisme commun invoqué par l'hypothèse
information effectivement observée sur l'actif consulté
degré d'utilisation de cette information dans la configuration
```

**[NORMATIF] — Conséquence.** Lorsque le doute est significatif au point de pouvoir modifier la
conclusion, deux voies seulement :

1. appliquer le **traitement le plus conservateur admissible** — retenir l'intensité de consultation
   de l'actif corrélé pour la période concernée ;
2. déclencher la **revue indépendante** du §4.5.

## 4.5 — Famille de recherche

**[NORMATIF]**

La consommation d'une période s'applique à l'intérieur d'une même **famille de recherche**.

### Critère principal — transmission d'information

> Deux hypothèses appartiennent à la même famille si la seconde a été formulée, sélectionnée ou
> paramétrée **en connaissance du résultat** de la première.

### Critères structurels

**[NORMATIF]** Deux hypothèses appartiennent à la même famille dès qu'**au moins une** des conditions
suivantes est réunie :

```
même mécanisme économique ou comportemental déclaré
même signal d'entrée
même anomalie de marché sous-jacente
```

**Pourquoi une disjonction et non une conjonction :** exiger la réunion simultanée permettrait
d'échapper à une famille en modifiant un seul élément — une reformulation narrative ou une
transformation superficielle du signal suffirait à créer artificiellement une famille nouvelle.

### Procédure de vérification

**[NORMATIF]**

```
1. Auto-déclaration de l'appartenance dans la charte
2. Application des critères structurels
3. Revue indépendante en cas de doute sérieux ou de contestation
```

**[NORMATIF]** Lorsqu'un doute sérieux existe sur une classification **susceptible de modifier
`N_famille` ou le statut probatoire d'une période**, la classification ne peut être tranchée
unilatéralement par l'auteur de la recherche.

**[INTERFACE]** Les modalités de la revue indépendante — qui la conduit, sous quel délai, selon quelle
forme — relèvent du protocole de gouvernance du projet et ne sont pas fixées ici.

**Risque de circularité reconnu.** La famille dépend en partie de la justification déclarée à
l'élément 3. Une justification peut être reformulée pour échapper à une famille consommée. Les
critères structurels disjonctifs et la revue indépendante constituent les garde-fous ; **ils ne
suppriment pas le risque, ils le rendent contestable**.

## 4.6 — Registre

**[NORMATIF]**

Chaque actif porte un registre traçant :

```
Actif                    : ...
Période                  : du ... au ...
État                     : VIERGE | CONSULTÉE | CONSOMMÉE
Intensité maximale       : I1 | I2 | I3
Statut probatoire courant: plein | réduit | faible | nul
Consultations exploratoires :
    date | nature | intensité | opérateur
Lectures confirmatoires :
    date | charte de référence | famille | résultat | opérateur
Actifs corrélés déclarés : ...
Périodes disponibles     : ...
```

**[NORMATIF]** Le registre couvre **toute observation des données**, y compris scripts, carnets,
exports, visualisations et analyses manuelles — non les seuls tests formellement qualifiés de
confirmatoires.

## 4.7 — Épuisement et hiérarchie de preuve

**[NORMATIF]**

Lorsqu'aucune période de statut probatoire plein ne subsiste pour une famille donnée, la piste n'est
pas automatiquement close. Quatre voies :

| Voie | Conséquence |
|---|---|
| Accumuler des données futures — confirmation prospective | Niveau de preuve le plus élevé accessible |
| Réplication sur un actif au domaine de généralisation déclaré | Niveau de preuve intermédiaire |
| Promotion à un niveau de preuve inférieur (§7) | Conséquences de promotion restreintes |
| Abandon | — |

**[NORMATIF]** Un redécoupage d'une période déjà consommée ne reconstitue pas un juge indépendant et
ne change pas son statut probatoire.

---

# 5. Promotion

**Portée : résultats confirmatoires uniquement.**

## 5.1 — Structure de la décision

**[NORMATIF]**

Les conditions de promotion se répartissent en trois catégories.

| Catégorie | Effet de l'échec |
|---|---|
| **[BLOQUANTE]** | Interdit la promotion. **Jamais compensable.** |
| **[RENFORCEMENT]** | N'interdit pas la promotion, **abaisse le niveau de preuve atteint** (§7) |
| **[CONTEXTUELLE]** | Élément de jugement rattaché au portefeuille ou au contexte. **Ne se convertit pas en seuil numérique.** |

**[NORMATIF] — Non-compensation**

> **L'échec d'une condition bloquante ne peut être compensé par aucune performance quantitative** :
> ni une meilleure p-value, ni un meilleur profit factor, ni un meilleur rendement, ni un meilleur
> drawdown, ni aucune autre métrique.
>
> La conjonction des conditions bloquantes est stricte. Aucun arbitrage numérique n'y est admis.

### Fondement de la classification

**[NORMATIF]**

L'appartenance d'une condition à l'une des trois catégories découle de la nature de ce qu'elle
garantit.

| Catégorie | Ce que la condition garantit | Motif du caractère non compensable |
|---|---|---|
| **[BLOQUANTE]** | **Validité de la preuve** — la mesure signifie-t-elle ce qu'elle prétend signifier ? | Une preuve invalide ne devient pas valide parce qu'une autre métrique est favorable |
| **[RENFORCEMENT]** | **Solidité et robustesse de l'effet** — l'effet mesuré résiste-t-il à des variations raisonnables ? | Une robustesse moindre n'invalide pas la preuve ; elle en réduit la portée, donc le niveau atteint |
| **[CONTEXTUELLE]** | **Compatibilité avec le portefeuille et le contexte d'exploitation** | Dépend d'un environnement extérieur à l'hypothèse, non de sa véracité |

**[NORMATIF]** Toute condition nouvelle ajoutée ultérieurement au §5.3 est classée selon ce fondement,
et non selon son importance apparente ou la difficulté de la satisfaire.

> **Traçabilité.** La classification du §5.3 et le fondement ci-dessus ont été arbitrés et validés le
> 21 août 2026. Ils ne relèvent plus d'un choix d'implémentation et ne peuvent être modifiés que par
> un arbitrage explicite consigné au journal des versions.

## 5.2 — Spécification préalable des contrôles

**[NORMATIF]**

Pour chaque condition du §5.3, la charte spécifie à son élément 10, **avant tout calcul
confirmatoire** :

```
périmètre exact du contrôle
procédure
critère de rejet
rôle du contrôle
```

**Typologie des rôles :**

| Rôle | Effet sur `N_famille` |
|---|---|
| **R1 — Condition de rejet** | N'entre pas, si le critère est fixé à l'avance et non révisable |
| **R2 — Diagnostic sans effet sélectif** | N'entre pas |
| **R3 — Source possible de variante candidate** | **Entre dans `N_famille`** |

**[NORMATIF]** Un contrôle non spécifié avant le calcul confirmatoire est réputé de rôle R3 et entre
dans `N_famille`.

**Pourquoi :** sans cette règle, la définition a posteriori du périmètre d'un contrôle transformerait
la promotion multi-critères en second mécanisme de sélection non comptabilisé.

## 5.3 — Conditions

**[NORMATIF]**

| # | Condition | Catégorie |
|---|---|---|
| 0 | Charte complète, horodatée, antérieure au premier calcul confirmatoire | **[BLOQUANTE]** |
| 1 | Taille effective d'échantillon conforme au §1, dépendance traitée selon le §1.5 | **[BLOQUANTE]** |
| 2 | Significativité sur la phase B au seuil corrigé du §2.B, test spécifié selon le §1.9 | **[BLOQUANTE]** |
| 3 | Statut probatoire du juge suffisant pour le niveau de preuve visé (§4.3, §7) | **[BLOQUANTE]** |
| 4 | Survie aux coûts complets selon un modèle de coûts opérationnellement défini | **[SUSPENDU]** |
| 5 | Audit des biais sans anomalie critique | **[BLOQUANTE]** |
| 6 | Gel technique effectif et reproductibilité vérifiée (§3.4) | **[BLOQUANTE]** |
| 7 | Stabilité paramétrique (§5.5) | **[RENFORCEMENT]** |
| 8 | Stabilité temporelle sur sous-périodes indépendantes | **[RENFORCEMENT]** |
| 9 | Robustesse à l'intérieur du domaine de généralisation déclaré (élément 5 de la charte) | **[RENFORCEMENT]** |
| 10 | Drawdown compatible avec le portefeuille et le champion en place | **[CONTEXTUELLE]** |
| 11 | Cohérence par régime | **[SUSPENDU]** — voir §5.7 |

**[NORMATIF] — Domaine de généralisation.** La condition 9 s'apprécie **exclusivement à l'intérieur du
domaine déclaré**. Une hypothèse conçue pour un actif ou un contexte spécifique n'est pas disqualifiée
par son absence de généralisation à des contextes extérieurs à ce domaine.

**[NORMATIF]** Une promotion ne peut être prononcée si la charte n'a pas fixé les valeurs des
paramètres opérationnels dont dépendent les conditions 7, 8, 9 et 10.

**[NORMATIF] — Conditions 3 et 6.** Le **statut probatoire du juge** (c.3) et le **gel technique**
(c.6) relèvent de la catégorie bloquante au titre du fondement du §5.1 : tous deux conditionnent la
validité de la preuve, non la solidité de l'effet.

Un résultat obtenu sur un juge de statut insuffisant ne mesure pas ce qu'il prétend mesurer. Un
résultat non reproductible ne peut être vérifié. **Dans les deux cas, aucune performance mesurée ne
peut rétablir la validité de la mesure.**

> **Traçabilité.** Le classement de ces deux conditions a été arbitré et validé le 21 août 2026.

## 5.4 — Articulation avec le niveau de preuve

**[NORMATIF]**

```
Toutes les conditions bloquantes satisfaites     → promotion possible
Conditions de renforcement satisfaites           → niveau de preuve élevé (§7)
Conditions de renforcement partiellement échouées→ niveau de preuve abaissé (§7)
Une condition bloquante échouée                  → aucune promotion
```

**[NORMATIF]** Une condition de renforcement échouée **ne se rachète pas** par une meilleure
performance sur une autre condition. Elle abaisse le niveau de preuve, ce qui restreint les
conséquences de la promotion.

## 5.5 — Stabilité paramétrique

**[PARAMÈTRE OPÉRATIONNEL]**

Méthode : déplacer chaque paramètre d'un cran de part et d'autre de la valeur retenue et mesurer la
dégradation.

**[RECOMMANDATION]** Une formulation relative — perte maximale admise en proportion de la valeur
centrale — est transposable d'une stratégie à l'autre et ne fige aucune métrique absolue.

**[NORMATIF] — Contrôle de voisinage et traitement dans `N_famille`**

> Un contrôle de voisinage ne peut être traité comme exclusivement diagnostique que si **son rôle
> décisionnel est spécifié dans la charte avant toute observation de ses résultats**.

Un contrôle de voisinage est exclusivement diagnostique ou falsificationnel lorsque, **avant son
exécution**, la charte définit :

```
les paramètres ou configurations voisines examinés
la méthode de calcul et les données utilisées
les règles d'interprétation
son objet limité de diagnostic ou de falsification
```

**[NORMATIF] — Interdictions attachées à ce statut.** Dans ce cas, le contrôle ne peut pas servir à
modifier la configuration centrale, le domaine, l'hypothèse, le test primaire, le critère de réussite,
le critère de promotion, le critère d'abandon, les frontières ou le budget déclarés.

Il ne peut pas non plus être invoqué après observation pour renforcer post hoc la conclusion centrale,
justifier une promotion, justifier la poursuite de la recherche ou éviter un abandon.

**[NORMATIF]** Lorsque toutes ces conditions sont satisfaites, le contrôle de voisinage est traité
comme **contrôle diagnostique pré-spécifié** et n'entre pas, à ce titre, dans `N_famille`.

**[NORMATIF] — Rôle décisionnel.** Dès lors que les résultats du voisinage peuvent influencer une
décision concernant la configuration centrale — y compris une décision de sélectionner, poursuivre,
promouvoir, conserver, abandonner ou **qualifier la robustesse** de l'hypothèse — le contrôle possède
un rôle décisionnel. Il doit alors être enregistré et gouverné selon les règles applicables du présent
document relatives au budget (§2.A), à la famille de recherche (§4.5), à la multiplicité (§2.B) et à
la consommation informationnelle (§4).

**[NORMATIF]** **Le maintien inchangé de la configuration centrale après observation des voisins ne
suffit pas, à lui seul, à qualifier le contrôle comme non décisionnel.**

**Constat conservé.** Ce contrôle a été appliqué sur une recherche antérieure — configuration au
centre d'un plateau, tous voisins au-dessus du plancher. **Cela n'a pas suffi**, l'artefact étant dans
les données. Le critère est nécessaire, non suffisant.

## 5.6 — Dégradation entre phases

**[PARAMÈTRE OPÉRATIONNEL]**

Une dégradation entre la phase A et la phase B est **attendue** : elle mesure la part de sélection.

**[NORMATIF] — Conséquence d'un effondrement**

> Un effondrement en territoire négatif **déclenche un examen des causes possibles**. Aucune cause ne
> peut être présumée automatiquement.

Causes à examiner :

```
variance d'échantillonnage
changement de régime
coûts sous-estimés
hypothèse réellement fausse
problème de données
problème de code
autre artefact méthodologique
```

**[NORMATIF]** L'examen conclut à l'une des trois qualifications du §6.2 — falsification, invalidation
de l'essai, ou résultat non interprétable — et la conséquence en découle.

**[NORMATIF] — Conditionnement du critère relatif**

> Un critère de dégradation exprimé en pourcentage est manipulable et **doit être conditionné à un
> niveau absolu minimal**.

**Démonstration.** Une dégradation de 49 % d'une espérance de conception faible et une dégradation de
36 % d'une espérance élevée sont comparables en taux et sans rapport en niveau. Un critère purement
relatif classerait les deux situations de façon équivalente.

La charte fixe donc **deux valeurs** : le taux maximal admis et le niveau absolu minimal en deçà
duquel le ratio n'a plus de sens.

## 5.7 — Cohérence par régime

**[SUSPENDU]**

La condition 11 du §5.3 est **inactive**. Elle ne peut fonder aucune décision de promotion ou de
rejet.

**Elle ne redeviendra active qu'une fois définis les cinq éléments suivants :**

```
taxonomie des régimes
méthode de classification
moment de déclaration de la classification
critère d'incohérence
conséquence décisionnelle
```

**[INTERFACE]** Ces définitions relèvent d'un document dédié.

---

# 6. Invalidation, falsification et abandon

## 6.1 — Symétrie avec la promotion

**[NORMATIF]**

Un protocole qui définit quand conserver sans définir quand abandonner rend la persévérance
indistinguable de l'acharnement.

## 6.2 — Trois qualifications distinctes

**[NORMATIF]**

| Qualification | Définition | Conséquence sur l'hypothèse | Conséquence sur l'essai |
|---|---|---|---|
| **A — Invalidation de l'essai** | Erreur de données confirmée, défaut de code, violation documentée du protocole, changement de spécification contractuelle | **Aucune** | Résultat annulé |
| **B — Falsification de l'hypothèse** | Réalisation des conditions de falsification déclarées à l'élément 6 de la charte, sur un essai valide | **Abandon de la piste** | — |
| **C — Résultat non interprétable** | Événement rendant le test non concluant sans le falsifier ni l'invalider | **Aucune** | Résultat sans portée |

**[NORMATIF]** Les conditions relevant de A et de C sont déclarées à l'élément 7 de la charte, **avant**
le calcul confirmatoire. Une condition d'invalidation invoquée après lecture d'un résultat défavorable
et non déclarée à l'avance **n'est pas recevable**.

### Règle de non-restitution

**[NORMATIF]**

> **Une invalidation ne restitue pas une consultation déjà effectuée.** Les données observées lors
> d'un essai invalidé demeurent consultées à l'intensité correspondante au sens du §4.2, et le statut
> probatoire de la période est mis à jour au registre.

**Pourquoi :** sans cette règle, invoquer un défaut de code permettrait de récupérer un juge
contaminé.

**[NORMATIF]** Un essai invalidé peut être rejoué **sous réserve du statut probatoire résultant**.
Si ce statut est devenu insuffisant, les voies du §4.7 s'appliquent.

## 6.3 — Conditions d'abandon

**[NORMATIF] pour la liste, [PARAMÈTRE OPÉRATIONNEL] pour les seuils**

| Condition | Statut |
|---|---|
| Taille effective disponible inférieure au requis, sans voie du §1.1 praticable | NORMATIF |
| Aucune période de statut suffisant, et aucune voie du §4.7 praticable | NORMATIF |
| Avantage détruit par les coûts complets | NORMATIF |
| Falsification au sens du §6.2-B | NORMATIF |
| Nombre de cycles de reprise dépassé | PARAMÈTRE OPÉRATIONNEL |

## 6.4 — Nombre de reprises autorisées

**[PARAMÈTRE OPÉRATIONNEL]**

Sans plafond, chaque reprise ajoute des éléments à `N_budget` sans que personne n'en tienne le compte.

---

# 7. Niveaux de preuve

**[NORMATIF]**

Le niveau de preuve atteint détermine les conséquences admissibles d'une promotion.

| Niveau | Conditions | Conséquences admissibles |
|---|---|---|
| **N0 — Exploratoire** | Régime exploratoire | Aucune. Formulation d'hypothèses uniquement |
| **N1 — Prévalidation** | Conditions bloquantes satisfaites sur juge de statut **faible** | Aucun engagement de capital. Ouvre une confirmation prospective |
| **N2 — Validation restreinte** | Conditions bloquantes satisfaites sur juge de statut **réduit**, renforcement partiel | Engagement de capital limité, sous réserve de confirmation prospective en cours |
| **N3 — Validation** | Conditions bloquantes satisfaites sur juge de statut **plein**, renforcement satisfait | Engagement de capital selon la politique de risque |
| **N4 — Validation confirmée** | N3 **et** confirmation prospective satisfaisante (phase D) | Niveau le plus élevé |

**[NORMATIF]** Le niveau de preuve visé est déclaré dans la charte. Un niveau supérieur au statut
probatoire du juge disponible ne peut être atteint, quelle que soit la performance mesurée.

### Fondement de la hiérarchie

**[NORMATIF]**

Le niveau atteint résulte de la conjonction de deux facteurs, et **ne peut excéder ce que le moins
favorable des deux autorise**.

| Facteur | Origine | Effet sur le niveau |
|---|---|---|
| **Statut probatoire du juge** | §4.3 — état et intensité de consultation de la période | Plafonne le niveau atteignable |
| **Satisfaction des conditions de renforcement** | §5.3 c.7 à c.9 | Détermine le niveau à l'intérieur de ce plafond |

**[NORMATIF]** Le franchissement des seules conditions bloquantes ouvre la promotion ; il ne détermine
pas à lui seul le niveau atteint.

**[NORMATIF]** Aucune performance quantitative ne relève un plafond fixé par le statut probatoire du
juge. Un résultat exceptionnel obtenu sur un juge de statut faible demeure au niveau N1.

> **Traçabilité.** Les cinq échelons N0 à N4, leurs conditions et leurs conséquences admissibles ont
> été arbitrés et validés le 21 août 2026. Ils constituent l'implémentation retenue de la hiérarchie
> de preuve et ne peuvent être modifiés que par un arbitrage explicite consigné au journal des
> versions.

**[RECOMMANDATION]** Avant d'engager un suivi prospectif, calculer sa durée nécessaire à partir de la
taille effective requise et du rythme attendu, puis l'accepter explicitement.

---

# 8. Architecture et paramètres opérationnels

## 8.A — Architecture méthodologique

**Cadre permanent, indépendant de toute recherche particulière.**

| Élément | Section |
|---|---|
| Liberté méthodologique encadrée — déclaré, justifié, traçable, conséquent | Règle cardinale |
| Aucune métrique isolée ne déclenche une décision | Règle cardinale |
| Distinction exploratoire / confirmatoire | 0.1 |
| Définition de l'engagement de capital | 0.1 |
| Séquence officielle, charte obligatoire et immuable | 0.2, 0.3 |
| Justification économique et limitation assumée | 0.4 |
| Justification préalable de la taille d'échantillon | 1.1 |
| Effet visé défini ex ante | 1.2 |
| Voie analytique — dimensionnement du test primaire, unilatéral et bilatéral | 1.3 |
| Voie alternative obligatoire à défaut | 1.4 |
| Unité statistique déclarée, dépendance traitée, regroupement heuristique | 1.5 |
| Estimation ex ante de la dispersion, restriction sur la dérivation analytique | 1.6 |
| Spécification du test en huit éléments | 1.9 |
| Séparation `N_budget` / `N_famille` | 2.A, 2.B.1 |
| Correction de multiplicité, description exacte de Bonferroni | 2.B.2 |
| Architecture des phases et gel de configuration | 3.1 |
| Gel et modification des frontières | 3.2 |
| Gel technique et interface | 3.4 |
| Trois états, trois intensités, conditions d'attribution de I1 et du statut plein | 4.1, 4.2, 4.2 bis, 4.3 |
| Traitement des actifs corrélés | 4.4 |
| Famille de recherche, critères disjonctifs, revue indépendante | 4.5 |
| Registre | 4.6 |
| Hiérarchie de preuve à l'épuisement | 4.7 |
| Catégories de conditions, non-compensation et fondement de la classification | 5.1 |
| Spécification préalable des contrôles et typologie des rôles | 5.2 |
| Qualification décisionnelle des contrôles de voisinage et traitement dans `N_famille` | 5.5 |
| Conséquence d'un effondrement, conditionnement du critère relatif | 5.6 |
| Trois qualifications, non-restitution d'une consultation | 6.2 |
| Niveaux de preuve et fondement de la hiérarchie | 7 |

## 8.B — Paramètres opérationnels

**Valeurs fixées dans la charte de chaque recherche confirmatoire.**

**[NORMATIF]** Ces paramètres n'ont pas à être arbitrés à l'avance ni de façon universelle. Ils
doivent être **fixés dans la charte avant le premier calcul confirmatoire**, et **aucune promotion ne
peut être prononcée** si la charte concernée ne les a pas fixés.

| # | Paramètre | Section | Recommandation |
|---|---|---|---|
| 1 | Rendement annuel minimal exploitable | 1.7 | non |
| 2 | Seuil α et puissance | 1.8 | oui — α plus strict que 0,05 |
| 3 | Méthode de correction pour tests multiples | 2.B.2 | non |
| 4 | Taille de `N_budget` | 2.A.3 | oui — budget restreint |
| 5 | Longueur relative des périodes | 3.3 | oui — dimensionner par la fréquence |
| 6 | Plancher de stabilité paramétrique | 5.5 | oui — formulation relative |
| 7 | Dégradation maximale et niveau absolu minimal | 5.6 | conditionnement : NORMATIF ; valeurs : paramètres |
| 8 | Tolérance de drawdown | 5.3 c.10 | oui — exprimée en pourcentage du capital |
| 9 | Nombre de cycles de reprise | 6.4 | non |

## 8.C — Complétude

**[NORMATIF]**

Le présent document est complet et applicable **sous une réserve explicite** : les conditions 4 et 11 du §5.3
sont **suspendues** et ne peuvent fonder aucune décision tant que les conditions opérationnelles
nécessaires à leur activation ne sont pas définies.

Aucune autre condition n'est suspendue. L'absence de valeurs pour les paramètres du §8.B n'affecte pas
la complétude du document : elle empêche seulement de prononcer une promotion tant qu'une charte ne
les a pas fixés pour la recherche concernée.

---

# 9. Interfaces inter-documents

**[INTERFACE]**

| Sujet | Traité par `04` | Relève de |
|---|---|---|
| Contrôles de qualité et de continuité des données | Principe rappelé au §0.1 | `05` |
| Modèle de coûts complets | Condition suspendue §5.3 c.4 ; détail opérationnel non encore validé | `05` |
| Procédure détaillée du gel technique | Principe et périmètre §3.4 | `05` ou document technique dédié |
| Capacité, liquidité, impact de marché, exposition factorielle, levier | Non traités | `05` ou document de risque |
| Taxonomie et classification des régimes | Condition suspendue §5.7 | Document dédié |
| Modalités de la revue indépendante | Principe §4.5 | Protocole de gouvernance |
| Surveillance post-promotion, dégradation d'un champion, rétrogradation | **Non traités** | Phases 11 et 12 de la checklist |

**[NORMATIF]** Aucune exigence de `04` ne peut être considérée comme satisfaite par renvoi implicite à
un autre document. Un renvoi n'est valide que s'il figure au présent tableau.

---

# 10. Points signalés

**A — Praticabilité des conditions bloquantes.** La conjonction de sept conditions bloquantes n'a pas
été éprouvée sur un système connu pour être exploitable. Un test de calibration rétrospective
lèverait ce doute. **Non traité dans cette version.**

**B — Calibration du regroupement.** Le §1.5 qualifie le regroupement d'heuristique conservatrice sans
qu'une étude de calibration ait été conduite. Tant qu'elle ne l'est pas, la qualification
d'heuristique doit être maintenue.

**C — Coût de la politique de consommation.** Le nombre de cycles confirmatoires qu'un historique
réel autorise avant épuisement n'a pas été mesuré. Détermine si la hiérarchie de preuve du §7 suffit
en pratique.

**D — Surveillance post-promotion.** `04` ne traite ni les critères de désactivation d'un champion, ni
la multiplicité créée par les contrôles répétés en suivi réel. Lacune réelle, hors périmètre.

---

# 11. Journal des versions

| Version | Date | Changement |
|---|---|---|
| 0.1 | 20/08/2026 | Rédaction initiale |
| 0.2 | 21/08/2026 | Principe multi-critères, correction de la circularité de `d`, séparation budget / correction / contrôles avancés, retrait des seuils exprimés en SQN |
| 0.3 | 21/08/2026 | Régimes exploratoire et confirmatoire, charte de recherche, nouveau §0 |
| 0.4 | 21/08/2026 | Famille de recherche, indépendance des observations, distinction consultée / consommée, séparation architecture / paramètres |
| 0.5 | 21/08/2026 | Contre-expertise externe et arbitrage croisé. Corrections F1–F17, implémentations F18–F24, architecture D1–D10. Statuts décisionnels bloquante / renforcement / contextuelle, niveaux de preuve, intensités de consultation, statut probatoire, architecture des phases, gel technique, séparation `N_budget` / `N_famille`, correction factuelle sur Bonferroni |
| 0.6.1 | 21/08/2026 | **Intégration de trois patches d'audit externe.** M-01 : le statut I1 devient procédural et vérifiable — périmètre informationnel défini, traçabilité exigée, statut plein conditionné (§4.2, §4.2 bis, §4.3). M-02 : un contrôle de voisinage n'échappe à `N_famille` que si son rôle décisionnel est pré-spécifié ; le maintien de la configuration ne suffit plus (§5.5). M-03 : formule de dimensionnement restreinte au test primaire, notation unilatérale et bilatérale explicitée (§1.3). Aucune autre modification |
| 0.6 | 21/08/2026 | **Arbitrage explicite de deux points d'implémentation.** §5.1 : fondement de la classification des conditions — validité de la preuve, solidité de l'effet, compatibilité de contexte — et règle de classement des conditions futures. §5.3 : justification du caractère bloquant des conditions 3 et 6. §7 : fondement de la hiérarchie — plafond par le statut du juge, position par les conditions de renforcement. Aucune modification de fond ailleurs |
| 0.6.2 | 23/08/2026 | **Correction chirurgicale CTR-01.** La condition §5.3 c.4 relative aux coûts complets est suspendue tant que le modèle de coûts n'est pas opérationnellement défini ; §8.C et §9 sont mis en cohérence. Aucune autre modification de fond |
