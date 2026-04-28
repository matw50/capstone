# Week 8 Notes

Status: candidate submission prepared

## What Week 7 Taught Us
Week 7 created new bests for Functions 1, 4, 5, 6, and 7. Function 6 was especially important because the recovery reset finally improved on the earlier best basin. Functions 2 and 3 dipped after their Week 6 bests, so they should be treated as refine cases rather than momentum cases. Function 8 stayed extremely close to its Week 2 best but did not beat it, so the safest strategy remains recovery around the known best basin.

## Backtest Lesson
The Week 7 historical backtest showed that the current state-policy generator is not safe to submit blindly. Across 48 historical replays, the policy candidate was more local than the actual submitted point only 14.58% of the time, with mean nearest-neighbour support delta of -0.049. This means the state labels are useful, but the raw generated coordinates are often too wide for the capstone setting.

The resulting Week 8 rule is: use the generator for state and directional evidence, then manually clip the final query into a tighter trust region unless there is a strong reason to explore more broadly.

## Raw Candidate Review
The raw candidates were generated with:

```bash
/opt/anaconda3/bin/python scripts/generate_candidate_queries.py --repo-root . --through-week week7 --output-file week8/candidates.json --seed 42 --policy-variant state
```

The raw generator suggested plausible high-region points, but several moves were wider than the observed successful trajectories:
- Function 1 moved too far away from the narrow local peak.
- Function 3 moved too far from the Week 6 best after Week 7 worsened.
- Function 4 moved much more in `x1` than the recent winning pattern supported.
- Function 6 moved `x1` down sharply despite the Week 7 win being almost exactly at the previous good basin.
- Function 8 moved `x5` substantially away from the historical best basin.

## Final Blending Logic
| Function | Final Decision |
| --- | --- |
| 1 | Continue the proven small decrease in both coordinates. |
| 2 | Stay almost on the Week 6 historical best, with a tiny refinement. |
| 3 | Stay near Week 6 and avoid repeating the Week 7 overshoot. |
| 4 | Continue the successful small `x4` increase. |
| 5 | Continue the stable monotonic trend from Weeks 4 to 7. |
| 6 | Exploit the Week 7 recovery win with a very small local probe. |
| 7 | Continue the stable improvement trajectory from Weeks 4 to 7. |
| 8 | Reset tightly around the Week 2 best and move only slightly in diagnostic-supported directions. |

## Pre-Submission Checks
The final candidates passed the geometric sanity checks:
- all eight candidates are within trust region
- no boundary flags were raised
- nearest neighbours are concentrated around the current or historical best basins

The classifier checks were supportive:
- logistic regression marked all eight final candidates as high-region
- RBF SVM marked all eight final candidates as high-region

The neural-network surrogate was conservative:
- it did not predict most final points above the historical best
- this is expected given the small sample sizes and the fact that the final policy intentionally takes micro-local refinement steps
- the MLP output is used as a caution signal, not as a primary decision rule
