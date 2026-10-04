# RPE-04 — EXTERNAL ADVERSARIAL REVIEW PACKET

Date: 2026-10-04

## Review target

RPE-04 — NB2 + NB3 REAL REMOTE OBSERVATION ADAPTER V0.1

Candidate state: QUALIFIED_FOR_EXTERNAL_REVIEW

Qualification HEAD before packet:
9ab0ec1093472ed71db974465a97afaaf1165bf4

Final implementation Git blob:
3492006ebee581c205b2c26d4ea98efab72d522a

Qualification blob:
81ce135f55a607dff7124ce477f9a3446584f634

Qualification report blob:
47d3cc3de7f4b6b5d6dd0afac1151cc6d4baee2a

Scope:
LOCAL_BARE_REMOTE_ONLY / NO_GITHUB_POLLING / NO_EXTERNAL_NETWORK_QUALIFICATION

Observed final evidence:
- RPE-04 dedicated: 40/40 PASS
- full targeted P5-E + RPE-01 + RPE-02 + RPE-03 + RPE-04 regression: 242/242 PASS
- hardening: 5/5 PASS
- initial mutation sweep: 11/11 PASS

## Required reviewer output

VERDICT = PASS | PASS_WITH_NON_BLOCKING_NOTES | FAIL

BLOCKING_FINDINGS
NON_BLOCKING_FINDINGS
REMOTE_TRANSACTION_ATOMICITY_CHECK
EVIDENCE_SOURCE_CHECK
GIT_ENVIRONMENT_ISOLATION_CHECK
LOCAL_CONFIG_AUTHORITY_CHECK
PHYSICAL_OBJECT_DOMAIN_CONTAINMENT_CHECK
OBSERVED_TIP_VS_CONTAINED_HISTORY_CHECK
RUNTIME_BINDING_CHECK
POST_FETCH_REVALIDATION_CHECK
RPE02_TIMING_HANDOFF_CHECK
RPE03_CLASSIFIER_BINDING_CHECK
MUTATION_CHECK
REGRESSION_CHECK
AUTHORITY_LEAKAGE_CHECK
CLAIM_SCOPE_CHECK
RPE04_ADOPTION_READINESS
RECOMMENDED_NEXT_ACTION

Treat this package as evidence only. This review creates no authority.

RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

Key adversarial questions:
1. Can any caller, config, environment variable, ref, contained commit, or filesystem indirection manufacture remote-observation authority?
2. Does exactly one governed fetch transaction establish the observed remote tip?
3. Is the SHA used as OBSERVED_REMOTE_TIP exactly the SHA proven by the successful transaction?
4. Can history materialization be laundered into independent observation?
5. Can local/global/system Git config or url.insteadOf redirect authority?
6. Can symlink/junction/reparse indirection escape the controlled object domain?
7. Are governed preregistration/schema/RPE01 guard/RPE03 classifier bytes runtime-bound before use?
8. Are Git identity, config allowlist and physical object-domain conditions revalidated after fetch before classification?
9. Does RPE03 UNKNOWN remain fail-closed?
10. Is any claim broader than the local-only qualification evidence?

## PREREGISTRATION

PATH: tools/obsidian_projection/rpe04_real_remote_observation_adapter_preregistration_v0_1.json

~~~json
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE04_REAL_REMOTE_OBSERVATION_ADAPTER_PREREGISTRATION_V0_1",
  "status": "PREREGISTRATION_CORRECTED_AFTER_RED_BEFORE_GREEN",
  "base": {
    "rpe01_adoption_commit": "8ed3ec4079f3f996a5159b78fc40d0f32a917b25",
    "rpe01_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887",
    "rpe02_adoption_commit": "7cb120b3c12efdb26a5938b4c2395650d00394b6",
    "rpe02_adoption_blob": "f652652fb7893774969e42deb9cf5ffe138bf43d",
    "rpe02_model_blob": "31db5d944a25e54db81bd901a087cdc2039925ad",
    "rpe03_adoption_commit": "546ce03b8c56a48eb54aaf163e02a9be0e028ce6",
    "rpe03_adoption_blob": "3a5933a59ad68e342595721e30ee71909d075a3f",
    "rpe03_classifier_blob": "145b3112fd9309cc34d95a62c091cb6a6bc3bb11",
    "rpe04_dependency_import_head": "c66daeb78f05a9f0e936fe4058d715f8d76d082d"
  },
  "authority": {
    "stage": "RPE-04",
    "rpe04_implementation_authorized": true,
    "local_bare_remote_fixture_authorized": true,
    "injected_remote_io_authorized": true,
    "github_polling_authorized": false,
    "external_network_qualification_authorized": false,
    "remote_push_authorized": false,
    "rpe05_authorized": false,
    "rpe06_authorized": false,
    "real_p5e_authorized": false,
    "real_p5d4_state_mutation_authorized": false,
    "vault_or_current_mutation_authorized": false,
    "evaluation_promotion_publication_authorized": false
  },
  "governed_config": {
    "authorized_entrypoint": "validate_governed_json(raw_document, raw_schema)",
    "private_guard_functions_forbidden": true,
    "validate_schema_definition_not_document_entrypoint": true,
    "runtime_preregistration_path": "tools/obsidian_projection/rpe04_real_remote_observation_adapter_preregistration_v0_1.json",
    "runtime_schema_path": "tools/obsidian_projection/rpe04_real_remote_observation_adapter_preregistration_v0_1_schema_v0_1.json",
    "environment_config_authority_forbidden": true,
    "cli_config_authority_forbidden": true,
    "unlisted_file_config_authority_forbidden": true
  },
  "qualification_environment": {
    "mode": "LOCAL_BARE_REMOTE_OR_INJECTED_REMOTE_IO_NO_GITHUB_POLLING",
    "qualification_root": "C:\\Users\\Boulevart\\ATDS-CONTROL\\RPE04-QUALIFICATION",
    "source_bare_repository": "C:\\Users\\Boulevart\\ATDS-CONTROL\\RPE04-QUALIFICATION\\source.git",
    "observer_bare_repository": "C:\\Users\\Boulevart\\ATDS-CONTROL\\RPE04-QUALIFICATION\\observer.git"
  },
  "git_executable": {
    "resolved_path": "C:\\Program Files\\Git\\cmd\\git.exe",
    "sha256": "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5",
    "observed_version": "git version 2.54.0.windows.1",
    "minimum_supported_version": "2.54.0.windows.1",
    "exact_executable_identity_required": true
  },
  "git_environment_isolation": {
    "strip_all_inherited_git_prefixed_variables": true,
    "explicit_git_environment": [
      "GIT_NO_REPLACE_OBJECTS=1",
      "GIT_CONFIG_NOSYSTEM=1",
      "GIT_CONFIG_GLOBAL=NUL",
      "GIT_TERMINAL_PROMPT=0",
      "GIT_OPTIONAL_LOCKS=0"
    ],
    "explicit_command_config": [
      "core.hooksPath=NUL",
      "gc.auto=0"
    ],
    "local_config_allowlist": [
      "core.repositoryformatversion=0",
      "core.filemode=false",
      "core.bare=true",
      "core.symlinks=false",
      "core.ignorecase=true"
    ],
    "inherited_url_instead_of_authority_forbidden": true,
    "local_include_path_forbidden": true,
    "local_include_if_forbidden": true,
    "canonical_user_worktree_mutation_forbidden": true
  },
  "remote_transaction": {
    "design": "ONE_GOVERNED_FETCH_TRANSACTION_PER_ATTEMPT",
    "remote_identity": "C:\\Users\\Boulevart\\ATDS-CONTROL\\RPE04-QUALIFICATION\\source.git",
    "source_ref": "refs/heads/rpe04-source",
    "isolated_local_ref": "refs/rpe04/observed",
    "observed_sha_evidence_source": "POST_SUCCESS_EXACT_LOCAL_REF_refs/rpe04/observed_UPDATED_BY_THE_SINGLE_FETCH",
    "observed_sha_extraction": "git rev-parse --verify refs/rpe04/observed^{commit}",
    "remote_observation_completion_timestamp_point": "IMMEDIATELY_AFTER_FETCH_PROCESS_SUCCESS_RETURN",
    "attempt_completion_timestamp_point": "AFTER_MATERIALIZATION_PROOF_RPE03_CLASSIFICATION_AND_NORMALIZED_EVENT_CONSTRUCTION",
    "timeout_milliseconds": 5000,
    "zero_ref_behavior": "READ_FAILURE_FAIL_CLOSED",
    "multiple_ref_behavior": "BLOCKED_UNEXPECTED_OBSERVATION_NAMESPACE",
    "unexpected_ref_behavior": "BLOCKED_UNEXPECTED_OBSERVATION_NAMESPACE",
    "namespace_lifecycle": "ONLY_refs/rpe04/observed_MAY_EXIST_UNDER_refs/rpe04",
    "object_domain_lifecycle": "PREINITIALIZED_BARE_OBSERVER_BEFORE_ATTEMPT",
    "object_domain_retention_across_attempts": "RETAIN_WITHIN_ONE_QUALIFICATION_TRACE_TO_CLASSIFY_TRANSITIONS",
    "local_plus_refspec_role": "ALLOW_LOCAL_OBSERVATION_NAMESPACE_TO_TRACK_NON_FAST_FORWARD_REMOTE_TRANSITIONS_ONLY",
    "remote_force_push_authority": false,
    "fetch_command_exact": "\"C:\\Program Files\\Git\\cmd\\git.exe\" -c core.hooksPath=NUL -c gc.auto=0 \"--git-dir=C:\\Users\\Boulevart\\ATDS-CONTROL\\RPE04-QUALIFICATION\\observer.git\" fetch --no-tags --no-recurse-submodules --no-write-fetch-head -- \"C:\\Users\\Boulevart\\ATDS-CONTROL\\RPE04-QUALIFICATION\\source.git\" +refs/heads/rpe04-source:refs/rpe04/observed"
  },
  "physical_object_domain": {
    "path_identity_not_equal_physical_containment": true,
    "no_ungoverned_indirection_required": true,
    "paths_checked": [
      "OBSERVER_REPOSITORY_ROOT",
      "objects",
      "objects/pack",
      "objects/info"
    ],
    "indirections_rejected": [
      "SYMLINK",
      "JUNCTION",
      "REPARSE_POINT",
      "EQUIVALENT_FILESYSTEM_REDIRECTION"
    ],
    "absent_required_subpath_behavior": "BLOCKED",
    "unprovable_containment_behavior": "BLOCKED"
  },
  "timing": {
    "normative_unit": "INTEGER_MONOTONIC_NANOSECONDS",
    "api": "time.monotonic_ns",
    "attempt_started_at_ns": "CAPTURED_IMMEDIATELY_BEFORE_SINGLE_FETCH_INVOCATION",
    "remote_observation_completed_at_ns": "CAPTURED_IMMEDIATELY_AFTER_SUCCESSFUL_FETCH_RETURN",
    "attempt_completed_at_ns": "CAPTURED_AFTER_LOCAL_PROOF_CLASSIFICATION_AND_EVENT_CONSTRUCTION",
    "floating_point_seconds_normative_forbidden": true
  },
  "evidence_semantics": {
    "exact_success_identity": "LOWERCASE_40_HEX_SHA",
    "successful_outcome": "REMOTE_HEAD_OBSERVED",
    "failed_read_outcome": "READ_FAILURE",
    "exact_remote_tip_label": "OBSERVED_REMOTE_TIP",
    "ancestry_only_label": "CONTENT_CONTAINED_NOT_OBSERVED",
    "intermediate_commit_injection_forbidden": true,
    "caller_supplied_observed_head_authority_forbidden": true,
    "caller_supplied_transition_class_authority_forbidden": true,
    "caller_supplied_containment_authority_forbidden": true,
    "observed_sha_must_be_materialized_commit_before_classification": true,
    "unprovable_observed_sha_behavior": "UNKNOWN_BLOCKED"
  },
  "normalized_output": {
    "event_type": "REMOTE_HEAD_OBSERVED",
    "transition_source": "QUALIFIED_RPE03_CLASSIFIER_ONLY",
    "transition_vocabulary": [
      "INITIAL",
      "SAME",
      "FAST_FORWARD",
      "NON_FAST_FORWARD",
      "UNKNOWN"
    ],
    "required_success_fields": [
      "outcome",
      "event_type",
      "evidence_label",
      "observed_head",
      "transition_class",
      "attempt_started_at_ns",
      "remote_observation_completed_at_ns",
      "attempt_completed_at_ns"
    ],
    "queue_coalescing_authority": false,
    "retargeting_authority": false,
    "evaluation_authority": false,
    "stage_a_authority": false,
    "stage_b_authority": false,
    "promotion_authority": false,
    "publication_authority": false,
    "vault_or_current_authority": false
  },
  "mandatory_red_cases": [
    "zero ref fails closed",
    "multiple or unexpected observation namespace ref blocks",
    "malformed observed SHA blocks",
    "remote read failure emits READ_FAILURE",
    "timeout emits READ_FAILURE",
    "inherited global Git config is neutralized",
    "inherited system Git config is neutralized",
    "url.insteadOf cannot redirect governed remote identity",
    "local include.path is rejected",
    "local includeIf is rejected",
    "hooks path is explicitly disabled",
    "terminal prompt is disabled",
    "off-contract fetch argv rejected by static contract test",
    "off-contract refspec rejected by static contract test",
    "tag fetch absent",
    "submodule recursion disabled",
    "FETCH_HEAD write disabled",
    "caller cannot supply transition class",
    "caller cannot supply containment claim",
    "observed SHA not materialized blocks",
    "contained history cannot become OBSERVED_REMOTE_TIP",
    "intermediate commit cannot be injected as observed tip",
    "local isolated namespace can track NON_FAST_FORWARD transition",
    "symlink junction or reparse object-domain indirection blocks",
    "RPE-03 UNKNOWN propagates without positive laundering"
  ],
  "claim_boundary": {
    "rpe04_local_adapter_semantics_qualified_candidate": true,
    "real_p5e_qualified": false,
    "real_60_second_sla_qualified": false,
    "production_github_polling_qualified": false
  },
  "stop": "EXTERNAL_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE",
  "preregistration_correction": {
    "reason": "NEUTRALIZED_GIT_INIT_BARE_OBSERVED_CORE_SYMLINKS_FALSE",
    "observation_environment": "git version 2.54.0.windows.1 / Windows / GIT_CONFIG_NOSYSTEM=1 / GIT_CONFIG_GLOBAL=NUL",
    "observed_additional_local_config": "core.symlinks=false",
    "scope_change": false,
    "implementation_semantics_change": false,
    "authority_expansion": false
  }
}

~~~

## PREREGISTRATION SCHEMA

PATH: tools/obsidian_projection/rpe04_real_remote_observation_adapter_preregistration_v0_1_schema_v0_1.json

~~~json
{
  "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
  "artifact_role": "RPE04_REAL_REMOTE_OBSERVATION_ADAPTER_PREREGISTRATION",
  "root": {
    "kind": "object",
    "fields": {
      "schema": {
        "kind": "string",
        "const": "ATDS_OBSIDIAN_REAL_P5E_RPE04_REAL_REMOTE_OBSERVATION_ADAPTER_PREREGISTRATION_V0_1"
      },
      "status": {
        "kind": "string",
        "const": "PREREGISTRATION_CORRECTED_AFTER_RED_BEFORE_GREEN"
      },
      "base": {
        "kind": "object",
        "fields": {
          "rpe01_adoption_commit": {
            "kind": "string",
            "const": "8ed3ec4079f3f996a5159b78fc40d0f32a917b25"
          },
          "rpe01_guard_blob": {
            "kind": "string",
            "const": "26f977961d72a062199d71ffd628d5a5cc047887"
          },
          "rpe02_adoption_commit": {
            "kind": "string",
            "const": "7cb120b3c12efdb26a5938b4c2395650d00394b6"
          },
          "rpe02_adoption_blob": {
            "kind": "string",
            "const": "f652652fb7893774969e42deb9cf5ffe138bf43d"
          },
          "rpe02_model_blob": {
            "kind": "string",
            "const": "31db5d944a25e54db81bd901a087cdc2039925ad"
          },
          "rpe03_adoption_commit": {
            "kind": "string",
            "const": "546ce03b8c56a48eb54aaf163e02a9be0e028ce6"
          },
          "rpe03_adoption_blob": {
            "kind": "string",
            "const": "3a5933a59ad68e342595721e30ee71909d075a3f"
          },
          "rpe03_classifier_blob": {
            "kind": "string",
            "const": "145b3112fd9309cc34d95a62c091cb6a6bc3bb11"
          },
          "rpe04_dependency_import_head": {
            "kind": "string",
            "const": "c66daeb78f05a9f0e936fe4058d715f8d76d082d"
          }
        }
      },
      "authority": {
        "kind": "object",
        "fields": {
          "stage": {
            "kind": "string",
            "const": "RPE-04"
          },
          "rpe04_implementation_authorized": {
            "kind": "boolean",
            "const": true
          },
          "local_bare_remote_fixture_authorized": {
            "kind": "boolean",
            "const": true
          },
          "injected_remote_io_authorized": {
            "kind": "boolean",
            "const": true
          },
          "github_polling_authorized": {
            "kind": "boolean",
            "const": false
          },
          "external_network_qualification_authorized": {
            "kind": "boolean",
            "const": false
          },
          "remote_push_authorized": {
            "kind": "boolean",
            "const": false
          },
          "rpe05_authorized": {
            "kind": "boolean",
            "const": false
          },
          "rpe06_authorized": {
            "kind": "boolean",
            "const": false
          },
          "real_p5e_authorized": {
            "kind": "boolean",
            "const": false
          },
          "real_p5d4_state_mutation_authorized": {
            "kind": "boolean",
            "const": false
          },
          "vault_or_current_mutation_authorized": {
            "kind": "boolean",
            "const": false
          },
          "evaluation_promotion_publication_authorized": {
            "kind": "boolean",
            "const": false
          }
        }
      },
      "governed_config": {
        "kind": "object",
        "fields": {
          "authorized_entrypoint": {
            "kind": "string",
            "const": "validate_governed_json(raw_document, raw_schema)"
          },
          "private_guard_functions_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "validate_schema_definition_not_document_entrypoint": {
            "kind": "boolean",
            "const": true
          },
          "runtime_preregistration_path": {
            "kind": "string",
            "const": "tools/obsidian_projection/rpe04_real_remote_observation_adapter_preregistration_v0_1.json"
          },
          "runtime_schema_path": {
            "kind": "string",
            "const": "tools/obsidian_projection/rpe04_real_remote_observation_adapter_preregistration_v0_1_schema_v0_1.json"
          },
          "environment_config_authority_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "cli_config_authority_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "unlisted_file_config_authority_forbidden": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "qualification_environment": {
        "kind": "object",
        "fields": {
          "mode": {
            "kind": "string",
            "const": "LOCAL_BARE_REMOTE_OR_INJECTED_REMOTE_IO_NO_GITHUB_POLLING"
          },
          "qualification_root": {
            "kind": "string",
            "const": "C:\\Users\\Boulevart\\ATDS-CONTROL\\RPE04-QUALIFICATION"
          },
          "source_bare_repository": {
            "kind": "string",
            "const": "C:\\Users\\Boulevart\\ATDS-CONTROL\\RPE04-QUALIFICATION\\source.git"
          },
          "observer_bare_repository": {
            "kind": "string",
            "const": "C:\\Users\\Boulevart\\ATDS-CONTROL\\RPE04-QUALIFICATION\\observer.git"
          }
        }
      },
      "git_executable": {
        "kind": "object",
        "fields": {
          "resolved_path": {
            "kind": "string",
            "const": "C:\\Program Files\\Git\\cmd\\git.exe"
          },
          "sha256": {
            "kind": "string",
            "const": "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5"
          },
          "observed_version": {
            "kind": "string",
            "const": "git version 2.54.0.windows.1"
          },
          "minimum_supported_version": {
            "kind": "string",
            "const": "2.54.0.windows.1"
          },
          "exact_executable_identity_required": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "git_environment_isolation": {
        "kind": "object",
        "fields": {
          "strip_all_inherited_git_prefixed_variables": {
            "kind": "boolean",
            "const": true
          },
          "explicit_git_environment": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 5,
            "max_items": 5,
            "unique": true,
            "ordered_const": [
              "GIT_NO_REPLACE_OBJECTS=1",
              "GIT_CONFIG_NOSYSTEM=1",
              "GIT_CONFIG_GLOBAL=NUL",
              "GIT_TERMINAL_PROMPT=0",
              "GIT_OPTIONAL_LOCKS=0"
            ],
            "allowed_values": [
              "GIT_NO_REPLACE_OBJECTS=1",
              "GIT_CONFIG_NOSYSTEM=1",
              "GIT_CONFIG_GLOBAL=NUL",
              "GIT_TERMINAL_PROMPT=0",
              "GIT_OPTIONAL_LOCKS=0"
            ]
          },
          "explicit_command_config": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 2,
            "max_items": 2,
            "unique": true,
            "ordered_const": [
              "core.hooksPath=NUL",
              "gc.auto=0"
            ],
            "allowed_values": [
              "core.hooksPath=NUL",
              "gc.auto=0"
            ]
          },
          "local_config_allowlist": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 5,
            "max_items": 5,
            "unique": true,
            "ordered_const": [
              "core.repositoryformatversion=0",
              "core.filemode=false",
              "core.bare=true",
              "core.symlinks=false",
              "core.ignorecase=true"
            ],
            "allowed_values": [
              "core.repositoryformatversion=0",
              "core.filemode=false",
              "core.bare=true",
              "core.symlinks=false",
              "core.ignorecase=true"
            ]
          },
          "inherited_url_instead_of_authority_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "local_include_path_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "local_include_if_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "canonical_user_worktree_mutation_forbidden": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "remote_transaction": {
        "kind": "object",
        "fields": {
          "design": {
            "kind": "string",
            "const": "ONE_GOVERNED_FETCH_TRANSACTION_PER_ATTEMPT"
          },
          "remote_identity": {
            "kind": "string",
            "const": "C:\\Users\\Boulevart\\ATDS-CONTROL\\RPE04-QUALIFICATION\\source.git"
          },
          "source_ref": {
            "kind": "string",
            "const": "refs/heads/rpe04-source"
          },
          "isolated_local_ref": {
            "kind": "string",
            "const": "refs/rpe04/observed"
          },
          "observed_sha_evidence_source": {
            "kind": "string",
            "const": "POST_SUCCESS_EXACT_LOCAL_REF_refs/rpe04/observed_UPDATED_BY_THE_SINGLE_FETCH"
          },
          "observed_sha_extraction": {
            "kind": "string",
            "const": "git rev-parse --verify refs/rpe04/observed^{commit}"
          },
          "remote_observation_completion_timestamp_point": {
            "kind": "string",
            "const": "IMMEDIATELY_AFTER_FETCH_PROCESS_SUCCESS_RETURN"
          },
          "attempt_completion_timestamp_point": {
            "kind": "string",
            "const": "AFTER_MATERIALIZATION_PROOF_RPE03_CLASSIFICATION_AND_NORMALIZED_EVENT_CONSTRUCTION"
          },
          "timeout_milliseconds": {
            "kind": "integer",
            "const": 5000
          },
          "zero_ref_behavior": {
            "kind": "string",
            "const": "READ_FAILURE_FAIL_CLOSED"
          },
          "multiple_ref_behavior": {
            "kind": "string",
            "const": "BLOCKED_UNEXPECTED_OBSERVATION_NAMESPACE"
          },
          "unexpected_ref_behavior": {
            "kind": "string",
            "const": "BLOCKED_UNEXPECTED_OBSERVATION_NAMESPACE"
          },
          "namespace_lifecycle": {
            "kind": "string",
            "const": "ONLY_refs/rpe04/observed_MAY_EXIST_UNDER_refs/rpe04"
          },
          "object_domain_lifecycle": {
            "kind": "string",
            "const": "PREINITIALIZED_BARE_OBSERVER_BEFORE_ATTEMPT"
          },
          "object_domain_retention_across_attempts": {
            "kind": "string",
            "const": "RETAIN_WITHIN_ONE_QUALIFICATION_TRACE_TO_CLASSIFY_TRANSITIONS"
          },
          "local_plus_refspec_role": {
            "kind": "string",
            "const": "ALLOW_LOCAL_OBSERVATION_NAMESPACE_TO_TRACK_NON_FAST_FORWARD_REMOTE_TRANSITIONS_ONLY"
          },
          "remote_force_push_authority": {
            "kind": "boolean",
            "const": false
          },
          "fetch_command_exact": {
            "kind": "string",
            "const": "\"C:\\Program Files\\Git\\cmd\\git.exe\" -c core.hooksPath=NUL -c gc.auto=0 \"--git-dir=C:\\Users\\Boulevart\\ATDS-CONTROL\\RPE04-QUALIFICATION\\observer.git\" fetch --no-tags --no-recurse-submodules --no-write-fetch-head -- \"C:\\Users\\Boulevart\\ATDS-CONTROL\\RPE04-QUALIFICATION\\source.git\" +refs/heads/rpe04-source:refs/rpe04/observed"
          }
        }
      },
      "physical_object_domain": {
        "kind": "object",
        "fields": {
          "path_identity_not_equal_physical_containment": {
            "kind": "boolean",
            "const": true
          },
          "no_ungoverned_indirection_required": {
            "kind": "boolean",
            "const": true
          },
          "paths_checked": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 4,
            "max_items": 4,
            "unique": true,
            "ordered_const": [
              "OBSERVER_REPOSITORY_ROOT",
              "objects",
              "objects/pack",
              "objects/info"
            ],
            "allowed_values": [
              "OBSERVER_REPOSITORY_ROOT",
              "objects",
              "objects/pack",
              "objects/info"
            ]
          },
          "indirections_rejected": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 4,
            "max_items": 4,
            "unique": true,
            "ordered_const": [
              "SYMLINK",
              "JUNCTION",
              "REPARSE_POINT",
              "EQUIVALENT_FILESYSTEM_REDIRECTION"
            ],
            "allowed_values": [
              "SYMLINK",
              "JUNCTION",
              "REPARSE_POINT",
              "EQUIVALENT_FILESYSTEM_REDIRECTION"
            ]
          },
          "absent_required_subpath_behavior": {
            "kind": "string",
            "const": "BLOCKED"
          },
          "unprovable_containment_behavior": {
            "kind": "string",
            "const": "BLOCKED"
          }
        }
      },
      "timing": {
        "kind": "object",
        "fields": {
          "normative_unit": {
            "kind": "string",
            "const": "INTEGER_MONOTONIC_NANOSECONDS"
          },
          "api": {
            "kind": "string",
            "const": "time.monotonic_ns"
          },
          "attempt_started_at_ns": {
            "kind": "string",
            "const": "CAPTURED_IMMEDIATELY_BEFORE_SINGLE_FETCH_INVOCATION"
          },
          "remote_observation_completed_at_ns": {
            "kind": "string",
            "const": "CAPTURED_IMMEDIATELY_AFTER_SUCCESSFUL_FETCH_RETURN"
          },
          "attempt_completed_at_ns": {
            "kind": "string",
            "const": "CAPTURED_AFTER_LOCAL_PROOF_CLASSIFICATION_AND_EVENT_CONSTRUCTION"
          },
          "floating_point_seconds_normative_forbidden": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "evidence_semantics": {
        "kind": "object",
        "fields": {
          "exact_success_identity": {
            "kind": "string",
            "const": "LOWERCASE_40_HEX_SHA"
          },
          "successful_outcome": {
            "kind": "string",
            "const": "REMOTE_HEAD_OBSERVED"
          },
          "failed_read_outcome": {
            "kind": "string",
            "const": "READ_FAILURE"
          },
          "exact_remote_tip_label": {
            "kind": "string",
            "const": "OBSERVED_REMOTE_TIP"
          },
          "ancestry_only_label": {
            "kind": "string",
            "const": "CONTENT_CONTAINED_NOT_OBSERVED"
          },
          "intermediate_commit_injection_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "caller_supplied_observed_head_authority_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "caller_supplied_transition_class_authority_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "caller_supplied_containment_authority_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "observed_sha_must_be_materialized_commit_before_classification": {
            "kind": "boolean",
            "const": true
          },
          "unprovable_observed_sha_behavior": {
            "kind": "string",
            "const": "UNKNOWN_BLOCKED"
          }
        }
      },
      "normalized_output": {
        "kind": "object",
        "fields": {
          "event_type": {
            "kind": "string",
            "const": "REMOTE_HEAD_OBSERVED"
          },
          "transition_source": {
            "kind": "string",
            "const": "QUALIFIED_RPE03_CLASSIFIER_ONLY"
          },
          "transition_vocabulary": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 5,
            "max_items": 5,
            "unique": true,
            "ordered_const": [
              "INITIAL",
              "SAME",
              "FAST_FORWARD",
              "NON_FAST_FORWARD",
              "UNKNOWN"
            ],
            "allowed_values": [
              "INITIAL",
              "SAME",
              "FAST_FORWARD",
              "NON_FAST_FORWARD",
              "UNKNOWN"
            ]
          },
          "required_success_fields": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 8,
            "max_items": 8,
            "unique": true,
            "ordered_const": [
              "outcome",
              "event_type",
              "evidence_label",
              "observed_head",
              "transition_class",
              "attempt_started_at_ns",
              "remote_observation_completed_at_ns",
              "attempt_completed_at_ns"
            ],
            "allowed_values": [
              "outcome",
              "event_type",
              "evidence_label",
              "observed_head",
              "transition_class",
              "attempt_started_at_ns",
              "remote_observation_completed_at_ns",
              "attempt_completed_at_ns"
            ]
          },
          "queue_coalescing_authority": {
            "kind": "boolean",
            "const": false
          },
          "retargeting_authority": {
            "kind": "boolean",
            "const": false
          },
          "evaluation_authority": {
            "kind": "boolean",
            "const": false
          },
          "stage_a_authority": {
            "kind": "boolean",
            "const": false
          },
          "stage_b_authority": {
            "kind": "boolean",
            "const": false
          },
          "promotion_authority": {
            "kind": "boolean",
            "const": false
          },
          "publication_authority": {
            "kind": "boolean",
            "const": false
          },
          "vault_or_current_authority": {
            "kind": "boolean",
            "const": false
          }
        }
      },
      "mandatory_red_cases": {
        "kind": "array",
        "items": {
          "kind": "string"
        },
        "min_items": 25,
        "max_items": 25,
        "unique": true,
        "ordered_const": [
          "zero ref fails closed",
          "multiple or unexpected observation namespace ref blocks",
          "malformed observed SHA blocks",
          "remote read failure emits READ_FAILURE",
          "timeout emits READ_FAILURE",
          "inherited global Git config is neutralized",
          "inherited system Git config is neutralized",
          "url.insteadOf cannot redirect governed remote identity",
          "local include.path is rejected",
          "local includeIf is rejected",
          "hooks path is explicitly disabled",
          "terminal prompt is disabled",
          "off-contract fetch argv rejected by static contract test",
          "off-contract refspec rejected by static contract test",
          "tag fetch absent",
          "submodule recursion disabled",
          "FETCH_HEAD write disabled",
          "caller cannot supply transition class",
          "caller cannot supply containment claim",
          "observed SHA not materialized blocks",
          "contained history cannot become OBSERVED_REMOTE_TIP",
          "intermediate commit cannot be injected as observed tip",
          "local isolated namespace can track NON_FAST_FORWARD transition",
          "symlink junction or reparse object-domain indirection blocks",
          "RPE-03 UNKNOWN propagates without positive laundering"
        ],
        "allowed_values": [
          "zero ref fails closed",
          "multiple or unexpected observation namespace ref blocks",
          "malformed observed SHA blocks",
          "remote read failure emits READ_FAILURE",
          "timeout emits READ_FAILURE",
          "inherited global Git config is neutralized",
          "inherited system Git config is neutralized",
          "url.insteadOf cannot redirect governed remote identity",
          "local include.path is rejected",
          "local includeIf is rejected",
          "hooks path is explicitly disabled",
          "terminal prompt is disabled",
          "off-contract fetch argv rejected by static contract test",
          "off-contract refspec rejected by static contract test",
          "tag fetch absent",
          "submodule recursion disabled",
          "FETCH_HEAD write disabled",
          "caller cannot supply transition class",
          "caller cannot supply containment claim",
          "observed SHA not materialized blocks",
          "contained history cannot become OBSERVED_REMOTE_TIP",
          "intermediate commit cannot be injected as observed tip",
          "local isolated namespace can track NON_FAST_FORWARD transition",
          "symlink junction or reparse object-domain indirection blocks",
          "RPE-03 UNKNOWN propagates without positive laundering"
        ]
      },
      "claim_boundary": {
        "kind": "object",
        "fields": {
          "rpe04_local_adapter_semantics_qualified_candidate": {
            "kind": "boolean",
            "const": true
          },
          "real_p5e_qualified": {
            "kind": "boolean",
            "const": false
          },
          "real_60_second_sla_qualified": {
            "kind": "boolean",
            "const": false
          },
          "production_github_polling_qualified": {
            "kind": "boolean",
            "const": false
          }
        }
      },
      "stop": {
        "kind": "string",
        "const": "EXTERNAL_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
      },
      "preregistration_correction": {
        "kind": "object",
        "fields": {
          "reason": {
            "kind": "string",
            "const": "NEUTRALIZED_GIT_INIT_BARE_OBSERVED_CORE_SYMLINKS_FALSE"
          },
          "observation_environment": {
            "kind": "string",
            "const": "git version 2.54.0.windows.1 / Windows / GIT_CONFIG_NOSYSTEM=1 / GIT_CONFIG_GLOBAL=NUL"
          },
          "observed_additional_local_config": {
            "kind": "string",
            "const": "core.symlinks=false"
          },
          "scope_change": {
            "kind": "boolean",
            "const": false
          },
          "implementation_semantics_change": {
            "kind": "boolean",
            "const": false
          },
          "authority_expansion": {
            "kind": "boolean",
            "const": false
          }
        }
      }
    }
  }
}

~~~

## PREREGISTRATION CORRECTION

PATH: reports/program/2026-10-04-OBSIDIAN-REAL-P5E-RPE04-PREREGISTRATION-TARGETED-CORRECTION.md

~~~text
# RPE-04 — PREREGISTRATION TARGETED CORRECTION BEFORE GREEN

Date: 2026-10-04

The initial preregistration was frozen before RED and validated by the RPE-01 public guard.

During the first implementation-candidate run, all functional failures converged on the local-config allowlist.

A fresh local calibration under the exact neutralized RPE-04 Git environment observed these five entries:

- core.repositoryformatversion=0
- core.filemode=false
- core.bare=true
- core.symlinks=false
- core.ignorecase=true

The initial calibration had omitted core.symlinks=false.

This correction adds only that observed entry to the closed local-config allowlist. It changes no fetch semantics, evidence semantics, timing semantics, claim scope, or authority.

The correction occurs before any GREEN result. The preregistration status is therefore explicitly changed to PREREGISTRATION_CORRECTED_AFTER_RED_BEFORE_GREEN.

The frozen RED test file is unchanged.

~~~

## FROZEN RED TEST

PATH: tests/obsidian_projection/test_rpe04_real_remote_observation_adapter_v0_1.py

~~~python
from __future__ import annotations

import importlib.util
import inspect
import json
import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_v0_1.py"
PREREG = ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_preregistration_v0_1.json"
SCHEMA = ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_preregistration_v0_1_schema_v0_1.json"
GUARD = ROOT / "tools/obsidian_projection/rpe01_governed_closed_schema.py"

GIT = pathlib.Path(r"C:\Program Files\Git\cmd\git.exe")
CONTROL = pathlib.Path(r"C:\Users\Boulevart\ATDS-CONTROL\RPE04-QUALIFICATION")
SOURCE = CONTROL / "source.git"
OBSERVER = CONTROL / "observer.git"
PRODUCER = CONTROL / "producer"
SOURCE_REF = "refs/heads/rpe04-source"
LOCAL_REF = "refs/rpe04/observed"


def load_file_module(path: pathlib.Path, name: str):
    if not path.exists():
        raise AssertionError(f"required implementation missing: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def clean_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_REPLACE_OBJECTS": "1",
    })
    return env


def git(*args: str, cwd: pathlib.Path | None = None, check: bool = True):
    cp = subprocess.run(
        [str(GIT), *args],
        cwd=str(cwd) if cwd else None,
        env=clean_env(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and cp.returncode != 0:
        raise AssertionError(f"git failed {args}: {cp.stderr}")
    return cp


def init_fixture():
    shutil.rmtree(CONTROL, ignore_errors=True)
    CONTROL.mkdir(parents=True, exist_ok=True)
    git("init", "--bare", str(SOURCE))
    git("init", "--bare", str(OBSERVER))
    git("init", str(PRODUCER))
    git("config", "user.name", "RPE04 Fixture", cwd=PRODUCER)
    git("config", "user.email", "rpe04@example.invalid", cwd=PRODUCER)
    (PRODUCER / "trace.txt").write_text("A\n", encoding="utf-8")
    git("add", "trace.txt", cwd=PRODUCER)
    git("commit", "-m", "A", cwd=PRODUCER)
    a = git("rev-parse", "HEAD", cwd=PRODUCER).stdout.strip()
    git("push", str(SOURCE), f"{a}:{SOURCE_REF}", cwd=PRODUCER)
    return a


def new_commit(label: str):
    with (PRODUCER / "trace.txt").open("a", encoding="utf-8") as fh:
        fh.write(label + "\n")
    git("add", "trace.txt", cwd=PRODUCER)
    git("commit", "-m", label, cwd=PRODUCER)
    return git("rev-parse", "HEAD", cwd=PRODUCER).stdout.strip()


def publish(sha: str):
    temp_ref = "refs/heads/rpe04-stage"
    git("push", str(SOURCE), f"{sha}:{temp_ref}", cwd=PRODUCER)
    git(f"--git-dir={SOURCE}", "update-ref", SOURCE_REF, sha)
    git(f"--git-dir={SOURCE}", "update-ref", "-d", temp_ref)


class TestRPE04Preregistration(unittest.TestCase):
    def test_preregistration_is_governed_by_rpe01_public_entrypoint(self):
        guard = load_file_module(GUARD, "rpe04_guard")
        raw = PREREG.read_text(encoding="utf-8")
        schema = SCHEMA.read_text(encoding="utf-8")
        guard.validate_governed_json(raw, schema)

    def test_preregistration_pins_git_identity_and_local_only_scope(self):
        p = json.loads(PREREG.read_text(encoding="utf-8"))
        self.assertEqual(p["git_executable"]["resolved_path"], str(GIT))
        self.assertEqual(p["git_executable"]["observed_version"], "git version 2.54.0.windows.1")
        self.assertFalse(p["authority"]["github_polling_authorized"])
        self.assertFalse(p["authority"]["external_network_qualification_authorized"])
        self.assertFalse(p["authority"]["remote_push_authorized"])


class TestRPE04Adapter(unittest.TestCase):
    def setUp(self):
        self.a = init_fixture()

    def tearDown(self):
        shutil.rmtree(CONTROL, ignore_errors=True)

    def m(self, name="rpe04_adapter"):
        return load_file_module(MODULE, name)

    def test_public_interface_cannot_accept_observed_head_transition_or_containment(self):
        m = self.m()
        params = list(inspect.signature(m.observe_once).parameters)
        self.assertEqual(params, ["previous_observed_head"])

    def test_initial_observation_is_exact_remote_tip(self):
        m = self.m()
        out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertEqual(out["event_type"], "REMOTE_HEAD_OBSERVED")
        self.assertEqual(out["evidence_label"], "OBSERVED_REMOTE_TIP")
        self.assertEqual(out["observed_head"], self.a)
        self.assertEqual(out["transition_class"], "INITIAL")
        self.assertFalse(out["blocked"])
        self.assertRegex(out["observed_head"], r"^[0-9a-f]{40}$")

    def test_timestamp_order_is_integer_monotonic_nanoseconds(self):
        m = self.m()
        out = m.observe_once(None)
        fields = [
            out["attempt_started_at_ns"],
            out["remote_observation_completed_at_ns"],
            out["attempt_completed_at_ns"],
        ]
        self.assertTrue(all(type(x) is int for x in fields))
        self.assertLessEqual(fields[0], fields[1])
        self.assertLessEqual(fields[1], fields[2])

    def test_one_fetch_transaction_per_attempt(self):
        m = self.m()
        original = m._run_fetch
        with mock.patch.object(m, "_run_fetch", wraps=original) as wrapped:
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertEqual(wrapped.call_count, 1)

    def test_fast_forward_transition_is_derived_by_rpe03(self):
        m = self.m()
        first = m.observe_once(None)
        b = new_commit("B")
        publish(b)
        second = m.observe_once(first["observed_head"])
        self.assertEqual(second["observed_head"], b)
        self.assertEqual(second["transition_class"], "FAST_FORWARD")

    def test_non_fast_forward_local_namespace_update_is_supported(self):
        m = self.m()
        b = new_commit("B")
        publish(b)
        first = m.observe_once(None)
        self.assertEqual(first["observed_head"], b)
        git(f"--git-dir={SOURCE}", "update-ref", SOURCE_REF, self.a)
        second = m.observe_once(b)
        self.assertEqual(second["observed_head"], self.a)
        self.assertEqual(second["transition_class"], "NON_FAST_FORWARD")

    def test_contained_history_is_not_laundered_as_observed_tip(self):
        m = self.m()
        b = new_commit("B")
        publish(b)
        out = m.observe_once(None)
        self.assertEqual(out["observed_head"], b)
        self.assertNotIn(self.a, json.dumps(out, sort_keys=True))

    def test_missing_remote_ref_fails_closed(self):
        m = self.m()
        git(f"--git-dir={SOURCE}", "update-ref", "-d", SOURCE_REF)
        out = m.observe_once(None)
        self.assertEqual(out["outcome"], "READ_FAILURE")
        self.assertEqual(out["failure_code"], "REMOTE_FETCH_FAILED")

    def test_timeout_fails_closed(self):
        m = self.m()
        with mock.patch.object(
            m,
            "_run_fetch",
            side_effect=subprocess.TimeoutExpired(cmd=["git", "fetch"], timeout=5),
        ):
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "READ_FAILURE")
        self.assertEqual(out["failure_code"], "REMOTE_FETCH_TIMEOUT")

    def test_unexpected_observation_namespace_ref_blocks(self):
        m = self.m()
        first = m.observe_once(None)
        self.assertEqual(first["outcome"], "REMOTE_HEAD_OBSERVED")
        git(f"--git-dir={OBSERVER}", "update-ref", "refs/rpe04/extra", self.a)
        out = m.observe_once(self.a)
        self.assertEqual(out["outcome"], "READ_FAILURE")
        self.assertEqual(out["failure_code"], "UNEXPECTED_OBSERVATION_NAMESPACE")

    def test_malformed_observed_sha_blocks(self):
        m = self.m()
        with mock.patch.object(m, "_extract_observed_sha", return_value="A" * 40):
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "READ_FAILURE")
        self.assertEqual(out["failure_code"], "MALFORMED_OBSERVED_SHA")

    def test_observed_sha_not_materialized_blocks(self):
        m = self.m()
        with mock.patch.object(m, "_extract_observed_sha", return_value="f" * 40):
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "READ_FAILURE")
        self.assertEqual(out["failure_code"], "OBSERVED_SHA_NOT_MATERIALIZED")

    def test_rpe03_unknown_propagates_as_blocked_not_positive_transition(self):
        m = self.m()
        out = m.observe_once("f" * 40)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertEqual(out["transition_class"], "UNKNOWN")
        self.assertTrue(out["blocked"])
        self.assertEqual(out["failure_code"], "ANCESTRY_UNKNOWN")

    def test_local_include_path_is_rejected(self):
        m = self.m()
        git(f"--git-dir={OBSERVER}", "config", "--local", "include.path", r"C:\evil-rpe04.cfg")
        out = m.observe_once(None)
        self.assertEqual(out["outcome"], "READ_FAILURE")
        self.assertEqual(out["failure_code"], "LOCAL_CONFIG_NOT_ALLOWLISTED")

    def test_local_include_if_is_rejected(self):
        m = self.m()
        git(
            f"--git-dir={OBSERVER}",
            "config",
            "--local",
            'includeIf.gitdir:C:/tmp/.path',
            r"C:\evil-rpe04.cfg",
        )
        out = m.observe_once(None)
        self.assertEqual(out["outcome"], "READ_FAILURE")
        self.assertEqual(out["failure_code"], "LOCAL_CONFIG_NOT_ALLOWLISTED")

    def test_inherited_global_config_and_url_insteadof_are_neutralized(self):
        m = self.m()
        with tempfile.TemporaryDirectory() as td:
            hostile = pathlib.Path(td) / "global.gitconfig"
            hostile.write_text(
                '[url "C:/definitely-wrong/"]\n\tinsteadOf = C:/Users/Boulevart/ATDS-CONTROL/RPE04-QUALIFICATION/\n',
                encoding="utf-8",
            )
            with mock.patch.dict(
                os.environ,
                {
                    "GIT_CONFIG_GLOBAL": str(hostile),
                    "GIT_DIR": r"C:\definitely-wrong",
                    "GIT_OBJECT_DIRECTORY": r"C:\definitely-wrong-objects",
                },
                clear=False,
            ):
                out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertEqual(out["observed_head"], self.a)

    def test_git_environment_strips_inherited_git_authority(self):
        m = self.m()
        with mock.patch.dict(
            os.environ,
            {"GIT_DIR": "evil", "GIT_CONFIG_SYSTEM": "evil", "GIT_TERMINAL_PROMPT": "1"},
            clear=False,
        ):
            env = m._build_git_env()
        self.assertNotEqual(env.get("GIT_DIR"), "evil")
        self.assertNotEqual(env.get("GIT_CONFIG_SYSTEM"), "evil")
        self.assertEqual(env["GIT_CONFIG_NOSYSTEM"], "1")
        self.assertEqual(env["GIT_CONFIG_GLOBAL"], "NUL")
        self.assertEqual(env["GIT_TERMINAL_PROMPT"], "0")

    def test_fetch_argv_is_exact_and_disables_tags_submodules_fetch_head_and_hooks(self):
        m = self.m()
        argv = m._build_fetch_argv()
        self.assertEqual(argv[0], str(GIT))
        self.assertIn("core.hooksPath=NUL", argv)
        self.assertIn("gc.auto=0", argv)
        self.assertIn("--no-tags", argv)
        self.assertIn("--no-recurse-submodules", argv)
        self.assertIn("--no-write-fetch-head", argv)
        self.assertEqual(argv[-1], "+refs/heads/rpe04-source:refs/rpe04/observed")
        self.assertNotIn("ls-remote", argv)

    def test_git_executable_identity_is_verified(self):
        m = self.m()
        self.assertTrue(m._verify_git_executable_identity())
        with mock.patch.object(m, "_sha256_file", return_value="0" * 64):
            self.assertFalse(m._verify_git_executable_identity())

    def test_physical_object_domain_accepts_normal_bare_repo(self):
        m = self.m()
        ok, code = m._verify_physical_object_domain(OBSERVER)
        self.assertTrue(ok, code)

    def test_physical_object_domain_rejects_actual_indirection(self):
        m = self.m()
        with tempfile.TemporaryDirectory(prefix="rpe04-link-") as td:
            td = pathlib.Path(td)
            fake = td / "fake.git"
            target = td / "outside-objects"
            fake.mkdir()
            target.mkdir()
            (target / "pack").mkdir()
            (target / "info").mkdir()
            link = fake / "objects"
            made = False
            try:
                os.symlink(target, link, target_is_directory=True)
                made = True
            except (OSError, NotImplementedError):
                cp = subprocess.run(
                    ["cmd.exe", "/c", "mklink", "/J", str(link), str(target)],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                made = cp.returncode == 0
            if not made:
                self.skipTest("platform cannot create symlink or junction")
            ok, code = m._verify_physical_object_domain(fake)
            self.assertFalse(ok)
            self.assertEqual(code, "PHYSICAL_OBJECT_DOMAIN_INDIRECTION")

    def test_exact_observed_sha_only_no_intermediate_injection(self):
        m = self.m()
        b = new_commit("B")
        publish(b)
        out = m.observe_once(None)
        self.assertEqual(
            set(out),
            {
                "outcome",
                "event_type",
                "evidence_label",
                "observed_head",
                "transition_class",
                "attempt_started_at_ns",
                "remote_observation_completed_at_ns",
                "attempt_completed_at_ns",
                "blocked",
                "failure_code",
            },
        )
        self.assertEqual(out["observed_head"], b)


if __name__ == "__main__":
    unittest.main()

~~~

## HISTORICAL RED REPORT

PATH: reports/program/2026-10-04-OBSIDIAN-REAL-P5E-RPE04-REAL-REMOTE-OBSERVATION-ADAPTER-RED.md

~~~text
# RPE-04 — REAL REMOTE OBSERVATION ADAPTER V0.1 — RED

Date: 2026-10-04

## Frozen preregistration

- preregistration blob: `0416bc26222b48713014e503ee39abfbfd40326f`
- schema blob: `ca3e5205a6bd902991376ae77852a40b4a505aca`
- preregistration HEAD: `5fba272905793ca4ac86ac5ba9ceb2803adda8bc`
- RPE-01 guard validation: PASS

## RED test identity

`tests/obsidian_projection/test_rpe04_real_remote_observation_adapter_v0_1.py`

Worktree blob before persistence:

`eec1d9b39714b5e841438fc76180d851b6494bce`

## Observed RED result

```text
Ran 24 tests

2 PASS
22 FAIL

RED_EXIT = 1
```

The two passing tests validate the preregistration and its RPE-01 governed boundary.

All 22 functional adapter tests fail because the preregistered implementation file does not yet exist:

`tools/obsidian_projection/rpe04_real_remote_observation_adapter_v0_1.py`

This is the expected test-first RED state.

## Functional surfaces already frozen by the RED suite

The frozen suite covers:
- exact public interface without caller-supplied observed head/transition/containment authority;
- exact observed remote tip evidence;
- integer monotonic nanosecond timestamps;
- exactly one fetch transaction per attempt;
- FAST_FORWARD and NON_FAST_FORWARD derivation through RPE-03;
- contained-history non-laundering;
- missing remote ref and timeout fail-closed behavior;
- unexpected isolated-namespace refs;
- malformed and unmaterialized observed SHA;
- RPE-03 UNKNOWN propagation without positive laundering;
- local include.path/includeIf rejection;
- inherited/global/system Git authority neutralization;
- exact fetch argv protections;
- Git executable identity binding;
- physical object-domain acceptance and indirection rejection;
- no intermediate observed-tip injection.

No implementation exists at this RED checkpoint.

~~~

## FINAL IMPLEMENTATION

PATH: tools/obsidian_projection/rpe04_real_remote_observation_adapter_v0_1.py

~~~python
"""RPE-04 V0.1: governed single-fetch remote observation adapter.

Qualification surface: local bare remote only. No GitHub polling, remote push,
queue mutation, evaluation, promotion, publication, Vault, or CURRENT authority.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import shutil
import stat
import subprocess
import time
from pathlib import Path
from typing import Final


_ROOT: Final = Path(__file__).resolve().parents[2]
_PREREG_PATH: Final = _ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_preregistration_v0_1.json"
_SCHEMA_PATH: Final = _ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_preregistration_v0_1_schema_v0_1.json"
_GUARD_PATH: Final = _ROOT / "tools/obsidian_projection/rpe01_governed_closed_schema.py"
_RPE03_PATH: Final = _ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py"
_SHA40_RE: Final = re.compile(r"[0-9a-f]{40}\Z")

_EXPECTED_RUNTIME_SHA256: Final = {
    "preregistration": "0c59111fe90b8d80f0c41daf0911d772274eca733c6e68673d484ab8abf2c6ba",
    "schema": "e39dbc4f3bc82f5d5c2181574bdd120ad6d0fca46bcfdf358fac406b572a8861",
    "rpe01_guard": "24b36f5b3c0a02bc6247732fe1fa23d6c0fe30bc2b1629a7c54d4c094a628298",
    "rpe03_classifier": "cbcb996199b06859d257cc194e673a6bc51419890dc0641b42837d3f7cfcb0c3",
}


def _raw_sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _verify_runtime_bindings() -> bool:
    expected = {
        _PREREG_PATH: _EXPECTED_RUNTIME_SHA256["preregistration"],
        _SCHEMA_PATH: _EXPECTED_RUNTIME_SHA256["schema"],
        _GUARD_PATH: _EXPECTED_RUNTIME_SHA256["rpe01_guard"],
        _RPE03_PATH: _EXPECTED_RUNTIME_SHA256["rpe03_classifier"],
    }
    try:
        return all(path.is_file() and _raw_sha256_file(path) == digest for path, digest in expected.items())
    except (OSError, ValueError):
        return False


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load governed dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_preregistration() -> dict:
    if not _verify_runtime_bindings():
        raise RuntimeError("RPE04_RUNTIME_BINDING_MISMATCH")
    guard = _load_module(_GUARD_PATH, "rpe04_rpe01_guard")
    raw_document = _PREREG_PATH.read_text(encoding="utf-8")
    raw_schema = _SCHEMA_PATH.read_text(encoding="utf-8")
    validated = guard.validate_governed_json(raw_document, raw_schema)
    if type(validated) is not dict:
        raise RuntimeError("governed preregistration did not validate to an object")
    return validated


_CFG: Final = _load_preregistration()
_RPE03: Final = _load_module(_RPE03_PATH, "rpe04_bound_rpe03_classifier")

_GIT: Final = Path(_CFG["git_executable"]["resolved_path"])
_SOURCE: Final = Path(_CFG["qualification_environment"]["source_bare_repository"])
_OBSERVER: Final = Path(_CFG["qualification_environment"]["observer_bare_repository"])
_SOURCE_REF: Final = _CFG["remote_transaction"]["source_ref"]
_LOCAL_REF: Final = _CFG["remote_transaction"]["isolated_local_ref"]
_TIMEOUT_SECONDS: Final = _CFG["remote_transaction"]["timeout_milliseconds"] / 1000


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(str(left.resolve(strict=False))) == os.path.normcase(
        str(right.resolve(strict=False))
    )


def _build_git_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(
        {
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "NUL",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
        }
    )
    return env


def _verify_git_executable_identity() -> bool:
    try:
        if not _GIT.is_file():
            return False
        if _sha256_file(_GIT) != _CFG["git_executable"]["sha256"]:
            return False
        resolved_token = shutil.which("git", path=os.environ.get("PATH"))
        if resolved_token is None or not _same_path(Path(resolved_token), _GIT):
            return False
        cp = subprocess.run(
            [str(_GIT), "--version"],
            env=_build_git_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
        return (
            cp.returncode == 0
            and cp.stdout.strip() == _CFG["git_executable"]["observed_version"]
        )
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False


def _is_indirection(path: Path) -> bool:
    try:
        if path.is_symlink():
            return True
        isjunction = getattr(os.path, "isjunction", None)
        if isjunction is not None and isjunction(path):
            return True
        attrs = getattr(os.lstat(path), "st_file_attributes", 0)
        reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        return bool(reparse and attrs & reparse)
    except (OSError, ValueError):
        return True


def _verify_physical_object_domain(repo_path: Path) -> tuple[bool, str | None]:
    try:
        repo = repo_path.resolve(strict=True)
    except (OSError, RuntimeError):
        return False, "PHYSICAL_OBJECT_DOMAIN_UNPROVABLE"
    required = [
        repo_path,
        repo_path / "objects",
        repo_path / "objects" / "pack",
        repo_path / "objects" / "info",
    ]
    for path in required:
        try:
            if not path.exists() or not path.is_dir():
                return False, "PHYSICAL_OBJECT_DOMAIN_REQUIRED_PATH_MISSING"
            if _is_indirection(path):
                return False, "PHYSICAL_OBJECT_DOMAIN_INDIRECTION"
            resolved = path.resolve(strict=True)
            if path == repo_path:
                if os.path.normcase(str(resolved)) != os.path.normcase(str(repo)):
                    return False, "PHYSICAL_OBJECT_DOMAIN_INDIRECTION"
            elif repo not in resolved.parents:
                return False, "PHYSICAL_OBJECT_DOMAIN_ESCAPE"
        except (OSError, RuntimeError):
            return False, "PHYSICAL_OBJECT_DOMAIN_UNPROVABLE"
    return True, None


def _run_local_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(_GIT), "-c", "core.hooksPath=NUL", "-c", "gc.auto=0", f"--git-dir={_OBSERVER}", *args],
        env=_build_git_env(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=_TIMEOUT_SECONDS,
        check=False,
    )


def _verify_local_config_allowlist() -> bool:
    try:
        cp = subprocess.run(
            [str(_GIT), f"--git-dir={_OBSERVER}", "config", "--local", "--no-includes", "--list"],
            env=_build_git_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False
    if cp.returncode != 0:
        return False
    observed = [line.strip() for line in cp.stdout.splitlines() if line.strip()]
    expected = _CFG["git_environment_isolation"]["local_config_allowlist"]
    return len(observed) == len(expected) and set(observed) == set(expected)


def _verify_remote_identity() -> bool:
    try:
        if not _SOURCE.exists() or not _SOURCE.is_dir() or _is_indirection(_SOURCE):
            return False
        cp = subprocess.run(
            [str(_GIT), f"--git-dir={_SOURCE}", "rev-parse", "--is-bare-repository"],
            env=_build_git_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
        return cp.returncode == 0 and cp.stdout.strip() == "true"
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False


def _build_fetch_argv() -> list[str]:
    return [
        str(_GIT),
        "-c",
        "core.hooksPath=NUL",
        "-c",
        "gc.auto=0",
        f"--git-dir={_OBSERVER}",
        "fetch",
        "--no-tags",
        "--no-recurse-submodules",
        "--no-write-fetch-head",
        "--",
        str(_SOURCE),
        f"+{_SOURCE_REF}:{_LOCAL_REF}",
    ]


def _render_command(argv: list[str]) -> str:
    return " ".join(f'"{x}"' if (" " in x or "\\" in x) else x for x in argv)


def _fetch_contract_exact() -> bool:
    return _render_command(_build_fetch_argv()) == _CFG["remote_transaction"]["fetch_command_exact"]


def _run_fetch() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        _build_fetch_argv(),
        env=_build_git_env(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=_TIMEOUT_SECONDS,
        check=False,
    )


def _namespace_refs() -> list[str] | None:
    try:
        cp = _run_local_git("for-each-ref", "--format=%(refname)", "refs/rpe04")
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    if cp.returncode != 0:
        return None
    return [line.strip() for line in cp.stdout.splitlines() if line.strip()]


def _extract_observed_sha() -> str | None:
    try:
        cp = _run_local_git("rev-parse", "--verify", f"{_LOCAL_REF}^{{commit}}")
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    if cp.returncode != 0:
        return None
    return cp.stdout.strip()


def _materialized_commit(sha: str) -> bool:
    try:
        cp = _run_local_git("cat-file", "-t", sha)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False
    return cp.returncode == 0 and cp.stdout.strip() == "commit"


def _failure(
    code: str,
    attempt_started_at_ns: int | None = None,
    remote_observation_completed_at_ns: int | None = None,
) -> dict:
    return {
        "outcome": "READ_FAILURE",
        "failure_code": code,
        "observed_head": None,
        "attempt_started_at_ns": attempt_started_at_ns,
        "remote_observation_completed_at_ns": remote_observation_completed_at_ns,
        "attempt_completed_at_ns": time.monotonic_ns(),
    }


def observe_once(previous_observed_head):
    """Perform one governed local-bare remote observation attempt."""
    if not _verify_git_executable_identity():
        return _failure("GIT_EXECUTABLE_IDENTITY_MISMATCH")

    ok, code = _verify_physical_object_domain(_OBSERVER)
    if not ok:
        return _failure(code or "PHYSICAL_OBJECT_DOMAIN_UNPROVABLE")

    if not _verify_local_config_allowlist():
        return _failure("LOCAL_CONFIG_NOT_ALLOWLISTED")

    if not _verify_remote_identity():
        return _failure("REMOTE_IDENTITY_UNPROVABLE")

    if not _fetch_contract_exact():
        return _failure("FETCH_CONTRACT_MISMATCH")

    attempt_started_at_ns = time.monotonic_ns()
    try:
        fetch = _run_fetch()
    except subprocess.TimeoutExpired:
        remote_done = time.monotonic_ns()
        return _failure("REMOTE_FETCH_TIMEOUT", attempt_started_at_ns, remote_done)
    except (OSError, ValueError):
        remote_done = time.monotonic_ns()
        return _failure("REMOTE_FETCH_EXECUTION_ERROR", attempt_started_at_ns, remote_done)

    remote_done = time.monotonic_ns()
    if fetch.returncode != 0:
        return _failure("REMOTE_FETCH_FAILED", attempt_started_at_ns, remote_done)

    ok, code = _verify_physical_object_domain(_OBSERVER)
    if not ok:
        return _failure(code or "PHYSICAL_OBJECT_DOMAIN_UNPROVABLE", attempt_started_at_ns, remote_done)

    if not _verify_local_config_allowlist():
        return _failure("LOCAL_CONFIG_NOT_ALLOWLISTED", attempt_started_at_ns, remote_done)

    refs = _namespace_refs()
    if refs != [_LOCAL_REF]:
        return _failure("UNEXPECTED_OBSERVATION_NAMESPACE", attempt_started_at_ns, remote_done)

    observed_head = _extract_observed_sha()
    if type(observed_head) is not str or _SHA40_RE.fullmatch(observed_head) is None:
        return _failure("MALFORMED_OBSERVED_SHA", attempt_started_at_ns, remote_done)

    if not _materialized_commit(observed_head):
        return _failure("OBSERVED_SHA_NOT_MATERIALIZED", attempt_started_at_ns, remote_done)

    if not _verify_runtime_bindings():
        return _failure("RUNTIME_BINDING_MISMATCH", attempt_started_at_ns, remote_done)

    if not _verify_git_executable_identity():
        return _failure("GIT_EXECUTABLE_IDENTITY_MISMATCH", attempt_started_at_ns, remote_done)

    transition = _RPE03.classify_transition(
        _OBSERVER,
        previous_observed_head,
        observed_head,
    )

    event = {
        "outcome": "REMOTE_HEAD_OBSERVED",
        "event_type": "REMOTE_HEAD_OBSERVED",
        "evidence_label": "OBSERVED_REMOTE_TIP",
        "observed_head": observed_head,
        "transition_class": transition,
        "attempt_started_at_ns": attempt_started_at_ns,
        "remote_observation_completed_at_ns": remote_done,
        "attempt_completed_at_ns": 0,
        "blocked": transition == "UNKNOWN",
        "failure_code": "ANCESTRY_UNKNOWN" if transition == "UNKNOWN" else None,
    }
    event["attempt_completed_at_ns"] = time.monotonic_ns()
    return event

~~~

## MUTATION TEST

PATH: tests/obsidian_projection/test_rpe04_real_remote_observation_adapter_mutation_v0_1.py

~~~python
from __future__ import annotations

import os
import pathlib
import subprocess
import tempfile
import types
import unittest
from unittest import mock

from tests.obsidian_projection.test_rpe04_real_remote_observation_adapter_v0_1 import (
    GIT,
    OBSERVER,
    SOURCE,
    SOURCE_REF,
    init_fixture,
    git,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_v0_1.py"


def load_source_module(name: str, replacements=()):
    source = MODULE.read_text(encoding="utf-8")
    for old, new in replacements:
        if source.count(old) != 1:
            raise AssertionError(f"mutation anchor count != 1: {old!r}")
        source = source.replace(old, new, 1)
    module = types.ModuleType(name)
    module.__file__ = str(MODULE)
    exec(compile(source, str(MODULE), "exec"), module.__dict__)
    return module


class TestRPE04MutationSweep(unittest.TestCase):
    def setUp(self):
        self.a = init_fixture()

    def tearDown(self):
        import shutil
        shutil.rmtree(SOURCE.parent, ignore_errors=True)

    def test_mutant_removing_git_hash_binding_is_detected(self):
        m = load_source_module(
            "rpe04_mut_hash",
            ((
                '        if _sha256_file(_GIT) != _CFG["git_executable"]["sha256"]:\n'
                '            return False\n',
                '        if False:\n'
                '            return False\n',
            ),),
        )
        with mock.patch.object(m, "_sha256_file", return_value="0" * 64):
            self.assertTrue(m._verify_git_executable_identity())

    def test_mutant_removing_path_token_binding_is_detected(self):
        m = load_source_module(
            "rpe04_mut_which",
            ((
                '        if resolved_token is None or not _same_path(Path(resolved_token), _GIT):\n'
                '            return False\n',
                '        if False:\n'
                '            return False\n',
            ),),
        )
        with mock.patch.object(m.shutil, "which", return_value=r"C:\evil\git.exe"):
            self.assertTrue(m._verify_git_executable_identity())

    def test_mutant_preserving_inherited_git_environment_is_detected(self):
        base = load_source_module("rpe04_base_env")
        m = load_source_module(
            "rpe04_mut_env",
            ((
                '    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\n',
                '    env = dict(os.environ)\n',
            ),),
        )
        with mock.patch.dict(os.environ, {"GIT_DIR": "evil"}, clear=False):
            self.assertNotIn("GIT_DIR", base._build_git_env())
            self.assertEqual(m._build_git_env()["GIT_DIR"], "evil")

    def test_mutant_bypassing_local_config_allowlist_is_detected(self):
        m = load_source_module(
            "rpe04_mut_config",
            ((
                '    return len(observed) == len(expected) and set(observed) == set(expected)\n',
                '    return True\n',
            ),),
        )
        git(f"--git-dir={OBSERVER}", "config", "--local", "include.path", r"C:\evil-rpe04.cfg")
        out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")

    def test_mutant_ignoring_unexpected_namespace_ref_is_detected(self):
        m = load_source_module(
            "rpe04_mut_namespace",
            ((
                '    if refs != [_LOCAL_REF]:\n',
                '    if False:\n',
            ),),
        )
        first = m.observe_once(None)
        self.assertEqual(first["outcome"], "REMOTE_HEAD_OBSERVED")
        git(f"--git-dir={OBSERVER}", "update-ref", "refs/rpe04/extra", self.a)
        out = m.observe_once(self.a)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")

    def test_mutant_skipping_materialization_proof_is_detected(self):
        m = load_source_module(
            "rpe04_mut_materialized",
            ((
                '    if not _materialized_commit(observed_head):\n',
                '    if False:\n',
            ),),
        )
        with mock.patch.object(m, "_extract_observed_sha", return_value="f" * 40):
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertEqual(out["transition_class"], "UNKNOWN")

    def test_mutant_laundering_unknown_as_fast_forward_is_detected(self):
        m = load_source_module(
            "rpe04_mut_transition",
            ((
                '    transition = _RPE03.classify_transition(\n'
                '        _OBSERVER,\n'
                '        previous_observed_head,\n'
                '        observed_head,\n'
                '    )\n',
                '    transition = "FAST_FORWARD"\n',
            ),),
        )
        out = m.observe_once("f" * 40)
        self.assertEqual(out["transition_class"], "FAST_FORWARD")
        self.assertFalse(out["blocked"])

    def test_mutant_dropping_no_write_fetch_head_breaks_exact_contract(self):
        m = load_source_module(
            "rpe04_mut_fetchhead",
            (('        "--no-write-fetch-head",\n', ''),),
        )
        self.assertNotIn("--no-write-fetch-head", m._build_fetch_argv())
        self.assertFalse(m._fetch_contract_exact())

    def test_mutant_dropping_local_plus_breaks_exact_contract(self):
        m = load_source_module(
            "rpe04_mut_plus",
            ((
                '        f"+{_SOURCE_REF}:{_LOCAL_REF}",\n',
                '        f"{_SOURCE_REF}:{_LOCAL_REF}",\n',
            ),),
        )
        self.assertFalse(m._fetch_contract_exact())

    def test_mutant_accepting_physical_escape_is_detected(self):
        m = load_source_module(
            "rpe04_mut_physical",
            (
                (
                    '            if _is_indirection(path):\n'
                    '                return False, "PHYSICAL_OBJECT_DOMAIN_INDIRECTION"\n',
                    '            if False:\n'
                    '                return False, "PHYSICAL_OBJECT_DOMAIN_INDIRECTION"\n',
                ),
                (
                    '            elif repo not in resolved.parents:\n'
                    '                return False, "PHYSICAL_OBJECT_DOMAIN_ESCAPE"\n',
                    '            elif False:\n'
                    '                return False, "PHYSICAL_OBJECT_DOMAIN_ESCAPE"\n',
                ),
            ),
        )
        with tempfile.TemporaryDirectory(prefix="rpe04-mut-link-") as td:
            td = pathlib.Path(td)
            fake = td / "fake.git"
            target = td / "outside-objects"
            fake.mkdir()
            target.mkdir()
            (target / "pack").mkdir()
            (target / "info").mkdir()
            link = fake / "objects"
            made = False
            try:
                os.symlink(target, link, target_is_directory=True)
                made = True
            except (OSError, NotImplementedError):
                cp = subprocess.run(
                    ["cmd.exe", "/c", "mklink", "/J", str(link), str(target)],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                made = cp.returncode == 0
            if not made:
                self.skipTest("platform cannot create symlink or junction")
            ok, code = m._verify_physical_object_domain(fake)
            self.assertTrue(ok, code)

    def test_mutant_accepting_uppercase_sha_is_detected(self):
        m = load_source_module(
            "rpe04_mut_sha",
            ((
                '    if type(observed_head) is not str or _SHA40_RE.fullmatch(observed_head) is None:\n',
                '    if False:\n',
            ),),
        )
        with mock.patch.object(m, "_extract_observed_sha", return_value=self.a.upper()):
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")


if __name__ == "__main__":
    unittest.main()

~~~

## HARDENING TEST

PATH: tests/obsidian_projection/test_rpe04_runtime_binding_hardening_v0_1.py

~~~python
from __future__ import annotations

import importlib.util
import pathlib
import unittest
from unittest import mock

from tests.obsidian_projection.test_rpe04_real_remote_observation_adapter_v0_1 import (
    init_fixture,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_v0_1.py"


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TestRPE04RuntimeBindingHardening(unittest.TestCase):
    def setUp(self):
        self.a = init_fixture()

    def tearDown(self):
        import shutil
        shutil.rmtree(
            pathlib.Path(r"C:\Users\Boulevart\ATDS-CONTROL\RPE04-QUALIFICATION"),
            ignore_errors=True,
        )

    def test_governed_runtime_dependencies_are_raw_sha256_bound(self):
        m = load_module("rpe04_binding_base")
        self.assertTrue(m._verify_runtime_bindings())
        self.assertEqual(
            m._EXPECTED_RUNTIME_SHA256["preregistration"],
            "0c59111fe90b8d80f0c41daf0911d772274eca733c6e68673d484ab8abf2c6ba",
        )
        self.assertEqual(
            m._EXPECTED_RUNTIME_SHA256["schema"],
            "e39dbc4f3bc82f5d5c2181574bdd120ad6d0fca46bcfdf358fac406b572a8861",
        )
        self.assertEqual(
            m._EXPECTED_RUNTIME_SHA256["rpe01_guard"],
            "24b36f5b3c0a02bc6247732fe1fa23d6c0fe30bc2b1629a7c54d4c094a628298",
        )
        self.assertEqual(
            m._EXPECTED_RUNTIME_SHA256["rpe03_classifier"],
            "cbcb996199b06859d257cc194e673a6bc51419890dc0641b42837d3f7cfcb0c3",
        )

    def test_runtime_binding_mismatch_fails_closed(self):
        m = load_module("rpe04_binding_mut")
        original = m._sha256_file

        def fake(path):
            if pathlib.Path(path) == m._RPE03_PATH:
                return "0" * 64
            return original(path)

        with mock.patch.object(m, "_raw_sha256_file", side_effect=fake):
            self.assertFalse(m._verify_runtime_bindings())

    def test_physical_domain_is_reverified_after_fetch(self):
        m = load_module("rpe04_binding_physical")
        with mock.patch.object(
            m,
            "_verify_physical_object_domain",
            wraps=m._verify_physical_object_domain,
        ) as wrapped:
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertGreaterEqual(wrapped.call_count, 2)

    def test_git_identity_is_reverified_before_rpe03_classification(self):
        m = load_module("rpe04_binding_git")
        with mock.patch.object(
            m,
            "_verify_git_executable_identity",
            wraps=m._verify_git_executable_identity,
        ) as wrapped:
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertGreaterEqual(wrapped.call_count, 2)

    def test_local_config_is_reverified_before_rpe03_classification(self):
        m = load_module("rpe04_binding_config")
        with mock.patch.object(
            m,
            "_verify_local_config_allowlist",
            wraps=m._verify_local_config_allowlist,
        ) as wrapped:
            out = m.observe_once(None)
        self.assertEqual(out["outcome"], "REMOTE_HEAD_OBSERVED")
        self.assertGreaterEqual(wrapped.call_count, 2)


if __name__ == "__main__":
    unittest.main()

~~~

## HARDENING RED REPORT

PATH: reports/program/2026-10-04-OBSIDIAN-REAL-P5E-RPE04-RUNTIME-BINDING-HARDENING-RED.md

~~~text
# RPE-04 — RUNTIME BINDING + POST-FETCH REVALIDATION HARDENING — RED

Date: 2026-10-04

## Why this hardening exists

A self-audit before external review identified that the candidate loaded the governed preregistration/schema and the adopted RPE-01/RPE-03 code from disk without independently binding the exact bytes consumed at runtime.

The audit also identified a small time-of-check/time-of-use surface between the pre-fetch checks and the RPE-03 classification.

No external reviewer finding was required to identify these issues.

## Frozen hardening test

tests/obsidian_projection/test_rpe04_runtime_binding_hardening_v0_1.py

Worktree blob before persistence:

d1bf928dd205a4d6c47761cf0a535aa5b315f10a

## RED result

Ran 5 tests.

- 2 ERROR: runtime binding function/identity map absent.
- 3 FAIL: Git identity, local-config allowlist, and physical object-domain checks occur only once before fetch.

HARDENING_RED_EXIT = 1

## Required closure

The implementation must:
- bind the raw SHA-256 bytes of the exact preregistration, schema, RPE-01 guard, and RPE-03 classifier it reads;
- fail closed on any runtime binding mismatch;
- reverify physical object-domain containment after fetch;
- reverify exact Git executable identity before RPE-03 classification;
- reverify local config allowlist before RPE-03 classification.

No claim scope or authority expansion is introduced.

~~~

## HARDENING TEST CORRECTION

PATH: reports/program/2026-10-04-OBSIDIAN-REAL-P5E-RPE04-HARDENING-TEST-CORRECTION-ADJUDICATION.md

~~~text
# RPE-04 — HARDENING TEST CORRECTION — INTERNAL ADJUDICATION

Date: 2026-10-04

The frozen hardening RED test blob was:

d1bf928dd205a4d6c47761cf0a535aa5b315f10a

After implementing the runtime-binding requirement, 4/5 hardening tests became GREEN.

The remaining test failed because the test monkeypatched the pre-existing helper named _sha256_file, while the new runtime dependency binding intentionally uses a distinct helper named _raw_sha256_file.

This is a test harness defect. The requirement remains unchanged:
a mismatched runtime dependency digest must make _verify_runtime_bindings() return false.

Authorized correction:
- replace only the monkeypatch target _sha256_file with _raw_sha256_file;
- change no expected verdict;
- change no implementation requirement;
- change no authority or claim scope.

Corrected hardening test worktree blob:

aeab0dd79b2e90d108525323ac401c062cc49ec8

~~~

## TIMEOUT RECOVERY RECONCILIATION

PATH: reports/program/2026-10-04-OBSIDIAN-REAL-P5E-RPE04-TIMEOUT-RECOVERY-RECONCILIATION.md

~~~text
# RPE-04 — TIMEOUT RECOVERY RECONCILIATION

Date: 2026-10-04

The chat/UI timed out while authorized RPE-04 tool operations were still executing on the remote machine.

Git history and Remote Desktop Commander call history show that the prior authorized execution continued and produced:
- preregistration correction;
- historical RED persistence;
- initial implementation;
- runtime-binding hardening RED;
- hardening test-harness correction;
- final hardening GREEN;
- final dedicated RPE-04 result: 40/40 PASS;
- final targeted regression result: 242/242 PASS;
- final tested implementation worktree blob: 3492006ebee581c205b2c26d4ea98efab72d522a.

During recovery, a later duplicate attempt rewrote the RED report content in commit f429e98 without changing the frozen RED test. This reconciliation restores the historical RED report bytes from commit 107bdfd:
036383b58ae0149047870b6b0d000addba30e81b

No reset, force, history rewrite, network qualification, RPE-05 opening, RPE-06 opening, or REAL P5-E authority is introduced.

The recovery rule is:
REAL REPOSITORY STATE + EXECUTION EVIDENCE > UI TIMEOUT STATE.

~~~

## QUALIFICATION

PATH: tools/obsidian_projection/rpe04_real_remote_observation_adapter_qualification_v0_1.json

~~~json
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE04_REAL_REMOTE_OBSERVATION_ADAPTER_QUALIFICATION_V0_1",
  "status": "QUALIFIED_FOR_EXTERNAL_REVIEW",
  "date": "2026-10-04",
  "branch": "feat/obsidian-projection-rpe04-real-remote-observation-adapter-v0.1",
  "lineage": {
    "rpe02_human_adopted_parent": "7cb120b3c12efdb26a5938b4c2395650d00394b6",
    "rpe03_dependency_import_head": "c66daeb78f05a9f0e936fe4058d715f8d76d082d",
    "initial_preregistration_head": "5fba272905793ca4ac86ac5ba9ceb2803adda8bc",
    "historical_red_head": "107bdfd4ad3d865c60e2840ff28c41a693999a31",
    "preregistration_correction_head": "61c58406a344bdbbc6fef45201333f6d6d88a274",
    "initial_implementation_head": "2667b1487147bab0521a8555d5b699eaa18149bd",
    "runtime_binding_hardening_red_head": "6a1aeda",
    "hardening_test_harness_correction_head": "366a11e",
    "timeout_recovery_duplicate_commit": "f429e98",
    "final_hardening_reconciliation_head": "3de1d5ad5270eaa385c98cde90c7c153b347d62e"
  },
  "exact_identities": {
    "rpe01_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887",
    "rpe02_model_blob": "31db5d944a25e54db81bd901a087cdc2039925ad",
    "rpe03_classifier_blob": "145b3112fd9309cc34d95a62c091cb6a6bc3bb11",
    "final_implementation_blob": "3492006ebee581c205b2c26d4ea98efab72d522a",
    "frozen_red_test_blob": "eec1d9b39714b5e841438fc76180d851b6494bce",
    "historical_red_report_blob": "036383b58ae0149047870b6b0d000addba30e81b",
    "mutation_test_blob": "3bccfb5f96e6c112f6a5c40fcb43bb5ebf2385c6",
    "hardening_test_blob": "aeab0dd79b2e90d108525323ac401c062cc49ec8",
    "corrected_preregistration_blob": "bd4541bdc1c790b7936034ec4747f1cfb5e23f73",
    "corrected_schema_blob": "9522d851d01c7948e81e0999c3a7cc907d7a4e5e",
    "preregistration_correction_report_blob": "2994712837db75dee8aa36cc089e566fd1fe9c10",
    "hardening_red_report_blob": "25f1b6cfcdbfbd7679598f95fd1675fa2397c185",
    "hardening_test_correction_adjudication_blob": "b4f4eed940ad24d2a53d68b9bba3e4c2f7f8f7b9",
    "timeout_recovery_reconciliation_blob": "5560e54d79e9d61d19c53d371e0587b8392cdd20",
    "p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
    "p5e_synthetic_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5"
  },
  "runtime_binding_raw_sha256": {
    "preregistration": "0c59111fe90b8d80f0c41daf0911d772274eca733c6e68673d484ab8abf2c6ba",
    "schema": "e39dbc4f3bc82f5d5c2181574bdd120ad6d0fca46bcfdf358fac406b572a8861",
    "rpe01_guard": "24b36f5b3c0a02bc6247732fe1fa23d6c0fe30bc2b1629a7c54d4c094a628298",
    "rpe03_classifier": "cbcb996199b06859d257cc194e673a6bc51419890dc0641b42837d3f7cfcb0c3"
  },
  "qualification_environment": {
    "git_path": "C:\\Program Files\\Git\\cmd\\git.exe",
    "git_sha256": "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5",
    "git_version": "git version 2.54.0.windows.1",
    "python_version": "Python 3.13.14",
    "network_mode": "LOCAL_BARE_REMOTE_ONLY_NO_GITHUB_POLLING"
  },
  "evidence": {
    "historical_red": "24 tests / 2 PASS / 22 FAIL due implementation absent",
    "initial_dedicated_green": "35/35 PASS",
    "initial_mutation_sweep": "11/11 PASS",
    "initial_full_targeted_regression": "237/237 PASS",
    "hardening_red": "5 tests / 2 ERROR / 3 FAIL",
    "hardening_green": "5/5 PASS",
    "final_dedicated_rpe04": "40/40 PASS",
    "final_full_targeted_regression": "242/242 PASS",
    "rpe01_guard_validation": "PASS"
  },
  "qualified_semantics": {
    "one_governed_fetch_transaction_per_attempt": true,
    "exact_observed_sha_only": true,
    "observed_tip_not_contained_history": true,
    "local_non_fast_forward_namespace_update": true,
    "git_executable_identity_bound": true,
    "governed_runtime_dependency_bytes_bound": true,
    "inherited_git_authority_neutralized": true,
    "local_config_allowlisted": true,
    "physical_object_domain_indirection_rejected": true,
    "physical_object_domain_revalidated_after_fetch": true,
    "git_identity_revalidated_before_rpe03": true,
    "local_config_revalidated_before_rpe03": true,
    "rpe02_integer_monotonic_ns_handoff": true,
    "rpe03_transition_only_derived": true,
    "rpe03_unknown_blocks_positive_transition": true
  },
  "claim_boundary": {
    "rpe04_local_adapter_semantics_qualified": true,
    "real_p5e_qualified": false,
    "real_60_second_sla_qualified": false,
    "production_github_polling_qualified": false,
    "production_remote_adapter_configuration_qualified": false
  },
  "authority_boundary": {
    "rpe04_human_adopted": false,
    "rpe05_opened": false,
    "rpe06_opened": false,
    "real_p5e_opened": false,
    "github_polling_authorized": false,
    "github_fetch_qualification_authorized": false,
    "remote_push_authorized": false,
    "p5d4_real_state_mutation_authorized": false,
    "vault_or_current_mutation_authorized": false
  },
  "next_gate": "EXTERNAL_ADVERSARIAL_REVIEW_THEN_HUMAN_ADJUDICATION",
  "stop": true
}

~~~

## QUALIFICATION SCHEMA

PATH: tools/obsidian_projection/rpe04_real_remote_observation_adapter_qualification_v0_1_schema_v0_1.json

~~~json
{
  "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
  "artifact_role": "RPE04_REAL_REMOTE_OBSERVATION_ADAPTER_QUALIFICATION",
  "root": {
    "kind": "object",
    "fields": {
      "schema": {
        "kind": "string",
        "const": "ATDS_OBSIDIAN_REAL_P5E_RPE04_REAL_REMOTE_OBSERVATION_ADAPTER_QUALIFICATION_V0_1"
      },
      "status": {
        "kind": "string",
        "const": "QUALIFIED_FOR_EXTERNAL_REVIEW"
      },
      "date": {
        "kind": "string",
        "const": "2026-10-04"
      },
      "branch": {
        "kind": "string",
        "const": "feat/obsidian-projection-rpe04-real-remote-observation-adapter-v0.1"
      },
      "lineage": {
        "kind": "object",
        "fields": {
          "rpe02_human_adopted_parent": {
            "kind": "string",
            "const": "7cb120b3c12efdb26a5938b4c2395650d00394b6"
          },
          "rpe03_dependency_import_head": {
            "kind": "string",
            "const": "c66daeb78f05a9f0e936fe4058d715f8d76d082d"
          },
          "initial_preregistration_head": {
            "kind": "string",
            "const": "5fba272905793ca4ac86ac5ba9ceb2803adda8bc"
          },
          "historical_red_head": {
            "kind": "string",
            "const": "107bdfd4ad3d865c60e2840ff28c41a693999a31"
          },
          "preregistration_correction_head": {
            "kind": "string",
            "const": "61c58406a344bdbbc6fef45201333f6d6d88a274"
          },
          "initial_implementation_head": {
            "kind": "string",
            "const": "2667b1487147bab0521a8555d5b699eaa18149bd"
          },
          "runtime_binding_hardening_red_head": {
            "kind": "string",
            "const": "6a1aeda"
          },
          "hardening_test_harness_correction_head": {
            "kind": "string",
            "const": "366a11e"
          },
          "timeout_recovery_duplicate_commit": {
            "kind": "string",
            "const": "f429e98"
          },
          "final_hardening_reconciliation_head": {
            "kind": "string",
            "const": "3de1d5ad5270eaa385c98cde90c7c153b347d62e"
          }
        }
      },
      "exact_identities": {
        "kind": "object",
        "fields": {
          "rpe01_guard_blob": {
            "kind": "string",
            "const": "26f977961d72a062199d71ffd628d5a5cc047887"
          },
          "rpe02_model_blob": {
            "kind": "string",
            "const": "31db5d944a25e54db81bd901a087cdc2039925ad"
          },
          "rpe03_classifier_blob": {
            "kind": "string",
            "const": "145b3112fd9309cc34d95a62c091cb6a6bc3bb11"
          },
          "final_implementation_blob": {
            "kind": "string",
            "const": "3492006ebee581c205b2c26d4ea98efab72d522a"
          },
          "frozen_red_test_blob": {
            "kind": "string",
            "const": "eec1d9b39714b5e841438fc76180d851b6494bce"
          },
          "historical_red_report_blob": {
            "kind": "string",
            "const": "036383b58ae0149047870b6b0d000addba30e81b"
          },
          "mutation_test_blob": {
            "kind": "string",
            "const": "3bccfb5f96e6c112f6a5c40fcb43bb5ebf2385c6"
          },
          "hardening_test_blob": {
            "kind": "string",
            "const": "aeab0dd79b2e90d108525323ac401c062cc49ec8"
          },
          "corrected_preregistration_blob": {
            "kind": "string",
            "const": "bd4541bdc1c790b7936034ec4747f1cfb5e23f73"
          },
          "corrected_schema_blob": {
            "kind": "string",
            "const": "9522d851d01c7948e81e0999c3a7cc907d7a4e5e"
          },
          "preregistration_correction_report_blob": {
            "kind": "string",
            "const": "2994712837db75dee8aa36cc089e566fd1fe9c10"
          },
          "hardening_red_report_blob": {
            "kind": "string",
            "const": "25f1b6cfcdbfbd7679598f95fd1675fa2397c185"
          },
          "hardening_test_correction_adjudication_blob": {
            "kind": "string",
            "const": "b4f4eed940ad24d2a53d68b9bba3e4c2f7f8f7b9"
          },
          "timeout_recovery_reconciliation_blob": {
            "kind": "string",
            "const": "5560e54d79e9d61d19c53d371e0587b8392cdd20"
          },
          "p5e_contract_blob": {
            "kind": "string",
            "const": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9"
          },
          "p5e_synthetic_model_blob": {
            "kind": "string",
            "const": "c0f16baa151c1466e30ba5778f1fca8184cd4aac"
          },
          "p5d4_runtime_blob": {
            "kind": "string",
            "const": "1825e53d195ba2a63b5b646a5b78eb77939b94b5"
          }
        }
      },
      "runtime_binding_raw_sha256": {
        "kind": "object",
        "fields": {
          "preregistration": {
            "kind": "string",
            "const": "0c59111fe90b8d80f0c41daf0911d772274eca733c6e68673d484ab8abf2c6ba"
          },
          "schema": {
            "kind": "string",
            "const": "e39dbc4f3bc82f5d5c2181574bdd120ad6d0fca46bcfdf358fac406b572a8861"
          },
          "rpe01_guard": {
            "kind": "string",
            "const": "24b36f5b3c0a02bc6247732fe1fa23d6c0fe30bc2b1629a7c54d4c094a628298"
          },
          "rpe03_classifier": {
            "kind": "string",
            "const": "cbcb996199b06859d257cc194e673a6bc51419890dc0641b42837d3f7cfcb0c3"
          }
        }
      },
      "qualification_environment": {
        "kind": "object",
        "fields": {
          "git_path": {
            "kind": "string",
            "const": "C:\\Program Files\\Git\\cmd\\git.exe"
          },
          "git_sha256": {
            "kind": "string",
            "const": "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5"
          },
          "git_version": {
            "kind": "string",
            "const": "git version 2.54.0.windows.1"
          },
          "python_version": {
            "kind": "string",
            "const": "Python 3.13.14"
          },
          "network_mode": {
            "kind": "string",
            "const": "LOCAL_BARE_REMOTE_ONLY_NO_GITHUB_POLLING"
          }
        }
      },
      "evidence": {
        "kind": "object",
        "fields": {
          "historical_red": {
            "kind": "string",
            "const": "24 tests / 2 PASS / 22 FAIL due implementation absent"
          },
          "initial_dedicated_green": {
            "kind": "string",
            "const": "35/35 PASS"
          },
          "initial_mutation_sweep": {
            "kind": "string",
            "const": "11/11 PASS"
          },
          "initial_full_targeted_regression": {
            "kind": "string",
            "const": "237/237 PASS"
          },
          "hardening_red": {
            "kind": "string",
            "const": "5 tests / 2 ERROR / 3 FAIL"
          },
          "hardening_green": {
            "kind": "string",
            "const": "5/5 PASS"
          },
          "final_dedicated_rpe04": {
            "kind": "string",
            "const": "40/40 PASS"
          },
          "final_full_targeted_regression": {
            "kind": "string",
            "const": "242/242 PASS"
          },
          "rpe01_guard_validation": {
            "kind": "string",
            "const": "PASS"
          }
        }
      },
      "qualified_semantics": {
        "kind": "object",
        "fields": {
          "one_governed_fetch_transaction_per_attempt": {
            "kind": "boolean",
            "const": true
          },
          "exact_observed_sha_only": {
            "kind": "boolean",
            "const": true
          },
          "observed_tip_not_contained_history": {
            "kind": "boolean",
            "const": true
          },
          "local_non_fast_forward_namespace_update": {
            "kind": "boolean",
            "const": true
          },
          "git_executable_identity_bound": {
            "kind": "boolean",
            "const": true
          },
          "governed_runtime_dependency_bytes_bound": {
            "kind": "boolean",
            "const": true
          },
          "inherited_git_authority_neutralized": {
            "kind": "boolean",
            "const": true
          },
          "local_config_allowlisted": {
            "kind": "boolean",
            "const": true
          },
          "physical_object_domain_indirection_rejected": {
            "kind": "boolean",
            "const": true
          },
          "physical_object_domain_revalidated_after_fetch": {
            "kind": "boolean",
            "const": true
          },
          "git_identity_revalidated_before_rpe03": {
            "kind": "boolean",
            "const": true
          },
          "local_config_revalidated_before_rpe03": {
            "kind": "boolean",
            "const": true
          },
          "rpe02_integer_monotonic_ns_handoff": {
            "kind": "boolean",
            "const": true
          },
          "rpe03_transition_only_derived": {
            "kind": "boolean",
            "const": true
          },
          "rpe03_unknown_blocks_positive_transition": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "claim_boundary": {
        "kind": "object",
        "fields": {
          "rpe04_local_adapter_semantics_qualified": {
            "kind": "boolean",
            "const": true
          },
          "real_p5e_qualified": {
            "kind": "boolean",
            "const": false
          },
          "real_60_second_sla_qualified": {
            "kind": "boolean",
            "const": false
          },
          "production_github_polling_qualified": {
            "kind": "boolean",
            "const": false
          },
          "production_remote_adapter_configuration_qualified": {
            "kind": "boolean",
            "const": false
          }
        }
      },
      "authority_boundary": {
        "kind": "object",
        "fields": {
          "rpe04_human_adopted": {
            "kind": "boolean",
            "const": false
          },
          "rpe05_opened": {
            "kind": "boolean",
            "const": false
          },
          "rpe06_opened": {
            "kind": "boolean",
            "const": false
          },
          "real_p5e_opened": {
            "kind": "boolean",
            "const": false
          },
          "github_polling_authorized": {
            "kind": "boolean",
            "const": false
          },
          "github_fetch_qualification_authorized": {
            "kind": "boolean",
            "const": false
          },
          "remote_push_authorized": {
            "kind": "boolean",
            "const": false
          },
          "p5d4_real_state_mutation_authorized": {
            "kind": "boolean",
            "const": false
          },
          "vault_or_current_mutation_authorized": {
            "kind": "boolean",
            "const": false
          }
        }
      },
      "next_gate": {
        "kind": "string",
        "const": "EXTERNAL_ADVERSARIAL_REVIEW_THEN_HUMAN_ADJUDICATION"
      },
      "stop": {
        "kind": "boolean",
        "const": true
      }
    }
  }
}

~~~

## QUALIFICATION REPORT

PATH: reports/program/2026-10-04-OBSIDIAN-REAL-P5E-RPE04-REAL-REMOTE-OBSERVATION-ADAPTER-QUALIFICATION.md

~~~text
# RPE-04 — REAL REMOTE OBSERVATION ADAPTER V0.1 — QUALIFICATION

Date: 2026-10-04

## Result

RPE-04 = QUALIFIED_FOR_EXTERNAL_REVIEW

This is not a human adoption and does not open RPE-05.

## Final implementation identity

Final implementation blob:

3492006ebee581c205b2c26d4ea98efab72d522a

Final hardening/reconciliation HEAD:

3de1d5ad5270eaa385c98cde90c7c153b347d62e

## Evidence

Historical RED:
24 tests / 2 PASS / 22 FAIL because implementation was absent.

Initial GREEN:
35/35 dedicated PASS.

Initial mutation sweep:
11/11 PASS.

Initial targeted regression:
237/237 PASS.

Runtime-binding hardening RED:
5 tests / 2 ERROR / 3 FAIL.

Hardening GREEN:
5/5 PASS.

Final RPE-04 dedicated surface:
40/40 PASS.

Final P5-E + RPE-01 + RPE-02 + RPE-03 + RPE-04 targeted regression:
242/242 PASS.

## Qualified properties

The candidate qualifies, on local bare-remote / injected-I/O scope only:

- one governed fetch transaction per attempt;
- exact observed SHA provenance;
- OBSERVED_REMOTE_TIP distinct from contained history;
- local isolated namespace updates including NON_FAST_FORWARD;
- explicit Git executable identity;
- governed runtime dependency byte binding;
- inherited Git authority neutralization;
- closed local config allowlist;
- physical object-domain indirection rejection;
- post-fetch physical-domain revalidation;
- pre-RPE03 Git identity and local-config revalidation;
- integer monotonic-nanosecond timing handoff from RPE-02;
- transition class derived only by adopted RPE-03;
- UNKNOWN propagation without positive laundering.

## Runtime dependency binding

Raw SHA-256:

preregistration = 0c59111fe90b8d80f0c41daf0911d772274eca733c6e68673d484ab8abf2c6ba

schema = e39dbc4f3bc82f5d5c2181574bdd120ad6d0fca46bcfdf358fac406b572a8861

RPE-01 guard = 24b36f5b3c0a02bc6247732fe1fa23d6c0fe30bc2b1629a7c54d4c094a628298

RPE-03 classifier = cbcb996199b06859d257cc194e673a6bc51419890dc0641b42837d3f7cfcb0c3

## Timeout recovery

The UI timeout did not stop the authorized remote execution.

Repository history and tool-call history were reconciled. The historical RED report was restored byte-for-byte to blob:

036383b58ae0149047870b6b0d000addba30e81b

No reset, force, history rewrite or scope expansion was used.

## Claim boundary

RPE-04 QUALIFIED does not mean:

- REAL P5-E qualified;
- real 60-second SLA qualified;
- production GitHub polling qualified;
- production remote adapter configuration qualified.

## Authority boundary

RPE-05 = CLOSED

RPE-06 = CLOSED

REAL P5-E = CLOSED

No GitHub polling/fetch qualification, remote push, P5-D4 real-state mutation, Vault/CURRENT mutation, promotion or publication authority is created.

Next gate:
EXTERNAL_ADVERSARIAL_REVIEW_THEN_HUMAN_ADJUDICATION

~~~

## RPE03 CLASSIFIER

PATH: tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py

~~~python
"""RPE-03 V0.1: fail-closed local Git ancestry classifier.

No network operations are permitted. The classifier rebuilds a sanitized Git
environment, verifies the local object domain, validates commit identities, and
only then maps merge-base ancestry to the governed transition vocabulary.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Final


_SHA40_RE: Final = re.compile(r"[0-9a-f]{40}\Z")
_TIMEOUT_SECONDS: Final = 5
_SAFE_GIT_ENV_KEYS: Final = {
    "GIT_NO_REPLACE_OBJECTS",
    "GIT_CONFIG_NOSYSTEM",
    "GIT_CONFIG_GLOBAL",
    "GIT_TERMINAL_PROMPT",
    "GIT_OPTIONAL_LOCKS",
    "GIT_NO_LAZY_FETCH",
}


def _safe_git_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(
        {
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_NO_LAZY_FETCH": "1",
        }
    )
    return env


def _run_git(repo_path: Path, *args: str) -> subprocess.CompletedProcess[str] | None:
    cmd = ["git", "-c", "core.commitGraph=false", *args]
    try:
        return subprocess.run(
            cmd,
            cwd=str(repo_path),
            env=_safe_git_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
    except (subprocess.TimeoutExpired, OSError, ValueError):
        return None


def _stdout_ok(cp: subprocess.CompletedProcess[str] | None) -> str | None:
    if cp is None or cp.returncode != 0:
        return None
    return cp.stdout.strip()


def _canonical_path(text: str, base: Path) -> Path:
    p = Path(text)
    if not p.is_absolute():
        p = base / p
    return p.resolve(strict=False)


def _same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(str(left)) == os.path.normcase(str(right))


def _verified_domain(repo_path: Path) -> tuple[Path, Path] | None:
    try:
        repo = repo_path.resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    if not repo.is_dir():
        return None

    dot_git = repo / ".git"
    if dot_git.is_file():
        return None

    bare_text = _stdout_ok(_run_git(repo, "rev-parse", "--is-bare-repository"))
    git_dir_text = _stdout_ok(_run_git(repo, "rev-parse", "--absolute-git-dir"))
    common_dir_text = _stdout_ok(
        _run_git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")
    )
    if bare_text not in {"true", "false"} or not git_dir_text or not common_dir_text:
        return None

    git_dir = _canonical_path(git_dir_text, repo)
    common_dir = _canonical_path(common_dir_text, repo)
    if not _same_path(git_dir, common_dir):
        return None

    if bare_text == "true":
        if not _same_path(git_dir, repo):
            return None
    else:
        top_text = _stdout_ok(_run_git(repo, "rev-parse", "--show-toplevel"))
        if not top_text:
            return None
        top = _canonical_path(top_text, repo)
        if not _same_path(top, repo):
            return None
        if not dot_git.is_dir():
            return None
        if not _same_path(git_dir, dot_git.resolve(strict=False)):
            return None

    shallow = _stdout_ok(_run_git(repo, "rev-parse", "--is-shallow-repository"))
    if shallow is None or shallow.lower() != "false":
        return None

    if (common_dir / "shallow").exists():
        return None
    if (common_dir / "info" / "grafts").exists():
        return None
    if (common_dir / "objects" / "info" / "alternates").exists():
        return None

    return repo, common_dir


def _valid_commit(repo: Path, sha: object) -> bool:
    if type(sha) is not str or _SHA40_RE.fullmatch(sha) is None:
        return False
    cp = _run_git(repo, "cat-file", "-t", sha)
    return cp is not None and cp.returncode == 0 and cp.stdout.strip() == "commit"


def classify_transition(
    repo_path,
    previous_observed_head,
    new_exact_observed_head,
):
    """Return INITIAL, SAME, FAST_FORWARD, NON_FAST_FORWARD, or UNKNOWN."""
    if type(new_exact_observed_head) is not str or _SHA40_RE.fullmatch(
        new_exact_observed_head
    ) is None:
        return "UNKNOWN"
    if previous_observed_head is not None and (
        type(previous_observed_head) is not str
        or _SHA40_RE.fullmatch(previous_observed_head) is None
    ):
        return "UNKNOWN"

    try:
        repo_candidate = Path(repo_path)
    except (TypeError, ValueError):
        return "UNKNOWN"

    domain = _verified_domain(repo_candidate)
    if domain is None:
        return "UNKNOWN"
    repo, _common_dir = domain

    if not _valid_commit(repo, new_exact_observed_head):
        return "UNKNOWN"

    if previous_observed_head is None:
        return "INITIAL"

    if not _valid_commit(repo, previous_observed_head):
        return "UNKNOWN"

    if previous_observed_head == new_exact_observed_head:
        return "SAME"

    cp = _run_git(
        repo,
        "merge-base",
        "--is-ancestor",
        previous_observed_head,
        new_exact_observed_head,
    )
    if cp is None:
        return "UNKNOWN"
    if cp.returncode == 0:
        return "FAST_FORWARD"
    if cp.returncode == 1:
        return "NON_FAST_FORWARD"
    return "UNKNOWN"

~~~

## RPE02 REAL-TIME MODEL

PATH: tools/obsidian_projection/rpe02_real_time_model_v0_1.py

~~~python
"""RPE-02 V0.1: nanosecond-native real-time representation.

Pure timing qualification except capture_monotonic_clock_capability(), which records
host clock capability/evidence. No network, CLI, environment, filesystem config, or
P5-D4/Vault mutation authority exists in this module.
"""

from __future__ import annotations

import platform
import re
import sys
import time
from typing import Any, Mapping, Sequence


NANOSECONDS_PER_SECOND = 1_000_000_000
POLL_INTERVAL_NS = 30 * NANOSECONDS_PER_SECOND
DETECTION_LATENCY_BOUND_NS = 60 * NANOSECONDS_PER_SECOND
_SHA40_RE = re.compile(r"[0-9a-f]{40}\Z")
_ALLOWED_OUTCOMES = {"READ_FAILURE", "REMOTE_HEAD_OBSERVED"}


class RPE02TimingError(ValueError):
    """Invalid RPE-02 timing evidence or plan."""


def _strict_int(name: str, value: object) -> int:
    if type(value) is not int:
        raise RPE02TimingError(f"{name} must be an integer nanosecond value")
    return value


def _strict_sha40(name: str, value: object) -> str:
    if type(value) is not str or _SHA40_RE.fullmatch(value) is None:
        raise RPE02TimingError(f"{name} must be lowercase 40-hex")
    return value


def make_real_time_plan(*, schedule_origin_ns: int) -> dict[str, Any]:
    origin = _strict_int("schedule_origin_ns", schedule_origin_ns)
    return {
        "schema": "ATDS_RPE02_REAL_TIME_PLAN_V0_1",
        "normative_unit": "INTEGER_MONOTONIC_NANOSECONDS",
        "schedule_origin_ns": origin,
        "poll_interval_ns": POLL_INTERVAL_NS,
        "detection_latency_bound_ns": DETECTION_LATENCY_BOUND_NS,
        "synthetic_reference_role": "IMMUTABLE_SEMANTIC_AND_EXACT_GRID_PARITY_REFERENCE",
    }


def first_fixed_rate_slot_at_or_after_ns(
    timestamp_ns: int,
    poll_interval_ns: int,
    schedule_origin_ns: int,
) -> int:
    timestamp = _strict_int("timestamp_ns", timestamp_ns)
    interval = _strict_int("poll_interval_ns", poll_interval_ns)
    origin = _strict_int("schedule_origin_ns", schedule_origin_ns)
    if interval <= 0:
        raise RPE02TimingError("poll_interval_ns must be positive")
    if timestamp <= origin:
        return origin + interval
    delta = timestamp - origin
    q, r = divmod(delta, interval)
    return origin + (q if r == 0 else q + 1) * interval


def _blocked(code: str, **extra: Any) -> dict[str, Any]:
    out: dict[str, Any] = {
        "status": "BLOCKED_REQUIRES_ADJUDICATION",
        "failure_code": code,
        "detection_latency_ns": None,
    }
    out.update(extra)
    return out


def _validate_plan(plan: Mapping[str, Any]) -> tuple[int, int, int]:
    if not isinstance(plan, Mapping):
        raise RPE02TimingError("plan must be a mapping")
    if plan.get("normative_unit") != "INTEGER_MONOTONIC_NANOSECONDS":
        raise RPE02TimingError("plan normative unit mismatch")
    origin = _strict_int("plan.schedule_origin_ns", plan.get("schedule_origin_ns"))
    interval = _strict_int("plan.poll_interval_ns", plan.get("poll_interval_ns"))
    bound = _strict_int(
        "plan.detection_latency_bound_ns",
        plan.get("detection_latency_bound_ns"),
    )
    if interval != POLL_INTERVAL_NS:
        raise RPE02TimingError("poll interval is not the preregistered 30 seconds")
    if bound != DETECTION_LATENCY_BOUND_NS:
        raise RPE02TimingError("latency bound is not the preregistered 60 seconds")
    return origin, interval, bound


def _normalize_observation(raw: Mapping[str, Any], index: int) -> dict[str, Any]:
    if not isinstance(raw, Mapping):
        raise RPE02TimingError(f"observations[{index}] must be a mapping")
    required = {
        "scheduled_at_ns",
        "attempt_started_at_ns",
        "remote_observation_completed_at_ns",
        "attempt_completed_at_ns",
        "outcome",
        "observed_head",
    }
    if set(raw) != required:
        raise RPE02TimingError(
            f"observations[{index}] keys mismatch: "
            f"missing={sorted(required - set(raw))}, "
            f"unknown={sorted(set(raw) - required)}"
        )
    out = dict(raw)
    for key in (
        "scheduled_at_ns",
        "attempt_started_at_ns",
        "remote_observation_completed_at_ns",
        "attempt_completed_at_ns",
    ):
        out[key] = _strict_int(f"observations[{index}].{key}", out[key])
    if type(out["outcome"]) is not str or out["outcome"] not in _ALLOWED_OUTCOMES:
        raise RPE02TimingError(
            f"observations[{index}].outcome must be one of "
            f"{sorted(_ALLOWED_OUTCOMES)}"
        )
    if out["outcome"] == "READ_FAILURE":
        if out["observed_head"] is not None:
            raise RPE02TimingError(
                f"observations[{index}] READ_FAILURE may not carry observed_head"
            )
    else:
        out["observed_head"] = _strict_sha40(
            f"observations[{index}].observed_head",
            out["observed_head"],
        )
    return out


def qualify_detection_ns(
    *,
    plan: Mapping[str, Any],
    controlled_source_release_started_at_ns: int,
    target_head: str,
    observations: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    origin, interval, bound = _validate_plan(plan)
    release = _strict_int(
        "controlled_source_release_started_at_ns",
        controlled_source_release_started_at_ns,
    )
    target = _strict_sha40("target_head", target_head)
    if release <= origin:
        raise RPE02TimingError(
            "controlled_source_release_started_at_ns must be greater than schedule_origin_ns"
        )
    if not isinstance(observations, Sequence) or isinstance(
        observations, (str, bytes, bytearray)
    ):
        raise RPE02TimingError("observations must be a sequence")

    normalized = [_normalize_observation(raw, i) for i, raw in enumerate(observations)]
    for index in range(1, len(normalized)):
        if normalized[index]["scheduled_at_ns"] < normalized[index - 1]["scheduled_at_ns"]:
            return _blocked("OBSERVATION_ORDER_NOT_STRICTLY_INCREASING")

    previous_scheduled: int | None = None
    previous_completion: int | None = None
    seen_slots: set[int] = set()

    for item in normalized:
        scheduled = item["scheduled_at_ns"]
        started = item["attempt_started_at_ns"]
        remote_done = item["remote_observation_completed_at_ns"]
        attempt_done = item["attempt_completed_at_ns"]

        if scheduled <= origin or (scheduled - origin) % interval != 0:
            return _blocked("ATTEMPT_OFF_FIXED_RATE_GRID")
        if scheduled in seen_slots:
            return _blocked("DUPLICATE_FIXED_RATE_SLOT")
        seen_slots.add(scheduled)

        if previous_scheduled is not None and scheduled != previous_scheduled + interval:
            return _blocked("CADENCE_GAP")
        if started < scheduled:
            return _blocked("ACTUAL_START_PRECEDES_SCHEDULED_SLOT")
        if started >= scheduled + interval:
            return _blocked("ACTUAL_START_MISSED_FIXED_RATE_SLOT")
        if remote_done < started:
            return _blocked("REMOTE_COMPLETION_PRECEDES_ATTEMPT_START")
        if remote_done > scheduled + interval:
            return _blocked("ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT")
        if attempt_done < remote_done:
            return _blocked("ATTEMPT_COMPLETION_PRECEDES_REMOTE_COMPLETION")
        if previous_completion is not None and previous_completion > started:
            return _blocked("ATTEMPT_OVERLAP")

        if (
            item["outcome"] == "REMOTE_HEAD_OBSERVED"
            and item["observed_head"] == target
            and started < release
        ):
            return _blocked(
                "TARGET_HEAD_OBSERVED_BY_PRE_RELEASE_ATTEMPT",
                first_detection_scheduled_at_ns=scheduled,
                first_detection_attempt_started_at_ns=started,
                first_detection_remote_observation_completed_at_ns=remote_done,
                first_detection_attempt_completed_at_ns=attempt_done,
            )

        previous_scheduled = scheduled
        previous_completion = attempt_done

    first_required = first_fixed_rate_slot_at_or_after_ns(release, interval, origin)
    if normalized:
        slots_at_or_after_release = [
            item["scheduled_at_ns"]
            for item in normalized
            if item["scheduled_at_ns"] >= first_required
        ]
        if slots_at_or_after_release and slots_at_or_after_release[0] != first_required:
            return _blocked("SKIPPED_REQUIRED_ATTEMPT")

    for item in normalized:
        if item["attempt_started_at_ns"] < release:
            continue
        if (
            item["outcome"] == "REMOTE_HEAD_OBSERVED"
            and item["observed_head"] == target
        ):
            latency = item["remote_observation_completed_at_ns"] - release
            status = (
                "PASS_DETECTED_WITHIN_BOUND"
                if latency <= bound
                else "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED"
            )
            return {
                "status": status,
                "failure_code": None,
                "detection_latency_ns": latency,
                "first_detection_scheduled_at_ns": item["scheduled_at_ns"],
                "first_detection_attempt_started_at_ns": item["attempt_started_at_ns"],
                "first_detection_remote_observation_completed_at_ns": item[
                    "remote_observation_completed_at_ns"
                ],
                "first_detection_attempt_completed_at_ns": item["attempt_completed_at_ns"],
            }

    next_required_slot = (
        normalized[-1]["scheduled_at_ns"] + interval
        if normalized
        else first_required
    )
    if next_required_slot - release > bound:
        return {
            "status": "FAIL_NO_DETECTION_BY_BOUND",
            "failure_code": "NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND",
            "detection_latency_ns": None,
        }
    return {
        "status": "INCOMPLETE_REAL_TIME_WINDOW",
        "failure_code": None,
        "detection_latency_ns": None,
    }


def capture_monotonic_clock_capability() -> dict[str, Any]:
    info = time.get_clock_info("monotonic")
    sample_1 = time.monotonic_ns()
    sample_2 = time.monotonic_ns()
    if not info.monotonic:
        raise RPE02TimingError("host monotonic clock does not report monotonic capability")
    return {
        "schema": "ATDS_RPE02_MONOTONIC_CLOCK_CAPABILITY_V0_1",
        "api": "time.monotonic_ns",
        "metadata_api": "time.get_clock_info('monotonic')",
        "normative_unit": "INTEGER_MONOTONIC_NANOSECONDS",
        "monotonic": bool(info.monotonic),
        "adjustable": bool(info.adjustable),
        "resolution_seconds": info.resolution,
        "implementation": info.implementation,
        "sample_1_ns": sample_1,
        "sample_2_ns": sample_2,
        "same_process_host_domain": True,
        "python_version": sys.version.replace("\n", " "),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
    }

~~~

## RPE01 GOVERNED SCHEMA GUARD

PATH: tools/obsidian_projection/rpe01_governed_closed_schema.py

~~~python
from __future__ import annotations

import json
import re
from typing import Any


SCHEMA_ID = "ATDS_GOVERNED_JSON_SCHEMA_V0_1"
MAX_GOVERNED_JSON_DEPTH = 64
_ALLOWED_KINDS = {"object", "array", "string", "integer", "boolean", "null"}
_SHA1_RE = re.compile(r"[0-9a-f]{40}\Z")


class GovernedSchemaError(ValueError):
    pass


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise GovernedSchemaError(f"duplicate JSON member: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise GovernedSchemaError(f"non-standard JSON numeric constant forbidden: {value}")


def _enforce_max_json_depth(text: str) -> None:
    depth = 0
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
            continue

        if char in "[{":
            depth += 1
            if depth > MAX_GOVERNED_JSON_DEPTH:
                raise GovernedSchemaError(
                    "maximum governed JSON depth exceeded: "
                    f"{depth} > {MAX_GOVERNED_JSON_DEPTH}"
                )
        elif char in "]}":
            depth -= 1


def parse_json_strict(raw: str | bytes) -> Any:
    if isinstance(raw, bytes):
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise GovernedSchemaError(f"governed JSON must be valid UTF-8: {exc}") from exc
    elif isinstance(raw, str):
        text = raw
    else:
        raise GovernedSchemaError("raw governed JSON must be str or bytes")
    _enforce_max_json_depth(text)
    try:
        return json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except GovernedSchemaError:
        raise
    except (json.JSONDecodeError, ValueError, RecursionError) as exc:
        raise GovernedSchemaError(
            f"invalid or unsupported governed JSON: {type(exc).__name__}: {exc}"
        ) from exc


def _exact_keys(label: str, value: object, allowed: set[str], required: set[str]) -> dict[str, Any]:
    if type(value) is not dict:
        raise GovernedSchemaError(f"{label} must be an object")
    actual = set(value)
    unknown = actual - allowed
    missing = required - actual
    if unknown or missing:
        raise GovernedSchemaError(
            f"{label} schema mismatch: missing={sorted(missing)} unknown={sorted(unknown)}"
        )
    return value


def _strict_int(label: str, value: object, *, minimum: int | None = None) -> int:
    if type(value) is not int:
        raise GovernedSchemaError(f"{label} must be an integer")
    if minimum is not None and value < minimum:
        raise GovernedSchemaError(f"{label} must be >= {minimum}")
    return value


def _strict_bool(label: str, value: object) -> bool:
    if type(value) is not bool:
        raise GovernedSchemaError(f"{label} must be a boolean")
    return value


def _strict_string(label: str, value: object, *, nonempty: bool = True) -> str:
    if type(value) is not str:
        raise GovernedSchemaError(f"{label} must be a string")
    if nonempty and not value:
        raise GovernedSchemaError(f"{label} must be non-empty")
    return value


def _unique_json_values(values: list[Any]) -> bool:
    encoded = [
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        for value in values
    ]
    return len(encoded) == len(set(encoded))


def _value_matches_kind(value: object, kind: str) -> bool:
    if kind == "object":
        return type(value) is dict
    if kind == "array":
        return type(value) is list
    if kind == "string":
        return type(value) is str
    if kind == "integer":
        return type(value) is int
    if kind == "boolean":
        return type(value) is bool
    if kind == "null":
        return value is None
    return False


def _validate_constraint_value(label: str, value: object, kind: str) -> None:
    if not _value_matches_kind(value, kind):
        raise GovernedSchemaError(f"{label} does not match node kind {kind}")


def _validate_schema_node(node: object, path: str) -> None:
    if type(node) is not dict:
        raise GovernedSchemaError(f"{path} schema node must be an object")
    kind = node.get("kind")
    if type(kind) is not str or kind not in _ALLOWED_KINDS:
        raise GovernedSchemaError(f"{path}.kind unsupported")

    if kind == "object":
        allowed = {"kind", "fields"}
        _exact_keys(path, node, allowed, allowed)
        fields = node["fields"]
        if type(fields) is not dict or not fields:
            raise GovernedSchemaError(f"{path}.fields must be a non-empty object")
        for name, child in fields.items():
            _strict_string(f"{path}.fields key", name)
            _validate_schema_node(child, f"{path}.fields.{name}")
        return

    if kind == "array":
        allowed = {
            "kind", "items", "min_items", "max_items", "unique",
            "ordered_const", "allowed_values",
        }
        _exact_keys(path, node, allowed, {"kind", "items"})
        _validate_schema_node(node["items"], f"{path}.items")
        item_kind = node["items"]["kind"]

        minimum = None
        maximum = None
        if "min_items" in node:
            minimum = _strict_int(f"{path}.min_items", node["min_items"], minimum=0)
        if "max_items" in node:
            maximum = _strict_int(f"{path}.max_items", node["max_items"], minimum=0)
        if minimum is not None and maximum is not None and minimum > maximum:
            raise GovernedSchemaError(f"{path} min_items exceeds max_items")
        if "unique" in node:
            _strict_bool(f"{path}.unique", node["unique"])
        for constraint in ("ordered_const", "allowed_values"):
            if constraint not in node:
                continue
            values = node[constraint]
            if type(values) is not list:
                raise GovernedSchemaError(f"{path}.{constraint} must be an array")
            for index, value in enumerate(values):
                _validate_constraint_value(
                    f"{path}.{constraint}[{index}]",
                    value,
                    item_kind,
                )
            if not _unique_json_values(values):
                raise GovernedSchemaError(f"{path}.{constraint} must not contain duplicates")
        if "ordered_const" in node:
            ordered = node["ordered_const"]
            if minimum is not None and len(ordered) < minimum:
                raise GovernedSchemaError(f"{path}.ordered_const shorter than min_items")
            if maximum is not None and len(ordered) > maximum:
                raise GovernedSchemaError(f"{path}.ordered_const longer than max_items")
        return

    if kind == "string":
        allowed = {"kind", "const", "enum", "pattern"}
        _exact_keys(path, node, allowed, {"kind"})
        if "const" in node:
            _validate_constraint_value(f"{path}.const", node["const"], kind)
        if "enum" in node:
            enum = node["enum"]
            if type(enum) is not list or not enum:
                raise GovernedSchemaError(f"{path}.enum must be a non-empty array")
            for index, value in enumerate(enum):
                _validate_constraint_value(f"{path}.enum[{index}]", value, kind)
            if not _unique_json_values(enum):
                raise GovernedSchemaError(f"{path}.enum must be unique")
        if "pattern" in node:
            pattern = _strict_string(f"{path}.pattern", node["pattern"])
            try:
                re.compile(pattern)
            except re.error as exc:
                raise GovernedSchemaError(f"{path}.pattern invalid: {exc}") from exc
        return

    if kind == "integer":
        allowed = {"kind", "const", "enum", "minimum", "maximum"}
        _exact_keys(path, node, allowed, {"kind"})
        if "const" in node:
            _validate_constraint_value(f"{path}.const", node["const"], kind)
        if "enum" in node:
            enum = node["enum"]
            if type(enum) is not list or not enum:
                raise GovernedSchemaError(f"{path}.enum must be a non-empty array")
            for index, value in enumerate(enum):
                _validate_constraint_value(f"{path}.enum[{index}]", value, kind)
            if not _unique_json_values(enum):
                raise GovernedSchemaError(f"{path}.enum must be unique")
        minimum = None
        maximum = None
        if "minimum" in node:
            minimum = _strict_int(f"{path}.minimum", node["minimum"])
        if "maximum" in node:
            maximum = _strict_int(f"{path}.maximum", node["maximum"])
        if minimum is not None and maximum is not None and minimum > maximum:
            raise GovernedSchemaError(f"{path} minimum exceeds maximum")
        return

    if kind == "boolean":
        allowed = {"kind", "const"}
        _exact_keys(path, node, allowed, {"kind"})
        if "const" in node:
            _validate_constraint_value(f"{path}.const", node["const"], kind)
        return

    if kind == "null":
        _exact_keys(path, node, {"kind"}, {"kind"})
        return

    raise GovernedSchemaError(f"{path}.kind unsupported")


def _validate_schema_definition(schema: object) -> dict[str, Any]:
    top = _exact_keys(
        "schema",
        schema,
        {"schema", "artifact_role", "source_binding", "root"},
        {"schema", "artifact_role", "root"},
    )
    if top["schema"] != SCHEMA_ID:
        raise GovernedSchemaError("unsupported governed schema version")
    _strict_string("schema.artifact_role", top["artifact_role"])
    if "source_binding" in top:
        binding = _exact_keys(
            "schema.source_binding",
            top["source_binding"],
            {"path", "git_blob"},
            {"path", "git_blob"},
        )
        _strict_string("schema.source_binding.path", binding["path"])
        blob = _strict_string("schema.source_binding.git_blob", binding["git_blob"])
        if _SHA1_RE.fullmatch(blob) is None:
            raise GovernedSchemaError("schema.source_binding.git_blob must be lowercase 40-hex")
    _validate_schema_node(top["root"], "schema.root")
    return top


def validate_schema_definition(schema: object) -> dict[str, Any]:
    try:
        return _validate_schema_definition(schema)
    except GovernedSchemaError:
        raise
    except RecursionError as exc:
        raise GovernedSchemaError(
            "governed schema validation exceeded recursion safety boundary"
        ) from exc


def _validate_document_node(value: object, node: dict[str, Any], path: str) -> None:
    kind = node["kind"]
    if not _value_matches_kind(value, kind):
        raise GovernedSchemaError(f"{path} must be {kind}")

    if kind == "object":
        fields = node["fields"]
        actual = set(value)
        expected = set(fields)
        if actual != expected:
            raise GovernedSchemaError(
                f"{path} closed-schema mismatch: "
                f"missing={sorted(expected - actual)} unknown={sorted(actual - expected)}"
            )
        for key, child in fields.items():
            _validate_document_node(value[key], child, f"{path}.{key}")
        return

    if kind == "array":
        length = len(value)
        if "min_items" in node and length < node["min_items"]:
            raise GovernedSchemaError(f"{path} shorter than min_items")
        if "max_items" in node and length > node["max_items"]:
            raise GovernedSchemaError(f"{path} longer than max_items")
        if node.get("unique") is True and not _unique_json_values(value):
            raise GovernedSchemaError(f"{path} contains duplicate items")
        if "allowed_values" in node:
            allowed = node["allowed_values"]
            for item in value:
                if item not in allowed:
                    raise GovernedSchemaError(f"{path} contains item outside closed vocabulary")
        if "ordered_const" in node and value != node["ordered_const"]:
            raise GovernedSchemaError(f"{path} violates normative array order/content")
        for index, item in enumerate(value):
            _validate_document_node(item, node["items"], f"{path}[{index}]")
        return

    if "const" in node and value != node["const"]:
        raise GovernedSchemaError(f"{path} const mismatch")
    if "enum" in node and value not in node["enum"]:
        raise GovernedSchemaError(f"{path} outside closed enum")
    if kind == "string" and "pattern" in node:
        if re.fullmatch(node["pattern"], value) is None:
            raise GovernedSchemaError(f"{path} pattern mismatch")
    if kind == "integer":
        if "minimum" in node and value < node["minimum"]:
            raise GovernedSchemaError(f"{path} below minimum")
        if "maximum" in node and value > node["maximum"]:
            raise GovernedSchemaError(f"{path} above maximum")


def parse_schema_json_strict(raw: str | bytes) -> dict[str, Any]:
    schema = parse_json_strict(raw)
    return validate_schema_definition(schema)


def _validate_document(document: object, validated_schema: dict[str, Any]) -> Any:
    _validate_document_node(document, validated_schema["root"], "$")
    return document


def validate_governed_json(
    raw_document: str | bytes,
    raw_schema: str | bytes,
) -> Any:
    try:
        validated_schema = parse_schema_json_strict(raw_schema)
        document = parse_json_strict(raw_document)
        return _validate_document(document, validated_schema)
    except GovernedSchemaError:
        raise
    except RecursionError as exc:
        raise GovernedSchemaError(
            "governed document validation exceeded recursion safety boundary"
        ) from exc

~~~
