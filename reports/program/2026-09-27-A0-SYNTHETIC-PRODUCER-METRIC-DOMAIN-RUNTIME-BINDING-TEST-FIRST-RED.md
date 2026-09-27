# A0 — SYNTHETIC PRODUCER METRIC-DOMAIN RUNTIME BINDING TEST-FIRST RED

Date: 2026-09-27

Persisted preregistration HEAD:

`e0320d5df64d39ad1386382efc197b1ae9739ecc`

Binding governance decision blob:

`82b399f06c41fa740a3676d0272cb39759911a7f`

Runtime binding manifest blob:

`935661cbdf4dee031a738e37969baafa0a975d81`

Runtime binding breaker blob:

`bcba5de33a73f9e32ff39e8fb498ab4d471af098`

Frozen authority blob:

`dd205d3e7b4a522a5ba23cef1e665d51c196acb8`

Standalone qualifier blob:

`9bd05f2a2a97f092c0fc2988319f15caff57dda3`

Execution run:

`36342749521`

## Ordering proof

The RB00..RB19 integration family was persisted on the governed branch before its first execution.

No runtime binding implementation was present when the breaker was frozen.

AF04 remained excluded. The AF04 observed metric literal is absent from the breaker.

## Preserved frozen surface

`107/107 PASS`

No existing A0 or standalone metric-domain test was modified.

## Runtime-binding RED result

```
TOTAL = 20
PASS = 4
FAIL = 16
```

PASS:

- RB08 — bool metric value remains fail-closed;
- RB09 — numeric-string metric value remains fail-closed;
- RB13 — Source Profile metric-domain widening attempt fails closed;
- RB14 — Global Normalization Policy metric-domain takeover fails closed.

FAIL:

- RB00;
- RB01;
- RB02;
- RB03;
- RB04;
- RB05;
- RB06;
- RB07;
- RB10;
- RB11;
- RB12;
- RB15;
- RB16;
- RB17;
- RB18;
- RB19.

## Consolidated integration defect groups

### A0-MDBIND-01 — binding trace absent

Current A0 projections do not represent the frozen metric-domain authority identity/hash/validation mapping.

Observed by:

RB00, RB01, RB07, RB10, RB11, RB15, RB16, RB17, RB18, RB19.

### A0-MDBIND-02 — mandatory governed authority resolution not enforced

For the applicable synthetic producer/source pair, A0 still derives an authoritative projection when the frozen authority is missing, corrupt or byte-different.

Observed by:

RB02, RB03, RB04.

### A0-MDBIND-03 — standalone metric-domain qualifier not bound to source measurements

Unknown/case-mutated metric identities and caller bypass attempts can still reach an A0 projection because the already-qualified standalone metric-domain validator is not invoked by A0.

Observed by:

RB05, RB06, RB12.

## Interpretation of the four PASS cases

The four passing cases do not establish runtime binding.

They are already blocked by pre-existing A0 protections:

- strict numeric parsing rejects bool/numeric-string values;
- Source Profile structural authority rejects unrecognized widening fields;
- Global Normalization Policy structural authority rejects takeover fields.

## Verdict

`A0_METRIC_DOMAIN_RUNTIME_BINDING_TEST_FIRST_RED = PASS_RED_PROFILE_ESTABLISHED`

`A0_EXISTING_107 = PASS_UNCHANGED`

`A0_METRIC_DOMAIN_RUNTIME_BINDING = NOT_IMPLEMENTED`

`A0_METRIC_DOMAIN_RUNTIME_BINDING_QUALIFICATION = NOT_YET`

`AF04_READJUDICATION = NOT_AUTHORIZED`

`ABF5_RUNTIME_CORRECTION = NOT_AUTHORIZED`

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

## Next governed boundary

`A0 — SYNTHETIC PRODUCER METRIC-DOMAIN RUNTIME BINDING MINIMAL IMPLEMENTATION CANDIDATE`

That boundary may modify only the minimum runtime integration necessary to close A0-MDBIND-01..03 while preserving all existing 127 tests unchanged:

```
previous frozen surface = 107
runtime-binding family = 20
TOTAL = 127
```

Constraints:

- keep RB00..RB19 unchanged;
- keep the previous 107 tests unchanged;
- keep `src/a0_metric_domain_authority.py` unchanged;
- keep the frozen authority unchanged;
- do not execute AF04 as an adjudication test;
- do not open A1/A2/DecisionPolicy/Decision/ACTION/trading/MT5/real-C01.
