"""
wsc_alpha.risk — position, portfolio, and drawdown risk management.

Intended responsibility (see docs/architecture.md):
- Position-level limits (max % NAV, max risk contribution per idea/cluster).
- Portfolio-level limits (gross/net exposure, market beta, sector beta,
  concentration, correlation).
- Drawdown policy (soft / reduce-risk / hard-stop thresholds, recovery staging,
  cooldown).

No implementation yet. NONE of the numeric limits from the private Quant Found
production system (risk_engine.py, risk_guard.py) are ported here — see
docs/quant_found_mapping.md's explicit warning that those thresholds were tuned for
a different (MOEX pairs/solo) production system and are not a calibration reference
for this one.
"""

from __future__ import annotations
