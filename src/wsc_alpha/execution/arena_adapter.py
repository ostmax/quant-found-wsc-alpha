"""
Abstract interface for the Arena API (Финам «Уолл-стрит код»).

Interface stub only — no network calls. Confirmed against the official
Регламент (docs/competition_rules.md, п. 2.1/2.2/2.6/2.7/2.11): "Finam Arena
API", free access via an individual token, instruments at
https://api.finam.ru/docs/rest/#assetsservice_assets, trading schedule at
https://api.finam.ru/docs/rest/#assetsservice_schedule. The Регламент does not
name order/account/position endpoints — those, and every method signature below,
remain a guess pending a read of the full REST docs at
https://api.finam.ru/docs/rest/ (not done as part of this pass — see
docs/competition_rules.md's UNKNOWN / NEEDS API VERIFICATION section).

Loosely modeled on the private Quant Found broker adapter's *shape*, not its
Tinkoff-specific implementation (see docs/quant_found_mapping.md).

Every method raises NotImplementedError.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


def format_ticker(symbol: str, mic: str) -> str:
    """SYMBOL@MIC (see docs/competition_rules.md, п. 2.7). Example from the
    Регламент itself: format_ticker("AAPL", "XNYS") == "AAPL@XNYS". Does not
    validate `mic`."""
    return f"{symbol}@{mic}"


# Field names below are placeholders, not confirmed against real Arena responses.

@dataclass
class ArenaAccount:
    account_id: str
    cash: float
    equity: float
    raw: dict[str, Any]


@dataclass
class ArenaPosition:
    ticker: str  # SYMBOL@MIC
    qty: float
    avg_price: float
    raw: dict[str, Any]


@dataclass
class ArenaOrder:
    order_id: str
    ticker: str  # SYMBOL@MIC
    side: str  # "BUY" | "SELL" — enum unconfirmed
    qty: float
    status: str
    raw: dict[str, Any]


class ArenaAdapter(ABC):
    """Adapter boundary so the rest of wsc_alpha can be built against a stable
    interface before the real Arena integration exists."""

    @abstractmethod
    def get_account(self) -> ArenaAccount: ...

    @abstractmethod
    def get_positions(self) -> list[ArenaPosition]: ...

    @abstractmethod
    def get_orders(self) -> list[ArenaOrder]:
        """Open orders only, or full history? Unconfirmed."""
        ...

    @abstractmethod
    def submit_order(
        self,
        *,
        ticker: str,
        side: str,
        qty: float,
        order_type: str = "TODO",
        limit_price: float | None = None,
    ) -> ArenaOrder:
        """order_type enum and time-in-force options unconfirmed."""
        ...

    @abstractmethod
    def cancel_order(self, order_id: str) -> bool: ...

    @abstractmethod
    def get_market_data(self, tickers: list[str]) -> dict[str, Any]:
        """Whether this is the same endpoint as account/orders or separate,
        per the competition's 15-minute delayed pricing, is unconfirmed."""
        ...


class UnimplementedArenaAdapter(ArenaAdapter):
    """Raises on every call. Never wire into anything expecting real data."""

    _MSG = "Arena API not implemented yet"

    def get_account(self) -> ArenaAccount:
        raise NotImplementedError(self._MSG)

    def get_positions(self) -> list[ArenaPosition]:
        raise NotImplementedError(self._MSG)

    def get_orders(self) -> list[ArenaOrder]:
        raise NotImplementedError(self._MSG)

    def submit_order(self, **kwargs: Any) -> ArenaOrder:
        raise NotImplementedError(self._MSG)

    def cancel_order(self, order_id: str) -> bool:
        raise NotImplementedError(self._MSG)

    def get_market_data(self, tickers: list[str]) -> dict[str, Any]:
        raise NotImplementedError(self._MSG)
