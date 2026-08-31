"""
wsc_alpha.execution — order execution against the Arena API.

Intended responsibility (see docs/architecture.md):
- Translate target positions into orders and submit them.
- Track order/execution lifecycle (a broker-agnostic FSM pattern is worth reusing
  from the private Quant Found execution_fsm.py — see docs/quant_found_mapping.md).
- Reconcile internal state against Arena-reported state before/after trading.

See arena_adapter.py for the current interface boundary — a stub only, no real
Arena API calls implemented yet, no token connected.
"""

from __future__ import annotations
