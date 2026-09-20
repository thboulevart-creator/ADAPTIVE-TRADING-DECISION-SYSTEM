from __future__ import annotations

import pytest

from breakers import native_bi5_qrm12_compatibility_breaker as qrm


def _check(source: str) -> None:
    qrm._assert_no_preseal_cross_path_source_flow(
        source,
        forbidden_module=qrm.IB2_MODULE,
        forbidden_result_name="ib_result",
    )


def test_e3a_required_isolation_field_is_not_cross_path_flow() -> None:
    _check(
        """
def snapshot(ctx):
    readable = ctx.get("other_path_output_readable")
    return {"other_path_output_readable": readable is False}
"""
    )


@pytest.mark.parametrize(
    "source",
    (
        "def f():\n    other_path_output = object()\n",
        "def f(obj):\n    return obj.other_path_output\n",
        "def f():\n    ib_result = object()\n",
        "def f():\n    expected_other_result = object()\n",
        "from src import native_bi5_independent_qualifier_qrm12\n",
        "def f(importlib):\n    return importlib.import_module('src.native_bi5_independent_qualifier_qrm12')\n",
        "def f(mapping):\n    return mapping['other_path_output']\n",
    ),
)
def test_e3b_real_static_cross_path_channels_remain_rejected(source: str) -> None:
    with pytest.raises(AssertionError):
        _check(source)


def test_e3c_comments_do_not_create_false_information_flow() -> None:
    _check(
        """
# other_path_output is forbidden as a real data channel.
def f(ctx):
    return ctx.get("other_path_output_readable") is False
"""
    )


def test_e3d_actual_qualified_ia_and_ib_sources_pass_repaired_control() -> None:
    ia = qrm._ia2()
    ib = qrm._ib2()
    import inspect

    qrm._assert_no_preseal_cross_path_source_flow(
        inspect.getsource(ia),
        forbidden_module=qrm.IB2_MODULE,
        forbidden_result_name="ib_result",
    )
    qrm._assert_no_preseal_cross_path_source_flow(
        inspect.getsource(ib),
        forbidden_module=qrm.IA2_MODULE,
        forbidden_result_name="ia_result",
    )
