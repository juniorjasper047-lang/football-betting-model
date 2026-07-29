# Freak Bets Tracking Project

**Source:** @freakbets Telegram channel (betting tips)
**Started:** 2026-07-28
**Tracker:** `football-betting-tracker.xlsx`

## Goal
Track every tip Jasper forwards from Freak Bets to build a real, unbiased P&L record. Cross-check picks against model probabilities where possible.

## How it works
1. Jasper forwards a tip/slip from Freak Bets to Cosmos
2. Cosmos logs it to the tracker (date, match, market, odds, stake, source)
3. On results: settle (win/loss/push), update P&L, calculate running ROI
4. Periodic review: accuracy by market, CLV, whether the tipster is actually +EV

## Forward format (anything goes, but ideally include)
- Teams/match
- Market (1X2, over/under, BTTS, etc.)
- Selection (which side)
- Odds
- Any stake mentioned
- Screenshot or text — either works

## Known patterns
- **Bet of the Day (BOTD)**: One featured single bet posted daily. Always a single, never a parlay.
- Additional picks sometimes posted alongside the BOTD.
- All picks shown as the channel's own bet slips with large stakes (€1,000+).

## Pick log

### 2026-07-28
| Type | Match | League | Market | Pick | Odds | Stake |
|------|-------|--------|--------|------|------|-------|
| **BOTD** | CSKA Sofia 1948 vs Spartak Trnava | Conf. League Q | 1X2 | CSKA W | 1.91 | 1,090€ |
| Extra | Celje vs Egnatia | UCL Q | 1X2 | Celje W | 1.616 | 3,500€ |
| Extra | KuPS vs Sabah Baku | UCL Q | 1H Over 1 | Over | 1.67 | 2,500€ |

### 2026-07-28 Results
| Type | Match | Pick | Odds | Result | P&L |
|------|-------|------|------|--------|-----|
| **BOTD** | CSKA Sofia 1948 vs Trnava | CSKA W | 1.91 | 0-0 (L) | -1,090€ |
| Extra | Celje vs Egnatia | Celje W | 1.616 | 1-1 (L) | -3,500€ |
| Extra | KuPS vs Sabah Baku | 1H O1 | 1.67 | HT 0-0 (L) | -2,500€ |

**Day 1: 0-3 (0%) | -7,090€ | ROI: -100%**

---

### 2026-07-29
| Type | Nº | Match | League | Market | Pick | Odds | Stake |
|------|----|-------|--------|--------|------|------|-------|
| Extra | — | Kauno Žalgiris vs Klaksvík + Lech Poznań vs AGF | UCL Q | Parlay (2-leg) | U2.5 + AGF O0.5 | 2.271 | 800€ |
| Extra | 84999596319 | Red Star vs Larne | UCL Q | Handicap | Red Star (-2.5) | 1.625 | 1,600€ |
| Extra | 84981662705 | Miami Marlins vs Phillies | MLB | 1X2 | Miami W | 1.74 | 2,500€ |

### 2026-07-29 Results
| Type | Nº | Match | Pick | Odds | Score | Result | P&L |
|------|----|-------|------|------|-------|--------|-----|
| Extra | — | Žalgiris U2.5 + AGF O0.5 | Parlay 2-leg | 2.271 | 1-0 + 1-4 | ✅ WON | **+1,016.96€** |
| Extra | 84999596319 | Red Star vs Larne | Red Star (-2.5) | 1.625 | 5-0 | ✅ WON | **+1,000€** |
| Extra | 84981662705 | Marlins vs Phillies | Miami W | 1.74 | Won | ✅ WON | **+1,850€** |

**Day 2: 3-0 (100%) | +3,866.96€ | ROI: +78.9% 🔥**

**Running total: 3W 3L | Staked: 11,990€ | P/L: -3,223.04€**

## Daily Automation (cron)
- **08:00 UTC** — Daily value betting scan across leagues
- **09:00 UTC** — Football betting infrastructure healthcheck
- **22:00 UTC** — Auto-settle open Freak Bets picks from results

## Notes
