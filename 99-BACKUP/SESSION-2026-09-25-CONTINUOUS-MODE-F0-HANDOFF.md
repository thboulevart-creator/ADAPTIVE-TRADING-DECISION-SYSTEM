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
- digest inventaire : `5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf`;
- 212 Parquet ;
- 3 936 721 231 octets ;
- identity/inventory manifest PASS borné.

## F0 matérialisé

Helper :
`tools/e0_source_b_footer_census.py`
blob : `7fd406e2419e77706028c1c465c595f349cd9b1e`.

Revue adversariale :
`reports/data-qualification/e0_source_b_f0_footer_census_adversarial_review_2026-09-25.md`
blob : `76fa43aad6b14ad23a32a42b67820b2939ba621c`.

Défauts du candidat initial corrigés :
1. possible écriture de rapport dans le corpus lors d'un échec précoce ;
2. sous-comptage du budget metadata en oubliant les 8 octets de probe initial ;
3. risque de signature schéma non déterministe via `repr()` ;
4. absence de manifest transformée en `BLOCKED_MANIFEST_NOT_FOUND` récupérable.

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

## Incident réel après premier handoff F0

La première exécution locale F0 a correctement bloqué sur :

```text
BLOCKED_MANIFEST_BINDING
canonical inventory digest mismatch:
5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf
!=
c6baf5c42808317167b5dc60c88d86b4481b3d0004565bc3a7b33d54ef13ea54
```

Diagnostic : le SHA-256 exact du JSON manifest est resté conforme (`c341fb5e...`). Le digest auxiliaire `c6baf5...` était une erreur de l'adjudication précédente. Deux recalculs indépendants de la formule publiée donnent `5cf0fe2c...`.

Correction durable :
- helper F0 blob `7fd406e2419e77706028c1c465c595f349cd9b1e` ;
- revue adversariale blob `76fa43aad6b14ad23a32a42b67820b2939ba621c` ;
- rapport de correction/re-break :
  `reports/data-qualification/e0_source_b_manifest_inventory_digest_correction_2026-09-25.md`
  blob `9ae1d775f2cc63174ba7c8500428267bccfa82bc`.

Re-break du binding corrigé : **PASS**.

La prochaine action reste une nouvelle exécution locale F0 avec le helper corrigé.