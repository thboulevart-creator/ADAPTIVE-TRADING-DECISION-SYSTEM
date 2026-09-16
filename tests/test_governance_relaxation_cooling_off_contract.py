from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / 'GOVERNANCE' / 'GOVERNANCE-EVOLUTION-AND-AUDIT-PROTOCOL.md'
REGISTER = ROOT / 'GOVERNANCE' / 'GOVERNANCE-AUDIT-REGISTER.md'


def test_governance_relaxation_cooling_off_contract_is_persisted() -> None:
    text = PROTOCOL.read_text(encoding='utf-8')
    required = (
        'GOVERNANCE_RELAXATION_COOLING_OFF_V1',
        '30 jours',
        'réinitialise les 30 jours',
        'Tier A',
        'falsifiabilité du moniteur par injection',
        'coût de révocation borné et connu',
        'Le système peut devenir plus restrictif seul ; il ne peut jamais devenir plus permissif seul.',
        "`BLOCKED` n'est jamais `PASS`",
    )
    for token in required:
        assert token in text


def test_p0_jit_audit_records_scope_and_explicit_complement() -> None:
    text = REGISTER.read_text(encoding='utf-8')
    assert 'P0_FULL_SUITE_REBASELINE_JIT_AUDIT_V1' in text
    assert 'Périmètre couvert' in text
    assert 'Complément explicitement non audité' in text
    assert 'BoundaryState' in text
    assert 'jonction `src/research/` ↔ `research_run_evidence`' in text
    assert 'aucun `skip`, `xfail` ou effacement de test' in text
