from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from tools.obsidian_projection.git_source import (
    FrozenGitSource,
    FrozenSourceError,
    RepositoryIdentityError,
    UnsafeGitInvocationError,
    normalize_origin,
    validate_git_args,
)

COMMIT = "1" * 40
TREE = "2" * 40
BLOB = "3" * 40


class FakeRunner:
    def __init__(
        self,
        repo_root: Path,
        responses: dict[tuple[str, ...], bytes],
    ) -> None:
        self.repo_root = repo_root.resolve()
        self.responses = responses
        self.calls: list[tuple[str, ...]] = []

    def __call__(self, repo_root: Path, args) -> bytes:
        if repo_root.resolve() != self.repo_root:
            raise AssertionError("unexpected repo root")
        key = tuple(args)
        self.calls.append(key)
        if key not in self.responses:
            raise FrozenSourceError(
                f"unexpected synthetic git call: {key}"
            )
        return self.responses[key]


class GitSourceTests(unittest.TestCase):
    def _source(
        self,
        root: Path,
        responses: dict[tuple[str, ...], bytes],
    ):
        runner = FakeRunner(root, responses)
        source = FrozenGitSource(
            root,
            "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
            COMMIT,
            TREE,
            runner=runner,
        )
        return source, runner

    def test_origin_normalization(self) -> None:
        expected = (
            "thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM"
        )
        self.assertEqual(
            normalize_origin(
                "https://github.com/" + expected + ".git"
            ),
            expected,
        )
        self.assertEqual(
            normalize_origin(
                "git@github.com:" + expected + ".git"
            ),
            expected,
        )

    def test_verify_exact_repository_and_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            responses = {
                ("rev-parse", "--show-toplevel"):
                    (str(root) + "\n").encode(),
                ("remote", "get-url", "origin"):
                    (
                        "https://github.com/thboulevart-creator/"
                        "ADAPTIVE-TRADING-DECISION-SYSTEM.git\n"
                    ).encode(),
                ("cat-file", "-t", COMMIT):
                    b"commit\n",
                ("rev-parse", f"{COMMIT}^{{tree}}"):
                    (TREE + "\n").encode(),
            }
            source, _ = self._source(root, responses)
            source.verify_repository()
            source.verify_frozen_source()

    def test_wrong_repository_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            responses = {
                ("rev-parse", "--show-toplevel"):
                    (str(root) + "\n").encode(),
                ("remote", "get-url", "origin"):
                    b"https://github.com/example/wrong.git\n",
            }
            source, _ = self._source(root, responses)
            with self.assertRaises(
                RepositoryIdentityError
            ):
                source.verify_repository()

    def test_wrong_tree_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            responses = {
                ("cat-file", "-t", COMMIT):
                    b"commit\n",
                ("rev-parse", f"{COMMIT}^{{tree}}"):
                    (("4" * 40) + "\n").encode(),
            }
            source, _ = self._source(root, responses)
            with self.assertRaises(FrozenSourceError):
                source.verify_frozen_source()

    def test_missing_blob_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            source, _ = self._source(root, {})
            with self.assertRaises(FrozenSourceError):
                source.read_blob(BLOB)

    def test_raw_blob_never_requests_transform_modes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            raw = b"a\nb\n"
            responses = {
                ("cat-file", "-t", BLOB): b"blob\n",
                ("cat-file", "blob", BLOB): raw,
            }
            source, runner = self._source(
                root,
                responses,
            )
            self.assertEqual(
                source.read_blob(BLOB),
                raw,
            )
            flattened = [
                arg
                for call in runner.calls
                for arg in call
            ]
            self.assertNotIn("--filters", flattened)
            self.assertNotIn("--textconv", flattened)

    def test_working_tree_crlf_does_not_change_raw_blob(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            local_file = root / "fixture.txt"
            local_file.write_bytes(b"a\r\nb\r\n")

            canonical = b"a\nb\n"
            responses = {
                ("cat-file", "-t", BLOB):
                    b"blob\n",
                ("cat-file", "blob", BLOB):
                    canonical,
            }

            source, _ = self._source(
                root,
                responses,
            )
            actual = source.read_blob(BLOB)

            self.assertEqual(actual, canonical)
            self.assertNotEqual(
                actual,
                local_file.read_bytes(),
            )
            self.assertEqual(
                hashlib.sha256(actual).hexdigest(),
                hashlib.sha256(canonical).hexdigest(),
            )

    def test_transform_options_are_rejected(self) -> None:
        with self.assertRaises(
            UnsafeGitInvocationError
        ):
            validate_git_args(
                ("cat-file", "--filters", BLOB)
            )

        with self.assertRaises(
            UnsafeGitInvocationError
        ):
            validate_git_args(
                ("cat-file", "--textconv", BLOB)
            )


if __name__ == "__main__":
    unittest.main()
