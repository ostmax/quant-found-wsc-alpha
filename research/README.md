# research/

Research notebooks, exploratory scripts, and one-off analysis for WSC Alpha go here.

Nothing is here yet — this stage of the project is architecture only (see the
top-level README's "Status" section and `docs/architecture.md`).

Guidelines once research work starts:
- No real Arena API credentials or account data in anything committed here (see
  `.gitignore` and `.env.example`).
- No large datasets committed directly — `data/` is git-ignored project-wide; use an
  external/local data directory and reference it by path, or document a data-fetch
  script instead of checking in the data itself.
- Research findings that inform a design decision belong in `docs/`, not buried in a
  notebook — see how `docs/quant_found_mapping.md` and `docs/architecture.md` are
  structured as the pattern to follow.
