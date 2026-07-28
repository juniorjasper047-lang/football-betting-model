#!/usr/bin/env python3
"""
Daily match analyzer: fetches fixtures, models outcomes, finds value, writes picks.

This is the main entry point for the 6:00 AM cron job.
Usage:
  python analyze.py --date 2026-07-28 --bankroll 100
"""

import argparse
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent))

from model import MatchInput, run_model, format_output
from value import calculate_value, format_value
from kelly import calculate_stake


# League configurations — avg goals per game, home advantage factor
LEAGUE_CONFIGS = {
    "Champions League Qual": {"gpg": 2.80, "home_adv": 0.30},
    "Europa League Qual": {"gpg": 2.70, "home_adv": 0.30},
    "Conference League Qual": {"gpg": 2.80, "home_adv": 0.30},
    "Czech Liga": {"gpg": 2.65, "home_adv": 0.35},
    "Denmark Superliga": {"gpg": 2.70, "home_adv": 0.35},
    "Finland Veikkausliiga": {"gpg": 2.55, "home_adv": 0.30},
    "Iceland Urvalsdeild": {"gpg": 2.85, "home_adv": 0.25},
    "Norway Eliteserien": {"gpg": 2.80, "home_adv": 0.30},
    "Russia Premier League": {"gpg": 2.45, "home_adv": 0.35},
    "Serbia Super Liga": {"gpg": 2.60, "home_adv": 0.40},
    "Sweden Allsvenskan": {"gpg": 2.65, "home_adv": 0.30},
    "Switzerland Super League": {"gpg": 2.75, "home_adv": 0.35},
    "Austria Bundesliga": {"gpg": 2.70, "home_adv": 0.35},
    "Croatia HNL": {"gpg": 2.55, "home_adv": 0.40},
    "Scottish Premiership": {"gpg": 2.60, "home_adv": 0.35},
}

# Active leagues by date range
ACTIVE_LEAGUES = [
    "Champions League Qual", "Europa League Qual", "Conference League Qual",
    "Czech Liga", "Denmark Superliga", "Finland Veikkausliiga",
    "Iceland Urvalsdeild", "Norway Eliteserien", "Russia Premier League",
    "Serbia Super Liga", "Sweden Allsvenskan", "Switzerland Super League",
    "Austria Bundesliga", "Croatia HNL", "Scottish Premiership",
]

# Strategy rules
SKIP_LEAGUES = ["MLS"]  # blacklisted
PREFERRED_MARKETS = ["Over/Under", "BTTS"]  # O2.5 + BTTS first, 1X2 last
EDGE_THRESHOLD = 0.05  # 5% minimum edge
MAX_EDGE_SKEPTICAL = 0.25  # >25% edge → treat as model error


def write_pick_markdown(date_str: str, picks: list, output_dir: str):
    """Write daily picks to markdown file."""
    year = date_str[:4]
    month = date_str[5:7]
    out_path = Path(output_dir) / "data" / "picks" / year / month / f"{date_str}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Picks — {date_str}",
        "",
        f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Leagues analyzed:** {len(ACTIVE_LEAGUES)}",
        f"**Value picks found:** {len(picks)}",
        "",
        "---",
        "",
    ]

    if not picks:
        lines.append("## No value picks today")
        lines.append("")
        lines.append("No bets met the minimum edge threshold of 5%.")
        out_path.write_text("\n".join(lines))
        return out_path

    lines.append("## Value Picks")
    lines.append("")
    lines.append("| # | League | Match | Market | Selection | Odds | Model% | True% | Edge | EV | Stake |")
    lines.append("|---|--------|-------|--------|-----------|------|--------|-------|------|-----|-------|")

    for i, p in enumerate(picks, 1):
        lines.append(
            f"| {i} | {p['league']} | {p['home']} vs {p['away']} | "
            f"{p['market']} | {p['selection']} | {p['odds']} | "
            f"{p['model_prob']:.1%} | {p['true_implied']:.1%} | "
            f"{p['edge']:+.1%} | {p['ev']:+.3f} | ${p['stake']:.2f} |"
        )

    lines.append("")
    lines.append("---")
    lines.append("")

    # Detailed per-pick
    for i, p in enumerate(picks, 1):
        lines.append(f"### Pick {i}: {p['home']} vs {p['away']} — {p['selection']} @ {p['odds']}")
        lines.append("")
        lines.append(f"**League:** {p['league']}")
        lines.append(f"**Market:** {p['market']}")
        lines.append(f"**Best odds:** {p['odds']}")
        lines.append(f"**Bookmaker:** {p.get('book', 'N/A')}")
        lines.append("")
        lines.append("**Model output:**")
        lines.append(f"- Expected goals: Home {p['xg_home']} — Away {p['xg_away']} — Total {p['xg_total']}")
        lines.append(f"- Predicted score: {p['predicted_score']}")
        lines.append(f"- Game state: {p.get('game_state', 'standard')}")
        lines.append(f"- Confidence: {p.get('confidence', 'Medium')}")
        lines.append("")
        lines.append("**Value analysis:**")
        lines.append(f"- Model probability: {p['model_prob']:.1%}")
        lines.append(f"- Implied probability (odds): {p['true_implied']:.1%}")
        lines.append(f"- Edge: {p['edge']:+.1%} | EV: {p['ev']:+.3f}")
        lines.append(f"- Stake: ${p['stake']:.2f} ({p.get('stake_pct', 0):.2f}% of bankroll)")
        lines.append(f"- Potential return: ${p.get('potential_return', 0):.2f}")
        lines.append("")
        lines.append(f"**Reason:** {p.get('reason', 'Value edge meets threshold')}")
        lines.append("")
        lines.append(f"**Sources:** {p.get('sources', 'Web search — odds aggregators')}")
        lines.append("")
        lines.append("**Result:** ⏳ Pending")
        lines.append("")
        lines.append("---")
        lines.append("")

    out_path.write_text("\n".join(lines))
    return out_path


def write_result_date(date_str: str, results_file: str, tracker_path: str):
    """Set up results template for evening cron to fill."""
    year = date_str[:4]
    month = date_str[5:7]
    results_path = Path(os.path.dirname(results_file)) / "data" / "results" / year / month / f"{date_str}.md"
    results_path.parent.mkdir(parents=True, exist_ok=True)
    results_path.write_text(f"# Results — {date_str}\n\n⏳ Pending settlement at 22:00 UTC\n")
    return results_path


def main():
    ap = argparse.ArgumentParser(description="Daily match analyzer")
    ap.add_argument("--date", default=date.today().isoformat(),
                    help="Date to analyze (YYYY-MM-DD)")
    ap.add_argument("--bankroll", type=float, default=100.0,
                    help="Paper bankroll amount")
    ap.add_argument("--output-dir", default=".",
                    help="Project root dir")
    args = ap.parse_args()

    print(f"Analyzing matches for {args.date}")
    print(f"Active leagues: {len(ACTIVE_LEAGUES)}")
    print(f"Paper bankroll: ${args.bankroll:.2f}")
    print()

    # This is where the cron agent will inject fixture data and run the model
    # For now, output the template that the agent fills
    picks = []  # Populated by the agent during cron run

    # Write template files
    pick_path = write_pick_markdown(args.date, picks, args.output_dir)
    print(f"Picks written to: {pick_path}")

    results_path = write_result_date(
        args.date,
        str(Path(args.output_dir) / "data" / "results" / year / month / f"{args.date}.md"),
        str(Path(args.output_dir) / "data" / "tracker.csv"),
    )
    print(f"Results placeholder: {results_path}")


if __name__ == "__main__":
    main()
