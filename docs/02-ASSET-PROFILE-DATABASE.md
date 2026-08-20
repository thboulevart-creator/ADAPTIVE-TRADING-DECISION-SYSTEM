# Asset Profile Database — Édition Desk

**Version :** 1.0  
**Date :** 20 août 2026  
**Statut :** Cahier des charges fondateur

---

# 1. Objectif

L'Asset Profile Database est la base de connaissance structurée du comportement des actifs utilisés par l'Adaptive Trading Decision System.

Son objectif n'est pas de stocker quelques statistiques générales sur un actif. Elle doit permettre au système de répondre à une question fondamentale :

> **« Comment cet actif se comporte-t-il, dans quelles conditions, avec quels risques, quels coûts et quels experts sont historiquement adaptés à son comportement ? »**

Elle constitue une couche transversale utilisée par le moteur de contexte, le routeur, le moteur de risque, le portefeuille et l'exécution.

Elle ne décide pas directement de prendre un trade.

Elle fournit le contexte nécessaire pour qu'une décision puisse être prise rationnellement.

---

# 2. Principe fondamental

Un actif n'est pas seulement un symbole.

Par exemple :

```text
NAS100
```

ne signifie pas uniquement « indice technologique américain ».

Pour notre système, NAS100 doit être décrit par son comportement observable :

- volatilité ;
- amplitude intraday ;
- liquidité ;
- spread ;
- comportement par session ;
- comportement par régime ;
- réaction aux événements macro ;
- corrélations ;
- coûts ;
- stabilité ;
- compatibilité avec les différents experts.

L'Asset Profile Database transforme donc un actif en **profil quantifiable et exploitable**.

---

# 3. Architecture de la fiche actif

Chaque actif possède une fiche structurée.

```text
ASSET PROFILE
│
├── 01. Identité
├── 02. Données et qualité
├── 03. Microstructure
├── 04. Volatilité
├── 05. Comportement intraday
├── 06. Régimes
├── 07. Structure de prix
├── 08. Experts
├── 09. Multi-horizon
├── 10. Corrélations
├── 11. Facteurs macro
├── 12. Événements / news
├── 13. Exécution
├── 14. Risque
├── 15. Portefeuille
├── 16. Saisonnalité
├── 17. Stabilité
├── 18. Scores Desk
├── 19. Niveau de confiance
└── 20. Historique des mises à jour
```

---

# 4. Classification des paramètres

Tous les paramètres ne doivent pas être traités de la même manière.

Chaque donnée appartient à une des trois catégories suivantes.

## 4.1 Données lentes

Elles évoluent peu.

Exemples :

- classe d'actif ;
- marché de référence ;
- horaires structurels ;
- devise de cotation ;
- spécifications contractuelles ;
- nature de l'instrument.

Elles peuvent être révisées périodiquement.

## 4.2 Données intermédiaires

Elles évoluent progressivement.

Exemples :

- volatilité moyenne ;
- ATR moyen ;
- spread moyen ;
- liquidité ;
- corrélations ;
- performance des experts ;
- comportement par session.

Elles doivent être recalculées régulièrement.

## 4.3 Données dynamiques

Elles décrivent l'état récent du marché.

Exemples :

- volatilité actuelle ;
- spread actuel ;
- régime actuel ;
- volume relatif ;
- corrélations récentes ;
- stress actuel ;
- conditions d'exécution actuelles.

Elles doivent pouvoir être actualisées fréquemment.

---

# 5. Identité de l'actif

Chaque fiche doit commencer par une identité claire.

Paramètres minimum :

| Paramètre | Description |
|---|---|
| Asset ID | Identifiant interne unique |
| Nom | Nom de l'actif |
| Symbole | Symbole utilisé par la source |
| Classe | Forex / indice / métal / crypto / etc. |
| Sous-classe | Exemple : indice actions US |
| Marché | Marché de référence |
| Devise | Devise de cotation |
| Type d'instrument | Spot / CFD / future / autre |
| Source principale | Source de données utilisée |
| Source secondaire | Source de contrôle éventuelle |
| Timezone | Référence temporelle |
| Date de création | Date d'intégration |
| Statut | Actif / surveillé / suspendu |

---

# 6. Qualité des données

La qualité du profil dépend directement de la qualité des données.

Paramètres :

- profondeur historique disponible ;
- granularité disponible ;
- continuité des données ;
- trous de données ;
- anomalies détectées ;
- qualité OHLC ;
- qualité volume ;
- qualité spread ;
- synchronisation temporelle ;
- cohérence entre sources.

### Exemple

Deux sources donnent un historique NAS100 différent.

Le système ne doit pas choisir silencieusement une version.

Il doit enregistrer :

```text
Source A → utilisée
Source B → contrôle
Écart détecté → oui
Cause → à analyser
Confiance → moyenne
```

---

# 7. Microstructure

La microstructure décrit la manière dont l'actif se négocie réellement.

Paramètres principaux :

- spread moyen ;
- spread médian ;
- spread par session ;
- spread pendant les news ;
- volume moyen ;
- volume relatif ;
- liquidité ;
- profondeur si disponible ;
- slippage moyen ;
- slippage par taille ;
- fréquence des gaps ;
- coût d'entrée ;
- coût de sortie.

### Exemple

Un actif peut être très rentable en backtest mais présenter un spread élevé pendant la session où le signal apparaît.

L'Asset Profile doit permettre au système de le savoir avant d'attribuer une taille importante.

---

# 8. Volatilité

La volatilité doit être mesurée sous plusieurs formes.

Paramètres :

- ATR ;
- ATR relatif au prix ;
- volatilité réalisée ;
- volatilité par horizon ;
- volatilité intraday ;
- volatilité par session ;
- volatilité conditionnelle ;
- fréquence des expansions ;
- fréquence des compressions ;
- volatilité extrême ;
- percentile de volatilité.

Exemple :

```text
Volatilité actuelle : 82e percentile

Interprétation :
conditions nettement plus volatiles que la normale historique.
```

Cette information peut modifier le sizing et le choix de l'expert.

---

# 9. Comportement intraday

Le profil doit identifier les périodes où l'actif présente historiquement des comportements différents.

Paramètres :

- rendement moyen par heure ;
- volatilité par heure ;
- volume par heure ;
- range par heure ;
- fréquence des breakouts ;
- fréquence des retournements ;
- comportement à l'ouverture ;
- comportement à la clôture ;
- comportement par session ;
- comportement autour des transitions de session.

Sessions possibles selon l'actif :

- Asie ;
- Londres ;
- New York ;
- overlap Londres/New York ;
- session spécifique au marché.

---

# 10. Structure de prix

Le profil doit mesurer les caractéristiques structurelles du prix.

Paramètres possibles :

- tendance moyenne ;
- persistance des mouvements ;
- longueur moyenne des tendances ;
- fréquence des retournements ;
- amplitude des swings ;
- distance moyenne entre extrêmes ;
- fréquence des gaps ;
- fréquence des fausses cassures ;
- fréquence des cassures suivies de continuation ;
- fréquence des cassures suivies de réintégration.

---

# 11. Régimes de marché

Le profil doit décrire le comportement de l'actif selon plusieurs régimes.

Minimum V1 :

```text
TENDANCE
RANGE
COMPRESSION
BREAKOUT
EXPANSION
STRESS
TRANSITION
```

Pour chaque régime, on cherche notamment :

- fréquence ;
- durée moyenne ;
- volatilité ;
- rendement moyen ;
- amplitude ;
- comportement des experts ;
- risque de retournement ;
- coûts d'exécution.

### Exemple NAS100

```text
Régime : Tendance + volatilité élevée

Momentum       → favorable
Breakout       → favorable
Mean Reversion → défavorable
```

Le routeur peut utiliser cette information pour orienter les experts.

---

# 12. Transitions de régime

Le régime actuel est important, mais le passage d'un régime à un autre l'est souvent davantage.

Le profil doit donc mesurer :

- Range → Breakout ;
- Compression → Expansion ;
- Tendance → Range ;
- Tendance → Stress ;
- Stress → Normalisation ;
- Range → Tendance.

### Exemple

```text
Compression
     ↓
Expansion
     ↓
Breakout
```

Un actif peut avoir un comportement particulièrement favorable au moment de cette transition.

---

# 13. Performance des experts

Chaque actif doit disposer d'un historique de performance par expert.

Structure minimale :

| Actif | Expert | Régime | Horizon | Trades | Expectancy | Drawdown | Stabilité |
|---|---|---|---|---:|---:|---:|---|
| NAS100 | Momentum | Tendance | 1h | ... | ... | ... | ... |
| NAS100 | Breakout | Breakout | 15m | ... | ... | ... | ... |
| NAS100 | Mean Reversion | Range | 1h | ... | ... | ... | ... |

Il ne suffit donc pas de dire :

> « Momentum fonctionne. »

Il faut pouvoir dire :

> « Momentum fonctionne sur cet actif, dans ce régime et sur cet horizon, avec telle stabilité. »

---

# 14. Analyse multi-horizon

Chaque actif doit être analysé sur plusieurs horizons.

V1 :

- 15 minutes ;
- 1 heure ;
- 4 heures.

Pour chaque horizon :

- volatilité ;
- tendance ;
- range ;
- momentum ;
- mean reversion ;
- breakout ;
- performance des experts ;
- drawdown ;
- stabilité.

### Exemple

```text
NAS100

15m → Breakout favorable
1h  → Momentum favorable
4h  → Tendance neutre
```

Le système possède alors une vision hiérarchique du contexte.

---

# 15. Corrélations

L'actif ne doit pas être étudié isolément.

Le profil doit suivre les corrélations pertinentes avec :

- indices ;
- devises ;
- matières premières ;
- taux ;
- volatilité ;
- crypto ;
- facteurs macro pertinents.

Exemples :

```text
NAS100 ↔ DXY
NAS100 ↔ US10Y
NAS100 ↔ VIX
Gold   ↔ DXY
Gold   ↔ US10Y
BTC    ↔ NAS100
EURUSD ↔ DXY
```

Les corrélations doivent être mesurées sur plusieurs fenêtres et non sur une seule période.

---

# 16. Facteurs macro

Selon la classe d'actif, le profil peut inclure les facteurs macro pertinents.

Exemples :

- DXY ;
- VIX ;
- taux américains ;
- inflation ;
- décisions de banques centrales ;
- emploi ;
- croissance ;
- liquidité globale ;
- conditions financières.

Le profil ne doit pas prétendre établir une causalité simplement parce qu'une corrélation existe.

Il doit distinguer :

```text
Relation observée
≠
Causalité démontrée
```

---

# 17. Événements et news

Le profil doit identifier la sensibilité de l'actif aux événements importants.

Paramètres :

- sensibilité aux annonces macro ;
- élargissement du spread ;
- variation de volatilité ;
- slippage autour des news ;
- comportement avant l'annonce ;
- comportement après l'annonce ;
- fréquence des mouvements extrêmes.

### Exemple

Si le NAS100 présente régulièrement une forte expansion de volatilité lors du CPI :

```text
CPI
 ↓
Volatilité ↑
Spread ↑
Slippage ↑
```

Le système doit intégrer ces éléments dans le filtre d'exécution et le moteur de risque.

---

# 18. Exécution

Le profil doit permettre d'estimer si un signal peut être exécuté économiquement.

Paramètres :

- spread normal ;
- spread extrême ;
- slippage moyen ;
- slippage percentile ;
- coût total moyen ;
- coût par session ;
- coût autour des news ;
- liquidité minimale ;
- taille maximale recommandée si estimable.

### Règle

Si :

```text
Alpha attendu ≤ coût total estimé
```

alors l'opportunité doit être considérée comme économiquement insuffisante.

---

# 19. Risque spécifique à l'actif

Chaque actif doit disposer d'une description de ses risques particuliers.

Exemples :

- gaps ;
- volatilité extrême ;
- liquidité insuffisante ;
- spread variable ;
- corrélation cachée ;
- exposition macro ;
- risque overnight ;
- risque de financement ;
- risque de marché spécifique.

---

# 20. Saisonnalité

La saisonnalité ne doit jamais être considérée automatiquement comme un signal de trading.

Elle constitue une information contextuelle.

Paramètres possibles :

- jour de semaine ;
- mois ;
- trimestre ;
- heure ;
- session ;
- périodes particulières ;
- anomalies calendaires.

Une saisonnalité n'est retenue que si elle présente une robustesse statistique suffisante.

---

# 21. Stabilité

Une caractéristique intéressante doit être testée dans le temps.

Le profil doit permettre de comparer :

- périodes anciennes ;
- périodes récentes ;
- différents régimes ;
- différents sous-échantillons ;
- différents horizons.

Exemple :

```text
2019–2021 → favorable
2022–2024 → favorable
2025–2026 → favorable

Conclusion provisoire : caractéristique relativement stable
```

À l'inverse :

```text
2019–2024 → favorable
2025–2026 → fortement dégradée
```

La caractéristique doit être considérée comme potentiellement instable.

---

# 22. Scores Desk

L'Asset Profile Database peut produire plusieurs scores synthétiques.

Ces scores ne remplacent jamais les données brutes.

## 22.1 Score de qualité des données

Évalue :

- profondeur historique ;
- continuité ;
- cohérence ;
- qualité des timestamps ;
- qualité des données de marché.

## 22.2 Score de tradabilité

Évalue :

- liquidité ;
- spread ;
- slippage ;
- coûts ;
- stabilité d'exécution.

## 22.3 Score de stabilité

Évalue la stabilité des caractéristiques observées.

## 22.4 Score de diversité

Mesure si l'actif apporte un comportement suffisamment différent des actifs déjà présents.

## 22.5 Score expert

Mesure l'adéquation historique avec chaque expert.

Exemple :

```text
NAS100

Momentum       86/100
Breakout       82/100
Mean Reversion 54/100
```

Ces scores sont des outils de synthèse, pas des décisions automatiques.

---

# 23. Niveau de confiance

Chaque caractéristique importante doit avoir un niveau de confiance.

Exemple :

```text
Paramètre : Spread moyen
Valeur    : 1,2
Échantillon : élevé
Stabilité : élevée
Confiance : élevée
```

Autre exemple :

```text
Paramètre : comportement pendant une condition rare
Échantillon : faible
Stabilité : inconnue
Confiance : faible
```

Une information peu fiable ne doit pas être traitée comme une vérité.

---

# 24. Provenance des données

Chaque donnée importante doit pouvoir être reliée à sa provenance.

Minimum :

- source ;
- période ;
- date de calcul ;
- méthode de calcul ;
- version de la méthode ;
- taille de l'échantillon ;
- niveau de confiance.

Objectif : rendre le profil **auditable et reproductible**.

---

# 25. Mise à jour

La base ne doit pas être modifiée de manière anarchique.

Principe :

```text
Nouvelle donnée
 ↓
Calcul
 ↓
Contrôle qualité
 ↓
Comparaison avec l'ancien profil
 ↓
Validation
 ↓
Nouvelle version du profil
```

Chaque modification importante doit être historisée.

---

# 26. Historique des profils

Une fiche actif doit pouvoir répondre à :

> « Que pensions-nous de cet actif à telle date ? »

Exemple :

```text
NAS100 Profile v1.0
20/08/2026

NAS100 Profile v1.1
20/09/2026

NAS100 Profile v1.2
20/10/2026
```

Les anciennes versions ne doivent pas être écrasées sans traçabilité.

---

# 27. Exemple simplifié — NAS100

```text
ACTIF
NAS100

CLASSE
Indice actions US

VOLATILITÉ
Élevée

LIQUIDITÉ
Élevée pendant les principales sessions

EXPERTS FAVORABLES
Momentum
Breakout

EXPERT MOINS ADAPTÉ
Mean Reversion en tendance forte

RÉGIMES FAVORABLES
Tendance
Breakout
Expansion

FACTEURS À SURVEILLER
DXY
US10Y
VIX
News macro US

RISQUES
Volatilité extrême
News
Slippage lors des annonces

CONFIANCE
À déterminer après étude complète
```

Cet exemple est uniquement illustratif. Les valeurs réelles devront être calculées à partir des données.

---

# 28. Exemple simplifié — Gold

```text
ACTIF
Gold / XAUUSD

CLASSE
Métaux précieux

CARACTÉRISTIQUES À ÉTUDIER
Volatilité
DXY
Taux réels / taux US
Sessions Londres / New York
News macro

EXPERTS À TESTER
Momentum
Breakout
Mean Reversion

RISQUES
Volatilité autour des annonces
Variations rapides
Spread / slippage selon session
```

Aucune conclusion de trading ne doit être inscrite avant analyse empirique.

---

# 29. Exemple simplifié — EURUSD

```text
ACTIF
EURUSD

CLASSE
Forex majeur

CARACTÉRISTIQUES À ÉTUDIER
Liquidité
Sessions Londres / New York
DXY
Volatilité intraday
Réactions aux annonces BCE / Fed / inflation / emploi

EXPERTS À TESTER
Mean Reversion
Momentum
Breakout

RISQUES
News
Compression prolongée
Faux breakouts
```

---

# 30. Exemple simplifié — BTC

```text
ACTIF
BTCUSD

CLASSE
Crypto

CARACTÉRISTIQUES À ÉTUDIER
Volatilité 24/7
Liquidité par heure
Funding
Open interest
Structure des dérivés
Corrélation avec actifs risqués

EXPERTS À TESTER
Momentum
Breakout
Mean Reversion

RISQUES
Volatilité extrême
Liquidations
Gaps sur certains marchés dérivés
Risque de week-end
Funding
```

---

# 31. Ce que la base ne doit PAS faire

L'Asset Profile Database ne doit pas devenir :

- un système de signal automatique ;
- une stratégie de trading déguisée ;
- un score magique donnant directement LONG/SHORT ;
- une collection de milliers de variables inutilisées ;
- une base impossible à maintenir ;
- une source de sur-optimisation.

Son rôle est de fournir une **connaissance structurée et exploitable**.

---

# 32. Architecture cible de stockage

La structure technique exacte pourra évoluer.

La logique cible est :

```text
asset_profiles/
│
├── NAS100/
│   ├── identity
│   ├── data_quality
│   ├── microstructure
│   ├── volatility
│   ├── intraday
│   ├── regimes
│   ├── experts
│   ├── correlations
│   ├── macro
│   ├── execution
│   ├── risk
│   └── history
│
├── GOLD/
│   └── ...
│
├── EURUSD/
│   └── ...
│
└── BTCUSD/
    └── ...
```

Cette structure est conceptuelle à ce stade.

Le format de stockage final sera choisi en fonction des besoins du moteur.

---

# 33. Priorité V1

Nous ne devons pas chercher à mesurer immédiatement tout ce qui est imaginable.

Priorité initiale :

### Niveau 1 — indispensable

- identité ;
- source de données ;
- qualité des données ;
- volatilité ;
- liquidité ;
- spread ;
- slippage ;
- sessions ;
- régimes ;
- corrélations principales ;
- comportement des experts ;
- coûts.

### Niveau 2 — important

- saisonnalité ;
- facteurs macro ;
- transitions de régime ;
- sensibilité aux news ;
- stabilité ;
- score de tradabilité.

### Niveau 3 — avancé

- microstructure détaillée ;
- données de carnet ;
- dérivés ;
- funding ;
- open interest ;
- modèles de liquidité avancés ;
- relations multi-actifs complexes.

---

# 34. Règle de conception

Chaque paramètre ajouté à l'Asset Profile Database doit répondre à trois questions :

1. **Que mesure-t-il ?**
2. **À quelle décision du système sert-il ?**
3. **Comment vérifie-t-on qu'il apporte réellement de la valeur ?**

Si aucune réponse claire n'existe, le paramètre n'est pas prioritaire.

---

# 35. Philosophie Desk

L'Asset Profile Database doit permettre à un trader, un chercheur ou un moteur de décision de comprendre rapidement :

> **« Quel type d'actif est-ce, comment se comporte-t-il, quand fonctionne-t-il, quand ne fonctionne-t-il pas, combien coûte son trading et quelle place peut-il raisonnablement occuper dans notre système ? »**

La base doit donc privilégier :

**Qualité > quantité**

**Mesure > intuition**

**Historique > anecdote**

**Stabilité > performance ponctuelle**

**Contexte > signal isolé**

**Traçabilité > mémoire informelle**

---

# 36. Définition finale

> **L'Asset Profile Database est la mémoire structurée, versionnée et auditable du comportement des actifs utilisés par l'Adaptive Trading Decision System. Elle décrit leur identité, leurs données, leur microstructure, leur volatilité, leurs comportements intraday, leurs régimes, leurs corrélations, leurs facteurs de risque, leurs coûts d'exécution et leur compatibilité avec les différents experts, afin d'alimenter rationnellement les couches de contexte, de routage, de risque, de portefeuille et d'exécution.**
