# A0 — SOURCE-SPECIFIC METRIC-DOMAIN AUTHORITY RESOLUTION

Date: 2026-09-27

Governed HEAD reviewed:

`4f60f2373b42a12493e39d9d577f1683b5413e29`

Runtime blob:

`18246b818c6c6af8c5412c3b0a515f76c5d5ddc8`

Governed breaker set:

```
historical = e02ecfa6d30c2877a33f5c5d81b161ee562202b6
V0.1 = 2911d5b282ccbb6147b2b54a7db5c357c2d315b6
V0.2 = 9833ce563305cfb6d6fe1de8907e8aa9fc96fda4
V0.3 = d23e3c72dd8bd2200cb392edc6c80b4e744d4751
V0.4 = efcc3ca7927b29b45f5d0dc0180b81176dbed51e
```

A0 V0.3 contract blob:

`f1168481879f33f8762dcb1e19e2ad35211c8ec2`

V0.5 sandbox candidate remains non-governed:

```
commit = f5f902339ddcf0f838790ca154001f91261f9d52
blob = f02eae836b79403673f8a43292cca19eab0c6b33
run = 36332006554
```

## Question resolved

Does an already-governed producer/protocol authority establish a source-specific metric identity/domain that can adjudicate AF04 without inventing a new rule after observation?

## Contract constraint

A0 V0.3 states:

- persistent numeric parsing is fail-closed;
- measurements remain exactly source-bound;
- producer-specific numeric domains remain producer/protocol responsibilities;
- the mandatory adversarial suite must include a source-specific invalid metric-domain mutation.

Therefore A0 itself cannot invent an allowed metric identity or numeric range.

## Authority inventory

Read-only inventory on the exact governed HEAD enumerated 74 candidate A0/research/producer/protocol paths.

Within this boundary, 60 high-probability artifacts were directly inspected across:

- research producer/interprocess contracts;
- research qualification reports;
- research foundation/charter/findings contracts;
- C01 producer/charter documentation;
- A0 governance/adjudication and prior qualification reports;
- backups containing research/producer checkpoints;
- research runtime modules;
- research fixtures/tests;
- research workflows and compatibility probes.

Targeted index searches were also executed for:

- `ATDS_A0_SYNTHETIC_PRODUCER_V0_1`;
- `SYNTHETIC_SCORE`;
- metric-domain terminology;
- allowed-metric terminology;
- measurement-domain terminology;
- numeric-domain terminology.

## Finding

No already-governed producer/protocol artifact establishes any of the following for the synthetic A0 fixture:

1. an allowed metric-identity set;
2. `SYNTHETIC_SCORE` as the exclusive or admitted metric identity;
3. a producer-specific numeric range/domain for `SYNTHETIC_SCORE`;
4. a rule under which `FOREIGN_METRIC` is mechanically invalid.

The strings used by synthetic fixtures are test-fixture content, not an independently governed producer/protocol metric-domain authority.

Therefore:

`IDENTITY ≠ AUTHORITY`

and:

`FIXTURE VALUE ≠ PRODUCER DOMAIN CONTRACT`

## Resolution

`A0_EXISTING_SOURCE_SPECIFIC_METRIC_DOMAIN_AUTHORITY = ABSENT`

`AF04_ORACLE_FROM_EXISTING_AUTHORITY = UNAVAILABLE`

`AF04_IMPLEMENTATION_FAIL = NOT_ESTABLISHED`

`A0_SOURCE_SPECIFIC_METRIC_DOMAIN_AUTHORITY_RESOLUTION = PASS_EXISTING_AUTHORITY_ABSENT`

The resolution boundary itself is complete: the question of whether an existing authority can be reused has been answered negatively.

However, a valid metric-domain authority has NOT been created.

Creating one now would be a new normative governance act and requires an explicit pre-observation human decision.

## Consequences

No runtime modification is authorized.

The V0.5 sandbox breaker candidate remains non-governed.

No hardcoded rejection of `FOREIGN_METRIC` is authorized.

No numeric range for `SYNTHETIC_SCORE` may be invented.

`A0_ADVERSARIAL_BREAK_EXPANSION_V0_5 = BLOCKED_PENDING_METRIC_DOMAIN_GOVERNANCE`

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

## Next governed boundary

`A0 — SYNTHETIC PRODUCER METRIC-DOMAIN GOVERNANCE DECISION`

That boundary must decide, before any AF04 re-adjudication, whether to create a dedicated synthetic-producer metric-domain authority and, if so, explicitly freeze at minimum:

- authority identity/version;
- producer identity to which it applies;
- admitted metric identity or identities;
- numeric-domain semantics for each metric where required;
- measurement binding fields covered by the authority;
- fail-closed behavior for unknown metric identities/domains;
- relationship to the existing Source Profile and Global Normalization Policy;
- pre-observation status and hash/identity pinning;
- qualification tests and mutation family.

Until that decision is persisted and qualified:

- AF04 remains unadjudicable;
- V0.5 remains blocked;
- no ABF5 runtime correction is authorized;
- no A1/A2/DecisionPolicy/Decision/ACTION/trading/MT5/real-C01 authority is opened.
