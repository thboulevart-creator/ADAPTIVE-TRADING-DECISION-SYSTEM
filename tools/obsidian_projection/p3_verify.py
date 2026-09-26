from __future__ import annotations

import argparse
import json
from pathlib import Path

from .materialize import materialize_once


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "P3-B one-shot real Vault materialization. "
            "This command writes only the bounded external "
            "Vault defined by the persisted P3 contract."
        )
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help=(
            "Path to the ATDS repository. "
            "No source-build or destination override exists."
        ),
    )
    parser.add_argument(
        "--materialize",
        action="store_true",
        help=(
            "Explicitly authorize the single bounded "
            "materialization attempt."
        ),
    )
    args = parser.parse_args()

    if not args.materialize:
        parser.error(
            "--materialize is required for the real "
            "P3-B materialization attempt"
        )

    report = materialize_once(
        Path(args.repo_root)
    )

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
