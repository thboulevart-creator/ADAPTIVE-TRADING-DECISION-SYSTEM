from __future__ import annotations

def test_red_owner_module_import():
    from src import p1_12c_ao_e0_native_owner as owner
    assert owner.CONTRACT=="P1_12C_AO_E0_CC05_NATIVE_EXECUTION_OWNER_V0_1"

def test_red_p112d_extension_import():
    from src import p1_12d_ao_e0_extension as ext
    assert ext.AO_E0_ALLOWED_OWNER=="P1.12C.AO-E0"
