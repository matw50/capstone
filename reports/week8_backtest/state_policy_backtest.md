# State Policy Backtest Through Week8

This report replays historical week boundaries without future data leakage. It compares the current state-policy recommendation with the actual next submission, using locality and nearest-neighbour support as proxy checks. It does not know the true output of unsubmitted counterfactual points.

## Overall Summary
| Metric | Value |
| --- | --- |
| Replays | 56 |
| Policy candidate more local than actual | 12.50% |
| Mean nearest-neighbour support delta | -0.048 |

## By Function
| Function | Replays | More Local Rate | Support Delta | Actual Improvements | Latest State |
| --- | --- | --- | --- | --- | --- |
| 1 | 7 | 0.00% | -0.316 | 3 | momentum |
| 2 | 7 | 0.00% | -0.049 | 2 | refine |
| 3 | 7 | 14.29% | 0.000 | 1 | refine |
| 4 | 7 | 14.29% | 0.000 | 3 | momentum |
| 5 | 7 | 14.29% | 0.000 | 7 | momentum |
| 6 | 7 | 0.00% | 0.011 | 1 | momentum |
| 7 | 7 | 28.57% | 0.000 | 6 | momentum |
| 8 | 7 | 28.57% | -0.028 | 1 | recovery |

## Recent Replays
| Boundary | Function | State | Actual Improved | Policy Move | Actual Move | Support Delta |
| --- | --- | --- | --- | --- | --- | --- |
| week6 to week7 | 1 | momentum | yes | local | micro-local | -0.188 |
| week6 to week7 | 2 | momentum | no | local | micro-local | -0.188 |
| week6 to week7 | 3 | momentum | no | local | micro-local | 0.000 |
| week6 to week7 | 4 | momentum | yes | local | micro-local | 0.000 |
| week6 to week7 | 5 | momentum | yes | local | micro-local | 0.000 |
| week6 to week7 | 6 | recovery | yes | local | micro-local | 0.000 |
| week6 to week7 | 7 | momentum | yes | local | micro-local | 0.000 |
| week6 to week7 | 8 | recovery | no | local | micro-local | -0.065 |
| week7 to week8 | 1 | momentum | yes | local | micro-local | -0.235 |
| week7 to week8 | 2 | refine | no | local | micro-local | 0.000 |
| week7 to week8 | 3 | refine | no | local | micro-local | 0.000 |
| week7 to week8 | 4 | momentum | yes | local | micro-local | 0.000 |
| week7 to week8 | 5 | momentum | yes | local | micro-local | 0.000 |
| week7 to week8 | 6 | momentum | no | local | micro-local | 0.000 |
| week7 to week8 | 7 | momentum | yes | micro-local | micro-local | 0.000 |
| week7 to week8 | 8 | recovery | no | local | micro-local | -0.085 |

## Interpretation
- A positive support delta means the policy candidate sat nearer stronger historical neighbours than the actual submitted point.
- A high more-local rate means the policy would have stayed closer to the best-known basin than the actual submission.
- This backtest is best used as a guardrail against unnecessary basin jumps, not as proof that a counterfactual point would have produced a better portal output.
