"""
wsc_alpha.universe — tradable universe construction.

Intended responsibility (see docs/architecture.md):
- Apply liquidity / spread / price / volatility / shortability / sector-availability
  / data-quality filters to build the active research and trading universe.
- Track point-in-time universe membership so backtests don't use today's constituents
  to evaluate the past.

No implementation yet. Filter thresholds are not finalized — see the separate
risk-design work's universe section for reasoned starting ranges (not copied here
verbatim; this package should derive its own, reviewed thresholds before use).
"""

from __future__ import annotations
