from __future__ import annotations

from pathlib import Path

from tools import rvo_10_retry_session as s


def _built():
    return {
        "specification": {"experiment_spec_id": "EXS-X"},
        "execution_binding": {"execution_binding_id": "EEB-X"},
        "qualified_input": {"experiment_execution_input_id": "QEI-X"},
        "data_binding": {
            "p1_data_evidence_binding_id": "P1DE-X",
            "p1_data_evidence_binding_digest": "d" * 64,
        },
        "invocation_profile": {
            "invocation_profile_id": "P1_12C_AP1_CLAIM_SCOPED_V1",
            "invocation_profile_digest": "p" * 64,
        },
        "runtime_lock": {
            "runtime_lock_id": "RPRL-X",
            "runtime_lock_digest": "r" * 64,
        },
        "plan": {
            "real_producer_execution_plan_id": "QRPP-X",
            "real_producer_execution_plan_digest": "q" * 64,
        },
        "resource_contract_blob": "a" * 40,
        "resource_contract_sha256": "b" * 64,
        "command": ["python.exe", "-E", "-P", "runner.py"],
        "command_digest": "c" * 64,
    }


def test_session_contract_is_exact():
    assert s.SESSION_CONTRACT == "ATDS_RVO_10_IN_MEMORY_PLAN_FREEZE_ACK_SESSION_V0_1"


def test_freeze_binds_same_in_memory_plan():
    freeze = s._build_freeze(
        execution_head="1" * 40,
        execution_tree="2" * 40,
        workspace={"clean": True},
        owners={"owner": "blob"},
        rvo09_final={"status": "RVO_09_QUALIFIED_CLOSED"},
        revalidation={"verdict": "GO"},
        history={"historical_invocation_count": 1},
        built=_built(),
        ap0_root=Path("AP0"),
        ap0_manifest=Path("AP0/AP0-MANIFEST.json"),
        retry_output=Path("retry.json"),
    )
    assert freeze["plan_binding_mode"] == "IN_MEMORY_FACTORY_OBJECT_HELD_ACROSS_FREEZE_ACK"
    assert freeze["experiment_spec_id"] == "EXS-X"
    assert freeze["execution_binding_id"] == "EEB-X"
    assert freeze["experiment_execution_input_id"] == "QEI-X"
    assert freeze["real_producer_execution_plan_id"] == "QRPP-X"
    assert freeze["real_producer_execution_plan_digest"] == "q" * 64
    assert freeze["automatic_retry"] is False
    assert freeze["m03_execution_authorized"] is False
    assert freeze["authority"]["scientific"] is False
    assert freeze["authority"]["trading"] is False
    assert freeze["authority"]["capital"] is False


def test_session_has_exactly_one_real_invocation_site():
    source = Path(s.__file__).read_text(encoding="utf-8")
    needle = 'cp = subprocess.run(\n            built["command"],'
    assert source.count(needle) == 1


def test_session_never_promotes_execution_result():
    source = Path(s.__file__).read_text(encoding="utf-8")
    assert '"scientific_finding": False' in source
    assert '"strategy_validated": False' in source
    assert '"trading_signal": False' in source
    assert '"m03_executed": False' in source
