# Rate history

Daily exchange rates kept for QuickFX's extended charts and date lookups.
QuickFX Pro's long charts download `charts/` (below); the rest is the raw archive.

## `frankfurter/`

A one-off copy of every daily rate available from the Frankfurter API
(`api.frankfurter.dev/v2`), downloaded on 2026-09-26 so QuickFX doesn't
depend on that service staying up.

- `usd-YYYY.json`: one file per year, base USD,
  `{"history": {"YYYY-MM-DD": {"EUR": 0.87, ...}}}`. Only days a source
  published are present (no weekends or bank holidays).
- `currencies.json`: every currency with its first and last available date.
- `providers.json`: the 98 central banks and official bodies the rates come
  from, with links to each one's terms where they publish them.

These are **official/reference rates**. For most currencies they're within a
fraction of a percent of market rates. For a few, where the official rate is
far from what people really pay (SSP, SYP, KPW, BOB, CUP; also SCR, AFN, BWP
at around 2%), don't mix them into charts next to OXR's market rates: the
join would look like a sudden move.

## `../history-archive.json`

Our own permanent record: the last OpenExchangeRates fetch of every UTC day,
appended automatically by the QuickRate rates workflow and never trimmed.
`rates.json` only keeps 90 days because the app downloads it on every launch.

## `charts/`

One file per currency for QuickFX Pro's 1-year, 5-year and all-time charts,
built by `scripts/build_chart_history.py` from `frankfurter/` (up to its last
day) and `../history-archive.json` (after it). Base USD,
`{"code", "base", "updated", "points": [["YYYY-MM-DD", rate], ...]}`: daily
for the last 5 years, weekly (dated Fridays) back to 20 years, monthly (dated
the 1st) before that. `index.json` lists the currencies and the build day.
The rates workflow rebuilds them once a day. SSP, SYP, KPW, BOB, CUP, SCR,
AFN and BWP are left out (see above).
