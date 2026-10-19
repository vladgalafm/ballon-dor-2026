---
name: fill-ballon-dor-total-standings
description: Fill the Total column (AI) and the standings (columns A:B) of the Ballon d'Or 2025-26 Google Sheet. Total is the live sum of the Stats Points and Bonus Points cells; the standings list all 37 players by Total, highest first, with each name as a formula pointing at the player's column D cell. Use when asked to fill in, rebuild, refresh or re-sort Total, the standings, the ranking, the leaderboard, the final order or column A, including after Stats Points or Bonus Points changed and the order needs updating. Never touches the metrics, Stats Points, Bonus Points or the coefficient tables.
argument-hint: "[spreadsheet link]"
allowed-tools: mcp__claude_ai_Google_Sheets__get_values mcp__claude_ai_Google_Sheets__update_formulas mcp__claude_ai_Google_Sheets__update_values Bash(python3 -I *build_total_standings.py*)
---

# Fill in Ballon d'Or 2025-26 Total and standings

Two things are written, in this order:

1. **Total (`AI`)**: one live formula per player row, `=AG<row>+AH<row>`. Later edits to a Stats Points or Bonus Points input recalculate it by themselves.
2. **Standings (`A1:B37`)**: row `r` holds place `r`. Column `A` is `=D<row>`, a reference to the player's own name cell, asterisk included. Column `B` is the static place number.

The rules for both are in `.claude/rules/ballon-dor-sheet-layout.md` (Standings) and `ballon-dor-scoring.md` (Total). `scripts/build_total_standings.py` generates the formulas and checks the inputs, so don't type them by hand: a wrong row number in a name reference puts the wrong player on the podium.

## Why the standings need a re-run

The order of column `A` is fixed at the moment it is written: each row points at one particular `D` cell. That is deliberate (the names stay plain references the user can trace), but it means the standings do not re-sort themselves. Whenever Stats Points, Bonus Points or the data change enough to reorder players, run this skill again. Total itself stays live.

## Hard limits

- Write **only** to `AI` of player rows (with `update_formulas`) and to `A1:B<n>` (`update_formulas` for `A`, `update_values` for `B`), using the ranges and values from the script's output verbatim.
- **Never** write to `D`, the metric cells `E:AF`, `AG` (Stats Points), `AH` (Bonus Points), header or label rows, `H61:H79`, `P61:R97`, `U60:Y79`, or anything in rows 38 and below of `A:B`.
- If an input is empty or not a number, that's for the user to resolve (a metrics, Stats Points or bonus task). Stop and say which cells. Don't fill the gap and don't wrap anything in `IFERROR`.

## Steps

1. **Locate the sheet.** Use the link in `$ARGUMENTS` if there is one, otherwise the default ID in the layout rule. The tab is `2025-26`.

2. **Read the inputs and save them as-is.** Call `get_values` for `'2025-26'!D1:D57` and `'2025-26'!AG1:AI57` and save each result to `<scratchpad>/d.json` and `<scratchpad>/agai.json` exactly as returned. Both ranges start at row 1 so that list position matches the sheet row. If the sheet has grown past row 57, extend both ranges to cover the last player row (the script finds the blocks itself).

3. **Plan the Total.**
   ```bash
   python3 -I ${CLAUDE_SKILL_DIR}/scripts/build_total_standings.py totals \
     --d <scratchpad>/d.json --agai <scratchpad>/agai.json --out <scratchpad>/totals.json
   ```
   The script requires a numeric Stats Points and Bonus Points on every player row. An error names the rows that aren't; report them and stop.

4. **Write the Total, small block first.** Call `update_formulas` for the first entry of `writes[]` (the GK block) with its `range` and `formulas` copied verbatim, then read the range back with `get_values`. The values must be numbers equal to AG+AH. Then write the remaining entries the same way. The first block is the smoke test: it would reveal a locale or range problem before all 37 cells are touched.

5. **Re-read and plan the standings.** Call `get_values` for `'2025-26'!AG1:AI57` again (the Totals have calculated now), save it over `agai.json`, and run:
   ```bash
   python3 -I ${CLAUDE_SKILL_DIR}/scripts/build_total_standings.py standings \
     --d <scratchpad>/d.json --agai <scratchpad>/agai.json --out <scratchpad>/standings.json
   ```
   The script sorts by Total, highest first, and prints the table it will write. It stops on a non-numeric Total or on **tied Totals**, because two players cannot share a place. The user sets Bonus Points to make all 37 distinct, so report the tie and let them adjust. Totals come back from `get_values` rounded to two decimals; that is the precision the user sees, so two players equal at two decimals count as a tie.

6. **Check what you are about to overwrite.** `get_values` `'2025-26'!A1:B40`. Column `A` should be empty and `B` may hold stale numbers that are not standings. Note anything in `A` that isn't empty, and anything in rows 38–40, so the report can mention it. Then overwrite.

7. **Write the standings.** `update_formulas` for `a.range` with `a.formulas`, then `update_values` for `b.range` with `b.values`.

8. **Verify.** `get_values` `'2025-26'!A1:B37`. Column `A` must hold 37 names, in the order the script printed, and `B` the numbers 1–37. Any `#REF!`, `#ERROR!` or empty cell needs a diagnosis, not a workaround.

9. **Report**, briefly:
   - the Total ranges written and that the first-block check passed,
   - the top five and bottom three of the standings with their Totals,
   - anything unusual: stale `B` values that were replaced, a tie that stopped the run,
   - that the metrics, Stats Points, Bonus Points and coefficient tables were left untouched,
   - that the order is fixed until the skill is run again.

## Things that look like bugs but aren't

- Column `B` is typed numbers while `A` is formulas. Places are positions, so they never change. Only the player behind each position does.
- Players from the wildcard group (`*` in column D) keep the asterisk in column `A`, for example `David Raya*`. The name is copied as it is, so it always matches column `D`.
- The Total cell shows two decimals, but the cell holds the full value. Order is decided from what `get_values` returns, which is the displayed two decimals.
- A name in `A` points at a `D` cell in another position block. The standings run across all blocks, so the references jump around the sheet.
