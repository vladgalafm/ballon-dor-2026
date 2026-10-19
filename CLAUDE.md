# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A mathematical model that ranks the Ballon d'Or 2026 nominees from their 2025/26 season statistics. The input data is in `player-stats/`. The only code is the three skill scripts: the metric calculator in `.claude/skills/fill-ballon-dor-metrics/scripts/`, the Stats Points formula builder in `.claude/skills/fill-ballon-dor-stats-points/scripts/` and the Total and standings builder in `.claude/skills/fill-ballon-dor-total-standings/scripts/`. There is no package manifest, build, lint or test setup, and no git repo yet. Don't assume a toolchain beyond that; when adding one, document its commands here.

## Google Sheet tooling

The ranking lives in the "2025-26" tab of a Google Sheet. Its structure, metric formulas and scoring terms are in `.claude/rules/ballon-dor-*.md` (derived from `google-sheet-table-transcript.md`).

- The `/fill-ballon-dor-metrics` skill (`.claude/skills/fill-ballon-dor-metrics/`) fills the metric cells `E:AF` from `player-stats/`. It never writes to the coefficient tables, Stats Points, Bonus Points or Total.
- The `/fill-ballon-dor-stats-points` skill (`.claude/skills/fill-ballon-dor-stats-points/`) writes the Stats Points formulas in column `AG` once the metrics and both coefficient tables are filled. It never writes to the metrics, coefficients, Bonus Points or Total.
- Bonus Points (column `AH`) have no skill. They are live formulas over the Bonus Points (Achievements) Coefficients table in `U60:Y70` and the competition coefficients `H61:H79`. The scale, the involvement rule and the update procedure are in `.claude/rules/ballon-dor-bonus.md`, and each player's achievements and sources are in `_docs/bonus-points-achievements.md`. The user decides when to change them.
- The `/fill-ballon-dor-total-standings` skill (`.claude/skills/fill-ballon-dor-total-standings/`) writes Total (`AI`, `=AG+AH`) and the standings in `A1:B37` (players sorted by Total, names as references to column `D`). It needs Stats Points and Bonus Points filled and stops on tied Totals. It never writes anything else.

## Data layout

`player-stats/<player-slug>/<category>.json` — 37 players (35 outfield plus two goalkeepers, David Raya and Vozinha), 129 files in total. One file per player per competition category:

| File | Contents | Coverage |
|---|---|---|
| `domestic-league.json` | Club league (Premier League, LaLiga, Ligue 1, Bundesliga, Serie A, Saudi Pro League, MLS, and Liga Portugal 2 for Vozinha) | all 37 |
| `domestic-cup.json` | Domestic cup (EFL Cup, DFB Pokal, Copa del Rey, King's Cup, Coppa Italia, Leagues Cup) | 24 — absent for all ten PSG players plus Mané, Raya and Vozinha |
| `international-cup.json` | Continental club competition, almost all UEFA Champions League (one CONCACAF Champions Cup, one AFC Champions League Two) | 33 — missing for Bruno Fernandes, Quiñones, Oyarzabal, Vozinha |
| `world-cup.json` | 2026 World Cup, national team | 33 — missing for Kvaratskhelia, Raya, Dimarco, Zabarnyi |
| `africa-cup-of-nations.json` | AFCON, national team | only Mané and Hakimi |

The category is encoded **only in the filename**. A missing file means the player did not play in that competition, which is a zero contribution and not a missing value.

### JSON shape (every file)

- `statistics` — flat object of raw season totals for that competition, plus a few derived fields. `statistics.type` is always `"overall"` and `statistics.id` is an upstream internal ID. Ignore both.
- `seasonRatingBreakdown` — `shotValue`, `passValue`, `dribbleValue`, `defensiveValue`: components of the provider's rating.
- `team` — club or national team. It is mostly metadata (colours, `fieldTranslations`, `userCount`). Use `team.name`, `team.national` and `team.ranking`. Note that `ranking` appears only on some national teams.
- `competition.name` — present in every file **except `world-cup.json`**.

## Gotchas when aggregating or modelling

- **Uneven schema, not nulls.** There are no `null` values, but keys are absent when the provider didn't track them. Of the 140 distinct `statistics` keys:
  - 10 `domestic-cup.json` files (Copa del Rey / King's Cup entries for Ferran Torres, Bellingham, Quiñones, Mbappé, Yamal, Cubarsí, Vinícius, Olmo, Oyarzabal, Pedri) are "sparse", with only about 19–24 keys. They have goals, assists, minutes and rating, but no shots, passes, dribbles or duels.
  - `expectedGoals`, `expectedAssists` and `expectedGoalInvolvements` are in about 100 files.
  - `kilometersCovered`, `numberOfSprints` and `topSpeed` are in about 103 files, and `kilometersCoveredPer90` and `numberOfSprintsPer90` in about 70. There is no `topSpeedPer90`.
  - The non-sparse files of the seven newest players (Olmo, Raya, Dimarco, Zabarnyi, Oyarzabal, Pedri, Vozinha) use a richer schema of about 134–139 keys, versus about 111–119 for the other players. The extra keys exist only for them: `touchesInOppBox`, `unsuccessfulTouches`, `cornersTaken`, `defensiveContributions`, `expectedGoalsOnTarget`, `expectedGoalsConceded`, `goalInvolvements`, `metersCovered*` and the running/sprinting/walking percentages. Don't use them for a cross-player comparison, since the other 30 players lack them.
  - Use `.get(key)` with an explicit missing-data policy. Never index directly.
- **Don't sum ratios.** To combine competitions:
  - `rating` is a mean. Re-weight it with `totalRating / countRating`.
  - `*Percentage`, `*Per90`, `scoringFrequency`, `penaltyConversion` and `goalConversionPercentage` must be recomputed from the underlying counts.
  - `topSpeed` aggregates as a max.
  - Raw counts (goals, assists, minutes, `appearances`) are safe to sum.
- **Minutes vs. appearances.** Competitions differ widely in sample size. A World Cup run is 4–8 appearances, versus about 30 for a league. Normalise per 90 using `minutesPlayed` rather than comparing totals blindly.
- **Position is not recorded.** Defender-only fields (`clearances`, `blockedShots`, `cleanSheet`) and goalkeeper-only fields (`saves`, `punches`, `highClaims`) exist in the 119 full-schema files, usually as zeros. Role-specific weighting needs a position mapping that you supply yourself.
- **Goalkeepers are in the set.** David Raya (Arsenal) and Vozinha (Chaves, Cabo Verde) are the only players with non-zero `saves`, `punches` and `highClaims`, in 4 files. `goalsPrevented` appears only in 3 of those files. `cleanSheet` and `goalsConceded` are team-level and non-zero for outfield players too, so they can't identify a goalkeeper, but `saves > 0` can. Goals, assists and xG are near zero for goalkeepers, so a model built on attacking output will rank them last unless it uses a separate goalkeeper formula.
- **Mixed competition strength.** The set spans leagues of very different levels (MLS, the Saudi Pro League and Vozinha's second-tier Liga Portugal 2 next to the Premier League and LaLiga). Any competition weighting is a modelling choice, so state it explicitly.
