# Critères de validation

**Version :** 0.1 — PROPOSITION, non validée
**Date :** 20 août 2026
**Statut :** soumis à arbitrage — aucune règle de ce document n'est en vigueur
**Position :** `01-SYSTEM-VISION` → `02-ASSET-PROFILE-DATABASE` → `03-REGIME-EXPERT-RESEARCH-FOUNDATION` → **`04-VALIDATION-CRITERIA`** → `05-DATA-CONTRACT`

---

## Objet

Ce document fixe **avant toute recherche** ce qui constitue une preuve suffisante pour conserver, promouvoir ou abandonner une hypothèse.

Sans critères définis à l'avance, la décision de conclure reste discrétionnaire, et le biais que le protocole cherche à éliminer se réintroduit au moment précis où l'on tranche.

---

## Convention de statut

Chaque règle porte l'un des trois statuts suivants.

| Statut | Signification |
|---|---|
| **NORMATIF** | Règle méthodologique universelle ou dérivation mathématique. Verrouillable immédiatement. Ne dépend d'aucune préférence. |
| **PARAMÈTRE À DÉCIDER** | Valeur dépendant de la philosophie de recherche ou de la tolérance au risque. La méthode de détermination est proposée ; **la valeur ne l'est pas**. |
| **RECOMMANDATION** | Aide à la décision, non contraignante. |

> **Règle de lecture :** un nombre figurant dans ce document au statut NORMATIF résulte d'un calcul reproductible. Un nombre au statut PARAMÈTRE À DÉCIDER est un exemple d'illustration, jamais une valeur adoptée.

---

# 1. Taille d'échantillon

## 1.1 — Calcul du seuil minimal — **NORMATIF**

Avant tout test, la taille d'échantillon minimale se calcule par analyse de puissance :

```
n_min = (z_α + z_β)² / d²

d   = espérance par transaction / écart-type par transaction
z_α = quantile normal du seuil de significativité retenu
z_β = quantile normal de la puissance retenue
```

Pour α = 0,05 unilatéral et une puissance de 80 % : `(1,645 + 0,842)² = 6,183`, donc :

```
n_min ≈ 6,19 / d²
```

| d visé | n_min |
|---|---|
| 0,30 | 69 |
| 0,20 | 155 |
| 0,15 | 275 |
| 0,10 | 619 |
| 0,08 | 967 |
| 0,05 | 2 474 |

**Pourquoi normatif :** c'est une identité mathématique, indépendante de toute préférence.

**Risque empêché :** conclure sur un échantillon incapable de porter la conclusion.

**Conséquence sur Sweep + MSS :** l'effet réel mesuré sur données continues vaut d = 0,022. Le calcul exigeait **plus de 12 000 transactions**. La validation en comptait 230. Le projet aurait été arrêté au cadrage, avant tout backtest.

## 1.2 — Effet minimal à détecter — **PARAMÈTRE À DÉCIDER**

La valeur de `d` visée détermine tout le reste : plus l'ambition est modeste, plus l'échantillon requis est grand.

**Méthode de détermination proposée :** partir de l'objectif économique, non de l'objectif statistique.

```
1. Fixer le rendement annuel net minimal jugé digne d'être exploité
2. Estimer le nombre de transactions par an du type de stratégie visé
3. En déduire l'espérance par transaction requise
4. Estimer l'écart-type par transaction à partir du profil de sortie
5. d = espérance / écart-type
6. Vérifier que n_min est atteignable sur les données disponibles
```

**Si n_min dépasse l'échantillon disponible, la piste doit être écartée au cadrage** — c'est une condition d'entrée, non un résultat.

## 1.3 — Puissance et seuil de significativité — **PARAMÈTRE À DÉCIDER**

α = 0,05 et puissance 80 % sont les conventions académiques usuelles. Elles ne sont pas obligatoires.

**Arbitrage requis :** un α plus strict réduit les faux positifs mais augmente n_min ; une puissance plus élevée réduit les faux négatifs au même prix. Le choix dépend du coût relatif des deux erreurs dans ce projet — trader une stratégie sans avantage, ou écarter une stratégie qui en avait un.

---

# 2. Budget d'hypothèses et tests multiples

## 2.1 — Déclaration préalable du nombre de tests — **NORMATIF**

Le nombre N de combinaisons à évaluer doit être **déclaré avant** le premier calcul, dans le document de cadrage de la recherche.

Toute exploration supplémentaire non prévue exige une déclaration amendée et datée, avec recalcul du seuil corrigé.

**Risque empêché :** data snooping. Le document `03` le nomme sans en tirer de règle opératoire.

**Conséquence sur Sweep + MSS :** aucun budget n'avait été déclaré. 7 400 combinaisons ont été évaluées, dont le décompte n'a été établi qu'a posteriori.

## 2.2 — Nécessité d'une correction — **NORMATIF**

Le seuil de significativité usuel ne vaut que pour **un seul** test. En enchaînant N tests indépendants au seuil α, le nombre attendu de faux positifs vaut `α × N`.

| N tests | Faux positifs attendus à α = 0,05 |
|---|---|
| 1 | 0,05 |
| 100 | 5 |
| 1 000 | 50 |
| 7 400 | **370** |

**Une correction pour tests multiples est donc obligatoire dès que N > 1.** Le principe est normatif ; la méthode de correction est un paramètre.

## 2.3 — Méthode de correction — **PARAMÈTRE À DÉCIDER**

Deux familles usuelles, aux propriétés opposées.

| Méthode | Contrôle | Caractère |
|---|---|---|
| **Bonferroni** | taux d'erreur familial : probabilité d'au moins un faux positif | très conservatrice |
| **Benjamini-Hochberg** | taux de fausses découvertes : proportion de faux positifs parmi les retenus | plus permissive |

Sous Bonferroni, `α_corrigé = α / N`, ce qui donne pour α = 0,05 :

| N | α corrigé | Seuil équivalent en SQN |
|---|---|---|
| 10 | 5,0 × 10⁻³ | 2,58 |
| 100 | 5,0 × 10⁻⁴ | 3,29 |
| 1 000 | 5,0 × 10⁻⁵ | 3,89 |
| 7 400 | 6,8 × 10⁻⁶ | **4,35** |

**Arbitrage requis :** Bonferroni suppose les tests indépendants, ce qui est faux quand on balaie des paramètres voisins — elle est donc excessivement stricte en pratique. Benjamini-Hochberg est mieux adaptée à des tests corrélés mais accepte une proportion de faux positifs.

**Conséquence sur Sweep + MSS :** avec 7 400 tests, le seuil Bonferroni était de 4,35. La configuration retenue affichait 5,04 en conception — **elle aurait franchi le seuil**. Ce constat est important : la correction seule n'aurait pas suffi à éviter l'échec. C'est le contrôle de continuité des données (document `05`) qui aurait tranché.

## 2.4 — Comptabilisation des tests — **NORMATIF**

Comptent dans N :
- toute combinaison de paramètres évaluée ;
- tout filtre testé ;
- toute variante de règle d'entrée ou de sortie ;
- tout actif supplémentaire testé avec la même hypothèse ;
- toute période supplémentaire testée après un premier résultat.

Ne comptent pas :
- les contrôles de stabilité au voisinage d'une configuration **déjà retenue**, dès lors qu'ils ne servent pas à en changer.

---

# 3. Frontières temporelles

## 3.1 — Gel et datation — **NORMATIF**

Les dates exactes séparant conception, validation et hors échantillon doivent être **inscrites dans le document de cadrage avant tout calcul**.

Tout déplacement d'une frontière exige une nouvelle version datée du document, accompagnée d'une justification indépendante des résultats observés.

**Risque empêché :** redécoupage opportuniste — choisir la coupure qui donne le meilleur résultat.

**Conséquence sur Sweep + MSS :** la frontière de validation a été déplacée de 2025 à 2024 en cours de projet pour élargir l'échantillon de test. La justification était légitime, **mais le déplacement n'a jamais été tracé**.

## 3.2 — Justification recevable d'un déplacement — **NORMATIF**

Un déplacement de frontière n'est recevable que s'il repose sur une propriété **des données ou du marché**, jamais sur un résultat.

Exemples recevables : rupture documentée de couverture d'une source, changement structurel d'instrument, indisponibilité de données.

Exemple non recevable : élargir la période de validation parce que la précédente comptait trop peu de transactions **après avoir constaté ce nombre**.

## 3.3 — Longueur relative des périodes — **PARAMÈTRE À DÉCIDER**

**Méthode proposée :** dimensionner la période de validation pour qu'elle contienne au moins `n_min` transactions au rythme attendu, puis attribuer le reste à la conception.

Cette approche fait dépendre le découpage de la fréquence du signal plutôt que d'une proportion arbitraire.

---

# 4. Consommation de l'échantillon

## 4.1 — Principe de consommation — **NORMATIF**

Une période hors échantillon est **consommée dès sa première lecture**. Elle ne peut plus servir de juge pour une hypothèse portant sur le même actif et la même famille de stratégie.

**Pourquoi :** relire une période dont on connaît le contenu la transforme en seconde période de conception. Le juge devient partie.

**Risque empêché :** le mécanisme le plus insidieux du data snooping — tester le candidat suivant jusqu'à ce qu'un passe.

**Conséquence sur Sweep + MSS :** la période 2024-2026 a été lue **trois fois** — rapport v2, rapport v3, reproduction sur données continues. Dès la deuxième lecture, plus aucun juge indépendant n'existait.

## 4.2 — Registre de consommation — **NORMATIF**

Chaque actif porte un registre tenu à jour, indiquant pour chaque période :

```
Actif           : ...
Période         : du ... au ...
Statut          : VIERGE | CONSOMMÉE
Lectures        : nombre, dates, hypothèse testée
Périodes vierges restantes : ...
```

Aucune validation ne peut être déclarée sur une période marquée CONSOMMÉE.

## 4.3 — Reconstitution d'un échantillon vierge — **NORMATIF**

Lorsqu'aucune période vierge ne subsiste sur un actif, trois voies seulement restent ouvertes :

1. accumuler des données futures par suivi réel ou en démonstration ;
2. changer d'actif, à condition que l'hypothèse ait un sens structurel sur le nouvel actif ;
3. abandonner la piste.

**Aucune autre voie n'est recevable.** En particulier, il n'est pas possible de « redécouper autrement » une période déjà consommée.

---

# 5. Critères de promotion

## 5.1 — Structure de la décision — **NORMATIF**

Une promotion exige la satisfaction de **toutes** les conditions ci-dessous. Aucune ne peut compenser une autre. Le rendement seul n'est jamais suffisant.

| # | Condition | Nature du critère |
|---|---|---|
| 1 | Taille d'échantillon ≥ n_min (§1.1) | dérivé — NORMATIF |
| 2 | Significativité hors échantillon au-delà du seuil corrigé (§2.3) | dérivé — NORMATIF |
| 3 | Stabilité paramétrique : aucun voisin immédiat sous un plancher | seuil — À DÉCIDER |
| 4 | Stabilité temporelle : positif sur chaque sous-période indépendante | À DÉCIDER (nombre et découpage) |
| 5 | Survie aux coûts complets | dérivé — NORMATIF |
| 6 | Drawdown ne dégradant pas le champion au-delà d'une tolérance | seuil — À DÉCIDER |
| 7 | Audit des biais sans anomalie critique | NORMATIF |

**Le caractère cumulatif des sept conditions est normatif. Les valeurs des conditions 3, 4 et 6 sont des paramètres à arbitrer.**

## 5.2 — Plancher de stabilité paramétrique — **PARAMÈTRE À DÉCIDER**

**Méthode proposée :** déplacer chaque paramètre d'un cran de part et d'autre de la valeur retenue et mesurer la dégradation.

Trois formulations possibles du critère, à arbitrer :
- aucun voisin ne descend sous un SQN plancher fixé ;
- aucun voisin ne perd plus de X % de l'espérance centrale ;
- la médiane des voisins reste au-dessus d'un plancher.

**Justification du besoin :** une configuration entourée de voisins faibles est un maximum local, signature du surajustement. Une configuration au centre d'un plateau est robuste.

**Conséquence sur Sweep + MSS :** ce contrôle a été appliqué — 28 voisins testés, minimum 2,36, médiane 4,60. La configuration était bien un plateau. **Cela n'a pas suffi**, l'artefact étant dans les données et non dans les paramètres. Le critère reste nécessaire, mais il n'est pas suffisant.

## 5.3 — Tolérance de dégradation entre conception et validation — **PARAMÈTRE À DÉCIDER**

Une dégradation de l'espérance entre conception et validation est **attendue et saine** : elle mesure la part de chance dans la sélection. Un effondrement en territoire négatif signale un artefact.

**Arbitrage requis :** à partir de quel taux de dégradation refuse-t-on la promotion ?

**Élément de repère :** sur Sweep + MSS, la dégradation observée était de 36 % — apparemment acceptable. **Sur données propres, l'espérance de conception n'était que de +0,022 R et la validation de 230 trades ne pouvait pas fournir la puissance nécessaire.**

---

# 6. Survie aux coûts

## 6.1 — Coûts complets — **NORMATIF**

Toute métrique de performance utilisée pour une promotion doit intégrer les coûts pertinents : spread, commission, glissement et financement le cas échéant.

Une stratégie qui n'est positive qu'avant coûts ne constitue pas une preuve d'exploitabilité.

## 6.2 — Sensibilité aux coûts — **RECOMMANDATION**

Présenter une analyse de sensibilité aux coûts permet de distinguer une stratégie robuste d'une stratégie dont l'avantage est entièrement absorbé par une petite variation du modèle d'exécution.

---

# 7. Drawdown et risque

## 7.1 — Mesure obligatoire — **NORMATIF**

La performance doit être accompagnée au minimum du drawdown maximal, de sa durée, de la série maximale de pertes et de la distribution des pertes.

## 7.2 — Tolérance — **PARAMÈTRE À DÉCIDER**

Le plafond de drawdown acceptable dépend du portefeuille cible et du budget de risque global. Il doit être fixé avant la promotion et ne peut être ajusté après observation des résultats.

---

# 8. Audit des biais

## 8.1 — Audit indépendant — **NORMATIF**

Avant toute promotion, un audit des biais doit rechercher au minimum : fuite d'information future, survivorship bias, look-ahead, data snooping, sélection opportuniste de période, biais de liquidité, biais de coûts, discontinuités de données et divergence d'implémentation.

Une anomalie critique entraîne l'échec automatique de la promotion, indépendamment de la performance.

## 8.2 — Traçabilité — **NORMATIF**

Chaque conclusion de l'audit doit être reliée à une preuve reproductible : test, rapport, identifiant de jeu de données, version de code ou journal d'exécution.

---

# 9. Décision de promotion

## 9.1 — États possibles — **NORMATIF**

Une hypothèse ne peut terminer une campagne que dans l'un des états suivants :

```
PROMUE
REJETÉE
INCONCLUSIVE
BLOQUÉE — ANOMALIE DE DONNÉES
BLOQUÉE — ANOMALIE MÉTHODOLOGIQUE
```

L'état **INCONCLUSIVE** est obligatoire lorsque les données ne permettent pas de conclure sans attribuer artificiellement un succès ou un échec.

## 9.2 — Interdiction de forcer une décision — **NORMATIF**

L'absence de preuve suffisante ne peut jamais être convertie en rejet de l'hypothèse ni en promotion. Elle doit rester **INCONCLUSIVE**.

---

# 10. Registre de décision

Toute décision finale doit enregistrer :

```
Hypothèse
Version de la spécification
Jeu(x) de données et identifiants
Budget N déclaré / N consommé
Périodes conception / validation / vierges restantes
n_min et n observé
Métriques avant / après coûts
Résultats des contrôles de stabilité
Audit des biais
Décision
Justification
Date
```

Le registre constitue la trace d'audit de la campagne. Une décision non enregistrée n'est pas considérée comme une décision du protocole.
