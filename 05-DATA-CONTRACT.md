# Contrat de données

**Version :** 0.1 — PROPOSITION, non validée
**Date :** 20 août 2026
**Statut :** soumis à arbitrage — aucune règle de ce document n'est en vigueur
**Position :** `01-SYSTEM-VISION` → `02-ASSET-PROFILE-DATABASE` → `03-REGIME-EXPERT-RESEARCH-FOUNDATION` → `04-VALIDATION-CRITERIA` → **`05-DATA-CONTRACT`**

---

## Objet

Toute donnée entrant dans un calcul doit porter une fiche d'identité vérifiable, et tout moteur qui
parcourt une série doit prouver qu'il en respecte les hypothèses.

Ce document est né d'un échec précis : le rapport v3 de la stratégie Sweep + MSS annonçait un SQN de
2,50 hors échantillon. Sur données réellement continues, ce SQN vaut 0,27. **47 % des transactions
traversaient une discontinuité artificielle du jeu de données et portaient la totalité du résultat.**

Aucune règle du protocole d'alors n'aurait permis de le détecter.

---

## Convention de statut

| Statut | Signification |
|---|---|
| **NORMATIF** | Règle méthodologique universelle. Verrouillable immédiatement. |
| **PARAMÈTRE À DÉCIDER** | Valeur ou choix technique dépendant du contexte. |
| **RECOMMANDATION** | Aide, non contraignante. |

L'essentiel de ce document est normatif : il ne s'agit pas de préférences mais de conditions de
validité d'un calcul.

---

# 1. Continuité temporelle

## 1.1 — Règle fondamentale — **NORMATIF**

> **Tout moteur qui accède aux barres par index doit vérifier la continuité temporelle de la série
> avant le parcours. À défaut, il doit parcourir par horodatage et s'arrêter à toute discontinuité
> non déclarée.**

**Pourquoi :** accéder à `bar[i+1]` en supposant qu'elle suit `bar[i]` dans le temps est une hypothèse
implicite. Elle n'est jamais énoncée, donc jamais vérifiée, et devient fausse dès qu'un jeu a été
filtré, extrait ou fusionné.

**Risque empêché :** une simulation qui traverse des sauts temporels invisibles, produisant des
résultats qui n'ont aucune contrepartie possible dans la réalité.

**Conséquence sur Sweep + MSS :** c'est la faille exacte. Le jeu de recherche était un extrait par
fenêtres — 60 barres avant chaque balayage, 300 après. Ce dimensionnement convenait aux versions à
cible fixe, dont la durée médiane de transaction était de 5 à 13 minutes. Le passage à un stop suiveur
a porté cette durée médiane à 174 minutes, avec un 90ᵉ centile à 567 minutes. Les transactions
dépassant leur fenêtre poursuivaient leur simulation sur les barres d'un autre balayage, parfois
plusieurs jours plus tard.

Cette règle aurait rendu l'erreur impossible.

## 1.2 — Contenu du contrôle — **NORMATIF**

Le contrôle de continuité doit produire, avant tout calcul :

```
Nombre de barres
Période couverte
Écarts entre barres consécutives > pas nominal
  · classification de chaque écart
  · nombre d'écarts non explicables par le calendrier de l'instrument
Verdict : SÉRIE CONTINUE | SÉRIE DISCONTINUE
```

**Une série déclarée DISCONTINUE ne peut être parcourue par index.** Aucune exception.

## 1.3 — Classification des interruptions — **NORMATIF pour le principe, PARAMÈTRE pour les seuils**

Les interruptions légitimes relèvent du calendrier de l'instrument, documenté dans son Asset Profile :
interruption quotidienne de cotation, fin de semaine, jours fériés.

Toute autre interruption est **suspecte** et doit être signalée nommément avec ses bornes.

**La classification est purement diagnostique** et ne doit jamais servir à une décision de trading.

**Paramètres à décider :** les seuils de durée séparant les catégories. Ils dépendent de l'instrument
et doivent figurer dans son Asset Profile, non dans ce document.

**Élément de repère :** sur les 593 fichiers Dukascopy NAS100 continus, une seule interruption suspecte
subsiste sur 8,3 ans. Sur le jeu extrait, il y en avait 383.

## 1.4 — Traversée d'une interruption légitime — **NORMATIF**

Une position ouverte peut traverser une interruption légitime — c'est le cas réel d'un week-end.
Le moteur doit alors :

1. reconnaître l'interruption comme légitime ;
2. modéliser l'écart de cotation à la réouverture, et non supposer une continuité de prix ;
3. enregistrer la traversée dans le journal de la transaction.

**Conséquence sur Sweep + MSS :** le moteur attribuait exactement −1,00 R dès que le stop était touché,
y compris lorsqu'une barre ouvrait très au-delà. Ce biais existe indépendamment de l'artefact
d'extraction et n'a jamais été corrigé.

---

# 2. Couverture

## 2.1 — Rapport obligatoire — **NORMATIF**

> **Aucun résultat quantitatif ne peut être présenté sans son rapport de couverture.**

Le rapport accompagne le résultat, dans le même livrable.

**Pourquoi :** un chiffre sans son périmètre de données est ininterprétable.

**Conséquence sur Sweep + MSS :** les rapports v1 et v3 ne portaient aucune information de couverture.
Le v1 reposait sur un jeu comportant six mois manquants en 2022 et quatre en 2026 — jamais détecté
avant le troisième rapport.

## 2.2 — Contenu minimal — **NORMATIF**

```
Source(s), nombre de fichiers
Instrument, granularité
Période couverte
Nombre de barres après déduplication
Nombre de doublons retirés
Nombre de jours cotés
Barres par jour : distribution, mois anormaux nommés
Interruptions : nombre par catégorie, suspectes listées
Verdict de continuité
Date de génération
```

## 2.3 — Vérification sur le contenu, jamais sur les noms — **NORMATIF**

> **La couverture se vérifie en lisant les données. Un inventaire fondé sur les noms de fichiers n'a
> aucune valeur probante.**

**Pourquoi :** un fichier peut exister, porter un nom couvrant une plage de dates, et ne contenir
qu'une fraction de cette plage — ou rien du tout.

**Conséquence sur Sweep + MSS :** une vérification par noms de fichiers a conclu « 0 jour ouvré
manquant » alors que six mois étaient absents. Les fichiers annuels issus de téléchargements
interrompus « couvraient » ces dates par leur nom tout en étant quasi vides. **Cette erreur de contrôle
a retardé la détection du problème de données de plusieurs jours.**

## 2.4 — Échecs silencieux d'acquisition — **NORMATIF**

Toute chaîne d'acquisition doit être considérée comme susceptible d'échouer sans le signaler.

Le contrôle de couverture est **le seul moyen de détection admis**. Un téléchargement qui se termine
sans message d'erreur ne constitue pas une preuve d'intégrité.

**Justification factuelle :** l'API Dukascopy renvoie une erreur 429 sans créer de fichier ; la boucle
d'appel poursuit son exécution et se termine normalement.

---

# 3. Transformation des données

## 3.1 — Toute transformation produit un nouveau jeu identifié — **NORMATIF**

> **Toute transformation d'un jeu validé — extraction, filtrage, agrégation, ré-échantillonnage,
> fusion, conversion de format — produit un nouveau jeu de données, portant son propre identifiant,
> son propre rapport de couverture et une déclaration explicite de ses limites d'usage.**

**Pourquoi :** un jeu validé en phase de contrôle qualité peut être remanié plus tard sans qu'aucun
contrôle ne se redéclenche. La validation initiale ne se transmet pas par héritage.

**Conséquence sur Sweep + MSS :** le fichier `nas-sweeps-v4.csv` était un extrait par fenêtres,
utilisable uniquement pour des transactions plus courtes que la fenêtre. **Cette limite d'usage
n'a jamais été écrite nulle part.** Elle n'existait que dans l'intention de celui qui a dimensionné la
fenêtre, et a été oubliée lors du changement de modèle de sortie.

Le même fichier a par ailleurs été converti au format MetaTrader 5 sous un autre nom, propageant
l'artefact à un environnement où il devenait encore moins détectable.

## 3.2 — Déclaration des limites d'usage — **NORMATIF**

Tout jeu transformé porte une déclaration explicite indiquant au minimum :

```
Jeu source           : identifiant
Transformation       : nature exacte, paramètres
Usages autorisés     : ...
Usages INTERDITS     : ...
Condition de validité: ...
Date, auteur
```

Exemple de ce qui aurait dû accompagner `nas-sweeps-v4.csv` :

```
Transformation        : extraction de fenêtres de −60 à +300 barres autour de chaque balayage
Usage autorisé        : détection de setups, simulation de transactions d'une durée
                        strictement inférieure à 220 barres après le MSS
Usage INTERDIT        : toute simulation dépassant la fenêtre ; tout parcours par index
                        au-delà de la fenêtre ; toute conversion vers une plateforme externe
Condition de validité : durée maximale de transaction < 220 barres
```

## 3.3 — Traçabilité de la chaîne — **NORMATIF**

Chaque jeu conserve la référence de son parent. La chaîne complète, de la source brute au jeu utilisé,
doit être reconstituable.

---

# 4. Conventions temporelles

## 4.1 — Convention unique par instrument — **NORMATIF**

Fuseau de référence, heure de bascule journalière et gestion du changement d'heure sont définis **une
fois** par instrument, dans son Asset Profile, et employés par tous les moteurs.

**Pourquoi :** le découpage journalier détermine les niveaux de référence. Une erreur de convention
déplace tous les signaux.

**Conséquence sur Sweep + MSS :** l'emploi de minuit UTC au lieu de 23 h Europe/Paris produisait 44
signaux nocturnes sur 59 — des artefacts purs, détectés par hasard en examinant la distribution
horaire.

## 4.2 — Stockage en temps universel — **NORMATIF**

Les horodatages sont stockés en UTC. La conversion vers un fuseau local n'intervient qu'à l'usage,
jamais au stockage.

## 4.3 — Vérification du changement d'heure — **NORMATIF**

Toute implémentation d'une conversion de fuseau doit être vérifiée sur les bascules d'heure d'été,
par comparaison entre au moins deux implémentations indépendantes.

**Conséquence sur Sweep + MSS :** cette vérification a été appliquée lors du portage — 390 cas testés,
dont les quinze bascules de 2019 à 2026, zéro divergence. **Elle a fonctionné.**

---

# 5. Parité entre implémentations

## 5.1 — Vérification préalable obligatoire — **NORMATIF**

> **Tout portage d'un moteur vers un autre langage ou environnement doit reproduire la référence à
> l'identique sur les mêmes données, avant toute expérience nouvelle.**

La tolérance admise doit être déclarée et justifiée. Une tolérance nulle est préférable lorsqu'elle
est atteignable.

**Pourquoi :** sans elle, une différence observée ne peut être attribuée ni aux données ni au code.

**Conséquence sur Sweep + MSS :** cette règle a été appliquée avant le test de reproduction. Le portage
JavaScript a reproduit le moteur Python sur douze métriques, sans tolérance. **C'est ce qui a permis
d'affirmer que la chute du SQN provenait des données et non du portage.** C'est le seul élément du
processus qui a fonctionné du premier coup.

## 5.2 — Contenu du rapport de parité — **NORMATIF**

Comparaison sur les mêmes données de : nombre de signaux détectés, nombre de transactions, taux de
réussite, espérance, profit factor, indicateur de qualité, drawdown, séries de pertes, et
horodatages des transactions lorsque disponibles.

Toute divergence doit être classée : défaut d'implémentation, différence de données, différence de
modèle d'exécution, ou limitation documentée et acceptée.

---

# 6. Format et unités

## 6.1 — Format canonique — **NORMATIF**

Un format unique de série de prix pour l'ensemble du projet : colonnes, ordre, unités et convention
d'horodatage fixés.

**Paramètre à décider :** le format lui-même.

## 6.2 — Absence de valeurs implicites — **NORMATIF**

Aucune valeur ne peut être déduite ou complétée silencieusement. Une donnée absente est absente et
doit apparaître comme telle dans le rapport de couverture.

---

# 7. Modèle de coûts

## 7.1 — Modèle unique par instrument — **NORMATIF**

Un modèle de coûts unique par instrument, défini dans l'Asset Profile, référencé par toutes les phases
de recherche, de validation et d'exécution.

**Pourquoi :** trois phases du plan maître mentionnent les coûts sans qu'un modèle commun soit imposé.
Rien n'empêche qu'une comparaison utilise un spread fixe et une autre un spread variable, rendant les
résultats incomparables.

## 7.2 — Expression relative des coûts — **NORMATIF**

Le spread et les coûts de transaction doivent être exprimés en pourcentage du prix, ou mesurés
historiquement, jamais figés en points sur une longue période.

**Justification :** un spread fixe en points sur un instrument passé de 6 608 à 30 000 représente un
coût relatif 4,5 fois plus élevé au début de la période qu'à la fin.

**Conséquence sur Sweep + MSS :** ce biais était présent dans tous les rapports. Le stop avait été
converti en pourcentage précisément pour cette raison ; **le spread est resté figé en points.**
L'incohérence n'a jamais été résolue.

## 7.3 — Composantes minimales — **NORMATIF pour la liste, À DÉCIDER pour les valeurs**

Spread, commission, glissement, financement le cas échéant, contraintes horaires d'exécution.

Le glissement doit être mesuré, non supposé nul. Lorsqu'il n'est pas mesuré, son absence doit être
déclarée comme limitation dans tout rapport.

---

# 8. Contrôle qualité en entrée

## 8.1 — Portée — **NORMATIF**

Le contrôle qualité s'applique à tout jeu entrant dans le projet, quelle que soit sa provenance, et
se redéclenche à chaque transformation (§3.1).

## 8.2 — Contrôles minimaux — **NORMATIF**

```
Doublons d'horodatage
Ordre chronologique
Cohérence OHLC : low ≤ min(open, close) ≤ max(open, close) ≤ high
Valeurs nulles, négatives ou aberrantes
Continuité temporelle (§1)
Couverture par mois (§2)
Cohérence entre sources lorsque plusieurs existent
```

## 8.3 — Divergence entre sources — **NORMATIF**

Lorsque deux sources divergent, le système ne choisit pas silencieusement. L'écart est enregistré, sa
cause analysée, et un niveau de confiance attribué au jeu retenu.

Cette exigence figure déjà au document `02`, section 6. Elle est reprise ici comme obligation
opératoire.

## 8.4 — Outillage — **NORMATIF**

Le contrôle qualité doit être **outillé et réutilisable**, non déclaratif. Un contrôle décrit dans un
document mais exécuté manuellement à chaque fois finira par être omis.

**Élément disponible :** le script `prepare.js` du dépôt `sweep-mss-nas100` constitue un prototype
fonctionnel produisant un rapport de couverture mois par mois.

---

# 9. Anti-look-ahead

## 9.1 — Principe — **NORMATIF**

Toute variable employée dans une décision doit être démontrablement disponible à l'instant de cette
décision.

## 9.2 — Contrôle programmatique — **NORMATIF**

Tout moteur de recherche doit intégrer une vérification automatique des index employés : aucun index
postérieur à l'instant de décision ne peut intervenir dans la construction du signal.

**Conséquence sur Sweep + MSS :** ce contrôle a été implémenté dans le script de reproduction et n'a
signalé aucune violation. **Le moteur ne souffrait d'aucun look-ahead** — l'échec était ailleurs, dans
les données. Cela illustre qu'un contrôle correct ne protège que de ce qu'il mesure.

---

# 10. Ce que ce document ne fixe pas

| Paramètre | Section |
|---|---|
| Seuils de classification des interruptions | 1.3 |
| Format canonique retenu | 6.1 |
| Valeurs des composantes de coûts | 7.3 |

Ces paramètres relèvent de l'Asset Profile de chaque instrument ou d'un choix technique à arbitrer.

---

# 11. Synthèse des règles normatives

| # | Règle | Aurait empêché l'échec Sweep + MSS |
|---|---|---|
| 1.1 | Continuité vérifiée avant parcours par index | **oui — directement** |
| 2.1 | Rapport de couverture joint à tout résultat | oui — détection plus précoce |
| 2.3 | Vérification sur le contenu, pas les noms | oui — détection plus précoce |
| 3.1 | Transformation = nouveau jeu identifié | **oui — directement** |
| 3.2 | Limites d'usage déclarées | **oui — directement** |
| 4.1 | Convention temporelle unique | oui — artefact des signaux nocturnes |
| 5.1 | Parité avant expérience | appliqué, a fonctionné |
| 7.2 | Coûts exprimés en relatif | non, mais biais présent |
| 9.2 | Contrôle anti-look-ahead | appliqué, a fonctionné |

**Trois règles auraient à elles seules rendu l'artefact impossible : 1.1, 3.1 et 3.2.**

---

# 12. Journal des versions

| Version | Date | Statut | Changement |
|---|---|---|---|
| 0.1 | 20/08/2026 | PROPOSITION | Rédaction initiale, soumise à arbitrage |
