# Quant Found WSC Alpha

**Status: Research / Development.**

## Purpose

Algorithmic market-neutral research and trading system developed for the
**Финам «Уолл-стрит код: битва алготрейдеров»** competition, Nomination 1
(«Альфа» / Alpha).

This repository is a clean, public research framework — it is a **separate project**
from Quant Found's private production trading system, not an export or fork of it.
No production code, credentials, live trading history, or proprietary strategy
parameters from the private system are included here. See
`docs/quant_found_mapping.md` for an explicit, published account of what (if
anything) is architecturally informed by the private system, and what is not.

## Core idea

- Search for relative statistical inefficiencies across a filtered universe of
  liquid US listed common stocks and permitted broad-market ETFs.
- Construct a **market-neutral** portfolio: positions are sized and hedged so the
  book carries close to zero persistent exposure to the broad market and to
  individual GICS sectors, rather than relying on general market or sector
  direction for return.
- Size positions in a **volatility-aware**, equity-scaled way — not fixed notional
  amounts.
- Apply **portfolio-level risk management**: exposure limits, beta limits,
  concentration limits, and a staged drawdown-response policy.
- Execute automatically through the competition's **Arena API**.

See `docs/architecture.md` for the intended data flow (Market Data → Universe →
Features → Alpha Discovery → Portfolio Construction → Market Neutralization → Risk
Management → Execution → NAV/Metrics) and `docs/quant_found_mapping.md` for the
architectural audit this design draws on.

## What this repository does *not* claim

- **No specific alpha signal or strategy logic is disclosed here.** Per the
  competition rules (participants' strategies are not disclosed to other
  participants — see `docs/competition_rules.md`), and independent of that rule,
  this stage of the project is architecture only.
- **No backtest has been run.** No performance numbers, Sharpe ratios, drawdown
  figures, or win rates are claimed anywhere in this repository. Any such number
  appearing here in the future will be accompanied by the exact methodology that
  produced it.
- **No live or paper trading is connected.** `src/wsc_alpha/execution/arena_adapter.py`
  is an interface stub — every method is `TODO` and raises `NotImplementedError`. No
  Arena API token is referenced or required by anything in this repository at this
  stage.
- **This is not the private Quant Found repository.** It does not include the
  private system's MOEX pairs/gap-fade/solo trading engines, its live-trading
  execution stack, or any of its historical data, logs, or account records.

## Repository layout

```
src/wsc_alpha/
    data/        market data ingestion (no implementation yet)
    universe/    tradable-universe filtering (no implementation yet)
    features/    market/sector beta + residual features (no implementation yet)
    alpha/       alpha candidate discovery (no implementation yet)
    portfolio/   portfolio construction / market neutralization (no implementation yet)
    risk/        position / portfolio / drawdown risk management (no implementation yet)
    execution/   Arena API adapter boundary (interface stub only)
    backtest/    point-in-time backtest engine (no implementation yet)
    metrics/     daily NAV + performance metrics (no implementation yet)
    runtime/     process orchestration (no implementation yet)

config/          example configuration (all risk/universe parameters TBD/UNKNOWN)
docs/            competition rules, architecture, Quant Found reuse mapping
research/        research notebooks/scripts go here (empty at this stage)
tests/           smoke tests only at this stage
```

## Documentation

- [`docs/competition_rules.md`](docs/competition_rules.md) — confirmed competition
  rules, with an explicit sourcing caveat (the primary Regulation document has not
  yet been supplied to this project — see that file's own warning at the top).
- [`docs/architecture.md`](docs/architecture.md) — intended system data flow.
- [`docs/quant_found_mapping.md`](docs/quant_found_mapping.md) — read-only
  architectural audit of the private Quant Found production system: what could
  potentially be reused (as *pattern*, not code) and what should not be.

## Getting started (development)

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
pytest
```

`config/wsc_alpha.example.yaml` and `.env.example` show the expected configuration
shape. Copy them to real (untracked) files before use — see `.gitignore`. Neither
file currently has real values to copy; both are placeholders pending competition
Regulation confirmation and Arena API documentation.

## License

Not yet decided — see the repository's LICENSE status. This is a public repository,
but public visibility does not by itself imply an open-source license grant; no
license terms should be assumed for any file in this repository until a LICENSE
file is explicitly added.

## Contact

Maxim Ostrovskiy (repository owner).
