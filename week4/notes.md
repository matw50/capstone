# Week 4 Notes

## Summary
Week 4 starts from the raw trust-region candidates in `candidates.json`, then applies the same blended review process used in Week 3. The core objective is to preserve the late-stage basin-aware strategy now that only nine guesses remain after this round.

## What The Checks Said

### Strong support for the current basin
- Function 6 passed the trust-region check and both classifiers supported the candidate as being in a high-performing region.
- Function 7 passed the trust-region check and both classifiers strongly supported the candidate, although the raw proposal still moved more in `x2` than seemed necessary.
- Function 8 had the strongest overall support. It passed the trust-region check, had very strong neighbours, and both classifiers strongly supported it.

### Strong rejection of the raw global-style move
- Function 1 failed the trust-region check and the nearby observed outcomes were too weak to justify the raw jump.
- Function 2 failed badly because the raw candidate moved far away from the confirmed good basin near `[0.70, 0.93]`.
- Function 3 again drifted toward a weak upper-corner region and also triggered a boundary warning.
- Function 4 looked better under the classifier than under the geometric checks, which is exactly why the classifier remains a secondary signal rather than the main decision-maker.

### Right basin, too aggressive move
- Function 5 remained the clearest example of a useful but over-aggressive raw candidate. The neighbours were excellent and both classifiers strongly supported the region, but the proposal still pushed too hard toward the boundary.

## Final Week 4 Submission Logic

### Function 1
Keep an ultra-local probe around the historical best point. The final point moves back toward the original narrow peak rather than following the raw GP jump.

### Function 2
Stay inside the established high-performing basin near the best historical point. The final point is a very small local refinement rather than a global move.

### Function 3
Continue cautious local refinement between the improving recent region and the historical best. The final point moves in that direction instead of chasing the raw corner-seeking proposal.

### Function 4
Continue the reset-to-best-basin strategy. Week 3 improved after moving back toward the original basin, so Week 4 stays close to that point and adjusts the fourth coordinate toward the best-known region.

### Function 5
Continue hard exploitation, but clip the raw proposal back inside a sensible local neighbourhood. The final point keeps the same winning pattern without moving all the way to the boundary.

### Function 6
Use soft local exploitation around the strongest known basin. The final point stays close to the current best structure and avoids the larger third-coordinate move from the raw proposal.

### Function 7
Continue hard exploitation around the new best point from Week 3. The final point stays close to that basin but avoids the larger `x2` drift from the raw candidate.

### Function 8
Continue hard exploitation around the best basin. The raw proposal was already well supported, so the final point stays very close to it while remaining slightly blended toward the best historical point.

## Final Week 4 Submission Set

- Function 1: `0.732500-0.739500`
- Function 2: `0.702000-0.927500`
- Function 3: `0.496000-0.640000-0.334000`
- Function 4: `0.577000-0.429000-0.426000-0.240000`
- Function 5: `0.140000-0.950000-0.950000-0.960000`
- Function 6: `0.507000-0.323000-0.380000-0.892000-0.039000`
- Function 7: `0.050000-0.485000-0.238000-0.198000-0.290000-0.734000`
- Function 8: `0.086500-0.038500-0.056000-0.067500-0.575000-0.823000-0.045000-0.406500`
