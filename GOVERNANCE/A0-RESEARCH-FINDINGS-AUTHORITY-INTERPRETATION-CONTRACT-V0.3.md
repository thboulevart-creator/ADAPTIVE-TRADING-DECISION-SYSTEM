# A0 — RESEARCH FINDINGS AUTHORITY / INTERPRETATION BOUNDARY — CONTRACT V0.3

Date: 2026-09-27

Contract ID:
`ATDS_A0_RESEARCH_FINDINGS_AUTHORITY_INTERPRETATION_V0_3`

Persistence base HEAD:
`d2871df7e45981a9b6b8f0b6af23545500b9dce3`

Status:
`HUMAN-ADOPTED DOCUMENTARY CONTRACT — PERSISTED-HEAD QUALIFICATION PENDING`

Implementation:
`NOT_AUTHORIZED`

Test-first RED:
`NOT_AUTHORIZED`

## 1. Purpose

A0 governs:

```
GOVERNED SCIENTIFIC SOURCE
            ↓
            A0
            ↓
AUTHORITATIVE RESEARCH PROJECTION
            ↓
future DecisionPolicy
```

A0 must prove that a downstream scientific projection is the exact, complete, reproducible and epistemically faithful derivation of governed scientific sources rather than a plausible object, favorable subset, caller-supplied status or post-hoc reinterpretation.

A0 does not establish universal truth. It establishes downstream admissibility under exact source authority and exact limitations.

## 2. Explicit boundary

A0 belongs to:

`RESEARCH → scientific authority → scientific interpretation`

A0 MUST NOT produce or authorize:

- DecisionPolicy;
- Decision;
- BUY / SELL / HOLD;
- risk allocation;
- portfolio allocation;
- positive P1.1 ACTION authorization;
- ACTION;
- order or broker instruction;
- MT5 execution;
- PnL claim;
- durable knowledge promotion;
- automatic adaptation.

A PASS means only that the projection may be treated as authoritative research evidence by a future governed consumer.

## 3. Existing ResearchFindings V0.1

The existing `src/research_findings.py` model remains historical and usable within its existing scope.

It is NOT the authoritative A0 carrier.

A0 requires a distinct authoritative projection capable of representing at least:

- source identity;
- producer/protocol identity;
- profile-registry/profile/policy identity;
- completeness;
- native statuses;
- normalized conclusion;
- data class;
- confirmatory-claim status;
- evidence level;
- research class;
- effective usage permissions;
- controls;
- folds;
- applicability;
- lineage/shared corpus;
- measurement references;
- positive-evidence consumability;
- canonical output identity.

The concrete Python class or serialization name is deferred to test-first implementation.

## 4. Governed inputs

A0 derivation consumes only governed, identifiable inputs:

1. exact scientific-result artifact;
2. exact applicable preregistration / registry / charter;
3. exact scientific producer;
4. exact Source Profile Registry;
5. exact Source Profile resolved from that registry;
6. exact Global Normalization Policy;
7. exact source-native bindings required by the profile;
8. exact expected-result-family authority.

The caller may identify where inputs are located. The caller may not assign their scientific meaning or authority.

## 5. Persistent identity

For persistent A0 artifacts, the normative content identity is:

`SHA-256(raw exact bytes)`

Git blob identity may be retained as repository-native corroboration but is not the normative A0 content identity.

`IDENTITY ≠ AUTHORITY`

A path, filename, schema string, identifier or hash alone never establishes scientific authority.

## 6. Source Profile Registry

A0 uses a pinned/versioned Source Profile Registry.

Its sole resolution function is:

`source_schema → exactly one ACTIVE Source Profile`

Each registry entry binds at minimum:

- `source_schema`;
- `profile_contract_id`;
- `profile_sha256`;
- `profile_status`;
- `supersedes_profile_sha256 | NONE`.

The registry itself has at minimum:

- `registry_schema`;
- `registry_version`;
- `registry_sha256`.

The registry is an authority input to every A0 derivation.

## 7. Registry resolution

For one exact registry version:

`one source_schema → exactly one ACTIVE profile`

The following produce NO AUTHORITATIVE OUTPUT:

- unknown schema;
- zero ACTIVE profiles;
- more than one ACTIVE profile;
- missing profile;
- profile hash mismatch;
- ambiguous registry;
- superseded profile presented as ACTIVE.

The caller cannot choose, override or fallback to another profile.

## 8. Profile identity

The resolved profile bytes MUST satisfy:

`SHA-256(actual profile bytes) == registry.profile_sha256`

And:

`artifact.source_schema == registry.source_schema == profile.accepted_source_schema`

Name equality without content equality is insufficient.

## 9. Profile supersession

Profile replacement is explicit:

`PROFILE V1 → superseded by PROFILE V2`

Two concurrently ACTIVE profiles for the same schema are forbidden.

For sources whose outcomes were already observed before profile creation/revision:

- a new profile MAY PRESERVE authority;
- a new profile MAY RESTRICT authority;
- a new profile MUST NOT INCREASE authority.

## 10. Pre-observation rule

Any future profile or interpretation rule capable of changing the treatment of an unseen outcome MUST be frozen before outcome observation.

Historical source profiles do not acquire fictitious preregistration status. Their allowed role is restriction-only.

## 11. Source Profile responsibilities

The Source Profile may define only how a source is read and bounded:

- accepted source schema/version;
- accepted producer identity;
- exact extraction paths;
- required source-native bindings;
- expected-family reference;
- native-status paths;
- fold-role authority;
- control-state authority;
- data-class authority;
- confirmatory-claim authority;
- research-class authority;
- applicability extraction;
- lineage extraction;
- source-supersession extraction;
- profile-level permission restriction;
- exact governed evidence-level source / derivation authority;
- exact governed native source-promotion-limit authority.

### 11.1 Evidence-level authority — MC1

The Source Profile MUST identify the exact governed evidence-level source or derivation authority applicable to the source family, or explicitly declare that no governed evidence level exists.

The caller MUST NOT supply, select, override or upgrade the evidence level.

If no governed authority establishes a level:

`evidence_level = UNDETERMINED`

and:

`P_evidence_level = ∅`

### 11.2 Source promotion-limit authority — MC2

The Source Profile MUST identify the exact native governed authority from which `source_promotion_limit` is extracted, or explicitly declare:

`source_promotion_limit = NOT_REPRESENTED`

A caller-supplied promotion limit has no authority.

If an applicable source promotion limit cannot be established from governed evidence:

`P_source_promotion_limit = ∅`

The Source Profile MUST NOT define a competing raw-status normalization table.

## 12. Global Normalization Policy

A separate pinned/versioned Global Normalization Policy defines:

- raw-native-status mappings;
- normalized scientific-conclusion vocabulary;
- evidence-level vocabulary;
- closed A0 usage-permission universe;
- D1–D4 mapping rules.

Source Profiles cannot override this global semantics layer.

## 13. Native-status-only authority — C4

A scientific status is authoritative only when extracted from the native producer artifact to which that status belongs.

A downstream redeclaration may establish lineage/context but cannot replace the native status authority.

Example:

`CR2 native evidence status > C01 charter redeclaration of CR2 status`

## 14. Raw native statuses

All relevant native status fields identified by the profile are preserved.

A source may legitimately contain execution, scientific, confirmatory, data-class, artifact-global or per-hypothesis status fields.

Their roles are determined by pinned extraction semantics.

An unresolved material contradiction among native status fields produces NO AUTHORITATIVE OUTPUT.

## 15. Normalized scientific conclusion

The A0 V0.3 vocabulary is closed:

- `SUPPORTED`;
- `REFUTED`;
- `NOT_INTERPRETABLE`;
- `NO_SCIENTIFIC_CLAIM`.

Normalization comes only from the pinned Global Normalization Policy.

## 16. D1 — Evidence level absent

If no governed authority establishes N0–N4:

`evidence_level = UNDETERMINED`

and:

`P_evidence_level = ∅`

No absent level may be inferred as N0.

## 17. D2 — SUPPORTED_N0_SYNTHESIS

`SUPPORTED_N0_SYNTHESIS` may normalize to `SUPPORTED` only while the following remain separately preserved:

- raw status;
- N0 evidence level;
- exact research/probation class;
- source promotion limitations;
- data class;
- effective usage permissions.

`SUPPORTED` does not erase N0 or SYNTHESIS limitations.

## 18. D3 — CONFIRMED

A raw `CONFIRMED` does not automatically establish scientific confirmation.

If `data_class != REAL` OR `confirmatory_claim_status != CONFIRMATORY_ESTABLISHED`:

`normalized_conclusion = NO_SCIENTIFIC_CLAIM`

A future genuinely real and governed established confirmatory result may normalize `CONFIRMED → SUPPORTED`.

`CONFIRMED ≠ N4`

Evidence level remains separately governed.

## 19. C01 authority — C5

For the currently known C01 synthetic path, A0 MUST NOT reconstruct adjudication precedence independently from Charter prose.

The currently qualified synthetic interpretation authority is the exact qualified C01 runner:

`tools/c01_confirmation_runner.py`

current Git blob at this contract base:

`7ea6ed6796eae8618cfd823b49eee1a63a19e096`

bound to the governed execution contract blob:

`f6823cfa7b3c582524b3d512d45b16fdc0450ee8`

and Charter blob:

`ada0ebf41ecd7ab406d2656ac745ed7003d5b5c1`

The current runner qualification is:

`PASS — SYNTHETIC_ONLY`

A0 cannot invent an alternate precedence.

If the runner authority is later superseded, the registry/profile binding must be explicitly superseded.

This does not authorize real C01 execution or scoring.

## 20. Epistemic dimensions

Every authoritative issue preserves separately:

- raw native statuses;
- normalized conclusion;
- data class;
- confirmatory-claim status;
- evidence level;
- research class;
- effective usage permissions.

These dimensions may constrain one another but cannot replace one another.

## 21. Data class

A0 must at minimum distinguish `REAL` from `SYNTHETIC_ONLY`.

Unknown, missing or unextractable mandatory data class MUST NOT be interpreted as REAL.

## 22. Confirmatory-claim status

The Global Normalization Policy defines a closed vocabulary including the semantics required to distinguish:

- `CONFIRMATORY_ESTABLISHED`;
- `NOT_CONFIRMATORY`;
- `SYNTHETIC_ONLY`;
- `NOT_ESTABLISHED`.

Absence never implies `CONFIRMATORY_ESTABLISHED`.

## 23. Control-state authority — C1

Critical controls use the closed states:

- `EVIDENCED_PASS`;
- `EVIDENCED_FAIL`;
- `NOT_REPRESENTED`;
- `CALLER_ASSERTED`.

`CALLER_ASSERTED ≠ EVIDENCED_PASS`

`NOT_REPRESENTED ≠ EVIDENCED_PASS`

The Source Profile may identify where governed evidence for a control resides. It cannot turn a caller assertion into evidence.

## 24. Critical-control precedence

When a source producer/protocol makes a control blocking, a critical failure cannot be compensated by favorable metrics.

A0 follows the qualified source authority; it does not invent statistical precedence.

## 25. Expected family

Completeness authority comes from an exact preregistration / registry / charter / protocol equivalent, never from whatever happened to be emitted.

The expected family is closed and mechanically comparable with observed members across applicable granularities such as:

- hypotheses;
- candidates;
- required comparisons;
- folds;
- primary/diagnostic roles;
- other explicitly preregistered members.

## 26. Completeness

Any of the following blocks authoritative output:

- missing member;
- foreign member;
- duplicate member;
- unexpected substitution;
- silent truncation;
- favorable cherry-picking.

Ordering is required only when contractually meaningful.

## 27. Fold semantics

Fold role comes exclusively from governed fold authority, not container name, JSON location, filename or ordering.

## 28. Applicability domain

A0 preserves the exact applicable domain defined by the source, which may include:

- instrument;
- dataset/corpus;
- price-core semantics;
- target semantics;
- primary horizon;
- diagnostic horizon;
- time scope;
- context scope;
- other declared boundaries.

A0 may preserve or restrict applicability. It may not widen it.

## 29. Lineage/shared corpus

A0 preserves known:

- `derived_from`;
- `shared_corpus_identity`;

or equivalent lineage.

A0 does not calculate universal statistical independence, but it must not erase known dependence/shared corpus.

## 30. Source-artifact supersession — C6

Native source supersession relationships are preserved.

A source explicitly known to be superseded MUST NOT be presented as current authority.

A0 does not define evidence-age decay or automatic supersession discovery.

## 31. Strict parsing — C2

Persistent artifacts participating in A0 authority are parsed fail-closed.

At minimum reject:

- duplicate JSON keys;
- NaN;
- +Infinity;
- -Infinity;
- bool used as numeric;
- numeric-string coercion;
- invalid exact-int semantics.

Producer-specific numeric domains remain producer/protocol responsibilities.

## 32. Measurement identity

Measurements remain exactly source-bound by relevant identity, value, scope, metric, sample size and fold role.

A0 MUST NOT invent, replace, rebind, silently round, silently coerce or mix measurements across source chains.

## 33. Non-SUPPORTED measurements — C3

For:

- `REFUTED`;
- `NOT_INTERPRETABLE`;
- `NO_SCIENTIFIC_CLAIM`;

measurements may remain available for trace/audit/explanation/future research but:

`positive_evidence_consumability = FALSE`

A future consumer cannot bypass the scientific conclusion by selecting a favorable metric.

## 34. Closed usage-permission universe

The Global Normalization Policy defines a finite, closed A0 usage-permission universe `U`.

Each permission source yields a subset of `U`.

Unknown permission tokens fail closed.

## 35. D4 — Closed permission intersection — MC4

For A0 V0.3 the permission-constraining dimensions are exactly the following six and no others:

```
P_effective =
    P_evidence_level
  ∩ P_research_class
  ∩ P_source_promotion_limit
  ∩ P_data_class
  ∩ P_confirmatory_claim
  ∩ P_profile_restriction
```

There is no:

- `P_other_explicit_applicable_constraints`;
- implicit seventh permission source;
- caller-added permission source.

A seventh permission-constraining dimension requires a later governed contract revision.

## 36. Missing permission source

If an applicable permission source cannot establish a governed set:

`P_dimension = ∅`

therefore:

`P_effective = ∅`

No permissive fallback exists.

## 37. Monotonicity

Adding a restriction MUST satisfy:

`P_new = P_old ∩ P_restriction`

therefore:

`P_new ⊆ P_old`

Adding evidence constraints cannot increase permissions.

Post-observation revisions cannot widen effective permissions.

## 38. Scientific conclusion vs usage permissions

`normalized_conclusion` and `effective_usage_permissions` are separate outputs.

It is valid to have:

```
normalized_conclusion = SUPPORTED
effective_usage_permissions = ∅
```

Scientific support does not create downstream permission.

## 39. No operational permission semantics

No token in the A0 permission universe is itself:

- Decision;
- BUY / SELL / HOLD;
- risk or sizing authority;
- ACTION authorization;
- execution right.

## 40. Free-text confinement

Narrative fields such as statement/reason/rationale may be preserved only as non-authoritative opaque references plus content identity when needed downstream.

Free text cannot create scientific, decision or action authority.

## 41. Persistent authority

Persistent A0 authority does not rely on `id()`, weakrefs or Python process-local object identity.

It derives from:

- pinned exact source bytes;
- pinned preregistration;
- pinned producer;
- pinned Source Profile Registry;
- pinned Source Profile;
- pinned Global Normalization Policy;
- deterministic derivation.

Process-local attestation may be an additional local defense only.

## 42. Canonical derivation

The same exact governed inputs MUST produce the same canonical output bytes.

The output has:

`canonical_projection_sha256 = SHA-256(canonical output bytes)`

## 43. Downstream verification

A freely reconstructed look-alike object carries no authority.

Authority can be reproduced only by verified deterministic re-derivation from the pinned governed inputs and exact canonical identity comparison.

## 44. Downstream authoritative-consumer rule — MC3

For the A0-governed research path, a future DecisionPolicy MUST treat as authoritative research evidence only a successfully verified A0 authoritative projection.

The following MUST NOT independently carry authoritative research evidence into DecisionPolicy:

- raw ResearchFindings V0.1;
- caller-constructed ResearchFinding / ResearchFindings;
- copied or reconstructed A0-looking objects;
- raw producer artifacts bypassing A0;
- downstream redeclarations of scientific status.

This rule does not implement DecisionPolicy and does not close the existing `produce_decision(..., decision=<str>)` bypass. Those remain A1/A2 responsibilities.

## 45. Canonical output minimum

The authoritative carrier includes at minimum:

- `source_artifact_sha256`;
- `source_schema`;
- source supersession status/reference;
- producer identity;
- protocol identity;
- `profile_registry_sha256`;
- `source_profile_sha256`;
- `normalization_policy_sha256`;
- expected-family identity;
- completeness status;
- raw native statuses;
- normalized conclusion;
- data class;
- confirmatory-claim status;
- evidence level;
- research class;
- effective usage permissions;
- control states;
- fold roles;
- applicability domain;
- lineage;
- shared-corpus identity;
- measurement references;
- positive-evidence consumability;
- opaque narrative references;
- `canonical_projection_sha256`.

Exact field names may be refined test-first; these represented properties may not be removed.

## 46. Mandatory invariant set

A0 V0.3 requires:

- unknown schema fails closed;
- registry is pinned/versioned/content-verified;
- exactly one ACTIVE profile per admitted schema;
- caller cannot choose profile;
- profile bytes match registry SHA-256;
- artifact/profile/registry schema binding exact;
- profile supersession explicit;
- historical post-observation profile cannot increase authority;
- future outcome-sensitive profile frozen pre-observation;
- artifact identity alone does not create authority;
- exact producer identity;
- exact protocol/interpreter identity;
- source-native lineage only;
- closed preregistered expected family;
- mechanical completeness;
- no cherry-picking;
- pinned-path native-status extraction;
- native producer artifact is status authority;
- downstream redeclaration cannot replace it;
- raw native status preserved;
- normalization only through pinned global policy;
- four normalized conclusions remain distinct;
- evidence level separate;
- absent governed level = UNDETERMINED;
- research class separate;
- data class separate;
- confirmatory claim separate;
- CONFIRMED never automatically N4;
- synthetic/non-established CONFIRMED cannot become scientific SUPPORTED;
- SUPPORTED_N0_SYNTHESIS retains N0/synthesis restrictions;
- explicit four-state control model;
- caller/absent control never equals evidenced PASS;
- critical failures not rescued by metrics;
- fold role from governed fold authority;
- applicability cannot widen;
- lineage/shared corpus cannot disappear;
- explicit source supersession preserved;
- superseded source cannot be current authority;
- strict parsing rejects duplicate/non-finite/coerced values;
- measurements remain exactly bound;
- non-SUPPORTED measurements cannot become positive evidence;
- finite closed permission universe;
- all six ceiling sources emit subsets of same universe;
- unknown permissions fail closed;
- effective permissions use exact six-set intersection;
- missing permission source contributes empty set;
- additional restriction cannot increase permissions;
- post-observation revision cannot widen permissions;
- conclusion and permissions remain separate;
- SUPPORTED may carry zero permissions;
- A0 permissions never become Decision/ACTION/execution authority;
- free text has no semantic authority;
- canonical derivation deterministic;
- canonical output SHA-256 identified;
- free reconstruction carries no authority;
- verified re-derivation may reproduce authority;
- any unresolved critical ambiguity yields no authoritative output.

## 47. Initial positive fixture

Initial qualification is `SYNTHETIC_ONLY`.

The fixture should be structurally close to a real known producer and include at minimum:

```
H1 → SUPPORTED_N0
H2 → REFUTED_N0
H3 → NOT_INTERPRETABLE
```

with:

- closed expected family;
- explicit fold contract;
- primary and diagnostic folds;
- finite exact measurements;
- exact positive integer sample sizes;
- explicit controls;
- applicability domain;
- lineage;
- N0 research class;
- synthetic data class;
- promotion restriction.

At least one `NOT_INTERPRETABLE` issue must intentionally carry the strongest-looking metric in the fixture.

## 48. Mandatory adversarial families

The test-first RED must cover at least:

### Authority/identity
- forged artifact;
- wrong artifact identity;
- wrong producer/protocol;
- missing/wrong registry;
- unknown schema;
- zero/two ACTIVE profiles;
- caller-selected profile;
- wrong profile hash;
- cross-producer profile;
- superseded profile.

### Post-observation
- profile widens permissions;
- profile widens applicability;
- mapping changes after outcome;
- expected family narrowed after outcome.

### Completeness
- missing SUPPORTED;
- missing REFUTED;
- missing NOT_INTERPRETABLE;
- foreign/duplicate member;
- forged alternative family authority;
- diagnostic promoted primary.

### Status/epistemic laundering
- caller forces SUPPORTED;
- REFUTED/NI/NO_SCIENTIFIC_CLAIM → SUPPORTED;
- downstream redeclaration replaces native status;
- unresolved native-status conflict silently resolved;
- N0 upgraded;
- UNDETERMINED → N0;
- SYNTHETIC_ONLY → REAL;
- NOT_ESTABLISHED → CONFIRMATORY_ESTABLISHED;
- CONFIRMED → N4;
- N0/SYNTHESIS erased.

### Controls
- CALLER_ASSERTED → EVIDENCED_PASS;
- NOT_REPRESENTED → EVIDENCED_PASS;
- critical failure hidden by favorable metric;
- control source replaced.

### Parsing/types
- duplicate key;
- NaN / ±Infinity;
- bool-as-int;
- numeric string;
- invalid exact-int;
- source-specific invalid metric domain.

### Permissions
- unknown permission;
- missing permission source;
- union instead of intersection;
- removed permission reappears;
- restriction increases permissions;
- SUPPORTED auto-adds permissions;
- profile adds permission excluded by another set;
- attempted seventh/open-ended permission source.

### Applicability/lineage
- shared corpus erased;
- derived_from erased;
- instrument/horizon widened;
- diagnostic promoted primary;
- superseded source presented active.

### Measurement bypass
- NOT_INTERPRETABLE + strong metric treated positive;
- REFUTED + strong secondary metric treated positive;
- foreign measurement/sample substitution.

### Reconstruction
- manual object construction;
- copy/deepcopy;
- serialize/reconstruct;
- one-byte canonical modification;
- hash-only authority;
- re-derivation from foreign inputs.

### Semantic escape
- BUY/SELL/HOLD;
- Decision;
- ACTION;
- P1.1 positive authorization;
- knowledge promotion.

## 49. Qualification semantics

PASS requires:

- exact positive fixture accepted;
- complete family preserved;
- all preregistered mutations rejected;
- deterministic derivation reproduced;
- canonical hashes stable;
- protected upstream chain unchanged/qualified;
- fresh persisted-head re-break PASS.

FAIL means a required property was actually tested and a forbidden authority, interpretation, permission or semantic escape was accepted.

BLOCKED means required proof or execution could not be completed.

`BLOCKED ≠ PASS`

`BLOCKED ≠ scientific REFUTED`

## 50. Existing Decision bypass

The current `produce_decision(..., decision=<caller supplied string>)` path remains outside A0 guarantees.

A0 PASS therefore does not prove all current Decision objects originate from A0.

That closure belongs to A1/A2.

## 51. Initial implementation scope

The first RED remains intentionally bounded to:

- synthetic A0 fixture;
- CR1-shaped extraction semantics;
- CR2-shaped extraction semantics;
- C01 `SYNTHETIC_ONLY`-shaped semantics.

No real producer becomes admitted merely because this contract exists. Admission requires a qualified registry/profile path.

## 52. Explicitly deferred

A0 V0.3 does not define:

- freshness scoring;
- evidence decay;
- automatic supersession discovery;
- replication scoring;
- statistical-independence scoring;
- knowledge promotion;
- DecisionPolicy mapping;
- risk/capital policy;
- execution.

## 53. Explicit non-authorizations

Even after future A0 qualification, NOT AUTHORIZED:

- DecisionPolicy implementation merely by virtue of A0 PASS;
- Decision production from A0 without A1;
- BUY / SELL / HOLD;
- positive P1.1 authorization;
- ACTION;
- Risk/Portfolio execution;
- broker/MT5/live/paper trading;
- capital deployment;
- strategy selection;
- durable knowledge promotion;
- automatic adaptation;
- C01 real execution;
- C01 confirmation-data access;
- C01 primary scientific scoring;
- C01 refit/redesign.

## 54. Human decisions incorporated

This contract incorporates D1–D4 exactly as persisted in the companion human-adjudication artifact.

## 55. Closed historical correction record

This contract explicitly includes all retained corrections from the A0 V0.1/V0.2 analysis, independent Claude/Grok counter-expertise, D1–D4 adjudication, A0-R1/A0-R2 and C1–C6.

No previous draft is required to interpret this contract.

## 56. Mechanical acceptance matrix

The closed 64-requirement documentary matrix has the following result for this exact contract text:

```
TOTAL = 64
PASS = 64
PARTIAL = 0
MISSING = 0
FAIL = 0
```

This matrix is a documentary precondition only. It does not qualify runtime code.

## 57. Next governed action

Persist this contract, the D1–D4 adjudication and checkpoint update atomically.

Then perform a fresh persisted-head documentary re-break.

Only after that re-break passes may the A0 test-first RED boundary be opened.
