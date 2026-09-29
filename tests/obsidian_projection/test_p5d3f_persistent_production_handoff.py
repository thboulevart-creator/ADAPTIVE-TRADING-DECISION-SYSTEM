from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.persistent_production_handoff import (
    PERSISTENT_GATE_CONTRACT_BLOB,
    QUALIFIED_P5D3F_IMPLEMENTATION_BLOB,
    PersistentHandoffBlockedError,
    PersistentHandoffGovernanceError,
    assert_zero_real_vault_mutation,
    fingerprint_tree,
    validate_persistent_paths,
    validate_staging_prestate,
)


def _write(root: Path, relative: str, raw: bytes) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


class P5D3FPersistentProductionHandoffTests(
    unittest.TestCase
):
    def test_authority_pins_are_exact(self) -> None:
        self.assertEqual(
            PERSISTENT_GATE_CONTRACT_BLOB,
            "59ce9e079d256799d072405fa4a623ba58b75c0d",
        )
        self.assertEqual(
            QUALIFIED_P5D3F_IMPLEMENTATION_BLOB,
            "cb8dd498fbc503acfcccb38799965c8139db82a7",
        )

    def test_exact_sibling_paths_are_accepted(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-persistent-paths-"
        ) as temp:
            parent = Path(temp)
            vault = parent / "vault"
            vault.mkdir()
            staging = parent / "staging"

            with (
                patch(
                    "tools.obsidian_projection."
                    "persistent_production_handoff.REAL_VAULT",
                    vault,
                ),
                patch(
                    "tools.obsidian_projection."
                    "persistent_production_handoff.PERSISTENT_STAGING",
                    staging,
                ),
            ):
                actual_staging, actual_vault = (
                    validate_persistent_paths()
                )

            self.assertEqual(actual_staging, staging.resolve())
            self.assertEqual(actual_vault, vault.resolve())

    def test_wrong_real_vault_identity_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-wrong-vault-"
        ) as temp:
            parent = Path(temp)
            vault = parent / "vault"
            vault.mkdir()
            staging = parent / "staging"
            wrong = parent / "wrong"
            wrong.mkdir()

            with (
                patch(
                    "tools.obsidian_projection."
                    "persistent_production_handoff.REAL_VAULT",
                    vault,
                ),
                patch(
                    "tools.obsidian_projection."
                    "persistent_production_handoff.PERSISTENT_STAGING",
                    staging,
                ),
            ):
                with self.assertRaises(
                    PersistentHandoffGovernanceError
                ):
                    validate_persistent_paths(
                        real_vault_root=wrong,
                    )

    def test_staging_and_vault_must_be_siblings(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-nonsibling-"
        ) as temp:
            parent = Path(temp)
            vault = parent / "vault"
            vault.mkdir()
            other = parent / "nested"
            other.mkdir()
            staging = other / "staging"

            with (
                patch(
                    "tools.obsidian_projection."
                    "persistent_production_handoff.REAL_VAULT",
                    vault,
                ),
                patch(
                    "tools.obsidian_projection."
                    "persistent_production_handoff.PERSISTENT_STAGING",
                    staging,
                ),
            ):
                with self.assertRaises(
                    PersistentHandoffGovernanceError
                ):
                    validate_persistent_paths()

    def test_absent_staging_prestate_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-staging-absent-"
        ) as temp:
            staging = Path(temp) / "staging"
            self.assertEqual(
                validate_staging_prestate(staging),
                "ABSENT",
            )

    def test_empty_staging_prestate_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-staging-empty-"
        ) as temp:
            staging = Path(temp) / "staging"
            staging.mkdir()
            self.assertEqual(
                validate_staging_prestate(staging),
                "PRESENT_EMPTY",
            )

    def test_nonempty_staging_prestate_blocks(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-staging-conflict-"
        ) as temp:
            staging = Path(temp) / "staging"
            staging.mkdir()
            _write(
                staging,
                "unknown.txt",
                b"UNKNOWN\n",
            )
            with self.assertRaises(
                PersistentHandoffBlockedError
            ):
                validate_staging_prestate(staging)

    def test_fingerprint_is_deterministic_and_binds_bytes(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-fingerprint-"
        ) as temp:
            root = Path(temp)
            _write(root, "a.txt", b"A\n")
            _write(root, "nested/b.bin", b"\x00\x01")

            first = fingerprint_tree(root)
            second = fingerprint_tree(root)
            self.assertEqual(first, second)

            _write(root, "a.txt", b"B\n")
            third = fingerprint_tree(root)
            self.assertNotEqual(
                first["tree_digest_sha256"],
                third["tree_digest_sha256"],
            )

    def test_fingerprint_binds_current_and_current_tmp_state(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-current-fingerprint-"
        ) as temp:
            root = Path(temp)
            first = fingerprint_tree(root)
            self.assertEqual(first["current_state"], "ABSENT")
            self.assertEqual(first["current_tmp_state"], "ABSENT")

            _write(root, "CURRENT.md", b"CURRENT\n")
            _write(root, "CURRENT.tmp", b"TMP\n")
            second = fingerprint_tree(root)
            self.assertEqual(second["current_state"], "PRESENT")
            self.assertEqual(second["current_tmp_state"], "PRESENT")
            self.assertEqual(
                second["current_sha256"],
                hashlib.sha256(b"CURRENT\n").hexdigest(),
            )

    def test_zero_mutation_accepts_identical_fingerprints(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-zero-equal-"
        ) as temp:
            root = Path(temp)
            _write(root, "sentinel.txt", b"UNCHANGED\n")
            before = fingerprint_tree(root)
            after = fingerprint_tree(root)
            proof = assert_zero_real_vault_mutation(
                before,
                after,
            )
            self.assertTrue(proof["unchanged"])

    def test_zero_mutation_rejects_created_path(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-zero-created-"
        ) as temp:
            root = Path(temp)
            before = fingerprint_tree(root)
            _write(root, "created.txt", b"CREATED\n")
            after = fingerprint_tree(root)
            with self.assertRaises(
                PersistentHandoffGovernanceError
            ):
                assert_zero_real_vault_mutation(
                    before,
                    after,
                )

    def test_zero_mutation_rejects_deleted_path(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-zero-deleted-"
        ) as temp:
            root = Path(temp)
            _write(root, "delete-me.txt", b"DELETE\n")
            before = fingerprint_tree(root)
            (root / "delete-me.txt").unlink()
            after = fingerprint_tree(root)
            with self.assertRaises(
                PersistentHandoffGovernanceError
            ):
                assert_zero_real_vault_mutation(
                    before,
                    after,
                )

    def test_zero_mutation_rejects_byte_change(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-zero-bytes-"
        ) as temp:
            root = Path(temp)
            _write(root, "same-path.txt", b"A\n")
            before = fingerprint_tree(root)
            _write(root, "same-path.txt", b"B\n")
            after = fingerprint_tree(root)
            with self.assertRaises(
                PersistentHandoffGovernanceError
            ):
                assert_zero_real_vault_mutation(
                    before,
                    after,
                )

    @unittest.skipUnless(
        hasattr(os, "symlink"),
        "symlink unsupported",
    )
    def test_fingerprint_rejects_alias_when_creatable(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-alias-"
        ) as temp:
            root = Path(temp)
            _write(root, "real.txt", b"REAL\n")
            alias = root / "alias.txt"
            try:
                os.symlink(
                    root / "real.txt",
                    alias,
                )
            except OSError:
                self.skipTest(
                    "symlink creation not permitted"
                )

            with self.assertRaises(
                PersistentHandoffGovernanceError
            ):
                fingerprint_tree(root)

    def test_source_contains_no_live_publication_or_stage_authority(
        self,
    ) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "persistent_production_handoff.py"
        ).read_text(encoding="utf-8")

        forbidden = (
            "execute_finite_live_publication",
            "PROMOTION_CONFIRMED",
            "STAGE_A",
            "STAGE_B",
            "os.replace(",
            "CURRENT.tmp",
            "threading.Thread",
            "while True",
            "schtasks",
            "CreateService",
        )
        for token in forbidden:
            self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
