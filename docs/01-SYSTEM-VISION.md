# Adaptive Trading Decision System — Vision du système

**Version :** 1.0  
**Date :** 20 août 2026  
**Statut :** Document fondateur

---

# 1. Vision

L'objectif de ce projet n'est pas de construire une IA capable de prédire parfaitement la prochaine bougie.

L'objectif est de construire un :

> **Système de décision adaptatif où la prédiction n'est qu'une composante de la décision finale.**

Le système doit être capable de déterminer :

1. Dans quel contexte de marché nous nous trouvons.
2. Quels comportements historiques sont pertinents dans ce contexte.
3. Quel expert est adapté à la situation.
4. Sur quel horizon l'opportunité existe.
5. Quelle exposition est rationnelle.
6. Quels risques doivent réduire ou empêcher une position.
7. Si les coûts d'exécution permettent encore de conserver un avantage statistique.
8. Pourquoi une décision a gagné ou perdu.
9. Si le comportement du système est en train de se dégrader.
10. Si une nouvelle version mérite d'être testée.

Le système doit donc être **adaptatif**, mais il ne doit pas être autorisé à se réentraîner librement en production.

---

# 2. Principe fondamental : adaptation contrôlée

Nous ne voulons pas construire un système fonctionnant selon :

```text
Perte
 ↓
Réentraînement automatique
 ↓
Nouveau modèle
 ↓
Production immédiate
```

Cette logique peut provoquer un surapprentissage du bruit récent.

Notre cycle de fonctionnement est donc :

```text
PRODUCTION
 ↓
Collecte des trades
 ↓
Attribution de la performance
 ↓
Surveillance des changements de régime
 ↓
Proposition d'un nouveau modèle
 ↓
Validation hors échantillon
 ↓
Walk-Forward
 ↓
Tests avec coûts réels
 ↓
Comparaison Champion / Challenger
 ↓
Critères de promotion
 ↓
PROMOTION ou REJET
 ↓
PRODUCTION
```

La production reste stable.

L'évolution du système est contrôlée.

---

# 3. Architecture générale

```text
                         DONNÉES DE MARCHÉ
                                │
                                ▼
                         ┌──────────────┐
                         │ DATA ENGINE  │
                         └──────┬───────┘
                                │
                                ▼
                 ┌──────────────────────────┐
                 │ ASSET PROFILE DATABASE   │
                 │                          │
                 │ Mémoire structurée du    │
                 │ comportement des actifs  │
                 └────────────┬─────────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │ CONTEXT ENGINE│
                       └──────┬───────┘
                              │
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
             MOMENTUM    MEAN REVERSION  BREAKOUT
                 │            │            │
                 └────────────┼────────────┘
                              ▼
                       EXPERT ROUTER
                              │
                              ▼
                       MULTI-HORIZON
                        15m / 1h / 4h
                              │
                              ▼
                         RISK ENGINE
                              │
                              ▼
                      PORTFOLIO ENGINE
                              │
                              ▼
                      EXECUTION ENGINE
                              │
                              ▼
                           TRADE
                              │
                              ▼
                    DONNÉES DE PERFORMANCE
                              │
                              ▼
                         SURVEILLANCE
                              │
                              ▼
                    CHAMPION / CHALLENGER
                              │
                              └──────► ÉVOLUTION CONTRÔLÉE
```

---

# 4. Asset Profile Database

L'Asset Profile Database est une **couche de connaissance transversale** du système.

Elle constitue la mémoire structurée du comportement de chaque actif.

Elle peut contenir notamment :

- volatilité ;
- liquidité ;
- spreads ;
- coûts d'exécution ;
- sessions de marché ;
- corrélations ;
- comportement par régime ;
- comportement intraday ;
- performance des différents experts ;
- stabilité historique ;
- relations avec d'autres actifs.

Elle alimente plusieurs couches :

```text
              ASSET PROFILE DATABASE
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       CONTEXT       ROUTER        RISK
          │            │            │
          └────────────┼────────────┘
                       ▼
                  PORTFOLIO
                       │
                       ▼
                  EXECUTION
```

Son fonctionnement détaillé est documenté dans :

`docs/02-ASSET-PROFILE-DATABASE.md`

---

# 5. Context Engine — Comprendre le marché

Le Context Engine répond d'abord à :

> **« Que se passe-t-il actuellement sur le marché ? »**

Il identifie notamment :

- tendance ;
- range ;
- compression ;
- breakout ;
- volatilité faible ;
- volatilité normale ;
- volatilité extrême ;
- stress ;
- conditions de liquidité.

### Exemple

Imaginons le NAS100.

Le système constate :

- tendance haussière ;
- compression préalable ;
- volatilité en expansion ;
- cassure d'une zone importante.

Il ne dit pas encore :

> « Achète le NAS100. »

Il dit :

> **« Le marché présente actuellement un contexte de breakout avec expansion de volatilité. »**

---

# 6. Experts

Chaque expert possède un mandat spécifique.

### Momentum

Cherche la continuation d'un mouvement existant.

### Mean Reversion

Cherche les situations où le prix a tendance à revenir vers une zone de référence.

### Breakout

Cherche les transitions entre compression et expansion.

D'autres experts pourront être ajoutés plus tard :

- volatilité ;
- microstructure ;
- anomalies ;
- risque de crash ;
- dérivés ;
- funding crypto ;
- exécution.

---

# 7. Expert Router

Le routeur répond à :

> **« Quel expert est le plus adapté au contexte actuel ? »**

Dans la première version, le routeur sera basé sur des règles explicables.

### Exemple

Marché :

```text
Tendance forte
+
Volatilité normale
```

Pondération possible :

```text
Momentum          60 %
Breakout          30 %
Mean Reversion    10 %
```

Autre contexte :

```text
Range
+
Volatilité faible
```

Pondération possible :

```text
Momentum          10 %
Breakout          10 %
Mean Reversion    80 %
```

Ces pondérations devront être déterminées et validées par les données.

---

# 8. Analyse multi-horizon

Version initiale :

- 15 minutes ;
- 1 heure ;
- 4 heures.

### Exemple NAS100

```text
15 min → Momentum positif
1 h    → Momentum fortement positif
4 h    → Contexte légèrement négatif
```

Le système peut alors réduire l'exposition plutôt que prendre une décision binaire.

---

# 9. Risk Engine

Le Risk Engine répond à :

> **« Quelle exposition est rationnelle compte tenu de l'opportunité et du risque ? »**

Il prend notamment en compte :

- rendement attendu ;
- volatilité anticipée ;
- incertitude ;
- drawdown ;
- corrélations ;
- concentration ;
- liquidité ;
- coûts.

### Exemple

Un signal NAS100 est excellent.

Mais le portefeuille possède déjà plusieurs positions fortement corrélées au Nasdaq.

Le Risk Engine peut réduire la taille du NAS100.

---

# 10. Portfolio Engine

Le système ne doit pas analyser chaque trade indépendamment.

### Exemple

```text
NAS100 → Momentum → fort
Gold   → Breakout → fort
EURUSD → Mean Reversion → moyen
BTC    → Breakout → très fort
```

Le Portfolio Engine vérifie :

- corrélations ;
- facteurs communs ;
- concentration ;
- exposition existante ;
- volatilité.

Il peut finalement décider :

```text
NAS100 → 1.0R
Gold   → 0.8R
EURUSD → 0R
BTC    → 0.5R
```

La force du signal individuel ne suffit donc pas à déterminer l'allocation.

---

# 11. Execution Engine

Une prédiction statistiquement correcte peut devenir économiquement inutile après :

- spread ;
- commission ;
- slippage ;
- liquidité ;
- impact de marché.

### Exemple

```text
Avantage attendu : +0,20 %
Coûts estimés    : +0,23 %
```

Décision :

> **PAS DE TRADE**

---

# 12. Production

La décision finale suit :

```text
DONNÉES
 ↓
CONTEXTE
 ↓
EXPERT
 ↓
HORIZON
 ↓
RISQUE
 ↓
PORTEFEUILLE
 ↓
EXÉCUTION
 ↓
DÉCISION
```

La décision peut être :

- LONG ;
- SHORT ;
- exposition réduite ;
- exposition normale ;
- PAS DE TRADE.

**Ne pas trader est une décision valide.**

---

# 13. Collecte et attribution

Chaque décision doit permettre de reconstruire :

> **Pourquoi cette décision a-t-elle été prise ?**

Exemple :

```text
Actif       : NAS100
Régime      : Tendance / forte volatilité
Expert      : Momentum
Horizon     : 1h
Signal      : +0,68
Taille      : 0,75R
Spread      : enregistré
Slippage    : enregistré
Résultat    : +1,4R
```

Nous voulons connaître non seulement le résultat, mais **la cause de la performance**.

---

# 14. Détection de changement de régime

Exemple :

Historique :

```text
Momentum + Tendance = très performant
```

Puis :

```text
Momentum + Tendance = performance en baisse
```

Le système ne modifie pas automatiquement le modèle.

Il déclenche :

> **« Dégradation potentielle détectée. »**

Une analyse contrôlée peut alors commencer.

---

# 15. Champion / Challenger

Le modèle actuellement en production est le :

> **Champion**

Une nouvelle version proposée est le :

> **Challenger**

Exemple :

```text
Champion
Momentum V1

vs

Challenger
Momentum V2
```

Le Challenger reste hors production tant qu'il n'a pas passé les validations.

---

# 16. Validation et Walk-Forward

Le Challenger doit être évalué sur des données qu'il n'a pas utilisées pour sa construction.

Le Walk-Forward simule progressivement les conditions réelles :

```text
APPRENTISSAGE → TEST
       ↓
    déplacement
       ↓
APPRENTISSAGE → TEST
       ↓
    déplacement
       ↓
APPRENTISSAGE → TEST
```

Les tests doivent intégrer autant que possible :

- spread ;
- commissions ;
- slippage ;
- financement ;
- contraintes d'exécution.

---

# 17. Champion contre Challenger

La comparaison doit prendre en compte :

- rendement ;
- Sharpe ;
- Sortino ;
- drawdown maximal ;
- stabilité ;
- profit factor ;
- nombre de trades ;
- performance par régime ;
- performance par actif ;
- sensibilité aux coûts ;
- robustesse Walk-Forward.

Le rendement seul ne suffit pas.

---

# 18. Promotion ou rejet

Le Challenger ne devient Champion que si des critères définis à l'avance sont satisfaits.

```text
CHALLENGER
    │
    ├── Robustesse
    ├── Performance hors échantillon
    ├── Walk-Forward
    ├── Coûts réels
    ├── Drawdown
    ├── Stabilité
    └── Absence de faiblesse critique
             │
             ▼
       PROMOTION / REJET
```

Un meilleur backtest ne suffit pas.

---

# 19. Ce que nous ne voulons pas construire

Le projet exclut volontairement :

- un oracle prédictif ;
- un modèle unique opaque ;
- un système qui s'autoréentraîne librement ;
- une optimisation après chaque perte ;
- une dépendance à un seul backtest ;
- un système ignorant les coûts ;
- un système obligé de prendre des trades ;
- une complexité sans amélioration mesurable.

---

# 20. Socle V1

La première version sera volontairement simple :

```text
DATA
 ↓
DÉTECTION DE RÉGIME
 ↓
3 EXPERTS
 ├── Momentum
 ├── Mean Reversion
 └── Breakout
 ↓
ROUTEUR À RÈGLES
 ↓
MULTI-HORIZON
 ├── 15m
 ├── 1h
 └── 4h
 ↓
RISK ENGINE
 ↓
PORTFOLIO ENGINE
 ↓
FILTRE D'EXÉCUTION
 ↓
PRODUCTION
 ↓
ATTRIBUTION
 ↓
SURVEILLANCE
 ↓
CHALLENGER
 ↓
VALIDATION
 ↓
CHAMPION / CHALLENGER
```

V1 doit être :

**Compréhensible.**

**Mesurable.**

**Testable.**

**Reproductible.**

**Modulaire.**

**Robuste.**

---

# 21. Évolution future

Après validation du socle :

- routeur appris ;
- nouveaux experts ;
- backbone multi-actifs ;
- mesure de l'incertitude ;
- allocation adaptative ;
- intelligence d'exécution.

Exemple de backbone :

```text
NAS100
Gold
DXY
US10Y
VIX
EURUSD
BTC
```

L'objectif est de comprendre les interactions entre marchés et non de considérer chaque actif isolément.

---

# 22. Philosophie

Nous ne cherchons pas à prédire parfaitement le marché.

Nous cherchons à **prendre de meilleures décisions dans un environnement incertain**.

Un système peut avoir des prédictions imparfaites et rester performant s'il sait :

- sélectionner les bons contextes ;
- utiliser les bons experts ;
- contrôler son exposition ;
- gérer les corrélations ;
- contrôler les coûts ;
- éviter les mauvaises opportunités ;
- détecter sa dégradation ;
- tester ses évolutions ;
- rejeter les modèles fragiles.

> **La prédiction est une composante du système. Elle n'est pas le système.**

---

# 23. Règle d'or

Toute nouvelle technologie, donnée, fonctionnalité ou modèle doit répondre à deux questions :

> **Où cette fonctionnalité s'intègre-t-elle dans l'architecture ?**

> **Quel problème mesurable résout-elle ?**

Si la réponse n'est pas claire, elle n'est pas prioritaire.

Nos priorités :

**Robustesse > sophistication**

**Validation > intuition**

**Explicabilité > opacité**

**Coûts réels > performance théorique**

**Contrôle > autonomie**

**Qualité de décision > précision prédictive**

**Survie > performance théorique**

---

# 24. Définition finale

L'Adaptive Trading Decision System est :

> **Un système de décision adaptatif, multi-actifs et multi-horizons composé d'un moteur de contexte, d'experts spécialisés, d'un routeur, d'un moteur de risque, d'une couche portefeuille et d'une couche d'exécution, dont l'évolution est contrôlée par un processus Champion / Challenger et validée hors échantillon avant toute promotion en production.**
