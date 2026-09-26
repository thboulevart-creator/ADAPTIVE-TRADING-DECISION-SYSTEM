from __future__ import annotations

import hashlib
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping, Sequence

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_FORBIDDEN_GIT_OPTIONS = frozenset({"--filters", "--textconv"})


class GitSourceError(RuntimeError):
    """Base error for the canonical Git source boundary."""


class RepositoryIdentityError(GitSourceError):
    """Raised when the local repository is not the expected repository."""


class FrozenSourceError(GitSourceError):
    """Raised when the frozen commit/tree/blob contract is not satisfied."""


class UnsafeGitInvocationError(GitSourceError):
    """Raised when a working-tree transforming Git mode is requested."""


@dataclass(frozen=True)
class TreeEntry:
    path: str
    mode: str
    object_type: str
    oid: str
    size: int | None


GitRunner = Callable[[Path, Sequence[str]], bytes]


def normalize_origin(origin: str) -> str:
    """Normalize supported GitHub origin forms to owner/repository."""
    value = origin.strip()
    if value.startswith("git@github.com:"):
        value = value[len("git@github.com:") :]
    elif value.startswith("https://github.com/"):
        value = value[len("https://github.com/") :]
    elif value.startswith("ssh://git@github.com/"):
        value = value[len("ssh://git@github.com/") :]
    else:
        raise RepositoryIdentityError(f"unsupported GitHub origin form: {origin!r}")

    if value.endswith(".git"):
        value = value[:-4]
    value = value.strip("/")
    if value.count("/") != 1 or not all(value.split("/", 1)):
        raise RepositoryIdentityError(f"invalid normalized GitHub origin: {value!r}")
    return value


def validate_git_args(args: Sequence[str]) -> None:
    """Reject modes that transform canonical Git-object bytes."""
    for arg in args:
        if (
            arg in _FORBIDDEN_GIT_OPTIONS
            or arg.startswith("--filters=")
            or arg.startswith("--textconv=")
        ):
            raise UnsafeGitInvocationError(
                f"forbidden Git transformation option: {arg}"
            )


def _default_git_runner(repo_root: Path, args: Sequence[str]) -> bytes:
    validate_git_args(args)
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    )
    if completed.returncode != 0:
        stderr = completed.stderr.decode("utf-8", errors="replace").strip()
        raise GitSourceError(f"git {' '.join(args)} failed: {stderr}")
    return completed.stdout


class FrozenGitSource:
    """Read-only access to an exact governed Git commit/tree/blob domain."""

    def __init__(
        self,
        repo_root: str | Path,
        expected_repository: str,
        source_commit: str,
        expected_tree: str,
        *,
        runner: GitRunner | None = None,
    ) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.expected_repository = expected_repository
        self.source_commit = self._require_oid(source_commit, "source_commit")
        self.expected_tree = self._require_oid(expected_tree, "expected_tree")
        self._runner = runner or _default_git_runner

    @staticmethod
    def _require_oid(value: str, field: str) -> str:
        lowered = value.lower()
        if not _HEX40.fullmatch(lowered):
            raise ValueError(
                f"{field} must be a full 40-character hexadecimal Git object id"
            )
        return lowered

    def _git(self, *args: str) -> bytes:
        validate_git_args(args)
        return self._runner(self.repo_root, args)

    def verify_repository(self) -> None:
        top_level = (
            self._git("rev-parse", "--show-toplevel")
            .decode("utf-8")
            .strip()
        )
        if Path(top_level).resolve() != self.repo_root:
            raise RepositoryIdentityError(
                f"repo_root mismatch: configured={self.repo_root} "
                f"git={Path(top_level).resolve()}"
            )

        origin = (
            self._git("remote", "get-url", "origin")
            .decode("utf-8")
            .strip()
        )
        actual_repository = normalize_origin(origin)
        if actual_repository != self.expected_repository:
            raise RepositoryIdentityError(
                f"repository mismatch: expected={self.expected_repository} "
                f"actual={actual_repository}"
            )

    def verify_frozen_source(self) -> None:
        object_type = (
            self._git("cat-file", "-t", self.source_commit)
            .decode("ascii")
            .strip()
        )
        if object_type != "commit":
            raise FrozenSourceError(
                f"frozen source is not a commit: "
                f"{self.source_commit} type={object_type}"
            )

        actual_tree = (
            self._git("rev-parse", f"{self.source_commit}^{{tree}}")
            .decode("ascii")
            .strip()
        )
        if actual_tree != self.expected_tree:
            raise FrozenSourceError(
                f"tree mismatch: expected={self.expected_tree} actual={actual_tree}"
            )

    def read_blob(self, oid: str) -> bytes:
        blob_oid = self._require_oid(oid, "blob_oid")
        object_type = (
            self._git("cat-file", "-t", blob_oid)
            .decode("ascii")
            .strip()
        )
        if object_type != "blob":
            raise FrozenSourceError(
                f"object is not a blob: {blob_oid} type={object_type}"
            )
        return self._git("cat-file", "blob", blob_oid)

    def blob_size(self, oid: str) -> int:
        blob_oid = self._require_oid(oid, "blob_oid")
        raw = self._git("cat-file", "-s", blob_oid).decode("ascii").strip()
        try:
            return int(raw)
        except ValueError as exc:
            raise FrozenSourceError(
                f"invalid blob size for {blob_oid}: {raw!r}"
            ) from exc

    def tree_entries(self) -> tuple[TreeEntry, ...]:
        raw = self._git("ls-tree", "-rz", "-l", self.source_commit)
        entries: list[TreeEntry] = []

        for record in raw.split(b"\0"):
            if not record:
                continue
            try:
                header, path_raw = record.split(b"\t", 1)
            except ValueError as exc:
                raise FrozenSourceError(
                    "malformed git ls-tree record"
                ) from exc

            fields = header.split()
            if len(fields) != 4:
                raise FrozenSourceError(
                    f"malformed git ls-tree header: {header!r}"
                )

            mode_b, type_b, oid_b, size_b = fields
            try:
                oid = oid_b.decode("ascii").lower()
            except UnicodeDecodeError as exc:
                raise FrozenSourceError(
                    "non-ASCII Git object id in tree"
                ) from exc

            self._require_oid(oid, "tree_entry_oid")
            size = None if size_b == b"-" else int(size_b)

            entries.append(
                TreeEntry(
                    path=path_raw.decode(
                        "utf-8",
                        errors="surrogateescape",
                    ),
                    mode=mode_b.decode("ascii"),
                    object_type=type_b.decode("ascii"),
                    oid=oid,
                    size=size,
                )
            )

        return tuple(entries)

    def tree_entry_map(self) -> Mapping[str, TreeEntry]:
        result: dict[str, TreeEntry] = {}
        for entry in self.tree_entries():
            if entry.path in result:
                raise FrozenSourceError(
                    f"duplicate path in Git tree: {entry.path}"
                )
            result[entry.path] = entry
        return result

    def read_path(self, path: str) -> bytes:
        entry = self.tree_entry_map().get(path)
        if entry is None:
            raise FrozenSourceError(
                f"path not present in frozen tree: {path}"
            )
        if entry.object_type != "blob" or entry.mode == "120000":
            raise FrozenSourceError(
                f"path is not an admissible regular blob: {path} "
                f"type={entry.object_type} mode={entry.mode}"
            )
        return self.read_blob(entry.oid)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
