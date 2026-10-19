#!/usr/bin/env python3
"""Build the Stats Points formulas (column AG) of the Ballon d'Or 2025-26 sheet.

Reads column D of the sheet (one line per sheet row), finds the position blocks, works out which
coefficient cell (H61:H79) applies to each player's Dom. League / Dom. Cup / Int. Cup / World Cup
column from the player-stats JSON, and writes one formula per player row. Output ranges are
AG<row> only. Formula definition: .claude/rules/ballon-dor-scoring.md (Stats Points)

Argument separators are ";" because the sheet uses a decimal-comma locale (a "," gives #ERROR!).
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

# Position block -> first row of its five metric rows in P61:R95 (P weight, Q mean, R SD)
POSITION_COEF_ROW = {
    "GK": 61,
    "CB": 66,
    "LB/RB/LWB/RWB": 71,
    "DMC/MC": 76,
    "MC/AMC": 81,
    "LW/RW": 86,
    "CF/SS": 91,
}
N90_COEF, RATING_COEF = 96, 97  # P96 (90s played), P97 (Rating)

# JSON competition.name -> row of its coefficient in H61:H79 (see ballon-dor-scoring.md)
COEF_ROW = {
    "Premier League": 61, "LaLiga": 62, "Bundesliga": 63, "Serie A": 64, "Ligue 1": 65,
    "Major League Soccer": 66, "Saudi Pro League": 67, "Liga Portugal 2": 68,
    "EFL Cup": 69, "Copa del Rey": 70, "DFB Pokal": 71, "Coppa Italia": 72, "Leagues Cup": 73,
    "King's Cup": 74, "Africa Cup of Nations": 75,
    "UEFA Champions League": 76, "CONCACAF Champions Cup": 77, "AFC Champions League Two": 78,
}
WORLD_CUP_ROW = 79  # world-cup.json has no competition.name

# Sheet column group -> candidate files. Same convention as the metrics skill: Hakimi and Mane
# have AFCON in the Dom. Cup column.
COMPETITIONS = [
    ("Dom. League", ["domestic-league"]),
    ("Dom. Cup", ["domestic-cup", "africa-cup-of-nations"]),
    ("Int. Cup", ["international-cup"]),
    ("World Cup", ["world-cup"]),
]
# Sheet column letters of each metric group's 4 competition columns
METRIC_COLS = [("E", "F", "G", "H"), ("I", "J", "K", "L"), ("M", "N", "O", "P"), ("Q", "R", "S", "T"), ("U", "V", "W", "X")]
N90_COLS = ("Y", "Z", "AA", "AB")
RATING_COLS = ("AC", "AD", "AE", "AF")


def slugify(name):
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")


def parse_blocks(lines):
    """Yield (position, [(row, display_name)]) for each position block."""
    blocks, i = [], 0
    while i < len(lines):
        label = lines[i].strip()
        if label in POSITION_COEF_ROW:
            players, r = [], i + 2  # skip the competition-label row
            while r < len(lines) and lines[r].strip():
                players.append((r + 1, lines[r].strip().rstrip("*").strip()))
                r += 1
            blocks.append((label, players))
            i = r
        i += 1
    return blocks


def coef_cells(stats_dir, slug):
    """Return [H-cell or None] for the 4 sheet competition columns of one player."""
    cells = []
    for label, categories in COMPETITIONS:
        hits = [c for c in categories if (stats_dir / slug / f"{c}.json").exists()]
        if len(hits) > 1:
            sys.exit(f"ERROR: {slug} has both {hits} for column '{label}'. Ask the user which to use.")
        if not hits:
            cells.append(None)
            continue
        if hits[0] == "world-cup":
            cells.append(WORLD_CUP_ROW)
            continue
        data = json.loads((stats_dir / slug / f"{hits[0]}.json").read_text())
        name = (data.get("competition") or {}).get("name")
        if name not in COEF_ROW:
            sys.exit(f"ERROR: {slug}/{hits[0]}.json has competition '{name}' with no coefficient row in H61:H79")
        cells.append(COEF_ROW[name])
    return cells


def formula(row, position, cells):
    c = ["0" if h is None else f"$H${h}" for h in cells]
    n90 = [f"N({col}{row})" for col in N90_COLS]
    rating = [f"N({col}{row})" for col in RATING_COLS]
    pbase = POSITION_COEF_ROW[position]
    # standardised: 70 + sum of P * (avg - Q) / R, with Q = position mean (GK: Raya) and R = position SD (GK: Raya)
    avgs = "70+" + "+".join(
        f"(avg({';'.join(f'{col}{row}' for col in cols)})-$Q${pbase + k})/$R${pbase + k}*$P${pbase + k}"
        for k, cols in enumerate(METRIC_COLS)
    )
    rating_num = "+".join(f"{r}*{n}" for r, n in zip(rating, n90))
    rating_den = "+".join(f"ISNUMBER({col}{row})*{n}" for col, n in zip(RATING_COLS, n90))
    return (
        f"=LET(cDL;{c[0]};cDC;{c[1]};cIC;{c[2]};cWC;{c[3]};"
        f"wDL;cDL*{n90[0]};wDC;cDC*{n90[1]};wIC;cIC*{n90[2]};wWC;cWC*{n90[3]};"
        "avg;LAMBDA(dl;dc;ic;wc;(N(dl)*wDL+N(dc)*wDC+N(ic)*wIC+N(wc)*wWC)"
        "/(ISNUMBER(dl)*wDL+ISNUMBER(dc)*wDC+ISNUMBER(ic)*wIC+ISNUMBER(wc)*wWC));"
        f"{avgs}+(wDL+wDC+wIC+wWC)*$P${N90_COEF}+({rating_num})/({rating_den})*$P${RATING_COEF})"
    )


def runs(rows):
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

    blocks, summary, seen = [], [], set()
    for position, players in parse_blocks(lines):
        rows = []
        for sheet_row, name in players:
            slug = slugify(name)
            if not (stats_dir / slug).is_dir():
                sys.exit(f"ERROR: no folder player-stats/{slug} for '{name}' (row {sheet_row})")
            seen.add(slug)
            if wanted and slug not in wanted:
                continue
            cells = coef_cells(stats_dir, slug)
            rows.append((sheet_row, name, formula(sheet_row, position, cells)))
            used = ", ".join(f"{label}=H{h}" for (label, _), h in zip(COMPETITIONS, cells) if h)
            summary.append(f"{position:14} row {sheet_row:>2}  {name}: {used}")
        writes = [
            {
                "range": f"'{args.sheet}'!AG{run[0][0]}:AG{run[-1][0]}",
                "players": [r[1] for r in run],
                "formulas": [[r[2]] for r in run],
            }
            for run in runs(rows)
        ]
        blocks.append({"position": position, "writes": writes})

    missing = wanted - seen
    if missing:
        sys.exit(f"ERROR: --players names not found in column D: {sorted(missing)}")

    Path(args.out).write_text(json.dumps({"blocks": blocks}, ensure_ascii=False, indent=1))
    print("\n".join(summary))
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
