#!/usr/bin/env python3
"""Full daily report for 2026-07-29 — UCL Qual + Conference League Qual."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import MatchInput, run_model
from value import calculate_value
from math import log

# UEFA Club Coefficients (2026)
COEFF = {
    # UCL Qual teams
    "Fenerbahce": 57.75, "Red Star": 46.5, "Slovan Bratislava": 36.0,
    "Lech Poznan": 27.25, "Omonia": 21.25, "Hapoel Beer-Sheva": 14.0,
    "Vikingur Reykjavik": 11.75, "Kairat": 11.0, "Univ Craiova": 10.5,
    "Klaksvik": 10.5, "Gornik Zabrze": 9.35, "Larne": 9.0, "AGF": 8.42,
    "Levski Sofia": 7.0, "Kauno Zalgiris": 6.0, "Iberia 1999": 5.0,
    # Conference League teams
    "Copenhagen": 54.375, "Rapid Wien": 29.75, "Lugano": 21.25,
    "Polissya Zhytomyr": 5.18, "Dukagjini": 5.0, "FC Santa Coloma": 5.0,
}

def coeff_to_att(c):
    if c >= 50: return 2.2
    if c >= 30: return 1.8
    if c >= 20: return 1.6
    if c >= 12: return 1.4
    if c >= 8: return 1.2
    if c >= 6: return 1.1
    return 0.9

def coeff_to_def(c):
    if c >= 50: return 0.6
    if c >= 30: return 0.8
    if c >= 20: return 1.0
    if c >= 12: return 1.2
    if c >= 8: return 1.5
    if c >= 6: return 1.6
    return 1.8

MARKETS = [
    ("O25", "Over 2.5", "O25"),
    ("BTTS_Y", "BTTS Yes", "BTTS_Y"),
    ("1", "Home Win", "1"),
    ("X", "Draw", "X"),
    ("2", "Away Win", "2"),
]

BANKROLL = 100.0

# =============================================================================
# ALL MATCHES: UCL Qual + Conference League Qual
# =============================================================================

MATCHES = [
    # === UCL QUALIFIERS (already analyzed, included for completeness) ===
    {
        "home": "Kairat Almaty", "away": "Omonia Nicosia",
        "league": "UCL Qual", "league_avg": 2.65, "home_adv": 0.30,
        "is_2nd_leg": True, "first_leg": "0-1", "def_adj": 0.0,
        "odds": {"1": 2.08, "X": 3.28, "2": 3.43, "O25": 2.13, "U25": 1.66, "BTTS_Y": 1.91},
    },
    {
        "home": "Kauno Zalgiris", "away": "KI Klaksvik",
        "league": "UCL Qual", "league_avg": 2.60, "home_adv": 0.25,
        "is_2nd_leg": True, "first_leg": "0-0", "def_adj": 0.0,
        "odds": {"1": 1.73, "X": 3.55, "2": 4.80, "O25": 1.98, "U25": 1.77, "BTTS_Y": 1.83},
    },
    {
        "home": "Lech Poznan", "away": "AGF Aarhus",
        "league": "UCL Qual", "league_avg": 2.70, "home_adv": 0.35,
        "is_2nd_leg": True, "first_leg": "4-1", "def_adj": -0.15,
        "odds": {"1": 1.71, "X": 3.83, "2": 4.48, "O25": 1.72, "U25": 1.99, "BTTS_Y": 1.71},
    },
    {
        "home": "Univ Craiova", "away": "Levski Sofia",
        "league": "UCL Qual", "league_avg": 2.55, "home_adv": 0.30,
        "is_2nd_leg": True, "first_leg": "0-1", "def_adj": 0.0,
        "odds": {"1": 1.90, "X": 3.45, "2": 4.00, "O25": 2.06, "U25": 1.74, "BTTS_Y": 1.87},
    },
    {
        "home": "H. Beer-Sheva", "away": "Vikingur Reykjavik",
        "league": "UCL Qual", "league_avg": 2.70, "home_adv": 0.30,
        "is_2nd_leg": True, "first_leg": "1-2", "def_adj": 0.10,
        "odds": {"1": 1.57, "X": 3.80, "2": 5.15, "O25": 1.70, "U25": 2.09, "BTTS_Y": 1.72},
    },
    {
        "home": "Red Star Belgrade", "away": "Larne",
        "league": "UCL Qual", "league_avg": 2.80, "home_adv": 0.25,
        "is_2nd_leg": True, "first_leg": "4-0", "def_adj": -0.20,
        "odds": {"1": 1.07, "X": 12.50, "2": 32.00, "O25": 1.29, "U25": 3.45, "BTTS_Y": 2.67},
    },
    {
        "home": "Slovan Bratislava", "away": "Iberia 1999",
        "league": "UCL Qual", "league_avg": 2.60, "home_adv": 0.30,
        "is_2nd_leg": True, "first_leg": "2-0", "def_adj": -0.05,
        "odds": {"1": 1.37, "X": 4.93, "2": 7.50, "O25": 1.61, "U25": 2.28, "BTTS_Y": 1.91},
    },
    {
        "home": "Gornik Zabrze", "away": "Fenerbahce",
        "league": "UCL Qual League Path", "league_avg": 2.55, "home_adv": 0.25,
        "is_2nd_leg": True, "first_leg": "0-1", "def_adj": 0.0,
        "odds": {"1": 6.65, "X": 4.50, "2": 1.45, "O25": 1.73, "U25": 1.99, "BTTS_Y": 1.91},
    },
    # === CONFERENCE LEAGUE QUALIFIERS (NEW) ===
    # Dukagjini (KOS) vs Lugano (SUI) — 1st leg 0-1, Lugano leads
    {
        "home": "Dukagjini", "away": "Lugano",
        "league": "Conf Lge Qual", "league_avg": 2.70, "home_adv": 0.30,
        "is_2nd_leg": True, "first_leg": "0-1", "def_adj": 0.0,
        "odds": {"1": 5.17, "X": 3.85, "2": 1.63, "O25": 1.80, "U25": 2.00, "BTTS_Y": 1.83},
    },
    # Copenhagen (DEN) vs Polissya Zhytomyr (UKR) — 1st leg 3-3, wide open
    {
        "home": "Copenhagen", "away": "Polissya Zhytomyr",
        "league": "Conf Lge Qual", "league_avg": 2.80, "home_adv": 0.35,
        "is_2nd_leg": True, "first_leg": "3-3", "def_adj": 0.10,
        "odds": {"1": 1.72, "X": 3.85, "2": 4.38, "O25": 1.70, "U25": 2.18, "BTTS_Y": 1.64},
    },
    # Rapid Wien (AUT) vs FC Santa Coloma (AND) — 1st leg 3-1, Rapid leads
    {
        "home": "Rapid Wien", "away": "FC Santa Coloma",
        "league": "Conf Lge Qual", "league_avg": 2.70, "home_adv": 0.35,
        "is_2nd_leg": True, "first_leg": "3-1", "def_adj": -0.10,
        "odds": {"1": 1.10, "X": 8.50, "2": 19.00, "O25": 1.48, "U25": 2.45, "BTTS_Y": 2.10},
    },
]

def get_model_prob(out, market_key):
    if market_key == "O25": return out.prob_over_2_5
    elif market_key == "BTTS_Y": return out.prob_btts
    elif market_key == "1": return out.prob_home
    elif market_key == "X": return out.prob_draw
    elif market_key == "2": return out.prob_away
    return 0

# =============================================================================
# RUN MODEL
# =============================================================================

results = []
leagues_analyzed = set()

for m in MATCHES:
    home_coeff = COEFF.get(m["home"], 10)
    away_coeff = COEFF.get(m["away"], 10)

    inp = MatchInput(
        home=m["home"], away=m["away"], league=m["league"],
        home_att=coeff_to_att(home_coeff), home_def=coeff_to_def(home_coeff),
        away_att=coeff_to_att(away_coeff), away_def=coeff_to_def(away_coeff),
        league_avg_gpg=m["league_avg"], home_advantage=m["home_adv"],
        first_leg_score=m["first_leg"], is_second_leg=m["is_2nd_leg"],
        defense_adj=m["def_adj"],
    )
    out = run_model(inp)
    odds = m["odds"]
    leagues_analyzed.add(m["league"])

    print(f"\n{'='*60}")
    print(f"{m['home']} vs {m['away']} ({m['league']})")
    print(f"First leg: {m['first_leg']} | Game State: {out.game_state_label}")
    print(f"Expected goals: H={out.home_expected} A={out.away_expected} T={out.total_expected}")
    print(f"1X2: {out.prob_home:.1%} / {out.prob_draw:.1%} / {out.prob_away:.1%}")
    print(f"O2.5: {out.prob_over_2_5:.1%} | BTTS: {out.prob_btts:.1%}")
    print(f"Predicted: {out.predicted_score} | Conf: {out.confidence}")

    picks = []
    for mkt_key, mkt_name, odds_key in MARKETS:
        if odds_key not in odds: continue
        true_prob = get_model_prob(out, mkt_key)
        odd = odds[odds_key]
        val = calculate_value(true_prob, odd)
        edge = val["edge"]
        ev = val["ev"]
        edge_pct = edge * 100

        print(f"  {mkt_name} @{odd}: model={true_prob:.3f} implied={val['implied']:.3f} edge={edge_pct:+.1f}% EV={ev:+.3f}")

        if edge_pct >= 5.0:
            if edge_pct > 12:
                stake = 0.75
                conf_label = "High"
            elif edge_pct > 7:
                stake = 0.50
                conf_label = "Medium"
            else:
                stake = 0.30
                conf_label = "Low"

            picks.append({
                "home": m["home"], "away": m["away"],
                "match": f"{m['home']} vs {m['away']}",
                "league": m["league"], "market": mkt_name,
                "selection": "Yes" if mkt_key in ("O25", "BTTS_Y") else mkt_name,
                "odds": odd, "model_prob": true_prob,
                "true_implied": val["implied"], "edge_pct": edge_pct,
                "edge": edge, "ev": ev, "stake": stake,
                "game_state": out.game_state_label, "confidence": out.confidence,
                "expected_goals": f"H={out.home_expected} A={out.away_expected} T={out.total_expected}",
                "predicted_score": out.predicted_score,
                "odds_key": mkt_key,
                "xg_home": out.home_expected, "xg_away": out.away_expected,
                "xg_total": out.total_expected,
            })

    results.append({"match": m, "model_out": out, "odds": odds, "picks": picks})

# =============================================================================
# SUMMARY
# =============================================================================

all_picks = []
for r in results:
    all_picks.extend(r["picks"])

all_picks.sort(key=lambda p: p["edge_pct"], reverse=True)

print(f"\n{'='*60}")
print(f"TOTAL VALUE PICKS FOUND: {len(all_picks)}")
print(f"LEAGUES ANALYZED: {', '.join(sorted(leagues_analyzed))}")
print(f"{'='*60}")

for i, p in enumerate(all_picks, 1):
    print(f"\n--- Pick #{i} ---")
    print(f"  {p['league']}: {p['match']}")
    print(f"  Market: {p['market']} @ {p['odds']}")
    print(f"  Model: {p['model_prob']:.1%} | Implied: {p['true_implied']:.1%} | Edge: {p['edge_pct']:.1f}%")
    print(f"  EV: {p['ev']:+.3f} | Stake: ${p['stake']:.2f} | GS: {p['game_state']}")

# =============================================================================
# CSV LINES FOR TRACKER
# =============================================================================

print("\n\n--- CSV LINES FOR TRACKER (NEW CONF LGE ONLY) ---")
new_picks = [p for p in all_picks if "Conf" in p["league"]]
for p in new_picks:
    line = f"2026-07-29,{p['league']},{p['home']},{p['away']},{p['market']},{p['selection']},{p['odds']},SportyBet,{p['model_prob']:.4f},{p['true_implied']:.4f},{p['edge']:.4f},{p['ev']:.4f},{p['stake']:.2f},{BANKROLL:.2f},open,"
    print(line)

# Full JSON output
output = {
    "date": "2026-07-29",
    "leagues_analyzed": sorted(leagues_analyzed),
    "leagues_with_no_fixtures": [
        "Premier League (pre-season only)", "LaLiga (starts Aug 15)", 
        "Serie A (starts Aug)", "Bundesliga (starts Aug 28-30)",
        "Ligue 1 (starts Aug)", "Europa League Qualifiers (next: July 30)"
    ],
    "total_fixtures": len(MATCHES),
    "picks_found": len(all_picks),
    "picks": all_picks,
}
print("\n--- JSON ---")
print(json.dumps(output, indent=2, default=str))
