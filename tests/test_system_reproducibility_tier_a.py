from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from tools.qualification_environment import (
    EnvironmentSnapshot,
    QualificationEnvironmentError,
    load_lock,
    validate_lock_document,
    verify_current_environment,
    verify_snapshot,
)


LOCK = Path('04-REFERENCE/QUALIFICATION-ENVIRONMENT-LOCK.json')
REQUIREMENTS = Path('requirements/qualification.lock.txt')
VERIFIER = Path('tools/qualification_environment.py')
CONTRACT = Path('04-REFERENCE/SYSTEM-REPRODUCIBILITY-CONTRACT.md')

CHECKOUT_SHA = '11d5960a326750d5838078e36cf38b85af677262'
SETUP_PYTHON_SHA = 'a26af69be951a213d495a4c3e4e4022e16d87065'

PROTECTED_WORKFLOWS = (
    Path('.github/workflows/data-to-context.yml'),
    Path('.github/workflows/context-to-research-boundary.yml'),
    Path('.github/workflows/research-findings-contract.yml'),
    Path('.github/workflows/research-to-decision-boundary.yml'),
    Path('.github/workflows/p0-2-decision-block-integration-rebreak.yml'),
    Path('.github/workflows/p0-3-multi-year-integration-rebreak.yml'),
    Path('.github/workflows/p0-4-research-producer-junction.yml'),
    Path('.github/workflows/p0-5-research-interprocess-reattestation.yml'),
    Path('.github/workflows/p0-6-system-reproducibility.yml'),
)

DURABLE_FUNCTIONAL_COMMANDS = {
    Path('.github/workflows/data-to-context.yml'): (
        'tests/test_data_to_context.py',
        'tests/test_context_to_research_boundary.py',
    ),
    Path('.github/workflows/context-to-research-boundary.yml'): (
        'tests/test_context_to_research_boundary.py',
        'tests/test_context_research_alternative_paths.py',
    ),
    Path('.github/workflows/research-findings-contract.yml'): (
        'tests/test_research_findings_contract.py',
    ),
    Path('.github/workflows/research-to-decision-boundary.yml'): (
        'tests/test_research_to_decision_boundary.py',
        'tests/test_research_findings_contract.py',
        'tests/test_research_reader_adversarial.py',
        'tests/test_context_research_alternative_paths.py',
        'tests/test_durable_ci_branch_independence.py',
    ),
}


def _lock() -> dict:
    return load_lock()


def _synthetic_valid_snapshot(lock: dict) -> EnvironmentSnapshot:
    return EnvironmentSnapshot(
        implementation=lock['python']['implementation'],
        python_version=lock['python']['version'],
        system=lock['platform']['system'],
        github_actions=True,
        runner_os=lock['platform']['github_runner_os'],
        runner_arch=lock['platform']['github_runner_arch'],
        environment=dict(lock['environment']),
        packages=dict(lock['requirements']['packages']),
    )


def _fails(lock: dict, snapshot: EnvironmentSnapshot) -> None:
    with pytest.raises(QualificationEnvironmentError):
        verify_snapshot(lock, snapshot)


def test_e0_authoritative_lock_and_current_environment_pass() -> None:
    assert LOCK.is_file()
    assert REQUIREMENTS.is_file()
    assert VERIFIER.is_file()
    assert CONTRACT.is_file()
    lock = _lock()
    assert lock['schema'] == 'QUALIFICATION_ENVIRONMENT_LOCK_V1'
    assert lock['scope'] == 'P0_2_TO_P0_6_QUALIFICATION'
    expected_requirements = (
        'iniconfig==2.3.0\n'
        'packaging==26.3\n'
        'pluggy==1.6.0\n'
        'Pygments==2.21.0\n'
        'pytest==8.4.2\n'
    ).encode('utf-8')
    assert REQUIREMENTS.read_bytes() == expected_requirements
    assert hashlib.sha256(expected_requirements).hexdigest() == lock['requirements']['sha256']
    verify_snapshot(lock, _synthetic_valid_snapshot(lock))
    verify_current_environment()


def test_e1_python_implementation_drift_rejected() -> None:
    lock = _lock()
    _fails(lock, replace(_synthetic_valid_snapshot(lock), implementation='pypy'))


def test_e2_python_version_drift_rejected() -> None:
    lock = _lock()
    _fails(lock, replace(_synthetic_valid_snapshot(lock), python_version='3.12.15'))
    _fails(lock, replace(_synthetic_valid_snapshot(lock), python_version='3.13.0'))


def test_e3_os_drift_rejected() -> None:
    lock = _lock()
    _fails(lock, replace(_synthetic_valid_snapshot(lock), system='Windows'))


def test_e4_github_runner_family_and_architecture_drift_rejected() -> None:
    lock = _lock()
    valid = _synthetic_valid_snapshot(lock)
    _fails(lock, replace(valid, runner_os='Windows'))
    _fails(lock, replace(valid, runner_arch='ARM64'))


def test_e5_required_environment_missing_or_drifted_rejected() -> None:
    lock = _lock()
    valid = _synthetic_valid_snapshot(lock)
    for name, expected in lock['environment'].items():
        missing = dict(valid.environment)
        missing[name] = None
        _fails(lock, replace(valid, environment=missing))
        drifted = dict(valid.environment)
        drifted[name] = expected + '-DRIFT'
        _fails(lock, replace(valid, environment=drifted))


def test_e6_required_package_missing_rejected() -> None:
    lock = _lock()
    valid = _synthetic_valid_snapshot(lock)
    for name in lock['requirements']['packages']:
        packages = dict(valid.packages)
        packages[name] = None
        _fails(lock, replace(valid, packages=packages))


def test_e7_required_package_version_drift_rejected() -> None:
    lock = _lock()
    valid = _synthetic_valid_snapshot(lock)
    for name, expected in lock['requirements']['packages'].items():
        packages = dict(valid.packages)
        packages[name] = expected + '.drift'
        _fails(lock, replace(valid, packages=packages))


def test_e8_requirements_bytes_drift_rejected_even_with_old_lock(tmp_path: Path) -> None:
    lock = _lock()
    requirements_dir = tmp_path / 'requirements'
    requirements_dir.mkdir()
    (requirements_dir / 'qualification.lock.txt').write_bytes(
        REQUIREMENTS.read_bytes() + b'pytest-cov==7.0.0\n'
    )
    with pytest.raises(QualificationEnvironmentError, match='hash mismatch'):
        validate_lock_document(copy.deepcopy(lock), root=tmp_path)


def test_e9_environment_lock_schema_unknown_missing_and_substituted_rejected() -> None:
    lock = _lock()

    unknown = copy.deepcopy(lock)
    unknown['unexpected'] = True
    with pytest.raises(QualificationEnvironmentError, match='schema mismatch'):
        validate_lock_document(unknown)

    missing = copy.deepcopy(lock)
    del missing['actions']
    with pytest.raises(QualificationEnvironmentError, match='schema mismatch'):
        validate_lock_document(missing)

    substituted = copy.deepcopy(lock)
    substituted['schema'] = 'QUALIFICATION_ENVIRONMENT_LOCK_V2_FORGED'
    with pytest.raises(QualificationEnvironmentError, match='unsupported'):
        validate_lock_document(substituted)


def test_e10_all_protected_workflows_pin_immutable_actions() -> None:
    for path in PROTECTED_WORKFLOWS:
        text = path.read_text(encoding='utf-8')
        assert f'actions/checkout@{CHECKOUT_SHA}' in text, path
        assert f'actions/setup-python@{SETUP_PYTHON_SHA}' in text, path
        assert 'actions/checkout@v4' not in text, path
        assert 'actions/setup-python@v5' not in text, path


def test_e11_all_protected_workflows_use_locked_runner_python_packages_and_verifier() -> None:
    required_env = {
        "PYTHONDONTWRITEBYTECODE": "'1'",
        "PYTHONHASHSEED": "'0'",
        "TZ": "'UTC'",
        "LANG": "'C.UTF-8'",
        "LC_ALL": "'C.UTF-8'",
    }
    for path in PROTECTED_WORKFLOWS:
        text = path.read_text(encoding='utf-8')
        assert 'runs-on: ubuntu-24.04' in text, path
        assert 'ubuntu-latest' not in text, path
        assert "python-version: '3.12.14'" in text, path
        assert "python-version: '3.12'" not in text, path
        assert 'pip install pytest==8.4.2' not in text, path
        assert '--no-deps -r requirements/qualification.lock.txt' in text, path
        assert 'python tools/qualification_environment.py verify' in text, path
        assert '\npermissions:\n  contents: read\n' in text, path
        for name, value in required_env.items():
            assert f'{name}: {value}' in text, (path, name)
        assert '04-REFERENCE/QUALIFICATION-ENVIRONMENT-LOCK.json' in text, path
        assert 'requirements/qualification.lock.txt' in text, path
        assert 'tools/qualification_environment.py' in text, path

    for path, commands in DURABLE_FUNCTIONAL_COMMANDS.items():
        text = path.read_text(encoding='utf-8')
        for command in commands:
            assert command in text, (path, command)


def test_e12_optional_pyarrow_remains_explicitly_outside_p06() -> None:
    lock = _lock()
    assert lock['optional_excluded']['pyarrow']['status'] == 'BLOCKED_OUTSIDE_P0_6'
    assert all(name.lower() != 'pyarrow' for name in lock['requirements']['packages'])
    contract = CONTRACT.read_text(encoding='utf-8')
    assert 'optional `pyarrow` Parquet path remains explicitly outside P0.6' in contract
