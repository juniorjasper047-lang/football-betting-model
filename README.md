# Football Betting Model — Automated Value Betting System

Daily automated football analysis across 15 European leagues. Poisson model + form adjustment + odds comparison → value bets with Kelly staking.

## Leagues Tracked

| # | League | Country | Season |
|---|--------|---------|--------|
| 1 | Champions League Qualifiers | Europe | Jul–Aug 2026 |
| 2 | Europa League Qualifiers | Europe | Jul–Aug 2026 |
| 3 | Conference League Qualifiers | Europe | Jul–Aug 2026 |
| 4 | Fortuna Liga | Czech Republic | Jul–May |
| 5 | Superliga | Denmark | Jul–May |
| 6 | Veikkausliiga | Finland | Apr–Oct |
| 7 | Úrvalsdeild | Iceland | Apr–Oct |
| 8 | Eliteserien | Norway | Mar–Nov |
| 9 | Premier League | Russia | Jul–May |
| 10 | Super Liga | Serbia | Jul–May |
| 11 | Allsvenskan | Sweden | Mar–Nov |
| 12 | Super League | Switzerland | Jul–May |
| 13 | Bundesliga | Austria | Jul–May |
| 14 | HNL | Croatia | Jul–May |
| 15 | Scottish Premiership | Scotland | Aug–May |

## Daily Workflow

```
06:00 UTC — Analyze all fixtures, generate picks → data/picks/YYYY-MM-DD.md
22:00 UTC — Fetch results, settle picks, update tracker → data/results/YYYY-MM-DD.md
```

## Dashboard

Live dashboard: [football-betting-model.vercel.app](https://football-betting-model.vercel.app)

## Repository Structure

```
├── data/
│   ├── picks/          # Daily pick files (YYYY-MM-DD.md)
│   ├── results/        # Settled results + lessons
│   └── tracker.csv     # Master tracker with all bets
├── scripts/
│   ├── analyze.py      # Main analysis engine (cron morning)
│   ├── settle.py       # Results settlement (cron evening)
│   ├── model.py        # Poisson model wrapper
│   ├── value.py        # Value/EV calculator
│   ├── kelly.py        # Kelly staking calculator
│   └── odds_convert.py # Odds conversion utilities
├── dashboard/          # Next.js dashboard
└── README.md
```

## Methodology

1. **Scope** — Identify fixtures in active leagues
2. **Gather** — Recent form, H2H, injuries, odds from multiple books
3. **Filter** — Remove dead rubbers, friendlies, low-information surfaces
4. **Model** — Poisson expected goals + game-state adjustment
5. **Value** — Compare model probability to bookmaker implied probability
6. **Stake** — Fractional Kelly scaled by edge confidence
7. **Log** — Write picks to markdown + tracker CSV
8. **Settle** — Update with results + lessons learned

## Strategy Rules

- ⚠️ **Paper only** until 50+ bet sample shows positive ROI
- ❌ No away-team 1X2 bets in Brazil
- ❌ No MLS (chaos league)
- ❌ No club friendlies (invisible lineups)
- ✅ O2.5 and BTTS preferred over 1X2
- ✅ European qualifiers given highest weight
- ✅ Proportional stakes by edge confidence
- ✅ Dead rubber matches skipped
- ✅ Edge threshold: ≥ 5% to bet, ≥ 2% marginal, < 2% skip

## Edge Model

```
edge = model_probability − bookmaker_true_implied
EV = model_prob × (odds − 1) − (1 − model_prob)
Stake = confidence_scaled × fractional_kelly × bankroll
```

⚠️ **Disclaimer:** This is a paper-trading model for research and analysis. Not financial advice. Historical performance does not guarantee future results. Gamble responsibly.
