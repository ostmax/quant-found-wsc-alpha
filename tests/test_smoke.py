"""Smoke tests: package imports, and the Arena adapter stub actually raises
instead of silently returning fake data."""

from __future__ import annotations

import importlib

import pytest


def test_top_level_package_imports():
    import wsc_alpha

    assert hasattr(wsc_alpha, "__version__")


def test_all_subpackages_import():
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


def test_arena_adapter_raises_not_implemented():
    from wsc_alpha.execution.arena_adapter import UnimplementedArenaAdapter

    adapter = UnimplementedArenaAdapter()

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
