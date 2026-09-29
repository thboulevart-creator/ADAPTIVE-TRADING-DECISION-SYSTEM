from __future__ import annotations

import importlib.util
import os
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/"tools/e1_08a_r1_real_run.py"

EXPECTED_BASE_PROTECTED={
    "e1_01_e1_02_freeze_package_blob":"6b1e0d6e76d9813cd50eb01eb4b6c06cbfa8260e",
    "e1_03_runtime_blob":"38d481755e00ce3c2ed9c66c4db710500ca0911a",
    "e1_04_runtime_blob":"15e72b8743e7726fc8b8bedd933cf7defe56413b",
    "e1_05_runtime_blob":"baad3bd7c2e810451737c89bf8f9bcabc17c5ba6",
    "e1_06_reference_blob":"25b01e6d31709f02f9c095262bfe78366e83003b",
    "e1_06_qualifier_blob":"0793adc08416563125f57a55c0d272d24bb4b3df",
    "e1_07_runtime_blob":"88ca1f1ae89d1a2cfac1ae35becb3ea6209755f5",
    "phase_21_decision_blob":"eecbfd4a7c214a2d09210f5b0490c06673619c24",
}

def _target():
    spec=importlib.util.spec_from_file_location("e108r2_target",TARGET)
    if spec is None or spec.loader is None:
        pytest.fail("R2_TARGET_UNLOADABLE",pytrace=False)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_r2_01_real_windows_environment_passes():
    m=_target()
    assert os.name=="nt"
    out=m.verify_runtime_environment()
    assert out["status"]=="PASS"
    assert out["system"]=="Windows"
    assert out["python"]=="3.12.10"
    assert out["pyarrow"]=="25.0.1"

def test_r2_02_windows_31214_rejected(monkeypatch):
    m=_target()
    monkeypatch.setattr(m.platform,"system",lambda:"Windows")
    monkeypatch.setattr(m.platform,"python_version",lambda:"3.12.14")
    out=m.verify_runtime_environment()
    assert out["status"]=="BLOCKED"
    assert out["reason"]=="PYTHON_VERSION_MISMATCH"

def test_r2_03_linux_31214_remains_accepted(monkeypatch):
    m=_target()
    monkeypatch.setattr(m.platform,"system",lambda:"Linux")
    monkeypatch.setattr(m.platform,"python_version",lambda:"3.12.14")
    monkeypatch.setattr(m.pa,"__version__","25.0.1")
    out=m.verify_runtime_environment()
    assert out["status"]=="PASS"
    assert out["system"]=="Linux"
    assert out["python"]=="3.12.14"

def test_r2_04_pyarrow_exact(monkeypatch):
    m=_target()
    monkeypatch.setattr(m.platform,"system",lambda:"Windows")
    monkeypatch.setattr(m.platform,"python_version",lambda:"3.12.10")
    monkeypatch.setattr(m.pa,"__version__","25.0.0")
    out=m.verify_runtime_environment()
    assert out["status"]=="BLOCKED"
    assert out["reason"]=="PYARROW_VERSION_MISMATCH"

def test_r2_05_non_environment_bindings_unchanged():
    m=_target()
    assert m.BASE_PROTECTED_BLOBS==EXPECTED_BASE_PROTECTED
    assert m.SOURCE_MANIFEST_SHA256=="c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5"
    assert m.SOURCE_INVENTORY_DIGEST=="5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf"
    assert m.H1_JSONL_SHA256=="94ccb7c78e2e21cb3baa2dfe0945e7b39e20f74300c3c72addb89135d5af1ca0"
    assert m.H1_CANONICAL_STREAM_SHA256=="15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f"
    assert m.OOS_START=="2025-05-25T00:00:00Z"
    assert m.OOS_END=="2026-05-24T23:59:59.963Z"
