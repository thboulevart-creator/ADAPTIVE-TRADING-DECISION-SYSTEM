# AP4 — PRICE STRUCTURE — adjudication V0.1
Date : 2026-09-25
Fresh HEAD avant persistance : `52da2531c98e63a934742f9dddc51b17179389df`.

## Evidence exacte

Rapport local reçu et ingéré :
`reports/program/evidence/2026-09-25-AP4-PRICE-STRUCTURE.json`

- taille exacte : 15 488 octets ;
- SHA-256 recalculé sur les octets reçus : `c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad` ;
- status : `AP4_COMPLETE` ;
- schema : `ATDS_AP4_PRICE_STRUCTURE_V0_1` ;
- input : `USTECH_PROFILE_MINUTE_CORE_V0_1`.

Bindings :
- AP0 manifest : `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce` ;
- AP3 exact : `caa2d02942d5cbd05bcfadd0dedfabde000e4e941cdf4aa4b0433801f76f42ef` ;
- helper AP4 : `f957b38a252ffb2649602fdc5405b82735c88300e1f32cc9fee5f41834098987` ;
- 61 fichiers AP0 rehashés.

## Contrôles d'intégrité

Les invariants pré-enregistrés ont été vérifiés sur le JSON exact :

- 1 709 180 minutes ;
- 1 606 segments ;
- 1 707 574 retours 1m valides ;
- 1 686 423 fenêtres 15m et 1 620 195 fenêtres 60m, réconciliées avec AP2 ;
- 1 605 frontières de réouverture ;
- matrice directionnelle : conservation des 1 706 047 paires éligibles ;
- 1 703 540 paires non nulles et 2 507 paires impliquant un zéro ;
- conservation des signes et des runs directionnels ;
- pour chaque horizon et direction, `event_count = reentered + not_reentered_full_15m + censored` ;
- le nombre des réintégrations égale le count du délai de première réintégration ;
- somme des minutes annuelles = 1 709 180 ;
- flags de portée conformes : aucune stratégie, signal, PnL, optimisation, volume source ou label prédictif exporté.

## Résultats descriptifs bornés

Direction minute :
- persistance = 0.4933796682202942 ;
- retournement = 0.5066203317797058.

Efficacité directionnelle :
- 15m moyenne = 0.25740927472902353, médiane = 0.22367145981390998 ;
- 60m moyenne = 0.13080767215518072, médiane = 0.1115368569298813.

Franchissements 15m :
- UP : 130 221 événements, 95 187 réintégrés, 34 510 non réintégrés sur 15m complets, 524 censurés ;
- DOWN : 117 253 événements, 87 688 réintégrés, 29 124 non réintégrés sur 15m complets, 441 censurés.

Franchissements 60m :
- UP : 61 792 événements, 45 064 réintégrés, 16 444 non réintégrés sur 15m complets, 284 censurés ;
- DOWN : 52 218 événements, 38 834 réintégrés, 13 160 non réintégrés sur 15m complets, 224 censurés.

Pour les événements effectivement réintégrés, le délai médian est 2 minutes et le p90 9 minutes dans les quatre groupes.

Réouvertures :
- 1 605 frontières ;
- déplacement discontinu absolu médian = 5.993795613435418 bps ;
- p90 = 31.995592415618358 bps ;
- p99 = 118.19115682382152 bps ;
- max = 517.6103757428144 bps.

## Limites

- Le rapport est issu de l'exécution locale utilisateur ; il n'a pas été reproduit indépendamment dans cet environnement.
- L'audit du helper a été réalisé par le même assistant que le producteur ; aucune indépendance n'est revendiquée.
- Les observations de réintégration utilisent le futur : `future_observations_used=true`, `causal_deployable=false`.
- Les fenêtres se chevauchent et ne sont pas des observations indépendantes.
- Les swings sont des suites close-to-close 1m, pas des pivots structurels universels.
- Les causes des interruptions/réouvertures ne sont pas inférées.
- AP6 reste nécessaire pour qualifier formellement la stabilité temporelle.
- Aucun résultat AP4 ne constitue une preuve d'edge, une règle de trading ou un prix d'exécution.

## Verdict

**PASS — AP4 PRICE STRUCTURE qualifié descriptivement sous le contrat pré-enregistré et les bindings exacts.**

Ce PASS qualifie le rapport AP4 et ses métriques strategy-agnostic. Il n'autorise ni stratégie, ni backtest, ni MT5, ni PnL, ni optimisation.

Prochaine action gouvernée : pré-enregistrer AP5 MICROSTRUCTURE PRICE-CORE.
