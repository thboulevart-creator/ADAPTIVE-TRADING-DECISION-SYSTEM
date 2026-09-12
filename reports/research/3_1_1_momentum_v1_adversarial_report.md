# 3.1.1 — RAPPORT DE CASSAGE ADVERSARIAL MOMENTUM V1

**Date : 12 septembre 2026**  
**Verdict final : PASS**

## 1. Formalisation initiale

La première candidate Momentum était fondée sur une variation de prix sur un horizon de 20 barres, avec une direction positive/négative/neutre.

## 2. Premier cassage — FAIL de formalisation

Deux ambiguïtés ont été identifiées :

1. le timeframe n'était pas explicitement figé ; « 20 barres » pouvait donc changer de signification ;
2. la distinction entre un changement de signal et une action de trading n'était pas suffisamment explicite.

Ces FAILs ne réfutaient pas l'hypothèse Momentum ; ils montraient que la définition n'était pas encore exécutable sans interprétation.

## 3. Correction

La définition a été figée comme suit :

- H1 ;
- variable Close ;
- horizon 20 barres ;
- `M_t = Close_t / Close_{t-20} - 1` ;
- `M_t > 0` → LONG ;
- `M_t < 0` → SHORT ;
- `M_t = 0` → NEUTRE ;
- historique insuffisant → UNDEFINED ;
- calcul à la clôture de `t`, utilisation à partir de `t+1` ;
- signal directionnel distinct d'une transaction.

## 4. Second cassage

Contrôles adversariaux :

- look-ahead → PASS ;
- utilisation de la barre courante → PASS ;
- timeframe → PASS ;
- ambiguïté de l'horizon → PASS ;
- changement de direction sans ordre implicite → PASS ;
- séparation ADX/ATR/régime → PASS ;
- optimisation cachée du paramètre 20 → PASS sous la contrainte que 20 reste une hypothèse de baseline non sélectionnée par backtest ;
- reproductibilité → PASS ;
- historique insuffisant → PASS via `UNDEFINED` ;
- données manquantes → PASS sous réserve que la couche de données les rejette ou les signale et que Momentum ne reconstruise rien.

## 5. Verdict

**3.1.1 — PASS**

Le PASS porte uniquement sur la définition formelle et sa résistance au second cassage. Il ne valide ni rentabilité, ni robustesse, ni avantage statistique, ni pertinence par régime.

## 6. Règle de non-régression

Ne pas réoptimiser ou modifier l'horizon 20 sur la base des résultats du premier backtest. Toute modification ultérieure doit être traitée comme nouvelle hypothèse et repasser par formalisation/cassage/re-cassage.

## 7. Prochaine action

Passer à `3.1.2 — Premier backtest baseline`, après formalisation et cassage du protocole de backtest lui-même.
