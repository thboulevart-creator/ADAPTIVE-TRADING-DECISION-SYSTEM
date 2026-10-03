VERDICT = PASS_WITH_NON_BLOCKING_NOTES

J'ai reconstruit les artefacts code et JSON du paquet. Leurs identités correspondent toutes : garde `3f61b91…`, schéma P5-E `87e45cc…`, préregistration `406e67d…`, test GREEN `391663e…`, balayage `bad4959…`, qualification JSON `782e4ef…`, contrat adopté `43d2e45…`.

Ce que j'ai reproduit (OBSERVÉ) :

- 22/22 tests RPE-01 (21 dans le fichier GREEN + 1 balayage) ;
- 89/89 sur la régression ciblée P5-E + RPE-01, avec les tests P5-E du paquet précédent, dont les blobs sont inchangés ;
- 41 sondes adversariales sur le garde.

Rien ne contredit le critère de sortie N4 : toutes les clés ajoutées et tous les vecteurs de doublon ou de coercition sont rejetés sémantiquement, sans recours à la liaison de blob. Les notes ci-dessous sont des durcissements, dont un à faire avant que RPE-02 s'appuie sur le garde.

### BLOCKING_FINDINGS

Aucun.

### NON_BLOCKING_FINDINGS

**NB-1 — L'API accepte un schéma déjà parsé, ce qui laisse contourner la protection contre les doublons du schéma.** (OBSERVÉ ; à corriger avant que RPE-02 consomme le garde)

- Concerné : « RPE-01 GUARD IMPLEMENTATION », `validate_governed_json(raw, schema: object)` et `validate_document(document, schema: object)`.
- Le document est forcément parsé strictement, mais le schéma peut arriver sous forme d'objet déjà construit.
- Falsification : un schéma brut avec deux membres `"fields"`, où le dernier ajoute `"evaluation_override": {"kind": "boolean"}`. Chargé par `json.loads`, il donne un schéma élargi, et `validate_governed_json('{"a":1,"evaluation_override":true}', schema)` est ACCEPTÉ. Le même schéma passé par `parse_schema_json_strict` est rejeté.
- C'est l'usage naturel : le test de balayage lui-même charge le schéma avec `json.loads`.
- Correction minimale : n'accepter que des schémas bruts (`str | bytes`) dans l'API publique, ou n'accepter que des objets produits par le parseur strict (marqueur ou type dédié).

**NB-2 — Exceptions non normalisées.** (OBSERVÉ)

- Concerné : `parse_json_strict`.
- Un entier de 4500 chiffres lève `ValueError` (limite Python de conversion entier/chaîne). Une imbrication de 100 000 niveaux lève `RecursionError`.
- Le comportement reste fail-closed, mais ce ne sont pas des `GovernedSchemaError` : un appelant qui n'intercepte que `GovernedSchemaError` plantera au lieu de rejeter.
- Correction : intercepter `ValueError` et `RecursionError` et les convertir en `GovernedSchemaError`, éventuellement avec une borne explicite de profondeur et de taille.

**NB-3 — Le schéma P5-E est structurel, pas sémantique.** (OBSERVÉ)

- Concerné : « P5-E CONCRETE GOVERNED SCHEMA ».
- Contenu : 89 booléens sans `const`, 3 entiers sans bornes, 57 chaînes libres. Les sondes `evaluation_authorized: true` et `poll_interval_seconds: -5` sont ACCEPTÉES par le garde.
- C'est cohérent avec le périmètre N4 (clés, types, listes), puisque les valeurs restent gardées par `assert_contract_invariants`.
- La qualification devrait le dire explicitement, par exemple : « closed structure, values guarded by P5-E invariants ».
- Pour les futures configurations de runner, d'adaptateur et d'expérience, préregistrer que les drapeaux d'autorité utilisent `const: false` dans le schéma lui-même, pour que le garde porte l'autorité sans dépendre d'un second vérificateur.

**NB-4 — `source_binding` et `artifact_role` ne sont pas appliqués par le garde.** (OBSERVÉ)

- Le garde valide un contrat différent (`objective.purpose` modifié) contre un schéma lié à `43d2e45`. Le rôle n'est jamais comparé à un rôle attendu.
- La liaison n'est donc vérifiée que par `test_p5e_schema_source_binding_matches_current_contract_blob`.
- Recommandation : ajouter des paramètres `expected_role` et, si souhaité, une vérification de blob calculée de façon pure (`sha1("blob <n>\0" + octets)`). Attention à la normalisation des fins de ligne sous Windows (CRLF).

**NB-5 — Langage de schéma : contradictions et classes de caractères.** (OBSERVÉ)

- `const ∉ enum`, `ordered_const ∉ allowed_values` et `const` incompatible avec `pattern` sont acceptés à la définition du schéma. L'effet est restrictif : le schéma devient insatisfiable et tout document est rejeté. Fail-closed, mais détectable seulement par le test d'acceptation de référence.
- `pattern: "\\d"` accepte le chiffre arabe `٣`. Les 13 motifs actuels (`[0-9a-f]{40}\Z`) ne sont pas concernés. Recommandation : `re.ASCII`, ou interdire `\d`, `\w`, `\s`.
- Une surrogate isolée (`\ud800`) est acceptée dans une chaîne libre. Elle pourrait faire échouer plus tard l'écriture des preuves en UTF-8.

**NB-6 — Le balayage de 433 mutations ne couvre pas tous les opérateurs préregistrés.** (OBSERVÉ)

- Concerné : « RPE-01 MUTATION SWEEP TEST » face à `preregistration.mutation_sweep.operators`.
- Les opérateurs « duplicate selected raw JSON member names » et « inject NaN/Infinity constants » sont absents du balayage, qui ne mute que des objets parsés. Ils sont couverts seulement par des tests unitaires ponctuels (`test_duplicate_*`, `test_nan_and_infinities_are_rejected`).
- Le nombre 433 compte donc uniquement les opérateurs sur objets parsés.
- Le balayage charge aussi le schéma de façon permissive (voir NB-1).

**NB-7 — Fidélité du paquet.** (OBSERVÉ)

- La source « RPE-01 RED TEST » embarquée est en réalité le blob GREEN `391663e`. Le RED annoncé `803709c` n'est pas fourni.
- Les rapports Markdown ne correspondent pas à leurs blobs (RED `32e4335` contre `b3a7df3` annoncé ; qualification `1791df2` contre `83f17da`), probablement à cause de l'encodage mal converti (« â€” ») lors de la construction du paquet.
- Le code et les JSON correspondent tous.

### STRICT_JSON_CHECK

- **Question 1.** Les doublons sont rejetés avant construction du dictionnaire, à toutes les profondeurs, y compris l'orthographe échappée `\u0065valuation_authorized`, qui est décodée avant que le hook la voie. Rejeté (OBSERVÉ).
- **Question 2.** `NaN`, `Infinity` et `-Infinity` sont rejetés. `1e400` (lu comme `inf`) est rejeté aussi, parce qu'aucun type « nombre flottant » n'existe dans le langage de schéma.
- **Question 3.** Le décodage UTF-8 est strict : octets invalides et BOM sont rejetés.
- **Question 4.** Restent les exceptions non normalisées (NB-2) et les surrogates isolées (NB-5). Aucun blanchiment de type ou d'autorité.

### SCHEMA_LANGUAGE_CHECK

- **Question 5.** Le langage est fermé : une clé inconnue, un `kind` non supporté, un `min_items` de type `"1"` ou `True`, un `unique` à `"yes"` sont rejetés.
- **Question 6.** Entiers et booléens sont bien distingués via `type(x) is …` : `true` à la place d'un entier et `0` à la place d'un booléen sont rejetés, et `[True]` contre `ordered_const [1]` aussi.
- **Question 7.** Les flottants et la notation scientifique sont rejetés là où un entier est requis (`30.0` et `1e2` rejetés).
- **Question 8.** Unicité, `allowed_values` et `ordered_const` sont sains. L'ordre de validation (vocabulaire, puis ordre, puis type des éléments) n'ouvre aucune faille d'égalité `True == 1`.
- **Question 9.** Les contraintes contradictoires restreignent mais n'élargissent jamais (NB-5).
- **Question 10.** Le parsing strict du schéma brut suffit, à condition qu'il soit obligatoire, ce qu'il n'est pas aujourd'hui (NB-1).

### GUARD_AUTHORITY_CHECK

- **Question 11.** Le garde est pur : imports limités à `json`, `re` et `typing`, aucun accès à l'environnement, aux arguments CLI, au système de fichiers ou au réseau.
- **Question 12.** Aucun canal d'autorité. Seul risque : un déni de service par regex coûteuse, mais les motifs viennent d'un schéma gouverné.
- **Questions 13 et 29.** Un JSON brut explicite plus un schéma explicite constituent la bonne frontière. Garder le garde pur, sans aide de chargement de fichier, est plus sûr ; le chargement est la responsabilité de l'appelant gouverné.

### P5E_CONCRETE_SCHEMA_CHECK

- **Questions 14 et 15.** Les 17 objets sont fermés et toutes les clés sont requises : le balayage ajoute une clé inconnue à chaque objet et retire chaque clé requise.
- **Question 16.** Les types des feuilles sont figés. Les valeurs ne le sont pas, ce qui est voulu (NB-3).
- **Question 17.** Les 8 listes sont fermées : `allowed_values`, unicité, et `min_items == max_items` égal à la cardinalité actuelle.
- **Question 18.** L'ordre de `real_end_to_end_stages` est figé par `ordered_const`.
- **Question 19.** La liaison au blob `43d2e45` est correcte, mais elle n'est prouvée que par un test (NB-4).
- **Question 20.** Le schéma est rigide sur les listes (cardinalité exacte), donc tout amendement exige de modifier le schéma. C'est l'effet recherché, et ce n'est pas dangereux.

### MUTATION_SWEEP_CHECK

- **Questions 21 et 22.** Le balayage est suffisant pour N4. Il rejette par la sémantique du schéma (`validate_document`), sans aucune liaison de blob.
- **Question 23.** Opérateurs à ajouter :&#x20;
  - doublons bruts et constantes NaN/Infinity, intégrés au balayage plutôt qu'en tests unitaires isolés ;
  - remplacement d'une feuille par un objet ou un tableau ;
  - schéma élargi via un chargement permissif (NB-1).
- **Questions 24 et 25.** Aucune mutation ne survit du fait de travailler sur des objets parsés. Les familles « doublons bruts » et « NaN/Infinity » sont couvertes, mais de façon ponctuelle (NB-6).

### NF_D_ADJACENT_CONFIG_CHECK

- **Questions 26 et 27.** Le garde générique convient. Les clés d'autorité, d'override d'environnement et d'override CLI inconnues dans une configuration voisine sont rejetées (`test_unknown_adjacent_config_authority_keys_are_rejected`).
- **Question 28.** Empêcher que du code de runner ou d'adaptateur lise `os.environ` ou `argv` relève à juste titre d'une préregistration ultérieure (RPE-04, RPE-05). Un schéma ne peut pas l'imposer. Il faudra l'exiger par une analyse statique d'imports et d'usages dans ces étapes.

### BINDING_CHECK

- **Question 30.** Les identités du garde et du schéma sont liées dans la qualification JSON. Suffisant.
- **Question 31.** Les sémantiques du langage de schéma n'ont pas besoin d'un artefact séparé. Le blob du garde est leur identité, et la préregistration les décrit.
- **Question 32.** « Toute modification du garde ou du schéma exige une requalification » suffit à ce stade.
- **Question 33.** Aucune auto-référence : le schéma lie le contrat, la qualification lie le garde et le schéma.

### REGRESSION_CHECK

- **Question 34.** 89/89 est suffisant, et reproduit (OBSERVÉ).
- **Question 35.** Une suite Obsidian complète n'est pas nécessaire : le contrat, le modèle et le runtime D4 sont inchangés, et le garde n'a aucun consommateur runtime (INFÉRENCE).

### AUTHORITY_LEAKAGE_CHECK

- **Question 36.** Aucune fuite. Les drapeaux de la préregistration sont tous à false hors `implementation_authorized` (périmètre garde seulement). `rpe02_opened: false`, `real_p5e_authorized: false`.

### CLAIM_SCOPE_CHECK

- **Question 37.** La déclaration `QUALIFIED_FOR_EXTERNAL_REVIEW` est correctement bornée.
- Une imprécision : `qualified_properties` devrait préciser que le schéma P5-E est structurel (NB-3), et que la propriété « schema definition itself strictly parsed » n'est vraie que via `parse_schema_json_strict` (NB-1).

### RECOMMENDED_NEXT_ACTION

1. Une correction minimale ciblée, avant l'adjudication humaine ou au plus tard avant que RPE-02 consomme le garde :&#x20;
   - NB-1 : API acceptant uniquement un schéma brut, ou issu du parseur strict ;
   - NB-2 : normalisation des exceptions.
   &#x20;Ajouter les deux tests RED correspondants et faire une revue delta courte.
2. Intégrer NB-3 et NB-4 (`const` pour les drapeaux d'autorité, `expected_role`) comme exigences des préregistrations RPE-04, RPE-05 et RPE-06.
3. NB-5 à NB-7 : documentaire ou optionnel.

Cette revue ne vaut ni adoption humaine, ni ouverture de RPE-02, ni autorisation de P5-E réel.