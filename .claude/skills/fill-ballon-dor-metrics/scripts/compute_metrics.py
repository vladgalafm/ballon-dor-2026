#!/usr/bin/env python3
"""Compute the metric cells (E:AF) of the Ballon d'Or 2025-26 sheet from player-stats JSON.

Reads column D of the sheet (one line per sheet row), finds the position blocks,
and writes a JSON file with one update range per block (or per contiguous run of
filtered players). Never produces anything outside columns E:AF of player rows.
Formulas and N/A policy: .claude/rules/ballon-dor-metrics.md
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

NA = "N/A"
FIRST_COL, LAST_COL = "E", "AF"  # 7 metric groups x 4 competition columns

# Column offset within each 4-column group -> (label, candidate files)
COMPETITIONS = [
    ("Dom. League", ["domestic-league"]),
    ("Dom. Cup", ["domestic-cup", "africa-cup-of-nations"]),
    ("Int. Cup", ["international-cup"]),
    ("World Cup", ["world-cup"]),
]

SHARED = ["90s played", "Rating (Sofascore + WhoScored)"]
POSITIONS = {
    "GK": ["Saves, %", "Goals Against, per 90", "Goals Prevented, +/-", "Clean Sheets, %", "Accurate Long Balls, %"],
    "CB": ["Tackles Won, %", "Aerial Duels Won, %", "Defensive Actions, per 90", "Accurate Passes, %", "Accurate Long Balls, %"],
    "LB/RB/LWB/RWB": ["Ground Duels Won, %", "Defensive Actions, per 90", "Accurate Final Third Passes, per 90", "Attacking Actions, per 90", "xG + xA, per 90"],
    "DMC/MC": ["Defensive Actions, per 90", "Press Resistance x Ground Engagement Win Rate, %", "Accurate Passes, %", "Accurate Final Third Passes, per 90", "Attacking Actions, per 90"],
    "MC/AMC": ["Goals, per 90", "xA, per 90", "Press Resistance x Ground Engagement Win Rate, %", "Accurate Final Third Passes, per 90", "Attacking Actions, per 90"],
    "LW/RW": ["Goals, per 90", "Goals, per Shot", "xA, per 90", "Dribbles Success, %", "Attacking Actions, per 90"],
    "CF/SS": ["Goals, per 90", "Goals, per Shot", "xA, per 90", "Aerial Duels Won, %", "Attacking Actions, per 90"],
}

# ---------------------------------------------------------------- formulas


def ratio(a, b):
    return None if a is None or b is None or b == 0 else a / b


def total(s, plus, minus=()):
    """Sum of `plus` fields minus `minus` fields; None if any field is missing."""
    keys = list(plus) + list(minus)
    if any(s.get(k) is None for k in keys):
        return None
    return sum(s[k] for k in plus) - sum(s[k] for k in minus)


def per90(s, numerator):
    m90 = ratio(s.get("minutesPlayed"), 90)
    return ratio(numerator, m90)


def field_pct(s, key):
    return None if s.get(key) is None else s[key] / 100


def count_pct(s, hit, tot, pct_key):
    """hit/tot, falling back to the provider percentage only when a count is missing."""
    if s.get(hit) is not None and s.get(tot) is not None:
        return ratio(s[hit], s[tot])
    return field_pct(s, pct_key)


def press_resistance(s):
    keys = ("touches", "dispossessed", "groundDuelsWon", "groundDuelsWonPercentage", "dribbledPast")
    if any(s.get(k) is None for k in keys):
        return None
    resist = ratio(s["touches"], s["touches"] + s["dispossessed"])
    contested = ratio(s["groundDuelsWon"], s["groundDuelsWonPercentage"] / 100)
    if resist is None or contested is None:
        return None
    engage = ratio(s["groundDuelsWon"], contested + s["dribbledPast"])
    return None if engage is None else resist * engage


def rating(s):
    if s.get("rating") is None or s.get("whoScoredRating") is None:
        return None
    return (s["rating"] + s["whoScoredRating"]) / 2


METRICS = {
    "90s played": lambda s: ratio(s.get("minutesPlayed"), 90),
    "Rating (Sofascore + WhoScored)": rating,
    "Saves, %": lambda s: field_pct(s, "savesPercentage"),
    "Goals Against, per 90": lambda s: per90(s, s.get("goalsConceded")),
    "Goals Prevented, +/-": lambda s: s.get("goalsPrevented"),
    "Clean Sheets, %": lambda s: ratio(s.get("cleanSheet"), s.get("matchesStarted")),
    "Accurate Long Balls, %": lambda s: count_pct(s, "accurateLongBalls", "totalLongBalls", "accurateLongBallsPercentage"),
    "Tackles Won, %": lambda s: count_pct(s, "tacklesWon", "tackles", "tacklesWonPercentage"),
    "Accurate Passes, %": lambda s: count_pct(s, "accuratePasses", "totalPasses", "accuratePassesPercentage"),
    "Aerial Duels Won, %": lambda s: field_pct(s, "aerialDuelsWonPercentage"),
    "Ground Duels Won, %": lambda s: field_pct(s, "groundDuelsWonPercentage"),
    "Dribbles Success, %": lambda s: field_pct(s, "successfulDribblesPercentage"),
    "Defensive Actions, per 90": lambda s: per90(s, total(s, ["tacklesWon", "interceptions", "blockedShots", "clearances"], ["fouls", "ownGoals"])),
    "Accurate Final Third Passes, per 90": lambda s: per90(s, s.get("accurateFinalThirdPasses")),
    "Attacking Actions, per 90": lambda s: per90(s, total(
        s,
        ["goals", "assists", "shotsOnTarget", "successfulDribbles", "keyPasses", "accurateCrosses"],
        ["penaltyGoals", "attemptPenaltyTarget", "dispossessed"],
    )),
    "xG + xA, per 90": lambda s: per90(s, total(s, ["expectedGoals", "expectedAssists"])),
    "xA, per 90": lambda s: per90(s, s.get("expectedAssists")),
    "Goals, per 90": lambda s: per90(s, s.get("goals")),
    "Goals, per Shot": lambda s: ratio(s.get("goals"), s.get("totalShots")),
    "Press Resistance x Ground Engagement Win Rate, %": press_resistance,
}
PERCENT_METRICS = {m for m in METRICS if m.endswith(", %")} - {"Goals Prevented, +/-"}

# ------------------------------------------------------------------ layout


def slugify(name):
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")


def parse_blocks(lines):
    """Yield (position, [(row, display_name, is_wildcard)]) for each position block."""
    blocks, i = [], 0
    while i < len(lines):
        label = lines[i].strip()
        if label in POSITIONS:
            players, r = [], i + 2  # skip the competition-label row
            while r < len(lines) and lines[r].strip():
                name = lines[r].strip()
                players.append((r + 1, name.rstrip("*").strip(), name.endswith("*")))
                r += 1
            blocks.append((label, players))
            i = r
        i += 1
    return blocks


def load_stats(stats_dir, slug):
    """Return {competition label: (statistics, competition name)} for one player."""
    found = {}
    for label, categories in COMPETITIONS:
        hits = [(c, stats_dir / slug / f"{c}.json") for c in categories]
        hits = [(c, p) for c, p in hits if p.exists()]
        if len(hits) > 1:
            sys.exit(f"ERROR: {slug} has both {[c for c, _ in hits]} for column '{label}'. Ask the user which to use.")
        if hits:
            category, path = hits[0]
            data = json.loads(path.read_text())
            name = data.get("competition", {}).get("name") or ("World Cup" if category == "world-cup" else category)
            found[label] = (data["statistics"], name)
    return found


def compute_row(position, stats, warnings, player):
    row = []
    for metric in POSITIONS[position] + SHARED:
        for label, _ in COMPETITIONS:
            value = None
            if label in stats:
                value = METRICS[metric](stats[label][0])
                if value is not None:
                    if metric in PERCENT_METRICS and not 0 <= value <= 1:
                        warnings.append(f"{player} / {label} / {metric}: {value:.4f} outside 0..1")
                    if metric == "Goals Prevented, +/-" and value == 0:
                        warnings.append(f"{player} / {label} / {metric}: exactly 0, possibly an untracked placeholder")
            row.append(NA if value is None else round(value, 6))
    return row


def runs(rows):
    """Group (row, ...) items into runs of consecutive sheet rows."""
    out = []
    for item in rows:
        if out and item[0] == out[-1][-1][0] + 1:
            out[-1].append(item)
        else:
            out.append([item])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--column-d", required=True, help="text file: line N = value of sheet cell DN (blank lines allowed)")
    ap.add_argument("--stats-dir", required=True, help="absolute path to the player-stats folder")
    ap.add_argument("--out", required=True, help="where to write the JSON result")
    ap.add_argument("--sheet", default="2025-26", help="tab name used in the output ranges")
    ap.add_argument("--players", default="", help="comma-separated names to restrict the output to")
    args = ap.parse_args()

    stats_dir = Path(args.stats_dir)
    lines = Path(args.column_d).read_text().split("\n")
    wanted = {slugify(p) for p in args.players.split(",") if p.strip()}

    blocks, warnings, summary, seen = [], [], [], set()
    for position, players in parse_blocks(lines):
        rows = []
        for sheet_row, name, wildcard in players:
            slug = slugify(name)
            if not (stats_dir / slug).is_dir():
                sys.exit(f"ERROR: no folder player-stats/{slug} for '{name}' (row {sheet_row})")
            seen.add(slug)
            if wanted and slug not in wanted:
                continue
            stats = load_stats(stats_dir, slug)
            values = compute_row(position, stats, warnings, name)
            rows.append((sheet_row, name, values))
            # Data gaps only: cells of competitions the player has no file for are N/A by definition.
            gaps = [f"{(POSITIONS[position] + SHARED)[k // 4]}@{COMPETITIONS[k % 4][0]}" for k, v in enumerate(values) if v == NA and COMPETITIONS[k % 4][0] in stats]
            comps = ", ".join(f"{label}={stats[label][1]}" for label, _ in COMPETITIONS if label in stats)
            absent = [label for label, _ in COMPETITIONS if label not in stats]
            summary.append(
                f"{position:14} row {sheet_row:>2}  {name}{'*' if wildcard else ''}: {comps}"
                + (f"\n{'':19}no file: {', '.join(absent)}" if absent else "")
                + (f"\n{'':19}missing data: {', '.join(gaps)}" if gaps else "")
            )
        writes = [
            {
                "range": f"'{args.sheet}'!{FIRST_COL}{run[0][0]}:{LAST_COL}{run[-1][0]}",
                "players": [r[1] for r in run],
                "values": [r[2] for r in run],
            }
            for run in runs(rows)
        ]
        blocks.append({"position": position, "metrics": POSITIONS[position] + SHARED, "writes": writes})

    missing = wanted - seen
    if missing:
        sys.exit(f"ERROR: --players names not found in column D: {sorted(missing)}")

    Path(args.out).write_text(json.dumps({"blocks": blocks, "warnings": warnings}, ensure_ascii=False, indent=1))
    print("\n".join(summary))
    print(f"\n{len(warnings)} warning(s)" + ("".join(f"\n  - {w}" for w in warnings)))
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
