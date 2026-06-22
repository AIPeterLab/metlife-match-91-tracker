from __future__ import annotations

import argparse
import json
import math
import random
import re
import urllib.parse
import urllib.request
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
DOCS_DIR = ROOT / "docs"

PRIORITY_GROUPS = ["C", "E", "F", "I"]
OWNER_TEAMS = {
    "Brazil",
    "Germany",
    "Japan",
    "Netherlands",
    "Senegal",
    "Norway",
    "France",
    "Ivory Coast",
    "Ecuador",
    "Morocco",
}

GROUPS = {
    "A": ["Mexico", "South Africa", "South Korea", "Czechia"],
    "B": ["Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["United States", "Paraguay", "Australia", "Turkey"],
    "E": ["Germany", "Curacao", "Ivory Coast", "Ecuador"],
    "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Iraq", "Norway"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
    "L": ["England", "Croatia", "Ghana", "Panama"],
}

FIFA_MATCH_API = (
    "https://api.fifa.com/api/v3/calendar/matches?"
    + urllib.parse.urlencode(
        {
            "language": "en",
            "count": "500",
            "idCompetition": "17",
            "idSeason": "285023",
        }
    )
)

FIFA_RANKS = {
    "Spain": 1,
    "Argentina": 2,
    "France": 3,
    "England": 4,
    "Brazil": 6,
    "Portugal": 6,
    "Morocco": 7,
    "Netherlands": 8,
    "Germany": 10,
    "Croatia": 10,
    "Colombia": 13,
    "United States": 14,
    "Senegal": 15,
    "Uruguay": 16,
    "Switzerland": 17,
    "Japan": 18,
    "South Korea": 22,
    "Ecuador": 23,
    "Australia": 26,
    "Mexico": 27,
    "Panama": 30,
    "Norway": 31,
    "Ivory Coast": 33,
    "Algeria": 35,
    "Sweden": 38,
    "Paraguay": 39,
    "Scotland": 42,
    "Czechia": 44,
    "Tunisia": 45,
    "Uzbekistan": 50,
    "Qatar": 51,
    "DR Congo": 56,
    "Iraq": 57,
    "Saudi Arabia": 60,
    "South Africa": 61,
    "Jordan": 66,
    "Cape Verde": 68,
    "Bosnia and Herzegovina": 71,
    "Ghana": 72,
    "Curacao": 82,
    "Haiti": 83,
    "New Zealand": 86,
    "Egypt": 30,
    "Belgium": 11,
    "Iran": 20,
    "Canada": 27,
    "Turkey": 25,
    "Austria": 24,
}

SEED_RESULTS = [
    ("2026-06-11", "A", "Mexico", "South Africa", 2, 0),
    ("2026-06-11", "A", "South Korea", "Czechia", 1, 0),
    ("2026-06-12", "B", "Canada", "Qatar", 6, 0),
    ("2026-06-13", "C", "Brazil", "Morocco", 1, 1),
    ("2026-06-13", "C", "Haiti", "Scotland", 0, 1),
    ("2026-06-14", "D", "United States", "Paraguay", 4, 1),
    ("2026-06-14", "E", "Germany", "Curacao", 7, 1),
    ("2026-06-14", "E", "Ivory Coast", "Ecuador", 1, 0),
    ("2026-06-14", "F", "Netherlands", "Japan", 2, 2),
    ("2026-06-14", "F", "Sweden", "Tunisia", 6, 1),
    ("2026-06-15", "G", "Belgium", "Iran", 0, 0),
    ("2026-06-15", "G", "Egypt", "New Zealand", 3, 1),
    ("2026-06-15", "H", "Spain", "Cape Verde", 0, 0),
    ("2026-06-15", "H", "Saudi Arabia", "Uruguay", 1, 1),
    ("2026-06-16", "I", "France", "Senegal", 3, 1),
    ("2026-06-16", "I", "Norway", "Iraq", 4, 1),
    ("2026-06-16", "J", "Argentina", "Algeria", 2, 0),
    ("2026-06-16", "J", "Austria", "Jordan", 1, 0),
    ("2026-06-17", "K", "Portugal", "DR Congo", 2, 0),
    ("2026-06-17", "K", "Colombia", "Uzbekistan", 1, 0),
    ("2026-06-17", "L", "England", "Croatia", 1, 1),
    ("2026-06-17", "L", "Ghana", "Panama", 1, 0),
    ("2026-06-18", "D", "United States", "Australia", 2, 1),
    ("2026-06-19", "C", "Scotland", "Morocco", 0, 1),
    ("2026-06-19", "C", "Brazil", "Haiti", 3, 0),
    ("2026-06-20", "E", "Germany", "Ivory Coast", 2, 1),
    ("2026-06-20", "E", "Ecuador", "Curacao", 0, 0),
    ("2026-06-20", "F", "Netherlands", "Sweden", 5, 1),
    ("2026-06-20", "F", "Tunisia", "Japan", 0, 4),
    ("2026-06-21", "H", "Spain", "Saudi Arabia", 4, 0),
    ("2026-06-21", "H", "Uruguay", "Cape Verde", 2, 2),
]

FIXTURE_DATES = {
    "A": ["2026-06-11", "2026-06-11", "2026-06-18", "2026-06-18", "2026-06-24", "2026-06-24"],
    "B": ["2026-06-12", "2026-06-12", "2026-06-18", "2026-06-18", "2026-06-24", "2026-06-24"],
    "C": ["2026-06-13", "2026-06-13", "2026-06-19", "2026-06-19", "2026-06-24", "2026-06-24"],
    "D": ["2026-06-12", "2026-06-12", "2026-06-19", "2026-06-19", "2026-06-25", "2026-06-25"],
    "E": ["2026-06-14", "2026-06-14", "2026-06-20", "2026-06-20", "2026-06-25", "2026-06-25"],
    "F": ["2026-06-14", "2026-06-14", "2026-06-20", "2026-06-20", "2026-06-25", "2026-06-25"],
    "G": ["2026-06-15", "2026-06-15", "2026-06-21", "2026-06-21", "2026-06-26", "2026-06-26"],
    "H": ["2026-06-15", "2026-06-15", "2026-06-21", "2026-06-21", "2026-06-26", "2026-06-26"],
    "I": ["2026-06-16", "2026-06-16", "2026-06-22", "2026-06-22", "2026-06-26", "2026-06-26"],
    "J": ["2026-06-16", "2026-06-16", "2026-06-22", "2026-06-22", "2026-06-27", "2026-06-27"],
    "K": ["2026-06-17", "2026-06-17", "2026-06-23", "2026-06-23", "2026-06-27", "2026-06-27"],
    "L": ["2026-06-17", "2026-06-17", "2026-06-23", "2026-06-23", "2026-06-27", "2026-06-27"],
}

PAIRINGS = [(0, 1), (2, 3), (0, 2), (3, 1), (3, 0), (1, 2)]


def norm_team(name: str) -> str:
    replacements = {
        "Curaçao": "Curacao",
        "Cote d'Ivoire": "Ivory Coast",
        "Côte d'Ivoire": "Ivory Coast",
        "Korea Republic": "South Korea",
        "USA": "United States",
        "United States of America": "United States",
        "Cabo Verde": "Cape Verde",
        "Congo DR": "DR Congo",
        "DR Congo": "DR Congo",
        "Türkiye": "Turkey",
        "IR Iran": "Iran",
    }
    cleaned = re.sub(r"\s+", " ", name.replace("(A)", "").replace("(E)", "")).strip()
    return replacements.get(cleaned, cleaned)


def localized(value) -> str:
    if isinstance(value, list):
        for item in value:
            if item.get("Locale") in {"en-GB", "en-US", "en"}:
                return item.get("Description", "")
        if value:
            return value[0].get("Description", "")
    if isinstance(value, dict):
        return value.get("Description", "")
    return str(value or "")


def fifa_team_name(team: dict) -> str:
    return norm_team(localized(team.get("TeamName")) or team.get("ShortClubName") or team.get("Abbreviation") or "")


def fetch_fifa_fixtures() -> tuple[list[dict], list[str]]:
    notes = []
    request = urllib.request.Request(
        FIFA_MATCH_API,
        headers={
            "User-Agent": "MetLifeMatch91Tracker/1.0 (+https://github.com/AIPeterLab/metlife-match-91-tracker)",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    fixtures = []
    for match in payload.get("Results", []):
        stage_name = localized(match.get("StageName"))
        group_name = localized(match.get("GroupName"))
        group_match = re.search(r"Group\s+([A-L])", group_name)
        if stage_name != "First Stage" or not group_match:
            continue
        home = fifa_team_name(match.get("Home") or {})
        away = fifa_team_name(match.get("Away") or {})
        if not home or not away:
            continue
        home_goals = match.get("HomeTeamScore")
        away_goals = match.get("AwayTeamScore")
        completed = home_goals is not None and away_goals is not None and int(match.get("ResultType") or 0) > 0
        fixtures.append(
            {
                "date": (match.get("LocalDate") or match.get("Date") or "")[:10],
                "group": group_match.group(1),
                "home": home,
                "away": away,
                "home_goals": int(home_goals) if completed else None,
                "away_goals": int(away_goals) if completed else None,
                "status": "completed" if completed else "scheduled",
                "source": FIFA_MATCH_API,
                "fifa_match_id": match.get("IdMatch"),
                "match_number": match.get("MatchNumber"),
            }
        )

    if len(fixtures) < 72:
        raise RuntimeError(f"FIFA API returned only {len(fixtures)} first-stage fixtures")
    notes.append(f"Loaded {len(fixtures)} first-stage fixtures directly from FIFA's public match API.")
    completed_count = sum(1 for match in fixtures if match["status"] == "completed")
    notes.append(f"FIFA match API has {completed_count} completed group-stage fixtures at generation time.")
    notes.append("Standings stats come from FIFA match records; tied-team ordering falls back to points, goal difference, goals for, and ranking because Team Conduct Score is not exposed in the match API.")
    return fixtures, notes


def seeded_fixtures() -> list[dict]:
    results_by_pair = {
        tuple(sorted((home, away))): (date, group, home, away, hg, ag)
        for date, group, home, away, hg, ag in SEED_RESULTS
    }
    fixtures = []
    for group, teams in GROUPS.items():
        for idx, (left, right) in enumerate(PAIRINGS):
            home, away = teams[left], teams[right]
            result = results_by_pair.get(tuple(sorted((home, away))))
            fixture = {"date": FIXTURE_DATES[group][idx], "group": group, "home": home, "away": away}
            if result:
                _, _, result_home, result_away, hg, ag = result
                if result_home == home:
                    fixture.update({"home_goals": hg, "away_goals": ag, "status": "completed"})
                else:
                    fixture.update({"home_goals": ag, "away_goals": hg, "status": "completed"})
            else:
                fixture.update({"home_goals": None, "away_goals": None, "status": "scheduled"})
            fixtures.append(fixture)
    return fixtures


def blank_row(team: str, group: str) -> dict:
    return {
        "team": team,
        "group": group,
        "played": 0,
        "won": 0,
        "drawn": 0,
        "lost": 0,
        "gf": 0,
        "ga": 0,
        "gd": 0,
        "points": 0,
        "rank": FIFA_RANKS.get(team, 99),
    }


def standings_from_fixtures(fixtures: list[dict]) -> dict:
    groups = {group: [blank_row(team, group) for team in teams] for group, teams in GROUPS.items()}
    by_team = {row["team"]: row for rows in groups.values() for row in rows}

    for match in fixtures:
        if match.get("status") != "completed":
            continue
        home, away = match["home"], match["away"]
        hg, ag = int(match["home_goals"]), int(match["away_goals"])
        if home not in by_team or away not in by_team:
            continue
        hr, ar = by_team[home], by_team[away]
        hr["played"] += 1
        ar["played"] += 1
        hr["gf"] += hg
        hr["ga"] += ag
        ar["gf"] += ag
        ar["ga"] += hg
        if hg > ag:
            hr["won"] += 1
            ar["lost"] += 1
            hr["points"] += 3
        elif hg < ag:
            ar["won"] += 1
            hr["lost"] += 1
            ar["points"] += 3
        else:
            hr["drawn"] += 1
            ar["drawn"] += 1
            hr["points"] += 1
            ar["points"] += 1

    for rows in groups.values():
        for row in rows:
            row["gd"] = row["gf"] - row["ga"]
        rows.sort(key=standings_sort_key)
        for pos, row in enumerate(rows, start=1):
            row["position"] = pos
    return groups


def standings_sort_key(row: dict) -> tuple:
    return (-row["points"], -row["gd"], -row["gf"], row.get("rank", 99), row["team"])


def valid_standing_row(row: dict) -> bool:
    return (
        0 <= row["played"] <= 3
        and row["played"] == row["won"] + row["drawn"] + row["lost"]
        and row["gd"] == row["gf"] - row["ga"]
        and row["points"] == row["won"] * 3 + row["drawn"]
    )


def outcome_prob(home: str, away: str) -> tuple[float, float, float]:
    rh = FIFA_RANKS.get(home, 65)
    ra = FIFA_RANKS.get(away, 65)
    diff = max(-35, min(35, ra - rh))
    draw = max(0.18, min(0.30, 0.25 - abs(diff) * 0.0012))
    home_edge = 1 / (1 + math.exp(-diff / 12))
    home_win = (1 - draw) * home_edge
    away_win = 1 - draw - home_win
    return home_win, draw, away_win


def knockout_prob(team_a: str, team_b: str) -> float:
    ra = FIFA_RANKS.get(team_a, 65)
    rb = FIFA_RANKS.get(team_b, 65)
    return 1 / (1 + math.exp(-(rb - ra) / 11))


def apply_sim_result(row_a: dict, row_b: dict, outcome: str) -> None:
    row_a["played"] += 1
    row_b["played"] += 1
    if outcome == "H":
        row_a.update(won=row_a["won"] + 1, points=row_a["points"] + 3, gf=row_a["gf"] + 2, ga=row_a["ga"] + 0)
        row_b.update(lost=row_b["lost"] + 1, gf=row_b["gf"] + 0, ga=row_b["ga"] + 2)
    elif outcome == "A":
        row_b.update(won=row_b["won"] + 1, points=row_b["points"] + 3, gf=row_b["gf"] + 2, ga=row_b["ga"] + 0)
        row_a.update(lost=row_a["lost"] + 1, gf=row_a["gf"] + 0, ga=row_a["ga"] + 2)
    else:
        row_a.update(drawn=row_a["drawn"] + 1, points=row_a["points"] + 1, gf=row_a["gf"] + 1, ga=row_a["ga"] + 1)
        row_b.update(drawn=row_b["drawn"] + 1, points=row_b["points"] + 1, gf=row_b["gf"] + 1, ga=row_b["ga"] + 1)
    row_a["gd"] = row_a["gf"] - row_a["ga"]
    row_b["gd"] = row_b["gf"] - row_b["ga"]


def simulate(fixtures: list[dict], standings: dict, runs: int = 12000) -> dict:
    rng = random.Random(91)
    slot_counts = {"C1": {}, "F2": {}, "E2": {}, "I2": {}}
    appearance_counts = {}
    combo_counts = {}
    match76_counts = {}
    match78_counts = {}

    remaining = [m for m in fixtures if m.get("status") != "completed"]

    for _ in range(runs):
        sim = deepcopy(standings)
        lookup = {row["team"]: row for rows in sim.values() for row in rows}
        for match in remaining:
            home, away = match["home"], match["away"]
            if home not in lookup or away not in lookup:
                continue
            hw, draw, _ = outcome_prob(home, away)
            roll = rng.random()
            outcome = "H" if roll < hw else "D" if roll < hw + draw else "A"
            apply_sim_result(lookup[home], lookup[away], outcome)

        for group in sim.values():
            group.sort(key=standings_sort_key)
            for idx, row in enumerate(group, start=1):
                row["position"] = idx

        c1 = sim["C"][0]["team"]
        f2 = sim["F"][1]["team"]
        e2 = sim["E"][1]["team"]
        i2 = sim["I"][1]["team"]
        slots = {"C1": c1, "F2": f2, "E2": e2, "I2": i2}
        for slot, team in slots.items():
            slot_counts[slot][team] = slot_counts[slot].get(team, 0) + 1

        m76_winner = c1 if rng.random() < knockout_prob(c1, f2) else f2
        m78_winner = e2 if rng.random() < knockout_prob(e2, i2) else i2
        match76_counts[m76_winner] = match76_counts.get(m76_winner, 0) + 1
        match78_counts[m78_winner] = match78_counts.get(m78_winner, 0) + 1
        appearance_counts[m76_winner] = appearance_counts.get(m76_winner, 0) + 1
        appearance_counts[m78_winner] = appearance_counts.get(m78_winner, 0) + 1
        combo = f"{m76_winner} vs {m78_winner}"
        combo_counts[combo] = combo_counts.get(combo, 0) + 1

    def pct_map(counts: dict) -> dict:
        return {team: round(count / runs * 100, 1) for team, count in sorted(counts.items(), key=lambda x: -x[1])}

    return {
        "runs": runs,
        "slots": {slot: pct_map(counts) for slot, counts in slot_counts.items()},
        "team_probabilities": pct_map(appearance_counts),
        "match76_winners": pct_map(match76_counts),
        "match78_winners": pct_map(match78_counts),
        "combinations": [
            {"matchup": combo, "probability": round(count / runs * 100, 1)}
            for combo, count in sorted(combo_counts.items(), key=lambda x: -x[1])[:10]
        ],
    }


def scrape_wikipedia_standings() -> tuple[dict, list[str]]:
    notes = []
    try:
        import requests
        from bs4 import BeautifulSoup
    except Exception as exc:
        return {}, [f"Live standings scrape skipped because optional dependencies are unavailable: {exc}"]

    scraped_groups = {}
    session = requests.Session()
    session.headers.update({"User-Agent": "MetLifeMatch91Tracker/1.0 (public GitHub Pages updater)"})
    for group, teams in GROUPS.items():
        url = f"https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_Group_{group}"
        try:
            html = session.get(url, timeout=25).text
            soup = BeautifulSoup(html, "html.parser")
        except Exception as exc:
            notes.append(f"Group {group}: fetch failed ({exc})")
            continue

        team_set = {norm_team(t) for t in teams}
        parsed_rows = []
        for table in soup.find_all("table"):
            text = table.get_text(" ", strip=True)
            if "Pld" not in text or "Pts" not in text:
                continue
            if sum(1 for team in team_set if team in text) < 3:
                continue
            for tr in table.find_all("tr"):
                cells = [cell.get_text(" ", strip=True) for cell in tr.find_all(["th", "td"])]
                if len(cells) < 9:
                    continue
                row_text = " ".join(cells)
                team = next((candidate for candidate in teams if re.search(rf"\b{re.escape(candidate)}\b", row_text)), None)
                if not team:
                    continue
                numbers = []
                for cell in cells:
                    cleaned = cell.replace("−", "-")
                    if re.fullmatch(r"[+-]?\d+", cleaned):
                        numbers.append(int(cleaned))
                if len(numbers) < 8:
                    continue
                # Tables may include a leading position column; the final eight numbers are W-D-L/GF/GA/GD/Pts plus played.
                played, won, drawn, lost, gf, ga, gd, points = numbers[-8:]
                parsed_rows.append(
                    {
                        "team": team,
                        "group": group,
                        "played": played,
                        "won": won,
                        "drawn": drawn,
                        "lost": lost,
                        "gf": gf,
                        "ga": ga,
                        "gd": gd,
                        "points": points,
                        "rank": FIFA_RANKS.get(team, 99),
                    }
                )
            if len({row["team"] for row in parsed_rows}) == 4:
                break
        unique = {row["team"]: row for row in parsed_rows if valid_standing_row(row)}
        if len(unique) == 4:
            rows = list(unique.values())
            rows.sort(key=standings_sort_key)
            for pos, row in enumerate(rows, start=1):
                row["position"] = pos
            scraped_groups[group] = rows
        else:
            notes.append(f"Group {group}: standings table was not parsed cleanly; fallback standings kept.")
    if scraped_groups:
        notes.append(f"Merged live standings for {len(scraped_groups)} groups from Wikipedia group pages.")
    return scraped_groups, notes


def projection_from_standings(standings: dict) -> dict:
    c1 = standings["C"][0]["team"]
    f2 = standings["F"][1]["team"]
    e2 = standings["E"][1]["team"]
    i2 = standings["I"][1]["team"]
    m76 = c1 if knockout_prob(c1, f2) >= 0.5 else f2
    m78 = e2 if knockout_prob(e2, i2) >= 0.5 else i2
    return {
        "slots": {"C1": c1, "F2": f2, "E2": e2, "I2": i2},
        "match76": {"home": c1, "away": f2, "projected_winner": m76},
        "match78": {"home": e2, "away": i2, "projected_winner": m78},
        "match91": f"{m76} vs {m78}",
    }


def latest_and_upcoming(fixtures: list[dict], report_date: str) -> tuple[list[dict], list[dict]]:
    completed = sorted([m for m in fixtures if m["status"] == "completed"], key=lambda x: x["date"], reverse=True)
    upcoming = sorted([m for m in fixtures if m["status"] != "completed" and m["date"] >= report_date], key=lambda x: x["date"])
    return completed[:8], upcoming[:8]


def previous_probabilities(report_date: str) -> dict:
    path = DATA_DIR / "tracker.json"
    if not path.exists():
        return {}
    try:
        previous = json.loads(path.read_text(encoding="utf-8"))
        if previous.get("report_date") == report_date:
            return {}
        return previous.get("simulation", {}).get("team_probabilities", {})
    except Exception:
        return {}


def build_payload(fetch: bool) -> dict:
    DATA_DIR.mkdir(exist_ok=True)
    today = datetime.now(timezone.utc).astimezone().date().isoformat()
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    notes = []

    fixtures = seeded_fixtures()
    if fetch:
        try:
            fixtures, fifa_notes = fetch_fifa_fixtures()
            notes.extend(fifa_notes)
        except Exception as exc:
            notes.append(f"FIFA match API fetch failed; seeded fallback data was used. Error: {exc}")
    else:
        notes.append("Fetch disabled; seeded fallback data was used.")

    standings = standings_from_fixtures(fixtures)
    projection = projection_from_standings(standings)
    simulation = simulate(fixtures, standings)
    projection["current_projected_match91"] = projection["match91"]
    projection["most_likely_match91"] = simulation["combinations"][0]["matchup"] if simulation["combinations"] else projection["match91"]
    latest_results, upcoming = latest_and_upcoming(fixtures, today)
    prev = previous_probabilities(today)

    probability_changes = {}
    for team, value in simulation["team_probabilities"].items():
        probability_changes[team] = round(value - float(prev.get(team, value)), 1)

    return {
        "generated_at": generated_at,
        "report_date": today,
        "match91": {
            "date": "2026-07-05",
            "venue": "MetLife Stadium, East Rutherford",
            "structure": {
                "Match 91": "Winner(Match 76) vs Winner(Match 78)",
                "Match 76": "Group C Winner (C1) vs Group F Runner-up (F2)",
                "Match 78": "Group E Runner-up (E2) vs Group I Runner-up (I2)",
            },
        },
        "groups": standings,
        "fixtures": fixtures,
        "latest_results": latest_results,
        "upcoming_fixtures": upcoming,
        "projection": projection,
        "simulation": simulation,
        "probability_changes": probability_changes,
        "owner_teams": sorted(OWNER_TEAMS),
        "data_notes": notes,
        "sources": [
            FIFA_MATCH_API,
            "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026",
        ],
    }


def fmt_match(match: dict) -> str:
    if match["status"] == "completed":
        return f"{match['date']} - Group {match['group']}: {match['home']} {match['home_goals']}-{match['away_goals']} {match['away']}"
    return f"{match['date']} - Group {match['group']}: {match['home']} vs {match['away']}"


def brazil_commentary(payload: dict) -> str:
    standings = payload["groups"]["C"]
    brazil = next(row for row in standings if row["team"] == "Brazil")
    slots = payload["simulation"]["slots"]
    c1_prob = slots.get("C1", {}).get("Brazil", 0)
    match91_prob = payload["simulation"]["team_probabilities"].get("Brazil", 0)
    f2 = max(payload["simulation"]["slots"].get("F2", {}).items(), key=lambda x: x[1])[0]
    return (
        f"Brazil are currently {ordinal(brazil['position'])} in Group C with {brazil['points']} points, "
        f"{brazil['gf']} goals for, {brazil['ga']} against, and a {brazil['gd']:+d} goal difference. "
        f"The model gives Brazil a {c1_prob:.1f}% chance to win Group C and a {match91_prob:.1f}% chance to reach Match 91. "
        f"The most common Match 76 opponent in the current simulation is {f2}, because the Group C winner faces the Group F runner-up."
    )


def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def render_report(payload: dict) -> str:
    projection = payload["projection"]
    lines = [
        f"# Match 91 Daily Report - {payload['report_date']}",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "## Match 91 Projection",
        "",
        f"- Most likely matchup: **{projection['most_likely_match91']}**",
        f"- Current bracket projection: **{projection['current_projected_match91']}**",
        f"- Match 76: {projection['match76']['home']} vs {projection['match76']['away']} -> projected winner: {projection['match76']['projected_winner']}",
        f"- Match 78: {projection['match78']['home']} vs {projection['match78']['away']} -> projected winner: {projection['match78']['projected_winner']}",
        "",
        "## Top 10 Match 91 Combinations",
        "",
    ]
    for idx, combo in enumerate(payload["simulation"]["combinations"], start=1):
        lines.append(f"{idx}. {combo['matchup']} - {combo['probability']:.1f}%")
    lines.extend(["", "## Team Appearance Probabilities", ""])
    for team, probability in sorted(payload["simulation"]["team_probabilities"].items(), key=lambda x: -x[1])[:20]:
        change = payload["probability_changes"].get(team, 0)
        lines.append(f"- {team}: {probability:.1f}% ({change:+.1f} pts vs previous run)")
    lines.extend(["", "## Latest Results", ""])
    for match in payload["latest_results"]:
        lines.append(f"- {fmt_match(match)}")
    lines.extend(["", "## Updated Standings", ""])
    for group in PRIORITY_GROUPS + [g for g in GROUPS if g not in PRIORITY_GROUPS]:
        lines.append(f"### Group {group}")
        lines.append("")
        lines.append("| Pos | Team | Pld | W | D | L | GF | GA | GD | Pts |")
        lines.append("| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for row in payload["groups"][group]:
            lines.append(
                f"| {row['position']} | {row['team']} | {row['played']} | {row['won']} | {row['drawn']} | {row['lost']} | {row['gf']} | {row['ga']} | {row['gd']:+d} | {row['points']} |"
            )
        lines.append("")
    lines.extend(["## Brazil Path Commentary", "", brazil_commentary(payload), "", "## Data Notes", ""])
    for note in payload["data_notes"]:
        lines.append(f"- {note}")
    lines.extend(["", "## Sources", ""])
    for source in payload["sources"]:
        lines.append(f"- {source}")
    lines.append("")
    return "\n".join(lines)


def row_class(team: str, group: str) -> str:
    classes = []
    if group in PRIORITY_GROUPS:
        classes.append("priority")
    if team in OWNER_TEAMS:
        classes.append("watch")
    return " ".join(classes)


def render_standings(payload: dict) -> str:
    parts = []
    for group in PRIORITY_GROUPS + [g for g in GROUPS if g not in PRIORITY_GROUPS]:
        parts.append(f"<section class='group-card' id='group-{group}'><h3>Group {group}</h3><table><thead><tr><th>Pos</th><th>Team</th><th>Pld</th><th>W</th><th>D</th><th>L</th><th>GF</th><th>GA</th><th>GD</th><th>Pts</th></tr></thead><tbody>")
        for row in payload["groups"][group]:
            parts.append(
                f"<tr class='{row_class(row['team'], group)}'><td>{row['position']}</td><td>{row['team']}</td><td>{row['played']}</td><td>{row['won']}</td><td>{row['drawn']}</td><td>{row['lost']}</td><td>{row['gf']}</td><td>{row['ga']}</td><td>{row['gd']:+d}</td><td><strong>{row['points']}</strong></td></tr>"
            )
        parts.append("</tbody></table></section>")
    return "\n".join(parts)


def render_html(payload: dict) -> str:
    sim = payload["simulation"]
    projection = payload["projection"]
    most_likely_left, most_likely_right = projection["most_likely_match91"].split(" vs ", 1)
    combos = "\n".join(
        f"<tr><td>{idx}</td><td>{combo['matchup']}</td><td><strong>{combo['probability']:.1f}%</strong></td></tr>"
        for idx, combo in enumerate(sim["combinations"], start=1)
    )
    owner_probs = "\n".join(
        f"<tr><td>{team}</td><td>{sim['team_probabilities'].get(team, 0):.1f}%</td><td>{payload['probability_changes'].get(team, 0):+.1f}</td></tr>"
        for team in sorted(OWNER_TEAMS, key=lambda t: -sim["team_probabilities"].get(t, 0))
    )
    latest = "\n".join(f"<li>{fmt_match(match)}</li>" for match in payload["latest_results"][:6])
    upcoming = "\n".join(f"<li>{fmt_match(match)}</li>" for match in payload["upcoming_fixtures"][:6])
    reports = f"<li><a href='reports/{payload['report_date']}.md'>{payload['report_date']}</a></li><li><a href='reports/latest.md'>latest.md</a></li>"
    standings = render_standings(payload)
    data_json = json.dumps(payload, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MetLife Match 91 Tracker</title>
  <meta name="description" content="Daily World Cup 2026 Match 91 projection tracker for MetLife Stadium ticket holders.">
  <style>
    :root {{
      --blue: #0b5cab;
      --blue-dark: #073b73;
      --green: #0f7a34;
      --ink: #142033;
      --muted: #607089;
      --line: #dbe3ee;
      --surface: #ffffff;
      --bg: #f4f7fb;
      --gold: #f5b700;
      --shadow: 0 18px 45px rgba(17, 38, 72, .10);
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: var(--ink); background: var(--bg); }}
    a {{ color: var(--blue); text-decoration: none; }}
    header {{ position: sticky; top: 0; z-index: 5; background: rgba(255,255,255,.94); border-bottom: 1px solid var(--line); backdrop-filter: blur(14px); }}
    .nav {{ max-width: 1180px; margin: 0 auto; padding: 16px 20px; display: flex; gap: 22px; align-items: center; justify-content: space-between; }}
    .brand {{ font-size: clamp(1.35rem, 2vw, 2rem); font-weight: 850; letter-spacing: 0; }}
    .brand span {{ color: var(--blue); }}
    .links {{ display: flex; gap: 18px; flex-wrap: wrap; font-size: .92rem; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 22px 20px 48px; }}
    .updated {{ text-align: right; color: var(--muted); font-size: .92rem; margin: 0 0 14px; }}
    .hero-grid {{ display: grid; grid-template-columns: minmax(0, 1.55fr) minmax(290px, .85fr); gap: 18px; align-items: stretch; }}
    .hero {{ min-height: 330px; padding: 28px; color: white; border-radius: 8px; box-shadow: var(--shadow); background:
      linear-gradient(90deg, rgba(5,25,47,.86), rgba(9,72,132,.78)),
      repeating-linear-gradient(90deg, rgba(255,255,255,.08) 0 1px, transparent 1px 120px),
      linear-gradient(160deg, #114b84, #09213f 55%, #0a632d); display: flex; flex-direction: column; justify-content: space-between; overflow: hidden; }}
    .hero h1 {{ margin: 0; font-size: clamp(2rem, 5vw, 4.1rem); line-height: .96; letter-spacing: 0; }}
    .hero p {{ max-width: 650px; font-size: 1.02rem; color: rgba(255,255,255,.82); }}
    .matchup {{ display: grid; grid-template-columns: 1fr 72px 1fr; border-radius: 8px; overflow: hidden; max-width: 720px; font-weight: 850; font-size: clamp(1.5rem, 4vw, 2.8rem); text-align: center; box-shadow: 0 20px 48px rgba(0,0,0,.25); }}
    .matchup div {{ padding: 19px 12px; }}
    .team-a {{ background: var(--green); }}
    .versus {{ background: white; color: var(--ink); }}
    .team-b {{ background: var(--blue); }}
    .panel {{ background: var(--surface); border: 1px solid var(--line); border-radius: 8px; box-shadow: var(--shadow); }}
    .panel, .group-card {{ overflow-x: auto; }}
    .panel h2, .panel h3 {{ margin: 0; padding: 16px 18px; font-size: .95rem; text-transform: uppercase; letter-spacing: .02em; border-bottom: 1px solid var(--line); }}
    .brazil {{ border-top: 4px solid var(--green); }}
    .brazil .big {{ font-size: 3.4rem; color: var(--green); font-weight: 850; padding: 20px 18px 4px; }}
    .brazil p {{ padding: 0 18px 18px; margin: 0; color: var(--muted); line-height: 1.55; }}
    table {{ width: 100%; border-collapse: collapse; font-size: .91rem; }}
    th, td {{ padding: 10px 12px; border-bottom: 1px solid var(--line); text-align: left; }}
    th {{ color: #34445d; font-size: .74rem; text-transform: uppercase; letter-spacing: .04em; background: #f8fafc; }}
    .content-grid {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(320px, .7fr); gap: 18px; margin-top: 18px; align-items: start; }}
    .path {{ padding: 18px; }}
    .path-flow {{ display: grid; grid-template-columns: 1fr auto 1fr auto 1fr; gap: 12px; align-items: center; }}
    .slot {{ border: 1px solid var(--line); background: #f9fbfe; border-radius: 8px; padding: 14px; min-height: 92px; }}
    .slot strong {{ display: block; font-size: 1.25rem; margin-top: 6px; }}
    .arrow {{ color: var(--blue); font-size: 1.8rem; font-weight: 800; }}
    .section-title {{ margin: 34px 0 12px; font-size: 1.35rem; }}
    .standings-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }}
    .group-card {{ background: white; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; overflow-x: auto; }}
    .group-card h3 {{ margin: 0; padding: 13px 14px; background: #f8fafc; border-bottom: 1px solid var(--line); }}
    .group-card:nth-child(-n+4) h3 {{ color: var(--blue-dark); box-shadow: inset 4px 0 var(--gold); }}
    tr.watch td:first-child, tr.watch td:nth-child(2) {{ color: var(--green); font-weight: 800; }}
    .split {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
    .list {{ margin: 0; padding: 14px 18px 18px 34px; line-height: 1.8; color: #26364f; }}
    footer {{ border-top: 1px solid var(--line); color: var(--muted); padding: 24px 0; margin-top: 38px; font-size: .9rem; }}
    @media (max-width: 860px) {{
      .nav {{ align-items: flex-start; flex-direction: column; gap: 10px; }}
      .hero-grid, .content-grid, .split, .standings-grid {{ grid-template-columns: 1fr; }}
      .matchup {{ grid-template-columns: 1fr; }}
      .path-flow {{ grid-template-columns: 1fr; }}
      .arrow {{ transform: rotate(90deg); justify-self: center; }}
      .updated {{ text-align: left; }}
      th, td {{ padding: 8px 7px; font-size: .82rem; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="nav">
      <div class="brand"><span>MetLife</span> Match 91 Tracker</div>
      <nav class="links">
        <a href="#tracker">Match 91 Tracker</a>
        <a href="#brazil">Brazil Tracker</a>
        <a href="#standings">Standings</a>
        <a href="#probabilities">Probability Table</a>
        <a href="#reports">Reports</a>
      </nav>
    </div>
  </header>
  <main>
    <p class="updated">Latest update: {payload['generated_at']} | Daily automation target: 8:00 AM America/New_York</p>
    <section class="hero-grid" id="tracker">
      <div class="hero">
        <div>
          <h1>Match 91 Tracker</h1>
          <p>Round of 16 projection for MetLife Stadium on July 5, 2026. Match 91 is Winner(Match 76) vs Winner(Match 78).</p>
        </div>
        <div class="matchup" aria-label="Projected Match 91 matchup">
          <div class="team-a">{most_likely_left}</div>
          <div class="versus">vs</div>
          <div class="team-b">{most_likely_right}</div>
        </div>
      </div>
      <aside class="panel brazil" id="brazil">
        <h2>Brazil Tracker</h2>
        <div class="big">{sim['team_probabilities'].get('Brazil', 0):.1f}%</div>
        <p>Estimated chance Brazil appears in Match 91. Current projected Match 76 path: {projection['match76']['home']} vs {projection['match76']['away']}.</p>
      </aside>
    </section>
    <section class="content-grid">
      <div class="panel">
        <h2>Top 10 Probable Match 91 Combinations</h2>
        <table><thead><tr><th>Rank</th><th>Matchup</th><th>Probability</th></tr></thead><tbody>{combos}</tbody></table>
      </div>
      <div class="panel">
        <h2>Match 91 Projection</h2>
        <table><tbody>
          <tr><th>Most likely</th><td><strong>{projection['most_likely_match91']}</strong></td></tr>
          <tr><th>Current bracket</th><td>{projection['current_projected_match91']}</td></tr>
          <tr><th>Match 76</th><td>{projection['match76']['home']} vs {projection['match76']['away']}</td></tr>
          <tr><th>Match 78</th><td>{projection['match78']['home']} vs {projection['match78']['away']}</td></tr>
          <tr><th>Simulation</th><td>{sim['runs']:,} runs</td></tr>
        </tbody></table>
      </div>
    </section>
    <section class="panel path" aria-label="Match 91 path visualization">
      <h2>Match 91 Path Visualization</h2>
      <div class="path-flow">
        <div class="slot">Group C Winner<strong>{projection['slots']['C1']}</strong></div>
        <div class="arrow">-></div>
        <div class="slot">Match 76<strong>{projection['match76']['projected_winner']}</strong><small>C1 vs F2</small></div>
        <div class="arrow">-></div>
        <div class="slot">Match 91<strong>{projection['match91']}</strong></div>
        <div class="slot">Group F Runner-up<strong>{projection['slots']['F2']}</strong></div>
        <div class="arrow">-></div>
        <div class="slot">Match 78<strong>{projection['match78']['projected_winner']}</strong><small>E2 vs I2</small></div>
        <div class="arrow">-></div>
        <div class="slot">MetLife Stadium<strong>July 5, 2026</strong></div>
        <div class="slot">Group E Runner-up<strong>{projection['slots']['E2']}</strong></div>
        <div></div>
        <div class="slot">Group I Runner-up<strong>{projection['slots']['I2']}</strong></div>
      </div>
    </section>
    <h2 class="section-title" id="probabilities">Probability Table</h2>
    <section class="panel">
      <table><thead><tr><th>Watch Team</th><th>Appearing in Match 91</th><th>Change vs Previous Run</th></tr></thead><tbody>{owner_probs}</tbody></table>
    </section>
    <h2 class="section-title" id="standings">Standings</h2>
    <div class="standings-grid">{standings}</div>
    <section class="split" id="results">
      <div class="panel"><h2>Latest Results</h2><ul class="list">{latest}</ul></div>
      <div class="panel"><h2>Upcoming Fixtures</h2><ul class="list">{upcoming}</ul></div>
    </section>
    <section class="panel" id="reports" style="margin-top:18px">
      <h2>Daily Report Archive</h2>
      <ul class="list">{reports}</ul>
    </section>
    <footer>
      Data source notes: public FIFA/Wikipedia-referenced tournament pages, with seeded fallback records when live parsing is unavailable. Probabilities are estimates, not betting advice.
    </footer>
  </main>
  <script type="application/json" id="tracker-data">{data_json}</script>
</body>
</html>
"""


def write_outputs(payload: dict) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    DOCS_DIR.mkdir(exist_ok=True)
    (DOCS_DIR / "reports").mkdir(exist_ok=True)
    (DATA_DIR / "tracker.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    report = render_report(payload)
    (REPORTS_DIR / f"{payload['report_date']}.md").write_text(report, encoding="utf-8")
    (REPORTS_DIR / "latest.md").write_text(report, encoding="utf-8")
    (DOCS_DIR / "reports" / f"{payload['report_date']}.md").write_text(report, encoding="utf-8")
    (DOCS_DIR / "reports" / "latest.md").write_text(report, encoding="utf-8")
    (DOCS_DIR / "index.html").write_text(render_html(payload), encoding="utf-8")
    (DOCS_DIR / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Update Match 91 data, reports, and static site.")
    parser.add_argument("--no-fetch", action="store_true", help="Use seeded fallback data only.")
    args = parser.parse_args()
    payload = build_payload(fetch=not args.no_fetch)
    write_outputs(payload)
    print(f"Updated Match 91 tracker for {payload['report_date']}")
    print(f"Projection: {payload['projection']['match91']}")


if __name__ == "__main__":
    main()
