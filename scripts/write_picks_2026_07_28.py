#!/usr/bin/env python3
"""Write 2026-07-28 picks markdown, results placeholder, and tracker rows."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
with open("/tmp/picks_2026-07-28.json") as f:\n    data = json.load(f)\n\ndate_str = "2026-07-28"
picks = data["picks"]
BANKROLL = 100.0

out_path = ROOT / f"data/picks/2026/07/{date_str}.md"
out_path.parent.mkdir(parents=True, exist_ok=True)

lines = [
    f"# Picks — {date_str}",
    "",
    f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
    f"**Leagues analyzed:** 15 (fixtures found in 2)",
    f"**Fixtures modeled:** {data['fixtures_analyzed']}",
    f"**Value picks found:** {len(picks)}",
    f"**Paper bankroll:** ${BANKROLL:.2f}",
    "",
    "## Scope",
    "",
    f"- **With fixtures today:** {', '.join(data['leagues_with_fixtures'])}",
    f"- **No fixtures / not scheduled:** {', '.join(data['leagues_no_fixtures'])}",
    "- **Europa League Qual:** second legs mainly 30 Jul (none today)",
    "- Domestic leagues (Nordic/CEE/Scotland/Austria/Swiss/Czech etc.): midweek gap / post-WC scheduling — no top-flight slate found for 28 Jul",
    "",
    "---",
    "",
    "## Value Picks",
    "",
    "| # | League | Match | Market | Selection | Odds | Model% | True% | Edge | EV | Stake |",
    "|---|--------|-------|--------|-----------|------|--------|-------|------|-----|-------|",
]

for i, p in enumerate(picks, 1):
    lines.append(
        f"| {i} | {p['league']} | {p['home']} vs {p['away']} | "
        f"{p['market']} | {p['selection']} | {p['odds']} | "
        f"{p['model_prob']:.1%} | {p['true_implied']:.1%} | "
        f"{p['edge']:+.1%} | {p['ev']:+.3f} | ${p['stake']:.2f} |"
    )

lines += ["", "---", ""]

for i, p in enumerate(picks, 1):
    lines += [
        f"### Pick {i}: {p['home']} vs {p['away']} — {p['selection']} @ {p['odds']}",
        "",
        f"**League:** {p['league']}",
        f"**Market:** {p['market']}",
        f"**Best odds:** {p['odds']}",
        f"**Bookmaker:** {p.get('book', 'SportyBet')}",
        f"**First leg:** {p.get('first_leg', 'n/a')}",
        "",
        "**Model output:**",
        f"- Expected goals: Home {p['xg_home']} — Away {p['xg_away']} — Total {p['xg_total']}",
        f"- 1X2 probs: H {p['p_home']:.1%} / D {p['p_draw']:.1%} / A {p['p_away']:.1%}",
        f"- O2.5: {p['p_o25']:.1%} | BTTS: {p['p_btts']:.1%}",
        f"- Predicted score: {p['predicted_score']}",
        f"- Game state: {p.get('game_state', 'standard')}",
        f"- Confidence: {p.get('confidence', 'Medium')}",
        "",
        "**Value analysis:**",
        f"- Model probability: {p['model_prob']:.1%}",
        f"- Implied probability (odds): {p['true_implied']:.1%}",
        f"- Edge: {p['edge']:+.1%} | EV: {p['ev']:+.3f}",
        f"- Stake: ${p['stake']:.2f} ({p.get('stake_pct', 0):.2f}% of bankroll) — fractional Kelly band / edge unit scale",
        f"- Potential return: ${p.get('potential_return', 0):.2f}",
        "",
        f"**Reason:** {p.get('reason', 'Value edge meets threshold')}",
        "",
        f"**Sources:** {p.get('sources', 'Web search — odds aggregators')}",
        "",
        "**Result:** ⏳ Pending",
        "",
        "---",
        "",
    ]

total_stake = sum(p["stake"] for p in picks)
lines += [
    "## Staking summary",
    "",
    f"- Picks: {len(picks)}",
    f"- Total stake: ${total_stake:.2f}",
    "- Edge bands: >10% → 0.75u | 7–10% → 0.50u | 5–7% → 0.30u (¼ Kelly framework)",
    "- Preferred markets only (O2.5 / BTTS); dead rubbers skipped (Hearts–Sturm 0-4, Lincoln–Mjällby 0-3, Apollon–Dila 4-0)",
    "",
    "## Skipped / no bet",
    "",
    "- **Hearts vs Sturm Graz** — dead_rubber_large (agg 0-4); O2.5/BTTS no edge",
    "- **Lincoln Red Imps vs Mjällby** — dead_rubber_moderate (agg 0-3); no goals-market edge",
    "- **Apollon Limassol vs Dila Gori** — dead_rubber_large (agg 4-0)",
    "- **Riga FC vs Vardar** — neutral state; O2.5/BTTS edges under 5%",
    "- **Dinamo Zagreb O2.5** — model 62.1% vs imp 61.3% (edge +0.8%, below threshold); BTTS taken instead",
    "",
]

out_path.write_text("\n".join(lines))
print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)")

res_path = ROOT / f"data/results/2026/07/{date_str}.md"
res_path.parent.mkdir(parents=True, exist_ok=True)
res_path.write_text(
    f"# Results — {date_str}\n\n"
    f"⏳ Pending settlement at 22:00 UTC\n\n"
    f"**Morning picks logged:** {len(picks)}\n"
    f"**Total stake at risk:** ${total_stake:.2f}\n\n"
    f"## Matches to settle\n\n"
    + "\n".join(
        f"- {p['home']} vs {p['away']} — {p['market']} {p['selection']} @ {p['odds']} (stake ${p['stake']:.2f})"
        for p in picks
    )
    + "\n"
)
print(f"Wrote {res_path}")

tracker_path = ROOT / "data/tracker.csv"
rows = tracker_path.read_text().strip().splitlines()
kept = [rows[0]]
for r in rows[1:]:
    if r.startswith("2026-07-28,"):
        continue
    kept.append(r)

br = BANKROLL
new_rows = []
for p in picks:
    lg = p["league"]
    if lg == "Champions League Qual":
        lg = "CL Qual"
    elif lg == "Conference League Qual":
        lg = "Conf Lge Qual"
    row = (
        f"{date_str},{lg},{p['home']},{p['away']},{p['market']},{p['selection']},"
        f"{p['odds']},{p['book']},{p['model_prob']},{p['true_implied']},{p['edge']},{p['ev']},"
        f"{p['stake']:.2f},{br:.2f},open,"
    )
    new_rows.append(row)
    br = round(br - p["stake"], 2)

final = "\n".join(kept + new_rows) + "\n"
tracker_path.write_text(final)
print(f"Updated tracker.csv — kept {len(kept)-1} historic + {len(new_rows)} new open picks")
print("\n".join(final.strip().splitlines()[-14:]))
