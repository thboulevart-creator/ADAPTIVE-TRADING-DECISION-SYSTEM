# POST-B-PE-SEM-05 LANE-S BLOCKED AUTHORITY RECOVERY ROUTE SELECTION

Date: 2026-09-22

Repository: thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

Branch: integration/system-v1

Starting HEAD: 295e450b6f00f75ef85b9b2baf2ba538f75a166f

## 1. Authoritative starting state

B-PE-SEM-05 is CLOSED / BLOCKED.

Package integrity is PASS.

Lane S semantic authority remains BLOCKED.

Target epoch remains BLOCKED_UNRESOLVED_TARGET_EPOCH.

No Lane P RequestManifest is authorized.

The three unresolved authority classes are:

A. exact immutable/provider-versioned legacy-hourly K1 semantic authority

B. exact provider-primary native BI5 USATECH raw scale/divisor authority

C. exhaustive target-epoch semantic change-point / continuity authority

This route-selection record performs no new documentary acquisition.

## 2. Classification of A — legacy-hourly K1 semantic authority

### Existing governed sources

Classification:

NOT RECOVERABLE BY REINTERPRETATION OF EXISTING GOVERNED SOURCES.

Existing provider evidence proves only:
- historical legacy-hourly object-family existence;
- current daily BI5 semantics;
- non-exact warning that older hourly files may use hour-relative timestamps;
- client/release chronology.

Existing independent reference implementations corroborate legacy-hourly interpretations but cannot become sole provider-primary authority.

Therefore no existing evidence can be promoted without violating B-PE-SEM-04.

### New documentary route

Classification:

CREDIBLY RECOVERABLE IN PRINCIPLE THROUGH NEW PROVIDER-VERSIONED ARTIFACT ACQUISITION.

The unexhausted route is provider-distributed versioned artifacts, especially:
- Dukascopy Maven DDS2/JForex binaries;
- matching source JARs if published;
- matching Javadoc JARs if published;
- provider-owned parser/history classes or resources embedded in exact versioned artifacts;
- provider-owned archived/versioned documentation snapshots referenced by those artifacts.

Recovery succeeds only if exact provider-shipped material binds the legacy-hourly native representation semantics.

### Current-channel availability

NOT YET CLASSIFIED AS EXTERNALLY UNPROVABLE.

The provider Maven/versioned-artifact channel has not yet been exhausted at class/resource level.

## 3. Classification of B — USATECH native BI5 raw scale/divisor authority

### Existing governed sources

Classification:

NOT RECOVERABLE BY REINTERPRETATION OF EXISTING GOVERNED SOURCES.

Current provider market metadata identifies USATECH and current CFD point value, but does not bind the native BI5 raw integer divisor.

Independent sources corroborate decimalFactor 1000, but remain third-party corroboration.

The inference:

current CFD point value -> native BI5 /1000 divisor

remains forbidden.

### New documentary route

Classification:

CREDIBLY RECOVERABLE IN PRINCIPLE THROUGH NEW PROVIDER-VERSIONED ARTIFACT ACQUISITION.

Candidate provider-primary locations include:
- provider instrument metadata embedded in exact JForex/DDS2 artifacts;
- provider Instrument/financial instrument classes or serialized resource tables;
- provider historical-data decoder/conversion code;
- provider versioned instrument-definition resources.

Recovery succeeds only if a provider-owned exact artifact binds USATECHIDXUSD to the raw integer scale/divisor or to an exact mapping from which the divisor follows noncircularly.

### Current-channel availability

NOT YET CLASSIFIED AS EXTERNALLY UNPROVABLE.

Provider-shipped versioned metadata/resources remain an unexhausted evidence channel.

## 4. Classification of C — target-epoch change-point / continuity authority

### Existing governed sources

Classification:

NOT RECOVERABLE BY REINTERPRETATION OF EXISTING GOVERNED SOURCES.

Current evidence leaves at least:
- the legacy-hourly to current-daily transition boundary unresolved;
- the semantic effect of the 2026-03-03 JETTA historical-data change unresolved;
- the provider Maven client timeline non-exhaustive as a K1 semantic changelog.

Therefore existing material cannot establish full 2021-08-13 through 2026-08-14 semantic continuity.

### New documentary route

Classification:

RECOVERY REQUIRES NEW PROVIDER-VERSIONED ARTIFACT ACQUISITION AND CROSS-VERSION COMPARISON.

This is the hardest of A/B/C.

A credible recovery requires:
- identify the exact provider-shipped class/resource implementing or declaring relevant historical-data semantics;
- obtain immutable versions spanning the target epoch;
- construct a version-to-version semantic change ledger;
- bind every material parser/metadata change point;
- account explicitly for 2026-03-03 JETTA;
- prove either continuity within each epoch or exact semantic changes.

If the provider artifacts do not expose the relevant semantics, or if the version history has gaps that cannot be closed, C must remain BLOCKED and may become EXTERNALLY UNPROVABLE under current public evidence channels.

### Current-channel availability

NOT YET PROVEN UNAVAILABLE.

However C carries the highest risk of ending as EXTERNALLY UNPROVABLE.

## 5. Routes compared

### Route 1 — STOP now

REJECTED AS PREMATURE.

Reason:
provider-distributed immutable/versioned artifact contents have not yet been exhausted.

### Route 2 — SIMPLIFY by lowering provider-primary authority requirements

REJECTED.

Reason:
this would weaken the already-qualified B-PE-SEM-04 contract and convert corroboration into authority by policy change rather than evidence.

### Route 3 — continue with broad mutable web search

REJECTED.

Reason:
unbounded live-page searching does not solve the immutability/versioning problem and would recreate the same evidence weakness already demonstrated by B-PE-SEM-05.

### Route 4 — continue directly to provider contact/support inquiry

NOT SELECTED YET.

Reason:
a provider response could be useful, but provider-distributed versioned artifacts are more reproducible, independently inspectable and already identified as an unexhausted source family.

Provider contact may become a later recovery route only if artifact archaeology fails.

### Route 5 — targeted provider-versioned artifact archaeology

SELECTED.

Reason:
it is the smallest remaining route that can potentially address A, B and C without weakening the authority contract or touching provider BI5 objects.

## 6. Decision

Decision:

CONTINUE.

Selected recovery route:

TARGETED PROVIDER-VERSIONED ARTIFACT RECOVERY.

Exactly one next bounded block is selected:

B-PE-SEM-05R-01 —
PROVIDER-VERSIONED ARTIFACT
DOCUMENTARY RECOVERY

The block is documentary acquisition only.

It is NOT executed by this route-selection record.

## 7. Exact authority boundary of B-PE-SEM-05R-01

When separately opened, the block may acquire only provider-owned immutable/versioned documentary or software-distribution artifacts relevant to A/B/C.

Allowed source families:
- Dukascopy official Maven/public repository;
- exact provider DDS2/JForex binary artifacts;
- exact matching source JARs;
- exact matching Javadoc JARs;
- provider-owned embedded instrument metadata/resources;
- provider-owned embedded historical-data/parser classes/resources;
- provider versioned release/change records needed to bind artifact versions;
- exact provider archive/snapshot material directly linked to these versioned artifacts.

The block may use exact cryptographic hashes for downloaded documentary/software artifacts.

The block may inspect/decompile provider-shipped classes/resources only as documentary evidence of provider implementation semantics.

This is NOT a provider-object market-data observation.

## 8. Prohibited in B-PE-SEM-05R-01

The block must NOT:
- request any historical BI5 tick object;
- request any provider hourly/daily market-data payload;
- build Lane P RequestManifest;
- implement P-DIAG-A or P-DIAG-B;
- execute physical BI5 discrimination;
- run FULL_INTERVAL;
- open B-FIQ-02R;
- materialize D;
- backtest;
- paper/broker/live trade.

It must also NOT:
- reinterpret third-party code as provider-primary authority;
- infer raw divisor from price plausibility;
- infer continuity from absence of release-note wording alone;
- treat a single current provider artifact as proof for the entire 2021–2026 epoch;
- silently bridge missing provider versions.

## 9. Exact objectives

The block must attempt three independent recoveries.

### Recovery A

Find an exact provider-owned versioned artifact that binds legacy-hourly K1 semantic format meaning.

Outcome:
RECOVERED / NOT_FOUND / AMBIGUOUS / BLOCKED.

### Recovery B

Find exact provider-owned versioned USATECH metadata or conversion logic binding native BI5 raw scale/divisor noncircularly.

Outcome:
RECOVERED / NOT_FOUND / AMBIGUOUS / BLOCKED.

### Recovery C

Build a provider-artifact version inventory sufficient to determine whether the relevant semantic implementation changes across the target epoch.

Outcome:
RECOVERED_CONTINUITY / RECOVERED_EPOCH_SPLITS / INCOMPLETE_VERSION_COVERAGE / SEMANTICS_NOT_EXPOSED / BLOCKED.

## 10. Required outputs

At minimum:

ProviderArtifactInventory

ProviderArtifactIdentityRegistry

RelevantClassResourceInventory

LegacyHourlySemanticArtifactFinding

USATECHRawScaleArtifactFinding

CrossVersionSemanticChangeLedger

JETTAChangeImpactFinding

RecoveryAResult

RecoveryBResult

RecoveryCResult

ArtifactLineageResolution

DocumentaryEvidenceHorizon

NoMarketDataObservationAttestation

The block must preserve exact bytes/hashes and provider artifact coordinates/version identities for every acquired artifact used as evidence.

## 11. Recovery success rule

B-PE-SEM-05R-01 does NOT itself promote Lane S dimensions to PASS.

Its role is evidence recovery only.

If one or more A/B/C recoveries succeed:
- persist exact recovered evidence;
- adversarially break the recovery package;
- final persisted-head re-break;
- close the recovery block;
- only then may a later separately governed Lane S re-adjudication consume the recovered evidence.

If all credible provider-versioned artifact channels are exhausted without sufficient authority:
- mark the affected authority class UNRECOVERED;
- distinguish NOT_FOUND from SEMANTICS_NOT_EXPOSED and INCOMPLETE_VERSION_COVERAGE;
- return BLOCKED;
- do not proceed to Lane P.

## 12. Current prohibition boundary

This route-selection record itself performs no new acquisition.

Until B-PE-SEM-05R-01 is separately opened:

provider documentary/software artifact acquisition = NOT AUTHORIZED

provider BI5 GET = NOT AUTHORIZED

new provider-object acquisition = NOT AUTHORIZED

Lane P RequestManifest = NOT AUTHORIZED

P-DIAG implementation = NOT AUTHORIZED

physical semantic discrimination = NOT AUTHORIZED

B-PE-SEM-06 = NOT AUTHORIZED

B-FIQ-02R = NOT AUTHORIZED

FULL_INTERVAL = NOT AUTHORIZED

D materialization = NOT AUTHORIZED

backtest = NOT AUTHORIZED

paper/broker/live = NOT AUTHORIZED

## 13. Final route decision

POST-B-PE-SEM-05 LANE-S BLOCKED AUTHORITY RECOVERY ROUTE SELECTION = PASS

Decision = CONTINUE

A =
existing governed sources insufficient;
new provider-versioned artifact recovery required;
not yet externally unprovable.

B =
existing governed sources insufficient;
new provider-versioned artifact recovery required;
not yet externally unprovable.

C =
existing governed sources insufficient;
new provider-versioned artifact recovery + cross-version comparison required;
highest risk of eventual external unprovability.

Selected next block:

B-PE-SEM-05R-01 —
PROVIDER-VERSIONED ARTIFACT DOCUMENTARY RECOVERY

No new documentary acquisition occurred in this route-selection record.

STOP.
