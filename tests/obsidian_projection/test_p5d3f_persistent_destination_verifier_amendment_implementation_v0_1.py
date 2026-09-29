from __future__ import annotations

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.obsidian_projection.test_candidate_generation_staging import (
    build_projection,
    candidate_for,
    content_digest,
)
from tools.obsidian_projection import candidate_generation_staging as cgs
from tools.obsidian_projection.candidate_generation_staging import (
    CandidateGenerationInvalidError,
    stage_candidate_generation,
    verify_candidate_generation,
    verify_persistent_candidate_generation,
)


class P5D3FPersistentDestinationVerifierAmendmentImplementationV01Tests(
    unittest.TestCase
):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(
            prefix="p5d3f-persistent-verifier-"
        )
        self.root = Path(self.temp.name)

        self.projection = self.root / "projection"
        self.projection.mkdir()
        build_projection(self.projection)

        self.candidate = candidate_for(
            self.projection
        )

        self.source_package = (
            self.root / "source-package"
        )
        self.source_descriptor = (
            stage_candidate_generation(
                self.candidate,
                verified_projection_root=(
                    self.projection
                ),
                package_root=self.source_package,
            )
        )

        self.staging = (
            self.root / "persistent-staging"
        )
        self.staging.mkdir()

        self.generation_root = (
            self.staging
            / "packages"
            / self.source_descriptor["generation_id"]
        )
        self.generation_root.mkdir(
            parents=True
        )

        self.persistent_package = (
            self.generation_root / "package"
        )
        shutil.copytree(
            self.source_package,
            self.persistent_package,
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def verify_persistent(
        self,
        package: Path | None = None,
        *,
        staging: Path | None = None,
        forbidden_roots: tuple[Path, ...] = (),
    ) -> dict:
        return verify_persistent_candidate_generation(
            package or self.persistent_package,
            authorized_staging_root=(
                staging or self.staging
            ),
            expected_candidate=self.candidate,
            forbidden_roots=forbidden_roots,
        )

    def test_historical_temp_verifier_remains_temp_only(
        self,
    ) -> None:
        fake_temp = self.root / "different-temp"

        with patch(
            "tools.obsidian_projection."
            "candidate_generation_staging."
            "tempfile.gettempdir",
            return_value=str(fake_temp),
        ):
            with self.assertRaises(
                CandidateGenerationInvalidError
            ):
                verify_candidate_generation(
                    self.source_package
                )

    def test_persistent_verifier_accepts_exact_authorized_wrapper(
        self,
    ) -> None:
        descriptor = self.verify_persistent()
        self.assertEqual(
            descriptor,
            self.source_descriptor,
        )

    def test_temp_and_persistent_verifiers_have_descriptor_parity(
        self,
    ) -> None:
        temp_descriptor = verify_candidate_generation(
            self.source_package,
            expected_candidate=self.candidate,
        )
        persistent_descriptor = (
            self.verify_persistent()
        )
        self.assertEqual(
            persistent_descriptor,
            temp_descriptor,
        )

    def test_persistent_verifier_is_read_only(
        self,
    ) -> None:
        before = content_digest(
            self.persistent_package
        )
        first = self.verify_persistent()
        middle = content_digest(
            self.persistent_package
        )
        second = self.verify_persistent()
        after = content_digest(
            self.persistent_package
        )

        self.assertEqual(
            first,
            self.source_descriptor,
        )
        self.assertEqual(second, first)
        self.assertEqual(before, middle)
        self.assertEqual(middle, after)

    def test_wrong_authorized_staging_root_is_rejected(
        self,
    ) -> None:
        wrong_staging = self.root / "wrong-staging"
        wrong_staging.mkdir()

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            self.verify_persistent(
                staging=wrong_staging
            )

    def test_wrong_wrapper_layout_is_rejected(
        self,
    ) -> None:
        wrong_root = (
            self.staging
            / "wrong"
            / self.source_descriptor["generation_id"]
        )
        wrong_root.mkdir(
            parents=True
        )
        wrong_package = wrong_root / "package"
        shutil.copytree(
            self.source_package,
            wrong_package,
        )

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            self.verify_persistent(
                package=wrong_package
            )

    def test_arbitrary_package_outside_authorized_staging_is_rejected(
        self,
    ) -> None:
        arbitrary_root = (
            self.root
            / "arbitrary"
            / "packages"
            / self.source_descriptor["generation_id"]
        )
        arbitrary_root.mkdir(
            parents=True
        )
        arbitrary_package = (
            arbitrary_root / "package"
        )
        shutil.copytree(
            self.source_package,
            arbitrary_package,
        )

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            self.verify_persistent(
                package=arbitrary_package
            )

    def test_real_vault_intersection_is_rejected(
        self,
    ) -> None:
        vault = self.root / "real-vault"
        vault.mkdir()

        wrapper = (
            vault
            / "packages"
            / self.source_descriptor["generation_id"]
        )
        wrapper.mkdir(
            parents=True
        )
        package = wrapper / "package"
        shutil.copytree(
            self.source_package,
            package,
        )

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            self.verify_persistent(
                package=package,
                staging=vault,
                forbidden_roots=(vault,),
            )

    def test_alias_reparse_chain_is_rejected(
        self,
    ) -> None:
        packages_root = self.staging / "packages"
        original = cgs._is_reparse_or_symlink

        def synthetic_alias(path: Path) -> bool:
            if Path(path) == packages_root:
                return True
            return original(Path(path))

        with patch(
            "tools.obsidian_projection."
            "candidate_generation_staging."
            "_is_reparse_or_symlink",
            side_effect=synthetic_alias,
        ):
            with self.assertRaises(
                CandidateGenerationInvalidError
            ):
                self.verify_persistent()


    def test_authorized_staging_ancestor_alias_is_rejected(
        self,
    ) -> None:
        ancestor = self.staging.parent
        original = cgs._is_reparse_or_symlink

        def synthetic_alias(path: Path) -> bool:
            if Path(path) == ancestor:
                return True
            return original(Path(path))

        with patch(
            "tools.obsidian_projection."
            "candidate_generation_staging."
            "_is_reparse_or_symlink",
            side_effect=synthetic_alias,
        ):
            with self.assertRaises(
                CandidateGenerationInvalidError
            ):
                self.verify_persistent()

    def test_hardlink_alias_is_rejected(
        self,
    ) -> None:
        payload = next(
            path
            for path in (
                self.persistent_package / "generated"
            ).rglob("*")
            if path.is_file()
        )
        external_link = (
            self.staging / "synthetic-hardlink"
        )

        try:
            os.link(
                payload,
                external_link,
            )
        except OSError as exc:
            self.skipTest(
                f"hard-link capability unavailable: {exc}"
            )

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            self.verify_persistent()

    def test_tampered_payload_is_rejected(
        self,
    ) -> None:
        payload = next(
            path
            for path in (
                self.persistent_package / "generated"
            ).rglob("*")
            if path.is_file()
        )
        payload.write_bytes(
            payload.read_bytes() + b"TAMPER"
        )

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            self.verify_persistent()

    def test_tampered_generation_manifest_is_rejected(
        self,
    ) -> None:
        path = (
            self.persistent_package
            / "_atds_generation"
            / "generation-manifest.json"
        )
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
        value["breaker_status"] = "FAIL"
        path.write_bytes(
            (
                json.dumps(
                    value,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                    allow_nan=False,
                )
                + "\n"
            ).encode("utf-8")
        )

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            self.verify_persistent()

    def test_tampered_seal_is_rejected(
        self,
    ) -> None:
        path = (
            self.persistent_package
            / "_atds_generation"
            / "SEAL.json"
        )
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
        value["seal_status"] = "SEALED_TAMPERED"
        path.write_bytes(
            (
                json.dumps(
                    value,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                    allow_nan=False,
                )
                + "\n"
            ).encode("utf-8")
        )

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            self.verify_persistent()

    def test_wrapper_generation_id_must_match_descriptor(
        self,
    ) -> None:
        wrong_wrapper = (
            self.staging
            / "packages"
            / ("0" * 64)
        )
        wrong_wrapper.mkdir(
            parents=True
        )
        wrong_package = (
            wrong_wrapper / "package"
        )
        shutil.copytree(
            self.source_package,
            wrong_package,
        )

        with self.assertRaises(
            CandidateGenerationInvalidError
        ):
            self.verify_persistent(
                package=wrong_package
            )

    def test_temp_and_persistent_verifiers_share_one_content_core(
        self,
    ) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "candidate_generation_staging.py"
        ).read_text(encoding="utf-8")

        self.assertEqual(
            source.count(
                "def _verify_candidate_generation_content("
            ),
            1,
        )
        self.assertGreaterEqual(
            source.count(
                "_verify_candidate_generation_content("
            ),
            3,
        )


    def test_p5d3f_destination_is_bound_to_persistent_verifier(
        self,
    ) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "p5d3f_promotion_handoff.py"
        ).read_text(encoding="utf-8")

        start = source.index(
            "destination_descriptor ="
        )
        window = source[
            start:start + 1400
        ]

        self.assertIn(
            "verify_persistent_candidate_generation(",
            window,
        )
        self.assertIn(
            "authorized_staging_root=staging",
            window,
        )
        self.assertNotIn(
            "verify_candidate_generation(\n"
            "                    destination_package",
            window,
        )

    def test_post_write_reverification_uses_explicit_staging_authority(
        self,
    ) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "p5d3f_promotion_handoff.py"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "promotion_staging_root=staging",
            source,
        )
        self.assertIn(
            "verify_persistent_candidate_generation(",
            source,
        )

    def test_persistent_wrapper_reverification_passes_staging_authority(
        self,
    ) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "persistent_production_handoff.py"
        ).read_text(encoding="utf-8")

        self.assertIn(
            'QUALIFIED_P5D3F_IMPLEMENTATION_BLOB = (\n'
            '    "23a4cc69b3b9f6fab1a6d77bed0247fce9b69c60"\n'
            ')',
            source,
        )
        self.assertIn(
            "verified = verify_promotion_handoff(\n"
            "            handoff_root,\n"
            "            live_vault_root=vault,\n"
            "            promotion_staging_root=staging,\n"
            "        )",
            source,
        )


    def test_no_later_publication_authority_is_added(
        self,
    ) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "candidate_generation_staging.py"
        ).read_text(encoding="utf-8")

        for forbidden in (
            "execute_finite_live_publication",
            "PROMOTION_CONFIRMED",
            "threading.Thread",
            "schtasks",
            "CreateService",
        ):
            self.assertNotIn(
                forbidden,
                source,
            )


if __name__ == "__main__":
    unittest.main()
