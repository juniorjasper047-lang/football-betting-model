#!/usr/bin/env python3
"""Morning pick generation for 2026-08-01 (Saturday).

Confirmed fixtures across all 15 tracked leagues. Heavy Saturday with Eliteserien,
Allsvenskan, Veikkausliiga, Czech Liga, Austria Bundesliga, Swiss Super League,
Scottish Premiership (MD1), Russia Premier League, Croatia HNL, Denmark Superliga,
and Iceland ongoing.

No UEFA qualifier fixtures (Q3 starts Aug 4-6). No Serbia Super Liga fixtures found.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import MatchInput, run_model
from value import calculate_value

BANKROLL = 100.0
DATE = "2026-08-01"

# Markets to evaluate. Prefer O2.5 / BTTS; 1X2 only with exceptional edge.
MARKETS = [
    ("O25", "Over 2.5", "O25"),
    ("BTTS_Y", "BTTS Yes", "BTTS_Y"),
    ("1", "Home Win", "1"),
    ("X", "Draw", "X"),
    ("2", "Away Win", "2"),
]

# League average goals per game (season/summer data):
LEAGUE_AVGS = {
    "Denmark Superliga": 2.70,
    "Eliteserien": 2.90,
    "Allsvenskan": 2.75,
    "Veikkausliiga": 2.60,
    "Czech Liga": 2.65,
    "Iceland Urvalsdeild": 2.95,
    "Austria Bundesliga": 2.75,
    "Croatia HNL": 2.55,
    "Swiss Super League": 2.85,
    "Scottish Premiership": 2.55,
    "Russia Premier League": 2.50,
}

FIXTURES = [
    # ── Denmark Superliga ──
    {
        "home": "Lyngby", "away": "AGF", "league": "Denmark Superliga",
        "home_att": 1.20, "home_def": 1.55, "away_att": 1.55, "away_def": 1.15,
        "home_advantage": 0.25, "odds": {
            "1": 3.25, "X": 3.65, "2": 2.05,
            "O25": 1.85, "BTTS_Y": 1.78,
        },
        "odds_source": "FanDuel/ESPN/SportyTrader (Jul 31-Aug 1 2026)",
        "kickoff": "12:00 UTC", "venue": "Lyngby Stadion, Lyngby",
        "notes": "AGF away fav; strong defensive record."
    },
    # ── Norway Eliteserien ──
    {
        "home": "Fredrikstad", "away": "Sandefjord", "league": "Eliteserien",
        "home_att": 1.45, "home_def": 1.30, "away_att": 1.20, "away_def": 1.60,
        "home_advantage": 0.30, "odds": {
            "1": 2.35, "X": 3.40, "2": 3.05,
            "O25": 1.74, "BTTS_Y": 1.54,
        },
        "odds_source": "Sportsgambler/ESPN/DraftKings (Aug 1 2026)",
        "kickoff": "08:00 UTC", "venue": "Fredrikstad Stadion",
        "notes": "Fredrikstad home slight fav; O2.5/BTTS favored in market."
    },
    {
        "home": "IK Start", "away": "Viking FK", "league": "Eliteserien",
        "home_att": 1.15, "home_def": 1.65, "away_att": 1.85, "away_def": 1.10,
        "home_advantage": 0.30, "odds": {
            "1": 5.40, "X": 4.35, "2": 1.51,
            "O25": 1.48, "BTTS_Y": 1.70,
        },
        "odds_source": "Sportsgambler/ESPN/DraftKings (Aug 1 2026)",
        "kickoff": "10:00 UTC", "venue": "Sparebanken Sor Arena, Kristiansand",
        "notes": "Viking heavy away fav; high goals expected (O2.5=1.48)."
    },
    # ── Sweden Allsvenskan ──
    {
        "home": "BK Hacken", "away": "Kalmar FF", "league": "Allsvenskan",
        "home_att": 1.70, "home_def": 1.15, "away_att": 1.10, "away_def": 1.50,
        "home_advantage": 0.30, "odds": {
            "1": 1.72, "X": 4.00, "2": 4.20,
            "O25": 1.50, "BTTS_Y": 1.65,
        },
        "odds_source": "Sportsgambler/SportyTrader (Aug 1 2026)",
        "kickoff": "09:00 UTC", "venue": "Bravida Arena, Gothenburg",
        "notes": "Hacken clear home fav; market expects O2.5 goals."
    },
    # ── Finland Veikkausliiga ──
    {
        "home": "TPS", "away": "Mariehamn", "league": "Veikkausliiga",
        "home_att": 1.55, "home_def": 1.20, "away_att": 1.05, "away_def": 1.55,
        "home_advantage": 0.25, "odds": {
            "1": 1.53, "X": 4.00, "2": 5.20,
            "O25": 1.72, "BTTS_Y": 1.85,
        },
        "odds_source": "Oddschecker/BBC (Aug 1 2026)",
        "kickoff": "10:00 UTC", "venue": "Veritas Stadion, Turku",
        "notes": "TPS heavy home fav; MD18."
    },
    {
        "home": "Lahti", "away": "Jaro", "league": "Veikkausliiga",
        "home_att": 1.40, "home_def": 1.35, "away_att": 1.20, "away_def": 1.50,
        "home_advantage": 0.25, "odds": {
            "1": 1.66, "X": 3.98, "2": 4.80,
            "O25": 1.78, "BTTS_Y": 1.80,
        },
        "odds_source": "Oddschecker/BBC (Aug 1 2026)",
        "kickoff": "13:00 UTC", "venue": "Toolpoint Areena",
        "notes": "Lahti moderate home fav; MD18."
    },
    {
        "home": "Gnistan", "away": "KuPS", "league": "Veikkausliiga",
        "home_att": 1.20, "home_def": 1.50, "away_att": 1.60, "away_def": 1.10,
        "home_advantage": 0.25, "odds": {
            "1": 3.20, "X": 3.68, "2": 2.08,
            "O25": 1.85, "BTTS_Y": 1.70,
        },
        "odds_source": "Oddschecker/BBC (Aug 1 2026)",
        "kickoff": "14:00 UTC", "venue": "Mustapekka Areena",
        "notes": "KuPS slight away fav; competitive match."
    },
    # ── Czech Liga ──
    {
        "home": "Liberec", "away": "Teplice", "league": "Czech Liga",
        "home_att": 1.55, "home_def": 1.25, "away_att": 1.10, "away_def": 1.55,
        "home_advantage": 0.30, "odds": {
            "1": 1.68, "X": 3.75, "2": 4.75,
            "O25": 1.70, "BTTS_Y": 1.75,
        },
        "odds_source": "Oddslot/Oddsportal (Aug 1 2026)",
        "kickoff": "10:00 UTC", "venue": "Stadion u Nisy, Liberec",
        "notes": "Liberec fav home; Round 2."
    },
    {
        "home": "Ostrava", "away": "Slavia Prague", "league": "Czech Liga",
        "home_att": 1.15, "home_def": 1.45, "away_att": 1.90, "away_def": 0.90,
        "home_advantage": 0.30, "odds": {
            "1": 5.00, "X": 4.00, "2": 1.65,
            "O25": 1.65, "BTTS_Y": 1.80,
        },
        "odds_source": "Oddsportal (Aug 1 2026)",
        "kickoff": "10:00 UTC", "venue": "Mestsky Stadion, Ostrava",
        "notes": "Slavia Prague heavy away fav; Round 2."
    },
    {
        "home": "Slovacko", "away": "Artis Brno", "league": "Czech Liga",
        "home_att": 1.70, "home_def": 1.15, "away_att": 0.90, "away_def": 1.70,
        "home_advantage": 0.30, "odds": {
            "1": 1.58, "X": 4.00, "2": 5.50,
            "O25": 1.65, "BTTS_Y": 1.88,
        },
        "odds_source": "Soccervital/Sportus (Aug 1 2026)",
        "kickoff": "10:00 UTC", "venue": "Mestsky Stadion, Uherske Hradiste",
        "notes": "Slovacko heavy home fav vs promoted Artis Brno."
    },
    {
        "home": "Plzen", "away": "Brno", "league": "Czech Liga",
        "home_att": 1.90, "home_def": 0.95, "away_att": 0.95, "away_def": 1.65,
        "home_advantage": 0.30, "odds": {
            "1": 1.52, "X": 4.50, "2": 6.50,
            "O25": 1.60, "BTTS_Y": 1.90,
        },
        "odds_source": "Oddsportal (Aug 1 2026)",
        "kickoff": "13:00 UTC", "venue": "Doosan Arena, Plzen",
        "notes": "Plzen heavy home fav; quality gap large."
    },
    # ── Iceland Urvalsdeild ──
    {
        "home": "IBV", "away": "Fram", "league": "Iceland Urvalsdeild",
        "home_att": 1.30, "home_def": 1.55, "away_att": 1.65, "away_def": 1.30,
        "home_advantage": 0.25, "odds": {
            "1": 2.80, "X": 3.20, "2": 1.80,
            "O25": 1.72, "BTTS_Y": 1.60,
        },
        "odds_source": "Oddschecker (Aug 1 2026)",
        "kickoff": "14:00 UTC", "venue": "Hasteinsvollur, Vestmannaeyjar",
        "notes": "Fram away fav; Icelandic league high-scoring environment."
    },
    # ── Austria Bundesliga ──
    {
        "home": "WSG Tirol", "away": "Sturm Graz", "league": "Austria Bundesliga",
        "home_att": 1.15, "home_def": 1.55, "away_att": 1.75, "away_def": 1.10,
        "home_advantage": 0.30, "odds": {
            "1": 3.70, "X": 3.88, "2": 1.93,
            "O25": 1.80, "BTTS_Y": 1.72,
        },
        "odds_source": "TheFishy/Sportsgambler (Aug 1 2026)",
        "kickoff": "14:00 UTC", "venue": "Tivoli Stadion, Innsbruck",
        "notes": "Sturm Graz away fav; MD1 season opener."
    },
    {
        "home": "Red Bull Salzburg", "away": "Hartberg", "league": "Austria Bundesliga",
        "home_att": 2.20, "home_def": 0.70, "away_att": 0.85, "away_def": 1.65,
        "home_advantage": 0.35, "odds": {
            "1": 1.29, "X": 5.91, "2": 9.51,
            "O25": 1.42, "BTTS_Y": 2.05,
        },
        "odds_source": "TheFishy/Sportsgambler (Aug 1 2026)",
        "kickoff": "16:30 UTC", "venue": "Red Bull Arena, Salzburg",
        "notes": "Salzburg heavy home fav; already has Draw pick in tracker from Jul 31 preview."
    },
    # ── Croatia HNL ──
    {
        "home": "NK Istra 1961", "away": "NK Lokomotiva Zagreb", "league": "Croatia HNL",
        "home_att": 1.25, "home_def": 1.35, "away_att": 1.30, "away_def": 1.30,
        "home_advantage": 0.30, "odds": {
            "1": 2.20, "X": 3.35, "2": 3.15,
            "O25": 1.95, "BTTS_Y": 1.78,
        },
        "odds_source": "SportyTrader/Oddspedia (Aug 1 2026)",
        "kickoff": "17:00 UTC", "venue": "Stadion Aldo Drosina, Pula",
        "notes": "Balanced matchup; HNL season opener."
    },
    # ── Switzerland Super League ──
    {
        "home": "FC Basel", "away": "Lausanne", "league": "Swiss Super League",
        "home_att": 1.65, "home_def": 1.20, "away_att": 1.30, "away_def": 1.40,
        "home_advantage": 0.30, "odds": {
            "1": 1.94, "X": 3.85, "2": 3.50,
            "O25": 1.68, "BTTS_Y": 1.62,
        },
        "odds_source": "Sportsgambler/Oddslot/SportyTrader (Aug 1 2026)",
        "kickoff": "16:00 UTC", "venue": "St. Jakob-Park, Basel",
        "notes": "Basel home fav; early season fixture."
    },
    {
        "home": "Thun", "away": "Young Boys", "league": "Swiss Super League",
        "home_att": 1.10, "home_def": 1.50, "away_att": 1.80, "away_def": 1.05,
        "home_advantage": 0.25, "odds": {
            "1": 4.20, "X": 3.70, "2": 1.75,
            "O25": 1.65, "BTTS_Y": 1.68,
        },
        "odds_source": "Mightytips/Tipsterarea (Aug 1 2026)",
        "kickoff": "18:30 UTC", "venue": "Stockhorn Arena, Thun",
        "notes": "Young Boys away fav; already has Draw pick in tracker from Jul 31 preview."
    },
    # ── Scotland Premiership ──
    {
        "home": "Falkirk", "away": "St Mirren", "league": "Scottish Premiership",
        "home_att": 1.25, "home_def": 1.35, "away_att": 1.20, "away_def": 1.30,
        "home_advantage": 0.30, "odds": {
            "1": 2.09, "X": 3.66, "2": 3.73,
            "O25": 1.85, "BTTS_Y": 1.75,
        },
        "odds_source": "Oddsportal/ESPN (Aug 1 2026)",
        "kickoff": "14:00 UTC", "venue": "Falkirk Stadium",
        "notes": "Opening day; Falkirk promoted, competitive opener."
    },
    {
        "home": "Aberdeen", "away": "Hearts", "league": "Scottish Premiership",
        "home_att": 1.30, "home_def": 1.25, "away_att": 1.45, "away_def": 1.15,
        "home_advantage": 0.30, "odds": {
            "1": 3.25, "X": 3.64, "2": 2.31,
            "O25": 1.80, "BTTS_Y": 1.68,
        },
        "odds_source": "Oddsportal/ESPN (Aug 1 2026)",
        "kickoff": "16:30 UTC", "venue": "Pittodrie Stadium, Aberdeen",
        "notes": "Opening day; Hearts slight fav."
    },
    # ── Russia Premier League ──
    {
        "home": "Akron", "away": "Rubin Kazan", "league": "Russia Premier League",
        "home_att": 1.15, "home_def": 1.40, "away_att": 1.40, "away_def": 1.20,
        "home_advantage": 0.25, "odds": {
            "1": 2.95, "X": 3.30, "2": 2.50,
            "O25": 2.00, "BTTS_Y": 1.85,
        },
        "odds_source": "Wincomparator (Aug 1 2026)",
        "kickoff": "10:00 UTC", "venue": "Samara Arena, Samara",
        "notes": "Rubin slight fav; Round 2."
    },
    {
        "home": "CSKA Moscow", "away": "Krylya Sovetov", "league": "Russia Premier League",
        "home_att": 1.85, "home_def": 0.95, "away_att": 1.10, "away_def": 1.45,
        "home_advantage": 0.30, "odds": {
            "1": 1.54, "X": 4.35, "2": 5.80,
            "O25": 1.72, "BTTS_Y": 1.90,
        },
        "odds_source": "Oddslot/SportyTrader (Aug 1 2026)",
        "kickoff": "12:15 UTC", "venue": "VEB Arena, Moscow",
        "notes": "CSKA heavy home fav; Round 2."
    },
    {
        "home": "Dynamo Makhachkala", "away": "Lokomotiv Moscow", "league": "Russia Premier League",
        "home_att": 1.10, "home_def": 1.35, "away_att": 1.45, "away_def": 1.20,
        "home_advantage": 0.25, "odds": {
            "1": 3.50, "X": 3.45, "2": 2.15,
            "O25": 2.00, "BTTS_Y": 1.80,
        },
        "odds_source": "Wincomparator (Aug 1 2026)",
        "kickoff": "14:30 UTC", "venue": "Anzhi Arena, Kaspiysk",
        "notes": "Loko slight away fav; tight match expected."
    },
    {
        "home": "Baltika", "away": "Dynamo Moscow", "league": "Russia Premier League",
        "home_att": 1.15, "home_def": 1.35, "away_att": 1.50, "away_def": 1.20,
        "home_advantage": 0.25, "odds": {
            "1": 2.95, "X": 3.25, "2": 2.55,
            "O25": 1.95, "BTTS_Y": 1.78,
        },
        "odds_source": "Wincomparator (Aug 1 2026)",
        "kickoff": "16:45 UTC", "venue": "Rostec Arena, Kaliningrad",
        "notes": "Dynamo Moscow slight fav; competitive."
    },
]


def get_model_prob(out, market_key):
    return {
        "O25": out.prob_over_2_5,
        "BTTS_Y": out.prob_btts,
        "1": out.prob_home,
        "X": out.prob_draw,
        "2": out.prob_away,
    }.get(market_key, 0)


# Tiered staking: edge-based unit allocation
def stake_from_edge(edge_pct: float) -> float:
    if edge_pct > 10:
        return 0.75
    if edge_pct > 7:
        return 0.50
    if edge_pct >= 5:
        return 0.30
    return 0.0


def conf_from_edge(edge_pct: float) -> str:
    if edge_pct > 10:
        return "High"
    if edge_pct > 7:
        return "Medium"
    return "Low"


def main():
    all_model_results = []
    all_picks = []
    all_new_picks = []

    for fx in FIXTURES:
        league = fx["league"]
        league_avg = LEAGUE_AVGS.get(league, 2.60)

        inp = MatchInput(
            home=fx["home"],
            away=fx["away"],
            league=league,
            home_att=fx["home_att"],
            home_def=fx["home_def"],
            away_att=fx["away_att"],
            away_def=fx["away_def"],
            league_avg_gpg=league_avg,
            home_advantage=fx.get("home_advantage", 0.30),
            first_leg_score=fx.get("first_leg_score"),
            is_second_leg=fx.get("is_second_leg", False),
            defense_adj=fx.get("defense_adj", 0.0),
        )
        out = run_model(inp)
        odds = fx["odds"]

        print(f"\n{fx['home']} vs {fx['away']} ({league})")
        print(f"  xG: H={out.home_expected} A={out.away_expected} T={out.total_expected}")
        print(
            f"  1X2: {out.prob_home:.1%}/{out.prob_draw:.1%}/{out.prob_away:.1%} "
            f"| O2.5: {out.prob_over_2_5:.1%} | BTTS: {out.prob_btts:.1%}"
        )
        print(
            f"  Odds: 1={odds.get('1')} X={odds.get('X')} 2={odds.get('2')} "
            f"O25={odds.get('O25')} BTTS_Y={odds.get('BTTS_Y')}"
        )

        match_picks = []
        for mkt_key, mkt_name, odds_key in MARKETS:
            if odds_key not in odds:
                continue
            true_prob = get_model_prob(out, mkt_key)
            odd = odds[odds_key]
            val = calculate_value(true_prob, odd)
            edge_pct = val["edge"] * 100

            # Prefer O2.5 and BTTS; 1X2 only with exceptional edge (>8%)
            if mkt_key in ("1", "X", "2") and edge_pct < 8.0:
                continue
            if edge_pct < 5.0:
                continue

            stake = stake_from_edge(edge_pct)
            conf = conf_from_edge(edge_pct)
            selection = "Yes" if mkt_key in ("O25", "BTTS_Y") else mkt_name

            pick = {
                "match": f"{fx['home']} vs {fx['away']}",
                "home": fx["home"],
                "away": fx["away"],
                "league": league,
                "market": mkt_name,
                "selection": selection,
                "odds": odd,
                "model_prob": true_prob,
                "true_implied": val["implied"],
                "edge_pct": edge_pct,
                "ev": val["ev"],
                "stake": stake,
                "game_state": out.game_state_label,
                "confidence": conf,
                "expected_goals": f"H={out.home_expected} A={out.away_expected} T={out.total_expected}",
                "home_xg": out.home_expected,
                "away_xg": out.away_expected,
                "total_xg": out.total_expected,
                "predicted_score": out.predicted_score,
                "prob_home": out.prob_home,
                "prob_draw": out.prob_draw,
                "prob_away": out.prob_away,
                "prob_o25": out.prob_over_2_5,
                "prob_btts": out.prob_btts,
                "odds_source": fx["odds_source"],
                "kickoff": fx["kickoff"],
                "venue": fx["venue"],
                "notes": fx["notes"],
                "model_conf": out.confidence,
            }
            match_picks.append(pick)

        all_model_results.append({"fx": fx, "out": out, "odds": odds})
        all_picks.extend(match_picks)

    all_picks.sort(key=lambda p: p["edge_pct"], reverse=True)

    # Exclude picks for matches already in tracker (Salzburg Draw, Thun Draw)
    EXISTING_TRACKER = {
        ("Red Bull Salzburg", "Hartberg", "Draw"),
        ("Thun", "Young Boys", "Draw"),
    }
    for p in all_picks:
        key = (p["home"], p["away"], p["selection"])
        if key not in EXISTING_TRACKER:
            all_new_picks.append(p)

    print(f"\n{'='*60}")
    print(f"TOTAL VALUE PICKS: {len(all_picks)} (New: {len(all_new_picks)}, Already tracked: {len(all_picks) - len(all_new_picks)})")
    print(f"{'='*60}")
    for i, p in enumerate(all_picks, 1):
        tag = " [NEW]" if p in all_new_picks else " [TRACKED]"
        print(f"\n--- Pick #{i}{tag} ---")
        print(f"  {p['league']}: {p['match']}")
        print(f"  {p['market']} @ {p['odds']}")
        print(
            f"  Model: {p['model_prob']:.1%} | Implied: {p['true_implied']:.1%} "
            f"| Edge: {p['edge_pct']:.1f}%"
        )
        print(f"  EV: {p['ev']:+.3f} | Stake: ${p['stake']:.2f} | Conf: {p['confidence']}")

    # CSV lines for new picks only
    if all_new_picks:
        print("\n\n--- CSV TRACKER LINES (NEW PICKS) ---")
        for p in all_new_picks:
            print(
                f"{DATE},{p['league']},{p['home']},{p['away']},{p['market']},{p['selection']},"
                f"{p['odds']},SportyBet,{p['model_prob']:.4f},{p['true_implied']:.4f},"
                f"{p['edge_pct']/100:.4f},{p['ev']:.4f},{p['stake']:.2f},{BANKROLL:.2f},open,"
            )

    # Identify leagues with/without fixtures
    all_15 = [
        "Champions League Qualifiers", "Europa League Qualifiers",
        "Conference League Qualifiers", "Czech Liga", "Denmark Superliga",
        "Finland Veikkausliiga", "Iceland Urvalsdeild", "Norway Eliteserien",
        "Russia Premier League", "Serbia Super Liga", "Sweden Allsvenskan",
        "Switzerland Super League", "Austria Bundesliga", "Croatia HNL",
        "Scottish Premiership",
    ]
    leagues_with = sorted(set(f["league"] for f in FIXTURES))
    leagues_without = sorted(set(all_15) - set(leagues_with))

    output = {
        "date": DATE,
        "leagues_analyzed": all_15,
        "leagues_with_fixtures": leagues_with,
        "leagues_with_no_fixtures": leagues_without,
        "total_fixtures": len(FIXTURES),
        "picks_found": len(all_picks),
        "picks_new": len(all_new_picks),
        "picks": all_picks,
        "model_results": [
            {
                "home": r["fx"]["home"],
                "away": r["fx"]["away"],
                "league": r["fx"]["league"],
                "home_expected": r["out"].home_expected,
                "away_expected": r["out"].away_expected,
                "total_expected": r["out"].total_expected,
                "prob_home": r["out"].prob_home,
                "prob_draw": r["out"].prob_draw,
                "prob_away": r["out"].prob_away,
                "prob_over_2_5": r["out"].prob_over_2_5,
                "prob_btts": r["out"].prob_btts,
                "predicted_score": r["out"].predicted_score,
                "confidence": r["out"].confidence,
                "game_state": r["out"].game_state_label,
                "odds": r["odds"],
                "odds_source": r["fx"]["odds_source"],
                "notes": r["fx"]["notes"],
                "kickoff": r["fx"]["kickoff"],
                "venue": r["fx"]["venue"],
            }
            for r in all_model_results
        ],
    }

    out_path = os.path.join(os.path.dirname(__file__), f"output_{DATE.replace('-', '_')}.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nWrote {out_path}")
    print(json.dumps({"picks_found": len(all_picks), "picks_new": len(all_new_picks), "fixtures": len(FIXTURES)}, indent=2))
    return output


if __name__ == "__main__":
    main()
