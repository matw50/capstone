# Week 5 Approach

Week 5 adapts the trust-region strategy based on a key observation from the first four rounds: for several functions, the historical best point is still from the initial data or an earlier week, not the most recent query.

The updated rule is:

- anchor on the historical best point by default
- use the latest result as directional evidence, not automatically as the next search centre
- keep hard exploitation only where the latest query produced a new best
- reject raw candidates that jump away from a validated basin, even if the model or classifier looks optimistic
- keep classifier outputs as secondary checks behind trust-region, nearest-neighbour, and boundary checks

This means the Week 5 submission is no longer “latest-point anchored.” It is “historical-best anchored with recent-direction adjustment.”

## Function Groups

### Hard exploitation
Functions 5 and 7 both produced new bests in Week 4, so their Week 5 proposals continue in small local steps around the Week 4 best points.

### Historical-best anchoring
Functions 1, 2, 3, 4, 6, and 8 did not produce new bests in Week 4. For these functions, the Week 5 proposal is anchored to the best historical point, with recent results used only to decide direction and search radius.

### Special cases
Function 1 remains sparse and sharply peaked, so the Week 5 point is an ultra-local probe near the initial best. Function 6 is a correction case because recent local moves have not beaten the Week 1 best.
