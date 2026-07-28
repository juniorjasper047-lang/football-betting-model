#!/usr/bin/env python3
"""Kelly criterion staking calculator.

Usage:
  python kelly.py --bankroll 100 --odds 2.10 --prob 0.55
  python kelly.py --bankroll 100 --odds 2.10 --prob 0.55 --frac 0.25 --cap 0.02
"""
import argparse


def kelly_fraction(odds: float, prob: float) -> float:
    b = odds - 1.0
    if b <= 0:
        return 0.0
    f = (b * prob - (1.0 - prob)) / b
    return max(0.0, f)


def calculate_stake(
    bankroll: float,
    odds: float,
    prob: float,
    frac: float = 0.25,
    cap: float = 0.02,
    flat: float | None = None,
    edge_confidence: str = "Medium",
) -> dict:
    """Calculate recommended stake with Kelly and confidence scaling."""
    if flat is not None:
        base_stake = flat * bankroll
        method = f"flat {flat*100:.1f}% unit"
    else:
        f = kelly_fraction(odds, prob)
        base_stake = frac * f * bankroll
        method = f"{frac*100:.0f}% Kelly (full Kelly={f:.4f})"

    # Confidence scaling: High=1.0, Medium=0.7, Low=0.4
    conf_scale = {"High": 1.0, "Medium": 0.7, "Low": 0.4}
    scale = conf_scale.get(edge_confidence, 0.7)
    stake = base_stake * scale

    cap_amount = cap * bankroll
    capped = stake > cap_amount
    stake = min(stake, cap_amount)

    profit = stake * (odds - 1.0)

    return {
        "method": method,
        "confidence_scale": scale,
        "stake": round(stake, 2),
        "capped": capped,
        "cap_amount": round(cap_amount, 2),
        "potential_profit": round(profit, 2),
        "potential_return": round(stake + profit, 2),
        "stake_pct": round(stake / bankroll * 100, 2),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bankroll", type=float, required=True)
    ap.add_argument("--odds", type=float, required=True)
    ap.add_argument("--prob", type=float, required=True, help="model win prob 0-1")
    ap.add_argument("--frac", type=float, default=0.25, help="Kelly fraction (default 0.25)")
    ap.add_argument("--cap", type=float, default=0.02, help="max stake as bankroll fraction")
    ap.add_argument("--flat", type=float, default=None, help="flat unit fraction")
    ap.add_argument("--confidence", type=str, default="Medium",
                    choices=["High", "Medium", "Low"])
    args = ap.parse_args()

    result = calculate_stake(
        args.bankroll, args.odds, args.prob,
        frac=args.frac, cap=args.cap, flat=args.flat,
        edge_confidence=args.confidence,
    )

    print(f"method={result['method']}")
    print(f"confidence_scale={result['confidence_scale']}")
    print(f"stake={result['stake']} ({result['stake_pct']}% of bankroll)")
    if result['capped']:
        print(f"  CAPPED at {result['cap_amount']}")
    print(f"potential_profit={result['potential_profit']}")
    print(f"potential_return={result['potential_return']}")


if __name__ == "__main__":
    main()
