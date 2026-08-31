"""
arena_adapter.py — abstract interface boundary for the Arena API (Финам
«Уолл-стрит код»).

STATUS: interface stub only. NOT a working implementation.

Nothing in this file makes a network call. No Arena API documentation has been
reviewed in depth for this pass — the method names/signatures below are a
*reasonable guess* at the operations any broker-style execution API needs
(account/positions/orders/submit/cancel/market-data), modeled loosely on the shape
of the private Quant Found broker adapter (see docs/quant_found_mapping.md,
"Execution" section — that adapter's *shape*, not its Tinkoff-specific
implementation, is the reference here).

Every method is marked TODO and raises NotImplementedError. Do not fill these in
from assumptions about Arena's actual API — implement each once the real API
documentation is available, and update the signature to match what Arena actually
returns/expects rather than what is guessed here.

No credentials, tokens, or endpoints are referenced anywhere in this file — see
.env.example for how a real token would be supplied later (via environment variable,
never hard-coded).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


# =========================================================
# TICKER FORMAT
# =========================================================
# Per docs/competition_rules.md (item 5, operator-relayed — not yet verified against
# the primary Regulation): instruments are addressed as "SYMBOL@MIC", e.g.
# "AAPL@XNAS". This helper exists so callers don't hand-roll the format in multiple
# places; it does not validate against a real MIC list (none confirmed yet).

def format_ticker(symbol: str, mic: str) -> str:
    """Build a SYMBOL@MIC identifier. Does not validate `mic` against a known list —
    no confirmed MIC list exists yet (see docs/competition_rules.md, open items)."""
    return f"{symbol}@{mic}"


# =========================================================
# DATA SHAPES
# =========================================================
# Placeholder shapes only — field names are a best guess, not confirmed against
# real Arena API responses. Expect these to change once real documentation exists.

@dataclass
class ArenaAccount:
    """TODO: fields unconfirmed — placeholder shape only."""
    account_id: str
    cash: float
    equity: float
    raw: dict[str, Any]


@dataclass
class ArenaPosition:
    """TODO: fields unconfirmed — placeholder shape only."""
    ticker: str  # SYMBOL@MIC
    qty: float
    avg_price: float
    raw: dict[str, Any]


@dataclass
class ArenaOrder:
    """TODO: fields unconfirmed — placeholder shape only."""
    order_id: str
    ticker: str  # SYMBOL@MIC
    side: str  # "BUY" | "SELL" — unconfirmed against real API enum
    qty: float
    status: str
    raw: dict[str, Any]


# =========================================================
# ADAPTER INTERFACE
# =========================================================

class ArenaAdapter(ABC):
    """
    Abstract boundary for all Arena API interaction.

    No concrete implementation exists yet. This class exists so the rest of
    wsc_alpha (portfolio construction, risk, backtest-vs-live parity) can be built
    and tested against this interface before the real Arena integration is written
    — the same "adapter boundary first" discipline the private Quant Found
    production system uses (see docs/quant_found_mapping.md, "Execution" section).

    Every method below is TODO. Do not implement against guessed behavior — wait
    for confirmed Arena API documentation.
    """

    # ---- account / state ----

    @abstractmethod
    def get_account(self) -> ArenaAccount:
        """TODO: confirm against real Arena API — cash/equity/buying-power shape
        unconfirmed."""
        raise NotImplementedError

    @abstractmethod
    def get_positions(self) -> list[ArenaPosition]:
        """TODO: confirm against real Arena API."""
        raise NotImplementedError

    @abstractmethod
    def get_orders(self) -> list[ArenaOrder]:
        """TODO: confirm against real Arena API — does this return only open orders,
        or full history? Unconfirmed."""
        raise NotImplementedError

    # ---- order management ----

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
        """TODO: confirm against real Arena API — order_type enum, whether
        limit_price is required/optional for each type, and time-in-force options
        are all unconfirmed. `order_type="TODO"` is a deliberate placeholder, not a
        real default."""
        raise NotImplementedError

    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """TODO: confirm against real Arena API — return shape on success/failure
        unconfirmed."""
        raise NotImplementedError

    # ---- market data ----
    # Per docs/competition_rules.md (item 8, operator-relayed): pricing is
    # 15-minute delayed. Whether Arena exposes this via the same API surface as
    # account/orders, or a separate market-data endpoint, is UNKNOWN — see
    # docs/architecture.md.

    @abstractmethod
    def get_market_data(self, tickers: list[str]) -> dict[str, Any]:
        """TODO: method name and return shape are both unconfirmed guesses.
        Replace once the real Arena market-data endpoint(s) are documented."""
        raise NotImplementedError


class UnimplementedArenaAdapter(ArenaAdapter):
    """
    Concrete placeholder that raises a clear error on every call, so the rest of
    the codebase can import and reference `ArenaAdapter` without a real
    implementation existing yet. Never wire this into anything that expects real
    account data.
    """

    def get_account(self) -> ArenaAccount:  # noqa: D102
        raise NotImplementedError("Arena API not yet implemented — see arena_adapter.py TODOs")

    def get_positions(self) -> list[ArenaPosition]:  # noqa: D102
        raise NotImplementedError("Arena API not yet implemented — see arena_adapter.py TODOs")

    def get_orders(self) -> list[ArenaOrder]:  # noqa: D102
        raise NotImplementedError("Arena API not yet implemented — see arena_adapter.py TODOs")

    def submit_order(self, **kwargs: Any) -> ArenaOrder:  # noqa: D102
        raise NotImplementedError("Arena API not yet implemented — see arena_adapter.py TODOs")

    def cancel_order(self, order_id: str) -> bool:  # noqa: D102
        raise NotImplementedError("Arena API not yet implemented — see arena_adapter.py TODOs")

    def get_market_data(self, tickers: list[str]) -> dict[str, Any]:  # noqa: D102
        raise NotImplementedError("Arena API not yet implemented — see arena_adapter.py TODOs")
