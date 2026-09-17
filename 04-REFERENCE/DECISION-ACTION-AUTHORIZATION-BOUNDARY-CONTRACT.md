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
6. `decision_id` must remain content-bound to the exact upstream identities and decision payload from which it was derived.
7. The boundary cannot accept a caller-supplied boolean, marker, tier, flag or self-declared `validated/authorized` field as proof of Decision authenticity.
8. No supported or module-level raw attestation/minter API may let normal callers mark arbitrary Decision instances as downstream-admissible.
9. `research_run_id` and `context_id` substitution must fail closed even when the substituted identifiers are individually well-formed.
10. Unknown, absent, malformed or incomplete authorization constraints must produce `BLOCKED`, never an implicit authorization.
11. A more permissive authorization state cannot be inferred from the mere existence of P1.0 or P1.1 code/contracts/tests.
12. P1.0 promotion-gate semantics remain authoritative for any future governance relaxation. P1.1 cannot bypass them.
13. `AUTHORIZED` means only "admissible to the next governed ACTION boundary". It does not mean "execute".
14. `BLOCKED` must be safe and side-effect free.
15. No acquisition, `.bi5` download, real backtest, broker call or live activation is permitted by P1.1.

### 5.1 Process-local trust model

The current attestation mechanism is a **process-local integrity mechanism**, not a sandbox against arbitrary code execution inside the same CPython interpreter.

For the current block-only candidate, the trusted computing boundary assumes that code executing inside the verifier process does not deliberately mutate verifier internals through reflective capabilities such as `__closure__`, closure-cell replacement, `__globals__`, monkeypatching or equivalent interpreter-level state manipulation.

Hostile or reflective mutation of verifier internals is classified as **process compromise**, not as an ordinary untrusted input crossing the P1.1 API.

This clarification does not convert process compromise into authorization. The current candidate MUST remain hard-blocked even when such reflective mutation is demonstrated.

**No positive `AUTHORIZED` path may be introduced while its security depends only on mutable process-local Python state exposed to potentially untrusted code.** Before any positive path exists, the authorization authority must either:

- execute inside an explicitly qualified isolated trust boundary with narrow inputs; or
- use another separately qualified attestation mechanism providing equivalent resistance to the caller threat model.

The current process-local registries therefore remain acceptable only for the block-only qualification and trusted-process object-integrity use case. They are not a future security token.

### 5.2 Identifier-security posture

The current `decision_id` and `constraint_id` use truncated SHA-256 identifiers for deterministic identity, not as standalone authorization proofs.

Their current 16-hex form MUST be requalified before any positive `AUTHORIZED`, persisted authorization token, cross-process authorization decision or adversarial external-input use. A positive path may require a larger collision-resistance budget.

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
- `B8` attempted access to any supported/module-level raw Decision attestation/minter API.

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

### G — Reflective process-compromise probes

These attacks are diagnostic probes against the process-integrity assumption, not evidence that pure-Python reflection is a supported P1.1 API.

- `G0` rebinding a module-level `BLOCKED` symbol must never produce an `AUTHORIZED`-looking verdict;
- `G1` direct manual construction of `AuthorizationVerdict(verdict="AUTHORIZED", ...)` must fail at runtime;
- `G2` monkeypatching the imported Decision verifier must still terminate in the block-only hard stop;
- `G3` reflective mutation of the Decision attestation registry must be demonstrable as process compromise and must never escape the block-only hard stop;
- `G4` reflective mutation of the constraint attestation registry must be demonstrable as process compromise and must never escape the block-only hard stop;
- `G5` a fully forged Decision + constraints chain created only through reflective process compromise must still terminate `BLOCKED / NO_GOVERNED_POSITIVE_AUTHORIZATION_POLICY` while the candidate remains block-only.

A future positive path must **change this expectation**: G3–G5 become hard blockers until the positive authorization authority is isolated or otherwise qualified against the caller threat model.

## 8. Positive-path boundary

The positive-path test fixture, when implemented, must be synthetic, local and side-effect free.

It may prove only that:

- an authentic producer-created Decision is recognized as authentic;
- explicit bounded authorization constraints are evaluated by the candidate boundary;
- the resulting verdict is structurally bound to the exact Decision and exact constraints;
- no ACTION is created or executed.

A successful P1.1 block-only test MUST NOT be interpreted as authorization to trade.

**The positive path itself remains BLOCKED until the process-compromise and identifier-security requirements in §5.1–5.2 are separately qualified.**

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

At the original baseline the boundary was expected to be **BLOCKED / not yet executable**, because:

- Decision downstream attestation was absent;
- no P1.1 authorization evaluator existed;
- no governed authorization-constraint object/protocol existed;
- no P1.1 adversarial qualification harness existed.

This is not a defect in the closed upstream blocks. It is the intentionally unopened downstream boundary.

## 11. Qualification rule

The **block-only P1.1 candidate** can become PASS only after:

`formalisation → candidate implementation → adversarial break → correction → re-break → protected upstream regression → persisted-HEAD re-break → verdict`

The candidate must remain fail-closed throughout qualification.

No green normal path, document existence or synthetic `AUTHORIZED` value is sufficient by itself.

A PASS of the block-only candidate does **not** qualify a positive authorization path. Positive `AUTHORIZED` remains separately BLOCKED until §5.1 and §5.2 have been satisfied.

## 12. Next governed action

For the current block-only phase:

1. preserve runtime-enforced `BLOCKED` semantics;
2. keep reflective process-compromise attacks G3–G5 visible as explicit limitations;
3. keep any future positive `AUTHORIZED` path blocked pending an isolated/equivalently strong authorization trust boundary and identifier requalification.

Only after those future prerequisites are separately governed may P1.1 be extended beyond block-only behavior.
