# Ballon d'Or 2025-26: metrics and formulas

Layout is in `ballon-dor-sheet-layout.md`, coefficients and Stats Points in `ballon-dor-scoring.md`. Source data: `player-stats/<slug>/<category>.json`, field `statistics`. Competitions are never summed here. **Each cell is computed from one file.**

## Competition columns and source files

| Sheet column | File | Notes |
|---|---|---|
| Dom. League | `domestic-league.json` | all 37 players |
| Dom. Cup | `domestic-cup.json` | **Achraf Hakimi and Sadio Mane use `africa-cup-of-nations.json` here**; neither has a domestic-cup file. If a player ever has both, stop and ask. |
| Int. Cup | `international-cup.json` | mostly UEFA Champions League |
| World Cup | `world-cup.json` | 2026 World Cup, national team |

## Value conventions

- Percentage metrics are fractions in **0..1**. The JSON `*Percentage` fields are 0..100, so divide by 100.
- Everything else is a plain number. Only `Goals Prevented, +/-`, `Defensive Actions, per 90`, and `Attacking Actions, per 90` can be negative.
- Write the literal string **`N/A`** when:
  - the player has no file for that competition (no participation is not zero), or
  - a field the formula needs is **missing** from `statistics` (the schema is uneven; keys are absent, not null), or
  - a denominator is zero.
- A metric that is `N/A` in one competition doesn't affect the other competitions.
- `90s played` is also `N/A` when there is no file.
- Ten sparse `domestic-cup.json` files (Copa del Rey / King's Cup) have only goals, assists, minutes and rating, so most of their metrics are `N/A`.

## Metrics per position

Each block has these five metrics (in column order) plus the two shared ones, `90s played` and `Rating (Sofascore + WhoScored)`.

| Position | Metric 1 | Metric 2 | Metric 3 | Metric 4 | Metric 5 |
|---|---|---|---|---|---|
| GK | Saves, % | Goals Against, per 90 | Goals Prevented, +/- | Clean Sheets, % | Accurate Long Balls, % |
| CB | Tackles Won, % | Aerial Duels Won, % | Defensive Actions, per 90 | Accurate Passes, % | Accurate Long Balls, % |
| LB/RB/LWB/RWB | Ground Duels Won, % | Defensive Actions, per 90 | Accurate Final Third Passes, per 90 | Attacking Actions, per 90 | xG + xA, per 90 |
| DMC/MC | Defensive Actions, per 90 | Press Resistance x Ground Engagement Win Rate, % | Accurate Passes, % | Accurate Final Third Passes, per 90 | Attacking Actions, per 90 |
| MC/AMC | Goals, per 90 | xA, per 90 | Press Resistance x Ground Engagement Win Rate, % | Accurate Final Third Passes, per 90 | Attacking Actions, per 90 |
| LW/RW | Goals, per 90 | Goals, per Shot | xA, per 90 | Dribbles Success, % | Attacking Actions, per 90 |
| CF/SS | Goals, per 90 | Goals, per Shot | xA, per 90 | Aerial Duels Won, % | Attacking Actions, per 90 |

## Formulas

`m90 = minutesPlayed / 90`. Every field named below must exist in the file, or the result is `N/A`.

| Metric | Formula |
|---|---|
| 90s played | `minutesPlayed / 90` |
| Rating (Sofascore + WhoScored) | `(rating + whoScoredRating) / 2` |
| Saves, % | `savesPercentage / 100` |
| Goals Against, per 90 | `goalsConceded / m90` |
| Goals Prevented, +/- | `goalsPrevented` (as is) |
| Clean Sheets, % | `cleanSheet / matchesStarted` |
| Accurate Long Balls, % | `accurateLongBalls / totalLongBalls`; if either is missing, `accurateLongBallsPercentage / 100` |
| Tackles Won, % | `tacklesWon / tackles`; if either is missing, `tacklesWonPercentage / 100` |
| Accurate Passes, % | `accuratePasses / totalPasses`; if either is missing, `accuratePassesPercentage / 100` |
| Aerial Duels Won, % | `aerialDuelsWonPercentage / 100` |
| Ground Duels Won, % | `groundDuelsWonPercentage / 100` |
| Dribbles Success, % | `successfulDribblesPercentage / 100` |
| Defensive Actions, per 90 | `(tacklesWon + interceptions + blockedShots + clearances - fouls - ownGoals) / m90` |
| Accurate Final Third Passes, per 90 | `accurateFinalThirdPasses / m90` |
| Attacking Actions, per 90 | `(goals + assists + (shotsOnTarget - penaltyGoals - attemptPenaltyTarget) + successfulDribbles + keyPasses + accurateCrosses - dispossessed) / m90` |
| xG + xA, per 90 | `(expectedGoals + expectedAssists) / m90` (`N/A` if either is missing) |
| xA, per 90 | `expectedAssists / m90` |
| Goals, per 90 | `goals / m90` |
| Goals, per Shot | `goals / totalShots` |
| Press Resistance x Ground Engagement Win Rate, % | `(touches / (touches + dispossessed)) * (groundDuelsWon / ((groundDuelsWon / (groundDuelsWonPercentage / 100)) + dribbledPast))` |

Press Resistance = `touches / (touches + dispossessed)`. Ground Engagement Win Rate = `groundDuelsWon / (groundDuelsContested + dribbledPast)`. The files carry no contested-duels field, so contested is derived as `groundDuelsWon / (groundDuelsWonPercentage / 100)`. `N/A` if `groundDuelsWonPercentage` is 0.

## Definitions

- **Defensive Actions:** successful tackles, interceptions, blocked shots and clearances, minus fouls committed and own goals.
- **Attacking Actions:** goals, assists, shots on target (excluding penalty kicks), successful dribbles, key passes and accurate crosses, minus times dispossessed.
- **Goals Prevented:** how the goalkeeper's conceded goals compare with the xGOT of the shots faced. Negative means more goals conceded than expected.
- **Accurate Final Third Passes:** accurate passes in the final ~30 m.
- **Press Resistance x Ground Engagement Win Rate:** how much a midfielder controls the ball on the ground; the key midfielder metric.
- **Position codes:**
  - GK: goalkeeper
  - CB: central defender
  - LB/RB/LWB/RWB: full-back or wing-back
  - DMC/MC: midfielder who plays more defensively
  - MC/AMC: midfielder who plays more in attack
  - LW/RW: winger
  - CF/SS: centre forward or second striker

## Known data quirks

- Vozinha's `domestic-league.json` has `goalsPrevented` of exactly `0`, which is probably an untracked placeholder in Liga Portugal 2. It is written as the spec says (`0`) but flagged.
- Five outfield players (Olmo, Dimarco, Zabarnyi, Oyarzabal, Pedri) have `savesPercentage: 0` in their files because of the richer schema. It is only read for the GK block, so it never reaches the sheet.
