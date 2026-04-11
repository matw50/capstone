# Week 5 Notes

## Summary
Week 5 starts from `week5/candidates.json`, generated from the accumulated data through Week 4. The final submission is manually blended using the updated historical-best anchoring rule.

## What Changed
The previous trust-region strategy mostly worked, but Week 4 made one weakness clear: for several functions, the best-known point still came from the initial data or an earlier week. Continuing to anchor on the latest query could slowly drift away from the strongest known point.

The Week 5 rule is therefore:

- if Week 4 produced a new best, anchor on Week 4
- if an earlier point is still best, anchor on that historical best
- use recent submissions as directional evidence only
- keep classifier checks secondary to basin-locality checks

## Raw Candidate Review
- Functions 1, 3, and 4: raw GP proposals jumped too far from the historical best and were rejected.
- Function 2: raw GP proposal stayed in a plausible area but pushed to the upper boundary, so it was replaced with a safer local point near the best basin.
- Function 5: raw proposal stayed in the right basin but pushed to the boundary; it was clipped to a small local exploitation step.
- Function 6: raw RF proposal passed the trust-region check but moved further than necessary, so it was softened back toward the Week 1 best.
- Function 7: raw RF proposal stayed in the right basin but moved too far in `x2`, so it was smoothed into a smaller local step.
- Function 8: raw RF proposal was well supported, but the final point was blended back toward the Week 2 best because Week 4 was close but not a new best.

## Final Validation
The final blended `week5/inputs.json` was checked again after the manual adjustments.

- All eight final candidates passed the trust-region check.
- None of the final candidates triggered boundary flags.
- Functions 5, 7, and 8 had the strongest classifier support.
- Function 3 remained the lower-confidence classifier case, but it stayed very close to the historical best and passed the primary geometric checks.
- Function 1 remained sparse, but the final point was extremely close to the best historical point and passed the trust-region check.

## Experimental Neural-Net Check
A small bootstrap ensemble of regularised MLP regressors was also run as an experimental secondary check. This did not change the final submission, because the dataset is still small and the neural net should not override the trust-region and neighbour checks.

| Function | NN Mean Prediction | NN Std | Predicted Percentile | Interpretation |
|---|---:|---:|---:|---|
| 1 | `-0.000198` | `0.000176` | `0.071` | Not useful for this sparse function; keep the geometric local rule. |
| 2 | `0.542967` | `0.025858` | `0.786` | Supports a good region but not above the historical best. |
| 3 | `-0.054835` | `0.018787` | `0.684` | Lower-confidence case, consistent with caution. |
| 4 | `-5.416710` | `0.655331` | `0.912` | High percentile but noisy absolute prediction; keep historical-best anchoring. |
| 5 | `2678.594528` | `217.655765` | `0.958` | Supports the high-performing basin, but not a reason to exceed the trust region. |
| 6 | `-0.577562` | `0.016325` | `0.917` | Supports recentering near the Week 1 best but not aggressive movement. |
| 7 | `1.421007` | `0.292213` | `0.941` | Supports the strong basin but shows uncertainty, so keep a small local move. |
| 8 | `9.764244` | `0.012706` | `0.932` | Supports the basin and agrees with continued local refinement. |

Overall, the neural-net check is useful as an ensemble-style sanity check, especially for Functions 5, 7, and 8, but it is not reliable enough to become the primary optimiser.

## Final Week 5 Submission Set

- Function 1: `0.731800-0.735000`
- Function 2: `0.698000-0.932000`
- Function 3: `0.494000-0.625000-0.337000`
- Function 4: `0.577500-0.428800-0.425900-0.247000`
- Function 5: `0.130000-0.955000-0.955000-0.965000`
- Function 6: `0.495000-0.325000-0.388000-0.894000-0.038500`
- Function 7: `0.051000-0.478000-0.240000-0.200000-0.296000-0.732000`
- Function 8: `0.089300-0.040400-0.054700-0.066500-0.570000-0.828000-0.054000-0.408000`

## Returned Results
Week 5 produced new bests for Functions 2, 5, and 7:

- Function 2: `0.6804759634712958`
- Function 5: `2962.2983942628757`
- Function 7: `1.6645971234129806`

Functions 3, 4, and 8 remained close to their historical best basins. Function 1 improved relative to recent sparse probes but did not beat the original best. Function 6 remained the weakest case and motivated the Week 6 correction probe.
