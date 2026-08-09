# Dataset: Formula 1 World Championship (1950–2024)

**Source:** Kaggle — Formula 1 World Championship (1950–2024)
**Category:** Sports & Athletics
**Size:** Race results (26,759 rows x 13 cols), Lap times (589,081 rows x 3 cols), Driver/Country standings (34,863 rows x 8 cols), Pit stops (11,371 rows x 3 cols)

## Key Findings

**Finding 1 — Eurocentric dominance:**
British and German drivers dominate F1 in both race entries and Grand Prix victories. British drivers lead participation (1,000+ races) and have secured nearly 300 wins. German and French drivers follow closely (~900 races each). F1 is widely popular and supported primarily by European countries.

**Finding 2 — Starting grid position determines race outcome:**
A driver's starting grid position heavily dictates their final race result. Most race finishes concentrate in the top 1st–5th positions for drivers who started near the front. This reflects F1's qualifying-then-race structure, and shows overtaking is difficult. Average lap times (80–100 seconds) stabilize after opening laps, but lap duration increases sharply the further back a driver starts — showing a steep performance gap between front-runners and back-of-grid racers.

**Finding 3 — Mechanical failures and lap deficits cause most DNFs:**
Among drivers who fail to finish, being lapped ("+1 Lap") is the most frequent cause, followed closely by mechanical failures (engine, gearbox). This signals that constructor reliability and car condition are major factors in race outcomes. Once a car falls behind, lap times decline steeply and it gets lapped by front-runners.

**Finding 4 — Most drivers never score championship points:**
F1's points system only rewards the top 10 finishers out of ~22 active drivers on the grid (historically top 6). More than half the grid never scores points in a given race. Combined with the fact that championships are heavily decided by car technical specifications, breaking into the points is a major challenge for most of the field.

## Overall Story
F1 is shaped by Eurocentric dominance, mechanical/constructor hierarchies, and structural exclusivity. Starting position and car reliability matter more than raw driver skill in determining outcomes. The sport lacks recognition outside Western regions (particularly Africa and Asia) due to high barriers to entry. Race outcomes are heavily decided by engineering and constructor investment, not solely driver skill.

## Limitations
- No data on car specifications, track conditions, or granular match details.
- European dominance may introduce fan-support/data bias (Eurocentric bias).
- Survivorship bias: lap time data only reflects drivers who completed the race.
- Historical bias: dataset spans 1950–2024, during which rules changed significantly (scoring adapted to modern standards for this analysis).
- No predictive modeling attempted — lack of car spec/track condition data makes this unreliable.