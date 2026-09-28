# PHASE 20 — COST_MAP

Date: 2026-09-28  
Base HEAD: `f3e02454f4a3ea5bb133586141fe9d28656b348d`

## Measurement rule

No precise historical time ledger is persisted for the audited workflow. This document therefore does **not** invent minutes, hours, euros or percentages.

Cost labels are structural audit estimates:

- `LOW` — little recurring human work or cheap deterministic machine replay.
- `MEDIUM` — repeated artifact/test handling or non-trivial engineering.
- `HIGH` — repeated human coordination, broad requalification, or substantial manual evidence handling.
- `UNKNOWN` — insufficient evidence.

These are **DERIVED estimates**, not measured timings.

## Cost map

| Cost ID | Control/work family | Human cost | Machine / I/O cost | Recurrence | Evidence basis | Delay risk |
|---|---|---:|---:|---|---|---|
| C-01 | Fresh repo/branch/HEAD/TREE checks | MEDIUM if manual | LOW | every mutation boundary | repository safety rule | MEDIUM |
| C-02 | Protected blob verification | MEDIUM if manually enumerated | LOW | every governed cycle | E1 reports/checkpoint | MEDIUM |
| C-03 | Contract + breaker preregistration | MEDIUM | LOW | each new control | E1-04→E1-07 | MEDIUM |
| C-04 | Test-first RED | LOW human | LOW-MEDIUM | each new control | persisted RED reports | LOW |
| C-05 | Full breaker replay/re-break | LOW human when automated | MEDIUM | candidate + persisted HEAD | E1 qualification reports | LOW-MEDIUM |
| C-06 | Exact raw-data rehash | LOW human | MEDIUM-HIGH I/O | data qualification boundaries | E1-03: 61 parquet files | MEDIUM |
| C-07 | Independent reference implementation | MEDIUM-HIGH one-time | LOW recurring | only where independence needed | E1-06 | LOW recurring |
| C-08 | Report + checkpoint duplication | MEDIUM | LOW | every control cycle | repeated evidence text in checkpoint/reports | HIGH cumulative |
| C-09 | Per-mechanical-step human approvals | HIGH | negligible | historically frequent | accelerated-mode rationale explicitly targets coordination overhead | **HIGH** |
| C-10 | Macro authorization + hard STOP | LOW-MEDIUM | negligible | once/control + exceptional STOP | checkpoint §308 | LOW |
| C-11 | Human normative decision protocol with counter-expertise | HIGH when triggered | MEDIUM | only genuine normative choices | Decision Support boundary | Acceptable if conditional |
| C-12 | E1-07 preflight/trace | LOW after implementation | LOW | each actual E1 execution attempt | E1-07 qualification | LOW |
| C-13 | E1-08 one-shot authorization | LOW | negligible | once per authorized real run | current readiness design | LOW |
| C-14 | A0 V0.3 coverage-gap expansion | MEDIUM-HIGH | MEDIUM-HIGH | if reopened | 149-test surface + missing coverage families | HIGH if placed before E1 without necessity proof |
| C-15 | Obsidian manual projection | UNKNOWN; historically material by audit premise | LOW-MEDIUM | potentially frequent | not canonical on current branch | HIGH if made blocking |
| C-16 | Historical checkpoint re-reading | MEDIUM-HIGH if broad/manual | LOW | every conversation recovery | very large recovery checkpoint | HIGH cumulative |
| C-17 | Project Control Plane implementation | HIGH one-time | MEDIUM | Phase 22+ only | future plan | DEFERRED |
| C-18 | Paper/broker/live safety gates | LOW until reached | UNKNOWN later | later lifecycle | currently closed | None for present E1 |

## Highest-cost / lowest-immediate-information areas

```text
1. repeated human micro-authorizations
2. repeated manual identity enumeration
3. duplicated report + checkpoint prose
4. broad historical re-reading instead of compact machine-readable state
5. reopening deferred A0/Obsidian work before necessity is demonstrated
```

## High-value controls despite cost

The following controls impose work but directly protect the validity of the next experimental result:

- OOS/window freeze;
- exact raw/H1 data identity;
- execution/cost semantics;
- independent parity;
- exact persisted-HEAD replay;
- preflight and trace;
- explicit E1-08 authority.

Their cost alone is not evidence that they should be weakened.

## Missing metric

Phase 12's intended before/after human-cost measurement is not yet represented by a persistent command/time telemetry system. That becomes a measurement target for the later Project Control Plane pilot, not a reason to invent a number now.
