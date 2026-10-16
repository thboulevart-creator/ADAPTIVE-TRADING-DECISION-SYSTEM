# ATDS-EA-02-D1-CR1 — TARGETED REQUALIFICATION V0.1

**Date:** 2026-10-16
**Authorization:** HUMAN_AUTHORIZED — ATDS-EA-02-D1-CR1 V0.1
**Final verdict:** QUALIFIED_CANDIDATE_FOR_HUMAN_REVIEW — SYNTHETIC-ONLY; NOT ADOPTED
**Scope:** Correct F01–F05; RED → GREEN → NON-REGRESSION → ADVERSARIAL RE-BREAK.
**Safety:** No MT5, no EX5, no real market observations, no backtests, no capital, no commits/push/merge/reset.

## 1. Canonical identity and worktree preflight

- Repository: thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM
- Governed branch: integration/system-v1.
- Immutable D1 worktree parent HEAD: 91fc53c406c67acde340599cb0ba35fd5347b02d.
- Parent TREE: c9274ca4f91c5b51d60aad2c607a8528c4f05027.
- Detached worktree: C:\Users\Boulevart\Documents\ATDS-EA-02-D1-ISOLATED.
- Local governed branch HEAD observed before and after: 9ed38d72580635d9a63eff76cf6196123be2d8a1.
- Nine D1 files present with preflight SHA-256 matching the prior verified checkpoint; no competing modifications, and CR1 report target did not exist.
- Files from other ATDS workstreams and tracked HEAD remained untouched.

## 2. RED — proven failures of uncorrected D1

Eleven newly added tests were run against original D1 implementations before any production correction.

- 11 executed; 8 FAIL and 3 ERROR. Expected RED status: 0/11 PASS.
- F01 observed deal profit changed from 0.00 to 999999.99 without source hash change and floating PnL forged: no source-value mismatch raised.
- F02 two distinct deals shared one raw source-record reference: no cardinality conflict raised.
- F03 negative/zero DEAL volumes and nonsensical direction: accepted.
- F04 unhashable source reference, unhashable claim and non-finite extension: uncontrolled TypeError/ValueError.
- F05 unattested negative-price semantics and source-bound nonnegative minimum: not distinguished.
- No original unit test was deleted or disabled.

## 3. Targeted corrections

### F01 — source-to-observation value binding
File: src/ea_observation/provenance.py; synthetic fixture updated.
- The raw synthetic records now contain independent source field values (order/deal/position/account/context) rather than only descriptive tags.
- Source hashes bind these synthetic values; each directly observed record is compared against its matching source values including economic fields, time and source sequence.
- A changed normalized value without a matching raw source generates SOURCE_VALUE_MISMATCH.
- A missing expected raw value generates SOURCE_VALUES_MISSING.
- A claimed deterministic derivation with only a self-declared rule is not treated as qualified; it generates DERIVATION_RULE_UNQUALIFIED.
- Hypothesized/unobserved deal profit is never included in the synthetic realized-gross sum.

### F02 — source-record cardinality
File: src/ea_observation/validation.py.
- Raw source records may feed only one distinct observed event/snapshot in D1.
- Exact event reimport (same ID and bytes) remains idempotent.
- Reuse for another distinct event/snapshot generates SOURCE_RECORD_CARDINALITY_VIOLATION.
- A future qualified one-to-many transformation requires a separately authorized, verifiable derivation; not silently supported in D1.

### F03 — numeric and accounting semantics
File: src/ea_observation/validation.py.
- DEAL BUY/SELL only; DEAL volume strictly positive, finite exact decimal.
- POSITION volume strictly positive; invalid sizes get dedicated errors.
- Source sequence is bound to its synthetic source record.
- Unknown commissions/currency remain unknown; no conversion to fabricated zeros.
- Existing bounded synthetic partial-close, HEDGING/NETTING and cash-flow separation preserved.

### F04 — malformed input fail closed
File: src/ea_observation/validation.py.
- The public validate_batch entrypoint catches anticipated malformed-input type, value, key, numeric and recursion exceptions and returns a stable result: overall_status FAIL, errors INVALID_INPUT, all authorities false.
- Malformed source IDs, claims, references or non-finite fields do not produce an unhandled exception on tested cases.
- Synthetic false-valued EA run attestations now require native Boolean True, not a truthy string.
- When structural violations exist, synthetic realized gross is suppressed rather than returned alongside FAIL.

### F05 — instrument-aware price semantics
File: src/ea_observation/validation.py.
- No universal rule that prices must be positive.
- A negative price with no qualified instrument-price specification produces PRICE_SEMANTICS_UNATTESTED; economics remain out of D1.
- An explicit synthetic instrument minimum is honored only if symbol/source/record match a source-bound INSTRUMENT_SPEC record.
- A negative price below attested minimum yields PRICE_BELOW_ATTESTED_MINIMUM; a negative price within a matching negative-minimum specification is allowed.
- Missing, forged or inconsistent instrument attestation yields INSTRUMENT_PRICE_SPEC_UNATTESTED.

## 4. GREEN and historic non-regression

After targeted production corrections and source-consistent synthetic fixture adjustments:
- Intermediate GREEN: 55/55 PASS, 0 FAIL, 0 ERROR.
- Original D1 suite: T01–T26 (26) and B01–B18 (18), all retained and PASS.
- RED additions: 11 mandatory CR1 regression tests, now PASS.
- Further recorded re-break regressions: 10 tests, PASS.
- Final command: py -B -m unittest discover -s tests -p 'test_ea_observation_*.py' -q
- Final outcome: **65/65 PASS, 0 FAIL, 0 ERROR**.
- PYTHONDONTWRITEBYTECODE=1. Tests entirely local and synthetic.

Some historically valid fixtures were made source-consistent without weakening their original assertions:
- New deals and cash flows receive new raw source records and updated hashes.
- Position-volume, direction, timestamp and commission variations used for intended non-error scenarios update synthetic raw evidence.
- The HEDGING multiple-position scenario uses a distinct raw source reference.
- Historical expected pass/block/fail assertions remain.

## 5. Independent adversarial re-break

A separate set of ten vectors, not restricted to the original GREEN test inputs, probed the corrected candidate.

Initial re-break: 6/10 behaved safely; four newly exposed bypasses were found (fabricated derived profit, inferred profit counted as observed, zero position size, truthy-string EA isolation flag).

Targeted hardening of those findings followed by complete retest:
- REB01 mutated commission: PASS, SOURCE_VALUE_MISMATCH.
- REB02 mutated account equity: PASS, SOURCE_VALUE_MISMATCH.
- REB03 record reference replaced by EA binding reference: PASS, source type mismatch.
- REB04 source field values removed followed by recomputed source hash: PASS, SOURCE_VALUES_MISSING.
- REB05 fabricated derivation/large profit: PASS, DERIVATION_RULE_UNQUALIFIED, gross suppressed.
- REB06 inferred large profit: PASS, treated as partial descriptive only; gross suppressed.
- REB07 zero-volume position: PASS, INVALID_POSITION_VOLUME.
- REB08 forged string "true" for isolated EA: PASS, UNPROVEN_EXACT_ATTRIBUTION.
- REB09 malformed source ID object: PASS, FAIL/INVALID_INPUT.
- REB10 non-finite cost value: PASS, controlled FAIL.
- **Final independent vectors: 10/10 PASS.**

This is a targeted adversarial re-break by the implementation/review agent, not an external independent third-party audit.

## 6. Modified file list and SHA-256 (after corrections)

- src/ea_observation/provenance.py
  1B046FF855964B97CB50919E96BE41B61FD4987F5ADD88EFF9CBF2C246300C2C
- src/ea_observation/validation.py
  DED3C41F1AF3243F854797BF9D1214CFB6F73D644E0AC475E4A6DE660EC822CD
- tests/test_ea_observation_schema.py
  1C4C22893579319A6399BEA27B732BF5ED6EAD2FA82945158C10DA1943B1EE54
- tests/test_ea_observation_validation.py
  AC556EA25FDF54397DD69958052AA754382060B8B7974917E115DB9F2BC7656F
- tests/fixtures/ea_observation_synthetic_v0_1.json
  4144DA4AF92F438BC6503BE540A730884D1606572F7B23D62EC8B4147A37E3AC

New CR1 report: reports/program/ATDS-EA-02-D1-CR1-TARGETED-REQUALIFICATION-V0.1.md (hash to be taken from final filesystem verification; self-hash not embedded here).

Protected, unchanged and checked against preflight:
- docs/ATDS-EA-02-D0-CONSOLIDATED-CONTRACT-V0.2.md — FC7839E6DFF6725E01686AFF4B482C040F9B63823959E3B45370AD93C1AA2283.
- src/ea_observation/__init__.py — DC9252C7FC82756ED2BFBBFCCB8FDD5489B7050AB5D17308B210092523B54D8F.
- src/ea_observation/schema.py — 749BA607E0AEE10F1E4A74B605732BDDCBE6BD8A2977796AA7F70F872BD76A24.
- reports/program/ATDS-EA-02-D1-SYNTHETIC-QUALIFICATION-V0.1.md — C337A551A2AA571FC556E92AAFAF9269F49F5B842BFA10BB8C9923869452169C.

## 7. Residual limitations and no-claim rules

- The source binding attests consistency against an embedded SYNTHETIC record and synthetic hash. It does NOT prove real exchange/terminal data authenticity; an attacker able to replace both synthetic source and checksum can still mint a different self-consistent fixture. Real-byte attestation is a separate future requirement.
- Derived observations remain blocked until rule execution and provenance are independently qualified. A rule_id alone is insufficient.
- Source cardinality presently supports only one-to-one or exact reimport, not general verified transformations.
- The instrument bound only demonstrates synthetic min-price compatibility, not tick, symbol contract, spread, margin or all broker price rules.
- Exact EA attribution here is a synthetic fixture assertion and does not prove attribution in a shared live account.
- No EA source code was recovered, no EX5 loaded and no MT5 history imported.
- No true net profitability, portfolio drawdown, continuous equity path, real cost-model, scientific edge or execution permission was evaluated.
- D0 architecture and existing CORE-02, WER-05, B11/B12 contracts were preserved.

## 8. Recommendation and STOP

Recommendation: **QUALIFIED_CANDIDATE_FOR_HUMAN_REVIEW** as a strictly synthetic, nonoperational source-bound validator. The known F01–F05 attacks and re-break vectors are blocked under the demonstrated tests. Human technical adoption or further independent expert review is a separate decision.

CR1 does not authorize a commit, push, merge, reset, MT5 operation, EA-03 start or capital deployment.

**STOP — CR1 COMPLETED FOR HUMAN REVIEW; GOVERNED BRANCH UNCHANGED.**
