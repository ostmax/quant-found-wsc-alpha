# Quant Found WSC Alpha

**Status: Research / Development.**

Research/development project for **Финам «Уолл-стрит код: битва алготрейдеров»**,
Nomination 1 («Альфа»).

Separate project from Quant Found's private production system — not an export or
fork. No production code, credentials, trading history, or proprietary strategy
parameters are included. See `docs/quant_found_mapping.md` for what (if anything)
is architecturally informed by the private system.

## Design goal (not yet demonstrated)

The intended approach, none of it built or validated yet:

- Relative statistical inefficiencies across a filtered universe of liquid US
  common stocks and broad-market-index-tracking ETFs (see
  `docs/competition_rules.md`, п. 2.6, for the exact eligibility criteria).
- **Market-neutral** construction: sizing/hedging aimed at near-zero persistent
  exposure to the broad market and to individual GICS sectors — a design target,
  not a property this repository has measured or proven.
- **Volatility-aware**, equity-scaled position sizing — not fixed notional.
- Portfolio-level risk management: exposure/beta/concentration limits, staged
  drawdown response.
- Automated execution through the competition's **Arena API**, once implemented.

Data flow and reuse rationale: `docs/architecture.md`, `docs/quant_found_mapping.md`.

## What this repository does not claim

- No alpha signal or strategy logic is disclosed (Регламент п. 2.16 keeps
  strategies private between participants; this stage is architecture-only
  regardless).
- No backtest has been run — no performance numbers anywhere in this repo.
- No market-neutrality has been demonstrated — it's the design's stated goal
  (see "Design goal" above), not a measured or validated property.
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

- [`docs/competition_rules.md`](docs/competition_rules.md) — rules sourced from
  the official Регламент (read in full 2026-08-31), cited by clause number.
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
