# OBSIDIAN P5-D3C2 — STAGING IMPLEMENTATION QUALIFICATION

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following local Windows execution result was supplied by the user.
It was not independently executed by the assistant.

## Qualified functional candidate

Exact corrected P5-D3C2 functional candidate:

    41d19df20dc5214e3b64098dd72519a23ea6e010

Branch:

    feat/obsidian-projection-p5d3c2-staging-implementation-v0.1

The previous candidate:

    f5304fa9697bd33ea98214598321473087b65e24

remains a failed targeted-test candidate due to a contract-test key typo.

The corrected candidate changed only the implementation-contract breaker key assertion.

The runtime contract, packager/verifier implementation and sandbox runner remained unchanged.

## Reported full regression result

The user reported:

    Ran 946 tests in 14.671s
    OK
    P5D3C2_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN_AFTER_TESTS=PASS

The governed wrapper therefore passed:

- py_compile;
- targeted P5-D3C + P5-D3C2 tests;
- the full tests/obsidian_projection regression suite;
- source-clean control checkout verification;

before proceeding to sacrificial sandbox qualification.

## Reported sacrificial sandbox result

Reported schema:

    ATDS_OBSIDIAN_P5D3C2_SANDBOX_REPORT_V0_1

Reported sandbox status:

    PASS_SANDBOX_SEALED_UNPROMOTED

Reported package verification status:

    PASS_SEALED_UNPROMOTED

Reported generation ID:

    gen-7e2c2523ed7574bf13c71b542921e1606126c391e80a39f21c16052275deea57

Reported candidate-generation digest:

    64e944f0c2f69502a7c39c05566f16c4078caec9a334ef8c4c0d2c57d43256ba

Reported payload file-map digest:

    cf03e9e30d52bc1b53c27d29789caf36cf5a60e25700d991f71b80e54a4a35dc

Reported payload file count:

    4

## Read-only verifier evidence

Reported:

    control_verify_repeat_equal=true
    control_content_digest_unchanged=true

This supports the tested claim that repeated verification of the control package did not mutate its content and returned stable package identity in the sacrificial sandbox.

## Required destructive mutation breakers

The user-reported sandbox passed all seven mandatory destructive breakers:

    PAYLOAD_BYTE_MUTATION
    PAYLOAD_FILE_DELETION
    UNMANIFESTED_EXTRA_FILE
    PAYLOAD_MANIFEST_MUTATION
    GENERATION_MANIFEST_MUTATION
    SEAL_MUTATION
    HARD_LINK_ALIAS

Reported count:

    required_mutation_breaker_count=7

All seven were rejected by the verifier as invalid candidate-generation packages.

## Reparse / symlink probe

Reported:

    reparse_probe_status=REJECTED_AS_INVALID

Therefore the host was capable of creating the tested link mutation and the verifier rejected it.

No capability waiver was needed for this run.

## Publication / authority boundary

Reported:

    current_pointer_created=false
    production_promotion_authorized=false
    real_vault_modified=false
    sandbox_retained=false

Final wrapper markers:

    P5D3C2_SANDBOX_QUALIFICATION=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3C2_QUALIFICATION_EXECUTION_COMPLETED=PASS

## Qualified P5-D3C2 boundary

P5-D3C2 now qualifies, within the tested sacrificial Windows filesystem environment:

- implementation of the generic candidate-generation packager defined by P5-D3C;
- implementation of the read-only candidate-generation verifier;
- fresh OS-temp staging;
- byte-exact payload copy;
- exclusive payload/manifests/seal creation;
- deterministic path-independent generation identity;
- payload file-map binding;
- payload-manifest binding;
- generation-manifest binding;
- packaged projection-tree digest recomputation;
- SEAL.json as final package mutation;
- PASS_SEALED_UNPROMOTED semantics;
- repeated read-only verification stability;
- rejection of payload-byte mutation;
- rejection of payload-file deletion;
- rejection of unmanifested extra payload file;
- rejection of payload-manifest mutation;
- rejection of generation-manifest mutation;
- rejection of seal mutation;
- rejection of hard-link aliasing;
- rejection of tested reparse/symlink mutation;
- preservation of the original control package across destructive mutation copies.

## Explicit limitations preserved

P5-D3C2 does NOT qualify:

- the historical projection builder as current-head capable;
- a current-head relation adapter;
- body reads for P5-D3B METADATA_ONLY records;
- the finite candidate-evaluation orchestrator;
- production promotion;
- CURRENT pointer creation or mutation;
- real Vault writes;
- background observer execution;
- polling;
- Windows startup/task/service persistence;
- Graph/Search CURRENT semantics.

The sandbox projection fixture remains packaging input only.

It does not establish that a real current-head deterministic projection can yet be produced.

## Verdict

**PASS — P5-D3C2 CANDIDATE GENERATION STAGING IMPLEMENTATION AND SANDBOX QUALIFICATION**

Evidence basis:

    USER-REPORTED LOCAL EXECUTION

This is not independent local execution by the assistant.

## Next governed frontier

The next authorized boundary is:

    P5-D3D — FINITE CANDIDATE EVALUATION ORCHESTRATOR
    WITH CURRENT-HEAD BUILDER ADAPTATION

P5-D3D must close the remaining gap between:

    qualified P5-D3B current-head semantic bridge output

and:

    a deterministic current-head projection consumable by qualified P5-D3C2 staging

while preserving:

- METADATA_ONLY no-body-read authority;
- deterministic double-build requirements;
- preregistered candidate breakers;
- QUALIFIED / REJECTED / BLOCKED outcome semantics;
- live_projection_head unchanged during evaluation;
- no promotion authority;
- no CURRENT mutation;
- no real Vault mutation.

Only after that builder/orchestrator boundary is qualified may P5-D3E attempt a complete sandbox candidate-evaluation flow.
