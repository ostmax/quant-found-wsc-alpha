"""
Smoke tests only, at this stage.

No backtest results, no strategy behavior, no live/paper execution is tested here —
none of that exists yet. This file only confirms the package skeleton is importable
and the sub-packages exist where the architecture doc says they should.
"""

from __future__ import annotations

import importlib


def test_top_level_package_imports():
    import wsc_alpha

    assert hasattr(wsc_alpha, "__version__")


def test_all_subpackages_import():
    """Every subpackage listed in docs/architecture.md's component table must at
    least be importable, even though none has a real implementation yet."""
    subpackages = [
        "wsc_alpha.data",
        "wsc_alpha.universe",
        "wsc_alpha.features",
        "wsc_alpha.alpha",
        "wsc_alpha.portfolio",
        "wsc_alpha.risk",
        "wsc_alpha.execution",
        "wsc_alpha.backtest",
        "wsc_alpha.metrics",
        "wsc_alpha.runtime",
    ]
    for name in subpackages:
        importlib.import_module(name)


def test_arena_adapter_interface_is_unimplemented_not_silently_working():
    """The Arena adapter must be a clearly-unimplemented stub, not something that
    could be mistaken for a working integration. Every method must raise."""
    from wsc_alpha.execution.arena_adapter import UnimplementedArenaAdapter

    adapter = UnimplementedArenaAdapter()

    import pytest

    with pytest.raises(NotImplementedError):
        adapter.get_account()

    with pytest.raises(NotImplementedError):
        adapter.get_positions()

    with pytest.raises(NotImplementedError):
        adapter.get_orders()

    with pytest.raises(NotImplementedError):
        adapter.submit_order(ticker="AAPL@XNAS", side="BUY", qty=1)

    with pytest.raises(NotImplementedError):
        adapter.cancel_order("some-id")

    with pytest.raises(NotImplementedError):
        adapter.get_market_data(["AAPL@XNAS"])


def test_ticker_format_helper():
    from wsc_alpha.execution.arena_adapter import format_ticker

    assert format_ticker("AAPL", "XNAS") == "AAPL@XNAS"
