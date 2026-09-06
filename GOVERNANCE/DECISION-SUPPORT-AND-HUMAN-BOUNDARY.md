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

## Mandatory adversarial falsification principle

The system MUST NOT optimize primarily for finding or confirming a plausible **correct answer**. For consequential architectural and qualification decisions, the primary analytical objective MUST also be to discover **where the current reasoning could be wrong**.

For every material candidate, recommendation, derived consequence, or proposed rule, the acting agent MUST actively attempt to falsify it before treating it as a viable basis for a decision. The analysis MUST ask, where applicable:

- **Where could we be wrong?**
- **Under what concrete conditions would this statement be false?**
- **What assumption, dependency, or interpretation could invalidate it?**
- **What can fail, break, become ambiguous, non-deterministic, non-reproducible, or semantically divergent?**
- **What evidence would disprove the current conclusion?**
- **What edge case or adversarial variant would expose a hidden weakness?**
- **Are we confusing an implementation convenience with a normative property?**
- **Are we silently relying on an unvalidated source, parser, ordering rule, identity mechanism, or convention?**
- **Could two independent implementations legitimately produce different results under the proposed rule?**
- **Could the proposed solution pass ordinary examples while failing reconstruction, reordering, duplicates, format changes, partitioning, insertion/deletion, restart, or other relevant adversarial conditions?**

A candidate MUST NOT be preferred merely because it works on nominal examples. Its failure modes, falsification conditions, and boundary conditions MUST be considered explicitly.

When a candidate survives adversarial analysis, that means only that the identified attacks did not falsify it; it does **not** by itself establish normative validity. Evidence, applicable contracts, and human decisions remain governed by the normal status discipline.

The same adversarial standard MUST be applied to the reasoning process itself. The acting agent MUST challenge its own conclusions rather than merely challenge alternatives. Claude and Grok responses MUST likewise be examined for possible errors rather than treated as confirmation.

This principle is intended to create progressive convergence toward robust architecture through elimination of incorrect reasoning, not through premature confidence in a supposedly correct answer.

## Mandatory three-way decision protocol

Whenever a **genuine human normative decision** is reached, the acting agent MUST use the following protocol before requesting the human decision, unless independent counter-expertise is demonstrably unavailable or materially unnecessary for the specific decision.

```text
1. STOP AUTONOMOUS INFERENCE
2. FORMULATE THE PRECISE DECISION QUESTION
3. OBTAIN AN INDEPENDENT CLAUDE RESPONSE
4. OBTAIN AN INDEPENDENT GROK RESPONSE
5. RETAIN AN INDEPENDENT INTERNAL ANALYSIS
6. PERFORM A THREE-WAY ADVERSARIAL COMPARISON
7. PRODUCE A SYNTHESIS / DECISION BRIEF
8. HUMAN MAKES THE NORMATIVE DECISION
9. PERSIST DECISION + RATIONALE + SCOPE IN GOVERNANCE
10. RESUME AUTONOMOUS EXECUTION
```

The three-way comparison MUST explicitly examine, where applicable:

- convergence and divergence between the analyses;
- hidden assumptions and dependencies;
- possible factual or logical errors;
- **where each analysis may be wrong and under what conditions**;
- **what could fail or not work, and why**;
- concrete falsification conditions and adversarial counterexamples;
- architectural consequences and failure modes;
- facts/evidence versus validated rules;
- derived consequences versus genuinely normative choices;
- proposals/hypotheses that must not be silently promoted;
- remaining trade-offs and reversibility;
- compatibility with authoritative contracts, adjudications, invariants, and gates.

Claude and Grok are **independent counter-expertise**, not normative authorities. Their recommendations MUST NOT be promoted to repository policy merely because they agree with one another. The acting agent's own analysis MUST remain independent rather than being retrofitted to match either response.

The human MUST receive the synthesized decision boundary and enough explanation of the competing consequences to make an informed normative choice. The acting agent MUST NOT silently select the normative outcome.

After the human decision, the resulting normative rule MUST be recorded with sufficient provenance to identify at least:

- the decision question;
- the accepted decision;
- the decision rationale;
- the applicable repository/scope;
- the evidence and counter-expertise used;
- relevant alternatives rejected or left unresolved;
- the effective contract/version or artifact affected;
- any residual uncertainty or follow-up condition.

The decision MUST then be treated according to the repository's normal evidence, adjudication, versioning, and audit rules. Recording a decision does not by itself make an implementation conforming; downstream validation remains mandatory.

If independent counter-expertise is unavailable, the absence MUST be recorded rather than simulated. A fabricated or assumed Claude/Grok response MUST NEVER be used as evidence.

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
ADVERSARIAL FALSIFICATION
    ↓
INDEPENDENT COUNTER-EXPERTISE (when useful)
    ↓
THREE-WAY ADVERSARIAL COMPARISON
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
