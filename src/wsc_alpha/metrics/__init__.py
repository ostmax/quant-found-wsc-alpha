"""
wsc_alpha.metrics — daily NAV construction and performance metrics.

Intended responsibility (see docs/architecture.md):
- Build a verified daily (and where available, intraday) NAV series from realized +
  unrealized PnL, fees, and slippage.
- Derive Max Drawdown, Drawdown Duration, Recovery Time, weekly return, weekly
  residual alpha, rolling volatility, Sharpe, Sortino from that series.

No implementation yet. This is flagged as the single highest-priority new component
in docs/quant_found_mapping.md: no component in the private Quant Found production
system produces a trustworthy daily NAV series today, and this package must not
inherit that gap.
"""

from __future__ import annotations
