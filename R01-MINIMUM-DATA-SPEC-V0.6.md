# R01-MINIMUM-DATA-SPEC-V0.6 — FINAL NORMATIVE CLOSURE

**Statut : GELÉE**  
**Périmètre : R01 — reclassification des CASE-01 → CASE-18**  
**Version : V0.6**

## 1. Objet

Cette version constitue la fermeture normative finale de deux zones ciblées identifiées lors des audits de `R01-MINIMUM-DATA-SPEC-V0.5` :

1. la distinction entre `AMBIGU` et `INSUFFISANT` lorsque l'origine ou la destination sont vagues ;
2. le traitement des informations extérieures au MDS lorsqu'elles sont liées à une contrainte opérationnelle.

Aucune autre partie du MDS, de la taxonomie ou des CASE-ID n'est modifiée par V0.6.

---

## 2. RÈGLE 1 — STRUCTURE ORIGINE → DESTINATION

La structure fondamentale du trajet est évaluée uniquement selon sa présence textuelle.

### 2.1 Structure PRÉSENTE

Une structure `origine → destination` est **PRÉSENTE** dès lors que le texte exprime une relation de déplacement entre une origine et une destination.

La structure reste **PRÉSENTE**, indépendamment du niveau de précision des deux valeurs.

Cela inclut notamment les cas où :

- l'origine est précise ou vague ;
- la destination est précise ou vague ;
- l'une des deux valeurs est générale ;
- les deux valeurs sont générales ;
- la localisation ne permet pas encore de satisfaire pleinement M2 ou M3.

Le caractère vague ou insuffisamment précis d'une origine ou d'une destination affecte l'évaluation de la dimension MDS correspondante, mais **ne transforme pas la structure origine → destination de PRÉSENTE en ABSENTE**.

### 2.2 Structure ABSENTE

La structure origine → destination est **ABSENTE** uniquement lorsque le texte n'exprime pas de relation de déplacement entre une origine et une destination.

L'absence de précision géographique ne constitue donc pas, à elle seule, une absence de structure.

### 2.3 Conséquence sur `AMBIGU` / `INSUFFISANT`

Une imprécision géographique, même importante, ne peut à elle seule justifier `INSUFFISANT` par absence de structure origine → destination lorsque cette relation est explicitement présente dans le texte.

Dans ce cas, les valeurs concernées sont évaluées selon M2/M3 et le verdict final est déterminé par la hiérarchie normative déjà gelée.

---

## 3. RÈGLE 2 — INFORMATION EXTÉRIEURE AU MDS

Une information extérieure au MDS ne peut affecter l'évaluation d'une dimension MDS existante que si le texte établit **explicitement** une dépendance entre cette information et la détermination de cette dimension.

Les trois conditions suivantes sont cumulatives :

1. l'information extérieure est explicitement exprimée dans le texte ;
2. le texte établit explicitement son lien avec une dimension MDS existante ;
3. le texte établit explicitement que cette information est nécessaire à la détermination de cette dimension MDS.

Si l'une de ces trois conditions n'est pas satisfaite, l'information reste extérieure au MDS et ne modifie pas le verdict R01.

### 3.1 Interdiction de déduction opérationnelle

Il est interdit de considérer qu'une information extérieure affecte une dimension MDS uniquement parce qu'elle serait :

- utile à l'exploitation ;
- utile à la tarification ;
- utile à la vérification de faisabilité ;
- utile au choix d'un véhicule ;
- utile à l'organisation opérationnelle ;
- normalement demandée par un professionnel du transport ;
- pertinente selon les connaissances métier de l'analyste.

L'utilité opérationnelle, commerciale ou métier **ne constitue pas une dépendance normative au MDS**.

### 3.2 Conséquence

Une contrainte telle que « véhicule adapté », « véhicule disponible », « faisabilité », « tarif » ou toute autre donnée extérieure ne devient pas une exigence MDS par simple utilité ou pertinence opérationnelle.

Elle ne peut affecter une dimension MDS que si le texte lui-même établit explicitement que cette information est nécessaire pour déterminer cette dimension.

Aucune nouvelle dimension MDS ne peut être créée par cette règle.

---

## 4. APPLICATION AU PÉRIMÈTRE R01

V0.6 ne modifie pas :

- les dimensions M1 → M6 ;
- la taxonomie des verdicts ;
- la hiérarchie `INSUFFISANT > AMBIGU > INFORMATION MANQUANTE > TRAITABLE` ;
- le caractère conditionnel de M6 ;
- les règles de référence temporelle ;
- la séparation entre qualification R01 et étapes post-R01 ;
- les CASE-01 → CASE-18.

V0.6 ferme uniquement les deux zones définies aux sections 2 et 3.

---

## 5. STATUT NORMATIF

À l'issue de l'audit ciblé final, aucune contradiction normative ni non-reproductibilité réelle n'a été démontrée sur ces deux règles pour les `CASE-01` à `CASE-18`.

Un cas limite linguistique hypothétique hors du jeu R01 ne constitue pas un motif de blocage de la reclassification.

**V0.6 est donc gelée pour `R01-RECLASSIFICATION-03`.**

**Prochaine étape autorisée : `R01-RECLASSIFICATION-03` sur `CASE-01 → CASE-18`.**
