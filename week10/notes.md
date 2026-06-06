# Week 10 Notes

Status: submitted

## What Week 9 Taught Us
Week 9 produced new bests for Functions 1, 3, 4, 5, 6, and 7. This strongly supported the micro-local trust-region approach. Function 6 was particularly useful evidence because the Week 9 return-to-basin move produced a new best after Week 8 had missed.

Function 2's bounded alternative failed, so Week 10 resets it close to the Week 6 best. Function 8 remains close to its Week 2 best but has not improved, so it remains a tightly anchored recovery case.

## Raw Candidate Review
Raw candidates were generated with the state-policy script and saved to `week10/candidates.json`.

The raw candidates again provided useful state and direction signals, but several were too wide relative to the successful Week 9 behaviour:
- Function 1 raw candidate moved too far from the narrow peak.
- Function 2 raw recovery candidate had weak neighbour support, so the final point reset closer to the Week 6 best.
- Function 3 raw candidate had some MLP support but still moved wider than necessary after a new best.
- Function 4 raw candidate was wider than the smooth recent trend.
- Function 6 and Function 7 raw candidates moved too far for momentum cases with strong recent local evidence.
- Function 8 raw candidate moved broadly and had a boundary warning, so the final point stayed close to the Week 2 best.

Function 5 kept the monotonic direction from prior rounds, with a hand-blended step rather than the raw full-radius candidate.

## Pre-Submission Checks
The final Week 10 inputs passed the main checks:
- all candidates are inside trust region
- nearest neighbours are concentrated around current or historical best basins
- logistic regression classified all eight as high-region
- RBF SVM classified all eight as high-region

The only notable flag was Function 5 being near the upper boundary on `x4`. This was accepted because Functions 5 has improved repeatedly while moving in this boundary-adjacent direction.

## Awaiting Results
After Week 10 outputs return, classify each function as:
- new best: continue momentum with a smaller local step
- near miss: refine around the historical best
- clear miss: reset to best basin
- repeated miss: allow one bounded alternative only if the function is already stagnant
