from __future__ import annotations
from dataclasses import dataclass, replace
import re

CELL_IDENTITY="sha256:38610ff2afd70998a7fa3e522575faf697ec3159e00829c2b2bbd5da45c52054"
STRATEGY_VERSION_IDENTITY="sha256:0927e983046ef99a01d2a5c165d18ba5d501f69fb863875f72303b95f69b9687"
DR01_ADOPTION_BLOB="848e59ac0ef8e56d16322a17bd3f55a0b6e87e45"
BASE_OWNER_BLOB="524ee6afe0fe2fb49459f70ca4f6612a3bcf2739"
BASE_P1_12D_EXTENSION_BLOB="fec520916ca07ee6fe7e6029b4ca611519c39bc2"

SHA40=re.compile(r"^[0-9a-f]{40}$")
SHA64=re.compile(r"^[0-9a-f]{64}$")

class B12ControllerBlocked(RuntimeError):
    pass

@dataclass(frozen=True)
class Gate:
    b8_closed: bool
    b12_open: bool
    b12_human_opening_receipt_blob: str
    forward_instance_digest: str
    cell_identity: str
    strategy_version_identity: str
    dr01_adoption_blob: str
    base_owner_blob: str
    base_p1_12d_extension_blob: str
    result_preexposed: bool=False

@dataclass(frozen=True)
class ConsumptionState:
    state: str="PRISTINE"
    forward_instance_digest: str|None=None
    human_opening_receipt_blob: str|None=None
    performance_bearing_read_count: int=0
    terminal_package_digest: str|None=None
    independent_confirmation_eligible: bool=True
    trading_authority: bool=False
    broker_execution_authority: bool=False
    capital_authority: bool=False

def _sha40(v): return isinstance(v,str) and bool(SHA40.fullmatch(v))
def _sha64(v): return isinstance(v,str) and bool(SHA64.fullmatch(v))

def metadata_preflight(state: ConsumptionState) -> ConsumptionState:
    if state.state not in {"PRISTINE","AUTHORIZED_PENDING_READ"}:
        raise B12ControllerBlocked("METADATA_PREFLIGHT_AFTER_CONSUMPTION_FORBIDDEN")
    return state

def authorize(state: ConsumptionState, gate: Gate) -> ConsumptionState:
    if state.state != "PRISTINE":
        raise B12ControllerBlocked("AUTHORIZATION_REQUIRES_PRISTINE_STATE")
    if not gate.b8_closed:
        raise B12ControllerBlocked("B8_NOT_CLOSED")
    if not gate.b12_open:
        raise B12ControllerBlocked("B12_NOT_HUMAN_OPEN")
    if not _sha40(gate.b12_human_opening_receipt_blob):
        raise B12ControllerBlocked("INVALID_B12_HUMAN_OPENING_RECEIPT")
    if not _sha64(gate.forward_instance_digest):
        raise B12ControllerBlocked("INVALID_FORWARD_INSTANCE_DIGEST")
    if gate.cell_identity != CELL_IDENTITY:
        raise B12ControllerBlocked("CELL_IDENTITY_MISMATCH")
    if gate.strategy_version_identity != STRATEGY_VERSION_IDENTITY:
        raise B12ControllerBlocked("STRATEGY_VERSION_MISMATCH")
    if gate.dr01_adoption_blob != DR01_ADOPTION_BLOB:
        raise B12ControllerBlocked("DR01_BINDING_MISMATCH")
    if gate.base_owner_blob != BASE_OWNER_BLOB:
        raise B12ControllerBlocked("BASE_OWNER_BINDING_MISMATCH")
    if gate.base_p1_12d_extension_blob != BASE_P1_12D_EXTENSION_BLOB:
        raise B12ControllerBlocked("P1_12D_BINDING_MISMATCH")
    if gate.result_preexposed:
        raise B12ControllerBlocked("RESULT_PREEXPOSED")
    return replace(
        state,
        state="AUTHORIZED_PENDING_READ",
        forward_instance_digest=gate.forward_instance_digest,
        human_opening_receipt_blob=gate.b12_human_opening_receipt_blob,
    )

def first_performance_bearing_read(state: ConsumptionState) -> ConsumptionState:
    if state.state != "AUTHORIZED_PENDING_READ":
        raise B12ControllerBlocked("FIRST_READ_REQUIRES_AUTHORIZED_PENDING_READ")
    if state.performance_bearing_read_count != 0:
        raise B12ControllerBlocked("FIRST_READ_ALREADY_OCCURRED")
    return replace(
        state,
        state="CONSUMED_EXPOSED",
        performance_bearing_read_count=1,
        independent_confirmation_eligible=False,
    )

def technical_failure(state: ConsumptionState) -> ConsumptionState:
    if state.state == "AUTHORIZED_PENDING_READ":
        return ConsumptionState()
    if state.state == "CONSUMED_EXPOSED":
        return replace(state,state="TECHNICAL_FAILURE_CONSUMED",independent_confirmation_eligible=False)
    raise B12ControllerBlocked("TECHNICAL_FAILURE_INVALID_STATE")

def terminal_package_ready(state: ConsumptionState, terminal_package_digest: str) -> ConsumptionState:
    if state.state != "CONSUMED_EXPOSED":
        raise B12ControllerBlocked("TERMINAL_PACKAGE_REQUIRES_CONSUMED_STATE")
    if not _sha64(terminal_package_digest):
        raise B12ControllerBlocked("INVALID_TERMINAL_PACKAGE_DIGEST")
    return replace(
        state,
        state="TERMINAL_PACKAGE_READY",
        terminal_package_digest=terminal_package_digest,
        independent_confirmation_eligible=False,
    )

def replay_semantics(state: ConsumptionState, instance_digest: str) -> dict:
    if state.state not in {"CONSUMED_EXPOSED","TERMINAL_PACKAGE_READY","TECHNICAL_FAILURE_CONSUMED"}:
        raise B12ControllerBlocked("REPLAY_REQUIRES_CONSUMED_STATE")
    if instance_digest != state.forward_instance_digest:
        raise B12ControllerBlocked("REPLAY_INSTANCE_MISMATCH")
    return {
        "reproducibility_replay_permitted_if_separately_authorized": True,
        "new_independent_confirmation": False,
        "pristine_restored": False,
    }
