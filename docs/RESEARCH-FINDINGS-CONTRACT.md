# ResearchFindings — contrat minimal

**Version :** 0.1-CANDIDAT  
**Statut :** contrat architectural candidat — non implémenté  
**Source principale :** `docs/03-REGIME-EXPERT-RESEARCH-FOUNDATION.md`  
**Source méthodologique complémentaire :** `docs/D1.3-RESEARCH-CHARTER.md`  

---

## 1. Objet

`ResearchFindings` est le produit analytique attendu entre un **Research Run** et une future **DecisionPolicy**.

Il ne constitue ni :

- le rapport de compatibilité/exécution V4.3 ;
- la preuve de provenance seule (`ResearchRunEvidence`) ;
- une décision de trading ;
- une action d'exécution ;
- une stratégie ou un moteur de recherche.

Chaînage cible :

```text
RESEARCH RUN
    ↓
RESEARCH FINDINGS
    ↓
DECISION POLICY
    ↓
DECISION
```

Le contrat doit permettre de répondre à une question simple :

> **Qu'est-ce que la recherche a effectivement trouvé, sur quel périmètre, avec quelles hypothèses, quelles mesures et quel niveau d'interprétabilité ?**

Aucune conclusion ne doit être inventée par le contrat.

---

## 2. Principe de séparation

`ResearchFindings` sépare explicitement quatre niveaux :

1. **Hypothèse** — ce qui était testé ;
2. **Observation / mesure** — ce qui a été calculé ;
3. **Finding** — conclusion conditionnelle dérivée des mesures selon une règle définie ;
4. **Décision scientifique** — état final de l'essai : `SUPPORTED`, `REFUTED` ou `NOT_INTERPRETABLE`.

Le contrat ne transforme jamais :

```text
absence de preuve → preuve négative
échec technique → hypothèse réfutée
résultat prometteur → règle de trading validée
```

---

## 3. Identité et provenance obligatoires

Tout `ResearchFindings` doit être rattaché à un Research Run précis.

Champs minimaux :

| Champ | Rôle |
|---|---|
| `findings_id` | identifiant déterministe du produit de findings |
| `research_run_id` | Research Run ayant produit les findings |
| `provenance_id` | provenance de la recherche |
| `code_version` | version du code ayant produit les résultats |
| `configuration_version` | configuration de recherche |
| `dataset_id` | dataset effectivement utilisé |
| `dataset_version` | version du dataset |
| `context_id` | contexte de recherche auquel les findings sont rattachés |

### Invariant d'identité

Les identifiants de `ResearchFindings` doivent correspondre à ceux du `ResearchRunEvidence` source.

Une reconstruction silencieuse, un fallback ou l'utilisation d'un seul `context_id` ne constitue pas une provenance valide.

---

## 4. Périmètre de recherche

Le produit doit conserver le périmètre nécessaire pour interpréter les résultats.

Champs minimaux :

- `instrument` ;
- `granularity` / unité d'observation ;
- `period_start` ;
- `period_end` ;
- `horizon` lorsque pertinent ;
- `research_scope` ou identifiant équivalent permettant de retrouver les frontières de l'essai.

Le contrat ne fixe pas ici les valeurs de ces paramètres : elles appartiennent au protocole de recherche effectivement exécuté.

---

## 5. Hypothèses testées

Le produit doit pouvoir référencer une ou plusieurs hypothèses explicitement testées.

Pour chaque hypothèse :

```text
hypothesis_id
statement
prediction
falsification_rule
```

`prediction` et `falsification_rule` doivent être présents lorsque la recherche est déclarée confirmatoire.

Une hypothèse peut rester non interprétable si les contrôles ou les données ne permettent pas de tirer une conclusion valide.

---

## 6. Régimes et experts — structure V1

Le contrat doit pouvoir représenter la structure de recherche définie dans la fondation V1 :

### Régimes

- `TENDANCE`
- `RANGE`
- `BREAKOUT`
- `STRESS`

Une catégorie supplémentaire peut exister uniquement si elle est explicitement définie par le protocole de recherche.

### Experts V1

- `MOMENTUM`
- `BREAKOUT`
- `MEAN_REVERSION`

Ces noms décrivent les catégories de recherche ; ils ne constituent pas à eux seuls des implémentations ou des règles de trading.

---

## 7. Mesures observées

Chaque résultat quantitatif doit être identifiable et rattaché à son périmètre.

Structure minimale conceptuelle :

```text
measurement_id
regime
expert
metric
value
sample_size
scope
```

`metric` est générique au niveau du contrat. Le contrat ne choisit pas arbitrairement une métrique de performance qui n'aurait pas été définie par le protocole de recherche.

Exemples de métriques possibles : performance, fréquence, amplitude, coûts, drawdown ou autre mesure explicitement définie par l'essai.

Une valeur sans périmètre ni taille d'échantillon n'est pas un finding exploitable.

---

## 8. Matrice conditionnelle Régime × Expert

Le produit doit pouvoir représenter la comparaison centrale de la fondation V1 :

| Régime | Momentum | Breakout | Mean Reversion |
|---|---:|---:|---:|
| Tendance | mesure(s) | mesure(s) | mesure(s) |
| Range | mesure(s) | mesure(s) | mesure(s) |
| Breakout | mesure(s) | mesure(s) | mesure(s) |
| Stress | mesure(s) | mesure(s) | mesure(s) |

Cette matrice est une **structure de comparaison**, pas une hypothèse de supériorité.

Le contrat interdit de coder implicitement :

```text
TENDANCE → MOMENTUM
RANGE → MEAN_REVERSION
BREAKOUT → BREAKOUT
```

comme findings validés.

Ces relations restent des hypothèses tant qu'elles ne sont pas démontrées par les résultats de recherche.

---

## 9. Finding

Un `finding` est une conclusion rattachée à des mesures effectivement produites.

Structure minimale :

```text
finding_id
hypothesis_id
statement
supporting_measurement_ids
status
```

`status` doit distinguer au minimum :

- `SUPPORTED` — la règle de décision définie par le protocole est satisfaite ;
- `REFUTED` — la règle de falsification / décision définie par le protocole conduit au rejet ;
- `NOT_INTERPRETABLE` — le résultat ne permet pas une conclusion valide.

`NOT_INTERPRETABLE` est un état terminal distinct de `REFUTED`.

---

## 10. Décision scientifique

Pour chaque hypothèse, le produit doit conserver l'issue scientifique, sans la transformer en décision de trading.

Structure minimale :

```text
hypothesis_id
scientific_status
rule_reference
reason
```

Valeurs minimales :

```text
SUPPORTED
REFUTED
NOT_INTERPRETABLE
```

Le statut `SUPPORTED` signifie uniquement que l'hypothèse satisfait le protocole défini. Il ne signifie pas :

- stratégie prête à trader ;
- avantage économique garanti ;
- robustesse hors échantillon garantie ;
- décision BUY/SELL/HOLD.

---

## 11. Conditions de validité du finding

Un finding ne peut être déclaré interprétable que si le produit peut rattacher la conclusion aux éléments suivants :

```text
Research Run
→ données utilisées
→ hypothèse
→ mesures
→ règle de décision
→ finding
```

Les contrôles critiques doivent être représentés comme :

```text
control_id
status
proof_reference
```

Un contrôle critique échoué ou non interprétable ne doit pas être masqué pour permettre un `SUPPORTED` artificiel.

---

## 12. Reproductibilité minimale

Le contrat doit conserver les références permettant de retrouver les artefacts nécessaires à la reproduction :

- rapport / artefact de recherche ;
- fichiers ou identifiants de mesures ;
- version du code ;
- configuration ;
- dataset ;
- protocole / charter applicable ;
- références des preuves de contrôle.

Le contrat ne prétend pas que la reproduction est réussie : il conserve les références permettant de la vérifier.

---

## 13. Ce que `ResearchFindings` ne peut pas produire

Le contrat ne produit pas :

- `BUY` / `SELL` / `HOLD` ;
- allocation de risque ;
- taille de position ;
- stop-loss ;
- take-profit ;
- ordre d'exécution ;
- action MT5 ;
- résultat de marché ;
- conclusion de portefeuille non testée.

Ces éléments appartiennent aux étapes aval.

---

## 14. Interface minimale vers `DecisionPolicy`

La future `DecisionPolicy` pourra consommer :

```text
ResearchFindings
    ↓
conditions / findings validés
    ↓
politique de décision
    ↓
Decision
```

Mais elle ne doit pas être autorisée à considérer comme validé un finding dont le statut est :

```text
REFUTED
NOT_INTERPRETABLE
```

ou dont les références de provenance / mesures sont incohérentes.

Le contrat de `ResearchFindings` ne définit pas encore la logique de `DecisionPolicy`.

---

## 15. Invariants minimaux à casser ultérieurement

Avant de déclarer le contrat implémentable, les tests adversariaux devront au minimum casser :

- `research_run_id` étranger ;
- `context_id` étranger ;
- `dataset_id` étranger ;
- `dataset_version` étrangère ;
- findings sans hypothèse ;
- finding sans mesure supportante ;
- mesure sans périmètre ;
- finding `SUPPORTED` avec contrôle critique échoué ;
- confusion `NOT_INTERPRETABLE` / `REFUTED` ;
- matrice régime/expert avec identité incohérente ;
- finding reconstruit silencieusement à partir d'un seul identifiant ;
- injection directe d'une conclusion de trading dans le finding.

Cette liste définit le futur périmètre de cassage du contrat ; elle ne constitue pas encore une preuve d'implémentation.

---

## 16. Statut actuel

**CONTRAT : FORMALISÉ — CANDIDAT**

**PRODUCTEUR : ABSENT**

**MOTEUR DE RECHERCHE : NON IMPLÉMENTÉ**

**Research Run → ResearchFindings : BLOCKED**

Le présent document formalise uniquement la frontière attendue. Il n'implémente ni `ResearchFindings`, ni détecteur de régime, ni expert, ni comparateur, ni calcul statistique.

La prochaine étape d'implémentation devra d'abord transformer ce contrat en objet exécutable minimal, puis le casser avant de construire le moteur de recherche.