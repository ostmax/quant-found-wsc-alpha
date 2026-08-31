"""
wsc_alpha.features — feature computation.

Intended responsibility (see docs/architecture.md):
- Rolling market/sector beta estimation (stock return regressed against SPY and the
  relevant GICS sector ETF).
- Residual (idiosyncratic) return series — the input to alpha candidate generation.

No implementation yet. The private Quant Found feature_engine.py is DO NOT USE here
(tick-resolution MOEX-specific file format) — see docs/quant_found_mapping.md.
"""

from __future__ import annotations
