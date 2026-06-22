# Week 12 Notes

Status: completed

## Week 11 Read
Week 11 produced new bests for Functions 1, 4, 5, and 7. Function 3 was a near miss against the Week 9 best, Function 8 was a tiny miss against the Week 10 best, and Functions 2 and 6 remained below their historical bests.

With only two submissions left, the strategy should not reward novelty for its own sake. The working functions should be protected with very small local moves. Only repeated recovery failures should receive bounded alternatives.

## Raw Candidate Review
Raw candidates were generated with `scripts/generate_candidate_queries.py` using results through Week 11 and saved to `week12/candidates.json`.

The raw candidates were useful as directional signals, but several were too wide for the endgame:
- Function 1 raw candidate moved far away from a narrow, improving local peak.
- Function 4 raw candidate moved wider than the recent smooth trend.
- Function 7 raw candidate reversed some of the recent successful direction and moved too far in `x6`.
- Function 8 raw candidate moved too broadly despite only a tiny Week 11 miss.

Function 5's raw candidate supported continued boundary-adjacent exploitation, but the final point uses a smaller step. Functions 2 and 6 are the only functions where a bounded alternative is deliberately accepted.

## Final Submission Logic
- Function 1: continue the tiny downward trend in both coordinates.
- Function 2: take one controlled alternative near the Week 6 best, moving `x1` up and `x2` down.
- Function 3: stay very close to the Week 9/Week 11 basin.
- Function 4: continue the smooth `x4` increase with tiny supporting changes.
- Function 5: continue the strong low-`x1`, high-remaining-coordinate trend near the boundary.
- Function 6: use one controlled alternative with higher `x2` and `x3`, while preserving high `x4` and low `x5`.
- Function 7: continue the repeated local trend: `x2` down, `x5` up.
- Function 8: return almost exactly to the Week 10 best basin with a tiny correction.

## Returned Results
| Function | Week 12 Output | Previous Best | Outcome |
|---|---:|---:|---|
| 1 | `3.039989296956165e-14` | `2.1298682212075036e-14` | New best |
| 2 | `0.6571581178488444` | `0.7729097325485852` | Strong recovery, but below Week 6 best |
| 3 | `-0.040370655143158865` | `-0.03004312377587237` | Miss, best remains Week 9 |
| 4 | `-3.8654468306983207` | `-3.8786214264912924` | New best |
| 5 | `4158.027157384591` | `3977.5206205578024` | New best |
| 6 | `-0.47913451327539497` | `-0.4783073181880428` | Extremely close miss |
| 7 | `1.9230918956863867` | `1.8932361849960195` | New best |
| 8 | `9.7844449115` | `9.784294951` | New best |

## Final-Round Read
Week 12 was a strong penultimate round. Functions 1, 4, 5, 7, and 8 all produced new bests, validating the decision to protect their existing basins. Function 2's controlled alternative recovered substantially from Week 11, although it did not beat the Week 6 best. Function 6's controlled alternative nearly matched the Week 9 best, suggesting that the broader direction was useful but the final query should remain close to the strongest observed region.

Function 3 was the clearest miss and should return to the Week 9 best basin for the final submission rather than widen further.
