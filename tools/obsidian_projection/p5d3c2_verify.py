from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Callable

from .candidate_generation_staging import (
    CandidateGenerationInfrastructureError,
    CandidateGenerationInvalidError,
    VerifiedProjectionCandidate,
    stage_candidate_generation,
    verify_candidate_generation,
)
from .integrity import (
    all_generated_files,
    projection_tree_digest,
)


REPORT_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3C2_SANDBOX_REPORT_V0_1"
)
BLOCKED_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3C2_SANDBOX_BLOCKED_V0_1"
)
FAIL_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3C2_SANDBOX_FAIL_V0_1"
)

_REQUIRED_MUTATIONS = (
    "PAYLOAD_BYTE_MUTATION",
    "PAYLOAD_FILE_DELETION",
    "UNMANIFESTED_EXTRA_FILE",
    "PAYLOAD_MANIFEST_MUTATION",
    "GENERATION_MANIFEST_MUTATION",
    "SEAL_MUTATION",
    "HARD_LINK_ALIAS",
)


class SandboxQualificationError(RuntimeError):
    pass


def _sha(label: str) -> str:
    return hashlib.sha256(
        label.encode("utf-8")
    ).hexdigest()


def _canonical_file(value: object) -> bytes:
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


def _write_fixture_file(
    path: Path,
    data: bytes,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    with path.open("xb") as handle:
        handle.write(data)


def _build_projection_fixture(root: Path) -> None:
    root.mkdir()
    _write_fixture_file(
        root / "generated" / "artifacts" / "alpha.md",
        b"# Alpha\n",
    )
    _write_fixture_file(
        root
        / "generated"
        / "artifacts"
        / "nested"
        / "beta.json",
        b'{"beta":2}\n',
    )
    _write_fixture_file(
        root / "generated" / "relations" / "edges.json",
        b'{"edges":[]}\n',
    )
    _write_fixture_file(
        root
        / "generated"
        / "manifests"
        / "build-manifest.json",
        (
            b'{"schema":'
            b'"P5D3C2_SANDBOX_PACKAGER_INPUT"}\n'
        ),
    )


def _candidate(
    projection_root: Path,
) -> VerifiedProjectionCandidate:
    return VerifiedProjectionCandidate(
        repository=(
            "thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM"
        ),
        branch="integration/system-v1",
        candidate_head="1" * 40,
        candidate_tree="2" * 40,
        dynamic_inventory_digest_sha256=_sha(
            "p5d3c2-sandbox-dynamic-inventory"
        ),
        semantic_bridge_digest_sha256=_sha(
            "p5d3c2-sandbox-semantic-bridge"
        ),
        semantic_record_digest_sha256=_sha(
            "p5d3c2-sandbox-semantic-records"
        ),
        projection_contract_version=(
            "P5D3C2_SANDBOX_PACKAGER_INPUT_V0_1"
        ),
        projection_tree_digest_sha256=(
            projection_tree_digest(
                projection_root
            )
        ),
        generated_file_count=len(
            all_generated_files(
                projection_root
            )
        ),
        breaker_status="PASS",
        determinism_status="PASS",
        breaker_manifest_digest_sha256=_sha(
            "p5d3c2-sandbox-breaker-manifest"
        ),
        breaker_result_digest_sha256=_sha(
            "p5d3c2-sandbox-breaker-result"
        ),
        determinism_evidence_digest_sha256=_sha(
            "p5d3c2-sandbox-determinism-evidence"
        ),
    )


def _package_content_digest(root: Path) -> str:
    rows: list[list[object]] = []
    for path in sorted(
        (
            item
            for item in root.rglob("*")
            if item.is_file()
        ),
        key=lambda item:
            item.relative_to(root).as_posix().encode(
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
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


def _copy_package(
    source: Path,
    destination: Path,
) -> None:
    shutil.copytree(
        source,
        destination,
        symlinks=False,
    )


def _expect_invalid(
    control_package: Path,
    mutation_root: Path,
    mutate: Callable[[Path], None],
) -> None:
    _copy_package(
        control_package,
        mutation_root,
    )
    mutate(mutation_root)

    try:
        verify_candidate_generation(
            mutation_root
        )
    except CandidateGenerationInvalidError:
        return
    except CandidateGenerationInfrastructureError as exc:
        raise SandboxQualificationError(
            "mutation breaker blocked by infrastructure: "
            f"{exc}"
        ) from exc

    raise SandboxQualificationError(
        "mutation survived verifier"
    )


def _mutate_payload_bytes(root: Path) -> None:
    path = (
        root
        / "generated"
        / "artifacts"
        / "alpha.md"
    )
    path.write_bytes(b"# MUTATED\n")


def _delete_payload_file(root: Path) -> None:
    (
        root
        / "generated"
        / "artifacts"
        / "alpha.md"
    ).unlink()


def _add_unmanifested_file(root: Path) -> None:
    path = (
        root
        / "generated"
        / "artifacts"
        / "extra.md"
    )
    with path.open("xb") as handle:
        handle.write(b"extra\n")


def _mutate_payload_manifest(root: Path) -> None:
    path = (
        root
        / "_atds_generation"
        / "payload-manifest.json"
    )
    value = json.loads(
        path.read_text(encoding="utf-8")
    )
    value["file_count"] += 1
    path.write_bytes(
        _canonical_file(value)
    )


def _mutate_generation_manifest(root: Path) -> None:
    path = (
        root
        / "_atds_generation"
        / "generation-manifest.json"
    )
    value = json.loads(
        path.read_text(encoding="utf-8")
    )
    value["determinism_status"] = "FAIL"
    path.write_bytes(
        _canonical_file(value)
    )


def _mutate_seal(root: Path) -> None:
    path = (
        root
        / "_atds_generation"
        / "SEAL.json"
    )
    value = json.loads(
        path.read_text(encoding="utf-8")
    )
    value["seal_status"] = "SEALED_TAMPERED"
    path.write_bytes(
        _canonical_file(value)
    )


def _hard_link_alias(root: Path) -> None:
    first = (
        root
        / "generated"
        / "artifacts"
        / "alpha.md"
    )
    second = (
        root
        / "generated"
        / "artifacts"
        / "nested"
        / "beta.json"
    )
    second.unlink()
    try:
        os.link(first, second)
    except OSError as exc:
        raise CandidateGenerationInfrastructureError(
            f"hard-link capability unavailable: {exc}"
        ) from exc


def _reparse_probe(
    control_package: Path,
    mutation_root: Path,
) -> str:
    _copy_package(
        control_package,
        mutation_root,
    )
    target = (
        mutation_root
        / "generated"
        / "artifacts"
        / "alpha.md"
    )
    link = (
        mutation_root
        / "generated"
        / "artifacts"
        / "nested"
        / "beta.json"
    )
    link.unlink()

    try:
        os.symlink(
            os.path.relpath(
                target,
                link.parent,
            ),
            link,
            target_is_directory=False,
        )
    except (OSError, NotImplementedError):
        return "CAPABILITY_UNAVAILABLE"

    try:
        verify_candidate_generation(
            mutation_root
        )
    except CandidateGenerationInvalidError:
        return "REJECTED_AS_INVALID"
    except CandidateGenerationInfrastructureError:
        return "BLOCKED_UNEXPECTED"

    return "BREAKER_SURVIVED"


def run_sandbox_qualification(
    *,
    forbidden_roots: tuple[Path, ...] = (),
) -> dict[str, object]:
    with tempfile.TemporaryDirectory(
        prefix="atds-p5d3c2-sandbox-"
    ) as temp:
        sandbox = Path(temp)
        projection = sandbox / "verified-projection"
        control = sandbox / "control-package"

        _build_projection_fixture(
            projection
        )
        candidate = _candidate(
            projection
        )

        descriptor = stage_candidate_generation(
            candidate,
            verified_projection_root=projection,
            package_root=control,
            forbidden_roots=forbidden_roots,
        )

        before_verify = _package_content_digest(
            control
        )
        first = verify_candidate_generation(
            control,
            expected_candidate=candidate,
            forbidden_roots=forbidden_roots,
        )
        between_verify = _package_content_digest(
            control
        )
        second = verify_candidate_generation(
            control,
            expected_candidate=candidate,
            forbidden_roots=forbidden_roots,
        )
        after_verify = _package_content_digest(
            control
        )

        if descriptor != first or first != second:
            raise SandboxQualificationError(
                "control verification descriptors differ"
            )

        repeat_equal = True
        content_unchanged = (
            before_verify
            == between_verify
            == after_verify
        )
        if not content_unchanged:
            raise SandboxQualificationError(
                "verifier mutated control package"
            )

        mutations: tuple[
            tuple[str, Callable[[Path], None]],
            ...
        ] = (
            (
                "PAYLOAD_BYTE_MUTATION",
                _mutate_payload_bytes,
            ),
            (
                "PAYLOAD_FILE_DELETION",
                _delete_payload_file,
            ),
            (
                "UNMANIFESTED_EXTRA_FILE",
                _add_unmanifested_file,
            ),
            (
                "PAYLOAD_MANIFEST_MUTATION",
                _mutate_payload_manifest,
            ),
            (
                "GENERATION_MANIFEST_MUTATION",
                _mutate_generation_manifest,
            ),
            (
                "SEAL_MUTATION",
                _mutate_seal,
            ),
            (
                "HARD_LINK_ALIAS",
                _hard_link_alias,
            ),
        )

        passed: list[str] = []
        for index, (
            name,
            mutator,
        ) in enumerate(mutations):
            mutation_root = (
                sandbox
                / f"mutation-{index:02d}"
            )
            _expect_invalid(
                control,
                mutation_root,
                mutator,
            )
            passed.append(name)

        if tuple(passed) != _REQUIRED_MUTATIONS:
            raise SandboxQualificationError(
                "required mutation registry mismatch"
            )

        reparse_status = _reparse_probe(
            control,
            sandbox / "mutation-reparse",
        )
        if reparse_status in {
            "BREAKER_SURVIVED",
            "BLOCKED_UNEXPECTED",
        }:
            raise SandboxQualificationError(
                "reparse/symlink breaker did not pass"
            )

        final_descriptor = (
            verify_candidate_generation(
                control,
                expected_candidate=candidate,
                forbidden_roots=forbidden_roots,
            )
        )
        if final_descriptor != descriptor:
            raise SandboxQualificationError(
                "control package changed after mutation copies"
            )

        return {
            "schema": REPORT_SCHEMA,
            "status":
                "PASS_SANDBOX_SEALED_UNPROMOTED",
            "package_verification_status":
                descriptor["verification_status"],
            "generation_id":
                descriptor["generation_id"],
            "candidate_generation_digest_sha256":
                descriptor[
                    "candidate_generation_digest_sha256"
                ],
            "payload_file_count":
                descriptor["payload_file_count"],
            "payload_file_map_digest_sha256":
                descriptor[
                    "payload_file_map_digest_sha256"
                ],
            "control_verify_repeat_equal":
                repeat_equal,
            "control_content_digest_unchanged":
                content_unchanged,
            "required_mutation_breakers_passed":
                passed,
            "required_mutation_breaker_count":
                len(passed),
            "reparse_probe_status":
                reparse_status,
            "real_vault_modified": False,
            "current_pointer_created": False,
            "production_promotion_authorized":
                False,
            "sandbox_retained": False,
        }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "P5-D3C2 sacrificial candidate-generation "
            "staging qualification."
        )
    )
    parser.add_argument(
        "--forbidden-root",
        action="append",
        default=[],
        help=(
            "Host path that staging must not intersect. "
            "May be repeated."
        ),
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    forbidden = tuple(
        Path(item)
        for item in args.forbidden_root
    )

    try:
        report = run_sandbox_qualification(
            forbidden_roots=forbidden,
        )
    except (
        CandidateGenerationInfrastructureError,
        OSError,
    ) as exc:
        print(
            json.dumps(
                {
                    "schema": BLOCKED_SCHEMA,
                    "status":
                        "BLOCKED_SANDBOX_INFRASTRUCTURE",
                    "error_type":
                        type(exc).__name__,
                    "error_message": str(exc),
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 2
    except (
        CandidateGenerationInvalidError,
        SandboxQualificationError,
    ) as exc:
        print(
            json.dumps(
                {
                    "schema": FAIL_SCHEMA,
                    "status": "FAIL",
                    "error_type":
                        type(exc).__name__,
                    "error_message": str(exc),
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    print(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
