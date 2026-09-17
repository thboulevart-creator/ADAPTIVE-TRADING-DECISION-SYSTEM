# RESEARCH PRODUCER JUNCTION — TIER-A CONTRACT V1

**Contract ID:** `RESEARCH_PRODUCER_JUNCTION_V1`  
**Status before qualification:** `BLOCKED`  
**Boundary:** `src/research/ runtime execution → ResearchRunEvidence`  
**Tier:** `A`

## 1. Purpose

Close the smallest executable junction that allows a real qualified research execution to become downstream-admissible `ResearchRunEvidence` without creating an alternative provenance route.

This boundary is Tier A because a successful output can authorize `ResearchFindings` and `DECISION` consumption.

## 2. Existing runtime surface mapped

At `feat/multi-year-dukascopy-acquisition@b7d13bb3492fb6e1f0d4dcab64079bf1a8f55698`, `src/research/` contains exactly the five-file dependency closure required by `run_qualified_research()`:

1. `src/research/__init__.py`
2. `src/research/bi5_reader.py`
3. `src/research/input_binding.py`
4. `src/research/engine.py`
5. `src/research/execution.py`

`execution.py` currently returns `ResearchExecutionResult(files_consumed, ticks_consumed, first_timestamp, last_timestamp, stream_sha256)`.

That object is not yet a `ResearchRunEvidence` and carries no downstream factory attestation.

## 3. Smallest authorized producer junction

The only admissible direction is:

`QualifiedResearchInput → bound input → actual research execution → identity-bound ResearchExecutionResult → ResearchRunEvidence factory → ResearchFindings / DECISION`

The attestation authority MUST remain inside `src/research_run_evidence.py`. Runtime modules must never receive a supported raw evidence-attestation capability.

## 4. Mandatory invariants

A downstream-admissible `ResearchRunEvidence` MUST satisfy all of the following:

1. It comes from the real runtime producer path, not from a report-only or manually reconstructed path.
2. Its execution result is identity-bound to the exact qualified input used for execution.
3. The bound input is itself factory-created and identity/content-bound; reconstruction, copy or post-factory mutation invalidates it.
4. Corpus and instrument-contract identities are revalidated fail-closed before execution.
5. A zero-file or zero-tick execution cannot mint downstream-admissible evidence.
6. `stream_sha256` is a non-empty valid SHA-256 identity and is incorporated into run provenance.
7. `dataset_id`, `dataset_version`, `configuration_version`, `provenance_id` and `research_run_id` are deterministic consequences of the validated execution/input/context identities; callers cannot freely choose them.
8. The supplied `DatasetIdentity` and full `Context` must match the derived runtime identities and observation bounds.
9. No supported/module-level raw attestation/minter API may allow normal callers to promote arbitrary `ResearchRunEvidence` instances.
10. The legacy V4.3 report adapter, if retained for compatibility, must not create evidence accepted by `is_factory_attested()` for `ResearchFindings` or `DECISION`.
11. Copies, exact field reconstruction, `object.__setattr__`, `__dict__` mutation, context substitution, dataset substitution, result substitution and input/result rebinding must fail closed.
12. Inter-process persistence of attestation is explicitly outside P0.4; P0.4 proves only the in-process junction.

### 4.1 Process-local trust model

P0.4 attestation is a **process-local integrity capability**, not a sandbox against arbitrary code execution inside the same CPython interpreter.

The P0.4 threat model treats hostile input objects, reconstruction, copies, field mutation and ordinary module/API calls as adversarial. It assumes the verifier process itself is trusted not to deliberately mutate verifier internals through reflective capabilities such as `__closure__`, closure-cell replacement, `__globals__`, monkeypatching or equivalent interpreter-level state manipulation.

Reflective mutation of the private registry is therefore classified as **process compromise**, not as an ordinary input/API bypass. This is an explicit trust assumption, not a claim that Python closure state is secret.

If untrusted code can execute with arbitrary reflection inside the producer/verifier interpreter, the process-local attestation authority is compromised and MUST NOT be treated as a security boundary.

Any later operational authorization that would rely on this authority must either isolate the authority behind a separately qualified process/trust boundary or use an equivalently strong attestation primitive. P0.5 deterministic replay creates fresh process-local authority and therefore inherits this same process-integrity assumption after replay.

## 5. Required adversarial attacks

P0.4 must at minimum attack:

- `C1` legacy V4.3 report-only evidence used for DECISION;
- `C2` direct module/API access to a supported raw evidence attestation/minter capability;
- `C2R` reflective closure-registry mutation, recorded explicitly as process compromise and not confused with an ordinary API minter;
- `C3` manually constructed `ResearchRunEvidence` promoted to admissible evidence through supported APIs;
- `C4` reconstructed/copied bound research input;
- `C5` post-binding mutation of corpus/contract identities;
- `C6` corpus or contract bytes changed after binding;
- `C7` reconstructed/copied execution result;
- `C8` execution result rebound to a different qualified input;
- `C9` post-execution mutation of result identity/content;
- `C10` zero-file / zero-tick execution;
- `C11` foreign or forged DatasetIdentity;
- `C12` foreign or forged Context/configuration/observation bounds;
- `C13` forged or malformed code version;
- `C14` manual ResearchRunEvidence field reconstruction after a valid runtime run;
- `C15` downstream ResearchFindings/DECISION use after any rejected ordinary-input/API path.

The positive path must use only synthetic local fixtures generated inside tests. It must not perform network access, `.bi5` acquisition or a real backtest.

`C2R` is diagnostic: it must demonstrate and preserve the exact process-integrity limitation. It does not convert arbitrary same-interpreter code execution into a supported P0.4 caller capability.

## 6. Pre-integration fail expectation

Before runtime integration, the original integration HEAD was expected to FAIL P0.4 because two observed alternative authorization paths existed:

- `from_v43_report(...)` could mint evidence accepted by `is_factory_attested()` without the runtime producer executing;
- the module-level `_attest_factory_evidence` capability was directly reachable.

That FAIL was captured before correction. It is evidence for the boundary design, not a reason to weaken the attacks.

The later closure-introspection finding is a separate threat-model clarification: it demonstrates that process-local Python state is not a security boundary against arbitrary code already executing inside the interpreter.

## 7. Import rule

No blind merge is permitted. Only the five-file `src/research/` dependency closure above may be considered for controlled import, and any source modification required to close Tier-A bypasses must be explicit, reviewed by diff, and re-broken.

Historical acquisition tools, `data/`, `LOCAL-EVIDENCE/`, downloader/probe surfaces and real backtest paths remain excluded.

## 8. Qualification rule

P0.4 can be PASS only after:

`formalisation → observed adversarial FAIL → minimal correction/import → adversarial re-break → complete regression → persisted-HEAD re-break`

A green normal path alone is insufficient.

The P0.4 PASS is explicitly **process-local and process-integrity-scoped**. It does not prove resistance to arbitrary code execution inside the same interpreter and cannot by itself authorize a future operational ACTION path.
