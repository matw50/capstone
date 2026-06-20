# Week 11 Approach

Week 11 used a micro-local trust-region strategy informed by the Week 10 results, generated candidates, sanity checks, classifier checks, and the historical backtest.

## Function States
- Momentum: Functions 1, 4, 5, 7, and 8
- Recovery: Function 2
- Refine: Functions 3 and 6

## Decision Logic
The raw state-policy candidates were generated from data through Week 10, but they were treated as directional suggestions rather than automatic submissions. The Week 10 backtest still showed that raw generated candidates tend to be wider than the successful hand-blended points, so the final Week 11 inputs were clipped tightly around known strong basins.

For Functions 1, 4, 5, and 7, the submission continued recent improving directions with small steps. Function 8 had just beaten its long-standing Week 2 best in Week 10, so the Week 11 point stayed extremely close to that new basin. Function 2 reset near the Week 6 historical best. Functions 3 and 6 returned toward their Week 9 best basins after Week 10 misses.

## Outcome
Week 11 produced new bests for Functions 1, 4, 5, and 7. Function 3 was a near miss, Function 8 was a tiny miss, and Functions 2 and 6 remained below their historical bests.
