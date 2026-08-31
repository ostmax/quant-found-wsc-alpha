# Competition Rules — Финам «Уолл-стрит код: битва алготрейдеров»

**Nomination:** 1 «Альфа» (Alpha).

## ⚠️ Sourcing note — read before relying on this document

This file was requested to cite, for every rule, "источник: пункт Регламента"
(the specific clause of the official competition Regulation). **The primary
Regulation document itself was not available to produce this file** — it was not
found anywhere in this session's context or on the local filesystem, despite the task
description stating it had been provided earlier.

Everything below is instead sourced from the **rules list given directly by the
operator in the task prompt that requested this document** (2026-08-31). That list is
treated here as a good-faith summary, not as the primary source — **no specific
clause/paragraph numbers are cited**, because none were available to verify against.

**Before this document is treated as authoritative for any configuration or strategy
decision, the actual official Regulation (Регламент) should be supplied and this file
re-verified against it, with real clause citations replacing the placeholder below.**

---

## Confirmed rules (as relayed by the operator — pending primary-source verification)

| # | Rule | Source (as available) |
|---|---|---|
| 1 | Nomination: **Alpha** («Альфа») | Operator-relayed summary, 2026-08-31 |
| 2 | Tradable universe: **US listed common stocks** | Operator-relayed summary, 2026-08-31 |
| 3 | Plus a set of **permitted broad-market ETFs** (exact list not yet specified) | Operator-relayed summary, 2026-08-31 — **UNKNOWN**: the actual permitted ETF list is not available; treated as TBD until confirmed |
| 4 | Execution via the **Arena API** | Operator-relayed summary, 2026-08-31 — **UNKNOWN**: no API documentation reviewed yet; see `src/wsc_alpha/execution/arena_adapter.py` for the resulting interface stub |
| 5 | Ticker format: **`SYMBOL@MIC`** | Operator-relayed summary, 2026-08-31 |
| 6 | Starting virtual capital: **1,000,000,000 ₽** (1 billion rubles) | Operator-relayed summary, 2026-08-31 |
| 7 | Commission: **0.1%** for the relevant US MIC(s) | Operator-relayed summary, 2026-08-31 — exact MIC list not specified |
| 8 | Market pricing: **15-minute delayed** | Operator-relayed summary, 2026-08-31 |
| 9 | Trading period: **maximum 8 weeks** | Operator-relayed summary, 2026-08-31 |
| 10 | All open positions are **automatically closed at competition end** | Operator-relayed summary, 2026-08-31 |
| 11 | The organizer may **change the list of permitted instruments** during the competition | Operator-relayed summary, 2026-08-31 |
| 12 | Participants' strategies are **not disclosed to other participants** | Operator-relayed summary, 2026-08-31 |
| 13 | The organizer **may conduct additional checks/audits** | Operator-relayed summary, 2026-08-31 |
| 14 | **No post-competition reports/statements** for the virtual account are provided by the organizer | Operator-relayed summary, 2026-08-31 |

## Explicitly not fabricated

Per the task's own instruction ("Не придумывай дополнительные правила"), no rule
beyond the 14 above is recorded here — no assumptions about leverage, short-selling
permissions, order types, position limits, scoring formula, disqualification
conditions, or anything else not explicitly listed above. Where this repository's
other documents (README, architecture, config) need to reference such a detail, they
mark it `TODO` / `UNKNOWN` / `TBD` rather than infer it from this list.

## Open items requiring the primary Regulation document

- Exact clause numbers for each rule above (currently unavailable).
- Full permitted-ETF list (item 3).
- Arena API authentication/endpoint documentation (item 4).
- Full US MIC list the 0.1% commission applies to (item 7) — and whether any other
  commission tier exists for MICs not covered by it.
- Whether short-selling is permitted, and under what constraints.
- Whether leverage/margin is available on the virtual account.
- The exact competition start/end dates for this specific run.
- The actual scoring formula (the task explicitly says not to guess it —
  see the separate risk-design work's §2.2 sensitivity-analysis approach for how this
  repository's risk philosophy handles that uncertainty without guessing).
