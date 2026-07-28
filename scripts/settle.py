#!/usr/bin/env python3
"""
Results settlement engine: fetches scores, marks picks WON/LOST/PUSH, updates tracker.

This is the entry point for the 10:00 PM cron job.
Usage:
  python settle.py --date 2026-07-28
"""

import argparse
import csv
import os
from datetime import date, datetime
from pathlib import Path


TRACKER_COLS = [
    "date", "league", "home", "away", "market", "selection",
    "best_odds", "book", "model_prob", "true_implied", "edge",
    "ev", "stake", "bankroll_before", "status", "clv",
]


def load_tracker(tracker_path: str) -> list[dict]:
    """Load tracker CSV as list of dicts."""
    if not os.path.exists(tracker_path):
        return []
    with open(tracker_path, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_tracker(tracker_path: str, rows: list[dict]):
    """Save tracker CSV."""
    with open(tracker_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=TRACKER_COLS)
        writer.writeheader()
        writer.writerows(rows)


def settle_bet(row: dict, home_score: int, away_score: int) -> tuple[str, float, str]:
    """
    Determine if a bet won/lost/pushed.
    Returns (status, return_amount, detail).
    """
    market = row.get("market", "")
    selection = row.get("selection", "")
    stake = float(row.get("stake", 0))
    odds = float(row.get("best_odds", 0))

    total_goals = home_score + away_score
    home_win = home_score > away_score
    away_win = home_score < away_score
    draw = home_score == away_score
    both_scored = home_score >= 1 and away_score >= 1

    if market == "1X2":
        if selection == "Home" and home_win:
            return "won", stake * odds, f"{home_score}-{away_score}"
        elif selection == "Away" and away_win:
            return "won", stake * odds, f"{home_score}-{away_score}"
        elif selection == "Draw" and draw:
            return "won", stake * odds, f"{home_score}-{away_score}"
        else:
            return "lost", 0, f"{home_score}-{away_score}"

    elif market in ("Over/Under",):
        lines = selection.split()
        if "Over" in selection:
            line = float(selection.split()[-1])
            if total_goals > line:
                return "won", stake * odds, f"Over {line} ({total_goals} goals)"
            elif total_goals < line:
                return "lost", 0, f"Under {line} ({total_goals} goals)"
            else:
                return "push", stake, f"Push {line} ({total_goals} goals)"
        else:
            line = float(selection.split()[-1])
            if total_goals < line:
                return "won", stake * odds, f"Under {line} ({total_goals} goals)"
            elif total_goals > line:
                return "lost", 0, f"Over {line} ({total_goals} goals)"
            else:
                return "push", stake, f"Push {line} ({total_goals} goals)"

    elif market == "BTTS":
        if selection == "Yes" and both_scored:
            return "won", stake * odds, f"BTTS ({home_score}-{away_score})"
        elif selection == "No" and not both_scored:
            return "won", stake * odds, f"No BTTS ({home_score}-{away_score})"
        else:
            return "lost", 0, f"BTTS {'No' if both_scored else 'Yes'} ({home_score}-{away_score})"

    return "unknown", 0, f"Unhandled: {market}/{selection}"


def settle_pick_markdown(pick_path: str, results: dict[str, tuple[str, float, str]]):
    """
    Update the pick markdown file with results.
    results: {match_id: (status, return_amount, detail)}
    """
    if not os.path.exists(pick_path):
        print(f"  Pick file not found: {pick_path}")
        return

    content = Path(pick_path).read_text()

    # Replace ⏳ Pending with actual result
    for match_id, (status, amount, detail) in results.items():
        emoji = {"won": "✅", "lost": "❌", "push": "🔄"}.get(status, "❓")
        old = f"**Result:** ⏳ Pending"
        new = f"**Result:** {emoji} {status.upper()} — {detail}"
        if content.count(old) > 1:
            # Replace the right occurrence
            # Simple approach: just replace all with per-match identifiers
            content = content.replace(old, new, 1)

    # Add a summary if there were results
    content += "\n## Settlement Summary\n\n"
    wins = sum(1 for s, _, _ in results.values() if s == "won")
    losses = sum(1 for s, _, _ in results.values() if s == "lost")
    pushes = sum(1 for s, _, _ in results.values() if s == "push")
    total_returns = sum(amount for _, amount, _ in results.values())
    total_staked = len(results)  # approximation

    content += f"- ✅ Won: {wins}\n"
    content += f"- ❌ Lost: {losses}\n"
    content += f"- 🔄 Push: {pushes}\n"
    content += f"- Returns: ${total_returns:.2f}\n"

    Path(pick_path).write_text(content)
    return content


def write_results_markdown(date_str: str, results: dict, output_dir: str):
    """Write results to the results markdown file."""
    year = date_str[:4]
    month = date_str[5:7]
    out_path = Path(output_dir) / "data" / "results" / year / month / f"{date_str}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    wins = sum(1 for s, _, _ in results.values() if s == "won")
    losses = sum(1 for s, _, _ in results.values() if s == "lost")
    pushes = sum(1 for s, _, _ in results.values() if s == "push")

    lines = [
        f"# Results — {date_str}",
        f"**Settled:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        f"| Status | Count |",
        f"|--------|-------|",
        f"| ✅ Won | {wins} |",
        f"| ❌ Lost | {losses} |",
        f"| 🔄 Push | {pushes} |",
        "",
    ]

    for match_id, (status, amount, detail) in results.items():
        emoji = {"won": "✅", "lost": "❌", "push": "🔄"}.get(status, "❓")
        lines.append(f"- {emoji} **{match_id}**: {detail} — Return: ${amount:.2f}")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Lessons Learned")
    lines.append("")
    if losses > 0:
        lines.append("- Review losing bets for model calibration gaps")
    if wins > 0:
        lines.append("- Confirm edge detection working on winning bets")
    lines.append("")

    out_path.write_text("\n".join(lines))
    return out_path


def update_tracker(tracker_path: str, results: dict[str, tuple[str, float, str]]) -> float:
    """Update tracker CSV with results, return new bankroll."""
    rows = load_tracker(tracker_path)
    total_return = 0.0

    for row in rows:
        if row.get("status") == "open":
            match_key = f"{row['home']} vs {row['away']} — {row['selection']}"
            if match_key in results:
                status, ret, detail = results[match_key]
                row["status"] = status
                total_return += ret

    save_tracker(tracker_path, rows)
    return total_return


def main():
    ap = argparse.ArgumentParser(description="Settle daily bet results")
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--output-dir", default=".")
    args = ap.parse_args()

    date_str = args.date
    year = date_str[:4]
    month = date_str[5:7]

    pick_path = Path(args.output_dir) / "data" / "picks" / year / month / f"{date_str}.md"
    tracker_path = Path(args.output_dir) / "data" / "tracker.csv"

    print(f"Settling results for {date_str}")
    print(f"Pick file: {pick_path}")
    print(f"Tracker: {tracker_path}")
    print()

    # This is where the cron agent injects match results and calls settle_bet()
    # For programmatic use, results dict format:
    # {"Home vs Away — Selection": ("won"|"lost"|"push", return_amount, "detail")}
    results = {}

    if not results:
        print("No results to settle. (Agent runs this part during cron execution)")
        return

    # Update pick file
    settle_pick_markdown(str(pick_path), results)

    # Update tracker
    new_bankroll = update_tracker(str(tracker_path), results)

    # Write results summary
    write_results_markdown(date_str, results, args.output_dir)

    print(f"Done. New bankroll: ${new_bankroll:.2f}")


if __name__ == "__main__":
    main()
