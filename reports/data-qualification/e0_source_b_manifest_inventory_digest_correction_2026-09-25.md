# E0-SOURCE-B — correction du digest canonique d'inventaire

Date : 2026-09-25  
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branche : `integration/system-v1`  
HEAD avant persistance : `7a4cb211cef943083f65c0bf09ed7fd6a5256e40`

## Incident

La tentative locale F0 a produit :

```text
BLOCKED_MANIFEST_BINDING
canonical inventory digest mismatch:
5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf
!=
c6baf5c42808317167b5dc60c88d86b4481b3d0004565bc3a7b33d54ef13ea54
```

Le breaker a donc fonctionné comme prévu et F0 n'a pas poursuivi.

## Vérification de l'identité du manifest

Le fichier exact joint antérieurement à la session a été retrouvé et relu.

Résultats :
- taille : **86 752 octets** ;
- SHA-256 exact : `c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5` ;
- schéma : `ATDS_E0_SOURCE_B_ACCESS_MANIFEST_V0_1` ;
- statut : `MANIFEST_COMPLETE` ;
- 212 entrées `inventory.files` ;
- somme `size_bytes` : **3 936 721 231 octets**.

Le SHA-256 exact correspond à l'ancre déjà scellée. Le manifest local utilisé par F0 n'a donc pas été substitué ni modifié.

## Recalcul du digest déclaré

Formule explicitement annoncée :

```text
relative_path<TAB>size_bytes<TAB>sha256<LF>
```

appliquée successivement aux 212 entrées dans l'ordre du manifest.

Deux implémentations indépendantes de construction du flux ont été exécutées :
1. construction de chaque ligne complète puis concaténation ;
2. alimentation incrémentale du SHA-256 champ par champ et séparateur par séparateur.

Les deux donnent exactement :

`5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf`.

Le digest historique :

`c6baf5c42808317167b5dc60c88d86b4481b3d0004565bc3a7b33d54ef13ea54`

est donc **ERRONÉ** pour la formule publiée.

## Cause et portée

La cause est une erreur dans l'adjudication assistant du 2026-09-24 lors de la production du digest secondaire. Elle n'affecte pas :
- le SHA-256 exact du JSON manifest ;
- les 212 SHA-256 individuels contenus dans le manifest ;
- les tailles ;
- les contrôles PAR1 ;
- `snapshot_stable` ;
- `sha256_complete` ;
- `parquet_magic_checked`.

Elle affecte uniquement le **digest auxiliaire d'inventaire dérivé** et tous les artefacts ultérieurs qui ont repris la valeur `c6baf5...`.

## Correction

Valeur correcte et normative pour le helper F0 courant :

`5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf`.

Le helper `tools/e0_source_b_footer_census.py` a été corrigé pour cette valeur, sans relâcher le contrôle du SHA-256 exact du JSON.

## Verdict

**PASS — correction du digest auxiliaire.**

**FAIL historique ciblé — la valeur `c6baf5...` ne doit plus être utilisée comme digest canonique de l'inventaire.**

Le breaker local ayant refusé la divergence avant toute lecture footer F0, aucune preuve F0 n'est contaminée.

## Suite

Re-break du helper corrigé contre le manifest exact scellé, puis nouvelle tentative locale F0.

Aucun F1, E1, backtest, MT5, paper/broker/live n'est ouvert.

## Re-break du binding corrigé

Le manifest exact scellé a été relu et le même contrat de validation que le helper F0 a été rejoué.

Contrôles PASS :
- SHA-256 JSON exact = `c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5` ;
- schema exact ;
- `MANIFEST_COMPLETE` ;
- 212 fichiers et 212 entrées ;
- total = 3 936 721 231 octets ;
- `sha256_complete=true` ;
- `parquet_magic_checked=true` ;
- `snapshot_stable=true` ;
- chemins uniques ;
- 212 SHA-256 individuels syntaxiquement valides avec status PASS ;
- digest canonique recalculé = `5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf`.

Résultat :

`CORRECTED_BINDING_REBREAK_PASS`.

La nouvelle tentative F0 peut donc être exécutée avec le helper corrigé.