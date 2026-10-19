---
name: fill-ballon-dor-metrics
description: Calculate and fill in the statistic metric values (columns E:AF) for each player and competition in the Ballon d'Or 2025-26 Google Sheet, from the player-stats JSON files. Use when asked to fill in, recalculate, refresh or fix the metrics table, optionally for specific players. Never touches the coefficient tables, Stats Points, Bonus Points or Total.
argument-hint: "[spreadsheet link] [player names, comma-separated]"
allowed-tools: mcp__claude_ai_Google_Sheets__get_values Bash(python3 -I *compute_metrics.py*)
---

# Fill in Ballon d'Or 2025-26 metrics

Computes the 7 metrics × 4 competitions for every player and writes them to the `2025-26` tab. Definitions, formulas and the N/A policy are in the project rules (`ballon-dor-sheet-layout.md`, `ballon-dor-metrics.md`, `ballon-dor-scoring.md`). The script implements them; don't re-derive formulas by hand.

## Hard limits

- Write **only** to `E:AF` of player rows, and only with `update_values` using the ranges and values from the script's output.
- **Never** write to columns A, B, and D, header or label rows, `AG:AI` (Stats Points, Bonus Points, Total), `H61:H79` or `P61:R97` (coefficients), or anywhere in rows 58 and below. Don't use `update_formulas`, `batch_clear_values`, `insert_dimension` or `update_spreadsheet`.
- If the user wants any of those cells changed, that is outside this skill; ask them first.

## Steps

1. **Locate the sheet.** Use the link in `$ARGUMENTS` if there is one, otherwise the default ID in the layout rule. The tab is `2025-26`.

2. **Read the table.** `get_values` on `'2025-26'!A1:AF57`.
   - Check each block's header row: the metric names in columns E, I, M, Q, U, Y, AC must match the position table in `ballon-dor-metrics.md`. If a block differs (renamed, reordered or new metric), **stop and tell the user**. The script hard-codes the metric order.
   - Save column D to `<scratchpad>/colD.txt`: **line N = the value of D in sheet row N**, empty line for blank rows. Keep the `*` on wildcards. The response is positional, so a blank row is an empty entry and the player name is the 4th element of a row.

3. **Compute.**
   ```bash
   python3 -I ${CLAUDE_SKILL_DIR}/scripts/compute_metrics.py \
     --column-d <scratchpad>/colD.txt \
     --stats-dir /Users/vladyslavh/Public/projects/ballon-dor-2026/player-stats \
     --out <scratchpad>/metrics.json \
     [--players "Pedri,Rodri"]
   ```
   Pass `--players` only when the user named specific players (names as in the sheet). The script finds the position blocks itself, maps each name to its folder, and prints which competitions each player has, which files are missing, which cells are `N/A` because of missing data, and any warnings. An error means something needs fixing before going on (an unknown player folder, a Hakimi/Mane-style conflict between a domestic cup and the AFCON, or a name not in column D).

4. **Review.** Read the summary and the warnings. Report warnings to the user, but don't suppress cells because of them. Currently known: Vozinha's Liga Portugal 2 `Goals Prevented` is exactly `0`, probably an untracked placeholder.

5. **Write.** Read `metrics.json` and call `update_values` once per entry in `blocks[].writes[]`, with that entry's `range` and `values` copied **verbatim** (numbers as numbers, `"N/A"` as a string). Don't round, reorder or reformat.

6. **Verify.** For each written range, `get_values` it back and compare it with `metrics.json`, at minimum the first and last row of every range plus any cell you doubt. Fix and rewrite any mismatch (a transcription slip), and re-check.

7. **Report**, briefly:
   - how many players and ranges were written,
   - the warnings,
   - the notable `N/A` patterns (sparse cup files, missing competitions),
   - that `P61:R97`, Stats Points, Bonus Points and Total were left untouched.

## Things that look like bugs but aren't

- A player with no file for a competition gets `N/A` in all of that competition's cells, including `90s played` and `Rating`.
- Hakimi's and Mané's AFCON numbers go in the **Dom. Cup** column.
- `Attacking Actions, per 90` can be negative, since dispossessions are subtracted and a short cup run may have few actions.
- Percentages are fractions (0.70, not 70).
