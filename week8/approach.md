# Week 8 Approach

Status: candidate submission prepared

## Main Principle
Week 8 uses a backtest-informed trust-region approach. The historical backtest showed that the raw state-policy generator is useful for identifying state and direction, but it tends to propose wider moves than the manually blended submissions that have worked best so far. Therefore, the final Week 8 submission treats generated candidates as signal, not instruction.

The operating rule is:
- keep the policy state labels from the generator
- use progress diagnostics to identify plausible coordinate directions
- apply micro-local clipping around proven basins unless there is strong evidence for a wider move
- prefer historical-best anchoring where the latest round did not improve

## Function States
| Function | State | Week 8 Treatment |
| --- | --- | --- |
| 1 | Momentum | Continue a very small move down in both coordinates after repeated improvement. |
| 2 | Refine | Return very close to the Week 6 historical best after Week 7 dipped. |
| 3 | Refine | Stay close to the Week 6 best, avoiding the wider raw GP candidate. |
| 4 | Momentum | Continue the successful small increase in `x4`, with tiny supporting moves in `x2` and `x3`. |
| 5 | Momentum | Continue the proven monotonic trend: lower `x1`, raise `x2`, `x3`, and `x4`. |
| 6 | Momentum | Exploit the Week 7 recovery win with a tiny local probe, not the wider RF move. |
| 7 | Momentum | Continue the successful trajectory from Weeks 4 to 7. |
| 8 | Recovery | Reset around the Week 2 best basin and make only a tiny diagnostic-informed perturbation. |

## Final Week 8 Inputs
| Function | Submission |
| --- | --- |
| 1 | `0.729400-0.728800` |
| 2 | `0.696500-0.934500` |
| 3 | `0.491500-0.600500-0.344000` |
| 4 | `0.578600-0.429000-0.426000-0.255000` |
| 5 | `0.100000-0.970000-0.970000-0.980000` |
| 6 | `0.500600-0.326000-0.386500-0.892500-0.039500` |
| 7 | `0.054000-0.457000-0.246000-0.206000-0.314000-0.726000` |
| 8 | `0.092400-0.042400-0.053400-0.065450-0.564500-0.833600-0.064000-0.410100` |

## Check Summary
All final candidates are inside the relevant trust regions and have no boundary flags. The logistic regression and RBF SVM classifier checks classified all eight final candidates as inside the high-performing region. The neural-network surrogate remained conservative and did not predict most points above the historical best, but that is treated as a secondary caution rather than an override because the dataset is small and the strongest empirical evidence favours tight basin refinement.
