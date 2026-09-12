# Contrat d'implémentation — Méta-gouvernance et auto-contestation

**Statut :** CONTRAT ARCHITECTURAL — à satisfaire avant de considérer la méta-gouvernance opérationnelle
**Date :** 12 septembre 2026
**Référence normative :** `GOVERNANCE/META-GOVERNANCE-AND-SELF-CHALLENGE.md`

## Objectif

Transformer la méta-gouvernance en mécanismes observables, testables et auditables. La présence du document de gouvernance seule ne constitue jamais une preuve d'implémentation.

## Gâtes d'acceptation

1. **Finalité** — le système peut détecter une dérive entre valeur réelle recherchée et proxy optimisé.
2. **Hypothèses** — les hypothèses critiques sont identifiables, versionnées et associées à leur contexte.
3. **Réfutation** — chaque connaissance/stratégie critique dispose d'une méthode explicite de recherche de contre-exemple.
4. **Anomalies** — les écarts significatifs entre attente et observation peuvent déclencher une investigation.
5. **Provenance** — toute connaissance critique peut remonter jusqu'à ses observations, expériences, résultats et preuves.
6. **Validité** — domaine de validité, confiance et conditions d'invalidation sont conservés.
7. **Drift** — les changements susceptibles d'invalider une connaissance peuvent être détectés ou, à défaut, explicitement déclarés non couverts.
8. **Promotion** — apprentissage et autorisation opérationnelle sont séparés par un gate vérifiable.
9. **Arrêt** — des critères explicites permettent de suspendre, rétrograder ou abandonner une hypothèse/évolution.
10. **Audit adversarial** — chaque gate peut être cassé et son verdict est exclusivement PASS / FAIL / BLOCKED.

## Règle de verdict

- **PASS** : preuve exécutable et satisfaisante.
- **FAIL** : mécanisme exécuté mais violation démontrée.
- **BLOCKED** : contrôle non exécutable ou preuve insuffisante pour conclure.

**BLOCKED ne devient jamais PASS par interprétation.**

## Principe de progression

Le contrat doit être intégré au système existant avec le minimum de nouvelles structures nécessaires. Toute nouvelle structure doit être justifiée par un manque démontré dans l'architecture actuelle.

La séquence obligatoire est :

**CARTOGRAPHIE → CANDIDAT MINIMAL → TEST ADVERSARIAL → CORRECTION → RE-CASSAGE → VERDICT**.

Tant que les gates ne disposent pas de preuves exécutables, l'implémentation globale reste **NON VALIDÉE**.
