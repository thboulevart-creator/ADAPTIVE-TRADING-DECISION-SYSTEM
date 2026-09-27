# A0 — SYNTHETIC PRODUCER METRIC-DOMAIN RUNTIME BINDING MINIMAL IMPLEMENTATION — PERSISTED-HEAD RE-BREAK

Date: 2026-09-27

Reviewed governed HEAD:

`8630a512ad7abafed10783caf5165c61e095b534`

Runtime blob:

`1210bee06a2d9aed2ed7d9078542934ff430175c`

Standalone qualifier blob:

`9bd05f2a2a97f092c0fc2988319f15caff57dda3`

Frozen authority blob:

`dd205d3e7b4a522a5ba23cef1e665d51c196acb8`

Binding governance decision blob:

`82b399f06c41fa740a3676d0272cb39759911a7f`

Runtime-binding preregistration manifest blob:

`935661cbdf4dee031a738e37969baafa0a975d81`

Runtime-binding breaker blob:

`bcba5de33a73f9e32ff39e8fb498ab4d471af098`

Pre-persistence sandbox qualification run:

`36343261232`

Fresh persisted-head re-break run:

`36343390967`

## Persistence scope

The governed implementation commit modifies exactly:

`src/a0_research_authority.py`

The standalone qualifier, frozen authority, governance decisions, preregistered breakers and A0 V0.3 contract remain unchanged.

## Implemented binding

For the already-governed synthetic producer/source pair, A0 now:

1. resolves the metric-domain authority from the fixed governed repository path;
2. fails closed if that authority is missing, unreadable or byte-different;
3. invokes the already-qualified standalone qualifier for every present source-native measurement;
4. rejects measurements outside the frozen metric-domain authority;
5. ignores caller attempts to select, replace or disable the authority;
6. preserves existing Source Profile and Global Normalization Policy isolation;
7. adds to the canonical projection:
   - `metric_domain_authority_identity`;
   - `metric_domain_authority_sha256`;
   - `metric_domain_validation`.

No new permission, scientific-normalization, Decision or ACTION authority is created.

## Qualification

Sandbox candidate:

`127/127 PASS`

Fresh persisted-head re-break:

`127/127 PASS`

Composition:

```
previous frozen surface = 107/107 PASS
runtime-binding family RB00..RB19 = 20/20 PASS
TOTAL = 127/127 PASS
```

The previously observed RED groups are closed relative to the frozen 127-test surface:

- `A0-MDBIND-01` — binding trace absent;
- `A0-MDBIND-02` — mandatory governed authority resolution not enforced;
- `A0-MDBIND-03` — standalone qualifier not bound to source measurements.

## Verdict

`A0_METRIC_DOMAIN_RUNTIME_BINDING_MINIMAL_IMPLEMENTATION = PASS_127_OF_127`

`A0_METRIC_DOMAIN_RUNTIME_BINDING_MINIMAL_IMPLEMENTATION_PERSISTED_REBREAK = PASS_127_OF_127`

`A0_METRIC_DOMAIN_RUNTIME_BINDING_QUALIFICATION = PASS`

AF04 was not executed in this boundary.

## Authorization state

All preconditions defined by the binding-governance decision for a separate AF04 re-adjudication boundary are now satisfied:

- independent binding family preregistered before execution;
- binding candidate implemented without changing expectations;
- full frozen pre-existing suite preserved;
- fresh persisted-head re-break PASS.

Therefore:

`AF04_READJUDICATION_CURRENT_BOUNDARY = NOT_EXECUTED`

`AF04_READJUDICATION_NEXT_BOUNDARY = AUTHORIZED`

`ABF5_RUNTIME_CORRECTION = NOT_AUTHORIZED`

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

No conclusion about AF04 is asserted until it is separately re-run under the now-qualified authority/binding.

## Next governed boundary

`A0 — AF04 METRIC-DOMAIN GOVERNED RE-ADJUDICATION`

That boundary must:

- use the exact persisted runtime HEAD established here;
- use the exact frozen authority and qualified standalone qualifier;
- execute AF04 separately from the independent qualifier/binding families;
- preserve all 127 currently passing tests unchanged;
- classify AF04 from observed evidence as PASS / FAIL / BLOCKED;
- make no corrective runtime mutation before that classification;
- keep A1/A2/DecisionPolicy/Decision/ACTION/trading/MT5/real-C01 closed.
