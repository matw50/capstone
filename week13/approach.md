# Week 13 Final-Round Approach

Week 13 is the final submission. The objective is no longer to gather information for a later round, so the strategy is almost entirely exploitative. Raw surrogate candidates are used only as reference because they continue to propose moves that are wider than the successful observed trajectories.

## Final Decision Rules
- Continue an established monotonic trajectory when it has improved repeatedly.
- Use tight local estimation around the historical best when a clear peak is visible.
- For unstable functions, make one evidence-based final hypothesis rather than repeating a known point.
- Do not make broad global jumps.

## Function Logic
- Function 1: continue the exact recent downward step pattern in both coordinates.
- Function 2: use a quadratic interpolation of the Week 5 to Week 7 local peak, placing the final query slightly below `x1=0.696` and above `x2=0.934`.
- Function 3: recent micro-local points alternate between strong and weak outputs. Move just beyond the latest strong Week 11 point rather than repeat the failed Week 12 midpoint.
- Function 4: continue the exact smooth trajectory that has improved in every recent round.
- Function 5: continue toward the apparent boundary optimum with one normal step, setting `x4` to its upper bound.
- Function 6: query the midpoint between the Week 9 historical best and the nearly equal Week 12 alternative. If the negative score is driven by summed penalties, the midpoint could improve on both endpoints.
- Function 7: continue the exact linear trajectory that has improved every round since Week 2.
- Function 8: make a tiny move from the Week 12 best following the latest sensitivity direction: lower `x6` and `x8`, and slightly increase `x5`.
