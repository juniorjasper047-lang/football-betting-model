#!/usr/bin/env python3
"""Odds conversion utilities: decimal/american/implied + margin removal.

Usage:
  python odds_convert.py --odds 1.98          # decimal → implied + american
  python odds_convert.py --implied 0.505      # implied → decimal
  python odds_convert.py --american -150      # american → decimal
  python odds_convert.py --odds "1.98,1.83"   # de-vig (remove margin)
"""
import argparse
from typing import List


def decimal_to_implied(odds: float) -> float:
    return 1.0 / odds


def implied_to_decimal(implied: float) -> float:
    return 1.0 / implied if implied > 0 else 0.0


def decimal_to_american(odds: float) -> str:
    if odds >= 2.0:
        return f"+{int((odds - 1) * 100)}"
    else:
        return f"-{int(100 / (odds - 1))}"


def american_to_decimal(american: str) -> float:
    val = int(american)
    if val > 0:
        return 1.0 + val / 100.0
    else:
        return 1.0 - 100.0 / val


def remove_margin(odds_list: List[float]) -> List[float]:
    """Proportional (Shin-like) margin removal across book odds."""
    implieds = [1.0 / o for o in odds_list]
    margin = sum(implieds) - 1.0
    if margin <= 0:
        return implieds
    true_implieds = [imp / (1.0 + margin) for imp in implieds]
    return true_implieds


def de_vig_1x2(home_odds: float, draw_odds: float, away_odds: float) -> dict:
    """Remove overround from 1X2 market."""
    raw = [1.0 / home_odds, 1.0 / draw_odds, 1.0 / away_odds]
    margin = sum(raw) - 1.0
    true = [p / (1.0 + margin) for p in raw]
    return {
        "raw_implied": {"home": raw[0], "draw": raw[1], "away": raw[2]},
        "margin": margin,
        "true_prob": {"home": true[0], "draw": true[1], "away": true[2]},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--odds", type=str, default=None, help="decimal odds (comma sep for de-vig)")
    ap.add_argument("--implied", type=float, default=None, help="implied probability")
    ap.add_argument("--american", type=str, default=None, help="american odds")
    ap.add_argument("--h", type=float, default=None, help="1X2: home odds")
    ap.add_argument("--d", type=float, default=None, help="1X2: draw odds")
    ap.add_argument("--a", type=float, default=None, help="1X2: away odds")
    args = ap.parse_args()

    if args.american:
        dec = american_to_decimal(args.american)
        print(f"american={args.american} → decimal={dec:.3f} implied={decimal_to_implied(dec):.3f}")

    elif args.implied:
        dec = implied_to_decimal(args.implied)
        print(f"implied={args.implied:.3f} → decimal={dec:.3f} american={decimal_to_american(dec)}")

    elif args.h and args.d and args.a:
        result = de_vig_1x2(args.h, args.d, args.a)
        print(f"1X2 de-vig (margin={result['margin']:.4f}):")
        print(f"  Home: {result['true_prob']['home']:.4f} | Draw: {result['true_prob']['draw']:.4f} | Away: {result['true_prob']['away']:.4f}")

    elif args.odds:
        odds_list = [float(x.strip()) for x in args.odds.split(",")]
        true = remove_margin(odds_list)
        for i, (o, t) in enumerate(zip(odds_list, true)):
            print(f"odds={o:.3f} raw_implied={1.0/o:.4f} true_implied={t:.4f}")
        margin = sum(1.0/o for o in odds_list) - 1.0
        print(f"margin={margin:.4f}")
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
