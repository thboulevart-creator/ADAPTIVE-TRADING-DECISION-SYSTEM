# Q — ADVERSARIAL BREAK OF FIRST NATIVE-BI5 QUALIFICATION CONTRACT CANDIDATE

**Date:** 2026-09-19  
**Candidate commit under attack:** `02d329bb2fa419b2fa48635787596d4bce73a9e3`  
**Candidate artifact:** `reports/data-qualification/q_native_bi5_qualification_contract_candidate_2026-09-19.md`

No acquisition, BI5 download, real-data read, freeze implementation or backtest occurred.

## 1. Attack basis

The candidate was attacked against:

- corrected/re-broken D/R/M candidate;
- corrected/re-broken B/A candidate;
- Q-RM-02 cardinality separation;
- Q-RM-04 failure-scope semantics;
- Q-RM-05 acquisition completeness;
- Q-RM-07 qualification-before-freeze;
- strict duplicate preservation;
- no canonical enumeration;
- no temporal authority;
- no silent repair.

---

# 2. Acquisition-level attacks

## Q-A01 — late QUALIFICATION BLOCKED after valid prefix

Attack:

Many components/candidates succeed, then one declared component produces `QUALIFICATION BLOCKED`.

Required:

No partial/prefix qualified universe.

Candidate result:

**SURVIVES.**

One blocking A outcome forces whole Q to `QUALIFICATION_BLOCKED` and no normative U.

## Q-A02 — future acquisition-fatal A outcome

Attack:

A compatible future A version explicitly marks one anomaly acquisition-fatal.

Candidate result:

**SURVIVES.**

Q reserves `ACQUISITION_REJECTED` and does not invent acquisition-fatality itself.

## Q-A03 — missing D component with otherwise valid prefix

Candidate result:

**SURVIVES.**

Incomplete D materialization blocks the whole qualification.

## Q-A04 — undeclared component silently ignored

Candidate result:

**SURVIVES.**

A02 blocks; Q cannot silently discard and continue.

---

# 3. Membership / duplicate attacks

## Q-A05 — strict duplicate payloads from distinct source slots

Attack:

Two B candidates have identical logical payloads but distinct component/slot provenance.

Candidate result:

**SURVIVES.**

Both remain retained.

## Q-A06 — same source slot emitted twice

Attack:

Implementation accidentally emits the same `(component_manifest_entry_id, component_local_slot_index)` twice.

Candidate result:

**SURVIVES.**

Q blocks as implementation/conformance duplication without promoting the physical locator to final observation identity.

## Q-A07 — same source slot both candidate and rejected

Attack:

One B report presents a valid candidate for slot S while A also says S is `REJECT RECORD`.

Candidate result:

**SURVIVES conceptually.**

Q blocks contradiction.

However this attack exposes that the candidate does not yet formally require every A record-level outcome to carry an exact target locator compatible with the B framing domain. This becomes Q-F01 below.

---

# 4. Layering attacks

## Q-A08 — hidden rejection of zero/crossed price

Candidate result:

**SURVIVES.**

Q V0.1 explicitly has no market-value filter.

## Q-A09 — hidden rejection of finite negative volume

Candidate result:

**SURVIVES.**

Finite decoded value is retained under Q V0.1.

## Q-A10 — timestamp regression sorted/rejected

Candidate result:

**SURVIVES.**

Q neither sorts nor rejects by traversal-relative timestamp.

## Q-A11 — warmup silently dropped

Candidate result:

**SURVIVES.**

D-member warmup candidates are retained.

## Q-A12 — evaluation interval changed by Q

Candidate result:

**SURVIVES.**

Q does not redefine the performance-evaluation interval.

## Q-A13 — Q invents canonical identity

Candidate result:

**SURVIVES.**

No canonical position/global ordinal/content ID is created.

## Q-A14 — Q overrides A outcome

Candidate result:

**SURVIVES.**

A outcomes are consumed; Q cannot downgrade BLOCKED to local reject or repair.

## Q-A15 — Q repairs B value

Candidate result:

**SURVIVES.**

No clipping/sorting/deduplication/value repair is authorized.

---

# 5. Demonstrated defect Q-F01 — ANOMALY_TARGET_BINDING_UNDERSPECIFIED

Attack:

A produces two local `REJECT RECORD` events for one component, but the events identify targets only by free-text diagnostics or ambiguous "record number" values.

Implementation A associates the first reject with physical slot 7.

Implementation B associates the same anomaly evidence with physical slot 8.

All other B candidates are identical.

Both implementations can claim they consumed the same A outcome category, yet they retain different occurrence universes.

The candidate currently says:

```text
reject_record_policy
= EXCLUDE_ONLY_NORMATIVELY_TARGETED_PHYSICAL_RECORD_OR_FRAGMENT
```

but does not define what makes the target **normatively exact**.

This leaves a membership-changing relation implementation-dependent.

Result:

**BREAK — Q-F01.**

Required correction:

Every A outcome consumed by Q must be bound to an exact declared target domain.

At minimum:

### Record/slot-local anomaly target

```text
component_manifest_entry_id
+
component_local_slot_index
```

for a complete fixed-width slot.

### Terminal-fragment target

```text
component_manifest_entry_id
+
terminal_fragment_start_offset
+
terminal_fragment_length
```

where the offset/length are B-framing facts, not canonical observation identity.

### Component/acquisition anomaly target

explicit component or acquisition scope identifier.

Free-text, traversal index, filename, parser row number, or diagnostic ordering is insufficient.

The target locator is anomaly/provenance evidence only and is not promoted to final observation identity.

---

# 6. Demonstrated defect Q-F02 — PHYSICAL_SLOT_ACCOUNTING_NOT_TOTAL

Attack:

One component decompresses into 100 complete 20-byte slots.

A conforming-looking implementation reports:

```text
98 B candidate occurrences
1 A REJECT RECORD slot
no blocking anomaly
```

Slot 57 is silently omitted from both the candidate set and anomaly registry.

Current Q input requires "all B candidate occurrences" and "all rejected diagnostics", but it does not state an independently checkable conservation rule tying them to B's complete-slot framing.

Q may therefore return `QUALIFIED` over 99 accounted slots even though B framing established 100 complete physical slots.

This silently destroys one potential occurrence and violates Q-RM-02/Q-RM-07 completeness.

Result:

**BREAK — Q-F02.**

Required correction:

For each fully decoded component whose framing is not globally blocked, Q must require an exact physical accounting invariant.

For B V0.1:

```text
complete_slot_indices
=
candidate_slot_indices
DISJOINT UNION
record_reject_slot_indices
```

subject to:

- no duplicate index in either side;
- no index outside `0 .. complete_slot_count-1`;
- no slot simultaneously candidate and rejected;
- terminal partial fragment, when present, is accounted separately and is not a complete slot;
- component-level BLOCKED outcome prevents qualified accounting/freeze for the acquisition.

Thus every complete fixed-width physical slot is accounted for exactly once before Q can be `QUALIFIED`.

This is a Q conformance check over B/A outputs, not a new B framing rule.

---

# 7. Other adversarial cases

## Q-A16 — content-hash deduplication

**SURVIVES.**

Payload equality cannot collapse distinct source occurrences.

## Q-A17 — traversal-order dependence

**SURVIVES.**

Membership is order-independent.

## Q-A18 — blocked acquisition still emits a "retained count"

Candidate already says no normative retained-universe count may be presented when blocked.

**SURVIVES.**

## Q-A19 — upstream version mismatch

**SURVIVES.**

Exact tuple mismatch blocks.

## Q-A20 — permission leakage

```text
Q candidate exists
→ acquisition or backtest authorized
```

is explicitly forbidden.

**SURVIVES.**

---

# 8. Market-quality policy attack

Q V0.1 deliberately retains deterministic finite decoded values such as:

- zero price;
- crossed quote;
- finite negative source volume.

This is a concrete membership policy, not an omission.

The authoritative corpus currently does not provide a frozen project-specific rule proving that these values must be excluded from the universal qualified tick universe.

Therefore the adversarial break does **not** silently insert such a filter.

A future consumer eligibility or new Q version may impose an explicit rule if justified.

**NO BREAK.**

---

# 9. Verdict

The first persisted Q candidate is not promoted.

```text
Q FIRST CONCRETE QUALIFICATION CONTRACT CANDIDATE
FAIL
```

Demonstrated defects:

1. `Q-F01 — ANOMALY_TARGET_BINDING_UNDERSPECIFIED`
2. `Q-F02 — PHYSICAL_SLOT_ACCOUNTING_NOT_TOTAL`

No D/R/M/B/A mutation is authorized.

No runtime mutation is authorized.

No acquisition is authorized.

## 10. Authorized minimal correction

Correct only Q:

1. define exact A target-binding forms for slot, terminal fragment, component and acquisition scopes;
2. reject filename/free-text/runtime-order targeting;
3. add exact per-component complete-slot conservation/accounting invariant;
4. require disjoint, exhaustive candidate-vs-record-reject slot accounting before `QUALIFIED`;
5. keep terminal fragments outside complete-slot count;
6. preserve no-partial-universe behavior.

Then persist and re-break the corrected Q candidate before any F/O work.
