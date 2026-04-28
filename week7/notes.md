# Week 7 Notes

## Summary
Week 7 starts from `week7/candidates.json`, generated from accumulated data through Week 6 using the new state-policy decision rules. The final submission keeps that policy as the engine, then applies manual basin-preserving overrides where the raw candidate is less conservative than the function history supports.

## What Week 6 Taught Us
- Functions 1, 2, 3, 4, 5, and 7 all set new best observed outputs.
- Function 8 remained very close to its historical best, so the basin still looks valid.
- Function 6 worsened materially, confirming that the deliberate lower-`x2`, lower-`x3` correction was the wrong direction.

## What The Benchmark Taught Us
The COCO/BBOB benchmark supported keeping the local trust-region strategy, but with explicit stagnation and recovery logic:

- old Week 6 style policy: `48` wins, `17` losses, `7` ties
- new state-policy dev benchmark: `54` wins, `16` losses, `2` ties
- new state-policy holdout benchmark: `210` wins, `55` losses, `23` ties

That result justifies using the state-policy generator for Week 7, but it does not remove the need for manual overrides on functions where the observed basin is much narrower than the generic benchmark problems.

## Raw Candidate Review
- Function 1: raw `0.698492-0.756814` was too aggressive for a sparse narrow peak, so it was replaced with an ultra-local continuation step.
- Function 2: raw `0.688668-0.908232` moved against the successful lower-`x1`, higher-`x2` direction, so it was replaced with a small continuation of that trend.
- Function 3: raw `0.480636-0.561951-0.349225` moved too far in `x2`, so it was smoothed into a smaller step along the same improving basin.
- Function 4: raw `0.544388-0.442764-0.439301-0.271712` jumped away from the validated basin, so it was replaced with a very small continuation around the Week 6 best.
- Function 5: raw `0.089436-0.979773-0.979773-0.984829` was directionally plausible but more aggressive than needed, so it was clipped to the next small boundary-following step.
- Function 6: raw `0.531818-0.327337-0.457703-0.877102-0.043070` widened `x3` and lowered `x4` too much, so it was replaced with a near-reset around the historical best basin.
- Function 7: raw `0.050400-0.451878-0.239475-0.252691-0.310372-0.726723` was broadly consistent, but the `x4` move was larger than the recent local trend, so it was smoothed into a smaller local continuation.
- Function 8: raw `0.083832-0.048337-0.020000-0.057516-0.567401-0.820099-0.075850-0.385018` pushed `x3` too low and moved too far in `x8`, so it was blended back toward the historical best basin.

## Final Validation
The final blended `week7/inputs.json` was checked after manual adjustment.

- All eight final candidates passed the trust-region check.
- None of the final candidates triggered boundary flags.
- Logistic and SVM classifier checks marked all eight final candidates as high-region.
- The neural-net surrogate remained strongest on Functions 5, 7, and 8, but did not predict any Week 7 candidate to beat the current best observed point. It is still treated as a secondary check rather than a decision maker.

## Final Week 7 Submission Set

- Function 1: `0.729800-0.729800`
- Function 2: `0.694000-0.936000`
- Function 3: `0.491000-0.594000-0.346000`
- Function 4: `0.578300-0.428800-0.425800-0.253000`
- Function 5: `0.110000-0.965000-0.965000-0.975000`
- Function 6: `0.500300-0.325000-0.386000-0.893000-0.039000`
- Function 7: `0.053000-0.464000-0.244000-0.204000-0.308000-0.728000`
- Function 8: `0.091500-0.041900-0.053700-0.065700-0.566100-0.832100-0.061800-0.409400`

## Returned Week 7 Outputs

- Function 1: `4.250433342725532e-15`
- Function 2: `0.7227908397061406`
- Function 3: `-0.05017215361785152`
- Function 4: `-3.962742151304709`
- Function 5: `3273.8921448849183`
- Function 6: `-0.4993080476858224`
- Function 7: `1.7491755214029385`
- Function 8: `9.784121999`

Week 7 produced new best observed outputs for Functions 1, 4, 5, 6, and 7. Function 6 was the most important strategic improvement because the recovery reset beat the previous Week 1 best. Function 8 remained extremely close to its historical best. Functions 2 and 3 underperformed relative to Week 6, so they should be reviewed carefully before generating Week 8.
