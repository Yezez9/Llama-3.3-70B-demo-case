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

## Additional Chart Data — NBA

**League-wide averages (all players, all teams):**
Average points per player: 10.61 | Win-loss ratio: 1.01 | Free throw rate: 76.57% 
| Field goal rate: 45.54%

**League-wide shooting composition (share of scoring makes):**
Field goal: 109,665 (57.68%) | Free throw: 44,907 (23.62%) | 3-point: 35,565 (18.7%)

**Top 10 teams by win rate (highest to lowest):**
OKC, CLE, BOS, MIN, NYK, IND, DEN, GSW, MEM, ORL

**Shai Gilgeous-Alexander (SGA) — filtered dashboard view:**
Average points: 31.93 | Win-loss ratio: 3.76 | Free throw rate: 89.63% | 
Field goal rate: 51.06%
Shooting composition: Field goal 1,101 (0.58%), Free throw 794 (0.42%), 
3-point 197 (0.1%)

**Feature importance for predicting player points (standardized coefficient, ranked):**
FGA (~6.2, highest), FTA (~2.2), 3PA (~0.35), MP (~0.3), AST (~0.1), TRB (~0.05), 
BLK (~0.05), TOV (~0.03), STL (~0.03)

**Team scoring vs. win percentage:** R² = 0.471, scatter ranges from ~105 to 
~121.7 average team points per game, with win percentage ranging roughly 21% to 79%.