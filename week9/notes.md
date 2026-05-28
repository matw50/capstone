# Week 9 Notes

Status: submitted

## What Week 8 Taught Us
Week 8 validated the micro-local approach for Functions 1, 4, 5, and 7, all of which produced new best outputs. It did not improve Functions 2, 3, 6, or 8.

The most important strategic update is that not every missed function should be handled the same way:
- Functions 2 and 3 have now missed twice after strong Week 6 results, so they can justify one bounded alternative.
- Function 6 missed only once after a successful Week 7 recovery, so it should return toward the Week 7 best rather than explore.
- Function 8 has remained very close to the Week 2 best for several rounds, so broad movement still looks risky.

## Raw Candidate Review
The raw state-policy generator was run through Week 8 and saved to `week9/candidates.json`.

The raw candidates were useful for state and direction, but several were again wider than the observed successful trajectories. The Week 8 backtest still showed the raw generator is usually wider than the hand-blended submissions, so the final points were manually clipped unless a bounded alternative was justified.

Accepted or mostly accepted:
- Function 2 used the raw local-exploit candidate because the function is now stagnant and the move is still within the local region.
- Function 5 continued the same monotonic trajectory, though with a safer hand-blended step.

Manually tightened:
- Function 1 stayed ultra-local around the Week 8 best rather than taking the wider GP move.
- Function 3 stayed near the Week 6/Week 8 basin rather than taking a larger jump.
- Function 4 continued the successful small `x4` movement rather than taking the full raw GP step.
- Function 6 returned near the Week 7 best rather than following the wider RF move.
- Function 7 continued the stable recent trend with a smaller step than the raw RF candidate.
- Function 8 stayed very close to the Week 2 best rather than following the raw RF move in `x8`.

## Pre-Submission Checks
The final Week 9 inputs passed the sanity checks:
- all eight candidates are within trust region
- no boundary flags were raised
- nearest neighbours are concentrated around current or historical best basins

Classifier checks were supportive:
- logistic regression classified all eight candidates as high-region
- RBF SVM classified all eight candidates as high-region

The neural-network surrogate was conservative:
- it did not predict most candidates above the historical best
- this was treated as caution rather than rejection because the data remains small and the primary rule is basin-aware local refinement

## Awaiting Results
After the Week 9 outputs return, classify each function as:
- new best: continue momentum with smaller local step
- near miss: refine around historical best
- clear miss: reset to best basin
- repeated miss: allow one bounded alternative, then recover if it fails
