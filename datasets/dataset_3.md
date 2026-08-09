# Dataset: FIFA World Player & Team Stats (players_22.csv)

**Source:** Kaggle — FIFA 22 Complete Player Dataset
**Category:** Sports & Athletics
**Size:** 19,239 rows x 110 columns (Numeric: 60, Categorical/Text: 48, Date/Time: 2)

## Key Findings

**Ratings distribution:**
Player quality follows a near-normal distribution centered at a mean rating of 65.8, with most players clustering in the 60–70 band. Elite 85+ rated stars (e.g. Messi at 93) are rare outliers.

**Attribute correlation — mental/technical over physical:**
Mental and technical skills drive overall rating far more than physical traits. movement_reactions is the strongest correlate (r = 0.87), ahead of passing (r = 0.72) and mentality_composure (r = 0.71). Physical traits are weak predictors: pace (r = 0.17), power_strength (r = 0.36), movement_sprint_speed (r = 0.21). Market variables also correlate but less strongly: wage_eur (0.60), value_eur (0.55).

**Position and value:**
Midfielders hold the highest average rating (66.0), narrowly ahead of Forwards and Defenders (65.9 each), with Goalkeepers trailing (64.4). However, Forwards command the highest average market value (€3.45M) and wage (€10,864/week) — attacking roles are valued at a premium despite not having the highest average rating.

**Contracts and value concentration:**
Longer contracts are concentrated among higher-rated, higher-value players. Players with 4+ years left on contract average a 70.0 rating and €9.3M market value, compared to 65.1 rating and €2.0M for players with 0–1 years left. Market value rises steadily with contract length: €2.0M (0–1 yrs) → €4.5M (2 yrs) → €5.5M (3 yrs) → €9.3M (4+ yrs). Clubs lock in their best talent long-term rather than the reverse.

## Overall Story
FIFA 22 models football success as skill-driven rather than purely athletic. The highest-rated players excel in mental/technical attributes (reactions, passing, composure) that capture decision-making speed and technical precision, while physical traits (pace, strength) show weak influence. This skill-centric pattern extends into economics: Forwards earn the most despite not rating highest, and clubs invest long-term contracts in players who are already highly rated and valuable — resources concentrate around proven, already-valuable talent rather than being distributed evenly.

## Limitations
- Subjective ratings: Overall/potential/attributes are scout-assigned by Sofifa/EA, not measured from real matches — introduces human bias (e.g. reputation bias toward star players).
- Snapshot in time: reflects FIFA 22 only, not career trajectories or in-season changes.
- Missing data: national-team fields absent for ~96% of players; loan data missing for ~94%.
- Correlation ≠ causation: strong correlations (e.g. reactions vs overall) don't prove direct influence — may reflect shared scouting judgments.
- Market noise: wages/values shaped by external factors (agents, budgets, marketability) not captured in the dataset.