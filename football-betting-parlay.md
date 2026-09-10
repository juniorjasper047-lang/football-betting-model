# Safe Parlay — Playbook (One-Pager)

**Status:** Live · **Strategy v2 (Model-Best)** · rewritten 2026-09-10
*(was "Daily Parlay", the small-stakes companion to Value Singles — Value Singles are now RETIRED)*

## Purpose
**One** high-probability accumulator per day, posted alongside the **Bet of the Day**.
"Safe" means *maximising the chance the slip lands*, **not** maximising the payout.

## Why the strategy changed (2026-09-10)
The BSD `dc-blend-v1` model is **market-derived** — on 37/37 fixtures tested its probabilities
matched margin-stripped consensus odds within ~1pp. So `edge = model_prob - true_implied` is
**~0 by construction**, and value/edge hunting produced a fake signal plus chronic paralysis
(0 value singles on 8 of the last 10 betting days). Picks are now ranked by **model probability**
instead of edge. Value Singles are retired permanently.

## Hard rules (leg selection)
| # | Rule | Value |
|---|------|-------|
| 1 | Allowed markets | **Home Win · Over 1.5 · Over 2.5 · BTTS Yes** |
| 2 | Banned | Draw, Away Win, handicaps, player props, any odds > 3.00 |
| 3 | Model probability per leg | **>= 70%** |
| 4 | Odds per leg | **1.05 - 1.60** |
| 5 | Legs | **2 by default**; a 3rd only if 2 legs cannot reach combined 1.35 |
| 6 | Same match | Never 2 legs from the same match |
| 7 | Combined odds target | **1.30 - 1.80** |
| 8 | Minimum qualifying legs | 2 — if fewer, **no parlay that day** |
| 9 | Slips per day | **exactly 1** |
| 10 | Overlap with Bet of the Day | at most 1 shared leg |

**Leg preference order:** Home Win -> Over 1.5 -> Over 2.5 -> BTTS Yes.
**Never stack 2+ Over 2.5 legs** (9/18 on this account; cause of most losses: Sirius 0-1,
Schalke 0-0, Betis 1-0, Aalesund 2-0, AEK 1-0).

## Staking & bankroll
- Shares the **Model-Best Bankroll** — **48.575u** at 2026-09-10 (the old 50u parlay bankroll carried over)
- Fixed stake **0.5u** per slip · combined daily exposure (BOTD + parlay) <= **1.5u**
- **20% drawdown (bankroll < 38.86u) = pause** and review

## Why only ONE slip per day
Both multi-slip experiments lost money, and for the same reason:

| Day | Slips | Result | Cause |
|-----|-------|--------|-------|
| 2026-08-31 | 4 x 0.5u | **-1.135u** | 3 of 4 slips shared the Sirius Over 2.5 leg (0-1) |
| 2026-09-04 | 5 x 0.5u | **-1.495u** | 2 slips shared Betis-Madrid Over 2.5 (1-0) |

Splitting one bankroll across slips built on the same matches is **correlation, not diversification**.

## Daily workflow
1. Fetch the BSD slate for the UTC date -> model probabilities + consensus odds
2. Rank all selections by model probability
3. Screen legs: >= 70% model, odds 1.05-1.60, distinct matches, max one Over 2.5
4. Take the top 2 (add a 3rd only if combined odds < 1.35); verify combined 1.30-1.80
5. Team-news cross-check every leg (SportsMole + one other source)
6. Stake 0.5u; log legs to `tracker.csv` (tag `SAFE PARLAY`)
7. On results: settle every leg -> slip P&L -> refresh ROI + bankroll

## Slip history
| Date | Legs | Combined odds | Stake | Result | P&L | Bankroll |
|------|------|---------------|-------|--------|-----|----------|
| 2026-08-27 | Barcelona HW 1.24 x Brighton HW 1.20 x Ajax HW 1.30 | 1.93 | 0.5u | WON | +0.465u | 50.000 -> 50.465 |
| 2026-08-28 | Bayern HW 1.23 x Milan HW 1.39 | 1.71 | 0.5u | WON | +0.355u | 50.465 -> 50.820 |
| 2026-08-29 | Celtic HW 1.21 x Juventus HW 1.23 x Dortmund HW 1.31 | 1.95 | 0.5u | WON | +0.475u | 50.820 -> 51.295 |
| 2026-08-30 | Viking HW 1.23 x Bodo/Glimt HW 1.35 x Real Madrid O2.5 1.31 | 2.17 | 0.5u | WON | +0.585u | 51.295 -> 51.880 |
| 2026-08-31 | Kobenhavn HW 1.34 x Sirius O2.5 1.45 | 1.94 | 0.5u | LOST | -0.5u | 51.880 -> 51.380 |
| 2026-08-31 | Kobenhavn O2.5 1.46 x Sirius O2.5 1.45 | 2.12 | 0.5u | LOST | -0.5u | 51.380 -> 50.880 |
| 2026-08-31 | Kobenhavn HW 1.34 x Barcelona O2.5 1.29 | 1.73 | 0.5u | WON | +0.365u | 50.880 -> 51.245 |
| 2026-08-31 | Sirius O2.5 1.45 x Ilves O2.5 1.51 | 2.19 | 0.5u | LOST | -0.5u | 51.245 -> 50.745 |
| 2026-09-02 | Celtic HW 1.24 x Luzern O2.5 1.33 | 1.65 | 0.5u | WON | +0.325u | 50.745 -> 51.070 |
| 2026-09-04 | Lyon HW 1.48 x Stuttgart O2.5 1.36 | 2.01 | 0.5u | WON | +0.505u | 51.070 -> 51.575 |
| 2026-09-04 | Betis-Madrid O2.5 1.37 x Ipswich-LIV O2.5 1.40 | 1.92 | 0.5u | LOST | -0.5u | 51.575 -> 51.075 |
| 2026-09-04 | Fredrikstad-Glimt O2.5 1.36 x Aalesund-Start O2.5 1.47 | 2.00 | 0.5u | LOST | -0.5u | 51.075 -> 50.575 |
| 2026-09-04 | Stuttgart HW 1.49 x Sandefjord-Viking O2.5 1.45 | 2.16 | 0.5u | LOST | -0.5u | 50.575 -> 50.075 |
| 2026-09-04 | Lyon HW 1.48 x Betis-Madrid O2.5 1.37 | 2.03 | 0.5u | LOST | -0.5u | 50.075 -> 49.575 |
| 2026-09-05 | Bayern-Schalke O2.5 1.22 x Brann-Lillestrom O2.5 1.43 | 1.74 | 0.5u | LOST | -0.5u | 49.575 -> 49.075 |
| 2026-09-08 | AEK Athens O2.5 1.63 x Dortmund O2.5 1.46 | 2.38 | 0.5u | LOST | -0.5u | 49.075 -> 48.575 |
| 2026-09-10 | Bayern HW 1.10 x Man Utd HW 1.11 x PSV O1.5 1.12 | 1.37 | 0.5u | PENDING | - | 48.575 -> |

**ParlayStats (live):** 16 settled slips x 7W-9L x net **-1.425u** on 8.0u staked x **ROI -17.8%** x bankroll **48.575u** (17th slip pending)
**Leg-level record:** Home Win **15/15** · Over 2.5 **9/18** · Draw/Away 0/0 attempted

**2026-09-08 settlement:** 1 slip @0.5u -> **LOST -0.5u**. AEK Athens 1-0 LASK Linz (O2.5 ✗); Borussia Dortmund 3-2 Villarreal (O2.5 ✓). Bankroll 49.075 -> 48.575u. Both legs were Over 2.5 again — the market that accounts for 9 of the 18 Over 2.5 legs and most losses.

**2026-09-09:** no picks logged (CL matchday not analysed; 0 exposure).

**2026-09-10 (strategy v2 launch):** 1 slip @0.5u -> **Bayern HW 1.10 x Man Utd HW 1.11 x PSV O1.5 1.12 = 1.37** (combined model 61.8%). All three legs >= 83.8% model. Third leg added because the top two legs only reached 1.221 (< 1.35 floor). Leg 3 shares the PSV match with the Bet of the Day (allowed: max 1 shared leg).

**Honest framing:** every leg carries the bookmaker margin, so a slip's EV ~= -(margin x legs). A 3-leg slip is roughly a **-15% EV bet**. This is a hit-rate / variance play, **not** a value bet. Expect to lose the slip about 4 times in 10. That is why it stays at 0.5u and never scales up.

## Tracking & adaptation
- Every slip logged: date, legs (match/market/selection/odds), combined odds, stake, status, scorelines
- On settle: update legs, compute slip P&L, refresh ParlayBankroll/ParlayStats, running ROI
- If parlay ROI is negative over 20+ slips -> shrink to 0.25u or pause
- The parlay is **never** promoted above the Bet of the Day

## Disclaimer
Paper-trading / entertainment budget only. Not financial advice. Gamble responsibly.
