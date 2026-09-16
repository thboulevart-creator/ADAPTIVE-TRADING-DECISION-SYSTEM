from pathlib import Path


LOCK = Path('04-REFERENCE/QUALIFICATION-ENVIRONMENT-LOCK.json')
REQUIREMENTS = Path('requirements/qualification.lock.txt')
VERIFIER = Path('tools/qualification_environment.py')

PROTECTED_WORKFLOWS = (
    Path('.github/workflows/data-to-context.yml'),
    Path('.github/workflows/context-to-research-boundary.yml'),
    Path('.github/workflows/research-findings-contract.yml'),
    Path('.github/workflows/research-to-decision-boundary.yml'),
    Path('.github/workflows/p0-2-decision-block-integration-rebreak.yml'),
    Path('.github/workflows/p0-3-multi-year-integration-rebreak.yml'),
    Path('.github/workflows/p0-4-research-producer-junction.yml'),
    Path('.github/workflows/p0-5-research-interprocess-reattestation.yml'),
)


def test_pre_p06_authoritative_lock_must_exist() -> None:
    assert LOCK.is_file(), 'P0.6 requires one authoritative environment lock'
    assert REQUIREMENTS.is_file(), 'P0.6 requires one authoritative qualification requirements lock'
    assert VERIFIER.is_file(), 'P0.6 requires a fail-closed environment verifier'


def test_pre_p06_protected_workflows_must_not_float_environment() -> None:
    for path in PROTECTED_WORKFLOWS:
        text = path.read_text(encoding='utf-8')
        assert 'ubuntu-latest' not in text, path
        assert 'actions/checkout@v4' not in text, path
        assert 'actions/setup-python@v5' not in text, path
        assert "python-version: '3.12'" not in text, path
        assert 'pip install pytest==8.4.2' not in text, path
