# PRE-BACKTEST CONCRETE EXECUTABLE GATE RECONCILIATION — 2026-09-19

**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Starting qualified HEAD:** `224e33187730739c49a0bf5dd3c6343023db7120`  
**Purpose:** reconcile the historical `D/R/M/B/A/Q/F/O/I_A/I_B` BLOCKED register against the actual current repository before any real acquisition or real backtest.

## Governing rule

This audit does not authorize acquisition, data use, real backtest, paper trading, broker execution, or live trading.

Each gate entry is examined against current GitHub evidence and receives only:

- `PASS` — concrete required artifact and evidence are present and sufficient;
- `FAIL` — concrete artifact exists but violates the governing requirement;
- `BLOCKED` — required evidence/artifact is absent or cannot currently be proven.

Each entry is persisted before the audit proceeds to the next entry.

Historical register:

`docs/QUALIFICATION-INPUT-REGISTER-V1-BLOCKED.md`

Global gate:

`docs/ADJUDICATION-GLOBAL-EXECUTABLE-GATE-RB-A-Q-RM-01-12-V1-2026-09-05.md`

---

# D — Acquisition declaration + complete component manifest

## Requirement

The global executable gate requires an immutable, versioned concrete acquisition declaration naming at least:

- acquisition domain identity/version;
- representation identity/version;
- complete physical component manifest;
- membership / inclusion / exclusion policy;
- completeness evidence;
- acquisition state.

Q-RM-08 defines the schema and universal semantics, but explicitly distinguishes that schema from project-specific declarations.

## Current repository evidence inspected

Current branch tree contains the governing schema/adjudication artifacts:

- `docs/ADJUDICATION-Q-RM-05-ACQUISITION-DOMAIN-V1-2026-09-05.md`;
- `docs/ADJUDICATION-Q-RM-08-ACQUISITION-DOMAIN-CONTRACT-V1-2026-09-05.md`;
- `docs/QUALIFICATION-INPUT-REGISTER-V1-BLOCKED.md`;
- `04-REFERENCE/EXECUTION-WINDOW-FREEZE.json`;
- Dukascopy calendar tooling.

The current tree contains no separate concrete acquisition declaration / component-manifest artifact for the intended real Dukascopy USATECHIDXUSD acquisition.

Repository content search likewise finds the concrete `acquisition_declaration_version`, `acquisition_domain_id`, `component_manifest`, `component_membership_policy`, and `completeness_evidence` fields only in the Q-RM-08 contract/schema discussion, not in a validated project-specific declaration instance.

The historical Q-RM-08 artifact itself states that project-specific acquisition declarations are BLOCKED.

## Adjudication

The selected execution-window freeze and calendar coverage do not satisfy D:

```text
execution window / expected trading calendar
≠ acquisition-domain declaration
≠ complete component manifest
≠ completeness evidence for acquired physical components
```

A tool default such as `Dukascopy USATECHIDXUSD` also cannot create normative acquisition membership.

No current evidence demonstrates that one exact future real acquisition has a frozen declaration and complete manifest.

## Verdict

```text
D — Acquisition declaration + complete component manifest
BLOCKED
```

Classification:

`ABSENCE OF CONCRETE PROOF / ARTIFACT`

This is not a failure of the universal Q-RM-05/Q-RM-08 architecture. It is a missing project-specific executable input.

## Closure evidence required

D can move to PASS only after a versioned concrete acquisition declaration exists and is adversarially qualified, with at minimum:

- exact Dukascopy instrument/source identity;
- exact bounded acquisition domain;
- exact expected component set or deterministic component-membership rule;
- explicit missing / extra / repeated component handling;
- completeness evidence;
- immutable declaration identity/version.

No acquisition is authorized by this audit.

---

**Current reconciliation state**

```text
D   BLOCKED
R   NOT YET RECONCILED
M   NOT YET RECONCILED
B   NOT YET RECONCILED
A   NOT YET RECONCILED
Q   NOT YET RECONCILED
F   NOT YET RECONCILED
O   NOT YET RECONCILED
I_A NOT YET RECONCILED
I_B NOT YET RECONCILED
```

# R — Representation identity/version

## Requirement

The global executable gate requires an explicit project decision identifying the concrete supported qualification representation and its version. Parser capability, filename extension, or a runtime default is not sufficient.

## Current repository evidence inspected

The repository currently contains technical support or references for multiple physical representations:

- CSV tick reader and admissibility code;
- a CSV schema default such as `tick-csv-v1`;
- Dukascopy BI5 parsing logic in the compatibility probe;
- Parquet support in the compatibility probe;
- Q-RM-06/Q-RM-09 universal binding/versioning contracts.

However, the current Q-RM-06/Q-RM-09 adjudications explicitly leave concrete CSV/JSON/binary/vendor bindings unresolved.

No current project-specific normative artifact selects one exact representation identity/version as the concrete representation for the intended real acquisition/backtest gate.

## Adjudication

```text
technical parser support
≠ normative supported representation selection

runtime schema default
≠ project decision

BI5 compatibility probe
≠ qualified representation/version
```

Because D is not yet instantiated, there is also no acquisition declaration binding a concrete `representation_id` / `representation_version`.

## Verdict

```text
R — Representation identity/version
BLOCKED
```

Classification:

`ABSENCE OF EXPLICIT PROJECT-SPECIFIC NORMATIVE SELECTION`

## Closure evidence required

A versioned project decision must select the concrete representation(s) admitted by the first real acquisition gate, including exact identity/version and relationship to D/B.

No representation is promoted to normative status by this audit.

---

# M — Record-model version

## Requirement

The global executable gate requires an explicit reference to the exact frozen record-model version used by the concrete qualification run.

## Current repository evidence inspected

The repository contains substantial normative/candidate work on logical record semantics, including:

- `docs/ADJUDICATION-NORMATIVE-LOGICAL-RECORD-MODEL-AUDIT-V1-2026-09-05.md`;
- Q-RM-01 through Q-RM-07 adjudications;
- acquisition-scoped occurrence identity semantics;
- occurrence-based rather than content-based individuality;
- qualification-before-enumeration;
- versioning requirements.

However, the record-model audit itself currently states:

```text
NORMATIVE LOGICAL RECORD MODEL = CANDIDATE DEFINED
RECORD MODEL FREEZE            = BLOCKED
```

and lists unresolved concrete dependencies including exact record-boundary semantics, physical→logical mapping, multi-file acquisition semantics, malformed/ambiguous handling and format binding/version matrix.

No concrete acquisition artifact currently references one exact frozen `record_model_version`.

## Adjudication

The existence of a `V1` adjudication document does not by itself constitute the concrete record-model version required by M.

```text
candidate semantic model
≠ frozen record-model version

document version/date
≠ concrete qualification reference
```

## Verdict

```text
M — Record-model version
BLOCKED
```

Classification:

`MODEL FAMILY DEFINED; CONCRETE FREEZE / VERSION REFERENCE ABSENT`

## Closure evidence required

A specific record-model contract/version must be frozen after its concrete representation dependencies are closed and then referenced exactly by the first acquisition/qualification tuple.

No record-model freeze is performed by this audit.

---

# B — Concrete format binding(s)

## Requirement

For each admitted representation/version, the binding must explicitly and versionedly determine:

- record framing / boundaries;
- logical segmentation;
- physical→logical cardinality;
- non-observation classification;
- logical field mapping / units;
- occurrence individuation;
- malformed / ambiguous classes;
- failure scope and acquisition interaction;
- cross-component framing;
- all qualification-relevant semantic dependencies.

## Current repository evidence inspected

The repository has executable parsing behavior for:

- CSV ticks;
- Dukascopy BI5 (including 20-byte records, `>IIIff`, UTC hour reconstruction, price scaling);
- Parquet in the V4.3 compatibility probe.

It also has data-admissibility checks for CSV.

However, Q-RM-09 explicitly states:

```text
CONTRACT SCHEMA = PASS
CONCRETE FORMAT BINDINGS = BLOCKED
```

The parser/probe code does not by itself constitute the versioned normative binding required by B. In particular, implementation behavior cannot silently become authority for framing, anomaly scope, individuation or acquisition interaction.

## Adjudication

```text
parser implementation
≠ normative format binding

BI5 struct knowledge
≠ complete Q-RM-09 binding

compatibility probe
≠ binding authority
```

## Verdict

```text
B — Concrete format binding(s)
BLOCKED
```

Classification:

`EXECUTABLE PARSERS EXIST; NORMATIVE CONCRETE BINDING ARTIFACT ABSENT`

## Closure evidence required

At least the representation selected by R for the first real acquisition must receive one concrete versioned binding satisfying every Q-RM-09 field and adversarial property. If raw Dukascopy BI5 is selected, its binding must explicitly freeze all BI5 semantics used for qualification rather than inherit them from probe code.

No parser is promoted to normative authority by this audit.

---

# A — Concrete anomaly matrix

## Requirement

For every supported binding, the concrete anomaly registry must versionedly define at least:

- anomaly class ID;
- trigger condition and evidence;
- affected physical scope;
- localisability test;
- possible interpretations;
- mandatory outcome;
- acquisition-fatal flag;
- impact on qualification membership;
- required diagnostic artifact;
- binding version.

## Current repository evidence inspected

Q-RM-10 establishes and adversarially constrains the universal failure policy:

```text
INVALID + constructively LOCALISABLE
→ REJECT RECORD

otherwise
→ QUALIFICATION BLOCKED

REJECT ACQUISITION
→ only when explicitly declared acquisition-fatal
```

But Q-RM-10 itself explicitly records:

```text
UNIVERSAL FAILURE POLICY = PASS
CONCRETE ANOMALY MATRIX  = BLOCKED
```

Executable CSV/BI5 checks currently detect some concrete errors, but there is no validated versioned anomaly registry tied to one admitted B representation that maps the complete declared anomaly classes to Q-RM-10 outcomes.

## Adjudication

```text
error checks in code
≠ concrete normative anomaly matrix

universal failure policy
≠ format-specific anomaly registry
```

## Verdict

```text
A — Concrete anomaly matrix
BLOCKED
```

Classification:

`UNIVERSAL POLICY CLOSED; FORMAT-SPECIFIC MATRIX ABSENT`

## Closure evidence required

After R/B are selected, publish and adversarially qualify a concrete anomaly matrix for the selected binding/version. Unknown/unregistered anomalies must remain fail-closed.

No existing runtime check is promoted to normative matrix authority by this audit.

---

# Q — Qualification contract + parameters

## Requirement

The global executable gate requires an immutable qualification contract containing:

- qualification identity/version;
- exact parameters;
- acceptance/rejection rules;
- relationship to D/R/M/B/A;
- mandatory adversarial variants;
- enough information for two conforming implementations to derive the same qualified logical universe.

## Current repository evidence inspected

Several qualified artifacts exist, but they solve different problems:

- `04-REFERENCE/EXECUTION-WINDOW-FREEZE.json` freezes the selected five-year execution window and explicitly records `real_backtest_authorized=false`;
- P0.3 qualifies the calendar/freeze surface while explicitly excluding native BI5 acquisition, tick completeness/manifests/reconciliation and real backtesting;
- `docs/03.1.2-MOMENTUM-V1-BASELINE-PROTOCOL.md` is a PASS protocol for the first baseline experiment;
- Q-RM-12 defines the generic determinism test protocol.

None of these artifacts instantiates the missing concrete logical-data qualification tuple with an exact `qualification_contract_id` / `qualification_contract_version` bound to D/R/M/B/A.

The unrelated root `R01-MINIMUM-DATA-SPEC-V0.6.md` concerns another MDS/reclassification domain and is not evidence for trading-data qualification.

## Adjudication

```text
execution-window freeze
≠ logical-data qualification contract

Momentum backtest protocol
≠ D/R/M/B/A qualification contract

Q-RM-12 generic test protocol
≠ concrete Q instance
```

## Verdict

```text
Q — Qualification contract + parameters
BLOCKED
```

Classification:

`EXPERIMENT PROTOCOL EXISTS; CONCRETE DATA-QUALIFICATION CONTRACT INSTANCE ABSENT`

## Closure evidence required

After D/R/M/B/A are concretized, persist one exact Q contract/version with all parameters and acceptance/rejection/adversarial rules needed to establish qualified logical membership for the first real acquisition.

The already-qualified Momentum protocol remains valid and does not need to be rebuilt merely to close Q.

---

# F — Freeze artifact + persistence

## Requirement

Q-RM-11 requires a concrete immutable serialized artifact capable of reconstructing exactly the qualified logical occurrence universe from the complete normative tuple:

```text
D + R + M + B + Q
```

plus explicit qualification status, membership, occurrence individuality, anomaly summary and freeze state.

## Current repository evidence inspected

The repository does contain a real persisted freeze:

`04-REFERENCE/EXECUTION-WINDOW-FREEZE.json`

and executable verification in `tools/frozen_execution_window.py`.

That artifact validly freezes the selected execution-window/calendar boundary and preserves:

- `2021-08-14 → 2026-08-14`;
- calendar-resolution counts;
- warmup policy;
- source qualification evidence;
- explicit `massive_acquisition_authorized=false`;
- explicit `real_backtest_authorized=false`.

However, this is not the Q-RM-11 logical-universe freeze. It contains no concrete D/R/M/B/Q reconstruction tuple and no serialized qualified occurrence membership/individuality result.

Q-RM-11 itself states:

```text
SEMANTIC FREEZE CONTRACT        = PASS
CONCRETE PERSISTENCE / SNAPSHOT = BLOCKED
```

The process-local `BoundResearchInput` attestation also does not satisfy Q-RM-11 persistence: it binds an existing corpus/contract in one process and does not serialize the qualified logical occurrence universe.

## Adjudication

```text
execution-window freeze
≠ logical-occurrence-universe freeze

corpus hash binding
≠ Q-RM-11 frozen qualification artifact
```

## Verdict

```text
F — Freeze artifact + persistence
BLOCKED
```

Classification:

`A DIFFERENT FREEZE EXISTS; REQUIRED LOGICAL-UNIVERSE SNAPSHOT DOES NOT`

## Closure evidence required

After D/R/M/B/A/Q are closed and qualification executes, persist one immutable Q-RM-11 artifact schema and concrete frozen artifact that can be independently reconstructed without relying on runtime traversal or ambient state.

The valid execution-window freeze remains preserved and must not be repurposed as a different semantic artifact.

---

# O — Deterministic semantic comparison oracle

## Requirement

Q-RM-12 requires an independently reviewable deterministic oracle defining semantic equality of two qualified logical occurrence universes.

The oracle must compare at least:

- acquisition-domain membership;
- logical record boundaries;
- logical cardinality;
- non-observation exclusion;
- anomaly classification/outcome;
- qualification membership;
- occurrence individuality;
- freeze reconstruction tuple.

It must not reduce equality to physical ordering or an arbitrary file/container hash.

## Current repository evidence inspected

Q-RM-12 defines the required comparison semantics and adversarial variants, but it explicitly states the executable determinism run remains BLOCKED.

Repository search finds no dedicated current executable semantic-universe oracle.

Existing mechanisms serve different scopes:

- corpus/file hashes prove exact-byte or inventory identity;
- compatibility probes compare transfer-relevant feed properties;
- pytest equality/assertions verify specific component contracts;
- no artifact currently defines semantic equality of complete Q-RM qualified logical occurrences.

## Adjudication

```text
Q-RM-12 oracle specification
≠ executable comparison oracle

content/inventory hash equality
≠ semantic logical-occurrence equality

feed-compatibility metrics
≠ Universe(A) = Universe(B)
```

## Verdict

```text
O — Deterministic semantic comparison oracle
BLOCKED
```

Classification:

`ORACLE SEMANTICS SPECIFIED; EXECUTABLE INDEPENDENT ORACLE ABSENT`

## Closure evidence required

Implement and adversarially qualify a deterministic semantic comparison oracle after M/B/A/Q/F define the semantic object being compared. It must preserve strict duplicate individuality and reject physical-order shortcuts.

---

# I_A — Reference implementation

## Requirement

I_A must be an executable reference implementation conforming to the complete concrete semantics:

```text
D + R + M + B + A + Q + F + O
```

and capable of producing the qualified logical occurrence universe without inventing missing semantics.

## Current repository evidence inspected

Executable candidate surfaces exist:

- `src/data/tick_reader.py`;
- `src/data/dataset_admissibility.py`;
- `tools/probe_research_execution_compatibility_v4_3.py`;
- calendar/freeze tooling;
- research input binding.

These are useful building blocks, but none is currently a complete implementation of the Q-RM qualification chain.

They do not jointly establish one current executable that consumes the concrete D/R/M/B/A/Q tuple, produces the Q-RM-11 F artifact, and exposes its result for comparison through O.

Moreover, D/R/M/B/A/Q/F/O are presently BLOCKED, so conformance to those concrete inputs cannot yet be demonstrated.

## Adjudication

```text
existing parser / admissibility / compatibility code
≠ Q-RM reference implementation

useful implementation building blocks
≠ I_A PASS
```

## Verdict

```text
I_A — Reference implementation
BLOCKED
```

Classification:

`PARTIAL IMPLEMENTATION SURFACES EXIST; COMPLETE CONFORMING REFERENCE PATH ABSENT / NOT QUALIFIABLE YET`

## Closure evidence required

After D/R/M/B/A/Q/F/O are concretely closed, implement or deliberately compose one reference path and adversarially prove that it conforms to those exact versions without fallback to parser defaults or ambient state.

Existing components should be reused where they already satisfy the final contracts; this audit does not require rewriting them merely because I_A is currently BLOCKED.

---

# I_B — Independent comparison implementation

## Requirement

I_B must be an independently implemented qualification path operating from the same concrete D/R/M/B/A/Q/F semantics as I_A, without sharing a semantic shortcut capable of reproducing the same defect.

Q-RM-12 explicitly permits different parser libraries and traversal implementations, but requires the resulting qualified logical universe to be semantically identical under O.

## Current repository evidence inspected

The repository contains:

- several parsers/probes and data utilities;
- independent conceptual counter-expertise artifacts;
- Q-RM-12's two-implementation test protocol.

No current executable artifact is identified as an independently implemented second qualification path conforming to the full concrete D/R/M/B/A/Q/F/O tuple.

External conceptual audits do not satisfy I_B because they are not executable producers of a qualified logical occurrence universe.

Likewise, the existence of CSV/BI5/Parquet readers does not create an independent qualification implementation; those paths do not currently consume the same frozen concrete semantic tuple and produce a Q-RM-11 artifact for oracle comparison.

## Adjudication

```text
second parser / probe
≠ independent Q-RM qualification implementation

independent conceptual review
≠ executable I_B

shared incomplete semantics
≠ independent determinism evidence
```

## Verdict

```text
I_B — Independent comparison implementation
BLOCKED
```

Classification:

`NO QUALIFIED INDEPENDENT SECOND IMPLEMENTATION FOUND`

## Closure evidence required

After the concrete semantic package and I_A exist, implement an independent comparison path with no shared semantic shortcut that could mask the same defect, then compare I_A/I_B through O under all mandatory Q-RM-12 variants.

---

**Next governed action:** persist the complete reconciliation conclusion and derive the smallest concrete closure program before any acquisition or real backtest.


---

# Complete reconciliation conclusion

## Final matrix

```text
D   BLOCKED
R   BLOCKED
M   BLOCKED
B   BLOCKED
A   BLOCKED
Q   BLOCKED
F   BLOCKED
O   BLOCKED
I_A BLOCKED
I_B BLOCKED
```

No historical BLOCKED entry can truthfully be promoted to PASS from the current repository state.

This result is a reconciliation result, not a regression of the qualified P0/P1 chain.

## What is already reusable and must not be rebuilt

The current repository already provides valuable qualified or executable foundations:

1. P0.6 reproducible qualification environment.
2. Qualified calendar / selected execution-window surface:
   `USATECHIDXUSD`, `2021-08-14 → 2026-08-14`, selected-window `68 / 68 / 0`.
3. Persisted execution-window freeze with explicit no-acquisition/no-real-backtest state.
4. Qualified Momentum V1 first-baseline protocol.
5. Existing CSV tick reader / admissibility checks.
6. Existing native Dukascopy BI5 decoding knowledge in the V4.3 compatibility probe.
7. Existing Parquet compatibility path.
8. Q-RM-01..12 universal semantic/falsifiability architecture.
9. P1.2..P1.16 governed experiment/evidence/result interpretation chain.
10. P1.16 qualified experimental finding boundary.

None of these should be reimplemented merely because the concrete executable data gate is still BLOCKED.

## Exact gap now exposed

The missing object is not "a backtester" in the abstract.

The missing object is a **concrete, versioned, executable data-qualification package for the first real research acquisition**, capable of instantiating the already-defined universal Q-RM semantics.

Conceptually:

```text
concrete D + R + M
        ↓
concrete B + A
        ↓
concrete Q
        ↓
concrete F + O
        ↓
I_A + independent I_B
        ↓
Q-RM-12 real determinism execution
        ↓
Universe(A) = Universe(B)
+
mandatory adversarial variants conform
        ↓
FINAL EXECUTABLE DATA GATE = PASS
```

Only after that data gate is PASS may a separate bounded acquisition/backtest permission be considered.

## Important distinction

The already-qualified Momentum V1 protocol solves much of the **experiment definition** side of the first backtest.

It does not solve the concrete data gate.

Likewise:

```text
P1.16 qualified finding semantics
≠ acquisition authorization
≠ data qualification
≠ real backtest authorization
```

## Current safety state

```text
real data acquisition       = NOT AUTHORIZED
massive acquisition         = false / NOT AUTHORIZED
real backtest               = false / NOT AUTHORIZED
positive P1.1 AUTHORIZED    = BLOCKED
broker / paper / live       = NOT AUTHORIZED
```

No network acquisition, BI5 download, real dataset processing or backtest was executed during this reconciliation.

## Smallest governed closure program

The dependency order for the next work is:

```text
BLOCK 1 — concrete declaration/model selection
D + R + M

BLOCK 2 — physical interpretation and failures
B + A

BLOCK 3 — qualification semantics
Q

BLOCK 4 — frozen evidence and semantic comparison
F + O

BLOCK 5 — executable determinism
I_A + I_B + Q-RM-12
```

Each block must follow:

```text
formalisation
→ candidate
→ adversarial break
→ correction
→ persisted-HEAD re-break
→ PASS / FAIL / BLOCKED
```

No block may inherit PASS merely because adjacent code already exists.

## Exactly one next governed action

Formalize **without acquiring data and without authorizing execution** the first concrete `D + R + M` candidate package for the bounded Dukascopy `USATECHIDXUSD` research acquisition associated with the already-frozen execution window.

The formalisation must distinguish:

- acquisition declaration rules from an actual acquired component manifest;
- representation selection from parser implementation;
- record-model version from format-specific binding;
- candidate design from qualification PASS.

No real component manifest can be claimed before acquisition evidence exists. Therefore the first D step may select and freeze the **declaration contract / expected membership rule** while the actual acquired-manifest completion remains BLOCKED until an explicitly authorized acquisition later exists.

No real acquisition is authorized by this next action.


---

# D/R/M formalization progress — 2026-09-19

The first concrete D/R/M candidate has now been formalized, adversarially broken, minimally corrected and re-broken.

Candidate artifact:

`reports/data-qualification/drm_first_concrete_candidate_formalization_2026-09-19.md`

Corrected candidate persisted HEAD:

`45b0db9a1b73ca233c6d966cfe409bb72c4cce63`

Corrected candidate blob:

`2249bea6dbf6b5a8e0d49b99a93bf16248f9c0e9`

Adversarial artifact:

`reports/data-qualification/drm_first_candidate_adversarial_break_2026-09-19.md`

Final adversarial re-break commit:

`276611060aaa390dc1304152bad75f03dcb3385c`

Final adversarial artifact blob:

`8e29d132d8a2eaf28bd9901f2bed33392cccfc79`

First persisted candidate verdict:

`FAIL`

Demonstrated defects:

```text
DRM-F01 — WARMUP_DOMAIN_MEMBERSHIP_UNDERSPECIFIED
DRM-F02 — RECORD_MODEL_RETAINED_CANDIDATE_WORDING_LEAK
```

Both were corrected without changing R or any runtime.

The corrected persisted candidate survived the full re-break with no additional demonstrated defect.

Current selected candidate semantics:

```text
D candidate
=
bounded Dukascopy USATECHIDXUSD research acquisition declaration family
with mandatory deterministic 20-H1 warmup prefix
+
frozen five-year evaluation window

R candidate
=
DUKASCOPY_NATIVE_BI5_HOURLY_TICKS_V1_CANDIDATE
with explicit declared UTC-hour provenance
and no filename/path authority

M candidate
=
PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL_V1_CANDIDATE
format-neutral
occurrence-based
strict-duplicate preserving
pre-Q
non-temporal
non-canonical
```

Official gate verdicts remain unchanged:

```text
D = BLOCKED
R = BLOCKED
M = BLOCKED
```

Reasons:

- D has no actual acquisition instance, component manifest or completeness evidence;
- R still requires qualified concrete BI5 B semantics;
- M still requires qualified B/Q semantics before concrete freeze.

This progress does not authorize acquisition or real backtesting.

The D/R/M candidate is now permitted only as candidate input to the next specification block:

```text
B + A
```

No downstream block has yet been started.


---

# B/A formalization progress — 2026-09-19

The first concrete native-BI5 `B + A` candidate has now been formalized, adversarially broken, minimally corrected and re-broken.

Candidate artifact:

`reports/data-qualification/ba_native_bi5_binding_anomaly_candidate_2026-09-19.md`

Initial candidate commit:

`f2a0ae0e038bc3014a2e24a05e55b914783f37b6`

Initial adversarial artifact:

`reports/data-qualification/ba_native_bi5_candidate_adversarial_break_2026-09-19.md`

Initial break commit:

`5a48fb531d26323a5b22e52568c318161443ae14`

Initial candidate verdict:

`FAIL`

Demonstrated layering defects:

```text
BA-F01 — MARKET_SEMANTIC_VALIDITY_LEAK_INTO_BINDING
BA-F02 — PHYSICAL_SLOT_ORDER_USED_AS_TEMPORAL_AUTHORITY
BA-F03 — SAME_HOUR_COMPONENT_CARDINALITY_LEAKS_D_OWNERSHIP
```

Minimal correction commit:

`678a8052c5b73fad8247d6a3f92173171c09111e`

Corrected candidate blob:

`25400abcc3a2a24438954ff27b970bd934313ae3`

Final persisted-head adversarial re-break commit:

`e95583dab2a87d6ef1a19b57599f5f01118a19f1`

Final adversarial artifact blob:

`484860e09305a3088edb6b8b914803b8717a5627`

No additional internal candidate defect was demonstrated after correction.

## Current B candidate semantics

```text
format_binding_id =
B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD

format_binding_version =
B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE
```

The candidate binds an explicitly declared component envelope rather than a bare path:

```text
acquisition_domain_id
component_manifest_entry_id
instrument_id = USATECHIDXUSD
declared_hour_bucket_utc
compressed_payload_bytes
content_hash / provenance reference
```

Filename/path syntax is not normative time authority.

Candidate physical semantics:

```text
one LZMA-Alone stream
→ decompressed bytes
→ byte-zero framing
→ fixed 20-byte slots
→ >IIIff
→ uint32 ms offset
→ uint32 ask raw
→ uint32 bid raw
→ binary32 ask volume
→ binary32 bid volume
```

Candidate logical decoding:

```text
timestamp = declared UTC hour + ms offset
ask = ask_raw / 1000
bid = bid_raw / 1000
volumes = exact finite source binary32 values, no scaling
```

Physical slot locator:

```text
(component_manifest_entry_id, component_local_slot_index)
```

is provenance/occurrence-individuation evidence only.

It is not canonical position, temporal authority or cross-acquisition identity.

B does not decide market-quality predicates such as:

```text
price > 0
ask >= bid
finite negative volume admissibility
chronological ordering of source slots
```

Those remain Q/temporal concerns.

D remains owner of component membership/multiplicity.

## Current A candidate semantics

Concrete anomaly classes now include at minimum:

```text
missing declared component
undeclared offered component
repeated/conflicting component delivery
missing/ambiguous hour provenance
decompression/envelope failure
zero decompressed bytes
terminal partial slot without completeness proof
terminal partial slot with constructive completeness proof
millisecond offset outside hour
NaN / ±Infinity volume
ambiguous component role/provenance
representation/binding identity mismatch
unknown anomaly class
```

Q-RM-10 outcomes are explicitly bound:

```text
constructively local INVALID
→ REJECT RECORD

non-local / ambiguous / unknown scope
→ QUALIFICATION BLOCKED
```

No acquisition-fatal anomaly class has been introduced by default.

No silent repair is permitted.

## Remaining B/A evidence blocker

The following provider-sensitive candidate facts are currently supported inside the repository only by the existing V4.3 implementation surface:

```text
LZMA-Alone
20-byte width
>IIIff
field order
price /1000
binary32 volume fields
```

Therefore:

```text
B = BLOCKED
A = BLOCKED
```

The corrected B/A candidate is internally stable enough to become input to Q formalization, but it is not yet qualified provider truth.

No real data was acquired or processed.

No downstream Q work was started before this persisted closure.
