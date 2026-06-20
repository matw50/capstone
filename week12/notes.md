# Week 12 Notes

Status: candidate prepared

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
