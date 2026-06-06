# Week 10 Approach

Status: submitted

## Main Principle
Week 10 continues the backtest-informed trust-region workflow. Week 9 was one of the strongest rounds so far, producing new bests for Functions 1, 3, 4, 5, 6, and 7. The main lesson was to continue micro-local exploitation where recent moves are working, while resetting the failed functions back toward their best known basins.

COCO/BBOB was not rerun for this round because the submission policy did not materially change. The weekly default remains capstone-specific diagnostics, historical backtesting, candidate sanity checks, classifier checks, and manual basin-aware blending.

## Function Treatment
| Function | State | Week 10 Treatment |
| --- | --- | --- |
| 1 | Momentum | Continue the tiny decreasing trend in both coordinates. |
| 2 | Recovery | Reset close to the Week 6 best after the Week 9 bounded alternative failed. |
| 3 | Momentum | Continue a very small basin-preserving move from the Week 9 best. |
| 4 | Momentum | Continue the successful small `x4` increase. |
| 5 | Momentum | Continue the monotonic trend toward lower `x1` and higher `x2`/`x3`/`x4`. |
| 6 | Momentum | Stay extremely close to the Week 9 best after the return-to-basin move worked. |
| 7 | Momentum | Continue the successful recent trajectory with a small step. |
| 8 | Recovery | Stay tightly anchored around the Week 2 best basin. |

## Final Week 10 Inputs
| Function | Submission |
| --- | --- |
| 1 | `0.728800-0.727400` |
| 2 | `0.695500-0.933000` |
| 3 | `0.490200-0.597000-0.345500` |
| 4 | `0.579200-0.429200-0.426200-0.259000` |
| 5 | `0.080000-0.980000-0.980000-0.990000` |
| 6 | `0.500100-0.324200-0.385200-0.893800-0.038700` |
| 7 | `0.056000-0.443000-0.250000-0.210000-0.326000-0.722000` |
| 8 | `0.092100-0.042300-0.053200-0.065300-0.565100-0.833200-0.064200-0.409800` |

## Check Summary
All final candidates are inside trust region. Logistic regression and RBF SVM checks classified all eight as high-region candidates. Function 5 is near the upper boundary on `x4`, but that is supported by repeated monotonic improvements, so the boundary flag was accepted rather than treated as a blocker.
