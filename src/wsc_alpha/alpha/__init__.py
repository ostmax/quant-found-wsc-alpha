"""
wsc_alpha.alpha — alpha candidate discovery.

Intended responsibility (see docs/architecture.md):
- Generate alpha idea candidates from residual (market/sector-neutralized) return
  features produced by wsc_alpha.features.
- Structure a candidate as an Alpha Idea (1..N legs), not as an independent position
  per instrument — see the separate risk-design work's Alpha Idea/Cluster section.

No implementation yet. No specific signal/strategy logic is disclosed in this public
repository — see README.md's "what this repo does not claim" section.
"""

from __future__ import annotations
