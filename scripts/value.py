#!/usr/bin/env python3
"""Value/EV calculator for comparing model probabilities to bookmaker odds.

Usage:
  python value.py --prob 0.63 --odds 1.98
"""
import argparse


def calculate_value(model_prob: float, odds: float) -> dict:
    implied = 1.0 / odds
    edge = model_prob - implied
    ev = model_prob * (odds - 1.0) - (1.0 - model_prob)

    if edge >= 0.05:
        verdict = "VALUE"
    elif edge >= 0.02:
        verdict = "marginal"
    else:
        verdict = "no value"

    return {
        "model_prob": model_prob,
        "implied": implied,
        "edge": edge,
        "ev": ev,
        "verdict": verdict,
    }


def format_value(result: dict) -> str:
    return (
        f"model_prob={result['model_prob']:.3f} "
        f"implied={result['implied']:.3f} "
        f"edge={result['edge']:+.3f} "
        f"EV={result['ev']:+.3f} "
        f"-> {result['verdict']}"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prob", type=float, required=True, help="model win prob 0-1")
    ap.add_argument("--odds", type=float, required=True, help="decimal odds")
    ap.add_argument("--taken", type=float, default=None, help="odds taken (for CLV)")
    ap.add_argument("--closing", type=float, default=None, help="closing odds (for CLV)")
    args = ap.parse_args()

    result = calculate_value(args.prob, args.odds)
    print(format_value(result))

    if args.taken and args.closing:
        clv = (1.0 / args.taken) - (1.0 / args.closing)
        print(f"CLV={clv:+.4f} ({'beat close' if clv > 0 else 'lost close'})")


if __name__ == "__main__":
    main()
