import subprocess
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
MODEL = ROOT / "tools" / "obsidian_projection" / "p5e_near_real_time_model.py"
MATRIX = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_requirement_evidence_matrix.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha1(path, relative_path):
    return subprocess.check_output(
        [
            "git",
            "hash-object",
            f"--path={relative_path}",
            str(path),
        ],
        cwd=ROOT,
        text=True,
    ).strip()


class TestP5ERequirementEvidenceMatrixV01(unittest.TestCase):
    def test_matrix_exists_and_schema_is_exact(self):
        self.assertTrue(MATRIX.is_file())
        m = load_json(MATRIX)
        self.assertEqual(
            m["schema"],
            "ATDS_OBSIDIAN_P5E_REQUIREMENT_EVIDENCE_MATRIX_V0_1",
        )
        self.assertEqual(
            m["qualification_scope"],
            "P5E_V0_1_EXTERNAL_REVIEW_TARGETED_CLOSURE",
        )
        self.assertFalse(m["real_p5e_execution_authorized"])

    def test_matrix_binds_exact_covered_contract_and_model(self):
        m = load_json(MATRIX)
        self.assertTrue(m["covered_object_drift_must_fail"])
        self.assertEqual(
            m["covered_contract_blob"],
            git_blob_sha1(
                CONTRACT,
                "tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json",
            ),
        )
        self.assertEqual(
            m["covered_model_blob"],
            git_blob_sha1(
                MODEL,
                "tools/obsidian_projection/p5e_near_real_time_model.py",
            ),
        )

    def test_every_required_case_and_breaker_is_mapped_exactly_once(self):
        c = load_json(CONTRACT)
        m = load_json(MATRIX)
        self.assertEqual(
            set(m["required_synthetic_cases"]),
            set(c["required_synthetic_cases"]),
        )
        self.assertEqual(
            set(m["base_breakers"]),
            set(c["required_breakers"]),
        )
        self.assertEqual(
            set(m["targeted_closure_breakers"]),
            set(c["external_review_targeted_closure"]["required_breakers"]),
        )
        self.assertEqual(
            len(m["required_synthetic_cases"]),
            len(c["required_synthetic_cases"]),
        )
        self.assertEqual(
            len(m["base_breakers"]),
            len(c["required_breakers"]),
        )
        self.assertEqual(
            len(m["targeted_closure_breakers"]),
            len(c["external_review_targeted_closure"]["required_breakers"]),
        )

    def test_all_mappings_bind_to_current_file_blobs_and_real_test_methods(self):
        m = load_json(MATRIX)
        sections = (
            "required_synthetic_cases",
            "base_breakers",
            "targeted_closure_breakers",
        )
        for section in sections:
            for requirement, entry in m[section].items():
                with self.subTest(section=section, requirement=requirement):
                    self.assertEqual(entry["verdict"], "PASS")
                    self.assertIn(
                        entry["evidence_kind"],
                        {"DIRECT_P5E", "REUSED_QUALIFIED_P5D2_P5D4"},
                    )
                    path = ROOT / entry["path"]
                    self.assertTrue(path.is_file(), entry["path"])
                    self.assertEqual(
                        entry["blob"],
                        git_blob_sha1(path, entry["path"]),
                    )
                    method = entry["test_method"].split(".")[-1]
                    text = path.read_text(encoding="utf-8")
                    self.assertIn(f"def {method}", text)

    def test_matrix_has_no_unmapped_or_deferred_requirements(self):
        m = load_json(MATRIX)
        summary = m["coverage_summary"]
        self.assertEqual(summary["unmapped"], 0)
        self.assertEqual(summary["deferred"], 0)
        self.assertEqual(summary["required_synthetic_cases_total"], 10)
        self.assertEqual(summary["base_breakers_total"], 25)
        self.assertEqual(summary["targeted_closure_breakers_total"], 8)
        self.assertEqual(summary["mapped_total"], 43)

    def test_matrix_does_not_claim_real_execution(self):
        m = load_json(MATRIX)
        self.assertFalse(m["real_p5e_execution_authorized"])
        self.assertFalse(m["real_60_second_sla_qualified"])
        self.assertFalse(m["per_transient_tip_detection_sla_qualified"])
        self.assertFalse(m["automatic_evaluation_authorized"])
        self.assertFalse(m["automatic_promotion_authorized"])
        self.assertFalse(m["automatic_publication_authorized"])


if __name__ == "__main__":
    unittest.main()
