# V4.3.3 — Research ↔ Execution Compatibility
## Conclusion expérimentale

**Version :** V4.3.3
**Date :** 2026-09-11
**Instrument Research :** Dukascopy USATECHIDXUSD
**Instrument Execution :** VT Markets NAS100.s
**Scope :** comparaison contrôlée sur fenêtre commune d'une heure
**Verdict global : UNVERIFIED**

---

## 1. Objet

V4.3.3 corrige la séparation entre :

1. l'admissibilité du corpus Research à long terme ;
2. la validité technique du pilote Research ↔ Execution exécuté sur une fenêtre commune ;
3. la validation de compatibilité entre les deux feeds.

Cette séparation évite qu'un échec de couverture du corpus Research soit artificiellement interprété comme une incompatibilité entre les deux sources.

---

## 2. Données réellement comparées

### Research

Source locale :

`data/dukascopy_research_a/ticks/USATECHIDXUSD/dukascopy_usatechidxusd_2025-08-15_14h_ticks.bi5`

Format :

`DUKASCOPY_BI5`

Fenêtre observée :

- début : `2025-08-15T14:00:00.008Z`
- fin : `2025-08-15T14:59:59.923Z`

Le fichier pilote ne représente qu'une heure de données.

### Execution

Source locale extraite depuis MT5 :

`reports/data-qualification/v4_3_execution_probe/mt5_NAS100s_2025-08-15_14h_ticks.csv`

Format :

`MT5_NATIVE_CSV`

Fenêtre observée :

- début : `2025-08-15T14:00:00.010Z`
- fin : `2025-08-15T14:59:58.286Z`

Les deux sources sont conservées séparément.

Aucun dataset n'a été fusionné, splicé ou réécrit.

---

## 3. Verdicts

| Gate | Verdict |
|---|---|
| Research corpus admissible ≥ 5 ans | **FAIL** |
| Research pilot data valid | **PASS** |
| Execution data valid | **PASS** |
| Transfer validation | **UNVERIFIED** |
| **Verdict global expérimental** | **UNVERIFIED** |

Le `FAIL` du corpus Research signifie uniquement que le fichier Research local utilisé pour ce pilote ne fournit pas les ≥5 années requises.

Il ne signifie pas que les données Research du pilote sont structurellement invalides.

---

## 4. Ce qui est démontré

Le pilote démontre que V4.3 sait lire et contrôler les deux formats natifs sans forcer leur conversion vers un schéma artificiel :

- Dukascopy BI5 ;
- MT5 native CSV.

Les contrôles d'accès, d'intégrité et d'ordre du pilote sont valides.

La fenêtre commune existe.

Les timestamps sont interprétés explicitement en UTC pour ces deux sources.

La frontière d'exécution précédemment qualifiée en V4.2 reste distincte de la comparaison Research.

---

## 5. Ce qui n'est pas démontré

V4.3.3 ne démontre pas :

- l'équivalence tick-for-tick ;
- l'équivalence statistique globale des feeds ;
- l'équivalence des trajectoires de prix sur plusieurs années ;
- la compatibilité suffisante pour transférer automatiquement une stratégie Research vers VT Markets ;
- la conformité du corpus Research local au minimum de cinq ans.

Aucun seuil d'équivalence statistique n'a été inventé.

La validation de transfert reste donc **UNVERIFIED**.

---

## 6. Interprétation du verdict

Le verdict **UNVERIFIED** est volontairement fail-closed.

Il signifie :

> Le pilote est techniquement exploitable et les deux sources présentent des données valides sur la fenêtre contrôlée, mais les preuves disponibles sont insuffisantes pour déclarer la compatibilité Research ↔ Execution comme établie.

Il serait incorrect de transformer ce résultat en PASS.

Il serait également incorrect de transformer le FAIL de couverture Research en preuve d'incompatibilité des feeds.

---

## 7. Garde-fous méthodologiques

V4.3.3 respecte les principes suivants :

- aucune fusion des datasets ;
- aucune réparation silencieuse ;
- aucun tri silencieux ;
- aucune déduplication silencieuse ;
- aucun timezone guessing ;
- aucune fabrication de volumes bid/ask pour MT5 ;
- aucun seuil d'équivalence inventé ;
- aucune promotion de UNVERIFIED ou BLOCKED vers PASS ;
- Research et Execution restent deux vérités de données distinctes.

---

## 8. Conclusion

**V4.3.3 est un pilote techniquement valide mais insuffisant pour certifier la compatibilité Research ↔ Execution.**

La prochaine phase doit donc porter sur l'augmentation de la preuve, et non sur la fabrication d'un verdict positif :

1. disposer d'un corpus Research ≥5 ans effectivement qualifié ;
2. définir explicitement les critères d'acceptation de transfert ;
3. tester ces critères adversarialement ;
4. mesurer la compatibilité sur plusieurs périodes et régimes ;
5. maintenir la séparation entre Research Truth et Execution Truth.

**Verdict final V4.3.3 : UNVERIFIED.**
