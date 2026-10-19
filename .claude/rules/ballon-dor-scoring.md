# Ballon d'Or 2025-26: coefficients and scoring

The metric values themselves are defined in `ballon-dor-metrics.md`, and cell locations in `ballon-dor-sheet-layout.md`. **Everything in this file is outside the metric-fill skill.** Only touch these cells when the user asks.

## Competition Type Coefficients (`H61:H79`)

Values as of 2026-10-18. Read the live sheet for the current numbers, since the user recalibrates them. Formulas must **reference these cells**, not copy the numbers, so calibration happens in one place.

| Cell | Competition | JSON `competition.name` | Value |
|---|---|---|---|
| H61 | English Premier League | `Premier League` | 1 |
| H62 | Spanish LaLiga | `LaLiga` | 1 |
| H63 | German Bundesliga | `Bundesliga` | 1 |
| H64 | Italian Serie A | `Serie A` | 1 |
| H65 | French Ligue 1 | `Ligue 1` | 1 |
| H66 | US MLS | `Major League Soccer` | 0.8 |
| H67 | Saudi Pro League | `Saudi Pro League` | 0.7 |
| H68 | Liga Portugal 2 | `Liga Portugal 2` | 0.6 |
| H69 | EFL Cup | `EFL Cup` | 0.5 |
| H70 | Copa del Rey | `Copa del Rey` | 0.5 |
| H71 | DFB Pokal | `DFB Pokal` | 0.5 |
| H72 | Coppa Italia | `Coppa Italia` | 0.5 |
| H73 | US Leagues Cup | `Leagues Cup` | 0.5 |
| H74 | Saudi King's Cup | `King's Cup` | 0.5 |
| H75 | Africa Cup of Nations | `Africa Cup of Nations` | 1.2 |
| H76 | UEFA Champions League | `UEFA Champions League` | 1.5 |
| H77 | CONCACAF Champions Cup | `CONCACAF Champions Cup` | 1 |
| H78 | AFC Champions League Two | `AFC Champions League Two` | 0.7 |
| H79 | World Cup | none (`world-cup.json` has no `competition.name`) | 1.5 |

Each player's coefficient for a column depends on the competition he actually played. For example, Dom. League is H62 for a LaLiga player and H61 for a Premier League player, and Dom. Cup for Hakimi or Mane is H75.

## Statistic Metrics Coefficients (`P61:R97`)

Per position metric (5 per position, rows 61–95) three cells: **`P` weight** (points per standard deviation), **`Q` reference** (the position mean of that metric's weighted average) and **`R` scale** (its population SD). `P96` (`90s played`) and `P97` (`Rating`) are plain multipliers with no Q/R. Together they make players in different positions comparable. Claude determines them when the user asks, after every metric is filled in. When that is requested:

- Derive the values from the filled-in metrics. Don't invent them.
- Keep the rank order sensible: the 5 position metrics matter most, `90s played` less, `Rating` least.
- State the method and assumptions.
- Formulas reference `P61:R97`, never literal numbers (the structural baseline `70` is the one exception).

### Metric importance (`_docs/player-metric-importance-ranking.md`)

Within a position, a metric's weight `P` follows its importance rank: rank 1–5 get weights in the ratio **22 : 18 : 14 : 10 : 6**. Ranks, by sheet column order (metric 1..5):

| Position | Ranks of metric 1..5 | Most important → least |
|---|---|---|
| GK | 2, 4, 1, 5, 3 | Goals Prevented, Saves %, Long Balls %, Goals Against, Clean Sheets % |
| CB | 3, 1, 5, 2, 4 | Aerial %, Passes %, Tackles Won %, Long Balls %, Defensive Actions |
| LB/RB/LWB/RWB | 3, 5, 2, 4, 1 | xG + xA, Final Third Passes, Ground Duels %, Attacking Actions, Defensive Actions |
| DMC/MC | 4, 1, 2, 3, 5 | Press Resistance x GEWR, Passes %, Final Third Passes, Defensive Actions, Attacking Actions |
| MC/AMC | 4, 1, 2, 3, 5 | xA, Press Resistance x GEWR, Final Third Passes, Goals, Attacking Actions |
| LW/RW | 1, 5, 2, 3, 4 | Goals, xA, Dribbles %, Attacking Actions, Goals per Shot |
| CF/SS | 1, 5, 2, 4, 3 | Goals, xA, Attacking Actions, Aerial %, Goals per Shot |

### Calibration (agreed with the user on 2026-10-19; re-derive with the same method if metrics, `H61:H79` or the ranking change)

Why standardised: with a plain `metric × coef`, a coefficient carries the metric's units (xA per 90 ≈ 0.16 needs a far bigger coefficient than Goals per 90 ≈ 0.9), and a metric's real influence depends on how much it varies between players. Dividing by the SD makes `P` the metric's actual say in the ranking.

1. For each player, take the five weighted averages exactly as the Stats Points formula does (`w = c * n90`).
2. Outfield positions: `Q` = unweighted mean of those averages over the position's players; `R` = their population SD.
3. `P_k = g × rankweight_k`, where the position factor `g` makes the SD (across the position's players) of `Σ P_k (avg_k − Q_k) / R_k` equal the SD of `Σ 14 × avg_k / Q_k`. In other words, each position keeps the average (70) and the spread of the original equal-weights model, and only which metric drives the differences changes.
4. GK (two keepers can't give an SD): `Q = R =` David Raya's own average (the only top-flight GK nominee). `P` = rank targets, so Raya scores exactly 70: Goals Against (lower is better) gets `−10`, the other four get `rankweight × 80/60` (Goals Prevented 29.33, Saves 24, Long Balls 18.67, Clean Sheets 8).
5. `90s played`: `P96 = 22 / (mean weighted 90s sum over all 37)`. `Rating`: `P97 = 8 / (mean rating over all 37)` (unchanged since 2026-10-18). An average nominee therefore scores about 100.
6. Round all values to 4 significant figures.

Superseded: on 2026-10-18 the coefficients were `14 / position mean` for every metric, with the plain `metric × coef` formula. That gave each metric equal weight, so it ignored importance (for CF/SS, xA drove more of the ranking than goals).

## Stats Points (column AG)

```
70 + P1 * (metric1 - Q1) / R1 + ... + P5 * (metric5 - Q5) / R5
  + (metricNinetyMinutes * coefNinetyMinutes) + (metricRating * coefRating)
```

(`P/Q/R` are the player's position rows of `P61:R95`, see above. This replaced the original `metric * coef` shape on 2026-10-19.)

Per-competition values are `v` and competition coefficients are `c` (from `H61:H79`). A competition whose cell is `N/A` is dropped from that sum and from its denominator.

1. **`metric1..metric5`** are averages weighted by competition coefficient **times 90s played** (`w = c * n90`), so a few minutes as a substitute can't swing a player's average (changed from `c` alone at the user's request on 2026-10-18):
   `(vDL*wDL + vDC*wDC + vIC*wIC + vWC*wWC) / (wDL + wDC + wIC + wWC)`
   If a player has only Dom. League and Int. Cup: `(vDL*wDL + vIC*wIC) / (wDL + wIC)`.
2. **90s played** is a weighted **sum**, not an average, so players who played more time or in bigger competitions are rewarded. It must not outweigh the five metrics.
   `n90DL*cDL + n90DC*cDC + n90IC*cIC + n90WC*cWC`
3. **Rating** is a true average weighted by 90s played, and is the least important term because attackers get higher ratings than defenders:
   `(rDL*n90DL + rDC*n90DC + rIC*n90IC + rWC*n90WC) / (n90DL + n90DC + n90IC + n90WC)`

## Bonus Points (column AH)

Bonuses for winning competitions, finishing as top scorer, top assister, season MVP, being in a Team of the Season and so on. Since 2026-10-19 they are live formulas that reference the Bonus Points (Achievements) Coefficients table (`U60:Y70`) and the competition coefficients (`H61:H79`). The scale, what counts, the involvement rule and the update procedure are in `ballon-dor-bonus.md`; each player's achievements are in `_docs/bonus-points-achievements.md`. Write them only when the user asks.

## Total (column AI)

Stats Points + Bonus Points, as a live formula `=AG<row>+AH<row>` per player. Written by `/fill-ballon-dor-total-standings` when the user asks, and only once both input columns are numbers on every player row. The same skill writes the standings in `A:B` (see `ballon-dor-sheet-layout.md`).

The final standings in `A1:B37` are sorted by Total. They are written only after all 37 Totals are filled. See `ballon-dor-sheet-layout.md` (Standings).
