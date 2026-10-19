#!/usr/bin/env python3
"""Build the Total formulas (column AI) and the standings (columns A:B) of the Ballon d'Or 2025-26 sheet.

Two subcommands, both reading the raw output of the Sheets connector's get_values (saved as-is):
  --d      get_values of 'D1:D<last>'     (player names and position codes)
  --agai   get_values of 'AG1:AI<last>'   (Stats Points, Bonus Points, Total)
Both ranges must start at row 1, so list index i is sheet row i+1.

  totals     checks that every player row has a numeric Stats Points (AG) and Bonus Points (AH),
             then writes the plan for AI<row> = AG<row>+AH<row>.
  standings  needs the Total column to be filled (after the totals write). Sorts the players by
             Total, highest first, and writes the plan for A1:A<n> (name formulas that point at the
             player's own D cell) and B1:B<n> (static places 1..n). Stops on a missing value or a tie.

Definition: .claude/rules/ballon-dor-sheet-layout.md (Standings) and ballon-dor-scoring.md (Total).
Argument separators in sheet formulas are ";" because the sheet uses a decimal-comma locale.
"""
import argparse
import json
import re
import sys

POSITIONS = {"GK", "CB", "LB/RB/LWB/RWB", "DMC/MC", "MC/AMC", "LW/RW", "CF/SS"}


class SheetError(Exception):
    pass


def brief(problems, limit=5):
    """Keep error output short when many rows share the same problem."""
    if len(problems) <= limit:
        return "\n  ".join(problems)
    return "\n  ".join(problems[:limit] + [f"... and {len(problems) - limit} more rows"])


def load_values(path):
    """Return a list of rows (list of strings) from a saved get_values result."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return [[str(c) if c is not None else "" for c in row] for row in data["values"]]


def cell(rows, r, c):
    """Value of 0-based column c on 1-based sheet row r ('' when absent)."""
    if r - 1 < len(rows) and c < len(rows[r - 1]):
        return rows[r - 1][c].strip()
    return ""


def parse_number(text):
    """Parse a number as the connector formats it (decimal comma, optional spaces); None if not numeric."""
    t = text.replace(" ", "").replace(" ", "")
    if not re.fullmatch(r"-?\d+([.,]\d+)?", t):
        return None
    return float(t.replace(",", "."))


def find_players(d_rows):
    """Return [(row, position, display_name)] for every player row, in sheet order.

    A block is a header row (D = position code), a competition-label row, then player rows up to the
    next blank D cell. Wildcard markers ('*') are stripped from the display name.
    """
    players, r = [], 1
    while r <= len(d_rows):
        label = cell(d_rows, r, 0)
        if label in POSITIONS:
            p = r + 2
            while cell(d_rows, p, 0):
                players.append((p, label, cell(d_rows, p, 0).rstrip("*").strip()))
                p += 1
            r = p
        r += 1
    if not players:
        raise SheetError("no position blocks found in column D (is the --d range correct?)")
    return players


def read_inputs(args):
    d_rows = load_values(args.d)
    agai = load_values(args.agai)
    return find_players(d_rows), agai


def total_plan(players, agai, sheet):
    problems = []
    for row, pos, name in players:
        for col, label in ((0, "Stats Points (AG)"), (1, "Bonus Points (AH)")):
            raw = cell(agai, row, col)
            if parse_number(raw) is None:
                problems.append(f"row {row} {name}: {label} is {raw!r}, not a number")
    if problems:
        raise SheetError("cannot fill Total yet:\n  " + brief(problems))
    # one write per run of consecutive rows (blocks are separated by header/label rows)
    writes, run = [], []
    for row, _, name in players:
        if run and row != run[-1][0] + 1:
            writes.append(run)
            run = []
        run.append((row, name))
    writes.append(run)
    return [
        {
            "range": f"'{sheet}'!AI{run[0][0]}:AI{run[-1][0]}",
            "players": [n for _, n in run],
            "formulas": [[f"=AG{r}+AH{r}"] for r, _ in run],
        }
        for run in writes
    ]


def standings_plan(players, agai, sheet):
    problems, scored = [], []
    for row, pos, name in players:
        raw = cell(agai, row, 2)
        val = parse_number(raw)
        if val is None:
            problems.append(f"row {row} {name}: Total (AI) is {raw!r}, not a number")
        else:
            scored.append((val, row, name))
    if problems:
        raise SheetError("cannot write the standings yet (fill Total first):\n  " + brief(problems))
    by_total = {}
    for val, row, name in scored:
        by_total.setdefault(val, []).append(name)
    ties = {v: n for v, n in by_total.items() if len(n) > 1}
    if ties:
        lines = [f"{v:.2f}: {', '.join(n)}" for v, n in sorted(ties.items(), reverse=True)]
        raise SheetError("tied Totals (the standings need distinct values, ask the user to adjust Bonus Points):\n  "
                         + "\n  ".join(lines))
    ordered = sorted(scored, key=lambda t: -t[0])
    n = len(ordered)
    return {
        "standings": [{"place": i + 1, "row": row, "name": name, "total": val}
                      for i, (val, row, name) in enumerate(ordered)],
        "a": {"range": f"'{sheet}'!A1:A{n}",
              "formulas": [[f"=D{row}"] for _, row, _ in ordered]},
        "b": {"range": f"'{sheet}'!B1:B{n}", "values": [[i + 1] for i in range(n)]},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["totals", "standings"])
    ap.add_argument("--d", required=True, help="saved get_values result for column D, starting at row 1")
    ap.add_argument("--agai", required=True, help="saved get_values result for AG:AI, starting at row 1")
    ap.add_argument("--out", required=True, help="where to write the JSON result")
    ap.add_argument("--sheet", default="2025-26", help="tab name used in the output ranges")
    args = ap.parse_args()
    try:
        players, agai = read_inputs(args)
        if args.command == "totals":
            result = {"players": len(players), "writes": total_plan(players, agai, args.sheet)}
        else:
            result = standings_plan(players, agai, args.sheet)
    except SheetError as err:
        sys.exit(f"ERROR: {err}")
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=1)
    if args.command == "totals":
        print(f"{result['players']} players, {len(result['writes'])} Total writes")
        for w in result["writes"]:
            print(f"  {w['range']}  {', '.join(w['players'])}")
    else:
        print(f"{len(result['standings'])} places; A {result['a']['range']}, B {result['b']['range']}")
        for s in result["standings"]:
            print(f"  {s['place']:>2}. {s['name']:<24} {s['total']:>8.2f}  (D{s['row']})")


if __name__ == "__main__":
    main()
