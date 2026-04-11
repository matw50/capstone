# Week 6 Notes

## Summary
Week 6 starts from `week6/candidates.json`, generated from accumulated data through Week 5. The final submission is manually blended using the historical-best anchoring rule, with Function 6 handled as a correction case.

## What Week 5 Taught Us
- Function 2 produced a new best after we anchored back to the historical basin.
- Function 5 and Function 7 continued to improve under hard exploitation.
- Functions 3, 4, and 8 remained close to their best basins and should stay local.
- Function 1 improved but still did not beat the initial sparse peak.
- Function 6 did not improve, so another tiny near-identical perturbation is unlikely to be the best use of the next query.

## Raw Candidate Review
- Functions 1, 3, and 4: raw GP proposals jumped too far from their historical-best basins and were rejected.
- Function 2: raw GP proposal moved away from the new Week 5 best, so it was replaced with a small continuation of the successful direction.
- Function 5: raw GP proposal chased the boundary, so it was clipped back to a small local step.
- Function 6: raw RF proposal stayed plausible but did not match the deliberate correction we wanted, so it was replaced with the lower-`x2`, lower-`x3` probe.
- Function 7: raw RF proposal moved too much in `x2`, so it was smoothed into a smaller local step.
- Function 8: raw RF proposal introduced a boundary flag and a large move in `x8`, so it was blended back toward the Week 2 best.

## Function 6 Correction
Function 6 keeps the strongest known structure from the Week 1 best:

- keep `x1` close to `0.50`
- test lower `x2`
- test lower `x3`
- keep `x4` high around `0.90`
- keep `x5` very low around `0.03`

Final Function 6 probe:

`0.500000-0.300000-0.365000-0.900000-0.030000`

## Final Validation
The final blended `week6/inputs.json` was checked after manual adjustment.

- All eight final candidates passed the trust-region check.
- None of the final candidates triggered boundary flags.
- Classifier checks marked all eight final candidates as high-region, though Function 3 remains lower confidence because the probabilities were weak.
- The neural-net check was supportive of the high-performing basins but did not predict any final candidate to beat the historical best. It remains a secondary sanity check only.
- Function 6 passed the primary checks, but its nearest neighbours are not the historical best. That is expected because Week 6 intentionally tests a slightly different lower-`x2`, lower-`x3` correction direction.

## Final Week 6 Submission Set

- Function 1: `0.730500-0.731500`
- Function 2: `0.696000-0.934000`
- Function 3: `0.492000-0.604000-0.343000`
- Function 4: `0.578000-0.428800-0.425800-0.251000`
- Function 5: `0.120000-0.960000-0.960000-0.970000`
- Function 6: `0.500000-0.300000-0.365000-0.900000-0.030000`
- Function 7: `0.052000-0.471000-0.242000-0.202000-0.302000-0.730000`
- Function 8: `0.091000-0.041500-0.053900-0.065900-0.567000-0.831000-0.060000-0.409000`
