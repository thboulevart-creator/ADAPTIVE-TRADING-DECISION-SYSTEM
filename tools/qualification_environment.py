from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import re
import sys
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Mapping


# Neutral qualification trigger: final persisted-HEAD re-break after P1.1 counter-expertise adjudication.
ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "04-REFERENCE" / "QUALIFICATION-ENVIRONMENT-LOCK.json"
CONTRACT_PATH = ROOT / "04-REFERENCE" / "SYSTEM-REPRODUCIBILITY-CONTRACT.md"
EXPECTED_SCHEMA = "QUALIFICATION_ENVIRONMENT_LOCK_V1"
EXPECTED_SCOPE = "P0_2_TO_P0_6_QUALIFICATION"
_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
_REQUIREMENT_RE = re.compile(r"(?P<name>[A-Za-z0-9_.-]+)==(?P<version>[A-Za-z0-9_.+!-]+)\Z")


class QualificationEnvironmentError(ValueError):
    pass


@dataclass(frozen=True)
class EnvironmentSnapshot:
    implementation: str
    python_version: str
    system: str
    github_actions: bool
    runner_os: str | None
    runner_arch: str | None
    environment: Mapping[str, str | None]
    packages: Mapping[str, str | None]


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise QualificationEnvironmentError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _exact_object(label: str, value: object, expected: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise QualificationEnvironmentError(f"{label} must be a JSON object")
    actual = set(value)
    if actual != expected:
        raise QualificationEnvironmentError(
            f"{label} schema mismatch: missing={sorted(expected - actual)} unknown={sorted(actual - expected)}"
        )
    return value


def _require_string(label: str, value: object) -> str:
    if not isinstance(value, str) or not value:
        raise QualificationEnvironmentError(f"{label} must be a non-empty string")
    return value


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def parse_requirements_lock(path: str | Path) -> dict[str, str]:
    source = Path(path)
    try:
        text = source.read_text(encoding="utf-8")
    except OSError as exc:
        raise QualificationEnvironmentError(f"cannot read qualification requirements lock: {exc}") from exc
    packages: dict[str, str] = {}
    normalized_names: set[str] = set()
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            raise QualificationEnvironmentError(f"blank requirements line at {line_number}")
        match = _REQUIREMENT_RE.fullmatch(line)
        if match is None:
            raise QualificationEnvironmentError(
                f"qualification requirement must be exact name==version at line {line_number}: {line!r}"
            )
        name = match.group("name")
        version = match.group("version")
        normalized = name.lower().replace("_", "-")
        if normalized in normalized_names:
            raise QualificationEnvironmentError(f"duplicate qualification requirement: {name}")
        normalized_names.add(normalized)
        packages[name] = version
    if not packages:
        raise QualificationEnvironmentError("qualification requirements lock must not be empty")
    return packages


def validate_lock_document(document: object, *, root: str | Path = ROOT) -> dict[str, Any]:
    top = _exact_object(
        "lock",
        document,
        {
            "schema",
            "scope",
            "python",
            "platform",
            "actions",
            "requirements",
            "environment",
            "optional_excluded",
            "observed_not_authoritative",
        },
    )
    if top["schema"] != EXPECTED_SCHEMA:
        raise QualificationEnvironmentError("unsupported qualification environment lock schema")
    if top["scope"] != EXPECTED_SCOPE:
        raise QualificationEnvironmentError("qualification environment lock scope mismatch")

    python_lock = _exact_object("python", top["python"], {"implementation", "version"})
    _require_string("python.implementation", python_lock["implementation"])
    _require_string("python.version", python_lock["version"])

    platform_lock = _exact_object(
        "platform",
        top["platform"],
        {"system", "github_runner", "github_runner_os", "github_runner_arch"},
    )
    for name in platform_lock:
        _require_string(f"platform.{name}", platform_lock[name])

    actions = _exact_object("actions", top["actions"], {"checkout", "setup_python"})
    for name, value in actions.items():
        text = _require_string(f"actions.{name}", value)
        if re.fullmatch(r"[0-9a-f]{40}", text) is None:
            raise QualificationEnvironmentError(f"actions.{name} must be an immutable 40-hex commit")

    requirements = _exact_object("requirements", top["requirements"], {"path", "sha256", "packages"})
    requirement_path_text = _require_string("requirements.path", requirements["path"])
    expected_hash = _require_string("requirements.sha256", requirements["sha256"])
    if _SHA256_RE.fullmatch(expected_hash) is None:
        raise QualificationEnvironmentError("requirements.sha256 must be lowercase SHA-256")
    packages = requirements["packages"]
    if not isinstance(packages, dict) or not packages:
        raise QualificationEnvironmentError("requirements.packages must be a non-empty object")
    for name, version in packages.items():
        _require_string("requirements package name", name)
        _require_string(f"requirements.packages.{name}", version)

    environment = top["environment"]
    if not isinstance(environment, dict) or not environment:
        raise QualificationEnvironmentError("environment must be a non-empty object")
    for name, value in environment.items():
        _require_string("environment variable name", name)
        _require_string(f"environment.{name}", value)

    optional = _exact_object("optional_excluded", top["optional_excluded"], {"pyarrow"})
    pyarrow = _exact_object("optional_excluded.pyarrow", optional["pyarrow"], {"status", "reason"})
    if pyarrow["status"] != "BLOCKED_OUTSIDE_P0_6":
        raise QualificationEnvironmentError("pyarrow optional status must remain BLOCKED_OUTSIDE_P0_6")
    _require_string("optional_excluded.pyarrow.reason", pyarrow["reason"])
    if any(name.lower() == "pyarrow" for name in packages):
        raise QualificationEnvironmentError("pyarrow must not be silently promoted into the P0.6 qualification lock")

    observed = _exact_object(
        "observed_not_authoritative",
        top["observed_not_authoritative"],
        {"ubuntu_version", "runner_image_version", "runner_version"},
    )
    for name, value in observed.items():
        _require_string(f"observed_not_authoritative.{name}", value)

    root_path = Path(root)
    requirement_path = root_path / requirement_path_text
    try:
        raw = requirement_path.read_bytes()
    except OSError as exc:
        raise QualificationEnvironmentError(f"cannot read locked requirements bytes: {exc}") from exc
    actual_hash = _sha256_bytes(raw)
    if actual_hash != expected_hash:
        raise QualificationEnvironmentError(
            f"qualification requirements hash mismatch: expected={expected_hash} actual={actual_hash}"
        )
    parsed_packages = parse_requirements_lock(requirement_path)
    if parsed_packages != packages:
        raise QualificationEnvironmentError(
            f"requirements package map mismatch: file={parsed_packages!r} lock={packages!r}"
        )
    return top


def load_lock(path: str | Path = LOCK_PATH, *, root: str | Path = ROOT) -> dict[str, Any]:
    source = Path(path)
    try:
        raw = source.read_text(encoding="utf-8")
        document = json.loads(raw, object_pairs_hook=_strict_object)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise QualificationEnvironmentError(f"cannot parse qualification environment lock: {exc}") from exc
    return validate_lock_document(document, root=root)


def current_snapshot(lock: Mapping[str, Any]) -> EnvironmentSnapshot:
    package_versions: dict[str, str | None] = {}
    for name in lock["requirements"]["packages"]:
        try:
            package_versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            package_versions[name] = None
    environment = {name: os.environ.get(name) for name in lock["environment"]}
    github_actions = os.environ.get("GITHUB_ACTIONS", "").lower() == "true"
    return EnvironmentSnapshot(
        implementation=sys.implementation.name,
        python_version=platform.python_version(),
        system=platform.system(),
        github_actions=github_actions,
        runner_os=os.environ.get("RUNNER_OS"),
        runner_arch=os.environ.get("RUNNER_ARCH"),
        environment=environment,
        packages=package_versions,
    )


def verify_snapshot(lock: Mapping[str, Any], snapshot: EnvironmentSnapshot) -> None:
    errors: list[str] = []
    python_lock = lock["python"]
    platform_lock = lock["platform"]

    if snapshot.implementation != python_lock["implementation"]:
        errors.append(
            f"python implementation drift: expected={python_lock['implementation']} actual={snapshot.implementation}"
        )
    if snapshot.python_version != python_lock["version"]:
        errors.append(f"python version drift: expected={python_lock['version']} actual={snapshot.python_version}")
    if snapshot.system != platform_lock["system"]:
        errors.append(f"platform drift: expected={platform_lock['system']} actual={snapshot.system}")

    if snapshot.github_actions:
        if snapshot.runner_os != platform_lock["github_runner_os"]:
            errors.append(
                f"GitHub runner OS drift: expected={platform_lock['github_runner_os']} actual={snapshot.runner_os}"
            )
        if snapshot.runner_arch != platform_lock["github_runner_arch"]:
            errors.append(
                f"GitHub runner architecture drift: expected={platform_lock['github_runner_arch']} actual={snapshot.runner_arch}"
            )

    for name, expected in lock["environment"].items():
        actual = snapshot.environment.get(name)
        if actual != expected:
            errors.append(f"environment drift {name}: expected={expected!r} actual={actual!r}")

    for name, expected in lock["requirements"]["packages"].items():
        actual = snapshot.packages.get(name)
        if actual is None:
            errors.append(f"required qualification package missing: {name}=={expected}")
        elif actual != expected:
            errors.append(f"qualification package drift {name}: expected={expected} actual={actual}")

    if errors:
        raise QualificationEnvironmentError("; ".join(errors))


def verify_current_environment(
    lock_path: str | Path = LOCK_PATH,
    *,
    root: str | Path = ROOT,
) -> EnvironmentSnapshot:
    lock = load_lock(lock_path, root=root)
    snapshot = current_snapshot(lock)
    verify_snapshot(lock, snapshot)
    return snapshot


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args not in ([], ["verify"]):
        print("usage: python tools/qualification_environment.py [verify]", file=sys.stderr)
        return 2
    try:
        snapshot = verify_current_environment()
    except QualificationEnvironmentError as exc:
        print(f"VERDICT=FAIL\nREASON={exc}")
        return 1
    print(f"VERDICT=PASS\nCONTRACT={EXPECTED_SCHEMA}\nPYTHON={snapshot.python_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
