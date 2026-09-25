# Sauvegarde session — mode continu + handoff E0-SOURCE-B-F0

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`

## Méthode de travail adoptée

Le protocole :
`docs/ALGO-ECOSYSTEM-AUTONOMOUS-EXECUTION-PROTOCOL.md`
est maintenant renforcé par les sections 12–15.

Mode par défaut :
```text
DETERMINE
→ EXECUTE
→ VERIFY
→ RECORD
→ HEARTBEAT IF LONG
→ ENCHAIN
→ REPEAT
→ STOP ONLY AT A REAL STOP CONDITION
```

Un heartbeat n'est jamais une demande de confirmation.

Arrêts seulement pour :
- action/commande/fichier local ;
- exécution externe ou contre-expertise réellement requise ;
- autorité normative humaine non déléguée ;
- blocker réel/missing evidence/capability ;
- action destructive/irréversible/live-capital ;
- ambiguïté matérielle non résolue.

La règle est aussi persistée dans `04-REFERENCE/AI-OPERATING-MEMORY.md`.

La plateforme ne permet pas à l'assistant de déclencher seul un nouveau tour après une réponse finale. Si une frontière runtime force une coupure, un simple `continue` suffit ; la reprise doit se faire depuis GitHub/checkpoint/backup sans reconstruction par l'utilisateur.

## État Source-B

Manifest exact :
- SHA-256 : `c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5`;
- digest inventaire : `c6baf5c42808317167b5dc60c88d86b4481b3d0004565bc3a7b33d54ef13ea54`;
- 212 Parquet ;
- 3 936 721 231 octets ;
- identity/inventory manifest PASS borné.

## F0 matérialisé

Helper :
`tools/e0_source_b_footer_census.py`
blob : `fee98c19b880a4d886c0b8cbd208858426de08dc`.

Revue adversariale :
`reports/data-qualification/e0_source_b_f0_footer_census_adversarial_review_2026-09-25.md`
blob : `e5becf81b172e4fe62cb1969cd0a221704a49dc8`.

Défauts du candidat initial corrigés :
1. possible écriture de rapport dans le corpus lors d'un échec précoce ;
2. sous-comptage du budget metadata en oubliant les 8 octets de probe initial ;
3. risque de signature schéma non déterministe via `repr()`.

Verdict de re-break interne :
**PASS — tentative locale F0 read-only autorisée**, avec limitations explicites documentées.

## Frontière actuelle

**LOCAL USER ACTION REQUIRED.**

Exécuter le helper exact sur :
`C:\Users\Boulevart\Documents\ADAPTIVE-TRADING-DECISION-SYSTEM\data\research_source_b_ustech\parquet`

avec le manifest scellé :
`C:\Users\Boulevart\Desktop\ATDS-E0-SOURCE-B-MANIFEST.json`

Le helper doit produire :
`%TEMP%\ATDS-E0-SOURCE-B-F0-FOOTER-CENSUS.json`.

Si `F0_COMPLETE` : joindre le JSON.
Si `BLOCKED_*` : joindre le JSON sans contourner.

Checkpoint actif : §199.

Aucun F1, E1, backtest, MT5, paper/broker/live ou contact Dukascopy n'est ouvert.

STOP à la frontière locale.
