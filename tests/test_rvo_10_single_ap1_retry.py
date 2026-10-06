from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools import rvo_10_single_ap1_retry as r


def test_rvo10_contract_and_budget_are_exact():
    assert r.CONTRACT == "ATDS_RVO_10_FIRST_REAL_CC02_SINGLE_AP1_RETRY_V0_1"
    assert r.HISTORICAL_INVOCATION_COUNT == 1
    assert r.RETRY_INVOCATION_BUDGET == 1
    assert r.TOTAL_ORDINAL == 2
    assert r.TIMEOUT_SECONDS == 3600
    assert r.MAX_OUTPUT_BYTES == 32 * 1024 * 1024


def test_repaired_profile_and_runtime_are_exact():
    assert r.PROFILE_ID == "P1_12C_AP1_CLAIM_SCOPED_V1"
    assert r.PROFILE_DIGEST == "7487a1ffc0adab8c60bd36caf196130402908367c676bb03ca9abe36b56c6d9c"
    assert r.RUNTIME_LOCK_ID == "RPRL-25a96a47d1a1e1677374974e9fe7c8db"
    assert r.RUNTIME_LOCK_DIGEST == "25a96a47d1a1e1677374974e9fe7c8dbd8e3abb37a0f3a1e0566ebd1d88fb306"


def test_protected_owner_identities_pin_repaired_p1_and_unchanged_ap1():
    assert r.PROTECTED_BLOBS["tools/ap1_intraday_spread_census.py"] == "9f613063fb8a190a1ff6f2f8b12c97c4ed97712a"
    assert r.PROTECTED_BLOBS["src/p1_12c_qualified_producer_execution.py"] == "87d2ef49c0b70b956ada19443f5ba693cfb5b242"
    assert r.PROTECTED_BLOBS["tools/p1_12c_sandbox_runner.py"] == "78aa1615a093c241774fdea1018b69f47728ecb6"
    assert r.PROTECTED_BLOBS["reports/program/2026-10-06-RVO-09-FINAL-QUALIFICATION-RECEIPT-V0.1.json"] == "34c0e1d6e57d4becdf72642c4bce0f46005403af"


def test_bounded_text_preserves_short_and_bounds_long():
    short, truncated = r.bounded_text(b"abc", limit=10)
    assert short == "abc"
    assert truncated is False

    long, truncated = r.bounded_text(b"x" * 100, limit=20)
    assert truncated is True
    assert "RVO10_DIAGNOSTIC_TRUNCATED" in long
    assert long.startswith("x" * 10)
    assert long.endswith("x" * 10)


def _make_verify_fixture(tmp_path: Path):
    freeze = tmp_path / "freeze.json"
    output = tmp_path / "output.json"
    stdout = tmp_path / "stdout.bin"
    stderr = tmp_path / "stderr.bin"
    receipt = tmp_path / "receipt.json"
    ledger = tmp_path / "ledger.json"

    freeze.write_text(json.dumps({"freeze": True}), encoding="utf-8")
    output.write_bytes(b"{}")
    stdout.write_bytes(b"stdout")
    stderr.write_bytes(b"stderr")

    payload = {
        "status": "RVO_10_SINGLE_AP1_RETRY_COMPLETE",
        "historical_invocation_count": 1,
        "retry_invocation_count": 1,
        "total_real_ap1_invocations": 2,
        "automatic_retry": False,
        "exit_code": 0,
        "timeout_observed": False,
        "m03_executed": False,
        "scientific_finding": False,
        "authority": dict(r.AUTHORITY_NONE),
        "output_transport": str(output),
        "output_bytes": output.stat().st_size,
        "output_sha256": r.sha256_path(output),
        "freeze_sha256": r.sha256_path(freeze),
        "stdout_path": str(stdout),
        "stdout_sha256": r.sha256_path(stdout),
        "stderr_path": str(stderr),
        "stderr_sha256": r.sha256_path(stderr),
    }
    receipt.write_text(json.dumps(payload), encoding="utf-8")
    ledger.write_text(json.dumps({
        "historical_invocation_count": 1,
        "retry_invocation_count": 1,
        "total_real_ap1_invocations": 2,
        "state": "COMPLETED_SUCCESS",
    }), encoding="utf-8")
    return freeze, receipt, ledger


def test_verify_accepts_exact_one_retry_history(tmp_path: Path, capsys):
    freeze, receipt, ledger = _make_verify_fixture(tmp_path)
    class Args:
        pass
    a = Args()
    a.freeze = str(freeze)
    a.execution_receipt = str(receipt)
    a.retry_ledger = str(ledger)
    assert r.verify(a) == 0
    assert "TOTAL_REAL_AP1_INVOCATIONS=2" in capsys.readouterr().out


def test_verify_rejects_total_invocation_count_not_two(tmp_path: Path):
    freeze, receipt, ledger = _make_verify_fixture(tmp_path)
    obj = json.loads(receipt.read_text(encoding="utf-8"))
    obj["total_real_ap1_invocations"] = 3
    receipt.write_text(json.dumps(obj), encoding="utf-8")
    class Args:
        pass
    a = Args()
    a.freeze = str(freeze)
    a.execution_receipt = str(receipt)
    a.retry_ledger = str(ledger)
    with pytest.raises(r.RVO10Blocked, match="TOTAL_INVOCATION_COUNT_INVALID"):
        r.verify(a)


def test_authority_none_excludes_scientific_trading_and_capital():
    assert r.AUTHORITY_NONE == {
        "scientific": False,
        "operational": False,
        "trading": False,
        "capital": False,
    }


def test_source_contains_single_real_command_invocation_site():
    source = Path(r.__file__).read_text(encoding="utf-8")
    needle = 'cp = subprocess.run(\n            built["command"],'
    assert source.count(needle) == 1
