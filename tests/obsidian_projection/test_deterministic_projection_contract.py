from __future__ import annotations

import json
import unittest
from pathlib import Path


class DeterministicProjectionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(__file__).resolve().parents[2]
        path = root / 'tools' / 'obsidian_projection' / 'deterministic_projection_contract_v0_1.json'
        cls.contract = json.loads(path.read_text(encoding='utf-8'))

    def test_bound_to_qualified_p1_and_frozen_source(self) -> None:
        self.assertEqual(self.contract['p1_classifier_head'], '26e541c0aedc85440bb069cdc767b2075b56317c')
        self.assertEqual(self.contract['frozen_source_commit'], '7bd8c1312430dfc3def5523eb65397a5d6a5ae05')
        self.assertEqual(self.contract['frozen_source_tree'], '66eeb08a338732d4cf7f5b7f4f5e5fd9fbb4d54b')
        self.assertEqual(self.contract['pilot_source_count'], 74)

    def test_real_vault_is_forbidden(self) -> None:
        b = self.contract['execution_boundary']
        self.assertTrue(b['staging_only'])
        self.assertFalse(b['real_vault_creation_authorized'])
        self.assertFalse(b['obsidian_config_creation_authorized'])

    def test_projection_authority_is_derived(self) -> None:
        self.assertEqual(self.contract['artifact_record']['field_mapping']['projection_authority_role'], 'DERIVED')
        self.assertEqual(self.contract['relation_record']['fixed_values']['projection_authority_role'], 'DERIVED')

    def test_ids_are_deterministic_and_collisions_block(self) -> None:
        a = self.contract['artifact_record']['projection_record_id']
        r = self.contract['relation_record']['projection_relation_id']
        self.assertIn('SHA256', a['algorithm'])
        self.assertIn('NUL', a['algorithm'])
        self.assertEqual(a['collision_policy'], 'BLOCK_BUILD')
        self.assertIn('SHA256', r['algorithm'])
        self.assertIn('evidence_source_blob_sha', r['algorithm'])
        self.assertEqual(r['collision_policy'], 'BLOCK_BUILD')

    def test_markdown_bytes_are_fully_bounded(self) -> None:
        s = self.contract['markdown_serialization']
        self.assertEqual(s['encoding'], 'UTF-8')
        self.assertFalse(s['bom'])
        self.assertEqual(s['newline'], 'LF')
        self.assertTrue(s['final_newline'])
        self.assertEqual(s['field_order'], 'EXACT_AS_REGISTERED')
        self.assertEqual(s['unknown_extra_fields'], 'BLOCK_BUILD')

    def test_no_volatile_fields_in_deterministic_inputs(self) -> None:
        f = set(self.contract['forbidden_deterministic_inputs'])
        self.assertTrue({'wall_clock_time','generated_at','host_name','user_name','absolute_local_repo_path','absolute_temp_path','randomness','uuid'}.issubset(f))

    def test_wikilinks_and_backlinks_are_not_relations(self) -> None:
        p = self.contract['relation_extraction_policy']
        self.assertFalse(p['wikilink_is_relation'])
        self.assertFalse(p['backlink_is_relation'])
        self.assertFalse(p['filename_similarity_is_relation'])
        self.assertFalse(p['chronological_adjacency_is_relation'])

    def test_inferred_is_forbidden_from_authoritative_relations(self) -> None:
        r = self.contract['relation_record']
        self.assertIn('INFERRED', r['forbidden_authoritative_basis'])
        self.assertNotIn('INFERRED', r['allowed_basis'])

    def test_relation_provenance_is_required(self) -> None:
        r = self.contract['relation_record']
        self.assertTrue(r['provenance_required'])
        self.assertIn('evidence_source_path', r['frontmatter_field_order'])
        self.assertIn('evidence_source_blob_sha', r['frontmatter_field_order'])

    def test_relation_target_is_bounded_to_pilot(self) -> None:
        p = self.contract['relation_record']['target_policy']
        self.assertEqual(p['pilot_v0_1'], 'TARGET_MUST_BE_ONE_OF_74_PROJECTED_ARTIFACT_RECORDS')
        self.assertEqual(p['unresolved_target'], 'DO_NOT_EMIT_RELATION')

    def test_source_path_is_not_output_path(self) -> None:
        p = self.contract['path_safety']
        self.assertFalse(p['source_path_used_as_output_path'])
        self.assertEqual(p['filename_source'], 'DETERMINISTIC_RECORD_ID_ONLY')

    def test_generated_machine_owned_views_human_owned(self) -> None:
        o = self.contract['ownership']
        self.assertEqual(o['generated']['owner'], 'MACHINE')
        self.assertFalse(o['generated']['overwrite_in_place'])
        self.assertEqual(o['views']['owner'], 'HUMAN')
        self.assertFalse(o['views']['builder_write_allowed'])
        self.assertFalse(o['views']['builder_read_as_semantic_input'])

    def test_staging_requires_fresh_exclusive_create(self) -> None:
        s = self.contract['staging']
        self.assertTrue(s['required_fresh_empty_directory'])
        self.assertEqual(s['preexisting_target_policy'], 'BLOCK')
        self.assertEqual(s['file_creation_mode'], 'CREATE_NEW_EXCLUSIVE')
        self.assertFalse(s['overwrite_in_place'])
        self.assertEqual(s['hard_link_check_unavailable'], 'BLOCK')

    def test_builder_may_not_write_views_or_obsidian(self) -> None:
        f = set(self.contract['path_safety']['forbidden_builder_write_roots'])
        self.assertEqual(f, {'views', '.obsidian'})

    def test_integrity_manifest_excludes_itself(self) -> None:
        m = self.contract['integrity_manifest']
        self.assertTrue(m['exclude_self'])
        self.assertEqual(m['serialization'], 'CANONICAL_JSON_UTF8_LF')

    def test_clean_flag_is_not_integrity_proof(self) -> None:
        s = self.contract['integrity_semantics']
        self.assertTrue(s['record_self_declared_CLEAN_is_not_sufficient'])
        self.assertEqual(s['manual_edit_result'], 'MODIFIED')
        self.assertEqual(s['missing_generated_file_result'], 'MISSING')

    def test_dynamic_freshness_does_not_contaminate_bytes(self) -> None:
        self.assertEqual(self.contract['integrity_semantics']['source_freshness_in_deterministic_artifact'], 'UNKNOWN')

    def test_build_manifest_has_no_timestamp_host_or_paths(self) -> None:
        f = set(self.contract['build_manifest']['forbidden_fields'])
        self.assertEqual(f, {'generated_at','host','user','absolute_repo_path','absolute_staging_path'})

    def test_double_build_requires_byte_identity(self) -> None:
        g = self.contract['determinism_gate']
        self.assertEqual(g['independent_build_count'], 2)
        req = set(g['required_equalities'])
        self.assertTrue({'relative_path_set','each_file_bytes','each_file_sha256','semantic_record_digest_sha256','artifact_set_digest_sha256','relation_set_digest_sha256','integrity_manifest_sha256','projection_tree_digest_sha256'}.issubset(req))
        self.assertEqual(g['mismatch_result'], 'BLOCK')

    def test_source_text_and_wikilinks_not_generated(self) -> None:
        s = self.contract['markdown_serialization']
        self.assertEqual(s['source_text_copying'], 'FORBIDDEN_IN_V0_1')
        self.assertEqual(s['wikilink_generation'], 'FORBIDDEN_IN_V0_1')

    def test_breaker_set_contains_critical_attacks(self) -> None:
        b = set(self.contract['acceptance_breakers'])
        expected = {'CRLF output','UTF-8 BOM output','volatile timestamp injected','wikilink interpreted as semantic relation','INFERRED relation enters generated/relations','relation lacks evidence_source_blob_sha','generated file overwritten in place','builder writes views/','builder writes .obsidian/','hard-link anomaly accepted','reparse/junction/symlink escape accepted','same-input double build has byte mismatch','source text copied into note body','extra frontmatter field silently accepted'}
        self.assertTrue(expected.issubset(b))

    def test_next_gate_is_temp_only_and_vault_remains_forbidden(self) -> None:
        g = self.contract['next_action_gate']
        self.assertEqual(g['allowed_after_persisted_rebreak'], 'P2_IMPLEMENTATION_CANDIDATE_IN_TEMP_STAGING_ONLY')
        self.assertTrue(g['renderer_implementation_allowed'])
        self.assertTrue(g['typed_relation_implementation_allowed'])
        self.assertTrue(g['integrity_manifest_implementation_allowed'])
        self.assertTrue(g['double_build_determinism_test_allowed'])
        self.assertFalse(g['real_vault_creation_allowed'])
        self.assertFalse(g['obsidian_open_allowed'])
        self.assertFalse(g['plugins_allowed'])
        self.assertFalse(g['sync_allowed'])


if __name__ == '__main__':
    unittest.main()
