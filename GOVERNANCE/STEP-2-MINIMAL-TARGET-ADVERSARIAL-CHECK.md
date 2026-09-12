# ÉTAPE 2 — Cassage adversarial de la cible minimale

**Statut :** CONTRÔLE EFFECTUÉ — corrections sémantiques requises avant gel
**Branche :** `feat/step2-minimal-system-target`

## Objectif

Casser la cible `DONNÉE → CONTEXTE → RECHERCHE / EXPÉRIENCE → DÉCISION → ACTION → RÉSULTAT → TRACE → MÉMOIRE → AUDIT → RÉVISION` avant toute implémentation.

Le test porte sur la sémantique de la cible, pas sur le code.

---

## 1. Attaque — « chaque décision doit-elle produire une nouvelle expérience ? »

### Violation recherchée

Interpréter la chaîne comme :

`DONNÉE → CONTEXTE → NOUVELLE EXPÉRIENCE → DÉCISION`

pour chaque décision.

### Résultat

**FAIL de l'interprétation**, car cela imposerait une expérimentation nouvelle à chaque décision opérationnelle et empêcherait une décision de réutiliser une connaissance déjà validée.

### Correction minimale

`RECHERCHE / EXPÉRIENCE` est défini comme **base d'apprentissage et de connaissance pertinente de la décision**, pas comme expérience obligatoirement créée juste avant chaque décision.

La chaîne de référence décrit la provenance complète d'une connaissance lorsqu'elle existe ; elle ne transforme pas chaque décision en expérience.

---

## 2. Attaque — « TRACE devient-elle productrice de continuité ? »

### Violation recherchée

Faire de `TRACE` le mécanisme qui crée ou garantit l'existence des événements précédents.

### Résultat

**FAIL.** Une trace ne peut pas fabriquer une décision, une action ou un résultat absent.

### Correction minimale

`TRACE` est une **projection de reconstruction et de liaison** des éléments réellement produits. Une trace sans événements source vérifiables ne constitue pas une preuve de leur existence.

---

## 3. Attaque — « MÉMOIRE → AUDIT → RÉVISION doit-il s'exécuter à chaque résultat ? »

### Violation recherchée

Transformer la boucle de gouvernance en pipeline synchrone obligatoire après chaque action.

### Résultat

**FAIL de cette contrainte**, car elle imposerait une architecture et une charge inutilement fortes.

### Correction minimale

La boucle est **fonctionnellement obligatoire**, mais son exécution peut être déclenchée selon la criticité, le type d'expérience, les règles de gouvernance ou les événements de réévaluation pertinents.

Un résultat critique ne peut toutefois pas être promu en connaissance opérationnelle sans le niveau de mémoire, contestation, preuve et autorisation requis.

---

## 4. Attaque — « les dix blocs sont-ils dix composants ? »

### Violation recherchée

Déduire de la cible fonctionnelle une architecture à dix services/modules/agents.

### Résultat

**REJETÉ.** Cela viole la règle de non-prolifération.

### Correction minimale

Les dix éléments sont des **fonctions à couvrir**. Un même mécanisme peut couvrir plusieurs fonctions et plusieurs mécanismes peuvent composer une fonction.

La cible ne prescrit ni stockage, ni service, ni agent, ni API, ni processus distribué.

---

## 5. Attaque — « ACTION implique-t-elle nécessairement une exécution de marché ? »

### Violation recherchée

Réduire `ACTION` à un ordre broker.

### Résultat

**FAIL.** Cela rendrait impossible la représentation de décisions valides telles que PAS DE TRADE, réduction d'exposition, suspension ou arrêt.

### Correction minimale

`ACTION` signifie **comportement effectivement engagé à la suite de la décision**, y compris l'absence contrôlée d'action lorsque celle-ci constitue la décision opérationnelle.

---

## 6. Attaque — « RÉSULTAT prouve-t-il la cause ? »

### Violation recherchée

Déduire automatiquement de `ACTION → RÉSULTAT` que l'action a causé le résultat ou qu'un résultat favorable valide la connaissance utilisée.

### Résultat

**FAIL.** Une corrélation temporelle ou un résultat favorable ne constitue pas une preuve causale suffisante.

### Correction minimale

`RÉSULTAT` enregistre ce qui est observé après l'action. L'explication causale reste une hypothèse à tester et appartient à la boucle d'expérience/mémoire/audit.

---

## 7. Attaque — « CONTEXTE est-il un raccourci vers la décision ? »

### Violation recherchée

Faire contenir au contexte une décision, un signal, une performance future ou une information connue seulement après l'instant de décision.

### Résultat

**REJETÉ.** Le contexte doit rester descriptif des conditions pertinentes et ne doit pas incorporer la réponse qu'il est censé aider à déterminer.

### Correction minimale

`CONTEXTE` décrit les conditions pertinentes au moment considéré ; il ne contient pas la décision ou son résultat comme données constitutives.

---

## 8. Attaque — « AUDIT signifie-t-il correction automatique ? »

### Violation recherchée

`AUDIT → RÉVISION` comme modification automatique du comportement.

### Résultat

**FAIL.** Cela permettrait à un contrôle de s'auto-promouvoir en changement opérationnel.

### Correction minimale

`AUDIT` produit un constat, une contestation ou un verdict selon les règles applicables. `RÉVISION` est une fonction contrôlée distincte ; elle peut conclure **aucun changement**.

---

## 9. Attaque globale — suppression de la distinction « chemin causal » / « boucle de gouvernance »

### Risque

Lire les dix blocs comme une chaîne temporelle unique où chaque bloc doit immédiatement produire le suivant.

### Verdict

**FAIL de cette lecture.**

### Correction structurante

La cible doit être comprise comme :

```text
        CHEMIN DE DÉCISION / ACTION

DONNÉE → CONTEXTE → BASE DE CONNAISSANCE → DÉCISION → ACTION → RÉSULTAT
                                      │                         │
                                      └────────── TRACE ─────────┘
                                                       │
                                                       ↓
                                      MÉMOIRE → AUDIT → RÉVISION
                                                       │
                                                       └──→ nouvelle recherche / expérience
```

La chaîne est donc une **graphe de provenance fonctionnelle**, pas une obligation de synchronisation de dix étapes.

---

## 10. Résultat du cassage

La cible initiale était correcte dans son intention mais présentait quatre ambiguïtés dangereuses :

1. confusion entre expérience nouvelle et connaissance expérimentale déjà disponible ;
2. risque de traiter TRACE comme producteur ;
3. risque de transformer mémoire/audit/révision en pipeline synchrone obligatoire ;
4. risque de confondre fonctions et composants techniques.

Ces ambiguïtés sont maintenant explicitement levées.

### État

**CIBLE MINIMALE : CANDIDATE CORRIGÉE — NON ENCORE GELÉE.**

Le prochain contrôle doit vérifier que ces corrections sont compatibles avec la cible globale sans réintroduire de nouveau bloc ou de nouvelle architecture.
