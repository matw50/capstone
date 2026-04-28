# State Policy Backtest Through Week7

This report replays historical week boundaries without future data leakage. It compares the current state-policy recommendation with the actual next submission, using locality and nearest-neighbour support as proxy checks. It does not know the true output of unsubmitted counterfactual points.

## Overall Summary
| Metric | Value |
| --- | --- |
| Replays | 48 |
| Policy candidate more local than actual | 14.58% |
| Mean nearest-neighbour support delta | -0.049 |

## By Function
| Function | Replays | More Local Rate | Support Delta | Actual Improvements | Latest State |
| --- | --- | --- | --- | --- | --- |
| 1 | 6 | 0.00% | -0.330 | 2 | momentum |
| 2 | 6 | 0.00% | -0.057 | 2 | momentum |
| 3 | 6 | 16.67% | 0.000 | 1 | momentum |
| 4 | 6 | 16.67% | 0.000 | 2 | momentum |
| 5 | 6 | 16.67% | 0.000 | 6 | momentum |
| 6 | 6 | 0.00% | 0.013 | 1 | recovery |
| 7 | 6 | 33.33% | 0.000 | 5 | momentum |
| 8 | 6 | 33.33% | -0.018 | 1 | recovery |

## Recent Replays
| Boundary | Function | State | Actual Improved | Policy Move | Actual Move | Support Delta |
| --- | --- | --- | --- | --- | --- | --- |
| week5 to week6 | 1 | recovery | yes | wide-local | micro-local | -0.133 |
| week5 to week6 | 2 | momentum | yes | local | micro-local | 0.000 |
| week5 to week6 | 3 | recovery | yes | local | micro-local | 0.000 |
| week5 to week6 | 4 | recovery | yes | local | micro-local | 0.000 |
| week5 to week6 | 5 | momentum | yes | local | micro-local | 0.000 |
| week5 to week6 | 6 | recovery | no | local | local | 0.080 |
| week5 to week6 | 7 | momentum | yes | local | micro-local | 0.000 |
| week5 to week6 | 8 | recovery | no | local | micro-local | -0.044 |
| week6 to week7 | 1 | momentum | yes | local | micro-local | -0.188 |
| week6 to week7 | 2 | momentum | no | local | micro-local | -0.188 |
| week6 to week7 | 3 | momentum | no | local | micro-local | 0.000 |
| week6 to week7 | 4 | momentum | yes | local | micro-local | 0.000 |
| week6 to week7 | 5 | momentum | yes | local | micro-local | 0.000 |
| week6 to week7 | 6 | recovery | yes | local | micro-local | 0.000 |
| week6 to week7 | 7 | momentum | yes | local | micro-local | 0.000 |
| week6 to week7 | 8 | recovery | no | local | micro-local | -0.065 |

## Interpretation
- A positive support delta means the policy candidate sat nearer stronger historical neighbours than the actual submitted point.
- A high more-local rate means the policy would have stayed closer to the best-known basin than the actual submission.
- This backtest is best used as a guardrail against unnecessary basin jumps, not as proof that a counterfactual point would have produced a better portal output.
