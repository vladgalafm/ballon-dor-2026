# Ballon d'Or 2025-26: Bonus Points (column AH)

Cell locations are in `ballon-dor-sheet-layout.md`, Stats Points and the other coefficients in `ballon-dor-scoring.md`. The research behind the bonus values (every player's achievements, sources, open issues) is `_docs/bonus-points-achievements.md`. That document is the source of truth for **which achievement each player has**. The sheet only holds the points arithmetic.

Claude writes Bonus Points only when the user asks. It never writes Total (`AI`) or the standings as part of a bonus task.

## Bonus Points (Achievements) Coefficients table (`U60:Y70`, plus notes in `U72:Y79`)

Written 2026-10-19, next to the two other coefficient tables. Values as of that date; read the live sheet for current numbers, since the user recalibrates them. Formulas must **reference these cells**, never copy the numbers.

| Cell | Meaning | Units |
|---|---|---|
| `Y61` | Winner (trophy) | 8 |
| `Y62` | Finalist | 3 |
| `Y63` | Semi-finalist | 1 |
| `Y64` | Player of the tournament / season | 5 |
| `Y65` | Top scorer | 3 |
| `Y66` | Top assister (any competition, including the domestic league) | 1.5 |
| `Y67` | Golden Glove / best GK or defender | 3 |
| `Y68` | Team of the tournament / season | 1 |
| `Y69` | Super cup / extra trophy, flat points | 1 |
| `Y70` | Half involvement multiplier (full = 1) | 0.5 |

`U72:Y77` lists the involvement thresholds. They are information only, and no formula reads them.

## Formula shape

```
Bonus = Σ units × H[competition]            (individual awards, and team results at full involvement)
      + Σ units × H[competition] × Y70      (team results at half involvement)
      + n × Y69                             (extra trophies won and played in the final)
```

`H[competition]` is the Competition Type Coefficient (`H61:H79`): PL `H61`, LaLiga `H62`, Bundesliga `H63`, Serie A `H64`, Ligue 1 `H65`, MLS `H66`, Saudi league `H67`, EFL Cup `H69`, Copa del Rey `H70`, DFB Pokal `H71`, Coppa Italia `H72`, AFCON `H75`, Champions League `H76`, AFC Champions League Two `H78`, World Cup `H79`.

Each AH cell is a plain sum of terms such as `$Y$61*$H$76` (winner of the Champions League) or `$Y$61*$H$65*$Y$70` (champion of Ligue 1 at half involvement). A trophy count is the only literal number (`3*$Y$69`). There are no function calls, so the `;` separator rule does not apply. Example, David Raya (Premier League champion, Champions League finalist, Golden Glove, two Teams of the Season): `=$Y$61*$H$61+$Y$62*$H$76+$Y$67*$H$61+$Y$68*$H$76+$Y$68*$H$61` = 18.

## What counts (decided with the user on 2026-10-19)

- **Team results** (winner, finalist, semi-finalist) are scaled by involvement, from the minutes in the sheet's data. Thresholds are applied **strictly, with no rounding up**:
  - league: full ≥ 40% of available minutes (3,420 for 38 games, 3,060 for 34), half 20–40%;
  - Champions League: full ≥ 500 min, half 250–499;
  - World Cup and AFCON: full ≥ 250, half 125–249;
  - domestic and other cups: full ≥ 200, half 100–199;
  - below half: no points.
- A league title counts for the champion only. Individual awards need no involvement check.
- **AFCON 2025:** the final is disputed (Senegal won on the pitch, CAF later awarded it to Morocco), so both teams are scored as **finalists**.
- **Shared awards** (ties for top assister) give full points to each player. One "Player of the Season" per competition counts: the league's own official award. PFA, FWA and media picks are not counted.
- **Teams of the season** use these sources: UEFA Champions League Team of the Season, the World Cup Team of the Tournament template, CAF AFCON Best XI, UNFP Ligue 1, PFA Premier League, the Wikipedia La Liga Awards page (the 11 listed), the EA Sports Bundesliga selection and the Wikipedia Serie A Team of the Year.
- **Super cups and extra trophies** (UEFA Super Cup, Intercontinental Cup, Trophée des Champions, Supercopa de España, DFL-Supercup, FA Cup): a flat `Y69` point each, for **winners only**, and only if the player took part in the final match.
- **Messi's MLS items** are provisional: MLS 2026 was still running on 2026-10-19 (top scorer and tied top assister). His 2025 MLS MVP, Best XI and MLS Cup are recorded as extras with no points.

## Updating

- To change a player's bonus (a new award, a corrected involvement level), edit the player's `AH` formula by adding, removing or editing one term, then update `_docs/bonus-points-achievements.md` so the two agree. Test the change on one cell and read it back.
- To recalibrate, change the unit cells (`Y61:Y70`). All bonuses recalculate.
- Changing `H61:H79` changes both Stats Points weighting and bonus weighting.
- After any change, re-read `AH` for all 37 players. Every value must match the document's per-player total.
- At the end of MLS 2026 (December), re-check Messi's formula (top scorer, top assister) against the final table.
