# Daily Parlay — Playbook (One-Pager)

**Status:** Live · small-stakes companion to Value Singles · tracked in the same repo

## Purpose
A "safe picks" accumulator posted daily alongside the value singles. It gives the parlay experience while mirroring the singles' market discipline — capped, separate bankroll, and never the main strategy.

## Why it exists separately
- **Value Singles** chase positive EV with edge-based staking → the primary money-maker.
- **Daily Parlay** = the 1% entertainment budget with the same market rules.
- Both log to the same tracker → ROI is measurable; if either stops performing, the record shows it and the rules adapt.

## Hard rules (leg selection)
| # | Rule | Value |
|---|------|-------|
| 1 | Allowed markets | **Home Win, Over 2.5 only** (proven: HW 75% win / +42% ROI; O2.5 58% / +52% ROI) |
| 2 | Banned | Draw, Away Win, BTTS, handicaps, player props |
| 3 | Model probability per leg | ≥ 60% |
| 4 | Odds per leg | 1.15 – 2.50 |
| 5 | Max legs | 3 (prefer 2) |
| 6 | Same match | Never 2 legs from the same match |
| 7 | Combined odds target | 1.5 – 2.5 |
| 8 | Minimum qualifying legs | 2 — if fewer, **no parlay that day** |

## Staking & bankroll
- Dedicated **50u parlay bankroll** — separate from the ~101u singles bankroll
- Fixed stake: **0.5u (1%)** per slip
- Max exposure: **3u** (≤ 6 open slips)
- **20% drawdown = pause** (50u → 40u): stop, review the playbook, restart only on agreement

## Daily workflow
1. Run the daily analysis (BSD fixtures → predictions → odds → margin-strip → edge filter)
2. Screen legs from the **same analysis** used for singles
3. Build the 2–3 leg slip (rules above); verify combined odds 1.5–2.5
4. Stake fixed 0.5u; log slip to tracker (ParlayBankroll + ParlayStats)
5. On results: settle legs → slip P&L → refresh ROI + bankroll

## Example slip (2026-08-27)
| Leg | Match | Market | Model | Odds |
|-----|-------|--------|-------|------|
| 1 | Arsenal (home) | Home Win | 80.7% | ~1.32 |
| 2 | Sirius (home) | Over 2.5 | 70.6% | ~1.71 |
| 3 | Marseille (home) | Over 2.5 | 61.5% | ~1.63 |

- Combined odds: **≈ 2.48**
- Combined model probability: **≈ 35%**
- Stake: **0.5u** · Potential return ≈ **1.24u**

**Honest framing:** a parlay multiplies risk — ~35% combined means it loses roughly 2/3 of the time. That is why it stays at 0.5u and never scales up.

## Tracking & adaptation
- Every slip logged: date, legs (match/market/selection/odds), combined odds, stake, status
- On settle: update legs, compute slip P&L, refresh ParlayBankroll/ParlayStats, running ROI
- If parlay ROI is negative over 20+ slips → shrink to 0.25u or pause
- If singles keep outperforming → parlay stays capped; it is never promoted to main strategy

## Disclaimer
Paper-trading / entertainment budget only. Not financial advice. Gamble responsibly.