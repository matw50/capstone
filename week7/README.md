# Week 7

Week 7 builds on the strong Week 6 outcome and the new state-policy benchmark work.

Week 6 produced new best observed outputs for Functions 1, 2, 3, 4, 5, and 7. Function 8 stayed very close to its historical best. Function 6 was the only clear miss, which pushed Week 7 toward a recovery reset for that function and continued local exploitation everywhere else.

This round also adopts the benchmark-backed state-policy approach validated on COCO/BBOB:

- dev benchmark: `54` wins, `16` losses, `2` ties, `75.0%` win rate
- holdout benchmark: `210` wins, `55` losses, `23` ties, `72.9%` win rate

The practical interpretation is that local trust-region exploitation remains the default, but raw model proposals are still manually clipped when they jump away from a clearly validated basin.

Core files:
- `inputs.json`: final Week 7 submission point for each function
- `submission.txt`: portal-ready Week 7 values in hyphen-separated format
- `outputs.json`: returned output value for each function once Week 7 is processed
- `results.json`: combined machine-readable input/output record once Week 7 is processed
- `approach.md`: Week 7 state-policy and function grouping
- `notes.md`: round-specific observations, raw-candidate review, and final adjustments
- `reproduction.md`: exact steps used to reproduce the Week 7 submission

Optional files:
- `candidates.json`: raw state-policy candidates before manual review
- `function_<n>/inputs.npy` and `function_<n>/outputs.npy`: accumulated arrays after the round is recorded
- plot folders such as `lower_dim/` or `convergence/`
