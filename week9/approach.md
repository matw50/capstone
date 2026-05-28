# Week 9 Approach

Status: submitted

## Main Principle
Week 9 uses the same backtest-informed trust-region workflow as Week 8, but adapts the state of each function based on the returned Week 8 outputs.

The Week 8 results created new bests for Functions 1, 4, 5, and 7, so those remain momentum cases. Functions 2 and 3 have now missed twice after their Week 6 bests, so they are treated as stagnant cases. Function 6 missed after its Week 7 recovery win, so it is a refine case anchored tightly on the Week 7 best. Function 8 remains a recovery case around the Week 2 best basin.

## Function Treatment
| Function | State | Week 9 Treatment |
| --- | --- | --- |
| 1 | Momentum | Continue an ultra-small decrease in both coordinates near the Week 8 best. |
| 2 | Stagnant | Accept one bounded alternative from the raw GP local-exploit candidate. |
| 3 | Stagnant | Stay close to the Week 6/Week 8 basin rather than taking the wider raw move. |
| 4 | Momentum | Continue the small successful `x4` increase with tiny supporting moves. |
| 5 | Momentum | Continue the monotonic trend: lower `x1`, raise `x2`, `x3`, and `x4`. |
| 6 | Refine | Return almost exactly to the Week 7 best basin after Week 8 missed. |
| 7 | Momentum | Continue the successful trend from Weeks 4 to 8. |
| 8 | Recovery | Stay tightly anchored around the Week 2 best basin. |

## Final Week 9 Inputs
| Function | Submission |
| --- | --- |
| 1 | `0.729100-0.728100` |
| 2 | `0.685699-0.956934` |
| 3 | `0.490800-0.598500-0.345000` |
| 4 | `0.578900-0.429100-0.426100-0.257000` |
| 5 | `0.090000-0.975000-0.975000-0.985000` |
| 6 | `0.500200-0.324500-0.385500-0.893500-0.038800` |
| 7 | `0.055000-0.450000-0.248000-0.208000-0.320000-0.724000` |
| 8 | `0.091800-0.042100-0.053600-0.065600-0.565600-0.832900-0.062900-0.409600` |

## Check Summary
All final candidates are inside the relevant trust regions and have no boundary flags. Logistic regression and RBF SVM checks classified all eight candidates as high-region. The neural-network surrogate remained conservative for most candidates, so it was treated as a secondary caution signal rather than an override.
