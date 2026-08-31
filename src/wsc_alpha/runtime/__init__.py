"""
wsc_alpha.runtime — process orchestration (research / paper / live modes).

Intended responsibility (see docs/architecture.md):
- Wire together data -> universe -> features -> alpha -> portfolio -> risk ->
  execution -> metrics into a runnable cycle, once each stage has a real
  implementation.
- Mode gating (research-only vs. paper vs. live), analogous in spirit to the private
  Quant Found's TRADING_MODE gate (DRY/PAPER/LIVE/...) — no implementation is
  ported, only the principle of an explicit, fail-closed mode switch.

No implementation yet. No mode in this package currently supports live or paper
trading — this repository does not connect to a real Arena account at this stage
(see README.md, "Status").
"""

from __future__ import annotations
