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
- Dedicated **50u parlay bankroll** — separate from the ~102u singles bankroll
- Fixed stake: **0.5u (1%)** per slip
- Max exposure: **3u** (≈ 6 open slips)
- **20% drawdown = pause** (50u → 40u): stop, review the playbook, restart only on agreement

## Daily workflow
1. Run the daily analysis (BSD fixtures → predictions → odds → margin-strip → edge filter)
2. Screen legs from the **same analysis** used for singles
3. Build the 2–3 leg slip (rules above); verify combined odds 1.5–2.5
4. Stake fixed 0.5u; log slip to tracker (ParlayBankroll + ParlayStats)
5. On results: settle legs → slip P&L → refresh ROI + bankroll

## Slip history
| Date | Legs | Combined odds | Stake | Result | P&L | Bankroll |
|------|------|---------------|-------|--------|-----|----------|
| 2026-08-27 | Barcelona HW 1.24 × Brighton HW 1.20 × Ajax HW 1.30 | 1.93 | 0.5u | ✅ WON | +0.465u | 50.00 → 50.465 |
| 2026-08-28 | Bayern HW 1.23 × Milan HW 1.39 | 1.71 | 0.5u | ✅ WON | +0.355u | 50.465 → 50.82 |
| 2026-08-29 | Celtic HW 1.21 × Juventus HW 1.23 × Dortmund HW 1.31 | 1.95 | 0.5u | ✅ WON | +0.475u | 50.82 → 51.295 |
| 2026-08-30 | Viking HW 1.23 × Bodø/Glimt HW 1.35 × Real Madrid O2.5 1.31 | 2.17 | 0.5u | ✅ WON | +0.585u | 51.295 → 51.88 |
| 2026-08-31 | København HW 1.34 × Sirius O2.5 1.45 | 1.94 | 0.5u | ⏳ Pending | – | 51.88 → (exposure 0.5u) |

**ParlayStats (live):** 4 settled slips × 4 wins × ROI +94.0% on stake (1.88u profit / 2.0u) × bankroll 51.88u

**Honest framing:** a parlay multiplies risk — ~43–52% combined mean it loses roughly half the time on paper. That is why it stays at 0.5u and never scales up.

## Tracking & adaptation
- Every slip logged: date, legs (match/market/selection/odds), combined odds, stake, status
- On settle: update legs, compute slip P&L, refresh ParlayBankroll/ParlayStats, running ROI
- If parlay ROI is negative over 20+ slips → shrink to 0.25u or pause
- If singles keep outperforming → parlay stays capped; it is never promoted to main strategy

## Disclaimer
Paper-trading / entertainment budget only. Not financial advice. Gamble responsibly.
