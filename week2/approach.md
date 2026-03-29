# Week 2 Approach

## Principle
For Week 2, the strategy shifts toward a more sample-efficient trust-region approach. The main idea is to use tight exploitation where Week 1 improved, and to return to the best historical region where Week 1 failed.

This means:
- exploit locally for Functions 5, 6, and 8
- refine cautiously for Functions 2 and 4
- return to the best historical region for Functions 1, 3, and 7

## What Changes From Week 1
Week 2 should not reuse the same broad random-forest style search across all higher-dimensional functions. With a limited remaining query budget, the strategy now needs to become more conservative and more local.

For the lower-dimensional functions, the plan is to use Gaussian-process-style reasoning around the best observed point. For the higher-dimensional functions, the plan is to use local surrogate-guided search rather than broad global search.

In practice, this means:
- smaller moves
- more trust in observed winners
- less willingness to jump to distant regions unless the previous direction clearly failed

## Function Groups
### Recovery functions
Functions 1, 3, and 7 are treated as recovery functions because the Week 1 direction did not perform well enough. The plan is to go back to the best historical point, search very close to it, and avoid broad exploration unless several local refinements also fail.

### Cautious refinement functions
Functions 2 and 4 are treated as uncertain but promising. The plan is to stay near the best region and make small corrective adjustments rather than reset completely.

### Momentum functions
Functions 5, 6, and 8 are treated as momentum functions because Week 1 produced strong signals there. The plan is to exploit around the new best point using a tight local neighbourhood and prioritise refinement over exploration.

## Operational Rule
The practical decision rule for the remaining rounds is:
1. If the latest query improved the best value, shrink the radius and exploit again.
2. If the latest query was close but not better, stay in the same region and adjust slightly.
3. If the latest query clearly failed, return to the historical best point and restart locally there.
4. Only if a region fails repeatedly, test a second-best region.

## Method Choice
- Use local Gaussian Process trust-region search for lower-dimensional functions.
- Use local Random Forest trust-region search for higher-dimensional functions.
- Keep broad exploration minimal because there are only a limited number of remaining guesses.
