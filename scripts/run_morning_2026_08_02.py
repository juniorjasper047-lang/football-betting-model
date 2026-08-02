#!/usr/bin/env python3
"""Morning pick generation for 2026-08-02 (Sunday).

Confirmed fixtures across 15 tracked leagues. Sunday Aug 2 features domestic league
matches from Eliteserien, Allsvenskan, Danish Superliga, Scottish Premiership,
Swiss Super League, Austria Bundesliga, Czech Liga, Russia Premier League, Croatia HNL.

No UEFA qualifier fixtures (Q3 starts Aug 4-6). No Serbia Super Liga, Iceland, or
Veikkausliiga fixtures found on this date.

Sources: SportsMole previews, fixture pages, and data analysis pages (Aug 1-2 2026).
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import MatchInput, run_model
from value import calculate_value

BANKROLL = 100.0
DATE = "2026-08-02"

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
    # ── Norway Eliteserien ──
    {
        "home": "Brann", "away": "Rosenborg", "league": "Eliteserien",
        "home_att": 1.55, "home_def": 1.35, "away_att": 1.45, "away_def": 1.10,
        "home_advantage": 0.30, "odds": {
            "1": 2.45, "X": 3.65, "2": 2.70,
            "O25": 1.72, "BTTS_Y": 1.62,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "16:15 UTC", "venue": "Brann Stadion, Bergen",
        "notes": "Rosenborg unbeaten in 3 league games under Alexandersson (3W). Brann have not kept a clean sheet in 13 matches. H2H: Brann W2 D1 L2 last 5. SportsMole model: Brann 56% win, O2.5 63.3%, BTTS 60.9%."
    },
    {
        "home": "Molde", "away": "Sarpsborg", "league": "Eliteserien",
        "home_att": 1.60, "home_def": 1.20, "away_att": 1.10, "away_def": 1.25,
        "home_advantage": 0.30, "odds": {
            "1": 2.00, "X": 3.70, "2": 3.50,
            "O25": 1.67, "BTTS_Y": 1.55,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "14:00 UTC", "venue": "Aker Stadion, Molde",
        "notes": "Molde won 4-2 last time out vs KFUM. Sarpsborg unbeaten in 5 league games (3W 2D), 3 clean sheets. Sarpsborg won last 3 H2H. SportsMole model: Molde 52.1%, O2.5 67.7%, BTTS 66.2%."
    },
    {
        "home": "Aalesund", "away": "Tromso", "league": "Eliteserien",
        "home_att": 1.20, "home_def": 1.55, "away_att": 1.70, "away_def": 1.15,
        "home_advantage": 0.30, "odds": {
            "1": 3.80, "X": 3.50, "2": 1.95,
            "O25": 1.75, "BTTS_Y": 1.65,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "14:00 UTC", "venue": "Color Line Stadion, Aalesund",
        "notes": "Aalesund winless in 5 (D4 L1). Tromso 3rd place, 4 pts off top. Tromso coming off EL elimination midweek tired legs. SportsMole tip: 2-2 draw."
    },
    {
        "home": "KFUM Oslo", "away": "Kristiansund", "league": "Eliteserien",
        "home_att": 1.25, "home_def": 1.50, "away_att": 0.85, "away_def": 1.60,
        "home_advantage": 0.30, "odds": {
            "1": 2.20, "X": 3.45, "2": 3.20,
            "O25": 1.85, "BTTS_Y": 1.70,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "14:00 UTC", "venue": "KFUM Arena, Oslo",
        "notes": "Relegation 6-pointer. Both on 12 pts. KFUM lost 3 straight but vs top-5 sides. Kristiansund winless in 5 (D1 L4), worst attack in league (12 goals). SportsMole tip: 2-1 KFUM."
    },
    # ── Denmark Superliga ──
    {
        "home": "Midtjylland", "away": "Horsens", "league": "Denmark Superliga",
        "home_att": 1.80, "home_def": 1.05, "away_att": 1.10, "away_def": 1.40,
        "home_advantage": 0.30, "odds": {
            "1": 1.40, "X": 4.80, "2": 6.50,
            "O25": 1.55, "BTTS_Y": 1.85,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "12:00 UTC", "venue": "MCH Arena, Herning",
        "notes": "Midtjylland W 3-2 at Sonderjyske MD1. Horsens promoted, D 1-1 vs Nordsjaelland MD1. FCM unbeaten in last 6 H2H (W4 D2). SportsMole tip: 3-1 Midtjylland."
    },
    {
        "home": "Brondby", "away": "Viborg", "league": "Denmark Superliga",
        "home_att": 1.55, "home_def": 1.15, "away_att": 1.40, "away_def": 1.25,
        "home_advantage": 0.30, "odds": {
            "1": 2.15, "X": 3.50, "2": 3.20,
            "O25": 1.80, "BTTS_Y": 1.70,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "12:00 UTC", "venue": "Brondby Stadium, Copenhagen",
        "notes": "Brondby D 1-1 at AGF MD1 (conceded late pen). Viborg W 1-0 vs Odense MD1. Viborg won 3 of last 5 H2H. SportsMole tip: 1-2 Viborg."
    },
    # ── Sweden Allsvenskan ──
    {
        "home": "Brommapojkarna", "away": "Malmo", "league": "Allsvenskan",
        "home_att": 1.20, "home_def": 1.45, "away_att": 1.65, "away_def": 1.10,
        "home_advantage": 0.25, "odds": {
            "1": 4.50, "X": 3.80, "2": 1.72,
            "O25": 1.75, "BTTS_Y": 1.70,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "12:00 UTC", "venue": "Grimsta IP, Stockholm",
        "notes": "BP winless in 5 (D3 L2), no clean sheets this season bar 1. Malmo 8th, 2 without a win. BP missing Hansen (4G 5A suspended). Malmo unbeaten in 9 visits (W6 D3). SportsMole tip: 1-2 Malmo."
    },
    {
        "home": "AIK", "away": "Orgryte", "league": "Allsvenskan",
        "home_att": 1.55, "home_def": 1.20, "away_att": 1.05, "away_def": 1.55,
        "home_advantage": 0.30, "odds": {
            "1": 1.62, "X": 4.00, "2": 5.00,
            "O25": 1.70, "BTTS_Y": 1.85,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "12:00 UTC", "venue": "Friends Arena, Stockholm",
        "notes": "AIK home fav. Orgryte promoted side struggling. MD15."
    },
    {
        "home": "Goteborg", "away": "Degerfors", "league": "Allsvenskan",
        "home_att": 1.45, "home_def": 1.25, "away_att": 1.15, "away_def": 1.45,
        "home_advantage": 0.30, "odds": {
            "1": 1.85, "X": 3.65, "2": 3.90,
            "O25": 1.88, "BTTS_Y": 1.75,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "14:30 UTC", "venue": "Gamla Ullevi, Gothenburg",
        "notes": "Goteborg home slight fav vs mid-table Degerfors. MD15."
    },
    # ── Scottish Premiership ──
    {
        "home": "St Johnstone", "away": "Kilmarnock", "league": "Scottish Premiership",
        "home_att": 1.15, "home_def": 1.25, "away_att": 1.05, "away_def": 1.00,
        "home_advantage": 0.30, "odds": {
            "1": 3.00, "X": 3.30, "2": 2.35,
            "O25": 1.95, "BTTS_Y": 1.80,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "13:00 UTC", "venue": "McDiarmid Park, Perth",
        "notes": "St Johnstone promoted as Championship winners. Kilmarnock finished 10th last season. Killie unbeaten in 10 competitive games (90 mins), 4 clean sheets in League Cup. SportsMole tip: 0-1 Killie."
    },
    {
        "home": "Hibernian", "away": "Motherwell", "league": "Scottish Premiership",
        "home_att": 1.50, "home_def": 1.25, "away_att": 1.55, "away_def": 1.15,
        "home_advantage": 0.30, "odds": {
            "1": 2.55, "X": 3.50, "2": 2.65,
            "O25": 1.78, "BTTS_Y": 1.60,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "15:30 UTC", "venue": "Easter Road, Edinburgh",
        "notes": "Hibs 5th last season, Motherwell 4th. Both coming off Conf Lge Q2 wins. Motherwell won 2 drew 2 of last 4 H2H. SportsMole tip: 2-2 draw."
    },
    # ── Switzerland Super League ──
    {
        "home": "FC Zurich", "away": "Servette", "league": "Swiss Super League",
        "home_att": 1.35, "home_def": 1.35, "away_att": 1.40, "away_def": 1.30,
        "home_advantage": 0.25, "odds": {
            "1": 2.45, "X": 3.40, "2": 2.80,
            "O25": 1.85, "BTTS_Y": 1.65,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "12:00 UTC", "venue": "Letzigrund, Zurich",
        "notes": "Early season fixture. Zurich slightly favored at home."
    },
    {
        "home": "Sion", "away": "St Gallen", "league": "Swiss Super League",
        "home_att": 1.20, "home_def": 1.45, "away_att": 1.35, "away_def": 1.35,
        "home_advantage": 0.25, "odds": {
            "1": 2.80, "X": 3.40, "2": 2.45,
            "O25": 1.82, "BTTS_Y": 1.70,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "14:30 UTC", "venue": "Stade de Tourbillon, Sion",
        "notes": "Early season Swiss Super League fixture."
    },
    {
        "home": "Lugano", "away": "Winterthur", "league": "Swiss Super League",
        "home_att": 1.55, "home_def": 1.20, "away_att": 1.15, "away_def": 1.50,
        "home_advantage": 0.25, "odds": {
            "1": 1.72, "X": 3.80, "2": 4.50,
            "O25": 1.78, "BTTS_Y": 1.80,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "14:30 UTC", "venue": "Stadio Cornaredo, Lugano",
        "notes": "Lugano home fav vs Winterthur."
    },
    # ── Austria Bundesliga ──
    {
        "home": "Austria Vienna", "away": "LASK", "league": "Austria Bundesliga",
        "home_att": 1.50, "home_def": 1.20, "away_att": 1.35, "away_def": 1.25,
        "home_advantage": 0.30, "odds": {
            "1": 2.15, "X": 3.45, "2": 3.20,
            "O25": 1.72, "BTTS_Y": 1.62,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "14:00 UTC", "venue": "Generali Arena, Vienna",
        "notes": "MD1 Austria Bundesliga fixture."
    },
    {
        "home": "Rapid Vienna", "away": "Wolfsberger AC", "league": "Austria Bundesliga",
        "home_att": 1.65, "home_def": 1.10, "away_att": 1.20, "away_def": 1.40,
        "home_advantage": 0.30, "odds": {
            "1": 1.55, "X": 4.20, "2": 5.50,
            "O25": 1.65, "BTTS_Y": 1.75,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "14:00 UTC", "venue": "Allianz Stadion, Vienna",
        "notes": "Rapid heavy home fav in MD1."
    },
    {
        "home": "SCR Altach", "away": "Austria Klagenfurt", "league": "Austria Bundesliga",
        "home_att": 1.15, "home_def": 1.50, "away_att": 1.20, "away_def": 1.40,
        "home_advantage": 0.30, "odds": {
            "1": 2.50, "X": 3.30, "2": 2.75,
            "O25": 1.90, "BTTS_Y": 1.72,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "16:00 UTC", "venue": "Cashpoint Arena, Altach",
        "notes": "MD1 Austria Bundesliga, competitive lower-half matchup."
    },
    # ── Czech Liga ──
    {
        "home": "Sigma Olomouc", "away": "Pardubice", "league": "Czech Liga",
        "home_att": 1.40, "home_def": 1.20, "away_att": 1.10, "away_def": 1.45,
        "home_advantage": 0.30, "odds": {
            "1": 1.75, "X": 3.65, "2": 4.50,
            "O25": 1.78, "BTTS_Y": 1.82,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "12:00 UTC", "venue": "Andruv Stadion, Olomouc",
        "notes": "Olomouc home fav in Round 2 of Czech Liga."
    },
    {
        "home": "Mlada Boleslav", "away": "Bohemians 1905", "league": "Czech Liga",
        "home_att": 1.35, "home_def": 1.30, "away_att": 1.15, "away_def": 1.35,
        "home_advantage": 0.30, "odds": {
            "1": 2.35, "X": 3.30, "2": 3.00,
            "O25": 1.90, "BTTS_Y": 1.75,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "14:30 UTC", "venue": "Lokotrans Arena, Mlada Boleslav",
        "notes": "Czech Liga Round 2."
    },
    {
        "home": "Jablonec", "away": "Hradec Kralove", "league": "Czech Liga",
        "home_att": 1.45, "home_def": 1.15, "away_att": 1.25, "away_def": 1.35,
        "home_advantage": 0.30, "odds": {
            "1": 2.05, "X": 3.40, "2": 3.45,
            "O25": 1.82, "BTTS_Y": 1.72,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "17:00 UTC", "venue": "Stadion Strelnice, Jablonec",
        "notes": "Czech Liga Round 2. Hradec just played EL Q2."
    },
    # ── Russia Premier League ──
    {
        "home": "FC Rostov", "away": "Fakel", "league": "Russia Premier League",
        "home_att": 1.40, "home_def": 1.25, "away_att": 1.00, "away_def": 1.45,
        "home_advantage": 0.25, "odds": {
            "1": 1.78, "X": 3.60, "2": 4.60,
            "O25": 1.88, "BTTS_Y": 1.85,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "11:00 UTC", "venue": "Rostov Arena, Rostov-on-Don",
        "notes": "Rostov home fav Round 2."
    },
    {
        "home": "Zenit", "away": "Nizhny Novgorod", "league": "Russia Premier League",
        "home_att": 2.20, "home_def": 0.70, "away_att": 0.95, "away_def": 1.55,
        "home_advantage": 0.35, "odds": {
            "1": 1.25, "X": 5.80, "2": 11.00,
            "O25": 1.52, "BTTS_Y": 2.15,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "13:15 UTC", "venue": "Gazprom Arena, St. Petersburg",
        "notes": "Zenit heavy home fav. Defending champions."
    },
    {
        "home": "Krasnodar", "away": "Akhmat Grozny", "league": "Russia Premier League",
        "home_att": 1.65, "home_def": 1.05, "away_att": 1.10, "away_def": 1.35,
        "home_advantage": 0.30, "odds": {
            "1": 1.55, "X": 4.10, "2": 5.60,
            "O25": 1.70, "BTTS_Y": 1.82,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "15:30 UTC", "venue": "Krasnodar Stadium, Krasnodar",
        "notes": "Krasnodar home fav Round 2."
    },
    # ── Croatia HNL ──
    {
        "home": "Rijeka", "away": "Slaven Belupo", "league": "Croatia HNL",
        "home_att": 1.70, "home_def": 0.95, "away_att": 1.05, "away_def": 1.45,
        "home_advantage": 0.30, "odds": {
            "1": 1.45, "X": 4.30, "2": 6.80,
            "O25": 1.62, "BTTS_Y": 1.85,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "15:30 UTC", "venue": "Stadion Rujevica, Rijeka",
        "notes": "Rijeka heavy home fav; early season HNL."
    },
    {
        "home": "Dinamo Zagreb", "away": "Osijek", "league": "Croatia HNL",
        "home_att": 2.00, "home_def": 0.85, "away_att": 1.25, "away_def": 1.20,
        "home_advantage": 0.30, "odds": {
            "1": 1.38, "X": 4.60, "2": 7.50,
            "O25": 1.58, "BTTS_Y": 1.90,
        },
        "odds_source": "SportsMole model / market consensus (Aug 2 2026)",
        "kickoff": "18:00 UTC", "venue": "Maksimir, Zagreb",
        "notes": "Dinamo Zagreb heavy home fav. Osijek competitive but away form weak."
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

    print(f"\n{'='*60}")
    print(f"TOTAL VALUE PICKS: {len(all_picks)}")
    print(f"{'='*60}")
    for i, p in enumerate(all_picks, 1):
        print(f"\n--- Pick #{i} ---")
        print(f"  {p['league']}: {p['match']}")
        print(f"  {p['market']} @ {p['odds']}")
        print(
            f"  Model: {p['model_prob']:.1%} | Implied: {p['true_implied']:.1%} "
            f"| Edge: {p['edge_pct']:.1f}%"
        )
        print(f"  EV: {p['ev']:+.3f} | Stake: ${p['stake']:.2f} | Conf: {p['confidence']}")

    # CSV lines for new picks
    if all_picks:
        print("\n\n--- CSV TRACKER LINES ---")
        for p in all_picks:
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
    print(json.dumps({"picks_found": len(all_picks), "fixtures": len(FIXTURES)}, indent=2))
    return output


if __name__ == "__main__":
    main()
