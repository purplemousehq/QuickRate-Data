#!/usr/bin/env python3
"""Builds history/charts/<CODE>.json: one small file per currency for
QuickFX Pro's long charts (1 year, 5 years, all time).

Sources, both base USD:
  history/frankfurter/usd-YYYY.json  official reference rates, a one-off
                                     copy up to 2026-09-26
  history-archive.json               our own OpenExchangeRates archive,
                                     one rate per UTC day, growing daily
Frankfurter is used up to its last day, the archive after it.

To stay small, detail thins out with age: daily for the last 5 years,
weekly (the week's last rate, dated that week's Friday) back to 20 years,
monthly (dated the 1st) before that. Weekly and monthly dates are the same
for every currency, so the app can pair any two files.

Run from the repo root. The rates workflow runs it hourly; it rebuilds at
most once a day (history/charts/index.json records the day), or with --force.
"""
import datetime as dt
import glob
import json
import os
import sys

OUT = "history/charts"
# Official rate far from what people pay: joining it to market rates would
# show a fake jump, so these get no long chart (see history/README.md).
EXCLUDED = {"SSP", "SYP", "KPW", "BOB", "CUP", "SCR", "AFN", "BWP"}


def load(path):
    with open(path) as f:
        return json.load(f)["history"]


def main():
    today = dt.date.today()
    index_path = os.path.join(OUT, "index.json")
    if "--force" not in sys.argv and os.path.exists(index_path):
        if json.load(open(index_path)).get("built") == today.isoformat():
            print("chart history already built today")
            return

    series = {}   # code -> {date: rate}
    last_official = ""
    for path in sorted(glob.glob("history/frankfurter/usd-*.json")):
        for day, rates in load(path).items():
            last_official = max(last_official, day)
            for code, rate in rates.items():
                series.setdefault(code, {})[day] = rate
    for day, rates in load("history-archive.json").items():
        if day <= last_official:
            continue
        for code, rate in rates.items():
            series.setdefault(code, {})[day] = rate

    daily_from = (today - dt.timedelta(days=5 * 366)).isoformat()
    weekly_from = (today - dt.timedelta(days=20 * 366)).isoformat()

    def bucket(day):
        if day >= daily_from:
            return day
        d = dt.date.fromisoformat(day)
        if day >= weekly_from:
            return (d + dt.timedelta(days=4 - d.weekday())).isoformat()   # that week's Friday
        return d.replace(day=1).isoformat()

    os.makedirs(OUT, exist_ok=True)
    built = []
    for code, points in sorted(series.items()):
        if code == "USD" or code in EXCLUDED or len(points) < 30:
            continue
        thinned = {}
        for day in sorted(points):        # later days overwrite: the bucket keeps its last rate
            thinned[bucket(day)] = points[day]
        out = {"code": code, "base": "USD", "updated": today.isoformat(),
               "points": [[day, float(f"{rate:.6g}")] for day, rate in sorted(thinned.items())]}
        with open(os.path.join(OUT, f"{code}.json"), "w") as f:
            json.dump(out, f, separators=(",", ":"))
        built.append(code)

    last = max(max(p) for p in series.values())
    json.dump({"built": today.isoformat(), "last": last, "codes": built},
              open(index_path, "w"), indent=1)
    print(f"built {len(built)} currencies, last day {last}")


if __name__ == "__main__":
    main()
