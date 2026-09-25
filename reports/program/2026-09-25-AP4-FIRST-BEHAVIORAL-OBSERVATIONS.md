# AP4 — premières observations comportementales qualifiées
Date : 2026-09-25
Source : `reports/program/evidence/2026-09-25-AP4-PRICE-STRUCTURE.json`
SHA-256 : `c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad`

Type épistémique : **OBSERVATION / DESCRIPTION**.
Aucune observation ci-dessous n'est une stratégie, un signal ou une preuve prédictive.

## 1. Alternance minute légèrement supérieure à la persistance

Sur les paires de retours 1m non nuls et contigus :
- persistance : 49.33796682202942 % ;
- retournement : 50.66203317797058 %.

Les buckets annuels montrent la même orientation descriptive, avec une persistance d'environ 49.10 % à 49.50 % selon l'année. Cela suggère une caractéristique descriptive peu variable dans ces agrégats annuels, mais **AP6 doit encore qualifier la stabilité** avant toute conclusion de stabilité.

## 2. Les runs directionnels 1m sont généralement courts

DOWN :
- médiane 1 minute ;
- p90 4 ;
- p99 7 ;
- max 20.

UP :
- médiane 2 minutes ;
- p90 4 ;
- p99 7 ;
- max 18.

Ces runs dépendent explicitement de la granularité 1m et ne doivent pas être confondus avec des swings/pivots de marché universels.

## 3. L'efficacité directionnelle décroît avec l'horizon

`E_H = |somme(r)| / somme(|r|)`.

Global :
- moyenne 15m = 0.25740927472902353 ;
- moyenne 60m = 0.13080767215518072.

Les moyennes annuelles 15m se situent environ entre 0.2531 et 0.2603 ; les moyennes 60m entre 0.1285 et 0.1333. C'est une description de trajectoires plus ou moins directes, pas une mesure de rentabilité.

## 4. Les réintégrations de range sont fréquentes dans les comptes observés

Le protocole ne transforme pas ces comptes en probabilité prédictive.

Franchissements du range passé 15m :
- UP : 95 187 réintégrations observées ; médiane du délai 2 minutes ;
- DOWN : 87 688 ; médiane 2 minutes.

Franchissements du range passé 60m :
- UP : 45 064 ; médiane 2 minutes ;
- DOWN : 38 834 ; médiane 2 minutes.

Le p90 du délai vaut 9 minutes dans les quatre cas. Les événements successifs se chevauchent potentiellement ; ils ne sont pas indépendants.

## 5. Les réouvertures portent des déplacements discontinus non négligeables

Sur 1 605 frontières de segment :
- déplacement absolu médian : 5.993795613435418 bps ;
- p90 : 31.995592415618358 bps ;
- p99 : 118.19115682382152 bps ;
- max : 517.6103757428144 bps.

Ces mouvements restent séparés des retours continus. Aucune cause — fermeture normale, holiday, perte d'acquisition ou autre — n'est attribuée par AP4.

## Limite de promotion

Aucune hypothèse de trading n'est promue depuis ces observations. AP5 doit maintenant qualifier la microstructure PRICE-CORE ; AP6 devra ensuite tester la stabilité temporelle.
