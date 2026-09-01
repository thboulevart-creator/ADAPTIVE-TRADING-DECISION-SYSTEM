# PRINCIPES TRANSVERSAUX — ALGORITHMES

> Document de référence vivant — ALGO ECOSYSTEM
>
> Ce document centralise les principes, hypothèses et idées transversales qui doivent être conservés jusqu'au moment où ils deviennent utiles dans la conception, la validation ou la gestion du système.

## Règle de gouvernance du document

Une idée enregistrée ici n'est pas automatiquement une vérité validée. Chaque entrée doit conserver son statut :

- **HYPOTHÈSE** — idée à tester ;
- **PRINCIPE DE CONCEPTION** — règle retenue pour guider la conception, encore susceptible d'être invalidée ;
- **INVARIANT VALIDÉ** — règle soutenue par des preuves suffisantes.

---

## PTA-001 — Risque borné, rendement non prédéterminé

**Statut : PRINCIPE DE CONCEPTION**

Le risque est une contrainte connue ; le rendement est une conséquence inconnue.

Lorsqu'un algorithme est créé, nous devons pouvoir déterminer à l'avance combien nous sommes capables de perdre sur une période donnée, notamment sur une journée. En revanche, nous ne devons pas chercher à déterminer à l'avance combien l'algorithme doit gagner.

La performance doit être laissée à la qualité des configurations et à la gestion de position. Il ne faut pas concevoir l'algo autour d'un ratio fixe du type « risque 1 pour gagner 2 » ou « risque 1 pour gagner 3 » comme objectif structurel.

La performance doit notamment pouvoir être exprimée sous la forme :

> « J'ai fait +3 % cette semaine pour tel niveau de risque. »

et non comme une promesse de rendement fixe associée à un ratio prédéterminé.

**Principe directeur :** borner la perte sans borner artificiellement le potentiel de gain.

---

## PTA-002 — La gestion de position est un moteur de performance

**Statut : HYPOTHÈSE / PRINCIPE DE CONCEPTION À VALIDER PAR LES DONNÉES**

La gestion de position peut faire une différence majeure dans la performance finale d'un algorithme.

Une position favorable doit pouvoir produire un gain potentiellement largement supérieur au risque initial lorsque le marché offre un mouvement exploitable. Un Take Profit fixe peut, selon la stratégie, limiter le potentiel d'un mouvement exceptionnel ; une gestion adaptative peut permettre de laisser courir davantage les gagnants.

Toute structure de sortie doit toutefois être démontrée par les données et ne doit pas être présumée supérieure simplement parce qu'elle permet théoriquement des gains plus importants.

---

## PTA-003 — Sélectivité conditionnelle du portefeuille

**Statut : PRINCIPE DE CONCEPTION**

Lorsque le régime de marché ne correspond pas aux conditions de validité d'un algorithme, celui-ci doit réduire fortement ou interrompre sa prise de position.

Lorsque le régime de marché correspond à son avantage statistique démontré, l'algorithme peut augmenter son activité et exploiter ses configurations avec une asymétrie favorable — notamment un Stop Loss relativement court et un potentiel de profit significativement plus large — lorsque cette structure est validée par les données.

À l'échelle du portefeuille, l'objectif n'est donc pas de maintenir un nombre constant de trades, mais de combiner plusieurs algorithmes présentant des régimes de performance, des forces, des faiblesses et des périodes de drawdown suffisamment différents afin de réduire la dépendance du portefeuille à un unique comportement du marché.

---

## PTA-004 — L'inactivité est une décision valide

**Statut : PRINCIPE DE CONCEPTION**

Un portefeuille robuste doit accepter de ne presque rien faire lorsque son avantage agrégé n'est pas présent.

Logique cible :

- marché défavorable à A → A reste inactif ;
- marché favorable à B → B travaille ;
- marché favorable à C → C travaille ;
- régime défavorable à tous → portefeuille très peu actif.

L'absence de trade ne doit donc pas être considérée comme un échec si les conditions nécessaires à l'existence d'un avantage statistique ne sont pas réunies.

---

## PTA-005 — Diversification des sources de rendement et des régimes de vulnérabilité

**Statut : HYPOTHÈSE / PRINCIPE DE CONCEPTION À VALIDER**

L'objectif futur du portefeuille n'est pas simplement de posséder plusieurs algorithmes ou plusieurs actifs. Il est de combiner des sources de rendement et des régimes de vulnérabilité différents.

Exemples de familles potentielles :

- algorithme directionnel ;
- algorithme range ;
- algorithme breakout ;
- algorithme mean reversion ;
- différents horizons temporels ;
- différents marchés ;
- comportements gagnants dans des régimes différents ;
- périodes de drawdown qui ne surviennent pas systématiquement simultanément.

La diversification devra être démontrée par des analyses appropriées et non déduite du seul fait que les algorithmes utilisent des instruments différents.

---

## PTA-006 — Décorrélation ≠ absence de corrélation statistique entre les actifs

**Statut : PRINCIPE DE CONCEPTION / À OPÉRATIONNALISER**

La « décorrélation » recherchée au niveau portefeuille ne doit pas être réduite à l'absence de corrélation statistique entre les actifs tradés.

Ce que nous cherchons réellement à construire est une diversification des sources de rendement et des régimes de vulnérabilité : les algorithmes doivent idéalement ne pas dépendre du même comportement de marché, ne pas subir leurs drawdowns systématiquement au même moment et ne pas perdre leur avantage pour les mêmes raisons.

L'analyse future devra donc considérer au minimum les rendements, les drawdowns, les expositions et les régimes de marché.

---

## PTA-007 — Track record : distinguer la preuve initiale de la crédibilité institutionnelle

**Statut : HYPOTHÈSE STRATÉGIQUE À VALIDER**

Un track record doit être évalué simultanément selon sa **durée**, sa **performance**, son **risque réellement pris** et la **stabilité de son comportement**. Une performance isolée sur une courte période ne constitue pas une preuve suffisante de robustesse.

### Niveau initial envisagé

Comme repère de travail, une première cible conceptuelle pourrait être :

- environ **20–30 % de performance annualisée** ;
- avec un risque explicitement maîtrisé ;
- et un drawdown historique de l'ordre de **15–19 % maximum**, sous réserve que ces chiffres restent compatibles avec la qualité, la stabilité et la robustesse du processus.

Ces chiffres ne constituent **ni une promesse de rendement ni un seuil universel de qualité**. Ils constituent un repère à tester et à confronter au contexte de marché, au profil de l'algo et à la qualité du track record.

### Niveau visant un intérêt professionnel

Une seconde hypothèse stratégique est qu'un track record capable de démontrer environ **30–50 % annualisés** tout en maintenant un drawdown maximal historique d'environ **10–15 %** pourrait présenter un profil particulièrement attractif pour des investisseurs professionnels, si — et seulement si — cette performance est réelle, robuste, reproductible et obtenue sans prise de risque cachée.

Ce niveau doit être considéré comme une **hypothèse de positionnement**, et non comme une norme imposée aux investisseurs institutionnels. Les critères réellement utilisés par les investisseurs devront être étudiés ultérieurement : durée du track record, volatilité, Sharpe/Sortino, profondeur et durée des drawdowns, liquidité, capacité, corrélation, stabilité des résultats, transparence du processus, risque de modèle et qualité opérationnelle.

### Durée minimale envisagée

Une durée d'au moins **2 années complètes** est retenue à ce stade comme repère minimal pour commencer à constituer un track record suffisamment exploitable pour une démarche visant des capitaux significatifs sous gestion.

Cette durée ne doit toutefois pas être considérée comme une garantie de crédibilité institutionnelle. Un historique plus long et couvrant plusieurs régimes de marché pourra être nécessaire selon l'objectif, le type d'investisseur et la stratégie.

### Principe important

Le système ne doit jamais chercher à atteindre une performance cible en augmentant artificiellement le risque. La question fondamentale doit rester :

> **« Quelle performance avons-nous obtenue pour quel risque, pendant combien de temps et dans quels régimes de marché ? »**

La qualité du track record doit donc être jugée par la relation entre **rendement, risque, durée, robustesse et stabilité**, et non par le rendement brut seul.

---

## Journal des idées à préserver

Cette section est destinée à recevoir les petites avancées, intuitions et hypothèses qui pourraient devenir importantes plus tard, même si leur place exacte dans l'architecture n'est pas encore connue.

**Règle :** mieux vaut enregistrer une idée clairement marquée comme hypothèse que la perdre dans l'historique des conversations. Une idée du journal ne doit cependant jamais être traitée comme une règle validée sans preuve.

### Entrée initiale — Portefeuille adaptatif

Le futur système de gestion du portefeuille algo devra pouvoir sélectionner dynamiquement les algorithmes selon les conditions de marché plutôt que d'imposer une activité constante à tous les algorithmes.

La cible conceptuelle est un portefeuille dans lequel chaque algo possède ses propres points forts et points faibles, tandis que la combinaison cherche à réduire les périodes de drawdown communes et la dépendance à un seul régime de marché.

### Entrée — Architecture de track record

Le futur système devra distinguer au minimum deux objectifs :

1. **Démontrer qu'un algo/portefeuille possède un edge exploitable avec un risque maîtrisé.**
2. **Démontrer qu'il peut supporter une analyse destinée à des capitaux professionnels significatifs.**

Les métriques et seuils ne devront pas être figés prématurément : ils devront être confrontés aux données, aux régimes de marché et aux exigences réelles des investisseurs ciblés.

---

## Principes de prudence

1. Aucun principe ci-dessus ne constitue une preuve de rentabilité.
2. Toute affirmation de supériorité doit être testée sur des données suffisantes et hors échantillon lorsque pertinent.
3. Une amélioration du backtest ne suffit pas à valider un principe si elle peut provenir d'un surajustement.
4. Les contraintes de risque doivent rester explicites même lorsque le potentiel de rendement est laissé ouvert.
5. Une hypothèse non démontrée ne doit jamais être présentée comme un invariant.
6. Un rendement élevé associé à un drawdown faible doit faire l'objet d'une analyse renforcée du risque caché, du surajustement et de la stabilité hors échantillon.
7. Les critères d'attractivité pour investisseurs professionnels ne doivent pas être déduits d'un seul couple rendement/drawdown.
