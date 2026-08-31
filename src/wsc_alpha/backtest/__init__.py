"""
wsc_alpha.backtest — point-in-time backtest engine.

Intended responsibility (see docs/architecture.md):
- Point-in-time universe reconstruction (no survivorship bias, no look-ahead).
- Realistic fills (NextOpenExecution-style: signal at close(t) -> fill at open(t+1),
  a philosophy worth reusing from the private Quant Found historical replay engine —
  see docs/quant_found_mapping.md; the implementation itself is not reused).
- Commission + slippage modeling, short-constraint enforcement.
- Walk-forward train/validation split, stress tests, parameter perturbation.

No implementation yet. NO backtest has been run under this package — any claim of
backtested performance for WSC Alpha before this package exists and has been run
would be fabricated.
"""

from __future__ import annotations
