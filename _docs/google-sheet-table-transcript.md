### This is a document which transcripts terms from the Ballon d'Or 2025-26 Google Sheet table, link to which will be provided once asked to fill-in this table or edit some values (and one asked to create Claude rule(s) and skill(s) from this document).

### Most of the terms define the specific statistic metrics of each player. All numbers for the formula calculations will be provided by JSON files from the `/player-stats` folder from this project.

## Column D
Column D contains all players' full names, statistics for each of those can be found in JSON files in `/player-stats` folder from the current project. This column also contains short form of position names where these players are playing of the football field. These positions are important, because for each position different statistics are calculated.

List of positions:
- **GK** - goalkeeper
- **CB** - central defender
- **LB/RB/LWB/RWB** - left or right full-back or wing-back
- **DMC/MC** - midfielder who more often plays defensively, closer to back lines
- **MC/AMC** - midfielder who more often plays in attack, closer to forward lines
- **LW/RW** - left or right winger, attacking player
- **CF/SS** - central forward or second striker

"wildcard" term means player is not from the main list of 30 nominated players.

## Competition types
Per each statistic field there're 4 columns defining to which competition the statistic number belongs.

Competition type column names:
- **Dom. League** - club-level domestic league (LaLiga, Ligue 1, etc.), statistics are in `domestic-league.json` files
- **Dom. Cup** - club-level domestic cup (EFL Cup, DFB Pokal, etc.), statistics are in `domestic-cup.json` files
    - for Achraf Hakimi and Sadio Mane this column will be used for their national teams statistics from Africa Cup of Nations cup (`africa-cup-of-nations.json`)
- **Int. Cup** - club-level international cup (for example, UEFA Champions League), statistics are in `international-cup.json` files
- **World Cup** - national team statistics from the World Cup 2026 (`world-cup.json`)

## Statistic Metrics
Per each position there are 5 different (some are shared between positions) statistic metrics that are required to evaluate each player efficency. In addition, there are 2 more statistic metrics shared between all positions.
All statistics data required for calculations there is placed in `statistics` object in each JSON file.
Values for the percentage stats are expected to be in range 0..1, rest are regular double numbers (all >= 0 except Goals Prevented metric, which might be negative).

- **90s played**
    - Means how many 90 minutes has player spent on the field per competition in total. More objective number than number of times player appeared on the field since they not always spend exactly 90 minutes on the field.
    - Formula: `minutesPlayed / 90`

- **Rating (Sofascore + WhoScored)**
    - An average score between Sofascore and WhoScored stats agregators.
    - Formula: `(rating + whoScoredRating) / 2`

- **Saves, %**
    - Percentage of shots that have been stopped from going into the goal.
    - Formula: `savesPercentage / 100`

- **Goals Against, per 90**
    - Means how many goals have been conceeded per each 90 minutes
    - Formula: `goalsConceded / (minutesPlayed / 90)`

- **Goals Prevented, +/-**
    - This statistic measures a goalkeeper's effectiveness in preventing goals. It's based on the ratio of goals conceded to the expected number of goals based on the quality of shots (xGOT). A negative score means the goalkeeper conceded more goals than expected.
    - Defined by: `goalsPrevented`

- **Clean Sheets, %**
    - Percentage of matches ended up conceeding zero goals.
    - Formula: `cleanSheet / matchesStarted`

- **Accurate Long Balls, %**
    - Percentage of accurate long passes.
    - Formula: `accurateLongBalls / totalLongBalls` (or `accurateLongBallsPercentage / 100` if any of previous two fields is missing)

- **Tackles Won, %**
    - Percentage of successful attempts of tackling the ball away from the opponent.
    - Formula: `tacklesWon / tackles` (or `tacklesWonPercentage / 100` if any of previous two fields is missing)

- **Aerial Duels Won, %**
    - Percentage of duels won in the air.
    - Formula: `aerialDuelsWonPercentage / 100`

- **Defensive Actions, per 90**
    - Actions in defense completed successfully, per 90 minutes. Including tackles, interceptions, blocked shots, and clearances. Subtracting fouls committed and own goals.
    - Formula: `(tacklesWon + interceptions + blockedShots + clearances - fouls - ownGoals) / (minutesPlayed / 90)`

- **Accurate Passes, %**
    - Percentage of accurate short passes.
    - Formula: `accuratePasses / totalPasses` (or `accuratePassesPercentage / 100` if any of previous two fields is missing)

- **Ground Duels Won, %**
    - Percentage of duels won on the ground.
    - Formula: `groundDuelsWonPercentage / 100`

- **Accurate Final Third Passes, per 90**
    - Accurate passes in the final 1/3 of the field (final ~30 meters) per 90 minutes.
    - Formula: `accurateFinalThirdPasses / (minutesPlayed / 90)`

- **Attacking Actions, per 90**
    - Actions in attack completed successfully, per 90 minutes. Including goals, assists, shots on target (not including penalty kicks), successful dribble attempts, key passes and accurate crosses - but also subtracting number of times player lost control of the ball after being tackled by an opposing player (dispossessed).
    - Formula: `(goals + assists + (shotsOnTarget - penaltyGoals - attemptPenaltyTarget) + successfulDribbles + keyPasses + accurateCrosses - dispossessed) / (minutesPlayed / 90)`

- **xG + xA, per 90**
    - Sum of expected goals and assists per 90 minutes.
    - Formula: `(expectedGoals + expectedAssists) / (minutesPlayed / 90)`

- **Press Resistance x Ground Engagement Win Rate, %**
    - Defines how much midfielder controlls the ball of the field, essential metric for midfielders.
    - Press Resistance % = Touches / (Touches + Dispossessed)
    - Ground Engagement Win Rate % = Ground Duels Won / (Ground Duels Contested + Dribbled Past)
    - Formula: `(touches / (touches + dispossessed)) * (groundDuelsWon / ((groundDuelsWon / (groundDuelsWonPercentage / 100)) + dribbledPast))`

- **Goals, per 90**
    - Number of goals per 90 minutes.
    - Formula: `goals / (minutesPlayed / 90)`

- **xA, per 90**
    - Expected assists per 90 minutes.
    - Formula: `expectedAssists / (minutesPlayed / 90)`

- **Goals, per Shot**
    - Number of goals per shot (any shot, on or off target). Metric for goal convertion.
    - Formula: `goals / totalShots`

- **Dribbles Success, %**
    - Percentage of how many times player managed to successfully dribble ball past the opponent.
    - Formula: `successfulDribblesPercentage / 100`

### Filling in metrics calculated data
If there's not enough data to calculate specific metric or player hasn't participated in specific competition type, related cell should be filled with "N/A".

## Competition Type Coefficients
Coefficients for each competition, needed to give more value for stats from more important competitions. These coefficients are used in **Stats Points** formula (to be defined later), and these coefficients should be used in this formula as references to values in `H61:H79` cells, so we can easily calibrate formulas by changing coefficients in one place.

## Statistic Metrics Coefficients
Coefficients for each statistics metric (5 for each position, 2 shared). These coefficients are used in **Stats Points** formulas (to be defined later), and needed to calibrate formula for each position. Since metrics per each position are different and we need to compare all players at once, we need different coeffitient value per each metric to evaluate all players and find trully best ones who deserve the win a Ballon d'Or.
These coefficients should be used in **Stats Points** formula as references to values in `P61:P97` cells, so we can easily calibrate formula by changing coefficients in one place.
Values for coefficients in `P61:P97` cells need to be determined by Claude after all Statistics Metrics are calculated and filled in the table.
Those players, who have played more competitions and have participated in important competitions like World Cup or UEFA Champions League, should be rewarded, that's why we are using such metrics like 90 minutes played and competition type coefficients.

## Stats Points
This should be calculated for each player by the formula that would look like this:
`(metric1 * coef1) + (metric2 * coef2) + (metric3 * coef3) + (metric4 * coef4) + (metric5 * coef5) + (metricNinetyMinutes * coefNinetyMinutes) + (metricRating * coefRating)`

Breakdown for each part in the formula:
1. `metric1..metric5` are metrics specific to each position, calculated by finding out the average value between all 4 (or less) competition types with the consideration of coefficients used for each competition type. This average value calculation would look like this:
`(domLeagueValue * domLeagueCoef + domCupValue * domCupCoef + intCupValue * intCupCoef + worldCupValue * worlCupCoef) / (domLeagueCoef + domCupCoef + intCupCoef + worldCupCoef)`.
    - If data for any of the competition type is not available for player, or player did not participate in that competition type (cell marked as N/A), this competion should not be included in the formula. For example, this is how formula would look like if player hasn't participated in Domestic Cup and World Cup:
    `(domLeagueValue * domLeagueCoef + intCupValue * intCupCoef) / (domLeagueCoef + intCupCoef)`
2. **90s played** (`metricNinetyMinutes`) is important to reward players who played more time and played in more important competitions. However, this part of the formula should not prevail first 5 metrics too hard, those 5 should remain more important. Formula for this metric should be like this:
`(domLeagueNinetyMinutes * domLeagueCoef + domCupNinetyMinutes * domCupCoef + intCupNinetyMinutes * intCupCoef + wordCupNinetyMinutes * worldCupCoef)`
    - If data for any of the competition type is not available for player, or player did not participate in that competition type (cell marked as N/A), this competion should not be included in the formula. For example, this is how formula would look like if player hasn't participated in Domestic Cup and World Cup:
    `(domLeagueNinetyMinutes * domLeagueCoef + intCupNinetyMinutes * intCupCoef)`
3. **Rating (Sofascore + WhoScored)** (`metricRating`), displays the average rating for the player, however, this should be less important, since attacking players usually have higher ratings than defending players as attacking returns are highly rewarded in ratings compared to defending returns. Formula for this metric should display true average, so it depends on 90s minutes played, and looks like this:
`(domLeagueRating * domLeagueNinetyMinutes + domCupRating * domCupNinetyMinutes + intCupRating * intCupNinetyMinutes + worldCupRating * worldCupNinetyMinutes) / (domLeagueNinetyMinutes + domCupNinetyMinutes + intCupNinetyMinutes + worldCupNinetyMinutes)`
    - If data for any of the competition type is not available for player, or player did not participate in that competition type (cell marked as N/A), this competion should not be included in the formula. For example, this is how formula would look like if player hasn't participated in Domestic Cup and World Cup:
    `(domLeagueRating * domLeagueNinetyMinutes + intCupRating * intCupNinetyMinutes) / (domLeagueNinetyMinutes + intCupNinetyMinutes)`

## Bonus Points
Will be determined later by myself. These are bonus points for winning competitions, scoring most goals, being named MVP of the season, and other achievements.

*(Added 2026-10-19: the bonus scale and each player's achievements are now in `bonus-points-achievements.md`, and the sheet implementation is described in `.claude/rules/ballon-dor-bonus.md`.)*

## Total
A sum of **Stats Points** and **Bonus Points**, determines the overall rating of players (more points - higher rating).
