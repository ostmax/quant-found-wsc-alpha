# Quant Found → WSC Alpha: Architecture Mapping

**Type:** read-only architectural audit of the private production Quant Found
codebase, performed to decide what can inform `quant-found-wsc-alpha`.
**Scope of this document:** analysis only. No production code is copied into this
repository by this document; nothing here changes production.
**Method:** direct source review of the private codebase (not documentation, not
memory) — file paths below are as they exist in the private repo and are not
included in this public repository.

For each area: where it lives privately, what it does, and a verdict:
`REUSE` / `REUSE WITH MODIFICATION` / `DO NOT USE` / `UNKNOWN`.

This mapping is deliberately narrower than the one prepared for the earlier
`WSC_ALPHA_RISK_SPEC.md` risk-design exercise — this file focuses only on
"what to build the public repo's skeleton around," not the full risk-parameter
design (see that spec's own §17 for the fuller reuse table if useful context is
ever needed for private-side work; it is not published here).

---

## Market data components

**Location (private):** `market_data_layer.py`, `price_engine.py`, `price_stream.py`,
`price_bus.py`, `microbar_ingress.py`, `history_collector.py`.

**What it does:** a streaming market-data layer built directly on the Tinkoff Invest
gRPC API (`tinkoff.invest.Client`, `SubscribeLastPriceRequest`,
`SubscribeOrderBookRequest`) for MOEX instruments, plus a companion historical
microbar collector.

**Verdict: DO NOT USE.**
Hard-coupled to a specific Russian broker's gRPC SDK and MOEX instruments. WSC Alpha
needs a completely different data path (US equities, delayed pricing per the
competition rules, Arena API — see `docs/competition_rules.md`). Nothing in this
layer is broker-agnostic enough to adapt; a new market data component is required
from scratch (`src/wsc_alpha/data/`).

## Feature engine

**Location (private):** `feature_engine.py`, `stock_feature_engine.py`,
`microstructure_engine.py`, `matrix_vol_engine.py`, `market_factor_engine.py`.

**What it does:** computes features from `data/raw/history.parquet` (a MOEX
tick-shaped file), tightly coupled to that file layout and to microstructure-scale
signals appropriate for the production system's much faster trading cadence.

**Verdict: DO NOT USE** (implementation) / **UNKNOWN** (concepts worth revisiting).
The concrete feature computations assume tick/microbar-resolution MOEX data that
doesn't exist for WSC Alpha's universe or timeframe. Whether any of the underlying
*statistical techniques* (not the code) generalize to a daily/multi-day US-equity
factor-residual feature set is not yet evaluated — marked `UNKNOWN`, not assumed
either way.

## Alpha engines

**Location (private):** `pair_alpha_engine.py`, `orthogonal_alpha_engine.py`,
`meta_alpha_engine.py`, `genetic_alpha_engine.py`, `portfolio_alpha_engine.py`,
`gap_fade_engine.py`, `cnru_scalp_engine.py`, `alpha_v11.py`.

**What they do:** a family of MOEX-specific alpha generators — statistical pairs
cointegration (`pair_alpha_engine.py`), a single-instrument gap-fade directional
strategy with a fixed-notional/fixed-stop design (`gap_fade_engine.py`), and several
exploratory/meta engines.

**Verdict:**
- `pair_alpha_engine.py`'s **filter-cascade pattern** (sequential quality gates —
  correlation → cointegration test → z-score → regime filter — before a candidate is
  considered tradable) is a reasonable **template** for how to structure an
  alpha-candidate pipeline: **REUSE WITH MODIFICATION** (pattern only; the actual
  filters — ADF cointegration, short-window z-score — are pairs-trading-specific and
  do not transfer to a factor-residual signal).
- `gap_fade_engine.py`: **DO NOT USE.** Fixed-notional sizing (not equity-scaled) and
  a single-instrument directional design are exactly the pattern the WSC market-
  neutral objective needs to avoid, not adapt.
- `orthogonal_alpha_engine.py` / `meta_alpha_engine.py` / `genetic_alpha_engine.py` /
  `alpha_v11.py`: **UNKNOWN.** Not reviewed in depth for this pass; flagged for a
  later, more thorough look before ruling in or out — not assumed reusable by
  default.

## Pair / statistical arbitrage components

**Location (private):** `pair_selection_engine.py`, `pair_target_engine.py`,
`pair_metrics_engine.py`, `pair_position_engine.py`, `pair_rebalance_engine.py`,
`pair_key_manager.py`, `pair_statistics_cache.py`, `cointegration_calibrator.py`,
`hybrid_leg_manager.py`, `hybrid_lifecycle.py`.

**What it does:** a full statistical-arbitrage pairs-trading stack — candidate
generation via ADF cointegration test over MOEX instrument pairs, z-score entry/exit,
half-life filtering, and (in `hybrid_leg_manager.py`) a substantial amount of
production-hardened logic for managing a pair whose two legs fill asymmetrically or
close independently.

**Verdict: DO NOT USE** (as a strategy) / **UNKNOWN, worth a deeper look separately**
(the *execution-robustness* lessons inside `hybrid_leg_manager.py`).
Statistical pairs trading (cointegration-based) is a different strategy paradigm from
the factor-residual, market-neutral approach this competition's brief points toward
(see `WSC_ALPHA_RISK_SPEC.md`, not part of this repo) — not reused directly. However,
the *problem* `hybrid_leg_manager.py` solves (a 2-leg idea whose legs fill/close
independently, needs one clean owner of "is this idea still market-neutral right
now") is a problem the Alpha Idea/Cluster abstraction (§10 of the risk spec) will
also face — worth a dedicated future review, not a blanket reuse decision today.

## Portfolio construction

**Location (private):** `portfolio_builder.py`, `portfolio_builder_v1.py`,
`portfolio_builder_5m_v2.py`, `portfolio_5m.py`, `allocation_engine.py`,
`rebalance_engine.py`.

**What it does:** several generations of a MOEX portfolio construction/rebalance
layer, sized against `instrument_registry.py`'s fixed 44-45-instrument universe.

**Verdict: UNKNOWN.**
Not reviewed in enough depth this pass to give a confident verdict either way — the
general shape (target-weight → rebalance-order generation) is a common pattern, but
whether any specific implementation detail is worth adapting (vs. building fresh
against a ~250-500 name US universe) needs a dedicated read before deciding. Not
assumed reusable.

## Sizing

**Location (private):** `sizing_engine.py`.

**What it does:** `SizingEngine.compute_target_qty()` implements
`target_qty = (weight × equity) / price`, lot-aligned; also handles effective-position
netting against in-flight executions (`get_effective_position()`), and a pair-specific
notional-matching helper (`align_pair()`).

**Verdict: REUSE WITH MODIFICATION.**
The **structure** — lot alignment, netting current position against pending
executions before computing a delta order, a clean `weight → target_qty` seam — is
broker-agnostic and well-designed. The **formula itself** (`weight × equity / price`)
is a simple weight-based sizer with no volatility-awareness; WSC Alpha needs a
vol-targeted, beta-adjusted sizing formula instead (see the separate risk-design
work), so the formula is replaced while the surrounding scaffolding is kept.

## Risk management

**Location (private):** `risk_engine.py`, `risk_guard.py`,
`portfolio_risk_engine.py`, `risk_engine_production.py`, `risk_utils.py`.

**What it does:** three parallel, independently-evolved risk layers exist in
production simultaneously:
- `risk_guard.py` — a kill-switch / network-degraded-mode state machine (equity
  drawdown thresholds, market-data staleness, cycle-latency, reconciliation-mismatch
  escalation).
- `risk_engine.py` (`RiskEngine`, logger name `risk_engine_v23`) — a separate
  gross/net/per-instrument exposure FSM (`TRADING`/`REDUCE_ONLY`/`STOP`/`KILL`) with
  its own, different drawdown thresholds than `risk_guard.py`.
- `portfolio_risk_engine.py` — a third, standalone risk-limit class
  (`MAX_TICKER_EXPOSURE`, `MAX_GROSS`, `MAX_NET`, `CORR_THRESHOLD`, `DD_LIMIT`) that
  is **not imported anywhere in the production codebase** — confirmed dead code.
- `risk_engine_production.py` — also confirmed unused/dead code, superseded by
  `risk_engine.py`.

**Verdict:**
- `risk_guard.py`: **REUSE WITH MODIFICATION.** The kill-switch/network-degraded
  state-machine *architecture* is sound (and was hardened this session against a
  real production incident — a hung broker call that froze the whole process for
  3h43min with no external supervision). Every numeric threshold and the
  Tinkoff-specific call sites need full replacement for a new broker/market.
- `risk_engine.py`: **REUSE WITH MODIFICATION**, same caveat — the FSM shape
  (mode transitions, per-instrument exposure check, scale-down-not-just-stop) is
  reusable structure; thresholds are production-MOEX-specific and not a reference
  point for WSC Alpha's own limits.
- `portfolio_risk_engine.py`, `risk_engine_production.py`: **DO NOT USE.** Both
  confirmed dead code in production — not a validated design, just an abandoned
  draft; their specific threshold values (e.g. `MAX_GROSS = 1.5`) are not evidence of
  anything and are not referenced as targets for WSC Alpha.
- Notably: **none of the three** compute portfolio-level market beta or sector beta.
  A beta/sector-beta risk engine is a genuinely new component for WSC Alpha
  regardless of which existing engine's FSM pattern is reused.

## Execution

**Location (private):** `execution_router.py`, `execution_engine.py`,
`execution_fsm.py`, `execution_fills.py`, `execution_retry.py`,
`execution_runtime.py`, `execution_finalize.py`, `execution_journal.py`,
`execution_monitor.py`, `broker_submitter.py`, `broker_retry.py`,
`broker_live_adapter_tbank.py`, `broker_utils.py`, `order_executor.py`,
`order_status_updater.py`.

**What it does:** a full order-lifecycle stack over the Tinkoff broker API: FSM-based
execution state tracking, retry/timeout wrapping around every broker call, fill
polling/reconciliation, and a router that dispatches rebalance orders to the broker
adapter.

**Verdict:**
- `execution_fsm.py`: **REUSE.** A genuinely broker-agnostic order lifecycle state
  machine (`NEW → PARTIAL → FILLED_OPEN → CLOSING → CLOSED/FAILED/DESYNC`, plus
  quarantine/retry states). Its core transitions do not assume anything MOEX- or
  Tinkoff-specific; a few pair-lifecycle-specific states (`PARTIAL_PAIR`,
  `RECOVERY_HOLD`) would be dropped if unneeded, not the whole module.
- `broker_retry.py`: **REUSE WITH MODIFICATION.** The retry/timeout/shared-pool
  pattern (bounded worker pool, abandoned-call tracking, network-vs-internal error
  classification) is broker-agnostic and was itself hardened this session after a
  real production incident (a `ThreadPoolExecutor`-per-call design that leaked
  threads and let a dead connection hang the whole process). The pattern transfers
  cleanly to a new broker adapter; the Tinkoff-specific exception types it classifies
  do not.
- `execution_router.py` / `execution_engine.py` / `execution_retry.py` /
  `execution_runtime.py` / `execution_finalize.py`: **REUSE WITH MODIFICATION.** The
  overall shape (route → submit → poll → reconcile → finalize, with a documented
  network-degraded-mode carve-out so a broker outage doesn't trip a hard kill switch)
  reflects real, hard-won production lessons and is worth keeping as an architectural
  reference; the implementation is Tinkoff-specific throughout and needs a new
  adapter underneath, not a port.
- `broker_live_adapter_tbank.py`, `order_executor.py`, `order_status_updater.py`:
  **DO NOT USE** as implementations (Tinkoff-specific), but see the note under
  "Arena API adapter" in `docs/architecture.md` — the same *shape* of adapter
  (get_positions / get_orders / submit_order / cancel_order boundary) is the model
  for `src/wsc_alpha/execution/arena_adapter.py` in this repo.

## Reconciliation

**Location (private):** `broker_reconciliation_engine.py`, `reconciliation_engine.py`,
`reconciliation.py`, `execution_reconciliation_engine.py`, `position_reconciliation_engine.py`,
`portfolio_sync.py`, `tbank_reconciler.py`.

**What it does:** compares internal position/execution state against the broker's own
reported state, with a graduated escalation ladder
(`MISMATCH_GRACE_SEC=30 → MISMATCH_DESYNC_SEC=300 → MISMATCH_REVIEW_SEC=1800`,
transient → persistent-desync-flag → chronic-requires-human-review) rather than an
immediate hard stop on the first mismatch.

**Verdict: REUSE WITH MODIFICATION.**
The escalation-ladder *philosophy* — don't panic on one transient mismatch, escalate
progressively, require a human at the "chronic" tier — is exactly the kind of
production-tested judgment worth keeping. `tbank_reconciler.py` is Tinkoff-specific
and not reusable directly; the general engines need a new broker adapter underneath
but the same escalation structure.

## Recovery

**Location (private):** `recovery_engine.py`, `startup_integrity_validator.py`,
`runtime_state.py` (startup-validation section), `recover_microbars.py`,
`pair_entry_recovery.py`, `single_leg_recovery_manager.py`,
`network_recovery_coordinator.py`, `network_failure_classifier.py`.

**What it does:** startup-time reconciliation against the broker before allowing
trading to begin, plus a network-outage recovery coordinator distinct from the
internal-failure kill switch (`risk_guard.py`'s `NETWORK_DEGRADED` state).

**Verdict: REUSE WITH MODIFICATION.**
The core principle — refuse to start trading until internal state and broker state
are confirmed to agree, and treat network outages as a self-healing, non-fatal
condition distinct from a genuine internal error — is directly relevant and was
concretely validated this session (an actual production restart blocked correctly on
a stale-local-state mismatch against a confirmed-flat broker). The specific
Tinkoff-coupled implementation is not reusable as-is; a new broker adapter is needed
underneath the same startup-validation and network-classification principles.

## Backtesting

**Location (private):** `run_backtest.py`, `backtest_engine.py` (referenced, not
reviewed in this pass), `run_historical.py`, `historical/` package (a large body of
MOEX-microstructure research scripts — `market_grammar.py`, `market_topology.py`,
`phase_origin_study.py`, etc.), `data/historical_runs/` (engine-determinism replay
artifacts).

**What it does:** `run_backtest.py` at the repo root is a minimal, thin script (loads
one parquet, computes simple realized vol, calls a `run()` function) — not a
full-featured point-in-time backtest engine. `run_historical.py` and the
`historical/` package implement a more substantial historical-replay engine with a
`NextOpenExecution` fill model (signal at close(t) → execute at open(t+1)) and a
simulated clock — but this was confirmed, during a prior audit this session, to be an
**engine-determinism validation harness** (checks two replay runs produce bit-for-bit
identical output), not a validated strategy backtest with realized P&L/drawdown/Sharpe
output. One replay run in `data/historical_runs/` shows `n_trades: 0` for its test
window, by design (a warm-up-period smoke test).

**Verdict: DO NOT USE** (implementation) / worth reusing one **philosophy**:
- `run_backtest.py`, `historical/` MOEX-microstructure research scripts: **DO NOT
  USE.** Wrong market, wrong timeframe, and (for the `historical/` package)
  research-exploration code, not a production-grade backtest component.
- The **`NextOpenExecution` fill philosophy** (signal at close(t) → execute at
  open(t+1), avoiding same-bar look-ahead) from `run_historical.py`: **REUSE (as a
  philosophy, not code)** — realistic and appropriate for a days-long-holding, non-HFT
  strategy; a new point-in-time US-equities backtest engine should adopt this fill
  timing convention rather than inventing a different one.
- No component in production computes a validated daily NAV series with drawdown,
  Sharpe, or turnover metrics end-to-end — this is a genuinely new component
  regardless of the above (see `docs/architecture.md`).

## Logging / metrics

**Location (private):** `logging_setup.py`, `log_utils.py`, `summary_logger.py`,
`event_logger.py`, `incident_recorder.py`, `telegram_notifier.py`, `runtime_metrics.py`.

**What it does:** `logging_setup.py` implements a multi-sink logging architecture
(console / `system.log` / `trading.log` / `reconciliation.log` / `debug.log`),
splitting an operator-facing event journal from full DEBUG-level forensic trace by
logger name and level, with an `operator`/`developer` mode switch. `log_utils.py`
provides `log_on_change`/`log_on_material_change`/`should_log_periodic` helpers to
avoid log-spamming identical repeated states. `telegram_notifier.py` is a minimal
`send_message()` wrapper already usable for alerting.

**Verdict: REUSE.**
This layer is broker/market-agnostic by construction — nothing in it assumes MOEX,
Tinkoff, or any specific instrument set. Directly applicable to WSC Alpha with no
Structural changes needed, only new logger names/log files as new components are
built.

**No dedicated "metrics" module was found that computes NAV-based Sharpe/Sortino/
drawdown from a verified daily series** — confirmed in the earlier production-account
audit this session: no trustworthy daily NAV pipeline exists anywhere in the private
codebase today. This is flagged again here because it's the single most-repeated
finding across every audit pass so far and is treated as a new, P0-priority component
for WSC Alpha (see `docs/architecture.md`).

---

## Summary table

| Area | Verdict |
|---|---|
| Market data | DO NOT USE — new component required |
| Feature engine | DO NOT USE (impl) / UNKNOWN (concepts) |
| Alpha engines | Mixed — pattern REUSE WITH MODIFICATION, GapFade DO NOT USE, others UNKNOWN |
| Pair/stat-arb | DO NOT USE (strategy) / UNKNOWN (execution lessons in hybrid_leg_manager.py) |
| Portfolio construction | UNKNOWN — not reviewed in depth |
| Sizing | REUSE WITH MODIFICATION (structure yes, formula no) |
| Risk management | REUSE WITH MODIFICATION (risk_guard.py, risk_engine.py) / DO NOT USE (portfolio_risk_engine.py, risk_engine_production.py — both dead code) |
| Execution | REUSE (execution_fsm.py) / REUSE WITH MODIFICATION (router/engine/retry) / DO NOT USE (Tinkoff adapter impl) |
| Reconciliation | REUSE WITH MODIFICATION |
| Recovery | REUSE WITH MODIFICATION |
| Backtesting | DO NOT USE (impl) / REUSE (NextOpenExecution philosophy only) — new engine required |
| Logging/metrics | REUSE (logging) / new component required (NAV-based metrics) |

**Nothing in this table was copied into `quant-found-wsc-alpha`.** This document is
analysis only, produced from a read-only review of the private repository.
