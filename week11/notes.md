# Week 11 Notes

Status: completed

## Week 10 Read
Week 10 produced new bests for Functions 1, 4, 5, 7, and 8. Function 8 finally beat the long-standing Week 2 best, so it moves from recovery to momentum. Function 2 missed again and remains the main recovery case. Functions 3 and 6 missed after Week 9 bests, so they should return toward the Week 9 best basins.

## Raw Candidate Review
Raw candidates were generated with `scripts/generate_candidate_queries.py` using results through Week 10 and saved to `week11/candidates.json`.

The raw candidates passed the main classifier checks, but several were wider than the successful recent manual submissions. The Week 10 backtest still shows the raw state-policy generator tends to be broader than the hand-blended points that have worked best, so the final Week 11 inputs were manually clipped around proven basins.

## Final Submission Logic
- Function 1 continues the tiny downward trend in both coordinates, avoiding the raw GP jump.
- Function 2 resets tightly around the Week 6 historical best rather than chasing the failed Week 10 point.
- Function 3 returns toward the Week 9 best and applies only a small x2-up, x3-down correction.
- Function 4 continues the smooth x4-increase trend with small supporting coordinate changes.
- Function 5 continues the strong monotonic boundary-adjacent trend, but less aggressively than the raw candidate.
- Function 6 returns very tightly to the Week 9 best basin after the Week 10 miss.
- Function 7 continues the repeated successful trend: x2 down, x5 up, with small supporting moves.
- Function 8 exploits the new Week 10 best with a very small local move rather than the wider raw RF candidate.

## Returned Results
| Function | Week 11 Output | Previous Best | Outcome |
|---|---:|---:|---|
| 1 | `2.1298682212075036e-14` | `1.4866234300522646e-14` | New best |
| 2 | `0.460083800687324` | `0.7729097325485852` | Miss, best remains Week 6 |
| 3 | `-0.03036841573134169` | `-0.03004312377587237` | Near miss, best remains Week 9 |
| 4 | `-3.8786214264912924` | `-3.894853077058254` | New best |
| 5 | `3977.5206205578024` | `3791.026604594503` | New best |
| 6 | `-0.5778993109420945` | `-0.4783073181880428` | Miss, best remains Week 9 |
| 7 | `1.8932361849960195` | `1.8607688064809809` | New best |
| 8 | `9.7842649265` | `9.784294951` | Tiny miss, best remains Week 10 |

## Week 12 Implications
Week 11 was strong overall, producing new bests for Functions 1, 4, 5, and 7. Function 3 was a very close miss against its Week 9 best, so it should remain a tight refine case rather than broad exploration. Function 8 was also a tiny miss after the Week 10 improvement, which argues for returning to the Week 10 best basin with only a minimal perturbation.

Function 2 continues to be the hardest recovery problem. The reset around the Week 6 best did not recover performance, so Week 12 should consider either a very small return exactly around the Week 6 best or one bounded alternative basin, but not a broad raw jump. Function 6 also remains difficult; the Week 11 return-to-basin point improved over Week 10 but did not approach the Week 9 best, so it should be treated as refine/recovery with caution.
