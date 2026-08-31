# Quant Found WSC Alpha

**Status: Research / Development.**

Algorithmic market-neutral trading system for **Финам «Уолл-стрит код: битва
алготрейдеров»**, Nomination 1 («Альфа»).

Separate project from Quant Found's private production system — not an export or
fork. No production code, credentials, trading history, or proprietary strategy
parameters are included. See `docs/quant_found_mapping.md` for what (if anything)
is architecturally informed by the private system.

## Core idea

- Relative statistical inefficiencies across a filtered universe of liquid US
  common stocks and permitted broad-market ETFs.
- **Market-neutral** construction: positions sized and hedged toward near-zero
  persistent exposure to the broad market and to individual GICS sectors.
- **Volatility-aware**, equity-scaled position sizing — not fixed notional.
- Portfolio-level risk management: exposure/beta/concentration limits, staged
  drawdown response.
- Automated execution through the competition's **Arena API**.

Data flow and reuse rationale: `docs/architecture.md`, `docs/quant_found_mapping.md`.

## What this repository does not claim

- No alpha signal or strategy logic is disclosed (competition rules keep
  strategies private between participants; this stage is architecture-only
  regardless).
- No backtest has been run — no performance numbers anywhere in this repo.
- No live or paper trading is connected — `arena_adapter.py` is an interface
  stub, every method raises `NotImplementedError`, no token referenced.
- Not the private Quant Found repository — none of its trading engines,
  execution stack, or historical data/logs are included.

## Repository layout

```
src/wsc_alpha/       package (see docs/architecture.md for what each submodule owns)
config/              example config — risk/universe parameters marked TBD/UNKNOWN
docs/                competition rules, architecture, Quant Found reuse mapping
research/            research notebooks/scripts (empty at this stage)
tests/               smoke tests
```

## Documentation

- [`docs/competition_rules.md`](docs/competition_rules.md) — confirmed rules, with
  a sourcing caveat (primary Regulation not yet supplied — see file header).
- [`docs/architecture.md`](docs/architecture.md) — intended data flow.
- [`docs/quant_found_mapping.md`](docs/quant_found_mapping.md) — audit of the
  private Quant Found system: what's reusable as pattern, and what isn't.

## Development

```bash
python -m venv .venv
source .venv/bin/activate   # .venv\Scripts\activate on Windows
pip install -e ".[dev]"
pytest
```

`config/wsc_alpha.example.yaml` and `.env.example` are placeholders — copy to
untracked real files before use (see `.gitignore`).

## License

Not yet decided. Public visibility does not imply an open-source grant — no
license should be assumed until a LICENSE file is added.

## Contact

Maxim Ostrovskiy (repository owner).
