#!/usr/bin/env python3
"""Poisson match model with game-state adjustment for 2nd legs.

Integrates attack/defense strengths, home advantage, league averages,
and game-state factors (must-score, dead rubber, etc.).

Usage:
  python model.py --home "Dinamo Zagreb" --away "Thun" --league "CL Qual" \
    --home-att 1.8 --home-def 0.9 --away-att 1.2 --away-def 1.0 \
    --first-leg "1-1" --is-second-leg
"""
import argparse
import json
import sys
from math import exp, factorial
from dataclasses import dataclass
from typing import Optional


@dataclass
class MatchInput:
    home: str
    away: str
    league: str
    home_att: float      # Goals scored per game (adjusted)
    home_def: float      # Goals conceded per game (adjusted)
    away_att: float
    away_def: float
    league_avg_gpg: float = 2.6
    home_advantage: float = 0.30   # +0.30 goals for home
    first_leg_score: Optional[str] = None
    is_second_leg: bool = False
    # Defense injury adjustments (add to expected total goals)
    defense_adj: float = 0.0


@dataclass
class MatchOutput:
    home_expected: float
    away_expected: float
    total_expected: float
    prob_home: float
    prob_draw: float
    prob_away: float
    prob_over_2_5: float
    prob_over_1_5: float
    prob_btts: float
    predicted_score: str
    game_state_label: str
    confidence: str  # High/Medium/Low


def poisson_pmf(lam: float, k: int) -> float:
    return exp(-lam) * (lam ** k) / factorial(k)


def score_grid(lh: float, la: float, n: int = 10) -> dict:
    grid = {}
    for i in range(n + 1):
        for j in range(n + 1):
            grid[(i, j)] = poisson_pmf(lh, i) * poisson_pmf(la, j)
    return grid


def prob_1x2(grid: dict) -> tuple[float, float, float]:
    h = sum(v for (i, j), v in grid.items() if i > j)
    d = sum(v for (i, j), v in grid.items() if i == j)
    a = sum(v for (i, j), v in grid.items() if i < j)
    return h, d, a


def prob_over(grid: dict, line: float) -> float:
    return sum(v for (i, j), v in grid.items() if i + j > line)


def prob_btts(grid: dict) -> float:
    h0 = sum(v for (i, j), v in grid.items() if i == 0)
    a0 = sum(v for (i, j), v in grid.items() if j == 0)
    return (1 - h0) * (1 - a0)


def predicted_score(grid: dict) -> tuple[int, int]:
    score, _ = max(grid.items(), key=lambda kv: kv[1])
    return score


def game_state_adjustment(m: MatchInput) -> tuple[float, str]:
    """
    Adjust expected goals based on game state (for 2nd legs).
    Returns (goal_multiplier, label).
    """
    if not m.is_second_leg or not m.first_leg_score:
        return 1.0, "standard"

    try:
        parts = m.first_leg_score.split("-")
        home_goals, away_goals = int(parts[0]), int(parts[1])
    except (ValueError, IndexError):
        return 1.0, "standard"

    diff = home_goals - away_goals

    if abs(diff) >= 4:
        return 0.85, "dead_rubber_large"
    if abs(diff) >= 3:
        return 0.90, "dead_rubber_moderate"

    total = home_goals + away_goals

    # Winner-takes-all at high aggregate (e.g., 3-3)
    if total >= 6 and abs(diff) <= 1:
        return 1.25, "winner_takes_all_high"
    # Must-chase (down 2, home team)
    if diff == -2 or diff == 2:
        return 1.18, "must_chase"
    # Tight tie (1 goal margin or draw)
    if abs(diff) <= 1 and total <= 4:
        return 1.05, "tight_tie"

    return 1.0, "neutral"


def run_model(m: MatchInput) -> MatchOutput:
    # Calculate expected goals
    league_avg = m.league_avg_gpg

    # Attack/defense ratios
    home_att_ratio = m.home_att / league_avg if league_avg > 0 else 1.0
    away_def_ratio = m.away_def / league_avg if league_avg > 0 else 1.0
    away_att_ratio = m.away_att / league_avg if league_avg > 0 else 1.0
    home_def_ratio = m.home_def / league_avg if league_avg > 0 else 1.0

    home_xg = league_avg * home_att_ratio * away_def_ratio + m.home_advantage
    away_xg = league_avg * away_att_ratio * home_def_ratio

    # Defense injury adjustment (split across both teams)
    home_xg += m.defense_adj / 2
    away_xg += m.defense_adj / 2

    # Game state adjustment
    gs_mult, gs_label = game_state_adjustment(m)
    home_xg *= gs_mult
    away_xg *= gs_mult

    # Run Poisson
    grid = score_grid(home_xg, away_xg)
    h_prob, d_prob, a_prob = prob_1x2(grid)
    over_25 = prob_over(grid, 2.5)
    over_15 = prob_over(grid, 1.5)
    btts_prob = prob_btts(grid)
    pred_score = predicted_score(grid)

    # Confidence based on model clarity
    max_prob = max(h_prob, d_prob, a_prob)
    if max_prob > 0.55:
        conf = "High"
    elif max_prob > 0.45:
        conf = "Medium"
    else:
        conf = "Low"

    return MatchOutput(
        home_expected=round(home_xg, 2),
        away_expected=round(away_xg, 2),
        total_expected=round(home_xg + away_xg, 2),
        prob_home=round(h_prob, 3),
        prob_draw=round(d_prob, 3),
        prob_away=round(a_prob, 3),
        prob_over_2_5=round(over_25, 3),
        prob_over_1_5=round(over_15, 3),
        prob_btts=round(btts_prob, 3),
        predicted_score=f"{pred_score[0]}-{pred_score[1]}",
        game_state_label=gs_label,
        confidence=conf,
    )


def format_output(out: MatchOutput) -> str:
    lines = [
        f"Expected goals: Home={out.home_expected} Away={out.away_expected} Total={out.total_expected}",
        f"1X2: Home={out.prob_home:.1%} Draw={out.prob_draw:.1%} Away={out.prob_away:.1%}",
        f"Over 2.5: {out.prob_over_2_5:.1%} | Over 1.5: {out.prob_over_1_5:.1%}",
        f"BTTS: {out.prob_btts:.1%}",
        f"Predicted score: {out.predicted_score}",
        f"Game state: {out.game_state_label} | Confidence: {out.confidence}",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Poisson match model")
    ap.add_argument("--home", required=True)
    ap.add_argument("--away", required=True)
    ap.add_argument("--league", default="Unknown")
    ap.add_argument("--home-att", type=float, default=1.5)
    ap.add_argument("--home-def", type=float, default=1.2)
    ap.add_argument("--away-att", type=float, default=1.3)
    ap.add_argument("--away-def", type=float, default=1.3)
    ap.add_argument("--league-avg", type=float, default=2.6)
    ap.add_argument("--home-adv", type=float, default=0.30)
    ap.add_argument("--first-leg", default=None)
    ap.add_argument("--is-second-leg", action="store_true")
    ap.add_argument("--def-adj", type=float, default=0.0)
    ap.add_argument("--json", action="store_true", help="Output JSON")
    args = ap.parse_args()

    m = MatchInput(
        home=args.home,
        away=args.away,
        league=args.league,
        home_att=args.home_att,
        home_def=args.home_def,
        away_att=args.away_att,
        away_def=args.away_def,
        league_avg_gpg=args.league_avg,
        home_advantage=args.home_adv,
        first_leg_score=args.first_leg,
        is_second_leg=args.is_second_leg,
        defense_adj=args.def_adj,
    )

    out = run_model(m)

    if args.json:
        print(json.dumps({
            "home": m.home, "away": m.away, "league": m.league,
            "expected_goals": {"home": out.home_expected, "away": out.away_expected, "total": out.total_expected},
            "probabilities": {"home": out.prob_home, "draw": out.prob_draw, "away": out.prob_away},
            "over_2_5": out.prob_over_2_5,
            "over_1_5": out.prob_over_1_5,
            "btts": out.prob_btts,
            "predicted_score": out.predicted_score,
            "game_state": out.game_state_label,
            "confidence": out.confidence,
        }))
    else:
        print(f"\n{m.home} vs {m.away} ({m.league})")
        print("=" * 50)
        print(format_output(out))


if __name__ == "__main__":
    main()
