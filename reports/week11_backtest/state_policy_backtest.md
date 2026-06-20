# State Policy Backtest Through Week11

This report replays historical week boundaries without future data leakage. It compares the current state-policy recommendation with the actual next submission, using locality and nearest-neighbour support as proxy checks. It does not know the true output of unsubmitted counterfactual points.

## Overall Summary
| Metric | Value |
| --- | --- |
| Replays | 80 |
| Policy candidate more local than actual | 8.75% |
| Mean nearest-neighbour support delta | -0.049 |

## By Function
| Function | Replays | More Local Rate | Support Delta | Actual Improvements | Latest State |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | 0.00% | -0.281 | 6 | momentum |
| 2 | 10 | 0.00% | -0.071 | 2 | recovery |
| 3 | 10 | 10.00% | 0.004 | 2 | refine |
| 4 | 10 | 10.00% | 0.000 | 6 | momentum |
| 5 | 10 | 10.00% | 0.000 | 10 | momentum |
| 6 | 10 | 0.00% | -0.019 | 2 | refine |
| 7 | 10 | 20.00% | 0.000 | 9 | momentum |
| 8 | 10 | 20.00% | -0.025 | 2 | momentum |

## Recent Replays
| Boundary | Function | State | Actual Improved | Policy Move | Actual Move | Support Delta |
| --- | --- | --- | --- | --- | --- | --- |
| week9 to week10 | 1 | momentum | yes | local | micro-local | -0.316 |
| week9 to week10 | 2 | recovery | no | local | micro-local | -0.316 |
| week9 to week10 | 3 | momentum | no | local | micro-local | 0.000 |
| week9 to week10 | 4 | momentum | yes | local | micro-local | 0.000 |
| week9 to week10 | 5 | momentum | yes | local | micro-local | 0.000 |
| week9 to week10 | 6 | momentum | no | local | micro-local | -0.034 |
| week9 to week10 | 7 | momentum | yes | local | micro-local | 0.000 |
| week9 to week10 | 8 | recovery | yes | local | micro-local | 0.000 |
| week10 to week11 | 1 | momentum | yes | local | micro-local | 0.000 |
| week10 to week11 | 2 | recovery | no | local | micro-local | -0.050 |
| week10 to week11 | 3 | refine | no | local | micro-local | 0.040 |
| week10 to week11 | 4 | momentum | yes | local | micro-local | 0.000 |
| week10 to week11 | 5 | momentum | yes | local | micro-local | 0.000 |
| week10 to week11 | 6 | refine | no | local | micro-local | -0.167 |
| week10 to week11 | 7 | momentum | yes | local | micro-local | 0.000 |
| week10 to week11 | 8 | momentum | no | local | micro-local | -0.060 |

## Interpretation
- A positive support delta means the policy candidate sat nearer stronger historical neighbours than the actual submitted point.
- A high more-local rate means the policy would have stayed closer to the best-known basin than the actual submission.
- This backtest is best used as a guardrail against unnecessary basin jumps, not as proof that a counterfactual point would have produced a better portal output.
