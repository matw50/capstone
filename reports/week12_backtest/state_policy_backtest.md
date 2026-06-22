# State Policy Backtest Through Week12

This report replays historical week boundaries without future data leakage. It compares the current state-policy recommendation with the actual next submission, using locality and nearest-neighbour support as proxy checks. It does not know the true output of unsubmitted counterfactual points.

## Overall Summary
| Metric | Value |
| --- | --- |
| Replays | 88 |
| Policy candidate more local than actual | 7.95% |
| Mean nearest-neighbour support delta | -0.048 |

## By Function
| Function | Replays | More Local Rate | Support Delta | Actual Improvements | Latest State |
| --- | --- | --- | --- | --- | --- |
| 1 | 11 | 0.00% | -0.277 | 7 | momentum |
| 2 | 11 | 0.00% | -0.064 | 2 | recovery |
| 3 | 11 | 9.09% | 0.004 | 2 | stagnant |
| 4 | 11 | 9.09% | 0.000 | 7 | momentum |
| 5 | 11 | 9.09% | 0.000 | 11 | momentum |
| 6 | 11 | 0.00% | -0.018 | 2 | stagnant |
| 7 | 11 | 18.18% | 0.000 | 10 | momentum |
| 8 | 11 | 18.18% | -0.027 | 3 | refine |

## Recent Replays
| Boundary | Function | State | Actual Improved | Policy Move | Actual Move | Support Delta |
| --- | --- | --- | --- | --- | --- | --- |
| week10 to week11 | 1 | momentum | yes | local | micro-local | 0.000 |
| week10 to week11 | 2 | recovery | no | local | micro-local | -0.050 |
| week10 to week11 | 3 | refine | no | local | micro-local | 0.040 |
| week10 to week11 | 4 | momentum | yes | local | micro-local | 0.000 |
| week10 to week11 | 5 | momentum | yes | local | micro-local | 0.000 |
| week10 to week11 | 6 | refine | no | local | micro-local | -0.167 |
| week10 to week11 | 7 | momentum | yes | local | micro-local | 0.000 |
| week10 to week11 | 8 | momentum | no | local | micro-local | -0.060 |
| week11 to week12 | 1 | momentum | yes | local | micro-local | -0.238 |
| week11 to week12 | 2 | recovery | no | wide-local | local | 0.000 |
| week11 to week12 | 3 | stagnant | no | local | micro-local | 0.000 |
| week11 to week12 | 4 | momentum | yes | local | micro-local | 0.000 |
| week11 to week12 | 5 | momentum | yes | local | micro-local | 0.000 |
| week11 to week12 | 6 | stagnant | no | local | local | 0.000 |
| week11 to week12 | 7 | momentum | yes | local | micro-local | 0.000 |
| week11 to week12 | 8 | refine | yes | local | micro-local | -0.039 |

## Interpretation
- A positive support delta means the policy candidate sat nearer stronger historical neighbours than the actual submitted point.
- A high more-local rate means the policy would have stayed closer to the best-known basin than the actual submission.
- This backtest is best used as a guardrail against unnecessary basin jumps, not as proof that a counterfactual point would have produced a better portal output.
