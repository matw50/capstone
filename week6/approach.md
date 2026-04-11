# Week 6 Approach

Week 6 keeps the historical-best anchored trust-region strategy, but adds a specific correction for Function 6.

The Week 5 results validated the anchoring rule: Functions 2, 5, and 7 reached new bests, while Functions 3, 4, and 8 stayed close to their best basins. Function 6 remained stalled, so Week 6 treats it as a special correction case rather than another near-identical local nudge.

The operating rule is:

- if Week 5 produced a new best, anchor on Week 5 and make a small local exploitation step
- if an earlier point is still best, anchor on that historical best and use recent observations only to choose direction
- reject raw GP/RF candidates that jump away from the validated basin or chase a boundary
- for Function 6, keep the strong `x4` high and `x5` low structure, but deliberately test lower `x2` and lower `x3`

The final Week 6 set remains conservative because only eight submissions remain after Week 5. The aim is to improve the best-known basins, not to map the full functions.
