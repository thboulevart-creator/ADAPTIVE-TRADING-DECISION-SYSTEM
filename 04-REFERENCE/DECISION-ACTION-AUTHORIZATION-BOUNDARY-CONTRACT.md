# P1.1 DECISION → ACTION AUTHORIZATION BOUNDARY — TIER-A CONTRACT V1

**Contract ID:** `P1_1_DECISION_ACTION_AUTHORIZATION_BOUNDARY_V1`  
**Status before qualification:** `BLOCKED`  
**Boundary:** `qualified Decision → pre-ACTION authorization verdict`  
**Tier:** `A`

## 1. Purpose

Close the smallest downstream boundary after `DECISION` without creating an ACTION engine, broker adapter, order model, sizing engine or standalone RISK service.

The boundary answers only:

> **May this exact qualified Decision be admitted to the future ACTION boundary under the exact applicable authorization constraints, or must it be blocked?**

P1.1 is Tier A because an erroneous positive verdict could eventually permit operational behavior. Therefore every unknown, incomplete, reconstructed, substituted, stale or unverifiable input must fail closed.

## 2. Governance alignment

The governed minimal system target remains:

`DATA → CONTEXT → RESEARCH / EXPERIENCE → DECISION → ACTION → RESULT → TRACE`

with the knowledge/governance loop:

`TRACE → MEMORY → AUDIT → REVISION → new RESEARCH / EXPERIENCE`.

P1.1 does **not** add an eleventh functional block named `RISK`.

Risk/cost control is treated here as a mandatory authorization property on the `DECISION → ACTION` boundary. A later implementation may use one or several mechanisms to satisfy that property, but this contract does not prescribe a standalone service, agent, process, database or engine.

## 3. Existing executable state

At the P1.0-closed integration baseline, `src/decision.py` defines an immutable `Decision` with:

- `decision_id`;
- `research_run_id`;
- `context_id`;
- `decision` payload.

`produce_decision(...)` validates factory-attested upstream research evidence and coherent Context before creating the Decision.

However, the produced `Decision` itself currently exposes no downstream proof that it came from the qualified producer path. A caller can instantiate `Decision(...)` directly with plausible fields.

Therefore the current `DECISION → ACTION` authorization boundary is **BLOCKED**.

## 4. Smallest authorized direction

The only admissible direction is conceptually:

`qualified producer-created Decision → identity/content verification → applicable authorization constraints → fail-closed authorization evaluation → AUTHORIZED | BLOCKED`

The P1.1 output is an authorization verdict only.

It MUST NOT create or execute an ACTION.

It MUST NOT create an order, position, broker request, lot size, stop loss, take profit, portfolio allocation or market-side effect.

## 5. Mandatory invariants

A future positive P1.1 authorization verdict MUST satisfy all of the following:

1. The boundary receives the full `Decision` object; `decision_id` alone is insufficient.
2. The Decision is proven to originate from the qualified `produce_decision(...)` producer path or an equivalently governed producer path explicitly qualified later.
3. Exact field reconstruction of a Decision cannot reproduce downstream admissibility merely because values are equal.
4. `copy.copy`, `copy.deepcopy`, dataclass replacement or equivalent silent reconstruction cannot preserve admissibility unless a future explicitly qualified persistence/reattestation protocol says otherwise.
5. Post-production mutation of `decision_id`, `research_run_id`, `context_id` or decision payload invalidates admissibility.
6. `decision_id` must remain cryptographically/content bound to the exact upstream identities and decision payload from which it was derived.
7. The boundary cannot accept a caller-supplied boolean, marker, tier, flag or self-declared `validated/authorized` field as proof of Decision authenticity.
8. No module-level raw attestation/minter capability may let callers mark arbitrary Decision instances as downstream-admissible.
9. `research_run_id` and `context_id` substitution must fail closed even when the substituted identifiers are individually well-formed.
10. Unknown, absent, malformed or incomplete authorization constraints must produce `BLOCKED`, never an implicit authorization.
11. A more permissive authorization state cannot be inferred from the mere existence of P1.0 or P1.1 code/contracts/tests.
12. P1.0 promotion-gate semantics remain authoritative for any future governance relaxation. P1.1 cannot bypass them.
13. `AUTHORIZED` means only "admissible to the next governed ACTION boundary". It does not mean "execute".
14. `BLOCKED` must be safe and side-effect free.
15. No acquisition, `.bi5` download, real backtest, broker call or live activation is permitted by P1.1.

## 6. Authorization-constraint rule

P1.1 does not yet define quantitative trading-risk semantics such as sizing, leverage, stop placement, portfolio exposure or daily drawdown.

Before any positive authorization path can be considered complete, the applicable authorization constraints must themselves be explicit, identifiable and bounded.

Until such constraints are supplied by a governed mechanism, uncertainty about them MUST resolve to `BLOCKED`.

This prevents P1.1 from becoming a hidden default-allow gateway while also avoiding premature construction of a standalone risk engine.

## 7. Required adversarial attack catalogue

P1.1 qualification must at minimum attack the following cases.

### A — Decision existence and type

- `A0` coherent producer-created Decision reaches the boundary without side effects;
- `A1` absent Decision (`None`);
- `A2` wrong object type;
- `A3` `decision_id` string supplied instead of the full Decision;
- `A4` dictionary/serialized fields supplied instead of the qualified object.

### B — Reconstruction and forgery

- `B0` direct manual `Decision(...)` reconstruction with exact valid fields;
- `B1` reconstruction with forged `decision_id`;
- `B2` reconstruction with valid-looking but foreign `research_run_id`;
- `B3` reconstruction with valid-looking but foreign `context_id`;
- `B4` dataclass `replace(...)` reconstruction;
- `B5` `copy.copy` reconstruction;
- `B6` `copy.deepcopy` reconstruction;
- `B7` caller-added/self-declared validation or factory marker;
- `B8` attempted access to any raw Decision attestation/minter capability.

### C — Post-production mutation

- `C0` mutate `decision_id` after valid production;
- `C1` mutate decision payload after valid production;
- `C2` mutate `research_run_id` after valid production;
- `C3` mutate `context_id` after valid production;
- `C4` mutate multiple fields while preserving superficially coherent values;
- `C5` mutate internal/private marker state if one exists.

### D — Identity/content substitution

- `D0` same payload with foreign research run;
- `D1` same payload with foreign context;
- `D2` same identifiers with altered payload;
- `D3` same `decision_id` reused for different content;
- `D4` valid Decision from one upstream chain rebound to another authorization request;
- `D5` stale Decision replayed outside its future declared admissibility envelope.

### E — Authorization-constraint failures

- `E0` constraints absent;
- `E1` constraints wrong type;
- `E2` constraints incomplete;
- `E3` unknown constraint field/value with permissive fallback attempt;
- `E4` caller asks to ignore or downgrade a failed constraint;
- `E5` caller supplies a precomputed `authorized=True` or equivalent bypass;
- `E6` conflict between constraints where precedence is undefined;
- `E7` stale or foreign constraints rebound to a valid Decision.

### F — Downstream bypass

- `F0` attempt to construct/emit ACTION directly from Decision without P1.1 authorization;
- `F1` attempt to treat `BLOCKED` as soft warning and continue;
- `F2` attempt to use DecisionTrace or another reconstruction artifact as authorization proof;
- `F3` attempt to infer authorization from P1.0 PASS/closure;
- `F4` attempt to infer acquisition, backtest or live permission from P1.1 state;
- `F5` any rejected Decision/constraint path followed by downstream ACTION construction must remain impossible in the P1.1 qualification harness.

## 8. Positive-path boundary

The positive-path test fixture, when implemented, must be synthetic, local and side-effect free.

It may prove only that:

- an authentic producer-created Decision is recognized as authentic;
- explicit bounded authorization constraints are evaluated by the candidate boundary;
- the resulting verdict is structurally bound to the exact Decision and exact constraints;
- no ACTION is created or executed.

A successful P1.1 test MUST NOT be interpreted as authorization to trade.

## 9. Explicitly out of scope

P1.1 does not implement or qualify:

- ACTION construction;
- broker/exchange connectivity;
- order submission;
- position sizing;
- leverage selection;
- stop-loss / take-profit logic;
- portfolio risk aggregation;
- daily/global loss limits;
- market/news filters;
- execution quality/slippage;
- RESULT production;
- TRACE/MEMORY/AUDIT completion;
- native USATECH acquisition;
- real-data backtest;
- live activation.

These require later separately governed boundaries.

## 10. Fail expectation before implementation

At the current baseline the boundary is expected to be **BLOCKED / not yet executable**, because:

- Decision downstream attestation is absent;
- no P1.1 authorization evaluator exists;
- no governed authorization-constraint object/protocol exists;
- no P1.1 adversarial qualification harness exists.

This is not a defect in the closed upstream blocks. It is the intentionally unopened downstream boundary.

## 11. Qualification rule

P1.1 can become PASS only after:

`formalisation → candidate implementation → adversarial break → correction → re-break → protected upstream regression → persisted-HEAD re-break → verdict`

The candidate must remain fail-closed throughout qualification.

No green normal path, document existence or synthetic `AUTHORIZED` value is sufficient by itself.

## 12. Next governed action

Determine and implement the **smallest candidate** that can satisfy this contract without constructing ACTION or a general risk engine.

The candidate design must first resolve two minimal responsibilities:

1. how a downstream consumer proves that a Decision is an authentic, unmodified output of the qualified producer;
2. what smallest explicit authorization-constraint representation is sufficient to prevent default-allow behavior while remaining independent of quantitative trading-risk policy.

Only after that candidate exists may A0–F5 be executed adversarially.
