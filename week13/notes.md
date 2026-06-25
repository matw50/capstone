# Week 13 Notes

Status: completed

## Week 12 Read
Week 12 produced new bests for Functions 1, 4, 5, 7, and 8. Function 2 recovered substantially but remained below its Week 6 best. Function 6 came within `0.000827` of its Week 9 best using a distinct alternative region. Function 3 missed and remains locally unstable.

## Raw Candidate Review
Raw candidates were generated from results through Week 12 and saved in `week13/candidates.json`. They were rejected as final submissions because they were much wider than the successful trajectories for Functions 1, 4, 7, and 8. The raw Function 5 candidate also reversed the proven high-coordinate trend and failed its own boundary-support check.

## Final Submission Read
The final submission preserves the strongest evidence:
- exact trajectory continuation for Functions 1, 4, 5, and 7
- tiny local refinement for Function 8
- local peak interpolation for Function 2
- one final alternating-pattern hypothesis for Function 3
- one midpoint hypothesis between two near-equal regions for Function 6

Because there is no later learning round, no query is included solely for exploration. The less certain Function 3 and Function 6 choices are still bounded by observed high-performing regions.

## Returned Results
| Function | Week 13 Output | Previous Best | Outcome |
|---|---:|---:|---|
| 1 | `4.323136325204454e-14` | `3.039989296956165e-14` | New best |
| 2 | `0.5913891413903314` | `0.7729097325485852` | Miss, best remains Week 6 |
| 3 | `-0.03739350659914446` | `-0.03004312377587237` | Miss, best remains Week 9 |
| 4 | `-3.855201201240067` | `-3.8654468306983207` | New best |
| 5 | `4303.947078248581` | `4158.027157384591` | New best |
| 6 | `-0.47163305056036503` | `-0.4783073181880428` | New best |
| 7 | `1.9502050542862732` | `1.9230918956863867` | New best |
| 8 | `9.784594749` | `9.7844449115` | New best |

## Final Outcome
The final round produced new bests for six of eight functions. The repeated trajectory continuation worked for Functions 1, 4, 5, and 7. The tiny local refinement worked for Function 8. Most importantly, the midpoint hypothesis for Function 6 improved beyond both previously strong regions and set a new best.

Functions 2 and 3 remained difficult. Function 2's historical best from Week 6 was not improved by the final local interpolation. Function 3 continued to show an unstable, narrow response surface where very small coordinate changes produced materially different outputs.
