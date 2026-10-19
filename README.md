# Ballon d'Or 2026 model

A mathematical model that ranks the Ballon d'Or 2026 nominees from their 2025/26 season statistics. The ranking lives in the "2025-26" tab of a Google Sheet. This repo holds the raw data, the scoring rules, and the scripts that fill the sheet.

## Repository layout

| Path | Contents |
|---|---|
| `player-stats/<player-slug>/<category>.json` | Season statistics for 37 players (one file per competition) |
| `.claude/rules/` | Scoring spec: metrics, coefficients, Stats Points, Bonus Points, sheet layout |
| `.claude/skills/*/scripts/` | The three Python scripts that compute the sheet cells |
| `_docs/` | Source transcript of the sheet spec, metric ranking, bonus achievements |

A missing category file means the player did not play in that competition. It is a zero contribution, not missing data.

## Pipeline

The sheet is filled in this order. Each step is a Claude Code skill.

1. `/fill-ballon-dor-metrics` writes the metric cells `E:AF` from `player-stats/`.
2. `/fill-ballon-dor-stats-points` writes Stats Points (`AG`) from the metrics and the coefficient tables.
3. Bonus Points (`AH`) are live formulas over the bonus coefficient table. The user changes them as awards happen. Achievements are listed in `_docs/bonus-points-achievements.md`.
4. `/fill-ballon-dor-total-standings` writes Total (`AI = AG + AH`) and the sorted standings in `A1:B37`. It stops on any tied Total.

Each skill writes only its own cells. The rule files list the protected ranges.

## Running the scripts

The scripts need Python 3 and nothing else. They are normally run by the skills, but they can be run directly:

```bash
python3 -I .claude/skills/fill-ballon-dor-metrics/scripts/compute_metrics.py --help
python3 -I .claude/skills/fill-ballon-dor-stats-points/scripts/build_stats_points.py --help
python3 -I .claude/skills/fill-ballon-dor-total-standings/scripts/build_total_standings.py --help
```

The `-I` flag ignores the working directory and environment, so a stray `json.py` in the current folder can't shadow the standard library.

## Where to look

- **Sheet structure and cell locations:** `.claude/rules/ballon-dor-sheet-layout.md`
- **Metric formulas and the N/A policy:** `.claude/rules/ballon-dor-metrics.md`
- **Coefficients and Stats Points:** `.claude/rules/ballon-dor-scoring.md`
- **Bonus Points:** `.claude/rules/ballon-dor-bonus.md`

## Notes

- Competitions are weighted by type (`H61:H79`). Mixing leagues of very different strength is a modelling choice, so the weights matter. Change them in the sheet, not in the scripts.
- The sheet uses a decimal-comma locale. Formula separators are `;`, and numbers are written as JSON numbers.
- The data is season 2025/26. Bonus achievements are as of 2026-10-19. MLS 2026 is still running, so Messi's MLS entries are provisional.
