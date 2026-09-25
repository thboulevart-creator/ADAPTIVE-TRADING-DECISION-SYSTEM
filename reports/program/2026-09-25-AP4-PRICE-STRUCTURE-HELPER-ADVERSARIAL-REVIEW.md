# AP4 — revue adversariale et re-break du candidat persisté
Date : 2026-09-25
Fresh HEAD et candidat relu : cc329b3cbe55c24072d6382aee600a5509eb4609.
Helper tools/ap4_price_structure.py : blob 6931712c06e7ed912266782487ed7813cd0be1ff.
SHA-256 f957b38a252ffb2649602fdc5405b82735c88300e1f32cc9fee5f41834098987.
Tests tests/test_ap4_price_structure.py : blob b439386288e94fe0ddd002ff5ed60aa28d199a71.
SHA-256 b4f34febc9a1e5f4205a9cfb214074736bb1e81e50f129527fa6f1d3b8cfe0f3.
Les deux fichiers ont été relus à ce commit et comparés exactement aux octets testés, avant re-break.
Même assistant producteur et auditeur : pas d'indépendance revendiquée.

## Résultats exécutés
python -m unittest discover -s tests -p test_ap4_price_structure.py -v : 9 tests PASS.
python -m py_compile tools/ap4_price_structure.py : PASS.
tests/run_ap4_mutation_breakers.py : 6/6 mutants détectés.
Le runner vérifie que neuf tests sont réellement exécutés et qu'une erreur de chargement ne compte pas comme mutant tué.
Résultats mutants dans reports/program/evidence/2026-09-25-AP4-MUTATION-RESULTS.json.

## Attaques et preuves
- Signe : invalidité/gap/segment coupent ; zéro conservé, dénominateur non nul séparé.
- Runs : zéro coupe ; conservation des retours non nuls.
- Fenêtres 15/60 : oracle à boucles sur 301 prix synthétiques, seed 974 ; même segment et minutes adjacentes.
- High/low précédent : oracle max/min Python ; minute courante exclue, égalité non franchissante.
- Efficacité : oracle somme de retours ; fenêtres plates exclues ; aucune division par zéro.
- Réintégration : range de l'événement figé ; bornes inclusives ; +1/+15 ; +16 hors horizon ; saut complet du range non réintégré ; fin/gap censurés ; événement réintégré avant gap conservé.
- Oracle réintégration séparé sur 200 observations synthétiques seed 42.
- Analyse agrégée synthétique complète : saut de prix entre deux segments exclu des mouvements continus et conservé dans reopen.
- Bindings AP0/AP3 contrefaits rejetés avant lecture Parquet.
- Output dans corpus, existant ou lien symbolique rejeté ; octets input inchangés.
- 6 mutants : inclusion minute courante, fenêtres traversant gap, zéros dans runs, franchissements inclusifs, réintégration traversant gap, rejet des nulls AP0 légitimes.

## Défauts rencontrés et corrections
1. Le candidat non persisté rejetait tout null. Lecture ciblée du producteur AP0 : gap_before_ms est null hors frontière >60s, y compris première ligne. Correction avant commit candidat ; test positif et deux tests négatifs.
Cette lecture de contrat n'est pas une réouverture de la qualification AP0.
2. Premier runner durable de mutation exigeait une AssertionError. Le mutant rejetant les nulls légitimes produit correctement ValueError pendant deux tests positifs. Runner initial FAIL ; correction étroite acceptant uniquement cette erreur identifiée, puis re-break 6/6.
Le helper n'a pas été modifié lors de cette correction du runner.

## Revue statique
- Hash AP0 manifest/AP3 et chaque Parquet avant et après lecture ; schéma/type/métadonnées, ordre, enveloppes OHLC, liaison gaps/segments.
- Extraction des colonnes AP0 bornée ; 61 fichiers, 91 734 766 octets exacts.
- Output création exclusive ; jamais écrasé même en erreur.
- Aucun volume, prix d'exécution, fill, trade, PnL ou sweep.
- Fenêtres chevauchantes et franchissements successifs : pas d'indépendance des observations.
- Réintégrations utilisent des observations futures : explicitement déclarées, pas de labels prédictifs exportés.
- Swings élémentaires 1m : aucune prétention de pivots universels.
- Par année : retours affectés par endpoint ; paires seulement si les deux endpoints sont dans l'année. Une paire trans-annuelle peut donc être absente des buckets annuels sans perte globale.
- AP6 nécessaire ; stabilité non qualifiée ici.

## Limites
PyArrow absent des deux runtimes Python vérifiés dans cette session ; corpus AP0 absent.
Lecture réelle Parquet, mémoire maximale et temps réel sur corpus : BLOCKED jusqu'à l'exécution locale.
Aucun résultat sur le corpus AP4 n'est revendiqué. Les tests du loader portent sur le rejet précoce des hashes ; la lecture PyArrow réussie n'est pas testée ici.
Les tests Windows des reparse points n'ont pas été exécutés ; contrôle statique seulement. Le test symlink est Linux.
Pas de protection absolue contre modifications hostiles concurrentes des parents de fichiers par un autre processus.
La vérification pré/post de hash couvre une dérive ordinaire mais n'est pas une attestation du poste.

## Verdict
PASS — candidat suffisamment borné et testé pour une tentative locale AP4.
BLOCKED — qualification AP4 sur corpus en attente du JSON exact.
Prochaine action unique : exécution locale du helper exact, puis transfert du JSON.
