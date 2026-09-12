# STEP 3 — GATE DU CONTRAT CONTEXT → RESEARCH

## 1. Objet

Ce document formalise le gate adversarial de la future liaison `CONTEXT → RESEARCH`.

Il ne constitue pas une implémentation de RESEARCH et ne modifie aucun composant de production.

Objectif unique : définir ce qui devra obligatoirement être accepté ou rejeté à la frontière lorsque RESEARCH consommera réellement `Context`.

## 2. Précondition

Le système possède déjà un `Context` déterministe construit à partir de l'identité DATA.

La liaison réelle vers RESEARCH n'est pas encore implémentée. Le statut actuel de cette frontière reste donc `BLOCKED`.

Ce gate ne doit pas être interprété comme une preuve d'intégration.

## 3. Contrat minimal

RESEARCH ne pourra considérer un `Context` comme une entrée valide que si :

1. un `Context` est effectivement fourni ;
2. son `context_id` est cohérent avec son contenu ;
3. `dataset_id` est cohérent ;
4. `dataset_version` est cohérente ;
5. `content_hash` est cohérent ;
6. `instrument` est cohérent ;
7. `granularity` est cohérente ;
8. `timezone_storage` est cohérent ;
9. `configuration_version` est cohérente.

Les sept dimensions d'identité utilisées pour le raccord sont donc :

- `dataset_id`
- `dataset_version`
- `content_hash`
- `instrument`
- `granularity`
- `timezone_storage`
- `configuration_version`

`observation_start` et `observation_end` ne font pas partie de l'identité déterministe actuelle du `Context` et ne doivent pas être ajoutés implicitement à ce contrat.

## 4. Règle de frontière

La vérification doit être effectuée **à l'entrée de RESEARCH**, avant que l'artefact de recherche soit considéré comme raccordé au `Context`.

Le point de décision est :

```text
CONTEXT
   ↓
[validation du raccord]
   ├── cohérent → RESEARCH
   └── incohérent / absent → REJECT
```

Aucune vérification tardive dans `DecisionTrace`, la TRACE, la mémoire ou l'audit ne peut remplacer cette vérification de frontière.

## 5. Cas adversariaux minimaux

| Cas | Violation | Attendu |
|---|---|---|
| C0 | Context valide et cohérent | ACCEPT |
| C1 | `context_id` falsifié | REJECT |
| C2 | `dataset_id` différent | REJECT |
| C3 | `dataset_version` différente | REJECT |
| C4 | `content_hash` différent | REJECT |
| C5 | `instrument` différent | REJECT |
| C6 | `granularity` différente | REJECT |
| C7 | `timezone_storage` différent | REJECT |
| C8 | `configuration_version` différente | REJECT |
| C9 | plusieurs dimensions étrangères simultanément | REJECT |
| C10 | aucun Context fourni | REJECT |

## 6. Interdictions de contournement

La future liaison ne doit pas :

- reconstruire silencieusement un `Context` à partir d'autres champs ;
- remplacer un `Context` absent par des valeurs par défaut ;
- accepter un `context_id` seul sans vérifier son contenu ;
- accepter un Context étranger puis corriger son identité après coup ;
- déléguer la décision de raccord à `DecisionTrace` ;
- utiliser un artefact synthétique comme preuve d'intégration réelle ;
- transformer une incohérence en simple avertissement ;
- créer un registre, bus, service ou nouvelle couche d'architecture pour satisfaire ce gate.

## 7. Testabilité

Les cas C0–C10 doivent être exécutables sur les artefacts existants dès que le consommateur RESEARCH acceptera réellement `Context`.

Les tests doivent vérifier non seulement le résultat `ACCEPT/REJECT`, mais aussi que le rejet se produit à la frontière `CONTEXT → RESEARCH`.

Le passage du gate ne pourra être déclaré `PASS` que lorsque :

- C0 est accepté ;
- C1 à C10 sont rejetés ;
- le rejet est produit par le contrôle de frontière ;
- `context_id` est effectivement propagé vers l'artefact RESEARCH ;
- les sept dimensions d'identité sont préservées et vérifiées ;
- aucune nouvelle architecture n'est introduite pour obtenir le résultat.

## 8. Statut actuel

**BLOCKED — absence de consommateur RESEARCH intégré acceptant actuellement `Context`.**

Ce statut signifie que le contrat est défini et cassé conceptuellement, mais que sa preuve exécutable appartient à l'étape suivante : déterminer le plus petit raccord de code permettant d'exposer cette frontière sans encore construire une nouvelle architecture de RESEARCH.

## 9. Prochaine action autorisée

Déterminer le **plus petit raccord de code existant** permettant à RESEARCH de recevoir le `Context` et d'exécuter C0–C10.

Aucune construction plus large de RESEARCH n'est autorisée à ce stade.
