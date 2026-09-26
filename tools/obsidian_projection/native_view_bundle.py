from __future__ import annotations

import hashlib
import json
import os
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence


class NativeViewBundleError(RuntimeError):
    pass


P4A_CONTRACT_SCHEMA = "ATDS_OBSIDIAN_HUMAN_NAVIGATION_CONTRACT_V0_1"
P4A_CONTRACT_BLOB = "699cbaf60141d8ecbb4f7f1afad214b6dd51f92b"
VIEW_SCHEMA = "ATDS_OBSIDIAN_VIEW_V0_1"
EXPECTED_VAULT = (
    r"C:\Users\Boulevart\OneDrive\Bureau\ATDS"
    r"\ATDS-OBSIDIAN-PROJECTION"
)
EXPECTED_GENERATED_COUNT = 92
EXPECTED_TREE_DIGEST = (
    "bf67fb65d42de58f394a21a884ca180665b3ba550be101ac2d410b0aa425e2e0"
)
VIEW_PATHS = (
    "views/HOME.md",
    "views/dashboards/PROJECT-SNAPSHOT.md",
    "views/dashboards/QUALIFICATION-STATUS.md",
    "views/maps/SYSTEM-ARCHITECTURE.md",
    "views/maps/GOVERNANCE.md",
    "views/maps/RESEARCH-LIFECYCLE.md",
    "views/canvas/ATDS-OVERVIEW.canvas",
)


def _git_blob_oid(raw: bytes) -> str:
    return hashlib.sha1(
        f"blob {len(raw)}\0".encode("ascii") + raw
    ).hexdigest()


def _canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def verify_p4a_contract(package_dir: Path) -> dict[str, Any]:
    path = package_dir / "human_navigation_contract_v0_1.json"
    try:
        raw = path.read_bytes()
        contract = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise NativeViewBundleError(
            "P4-A contract unreadable"
        ) from exc

    if _git_blob_oid(raw) != P4A_CONTRACT_BLOB:
        raise NativeViewBundleError(
            "P4-A contract blob mismatch"
        )
    if contract.get("schema") != P4A_CONTRACT_SCHEMA:
        raise NativeViewBundleError(
            "unexpected P4-A contract schema"
        )

    p4b = contract.get("p4b_candidate_boundary")
    if not isinstance(p4b, dict):
        raise NativeViewBundleError(
            "P4-B boundary missing"
        )

    required = (
        "may_read_generated_projection",
        "may_read_build_manifest",
        "may_read_integrity_manifest",
        "may_write_only_views",
        "may_write_only_if_views_empty",
        "may_not_modify_generated",
        "may_not_modify_obsidian_config",
        "may_not_enable_plugins_or_sync",
        "must_verify_projection_digest_before_write",
        "must_verify_written_bundle_after_write",
        "must_leave_repository_state_unchanged",
    )
    for field in required:
        if p4b.get(field) is not True:
            raise NativeViewBundleError(
                f"P4-B boundary not authorized: {field}"
            )

    return contract


def _parse_frontmatter(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise NativeViewBundleError(
            f"cannot read projection record: {path}"
        ) from exc

    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise NativeViewBundleError(
            f"frontmatter missing: {path}"
        )
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise NativeViewBundleError(
            f"frontmatter terminator missing: {path}"
        ) from exc

    result: dict[str, Any] = {}
    for line in lines[1:end]:
        if ": " not in line:
            raise NativeViewBundleError(
                f"invalid frontmatter line: {path}"
            )
        key, encoded = line.split(": ", 1)
        if key in result:
            raise NativeViewBundleError(
                f"duplicate frontmatter key: {path}"
            )
        try:
            result[key] = json.loads(encoded)
        except json.JSONDecodeError as exc:
            raise NativeViewBundleError(
                f"invalid frontmatter value: {path}: {key}"
            ) from exc
    return result


def load_projection_records(
    vault: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    artifact_dir = vault / "generated" / "artifacts"
    relation_dir = vault / "generated" / "relations"

    if not artifact_dir.is_dir():
        raise NativeViewBundleError(
            "generated/artifacts missing"
        )
    if not relation_dir.is_dir():
        raise NativeViewBundleError(
            "generated/relations missing"
        )

    artifacts: list[dict[str, Any]] = []
    for path in sorted(
        artifact_dir.glob("*.md"),
        key=lambda item: item.name.encode("utf-8"),
    ):
        fm = _parse_frontmatter(path)
        if fm.get("record_schema") != "ATDS_OBSIDIAN_ARTIFACT_V0_1":
            raise NativeViewBundleError(
                f"unexpected artifact schema: {path.name}"
            )
        if fm.get("record_type") != "ARTIFACT":
            raise NativeViewBundleError(
                f"unexpected artifact type: {path.name}"
            )
        if fm.get("projection_authority_role") != "DERIVED":
            raise NativeViewBundleError(
                f"artifact authority drift: {path.name}"
            )
        if fm.get("projection_integrity") != "CLEAN":
            raise NativeViewBundleError(
                f"artifact integrity drift: {path.name}"
            )
        artifacts.append(fm)

    relations: list[dict[str, Any]] = []
    for path in sorted(
        relation_dir.glob("*.md"),
        key=lambda item: item.name.encode("utf-8"),
    ):
        fm = _parse_frontmatter(path)
        if fm.get("record_schema") != "ATDS_OBSIDIAN_RELATION_V0_1":
            raise NativeViewBundleError(
                f"unexpected relation schema: {path.name}"
            )
        if fm.get("record_type") != "RELATION":
            raise NativeViewBundleError(
                f"unexpected relation record type: {path.name}"
            )
        if fm.get("projection_authority_role") != "DERIVED":
            raise NativeViewBundleError(
                f"relation authority drift: {path.name}"
            )
        if fm.get("projection_integrity") != "CLEAN":
            raise NativeViewBundleError(
                f"relation integrity drift: {path.name}"
            )
        relations.append(fm)

    if not artifacts:
        raise NativeViewBundleError(
            "projection contains no artifacts"
        )

    artifact_ids = {
        str(item["projection_record_id"])
        for item in artifacts
    }
    if len(artifact_ids) != len(artifacts):
        raise NativeViewBundleError(
            "duplicate projection artifact IDs"
        )

    for relation in relations:
        if str(relation["source_record_id"]) not in artifact_ids:
            raise NativeViewBundleError(
                "relation source outside artifact set"
            )
        if str(relation["target_record_id"]) not in artifact_ids:
            raise NativeViewBundleError(
                "relation target outside artifact set"
            )

    commits = {
        str(item["source_commit"])
        for item in artifacts
    }
    if len(commits) != 1:
        raise NativeViewBundleError(
            "mixed projection source commits"
        )

    return artifacts, relations


def _frontmatter(
    *,
    view_id: str,
    view_role: str,
    source_commit: str,
) -> bytes:
    fields = (
        ("view_schema", VIEW_SCHEMA),
        ("view_contract_schema", P4A_CONTRACT_SCHEMA),
        ("view_id", view_id),
        ("view_role", view_role),
        ("authority_role", "VIEW"),
        ("semantic_authority", "NONE"),
        ("projection_tree_digest_sha256", EXPECTED_TREE_DIGEST),
        ("projection_source_commit", source_commit),
        ("projection_freshness", "BOUND"),
    )

    lines = ["---"]
    for key, value in fields:
        lines.append(
            f"{key}: "
            + json.dumps(
                value,
                ensure_ascii=False,
                separators=(",", ":"),
            )
        )
    lines.extend(["---", ""])
    return "\n".join(lines).encode("utf-8")


def _artifact_link(item: Mapping[str, Any]) -> str:
    record_id = str(item["projection_record_id"])
    source_path = str(item["source_path"]).replace("]", "")
    return (
        f"[[generated/artifacts/{record_id}|"
        f"{source_path}]]"
    )


def _count_rows(
    artifacts: Sequence[Mapping[str, Any]],
    field: str,
) -> list[tuple[str, int]]:
    counts = Counter(
        str(item.get(field, "UNKNOWN"))
        for item in artifacts
    )
    return sorted(
        counts.items(),
        key=lambda item: item[0].encode("utf-8"),
    )


def _table(rows: Sequence[tuple[str, int]]) -> str:
    lines = [
        "| Valeur | Nombre |",
        "|---|---:|",
    ]
    for value, count in rows:
        lines.append(
            f"| {value.replace('|', '/')} | {count} |"
        )
    return "\n".join(lines)


def _group_links(
    artifacts: Sequence[Mapping[str, Any]],
    field: str,
) -> str:
    groups: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for item in artifacts:
        groups[str(item.get(field, "UNKNOWN"))].append(item)

    lines: list[str] = []
    for value in sorted(
        groups,
        key=lambda item: item.encode("utf-8"),
    ):
        lines.append(f"### {value}")
        for item in sorted(
            groups[value],
            key=lambda row:
                str(row["source_path"]).encode("utf-8"),
        ):
            lines.append(f"- {_artifact_link(item)}")
        lines.append("")
    return "\n".join(lines).rstrip()


def _render_home(source_commit: str) -> bytes:
    body = f"""# ATDS — Navigation

> Vue non autoritative. La vérité canonique reste GitHub / ATDS.

## Projection liée

- Source commit : {source_commit}
- Projection digest : {EXPECTED_TREE_DIGEST}
- Fraîcheur : BOUND

## Tableaux de bord

- [[views/dashboards/PROJECT-SNAPSHOT|Project Snapshot]]
- [[views/dashboards/QUALIFICATION-STATUS|Qualification Status]]

## Cartes

- [[views/maps/SYSTEM-ARCHITECTURE|System Architecture]]
- [[views/maps/GOVERNANCE|Governance]]
- [[views/maps/RESEARCH-LIFECYCLE|Research Lifecycle]]

## Vue visuelle

- [[views/canvas/ATDS-OVERVIEW.canvas|ATDS Overview Canvas]]

## Frontière d’autorité

- GitHub / ATDS = vérité canonique
- generated/ = projection déterministe dérivée
- views/ = navigation humaine non autoritative

Les wikilinks, backlinks et connexions Canvas servent à naviguer. Ils ne créent pas de relation sémantique qualifiée.
"""
    return (
        _frontmatter(
            view_id="HOME",
            view_role="ENTRY_POINT",
            source_commit=source_commit,
        )
        + body.encode("utf-8")
    )


def _render_project_snapshot(
    artifacts: Sequence[Mapping[str, Any]],
    relations: Sequence[Mapping[str, Any]],
    source_commit: str,
) -> bytes:
    dimensions = (
        ("artifact_family", "Familles d’artefacts"),
        ("semantic_role", "Rôles sémantiques"),
        ("procedure_role", "Rôles procéduraux"),
        ("source_authority_role", "Autorité source"),
        ("epistemic_role", "Rôles épistémiques"),
        ("temporal_role", "Rôles temporels"),
        ("persistence_state", "États de persistance"),
    )

    lines = [
        "# Project Snapshot",
        "",
        "> Snapshot descriptif lié à une projection déterministe. Ce tableau de bord n’est pas une autorité de qualification.",
        "",
        "## Identité",
        "",
        f"- Source commit : {source_commit}",
        f"- Projection digest : {EXPECTED_TREE_DIGEST}",
        f"- Fichiers generated/ : {EXPECTED_GENERATED_COUNT}",
        f"- Artefacts projetés : {len(artifacts)}",
        f"- Relations projetées : {len(relations)}",
        "",
    ]

    for field, title in dimensions:
        lines.extend(
            [
                f"## {title}",
                "",
                _table(_count_rows(artifacts, field)),
                "",
            ]
        )

    return (
        _frontmatter(
            view_id="PROJECT-SNAPSHOT",
            view_role="FACTUAL_SNAPSHOT_DASHBOARD",
            source_commit=source_commit,
        )
        + ("\n".join(lines).rstrip() + "\n").encode("utf-8")
    )


def _render_qualification(
    artifacts: Sequence[Mapping[str, Any]],
    source_commit: str,
) -> bytes:
    lines = [
        "# Qualification Status",
        "",
        "> qualification_status et scientific_status restent distincts. Aucun score synthétique n’est calculé.",
        "",
        "## Distribution — qualification",
        "",
        _table(_count_rows(artifacts, "qualification_status")),
        "",
        "## Distribution — statut scientifique",
        "",
        _table(_count_rows(artifacts, "scientific_status")),
        "",
        "## Artefacts par qualification",
        "",
        _group_links(artifacts, "qualification_status"),
        "",
        "## Règle de lecture",
        "",
        "PASS conserve sa portée locale. BLOCKED n’est pas converti en FAIL. UNKNOWN reste visible.",
        "",
    ]

    return (
        _frontmatter(
            view_id="QUALIFICATION-STATUS",
            view_role="QUALIFICATION_NAVIGATION_DASHBOARD",
            source_commit=source_commit,
        )
        + ("\n".join(lines).rstrip() + "\n").encode("utf-8")
    )


def _render_architecture(
    artifacts: Sequence[Mapping[str, Any]],
    source_commit: str,
) -> bytes:
    lines = [
        "# System Architecture",
        "",
        "> Carte de navigation et de frontière d’autorité. Les flèches ci-dessous ne constituent pas des relations sémantiques qualifiées.",
        "",
        "~~~mermaid",
        "flowchart LR",
        '  A["GitHub / ATDS<br/>CANONICAL"] --> B["generated/<br/>DERIVED · MACHINE"]',
        '  B --> C["views/<br/>VIEW · HUMAN · NON-AUTHORITATIVE"]',
        '  C --> D["Obsidian<br/>OBSERVE · NAVIGATE · VISUALIZE"]',
        "~~~",
        "",
        "## Artefacts par famille",
        "",
        _group_links(artifacts, "artifact_family"),
        "",
    ]

    return (
        _frontmatter(
            view_id="SYSTEM-ARCHITECTURE",
            view_role="ARCHITECTURE_MAP",
            source_commit=source_commit,
        )
        + ("\n".join(lines).rstrip() + "\n").encode("utf-8")
    )


def _render_governance(
    artifacts: Sequence[Mapping[str, Any]],
    source_commit: str,
) -> bytes:
    governance = [
        item
        for item in artifacts
        if str(item["source_path"]).startswith("GOVERNANCE/")
    ]

    lines = [
        "# Governance",
        "",
        "> Navigation vers les artefacts de gouvernance projetés. Cette page ne remplace pas leurs sources GitHub.",
        "",
        "~~~mermaid",
        "flowchart TD",
        '  A["GitHub / ATDS"] --> B["Source authority"]',
        '  B --> C["Derived projection"]',
        '  C --> D["Human views"]',
        '  D -. "no authority promotion" .-> C',
        "~~~",
        "",
        "## Artefacts de gouvernance",
        "",
    ]

    if governance:
        for item in sorted(
            governance,
            key=lambda row:
                str(row["source_path"]).encode("utf-8"),
        ):
            lines.append(f"- {_artifact_link(item)}")
    else:
        lines.append(
            "- UNKNOWN — aucun artefact GOVERNANCE/ n’est présent dans le périmètre projeté."
        )

    lines.extend(
        [
            "",
            "## Principes de lecture",
            "",
            "- CANONICAL ≠ QUALIFIED",
            "- PASS reste scoped",
            "- PASS ≠ SUPPORTED",
            "- succès d’exécution ≠ PASS gouverné",
            "- vue Obsidian ≠ autorité",
            "",
        ]
    )

    return (
        _frontmatter(
            view_id="GOVERNANCE",
            view_role="GOVERNANCE_MAP",
            source_commit=source_commit,
        )
        + ("\n".join(lines).rstrip() + "\n").encode("utf-8")
    )


def _render_research(
    artifacts: Sequence[Mapping[str, Any]],
    relations: Sequence[Mapping[str, Any]],
    source_commit: str,
) -> bytes:
    relation_counts = Counter(
        str(item["relation_type"])
        for item in relations
    )

    lines = [
        "# Research Lifecycle",
        "",
        "> Carte descriptive du périmètre projeté. Les seules relations sémantiques affichées comme telles proviennent de generated/relations/.",
        "",
        "## Rôles sémantiques",
        "",
        _table(_count_rows(artifacts, "semantic_role")),
        "",
        "## Rôles procéduraux",
        "",
        _table(_count_rows(artifacts, "procedure_role")),
        "",
        "## Relations qualifiées projetées",
        "",
        _table(
            sorted(
                relation_counts.items(),
                key=lambda item:
                    item[0].encode("utf-8"),
            )
        ),
        "",
        "## Navigation par rôle sémantique",
        "",
        _group_links(artifacts, "semantic_role"),
        "",
    ]

    return (
        _frontmatter(
            view_id="RESEARCH-LIFECYCLE",
            view_role="RESEARCH_NAVIGATION_MAP",
            source_commit=source_commit,
        )
        + ("\n".join(lines).rstrip() + "\n").encode("utf-8")
    )


def _stable_id(value: str) -> str:
    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()[:16]


def _render_canvas() -> bytes:
    specs = (
        ("home", "views/HOME.md", 0, 0, 340, 220),
        ("snapshot", "views/dashboards/PROJECT-SNAPSHOT.md", 520, -260, 360, 240),
        ("qualification", "views/dashboards/QUALIFICATION-STATUS.md", 520, 40, 360, 240),
        ("architecture", "views/maps/SYSTEM-ARCHITECTURE.md", -520, -320, 360, 240),
        ("governance", "views/maps/GOVERNANCE.md", -520, -20, 360, 240),
        ("research", "views/maps/RESEARCH-LIFECYCLE.md", -520, 280, 360, 240),
    )

    nodes = [
        {
            "id": _stable_id(f"node:{label}"),
            "type": "file",
            "file": file,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
        }
        for label, file, x, y, width, height in specs
    ]

    home_id = _stable_id("node:home")
    edges = [
        {
            "id": _stable_id(f"edge:home:{label}"),
            "fromNode": home_id,
            "toNode": _stable_id(f"node:{label}"),
        }
        for label, *_rest in specs[1:]
    ]

    return _canonical_json_bytes(
        {
            "nodes": nodes,
            "edges": edges,
        }
    )


def build_view_bundle(
    vault: Path,
) -> dict[str, bytes]:
    artifacts, relations = load_projection_records(vault)
    source_commit = str(artifacts[0]["source_commit"])

    bundle = {
        "views/HOME.md": _render_home(source_commit),
        "views/dashboards/PROJECT-SNAPSHOT.md":
            _render_project_snapshot(
                artifacts,
                relations,
                source_commit,
            ),
        "views/dashboards/QUALIFICATION-STATUS.md":
            _render_qualification(
                artifacts,
                source_commit,
            ),
        "views/maps/SYSTEM-ARCHITECTURE.md":
            _render_architecture(
                artifacts,
                source_commit,
            ),
        "views/maps/GOVERNANCE.md":
            _render_governance(
                artifacts,
                source_commit,
            ),
        "views/maps/RESEARCH-LIFECYCLE.md":
            _render_research(
                artifacts,
                relations,
                source_commit,
            ),
        "views/canvas/ATDS-OVERVIEW.canvas":
            _render_canvas(),
    }

    if tuple(bundle.keys()) != VIEW_PATHS:
        raise NativeViewBundleError(
            "view bundle path/order drift"
        )

    for relative, raw in bundle.items():
        if not raw.endswith(b"\n"):
            raise NativeViewBundleError(
                f"view must end with LF: {relative}"
            )
        if b"\r" in raw:
            raise NativeViewBundleError(
                f"CR/CRLF forbidden: {relative}"
            )
        if raw.startswith(b"\xef\xbb\xbf"):
            raise NativeViewBundleError(
                f"UTF-8 BOM forbidden: {relative}"
            )

    return bundle


def bundle_manifest(
    bundle: Mapping[str, bytes],
) -> dict[str, dict[str, Any]]:
    return {
        relative: {
            "size_bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        }
        for relative, raw in sorted(
            bundle.items(),
            key=lambda item: item[0].encode("utf-8"),
        )
    }


def _tree_digest(root: Path) -> str:
    if not root.exists():
        return hashlib.sha256(b"[]\n").hexdigest()
    if not root.is_dir():
        raise NativeViewBundleError(
            f"tree root is not a directory: {root}"
        )

    entries: list[list[Any]] = []
    for current, directories, files in os.walk(
        root,
        topdown=True,
        followlinks=False,
    ):
        directories.sort(key=lambda x: x.encode("utf-8"))
        files.sort(key=lambda x: x.encode("utf-8"))
        current_path = Path(current)

        for name in files:
            path = current_path / name
            raw = path.read_bytes()
            entries.append(
                [
                    path.relative_to(root).as_posix(),
                    hashlib.sha256(raw).hexdigest(),
                    len(raw),
                ]
            )

    return hashlib.sha256(
        _canonical_json_bytes(entries)
    ).hexdigest()


def _repo_state(repo_root: Path) -> dict[str, str]:
    def git(*args: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            env={
                **os.environ,
                "GIT_OPTIONAL_LOCKS": "0",
            },
        )
        if completed.returncode != 0:
            raise NativeViewBundleError(
                "git command failed: "
                + completed.stderr.decode(
                    "utf-8",
                    errors="replace",
                ).strip()
            )
        return completed.stdout.decode(
            "utf-8",
            errors="strict",
        ).rstrip("\r\n")

    return {
        "branch": git("branch", "--show-current"),
        "head": git("rev-parse", "HEAD"),
        "status_porcelain": git("status", "--porcelain"),
    }


def _exclusive_seed_views(
    views: Path,
    bundle: Mapping[str, bytes],
) -> None:
    if not views.exists() or not views.is_dir():
        raise NativeViewBundleError(
            "views directory missing"
        )
    if list(views.iterdir()):
        raise NativeViewBundleError(
            "views must be empty before initial seed"
        )

    directories = sorted(
        {
            (views.parent / Path(relative)).parent
            for relative in bundle
        },
        key=lambda item:
            (len(item.parts), str(item).encode("utf-8")),
    )

    for directory in directories:
        if directory == views:
            continue
        directory.mkdir(exist_ok=False)

    for relative in VIEW_PATHS:
        target = views.parent / Path(relative)
        try:
            with target.open("xb") as handle:
                handle.write(bundle[relative])
        except OSError as exc:
            raise NativeViewBundleError(
                f"exclusive view write failed: {relative}"
            ) from exc


def _verify_seeded_bundle(
    vault: Path,
    bundle: Mapping[str, bytes],
) -> dict[str, dict[str, Any]]:
    views = vault / "views"
    actual_paths: list[str] = []

    for current, directories, files in os.walk(
        views,
        topdown=True,
        followlinks=False,
    ):
        directories.sort(key=lambda x: x.encode("utf-8"))
        files.sort(key=lambda x: x.encode("utf-8"))
        current_path = Path(current)

        for name in files:
            actual_paths.append(
                (current_path / name)
                .relative_to(vault)
                .as_posix()
            )

    if tuple(actual_paths) != VIEW_PATHS:
        raise NativeViewBundleError(
            "seeded view path set/order mismatch"
        )

    manifest: dict[str, dict[str, Any]] = {}
    for relative in VIEW_PATHS:
        actual = (vault / Path(relative)).read_bytes()
        expected = bundle[relative]

        if actual != expected:
            raise NativeViewBundleError(
                f"seeded view bytes mismatch: {relative}"
            )

        manifest[relative] = {
            "size_bytes": len(actual),
            "sha256": hashlib.sha256(actual).hexdigest(),
        }

    return manifest


def seed_native_views(
    *,
    repo_root: Path,
    vault: Path,
) -> dict[str, Any]:
    package_dir = Path(__file__).resolve().parent
    verify_p4a_contract(package_dir)

    if os.name != "nt":
        raise NativeViewBundleError(
            "P4-B real Vault seed requires Windows"
        )

    from .first_open_onedrive import (
        _assert_safe_directory,
        _file_native_state,
        _generated_state,
        _obsidian_running,
        _projection_tree_digest_from_map,
    )

    if str(vault) != EXPECTED_VAULT:
        raise NativeViewBundleError(
            "runtime Vault path mismatch"
        )
    if _obsidian_running():
        raise NativeViewBundleError(
            "Obsidian must be fully closed before P4-B seed"
        )

    views = vault / "views"
    obsidian = vault / ".obsidian"
    generated = vault / "generated"

    _assert_safe_directory(vault)
    _assert_safe_directory(views)
    _assert_safe_directory(generated)
    _assert_safe_directory(obsidian)

    if (vault / ".git").exists():
        raise NativeViewBundleError(
            ".git forbidden inside Vault"
        )

    repo_before = _repo_state(repo_root)
    generated_before, generated_summary_before = (
        _generated_state(vault)
    )

    if len(generated_before) != EXPECTED_GENERATED_COUNT:
        raise NativeViewBundleError(
            "generated file count mismatch"
        )
    if (
        _projection_tree_digest_from_map(
            generated_before
        )
        != EXPECTED_TREE_DIGEST
    ):
        raise NativeViewBundleError(
            "projection digest mismatch"
        )

    obsidian_before = _tree_digest(obsidian)
    bundle = build_view_bundle(vault)
    expected_manifest = bundle_manifest(bundle)

    _exclusive_seed_views(views, bundle)

    for relative in VIEW_PATHS:
        state = _file_native_state(
            vault / Path(relative)
        )
        if state["class"] not in (
            "NO_REPARSE_POINT",
            "IO_REPARSE_TAG_CLOUD_6",
        ):
            raise NativeViewBundleError(
                f"unexpected seeded view class: {relative}"
            )

    actual_manifest = _verify_seeded_bundle(
        vault,
        bundle,
    )
    if actual_manifest != expected_manifest:
        raise NativeViewBundleError(
            "view bundle manifest mismatch"
        )

    generated_after, generated_summary_after = (
        _generated_state(vault)
    )
    if generated_after != generated_before:
        raise NativeViewBundleError(
            "generated changed during P4-B seed"
        )
    if _tree_digest(obsidian) != obsidian_before:
        raise NativeViewBundleError(
            ".obsidian changed during P4-B seed"
        )
    if _repo_state(repo_root) != repo_before:
        raise NativeViewBundleError(
            "repository state changed during P4-B seed"
        )

    return {
        "schema":
            "ATDS_OBSIDIAN_P4B_NATIVE_VIEW_BUNDLE_REPORT_V0_1",
        "status": "PASS",
        "p4b_seed_qualified": True,
        "vault_resolved_path": str(vault),
        "view_file_count": len(VIEW_PATHS),
        "view_paths": list(VIEW_PATHS),
        "view_manifest": actual_manifest,
        "projection_tree_digest_sha256":
            EXPECTED_TREE_DIGEST,
        "projection_generated_file_count":
            EXPECTED_GENERATED_COUNT,
        "projection_reparse_policy_summary_before":
            generated_summary_before,
        "projection_reparse_policy_summary_after":
            generated_summary_after,
        "generated_modified": False,
        "obsidian_config_modified": False,
        "repository_state_preserved": True,
        "community_plugins_required": False,
        "obsidian_sync_required": False,
        "dataview_required": False,
        "native_canvas_created": True,
        "automatic_overwrite_authorized": False,
    }
