from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.obsidian_projection.classification import (
    ClassificationError,
    classify_record,
    git_blob_oid,
    records_digest_sha256,
)
from tools.obsidian_projection.inventory import (
    FrozenInventory,
    InventoryEntry,
)

COMMIT = "1" * 40
TREE = "2" * 40
REPOSITORY = (
    "thboulevart-creator/"
    "ADAPTIVE-TRADING-DECISION-SYSTEM"
)


def make_inventory(entry: InventoryEntry) -> FrozenInventory:
    return FrozenInventory(
        schema="ATDS_OBSIDIAN_PILOT_INVENTORY_V0_1",
        source_repository=REPOSITORY,
        source_branch="integration/system-v1",
        source_commit=COMMIT,
        source_tree=TREE,
        source_artifact_count=1,
        entries=(entry,),
    )


def base_rules() -> dict:
    return {
        "source_commit": COMMIT,
        "source_tree": TREE,
        "pilot_source_count": 1,
        "defaults": {
            "semantic_role": "UNKNOWN",
            "procedure_role": "NONE",
            "qualification_status": "UNKNOWN",
            "scientific_status": "UNKNOWN",
            "epistemic_role": "UNKNOWN",
            "temporal_role": "UNKNOWN",
        },
        "exact_fixtures": [],
    }


def entry_for(
    path: str,
    raw: bytes,
    inventory_class: str,
) -> InventoryEntry:
    return InventoryEntry(
        source_path=path,
        source_blob_sha=git_blob_oid(raw),
        source_blob_size=len(raw),
        inventory_class=inventory_class,
    )


class ClassificationTests(unittest.TestCase):
    def test_filename_tokens_cannot_self_qualify(self) -> None:
        raw = (
            b"# PASS ADJUDICATION BLOCKED BACKUP\n"
            b"\nNo terminal decision is made here.\n"
        )
        entry = entry_for(
            "PASS-ADJUDICATION-BLOCKED-BACKUP.md",
            raw,
            "AP_PROGRAM",
        )
        record = classify_record(
            make_inventory(entry),
            entry,
            raw,
            base_rules(),
        )
        self.assertEqual(
            record.qualification_status,
            "UNKNOWN",
        )
        self.assertEqual(record.procedure_role, "NONE")
        self.assertEqual(
            record.temporal_role,
            "UNKNOWN",
        )

    def test_machine_status_json_is_not_governed_pass(self) -> None:
        raw = json.dumps(
            {
                "schema": "X",
                "status": "AP6_COMPLETE_VERIFIED",
            }
        ).encode()
        entry = entry_for(
            "evidence.json",
            raw,
            "EVIDENCE",
        )
        record = classify_record(
            make_inventory(entry),
            entry,
            raw,
            base_rules(),
        )
        self.assertEqual(
            record.qualification_status,
            "UNKNOWN",
        )
        self.assertEqual(
            record.semantic_role,
            "RESULT",
        )

    def test_mutants_killed_are_test_result_not_pass(self) -> None:
        raw = json.dumps(
            {
                "m1": "KILLED",
                "m2": "KILLED",
            }
        ).encode()
        entry = entry_for(
            "mutation.json",
            raw,
            "EVIDENCE",
        )
        record = classify_record(
            make_inventory(entry),
            entry,
            raw,
            base_rules(),
        )
        self.assertEqual(
            record.procedure_role,
            "TEST_RESULT",
        )
        self.assertEqual(
            record.qualification_status,
            "UNKNOWN",
        )

    def test_handoff_reported_pass_does_not_self_qualify(self) -> None:
        raw = (
            b"# Session handoff\n\n"
            b"AP4 verdict: PASS.\n\n"
            b"## Next action\nDo AP5.\n"
        )
        entry = entry_for(
            "session.md",
            raw,
            "HISTORICAL_LINEAGE",
        )
        record = classify_record(
            make_inventory(entry),
            entry,
            raw,
            base_rules(),
        )
        self.assertEqual(
            record.procedure_role,
            "HANDOFF",
        )
        self.assertEqual(
            record.qualification_status,
            "UNKNOWN",
        )
        self.assertEqual(
            record.temporal_role,
            "HISTORICAL",
        )

    def test_pass_never_maps_to_supported(self) -> None:
        raw = (
            b"# Candidate adjudication\n\n"
            b"## Inputs\nexact\n\n"
            b"## Verdict\n**PASS -- bounded.**\n"
        )
        entry = entry_for(
            "decision.md",
            raw,
            "AP_PROGRAM",
        )
        rules = base_rules()
        rules["exact_fixtures"] = [
            {
                "source_path": entry.source_path,
                "source_blob_sha": entry.source_blob_sha,
                "expected": {
                    "semantic_role": "DECISION",
                    "procedure_role": "ADJUDICATION",
                    "qualification_status": "PASS",
                    "qualification_scope": "BOUNDED",
                    "scientific_status": "NOT_APPLICABLE",
                },
            }
        ]
        record = classify_record(
            make_inventory(entry),
            entry,
            raw,
            rules,
        )
        self.assertEqual(
            record.qualification_status,
            "PASS",
        )
        self.assertNotEqual(
            record.scientific_status,
            "SUPPORTED",
        )

    def test_exact_fixture_requires_path_and_blob(self) -> None:
        raw = b"# Neutral\n"
        entry = entry_for(
            "same-path.md",
            raw,
            "AP_PROGRAM",
        )

        rules = base_rules()
        rules["exact_fixtures"] = [
            {
                "source_path": entry.source_path,
                "source_blob_sha": "9" * 40,
                "expected": {
                    "qualification_status": "PASS",
                    "qualification_scope": "SHOULD_NOT_APPLY",
                },
            }
        ]

        record = classify_record(
            make_inventory(entry),
            entry,
            raw,
            rules,
        )
        self.assertEqual(
            record.qualification_status,
            "UNKNOWN",
        )

    def test_raw_blob_identity_mismatch_blocks(self) -> None:
        raw = b"# A\n"
        entry = InventoryEntry(
            source_path="a.md",
            source_blob_sha="9" * 40,
            source_blob_size=len(raw),
            inventory_class="AP_PROGRAM",
        )
        with self.assertRaises(ClassificationError):
            classify_record(
                make_inventory(entry),
                entry,
                raw,
                base_rules(),
            )

    def test_dedicated_limitations_section_only(self) -> None:
        raw = (
            b"# Result\n\n"
            b"Random prose says not causal.\n\n"
            b"## Limitations\n"
            b"- local execution only\n"
            b"- no independent review\n"
        )
        entry = entry_for(
            "result.md",
            raw,
            "AP_PROGRAM",
        )
        record = classify_record(
            make_inventory(entry),
            entry,
            raw,
            base_rules(),
        )
        self.assertEqual(
            record.limitations,
            (
                "local execution only",
                "no independent review",
            ),
        )
        self.assertEqual(record.non_claims, ())

    def test_non_promotions_are_explicit_non_claims(self) -> None:
        raw = (
            b"# Result\n\n"
            b"## Non-promotions\n"
            b"- edge\n"
            b"- strategy\n"
        )
        entry = entry_for(
            "result.md",
            raw,
            "AP_PROGRAM",
        )
        record = classify_record(
            make_inventory(entry),
            entry,
            raw,
            base_rules(),
        )
        self.assertEqual(
            record.non_claims,
            ("edge", "strategy"),
        )

    def test_scope_it_is_not_list_is_explicit_non_claim(self) -> None:
        raw = (
            b"# Profile\n\n"
            b"## 1. Scope\n"
            b"This describes behavior.\n\n"
            b"It is not:\n"
            b"- a strategy;\n"
            b"- an edge claim;\n\n"
            b"Other text.\n"
        )
        entry = entry_for(
            "profile.md",
            raw,
            "CORE_PROFILE",
        )
        record = classify_record(
            make_inventory(entry),
            entry,
            raw,
            base_rules(),
        )
        self.assertEqual(
            record.non_claims,
            ("a strategy;", "an edge claim;"),
        )

    def test_generic_negation_outside_allowed_sections_is_ignored(self) -> None:
        raw = (
            b"# Note\n\n"
            b"This is not a strategy and not causal.\n"
        )
        entry = entry_for(
            "note.md",
            raw,
            "AP_PROGRAM",
        )
        record = classify_record(
            make_inventory(entry),
            entry,
            raw,
            base_rules(),
        )
        self.assertEqual(record.non_claims, ())

    def test_latest_name_never_becomes_current(self) -> None:
        raw = b"# Latest final v999\n"
        entry = entry_for(
            "LATEST-FINAL-V999.md",
            raw,
            "AP_PROGRAM",
        )
        record = classify_record(
            make_inventory(entry),
            entry,
            raw,
            base_rules(),
        )
        self.assertEqual(
            record.temporal_role,
            "UNKNOWN",
        )

    def test_physical_families_are_bounded(self) -> None:
        cases = (
            ("x.py", "IMPLEMENTATION", "CODE"),
            ("x.py", "TEST", "TEST"),
            ("x.py", "BREAKER", "BREAKER"),
            ("x.json", "EVIDENCE", "EVIDENCE"),
            ("x.md", "AP_PROGRAM", "DOCUMENT"),
        )
        for path, inventory_class, expected in cases:
            with self.subTest(path=path, cls=inventory_class):
                raw = b"# x\n" if path.endswith(".md") else (
                    b"print('x')\n"
                    if path.endswith(".py")
                    else b"{}\n"
                )
                entry = entry_for(
                    path,
                    raw,
                    inventory_class,
                )
                record = classify_record(
                    make_inventory(entry),
                    entry,
                    raw,
                    base_rules(),
                )
                self.assertEqual(
                    record.artifact_family,
                    expected,
                )

    def test_canonical_does_not_imply_pass(self) -> None:
        raw = b"# Neutral\n"
        entry = entry_for(
            "neutral.md",
            raw,
            "AP_PROGRAM",
        )
        record = classify_record(
            make_inventory(entry),
            entry,
            raw,
            base_rules(),
        )
        self.assertEqual(
            record.authority_role,
            "CANONICAL",
        )
        self.assertEqual(
            record.persistence_state,
            "TRACKED_IN_GIT_TREE",
        )
        self.assertEqual(
            record.qualification_status,
            "UNKNOWN",
        )

    def test_records_digest_is_deterministic(self) -> None:
        raw_a = b"# A\n"
        raw_b = b"# B\n"
        entry_a = entry_for(
            "a.md",
            raw_a,
            "AP_PROGRAM",
        )
        entry_b = entry_for(
            "b.md",
            raw_b,
            "AP_PROGRAM",
        )
        record_a = classify_record(
            make_inventory(entry_a),
            entry_a,
            raw_a,
            base_rules(),
        )
        record_b = classify_record(
            make_inventory(entry_b),
            entry_b,
            raw_b,
            base_rules(),
        )
        self.assertEqual(
            records_digest_sha256(
                (record_a, record_b)
            ),
            records_digest_sha256(
                (record_b, record_a)
            ),
        )

    def test_rules_binding_mismatch_blocks(self) -> None:
        raw = b"# Neutral\n"
        entry = entry_for(
            "neutral.md",
            raw,
            "AP_PROGRAM",
        )
        rules = base_rules()
        rules["source_tree"] = "8" * 40

        with self.assertRaises(ClassificationError):
            classify_record(
                make_inventory(entry),
                entry,
                raw,
                rules,
            )


if __name__ == "__main__":
    unittest.main()
