# AP5 — Microstructure price-core — adjudication

Date : 2026-09-25  
Branche : `integration/system-v1`  
Fresh HEAD avant persistance : `38a9a9ad12de6574ffe4686c77bd98fa7638245d`.

## Evidence qualifiée

Evidence exacte :
`reports/program/evidence/2026-09-25-AP5-MICROSTRUCTURE-PRICE-CORE.json`

Identité :
- taille : 39 460 octets ;
- SHA-256 : `21dc09b082e32f20543c6206c276c24389b7b61fd930fbe2d1783adabaca4406` ;
- schema : `ATDS_AP5_MICROSTRUCTURE_PRICE_CORE_V0_1` ;
- status : `AP5_COMPLETE`.

La copie reçue a été rehashée indépendamment avant persistance et correspond exactement au SHA annoncé par l'exécution locale R4.

## Provenance d'exécution R4

Le terminal R4 a établi avant exécution :
- helper brut Git exact : SHA-256 `fdb929f54d5c816cd12fb03130545b3714a38cb2261d3b23433fb1cd4b0f7671`, 566 LF, 0 CRLF ;
- AP4 brut Git exact : SHA-256 `c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad`, 644 LF, 0 CRLF ;
- rehash PowerShell identique pour les deux fichiers ;
- `python -m py_compile` : PASS ;
- `AP5_COMPLETE` ;
- exit code 0.

R1/R2 sont conservés comme BLOCKED de binding AP4.
R3 est conservé comme candidat non qualifié à cause du helper local non canonique.
R4 est la première tentative satisfaisant simultanément les bindings binaires et l'exécution complète.

## Bindings et couverture

- AP0 files rehashed : 61 ;
- AP0 manifest SHA-256 : `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce` ;
- AP4 SHA-256 : `c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad` ;
- minute rows : 1709180 ;
- source ticks accounted : 376003618 ;
- segments : 1606 ;
- segment-start rows : 1606.

Les cinq partitions vérifiées — heure New York, session-clock proxy, quintiles de range, quintiles de tick density et années UTC — reconservent chacune exactement 1709180 minutes et 376003618 ticks source.

## Réconciliations pré-enregistrées

Toutes PASS :
- F2 spread min = 0.000999999996565748 ;
- F2 spread max = 35.66699999999764 ;
- F2/AP1 spread tick-weighted mean = 2.1395040593705206 ;
- AP2 minute-range mean = 4.033115022615127 bps ;
- AP2 valid 1m count = 1707574 ;
- AP2 mean abs 1m = 2.130371613870453 bps.

Tolérance numérique enregistrée : 1e-9.

## Scope

Le payload déclare :
- strategy_agnostic = true ;
- signals_calculated = false ;
- pnl_calculated = false ;
- optimization = false ;
- source_volume_used = false ;
- subminute_microstructure_qualified = false ;
- future_observations_used = false ;
- causal_deployable = false.

Aucune donnée volume/profondeur/order-flow n'est qualifiée.

## Limites

- `tick_count` mesure la densité de ticks, pas le volume négocié ;
- le proxy 09:30–16:00 America/New_York est un proxy d'horloge weekday, pas un calendrier officiel d'exchange ;
- les corrélations sont descriptives, pas causales ;
- les quintiles full-sample ne sont pas des seuils de déploiement live ;
- aucune microstructure sub-minute n'est qualifiée ;
- AP6 doit encore mesurer la stabilité temporelle ;
- même assistant producteur/auditeur : aucune indépendance revendiquée.

## Verdict

**PASS — AP5 MICROSTRUCTURE PRICE-CORE.**

Ce PASS qualifie uniquement le profil descriptif price-core enregistré. Il ne qualifie aucune stratégie, aucun edge et aucune causalité.

AP6 peut être ouvert.
