# State Policy Backtest Through Week10

This report replays historical week boundaries without future data leakage. It compares the current state-policy recommendation with the actual next submission, using locality and nearest-neighbour support as proxy checks. It does not know the true output of unsubmitted counterfactual points.

## Overall Summary
| Metric | Value |
| --- | --- |
| Replays | 72 |
| Policy candidate more local than actual | 9.72% |
| Mean nearest-neighbour support delta | -0.051 |

## By Function
| Function | Replays | More Local Rate | Support Delta | Actual Improvements | Latest State |
| --- | --- | --- | --- | --- | --- |
| 1 | 9 | 0.00% | -0.312 | 5 | momentum |
| 2 | 9 | 0.00% | -0.073 | 2 | recovery |
| 3 | 9 | 11.11% | 0.000 | 2 | momentum |
| 4 | 9 | 11.11% | 0.000 | 5 | momentum |
| 5 | 9 | 11.11% | 0.000 | 9 | momentum |
| 6 | 9 | 0.00% | -0.003 | 2 | momentum |
| 7 | 9 | 22.22% | 0.000 | 8 | momentum |
| 8 | 9 | 22.22% | -0.022 | 2 | recovery |

## Recent Replays
| Boundary | Function | State | Actual Improved | Policy Move | Actual Move | Support Delta |
| --- | --- | --- | --- | --- | --- | --- |
| week8 to week9 | 1 | momentum | yes | local | micro-local | -0.278 |
| week8 to week9 | 2 | stagnant | no | local | local | 0.000 |
| week8 to week9 | 3 | stagnant | yes | wide-local | micro-local | 0.000 |
| week8 to week9 | 4 | momentum | yes | local | micro-local | 0.000 |
| week8 to week9 | 5 | momentum | yes | local | micro-local | 0.000 |
| week8 to week9 | 6 | refine | yes | local | micro-local | -0.071 |
| week8 to week9 | 7 | momentum | yes | local | micro-local | 0.000 |
| week8 to week9 | 8 | recovery | no | local | micro-local | 0.000 |
| week9 to week10 | 1 | momentum | yes | local | micro-local | -0.316 |
| week9 to week10 | 2 | recovery | no | local | micro-local | -0.316 |
| week9 to week10 | 3 | momentum | no | local | micro-local | 0.000 |
| week9 to week10 | 4 | momentum | yes | local | micro-local | 0.000 |
| week9 to week10 | 5 | momentum | yes | local | micro-local | 0.000 |
| week9 to week10 | 6 | momentum | no | local | micro-local | -0.034 |
| week9 to week10 | 7 | momentum | yes | local | micro-local | 0.000 |
| week9 to week10 | 8 | recovery | yes | local | micro-local | 0.000 |

## Interpretation
- A positive support delta means the policy candidate sat nearer stronger historical neighbours than the actual submitted point.
- A high more-local rate means the policy would have stayed closer to the best-known basin than the actual submission.
- This backtest is best used as a guardrail against unnecessary basin jumps, not as proof that a counterfactual point would have produced a better portal output.
