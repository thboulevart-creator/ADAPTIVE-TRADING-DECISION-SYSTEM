VERDICT = FAIL

J'ai reconstruit localement les 17 artefacts code et JSON du paquet. Toutes les identités de blob annoncées correspondent (contrat `b0668b4…`, modèle `b783717…`, tests `a4fbd35…`, `3c0f556…`, `15c3e44…`, `ff9db4c…`, matrice `0440175…`, ainsi que D2 `fd212f6…`/`9c472a3…` et D4 `1825e53…`/`5bcc563…`). La surface P5-E ciblée tourne à 50/50 OK et D2 à 54/54 OK. D4 runtime passe 16/17 avec un `USERPROFILE` simulé ; `test_00` échoue seulement parce que la préregistration D4 n'est pas embarquée (cause environnementale). Les 23 tests distincts référencés par la matrice passent tous.

Le FAIL repose sur un seul défaut bloquant. Il est démontré, il porte sur un critère préregistré, et sa correction est mécanique.

### BLOCKING_FINDINGS

**BB1 — La clôture B1 est incomplète : on peut réintroduire exactement le défaut B4 sans qu'aucun des 50 tests ne casse.** (OBSERVÉ)

*Où :*

- « TARGETED CLOSURE PREREGISTRATION », `coverage_closure.adversarial_invariants_must_cover_all_normative_contract_blocks: true` ;
- « CORRECTED P5-E ADVERSARIAL TESTS », `assert_contract_invariants` ;
- « CORRECTED P5-E BASE TESTS », `test_real_latency_metric_is_falsifiable_and_local_monotonic` ;
- « TARGETED CLOSURE QUALIFICATION », §B1 (« The former P5-E invariant gaps were closed », bloc « timing » déclaré gardé).

*Falsification minimale.* J'applique simultanément les mutations suivantes au contrat :

- `near_real_time_timing.detection_latency_definition` revient à l'ancienne valeur `FIRST_SUCCESSFUL_EXACT_REMOTE_HEAD_OBSERVATION_TIME_MINUS_SOURCE_HEAD_AVAILABLE_TIME` ;
- `future_real_bound_clock = "WALL_CLOCK"` ;
- `future_real_wall_clock_may_be_recorded_as_evidence_only = false` ;
- `latency_bound_breach_must_not_be_reported_as_near_real_time_pass = false` ;
- `monitored_source.branch = "main"` ;
- `burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification = false`.

Résultat : `Ran 50 tests … OK`.

*Balayage exhaustif.* J'ai muté chaque feuille du contrat une par une (inversion de booléen, entier +1, chaîne remplacée par "MUTATED", liste raccourcie), soit 154 mutations. 36 survivent. Parmi elles, des champs normatifs :

- `monitored_source.{remote, branch, canonical_authority, local_working_tree_is_not_authority}` ;
- `near_real_time_timing.{detection_latency_definition, future_real_bound_clock, future_real_wall_clock_may_be_recorded_as_evidence_only, latency_bound_breach_must_not_be_reported_as_near_real_time_pass}` ;
- `head_transition_policy.{initial_head…, fast_forward_head…}_under_existing_p5d2_semantics` ;
- `queue_and_supersession.burst_catch_up_claim_forbidden…` ;
- `end_to_end_definition.{real_end_to_end_stages, real_end_to_end_pass_requires_all_authorized_applicable_stages}` ;
- `real_context_evidence_only.{must_not_be_used_as_real_experiment_execution, must_not_be_mutated_by_contract_qualification}` ;
- `tip_visibility_semantics.future_ancestry_enumeration_requires_separate_qualification` ;
- `external_review_targeted_closure.external_rereview_required_before_human_normative_adoption`.

*Pourquoi c'est bloquant :*

- Le contrat porte aujourd'hui deux champs qui définissent la latence. Seul `real_latency_metric` est gardé ; `detection_latency_definition` ne l'est pas. Le contrat peut donc redevenir contradictoire sur l'origine de la mesure, ce qui est le cœur même de B4.
- Le breaker de clôture `REMOTE_AVAILABILITY_TIME_TREATED_AS_MEASURABLE_ORIGIN` est donc fermé seulement en partie.
- Aggravant : la matrice n'épingle ni le blob du contrat ni celui du modèle. Son test vérifie les blobs des fichiers de test, pas l'objet couvert. Une dérive du contrat n'invalide donc pas la matrice.

*Le défaut est un trou de garde, pas une valeur fausse.* Les valeurs actuelles sont correctes. Le défaut est l'absence de garde, et c'est exactement la classe de défaut que B1 devait fermer.

### NON_BLOCKING_FINDINGS

- **NB1 — Lecture qui déborde sur le créneau suivant.** (OBSERVÉ, modèle `qualify_detection`)&#x20;
  - Cas : `release=1`, `[(30, 61, OBS, A)]` donne `PASS_DETECTED_WITHIN_BOUND` avec une latence de 60. Le créneau 60 n'a jamais démarré pendant la lecture en cours.
  - Contradiction : la préregistration de clôture exige `all_required_attempt_slots_must_be_present_until_terminal_result` et `overlapping_single_writer_attempts_forbidden`.
  - Pourquoi non bloquant : la latence rapportée reste vraie.
  - Asymétrie : un échec qui déborde n'est bloqué que si un enregistrement suit (E4 donne `CADENCE_GAP`). S'il est le dernier enregistrement (E5), le résultat est `INCOMPLETE`.
  - Il faut clarifier le contrat ou le modèle.
- **NB2 — Ordre ambigu non détecté.** (OBSERVÉ)&#x20;
  - Cas : `release=1`, `[(30, B), (60, A)]` donne PASS avec une latence de 60. La tête B, qui n'est ni la cible ni la tête d'avant la libération, a été vue après la libération, puis A réapparaît.
  - Le modèle ne connaît pas la tête attendue avant libération. Il ne peut donc pas distinguer une réplique encore en retard d'un push tiers ou d'un retour arrière.
  - Ce n'est pas une impossibilité, comme l'était B3, mais une ambiguïté que le contrat classe `BLOCKED` (`unexpected_state_or_timing_ambiguity_result`).
  - À fermer avant toute préregistration réelle.
- **NB3 — `classify_tip_visibility` sans état.** (OBSERVÉ et INFÉRENCE)&#x20;
  - Le fait de contenance est une affirmation passée par l'appelant, non vérifiée par la fonction.
  - Le libellé `CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED` est rendu même si A a déjà été observée et mise en file auparavant.
  - Le cas normal « pas encore visible » (tête observée = ancêtre de la cible) tombe dans `UNRELATED_OR_UNPROVEN_REQUIRES_ADJUDICATION`.
  - La fonction n'est appelée par aucun chemin de décision, d'où le caractère non bloquant. Mais si un adaptateur futur la branchait sur la file, elle pourrait mal traiter une tête déjà en file.
- **NB4 — Une partie de la clôture B5 est déclarative.** (INFÉRENCE)&#x20;
  - La phrase « No unobserved intermediate tip may be injected into the queue » (qualification, §B5) ne s'appuie sur aucune preuve exécutable.
  - D2 met en file n'importe quelle tête hexadécimale de 40 caractères étiquetée `FAST_FORWARD` (OBSERVÉ).
  - Le seul point d'application serait l'adaptateur d'observation futur, qui n'existe pas encore. C'est acceptable à ce stade, à condition de le formuler comme une règle et non comme une propriété qualifiée.
- **NB5 — Preuves D2 conditionnées à une étiquette fournie par l'appelant.** (OBSERVÉ)&#x20;
  - Les tests réutilisés `test_non_fast_forward_blocks_without_queueing` et `test_unknown_ancestry_blocks_without_queueing` prouvent le comportement de D2 pour une `transition_class` fournie de l'extérieur. Ils ne prouvent pas que la classification d'ascendance est correcte.
  - Sonde A→B→A : relabelliser H1 en `FAST_FORWARD` après H2 est accepté. D2 émet `QUEUE_EXACT_HEAD_FOR_EVALUATION` sans rien ajouter (déduplication) et `latest_observed_head` régresse vers H1.
  - L'ordre FIFO est préservé, mais la trace d'audit est trompeuse. C'est un comportement de prédécesseur, hors périmètre de la correction.
- **NB6 — Écarts sémantiques dans la matrice.**&#x20;
  - `SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD` et `PENDING_HEAD_RETARGETED_TO_NEWER_HEAD` pointent vers `test_fast_forward_queues_without_retargeting_active`, qui couvre une tête *active*, pas une tête *en attente non active*. Ma sonde montre que la tête en attente non active conserve bien `[H1, H2]` (OBSERVÉ) ; le comportement tient, mais la correspondance est inexacte.
  - `QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD` et `QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT` sont étiquetés `DIRECT_P5E` alors qu'ils pointent vers une mutation de drapeau (`test_queue_mutations_are_rejected`). La preuve comportementale existe pourtant dans `test_07_queue_capacity_blocks_before_tick`.
- **NB7 — Vocabulaire et garde résiduelle.**&#x20;
  - `INCOMPLETE_SYNTHETIC_WINDOW` est toujours absent du contrat (0 occurrence) ; il faut déclarer son statut non-PASS.
  - Un doublon de créneau est codé `CADENCE_GAP` (E11), ce qui est un mauvais libellé.
  - La garde AST est nettement meilleure, mais reste contournable via `getattr(__builtins__, …)`. Le modèle actuel est pur à la lecture.
- **NB8 — Discipline d'évidence moins stricte que la passe précédente.**&#x20;
  - La passe complète a été exécutée sur un worktree dont seul l'état « propre » est déclaré, sans clone jetable ni empreinte pré/post de l'état réel. La passe précédente fournissait ces deux éléments, et l'anomalie de provenance (cause inconnue) n'est pas résolue.
  - Je ne peux vérifier ni les 270 ni les 1474 tests.
- **NB9 — Préconditions du protocole réel.** (B4, question 14)&#x20;
  - L'instant exact de `CONTROLLED_SOURCE_RELEASE_MONOTONIC` n'est pas défini : début du push, accusé de réception, ou confirmation de mise à jour de la ref ? L'écart vaut plusieurs secondes sur une borne de 60.
  - L'exigence d'un même domaine monotone (même hôte, même horloge) que le lecteur figure dans l'adjudication, mais pas dans le contrat.
  - La ref utilisée pour la libération contrôlée et l'autorité de pousser ne sont pas énumérées. Pousser sur `integration/system-v1` reviendrait à muter la source canonique.
  - Ces points ne sont pas bloquants pour le candidat, mais obligatoires avant toute préregistration d'une expérience réelle.

### B1_CLOSURE_CHECK

- **Question 1.** Les 8 mutations précédemment survivantes sont rejetées (OBSERVÉ, `test_b1_adversarial_invariants_reject_previously_surviving_mutations`). En revanche, la couverture « tous blocs normatifs » est en échec (BB1).
- **Questions 2 et 3.** Les 10 cas, 25 breakers de base et 8 breakers de clôture sont tous présents dans la matrice. Chaque entrée pointe vers une paire classe.méthode qui existe réellement : je l'ai vérifié par AST et non par sous-chaîne. Les 23 tests distincts passent (OBSERVÉ).
- **Question 4.** Les réutilisations D2/D4 sont globalement suffisantes, avec les réserves NB5 et NB6.
- **Question 5.** Il reste des preuves déclaratives présentées comme comportementales (NB4, NB6).
- **Question 6.** Oui, dans une mesure limitée : `verdict: "PASS"` est une chaîne écrite à la main. Le test de matrice n'exécute rien et n'épingle pas l'objet couvert (BB1).

### B2_CADENCE_CHECK

- **Question 7.** La cadence fixed-rate est appliquée, pas seulement la divisibilité par 30 (`scheduled - previous_scheduled != interval` donne `CADENCE_GAP`).
- **Question 8.** Sauter le premier créneau requis donne `SKIPPED_REQUIRED_ATTEMPT` (OBSERVÉ).
- **Question 9.** Un trou, un doublon, un chevauchement ou une tentative hors grille sont bloqués. Le débordement non enregistré reste un cas limite (NB1).
- **Question 10.** Les valeurs 30, 60 et l'origine 0 sont figées dans `make_timing_plan`, et `_validate_plan` exige l'égalité stricte.

### B3_TEMPORAL_INCONSISTENCY_CHECK

- **Question 11.** Une cible vue dans une tentative démarrée avant la libération donne `BLOCKED`, y compris quand la lecture se termine après la libération (E9, OBSERVÉ).
- **Question 12.** L'ordre ambigu B→A n'est pas détecté (NB2).
- **Question 13.** Toute la séquence est validée avant de décider. Une incohérence survenant après la détection fait basculer le PASS en `BLOCKED` (E10, OBSERVÉ). Aucun blanchiment par une observation ultérieure.

### B4_TIMING_METRIC_CHECK

- **Questions 15 à 17.** L'instant de début et l'instant de fin sont deux champs distincts, et la latence est mesurée à la fin de lecture : la durée de lecture est donc incluse (OBSERVÉ : `test_b4_read_completion_not_poll_start_controls_latency`, latence 61 donne FAIL). La frontière à 60 inclus est cohérente.
- **Question 18.** Le fixed-rate est suffisamment spécifié pour le modèle. Il ne l'est pas encore pour une expérience réelle (NB9 ; la gigue ou le décalage d'un démarrage réel par rapport à la grille n'est pas défini).
- **Question 19.** Le contenu du contrat ne prétend plus que l'origine est observable, mais aucune garde n'empêche d'y revenir (BB1).
- **Question 20.** La garantie de 60 s avec une panne transitoire n'est plus inconditionnelle (`single_transient_read_failure_may_still_meet_60_second_bound: false`, gardé), et la version conditionnelle est correcte.
- **Question 14.** Origine valide en principe, sous les réserves NB9.

### B5_TIP_AND_QUEUE_CHECK

- **Questions 21 et 22.** `EXACT_TIP_OBSERVED` exige l'égalité stricte des identités, et une observation réussie sans identité est rejetée. Une tête intermédiaire n'est jamais déclarée observée par le modèle, qui renvoie FAIL ou INCOMPLETE (E7). La non-injection dans la file n'est pas exécutable (NB4).
- **Question 23.** Aucune coalescence réintroduite : la contenance n'entre dans aucune opération de file.
- **Question 24.** FIFO, absence de remplacement et absence de reciblage tiennent (OBSERVÉ via D2), avec la réserve d'audit NB5.
- **Question 25.** Aucune promesse de détection par tête transitoire : `PER_TRANSIENT_TIP_DETECTION_SLA_QUALIFIED` est interdit et gardé.

### EVIDENCE_MATRIX_CHECK

- 43 entrées correspondent à 23 tests distincts.
- Les blobs correspondent sous `git hash-object --path`.
- Les classes et méthodes existent.
- Défauts : statut PASS écrit à la main, contrat et modèle non épinglés (BB1), types de preuve mal étiquetés (NB6).
- Les clés JSON en double seraient fusionnées silencieusement à la lecture ; c'est un risque mineur.

### AUTHORITY_LEAKAGE_CHECK

- Aucune fuite observée : le modèle est pur, `_result` code en dur `automatic_*` et `real_*` à False, et les runtimes D2/D4 sont inchangés.
- L'autorité humaine est gardée (`human_adjudication_before_external_rereview_forbidden`, mutation détectée).
- Deux points ouverts, déjà signalés précédemment et non adressés : la mutation de l'état de contrôle D4 réel par une observation future, et l'autorité de pousser pour la libération contrôlée (NB9). Ils doivent être énumérés avant toute expérience réelle.

### CLAIM_SCOPE_CHECK

- La déclaration maximale (`…TARGETED_CLOSURE_CANDIDATE_QUALIFIED_PENDING_EXTERNAL_REREVIEW`) est cohérente avec le contrat.
- Le §B1 du rapport de qualification surdéclare (BB1). Le §B5 présente une règle comme une propriété (NB4).
- Les rapports ne prétendent ni SLA réel ni boucle réelle.

### MISSING_ADVERSARIAL_CASES

- Mutation de chaque champ normatif survivant (BB1), et combinaison de régressions B4.
- Lecture qui déborde au-delà du créneau suivant, avec ou sans enregistrement suivant (NB1).
- Tête tierce observée après la libération puis cible ; retour arrière vers la cible (NB2).
- Tête déjà en file puis descendante observée, appliquées à `classify_tip_visibility` (NB3).
- Tête en attente non active plus nouvelle tête FF : le test existe en D2 mais n'est pas référencé (NB6).
- Changement du contrat après construction de la matrice.

### RECOMMENDED_TARGETED_CORRECTIONS

1. **(BB1)** Dans `assert_contract_invariants`, ajouter des égalités strictes pour les 20 champs normatifs survivants listés en BB1. Ne pas ajouter les textes `purpose`/`name`, ni les SHA de contexte qui ne sont que des traces historiques.
2. **(BB1)** Dans la matrice et son test, épingler les blobs du contrat et du modèle couverts, et échouer en cas d'écart.
3. Rejouer le balayage de mutations de feuilles comme critère de sortie. Survivants admis : seulement des champs explicitement déclarés non normatifs.
4. **(Optionnel, même passe)** Pour NB1, soit bloquer quand `completed > scheduled + interval` sans tentative suivante, soit déclarer ce débordement admissible dans le contrat. Pour NB6, réétiqueter les preuves déclaratives et référencer `test_07` ainsi que le cas D2 « en attente non active ». Pour NB7, ajouter `INCOMPLETE_SYNTHETIC_WINDOW` au contrat comme statut non-PASS.
5. NB2, NB3, NB4 et NB9 relèvent de la préregistration d'une future expérience réelle, pas de cette clôture.

Ensuite : passe adversariale ciblée sur le HEAD persisté, puis une seule passe complète, de préférence en clone jetable avec empreinte de l'état réel (NB8).

Cette revue n'est ni une adoption humaine ni une autorisation d'exécution réelle.