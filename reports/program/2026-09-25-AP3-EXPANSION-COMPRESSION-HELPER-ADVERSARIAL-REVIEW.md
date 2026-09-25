# AP3 — EXPANSION / COMPRESSION — revue adversariale du helper

Date : 2026-09-25

Candidat :
`tools/ap3_expansion_compression.py`

Blob :
`8a7aa643eb6e4414dad378ca4ddb8b98adce7bd1`.

## Attaques

### E1 — AP3 devient une stratégie
Le helper ne calcule :
- aucun sens long/short ;
- aucun signal ;
- aucun PnL ;
- aucun résultat futur.

Les états décrivent uniquement un niveau de volatilité.

**PASS.**

### E2 — seuils choisis selon une performance
Seuils préenregistrés :
- p20 ;
- p80.

Aucun sweep.
Aucun PnL.
Aucune sélection par performance.

**PASS.**

### E3 — fuite temporelle des seuils full-sample
Les médianes horaires et quantiles utilisent le corpus complet.

Le helper doit déclarer :
- `full_sample_descriptive_thresholds=true` ;
- `causal_deployable=false`.

Ces labels sont interdits comme feature temps-réel ou signal sans nouveau contrat causal.

**PASS par restriction explicite de portée.**

### E4 — divergence avec AP2
Avant classification, AP3 reconstruit RV15 et RV60 à partir d'AP0.

Il doit retrouver AP2 pour :
- count ;
- mean ;
- p50 ;
- p90 ;
- p95 ;
- p99 ;
- p99.9 ;
- max ;
à tolérance absolue 1e-9.

**PASS fail-closed.**

### E5 — gap traversé
RV15/RV60 reprennent la règle AP2 :
- transitions 1m valides ;
- même segment ;
- écart temporel exact.

**PASS.**

### E6 — saisonnalité intraday confondue avec expansion
Deux lentilles distinctes :
1. absolute RV15 ;
2. RV15 / médiane RV15 de la même heure New York.

La seconde réduit le biais horaire attendu.

**PASS.**

### E7 — changement artificiel à une frontière d'heure
Le candidat initial aurait pu créer une transition à HH:59→HH+1:00 uniquement parce que la médiane de normalisation change.

Correction :
les phases et transitions de la lentille normalisée exigent désormais la même heure New York aux deux côtés.

**Re-break : PASS.**

### E8 — perte d'observations lors de normalisation
Le helper exige :
- somme des valid_count des 24 baselines = count RV15 valide ;
- normalized valid count = RV15 valid count ;
- somme des valid_count annuels = normalized valid count.

**PASS fail-closed.**

### E9 — phase incohérente
Une phase exige :
- état valide ;
- même état ;
- même segment ;
- minute suivante exacte ;
- et, pour la lentille normalisée, même heure NY.

La somme des durées de phase doit égaler le nombre de minutes d'état valides.

**PASS.**

### E10 — matrice de transitions ambiguë
Transitions uniquement entre minutes adjacentes valides dans le même segment.
La lentille normalisée exclut les changements d'heure.

Counts + probabilités conditionnelles sont conservés.

Aucune transition n'est présentée comme prédiction.

**PASS.**

### E11 — variance-share impossible
`RV15^2/RV60^2` doit rester dans [0,1] à tolérance 1e-9 lorsque RV60>0.

Tout dépassement matériel bloque.

**PASS.**

### E12 — direction de marché cachée
RV15/RV60 utilisent les carrés des log-returns.
La variance-share ne contient pas de direction.

**PASS.**

### E13 — dérive de données
Bindings exacts :
- AP0 manifest ;
- AP2 JSON ;
- 61 fichiers AP0 re-hashés.

**PASS.**

### E14 — stabilité temporelle ignorée
AP3 conserve les shares de la lentille normalisée par UTC-year.
2021 et 2026 sont marquées partielles.

AP6 reste nécessaire pour une conclusion de stabilité.

**PASS.**

## Verdict

**PASS — helper AP3 suffisamment borné pour tentative locale.**

Ce PASS autorise uniquement une description ex post :
- compression ;
- normal ;
- expansion ;
- durées ;
- transitions adjacentes ;
- concentration de variance.

Il n'autorise aucune utilisation causale/stratégique des labels AP3.

Prochaine frontière :
exécuter AP3 localement et joindre le JSON exact.
