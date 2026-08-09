# Dataset: European Soccer Database

**Source:** Kaggle — European Soccer Database
**Category:** Sports & Athletics
**Size:** Raw match table (~25,000 rows x 115 cols), Raw player attributes (183,978 rows x 42 cols), Engineered analysis table (18,815 complete match rows x 40 cols — 1 target variable `home_win`, 1 match ID, 38 average team attribute differentials)

## Key Findings

**Finding 1 — Team quality baseline predictor:**
A squad's higher overall player rating is the most reliable predictor of winning a match (correlation: 0.4404). The overall ceiling of a team's talent directly relates to baseline win chance (correlation: 0.4229).

**Finding 2 — Control over speed:**
Game intelligence and ball control matter far more than physical athleticism. A team's ability to react quickly (r = 0.4165), maintain possession (r = 0.3984), and execute short passes accurately (r = 0.3946) drives match success significantly more than raw running speed or stamina.

**Finding 3 — Attacking skill matters less once technical skill is accounted for:**
Raw attacking skills like finishing and shot power seem important on their own, but matter much less once a team's overall technical skill is factored in (model weight: 0.0366 for attacking vs. 0.1021 for technical). Technically skilled teams naturally create scoring chances through passing and control, making raw shooting stats less critical to predicting a win.

**Finding 4 — Irrelevant tactics and model accuracy:**
The ratio of right-footed to left-footed players on the pitch offers zero competitive advantage (correlation: 0.0023). Overall, grouping a team's baseline skills predicts real-world match outcomes correctly in about 7 of 10 games (accuracy: 70.42%, ROC-AUC: 0.7507) without looking at tactical formations at all.

## Overall Story
European soccer is won primarily through technical mastery, not pure physical dominance. Victory is systematically driven by game intelligence, precise passing, and ball retention — a team that controls the pace and space of a match has a consistently higher win chance than one relying on speed or isolated shooting power. In short: brains and ball control beat brawn.

## Limitations
- Goalkeeper stat dilution: averaging skills across all 11 players waters down the goalkeeper's specific stats (outfield players have very low goalkeeping scores), masking the goalkeeper's true impact.
- Missing live context: dataset relies on video-game skill ratings and ignores real-world variables like red cards, weather changes, or home-crowd psychological effects.
- Missing historical lineups: ~25% of matches were discarded due to missing starting lineup records for older games.