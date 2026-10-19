# Ballon d'Or 2025-26 spreadsheet: layout

Companion rules: `ballon-dor-metrics.md` (metric formulas, N/A policy) `ballon-dor-scoring.md` (coefficients, Stats Points, Total) and `ballon-dor-bonus.md` (Bonus Points and its coefficient table). The human-written spec these rules were derived from is `_docs/google-sheet-table-transcript.md`.

## Where it lives

- Spreadsheet "e'ballon d'or", ID `10X-_E_lbtAmJ3WePbnNktKH0gefyYk9qZAdso_p4Ww8`, tab **`2025-26`** (gid 1726247710, 35 columns, 4 frozen columns). If the user supplies a different link, the link wins.
- The older tabs (2021 … 2024-25) use other layouts. Never use them as a template.
- Access goes through the `mcp__claude_ai_Google_Sheets__*` tools.
- The sheet's locale uses a decimal comma (coefficients display as `0,8`). Always write numbers as JSON numbers, never as locale-formatted strings.

## Columns

| Columns | Content |
|---|---|
| A | standings: player full name, a formula referencing column D (see Standings) |
| B | standings: place, a static number (see Standings) |
| C | unused |
| D | player name (wildcards end with `*`), or the position code on a header row |
| E–H | metric 1 |
| I–L | metric 2 |
| M–P | metric 3 |
| Q–T | metric 4 |
| U–X | metric 5 |
| Y–AB | `90s played` |
| AC–AF | `Rating (Sofascore + WhoScored)` |
| AG | Stats Points |
| AH | Bonus Points |
| AI | Total |

Inside every 4-column metric group the offsets are fixed: **+0 Dom. League, +1 Dom. Cup, +2 Int. Cup, +3 World Cup**.

## Row blocks (verified 2026-10-18)

Each position block is: a header row (D = position code, E/I/M/Q/U/Y/AC/AG/AH/AI = metric names), then a row holding the competition labels, then the player rows, then a blank row.

| Position | Header row | Player rows |
|---|---|---|
| GK | 1 | 3–4 (David Raya\*, Vozinha\*) |
| CB | 6 | 8–14 |
| LB/RB/LWB/RWB | 16 | 18–21 |
| DMC/MC | 23 | 25–29 |
| MC/AMC | 31 | 33–36 |
| LW/RW | 38 | 40–46 |
| CF/SS | 48 | 50–57 |

Rows can shift when the user edits the sheet. **Locate blocks by scanning column D for the position codes**; use the table above only as a sanity check. A player's position is the block they sit in, since the JSON files don't record position.

`*` marks a wildcard (a nominee outside the main 30). The sheet keeps it in column D and in the standings; strip it only when looking up the data folder (see below).

## Player name to data folder

Name → ASCII, lowercase, non-alphanumerics become `-`: `Pau Cubarsi` → `player-stats/pau-cubarsi/`. All 37 sheet players map this way.

## Standings (columns A:B, rows 1–37)

The final standings list all 37 players, sorted by `Total` (AI), highest first. They are written **only** when the user asks, and **only after every player's `Total` is filled in**. If any Total is blank, stop and report it.

- **Rows 1–37, columns A:B:** one row per place. Row `r` holds place `r`.
- **B (place):** a static integer, 1 for the highest Total, 2 for the next, and so on up to 37. Write it as a JSON number.
- **A (name):** a formula that references the player's own column D cell, asterisk included, for example `=D25` (a wildcard player shows as `David Raya*`). Don't type the name. The formula reference changes with each player, because the rows are in Total order, not block order.
- **Ties:** not allowed. The user sets Bonus Points so that all 37 Totals are distinct. If two Totals are equal, stop and report it.
- **Stale values:** B1:B37 currently holds numbers that are not standings (for example B8 = 8, B26 = 25, B29 = 26). Check every cell before writing, then overwrite A1:B37 with the standings. Column A is empty.
- **Scope:** the metric fill skill never writes A:B. Writing Total and the standings is the job of `/fill-ballon-dor-total-standings` (`.claude/skills/fill-ballon-dor-total-standings/`), run on request. The order is fixed when the skill runs, because each row points at one `D` cell, so run it again after Stats Points or Bonus Points change the ranking.

## Lower tables (rows 60–97)

- `D60` "* - wildcards".
- **Competition Type Coefficients:** `E` type, `F` competition, **`H61:H79` value** (19 rows). See `ballon-dor-scoring.md`.
- **Statistic Metrics Coefficients:** `K` position, `L` metric name, **`P61:P97` weight** (37 rows), and for rows 61–95 **`Q` mean** and **`R` SD** (headers `Q60` "Position avg" (average), `R60` "Typical gap"; `S61` notes that the GK rows hold Raya's own values instead).

| Rows | Metric coefficients for |
|---|---|
| 61–65 | GK metrics 1–5 |
| 66–70 | CB |
| 71–75 | LB/RB/LWB/RWB |
| 76–80 | DMC/MC |
| 81–85 | MC/AMC |
| 86–90 | LW/RW |
| 91–95 | CF/SS |
| 96 | 90s played |
| 97 | Rating |

- **Bonus Points (Achievements) Coefficients** (added 2026-10-19), to the right of the two tables above: `U60:Y60` merged header, `U` group (Team result, Individual award, Other trophy, Involvement), `V:X` merged achievement name, **`Y61:Y70` units** (10 rows). Below it, `U72:Y77` holds the involvement thresholds (information only), and `U78:Y79` is a note. See `ballon-dor-bonus.md`.

## Protected cells

Filling in metric values writes **only** to `E:AF` on player rows. Writing the standings writes **only** to `A1:B37`. Never touch:

- column D and every header or competition-label row
- `AG:AI` (Stats Points, Bonus Points, Total). `AG` is written only by the Stats Points skill and `AH` only when the user asks for a bonus update (see `ballon-dor-bonus.md`). `AI` (Total) is written only by the total-standings skill, on request.
- `H61:H79`, `P61:R97` and `U60:Y79` (the coefficient tables) and anything else in rows 58 and below
- `A:B` outside the standings task, and `A:B` in rows 38 and below

Changing any of those needs the user to ask for it explicitly.
