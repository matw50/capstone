# Week 12 Approach

Week 12 is the penultimate submission, so the strategy shifts from normal iterative optimisation to an endgame policy.

## Endgame Policy
- Preserve winning basins for functions with recent momentum.
- Make only tiny corrections for near-miss functions.
- Use one controlled alternative for functions where repeated reset-to-best submissions have failed.
- Avoid broad raw-surrogate jumps unless the function is already a recovery problem.

## Function States
- Momentum: Functions 1, 4, 5, and 7
- Near-miss/refine: Functions 3 and 8
- Controlled alternative: Functions 2 and 6

## Decision Logic
The raw state-policy candidates were generated from data through Week 11, but several were too wide for the final two submissions. Functions 1, 4, 5, and 7 have continued to improve under local exploitation, so the final Week 12 inputs stay close to their latest bests. Function 3 nearly matched its Week 9 best in Week 11, and Function 8 only narrowly missed its Week 10 best, so both remain tightly anchored.

Function 2 and Function 6 are the exceptions. Repeated near-best resets have not recovered their historical best outputs, so Week 12 uses one bounded alternative for each. Function 2 moves slightly up in `x1` and down in `x2` relative to the Week 6 best, following the recent coordinate-sensitivity read rather than the raw candidate. Function 6 keeps the high-`x4`, low-`x5` structure but allows a moderate increase in `x2` and `x3`, because tiny repeats around the Week 9 point have not improved.
