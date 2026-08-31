"""
wsc_alpha.portfolio — portfolio construction and market/sector neutralization.

Intended responsibility (see docs/architecture.md):
- Aggregate active alpha ideas into portfolio-level target positions.
- Beta-adjust leg sizing so ideas net close to market/sector-beta-neutral, not just
  dollar-neutral (dollar-neutral and beta-neutral are different targets — see the
  separate risk-design work's position-sizing worked example).

No implementation yet.
"""

from __future__ import annotations
