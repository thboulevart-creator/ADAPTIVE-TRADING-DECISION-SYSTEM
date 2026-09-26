from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.obsidian_projection.native_view_bundle import (
    EXPECTED_TREE_DIGEST,
    P4A_CONTRACT_SCHEMA,
    VIEW_PATHS,
    VIEW_SCHEMA,
    NativeViewBundleError,
    _exclusive_seed_views,
    _parse_frontmatter,
    build_view_bundle,
    bundle_manifest,
)


def _frontmatter(values: dict[str, object]) -> str:
    lines = ["---"]
    for key, value in values.items():
        lines.append(
            f"{key}: "
            + json.dumps(
                value,
                ensure_ascii=False,
                separators=(",", ":"),
            )
        )
    lines.extend(["---", ""])
    return "\n".join(lines)


class P4BNativeViewBundleTests(unittest.TestCase):
    def _fixture(self, root: Path) -> Path:
        vault = root / "vault"
        artifact_dir = (
            vault
            / "generated"
            / "artifacts"
        )
        relation_dir = (
            vault
            / "generated"
            / "relations"
        )
        views = vault / "views"

        artifact_dir.mkdir(parents=True)
        relation_dir.mkdir(parents=True)
        views.mkdir()

        a1 = {
            "record_schema":
                "ATDS_OBSIDIAN_ARTIFACT_V0_1",
            "record_type": "ARTIFACT",
            "projection_record_id": "A-aaaaaaaaaaaaaaaa",
            "source_repository": "owner/repo",
            "source_branch": "branch",
            "source_commit": "1" * 40,
            "source_tree": "2" * 40,
            "source_path": "GOVERNANCE/README.md",
            "source_blob_sha": "3" * 40,
            "source_blob_size": 100,
            "artifact_family": "DOCUMENT",
            "semantic_role": "GOVERNANCE",
            "procedure_role": "REFERENCE",
            "source_authority_role": "CANONICAL",
            "projection_authority_role": "DERIVED",
            "qualification_status": "PASS",
            "qualification_scope": "DOCUMENT_ONLY",
            "scientific_status": "NOT_APPLICABLE",
            "epistemic_role": "KNOWLEDGE",
            "temporal_role": "CURRENT",
            "persistence_state": "TRACKED_IN_GIT_TREE",
            "source_freshness": "UNKNOWN",
            "projection_integrity": "CLEAN",
            "limitations": [],
            "non_claims": [],
        }
        a2 = {
            **a1,
            "projection_record_id": "A-bbbbbbbbbbbbbbbb",
            "source_path": "docs/RESULT.md",
            "artifact_family": "EVIDENCE",
            "semantic_role": "RESULT",
            "procedure_role": "ADJUDICATION",
            "source_authority_role": "DERIVED",
            "qualification_status": "BLOCKED",
            "qualification_scope": None,
            "scientific_status": "SUPPORTED",
            "epistemic_role": "EVIDENCE",
            "temporal_role": "HISTORICAL",
        }

        for item in (a1, a2):
            path = (
                artifact_dir
                / f"{item['projection_record_id']}.md"
            )
            path.write_text(
                _frontmatter(item)
                + f"# {item['projection_record_id']}\n",
                encoding="utf-8",
                newline="\n",
            )

        relation = {
            "record_schema":
                "ATDS_OBSIDIAN_RELATION_V0_1",
            "record_type": "RELATION",
            "projection_relation_id":
                "R-cccccccccccccccc",
            "source_record_id":
                "A-aaaaaaaaaaaaaaaa",
            "relation_type": "REFERENCES",
            "target_record_id":
                "A-bbbbbbbbbbbbbbbb",
            "basis": "EXPLICIT_TEXT",
            "evidence_source_path":
                "GOVERNANCE/README.md",
            "evidence_source_blob_sha": "3" * 40,
            "source_commit": "1" * 40,
            "projection_authority_role": "DERIVED",
            "projection_integrity": "CLEAN",
        }
        (
            relation_dir
            / "R-cccccccccccccccc.md"
        ).write_text(
            _frontmatter(relation)
            + "# R-cccccccccccccccc\n",
            encoding="utf-8",
            newline="\n",
        )

        return vault

    def test_bundle_has_exact_seven_paths(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = self._fixture(Path(td))
            bundle = build_view_bundle(vault)
            self.assertEqual(
                tuple(bundle.keys()),
                VIEW_PATHS,
            )
            self.assertEqual(len(bundle), 7)

    def test_all_views_are_lf_utf8_without_bom(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = self._fixture(Path(td))
            bundle = build_view_bundle(vault)

            for relative, raw in bundle.items():
                with self.subTest(relative=relative):
                    self.assertTrue(
                        raw.endswith(b"\n")
                    )
                    self.assertNotIn(b"\r", raw)
                    self.assertFalse(
                        raw.startswith(b"\xef\xbb\xbf")
                    )
                    raw.decode("utf-8")

    def test_markdown_views_are_snapshot_bound(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = self._fixture(Path(td))
            bundle = build_view_bundle(vault)

            for relative in VIEW_PATHS[:-1]:
                with self.subTest(relative=relative):
                    path = Path(td) / "view.md"
                    path.write_bytes(bundle[relative])
                    fm = _parse_frontmatter(path)
                    self.assertEqual(
                        fm["view_schema"],
                        VIEW_SCHEMA,
                    )
                    self.assertEqual(
                        fm["view_contract_schema"],
                        P4A_CONTRACT_SCHEMA,
                    )
                    self.assertEqual(
                        fm["authority_role"],
                        "VIEW",
                    )
                    self.assertEqual(
                        fm["semantic_authority"],
                        "NONE",
                    )
                    self.assertEqual(
                        fm[
                            "projection_tree_digest_sha256"
                        ],
                        EXPECTED_TREE_DIGEST,
                    )
                    self.assertEqual(
                        fm["projection_freshness"],
                        "BOUND",
                    )

    def test_home_exposes_authority_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = self._fixture(Path(td))
            text = build_view_bundle(vault)[
                "views/HOME.md"
            ].decode("utf-8")
            self.assertIn(
                "vérité canonique",
                text,
            )
            self.assertIn(
                "navigation humaine non autoritative",
                text,
            )

    def test_snapshot_keeps_axes_separate(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = self._fixture(Path(td))
            text = build_view_bundle(vault)[
                "views/dashboards/PROJECT-SNAPSHOT.md"
            ].decode("utf-8")
            self.assertIn(
                "Autorité source",
                text,
            )
            self.assertIn(
                "Rôles épistémiques",
                text,
            )
            self.assertIn(
                "Rôles temporels",
                text,
            )
            self.assertIn(
                "États de persistance",
                text,
            )

    def test_qualification_keeps_scientific_axis_separate(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = self._fixture(Path(td))
            text = build_view_bundle(vault)[
                "views/dashboards/QUALIFICATION-STATUS.md"
            ].decode("utf-8")
            self.assertIn(
                "Distribution — qualification",
                text,
            )
            self.assertIn(
                "Distribution — statut scientifique",
                text,
            )
            self.assertIn("BLOCKED", text)
            self.assertIn("PASS", text)

    def test_governance_links_only_projected_records(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = self._fixture(Path(td))
            text = build_view_bundle(vault)[
                "views/maps/GOVERNANCE.md"
            ].decode("utf-8")
            self.assertIn(
                "GOVERNANCE/README.md",
                text,
            )
            self.assertNotIn(
                "docs/RESULT.md]]",
                text,
            )

    def test_research_map_uses_qualified_relation_types(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = self._fixture(Path(td))
            text = build_view_bundle(vault)[
                "views/maps/RESEARCH-LIFECYCLE.md"
            ].decode("utf-8")
            self.assertIn("REFERENCES", text)
            self.assertIn(
                "generated/relations/",
                text,
            )

    def test_canvas_is_native_json_with_navigation_edges(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = self._fixture(Path(td))
            raw = build_view_bundle(vault)[
                "views/canvas/ATDS-OVERVIEW.canvas"
            ]
            value = json.loads(raw.decode("utf-8"))
            self.assertEqual(len(value["nodes"]), 6)
            self.assertEqual(len(value["edges"]), 5)
            self.assertTrue(
                all(
                    node["type"] == "file"
                    for node in value["nodes"]
                )
            )
            self.assertTrue(
                all(
                    node["file"].startswith("views/")
                    for node in value["nodes"]
                )
            )
            self.assertTrue(
                all(
                    "label" not in edge
                    for edge in value["edges"]
                )
            )

    def test_bundle_manifest_is_recomputable(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = self._fixture(Path(td))
            bundle = build_view_bundle(vault)
            manifest = bundle_manifest(bundle)

            for relative, raw in bundle.items():
                self.assertEqual(
                    manifest[relative]["size_bytes"],
                    len(raw),
                )
                self.assertEqual(
                    manifest[relative]["sha256"],
                    hashlib.sha256(raw).hexdigest(),
                )

    def test_initial_seed_requires_empty_views(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = self._fixture(Path(td))
            bundle = build_view_bundle(vault)
            views = vault / "views"
            (views / "human.md").write_text(
                "do not overwrite",
                encoding="utf-8",
            )
            with self.assertRaises(
                NativeViewBundleError
            ):
                _exclusive_seed_views(
                    views,
                    bundle,
                )

    def test_initial_seed_is_exclusive_and_exact(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = self._fixture(Path(td))
            bundle = build_view_bundle(vault)
            views = vault / "views"

            _exclusive_seed_views(
                views,
                bundle,
            )

            actual = sorted(
                path.relative_to(vault).as_posix()
                for path in views.rglob("*")
                if path.is_file()
            )
            expected = sorted(VIEW_PATHS)
            self.assertEqual(actual, expected)

            for relative in VIEW_PATHS:
                self.assertEqual(
                    (vault / relative).read_bytes(),
                    bundle[relative],
                )

    def test_second_seed_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = self._fixture(Path(td))
            bundle = build_view_bundle(vault)
            views = vault / "views"

            _exclusive_seed_views(
                views,
                bundle,
            )

            with self.assertRaises(
                NativeViewBundleError
            ):
                _exclusive_seed_views(
                    views,
                    bundle,
                )


if __name__ == "__main__":
    unittest.main()
