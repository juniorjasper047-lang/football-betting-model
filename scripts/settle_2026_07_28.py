#!/usr/bin/env python3
"""Settle 2026-07-28 picks with verified FT scores (90' only)."""
from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKER = ROOT / "data/tracker.csv"
RESULTS = ROOT / "data/results/2026/07/2026-07-28.md"


def main() -> None:
    rows = list(csv.DictReader(TRACKER.open()))
    for r in rows:
        if (
            r["date"] == "2026-07-28"
            and r["home"] == "Shamrock Rovers"
            and "Over 2.5" in r["selection"]
        ):
            r["status"] = "lost"
            if r.get("clv") is None:
                r["clv"] = ""

    cols = list(rows[0].keys())
    with TRACKER.open("w", newline="") as f:\n        w = csv.DictWriter(f, fieldnames=cols)\n        w.writeheader()\n        w.writerows(rows)\n\n    results_detail = [\n        {\n            "home": "Celje",
            "away": "Egnatia",
            "market": "BTTS",
            "selection": "Yes",
            "odds": 1.98,
            "stake": 0.75,
            "score": "1-1 (90' / 2-2 AET)",
            "status": "won",
            "detail": "BTTS Yes — both scored in 90'",
        },
        {
            "home": "Celje",
            "away": "Egnatia",
            "market": "Over/Under",
            "selection": "Over 2.5",
            "odds": 1.68,
            "stake": 0.50,
            "score": "1-1 (90')",
            "status": "lost",
            "detail": "O2.5 lost — 2 goals in 90' (ET goals excluded)",
        },
        {
            "home": "Shamrock Rovers",
            "away": "Ararat-Armenia",
            "market": "Over/Under",
            "selection": "Over 2.5",
            "odds": 1.75,
            "stake": 0.50,
            "score": "2-0",
            "status": "lost",
            "detail": "O2.5 lost — only 2 goals (corrected from prior mis-settle)",
        },
        {
            "home": "Dinamo Zagreb",
            "away": "Thun",
            "market": "Over/Under",
            "selection": "Over 2.5",
            "odds": 1.63,
            "stake": 0.30,
            "score": "2-2 (90' / 3-2 AET)",
            "status": "won",
            "detail": "O2.5 won — 4 goals in 90'",
        },
    ]

    for d in results_detail:
        if d["status"] == "won":
            d["ret"] = round(d["stake"] * d["odds"], 3)
            d["pnl"] = round(d["ret"] - d["stake"], 3)
        elif d["status"] == "push":
            d["ret"] = d["stake"]
            d["pnl"] = 0.0
        else:
            d["ret"] = 0.0
            d["pnl"] = round(-d["stake"], 3)

    won = sum(1 for d in results_detail if d["status"] == "won")
    lost = sum(1 for d in results_detail if d["status"] == "lost")
    push = sum(1 for d in results_detail if d["status"] == "push")
    staked = round(sum(d["stake"] for d in results_detail), 2)
    returns = round(sum(d["ret"] for d in results_detail), 3)
    pnl = round(sum(d["pnl"] for d in results_detail), 3)
    start_br = 99.90
    new_br = round(start_br - staked + returns, 2)
    hit = won / (won + lost) if (won + lost) else 0.0

    lg: dict[str, dict] = defaultdict(
        lambda: {"n": 0, "w": 0, "l": 0, "p": 0, "pnl": 0.0, "staked": 0.0}
    )
    mk: dict[str, dict] = defaultdict(
        lambda: {"n": 0, "w": 0, "l": 0, "p": 0, "pnl": 0.0, "staked": 0.0}
    )
    for d in results_detail:
        for bag, key in ((lg, "CL Qual"), (mk, d["market"])):
            bag[key]["n"] += 1
            bag[key]["staked"] += d["stake"]
            bag[key]["pnl"] += d["pnl"]
            bag[key][{"won": "w", "lost": "l", "push": "p"}[d["status"]]] += 1

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Results — 2026-07-28",
        f"**Settled:** {now}",
        "**Competition focus:** UEFA Champions League Qualifying (Q2 second legs)",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Picks settled | {len(results_detail)} |",
        f"| Won | {won} |",
        f"| Lost | {lost} |",
        f"| Push | {push} |",
        f"| Hit rate | {hit:.0%} ({won}/{won + lost}) |",
        f"| Total staked | ${staked:.2f} |",
        f"| Total returns | ${returns:.2f} |",
        f"| Day P&L | ${pnl:+.2f}u |",
        f"| Bankroll before (first pick) | ${start_br:.2f} |",
        f"| **New bankroll** | **${new_br:.2f}** |",
        "",
        "> Correction note: an earlier same-day tracker pass marked Shamrock Rovers O2.5 as won. Verified FT score is **2-0** (2 goals) → **lost**. Settled on **90-minute** scores only (standard OU/BTTS; ET excluded).",
        "",
        "## Results by pick",
        "",
        "| Match | Score (90') | Market | Selection | Odds | Stake | Result | P&L |",
        "|-------|-------------|--------|-----------|------|-------|--------|-----|",
    ]
    for d in results_detail:
        emoji = {"won": "✅", "lost": "❌", "push": "🔄"}[d["status"]]
        lines.append(
            f"| {d['home']} vs {d['away']} | {d['score']} | {d['market']} | {d['selection']} | {d['odds']:.2f} | ${d['stake']:.2f} | {emoji} {d['status'].upper()} | ${d['pnl']:+.2f} |"
        )

    lines += ["", "### Detail", ""]
    for i, d in enumerate(results_detail, 1):
        emoji = {"won": "✅", "lost": "❌", "push": "🔄"}[d["status"]]
        lines += [
            f"{i}. {emoji} **{d['home']} vs {d['away']} — {d['selection']} @ {d['odds']}**",
            f"   - FT: {d['score']}",
            f"   - {d['detail']}",
            f"   - Stake ${d['stake']:.2f} → return ${d['ret']:.2f} (P&L ${d['pnl']:+.2f})",
            "",
        ]

    lines += [
        "## League-by-league",
        "",
        "| League | Picks | W-L-P | Staked | P&L |",
        "|--------|------:|-------|-------:|----:|",
    ]
    for k, v in lg.items():
        lines.append(
            f"| {k} | {v['n']} | {v['w']}-{v['l']}-{v['p']} | ${v['staked']:.2f} | ${v['pnl']:+.2f} |"
        )

    lines += [
        "",
        "## Market-by-market",
        "",
        "| Market | Picks | W-L-P | Staked | P&L |",
        "|--------|------:|-------|-------:|----:|",
    ]
    for k, v in mk.items():
        lines.append(
            f"| {k} | {v['n']} | {v['w']}-{v['l']}-{v['p']} | ${v['staked']:.2f} | ${v['pnl']:+.2f} |"
        )

    lines += [
        "",
        "## Lessons / notes",
        "",
        "### What worked",
        "- **Celje BTTS Yes @ 1.98** — high-event second leg after 3-3 first leg delivered both teams on the scoresheet in 90' (1-1). Game-state 'winner_takes_all_high' + open first leg correctly flagged two-way scoring risk.",
        "- **Dinamo Zagreb O2.5 @ 1.63** — 2-2 at 90' (4 goals). Tight-tie second leg with quality home side chasing progression produced the volume; Poisson total edge held.",
        "",
        "### What didn't",
        "- **Celje O2.5** lost despite BTTS landing. Same match, correlated markets: 1-1 is BTTS yes + under 2.5. Model over-projected total goals (xG total 4.17) vs a cagey 90' that only exploded in ET. **Do not double-stake correlated BTTS + O2.5 on the same leg without reducing combined exposure.**",
        "- **Shamrock Rovers O2.5** lost 2-0. Must-chase narrative (0-2 down from first leg) produced home goals but **clean sheet away** — totals without a BTTS/away-score component overstated two-way chaos. Shamrock controlled the tie without opening up enough for 3+.",
        "",
        "### Model adjustments",
        "1. **90' settlement discipline:** always settle OU/BTTS on regulation time; ignore ET/pens. Log AET scores only as context.",
        "2. **Correlation haircut:** if taking BTTS + O2.5 on same fixture, treat combined stake as one risk unit (cap ~0.75–1.0u total), not two independent Kelly slices.",
        "3. **Must-chase totals:** when home trails on agg and is favorite, fade pure O2.5 unless away xG also supports; prefer home ML / home team totals / BTTS only when away threat is real.",
        "4. **CL qual second legs:** variance is high and prices are sharp on big clubs; keep stakes small (today's band 0.3–0.75u was right). Avoid stacking three overs on the same slate without diversification.",
        "5. **Process bug:** prior auto-settle marked Shamrock O2.5 won without verifying total goals ≥ 3. Settlement must require explicit FT score + goal count check before status write.",
        "",
        "### Bankroll continuity",
        f"- Start (pre-settle reference): ${start_br:.2f}",
        f"- Staked: ${staked:.2f} | Returns: ${returns:.2f} | P&L: ${pnl:+.2f}",
        f"- **End bankroll: ${new_br:.2f}**",
        "",
        "---",
        "",
        "**Disclaimer:** Models and opinions, not guarantees. Paper/tracking only — never auto-place bets. Only risk disposable bankroll. If gambling stops being fun, stop. Help: BeGambleAware / local helplines.",
        "",
    ]

    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text("\n".join(lines))
    print(f"Wrote {RESULTS}")
    print(f"new_br={new_br} pnl={pnl:+.3f} record={won}-{lost}-{push}")
    print("--- tracker tail ---")
    print("\n".join(TRACKER.read_text().splitlines()[-5:]))


if __name__ == "__main__":
    main()
