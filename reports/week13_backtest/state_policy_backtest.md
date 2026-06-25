# State Policy Backtest Through Week13

This report replays historical week boundaries without future data leakage. It compares the current state-policy recommendation with the actual next submission, using locality and nearest-neighbour support as proxy checks. It does not know the true output of unsubmitted counterfactual points.

## Overall Summary
| Metric | Value |
| --- | --- |
| Replays | 96 |
| Policy candidate more local than actual | 7.29% |
| Mean nearest-neighbour support delta | -0.046 |

## By Function
| Function | Replays | More Local Rate | Support Delta | Actual Improvements | Latest State |
| --- | --- | --- | --- | --- | --- |
| 1 | 12 | 0.00% | -0.254 | 8 | momentum |
| 2 | 12 | 0.00% | -0.070 | 2 | recovery |
| 3 | 12 | 8.33% | 0.006 | 2 | recovery |
| 4 | 12 | 8.33% | 0.000 | 8 | momentum |
| 5 | 12 | 8.33% | 0.000 | 12 | momentum |
| 6 | 12 | 0.00% | -0.021 | 3 | recovery |
| 7 | 12 | 16.67% | 0.000 | 11 | momentum |
| 8 | 12 | 16.67% | -0.031 | 4 | momentum |

## Recent Replays
| Boundary | Function | State | Actual Improved | Policy Move | Actual Move | Support Delta |
| --- | --- | --- | --- | --- | --- | --- |
| week11 to week12 | 1 | momentum | yes | local | micro-local | -0.238 |
| week11 to week12 | 2 | recovery | no | wide-local | local | 0.000 |
| week11 to week12 | 3 | stagnant | no | local | micro-local | 0.000 |
| week11 to week12 | 4 | momentum | yes | local | micro-local | 0.000 |
| week11 to week12 | 5 | momentum | yes | local | micro-local | 0.000 |
| week11 to week12 | 6 | stagnant | no | local | local | 0.000 |
| week11 to week12 | 7 | momentum | yes | local | micro-local | 0.000 |
| week11 to week12 | 8 | refine | yes | local | micro-local | -0.039 |
| week12 to week13 | 1 | momentum | yes | local | micro-local | 0.000 |
| week12 to week13 | 2 | recovery | no | wide-local | micro-local | -0.136 |
| week12 to week13 | 3 | recovery | no | local | micro-local | 0.037 |
| week12 to week13 | 4 | momentum | yes | local | micro-local | 0.000 |
| week12 to week13 | 5 | momentum | yes | local | micro-local | 0.000 |
| week12 to week13 | 6 | recovery | yes | local | micro-local | -0.062 |
| week12 to week13 | 7 | momentum | yes | local | micro-local | 0.000 |
| week12 to week13 | 8 | momentum | yes | local | micro-local | -0.077 |

## Interpretation
- A positive support delta means the policy candidate sat nearer stronger historical neighbours than the actual submitted point.
- A high more-local rate means the policy would have stayed closer to the best-known basin than the actual submission.
- This backtest is best used as a guardrail against unnecessary basin jumps, not as proof that a counterfactual point would have produced a better portal output.
