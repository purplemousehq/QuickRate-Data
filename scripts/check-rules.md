# Weekly check: QuickFX "Actual price" rules

This is the brief for the weekly cloud routine. The routine checks `real-price-rules.json` (tax and tipping rules for 130 places) against the sources it cites.

## For each rule in `real-price-rules.json`

1. Open every URL in its `sources`.
   - Read the raw page text, not a summary.
   - If a page returns 403 or 404, try the latest Wayback Machine copy (`https://web.archive.org/web/2026/<url>`).
2. Compare these values with what the source says now:
   - tax lines: name, rate, added vs. included;
   - service charge: kind, rate, plusPlus, serviceTaxed;
   - tip custom: kind, min, usual, generous.
   - A difference counts only when the source states a new value **and** an effective date, or clearly replaces the old one. Wording changes don't count.
3. If a source is unreachable on both the live site and Wayback, list it in the report. Don't change the rule.

## Conditional taxes

A tax that applies only sometimes (alcohol only, one city, hotel restaurants, resort towns) goes in `conditionalTaxes`, never in `restaurantExtra`. App versions up to 3.5 add every `restaurantExtra` rate to every price. Keep `restaurantExtra` as `[]` unless a tax applies to every restaurant meal in that place.

## If anything changed

- Create a branch `rules/<yyyy-mm-dd>`.
- Edit `real-price-rules.json`: update only the changed values, and set `checked` to the current `yyyy-mm`.
- If a rule's note text changes meaning, update the matching entry in all 8 `real-price-strings/<lang>.json` files. Write natural, polite translations.
- Validate: every rule still has the same fields and types, and the JSON parses.
- Open a pull request against `main`:
  - Title: `Rules: <place> <old> → <new>` (for several changes: `Rules: N changes (<places>)`).
  - Body, in plain English, per change: place, old value, new value, effective date, the source URL and a quote of the line that shows it.
  - Request review from `michaelknox` (Mike). If that fails, mention @michaelknox in the body.
- **Never merge.** Mike approves in the GitHub app.

## If nothing changed

Commit straight to `main`, changing only the `checked` month in `real-price-rules.json` (and only if it changed). Commit message: `Rules checked <yyyy-mm>: no changes`.

## Never

- Touch `rates.json`, `history*`, `update-log.json` or `privacy.html`.
- Merge a pull request, force-push, or delete branches other than your own.
