from pathlib import Path


DURABLE_BOUNDARY_WORKFLOWS = (
    Path('.github/workflows/data-to-context.yml'),
    Path('.github/workflows/context-to-research-boundary.yml'),
    Path('.github/workflows/research-findings-contract.yml'),
    Path('.github/workflows/research-to-decision-boundary.yml'),
)


def test_durable_boundary_workflows_are_branch_neutral_and_pr_covered() -> None:
    for path in DURABLE_BOUNDARY_WORKFLOWS:
        text = path.read_text(encoding='utf-8')
        assert '\n    branches:' not in text, path
        assert 'feat/' not in text, path
        assert '\n  push:' in text, path
        assert '\n  pull_request:' in text, path
        assert text.count('\n    paths:') >= 2, path
        assert '\n  workflow_dispatch:' in text, path
        assert '\npermissions:\n  contents: read\n' in text, path
