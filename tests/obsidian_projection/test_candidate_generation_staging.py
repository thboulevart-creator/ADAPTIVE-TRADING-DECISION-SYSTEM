from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.candidate_generation_staging import (
    CandidateGenerationInfrastructureError,
    CandidateGenerationInvalidError,
    STAGING_CONTRACT_BLOB,
    VerifiedProjectionCandidate,
    stage_candidate_generation,
    verify_candidate_generation,
)
from tools.obsidian_projection.integrity import (
    IntegrityError,
    all_generated_files,
    projection_tree_digest,
)


HEAD = "1" * 40
TREE = "2" * 40


def sha(label: str) -> str:
    return hashlib.sha256(
        label.encode("utf-8")
    ).hexdigest()


def write_file(
    path: Path,
    data: bytes,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    path.write_bytes(data)


def build_projection(root: Path) -> None:
    write_file(
        root / "generated" / "artifacts" / "a.md",
        b"# Alpha\n",
    )
    write_file(
        root / "generated" / "artifacts" / "b.json",
        b'{"alpha":1}\n',
    )
    write_file(
        root / "generated" / "relations" / "edges.json",
        b'{"edges":[]}\n',
    )
    write_file(
        root
        / "generated"
        / "manifests"
        / "build-manifest.json",
        b'{"schema":"P5D3C2_SANDBOX_BUILD"}\n',
    )


def candidate_for(root: Path) -> VerifiedProjectionCandidate:
    return VerifiedProjectionCandidate(
        repository=(
            "thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM"
        ),
        branch="integration/system-v1",
        candidate_head=HEAD,
        candidate_tree=TREE,
        dynamic_inventory_digest_sha256=sha(
            "dynamic-inventory"
        ),
        semantic_bridge_digest_sha256=sha(
            "semantic-bridge"
        ),
        semantic_record_digest_sha256=sha(
            "semantic-records"
        ),
        projection_contract_version=(
            "P5D3C2_SANDBOX_PROJECTION_V0_1"
        ),
        projection_tree_digest_sha256=(
            projection_tree_digest(root)
        ),
        generated_file_count=len(
            all_generated_files(root)
        ),
        breaker_status="PASS",
        determinism_status="PASS",
        breaker_manifest_digest_sha256=sha(
            "breaker-manifest"
        ),
        breaker_result_digest_sha256=sha(
            "breaker-result"
        ),
        determinism_evidence_digest_sha256=sha(
            "determinism-evidence"
        ),
    )


def canonical_file(value: object) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def content_digest(root: Path) -> str:
    rows: list[list[object]] = []
    for path in sorted(
        (
            p
            for p in root.rglob("*")
            if p.is_file()
        ),
        key=lambda p:
            p.relative_to(root).as_posix().encode(
                "utf-8"
            ),
    ):
        data = path.read_bytes()
        rows.append(
            [
                path.relative_to(root).as_posix(),
                len(data),
                hashlib.sha256(data).hexdigest(),
            ]
        )
    return hashlib.sha256(
        json.dumps(
            rows,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


class CandidateGenerationStagingTests(
    unittest.TestCase
):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(
            prefix="atds-p5d3c2-test-"
        )
        self.root = Path(self.temp.name)
        self.projection = self.root / "projection"
        self.projection.mkdir()
        build_projection(self.projection)
        self.candidate = candidate_for(
            self.projection
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def stage(
        self,
        name: str = "package",
    ) -> tuple[Path, dict]:
        package = self.root / name
        descriptor = stage_candidate_generation(
            self.candidate,
            verified_projection_root=self.projection,
            package_root=package,
        )
        return package, descriptor

    def clone_package(
        self,
        package: Path,
        name: str,
    ) -> Path:
        target = self.root / name
        shutil.copytree(package, target)
        return target

    def test_stage_and_verify_sealed_unpromoted(
        self,
    ) -> None:
        package, descriptor = self.stage()

        self.assertEqual(
            descriptor["verification_status"],
            "PASS_SEALED_UNPROMOTED",
        )
        self.assertFalse(
            descriptor["promotion_authorized"]
        )
        self.assertEqual(
            descriptor["candidate_head"],
            HEAD,
        )
        self.assertEqual(
            descriptor["candidate_tree"],
            TREE,
        )
        self.assertEqual(
            descriptor["payload_file_count"],
            4,
        )

        verified = verify_candidate_generation(
            package,
            expected_candidate=self.candidate,
        )
        self.assertEqual(verified, descriptor)

    def test_package_layout_is_exact(self) -> None:
        package, _ = self.stage()
        self.assertEqual(
            {p.name for p in package.iterdir()},
            {"generated", "_atds_generation"},
        )
        self.assertTrue(
            (
                package
                / "_atds_generation"
                / "payload-manifest.json"
            ).is_file()
        )
        self.assertTrue(
            (
                package
                / "_atds_generation"
                / "generation-manifest.json"
            ).is_file()
        )
        self.assertTrue(
            (
                package
                / "_atds_generation"
                / "SEAL.json"
            ).is_file()
        )
        for forbidden in (
            "CURRENT",
            "CURRENT.md",
            "CURRENT.json",
            "CURRENT.tmp",
            ".git",
            ".obsidian",
            "views",
        ):
            self.assertFalse(
                (package / forbidden).exists()
            )

    def test_manifests_bind_contract_and_status(
        self,
    ) -> None:
        package, _ = self.stage()
        generation = json.loads(
            (
                package
                / "_atds_generation"
                / "generation-manifest.json"
            ).read_text(encoding="utf-8")
        )
        seal = json.loads(
            (
                package
                / "_atds_generation"
                / "SEAL.json"
            ).read_text(encoding="utf-8")
        )

        self.assertEqual(
            generation["staging_contract_blob"],
            STAGING_CONTRACT_BLOB,
        )
        self.assertEqual(
            generation["breaker_status"],
            "PASS",
        )
        self.assertEqual(
            generation["determinism_status"],
            "PASS",
        )
        self.assertEqual(
            generation["package_status"],
            "COMPLETE_PENDING_SEAL",
        )
        self.assertEqual(
            seal["seal_status"],
            "SEALED_UNPROMOTED",
        )
        self.assertEqual(
            seal["staging_contract_blob"],
            STAGING_CONTRACT_BLOB,
        )

    def test_generation_identity_is_path_independent(
        self,
    ) -> None:
        package_a, descriptor_a = self.stage(
            "package-a"
        )
        package_b, descriptor_b = self.stage(
            "package-b"
        )

        self.assertNotEqual(package_a, package_b)
        self.assertEqual(
            descriptor_a["generation_id"],
            descriptor_b["generation_id"],
        )
        self.assertEqual(
            descriptor_a[
                "candidate_generation_digest_sha256"
            ],
            descriptor_b[
                "candidate_generation_digest_sha256"
            ],
        )

    def test_source_projection_is_not_mutated(self) -> None:
        before = content_digest(self.projection)
        self.stage()
        after = content_digest(self.projection)
        self.assertEqual(before, after)

    def test_verifier_is_repeatable_and_read_only(
        self,
    ) -> None:
        package, descriptor = self.stage()
        before = content_digest(package)

        first = verify_candidate_generation(
            package,
            expected_candidate=self.candidate,
        )
        middle = content_digest(package)
        second = verify_candidate_generation(
            package,
            expected_candidate=self.candidate,
        )
        after = content_digest(package)

        self.assertEqual(first, descriptor)
        self.assertEqual(second, descriptor)
        self.assertEqual(before, middle)
        self.assertEqual(middle, after)

    def test_stat_unavailability_is_infrastructure_block(
        self,
    ) -> None:
        with patch(
            "tools.obsidian_projection."
            "candidate_generation_staging."
            "validate_new_temp_staging_path",
            side_effect=IntegrityError(
                "cannot lstat path: synthetic"
            ),
        ):
            with self.assertRaises(
                CandidateGenerationInfrastructureError
            ):
                stage_candidate_generation(
                    self.candidate,
                    verified_projection_root=self.projection,
                    package_root=self.root / "infra-block",
                )

    def test_preexisting_package_root_is_rejected(
        self,
    ) -> None:
        package = self.root / "preexisting"
        package.mkdir()

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            stage_candidate_generation(
                self.candidate,
                verified_projection_root=self.projection,
                package_root=package,
            )

    def test_package_inside_projection_input_is_rejected(
        self,
    ) -> None:
        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            stage_candidate_generation(
                self.candidate,
                verified_projection_root=self.projection,
                package_root=(
                    self.projection / "nested-package"
                ),
            )

    def test_package_inside_forbidden_root_is_rejected(
        self,
    ) -> None:
        forbidden = self.root / "forbidden"
        forbidden.mkdir()

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            stage_candidate_generation(
                self.candidate,
                verified_projection_root=self.projection,
                package_root=forbidden / "package",
                forbidden_roots=(forbidden,),
            )

    def test_breaker_status_must_be_pass(self) -> None:
        candidate = VerifiedProjectionCandidate(
            **{
                **self.candidate.__dict__,
                "breaker_status": "FAIL",
            }
        )
        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            stage_candidate_generation(
                candidate,
                verified_projection_root=self.projection,
                package_root=self.root / "bad-breaker",
            )

    def test_determinism_status_must_be_pass(
        self,
    ) -> None:
        candidate = VerifiedProjectionCandidate(
            **{
                **self.candidate.__dict__,
                "determinism_status": "FAIL",
            }
        )
        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            stage_candidate_generation(
                candidate,
                verified_projection_root=self.projection,
                package_root=self.root / "bad-determinism",
            )

    def test_projection_tree_mismatch_is_rejected(
        self,
    ) -> None:
        candidate = VerifiedProjectionCandidate(
            **{
                **self.candidate.__dict__,
                "projection_tree_digest_sha256":
                    sha("wrong-projection-tree"),
            }
        )
        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            stage_candidate_generation(
                candidate,
                verified_projection_root=self.projection,
                package_root=self.root / "bad-tree",
            )

    def test_generated_file_count_mismatch_is_rejected(
        self,
    ) -> None:
        candidate = VerifiedProjectionCandidate(
            **{
                **self.candidate.__dict__,
                "generated_file_count": 5,
            }
        )
        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            stage_candidate_generation(
                candidate,
                verified_projection_root=self.projection,
                package_root=self.root / "bad-count",
            )

    def test_current_like_payload_is_rejected(
        self,
    ) -> None:
        write_file(
            self.projection
            / "generated"
            / "artifacts"
            / "CURRENT.md",
            b"forbidden\n",
        )
        candidate = candidate_for(
            self.projection
        )
        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            stage_candidate_generation(
                candidate,
                verified_projection_root=self.projection,
                package_root=self.root / "current-payload",
            )

    def test_dot_obsidian_payload_is_rejected(
        self,
    ) -> None:
        write_file(
            self.projection
            / "generated"
            / ".obsidian"
            / "x.json",
            b"{}\n",
        )
        candidate = candidate_for(
            self.projection
        )
        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            stage_candidate_generation(
                candidate,
                verified_projection_root=self.projection,
                package_root=self.root / "obsidian-payload",
            )

    def test_payload_byte_mutation_is_rejected(
        self,
    ) -> None:
        package, _ = self.stage()
        mutant = self.clone_package(
            package,
            "mut-byte",
        )
        path = (
            mutant
            / "generated"
            / "artifacts"
            / "a.md"
        )
        path.write_bytes(b"# MUTATED\n")

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            verify_candidate_generation(mutant)

    def test_payload_deletion_is_rejected(self) -> None:
        package, _ = self.stage()
        mutant = self.clone_package(
            package,
            "mut-delete",
        )
        (
            mutant
            / "generated"
            / "artifacts"
            / "a.md"
        ).unlink()

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            verify_candidate_generation(mutant)

    def test_unmanifested_extra_file_is_rejected(
        self,
    ) -> None:
        package, _ = self.stage()
        mutant = self.clone_package(
            package,
            "mut-extra",
        )
        write_file(
            mutant
            / "generated"
            / "artifacts"
            / "extra.md",
            b"extra\n",
        )

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            verify_candidate_generation(mutant)

    def test_payload_manifest_mutation_is_rejected(
        self,
    ) -> None:
        package, _ = self.stage()
        mutant = self.clone_package(
            package,
            "mut-payload-manifest",
        )
        path = (
            mutant
            / "_atds_generation"
            / "payload-manifest.json"
        )
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
        value["file_count"] += 1
        path.write_bytes(canonical_file(value))

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            verify_candidate_generation(mutant)

    def test_generation_manifest_mutation_is_rejected(
        self,
    ) -> None:
        package, _ = self.stage()
        mutant = self.clone_package(
            package,
            "mut-generation-manifest",
        )
        path = (
            mutant
            / "_atds_generation"
            / "generation-manifest.json"
        )
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
        value["breaker_status"] = "FAIL"
        path.write_bytes(canonical_file(value))

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            verify_candidate_generation(mutant)

    def test_seal_mutation_is_rejected(self) -> None:
        package, _ = self.stage()
        mutant = self.clone_package(
            package,
            "mut-seal",
        )
        path = (
            mutant
            / "_atds_generation"
            / "SEAL.json"
        )
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
        value["seal_status"] = "SEALED_TAMPERED"
        path.write_bytes(canonical_file(value))

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            verify_candidate_generation(mutant)

    def test_noncanonical_manifest_bytes_are_rejected(
        self,
    ) -> None:
        package, _ = self.stage()
        mutant = self.clone_package(
            package,
            "mut-noncanonical",
        )
        path = (
            mutant
            / "_atds_generation"
            / "payload-manifest.json"
        )
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
        path.write_text(
            json.dumps(
                value,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            verify_candidate_generation(mutant)

    def test_extra_generation_manifest_field_is_rejected(
        self,
    ) -> None:
        package, _ = self.stage()
        mutant = self.clone_package(
            package,
            "mut-extra-manifest-field",
        )
        path = (
            mutant
            / "_atds_generation"
            / "generation-manifest.json"
        )
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
        value["generated_at"] = "forbidden"
        path.write_bytes(canonical_file(value))

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            verify_candidate_generation(mutant)

    def test_verifier_recomputes_projection_tree_digest(
        self,
    ) -> None:
        package, _ = self.stage()

        with patch(
            "tools.obsidian_projection."
            "candidate_generation_staging."
            "projection_tree_digest",
            return_value=sha("wrong-packaged-tree"),
        ):
            with self.assertRaises(
                CandidateGenerationInvalidError
            ):
                verify_candidate_generation(
                    package
                )

    def test_expected_candidate_mismatch_is_rejected(
        self,
    ) -> None:
        package, _ = self.stage()
        wrong = VerifiedProjectionCandidate(
            **{
                **self.candidate.__dict__,
                "candidate_head": "3" * 40,
            }
        )

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            verify_candidate_generation(
                package,
                expected_candidate=wrong,
            )

    def test_hard_link_alias_is_rejected(self) -> None:
        package, _ = self.stage()
        mutant = self.clone_package(
            package,
            "mut-hardlink",
        )
        first = (
            mutant
            / "generated"
            / "artifacts"
            / "a.md"
        )
        second = (
            mutant
            / "generated"
            / "artifacts"
            / "b.json"
        )
        second.unlink()

        try:
            os.link(first, second)
        except OSError as exc:
            self.skipTest(
                f"hard-link capability unavailable: {exc}"
            )

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            verify_candidate_generation(mutant)

    def test_symlink_is_rejected_when_capability_exists(
        self,
    ) -> None:
        package, _ = self.stage()
        mutant = self.clone_package(
            package,
            "mut-symlink",
        )
        target = (
            mutant
            / "generated"
            / "artifacts"
            / "a.md"
        )
        link = (
            mutant
            / "generated"
            / "artifacts"
            / "b.json"
        )
        link.unlink()

        try:
            os.symlink(
                target.name,
                link,
                target_is_directory=False,
            )
        except OSError as exc:
            self.skipTest(
                f"symlink capability unavailable: {exc}"
            )

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            verify_candidate_generation(mutant)

    def test_descriptor_contains_no_absolute_stage_path(
        self,
    ) -> None:
        package, descriptor = self.stage()
        serialized = json.dumps(
            descriptor,
            sort_keys=True,
        )
        self.assertNotIn(
            str(package),
            serialized,
        )
        self.assertNotIn(
            str(self.root),
            serialized,
        )
        self.assertFalse(
            descriptor["promotion_authorized"]
        )


if __name__ == "__main__":
    unittest.main()
