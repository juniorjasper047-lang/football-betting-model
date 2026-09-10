# Bet of the Day — Playbook (One-Pager)

**Status:** Live · **Strategy v2 (Model-Best)** · launched 2026-09-10
**Bankroll:** shares the **Model-Best Bankroll** (48.575u at launch)

## Purpose
ONE single per day. The highest model-probability selection on the slate that is still worth
staking as a standalone single. It carries the **larger stake** (1.0u vs the parlay's 0.5u)
because a single leg pays the bookmaker margin only **once**, whereas a 3-leg parlay pays it
three times over. The BOTD is therefore the least-negative-EV bet this system can produce.

## Hard rules
| # | Rule | Value |
|---|------|-------|
| 1 | Count | **exactly 1 per day** (0 is allowed — never force) |
| 2 | Stake | **1.0u flat** |
| 3 | Allowed markets | **Home Win · Over 1.5 · Over 2.5 · BTTS Yes** |
| 4 | Model probability | **>= 65%** |
| 5 | Odds window | **1.25 - 2.00** |
| 6 | Ranking | descending model probability |
| 7 | Tie-break | Home Win > Over 1.5 > Over 2.5 > BTTS Yes, then lower odds |
| 8 | Banned | Draw, Away Win, any odds > 3.00, computed edge > 25% (model error) |

## Why the 1.25 odds floor
The model's *most probable* outcome on a typical day is a heavy favourite at 1.05-1.20.
Staking a single there risks 1.00u to win 0.05-0.20u — the worst ratio on the board.
Those selections are **not discarded**: they are exactly what the Safe Parlay wants, and they
become its legs. That is why the BOTD and the parlay are built from the same ranked board.

## Team-news override
If a cross-checked source reports the favourite missing key players, or the team has a bigger
fixture immediately after (rotation risk), downgrade one tier or drop the pick. Record the
reason either way — the log matters more than the pick.

## Daily workflow
1. Fetch the BSD slate for the UTC date -> model probabilities + consensus odds
2. Build the full model board, ranked by probability
3. Drop out-of-scope leagues, away-favourite-only matches, and ban-list markets
4. Take rank #1 among eligible selections (odds >= 1.25, model >= 65%)
5. Team-news cross-check (SportsMole + one other source)
6. Stake 1.0u; log to `tracker.csv` (tag `BOTD`)
7. Settle next session -> results file -> refresh stats below

## History
| Date | Match | Selection | Odds | Model % | Stake | Result | P&L |
|------|-------|-----------|------|---------|-------|--------|-----|
| 2026-09-10 | PSV Eindhoven vs Shakhtar Donetsk | Home Win | 1.42 | 66.3% | 1.00u | PENDING | - |

## Stats
- Picks: **1** · Won 0 · Lost 0 · Pending 1
- Staked: 1.00u · Returned: 0.00u · Net: 0.00u · ROI: n/a
- Bankroll: **48.575u**

## Notes
- **2026-09-10 (launch):** PSV Home Win @1.42 taken as rank #1 of eligible selections.
  Ranked above it by raw probability — but excluded by the 1.25 odds floor — were
  Bayern HW 86.3% @1.10, Man Utd HW 85.5% @1.11, Bayern O2.5 83.3% @1.12, PSV O1.5 83.8% @1.12
  and Como O1.5 81.0% @1.16. All five went into the parlay candidate pool instead.
  Risk flagged at selection time: PSV had lost each of their previous five CL matchday-one
  fixtures, and four of their last five CL home games.
- **No-bet days are logged too.** A "No Bet of the Day" is a valid, expected outcome — never
  force a pick to fill the slot. The selection bar exists to stop that.

## Honest framing
The model is market-derived, so `model_prob ~= fair_prob` and **EV ~= -(bookmaker margin)**
(~ -5% on a single 1X2 leg). This is a high-hit-rate, low-payout approach, **not** a value bet.
The only datapoint hinting at real edge is the 15/15 Home Win leg record on settled parlays,
which may indicate the market mildly under-prices short home favourites.

## Disclaimer
Paper-trading / entertainment budget only. Not financial advice. Gamble responsibly.
