# E0 — Inventaire réel des neuf archives historiques déjà présentes sur GitHub

Date : 2026-09-23
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD de lecture figé : `19f8b363e45f070ccbce9a5d0322f005579b4f08`
Nature : lecture seule des octets **déjà archivés** ; aucune acquisition auprès du fournisseur, aucun signal, position, trade, PnL ni backtest.

## 1. Périmètre et bornes

Le premier périmètre réellement accessible depuis cette session est le dossier GitHub :
`evidence/berd02/gha_run_35533153289/bodies/` — **neuf** objets K1 `.bi5` déjà versionnés. Le dépôt exact et la connexion GitHub étaient autorisés ; l'instruction utilisateur a déclenché le seul inventaire E0 de ces fichiers, sans accès au disque local.

Métadonnées lues pour confrontation dans le même snapshot :
- `evidence/berd02/gha_run_35533153289/transport_captures.json`, blob `7048fd421e934382dfbbe830e23fd3f6161540e3` ;
- `evidence/berd02/gha_run_35533153289/execution_result.json`, blob `c4d994a9c39cb2addae492a4f55556c7f799d091` ;
- `evidence/berd02/gha_run_35533153289/diagnostic_a.json`, blob `77c5b216e92bd04e9c3bb121e7b2759bf38a66b7` ;
- `evidence/berd02/gha_run_35533153289/diagnostic_b.json`, blob `6322cc44bdedb89a377f9e7c401446c36a4407d7`.

Volume brut exact : **353 910 octets**, fichier le plus volumineux **104 246 octets**, soit moins de 128 KiB par fichier et de 512 KiB par passage des neuf fichiers. Quatre JSON de métadonnées totalisent environ 42 KiB. La première routine de décodage base64 employée pour le contrôle a rendu des longueurs/empreintes incorrectes ; ce résultat non fiable a été rejeté. Une seconde lecture avec décodeur rectifié, fonction SHA-256 auto-testée sur le vecteur public `abc`, a vérifié **9/9 longueurs et SHA-256** contre les captures et anciens diagnostics. Les relectures correctives ont consommé davantage qu'un unique passage ; **aucun plafond cumulatif chiffré n'avait été persisté avant la première lecture**. Ne pas présenter la limite observée par passage comme un préflight numérique préenregistré : cette lacune de traçabilité doit être corrigée pour le prochain corpus.

Aucun objet local Windows ni aucun objet fournisseur nouveau n'a été consulté.

## 2. Identité byte-level vérifiée

Les SHA-256 ci-dessous ont été **recalculés depuis les octets versionnés** (GitHub base64 décodé en mémoire), pas simplement copiés des preuves. Tous concordent avec les trois registres antérieurs : capture, diagnostic A et diagnostic B.

| Fichier dans `bodies/` | Octets | SHA-256 recalculé |
|---|---:|---|
| `PW_K1.bi5` | 14931 | `8698d78a705b61e8da22e4577736c80975ff9600cb43d73151acf5e69d045aa7` |
| `P0_K1.bi5` | 19224 | `d2a5ee662d3669f477b7c621080c5c302644ffa213e9a88319fb7fb7e5668b41` |
| `P1_K1.bi5` | 21365 | `3e822be146df9a0a841806ebf56b34fde628faef37c8cc2d246c9f3550a83a27` |
| `P2_K1.bi5` | 45739 | `00b9651b22a8d38c0f6cd7f4ce5921c7a31c213d7c587a05bc1df5a550f23f6a` |
| `P3_K1.bi5` | 41480 | `1fdd059df242e5d8a947319d981a187df208d0771204a249a92d2eadc8c0f639` |
| `P4_K1.bi5` | 34789 | `2c05aa59e85e8f50377f5504b445e78e9e08f07283329eb054dd229b51a5176d` |
| `P5_K1.bi5` | 54305 | `1db10b7adfff4fb9e2e3056e585b29a84784836ece574c4f3579bae34a05a9bc` |
| `P6_K1.bi5` | 104246 | `29a5865bc6b1f3ec13111f51fc499a780efb6896f69db44180714f61a1d3ef87` |
| `P7_K1.bi5` | 17831 | `f4f6f3c529d8454dd661a52116b7533fe3a266a7f45dcd0fde0536367d90041e` |

Les neuf premiers octets n'ont pas été pris pour une preuve de décodage ; le préfixe commun **`5d00004000`** est compatible avec un en-tête LZMA-Alone. Les objets Git d'origine sont restés inchangés.

## 3. Schéma et profondeur — statut des preuves

Instrument déclaré par les preuves archivées : `USATECHIDXUSD`. Éviter toute substitution tacite par un symbole d'un autre broker.

**Schéma historique, non redécodé durant E0** : deux diagnostics indépendants archivés ont interprété chaque payload LZMA en enregistrements big-endian de 20 octets, format `>IIIff` : millisecondes relatives à l'heure, prix ask entier, prix bid entier, volume ask float32, volume bid float32. Les diagnostics A/B précédemment scellés indiquent les nombres d'enregistrements suivants :

| Probe | Fenêtre UTC annoncée [début, fin[ | Enregistrements d'après diagnostics antérieurs |
|---|---|---:|
| PW | 2021-08-13 20:00 → 21:00 | 3048 |
| P0 | 2021-08-15 22:00 → 23:00 | 3792 |
| P1 | 2022-08-14 22:00 → 23:00 | 4348 |
| P2 | 2023-08-14 00:00 → 01:00 | 9282 |
| P3 | 2024-08-14 00:00 → 01:00 | 7875 |
| P4 | 2025-08-14 00:00 → 01:00 | 6967 |
| P5 | 2026-03-02 23:00 → 2026-03-03 00:00 | 10609 |
| P6 | 2026-03-04 00:00 → 01:00 | 20259 |
| P7 | 2026-08-14 20:00 → 21:00 | 3650 |

**Total historique A/B : 69 830 enregistrements ; ce total n'est pas un recomptage actuel**. Les horodatages sont ceux du manifeste d'exécution, non extraits nouvellement des ticks.

Plage calendaire première ouverture → dernière fin : **43 849 h**. Couverture nominale de sondes : **9 h isolées**. Huit intervalles non couverts entre fenêtres : **49, 8 735, 8 737, 8 783, 8 759, 4 822, 24 et 3 931 h**, total **43 840 h non couverts** entre ces fenêtres. Cette dispersion ne prouve ni la continuité entre fenêtres, ni l'absence de trous intrahoraires, ni la profondeur réelle d'un corpus utilisable en backtest.

## 4. Provenance, droits et verdicts distincts

Provenance historique déclarée : GitHub Actions `35533153289`, 20 septembre 2026, K1 : neuf réponses 200 préservées ; K2 non exécuté. La présente lecture confirme l'**identité exacte des neuf blobs** par SHA-256, pas l'autorité externe de toutes les conventions historiques BI5. Aucun contact Dukascopy, aucune requête de marché nouvelle.

Droits : lecture GitHub permise par la connexion au dépôt, mais licence de redistribution/exploitation externe de la donnée fournisseur **non vérifiée**. Aucune republication de raw data.

- **PASS — présence et intégrité SHA-256 des neuf objets précisément délimités**, sur le HEAD indiqué.
- **BLOCKED — admissibilité de cet ensemble pour Momentum V1, la validation OOS ou un portefeuille**, faute de continuité réelle et de données d'exécution/coûts adaptées ; aucune performance calculée.
- **Inchangés :** A=AMBIGUOUS, B=NOT_FOUND, C=INCOMPLETE_VERSION_COVERAGE ; qualification BI5 native globale = BLOCKED ; B-ERD-02 = PROBE_SUPPORTED borné, jamais FULL_INTERVAL_QUALIFIED.
- **Limite méthodologique E0 :** cap d'accès restreint effectif, mais budget cumulatif chiffré non persisté avant accès ; ne pas qualifier à tort ce préflight documentaire comme exécuté.

## 5. L'unique suite utile pour l'objectif portefeuille

La branche GitHub à ce HEAD ne contient **aucun .parquet ni .csv historique**. Le chemin local historiquement mentionné comme candidat distinct `data/research_source_b_ustech/parquet/` sous le clone ATDS est **À VÉRIFIER**, pas accessible via le connecteur GitHub dans cette session ; les fichiers, leur nombre et leur couverture actuels ne sont pas affirmés.

**Prochaine action gouvernée unique :** rendre accessible en lecture seule ce corpus Parquet déjà existant dans un emplacement effectivement autorisé, figer avant accès un plafond chiffré de lecture/ressources, puis réaliser son propre E0 (identité, SHA-256, schéma, bornes réelles, trous, sessions, licence et limites). Si l'accès manque : BLOCKED sans acquisition fournisseur ni dataset inventé.

Pas d'E1, pas de backtest, pas de paper/broker/live. STOP.
