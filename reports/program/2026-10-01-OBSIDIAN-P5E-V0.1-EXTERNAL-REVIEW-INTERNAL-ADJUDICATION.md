# P5-E V0.1 — EXTERNAL REVIEW INTERNAL ADJUDICATION

Date: 2026-10-01

## Scope

This record adjudicates the user-supplied external adversarial review of
`P5-E — END-TO-END NEAR-REAL-TIME QUALIFICATION V0.1`.

External review verdict: `FAIL`.

This record does not adopt the external review automatically. Each blocking finding was checked against the current candidate on the governed branch.

Opening branch:

`feat/obsidian-projection-p5e-end-to-end-near-real-time-qualification-v0.1`

Opening HEAD:

`4ffe259c2485437b5d782be633e1ba23985d4945`

Worktree at opening: `CLEAN`.

## Candidate identity

Contract blob:

`e5c3d7a9d451aba65e8062078c6c10d23e586f39`

Synthetic model blob:

`8662dd97a1c8a1af33d6593ae923384e96404b5a`

Base test blob:

`2305e0768182d82657c34a7cb53c502714a2ab81`

Adversarial test blob:

`6235c4b2addc16acd043832664440ec76f6dada2`

P5-D4 runtime blob:

`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

The candidate technical blobs are unchanged from the external-review packet.

## B1 — coverage and claim overreach

Adjudication:

`CONFIRMED_BLOCKING_WITH_UPSTREAM_COVERAGE_NUANCE`

Local mutation probes confirmed that the P5-E adversarial invariant function accepts critical mutations including:

- NON_FAST_FORWARD result changed to automatic continuation;
- UNKNOWN automatic-continuation guard disabled;
- SAME-head queue-growth guard disabled;
- queue-capacity no-mutation guard disabled;
- synthetic clock changed to WALL_CLOCK;
- observer governance-authority flag enabled;
- P6 closure flag disabled;
- the complete required-breaker list replaced by fictitious names.

However, several behavioral requirements already have executable upstream coverage in qualified P5-D2/P5-D4 surfaces.

Examples:

- SAME-head queue NOOP and no growth:
  `tests/obsidian_projection/test_observer_tick.py`
  blob `9c472a39e3d8eed8cf6cfc910bce27ee5fac7c58`;
- NON_FAST_FORWARD and UNKNOWN block without queueing:
  same test blob;
- newer FAST_FORWARD does not retarget active evaluation:
  same test blob;
- queue capacity blocks before tick/state mutation:
  `tests/obsidian_projection/test_p5d4_bounded_observer_loop_runtime_v0_1.py`
  blob `5bcc563487ca8c64a1afde9f022504b2b618af7b`.

Therefore the closure must both strengthen P5-E invariants and create an explicit requirement-to-executable-proof matrix instead of duplicating already-qualified behavior.

## B2 — silent cadence widening

Adjudication:

`CONFIRMED_BLOCKING`

Reproduced on the current model:

- source time 250, first exact observation at 300 -> PASS with latency 50 despite a skipped 270-second slot;
- source time 1, first exact observation at 60 -> PASS with latency 59 despite a skipped 30-second slot.

The current model verifies grid phase, not fixed-rate cadence continuity.

## B3 — impossible pre-source observation

Adjudication:

`CONFIRMED_BLOCKING`

Reproduced on the current model:

- source time 45;
- exact observation at 30;
- exact observation at 60;

result:

`PASS_DETECTED_WITHIN_BOUND`

The exact observation before the claimed source event is silently ignored. This must become fail-closed timing inconsistency.

## B4 — real latency origin and endpoint not operationalized

Adjudication:

`CONFIRMED_BLOCKING`

The current contract defines detection latency as remote-head availability to first successful exact observation while requiring a local monotonic clock.

It does not define a directly observable remote-availability timestamp in that local monotonic domain, nor whether observation time means read start or read completion, nor a fixed-rate/fixed-delay scheduling rule.

Correction direction:

- preserve 30-second interval and 60-second maximum;
- replace the unobservable real measurement origin with a controlled local source-release event in the same monotonic domain;
- use successful remote-read completion as the conservative endpoint;
- freeze fixed-rate scheduling;
- expose read duration rather than assuming zero-duration reads;
- make the future real metric falsifiable.

No real timing execution is authorized by this amendment.

## B5 — intermediate remote tips during bursts

Adjudication:

`PARTIALLY_CONFIRMED_BLOCKING_SEMANTIC_GAP`

A polling observer cannot guarantee that every transient remote tip is observed.

The external review correctly identifies that an A -> B burst between polls can cause A never to be observed as the remote tip.

This is not necessarily content loss when B is a verified fast-forward containing A. Therefore the corrected contract must distinguish:

- `OBSERVED_REMOTE_TIP`: a head actually returned by a read and therefore eligible for existing P5-D2/P5-D4 queue semantics;
- `INTERMEDIATE_FAST_FORWARD_COMMIT`: content contained in a later observed head but not itself claimed to have been observed as a tip.

The corrected candidate must not:

- claim exact-tip detection for a transient tip never observed;
- inject an unobserved intermediate tip into P5-D2/P5-D4;
- call containment "coalescing";
- replace or retarget a head that was already observed and queued.

Future ancestry enumeration or per-tip detection semantics require separate qualification.

## Internal verdict

```text
B1 = CONFIRMED_BLOCKING_WITH_UPSTREAM_COVERAGE_NUANCE
B2 = CONFIRMED_BLOCKING
B3 = CONFIRMED_BLOCKING
B4 = CONFIRMED_BLOCKING
B5 = PARTIALLY_CONFIRMED_BLOCKING_SEMANTIC_GAP

P5E_V0_1_CURRENT_CANDIDATE
= NOT_READY_FOR_HUMAN_NORMATIVE_ADOPTION

REAL_P5E
= CLOSED
```

The next authorized work is the targeted closure amendment only.
