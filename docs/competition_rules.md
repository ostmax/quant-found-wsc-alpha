# Competition Rules — Финам «Уолл-стрит код: битва алготрейдеров»

**Source: official Регламент Конкурса**, утверждён приказом АО «ФИНАМ» от
01.09.2026 № ФИН/ПР/260901/1, 7 страниц. Read in full 2026-08-31. Every rule below
cites its clause number. This replaces the earlier version of this file, which was
based only on an operator paraphrase and has now been fully superseded — nothing
below is guessed or carried over unverified from that draft.

Organizer: АО «Инвестиционная компания «ФИНАМ» (АО «ФИНАМ»), ОГРН 1027739572343.
Competition site: https://collab.finam.ru/wsc/. The Regulation itself states the
Organizer may amend it unilaterally at any time, effective on publication (п. 6.5)
— this document should be re-checked against the live Регламент page before the
competition ends, not treated as permanently fixed.

**Nomination scope of this document:** Nomination 1 «Альфа». Rules specific to
Nomination 2 «Бета» and Nomination 3 «Ручной трейдинг» are noted only where needed
to avoid confusing them with Nomination 1's terms (starting capital differs, for
example).

---

## Dates

| Item | Value | Clause |
|---|---|---|
| Overall competition period | 01.09.2026 — 30.11.2026 | title table |
| Registration window | 01.09.2026 — 23.11.2026 | п. 2.3 |
| **Actual trading period** (виртуальные биржевые торги) | **28.09.2026 16:30 МСК — 23.11.2026 23:00 МСК** | п. 2.3 |
| Results / winners announced | 30.11.2026 (by 23:59 МСК per п. 3.3) | п. 2.3, п. 3.3 |
| Nomination 1/2 max participation length | **≤ 8 weeks**, within the trading period above | п. 2.4 |
| Nomination 3 max participation length | ≤ 2 weeks from registration, no later than 11.10.2026 | п. 2.4 |

Note: 28.09.2026 → 23.11.2026 is exactly 8 weeks (56 days) — so for Nomination 1,
the "≤ 8 weeks" cap and the overall trading-period window are effectively the same
window; there is no meaningful flexibility to start later and still get a full 8
weeks.

## Nomination 1 «Альфа»

> «Альфа»: демонстрация навыков с помощью алгоритмических стратегий, нацеленных
> на генерацию дохода независимо от динамики рынка. — п. 1.3

This is the Regulation's own definition of "alpha" for this competition: return
generation independent of market direction. It does not define a scoring formula
(see "Rating methodology" below — none is disclosed, by design).

## Permitted instruments (п. 2.6)

Two eligible instrument types, **not a fixed enumerated list** — eligibility is
criterion-based, and the actual live-tradable set is served dynamically via the
Arena API and can change without notice (see below):

1. **Common stock** («common stock») эмитентов, включённых в список ценных бумаг,
   допущенных к организованным торгам («listed securities») на одной или
   нескольких зарегистрированных национальных фондовых биржах США, в том числе
   NYSE и/или NASDAQ.
2. **ETF shares** whose portfolio is constructed to track a **broad U.S. market
   index** (broad-based U.S. market index) — examples given: S&P 500, Dow Jones
   Industrial Average, Russell 3000 "и аналогичных" (and similar) — listed on one
   or more registered U.S. national stock exchanges.

**Correction from the previous draft of this file**: that draft treated "the
permitted ETF list" as an unpublished-but-fixed list waiting to be discovered. The
Regulation does not define a fixed list at all — eligibility is a *criterion*
(tracks a broad market index), and the actual current tradable set is only
available live, via the Arena API instrument endpoint below.

**Live instrument list**: https://api.finam.ru/docs/rest/#assetsservice_assets
(п. 2.6). **The Organizer may change the permitted instrument list at any time
without prior notice to participants** (п. 2.6, explicit).

Orders referencing instruments outside the current list, or with a malformed
ticker, or on a non-permitted venue are rejected without execution (п. 2.8).

## Ticker format (п. 2.7)

`SYMBOL@MIC` — `SYMBOL` is the instrument's ticker on the relevant exchange, `MIC`
is its market identifier code per international standard. **The Regulation's own
example: `AAPL@XNYS`.** (Previous drafts of this repo's code used `AAPL@XNAS` as an
illustrative example — corrected to match the Regulation's literal example.)

## Starting capital (п. 2.9)

- **Nomination 1 / Nomination 2**: **1,000,000,000 (one billion) virtual rubles**,
  per virtual account, credited on the first day that account is opened.
- Nomination 3 (not this repo's scope): 1,000,000 USD virtual-ruble equivalent at
  the Bank of Russia's official rate on the account's opening date — different
  from Nomination 1, noted here only to avoid conflating the two.

Each participant gets up to 3 virtual accounts auto-opened across their chosen
nominations (п. 2.2); if 4+ accounts end up open, only the 3 opened earliest count
for results (п. 2.2). The exact allocation of the "up to 3" across multiple
nominations is not fully spelled out in the text — **UNKNOWN**, not load-bearing
for a Nomination-1-only participant.

## Commission (п. 2.10)

**0.1%** of trade value, for trades on any of these MICs:
`PINX` (OTC Markets Pink Open Market), `XASE` (NYSE American), `XNCM` (NASDAQ
Capital Market), `XNGS` (NASDAQ Global Select Market), `XNMS` (NASDAQ Stock
Market), `XNYM` (New York Mercantile Exchange), `XNYS` (New York Stock Exchange),
`XCME` (Chicago Mercantile Exchange), `BATS` (Better Alternative Trading System),
`ARCX` (NYSE Arca), `XCEC` (Commodities Exchange Center) — **all 11 listed MICs
carry the same 0.1% rate**; no other commission tier appears anywhere in the
Regulation. Note `XNYM`/`XCME`/`XCEC` are commodity/futures venues, not relevant
to Nomination 1's actual instrument universe (п. 2.6, stock + ETF only) — likely
listed for completeness across all of Finam's Arena API products, not specific to
this nomination.

## Market data / pricing (п. 2.13, п. 2.11)

- Trade price is based on market quotes **delayed 15 minutes** relative to real
  time (п. 2.13) — confirmed.
- Trading hours are set individually per instrument, per that exchange's own
  schedule, served via
  https://api.finam.ru/docs/rest/#assetsservice_schedule (п. 2.11). Orders
  outside an instrument's trading hours, or outside the competition's trading
  period, are rejected without execution (п. 2.12).

## Automated trading tools (п. 2.5)

> В рамках виртуальной торговли в Номинации 1 и Номинации 2 участникам Конкурса
> разрешается использовать автоматизированные технические решения, включая
> программное обеспечение ZipLime.

Automated technical solutions are explicitly permitted, with "ZipLime" software
named as one example — not a requirement to use it, and not otherwise defined in
the Regulation. **UNKNOWN** whether ZipLime is a Finam-provided tool relevant to
this project or unrelated third-party software; not investigated further, not
assumed either way.

## End of competition (п. 2.17, п. 2.18)

- **All open positions are automatically closed** at the price of the last virtual
  trade registered on the relevant venue, on the competition's last trading day
  (per the nomination-specific deadlines in п. 2.3/2.4) — confirmed, п. 2.17.
- **Corporate-action-driven price gaps are excluded from result/return
  calculations** (п. 2.18) — new information not previously captured: the
  Organizer's own scoring does not penalize/reward a position for a split/
  dividend/other corporate-action price discontinuity.

## Rating methodology — explicitly undisclosed (п. 2.19, п. 2.20)

- **Nomination 1 / Nomination 2**: "Рейтинг участников Конкурса... формируется по
  единоличному решению Организатора Конкурса, которое принимается им
  самостоятельно. **Методика определения указанного рейтинга участников Конкурса
  не подлежит раскрытию и не предоставляется по запросам участников Конкурса и
  третьих лиц.**" (п. 2.20) — the Organizer's sole discretion, method never
  disclosed, not obtainable on request, even after the fact.
- Nomination 3 (not this repo's scope) uses a disclosed return-% ranking with a
  max-drawdown tiebreak (п. 2.19) — structurally different from Nomination 1 and
  not a proxy for how Nomination 1 is scored.
- This confirms — as a regulatory fact, not merely a design assumption — that no
  scoring formula for Nomination 1 will ever be published. The private research
  work informing this project's risk design already treats this as a given
  (multiple plausible score functions checked for robust common properties,
  rather than guessing one true formula) — this clause is why that approach is
  the right one, not just a cautious hedge.

## Strategy confidentiality / partial leaderboard visibility (п. 2.16)

Strategies (technical solutions — trading algorithms) run by participants are
**not disclosed or displayed to other participants or third parties** during the
competition. **Only the top-10 participants by return are visible** on the public
leaderboard, showing their current standing **without strategy detail**
(https://collab.finam.ru/competitions, п. 2.15/2.16).

## Restrictions on using competition data (п. 2.21)

Participants may use information obtained about trading activity during the
competition **only for competition purposes**. They may not redistribute or
broadcast it, may not use it to compute derivative information intended for
public distribution, and — explicitly — **this information may not be used to
make investment decisions in real trading of financial instruments or currency.**

## Additional checks / suspicious-trade monitoring (п. 2.23, гл. 4)

- The Organizer may conduct **additional checks** of participants' actions, trades,
  and results for compliance with the rules, on the Arena API virtual platform
  (п. 2.23).
- A **3-person judging committee** (сотрудники АО «ФИНАМ») separately monitors for
  price manipulation or non-standard trades ("Подозрительные сделки" — Suspicious
  Trades). If found to be intentional and aimed at influencing results, the
  committee may exclude the participant (гл. 4, п. 4.1–4.2). Committee decisions
  are published within 3 business days (п. 4.3).

## Disqualification grounds (п. 6.3, п. 2.22)

Explicit grounds for disqualification: reasonable suspicion of bad-faith conduct;
false/incomplete/erroneous/incorrect/inaccurate submitted information; creating
multiple accounts; manipulating the system or exploiting Arena API / virtual
platform bugs; collusion between participants; any form of fraud or unfair
advantage (п. 6.3). Violating contest procedure separately costs the participant
prize eligibility and the ability to re-participate (п. 2.22).

## Authorship requirement (п. 1.8) — read carefully, see note below

> Направляя техническое решение (торговые алгоритмы) для участия в Конкурсе,
> участник Конкурса гарантирует Организатору Конкурса, что техническое решение
> **создано автором лично** и **не является следствием плагиата**, **не нарушает
> прав и законных интересов третьих лиц в сфере защиты интеллектуальной
> собственности**. В случае нарушения участником Конкурса указанных гарантий,
> участник Конкурса обязуется возместить Организатору Конкурса все понесенные им
> убытки в полном объеме.

Exact requirements: (1) the technical solution was created by the author
personally, (2) it is not the result of plagiarism, (3) it does not infringe
third parties' intellectual-property rights. **The clause does not mention AI
tools, AI-assisted development, or code-generation assistants anywhere, in either
direction** — it neither permits nor prohibits them by name.

**This is flagged as a potential conflict requiring the repository owner's own
judgment, not resolved here** — see the standalone note at the end of this
document and the project's audit history for the full context. Nothing in this
project asserts compliance or non-compliance with п. 1.8.

## License grant to the Organizer (п. 1.5–1.7)

By submitting a technical solution for Nomination 1/2, the participant grants the
Organizer a **limited, royalty-free license** for the competition's duration only:
right to store it in Organizer databases, load it, test it "всеми возможными
способами" (by any means, at the Organizer's discretion), and publicly demonstrate
completed trades and derived data based on them. **The license expires at contest
end**; the Organizer then loses all rights to use it and, on the participant's
request, must delete it from its systems and destroy any media containing it
(п. 1.6). Territory: Russian Federation (п. 1.7).

## Arena API (п. 2.1, п. 2.2)

- "Finam Arena API" — an open programmatic interface, access provided free of
  charge by the Organizer, used to submit virtual trade orders against a virtual
  Конкурсный счёт (Competition Account).
- Access is via a **unique individual generated token** ("api_token"), issued in
  the participant's Личный кабинет (Personal Account) after registration, used via
  a POST request (п. 2.2).
- Confirmed documentation endpoints referenced by the Regulation itself:
  - Instruments: https://api.finam.ru/docs/rest/#assetsservice_assets
  - Trading schedule: https://api.finam.ru/docs/rest/#assetsservice_schedule
  - No order-submission/account/position endpoints are named in the Regulation
    text itself — see Open Items below.

## No post-competition reports (п. 6.6)

> Предоставление отчетов и технических (статистических) данных (информации) о
> работе Arena API и виртуальной торговой платформы Организатора в рамках участия
> в Конкурсе не предусмотрено. Организатор не предоставляет какие-либо выписки по
> виртуальному счету, отчеты о виртуальных сделках, совершенных в рамках Конкурса,
> а также иные документы, связанные с проверкой таких сделок и операций.

Confirmed exactly as previously understood: no account statements, trade reports,
or audit documents are provided by the Organizer after the fact, for any purpose.

## System risk / liability (п. 6.1, п. 6.2, п. 6.4)

The Organizer disclaims liability for system risks (equipment/software/
connectivity/power failures) beyond making "all possible efforts" to fix them
(п. 6.1), does not reimburse participation-related losses or costs (п. 6.2), and
may end or pause the competition at any time without notice or explanation
(п. 6.4) — early termination is explicitly not grounds for a claim.

---

## Explicitly UNKNOWN / NEEDS API VERIFICATION

Nothing below is guessed. Each item was checked against the full 7-page Regulation
and is absent from it.

- **Exact Alpha scoring formula** — not merely undiscovered: п. 2.20 confirms the
  Organizer will never disclose it, by design, even on request.
- **Whether short-selling is permitted** — not mentioned anywhere in the
  Regulation.
- **Whether margin/leverage is available** — not mentioned anywhere.
- **The concrete, current tradable universe** — only available live via
  `assetsservice_assets`; not enumerated in the Regulation and can change without
  notice (п. 2.6).
- **Full list of "broad U.S. market index" ETFs beyond the three named examples**
  (S&P 500, DJIA, Russell 3000 "и аналогичных") — the "и аналогичных" (and
  similar) qualifier is not further defined.
- **Order-submission, account, and position API endpoints** — the Regulation only
  names the instrument-list and schedule endpoints; trading-operation endpoints
  require reading the full Arena API REST documentation at
  https://api.finam.ru/docs/rest/ directly (not done as part of this
  documentation-only task).
- **Whether "ZipLime" (п. 2.5) is relevant to this project** — named only as an
  example of permitted tooling, not otherwise described.
- **Exact allocation of "up to 3" virtual accounts across multiple nominations**
  (п. 2.2) — not load-bearing for a Nomination-1-only participant.

---

## ⚠️ Flagged, not resolved: AI-assisted development vs. п. 1.8

This repository, including its architecture, documentation, and this file itself,
has been produced with the assistance of Claude Code (an AI coding tool) across
multiple sessions. That fact is disclosed, not hidden — see this project's git
history and its prior audit report (kept privately, not in this public repo).

**п. 1.8 requires the technical solution to be "создано автором лично" (created
by the author personally), not the result of plagiarism, and not infringing
third-party IP rights.** The clause does not address AI-assisted development
either way. Whether AI-assisted development is consistent with "personal
authorship" under this clause is a genuine interpretive question this document
does not attempt to answer — it depends on legal/competition judgment this
project cannot supply. The repository owner should form their own view of this,
and may wish to confirm directly with the Organizer (АО «ФИНАМ», contacts in the
Regulation's header) before submitting a technical solution for Nomination 1,
rather than rely on an inferred answer.
