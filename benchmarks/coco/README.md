# COCO / BBOB Benchmarks

This folder stores benchmark experiments for the capstone query strategy using the
COCO/BBOB continuous black-box optimization suite.

Current benchmark framing:
- use the same dimensions as the capstone: `2,3,4,5,6,8`
- start from `10` random initial evaluations
- allow `13` sequential guided evaluations
- compare the capstone local policy against a random continuation baseline and experimental variants
- use the state-machine trust-region policy with `bootstrap`, `momentum`, `refine`, `stagnant`, and `recovery` modes

Note:
- standard `bbob` does not provide every capstone dimension exactly
- the benchmark script reports both the requested dimensions and the actual dimensions returned by the suite

Main script:
- `scripts/run_coco_benchmark.py`

Typical command:

```bash
/opt/anaconda3/bin/python scripts/run_coco_benchmark.py \
  --repo-root . \
  --initial-design 10 \
  --sequential-budget 13 \
  --dimensions 2,3,4,5,6,8 \
  --instances 1
```

To compare the state policy, ranking-based policy, and random continuation baseline:

```bash
/opt/anaconda3/bin/python scripts/run_coco_benchmark.py \
  --repo-root . \
  --initial-design 10 \
  --sequential-budget 13 \
  --dimensions 2,3,4,5,6,8 \
  --instances 1 \
  --methods state,ranked,random \
  --output-dir benchmarks/coco/ranked_policy_dev_instance1
```

Outputs:
- `results.csv`: one row per problem and method
- `summary.json`: aggregated win/loss summary against random continuation
- `histories.json`: best-so-far traces and proposal method traces per problem

Key saved runs:
- `week6_style_budget13/`: original Week 6 style local policy benchmark
- `state_policy_dev_instance1_v5/`: updated state-policy development benchmark on instance `1`
- `state_policy_holdout_instances2to5_v5/`: updated state-policy holdout benchmark on unseen instances `2,3,4,5`
- `ranked_smoke/`: quick smoke test of the ranking-based candidate-selection layer
- `ranked_policy_dev_instance1/`: development benchmark comparing state policy, ranked policy, and random continuation

Ranking-policy decision:
- the ranked policy is implemented and benchmarked, but not currently used for live capstone submissions
- in the full development benchmark, ranked beat random continuation on `50` of `72` problems, but lost to the simpler state policy on `44` of `72` comparable problems
- this makes it a useful documented experiment, not the default operating strategy
