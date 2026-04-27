# Week 7 Approach

Week 7 uses the new state-policy decision rule, but keeps manual basin-preserving overrides as a final guardrail.

The benchmark-backed operating rule is:

- if the latest query made a new best, enter `momentum` and exploit locally around that latest point
- if a function is close to best but did not improve, enter `refine` and stay near the historical best basin
- if a function has failed repeatedly, enter `recovery` and return to the historical best region before exploring again
- use GP-style local search for lower-dimensional functions and RF-style local search for higher-dimensional functions
- reject raw candidates that break sparse-peak logic, reverse a clearly successful direction, or jump outside a well-validated local basin

Week 7 function grouping:

- `momentum`: Functions 1, 2, 3, 4, 5, 7
- `refine`: Function 8
- `recovery`: Function 6

In practice, Week 7 is still mostly exploitative. The new state-policy is used to generate the raw candidates in `week7/candidates.json`, but the final `week7/inputs.json` blends those outputs back toward the strongest observed basins when the raw move is larger than the capstone evidence justifies.
