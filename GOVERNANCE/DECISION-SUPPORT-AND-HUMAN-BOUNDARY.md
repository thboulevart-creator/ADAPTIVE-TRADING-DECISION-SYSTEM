# Decision Support and Human Boundary

## Status

**NORMATIVE GOVERNANCE RULE — USER-DIRECTED**

This rule governs how increasingly complex architectural and qualification questions are handled when they arise while pursuing the repository's final system objective.

## Purpose

The system's objective may remain clear while the intermediate architectural questions become progressively more technical, abstract, or consequential. The person responsible for the final objective must not be expected to invent normative technical answers merely because a later step requires them.

The methodology MUST therefore separate:

1. the **final objective**, which provides the purpose and acceptance direction;
2. the **technical investigation**, which determines what architectures and properties can satisfy that objective;
3. the **adversarial verification**, which attempts to falsify candidate solutions and exposes hidden consequences;
4. the **human normative decision**, which is required only when the evidence does not uniquely determine the choice.

## Mandatory operating rule

When an architectural question becomes sufficiently complex that an uninformed answer could introduce an incorrect normative decision, the acting agent MUST NOT ask the human to guess or improvise the technical answer.

Instead, the acting agent MUST, as far as possible:

1. derive the requirements imposed by the final objective;
2. identify the actual architectural decision boundary;
3. investigate viable candidate architectures and their consequences;
4. obtain independent counter-expertise when useful, including from independent agents such as Claude or Grok;
5. perform an adversarial comparison against the repository's existing contracts, adjudications, invariants, and qualification gates;
6. distinguish facts, validated rules, derived consequences, proposals, hypotheses, and unresolved questions;
7. produce a concise human decision only when a genuine normative choice remains.

The human MUST NOT be required to select a technical mechanism without first being given enough explanation to understand what the alternatives mean for the final objective.

## Decision boundary

A question is a **genuine human normative decision** when the available evidence, contracts, and adversarial analysis do not uniquely determine the required architectural choice and selecting among the remaining alternatives would establish or change a normative rule.

Until that boundary is reached, the agent SHOULD continue the investigation autonomously.

If the boundary is reached, the agent MUST NOT silently choose a normative answer on behalf of the human.

## Evidence and status discipline

Increasing technical complexity MUST NOT be treated as evidence that a particular answer is correct.

The following distinctions MUST remain explicit:

- **FACT / EVIDENCE** — directly established by authoritative repository evidence or reproducible observation.
- **VALIDATED RULE / INVARIANT** — explicitly adjudicated and authoritative for its stated scope.
- **DERIVED CONSEQUENCE** — logically follows from validated premises without introducing a new normative choice.
- **PROPOSAL / HYPOTHESIS** — candidate reasoning that has not been normatively adopted.
- **BLOCKED** — a required input, proof, or decision is missing.
- **HUMAN DECISION REQUIRED** — a normative choice remains after the technical and adversarial analysis has been performed.

No proposal, hypothesis, plausible recommendation, or BLOCKED item may be promoted to PASS or normative status merely because it appears reasonable.

## Objective-first method

For consequential architectural questions, the preferred sequence is:

```text
FINAL OBJECTIVE
    ↓
REQUIRED PROPERTIES / CONSTRAINTS
    ↓
ARCHITECTURAL CANDIDATES
    ↓
ADVERSARIAL ANALYSIS
    ↓
INDEPENDENT COUNTER-EXPERTISE (when useful)
    ↓
COMPARISON AGAINST AUTHORITATIVE CONTRACTS
    ↓
RECOMMENDATION / REMAINING TRADE-OFFS
    ↓
HUMAN NORMATIVE DECISION (only if genuinely required)
```

This sequence MUST be preferred over asking the human to answer increasingly technical sub-questions one by one without first establishing their relationship to the final objective.

## Scope and provenance

This rule applies to architectural, qualification, identity, data-model, determinism, provenance, and other consequential decisions in this repository where an incorrect intermediate choice could invalidate downstream qualification or system behavior.

It does not authorize any specific technical architecture by itself. It defines the decision-making method only.

Any concrete architectural choice remains subject to the repository's applicable contracts, adjudications, evidence requirements, and governance rules.
