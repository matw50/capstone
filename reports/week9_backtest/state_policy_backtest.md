# State Policy Backtest Through Week9

This report replays historical week boundaries without future data leakage. It compares the current state-policy recommendation with the actual next submission, using locality and nearest-neighbour support as proxy checks. It does not know the true output of unsubmitted counterfactual points.

## Overall Summary
| Metric | Value |
| --- | --- |
| Replays | 64 |
| Policy candidate more local than actual | 10.94% |
| Mean nearest-neighbour support delta | -0.047 |

## By Function
| Function | Replays | More Local Rate | Support Delta | Actual Improvements | Latest State |
| --- | --- | --- | --- | --- | --- |
| 1 | 8 | 0.00% | -0.312 | 4 | momentum |
| 2 | 8 | 0.00% | -0.043 | 2 | stagnant |
| 3 | 8 | 12.50% | 0.000 | 2 | stagnant |
| 4 | 8 | 12.50% | 0.000 | 4 | momentum |
| 5 | 8 | 12.50% | 0.000 | 8 | momentum |
| 6 | 8 | 0.00% | 0.001 | 2 | refine |
| 7 | 8 | 25.00% | 0.000 | 7 | momentum |
| 8 | 8 | 25.00% | -0.024 | 1 | recovery |

## Recent Replays
| Boundary | Function | State | Actual Improved | Policy Move | Actual Move | Support Delta |
| --- | --- | --- | --- | --- | --- | --- |
| week7 to week8 | 1 | momentum | yes | local | micro-local | -0.235 |
| week7 to week8 | 2 | refine | no | local | micro-local | 0.000 |
| week7 to week8 | 3 | refine | no | local | micro-local | 0.000 |
| week7 to week8 | 4 | momentum | yes | local | micro-local | 0.000 |
| week7 to week8 | 5 | momentum | yes | local | micro-local | 0.000 |
| week7 to week8 | 6 | momentum | no | local | micro-local | 0.000 |
| week7 to week8 | 7 | momentum | yes | micro-local | micro-local | 0.000 |
| week7 to week8 | 8 | recovery | no | local | micro-local | -0.085 |
| week8 to week9 | 1 | momentum | yes | local | micro-local | -0.278 |
| week8 to week9 | 2 | stagnant | no | local | local | 0.000 |
| week8 to week9 | 3 | stagnant | yes | wide-local | micro-local | 0.000 |
| week8 to week9 | 4 | momentum | yes | local | micro-local | 0.000 |
| week8 to week9 | 5 | momentum | yes | local | micro-local | 0.000 |
| week8 to week9 | 6 | refine | yes | local | micro-local | -0.071 |
| week8 to week9 | 7 | momentum | yes | local | micro-local | 0.000 |
| week8 to week9 | 8 | recovery | no | local | micro-local | 0.000 |

## Interpretation
- A positive support delta means the policy candidate sat nearer stronger historical neighbours than the actual submitted point.
- A high more-local rate means the policy would have stayed closer to the best-known basin than the actual submission.
- This backtest is best used as a guardrail against unnecessary basin jumps, not as proof that a counterfactual point would have produced a better portal output.
