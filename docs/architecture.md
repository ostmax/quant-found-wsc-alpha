# WSC Alpha — Architecture (Draft)

**Status:** design draft, no implementation behind most stages yet. This document
describes the *intended* data flow and component boundaries, not a working system.
See `docs/quant_found_mapping.md` for what (if anything) informs each stage from the
private Quant Found production system, and README.md's "Status" section for the
current state of the repository.

## Intended data flow

```
Market Data
   │  (US common stock + broad-market-index-tracking ETFs, 15-minute delayed,
   │   ticker format SYMBOL@MIC, live instrument list via Arena API — all
   │   confirmed against the official Регламент, see docs/competition_rules.md)
   ▼
Universe
   │  (liquidity / spread / price / volatility / shortability / sector /
   │   data-quality filters; point-in-time membership for backtests)
   ▼
Features
   │  (rolling market + sector beta estimation; residual return series)
   ▼
Alpha Discovery
   │  (candidate generation from residual features)
   ▼
Alpha Candidates
   │  (Alpha Idea: 1..N legs, not independent per-instrument risks)
   ▼
Portfolio Construction
   │  (aggregate active ideas into target positions)
   ▼
Market Neutralization
   │  (beta-adjust leg sizing so ideas net close to beta-neutral,
   │   not just dollar-neutral)
   ▼
Risk Management
   │  (position / portfolio / drawdown limits — see config/wsc_alpha.example.yaml)
   ▼
Execution
   │  (Arena API — see src/wsc_alpha/execution/arena_adapter.py, interface only)
   ▼
NAV / Metrics
   │  (daily NAV series → drawdown, Sharpe, Sortino, weekly alpha)
   └─ feeds back into Risk Management (drawdown policy throttles position sizing)
```

The feedback arrow (NAV/Metrics → Risk Management) is deliberate: a drawdown policy
that only observes NAV without being able to throttle subsequent sizing is not
actually a risk control, just a dashboard. This mirrors a pattern already proven in
the private Quant Found production system (a multiplicative risk-scale factor
applied at the sizing layer) — see `docs/quant_found_mapping.md`, "Risk management".

Two competition-specific facts, confirmed against the official Регламент, shape
this flow directly:

- **NAV/Metrics should exclude corporate-action price gaps from realized
  drawdown/return, matching the Organizer's own scoring convention** (Регламент
  п. 2.18) — if this project's own metrics adjusted for those gaps differently
  from how the competition scores them, internal metrics and competition
  standing could diverge for reasons unrelated to the strategy itself.
- **The Nomination 1 scoring formula will never be disclosed, by design**
  (Регламент п. 2.20 — Organizer's sole discretion, not provided even on
  request). This is why Risk Management and Metrics are not designed around
  optimizing one guessed formula — see the separate risk-design work's
  score-robustness analysis for the actual approach (checking which portfolio
  properties hold up across several plausible scoring functions).

## Component → package mapping

| Stage | Package | Status |
|---|---|---|
| Market Data | `src/wsc_alpha/data/` | New component. No implementation. |
| Universe | `src/wsc_alpha/universe/` | New component. No implementation. |
| Features | `src/wsc_alpha/features/` | New component. No implementation. |
| Alpha Discovery / Candidates | `src/wsc_alpha/alpha/` | New component. No implementation, no strategy logic disclosed. |
| Portfolio Construction / Market Neutralization | `src/wsc_alpha/portfolio/` | New component. No implementation. |
| Risk Management | `src/wsc_alpha/risk/` | New component (existing private risk engines' *state-machine pattern* is a reference, thresholds are not — see mapping doc). No implementation. |
| Execution | `src/wsc_alpha/execution/` | Interface stub only (`arena_adapter.py`) — no real Arena API calls. |
| NAV / Metrics | `src/wsc_alpha/metrics/` | New component. No implementation. Flagged as highest priority — see mapping doc. |
| Orchestration | `src/wsc_alpha/runtime/` | New component. No implementation. No live/paper mode exists. |
| Backtest | `src/wsc_alpha/backtest/` | New component (fill-timing *philosophy* reused from private historical replay engine, implementation is not). No implementation. |

## What's built from scratch vs. adapted from Quant Found

**Built from scratch (no equivalent in the private production system, or the private
equivalent is explicitly not reusable):**
- Market data layer (different broker/market entirely — Arena API / US equities vs.
  Tinkoff / MOEX).
- Universe filters (different universe, different filter criteria).
- Beta/sector-beta factor model (nothing in production computes portfolio-level
  beta today).
- Alpha Idea / Leg / Cluster abstraction (production hard-codes 2-leg pairs, not a
  general idea model).
- Daily NAV / metrics pipeline (confirmed absent from production — see mapping doc).
- Vol-targeted, beta-adjusted position sizing formula (production uses a simple
  `weight × equity / price` formula with no vol-awareness).

**Patterns worth adapting from Quant Found's *architecture* (not its code, per
`docs/quant_found_mapping.md`'s explicit "nothing here was copied" note):**
- Broker-agnostic order-lifecycle state machine shape (`execution_fsm.py`'s
  transition model).
- Retry/timeout/shared-pool discipline around external API calls (`broker_retry.py`'s
  pattern, itself hardened this session after a real production incident).
- Graduated mismatch-escalation ladder for reconciliation (transient → persistent →
  chronic, not an immediate hard stop on the first discrepancy).
- Multi-sink, level/logger-filtered logging architecture (`logging_setup.py`).
- Startup-time reconciliation-before-trading discipline (`recovery_engine.py`'s
  principle).

## Explicitly out of scope for this document / this stage

- No strategy signal logic.
- No live or paper Arena connection.
- No backtest results.
- No final numeric risk parameters (see `config/wsc_alpha.example.yaml` — all
  marked `TBD`/`TODO`/`UNKNOWN` deliberately).
