# Rate history

Daily exchange rates kept for QuickFX's extended charts and date lookups.
The app does not download anything in this folder yet.

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
