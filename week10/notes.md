# Week 10 Notes

Status: completed

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

## Returned Results
| Function | Week 10 Output | Previous Best | Outcome |
|---|---:|---:|---|
| 1 | `1.4866234300522646e-14` | `1.0336471033861818e-14` | New best |
| 2 | `0.5643141829384726` | `0.7729097325485852` | Miss, best remains Week 6 |
| 3 | `-0.04091048355168235` | `-0.03004312377587237` | Miss, best remains Week 9 |
| 4 | `-3.894853077058254` | `-3.914241793277785` | New best |
| 5 | `3791.026604594503` | `3611.7361248913985` | New best |
| 6 | `-0.6311451723650855` | `-0.4783073181880428` | Miss, best remains Week 9 |
| 7 | `1.8607688064809809` | `1.8258324483760047` | New best |
| 8 | `9.784294951` | `9.7841491208186` | New best, finally beat Week 2 |

## Week 11 Implications
Week 10 mostly confirmed the late-stage micro-local strategy. Functions 1, 4, 5, 7, and 8 should be treated as momentum cases, with smaller moves around the latest successful point. Function 8 is the most important positive update because the Week 10 recovery probe finally improved the long-standing Week 2 best.

Function 2 remains the main recovery problem and should reset toward the Week 6 best basin rather than chase the Week 10 point. Functions 3 and 6 should be treated as refine cases returning to their Week 9 best basins, because both missed after recent improvements.

The Week 10 diagnostics and backtest still support the existing decision logic: use generated candidates for state and direction, but keep final submissions conservative, basin-aware, and manually clipped when raw candidates are too wide.
