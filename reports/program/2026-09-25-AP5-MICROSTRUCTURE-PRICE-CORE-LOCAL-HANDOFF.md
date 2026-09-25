# AP5 — MICROSTRUCTURE PRICE-CORE — handoff local

Date : 2026-09-25  
Branche gouvernée : `integration/system-v1`.

Helper figé :
- commit : `715c3e4affa44778785d6c222782eda257ed19e7` ;
- path : `tools/ap5_microstructure_price_core.py` ;
- blob : `21de65a7fbf8277dd2eb0afc99f4c2b80912af06` ;
- SHA-256 : `fdb929f54d5c816cd12fb03130545b3714a38cb2261d3b23433fb1cd4b0f7671`.

Re-break :
- 12/12 tests PASS ;
- 7/7 mutation breakers détectés ;
- compilation PASS.

Verdict :
**PASS — helper pour tentative locale.**
**BLOCKED — AP5 corpus avant résultat exact.**

## Entrées attendues

AP0 :
`%USERPROFILE%\Documents\ATDS-DERIVED\USTECH_PROFILE_MINUTE_CORE_V0_1`

Manifest :
`%USERPROFILE%\Documents\ATDS-DERIVED\USTECH_PROFILE_MINUTE_CORE_V0_1\AP0-MANIFEST.json`

Repo local :
le clone exact du dépôt `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`.

Le helper lie également l'evidence AP4 versionnée :
`reports/program/evidence/2026-09-25-AP4-PRICE-STRUCTURE.json`
SHA-256 :
`c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad`.

## Règle d'exécution

Extraire le helper depuis le commit figé avec `git show`, vérifier son SHA-256, puis l'exécuter.

Ne pas :
- changer de branche ;
- reset/rebase ;
- écraser un output existant ;
- installer une dépendance automatiquement ;
- utiliser un autre helper ;
- contourner un BLOCKED.

Output attendu :
`%TEMP%\ATDS-AP5-MICROSTRUCTURE-PRICE-CORE.json`.

Succès terminal attendu :
`AP5_COMPLETE`.

Après exécution, fournir le terminal et le JSON exact. En cas de `BLOCKED_AP5_*`, fournir le terminal et ne rien contourner.
