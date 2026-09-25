# E0-SOURCE-B — réconciliation timestamp/session après récupération historique

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD vérifié avant écriture : `b860fc3469752942a79033cbdaa2bc8e18f21e22`

## Objet

Résoudre la contradiction entre :
- F0 : `timestamp[ms]` sans timezone qualifiée ;
- anciens probes de session ;
- probes ultérieurs ayant imposé `Europe/Paris wall-clock -> UTC` ;
- F1 courant ;
- horaires officiels USATECH.

Aucune donnée prix/volume n'est relue ici.

## 1. Ancre F1

F1 exact :
- SHA-256 : `2b95780b053e7c83bdb48e10eb6702828e3d80ebf38e1a68eb811890a9523067` ;
- 376 003 618 timestamps ;
- 1 605 gaps >60 s ;
- 0 null ;
- 0 backward ;
- 0 equal-adjacent.

Les ISO F1 sont des représentations naïves des valeurs physiques millisecondes.

## 2. Source officielle de session

Dukascopy, page officielle "Range of markets", tableau CFD "Trading Hours (GMT)":

USATECH.IDX/USD :
- **Summer** : trading Sun–Fri 22:00–20:15 GMT ; break daily **20:15–22:00 GMT** ;
- **Winter** : trading Sun–Fri 23:00–21:15 GMT ; break daily **21:15–23:00 GMT**.

Source :
`https://www.dukascopy.com/swiss/spanish/cfd/range-of-markets/`

La page identifie explicitement les colonnes comme `Trading Hours (GMT)` et `Trading Breaks (GMT)`.

Une publication officielle Dukascopy sur le DST US 2024 indique que le passage à Summer Trading time intervient avec le changement d'heure US et inclut USATECH.IDX/USD.

Source :
`https://www.dukascopy.com/swiss/pl/about/ournews/daylight-saving-time-2024-in-the-us`

## 3. Empreinte session observée dans F1

Parmi les 1 605 gaps >60 s :

- gaps dont le dernier tick brut est à minute **20:14** et la reprise à heure **22** : **818** ;
- dont reprise exactement à **22:00** : **567** ;
- gaps dont le dernier tick brut est à minute **21:14** et la reprise à heure **23** : **406** ;
- dont reprise exactement à **23:00** : **404**.

Les changements saisonniers du motif brut observés apparaissent au premier jour de trading suivant le changement DST US :

- 2021-11-08 : 21:14→23:00 ;
- 2022-03-14 : 20:14→22:00 ;
- 2022-11-07 : 21:14→23:00 ;
- 2023-03-13 : 20:14→22:00 ;
- 2023-11-06 : 21:14→23:00 ;
- 2024-03-11 : 20:14→22:00 ;
- 2024-11-04 : 21:14→23:00 ;
- 2025-03-10 : 20:14→22:xx ;
- 2025-11-03 : 21:14→23:00 ;
- 2026-03-09 : 20:14→22:00.

Cette empreinte correspond directement aux heures GMT officielles Summer/Winter de USATECH.

## 4. Test des hypothèses de timezone

### H-UTC/GMT

Interpréter la valeur naïve brute comme horloge GMT/UTC.

Prédiction :
- summer break brut ≈20:15→22:00 ;
- winter break brut ≈21:15→23:00.

Observation F1 :
**correspondance directe et répétée sur 2021–2026.**

Verdict :
**SUPPORTED.**

### H-EUROPE/PARIS

Interpréter la valeur brute comme Europe/Paris puis convertir en GMT.

En été, un brut 20:15→22:00 Paris deviendrait ≈18:15→20:00 GMT.
En hiver, un brut 21:15→23:00 Paris deviendrait ≈20:15→22:00 GMT.

Ces prédictions ne correspondent pas au tableau officiel USATECH.

Verdict :
**CONTRADICTED par l'empreinte session.**

## 5. Origine probable de l'ancienne ambiguïté

Le script historique `probe_huggingface_ustech_session_continuity_h9_1_c3_b2_c1.py` transforme un datetime naïf avec :

```python
value.timestamp()
```

Sur un host Windows configuré Europe/Paris, `datetime.timestamp()` applique implicitement le timezone local à une valeur naïve. Cette conversion a produit des timestamps décalés sans politique timezone explicitement scellée.

D'autres scripts ont ensuite tenté de normaliser explicitement Europe/Paris.

Le rapport historique `timezone_normalized_provenance...` reste `PASS_WITH_LIMITATION` et ne certifie pas l'équivalence feed :
- 33 timestamps exacts communs sur 7 156 Parquet / 8 184 source ;
- 0 exact bid/ask match ;
- divergence de prix importante ;
- classification `TEMPORALLY_ALIGNED_BUT_PRICE_DIVERGENCE`.

Il ne constitue donc pas une preuve suffisante pour imposer Europe/Paris face à l'empreinte session officielle.

## 6. Classification régulière des 1 605 gaps

Le F1 a été reclassé sans lire les prix, en :
1. interprétant le brut comme UTC/GMT ;
2. convertissant en `America/New_York` ;
3. appliquant la session régulière :
   Sunday 18:00 NY → Friday 16:15 NY ;
   daily break 16:15→18:00 NY ;
4. sans holiday overrides.

Résultat :
- `SESSION_BOUNDARY_GAP` : **1 290** ;
- `TRUE_OPEN_SESSION_GAP` : **315** ;
- `NORMAL_CLOSED_PERIOD` : **0** parmi les gaps >60 s, car les endpoints entourant les fermetures contiennent typiquement quelques millisecondes/secondes de période ouverte.

Les 22 gaps du gap-forensics historique sont tous :
**22/22 TRUE_OPEN_SESSION_GAP** sous cette réconciliation.

## 7. Portée du verdict

**PASS_WITH_LIMITATION — la sémantique de l'horloge brute comme GMT/UTC est suffisamment supportée pour la classification de session régulière.**

La limitation est volontaire :
- le Parquet lui-même ne porte pas de timezone ajustée ;
- les horaires spéciaux de jours fériés ne sont pas encore appliqués au full corpus ;
- des interruptions de cotation en session ouverte ne sont pas automatiquement des pertes de données.

La politique historique `Europe/Paris wall-clock -> UTC` est **SUPERSEDED pour la classification de session Source-B**, sans effacer son historique.

## 8. Prochaine action

Ne pas refaire les 22 cas déjà cross-checkés.

Sur les **315 TRUE_OPEN_SESSION_GAP** du full corpus :
1. retirer les fermetures spéciales documentées par le Trading Breaks Calendar / notices officielles ;
2. conserver séparément les gaps de faible activité de cotation ;
3. appliquer les 13 LOSS / 9 UNKNOWN historiques aux 22 intervalles exacts ;
4. déterminer le sous-ensemble résiduel réellement non expliqué ;
5. décider si ce résiduel est matériel pour l'usage de recherche visé.

Aucun backtest/E1 n'est ouvert par ce rapport.
