---
name: fill-ballon-dor-stats-points
description: Write the Stats Points formulas (column AG) for every player in the Ballon d'Or 2025-26 Google Sheet, using the already-filled metrics (E:AF) and the prepared coefficient tables (H61:H79, P61:R97). Use when asked to fill in, rebuild, refresh or fix Stats Points / the AG column / player scores, optionally for specific players, or after metrics or coefficients were changed and the scores need re-applying. Never touches metrics, coefficients, Bonus Points, Total or the standings.
argument-hint: "[spreadsheet link] [player names, comma-separated]"
allowed-tools: mcp__claude_ai_Google_Sheets__get_values mcp__claude_ai_Google_Sheets__update_formulas Bash(python3 -I *build_stats_points.py*)
---

# Fill in Ballon d'Or 2025-26 Stats Points

Writes one live formula per player into column AG of the `2025-26` tab. The formula reads that row's metric cells and the coefficient tables, so later edits to a metric or a coefficient recalculate by themselves. This skill only has to run again when the *shape* of a row changes: a new player, a moved block, or a different set of competitions.

The scoring model (minutes-weighted averages standardised per position, 90s played as a weighted sum, rating weighted by 90s) is in `.claude/rules/ballon-dor-scoring.md`; the layout is in `ballon-dor-sheet-layout.md`. `scripts/build_stats_points.py` generates the formulas, so don't write them by hand. Per-cell hand-typing is how a wrong `$P$` row or `$H$` cell slips in.

## Hard limits

- Write **only** to `AG` of player rows, with `update_formulas`, using the ranges and formulas from the script's output verbatim.
- **Never** write to the metric cells `E:AF`, columns A, B and D, header or label rows, `AH` (Bonus Points), `AI` (Total), `H61:H79`, `P61:R97`, or anything in rows 58 and below. Bonus Points and Total are the user's.
- If the coefficients are empty or wrong, that's a calibration task for the user to request, not something to fix here.

## Steps

1. **Locate the sheet.** Use the link in `$ARGUMENTS` if there is one, otherwise the default ID in the layout rule. The tab is `2025-26`.

2. **Check the preconditions.** The formulas silently produce nonsense if the inputs aren't ready, so check before writing:
   - `get_values` `'2025-26'!A1:AG57`. Every block's `AG` header must be `Stats Points`. Every player's `Y:AB` (90s played) and `AC:AF` (rating) cells must be a number or `N/A`, never blank. A blank means the metrics fill hasn't run for that player; stop and tell the user.
   - `get_values` `'2025-26'!E61:R97`. `H61:H79`, `P61:P97` and `Q61:R95` (position mean and SD) must all be numbers, and no `R` may be 0 (the coefficient labels in `F61:F79` should match the competition order in the scoring rule). If any are empty, stop and tell the user. Don't invent coefficients.
   - Save column D to `<scratchpad>/colD.txt`: **line N = the value of D in sheet row N**, empty line for blank rows, `*` kept on wildcards.

3. **Generate.**
   ```bash
   python3 -I ${CLAUDE_SKILL_DIR}/scripts/build_stats_points.py \
     --column-d <scratchpad>/colD.txt \
     --stats-dir /Users/vladyslavh/Public/projects/ballon-dor-2026/player-stats \
     --out <scratchpad>/stats_points.json \
     [--players "Pedri,Rodri"]
   ```
   Pass `--players` only when the user named specific players (names as in the sheet). The script finds the position blocks, then, for each player, lists which coefficient cell (`H61:H79`) applies to each competition column, taken from the `competition.name` in that player's JSON files. A competition with no file gets `0`, which drops it from every average and sum. An error means something needs fixing first: an unknown player folder, a competition name with no coefficient row, or a player with both a domestic cup and the AFCON.

4. **Sanity-read the summary.** The printed competition mapping should agree with the data layout in `CLAUDE.md`. For example, PSG players have no Dom. Cup, Hakimi and Mané use `H75` (AFCON) in the Dom. Cup column, and Messi's Int. Cup is `H77` (CONCACAF). A surprise means the data or the rules changed, so report it instead of writing.

5. **Write, small block first.** Call `update_formulas` for the first entry of `blocks[0].writes[]` (the GK block) with its `range` and `formulas` copied verbatim, and read the range back with `get_values`. The values must be numbers. Then write the remaining entries the same way. The first write is a smoke test: the sheet's locale is decimal-comma, so formulas use `;` separators (`,` gives `#ERROR!`), and a locale change would show up here before 37 cells are affected.

6. **Verify.** `get_values` `'2025-26'!AG1:AG57`. Every player row must hold a number. Any `#DIV/0!`, `#ERROR!`, `#REF!` or `#N/A` needs a diagnosis. The usual cause is a player whose metric cell is `N/A` in *every* competition, which empties a weighted average's denominator. Report the cell, and don't wrap the formula in `IFERROR` to hide it.

7. **Report**, briefly:
   - how many rows were written and the ranges,
   - any errors found in step 6,
   - the five highest and five lowest Stats Points, and the user's fairness checks from memory (`stats-points-calibration`): Pacho above Zabarnyi, Kane above Dembélé, Yamal clearly above Kvaratskhelia, and no goalkeeper at the top. State pass or fail for each. Don't change anything because of a failure; a failed check is a signal to recalibrate, which is the user's call,
   - that metrics, coefficients, Bonus Points, Total and the standings were left untouched.

## What the formula does, in one paragraph

For each of the five position metrics, a competition-and-minutes weighted average: weight = competition coefficient × that competition's 90s played, and a competition whose cell is `N/A` is excluded from both numerator and denominator (that's why every cell goes through `N()` and `ISNUMBER()`). Each average is standardised against the player's position, `(avg − Q) / R` (Q = position mean, R = position SD), multiplied by its `P` weight and added to a baseline of `70`. Then comes the sum of `90s × competition coefficient`, times `P96`, and finally the rating averaged by 90s only (no competition weight) times `P97`. All of this is inside one `LET`, so the four competition coefficients are visible at the top of every cell.

## Things that look like bugs but aren't

- A cell shows `0` for a competition coefficient (`cDC;0`) when the player has no file for it. That's intentional, not a missing reference.
- Goals Against, per 90 has a negative `P62`, so a Goals Against average above the reference *subtracts* from a goalkeeper's points. Lower is better.
- Every outfield five-metric part starts at `70` and moves by `P` points per SD above or below the position mean, so a metric can contribute a negative amount. That is a below-average value, not an error. For GK, `Q = R =` Raya's value, which makes Raya exactly 70.
- Stats Points values change when the user edits a coefficient or a metric. They're live formulas, not snapshots.
