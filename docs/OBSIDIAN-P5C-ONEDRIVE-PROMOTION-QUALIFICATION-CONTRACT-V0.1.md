# OBSIDIAN P5-C — WINDOWS / ONEDRIVE PROMOTION QUALIFICATION CONTRACT V0.1

Date: 2026-09-26

## Purpose

P5-C qualifies or rejects concrete promotion primitives for making one complete machine-owned generation replace another under Windows + OneDrive without exposing an incoherent live state.

P5-C does not touch the real ATDS Obsidian Vault. All empirical work must occur in a sacrificial sibling sandbox under the same OneDrive root.

## Qualified predecessor

P5-B2 qualification:

    eb7b3202c8c3c9ced8cb6d068051e0a922da5e22

## Live Vault protection

The real Vault remains:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION

P5-C authorizes no mutation of:

- live generated projection;
- human views;
- .obsidian;
- canonical repository.

## Sandbox

Required experiment target:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-P5C-PROMOTION-SANDBOX

It must be:

- outside the live Vault;
- under the same OneDrive root;
- sacrificial;
- not a Git repository;
- empty or absent before the experiment.

## Primary acceptance property

The primary invariant is:

    ZERO_MIXED_GENERATION_VISIBILITY

A reader observing the official live entrypoint must never observe files from GEN_A and GEN_B in one logical generation.

The reader also requires:

    zero missing-entrypoint observations
    zero partial-generation observations
    zero parse errors

## Fixture

Each experimental generation contains:

    128 files
    8 nested directories
    per-file embedded generation ID
    deterministic manifest
    deterministic generation tree digest

Two generations are alternated:

    GEN_A
    GEN_B

## Reader probe

A concurrent reader samples at <= 10 ms intervals and verifies:

- live entrypoint exists;
- generation ID parses;
- all referenced files exist;
- all referenced files claim the same generation;
- manifest tree digest matches;
- staging/temp paths are not exposed as live.

Each qualifiable candidate requires at least:

    250 promotion cycles
    5000 reader samples
    both A→B and B→A transitions

One successful rename or replace is not evidence of atomicity.

## Candidate primitives

### Negative control — per-file replacement

    DIRECT_IN_PLACE_PER_FILE_REPLACE

This is deliberately non-qualifiable and exists to prove that the reader probe can detect mixed/non-atomic behavior.

### Candidate A — two-rename directory swap

    DIRECTORY_TWO_RENAME_SWAP

Current live directory is moved aside and the complete staged directory is moved into the live name.

It passes only if the reader never observes a missing or mixed generation window.

### Candidate B — Win32 MoveFileEx directory replacement

    WINDOWS_MOVEFILEEX_DIRECTORY_REPLACE

This candidate tests the actual Win32 API behavior on this specific Windows/OneDrive environment.

No assumption based on documentation is accepted without empirical evidence.

### Candidate C — immutable generations + atomic pointer

    IMMUTABLE_GENERATION_ATOMIC_POINTER

Complete immutable generation directories coexist while one small current pointer/entry file is atomically replaced.

A PASS qualifies only the promotion primitive. It does not automatically approve the long-term Obsidian Graph/Search architecture when more than one generation exists.

## Failure is allowed

P5-C does not require that one candidate pass.

If all candidates fail:

    P5-C RESULT = ALL CANDIDATES REJECTED

and P5-D continuous observer work remains blocked until the architecture is redesigned.

No mechanism may be selected merely because it is preferred or convenient.

## Crash recovery

The finally selected primitive must also survive interruption probes around its mutation boundary.

The last-known-good generation must remain identifiable and the only good generation may never be recursively deleted as part of the experiment.

## Obsidian-open behavior

Filesystem qualification comes first.

A filesystem PASS does not authorize promotion while the real user Vault is open in Obsidian.

Open-state compatibility must later be tested in a sacrificial sandbox Vault.

## Evidence

Raw metrics are append-only and include:

- promotion cycles;
- reader samples;
- mixed-generation observations;
- missing entrypoint observations;
- partial-generation observations;
- parse errors;
- final tree digest;
- environment identity.

Candidate outcomes are:

    PASS
    FAIL
    BLOCKED
    NOT_SUPPORTED

## P5-C non-authorizations

This contract phase does not authorize:

- sandbox execution yet;
- live-Vault experiment;
- background observer;
- continuous synchronization;
- Windows Task Scheduler registration;
- production promotion.

## Next gate

After persisted P5-C contract re-break PASS:

    P5-C2 — PROMOTION EXPERIMENT HARNESS CANDIDATE

P5-C2 will implement and execute the sandbox experiment.

## Success meaning

P5-C contract PASS means only that the experimental protocol and acceptance criteria are fixed before observing candidate behavior.
