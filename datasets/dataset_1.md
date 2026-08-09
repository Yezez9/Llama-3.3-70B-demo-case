# Dataset: NBA — Player Stats, Season 2024–25

**Source:** Kaggle — NBA Player Stats Season 24/25
**Category:** NBA player performance & shooting stats
**Size:** 28,265 rows x 24 columns (player-game records)
**Columns:** Player, Tm, Opp, Res, MP, FG, FGA, FG%, 3P, 3PA, 3P%, FT, FTA, FT%, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS, GmSc, Date

## Key Findings

**Finding 1 — Scoring explains less than half of winning:**
Average team points per game has a positive, statistically observable relationship with win percentage, but scoring alone explains just under half of winning (R² = 0.471). Scoring more generally helps a team win more, but it is not a reliable standalone predictor — roughly 53% of what determines wins comes from factors this dataset doesn't capture (defense, opponent quality, clutch performance, depth).

**Finding 2 — FGA and FTA are the main drivers of individual points:**
Field goal attempts (FGA) is by far the strongest predictor of a player's points, followed distantly by free throw attempts (FTA). Other stats — 3PA, MP, AST, TRB, BLK, TOV, STL — contribute marginally (R² = 0.844, MAE = 2.614). Among player skills measured, shot volume (FGA/FTA) matters far more than other stat categories in predicting point totals.

**Finding 3 — Seasonal FGA/points trend and playoff dip:**
FGA (bar) and average points (line) track closely together month-over-month across the season. Both decline sharply from April into June. This is not a performance or scoring decline — it's a sample-size effect: playoff elimination progressively shrinks the pool of active teams/players from April through June, so fewer games and players are averaged into those months.

**Finding 4 — Case study: Shai Gilgeous-Alexander (SGA):**
SGA is the league's top scorer (31.93 PPG, almost 3x the average player) and plays for OKC (Oklahoma City Thunder), the team with the best win rate this season (79.2%). His free throw percentage is 89.63%, well above league average. He illustrates the "volume + efficiency" pattern — shoots a lot AND converts efficiently, especially at the line — but this is a single case, not proof his stats caused OKC's team success.

**Additional check — top scorers don't cluster on top teams:**
Checking all 10 top scorers against team win-rate rank shows the "elite scorer = elite team" pattern does NOT hold broadly: SGA (#1 scorer) is on the #1 win-rate team, but Giannis Antetokounmpo (#2 scorer) is on the 12th-ranked team, Kevin Durant (#8 scorer) is on the 22nd-ranked team, and Tyrese Maxey (#9 scorer) is on the 26th-ranked team (out of 30). Elite individual scoring does not reliably predict team success.

## Overall Story
Team scoring explains only 47% of win percentage (R² = 0.471) — shot volume and attempts, while the strongest predictors of individual point totals (R² = 0.844), are necessary but not sufficient to explain wins. The remaining ~53% likely reflects factors outside this dataset (defense, opponent strength, clutch execution, bench depth). Scoring is the floor, not the ceiling, for winning.

## Limitations
- Dataset only contains box-score stats — no defensive matchup data, coaching, payroll, or roster-construction data.
- SGA/OKC case study is a single data point and does not establish causation.
- No multicollinearity testing between FGA and FTA in the regression (high-volume scorers likely also draw more fouls, so these predictors may be correlated with each other).