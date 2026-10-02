# P5-E V0.1 — BB1 NORMATIVE GUARD COVERAGE — SELF-CONTAINED EXTERNAL RE-REVIEW PACKET

Date: 2026-10-02

## Independent reviewer mandate

Perform a new independent adversarial review of:

`P5-E V0.1 — BB1 NORMATIVE GUARD COVERAGE CLOSURE`

A prior external re-review returned `FAIL` with one blocking finding:

`BB1 — normative contract leaves could drift without breaking the P5-E targeted tests.`

The prior external return is embedded in this packet.

Do not assume access to prior conversation context.

Do not authorize real execution or human adoption.

## Maximum claim under review

`P5E_V0_1_BB1_NORMATIVE_GUARD_CLOSURE_CANDIDATE_QUALIFIED_FOR_EXTERNAL_REREVIEW`
Explicitly NOT claimed:
- real P5-E end-to-end qualification;
- continuous synchronization qualification;
- a real 60-second SLA;
- per-transient-tip detection SLA;
- automatic evaluation;
- automatic promotion;
- automatic publication;
- real observation-adapter behavior;
- ancestry-classifier correctness.

## Candidate identity

Governed executable HEAD:
`647edf62723fa84c7260c0ea3b25c074f180604f`

Corrected contract blob:
`7e3e18ba946246065b43bc5fbabdc35980140eb9`

Corrected model blob:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`

Corrected evidence matrix blob:
`88e13a447a96455d4ac1d9d0f96e11b29329616d`
Observer-tick behavioral test blob:
`f5b4bca7524f74f221927d1ec389e23d607d1eee`

P5-E adversarial test blob:
`16b6fdb9c0bb5be980e5db59eb6f87f93e160205`

Evidence-matrix test blob:
`182a7b60b440ddb8d5c0c9fdc65f423309383244`

BB1 closure test blob:
`ed4a2c3d9c67f2d67d32b632bfa5c25d36cd0880`

P5-D4 runtime blob:
`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

## Candidate evidence claims to audit

```text
BB1 RED = demonstrated
TARGETED GREEN = 133 / 133 PASS
POST-CORRECTION P5-E BASELINE = 51 / 51 PASS
CONTRACT LEAF MUTATIONS = 161
SURVIVING CONTRACT MUTATIONS = 0
TARGETED PREDECESSOR REGRESSION = 282 / 282 PASS
FULL DISPOSABLE-CLONE OBSIDIAN SUITE = 1486 / 1486 PASS
REAL P5D4 CONTROL FINGERPRINT = UNCHANGED
```
Treat persisted reports as claims to audit, not as authority.

## Required BB1 closure questions

1. Do all 23 originally surviving normative leaves now fail strict mutation?
2. Did the closure introduce any new normative leaf that can drift without detection?
3. Can the original combined BB1 regression still survive?
4. Does the evidence matrix bind the exact contract blob?
5. Does it bind the exact model blob?
6. Does changing either covered object invalidate the matrix?
7. Does any alternative contract/model path bypass that binding?
8. Is the leaf-mutation method sufficient to falsify the claimed guard coverage?
9. Are non-normative/historical metadata correctly separated from behavioral authority?
10. Can declarative PASS labels still launder an unexecuted semantic property into qualification?

## NB1 questions

11. Does a terminal read from 30 to 61 fail closed as `ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT`?
12. Is completion exactly at the next slot boundary handled consistently?
13. Do multi-observation overlaps remain fail-closed without hiding cadence defects?
14. Can an overrun be laundered by a later exact target observation?
## NB4 questions

15. Is unobserved-tip non-injection now clearly a future adapter rule rather than a currently qualified runtime property?
16. Does any report still overclaim implemented queue protection for an adapter that does not exist?

## NB6 questions

17. Do queue-capacity replacement/coalescing mappings now point to behavioral P5-D4 evidence?
18. Does pending-non-active FIFO/no-retarget mapping now point to a semantically exact D2 test?
19. Are evidence_kind labels accurate?

## NB7 questions

20. Is `INCOMPLETE_SYNTHETIC_WINDOW` explicitly NON-PASS?
21. Is duplicate-slot handling semantically distinct from `CADENCE_GAP`?
22. Did the cleanup create any new unguarded failure code or claim?

## Additional adversarial mandate

Try to break the candidate beyond the listed cases.
At minimum test:
- mutation of every scalar/list contract leaf;
- combined mutation of multiple BB1 timing/source/queue leaves;
- contract change after matrix construction;
- model change after matrix construction;
- source repository/remote/branch drift;
- latency-definition drift back to remote-availability semantics;
- wall-clock promotion to normative timing;
- stage-list truncation;
- removal of human/external-review gate;
- removal of future-adapter-rule qualification boundaries;
- duplicate fixed-rate slots;
- terminal read overrun;
- read completion exactly at 60-second bound;
- read completion exactly on next fixed-rate slot;
- evidence-matrix method/path/blob mismatch;
- authority leakage into evaluation, Stage A/B, promotion, publication, Vault mutation, P6, daemon/task/service registration.

Also inspect deferred NB2/NB3/NB5/NB9 only to ensure this closure did not silently claim to solve them.

## Required output

Return exactly one top-level verdict:

`VERDICT = PASS | PASS_WITH_NON_BLOCKING_NOTES | FAIL`
Then provide:
- BLOCKING_FINDINGS
- NON_BLOCKING_FINDINGS
- BB1_NORMATIVE_GUARD_CHECK
- CONTRACT_MODEL_BINDING_CHECK
- NB1_FIXED_RATE_OVERRUN_CHECK
- NB4_CLAIM_SCOPE_CHECK
- NB6_EVIDENCE_MAPPING_CHECK
- NB7_NON_PASS_SEMANTICS_CHECK
- AUTHORITY_LEAKAGE_CHECK
- CLAIM_SCOPE_CHECK
- MISSING_ADVERSARIAL_CASES
- RECOMMENDED_TARGETED_CORRECTIONS

For every finding:
- cite the exact packet section;
- name the exact field/function/test/matrix entry;
- distinguish OBSERVED reproduction from INFERENCE;
- label it BLOCKING or NON_BLOCKING;
- provide a minimal falsification case where possible.

This review is not human normative adoption.

This review does not authorize any real P5-E execution.

---

# SOURCE: PRIOR EXTERNAL REREVIEW CLAUDE RETURN

Path: reports/program/2026-10-01-OBSIDIAN-P5E-V0.1-TARGETED-CLOSURE-EXTERNAL-REREVIEW-CLAUDE-RETURN.md
~~~~
VERDICT = FAIL

J'ai reconstruit localement les 17 artefacts code et JSON du paquet. Toutes les identitÃ©s de blob annoncÃ©es correspondent (contrat `b0668b4â€¦`, modÃ¨le `b783717â€¦`, tests `a4fbd35â€¦`, `3c0f556â€¦`, `15c3e44â€¦`, `ff9db4câ€¦`, matrice `0440175â€¦`, ainsi que D2 `fd212f6â€¦`/`9c472a3â€¦` et D4 `1825e53â€¦`/`5bcc563â€¦`). La surface P5-E ciblÃ©e tourne Ã  50/50 OK et D2 Ã  54/54 OK. D4 runtime passe 16/17 avec un `USERPROFILE` simulÃ© ; `test_00` Ã©choue seulement parce que la prÃ©registration D4 n'est pas embarquÃ©e (cause environnementale). Les 23 tests distincts rÃ©fÃ©rencÃ©s par la matrice passent tous.

Le FAIL repose sur un seul dÃ©faut bloquant. Il est dÃ©montrÃ©, il porte sur un critÃ¨re prÃ©registrÃ©, et sa correction est mÃ©canique.

### BLOCKING_FINDINGS

**BB1 â€” La clÃ´ture B1 est incomplÃ¨te : on peut rÃ©introduire exactement le dÃ©faut B4 sans qu'aucun des 50 tests ne casse.** (OBSERVÃ‰)

*OÃ¹ :*

- Â« TARGETED CLOSURE PREREGISTRATION Â», `coverage_closure.adversarial_invariants_must_cover_all_normative_contract_blocks: true` ;
- Â« CORRECTED P5-E ADVERSARIAL TESTS Â», `assert_contract_invariants` ;
- Â« CORRECTED P5-E BASE TESTS Â», `test_real_latency_metric_is_falsifiable_and_local_monotonic` ;
- Â« TARGETED CLOSURE QUALIFICATION Â», Â§B1 (Â« The former P5-E invariant gaps were closed Â», bloc Â« timing Â» dÃ©clarÃ© gardÃ©).

*Falsification minimale.* J'applique simultanÃ©ment les mutations suivantes au contrat :

- `near_real_time_timing.detection_latency_definition` revient Ã  l'ancienne valeur `FIRST_SUCCESSFUL_EXACT_REMOTE_HEAD_OBSERVATION_TIME_MINUS_SOURCE_HEAD_AVAILABLE_TIME` ;
- `future_real_bound_clock = "WALL_CLOCK"` ;
- `future_real_wall_clock_may_be_recorded_as_evidence_only = false` ;
- `latency_bound_breach_must_not_be_reported_as_near_real_time_pass = false` ;
- `monitored_source.branch = "main"` ;
- `burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification = false`.

RÃ©sultat : `Ran 50 tests â€¦ OK`.

*Balayage exhaustif.* J'ai mutÃ© chaque feuille du contrat une par une (inversion de boolÃ©en, entier +1, chaÃ®ne remplacÃ©e par "MUTATED", liste raccourcie), soit 154 mutations. 36 survivent. Parmi elles, des champs normatifs :

- `monitored_source.{remote, branch, canonical_authority, local_working_tree_is_not_authority}` ;
- `near_real_time_timing.{detection_latency_definition, future_real_bound_clock, future_real_wall_clock_may_be_recorded_as_evidence_only, latency_bound_breach_must_not_be_reported_as_near_real_time_pass}` ;
- `head_transition_policy.{initial_headâ€¦, fast_forward_headâ€¦}_under_existing_p5d2_semantics` ;
- `queue_and_supersession.burst_catch_up_claim_forbiddenâ€¦` ;
- `end_to_end_definition.{real_end_to_end_stages, real_end_to_end_pass_requires_all_authorized_applicable_stages}` ;
- `real_context_evidence_only.{must_not_be_used_as_real_experiment_execution, must_not_be_mutated_by_contract_qualification}` ;
- `tip_visibility_semantics.future_ancestry_enumeration_requires_separate_qualification` ;
- `external_review_targeted_closure.external_rereview_required_before_human_normative_adoption`.

*Pourquoi c'est bloquant :*

- Le contrat porte aujourd'hui deux champs qui dÃ©finissent la latence. Seul `real_latency_metric` est gardÃ© ; `detection_latency_definition` ne l'est pas. Le contrat peut donc redevenir contradictoire sur l'origine de la mesure, ce qui est le cÅ“ur mÃªme de B4.
- Le breaker de clÃ´ture `REMOTE_AVAILABILITY_TIME_TREATED_AS_MEASURABLE_ORIGIN` est donc fermÃ© seulement en partie.
- Aggravant : la matrice n'Ã©pingle ni le blob du contrat ni celui du modÃ¨le. Son test vÃ©rifie les blobs des fichiers de test, pas l'objet couvert. Une dÃ©rive du contrat n'invalide donc pas la matrice.

*Le dÃ©faut est un trou de garde, pas une valeur fausse.* Les valeurs actuelles sont correctes. Le dÃ©faut est l'absence de garde, et c'est exactement la classe de dÃ©faut que B1 devait fermer.

### NON_BLOCKING_FINDINGS

- **NB1 â€” Lecture qui dÃ©borde sur le crÃ©neau suivant.** (OBSERVÃ‰, modÃ¨le `qualify_detection`)&#x20;
  - Cas : `release=1`, `[(30, 61, OBS, A)]` donne `PASS_DETECTED_WITHIN_BOUND` avec une latence de 60. Le crÃ©neau 60 n'a jamais dÃ©marrÃ© pendant la lecture en cours.
  - Contradiction : la prÃ©registration de clÃ´ture exige `all_required_attempt_slots_must_be_present_until_terminal_result` et `overlapping_single_writer_attempts_forbidden`.
  - Pourquoi non bloquant : la latence rapportÃ©e reste vraie.
  - AsymÃ©trie : un Ã©chec qui dÃ©borde n'est bloquÃ© que si un enregistrement suit (E4 donne `CADENCE_GAP`). S'il est le dernier enregistrement (E5), le rÃ©sultat est `INCOMPLETE`.
  - Il faut clarifier le contrat ou le modÃ¨le.
- **NB2 â€” Ordre ambigu non dÃ©tectÃ©.** (OBSERVÃ‰)&#x20;
  - Cas : `release=1`, `[(30, B), (60, A)]` donne PASS avec une latence de 60. La tÃªte B, qui n'est ni la cible ni la tÃªte d'avant la libÃ©ration, a Ã©tÃ© vue aprÃ¨s la libÃ©ration, puis A rÃ©apparaÃ®t.
  - Le modÃ¨le ne connaÃ®t pas la tÃªte attendue avant libÃ©ration. Il ne peut donc pas distinguer une rÃ©plique encore en retard d'un push tiers ou d'un retour arriÃ¨re.
  - Ce n'est pas une impossibilitÃ©, comme l'Ã©tait B3, mais une ambiguÃ¯tÃ© que le contrat classe `BLOCKED` (`unexpected_state_or_timing_ambiguity_result`).
  - Ã€ fermer avant toute prÃ©registration rÃ©elle.
- **NB3 â€” `classify_tip_visibility` sans Ã©tat.** (OBSERVÃ‰ et INFÃ‰RENCE)&#x20;
  - Le fait de contenance est une affirmation passÃ©e par l'appelant, non vÃ©rifiÃ©e par la fonction.
  - Le libellÃ© `CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED` est rendu mÃªme si A a dÃ©jÃ  Ã©tÃ© observÃ©e et mise en file auparavant.
  - Le cas normal Â« pas encore visible Â» (tÃªte observÃ©e = ancÃªtre de la cible) tombe dans `UNRELATED_OR_UNPROVEN_REQUIRES_ADJUDICATION`.
  - La fonction n'est appelÃ©e par aucun chemin de dÃ©cision, d'oÃ¹ le caractÃ¨re non bloquant. Mais si un adaptateur futur la branchait sur la file, elle pourrait mal traiter une tÃªte dÃ©jÃ  en file.
- **NB4 â€” Une partie de la clÃ´ture B5 est dÃ©clarative.** (INFÃ‰RENCE)&#x20;
  - La phrase Â« No unobserved intermediate tip may be injected into the queue Â» (qualification, Â§B5) ne s'appuie sur aucune preuve exÃ©cutable.
  - D2 met en file n'importe quelle tÃªte hexadÃ©cimale de 40 caractÃ¨res Ã©tiquetÃ©e `FAST_FORWARD` (OBSERVÃ‰).
  - Le seul point d'application serait l'adaptateur d'observation futur, qui n'existe pas encore. C'est acceptable Ã  ce stade, Ã  condition de le formuler comme une rÃ¨gle et non comme une propriÃ©tÃ© qualifiÃ©e.
- **NB5 â€” Preuves D2 conditionnÃ©es Ã  une Ã©tiquette fournie par l'appelant.** (OBSERVÃ‰)&#x20;
  - Les tests rÃ©utilisÃ©s `test_non_fast_forward_blocks_without_queueing` et `test_unknown_ancestry_blocks_without_queueing` prouvent le comportement de D2 pour une `transition_class` fournie de l'extÃ©rieur. Ils ne prouvent pas que la classification d'ascendance est correcte.
  - Sonde Aâ†’Bâ†’A : relabelliser H1 en `FAST_FORWARD` aprÃ¨s H2 est acceptÃ©. D2 Ã©met `QUEUE_EXACT_HEAD_FOR_EVALUATION` sans rien ajouter (dÃ©duplication) et `latest_observed_head` rÃ©gresse vers H1.
  - L'ordre FIFO est prÃ©servÃ©, mais la trace d'audit est trompeuse. C'est un comportement de prÃ©dÃ©cesseur, hors pÃ©rimÃ¨tre de la correction.
- **NB6 â€” Ã‰carts sÃ©mantiques dans la matrice.**&#x20;
  - `SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD` et `PENDING_HEAD_RETARGETED_TO_NEWER_HEAD` pointent vers `test_fast_forward_queues_without_retargeting_active`, qui couvre une tÃªte *active*, pas une tÃªte *en attente non active*. Ma sonde montre que la tÃªte en attente non active conserve bien `[H1, H2]` (OBSERVÃ‰) ; le comportement tient, mais la correspondance est inexacte.
  - `QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD` et `QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT` sont Ã©tiquetÃ©s `DIRECT_P5E` alors qu'ils pointent vers une mutation de drapeau (`test_queue_mutations_are_rejected`). La preuve comportementale existe pourtant dans `test_07_queue_capacity_blocks_before_tick`.
- **NB7 â€” Vocabulaire et garde rÃ©siduelle.**&#x20;
  - `INCOMPLETE_SYNTHETIC_WINDOW` est toujours absent du contrat (0 occurrence) ; il faut dÃ©clarer son statut non-PASS.
  - Un doublon de crÃ©neau est codÃ© `CADENCE_GAP` (E11), ce qui est un mauvais libellÃ©.
  - La garde AST est nettement meilleure, mais reste contournable via `getattr(__builtins__, â€¦)`. Le modÃ¨le actuel est pur Ã  la lecture.
- **NB8 â€” Discipline d'Ã©vidence moins stricte que la passe prÃ©cÃ©dente.**&#x20;
  - La passe complÃ¨te a Ã©tÃ© exÃ©cutÃ©e sur un worktree dont seul l'Ã©tat Â« propre Â» est dÃ©clarÃ©, sans clone jetable ni empreinte prÃ©/post de l'Ã©tat rÃ©el. La passe prÃ©cÃ©dente fournissait ces deux Ã©lÃ©ments, et l'anomalie de provenance (cause inconnue) n'est pas rÃ©solue.
  - Je ne peux vÃ©rifier ni les 270 ni les 1474 tests.
- **NB9 â€” PrÃ©conditions du protocole rÃ©el.** (B4, question 14)&#x20;
  - L'instant exact de `CONTROLLED_SOURCE_RELEASE_MONOTONIC` n'est pas dÃ©fini : dÃ©but du push, accusÃ© de rÃ©ception, ou confirmation de mise Ã  jour de la ref ? L'Ã©cart vaut plusieurs secondes sur une borne de 60.
  - L'exigence d'un mÃªme domaine monotone (mÃªme hÃ´te, mÃªme horloge) que le lecteur figure dans l'adjudication, mais pas dans le contrat.
  - La ref utilisÃ©e pour la libÃ©ration contrÃ´lÃ©e et l'autoritÃ© de pousser ne sont pas Ã©numÃ©rÃ©es. Pousser sur `integration/system-v1` reviendrait Ã  muter la source canonique.
  - Ces points ne sont pas bloquants pour le candidat, mais obligatoires avant toute prÃ©registration d'une expÃ©rience rÃ©elle.

### B1_CLOSURE_CHECK

- **Question 1.** Les 8 mutations prÃ©cÃ©demment survivantes sont rejetÃ©es (OBSERVÃ‰, `test_b1_adversarial_invariants_reject_previously_surviving_mutations`). En revanche, la couverture Â« tous blocs normatifs Â» est en Ã©chec (BB1).
- **Questions 2 et 3.** Les 10 cas, 25 breakers de base et 8 breakers de clÃ´ture sont tous prÃ©sents dans la matrice. Chaque entrÃ©e pointe vers une paire classe.mÃ©thode qui existe rÃ©ellement : je l'ai vÃ©rifiÃ© par AST et non par sous-chaÃ®ne. Les 23 tests distincts passent (OBSERVÃ‰).
- **Question 4.** Les rÃ©utilisations D2/D4 sont globalement suffisantes, avec les rÃ©serves NB5 et NB6.
- **Question 5.** Il reste des preuves dÃ©claratives prÃ©sentÃ©es comme comportementales (NB4, NB6).
- **Question 6.** Oui, dans une mesure limitÃ©e : `verdict: "PASS"` est une chaÃ®ne Ã©crite Ã  la main. Le test de matrice n'exÃ©cute rien et n'Ã©pingle pas l'objet couvert (BB1).

### B2_CADENCE_CHECK

- **Question 7.** La cadence fixed-rate est appliquÃ©e, pas seulement la divisibilitÃ© par 30 (`scheduled - previous_scheduled != interval` donne `CADENCE_GAP`).
- **Question 8.** Sauter le premier crÃ©neau requis donne `SKIPPED_REQUIRED_ATTEMPT` (OBSERVÃ‰).
- **Question 9.** Un trou, un doublon, un chevauchement ou une tentative hors grille sont bloquÃ©s. Le dÃ©bordement non enregistrÃ© reste un cas limite (NB1).
- **Question 10.** Les valeurs 30, 60 et l'origine 0 sont figÃ©es dans `make_timing_plan`, et `_validate_plan` exige l'Ã©galitÃ© stricte.

### B3_TEMPORAL_INCONSISTENCY_CHECK

- **Question 11.** Une cible vue dans une tentative dÃ©marrÃ©e avant la libÃ©ration donne `BLOCKED`, y compris quand la lecture se termine aprÃ¨s la libÃ©ration (E9, OBSERVÃ‰).
- **Question 12.** L'ordre ambigu Bâ†’A n'est pas dÃ©tectÃ© (NB2).
- **Question 13.** Toute la sÃ©quence est validÃ©e avant de dÃ©cider. Une incohÃ©rence survenant aprÃ¨s la dÃ©tection fait basculer le PASS en `BLOCKED` (E10, OBSERVÃ‰). Aucun blanchiment par une observation ultÃ©rieure.

### B4_TIMING_METRIC_CHECK

- **Questions 15 Ã  17.** L'instant de dÃ©but et l'instant de fin sont deux champs distincts, et la latence est mesurÃ©e Ã  la fin de lecture : la durÃ©e de lecture est donc incluse (OBSERVÃ‰ : `test_b4_read_completion_not_poll_start_controls_latency`, latence 61 donne FAIL). La frontiÃ¨re Ã  60 inclus est cohÃ©rente.
- **Question 18.** Le fixed-rate est suffisamment spÃ©cifiÃ© pour le modÃ¨le. Il ne l'est pas encore pour une expÃ©rience rÃ©elle (NB9 ; la gigue ou le dÃ©calage d'un dÃ©marrage rÃ©el par rapport Ã  la grille n'est pas dÃ©fini).
- **Question 19.** Le contenu du contrat ne prÃ©tend plus que l'origine est observable, mais aucune garde n'empÃªche d'y revenir (BB1).
- **Question 20.** La garantie de 60 s avec une panne transitoire n'est plus inconditionnelle (`single_transient_read_failure_may_still_meet_60_second_bound: false`, gardÃ©), et la version conditionnelle est correcte.
- **Question 14.** Origine valide en principe, sous les rÃ©serves NB9.

### B5_TIP_AND_QUEUE_CHECK

- **Questions 21 et 22.** `EXACT_TIP_OBSERVED` exige l'Ã©galitÃ© stricte des identitÃ©s, et une observation rÃ©ussie sans identitÃ© est rejetÃ©e. Une tÃªte intermÃ©diaire n'est jamais dÃ©clarÃ©e observÃ©e par le modÃ¨le, qui renvoie FAIL ou INCOMPLETE (E7). La non-injection dans la file n'est pas exÃ©cutable (NB4).
- **Question 23.** Aucune coalescence rÃ©introduite : la contenance n'entre dans aucune opÃ©ration de file.
- **Question 24.** FIFO, absence de remplacement et absence de reciblage tiennent (OBSERVÃ‰ via D2), avec la rÃ©serve d'audit NB5.
- **Question 25.** Aucune promesse de dÃ©tection par tÃªte transitoire : `PER_TRANSIENT_TIP_DETECTION_SLA_QUALIFIED` est interdit et gardÃ©.

### EVIDENCE_MATRIX_CHECK

- 43 entrÃ©es correspondent Ã  23 tests distincts.
- Les blobs correspondent sous `git hash-object --path`.
- Les classes et mÃ©thodes existent.
- DÃ©fauts : statut PASS Ã©crit Ã  la main, contrat et modÃ¨le non Ã©pinglÃ©s (BB1), types de preuve mal Ã©tiquetÃ©s (NB6).
- Les clÃ©s JSON en double seraient fusionnÃ©es silencieusement Ã  la lecture ; c'est un risque mineur.

### AUTHORITY_LEAKAGE_CHECK

- Aucune fuite observÃ©e : le modÃ¨le est pur, `_result` code en dur `automatic_*` et `real_*` Ã  False, et les runtimes D2/D4 sont inchangÃ©s.
- L'autoritÃ© humaine est gardÃ©e (`human_adjudication_before_external_rereview_forbidden`, mutation dÃ©tectÃ©e).
- Deux points ouverts, dÃ©jÃ  signalÃ©s prÃ©cÃ©demment et non adressÃ©s : la mutation de l'Ã©tat de contrÃ´le D4 rÃ©el par une observation future, et l'autoritÃ© de pousser pour la libÃ©ration contrÃ´lÃ©e (NB9). Ils doivent Ãªtre Ã©numÃ©rÃ©s avant toute expÃ©rience rÃ©elle.

### CLAIM_SCOPE_CHECK

- La dÃ©claration maximale (`â€¦TARGETED_CLOSURE_CANDIDATE_QUALIFIED_PENDING_EXTERNAL_REREVIEW`) est cohÃ©rente avec le contrat.
- Le Â§B1 du rapport de qualification surdÃ©clare (BB1). Le Â§B5 prÃ©sente une rÃ¨gle comme une propriÃ©tÃ© (NB4).
- Les rapports ne prÃ©tendent ni SLA rÃ©el ni boucle rÃ©elle.

### MISSING_ADVERSARIAL_CASES

- Mutation de chaque champ normatif survivant (BB1), et combinaison de rÃ©gressions B4.
- Lecture qui dÃ©borde au-delÃ  du crÃ©neau suivant, avec ou sans enregistrement suivant (NB1).
- TÃªte tierce observÃ©e aprÃ¨s la libÃ©ration puis cible ; retour arriÃ¨re vers la cible (NB2).
- TÃªte dÃ©jÃ  en file puis descendante observÃ©e, appliquÃ©es Ã  `classify_tip_visibility` (NB3).
- TÃªte en attente non active plus nouvelle tÃªte FF : le test existe en D2 mais n'est pas rÃ©fÃ©rencÃ© (NB6).
- Changement du contrat aprÃ¨s construction de la matrice.

### RECOMMENDED_TARGETED_CORRECTIONS

1. **(BB1)** Dans `assert_contract_invariants`, ajouter des Ã©galitÃ©s strictes pour les 20 champs normatifs survivants listÃ©s en BB1. Ne pas ajouter les textes `purpose`/`name`, ni les SHA de contexte qui ne sont que des traces historiques.
2. **(BB1)** Dans la matrice et son test, Ã©pingler les blobs du contrat et du modÃ¨le couverts, et Ã©chouer en cas d'Ã©cart.
3. Rejouer le balayage de mutations de feuilles comme critÃ¨re de sortie. Survivants admis : seulement des champs explicitement dÃ©clarÃ©s non normatifs.
4. **(Optionnel, mÃªme passe)** Pour NB1, soit bloquer quand `completed > scheduled + interval` sans tentative suivante, soit dÃ©clarer ce dÃ©bordement admissible dans le contrat. Pour NB6, rÃ©Ã©tiqueter les preuves dÃ©claratives et rÃ©fÃ©rencer `test_07` ainsi que le cas D2 Â« en attente non active Â». Pour NB7, ajouter `INCOMPLETE_SYNTHETIC_WINDOW` au contrat comme statut non-PASS.
5. NB2, NB3, NB4 et NB9 relÃ¨vent de la prÃ©registration d'une future expÃ©rience rÃ©elle, pas de cette clÃ´ture.

Ensuite : passe adversariale ciblÃ©e sur le HEAD persistÃ©, puis une seule passe complÃ¨te, de prÃ©fÃ©rence en clone jetable avec empreinte de l'Ã©tat rÃ©el (NB8).

Cette revue n'est ni une adoption humaine ni une autorisation d'exÃ©cution rÃ©elle.
~~~~

# SOURCE: BB1 INTERNAL ADJUDICATION

Path: reports/program/2026-10-02-OBSIDIAN-P5E-BB1-NORMATIVE-GUARD-INTERNAL-ADJUDICATION.md
~~~~
# P5-E V0.1 â€” BB1 NORMATIVE GUARD COVERAGE â€” INTERNAL ADJUDICATION

Date: 2026-10-02

## Opening identity

Branch:
`feat/obsidian-projection-p5e-v0.1-bb1-normative-guard-closure`

Opening checkpoint:
`fe622489e9b822a987a1ec571f99b180fcfa5fb5`

Opening worktree:
`CLEAN`

Contract blob:
`b0668b4dff65b8e30ee0d93a3e5a3fe42c4421dd`

Model blob:
`b783717c9e9596b585b7b1686835c73fffbd1a7c`

Matrix blob:
`0440175fbb79877e466119cb973ea82389a4ecd8`
## BB1 local reproduction

The external reviewer reported that a combination of normative regressions could survive the 50-test P5-E targeted surface.

The exact defect was reproduced locally on the governed checkpoint without mutating repository files.

Baseline:
```text
50 tests
0 failures
0 errors
```

Combined BB1 mutation:
```text
50 tests
0 failures
0 errors
```

Therefore:
`BB1 = CONFIRMED_BLOCKING`

The defect is guard coverage, not an incorrect current value.
## Full leaf mutation sweep

A read-only sweep mutated every contract leaf independently in a temporary copy.

Observed:
```text
TOTAL_LEAF_MUTATIONS = 154
SURVIVING_FULL_50_MUTATIONS = 36
```

The 36 survivors divide into:
```text
NORMATIVE_SURVIVORS = 23
NON_NORMATIVE_OR_HISTORICAL_SURVIVORS = 13
```

The exit criterion for this closure is not zero total survivors.

The binding exit criterion is:
`NORMATIVE_LEAF_MUTATIONS_SURVIVING = 0`
## Normative survivor set â€” 23 leaves

1. `source_repository`
2. `monitored_source.remote`
3. `monitored_source.branch`
4. `monitored_source.canonical_authority`
5. `monitored_source.local_working_tree_is_not_authority`
6. `objective.this_stage_is_not_real_end_to_end_execution`
7. `objective.this_stage_may_not_claim_continuous_synchronization`
8. `near_real_time_timing.delivery_semantics`
9. `near_real_time_timing.detection_latency_definition`
10. `near_real_time_timing.future_real_bound_clock`
11. `near_real_time_timing.future_real_wall_clock_may_be_recorded_as_evidence_only`
12. `near_real_time_timing.latency_bound_breach_must_not_be_reported_as_near_real_time_pass`
13. `synthetic_timing_model.required`
14. `synthetic_timing_model.observation_record_fields`
15. `head_transition_policy.initial_head_may_queue_exact_head_only_under_existing_p5d2_semantics`
16. `head_transition_policy.fast_forward_head_may_queue_exact_head_only_under_existing_p5d2_semantics`
17. `queue_and_supersession.burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification`
18. `end_to_end_definition.real_end_to_end_stages`
19. `end_to_end_definition.real_end_to_end_pass_requires_all_authorized_applicable_stages`
20. `real_context_evidence_only.must_not_be_used_as_real_experiment_execution`
21. `real_context_evidence_only.must_not_be_mutated_by_contract_qualification`
22. `tip_visibility_semantics.future_ancestry_enumeration_requires_separate_qualification`
23. `external_review_targeted_closure.external_rereview_required_before_human_normative_adoption`

All 23 require strict protection or semantic de-duplication.
## Explicit non-normative / historical survivor set â€” 13 leaves

These may survive the normative mutation criterion:

- `objective.name`
- `objective.purpose`
- `synthetic_timing_model.purpose`
- `queue_and_supersession.p5a_supersession_intent_preserved_as_future_design_debt`
- `real_context_evidence_only.live_projection_head_at_opening`
- `real_context_evidence_only.queued_unevaluated_head_at_opening`
- `real_context_evidence_only.remote_head_observed_during_contract_opening`
- `real_context_evidence_only.queued_head_is_ancestor_of_remote_head`
- `external_review_targeted_closure.findings.B1`
- `external_review_targeted_closure.findings.B2`
- `external_review_targeted_closure.findings.B3`
- `external_review_targeted_closure.findings.B4`
- `external_review_targeted_closure.findings.B5`

They are descriptive, historical, or debt-tracking metadata rather than current behavioral authority.
## Matrix binding defect

The current evidence matrix contains no exact binding for:
- the covered P5-E contract blob;
- the covered P5-E model blob.

Its tests validate mapped test-file blobs but not the exact contract/model objects being qualified.

This is independently confirmed as part of BB1.

## Adjudicated same-pass corrections

NB1:
`VALID â€” CLOSE IN THIS PASS`
A read that crosses the next required fixed-rate slot must fail closed rather than silently terminalize as PASS.

NB4:
`VALID â€” CLAIM CORRECTION ONLY`
The non-injection of an unobserved intermediate tip is a future adapter rule, not a currently qualified runtime property.
NB6:
`VALID â€” MATRIX EVIDENCE REMAP`
Mappings must point to semantically exact behavioral evidence. Add a dedicated pending-non-active test only if no exact existing test exists.

NB7:
`PARTIAL â€” SMALL SEMANTIC CLEANUP`
- `INCOMPLETE_SYNTHETIC_WINDOW` must be explicitly NON-PASS.
- duplicate fixed-rate slot must have a distinct failure code from `CADENCE_GAP`.
- theoretical AST bypass is not part of this closure because no current model defect was demonstrated.

## Deferred by scope

NB2, NB3, NB5, and NB9 remain recorded for future real-observation / ancestry-classifier preregistration.

They are not reopened here.
## Real-state fingerprint before closure work

P5-D4 control files at opening:
```text
observer-events.jsonl
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

observer-checkpoint.json
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

The closure must not mutate these files.

## Internal verdict

```text
BB1 = CONFIRMED_BLOCKING
BB1_LOCAL_REPRODUCTION = COMPLETE
NORMATIVE_SURVIVORS = 23
MATRIX_CONTRACT_BINDING = ABSENT
MATRIX_MODEL_BINDING = ABSENT
REAL_P5E = CLOSED
```

~~~~

# SOURCE: BB1 PREREGISTRATION

Path: tools/obsidian_projection/p5e_bb1_normative_guard_closure_preregistration_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_P5E_BB1_NORMATIVE_GUARD_CLOSURE_PREREGISTRATION_V0_1",
  "status": "PREREGISTERED_BEFORE_RED",
  "repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "branch": "feat/obsidian-projection-p5e-v0.1-bb1-normative-guard-closure",
  "opening_checkpoint": "fe622489e9b822a987a1ec571f99b180fcfa5fb5",
  "authority_scope": "BB1_PLUS_NB1_NB4_NB6_NB7_ONLY",
  "real_p5e_execution_authorized": false,
  "opening_identity": {
    "contract_blob": "b0668b4dff65b8e30ee0d93a3e5a3fe42c4421dd",
    "model_blob": "b783717c9e9596b585b7b1686835c73fffbd1a7c",
    "matrix_blob": "0440175fbb79877e466119cb973ea82389a4ecd8",
    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5"
  },
  "bb1_reproduction": {
    "baseline_tests": 50,
    "baseline_failures": 0,
    "baseline_errors": 0,
    "combined_bb1_mutation_tests": 50,
    "combined_bb1_mutation_failures": 0,
    "combined_bb1_mutation_errors": 0,
    "full_leaf_mutations": 154,
    "surviving_mutations": 36,
    "normative_survivors": 23,
    "non_normative_or_historical_survivors": 13
  },
  "normative_leaf_set": [
    "source_repository",
    "monitored_source.remote",
    "monitored_source.branch",
    "monitored_source.canonical_authority",
    "monitored_source.local_working_tree_is_not_authority",
    "objective.this_stage_is_not_real_end_to_end_execution",
    "objective.this_stage_may_not_claim_continuous_synchronization",
    "near_real_time_timing.delivery_semantics",
    "near_real_time_timing.detection_latency_definition",
    "near_real_time_timing.future_real_bound_clock",
    "near_real_time_timing.future_real_wall_clock_may_be_recorded_as_evidence_only",
    "near_real_time_timing.latency_bound_breach_must_not_be_reported_as_near_real_time_pass",
    "synthetic_timing_model.required",
    "synthetic_timing_model.observation_record_fields",
    "head_transition_policy.initial_head_may_queue_exact_head_only_under_existing_p5d2_semantics",
    "head_transition_policy.fast_forward_head_may_queue_exact_head_only_under_existing_p5d2_semantics",
    "queue_and_supersession.burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification",
    "end_to_end_definition.real_end_to_end_stages",
    "end_to_end_definition.real_end_to_end_pass_requires_all_authorized_applicable_stages",
    "real_context_evidence_only.must_not_be_used_as_real_experiment_execution",
    "real_context_evidence_only.must_not_be_mutated_by_contract_qualification",
    "tip_visibility_semantics.future_ancestry_enumeration_requires_separate_qualification",
    "external_review_targeted_closure.external_rereview_required_before_human_normative_adoption"
  ],
  "non_normative_metadata_set": [
    "objective.name",
    "objective.purpose",
    "synthetic_timing_model.purpose",
    "queue_and_supersession.p5a_supersession_intent_preserved_as_future_design_debt",
    "real_context_evidence_only.live_projection_head_at_opening",
    "real_context_evidence_only.queued_unevaluated_head_at_opening",
    "real_context_evidence_only.remote_head_observed_during_contract_opening",
    "real_context_evidence_only.queued_head_is_ancestor_of_remote_head",
    "external_review_targeted_closure.findings.B1",
    "external_review_targeted_closure.findings.B2",
    "external_review_targeted_closure.findings.B3",
    "external_review_targeted_closure.findings.B4",
    "external_review_targeted_closure.findings.B5"
  ],
  "mutation_sweep_contract": {
    "mutation_operator": {
      "boolean": "INVERT",
      "integer": "PLUS_ONE",
      "string": "REPLACE_WITH_MUTATED",
      "list": "DROP_LAST_ITEM"
    },
    "exit_criterion": "NORMATIVE_LEAF_MUTATIONS_SURVIVING_EQUALS_ZERO",
    "non_normative_survivors_permitted": true,
    "combined_bb1_regression_case_required": true,
    "all_normative_leaves_must_be_guarded_or_semantically_deduplicated": true
  },
  "matrix_binding_closure": {
    "covered_contract_blob_required": true,
    "covered_model_blob_required": true,
    "matrix_test_must_fail_on_contract_drift": true,
    "matrix_test_must_fail_on_model_drift": true
  },
  "nb1_closure": {
    "status": "IN_SCOPE",
    "fixed_rate_single_writer_preserved": true,
    "read_crossing_next_required_slot_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "failure_code": "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT"
  },
  "nb4_closure": {
    "status": "IN_SCOPE_CLAIM_ONLY",
    "unobserved_tip_non_injection_is_future_adapter_rule": true,
    "unobserved_tip_non_injection_is_current_runtime_qualified_property": false
  },
  "nb6_closure": {
    "status": "IN_SCOPE",
    "matrix_mapping_must_match_exact_semantic_behavior": true,
    "queue_capacity_behavior_should_reuse_p5d4_test_07": true,
    "pending_non_active_behavior_requires_exact_existing_or_new_minimal_test": true
  },
  "nb7_closure": {
    "status": "IN_SCOPE_PARTIAL",
    "incomplete_synthetic_window_must_be_explicit_non_pass": true,
    "duplicate_slot_must_not_use_cadence_gap_code": true,
    "duplicate_slot_failure_code": "DUPLICATE_FIXED_RATE_SLOT",
    "ast_theoretical_bypass_in_scope": false
  },
  "deferred_findings": [
    "NB2",
    "NB3",
    "NB5",
    "NB9"
  ],
  "real_state_fingerprint_before": {
    "observer_events_sha256": "54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af",
    "observer_checkpoint_sha256": "c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4",
    "last_run_sha256": "eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259"
  },
  "qualification_sequence": [
    "PERSIST_ADJUDICATION_AND_PREREGISTRATION",
    "CREATE_MUTATION_SWEEP_AND_BB1_RED",
    "CREATE_NB1_NB4_NB6_NB7_RED",
    "PERSIST_RED_EVIDENCE",
    "APPLY_MINIMAL_GUARD_AND_SEMANTIC_CORRECTIONS",
    "BIND_MATRIX_TO_EXACT_CONTRACT_AND_MODEL_BLOBS",
    "RERUN_NORMATIVE_MUTATION_SWEEP",
    "REQUIRE_ZERO_NORMATIVE_SURVIVORS",
    "RUN_TARGETED_REGRESSIONS",
    "RUN_EXACTLY_ONE_FULL_OBSIDIAN_SUITE_IN_DISPOSABLE_CLONE",
    "VERIFY_REAL_P5D4_FINGERPRINT_UNCHANGED",
    "BUILD_SELF_CONTAINED_EXTERNAL_REVIEW_PACKET",
    "PERSIST_QUALIFICATION_AND_STOP"
  ],
  "full_suite_budget": {
    "maximum_runs": 1,
    "disposable_clone_required": true,
    "pre_post_real_state_fingerprints_required": true
  },
  "authority_boundary": {
    "real_polling_loop_authorized": false,
    "real_head_evaluation_authorized": false,
    "stage_a_authorized": false,
    "stage_b_authorized": false,
    "promotion_authorized": false,
    "publication_authorized": false,
    "real_vault_mutation_authorized": false,
    "current_mutation_authorized": false,
    "p5d4_real_state_mutation_authorized": false,
    "daemon_authorized": false,
    "scheduled_task_authorized": false,
    "windows_service_authorized": false,
    "startup_registration_authorized": false,
    "p6_authorized": false,
    "automatic_human_adoption_authorized": false
  },
  "mandatory_stop": "BEFORE_HUMAN_NORMATIVE_ADOPTION_AND_BEFORE_ANY_REAL_P5E_EXECUTION"
}

~~~~

# SOURCE: PRIOR TARGETED CLOSURE PREREGISTRATION

Path: tools/obsidian_projection/p5e_external_review_targeted_closure_preregistration_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_P5E_EXTERNAL_REVIEW_TARGETED_CLOSURE_PREREGISTRATION_V0_1",
  "status": "PREREGISTERED_BEFORE_TARGETED_RED",
  "repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "branch": "feat/obsidian-projection-p5e-v0.1-external-review-targeted-closure",
  "opening_base_head": "4ffe259c2485437b5d782be633e1ba23985d4945",
  "authority_scope": "B1_TO_B5_TARGETED_CLOSURE_ONLY",
  "real_p5e_execution_authorized": false,
  "candidate_identity": {
    "contract_blob": "e5c3d7a9d451aba65e8062078c6c10d23e586f39",
    "model_blob": "8662dd97a1c8a1af33d6593ae923384e96404b5a",
    "base_test_blob": "2305e0768182d82657c34a7cb53c502714a2ab81",
    "adversarial_test_blob": "6235c4b2addc16acd043832664440ec76f6dada2",
    "p5d2_runtime_blob": "fd212f61ec38332b677110f40265638af55a73e2",
    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5"
  },
  "adjudicated_findings": {
    "B1": "CONFIRMED_BLOCKING_WITH_UPSTREAM_COVERAGE_NUANCE",
    "B2": "CONFIRMED_BLOCKING",
    "B3": "CONFIRMED_BLOCKING",
    "B4": "CONFIRMED_BLOCKING",
    "B5": "PARTIALLY_CONFIRMED_BLOCKING_SEMANTIC_GAP"
  },
  "inherited_timing_constraints": {
    "poll_interval_seconds": 30,
    "detection_latency_seconds_max": 60,
    "silent_widening_forbidden": true
  },
  "timing_closure_contract": {
    "real_measurement_origin": "CONTROLLED_SOURCE_RELEASE_MONOTONIC",
    "unobservable_remote_head_available_time_claim_authorized": false,
    "measurement_endpoint": "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC",
    "schedule_semantics": "FIXED_RATE",
    "synthetic_schedule_origin_seconds": 0,
    "first_required_attempt": "FIRST_FIXED_RATE_SLOT_AT_OR_AFTER_SOURCE_RELEASE",
    "all_required_attempt_slots_must_be_present_until_terminal_result": true,
    "attempt_start_and_read_completion_must_be_separate": true,
    "read_completion_before_attempt_start_forbidden": true,
    "overlapping_single_writer_attempts_forbidden": true,
    "exact_tip_observed_before_source_release_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "skipped_required_attempt_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "cadence_gap_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "detection_after_60_seconds_result": "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
    "no_future_fixed_rate_attempt_can_meet_bound_result": "FAIL_NO_DETECTION_BY_BOUND"
  },
  "tip_visibility_closure": {
    "observation_records_must_carry_head_identity": true,
    "exact_tip_observed_definition": "REMOTE_READ_RETURNED_TARGET_HEAD",
    "intermediate_fast_forward_commit_definition": "COMMIT_CONTAINED_BY_LATER_OBSERVED_FAST_FORWARD_HEAD_BUT_NOT_ITSELF_OBSERVED_AS_REMOTE_TIP",
    "unobserved_intermediate_tip_may_be_claimed_exactly_observed": false,
    "unobserved_intermediate_tip_may_be_queued": false,
    "fast_forward_content_containment_is_not_queue_coalescing": true,
    "already_observed_queued_head_replacement_forbidden": true,
    "already_observed_queued_head_retarget_forbidden": true,
    "per_transient_tip_detection_sla_authorized": false
  },
  "coverage_closure": {
    "explicit_requirement_to_test_blob_matrix_required": true,
    "upstream_behavioral_tests_may_be_reused_if_exactly_mapped": true,
    "unmapped_required_case_result": "BLOCKED",
    "unmapped_required_breaker_result": "BLOCKED",
    "required_case_list_must_be_exactly_frozen": true,
    "required_breaker_list_must_be_exactly_frozen": true,
    "adversarial_invariants_must_cover_all_normative_contract_blocks": true,
    "claims_without_executable_evidence_forbidden": true
  },
  "required_new_red_cases": [
    "B1_UNGUARDED_HEAD_TRANSITION_MUTATION_SURVIVES",
    "B1_UNGUARDED_FAILURE_SEMANTICS_MUTATION_SURVIVES",
    "B1_UNGUARDED_SYNTHETIC_CLOCK_MUTATION_SURVIVES",
    "B1_REQUIRED_BREAKER_LIST_REPLACEMENT_SURVIVES",
    "B2_SKIPPED_FIRST_REQUIRED_SLOT_ACCEPTED",
    "B2_CADENCE_GAP_ACCEPTED",
    "B3_PRE_SOURCE_TARGET_OBSERVATION_IGNORED",
    "B4_REMOTE_AVAILABILITY_ORIGIN_REMAINS_NORMATIVE",
    "B4_READ_COMPLETION_DURATION_HIDDEN",
    "B5_OBSERVATION_WITHOUT_HEAD_IDENTITY_ACCEPTED",
    "B5_INTERMEDIATE_TIP_CLAIMED_AS_EXACT_OBSERVATION"
  ],
  "required_existing_behavioral_mappings": {
    "SAME_HEAD_NOOP": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "method": "ObserverTickTests.test_same_head_is_strict_noop_for_queue",
      "blob": "9c472a39e3d8eed8cf6cfc910bce27ee5fac7c58"
    },
    "NON_FAST_FORWARD_BLOCKED": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "method": "ObserverTickTests.test_non_fast_forward_blocks_without_queueing",
      "blob": "9c472a39e3d8eed8cf6cfc910bce27ee5fac7c58"
    },
    "UNKNOWN_ANCESTRY_BLOCKED": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "method": "ObserverTickTests.test_unknown_ancestry_blocks_without_queueing",
      "blob": "9c472a39e3d8eed8cf6cfc910bce27ee5fac7c58"
    },
    "PENDING_QUEUE_FULL_NEWER_HEAD_FAILS_CLOSED": {
      "path": "tests/obsidian_projection/test_p5d4_bounded_observer_loop_runtime_v0_1.py",
      "method": "P5D4RuntimeV01Tests.test_07_queue_capacity_blocks_before_tick",
      "blob": "5bcc563487ca8c64a1afde9f022504b2b618af7b"
    },
    "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "method": "ObserverTickTests.test_fast_forward_queues_without_retargeting_active",
      "blob": "9c472a39e3d8eed8cf6cfc910bce27ee5fac7c58"
    }
  },
  "authority_boundary": {
    "real_polling_loop_authorized": false,
    "real_head_evaluation_authorized": false,
    "stage_a_authorized": false,
    "stage_b_authorized": false,
    "promotion_authorized": false,
    "publication_authorized": false,
    "real_vault_mutation_authorized": false,
    "current_mutation_authorized": false,
    "daemon_authorized": false,
    "scheduled_task_authorized": false,
    "windows_service_authorized": false,
    "startup_registration_authorized": false,
    "p6_authorized": false,
    "automatic_human_adoption_authorized": false
  },
  "qualification_sequence": [
    "PERSIST_INTERNAL_ADJUDICATION_AND_PREREGISTRATION",
    "ADD_TARGETED_RED_TESTS",
    "PERSIST_RED_EVIDENCE",
    "APPLY_MINIMAL_CONTRACT_MODEL_TEST_CORRECTIONS",
    "BUILD_REQUIREMENT_TO_EXECUTABLE_EVIDENCE_MATRIX",
    "RUN_TARGETED_GREEN_AND_ADVERSARIAL",
    "RUN_REQUIRED_PREDECESSOR_REGRESSIONS",
    "RUN_EXACTLY_ONE_FULL_OBSIDIAN_SUITE",
    "BUILD_CORRECTED_SELF_CONTAINED_EXTERNAL_REVIEW_PACKET",
    "PERSIST_QUALIFICATION_EVIDENCE",
    "STOP_BEFORE_HUMAN_ADOPTION_AND_REAL_P5E"
  ],
  "full_suite_budget": {
    "maximum_new_full_obsidian_runs": 1
  },
  "mandatory_stop": "BEFORE_HUMAN_NORMATIVE_ADOPTION_AND_BEFORE_ANY_REAL_P5E_EXECUTION"
}

~~~~

# SOURCE: ORIGINAL P5-E PREREGISTRATION

Path: tools/obsidian_projection/p5e_end_to_end_near_real_time_preregistration_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_PREREGISTRATION_V0_1",
  "status": "PREREGISTERED_BEFORE_RED",
  "repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "branch": "feat/obsidian-projection-p5e-end-to-end-near-real-time-qualification-v0.1",
  "opening_base_head": "11c6c5e1a009b171466f26e295f812030015d655",
  "authorized_stage": "CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY",
  "real_p5e_execution_authorized": false,
  "predecessor_identities": {
    "p5a_continuous_projection_contract_blob": "96ec1a768b8e9ff77d94bbcd36ee513678c258e6",
    "p5a_qualification_report_blob": "8954475370494ff00f77af8331b2e54b80cf3f70",
    "p5d1_observer_contract_blob": "a20999ae991e07447e25ecd1592964f2d333449b",
    "p5d1_static_review_blob": "d10a6659e8deec917803f53c652fc7e4d4d19458",
    "p5d2_one_shot_contract_blob": "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3",
    "p5d2_static_review_blob": "023cc210facdbc4b571b88bd257057c67a3df46b",
    "p5d4_loop_contract_blob": "6980de1eb55e49c0c2bd2f91620aeb75640753b6",
    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
    "p5d4_real_v0_2_qualification_blob": "660a679532d1bb122b0df382230d4d249a0cac1f",
    "p5d4_human_adjudication_blob": "ef5e07c6641db94e91d9f2bc0e8093b244baa507"
  },
  "inherited_timing_constraints": {
    "delivery_semantics": "NEAR_REAL_TIME_BOUNDED_LATENCY",
    "instantaneous_realtime_claim_forbidden": true,
    "target_detection_latency_seconds_max": 60,
    "candidate_poll_interval_seconds": 30,
    "silent_interval_widening_forbidden": true,
    "silent_latency_bound_widening_forbidden": true
  },
  "timing_semantics_to_freeze": {
    "detection_latency_definition": "FIRST_SUCCESSFUL_EXACT_REMOTE_HEAD_OBSERVATION_TIME_MINUS_SOURCE_HEAD_AVAILABLE_TIME",
    "future_real_clock_requirement": "MONOTONIC_ELAPSED_TIME_FOR_BOUND_ENFORCEMENT",
    "synthetic_model_clock": "EXPLICIT_INJECTED_SECONDS_ONLY",
    "synthetic_model_may_sleep": false,
    "synthetic_model_may_use_network": false,
    "synthetic_model_may_use_filesystem_state": false,
    "synthetic_model_may_launch_processes": false,
    "source_change_just_after_poll_must_be_covered": true,
    "one_transient_read_failure_then_success_by_60_seconds_must_be_covered": true,
    "first_success_after_60_seconds_must_fail_latency_qualification": true,
    "no_success_by_60_seconds_must_fail_latency_qualification": true
  },
  "authority_boundary": {
    "pending_head_evaluation_authorized": false,
    "evaluation_authorized": false,
    "stage_a_authorized": false,
    "stage_b_authorized": false,
    "promotion_authorized": false,
    "publication_authorized": false,
    "real_vault_mutation_authorized": false,
    "current_mutation_authorized": false,
    "current_tmp_mutation_authorized": false,
    "real_polling_loop_authorized": false,
    "daemon_authorized": false,
    "startup_registration_authorized": false,
    "scheduled_task_authorized": false,
    "windows_service_authorized": false,
    "p6_authorized": false
  },
  "queue_semantics_resolution": {
    "p5a_historical_supersession_intent": "NON_NORMATIVE_WHERE_IT_CONFLICTS_WITH_CURRENT_EXECUTABLE_P5D4_QUEUE_SEMANTICS",
    "p5d4_fifo_required": true,
    "p5d4_silent_drop_forbidden": true,
    "p5d4_silent_reorder_forbidden": true,
    "p5d4_latest_only_replacement_forbidden": true,
    "p5d4_coalescing_authorized": false,
    "p5d4_queue_capacity_exhausted_result": "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
    "newer_head_must_not_retarget_active_or_pending_head": true,
    "no_new_coalescing_event_may_be_invented_in_p5e_v0_1": true
  },
  "observed_real_context_read_only": {
    "live_projection_head": "59f1dc26973b0b50efefccf12b26784d1e41f546",
    "queued_unevaluated_head": "1d4c2f3d657b36ecaa6ab25b967e46b3620190d1",
    "remote_head_at_opening": "fcca78571a26955ae3fe462746ef49557e4e84e5",
    "queued_head_is_ancestor_of_remote_head": true,
    "p5d4_event_log_sha256": "54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af",
    "p5d4_checkpoint_sha256": "c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4",
    "p5d4_last_run_sha256": "eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259",
    "context_is_evidence_only_not_test_input_authority": true,
    "real_context_must_not_be_mutated_or_evaluated_in_this_stage": true
  },
  "claim_boundary": {
    "contract_pass_may_claim": "P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL_QUALIFIED",
    "contract_pass_may_not_claim": [
      "P5E_REAL_END_TO_END_QUALIFIED",
      "CONTINUOUS_SYNCHRONIZATION_QUALIFIED",
      "REAL_60_SECOND_SLA_QUALIFIED",
      "AUTOMATIC_EVALUATION_QUALIFIED",
      "AUTOMATIC_PROMOTION_QUALIFIED",
      "AUTOMATIC_PUBLICATION_QUALIFIED"
    ],
    "real_end_to_end_claim_requires_separate_human_authorization_and_real_experiment": true
  },
  "required_synthetic_cases": [
    "SAME_HEAD_NOOP",
    "CHANGE_JUST_AFTER_POLL_DETECTED_AT_NEXT_30_SECOND_SLOT",
    "ONE_TRANSIENT_READ_FAILURE_THEN_DETECTED_BY_60_SECONDS",
    "DETECTION_AFTER_60_SECONDS_REJECTED",
    "NO_DETECTION_BY_60_SECONDS_REJECTED",
    "NON_FAST_FORWARD_BLOCKED",
    "UNKNOWN_ANCESTRY_BLOCKED",
    "PENDING_QUEUE_FULL_NEWER_HEAD_FAILS_CLOSED",
    "SAME_HEAD_DOES_NOT_GROW_QUEUE",
    "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD"
  ],
  "required_breakers": [
    "POLL_INTERVAL_NOT_EXACTLY_30_ACCEPTED",
    "DETECTION_BOUND_ABOVE_60_ACCEPTED",
    "INSTANTANEOUS_REALTIME_CLAIM_ACCEPTED",
    "WALL_CLOCK_USED_AS_SYNTHETIC_CONTROL_CLOCK",
    "SLEEP_USED_IN_SYNTHETIC_MODEL",
    "NETWORK_USED_IN_SYNTHETIC_MODEL",
    "FILESYSTEM_STATE_USED_IN_SYNTHETIC_MODEL",
    "PROCESS_LAUNCH_USED_IN_SYNTHETIC_MODEL",
    "SUCCESS_AFTER_60_SECONDS_CLASSIFIED_PASS",
    "NO_SUCCESS_BY_60_SECONDS_CLASSIFIED_PASS",
    "SAME_HEAD_GROWS_QUEUE",
    "NON_FAST_FORWARD_AUTO_CONTINUES",
    "UNKNOWN_ANCESTRY_AUTO_CONTINUES",
    "QUEUE_FULL_SILENTLY_DROPS_HEAD",
    "QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD",
    "QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT",
    "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD",
    "EVALUATION_AUTHORITY_BECOMES_TRUE",
    "PROMOTION_AUTHORITY_BECOMES_TRUE",
    "PUBLICATION_AUTHORITY_BECOMES_TRUE",
    "REAL_VAULT_MUTATION_AUTHORITY_BECOMES_TRUE",
    "REAL_POLLING_AUTHORITY_BECOMES_TRUE",
    "DAEMON_OR_SERVICE_AUTHORITY_BECOMES_TRUE",
    "P6_AUTHORITY_BECOMES_TRUE",
    "CONTRACT_PASS_LAUNDERS_INTO_REAL_P5E_PASS"
  ],
  "test_first_sequence": [
    "PERSIST_PREREGISTRATION",
    "ADD_TESTS_EXPECTING_ABSENT_CONTRACT_AND_MODEL",
    "RUN_RED_AND_PERSIST_EVIDENCE",
    "ADD_MINIMAL_CONTRACT_AND_PURE_SYNTHETIC_MODEL",
    "RUN_TARGETED_GREEN",
    "ADD_ADVERSARIAL_TESTS",
    "MECHANICAL_CORRECTIONS_ONLY_IF_DEMONSTRATED",
    "RUN_TARGETED_REGRESSIONS",
    "RUN_ONE_FULL_OBSIDIAN_REBREAK",
    "BUILD_SELF_CONTAINED_EXTERNAL_REVIEW_PACKET",
    "PERSIST_QUALIFICATION_EVIDENCE",
    "STOP_BEFORE_REAL_P5E"
  ],
  "mandatory_stop": "AFTER_CONTRACT_SYNTHETIC_QUALIFICATION_AND_EXTERNAL_REVIEW_PACKET_BEFORE_ANY_REAL_P5E_EXECUTION"
}

~~~~

# SOURCE: CORRECTED P5-E CONTRACT

Path: tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1",
  "status": "CANDIDATE_TARGETED_CLOSURE_PENDING_EXTERNAL_REREVIEW",
  "qualification_stage": "CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY",
  "real_p5e_execution_authorized": false,
  "source_repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "monitored_source": {
    "remote": "origin",
    "branch": "integration/system-v1",
    "canonical_authority": "GITHUB_REMOTE_BRANCH",
    "local_working_tree_is_not_authority": true
  },
  "predecessors": {
    "p5a_continuous_projection_contract_blob": "96ec1a768b8e9ff77d94bbcd36ee513678c258e6",
    "p5a_qualification_report_blob": "8954475370494ff00f77af8331b2e54b80cf3f70",
    "p5d1_observer_contract_blob": "a20999ae991e07447e25ecd1592964f2d333449b",
    "p5d1_static_review_blob": "d10a6659e8deec917803f53c652fc7e4d4d19458",
    "p5d2_one_shot_contract_blob": "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3",
    "p5d2_static_review_blob": "023cc210facdbc4b571b88bd257057c67a3df46b",
    "p5d4_loop_contract_blob": "6980de1eb55e49c0c2bd2f91620aeb75640753b6",
    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
    "p5d4_real_v0_2_qualification_blob": "660a679532d1bb122b0df382230d4d249a0cac1f",
    "p5d4_human_adjudication_blob": "ef5e07c6641db94e91d9f2bc0e8093b244baa507"
  },
  "objective": {
    "name": "END_TO_END_NEAR_REAL_TIME_QUALIFICATION",
    "purpose": "Define the temporal and authority contract required before any real repeated observation experiment may claim bounded near-real-time behavior around the already-qualified P5-D4 bounded loop.",
    "this_stage_is_not_real_end_to_end_execution": true,
    "this_stage_may_not_claim_continuous_synchronization": true
  },
  "near_real_time_timing": {
    "delivery_semantics": "NEAR_REAL_TIME_BOUNDED_LATENCY",
    "poll_interval_seconds": 30,
    "detection_latency_seconds_max": 60,
    "instantaneous_realtime_claim_forbidden": true,
    "silent_interval_widening_forbidden": true,
    "silent_latency_bound_widening_forbidden": true,
    "detection_latency_definition": "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC_MINUS_CONTROLLED_SOURCE_RELEASE_MONOTONIC",
    "future_real_bound_clock": "MONOTONIC_ELAPSED_TIME",
    "future_real_wall_clock_may_be_recorded_as_evidence_only": true,
    "future_real_poll_schedule_semantics": "FIXED_RATE_30_SECOND_GRID",
    "single_transient_read_failure_may_still_meet_60_second_bound": false,
    "latency_bound_breach_must_not_be_reported_as_near_real_time_pass": true,
    "real_measurement_origin": "CONTROLLED_SOURCE_RELEASE_MONOTONIC",
    "measurement_endpoint": "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC",
    "schedule_semantics": "FIXED_RATE",
    "remote_head_available_time_is_measurable_origin": false,
    "real_latency_metric": "REMOTE_READ_COMPLETION_MONOTONIC_MINUS_CONTROLLED_SOURCE_RELEASE_MONOTONIC",
    "attempt_start_and_read_completion_are_distinct": true,
    "read_duration_is_included_in_detection_latency": true,
    "eligible_detection_attempt_must_start_at_or_after_release": true,
    "single_transient_read_failure_may_meet_bound_only_if_read_completion_is_within_60_seconds": true
  },
  "synthetic_timing_model": {
    "required": true,
    "clock_source": "EXPLICIT_INJECTED_MONOTONIC_SECONDS_ONLY",
    "sleep_forbidden": true,
    "network_forbidden": true,
    "filesystem_state_forbidden": true,
    "process_launch_forbidden": true,
    "environment_read_forbidden": true,
    "real_p5d4_control_state_access_forbidden": true,
    "real_vault_access_forbidden": true,
    "purpose": "Prove timing arithmetic and claim boundaries without performing repeated real observation.",
    "schedule_semantics": "FIXED_RATE",
    "schedule_origin_seconds": 0,
    "observation_record_fields": [
      "scheduled_at_seconds",
      "completed_at_seconds",
      "outcome",
      "observed_head"
    ],
    "head_identity_required_on_successful_remote_observation": true,
    "skipped_required_attempt_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "cadence_gap_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "pre_source_target_observation_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "explicit_non_pass_statuses": [
      "INCOMPLETE_SYNTHETIC_WINDOW"
    ],
    "attempt_overruns_next_required_slot_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "attempt_overruns_next_required_slot_failure_code": "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT",
    "duplicate_fixed_rate_slot_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "duplicate_fixed_rate_slot_failure_code": "DUPLICATE_FIXED_RATE_SLOT"
  },
  "authority_boundary": {
    "observer_may_create_governance_authority": false,
    "pending_head_evaluation_authorized": false,
    "evaluation_authorized": false,
    "stage_a_authorized": false,
    "stage_b_authorized": false,
    "promotion_authorized": false,
    "publication_authorized": false,
    "real_vault_mutation_authorized": false,
    "current_mutation_authorized": false,
    "current_tmp_mutation_authorized": false,
    "real_polling_loop_authorized": false,
    "daemon_authorized": false,
    "startup_registration_authorized": false,
    "scheduled_task_authorized": false,
    "windows_service_authorized": false,
    "p6_authorized": false
  },
  "head_transition_policy": {
    "same_head_result": "NOOP",
    "same_head_queue_growth_forbidden": true,
    "initial_head_may_queue_exact_head_only_under_existing_p5d2_semantics": true,
    "fast_forward_head_may_queue_exact_head_only_under_existing_p5d2_semantics": true,
    "non_fast_forward_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "unknown_ancestry_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "non_fast_forward_auto_continue_forbidden": true,
    "unknown_ancestry_auto_continue_forbidden": true,
    "active_or_pending_candidate_retarget_forbidden": true
  },
  "queue_and_supersession": {
    "precedence_rule": "CURRENT_QUALIFIED_P5D4_EXECUTABLE_QUEUE_SEMANTICS_OVERRIDE_EARLIER_P5A_DESIGN_INTENT_WHERE_THEY_CONFLICT",
    "p5a_supersession_intent_preserved_as_future_design_debt": true,
    "fifo_required": true,
    "unique_heads_required": true,
    "silent_drop_forbidden": true,
    "silent_reorder_forbidden": true,
    "latest_only_replacement_forbidden": true,
    "coalescing_authorized": false,
    "new_coalescing_semantic_event_authorized": false,
    "pending_head_retarget_forbidden": true,
    "capacity_exhausted_result": "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
    "capacity_exhausted_must_not_mutate_p5d2_state": true,
    "burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification": true
  },
  "failure_and_freshness": {
    "fail_closed_default": true,
    "network_failure_must_not_create_current_claim": true,
    "last_known_good_live_projection_preserved": true,
    "latency_bound_breach_result": "NEAR_REAL_TIME_BOUND_NOT_QUALIFIED",
    "queue_capacity_exhaustion_result": "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
    "non_fast_forward_or_unknown_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "unexpected_state_or_timing_ambiguity_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "timing_inconsistency_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "skipped_required_attempt_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "cadence_gap_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "pre_source_target_observation_result": "BLOCKED_REQUIRES_ADJUDICATION"
  },
  "end_to_end_definition": {
    "real_end_to_end_stages": [
      "SOURCE_HEAD_BECOMES_OBSERVABLE",
      "REMOTE_HEAD_DETECTED_WITHIN_BOUND",
      "HEAD_TRANSITION_CLASSIFIED",
      "EXACT_HEAD_ENTERED_GOVERNED_QUEUE_OR_FAIL_CLOSED",
      "EXACT_HEAD_EVALUATED_IF_SEPARATELY_AUTHORIZED",
      "PROMOTION_DECISION_IF_SEPARATELY_AUTHORIZED",
      "PUBLICATION_IF_SEPARATELY_AUTHORIZED",
      "LIVE_GENERATION_VERIFIED_IF_PUBLICATION_AUTHORIZED"
    ],
    "current_stage_may_qualify_only": [
      "TIMING_CONTRACT",
      "SYNTHETIC_FIXED_RATE_DETECTION_MODEL",
      "AUTHORITY_BOUNDARIES",
      "REUSED_MAPPED_P5D2_P5D4_FAIL_CLOSED_QUEUE_BEHAVIOR"
    ],
    "real_end_to_end_pass_requires_all_authorized_applicable_stages": true,
    "omitted_unauthorized_downstream_stages_may_not_be_relabelled_pass": true,
    "transient_tip_exact_detection_sla_not_qualified": true,
    "real_remote_availability_to_detection_sla_not_qualified": true
  },
  "claim_boundary": {
    "maximum_current_claim": "P5E_V0_1_TARGETED_CLOSURE_CANDIDATE_QUALIFIED_PENDING_EXTERNAL_REREVIEW",
    "real_end_to_end_qualification_requires_separate_authorization": true,
    "forbidden_current_claims": [
      "P5E_REAL_END_TO_END_QUALIFIED",
      "CONTINUOUS_SYNCHRONIZATION_QUALIFIED",
      "REAL_60_SECOND_SLA_QUALIFIED",
      "AUTOMATIC_EVALUATION_QUALIFIED",
      "AUTOMATIC_PROMOTION_QUALIFIED",
      "AUTOMATIC_PUBLICATION_QUALIFIED",
      "REMOTE_HEAD_AVAILABLE_TIME_TO_DETECTION_SLA_QUALIFIED",
      "PER_TRANSIENT_TIP_DETECTION_SLA_QUALIFIED"
    ]
  },
  "real_context_evidence_only": {
    "live_projection_head_at_opening": "59f1dc26973b0b50efefccf12b26784d1e41f546",
    "queued_unevaluated_head_at_opening": "1d4c2f3d657b36ecaa6ab25b967e46b3620190d1",
    "remote_head_observed_during_contract_opening": "fcca78571a26955ae3fe462746ef49557e4e84e5",
    "queued_head_is_ancestor_of_remote_head": true,
    "must_not_be_used_as_real_experiment_execution": true,
    "must_not_be_mutated_by_contract_qualification": true
  },
  "required_synthetic_cases": [
    "SAME_HEAD_NOOP",
    "CHANGE_JUST_AFTER_POLL_DETECTED_AT_NEXT_30_SECOND_SLOT",
    "ONE_TRANSIENT_READ_FAILURE_THEN_DETECTED_BY_60_SECONDS",
    "DETECTION_AFTER_60_SECONDS_REJECTED",
    "NO_DETECTION_BY_60_SECONDS_REJECTED",
    "NON_FAST_FORWARD_BLOCKED",
    "UNKNOWN_ANCESTRY_BLOCKED",
    "PENDING_QUEUE_FULL_NEWER_HEAD_FAILS_CLOSED",
    "SAME_HEAD_DOES_NOT_GROW_QUEUE",
    "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD"
  ],
  "required_breakers": [
    "POLL_INTERVAL_NOT_EXACTLY_30_ACCEPTED",
    "DETECTION_BOUND_ABOVE_60_ACCEPTED",
    "INSTANTANEOUS_REALTIME_CLAIM_ACCEPTED",
    "WALL_CLOCK_USED_AS_SYNTHETIC_CONTROL_CLOCK",
    "SLEEP_USED_IN_SYNTHETIC_MODEL",
    "NETWORK_USED_IN_SYNTHETIC_MODEL",
    "FILESYSTEM_STATE_USED_IN_SYNTHETIC_MODEL",
    "PROCESS_LAUNCH_USED_IN_SYNTHETIC_MODEL",
    "SUCCESS_AFTER_60_SECONDS_CLASSIFIED_PASS",
    "NO_SUCCESS_BY_60_SECONDS_CLASSIFIED_PASS",
    "SAME_HEAD_GROWS_QUEUE",
    "NON_FAST_FORWARD_AUTO_CONTINUES",
    "UNKNOWN_ANCESTRY_AUTO_CONTINUES",
    "QUEUE_FULL_SILENTLY_DROPS_HEAD",
    "QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD",
    "QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT",
    "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD",
    "EVALUATION_AUTHORITY_BECOMES_TRUE",
    "PROMOTION_AUTHORITY_BECOMES_TRUE",
    "PUBLICATION_AUTHORITY_BECOMES_TRUE",
    "REAL_VAULT_MUTATION_AUTHORITY_BECOMES_TRUE",
    "REAL_POLLING_AUTHORITY_BECOMES_TRUE",
    "DAEMON_OR_SERVICE_AUTHORITY_BECOMES_TRUE",
    "P6_AUTHORITY_BECOMES_TRUE",
    "CONTRACT_PASS_LAUNDERS_INTO_REAL_P5E_PASS"
  ],
  "next_gate_after_candidate_qualification": {
    "external_adversarial_review_required_before_normative_adoption": true,
    "human_adjudication_required_after_external_review": true,
    "real_p5e_execution_requires_separate_human_authorization": true,
    "p6_remains_closed": true,
    "external_adversarial_rereview_required": true,
    "human_adjudication_before_external_rereview_forbidden": true
  },
  "tip_visibility_semantics": {
    "observed_remote_tip_definition": "HEAD_IDENTITY_RETURNED_BY_A_SUCCESSFUL_REMOTE_READ",
    "intermediate_fast_forward_commit_definition": "COMMIT_CONTAINED_BY_LATER_OBSERVED_FAST_FORWARD_HEAD_BUT_NOT_ITSELF_OBSERVED_AS_REMOTE_TIP",
    "unobserved_intermediate_tip_may_be_claimed_observed": false,
    "unobserved_intermediate_tip_may_be_queued": false,
    "fast_forward_content_containment_is_queue_coalescing": false,
    "already_observed_queued_head_replacement_forbidden": true,
    "already_observed_queued_head_retarget_forbidden": true,
    "per_transient_tip_detection_sla_authorized": false,
    "future_ancestry_enumeration_requires_separate_qualification": true,
    "unobserved_intermediate_tip_non_injection_is_future_adapter_rule": true,
    "unobserved_intermediate_tip_non_injection_is_current_runtime_qualified_property": false
  },
  "external_review_targeted_closure": {
    "findings": {
      "B1": "CONFIRMED_BLOCKING_WITH_UPSTREAM_COVERAGE_NUANCE",
      "B2": "CONFIRMED_BLOCKING",
      "B3": "CONFIRMED_BLOCKING",
      "B4": "CONFIRMED_BLOCKING",
      "B5": "PARTIALLY_CONFIRMED_BLOCKING_SEMANTIC_GAP"
    },
    "required_breakers": [
      "SKIPPED_REQUIRED_ATTEMPT_ACCEPTED",
      "CADENCE_GAP_ACCEPTED",
      "PRE_SOURCE_TARGET_OBSERVATION_IGNORED",
      "REMOTE_AVAILABILITY_TIME_TREATED_AS_MEASURABLE_ORIGIN",
      "READ_COMPLETION_LATENCY_HIDDEN",
      "OBSERVATION_WITHOUT_HEAD_IDENTITY_ACCEPTED",
      "UNOBSERVED_TRANSIENT_TIP_CLAIMED_EXACTLY_OBSERVED",
      "REQUIRED_CASE_OR_BREAKER_UNMAPPED"
    ],
    "requirement_to_executable_evidence_matrix_required": true,
    "all_required_cases_must_be_mapped": true,
    "all_base_breakers_must_be_mapped": true,
    "all_targeted_closure_breakers_must_be_mapped": true,
    "unmapped_requirement_result": "BLOCKED",
    "external_rereview_required_before_human_normative_adoption": true
  }
}

~~~~

# SOURCE: CORRECTED P5-E MODEL

Path: tools/obsidian_projection/p5e_near_real_time_model.py
~~~~
from __future__ import annotations

from typing import Any


PLAN_SCHEMA = "ATDS_OBSIDIAN_P5E_SYNTHETIC_TIMING_PLAN_V0_1_AMENDED"
RESULT_SCHEMA = "ATDS_OBSIDIAN_P5E_SYNTHETIC_TIMING_RESULT_V0_1_AMENDED"

_POLL_INTERVAL_SECONDS = 30
_DETECTION_LATENCY_SECONDS_MAX = 60
_SCHEDULE_ORIGIN_SECONDS = 0
_ALLOWED_OUTCOMES = frozenset({"READ_FAILURE", "REMOTE_HEAD_OBSERVED"})


class P5ETimingModelError(ValueError):
    pass


def _is_nonnegative_int(value: Any) -> bool:
    return (
        not isinstance(value, bool)
        and isinstance(value, int)
        and value >= 0
    )


def _valid_head(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 40:
        return False
    return all(ch in "0123456789abcdef" for ch in value)


def make_timing_plan(
    *,
    poll_interval_seconds: int = _POLL_INTERVAL_SECONDS,
    detection_latency_seconds_max: int = _DETECTION_LATENCY_SECONDS_MAX,
    schedule_origin_seconds: int = _SCHEDULE_ORIGIN_SECONDS,
) -> dict[str, Any]:
    if poll_interval_seconds != _POLL_INTERVAL_SECONDS:
        raise P5ETimingModelError(
            "P5-E V0.1 poll interval must remain exactly 30 seconds"
        )
    if detection_latency_seconds_max != _DETECTION_LATENCY_SECONDS_MAX:
        raise P5ETimingModelError(
            "P5-E V0.1 detection bound must remain exactly 60 seconds"
        )
    if schedule_origin_seconds != _SCHEDULE_ORIGIN_SECONDS:
        raise P5ETimingModelError(
            "P5-E V0.1 synthetic fixed-rate origin must remain exactly zero"
        )
    return {
        "schema": PLAN_SCHEMA,
        "poll_interval_seconds": _POLL_INTERVAL_SECONDS,
        "detection_latency_seconds_max": _DETECTION_LATENCY_SECONDS_MAX,
        "schedule_origin_seconds": _SCHEDULE_ORIGIN_SECONDS,
        "schedule_semantics": "FIXED_RATE",
        "clock_source": "EXPLICIT_INJECTED_MONOTONIC_SECONDS_ONLY",
        "measurement_origin": "CONTROLLED_SOURCE_RELEASE_MONOTONIC",
        "measurement_endpoint": "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC",
        "real_execution_authorized": False,
    }


def _validate_plan(plan: dict[str, Any]) -> None:
    if not isinstance(plan, dict):
        raise P5ETimingModelError("plan must be an object")
    if plan != make_timing_plan(
        poll_interval_seconds=plan.get("poll_interval_seconds"),
        detection_latency_seconds_max=plan.get(
            "detection_latency_seconds_max"
        ),
        schedule_origin_seconds=plan.get("schedule_origin_seconds"),
    ):
        raise P5ETimingModelError("plan fields mismatch")


def _blocked(failure_code: str) -> dict[str, Any]:
    return _result(
        status="BLOCKED_REQUIRES_ADJUDICATION",
        failure_code=failure_code,
        detection_latency_seconds=None,
        first_detection_scheduled_at_seconds=None,
        first_detection_completed_at_seconds=None,
        observed_head=None,
    )


def _result(
    *,
    status: str,
    failure_code: str | None,
    detection_latency_seconds: int | None,
    first_detection_scheduled_at_seconds: int | None,
    first_detection_completed_at_seconds: int | None,
    observed_head: str | None,
) -> dict[str, Any]:
    return {
        "schema": RESULT_SCHEMA,
        "status": status,
        "failure_code": failure_code,
        "detection_latency_seconds": detection_latency_seconds,
        "first_detection_scheduled_at_seconds": (
            first_detection_scheduled_at_seconds
        ),
        "first_detection_completed_at_seconds": (
            first_detection_completed_at_seconds
        ),
        "observed_head": observed_head,
        "real_end_to_end_qualified": False,
        "continuous_synchronization_qualified": False,
        "automatic_evaluation_authorized": False,
        "automatic_promotion_authorized": False,
        "automatic_publication_authorized": False,
    }


def _first_fixed_rate_slot_at_or_after(
    *,
    instant_seconds: int,
    interval: int,
    origin: int,
) -> int:
    first_slot = origin + interval
    if instant_seconds <= first_slot:
        return first_slot
    delta = instant_seconds - origin
    quotient, remainder = divmod(delta, interval)
    return origin + (quotient + (1 if remainder else 0)) * interval


def _validate_observation_shapes(
    observations: list[dict[str, Any]],
) -> None:
    if not isinstance(observations, list) or not observations:
        raise P5ETimingModelError("observations must be a non-empty list")
    required_fields = {
        "scheduled_at_seconds",
        "completed_at_seconds",
        "outcome",
        "observed_head",
    }
    for observation in observations:
        if not isinstance(observation, dict):
            raise P5ETimingModelError("observation must be an object")
        if set(observation) != required_fields:
            raise P5ETimingModelError("observation fields mismatch")
        scheduled = observation["scheduled_at_seconds"]
        completed = observation["completed_at_seconds"]
        outcome = observation["outcome"]
        observed_head = observation["observed_head"]
        if not _is_nonnegative_int(scheduled):
            raise P5ETimingModelError("scheduled time must be nonnegative")
        if not _is_nonnegative_int(completed):
            raise P5ETimingModelError("completion time must be nonnegative")
        if outcome not in _ALLOWED_OUTCOMES:
            raise P5ETimingModelError("observation outcome invalid")
        if outcome == "READ_FAILURE":
            if observed_head is not None:
                raise P5ETimingModelError(
                    "read failure may not carry a head identity"
                )
        elif not _valid_head(observed_head):
            raise P5ETimingModelError(
                "successful remote observation requires exact head identity"
            )


def classify_tip_visibility(
    *,
    target_head: str,
    observed_head: str,
    fast_forward_contains_target: bool,
) -> str:
    if not _valid_head(target_head) or not _valid_head(observed_head):
        raise P5ETimingModelError("tip identity must be a lowercase 40-hex SHA")
    if not isinstance(fast_forward_contains_target, bool):
        raise P5ETimingModelError("containment fact must be boolean")
    if observed_head == target_head:
        return "EXACT_TIP_OBSERVED"
    if fast_forward_contains_target:
        return "CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED"
    return "UNRELATED_OR_UNPROVEN_REQUIRES_ADJUDICATION"


def qualify_detection(
    *,
    plan: dict[str, Any],
    source_release_at_seconds: int,
    target_head: str,
    observations: list[dict[str, Any]],
) -> dict[str, Any]:
    _validate_plan(plan)
    if not _is_nonnegative_int(source_release_at_seconds):
        raise P5ETimingModelError(
            "controlled source release time must be a nonnegative integer"
        )
    if not _valid_head(target_head):
        raise P5ETimingModelError(
            "target head must be a lowercase 40-hex SHA"
        )
    _validate_observation_shapes(observations)

    interval = plan["poll_interval_seconds"]
    bound = plan["detection_latency_seconds_max"]
    origin = plan["schedule_origin_seconds"]

    previous_scheduled: int | None = None
    previous_completed: int | None = None
    for observation in observations:
        scheduled = observation["scheduled_at_seconds"]
        completed = observation["completed_at_seconds"]

        if scheduled <= origin or (scheduled - origin) % interval != 0:
            return _blocked("ATTEMPT_OFF_FIXED_RATE_GRID")
        if completed < scheduled:
            return _blocked("READ_COMPLETION_PRECEDES_ATTEMPT_START")
        if previous_scheduled is not None:
            if scheduled == previous_scheduled:
                return _blocked("DUPLICATE_FIXED_RATE_SLOT")
            if scheduled - previous_scheduled != interval:
                return _blocked("CADENCE_GAP")
            if previous_completed is not None and previous_completed > scheduled:
                return _blocked("ATTEMPT_OVERLAP")
        previous_scheduled = scheduled
        previous_completed = completed

        if (
            observation["outcome"] == "REMOTE_HEAD_OBSERVED"
            and observation["observed_head"] == target_head
            and scheduled < source_release_at_seconds
        ):
            return _blocked(
                "TARGET_HEAD_OBSERVED_BEFORE_CONTROLLED_RELEASE"
            )

    last_observation = observations[-1]
    if (
        last_observation["completed_at_seconds"]
        > last_observation["scheduled_at_seconds"] + interval
    ):
        return _blocked("ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT")

    first_required_slot = _first_fixed_rate_slot_at_or_after(
        instant_seconds=source_release_at_seconds,
        interval=interval,
        origin=origin,
    )
    scheduled_slots = {
        observation["scheduled_at_seconds"] for observation in observations
    }
    if (
        any(slot >= first_required_slot for slot in scheduled_slots)
        and first_required_slot not in scheduled_slots
    ):
        return _blocked("SKIPPED_REQUIRED_ATTEMPT")

    first_detection: dict[str, Any] | None = None
    for observation in observations:
        if observation["scheduled_at_seconds"] < source_release_at_seconds:
            continue
        if (
            observation["outcome"] == "REMOTE_HEAD_OBSERVED"
            and observation["observed_head"] == target_head
        ):
            first_detection = observation
            break

    if first_detection is not None:
        completed = first_detection["completed_at_seconds"]
        latency = completed - source_release_at_seconds
        if latency <= bound:
            status = "PASS_DETECTED_WITHIN_BOUND"
            failure_code = None
        else:
            status = "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED"
            failure_code = "DETECTION_COMPLETION_EXCEEDED_BOUND"
        return _result(
            status=status,
            failure_code=failure_code,
            detection_latency_seconds=latency,
            first_detection_scheduled_at_seconds=(
                first_detection["scheduled_at_seconds"]
            ),
            first_detection_completed_at_seconds=completed,
            observed_head=first_detection["observed_head"],
        )

    last_scheduled = observations[-1]["scheduled_at_seconds"]
    next_required_slot = last_scheduled + interval
    if next_required_slot - source_release_at_seconds > bound:
        return _result(
            status="FAIL_NO_DETECTION_BY_BOUND",
            failure_code="NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND",
            detection_latency_seconds=None,
            first_detection_scheduled_at_seconds=None,
            first_detection_completed_at_seconds=None,
            observed_head=None,
        )

    return _result(
        status="INCOMPLETE_SYNTHETIC_WINDOW",
        failure_code=None,
        detection_latency_seconds=None,
        first_detection_scheduled_at_seconds=None,
        first_detection_completed_at_seconds=None,
        observed_head=None,
    )

~~~~

# SOURCE: P5-E BASE TESTS

Path: tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py
~~~~
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
PREREG = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_preregistration_v0_1.json"
MODEL = ROOT / "tools" / "obsidian_projection" / "p5e_near_real_time_model.py"

TARGET = "a" * 40
OTHER = "b" * 40

EXPECTED_PREDECESSORS = {
    "p5a_continuous_projection_contract_blob": "96ec1a768b8e9ff77d94bbcd36ee513678c258e6",
    "p5a_qualification_report_blob": "8954475370494ff00f77af8331b2e54b80cf3f70",
    "p5d1_observer_contract_blob": "a20999ae991e07447e25ecd1592964f2d333449b",
    "p5d1_static_review_blob": "d10a6659e8deec917803f53c652fc7e4d4d19458",
    "p5d2_one_shot_contract_blob": "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3",
    "p5d2_static_review_blob": "023cc210facdbc4b571b88bd257057c67a3df46b",
    "p5d4_loop_contract_blob": "6980de1eb55e49c0c2bd2f91620aeb75640753b6",
    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
    "p5d4_real_v0_2_qualification_blob": "660a679532d1bb122b0df382230d4d249a0cac1f",
    "p5d4_human_adjudication_blob": "ef5e07c6641db94e91d9f2bc0e8093b244baa507",
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_model():
    spec = importlib.util.spec_from_file_location("p5e_near_real_time_model", MODEL)
    if spec is None or spec.loader is None:
        raise AssertionError("P5-E synthetic timing model unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def obs(scheduled, completed, outcome, head=None):
    return {
        "scheduled_at_seconds": scheduled,
        "completed_at_seconds": completed,
        "outcome": outcome,
        "observed_head": head,
    }


class TestP5EContractV01(unittest.TestCase):
    def test_preregistration_is_present_and_frozen_before_contract(self):
        p = load_json(PREREG)
        self.assertEqual(p["status"], "PREREGISTERED_BEFORE_RED")
        self.assertFalse(p["real_p5e_execution_authorized"])

    def test_contract_schema_stage_and_status_are_exact(self):
        c = load_json(CONTRACT)
        self.assertEqual(
            c["schema"],
            "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1",
        )
        self.assertEqual(
            c["qualification_stage"],
            "CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY",
        )
        self.assertEqual(
            c["status"],
            "CANDIDATE_TARGETED_CLOSURE_PENDING_EXTERNAL_REREVIEW",
        )
        self.assertFalse(c["real_p5e_execution_authorized"])

    def test_all_predecessor_blobs_are_exact(self):
        c = load_json(CONTRACT)
        self.assertEqual(c["predecessors"], EXPECTED_PREDECESSORS)

    def test_timing_inheritance_remains_exact_30_and_60(self):
        t = load_json(CONTRACT)["near_real_time_timing"]
        self.assertEqual(t["poll_interval_seconds"], 30)
        self.assertEqual(t["detection_latency_seconds_max"], 60)
        self.assertTrue(t["instantaneous_realtime_claim_forbidden"])
        self.assertTrue(t["silent_interval_widening_forbidden"])
        self.assertTrue(t["silent_latency_bound_widening_forbidden"])

    def test_real_latency_metric_is_falsifiable_and_local_monotonic(self):
        t = load_json(CONTRACT)["near_real_time_timing"]
        self.assertEqual(
            t["real_measurement_origin"],
            "CONTROLLED_SOURCE_RELEASE_MONOTONIC",
        )
        self.assertEqual(
            t["measurement_endpoint"],
            "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC",
        )
        self.assertEqual(t["schedule_semantics"], "FIXED_RATE")
        self.assertFalse(t["remote_head_available_time_is_measurable_origin"])
        self.assertTrue(t["attempt_start_and_read_completion_are_distinct"])
        self.assertTrue(t["read_duration_is_included_in_detection_latency"])
        self.assertTrue(
            t["eligible_detection_attempt_must_start_at_or_after_release"]
        )

    def test_contract_forbids_authority_expansion(self):
        a = load_json(CONTRACT)["authority_boundary"]
        for field in (
            "observer_may_create_governance_authority",
            "pending_head_evaluation_authorized",
            "evaluation_authorized",
            "stage_a_authorized",
            "stage_b_authorized",
            "promotion_authorized",
            "publication_authorized",
            "real_vault_mutation_authorized",
            "current_mutation_authorized",
            "current_tmp_mutation_authorized",
            "real_polling_loop_authorized",
            "daemon_authorized",
            "startup_registration_authorized",
            "scheduled_task_authorized",
            "windows_service_authorized",
            "p6_authorized",
        ):
            self.assertFalse(a[field], field)

    def test_queue_conflict_resolves_in_favor_of_p5d4(self):
        q = load_json(CONTRACT)["queue_and_supersession"]
        self.assertTrue(q["fifo_required"])
        self.assertTrue(q["silent_drop_forbidden"])
        self.assertTrue(q["silent_reorder_forbidden"])
        self.assertTrue(q["latest_only_replacement_forbidden"])
        self.assertFalse(q["coalescing_authorized"])
        self.assertFalse(q["new_coalescing_semantic_event_authorized"])
        self.assertTrue(q["pending_head_retarget_forbidden"])
        self.assertTrue(q["capacity_exhausted_must_not_mutate_p5d2_state"])
        self.assertEqual(
            q["capacity_exhausted_result"],
            "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
        )

    def test_tip_visibility_does_not_claim_unobserved_tip_detection(self):
        t = load_json(CONTRACT)["tip_visibility_semantics"]
        self.assertFalse(t["unobserved_intermediate_tip_may_be_claimed_observed"])
        self.assertFalse(t["unobserved_intermediate_tip_may_be_queued"])
        self.assertFalse(t["fast_forward_content_containment_is_queue_coalescing"])
        self.assertTrue(t["already_observed_queued_head_replacement_forbidden"])
        self.assertTrue(t["already_observed_queued_head_retarget_forbidden"])
        self.assertFalse(t["per_transient_tip_detection_sla_authorized"])

    def test_claim_boundary_is_narrowed_pending_external_rereview(self):
        claims = load_json(CONTRACT)["claim_boundary"]
        self.assertEqual(
            claims["maximum_current_claim"],
            "P5E_V0_1_TARGETED_CLOSURE_CANDIDATE_QUALIFIED_PENDING_EXTERNAL_REREVIEW",
        )
        self.assertTrue(
            claims["real_end_to_end_qualification_requires_separate_authorization"]
        )
        forbidden = set(claims["forbidden_current_claims"])
        for claim in (
            "P5E_REAL_END_TO_END_QUALIFIED",
            "REAL_60_SECOND_SLA_QUALIFIED",
            "CONTINUOUS_SYNCHRONIZATION_QUALIFIED",
            "REMOTE_HEAD_AVAILABLE_TIME_TO_DETECTION_SLA_QUALIFIED",
            "PER_TRANSIENT_TIP_DETECTION_SLA_QUALIFIED",
        ):
            self.assertIn(claim, forbidden)

    def test_model_freezes_exact_plan(self):
        m = load_model()
        plan = m.make_timing_plan()
        self.assertEqual(plan["poll_interval_seconds"], 30)
        self.assertEqual(plan["detection_latency_seconds_max"], 60)
        self.assertEqual(plan["schedule_semantics"], "FIXED_RATE")
        self.assertEqual(plan["schedule_origin_seconds"], 0)
        with self.assertRaises(m.P5ETimingModelError):
            m.make_timing_plan(poll_interval_seconds=31)
        with self.assertRaises(m.P5ETimingModelError):
            m.make_timing_plan(detection_latency_seconds_max=61)
        with self.assertRaises(m.P5ETimingModelError):
            m.make_timing_plan(schedule_origin_seconds=1)

    def test_change_just_after_poll_is_detected_at_next_slot_completion(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[obs(30, 31, "REMOTE_HEAD_OBSERVED", TARGET)],
        )
        self.assertEqual(result["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(result["detection_latency_seconds"], 30)
        self.assertEqual(result["first_detection_scheduled_at_seconds"], 30)
        self.assertEqual(result["first_detection_completed_at_seconds"], 31)
        self.assertFalse(result["real_end_to_end_qualified"])

    def test_one_transient_failure_can_pass_only_by_completion_within_60(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                obs(30, 31, "READ_FAILURE"),
                obs(60, 61, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(result["detection_latency_seconds"], 60)

    def test_read_completion_after_60_is_rejected(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                obs(30, 31, "READ_FAILURE"),
                obs(60, 62, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(
            result["status"], "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED"
        )
        self.assertEqual(result["detection_latency_seconds"], 61)

    def test_no_detection_fails_when_next_fixed_rate_slot_cannot_meet_bound(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                obs(30, 31, "READ_FAILURE"),
                obs(60, 60, "READ_FAILURE"),
            ],
        )
        self.assertEqual(result["status"], "FAIL_NO_DETECTION_BY_BOUND")
        self.assertEqual(
            result["failure_code"],
            "NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND",
        )

    def test_off_grid_schedule_is_fail_closed(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[obs(31, 32, "REMOTE_HEAD_OBSERVED", TARGET)],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(result["failure_code"], "ATTEMPT_OFF_FIXED_RATE_GRID")

    def test_tip_visibility_classification_is_explicit(self):
        m = load_model()
        self.assertEqual(
            m.classify_tip_visibility(
                target_head=TARGET,
                observed_head=TARGET,
                fast_forward_contains_target=False,
            ),
            "EXACT_TIP_OBSERVED",
        )
        self.assertEqual(
            m.classify_tip_visibility(
                target_head=TARGET,
                observed_head=OTHER,
                fast_forward_contains_target=True,
            ),
            "CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED",
        )


if __name__ == "__main__":
    unittest.main()

~~~~

# SOURCE: P5-E ADVERSARIAL TESTS

Path: tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py
~~~~
import ast
import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
MODEL = ROOT / "tools" / "obsidian_projection" / "p5e_near_real_time_model.py"

TARGET = "a" * 40
OTHER = "b" * 40

EXPECTED_CASES = [
    "SAME_HEAD_NOOP",
    "CHANGE_JUST_AFTER_POLL_DETECTED_AT_NEXT_30_SECOND_SLOT",
    "ONE_TRANSIENT_READ_FAILURE_THEN_DETECTED_BY_60_SECONDS",
    "DETECTION_AFTER_60_SECONDS_REJECTED",
    "NO_DETECTION_BY_60_SECONDS_REJECTED",
    "NON_FAST_FORWARD_BLOCKED",
    "UNKNOWN_ANCESTRY_BLOCKED",
    "PENDING_QUEUE_FULL_NEWER_HEAD_FAILS_CLOSED",
    "SAME_HEAD_DOES_NOT_GROW_QUEUE",
    "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD",
]

EXPECTED_BASE_BREAKERS = [
    "POLL_INTERVAL_NOT_EXACTLY_30_ACCEPTED",
    "DETECTION_BOUND_ABOVE_60_ACCEPTED",
    "INSTANTANEOUS_REALTIME_CLAIM_ACCEPTED",
    "WALL_CLOCK_USED_AS_SYNTHETIC_CONTROL_CLOCK",
    "SLEEP_USED_IN_SYNTHETIC_MODEL",
    "NETWORK_USED_IN_SYNTHETIC_MODEL",
    "FILESYSTEM_STATE_USED_IN_SYNTHETIC_MODEL",
    "PROCESS_LAUNCH_USED_IN_SYNTHETIC_MODEL",
    "SUCCESS_AFTER_60_SECONDS_CLASSIFIED_PASS",
    "NO_SUCCESS_BY_60_SECONDS_CLASSIFIED_PASS",
    "SAME_HEAD_GROWS_QUEUE",
    "NON_FAST_FORWARD_AUTO_CONTINUES",
    "UNKNOWN_ANCESTRY_AUTO_CONTINUES",
    "QUEUE_FULL_SILENTLY_DROPS_HEAD",
    "QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD",
    "QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT",
    "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD",
    "EVALUATION_AUTHORITY_BECOMES_TRUE",
    "PROMOTION_AUTHORITY_BECOMES_TRUE",
    "PUBLICATION_AUTHORITY_BECOMES_TRUE",
    "REAL_VAULT_MUTATION_AUTHORITY_BECOMES_TRUE",
    "REAL_POLLING_AUTHORITY_BECOMES_TRUE",
    "DAEMON_OR_SERVICE_AUTHORITY_BECOMES_TRUE",
    "P6_AUTHORITY_BECOMES_TRUE",
    "CONTRACT_PASS_LAUNDERS_INTO_REAL_P5E_PASS",
]

EXPECTED_CLOSURE_BREAKERS = [
    "SKIPPED_REQUIRED_ATTEMPT_ACCEPTED",
    "CADENCE_GAP_ACCEPTED",
    "PRE_SOURCE_TARGET_OBSERVATION_IGNORED",
    "REMOTE_AVAILABILITY_TIME_TREATED_AS_MEASURABLE_ORIGIN",
    "READ_COMPLETION_LATENCY_HIDDEN",
    "OBSERVATION_WITHOUT_HEAD_IDENTITY_ACCEPTED",
    "UNOBSERVED_TRANSIENT_TIP_CLAIMED_EXACTLY_OBSERVED",
    "REQUIRED_CASE_OR_BREAKER_UNMAPPED",
]


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def load_model():
    spec = importlib.util.spec_from_file_location("p5e_near_real_time_model_adv", MODEL)
    if spec is None or spec.loader is None:
        raise AssertionError("P5-E synthetic timing model unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def obs(scheduled, completed, outcome, head=None):
    return {
        "scheduled_at_seconds": scheduled,
        "completed_at_seconds": completed,
        "outcome": outcome,
        "observed_head": head,
    }


def assert_contract_invariants(contract):
    assert contract["schema"] == "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1"
    assert contract["status"] == "CANDIDATE_TARGETED_CLOSURE_PENDING_EXTERNAL_REREVIEW"
    assert contract["qualification_stage"] == "CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY"
    assert contract["real_p5e_execution_authorized"] is False
    assert contract["source_repository"] == "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"

    source = contract["monitored_source"]
    assert source["remote"] == "origin"
    assert source["branch"] == "integration/system-v1"
    assert source["canonical_authority"] == "GITHUB_REMOTE_BRANCH"
    assert source["local_working_tree_is_not_authority"] is True

    objective = contract["objective"]
    assert objective["this_stage_is_not_real_end_to_end_execution"] is True
    assert objective["this_stage_may_not_claim_continuous_synchronization"] is True

    timing = contract["near_real_time_timing"]
    assert timing["poll_interval_seconds"] == 30
    assert timing["detection_latency_seconds_max"] == 60
    assert timing["instantaneous_realtime_claim_forbidden"] is True
    assert timing["silent_interval_widening_forbidden"] is True
    assert timing["silent_latency_bound_widening_forbidden"] is True
    assert timing["delivery_semantics"] == "NEAR_REAL_TIME_BOUNDED_LATENCY"
    assert timing["detection_latency_definition"] == (
        "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC_MINUS_CONTROLLED_SOURCE_RELEASE_MONOTONIC"
    )
    assert timing["future_real_bound_clock"] == "MONOTONIC_ELAPSED_TIME"
    assert timing["future_real_wall_clock_may_be_recorded_as_evidence_only"] is True
    assert timing["latency_bound_breach_must_not_be_reported_as_near_real_time_pass"] is True
    assert timing["real_measurement_origin"] == "CONTROLLED_SOURCE_RELEASE_MONOTONIC"
    assert timing["measurement_endpoint"] == "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC"
    assert timing["schedule_semantics"] == "FIXED_RATE"
    assert timing["future_real_poll_schedule_semantics"] == "FIXED_RATE_30_SECOND_GRID"
    assert timing["remote_head_available_time_is_measurable_origin"] is False
    assert timing["attempt_start_and_read_completion_are_distinct"] is True
    assert timing["read_duration_is_included_in_detection_latency"] is True
    assert timing["eligible_detection_attempt_must_start_at_or_after_release"] is True
    assert timing["single_transient_read_failure_may_still_meet_60_second_bound"] is False
    assert timing[
        "single_transient_read_failure_may_meet_bound_only_if_read_completion_is_within_60_seconds"
    ] is True

    synthetic = contract["synthetic_timing_model"]
    assert synthetic["required"] is True
    assert synthetic["clock_source"] == "EXPLICIT_INJECTED_MONOTONIC_SECONDS_ONLY"
    assert synthetic["schedule_semantics"] == "FIXED_RATE"
    assert synthetic["schedule_origin_seconds"] == 0
    assert synthetic["sleep_forbidden"] is True
    assert synthetic["network_forbidden"] is True
    assert synthetic["filesystem_state_forbidden"] is True
    assert synthetic["process_launch_forbidden"] is True
    assert synthetic["environment_read_forbidden"] is True
    assert synthetic["real_p5d4_control_state_access_forbidden"] is True
    assert synthetic["real_vault_access_forbidden"] is True
    assert synthetic["observation_record_fields"] == [
        "scheduled_at_seconds",
        "completed_at_seconds",
        "outcome",
        "observed_head",
    ]
    assert synthetic["head_identity_required_on_successful_remote_observation"] is True
    assert synthetic["explicit_non_pass_statuses"] == ["INCOMPLETE_SYNTHETIC_WINDOW"]
    assert synthetic["attempt_overruns_next_required_slot_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert synthetic["attempt_overruns_next_required_slot_failure_code"] == "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT"
    assert synthetic["duplicate_fixed_rate_slot_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert synthetic["duplicate_fixed_rate_slot_failure_code"] == "DUPLICATE_FIXED_RATE_SLOT"
    assert synthetic["skipped_required_attempt_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert synthetic["cadence_gap_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert synthetic["pre_source_target_observation_result"] == "BLOCKED_REQUIRES_ADJUDICATION"

    transition = contract["head_transition_policy"]
    assert transition["same_head_result"] == "NOOP"
    assert transition["same_head_queue_growth_forbidden"] is True
    assert transition["initial_head_may_queue_exact_head_only_under_existing_p5d2_semantics"] is True
    assert transition["fast_forward_head_may_queue_exact_head_only_under_existing_p5d2_semantics"] is True
    assert transition["non_fast_forward_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert transition["non_fast_forward_auto_continue_forbidden"] is True
    assert transition["unknown_ancestry_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert transition["unknown_ancestry_auto_continue_forbidden"] is True
    assert transition["active_or_pending_candidate_retarget_forbidden"] is True

    queue = contract["queue_and_supersession"]
    assert queue["fifo_required"] is True
    assert queue["unique_heads_required"] is True
    assert queue["silent_drop_forbidden"] is True
    assert queue["silent_reorder_forbidden"] is True
    assert queue["latest_only_replacement_forbidden"] is True
    assert queue["coalescing_authorized"] is False
    assert queue["new_coalescing_semantic_event_authorized"] is False
    assert queue["pending_head_retarget_forbidden"] is True
    assert queue["capacity_exhausted_result"] == "QUEUE_CAPACITY_REQUIRES_ADJUDICATION"
    assert queue["capacity_exhausted_must_not_mutate_p5d2_state"] is True
    assert queue["burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification"] is True
    assert queue["precedence_rule"] == (
        "CURRENT_QUALIFIED_P5D4_EXECUTABLE_QUEUE_SEMANTICS_OVERRIDE_"
        "EARLIER_P5A_DESIGN_INTENT_WHERE_THEY_CONFLICT"
    )

    failure = contract["failure_and_freshness"]
    assert failure["fail_closed_default"] is True
    assert failure["network_failure_must_not_create_current_claim"] is True
    assert failure["last_known_good_live_projection_preserved"] is True
    assert failure["latency_bound_breach_result"] == "NEAR_REAL_TIME_BOUND_NOT_QUALIFIED"
    assert failure["queue_capacity_exhaustion_result"] == "QUEUE_CAPACITY_REQUIRES_ADJUDICATION"
    assert failure["non_fast_forward_or_unknown_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert failure["unexpected_state_or_timing_ambiguity_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert failure["timing_inconsistency_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert failure["skipped_required_attempt_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert failure["cadence_gap_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert failure["pre_source_target_observation_result"] == "BLOCKED_REQUIRES_ADJUDICATION"

    authority = contract["authority_boundary"]
    for field in (
        "observer_may_create_governance_authority",
        "pending_head_evaluation_authorized",
        "evaluation_authorized",
        "stage_a_authorized",
        "stage_b_authorized",
        "promotion_authorized",
        "publication_authorized",
        "real_vault_mutation_authorized",
        "current_mutation_authorized",
        "current_tmp_mutation_authorized",
        "real_polling_loop_authorized",
        "daemon_authorized",
        "startup_registration_authorized",
        "scheduled_task_authorized",
        "windows_service_authorized",
        "p6_authorized",
    ):
        assert authority[field] is False

    real_context = contract["real_context_evidence_only"]
    assert real_context["must_not_be_used_as_real_experiment_execution"] is True
    assert real_context["must_not_be_mutated_by_contract_qualification"] is True

    tips = contract["tip_visibility_semantics"]
    assert tips["observed_remote_tip_definition"] == "HEAD_IDENTITY_RETURNED_BY_A_SUCCESSFUL_REMOTE_READ"
    assert tips["unobserved_intermediate_tip_may_be_claimed_observed"] is False
    assert tips["unobserved_intermediate_tip_may_be_queued"] is False
    assert tips["fast_forward_content_containment_is_queue_coalescing"] is False
    assert tips["already_observed_queued_head_replacement_forbidden"] is True
    assert tips["already_observed_queued_head_retarget_forbidden"] is True
    assert tips["per_transient_tip_detection_sla_authorized"] is False
    assert tips["future_ancestry_enumeration_requires_separate_qualification"] is True
    assert tips["unobserved_intermediate_tip_non_injection_is_future_adapter_rule"] is True
    assert tips["unobserved_intermediate_tip_non_injection_is_current_runtime_qualified_property"] is False

    end_to_end = contract["end_to_end_definition"]
    assert end_to_end["real_end_to_end_stages"] == [
        "SOURCE_HEAD_BECOMES_OBSERVABLE",
        "REMOTE_HEAD_DETECTED_WITHIN_BOUND",
        "HEAD_TRANSITION_CLASSIFIED",
        "EXACT_HEAD_ENTERED_GOVERNED_QUEUE_OR_FAIL_CLOSED",
        "EXACT_HEAD_EVALUATED_IF_SEPARATELY_AUTHORIZED",
        "PROMOTION_DECISION_IF_SEPARATELY_AUTHORIZED",
        "PUBLICATION_IF_SEPARATELY_AUTHORIZED",
        "LIVE_GENERATION_VERIFIED_IF_PUBLICATION_AUTHORIZED",
    ]
    assert end_to_end["current_stage_may_qualify_only"] == [
        "TIMING_CONTRACT",
        "SYNTHETIC_FIXED_RATE_DETECTION_MODEL",
        "AUTHORITY_BOUNDARIES",
        "REUSED_MAPPED_P5D2_P5D4_FAIL_CLOSED_QUEUE_BEHAVIOR",
    ]
    assert end_to_end["real_end_to_end_pass_requires_all_authorized_applicable_stages"] is True
    assert end_to_end["omitted_unauthorized_downstream_stages_may_not_be_relabelled_pass"] is True
    assert end_to_end["transient_tip_exact_detection_sla_not_qualified"] is True
    assert end_to_end["real_remote_availability_to_detection_sla_not_qualified"] is True

    claims = contract["claim_boundary"]
    assert claims["maximum_current_claim"] == (
        "P5E_V0_1_TARGETED_CLOSURE_CANDIDATE_QUALIFIED_PENDING_EXTERNAL_REREVIEW"
    )
    assert claims["real_end_to_end_qualification_requires_separate_authorization"] is True
    forbidden = set(claims["forbidden_current_claims"])
    for claim in (
        "P5E_REAL_END_TO_END_QUALIFIED",
        "REAL_60_SECOND_SLA_QUALIFIED",
        "CONTINUOUS_SYNCHRONIZATION_QUALIFIED",
        "REMOTE_HEAD_AVAILABLE_TIME_TO_DETECTION_SLA_QUALIFIED",
        "PER_TRANSIENT_TIP_DETECTION_SLA_QUALIFIED",
    ):
        assert claim in forbidden

    gate = contract["next_gate_after_candidate_qualification"]
    assert gate["external_adversarial_review_required_before_normative_adoption"] is True
    assert gate["human_adjudication_required_after_external_review"] is True
    assert gate["p6_remains_closed"] is True
    assert gate["real_p5e_execution_requires_separate_human_authorization"] is True
    assert gate["external_adversarial_rereview_required"] is True
    assert gate["human_adjudication_before_external_rereview_forbidden"] is True

    assert contract["required_synthetic_cases"] == EXPECTED_CASES
    assert contract["required_breakers"] == EXPECTED_BASE_BREAKERS
    closure = contract["external_review_targeted_closure"]
    assert closure["required_breakers"] == EXPECTED_CLOSURE_BREAKERS
    assert closure["requirement_to_executable_evidence_matrix_required"] is True
    assert closure["all_required_cases_must_be_mapped"] is True
    assert closure["all_base_breakers_must_be_mapped"] is True
    assert closure["all_targeted_closure_breakers_must_be_mapped"] is True
    assert closure["unmapped_requirement_result"] == "BLOCKED"
    assert closure["external_rereview_required_before_human_normative_adoption"] is True


class TestP5EAdversarialV01(unittest.TestCase):
    def setUp(self):
        self.contract = load_contract()
        assert_contract_invariants(self.contract)

    def assert_mutation_rejected(self, mutator):
        candidate = copy.deepcopy(self.contract)
        mutator(candidate)
        with self.assertRaises(AssertionError):
            assert_contract_invariants(candidate)

    def test_timing_mutations_are_rejected(self):
        mutations = [
            lambda c: c["near_real_time_timing"].__setitem__("poll_interval_seconds", 31),
            lambda c: c["near_real_time_timing"].__setitem__("detection_latency_seconds_max", 61),
            lambda c: c["near_real_time_timing"].__setitem__("instantaneous_realtime_claim_forbidden", False),
            lambda c: c["near_real_time_timing"].__setitem__("schedule_semantics", "FIXED_DELAY"),
            lambda c: c["near_real_time_timing"].__setitem__("remote_head_available_time_is_measurable_origin", True),
            lambda c: c["near_real_time_timing"].__setitem__("read_duration_is_included_in_detection_latency", False),
        ]
        for mutator in mutations:
            self.assert_mutation_rejected(mutator)

    def test_previously_surviving_contract_mutations_are_rejected(self):
        mutations = [
            lambda c: c["head_transition_policy"].__setitem__("non_fast_forward_result", "AUTO_CONTINUE"),
            lambda c: c["head_transition_policy"].__setitem__("unknown_ancestry_auto_continue_forbidden", False),
            lambda c: c["head_transition_policy"].__setitem__("same_head_queue_growth_forbidden", False),
            lambda c: c["queue_and_supersession"].__setitem__("capacity_exhausted_must_not_mutate_p5d2_state", False),
            lambda c: c["synthetic_timing_model"].__setitem__("clock_source", "WALL_CLOCK"),
            lambda c: c["authority_boundary"].__setitem__("observer_may_create_governance_authority", True),
            lambda c: c["next_gate_after_candidate_qualification"].__setitem__("p6_remains_closed", False),
            lambda c: c.__setitem__("required_breakers", [f"FAKE_{i}" for i in range(25)]),
        ]
        for mutator in mutations:
            self.assert_mutation_rejected(mutator)

    def test_authority_mutations_are_rejected(self):
        for field in (
            "evaluation_authorized",
            "promotion_authorized",
            "publication_authorized",
            "real_vault_mutation_authorized",
            "real_polling_loop_authorized",
            "daemon_authorized",
            "startup_registration_authorized",
            "scheduled_task_authorized",
            "windows_service_authorized",
            "p6_authorized",
        ):
            self.assert_mutation_rejected(
                lambda c, field=field: c["authority_boundary"].__setitem__(field, True)
            )

    def test_queue_mutations_are_rejected(self):
        mutations = [
            lambda c: c["queue_and_supersession"].__setitem__("coalescing_authorized", True),
            lambda c: c["queue_and_supersession"].__setitem__("latest_only_replacement_forbidden", False),
            lambda c: c["queue_and_supersession"].__setitem__("pending_head_retarget_forbidden", False),
            lambda c: c["queue_and_supersession"].__setitem__("capacity_exhausted_result", "CONTINUE"),
        ]
        for mutator in mutations:
            self.assert_mutation_rejected(mutator)

    def test_claim_and_tip_mutations_are_rejected(self):
        mutations = [
            lambda c: c["claim_boundary"].__setitem__("maximum_current_claim", "P5E_REAL_END_TO_END_QUALIFIED"),
            lambda c: c["tip_visibility_semantics"].__setitem__("unobserved_intermediate_tip_may_be_claimed_observed", True),
            lambda c: c["tip_visibility_semantics"].__setitem__("per_transient_tip_detection_sla_authorized", True),
            lambda c: c["end_to_end_definition"]["current_stage_may_qualify_only"].append("REAL_END_TO_END"),
        ]
        for mutator in mutations:
            self.assert_mutation_rejected(mutator)

    def test_required_lists_cannot_be_reduced_or_replaced(self):
        self.assert_mutation_rejected(
            lambda c: c.__setitem__("required_synthetic_cases", ["SAME_HEAD_NOOP"])
        )
        self.assert_mutation_rejected(
            lambda c: c["external_review_targeted_closure"].__setitem__(
                "required_breakers", ["FAKE"]
            )
        )

    def test_synthetic_model_imports_are_ast_allowlisted(self):
        tree = ast.parse(MODEL.read_text(encoding="utf-8"))
        allowed = {"__future__", "typing"}
        forbidden_calls = {
            "open", "eval", "exec", "__import__", "compile", "input"
        }
        forbidden_attributes = {
            "sleep", "wait", "system", "popen", "Popen", "run",
            "connect", "request", "urlopen", "FileIO", "environ"
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertIn(alias.name.split(".")[0], allowed)
            elif isinstance(node, ast.ImportFrom):
                self.assertIn((node.module or "").split(".")[0], allowed)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, forbidden_calls)
                elif isinstance(node.func, ast.Attribute):
                    self.assertNotIn(node.func.attr, forbidden_attributes)
            elif isinstance(node, ast.Attribute):
                self.assertNotIn(node.attr, forbidden_attributes)

    def test_exact_60_second_completion_boundary_passes(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=0,
            target_head=TARGET,
            observations=[
                obs(30, 30, "READ_FAILURE"),
                obs(60, 60, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(result["detection_latency_seconds"], 60)

    def test_pre_source_target_observation_blocks(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=45,
            target_head=TARGET,
            observations=[
                obs(30, 31, "REMOTE_HEAD_OBSERVED", TARGET),
                obs(60, 61, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(
            result["failure_code"],
            "TARGET_HEAD_OBSERVED_BEFORE_CONTROLLED_RELEASE",
        )

    def test_invalid_source_release_values_are_rejected(self):
        m = load_model()
        for value in (-1, True):
            with self.assertRaises(m.P5ETimingModelError):
                m.qualify_detection(
                    plan=m.make_timing_plan(),
                    source_release_at_seconds=value,
                    target_head=TARGET,
                    observations=[obs(30, 30, "REMOTE_HEAD_OBSERVED", TARGET)],
                )

    def test_empty_observation_list_is_rejected(self):
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=0,
                target_head=TARGET,
                observations=[],
            )

    def test_invalid_observation_shape_and_head_are_rejected(self):
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=0,
                target_head=TARGET,
                observations=[obs(30, 30, "REMOTE_HEAD_OBSERVED", None)],
            )
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=0,
                target_head=TARGET,
                observations=[obs(30, 30, "PROMOTE", None)],
            )

    def test_cadence_duplicate_and_gap_are_blocked(self):
        m = load_model()
        for observations, code in (
            (
                [
                    obs(30, 30, "READ_FAILURE"),
                    obs(30, 30, "REMOTE_HEAD_OBSERVED", TARGET),
                ],
                "DUPLICATE_FIXED_RATE_SLOT",
            ),
            (
                [
                    obs(30, 30, "READ_FAILURE"),
                    obs(90, 90, "REMOTE_HEAD_OBSERVED", TARGET),
                ],
                "CADENCE_GAP",
            ),
        ):
            result = m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=1,
                target_head=TARGET,
                observations=observations,
            )
            self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
            self.assertEqual(result["failure_code"], code)

    def test_attempt_overlap_is_blocked(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                obs(30, 61, "READ_FAILURE"),
                obs(60, 62, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(result["failure_code"], "ATTEMPT_OVERLAP")

    def test_incomplete_window_does_not_claim_pass(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[obs(30, 31, "READ_FAILURE")],
        )
        self.assertEqual(result["status"], "INCOMPLETE_SYNTHETIC_WINDOW")
        self.assertFalse(result["real_end_to_end_qualified"])
        self.assertFalse(result["continuous_synchronization_qualified"])

    def test_all_result_paths_keep_downstream_authority_false(self):
        m = load_model()
        cases = [
            [obs(30, 30, "REMOTE_HEAD_OBSERVED", TARGET)],
            [obs(30, 31, "READ_FAILURE"), obs(60, 60, "READ_FAILURE")],
            [obs(30, 31, "READ_FAILURE"), obs(60, 62, "REMOTE_HEAD_OBSERVED", TARGET)],
            [obs(60, 61, "REMOTE_HEAD_OBSERVED", TARGET)],
        ]
        for observations in cases:
            result = m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=1,
                target_head=TARGET,
                observations=observations,
            )
            self.assertFalse(result["automatic_evaluation_authorized"])
            self.assertFalse(result["automatic_promotion_authorized"])
            self.assertFalse(result["automatic_publication_authorized"])

    def test_tip_visibility_does_not_launder_containment_into_exact_observation(self):
        m = load_model()
        self.assertEqual(
            m.classify_tip_visibility(
                target_head=TARGET,
                observed_head=OTHER,
                fast_forward_contains_target=True,
            ),
            "CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED",
        )
        self.assertEqual(
            m.classify_tip_visibility(
                target_head=TARGET,
                observed_head=OTHER,
                fast_forward_contains_target=False,
            ),
            "UNRELATED_OR_UNPROVEN_REQUIRES_ADJUDICATION",
        )


if __name__ == "__main__":
    unittest.main()

~~~~

# SOURCE: PRIOR B1-B5 TARGETED CLOSURE TESTS

Path: tests/obsidian_projection/test_p5e_external_review_targeted_closure_v0_1.py
~~~~
import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
MODEL = ROOT / "tools" / "obsidian_projection" / "p5e_near_real_time_model.py"
ADV = ROOT / "tests" / "obsidian_projection" / "test_p5e_end_to_end_near_real_time_adversarial_v0_1.py"

TARGET = "a" * 40
OTHER = "b" * 40

EXPECTED_CASES = [
    "SAME_HEAD_NOOP",
    "CHANGE_JUST_AFTER_POLL_DETECTED_AT_NEXT_30_SECOND_SLOT",
    "ONE_TRANSIENT_READ_FAILURE_THEN_DETECTED_BY_60_SECONDS",
    "DETECTION_AFTER_60_SECONDS_REJECTED",
    "NO_DETECTION_BY_60_SECONDS_REJECTED",
    "NON_FAST_FORWARD_BLOCKED",
    "UNKNOWN_ANCESTRY_BLOCKED",
    "PENDING_QUEUE_FULL_NEWER_HEAD_FAILS_CLOSED",
    "SAME_HEAD_DOES_NOT_GROW_QUEUE",
    "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD",
]

EXPECTED_BASE_BREAKERS = [
    "POLL_INTERVAL_NOT_EXACTLY_30_ACCEPTED",
    "DETECTION_BOUND_ABOVE_60_ACCEPTED",
    "INSTANTANEOUS_REALTIME_CLAIM_ACCEPTED",
    "WALL_CLOCK_USED_AS_SYNTHETIC_CONTROL_CLOCK",
    "SLEEP_USED_IN_SYNTHETIC_MODEL",
    "NETWORK_USED_IN_SYNTHETIC_MODEL",
    "FILESYSTEM_STATE_USED_IN_SYNTHETIC_MODEL",
    "PROCESS_LAUNCH_USED_IN_SYNTHETIC_MODEL",
    "SUCCESS_AFTER_60_SECONDS_CLASSIFIED_PASS",
    "NO_SUCCESS_BY_60_SECONDS_CLASSIFIED_PASS",
    "SAME_HEAD_GROWS_QUEUE",
    "NON_FAST_FORWARD_AUTO_CONTINUES",
    "UNKNOWN_ANCESTRY_AUTO_CONTINUES",
    "QUEUE_FULL_SILENTLY_DROPS_HEAD",
    "QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD",
    "QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT",
    "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD",
    "EVALUATION_AUTHORITY_BECOMES_TRUE",
    "PROMOTION_AUTHORITY_BECOMES_TRUE",
    "PUBLICATION_AUTHORITY_BECOMES_TRUE",
    "REAL_VAULT_MUTATION_AUTHORITY_BECOMES_TRUE",
    "REAL_POLLING_AUTHORITY_BECOMES_TRUE",
    "DAEMON_OR_SERVICE_AUTHORITY_BECOMES_TRUE",
    "P6_AUTHORITY_BECOMES_TRUE",
    "CONTRACT_PASS_LAUNDERS_INTO_REAL_P5E_PASS",
]

EXPECTED_CLOSURE_BREAKERS = [
    "SKIPPED_REQUIRED_ATTEMPT_ACCEPTED",
    "CADENCE_GAP_ACCEPTED",
    "PRE_SOURCE_TARGET_OBSERVATION_IGNORED",
    "REMOTE_AVAILABILITY_TIME_TREATED_AS_MEASURABLE_ORIGIN",
    "READ_COMPLETION_LATENCY_HIDDEN",
    "OBSERVATION_WITHOUT_HEAD_IDENTITY_ACCEPTED",
    "UNOBSERVED_TRANSIENT_TIP_CLAIMED_EXACTLY_OBSERVED",
    "REQUIRED_CASE_OR_BREAKER_UNMAPPED",
]


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def observation(scheduled, completed, outcome, observed_head=None):
    return {
        "scheduled_at_seconds": scheduled,
        "completed_at_seconds": completed,
        "outcome": outcome,
        "observed_head": observed_head,
    }


class TestP5EExternalReviewTargetedClosureV01(unittest.TestCase):
    def setUp(self):
        self.contract = load_json(CONTRACT)

    def test_b1_required_lists_are_exactly_frozen(self):
        self.assertEqual(self.contract["required_synthetic_cases"], EXPECTED_CASES)
        self.assertEqual(self.contract["required_breakers"], EXPECTED_BASE_BREAKERS)
        self.assertEqual(
            self.contract["external_review_targeted_closure"]["required_breakers"],
            EXPECTED_CLOSURE_BREAKERS,
        )

    def test_b1_adversarial_invariants_reject_previously_surviving_mutations(self):
        adv = load_module(ADV, "p5e_adv_for_closure")
        mutations = [
            lambda c: c["head_transition_policy"].__setitem__(
                "non_fast_forward_result", "AUTO_CONTINUE"
            ),
            lambda c: c["head_transition_policy"].__setitem__(
                "unknown_ancestry_auto_continue_forbidden", False
            ),
            lambda c: c["head_transition_policy"].__setitem__(
                "same_head_queue_growth_forbidden", False
            ),
            lambda c: c["queue_and_supersession"].__setitem__(
                "capacity_exhausted_must_not_mutate_p5d2_state", False
            ),
            lambda c: c["synthetic_timing_model"].__setitem__(
                "clock_source", "WALL_CLOCK"
            ),
            lambda c: c["authority_boundary"].__setitem__(
                "observer_may_create_governance_authority", True
            ),
            lambda c: c["next_gate_after_candidate_qualification"].__setitem__(
                "p6_remains_closed", False
            ),
            lambda c: c.__setitem__(
                "required_breakers", [f"FAKE_{i}" for i in range(25)]
            ),
        ]
        for mutator in mutations:
            candidate = copy.deepcopy(self.contract)
            mutator(candidate)
            with self.assertRaises(AssertionError):
                adv.assert_contract_invariants(candidate)

    def test_b4_contract_uses_falsifiable_local_monotonic_measurement(self):
        timing = self.contract["near_real_time_timing"]
        self.assertEqual(
            timing["real_measurement_origin"],
            "CONTROLLED_SOURCE_RELEASE_MONOTONIC",
        )
        self.assertEqual(
            timing["measurement_endpoint"],
            "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC",
        )
        self.assertEqual(timing["schedule_semantics"], "FIXED_RATE")
        self.assertFalse(
            timing["remote_head_available_time_is_measurable_origin"]
        )
        self.assertEqual(
            timing["real_latency_metric"],
            "REMOTE_READ_COMPLETION_MONOTONIC_MINUS_CONTROLLED_SOURCE_RELEASE_MONOTONIC",
        )

    def test_b5_contract_distinguishes_observed_tip_from_intermediate_commit(self):
        tip = self.contract["tip_visibility_semantics"]
        self.assertEqual(
            tip["observed_remote_tip_definition"],
            "HEAD_IDENTITY_RETURNED_BY_A_SUCCESSFUL_REMOTE_READ",
        )
        self.assertEqual(
            tip["intermediate_fast_forward_commit_definition"],
            "COMMIT_CONTAINED_BY_LATER_OBSERVED_FAST_FORWARD_HEAD_BUT_NOT_ITSELF_OBSERVED_AS_REMOTE_TIP",
        )
        self.assertFalse(tip["unobserved_intermediate_tip_may_be_claimed_observed"])
        self.assertFalse(tip["unobserved_intermediate_tip_may_be_queued"])
        self.assertFalse(tip["per_transient_tip_detection_sla_authorized"])
        self.assertTrue(tip["already_observed_queued_head_retarget_forbidden"])

    def test_b2_skipped_first_required_slot_blocks(self):
        m = load_module(MODEL, "p5e_model_b2_first")
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                observation(60, 61, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(result["failure_code"], "SKIPPED_REQUIRED_ATTEMPT")

    def test_b2_cadence_gap_blocks(self):
        m = load_module(MODEL, "p5e_model_b2_gap")
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                observation(30, 31, "READ_FAILURE"),
                observation(90, 91, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(result["failure_code"], "CADENCE_GAP")

    def test_b3_pre_source_target_observation_blocks(self):
        m = load_module(MODEL, "p5e_model_b3")
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=45,
            target_head=TARGET,
            observations=[
                observation(30, 31, "REMOTE_HEAD_OBSERVED", TARGET),
                observation(60, 61, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(
            result["failure_code"],
            "TARGET_HEAD_OBSERVED_BEFORE_CONTROLLED_RELEASE",
        )

    def test_b4_read_completion_not_poll_start_controls_latency(self):
        m = load_module(MODEL, "p5e_model_b4_duration")
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                observation(30, 31, "READ_FAILURE"),
                observation(60, 62, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(
            result["status"],
            "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
        )
        self.assertEqual(result["detection_latency_seconds"], 61)
        self.assertEqual(result["first_detection_completed_at_seconds"], 62)

    def test_non_aligned_source_failure_window_becomes_fail_when_future_slot_cannot_meet_bound(self):
        m = load_module(MODEL, "p5e_model_no_future")
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                observation(30, 31, "READ_FAILURE"),
                observation(60, 60, "READ_FAILURE"),
            ],
        )
        self.assertEqual(result["status"], "FAIL_NO_DETECTION_BY_BOUND")
        self.assertEqual(result["failure_code"], "NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND")

    def test_b5_observation_requires_head_identity(self):
        m = load_module(MODEL, "p5e_model_b5_identity")
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=1,
                target_head=TARGET,
                observations=[
                    observation(30, 31, "REMOTE_HEAD_OBSERVED", None),
                ],
            )

    def test_b5_exact_and_contained_tip_classifications_are_distinct(self):
        m = load_module(MODEL, "p5e_model_b5_visibility")
        self.assertEqual(
            m.classify_tip_visibility(
                target_head=TARGET,
                observed_head=TARGET,
                fast_forward_contains_target=False,
            ),
            "EXACT_TIP_OBSERVED",
        )
        self.assertEqual(
            m.classify_tip_visibility(
                target_head=TARGET,
                observed_head=OTHER,
                fast_forward_contains_target=True,
            ),
            "CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED",
        )
        self.assertEqual(
            m.classify_tip_visibility(
                target_head=TARGET,
                observed_head=OTHER,
                fast_forward_contains_target=False,
            ),
            "UNRELATED_OR_UNPROVEN_REQUIRES_ADJUDICATION",
        )

    def test_synthetic_model_imports_are_ast_allowlisted(self):
        import ast

        tree = ast.parse(MODEL.read_text(encoding="utf-8"))
        allowed = {"__future__", "typing"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertIn(alias.name.split(".")[0], allowed)
            elif isinstance(node, ast.ImportFrom):
                self.assertIn((node.module or "").split(".")[0], allowed)


if __name__ == "__main__":
    unittest.main()

~~~~

# SOURCE: EVIDENCE MATRIX TESTS

Path: tests/obsidian_projection/test_p5e_requirement_evidence_matrix_v0_1.py
~~~~
import subprocess
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
MODEL = ROOT / "tools" / "obsidian_projection" / "p5e_near_real_time_model.py"
MATRIX = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_requirement_evidence_matrix.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha1(path, relative_path):
    return subprocess.check_output(
        [
            "git",
            "hash-object",
            f"--path={relative_path}",
            str(path),
        ],
        cwd=ROOT,
        text=True,
    ).strip()


class TestP5ERequirementEvidenceMatrixV01(unittest.TestCase):
    def test_matrix_exists_and_schema_is_exact(self):
        self.assertTrue(MATRIX.is_file())
        m = load_json(MATRIX)
        self.assertEqual(
            m["schema"],
            "ATDS_OBSIDIAN_P5E_REQUIREMENT_EVIDENCE_MATRIX_V0_1",
        )
        self.assertEqual(
            m["qualification_scope"],
            "P5E_V0_1_EXTERNAL_REVIEW_TARGETED_CLOSURE",
        )
        self.assertFalse(m["real_p5e_execution_authorized"])

    def test_matrix_binds_exact_covered_contract_and_model(self):
        m = load_json(MATRIX)
        self.assertTrue(m["covered_object_drift_must_fail"])
        self.assertEqual(
            m["covered_contract_blob"],
            git_blob_sha1(
                CONTRACT,
                "tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json",
            ),
        )
        self.assertEqual(
            m["covered_model_blob"],
            git_blob_sha1(
                MODEL,
                "tools/obsidian_projection/p5e_near_real_time_model.py",
            ),
        )

    def test_every_required_case_and_breaker_is_mapped_exactly_once(self):
        c = load_json(CONTRACT)
        m = load_json(MATRIX)
        self.assertEqual(
            set(m["required_synthetic_cases"]),
            set(c["required_synthetic_cases"]),
        )
        self.assertEqual(
            set(m["base_breakers"]),
            set(c["required_breakers"]),
        )
        self.assertEqual(
            set(m["targeted_closure_breakers"]),
            set(c["external_review_targeted_closure"]["required_breakers"]),
        )
        self.assertEqual(
            len(m["required_synthetic_cases"]),
            len(c["required_synthetic_cases"]),
        )
        self.assertEqual(
            len(m["base_breakers"]),
            len(c["required_breakers"]),
        )
        self.assertEqual(
            len(m["targeted_closure_breakers"]),
            len(c["external_review_targeted_closure"]["required_breakers"]),
        )

    def test_all_mappings_bind_to_current_file_blobs_and_real_test_methods(self):
        m = load_json(MATRIX)
        sections = (
            "required_synthetic_cases",
            "base_breakers",
            "targeted_closure_breakers",
        )
        for section in sections:
            for requirement, entry in m[section].items():
                with self.subTest(section=section, requirement=requirement):
                    self.assertEqual(entry["verdict"], "PASS")
                    self.assertIn(
                        entry["evidence_kind"],
                        {"DIRECT_P5E", "REUSED_QUALIFIED_P5D2_P5D4"},
                    )
                    path = ROOT / entry["path"]
                    self.assertTrue(path.is_file(), entry["path"])
                    self.assertEqual(
                        entry["blob"],
                        git_blob_sha1(path, entry["path"]),
                    )
                    method = entry["test_method"].split(".")[-1]
                    text = path.read_text(encoding="utf-8")
                    self.assertIn(f"def {method}", text)

    def test_matrix_has_no_unmapped_or_deferred_requirements(self):
        m = load_json(MATRIX)
        summary = m["coverage_summary"]
        self.assertEqual(summary["unmapped"], 0)
        self.assertEqual(summary["deferred"], 0)
        self.assertEqual(summary["required_synthetic_cases_total"], 10)
        self.assertEqual(summary["base_breakers_total"], 25)
        self.assertEqual(summary["targeted_closure_breakers_total"], 8)
        self.assertEqual(summary["mapped_total"], 43)

    def test_matrix_does_not_claim_real_execution(self):
        m = load_json(MATRIX)
        self.assertFalse(m["real_p5e_execution_authorized"])
        self.assertFalse(m["real_60_second_sla_qualified"])
        self.assertFalse(m["per_transient_tip_detection_sla_qualified"])
        self.assertFalse(m["automatic_evaluation_authorized"])
        self.assertFalse(m["automatic_promotion_authorized"])
        self.assertFalse(m["automatic_publication_authorized"])


if __name__ == "__main__":
    unittest.main()

~~~~

# SOURCE: BB1 NORMATIVE GUARD CLOSURE TESTS

Path: tests/obsidian_projection/test_p5e_bb1_normative_guard_closure_v0_1.py
~~~~
import copy
import importlib.util
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
MODEL = ROOT / "tools" / "obsidian_projection" / "p5e_near_real_time_model.py"
MATRIX = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_requirement_evidence_matrix.json"
PREREG = ROOT / "tools" / "obsidian_projection" / "p5e_bb1_normative_guard_closure_preregistration_v0_1.json"
ADV = ROOT / "tests" / "obsidian_projection" / "test_p5e_end_to_end_near_real_time_adversarial_v0_1.py"

TARGET = "a" * 40


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_path(obj, dotted):
    cur = obj
    for key in dotted.split("."):
        cur = cur[key]
    return cur


def set_path(obj, dotted, value):
    parts = dotted.split(".")
    cur = obj
    for key in parts[:-1]:
        cur = cur[key]
    cur[parts[-1]] = value


def mutate(value):
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return "MUTATED"
    if isinstance(value, list):
        return value[:-1] if value else ["MUTATED"]
    raise AssertionError(f"unsupported normative leaf type: {type(value)}")


def git_blob(path):
    relative = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(
        ["git", "hash-object", f"--path={relative}", str(path)],
        cwd=ROOT,
        text=True,
    ).strip()


def obs(scheduled, completed, outcome, head=None):
    return {
        "scheduled_at_seconds": scheduled,
        "completed_at_seconds": completed,
        "outcome": outcome,
        "observed_head": head,
    }


class TestP5EBB1NormativeGuardClosureV01(unittest.TestCase):
    def setUp(self):
        self.contract = load_json(CONTRACT)
        self.prereg = load_json(PREREG)
        self.adv = load_module(ADV, "p5e_adv_bb1_closure")

    def test_preregistration_freezes_exact_leaf_sets(self):
        self.assertEqual(self.prereg["status"], "PREREGISTERED_BEFORE_RED")
        self.assertEqual(len(self.prereg["normative_leaf_set"]), 23)
        self.assertEqual(len(self.prereg["non_normative_metadata_set"]), 13)
        self.assertEqual(
            self.prereg["mutation_sweep_contract"]["exit_criterion"],
            "NORMATIVE_LEAF_MUTATIONS_SURVIVING_EQUALS_ZERO",
        )
        self.assertFalse(self.prereg["real_p5e_execution_authorized"])

    def test_all_preregistered_normative_leaf_mutations_are_rejected(self):
        survivors = []
        for dotted in self.prereg["normative_leaf_set"]:
            candidate = copy.deepcopy(self.contract)
            original = get_path(candidate, dotted)
            set_path(candidate, dotted, mutate(original))
            try:
                self.adv.assert_contract_invariants(candidate)
            except AssertionError:
                continue
            survivors.append(dotted)
        self.assertEqual(
            survivors,
            [],
            "normative mutations survived: " + ", ".join(survivors),
        )
    def test_combined_bb1_regression_is_rejected(self):
        candidate = copy.deepcopy(self.contract)
        changes = {
            "near_real_time_timing.detection_latency_definition":
                "FIRST_SUCCESSFUL_EXACT_REMOTE_HEAD_OBSERVATION_TIME_MINUS_SOURCE_HEAD_AVAILABLE_TIME",
            "near_real_time_timing.future_real_bound_clock": "WALL_CLOCK",
            "near_real_time_timing.future_real_wall_clock_may_be_recorded_as_evidence_only": False,
            "near_real_time_timing.latency_bound_breach_must_not_be_reported_as_near_real_time_pass": False,
            "monitored_source.branch": "main",
            "queue_and_supersession.burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification": False,
        }
        for dotted, value in changes.items():
            set_path(candidate, dotted, value)
        with self.assertRaises(AssertionError):
            self.adv.assert_contract_invariants(candidate)

    def test_matrix_binds_exact_contract_and_model_blobs(self):
        matrix = load_json(MATRIX)
        self.assertEqual(matrix["covered_contract_blob"], git_blob(CONTRACT))
        self.assertEqual(matrix["covered_model_blob"], git_blob(MODEL))
        self.assertTrue(matrix["covered_object_drift_must_fail"])

    def test_nb1_read_overrun_of_next_required_slot_blocks(self):
        model = load_module(MODEL, "p5e_model_bb1_nb1")
        result = model.qualify_detection(
            plan=model.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[obs(30, 61, "REMOTE_HEAD_OBSERVED", TARGET)],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(
            result["failure_code"],
            "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT",
        )

    def test_nb4_contract_marks_non_injection_as_future_adapter_rule_only(self):
        tips = self.contract["tip_visibility_semantics"]
        self.assertTrue(
            tips["unobserved_intermediate_tip_non_injection_is_future_adapter_rule"]
        )
        self.assertFalse(
            tips["unobserved_intermediate_tip_non_injection_is_current_runtime_qualified_property"]
        )

    def test_nb6_matrix_uses_behavioral_queue_capacity_evidence(self):
        matrix = load_json(MATRIX)
        for key in (
            "QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD",
            "QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT",
        ):
            entry = matrix["base_breakers"][key]
            self.assertEqual(
                entry["path"],
                "tests/obsidian_projection/test_p5d4_bounded_observer_loop_runtime_v0_1.py",
            )
            self.assertEqual(
                entry["test_method"],
                "P5D4RuntimeV01Tests.test_07_queue_capacity_blocks_before_tick",
            )
            self.assertEqual(
                entry["evidence_kind"],
                "REUSED_QUALIFIED_P5D2_P5D4",
            )

    def test_nb6_pending_non_active_mapping_is_semantically_exact(self):
        matrix = load_json(MATRIX)
        for key in (
            "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD",
            "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD",
        ):
            section = (
                matrix["required_synthetic_cases"]
                if key in matrix["required_synthetic_cases"]
                else matrix["base_breakers"]
            )
            entry = section[key]
            self.assertEqual(
                entry["test_method"],
                "ObserverTickTests.test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation",
            )
            self.assertEqual(
                entry["evidence_kind"],
                "REUSED_QUALIFIED_P5D2_P5D4",
            )
    def test_nb7_incomplete_window_is_explicit_non_pass(self):
        synthetic = self.contract["synthetic_timing_model"]
        self.assertIn(
            "INCOMPLETE_SYNTHETIC_WINDOW",
            synthetic["explicit_non_pass_statuses"],
        )

    def test_nb7_duplicate_slot_has_distinct_failure_code(self):
        model = load_module(MODEL, "p5e_model_bb1_nb7")
        result = model.qualify_detection(
            plan=model.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                obs(30, 30, "READ_FAILURE"),
                obs(30, 30, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(result["failure_code"], "DUPLICATE_FIXED_RATE_SLOT")


if __name__ == "__main__":
    unittest.main()

~~~~

# SOURCE: EVIDENCE MATRIX

Path: tools/obsidian_projection/p5e_v0_1_requirement_evidence_matrix.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_P5E_REQUIREMENT_EVIDENCE_MATRIX_V0_1",
  "qualification_scope": "P5E_V0_1_EXTERNAL_REVIEW_TARGETED_CLOSURE",
  "built_against_head": "95881afe5f03783de3c933d2c8ee65373220f3ed",
  "binding": "GIT_HASH_OBJECT_WITH_PATH_FILTERS",
  "real_p5e_execution_authorized": false,
  "real_60_second_sla_qualified": false,
  "per_transient_tip_detection_sla_qualified": false,
  "automatic_evaluation_authorized": false,
  "automatic_promotion_authorized": false,
  "automatic_publication_authorized": false,
  "required_synthetic_cases": {
    "SAME_HEAD_NOOP": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_same_head_is_strict_noop_for_queue",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "CHANGE_JUST_AFTER_POLL_DETECTED_AT_NEXT_30_SECOND_SLOT": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py",
      "test_method": "TestP5EContractV01.test_change_just_after_poll_is_detected_at_next_slot_completion",
      "blob": "a4fbd35987b4abb4fe185f8ceee3f75bd749e23d",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "ONE_TRANSIENT_READ_FAILURE_THEN_DETECTED_BY_60_SECONDS": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py",
      "test_method": "TestP5EContractV01.test_one_transient_failure_can_pass_only_by_completion_within_60",
      "blob": "a4fbd35987b4abb4fe185f8ceee3f75bd749e23d",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "DETECTION_AFTER_60_SECONDS_REJECTED": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py",
      "test_method": "TestP5EContractV01.test_read_completion_after_60_is_rejected",
      "blob": "a4fbd35987b4abb4fe185f8ceee3f75bd749e23d",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "NO_DETECTION_BY_60_SECONDS_REJECTED": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py",
      "test_method": "TestP5EContractV01.test_no_detection_fails_when_next_fixed_rate_slot_cannot_meet_bound",
      "blob": "a4fbd35987b4abb4fe185f8ceee3f75bd749e23d",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "NON_FAST_FORWARD_BLOCKED": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_non_fast_forward_blocks_without_queueing",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "UNKNOWN_ANCESTRY_BLOCKED": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_unknown_ancestry_blocks_without_queueing",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "PENDING_QUEUE_FULL_NEWER_HEAD_FAILS_CLOSED": {
      "path": "tests/obsidian_projection/test_p5d4_bounded_observer_loop_runtime_v0_1.py",
      "test_method": "P5D4RuntimeV01Tests.test_07_queue_capacity_blocks_before_tick",
      "blob": "5bcc563487ca8c64a1afde9f022504b2b618af7b",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "SAME_HEAD_DOES_NOT_GROW_QUEUE": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_same_head_is_strict_noop_for_queue",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    }
  },
  "base_breakers": {
    "POLL_INTERVAL_NOT_EXACTLY_30_ACCEPTED": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_timing_mutations_are_rejected",
      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "DETECTION_BOUND_ABOVE_60_ACCEPTED": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_timing_mutations_are_rejected",
      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "INSTANTANEOUS_REALTIME_CLAIM_ACCEPTED": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_timing_mutations_are_rejected",
      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "WALL_CLOCK_USED_AS_SYNTHETIC_CONTROL_CLOCK": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_previously_surviving_contract_mutations_are_rejected",
      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "SLEEP_USED_IN_SYNTHETIC_MODEL": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_synthetic_model_imports_are_ast_allowlisted",
      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "NETWORK_USED_IN_SYNTHETIC_MODEL": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_synthetic_model_imports_are_ast_allowlisted",
      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "FILESYSTEM_STATE_USED_IN_SYNTHETIC_MODEL": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_synthetic_model_imports_are_ast_allowlisted",
      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "PROCESS_LAUNCH_USED_IN_SYNTHETIC_MODEL": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_synthetic_model_imports_are_ast_allowlisted",
      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "SUCCESS_AFTER_60_SECONDS_CLASSIFIED_PASS": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py",
      "test_method": "TestP5EContractV01.test_read_completion_after_60_is_rejected",
      "blob": "a4fbd35987b4abb4fe185f8ceee3f75bd749e23d",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "NO_SUCCESS_BY_60_SECONDS_CLASSIFIED_PASS": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py",
      "test_method": "TestP5EContractV01.test_no_detection_fails_when_next_fixed_rate_slot_cannot_meet_bound",
      "blob": "a4fbd35987b4abb4fe185f8ceee3f75bd749e23d",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "SAME_HEAD_GROWS_QUEUE": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_same_head_is_strict_noop_for_queue",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "NON_FAST_FORWARD_AUTO_CONTINUES": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_non_fast_forward_blocks_without_queueing",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "UNKNOWN_ANCESTRY_AUTO_CONTINUES": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_unknown_ancestry_blocks_without_queueing",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "QUEUE_FULL_SILENTLY_DROPS_HEAD": {
      "path": "tests/obsidian_projection/test_p5d4_bounded_observer_loop_runtime_v0_1.py",
      "test_method": "P5D4RuntimeV01Tests.test_07_queue_capacity_blocks_before_tick",
      "blob": "5bcc563487ca8c64a1afde9f022504b2b618af7b",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD": {
      "path": "tests/obsidian_projection/test_p5d4_bounded_observer_loop_runtime_v0_1.py",
      "test_method": "P5D4RuntimeV01Tests.test_07_queue_capacity_blocks_before_tick",
      "blob": "5bcc563487ca8c64a1afde9f022504b2b618af7b",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT": {
      "path": "tests/obsidian_projection/test_p5d4_bounded_observer_loop_runtime_v0_1.py",
      "test_method": "P5D4RuntimeV01Tests.test_07_queue_capacity_blocks_before_tick",
      "blob": "5bcc563487ca8c64a1afde9f022504b2b618af7b",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "EVALUATION_AUTHORITY_BECOMES_TRUE": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "PROMOTION_AUTHORITY_BECOMES_TRUE": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "PUBLICATION_AUTHORITY_BECOMES_TRUE": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "REAL_VAULT_MUTATION_AUTHORITY_BECOMES_TRUE": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "REAL_POLLING_AUTHORITY_BECOMES_TRUE": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "DAEMON_OR_SERVICE_AUTHORITY_BECOMES_TRUE": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "P6_AUTHORITY_BECOMES_TRUE": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "CONTRACT_PASS_LAUNDERS_INTO_REAL_P5E_PASS": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_claim_and_tip_mutations_are_rejected",
      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    }
  },
  "targeted_closure_breakers": {
    "SKIPPED_REQUIRED_ATTEMPT_ACCEPTED": {
      "path": "tests/obsidian_projection/test_p5e_external_review_targeted_closure_v0_1.py",
      "test_method": "TestP5EExternalReviewTargetedClosureV01.test_b2_skipped_first_required_slot_blocks",
      "blob": "15c3e44ab9c1c40873110d88ff42cebb13a2643e",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "CADENCE_GAP_ACCEPTED": {
      "path": "tests/obsidian_projection/test_p5e_external_review_targeted_closure_v0_1.py",
      "test_method": "TestP5EExternalReviewTargetedClosureV01.test_b2_cadence_gap_blocks",
      "blob": "15c3e44ab9c1c40873110d88ff42cebb13a2643e",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "PRE_SOURCE_TARGET_OBSERVATION_IGNORED": {
      "path": "tests/obsidian_projection/test_p5e_external_review_targeted_closure_v0_1.py",
      "test_method": "TestP5EExternalReviewTargetedClosureV01.test_b3_pre_source_target_observation_blocks",
      "blob": "15c3e44ab9c1c40873110d88ff42cebb13a2643e",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "REMOTE_AVAILABILITY_TIME_TREATED_AS_MEASURABLE_ORIGIN": {
      "path": "tests/obsidian_projection/test_p5e_external_review_targeted_closure_v0_1.py",
      "test_method": "TestP5EExternalReviewTargetedClosureV01.test_b4_contract_uses_falsifiable_local_monotonic_measurement",
      "blob": "15c3e44ab9c1c40873110d88ff42cebb13a2643e",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "READ_COMPLETION_LATENCY_HIDDEN": {
      "path": "tests/obsidian_projection/test_p5e_external_review_targeted_closure_v0_1.py",
      "test_method": "TestP5EExternalReviewTargetedClosureV01.test_b4_read_completion_not_poll_start_controls_latency",
      "blob": "15c3e44ab9c1c40873110d88ff42cebb13a2643e",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "OBSERVATION_WITHOUT_HEAD_IDENTITY_ACCEPTED": {
      "path": "tests/obsidian_projection/test_p5e_external_review_targeted_closure_v0_1.py",
      "test_method": "TestP5EExternalReviewTargetedClosureV01.test_b5_observation_requires_head_identity",
      "blob": "15c3e44ab9c1c40873110d88ff42cebb13a2643e",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "UNOBSERVED_TRANSIENT_TIP_CLAIMED_EXACTLY_OBSERVED": {
      "path": "tests/obsidian_projection/test_p5e_external_review_targeted_closure_v0_1.py",
      "test_method": "TestP5EExternalReviewTargetedClosureV01.test_b5_exact_and_contained_tip_classifications_are_distinct",
      "blob": "15c3e44ab9c1c40873110d88ff42cebb13a2643e",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "REQUIRED_CASE_OR_BREAKER_UNMAPPED": {
      "path": "tests/obsidian_projection/test_p5e_requirement_evidence_matrix_v0_1.py",
      "test_method": "TestP5ERequirementEvidenceMatrixV01.test_matrix_has_no_unmapped_or_deferred_requirements",
      "blob": "182a7b60b440ddb8d5c0c9fdc65f423309383244",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    }
  },
  "coverage_summary": {
    "required_synthetic_cases_total": 10,
    "base_breakers_total": 25,
    "targeted_closure_breakers_total": 8,
    "mapped_total": 43,
    "unmapped": 0,
    "deferred": 0
  },
  "covered_contract_blob": "7e3e18ba946246065b43bc5fbabdc35980140eb9",
  "covered_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
  "covered_object_drift_must_fail": true
}

~~~~

# SOURCE: P5-A CONTINUOUS PROJECTION CONTRACT

Path: tools/obsidian_projection/continuous_projection_contract_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_CONTINUOUS_PROJECTION_CONTRACT_V0_1",
  "status": "CANDIDATE_PREREGISTRATION_ONLY",
  "source_repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "predecessor_p4c_head": "10355f467ccf8f87070ab18839b96ba6fc547d9d",
  "monitored_source": {
    "remote": "origin",
    "branch": "integration/system-v1",
    "observed_head_at_preregistration": "6aef3b1304313c3446c08a3a37b51ea61733f41e",
    "canonical_authority": "GITHUB_REMOTE_BRANCH",
    "local_working_tree_is_not_authority": true
  },
  "objective": {
    "name": "CONTINUOUS_GITHUB_TO_OBSIDIAN_PROJECTION",
    "user_goal": "Every governed GitHub update on the monitored ATDS branch becomes visible in Obsidian without manual projection rebuild.",
    "delivery_semantics": "NEAR_REAL_TIME_BOUNDED_LATENCY",
    "instantaneous_realtime_claim_forbidden": true,
    "target_detection_latency_seconds_max": 60,
    "implementation_poll_interval_seconds_candidate": 30
  },
  "architecture_choice": {
    "selected_candidate": "LOCAL_REMOTE_REF_OBSERVER",
    "rationale": [
      "The qualified Vault is local Windows/OneDrive storage.",
      "GitHub Actions cannot directly mutate the user's local Vault.",
      "A GitHub webhook would require an inbound endpoint and additional infrastructure.",
      "Obsidian Git automation would violate the existing authority and persistence boundary.",
      "A local remote-ref observer can remain read-only toward GitHub and write only the derived projection."
    ],
    "rejected_initial_mechanisms": [
      "OBSIDIAN_GIT_AUTO_PULL_PUSH",
      "GITHUB_ACTION_DIRECT_TO_LOCAL_VAULT",
      "PUBLIC_WEBHOOK_ENDPOINT_REQUIRED"
    ],
    "webhook_may_be_reconsidered_later": true
  },
  "authority_boundary": {
    "github_remote_branch": "CANONICAL",
    "canonical_local_checkout": "READ_ONLY_EXECUTION_INPUT",
    "projection": "DERIVED",
    "obsidian": "OBSERVE_NAVIGATE_QUERY_VISUALIZE_UNDERSTAND",
    "observer_may_push_to_github": false,
    "observer_may_commit_to_github": false,
    "observer_may_modify_canonical_worktree": false,
    "observer_may_create_operational_authority": false
  },
  "runtime_isolation": {
    "canonical_user_repo_mutation_forbidden": true,
    "build_checkout_location": "OS_TEMP_OR_DEDICATED_NON_VAULT_CONTROL_ROOT",
    "build_checkout_must_be_disposable": true,
    "build_checkout_must_resolve_exact_repo_origin": true,
    "build_checkout_must_resolve_exact_target_commit": true,
    "build_must_not_use_user_worktree_registry": true,
    "vault_must_not_contain_git_directory": true
  },
  "remote_observation": {
    "operation_class": "READ_ONLY_REMOTE_REF_CHECK",
    "permitted_examples": [
      "git ls-remote origin refs/heads/integration/system-v1",
      "git fetch --no-tags origin integration/system-v1"
    ],
    "full_fetch_on_every_poll_required": false,
    "credentials_must_not_be_logged": true,
    "network_failure_result": "NO_PROMOTION_KEEP_LAST_KNOWN_GOOD",
    "repeated_same_head_result": "NOOP",
    "new_head_result": "QUEUE_EXACT_HEAD_FOR_QUALIFICATION"
  },
  "head_transition_policy": {
    "classify_transition": [
      "INITIAL",
      "FAST_FORWARD",
      "NON_FAST_FORWARD",
      "UNKNOWN"
    ],
    "automatic_promotion_allowed_for": [
      "INITIAL",
      "FAST_FORWARD"
    ],
    "non_fast_forward_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "unknown_ancestry_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "silent_history_rewrite_acceptance_forbidden": true
  },
  "event_coalescing": {
    "every_observed_head_must_be_logged": true,
    "active_build_may_finish_against_its_exact_head": true,
    "newer_head_arriving_during_build_must_be_queued": true,
    "superseded_heads_may_skip_projection_only_if_fast_forward_contained_by_later_head": true,
    "skipped_head_status": "SUPERSEDED_NOT_PROMOTED",
    "latest_head_must_eventually_be_evaluated": true
  },
  "current_head_projection_prerequisite": {
    "frozen_pilot_inventory_is_insufficient_for_continuous_mode": true,
    "continuous_mode_requires_dynamic_inventory_for_each_exact_head": true,
    "inventory_scope_candidate": [
      "GOVERNANCE",
      "docs",
      "evidence",
      "reports",
      "requirements",
      "src",
      "tests",
      "tools",
      "breakers",
      ".github/workflows"
    ],
    "binary_or_large_artifact_policy_must_be_explicit": true,
    "secrets_and_credentials_must_never_be_projected": true,
    "source_selection_contract_required_before_runtime": true
  },
  "qualification_pipeline": {
    "ordered_gates": [
      "OBSERVE_REMOTE_HEAD",
      "VERIFY_REPOSITORY_IDENTITY",
      "CLASSIFY_HEAD_TRANSITION",
      "FETCH_EXACT_HEAD",
      "CREATE_ISOLATED_CHECKOUT",
      "BUILD_DYNAMIC_INVENTORY",
      "CLASSIFY_ARTIFACTS",
      "BUILD_DETERMINISTIC_PROJECTION_A",
      "BUILD_DETERMINISTIC_PROJECTION_B",
      "REQUIRE_A_EQUALS_B",
      "RUN_PROJECTION_BREAKERS",
      "BUILD_MACHINE_VIEW_LAYER_IF_AUTHORIZED",
      "STAGE_COMPLETE_GENERATION",
      "VERIFY_STAGED_GENERATION",
      "PROMOTE_ATOMICALLY_OR_BLOCK",
      "VERIFY_LIVE_GENERATION",
      "RECORD_EVENT_AND_STATE"
    ],
    "any_gate_failure_result": "NO_PROMOTION_KEEP_LAST_KNOWN_GOOD",
    "partial_success_may_not_be_promoted": true
  },
  "generation_identity": {
    "required_fields": [
      "repository",
      "branch",
      "source_head",
      "source_tree",
      "projection_contract_version",
      "inventory_digest",
      "semantic_record_digest",
      "projection_tree_digest",
      "generated_file_count",
      "qualified_at_state_transition"
    ],
    "volatile_host_data_in_deterministic_tree_forbidden": true,
    "source_head_must_match_built_checkout_head": true
  },
  "projection_states": {
    "allowed": [
      "CURRENT",
      "STALE",
      "BLOCKED",
      "ORPHAN",
      "MISSING"
    ],
    "current_definition": "LIVE_PROJECTION_SOURCE_HEAD_EQUALS_LATEST_QUALIFIED_MONITORED_REMOTE_HEAD",
    "stale_definition": "REMOTE_HEAD_IS_NEWER_THAN_LIVE_PROJECTION_HEAD_OR_LATEST_HEAD_NOT_YET_PROMOTED",
    "blocked_definition": "LATEST_OBSERVED_HEAD_FAILED_OR_REQUIRES_ADJUDICATION",
    "orphan_definition": "DERIVED_ARTIFACT_SOURCE_NO_LONGER_EXISTS_IN_CURRENT_QUALIFIED_SOURCE_TREE",
    "missing_definition": "EXPECTED_DERIVED_ARTIFACT_IS_ABSENT",
    "unknown_must_not_be_mapped_to_current": true
  },
  "last_known_good": {
    "required": true,
    "live_projection_must_remain_usable_on_failure": true,
    "failed_candidate_must_not_modify_live_projection": true,
    "failed_candidate_evidence_must_be_preserved_outside_live_projection": true,
    "last_known_good_source_head_must_be_recorded": true
  },
  "promotion_atomicity": {
    "mixed_generation_visibility_forbidden": true,
    "direct_in_place_multi_file_overwrite_forbidden": true,
    "staging_required": true,
    "candidate_mechanism": "STAGED_GENERATION_SWAP_OR_EQUIVALENT_ATOMIC_VISIBILITY_PRIMITIVE",
    "exact_windows_onedrive_mechanism_not_yet_qualified": true,
    "obsidian_open_during_promotion_not_yet_authorized": true,
    "empirical_promotion_primitive_qualification_required": true
  },
  "vault_policy": {
    "vault_path": "C:\\Users\\Boulevart\\OneDrive\\Bureau\\ATDS\\ATDS-OBSIDIAN-PROJECTION",
    "generated_owner": "MACHINE",
    "views_owner": "HUMAN",
    "obsidian_config_owner": "OBSIDIAN_UI",
    "observer_may_write_generated_only_after_promotion_gate": true,
    "observer_may_overwrite_human_views": false,
    "observer_may_modify_obsidian_config": false,
    "observer_may_enable_obsidian_sync": false,
    "observer_may_install_plugins": false
  },
  "machine_visual_layer_future_policy": {
    "continuous_visual_refresh_required_for_final_goal": true,
    "current_human_views_must_not_be_silently_overwritten": true,
    "future_machine_managed_visual_namespace_required": true,
    "candidate_namespace": "generated/live",
    "bases_graph_canvas_dashboards_may_be_generated_only_after_separate_contract": true,
    "human_views_may_link_to_machine_live_views": true
  },
  "runtime_state_storage": {
    "deterministic_projection_state_inside_generated_allowed": true,
    "volatile_daemon_state_location": "LOCALAPPDATA_OUTSIDE_VAULT",
    "append_only_event_log_required": true,
    "minimum_event_fields": [
      "observed_at",
      "remote_head",
      "previous_live_head",
      "transition_class",
      "pipeline_result",
      "live_head_after",
      "projection_state",
      "failure_code"
    ],
    "event_log_is_not_semantic_authority": true
  },
  "concurrency": {
    "single_promotion_writer_required": true,
    "lock_scope": "CONTINUOUS_PROJECTION_ENGINE",
    "second_instance_result": "NO_WRITE_BLOCKED_BY_LOCK",
    "obsidian_readers_must_never_observe_partial_generation": true
  },
  "recovery": {
    "crash_before_promotion": "DISCARD_OR_PRESERVE_STAGING_NO_LIVE_CHANGE",
    "crash_during_unqualified_atomic_primitive": "BLOCK_CONTINUOUS_MODE_UNTIL_ADJUDICATED",
    "crash_after_promotion_before_state_log": "RECONSTRUCT_STATE_FROM_LIVE_GENERATION_IDENTITY",
    "no_recursive_delete_of_last_known_good": true
  },
  "observability": {
    "health_report_required": true,
    "fields": [
      "observer_running",
      "latest_remote_head",
      "live_projection_head",
      "projection_state",
      "last_success_time",
      "last_failure_time",
      "last_failure_code",
      "queued_head_count"
    ],
    "current_state_must_be_visible_in_obsidian_later": true,
    "current_state_visibility_must_not_create_authority": true
  },
  "p5a_boundary": {
    "contract_tests_and_architecture_only": true,
    "background_observer_execution_authorized": false,
    "remote_polling_loop_authorized": false,
    "vault_continuous_write_authorized": false,
    "generated_replacement_authorized": false,
    "human_views_overwrite_authorized": false,
    "windows_startup_registration_authorized": false,
    "scheduled_task_creation_authorized": false
  },
  "required_breakers": [
    "observer pushes to GitHub",
    "observer commits to canonical repository",
    "canonical user working tree is mutated",
    "wrong repository origin accepted",
    "wrong monitored branch accepted",
    "build checkout HEAD differs from observed remote HEAD",
    "same HEAD triggers rebuild",
    "non-fast-forward silently auto-promoted",
    "unknown ancestry silently auto-promoted",
    "frozen 74-artifact pilot treated as sufficient dynamic inventory",
    "secret or credential projected",
    "single build accepted without deterministic double-build comparison",
    "failed candidate mutates live projection",
    "partial candidate promoted",
    "mixed generations visible",
    "direct in-place multi-file overwrite used as promotion",
    "last-known-good deleted before new generation verified",
    "human views overwritten",
    ".obsidian modified by observer",
    "Obsidian Sync enabled",
    "community plugin required",
    "Git automation inside Vault enabled",
    "volatile daemon data changes deterministic digest",
    "remote network failure marks projection CURRENT",
    "UNKNOWN mapped to CURRENT",
    "STALE silently presented as CURRENT",
    "second writer bypasses engine lock",
    "event history lost for observed HEAD",
    "superseded HEAD omitted without fast-forward containment",
    "latest queued HEAD never evaluated",
    "atomic promotion primitive assumed without Windows/OneDrive evidence",
    "Obsidian-open promotion assumed safe without empirical qualification"
  ],
  "next_gates": {
    "p5b": "DYNAMIC_CURRENT_HEAD_INVENTORY_AND_SOURCE_SELECTION_CONTRACT",
    "p5c": "WINDOWS_ONEDRIVE_ATOMIC_PROMOTION_PRIMITIVE_QUALIFICATION",
    "p5d": "CONTINUOUS_OBSERVER_IMPLEMENTATION_CANDIDATE",
    "p5e": "END_TO_END_NEAR_REAL_TIME_QUALIFICATION"
  }
}

~~~~

# SOURCE: P5-D2 ONE-SHOT OBSERVER CONTRACT

Path: tools/obsidian_projection/one_shot_observer_tick_contract_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_ONE_SHOT_OBSERVER_TICK_CONTRACT_V0_1",
  "status": "CANDIDATE_PREREGISTRATION_ONLY",
  "source_repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "monitored_branch": "integration/system-v1",
  "qualified_predecessor": {
    "p5d1_contract_blob": "a20999ae991e07447e25ecd1592964f2d333449b",
    "p5d1_qualification_report_blob": "fbe4a60f2349a96bf7a1f4c5dea0eb28328af841",
    "p5d1_qualification_commit": "dce36303982d73a37d8498400f0a13e708e841b6"
  },
  "objective": {
    "name": "ONE_SHOT_DETERMINISTIC_OBSERVER_TICK",
    "input": "previous_state_plus_one_normalized_input",
    "output": "next_state_plus_decision_plus_audit_record",
    "exactly_one_transition_per_invocation": true,
    "repeated_tick_loop_forbidden": true,
    "sleep_forbidden": true,
    "background_execution_forbidden": true,
    "network_io_forbidden": true,
    "filesystem_io_forbidden": true,
    "process_launch_forbidden": true,
    "environment_read_forbidden": true,
    "wall_clock_read_forbidden": true,
    "randomness_forbidden": true
  },
  "schemas": {
    "state": "ATDS_OBSIDIAN_OBSERVER_STATE_V0_1",
    "input": "ATDS_OBSIDIAN_OBSERVER_INPUT_V0_1",
    "decision": "ATDS_OBSIDIAN_OBSERVER_DECISION_V0_1",
    "audit": "ATDS_OBSIDIAN_OBSERVER_EVENT_V0_1",
    "tick_result": "ATDS_OBSIDIAN_ONE_SHOT_TICK_RESULT_V0_1"
  },
  "canonicalization": {
    "encoding": "UTF-8",
    "json": "SORT_KEYS_COMPACT",
    "line_termination": "LF",
    "terminal_lf_required": true,
    "digest_algorithm": "SHA256",
    "unicode_normalization": "INPUT_MUST_ALREADY_BE_NORMALIZED",
    "non_json_values_forbidden": true
  },
  "state_validation": {
    "repository_exact": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
    "branch_exact": "integration/system-v1",
    "observer_phase_allowed": [
      "IDLE",
      "CANDIDATE_PENDING",
      "EVALUATING",
      "BLOCKED",
      "STOPPED"
    ],
    "remote_freshness_allowed": [
      "KNOWN",
      "UNKNOWN"
    ],
    "projection_state_allowed": [
      "CURRENT",
      "STALE",
      "BLOCKED",
      "ORPHAN",
      "MISSING"
    ],
    "head_format": "LOWERCASE_40_HEX_SHA1_OR_NULL",
    "pending_heads": "FIFO_UNIQUE_LOWERCASE_40_HEX",
    "last_event_sequence": "NONNEGATIVE_INTEGER",
    "current_requires": [
      "remote_freshness == KNOWN",
      "latest_observed_head == live_projection_head",
      "live_projection_head == last_qualified_head",
      "live_projection_head != null"
    ],
    "evaluating_requires_nonempty_pending_queue": true,
    "candidate_pending_requires_last_qualified_head": true,
    "blocked_phase_requires_projection_blocked": true,
    "blocked_phase_requires_blocked_head": true,
    "blocked_phase_requires_failure_code": true
  },
  "normalized_input": {
    "required_fields": [
      "schema",
      "event_type",
      "sequence",
      "observed_head",
      "transition_class",
      "candidate_head",
      "failure_code"
    ],
    "event_types": [
      "BOOTSTRAP",
      "REMOTE_HEAD_OBSERVED",
      "REMOTE_OBSERVATION_FAILED",
      "EVALUATION_STARTED",
      "EVALUATION_PASSED",
      "EVALUATION_FAILED",
      "PROMOTION_CONFIRMED",
      "PROMOTION_FAILED",
      "LOCK_CONTENDED",
      "SHUTDOWN_REQUESTED"
    ],
    "transition_classes": [
      "INITIAL",
      "SAME",
      "FAST_FORWARD",
      "NON_FAST_FORWARD",
      "UNKNOWN"
    ],
    "sequence_rule": "input.sequence == previous_state.last_event_sequence + 1",
    "transition_class_state_consistency": {
      "INITIAL": "previous latest_observed_head must be null",
      "SAME": "observed_head must equal previous latest_observed_head",
      "FAST_FORWARD": "previous latest_observed_head must exist and differ from observed_head",
      "NON_FAST_FORWARD": "previous latest_observed_head must exist and differ from observed_head",
      "UNKNOWN": "previous latest_observed_head must exist and differ from observed_head"
    },
    "extra_fields_forbidden": true,
    "event_specific_rules": {
      "BOOTSTRAP": {
        "observed_head": null,
        "transition_class": null,
        "candidate_head": null,
        "failure_code": null
      },
      "REMOTE_HEAD_OBSERVED": {
        "observed_head_required": true,
        "transition_class_required": true,
        "candidate_head": null,
        "failure_code": null
      },
      "REMOTE_OBSERVATION_FAILED": {
        "observed_head": null,
        "transition_class": null,
        "candidate_head": null,
        "failure_code_required": true
      },
      "EVALUATION_STARTED": {
        "observed_head": null,
        "transition_class": null,
        "candidate_head_required": true,
        "failure_code": null
      },
      "EVALUATION_PASSED": {
        "observed_head": null,
        "transition_class": null,
        "candidate_head_required": true,
        "failure_code": null
      },
      "EVALUATION_FAILED": {
        "observed_head": null,
        "transition_class": null,
        "candidate_head_required": true,
        "failure_code_required": true
      },
      "PROMOTION_CONFIRMED": {
        "observed_head": null,
        "transition_class": null,
        "candidate_head_required": true,
        "failure_code": null,
        "external_confirmation_only": true
      },
      "PROMOTION_FAILED": {
        "observed_head": null,
        "transition_class": null,
        "candidate_head_required": true,
        "failure_code_required": true,
        "external_confirmation_only": true
      },
      "LOCK_CONTENDED": {
        "observed_head": null,
        "transition_class": null,
        "candidate_head": null,
        "failure_code": "LOCK_CONTENDED"
      },
      "SHUTDOWN_REQUESTED": {
        "observed_head": null,
        "transition_class": null,
        "candidate_head": null,
        "failure_code": null
      }
    }
  },
  "transition_semantics": {
    "BOOTSTRAP": {
      "allowed_only_when_last_event_sequence_zero": true,
      "requires_canonical_initial_state": true,
      "action": "NOOP",
      "state_unchanged_except_sequence": true
    },
    "REMOTE_HEAD_OBSERVED_WHILE_BLOCKED": {
      "action": "BLOCK_REQUIRES_ADJUDICATION",
      "remote_freshness": "KNOWN",
      "latest_observed_head_may_advance": true,
      "queue_unchanged": true,
      "blocked_head_unchanged": true,
      "blocking_failure_code_unchanged": true,
      "observer_phase": "BLOCKED",
      "projection_state": "BLOCKED",
      "live_projection_head_unchanged": true
    },
    "REMOTE_HEAD_OBSERVED_SAME": {
      "action": "NOOP",
      "queue_unchanged": true,
      "evaluation_not_started": true,
      "remote_freshness": "KNOWN",
      "latest_observed_head_becomes_observed": true,
      "stale_may_return_current_only_if_current_invariants_hold": true,
      "blocked_state_may_not_be_auto_cleared": true
    },
    "REMOTE_HEAD_OBSERVED_INITIAL": {
      "action": "QUEUE_EXACT_HEAD_FOR_EVALUATION",
      "queue_append_if_absent": true,
      "remote_freshness": "KNOWN",
      "latest_observed_head_becomes_observed": true,
      "projection_state_if_live_missing": "MISSING",
      "projection_state_if_live_exists": "STALE"
    },
    "REMOTE_HEAD_OBSERVED_FAST_FORWARD": {
      "action": "QUEUE_EXACT_HEAD_FOR_EVALUATION",
      "queue_append_if_absent": true,
      "remote_freshness": "KNOWN",
      "latest_observed_head_becomes_observed": true,
      "projection_state": "STALE",
      "active_evaluation_must_not_be_retargeted": true
    },
    "REMOTE_HEAD_OBSERVED_NON_FAST_FORWARD": {
      "action": "BLOCK_REQUIRES_ADJUDICATION",
      "queue_append_forbidden": true,
      "observer_phase": "BLOCKED",
      "projection_state": "BLOCKED",
      "blocked_head_becomes_observed": true,
      "live_projection_head_unchanged": true
    },
    "REMOTE_HEAD_OBSERVED_UNKNOWN": {
      "action": "BLOCK_REQUIRES_ADJUDICATION",
      "queue_append_forbidden": true,
      "observer_phase": "BLOCKED",
      "projection_state": "BLOCKED",
      "blocked_head_becomes_observed": true,
      "live_projection_head_unchanged": true
    },
    "REMOTE_OBSERVATION_FAILED": {
      "action": "RETAIN_LAST_KNOWN_GOOD",
      "remote_freshness": "UNKNOWN",
      "latest_observed_head_unchanged": true,
      "live_projection_head_unchanged": true,
      "previous_current_becomes_stale": true,
      "other_projection_states_retained": true,
      "failure_code_recorded": true
    },
    "EVALUATION_STARTED": {
      "requires_observer_phase": "IDLE",
      "candidate_must_equal_pending_queue_head": true,
      "observer_phase": "EVALUATING",
      "action": "START_EXACT_HEAD_EVALUATION",
      "queue_unchanged": true,
      "live_projection_head_unchanged": true
    },
    "EVALUATION_PASSED": {
      "requires_observer_phase": "EVALUATING",
      "candidate_must_equal_pending_queue_head": true,
      "candidate_removed_from_queue_head": true,
      "last_qualified_head_becomes_candidate": true,
      "observer_phase": "CANDIDATE_PENDING",
      "action": "CANDIDATE_QUALIFIED_PENDING_PROMOTION",
      "live_projection_head_unchanged": true
    },
    "EVALUATION_FAILED": {
      "requires_observer_phase": "EVALUATING",
      "candidate_must_equal_pending_queue_head": true,
      "candidate_removed_from_queue_head": true,
      "blocked_head_becomes_candidate": true,
      "failure_code_recorded": true,
      "observer_phase": "BLOCKED",
      "projection_state": "BLOCKED",
      "action": "RETAIN_LAST_KNOWN_GOOD",
      "live_projection_head_unchanged": true
    },
    "PROMOTION_CONFIRMED": {
      "requires_observer_phase": "CANDIDATE_PENDING",
      "candidate_must_equal_last_qualified_head": true,
      "live_projection_head_becomes_candidate": true,
      "projection_state_current_only_if_freshness_and_head_equality_hold": true,
      "otherwise_projection_state": "STALE",
      "observer_phase": "IDLE",
      "action": "CONFIRM_LIVE_PROJECTION",
      "actual_promotion_io_forbidden": true
    },
    "PROMOTION_FAILED": {
      "requires_observer_phase": "CANDIDATE_PENDING",
      "candidate_must_equal_last_qualified_head": true,
      "blocked_head_becomes_candidate": true,
      "failure_code_recorded": true,
      "observer_phase": "BLOCKED",
      "projection_state": "BLOCKED",
      "action": "RETAIN_LAST_KNOWN_GOOD",
      "live_projection_head_unchanged": true,
      "actual_promotion_io_forbidden": true
    },
    "LOCK_CONTENDED": {
      "action": "NOOP",
      "state_unchanged_except_sequence": true,
      "production_write_authorized": false
    },
    "SHUTDOWN_REQUESTED": {
      "observer_phase": "STOPPED",
      "action": "STOP",
      "pending_heads_preserved": true,
      "live_projection_head_unchanged": true
    },
    "STOPPED_TERMINAL": {
      "further_events_forbidden": true
    }
  },
  "decision_invariants": {
    "required_fields": [
      "schema",
      "action",
      "reason_code",
      "observed_head",
      "candidate_head",
      "previous_live_head",
      "next_projection_state",
      "automatic_promotion_authorized",
      "production_write_authorized"
    ],
    "automatic_promotion_authorized_always_false": true,
    "production_write_authorized_always_false": true
  },
  "audit_invariants": {
    "required_fields": [
      "schema",
      "sequence",
      "event_type",
      "previous_state_digest",
      "input_digest",
      "decision_digest",
      "next_state_digest",
      "reason_code"
    ],
    "sequence_equals_input_sequence": true,
    "event_type_equals_input_event_type": true,
    "reason_code_equals_decision_reason_code": true,
    "volatile_fields_forbidden": true
  },
  "failure_model": {
    "invalid_state": "RAISE_OBSERVER_TICK_ERROR_NO_OUTPUT",
    "invalid_input": "RAISE_OBSERVER_TICK_ERROR_NO_OUTPUT",
    "invalid_transition": "RAISE_OBSERVER_TICK_ERROR_NO_OUTPUT",
    "digest_or_serialization_failure": "RAISE_OBSERVER_TICK_ERROR_NO_OUTPUT",
    "partial_result_forbidden": true
  },
  "p5d2_boundary": {
    "pure_one_shot_transition_implementation_authorized": true,
    "network_adapter_authorized": false,
    "git_adapter_authorized": false,
    "filesystem_state_store_authorized": false,
    "append_only_disk_event_log_authorized": false,
    "background_observer_authorized": false,
    "polling_loop_authorized": false,
    "sleep_or_timer_authorized": false,
    "production_promotion_authorized": false,
    "continuous_vault_write_authorized": false,
    "windows_startup_registration_authorized": false,
    "scheduled_task_authorized": false,
    "windows_service_authorized": false,
    "graph_search_current_semantics_authorized": false
  },
  "required_breakers": [
    "invalid repository accepted",
    "invalid branch accepted",
    "invalid observer phase accepted",
    "invalid remote freshness accepted",
    "invalid projection state accepted",
    "uppercase or malformed HEAD accepted",
    "duplicate pending HEAD accepted",
    "negative or boolean event sequence accepted",
    "CURRENT accepted with UNKNOWN freshness",
    "CURRENT accepted with unequal observed live qualified heads",
    "EVALUATING accepted with empty pending queue",
    "CANDIDATE_PENDING accepted without qualified head",
    "BLOCKED phase accepted without blocked projection/head/failure code",
    "input sequence skip accepted",
    "input sequence replay accepted",
    "BOOTSTRAP accepted from noncanonical initial state",
    "extra normalized input field accepted",
    "wrong input schema accepted",
    "REMOTE_HEAD_OBSERVED without head accepted",
    "REMOTE_HEAD_OBSERVED without transition class accepted",
    "SAME accepted when observed head differs from previous observed head",
    "INITIAL accepted after previous observed head exists",
    "FAST_FORWARD accepted without previous observed head",
    "FAST_FORWARD accepted for unchanged observed head",
    "NON_FAST_FORWARD accepted for unchanged observed head",
    "UNKNOWN accepted for unchanged observed head",
    "SAME changes queue",
    "SAME starts evaluation",
    "SAME auto-clears BLOCKED",
    "new remote HEAD clears BLOCKED phase",
    "new remote HEAD grows queue while already BLOCKED",
    "INITIAL fails to queue exact head",
    "FAST_FORWARD fails to queue exact head",
    "new FAST_FORWARD retargets active evaluation",
    "NON_FAST_FORWARD queues head",
    "UNKNOWN queues head",
    "network failure changes live head",
    "network failure leaves fresh CURRENT claim",
    "evaluation starts outside IDLE phase",
    "evaluation starts for non-head-of-queue candidate",
    "evaluation PASS changes live head",
    "evaluation PASS fails to advance last qualified head",
    "evaluation FAIL changes live head",
    "promotion confirmation for non-qualified candidate accepted",
    "promotion failure changes live head",
    "LOCK_CONTENDED mutates semantic state",
    "SHUTDOWN drops pending heads",
    "event accepted after STOPPED",
    "automatic promotion authority becomes true",
    "production write authority becomes true",
    "same inputs produce different normalized bytes",
    "same inputs produce different digests",
    "volatile host data appears in audit record",
    "network API imported or called",
    "subprocess imported or called",
    "filesystem API used for state transition",
    "sleep or timer used",
    "environment variable read",
    "randomness used",
    "loop construct used for repeated observer ticks",
    "background thread or async task created",
    "Git command launched",
    "Vault path referenced for writes",
    "Windows startup registration referenced",
    "scheduled task referenced",
    "Windows service referenced",
    "Graph/Search CURRENT semantics claimed"
  ],
  "next_gates": {
    "p5d3": "CONTROLLED_CANDIDATE_EVALUATION_PIPELINE",
    "p5d4": "BOUNDED_OBSERVER_LOOP_CANDIDATE",
    "p5e": "END_TO_END_NEAR_REAL_TIME_QUALIFICATION",
    "p6": "CONTROLLED_KNOWLEDGE_GRAPH_ARCHITECTURE"
  }
}

~~~~

# SOURCE: P5-D2 OBSERVER TICK RUNTIME

Path: tools/obsidian_projection/observer_tick.py
~~~~
from __future__ import annotations

import hashlib
import json
import re
from typing import Any


class ObserverTickError(RuntimeError):
    pass


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
EXPECTED_BRANCH = "integration/system-v1"
CONTRACT_BLOB = "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3"

STATE_SCHEMA = "ATDS_OBSIDIAN_OBSERVER_STATE_V0_1"
INPUT_SCHEMA = "ATDS_OBSIDIAN_OBSERVER_INPUT_V0_1"
DECISION_SCHEMA = "ATDS_OBSIDIAN_OBSERVER_DECISION_V0_1"
EVENT_SCHEMA = "ATDS_OBSIDIAN_OBSERVER_EVENT_V0_1"
RESULT_SCHEMA = "ATDS_OBSIDIAN_ONE_SHOT_TICK_RESULT_V0_1"

OBSERVER_PHASES = frozenset(
    {
        "IDLE",
        "CANDIDATE_PENDING",
        "EVALUATING",
        "BLOCKED",
        "STOPPED",
    }
)
REMOTE_FRESHNESS = frozenset({"KNOWN", "UNKNOWN"})
PROJECTION_STATES = frozenset(
    {
        "CURRENT",
        "STALE",
        "BLOCKED",
        "ORPHAN",
        "MISSING",
    }
)
EVENT_TYPES = frozenset(
    {
        "BOOTSTRAP",
        "REMOTE_HEAD_OBSERVED",
        "REMOTE_OBSERVATION_FAILED",
        "EVALUATION_STARTED",
        "EVALUATION_PASSED",
        "EVALUATION_FAILED",
        "PROMOTION_CONFIRMED",
        "PROMOTION_FAILED",
        "LOCK_CONTENDED",
        "SHUTDOWN_REQUESTED",
    }
)
TRANSITION_CLASSES = frozenset(
    {
        "INITIAL",
        "SAME",
        "FAST_FORWARD",
        "NON_FAST_FORWARD",
        "UNKNOWN",
    }
)

_STATE_KEYS = frozenset(
    {
        "schema",
        "repository",
        "branch",
        "observer_phase",
        "remote_freshness",
        "latest_observed_head",
        "last_qualified_head",
        "live_projection_head",
        "projection_state",
        "pending_heads",
        "blocked_head",
        "last_failure_code",
        "last_event_sequence",
    }
)
_INPUT_KEYS = frozenset(
    {
        "schema",
        "event_type",
        "sequence",
        "observed_head",
        "transition_class",
        "candidate_head",
        "failure_code",
    }
)

_HEAD_RE = re.compile(r"^[0-9a-f]{40}$")


def _canonical_json_bytes(value: Any) -> bytes:
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ObserverTickError(
            "value is not canonical JSON"
        ) from exc
    return (encoded + "\n").encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(
        _canonical_json_bytes(value)
    ).hexdigest()


def _clone(value: Any) -> Any:
    try:
        return json.loads(
            _canonical_json_bytes(value).decode("utf-8")
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ObserverTickError(
            "canonical clone failed"
        ) from exc


def _is_head(value: Any) -> bool:
    return (
        isinstance(value, str)
        and _HEAD_RE.fullmatch(value) is not None
    )


def _require_optional_head(
    value: Any,
    field: str,
) -> None:
    if value is not None and not _is_head(value):
        raise ObserverTickError(
            f"{field} must be lowercase 40-hex SHA-1 or null"
        )


def _require_failure_code(
    value: Any,
    *,
    required: bool,
) -> None:
    if required:
        if (
            not isinstance(value, str)
            or not value
            or value.strip() != value
        ):
            raise ObserverTickError(
                "failure_code required"
            )
        return
    if value is not None:
        raise ObserverTickError(
            "failure_code must be null"
        )


def _validate_state(state: dict[str, Any]) -> None:
    if not isinstance(state, dict):
        raise ObserverTickError("state must be an object")
    if frozenset(state) != _STATE_KEYS:
        raise ObserverTickError("state fields mismatch")
    if state["schema"] != STATE_SCHEMA:
        raise ObserverTickError("state schema mismatch")
    if state["repository"] != EXPECTED_REPOSITORY:
        raise ObserverTickError("repository mismatch")
    if state["branch"] != EXPECTED_BRANCH:
        raise ObserverTickError("branch mismatch")
    if state["observer_phase"] not in OBSERVER_PHASES:
        raise ObserverTickError("invalid observer phase")
    if state["remote_freshness"] not in REMOTE_FRESHNESS:
        raise ObserverTickError("invalid remote freshness")
    if state["projection_state"] not in PROJECTION_STATES:
        raise ObserverTickError("invalid projection state")

    _require_optional_head(
        state["latest_observed_head"],
        "latest_observed_head",
    )
    _require_optional_head(
        state["last_qualified_head"],
        "last_qualified_head",
    )
    _require_optional_head(
        state["live_projection_head"],
        "live_projection_head",
    )
    _require_optional_head(
        state["blocked_head"],
        "blocked_head",
    )

    pending = state["pending_heads"]
    if not isinstance(pending, list):
        raise ObserverTickError(
            "pending_heads must be an array"
        )
    if not all(_is_head(item) for item in pending):
        raise ObserverTickError(
            "pending_heads contains invalid HEAD"
        )
    if len(pending) != len(set(pending)):
        raise ObserverTickError(
            "pending_heads contains duplicate HEAD"
        )

    failure = state["last_failure_code"]
    if failure is not None and (
        not isinstance(failure, str)
        or not failure
        or failure.strip() != failure
    ):
        raise ObserverTickError(
            "invalid last_failure_code"
        )

    sequence = state["last_event_sequence"]
    if (
        isinstance(sequence, bool)
        or not isinstance(sequence, int)
        or sequence < 0
    ):
        raise ObserverTickError(
            "invalid last_event_sequence"
        )

    if state["projection_state"] == "CURRENT":
        if state["remote_freshness"] != "KNOWN":
            raise ObserverTickError(
                "CURRENT requires KNOWN remote freshness"
            )
        live = state["live_projection_head"]
        if live is None:
            raise ObserverTickError(
                "CURRENT requires live projection HEAD"
            )
        if state["latest_observed_head"] != live:
            raise ObserverTickError(
                "CURRENT requires observed == live"
            )
        if state["last_qualified_head"] != live:
            raise ObserverTickError(
                "CURRENT requires live == qualified"
            )

    if (
        state["observer_phase"] == "EVALUATING"
        and not pending
    ):
        raise ObserverTickError(
            "EVALUATING requires pending queue head"
        )

    if (
        state["observer_phase"] == "CANDIDATE_PENDING"
        and state["last_qualified_head"] is None
    ):
        raise ObserverTickError(
            "CANDIDATE_PENDING requires qualified HEAD"
        )

    if state["observer_phase"] == "BLOCKED":
        if state["projection_state"] != "BLOCKED":
            raise ObserverTickError(
                "BLOCKED phase requires BLOCKED projection"
            )
        if state["blocked_head"] is None:
            raise ObserverTickError(
                "BLOCKED phase requires blocked HEAD"
            )
        if state["last_failure_code"] is None:
            raise ObserverTickError(
                "BLOCKED phase requires failure code"
            )


def _validate_input(
    previous_state: dict[str, Any],
    event: dict[str, Any],
) -> None:
    if not isinstance(event, dict):
        raise ObserverTickError("input must be an object")
    if frozenset(event) != _INPUT_KEYS:
        raise ObserverTickError("input fields mismatch")
    if event["schema"] != INPUT_SCHEMA:
        raise ObserverTickError("input schema mismatch")
    if event["event_type"] not in EVENT_TYPES:
        raise ObserverTickError("invalid event type")

    sequence = event["sequence"]
    if (
        isinstance(sequence, bool)
        or not isinstance(sequence, int)
        or sequence
        != previous_state["last_event_sequence"] + 1
    ):
        raise ObserverTickError(
            "input sequence must advance exactly once"
        )

    _require_optional_head(
        event["observed_head"],
        "observed_head",
    )
    _require_optional_head(
        event["candidate_head"],
        "candidate_head",
    )

    transition_class = event["transition_class"]
    if (
        transition_class is not None
        and transition_class not in TRANSITION_CLASSES
    ):
        raise ObserverTickError(
            "invalid transition class"
        )

    event_type = event["event_type"]

    if event_type == "REMOTE_HEAD_OBSERVED":
        if event["observed_head"] is None:
            raise ObserverTickError(
                "REMOTE_HEAD_OBSERVED requires observed_head"
            )
        if transition_class is None:
            raise ObserverTickError(
                "REMOTE_HEAD_OBSERVED requires transition_class"
            )
        if event["candidate_head"] is not None:
            raise ObserverTickError(
                "remote observation forbids candidate_head"
            )
        _require_failure_code(
            event["failure_code"],
            required=False,
        )
        return

    if event_type == "REMOTE_OBSERVATION_FAILED":
        if (
            event["observed_head"] is not None
            or transition_class is not None
            or event["candidate_head"] is not None
        ):
            raise ObserverTickError(
                "remote failure carries no HEAD"
            )
        _require_failure_code(
            event["failure_code"],
            required=True,
        )
        return

    if event_type in {
        "EVALUATION_STARTED",
        "EVALUATION_PASSED",
        "PROMOTION_CONFIRMED",
    }:
        if (
            event["observed_head"] is not None
            or transition_class is not None
            or event["candidate_head"] is None
        ):
            raise ObserverTickError(
                f"{event_type} normalized fields invalid"
            )
        _require_failure_code(
            event["failure_code"],
            required=False,
        )
        return

    if event_type in {
        "EVALUATION_FAILED",
        "PROMOTION_FAILED",
    }:
        if (
            event["observed_head"] is not None
            or transition_class is not None
            or event["candidate_head"] is None
        ):
            raise ObserverTickError(
                f"{event_type} normalized fields invalid"
            )
        _require_failure_code(
            event["failure_code"],
            required=True,
        )
        return

    if event_type == "LOCK_CONTENDED":
        if (
            event["observed_head"] is not None
            or transition_class is not None
            or event["candidate_head"] is not None
            or event["failure_code"] != "LOCK_CONTENDED"
        ):
            raise ObserverTickError(
                "LOCK_CONTENDED normalized fields invalid"
            )
        return

    if (
        event["observed_head"] is not None
        or transition_class is not None
        or event["candidate_head"] is not None
    ):
        raise ObserverTickError(
            f"{event_type} carries unexpected HEAD"
        )
    _require_failure_code(
        event["failure_code"],
        required=False,
    )


def make_initial_state() -> dict[str, Any]:
    state = {
        "schema": STATE_SCHEMA,
        "repository": EXPECTED_REPOSITORY,
        "branch": EXPECTED_BRANCH,
        "observer_phase": "IDLE",
        "remote_freshness": "UNKNOWN",
        "latest_observed_head": None,
        "last_qualified_head": None,
        "live_projection_head": None,
        "projection_state": "MISSING",
        "pending_heads": [],
        "blocked_head": None,
        "last_failure_code": None,
        "last_event_sequence": 0,
    }
    _validate_state(state)
    return state


def _decision(
    *,
    action: str,
    reason_code: str,
    observed_head: str | None,
    candidate_head: str | None,
    previous_live_head: str | None,
    next_projection_state: str,
) -> dict[str, Any]:
    return {
        "schema": DECISION_SCHEMA,
        "action": action,
        "reason_code": reason_code,
        "observed_head": observed_head,
        "candidate_head": candidate_head,
        "previous_live_head": previous_live_head,
        "next_projection_state": next_projection_state,
        "automatic_promotion_authorized": False,
        "production_write_authorized": False,
    }


def _apply_remote_observed(
    state: dict[str, Any],
    event: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    observed = event["observed_head"]
    transition_class = event["transition_class"]
    previous_live = state["live_projection_head"]
    previous_observed = state["latest_observed_head"]

    if transition_class == "INITIAL":
        if previous_observed is not None:
            raise ObserverTickError(
                "INITIAL requires no previous observed HEAD"
            )
    elif transition_class == "SAME":
        if previous_observed != observed:
            raise ObserverTickError(
                "SAME requires previous observed HEAD equality"
            )
    else:
        if previous_observed is None:
            raise ObserverTickError(
                f"{transition_class} requires previous observed HEAD"
            )
        if previous_observed == observed:
            raise ObserverTickError(
                f"{transition_class} requires a new observed HEAD"
            )

    if state["observer_phase"] == "BLOCKED":
        if (
            transition_class == "SAME"
            and state["latest_observed_head"] != observed
        ):
            raise ObserverTickError(
                "SAME requires previous observed HEAD equality"
            )
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        decision = _decision(
            action="BLOCK_REQUIRES_ADJUDICATION",
            reason_code="OBSERVER_ALREADY_BLOCKED",
            observed_head=observed,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state="BLOCKED",
        )
        return next_state, decision

    if transition_class == "SAME":
        if state["latest_observed_head"] != observed:
            raise ObserverTickError(
                "SAME requires previous observed HEAD equality"
            )
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        next_state["last_failure_code"] = None
        if (
            next_state["observer_phase"] != "BLOCKED"
            and next_state["live_projection_head"] is not None
            and next_state["live_projection_head"] == observed
            and next_state["last_qualified_head"] == observed
        ):
            next_state["projection_state"] = "CURRENT"
        decision = _decision(
            action="NOOP",
            reason_code="REMOTE_HEAD_SAME",
            observed_head=observed,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=next_state[
                "projection_state"
            ],
        )
        return next_state, decision

    if transition_class == "INITIAL":
        if state["latest_observed_head"] is not None:
            raise ObserverTickError(
                "INITIAL requires no previous observed HEAD"
            )
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        next_state["last_failure_code"] = None
        if observed not in next_state["pending_heads"]:
            next_state["pending_heads"].append(observed)
        next_state["projection_state"] = (
            "MISSING"
            if next_state["live_projection_head"] is None
            else "STALE"
        )
        decision = _decision(
            action="QUEUE_EXACT_HEAD_FOR_EVALUATION",
            reason_code="REMOTE_HEAD_INITIAL_QUEUED",
            observed_head=observed,
            candidate_head=observed,
            previous_live_head=previous_live,
            next_projection_state=next_state[
                "projection_state"
            ],
        )
        return next_state, decision

    if state["latest_observed_head"] is None:
        raise ObserverTickError(
            f"{transition_class} requires previous observed HEAD"
        )
    if state["latest_observed_head"] == observed:
        raise ObserverTickError(
            f"{transition_class} requires a new observed HEAD"
        )

    if transition_class == "FAST_FORWARD":
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        next_state["last_failure_code"] = None
        if observed not in next_state["pending_heads"]:
            next_state["pending_heads"].append(observed)
        next_state["projection_state"] = "STALE"
        decision = _decision(
            action="QUEUE_EXACT_HEAD_FOR_EVALUATION",
            reason_code="REMOTE_HEAD_FAST_FORWARD_QUEUED",
            observed_head=observed,
            candidate_head=observed,
            previous_live_head=previous_live,
            next_projection_state="STALE",
        )
        return next_state, decision

    if transition_class in {
        "NON_FAST_FORWARD",
        "UNKNOWN",
    }:
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        next_state["observer_phase"] = "BLOCKED"
        next_state["projection_state"] = "BLOCKED"
        next_state["blocked_head"] = observed
        next_state["last_failure_code"] = (
            "NON_FAST_FORWARD_REQUIRES_ADJUDICATION"
            if transition_class == "NON_FAST_FORWARD"
            else "UNKNOWN_ANCESTRY_REQUIRES_ADJUDICATION"
        )
        decision = _decision(
            action="BLOCK_REQUIRES_ADJUDICATION",
            reason_code=next_state["last_failure_code"],
            observed_head=observed,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state="BLOCKED",
        )
        return next_state, decision

    raise ObserverTickError(
        "unsupported remote transition class"
    )


def _apply_transition(
    state: dict[str, Any],
    event: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    event_type = event["event_type"]
    previous_live = state["live_projection_head"]

    if state["observer_phase"] == "STOPPED":
        raise ObserverTickError(
            "STOPPED observer accepts no further events"
        )

    if event_type == "BOOTSTRAP":
        if state["last_event_sequence"] != 0:
            raise ObserverTickError(
                "BOOTSTRAP allowed only at sequence zero"
            )
        if state != make_initial_state():
            raise ObserverTickError(
                "BOOTSTRAP requires canonical initial state"
            )
        next_state = _clone(state)
        decision = _decision(
            action="NOOP",
            reason_code="BOOTSTRAP_ACCEPTED",
            observed_head=None,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=state[
                "projection_state"
            ],
        )
        return next_state, decision

    if event_type == "REMOTE_HEAD_OBSERVED":
        return _apply_remote_observed(state, event)

    if event_type == "REMOTE_OBSERVATION_FAILED":
        next_state = _clone(state)
        next_state["remote_freshness"] = "UNKNOWN"
        next_state["last_failure_code"] = event[
            "failure_code"
        ]
        if next_state["projection_state"] == "CURRENT":
            next_state["projection_state"] = "STALE"
        decision = _decision(
            action="RETAIN_LAST_KNOWN_GOOD",
            reason_code="REMOTE_OBSERVATION_FAILED",
            observed_head=None,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=next_state[
                "projection_state"
            ],
        )
        return next_state, decision

    if event_type == "EVALUATION_STARTED":
        candidate = event["candidate_head"]
        if state["observer_phase"] != "IDLE":
            raise ObserverTickError(
                "evaluation may start only from IDLE"
            )
        if (
            not state["pending_heads"]
            or state["pending_heads"][0] != candidate
        ):
            raise ObserverTickError(
                "evaluation candidate must equal queue head"
            )
        next_state = _clone(state)
        next_state["observer_phase"] = "EVALUATING"
        decision = _decision(
            action="START_EXACT_HEAD_EVALUATION",
            reason_code="EVALUATION_STARTED",
            observed_head=None,
            candidate_head=candidate,
            previous_live_head=previous_live,
            next_projection_state=next_state[
                "projection_state"
            ],
        )
        return next_state, decision

    if event_type in {
        "EVALUATION_PASSED",
        "EVALUATION_FAILED",
    }:
        candidate = event["candidate_head"]
        if state["observer_phase"] != "EVALUATING":
            raise ObserverTickError(
                f"{event_type} requires EVALUATING phase"
            )
        if (
            not state["pending_heads"]
            or state["pending_heads"][0] != candidate
        ):
            raise ObserverTickError(
                "evaluation result candidate must equal queue head"
            )
        next_state = _clone(state)
        next_state["pending_heads"] = (
            next_state["pending_heads"][1:]
        )

        if event_type == "EVALUATION_PASSED":
            next_state["last_qualified_head"] = candidate
            next_state["observer_phase"] = (
                "CANDIDATE_PENDING"
            )
            next_state["blocked_head"] = None
            next_state["last_failure_code"] = None
            decision = _decision(
                action=(
                    "CANDIDATE_QUALIFIED_PENDING_PROMOTION"
                ),
                reason_code="EVALUATION_PASSED",
                observed_head=None,
                candidate_head=candidate,
                previous_live_head=previous_live,
                next_projection_state=next_state[
                    "projection_state"
                ],
            )
            return next_state, decision

        next_state["observer_phase"] = "BLOCKED"
        next_state["projection_state"] = "BLOCKED"
        next_state["blocked_head"] = candidate
        next_state["last_failure_code"] = event[
            "failure_code"
        ]
        decision = _decision(
            action="RETAIN_LAST_KNOWN_GOOD",
            reason_code="EVALUATION_FAILED",
            observed_head=None,
            candidate_head=candidate,
            previous_live_head=previous_live,
            next_projection_state="BLOCKED",
        )
        return next_state, decision

    if event_type in {
        "PROMOTION_CONFIRMED",
        "PROMOTION_FAILED",
    }:
        candidate = event["candidate_head"]
        if state["observer_phase"] != "CANDIDATE_PENDING":
            raise ObserverTickError(
                f"{event_type} requires CANDIDATE_PENDING"
            )
        if state["last_qualified_head"] != candidate:
            raise ObserverTickError(
                "promotion candidate must equal last qualified HEAD"
            )
        next_state = _clone(state)

        if event_type == "PROMOTION_CONFIRMED":
            next_state["live_projection_head"] = candidate
            next_state["observer_phase"] = "IDLE"
            next_state["blocked_head"] = None
            next_state["last_failure_code"] = None
            if (
                next_state["remote_freshness"] == "KNOWN"
                and next_state["latest_observed_head"]
                == candidate
            ):
                next_state["projection_state"] = "CURRENT"
            else:
                next_state["projection_state"] = "STALE"
            decision = _decision(
                action="CONFIRM_LIVE_PROJECTION",
                reason_code="PROMOTION_CONFIRMED",
                observed_head=None,
                candidate_head=candidate,
                previous_live_head=previous_live,
                next_projection_state=next_state[
                    "projection_state"
                ],
            )
            return next_state, decision

        next_state["observer_phase"] = "BLOCKED"
        next_state["projection_state"] = "BLOCKED"
        next_state["blocked_head"] = candidate
        next_state["last_failure_code"] = event[
            "failure_code"
        ]
        decision = _decision(
            action="RETAIN_LAST_KNOWN_GOOD",
            reason_code="PROMOTION_FAILED",
            observed_head=None,
            candidate_head=candidate,
            previous_live_head=previous_live,
            next_projection_state="BLOCKED",
        )
        return next_state, decision

    if event_type == "LOCK_CONTENDED":
        next_state = _clone(state)
        decision = _decision(
            action="NOOP",
            reason_code="LOCK_CONTENDED",
            observed_head=None,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=state[
                "projection_state"
            ],
        )
        return next_state, decision

    if event_type == "SHUTDOWN_REQUESTED":
        next_state = _clone(state)
        next_state["observer_phase"] = "STOPPED"
        decision = _decision(
            action="STOP",
            reason_code="SHUTDOWN_REQUESTED",
            observed_head=None,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=state[
                "projection_state"
            ],
        )
        return next_state, decision

    raise ObserverTickError("unsupported event type")


def one_shot_tick(
    previous_state: dict[str, Any],
    normalized_input: dict[str, Any],
) -> dict[str, Any]:
    previous = _clone(previous_state)
    event = _clone(normalized_input)

    _validate_state(previous)
    _validate_input(previous, event)

    next_state, decision = _apply_transition(
        previous,
        event,
    )
    next_state["last_event_sequence"] = event["sequence"]

    _validate_state(next_state)

    audit = {
        "schema": EVENT_SCHEMA,
        "sequence": event["sequence"],
        "event_type": event["event_type"],
        "previous_state_digest": _digest(previous),
        "input_digest": _digest(event),
        "decision_digest": _digest(decision),
        "next_state_digest": _digest(next_state),
        "reason_code": decision["reason_code"],
    }

    result = {
        "schema": RESULT_SCHEMA,
        "next_state": next_state,
        "decision": decision,
        "audit": audit,
    }

    _canonical_json_bytes(result)
    return result


def canonical_result_bytes(
    result: dict[str, Any],
) -> bytes:
    return _canonical_json_bytes(result)

~~~~

# SOURCE: P5-D2 OBSERVER TICK TESTS

Path: tests/obsidian_projection/test_observer_tick.py
~~~~
from __future__ import annotations

import copy
import hashlib
import json
import unittest

from tools.obsidian_projection.observer_tick import (
    DECISION_SCHEMA,
    EVENT_SCHEMA,
    INPUT_SCHEMA,
    RESULT_SCHEMA,
    STATE_SCHEMA,
    ObserverTickError,
    canonical_result_bytes,
    make_initial_state,
    one_shot_tick,
)


H1 = "1" * 40
H2 = "2" * 40
H3 = "3" * 40
H4 = "4" * 40


def event(
    sequence: int,
    event_type: str,
    *,
    observed_head: str | None = None,
    transition_class: str | None = None,
    candidate_head: str | None = None,
    failure_code: str | None = None,
) -> dict:
    return {
        "schema": INPUT_SCHEMA,
        "event_type": event_type,
        "sequence": sequence,
        "observed_head": observed_head,
        "transition_class": transition_class,
        "candidate_head": candidate_head,
        "failure_code": failure_code,
    }


def tick(
    state: dict,
    event_type: str,
    **kwargs,
) -> dict:
    payload = event(
        state["last_event_sequence"] + 1,
        event_type,
        **kwargs,
    )
    return one_shot_tick(state, payload)


def bootstrap() -> dict:
    state = make_initial_state()
    return tick(
        state,
        "BOOTSTRAP",
    )["next_state"]


def observe_initial(
    state: dict,
    head: str = H1,
) -> dict:
    return tick(
        state,
        "REMOTE_HEAD_OBSERVED",
        observed_head=head,
        transition_class="INITIAL",
    )["next_state"]


def begin_evaluation(
    state: dict,
    head: str = H1,
) -> dict:
    return tick(
        state,
        "EVALUATION_STARTED",
        candidate_head=head,
    )["next_state"]


def qualify(
    state: dict,
    head: str = H1,
) -> dict:
    return tick(
        state,
        "EVALUATION_PASSED",
        candidate_head=head,
    )["next_state"]


def promote(
    state: dict,
    head: str = H1,
) -> dict:
    return tick(
        state,
        "PROMOTION_CONFIRMED",
        candidate_head=head,
    )["next_state"]


def make_current_state() -> dict:
    state = bootstrap()
    state = observe_initial(state, H1)
    state = begin_evaluation(state, H1)
    state = qualify(state, H1)
    state = promote(state, H1)
    return state


class ObserverTickTests(unittest.TestCase):
    def test_initial_state_is_canonical(self) -> None:
        state = make_initial_state()
        self.assertEqual(state["schema"], STATE_SCHEMA)
        self.assertEqual(state["observer_phase"], "IDLE")
        self.assertEqual(
            state["remote_freshness"],
            "UNKNOWN",
        )
        self.assertEqual(
            state["projection_state"],
            "MISSING",
        )
        self.assertEqual(state["pending_heads"], [])
        self.assertEqual(state["last_event_sequence"], 0)

    def test_bootstrap_changes_only_sequence(self) -> None:
        state = make_initial_state()
        result = tick(state, "BOOTSTRAP")
        next_state = result["next_state"]
        expected = copy.deepcopy(state)
        expected["last_event_sequence"] = 1
        self.assertEqual(next_state, expected)
        self.assertEqual(
            result["decision"]["action"],
            "NOOP",
        )
        self.assertEqual(
            result["decision"]["reason_code"],
            "BOOTSTRAP_ACCEPTED",
        )

    def test_bootstrap_rejects_noncanonical_state(
        self,
    ) -> None:
        state = make_initial_state()
        state["remote_freshness"] = "KNOWN"
        with self.assertRaises(ObserverTickError):
            tick(state, "BOOTSTRAP")

    def test_initial_head_is_queued_exactly_once(
        self,
    ) -> None:
        state = bootstrap()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["latest_observed_head"],
            H1,
        )
        self.assertEqual(
            next_state["pending_heads"],
            [H1],
        )
        self.assertEqual(
            next_state["remote_freshness"],
            "KNOWN",
        )
        self.assertEqual(
            next_state["projection_state"],
            "MISSING",
        )
        self.assertEqual(
            result["decision"]["action"],
            "QUEUE_EXACT_HEAD_FOR_EVALUATION",
        )

    def test_initial_rejected_after_previous_observation(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H2,
                transition_class="INITIAL",
            )

    def test_same_head_is_strict_noop_for_queue(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        before_pending = copy.deepcopy(
            state["pending_heads"]
        )
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="SAME",
        )
        self.assertEqual(
            result["next_state"]["pending_heads"],
            before_pending,
        )
        self.assertEqual(
            result["decision"]["action"],
            "NOOP",
        )

    def test_same_requires_previous_observed_equality(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H2,
                transition_class="SAME",
            )

    def test_network_failure_from_current_becomes_stale(
        self,
    ) -> None:
        state = make_current_state()
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "REMOTE_OBSERVATION_FAILED",
            failure_code="NETWORK_UNAVAILABLE",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["remote_freshness"],
            "UNKNOWN",
        )
        self.assertEqual(
            next_state["projection_state"],
            "STALE",
        )
        self.assertEqual(
            next_state["live_projection_head"],
            live_before,
        )
        self.assertEqual(
            next_state["last_failure_code"],
            "NETWORK_UNAVAILABLE",
        )

    def test_same_head_restores_current_after_network_failure(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_OBSERVATION_FAILED",
            failure_code="NETWORK_UNAVAILABLE",
        )["next_state"]
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="SAME",
        )
        self.assertEqual(
            result["next_state"]["remote_freshness"],
            "KNOWN",
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "CURRENT",
        )

    def test_same_does_not_clear_blocked_state(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="NON_FAST_FORWARD",
        )["next_state"]
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="SAME",
        )
        self.assertEqual(
            result["next_state"]["observer_phase"],
            "BLOCKED",
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "BLOCKED",
        )

    def test_new_remote_head_does_not_clear_blocked_state(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="NON_FAST_FORWARD",
        )["next_state"]
        pending_before = copy.deepcopy(
            state["pending_heads"]
        )
        blocked_before = state["blocked_head"]
        failure_before = state["last_failure_code"]
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H3,
            transition_class="FAST_FORWARD",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["observer_phase"],
            "BLOCKED",
        )
        self.assertEqual(
            next_state["projection_state"],
            "BLOCKED",
        )
        self.assertEqual(
            next_state["pending_heads"],
            pending_before,
        )
        self.assertEqual(
            next_state["blocked_head"],
            blocked_before,
        )
        self.assertEqual(
            next_state["last_failure_code"],
            failure_before,
        )
        self.assertEqual(
            next_state["latest_observed_head"],
            H3,
        )
        self.assertEqual(
            result["decision"]["action"],
            "BLOCK_REQUIRES_ADJUDICATION",
        )

    def test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        self.assertEqual(state["observer_phase"], "IDLE")
        self.assertEqual(state["pending_heads"], [H1])
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )
        next_state = result["next_state"]
        self.assertEqual(next_state["observer_phase"], "IDLE")
        self.assertEqual(next_state["pending_heads"], [H1, H2])
        self.assertEqual(
            result["decision"]["action"],
            "QUEUE_EXACT_HEAD_FOR_EVALUATION",
        )
        self.assertEqual(result["decision"]["candidate_head"], H2)

    def test_fast_forward_queues_without_retargeting_active(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["observer_phase"],
            "EVALUATING",
        )
        self.assertEqual(
            next_state["pending_heads"],
            [H1, H2],
        )
        self.assertEqual(
            next_state["projection_state"],
            "STALE",
        )

    def test_fast_forward_rejects_unchanged_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="FAST_FORWARD",
            )

    def test_non_fast_forward_rejects_unchanged_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="NON_FAST_FORWARD",
            )

    def test_unknown_rejects_unchanged_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="UNKNOWN",
            )

    def test_fast_forward_requires_previous_observed_head(
        self,
    ) -> None:
        state = bootstrap()
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H2,
                transition_class="FAST_FORWARD",
            )

    def test_non_fast_forward_blocks_without_queueing(
        self,
    ) -> None:
        state = make_current_state()
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="NON_FAST_FORWARD",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["observer_phase"],
            "BLOCKED",
        )
        self.assertEqual(
            next_state["projection_state"],
            "BLOCKED",
        )
        self.assertEqual(
            next_state["blocked_head"],
            H2,
        )
        self.assertEqual(
            next_state["live_projection_head"],
            live_before,
        )
        self.assertNotIn(H2, next_state["pending_heads"])

    def test_unknown_ancestry_blocks_without_queueing(
        self,
    ) -> None:
        state = make_current_state()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="UNKNOWN",
        )
        self.assertEqual(
            result["decision"]["action"],
            "BLOCK_REQUIRES_ADJUDICATION",
        )
        self.assertNotIn(
            H2,
            result["next_state"]["pending_heads"],
        )

    def test_evaluation_start_binds_queue_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        result = tick(
            state,
            "EVALUATION_STARTED",
            candidate_head=H1,
        )
        self.assertEqual(
            result["next_state"]["observer_phase"],
            "EVALUATING",
        )
        self.assertEqual(
            result["next_state"]["pending_heads"],
            [H1],
        )
        self.assertEqual(
            result["decision"]["candidate_head"],
            H1,
        )

    def test_evaluation_start_rejects_non_queue_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "EVALUATION_STARTED",
                candidate_head=H2,
            )

    def test_evaluation_start_requires_idle(self) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "EVALUATION_STARTED",
                candidate_head=H1,
            )

    def test_evaluation_pass_advances_qualified_not_live(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "EVALUATION_PASSED",
            candidate_head=H1,
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["last_qualified_head"],
            H1,
        )
        self.assertEqual(
            next_state["live_projection_head"],
            live_before,
        )
        self.assertEqual(
            next_state["pending_heads"],
            [],
        )
        self.assertEqual(
            next_state["observer_phase"],
            "CANDIDATE_PENDING",
        )

    def test_evaluation_pass_preserves_newer_queued_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )["next_state"]
        result = tick(
            state,
            "EVALUATION_PASSED",
            candidate_head=H1,
        )
        self.assertEqual(
            result["next_state"]["pending_heads"],
            [H2],
        )
        self.assertEqual(
            result["next_state"]["last_qualified_head"],
            H1,
        )

    def test_evaluation_failure_preserves_live_head(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )["next_state"]
        state = begin_evaluation(state, H2)
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "EVALUATION_FAILED",
            candidate_head=H2,
            failure_code="CANDIDATE_INVALID",
        )
        self.assertEqual(
            result["next_state"]["live_projection_head"],
            live_before,
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "BLOCKED",
        )
        self.assertEqual(
            result["next_state"]["blocked_head"],
            H2,
        )

    def test_promotion_confirmation_is_logical_only(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        state = qualify(state, H1)
        result = tick(
            state,
            "PROMOTION_CONFIRMED",
            candidate_head=H1,
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["live_projection_head"],
            H1,
        )
        self.assertEqual(
            next_state["projection_state"],
            "CURRENT",
        )
        self.assertEqual(
            result["decision"][
                "production_write_authorized"
            ],
            False,
        )
        self.assertEqual(
            result["decision"][
                "automatic_promotion_authorized"
            ],
            False,
        )

    def test_promotion_confirmation_stays_stale_if_newer_remote(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )["next_state"]
        state = qualify(state, H1)
        result = tick(
            state,
            "PROMOTION_CONFIRMED",
            candidate_head=H1,
        )
        self.assertEqual(
            result["next_state"]["live_projection_head"],
            H1,
        )
        self.assertEqual(
            result["next_state"]["latest_observed_head"],
            H2,
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "STALE",
        )
        self.assertEqual(
            result["next_state"]["pending_heads"],
            [H2],
        )

    def test_promotion_rejects_nonqualified_candidate(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        state = qualify(state, H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "PROMOTION_CONFIRMED",
                candidate_head=H2,
            )

    def test_promotion_failure_preserves_live_head(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )["next_state"]
        state = begin_evaluation(state, H2)
        state = qualify(state, H2)
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "PROMOTION_FAILED",
            candidate_head=H2,
            failure_code="POINTER_NOT_CONFIRMED",
        )
        self.assertEqual(
            result["next_state"]["live_projection_head"],
            live_before,
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "BLOCKED",
        )

    def test_lock_contended_changes_only_sequence(
        self,
    ) -> None:
        state = make_current_state()
        expected = copy.deepcopy(state)
        expected["last_event_sequence"] += 1
        result = tick(
            state,
            "LOCK_CONTENDED",
            failure_code="LOCK_CONTENDED",
        )
        self.assertEqual(result["next_state"], expected)
        self.assertEqual(
            result["decision"]["action"],
            "NOOP",
        )

    def test_shutdown_preserves_pending_and_live(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        pending_before = copy.deepcopy(
            state["pending_heads"]
        )
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "SHUTDOWN_REQUESTED",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["observer_phase"],
            "STOPPED",
        )
        self.assertEqual(
            next_state["pending_heads"],
            pending_before,
        )
        self.assertEqual(
            next_state["live_projection_head"],
            live_before,
        )

    def test_stopped_state_accepts_no_further_event(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = tick(
            state,
            "SHUTDOWN_REQUESTED",
        )["next_state"]
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="SAME",
            )

    def test_input_sequence_skip_is_rejected(self) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 2,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_input_sequence_replay_is_rejected(
        self,
    ) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"],
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_boolean_sequence_is_rejected(self) -> None:
        state = make_initial_state()
        payload = event(
            True,
            "BOOTSTRAP",
        )
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_extra_input_field_is_rejected(self) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        payload["unexpected"] = "x"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_wrong_input_schema_is_rejected(self) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        payload["schema"] = "WRONG"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_remote_observed_requires_head(self) -> None:
        state = bootstrap()
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                transition_class="INITIAL",
            )

    def test_remote_observed_requires_transition_class(
        self,
    ) -> None:
        state = bootstrap()
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
            )

    def test_invalid_repository_is_rejected(self) -> None:
        state = make_initial_state()
        state["repository"] = "wrong/repo"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_invalid_branch_is_rejected(self) -> None:
        state = make_initial_state()
        state["branch"] = "main"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_uppercase_head_is_rejected(self) -> None:
        state = bootstrap()
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head="A" * 40,
                transition_class="INITIAL",
            )

    def test_duplicate_pending_heads_are_rejected(
        self,
    ) -> None:
        state = make_initial_state()
        state["pending_heads"] = [H1, H1]
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_current_unknown_freshness_is_rejected(
        self,
    ) -> None:
        state = make_current_state()
        state["remote_freshness"] = "UNKNOWN"
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="SAME",
            )

    def test_current_head_mismatch_is_rejected(
        self,
    ) -> None:
        state = make_current_state()
        state["latest_observed_head"] = H2
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H2,
                transition_class="SAME",
            )

    def test_evaluating_empty_queue_is_rejected(
        self,
    ) -> None:
        state = make_initial_state()
        state["observer_phase"] = "EVALUATING"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_candidate_pending_requires_qualified_head(
        self,
    ) -> None:
        state = make_initial_state()
        state["observer_phase"] = "CANDIDATE_PENDING"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_blocked_phase_requires_consistent_block_state(
        self,
    ) -> None:
        state = make_initial_state()
        state["observer_phase"] = "BLOCKED"
        state["projection_state"] = "STALE"
        state["blocked_head"] = H1
        state["last_failure_code"] = "BLOCKED_FOR_TEST"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_blocked_phase_requires_blocked_head(
        self,
    ) -> None:
        state = make_initial_state()
        state["observer_phase"] = "BLOCKED"
        state["projection_state"] = "BLOCKED"
        state["last_failure_code"] = "BLOCKED_FOR_TEST"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_caller_inputs_are_not_mutated(self) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        state_before = copy.deepcopy(state)
        payload_before = copy.deepcopy(payload)
        one_shot_tick(state, payload)
        self.assertEqual(state, state_before)
        self.assertEqual(payload, payload_before)

    def test_result_schemas_and_authority_flags(
        self,
    ) -> None:
        state = bootstrap()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        self.assertEqual(result["schema"], RESULT_SCHEMA)
        self.assertEqual(
            result["next_state"]["schema"],
            STATE_SCHEMA,
        )
        self.assertEqual(
            result["decision"]["schema"],
            DECISION_SCHEMA,
        )
        self.assertEqual(
            result["audit"]["schema"],
            EVENT_SCHEMA,
        )
        self.assertFalse(
            result["decision"][
                "automatic_promotion_authorized"
            ]
        )
        self.assertFalse(
            result["decision"][
                "production_write_authorized"
            ]
        )

    def test_same_inputs_are_byte_deterministic(
        self,
    ) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        first = one_shot_tick(state, payload)
        second = one_shot_tick(state, payload)
        self.assertEqual(first, second)
        self.assertEqual(
            canonical_result_bytes(first),
            canonical_result_bytes(second),
        )

    def test_canonical_result_is_compact_sorted_lf(
        self,
    ) -> None:
        state = bootstrap()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        raw = canonical_result_bytes(result)
        self.assertTrue(raw.endswith(b"\n"))
        self.assertNotIn(b": ", raw)
        self.assertNotIn(b", ", raw)
        decoded = json.loads(raw.decode("utf-8"))
        self.assertEqual(decoded, result)

    def test_audit_digests_match_canonical_values(
        self,
    ) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        result = one_shot_tick(state, payload)

        def digest(value: dict) -> str:
            raw = (
                json.dumps(
                    value,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                    allow_nan=False,
                )
                + "\n"
            ).encode("utf-8")
            return hashlib.sha256(raw).hexdigest()

        audit = result["audit"]
        self.assertEqual(
            audit["previous_state_digest"],
            digest(state),
        )
        self.assertEqual(
            audit["input_digest"],
            digest(payload),
        )
        self.assertEqual(
            audit["decision_digest"],
            digest(result["decision"]),
        )
        self.assertEqual(
            audit["next_state_digest"],
            digest(result["next_state"]),
        )

    def test_audit_has_no_volatile_host_fields(
        self,
    ) -> None:
        state = bootstrap()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        audit = result["audit"]
        for forbidden in (
            "observed_at",
            "timestamp",
            "host_id",
            "process_id",
            "pid",
            "path",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, audit)


if __name__ == "__main__":
    unittest.main()

~~~~

# SOURCE: P5-D4 BOUNDED LOOP CONTRACT

Path: tools/obsidian_projection/p5d4_bounded_observer_loop_contract_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_P5D4_BOUNDED_OBSERVER_LOOP_CONTRACT_V0_1",
  "status": "CANDIDATE_PREREGISTRATION_ONLY",
  "source_repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "monitored_source": {
    "remote": "origin",
    "branch": "integration/system-v1",
    "canonical_authority": "GITHUB_REMOTE_BRANCH",
    "local_working_tree_is_not_authority": true
  },
  "frontier": "P5-D4-BOUNDED-OBSERVER-LOOP-CANDIDATE",
  "title": "BOUNDED_OBSERVER_LOOP_CONTRACT",
  "purpose": "Define a finite, persistent and auditable orchestration envelope around already-qualified P5-D2/P5-D3 one-shot primitives without creating implicit promotion authority, permanent background execution, or P5-E near-real-time authority.",
  "qualified_predecessors": {
    "p5d1_observer_core_contract_blob": "a20999ae991e07447e25ecd1592964f2d333449b",
    "p5d2_one_shot_contract_blob": "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3",
    "p5d2_observer_tick_blob": "fd212f61ec38332b677110f40265638af55a73e2",
    "p5d3d_finite_evaluator_contract_blob": "b6c17167875874db30a575be95e8e6aa33d630dd",
    "p5d3d_finite_evaluator_blob": "bff5f51abbb344c1ccc5e9c669a11cf0e26c2562",
    "p5d3e_real_exact_head_sandbox_contract_blob": "ae4b1691fae16fcd1616e265a089670b9654db4a",
    "p5d3e_verifier_blob": "bd7f63b08432a53eaff5deeb2147396eb60d723f",
    "p5d3f_handoff_contract_blob": "64744325251db350d26c0269090ce62d5fa5f2e8",
    "p5d3f_handoff_blob": "23a4cc69b3b9f6fab1a6d77bed0247fce9b69c60",
    "p5d3g_live_publication_contract_blob": "64997ddd9977229961387f66af4de356c045c0ac",
    "p5d3g_live_publication_blob": "956ccb7274cea366b1a414df5a9239cbf580e3bf",
    "p5d3g_stage_b_gate_contract_blob": "c5c7fbb52f3dd2e3d3f5d1c1bbdc1069e2dabead",
    "p5d3g_stage_b_prestate_rebind_amendment_blob": "441fea40d33aa85dcfc6305d4d32cef39c42388e",
    "p5d3g_stage_b_runtime_blob": "077ea7a428f90d64122f15fe6b52f342f329f7b6"
  },
  "core_authority_model": {
    "observer_semantic_state_mutation_authority": "P5D2_ONE_SHOT_TICK_ONLY",
    "direct_observer_state_mutation_forbidden": true,
    "p5d3_primitive_reimplementation_forbidden": true,
    "loop_authority_is_not_promotion_authority": true,
    "qualified_candidate_requires_separate_promotion_authority": true,
    "candidate_pending_without_separate_authority_result": "PROMOTION_AUTHORITY_REQUIRED",
    "automatic_live_publication_authorized": false,
    "implicit_stage_a_authority_authorized": false,
    "implicit_stage_b_authority_authorized": false,
    "historical_stage_a_or_stage_b_authority_reuse_forbidden": true
  },
  "schemas": {
    "loop_plan": "ATDS_OBSIDIAN_P5D4_LOOP_PLAN_V0_1",
    "loop_checkpoint": "ATDS_OBSIDIAN_P5D4_LOOP_CHECKPOINT_V0_1",
    "loop_event": "ATDS_OBSIDIAN_P5D4_LOOP_EVENT_V0_1",
    "ownership_record": "ATDS_OBSIDIAN_P5D4_OWNERSHIP_RECORD_V0_1",
    "reconciliation_report": "ATDS_OBSIDIAN_P5D4_RECONCILIATION_REPORT_V0_1"
  },
  "bounded_loop_envelope": {
    "every_run_requires_explicit_canonical_plan": true,
    "plan_digest_required": true,
    "unbounded_defaults_forbidden": true,
    "required_limits": {
      "max_cycles": {
        "type": "POSITIVE_INTEGER",
        "minimum": 1
      },
      "max_remote_observations": {
        "type": "POSITIVE_INTEGER",
        "minimum": 1
      },
      "max_evaluations": {
        "type": "NONNEGATIVE_INTEGER",
        "minimum": 0
      },
      "max_pending_heads": {
        "type": "POSITIVE_INTEGER",
        "minimum": 1
      },
      "max_consecutive_failures": {
        "type": "NONNEGATIVE_INTEGER",
        "minimum": 0
      }
    },
    "cycle_budget_consumed_exactly_once_per_started_cycle": true,
    "budget_check_required_before_starting_next_cycle": true,
    "bound_reached_must_not_inject_p5d2_shutdown_event": true,
    "bound_reached_is_runner_stop_not_semantic_state_transition": true,
    "loop_construct_without_verified_budget_forbidden": true,
    "allowed_terminal_reasons": [
      "BOUND_REACHED",
      "NO_PENDING_WORK",
      "BLOCKED_REQUIRES_ADJUDICATION",
      "PROMOTION_AUTHORITY_REQUIRED",
      "SHUTDOWN_REQUESTED",
      "LOCK_CONTENDED",
      "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
      "RECONCILIATION_REQUIRED",
      "FATAL_INCONSISTENCY"
    ],
    "terminal_reason_must_be_persisted": true,
    "new_cycle_after_terminal_reason_forbidden": true
  },
  "durable_observer_state_checkpoint": {
    "required": true,
    "location_class": "LOCALAPPDATA_OUTSIDE_VAULT",
    "candidate_root_expression": "%LOCALAPPDATA%\\ATDS-OBSIDIAN-PROJECTION\\P5D4",
    "inside_real_vault_forbidden": true,
    "inside_canonical_repository_forbidden": true,
    "canonical_json_required": true,
    "utf8_required": true,
    "terminal_lf_required": true,
    "sha256_required": true,
    "required_fields": [
      "schema",
      "loop_plan_digest_sha256",
      "observer_state",
      "observer_state_digest_sha256",
      "last_event_sequence",
      "last_event_digest_sha256",
      "checkpoint_generation"
    ],
    "observer_state_must_validate_under_p5d2": true,
    "last_event_sequence_must_equal_observer_state_last_event_sequence": true,
    "volatile_host_data_excluded_from_observer_state_digest": [
      "pid",
      "hostname",
      "wall_clock_time",
      "absolute_runtime_path",
      "process_start_time"
    ],
    "commit_protocol": [
      "BUILD_NEXT_STATE_ONLY_VIA_P5D2_ONE_SHOT_TICK",
      "BUILD_CANONICAL_LOOP_EVENT",
      "APPEND_AND_DURABLY_FLUSH_LOOP_EVENT",
      "WRITE_CHECKPOINT_TO_SIBLING_TEMP",
      "DURABLY_FLUSH_CHECKPOINT_TEMP",
      "ATOMIC_REPLACE_CHECKPOINT",
      "VERIFY_CHECKPOINT_READ_AFTER_WRITE"
    ],
    "checkpoint_may_not_be_committed_before_corresponding_event": true,
    "direct_in_place_checkpoint_overwrite_forbidden": true
  },
  "append_only_observer_event_log": {
    "required": true,
    "location_class": "LOCALAPPDATA_OUTSIDE_VAULT",
    "format": "CANONICAL_JSONL",
    "append_only": true,
    "truncate_forbidden": true,
    "rewrite_prior_record_forbidden": true,
    "durable_flush_required_before_checkpoint_replace": true,
    "every_accepted_p5d2_tick_requires_record": true,
    "required_fields": [
      "schema",
      "sequence",
      "loop_id",
      "cycle_index",
      "normalized_input",
      "p5d2_audit",
      "previous_state_digest_sha256",
      "next_state_digest_sha256",
      "previous_record_digest_sha256",
      "record_digest_sha256",
      "record_origin"
    ],
    "record_origin_allowed": [
      "LIVE_BOUNDED_LOOP",
      "EVIDENCE_RECONSTRUCTION"
    ],
    "hash_chain_required": true,
    "sequence_strictly_monotonic": true,
    "duplicate_sequence_forbidden": true,
    "unterminated_or_noncanonical_tail_requires_reconciliation": true,
    "event_log_is_evidence_not_source_authority": true
  },
  "queue_capacity_policy": {
    "runtime_capacity_source": "loop_plan.max_pending_heads",
    "fifo_required": true,
    "unique_heads_required": true,
    "silent_drop_forbidden": true,
    "silent_reorder_forbidden": true,
    "latest_only_replacement_forbidden": true,
    "direct_queue_mutation_outside_p5d2_forbidden": true,
    "coalescing_authorized": false,
    "reason_coalescing_closed": "P5-D2 has no qualified queue-coalescing semantic event in V0.1",
    "preflight_capacity_check_required_before_event_that_would_append": true,
    "capacity_exhausted_result": "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
    "capacity_exhausted_must_not_feed_mutating_event_to_p5d2": true,
    "active_evaluation_candidate_retargeting_forbidden": true
  },
  "single_instance_ownership": {
    "required": true,
    "scope": "P5D4_CONTROL_STATE_ROOT",
    "exclusive_ownership_record_required": true,
    "ownership_record_outside_vault": true,
    "second_instance_result": "NO_WRITE_BLOCKED_BY_LOCK",
    "second_instance_may_observe_only": false,
    "second_instance_may_advance_sequence": false,
    "second_instance_may_modify_checkpoint": false,
    "second_instance_may_append_event": false,
    "second_instance_may_start_evaluation": false,
    "stale_or_ambiguous_lock_auto_steal_authorized": false,
    "stale_or_ambiguous_lock_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "volatile_ownership_metadata_must_not_enter_semantic_observer_digest": true
  },
  "restart_reconciliation_protocol": {
    "required_before_any_loop_continuation_after_restart": true,
    "authority_order": [
      "GITHUB_REMOTE_BRANCH_SOURCE_AUTHORITY",
      "VERIFIED_PHYSICAL_CURRENT_PUBLICATION_FACT",
      "P5D4_CHECKPOINT_DERIVED_OPERATIONAL_STATE",
      "P5D4_EVENT_LOG_AUDIT_EVIDENCE"
    ],
    "fresh_remote_read_only_observation_required": true,
    "physical_current_verification_required": true,
    "checkpoint_validation_required_if_present": true,
    "event_log_tail_validation_required_if_present": true,
    "allowed_checkpoint_log_relation": [
      "EXACTLY_ALIGNED",
      "LOG_EXACTLY_ONE_RECORD_AHEAD_WITH_REPLAYABLE_TRANSITION"
    ],
    "checkpoint_ahead_of_log_forbidden": true,
    "log_more_than_one_record_ahead_forbidden": true,
    "one_record_ahead_recovery": {
      "requires_previous_state_digest_match_checkpoint": true,
      "requires_deterministic_replay_via_p5d2_one_shot_tick": true,
      "requires_replayed_next_state_digest_match_log": true,
      "action": "ADVANCE_CHECKPOINT_ONLY_AFTER_REPLAY_MATCH"
    },
    "current_head_checkpoint_live_head_mismatch_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "event_tail_checkpoint_sequence_mismatch_unrecoverable_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "remote_non_fast_forward_or_unknown_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "restart_may_not_repeat_completed_evaluation_without_evidence": true,
    "restart_may_not_repeat_completed_promotion_without_evidence": true,
    "no_checkpoint_no_log_current_absent_result": "INITIALIZE_CANONICAL_P5D2_STATE",
    "no_checkpoint_no_log_current_present_result": "EVIDENCE_RECONSTRUCTION_REQUIRED",
    "evidence_reconstruction": {
      "direct_state_assignment_forbidden": true,
      "must_start_from_p5d2_make_initial_state": true,
      "must_use_p5d2_one_shot_tick_for_each_semantic_transition": true,
      "verified_current_identity_required": true,
      "matching_p5d3g_physical_and_logical_receipts_required": true,
      "reconstructed_event_records_must_use_origin": "EVIDENCE_RECONSTRUCTION",
      "reconstruction_must_not_claim_new_evaluation_or_new_publication_execution": true,
      "missing_or_ambiguous_p5d3g_evidence_result": "BLOCKED_REQUIRES_ADJUDICATION"
    }
  },
  "observation_adapter_boundary": {
    "remote_io_outside_p5d2_required": true,
    "normalized_event_injection_required": true,
    "one_shot_tick_network_io_remains_forbidden": true,
    "real_remote_observation_may_use_read_only_git": true,
    "time_based_polling_in_p5d4_v0_1_authorized": false,
    "sleep_or_timer_authorized": false,
    "p5e_owns_near_real_time_polling_qualification": true
  },
  "evaluation_orchestration": {
    "evaluation_may_start_only_on_p5d2_action": "START_EXACT_HEAD_EVALUATION",
    "evaluation_candidate_must_equal_queue_head": true,
    "candidate_head_frozen_for_entire_finite_evaluation": true,
    "new_remote_head_may_be_observed_while_evaluation_active_only_as_separately_queued_work": true,
    "active_evaluation_retarget_forbidden": true,
    "finite_evaluator_reuse_required": true,
    "qualified_evaluator_reimplementation_forbidden": true,
    "blocked_and_rejected_semantics_must_remain_distinct": true,
    "evaluation_result_must_reenter_state_only_via_p5d2_one_shot_tick": true
  },
  "promotion_boundary": {
    "candidate_pending_is_terminal_for_automatic_p5d4_orchestration": true,
    "required_stop_reason_without_separate_authority": "PROMOTION_AUTHORITY_REQUIRED",
    "p5d3f_or_p5d3g_invocation_from_loop_without_separate_authority_forbidden": true,
    "automatic_stage_a_authority_forbidden": true,
    "automatic_stage_b_authority_forbidden": true,
    "old_authorization_reuse_forbidden": true,
    "promotion_confirmed_may_enter_observer_state_only_from_verified_external_promotion_evidence": true,
    "promotion_failed_may_enter_observer_state_only_from_verified_external_failure_evidence": true
  },
  "failure_and_stop_semantics": {
    "fail_closed_default": true,
    "state_or_log_corruption_result": "FATAL_INCONSISTENCY",
    "unexpected_exception_result": "FATAL_INCONSISTENCY",
    "network_failure_must_not_create_current_claim": true,
    "last_known_good_live_projection_preserved_on_failure": true,
    "loop_stop_must_not_delete_checkpoint_or_event_log": true,
    "loop_stop_must_not_delete_last_known_good_generation": true
  },
  "contract_only_boundary": {
    "contract_and_tests_only": true,
    "loop_runtime_creation_authorized": false,
    "loop_runtime_modification_authorized": false,
    "bounded_loop_execution_authorized": false,
    "repeated_real_polling_authorized": false,
    "sleep_authorized": false,
    "timer_authorized": false,
    "permanent_daemon_authorized": false,
    "windows_startup_authorized": false,
    "scheduled_task_authorized": false,
    "windows_service_authorized": false,
    "real_vault_mutation_authorized": false,
    "automatic_publication_authorized": false,
    "implicit_stage_a_authority_authorized": false,
    "implicit_stage_b_authority_authorized": false,
    "p5e_authorized": false,
    "p6_authorized": false
  },
  "required_breakers": [
    "UNBOUNDED_LOOP_PLAN_ACCEPTED",
    "ZERO_OR_NEGATIVE_MAX_CYCLES_ACCEPTED",
    "CYCLE_STARTED_AFTER_BUDGET_EXHAUSTED",
    "BOUND_REACHED_INJECTS_P5D2_SHUTDOWN_EVENT",
    "NEW_CYCLE_AFTER_TERMINAL_REASON",
    "DIRECT_OBSERVER_STATE_MUTATION",
    "CHECKPOINT_INSIDE_REAL_VAULT",
    "CHECKPOINT_INSIDE_CANONICAL_REPOSITORY",
    "CHECKPOINT_DIRECT_IN_PLACE_OVERWRITE",
    "CHECKPOINT_COMMITTED_BEFORE_EVENT_APPEND",
    "CHECKPOINT_STATE_DIGEST_MISMATCH",
    "CHECKPOINT_SEQUENCE_DIFFERS_FROM_OBSERVER_STATE",
    "VOLATILE_HOST_DATA_LAUNDERED_INTO_SEMANTIC_DIGEST",
    "EVENT_LOG_TRUNCATED",
    "EVENT_LOG_PRIOR_RECORD_REWRITTEN",
    "EVENT_SEQUENCE_DUPLICATED",
    "EVENT_SEQUENCE_SKIPPED",
    "EVENT_HASH_CHAIN_BROKEN",
    "CHECKPOINT_AHEAD_OF_EVENT_LOG",
    "EVENT_LOG_MORE_THAN_ONE_RECORD_AHEAD",
    "ONE_RECORD_AHEAD_REPLAY_DIGEST_MISMATCH",
    "QUEUE_OVERFLOW_SILENT_DROP",
    "QUEUE_OVERFLOW_LATEST_ONLY_REPLACEMENT",
    "QUEUE_REORDERED",
    "QUEUE_DUPLICATE_HEAD",
    "QUEUE_MUTATED_OUTSIDE_P5D2",
    "QUEUE_COALESCING_WITHOUT_QUALIFIED_P5D2_EVENT",
    "ACTIVE_EVALUATION_RETARGETED",
    "SECOND_LOOP_RUNNER_ADVANCES_SEQUENCE",
    "SECOND_LOOP_RUNNER_WRITES_CHECKPOINT",
    "SECOND_LOOP_RUNNER_STARTS_EVALUATION",
    "STALE_LOCK_AUTO_STOLEN",
    "RESTART_CONTINUES_WITHOUT_RECONCILIATION",
    "CURRENT_DIFFERS_FROM_CHECKPOINT_LIVE_HEAD",
    "CHECKPOINT_LOG_TAIL_UNRECOVERABLE_MISMATCH_CONTINUES",
    "RESTART_REPEATS_COMPLETED_EVALUATION",
    "RESTART_REPEATS_COMPLETED_PROMOTION",
    "BOOTSTRAP_CURRENT_PRESENT_DIRECT_STATE_ASSIGNMENT",
    "BOOTSTRAP_CURRENT_PRESENT_WITHOUT_P5D3G_EVIDENCE",
    "EVIDENCE_RECONSTRUCTION_CLAIMS_NEW_PUBLICATION",
    "SAME_HEAD_TRIGGERS_EVALUATION",
    "REMOTE_NETWORK_FAILURE_MARKS_CURRENT",
    "NON_FAST_FORWARD_CONTINUES_AUTOMATICALLY",
    "UNKNOWN_ANCESTRY_CONTINUES_AUTOMATICALLY",
    "BLOCKED_RESULT_RELABELED_REJECTED",
    "REJECTED_RESULT_RELABELED_BLOCKED",
    "P5D3_FINITE_EVALUATOR_REIMPLEMENTED",
    "CANDIDATE_PENDING_AUTO_PUBLISHED",
    "P5D3F_CALLED_WITHOUT_SEPARATE_AUTHORITY",
    "P5D3G_CALLED_WITHOUT_SEPARATE_AUTHORITY",
    "OLD_STAGE_A_AUTHORITY_REUSED",
    "OLD_STAGE_B_AUTHORITY_REUSED",
    "PROMOTION_CONFIRMED_WITHOUT_VERIFIED_EXTERNAL_EVIDENCE",
    "LOOP_PUSHES_TO_GITHUB",
    "LOOP_COMMITS_CANONICAL_REPOSITORY",
    "LOOP_MUTATES_CANONICAL_WORKTREE",
    "LOOP_OVERWRITES_HUMAN_VIEWS",
    "LOOP_MODIFIES_OBSIDIAN_CONFIG",
    "REAL_VAULT_WRITE_SURFACE_INTRODUCED",
    "PERMANENT_DAEMON_SURFACE_INTRODUCED",
    "SLEEP_OR_TIMER_SURFACE_INTRODUCED",
    "WINDOWS_STARTUP_SURFACE_INTRODUCED",
    "SCHEDULED_TASK_SURFACE_INTRODUCED",
    "WINDOWS_SERVICE_SURFACE_INTRODUCED",
    "P5E_AUTHORITY_LEAK",
    "P6_AUTHORITY_LEAK"
  ],
  "qualification_requirements": {
    "static_contract_tests_required": true,
    "predecessor_pin_tests_required": true,
    "breaker_coverage_tests_required": true,
    "directly_affected_predecessor_contract_tests_required": [
      "P5D1_CONTINUOUS_OBSERVER_CORE_CONTRACT",
      "P5D2_ONE_SHOT_OBSERVER_TICK_CONTRACT",
      "P5D3A_CANDIDATE_EVALUATION_CONTRACT",
      "P5D3D_FINITE_CANDIDATE_EVALUATOR_CONTRACT",
      "P5D3G_LIVE_PUBLICATION_TRANSACTION_CONTRACT"
    ],
    "runtime_tests_required": false,
    "real_loop_execution_required": false,
    "real_vault_access_required": false
  },
  "next_gate": {
    "after_contract_qualification": "P5-D4-BOUNDED-OBSERVER-LOOP-RUNTIME-IMPLEMENTATION-CANDIDATE",
    "p5e": "END_TO_END_NEAR_REAL_TIME_QUALIFICATION",
    "p6": "CONTROLLED_KNOWLEDGE_GRAPH_ARCHITECTURE",
    "mandatory_human_stop_before_runtime": true
  }
}

~~~~

# SOURCE: P5-D4 BOUNDED LOOP RUNTIME

Path: tools/obsidian_projection/p5d4_bounded_observer_loop.py
~~~~
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import tempfile
from pathlib import Path
from typing import Any, Callable, Iterable

from .observer_tick import (
    INPUT_SCHEMA,
    _validate_state,
    make_initial_state,
    one_shot_tick,
)

PLAN_SCHEMA = "ATDS_OBSIDIAN_P5D4_LOOP_PLAN_V0_1"
CHECKPOINT_SCHEMA = "ATDS_OBSIDIAN_P5D4_LOOP_CHECKPOINT_V0_1"
EVENT_SCHEMA = "ATDS_OBSIDIAN_P5D4_LOOP_EVENT_V0_1"
OWNERSHIP_SCHEMA = "ATDS_OBSIDIAN_P5D4_OWNERSHIP_RECORD_V0_1"
EVIDENCE_SCHEMA = "ATDS_OBSIDIAN_P5D4_VERIFIED_PUBLICATION_EVIDENCE_V0_1"
RUN_RESULT_SCHEMA = "ATDS_OBSIDIAN_P5D4_BOUNDED_LOOP_RESULT_V0_1"

_HEAD_RE = re.compile(r"^[0-9a-f]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_PLAN_KEYS = frozenset({
    "schema","loop_id","max_cycles","max_remote_observations",
    "max_evaluations","max_pending_heads","max_consecutive_failures",
    "plan_digest_sha256",
})

class P5D4RuntimeError(RuntimeError):
    pass

class LoopPlanError(P5D4RuntimeError):
    pass

class PersistenceError(P5D4RuntimeError):
    pass

class ReconciliationError(P5D4RuntimeError):
    pass

class OwnershipError(P5D4RuntimeError):
    pass

class OwnershipContended(OwnershipError):
    pass

class QueueCapacityError(P5D4RuntimeError):
    pass

class ControlRootBindingError(P5D4RuntimeError):
    pass

def _canonical_bytes(value: Any) -> bytes:
    try:
        text = json.dumps(
            value, ensure_ascii=False, sort_keys=True,
            separators=(",", ":"), allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise PersistenceError("value is not canonical JSON") from exc
    return (text + "\n").encode("utf-8")

def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()

def _is_int(value: Any, minimum: int) -> bool:
    return not isinstance(value, bool) and isinstance(value, int) and value >= minimum

def _is_head(value: Any) -> bool:
    return isinstance(value, str) and _HEAD_RE.fullmatch(value) is not None

def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None

def _plan_payload(plan: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in plan.items() if key != "plan_digest_sha256"}

def make_loop_plan(
    *,
    loop_id: str,
    max_cycles: int,
    max_remote_observations: int,
    max_evaluations: int,
    max_pending_heads: int,
    max_consecutive_failures: int,
) -> dict[str, Any]:
    plan = {
        "schema": PLAN_SCHEMA,
        "loop_id": loop_id,
        "max_cycles": max_cycles,
        "max_remote_observations": max_remote_observations,
        "max_evaluations": max_evaluations,
        "max_pending_heads": max_pending_heads,
        "max_consecutive_failures": max_consecutive_failures,
    }
    plan["plan_digest_sha256"] = _digest(plan)
    return validate_loop_plan(plan)

def validate_loop_plan(plan: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(plan, dict) or frozenset(plan) != _PLAN_KEYS:
        raise LoopPlanError("loop plan fields mismatch")
    if plan["schema"] != PLAN_SCHEMA:
        raise LoopPlanError("loop plan schema mismatch")
    loop_id = plan["loop_id"]
    if not isinstance(loop_id, str) or not loop_id or loop_id.strip() != loop_id:
        raise LoopPlanError("invalid loop_id")
    for field, minimum in (
        ("max_cycles", 1),
        ("max_remote_observations", 1),
        ("max_evaluations", 0),
        ("max_pending_heads", 1),
        ("max_consecutive_failures", 0),
    ):
        if not _is_int(plan[field], minimum):
            raise LoopPlanError(f"invalid {field}")
    expected = _digest(_plan_payload(plan))
    if plan["plan_digest_sha256"] != expected:
        raise LoopPlanError("loop plan digest mismatch")
    return json.loads(_canonical_bytes(plan).decode("utf-8"))

def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]

def _resolved(path: Path) -> Path:
    try:
        return Path(path).resolve(strict=False)
    except OSError as exc:
        raise P5D4RuntimeError("path resolution unavailable") from exc

def _intersects(first: Path, second: Path) -> bool:
    return (
        first == second
        or first in second.parents
        or second in first.parents
    )

def _normcase_path(path: Path) -> str:
    return os.path.normcase(os.path.normpath(str(path)))

def _path_is_within(path: Path, anchor: Path) -> bool:
    candidate = _normcase_path(path)
    parent = _normcase_path(anchor)
    try:
        return os.path.commonpath([candidate, parent]) == parent
    except ValueError:
        return False

def _existing_chain_has_reparse_point(path: Path) -> bool:
    current = Path(path)
    visited: set[str] = set()
    for _ in range(512):
        key = _normcase_path(current)
        if key in visited:
            raise ControlRootBindingError("control root path chain loop detected")
        visited.add(key)
        try:
            if current.exists() or current.is_symlink():
                info = os.lstat(current)
                attributes = getattr(info, "st_file_attributes", 0)
                reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
                if current.is_symlink() or (reparse_flag and attributes & reparse_flag):
                    return True
                is_junction = getattr(current, "is_junction", None)
                if callable(is_junction) and is_junction():
                    return True
        except OSError as exc:
            raise ControlRootBindingError(
                "control root path chain inspection unavailable"
            ) from exc
        if current.parent == current:
            return False
        current = current.parent
    raise ControlRootBindingError("control root path depth exceeds bound")

def _userprofile_root() -> Path:
    value = os.environ.get("USERPROFILE")
    if not isinstance(value, str) or not value.strip():
        raise ControlRootBindingError("USERPROFILE unavailable")
    profile = Path(value)
    if not profile.is_absolute():
        raise ControlRootBindingError("USERPROFILE is not absolute")
    return _resolved(profile)

def canonical_production_control_root() -> Path:
    return _userprofile_root() / "ATDS-CONTROL" / "OBSIDIAN-PROJECTION" / "P5D4"

def _qualification_control_anchor() -> Path:
    return _userprofile_root() / "ATDS-CONTROL" / "_QUALIFICATION"

def resolve_and_validate_control_root(root: Path) -> Path:
    requested = Path(root)
    if not requested.is_absolute():
        raise ControlRootBindingError("control root must be absolute")
    if _existing_chain_has_reparse_point(requested):
        raise ControlRootBindingError(
            "control root path chain contains reparse point"
        )

    resolved = _resolved(requested)
    canonical = _resolved(canonical_production_control_root())
    qualification = _resolved(_qualification_control_anchor())
    temp_root = _resolved(Path(tempfile.gettempdir()))

    requested_norm = _normcase_path(resolved)
    canonical_norm = _normcase_path(canonical)
    is_production = requested_norm == canonical_norm
    is_qualification = _path_is_within(resolved, qualification)
    is_temp = _path_is_within(resolved, temp_root)

    if not (is_production or is_qualification or is_temp):
        raise ControlRootBindingError(
            "control root is outside canonical or synthetic qualification namespaces"
        )

    if is_production:
        localappdata = os.environ.get("LOCALAPPDATA")
        appdata = os.environ.get("APPDATA")
        for forbidden in (localappdata, appdata):
            if isinstance(forbidden, str) and forbidden.strip():
                if _path_is_within(canonical, _resolved(Path(forbidden))):
                    raise ControlRootBindingError(
                        "production control root depends on AppData"
                    )
        lowered = _normcase_path(canonical)
        if (
            os.path.normcase("\\packages\\") in lowered
            or os.path.normcase("\\localcache\\") in lowered
        ):
            raise ControlRootBindingError(
                "production control root is Store-redirectable"
            )
        return canonical

    return resolved

def _validate_control_root(
    root: Path,
    *,
    forbidden_roots: Iterable[Path] = (),
) -> Path:
    resolved = resolve_and_validate_control_root(root)
    protected = (_resolved(_repo_root()),) + tuple(_resolved(x) for x in forbidden_roots)
    if any(_intersects(resolved, item) for item in protected):
        raise P5D4RuntimeError("control root intersects protected root")
    try:
        resolved.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise P5D4RuntimeError("control root unavailable") from exc
    if not resolved.is_dir():
        raise P5D4RuntimeError("control root is not a directory")
    return resolved

def _write_durable(path: Path, raw: bytes, *, exclusive: bool = False) -> None:
    flags = os.O_WRONLY | os.O_CREAT
    flags |= os.O_EXCL if exclusive else os.O_TRUNC
    fd = os.open(str(path), flags, 0o600)
    try:
        with os.fdopen(fd, "wb", closefd=False) as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(fd)
def acquire_ownership(
    control_root: Path,
    *,
    loop_id: str,
    owner_token: str,
) -> dict[str, Any]:
    root = _validate_control_root(control_root)
    if not isinstance(loop_id, str) or not loop_id:
        raise OwnershipError("invalid loop id")
    if not isinstance(owner_token, str) or not owner_token:
        raise OwnershipError("invalid owner token")
    record = {
        "schema": OWNERSHIP_SCHEMA,
        "loop_id": loop_id,
        "owner_token": owner_token,
    }
    path = root / "ownership.lock"
    try:
        _write_durable(path, _canonical_bytes(record), exclusive=True)
    except FileExistsError as exc:
        raise OwnershipContended("ownership already held") from exc
    return record

def release_ownership(control_root: Path, ownership: dict[str, Any]) -> None:
    root = _validate_control_root(control_root)
    path = root / "ownership.lock"
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise OwnershipError("ownership record unavailable") from exc
    try:
        current = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise OwnershipError("ownership record invalid") from exc
    if raw != _canonical_bytes(current) or current != ownership:
        raise OwnershipError("ownership mismatch")
    try:
        path.unlink()
    except OSError as exc:
        raise OwnershipError("ownership release failed") from exc

def _event_record_digest(record: dict[str, Any]) -> str:
    body = dict(record)
    body.pop("record_digest_sha256", None)
    return _digest(body)

def load_event_log(control_root: Path) -> list[dict[str, Any]]:
    root = _validate_control_root(control_root)
    path = root / "observer-events.jsonl"
    if not path.exists():
        return []
    raw = path.read_bytes()
    if not raw:
        return []
    if not raw.endswith(b"\n"):
        raise PersistenceError("event log has unterminated record")
    records: list[dict[str, Any]] = []
    previous_digest: str | None = None
    expected_sequence = 1
    for line in raw.splitlines(keepends=True):
        try:
            record = json.loads(line.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PersistenceError("event log record invalid") from exc
        if line != _canonical_bytes(record):
            raise PersistenceError("event log record noncanonical")
        required = {
            "schema","sequence","loop_id","cycle_index","normalized_input",
            "p5d2_audit","previous_state_digest_sha256",
            "next_state_digest_sha256","previous_record_digest_sha256",
            "record_digest_sha256","record_origin",
        }
        if set(record) != required or record.get("schema") != EVENT_SCHEMA:
            raise PersistenceError("event log fields mismatch")
        if record["record_origin"] not in {
            "LIVE_BOUNDED_LOOP",
            "EVIDENCE_RECONSTRUCTION",
        }:
            raise PersistenceError("event log record origin invalid")
        if record["sequence"] != expected_sequence:
            raise PersistenceError("event log sequence mismatch")
        if record["previous_record_digest_sha256"] != previous_digest:
            raise PersistenceError("event log hash chain mismatch")
        if record["record_digest_sha256"] != _event_record_digest(record):
            raise PersistenceError("event log digest mismatch")
        event = record["normalized_input"]
        audit = record["p5d2_audit"]
        if (
            not isinstance(event, dict)
            or event.get("sequence") != expected_sequence
            or not isinstance(audit, dict)
            or audit.get("sequence") != expected_sequence
            or audit.get("next_state_digest") != record["next_state_digest_sha256"]
            or audit.get("previous_state_digest") != record["previous_state_digest_sha256"]
        ):
            raise PersistenceError("event log P5-D2 binding mismatch")
        previous_digest = record["record_digest_sha256"]
        expected_sequence += 1
        records.append(record)
    return records

def load_checkpoint(control_root: Path) -> dict[str, Any] | None:
    root = _validate_control_root(control_root)
    path = root / "observer-checkpoint.json"
    if not path.exists():
        return None
    raw = path.read_bytes()
    try:
        checkpoint = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PersistenceError("checkpoint invalid") from exc
    if raw != _canonical_bytes(checkpoint):
        raise PersistenceError("checkpoint noncanonical")
    required = {
        "schema","loop_plan_digest_sha256","observer_state",
        "observer_state_digest_sha256","last_event_sequence",
        "last_event_digest_sha256","checkpoint_generation",
    }
    if set(checkpoint) != required or checkpoint.get("schema") != CHECKPOINT_SCHEMA:
        raise PersistenceError("checkpoint fields mismatch")
    state = checkpoint["observer_state"]
    try:
        _validate_state(state)
    except Exception as exc:
        raise PersistenceError("checkpoint observer state invalid") from exc
    if checkpoint["observer_state_digest_sha256"] != _digest(state):
        raise PersistenceError("checkpoint state digest mismatch")
    if checkpoint["last_event_sequence"] != state["last_event_sequence"]:
        raise PersistenceError("checkpoint sequence mismatch")
    if not _is_int(checkpoint["checkpoint_generation"], 1):
        raise PersistenceError("checkpoint generation invalid")
    if not _is_sha256(checkpoint["loop_plan_digest_sha256"]):
        raise PersistenceError("checkpoint plan digest invalid")
    if not _is_sha256(checkpoint["last_event_digest_sha256"]):
        raise PersistenceError("checkpoint event digest invalid")
    return checkpoint

def _checkpoint_value(
    *,
    plan: dict[str, Any],
    state: dict[str, Any],
    event_digest: str,
    generation: int,
) -> dict[str, Any]:
    return {
        "schema": CHECKPOINT_SCHEMA,
        "loop_plan_digest_sha256": plan["plan_digest_sha256"],
        "observer_state": state,
        "observer_state_digest_sha256": _digest(state),
        "last_event_sequence": state["last_event_sequence"],
        "last_event_digest_sha256": event_digest,
        "checkpoint_generation": generation,
    }

def _write_checkpoint(
    root: Path,
    *,
    plan: dict[str, Any],
    state: dict[str, Any],
    event_digest: str,
) -> dict[str, Any]:
    existing = load_checkpoint(root)
    generation = 1 if existing is None else existing["checkpoint_generation"] + 1
    value = _checkpoint_value(
        plan=plan, state=state, event_digest=event_digest, generation=generation)
    temp = root / "observer-checkpoint.tmp"
    final = root / "observer-checkpoint.json"
    _write_durable(temp, _canonical_bytes(value))
    try:
        os.replace(str(temp), str(final))
    except OSError as exc:
        raise PersistenceError("checkpoint atomic replace failed") from exc
    verified = load_checkpoint(root)
    if verified != value:
        raise PersistenceError("checkpoint read-after-write mismatch")
    return verified
def _append_event(root: Path, record: dict[str, Any]) -> None:
    path = root / "observer-events.jsonl"
    raw = _canonical_bytes(record)
    try:
        with path.open("ab") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except OSError as exc:
        raise PersistenceError("event append failed") from exc

def _would_append_queue(state: dict[str, Any], event: dict[str, Any]) -> bool:
    return (
        event.get("event_type") == "REMOTE_HEAD_OBSERVED"
        and event.get("transition_class") in {"INITIAL", "FAST_FORWARD"}
        and event.get("observed_head") not in state.get("pending_heads", [])
    )

def persist_tick(
    *,
    control_root: Path,
    plan: dict[str, Any],
    previous_state: dict[str, Any],
    normalized_input: dict[str, Any],
    loop_id: str,
    cycle_index: int,
    record_origin: str = "LIVE_BOUNDED_LOOP",
    fault_injector: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    plan = validate_loop_plan(plan)
    root = _validate_control_root(control_root)
    try:
        _validate_state(previous_state)
    except Exception as exc:
        raise PersistenceError("previous observer state invalid") from exc
    if loop_id != plan["loop_id"]:
        raise PersistenceError("loop id mismatch")
    if record_origin not in {"LIVE_BOUNDED_LOOP", "EVIDENCE_RECONSTRUCTION"}:
        raise PersistenceError("record origin invalid")
    if _would_append_queue(previous_state, normalized_input):
        if len(previous_state["pending_heads"]) >= plan["max_pending_heads"]:
            raise QueueCapacityError("pending queue capacity exhausted")

    log = load_event_log(root)
    if log:
        tail = log[-1]
        if tail["sequence"] != previous_state["last_event_sequence"]:
            raise PersistenceError("event log/state sequence mismatch")
        if tail["next_state_digest_sha256"] != _digest(previous_state):
            raise PersistenceError("event log/state digest mismatch")
    elif previous_state["last_event_sequence"] != 0:
        raise PersistenceError("noninitial state has no event history")
    tick = one_shot_tick(previous_state, normalized_input)
    audit = tick["audit"]
    previous_record_digest = log[-1]["record_digest_sha256"] if log else None
    record = {
        "schema": EVENT_SCHEMA,
        "sequence": normalized_input["sequence"],
        "loop_id": loop_id,
        "cycle_index": cycle_index,
        "normalized_input": normalized_input,
        "p5d2_audit": audit,
        "previous_state_digest_sha256": audit["previous_state_digest"],
        "next_state_digest_sha256": audit["next_state_digest"],
        "previous_record_digest_sha256": previous_record_digest,
        "record_origin": record_origin,
    }
    record["record_digest_sha256"] = _event_record_digest(record)
    _append_event(root, record)
    if fault_injector is not None:
        fault_injector("AFTER_EVENT_DURABLE_BEFORE_CHECKPOINT_REPLACE")
    checkpoint = _write_checkpoint(
        root,
        plan=plan,
        state=tick["next_state"],
        event_digest=record["record_digest_sha256"],
    )
    return {
        "tick_result": tick,
        "event_record": record,
        "checkpoint": checkpoint,
    }

def _replay_record(
    state: dict[str, Any],
    record: dict[str, Any],
) -> dict[str, Any]:
    if record["previous_state_digest_sha256"] != _digest(state):
        raise ReconciliationError("replay previous-state digest mismatch")
    try:
        tick = one_shot_tick(state, record["normalized_input"])
    except Exception as exc:
        raise ReconciliationError("P5-D2 replay rejected") from exc
    if tick["audit"] != record["p5d2_audit"]:
        raise ReconciliationError("replay audit mismatch")
    if _digest(tick["next_state"]) != record["next_state_digest_sha256"]:
        raise ReconciliationError("replay next-state digest mismatch")
    return tick["next_state"]

def _validate_evidence(
    verified_current_head: str,
    evidence: dict[str, Any] | None,
) -> dict[str, Any]:
    if not _is_head(verified_current_head):
        raise ReconciliationError("verified CURRENT head invalid")
    if not isinstance(evidence, dict):
        raise ReconciliationError("verified publication evidence required")
    required = {
        "schema","candidate_head","status","transaction_plan_digest_sha256",
        "physical_receipt_digest_sha256","logical_receipt_digest_sha256",
        "p5d2_promotion_confirmed_emitted",
    }
    if set(evidence) != required or evidence.get("schema") != EVIDENCE_SCHEMA:
        raise ReconciliationError("publication evidence fields mismatch")
    if evidence["candidate_head"] != verified_current_head:
        raise ReconciliationError("publication evidence head mismatch")
    if evidence["status"] != "PASS_LIVE_PUBLICATION_CONFIRMED":
        raise ReconciliationError("publication evidence status mismatch")
    for field in (
        "transaction_plan_digest_sha256",
        "physical_receipt_digest_sha256",
        "logical_receipt_digest_sha256",
    ):
        if not _is_sha256(evidence[field]):
            raise ReconciliationError("publication evidence digest invalid")
    if evidence["p5d2_promotion_confirmed_emitted"] is not True:
        raise ReconciliationError("promotion confirmation evidence missing")
    return evidence

def reconstruct_from_verified_publication_evidence(
    *,
    control_root: Path,
    plan: dict[str, Any],
    verified_current_head: str,
    promotion_evidence: dict[str, Any] | None,
) -> dict[str, Any]:
    plan = validate_loop_plan(plan)
    root = _validate_control_root(control_root)
    if load_checkpoint(root) is not None or load_event_log(root):
        raise ReconciliationError("evidence reconstruction requires empty control state")
    _validate_evidence(verified_current_head, promotion_evidence)
    state = make_initial_state()
    events = (
        {
            "schema": INPUT_SCHEMA, "event_type": "REMOTE_HEAD_OBSERVED",
            "sequence": 1, "observed_head": verified_current_head,
            "transition_class": "INITIAL", "candidate_head": None, "failure_code": None,
        },
        {
            "schema": INPUT_SCHEMA, "event_type": "EVALUATION_STARTED",
            "sequence": 2, "observed_head": None, "transition_class": None,
            "candidate_head": verified_current_head, "failure_code": None,
        },
        {
            "schema": INPUT_SCHEMA, "event_type": "EVALUATION_PASSED",
            "sequence": 3, "observed_head": None, "transition_class": None,
            "candidate_head": verified_current_head, "failure_code": None,
        },
        {
            "schema": INPUT_SCHEMA, "event_type": "PROMOTION_CONFIRMED",
            "sequence": 4, "observed_head": None, "transition_class": None,
            "candidate_head": verified_current_head, "failure_code": None,
        },
    )
    for event in events:
        persisted = persist_tick(
            control_root=root,
            plan=plan,
            previous_state=state,
            normalized_input=event,
            loop_id=plan["loop_id"],
            cycle_index=0,
            record_origin="EVIDENCE_RECONSTRUCTION",
        )
        state = persisted["tick_result"]["next_state"]
    return {
        "status": "PASS_RECONSTRUCTED_VERIFIED_PUBLICATION_EVIDENCE",
        "observer_state": state,
        "evidence": promotion_evidence,
    }

def reconcile_control_state(
    *,
    control_root: Path,
    plan: dict[str, Any],
    verified_current_head: str | None,
    promotion_evidence: dict[str, Any] | None,
) -> dict[str, Any]:
    plan = validate_loop_plan(plan)
    root = _validate_control_root(control_root)
    log = load_event_log(root)
    checkpoint = load_checkpoint(root)

    if checkpoint is None and not log:
        if verified_current_head is None:
            return {
                "status": "PASS_CANONICAL_INITIAL_STATE",
                "observer_state": make_initial_state(),
            }
        return reconstruct_from_verified_publication_evidence(
            control_root=root,
            plan=plan,
            verified_current_head=verified_current_head,
            promotion_evidence=promotion_evidence,
        )

    if checkpoint is None:
        if len(log) != 1:
            raise ReconciliationError("event log too far ahead without checkpoint")
        base = make_initial_state()
        next_state = _replay_record(base, log[0])
        _write_checkpoint(
            root,
            plan=plan,
            state=next_state,
            event_digest=log[0]["record_digest_sha256"],
        )
        return {
            "status": "PASS_RECONCILED_ONE_RECORD_AHEAD",
            "observer_state": next_state,
        }

    if checkpoint["loop_plan_digest_sha256"] != plan["plan_digest_sha256"]:
        raise ReconciliationError("checkpoint loop-plan mismatch")
    cp_seq = checkpoint["last_event_sequence"]
    if cp_seq > len(log):
        raise ReconciliationError("checkpoint ahead of event log")
    delta = len(log) - cp_seq
    if delta > 1:
        raise ReconciliationError("event log more than one record ahead")
    state = checkpoint["observer_state"]
    if cp_seq:
        tail_at_checkpoint = log[cp_seq - 1]
        if checkpoint["last_event_digest_sha256"] != tail_at_checkpoint["record_digest_sha256"]:
            raise ReconciliationError("checkpoint event digest mismatch")
        if checkpoint["observer_state_digest_sha256"] != tail_at_checkpoint["next_state_digest_sha256"]:
            raise ReconciliationError("checkpoint/log state digest mismatch")
    if delta == 1:
        record = log[-1]
        state = _replay_record(state, record)
        _write_checkpoint(
            root,
            plan=plan,
            state=state,
            event_digest=record["record_digest_sha256"],
        )
        status = "PASS_RECONCILED_ONE_RECORD_AHEAD"
    else:
        status = "PASS_RECONCILED_ALIGNED"

    live = state["live_projection_head"]
    if verified_current_head is None:
        if live is not None:
            raise ReconciliationError("checkpoint live head has no physical CURRENT")
    elif live != verified_current_head:
        raise ReconciliationError("physical CURRENT differs from checkpoint live head")

    return {"status": status, "observer_state": state}

def _normalized_event(
    state: dict[str, Any],
    event_type: str,
    *,
    candidate_head: str | None = None,
    failure_code: str | None = None,
) -> dict[str, Any]:
    return {
        "schema": INPUT_SCHEMA,
        "event_type": event_type,
        "sequence": state["last_event_sequence"] + 1,
        "observed_head": None,
        "transition_class": None,
        "candidate_head": candidate_head,
        "failure_code": failure_code,
    }

def _write_run_result(root: Path, result: dict[str, Any]) -> None:
    temp = root / "last-run.tmp"
    final = root / "last-run.json"
    _write_durable(temp, _canonical_bytes(result))
    try:
        os.replace(str(temp), str(final))
    except OSError as exc:
        raise PersistenceError("run-result replace failed") from exc

def _base_run_result(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": RUN_RESULT_SCHEMA,
        "loop_id": plan["loop_id"],
        "loop_plan_digest_sha256": plan["plan_digest_sha256"],
        "terminal_reason": None,
        "cycles_started": 0,
        "remote_observations": 0,
        "evaluations_started": 0,
        "consecutive_failures": 0,
        "observer_state": None,
        "automatic_promotion_authorized": False,
        "production_write_authorized": False,
    }

def run_bounded_loop(
    *,
    plan: dict[str, Any],
    control_root: Path,
    observation_adapter: Callable[[dict[str, Any]], dict[str, Any]],
    evaluation_adapter: Callable[[str, dict[str, Any]], dict[str, Any]],
    verified_current_head: str | None,
    promotion_evidence: dict[str, Any] | None,
    forbidden_roots: Iterable[Path] = (),
    owner_token: str,
) -> dict[str, Any]:
    plan = validate_loop_plan(plan)
    root = _validate_control_root(control_root, forbidden_roots=forbidden_roots)
    result = _base_run_result(plan)
    try:
        ownership = acquire_ownership(
            root, loop_id=plan["loop_id"], owner_token=owner_token)
    except OwnershipContended:
        result["terminal_reason"] = "LOCK_CONTENDED"
        return result

    state: dict[str, Any] | None = None
    try:
        reconciled = reconcile_control_state(
            control_root=root,
            plan=plan,
            verified_current_head=verified_current_head,
            promotion_evidence=promotion_evidence,
        )
        state = reconciled["observer_state"]

        if state["observer_phase"] == "CANDIDATE_PENDING":
            result["terminal_reason"] = "PROMOTION_AUTHORITY_REQUIRED"
        elif state["observer_phase"] == "BLOCKED":
            result["terminal_reason"] = "BLOCKED_REQUIRES_ADJUDICATION"
        elif state["observer_phase"] == "EVALUATING":
            result["terminal_reason"] = "RECONCILIATION_REQUIRED"
        elif state["observer_phase"] == "STOPPED":
            result["terminal_reason"] = "SHUTDOWN_REQUESTED"

        for cycle_index in range(1, plan["max_cycles"] + 1):
            if result["terminal_reason"] is not None:
                break
            result["cycles_started"] += 1

            if state["pending_heads"]:
                if result["evaluations_started"] >= plan["max_evaluations"]:
                    result["terminal_reason"] = "BOUND_REACHED"
                    break
                candidate = state["pending_heads"][0]
                started = persist_tick(
                    control_root=root,
                    plan=plan,
                    previous_state=state,
                    normalized_input=_normalized_event(
                        state, "EVALUATION_STARTED", candidate_head=candidate),
                    loop_id=plan["loop_id"],
                    cycle_index=cycle_index,
                )
                state = started["tick_result"]["next_state"]
                result["evaluations_started"] += 1
                outcome = evaluation_adapter(candidate, started["tick_result"])
                if not isinstance(outcome, dict):
                    raise P5D4RuntimeError("evaluation adapter result invalid")
                classification = outcome.get("outcome")
                failure_code = outcome.get("failure_code")
                if classification == "QUALIFIED":
                    finished = persist_tick(
                        control_root=root, plan=plan, previous_state=state,
                        normalized_input=_normalized_event(
                            state, "EVALUATION_PASSED", candidate_head=candidate),
                        loop_id=plan["loop_id"], cycle_index=cycle_index)
                    state = finished["tick_result"]["next_state"]
                    result["terminal_reason"] = "PROMOTION_AUTHORITY_REQUIRED"
                elif classification == "REJECTED":
                    if not isinstance(failure_code, str) or not failure_code:
                        raise P5D4RuntimeError("rejected evaluation requires failure code")
                    finished = persist_tick(
                        control_root=root, plan=plan, previous_state=state,
                        normalized_input=_normalized_event(
                            state, "EVALUATION_FAILED",
                            candidate_head=candidate, failure_code=failure_code),
                        loop_id=plan["loop_id"], cycle_index=cycle_index)
                    state = finished["tick_result"]["next_state"]
                    result["terminal_reason"] = "BLOCKED_REQUIRES_ADJUDICATION"
                elif classification == "BLOCKED":
                    result["terminal_reason"] = "BLOCKED_REQUIRES_ADJUDICATION"
                else:
                    raise P5D4RuntimeError("evaluation outcome invalid")
                continue

            if result["remote_observations"] >= plan["max_remote_observations"]:
                result["terminal_reason"] = "BOUND_REACHED"
                break
            event = observation_adapter(state)
            result["remote_observations"] += 1
            observed = persist_tick(
                control_root=root,
                plan=plan,
                previous_state=state,
                normalized_input=event,
                loop_id=plan["loop_id"],
                cycle_index=cycle_index,
            )
            state = observed["tick_result"]["next_state"]
            if event.get("event_type") == "REMOTE_OBSERVATION_FAILED":
                result["consecutive_failures"] += 1
                if result["consecutive_failures"] > plan["max_consecutive_failures"]:
                    result["terminal_reason"] = "BOUND_REACHED"
                    break
            else:
                result["consecutive_failures"] = 0

            if state["observer_phase"] == "BLOCKED":
                result["terminal_reason"] = "BLOCKED_REQUIRES_ADJUDICATION"
                break
            if (
                observed["tick_result"]["decision"]["action"] == "NOOP"
                and not state["pending_heads"]
            ):
                result["terminal_reason"] = "NO_PENDING_WORK"
                break

        if result["terminal_reason"] is None:
            result["terminal_reason"] = "BOUND_REACHED"
        result["observer_state"] = state
        _write_run_result(root, result)
        return result
    except QueueCapacityError:
        result["terminal_reason"] = "QUEUE_CAPACITY_REQUIRES_ADJUDICATION"
        result["observer_state"] = state
        _write_run_result(root, result)
        return result
    except ReconciliationError:
        result["terminal_reason"] = "RECONCILIATION_REQUIRED"
        result["observer_state"] = state
        _write_run_result(root, result)
        return result
    except Exception:
        result["terminal_reason"] = "FATAL_INCONSISTENCY"
        result["observer_state"] = state
        _write_run_result(root, result)
        return result
    finally:
        release_ownership(root, ownership)

~~~~

# SOURCE: P5-D4 BOUNDED LOOP RUNTIME TESTS

Path: tests/obsidian_projection/test_p5d4_bounded_observer_loop_runtime_v0_1.py
~~~~
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.obsidian_projection.observer_tick import INPUT_SCHEMA, make_initial_state

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_PATH = ROOT / "tools" / "obsidian_projection" / "p5d4_bounded_observer_loop.py"
PREREG_REL = "tools/obsidian_projection/p5d4_bounded_observer_loop_runtime_preregistration_v0_1.json"
PREREG_BLOB = "7645a96ae8b9b827a78c3313127219023dd2c7ac"
HEAD_A, HEAD_B = "1" * 40, "2" * 40
SHA_A, SHA_B, SHA_C = "a" * 64, "b" * 64, "c" * 64

def _git_blob(relative):
    return subprocess.run(["git","rev-parse",f"HEAD:{relative}"],cwd=str(ROOT),
        check=True,text=True,capture_output=True).stdout.strip()

def _event(state, event_type, observed=None, transition=None, candidate=None, failure=None):
    return {"schema":INPUT_SCHEMA,"event_type":event_type,
        "sequence":state["last_event_sequence"]+1,"observed_head":observed,
        "transition_class":transition,"candidate_head":candidate,"failure_code":failure}

def _evidence(head=HEAD_A):
    return {"schema":"ATDS_OBSIDIAN_P5D4_VERIFIED_PUBLICATION_EVIDENCE_V0_1",
        "candidate_head":head,"status":"PASS_LIVE_PUBLICATION_CONFIRMED",
        "transaction_plan_digest_sha256":SHA_C,"physical_receipt_digest_sha256":SHA_A,
        "logical_receipt_digest_sha256":SHA_B,"p5d2_promotion_confirmed_emitted":True}
class P5D4RuntimeV01Tests(unittest.TestCase):
    def _runtime(self):
        self.assertTrue(RUNTIME_PATH.exists(), "RED: P5-D4 runtime candidate does not exist yet")
        spec = importlib.util.spec_from_file_location(
            "tools.obsidian_projection.p5d4_bounded_observer_loop", RUNTIME_PATH)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _plan(self, rt, **overrides):
        values = dict(loop_id="synthetic-loop-01", max_cycles=4,
            max_remote_observations=4, max_evaluations=2,
            max_pending_heads=2, max_consecutive_failures=1)
        values.update(overrides)
        return rt.make_loop_plan(**values)

    def test_00_preregistration_blob_is_exact(self):
        self.assertEqual(_git_blob(PREREG_REL), PREREG_BLOB)

    def test_01_runtime_surface_and_api(self):
        rt = self._runtime()
        for name in ("make_loop_plan","validate_loop_plan","acquire_ownership",
            "release_ownership","load_event_log","load_checkpoint",
            "reconcile_control_state","reconstruct_from_verified_publication_evidence",
            "persist_tick","run_bounded_loop"):
            self.assertTrue(callable(getattr(rt,name,None)), name)

    def test_02_loop_plan_is_digest_bound_and_strict(self):
        rt = self._runtime()
        first, second = self._plan(rt), self._plan(rt)
        self.assertEqual(first, second)
        self.assertRegex(first["plan_digest_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(rt.validate_loop_plan(first), first)
        for field,value in (("max_cycles",0),("max_pending_heads",0),
            ("max_evaluations",-1),("max_cycles",True)):
            with self.assertRaises(rt.LoopPlanError):
                self._plan(rt, **{field:value})
    def test_03_ownership_exclusive_and_no_auto_steal(self):
        rt = self._runtime()
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            owner=rt.acquire_ownership(root,loop_id="a",owner_token="one")
            with self.assertRaises(rt.OwnershipContended):
                rt.acquire_ownership(root,loop_id="b",owner_token="two")
            wrong=dict(owner); wrong["owner_token"]="wrong"
            with self.assertRaises(rt.OwnershipError):
                rt.release_ownership(root,wrong)
            self.assertTrue((root/"ownership.lock").exists())
            rt.release_ownership(root,owner)
            self.assertFalse((root/"ownership.lock").exists())

    def test_04_persist_tick_event_then_checkpoint(self):
        rt=self._runtime()
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); plan=self._plan(rt); state=make_initial_state()
            result=rt.persist_tick(control_root=root,plan=plan,previous_state=state,
                normalized_input=_event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"),
                loop_id=plan["loop_id"],cycle_index=1)
            log=rt.load_event_log(root); cp=rt.load_checkpoint(root)
            self.assertEqual(len(log),1)
            self.assertIsNone(log[0]["previous_record_digest_sha256"])
            self.assertEqual(cp["last_event_digest_sha256"],log[0]["record_digest_sha256"])
            self.assertEqual(cp["observer_state"],result["tick_result"]["next_state"])

    def test_05_crash_window_replays_exactly_one_event(self):
        rt=self._runtime()
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); plan=self._plan(rt); state=make_initial_state()
            def fault(point):
                if point=="AFTER_EVENT_DURABLE_BEFORE_CHECKPOINT_REPLACE":
                    raise RuntimeError("synthetic crash")
            with self.assertRaises(RuntimeError):
                rt.persist_tick(control_root=root,plan=plan,previous_state=state,
                    normalized_input=_event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"),
                    loop_id=plan["loop_id"],cycle_index=1,fault_injector=fault)
            self.assertIsNone(rt.load_checkpoint(root))
            rec=rt.reconcile_control_state(control_root=root,plan=plan,
                verified_current_head=None,promotion_evidence=None)
            self.assertEqual(rec["status"],"PASS_RECONCILED_ONE_RECORD_AHEAD")
            self.assertEqual(rec["observer_state"]["last_event_sequence"],1)
    def test_06_checkpoint_or_log_corruption_fails_closed(self):
        rt=self._runtime()
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); plan=self._plan(rt); state=make_initial_state()
            rt.persist_tick(control_root=root,plan=plan,previous_state=state,
                normalized_input=_event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"),
                loop_id=plan["loop_id"],cycle_index=1)
            (root/"observer-events.jsonl").write_bytes(b"")
            with self.assertRaises(rt.ReconciliationError):
                rt.reconcile_control_state(control_root=root,plan=plan,
                    verified_current_head=None,promotion_evidence=None)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); plan=self._plan(rt); state=make_initial_state()
            rt.persist_tick(control_root=root,plan=plan,previous_state=state,
                normalized_input=_event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"),
                loop_id=plan["loop_id"],cycle_index=1)
            p=root/"observer-checkpoint.json"; value=json.loads(p.read_text())
            value["observer_state_digest_sha256"]=SHA_A
            p.write_text(json.dumps(value,sort_keys=True,separators=(",",":"))+"\n",encoding="utf-8")
            with self.assertRaises(rt.PersistenceError):
                rt.load_checkpoint(root)

    def test_07_queue_capacity_blocks_before_tick(self):
        rt=self._runtime(); plan=self._plan(rt,max_pending_heads=1)
        state=make_initial_state()
        state=rt.persist_tick
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); initial=make_initial_state()
            first=rt.persist_tick(control_root=root,plan=plan,previous_state=initial,
                normalized_input=_event(initial,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"),
                loop_id=plan["loop_id"],cycle_index=1)
            queued=first["tick_result"]["next_state"]
            with self.assertRaises(rt.QueueCapacityError):
                rt.persist_tick(control_root=root,plan=plan,previous_state=queued,
                    normalized_input=_event(queued,"REMOTE_HEAD_OBSERVED",HEAD_B,"FAST_FORWARD"),
                    loop_id=plan["loop_id"],cycle_index=2)
            self.assertEqual(len(rt.load_event_log(root)),1)
    def test_08_existing_current_reconstructs_via_four_evidence_events(self):
        rt=self._runtime(); plan=self._plan(rt)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            result=rt.reconstruct_from_verified_publication_evidence(
                control_root=root,plan=plan,verified_current_head=HEAD_A,
                promotion_evidence=_evidence())
            state=result["observer_state"]; log=rt.load_event_log(root)
            self.assertEqual(state["projection_state"],"CURRENT")
            self.assertEqual(state["live_projection_head"],HEAD_A)
            self.assertEqual(len(log),4)
            self.assertEqual([x["normalized_input"]["event_type"] for x in log],
                ["REMOTE_HEAD_OBSERVED","EVALUATION_STARTED",
                 "EVALUATION_PASSED","PROMOTION_CONFIRMED"])
            self.assertTrue(all(x["record_origin"]=="EVIDENCE_RECONSTRUCTION" for x in log))
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(rt.ReconciliationError):
                rt.reconstruct_from_verified_publication_evidence(
                    control_root=Path(td),plan=plan,verified_current_head=HEAD_A,
                    promotion_evidence=None)

    def test_09_two_cycles_qualify_then_stop_for_promotion_authority(self):
        rt=self._runtime(); plan=self._plan(rt,max_cycles=2); calls={"obs":0,"eval":0}
        def observe(state):
            calls["obs"]+=1
            return _event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL")
        def evaluate(candidate,activation):
            calls["eval"]+=1
            self.assertEqual(candidate,HEAD_A)
            self.assertEqual(activation["decision"]["action"],"START_EXACT_HEAD_EVALUATION")
            return {"outcome":"QUALIFIED","failure_code":None}
        with tempfile.TemporaryDirectory() as td:
            report=rt.run_bounded_loop(plan=plan,control_root=Path(td),
                observation_adapter=observe,evaluation_adapter=evaluate,
                verified_current_head=None,promotion_evidence=None,
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["terminal_reason"],"PROMOTION_AUTHORITY_REQUIRED")
            self.assertEqual(report["cycles_started"],2)
            self.assertEqual(report["evaluations_started"],1)
            self.assertFalse(report["automatic_promotion_authorized"])
            self.assertEqual(calls,{"obs":1,"eval":1})
    def test_10_same_current_is_noop_without_evaluation(self):
        rt=self._runtime(); plan=self._plan(rt); calls={"eval":0}
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            rt.reconstruct_from_verified_publication_evidence(
                control_root=root,plan=plan,verified_current_head=HEAD_A,
                promotion_evidence=_evidence())
            def observe(state):
                return _event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"SAME")
            def evaluate(*args):
                calls["eval"]+=1
                raise AssertionError("SAME must not evaluate")
            report=rt.run_bounded_loop(plan=plan,control_root=root,
                observation_adapter=observe,evaluation_adapter=evaluate,
                verified_current_head=HEAD_A,promotion_evidence=_evidence(),
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["terminal_reason"],"NO_PENDING_WORK")
            self.assertEqual(report["observer_state"]["projection_state"],"CURRENT")
            self.assertEqual(calls["eval"],0)

    def test_11_non_fast_forward_blocks_without_evaluation(self):
        rt=self._runtime(); plan=self._plan(rt)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            rt.reconstruct_from_verified_publication_evidence(
                control_root=root,plan=plan,verified_current_head=HEAD_A,
                promotion_evidence=_evidence())
            def observe(state):
                return _event(state,"REMOTE_HEAD_OBSERVED",HEAD_B,"NON_FAST_FORWARD")
            report=rt.run_bounded_loop(plan=plan,control_root=root,
                observation_adapter=observe,
                evaluation_adapter=lambda *_: (_ for _ in ()).throw(AssertionError()),
                verified_current_head=HEAD_A,promotion_evidence=_evidence(),
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["terminal_reason"],"BLOCKED_REQUIRES_ADJUDICATION")
            self.assertEqual(report["observer_state"]["observer_phase"],"BLOCKED")
    def test_12_rejected_and_blocked_evaluation_remain_distinct(self):
        rt=self._runtime(); plan=self._plan(rt,max_cycles=2)
        def observe(state):
            return _event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL")
        with tempfile.TemporaryDirectory() as td:
            report=rt.run_bounded_loop(plan=plan,control_root=Path(td),
                observation_adapter=observe,
                evaluation_adapter=lambda *_:{"outcome":"REJECTED","failure_code":"BREAK"},
                verified_current_head=None,promotion_evidence=None,
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["observer_state"]["observer_phase"],"BLOCKED")
            self.assertEqual(report["observer_state"]["last_failure_code"],"BREAK")
        with tempfile.TemporaryDirectory() as td:
            report=rt.run_bounded_loop(plan=plan,control_root=Path(td),
                observation_adapter=observe,
                evaluation_adapter=lambda *_:{"outcome":"BLOCKED","failure_code":"INFRA"},
                verified_current_head=None,promotion_evidence=None,
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["terminal_reason"],"BLOCKED_REQUIRES_ADJUDICATION")
            self.assertEqual(report["observer_state"]["observer_phase"],"EVALUATING")

    def test_13_cycle_and_evaluation_budgets_are_hard_bounds(self):
        rt=self._runtime(); plan=self._plan(rt,max_cycles=1)
        calls={"obs":0,"eval":0}
        def observe(state):
            calls["obs"]+=1
            return _event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL")
        with tempfile.TemporaryDirectory() as td:
            report=rt.run_bounded_loop(plan=plan,control_root=Path(td),
                observation_adapter=observe,
                evaluation_adapter=lambda *_: calls.__setitem__("eval",calls["eval"]+1),
                verified_current_head=None,promotion_evidence=None,
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["terminal_reason"],"BOUND_REACHED")
            self.assertEqual(report["cycles_started"],1)
            self.assertEqual(calls,{"obs":1,"eval":0})
    def test_14_second_runner_writes_nothing(self):
        rt=self._runtime(); plan=self._plan(rt)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            owner=rt.acquire_ownership(root,loop_id="held",owner_token="held")
            before={p.relative_to(root).as_posix():p.read_bytes()
                for p in root.rglob("*") if p.is_file()}
            report=rt.run_bounded_loop(plan=plan,control_root=root,
                observation_adapter=lambda *_: (_ for _ in ()).throw(AssertionError()),
                evaluation_adapter=lambda *_: (_ for _ in ()).throw(AssertionError()),
                verified_current_head=None,promotion_evidence=None,
                forbidden_roots=(),owner_token="second")
            after={p.relative_to(root).as_posix():p.read_bytes()
                for p in root.rglob("*") if p.is_file()}
            self.assertEqual(report["terminal_reason"],"LOCK_CONTENDED")
            self.assertEqual(before,after)
            rt.release_ownership(root,owner)

    def test_15_restart_in_evaluating_never_repeats_evaluation(self):
        rt=self._runtime(); plan=self._plan(rt)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); state=make_initial_state()
            first=rt.persist_tick(control_root=root,plan=plan,previous_state=state,
                normalized_input=_event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"),
                loop_id=plan["loop_id"],cycle_index=0)
            state=first["tick_result"]["next_state"]
            rt.persist_tick(control_root=root,plan=plan,previous_state=state,
                normalized_input=_event(state,"EVALUATION_STARTED",candidate=HEAD_A),
                loop_id=plan["loop_id"],cycle_index=0)
            calls={"eval":0}
            report=rt.run_bounded_loop(plan=plan,control_root=root,
                observation_adapter=lambda *_: (_ for _ in ()).throw(AssertionError()),
                evaluation_adapter=lambda *_: calls.__setitem__("eval",calls["eval"]+1),
                verified_current_head=None,promotion_evidence=None,
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["terminal_reason"],"RECONCILIATION_REQUIRED")
            self.assertEqual(calls["eval"],0)
    def test_16_control_root_boundary_and_static_authority_surface(self):
        rt=self._runtime(); plan=self._plan(rt)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            with self.assertRaises(rt.P5D4RuntimeError):
                rt.run_bounded_loop(plan=plan,control_root=root,
                    observation_adapter=lambda *_:None,evaluation_adapter=lambda *_:None,
                    verified_current_head=None,promotion_evidence=None,
                    forbidden_roots=(root,),owner_token="owner")
        source=RUNTIME_PATH.read_text(encoding="utf-8")
        for token in ("while True","time.sleep","asyncio.sleep","Timer(","schtasks",
            "WindowsService","p5d3f_promotion_handoff","p5d3g_stageb_real_execution",
            "execute_one_real_live_publication","execute_finite_live_publication",
            "build_current_head_projection","stage_candidate_generation"):
            self.assertNotIn(token,source)
        self.assertIn("one_shot_tick",source)
        self.assertIn("make_initial_state",source)

if __name__ == "__main__":
    unittest.main()

~~~~

# SOURCE: P5-D4 HUMAN ADJUDICATION

Path: GOVERNANCE/P5-D4-REAL-BOUNDED-LOOP-REQUALIFICATION-V0.2-HUMAN-ADJUDICATION-2026-10-01.md
~~~~
# P5-D4 â€” REAL BOUNDED LOOP REQUALIFICATION V0.2

## HUMAN ADJUDICATION â€” ADOPT

Date: 2026-10-01

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branch: `feat/obsidian-projection-p5d4-control-root-binding-remediation-v0.1`

Human decision supplied in conversation:

```text
P5D4_REAL_REQUALIFICATION_V0_2 = HUMAN_ADOPTED
```

This record persists the human decision. It is not represented as independent cryptographic proof of human identity.

## 1. Persistence base

Fresh-verified immediately before persistence:

```text
PRE_PERSISTENCE_HEAD =
bc70768d0966fed15af9ebd653bf9ff255df3095

PRE_PERSISTENCE_REMOTE_HEAD =
bc70768d0966fed15af9ebd653bf9ff255df3095

WORKTREE =
CLEAN
```

Qualification artifact:

`reports/program/2026-10-01-OBSIDIAN-P5D4-REAL-BOUNDED-LOOP-REQUALIFICATION-V0.2.md`

Qualification artifact blob:

`660a679532d1bb122b0df382230d4d249a0cac1f`

Qualified P5-D4 runtime blob:

`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

## 2. Human adjudication

The human adopts the persisted P5-D4 V0.2 qualification within the surface actually tested.

```text
P5-D4 REAL BOUNDED LOOP REQUALIFICATION V0.2
= HUMAN_ADOPTED

QUALIFICATION_SCOPE
= ACTUALLY_TESTED_SURFACE_ONLY
```

This adoption does not convert a scoped PASS into a claim that no material failure exists outside the tested surface.

## 3. Preserved pending state

The observed source HEAD remains:

`1d4c2f3d657b36ecaa6ab25b967e46b3620190d1`

Its governed state remains:

```text
PENDING_HEAD
= QUEUED

EVALUATED
= FALSE

PROMOTED
= FALSE

PUBLISHED
= FALSE
```

No authority to evaluate, promote, or publish that HEAD is created by this adjudication.

## 4. Explicit non-authorizations

This human adoption does not authorize:

```text
PENDING_HEAD_EVALUATION = FALSE
PROMOTION = FALSE
PUBLICATION = FALSE
P5-E = CLOSED
P6 = CLOSED
STAGE_A = CLOSED
STAGE_B = CLOSED
REAL_VAULT_MUTATION = FALSE
CURRENT_MUTATION = FALSE
CURRENT_TMP_MUTATION = FALSE
DAEMON = FALSE
PERIODIC_POLLING = FALSE
SCHEDULED_TASK = FALSE
WINDOWS_SERVICE = FALSE
```

## 5. Authority boundary

This decision changes only the governance status of the already-qualified P5-D4 V0.2 result.

It does not modify:

- the P5-D4 runtime;
- P5-D2 observer semantics;
- the live Vault;
- `CURRENT.md`;
- `CURRENT.tmp`;
- the queued HEAD;
- any evaluation or publication state.

Any subsequent frontier requires separate human authorization.

## 6. Adopted state

```text
P5D4_REAL_REQUALIFICATION_V0_2
= HUMAN_ADOPTED

P5D4_REAL_BOUNDED_LOOP
= QUALIFIED_AND_HUMAN_ADOPTED

PENDING_SOURCE_HEAD
= 1d4c2f3d657b36ecaa6ab25b967e46b3620190d1

PENDING_SOURCE_HEAD_STATUS
= QUEUED_NOT_EVALUATED

P5-E
= CLOSED

P6
= CLOSED
```

## 7. Stop boundary

After persistence and post-persistence verification:

```text
NEW_RUNTIME_EXECUTION
= NOT_AUTHORIZED

PENDING_HEAD_EVALUATION
= NOT_AUTHORIZED

P5-E_OPENING
= NOT_AUTHORIZED

P6_OPENING
= NOT_AUTHORIZED

STOP
= TRUE
```

~~~~

# SOURCE: BB1 RED EVIDENCE

Path: reports/program/2026-10-02-OBSIDIAN-P5E-BB1-NORMATIVE-GUARD-RED-EVIDENCE.md
~~~~
# P5-E V0.1 â€” BB1 NORMATIVE GUARD COVERAGE â€” RED EVIDENCE

Date: 2026-10-02

## Scope

First RED execution after persistence of BB1 internal adjudication and preregistration.

Preregistration HEAD:
`64eb3b5aea96d2d8bb36114737c19489862f85f4`

Adjudication blob:
`32741174bd2ad845af4dbbfb664c38d887e181e9`

Preregistration blob:
`0f12b589fe1b74320732fb531936bf6e843653d9`

## RED test artifact

`tests/obsidian_projection/test_p5e_bb1_normative_guard_closure_v0_1.py`

The test was created before any contract/model/matrix correction.
## Command

```text
python -B -m unittest tests.obsidian_projection.test_p5e_bb1_normative_guard_closure_v0_1
```

## Observed result

```text
Ran 10 tests in 0.050s

FAILED (failures=6, errors=3)

RED_EXIT=1
```

One test passed:
- preregistration freezes the exact 23 normative and 13 non-normative leaf sets.

Nine tests were red as expected.
## RED families demonstrated

1. All 23 preregistered normative leaf mutations still survive the invariant checker.
2. The combined BB1 regression is still accepted.
3. Evidence matrix has no exact contract/model blob binding.
4. NB1 read overrun currently returns PASS instead of fail-closed.
5. NB4 future-adapter-rule fields are absent.
6. NB6 queue-capacity mappings point to declarative P5-E mutation tests rather than behavioral P5-D4 evidence.
7. NB6 pending non-active semantics are mapped to an active-evaluation test.
8. NB7 explicit `INCOMPLETE_SYNTHETIC_WINDOW` non-pass declaration is absent.
9. NB7 duplicate fixed-rate slot still returns `CADENCE_GAP`.

## Authority

No real P5-E execution occurred.

No P5-D4 runtime or real control state was modified.

`REAL_P5E = CLOSED`

~~~~

# SOURCE: BB1 GREEN EVIDENCE

Path: reports/program/2026-10-02-OBSIDIAN-P5E-BB1-NORMATIVE-GUARD-GREEN-EVIDENCE.md
~~~~
# P5-E V0.1 â€” BB1 NORMATIVE GUARD COVERAGE â€” GREEN EVIDENCE

Date: 2026-10-02

## Scope

Minimal closure of:
- BB1 normative guard coverage;
- NB1 fixed-rate read overrun;
- NB4 claim scope;
- NB6 evidence mapping;
- NB7 non-pass / duplicate-slot semantics.

RED predecessor:
`e9b5f1664d2fd215fe77edbecbb24f24c306e2c3`

No real P5-E execution occurred.

## Corrected prospective identities

Contract:
`7e3e18ba946246065b43bc5fbabdc35980140eb9`

Model:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`
Evidence matrix:
`88e13a447a96455d4ac1d9d0f96e11b29329616d`

Observer-tick behavioral tests:
`f5b4bca7524f74f221927d1ec389e23d607d1eee`

P5-E adversarial tests:
`16b6fdb9c0bb5be980e5db59eb6f87f93e160205`

Matrix tests:
`182a7b60b440ddb8d5c0c9fdc65f423309383244`

BB1 closure tests remain:
`ed4a2c3d9c67f2d67d32b632bfa5c25d36cd0880`

P5-D4 runtime remains:
`1825e53d195ba2a63b5b646a5b78eb77939b94b5`
## BB1 guard closure

The original 23 normative survivor leaves are now rejected by strict invariant checks.

The combined BB1 regression is rejected.

Newly introduced NB1/NB4/NB7 normative fields are also strictly guarded.

## Matrix object binding

The evidence matrix now binds:
- exact contract blob;
- exact model blob.

`covered_object_drift_must_fail = true`

The matrix test recomputes Git object identity using `git hash-object --path` and fails on drift.

## NB1

A terminal read extending beyond its next required fixed-rate slot now returns:

```text
BLOCKED_REQUIRES_ADJUDICATION
ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT
```
Existing multi-observation overlap semantics remain separately testable.

## NB4

The contract now distinguishes:
- future adapter non-injection rule = true;
- current runtime-qualified non-injection property = false.

No adapter/runtime authority was introduced.

## NB6

Queue-capacity replacement/coalescing mappings now reuse:
`P5D4RuntimeV01Tests.test_07_queue_capacity_blocks_before_tick`

Pending non-active FIFO/no-retarget semantics now use a dedicated D2 behavioral test:
`ObserverTickTests.test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation`

No D2 runtime modification occurred.

## NB7

`INCOMPLETE_SYNTHETIC_WINDOW` is explicitly NON-PASS.

Duplicate fixed-rate slots now return:
`DUPLICATE_FIXED_RATE_SLOT`
instead of `CADENCE_GAP`.
## Targeted green execution

Covered:
- BB1 closure tests;
- P5-E contract tests;
- P5-E adversarial tests;
- prior B1â†’B5 closure tests;
- evidence-matrix tests;
- D2 observer-tick behavioral tests;
- P5-D4 bounded-loop runtime tests.

Observed:
```text
Ran 133 tests in 2.625s
OK
```

## Mutation-sweep exit criterion

Post-correction full P5-E surface baseline:
```text
51 tests
0 failures
0 errors
```

Every contract leaf was then independently mutated in a temporary copy.
Observed:
```text
FULL50_LEAF_MUTATIONS_TOTAL = 161
FULL50_SURVIVORS = 0
```

Therefore:
`NORMATIVE_LEAF_MUTATIONS_SURVIVING = 0`

This satisfies the preregistered BB1 exit criterion.

## Current boundary

```text
BB1_TARGETED_GREEN = PASS
TARGETED_PREDECESSOR_REGRESSION = NEXT
FULL_SUITE = NOT_YET_RUN
REAL_P5E = CLOSED
HUMAN_NORMATIVE_ADOPTION = CLOSED
```

~~~~

# SOURCE: BB1 TARGETED PREDECESSOR REGRESSION

Path: reports/program/2026-10-02-OBSIDIAN-P5E-BB1-TARGETED-PREDECESSOR-REGRESSION.md
~~~~
# P5-E V0.1 â€” BB1 TARGETED PREDECESSOR REGRESSION

Date: 2026-10-02

## Execution identity

Branch:
`feat/obsidian-projection-p5e-v0.1-bb1-normative-guard-closure`

HEAD:
`e276962b9e5c89e32c75fc35e16fb07b200d06ee`

P5-D4 runtime blob:
`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

## Covered surfaces

- P5-A continuous projection contract;
- P5-D1 continuous observer core;
- P5-D2 one-shot observer contract and behavioral runtime tests;
- P5-D4 bounded-loop contract/runtime/adversarial/control-root remediation;
- P5-E contract, adversarial, B1â†’B5 closure, evidence matrix;
- BB1 normative-guard closure.
## Result

```text
Ran 282 tests in 5.356s

OK

TARGETED_REGRESSION_EXIT=0
```

Historical subprocess tests emitted three non-failing `ResourceWarning` messages for unclosed text streams.

Cross-interpreter tests generated three Python 3.14 bytecode-cache files.

Those cache files are runtime residue only and are removed before persistence.

## Verdict

```text
TARGETED_PREDECESSOR_REGRESSION = 282 / 282 PASS
P5D4_RUNTIME = UNCHANGED
REAL_P5E = CLOSED
```

The next preregistered step is exactly one full Obsidian suite in a disposable clone.

~~~~

# SOURCE: BB1 FULL OBSIDIAN REBREAK

Path: reports/program/2026-10-02-OBSIDIAN-P5E-BB1-FULL-OBSIDIAN-REBREAK.md
~~~~
# P5-E V0.1 â€” BB1 FULL OBSIDIAN RE-BREAK

Date: 2026-10-02

## Scope

This is the single full Obsidian suite authorized by:
`P5-E V0.1 â€” BB1 NORMATIVE GUARD COVERAGE CLOSURE`

Full-suite budget:
`1 / 1 CONSUMED`

The run was executed in a disposable clone, not in the canonical working tree.

## Exact executable identity

Branch:
`feat/obsidian-projection-p5e-v0.1-bb1-normative-guard-closure`

HEAD:
`647edf62723fa84c7260c0ea3b25c074f180604f`
Contract blob:
`7e3e18ba946246065b43bc5fbabdc35980140eb9`

Model blob:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`

Evidence matrix blob:
`88e13a447a96455d4ac1d9d0f96e11b29329616d`

P5-D4 runtime blob:
`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

Disposable clone path during execution:
`C:\Users\Boulevart\ATDS-TMP\P5E-BB1-FULL-647edf62723f`

The clone HEAD matched the governed HEAD before execution.
## Real P5-D4 fingerprint before full suite

```text
observer-events.jsonl
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

observer-checkpoint.json
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

## Command

```text
python -B -m unittest discover -s tests/obsidian_projection -p 'test_*.py'
```
## Result

```text
Ran 1486 tests in 245.601s

OK

FULL_EXIT=0
FULL_SECONDS=247.637
```

The disposable clone reported three post-run worktree residues.

They were not enumerated before clone deletion, so no stronger claim is made about their exact filenames.

The disposable clone was removed after the run.

## Real P5-D4 fingerprint after full suite

```text
observer-events.jsonl
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af
observer-checkpoint.json
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

Therefore:
`REAL_P5D4_STATE_CHANGED = FALSE`

Canonical repository status after clone deletion:
`CLEAN`

## Non-failing observations

The run emitted:
- the existing sample-worktree LF/CRLF warning;
- historical `ResourceWarning` messages for unclosed subprocess text streams.

Neither changed the unittest verdict.

## Verdict

```text
FULL_OBSIDIAN_REBREAK = 1486 / 1486 PASS
DISPOSABLE_CLONE = USED_AND_REMOVED
REAL_P5D4_FINGERPRINT = UNCHANGED
REAL_P5E = CLOSED
```

~~~~

# SOURCE: BB1 QUALIFICATION

Path: reports/program/2026-10-02-OBSIDIAN-P5E-BB1-NORMATIVE-GUARD-QUALIFICATION.md
~~~~
# P5-E V0.1 â€” BB1 NORMATIVE GUARD COVERAGE â€” QUALIFICATION

Date: 2026-10-02

## Qualification verdict

```text
BB1_LOCAL_REPRODUCTION = COMPLETE
BB1_INTERNAL_ADJUDICATION = COMPLETE
BB1_PREREGISTRATION = PASS
BB1_RED = PASS
BB1_TARGETED_GREEN = PASS
NORMATIVE_MUTATION_EXIT = PASS
TARGETED_PREDECESSOR_REGRESSION = PASS
FULL_OBSIDIAN_REBREAK = PASS

BB1_NORMATIVE_GUARD_CLOSURE_CANDIDATE
= QUALIFIED_FOR_EXTERNAL_REREVIEW

EXTERNAL_REREVIEW
= PENDING

HUMAN_NORMATIVE_ADOPTION
= CLOSED_PENDING_REREVIEW

REAL_P5E
= CLOSED
```
## Evidence chain

Internal adjudication blob:
`32741174bd2ad845af4dbbfb664c38d887e181e9`

Preregistration blob:
`0f12b589fe1b74320732fb531936bf6e843653d9`

RED evidence blob:
`7ebe7bcdba7db8beaf06fc1480a7ce5cb512714a`

BB1 closure test blob:
`ed4a2c3d9c67f2d67d32b632bfa5c25d36cd0880`

GREEN evidence blob:
`4681d7cc42f5513b9274f1b814f6996633ac4a9d`

Targeted predecessor regression blob:
`fc04dbe0e560aa00b89f4b3840cdbcdef20ea564`
## Corrected candidate identity

Contract:
`7e3e18ba946246065b43bc5fbabdc35980140eb9`

Synthetic model:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`

Evidence matrix:
`88e13a447a96455d4ac1d9d0f96e11b29329616d`

Observer-tick behavioral test:
`f5b4bca7524f74f221927d1ec389e23d607d1eee`

P5-E adversarial test:
`16b6fdb9c0bb5be980e5db59eb6f87f93e160205`

Evidence-matrix test:
`182a7b60b440ddb8d5c0c9fdc65f423309383244`

P5-D4 runtime remains:
`1825e53d195ba2a63b5b646a5b78eb77939b94b5`
## BB1 closure

The external blocker was reproduced locally before correction.

Before correction:
```text
BASELINE = 50 / 50 PASS
BB1 COMBINED REGRESSION = 50 / 50 PASS
154 contract leaf mutations
36 survived the complete P5-E targeted surface
23 were adjudicated normative survivors
```

After correction:
- all original 23 normative survivor leaves are strictly guarded;
- newly introduced closure fields are also strictly guarded;
- the evidence matrix binds the exact contract and model blobs;
- a contract or model object drift invalidates the matrix.

## Mutation-sweep exit

Post-correction P5-E targeted surface:
```text
BASELINE = 51 / 51 PASS
CONTRACT LEAF MUTATIONS = 161
SURVIVING MUTATIONS = 0
NORMATIVE_LEAF_MUTATIONS_SURVIVING = 0
```
This exceeds the preregistered minimum exit criterion.

## NB1 closure

A terminal remote read that crosses the next required fixed-rate slot now fails closed:

```text
BLOCKED_REQUIRES_ADJUDICATION
ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT
```

Existing multi-observation overlap semantics remain separately represented.

## NB4 closure

The candidate now distinguishes:
- non-injection of an unobserved intermediate tip as a future adapter rule;
- current runtime qualification of that property as false.

No future adapter behavior is claimed as already implemented.
## NB6 closure

Queue-capacity replacement/coalescing requirements now map to the behavioral P5-D4 capacity test.

Pending non-active FIFO/no-retarget semantics now map to a dedicated D2 behavioral test.

No D2 or P5-D4 runtime code was modified.

## NB7 closure

`INCOMPLETE_SYNTHETIC_WINDOW` is explicitly declared NON-PASS.

Duplicate fixed-rate slots return:
`DUPLICATE_FIXED_RATE_SLOT`

The theoretical dynamic-builtin AST bypass remains outside scope because no defect in the current model was demonstrated.

## Regression evidence

Targeted predecessor regression:
`282 / 282 PASS`

Full disposable-clone Obsidian suite:
`1486 / 1486 PASS`
## Evidence discipline improvement

The full suite was executed in a disposable clone of exact HEAD:
`647edf62723fa84c7260c0ea3b25c074f180604f`

Real P5-D4 control-state SHA-256 fingerprints were captured before and after.

All three were byte-identical.

The disposable clone was removed.

## Deferred findings preserved

Not resolved by this closure:
- NB2;
- NB3;
- NB5;
- NB9.

They remain future prerequisites for real observation / ancestry-classifier / real P5-E preregistration.

## Maximum current claim

`P5E_V0_1_BB1_NORMATIVE_GUARD_CLOSURE_CANDIDATE_QUALIFIED_FOR_EXTERNAL_REREVIEW`
Explicitly not qualified:
- real P5-E end-to-end synchronization;
- continuous synchronization;
- real 60-second SLA;
- per-transient-tip detection SLA;
- automatic evaluation;
- automatic promotion;
- automatic publication;
- real observation adapter semantics;
- ancestry-classifier correctness.

## Mandatory next gate

A new independent external adversarial re-review is required.

That review creates no authority.

Human normative adjudication remains closed until after that review.

```text
EXTERNAL_REREVIEW = NEXT
REAL_P5E = CLOSED
P6 = CLOSED
STOP = TRUE
```

~~~~
