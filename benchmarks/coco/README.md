# COCO / BBOB Benchmarks

This folder stores benchmark experiments for the capstone query strategy using the
COCO/BBOB continuous black-box optimization suite.

Current benchmark framing:
- use the same dimensions as the capstone: `2,3,4,5,6,8`
- start from `10` random initial evaluations
- allow `13` sequential guided evaluations
- compare the capstone local policy against a random continuation baseline

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

Outputs:
- `results.csv`: one row per problem and method
- `summary.json`: aggregated win/loss summary against random continuation
- `histories.json`: best-so-far traces and proposal method traces per problem
